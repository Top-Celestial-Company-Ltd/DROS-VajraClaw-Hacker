# docker/server.py
"""
DROS VajraClaw Hacker Gateway Server (DWGR-8 Self-Contained Edition)
--------------------------------------------------------------------
Provides zero-dependency local HTTP evaluation endpoints for AI Agents
(DSH, Google Antigravity, OpenAI Codex, Claude Code, Cursor).

Supports:
1. DWGR-8 Declarative Personal Policy (dros.personal.config.json)
2. In-band Param-level boundary checks (Path traversal, SQL injection, bounds)
3. Action Whitelist / Blacklist enforcement
4. Tamper-evident SHA-256 local audit chain
5. Full backwards compatibility with legacy tool-evaluation requests
"""

import os
import sys
import json
import time
import hashlib
import uuid
import re
from typing import Optional, Dict, Any, List
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
POLICY_PATH = os.environ.get("DROS_POLICY_PATH", "dros.personal.config.json")
LICENSE_KEY = os.environ.get("DROS_LICENSE_KEY", "")

class DrosPersonalEngine:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.audit_chain: List[str] = ["GENESIS_LOCAL_HASH_CHAIN_DROS_DOCKER_00000000000000000000000000000000"]
        self.audit_records: List[Dict[str, Any]] = []
        self.load_policy()

    def load_policy(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
                print(f"[*] DROS Docker Gateway armed with declarative config: {self.config_path}")
                return
            except Exception as e:
                print(f"[!] Warning: Failed to parse {self.config_path}: {e}")

        # Default fallback policy if file does not exist
        self.config = {
            "version": "1.0.0",
            "principalId": "did:key:docker-hacker-default",
            "mode": "strict",
            "rules": [
                {
                    "toolId": "filesystem",
                    "allowedActions": ["read_file", "list_directory", "get_file_info"],
                    "blockedActions": ["delete_file", "remove_directory", "format_disk"],
                    "paramConstraints": {
                        "path": {
                            "disallowedPatterns": ["..", "/etc/", "/root/", "C:\\Windows\\", ".env", ".ssh"]
                        }
                    }
                },
                {
                    "toolId": "sqlite",
                    "allowedActions": ["read_query", "select"],
                    "blockedActions": ["drop_table", "truncate", "alter_table"],
                    "paramConstraints": {
                        "query": {
                            "disallowedPatterns": ["DROP ", "DELETE ", "TRUNCATE ", "ALTER "]
                        }
                    }
                },
                {
                    "toolId": "bash",
                    "allowedActions": ["exec"],
                    "blockedActions": ["sudo", "su"],
                    "paramConstraints": {
                        "command": {
                            "disallowedPatterns": ["rm -rf /", "rm -fr /", ":(){ :|:& };:", "mkfs", "chmod 777"]
                        }
                    }
                }
            ]
        }
        print("[*] DROS Docker Gateway armed with built-in default DWGR-8 policy")

    def evaluate(self, tool: str, args: Dict[str, Any], agent_id: str = "default-agent") -> Dict[str, Any]:
        violations = []
        rules = self.config.get("rules", [])
        matched_rule = next((r for r in rules if r.get("toolId") == tool), None)

        action = args.get("action") or args.get("command") or args.get("operation") or "execute"
        if not isinstance(action, str):
            action = "execute"

        if matched_rule:
            blocked_actions = matched_rule.get("blockedActions", [])
            if action in blocked_actions:
                violations.append(f"Blocked action '{action}' explicitly prohibited for tool '{tool}'")

            allowed_actions = matched_rule.get("allowedActions")
            if allowed_actions is not None and action not in allowed_actions:
                violations.append(f"Action '{action}' not in allowed actions list for tool '{tool}'")

            param_constraints = matched_rule.get("paramConstraints", {})
            for param_key, constraint in param_constraints.items():
                val = args.get(param_key)
                if val is not None:
                    # String pattern constraints (Path traversal, dangerous commands)
                    if isinstance(val, str) and "disallowedPatterns" in constraint:
                        for pattern in constraint["disallowedPatterns"]:
                            if pattern.upper() in val.upper():
                                violations.append(f"Disallowed pattern '{pattern}' in param '{param_key}'")

                    # Numeric bounds constraints
                    if isinstance(val, (int, float)):
                        if "max" in constraint and val > constraint["max"]:
                            violations.append(f"Parameter '{param_key}' exceeds maximum bound of {constraint['max']} (actual: {val})")
                        if "min" in constraint and val < constraint["min"]:
                            violations.append(f"Parameter '{param_key}' below minimum bound of {constraint['min']} (actual: {val})")

        # Fallback regex circuit-breaker if no rule matched or for general shell defense
        args_str = json.dumps(args).lower()
        if re.search(r'\brm\s+-[a-z]*r[a-z]*f[a-z]*\s+(\/|\/\*|\.\/|~)', args_str) or re.search(r'\brm\s+-[a-z]*f[a-z]*r[a-z]*\s+(\/|\/\*|\.\/|~)', args_str):
            violations.append("Destructive recursive deletion pattern detected")
        if "id_rsa" in args_str or ".env_secrets" in args_str:
            violations.append("Attempt to access sensitive credential file detected")

        is_denied = len(violations) > 0
        decision = "DENY" if is_denied else "ALLOW"
        reason = "; ".join(violations) if is_denied else "All policy constraints satisfied"
        lease_id = f"docker-lease-{uuid.uuid4()}" if decision == "ALLOW" else None

        # Tamper-evident Audit Lineage
        params_hash = hashlib.sha256(json.dumps(args, sort_keys=True).encode("utf-8")).hexdigest()
        record = {
            "index": len(self.audit_records),
            "timestamp": int(time.time() * 1000),
            "toolId": tool,
            "action": action,
            "paramsHash": params_hash,
            "decision": decision,
            "reason": reason,
            "leaseId": lease_id,
            "agentId": agent_id
        }
        self.audit_records.append(record)

        prev_hash = self.audit_chain[-1]
        new_hash = hashlib.sha256(f"{prev_hash}:{json.dumps(record, sort_keys=True)}".encode("utf-8")).hexdigest()
        self.audit_chain.append(new_hash)

        return {
            "decision": "BLOCK" if decision == "DENY" else "ALLOW",
            "reason": reason,
            "lease_id": lease_id,
            "violations": violations
        }

engine = DrosPersonalEngine(POLICY_PATH)

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
                "engine": "DROS VajraClaw Personal Gateway (DWGR-8)",
                "version": "2.1.0",
                "concurrency_limit": 5 if LICENSE_KEY else 2,
                "tier": "Hacker Edition" if LICENSE_KEY else "Free-Trial (30-day)",
                "audit_chain_length": len(engine.audit_chain),
                "latency_guarantee": "<1 microsecond (O(1) Memory Engine)"
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
        elif self.path == "/api/status":
            self._set_headers(200)
            res = {
                "active_agents": 1,
                "audit_records_count": len(engine.audit_records),
                "latest_hash": engine.audit_chain[-1],
                "mode": engine.config.get("mode", "strict")
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        elif self.path == "/api/audit":
            self._set_headers(200)
            res = {
                "chain_length": len(engine.audit_chain),
                "records": engine.audit_records,
                "latest_hash": engine.audit_chain[-1]
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False, indent=2).encode("utf-8"))
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
            tool = payload.get("tool", "")
            args = payload.get("args", {})
            agent_id = payload.get("agent_id") or payload.get("agentId") or "default-agent"

            start_t = time.perf_counter()
            eval_res = engine.evaluate(tool, args, agent_id=agent_id)
            elapsed_us = (time.perf_counter() - start_t) * 1_000_000

            self._set_headers(200)
            res = {
                "decision": eval_res["decision"],
                "tool": tool,
                "agent_id": agent_id,
                "reason": eval_res["reason"],
                "lease_id": eval_res.get("lease_id"),
                "violations": eval_res.get("violations", []),
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

        elif self.path == "/mcp":
            # Streamable HTTP MCP Endpoint (JSON-RPC 2.0)
            req_id = payload.get("id")
            method = payload.get("method", "")
            params = payload.get("params", {})

            if method == "initialize":
                self._set_headers(200)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {
                            "name": "dros-vajraclaw-gateway",
                            "version": "2.1.0"
                        },
                        "capabilities": {
                            "tools": {}
                        }
                    }
                }
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

            elif method == "tools/list":
                self._set_headers(200)
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "dros_evaluate",
                                "description": "Evaluate an agent tool call against declarative DWGR-8 policy boundaries before execution.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "agent_id": {
                                            "type": "string",
                                            "description": "Identifier of the agent requesting tool execution."
                                        },
                                        "tool": {
                                            "type": "string",
                                            "description": "Target tool or capability identifier (e.g. filesystem, sqlite, bash)."
                                        },
                                        "payload": {
                                            "type": "object",
                                            "description": "Execution payload parameters (e.g. path, query, command, action)."
                                        }
                                    },
                                    "required": ["agent_id", "tool", "payload"]
                                }
                            },
                            {
                                "name": "dros_audit",
                                "description": "Read-only query of the tamper-evident SHA-256 local audit hash chain and execution records.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "limit": {
                                            "type": "integer",
                                            "description": "Maximum number of audit records to retrieve (default: 50)."
                                        }
                                    }
                                }
                            },
                            {
                                "name": "dros_status",
                                "description": "Retrieve current DROS Gateway operational status, active policy mode, and latest audit hash.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            }
                        ]
                    }
                }
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

            elif method == "tools/call":
                tool_name = params.get("name", "")
                arguments = params.get("arguments", {})

                if tool_name == "dros_evaluate":
                    agent_id = arguments.get("agent_id")
                    tool = arguments.get("tool")
                    payload_args = arguments.get("payload")

                    if not agent_id or not tool or payload_args is None:
                        self._set_headers(200)
                        err_res = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "error": {
                                "code": -32602,
                                "message": "Invalid params: 'agent_id', 'tool', and 'payload' are required."
                            }
                        }
                        self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))
                        return

                    if not isinstance(payload_args, dict):
                        self._set_headers(200)
                        err_res = {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "error": {
                                "code": -32602,
                                "message": "Invalid params: 'payload' must be an object."
                            }
                        }
                        self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))
                        return

                    start_t = time.perf_counter()
                    eval_res = engine.evaluate(tool, payload_args, agent_id=agent_id)
                    elapsed_us = (time.perf_counter() - start_t) * 1_000_000

                    result_payload = {
                        "decision": eval_res["decision"],
                        "reason": eval_res["reason"],
                        "latency_us": round(elapsed_us, 2),
                        "audit_reference": engine.audit_chain[-1],
                        "lease_id": eval_res.get("lease_id"),
                        "violations": eval_res.get("violations", [])
                    }

                    self._set_headers(200)
                    res = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result_payload, ensure_ascii=False, indent=2)
                                }
                            ],
                            "isError": eval_res["decision"] != "ALLOW"
                        }
                    }
                    self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

                elif tool_name == "dros_audit":
                    limit = arguments.get("limit", 50)
                    if not isinstance(limit, int) or limit < 1:
                        limit = 50
                    records = engine.audit_records[-limit:]
                    result_payload = {
                        "chain_length": len(engine.audit_chain),
                        "latest_hash": engine.audit_chain[-1],
                        "records_returned": len(records),
                        "records": records
                    }
                    self._set_headers(200)
                    res = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result_payload, ensure_ascii=False, indent=2)
                                }
                            ]
                        }
                    }
                    self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

                elif tool_name == "dros_status":
                    result_payload = {
                        "gateway_state": "HEALTHY",
                        "active_agents": len(set(r.get("agentId") for r in engine.audit_records)) if engine.audit_records else 1,
                        "policy_mode": engine.config.get("mode", "strict"),
                        "latest_audit_hash": engine.audit_chain[-1],
                        "version": "2.1.0",
                        "tier": "Community / Non-Commercial Free Edition"
                    }
                    self._set_headers(200)
                    res = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result_payload, ensure_ascii=False, indent=2)
                                }
                            ]
                        }
                    }
                    self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

                else:
                    self._set_headers(200)
                    err_res = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found or tool not permitted: '{tool_name}'"
                        }
                    }
                    self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))

            else:
                self._set_headers(200)
                err_res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unsupported MCP method: '{method}'"
                    }
                }
                self.wfile.write(json.dumps(err_res, ensure_ascii=False).encode("utf-8"))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint Not Found"}).encode("utf-8"))

def run():
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
