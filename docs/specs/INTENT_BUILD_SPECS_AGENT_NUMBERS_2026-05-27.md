# Intent Build Specs - Agent Numbers

**Date**: 2026-05-27  
**Owner**: codex.implementation  
**Context**: Build-level decomposition for the finalized 6-intent Palette architecture.  
**Source Specs**:

- `docs/specs/INTENT_CONVERGENCE_REPORT_2026-05-27.md`
- `docs/specs/TESSITURA_DESIGN_6_INTENTS.md`
- `docs/specs/CODEX_INTEGRITY_ENGINE_INTENT_ADDENDUM_2026-05-27.md`

---

## Final Execution Grammar

```text
intent -> RIU -> boundary -> integrity card -> recipe/tool -> artifact -> memory -> integrity signal
```

This spec turns that grammar into build units, runtime agent ownership, and crew review numbers.

---

## Scope Boundary

### BDB Must Ship

Only the demo-critical path must be hard-wired:

```text
PROTECT -> RESEARCH -> DECIDE
```

With supporting minimums:

- typed artifact schemas for all 6 intents
- integrity posture hook for the demo path
- `.palette/artifacts/` storage
- `UNVALIDATED_FALLBACK`
- Perplexity -> `EvidenceBrief` adapter
- `REFLECT -> GOVERN` as proposal-only, no source-of-truth mutation

### Post-BDB May Harden

- full `CREATE`
- full `DIAGNOSE`
- full `REFLECT`
- recipe success/failure feedback for every recipe
- tessitura enforcement across all surfaces
- full intent transition matrix beyond demo path

---

## Build Unit Numbers

| # | Build Unit | Purpose | Primary Runtime Agent | Crew Owner | Estimate | BDB Priority |
|---|---|---|---|---|---:|---|
| 1 | Intent CLI shell | `palette protect/research/decide/...` entrypoints | resolver | Kiro + Codex | 2h | P0 |
| 2 | Intent resolver | Map utterance to intent + RIU + guard intents | resolver | Kiro | 3h | P0 |
| 3 | Artifact schemas | Pydantic/dataclass contracts for 6 artifacts | validator | Codex | 3h | P0 |
| 4 | Artifact storage | `.palette/artifacts/<intent>/<timestamp>.md` with YAML frontmatter | orchestrator | Codex | 2h | P0 |
| 5 | Integrity posture adapter | Call existing integrity card and map to posture | health / total-health | Codex | 3h | P0 |
| 6 | Checkpoint function | Transition logic + depth limit + priority ordering | orchestrator | Kiro | 2h | P0 |
| 7 | PROTECT intent | Sensitivity scan, boundary decision, GateDecision | validator / monitor | Kiro | 4h | P0 |
| 8 | RESEARCH intent | Local first, external sanitized query, EvidenceBrief | researcher | Kiro | 3h | P0 |
| 9 | Perplexity adapter | Convert Perplexity output to EvidenceBrief schema | researcher | Codex | 1.5h | P0 |
| 10 | UNVALIDATED_FALLBACK | Continue locally with warning and gap signal | resolver / researcher | Codex | 2h | P0 |
| 11 | DECIDE intent | DecisionRecord with counterargument/reversibility | architect / validator | Kiro | 6h | P1 |
| 12 | Context firewall | Purge high-tier raw text on boundary downgrade | validator / orchestrator | Codex | 3h | P1 |
| 13 | REFLECT minimal | ImprovementProposal only; GOVERN handoff; no mutation | total-health / orchestrator | Kiro | 4h | P1 |
| 14 | Integrity signal loop | recipe_success/failure emits feedback signal | monitor / health | Codex | 3h | P1 |
| 15 | DIAGNOSE minimal | FailureLesson + 5 whys + no-code-before-root-cause | debugger / remediation | Kiro | 5h | P2 |
| 16 | CREATE minimal | ArtifactLineage, max 3 iterations, audience flag | builder / narrator | Kiro | 8h | P2 |
| 17 | Tessitura behavior layer | Required moves + stance per intent, no persona prompts | orchestrator | Mistral + Codex | 2h | P2 |
| 18 | Validation suite | schema tests, posture tests, transition tests | validator | Gemini + Codex | 4h | P0/P1 |

