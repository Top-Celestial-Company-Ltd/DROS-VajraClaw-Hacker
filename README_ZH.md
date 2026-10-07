# ?儭?Deterministic Runtime OS (DROS) - VajraClaw Hacker Edition
**DROS: 蝣箏??批銵?瘝餌?雿平蝟餌絞??Agent 摰敺格敹?*

[![License: Source-Available](https://img.shields.io/badge/License-Source--Available%20(??璆剖?鞎餉?隡?-blue.svg)](#-????閬?licensing--compliance)
[![Patent Status](https://img.shields.io/badge/U.S._Patent_Pending-64%2F111%2C973-blue.svg)](#-????閬?licensing--compliance)
[![Technical Reports](https://img.shields.io/badge/Open_Archive-Zenodo_Preprints-purple.svg)](https://doi.org/10.5281/zenodo.21808499)
[![Internal Spec](https://img.shields.io/badge/?折閬-DROS--RFC--010-darkgreen.svg)](#)

[English](README_EN.md) | [蝜?銝剜?](README_ZH.md)

---

> ?? **??瑁????閬?璅∪??箸靘蝳佗?蝟餌絞撠勗歇蝬◤?餌鈭?*
>
> Prompt Engineering ?其?璆剔?摰?Ｗ?撌脩?憭望??隢?System Prompt 閮剛?敺?銴?嚗????內閰釣?亦?蝛嗉蝛輸蝺?
> **DROS 銝蝝?摮?Prompt 瞈曄雯嚗 Agent ?瑁??祥??皞?* ???賢?撽??蔭?潛楊霅舀?嚗蒂?典銵??祕?賜Ⅱ摰扳蝑??伐?
> * **撣嗅 C-ABI / Rust 敺格敹?*嚗?*$< 3\ \mu\text{s}$** 蝣箏??扯?????瘥?嚗??????閮擃??蝵抬???
> * **Docker ?砍?啣?蝬脤?**嚗?*$< 1\ \text{ms}$** ?砍 HTTP/IPC 隞??撱園嚗?? Agent 瘝??啣???

---

> ? **??啣??嫘??冽?甈?隡平?寞?隢誑 [摰蝬脩? (dr-os.io)](https://dr-os.io) ?砍??箸???*

| 摰? / 6-Pillar 璈蝬剖漲 | ? Hacker (?犖蝷曄黎??- ?祥閰摯) | ? Startup | ? Enterprise | ?? Sovereign |
| :--- | :---: | :---: | :---: | :---: |
| **?格?摰Ｘ** | **?犖???/ ?祆?憭?Agent嚗??平?券?** | 10~50鈭箸?萄???| 銝剖之??璆?/ 銝??砍 | ??? / ? |
| **璈?? (UUIDs)** | **1 蝯?UUID** | 3 蝯?UUIDs | 15 蝯?UUIDs | **?⊿???* |
| **Concurrent Agents 銝?** | **5 ?蒂??Agent** | 30 ??| 450 ??| **?⊿???(Swarm)** |
| **Pillar 1嚗rincipal 頨思遢霅?** | ??**?? W3C `did:key` ??** | ??**3-Tier PKI DIT** | ??**頝典? BEC ???潭** | ??蝖祇? Dongle ?啗? |
| **Pillar 2嚗uthorization 甈????*| ??**?賢?暺??撠?* | ??**?嗅?蝛?Bitmaps** | ??**?刻閮?Capability ??**| ????雿???蝬剔??|
| **Pillar 3嚗ool Bound 撌亙??** | ??**撣嗅 C-ABI嚗?<3\mu\text{s}$**<br>*(Docker 隞??嚗?<1\text{ms}$)* | ??**撣嗅? $<30\mu\text{s}$** | ??**甈∪凝蝘?敺格敹?*| ???嗥?蝖祇?蝝????|
| **Pillar 4嚗olicy Gate 銝之???* | ????????| ??**?? PII ?株** | ??**HITL ?偷 + ZKP-Lite** | ??頠?蝝??亦??|
| **Pillar 5嚗udit Log 蝔賣餈賣滲** | ??**Ed25519 蝪賜??亥?** | ??**Ed25519 ?訾?蝪賜?**| ??**SHA-256 Merkle ????* | ??銝?西??扳??Ｙ??? |
| **Pillar 6嚗xpiry/Revocation 蝘**| ????? Gateway | ? 15?? BEC ?? | ??**閮擃??????** | ???撘?蝝雯?潭??|
| **DROS-RFC-010 ?折霅瑞?澆?** | ??**?砍摰蝪賜??潸?** | ??**憭???DIT 蝪賜蔡** | ??**隡平 GuardVM ?葉撽?** | ???蝝?3-Tier 蝪賜???|
| **?敶批?鞈潛璆剖?閬?Package** | ??銝??曉?鞈?| ? **?敶批?鞈?* | 潃?**?敶批?鞈?* | ???摰甈? |
| **?函蔡頛?** | **Local PC / Docker 蝬脤?**| **VM / NAS Docker** | K8s / GKE / Cluster | Air-Gapped / FPGA |

---

## ?? 憭?舀???函蔡?? (Multi-Scenario Deployment Guide)

### ?? ?? A嚗SH (DeepSeek Harness) 瘝?雿輻??
1. **?? DROS Docker 蝬脤?**嚗?
   ```bash
   docker run -d -p 8080:8080 --name dros-gateway dros/hacker-gateway:v2.1.0
   ```
2. **??DSH 銝剖?鋆冗?憭?**嚗?
   ```bash
   dsh plugin --profile web add dsh-plugin-dros
   ```
3. **鈭怠?敺桃?蝝銵祥??*嚗SH ?抒? Agent 撌亙隤輻撠??喟 DROS ?瑁??凝?詨??脰?蝣箏??折霅瑁?撖抵???

---

### ? ?? B嚗ntigravity 2.0 / Codex / Cursor ???(MCP ?降)
?冽??`mcp_settings.json` ??Claude Desktop ?蔭銝剖???DROS 蝬脤?嚗?
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

### ?? ?? C嚗???Python / LangChain / AutoGen ???
```python
from integrations.vajraclaw.runtime import VajraClaw

vc = VajraClaw("demo_policy.yaml")
decision = vc.evaluate("execute_payment", {"amount": 500})
if not decision:
    raise PermissionError(f"Blocked by DROS: {decision.reason}")
```

---

## ?儭??格??函蔡?怠???痊隞餃?蝵格?隞?(Target Profiles & Shared Responsibility)

DROS ?湔???**?撅文?閬炎?仿? (In-Process PEP)** ??**?函??脩?蝖祇???(Isolated Confinement)** 銋???

| ?格??函蔡?怠? (Target Profile) | ?函蔡頛??銵憓?| 靽?蝑??霅瑟???| 隤?隢????蔭璇辣 |
| :--- | :--- | :--- | :--- |
| **Linux / Windows 隡箸??刻??璈?* | ?函??脩?蝬脤? / Docker Sidecar | **撘瑕??Fail-Closed嚗?⊥??賂?** | Agent ???澆??雯頝臬?征??(`egress: default-deny`)嚗ateway ?箏銝隞???箏嚗??函?撖行?霅??券??Ｘ Gateway 閮擃?|
| **?楠?∩犖璈?(Physical AI / UAV)** | 璈?隡湧閮?璈?(NVIDIA Jetson / Linux ROS 2) | **撣嗅 MAVLink ???誘?** | ???潔撈?券?佗??冽?隞斤敺憌? UART/Ethernet ???嚗?銝?仿?銵頝?RTOS/??MMU ??撅文凝?批?券??找蜓????|
| **銵?蝡?SDK (iOS / Android)** | 摰蹂蜓 App ?批????摨?(`.dylib` / `.so`) | **In-Process PEP嚗??典惜??嚗?* | ??蝺刻陌??App 鈭脖??找誑蝝??折 Agent 銵嚗?銝脰??典? OS 蝟餌絞隤輻?嚗?頞? iOS/Android 瘝??湔蝳迫頝券脩?瘜典嚗???|

> [!IMPORTANT]
> **?函蔡?捱璇辣 (Deployment Precondition)**嚗?*?gent 摰瘛芷銝??嗆?蝡??拍? Fail-Closed??* 靽?嚗?*? Agent ??Gateway ?函蔡?潮??Ｗ捆?冽??蝬脰楝?嚗?蝬?Raw Socket ??OS ?詨?撠?嚗???**???犖摰蹂蜓璈?嚗n-Process ?雿?Ｗ??????瑼Ｘ暺?

---

## ?? ?銵?格?敹?銵???(Technical Whitepapers & Core Papers)

DROS ?瑁??Ⅱ摰扳祥?瑽?雓寧?摮貉?隤?隢蝷??函頂???餃歇?脣??飛銵??舐砥??DOI 瘞訾?摮?嚗?

### ?妣 蝘??冽撠? (Master Overview & Falsification Manifesto)
*   **?ROS ?冽蝘?撠?嚗蝭?????????隢?蝟餉??航??賣扯??*
    *   *A Synoptic Guide to the DROS Program: Problem Formulation, Theoretical Architecture, and Falsification Criteria*
    *   **Zenodo DOI**: [`10.5281/zenodo.22255275`](https://doi.org/10.5281/zenodo.22255275) | **Record**: [zenodo.org/records/22255275](https://zenodo.org/records/22255275)

---

### ? ?剖之?詨??銵???(The 6-Paper Program)

1. ??儭?**Paper 1: DROS-6P (瘝餌?閬撅??? 隡平靽∩遙?憭折??祥??**
   * *DROS-6P: A Unified Deterministic Runtime Governance Architecture Closing the Six Fundamental Trust Boundaries of Enterprise AI Agents*
   * **Zenodo DOI**: [`10.5281/zenodo.21833970`](https://doi.org/10.5281/zenodo.21833970) | **Record**: [zenodo.org/records/21833970](https://zenodo.org/records/21833970)

2. ?儭?**Paper 2: DROS 4-Layer (?瑁??賢撅??? ?惜瘛勗漲?脩戌蝮望楛?嗆?)**
   * *DROS 4-Layer Defense-in-Depth Architecture for Autonomous AI Workloads*
   * **Zenodo DOI**: [`10.5281/zenodo.22092008`](https://doi.org/10.5281/zenodo.22092008) | **Record**: [zenodo.org/records/22092008](https://zenodo.org/records/22092008)

3. ?? **Paper 3: DROS-PGM (?扳?批撅??? 撖阡??脰風璅∠????臬隤折?銵?甇貉痊)**
   * *Runtime Attribution Framework: An External C-ABI and PKI-Based Zero-Trust Infrastructure for Non-Repudiable Execution Governance in Multi-Agent Systems*
   * **Zenodo DOI**: [`10.5281/zenodo.21903687`](https://doi.org/10.5281/zenodo.21903687) | **Record**: [zenodo.org/records/21903687](https://zenodo.org/records/21903687)

4. ?? **Paper 4: DROS-WebMCP (蝬脩窗?賢?撅??? Agentic Web ???脣銵祥??**
   * *DROS-WebMCP: A Cryptographically Attributable Execution Governance Layer for the Agentic Web*
   * **Zenodo DOI**: [10.5281/zenodo.22290238](https://doi.org/10.5281/zenodo.22290238) | **Record**: [zenodo.org/records/22290238](https://zenodo.org/records/22290238)

5. ? **Paper 5: Post-Compromise Mobile (?訾?蝟餌絞撖西? ?? ?訾?蝟餌絞撖西?)**
   * *Post-Compromise Security for Autonomous Mobile Agents: A Deterministic Runtime Attenuation and Proof-Carrying Authorization Architecture*
   * **Zenodo DOI**: [`10.5281/zenodo.22253147`](https://doi.org/10.5281/zenodo.22253147) | **Record**: [zenodo.org/records/22253147](https://zenodo.org/records/22253147)

6. ? **Paper 6: Post-Compromise Physical AI / UAV (蝬脩窗-撖阡?撖西? ?? 蝬脩窗-撖阡?撖西?)**
   * *Post-Compromise Security for Physical AI: Deterministic Runtime Enforcement of Physical Action Authority in Autonomous UAVs*
   * **Zenodo DOI**: [`10.5281/zenodo.22254372`](https://doi.org/10.5281/zenodo.22254372) | **Record**: [zenodo.org/records/22254372](https://zenodo.org/records/22254372)

---
*??閰葫???賣???[DROS-VEP Lite (GitHub)](https://github.com/Top-Celestial-Company-Ltd/dros-vep-lite) ?? 摰? RFC-001 憡?璅∪???4 ?挾??望?皜祈岫??

---

## ??儭?摰?潸?蝯??蝜怨?閮?(Official Contact)
* **?潸?銝駁?**嚗op-Celestial Company Ltd. (摨瑕捂?????
* **摰蝬脩?**嚗https://dr-os.io](https://dr-os.io)
* **摰Ｘ?????垣閰?*嚗service@dr-os.io](mailto:service@dr-os.io)
* **GitHub 摰蝯?**嚗https://github.com/Top-Celestial-Company-Ltd](https://github.com/Top-Celestial-Company-Ltd)

---

## ?? ????閬?(Licensing & Compliance)

*   **??璅∪? (License Model)**: **皞Ⅳ?舐??嚗ource-Available嚗??平?券??犖閰摯?祥嚗?*?遙雿?璆剖??函蔡?aaS 閮恣??璆剔??Ｙ憓矽?剁????????平閮??璆剜?甈?蝝?
*   **撠摰?? (Patent Notice)**: DROS ?瑁?瘝餌????冽?銵歇?唾?蝢??冽?撠靽風嚗?*U.S. Patent Application No. 64/111,973嚗atent Pending**嚗?
*   **摮貉?靘?????(Academic Preprints & Specs)**: ?嗆????箇?撱箇???Zenodo ?祇?摮???祉頂????DOI: 10.5281/zenodo.21808499 蝟餃?嚗????折?銵瑽?蝭?DROS-RFC-010嚗?

---
*DROS ?平?Ｗ?蝑憪???? ?０摰嚗?頛芷?摰??Ｘ平??憟??滯?嫘? ???儭?儭?
---

## License

DROS VajraClaw Hacker Edition is **not Open Source software**.

The source code is made available under a proprietary
personal and non-commercial free license.

- Personal use: **Free**
- Non-commercial use: **Free**
- Commercial use: **Requires a separate commercial license**
- Open Source / OSI license: **Not granted**

Patent pending:
U.S. Provisional Patent Application No. 64/111,973.

A provisional patent application is not a granted patent.

See LICENSE for the complete license terms.
---

## License

DROS VajraClaw Hacker Edition is **not Open Source software**.

The source code is made available under a proprietary
personal and non-commercial free license.

- Personal use: **Free**
- Non-commercial use: **Free**
- Commercial use: **Requires a separate commercial license**
- Open Source / OSI license: **Not granted**

Patent pending:
U.S. Provisional Patent Application No. 64/111,973.

A provisional patent application is not a granted patent.

See LICENSE for the complete license terms.
---

## License

DROS VajraClaw Hacker Edition is **not Open Source software**.

The source code is made available under a proprietary
personal and non-commercial free license.

- Personal use: **Free**
- Non-commercial use: **Free**
- Commercial use: **Requires a separate commercial license**
- Open Source / OSI license: **Not granted**

Patent pending:
U.S. Provisional Patent Application No. 64/111,973.

A provisional patent application is not a granted patent.

See LICENSE for the complete license terms.

