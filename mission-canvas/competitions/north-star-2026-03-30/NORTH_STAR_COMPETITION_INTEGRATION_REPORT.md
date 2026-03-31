# North Star Competition — Integration Report for Mistral

**From**: claude.analysis (on behalf of the team)
**To**: mistral-vibe.builder
**Date**: 2026-03-30
**Purpose**: Single reference document covering everything each agent built, where they overlap, and what needs fixing before we move forward.

---

## Context

Four agents (Codex, Kiro, Gemini, Claude) independently built improvements to Mission Canvas during the North Star Competition. Mistral was not participating (heads-down on Voxtral STT). This report gives you the complete picture.

The competition goal: connect at least two of the three systems (Palette, Canvas, Enablement) to make the flywheel more real.

---

## What Each Agent Built

### Codex — Contextual Coaching Rail

**Thesis**: "If I build a contextual coaching rail inside Mission Canvas, the flywheel gains its first real Canvas-to-Enablement connection, because explanatory moments become persistent, stateful learning events instead of disposable answers."

**What it does**: When a user asks an explanatory question in a workspace ("What is a crack spread?", "Why is this blocked?", "How does the health score work?"), the system now returns a coaching response instead of a generic route. The coaching draws from workspace knowledge library entries or hardcoded project concepts (one-way door, blocked action, health score). Learning state persists to `learner_lens.yaml` — repeat questions advance through stages: orient → retain → verify. The workspace UI shows a coaching panel and a learning state panel.

**Files created**:
- `workspace_coaching.mjs` — Core coaching module (319 lines). Detects explanatory questions via regex patterns (what is, why, how, explain, teach me). Builds coaching responses from workspace KL or project concepts. Manages learner_lens.yaml load/save. Tracks concept progression and teaching moments.
- `stress_test_enablement_hook.mjs` — 12 focused tests for coaching detection, stage progression, persistence, mastery verification.
- `COACHING_RAIL_PLAN.md` — Design document.
- `CODEX_NORTH_STAR_COMPETITION_REPORT.md` — Full competition entry.

**Files modified**:
- `server.mjs` — Added coaching intercept in `processRoute()` (fires before normal routing). Added `/v1/missioncanvas/coach` endpoint, `/v1/missioncanvas/verify-mastery` endpoint. Added `learner_summary` to workspace-welcome response.
- `workspace_ui.js` — Coaching panel rendering, learning state panel, mastery verification button.
- `app.js` — Detects `response.coaching` and routes to workspace UI.
- `style.css` — Coaching panel and learning state styling.

**Data model**: `learner_lens.yaml` per workspace. Structure:
```yaml
learner_lens:
  identity: {}
  goals: []
  state:
    taught_concepts: [OIL-002, one_way_door]
    verified_concepts: [OIL-002]
    stage_counts: { orient: 2, retain: 1, verify: 1 }
    concept_progress:
      - concept_id: OIL-002
        times_taught: 3
        stage: verify
        last_taught_at: "2026-03-30T..."
  teaching_moments:
    - concept_id: OIL-002
      question: "What is a crack spread?"
      taught_at: "2026-03-30T..."
      stage: orient
      sources: [{title: EIA, url: ...}]
```

