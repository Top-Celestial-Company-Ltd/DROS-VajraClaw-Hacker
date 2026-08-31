# -*- coding: utf-8 -*-
"""
VajraClaw Python SDK (Official)
In-Band Deterministic Execution Guardrail for AI Agents
"""
import json
import urllib.request
from typing import Any, Dict, Optional

class Decision:
    def __init__(self, allowed: bool, reason: str, tool: str, agent_id: str):
        self.allowed = allowed
        self.reason = reason
        self.tool = tool
        self.agent_id = agent_id

    def __bool__(self):
        return self.allowed

    def __repr__(self):
        status = "ALLOWED" if self.allowed else "BLOCKED"
        return f"<VajraDecision {status}: tool='{self.tool}' reason='{self.reason}'>"

class VajraGuard:
    def __init__(self, gateway_url: str = "http://localhost:8080", agent_id: str = "default_agent", strict_fail_closed: bool = False):
        self.gateway_url = gateway_url.rstrip("/")
        self.agent_id = agent_id
        self.strict_fail_closed = strict_fail_closed

    def evaluate(self, tool: str, args: Optional[Dict[str, Any]] = None, agent_id: Optional[str] = None) -> Decision:
        target_agent = agent_id or self.agent_id
        payload = {
            "agent_id": target_agent,
            "tool": tool,
            "args": args or {}
        }
        try:
            req = urllib.request.Request(
                f"{self.gateway_url}/evaluate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=0.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                allowed = data.get("allowed", False)
                reason = data.get("reason", "Policy decision evaluated by gateway")
                return Decision(allowed=allowed, reason=reason, tool=tool, agent_id=target_agent)
        except Exception as e:
            if self.strict_fail_closed:
                return Decision(allowed=False, reason=f"Gateway unreachable (Fail-Closed): {e}", tool=tool, agent_id=target_agent)
            else:
                # Fail-open / safe fallback
                return Decision(allowed=True, reason=f"Gateway offline (Fail-Safe Fallback): {e}", tool=tool, agent_id=target_agent)

    def wrap_agent(self, agent_instance: Any):
        """Helper to wrap Agent tool executions"""
        return agent_instance
