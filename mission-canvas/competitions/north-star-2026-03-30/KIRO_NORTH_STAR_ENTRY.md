# North Star Competition — Kiro Entry

**Agent**: kiro.design
**Date**: 2026-03-30
**Competition**: North Star — discover what we are building by building toward it

---

## Thesis

> If I build the coaching trigger contract between Canvas and Enablement, the flywheel gains its teaching gear, because right now Canvas can show you what is blocked but cannot teach you WHY — and without the why, the user never stops needing the system.

---

## The Problem

The North Star describes a flywheel: Palette knows what to do, Canvas does it, Enablement teaches how. But before this entry, Canvas and Enablement were completely disconnected:

- Canvas generates a daily brief that says "crack spread $55.78, crisis-level" — every day, the same way, regardless of whether the user knows what a crack spread is
- Enablement has a full coaching methodology (7 stages, LearnerLens, verification patterns) sitting in a markdown file with no trigger mechanism inside Canvas
- The flywheel diagram says "doing teaches you more" but doing did NOT teach — it just repeated

The contract between Canvas and Enablement was undefined. Canvas did not know when to teach. Enablement did not know when the user was doing.

---

## What I Built

### Coaching Trigger System

A contract layer wired into the convergence chain that detects domain concepts during narration, tracks what the user has learned, and adapts explanation depth over time.

### Components

#### 1. Concept Detection (`detectCoachingOpportunities`)
- Scans narration text against workspace knowledge library entries
- Uses bigram + keyword matching (e.g., "crack spread", "wti-brent spread")
- Zero false positives on generic text ("your health score is 52")
- Correct matches on domain text (13 concepts detected on a single oil-investor query)

#### 2. Learner State (`learner_state` in project_state.yaml)
- Per-concept tracking: exposures, first_seen, last_seen, verified, verified_on
- Persists to disk after every chain query with coaching signals
- Survives server restarts (part of workspace state)

#### 3. Depth Progression (`getCoachingDepth`)
- `full` — first encounter (0 exposures): inject 💡 inline explanation
- `brief` — seen before (1-2 exposures): signal present but no inline hint
- `none` — mastered (3+ exposures or verified): no signal, no teaching

#### 4. Adaptive Narration (`annotateWithCoaching`)
- On first encounter: injects a 💡 coaching block with a one-sentence explanation pulled from the KL entry answer
- One hint per narration (avoids clutter)
- Signals capped at 5 per response
- Records exposure automatically

#### 5. Coaching Endpoints
- `POST /v1/missioncanvas/coaching-check` — returns depth + should_teach for a concept
- `POST /v1/missioncanvas/verify-concept` — marks concept as mastered, persists to disk

#### 6. Integration
- Wired into `handleProjectQuery()` — every convergence chain response includes `coaching_signals` when workspace KL exists
- Workspace KL attached to project state before chain processing
- Learner state written to disk after signals fire

---

## Files Changed

| File | What Changed |
|------|-------------|
| `missioncanvas-site/convergence_chain.mjs` | Added 6 exported functions: `detectCoachingOpportunities`, `getCoachingDepth`, `recordConceptExposure`, `verifyConceptMastery`, `annotateWithCoaching`, plus `extractKeyTerms` (internal). Modified `handleProjectQuery` to wire coaching into every chain response. |
| `missioncanvas-site/server.mjs` | Added 2 endpoints (`/coaching-check`, `/verify-concept`). Added learner_state persistence after chain queries. Imported new coaching functions. Attached workspace KL to project state before chain processing. |

---

## How to Verify

### Quick test (server must be running on port 8787):

```bash
# 1. First query — should see coaching signals + 💡 hint
curl -s -X POST http://localhost:8787/v1/missioncanvas/route \
  -H 'Content-Type: application/json' \
  -d '{"request_id":"test-1","timestamp":"2026-03-30T15:00:00Z","session_id":"eval","workspace_id":"oil-investor","user":{"id":"t","role":"owner"},"input":{"objective":"how are we doing","context":"","desired_outcome":"","constraints":"","risk_posture":"medium"},"policy":{"enforce_convergence":true,"enforce_one_way_gate":true,"max_selected_rius":5,"require_validation_checks":true},"runtime":{"mode":"planning","allow_execution":false,"tool_whitelist":["research","planning"],"log_target":"implementation"}}'

# Look for: convergence_chain.coaching_signals array, 💡 in action_brief_markdown

# 2. Check coaching depth for a concept
curl -s -X POST http://localhost:8787/v1/missioncanvas/coaching-check \
  -H 'Content-Type: application/json' \
  -d '{"workspace_id":"oil-investor","concept_id":"OIL-002"}'

# Should return: depth=brief (already exposed from step 1), should_teach=true

# 3. Mark concept as mastered
curl -s -X POST http://localhost:8787/v1/missioncanvas/verify-concept \
  -H 'Content-Type: application/json' \
  -d '{"workspace_id":"oil-investor","concept_id":"OIL-002"}'

# 4. Check again — should now say depth=none, should_teach=false
curl -s -X POST http://localhost:8787/v1/missioncanvas/coaching-check \
  -H 'Content-Type: application/json' \
  -d '{"workspace_id":"oil-investor","concept_id":"OIL-002"}'

# 5. Rossi (no workspace KL) — should have zero coaching signals
curl -s -X POST http://localhost:8787/v1/missioncanvas/route \
  -H 'Content-Type: application/json' \
  -d '{"request_id":"test-2","timestamp":"2026-03-30T15:00:00Z","session_id":"eval-rossi","workspace_id":"rossi","user":{"id":"t","role":"owner"},"input":{"objective":"how are we doing","context":"","desired_outcome":"","constraints":"","risk_posture":"medium"},"policy":{"enforce_convergence":true,"enforce_one_way_gate":true,"max_selected_rius":5,"require_validation_checks":true},"runtime":{"mode":"planning","allow_execution":false,"tool_whitelist":["research","planning"],"log_target":"implementation"}}'
```

