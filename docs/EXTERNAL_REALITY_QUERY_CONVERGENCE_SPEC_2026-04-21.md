# External Reality Query + Convergence Spec

Date: 2026-04-21
Status: Companion spec to `EXTERNAL_REALITY_LAYER_SPEC_2026-04-21.md`
Purpose: Define the queryable system that sits on top of the External Reality Layer and forces convergence before Palette acts on market signals.

## One-Sentence Design

Build the External Reality Layer as a read-first, action-gated intelligence service: agents and humans can query what is happening in the outside AI market, but every material action must pass through an explicit convergence packet that classifies evidence, affected RIUs, reversibility, confidence, and proposed next step before changing Palette behavior.

## V1 Scope Controls

Review disposition: Kiro approved the architecture with scope controls. Codex accepts these controls as binding for v1 implementation.

The architecture should stay large enough to preserve the boundary, but v1 must stay small enough to prove the data can feed the machinery:

1. Implementation cap: Slices 1-3 must stay under 500 lines of implementation code. If the design needs more than that to prove value, the first slice is too broad.
2. Core schema only: v1 uses the core zone only. Extensions and experimental fields go to the schema backlog until a query, gate, health check, generated artifact, or deterministic join requires them.
3. One script, one agent, three steps: v1 should not use a multi-agent workflow. It should query, produce SignalPackets, and emit a convergence brief.
4. No bot before CLI proof: bot commands are deferred until Slice 3 works and has been used at least 5 times.

Kill switch:

```text
If after Slice 3 fewer than 5 actionable SignalPackets have been produced, pause ERS implementation and reassess whether the available data justifies the system.
```

This is not a reduction of the concept. It is the proof harness that prevents the External Reality Layer from becoming a second project before it has earned operational gravity.

## Palette Routing Pass

This design maps to existing Palette RIUs:

- `RIU-140` — Competitive/Alternatives Scan: market and alternatives research.
- `RIU-201` — Competitive/Alternatives Research: detailed company/category evaluation.
- `RIU-543` — Drift Detection Configuration: detect data, market, behavior, and recommendation drift.
- `RIU-087` — Human Review Gate: irreversible or high-impact actions require explicit confirmation.
- `RIU-608` — Workflow Definition for Multi-Agent Engagements: typed workflow with phases, assignments, gates, and checkpoints.
- `RIU-003` — Decision Log + One-Way Door Registry: material changes must be logged for restartability.

The new system should not bypass Palette. It should become the external signal source that feeds existing convergence, routing, and governance.

## Core Separation

The most important architectural boundary:

```text
Querying external reality is not acting on external reality.
```

Palette should support two modes:

1. Observation Mode
- read-only
- answer questions
- surface signals, contradictions, and stale data
- no changes to recommendations or routing

2. Action Mode
- requires convergence packet
- may update Company Index, People Library, recipes, RIUs, radar, traversal confidence, or decisions
- gated by reversibility and confidence

Refined operating rule:

```text
External reality is validated on pull, not continuously.
```

ERS should not create a permanent MLOps-style validation burden. It should hold structured observations and only force validation when a human or agent pulls information for a concrete use:

- `/brief`
- topic query
- quarterly update
- pull request / data change
- recommendation change
- proposed action

This keeps maintenance cost low while ensuring no unverified signal becomes a decision.

## Why A Separate Query System

The External Reality Layer should not be embedded directly inside the traversal engine at first.

Reasons:

- The data will be noisy.
- Signals will conflict.
- Market movement is not the same as recommendation change.
- Agents may over-trust fresh external data.
- The existing internal ontology should remain stable unless external evidence passes a convergence gate.

So the right design is a separate queryable service with controlled bridges back into Palette.

## Proposed Component

Name options:

- `reality_query`
- `external_reality_service`
- `market_signal_engine`
- `signal_convergence_engine`

Recommended name:

```text
External Reality Service (ERS)
```

Short name in code:

