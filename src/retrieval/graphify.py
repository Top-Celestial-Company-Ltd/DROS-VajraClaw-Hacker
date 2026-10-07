"""
DROS 7.2 Graphify v2.6 - 剛柔並濟語義圖譜檢索引擎 (相容且強化版)
目標：融合 v1.0 的嚴格目錄排除與相容性，以及 v2.0 的多維度權重排序與標籤提取
"""

import re
import time
import sys
import logging
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Optional

from src.config import config

logger = logging.getLogger("DROS.Graphify")


class GraphifyRetriever:
    """Graphify v2.6 核心相容暨大覺藏座標直連增強型檢索引擎"""
    
    def __init__(self, core_path: Optional[Path] = None):
        self.core_path = Path(core_path or config.core_path)
        self.index = {
            "nodes": {},           # node_name_lower -> file_path
            "keywords": defaultdict(list),  # keyword -> [node_names]
            "t_coordinates": defaultdict(list),  # t_id_lower -> [node_names] (O(1) 座標直接映射表)
            "cross_refs": defaultdict(set)  # 拓撲關聯
        }
        self.build_index()

    def build_index(self):
        """建立增強型索引 (融合 v1.0 的嚴格目錄排除，杜絕重複源污染，內建效能監控)"""
        start_time = time.perf_counter()
        logger.info("正在建立 Graphify v2.6 索引...")
        
        # 嚴格排除目錄名單 (全小寫)
        EXCLUDE_DIRS = {
            "long_classics", 
            "system_docs", 
            "pavilion_sandbox", 
            "pavilion_digital", 
            "user_pavilion",
            "backups",
            "backup",
            "tempbackupcheck",
            "temp_refine",
            "temp_refine_single",
            "temp_run"
        }

        count = 0
        for md_file in self.core_path.rglob("*.md"):
            # 取得相對於 core_path 的父目錄名稱，進行小寫比對過濾
            relative_parts = [p.lower() for p in md_file.relative_to(self.core_path).parts[:-1]]
            
            should_exclude = False
            for part in relative_parts:
                if (part in EXCLUDE_DIRS or 
                    "backup" in part or 
                    "temp" in part or 
                    "sandbox" in part or 
                    "pavilion" in part or
                    "long_classics" in part or
                    "system_docs" in part):
                    should_exclude = True
                    break
            
            if should_exclude:
                continue

            node_name = md_file.stem
            self.index["nodes"][node_name.lower()] = md_file
            count += 1

            try:
                # 1. 優先提取節點名稱本身的 N-Gram（極致高保真義理名相，100% 無雜音）
                name_ngrams = self._extract_ngrams(node_name)
                for ngram in name_ngrams:
                    self.index["keywords"][ngram].append(node_name)

                # 2. 僅讀取前 300 字（核心義理摘要），相較 3000 字降低 90% 以上的記憶體與啟動效能負擔
                content = md_file.read_text(encoding='utf-8')[:300]
                
                # 提取摘要中的中文 N-Gram
                content_ngrams = self._extract_ngrams(content)
                for ngram in content_ngrams:
                    self.index["keywords"][ngram].append(node_name)
                
                # 3. 提取括號內的重要標註（如 [!NOTE]、[!QUOTE] 後的關鍵詞）
                tags = re.findall(r'\[\!.*?\](.*?)[\n\r]', content)
                for tag in tags:
                    tag_ngrams = self._extract_ngrams(tag)
                    for ngram in tag_ngrams:
                        self.index["keywords"][ngram].append(node_name)

                # 4. 提取 T-編號 真理座標，建立 O(1) 座標對齊索引表
                t_ids = re.findall(r'T\d{4}[a-zA-Z]?', content)
                for t_id in t_ids:
                    self.index["t_coordinates"][t_id.lower()].append(node_name)
                        
            except Exception:
                continue

        duration = time.perf_counter() - start_time
        
        # 估算索引大略記憶體開銷 (字典結構本身 + key-value 估算)
        keywords_est_bytes = sys.getsizeof(self.index["keywords"]) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.index["keywords"].items())
        t_coords_est_bytes = sys.getsizeof(self.index["t_coordinates"]) + sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.index["t_coordinates"].items())

        logger.info(
            f"Graphify v2.6 索引建立完成 | 耗時: {duration:.4f} 秒 | "
            f"實際掛載節點: {len(self.index['nodes'])} | "
            f"關鍵詞索引: {len(self.index['keywords'])} (估計: {keywords_est_bytes / 1024:.2f} KB) | "
            f"座標索引: {len(self.index['t_coordinates'])} (估計: {t_coords_est_bytes / 1024:.2f} KB)"
        )

    # 常用口語虛詞與無意義詞過濾表 (保護記憶體與啟動效能，根治分詞雜音)
    STOP_WORDS = {
        "我們", "可以", "因為", "所以", "但是", "一個", "因此", "這個", "這些", "以及", 
        "而且", "如果", "沒有", "進行", "開始", "目前", "特別", "對於", "關於", "什麼",
        "這樣", "那樣", "這時", "那時", "由於", "就是", "也是", "有些", "其中", "不是",
        "那麼", "或者", "或是", "並且", "然後", "已經", "正在", "非常", "相當", "比較",
        "如何", "為何", "什麼時候", "哪裡", "因此", "因為", "所以", "並且", "可以", "有些"
    }

    def _extract_ngrams(self, text: str, min_len: int = 2, max_len: int = 4) -> List[str]:
        """高效率提取中文字元的 2~4 字 N-Gram（內建停用詞過濾）"""
        chinese_blocks = re.findall(r'[\u4e00-\u9fa5]+', text)
        ngrams = []
        for block in chinese_blocks:
            n = len(block)
            for length in range(min_len, min(max_len + 1, n + 1)):
                for i in range(n - length + 1):
                    word = block[i:i+length]
                    if word not in self.STOP_WORDS:
                        ngrams.append(word)
        return list(set(ngrams))

    def search(self, query: str, top_k: int = 10, min_score: float = 6.0) -> List[Dict]:
        """v2.6 強化檢索：極速座標匹配 + 多維度權重 + N-Gram 語義擴展 + 倒排匹配"""
        start_time = time.perf_counter()
        if not query or not query.strip():
            return []

        query_lower = query.lower().strip()
        score_dict = defaultdict(float)

        # 0. 座標精準匹配（O(1) 精準查表）
        query_t_ids = re.findall(r'[tT]\d{4}[a-zA-Z]?', query_lower)
        for q_t_id in query_t_ids:
            if q_t_id in self.index.get("t_coordinates", {}):
                for node_name in self.index["t_coordinates"][q_t_id]:
                    score_dict[node_name.lower()] += 40.0  # 提供超高的極致優先級

        # 1. 精準名稱匹配（最高權重）
        if query_lower in self.index["nodes"]:
            score_dict[query_lower] += 35

        # 提取查詢字句的 N-Gram
        query_ngrams = self._extract_ngrams(query)

        # 2. 關鍵詞 N-Gram 匹配
        for ngram in query_ngrams:
            if ngram in self.index["keywords"]:
                weight = len(ngram) * 4.5  # 2字=9分，3字=13.5分，4字=18分
                for node_name in self.index["keywords"][ngram]:
                    score_dict[node_name.lower()] += weight

        # 3. 模糊匹配與部分匹配
        for node_name in self.index["nodes"]:
            name_lower = node_name.lower()
            if query_lower in name_lower:
                score_dict[name_lower] += 22
            elif any(w in name_lower for w in query_ngrams):
                score_dict[name_lower] += 9

        # 排序並過濾
        sorted_results = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for node_name, score in sorted_results[:top_k]:
            if score >= min_score:
                node = self._load_node_detail(node_name, query)
                if node:
                    node["match_score"] = round(score, 1)
                    results.append(node)

        duration = time.perf_counter() - start_time
        logger.info(f"Graphify 檢索完成 | 查詢: '{query}' | 耗時: {duration * 1000:.2f} 毫秒 | 回傳結果數: {len(results)}")
        return results

    def _load_node_detail(self, node_name: str, query: str = "") -> Optional[Dict]:
        """載入節點詳細內容，若掛載大覺藏則動態加載與檢索詞最契合的原始經文段落"""
        path = self.index["nodes"].get(node_name.lower())
        if not path:
            return None

        try:
            content = path.read_text(encoding='utf-8')
            
            summary = re.search(r"> \[!NOTE\].*?(?:\n>.*)+", content, re.S)
            quote_match = re.search(r"> \[!QUOTE\].*?(?:\n>.*)+", content, re.S)

            summary_text = summary.group(0) if summary else ""
            quote_text = quote_match.group(0) if quote_match else ""

            # 若有啟用大覺藏且存在 T-座標，進行動態引文載入與精準切片
            vault_path = Path(config.vault_path)
            if vault_path.exists():
                t_ids = list(set(re.findall(r'T\d{4}[a-zA-Z]?', summary_text or content)))
                if t_ids:
                    dynamic_quotes = []
                    query_terms = self._extract_ngrams(query) if query else []
                    
                    for t_id in t_ids:
                        classic_file = self._find_classic_file(vault_path, t_id)
                        if classic_file and classic_file.exists():
                            segment = self._extract_relevant_segment(classic_file, query_terms)
                            if segment:
                                # 安全消毒與清洗
                                sanitized_segment = self._sanitize_content(segment)
                                dynamic_quotes.append(
                                    f"> [!QUOTE] 【大覺藏原典動態載入 ({t_id})】\n" + 
                                    "\n".join(f"> {line}" for line in sanitized_segment.split("\n"))
                                )
                            else:
                                logger.warning(f"大覺藏原典切片失敗 | 檔案: {classic_file} | 座標: {t_id}")
                                dynamic_quotes.append(
                                    f"> [!WARNING] 【大覺藏加載降級 ({t_id})】\n" +
                                    f"> *真理座標對應之經文段落切片失敗，已啟用安全降級守衛。*"
                                )
                        else:
                            logger.warning(f"找不到大覺藏原典檔案 | 座標: {t_id} | 路徑: {vault_path}")
                            dynamic_quotes.append(
                                f"> [!WARNING] 【大覺藏加載降級 ({t_id})】\n" +
                                f"> *大覺藏庫中查無與座標 {t_id} 匹配之經典檔案，已啟用安全降級守衛。*"
                            )
                    
                    if dynamic_quotes:
                        # 將動態載入的原典內容拼接到原有 quote_text 後方
                        dynamic_block = "\n\n".join(dynamic_quotes)
                        if quote_text:
                            quote_text += f"\n\n{dynamic_block}"
                        else:
                            quote_text = dynamic_block

            return {
                "name": path.stem,
                "path": str(path),
                "summary": summary_text,
                "quote": quote_text,
                "has_authority": bool(quote_text)
            }
        except Exception as e:
            logger.warning(f"載入節點失敗 {node_name}: {e}")
            return None

    def _find_classic_file(self, vault_path: Path, t_id: str) -> Optional[Path]:
        """在大覺藏庫中尋找與 T-編號 匹配的經文檔案（支持多種容錯匹配）"""
        try:
            t_id_clean = t_id.upper()
            # 遞迴尋找包含該 T-編號 的 .md 經文
            for p in vault_path.rglob(f"*{t_id_clean}*.md"):
                return p
        except Exception:
            pass
        return None

    def _extract_relevant_segment(self, file_path: Path, query_terms: List[str], max_chars: int = 800) -> str:
        """從原始經典中提取與關鍵字最相關的段落切片"""
        try:
            content = file_path.read_text(encoding='utf-8')
            # 移除 Front matter (開頭 YAML)
            content_clean = re.sub(r'^---.*?\n---\n', '', content, flags=re.S).strip()
            
            # 切分成段落
            paragraphs = [p.strip() for p in re.split(r'\n+', content_clean) if p.strip()]
            
            # 尋找匹配字數最多的段落
            best_para = None
            best_score = 0
            for para in paragraphs:
                # 避開標題與註解
                if para.startswith("---") or para.startswith("#"):
                    continue
                
                score = 0
                for term in query_terms:
                    if len(term) >= 2 and term in para:
                        score += len(term)
                
                if score > best_score:
                    best_score = score
                    best_para = para
            
            # 如果找到了包含關鍵字的段落，返回該段落以及前後的上下文（不超過 max_chars）
            if best_para:
                best_idx = paragraphs.index(best_para)
                selected = []
                
                # 向前看一段
                if best_idx > 0 and not paragraphs[best_idx-1].startswith("#"):
                    selected.append(paragraphs[best_idx-1])
                    
                selected.append(best_para)
                
                # 向後看一段
                if best_idx < len(paragraphs) - 1:
                    selected.append(paragraphs[best_idx+1])
                    
                segment = "\n\n".join(selected)
                if len(segment) > max_chars:
                    segment = segment[:max_chars] + "..."
                return segment
                
            # 若無匹配段落，則回退加載前 800 字
            if len(content_clean) > max_chars:
                return content_clean[:max_chars] + "..."
            return content_clean
        except Exception as e:
            return f"【大覺藏加載錯誤：{e}】"

    def _sanitize_content(self, text: str) -> str:
        """安全防禦：消毒並清洗經文段落內容，防止自訂 Vault 惡意注入或惡意標籤"""
        if not text:
            return ""
        # 1. 移除潛在的 HTML 標籤（如 <script>, <iframe> 等），防止前端注入渲染
        cleaned = re.sub(r'<[^>]+>', '', text)
        
        # 2. 過濾惡意的 Prompt Injection 注入特徵字句（如 'ignore previous', 'system prompt bypass' 等）
        cleaned = re.sub(
            r'(?i)(ignore\s+previous|system\s+prompt|bypass\s+instructions|忽略先前|繞過系統|你是\s*LLM)', 
            '[已安全消毒之異常指令]', 
            cleaned
        )
        
        # 3. 避免 markdown 連結中的 javascript: 協議等漏洞，防止 Markdown 渲染器攻擊
        cleaned = re.sub(r'\[([^\]]*)\]\(javascript:[^\)]*\)', r'[\1](#)', cleaned)
        
        return cleaned.strip()


# 便捷函數
def get_retriever() -> GraphifyRetriever:
    return GraphifyRetriever()