### Total Implementation Estimate

```text
P0 demo spine: 25.5h
P1 credibility hardening: 18h
P2 full 6-intent polish: 15h
Total full build: 58.5h
```

This is larger than the earlier 30h because it includes infrastructure glue, tests, storage, adapters, and guardrails. The original 30h was intent behavior only.

Recommended BDB build commitment:

```text
Ship P0 + DECIDE from P1 = ~31.5h
Defer the rest unless time remains.
```

---

## Runtime Palette Agent Ownership

These are the runtime responsibilities inside Palette. This is not crew labor; this is how the system should route work.

| Runtime Agent | Owns | Intent Touchpoints | Required Outputs | Estimate To Wire |
|---|---|---|---|---:|
| resolver | first-pass intent + RIU classification | all intents | `IntentRoute` | 3h |
| validator | artifact validation, boundary checks, GO/NO-GO | PROTECT, DECIDE, CREATE | validation verdicts | 4h |
| researcher | local retrieval + governed external research | RESEARCH, DECIDE | `EvidenceBrief` inputs | 4.5h |
| architect | tradeoff reasoning and reversibility | DECIDE, CREATE | `DecisionRecord` reasoning | 3h |
| builder | artifact implementation | CREATE | `ArtifactLineage` | 4h |
| narrator | audience-specific creation | CREATE `--audience` | audience variant metadata | 1.5h |
| debugger | failure isolation | DIAGNOSE | `FailureLesson` | 3h |
| remediation | validator -> debugger -> builder loop | DIAGNOSE, CREATE | repair handoff | 2h |
| monitor | integrity signal emission | PROTECT, RESEARCH, DIAGNOSE | recipe success/failure signal | 2h |
| health | existing integrity health checks | all intents | posture source | 2h |
| total-health | cross-layer integrity and reflection | REFLECT | `ImprovementProposal` | 3h |
| orchestrator | transitions, checkpoint, storage | all intents | state machine updates | 5h |
| business-plan-creation | no BDB intent runtime dependency | none for MVP | none | 0h |

Runtime wiring total if fully integrated: ~37h. BDB should wire only resolver, validator, researcher, architect, health, orchestrator, and minimal monitor.

---

## Crew Numbers

This is the practical assignment model for the current crew.

| Crew Agent | Build/Review Role | Concrete Work | Estimate | Critical Path? |
|---|---|---|---:|---|
| Kiro | primary builder | CLI, resolver, checkpoint, PROTECT, RESEARCH, DECIDE | 20h | yes |
| Codex | implementation hardening | schemas, storage, integrity posture adapter, Perplexity adapter, fallback, context firewall | 14.5h | yes |
| Gemini / Specialist | validation and adversarial testing | transition tests, boundary downgrade tests, recursive loop tests, artifact schema stress | 4h | yes |
| Mistral | implementation contract review | tessitura guardrails, schema strictness, no-overbuild review | 2h | no, but valuable |
| Claude | synthesis and docs | keep convergence/build docs current, demo wording alignment | 2h | no |
| Operator | product decision | crew vote, demo acceptance, scope cuts | 1h | yes |

Minimum BDB critical path:

```text
Kiro 16h + Codex 10h + Gemini 3h + Operator 1h = ~30h
```

Full polished path:

```text
Kiro 20h + Codex 14.5h + Gemini 4h + Mistral 2h + Claude 2h + Operator 1h = ~43.5 crew-hours
```

---

## Intent-Level Build Specs

### 1. PROTECT

**Runtime owner**: `validator` primary, `monitor` secondary  
**Crew owner**: Kiro primary, Codex review  
**Estimate**: 4h  
**Artifact**: `GateDecision`

Required fields:

```yaml
boundary: local_only | governed_external | open_creation | human_checkpoint
action: BLOCK | SANITIZE | ALLOW
blocked_entities: []
redaction_map: {}
riu_id: RIU-xxx
integrity_posture: execute | blocked_by_boundary | narrow_or_confirm
```

Build tasks:

1. Add `palette protect <query>` CLI command.
2. Map legal/private examples to `RIU-700`, `RIU-012`, or local-only posture.
3. Default unclear boundary to `local_only`.
4. Emit `GateDecision` to `.palette/artifacts/protect/`.
5. Before any external research call, require PROTECT pass or sanitized query.

