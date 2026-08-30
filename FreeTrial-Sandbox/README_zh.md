# 🛡️ DROS™ 金剛爪 VajraClaw (免費試用版 / Free Trial PLG)
[![官方網站](https://img.shields.io/badge/Website-dr--os.io-purple.svg?style=for-the-badge)](https://dr-os.io)

[English](README.md) | [繁體中文](README_zh.md)

**版本：v1.0.0-free**

**自主型 AI Agent 系統之執行治理工業標準 (Execution Governance Standard)**

歡迎使用 DROS VajraClaw 開源免費試用版。本目錄包含核心 $\mathcal{O}(1)$ 物理熔斷器引擎與攻擊模擬沙盒（具備 30 天離線 RSA 時間憑證限制，支援最多 2 個並發 AI Agent 實例）。

## 🛑「如果運行期還需要智慧去判斷，系統就已經被攻破了。」
在企業資安領域，依賴提示工程 (Prompt Engineering) 已經宣告失效。無論您的系統提示詞寫得多麼嚴密，越獄 (Jailbreak) 與提示注入 (Prompt Injection) 終究會找到破口。傳統 API 網關之所以潰敗，是因為它們誤將人類導向的靜態邊界套用在自主 AI Agent 之上。

**DROS** 絕非單純的 Prompt 封裝層。它是**執行治理標準 (Execution Governance Standard)**。我們將智慧前移至編譯期 (`demo_policy.yaml`)，並在運行期透過 **$\mathcal{O}(1)$ 位元圖譜引擎** (`core/vajra_claw.dll` / `.so`) 實施強制熔斷。一旦 Agent 嘗試發起越權操作，DROS 會立即觸發**物理硬熔斷 (Strict Fail-Closed)**，於 1 毫秒內中斷進程。

## ⚡ 效能基準 (Performance Benchmark)
我們的引擎以 **$\mathcal{O}(1)$ 常數時間** 運作，運行期零 JSON 解析開銷：
- **正常執行安全開銷**：~5.6 ms
- **惡意攻擊攔截硬熔斷延遲**：**~0.37 ms**

## 🚀 快速上手 (Quick Start Demo)
1. 確保已安裝 Python 3.8+。安裝依賴：`pip install PyYAML`。
2. 檢視 `demo_policy.yaml` 中定義的 $\mathcal{O}(1)$ 邊界約束。
3. 執行攻擊模擬：`python run_demo_attack.py`。
4. 親眼見證引擎在 1 毫秒內物理攔截提示注入攻擊（First Denial Moment）！

---
**由 DROS Labs 開發**  
*以確定性執行守護自主 AI 前沿。*
