# Palette External Reality Layer Spec

Date: 2026-04-21
Author: Codex, with operator direction from Mical
Status: Proposed system blueprint
Scope: People Library, Company Index, service routing, recipes, RIUs, agents, wiki, and human enablement

## One-Sentence Thesis

Palette needs an External Reality Layer: a market-sensing nervous system that mirrors the internal ontology, detects movement in the outside AI ecosystem, and turns weak signals from people, companies, funding, product launches, and practitioner behavior into governed decisions about what to learn, research, buy, build, integrate, monitor, or ignore.

## Why This Exists

Palette already has a strong internal system:

- RIUs define the problem space.
- The Knowledge Library stores validated knowledge.
- Service routing maps problems to options.
- Recipes prove integration reality.
- Agents act on structured contracts.
- Skills and learning paths teach humans the same ontology.

But the outside world moves faster than static knowledge:

- Companies pivot, get acquired, decay, or explode.
- New categories appear before the taxonomy has names for them.
- Tool recommendations spread through practitioner networks before formal reports catch up.
- Funding and valuation can indicate momentum, but also hype.
- Open-source frameworks can become de facto standards before vendors mature.
- Regulatory, safety, and enterprise adoption signals change what should be recommended.

The current People Library and Company Index already point toward the answer. They are not just auxiliary data files. They are the beginning of Palette's external sensory apparatus.

The missing move is to make that role explicit.

## Core Concept

Palette needs two mirrored systems:

1. Internal Ontology
- What Palette believes about AI adoption problems.
- What it knows.
- What it can do.
- What it can teach.
- What it can integrate.

2. External Reality Layer
- What the market is proving.
- What practitioners are actually using.
- Which companies are rising, decaying, or pivoting.
- Which categories are emerging.
- Which RIUs are heating up.
- Which recommendations need refresh, demotion, or escalation.

The internal system gives Palette coherence.
The external system gives Palette contact with reality.

Together they create convergence.

## The Big Design Shift

The People Library should no longer be understood as "influencer tracking."
The Company Index should no longer be understood as "vendor inventory."

They should become a structured signal system:

- People are sensors.
- Companies are options.
- RIUs are demand.
- Recipes are reality.
- Agents are actuators.
- Human learning paths are the internalization layer.

This creates a closed loop:

```text
People signal
  -> Company option
  -> RIU demand
  -> Recipe proof
  -> Agent action
  -> Outcome feedback
  -> Signal recalibration
```

## System Role In Palette

The External Reality Layer answers questions the internal system cannot answer alone:

- Is this recommendation still current?
- Is this tool rising because practitioners actually use it, or only because it raised money?
- Is this category missing from the taxonomy?
- Is this company ready for integration, evaluation, monitoring, or archival?
- Is Palette over-indexed on one ecosystem?
- Which external shifts should trigger new skills, recipes, lenses, or wiki pages?
- Which people provide durable signal versus fast-decaying noise?
- Where does external reality contradict Palette's internal assumptions?

## Design Principles

### 1. Signals Are Not Truth

A person recommending a tool is not proof the tool works.
A company raising money is not proof the category matters.
A valuation is not a recommendation.
A founder claim is not external validation.

Every signal must carry:

- source type
- recency
- bias
- durability
- validation state
- relationship to RIUs
- actionability for Palette

### 2. Freshness Is Domain-Specific

AI video model recommendations can decay in weeks.
Enterprise architecture principles can remain useful for years.
Funding data may matter for market momentum but not product quality.
Safety and governance principles may be slow-moving but high-impact.

The system must encode decay rate, not just last-updated.

### 3. People Have Roles, Not Just Names

People should be modeled as instruments in a signal network.

Examples:

- mass adoption sensor
- production engineering sensor
- frontier lab signal
- enterprise buyer signal
- safety / policy signal
- founder roadmap signal
- investor market-map signal
- practitioner proof signal
- derivative content amplifier

This prevents treating Ruben Hassid, Chip Huyen, Dario Amodei, and Olivia Moore as equivalent "people entries."

### 4. Companies Are Decisions Waiting To Happen

Every company in the index should eventually answer:

- Should Palette integrate this?
- Should Palette evaluate this?
- Should Palette monitor this?
- Should Palette ignore this?
- Should Palette archive this?
- Does this company change a build-vs-buy recommendation?
- Does this company expose a taxonomy gap?
- Does this company deserve a recipe?

### 5. Recipes Beat Hype

A company with a working integration recipe is operationally different from a company with market buzz.

Palette should always distinguish:

