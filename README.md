# 🛡️ Deterministic Runtime OS (DROS) - VajraClaw Hacker Edition
**The Deterministic In-Band Execution Governance Gateway for Autonomous Agentic AI**

[![License: Source-Available](https://img.shields.io/badge/License-Source--Available%20(Non--Commercial)-blue.svg)](#-licensing--intellectual-property)
[![Patent Status](https://img.shields.io/badge/U.S._Patent_Pending-64%2F111%2C973-blue.svg)](#-licensing--intellectual-property)
[![Official Website](https://img.shields.io/badge/Official_Website-dr--os.io-purple.svg)](https://dr-os.io)
[![Technical Reports](https://img.shields.io/badge/Open_Archive-Zenodo_Preprints-purple.svg)](https://doi.org/10.5281/zenodo.21808499)

📖 **Documentation / 語言選擇**: [English (Default)](README.md) | [繁體中文文檔 (Traditional Chinese)](README_ZH.md)

---

> 🛑 **"If runtime security depends on model intelligence, the system is already broken."**
>
> Prompt engineering and guardrails fail under adaptive adversarial jailbreaks. 
> **DROS is NOT a prompt wrapper. It is an In-Band Execution Governance Gateway.** 
> By moving verification to compile-time capabilities, DROS enforces deterministic policy gates at runtime:
> * **In-Process C-ABI / Rust Core**: **$< 3\ \mu\text{s}$** deterministic capability bitmap evaluation (zero-heap, in-memory bitmasking).
> * **Docker Loopback Gateway**: **$< 1\ \text{ms}$** local HTTP/IPC proxy latency for multi-agent harness environments.

---

## 📚 Official Documentation Navigation

| Document | Language | Description |
| :--- | :--- | :--- |
| **[README_EN.md](README_EN.md)** | English | Detailed product overview, benchmarks, and licensing terms |
| **[README_ZH.md](README_ZH.md)** | 繁體中文 | 完整產品架構、微秒級熔斷原理與個人免費版中文說明 |
| **[SAFETY_EN.md](SAFETY_EN.md)** / **[SAFETY_ZH.md](SAFETY_ZH.md)** | EN / 繁中 | Ethical boundaries, GuardVM sandbox policy, and scope limits |
| **[VERIFICATION_GUIDE_EN.md](VERIFICATION_GUIDE_EN.md)** | English | Zero-dependency local CLI verification, diagnostics, and testing |
| **[docs/KEY_MANAGEMENT.md](docs/KEY_MANAGEMENT.md)** | Bilingual | Ephemeral keys, static key backup, and disaster recovery SOP |
| **[DROS_BOUNDARY_AND_VAJRA_GUIDE_EN.md](DROS_BOUNDARY_AND_VAJRA_GUIDE_EN.md)** | English | Dual-perspective mechanics and Vajra policy authoring guide |

---

## 🚀 Quick Start (Docker Loopback Gateway)

Run the pre-built gateway container locally (no API key required for local evaluation):

```bash
docker run -d -p 8080:8080 --name dros-gateway \
  -v $(pwd)/FreeTrial-Sandbox/demo_policy.yaml:/app/demo_policy.yaml \
  dros/hacker-gateway:v2.1.0
```

### Connect with MCP Clients (Claude, Cursor, Codex, Antigravity)
Add DROS Gateway to your client configuration (`mcp_settings.json`):
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

## ⚖️ Licensing & Intellectual Property

DROS VajraClaw Hacker Edition is **proprietary software** provided under a **personal, non-commercial free license**.

* **Personal Use**: **Free**
* **Non-Commercial Research & Evaluation**: **Free**
* **Commercial / Enterprise Production Use**: **Requires a commercial license** ([dr-os.io](https://dr-os.io))
* **Open Source / OSI License**: **Not Granted** (Not Apache-2.0, Not AGPL)

### 🛡️ Patent Notice
DROS execution governance and security technology is protected under:
> **U.S. Provisional Patent Application No. 64/111,973 (Patent Pending)**  
> *(A provisional patent application establishes priority and is not a granted patent.)*

---

*Top-Celestial Company Ltd. (康宸園有限公司) ── Commercial inquiries: [service@dr-os.io](mailto:service@dr-os.io)*
