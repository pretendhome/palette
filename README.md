<div align="center">

# Mission Canvas

### Your judgment compounds here.

**Local-first AI for regulated professionals.**  
Safe research. Governed memory. Smarter every time.

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-129_passing-brightgreen)]()
[![Capability Areas](https://img.shields.io/badge/capability_areas-131-blue)]()
[![Knowledge](https://img.shields.io/badge/knowledge-203_entries-blue)]()

</div>

---

## The Problem

25 million professionals in legal, finance, and healthcare are currently locked out of the AI revolution. Sending client data to the cloud isn't just a "setting"—it's a malpractice risk. Today, high-agency operators are improvising with disconnected local models and private notes. Their work is safe, but it doesn't compound.

## The Solution

**Mission Canvas** is the governed alternative. It is a local-first AI runtime designed for work that cannot leak.

- **Classify before Action**: Every query is mapped to a professional competency node (RIU) before it's processed.
- **Structural Security**: PII detection and strategy language blocking are built into the architecture, not added as a filter.
- **Governed Memory**: Your research and decisions are stored as typed artifacts that automatically connect to future work.

---

## Quick Start

```bash
git clone https://github.com/pretendhome/palette.git
cd palette
bash setup.sh
```

Mission Canvas checks dependencies, installs required packages, and starts the governed runtime.

**Requirements**: Python 3.10+, Node.js 18+.  
**Optional**: Ollama (fully local reasoning), Perplexity API key (governed external research).

---

## See It Work: Sarah's Morning

```bash
palette demo sarah
```

Follow a solo attorney through a high-stakes morning. Three moments, three intents, zero data leakage.

1.  **PROTECT** — "What's our exposure?" → **BLOCKED**. Strategy language detected at the gate. Zero data leaves the machine.
2.  **RESEARCH** — "Delaware fiduciary duty standards?" → Query sanitized, routed to Perplexity, results merged with verified local knowledge.
3.  **DECIDE** — "Should Sarah settle or litigate?" → **[CONNECT]** signal fires. Palette connects today's question to yesterday's research. Your judgment compounds.

---

## Your Judgment Trail

Every interaction improves the system. Use `palette stats` to see your professional footprint grow.

```bash
palette stats
```

```text
  mission canvas — your judgment trail

  Artifacts stored:     277
  Capability nodes:     29 / 131 (22%) active
  PII blocks:           95
  Integrity signals:    434
  Compounding for:      2 days

  Your judgment compounds here.
```

---

## 6 Governed Intents

Mission Canvas uses **Intents** to enforce boundaries between different types of work.

| Intent | Purpose | Governance |
|:---|:---|:---|
| `palette protect` | Safety gate | Blocks PII and strategy language at the source. |
| `palette research` | Evidence gathering | Sanitizes queries for safe external research via Perplexity. |
| `palette decide` | Decision support | Connects prior work and flags irreversible ONE-WAY DOORS. |
| `palette create` | Documentation | Generates typed artifacts with full provenance tracking. |
| `palette diagnose` | Problem isolation | Captures failure patterns as reusable lessons. |
| `palette reflect` | System audit | Proposes improvements to the local knowledge base. |

---

## Governed Automations (Crons)

Automate your high-stakes workflows without losing control.

```bash
palette cron create morning-brief RESEARCH "Delaware corporate law changes this week"
palette cron daemon
```

Every scheduled task follows the same governance rules as manual queries: boundary enforced, results stored for compounding.

---

## Built for Reliability

- **Socket Firewall**: 10-host allowlist; unauthorized external connections are physically impossible.
- **Risk-Tiered Execution**: Decisions involving irreversible steps require explicit human sign-off.
- **Local-First Knowledge**: Ships with a library of 203 verified legal and professional entries.
- **Append-only Audit**: Every signal is captured in an immutable integrity log.

---

## Architecture: The 6 Layers of Palette

Mission Canvas is powered by the **Palette Intelligence System**, a modular runtime for professional judgment.

1.  **Core**: Governance tiers and immutable execution rules.
2.  **Taxonomy**: 131 capability nodes that classify intent before action.
3.  **Knowledge**: Evidence-tiered library with 565+ citations.
4.  **Agents**: 13 specialized agents with performance-based trust tracking.
5.  **Service Mesh**: Governed routing to local (Ollama) or external (Perplexity/Claude) models.
6.  **Skills**: Domain-specific frameworks for legal, finance, and architecture.

---

<div align="center">

*Your judgment compounds here. Never elsewhere.*

[Quick Start](QUICKSTART.md) · [Architecture](CLAUDE.md) · [missioncanvas.ai](https://missioncanvas.ai)

</div>