- market relevance
- practitioner validation
- integration feasibility
- actual Palette adoption

### 6. Contradiction Is Valuable

Conflicts between layers should not be hidden.

Examples:

- People Library says a tool is high-signal, Company Index says it is missing.
- Company Index says active, audit says pivoted.
- Service routing recommends a vendor, but signal network shows decay.
- Recipe exists, but company is stale or acquired.

These contradictions are not bugs only. They are intelligence.

## Architecture

### Layer 1: Signal Sources

Input sources:

- People Library profiles
- People-to-company crossref
- Company Index
- Integration recipes
- Service routing
- Knowledge Library citations
- Funding / acquisition / pivot events
- Product launch notes
- Agent usage logs
- Human operator notes
- Wiki proposal feedback
- External research reports

### Layer 2: Canonical Entities

Required canonical IDs:

- `person_id`
- `company_id`
- `riu_id`
- `recipe_id`
- `signal_id`
- `source_id`
- `category_id`

The most urgent addition is `company_id`, because company naming currently fragments across:

- People Library
- Company signals crossref
- Company Index
- Recipes
- Service routing
- Knowledge Library

### Layer 3: Signal Normalization

All signals should normalize into a common shape:

```yaml
signal_id: "SIG-..."
signal_type: person_recommendation | founder_claim | funding_event | product_launch | practitioner_case | recipe_status | audit_finding | usage_result
source:
  source_id: "SRC-..."
  source_type: primary | practitioner | investor | founder | curator | analyst | vendor | internal
  url: ""
  retrieved_at: "YYYY-MM-DD"
  confidence: confirmed | partially_confirmed | unvalidated
subject:
  person_id: null
  company_id: "COMP-..."
  riu_ids: ["RIU-..."]
claim: ""
signal_dimensions:
  recency: fresh | aging | stale
  originality: primary | practitioner | curator | derivative
  reach: niche | strong | mass
  durability: fast_decay | medium_decay | durable
  bias: founder | investor | educator | operator | analyst | vendor | unknown
  validation: confirmed | partially_confirmed | unvalidated
palette_actionability: integrate | evaluate | monitor | skip | archive | unknown
```

### Layer 4: Scoring And Interpretation

Signals should feed interpreted fields, not raw counts only.

Core derived metrics:

- `market_heat`
- `practitioner_validation`
- `enterprise_readiness`
- `integration_readiness`
- `signal_confidence`
- `hype_risk`
- `decay_risk`
- `taxonomy_pressure`
- `recipe_gap`
- `recommendation_stability`

### Layer 5: Decision Outputs

The External Reality Layer should produce:

- company status updates
- RIU heatmap
- taxonomy gap proposals
- recipe candidates
- integration/evaluation queue
- people follow/update queue
- contradiction ledger
- radar view
- quarterly enrichment brief
- agent routing hints

## Schema Evolution

### People Profile Additions

Current people profiles have `signal_type`, `signal_quality`, `status`, `lens`, and `palette_relevance`.

Add:

```yaml
signal_role:
  primary: mass_adoption_sensor | production_engineering_sensor | frontier_lab_signal | enterprise_buyer_signal | safety_policy_signal | founder_roadmap_signal | investor_market_map | practitioner_proof | derivative_amplifier
  secondary: []

signal_dimensions:
  recency: fresh | aging | stale
  originality: primary | practitioner | curator | derivative
  reach: niche | strong | mass
  durability: fast_decay | medium_decay | durable
  bias: founder | investor | educator | operator | analyst | vendor | mixed
  validation: confirmed | partially_confirmed | unvalidated

cadence:
  search_cadence: weekly | biweekly | monthly | quarterly | event_driven | manual_only
  last_run: "YYYY-MM-DD"
  next_scheduled_run: "YYYY-MM-DD"
  cadence_status: scheduled | pending | overdue | manual_only

signal_decay_rate: fast | medium | slow | durable
last_activity_date: "YYYY-MM-DD"

external_reality_role:
  detects:
    - "consumer AI workflow adoption"
    - "production ML architecture"
  weak_signal_value: low | medium | high
  noise_risk: low | medium | high
```

### Company Entry Additions

Add:

```yaml
company_id: "COMP-..."
status: active | watch | pivoted | acquired | declining | stale_unverified | archived
last_validated: "YYYY-MM-DD"
validation:
  state: confirmed | partially_confirmed | unvalidated
  sources: []
  next_validation_due: "YYYY-MM-DD"

agentic_profile:
  type: framework | executor | orchestrator | agent-aware | agent-native-product | not_agentic
  autonomy_level: none | assisted | semi_autonomous | autonomous
  human_checkpoint_support: true
  production_observability: unknown | weak | moderate | strong

palette_status:
  recommendation: integrate | evaluate | monitor | skip | archive | avoid
  integration_status: none | candidate | in_progress | implemented | deprecated
  recipe_file: null
  rationale: ""

people_library_signals:
  tier_1_mentions: []
  tier_2_mentions: []
  tier_3_mentions: []
  conflicting_signals: []

build_vs_buy_assessment:
  strategic_fit: 1
  time_to_value: 1
  integration_complexity: 1
  data_control: 1
  cost: 1
  lock_in: 1
  notes: ""

market_state:
  market_heat: low | medium | high | extreme
  hype_risk: low | medium | high
  decay_risk: low | medium | high
  funding_momentum: low | medium | high
  practitioner_adoption: low | medium | high

decision_notes:
  why_now: ""
  why_not: ""
  revisit_trigger: ""
```

### RIU Additions

Add optional external signal metadata:

```yaml
external_reality:
  market_heat: low | medium | high | extreme
  signal_count: 0
  company_count: 0
  recipe_count: 0
  missing_category_pressure: low | medium | high
  taxonomy_gap_candidates: []
  top_companies: []
  top_people_signals: []
  recommended_palette_action: none | monitor | evaluate | add_recipe | add_skill | add_knowledge | add_riu
```

## Generated Artifacts

### 1. `lens_index.yaml`

Purpose:
- fast agent routing over people profiles
- no need for Orchestrator to scan every profile
- exposes overdue cadence

Shape:

```yaml
lens_routing_table:
  - lens_id: "LENS-PERSON-001"
    person_id: "PERSON-001"
    person_name: "Ruben Hassid"
    signal_role: "mass_adoption_sensor"
    signal_quality: high
    activate_when: []
    focus: ""
    search_cadence: weekly
    last_run: "2026-02-24"
    cadence_status: overdue
```

### 2. `company_index_health.yaml`

Purpose:
- health summary for Company Index
- used by Health / Total Health agents

Shape:

```yaml
metadata:
  generated_at: "YYYY-MM-DD"
  total_companies: 127
  active: 0
  stale_unverified: 127
  pivoted: 0
  acquired: 0
  archived: 0
  health: critical
```

### 3. `contradiction_ledger.yaml`

Purpose:
- record conflicts across People, Company, Recipes, Service Routing, and Knowledge

Shape:

```yaml
contradictions:
  - id: "CONFLICT-001"
    severity: critical | high | medium | low
    type: stale_company_status | missing_company_entry | relationship_error | recipe_company_mismatch | signal_conflict
    affected_entities:
      companies: []
      people: []
      rius: []
      recipes: []
    description: ""
    proposed_resolution: ""
    owner_agent: researcher | architect | validator | human
    status: open | resolved | accepted_risk
```

### 4. `palette_radar.md`

Purpose:
- human-facing view of external reality
- turns raw YAML into strategic awareness

Radar rings:

- Adopt
- Trial
- Watch
- Archive

Categories:

- model providers
- coding agents
- agent orchestration
- AI search/research
- voice agents
- enterprise AI
- creative/video
- GTM/sales
- legal/compliance
- data analytics
- safety/governance

Example:

```markdown
## Adopt
- Claude / Anthropic — primary LLM, already operational
- Perplexity — research enrichment, already operational

## Trial
- Lovable — no-code app generation; run Phase 0 prototype experiment
- NotebookLM — long-document synthesis for Researcher

## Watch
- ElevenLabs — voice agent category heat, not yet core Palette integration
- Harvey — legal AI, high market heat but low current Palette fit

## Archive
- Fixie.ai as orchestration platform — pivoted to Ultravox voice model
```

### 5. `external_reality_quarterly_brief.md`

Purpose:
- quarterly narrative layer
- what changed, why it matters, what Palette should do

Sections:

- category heat shifts
- top company changes
- people signal changes
- taxonomy pressure
- recipe candidates
- retired / pivoted entities
- recommended governance votes

## Agent Responsibilities

### Researcher

Responsibilities:
- verify factual claims
- enrich people/company entries
- detect funding, acquisition, pivot, launch, and role changes
- attach source provenance

Must not:
- decide recommendations alone
- promote hype without validation

### Architect

Responsibilities:
- interpret structural implications
- propose schema evolution
- decide when a category needs a new RIU
- evaluate build-vs-buy consequences

Must not:
- let market heat alone drive architecture

