# Palette PIS Gap Analysis and Implementation Plan (v1)

**Date**: 2026-02-25  
**Scope**: Palette Intelligence System (PIS), library layers, traversal product gap, orchestration path  
**Author**: Codex (analysis + synthesis based on local audit + user-provided feedback)

---

## Executive Summary

Palette has already solved the hardest foundational problem: **it has a structured, high-quality data layer** (knowledge, people signals, service routing, integration recipes, taxonomy) with real sourcing discipline.

What it does **not** yet have is the core product behavior those layers imply:

- `user problem -> RIU -> service route -> recipe -> signal validation -> actionable recommendation`

That traversal is the product. Today, the layers exist mostly as files a human reads manually.

The highest-leverage next move is **not** adding more data. It is building a **minimal deterministic orchestrator** that walks the four layers and returns a structured, provenance-backed answer with graceful fallbacks when data is missing.

---

## What I Perceive as the Long-Term Goal (from my perspective)

From the current architecture, docs, and feedback, the long-term goal appears to be:

### Long-term goal (product-level)
Build a **general-purpose agentic execution interface** that can:

1. Understand a real-world problem in user language
2. Map it to a reusable intervention pattern (RIU)
3. Determine whether to solve it internally (Palette agents) or externally (services/tools)
4. Route to the best available service stack (quality/cost/trust aware)
5. Provide integration-ready guidance (recipes, steps, constraints)
6. Learn from outcomes over time (routing success/failure feedback)

### Why this is strategically important
This is not just a knowledge base or a tool directory.
It is a **decision-and-execution router**:

- knowledge layer = "what do we know?"
- signals layer = "who is using what and why?"
- routing layer = "what should we use?"
- recipe layer = "how do we do it?"
- orchestration layer = "how do we turn this into an answer/action now?"

That is a stronger and more defensible product than "another AI assistant."

---

## Current State (Short, Honest)

### What is strong
- Knowledge library is broad and sourced
- People signal layer is high quality and cross-referenced
- Service routing exists and is partially cost-aware
- Taxonomy/RIU system is mature enough to support traversal
- Integration recipes exist for real tools

### What is missing
- The traversal orchestrator (core product behavior)
- Shared agent state / handoff enforcement
- Coverage completion on key routing RIUs
- Company-library hydration behind the signal layer
- A test suite for the product promise
- Outcome telemetry for routing quality

---

## Problem -> Proposed Solution Matrix (Extensive)

## Problem 1: No Traversal Orchestrator (Core Product Gap)

### Problem statement
Palette can resolve intent (`Resolver`) and perform research (`Researcher`), but no agent/function currently performs the full middle traversal:

- `RIU -> service routing -> best option -> integration recipe -> people signal validation`

This means the core PIS promise is still conceptual.

### Why it matters
Without this, the system remains a high-quality reference architecture rather than a working routing product.

### Proposed solution
Build a **Minimal Traversal Orchestrator v0** (deterministic first).

### Proposed implementation
- Input: `task text` or `RIU ID`
- Step 1: If task text, call Resolver (or deterministic RIU resolver) -> `RIU + confidence`
- Step 2: Pull matching routing entry
- Step 3: Pull matching integration recipe(s)
- Step 4: Pull people-signal validation for candidate tools
- Step 5: Pull supporting knowledge entries (selection/eval guidance)
- Step 6: Return structured recommendation + gaps + confidence/completeness

### Output contract (recommended)
```yaml
query:
  task: "add guardrails to my LLM app"
  resolved_riu: "RIU-082"
  resolver_confidence: 0.84
result:
  recommendation:
    primary_service: "Bedrock Guardrails"
    rationale: "..."
  alternatives:
    - "Lakera"
    - "Guardrails AI"
  knowledge_support:
    - lib_id: "LIB-..."
      reason: "..."
  recipe:
    path: "palette/buy-vs-build/integrations/.../recipe.yaml"
    status: "available"
  signal_validation:
    strength: "medium"
    recommenders: ["PERSON-..."]
  gaps:
    - "Pricing validation older than 90 days"
  completeness_score: 82
```

### Success criteria
- 5 fixture queries run end-to-end
- At least 3/5 produce full 4-layer traversal
- Missing data is explicitly surfaced, not hidden

### Priority
**P0**

---

## Problem 2: No Shared Agent State / Handoff Coordination

### Problem statement
Agents operate mostly as isolated scripts. Resolver may resolve an RIU, Researcher may research a topic, but there is no enforced shared state that reliably preserves:

