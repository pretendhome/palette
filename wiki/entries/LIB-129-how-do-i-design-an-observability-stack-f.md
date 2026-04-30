---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-129
source_hash: sha256:6250fbf2c27e2843
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [datadog, knowledge-entry, monitoring, observability, orchestration, production]
related: [RIU-061, RIU-070, RIU-542]
handled_by: [architect, builder, monitor]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design an observability stack for AI/ML systems in production?

AI observability requires three layers — infrastructure metrics (CPU, memory, latency), model metrics (prediction quality, drift, throughput), and business metrics (user satisfaction, task completion). Choose one primary platform — Datadog for enterprise-scale with broad integrations, Honeycomb for high-cardinality debugging, New Relic for best free tier (100GB/month, all features). Key decision — start with the free tier of your chosen platform and validate it captures what you need before committing budget. For AI-specific observability, add Arize AI or Evidently for model monitoring (drift, data quality, feature importance). Do not build custom dashboards until you have proven the platform captures the signals that predict production incidents.

## Definition

AI observability requires three layers — infrastructure metrics (CPU, memory, latency), model metrics (prediction quality, drift, throughput), and business metrics (user satisfaction, task completion). Choose one primary platform — Datadog for enterprise-scale with broad integrations, Honeycomb for high-cardinality debugging, New Relic for best free tier (100GB/month, all features). Key decision — start with the free tier of your chosen platform and validate it captures what you need before committing budget. For AI-specific observability, add Arize AI or Evidently for model monitoring (drift, data quality, feature importance). Do not build custom dashboards until you have proven the platform captures the signals that predict production incidents.

## Evidence

- **Tier 1 (entry-level)**: [Palette internal knowledge base](https://github.com/pretendhome/pretendhome)
- **Tier 1 (entry-level)**: FDE field experience (`internal`)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-061](../rius/RIU-061.md)
- [RIU-070](../rius/RIU-070.md)
- [RIU-542](../rius/RIU-542.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-129.
Evidence tier: 1.
Journey stage: orchestration.
