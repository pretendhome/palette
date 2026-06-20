# Contextual Coaching Rail — North Star Plan

## Thesis

If I build a contextual coaching rail inside Mission Canvas, the flywheel gains its first real Canvas-to-Enablement connection, because explanatory moments become persistent, stateful learning events instead of disposable answers.

## Current State

- Canvas can detect project-state questions and answer them with convergence-chain views.
- Canvas can inject workspace knowledge-library entries into normal route responses.
- Enablement exists as a methodology, but there is no trigger mechanism in Canvas.
- Workspace state persists, but learning state does not.
- A user asking "what is X?" inside a workspace gets a generic route-shaped response, not a coaching surface.

## Proposed Changes

1. Add a deterministic coaching detector for explanatory questions inside workspace mode.
2. Build a coaching response shape that includes:
   - concept
   - explanation
   - why it matters in this workspace
   - verification prompt
   - next-step queries
3. Persist each teaching moment to `workspaces/<id>/learner_lens.yaml`.
4. Make repeated coaching questions adapt based on prior teaching moments.
5. Render coaching as a first-class panel in `workspace_ui.js`, not as generic route text.

## Files

- `missioncanvas-site/workspace_coaching.mjs`
- `missioncanvas-site/server.mjs`
- `missioncanvas-site/workspace_ui.js`
- `missioncanvas-site/app.js`
- `missioncanvas-site/style.css`
- `missioncanvas-site/stress_test_enablement_hook.mjs`

## Flywheel Impact

- Palette -> Canvas:
  Workspace knowledge-library entries become the source material for coaching answers.
- Canvas -> Enablement:
  Explanatory questions become explicit teaching moments with state and UI.
- Enablement -> Canvas:
  Prior teaching changes the next response shape for the same concept.

## Success Signal

- In a workspace, "What is a crack spread?" returns a coaching card instead of a generic route.
- The same concept asked again reflects prior teaching and shifts from orient to retain.
- A `learner_lens.yaml` file is created and updated automatically.
- The UI makes the difference visible to a real user.

## Risk

- Heuristic detection may catch some queries that should remain normal routing.
- Lightweight learner-lens persistence could become too bespoke if the final enablement model evolves sharply.

## Rollback

- Remove the coaching branch from `processRoute()`.
- Keep `workspace_coaching.mjs` isolated so the rollback is low-risk.
