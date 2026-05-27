# Kiro Build Spec — 6 Intents for BDB
**Date**: 2026-05-27
**From**: claude.analysis
**To**: kiro.design
**Status**: LOCKED — build from this, do not reopen strategy
**Source**: `INTENT_CONVERGENCE_REPORT_2026-05-27.md` (crew-converged)

---

## What You're Building

6 CLI commands. Each takes a query, runs through the execution grammar, produces a typed artifact on disk.

```
palette protect <query>
palette research <query>
palette decide <query>
palette create <query>       # --audience flag optional
palette diagnose <query>     # `palette fix` = alias
palette reflect <query>
```

## Execution Grammar (Every Intent)

```
intent → RIU → boundary → integrity card → recipe/tool → artifact → memory → integrity signal
```

Every intent follows this flow. The differences are which steps are heavy vs. stubbed.

## Build Order

| # | Intent | Hours | BDB Demo? | Priority |
|---|---|---|---|---|
| 1 | PROTECT | 4h | Moment 1 | **P0 — start here** |
| 2 | RESEARCH | 3h | Moment 2 | P0 |
| 3 | DECIDE | 6h | Moment 3 | P0 |
| 4 | REFLECT | 4h | Thesis only | P1 |
| 5 | DIAGNOSE | 5h | Thesis only | P1 |
| 6 | CREATE | 8h | Thesis only | P2 |

**Total: ~30 hours. BDB-critical path: PROTECT + RESEARCH + DECIDE = 13 hours.**

---

## Shared Infrastructure (Build First, ~2h)

### 1. Intent State Object

```python
@dataclass
class IntentState:
    intent: str              # PROTECT, RESEARCH, DECIDE, etc.
    query: str               # user input
    riu: str | None          # resolved RIU ID
    boundary: str            # local_only, governed_external
    posture: str             # execute, execute_with_limitations, etc.
    integrity_card: dict     # from integrity engine
    transition_depth: int    # starts at 0, max 2
    matter_id: str | None    # links artifacts within a matter
    artifacts: list          # accumulated artifact refs this session
```

### 2. Palette Checkpoint

```python
def palette_checkpoint(state: IntentState) -> IntentState:
    card = integrity_card(state.riu)
    if card.posture == "blocked_by_boundary":
        return state.transition_to("PROTECT")
    if card.posture == "governance_required":
        return state.transition_to("GOVERN")
    if state.transition_depth > 2:
        return state.halt_and_escalate("Recursive Intent Oscillation")
    if state.governance_changed():
        return state.transition_to("PROTECT")
    if state.confidence_sufficient():
        return state.transition_to("DECIDE")
    if state.artifact_failed():
        return state.transition_to("DIAGNOSE")
    return state
```

### 3. Integrity Card Builder

Call existing `integrity.py` for the resolved RIU. Map completeness/gaps to posture:

```python
def integrity_card(riu_id: str) -> IntegrityCard:
    """Build card from existing integrity engine."""
    # Use existing integrity checks for this RIU:
    # - knowledge coverage
    # - routing coverage  
    # - recipe coverage
    # - people/tool signals
    # Map to posture:
    posture = "execute"
    if not has_knowledge_coverage(riu_id):
        posture = "research_or_reflect_first"
    if not has_recipe_coverage(riu_id):
        posture = "execute_with_limitations"
    if is_internal_only(riu_id) and requested_external:
        posture = "blocked_by_boundary"
    return IntegrityCard(riu_id=riu_id, posture=posture, ...)
```

### 4. Integrity Cache

```
.palette/integrity_cache.json
```

Session-persistent JSON. Tracks recipe performance (success rate, latency, schema fidelity). If a recipe fails 3 times → auto-demote posture for the rest of the day. No human touch needed.

### 5. Artifact Storage

```
.palette/artifacts/
├── gate_decision/
├── evidence_brief/
├── decision_record/
├── artifact_lineage/
├── failure_lesson/
└── improvement_proposal/
```

Each artifact: markdown file with YAML frontmatter. Frontmatter is the typed schema (parseable). Body is human-readable.

### 6. UNVALIDATED_FALLBACK

When integrity returns `research_or_reflect_first` but user needs an answer:
- Log gap signal (background STORE)
- Answer using local-only base model reasoning
- Tag artifact: `status: UNVALIDATED_FALLBACK`
- CLI output: yellow ANSI `[!] UNVALIDATED` header — visually distinct

