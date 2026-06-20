# Codex North Star Competition Report

**Author:** `codex.implementation`  
**Date:** `2026-03-30`  
**Scope:** North Star Competition work completed through the current round

## Original Objective

The competition objective was not to ship an isolated feature. It was to make the three-system flywheel more real:

- **Palette** knows what to do
- **Mission Canvas** does the work
- **Enablement** teaches you how

The prompt to Codex was:

> You see the system as a product. Where does the product break when a real user touches it?

My answer was:

The product breaks the first time a user asks an explanatory question during real work and the system does not respond like a teaching system with memory. It can answer, but it does not yet teach in a persistent way.

## Thesis

> If I build a contextual coaching rail inside Mission Canvas, the flywheel gains its first real Canvas-to-Enablement connection, because explanatory moments become persistent, stateful learning events instead of disposable answers.

## What I Built

I built the first native **contextual coaching rail** inside Mission Canvas.

This means that in workspace mode, explanatory questions now take a dedicated coaching path instead of falling back to generic route behavior.

Examples:
- `What is a crack spread?`
- `Why is this blocked?`
- `What is a one-way door?`
- `How does the health score work?`

The coaching path now:

1. Detects explanatory questions in workspace mode
2. Builds a coaching response from workspace knowledge or project-state concepts
3. Persists the teaching moment to `learner_lens.yaml`
4. Advances concept progression over time
5. Exposes learning state back into the workspace UI
6. Supports explicit mastery verification

## End Result

Mission Canvas now has a real product seam between execution and enablement.

Before:
- explanatory questions were effectively disposable
- the system did not remember that it had taught something
- the workspace had no visible learning state
- the flywheel was still mostly architecture language

After:
- explanatory questions can return `source: enablement_hook`
- learning state persists per workspace in `learner_lens.yaml`
- repeat teaching can change stage over time
- verified concepts are tracked
- the workspace welcome can show learning state as a first-class part of the product

This is the first concrete slice where **doing** and **teaching** are connected inside Mission Canvas.

## Files

### New files

- [COACHING_RAIL_PLAN.md](/home/mical/fde/missioncanvas-site/COACHING_RAIL_PLAN.md)
- [workspace_coaching.mjs](/home/mical/fde/missioncanvas-site/workspace_coaching.mjs)
- [stress_test_enablement_hook.mjs](/home/mical/fde/missioncanvas-site/stress_test_enablement_hook.mjs)
- [CODEX_NORTH_STAR_COMPETITION_REPORT.md](/home/mical/fde/missioncanvas-site/CODEX_NORTH_STAR_COMPETITION_REPORT.md)

### Modified files

- [server.mjs](/home/mical/fde/missioncanvas-site/server.mjs)
- [workspace_ui.js](/home/mical/fde/missioncanvas-site/workspace_ui.js)
- [app.js](/home/mical/fde/missioncanvas-site/app.js)
- [style.css](/home/mical/fde/missioncanvas-site/style.css)

### Live workspace state touched during integration

- [learner_lens.yaml](/home/mical/fde/missioncanvas-site/workspaces/oil-investor/learner_lens.yaml)

## What Each File Does

### [COACHING_RAIL_PLAN.md](/home/mical/fde/missioncanvas-site/COACHING_RAIL_PLAN.md)

Design and judging plan for the competition entry:
- thesis
- current state
- proposed changes
- flywheel impact
- success signal
- risks

### [workspace_coaching.mjs](/home/mical/fde/missioncanvas-site/workspace_coaching.mjs)

Core implementation for the new seam:
- explanatory question detection
- concept extraction
- workspace-KL coaching generation
- project-state concept coaching generation
- learner lens load/save
- concept progression
- mastery verification

### [server.mjs](/home/mical/fde/missioncanvas-site/server.mjs)

Integration point:
- routes workspace explanatory questions into the coaching rail
- returns `learner_summary` in `workspace-welcome`
- supports `/v1/missioncanvas/coach`
- supports `/v1/missioncanvas/verify-mastery`
- keeps review focused on the new learner-lens path

### [workspace_ui.js](/home/mical/fde/missioncanvas-site/workspace_ui.js)

Product surface:
- renders the coaching panel
- renders the learning-state panel
- allows mastery verification from the coaching view
- avoids exposing ambiguous or half-finished review paths

