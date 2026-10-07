#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DROS VajraClaw - 併發熔斷高載壓力測試工具
此工具使用 asyncio 與 httpx 同時發起 3 個並行推理請求。
預期在 Free-Trial 版 (限制 2 併發) 下，會有 2 個順利放行，而第 3 個會被 SDK 物理熔斷 (回傳 429 阻斷)！
"""

import asyncio
import httpx
import sys
import time

# 強制控制台使用 UTF-8 編碼
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROXY_URL = "http://127.0.0.1:5000/v1/chat/completions"

def print_banner(text: str):
    print("\n" + "=" * 65)
    print(f" {text.center(63)}")
    print("=" * 65)

async def send_single_request(client: httpx.AsyncClient, task_id: int, stream: bool = True):
    payload = {
        "messages": [{"role": "user", "content": f"隨機法義開採測試_{task_id}: 什麼是阿陀那識？"}],
        "stream": stream,
        "model": "bodhisattva"
    }
    
    print(f"🚀 [協程 {task_id}] 發起並行 API 請求 (stream={stream})...")
    start_time = time.time()
    
    try:
        if stream:
            # 測試串流併發熔斷
            async with client.stream("POST", PROXY_URL, json=payload, timeout=20.0) as response:
                latency = time.time() - start_time
                if response.status_code == 200:
                    print(f"✅ [協程 {task_id}] \033[92m【連線成功 (200 OK)】\033[0m 耗時: {latency:.2f} 秒。開始流式讀取...")
                    # 讀取首個 chunk 作為抵達驗證，隨後關閉流
                    async for line in response.aiter_lines():
                        if line.strip():
                            print(f"   -> [協程 {task_id}] 首位 Token 抵達: {line[:60]}...")
                            break
                    # 持續讀取直至流結束以佔用併發
                    async for line in response.aiter_lines():
                        pass
                    print(f"🧹 [協程 {task_id}] 流式傳輸結束。")
                elif response.status_code == 429:
                    # 讀取錯誤內容
                    error_text = await response.aread()
                    try:
                        error_json = error_text.decode('utf-8')
                        error_msg = error_json
                    except:
                        error_msg = str(error_text)
                    print(f"🚨 [協程 {task_id}] \033[91m【併發熔斷觸發 (429 Too Many Requests)】\033[0m 耗時: {latency:.2f} 秒")
                    print(f"   -> 阻斷訊息: {error_msg}")
                else:
                    print(f"⚠️ [協程 {task_id}] 異常狀態碼: {response.status_code}，耗時: {latency:.2f} 秒")
        else:
            # 測試非串流併發熔斷
            response = await client.post(PROXY_URL, json=payload, timeout=20.0)
            latency = time.time() - start_time
            if response.status_code == 200:
                print(f"✅ [協程 {task_id}] \033[92m【連線成功 (200 OK)】\033[0m 耗時: {latency:.2f} 秒")
            elif response.status_code == 429:
                print(f"🚨 [協程 {task_id}] \033[91m【併發熔斷觸發 (429 Too Many Requests)】\033[0m 耗時: {latency:.2f} 秒")
                print(f"   -> 阻斷訊息: {response.text}")
            else:
                print(f"⚠️ [協程 {task_id}] 異常狀態碼: {response.status_code}，耗時: {latency:.2f} 秒")
                
    except httpx.ConnectError:
        print(f"❌ [協程 {task_id}] 無法連線至 Proxy 伺服器，請確保已在另一個終端機啟動 `python main.py --serve`。")
    except Exception as e:
        print(f"❌ [協程 {task_id}] 協程執行異常: {e}")

async def main():
    print_banner("DROS VajraClaw 桌面版 2 併發熔斷壓力測試")
    print(f"目標網關: {PROXY_URL}")
    print("我們將以【完全並行】的方式發起 3 個 API 協程...")
    print("預期結果：2 個成功放行讀取，第 3 個被 429 當場熔斷！")
    print("=" * 65)
    
    # 建立連接池
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    async with httpx.AsyncClient(limits=limits) as client:
        # 同時排程 3 個連線任務
        tasks = [
            send_single_request(client, 1, stream=True),
            send_single_request(client, 2, stream=True),
            send_single_request(client, 3, stream=True)
        ]
        
        # 同步啟動並行發包
        await asyncio.gather(*tasks)
        
    print_banner("壓力測試評估報告")
    print("🎉 併發物理防禦力驗證完成。您可以從上方日誌看見 429 阻斷的效果！")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    # 使用 asyncio 執行
    asyncio.run(main())