```text
ers
```

Reason:
- neutral, extensible, not hypey
- covers people, companies, signals, categories, and market drift
- does not imply action by itself

## High-Level Architecture

```text
External sources / audits / people / companies / recipes
        ↓
External Reality Store
        ↓
External Reality Query API
        ↓
Signal Packet
        ↓
Convergence Gate
        ↓
Action Proposal
        ↓
Human / Agent Approval
        ↓
Palette Data Change
```

## Data Stores

### 1. External Reality Store

Normalized read model for external signals.

Potential files:

```text
buy-vs-build/external-reality/
├── external_reality_store.yaml
├── signal_events.yaml
├── entity_aliases.yaml
├── company_registry.yaml
├── person_registry.yaml
├── contradiction_ledger.yaml
├── radar.yaml
└── generated/
    ├── lens_index.yaml
    ├── company_index_health.yaml
    └── riu_market_heat.yaml
```

The store can start as YAML. It should be structured as if it could later move to SQLite or graph storage.

### 2. Source-of-Truth Artifacts

Existing artifacts remain authoritative until changed:

- People Library
- Company Index
- Recipes
- Service Routing
- Taxonomy
- Knowledge Library

External Reality Store is a read model and signal layer, not the canonical source for every object.

## Query API

Queries should return evidence and actionability, not just answers.

ERS has two query tiers:

1. Observation
- returns known signals with labels
- no mandatory research refresh
- suitable for browsing, brainstorming, radar views, and "what is happening?" questions

2. Verified Pull
- mandates Researcher validation before action
- required before ActionProposal
- required before any source-of-truth data change
- required before PR merge involving external reality updates

The system should make the tier explicit in every result.

### Query Types

```yaml
query_type:
  - company_status
  - person_signal
  - category_heat
  - riu_market_pressure
  - recommendation_drift
  - contradiction_lookup
  - recipe_gap
  - radar_view
  - action_candidates
```

### Example Queries

```text
What is happening in AI coding agents?
Which companies affect RIU-510?
Which recommendations have drifted since February?
Which People Library signals mention Lovable?
Which companies are high heat but have no recipe?
Which categories have enough signal to propose a new RIU?
What changed that could affect service routing?
```

### Query Result Shape

```yaml
query_result:
  query_id: "ERQ-..."
  query: ""
  query_type: "category_heat"
  generated_at: "YYYY-MM-DDTHH:MM:SS"
  mode: observation | verified_pull
  validation_state: unverified_observation | researcher_verified | stale_verified | blocked
  related_rius: []
  entities:
    people: []
    companies: []
    recipes: []
  signals:
    - signal_id: "SIG-..."
      claim: ""
      confidence: confirmed | partially_confirmed | unvalidated
      source_type: primary | practitioner | founder | investor | vendor | internal
      decay_rate: fast | medium | slow | durable
  synthesis:
    what_changed: ""
    why_it_matters: ""
    confidence: low | medium | high
    uncertainty: []
  actionability:
    recommended_mode: observe | converge | act
    possible_actions: []
    blocked_actions: []
```

## Pull-Time Validation

Validation happens when information is pulled into a decision context.

Trigger validation when:

- a PR changes People Library, Company Index, recipes, service routing, taxonomy, radar, or ERS files
- a user asks for an action, not just a briefing
- a query result will be used to change a recommendation
- a company/person/category is promoted from watch to evaluate/integrate
- a stale signal is older than its decay budget and appears in a proposed action

Do not trigger validation when:

- user only asks for a read-only brief
- signal remains in observation tier
- radar displays clearly label unverified/stale status
- data is added as an unverified note without actionability

### Pull-Time Validation Contract

Every verified pull should produce:

```yaml
validation_record:
  id: "VAL-..."
  query_id: "ERQ-..."
  validated_by: researcher
  validated_at: "YYYY-MM-DDTHH:MM:SS"
  validation_scope:
    companies: []
    people: []
    rius: []
    claims: []
  confidence: low | medium | high
  sources_checked: []
  claims_confirmed: []
  claims_rejected: []
  claims_uncertain: []
  action_allowed: true
  notes: ""
```

