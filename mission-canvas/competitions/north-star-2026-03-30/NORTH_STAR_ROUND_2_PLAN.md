# North Star — Round 2 Plan

**Author**: claude.analysis
**Date**: 2026-03-30
**Status**: Ready for team review
**Scope**: Learner system unification + Palette enrichment pipeline + task assignments

---

## Part 1: What Was Built (Complete Inventory)

### Competition Summary

Four agents built independently. All six flywheel arrows now have a first implementation. 240+ tests pass. Three integration issues need fixing before Round 2.

### By Agent

#### Codex — Contextual Coaching Rail
**Arrow activated**: Canvas → Enablement (explanatory questions trigger stateful coaching)

| Deliverable | Description |
|-------------|-------------|
| `workspace_coaching.mjs` (369 lines) | 7 exports: detectCoachingMoment, buildCoachingResponse, loadLearnerLens, saveLearnerLens, verifyMastery, learnerLensPath, findExistingConcept |
| `stress_test_enablement_hook.mjs` | 14 tests covering detection, stage progression, persistence, mastery verification |
| `server.mjs` changes | Coaching intercept in processRoute (fires before normal routing), `/coach` endpoint, `/verify-mastery` endpoint, `learner_summary` in workspace-welcome |
| `workspace_ui.js` + `app.js` + `style.css` | Coaching panel, learning state panel, mastery verification UI |
| `learner_lens.yaml` | Per-workspace file tracking taught_concepts, verified_concepts, stage_counts, concept_progress, teaching_moments |

**Stage model**: orient (first teaching) → retain (recap) → verify (check understanding)
**Concept sources**: Workspace KL entries + 3 hardcoded project concepts (one_way_door, blocked_action, health_score)

#### Kiro — Chain-Level Coaching Annotations
**Arrow activated**: Canvas → Enablement (narration adapts to what user has learned)

| Deliverable | Description |
|-------------|-------------|
| `convergence_chain.mjs` additions | 6 exports: detectCoachingOpportunities, getCoachingDepth, recordConceptExposure, verifyConceptMastery, annotateWithCoaching, extractKeyTerms |
| `server.mjs` changes | Workspace KL attached to project state before chain processing, learner_state persistence after chain queries |
| `KIRO_NORTH_STAR_ENTRY.md` | Full competition entry |

**Depth model**: full (💡 inline hint) → brief (signal only) → none (mastered after 3 exposures or verification)
**Data store**: `learner_state` in project_state object (in-memory, written to project_state.yaml if coaching_signals exist)
**Trigger**: Automatic — fires during every `handleProjectQuery()` call, scanning narration for KL terms

#### Gemini — Date Standardization + Critical Nudge Bypass
**Arrow activated**: None (infrastructure improvement)

| Deliverable | Description |
|-------------|-------------|
| `convergence_chain.mjs` changes | `getISODate()` helper (now used everywhere), critical nudge bypass in `generateNudges()` — critical priority items nudge on day 0 |

Clean, isolated, no conflicts with anyone.

#### Claude — Flywheel Return Path
**Arrows activated**: Canvas → Palette, Canvas → Enablement (decision coaching), Enablement → Palette

| Deliverable | Description |
|-------------|-------------|
| `flywheel_feedback.mjs` (228 lines) | 8 exports: generateKLCandidate, generateDecisionRecord, generateDecisionCoaching, generateMasterySignal, persistFeedback, loadFeedback, getPendingFeedback, markFeedbackIngested |
| `stress_test_flywheel_feedback.mjs` | 75 tests across 8 sections |
| `server.mjs` changes | 3 hooks (resolve-evidence → KL candidate, confirm-one-way-door → decision record + coaching signal, verify-mastery → mastery signal), `/palette-feedback` endpoint |
| `convergence_chain.mjs` fix | Syntax error at line 1373 (orphaned spread operator) |

**Data store**: `palette_feedback.yaml` per workspace — staging area for Palette ingestion
**Entry types**: KLC- (KL candidates), DR- (decision records), MS- (mastery signals)

### All Endpoints (16 total, 6 new from competition)

