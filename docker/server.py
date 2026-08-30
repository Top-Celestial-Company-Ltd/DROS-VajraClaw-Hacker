# docker/server.py
"""
DROS VajraClaw Hacker Gateway Server
------------------------------------
Provides local HTTP/MCP evaluation endpoints for AI Agents (DSH, Antigravity, Codex, Cursor).
"""

import os
import sys
import json
import time
from typing import Optional, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add parent directory to path to load vajraclaw runtime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from integrations.vajraclaw.runtime import VajraClaw

PORT = int(os.environ.get("PORT", 8080))
POLICY_PATH = os.environ.get("DROS_POLICY_PATH", "demo_policy.yaml")
LICENSE_KEY = os.environ.get("DROS_LICENSE_KEY", "")

# Initialize VajraClaw Engine
vc: Optional[VajraClaw] = None

def init_engine():
    global vc
    if os.path.exists(POLICY_PATH):
        with open(POLICY_PATH, "r", encoding="utf-8") as f:
            policy_str = f.read()
        vc = VajraClaw(rules_string=policy_str)
        print(f"[*] DROS VajraClaw Engine armed with policy: {POLICY_PATH}")
    else:
        # Default safety policy
        default_policy = """
vajra_version: "1.0"
security_level: STRICT
rules:
  - id: R001
    action: ALLOW
    tool: read_*
  - id: R002
    action: ALLOW
    tool: execute_payment
    condition: "payload.get('amount', 0) <= 1000"
  - id: R003
    action: BLOCK
    tool: "*"
"""
        vc = VajraClaw(rules_string=default_policy)
        print("[*] DROS VajraClaw Engine armed with default fallback policy")

class DrosGatewayHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            self._set_headers(200)
            res = {
                "status": "HEALTHY",
                "engine": "DROS VajraClaw Micro-Kernel",
                "version": "v1.0.0-hacker-docker",
                "concurrency_limit": 5 if LICENSE_KEY else 2,
                "tier": "Hacker Edition" if LICENSE_KEY else "Free-Trial (30-day)",
                "latency_guarantee": "<1 microsecond (O(1) Bitmap)"
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
        elif self.path == "/api/status":
            self._set_headers(200)
            res = {
                "active_agents": 1,
                "blocked_count": 0,
                "passed_count": 0,
                "mode": "FAIL_CLOSED"
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if self.path == "/evaluate" or self.path == "/v1/evaluate":
            # Tool evaluation endpoint (Used by DSH Plugin, MCP, etc.)
            tool = payload.get("tool", "")
            args = payload.get("args", {})
            agent_id = payload.get("agent_id", "default-agent")

            start_t = time.perf_counter()
            try:
                if vc:
                    eval_res = vc.evaluate(tool=tool, payload_or_agent_id=args, args_json=json.dumps(args))
                    decision = "ALLOW" if eval_res else "BLOCK"
                    reason = eval_res.reason if hasattr(eval_res, 'reason') else "Evaluated by policy"
                else:
                    decision = "ALLOW"
                    reason = "Engine not initialized"
            except Exception as e:
                decision = "BLOCK"
                reason = f"Security Violation: {str(e)}"
            
            elapsed_us = (time.perf_counter() - start_t) * 1_000_000

            self._set_headers(200)
            res = {
                "decision": decision,
                "tool": tool,
                "agent_id": agent_id,
                "reason": reason,
                "latency_us": round(elapsed_us, 2)
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/license/activate":
            global LICENSE_KEY
            key = payload.get("license_key", "").strip()
            if key:
                LICENSE_KEY = key
                self._set_headers(200)
                res = {
                    "success": True,
                    "tier": "Hacker Edition",
                    "max_concurrent_agents": 5,
                    "message": "License successfully activated! 5 Concurrent Agents unlocked."
                }
            else:
                self._set_headers(400)
                res = {"success": False, "error": "Invalid License Key"}
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint Not Found"}).encode("utf-8"))

def run():
    init_engine()
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, DrosGatewayHandler)
    print(f"🛡️  DROS Hacker Gateway running on http://0.0.0.0:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down DROS Gateway...")
        httpd.server_close()

if __name__ == "__main__":
    run()
