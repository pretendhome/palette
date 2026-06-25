# Palette

A Structured Knowledge Harness (SKH) that organizes information by problem pattern for LLM consumption. 131 taxonomy nodes classify every incoming problem before retrieval happens. The taxonomy determines what the model sees. The evidence tiers determine what the model can trust. The integrity engine proves the system is consistent.

> **"What does the model need from the system to do its best work?"**

## Why This Exists

Most retrieval systems search first and hope the model can figure out what's relevant. Palette classifies first, then retrieves within the classified scope. The taxonomy does the planning. The model does the reasoning. They never compete.

The design principle: the single largest quality improvement in a knowledge retrieval system is often a taxonomy reclassification — restructuring how information is organized — not a model change, not an algorithm change. The architecture IS the intervention.

## Six Layers — What Each One Does and Why It Can't Be Collapsed

| Layer | Artifacts | Role | Why It's Separate |
|-------|-----------|------|-------------------|
| **Taxonomy** | 131 RIUs | Classify problems → solution categories | The INDEX. Without it, retrieval degrades to semantic search across 203 entries. |
| **Knowledge Library** | 203 entries, 610 cross-refs | Evidence-tiered answers | The ANSWERS. The taxonomy classifies. The library answers. Different data, different update cycle. |
| **Buy-vs-Build** | 71 recipes, 43 profiles | Service selection with cost data | The ROUTING. Knowledge says what's true. Routing says what to use and what it costs. |
| **People Signals** | 21 profiles, 43 signals | Practitioner credibility tracking | The TRUST MAP. Who is saying what, with what authority. |
| **Agents** | 13 with maturity tracking | Specialized execution roles | The WORKFORCE. Each agent has hard constraints. They promote through reliability, not configuration. |
| **Integrity Engine** | 8 checks, 7 SLOs | Cross-layer consistency proof | The IMMUNE SYSTEM. Catches drift, orphans, and broken cross-references automatically. |

### Taxonomy — 131 Reusable Intelligence Units

Each RIU encodes: problem pattern, execution intent, classification (internal-only, service-routed, or both), related RIUs, failure modes, and difficulty tier. This is the routing engine — it determines what knowledge and services are relevant before retrieval fires.

### Knowledge Library — 203 entries, evidence-tiered

202 of 203 entries cite sources. Evidence hierarchy: Tier 1 (direct AI company publications), Tier 2 (NIST, EU AI Act, ISO, peer-reviewed), Tier 3 (validated open source, >500-star GitHub). 610 cross-references link entries to taxonomy nodes.

### Buy-vs-Build — 71 recipes, 43 service profiles

Each recipe includes: provider, quality tier, cost data, integration complexity, and when to use it. Each routing profile maps a classified problem to specific services with alternatives. 112/112 routing↔recipe consistency verified.

### Agents — 13 specialized with maturity tracking

| Agent | Role | Maturity |
|-------|------|----------|
| resolver | Intent classification → RIU routing | WORKING |
| researcher | External research via Perplexity | WORKING |
| narrator | Evidence-based narrative | WORKING |
| health | System integrity (8 sections) | PRODUCTION |
| total-health | Cross-layer audit (13 sections) | WORKING |
| remediation | Automated fix proposals | WORKING |
| architect | System design, tradeoff evaluation | Design spec |
| builder | Implementation within bounded spec | Design spec |
| debugger | Failure diagnosis, minimal repair | Design spec |
| validator | Plan assessment, GO/NO-GO verdicts | Design spec |
| monitor | Signal monitoring, anomaly detection | Design spec |
| orchestrator | Workflow routing between agents | Design spec |
| business-plan-creation | Multi-agent business plan workflow | Design spec |

Maturity model: UNVALIDATED (human-in-loop) → WORKING (autonomous with review, 10+ successes) → PRODUCTION (fully autonomous, 50+ impressions, <5% failure). Agents promote through measured reliability. They demote on repeated failure.

### Integrity Engine — Structural Proof

```
$ python3 -m scripts.palette_intelligence_system.integrity --checks-only

✓ Taxonomy↔Classification: 131/131
✗ Classification↔Routing: 40/43 (3 pending)
✓ Routing↔Recipe: 112/112
✓ Signals↔Taxonomy: 33/33
✓ Knowledge↔Taxonomy: 610/610
✗ Orphan recipes: 70/71 (1 orphan)
✓ Orphan signals: 43/43
✓ People↔Signals: 20/20
```

6/8 passing. The 2 failures are known and tracked. The integrity engine catches them automatically — that's the point.

### The Traverse Engine

Query any competency area for a structured assessment:

```
$ python3 -c "
from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.traverse import traverse
print(traverse(load_all(), riu_id='RIU-082'))
"

RIU-082 — LLM Safety Guardrails
Classification: both
Recommendation: primary guardrail service (tier_1, usage-based pricing)
Alternatives: adversarial defense service, open-source validator
Knowledge: 9 entries | Completeness: 85/100
```

## Key Design Choices

**Taxonomy-first, not embedding-first.** The RIU determines what knowledge to surface. This prevents the failure mode where high cosine similarity returns the right topic but the wrong answer.

**Evidence tiers are a quality signal, not metadata.** Recommendations cite Tier 1 evidence. An engineer can grep the citations and verify.

**Glass-box architecture.** Every routing decision traces from problem → taxonomy → knowledge → recommendation with citations. No black boxes.

**Retrieval ≠ Authorization.** Content retrieved by relevance, filtered by permission BEFORE entering the context window.

**Multi-agent relay model.** Five agents built this system in parallel. Each finds different classes of problems:
- Codex sees the problem behind the problem
- Kiro ships the first working version fast
- Claude finds the bugs and finishes
- Gemini executes under governed task loops
- Mistral catches tone and user experience

The governance pipeline is the coordination. Agent differences are the specialization.

## Design Lineage

The patterns here — taxonomy-first classification, cross-source normalization, evidence tiering, integrity validation across layers — come from working on large-scale knowledge graphs and enterprise knowledge retrieval systems. The comparative linguistics foundation (mapping natural language to structured competency) directly informed the architecture: intent classification follows the same structure as utterance → intent → slot → action. In Palette, that becomes question → competency area → knowledge entry → governed assessment.

## Relationship to Mission Canvas

Palette and [Mission Canvas](https://github.com/pretendhome/mission-canvas) are two implementations of the Structured Knowledge Harness category:

- **Palette** organizes knowledge ABOUT a domain — what we know, how confident we are, where it came from. The library.
- **Mission Canvas** governs how a model INTERACTS with knowledge in real time — what the model should see, what it should never see, and what we learned. The workflow.

They share architectural principles but operate independently. Together, they demonstrate that the most impactful intervention in AI system quality is not a better model — it's a better information architecture.

## Architecture

```
palette/
├── core/                    # Governance tiers (immutable rules)
├── taxonomy/releases/v1.3/  # 131 RIUs mapping problems to solutions
├── knowledge-library/v1.4/  # 203 entries with evidence tiers
├── buy-vs-build/
│   ├── integrations/        # 71 integration recipes
│   ├── service-routing/     # 43 routing profiles
│   └── people-library/      # 21 profiles, 43 signals
├── agents/                  # 13 specialized with maturity tracking
├── skills/                  # 7 domain frameworks (talent, education, retail-ai, travel, enablement, lenses, tax)
├── scripts/                 # Integrity, audit, regression, drift, traverse
├── lenses/                  # 33 reasoning overlays
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

*Generated by the Palette narrator agent (WORKING, Tier 2). Claims cite evidence from the system's own layers.*

## License

Private — all rights reserved.
