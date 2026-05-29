<div align="center">

# Mission Canvas

### Your judgment compounds here.

Governed AI for professionals who can't send client data to the cloud.

[![License](https://img.shields.io/badge/license-Apache_2.0-blue)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-129_passing-brightgreen)]()
[![RIUs](https://img.shields.io/badge/routing_nodes-131-blue)]()
[![Knowledge](https://img.shields.io/badge/knowledge-203_entries-blue)]()

</div>

---

## Quick Start

```bash
git clone https://github.com/pretendhome/palette.git
cd palette
bash setup.sh
```

That's it. Checks dependencies, installs packages, prompts for API keys (all optional), starts services, opens your browser.

**Requirements**: Python 3.10+, Node.js 18+. Optional: Ollama (fully local queries), Perplexity API key (external research).

---

## See It Work

```bash
palette demo sarah
```

Three moments. Three intents. Three typed artifacts. Zero data leakage.

1. **PROTECT** — "What's our exposure?" → BLOCKED. Strategy language detected. Zero data left the machine.
2. **RESEARCH** — "Delaware fiduciary duty standards?" → Sanitized, routed to Perplexity, citations returned. Client identity stripped.
3. **DECIDE** — "Should we settle or litigate?" → Connected to 2 prior decisions. Reversibility checked. Judgment compounded.

---

## Your Judgment Trail

```bash
palette stats
```

```
  mission canvas — your judgment trail

  Artifacts stored:     260
  RIUs activated:       29 / 131 (22%)
  Cron executions:      1 (100% governed)
  PII blocks:           89
  Integrity signals:    401
  First artifact:       2026-05-27
  Compounding for:      1 days

  Your judgment compounds here.
```

---

## 6 Governed Intents

Every interaction is classified before it's acted on. That's the difference.

| Intent | What It Does | Governance |
|:--|:--|:--|
| `palette protect` | PII detection, local-only routing | Blocks client data at architecture level |
| `palette research` | Governed external research via Perplexity | Query sanitized, citations returned |
| `palette decide` | Decision with reversibility check | Prior decisions connected, one-way doors flagged |
| `palette create` | Artifact creation with provenance | Who created what, when, why — tracked |
| `palette diagnose` | Root cause isolation, fix verification | Failure patterns captured as lessons |
| `palette reflect` | System self-audit | Improvement proposals through governance |

---

## Scheduled Tasks (Governed Crons)

```bash
palette cron create morning-brief RESEARCH "Delaware corporate law changes this week"
palette cron list
palette cron daemon
```

Every scheduled task is governance-gated: approved, not expired, boundary enforced. Results stored as typed artifacts for compounding. This is what makes Mission Canvas crons different — scheduled tasks with trust boundaries.

---

## Telegram Bot

```bash
MC_BOT_TOKEN="your-token" python3 mission-canvas/mc_telegram.py
```

"Who are you?" → role selection → governed queries with visible governance signals. Works where you already are.

---

## Built for Work That Cannot Leak

- Socket firewall — 10-host allowlist, unauthorized connections blocked
- PII sanitizer — 3-layer detection before any external call
- Governance tiers — irreversible actions require human sign-off
- Append-only decision log — immutable audit trail
- Approval workflows — scheduled tasks require sign-off and expiry
- Trust boundaries — internal-only vs governed-external classification
- Zero CVEs — security designed in, not bolted on

---

## Architecture

Mission Canvas is powered by Palette — a governed runtime with 6 layers:

| Layer | What | Scale |
|:--|:--|:--|
| **Core** | Governance tiers, immutable rules, ONE-WAY DOOR classification | 3 tiers |
| **Taxonomy** | Problem classification before retrieval | 131 RIU nodes |
| **Knowledge** | Evidence-tiered, cited entries | 203 entries, 565 citations |
| **Agents** | Governed specialists with maturity tracking | 13 agents |
| **Buy-vs-Build** | Service routing with integration recipes | 106 services, 75 recipes |
| **Skills** | Validated domain frameworks | 6 domains |

### Hybrid Retrieval

FTS5 full-text + vector embeddings + keyword matching, fused with reciprocal rank fusion. Local-first, zero API cost. Every query is classified through the taxonomy before the LLM response is grounded in verified knowledge.

### Multi-Agent Coordination

13 governed agents. Each earns trust through performance (UNVALIDATED → WORKING → PRODUCTION). Automatic demotion on repeated failures. Message bus with schema-validated envelopes, risk gates, and human checkpoints.

### Voice Interface

Talk to any agent. 5 LLMs (Claude, Mistral, GPT, Qwen, Perplexity) in 4 languages. Rime Arcana TTS. Web Speech STT.

---

## Run Tests

```bash
uv run pytest -q scripts/palette_intelligence_system/test_*.py
```

---

## Origin

Palette was distilled from 12 years of knowledge engineering at Amazon and 250+ enterprise AI enablement sessions reaching 20,000+ users annually. The 131 competency areas emerged from real questions asked by real practitioners. The knowledge library was built through iterative research, source verification, and evidence tiering — not generated from a prompt.

The comparative linguistics foundation (MA, Universite Paris-Sorbonne) directly informed the architecture: mapping natural language to structured competency is the same discipline as intent classification.

---

<div align="center">

*Your judgment compounds here.*

[Quick Start](QUICKSTART.md) · [Architecture](CLAUDE.md) · [Landing Page](https://missioncanvas.ai) · [Competitive Analysis](bdb/COMPETITIVE_INTELLIGENCE_2026-05-28.md)

</div>
