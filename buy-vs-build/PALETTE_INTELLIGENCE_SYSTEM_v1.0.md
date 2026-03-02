# Palette Intelligence System (PIS) — Architecture v1.0

**Date**: 2026-02-24
**Status**: DESIGN — implementation in progress
**Research basis**: Web research (2026-02-24) + existing Palette artifact analysis

---

## 1. What This Is

The Palette Intelligence System (PIS) is the market intelligence and service routing layer of Palette. It answers two questions:

1. **"What exists?"** — Which companies/services can accomplish a given type of work (mapped to RIUs)?
2. **"What should I use?"** — Given a task, which service combination is cheapest, best, or most trusted by practitioners?

Long-term goal: become the intelligence layer that lets Palette act as a task router that selects the right external service for any job — including knowing *not* to call an external service when a Palette agent can do it cheaper/better internally.

This is the path toward the SageMaker disruption goal: one agentic interface where users can accomplish any task, with Palette routing to the right tool, model, or agent automatically.

---

## 2. Why This Is Different From Existing Tools

| System | What it routes | What's missing |
|---|---|---|
| OpenRouter / LiteLLM | Between LLM API endpoints | Not task-semantic; no non-LLM services |
| TAAFT / Toolify.ai | AI tool discovery directories | Not for routing; not RIU-mapped; no build-vs-buy |
| LangGraph / CrewAI | Between pre-configured agents | Assumes services already selected |
| SageMaker | ML model deployment on AWS | AWS-locked; no external SaaS services |
| Favikon / Modash | Influencer discovery for marketing | Not technical signal intelligence |

**PIS differentiators**:
- RIU-mapped: what problem pattern does this service solve, not just what category it's in
- Practitioner-weighted: signal strength comes from trusted practitioners, not just SEO
- Build-vs-buy: explicit guidance on when to integrate vs. implement internally
- Non-LLM services: routes to Wispr Flow, Gamma, Lovable — not just LLM providers
- Integration recipes: not just "this service exists" but "here's how to call it"

---

## 3. Five Use Cases (User's Original Vision)

### UC-1: Service Routing Index
"Which service do I use for this task?"

- Input: task description or RIU ID
- Output: ranked list of services with quality/cost/integration data
- Example: RIU-502 (Audio Processing) → [Wispr Flow: high quality, $9/mo, recipe link] [OpenAI Whisper: medium quality, free, already integrated]
- Layer: `service-routing/v1.0/`

### UC-2: Market Gap Analysis
"How many companies solve this? Where are the gaps?"

- Input: RIU ID or use case category
- Output: company density, funding concentration, gap analysis
- Example: RIU-502 has 2 companies → validated market. RIU-503 (Cross-Modal Validation) has 0 → gap
- Layer: `buy-vs-build/v1.0/`
- Already demonstrated in talent-job-search implementation

### UC-3: Integration Discovery
"A new service just launched — should we integrate it?"

- Input: company name or GitHub URL
- Output: what RIUs it covers, signal_strength from influencer network, build-vs-buy score
- Layer: people-library signals → buy-vs-build → service-routing
- Example: OpenClaw integrated (documented in research/openclaw_vs_palette_analysis.md); Kimi 2.5 integrated

### UC-4: Task Cost Optimization (SageMaker Goal)
"What's the cheapest way to accomplish X right now?"

- Input: task description
- Output: service pipeline with total cost estimate
- Example: "Generate a 2-minute explainer video from a blog post" → Claude (summarize, $0.003) + Gamma (slides, $0.00 free tier) + Seedance Pro (video, TBD)
- Layer: service-routing + integrations + cost-oracle (future)
- Requires: price oracle (UC-4 extension, Phase 2)

### UC-5: People Signal Tracking
"Who is recommending what? What new services should we investigate?"

- Input: people-library monitoring (weekly/monthly cadence)
- Output: new company entries for watch list, updated signal_strength
- Layer: people-library → company-signals crossref → buy-vs-build
- Example: Axelle Malek posts about Seedance 2.0 → Seedance added to ai_video_generation → signal_strength: high (confirmed by 2 practitioners)

---

## 4. Additional Ideas (Research-Surfaced)

