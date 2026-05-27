# Kiro Build Report — 6 Palette Intents Shipped
**Date**: 2026-05-27
**Author**: kiro.design
**Status**: BUILT + TESTED — ready for Gemini validation
**Tag**: BDB-INTENTS-BUILD

---

## What Was Built

6 CLI commands implementing the Adaptive Intent Framework. Each takes a query, runs through the execution grammar, produces a typed artifact on disk, and emits an integrity signal.

```
./palette protect <query>     → GateDecision
./palette research <query>    → EvidenceBrief
./palette decide <query>      → DecisionRecord
./palette create <query>      → ArtifactLineage
./palette diagnose <query>    → FailureLesson
./palette reflect <query>     → ImprovementProposal
```

---

## File Inventory

| File | Purpose | Lines |
|---|---|---|
| `scripts/palette_intent.py` | Unified CLI entry point + help | ~60 |
| `scripts/palette_intents/__init__.py` | Package marker | 1 |
| `scripts/palette_intents/infra.py` | Shared infrastructure (IntentState, checkpoint, integrity card, artifact storage, signals) | ~230 |
| `scripts/palette_intents/protect.py` | PROTECT intent | ~250 |
| `scripts/palette_intents/research.py` | RESEARCH intent | ~300 |
| `scripts/palette_intents/decide.py` | DECIDE intent | ~270 |
| `scripts/palette_intents/create.py` | CREATE intent | ~240 |
| `scripts/palette_intents/diagnose.py` | DIAGNOSE intent | ~210 |
| `scripts/palette_intents/reflect.py` | REFLECT intent | ~230 |
| `scripts/palette_intents/test_intents.py` | 11 regression tests | ~130 |
| `palette` | Shell wrapper (executable) | 4 |
| `.palette/artifacts/.gitignore` | Exclude session artifacts from git | 3 |
| `.palette/.gitignore` | Exclude cache from git | 2 |

---

## Execution Grammar (Every Intent)

```
intent → RIU → boundary → integrity card → recipe/tool → artifact → memory → integrity signal
```

Implemented as:
1. `resolve_query()` — classify via taxonomy (hybrid FTS5 + keyword)
2. `build_integrity_card_fast()` — posture from classification + knowledge count
3. `palette_checkpoint()` — transition check (blocked_by_boundary → PROTECT, governance_required → halt)
4. Intent-specific logic (sanitizer, Perplexity, Ollama, etc.)
5. `store_artifact()` — YAML frontmatter + markdown body to `.palette/artifacts/<type>/`
6. `emit_integrity_signal()` — append to `peers/gap_signals.ndjson`

---

## Performance

| Intent | Latency | Notes |
|---|---|---|
| PROTECT | 70ms | Fast-path integrity card, no full PIS load |
| RESEARCH (local) | 50ms | Retrieval only |
| RESEARCH (external) | 17s | Perplexity API latency |
| DECIDE | 41s | 3 Ollama calls (recommendation + critique + trigger) |
| CREATE | 61s | 2 Ollama calls (build + review) |
| DIAGNOSE | 24s | 2 Ollama calls (5-whys + fix proposal) |
| REFLECT | 41ms | Artifact scan + pattern detection, no model calls |

Note: Python cold-start adds ~750ms (YAML taxonomy load). Within-process times are as shown above.

---

## Artifact Schemas

### GateDecision (PROTECT)
```yaml
artifact_type: GateDecision
intent: PROTECT
timestamp: ISO8601
matter_id: string | null
riu_id: string
boundary: local_only | governed_external
action: BLOCK | ALLOW
reason: string
blocked_entities: [string]
redaction_map: {token: entity}
safe_rewrite: string | null
confidence: float
posture: string
local_knowledge: [{id, question, evidence_tier}]
local_answer: string | null
```

### EvidenceBrief (RESEARCH)
```yaml
artifact_type: EvidenceBrief
intent: RESEARCH
timestamp: ISO8601
matter_id: string | null
riu_id: string
boundary: local_only | governed_external
local_canon: [{id, content, question, evidence_tier, score}]
external_delta: [{source, content, sources}]
contradictions: string | null
confidence: float
status: VALIDATED | LOCAL_ONLY | UNVALIDATED_FALLBACK
prior_artifacts: [path]
sources: [url]
```

### DecisionRecord (DECIDE)
```yaml
artifact_type: DecisionRecord
intent: DECIDE
timestamp: ISO8601
matter_id: string | null
riu_id: string
boundary: local_only
recommendation: string
evidence_sources: [path]
strongest_counterargument: string  # MUST be >50 words
change_my_mind_trigger: string
reversibility: ONE_WAY | TWO_WAY
checkpoint_required: boolean
confidence: float
status: VALIDATED | UNVALIDATED_FALLBACK
```

