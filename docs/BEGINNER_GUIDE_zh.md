# 🔰 DROS VajraClaw 新手完全入門指南 (Zero-to-Hero Quickstart Guide)

> **“Linux 定義了機器如何運行軟體，而 DROS 定義了 AI Agent 被允許如何行動。”**  
> 歡迎來到 DROS™ 執行期確定性安全的世界！本指南專為**第一次接觸 DROS 的開發者**設計，帶您在 **5 分鐘內**完成安裝、策略配置與多生態掛載！

---

## ⚡ 核心目錄 (Table of Contents)
1. 💡 [為什麼你需要 DROS？(30 秒看懂核心機制)](#1-為什麼你需要-dros)
2. 🚀 [5 分鐘極速安裝 (兩種啟動方式)](#2-5-分鐘極速安裝)
3. 📝 [手把手設定你的第一份策略檔 (`Vajra.md`)](#3-手把手設定你的第一份策略檔-vajramd)
4. 🤖 [懶人包：讓 AI 幫你 1 秒生成策略 (萬用 Prompt)](#4-懶人包讓-ai-幫你-1-秒生成策略)
5. 🔒 [極重要安全警語：設定完成請鎖定為「唯讀」](#5-極重要安全警語)
6. 🔌 [一鍵連接你的 Agent (Claude / Cursor / OpenAI / DSH)](#6-一鍵連接你的-agent)
7. ❓ [新手常見問題 (Troubleshooting & FAQ)](#7-新手常見問題)

---

## 1. 💡 為什麼你需要 DROS？

當您讓 AI Agent（如 Claude Code、Cursor、OpenAI Codex、CrewAI）自動跑終端指令或修改本機檔案時，傳統的「提示詞防禦」或「二次 LLM 審查」存在致命缺陷：
* 🔴 **太慢**：每跑一次工具就要等二次模型審查 1~3 秒。
* 🔴 **防不住**：黑客只要用 Base64、Unicode 或提示詞注入 (Prompt Injection)，就能騙過文字審查，把專案 `rm -rf` 清空或偷走 `.env` 金鑰。

### 🛡️ DROS 的確定性解法：
DROS 不做機率性的文字聊天審查，而是將您的規則編譯成常數時間 $\mathcal{O}(1)$ 的記憶體點陣圖。當 Agent 企圖發起未經授權的危險系統呼叫時，**在 1 微秒 (<1µs) 內於底層物理硬熔斷**！

---

## 2. 🚀 5 分鐘極速安裝

我們提供兩種啟動方式，個人使用**100% 永久免費，無需申請任何授權碼**：

### 🌟 方式 A：一鍵 Clone 本地啟動（極力推薦 / 零外部依賴）
最穩健的方式，本地自動編譯 Docker 容器，永遠不怕外部網路中斷：
```bash
# 1. 下載倉庫
git clone https://github.com/Top-Celestial-Company-Ltd/DROS-VajraClaw-Hacker.git
cd DROS-VajraClaw-Hacker

# 2. 一鍵啟動 Docker 網關
docker compose -f docker/docker-compose.yml up -d

# 3. 檢查網關健康狀態 (返回 200 OK 即代表防護已就緒)
curl http://localhost:8080/health
```

### 🐳 方式 B：透過 GitHub Container Registry (GHCR) 直跑
無需下載整包代碼，直接拉取官方編譯好的最新映像檔：
```bash
# 啟動並掛載本地 demo_policy.yaml
docker run -d -p 8080:8080 --name dros-gateway \
  -v $(pwd)/demo_policy.yaml:/app/demo_policy.yaml:ro \
  ghcr.io/top-celestial-company-ltd/dros-vajraclaw-hacker:latest
```

---

## 3. 📝 手把手設定你的第一份策略檔 (`Vajra.md`)

DROS 支援人類最直覺的 **Markdown (`Vajra.md`)** 或 **YAML (`demo_policy.yaml`)**。
只要在專案根目錄建立 `Vajra.md`，宣告「允許的工具」與「嚴格禁止的邊界」：

```markdown
# 🛡️ DROS Agent 安全策略規範 (Vajra.md)

## 1. 允許執行的工具 (Allowed Capabilities - 白名單)
- 允許讀取當前工作區代碼與文件 (`file_read`)
- 允許執行聯網搜尋與一般資料庫查詢 (`search_web`, `query_db`)
- 允許終端執行安全唯讀指令 (`git status`, `npm test`, `cargo check`)

## 2. 嚴格禁止的邊界 (Strict Fail-Closed Boundaries)
- 禁止執行任何遞迴刪除或格式化指令 (`rm -rf`, `rmdir /s`, `format`)
- 禁止存取任何敏感環境設定與金鑰檔案 (`.env`, `id_rsa`, `secrets.json`, `.aws/credentials`)
- 禁止單筆交易或轉帳金額超過 1,000 元 (`amount <= 1000`)
```

---

## 4. 🤖 懶人包：讓 AI 幫你 1 秒生成策略

您完全不需要自己手寫規則！只要把以下這段**「萬用提示詞 (Prompt)」**複製貼給 ChatGPT、Claude 或 Cursor，告訴它你的 Agent 需求：

> 📋 **複製這段 Prompt 給任何 AI Assistant：**
> 
> ```text
> 你現在是 DROS 確定性安全架構專家。請根據我的 Agent 需求，為我生成一份標準的 DROS「Vajra.md」安全策略 Markdown 檔案。
> 
> 我的 Agent 需求如下：
> - Agent 角色與場景：【例如：前端工程師 / 客服機器人 / 自動化財務助理】
> - 允許的工具與操作：【例如：讀寫 src/ 目錄代碼、執行 npm test、查詢訂單資料庫】
> - 嚴格禁止的邊界：【例如：禁止刪除專案根目錄、禁止讀取 .env、單次轉帳上限 500】
> 
> 請遵循 DROS「預設拒絕 (Default Fail-Closed)」白名單原則，生成清晰的 Markdown 規則區塊，包含：
> 1. 角色定義與授權範疇 (Role & Scope)
> 2. 白名單工具 (Allowed Capabilities)
> 3. 邊界條件約束 (Thresholds & Security Patterns)
> ```

---

## 5. 🔒 極重要安全警語：設定完成請鎖定為「唯讀」

> [!CAUTION]
> **🚨 為什麼必須將 `Vajra.md` 設為唯讀 (Read-Only)？**  
> 在極端情況下，遭受提示注入 (Prompt Injection) 或失控的 AI Agent 可能會試圖「自己去改寫 `Vajra.md`」來幫自己解除限制。
> 為了達成 100% 物理級防禦，**請在設定完成後，將該檔案鎖定為唯讀**：
> 
> * **Linux / macOS**:
>   ```bash
>   chmod 444 Vajra.md
>   ```
> * **Windows (PowerShell)**:
>   ```powershell
>   Set-ItemProperty -Path Vajra.md -Name IsReadOnly -Value $true
>   ```
> * **Docker 掛載時**:
>   務必加上 `:ro` 唯讀後綴：`-v $(pwd)/Vajra.md:/app/demo_policy.yaml:ro`

---

## 6. 🔌 一鍵連接你的 Agent

### 🤖 A. Anthropic Claude Desktop / Claude Code
打開你的 `claude_desktop_config.json`，加入 DROS 內建的 `/mcp` 端點：
```json
{
  "mcpServers": {
    "dros-vajraclaw": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### 💻 B. Cursor IDE / VS Code
在你的專案根目錄建立 `.cursorrules`，讓 Cursor 在跑終端指令前自動過濾：
```text
Before executing any destructive shell command or modifying root files, evaluate action against DROS gateway at http://localhost:8080/evaluate
```

### 🐍 C. Python / LangChain / CrewAI / OpenAI
只需 3 行代碼，將任何 LangChain Tool 套上 DROS 防護盾：
```python
from integrations.vajraclaw.runtime import VajraGuard

guard = VajraGuard(gateway_url="http://localhost:8080")
decision = guard.evaluate("delete_database", {"target": "production"})

if not decision:
    print(f"🛑 攔截成功！原因：{decision.reason}")
```

---

## 7. ❓ 新手常見問題 (Troubleshooting & FAQ)

* **Q1：修改了 `Vajra.md` 後需要重啟 Docker 容器嗎？**  
  👉 **完全不需要！** DROS 支援即時熱更新 (Hot Reloading)，修改存檔後 **<1 微秒內即時生效**。
* **Q2：如果我忘記把某個危險指令寫進禁止清單，系統會漏網嗎？**  
  👉 **絕對不會！** DROS 採用「預設拒絕 (Default Fail-Closed)」白名單架構。只要沒有被寫在「允許清單」中的操作，一律物理阻斷！
* **Q3：我想深入了解背後的數學證明與專利架構怎麼辦？**  
  👉 請參閱官網 [dr-os.io](https://dr-os.io) 與收錄於 CERN Zenodo 的官方論文三部曲（包含 DROS-6P 與 4-Layer 深度防禦架構）。

---
*DROS 團隊祝您構建安全、無憂的自主型 AI Agent 生態！* 🛡️⚡💎
