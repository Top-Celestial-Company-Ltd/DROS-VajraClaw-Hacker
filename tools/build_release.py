import os
import sys
import shutil
import subprocess
from pathlib import Path

# 解決 Windows cp950 編碼問題
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def main():
    base_dir = Path(__file__).resolve().parent.parent
    os.chdir(base_dir)

    print("🚀 開始建構 VajraClaw-Hacker (PyInstaller) ...")

    # PyInstaller 指令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "VajraClaw-Hacker",
        "--onedir",
        "--noconfirm",
        "--clean",
        # Uvicorn & Quart 隱藏依賴
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.protocols",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.websockets",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.lifespan",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "quart",
        "--hidden-import", "google.generativeai",
        "main.py"
    ]

    subprocess.run(cmd, check=True)

    dist_dir = base_dir / "dist" / "VajraClaw-Hacker"
    print(f"✅ 編譯完成！輸出目錄：{dist_dir}")

    # 複製必要的外部配置檔到 dist_dir，讓使用者可以直接執行並修改
    print("📦 複製必要配置檔...")
    
    # 複製 config.yaml
    if (base_dir / "config.yaml").exists():
        shutil.copy2(base_dir / "config.yaml", dist_dir / "config.yaml")
        print("  - 複製 config.yaml")
        
    # 複製 .env 範本 (避免覆蓋真實的金鑰，改名為 .env 或 .env.example)
    if (base_dir / ".env").exists():
        # 為了讓使用者直接能用，我們直接複製為 .env (若有真實機密，建議先清空 LEMONSQUEEZY_LICENSE_KEY)
        # 這裡我們讀取 .env 並將其複製，確保有 VCLAW-FREE-TRIAL-KEY 範例
        with open(base_dir / ".env", "r", encoding="utf-8") as f:
            env_content = f.read()
        
        with open(dist_dir / ".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("  - 複製 .env")
        
    # 複製 dros_golden_manifest.json (如果存在)
    if (base_dir / "dros_golden_manifest.json").exists():
        shutil.copy2(base_dir / "dros_golden_manifest.json", dist_dir / "dros_golden_manifest.json")
        print("  - 複製 dros_golden_manifest.json")

    # 壓縮為 ZIP
    print("🗜️ 正在壓縮為 ZIP 檔...")
    shutil.make_archive(str(base_dir / "dist" / "VajraClaw-Hacker-Win64"), 'zip', root_dir=base_dir / "dist", base_dir="VajraClaw-Hacker")
    
    print("🎉 發布包建立成功：dist/VajraClaw-Hacker-Win64.zip")

if __name__ == "__main__":
    main()
