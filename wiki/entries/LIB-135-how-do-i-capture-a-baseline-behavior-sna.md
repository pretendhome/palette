---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-135
source_hash: sha256:96dc34c0a04a7413
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [baseline, evaluation, knowledge-entry, measurement, regression]
related: [RIU-020, RIU-086, RIU-604]
handled_by: [architect, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I capture a baseline behavior snapshot before making changes to an AI system?

RIU-020 defines baseline capture as a three-artifact process. Artifact 1 — Golden Inputs: select 50-200 representative inputs that cover the key operating scenarios (happy path, edge cases, adversarial inputs, empty/null inputs). These become your regression anchors. Artifact 2 — Baseline Outputs: run golden inputs through the current system and store the exact outputs with timestamps, model version, and configuration. For non-deterministic systems (LLMs), run each input 3-5 times and record the distribution of outputs. Artifact 3 — Baseline Metrics: compute aggregate metrics (accuracy, latency p50/p95/p99, cost per request, error rate, token usage). Store as baseline_metrics.json. The baseline serves three purposes: (1) regression detection — any change that degrades baseline metrics is a red flag; (2) improvement measurement — you can only claim improvement if you have a before; (3) rollback decision support — if the new version is worse, you have a concrete comparison. Common failure: using a non-representative baseline (e.g., only happy-path inputs). Mitigate by including inputs from production logs stratified by frequency and error history. Cross-reference with RIU-604 (AI ROI Quantification) — the baseline is also the "before" measurement for ROI calculations.

## Definition

RIU-020 defines baseline capture as a three-artifact process. Artifact 1 — Golden Inputs: select 50-200 representative inputs that cover the key operating scenarios (happy path, edge cases, adversarial inputs, empty/null inputs). These become your regression anchors. Artifact 2 — Baseline Outputs: run golden inputs through the current system and store the exact outputs with timestamps, model version, and configuration. For non-deterministic systems (LLMs), run each input 3-5 times and record the distribution of outputs. Artifact 3 — Baseline Metrics: compute aggregate metrics (accuracy, latency p50/p95/p99, cost per request, error rate, token usage). Store as baseline_metrics.json. The baseline serves three purposes: (1) regression detection — any change that degrades baseline metrics is a red flag; (2) improvement measurement — you can only claim improvement if you have a before; (3) rollback decision support — if the new version is worse, you have a concrete comparison. Common failure: using a non-representative baseline (e.g., only happy-path inputs). Mitigate by including inputs from production logs stratified by frequency and error history. Cross-reference with RIU-604 (AI ROI Quantification) — the baseline is also the "before" measurement for ROI calculations.

## Evidence

- **Tier 1 (entry-level)**: [Google: MLOps — Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- **Tier 1 (entry-level)**: [Anthropic: Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agent-patterns)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-020](../rius/RIU-020.md)
- [RIU-086](../rius/RIU-086.md)
- [RIU-604](../rius/RIU-604.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-135.
Evidence tier: 1.
Journey stage: evaluation.
