import os
import re
import glob
import sys
from pathlib import Path
from typing import Dict, Set
import logging

# 解決 Windows 繁體中文環境 cp950 / UTF-8 終端機顯示 Emoji 的編碼崩潰問題
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ====================== 日誌設定 ======================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("DROS.DNA_Enricher")

# ====================== 配置 ======================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
VAULT_PATH = BASE_DIR / "Vault_DajueZang"
CORE_PATH = BASE_DIR / "core"

def find_vault_index() -> Path | None:
    """尋找大覺藏索引檔案"""
    index_patterns = [
        VAULT_PATH / "0-大覺藏集索引.md",
        VAULT_PATH / "**/0-大覺藏集索引.md"
    ]
    for pattern in index_patterns:
        for file in glob.glob(str(pattern), recursive=True):
            return Path(file)
    return None

def build_title_map(index_path: Path) -> Dict[str, str]:
    """建立 {經典名稱: T-編號} 映射表"""
    if not index_path or not index_path.exists():
        logger.warning(f"找不到大覺藏索引檔案: {index_path}")
        return {}

    title_map = {}
    pattern = re.compile(r'\[(T\d{4}[a-zA-Z]?)[ _]?[《]?([^》\]]+)[》]?\]')

    with open(index_path, 'r', encoding='utf-8') as f:
        for line in f:
            matches = pattern.findall(line)
            for t_id, title in matches:
                clean_title = title.strip()
                title_map[clean_title] = t_id
                # 增加常見變體
                if "經" in clean_title:
                    title_map[clean_title.replace("經", "")] = t_id

    logger.info(f"成功載入 {len(title_map)} 個經典 T-編號映射")
    return title_map

def enrich_nodes(title_map: Dict[str, str], dry_run: bool = False) -> int:
    """核心：為 CORE 節點注入 T-座標 (具備冪等性防護)"""
    if not CORE_PATH.exists():
        logger.error(f"Core 目錄不存在: {CORE_PATH}")
        return 0

    md_files = list(CORE_PATH.rglob("*.md"))
    enriched_count = 0
    skipped_count = 0

    for file_path in md_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 【防禦升級】：冪等性 (Idempotency) 檢查
            # 如果已經注入過真理座標，則直接跳過，避免重複寫入
            if "> [!NOTE] AI 真理座標:" in content:
                skipped_count += 1
                continue
                
            original_content = content

            # 找出檔案中出現的經典名稱
            found_t_ids: Set[str] = set()
            for title, t_id in title_map.items():
                if len(title) >= 3 and title in content:
                    found_t_ids.add(t_id)

            if not found_t_ids:
                continue

            coord_tag = f"\n> [!NOTE] AI 真理座標: {', '.join(sorted(found_t_ids))}\n"

            # 尋找最佳注入位置
            if "> [!QUOTE]" in content:
                # 在第一個 [!QUOTE] 區塊後注入
                content = re.sub(
                    r'(\[!QUOTE\].*?)(?=\n\n|\Z)', 
                    rf'\1{coord_tag}', 
                    content, 
                    count=1, 
                    flags=re.S
                )
            else:
                # 否則在檔案前端 Meta 區塊後注入
                content = re.sub(
                    r'^(---.*?\n---\n)', 
                    rf'\1{coord_tag}', 
                    content, 
                    count=1, 
                    flags=re.S
                ) or (coord_tag + content)

            if content != original_content:
                if not dry_run:
                    file_path.write_text(content, encoding='utf-8')
                enriched_count += 1
                
                if enriched_count % 200 == 0:
                    logger.info(f"已處理 {enriched_count} 個節點...")

        except Exception as e:
            logger.error(f"處理失敗 {file_path.name}: {e}")

    logger.info(f"[OK] DNA 座標注入完成！共硬化 {enriched_count} 個核心節點 (已跳過 {skipped_count} 個既有節點)")
    return enriched_count


def main():
    print("=" * 60)
    print("DROS 7.0 Nirvana Edition - 金剛 DNA 注射器 v2.1")
    print("=" * 60)

    index_path = find_vault_index()
    if not index_path:
        logger.error("[ERROR] 未找到大覺藏索引檔案，請確認 Vault_DajueZang 已正確放置")
        sys.exit(1)

    title_map = build_title_map(index_path)
    if not title_map:
        logger.error("[ERROR] 無法建立 T-編號映射表")
        sys.exit(1)

    enriched = enrich_nodes(title_map, dry_run=False)
    
    print("\n[OK] 金剛注射器執行完畢！")
    print(f"   處理節點數：{enriched}")
    print(f"   索引來源：{index_path.name}")


if __name__ == "__main__":
    main()
