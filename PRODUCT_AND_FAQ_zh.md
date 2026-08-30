# 🛡️ DROS™ 官方商品全覽、定價方案與技術核心 FAQ
### DROS (Deterministic Runtime Operating System) 企業級執行治理標準規格書

[![官方網站](https://img.shields.io/badge/官方網站-dr--os.io-purple.svg?style=for-the-badge)](https://dr-os.io)
[![美國臨時專利](https://img.shields.io/badge/美國臨時專利-64%2F111%2C973-blue.svg)](#)
[![標準協議](https://img.shields.io/badge/RFC--010-Draft-orange.svg)](#)
[![授權模式](https://img.shields.io/badge/授權-標準三大層級憲法-green.svg)](#)

[English Version (PRODUCT_AND_FAQ.md)](PRODUCT_AND_FAQ.md) | [繁體中文說明 (PRODUCT_AND_FAQ_zh.md)](PRODUCT_AND_FAQ_zh.md) | [🌐 官方網站 (dr-os.io)](https://dr-os.io)

---

## 🛑 一、 為什麼需要 DROS 確定性執行治理？
傳統依賴 Prompt Engineering、Llama-Guard 或模型自我審查的「機率型安全」在執行期必定潰敗：
1. **提示注入 (Prompt Injection) 輕易繞過**：黑客只需簡單的混淆或 Jailbreak 即可誘騙 Agent 執行 `rm -rf /` 或外洩敏感金鑰。
2. **無法防範執行期競爭 (TOCTOU) 與延遲**：調用外部審查模型會產生 1~3 秒的巨大延遲，且無法管到作業系統系統呼叫 (Syscall)。
3. **缺乏法律不可否認性**：無法從密碼學上證明 *為什麼* Agent 執行了某項特權操作。

**DROS 不是 Prompt 包裝器，而是確定性執行期作業系統 (Deterministic Runtime OS)**：
將安全智慧移至編譯期 (`demo_policy.yaml` / `Vajra.md`)，並在運行期透過純記憶體常數時間 $\mathcal{O}(1)$ 位元圖譜直接在系統呼叫前**硬性熔斷 (Strict Fail-Closed)**！

---

## 🏛️ 二、 企業級 AI 六大信任基石模型 (DROS-6P)

DROS-VajraClaw 於 C-ABI / FFI 帶內執行層實時強制執行六大基礎信任邊界：

1. **主體身分 (Principal)**：3-Tier PKI 簽發之 `DrosIdentityToken (DIT)` 與原生 W3C `did:key` (Ed25519)，實現不可偽造的 Agent 身分綁定。
2. **確定性授權 (Authorization)**：不可篡改之 $\mathcal{O}(1)$ 權限位元圖譜，精確將角色映射至執行向量。
3. **系統呼叫閘門 (Action Bound)**：亞微秒級 (<500ns) 二進位攔截，施加硬性物理邊界。
4. **動態策略控制 (Policy Gate)**：動態敏感資料遮蔽、人機協同 (HITL) 與 ZKP-Lite 零知識證明。
5. **不可篡改審計 (Audit Log)**：SHA-256 Merkle Hash 鏈結 ＋ Ed25519 簽名，完全符合歐盟 AI 法案 (EU AI Act) 第 12 條規範。
6. **微秒級撤銷 (Expiry/Revocation)**：常數時間 $\mathcal{O}(1)$ 動態位元圖譜更新，實現微秒級權限撤銷與即時 HTTP 403 阻斷。

---

## 🔥 三、 官方全產品線與定價矩陣 (Product Lines & Pricing)

| 產品版本 | 定價 | 適用對象 | 核心授權與治理範疇 |
| :--- | :--- | :--- | :--- |
| **DSH 外掛版 (`dsh-plugin-vajraclaw`)** | **$0 (Apache-2.0 開源)** | DSH 終端使用者 | 純 TypeScript 進程內正則安全閥、本地 JSONL 雜湊鏈、支援升級 Docker 網關 |
| **Hacker Edition (Docker 網關)** | **$0 (個人永久免費)** | 個人開發者、研究人員 | 1 台主機、最多 5 並發 Agent、W3C DID 簽章、AST <1μs 硬熔斷、SHA-256 Merkle 鏈 |
| **Startup Edition (商用起步版)** | **$2,990 / 年** | AI 新創團隊、SaaS MVP | 3 台主機、每台 10 並發 Agent (共30 Agent)、C-ABI 原生庫 (`.dll`/`.so`)、多語言 SDK |
| **Enterprise Audit (企業審計版)** | **$29,990 / 年** | 金融 (FinTech)、醫療、大型企業 | 15 台主機、每台 30 並發 Agent (共450 Agent)、歐盟 AI 法案第12條法院級存證、硬體 HSM 綁定、私有雲隔離 |
| **Sovereign Mesh / Source Buyout** | **專案報價 (Custom Quote)** | 國防安全、主權 AI 基建 | 完整 C-ABI / Go / Rust 原始碼買斷、集中式 IAM Control Plane、K8s Helm、全球毫秒級緊急熔斷廣播 |

---

## ❓ 四、 技術與資安核心 FAQ (Frequently Asked Questions)

### Q1：黑客如果想辦法直接「替換或覆寫」DROS 微核心 (.dll / .so)，系統會破工嗎？
**A：絕對不會破工。** DROS 具備四重不變量防線：
1. **更換操作本身即是受管轄的 Syscall**：黑客若要覆寫二進位檔，必須驅使 Agent 執行 `cp`、`mv`、`curl` 或檔案寫入操作。在抵達 OS 前已被 DROS 帶內攔截。
2. **嚴格白名單 (Default Fail-Closed)**：未明確宣告為 `ALLOW` 的動作預設一律為 `BLOCK`，安全不依賴使用者的細心。
3. **內核級不可侵犯不變量 (Kernel Hard Invariants)**：DROS 編譯器強制將針對核心檔案與私鑰種子的寫入操作永久鎖定為 `HARD_BLOCKED`，即使管理員給予全放行權限亦無法覆寫。
4. **OS 內核檔案鎖與 Ed25519 簽名**：運行中的動態庫受 OS 內核鎖定（Windows `FILE_SHARE_READ` / Linux `ETXTBUSY`），宿主進程啟動時會校驗 Ed25519 數位簽章，竄改後進程直接中斷拒絕加載。

### Q2：如果使用者或管理員疏失，沒把某些危險指令寫入黑名單，會不會破工？
**A：完全不會。** DROS 採用零信任白名單架構（Default Fail-Closed）。使用者只需要宣告「允許哪些動作」，任何未註冊或未宣告的指令，在編譯期點陣圖中預設就是 `0`（拒絕），運行期直接硬性熔斷。

### Q3：DSH 純 TypeScript 外掛與 Docker 網關版有何差異？
**A：**
* **純 TS 外掛**：輕量免安裝 Docker，提供基礎的正則安全閥與防刪庫保護。
* **Docker 網關版**：具備完整 W3C `did:key` 密碼學身分、<1μs 微秒級 AST 硬熔斷、SHA-256 Merkle 法院級存證，並能同時跨平台聯防保護整台電腦上的所有 Agent（AGY、Claude、Codex、Cursor、DSH）。

---

## 📜 五、 相關技術核心論文與實測驗證 (Technical Foundations & Benchmarks)

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

## ⚖️ 六、 標準三大層級授權憲法聲明 (Standard 3-Tier License Constitution)

1. **核心執行期微內核 (Core Runtime Substrate) ➔ 專利保護 (Patent Pending)**：
   * DROS 執行期確定性治理與微秒帶內防禦技術已申請美國臨時專利保護（**U.S. Patent Application No. 64/111,973，Patent Pending**）。所有商業部署與生產環境實施權益由 康宸園有限公司 (Top-Celestial Company Ltd.) 專有保留。
2. **個人與社群外掛套件 (Community Client / Docker Gateway) ➔ 個人永久免費授權 (Free License for Individuals)**：
   * 賦能個人開發者獲得 1 微秒帶內硬熔斷保護（支援最多 5 個並發 Agent），源代碼專有保留，嚴禁第三方進行未經授權之企業商用或轉售。
3. **評測沙盒與重現套件 (Benchmark Harness) ➔ 評測工具開源 (Apache 2.0)**：
   * 開放評測代碼供學術重現與反證評鑑（評測代碼開源 ≠ 底層治理專利技術開源）。

---
**Developed by DROS Labs / 康宸園有限公司 (Top-Celestial Company Ltd.)**  
*Official Portal: [https://dr-os.io](https://dr-os.io) | Contact: [service@dr-os.io](mailto:service@dr-os.io)*