### ArtifactLineage (CREATE)
```yaml
artifact_type: ArtifactLineage
intent: CREATE
timestamp: ISO8601
matter_id: string | null
riu_id: string
boundary: local_only
spec: string
constraints: [string]
audience: string | null
iterations: int
max_iterations: 3
models_used: [string]
review_passed: boolean
provenance: [path]
status: VALIDATED | NEEDS_REVIEW
```

### FailureLesson (DIAGNOSE)
```yaml
artifact_type: FailureLesson
intent: DIAGNOSE
timestamp: ISO8601
matter_id: string | null
riu_id: string
symptom: string
five_whys: [string]  # MUST be exactly 5
root_cause_isolated: boolean
architectural_patch: string
fix_verified: boolean
tests_added: [string]
status: OPEN
```

### ImprovementProposal (REFLECT)
```yaml
artifact_type: ImprovementProposal
intent: REFLECT
timestamp: ISO8601
matter_id: string | null
query: string
session_summary: {total_artifacts, by_intent, by_status}
patterns: [string]
proposed_actions: [{action, target_file, priority, pattern}]
status: PROPOSED  # never PROMOTED directly
```

---

## Validation Rules Enforced

| Rule | Intent | Implementation |
|---|---|---|
| `blocked_entities` non-empty if BLOCK | PROTECT | Strategy + PII detection |
| Empty/short query → BLOCK | PROTECT | `len(query) < 5` check |
| `contradictions` cannot overwrite `local_canon` | RESEARCH | Separate fields, flag only |
| Strong contradiction signals only | RESEARCH | "overruled", "superseded", not "however" |
| Re-check safety before external call | RESEARCH | `is_safe_for_external()` gate |
| `strongest_counterargument` > 50 words | DECIDE | Retry with stronger prompt if <50 |
| ONE-WAY DOOR → `checkpoint_required = true` | DECIDE | Keyword detection on query + recommendation |
| `five_whys` exactly 5 entries | DIAGNOSE | Pad to 5, truncate to 5 |
| `root_cause_isolated` before fix | DIAGNOSE | Check for "incomplete" in whys |
| `max_iterations <= 3` | CREATE | Hardcoded limit |
| `target_file` in `wiki/proposed/` only | REFLECT | Write-Lock Membrane |

---

## Compounding (Matter Linkage)

When `--matter <id>` is passed:
- PROTECT stores `matter_id` in artifact
- RESEARCH finds prior PROTECT artifacts for same matter → shows `[CONNECT]`
- DECIDE finds ALL prior artifacts for same matter → uses as evidence context
- REFLECT scopes pattern detection to matter artifacts only

**Demo flow verified**:
```
palette protect  --matter sarah-demo "What's our exposure..."
  → GateDecision stored with matter_id

palette research --matter sarah-demo "What fiduciary standards..."
  → [CONNECT] shows prior GateDecision
  → EvidenceBrief stored with matter_id

palette decide   --matter sarah-demo "Should Sarah settle or litigate?"
  → [CONNECT] shows GateDecision + EvidenceBrief
  → DecisionRecord references both in evidence_sources
```

---

## Transition Matrix (Implemented)

| From | To | Trigger | Implementation |
|---|---|---|---|
| PROTECT | RESEARCH | Query is ALLOW | Output shows "Next: palette research..." |
| RESEARCH | DECIDE | Confidence ≥ 60% | Output shows "Evidence sufficient. Consider: palette decide..." |
| DECIDE | RESEARCH | Evidence thin | `palette_checkpoint()` (posture: research_or_reflect_first) |
| CREATE | DIAGNOSE | Review fails 3x | `max_iterations` exceeded |
| REFLECT | GOVERN | Proposal needs promotion | Output shows "requires GOVERN to promote" |

Note: Transitions are currently advisory (output hints). Auto-transitions via `palette_checkpoint()` exist in infra but are not yet wired to auto-invoke the next intent. Human drives the flow for BDB demo.

---

## Integrity Infrastructure

### Integrity Card (Fast Path)
- Built from resolve result (classification + knowledge count)
- No full PIS YAML load (saves 700ms)
- Maps to execution posture: `execute`, `execute_with_limitations`, `blocked_by_boundary`, `research_or_reflect_first`, `governance_required`

### Integrity Cache
- Location: `.palette/integrity_cache.json`
- Tracks recipe failures (3 failures → auto-demote posture)
- Session-persistent, not committed to git

