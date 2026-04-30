---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-097
source_hash: sha256:dd9e10d7a47fbb90
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, decision-logging, documentation, knowledge-entry, palette-meta, restartability]
related: [RIU-001, RIU-003, RIU-004]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What must be logged in decisions.md for restartability?

Per Palette Tier 1 and Tier 3, decisions.md is append-only and must contain:

## Definition

Per Palette Tier 1 and Tier 3, decisions.md is append-only and must contain:

**A) Toolkit-Changing ONE-WAY DOOR Decisions** (manual header list):
- Decisions that change Palette itself
- Example: "Promoted Orchestrator from DESIGN-ONLY to implemented"
- Keep this section small and current

**B) Engagement Updates** (append new blocks):

**Required in each update**:
1. **Semantic Blueprint** (or reference to existing):
   - Goal, Roles, Capabilities, Constraints, Non-goals
   - What changed since last update

2. **Selected RIUs**:
   - List of RIUs applied (with match strength if relevant)
   - Rationale for selection

3. **Artifacts Created/Updated**:
   - File paths
   - What each artifact does

4. **Agent Maturity Updates**:
   - Success/failure logged
   - Impressions updated
   - Tier changes noted

5. **Next Checks**:
   - What needs to happen next
   - Open questions or blockers

**Optional (log if material)**:
- Post-mortems when agents fail
- Assumptions that drove decisions
- Knowledge gaps detected (reference KGE-ID)

**Do NOT log**:
- Exhaustive execution logs
- Every file touched
- Every source consulted
- Routine TWO-WAY DOOR decisions (unless they fail or affect restartability)

**Format**:
```
---
### Engagement Update: YYYY-MM-DD / [DESCRIPTIVE-ID]

#### Semantic Blueprint
[5 elements or reference]

#### Selected RIUs
[List with rationale]

#### Artifacts Created
[Paths and descriptions]

#### Agent Maturity Update
[Tracking block]

#### Next Checks
[What's next]

---
```

**Purpose**: Enable restartability from scratch using existing documentation. Someone should be able to read decisions.md and understand what was built, why, and what's next.

**From Palette experience**:
- Bootstrap entry documents initial toolkit setup
- Researcher implementation logged with RIU selection and artifacts
- Architect implementation logged with maturity tracking


## Evidence

- **Tier 3 (entry-level)**: Palette Tier 1 - Decision Persistence (`palette/.steering/palette-core.md`)
- **Tier 3 (entry-level)**: Palette Tier 3 - Engagement Update Template (`palette/.steering/decisions-prompt.md`)
- **Tier 3 (entry-level)**: Palette decisions.md - Live Example (`palette/decisions.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-003](../rius/RIU-003.md)
- [RIU-004](../rius/RIU-004.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-097.
Evidence tier: 3.
Journey stage: all.
