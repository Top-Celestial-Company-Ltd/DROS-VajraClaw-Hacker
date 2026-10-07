---
name: dros-execution-governance
description: Guide the agent to evaluate tool calls against DROS VajraClaw declarative policy boundaries and inspect audit trails before executing privileged actions.
---

# DROS Execution Governance Skill

This skill defines the operational workflow for interacting with the DROS VajraClaw MCP Gateway.

> **CRITICAL ARCHITECTURAL BOUNDARY:**
> This skill is a **workflow guidance layer**, NOT an enforcement layer.
> Physical security boundaries and Fail-Closed enforcement are executed exclusively by the **DROS VajraClaw Gateway & DWGR-8 Engine** through the MCP layer.

---

## 1. When to Use `dros_evaluate`

Before invoking any privileged tool that interacts with:
1. **Filesystem** (e.g. reading, writing, modifying files)
2. **Databases / Data stores** (e.g. SQL queries, table drops)
3. **Shell / OS command execution** (e.g. bash scripts, terminal commands)
4. **Network / External services**

The agent MUST first invoke the `dros_evaluate` MCP tool:
```json
{
  "agent_id": "<your-unique-agent-identifier>",
  "tool": "<target-tool-identifier>",
  "payload": {
    "action": "<action-name>",
    "<param_key>": "<param_value>"
  }
}
```

---

## 2. Interpreting Evaluation Results

* **If `decision == "ALLOW"`**:
  - The parameter boundary checks and policy rules have been satisfied.
  - A lease ID is issued (`lease_id`).
  - Proceed with the execution of the governed tool.
* **If `decision == "BLOCK"`**:
  - **STOP IMMEDIATELY.**
  - Do NOT attempt to retry the action with obfuscated arguments.
  - Do NOT attempt to circumvent the gateway via another unapproved tool.
  - Inform the user of the policy violation and the reasons specified in `violations`.

---

## 3. When to Check `dros_status`

* At agent initialization or when troubleshooting gateway communication.
* Verify that `gateway_state == "HEALTHY"` and review `policy_mode`.

---

## 4. When to Query `dros_audit`

* When the user requests proof of execution history or security audit lineage.
* `dros_audit` is strictly **READ-ONLY**. It provides tamper-evident SHA-256 hash chains demonstrating all allowed and blocked decisions.