This is intentionally simple. It is not an MLOps subsystem. It is a mandated research check before action.

## Signal Packet

Any query that might lead to action becomes a `SignalPacket`.

The SignalPacket is the bridge between observation and convergence.

It should behave like an immutable event, not a mutable task note.

Design rule:

```text
SignalPackets record that external reality may have changed.
They do not decide what Palette should do.
```

```yaml
signal_packet:
  id: "SIGPKT-..."
  packet_version: "1.0"
  source_query_id: "ERQ-..."
  created_at: "YYYY-MM-DD"
  created_by: researcher | monitor | human | orchestrator
  lifecycle_state: observed | enriched | deduped | gated | converged | actioned | rejected | archived
  idempotency_key: ""
  related_rius: []
  affected_artifacts:
    people_library: []
    company_index: []
    recipes: []
    service_routing: []
    taxonomy: []
    knowledge_library: []
  signal_summary: ""
  evidence:
    confirmed: []
    partial: []
    unvalidated: []
  contradiction_check:
    conflicts_found: true
    conflicts: []
  palette_action_class: observe | research | update_index | update_recipe | propose_riu | alert_human
  proposed_action:
    action_type: update_data | add_entity | archive_entity | add_recipe_candidate | propose_riu | change_recommendation | monitor_only
    description: ""
  confidence:
    evidence_quality: low | medium | high
    action_confidence: low | medium | high
  reversibility:
    classification: two_way | one_way
    rationale: ""
  convergence_required: true
```

`palette_action_class` is a core v1 field because it makes the governance path deterministic:

- `observe` means no action, only record or brief.
- `research` means pull a Researcher validation run before any recommendation.
- `update_index` means Company Index or People Library may be affected.
- `update_recipe` means an integration recipe may be added, changed, or deprecated.
- `propose_riu` means the signal suggests a new requirement or taxonomy gap.
- `alert_human` means the signal is high-impact, contradictory, time-sensitive, or otherwise unsafe to route automatically.

The convergence gate can then apply different thresholds by action class instead of treating every proposed action as the same kind of change.

Operational enforcement:

- every `palette_action_class` must map to an `RIU-003` decision-log / one-way-door registry posture
- `observe` and `research` default to no decision-log write unless they are attached to a later action
- `update_index`, `update_recipe`, and `propose_riu` require a convergence brief before source-of-truth writes
- `alert_human` always creates a human-review task and cannot be auto-promoted

This makes action class more than a label. It becomes the deterministic bridge between external signal and Palette governance.

### SignalPacket Lifecycle

```text
Observe -> Packetize -> Deduplicate -> Enrich -> Gate -> Converge -> Act / Monitor / Reject -> Replay
```

1. Observe
- QueryResult surfaces a potentially material change.
- Example: "Fixie.ai no longer belongs in agent orchestration."

2. Packetize
- Convert the observation into a bounded SignalPacket.
- Attach affected RIUs, companies, people, recipes, and source artifacts.

3. Deduplicate
- Check whether the same external event has already been packetized.
- Use `idempotency_key`, canonical entity IDs, event type, and normalized claim hash.

4. Enrich
- Add evidence, confidence, source type, decay rate, and contradiction check.
- Researcher owns evidence enrichment.

5. Gate
- Determine whether action is monitor-only, two-way, one-way, or blocked.
- Validator / Architect owns gate classification.

6. Converge
- Produce a ConvergenceResult with explicit action, rationale, rejected options, and next agent.

7. Act / Monitor / Reject
- Builder acts only after gate passes.
- Monitor tracks if no action is safe yet.
- Rejected packets remain in history with rationale.

8. Replay
- Old SignalPackets can be replayed against current state to detect decision drift.

### Deduplication Strategy

