---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-096
source_hash: sha256:4212019c62133fa9
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, knowledge-entry, palette-meta, riu-selection, taxonomy, workflow]
related: [RIU-001, RIU-002, RIU-003, RIU-004]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I select RIUs for a given problem in Palette?

Per Palette Tier 3 workflow, RIU selection follows this process:

## Definition

Per Palette Tier 3 workflow, RIU selection follows this process:

**Step 1: Extract Observed Trigger Signals**
- List explicit signals from engagement input (bullet format)
- Example: "Stakeholders have conflicting goals", "No clear success metric", "Requirements change weekly"

**Step 2: Retrieve BROAD Candidate RIUs** (aim 8-15):
- Search taxonomy by trigger_signals (first-class evidence)
- Use problem_type as soft anchor (not constraint)
- Bias toward coverage + relevance, not premature narrowing
- "NO MATCH" is valid - surfaces gaps explicitly

**Step 3: Indicate Match Strength**:
- **STRONG**: Trigger signals directly match, problem pattern aligns
- **MODERATE**: Partial match, some signals align
- **WEAK**: Tangential relevance, consider but don't force

**Step 4: Narrow to Focused Selection** (3-5 RIUs):
- Prioritize STRONG matches
- Consider dependencies (some RIUs require others first)
- Check reversibility (prefer TWO-WAY DOOR RIUs early)
- Validate against constraints

**Matching Rules**:
- Coordinates (industry/category/use_case) are soft anchors only
- Multiple RIUs may apply simultaneously
- When uncertain, prefer broader coverage over forced fit
- If no match, surface gap and consider creating new RIU

**Example** (from Palette implementation):
- **Problem**: "Build first Palette agent"
- **Trigger Signals**: "New agent needed", "No validation framework", "Need test scenarios"
- **Candidates**: RIU-511 (Agent Capability Design), RIU-540 (Agent Fixture Design), RIU-003 (Implementation Scoping)
- **Match Strength**: All STRONG
- **Selected**: All 3 (logged in decisions.md)

**Anti-patterns**:
- Don't force RIU match when none fits (surface gap instead)
- Don't select RIUs based on name alone (check trigger_signals)
- Don't skip broad candidate phase (premature narrowing loses options)


## Evidence

- **Tier 3 (entry-level)**: Palette Tier 3 - RIU Matching Rules (`palette/.steering/decisions-prompt.md`)
- **Tier 3 (entry-level)**: Palette Taxonomy v1.1 (`palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-002](../rius/RIU-002.md)
- [RIU-003](../rius/RIU-003.md)
- [RIU-004](../rius/RIU-004.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-096.
Evidence tier: 3.
Journey stage: all.