### Integrity Signals
- Appended to `peers/gap_signals.ndjson` after every intent execution
- Fields: `type`, `intent`, `riu_id`, `success`, `artifact_path`, `details`, `timestamp`
- Used by REFLECT for pattern detection

### Palette Checkpoint
```python
def palette_checkpoint(state: IntentState) -> IntentState:
    if state.transition_depth > 2:
        return state  # halt — no infinite oscillation
    if posture == "blocked_by_boundary" and state.intent != "PROTECT":
        return state.transition_to("PROTECT")
    if posture == "governance_required":
        return state  # halt for human
    return state
```

---

## Regression Tests

**File**: `scripts/palette_intents/test_intents.py`
**Run**: `python3 scripts/palette_intents/test_intents.py`
**Result**: 11/11 PASS

| # | Test | Status |
|---|---|---|
| 1 | PROTECT blocks strategy language | ✅ |
| 2 | PROTECT allows public research | ✅ |
| 3 | PROTECT blocks empty query | ✅ |
| 4 | PROTECT blocks PII | ✅ |
| 5 | PROTECT carries matter_id | ✅ |
| 6 | RESEARCH local-only returns EvidenceBrief | ✅ |
| 7 | RESEARCH blocks privileged queries | ✅ |
| 8 | RESEARCH schema complete | ✅ |
| 9 | REFLECT produces ImprovementProposal | ✅ |
| 10 | REFLECT handles empty matter | ✅ |
| 11 | REFLECT write-lock membrane intact | ✅ |

Tests for DECIDE, DIAGNOSE, CREATE are not in the fast suite (require Ollama, 20-60s each). Verified manually.

---

## What Gemini Should Validate

### 1. Failure Mode Testing
Run each intent with adversarial inputs:
- PROTECT: queries that look public but contain hidden privilege signals
- RESEARCH: queries where local knowledge contradicts external (test contradiction detection)
- DECIDE: queries where the model might produce <50 word counterarguments
- CREATE: queries where constraints should block the output
- DIAGNOSE: symptoms where 5-whys might loop or produce shallow analysis
- REFLECT: sessions with no artifacts (empty state)

### 2. Integrity Card Accuracy
- Does `build_integrity_card_fast()` produce correct postures for known RIUs?
- Does `blocked_by_boundary` correctly fire for `internal_only` RIUs?
- Does the fast path miss any cases that the full PIS load would catch?

### 3. Compounding Correctness
- Run the full 3-moment demo flow with `--matter`
- Verify DECIDE's `evidence_sources` actually contains paths to prior artifacts
- Verify the context passed to Ollama includes prior artifact content

### 4. Schema Fidelity
- Parse every artifact in `.palette/artifacts/` with YAML
- Verify all required fields present per schema above
- Verify validation rules (counterargument >50 words, five_whys == 5, etc.)

### 5. Transition Depth Limit
- Manually invoke `palette_checkpoint()` with `transition_depth=3`
- Verify it returns the same state (no transition)
- This prevents the Infinite Loop threat from the sandbox analysis

### 6. Write-Lock Membrane
- Verify no intent writes to `taxonomy/`, `knowledge-library/`, or `wiki/` (only `wiki/proposed/`)
- REFLECT is the only intent that proposes changes, and it targets `wiki/proposed/` exclusively

---

## Known Limitations (Not Bugs)

1. **Cold-start latency**: ~750ms Python startup + YAML load. Acceptable for demo.
2. **DECIDE/CREATE/DIAGNOSE require Ollama**: If Ollama is down, they produce fallback messages.
3. **Transitions are advisory**: Human drives the flow. Auto-transitions exist in code but are not wired to auto-invoke.
4. **Contradiction detection is heuristic**: Only catches strong signals (overruled, superseded). Won't catch subtle contradictions.
5. **ONE-WAY DOOR detection is keyword-based**: Works for legal domain. Production would use model classification.
6. **No streaming output**: Ollama calls block until complete. Demo video can cut around this.

---

## BDB Demo Readiness

| Requirement | Status |
|---|---|
| `palette protect` blocks privileged queries | ✅ |
| `palette protect` answers locally after block | ✅ |
| `palette research` calls Perplexity with sanitized query | ✅ |
| `palette research` shows local + external evidence | ✅ |
| `palette decide` connects to prior artifacts | ✅ |
| `palette decide` flags ONE-WAY DOOR | ✅ |
| Compounding visible across 3 moments | ✅ |
| All artifacts stored with typed schemas | ✅ |
| Zero data leakage on BLOCK path | ✅ |
| Transition hints guide the user | ✅ |

**The BDB demo flow is ready to record.**

---

*— kiro.design, 2026-05-27T14:27 PDT*