Do not rely only on source URL. The same event may appear in multiple sources.

Compute:

```yaml
idempotency_key_inputs:
  entity_type: company | person | category | riu | recipe
  canonical_entity_id: "COMP-..."
  event_type: funding | acquisition | pivot | product_launch | recommendation | correction | contradiction
  normalized_claim_hash: "sha256(...)"
  event_date: "YYYY-MM-DD"
```

Rules:

- same entity + same event type + same normalized claim within a time window = likely duplicate
- same entity + same event type + materially different claim = contradiction candidate
- same claim from multiple source types = confidence upgrade candidate
- same claim only from derivative sources = no confidence upgrade

### Replay Semantics

SignalPackets must be append-only so Palette can answer:

- What did we believe when we made this recommendation?
- Which external signal changed the decision?
- Would we make the same decision today?
- Which stale signals are still influencing recommendations?

Replay should rebuild:

- entity status
- radar ring
- contradiction ledger
- recommendation drift candidates
- RIU market heat

### Confidence Is Multi-Dimensional

Avoid one scalar confidence score as the only signal.

Use:

```yaml
confidence:
  evidence_quality: low | medium | high
  source_diversity: low | medium | high
  source_independence: low | medium | high
  claim_specificity: low | medium | high
  recency_fit: low | medium | high
  action_confidence: low | medium | high
```

Reason:
- A funding claim may have high source confidence but low Palette action confidence.
- A practitioner recommendation may have high action relevance but low generalizability.
- A founder claim may be current but biased.

Anti-hype rule:

```text
Practitioner proof outranks reach.
```

For v1, ERS should prefer evidence that someone competent actually used, evaluated, migrated from, or rejected a tool over evidence that the tool is merely popular, heavily funded, or repeatedly mentioned. Reach may increase `market_heat`; it should not by itself increase `action_confidence`.

### Simple Top-Level Confidence

For operator usability, also expose one simple top-level confidence label:

```yaml
confidence_label: low | medium | high
```

Use it as a summary, not as the source of truth.

Recommended rules:

- `high`: at least two independent sources or one primary source plus strong practitioner confirmation; no unresolved contradiction
- `medium`: one credible source or multiple derivative sources; some uncertainty remains
- `low`: unvalidated, derivative, stale, founder-only, or contradicted

No numeric scoring is required for v1.

Do not add a sentiment or warmth score to core v1. If a quarterly brief needs narrative tone later, capture it as an extension field or generated-artifact annotation after CLI usage proves it affects decisions.

### Approval Gate Matrix

```yaml
gate_matrix:
  monitor_note:
    default_gate: pass
    decision_log_required: false
  add_unvalidated_signal:
    default_gate: pass
    decision_log_required: false
  add_company_alias:
    default_gate: pass_if_no_conflict
    decision_log_required: false
  add_company_entry:
    default_gate: convergence_required
    decision_log_required: true
  change_company_status:
    default_gate: convergence_required
    decision_log_required: true
  change_recommendation:
    default_gate: human_if_high_impact
    decision_log_required: true
  archive_company:
    default_gate: human_required_if_recipe_or_routing_exists
    decision_log_required: true
  add_riu:
    default_gate: human_required
    decision_log_required: true
```

## Convergence Gate

The convergence gate answers:

> "Do we understand enough to act, and what kind of action is safe?"

### Gate Inputs

- SignalPacket
- affected RIUs
- existing Palette recommendation
- evidence confidence
- contradiction ledger
- artifact blast radius
- reversibility classification
- operator intent

### Gate Outputs

```yaml
convergence_result:
  packet_id: "SIGPKT-..."
  status: converged | blocked | monitor_only | needs_research | needs_human
  decision:
    action: none | monitor | update | propose | implement
    reversibility: two_way | one_way
    approval_required: true
  rationale: ""
  accepted_risks: []
  rejected_actions: []
  next_agent: researcher | architect | builder | validator | monitor | human
  decision_log_required: true
```