---

## Intent 1: PROTECT (4h)

**Anxiety**: "I might leak something"
**Artifact**: `GateDecision`

### Schema

```yaml
---
artifact_type: GateDecision
intent: PROTECT
timestamp: 2026-05-27T12:00:00Z
matter_id: sarah-llc-001
boundary: local_only
action: BLOCK           # BLOCK or ALLOW
reason: "strategy language detected"
blocked_entities: ["our exposure", "majority member"]
redaction_map:
  "[Entity A]": "majority member"   # ephemeral, session-only
safe_rewrite: null       # sanitized query if ALLOW
---
# Human-readable explanation below
```

### Validation Rules
- `blocked_entities` must be non-empty if `action = BLOCK`
- `redaction_map` must use consistent tokens (`[Entity A]`, `[Entity B]`)

### What Exists
- `sanitizer.py` — PII detection (regex + patterns)
- `gateway.__init__.py` — `needs_external()` confidence gate
- `palette_query.py` step_route — classification before external call
- RIU-700 (privilege risk) in taxonomy

### What to Build
1. `palette protect <query>` CLI entry point
2. Classify query via resolver → get RIU
3. Call integrity_card(riu) → check routing classification
4. Run sanitizer with **referential redaction** (tokens, not deletion)
5. Emit GateDecision artifact to `.palette/artifacts/gate_decision/`
6. If ALLOW: output sanitized query ready for RESEARCH transition
7. If BLOCK: explain why, stay local
8. Default if classification fails: `local_only` (fail safe)

### Transition
- PROTECT → RESEARCH: when query is sanitized and safe for external

---

## Intent 2: RESEARCH (3h)

**Anxiety**: "I don't know what's true"
**Artifact**: `EvidenceBrief`

### Schema

```yaml
---
artifact_type: EvidenceBrief
intent: RESEARCH
timestamp: 2026-05-27T12:05:00Z
matter_id: sarah-llc-001
boundary: governed_external
riu_id: RIU-701
local_canon:
  - id: KL-123
    content: "Delaware LLC Act §18-1104..."
    evidence_tier: 1
external_delta:
  - source: "perplexity"
    content: "Recent case Heppner v. Agiloft..."
    url: "..."
contradictions: null     # or explicit string if external contradicts local
confidence: 85
status: VALIDATED        # or UNVALIDATED_FALLBACK
---
# Synthesized brief below
```

### Validation Rules
- `contradictions` cannot overwrite `local_canon` — if external contradicts local, local is canonical, flag the contradiction
- `local_canon` and `external_delta` must be physically separated (no mixing)

### What Exists
- `palette_query.py` — full 5-step pipeline (RESOLVE→RETRIEVE→ROUTE→RESPOND→EXTRACT)
- `PerplexityGateway` — sanitization, caching, rate limiting, audit
- `palette_retrieve.py` — hybrid FTS5 + keyword retrieval
- Knowledge Library (193 entries)

### What to Build
1. `palette research <query>` CLI entry point
2. Resolve RIU → integrity card → check posture
3. Retrieve local knowledge for this RIU (existing `palette_retrieve`)
4. If posture allows external: run Perplexity via gateway (existing)
5. **Perplexity adapter**: map raw Perplexity output → EvidenceBrief schema (~50 lines)
6. **Re-evaluation hook**: check integrity card boundary immediately before Perplexity call
7. Synthesize: local_canon + external_delta → brief (Claude or local)
8. Emit EvidenceBrief artifact
9. If Perplexity fails: emit `recipe_failure` integrity signal → update cache → degrade to local-only with `UNVALIDATED_FALLBACK`
10. If no results at all: auto-transition to REFLECT (log gap)

### Transition
- RESEARCH → DECIDE: when evidence confidence ≥ threshold

---

## Intent 3: DECIDE (6h)

**Anxiety**: "I don't know what to do"
**Artifact**: `DecisionRecord`

### Schema

```yaml
---
artifact_type: DecisionRecord
intent: DECIDE
timestamp: 2026-05-27T12:15:00Z
matter_id: sarah-llc-001
boundary: local_only
riu_id: RIU-701
recommendation: "..."
evidence_sources:
  - artifact_ref: evidence_brief/2026-05-27T120500Z.md
  - artifact_ref: gate_decision/2026-05-27T120000Z.md
strongest_counterargument: ">50 words mandatory..."
change_my_mind_trigger: "If discovery reveals no self-dealing transactions"
reversibility: TWO_WAY
checkpoint_required: false
status: VALIDATED
---
# Decision rationale below
```