Acceptance checks:

- Client-specific query is blocked or sanitized.
- Public legal query is allowed as governed external.
- Unclear query defaults local-only.
- GateDecision includes blocked entities if action is `BLOCK`.

---

### 2. RESEARCH

**Runtime owner**: `researcher`  
**Crew owner**: Kiro primary, Codex adapter  
**Estimate**: 3h + 1.5h adapter  
**Artifact**: `EvidenceBrief`

Required fields:

```yaml
local_canon: []
external_delta: []
contradictions: []
sanitized_query: ""
sources: []
status: VALIDATED | UNVALIDATED_FALLBACK
integrity_posture: execute | execute_with_limitations | research_or_reflect_first
```

Build tasks:

1. Add `palette research <query>` CLI command.
2. Retrieve local KL first.
3. Run PROTECT/sanitizer before external search.
4. Route governed external query to Perplexity adapter.
5. Map Perplexity response into `EvidenceBrief`.
6. If no external result or weak KL coverage, return `UNVALIDATED_FALLBACK` with warning.
7. Emit `research_gap` or `recipe_failure` integrity signal when needed.

Acceptance checks:

- External result cannot overwrite `local_canon`.
- Contradictions are represented separately.
- Perplexity failure returns fallback, not crash.
- EvidenceBrief persists under `.palette/artifacts/research/`.

---

### 3. DECIDE

**Runtime owner**: `architect` primary, `validator` secondary  
**Crew owner**: Kiro  
**Estimate**: 6h  
**Artifact**: `DecisionRecord`

Required fields:

```yaml
recommendation: ""
options_considered: []
strongest_counterargument: ""
reversibility: two_way | one_way
checkpoint_required: true | false
change_my_mind_trigger: ""
evidence_refs: []
integrity_posture: execute | execute_with_limitations | governance_required
```

Build tasks:

1. Add `palette decide <query>` CLI command.
2. Require an EvidenceBrief or local evidence refs when confidence is not obvious.
3. If evidence thin, transition to `RESEARCH` or mark `UNVALIDATED_FALLBACK`.
4. Always include strongest counterargument.
5. Classify reversibility.
6. If one-way/source-of-truth decision, set checkpoint or GOVERN handoff.

Acceptance checks:

- No DecisionRecord without counterargument.
- One-way decision triggers checkpoint.
- Thin evidence transitions to RESEARCH or marks fallback.
- DecisionRecord links to EvidenceBrief when present.

---

### 4. REFLECT

**Runtime owner**: `total-health` primary, `orchestrator` secondary  
**Crew owner**: Kiro  
**Estimate**: 4h minimal  
**Artifact**: `ImprovementProposal`

Required fields:

```yaml
lesson: ""
pattern_evidence: []
proposed_action: add_kl | update_recipe | propose_riu | governance_review | monitor_only
target_file: "wiki/proposed/..."
governance_required: true
integrity_signal: ""
```

Build tasks:

1. Add `palette reflect <artifact_ref>` CLI command.
2. Read prior typed artifacts.
3. Extract lesson and proposed action.
4. Write proposal only under governed/proposed path.
5. Emit `REFLECT -> GOVERN` if source-of-truth would change.

Acceptance checks:

- Cannot write directly to taxonomy or knowledge library.
- Proposed source-of-truth changes become governance proposals.
- ImprovementProposal persists under `.palette/artifacts/reflect/`.

---

### 5. DIAGNOSE

**Runtime owner**: `debugger` primary, `remediation` secondary  
**Crew owner**: Kiro  
**Estimate**: 5h  
**Artifact**: `FailureLesson`

Required fields:

```yaml
symptom: ""
five_whys: []
root_cause_isolated: true | false
minimal_fix_spec: ""
verification_plan: []
patch_allowed: true | false
```

Build tasks:

1. Add `palette diagnose <failure>` CLI command.
2. Enforce 5-whys structure.
3. No patch/build handoff until `root_cause_isolated = true`.
4. If recipe failure triggered DIAGNOSE, include recipe key and failure signal.

Acceptance checks:

- `five_whys.length == 5`.
- `patch_allowed` false until root cause isolated.
- FailureLesson persists under `.palette/artifacts/diagnose/`.

