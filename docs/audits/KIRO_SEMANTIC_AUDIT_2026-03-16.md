# Semantic Consistency Audit — Wire Contract Terminology

**Date**: 2026-03-16
**Auditor**: Kiro
**Purpose**: Map all terminology discrepancies between the canonical wire contract, Python SDK, Go core, and agent implementations

---

## The Canonical Contract (as finalized)

**Packet**: `id`, `from`, `to`, `task`, `riu_ids`, `payload`, `trace_id`
**Result**: `packet_id`, `from`, `status`, `output`, `blockers`, `artifacts`, `next_agent`
**Status enum**: `success | failure | blocked`

---

## Discrepancy Map

### 1. Field Name Divergence

| Canonical | Python SDK (`agent_base.py`) | Go Core (`packet.go`) | Notes |
|---|---|---|---|
| `id` | ❌ missing | ✅ `id` | SDK packets have no ID — can't link results to packets |
| `from` | `from_agent` | ✅ `from` | |
| `to` | `to_agent` | ✅ `to` | |
| `task` | ✅ `task` | ✅ `task` | Aligned |
| `riu_ids` | ✅ `riu_ids` | ✅ `riu_ids` | Aligned |
| `payload` | ❌ `context` | ✅ `payload` | SDK uses `context`, canonical uses `payload` |
| `trace_id` | ❌ missing | ✅ `trace_id` | SDK has no trace concept |
| `packet_id` | ❌ missing | ✅ `packet_id` | SDK results can't reference their packet |
| `output` | `outputs` (plural) | ✅ `output` | |
| `blockers` | `gaps` | ✅ `blockers` | Semantic difference — see below |
| `artifacts` | ✅ `artifacts` | `produced_artifacts` | Go uses longer name |
| `next_agent` | ✅ `next_agent` | ✅ `next_agent` | Aligned |
| `status` | ✅ `status` | ✅ `status` | Aligned (but enum values differ) |

**Python SDK has extra fields not in canonical**: `schema_version`, `constraints`, `validation_warnings`

### 2. Status Enum Divergence

| Canonical | Python SDK | Go Core |
|---|---|---|
| `success` | ✅ `success` | ❌ `complete` |
| `failure` | ✅ `failure` | ❌ `escalate` |
| `blocked` | ✅ `blocked` | ✅ `blocked` |
| — | — | ❌ `one_way_door` (extra) |

The Go core uses `complete`/`blocked`/`escalate`/`one_way_door`. The canonical contract uses `success`/`failure`/`blocked`. The Python SDK already uses the canonical values.

The coordination system (`coordination.py`) uses its own set: `pending`/`running`/`success`/`failed`/`completed`. These are internal workflow states, not wire contract statuses, so they're a separate concern.

### 3. `gaps` vs `blockers` — Semantic Difference

This is the most important terminology decision.

| Term | Current meaning in Palette | Canonical contract |
|---|---|---|
| `gaps` | Epistemic: "what we don't know" — knowledge gaps, assumptions, uncertainties | Not used |
| `blockers` | Operational: "what prevented completion" — errors, missing data, permissions | ✅ Used |

**Current usage**:
- Python SDK `HandoffResult.gaps` — used for both epistemic gaps AND operational errors
- Go core `HandoffResult.Blockers` — used for operational blockers only
- Researcher agent — uses `gaps` for epistemic ("decision_context missing") AND operational ("search error")
- Resolver agent — uses `blockers` for operational errors
- IntegrityGate — checks `gaps` field for glass-box compliance

**The problem**: `gaps` conflates two different things. An agent saying "I don't know the pricing" (epistemic) is different from "the API timed out" (operational). The canonical contract chose `blockers` for the wire field, which is the right call for the protocol — but the epistemic `gaps` concept is valuable and shouldn't be lost.

**Recommendation**: Use `blockers` on the wire (canonical). Move epistemic gaps into `output` as a domain-specific field (e.g., `output.gaps` or `output.knowledge_gaps`). This preserves both concepts without overloading the wire field.

### 4. Go Core Extra Fields (not in canonical)

The Go `packet.go` has fields the canonical contract simplified away:

| Go field | In canonical? | Recommendation |
|---|---|---|
| `constraints` | ❌ | Move to `payload` |
| `artifacts` (input) | ❌ | Move to `payload` |
| `one_way_door` | ❌ | Move to `payload` or handle as a status |
| `timestamp` | ❌ | Transport metadata, not protocol |
| `produced_artifacts` | `artifacts` | Rename to `artifacts` |

### 5. JSON Schema vs Go Code vs Canonical

The JSON schemas in `core/schema/` match the Go code, not the canonical contract:
- `packet.schema.json` has 11 fields (canonical has 7)
- `result.schema.json` has 8 fields (canonical has 7)

The schemas need updating to match the simplified canonical contract.

---

## Files That Need Changes for V2.2 Alignment

| File | What changes |
|---|---|
| `sdk/agent_base.py` | Rename fields: `from_agent`→`from`, `to_agent`→`to`, `context`→`payload`, `outputs`→`output`, `gaps`→`blockers`. Add `id`, `trace_id`, `packet_id`. |
| `sdk/__init__.py` | No change (exports class names, not field names) |
| `sdk/integrity_gate.py` | Update field access: `outputs`→`output`, `gaps`→`blockers` |
| `sdk/tests/*.py` | Update all field references |
| `agents/researcher/researcher.py` | Update `gaps=` → `blockers=`, `outputs=` → `output=` |
| `core/packet.go` | Update status enum: `complete`→`success`, `escalate`→`failure`. Remove `one_way_door` status. Rename `produced_artifacts`→`artifacts`. |
| `core/schema/packet.schema.json` | Simplify to 7 canonical fields |
| `core/schema/result.schema.json` | Simplify to 7 canonical fields, rename fields |
| `agents/orchestrator/runner.go` | Remove fallback parsing (won't be needed once aligned) |
| `agents/resolver/resolver.py` | Already uses `blockers` — verify alignment |

---

## What Does NOT Need to Change

- **Coordination system** (`coordination.py`) — uses internal workflow states (`pending`/`running`/`completed`/`failed`), not wire contract statuses. These are a different abstraction layer.
- **IntegrityGate concept** — the glass-box check is valuable regardless of field names. Just update the field it reads.
- **Agent archetypes and Palette governance** — terminology like "convergence," "one-way door," "semantic blueprint" is Palette domain language, not wire contract language. No change needed.
- **Knowledge library, taxonomy, routing** — data layer terminology is separate from wire contract terminology.

---

## Summary

The codebase has 3 dialects of the same protocol:
1. **Go core** (closest to canonical, but has extra fields and different status values)
2. **Python SDK** (different field names, missing `id`/`trace_id`/`packet_id`)
3. **Canonical contract** (the simplification you just finalized)

V2.2 alignment means converging all three to the canonical contract. The Go code is closer — it mostly needs field pruning and status enum updates. The Python SDK needs field renaming and additions. The JSON schemas need simplification.

The `gaps` → `blockers` rename is the only semantically loaded change. Everything else is mechanical.
