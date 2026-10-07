import os
import re
import asyncio
import json
import sys
import subprocess
import tempfile

# --- 環境硬化 (Phase 1) ---
sys.stdout.reconfigure(encoding='utf-8')

# 自動偵測與動態解析專案根目錄，並強勢注入 sys.path 以防 ModuleNotFoundError
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(SCRIPT_DIR, "core")):
    VAULT_ROOT = SCRIPT_DIR
else:
    VAULT_ROOT = os.path.join(SCRIPT_DIR, "數位佛堂")
    if not os.path.exists(VAULT_ROOT):
        VAULT_ROOT = SCRIPT_DIR

if VAULT_ROOT not in sys.path:
    sys.path.insert(0, VAULT_ROOT)

from pathlib import Path
from src.config import config
from src.engine.contract import InferenceContract

from quart import Quart, request, jsonify, Response, make_response
from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="*")

NODE_EXE = "node"
GEMINI_JS = "gemini.js" # 已升級直連 SDK，此處保留作為中性相容標記

# --- 模型策略配置 (使用 CLI 自動熱對齊別名，未來自動升級最佳模型)
ROUTER_MODEL = "flash-lite"
SYNTHESIZER_MODEL = "pro"

# 內容淨化正則 (移除 ANSI 顏色與 CLI 標記)
CLEAN_REGEX = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\*\]|\[\+\]')

# --- Graphify v2.5 語義與倒排精準模糊匹配延遲初始化器 ---
_retriever_instance = None

def get_graphify_retriever():
    global _retriever_instance
    if _retriever_instance is None:
        try:
            from src.retrieval.graphify import GraphifyRetriever
            core_folder = os.path.join(VAULT_ROOT, "core")
            if os.path.exists(core_folder):
                _retriever_instance = GraphifyRetriever(core_folder)
            else:
                _retriever_instance = GraphifyRetriever(VAULT_ROOT)
        except Exception as e:
            print(f"  [!] 初始化 GraphifyRetriever 失敗: {e}")
    return _retriever_instance

async def get_node_content_async(core_nodes, related_nodes=[]):
    """從本機庫提取 Markdown 內容 (含 Token Watchdog 降維機制，整合 Graphify v2.5)"""
    context = ""
    total_len = 0
    
    def _read_file(name, is_core=True):
        nonlocal context, total_len
        
        paths_to_check = []
        
        # 1. 搜尋 DROS 7.0 架構 (core 分館)
        core_path = os.path.join(VAULT_ROOT, "core")
        if os.path.exists(core_path):
            for root, dirs, files in os.walk(core_path):
                if f"{name}.md" in files:
                    paths_to_check.append(os.path.join(root, f"{name}.md"))
                    break
        
        # 2. 若 core 找不到，搜尋 User_Pavilion
        if not paths_to_check:
            user_path = os.path.join(VAULT_ROOT, "User_Pavilion")
            if os.path.exists(user_path):
                for root, dirs, files in os.walk(user_path):
                    if f"{name}.md" in files:
                        paths_to_check.append(os.path.join(root, f"{name}.md"))
                        break
                        
        # 3. 🚨 DROS 7.2 核心升級：若前兩者均找不到，啟動 Graphify v2.5 進行語義與倒排精準模糊匹配！
        if not paths_to_check:
            r = get_graphify_retriever()
            if r:
                fuzzy_results = r.search(name, top_k=1, min_score=6.0)
                if fuzzy_results:
                    matched = fuzzy_results[0]
                    matched_path = matched["path"]
                    matched_name = matched["name"]
                    print(f"  [+] Graphify v2.5 語義對齊對應: '{name}' -> '{matched_name}' (分數: {matched['match_score']})")
                    paths_to_check.append(matched_path)
            
        for path in paths_to_check:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content_text = f.read()
                        
                        # DROS 7.0 升級：利用結構化標籤提取精華，減少 Token 消耗
                        summary_match = re.search(r"> \[!NOTE\] (?:核心義理|歷史精鍊).*?\n(?:> .*?\n)+", content_text, re.S)
                        quote_match = re.search(r"> \[(?:!QUOTE|!NOTE)\] (?:原典引文|跨館開採|語義融合).*?\n(?:> .*?\n)+", content_text, re.S)
                        
                        if summary_match or quote_match:
                            data = ""
                            if summary_match: data += summary_match.group(0) + "\n"
                            if quote_match: data += quote_match.group(0) + "\n"
                        else:
                            data = content_text # 若無標籤，則保留原文
                            
                        if not is_core:
                            if total_len > 12000:
                                print(f"  [!] Context Watchdog: 達硬上限 (12000字)，捨棄節點: {name}")
                                return True
                            elif total_len > 8000:
                                print(f"  [!] Context Watchdog: 超過警告線 (8000字)，啟動降維: {name}")
                                # 階梯降維：僅保留前 150 字作為推理路標
                                data = data[:150] + "\n... (Token 限制，內容已折疊)\n"
                                
                        context += f"\n--- 節點: {name} ---\n{data}\n"
                        total_len += len(data)
                    return True
                except Exception as e:
                    print(f"  [!] 讀取節點 {name} 失敗: {e}")
        return False

    for name in core_nodes:
        if not _read_file(name, is_core=True):
            print(f"  [!] 找不到核心節點: {name}")
            
    for name in related_nodes:
        if not _read_file(name, is_core=False):
            print(f"  [!] 找不到關聯節點: {name}")
            
    return context

