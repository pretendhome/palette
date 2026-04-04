---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-175
source_hash: sha256:51d983c65a289ae8
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, checklist, deployment, knowledge-entry, operational-safety, release-engineering, rollback]
related: [RIU-001, RIU-062]
handled_by: [architect, debugger, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I build a release checklist that prevents deployment failures?

A release checklist covers six areas in order: (1) Migration safety — is every DB migration backward-compatible and zero-downtime? Are there table locks? (2) Feature flags — should any part be behind a flag for gradual rollout? (3) Rollout order — correct sequence (migrate first, deploy second)? Old code and new code running simultaneously — what breaks? (4) Rollback plan — explicit step-by-step, including time estimate. (5) Post-deploy verification — what automated checks run in the first 5 minutes? First hour? (6) Smoke tests — what proves the deployment succeeded? For each area, the checklist should produce a concrete artifact: migration SQL reviewed, feature flag config committed, rollback runbook written, smoke test commands documented. The most common deployment failures come from partial states (old and new code running together) and missing rollback plans, not from the code itself.

## Definition

A release checklist covers six areas in order: (1) Migration safety — is every DB migration backward-compatible and zero-downtime? Are there table locks? (2) Feature flags — should any part be behind a flag for gradual rollout? (3) Rollout order — correct sequence (migrate first, deploy second)? Old code and new code running simultaneously — what breaks? (4) Rollback plan — explicit step-by-step, including time estimate. (5) Post-deploy verification — what automated checks run in the first 5 minutes? First hour? (6) Smoke tests — what proves the deployment succeeded? For each area, the checklist should produce a concrete artifact: migration SQL reviewed, feature flag config committed, rollback runbook written, smoke test commands documented. The most common deployment failures come from partial states (old and new code running together) and missing rollback plans, not from the code itself.

## Evidence

- **Tier 3 (entry-level)**: [garrytan/gstack ship skill — release hygiene methodology](https://github.com/garrytan/gstack)

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

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-175.
Evidence tier: 3.
Journey stage: all.
