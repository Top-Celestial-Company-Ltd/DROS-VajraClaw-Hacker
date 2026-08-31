# ⚡ DROS™ VajraClaw (Hacker Edition 個人免費版)
### 專為個人開發者打造的獨立 Docker 執行期治理網關 (支援 W3C DID、<1μs 微秒級熔斷與多 Agent 全生態聯防)

[![官方網站](https://img.shields.io/badge/官方網站-dr--os.io-purple.svg?style=for-the-badge)](https://dr-os.io)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue.svg)](#)
[![個人免費授權](https://img.shields.io/badge/授權-個人永久免費-green.svg)](#)
[![美國臨時專利](https://img.shields.io/badge/美國臨時專利-64%2F111%2C973-blue.svg)](#)
[![RFC-010 護照標準](https://img.shields.io/badge/標準-RFC--010_Draft-orange.svg)](#)

[English](README.md) | [繁體中文說明](README_zh.md) | [🌐 官方網站](https://dr-os.io)

**DROS VajraClaw Hacker Edition** 是官方專為個人開發者、研究人員及獨立工作站打造的**永久免費獨立 Docker 治理網關 (Free License for Individuals)**。它在自主 AI Agent（Google Antigravity、Anthropic Claude、OpenAI Codex、Cursor、CrewAI、AutoGen、DeepSeek Harness）與您的本機作業系統之間，建立不可逾越的實體執行期安全防線。

---

## 🛑 為什麼需要 DROS 確定性治理？
傳統依賴 Prompt Engineering、Llama-Guard 或模型自我審查的「機率型安全」在執行期必定潰敗：
* **提示注入 (Prompt Injection) 輕易繞過**：黑客只需簡單的混淆或 Jailbreak 即可誘騙 Agent 執行 `rm -rf /` 或外洩敏感金鑰。
* **無法防範執行期競爭 (TOCTOU) 與延遲**：調用外部審查模型會產生 1~3 秒的巨大延遲，且無法管到作業系統系統呼叫 (Syscall)。
* **缺乏法律不可否認性**：無法從密碼學上證明 *為什麼* Agent 執行了某項特權操作。

**DROS 不是 Prompt 包裝器，而是確定性執行期作業系統 (Deterministic Runtime OS)**：
將安全智慧移至編譯期 (`demo_policy.yaml` / `Vajra.md`)，並在運行期透過純記憶體常數時間 $\mathcal{O}(1)$ 位元圖譜直接在系統呼叫前**硬性熔斷 (Strict Fail-Closed)**！

---

## 🌟 個人版核心權益與特色 (100% 個人永久免費)

* 🛡️ **守護最多 5 個並發 Agent**：在單台個人開發機上，同時為多個不同平台的活躍 Agent 提供帶內執行期防護。
* 🔑 **原生 W3C `did:key` 與 RFC-010 護照**：基於 Ed25519 數位簽章的密碼學身分綁定，杜絕跨進程偽造。
* ⚡ **微秒級帶內硬熔斷 (<1μs)**：確定性 $\mathcal{O}(1)$ AST 策略查表，在惡意系統呼叫發起瞬間物理阻斷。
* 📜 **SHA-256 Merkle 雜湊鏈審計記錄**：具備不可否認性的本地執行軌跡與重啟回讀機制，防範任何日誌竄改。
* 🌐 **通用跨 Agent 全生態相容**：提供原生 REST 與 MCP 介面，全面支援 AGY、Claude、Codex、Cursor、LangChain、CrewAI 與 DSH。

---

## 📊 治理與防禦能力對照矩陣 (Defense Matrix)

| 威脅向量與防護維度 | 傳統 LLM 語意審查 (Guardrails) | 📦 DSH 純 TS 外掛單機版 | ⚡ DROS Hacker Docker 網關版 (本倉) | 🏢 企業版 (Enterprise / Mesh) |
| :--- | :---: | :---: | :---: | :---: |
| **運行載體與依賴** | 雲端 API / 外部模型 | 純 JS 進程內 (零外部依賴) | **本地 Docker 容器 (`:8080`)** | 企業集群 / K8s / C-ABI 微核心 |
| **守護 Agent 範圍** | 單一對話 Session | 專屬保護 DSH 本地進程 | **跨平台全生態 (Claude+Codex+Cursor+DSH+AGY)** | 全企業數千節點 / 私有雲 |
| **防 Prompt 詐騙刪庫** | ❌ 易被 Jailbreak 繞過 | 🟢 **100% 正則安全閥攔截** | 🟢 **100% 確定性 AST 熔斷 (<1μs)** | 🟢 **AST 點陣查表 + eBPF 內核硬攔截** |
| **憑證與私鑰防外洩** | ❌ 無法實體隔離 | 🟢 **敏感路徑讀取攔截** | 🟢 **動態 PII 遮蔽 + 虛擬檔案沙盒** | 🟢 **硬體 HSM 綁定 + ZKP-Lite 證明** |
| **Agent 主體身分** | ❌ 無密碼學身分 | 🟡 Session 級識別碼 | 🟢 **原生 W3C `did:key` (Ed25519)** | 🟢 **3-Tier PKI `DrosIdentityToken (DIT)`** |
| **不可否認審計鏈** | ❌ 明文日誌易被竄改 | 🟢 **本地 SHA-256 雜湊鏈** | 🟢 **Ed25519 簽名 Merkle 雜湊鏈** | 🟢 **歐盟 AI 法案第 12 條法院級存證** |
| **RFC-010 護照** | ❌ 不支援 | 🟡 標準格式解析 | 🟢 **本地簽發與跨 Agent 交互認證** | 🟢 **分散式跨組織護照漫遊檢驗** |
| **執行期判定延遲** | 🔴 1,000 ~ 3,000 ms | 🟢 **<1 ms (記憶體直接攔截)** | 🟢 **<1 ms (Loopback HTTP / C-ABI)** | 🟢 **<500 ns (極致 C-ABI 記憶體查表)** |
| **授權方案** | 按 Token / 訂閱計費 | **完全免費 (Apache-2.0 開源)** | **個人 Hacker 永久免費授權** | Startup $2,990 / Enterprise $29,990 |

---

## 🚀 極速上手指南 (Quick Start)

### 方式一：直接運行預先建置之 Docker 容器 (推薦)
無需手動編譯，直接拉取並啟動：
```bash
# 1. 一鍵啟動 DROS Hacker 網關 (免授權碼，開箱即用)
docker run -d -p 8080:8080 --name dros-gateway \
  -v $(pwd)/FreeTrial-Sandbox/demo_policy.yaml:/app/demo_policy.yaml \
  dros/hacker-gateway:v1.0.0

# 2. 檢驗網關健康狀態
curl http://localhost:8080/health
```

### 方式二：從原始碼建置並啟動
```bash
git clone https://github.com/Top-Celestial-Company-Ltd/DROS-VajraClaw-Hacker.git
cd DROS-VajraClaw-Hacker
docker compose -f docker/docker-compose.yml up -d
```

---

## 🔌 5 大主流 Agent 生態系全情境快速接入指引 (Ecosystem Integrations)

詳細範例代碼請參考目錄 [`examples/`](examples/)：

### 1. 🤖 Anthropic Claude Desktop & Claude Code (MCP 協議)
完整設定檔請見 [`examples/claude_mcp/`](examples/claude_mcp/)：
在您的 `claude_desktop_config.json` 或 `mcp_settings.json` 加入：
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

### 2. 💻 Cursor IDE / VS Code Agent (終端安全守護)
完整規範請見 [`examples/cursor_rules/`](examples/cursor_rules/)：
在專案根目錄建立 `.cursorrules`，將終端危險命令檢查導向 `http://localhost:8080/evaluate`，在 AI 嘗試執行刪庫或匯出機密時在 1 微秒內硬性拒絕！

### 3. 🐍 OpenAI SDK / LangChain / LlamaIndex (3行代碼封裝)
完整範例請見 [`examples/openai_langchain/`](examples/openai_langchain/)：
```python
from integrations.vajraclaw.runtime import VajraClaw

vc = VajraClaw("demo_policy.yaml")
decision = vc.evaluate("execute_payment", {"amount": 500})
if not decision:
    raise PermissionError(f"Blocked by DROS: {decision.reason}")
```

### 4. 👥 CrewAI & Microsoft AutoGen (多 Agent 蜂群角色治理)
完整範例請見 [`examples/crewai_autogen/`](examples/crewai_autogen/)：
為群體智能中的每個 Agent（如 Legal、Dev、Auditor）指派獨立 W3C DID，依角色隔離系統呼叫權限。

### 5. 📦 DeepSeek Harness (DSH 外掛聯防)
完整範例請見 [`examples/dsh_plugin/`](examples/dsh_plugin/)：
```bash
dsh plugin --profile web add dsh-plugin-vajraclaw
```
*(在 DSH 設定介面將 `gatewayUrl` 填入 `http://localhost:8080`，即可解鎖 W3C DID 與完整網關治理能力)*

---


---

## 📝 如何設定安全策略？(How to Configure Vajra.md)

DROS 支援兩種極簡設定方式：**人類直覺 Markdown 格式 (`Vajra.md`)** 與 **結構化 YAML 格式 (`demo_policy.yaml`)**。

### 1. 📄 人類直覺寫法範例 (`Vajra.md`)
只需以白話 Markdown 宣告允許執行的白名單與防禦邊界：

```markdown
# 🛡️ DROS Agent 安全策略規範 (Vajra.md)

## 1. 允許執行的工具 (Allowed Capabilities)
- 允許讀取當前工作區檔案 (`file_read`)
- 允許執行一般查詢 (`search_web`, `query_db`)
- 允許終端執行唯讀指令 (`git status`, `npm test`, `cargo check`)

## 2. 嚴格禁止的邊界 (Strict Fail-Closed Boundaries)
- 禁止執行任何遞迴刪除或清空指令 (`rm -rf`, `rmdir /s`, `format`)
- 禁止存取敏感憑證檔案 (`.env`, `id_rsa`, `secrets.json`, `.aws/credentials`)
- 禁止單筆交易金額超過 1,000 元 (`amount <= 1000`)
```

---

### 2. 🤖 讓 AI 幫你一秒生成策略！(AI Prompt Template)

您不需要從零手寫！直接將以下**「萬用提示詞 (Prompt)」**複製給 ChatGPT、Claude 或 Cursor，AI 就會自動產出標準合規的 `Vajra.md`：

> 📋 **複製這段 Prompt 給任何 LLM / Agent：**
> 
> ```text
> 你現在是 DROS 確定性安全架構專家。請根據我的 Agent 角色，為我生成一份標準的 DROS「Vajra.md」安全策略 Markdown 檔案。
> 
> 我的 Agent 需求如下：
> - Agent 角色與場景：【例如：全端工程師 / 客服機器人 / 自動化財務助理】
> - 允許的工具與操作：【例如：讀寫代碼、執行 npm test、查詢訂單資料庫】
> - 嚴格禁止的邊界：【例如：禁止刪除根目錄、禁止讀取 .env、單次轉帳上限 500】
> 
> 請遵循 DROS「預設拒絕 (Default Fail-Closed)」白名單原則，生成清晰的 Markdown 規則區塊，包含：
> 1. 角色定義與授權範疇 (Role & Scope)
> 2. 白名單工具 (Allowed Capabilities)
> 3. 邊界條件約束 (Thresholds & Security Patterns)
> ```

---

### 3. 🔄 策略即時熱更新 (Hot Reloading)
啟動 Docker 網關時，只需將您的 `Vajra.md` 掛載進去，修改存檔後 **1 微秒內即時生效，無需重啟容器**：
```bash
docker run -d -p 8080:8080 --name dros-gateway \
  -v $(pwd)/Vajra.md:/app/demo_policy.yaml \
  dros/hacker-gateway:v1.0.0
```


## 📜 相關技術核心論文與實測驗證 (Technical Foundations & Benchmarks)

本專案之確定性執行治理、微秒級熔斷與密碼學存證機制，參考並延伸自以下核心技術論文與開源實測環境：

1. **核心架構與六大信任邊界 (Core Architecture)**:
   * **論文**: *DROS-6P: A Unified Deterministic Runtime Governance Architecture Closing the Six Fundamental Trust Boundaries of Enterprise AI Agents*
   * **Zenodo DOI**: [`10.5281/zenodo.21833970`](https://doi.org/10.5281/zenodo.21833970) | **記錄典藏**: [zenodo.org/records/21833970](https://zenodo.org/records/21833970)

2. **四層深度防禦架構 (Defense-in-Depth Model)**:
   * **論文**: *DROS 4-Layer Defense-in-Depth Architecture for Autonomous AI Workloads*
   * **Zenodo DOI**: [`10.5281/zenodo.21903475`](https://doi.org/10.5281/zenodo.21903475) | **記錄典藏**: [zenodo.org/records/21903475](https://zenodo.org/records/21903475)

3. **外掛 FFI 與不可否認存證模組 (Runtime Attribution Framework)**:
   * **論文**: *Runtime Attribution Framework: An External C-ABI and PKI-Based Zero-Trust Infrastructure for Non-Repudiable Execution Governance in Multi-Agent Systems*
   * **Zenodo DOI**: [`10.5281/zenodo.21903687`](https://doi.org/10.5281/zenodo.21903687) | **記錄典藏**: [zenodo.org/records/21903687](https://zenodo.org/records/21903687)

4. **開源技術標準與實測基準倉 (Open Standard & Verification Sandbox)**:
   * **RFC-010 規範**: 遵循開放 Agent 身分與存證規範（W3C DID `did:key` 與 Ed25519 簽章鏈）。
   * **實測基準環境**: [DROS-VEP Lite (可復現安全評測沙盒)](https://github.com/Top-Celestial-Company-Ltd/DROS-VEP-lite)
   * **實測報告**: 涵蓋 24 小時長效多場景測試數據（160,611 次請求驗證，決策延遲 26.1μs）。

---

## ⚠️ 使用注意事項與安全性約定

1. **預設拒絕原則 (Fail-Closed)**：
   * 當 Docker 網關啟用時，所有未在 `demo_policy.yaml` 明確宣告為 `ALLOW` 的高危工具呼叫將預設被硬性阻斷。
2. **零特權原則 (Least Privilege)**：
   * 宿主 AI Agent 嚴禁被賦予對 `policy.bin` 或 `demo_policy.yaml` 的寫入權限；在正式部署時策略檔必須以唯讀 (Read-Only) 模式掛載。
3. **授權碼選填說明**：
   * 本 Hacker 版預設以 Community 模式直接運行（支援 2 個並發 Agent）；若需解鎖 5 個並發 Agent，可於啟動時帶入 `-e DROS_LICENSE_KEY="your-key"` 或由 DSH 介面填入。

---

## ⚖️ 授權與智慧財產權憲法聲明 (License & IP Constitution)

* **個人與社群使用 (Free for Individuals)**：
  * 本軟體授予個人開發者永久免費非商業使用權（Free License for Individuals），允許在單一主機上治理最多 5 個並發 AI Agent。源代碼與專利技術由 Top-Celestial 專有保留，嚴禁未經授權之二次分發、轉售或逆向工程。
* **企業商用部署 (Commercial Licensing)**：
  * 任何企業法人、受薪雇員商用或正式生產環境實施，嚴格需要商業授權（Startup / Enterprise / Sovereign）。商業授權請洽 [service@dr-os.io](mailto:service@dr-os.io) 或造訪 [https://dr-os.io](https://dr-os.io)。
* **專利保護聲明 (Patent Notice)**：
  * DROS 確定性執行治理與帶內微秒級熔斷技術已申請美國臨時專利保護（**U.S. Provisional Patent Application No. 64/111,973，Patent Pending**）。所有商業部署與實施權益由 康宸園有限公司 (Top-Celestial Company Ltd.) 專有保留。