async def call_gemini_stream(prompt, model, temperature=None):
    """核心：全面升級為原生 Google Generative AI SDK 直連模式，完美流式輸出且無任何緩衝與解析問題"""
    import google.generativeai as genai
    import os

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        # 嘗試從 Windows 登錄檔讀取以防 IDE 背景環境變數未載入
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
            api_key, _ = winreg.QueryValueEx(key, "GOOGLE_API_KEY")
        except:
            pass

    if not api_key:
        print("    [!] 嚴重錯誤：找不到 GOOGLE_API_KEY 環境變數或登錄檔設定！")
        yield "Error: GOOGLE_API_KEY not found."
        return

    genai.configure(api_key=api_key)

    # 模型對照
    if model == "flash-lite":
        gemini_model = "gemini-2.5-flash-lite"
    elif model == "pro":
        gemini_model = "gemini-3.1-pro"
    elif model.startswith("gemini-"):
        gemini_model = model
    else:
        gemini_model = f"gemini-{model}-latest"

    try:
        model_instance = genai.GenerativeModel(gemini_model)
        gen_config = {}
        if temperature is not None:
            gen_config["temperature"] = temperature
        response = await model_instance.generate_content_async(prompt, stream=True, generation_config=gen_config)
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        print(f"    [!] call_gemini_stream 發生異常: {e}")
        import traceback
        traceback.print_exc()


async def nlm_query_async(query, notebook_name="AI佛學總論"):
    """當本地 Wiki 找不到時，調用 NotebookLM 作為 Vector RAG Fallback (報報 6.2 實作)"""
    print(f"    [!] 觸發 Fallback：正在向 NotebookLM [{notebook_name}] 進行語義檢索...")
    try:
        # 決定 Notebook ID (新版 nlm 需使用 ID)
        notebook_mapping = {
            "AI佛學總論": "387b899a-2095-4f68-945f-e2fa35c5670b",
            "AI善導大師-淨土宗": "f0535e46-586a-44e2-bffd-59b12b21e77a",
            "AI龍樹-中觀": "359f6065-dbec-4e5e-b85d-8377c7eea534",
            "AI惠能-禪宗": "396d76a0-c781-48fe-8a73-534b1d25fc37",
            "數位佛堂_3.0": "32e46b09-02f5-42d5-91c7-ca8147ffdcaa",
            "AI彌勒-唯識宗": "b2a15532-edba-4f18-9565-96ab1ab045d9",
            "AI智者大師-天台宗": "9b4b3b81-7bd6-492b-9e71-63a1c63a60c4",
        }
        notebook_id = notebook_mapping.get(notebook_name, notebook_name)
        
        # 調用 nlm query notebook 指令 (符合最新 CLI 語法)
        process = await asyncio.create_subprocess_exec(
            'nlm', 'query', 'notebook', notebook_id, query,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
            shell=False
        )
        stdout = (await process.communicate())[0]
        
        if process.returncode == 0:
            result = stdout.decode('utf-8', errors='ignore')
            # 清理輸出內容中的 ANSI 碼與雜訊
            clean_result = CLEAN_REGEX.sub('', result).strip()
            
            # JSON 智能解析 (排除 CLI 封裝雜訊，直接還原純淨義理 Markdown)
            try:
                json_match = re.search(r'\{.*\}', clean_result, re.DOTALL)
                if json_match:
                    parsed_data = json.loads(json_match.group(0))
                    if isinstance(parsed_data, dict):
                        answer_text = ""
                        if "value" in parsed_data and isinstance(parsed_data["value"], dict) and "answer" in parsed_data["value"]:
                            answer_text = parsed_data["value"]["answer"]
                        elif "answer" in parsed_data:
                            answer_text = parsed_data["answer"]
                        
                        if answer_text:
                            clean_result = answer_text
            except Exception as json_err:
                print(f"    [!] JSON 解析 RAG 結果失敗 (非標準 JSON 回傳): {json_err}")
                
            # 物理清洗大模型思維鏈標籤 (Thought Process Tags) 避免干擾下游金剛契約推理
            clean_result = re.sub(r'<thought_process>.*?</thought_process>', '', clean_result, flags=re.DOTALL).strip()
            
            return f"\n--- NotebookLM Vector RAG 檢索結果 ---\n{clean_result}\n"
        else:
            print(f"    [!] NotebookLM 檢索失敗 (代碼: {process.returncode})")
            return ""
    except Exception as e:
        print(f"    [!] NotebookLM 執行異常: {e}")
        return ""

