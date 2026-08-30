#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json

class DROSGuard:
    def __init__(self, gateway_url="http://localhost:8080"):
        self.gateway_url = gateway_url

    def check_tool(self, tool_name: str, payload: dict) -> bool:
        try:
            req = urllib.request.Request(
                f"{self.gateway_url}/evaluate",
                data=json.dumps({"tool": tool_name, "args": payload}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("allowed", False)
        except Exception as e:
            print(f"[DROS Alert] Guard evaluation error: {e}")
            return False

if __name__ == "__main__":
    guard = DROSGuard()
    print("1. Benign tool call:", guard.check_tool("query_weather", {"city": "Taipei"}))
    print("2. Dangerous deletion:", guard.check_tool("execute_shell", {"command": "rm -rf /"}))