- prior resolution
- prior findings
- unresolved gaps
- provenance
- next-step status

### Why it matters
This creates repeated work, weak coordination, and makes debugging difficult.

### Proposed solution
Implement a **task-scoped shared handoff state** (HandoffPacket v2), not full memory.

### Proposed implementation
Use a persistent artifact (JSON/YAML/MD+frontmatter) per task with:
- `task_id`
- original query
- Resolver output (`riu`, confidence, alternatives)
- Researcher output summary + source refs
- Orchestrator traversal output
- gaps/missing-data flags
- final recommendation
- status transitions

### Why this approach first
- Solves coordination immediately
- Enables replay/debug
- Creates a clean stepping stone to memory later
- Lower complexity than full agent memory systems

### Success criteria
- Every traversal task produces one HandoffPacket
- Failed traversals can be replayed/debugged from packet state
- Resolver/Researcher/orchestrator stop redoing work in the same task

### Priority
**P0**

---

## Problem 3: Service Routing Layer Coverage is Only 20/40 Full (Half Stubbed)

### Problem statement
Service routing has all 37 `both` RIUs represented (plus 3 extras), but half the entries are still stubs. This means many traversals will hit low-confidence or incomplete routing.

### Why it matters
The query agent will produce dead ends or partial recommendations on a significant portion of externally routable questions.

### Proposed solution
Do **usage-driven stub burn-down**, not blanket completion.

### Proposed implementation
1. Ship orchestrator first
2. Track which RIUs hit stub routing in real traversals
3. Prioritize stub completion by:
   - query frequency
   - business importance
   - recipe availability
   - signal strength

### Routing entry maturity model (recommended)
- `seed`
- `pricing_validated`
- `api_validated`
- `production_validated`

### Add fields
- `validation_status`
- `validated_at`
- `evidence_url`
- `capability_flags` (`streaming`, `batch`, `tooling`, `multimodal`, etc.)

### Success criteria
- Top 10 most frequently traversed `both` RIUs reach `pricing_validated+`
- Orchestrator fallback rate on routing drops materially over time

### Priority
**P0**

---

## Problem 4: No Graceful Degradation Behavior Across Missing Layers

### Problem statement
If routing, recipe, or signal data is missing, the future orchestrator risks failing or hallucinating unless explicit fallback behavior exists.

### Why it matters
This is a trust problem. A partially complete system can still be useful if it is honest and structured about what is missing.

### Proposed solution
Add **graceful degradation as a first-class feature**.

### Proposed implementation
Fallback logic:

#### If routing is missing
- Return knowledge support + candidate tools from people signals
- Flag: `routing_not_validated`

#### If recipe is missing
- Return route + note `recipe_missing`
- Add explicit next action: create recipe

#### If people signals missing
- Return route + `signal_validation: none`
- Lower confidence, do not block recommendation

#### If knowledge support is weak
- Return route/recipe + explicit note: "selection rationale under-documented"

### Success criteria
- Orchestrator never returns silent failure on missing layer data
- Every partial answer has explicit gap flags

### Priority
**P0**

---

## Problem 5: Knowledge Library Coverage Mismatch (Especially for `both` RIUs)

### Problem statement
Knowledge library has 101 entries and good breadth, but only 66 unique RIUs are covered. Critically, 17 of 37 `both` RIUs appear to lack knowledge coverage.

### Why it matters
These are the RIUs where service selection and integration judgment matter most. Missing knowledge support weakens route justification and eval logic.

### Proposed solution
Create **coverage gates keyed to RIU classification**.

### Proposed implementation
For each `both` RIU:
- Minimum 1 knowledge entry: problem framing / selection context
- Minimum 1 eval entry: how to compare or validate options
- Optional 1 integration/ops entry

### Suggested automation
Coverage audit script outputs:
- `both` RIUs missing knowledge entries
- `both` RIUs missing eval coverage
- `routed` RIUs missing recipe or signal support

### Success criteria
- `both` RIU uncovered count reduced from 17 -> 0 (or near-zero)
- Top traversed `both` RIUs all have eval support

### Priority
**P0**

---

## Problem 6: Company-Library Hydration Debt (Crossref Exists, Company Records Mostly Don’t)

### Problem statement
People signals crossref tracks 43 tools, but 42/43 still show `company_library_status: needs_entry`.

### Why it matters
This blocks durable market intelligence and weakens routing provenance.

The signal graph says what tools matter. The buy-vs-build is where that becomes normalized, queryable intelligence. Right now that bridge is mostly unbuilt.

