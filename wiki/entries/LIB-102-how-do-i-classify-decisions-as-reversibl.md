---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-102
source_hash: sha256:6fd1ed04e36eaffa
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, knowledge-entry]
related: [RIU-001, RIU-105]
handled_by: [architect, narrator, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I classify decisions as reversible vs irreversible?

All material decisions must be classified before execution.

## Definition

All material decisions must be classified before execution.

TWO-WAY DOOR (Reversible):
- Cheap to undo or change
- Low organizational impact
- Can be rolled back without significant cost
- AI may proceed autonomously
- Log only if material or if it fails
- Examples: refactoring code, A/B testing, updating docs, 
  changing variable names, adjusting UI layout

ONE-WAY DOOR (Irreversible):
- Hard or expensive to reverse
- High organizational impact
- Externally binding commitments
- Requires explicit human approval before proceeding
- Must be logged with rationale in decisions.md
- Examples: database selection, architecture commitments, 
  deployments, data deletion, security posture changes,
  API contracts, compliance decisions

The "Trust Trade-Off":
- Agents need power to be useful (autonomy, tools, access)
- Every ounce of power introduces risk
- ONE-WAY DOOR classification manages this trade-off
- Give agents "a leash long enough to do their job, 
  but short enough to keep them from running into traffic"

Who performs classification:
- Primary: Architect (Architecture agent) - designs systems, identifies ONE-WAY DOORs
- Secondary: Any agent that detects a ONE-WAY DOOR must flag and stop
- Validation: Validator reviews classification during quality checks
- Override: Human can reclassify if agent gets it wrong

Decision process:
1. Agent identifies decision point
2. Classifies as TWO-WAY or ONE-WAY DOOR
3. If ONE-WAY: Emit "🚨 ONE-WAY DOOR — confirmation required"
4. Pause execution, present rationale to human
5. Wait for explicit approval before proceeding
6. Log decision + rationale in decisions.md
7. If TWO-WAY: Proceed, log if material

Cost of getting it wrong:
- Treating ONE-WAY as TWO-WAY: Silent commitments, locked-in risk, 
  irreversible harm, loss of trust
- Treating TWO-WAY as ONE-WAY: Unnecessary friction, slowed velocity, 
  reduced agent utility

Edge cases:
- When uncertain: Default to ONE-WAY DOOR (safer)
- Context matters: Deleting test data = TWO-WAY, deleting prod data = ONE-WAY
- Cumulative effect: Multiple TWO-WAY decisions can compound into ONE-WAY impact

Integration with Palette:
- Tier 1 defines the principle (immutable)
- This Library entry provides implementation guidance (reusable)
- RIU-001 (Convergence Brief) includes decision classification
- RIU-105 (Security) - security decisions are often ONE-WAY DOOR


## Evidence

- **Tier 1 (entry-level)**: [Amazon's 'one-way door' decision framework (Jeff Bezos shareholder letters)](https://www.amazon.com/p/feature/z6o9g6sysxur57t)
- **Tier 1 (entry-level)**: [Google Introduction to Agents (Nov 2025) - Trust trade-off concept](https://cloud.google.com/use-cases/agents)
- **Tier 1 (entry-level)**: Palette Tier 1 (palette-core.md) - Decision Handling section (`palette/.steering/palette-core.md#decision-handling`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-105](../rius/RIU-105.md)

## Handled By

- [Architect](../agents/architect.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-102.
Evidence tier: 1.
Journey stage: all.