### UC-6: Benchmark Integration
Pull quality data from Artificial Analysis (artificialanalysis.ai) and Epoch AI (epoch.ai) for LLM-based services. When routing "code generation", compare services on benchmark scores *and* influencer recommendations, not just one signal.

### UC-7: Price Oracle
Automated pricing scrape from published pricing pages. OpenRouter already does this for LLMs. Extend to SaaS pricing pages. Enables the "cheapest capable service" calculation in UC-4.

### UC-8: GitHub Intelligence
Influencer says "this GitHub account is amazing" → Researcher analyzes: stars, forks, recent commits, license, dependency count, API exposure. Adds to `open-source-services/` section alongside commercial entries. Pipeline:
```
Influencer rec → Researcher GitHub analysis → open-source-services entry → RIU mapping → service-routing entry
```

### UC-9: Integration Health Monitoring
Monitor (Monitor agent) watches integrated services. If Wispr Flow API degrades, automatically route to Whisper fallback. This is the reliability layer for UC-1. Requires: Monitor integration with service-routing.

### UC-10: Routing Outcome Tracking
Log which routing decisions led to good outcomes. Feed back into routing weights over time. This is the learning layer — turns PIS from a static index into a reinforcement-learning-style optimizer. Long-term, Phase 3+.

---

## 5. Architecture: Four Layers

```
fde/palette/
└── buy-vs-build/
    │
    ├── PALETTE_INTELLIGENCE_SYSTEM_v1.0.md   ← This document
    │
    ├── v1.0/                                  ← LAYER 1: Company-RIU Index
    │   ├── palette_company_riu_mapping_v1.0.yaml
    │   ├── README.md
    │   └── COMPANY_INTEL_PLAYBOOK.md
    │
    ├── people-library/                         ← LAYER 2: Signal Network
    │   └── v1.0/
    │       ├── people_library_v1.0.yaml         ← 18 profiles (complete ✓)
    │       ├── README.md
    │       └── people_library_company_signals_v1.0.yaml  ← Crossref (in progress)
    │
    ├── service-routing/                         ← LAYER 3: Service Routing Index (new)
    │   └── v1.0/
    │       ├── service_routing_v1.0.yaml         ← RIU → [services ranked by quality/cost]
    │       └── README.md
    │
    └── integrations/                            ← LAYER 4: Integration Recipes (new)
        ├── perplexity-mcp/                      ← Complete ✓
        ├── wispr-flow/                          ← Planned
        ├── gamma-api/                           ← Planned
        └── openrouter/                          ← Planned (LLM routing gateway)
```

---

## 6. Data Flow

```
profiles-raw.txt (LinkedIn scrape)
  → people_library_v1.0.yaml        (LAYER 2: who recommends what)
  → company_signals_v1.0.yaml       (LAYER 2 → LAYER 1: tool → RIU mapping)
  → palette_company_riu_mapping.yaml (LAYER 1: market validation)
  → service_routing_v1.0.yaml       (LAYER 3: routing decisions)
  → integration recipes              (LAYER 4: execution)

Perplexity enrichment (pending)
  → updates people-library (stubs → active)
  → updates buy-vs-build (funding, capabilities validated)
  → updates service-routing (quality scores validated)

Benchmark feeds (future)
  → quality_scores.yaml              (Layer 3 enrichment)

Price oracle (future)
  → pricing.yaml                     (Layer 3 enrichment)
```

---

## 7. Schema Standards

### Company entry schema (Layer 1)
```yaml
- name: "Company Name"
  founded: YYYY
  funding_stage: "Series X"
  funding_amount: "$XM"
  agentic_native: true/false
  use_case: "what it does"
  source: "url"
  people_library_signal:          # NEW FIELD (from people-library crossref)
    recommended_by: ["PERSON-001", "PERSON-002"]
    signal_strength: high | medium | low | unvalidated
    note: "why practitioners use it"
  palette_note: "how this relates to Palette"
```

### Service routing entry schema (Layer 3)
```yaml
- riu_id: RIU-XXX
  riu_name: "RIU Name"
  services:
    - name: "Service Name"
      quality_tier: tier_1 | tier_2 | tier_3
      cost_model: free | usage_based | subscription | enterprise
      cost_estimate: "$X per unit"
      integration_recipe: "integrations/service-name/"
      palette_integration_status: integrated | available | planned | evaluate
      people_library_signal_strength: high | medium | low | none
      build_vs_buy: adopt_pattern | integrate | defer
      notes: "..."
```