### Proposed solution
Build a **crossref -> buy-vs-build hydration pipeline**.

### Proposed implementation
For each signal row with `needs_entry`:
1. Normalize company/tool identity
2. Create/merge company record
3. Carry forward:
   - RIU mappings
   - signal strength + recommenders
   - company metadata (funding, stage, URL)
   - docs/pricing/API refs if available
4. Update crossref status to `in_company_library`

### Scope strategy
Start with:
- all `integrate` and `evaluate` action tools
- then top `monitor` by signal tier

### Success criteria
- `needs_entry` count reduced from 42 -> <20 in first pass
- all `integrate` tools hydrated

### Priority
**P1** (but can be partially parallelized after orchestrator v0)

---

## Problem 7: Palette Lacks Knowledge About Its Own Multi-Agent Coordination Needs

### Problem statement
Palette has strong knowledge on client-facing AI system design, but less formalized coverage for patterns Palette itself needs:
- agent handoff and state passing
- memory strategies
- conflict resolution
- decomposition/recomposition
- context budgeting across agents

### Why it matters
This is now a practical bottleneck. The system is becoming the kind of system it lacks internal guidance for.

### Proposed solution
Add a **Palette meta-operations knowledge track** to the knowledge library.

### Proposed implementation
Add entries covering:
- multi-agent handoff protocols
- checkpointing and resumability
- shared state vs long-term memory
- agent role arbitration/conflict patterns
- token/context budget allocation strategies
- orchestration failure handling

### Good framing
This is not “extra research.” It directly supports orchestrator reliability and HandoffPacket quality.

### Success criteria
- Meta-ops knowledge entries exist and are referenced by orchestrator/agent docs
- Fewer ad hoc coordination rules in code

### Priority
**P1**

---

## Problem 8: No Ranking Policy When Layers Conflict

### Problem statement
What happens when:
- routing recommends A
- people signals strongly favor B
- only C has a recipe

No explicit precedence/ranking policy appears to exist yet.

### Why it matters
Without a ranking policy, orchestrator behavior will become inconsistent and hard to debug.

### Proposed solution
Define **Ranking Policy v0** (deterministic, explicit).

### Proposed implementation (example)
Weighted components:
- routing quality/cost score (primary)
- recipe availability bonus (execution readiness)
- people signal confidence modifier
- validation freshness modifier
- fallback penalty for missing pricing/API validation

### Output requirement
Every recommendation should include:
- `why_primary`
- `why_not_alternative`
- `confidence`

### Success criteria
- Same input produces stable ranking output
- Tradeoffs are explainable

### Priority
**P0**

---

## Problem 9: No Completeness/Confidence Score for Traversal Answers

### Problem statement
The future query layer needs a way to communicate answer quality under partial coverage.

### Why it matters
Users need to know whether they received:
- a fully supported recommendation
- a partial recommendation
- a provisional suggestion with missing validation

### Proposed solution
Add a `completeness_score` and `confidence_reasoning`.

### Proposed implementation
Score components:
- knowledge support found
- routing found
- recipe found
- signal validation found
- pricing/API validation freshness
- RIU resolution confidence

### Example
- `completeness_score: 82`
- `confidence: medium`
- `downgrade_reasons: [\"recipe missing\", \"pricing stale\"]`

### Success criteria
- Every traversal response exposes completeness
- Partial outputs are trustworthy and actionable

### Priority
**P0**

---

## Problem 10: No Task-Level Traversal Regression Suite

### Problem statement
There is no explicit regression harness for the product promise:
"Given a task, Palette should traverse layers and return a grounded recommendation."

### Why it matters
Without tests, improvements to routing/hydration/orchestrator may silently regress the core value.

### Proposed solution
Create a **PIS traversal fixture suite**.

### Proposed fixture set (initial 5)
1. Add guardrails to LLM app
2. Choose eval platform
3. Set up voice input modality
4. Create customer demo deck
5. Competitive/alternatives research

### For each fixture, assert
- RIU resolution present
- routing lookup attempted
- recipe lookup attempted
- signal provenance surfaced
- graceful degradation works if data missing

### Success criteria
- CI/local script pass/fail on core traversal behavior

### Priority
**P0**

---

## Problem 11: Schema/Metadata Consistency Drift Risk

### Problem statement
Human-friendly YAML summaries and machine-parsed values can drift (e.g., metadata vs row statuses, summary counts vs row counts).

### Why it matters
Automation and agents will trust machine fields. If metadata is inconsistent, orchestration becomes brittle.

