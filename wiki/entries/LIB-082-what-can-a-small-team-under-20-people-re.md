---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-082
source_hash: sha256:80e216f4899eb4c2
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, indie-development, knowledge-entry, scope-management, small-team, team-size]
related: [RIU-003, RIU-120, RIU-121]
handled_by: [architect, builder, debugger]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What can a small team (under 20 people) realistically achieve in game development?

Based on proven examples from your research:

## Definition

Based on proven examples from your research:

**Hades (Supergiant Games) - 20 core people**:
- Result: 1M+ copies sold, Game of the Year 2020
- Approach: 2D isometric, stylized art (not photorealistic)
- Complexity: MEDIUM (roguelike structure = replayability without massive content)
- Key insight: Strong design + focused scope > large team + weak design

**Dead Cells (Motion Twin) - Small worker cooperative**:
- Result: Critical acclaim, strong indie success
- Approach: 2D roguelite-Metroidvania
- Complexity: LOW-MEDIUM

**Slay the Spire (MegaCrit) - Very small indie**:
- Result: Genre-defining hit
- Approach: Card-based, minimal graphics
- Complexity: LOW

**Pattern**: Small teams succeed by:
1. Choosing stylized art over photorealism (reduces art load dramatically)
2. Using roguelike/roguelite structure (replayability without massive content creation)
3. Focusing on strong core mechanics over feature breadth
4. Targeting 3-6 month delivery cycles to build confidence

**For 2-person teams (your context)**:
- Achievable: 4-player co-op with strong core loop, stylized graphics, procedural elements
- Not achievable: AAA graphics, massive open world, 100+ hours of unique content
- Timeline: 12-16 weeks for MVP with systematic implementation (per your infrastructure research)

**Critical**: Engineering complexity ≠ success. Hades beat AAA competitors with 20 people.


## Evidence

- **Tier 3 (entry-level)**: Mythical Games Research - Hades Analysis (`implementations/dev/dev-mythfall-game/RESEARCH_HANDOFF_ADAM.md`)
- **Tier 3 (entry-level)**: Optimal Multiplayer Game Infrastructure - Timeline (`implementations/dev/dev-mythfall-game/Optimal Multiplayer Game Infrastructure-.pdf`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-120](../rius/RIU-120.md)
- [RIU-121](../rius/RIU-121.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-082.
Evidence tier: 3.
Journey stage: all.