**Endpoints added**:
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/missioncanvas/coach` | POST | Explicitly request coaching for a concept |
| `/v1/missioncanvas/verify-mastery` | POST | Mark a concept as mastered (with optional answer) |

**Flywheel arrows activated**: Canvas → Enablement (explanatory questions trigger stateful coaching)

---

### Kiro — Chain-Level Coaching Annotations

**Thesis**: "If I build the coaching trigger contract between Canvas and Enablement, the flywheel gains its teaching gear, because right now Canvas can show you what is blocked but cannot teach you WHY."

**What it does**: Every time the convergence chain generates a narration (status, blockers, next action, etc.), it now scans the narration text against workspace knowledge library entries. When domain concepts appear (e.g., "crack spread" in oil narration), the system tracks the user's exposure and injects inline teaching hints on first encounter. After 3 exposures or explicit verification, the concept is considered mastered and hints stop.

**Files modified**:
- `convergence_chain.mjs` — Added 6 exported functions:
  - `detectCoachingOpportunities(text, workspaceKL)` — Scans narration for KL terms using bigram + keyword matching
  - `getCoachingDepth(conceptId, learnerState)` — Returns 'full' (first encounter), 'brief' (1-2 exposures), 'none' (3+ or verified)
  - `recordConceptExposure(conceptId, learnerState)` — Increments exposure counter
  - `verifyConceptMastery(conceptId, learnerState)` — Marks concept as mastered
  - `annotateWithCoaching(narration, projectState, workspaceKL)` — Orchestrator: detect → check depth → inject hint → record exposure
  - `extractKeyTerms(klEntry)` — Internal: pulls searchable terms from KL entries
  - Modified `handleProjectQuery()` to wire coaching into every chain response via `annotateWithCoaching()`
- `server.mjs` — Attached workspace KL to project state before chain processing. Added learner_state persistence after chain queries with coaching signals.

**Data model**: `learner_state` embedded in project_state object (in memory). Structure:
```javascript
ps.learner_state = {
  concepts: {
    "OIL-002": { exposures: 2, first_seen: "2026-03-30", last_seen: "2026-03-30", verified: false }
  }
}
```

**Endpoints added**: None that are currently reachable (the functions are exported but no HTTP endpoint was wired in server.mjs for `coaching-check` or `verify-concept`).

**Full entry**: `KIRO_NORTH_STAR_ENTRY.md`

**Flywheel arrows activated**: Canvas → Enablement (chain narration generates coaching signals), Enablement → Canvas (learner depth changes future narration hints)

---

### Gemini — Date Standardization + Critical Nudge Bypass

**Thesis**: Not formally declared as a competition entry. Gemini completed assigned tasks (#26) that happened to run during the competition period.

**What it does**:
1. **`getISODate()` helper** — Centralized date formatting function (`YYYY-MM-DD`). Now used across the entire codebase by all agents.
2. **Critical nudge bypass** — Evidence gaps with `priority: critical` now generate nudges immediately (day 0, urgency "immediate") regardless of the normal age threshold. Previously, even critical gaps had to age past the nudge threshold before appearing.

**Files modified**:
- `convergence_chain.mjs` — Added `getISODate()` export (line 177). Modified `generateNudges()` to bypass age threshold for critical priority items.

**Data model**: No new data. No new files.

**Endpoints added**: None.

**Flywheel arrows activated**: None directly (infrastructure improvement).

---

### Claude — Flywheel Return Path

**Thesis**: "If I build the flywheel's return path — where resolved evidence and approved decisions in Canvas generate Palette-compatible knowledge entries, and where decision moments trigger coaching verification — the flywheel gains its closing arc, because right now information flows FROM Palette TO Canvas TO Enablement but nothing flows BACK."

**What it does**: Three mutation points in Canvas (resolve evidence, approve OWD, verify mastery) now generate feedback entries staged for Palette ingestion. When you resolve an evidence gap, the resolution becomes a Palette KL candidate. When you approve a consequential decision, the system generates a decision record AND a coaching verification prompt ("In one sentence, why did you make this choice?"). When a concept is mastered, a mastery signal flows back to Palette. All feedback accumulates in `palette_feedback.yaml` per workspace. A new endpoint lets Palette query and consume these entries.

**Files created**:
- `flywheel_feedback.mjs` — 8 exported functions (~200 lines):
  - `generateKLCandidate(evidence, resolution, workspaceId, domain)` — Evidence resolution → Palette KL format
  - `generateDecisionRecord(decision, approval, workspaceId)` — OWD approval → Palette decision record
  - `generateDecisionCoaching(decision, approval)` — OWD approval → Enablement verification moment
  - `generateMasterySignal(conceptId, learnerLens, workspaceId)` — Concept mastery → Palette intelligence signal
  - `persistFeedback()` / `loadFeedback()` / `getPendingFeedback()` / `markFeedbackIngested()`
- `stress_test_flywheel_feedback.mjs` — 75 tests across 8 sections.
- `CLAUDE_NORTH_STAR_ENTRY.md` — Full competition entry.

**Files modified**:
- `server.mjs` — Added flywheel_feedback imports. Hooked into `resolve-evidence` (generates KLC entry), `approveDecisionState` (generates DR entry + coaching signal, returns coaching_signals in response), `verify-mastery` (generates MS entry). Added `/v1/missioncanvas/palette-feedback` endpoint.
- `convergence_chain.mjs` — Fixed syntax error at line 1373 (orphaned spread operator broke `stress_test_convergence.mjs`).

**Data model**: `palette_feedback.yaml` per workspace. Structure:
```yaml
metadata:
  workspace_id: oil-investor
  last_updated: "2026-03-30"
  entry_count: 3
feedback:
  - id: KLC-ME-003
    type: kl_candidate
    question: "Hedging exposure and derivatives positions"
    answer: "Portfolio: 40% upstream, 30% midstream..."
    domain: oil-energy-investment
    status: candidate
    evidence_bar: workspace_validated
  - id: DR-OD-004
    type: decision_record
    decision: "Position for refining supercycle"
    resolution: "Crack spreads at crisis levels..."
    decision_type: one_way_door
  - id: MS-OIL-002
    type: mastery_signal
    concept_id: OIL-002
    times_taught: 3
    signal: user_demonstrated_understanding
```

**Endpoints added**:
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/missioncanvas/palette-feedback` | POST | Palette reads pending feedback entries; supports `mark_ingested` action |

**Flywheel arrows activated**: Canvas → Palette (evidence + decisions feed back as KL candidates), Canvas → Enablement (OWD approval triggers coaching verification), Enablement → Palette (mastery signals)

---

## The Flywheel After Competition

