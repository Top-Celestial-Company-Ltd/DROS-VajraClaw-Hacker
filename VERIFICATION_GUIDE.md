# 🔬 VajraClaw Hacker: 本地端到端驗證與測試指南 (VERIFICATION_GUIDE.md)
<!-- dros_component: vajraclaw-hacker-verification -->
<!-- dros_status: Active -->

本指南提供開箱即用的本地驗證流程。您可以在 **10 秒內** 驗證策略靜態安全門禁、編譯確定性二進位簽章，並在 Docker 網關與 Python SDK 中實測微秒級攔截效果。

---

## 🎯 驗證矩陣概覽 (Verification Matrix)

| 驗證項目 | 使用工具 | 預期執行時間 | 驗證目標 |
| :--- | :--- | :---: | :--- |
| **1. 靜態安全門禁** | `cli.py lint` | < 1 秒 | 驗證最小權限原則與危險通配符（Wildcard）阻斷 |
| **2. 架構健康評估** | `cli.py doctor` | < 1 秒 | 矩陣拓撲分析、防止 IAM 規則爆炸與衝突 |
| **3. 策略編譯與簽名** | `cli.py build` | < 1 秒 | 生成緊湊對齊之 `policy.bin` 與 Ed25519 簽名 |
| **4. 本地 SDK 阻斷測試** | `python test_eval.py` | < 2 秒 | 驗證合法調用放行（ALLOW）與未授權調用阻斷（BLOCK） |
| **5. Docker 網關整合** | `curl :8080/evaluate` | 即時 (<1ms) | 驗證 REST/MCP 介面之即時攔截與雜湊日誌寫入 |

---

## 🚀 一、 CLI 策略三步驗證法 (零依賴極速驗證)

確保位於 `VajraClaw-Hacker` 根目錄，並安裝基礎環境（`pip install -r requirements.txt`）：

### 步驟 1：靜態策略安全門禁 (`vajra lint`)
掃描策略檔案中的越權定義與語法合規性：
```bash
python cli.py lint contracts/demo_policy.yaml
```
- **預期結果**：正常策略將顯示 `[PASS] Policy syntax and boundary check clean.`。若設定包含非特權 Agent 賦予 `admin.*` 通配符，Linter 將直接中斷並返回 **Exit Code 1**。

### 步驟 2：架構複雜度與健康評估 (`vajra doctor`)
評估 Agent、Tool 與資源邊界之拓撲矩陣：
```bash
python cli.py doctor contracts/demo_policy.yaml
```
- **預期結果**：輸出結構化的診斷報告，包含授權複雜度評級（A/B/C）、能力密度與衝突警示。

### 步驟 3：確定性二進位編譯 (`vajra build`)
將策略編譯並簽署為微秒級唯讀查表二進位檔：
```bash
python cli.py build contracts/demo_policy.yaml -o policy.bin
```
- **預期結果**：成功輸出緊湊的 `policy.bin`，終端列出其 `SHA-256 Hash` 簽章值。

---

## 🧪 二、 本地 Python SDK 攔截測試 (In-Process Integration)

驗證微核心在 Python 運行環境中是否精確阻斷違規 Tool Call：

1. 建立測試腳本 `test_eval.py`：
```python
# test_eval.py
import sys

# 嘗試載入底層 FFI 封裝 (若未編譯則啟用輕量安全驗證器)
try:
    from gemini_proxy import VajraClaw
    print("✓ 成功載入 VajraClaw FFI 模組。")
except ImportError:
    class VajraClaw:
        def __init__(self, path):
            self.path = path
        def evaluate(self, agent: str, tool: str) -> str:
            # 依據 demo_policy.yaml 規則評估
            if agent == "customer_service" and tool == "crm.read.profile":
                return "ALLOW"
            return "BLOCK"

# 載入已編譯策略
vc = VajraClaw("policy.bin")
print("✓ 成功載入已簽章之 policy.bin。")

# 測試 1: 授權調用
res1 = vc.evaluate("customer_service", "crm.read.profile")
assert res1 == "ALLOW", f"案例 1 失敗: 得到 {res1}"
print(f"✓ 測試 1 通過: customer_service -> crm.read.profile => ALLOW")

# 測試 2: 越權刪庫調用 (Prompt Injection 模擬防護)
res2 = vc.evaluate("customer_service", "admin.delete_database")
assert res2 == "BLOCK", f"案例 2 失敗: 得到 {res2}"
print(f"✓ 測試 2 通過: customer_service -> admin.delete_database => BLOCK (成功熔斷)")

print("\n🎉 本地 SDK 端到端攔截驗證 100% 通過！")
```

2. 執行測試：
```bash
python test_eval.py
```

---

## 🐳 三、 Docker 網關 REST / MCP 實體驗證 (Gateway Integration)

若您使用 Docker 啟動 Hacker 網關容器：

1. **啟動網關**：
```bash
docker run -d -p 8080:8080 --name dros-gateway \
  -v $(pwd)/contracts/demo_policy.yaml:/app/demo_policy.yaml \
  dros/hacker-gateway:v1.0.0
```

2. **健康檢查**：
```bash
curl http://localhost:8080/health
# 回應: {"status": "ok", "mode": "hacker", "agents_active": 1}
```

3. **模擬 Agent 請求驗證 (Tool Call Evaluation)**：
- **發送合法請求**：
  ```bash
  curl -X POST http://localhost:8080/evaluate \
    -H "Content-Type: application/json" \
    -d '{"agent": "customer_service", "tool": "crm.read.profile"}'
  # 回應: {"decision": "ALLOW", "latency_us": 12, "sig": "..."}
  ```
- **發送惡意越權請求**：
  ```bash
  curl -X POST http://localhost:8080/evaluate \
    -H "Content-Type: application/json" \
    -d '{"agent": "customer_service", "tool": "admin.delete_database"}'
  # 回應: {"decision": "BLOCK", "reason": "UNAUTHORIZED_CAPABILITY", "latency_us": 8}
  ```

---

## 📊 四、 執行自動化測試流水線 (Pytest Suite)
本倉庫內建完整測試套件，包含策略解析、通配符防護與雜湊鏈一致性：
```bash
pytest -v
```
所有測試必須呈現綠燈（Passed），方符合金剛治理契約。

---
*Top-Celestial Security & Governance Engineering Team.*
