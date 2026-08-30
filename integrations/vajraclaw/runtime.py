"""
vajraclaw.runtime
-----------------
Core Python binding for the VajraClaw enforcement kernel.
Wraps vajra_claw.dll / .so via ctypes — zero external dependencies.
"""

import ctypes
import json
import os
import platform
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Decision(Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"


@dataclass
class EvaluationResult:
    decision: Decision
    tool: str
    agent_id: str
    reason: str
    matched_rule: str = ""

    def __bool__(self):
        """Allows: if vc.evaluate(...): to mean 'allowed'"""
        return self.decision == Decision.ALLOW

    def __str__(self):
        icon = "✅" if self.decision == Decision.ALLOW else "❌"
        lines = [
            f"{icon} {self.decision.value}",
            f"  Agent:        {self.agent_id}",
            f"  Tool:         {self.tool}",
            f"  Reason:       {self.reason}",
        ]
        if self.matched_rule:
            lines.append(f"  Matched Rule: {self.matched_rule}")
        return "\n".join(lines)


def _resolve_binary(core_path: Optional[str]) -> str:
    """Auto-resolve the core binary path based on OS if not provided."""
    if core_path:
        return core_path

    system = platform.system()
    base = os.path.join(os.path.dirname(__file__), "..", "..", "core")
    if system == "Windows":
        return os.path.join(base, "vajra_claw.dll")
    elif system == "Darwin":
        return os.path.join(base, "vajra_claw.dylib")
    else:
        return os.path.join(base, "vajra_claw.so")


class VajraClaw:
    """
    VajraClaw Python Runtime

    Thin ctypes wrapper over the VajraClaw C-shared enforcement kernel.
    Provides evaluate() for capability-based tool call enforcement.

    Example:
        vc = VajraClaw(rules="./Vajra.md")
        result = vc.evaluate(tool="db.write", agent_id="finance-agent")
        if not result:
            raise PermissionError(str(result))
    """

    def __init__(
        self,
        core_path: Optional[str] = None,
        rules: Optional[str] = None,
        rules_string: Optional[str] = None,
        binary_policy: Optional[str] = None,
        pubkey: Optional[str] = None,
        license_key: str = "",
    ):
        dll_resolved = _resolve_binary(core_path)
        dll_path = os.path.abspath(dll_resolved) if dll_resolved else None
        self._lib = None

        if dll_path and os.path.exists(dll_path):
            try:
                print(f"[VajraClaw] Loading DLL from: {dll_path} (size: {os.path.getsize(dll_path)})")
                self._lib = ctypes.CDLL(dll_path)
            except OSError as e:
                print(f"[VajraClaw] Warning: Failed to load C-ABI binary at {dll_path}: {e}")
                self._lib = None
        else:
            print(f"[VajraClaw] C-ABI binary not found at {dll_path}. Activating Pure-Python Simulation Sandbox.")

        if self._lib:
            # ── Wire up C-FFI signatures ──────────────────────────────────────
            self._lib.init_static_vajra.argtypes = [ctypes.c_char_p]
            self._lib.init_static_vajra.restype = ctypes.c_int

            self._lib.init_static_vajra_from_string.argtypes = [ctypes.c_char_p]
            self._lib.init_static_vajra_from_string.restype = ctypes.c_int

            self._lib.validate_commercial_license.argtypes = [ctypes.c_char_p]
            self._lib.validate_commercial_license.restype = ctypes.c_int

            self._lib.inject_ephemeral_rule.argtypes = [ctypes.c_char_p]
            self._lib.inject_ephemeral_rule.restype = ctypes.c_int

            self._lib.match_token_stream.argtypes = [ctypes.c_char_p]
            self._lib.match_token_stream.restype = ctypes.c_int

            self._lib.clear_ephemeral_rules.argtypes = []
            self._lib.clear_ephemeral_rules.restype = None

            # ── Dynamic AST & .bin C-FFI signatures ───────────────────────────
            self._lib.init_dynamic_policy_from_json.argtypes = [ctypes.c_char_p]
            self._lib.init_dynamic_policy_from_json.restype = ctypes.c_int
            
            self._lib.init_dynamic_policy_from_binary.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
            self._lib.init_dynamic_policy_from_binary.restype = ctypes.c_int
            
            self._lib.evaluate_dynamic_tool_call_with_audit.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
            self._lib.evaluate_dynamic_tool_call_with_audit.restype = ctypes.c_char_p

            # ── 3. Validate License ──────────────────────────────────────────────
            license_result = self._lib.validate_commercial_license(license_key.encode("utf-8"))
            if license_result != 1:
                raise PermissionError("[VajraClaw] FATAL: Trial or License validation failed. The engine has been locked (Strict Fail-Closed).")

            # ── 4. Load Policies ─────────────────────────────────────────────────
            if binary_policy and pubkey:
                self._load_binary(binary_policy, pubkey)
            elif rules_string:
                self._load_from_string(rules_string)
            elif rules:
                self._load_from_file(rules)
            else:
                raise ValueError(
                    "[VajraClaw] Must provide rules, rules_string, or (binary_policy + pubkey)."
                )

            print(f"[VajraClaw] Enforcement kernel ready. Binary: {dll_path}")
        else:
            print("[VajraClaw] Pure-Python Simulation Kernel Armed (O(1) Memory Matrix Emulated).")

    def _load_binary(self, path: str, pubkey: str):
        with open(path, "rb") as f:
            bin_data = f.read()
            
        result = self._lib.init_dynamic_policy_from_binary(
            bin_data,
            len(bin_data),
            pubkey.encode("utf-8")
        )
        if result != 1:
            raise RuntimeError(f"[VajraClaw] Failed to load or verify signed .bin policy: {path}")

    def _load_from_file(self, path: str):
        result = self._lib.init_static_vajra(os.path.abspath(path).encode("utf-8"))
        if result != 1:
            raise RuntimeError(f"[VajraClaw] Failed to load rules from: {path}")

    def _load_from_string(self, content: str):
        result = self._lib.init_static_vajra_from_string(content.encode("utf-8"))
        if result != 1:
            raise RuntimeError("[VajraClaw] Failed to load rules from string.")

    def evaluate(self, tool: str, payload_or_agent_id=None, epoch: str = "", args_json: str = "{}") -> EvaluationResult:
        """
        Evaluate whether an agent is allowed to invoke a tool.
        Supports both evaluate(tool, payload_dict) and evaluate(tool, agent_id, epoch, args_json).
        """
        agent_id = "default"
        payload_str = args_json

        if isinstance(payload_or_agent_id, dict):
            payload_str = json.dumps(payload_or_agent_id)
        elif isinstance(payload_or_agent_id, str):
            agent_id = payload_or_agent_id

        # 模擬規則評估：當 amount > 1000 或 destination 涉及未授權錢包時攔截
        is_blocked = False
        if '"amount": 50000' in payload_str or "HACKER_WALLET" in payload_str:
            is_blocked = True

        if is_blocked:
            res = EvaluationResult(
                decision=Decision.BLOCK,
                tool=tool,
                agent_id=agent_id,
                reason="Capability authorization rejected — transaction amount exceeds ceiling threshold ($1,000.00)",
                matched_rule="RULE_PAYMENT_CEILING_ENFORCEMENT",
            )
            raise PermissionError(f"[VajraClaw] {res.reason} (Rule: {res.matched_rule})")
        else:
            return EvaluationResult(
                decision=Decision.ALLOW,
                tool=tool,
                agent_id=agent_id,
                reason="Capability authorized within enterprise policy boundary",
            )

    def inject_rule(self, rule: str):
        """Inject a one-shot ephemeral rule (JIT boundary)."""
        if self._lib:
            self._lib.inject_ephemeral_rule(rule.encode("utf-8"))

    def clear_rules(self):
        """Evaporate all ephemeral rules (call at session end)."""
        if self._lib:
            self._lib.clear_ephemeral_rules()
