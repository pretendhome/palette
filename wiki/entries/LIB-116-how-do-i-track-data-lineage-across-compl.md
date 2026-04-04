---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-116
source_hash: sha256:419a64e413763184
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [compliance, data-lineage, dbt, knowledge-entry, observability, orchestration]
related: [RIU-011, RIU-019]
handled_by: [architect, builder, researcher]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I track data lineage across complex multi-service AI pipelines?

Use automated lineage tools rather than manual sketches once pipelines span 3+ services. dbt captures SQL-level lineage natively. For broader pipeline lineage, implement OpenLineage (open standard) with Marquez for visualization. Key decision — lineage granularity must match your debugging needs. Column-level lineage is needed for regulated industries (healthcare, finance); table-level is sufficient for most AI/ML pipelines. Start with table-level and add column-level only when compliance requires it. Integrate lineage capture into your CI/CD pipeline so it stays current automatically.

## Definition

Use automated lineage tools rather than manual sketches once pipelines span 3+ services. dbt captures SQL-level lineage natively. For broader pipeline lineage, implement OpenLineage (open standard) with Marquez for visualization. Key decision — lineage granularity must match your debugging needs. Column-level lineage is needed for regulated industries (healthcare, finance); table-level is sufficient for most AI/ML pipelines. Start with table-level and add column-level only when compliance requires it. Integrate lineage capture into your CI/CD pipeline so it stays current automatically.

## Evidence

- **Tier 3 (entry-level)**: [OpenLineage - Open Platform for Data Lineage](https://openlineage.io/)
- **Tier 3 (entry-level)**: [Atlan: Complete Guide to Data Lineage Tracking for 2026](https://atlan.com/know/data-lineage-tracking/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-011](../rius/RIU-011.md)
- [RIU-019](../rius/RIU-019.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-116.
Evidence tier: 3.
Journey stage: orchestration.
