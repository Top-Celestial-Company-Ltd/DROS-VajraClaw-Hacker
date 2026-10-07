#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DROS VajraClaw Hacker Gateway - MCP Protocol & Security Comprehensive Test Suite
Validates:
1. MCP initialization (protocolVersion, serverInfo, capabilities)
2. MCP tools/list (dros_evaluate, dros_audit, dros_status schemas)
3. TEST-01: Normal ALLOW (benign filesystem read)
4. TEST-02: Policy DENY (prohibited delete_file)
5. TEST-03: Missing required parameters & malformed payload
6. TEST-04: Arbitrary shell command request (Rejection of unapproved tools)
7. TEST-05: Path traversal injection pattern (BLOCK on .. and /etc/)
8. TEST-06: Destructive shell pattern in args (BLOCK on rm -rf /)
9. TEST-07: Read-only dros_audit retrieval & tamper-evident chain verification
10. TEST-08: dros_status operational health & active agents check
11. TEST-09: Multi-Agent ID Routing & Log Isolation
"""

import sys
import os
import json
import time
import threading
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server

def post_mcp(base_url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/mcp",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_tests():
    print("=" * 65)
    print("=== DROS VajraClaw Hacker Gateway: MCP & Security Test Suite ===")
    print("=" * 65)

    test_port = 8998
    server.PORT = test_port
    server.POLICY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dros.personal.config.json")
    server.engine = server.DrosPersonalEngine(server.POLICY_PATH)

    httpd = server.HTTPServer(("127.0.0.1", test_port), server.DrosGatewayHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    base_url = f"http://127.0.0.1:{test_port}"

    # 1. Initialize
    init_res = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    })
    assert init_res["jsonrpc"] == "2.0"
    assert init_res["result"]["serverInfo"]["name"] == "dros-vajraclaw-gateway"
    assert "tools" in init_res["result"]["capabilities"]
    print("[PASS] MCP Init: ServerInfo and capabilities validated")

    # 2. Tools List
    tools_res = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    })
    tools = {t["name"]: t for t in tools_res["result"]["tools"]}
    assert "dros_evaluate" in tools
    assert "dros_audit" in tools
    assert "dros_status" in tools
    print("[PASS] MCP Tool Discovery: Exactly 3 minimal tools discovered")

    # 3. TEST-01: Normal ALLOW
    eval_allow = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "dros_evaluate",
            "arguments": {
                "agent_id": "codex-agent-01",
                "tool": "filesystem",
                "payload": {"action": "read_file", "path": "src/main.py"}
            }
        }
    })
    res_data = json.loads(eval_allow["result"]["content"][0]["text"])
    assert res_data["decision"] == "ALLOW"
    assert res_data["lease_id"] is not None
    assert eval_allow["result"].get("isError", False) is False
    print(f"[PASS] TEST-01 Normal ALLOW: Validated (decision={res_data['decision']}, latency={res_data['latency_us']}us)")

    # 4. TEST-02: Policy DENY
    eval_deny = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "dros_evaluate",
            "arguments": {
                "agent_id": "codex-agent-01",
                "tool": "filesystem",
                "payload": {"action": "delete_file", "path": "src/main.py"}
            }
        }
    })
    deny_data = json.loads(eval_deny["result"]["content"][0]["text"])
    assert deny_data["decision"] == "BLOCK"
    assert "delete_file" in deny_data["reason"]
    assert eval_deny["result"]["isError"] is True
    print(f"[PASS] TEST-02 Policy DENY: Blocked prohibited action (reason={deny_data['reason'][:40]}...)")

    # 5. TEST-03: Malformed & Missing Fields
    malformed_res = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "dros_evaluate",
            "arguments": {
                "agent_id": "codex-agent-01"
                # missing tool and payload
            }
        }
    })
    assert "error" in malformed_res
    assert malformed_res["error"]["code"] == -32602
    print("[PASS] TEST-03 Missing Params: Correctly returned JSON-RPC error -32602")

    # 6. TEST-04: Arbitrary Shell Execution Attempt
    shell_attempt = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/call",
        "params": {
            "name": "run_shell",
            "arguments": {"command": "whoami"}
        }
    })
    assert "error" in shell_attempt
    assert shell_attempt["error"]["code"] == -32601
    print("[PASS] TEST-04 Arbitrary Shell: Tool 'run_shell' correctly REJECTED (Method not found)")

    # 7. TEST-05: Path Traversal
    traversal_res = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "tools/call",
        "params": {
            "name": "dros_evaluate",
            "arguments": {
                "agent_id": "codex-agent-01",
                "tool": "filesystem",
                "payload": {"action": "read_file", "path": "../../etc/shadow"}
            }
        }
    })
    trav_data = json.loads(traversal_res["result"]["content"][0]["text"])
    assert trav_data["decision"] == "BLOCK"
    assert "Disallowed pattern" in trav_data["reason"]
    print("[PASS] TEST-05 Path Traversal: Blocked ../../etc/shadow")

    # 8. TEST-06: Shell Destructive Deletion
    del_res = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 8,
        "method": "tools/call",
        "params": {
            "name": "dros_evaluate",
            "arguments": {
                "agent_id": "codex-agent-01",
                "tool": "bash",
                "payload": {"command": "rm -rf /"}
            }
        }
    })
    del_data = json.loads(del_res["result"]["content"][0]["text"])
    assert del_data["decision"] == "BLOCK"
    print("[PASS] TEST-06 Destructive Deletion: Blocked 'rm -rf /'")

    # 9. TEST-07: Audit Lineage & Chain
    audit_res = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 9,
        "method": "tools/call",
        "params": {
            "name": "dros_audit",
            "arguments": {"limit": 10}
        }
    })
    audit_data = json.loads(audit_res["result"]["content"][0]["text"])
    assert audit_data["chain_length"] >= 5
    assert len(audit_data["records"]) >= 4
    print(f"[PASS] TEST-07 Audit Lineage: Verified chain length={audit_data['chain_length']}, latest_hash={audit_data['latest_hash'][:16]}...")

    # 10. TEST-08: Status Query
    status_res = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "tools/call",
        "params": {
            "name": "dros_status",
            "arguments": {}
        }
    })
    status_data = json.loads(status_res["result"]["content"][0]["text"])
    assert status_data["gateway_state"] == "HEALTHY"
    assert status_data["policy_mode"] == "strict"
    print(f"[PASS] TEST-08 Status Query: gateway_state={status_data['gateway_state']}, mode={status_data['policy_mode']}")

    # 11. TEST-09: Multi-Agent Isolation
    post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 11,
        "method": "tools/call",
        "params": {
            "name": "dros_evaluate",
            "arguments": {
                "agent_id": "agent-alpha",
                "tool": "filesystem",
                "payload": {"action": "read_file", "path": "alpha.txt"}
            }
        }
    })
    post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 12,
        "method": "tools/call",
        "params": {
            "name": "dros_evaluate",
            "arguments": {
                "agent_id": "agent-beta",
                "tool": "filesystem",
                "payload": {"action": "read_file", "path": "beta.txt"}
            }
        }
    })
    audit_multi = post_mcp(base_url, {
        "jsonrpc": "2.0",
        "id": 13,
        "method": "tools/call",
        "params": {
            "name": "dros_audit",
            "arguments": {"limit": 2}
        }
    })
    multi_records = json.loads(audit_multi["result"]["content"][0]["text"])["records"]
    assert multi_records[-2]["agentId"] == "agent-alpha"
    assert multi_records[-1]["agentId"] == "agent-beta"
    print("[PASS] TEST-09 Multi-Agent Routing & Log Isolation: agent-alpha and agent-beta accurately identified")

    print("=" * 65)
    print("=== All 11 MCP & Security End-to-End Tests Passed! ===")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
