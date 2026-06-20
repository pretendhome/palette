# Palette Lenses (Optional Context Overlays)

Lenses are optional context overlays that shape output framing for a session.

They do not replace agent roles and do not override:
- RIU routing
- ONE-WAY DOOR gates
- Agent constraints

## Why this exists

Palette already has strong agent specialization. Lenses help when the failure mode is not "wrong agent", but "right agent, wrong decision frame for this stakeholder context."

## How to use

1. Pick no lens by default.
2. Activate a lens only when the work needs role-specific decision framing.
3. Validate lens impact with eval metrics before keeping it.

## Success criteria for any lens

- Better convergence quality (fewer clarification loops)
- Better artifact acceptance (less rework)
- Better decision hygiene (owner, metric, reversibility)

## Kill criteria

- No measurable gain after comparable runs
- Adds process overhead without quality gain
- Increases confident-but-unsupported outputs

## Current v0 lenses

- `releases/v0/LENS-PM-001_product_decision.yaml`
- `releases/v0/LENS-ENG-001_engineering_execution.yaml`
- `releases/v0/LENS-DEV-001_developer_delivery.yaml`
