---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-134
source_hash: sha256:2b683a4c282afe20
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [data-integration, foundation, knowledge-entry, mapping, schema, transform]
related: [RIU-011, RIU-018, RIU-086]
handled_by: [architect, builder, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I create a schema mapping table that eliminates field mapping churn between source and target systems?

RIU-018 prescribes a mapping table with seven columns: Source Field, Source Type, Target Field, Target Type, Transform Rule, Default Value, and Provenance (who agreed to this mapping and when). Step 1 — Freeze source schema using RIU-011 (Data Contract) before mapping begins. If the source schema is still shifting, mapping is premature and will cause rework. Step 2 — Document every transform explicitly: type coercion (string to int), unit conversion (USD cents to dollars), enum mapping (source status codes to target status codes), null handling (default vs reject vs propagate). Never leave an implicit transform undocumented — this is the number one cause of mapping bugs. Step 3 — Validate with sample payloads. Run 10-20 representative records through the mapping and verify outputs with the target system owner. Step 4 — Write mapping tests. Each transform rule should have at least one positive test and one edge case test (null input, max-length input, unicode). Store these as regression tests (RIU-086). Optional fields are the most dangerous — they often appear in only 5% of records and their absence is not caught until production.

## Definition

RIU-018 prescribes a mapping table with seven columns: Source Field, Source Type, Target Field, Target Type, Transform Rule, Default Value, and Provenance (who agreed to this mapping and when). Step 1 — Freeze source schema using RIU-011 (Data Contract) before mapping begins. If the source schema is still shifting, mapping is premature and will cause rework. Step 2 — Document every transform explicitly: type coercion (string to int), unit conversion (USD cents to dollars), enum mapping (source status codes to target status codes), null handling (default vs reject vs propagate). Never leave an implicit transform undocumented — this is the number one cause of mapping bugs. Step 3 — Validate with sample payloads. Run 10-20 representative records through the mapping and verify outputs with the target system owner. Step 4 — Write mapping tests. Each transform rule should have at least one positive test and one edge case test (null input, max-length input, unicode). Store these as regression tests (RIU-086). Optional fields are the most dangerous — they often appear in only 5% of records and their absence is not caught until production.

## Evidence

- **Tier 1 (entry-level)**: [DAMA-DMBOK: Data Integration and Interoperability](https://www.dama.org/cpages/body-of-knowledge)
- **Tier 1 (entry-level)**: [AWS Glue Schema Registry](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-011](../rius/RIU-011.md)
- [RIU-018](../rius/RIU-018.md)
- [RIU-086](../rius/RIU-086.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-134.
Evidence tier: 1.
Journey stage: foundation.
