---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-133
source_hash: sha256:628998952ff1ef5f
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [data-governance, data-quality, foundation, inventory, knowledge-entry, source-of-truth]
related: [RIU-011, RIU-013, RIU-019]
handled_by: [architect, builder, researcher]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I build a source-of-truth inventory when multiple systems claim to own the same data?

Use RIU-013 to create a structured inventory with five columns per data field: Field Name, Authoritative System, System Owner (person), Update Cadence (real-time / hourly / daily / manual), and Trust Level (gold / silver / bronze). Start with the critical-path fields for your engagement — do not attempt to inventory everything. For each contested field, apply the "last writer wins" test: which system is the one that humans actually update when the data changes? That system is gold-tier authoritative. Systems that read from it are silver. Systems that have stale copies are bronze and should be flagged for eventual deprecation or sync. Common failure patterns: (1) shadow spreadsheets that override the "official" system — interview operators, not just architects; (2) post-merger environments where two CRMs both claim to own customer records — resolve by picking one as authoritative for specific field groups (e.g., billing fields from System A, engagement fields from System B); (3) timestamp-free systems where staleness is undetectable — add last_modified tracking as a prerequisite. Cross-reference with RIU-019 (Data Lineage Sketch) to visualize the flow between systems.

## Definition

Use RIU-013 to create a structured inventory with five columns per data field: Field Name, Authoritative System, System Owner (person), Update Cadence (real-time / hourly / daily / manual), and Trust Level (gold / silver / bronze). Start with the critical-path fields for your engagement — do not attempt to inventory everything. For each contested field, apply the "last writer wins" test: which system is the one that humans actually update when the data changes? That system is gold-tier authoritative. Systems that read from it are silver. Systems that have stale copies are bronze and should be flagged for eventual deprecation or sync. Common failure patterns: (1) shadow spreadsheets that override the "official" system — interview operators, not just architects; (2) post-merger environments where two CRMs both claim to own customer records — resolve by picking one as authoritative for specific field groups (e.g., billing fields from System A, engagement fields from System B); (3) timestamp-free systems where staleness is undetectable — add last_modified tracking as a prerequisite. Cross-reference with RIU-019 (Data Lineage Sketch) to visualize the flow between systems.

## Evidence

- **Tier 3 (entry-level)**: [DAMA-DMBOK: Data Management Body of Knowledge](https://www.dama.org/cpages/body-of-knowledge)
- **Tier 3 (entry-level)**: [Databricks: Data Governance Best Practices](https://www.databricks.com/glossary/data-governance)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-011](../rius/RIU-011.md)
- [RIU-013](../rius/RIU-013.md)
- [RIU-019](../rius/RIU-019.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-133.
Evidence tier: 3.
Journey stage: foundation.