| Endpoint | Method | Author | Purpose |
|----------|--------|--------|---------|
| `/v1/missioncanvas/health` | GET | Pre-existing | Server status |
| `/v1/missioncanvas/capabilities` | GET | Pre-existing | Feature list |
| `/v1/missioncanvas/workspace-welcome` | POST | **Codex modified** | Now includes `learner_summary` |
| `/v1/missioncanvas/workspaces` | GET | Pre-existing | List workspaces |
| `/v1/missioncanvas/route` | POST | **Kiro modified** | Now returns `coaching_signals` |
| `/v1/missioncanvas/commit` | POST | Pre-existing | Persist decision |
| `/v1/missioncanvas/uncommit` | POST | Pre-existing | Revert decision |
| `/v1/missioncanvas/talk-stream` | POST | Pre-existing | Streaming voice |
| `/v1/missioncanvas/confirm-one-way-door` | POST | **Claude modified** | Now returns `flywheel.coaching_signals` |
| `/v1/missioncanvas/resolve-evidence` | POST | **Claude modified** | Now returns `flywheel.kl_candidate` |
| `/v1/missioncanvas/add-fact` | POST | Pre-existing | Add known fact |
| `/v1/missioncanvas/fetch-signals` | POST | Pre-existing | Signal fetching |
| `/v1/missioncanvas/coach` | POST | **Codex (new)** | Explicit coaching request |
| `/v1/missioncanvas/verify-mastery` | POST | **Codex (new)** | Mark concept mastered |
| `/v1/missioncanvas/palette-feedback` | POST | **Claude (new)** | Palette reads workspace feedback |
| `/v1/missioncanvas/log-append` | POST | Pre-existing | Decision log |

### Test Status

| Suite | Count | Status |
|-------|-------|--------|
| `stress_test_v03_day2.mjs` | 62 | ALL PASS |
| `stress_test_convergence.mjs` | 103 | ALL PASS |
| `stress_test_enablement_hook.mjs` | 14 | ALL PASS |
| `stress_test_flywheel_feedback.mjs` | 75 | ALL PASS |
| **Total** | **254** | **ALL PASS** |

---

## Part 2: Learner System Unification

### The Problem

Two parallel systems track what a user has learned:

| | Kiro's System | Codex's System |
|---|---|---|
| **File** | `project_state.yaml` (learner_state key) | `learner_lens.yaml` (separate file) |
| **Shape** | `{ concepts: { id: { exposures, first_seen, verified } } }` | `{ state: { taught_concepts[], verified_concepts[], concept_progress[], stage_counts }, teaching_moments[] }` |
| **Trigger** | Automatic during chain narration | Explicit explanatory questions |
| **Persistence** | Fragile (only writes if signals exist, not in schema) | Reliable (writes on every coaching call) |
| **Depth model** | exposures count: 0=full, 1-2=brief, 3+=none | times_taught: 1=orient, 2=retain, 3+=verify |
| **UI** | None | Coaching panel + learning state panel |

They never read from each other. A concept can be "mastered" in one and "first encounter" in the other.

### The Decision

**Codex's `learner_lens.yaml` wins.** Reasons:

1. **Richer data model** — stages, teaching moments with full history, verification answers, source tracking
2. **Reliable persistence** — separate file, writes every time, no schema conflict
3. **UI integration** — already wired into workspace_ui.js
4. **Flywheel integration** — Claude's mastery signals read from learner_lens

### The Merge Plan

**Step 1: Modify `annotateWithCoaching()` to use learner_lens** (~20 min)

Currently `annotateWithCoaching` in convergence_chain.mjs reads/writes `ps.learner_state`. Change it to:
- Import `loadLearnerLens` and `saveLearnerLens` from workspace_coaching.mjs
- Accept `workspacesDir` and `workspaceId` parameters (passed from server.mjs)
- Read concept exposure from `learner_lens.state.concept_progress` instead of `learner_state.concepts`
- Map depth: if concept has `times_taught >= 3` or is in `verified_concepts` → 'none'; if `times_taught >= 1` → 'brief'; else → 'full'
- On recording exposure: update `concept_progress` entry (increment times_taught) and save via `saveLearnerLens()`

**Step 2: Remove learner_state from project_state** (~5 min)

- Remove `ps.learner_state = learnerState` write in `annotateWithCoaching()`
- Remove the `updateProjectState` call in server.mjs that only fires for coaching_signals
- Delete `learner_state` key from any project_state.yaml files that have it (check oil-investor, rossi)

**Step 3: Fix routing priority** (~15 min)

