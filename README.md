<div align="center">

<img src="legal/trademarks/palette_tag_primary_uspto.jpg" alt="Palette" height="80">
<br>
<sup>™</sup>

### The Operating System for Human Judgment

Every AI tool gives you an answer and forgets why you asked. Palette remembers what you decided, why you decided it, and makes every future decision better. Your judgment compounds here.

---

[![Status](https://img.shields.io/badge/status-V3_active-blue)]()
[![Health](https://img.shields.io/badge/health-122%2F135_passing-brightgreen)]()
[![Tests](https://img.shields.io/badge/tests-201_passing-brightgreen)]()
[![RIUs](https://img.shields.io/badge/taxonomy-121_nodes-blue)]()
[![Knowledge](https://img.shields.io/badge/knowledge-183_entries-blue)]()
[![Agents](https://img.shields.io/badge/agents-13_governed-blue)]()
[![License](https://img.shields.io/badge/license-Apache_2.0-blue)](LICENSE)

</div>

---

## What Is Palette?

Palette is a governed runtime for multi-agent AI. You talk to it. It coordinates a team of agents — each with its own voice, memory, and behavioral rules — grounded in verified knowledge, controlled by auditable governance. The system doesn't just make you more efficient. It makes you more capable.

**The moat**: Palette builds a governed, portable, compounding record of what you are trying to do, what you decided, why you decided it, and what the system learned with you. This is architecturally impossible to bolt onto a chat interface — it requires taxonomy, governance, and memory to be the foundation, not features.

**The thesis**: accumulated context + intent is the defining asset of the AI-mediated information economy. Palette is the first system that architecturally encodes this asset at the protocol level — local-first, portable, glass-box.

### Why ChatGPT Cannot Bolt This On

The moat is not "memory." It is a stack of architectural primitives working together:

- **Taxonomy-first routing** — 121 nodes classify your problem BEFORE retrieval. The system knows what kind of decision you're making.
- **Governed knowledge** — 183 entries, 565 citations, evidence tiers. Every claim traces to a source. Zero unsourced assertions.
- **Append-only decision history** — What you decided, why, and what evidence supported it. Judgment trail, not chat history.
- **Portable local state** — YAML files on your machine. Take your judgment anywhere. No vendor lock-in.
- **Multi-agent convergence** — 13 specialists disagree productively, then converge. The room where you think with AI.
- **Capability-building** — Learning Mode teaches you while it works. The system makes you more capable, not more dependent.
- **Hybrid retrieval** — FTS5 + vector embeddings + keyword matching, fused with reciprocal rank fusion. Local-first, zero API cost.
- **Adaptive Intent Framework** — Designed experiences that guide professionals through governed multi-model workflows. CONVERGE, CREATE, DIAGNOSE, RESEARCH, TEACH, EVALUATE, COMMUNICATE, REFLECT. Each intent is a heuristic sequence where Palette checkpoints between every step — the OS can branch, loop back, or switch intents mid-flow based on what it learns. Nobody else has this.
- **Voice interface** — Talk to any agent. Each has its own voice (Tessitura). Spatial metaphor, not chat window.

---

## Voice & Multilingual Agent Design

Palette includes specialized tooling for multilingual voice agent evaluation, multi-agent voice coordination, and speech synthesis integration.

### [Voice Evaluation Workbench](voice/workbench/) — [Live Demo](https://pretendhome.github.io/palette/voice-workbench/)
A multilingual tool for comparing, scoring, and choosing AI agent voices across customer journey stages (Acceptance, Resolution, Satisfaction). Structured rubric (Naturalness, Trust, Cultural Fit, Brand Fit, Clarity), weighted scoring, TTFA measurement, locale-specific watchouts, and exportable decision scorecards. 4 languages, native-speaker voices per language, 3 journey stages.

### [Voice Hub](peers/hub/) — Multi-Agent Voice Interface
A voice-first interface connecting 5 LLM agents (Claude, Mistral, GPT, Qwen, Perplexity) through voice in 4 languages. Rime Arcana v2 TTS with sentence-boundary streaming, Whisper local STT, and every voice query classified through the 121-node RIU taxonomy before grounding the response in the knowledge library. Governed message bus with risk gates and human checkpoints.

![Voice Hub — 4 agents, 4 languages, one workflow](docs/images/voice-hub-screenshot.png)
*Research (FR/Perplexity) → Design (EN/Claude) → Build (IT/Codex) → Implement (ES/Qwen) — four agents, four languages, one workflow.*

---

## System Summary

<div align="center">

| Component | Specification |
|:--|:--|
| Taxonomy Nodes (RIUs) | 121 (81 internal, 40 service-routed) |
| Knowledge Entries | 183 with 565 verified source citations and evidence tiers |
| Governed Agents | 13 (resolver, researcher, architect, builder, debugger, narrator, validator, monitor, orchestrator, remediation, business-plan-creation, health, total-health) |
| Integration Recipes | 75 (auth, endpoints, cost, quality tier) |
| Service Routing | 106 services across 40 routing profiles |
| Hybrid Retrieval | FTS5 + vector embeddings + keyword (reciprocal rank fusion) |
| Voice Interface | 8 agents with unique Arcana v3 voices (Tessitura) |
| Health Score | 122/135 passing (15 sections) |
| Test Suite | 201 passing across 4 suites (PIS, SDK, gateway, V3) |
| Lenses | 30 role-based context overlays |
| Skills | 6 domains (retail-ai, talent, education, travel, enablement, lenses) |

</div>

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Natural Language In                       │
├─────────────────────────────────────────────────────────────┤
│  Resolver  →  Coordination Pipeline  →  Traverse     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  6 Data Layers                                       │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │    │
│  │  │Taxonomy  │ │Routing   │ │Recipes   │            │    │
│  │  │121 RIUs  │ │106 svcs  │ │75 specs  │            │    │
│  │  └──────────┘ └──────────┘ └──────────┘            │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │    │
│  │  │Knowledge │ │Signals   │ │Overrides │            │    │
│  │  │183 entries│ │21 people │ │19 maps   │            │    │
│  │  └──────────┘ └──────────┘ └──────────┘            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Integrity Layer                                     │    │
│  │  Integrity → Audit → Regression → Drift → Monitor      │    │
│  │  8/8 checks   1 finding  7/7 SLOs   15 clusters     │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                    Governed Action Out                        │
│         ship │ ship_with_risks │ ship_with_convergence │ block│
└─────────────────────────────────────────────────────────────┘
```

### Three Tiers

**Tier 1: Core Governance** — Immutable rules. Convergence before execution, glass-box reasoning, ONE-WAY DOOR (irreversible, requires human review) vs TWO-WAY DOOR (reversible, can proceed) classification.

**Tier 2: Agent Maturity** — 12 specialized agents that earn autonomy through measured performance. UNVALIDATED → WORKING → PRODUCTION. Automatic demotion on repeated failures. This is a competency framework applied to AI agents themselves.

**Tier 3: Integrity & Assessment** — Structural proof that the system is healthy. Consistency checks, audit findings, regression detection, SLO enforcement, terminology drift tracking. The integrity engine is the assessment layer — it evaluates whether knowledge is current, complete, and internally consistent.

---

## Current Status

<div align="center">

| Metric | Value | Threshold |
|:--|:--|:--|
| Consistency checks | **8/8 passing** | 8/8 |
| Taxonomy↔Classification | **121/121** | 121/121 |
| Classification↔Routing | **40/40** | 40/40 |
| Routing↔Recipe | **112/112** | ≥ 95% |
| Knowledge↔Taxonomy | **575/575** | — |
| Signal↔Taxonomy | **45/45** | — |
| Orphan recipes | **70/70** clean | 0 orphans |
| Orphan signals | **57/57** clean | 0 orphans |
| Traverse health | **121/121 healthy** | — |
| Test suites | **201 passing** | — |

</div>

---

## Verified Operational State

Verified in the current repo as of 2026-05-26:

- **Integrity engine**: 8/8 cross-layer consistency checks passing (taxonomy↔classification↔routing↔recipe↔knowledge).
- **Test suites**: 201 tests passing across 4 suites — PIS integrity (60), SDK agent framework (89), gateway (12), V3 pipeline (40+). 4 integration tests skipped (require numpy/Ollama for vector embeddings).
- **Hybrid retrieval engine**: FTS5 full-text search + vector embeddings (nomic-embed-text via Ollama) + keyword matching, fused with reciprocal rank fusion. Local-first, zero API cost. Called by Voice Hub for taxonomy-grounded responses.
- **Wiki governance pipeline**: Deterministic compiler (345 pages), 4-script pipeline (file → vote → promote → bridge), multi-agent voting roster with trust tiers.
- **Peers bus**: Governed message bus at `127.0.0.1:7899` with 5 registered peers (Claude, Kiro, Codex, Gemini, Hub), schema-validated envelopes, delivery tracking.
- **Voice Hub**: Multi-agent voice interface with Rime Arcana TTS, Web Speech STT, taxonomy-grounded retrieval, 4 languages.
- **Gateway** (V3): Perplexity Sonar API gateway with prompt sanitization, response caching, rate limiting, and audit logging. 12/12 tests passing.

Health scores: 79/90 base health, 122/135 total health. Remaining failures are repo-sync drift (competition branch divergence) and name scrub in working documents — not system integrity issues.

---

## Traverse Engine

The traverse engine queries any competency area and returns a structured assessment packet — recommendation, alternatives, cost data, knowledge citations, and completeness score:

```
$ python3 -c "
from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.traverse import traverse
r = traverse(load_all(), riu_id='RIU-082')
"

RIU: RIU-082 — LLM Safety Guardrails (Content + Tool Use)
Classification: both
Recommendation: AWS Bedrock Guardrails
  Quality: tier_1 | Cost: PII + word filters FREE. Content: $0.15/1K units.
  Integration: available | Recipe: True
Alternatives:
  - Lakera Guard (tier_1, free 10K req/month, Pro $99/month)
  - Guardrails AI (tier_1, OSS free, Pro ~$50/month)
Knowledge support: 9 entries
Completeness: 85/100
Health: ok
```

Every service-routed competency area (40/40) returns a recommendation with alternatives, cost data, and evidence citations.

---

## Hybrid Retrieval Engine

Three retrieval strategies combined via Reciprocal Rank Fusion (RRF):

```
Query: "how do I evaluate voice quality?"

┌──────────────────────────────────────────────────────┐
│  1. Keyword Resolve (prefix match → RIU taxonomy)     │
│     → RIU-524: Voice Quality Assessment               │
│     → 3 knowledge entries matched                     │
│                                                       │
│  2. FTS5 Full-Text Search (Porter stemming, BM25)     │
│     → 7 passages ranked by term frequency             │
│     → Source: knowledge library + taxonomy descriptions│
│                                                       │
│  3. Vector Similarity (nomic-embed-text via Ollama)    │
│     → Top-5 by cosine similarity                      │
│     → Embeddings computed once, cached locally         │
│                                                       │
│  Reciprocal Rank Fusion: merge all three ranked lists  │
│  → Final ranked results with RIU classification        │
│  → Context string for LLM grounding                   │
└──────────────────────────────────────────────────────┘
```

The retrieval engine powers the Voice Hub — every voice query is classified through the 121-node taxonomy before the LLM response is grounded in verified knowledge. Local-first, zero API cost for retrieval.

**Architecture**: `peers/hub/palette_retrieve.py` (retrieval) + `peers/hub/server.mjs` (API + streaming) + `peers/hub/palette_db.py` (FTS5 + vector store).

---

## Integrity Engine

The integrity engine is the write path — structural proof that the system is healthy.

```bash
# Consistency checks
python3 -m scripts.palette_intelligence_system.integrity --checks-only

# Audit with severity ranking
python3 -m scripts.palette_intelligence_system.audit_system

# Regression check against baseline
python3 -m scripts.palette_intelligence_system.regression --check

# Terminology drift detection
python3 -m scripts.palette_intelligence_system.drift

# Governance decision
python3 -m scripts.palette_intelligence_system.para_decision
```

The Monitor decision engine chains all four checks and outputs a governed decision:

```
Decision: ship_with_risks
Accepted risks:
  - LINK_MISSING_PEOPLE_SIGNALS: 28 RIUs without people signal coverage
Required actions:
  - Expand people signal crossrefs for uncovered both-classified RIUs
```

---

## Agents

| Agent | Role | Specialty |
|:--|:--|:--|
| **Resolver** | Intent Resolution | Maps input to RIU, asks clarifying questions |
| **Researcher** | Research | Check internal libraries first, then Perplexity Sonar API |
| **Architect** | Architecture | Design with explicit tradeoff clarity |
| **Builder** | Build | Scope-bounded implementation |
| **Debugger** | Debug | Root cause analysis, fix verification |
| **Narrator** | Narrative | Evidence-based GTM, no speculation |
| **Validator** | Validation | Quality gates, GO/NO-GO verdicts |
| **Monitor** | Monitoring | Governance decisions, block routing |
| **Orchestrator** | Workflow | Routes between agents, manages relay |
| **Business Plan** | Planning | Multi-agent business plan workflow |
| **Health** | Integrity | System-wide health checklist, 8 sections |
| **Total Health** | Deep Audit | Cross-layer integrity, identity coherence, 13 sections |

**Maturity Model**: Agents earn trust through performance.
- **UNVALIDATED** → 10 successes → **WORKING** → 50 runs <5% fail → **PRODUCTION**
- 2 failures in 10 runs → automatic demotion

**Block Routing**: When Monitor blocks a decision, it routes to the right agent:
- Self-inflicted bug → Debugger
- Architecture gap → Architect
- Research gap → Researcher

---

## Project Structure

```
palette/
├── CLAUDE.md                           # Claude Code project instructions
├── AGENTS.md                           # OpenAI Codex project instructions
├── MANIFEST.yaml                       # Single source of truth for versions/paths
├── .steering/                          # AI agent self-reflection and steering
│   ├── claude-code/                    # Claude Code context
│   ├── codex/                          # OpenAI Codex context
│   ├── gemini/                         # Gemini context
│   ├── kiro/                           # Kiro steering + audits
│   ├── mistral/                        # Mistral context
│   └── perplexity/                     # Perplexity context
├── core/                               # Governance tiers
│   ├── palette-core.md                 # Tier 1 — Immutable rules
│   ├── assumptions.md                  # Tier 2 — Experimental assumptions
│   └── decisions-prompt.md             # Tier 3 — Decision log policy
├── taxonomy/releases/v1.3/             # 121 competency areas (RIUs)
├── knowledge-library/v1.4/             # 183 entries with evidence tiers
├── buy-vs-build/
│   ├── integrations/                   # 75 integration recipes
│   ├── service-routing/v1.0/           # 106 services, 40 routing profiles
│   └── people-library/v1.1/           # 21 profiles, 33 tools tracked
├── mission-canvas/                     # Voice-first execution platform
│   ├── index.html                      # Unified voice UI
│   ├── server.mjs                      # API server (10 endpoints)
│   ├── workspaces/                     # Workspace configs + state
│   └── competitions/                   # Multi-agent design competitions
├── agents/                             # 12 specialized agents
│   ├── resolver/                       # Intent resolution
│   ├── researcher/                     # Research (Perplexity Sonar primary)
│   ├── architect/                      # System design
│   ├── builder/                        # Implementation
│   ├── debugger/                       # Failure diagnosis
│   ├── narrator/                       # GTM/narrative
│   ├── validator/                      # Quality gates
│   ├── monitor/                        # Signal monitoring
│   ├── orchestrator/                   # Workflow routing
│   ├── business-plan-creation/         # Multi-agent business plan
│   ├── health/                         # System integrity (8 sections)
│   └── total-health/                   # Cross-layer audit (13 sections)
├── peers/                              # Governed multi-agent message bus
├── skills/                             # Validated domain frameworks
│   ├── retail-ai/                      # Enterprise AI strategy
│   ├── talent/                         # Interview prep + applications
│   ├── education/                      # Adaptive learning
│   ├── travel/                         # Route planning + booking
│   ├── enablement/                     # Agentic coaching
│   └── lenses/                         # Role lens methodology
├── bdb/                                # V3 gateway, vertical knowledge packs
├── sdk/                                # Agent SDK (Python)
├── scripts/                            # Integrity, audit, regression, drift
├── lenses/                             # 30 role-based context overlays
├── docs/                               # All documentation
│   ├── audits/                         # Dated audit and stress test reports
│   ├── onboarding/                     # Agent onboarding guides
│   ├── product/                        # Product thinking and specs
│   ├── research/                       # Research outputs
│   └── architecture/                   # System architecture docs
├── assets/                             # Brand, one-pager, UX reports
├── bridges/                            # Telegram bridge interfaces
└── legal/                              # Trademarks and IP
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/pretendhome/palette.git
cd palette

# Run integrity checks
python3 -m scripts.palette_intelligence_system.integrity --checks-only

# Run full audit
python3 -m scripts.palette_intelligence_system.audit_system

# Check regression status
python3 -m scripts.palette_intelligence_system.regression --check

# Run governance decision
python3 -m scripts.palette_intelligence_system.para_decision

# Traverse a specific RIU
python3 -c "
from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.traverse import traverse
r = traverse(load_all(), riu_id='RIU-521')
print(f'{r.query_riu} — {r.query_riu_name}')
print(f'Recommendation: {r.recommendation.service_name}')
print(f'Completeness: {r.completeness.total}/100')
"
```

---

## Development History

| Phase | Status | What Was Built |
|:--|:--|:--|
| Phase 0 | Done | Competency taxonomy v1.3 (121 areas), knowledge library, company mapping |
| Phase 1 | Done | People library (21 profiles), service routing (40 entries), 3 recipes |
| Phase 2 | Done | RIU classification, cost enrichment, repo cleanup |
| Phase 3 | Done | Integrity engine, audit system, regression/SLO, drift detection, 75 recipes, 183 knowledge entries, override registry, governance decision contract |
| Phase 4 | Done | Wiki governance pipeline, deterministic compiler, peers-bus voice interface, multi-agent coordination bus |
| Phase 5 | Done | Hybrid retrieval engine (FTS5 + vector + keyword, reciprocal rank fusion), Voice Hub with taxonomy-grounded responses, multi-agent voice interface (5 agents, 4 languages) |
| Phase 6 | Active | Perplexity Sonar gateway (sanitization, caching, rate limiting, audit), vertical knowledge packs, SDK for Humans thesis |

---

## Connected Systems

Palette is the intelligence layer in a three-system flywheel:

- **[Mission Canvas](mission-canvas/)** — Voice-first execution platform. Speak a question, get Palette intelligence back with coaching signals and workspace health.
- **[Enablement](https://github.com/pretendhome/enablement)** — Competency-based developer education and certification built on Palette's knowledge architecture.

Doing teaches, learning improves doing, both feed the intelligence layer.

---

## Origin

Palette was not generated from a prompt. It was distilled from 8 years of knowledge engineering at Amazon and 250+ enterprise AI enablement sessions reaching 20,000+ users annually. The 121 competency areas emerged from real questions asked by real practitioners — CIOs, data scientists, ML engineers, solutions architects — across every major industry vertical. The knowledge library was systematically built through iterative research, source verification, and evidence tiering over 12 months.

The comparative linguistics foundation (MA, Université Paris-Sorbonne) directly informed the architecture: mapping natural language to structured competency is the same discipline as intent classification — utterance → intent → slot → action becomes question → competency area → knowledge entry → governed assessment.

## Built By

**The operator** — 12+ years at Amazon/AWS. Comparative linguistics background. Knowledge architecture, AI enablement systems, competency frameworks, and assessment design. Built Palette to solve the problem of structuring what people need to know about AI, measuring whether they know it, and keeping it current as capabilities evolve — through intelligent automation, not headcount.

---

<div align="center">

*Your judgment compounds here.*

</div>