### Builder

Responsibilities:
- implement schema migrations
- generate indices
- connect recipes and company IDs
- build health scripts

Must not:
- rewrite data semantics without review

### Validator

Responsibilities:
- verify schema conformance
- detect contradictions
- check source coverage
- run health gates

Must not:
- silently downgrade critical stale facts

### Monitor

Responsibilities:
- watch cadence
- flag overdue profiles and companies
- detect heat changes and category movement

Must not:
- interpret signal alone

### Narrator

Responsibilities:
- turn external reality into readable briefings
- explain why changes matter to operators, learners, and portfolio stories

Must not:
- overstate market claims

### Orchestrator

Responsibilities:
- route enrichment and validation tasks
- decide which agent should handle contradictions
- use `lens_index.yaml` and radar outputs for routing

Must not:
- scan raw YAML when generated routing surfaces exist

## Governance Model

### Decision Types

Two-way-door decisions:

- mark company as monitor
- add signal note
- add unvalidated source
- add radar watch item
- add preliminary taxonomy gap candidate

One-way-door or high-risk decisions:

- remove company from active recommendation
- change primary company identity
- add new RIU
- promote company to integrate
- publish externally
- mark person/company as authoritative

### Validation Requirements

Before next publish:

- no critical relationship errors
- no active company without `last_validated`
- no renamed/acquired company without alias mapping
- no recipe without `company_id`
- no Tier 1 recommendation without at least one confirmed source
- no external-facing funding/valuation claim without source date

## Health Checks

Add checks:

1. Company validation freshness
- fail if more than N active companies are `stale_unverified`

2. People cadence freshness
- warn when search cadence overdue

3. Company ID coverage
- fail if company entries lack `company_id`

4. Recipe linkage
- warn if recipe has no company link

5. Crossref orphan detection
- fail if People crossref mentions a company missing from Company Index

6. Pivot/acquisition alias check
- warn if old brand appears without canonical alias

7. Agentic profile completeness
- warn if `agentic_native` exists without typed `agentic_profile`

8. Contradiction debt
- report unresolved contradictions by severity

9. Radar freshness
- warn if radar not regenerated after company/person changes

10. Taxonomy pressure
- warn if multiple high-signal companies cluster around missing RIU

## First Implementation Slice

Do not implement everything at once.

### Phase 0 — Data Safety

Goal:
- prevent corrupted reasoning.

Actions:

1. Fix critical People Library factual errors.
2. Rename Codeium -> Windsurf.
3. Reclassify Fixie.ai as pivoted / voice AI.
4. Add Lovable to Company Index.
5. Add minimal `status` and `last_validated` to Company Index entries.

Output:
- clean baseline
- no known critical factual errors

### Phase 1 — Join Layer

Goal:
- make cross-artifact reasoning deterministic.

Actions:

1. Add `company_id`.
2. Create alias registry.
3. Link People crossref to `company_id`.
4. Link recipes to `company_id`.
5. Generate `company_index_health.yaml`.

Output:
- deterministic company joins
- health visibility

### Phase 2 — Signal Semantics

Goal:
- make people and companies interpretable, not just listed.

Actions:

1. Add `signal_role` and `signal_dimensions` to people.
2. Add typed `agentic_profile` to companies.
3. Add `people_library_signals` reverse links to companies.
4. Generate `lens_index.yaml`.

Output:
- agent routing over people
- typed company interpretation

### Phase 3 — Radar

Goal:
- expose external reality to humans and agents.

Actions:

1. Generate `palette_radar.md`.
2. Add radar categories and rings.
3. Add external reality section to wiki.
4. Add radar freshness health check.

Output:
- human-readable external reality layer

### Phase 4 — Decision Intelligence

Goal:
- use external reality in traversal and recommendations.

Actions:

1. Add market heat to RIUs.
2. Add build-vs-buy scoring to top companies.
3. Add contradiction ledger.
4. Feed external signal confidence into traversal.
5. Emit recommendation stability notes.

Output:
- recommendations that know when external reality has changed

## Initial Additions Policy

The audit recommends 8 people and 20 companies.

Do not add all at once.

### First 5 People

Recommended first wave:

1. Ethan Mollick
- research-backed adoption signal

2. Harrison Chase
- agent infrastructure signal

3. Allie K. Miller
- enterprise AI / B2B ROI signal

4. Fei-Fei Li
- safety, ethics, human-centered AI signal

5. Dario Amodei or Demis Hassabis
- frontier lab executive signal

