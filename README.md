# Palette

A knowledge architecture that organizes information by problem pattern — not by document, topic, or folder. 121 problem-solution taxonomies (RIUs) route any AI/ML question to the right combination of evidence-tiered knowledge and external services before a model reasons about it.

## Why This Exists

Most knowledge systems organize information for human browsing: folders, tags, search bars. LLMs don't browse. They need structured context: what problem is this, what do we already know about it, what's the evidence quality, what are the failure modes, and what should come next.

Palette answers those questions through six layers:

1. **Taxonomy** — 121 RIUs mapping problems to solution categories. The routing engine.
2. **Knowledge Library** — 176 entries, 565 citations, zero unsourced claims. Evidence-tiered: Tier 1 (Google/Anthropic/AWS/Meta), Tier 2 (NIST/EU/peer-reviewed), Tier 3 (>500-star GitHub).
3. **Buy-vs-Build** — 75 integration recipes with service routing across 106 services. Cost data, quality tiers, integration specs.
4. **People Signals** — 21 tracked practitioners and influencers with signal quality ratings and market positions.
5. **Agents** — 12 specialized agents with maturity tracking (UNVALIDATED → WORKING → PRODUCTION). Automatic demotion on repeated failures.
6. **Integrity Engine** — 8 consistency checks, 7 SLOs, regression detection, terminology drift tracking. Structural proof the system is healthy.

## Key Design Choices

**Taxonomy-first, not embedding-first.** Problems are classified before retrieval. The RIU determines what knowledge to surface. This prevents the failure mode where high cosine similarity returns the right topic but the wrong answer.

**Evidence tiers.** Every knowledge entry cites sources. No unsourced claims. The evidence hierarchy is explicit: Tier 1 (direct AI company publications), Tier 2 (NIST, EU AI Act, peer-reviewed), Tier 3 (validated open-source frameworks). Human experts are ground truth — but they don't scale. This library does.

**Retrieval ≠ Authorization.** Content is retrieved by relevance, then filtered by permission BEFORE entering the model's context window. Once a secret is in the context, it has already leaked.

**Glass-box architecture.** Every decision is transparent, inspectable, and explainable. No black boxes. Every routing decision traces from problem → taxonomy → knowledge → recommendation with citations.

**Multi-agent relay model.** Five agents (Claude, Kiro, Codex, Gemini, Mistral) work the same codebase in parallel. Each finds different classes of problems. The relay model emerged from evidence, not theory:
- Codex sees the problem behind the problem (classification vs matching)
- Kiro ships the first working version fast
- Claude finds the bugs and finishes
- Gemini executes under governed task loops
- Mistral catches tone and user experience

Specialization and coordination co-evolve. The governance pipeline is the coordination. Agent differences are the specialization. Neither works without the other.

## Numbers

| Metric | Value |
|--------|-------|
| Competency areas (RIUs) | 121 (81 internal, 40 service-routed) |
| Knowledge entries | 176 with 565 citations |
| Integration recipes | 75 |
| Service routing | 106 services across 40 profiles |
| People signals | 21 profiles, 33 tools tracked |
| Agents | 12 specialized with maturity tracking |
| Consistency checks | 8/8 passing |
| SLOs | 7/7 passing |
| Traverse health | 121/121 healthy |
| Knowledge coverage | 176/176 (100%) |

## The Traverse Engine

Query any competency area and get a structured assessment: recommendation, alternatives, cost data, knowledge citations, and completeness score.

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
Alternatives:
  - Lakera Guard (tier_1, free 10K req/month, Pro $99/month)
  - Guardrails AI (tier_1, OSS free, Pro ~$50/month)
Knowledge support: 9 entries
Completeness: 85/100
```

Every service-routed competency area (40/40) returns a recommendation with alternatives, cost data, and evidence citations.

## The Integrity Engine

Structural proof that the system is healthy. Not assertions — checks.

```bash
python3 -m scripts.palette_intelligence_system.integrity --checks-only   # 8/8 checks
python3 -m scripts.palette_intelligence_system.audit_system              # Audit with severity
python3 -m scripts.palette_intelligence_system.regression --check        # Regression baseline
python3 -m scripts.palette_intelligence_system.drift                     # Terminology drift
python3 -m scripts.palette_intelligence_system.para_decision             # Governed ship/block decision
```

The Monitor chains all checks and outputs a governed decision:

```
Decision: ship_with_risks
Accepted risks:
  - LINK_MISSING_PEOPLE_SIGNALS: 28 RIUs without people signal coverage
Required actions:
  - Expand people signal crossrefs for uncovered both-classified RIUs
```

## Governance

```
Tier 1 — Immutable rules. Core team vote required to change.
Tier 2 — Reviewed decisions. Human approval required.
Tier 3 — Automated observations. System applies and logs.
```

Every decision classified as ONE-WAY DOOR (irreversible, requires human review) or TWO-WAY DOOR (reversible, can proceed). The system enforces this distinction — it's not a guideline.

## Architecture

```
palette/
├── core/                    # Governance tiers (immutable rules, assumptions, decisions)
├── taxonomy/releases/v1.3/  # 121 RIUs mapping problems to solution categories
├── knowledge-library/v1.4/  # 176 entries with evidence tiers (565 citations)
├── buy-vs-build/
│   ├── integrations/        # 75 integration recipes
│   ├── service-routing/     # 106 services, 40 routing profiles
│   └── people-library/      # 21 profiles, 33 tools tracked
├── agents/                  # 12 specialized agents with maturity tracking
├── skills/                  # 6 validated domain frameworks
├── scripts/                 # Integrity, audit, regression, drift, traverse
├── lenses/                  # 26 role-based reasoning overlays
├── peers/                   # Governed multi-agent message bus
├── voice/                   # Voice evaluation workbench + hub
├── sdk/                     # Agent SDK (Python)
└── .steering/               # Per-agent context (Claude, Codex, Kiro, Gemini, Mistral)
```

## Connected Systems

Palette is the knowledge architecture. Two systems build on it:

- **[Mission Canvas](https://github.com/pretendhome/mission-canvas)** — A governed pipeline that restructures how models interact with knowledge. 9-step pipeline, 174 nodes, pre-reasoning governance.
- **[Enablement](https://github.com/pretendhome/enablement)** — Learning paths built FROM the knowledge architecture. The taxonomy determines what to teach. The evidence tiers determine what sources to use. The assessment rubric maps to each RIU's success conditions.

## Origin

Palette was distilled from 8 years of knowledge engineering at Amazon and 250+ enterprise AI enablement sessions reaching 20,000+ users annually. The 121 competency areas emerged from real questions asked by real practitioners — CIOs, data scientists, ML engineers, solutions architects — across every major industry vertical. The knowledge library was systematically built through iterative research, source verification, and evidence tiering.

The comparative linguistics foundation (MA, Université Paris-Sorbonne) directly informed the architecture: mapping natural language to structured competency is the same discipline as intent classification — utterance → intent → slot → action becomes question → competency area → knowledge entry → governed assessment.

## License

Private — all rights reserved.