### Forced Convergence Rules

The system must block action if:

- evidence is unvalidated and action changes recommendation
- affected artifact is taxonomy, service routing, or recipe status
- company/person identity is being changed
- existing recommendation would be demoted or removed
- a new RIU is proposed
- blast radius touches more than one RIU group
- contradiction ledger has unresolved high/critical conflict

The system can allow two-way action if:

- adding a monitor note
- adding unvalidated signal with clear label
- updating radar watch item
- opening an enrichment task
- adding a non-authoritative alias

## Wire Contract Integration

Use existing Palette HandoffPacket / HandoffResult.

### HandoffPacket Example

```json
{
  "id": "uuid",
  "from": "orchestrator",
  "to": "researcher",
  "task": "Validate external signal about Lovable and determine whether Company Index action is warranted",
  "riu_ids": ["RIU-140", "RIU-201", "RIU-087"],
  "payload": {
    "external_reality": {
      "mode": "convergence",
      "query_id": "ERQ-001",
      "signal_packet_id": "SIGPKT-001",
      "proposed_action": "add_or_update_company_entry",
      "affected_artifacts": [
        "palette_company_riu_mapping_v1.0.yaml",
        "people_library_company_signals_v1.1.yaml"
      ],
      "evidence_requirements": {
        "min_confirmed_sources": 2,
        "allow_unvalidated_funding_claims": false
      }
    }
  },
  "trace_id": "trace-id"
}
```

### HandoffResult Example

```json
{
  "packet_id": "uuid",
  "from": "researcher",
  "status": "success",
  "output": {
    "signal_packet_id": "SIGPKT-001",
    "evidence_quality": "high",
    "recommended_gate_status": "needs_human",
    "proposed_action": "add_lovable_to_company_index",
    "reversibility": "two_way",
    "rationale": "Missing company creates recommendation gap; addition is additive and reversible."
  },
  "blockers": [],
  "artifacts": [
    "external_reality/reports/ERQ-001_lovable_validation.md"
  ],
  "next_agent": "architect"
}
```

## Agent Workflow

### Phase 1: Observe

Actor:
- human, Monitor, Researcher, Orchestrator

Output:
- QueryResult

No action allowed.

### Phase 2: Packetize

Actor:
- Monitor or Orchestrator

Output:
- SignalPacket

Purpose:
- convert interesting signal into bounded decision object

### Phase 3: Converge

Actor:
- Architect + Validator, with Researcher evidence if needed

Output:
- ConvergenceResult

Purpose:
- decide if action is safe

### Phase 4: Act

Actor:
- Builder for code/data changes
- Human for one-way approvals
- Monitor for watch-state updates

Output:
- artifact changes
- decision log entry if required

### Phase 5: Replay

Actor:
- Validator / Monitor

Output:
- impact report

Purpose:
- determine whether recommendations or traversal outputs changed

## Query Surface

Start with CLI before UI.

```bash
python3 -m scripts.external_reality.query \
  --type category_heat \
  --category ai_coding_agents

python3 -m scripts.external_reality.query \
  --company Lovable \
  --mode observation

python3 -m scripts.external_reality.converge \
  --query ERQ-001 \
  --proposed-action add_company_entry
```

Later:

- Mission Canvas endpoint
- Voice query
- Wiki page
- Radar dashboard
- Peers bus notifications

## Skill-Style Operating Model

ERS should behave like a Palette skill: exact instructions, invoked when needed, bounded output, no ambient mutation.

Skill name:

```text
external-reality-pull
```

Invocation examples:

```text
Run external-reality-pull for "research agent creation."
Run external-reality-pull for "AI coding agents."
Run external-reality-pull for "voice agent platforms."
Run external-reality-pull for "what changed since last week?"
```

Skill flow:

1. Clarify topic
- topic, category, RIUs if known, time horizon, intended use

2. Query ERS
- pull current observations from local store

3. Decide tier
- observation only or verified pull

