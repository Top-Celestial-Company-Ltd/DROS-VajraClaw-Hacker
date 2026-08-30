# ⚡ DROS™ VajraClaw (Hacker Edition 個人免費版)
### 專為個人開發者打造的獨立 Docker 執行期治理網關 (支援 W3C DID、<1μs 微秒級熔斷與多 Agent 聯防)

[![官方網站](https://img.shields.io/badge/官方網站-dr--os.io-purple.svg?style=for-the-badge)](https://dr-os.io)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue.svg)](#)
[![個人免費授權](https://img.shields.io/badge/授權-個人永久免費-green.svg)](#)
[![美國臨時專利](https://img.shields.io/badge/美國臨時專利-64%2F111%2C973-blue.svg)](#)
[![RFC-010 護照標準](https://img.shields.io/badge/標準-RFC--010_Draft-orange.svg)](#)

[English](README.md) | [繁體中文說明](README_zh.md) | [🌐 官方網站](https://dr-os.io)

**DROS VajraClaw Hacker Edition** 是官方專為個人開發者、研究人員及獨立工作站打造的**永久免費獨立 Docker 治理網關 (Free License for Individuals)**。它在自主 AI Agent（Google Antigravity、OpenAI Codex、Claude Code、Cursor、DeepSeek Harness）與您的本地作業系統之間，建立不可逾越的實體執行期安全防線。

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
* 🌐 **通用跨 Agent 相容性**：提供原生 REST 與 MCP 介面，全面支援 AGY、Codex、Claude Code、Cursor 與 DSH。

---

## 📊 治理與防禦能力對照矩陣 (Defense Matrix)

| 威脅向量與防護維度 | 傳統 LLM 語意審查 (Guardrails) | 📦 DSH 純 TS 外掛單機版 | ⚡ DROS Hacker Docker 網關版 (本倉) | 🏢 企業版 (Enterprise / Mesh) |
| :--- | :---: | :---: | :---: | :---: |
| **運行載體與依賴** | 雲端 API / 外部模型 | 純 JS 進程內 (零外部依賴) | **本地 Docker 容器 (`:8080`)** | 企業集群 / K8s / C-ABI 微核心 |
| **守護 Agent 範圍** | 單一對話 Session | 專屬保護 DSH 本地進程 | **跨平台聯防 (AGY+Codex+Claude+Cursor+DSH)** | 全企業數千節點 / 私有雲 |
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

## 🔌 跨平台多 Agent 快速接入指引

### 1. Google Antigravity 2.0 / Claude Desktop / Cursor (MCP 模式)
在您的 `mcp_settings.json` 或 Claude 擴充配置中加入 DROS 網關：
```json
{
  "mcpServers": {
    "dros-governance": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### 2. DeepSeek Harness (DSH)
在 DSH 中安裝官方安全外掛，並指向 Docker 網關：
```bash
dsh plugin --profile web add dsh-plugin-vajraclaw
```
*(在 DSH 設定介面將 `gatewayUrl` 填入 `http://localhost:8080`，即可解鎖 W3C DID 與完整網關治理能力)*

### 3. OpenAI Codex / Claude Code / Python SDK
在您的開發環境中設定環境變數：
```bash
export DROS_GATEWAY_URL="http://localhost:8080"
export DROS_IDENTITY_SEED="0x1a2b3c4d5e6f..." # 您的本機 Ed25519 種子
```

在 Python 代碼中直接調用：
```python
from integrations.vajraclaw.runtime import VajraClaw

vc = VajraClaw("demo_policy.yaml")
decision = vc.evaluate("execute_payment", {"amount": 500})
if not decision:
    raise PermissionError(f"Blocked by DROS: {decision.reason}")
```

---

## 📜 學術三部曲論文與權威引用 (Technical Foundations & Academic Citations)

若您在學術論文、產業報告或開源研究中引用 DROS 執行期確定性治理架構，請引用我們已公開於 Zenodo 的權威論文三部曲：

* 📖 **[DROS 學術三部曲導讀 (Reading Guide Technical Note)](https://doi.org/10.5281/zenodo.22114036)**: *An Agent Runtime Operation Substrate: Technical Foundations, Reading Guide, and Roadmap for the DROS Paper Trilogy*（Zenodo: [`10.5281/zenodo.22114036`](https://doi.org/10.5281/zenodo.22114036)）
* 🏛️ **Paper 1: DROS-6P** — *A Unified Deterministic Runtime Governance Architecture Closing the Six Fundamental Trust Boundaries of Enterprise AI Agents*（DOI: [`10.5281/zenodo.21833970`](https://doi.org/10.5281/zenodo.21833970)）
* 🏛️ **Paper 2: DROS 4-Layer (v3)** — *Bridging the Agent-to-Execution Attribution Gap in Autonomous AI Workloads: A 4-Layer Deterministic Runtime Operating System*（DOI: [`10.5281/zenodo.22092008`](https://doi.org/10.5281/zenodo.22092008)）
* 🏛️ **Paper 3: DROS-PGM** — *A Deterministic Kernel-Level Execution Control Plane for Post-Compromise Security in Autonomous AI Systems*（DOI: [`10.5281/zenodo.21903687`](https://doi.org/10.5281/zenodo.21903687)）

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
