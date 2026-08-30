#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json

def dros_enforce(agent_role: str, tool_name: str, args: dict) -> bool:
    try:
        req = urllib.request.Request(
            "http://localhost:8080/evaluate",
            data=json.dumps({"agent_id": agent_role, "tool": tool_name, "args": args}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=1.0) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res.get("allowed", False)
    except Exception as e:
        print(f"[DROS Enforcement Alert] {e}")
        return False

if __name__ == "__main__":
    print("Legal Agent checking contract:", dros_enforce("Legal_Agent", "read_contract", {"path": "nda.pdf"}))
    print("Dev Agent attempting payment:", dros_enforce("Dev_Agent", "execute_payment", {"amount": 50000}))
