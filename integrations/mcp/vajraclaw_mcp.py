"""
VajraClaw × MCP (Model Context Protocol) Integration
------------------------------------------------------
Wraps MCP tool execution with VajraClaw capability enforcement.
Any tool invocation through this middleware is physically checked
before reaching the MCP Tool Execution Server.

This positions VajraClaw as a deterministic enforcement layer
at the MCP client → server boundary.

Architecture:
    MCP Client
        ↓
    VajraMCPMiddleware   ← VajraClaw enforcement here
        ↓
    MCP Tool Execution Server

Usage:
    from vajraclaw_mcp import VajraMCPMiddleware
    middleware = VajraMCPMiddleware(agent_id="customer-service-bot")
    result = middleware.call_tool("filesystem.write", {"path": "/etc/config"})
"""

import os
import sys
from typing import Any, Dict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from vajraclaw import VajraClaw


# Default inline demo policy
_DEFAULT_POLICY = """
# VajraClaw MCP Demo Policy
# Only read operations are authorized.
# Write / execute operations require elevated capability.
allowed_tools:
  - filesystem.read
  - db.query
  - web.search
"""


class VajraMCPMiddleware:
    """
    VajraClaw enforcement middleware for MCP tool calls.

    Drop this in between your MCP client and tool execution server.
    All tool invocations are capability-checked before execution.
    """

    def __init__(
        self,
        agent_id: str,
        policy: str = None,
        policy_file: str = None,
        core_path: str = None,
    ):
        self.agent_id = agent_id

        if policy_file:
            self._vc = VajraClaw(core_path=core_path, rules=policy_file)
        else:
            self._vc = VajraClaw(
                core_path=core_path,
                rules_string=policy or _DEFAULT_POLICY,
            )

    def call_tool(
        self,
        tool_name: str,
        payload: Dict[str, Any],
        executor=None,
    ) -> Dict[str, Any]:
        """
        Evaluate and (if authorized) execute an MCP tool call.

        Args:
            tool_name: The MCP tool identifier (e.g. "filesystem.write")
            payload:   The tool's input parameters
            executor:  Optional callable executor(tool_name, payload) → result
                       If not provided, returns a mock success response.

        Returns:
            A dict with status and result, or a blocked denial response.
        """
        result = self._vc.evaluate(tool=tool_name, agent_id=self.agent_id)

        if not result:
            print(result)  # Prints the full ❌ denial report
            return {
                "status": "blocked",
                "tool": tool_name,
                "agent_id": self.agent_id,
                "reason": "VajraClaw: capability violation — execution physically blocked",
                "vajraclaw_decision": "BLOCK",
            }

        print(result)  # Prints ✅ ALLOW

        # Execute via provided executor, or mock
        if executor:
            output = executor(tool_name, payload)
        else:
            output = f"[MCP] Tool '{tool_name}' executed with payload: {payload}"

        return {
            "status": "ok",
            "tool": tool_name,
            "result": output,
            "vajraclaw_decision": "ALLOW",
        }


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    middleware = VajraMCPMiddleware(agent_id="customer-service-bot")

    print("=" * 60)
    print("VajraClaw × MCP — Enforcement Demo")
    print("=" * 60)

    # ── Test 1: Authorized read (should ALLOW) ───────────────────────────
    print("\n[Test 1] Agent calls filesystem.read (authorized)")
    resp = middleware.call_tool("filesystem.read", {"path": "/data/report.pdf"})
    print(f"  Response: {resp['status']}")

    # ── Test 2: Unauthorized write (should BLOCK) ────────────────────────
    print("\n[Test 2] Agent calls filesystem.write (NOT authorized)")
    resp = middleware.call_tool(
        "filesystem.write", {"path": "/etc/config", "content": "malicious payload"}
    )
    print(f"  Response: {resp['status']} — {resp.get('reason', '')}")

    # ── Test 3: Simulate an attack escalation ────────────────────────────
    print("\n[Test 3] Agent calls db.execute (attack attempt)")
    resp = middleware.call_tool("db.execute", {"sql": "DROP TABLE users"})
    print(f"  Response: {resp['status']} — {resp.get('reason', '')}")

    print("\n" + "=" * 60)
    print("Demo complete.")
    print("=" * 60)
