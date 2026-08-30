# VajraClaw Python Runtime
# Wraps the Go Mobile SDK via ctypes for use in Python AI stacks (LangChain, MCP, etc.)
#
# Architecture:
#   This package calls the core C-shared binary (vajra_claw.dll / .so)
#   which exposes the O(1) enforcement kernel via C-FFI.
#
#   For enterprise governance features (Modes C/D, Ed25519, JSONL Audit),
#   use the Go Mobile SDK directly (vajraclaw_sdk/mobile/).
#
# Usage:
#   from vajraclaw import VajraClaw
#   vc = VajraClaw(core_path="./core/vajra_claw.dll", rules="./Vajra.md")
#   result = vc.evaluate(tool="db.write", agent_id="finance-agent")

from .runtime import VajraClaw, Decision

__all__ = ["VajraClaw", "Decision"]
__version__ = "0.1.0"
