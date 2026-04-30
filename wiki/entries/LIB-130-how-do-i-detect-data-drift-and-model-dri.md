---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-130
source_hash: sha256:29e82c63a6170088
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [arize, drift-detection, evidently, knowledge-entry, monitoring, specialization]
related: [RIU-524, RIU-543]
handled_by: [debugger, monitor, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I detect data drift and model drift in production AI systems?

Use a dedicated drift detection platform — Arize AI (managed, production-grade, supports embeddings and tabular data) or Evidently AI (open-source, Python-native, good for experimentation). Monitor three drift types — data drift (input feature distributions shift), prediction drift (model output distribution shifts), and concept drift (the real-world relationship between inputs and outcomes changes). Set statistical thresholds — PSI above 0.2 or KS test p-value below 0.05 triggers investigation, not automatic retraining. Key insight — most drift is seasonal or cyclical, not catastrophic. Build dashboards that show drift trends over time, not just point-in-time alerts. Retrain only when drift correlates with measured quality degradation.

## Definition

Use a dedicated drift detection platform — Arize AI (managed, production-grade, supports embeddings and tabular data) or Evidently AI (open-source, Python-native, good for experimentation). Monitor three drift types — data drift (input feature distributions shift), prediction drift (model output distribution shifts), and concept drift (the real-world relationship between inputs and outcomes changes). Set statistical thresholds — PSI above 0.2 or KS test p-value below 0.05 triggers investigation, not automatic retraining. Key insight — most drift is seasonal or cyclical, not catastrophic. Build dashboards that show drift trends over time, not just point-in-time alerts. Retrain only when drift correlates with measured quality degradation.

## Evidence

- **Tier 1 (entry-level)**: [Palette internal knowledge base](https://github.com/pretendhome/pretendhome)
- **Tier 1 (entry-level)**: FDE field experience (`internal`)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-524](../rius/RIU-524.md)
- [RIU-543](../rius/RIU-543.md)

## Handled By

- [Debugger](../agents/debugger.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-524](../paths/RIU-524-llm-output-quality-monitoring.md) — hands-on exercise
- [RIU-543](../paths/RIU-543-drift-detection.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-130.
Evidence tier: 1.
Journey stage: specialization.
