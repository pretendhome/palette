# Palette

A Structured Knowledge Harness (SKH) that organizes information by problem pattern for LLM consumption — not by document, topic, or folder. Every incoming problem is classified through a 131-node taxonomy before retrieval happens. The taxonomy determines what the model sees. The evidence tiers determine what the model can trust. The integrity engine proves the system is consistent. The model starts from a known position on a known map.

## What Is a Structured Knowledge Harness

Most knowledge systems organize information for human browsing: folders, tags, search bars, wikis. Humans navigate with intent and judgment — they scan, filter, and decide what's relevant. LLMs don't browse. They need structured context delivered before reasoning begins: what problem is this, what do we already know, how confident are we, where did it come from, and what should come next.

A Structured Knowledge Harness answers those questions through architecture, not prompting. It reorganizes information so the structure itself guides the model — so the model reasons from a known position instead of a blank context.

Palette and [Mission Canvas](https://github.com/pretendhome/mission-canvas) are two SKH implementations that solve different parts of this problem:

- **Palette** organizes knowledge ABOUT a domain. It answers: *what do we know about this problem, how confident are we, and where did it come from?* Taxonomy → knowledge → services → agents.
- **Mission Canvas** governs how a model INTERACTS with knowledge in real-time. It answers: *given this query, what should the model see, what should it never see, and what did we learn?* Classify → traverse → retrieve → reason → store.

Palette is the library. Mission Canvas is the librarian's governed workflow. Both are needed. Neither replaces the other.

## Why This Architecture Exists

Most retrieval systems search first and hope the model can figure out what's relevant. Palette classifies first, then retrieves within the classified scope. The taxonomy does the planning. The model does the reasoning. They never compete.

The design principle behind this: the single largest quality improvement in a knowledge retrieval system is often a taxonomy reclassification — restructuring how information is organized — not a model change, not an embedding change, not an algorithm change. The architecture IS the intervention.

## Six Layers

Each layer solves a problem the layer above cannot solve alone. They cannot be collapsed.

### 1. Taxonomy — 131 RIUs

131 Reusable Intelligence Units mapping problems to solution categories. Each RIU encodes: problem pattern, execution intent, classification (internal-only, service-routed, or both), related RIUs, and difficulty tier. The taxonomy is the routing engine — it determines what knowledge and services are relevant before retrieval fires.

*Why this can't be collapsed into the knowledge layer*: The taxonomy is the INDEX. Without it, retrieval degrades to semantic search across all 203 knowledge entries — the failure mode where high cosine similarity returns the right topic but the wrong answer.

[Evidence: 131/131 taxonomy↔classification consistency verified — `integrity --checks-only`]

### 2. Knowledge Library — 203 entries, evidence-tiered

202 of 203 entries cite sources; the remaining gap is visible to integrity review. The evidence hierarchy is explicit:
- **Tier 1**: Direct AI company and platform publications
- **Tier 2**: Standards bodies, peer-reviewed (NIST, EU AI Act, ISO)
- **Tier 3**: Validated open-source frameworks (>500-star GitHub)

610 cross-references link knowledge entries to taxonomy nodes.

*Why this can't be collapsed into the taxonomy*: The taxonomy classifies. The knowledge library ANSWERS. A taxonomy node says "this is a guardrails problem." The knowledge entry says "here are the three approaches, their evidence basis, and their tradeoffs."

[Evidence: 203 entries loaded, 610 taxonomy cross-references verified — `loader.load_all()`, `integrity --checks-only`]

### 3. Buy-vs-Build — 71 recipes, 43 service profiles

Service routing with integration recipes. Each recipe includes: provider, quality tier, cost data, integration complexity, and when to use it. Each routing profile maps a classified problem to specific services with alternatives.

*Why this can't be collapsed into the knowledge layer*: Knowledge says what's true. Service routing says what to use. A knowledge entry explains how guardrails work. A service route says which guardrail, validation, or safety service fits the classified problem, with alternatives and cost model where available.

[Evidence: 71 recipes, 43 routing profiles, 112/112 routing↔recipe consistency — `integrity --checks-only`]

### 4. People Signals — 21 profiles, 43 tracked signals

Practitioner and influencer tracking with signal quality ratings and market positions. Maps who is saying what about which technology, with credibility weighting.

[Evidence: 43 signals, 20/20 people↔signals cross-reference — `integrity --checks-only`]

### 5. Agents — 13 specialized with maturity tracking

Each agent has a defined role, hard constraints, and a maturity model:
- **Tier 1 (UNVALIDATED)**: Human-in-loop for every execution
- **Tier 2 (WORKING)**: Autonomous with review (after 10 successes, 0 failures)
- **Tier 3 (PRODUCTION)**: Fully autonomous (after 50 impressions with <5% failure rate)

Agents promote through measured reliability, not configuration. They demote automatically on repeated failures.

| Agent | Role | Status |
|-------|------|--------|
| resolver | Intent classification → RIU | WORKING |
| researcher | Research via Perplexity | WORKING |
| narrator | Evidence-based narrative | WORKING (13/0, this README) |
| health | System integrity (8 sections) | PRODUCTION |
| total-health | Cross-layer audit (13 sections) | WORKING |
| + 8 more | architect, builder, debugger, validator, monitor, orchestrator, business-plan-creation | Various |

[Evidence: 13 agents defined in `agents/`, maturity tracked in each `agent.json`]

### 6. Integrity Engine — 8 consistency checks, 7 SLOs

Structural proof the system is healthy. Not assertions — checks that cross-validate between layers:

```
$ python3 -m scripts.palette_intelligence_system.integrity --checks-only

✓ Taxonomy↔Classification: 131/131
✗ Classification↔Routing: 40/43 (3 new RIUs pending routing)
✓ Routing↔Recipe: 112/112
✓ Signals↔Taxonomy: 33/33
✓ Knowledge↔Taxonomy: 610/610
✗ Orphan recipes: 70/71 (1 orphan)
✓ Orphan signals: 43/43
✓ People↔Signals: 20/20
```

6/8 passing. The 2 failures are known: 3 recently added RIUs awaiting routing entries, and 1 orphan recipe. The integrity engine catches these automatically — that's the point.

[Evidence: output of `integrity --checks-only`, run on 2026-06-24]

## Key Design Choices

**Taxonomy-first, not embedding-first.** Problems are classified before retrieval. The RIU determines what knowledge to surface. This prevents the failure mode where high cosine similarity returns the right topic but the wrong answer.

**Evidence tiers are a quality signal, not decorative metadata.** When the system recommends a service, the recommendation cites Tier 1 evidence (direct vendor documentation), not blog posts. When the knowledge library answers a question, the answer traces to specific sources. An engineer can grep the citations and verify them.

**Glass-box architecture.** Every decision is transparent, inspectable, and explainable. Every routing decision traces from problem → taxonomy → knowledge → recommendation with citations. No black boxes.

**Retrieval ≠ Authorization.** Content is retrieved by relevance, then filtered by permission BEFORE entering the model's context window. Once a secret is in the context, it has already leaked. This distinction matters for any deployment in legal, medical, or financial environments.

**Multi-agent relay model.** Five agents (Claude, Kiro, Codex, Gemini, Mistral) built this system working the same codebase in parallel. Each finds different classes of problems. The relay model emerged from evidence:
- Codex sees the problem behind the problem (classification vs matching)
- Kiro ships the first working version fast
- Claude finds the bugs and finishes
- Gemini executes under governed task loops
- Mistral catches tone and user experience

The governance pipeline is the coordination. Agent differences are the specialization. Neither works without the other.

## The Traverse Engine

Query any competency area and get a structured assessment:

```
$ python3 -c "
from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.traverse import traverse
print(traverse(load_all(), riu_id='RIU-082'))
"

# Example summary of the structured result:
RIU: RIU-082 — LLM Safety Guardrails (Content + Tool Use)
Classification: both
Recommendation: primary guardrail service
  Quality: tier_1 | Cost: usage-based with free filtering tiers
Alternatives:
  - adversarial defense service
  - open-source validator framework
Knowledge support: 9 entries
Completeness: 85/100
```

Every service-routed competency area returns a recommendation with alternatives, cost data, and evidence citations.

## Design Lineage

The architectural patterns in Palette — taxonomy-first classification, cross-source normalization, evidence tiering, integrity validation across layers — come from working on large-scale knowledge graphs and enterprise knowledge retrieval systems. The same discipline that normalizes conflicting data providers into a canonical taxonomy applies to normalizing AI/ML knowledge for LLM consumption.

The comparative linguistics foundation (mapping natural language to structured competency) directly informed the architecture: intent classification follows the same structure as utterance → intent → slot → action. In Palette, that becomes question → competency area → knowledge entry → governed assessment.

## Connected Systems

- **[Mission Canvas](https://github.com/pretendhome/mission-canvas)** — The other SKH. Governed execution loop that restructures how models interact with knowledge in real time. 174 nodes, pre-reasoning classification, structural memory. Shares architectural principles with Palette but operates independently.
- **[Enablement](https://github.com/pretendhome/enablement)** — Learning paths built FROM the knowledge architecture. The taxonomy determines what to teach. The evidence tiers determine what sources to use.

## Architecture

```
palette/
├── core/                    # Governance tiers (immutable rules, assumptions, decisions)
├── taxonomy/releases/v1.3/  # 131 RIUs mapping problems to solution categories
├── knowledge-library/v1.4/  # 203 entries with evidence tiers
├── buy-vs-build/
│   ├── integrations/        # 71 integration recipes
│   ├── service-routing/     # 43 routing profiles
│   └── people-library/      # 21 profiles, 43 signals
├── agents/                  # 13 specialized with maturity tracking
├── skills/                  # 6 active skill domains
├── scripts/                 # Integrity, audit, regression, drift, traverse
├── lenses/                  # 30 reasoning overlays
├── peers/                   # Governed multi-agent message bus
├── voice/                   # Voice evaluation workbench
├── sdk/                     # Agent SDK (Python)
└── .steering/               # Per-agent context (Claude, Codex, Kiro, Gemini, Mistral)
```

## Verify

```bash
# Load and count all layers
python3 -c "
from scripts.palette_intelligence_system.loader import load_all
d = load_all()
print(f'Knowledge: {len(d.knowledge)} | Recipes: {len(d.recipes)} | Routing: {len(d.routing)} | Classification: {len(d.classification)} | Signals: {len(d.signals)}')
"

# Run integrity checks
python3 -m scripts.palette_intelligence_system.integrity --checks-only

# Traverse a competency area
python3 -c "
from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.traverse import traverse
print(traverse(load_all(), riu_id='RIU-082'))
"
```

---

*Generated by the Palette narrator agent (WORKING, Tier 2). Key claims cite evidence from the system's own layers. The integrity output is real, not rounded up.*

## License

Private — all rights reserved.