In `processRoute()` (server.mjs), flip the order:
```javascript
// FIRST: check if it's a project-state query
const queryDetection = detectProjectQuery(payload.input.objective);
if (queryDetection.detected && workspace) {
  // Run convergence chain (includes Kiro's inline coaching)
  // ...
}

// SECOND: if NOT a project-state query, try coaching intercept
if (workspace) {
  const coachingResult = buildCoachingResponse({...});
  if (coachingResult) { return coachingResult; }
}
```

This means "Why is this blocked?" gets actual chain narration with project state data (+ inline coaching hints), while "What is a crack spread?" still gets the dedicated coaching response.

**Step 4: Wire Kiro's signals into flywheel** (~10 min)

After `handleProjectQuery` returns coaching_signals in server.mjs, persist them:
```javascript
if (chainResult.convergence_chain?.coaching_signals?.length > 0) {
  for (const signal of chainResult.convergence_chain.coaching_signals) {
    persistFeedback(WORKSPACES_DIR, workspaceId, {
      id: `CE-${signal.concept_id}`,
      type: 'concept_exposure',
      concept_id: signal.concept_id,
      workspace_id: workspaceId,
      depth: signal.depth,
      detected_at: getISODate()
    });
  }
}
```

**Step 5: Clean up dead exports** (~5 min)

- Remove `getCoachingDepth` and `verifyConceptMastery` from convergence_chain.mjs exports (superseded by workspace_coaching equivalents)
- Keep `recordConceptExposure` if still used internally by `annotateWithCoaching`, otherwise remove
- Update any imports in server.mjs

**Step 6: Update tests** (~15 min)

- Update `stress_test_convergence.mjs` if it directly tests removed functions
- Add tests confirming unified learner_lens is updated by both coaching paths
- Verify all 254 tests still pass

**Total estimate: ~70 minutes**

---

## Part 3: Palette Enrichment Pipeline Plan

### What It Does

The pipeline automatically consumes feedback from Canvas workspaces and promotes it into Palette's knowledge library. This is the piece that makes the flywheel return path LIVE instead of a staging area.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                 PALETTE ENRICHMENT                    │
│                                                       │
│  1. SCAN: Poll /palette-feedback for each workspace  │
│  2. VALIDATE: Check format, dedup, evidence bar      │
│  3. CLASSIFY: Map to RIU, assign journey stage       │
│  4. PROMOTE: Add to workspace KL (auto) or           │
│     Palette KL v1.4 (requires human review)          │
│  5. INGEST: Mark entries as consumed                  │
│  6. AUDIT: Log all actions to enrichment_log.jsonl   │
└─────────────────────────────────────────────────────┘
```

### Existing Infrastructure to Build On

Palette already has an enrichment pipeline at `palette/scripts/enrichment/`:
- `enrich.py` — CLI orchestrator (scan → fetch → update → validate → log)
- `config.py` — Centralized paths and thresholds
- `profile_scanner.py` — Target identification with priority ranking
- `yaml_updater.py` — Round-trip YAML editing (preserves comments)
- `audit_log.py` — JSONL logging of all enrichment actions
- `crossref_regenerator.py` — Rebuilds cross-reference indexes

The Canvas pipeline follows the same pattern, replacing "GitHub profile" with "workspace feedback."

### Pipeline Design

#### Stage 1: Collector (`canvas_collector.py`)

Polls each workspace's `/palette-feedback` endpoint.

```python
def collect_feedback(workspaces: list[str], canvas_url: str) -> list[FeedbackEntry]:
    """Fetch pending feedback from all workspaces."""
    entries = []
    for ws_id in workspaces:
        resp = requests.post(f"{canvas_url}/v1/missioncanvas/palette-feedback",
                           json={"workspace_id": ws_id})
        if resp.ok:
            data = resp.json()
            entries.extend(data.get("entries", []))
    return entries
