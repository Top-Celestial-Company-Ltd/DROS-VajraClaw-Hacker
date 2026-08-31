# ⚡ VajraClaw Python SDK (Official)

In-band deterministic runtime security guardrail for OpenAI, LangChain, CrewAI, AutoGen, and custom Python AI Agents.

## Installation
```bash
pip install vajraclaw
```

## 3-Line Quickstart
```python
from vajraclaw import VajraGuard

guard = VajraGuard(gateway_url="http://localhost:8080")
decision = guard.evaluate("execute_payment", {"amount": 500})
if not decision.allowed:
    raise PermissionError(f"Blocked by DROS: {decision.reason}")
```
