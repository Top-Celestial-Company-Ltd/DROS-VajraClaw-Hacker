# ⚡ DROS™ VajraClaw (Hacker Edition)
### Free Standalone Docker Governance Gateway for Individual Multi-Agent Workstations (W3C DID & <1μs Enforcement)

[![Official Website](https://img.shields.io/badge/Official_Website-dr--os.io-purple.svg?style=for-the-badge)](https://dr-os.io)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue.svg)](#)
[![License: Free for Individuals](https://img.shields.io/badge/License-Free_for_Individuals-green.svg)](#)
[![U.S. Patent Pending](https://img.shields.io/badge/U.S._Patent-64%2F111%2C973-blue.svg)](#)
[![RFC-010 Standard](https://img.shields.io/badge/Standard-RFC--010_Draft-orange.svg)](#)

[English](README.md) | [繁體中文說明](README_zh.md) | [🌐 Official Website](https://dr-os.io)

**DROS VajraClaw Hacker Edition** is the official standalone, free Docker governance gateway designed for individual developers, AI researchers, and local developer workstations. It physicalizes execution security between autonomous AI Agents (Google Antigravity, OpenAI Codex, Claude Code, Cursor, DeepSeek Harness) and your local operating system.

---

## 🛑 Why Deterministic Execution Governance?
Probabilistic security relying on Prompt Engineering, Llama-Guard, or LLM-as-a-judge inevitably fails at runtime:
* **Prompt Injections & Jailbreaks Bypass Text Guards**: Attackers easily obfuscate prompts to trick agents into running `rm -rf /` or leaking `.env` secrets.
* **Unpredictable Latency & TOCTOU**: Calling secondary models adds 1~3s delays and fails to protect OS syscalls.
* **Lack of Auditability**: You cannot mathematically prove *why* an LLM wrapper allowed an action.

**DROS is NOT a prompt wrapper; it is a Deterministic Runtime OS**:
It moves intelligence to compile-time (`demo_policy.yaml` / `Vajra.md`) and enforces rules at runtime via constant-time $\mathcal{O}(1)$ memory bitmaps with instant physical fusing (**Strict Fail-Closed**)!

---

## 🌟 Hacker Edition Key Features (100% Free Forever for Individuals)

* 🛡️ **Protect Up to 5 Concurrent Agents**: Simultaneously govern multiple active agents across different IDEs on a single host.
* 🔑 **Native W3C `did:key` & RFC-010 Passports**: Cryptographic agent identity binding with Ed25519 signatures.
* ⚡ **Microsecond In-Band Fusing (<1μs)**: Deterministic $\mathcal{O}(1)$ AST policy lookup that severs unauthorized syscalls before execution.
* 📜 **SHA-256 Merkle Hash-Linked Audit Chain**: Non-repudiable local execution logs with startup recovery to prevent log tampering.
* 🌐 **Universal Agent Compatibility**: Native REST and MCP endpoints compatible with AGY, Codex, Claude Code, Cursor, and DSH.

---

## 📊 Governance & Defense Capability Matrix

| Threat Vector / Capability | Traditional LLM Guardrails | 📦 DSH Standalone TS Plugin | ⚡ DROS Hacker Docker Gateway (This Repo) | 🏢 Enterprise / Mesh Tier |
| :--- | :---: | :---: | :---: | :---: |
| **Runtime Vehicle** | Cloud API / External Model | In-Process JS (Zero Deps) | **Local Docker Container (`:8080`)** | Enterprise Cluster / K8s / C-ABI |
| **Protected Scope** | Single Chat Session | DSH Local Process | **Cross-Platform (AGY+Codex+Claude+Cursor+DSH)** | Multi-Node Fleet / Private Cloud |
| **Destructive Command Blocking** | ❌ Vulnerable | 🟢 **100% Regex Failsafe** | 🟢 **100% Deterministic AST Fusing (<1μs)** | 🟢 **AST Bitmaps + eBPF Kernel Hooks** |
| **Credential & Secret Protection** | ❌ No Physical Guard | 🟢 **Sensitive Path Block** | 🟢 **Dynamic PII Redaction + Virtual Sandboxing**| 🟢 **Hardware HSM + ZKP-Lite Proofs** |
| **Agent Identity Binding** | ❌ No Identity | 🟡 Session-level ID | 🟢 **Native W3C `did:key` (Ed25519)** | 🟢 **3-Tier PKI `DrosIdentityToken (DIT)`** |
| **Non-Repudiable Audit Chain** | ❌ Plain Text Logs | 🟢 **Local SHA-256 Hash Chain**| 🟢 **Ed25519 Signed Merkle Hash Chain** | 🟢 **EU AI Act Art. 12 Court-Grade Chain** |
| **RFC-010 Passports** | ❌ Unsupported | 🟡 Format Parser | 🟢 **Local Minting & Cross-Agent Verification**| 🟢 **Cross-Organization Roaming Passports** |
| **Decision Latency** | 🔴 1,000 ~ 3,000 ms | 🟢 **<1 ms (Direct Hook)** | 🟢 **<1 ms (Loopback HTTP / C-ABI)** | 🟢 **<500 ns (Zero-Copy Memory Lookup)** |
| **License** | Pay-per-Token | **100% Free (Apache-2.0)** | **Free License for Individuals** | Startup $2,990 / Enterprise $29,990 |

---

## 🚀 Quick Start (One-Command Setup)

### Option 1: Run via Pre-built Docker Container (Recommended)
```bash
# 1. Start DROS Hacker Gateway (No license key required out-of-the-box)
docker run -d -p 8080:8080 --name dros-gateway \
  -v $(pwd)/FreeTrial-Sandbox/demo_policy.yaml:/app/demo_policy.yaml \
  dros/hacker-gateway:v1.0.0

# 2. Verify health status
curl http://localhost:8080/health
```

### Option 2: Build & Run from Source
```bash
git clone https://github.com/Top-Celestial-Company-Ltd/DROS-VajraClaw-Hacker.git
cd DROS-VajraClaw-Hacker
docker compose -f docker/docker-compose.yml up -d
```

---

## 🔌 Connecting Your Multi-Agent Workstation

### 1. Google Antigravity 2.0 / Claude Desktop / Cursor (MCP Mode)
Add to your `mcp_settings.json`:
```json
{
  "mcpServers": {
    "dros-governance": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### 2. DeepSeek Harness (DSH)
Install the official failsafe plugin:
```bash
dsh plugin --profile web add dsh-plugin-vajraclaw
```
*(In DSH settings, set `gatewayUrl` to `http://localhost:8080` to activate W3C DID & full Docker gateway governance)*

### 3. OpenAI Codex / Claude Code / Python SDK
```bash
export DROS_GATEWAY_URL="http://localhost:8080"
export DROS_IDENTITY_SEED="0x1a2b3c4d5e6f..." # Local Ed25519 Seed Hex
```

In Python:
```python
from integrations.vajraclaw.runtime import VajraClaw

vc = VajraClaw("demo_policy.yaml")
decision = vc.evaluate("execute_payment", {"amount": 500})
if not decision:
    raise PermissionError(f"Blocked by DROS: {decision.reason}")
```

---

## 📜 Technical Foundations & Benchmark Publications

The deterministic execution governance, microsecond fusing, and cryptographic audit mechanisms in this project are referenced from and build upon the following core technical papers and verification environments:

1. **Core Architecture & Six Trust Boundaries (Core Architecture)**:
   * **Paper**: *DROS-6P: A Unified Deterministic Runtime Governance Architecture Closing the Six Fundamental Trust Boundaries of Enterprise AI Agents*
   * **Zenodo DOI**: [10.5281/zenodo.21833970](https://doi.org/10.5281/zenodo.21833970) | **Archived Record**: [zenodo.org/records/21833970](https://zenodo.org/records/21833970)

2. **Defense-in-Depth Model (4-Layer Security)**:
   * **Paper**: *DROS 4-Layer Defense-in-Depth Architecture for Autonomous AI Workloads*
   * **Zenodo DOI**: [10.5281/zenodo.21903475](https://doi.org/10.5281/zenodo.21903475) | **Archived Record**: [zenodo.org/records/21903475](https://zenodo.org/records/21903475)

3. **Runtime Attribution & C-ABI Module (Attribution Framework)**:
   * **Paper**: *Runtime Attribution Framework: An External C-ABI and PKI-Based Zero-Trust Infrastructure for Non-Repudiable Execution Governance in Multi-Agent Systems*
   * **Zenodo DOI**: [10.5281/zenodo.21903687](https://doi.org/10.5281/zenodo.21903687) | **Archived Record**: [zenodo.org/records/21903687](https://zenodo.org/records/21903687)

4. **Open Standards & Verification Sandbox**:
   * **RFC-010 Specification**: Adheres to open Agent Identity & Attestation standard (W3C DID did:key & Ed25519 signature chain).
   * **Verification Sandbox**: [DROS-VEP Lite (Reproducible Evaluation Sandbox)](https://github.com/Top-Celestial-Company-Ltd/DROS-VEP-lite)
   * **Evaluation Metrics**: 24-hour soak benchmark results (160,611 verified requests, 26.1μs decision latency).

## ⚠️ Important Notices & Operational Security

1. **Strict Fail-Closed Enforcement**:
   * By default, any capability or syscall not explicitly declared as `ALLOW` in `demo_policy.yaml` is permanently blocked.
2. **Privilege Separation**:
   * The AI Agent must **never** possess write permissions to policy files. In production, mount policy files as Read-Only.
3. **License Key Activation (Optional)**:
   * Out-of-the-box, the gateway runs in Community mode (supporting 2 concurrent agents). To unlock 5 concurrent agents, pass `-e DROS_LICENSE_KEY="your-key"` or activate via DSH settings.

---

## ⚖️ Standard 3-Tier License & Intellectual Property Constitution

* **Personal & Community Use (Free for Individuals)**:
  * Granted permanently for individual developers and researchers (Free License for Individuals) on up to 1 host and 5 concurrent agents. Source code and patent claims are proprietary. Unauthorized redistribution or reverse engineering is strictly prohibited.
* **Enterprise & Commercial Deployment**:
  * Enterprise implementation or use by corporate entities requires commercial licensing (Startup / Enterprise / Sovereign). Contact [service@dr-os.io](mailto:service@dr-os.io) or visit [https://dr-os.io](https://dr-os.io).
* **Patent Notice**:
  * DROS deterministic runtime governance and in-band interception technology is protected under U.S. Provisional Patent Application (**U.S. PPA No. 64/111,973, Patent Pending**). All commercial and enterprise rights are reserved by Top-Celestial Company Ltd.