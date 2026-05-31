import os
import re
import glob
import sys

# 強制 UTF-8 輸出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# DROS 2.0 DNA Enricher v5.5
# 功能：解析大覺藏索引，為 CORE 節點注入 T-編號座標，消除 AI 幻覺。

# 自動定位大覺藏索引路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_SEARCH_PATH = os.path.join(BASE_DIR, "Vault_DajueZang")
CORE_PATH = os.path.join(BASE_DIR, "core")

def find_vault_index():
    """在 Vault_DajueZang 中遞迴搜尋索引檔"""
    for root, dirs, files in os.walk(VAULT_SEARCH_PATH):
        if "0-大覺藏集索引.md" in files:
            return os.path.join(root, "0-大覺藏集索引.md")
    return None

VAULT_INDEX = find_vault_index()

def build_title_map():
    """解析索引，建立 {經名: T-編號} 映射表"""
    title_map = {}
    if not VAULT_INDEX or not os.path.exists(VAULT_INDEX):
        print(f"【系統提示】在大覺藏預留區 ({VAULT_SEARCH_PATH}) 找不到索引檔案。")
        print("請確保您已將大覺藏集解壓縮至 Vault_DajueZang 資料夾內。")
        return {}
    
    # 匹配模式: [T0001_《長阿含經》]
    pattern = re.compile(r'\[(T\d{4}[a-z]?)_《?([^》\]]+)》?\]')
    with open(VAULT_INDEX, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                t_id = match.group(1)
                title = match.group(2)
                title_map[title] = t_id
    return title_map

def enrich_nodes(title_map):
    """遍歷 CORE 節點並注入座標"""
    md_files = glob.glob(os.path.join(CORE_PATH, "**", "*.md"), recursive=True)
    count = 0
    
    # 預先定義一些常見經典的縮寫或全稱對應
    common_titles = list(title_map.keys())
    
    for file_path in md_files:
        modified = False
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            content = "".join(lines)
            found_t_ids = set()
            
            # 1. 偵測內容中的經典名稱
            for title in common_titles:
                if len(title) < 3: continue # 避開太短的詞
                if title in content:
                    found_t_ids.add(title_map[title])
            
            if not found_t_ids: continue
            
            # 2. 準備注入的標籤
            coord_tag = f"\n> [!NOTE] AI 真理座標: {', '.join(sorted(found_t_ids))}\n"
            
            # 3. 尋找注入位置 (通常在 [!QUOTE] 區塊後，或檔案末尾)
            new_lines = []
            in_quote = False
            injected = False
            
            for line in lines:
                new_lines.append(line)
                if "[!QUOTE]" in line:
                    in_quote = True
                if in_quote and line.strip() == "" and not injected:
                    new_lines.append(coord_tag)
                    injected = True
                    in_quote = False
                    modified = True
            
            # 如果沒找到 [!QUOTE]，就加在最前面 (Meta 區塊下方)
            if not injected:
                new_lines.insert(2, coord_tag)
                modified = True
            
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                count += 1
                if count % 100 == 0:
                    print(f"INFO: Processed {count} nodes...")
            
        except Exception as e:
            print(f"ERROR: Failed processing {file_path}: {e}")
            
    return count

if __name__ == "__main__":
    print("START: Starting DROS 2.0 DNA Enrichment Plan...")
    t_map = build_title_map()
    print(f"SUCCESS: Read {len(t_map)} Vault coordinate mappings.")
    total = enrich_nodes(t_map)
    print(f"DONE: Task completed! Enriched {total} core nodes with truth coordinates.")
