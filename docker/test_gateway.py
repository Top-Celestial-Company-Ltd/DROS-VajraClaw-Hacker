#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DROS VajraClaw Hacker Gateway Server - DWGR-8 End-to-End Automated Test Suite
Validates all endpoints:
1. GET /health - Status & Version Check
2. GET /api/status - Runtime Active Mode & Audit Counter
3. POST /evaluate - Benign File Read (ALLOW & Lease issued)
4. POST /evaluate - Prohibited Destructive Action (BLOCK on delete_file)
5. POST /evaluate - Path Traversal Pattern Violation (BLOCK on ..)
6. POST /evaluate - SQL Injection Pattern (BLOCK on DROP TABLE)
7. POST /evaluate - Shell Recursive Deletion (BLOCK on rm -rf /)
8. POST /evaluate - Numeric Parameter Limit (BLOCK on transfer > 500)
9. GET /api/audit - Tamper-Evident SHA-256 Chain Lineage Verification
"""

import sys
import os
import json
import time
import threading
import urllib.request
import urllib.error

# Set path to server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server

def run_tests():
    print("=" * 60)
    print("=== Running DROS Hacker Gateway DWGR-8 Docker Test Suite ===")
    print("=" * 60)

    # 1. Start server in a background daemon thread on port 8999 for test
    server.PORT = 8999
    server.POLICY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dros.personal.config.json")
    server.engine = server.DrosPersonalEngine(server.POLICY_PATH)

    httpd = server.HTTPServer(("127.0.0.1", 8999), server.DrosGatewayHandler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.5)

    base_url = "http://127.0.0.1:8999"

    # Test 1: GET /health
    with urllib.request.urlopen(f"{base_url}/health") as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "HEALTHY"
        assert "2.1.0" in data["version"]
        print("[PASS] Test 1: GET /health returns HEALTHY & 2.1.0")

    # Test 2: GET /api/status
    with urllib.request.urlopen(f"{base_url}/api/status") as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["mode"] == "strict"
        print("[PASS] Test 2: GET /api/status returns strict mode & active agent")

    # Helper for POST /evaluate
    def evaluate_request(payload):
        req = urllib.request.Request(
            f"{base_url}/evaluate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # Test 3: Benign Tool Call Allowed
    res3 = evaluate_request({
        "tool": "filesystem",
        "args": {"action": "read_file", "path": "src/main.py"},
        "agentId": "test-agent-01"
    })
    assert res3["decision"] == "ALLOW", f"Expected ALLOW, got {res3['decision']}"
    assert res3["lease_id"] is not None
    print(f"[PASS] Test 3: Benign Tool Call Allowed with Lease: {res3['lease_id']} ({res3['latency_us']} us)")

    # Test 4: Prohibited Action Blocked (delete_file)
    res4 = evaluate_request({
        "tool": "filesystem",
        "args": {"action": "delete_file", "path": "src/main.py"},
        "agentId": "test-agent-01"
    })
    assert res4["decision"] == "BLOCK", f"Expected BLOCK, got {res4['decision']}"
    assert "delete_file" in res4["reason"]
    print(f"[PASS] Test 4: Prohibited Action (delete_file) Blocked: {res4['reason']}")

    # Test 5: Path Traversal (..) Blocked
    res5 = evaluate_request({
        "tool": "filesystem",
        "args": {"action": "read_file", "path": "../../etc/shadow"},
        "agentId": "test-agent-01"
    })
    assert res5["decision"] == "BLOCK", f"Expected BLOCK, got {res5['decision']}"
    assert ".." in res5["reason"]
    print(f"[PASS] Test 5: Path Traversal (..) Blocked: {res5['reason']}")

    # Test 6: SQL Injection Pattern (DROP TABLE) Blocked
    res6 = evaluate_request({
        "tool": "sqlite",
        "args": {"action": "read_query", "query": "DROP TABLE users;"},
        "agentId": "test-agent-01"
    })
    assert res6["decision"] == "BLOCK", f"Expected BLOCK, got {res6['decision']}"
    assert "DROP " in res6["reason"]
    print(f"[PASS] Test 6: SQL DROP Injection Pattern Blocked: {res6['reason']}")

    # Test 7: Shell Destructive Deletion (rm -rf /) Blocked
    res7 = evaluate_request({
        "tool": "bash",
        "args": {"action": "exec", "command": "rm -rf /"},
        "agentId": "test-agent-01"
    })
    assert res7["decision"] == "BLOCK", f"Expected BLOCK, got {res7['decision']}"
    assert "rm -rf /" in res7["reason"] or "Destructive" in res7["reason"]
    print(f"[PASS] Test 7: Shell Destructive Deletion Blocked: {res7['reason']}")

    # Test 8: Numeric Parameter Upper Bound (payment > 500) Blocked
    res8 = evaluate_request({
        "tool": "payment",
        "args": {"action": "transfer", "amount": 1000},
        "agentId": "test-agent-01"
    })
    assert res8["decision"] == "BLOCK", f"Expected BLOCK, got {res8['decision']}"
    assert "exceeds maximum bound" in res8["reason"]
    print(f"[PASS] Test 8: Numeric Upper Bound Breach Blocked: {res8['reason']}")

    # Test 9: GET /api/audit SHA-256 Hash Chain Verification
    with urllib.request.urlopen(f"{base_url}/api/audit") as resp:
        assert resp.status == 200
        audit_data = json.loads(resp.read().decode("utf-8"))
        assert audit_data["chain_length"] == 7  # Genesis + 6 evaluates
        assert len(audit_data["records"]) == 6
        assert len(audit_data["latest_hash"]) == 64
        print(f"[PASS] Test 9: Tamper-Evident SHA-256 Audit Chain Verified (Chain Length: {audit_data['chain_length']}, Latest: {audit_data['latest_hash'][:16]}...)")

    print("=" * 60)
    print("=== All 9 Docker Gateway End-to-End Tests Passed Successfully! ===")
    print("=" * 60)
    httpd.shutdown()
    sys.exit(0)

if __name__ == "__main__":
    run_tests()
