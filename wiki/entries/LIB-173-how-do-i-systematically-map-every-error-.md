---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-173
source_hash: sha256:be78970db188122c
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, code-review, error-handling, failure-modes, knowledge-entry, production-safety, reliability]
related: [RIU-001, RIU-062]
handled_by: [architect, debugger, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I systematically map every error path in a new feature before shipping?

Use an error/rescue registry — a table that maps every method or codepath that can fail to its specific exception classes, whether each is rescued, what the rescue action is, and what the user sees. Format: METHOD | WHAT CAN GO WRONG | EXCEPTION CLASS | RESCUED? | RESCUE ACTION | USER SEES. Rules: (1) Never use catch-all exception handling — name specific exceptions. (2) Every rescued error must either retry with backoff, degrade gracefully with a user-visible message, or re-raise with added context. (3) For every data flow, trace four paths: happy path, nil input, empty input, and upstream error. (4) Any row where RESCUED=N and TESTED=N and USER SEES=silent is a critical gap. This methodology comes from production code review practice where the class of bugs that survive CI but break in production are almost always unhandled error paths, not logic errors.

## Definition

Use an error/rescue registry — a table that maps every method or codepath that can fail to its specific exception classes, whether each is rescued, what the rescue action is, and what the user sees. Format: METHOD | WHAT CAN GO WRONG | EXCEPTION CLASS | RESCUED? | RESCUE ACTION | USER SEES. Rules: (1) Never use catch-all exception handling — name specific exceptions. (2) Every rescued error must either retry with backoff, degrade gracefully with a user-visible message, or re-raise with added context. (3) For every data flow, trace four paths: happy path, nil input, empty input, and upstream error. (4) Any row where RESCUED=N and TESTED=N and USER SEES=silent is a critical gap. This methodology comes from production code review practice where the class of bugs that survive CI but break in production are almost always unhandled error paths, not logic errors.

## Evidence

- **Tier 1 (entry-level)**: [garrytan/gstack review skill — error/rescue map methodology](https://github.com/garrytan/gstack)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-062](../rius/RIU-062.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-173.
Evidence tier: 1.
Journey stage: all.