```

Alternatively, for local-only (no server needed): read `palette_feedback.yaml` files directly from disk.

#### Stage 2: Validator (`canvas_validator.py`)

Checks each entry against Palette standards:

**KL Candidates**:
- Required fields present (id, question, answer, domain, source_type)
- Answer length >= 20 characters (not trivially short)
- No duplicate question in existing workspace KL or Palette KL
- Domain matches workspace config
- Assign evidence_bar: `workspace_validated` (lowest tier — can be promoted later with sourcing)

**Decision Records**:
- Required fields present (id, decision, resolution, workspace_id)
- decision_type is `one_way_door`
- No duplicate decision_id already recorded

**Mastery Signals**:
- Required fields present (id, concept_id, workspace_id, verified_at)
- concept_id exists in workspace KL or project concepts
- times_taught > 0 (actually taught, not just seen)

#### Stage 3: Classifier (`canvas_classifier.py`)

Maps validated entries to Palette taxonomy:

**For KL candidates**:
- Infer `problem_type` from domain and question keywords
- Suggest `related_rius` based on workspace config domain mapping
- Assign `journey_stage` = "foundation" (default for workspace-generated knowledge)
- Assign `difficulty` based on original evidence priority (critical→high, moderate→medium, low→low)

**For mastery signals**:
- Identify which Palette KL entry the concept maps to (if any)
- Tag the entry with `user_validated: true` and `validation_workspace: {id}`
- Track `avg_times_to_mastery` across workspaces (useful for difficulty calibration)

#### Stage 4: Promoter (`canvas_promoter.py`)

Two promotion tracks:

**Auto-promote to workspace KL** (no human review):
- KL candidates with `evidence_bar: workspace_validated` get appended to the workspace's own knowledge library
- This means the oil-investor workspace gets smarter from its own resolved evidence
- Format: matches existing workspace KL format exactly

**Queue for Palette KL review** (human checkpoint):
- KL candidates that could be domain-agnostic (e.g., "what is a one-way door?") get queued
- Decision records with general patterns get queued
- Output: `palette/enrichment/canvas_candidates/pending_review.yaml`
- Format: matches `palette_knowledge_library_v1.4.yaml` entry format
- Human reviews and either promotes to v1.4 or rejects

#### Stage 5: Ingestor (`canvas_ingestor.py`)

Marks processed entries as consumed:

```python
def mark_ingested(workspace_id: str, entry_ids: list[str], canvas_url: str):
    requests.post(f"{canvas_url}/v1/missioncanvas/palette-feedback",
                 json={"workspace_id": workspace_id, "action": "mark_ingested", "entry_ids": entry_ids})
```

#### Stage 6: Auditor (uses existing `audit_log.py`)

Logs every action:
```json
{
  "action": "canvas_enrichment",
  "timestamp": "2026-03-31T...",
  "source": "canvas_feedback",
  "workspace_id": "oil-investor",
  "entries_collected": 3,
  "kl_candidates_promoted": 1,
  "decision_records_logged": 1,
  "mastery_signals_processed": 1,
  "errors": 0,
  "pipeline_run_id": "20260331T..."
}
```

### File Plan

```
palette/scripts/enrichment/
  enrich.py              ← existing (GitHub enrichment)
  canvas_enrichment.py   ← NEW: CLI entry point for Canvas pipeline
  canvas_collector.py    ← NEW: Stage 1
  canvas_validator.py    ← NEW: Stage 2
  canvas_classifier.py   ← NEW: Stage 3
  canvas_promoter.py     ← NEW: Stage 4
  canvas_ingestor.py     ← NEW: Stage 5
  config.py              ← MODIFY: add Canvas paths + thresholds
  audit_log.py           ← existing (reuse)

palette/enrichment/canvas_candidates/
  pending_review.yaml    ← NEW: human review queue