### Validation Rules
- `strongest_counterargument` must be > 50 words (anti-sycophancy)
- `change_my_mind_trigger` must name a specific metric or event
- If `reversibility = ONE_WAY` → `checkpoint_required = true`
- Must reference prior artifacts via `evidence_sources` (compounding)

### What Exists
- `decisions.md` append-only log
- ONE-WAY/TWO-WAY door classification in palette-core.md
- `para_decision.py` script (parallel decision analysis)

### What to Build
1. `palette decide <query>` CLI entry point
2. Resolve RIU → integrity card → check posture
3. Retrieve local knowledge + **prior artifacts from this matter_id** (compounding)
4. Check: is this a ONE-WAY DOOR? If yes → set `checkpoint_required = true`
5. Generate recommendation via local model (Ollama or Claude governed)
6. **Mandatory adversarial critique**: run a second model call specifically for counterargument
7. If `strongest_counterargument` < 50 words → reject, re-run critique
8. Emit DecisionRecord artifact
9. Append to `decisions.md` (existing pattern)
10. **This is the compounding moment**: the demo shows that DECIDE connects to PROTECT + RESEARCH artifacts from earlier in the session

### Transition
- DECIDE → RESEARCH: when evidence is thin
- DECIDE → CREATE: when decision implies building an artifact

---

## Intent 4: REFLECT (4h)

**Anxiety**: "I don't want to lose the lesson"
**Artifact**: `ImprovementProposal`

### Schema

```yaml
---
artifact_type: ImprovementProposal
intent: REFLECT
timestamp: 2026-05-27T18:00:00Z
matter_id: null
lesson: "..."
patterns:
  - "Delaware LLC queries lack KL coverage"
proposed_action: "Add KL entry for Delaware fiduciary duty standards"
target_file: "wiki/proposed/KL-PROP-delaware-fiduciary.yaml"
status: PROPOSED      # never PROMOTED directly
---
# Reflection narrative below
```

### Validation Rules
- `target_file` MUST be in `wiki/proposed/` — **Write-Lock Membrane**
- NO write access to `taxonomy/` or `knowledge-library/` directly
- Promotion requires GOVERN primitive (existing wiki governance pipeline)

### What Exists
- `auto_enrich.py` — proposes KL entries from gap signals
- `gap_signals.ndjson` — accumulated signals
- Wiki governance pipeline (propose → vote → promote)

### What to Build
1. `palette reflect <query>` CLI entry point
2. Read session artifacts + gap signals
3. Identify patterns across artifacts
4. Propose improvements → emit ImprovementProposal
5. File to `wiki/proposed/` queue
6. If proposal requires source-of-truth mutation → transition to GOVERN

### Transition
- REFLECT → CREATE: when lesson should become a template
- REFLECT → GOVERN: when lesson proposes taxonomy/KL/governance change

---

## Intent 5: DIAGNOSE (5h)

**Anxiety**: "Something is wrong"
**Artifact**: `FailureLesson`

### Schema

```yaml
---
artifact_type: FailureLesson
intent: DIAGNOSE
timestamp: 2026-05-27T14:00:00Z
matter_id: null
symptom: "Privileged query routed externally"
five_whys:
  - "1. Why did it route externally? → sanitizer returned ALLOW"
  - "2. Why did sanitizer allow it? → strategy language not in pattern list"
  - "3. Why is strategy language missing? → patterns focus on PII, not privilege"
  - "4. Why only PII patterns? → original sanitizer built for GDPR, not legal privilege"
  - "5. Why no legal privilege patterns? → legal taxonomy (RIU-700s) added after sanitizer was built"
root_cause_isolated: true
architectural_patch: "Add legal privilege patterns to sanitizer from RIU-700 taxonomy"
fix_verified: false
tests_added: []
status: OPEN
---
# Diagnosis narrative below
```

### Validation Rules
- `five_whys` must have exactly 5 entries
- `root_cause_isolated` must be `true` before any fix is attempted
- Validator rejects if `five_whys.length < 5` or `root_cause_isolated = false`

### What Exists
- Debugger agent v2 (22 tests passing)
- Remediation loop (validator → debugger → builder)
- `test_loop.py` integration test

