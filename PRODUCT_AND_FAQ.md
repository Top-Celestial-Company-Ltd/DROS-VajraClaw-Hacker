# 🛡️ DROS™ Official Product Catalog & Technical FAQ
### Enterprise Execution Governance Standard Specification for Agentic AI

[![Official Website](https://img.shields.io/badge/Official_Website-dr--os.io-purple.svg?style=for-the-badge)](https://dr-os.io)
[![U.S. Patent Pending](https://img.shields.io/badge/U.S._Patent-64%2F111%2C973-blue.svg)](#)
[![RFC-010 Standard](https://img.shields.io/badge/Standard-RFC--010_Draft-orange.svg)](#)
[![License: 3-Tier Model](https://img.shields.io/badge/License-Standard_3--Tier_Model-green.svg)](#)

[English Version (PRODUCT_AND_FAQ.md)](PRODUCT_AND_FAQ.md) | [繁體中文說明 (PRODUCT_AND_FAQ_zh.md)](PRODUCT_AND_FAQ_zh.md) | [🌐 Official Pricing & Plans (dr-os.io/pricing)](https://dr-os.io/pricing)

---

## 🛑 1. Why Deterministic Runtime Governance?
Probabilistic security relying on Prompt Engineering, Llama-Guard, or LLM-as-a-judge inevitably fails at runtime:
1. **Prompt Injections & Jailbreaks Bypass Text Guards**: Attackers easily obfuscate prompts to trick agents into running `rm -rf /` or leaking `.env` secrets.
2. **Unpredictable Latency & TOCTOU**: Calling secondary models adds 1~3s delays and fails to protect OS syscalls.
3. **Lack of Auditability**: You cannot mathematically prove *why* an LLM wrapper allowed a specific privileged execution.

**DROS is NOT a prompt wrapper; it is a Deterministic Runtime Operating System**:
It moves intelligence to compile-time (`demo_policy.yaml` / `Vajra.md`) and enforces rules at runtime via constant-time $\mathcal{O}(1)$ memory bitmaps with instant physical fusing (**Strict Fail-Closed**)!

---

## 🏛️ 2. The 6-Pillars Enterprise AI Trust Model (DROS-6P)

DROS-VajraClaw enforces six fundamental trust boundaries in real time at the C-ABI / FFI in-band execution layer:

1. **Principal (Identity)**: 3-Tier PKI-signed `DrosIdentityToken (DIT)` and native W3C `did:key` (Ed25519) for unbypassable agent identity binding.
2. **Authorization (Deterministic)**: Immutable $\mathcal{O}(1)$ capability bitmaps mapping agent roles to execution vectors.
3. **Action Bound (Syscall Gate)**: Sub-microsecond (<500ns) binary interception enforcing hard physical OS limits.
4. **Policy Gate (Dynamic Control)**: Dynamic data redaction, Human-In-The-Loop (HITL), and ZKP-Lite zero-knowledge proofs.
5. **Audit Log (Non-repudiability)**: SHA-256 Merkle Hash Chain + Ed25519 signatures, fully compliant with EU AI Act Art. 12.
6. **Expiry / Revocation (Microsecond)**: Constant-time $\mathcal{O}(1)$ dynamic bitmap updates for microsecond-level revocation and instant HTTP 403 enforcement.

---

## 🔥 3. Official Product Editions & Scope

> 💡 *For real-time pricing, seat allocation, and active subscriptions, please refer directly to [dr-os.io/pricing](https://dr-os.io/pricing).*

| Tier | License Model | Best For | Governance Scope & Deliverables |
| :--- | :--- | :--- | :--- |
| **DSH Plugin (`dsh-plugin-vajraclaw`)** | **Open Source (Apache-2.0)** | DSH IDE Users | Pure TypeScript in-process regex failsafe, local JSONL hash chain, upgradeable to Docker gateway |
| **Hacker Edition (Docker Gateway)** | **Free License for Individuals** | Individual Developers & Researchers | Up to 5 Concurrent Agents, W3C DID, <1μs AST Fusing, SHA-256 Merkle Chain |
| **Startup Edition (Commercial)** | **Commercial Annual Subscription** | AI Startups & SaaS Apps | Multi-Host Deployment, Native C-ABI SDKs (`.dll`/`.so`), Multi-Language Bindings |
| **Enterprise Audit Edition** | **Enterprise Compliance License** | FinTech, Healthcare & Enterprises | EU AI Act Art. 12 Court-Grade Audit, Hardware HSM, Air-Gapped, Dedicated SLA |
| **Sovereign Mesh / Source Buyout** | **Custom Sovereign License** | Defense & Sovereign Infrastructure | Full Source Code Buyout (C-ABI/Go/Rust), Centralized IAM Control Plane, K8s Helm Clusters |

---

## ❓ 4. Technical & Security FAQ (Frequently Asked Questions)

### Q1: What if an attacker tries to replace/overwrite the DROS microkernel binary (.dll / .so)?
**A: DROS cannot be bypassed or compromised through binary tampering.** The architecture enforces a four-layer invariant defense:
1. **File Overwrites Are Regulated Syscalls**: To overwrite a binary, an agent must execute `cp`, `mv`, `curl`, or file-write syscalls. These actions are evaluated and blocked in-band by DROS before reaching the OS.
2. **Strict Default Fail-Closed (Whitelist Model)**: Any action not explicitly declared as `ALLOW` is denied by default. Security does not rely on human diligence in maintaining blacklists.
3. **Kernel Hard Invariants**: The DROS compiler hardcodes immutable rejection rules protecting core binaries and cryptographic identity seeds, preventing override even under permissive admin policies.
4. **OS File Locking & Ed25519 Signature Verification**: Running binaries are locked by the OS kernel (`FILE_SHARE_READ` on Windows, `ETXTBUSY` on Linux). Host processes verify Ed25519 digital signatures at load time, terminating immediately (Panic) upon tampering.

### Q2: What if an admin forgets to add certain dangerous commands to the blacklist?
**A: Zero risk.** DROS operates exclusively on a zero-trust whitelist (Default Fail-Closed). Admins only specify what is allowed. Any undeclared or unrecognized capability is compiled to bit `0` (Deny) and severed instantaneously at runtime.

### Q3: What is the fundamental difference between the pure TS plugin and the Docker Gateway?
**A:**
* **Pure TS Plugin**: Zero-dependency lightweight in-process guardrail for local DSH users against basic command injection and file deletion.
* **Docker Gateway**: Complete enterprise-grade substrate featuring W3C `did:key` identity tokens, <1μs AST memory fusing, SHA-256 Merkle court-grade audit logs, and unified multi-agent governance across AGY, Claude, Codex, Cursor, and DSH simultaneously.

---


### Q4: How do I configure `Vajra.md` policies, and how does Personal Edition compare to Enterprise Edition in defense architecture?
**A:**
* **Simple Configuration**: Individual developers can define allowed capabilities and boundary rules using plain Markdown (`Vajra.md`) or YAML, or use our universal AI Prompt to generate compliant rules in 1 second via ChatGPT, Claude, or Cursor.
* **Personal / Hacker Edition Defense (Local Sandbox)**:
  - **Mechanisms**: Enforces local OS file-level read-only locks (`chmod 444`, `Set-ItemProperty IsReadOnly`, Docker `:ro`) combined with DROS in-band sub-microsecond Syscall interception to stop hallucinating agents from self-modifying policies to escalate privileges.
* **Enterprise Edition Defense (Cluster Defense-in-Depth)**:
  - **Remote Vault / KMS Storage**: Policies are centralized in an external, isolated configuration plane; local agents physically cannot view or access the policy storage.
  - **Multi-Signature Governance (Multi-Sig M-of-N)**: Boundary relaxations require cryptographic approvals from SecOps and compliance officers.
  - **K8s RBAC & eBPF Kernel Isolation**: Namespace-level isolation prevents host penetration even if the agent compromises Pod root privileges.
  - **Hardware HSM Key Isolation & WORM Storage**: W3C DID private keys never leave physical hardware chips, and audit trails are synced to Write-Once-Read-Many (WORM) court-grade legal storage.

---

## 📜 5. Technical Foundations & Academic Benchmark Publications

The deterministic execution governance, microsecond fusing, and cryptographic audit mechanisms in this project are referenced from and build upon the following core technical papers and verification environments:

1. **Core Architecture & Six Trust Boundaries (Core Architecture)**:
   * **Paper**: *DROS-6P: A Unified Deterministic Runtime Governance Architecture Closing the Six Fundamental Trust Boundaries of Enterprise AI Agents*
   * **Zenodo DOI**: [`10.5281/zenodo.21833970`](https://doi.org/10.5281/zenodo.21833970) | **Archived Record**: [zenodo.org/records/21833970](https://zenodo.org/records/21833970)

2. **Defense-in-Depth Model (4-Layer Security)**:
   * **Paper**: *DROS 4-Layer Defense-in-Depth Architecture for Autonomous AI Workloads*
   * **Zenodo DOI**: [`10.5281/zenodo.21903475`](https://doi.org/10.5281/zenodo.21903475) | **Archived Record**: [zenodo.org/records/21903475](https://zenodo.org/records/21903475)

3. **Runtime Attribution & C-ABI Module (Attribution Framework)**:
   * **Paper**: *Runtime Attribution Framework: An External C-ABI and PKI-Based Zero-Trust Infrastructure for Non-Repudiable Execution Governance in Multi-Agent Systems*
   * **Zenodo DOI**: [`10.5281/zenodo.21903687`](https://doi.org/10.5281/zenodo.21903687) | **Archived Record**: [zenodo.org/records/21903687](https://zenodo.org/records/21903687)

4. **Open Standards & Verification Sandbox**:
   * **RFC-010 Specification**: Adheres to open Agent Identity & Attestation standard (W3C DID `did:key` & Ed25519 signature chain).
   * **Verification Sandbox**: [DROS-VEP Lite (Reproducible Evaluation Sandbox)](https://github.com/Top-Celestial-Company-Ltd/DROS-VEP-lite)
   * **Evaluation Metrics**: 24-hour soak benchmark results (160,611 verified requests, 26.1μs decision latency).

---

## ⚖️ 6. Standard 3-Tier License & Patent Constitution

1. **Core Enforcement Substrate ➔ Patent Protected (Patent Pending)**:
   * DROS deterministic runtime governance and in-band interception technology is protected under U.S. Provisional Patent Application (**U.S. PPA No. 64/111,973, Patent Pending**). All commercial and enterprise rights reserved by Top-Celestial Company Ltd.
2. **Community Client & Docker Gateway ➔ Free for Individuals**:
   * Granted permanently for individual developers and researchers (Free License for Individuals) for up to 5 concurrent agents. Source code and proprietary claims are strictly reserved.
3. **Benchmark Testbed ➔ Open Source Evaluation (Apache 2.0)**:
   * Open evaluation harness for academic reproducibility and falsification.

---
**Developed by DROS Labs / 康宸園有限公司 (Top-Celestial Company Ltd.)**  
*Official Portal: [https://dr-os.io](https://dr-os.io) | Contact: [service@dr-os.io](mailto:service@dr-os.io)*
