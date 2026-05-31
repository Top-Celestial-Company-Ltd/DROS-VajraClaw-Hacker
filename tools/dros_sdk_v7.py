import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

from dros_contract_ast import InferenceContract
from dros_guard_vm import GuardVM

class DrosEngine:
    """
    DROS 7.0 核心引擎 - 工業級定稿版
    特點：輕量化記憶體索引、自適應配置管理、防彈節點載入
    """
    
    def __init__(self, core_path: str):
        self.core_path = Path(core_path)
        self.index = self._build_index()
        
        # 配置載入 (預設採用極速、高性價比的 2.5-flash-lite，將高算力保留給進階契約)
        self.model_id = os.getenv("DROS_MODEL_ID", "gemini-2.5-flash-lite")
        self.temperature = float(os.getenv("DROS_TEMPERATURE", 0.1))
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_base = os.getenv("DROS_API_BASE", "") # 支援廠商中立的萬能轉接頭
        
        print(f"🚀 DROS 7.0 Engine 初始化完成")
        print(f"   - Core Path: {self.core_path}")
        print(f"   - Default Model: {self.model_id}")
        print(f"   - Indexed Nodes: {len(self.index)}")

    def _build_index(self) -> Dict[str, Path]:
        """建立輕量記憶體索引，大幅提升檢索速度，極低 RAM 佔用"""
        index = {}
        for md_file in self.core_path.rglob("*.md"):
            stem = md_file.stem
            index[stem.lower()] = md_file
            # 支援多種命名方式 (例如去除底線，增加容錯)
            index[stem.replace("_", "").lower()] = md_file
        return index

    def retrieve_nodes(self, query: str, contract: InferenceContract, top_k: int = 8) -> List[Dict]:
        """智慧檢索 - 支援模糊匹配與權重"""
        query_lower = query.lower().strip()
        candidates = []

        for name, path in self.index.items():
            score = 0
            if query_lower in name:
                score += 15
            elif any(word in name for word in query_lower.split()):
                score += 8
            
            if score > 0:
                candidates.append((score, name, path))

        # 排序並取 top_k
        candidates.sort(reverse=True)
        results = []
        
        for _, name, path in candidates[:top_k]:
            node = self._load_node_safe(path)
            if node:
                results.append(node)

        return results

    def _load_node_safe(self, filepath: Path) -> Optional[Dict]:
        """安全載入節點，提取結構化內容 (防彈設計，單一損毀不影響全域)"""
        try:
            content = filepath.read_text(encoding='utf-8')
            name = filepath.stem

            # 提取核心義理
            summary_match = re.search(
                r"> \[!NOTE\] (?:核心義理|歷史精鍊|AI 真理座標).*?(?:\n> .*?)+", 
                content, re.S
            )
            # 提取權威引用
            quote_match = re.search(
                r"> \[!QUOTE\].*?(?:\n> .*?)+", 
                content, re.S
            )

            return {
                "name": name,
                "path": str(filepath),
                "summary": summary_match.group(0) if summary_match else "",
                "quote": quote_match.group(0) if quote_match else "",
                "has_authority": bool(quote_match)
            }
        except Exception as e:
            print(f"⚠️ 載入節點失敗 {filepath.name}: {e}")
            return None

    def ask(self, query: str, contract: InferenceContract):
        """主要查詢入口"""
        # 1. 檢索
        nodes = self.retrieve_nodes(query, contract)
        if not nodes:
            return {"status": "error", "reason": "NO_RELEVANT_NODES_FOUND"}

        # 2. 決定運行模式
        has_strong_authority = any(n["has_authority"] for n in nodes)
        runtime_mode = contract.InferenceMode if has_strong_authority else getattr(contract, 'Fallback', 'Bodhisattva')

        # 3. GuardVM 驗證準備
        vm = GuardVM(contract)

        # 4. Mock 輸出生成 (後續可在此替換為真實 API 呼叫，傳入 self.api_base 與 self.model_id)
        mock_output = f"根據 DROS 節點檢索結果，以下為針對「{query}」的法義闡述：\n\n"

        for node in nodes[:3]:
            if node["summary"]:
                mock_output += f"**[[{node['name']}]]**\n{node['summary'][:500]}...\n\n"

        # 5. GuardVM 最終把關
        verify_result = vm.verify(mock_output)
        
        if verify_result["passed"]:
            return {
                "status": "success",
                "runtime_mode": runtime_mode,
                "content": mock_output,
                "sources": [n["name"] for n in nodes[:5]],
                "model_used": getattr(contract, 'ComputeEngine', {}).get('Model', self.model_id) # 支援契約覆寫算力
            }
        else:
            return {
                "status": "fallback",
                "runtime_mode": "Bodhisattva",
                "content": vm.apply_fallback(mock_output),
                "issues": verify_result["issues"]
            }