@app.route('/v1/chat/completions', methods=['POST'])
async def chat():
    try:
        data = await request.get_json()
        messages = data.get('messages', [])
        is_stream = data.get('stream', False)
        
        if not messages:
            return jsonify({"error": "No messages"}), 400
            
        raw_content = messages[-1]['content']
        if isinstance(raw_content, list):
            # Obsidian Copilot 有時會傳入 [{type: 'text', text: '...'}] 的格式
            user_query = " ".join([part.get('text', '') for part in raw_content if part.get('type') == 'text'])
            if not user_query:
                user_query = str(raw_content)
        else:
            user_query = str(raw_content)
        # --- 階段一：路由調度 (此階段較短，維持非串流) ---
        print(f"\n[*] 階段一：路由調度中 [Model: {ROUTER_MODEL}]")
        routing_prompt = f"""分析使用者提問，並決定調用節點。請嚴格輸出 JSON。
提問內容：{user_query}
格式：{{"tool": "graph_query", "core_nodes": ["核心節點名稱"], "related_nodes": ["關聯節點名稱"], "fallback_notebook": "AI佛學總論"}}
"""
        router_output = ""
        async for chunk in call_gemini_stream(routing_prompt, model=ROUTER_MODEL):
            router_output += chunk
            
        try:
            json_match = re.search(r'\{.*\}', router_output, re.DOTALL)
            plan = json.loads(json_match.group(0))
            nodes = plan.get('core_nodes', [])
            related = plan.get('related_nodes', [])
            notebook = plan.get('fallback_notebook') or "AI佛學總論"
            print(f"    -> 核心: {nodes} / 關聯: {related}")
        except:
            print("    [!] 路由解析失敗。")
            nodes = []
            related = []
            notebook = "AI佛學總論"

        # --- 階段二：檢索 (Graphify First) ---
        context = await get_node_content_async(nodes, related)
        
        # --- [FALLBACK] 6.2 降級機制：如果本地找不到內容，啟動 Vector RAG ---
        if not context.strip():
            context = await nlm_query_async(user_query, notebook)
            
        # --- 🚨 DROS 7.3 物理熔斷與合約感知對齊 ---
        contracts_dir = Path(os.path.join(VAULT_ROOT, "contracts"))
        requested_mode = data.get("model", "bodhisattva").lower()
        if "vajra" in requested_mode or "gold" in requested_mode:
            contract_name = "vajra_strict"
        else:
            contract_name = "bodhisattva_default"
            
        contract = InferenceContract.load(contract_name, contracts_dir=contracts_dir)
        
        has_context = bool(context and context.strip() and "未檢索到" not in context)
        runtime_mode = contract.InferenceMode if has_context else contract.FallbackMode
        model_to_use = getattr(contract, 'ComputeEngine', {}).get('Model', SYNTHESIZER_MODEL) if has_context else ROUTER_MODEL
        if not model_to_use:
            model_to_use = SYNTHESIZER_MODEL
            
        # 2. 優先使用 Obsidian 前端傳入的自訂提示詞 (custom_prompt)，達成完美的契合對齊
        prompt_template = data.get('custom_prompt')
        if not prompt_template:
            # Fallback 1：載入本地 docs 目錄下的 v5.5 提示詞模板
            prompt_template_path = Path(os.path.join(VAULT_ROOT, "docs", "System_Prompt_v5.5.md"))
            if not prompt_template_path.exists():
                # Fallback 2：如果找不到 v5.5，嘗試載入舊版範本
                prompt_template_path = Path(os.path.join(VAULT_ROOT, "docs", "System_Prompt_v5.2.md"))
                
            if prompt_template_path.exists():
                try:
                    with open(prompt_template_path, 'r', encoding='utf-8') as f:
                        prompt_template = f.read()
                except Exception as e:
                    print(f"[!] 讀取本地提示詞範本失敗: {e}")
                    prompt_template = ""
            else:
                prompt_template = ""

        if not prompt_template:
            # 極簡 Fallback 內置常量
            prompt_template = """# DROS 核心提示詞：v5.5 契約感知與雙軌智慧引擎
你是 DROS 7.2 的法義推理單元。本次行為由注入的 {{EXECUTION_CONTRACT}} 與 {{RUNTIME_MODE}} 完全決定。

## ⚙️ 雙軌執行協議
### 【Vajra 金剛模式】
- 客觀、嚴謹、學術化。依據 {{INJECTED_NODES}} 並標註真實出處。若不足則老實拒答。
### 【Bodhisattva 菩薩模式】
- 溫潤、親切、慈悲感。方便譬喻，結尾鼓勵。

---
*Dharma Reasoning OS v7.2 — 金剛治學，菩薩度眾，理事無礙。*"""

        # 準備注入內容
        injected_nodes_text = context if context.strip() else "（未檢索到相關權威節點）"

        # 語言感知處理 (DROS 7.2 強約束語系合約)
        lang = data.get('lang', 'ZH')
        target_language = "Traditional Chinese (繁體中文)" if lang == "ZH" else "Academic English (學術英文)"

        # 字串替換
        contract_envelope_text = plan.get("contract_envelope") if "plan" in locals() and plan else ""
        if not contract_envelope_text:
            contract_envelope_text = contract.to_prompt_envelope()

        final_prompt = prompt_template.replace("{{EXECUTION_CONTRACT}}", str(contract_envelope_text))
        final_prompt = final_prompt.replace("{{INJECTED_NODES}}", injected_nodes_text)
        final_prompt = final_prompt.replace("{{RUNTIME_MODE}}", runtime_mode)
        final_prompt = final_prompt.replace("{{TARGET_LANGUAGE}}", target_language)

        # 使用者問題放在最下方
        final_prompt += f"\n\n【使用者問題】：{user_query}"

        # 根據運作模式動態綁定生成溫度 (Temperature) 進行契約感知控制
        # 金剛模式 (Vajra) 要求極致嚴謹的無偏航演繹，設定極低溫度 0.05
        # 菩薩模式 (Bodhisattva) 要求語言自然、溫潤且富含譬喻力，設定適中溫度 0.5
        temp_to_use = 0.05 if runtime_mode == "Vajra" else 0.5

        print(f"[*] 已調度 DROS 智慧流露 | Mode: {runtime_mode} | Temp: {temp_to_use}")

        if is_stream:
            async def generate():
                try:
                    async for chunk in call_gemini_stream(final_prompt, model=model_to_use, temperature=temp_to_use):
                        # 模擬 OpenAI SSE 格式
                        payload = {
                            "choices": [{"delta": {"content": chunk}, "index": 0, "finish_reason": None}]
                        }
                        yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
                    yield "data: [DONE]\n\n"
                except Exception as ex:
                    print(f"    [!] generate() 內層發生異常: {ex}")
                    import traceback
                    traceback.print_exc()
            
            return Response(generate(), mimetype='text/event-stream')
        else:
            full_answer = ""
            async for chunk in call_gemini_stream(final_prompt, model=model_to_use, temperature=temp_to_use):
                full_answer += chunk
            
            return jsonify({
                "choices": [{"message": {"role": "assistant", "content": full_answer}, "finish_reason": "stop"}]
            })

    except Exception as e:
        print(f"[!] 系統錯誤: {e}")
        return jsonify({"error": {"message": str(e)}}), 500

if __name__ == '__main__':
    print("--- [Digital Dharma Gateway v5.1] Async SSE + Vector RAG Fallback Active ---")
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
