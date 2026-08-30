"""
VajraClaw × LangChain Integration Demo
---------------------------------------
This demo shows how to wrap a LangChain agent's tool calls
with VajraClaw enforcement. When the agent attempts an
unauthorized action, execution is physically blocked before
any system call is made.

Features demonstrated:
1. Dynamic AST Engine: Blocks if 'amount' > 1000
2. Epoch Lock: Requires 'v2-stable'
3. Binary Policy: Loads cryptographically signed .bin file

Requirements:
    pip install langchain langchain-openai pydantic PyNaCl

Run:
    python demo_langchain.py
"""

import os
import sys
import json
import subprocess
from typing import Any

# ── 0. Compile Demo Policy Binary ─────────────────────────────────────────────
# We simulate the process of compiling a security policy into a signed binary.
import nacl.signing
# Use a known seed so we know the public key
SEED_HEX = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
sk = nacl.signing.SigningKey(bytes.fromhex(SEED_HEX))
PUB_HEX = sk.verify_key.encode().hex()

# A demo policy allowing file.read, db.read, and conditionally execute_payment
DEMO_YAML = """
epoch: "v2-stable"
tool_policies:
  - name: "file.read"
    effect: "allow"
  - name: "db.read"
    effect: "allow"
  - name: "execute_payment"
    effect: "allow"
    conditions:
      - field: "amount"
        operator: "<="
        value: 1000
"""
with open("demo_rules.yaml", "w") as f:
    f.write(DEMO_YAML)

print("[Demo] Compiling test policy to .bin using Ed25519 signature...")
compile_script = os.path.join(os.path.dirname(__file__), "..", "..", "cli", "vajra_compile.py")
subprocess.run([
    sys.executable, compile_script,
    "--policy", "demo_rules.yaml",
    "--out", "demo_policy.bin",
    "--key", SEED_HEX
], check=True)
print("[Demo] Compilation complete.\n")

# ── VajraClaw ─────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from integrations.vajraclaw.runtime import VajraClaw

# ── LangChain ─────────────────────────────────────────────────────────────────
from langchain.tools import BaseTool

# Initialize the enforcement kernel with the binary policy
vc = VajraClaw(binary_policy="demo_policy.bin", pubkey=PUB_HEX)


# ── Wrap ANY LangChain BaseTool with VajraClaw enforcement ───────────────────
class VajraProtectedTool(BaseTool):
    """
    A LangChain BaseTool wrapper that enforces VajraClaw capability checks
    before executing the underlying tool.

    Wrap any existing tool:
        protected = VajraProtectedTool.wrap(my_tool, agent_id="finance-agent")
    """

    name: str = "vajra_protected_tool"
    description: str = ""
    _inner: Any = None
    _agent_id: str = "default"
    _epoch: str = "v2-stable"

    @classmethod
    def wrap(cls, tool: BaseTool, agent_id: str = "default", epoch: str = "v2-stable") -> "VajraProtectedTool":
        wrapped = cls()
        wrapped.name = tool.name
        wrapped.description = tool.description
        wrapped._inner = tool
        wrapped._agent_id = agent_id
        wrapped._epoch = epoch
        return wrapped

    def _run(self, *args, **kwargs) -> str:
        # Evaluate dynamically using arguments (AST engine) and Epoch lock
        args_json = json.dumps(kwargs)
        result = vc.evaluate(
            tool=self.name,
            agent_id=self._agent_id,
            epoch=self._epoch,
            args_json=args_json
        )

        if not result:
            # ❌ PHYSICAL BLOCK — print full denial report and raise
            print(result)
            raise PermissionError(
                f"[VajraClaw] Execution blocked: agent '{self._agent_id}' "
                f"is not authorized to call '{self.name}' with args {kwargs}"
            )

        print(result)
        return self._inner._run(*args, **kwargs)

    async def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)


# ── Mock tools (simulate a real agent environment) ────────────────────────────
class MockDbReadTool(BaseTool):
    name: str = "db.read"
    description: str = "Read records from the database"

    def _run(self, query: str = "") -> str:
        return f"[DB] Read result for: {query}"

class MockDbWriteTool(BaseTool):
    name: str = "db.write"
    description: str = "Write records to the database"

    def _run(self, data: str = "") -> str:
        return f"[DB] Written: {data}"

class MockExecutePaymentTool(BaseTool):
    name: str = "execute_payment"
    description: str = "Execute a financial payment"

    def _run(self, amount: int = 0, to: str = "") -> str:
        return f"[BANK] Payment of ${amount} to {to} executed successfully."


# ── Main demo ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    agent_id = "finance-agent"

    # Wrap tools with VajraClaw enforcement
    protected_read = VajraProtectedTool.wrap(MockDbReadTool(), agent_id=agent_id)
    protected_write = VajraProtectedTool.wrap(MockDbWriteTool(), agent_id=agent_id)
    protected_payment = VajraProtectedTool.wrap(MockExecutePaymentTool(), agent_id=agent_id)

    print("=" * 70)
    print("VajraClaw × LangChain — Enforcement Demo")
    print("=" * 70)

    # ── Test 1: Authorized tool (should ALLOW) ───────────────────────────
    print("\n[Test 1] Agent calls db.read (whitelisted tool)")
    try:
        output = protected_read._run(query="SELECT * FROM transactions")
        print(f"  Result: {output}")
    except PermissionError as e:
        print(f"  {e}")

    # ── Test 2: Unauthorized tool (should BLOCK) ─────────────────────────
    print("\n[Test 2] Agent calls db.write (NOT in whitelist)")
    try:
        output = protected_write._run(data="DROP TABLE users")
        print(f"  Result: {output}")
    except PermissionError as e:
        print(f"  → Correctly blocked. Agent cannot write to DB.")

    # ── Test 3: AST Dynamic Parameter Check (ALLOW) ──────────────────────
    print("\n[Test 3] Agent calls execute_payment with amount=500 (within limits)")
    try:
        output = protected_payment._run(amount=500, to="Supplier A")
        print(f"  Result: {output}")
    except PermissionError as e:
        print(f"  {e}")

    # ── Test 4: AST Dynamic Parameter Check (BLOCK) ──────────────────────
    print("\n[Test 4] Agent calls execute_payment with amount=5000 (exceeds limit!)")
    try:
        output = protected_payment._run(amount=5000, to="Hacker Wallet")
        print(f"  Result: {output}")
    except PermissionError as e:
        print(f"  → Correctly blocked. Prompt Injection foiled! Over limit.")

    # ── Test 5: Downgrade Attack (Epoch Mismatch BLOCK) ──────────────────
    print("\n[Test 5] Downgrade Attack: App expects 'v2-stable', but runtime loads 'v1-old'")
    # We simulate this by changing the app's expected epoch to something else
    hacked_read = VajraProtectedTool.wrap(MockDbReadTool(), agent_id=agent_id, epoch="v3-future")
    try:
        output = hacked_read._run(query="SELECT * FROM secrets")
        print(f"  Result: {output}")
    except PermissionError as e:
        print(f"  → Correctly blocked. Epoch mismatch detected.")

    print("\n" + "=" * 70)
    print("Demo complete. VajraClaw physically enforced all capability boundaries.")
    print("=" * 70)

    # Cleanup temporary files
    if os.path.exists("demo_rules.yaml"): os.remove("demo_rules.yaml")
    if os.path.exists("demo_policy.bin"): os.remove("demo_policy.bin")
