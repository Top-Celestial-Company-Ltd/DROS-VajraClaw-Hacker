# 🔰 DROS VajraClaw Zero-to-Hero Quickstart Guide (English Version)

> **“Linux defines how machines run software; DROS defines how AI Agents are permitted to act.”**  
> Welcome to the world of deterministic execution security with DROS™! This guide is specially designed for **first-time developers**, walking you through installation, policy configuration, and multi-agent ecosystem integration in **under 5 minutes**!

---

## ⚡ Table of Contents
1. 💡 [Why Do You Need DROS? (Core Mechanism in 30 Seconds)](#1--why-do-you-need-dros)
2. 🚀 [5-Minute Quickstart (Two Setup Options)](#2--5-minute-quickstart)
3. 📝 [Step-by-Step: Writing Your First Policy (`Vajra.md`)](#3--step-by-step-writing-your-first-policy-vajramd)
4. 🤖 [Cheat Sheet: Let AI Generate Your Policy in 1 Second](#4--cheat-sheet-let-ai-generate-your-policy-in-1-second)
5. 🔒 [Crucial Security Warning: Lock Policies to Read-Only](#5--crucial-security-warning-lock-policies-to-read-only)
6. 🔌 [One-Click Integration for Your Agents (Claude / Cursor / OpenAI / DSH)](#6--one-click-integration-for-your-agents)
7. ❓ [Beginner FAQ & Troubleshooting](#7--beginner-faq--troubleshooting)

---

## 1. 💡 Why Do You Need DROS?

When you allow autonomous AI Agents (such as Claude Code, Cursor, OpenAI Codex, CrewAI, AutoGen) to run shell commands or modify local files, traditional prompt guards and secondary LLM reviewers suffer from fatal flaws:
* 🔴 **High Latency**: Calling a secondary LLM for every single tool invocation introduces a 1~3 second bottleneck.
* 🔴 **Vulnerable to Injections**: Attackers can easily bypass text filters using Base64, Unicode, or Jailbreak prompts, instructing agents to run `rm -rf /` or exfiltrate `.env` secrets.

### 🛡️ DROS's Deterministic Approach:
DROS replaces probabilistic prompt filters with compile-time $\mathcal{O}(1)$ memory bitmaps. When an agent attempts an unauthorized system call, DROS executes **a physical in-band hard fuse in <1 microsecond (<1µs)** before the OS ever sees the command!

---

## 2. 🚀 5-Minute Quickstart

We provide two setup options. DROS Hacker Edition is **100% permanently free for individuals with no license key required**:

### 🌟 Option A: One-Command Clone & Start (Recommended / Zero External Deps)
The most resilient setup. Builds your local Docker container automatically without relying on external registries:
```bash
# 1. Clone the repository
git clone https://github.com/Top-Celestial-Company-Ltd/DROS-VajraClaw-Hacker.git
cd DROS-VajraClaw-Hacker

# 2. Start the Docker Gateway
docker compose -f docker/docker-compose.yml up -d

# 3. Verify health status (Returns 200 OK when ready)
curl http://localhost:8080/health
```

### 🐳 Option B: Run via GitHub Container Registry (GHCR)
Run instantly by pulling our pre-built official image:
```bash
# Launch container with local policy mount
docker run -d -p 8080:8080 --name dros-gateway \
  -v $(pwd)/demo_policy.yaml:/app/demo_policy.yaml:ro \
  ghcr.io/top-celestial-company-ltd/dros-vajraclaw-hacker:latest
```

---

## 3. 📝 Step-by-Step: Writing Your First Policy (`Vajra.md`)

DROS supports plain human-readable **Markdown (`Vajra.md`)** as well as structured **YAML (`demo_policy.yaml`)**.
Create `Vajra.md` in your project root to declare allowed capabilities and hard security boundaries:

```markdown
# 🛡️ DROS Agent Security Policy (Vajra.md)

## 1. Allowed Capabilities (Whitelist)
- Allow reading workspace code and documentation (`file_read`)
- Allow web search and general database read queries (`search_web`, `query_db`)
- Allow safe read-only terminal commands (`git status`, `npm test`, `cargo check`)

## 2. Strict Fail-Closed Boundaries
- Block all recursive deletion and disk wiping commands (`rm -rf`, `rmdir /s`, `format`)
- Block access to sensitive configuration and secret keys (`.env`, `id_rsa`, `secrets.json`, `.aws/credentials`)
- Restrict transaction or transfer amounts exceeding $1,000 threshold (`amount <= 1000`)
```

---

## 4. 🤖 Cheat Sheet: Let AI Generate Your Policy in 1 Second

You don't need to write rules manually! Copy and paste this **Universal Prompt** into ChatGPT, Claude, or Cursor:

> 📋 **Copy this Prompt to any AI Assistant:**
> 
> ```text
> You are a DROS deterministic security architecture expert. Based on my Agent requirements, generate a standard DROS "Vajra.md" security policy in Markdown.
> 
> Agent Details:
> - Agent Role & Scenario: [e.g., Fullstack Developer / Customer Service / Financial Assistant]
> - Allowed Tools & Operations: [e.g., Read/Write src/ directory, Run npm test, Query order database]
> - Strict Boundaries & Denials: [e.g., Block deleting root directory, Block reading .env, Payment limit $500]
> 
> Follow the DROS "Default Fail-Closed" whitelist principle and structure the output into:
> 1. Role & Capability Scope
> 2. Allowed Capabilities (Whitelist)
> 3. Security Boundary Constraints (Thresholds & Pattern Failsafes)
> ```

---

## 5. 🔒 Crucial Security Warning: Lock Policies to Read-Only

> [!CAUTION]
> **🚨 Why Must You Lock `Vajra.md` to Read-Only?**  
> Under extreme prompt injection attacks or hallucination loops, an agent might attempt to "edit its own policy file" to grant itself unrestricted permissions.
> To achieve 100% physical defense, **always lock `Vajra.md` as read-only once configured**:
> 
> * **Linux / macOS**:
>   ```bash
>   chmod 444 Vajra.md
>   ```
> * **Windows (PowerShell)**:
>   ```powershell
>   Set-ItemProperty -Path Vajra.md -Name IsReadOnly -Value $true
>   ```
> * **Docker Mounts**:
>   Always append the `:ro` flag: `-v $(pwd)/Vajra.md:/app/demo_policy.yaml:ro`

---

## 6. 🔌 One-Click Integration for Your Agents

### 🤖 A. Anthropic Claude Desktop & Claude Code
Open your `claude_desktop_config.json` and add the built-in DROS `/mcp` endpoint:
```json
{
  "mcpServers": {
    "dros-vajraclaw": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### 💻 B. Cursor IDE / VS Code
Place `.cursorrules` in your project root to intercept high-risk terminal commands before execution:
```text
Before executing any destructive shell command or modifying root files, evaluate action against DROS gateway at http://localhost:8080/evaluate
```

### 🐍 C. Python / LangChain / CrewAI / OpenAI SDK
Protect any Python tool execution in just 3 lines:
```python
from integrations.vajraclaw.runtime import VajraGuard

guard = VajraGuard(gateway_url="http://localhost:8080")
decision = guard.evaluate("delete_database", {"target": "production"})

if not decision:
    print(f"🛑 Intercepted by DROS! Reason: {decision.reason}")
```

---

## 7. ❓ Beginner FAQ & Troubleshooting

* **Q1: Do I need to restart Docker after modifying `Vajra.md`?**  
  👉 **No restart needed!** DROS supports instantaneous hot reloading; policy updates take effect in **<1 microsecond**.
* **Q2: What if I forget to add a dangerous command to the blacklist?**  
  👉 **Zero risk!** DROS operates under a strict "Default Fail-Closed" whitelist model. Any action not explicitly declared as `ALLOW` is automatically blocked.
* **Q3: Where can I read about the mathematical proofs and architecture?**  
  👉 Please visit our official website [dr-os.io](https://dr-os.io) and read our peer-reviewed research trilogy indexed on CERN Zenodo (covering DROS-6P and 4-Layer Defense-in-Depth).

---
*The DROS Team wishes you a safe and fearless journey in autonomous AI development!* 🛡️⚡💎