### What to Build
1. `palette diagnose <query>` CLI entry point (+ `palette fix` alias)
2. Classify failure type via resolver
3. Check integrity card: is this tied to a known RIU, prior lesson, recipe gap?
4. Run 5-whys analysis (model-assisted, schema-enforced)
5. Emit FailureLesson artifact
6. If fix requires new capability → transition to CREATE

### Transition
- DIAGNOSE → CREATE: when root cause is bounded, fix is a new artifact
- DIAGNOSE → RESEARCH: when root cause is unknown

---

## Intent 6: CREATE (8h)

**Anxiety**: "I need something real"
**Artifact**: `ArtifactLineage`

### Schema

```yaml
---
artifact_type: ArtifactLineage
intent: CREATE
timestamp: 2026-05-27T15:00:00Z
matter_id: sarah-llc-001
boundary: local_only
spec: "Draft client update memo for fiduciary case"
constraints:
  - "No client names in output"
  - "Reference only public legal doctrine"
  - "Max 500 words"
artifact_path: "./artifacts/client-update-2026-05-27.md"
iterations: 1
max_iterations: 3
audience: null           # or "judge", "client", "board"
models_used: ["ollama/llama3"]
provenance:
  - evidence_brief/2026-05-27T120500Z.md
  - decision_record/2026-05-27T121500Z.md
status: VALIDATED
---
# Created artifact below or at artifact_path
```

### Validation Rules
- `max_iterations <= 3` — after 3 loops, force transition to DIAGNOSE
- `constraints` from spec step must be injected into system prompt of EVERY subsequent iteration (constraint anchoring)
- If `--audience` flag set: load audience lens, frame accordingly

### What Exists
- Builder agent (agents/builder/)
- Remediation loop (validator → debugger → builder)
- SDK agent_base

### What to Build
1. `palette create <query>` CLI entry point (with `--audience` optional flag)
2. Classify artifact type via resolver
3. Check integrity card: does RIU have recipe path + artifact contract?
4. Spec step: define what to build (constraints, non-goals)
5. Build step: generate artifact
6. Review step: validate against spec constraints
7. If review fails and iterations < 3: rebuild with feedback
8. If iterations >= 3: transition to DIAGNOSE
9. Emit ArtifactLineage artifact with full provenance

### Transition
- CREATE → DIAGNOSE: when artifact fails validation
- CREATE → PROTECT: when artifact contains sensitive content before publish

---

## Gemini's 3 Polish Items (Integrate During Build)

1. **Integrity Cache** (`.palette/integrity_cache.json`): Track recipe performance. 3 failures → auto-demote posture. Build into shared infrastructure, not per-intent.

2. **Amber State UI**: UNVALIDATED_FALLBACK output gets yellow ANSI `[!] UNVALIDATED` frame. Build into artifact display helper, not per-intent.

3. **Matter-ID Linkage**: Every EvidenceBrief and DecisionRecord includes `matter_id` in frontmatter. Already in schemas above. REFLECT sweeps by `matter_id` to find cross-artifact patterns.

---

## System Guardrails (From Mistral, build into shared infra)

- **Context Firewall**: On intent transition to lower security tier → purge raw text of higher-tier artifacts, replace with `[Reference: DecisionRecord-1044 (Privileged)]`
- **Checkpoint Semaphores**: `palette_checkpoint()` synchronous, thread-locked. Priority: PROTECT > DIAGNOSE > RESEARCH > DECIDE > CREATE > REFLECT
- **Transition Depth Limit**: `transition_depth > 2` → halt_and_escalate

---

## Definition of Done

Each intent is DONE when:
1. `palette <intent> <query>` runs end-to-end from CLI
2. Produces a typed artifact in `.palette/artifacts/<type>/`
3. Artifact passes schema validation (required fields, validation rules)
4. Integrity card is checked before execution
5. Integrity signal emitted after execution (success/failure)
6. Transitions work (at least one transition tested per intent)

**For BDB demo specifically**: PROTECT → RESEARCH → DECIDE runs as a continuous Sarah scenario. Three artifacts produced. Compounding visible (DECIDE references prior PROTECT + RESEARCH artifacts).

---

*Build spec by claude.analysis for kiro.design. Derived from crew-converged INTENT_CONVERGENCE_REPORT_2026-05-27.md. All strategy decisions are locked. This document is implementation-only. 2026-05-27.*