Rationale:
- closes research adoption, agent frameworks, enterprise AI, safety, and frontier-lab gaps without overloading the library.

### First 8 Companies

Recommended first wave:

1. Anthropic / Claude
2. Lovable
3. Sierra
4. Decagon
5. ElevenLabs
6. Perplexity
7. Cognition / Devin
8. Glean

Rationale:
- covers model providers, no-code app generation, CX agents, voice agents, AI search, coding agents, and enterprise search.

Hold:

- Harvey
- Clay
- Runway
- Mistral
- xAI
- Hex
- Cohere
- LangGraph standalone

These are important but should be added after canonical IDs and category schema exist.

## Creative Extensions

### 1. Signal Portfolio Theory

Palette should balance signal sources like an investment portfolio.

Too many creator signals creates hype exposure.
Too many frontier lab signals creates strategy without workflow reality.
Too many VC signals creates funding bias.
Too many practitioner signals may miss platform shifts.

The People Library should track signal diversification:

```yaml
signal_portfolio:
  creator: 30%
  practitioner: 25%
  frontier_lab: 15%
  enterprise_buyer: 10%
  safety_policy: 10%
  investor: 10%
```

The goal is not equal weights. The goal is intentional exposure.

### 2. Heat Without Hype

Market heat should be decomposed:

- funding heat
- practitioner heat
- enterprise adoption heat
- open-source heat
- regulatory heat
- Palette action heat

This prevents funding from masquerading as usefulness.

### 3. Category Birth Detector

When People signals and Company signals cluster around no existing RIU, Palette should generate a taxonomy pressure alert.

Example:

```yaml
taxonomy_pressure:
  proposed_riu: "No-Code AI App Generation"
  evidence:
    people_signals: ["Ruben", "Lovable orbit"]
    companies: ["Lovable", "v0", "Replit"]
    recipes: []
  recommended_action: "create RIU proposal"
```

### 4. External Reality Replay

Run past build-vs-buy decisions against updated external reality.

Question:
- Would Palette still make the same recommendation today?

If not:
- emit decision drift.

### 5. Signal Memory For Agents

Agents should be able to ask:

- "Why do we trust this company?"
- "Who validated this?"
- "When did we last check it?"
- "What would cause us to change our mind?"

This makes external reality explainable.

## User-Facing Value

For the operator:

- fewer stale recommendations
- faster awareness of market shifts
- clearer build-vs-buy judgment
- explicit "why now / why not" reasoning

For agents:

- better routing
- less fuzzy matching
- stronger evidence
- visible contradictions
- clear enrichment tasks

For human enablement:

- learning paths stay current
- skills evolve with the market
- people can see not just what to learn, but why the category matters now

For Portfolio / interview / proof-of-work:

- shows Palette is not a static knowledge base
- proves the system can sense external change and adapt
- demonstrates a real FDE-grade intelligence loop

## Anti-Patterns To Avoid

1. Valuation chasing
- Funding is a signal, not a recommendation.

2. Infinite enrichment
- More entities do not equal better intelligence.

3. Influencer overfitting
- High reach does not mean high truth.

4. Schema bloat before joins
- Do not add advanced fields before canonical IDs.

5. Flattened agentic classification
- Agentic-native is no longer a binary.

6. Publishing unvalidated claims
- Especially funding, valuation, roles, acquisitions, and leadership relationships.

7. Treating monitor as failure
- "Monitor" is a valid decision.

8. Losing historical pivots
- Archive and pivot states preserve memory.

## Definition Of Done

The External Reality Layer is operational when:

1. Company joins are deterministic across People, Company, Recipes, and Service Routing.
2. People profiles expose signal role, cadence, and decay.
3. Company entries expose status, validation, integration state, and agentic profile.
4. Health checks flag stale and contradictory external reality.
5. Palette can generate a radar view.
6. Traversal can say: "This recommendation changed because external reality changed."
7. Agents can route enrichment work without scanning raw files.
8. Human users can understand what is rising, what is credible, what is hype, and what Palette should do next.

## Final Frame

Palette's internal system answers:

> "Given what we know, what should we do?"

The External Reality Layer answers:

> "Has the world changed enough that what we know should change?"

That is the missing mirror.

The taxonomy is Palette's internal map.
The People/Company/Recipe signal network is the outside world pushing back.

When the outside world moves, Palette should feel it:

- RIUs heat up.
- Company recommendations change.
- Recipes become urgent.
- Agents reroute.
- Skills evolve.
- Learning paths update.
- The operator sees the next move sooner.

This is not just a data cleanup.
This is Palette becoming adaptive.
