# VajraClaw Hacker 版金鑰管理與備份指南 (KEY_MANAGEMENT.md)

本指南專為 **個人開發者與極客（Solo Developers / Hackers）** 設計。在本地單機或輕量化開發場景中，DROS / VajraClaw 透過將「安全合約簽署」與「執行端驗證」實體分離來保護您的系統安全。為了避免系統更新時發生預期外的物理熔斷，請遵循本指南妥善管理與備份您的 Ed25519 簽署金鑰。

> [!CAUTION]
> **核心安全聲明：原廠無後門與金鑰救援機制（No Backdoors Warning）**
> * **聯絡原廠也無法救援**：DROS / VajraClaw 嚴格遵循零信任安全原則，系統中**不包含任何原廠萬能金鑰或後門**。如果您遺失了私鑰種子（Seed Hex），**即使聯絡原廠也完全無法幫您復原私鑰，亦無法替您簽署新的 `policy.bin`**。
> * **唯一救贖路徑**：您必須手動執行「重建信任根」程序（詳見第 3 節情況 B）。這要求您必須仍保有對伺服器的最高管理員權限（SSH/Root），重新生成金鑰對並逐一更新所有執行端節點的公鑰配置。如果同時遺失私鑰與伺服器控制權，系統將永久鎖死，無法升級。

---

## 1. 為什麼個人開發者也需要備份私鑰？

VajraClaw 採用非對稱加密技術：
* **簽發端（您的開發電腦）**：持有 **私鑰種子（Seed Hex）**，用於將安全策略 YAML 編譯並簽章為二進位 `policy.bin`。
* **執行端（運行 AI 的本地伺服器或背景代理）**：僅持有 **公鑰（Verify Key）**，用於校驗 `policy.bin` 的完整性。

如果您沒有指定 `--key` 進行編譯，編譯器將預設使用隨機的 **臨時金鑰（Ephemeral Key）**。這意味著您每次編譯出來的 `policy.bin` 簽名都不同。為了在執行端實施穩定的策略管理，您**必須使用靜態金鑰**。

如果您遺失了這組靜態私鑰，您將無法在公鑰不變的狀況下更新任何安全規則。

---

## 2. 金鑰生成與備份三步驟

### 第一步：生成固定金鑰
您可以在本地終端執行以下 Python 程式碼，生成一組永久的金鑰對：
```python
import nacl.signing
import binascii

# 生成隨機金鑰種子 (Seed)
signing_key = nacl.signing.SigningKey.generate()
seed_hex = binascii.hexlify(signing_key.encode()).decode('utf-8')
pub_hex = binascii.hexlify(signing_key.verify_key.encode()).decode('utf-8')

print(f"請儲存您的私鑰種子 (32-byte Seed Hex): {seed_hex}")
print(f"請配置您的驗證公鑰 (PubKey Hex)      : {pub_hex}")
```

### 第二步：安全備份（個人開發者推薦）
* **密碼管理器**：請將生成的 `Seed Hex` 存放在您本機的密碼管理器（如 KeePass, Bitwarden, 1Password）作為安全備註。
* **防止 Git 洩漏**：千萬不要將包含 `seed_hex` 的腳本提交到 GitHub 等代碼庫。可將私鑰配置於環境變數中，編譯時讀取。

### 第三步：編譯時指定金鑰
在編譯您的金剛合約時，帶入 `--key` 參數：
```bash
python cli.py build contracts/demo_policy.yaml -o policy.bin --key <您的私鑰種子 Hex>
```

---

## 3. 災難復原步驟 (Disaster Recovery)

當您的開發電腦損毀，但您需要更新執行端的安全政策時：

### 情況 A：私鑰種子有備份（推薦）
1. 在新電腦上重新安裝 Python 與依賴庫（`pip install pynacl pyyaml`）。
2. 從密碼管理器取出備份的 `Seed Hex`。
3. 執行上述第三步編譯命令，重新產出帶簽章的 `policy.bin`。
4. 將 `policy.bin` 部署覆蓋到您的執行端。執行端 GuardVM 將自動驗證通過，無需修改任何設定。

### 情況 B：私鑰種子也遺失了（災難重建）
1. 依據第 2 節重新生成一對全新的 `NEW_SEED` 與 `NEW_PUBKEY`。
2. 使用 `NEW_SEED` 重新編譯您的政策。
3. 登入運行 AI 的伺服器，將配置檔（或 `gemini_proxy.py` 初始化代碼）中的舊驗證公鑰替換為 `NEW_PUBKEY`。
4. 將 `NEW_SEED` 妥善存入密碼管理器備份。
5. 重啟代理服務（如重啟 `dros-proxy`），使新公鑰生效並加載新的 `policy.bin`。
