---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-176
source_hash: sha256:78fdb292ce71b81a
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, diff-aware, knowledge-entry, qa-methodology, quality-assurance, regression-testing, testing]
related: [RIU-001, RIU-062]
handled_by: [architect, debugger, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I scope QA testing based on what actually changed instead of testing everything?

Use diff-aware QA scoping: start from the code diff, trace to affected components, then select a testing tier. Step 1 — Change scope analysis: read the diff, identify which files changed, map those to affected routes, services, and UI components. Step 2 — Tier selection based on risk: Quick (under 2 min, smoke test for low-risk changes), Standard (5-15 min, affected routes plus adjacent components for most PRs), or Exhaustive (30-60 min, full coverage for major releases, security changes, or data model changes). Step 3 — Test plan ordered by risk: for each affected component, test happy path, one failure path, and one edge case. Step 4 — Health score: quantify quality 0-100 with category breakdown so you can track improvement over time. Step 5 — Regression delta: compare against previous baseline to identify what improved, what regressed, and what is new. The key insight is that testing everything equally wastes time on unchanged code while under-testing the actual changes.

## Definition

Use diff-aware QA scoping: start from the code diff, trace to affected components, then select a testing tier. Step 1 — Change scope analysis: read the diff, identify which files changed, map those to affected routes, services, and UI components. Step 2 — Tier selection based on risk: Quick (under 2 min, smoke test for low-risk changes), Standard (5-15 min, affected routes plus adjacent components for most PRs), or Exhaustive (30-60 min, full coverage for major releases, security changes, or data model changes). Step 3 — Test plan ordered by risk: for each affected component, test happy path, one failure path, and one edge case. Step 4 — Health score: quantify quality 0-100 with category breakdown so you can track improvement over time. Step 5 — Regression delta: compare against previous baseline to identify what improved, what regressed, and what is new. The key insight is that testing everything equally wastes time on unchanged code while under-testing the actual changes.

## Evidence

- **Tier 3 (entry-level)**: [garrytan/gstack qa skill — diff-aware tiered QA methodology](https://github.com/garrytan/gstack)

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

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-176.
Evidence tier: 3.
Journey stage: all.
