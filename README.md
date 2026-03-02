<div align="center">

# Palette

### An Applied Intelligence Toolkit for Forward Deployed Engineers

One conversational interface that knows your business, routes any problem to the best service at the lowest cost, and delivers a governed outcome — not just an answer.

---

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)]()
[![Integrity](https://img.shields.io/badge/integrity-8%2F8_passing-brightgreen)]()
[![SLOs](https://img.shields.io/badge/SLOs-7%2F7_passing-brightgreen)]()
[![RIUs](https://img.shields.io/badge/RIUs-117-blue)]()
[![Knowledge](https://img.shields.io/badge/knowledge-498_entries-blue)]()
[![Recipes](https://img.shields.io/badge/recipes-69-blue)]()
[![License](https://img.shields.io/badge/license-private-lightgrey)]()

</div>

---

## What Is Palette?

Palette is an applied intelligence toolkit that turns natural language problems into governed, evidence-backed decisions. It maps 117 validated problem-solution pairs across 6 data layers, routes to the cheapest and best service for each task, and proves its own structural health at every step.

**The thesis**: instead of configuring pipelines and picking models, you describe your problem. The system knows your context, routes to the right tool at the right price, and delivers a governed outcome with evidence at every step.

### Key Capabilities

- **Traversal Engine** — Query any problem, get a structured decision packet: top recommendation, ranked alternatives, cost data, knowledge citations, completeness score
- **Integrity Engine** — 8 consistency checks across 6 data layers, catching orphans, missing links, and ambiguous mappings in real time
- **Governance Layer** — Every decision classified as `ship` / `ship_with_risks` / `ship_with_convergence` / `block` with explicit reversibility gates
- **Multi-Agent Relay** — 7 specialized agents with promotion/demotion logic and explicit handoff contracts

---

## System Summary

<div align="center">

| Component | Specification |
|:--|:--|
| Problem-Solution Pairs (RIUs) | 117 (80 internal, 37 service-routed) |
| Knowledge Entries | 498 with verified source citations |
| Integration Recipes | 69 (auth, endpoints, cost, quality tier) |
| Service Routing | 106 services across 40 routing profiles |
| People Signals | 21 profiles, 33 tools tracked |
| Override Registry | 19 explicit mappings for ambiguous cases |
| Agents | 7 specialized (research, architecture, build, debug, narrative, validation, monitoring) |
| Active Projects | 9 (retail, talent, education, finance, dev) |

</div>

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Natural Language In                       │
├─────────────────────────────────────────────────────────────┤
│  Cory (Resolver)  →  Coordination Pipeline  →  Traverse     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  6 Data Layers                                       │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │    │
│  │  │Taxonomy  │ │Routing   │ │Recipes   │            │    │
│  │  │117 RIUs  │ │106 svcs  │ │69 specs  │            │    │
│  │  └──────────┘ └──────────┘ └──────────┘            │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │    │
│  │  │Knowledge │ │Signals   │ │Overrides │            │    │
│  │  │498 entries│ │21 people │ │19 maps   │            │    │
│  │  └──────────┘ └──────────┘ └──────────┘            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Integrity Layer                                     │    │
│  │  Integrity → Audit → Regression → Drift → Para      │    │
│  │  8/8 checks   1 finding  7/7 SLOs   15 clusters     │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                    Governed Action Out                        │
│         ship │ ship_with_risks │ ship_with_convergence │ block│
└─────────────────────────────────────────────────────────────┘
```

### Three Tiers

**Tier 1: Core Prompt** — Immutable rules. Convergence before execution, glass-box reasoning, ONE-WAY DOOR vs TWO-WAY DOOR classification.

**Tier 2: Agents** — 7 specialized agents that earn autonomy through measured performance. UNVALIDATED → WORKING → PRODUCTION. Automatic demotion on repeated failures.

**Tier 3: Integrity System** — Structural proof that the system is healthy. Consistency checks, audit findings, regression detection, SLO enforcement, terminology drift tracking.

---

## Current Status

<div align="center">

| Metric | Value | Threshold |
|:--|:--|:--|
| Consistency checks | **8/8 passing** | 8/8 |
| SLO compliance | **7/7 passing** | 7/7 |
| Regressions | **0** | 0 |
| Improvements tracked | **44** | — |
| Audit findings | **1** (medium, non-blocking) | 0 critical |
| Risk score | **2** (down from 14) | — |
| Avg completeness | **81.8/100** | ≥ 40 |
| Routing↔Recipe match | **106/106** | ≥ 95% |
| Knowledge coverage | **498/498** (100%) | ≥ 50% |
| Terminology drift clusters | **15** (3 high, 9 medium, 3 low) | — |
| Traverse health | **117/117 healthy** | — |

</div>

---

## Traverse Engine

The traverse engine is the read path of the system. Query any RIU and get a structured decision packet:

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

Every both-classified RIU (37/37) returns a recommendation with alternatives, cost data, and evidence citations.

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

The Para decision engine chains all four checks and outputs a governed decision:

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
| **Argentavis** (Argy) | Research | Check internal libraries first, then external sources |
| **Tyrannosaurus** (Rex) | Architecture | Design with explicit tradeoff clarity |
| **Therizinosaurus** (Theri) | Build | Scope-bounded implementation |
| **Velociraptor** (Raptor) | Debug | Root cause analysis, fix verification |
| **Yutyrannus** (Yuty) | Narrative | Evidence-based GTM, no speculation |
| **Ankylosaurus** (Anky) | Validation | Quality gates, test coverage |
| **Parasaurolophus** (Para) | Monitoring | Governance decisions, block routing |

**Maturity Model**: Agents earn trust through performance.
- **UNVALIDATED** → 10 successes → **WORKING** → 50 runs <5% fail → **PRODUCTION**
- 2 failures in 10 runs → automatic demotion

**Block Routing**: When Para blocks a decision, it routes to the right agent:
- Self-inflicted bug → Raptor
- Architecture gap → Rex
- Research gap → Argy

---

## Project Structure

```
palette/
├── core/                               # Governance tiers (visible on GitHub)
│   ├── palette-core.md                 # Tier 1 — Immutable rules
│   ├── assumptions.md                  # Tier 2 — Experimental assumptions
│   └── decisions-prompt.md             # Tier 3 — Decision log policy
├── taxonomy/releases/v1.3/             # 117 RIUs (problem-solution pairs)
├── knowledge-library/v1.4/             # 498 entries with source citations
├── company-library/
│   ├── integrations/                   # 69 integration recipes
│   ├── service-routing/v1.0/           # 106 services, 40 routing profiles
│   ├── people-library/v1.1/            # 21 profiles, 33 tools tracked
│   └── PALETTE_INTELLIGENCE_SYSTEM_v1.0.md
├── agents/
│   ├── argentavis/                     # Argy — Research
│   ├── rex/                            # Rex — Architecture
│   ├── therizinosaurus/                # Theri — Build
│   ├── velociraptor/                   # Raptor — Debug
│   ├── yutyrannus/                     # Yuty — Narrative
│   ├── ankylosaurus/                   # Anky — Validation
│   └── parasaurolophus/                # Para — Monitoring
├── scripts/palette_intelligence_system/
│   ├── integrity.py                    # 8 consistency checks across 6 layers
│   ├── audit_system.py                 # Severity-ranked findings
│   ├── regression.py                   # Baseline snapshots + 7 SLOs
│   ├── drift.py                        # Terminology inconsistency detection
│   ├── para_decision.py                # Governance decision engine
│   ├── traverse.py                     # Structured decision packets
│   └── test_*.py                       # 60 tests, all passing
├── docs/
│   ├── architecture/                   # E2E system diagrams (Mermaid)
│   ├── audits/                         # Hardening reviews
│   └── PARA_DECISION_CONTRACT.md       # Governance spec
└── implementations/                    # Live projects using the toolkit
    ├── retail/                         # Small business (Rossi Store)
    ├── talent/                         # Interview prep (Glean, Gap)
    ├── education/                      # Resume optimization (Lenovo EKM)
    └── ...                             # 9 active projects
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
| Phase 0 | Done | Taxonomy v1.3 (117 RIUs), knowledge library, company mapping |
| Phase 1 | Done | People library (21 profiles), service routing (40 entries), 3 recipes |
| Phase 2 | Done | RIU classification, cost enrichment, repo cleanup |
| Phase 3 | Done | Integrity engine, audit system, regression/SLO, drift detection, 49 recipes, 116 knowledge entries, override registry, Para decision contract |
| Phase 4 | Next | Decision quality audit, operational monitoring, contradiction ledger |

---

## Built By

**Mical Neill** — 11 years at Amazon/AWS. Knowledge architecture, AI deployment, GenAI partnerships. Built Palette over 2.5 years to solve the problem of scaling human expertise through governed AI systems.

---

<div align="center">

*Natural language in. Governed action out. Structural proof at every step.*

</div>
