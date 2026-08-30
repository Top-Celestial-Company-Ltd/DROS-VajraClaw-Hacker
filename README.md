# 🛡️ DROS - Execution Governance Standard for Agentic Systems

> **The missing execution layer for autonomous AI systems.**

[English](README.md) | [繁體中文](README_zh.md)

DROS (Deterministic Runtime Operating System) is an invisible, military-grade execution governance infrastructure for Agentic AI. 
It operates completely outside of the LLM reasoning space, sitting physically between the Agent's output and your enterprise operating system.

## 1. The Core Problem: Probabilistic Security Fails

Without execution control, AI Agents are a loaded gun pointed at your infrastructure. Current "security" relies on LLM-as-a-judge or JSON parsers, which fail because:
*   **Prompt Injections**: Zero-day semantic attacks bypass natural language guards.
*   **TOCTOU & Latency**: JSON parsing at runtime creates unpredictable delays and vulnerabilities.
*   **Lack of Auditability**: You cannot cryptographically prove *why* a prompt engineering wrapper allowed an action.

## 2. Developer Experience: Policy-as-Code via AI

Forget complex YAML or JSON configurations. With DROS, your CISO or Security Engineer simply writes the policy in natural language mixed with Markdown (`Vajra.md`). 
You can even use ChatGPT or Claude to generate your `Vajra.md` based on your company's security playbook. 

Once written, the **DROS Compiler** transforms this human-readable Markdown into a highly optimized, cryptographically signed `policy.bin` artifact ready for production.

## 3. The DROS Solution: Deterministic OS Layer

DROS shifts intelligence to **compile-time** and enforces rules via an **O(1) deterministic bitmap** at **runtime**.

1.  **DROS Compiler**: Write `Vajra.md` Policy-as-Code. Compile it into a cryptographically signed binary artifact (`policy.bin`).
2.  **DROS Engine**: A C-FFI / JNI embedded engine that performs pure bitwise AND operations (O(1) memory lookup) to validate execution. **No LLM evaluation. No semantic interpretation. No bypass.**

### Strict Fail-Closed Guarantee
DROS operates on a Zero-Trust basis. If an Agent attempts an unauthorized action, if the Ed25519 signature doesn't match, or if the Policy Hash is corrupted, DROS physically severs the execution path at the OS level (Panic). It will rather crash the application than let an unverified payload touch your database.

## 4. The 6-Pillars Enterprise AI Trust Model (DROS-6P)

DROS-VajraClaw enforces six fundamental trust boundaries in real time at the C-ABI / FFI in-band execution layer:

1. **Principal (Identity)**: 3-tier PKI-signed `DrosIdentityToken (DIT)` for unbypassable agent identity binding.
2. **Authorization (Deterministic)**: Immutable $O(1)$ capability bitmaps mapping roles to execution vectors.
3. **Action Bound (Syscall Gate)**: Sub-microsecond (<500ns) binary interception enforcing hard physical limits.
4. **Policy Gate (Dynamic Control)**: Dynamic data redaction, Human-In-The-Loop (HITL), and ZKP-Lite zero-knowledge proofs.
5. **Audit Log (Non-repudiability)**: SHA-256 Merkle Hash Chain + Ed25519 signatures, fully compliant with EU AI Act Art. 12.
6. **Expiry / Revocation (Microsecond)**: Constant-time $O(1)$ dynamic bitmap updates for microsecond-level revocation and instant HTTP 403 enforcement.

---

## 📜 Technical Foundations & Benchmark Publications

## 📜 Technical Foundations & Benchmark Publications
If you reference DROS zero-trust execution governance in your research or enterprise architecture, please cite the DROS Academic Trilogy on Zenodo:

* 📖 **[DROS Trilogy Reading Guide (Technical Note)](https://doi.org/10.5281/zenodo.22114036)**: *An Agent Runtime Operation Substrate* (Zenodo: [10.5281/zenodo.22114036](https://zenodo.org/records/22114036))
* 🏛️ **Paper 1: DROS-6P** — *A Unified Deterministic Runtime Governance Architecture Closing the Six Fundamental Trust Boundaries of Enterprise AI Agents* (DOI: [`10.5281/zenodo.21833970`](https://doi.org/10.5281/zenodo.21833970))
* 🏛️ **Paper 2: DROS 4-Layer (v3)** — *Bridging the Agent-to-Execution Attribution Gap in Autonomous AI Workloads: A 4-Layer Deterministic Runtime Operating System* (DOI: [`10.5281/zenodo.22092008`](https://doi.org/10.5281/zenodo.22092008))
* 🏛️ **Paper 3: DROS-PGM** — *A Deterministic Kernel-Level Execution Control Plane for Post-Compromise Security in Autonomous AI Systems* (DOI: [`10.5281/zenodo.21903687`](https://doi.org/10.5281/zenodo.21903687))

### 📖 Full Technical Whitepapers
* 📖 **[Full Whitepaper (English v2.5)](docs/DROS_AgenticWeb_Defense_Whitepaper_EN.md)**: *Zero-Trust Execution Governance for Autonomous AI Workloads (DROS 4-Layer & 6P Model)*
* 📖 **[完整技術白皮書 (繁體中文 v2.5)](docs/DROS_AgenticWeb_Defense_Whitepaper_CN.md)**: *自主型 AI 工作負載的零信任執行治理 (DROS 四層防禦縱深與 6P 模型)*
* 🏛️ **[Defensive Publication & Prior Art Declaration](docs/DEFENSIVE_PUBLICATION.md)**: *Prior Art declaration establishing DROS Compile-time & O(1) Bitmap governance*

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

### 💻 Scenario B: Antigravity 2.0 / Codex / Cursor Developers (MCP Protocol)
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

> **"Linux defined how machines run software. DROS defines how agents are allowed to act."**

*Developed by DROS Labs / 康宸園有限公司 (Top-Celestial Company Ltd.)*  
*Protected under U.S. Provisional Patent Application No. 64/111,973 (Patent Pending).*