### Proposed solution
Add machine contracts and validation.

### Proposed implementation
- JSON Schema / Pydantic for each major layer
- explicit `schema_version`
- explicit `summary_counts_method` when summary counts are curated
- validation script in `palette/scripts/`

### Success criteria
- Validation catches metadata drift before release
- Agents consume stable schemas

### Priority
**P1**

---

## Problem 12: Routing Outcome Learning Loop Not Implemented

### Problem statement
Routing weights remain static without telemetry and outcome capture.

### Why it matters
The system cannot improve from its own recommendations.

### Proposed solution
Instrument routing decisions and outcomes with a simple telemetry loop (OTel-compatible if possible).

### Proposed implementation
Track:
- task / RIU
- chosen service(s)
- fallbacks
- latency
- cost (estimated vs actual if available)
- success/failure
- human override
- satisfaction/outcome score

Then periodically recompute ranking priors.

### Success criteria
- Routing decisions are logged with IDs
- Ranking adjustments can be traced to observed outcomes

### Priority
**P2** (after orchestrator + fixtures + basic coverage)

---

## Suggested Implementation Order (Recommended)

This is the shortest path from "excellent data foundation" to "working product."

## Phase 1 — Prove the Core Product (P0)

### 1. Minimal Traversal Orchestrator v0
- Deterministic, layer-by-layer lookup
- Structured output with provenance
- No fancy reasoning required

### 2. Ranking Policy v0
- Explicit precedence and weighting across routing/recipe/signals
- Stable and explainable output

### 3. Graceful Degradation Rules
- Partial answers with gap flags
- No silent failure

### 4. Completeness/Confidence Scoring
- Tell users how complete the answer is

### 5. Traversal Regression Fixtures (5 cases)
- Lock the product promise into tests

---

## Phase 2 — Make the Agents Coordinate (P0/P1 boundary)

### 6. HandoffPacket v2 / Shared Task State
- Persist Resolver -> Researcher -> Orchestrator handoffs
- Add replay/debug path

### 7. Connect Resolver -> Traversal (and optional Researcher fallback)
- Resolver resolves RIU
- Orchestrator traverses layers
- Researcher used only when a layer is missing or stale

---

## Phase 3 — Fill the Most Painful Data Gaps (P0/P1)

### 8. Usage-Driven Service Routing Stub Burn-Down
- Prioritize by actual traversal failures and query frequency

### 9. Knowledge Coverage Gates for `both` RIUs
- Fill the 17 uncovered `both` RIUs first

### 10. Focused Company-Library Hydration
- Hydrate all `integrate` + `evaluate` tools first

---

## Phase 4 — Increase System Intelligence (P1/P2)

### 11. Palette Meta-Ops Knowledge Track
- Agent memory/coordination/handoff patterns

### 12. Schema Validation + Drift Detection
- Pydantic/JSON Schema + validation scripts

### 13. Routing Telemetry + Outcome Feedback Loop
- OTel/OpenInference-friendly instrumentation

---

## Overall Comments (Perspective)

From my perspective, the project is in a good place strategically, even if it feels unfinished operationally.

### What you got right (and this matters)
- You built the **data foundation before the query layer**
- You enforced **source quality early**
- You modeled the problem in terms of **task semantics (RIUs)** instead of tool categories
- You separated **signal**, **routing**, and **integration** as distinct concerns

That is the right architecture for the long-term goal.

### Where the system now needs to evolve
It needs to shift from:
- "curated intelligence corpus"

to:
- "deterministic, inspectable traversal engine with graceful fallbacks"

The next milestone is not “more knowledge.” It is a working traversal output that makes a user say:

> “This system took my problem and gave me a grounded recommendation with a real path to implementation.”

Once that exists, every additional layer (hydration, telemetry, reranking, memory) compounds value instead of just adding data.

### Practical interpretation of where you are
- Foundation quality: high
- Product behavior (PIS traversal): early
- Automation sustainability: emerging
- Differentiation potential: high, if orchestrator ships soon

---

## Suggested Immediate Next Deliverables (If You Want to Execute This Plan)

1. `fde/palette/docs/PIS_ORCHESTRATOR_V0_SPEC.md`
2. `fde/palette/core/schema/HandoffPacket_v2.schema.yaml`
3. `fde/palette/scripts/pis_traversal_fixture_runner.py`
4. `fde/palette/scripts/library_coverage_audit.py`

These four deliverables would convert this analysis into execution quickly.

