# External Reality Query + Convergence Spec

Date: 2026-04-21
Status: Companion spec to `EXTERNAL_REALITY_LAYER_SPEC_2026-04-21.md`
Purpose: Define the queryable system that sits on top of the External Reality Layer and forces convergence before Palette acts on market signals.

## One-Sentence Design

Build the External Reality Layer as a read-first, action-gated intelligence service: agents and humans can query what is happening in the outside AI market, but every material action must pass through an explicit convergence packet that classifies evidence, affected RIUs, reversibility, confidence, and proposed next step before changing Palette behavior.

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
  mode: observation
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

No writes.

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