---

### 6. CREATE

**Runtime owner**: `builder` primary, `narrator` when `--audience`  
**Crew owner**: Kiro  
**Estimate**: 8h  
**Artifact**: `ArtifactLineage`

Required fields:

```yaml
spec: ""
constraints: []
negative_constraints: []
iterations: []
max_iterations: 3
artifact_path: ""
review_result: pass | fail | unvalidated
```

Build tasks:

1. Add `palette create <request>` CLI command.
2. Capture spec before build.
3. Enforce max 3 iterations.
4. If artifact fails validation, transition to DIAGNOSE.
5. If `--audience`, apply EXPLAIN-like framing as modifier, not separate intent.

Acceptance checks:

- No CREATE without spec.
- Iteration count cannot exceed 3.
- Failed validation transitions to DIAGNOSE.
- ArtifactLineage persists under `.palette/artifacts/create/`.

---

## Shared Data Contracts

### `IntentRoute`

```yaml
intent: PROTECT | RESEARCH | DECIDE | CREATE | DIAGNOSE | REFLECT
riu_id: RIU-xxx
secondary_intents: []
guard_intents: []
boundary: local_only | governed_external | open_creation | human_checkpoint
confidence: low | medium | high
lens: legal | ai_adoption | software | general
```

### `IntegrityPosture`

```yaml
riu_id: RIU-xxx
posture: execute | execute_with_limitations | narrow_or_confirm | research_or_reflect_first | blocked_by_boundary | governance_required
completeness_label: full | partial | weak | bare
gaps: []
actions: []
recipe_coverage: []
```

### `IntegritySignal`

```yaml
signal_type: recipe_success | recipe_failure | artifact_validation_failure | fallback_used | boundary_block | governance_handoff
intent: ""
riu_id: ""
artifact_ref: ""
recipe_key: ""
summary: ""
created_at: ""
```

---

## Files To Add Or Touch

Recommended minimal file map:

```text
scripts/palette_intents/
  __init__.py
  cli.py
  schemas.py
  resolver.py
  checkpoint.py
  storage.py
  integrity_adapter.py
  recipe_adapters.py
  intents/
    protect.py
    research.py
    decide.py
    reflect.py
    diagnose.py
    create.py
  tests/
    test_schemas.py
    test_checkpoint.py
    test_protect_research_decide.py
```

Storage path created at runtime:

```text
.palette/artifacts/
  protect/
  research/
  decide/
  create/
  diagnose/
  reflect/
```

Do not mutate source-of-truth files from intent execution. Only write typed artifacts and governance proposals.

---

## Suggested Milestones

### Milestone 1 - Demo Spine (P0, ~25.5h)

- CLI shell
- schemas
- storage
- resolver minimal
- integrity adapter minimal
- checkpoint minimal
- PROTECT
- RESEARCH
- Perplexity EvidenceBrief adapter
- UNVALIDATED_FALLBACK
- basic tests

Demo proof:

```text
palette protect "client-specific legal strategy"
palette research "Delaware LLC fiduciary duty co-founder self-dealing"
palette decide "Given the evidence, what would opposing counsel argue?"
```

### Milestone 2 - Judgment Closure (P1, +6h)

- DECIDE hardening
- EvidenceBrief -> DecisionRecord linking
- one-way door checkpoint
- context firewall minimal

### Milestone 3 - Compounding Proof (P1, +4h)

- REFLECT minimal
- ImprovementProposal
- REFLECT -> GOVERN handoff

### Milestone 4 - Full Six (P2, +13h)

- DIAGNOSE minimal
- CREATE minimal
- tessitura behavior layer

---

## Recommendation

For BDB, build only this critical path first:

```text
schemas + storage + resolver + integrity adapter + checkpoint
PROTECT + RESEARCH + DECIDE
Perplexity EvidenceBrief adapter
UNVALIDATED_FALLBACK
```

That is the smallest implementation that proves the thesis:

```text
Palette knows when Sarah is protecting, researching, and deciding.
It routes through RIUs, checks integrity, uses recipes, produces typed artifacts, and keeps privileged material local.
```

Everything else can be described as already specified and partially wired for post-BDB expansion.
