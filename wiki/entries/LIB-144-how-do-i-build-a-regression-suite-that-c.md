---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-144
source_hash: sha256:4e485ab6fc0a85eb
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [evaluation, knowledge-entry, metamorphic, quality, regression, testing]
related: [RIU-020, RIU-021, RIU-086]
handled_by: [architect, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I build a regression suite that catches regressions beyond a small golden test set using metamorphic testing?

RIU-086 extends traditional golden-set testing with metamorphic testing and invariant checks. Golden Tests (necessary but insufficient): 50-200 curated input-output pairs where the expected output is known. These catch exact regressions but miss novel failures. Metamorphic Tests (the key addition): define properties that must hold under input transformations even when the exact output is unknown. Examples: (a) Paraphrase invariance — rephrasing a query should produce semantically equivalent results; (b) Monotonicity — adding a positive signal should not decrease the score; (c) Symmetry — swapping entity order in a comparison should swap the result; (d) Negation — negating the input should change the output; (e) Subset — a more specific query should return a subset of a broader query. Metamorphic tests are powerful because they do not require ground-truth labels — they test relationships between inputs and outputs. Invariant Checks: define system-level invariants that must always hold. Examples: output schema always valid, confidence scores between 0 and 1, latency below budget, no PII in outputs. Run invariants on every test case. Suite Composition: aim for 60% golden, 25% metamorphic, 15% invariant. Run the full suite on every model update, prompt change, or dependency update. Track pass rate over time — a declining metamorphic pass rate is an early warning of model drift even when golden tests still pass.

## Definition

RIU-086 extends traditional golden-set testing with metamorphic testing and invariant checks. Golden Tests (necessary but insufficient): 50-200 curated input-output pairs where the expected output is known. These catch exact regressions but miss novel failures. Metamorphic Tests (the key addition): define properties that must hold under input transformations even when the exact output is unknown. Examples: (a) Paraphrase invariance — rephrasing a query should produce semantically equivalent results; (b) Monotonicity — adding a positive signal should not decrease the score; (c) Symmetry — swapping entity order in a comparison should swap the result; (d) Negation — negating the input should change the output; (e) Subset — a more specific query should return a subset of a broader query. Metamorphic tests are powerful because they do not require ground-truth labels — they test relationships between inputs and outputs. Invariant Checks: define system-level invariants that must always hold. Examples: output schema always valid, confidence scores between 0 and 1, latency below budget, no PII in outputs. Run invariants on every test case. Suite Composition: aim for 60% golden, 25% metamorphic, 15% invariant. Run the full suite on every model update, prompt change, or dependency update. Track pass rate over time — a declining metamorphic pass rate is an early warning of model drift even when golden tests still pass.

## Evidence

- **Tier 1 (entry-level)**: [Segura et al.: A Survey on Metamorphic Testing (ACM Computing Surveys, 2016)](https://doi.org/10.1145/2907070)
- **Tier 1 (entry-level)**: [Google: Testing ML Systems — ML Test Score](https://research.google/pubs/pub46555/)
- **Tier 1 (entry-level)**: [Ribeiro et al.: Beyond Accuracy — Behavioral Testing of NLP Models (ACL 2020)](https://aclanthology.org/2020.acl-main.442/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-020](../rius/RIU-020.md)
- [RIU-021](../rius/RIU-021.md)
- [RIU-086](../rius/RIU-086.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-144.
Evidence tier: 1.
Journey stage: evaluation.
