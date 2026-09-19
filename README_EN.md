# 🛡️ Deterministic Runtime OS (DROS) - VajraClaw Hacker Edition
**DROS: The Execution Governance Standard for Agentic AI**

[![License: Commercial](https://img.shields.io/badge/License-Commercial-blue.svg)](#)
[![Patent Status](https://img.shields.io/badge/U.S._Patent-64%2F111%2C973-blue.svg)](#)
[![Academic Paper](https://img.shields.io/badge/Academic_Paper-DROS--6P-purple.svg)](https://doi.org/10.5281/zenodo.21808499)
[![Specification: RFC-010](https://img.shields.io/badge/Specification-RFC--010%20Open%20Passport-darkgreen.svg)](#)

[English](README_EN.md) | [繁體中文](README_ZH.md)

---

> 🛑 **"If runtime needs intelligence, the system is already broken."**
>
> Prompt Engineering is dead when it comes to enterprise security. No matter how complex your System Prompt is, Jailbreaks and Prompt Injections will find a way through.
> **DROS is NOT a prompt wrapper. It is the Execution Governance Standard.** We move intelligence to compile-time and enforce deterministic rules via an $O(1)$ microsecond binary kernel.

---

> 💡 **For the latest pricing and tiers, please refer to the [Official Website (dr-os.io)](https://dr-os.io).**

| Feature / 6-Pillar Dimension | 🟢 Hacker / Community (Non-Commercial) | 🔵 Startup | 🟣 Enterprise | 👑 Sovereign |
| :--- | :---: | :---: | :---: | :---: |
| **Target Audience** | **Individual Devs / Local Multi-Agent (Non-Commercial)** | 10~50 Dev Startup Teams | Enterprises / Listed Co. | Banking / Defense / Gov |
| **Machine UUID Limit** | **1 UUID** | 3 UUIDs | 15 UUIDs | **Unlimited** |
| **Concurrent Agents** | **5 Concurrent Agents** | 30 Agents | 450 Agents | **Unlimited (Swarm)** |
| **Pillar 1: Principal (W3C DID)** | ✅ **Native W3C `did:key`** | ✅ **3-Tier PKI DIT** | ✅ **Cross-Domain BEC Issuance** | ✅ Hardware Dongle |
| **Pillar 2: Authorization (Deterministic)**| ✅ **AST Bitmap Matching** | ✅ **Zero-Heap Bitmaps** | ✅ **Custom Capability Vector**| ✅ Multi-Dim Bitmap Matrix |
| **Pillar 3: Tool Bound (Syscall Gate)** | ✅ **C-ABI / HTTP Fuse (<1μs)**| ✅ **26.1μs In-Band Fuse** | ✅ **Sub-500ns Thread Panic**| ✅ Hardware Physical Fusing |
| **Pillar 4: Policy Gate (Dynamic Control)**| ❌ Static Rules Only | ✅ **Dynamic PII Masking** | ✅ **HITL Multi-Sig + ZKP** | ✅ Military Gate Matrix |
| **Pillar 5: Audit Log (Non-Repudiation)** | ✅ **Ed25519 Signed JSON** | ✅ **Ed25519 Signatures**| ✅ **SHA-256 Merkle Tree** | ✅ Forensic Compliance Audit Lineage |
| **Pillar 6: Expiry/Revocation (<1μs)** | ❌ Gateway Restart | 🟡 15-min BEC Expiry | ✅ **<1μs RCU Pointer Swap** | ✅ Distributed Mesh Revoke |
| **RFC-010 Open Passport Standard** | ✅ **Full Local Issuance** | ✅ **Multi-Role DIT Sign** | ✅ **GuardVM Validation** | ✅ 3-Tier Sign Chain |
| **Add-On Compliance Packages** | ❌ Not Eligible | 💡 **Eligible for Add-Ons** | ⭐ **Eligible for Add-Ons** | ✅ Fully Included |
| **Deployment Target** | **Local PC / Docker Gateway** | **VM / NAS Docker** | K8s / GKE / Cluster | Air-Gapped / FPGA |

---

## 🧩 Agent Engineering & Governance Patterns (DROS AP Series)

> Tired of autonomous AI agents producing monolithic slop, fake mocks (`return True` / `pass`), or running destructive shell mutations behind your back?  
> VajraClaw Hacker Edition ships natively with **DROS Application Governance Patterns and Zero-Dependency Verification Tooling**:

| Pattern ID | Problem & Title | Governance Invariant | Included Tool |
| :--- | :--- | :--- | :--- |
| **[AP-001](docs/application-patterns/AP-001-task-modularization.md)** | **Task Modularization via Governance Boundaries**<br>Code size is the wrong metric; use GBAI to prevent over-engineering and privilege mixing. | `GBAI` | `tools/dros_verify.py` |
| **[AP-002](docs/application-patterns/AP-002-anti-stub-artifacts.md)** | **Anti-Stub & Sham Implementation Detection**<br>Catching AI minimal-effort evasions (`pass`, empty stubs, `assert True`) before execution. | `5-Stage Capability Lifecycle` | `tools/dros_verify.py` |

👉 **[Explore Full Pattern Catalog (AP-001 ~ AP-008) →](docs/application-patterns/README.md)**

```bash
# Verify your agent scripts in 0.1s locally
python tools/dros_verify.py my_agent_script.py
```

---

## 🚀 Multi-Scenario Deployment & Setup Guide

### 🌟 Scenario A: DSH (DeepSeek Harness) Sandbox Users
1. **Start the DROS Docker Gateway**:
   ```bash
   docker run -d -p 8080:8080 --name dros-gateway dros/hacker-gateway:v1.0.0
   ```
2. **Install DROS Community Plugin in DSH**:
   ```bash
   dsh plugin --profile web add dsh-plugin-dros
   ```
3. **Enjoy Zero-Friction Protection**: DSH Agents are immediately bound to microsecond $O(1)$ tool interception.

---

### 💻 Scenario B: Antigravity 2.0 / Claude Desktop / Cursor Developers (WebMCP Protocol & Local Execution Governance)

DROS Hacker Edition natively includes the **WebMCP / MCP (Model Context Protocol) Execution Governance Layer**. You can choose between "Zero-Dependency Native Stdio Proxy Gate" and "Docker HTTP Gateway":

#### Method 1: Zero-Dependency Native Stdio Gate (Recommended for Individual Devs)
No Docker required. Initialize `dros.personal.config.json` directly in your workspace to enforce DWGR-8 execution boundaries (blocking directory traversal, destructive SQL injection, spending limits):
1. **Initialize local governance configuration**:
   ```bash
   npx @dros/personal init
   # Or copy the included template: dros.personal.config.json
   ```
2. **Mount in Claude Desktop (`claude_desktop_config.json`) or Cursor / Antigravity**:
   ```json
   {
     "mcpServers": {
       "filesystem-governed": {
         "command": "npx",
         "args": ["-y", "@dros/personal", "gate", "--tool", "filesystem", "--", "@modelcontextprotocol/server-filesystem", "E:\\projects"]
       }
     }
   }
   ```
3. **Tamper-Evident Local Audit Chain**: All permitted and blocked tool calls are automatically hashed into a DWGR-8 R6-compliant SHA-256 linear chain.

#### Method 2: Containerized Mode (Docker HTTP Gateway)
Add the DROS Gateway to your `mcp_settings.json` / Claude Config:
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

---

### 🐍 Scenario C: Native Python / LangChain / AutoGen Developers
```python
from integrations.vajraclaw.runtime import VajraClaw

vc = VajraClaw("demo_policy.yaml")
decision = vc.evaluate("execute_payment", {"amount": 500})
if not decision:
    raise PermissionError(f"Blocked by DROS: {decision.reason}")
```

---

## 📜 Technical Whitepapers & Academic DOI Citations

The DROS deterministic runtime governance architecture is grounded in rigorous scientific epistemology. The complete series of technical papers has achieved permanent, immutable DOI registration via Zenodo:

### 🧭 Master Research Overview & Falsification Manifesto
*   **《A Synoptic Guide to the DROS Program: Problem Formulation, Theoretical Architecture, and Falsification Criteria》**
    *   *Zenodo Reading Guide v2 (Comprehensive Overview)*
    *   **Zenodo DOI**: [`10.5281/zenodo.22255275`](https://doi.org/10.5281/zenodo.22255275) | **Record**: [zenodo.org/records/22255275](https://zenodo.org/records/22255275)

---

### 🏹 The 5-Paper Technical Program

1. 🏛️ **Paper 1: DROS-6P (Governance Specification Layer ── Enterprise AI Trust Boundaries)**
   * *DROS-6P: A Unified Deterministic Runtime Governance Architecture Closing the Six Fundamental Trust Boundaries of Enterprise AI Agents*
   * **Zenodo DOI**: [`10.5281/zenodo.21833970`](https://doi.org/10.5281/zenodo.21833970) | **Record**: [zenodo.org/records/21833970](https://zenodo.org/records/21833970)

2. 🛡️ **Paper 2: DROS 4-Layer (Implementation Layer ── Defense-in-Depth Governance)**
   * *DROS 4-Layer Defense-in-Depth Architecture for Autonomous AI Workloads*
   * **Zenodo DOI**: [`10.5281/zenodo.22092008`](https://doi.org/10.5281/zenodo.22092008) | **Record**: [zenodo.org/records/22092008](https://zenodo.org/records/22092008)

3. ⚙️ **Paper 3: DROS-PGM (Kernel Control Layer ── Physical Guard Module & Non-Repudiable Attribution)**
   * *Runtime Attribution Framework: An External C-ABI and PKI-Based Zero-Trust Infrastructure for Non-Repudiable Execution Governance in Multi-Agent Systems*
   * **Zenodo DOI**: [`10.5281/zenodo.21903687`](https://doi.org/10.5281/zenodo.21903687) | **Record**: [zenodo.org/records/21903687](https://zenodo.org/records/21903687)

4. 📱 **Paper 4: Post-Compromise Mobile (Digital System Empirical Validation ── Submitted to IEEE TMC)**
   * *Post-Compromise Security for Autonomous Mobile Agents: A Deterministic Runtime Attenuation and Proof-Carrying Authorization Architecture*
   * **Zenodo DOI**: [`10.5281/zenodo.22253147`](https://doi.org/10.5281/zenodo.22253147) | **Record**: [zenodo.org/records/22253147](https://zenodo.org/records/22253147)

5. 🛸 **Paper 5: Post-Compromise Physical AI / UAV (Cyber-Physical Empirical Validation ── Submitted to IEEE TAES)**
   * *Post-Compromise Security for Physical AI: Deterministic Runtime Enforcement of Physical Action Authority in Autonomous UAVs*
   * **Zenodo DOI**: [`10.5281/zenodo.22254372`](https://doi.org/10.5281/zenodo.22254372) | **Record**: [zenodo.org/records/22254372](https://zenodo.org/records/22254372)

---
*Open Evaluation & Falsification Sandbox: [DROS-VEP Lite (GitHub)](https://github.com/Top-Celestial-Company-Ltd/dros-vep-lite) ── Reproduce RFC-001 Threat Models and 4-Phase Lifecycle Tests.*

---

## 🧪 Empirical Test Suite & Community Verification Directory

To enable open-source developers and security researchers to independently verify Hacker Edition defensive invariants, this section details the standardized benchmark testbed, 5-framework integration test procedures, high-risk containment vectors, and architectural boundaries:

### 1. Testbed Specifications
* **Host Operating System**: Ubuntu Linux 22.04 LTS (Kernel `5.15.0-190-generic` x86_64) / Windows 11 Enterprise
* **CPU Hardware**: Intel Xeon E3-1265L v3 @ 2.50GHz / Core i7-12700
* **Container Runtime**: Docker Engine 26.1.0 / Docker Compose v2.27.0
* **Toolchain & Compilers**: GCC 11.4.0 (`-O2`), Rust 1.78.0 (`opt-level=3, lto=true`, exporting `dros_core_rs.dll` / `.so`)
* **Verification Harness**: `dros_test_pipeline.py`, `tools/stress_test.py`

### 2. Latency Measurement Methodology
* **Measurement Pathway**: Client issues HTTP/MCP Tool-Call $\to$ Docker Gateway receives request $\to$ In-Memory Bitmask lookup $\to$ Returns decision JSON frame (Full Round-Trip Time).
* **Statistical Confidence**: Continuous 24-hour soak test ($N = 160,611$ requests), **P50 = 26.21μs**, **P95 = 31.05μs**, **P99 = 34.80μs**, maximum jitter $< 85\mu\text{s}$.

### 3. End-to-End Test Matrix Across 5 Major Agent Ecosystems

| Agent Framework | Integration Protocol / Mode | Test Vector & Payload | Verification Result & Status |
| :--- | :--- | :--- | :--- |
| **Anthropic Claude Code / Desktop** | MCP (Model Context Protocol) | High-risk tool invocation intercepted | **PASS** (`MCP Error 403: Capability Denied`) |
| **Cursor IDE / VS Code Agent** | Terminal Evaluation Hook | Agent attempts `rm -rf /` | **PASS** (`Exit 1: Blocked by Vajra Policy`) |
| **OpenAI SDK / LangChain** | 3-Line Python Wrapper | Transaction amount exceeds $1,000 threshold | **PASS** (`PermissionError: Threshold Exceeded`) |
| **CrewAI / AutoGen** | Multi-Agent W3C DID Delegation | Unauthorized principal attempts `.env` read | **PASS** (`HTTP 403: Role Invariant Broken`) |
| **DeepSeek Harness (DSH)** | Native Plugin (`dsh-dros-vajraclaw`) | High-concurrency toolchains & compliance audit | **PASS** (`All Invariants Passed, Zero Leak`) |

### 4. High-Risk Containment Test Cases

| Case ID | Compromised Agent Action / Payload | DROS Enforcement Action | Empirical Result & Audit Log |
| :--- | :--- | :--- | :--- |
| **HC-01** | `rm -rf /` or `rmdir /s /q C:\` | Static Pattern Failsafe | **PASS**: Blocked, logged as `[DENY_WIPE_COMMAND]` |
| **HC-02** | `cat .env` or reading `id_rsa` / secret keys | Path Boundary Failsafe | **PASS**: Blocked, logged as `[DENY_SECRET_PATH_ACCESS]` |
| **HC-03** | `execute_payment({"amount": 5000})` | Value Threshold Failsafe | **PASS**: Blocked, logged as `[DENY_THRESHOLD_EXCEEDED]` |
| **HC-04** | Any tool not declared in `demo_policy.yaml` | Default Fail-Closed Policy | **PASS**: Blocked, logged as `[DENY_NOT_WHITELISTED]` |

### 5. Honest Architectural Boundaries
* **Hacker Edition Scope**: Focused exclusively on **Protocol Gateway Governance (MCP / REST Ingress/Egress)**, offering zero-overhead compatibility with standard agent frameworks.
* **Out-of-Scope Notice**: In-process direct memory mutations or local libc invocations bypassing network protocols are out-of-scope for the Hacker gateway. For Linux kernel-level Seccomp-BPF / Raw Syscall physical enforcement and K8s high availability, refer to **Enterprise Edition**.

---

## 🏛️ Official Organization & Contact Information
* **Company**: Top-Celestial Company Ltd. (康宸園有限公司)
* **Official Website**: [https://dr-os.io](https://dr-os.io)
* **Customer Support & Inquiries**: [service@dr-os.io](mailto:service@dr-os.io)
* **GitHub Organization**: [https://github.com/Top-Celestial-Company-Ltd](https://github.com/Top-Celestial-Company-Ltd)

---

## ⚖️ Licensing & Compliance

*   **Micro-Kernel Engine**: Licensed under Commercial & Patent Protections.
*   **Patent Notice**: Protected under **U.S. Provisional Patent Application No. 64/111,973 (Patent Pending)**.
*   **Academic Citation**: Based on IEEE Paper *DROS-6P* and RFC-010 Open Agent Passport Standard.

---
*DROS Commercial Strategy Committee ── Tiered Pricing, Flywheel Locked, Add-On Value Premium.* 💎🛡️⚙️
