---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-092
source_hash: sha256:4fe1c13057ce9b1e
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [agent-maturity, knowledge-entry, orchestration, palette-meta, reliability, trust-model]
related: [RIU-100, RIU-101, RIU-511]
handled_by: [architect, builder, monitor, narrator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How does agent maturity progression work in Palette?

Palette uses a three-tier maturity model based on empirical reliability:

## Definition

Palette uses a three-tier maturity model based on empirical reliability:

**Tier 1: UNVALIDATED**
- **Status**: New agent, unproven
- **Behavior**: Human-in-the-loop required for EACH execution
- **Promotion**: 10 consecutive successes
- **Use when**: Agent just created, major version bump (V1→V2)

**Tier 2: WORKING**
- **Status**: Proven reliable, but monitored
- **Behavior**: Autonomous execution with review
- **Promotion**: 50 impressions with <5% failure rate
- **Demotion**: Failure occurs while fail_gap ≤ 9 → demote to Tier 1
- **Use when**: Agent works but needs validation at scale

**Tier 3: PRODUCTION**
- **Status**: Fully trusted, autonomous
- **Behavior**: Fully autonomous until failure
- **Demotion**: Two failures within any 10 impressions (fail_gap ≤ 9) → demote to Tier 2
- **Use when**: Agent has proven reliability over time

**Tracking Format** (in decisions.md):
```
agent: researcher
ark_type: Researcher
version: 1.0
status: UNVALIDATED
impressions:
  success: 0
  fail: 0
  fail_gap: 0
notes: First agent implementation
```

**On Success**:
- Increment `success` count
- Increment `fail_gap` (runs since last failure)
- Check promotion criteria

**On Failure**:
- If `fail_gap ≤ 9`: Demote per tier rules
- Set `fail_gap = 0`
- Increment `fail` count
- Log post-mortem in decisions.md

**Versioning Impact**:
- **Major bump** (V1.0 → V2.0): Resets impressions + fail_gap, back to UNVALIDATED
- **Minor bump** (V1.0 → V1.1): Preserves impressions + fail_gap

**Key Insight**: Maturity is about measured trust, not function. A simple agent at PRODUCTION is more valuable than a complex agent at UNVALIDATED.

**Current Palette status** (as of implementation):
- Researcher: 1 success, 0 failures, UNVALIDATED (needs 9 more successes)
- Architect: 0 executions, UNVALIDATED (awaiting first use)


## Evidence

- **Tier 1 (entry-level)**: Palette Tier 2 - Agent Maturity Model (`palette/.steering/assumptions.md`)
- **Tier 1 (entry-level)**: Palette decisions.md - Agent Tracking (`palette/decisions.md`)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-511](../rius/RIU-511.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Narrator](../agents/narrator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-092.
Evidence tier: 1.
Journey stage: orchestration.