4. If verified, call Researcher
- validate claims and find missing updates

5. Produce SignalPackets
- only for materially relevant changes

6. Converge before action
- action proposal never bypasses gate

7. Emit brief
- concise human artifact plus machine-readable packet refs

This keeps ERS procedural and safe.

## Bot / Notification Model

ERS should eventually have a bot interface similar to the Joseph / Palette Telegram bot pattern.

Potential commands:

```text
/brief
/brief ai-coding-agents
/brief research-agents
/watch Lovable
/watch RIU-510
/alerts
/validate SIGPKT-001
/radar
/stale
/contradictions
```

Command behavior:

- `/brief`: observation-tier summary of hottest updates
- `/brief <topic>`: topic-specific external reality pull
- `/watch <entity>`: add monitor item
- `/alerts`: show threshold-crossing changes
- `/validate <packet>`: trigger Researcher verification
- `/radar`: show Adopt / Trial / Watch / Archive
- `/stale`: show signals past decay budget
- `/contradictions`: show unresolved conflict ledger

Alarm examples:

- company with recipe becomes acquired/pivoted
- Tier 1 company status changes
- 3+ high-signal people mention a missing company
- RIU has market heat but no company/recipe coverage
- recommendation depends on stale signal

Important:

Bot output is observation unless explicitly validated.

Every bot response should show:

```text
Mode: observation | verified
Confidence: low | medium | high
Action: none | validation suggested | convergence required
```

## Proposed CLI Commands

```bash
# Query only
python3 -m scripts.external_reality.query --q "What is happening in AI coding agents?"

# Produce signal packet from query
python3 -m scripts.external_reality.packetize --query-id ERQ-001

# Run convergence gate
python3 -m scripts.external_reality.converge --packet-id SIGPKT-001

# Generate radar
python3 -m scripts.external_reality.radar

# Run health checks
python3 -m scripts.external_reality.health
```

## Decision Policy

### Observation Does Not Require Approval

Examples:

- "What is happening with Lovable?"
- "Which companies mention RIU-510?"
- "What categories are heating up?"
- "Which entries are stale?"

### Action Requires Convergence

Examples:

- Add company to index.
- Remove company from recommendation.
- Change agentic profile.
- Change service routing.
- Add RIU.
- Promote tool to integrate.

Action requires two tiers:

1. Researcher-verified pull
2. One-way-door style approval gate before final decision if source-of-truth artifacts or recommendations change

Even if the edit is technically reversible, force a decision checkpoint for:

- recommendation changes
- company status changes affecting routing
- RIU additions
- recipe status changes
- external-facing publish

### One-Way Door Requires Human

Examples:

- Publish externally.
- Demote a current recommendation.
- Archive a company with existing recipe.
- Change canonical company identity.
- Add taxonomy category that affects traversal.

## Why This Is Better Than Direct Integration

Directly wiring market signals into traversal creates risk:

- fresh but wrong signals could override stable knowledge
- agents may recommend hot tools prematurely
- schema instability could leak into user-facing decisions
- company hype could look like evidence

The separate ERS design creates a buffer:

```text
External movement -> Query -> SignalPacket -> Convergence -> Action
```

That preserves Palette's core strength: convergence before commitment.

## Schema Creep Control

The main implementation risk is not bad market data. The main risk is schema sprawl: adding fields opportunistically until the data layer becomes hard to maintain.

ERS should use a schema budget.

### Schema Budget Rule

No new field may be added unless it satisfies at least one of:

- used by a query
- used by a gate
- used by a health check
- used by a generated artifact
- required for deterministic joins

If a field is only "nice to know," it goes in `notes` or `raw_observations`, not the canonical schema.

### Three-Zone Schema Model

1. Core fields
- stable
- required for joins, gates, and replay
- examples: `company_id`, `person_id`, `event_type`, `confidence_label`, `validation_state`