### [app.js](/home/mical/fde/missioncanvas-site/app.js)

Wiring:
- detects `response.coaching`
- routes coaching responses into the workspace UI
- keeps workspace output formatting consistent

### [style.css](/home/mical/fde/missioncanvas-site/style.css)

Presentation:
- coaching panel styling
- learning-state panel styling
- reviewable visual distinction between execution and enablement surfaces

### [stress_test_enablement_hook.mjs](/home/mical/fde/missioncanvas-site/stress_test_enablement_hook.mjs)

Focused test coverage for the competition slice:
- coaching detection
- stage progression
- project-state coaching
- learner-lens persistence
- mastery verification behavior

## Build Sequence

### Phase 1: Thesis and Plan

I read:
- `NORTH_STAR_ARCHITECTURE.md`
- `NORTH_STAR_COMPETITION.md`
- `UNIFIED_PRODUCT_THESIS.md`
- the enablement skill
- route and workspace UI hook points

I concluded that the product breaks on explanatory questions, not on routing depth.

I then wrote:
- [COACHING_RAIL_PLAN.md](/home/mical/fde/missioncanvas-site/COACHING_RAIL_PLAN.md)

### Phase 2: First Implementation Slice

I added:
- deterministic coaching detection
- coaching responses from workspace KL or project concepts
- `learner_lens.yaml` persistence
- a dedicated coaching panel

This created the first real Canvas-to-Enablement seam.

### Phase 3: Richer Learning State

I expanded the learner model to track:
- `taught_concepts`
- `verified_concepts`
- `stage_counts`
- `concept_progress`
- last taught concept and timestamp

I exposed that via `workspace-welcome` and rendered it as a `Learning State` panel.

### Phase 4: Live Integration Pass

I ran the implementation against the live `oil-investor` workspace and found a real bug:

- repeat explanatory questions were not advancing properly in the live workspace because concept matching was too literal

I fixed that by normalizing concept extraction and matching.

### Phase 5: Review-Surface Cleanup

I did a final quality pass and removed ambiguity from the judged surface:

- reduced overlap between the older `learner_state` path and the new `learner_lens.yaml` path
- tightened `verifyMastery()` so it only verifies concepts that were actually taught
- removed speculative UI affordances that made the surface noisier than the core seam

## Verification

### Static checks

Passed:
- `node --check /home/mical/fde/missioncanvas-site/workspace_coaching.mjs`
- `node --check /home/mical/fde/missioncanvas-site/server.mjs`
- `node --check /home/mical/fde/missioncanvas-site/workspace_ui.js`
- `node --check /home/mical/fde/missioncanvas-site/app.js`

### Focused test

Passed:
- `node /home/mical/fde/missioncanvas-site/stress_test_enablement_hook.mjs`

Coverage includes:
- explanatory question detection
- non-explanatory bypass
- orient -> retain -> verify progression
- project-state concept coaching
- learner-lens persistence
- mastery verification success/failure behavior

### Live integration

Confirmed locally on the running server:
- `GET /v1/missioncanvas/health`
- `POST /v1/missioncanvas/route` returns `source: enablement_hook` for coaching questions
- `POST /v1/missioncanvas/workspace-welcome` returns `learner_summary`
- `POST /v1/missioncanvas/verify-mastery` responds correctly

## What Reviewers Should Judge

I recommend judging this entry on four criteria:

1. **Does the product feel more real?**  
   When a user asks an explanatory question, does the system feel like an implementation partner instead of a generic answer engine?

2. **Does learning change the next interaction?**  
   The important shift is not that the system answered once. It is that the workspace now remembers the teaching event and reflects it later.

3. **Is the state model coherent?**  
   Is the learner state visible, understandable, and plausible as a real product layer?

4. **Does this clarify the North Star?**  
   Did this work make the flywheel more concrete, or only add one more feature?

## My Read on the Result

This work does not complete the north star. It does clarify it.

The key product lesson from this round is:

> The flywheel becomes believable when execution changes the next interaction.

Not when the system answers more questions.  
Not when the UI has more cards.  
Not when routing gets smarter in the abstract.

The first believable connection between Canvas and Enablement is remembered teaching in the middle of work.

## Suggested Evaluation Metric

If the team wants one concise metric for this entry:

> **Does Mission Canvas now teach in context with memory, rather than merely explain on demand?**

If the answer is yes, this round succeeded.