```

### Scheduling

**Phase 1** (build it): Run manually via CLI: `python canvas_enrichment.py --workspaces oil-investor,rossi`
**Phase 2** (automate it): Cron job or hook that runs after evidence resolution / OWD approval
**Phase 3** (make it smart): Threshold-based — only run when pending entries exceed N, or on a daily schedule

### Success Criteria

1. Resolve an evidence gap in oil-investor → KL candidate appears in palette_feedback.yaml → pipeline promotes it to oil workspace KL → next coaching response can reference it
2. Mastery signals from multiple workspaces aggregate → Palette knows which concepts users struggle with
3. Decision records accumulate → Palette can report on decision patterns across workspaces
4. Zero manual steps after initial setup (except human review for Palette KL promotion)

---

## Part 4: Task Assignments — Round 2

### Priority 1: Learner System Unification (blocks everything else)

| Task | Agent | Description | Estimate |
|------|-------|-------------|----------|
| #33 | **Claude** | Modify `annotateWithCoaching()` to use learner_lens.yaml instead of learner_state. Remove learner_state from project_state writes. | 25 min |
| #34 | **Claude** | Fix routing priority in processRoute(): project-state queries first, coaching intercept second. | 15 min |
| #35 | **Claude** | Wire Kiro's coaching_signals into palette_feedback.yaml as concept_exposure entries. | 10 min |
| #36 | **Kiro** | Review #33-35 changes. Verify convergence_chain coaching still annotates correctly with unified learner store. Run stress_test_convergence.mjs. | 15 min |

### Priority 2: Palette Enrichment Pipeline

| Task | Agent | Description | Estimate |
|------|-------|-------------|----------|
| #37 | **Codex** | Build `canvas_collector.py` + `canvas_validator.py` (Stages 1-2). Read palette_feedback.yaml from disk, validate entries against KL schema. | 45 min |
| #38 | **Codex** | Build `canvas_classifier.py` + `canvas_promoter.py` (Stages 3-4). Auto-promote to workspace KL, queue domain-agnostic entries for review. | 45 min |
| #39 | **Codex** | Build `canvas_ingestor.py` + `canvas_enrichment.py` CLI (Stages 5-6). Mark entries ingested, audit logging. | 30 min |
| #40 | **Gemini** | Add tests for the enrichment pipeline. Validate that a KL candidate round-trips: evidence resolution → palette_feedback.yaml → pipeline → workspace KL. | 30 min |

### Priority 3: FDE Toolkit Workspace (the missing proof point)

| Task | Agent | Description | Estimate |
|------|-------|-------------|----------|
| #41 | **Gemini** | Create `workspaces/fde-toolkit/config.yaml` — domain: ai-sales-engineering, startup_artifact: meeting_brief, primary_frontend: voice. | 20 min |
| #42 | **Gemini** | Create `workspaces/fde-toolkit/project_state.yaml` — customer pipeline state with evidence gaps, open decisions, blocked actions for an FDE preparing for a customer call. | 30 min |
| #43 | **Kiro** | Create `workspaces/fde-toolkit/fde_knowledge_library_v1.yaml` — 15-20 entries covering objection handling, demo scripts, competitive positioning, guardrails pitch, pricing. Draw from Palette's existing service routing + integration recipes. | 45 min |

### Priority 4: Voxtral Integration (when Mistral is ready)

| Task | Agent | Description | Estimate |
|------|-------|-------------|----------|
| #44 | **Mistral** | Wire Voxtral STT output into Canvas `/route` endpoint. Voice in → text objective → convergence chain response. Define the integration contract. | When ready |
| #45 | **Mistral** | Judge North Star Competition using her framework. Agents self-evaluate, then vote. | When ready |

### Priority 5: Cleanup

| Task | Agent | Description | Estimate |
|------|-------|-------------|----------|
| #46 | **Kiro** | Remove dead exports from convergence_chain.mjs (verifyConceptMastery, getCoachingDepth if no longer used after #33). Update imports in server.mjs. | 10 min |
| #47 | **Claude** | Update all test suites after unification. Confirm 254+ tests still pass. Add 5-10 tests covering unified learner path. | 20 min |

---

## Dependency Graph

```
#33 (unify learner) ──┐
#34 (fix routing)  ────┤── #36 (Kiro review) ── #47 (update tests)
#35 (wire signals) ────┘
                                │
                                ▼
                    #37 (collector) ── #38 (classifier) ── #39 (CLI) ── #40 (pipeline tests)
                                                                              │
                                                                              ▼
                                                            #41 (fde config) ── #42 (fde state) ── #43 (fde KL)
```

Tasks #33-35 must complete before #36-47. Tasks #37-39 can start in parallel with #36. Tasks #41-43 can start immediately (no dependency on unification).

---

## For Mistral

When you're finished with Voxtral:

1. Read `NORTH_STAR_COMPETITION_INTEGRATION_REPORT.md` — full picture of what everyone built
2. Design your judging framework (#45) — the team will self-evaluate and vote
3. Review the enrichment pipeline plan above — your perspective on the Palette-side ingestion would be valuable
4. When ready, wire Voxtral into Canvas (#44) — the voice bridge is waiting

No rush. The team has enough work for the next round.