2. Extension fields
- optional
- namespaced
- can evolve without breaking consumers
- examples: `market_state`, `agentic_profile`, `build_vs_buy_assessment`

3. Raw observations
- unstructured or lightly structured
- not used for decisions
- safe place for exploratory data

Shape:

```yaml
core:
  id: "SIGPKT-..."
  entity_ref: "COMP-..."
  event_type: "funding"
  validation_state: researcher_verified
  confidence_label: medium
extensions:
  market_state:
    market_heat: high
raw_observations:
  notes:
    - "Founder claim seen in interview; not independently verified."
```

Deferred extension candidate:

```yaml
extensions:
  narrative:
    human_sentiment_label: optimistic | skeptical | alarmist
```

This is explicitly not core v1. It may graduate only if a generated quarterly brief or operator query uses it repeatedly and it changes routing, prioritization, or review quality.

### Schema Change Gate

Any new canonical field requires:

- field name
- purpose
- consumer
- default value
- migration behavior
- example query or gate that uses it

This prevents random updates from becoming permanent debt.

### Parking Lot For New Ideas

Create a file:

```text
buy-vs-build/external-reality/schema_backlog.yaml
```

Fields can be proposed there before becoming canonical.

```yaml
proposed_fields:
  - name: "enterprise_readiness"
    proposed_by: "codex"
    reason: "Useful for buy-vs-build recommendations"
    consumer: "not yet identified"
    status: parked
```

Only promote when a real consumer exists.

## Minimal Data Model

Start small:

```yaml
external_reality_event:
  id: "ERE-..."
  date: "YYYY-MM-DD"
  entity_type: company | person | category | riu | recipe
  entity_ref: ""
  event_type: funding | acquisition | pivot | product_launch | recommendation | correction | contradiction | validation
  summary: ""
  source: ""
  confidence: confirmed | partially_confirmed | unvalidated
  affects_rius: []
  proposed_action: none | monitor | converge
```

This is enough to query, track, and converge without building a full graph database.

## Implementation Sequence

### Slice 1: Read-Only Query

Build:

- `scripts/external_reality/query.py`
- reads People Library, Company Index, crossref, recipes
- outputs QueryResult JSON
- treats researcher auto-enrichment as the first ERS source path: research findings become candidate SignalPackets rather than standalone knowledge-library writes

No writes.

Also create skill instructions:

```text
skills/external-reality/external-reality-pull.md
```

### Slice 2: Signal Packet

Build:

- `scripts/external_reality/packetize.py`
- converts QueryResult to SignalPacket

Still no source artifact writes.

### Slice 3: Convergence Gate

Build:

- `scripts/external_reality/converge.py`
- classifies action as `monitor_only`, `two_way`, `one_way`, `blocked`

### Slice 4: Monitor Actions Only

Allow:

- write radar watch items
- write contradiction ledger
- write enrichment task queue

Still block source-of-truth changes.

### Slice 5: Data Patches With Approval

Allow:

- additive company entries
- status/last_validated updates
- alias additions

Require:

- convergence result
- validation result
- optional human approval based on reversibility

### Slice 6: Bot Interface

Build after CLI proves useful:

- local command first
- Telegram/voice interface later
- `/brief`, `/watch`, `/alerts`, `/validate`, `/radar`

The bot should read from ERS and create SignalPackets, but not mutate source-of-truth artifacts directly.

## Best Design Choice

The best design is not "make the Company Index smarter."

The best design is:

```text
External Reality Service = Queryable outside-world memory
SignalPacket = bounded unit of market change
Convergence Gate = forced reasoning before action
Action Proposal = governed bridge back into Palette
```

This mirrors Palette's enablement system:

- humans can explore
- agents can retrieve
- signals can accumulate
- but action requires a structured packet and gate

## Final Recommendation

Build ERS as a separate service/module first, not as direct traversal logic.

Use it to answer:

> "What is happening?"

Then force convergence before:

> "What should Palette change?"

That distinction is the whole product.
