# Palette Workflow Definitions

Workflow files define the phase structure, agent assignments, quality gates, and decision checkpoints for multi-agent engagements. They make implicit workflows explicit and auditable.

## Format

Workflow files are YAML with the following structure:

- **id**: Unique workflow identifier
- **name**: Human-readable name
- **description**: What this workflow produces
- **phases**: Ordered list of phases, each containing:
  - **id**: Phase identifier (e.g., `phase-1-research`)
  - **name**: Phase name
  - **agent**: Primary Palette agent
  - **supporting_agents**: Optional list of supporting agents
  - **inputs**: What this phase requires (files, decisions, context)
  - **outputs**: What this phase produces (files with descriptions)
  - **quality_gate**: Validation criteria checked before proceeding
  - **decisions**: ONE-WAY DOOR or TWO-WAY DOOR decisions expected in this phase
  - **memory_updates**: What canonical facts this phase is expected to establish or modify
  - **approval**: `auto` (Anky validates) or `human` (human must approve)

## Rules

1. Every engagement with 3+ phases MUST have a workflow file.
2. No phase may begin until the previous phase's quality gate passes.
3. ONE-WAY DOOR decisions MUST have `approval: human`.
4. Every phase that produces quantitative output MUST include a `memory_updates` field.
5. Anky spot-checks between phases (not just at the end).
