# 🛡️ DROS™ VajraClaw Hacker Edition: 安全規範與執行期邊界 (SAFETY.md)
<!-- dros_component: vajraclaw-hacker-safety -->
<!-- dros_status: Active -->

本文件定義 **DROS VajraClaw (Hacker Edition 個人免費版)** 在本機工作站與開發環境中的安全防護邊界、白帽紅隊測試準則與漏洞通報協議。

---

## 1. 🎯 治理網關定位與安全邊界 (Security Boundary)

DROS VajraClaw Hacker Edition 定位為**本地獨立執行期治理網關 (Deterministic Runtime Governance Gateway)**，介於自主 AI Agent（如 Claude Code, Cursor, Codex, LangChain, CrewAI）與本地作業系統/敏感 API 之間。

### ✅ 核心防禦能力 (In-Scope Protections)
1. **工具調用帶內硬攔截 (<1ms Gateway / <3μs PDP)**：透過編譯期 AST 策略與 $\mathcal{O}(1)$ 位元圖查表，在 Agent 嘗試調用未授權工具（如刪庫、格式化磁碟、提權命令）瞬間實體阻斷。
2. **敏感憑證與路徑隔離**：攔截 Agent 讀取 `.env`、SSH 私鑰、OAuth Token 或雲端憑證的未授權存取。
3. **不可否認審計鏈 (Audit Trail)**：所有通過與被阻斷的決策均以 Ed25519 簽名與 SHA-256 雜湊鏈存證，防止日誌被 Agent 掩蓋或竄改。
4. **W3C `did:key` 身分綁定**：每個被納管的 Agent 均配置唯一密碼學憑證，防範跨進程偽造與提權。

### ⚠️ 防護邊界與非承諾事項 (Out-of-Scope Constraints)
1. **非靜態程式碼審計器**：本網關重點在**執行期（Runtime）的 Tool Call 與特權命令攔截**，不負責靜態預測自然語言對話的所有語意變化。
2. **底層系統呼叫非承諾 (Syscall Mediation Boundary)**：本開源 Hacker 版為應用層與代理網關攔截；針對底層作業系統任意原生系統呼叫 (Arbitrary Kernel Syscalls) 之硬性隔離，屬於 OS-level PGM 模組範疇。
3. **本機資源配額上限**：個人 Hacker 免費版設計為單機防禦，最多同時守護 **5 個並發 Agent**；若需大規模分散式 Mesh 或硬體 HSM 綁定，屬於 Enterprise 方案範疇。
4. **網路硬體防火牆替代**：本系統為應用層與系統呼叫治理網關，不替代實體交換機與網路層 IDS/IPS。

---

## 2. ⚔️ 白帽紅隊測試與負責任使用準則 (Ethical Hacking & Red-Teaming)

本工具特別提供給安全研究員測試 Agent 的抗注入與越權能力，使用者必須遵守以下白帽原則：
1. **僅限已授權之環境**：所有提示注入（Prompt Injection）、Jailbreak、與越權模擬測試，僅限於使用者自身擁有的機器或獲得明確書面授權的受控沙盒內。
2. **禁止武器化開發**：嚴禁用於開發惡意 Agent、規避企業合規監管、或撰寫攻擊載體。
3. **免責聲明**：使用者因違反授權或濫用本開源工具對第三方造成的任何損害，開發團隊概不承擔法律責任。

---

## 3. 🚨 弱點通報與漏洞協同揭露程序 (Vulnerability Disclosure Policy)

若您在微核心（Go/C-ABI）、策略編譯器（`cli.py`）或 Docker 網關中發現逃逸路徑、記憶體錯誤或策略繞過缺陷：

- **通報原則**：請遵循負責任的協同揭露原則（CVD），**切勿在 GitHub Public Issues 公開張貼 0-day PoC**。
- **專屬回報管道**：
  - **Security Email**: `security@top-celestial.com.tw`
  - **信件主旨**: `[VULNERABILITY] VajraClaw Hacker - <漏洞簡述>`
- **承諾與協同**：
  - 我們將在 **48 小時內** 確認收到並立案分析。
  - 在 **7 個工作天內** 提供修復補丁或緩解策略。
  - 請通報者提供至少 **90 天之協同揭露保密期**，以利發行安全性更新。

---

## 4. ⚖️ 專利聲明與授權條款 (Patent & License Notice)

- **專利保護宣告**：
  > **專利聲明：** DROS 執行治理與安全技術已申請美國臨時專利保護（U.S. Patent Application No. 64/111,973，Patent Pending）。
- **授權條款**：
  - 個人版微核心代碼遵循 **AGPL-3.0** 授權。
  - 個人開發者、學生與安全研究人員享有永久免費個人授權；商業產品嵌入或企業級部署請聯繫商務授權 (`jimmychen@top-celestial.com.tw`)。

---
*Top-Celestial Security & Governance Engineering Team.*