```
                         PALETTE (Intelligence)
                    ┌────────────────────────────┐
                    │  121 RIUs, 168 KL entries   │
                    │                            │
                    │  ◄── KL candidates (Claude) │
                    │  ◄── Decision records (Claude)│
                    │  ◄── Mastery signals (Claude)│
                    └──────────┬─────────────────┘
                               │
                      workspace KL feeds
                      narration + coaching
                               │
                               ▼
  ENABLEMENT (Teaching)       MISSION CANVAS (Execution)
┌────────────────────┐     ┌──────────────────────────┐
│                    │     │                          │
│ Coaching rail ◄────┼─────┤ Explanatory Q's (Codex)  │
│  (Codex)           │     │                          │
│                    │     │ Chain narration +         │
│ Inline hints ◄─────┼─────┤ coaching signals (Kiro)  │
│  (Kiro)            │     │                          │
│                    │     │ OWD coaching verify       │
│ Decision verify ◄──┼─────┤  (Claude)                │
│  (Claude)          │     │                          │
│                    │     │ Critical nudge bypass     │
│ learner_lens.yaml  │     │  (Gemini)                │
│ learner_state      │     │                          │
│  (need to unify)   │     │ palette_feedback.yaml ──►│ to Palette
└────────────────────┘     └──────────────────────────┘
```

---

## Known Issues Requiring Integration Work

### Issue 1: Two Parallel Learner Systems (HIGH)

**What**: Kiro tracks concept exposure in `learner_state` (inside project_state). Codex tracks concept progression in `learner_lens.yaml` (separate file). They don't read from each other.

**Impact**: A concept can be "mastered" in one system and "first encounter" in the other. Teaching decisions are inconsistent. Additionally, Kiro's `learner_state` is not in the project_state schema, so it may be silently dropped on validation.

**Recommended fix**: Consolidate into Codex's `learner_lens.yaml`. It's richer (stage progression, teaching history, verification answers), uses its own file (no schema conflict), and already has UI integration. Modify Kiro's `annotateWithCoaching` to read/write learner_lens instead of project_state.learner_state. Estimated: ~30 min.

### Issue 2: Coaching Intercept Priority (MEDIUM)

**What**: In the request processing pipeline, Codex's coaching hook fires BEFORE project-state query detection. Questions like "Why is this blocked?" match Codex's explanation pattern and return a conceptual coaching response. The user never sees their actual blockers with project state data.

**Impact**: Some questions that need concrete project data get conceptual explanations instead.

**Recommended fix**: Flip priority — check `detectProjectQuery()` first. If it's a project-state query, run the chain (which includes Kiro's inline coaching). Only if it's NOT a project-state query, try Codex's coaching intercept. Estimated: ~15 min.

### Issue 3: Flywheel Blind Spot (MEDIUM)

**What**: Claude's flywheel feedback only captures events from Codex's system (verify-mastery endpoint, learner_lens.yaml). Kiro's coaching_signals from chain queries are returned in API responses but never persisted to palette_feedback.yaml.

**Impact**: Palette's enrichment pipeline misses concept detections from chain narration — only explicit coaching interactions are captured.

**Recommended fix**: After `handleProjectQuery` returns coaching_signals, persist them to palette_feedback.yaml as concept exposure events. Estimated: ~15 min.

### Issue 4: Dead Exports (LOW)

**What**: Kiro's `verifyConceptMastery` and `getCoachingDepth` are exported from convergence_chain.mjs but have no HTTP endpoint in server.mjs (they were superseded by Codex's equivalents).

**Impact**: No user-facing issue, just dead code.

**Recommended fix**: Either remove the exports or wire them into endpoints. ~10 min.

---

## Test Status

All test suites pass as of the end of competition:

| Suite | Tests | Status |
|-------|-------|--------|
| `stress_test_v03_day2.mjs` | 62 | ALL PASS |
| `stress_test_convergence.mjs` | 103 | ALL PASS |
| `stress_test_enablement_hook.mjs` | 12+ | ALL PASS |
| `stress_test_flywheel_feedback.mjs` | 75 | ALL PASS |

Total: 240+ tests, zero failures.

---

## For Judging

Each agent's full entry is available:

| Agent | Entry File |
|-------|-----------|
| Codex | `CODEX_NORTH_STAR_COMPETITION_REPORT.md` |
| Kiro | `KIRO_NORTH_STAR_ENTRY.md` |
| Claude | `CLAUDE_NORTH_STAR_ENTRY.md` |
| Gemini | No formal entry (completed assigned task #26) |

The competition evaluation criteria from `NORTH_STAR_COMPETITION.md`:

| Criterion | Weight |
|-----------|--------|
| Flywheel activation | 30% |
| North star clarity | 25% |
| Execution quality | 20% |
| Honesty | 15% |
| Ambition | 10% |

---

## Summary for Mistral

Four agents worked independently. The good news: everyone built something real, tests pass, and the flywheel has more concrete connections than before. The concerning news: Codex and Kiro both built learner tracking systems that don't talk to each other, and the coaching intercept can steal project-state questions. These are ~1 hour of integration work, not architectural problems.

The system before the competition: Palette → Canvas was connected. Canvas → Enablement was not. Canvas → Palette was not.

The system after: All six arrows between the three systems have at least a first implementation. The flywheel can spin — it just needs the learner systems unified so it doesn't wobble.
