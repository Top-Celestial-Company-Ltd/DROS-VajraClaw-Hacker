# 🛡️ DROS™ VajraClaw (Free Trial PLG)
[![Official Website](https://img.shields.io/badge/Website-dr--os.io-purple.svg?style=for-the-badge)](https://dr-os.io)

[English](README.md) | [繁體中文](README_zh.md)

**Version: v1.0.0-free**

**The Execution Governance Standard for Agentic AI**

Welcome to the open-source Free Trial edition of DROS VajraClaw. This repository contains the core O(1) Physical Circuit Breaker engine with a 30-day offline RSA timebomb limit, supporting up to 2 concurrent AI Agents.

## 🛑 "If runtime needs intelligence, the system is already broken."
Prompt Engineering is dead when it comes to enterprise security. No matter how complex your System Prompt is, Jailbreaks and Prompt Injections will find a way through. API Gateways fail because they assume human-driven execution constraints apply to autonomous agents.

**DROS** is NOT a prompt wrapper. It is the **Execution Governance Standard**. We move intelligence to compile-time (`demo_policy.yaml`) and enforce rules via an **O(1) Bitmap Runtime Engine** (`core/vajra_claw.dll` / `.so`). If the Agent attempts an unauthorized action, DROS triggers a **Physical Fusing (Strict Fail-Closed)** and terminates the process in under 1 millisecond.

## ⚡ Performance Benchmark
Our engine operates in **O(1) constant time** with zero JSON parsing at runtime.
- **Normal execution overhead**: ~5.6 ms
- **Malicious prompt interception latency**: **~0.37 ms**

## 🚀 Quick Start (Demo)
1. Ensure you have Python 3.8+ installed. Install dependencies: `pip install -r ../requirements.txt` (or `pip install PyYAML`).
2. Review the O(1) constraints defined in `demo_policy.yaml`.
3. Run the attack simulation: `python run_demo_attack.py`
4. Watch the engine physically block the Prompt Injection attempt in under 1 millisecond!

---
**Developed by DROS Labs**
*Securing the autonomous frontier through Deterministic Execution.*
