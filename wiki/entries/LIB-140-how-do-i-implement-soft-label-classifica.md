---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-140
source_hash: sha256:3dc01143ea1f7a67
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [calibration, classification, knowledge-entry, orchestration, soft-labels, uncertainty]
related: [RIU-021, RIU-033, RIU-086]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I implement soft-label classification that avoids overconfident wrong predictions?

RIU-033 implements classification with three key design choices. Choice 1 — Soft Labels: instead of returning a single hard label, return a probability distribution across all candidate labels. This preserves uncertainty information that hard labels destroy. For example, instead of "category: fraud" return "fraud: 0.72, legitimate: 0.18, unclear: 0.10". Choice 2 — Abstention: define an explicit "abstain" option. When the highest-confidence label is below a threshold (typically 0.6-0.7), the classifier should abstain rather than guess. Abstentions are signals, not failures — they identify cases that need human review, new labels, or more training data. Track abstention rate as a key metric; rising abstention often indicates concept drift or a new category emerging. Choice 3 — Uncertainty Logging: log the full probability distribution for every classification, not just the winner. This enables: (a) offline analysis of decision boundaries, (b) detection of bimodal distributions (the model is genuinely uncertain, not randomly noisy), (c) calibration checks (are predicted 80% confidence cases actually correct 80% of the time?). Implementation: use LLM-based classification with logprobs enabled, or traditional ML classifiers with predict_proba(). For LLM-based, request structured output with a confidence field and validate calibration on your eval set. The most dangerous failure mode is overconfident wrong labels — mitigate by calibrating confidence scores against ground truth and adjusting thresholds accordingly.

## Definition

RIU-033 implements classification with three key design choices. Choice 1 — Soft Labels: instead of returning a single hard label, return a probability distribution across all candidate labels. This preserves uncertainty information that hard labels destroy. For example, instead of "category: fraud" return "fraud: 0.72, legitimate: 0.18, unclear: 0.10". Choice 2 — Abstention: define an explicit "abstain" option. When the highest-confidence label is below a threshold (typically 0.6-0.7), the classifier should abstain rather than guess. Abstentions are signals, not failures — they identify cases that need human review, new labels, or more training data. Track abstention rate as a key metric; rising abstention often indicates concept drift or a new category emerging. Choice 3 — Uncertainty Logging: log the full probability distribution for every classification, not just the winner. This enables: (a) offline analysis of decision boundaries, (b) detection of bimodal distributions (the model is genuinely uncertain, not randomly noisy), (c) calibration checks (are predicted 80% confidence cases actually correct 80% of the time?). Implementation: use LLM-based classification with logprobs enabled, or traditional ML classifiers with predict_proba(). For LLM-based, request structured output with a confidence field and validate calibration on your eval set. The most dangerous failure mode is overconfident wrong labels — mitigate by calibrating confidence scores against ground truth and adjusting thresholds accordingly.

## Evidence

- **Tier 1 (entry-level)**: [Google: Classification Best Practices for ML](https://developers.google.com/machine-learning/guides/text-classification)
- **Tier 1 (entry-level)**: [Databricks: MLflow Model Evaluation](https://docs.databricks.com/en/mlflow/llm-evaluate.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-033](../rius/RIU-033.md)
- [RIU-086](../rius/RIU-086.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-140.
Evidence tier: 1.
Journey stage: orchestration.
