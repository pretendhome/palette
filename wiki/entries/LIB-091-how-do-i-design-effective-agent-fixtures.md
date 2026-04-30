---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-091
source_hash: sha256:fbe98196b50ced39
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [agent-design, fixtures, knowledge-entry, orchestration, palette-meta, testing, validation]
related: [RIU-100, RIU-101, RIU-540]
handled_by: [architect, narrator, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design effective agent fixtures for validation?

Based on Palette agent implementation experience (Researcher RES-001, Architect ARCH-001):

## Definition

Based on Palette agent implementation experience (Researcher RES-001, Architect ARCH-001):

**Fixture Structure**:
```
# Fixture: [Descriptive Name]
Fixture ID: [AGENT-###]
Agent: [Agent Name] v[Version]
Scenario: [What situation this tests]

## Input
Initial Request: [Exact user input]
Expected Clarifying Questions: [List of questions agent should ask]
Sample Answers: [Realistic responses]

## Expected Output
[Structured format agent should produce]

## Success Criteria
✅ [Specific, testable criterion]
✅ [Specific, testable criterion]

## Notes
[What this fixture validates about agent behavior]
```

**Key Principles**:
1. **Test ONE behavior per fixture** - Don't combine multiple scenarios
2. **Use real examples** - RES-001 tests "multiplayer networking research" (actual Mythfall need)
3. **Make success criteria binary** - "Agent asked all 5 questions" not "Agent asked good questions"
4. **Include failure modes** - What should agent NOT do?
5. **Provide realistic inputs** - Not edge cases first, test common path

**Fixture Naming**:
- Format: `[ARK-CODE]-###-[descriptive-name].md`
- Examples: `RES-001-multiplayer-networking.md`, `ARCH-001-multiplayer-architecture.md`
- Store in: `fde/agents/[agent-name]/fixtures/`

**What to test**:
- **Clarification phase**: Does agent ask right questions before acting?
- **Constraint adherence**: Does agent respect its disallowed actions?
- **Output format**: Does agent produce expected structure?
- **Decision classification**: Does agent correctly flag ONE-WAY DOOR vs TWO-WAY DOOR?

**Validation workflow**:
1. Run agent with fixture input
2. Compare output against success criteria
3. Log result in decisions.md (success/fail)
4. Update agent maturity tracking (impressions, fail_gap)

**From Palette experience**:
- RES-001 validates Researcher's clarification-before-search behavior
- ARCH-001 validates Architect's multi-option tradeoff analysis
- Both test agent stays within role boundaries


## Evidence

- **Tier 1 (entry-level)**: Researcher Fixture RES-001 (`palette/agents/researcher/fixtures/RES-001-multiplayer-networking.md`)
- **Tier 1 (entry-level)**: Architect Fixture ARCH-001 (`palette/agents/architect/fixtures/ARCH-001-multiplayer-architecture.md`)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-540](../rius/RIU-540.md)

## Handled By

- [Architect](../agents/architect.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-091.
Evidence tier: 1.
Journey stage: orchestration.