### Signal crossref entry schema (Layer 2 crossref)
```yaml
- tool: "Tool Name"
  company_url: "url"
  riu_primary: RIU-XXX
  riu_secondary: [RIU-YYY, RIU-ZZZ]
  signal_tier: 1 | 2 | 3
  recommenders: ["PERSON-001", "PERSON-002"]
  aggregate_signal_strength: high | medium | low
  company_library_status: mapped | missing | cross_listed
  palette_action: integrate | evaluate | monitor | skip
```

---

## 8. Build Roadmap

### Phase 0 (this session) — Foundation
- [x] people_library_v1.0.yaml (18 profiles, 5 clusters)
- [ ] people_library_company_signals_v1.0.yaml (crossref)
- [ ] service_routing_v1.0.yaml (schema + seed entries)
- [ ] Update Researcher to reference people-library

### Phase 1 — Enrichment
- [ ] Run Perplexity queries for all 18 profiles
- [ ] Enrich 4 stubs (Filip Mark, Pablo Palafox, Lazar Jovanovic + 1)
- [ ] Promote top 5 watch list candidates to full profiles
- [ ] Update buy-vs-build with validated data

### Phase 2 — Service Routing
- [ ] Complete service_routing_v1.0.yaml for all high-signal RIUs
- [ ] Add cost estimates (manual first, oracle later)
- [ ] Build 3 integration recipes (Wispr Flow, Gamma, OpenRouter)
- [ ] Test routing decisions against real tasks

### Phase 3 — Automation
- [ ] Automated Perplexity enrichment pipeline (scheduled)
- [ ] GitHub intelligence module (Researcher extension)
- [ ] Price oracle (pricing page scraping)
- [ ] Benchmark integration (Artificial Analysis API or scrape)

### Phase 4 — Query Interface
- [ ] PIS query agent (Researcher variant or new agent)
- [ ] "What service for this task?" query handler
- [ ] "What's cheapest?" optimizer
- [ ] Routing outcome logging (Monitor integration)

---

## 9. Relationship to Existing Palette Artifacts

| Artifact | Feeds Into | Fed By |
|---|---|---|
| `taxonomy/v1.3/` | service-routing (RIU IDs) | — |
| `buy-vs-build/v1.0/` | service-routing (company data) | people-library signals |
| `people-library/v1.0/` | buy-vs-build signals | profiles-raw.txt |
| `knowledge-library/v1.2/` | Researcher search (internal) | — |
| `agents/researcher/` | research queries | people-library, knowledge-library, Perplexity |
| `service-routing/v1.0/` | Researcher routing decisions | buy-vs-build, people-library signals |

---

## 10. Market Position (Long-Term)

What PIS builds toward, with Palette's convergence-first framework on top:

```
User: "I need to analyze 50 customer interviews and build a demo presentation"

Palette Orchestrator:
  → RIU-200 (Customer Problem Narrative): route to Granola + Claude
  → RIU-413 (Customer Value Demo Creation): route to Gamma
  → Service routing: Granola (free tier) + Claude Sonnet 4.6 ($0.003/req) + Gamma (free tier)
  → Estimated cost: $0.15 for 50 interviews
  → Integration recipes: load granola-api, claude-api, gamma-api
  → Execute with human approval gates at ONE-WAY DOOR decisions

vs. SageMaker:
  → AWS-only
  → LLM models only
  → No convergence-first framework
  → No build-vs-buy guidance
  → No practitioner signal weighting
```

This is not built in a day. But the architecture is clear and the foundation (people-library, buy-vs-build, taxonomy) is already laid.

---

## Changelog

**v1.0** (2026-02-24):
- Initial architecture document
- Research basis: OpenRouter, LiteLLM, LangGraph, TAAFT, Favikon comparative analysis
- 5 use cases defined (user's vision)
- 5 additional ideas (research-surfaced)
- 4-layer architecture proposed
- Schema standards defined
- Phase 0-4 build roadmap