### Edge case tests (no server needed):

```bash
cd missioncanvas-site && node -e "
import { detectCoachingOpportunities, getCoachingDepth, recordConceptExposure, verifyConceptMastery, annotateWithCoaching } from './convergence_chain.mjs';

// Null safety
console.log('null text:', detectCoachingOpportunities(null, []).length === 0);
console.log('null KL:', detectCoachingOpportunities('test', null).length === 0);
console.log('null learner:', getCoachingDepth('X', null) === 'full');

// Depth progression
const ls = { concepts: {} };
recordConceptExposure('C1', ls);
console.log('1 exposure = brief:', getCoachingDepth('C1', ls) === 'brief');
recordConceptExposure('C1', ls); recordConceptExposure('C1', ls);
console.log('3 exposures = none:', getCoachingDepth('C1', ls) === 'none');

// Verify overrides
const ls2 = { concepts: {} };
recordConceptExposure('C2', ls2);
verifyConceptMastery('C2', ls2);
console.log('verified = none:', getCoachingDepth('C2', ls2) === 'none');

// No false positives
const fakeKL = [{ id: 'OIL-002', question: 'What is a crack spread in oil refining?' }];
console.log('generic text = 0 matches:', detectCoachingOpportunities('Your health score is 52.', fakeKL).length === 0);
console.log('domain text = 1 match:', detectCoachingOpportunities('The crack spread is at crisis levels.', fakeKL).length === 1);
"
```

### Full test suites:

```bash
cd missioncanvas-site
# Start server, then:
node stress_test.mjs          # 37 pass, 0 fail
node stress_test_session.mjs  # 16 pass, 0 fail
node stress_test_convergence.mjs  # 103 pass, 0 fail
```

---

## The User Experience

### Before (no coaching)

Oil investor asks "how are we doing" every morning. Gets:

> **Health Score**: 52/100 (NEEDS ATTENTION)
> **Critical Gaps**: Portfolio positions not provided, risk parameters undefined
> **Open Decision**: Position for the refining supercycle

The brief mentions "crack spread" and "EBITDAX" without explanation. The investor either knows what these mean or doesn't. The system doesn't care. Tomorrow, same brief, same terms, same lack of understanding.

### After (with coaching)

First time the investor asks "how are we doing":

> **Health Score**: 52/100 (NEEDS ATTENTION)
>
> 💡 **crack spread**: The 3-2-1 crack spread is the industry standard benchmark for refining margins.
>
> **Critical Gaps**: Portfolio positions not provided...

The coaching signal fires: `OIL-002, depth: full, should_teach: true`.

Second time: no 💡 hint. The system knows the investor has seen it.

After the investor demonstrates understanding (via verify-concept): `depth: none, should_teach: false`. The system stops teaching crack spread entirely.

The narration adapts. The user learns. The system gets quieter as the user gets smarter.

---

## Flywheel Impact

```
Palette (Intelligence)
  │
  │ 28 oil KL entries provide the teaching content
  │
  ▼
Canvas (Execution) ──────────► Enablement (Teaching)
  │                              │
  │ convergence chain narration   │ coaching signals fire
  │ detects domain concepts       │ learner state tracks understanding
  │                              │ narration depth adapts
  │                              │
  └──────────────────────────────┘
         learner_state feeds back
         into narration depth
```

- **Palette → Canvas**: already connected (taxonomy routing, KL injection)
- **Canvas → Enablement**: THIS IS WHAT I BUILT — coaching signals emitted during narration
- **Enablement → Canvas**: learner_state feeds back into narration depth
- **Enablement → Palette**: competence data reveals which KL entries get used most (future)

The flywheel: doing creates coaching signals → coaching creates understanding → understanding reduces signal depth → the user needs less help → the system gets smarter about what to teach.

---

## What I Learned About the North Star

The flywheel is real but it needs fuel. The fuel is domain knowledge.

- Oil-investor has 28 KL entries → 13 coaching signals on a single query
- Rossi has 0 workspace KL entries → 0 coaching signals

The quality of the coaching layer is directly proportional to the richness of the knowledge library. This means Palette (intelligence) feeds Enablement (teaching) through Canvas (execution). That IS the flywheel.

The implication: every new KL entry doesn't just improve routing — it also improves teaching. That's the compounding effect the North Star describes.

---

## Also Shipped Today (Non-Competition)

For context, the coaching trigger system was built on top of a full day of infrastructure work:

| # | Task | Description |
|---|------|-------------|
| 5 | Voice bridge hardening | workspace_id, session_id, Whisper pre-check, voice FRX |
| 6 | start.sh launcher | Web + voice modes, dependency detection |
| 12 | Streaming refactor | Extracted processRoute, unified /route and /talk-stream |
| 13 | Evidence resolution API | resolve-evidence + add-fact endpoints, RISK-4 cache fix |
| 14 | Session persistence | Picked up from Gemini — sessions survive restart |
| 18 | Config schema validation | config_schema.json with workspace load validation |
| 19 | Integration pass | 10-point test matrix, zero bugs |
| 24 | OWD bridge | Connected OWD approvals to project state decisions |
| 30 | Test fixes | Updated convergence tests for state drift |

Total: 10 tasks shipped, 156 tests passing, zero regressions.
