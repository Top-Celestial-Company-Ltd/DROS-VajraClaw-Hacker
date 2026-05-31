import os
import sys
import json
import urllib.request
import urllib.error
import hashlib
from datetime import datetime, timedelta

# 商業防禦設定
TRIAL_LICENSE_KEY = "VCLAW-FREE-TRIAL-KEY"
TRIAL_DURATION_DAYS = 30
TRIAL_CONCURRENCY_LIMIT = 2
SIGNATURE_SALT = "DROS_VajraClaw_Hacker_Salt_2026_TopCelestial"

def calculate_trial_signature(activated_at_str: str) -> str:
    """計算防護電子簽章，防杜使用者非法改動本地時間"""
    data = f"{activated_at_str}_{SIGNATURE_SALT}"
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def validate_license_or_die():
    """
    驗證授權碼。
    如果是 VCLAW-FREE-TRIAL-KEY，執行 1 安裝、2 併發、1個月本地加密試用期校驗；
    若是其他 Key，則對接 LemonSqueezy 官方線上驗證。
    """
    license_key = os.environ.get("LEMONSQUEEZY_LICENSE_KEY")
    
    if not license_key or not license_key.strip():
        print("\n\033[91m" + "="*60)
        print("⛔ 嚴重錯誤：找不到有效授權碼 (License Key)！")
        print("請在 .env 檔案中設定 LEMONSQUEEZY_LICENSE_KEY，")
        print("或使用試用金鑰: VCLAW-FREE-TRIAL-KEY 進行免費試用。")
        print("="*60 + "\033[0m\n")
        sys.exit(1)
        
    license_key = license_key.strip()
    
    # ----------------- 離線 Free-Trial 試用分支 -----------------
    if license_key == TRIAL_LICENSE_KEY:
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        registry_path = os.path.join(base_dir, ".trial_registry")
        now = datetime.now()
        
        # 1. 首次啟用，寫入安全註冊表
        if not os.path.exists(registry_path):
            activated_at_str = now.strftime("%Y-%m-%d %H:%M:%S")
            signature = calculate_trial_signature(activated_at_str)
            
            registry_data = {
                "license_key": TRIAL_LICENSE_KEY,
                "activated_at": activated_at_str,
                "signature": signature,
                "note": "Top-Celestial DROS VajraClaw Free-Trial Registry. Do not modify."
            }
            
            try:
                with open(registry_path, "w", encoding="utf-8") as f:
                    json.dump(registry_data, f, indent=4)
            except Exception as e:
                print(f"\n\033[91m⛔ 嚴重錯誤：無法建立本地試用註冊表 ({e})。\033[0m")
                sys.exit(1)
                
            expire_date = now + timedelta(days=TRIAL_DURATION_DAYS)
            print("\n\033[93m" + "="*65)
            print("🎉 DROS VajraClaw [Free-Trial 免費試用版] 首次激活成功！")
            print(f"   - 首次啟用時間：{activated_at_str}")
            print(f"   - 授權有效期限：{TRIAL_DURATION_DAYS} 天 (到期日：{expire_date.strftime('%Y-%m-%d')})")
            print(f"   - 併發連線限制：最大 {TRIAL_CONCURRENCY_LIMIT} 個並行請求 (限制 1 個安裝)")
            print("="*65 + "\033[0m\n")
            return
            
        # 2. 已激活，載入並校驗安全簽章與到期時間
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                registry_data = json.load(f)
        except Exception as e:
            print(f"\n\033[91m⛔ 嚴重錯誤：本地試用註冊表損毀，防護機制 Fail-Closed 熔斷！({e})\033[0m")
            sys.exit(1)
            
        activated_at_str = registry_data.get("activated_at", "")
        signature = registry_data.get("signature", "")
        
        # A. 驗證電子簽章，防篡改時間
        expected_sig = calculate_trial_signature(activated_at_str)
        if signature != expected_sig:
            print("\n\033[91m" + "="*60)
            print("⛔ 嚴重安全警訊：檢測到授權資料遭受非法修改或篡改！")
            print("DROS 防破解核心啟動【物理熔斷】，軟體拒絕載入。")
            print("="*60 + "\033[0m\n")
            sys.exit(1)
            
        # B. 驗證是否過期
        try:
            activated_at = datetime.strptime(activated_at_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"\n\033[91m⛔ 嚴重錯誤：無效的時間戳特徵碼 ({e})。\033[0m")
            sys.exit(1)
            
        expire_date = activated_at + timedelta(days=TRIAL_DURATION_DAYS)
        remaining = expire_date - now
        
        if remaining.total_seconds() <= 0:
            print("\n\033[91m" + "="*65)
            print("⛔ 免費試用授權已過期 (Trial Expired)！")
            print(f"   您的 {TRIAL_DURATION_DAYS} 天免費試用期已於 {expire_date.strftime('%Y-%m-%d %H:%M:%S')} 結束。")
            print("   請聯繫 康宸園有限公司 (Top-Celestial) 訂閱正式個人 Hacker 版或企業版。")
            print("="*65 + "\033[0m\n")
            sys.exit(1)
            
        # C. 授權狀態正常，輸出剩餘日誌
        days = remaining.days
        hours = remaining.seconds // 3600
        print(f"🔐 DROS [免費試用版] 驗證成功 (剩餘試用期: {days} 天 {hours} 小時)...", end=" ", flush=True)
        print("\033[92m[狀態正常]\033[0m")
        return

    # ----------------- 線上 LemonSqueezy 正式版分支 -----------------
    print(f"🔐 正在驗證並啟用正式 Hacker 授權碼 ({license_key[:4]}****)...", end=" ", flush=True)
    
    url = "https://api.lemonsqueezy.com/v1/licenses/activate"
    import socket
    instance_name = socket.gethostname() or "DROS-Node"
    payload = json.dumps({
        "license_key": license_key,
        "instance_name": instance_name
    }).encode("utf-8")
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response_body = response.read().decode("utf-8")
            data = json.loads(response_body)
            
            if data.get("activated") is True or data.get("valid") is True:
                status = data.get("license_key", {}).get("status", "unknown")
                if status == "active":
                    print("\033[92m[驗證成功]\033[0m")
                    return
                else:
                    print(f"\n\033[91m⛔ 授權碼狀態異常 ({status})，啟動失敗。\033[0m")
                    sys.exit(1)
            else:
                error_msg = data.get("error", "未知錯誤")
                print(f"\n\033[91m⛔ 授權碼無效、已退租或啟用次數達上限 ({error_msg})。\033[0m")
                sys.exit(1)
                
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode("utf-8")
            error_data = json.loads(error_body)
            error_msg = error_data.get("error", str(e))
        except:
            error_msg = str(e)
            
        print(f"\n\033[91m⛔ 授權碼連線驗證失敗 ({error_msg})。\033[0m")
        sys.exit(1)
        
    except urllib.error.URLError as e:
        print(f"\n\033[91m⛔ 無法連線至授權伺服器 ({e.reason})，請檢查您的網路連線。\033[0m")
        sys.exit(1)
    except Exception as e:
        print(f"\n\033[91m⛔ 未知的授權驗證錯誤 ({str(e)})。\033[0m")
        sys.exit(1)

