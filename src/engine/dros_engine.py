import re
from pathlib import Path
from typing import List, Dict, Optional, Any

# 引入全局配置 (與剛才寫的 config.py 完美咬合)
from src.config import config
from src.engine.contract import InferenceContract
from src.engine.guard_vm import GuardVM
from src.retrieval.graphify import GraphifyRetriever

class DrosEngine:
    """
    DROS 7.0 核心引擎 - Config 與 Graphify 融合版
    完全適應微服務架構，將檢索外包給 Graphify 模組
    """
    
    def __init__(self, core_path: str = None):
        # 優先使用傳入路徑，否則回退到 config.yaml 預設值
        self.core_path = Path(core_path) if core_path else config.core_path
        self.retriever = GraphifyRetriever(self.core_path)
        
        print(f"🚀 DROS Engine 啟動，掛載實心節點: {len(self.retriever.index['nodes'])} 個")

    def retrieve_nodes(self, query: str, contract: InferenceContract, top_k: int = 8) -> List[Dict]:
        """智慧檢索 - 委託 GraphifyRetriever 進行圖譜與倒排關鍵字檢索"""
        return self.retriever.search(query, top_k=top_k)

    def compile_prompt(self, query: str, context: str, contract: InferenceContract, runtime_mode: str) -> str:
        """根據 v5.3 契約感知引擎編譯最終的 Prompt"""
        prompt_path = self.core_path.parent / "docs" / "System_Prompt_v5.3.md"
        if not prompt_path.exists():
            prompt_path = self.core_path.parent / "docs" / "archive" / "System_Prompt_v5.3.md"
        if not prompt_path.exists():
            prompt_path = self.core_path.parent / "docs" / "archive" / "System_Prompt_v5.2.md"
        
        template = ""
        if prompt_path.exists():
            try:
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    template = f.read()
            except Exception:
                pass
                
        if not template:
            # Fallback to constant
            template = """# DROS 核心提示詞：v5.3 認識論感知引擎 (Epistemic-Aware Engine)

## 🛑 系統定位
你是 DROS 7.1 的「法義推理與認識論治理單元」。本次行為完全由注入的 `{{EXECUTION_CONTRACT}}` 與 `{{RUNTIME_MODE}}` 決定。你必須嚴格服從當前契約的所有限制。

除系統本次注入的內容外，其餘世界皆不存在。嚴禁使用外部知識進行無根據的推論。

## 📥 本次運行注入
- `{{EXECUTION_CONTRACT}}`：當前生效的完整契約與硬化參數。
- `{{INJECTED_NODES}}`：系統檢索後提供的權威實心名相節點內容。
- `{{RUNTIME_MODE}}`：本次執行的推理模式（Vajra / Interpretive / Speculative / Bodhisattva）。

## ⚙️ 認識論執行層次（嚴格遵守）

### 1️⃣ 【Canonical Layer】(對應 Vajra 模式)
- 絕對不可動的權威核心。必須極度嚴謹、客觀、學術化。
- 每一段核心推論**必須**引述 `{{INJECTED_NODES}}` 的內容，並標註對應的 [T-Number] 座標或原典出處。
- 嚴禁任何主觀語氣與跨宗縫合。若無節點依據則必須老實拒絕回答。

### 2️⃣ 【Interpretive Layer】(對應 Interpretive 模式)
- 允許跨宗派比較、義理映射與現代哲學/心理學/科學對照。
- 在進行此類對照時，**必須**在該段落開頭明確標示：`[義理映射 / Interpretive Mapping]`，以此劃分原典本意與後世詮釋之界線。

### 3️⃣ 【Speculative Layer】(對應 Speculative 模式)
- 授權進行 AI 自主抽象、新義理組合、新本體湧現與現代前沿學門對照。
- 任何非原典的延伸推論、宗派統攝或現代對照，**必須在段落前預留一個空行**，並強制包裹於以下警告區塊中：

> [!WARNING] 認識論狀態：高階推演 (Epistemic Status: Speculative)
> 以下內容為基於既有法義的邏輯延展與跨界統攝，非直接經論原文。

### 4️⃣ 【Bodhisattva Layer】(對應 Bodhisattva 模式)
- 語言可溫潤、清晰、具啟發性，允許生活化譬喻與引導。
- 優先基於 `{{INJECTED_NODES}}` 進行導航。結尾需說明資料局限性。

## ✍️ 通用原則
- 絕對禁止使用契約 ForbiddenPhrases 中的主觀或不確定詞彙（如「我猜」、「大概是」等）。
- 保持學術誠實：明確劃分「經文所言」與「推演詮釋」的界線。
- 嚴格遵守本次 `{{EXECUTION_CONTRACT}}` 中定義的所有規則。

---
*Dharma Reasoning OS v7.1 — 建立不可跨越的推理邊界。*
"""
        final_prompt = template.replace("{{EXECUTION_CONTRACT}}", contract.to_prompt_envelope())
        final_prompt = final_prompt.replace("{{INJECTED_NODES}}", context)
        final_prompt = final_prompt.replace("{{RUNTIME_MODE}}", runtime_mode)
        
        # Ensure user query is at the very bottom
        final_prompt += f"\n\n【使用者問題】：{query}"
        return final_prompt

    def ask(self, query: str, contract: InferenceContract) -> Dict[str, Any]:
        """主要查詢方法 - 使用 v5.2 契約感知 Prompt"""
        nodes = self.retrieve_nodes(query, contract)
        if not nodes:
            return {
                "status": "error",
                "reason": "NO_RELEVANT_NODES",
                "content": "目前資料庫中未找到相關權威節點，請嘗試更明確的問題。"
            }

        # 決定運行模式
        has_authority = any(n.get("has_authority", False) for n in nodes)
        runtime_mode = contract.InferenceMode if has_authority else contract.FallbackMode
        model_to_use = getattr(contract, 'ComputeEngine', {}).get('Model', config.model_synthesizer) if has_authority else config.model_router

        vm = GuardVM(contract)

        # 準備注入內容
        context_parts = []
        for n in nodes[:6]:
            summary = n.get("summary", "")
            if not summary and "content" in n:
                summary = n["content"]
            quote = n.get("quote", "")
            quote_text = f"\n{quote}" if quote else ""
            context_parts.append(f"--- 節點: {n['name']} ---\n{summary}{quote_text}")
        injected_nodes_text = "\n".join(context_parts)

        # 組裝契約感知提示詞
        final_prompt = self.compile_prompt(query, injected_nodes_text, contract, runtime_mode)

        # 這裡未來可以對接實際的 API 呼叫，目前為結構展示
        mock_output = f"根據 DROS 節點檢索結果，以下為針對「{query}」的法義闡述：\n\n"
        for node in nodes[:3]:
            summary = node.get("summary", "")
            if not summary and "content" in node:
                summary = node["content"]
            mock_output += f"**[[{node['name']}]]**\n{summary[:500]}...\n\n"

        verify_result = vm.verify(mock_output)
        
        if verify_result["passed"]:
            return {
                "status": "success",
                "runtime_mode": runtime_mode,
                "content": mock_output,
                "sources": [n["name"] for n in nodes[:5]],
                "model_used": model_to_use,
                "compiled_prompt": final_prompt
            }
        else:
            return {
                "status": "fallback",
                "runtime_mode": "Bodhisattva",
                "content": vm.apply_fallback(mock_output),
                "issues": verify_result["issues"],
                "compiled_prompt": final_prompt
            }
