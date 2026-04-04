# Legacy Compatibility Pointer — assumptions.md

This file exists for backward compatibility with tooling that still expects
`palette/.kiro/steering/assumptions.md`.

The canonical Tier 2 assumptions document is:

- `palette/core/assumptions.md`

Use the canonical file for all edits and reviews. Do not fork policy content
here.

## Compatibility Notes

- Canonical source: `palette/core/assumptions.md`
- Validator dependency: this file must preserve the legacy Orchestrator guard
  string expected by `scripts/validate_palette_state.py`

## Orchestrator Guard

DESIGN-ONLY PLACEHOLDER

The Orchestrator remains design-only until there is explicit promotion
evidence in `decisions.md` and matching fixture evidence in the agent layer.

## Orchestrator Agent Status
**Status**: DESIGN-ONLY PLACEHOLDER — do not treat as an implemented agent until it exists as a Kiro agent.
The Orchestrator follows the same lifecycle as other agents but tracks workflow-level success, not task-level execution.
