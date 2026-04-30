---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-022
source_hash: sha256:e31aef6e8b939632
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [evaluation, expert-comparison, knowledge-entry, quality-assurance, testing, validation]
related: [RIU-006, RIU-014, RIU-021, RIU-540]
handled_by: [architect, builder, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What testing strategy validates that AI behavior matches human expert judgment?

Use a multi-layered validation strategy: create expert-labeled datasets, measure agreement, automate with LLM-as-a-Judge, and maintain human oversight.

## Definition

Use a multi-layered validation strategy: create expert-labeled datasets, measure agreement, automate with LLM-as-a-Judge, and maintain human oversight.
      
      **Step 1: Create Golden Set with experts (RIU-021)**
      - Generate candidate Q&A pairs using LLM, then have experts review/correct
      - Use FMEval triplet format: (question, context, expected_answer)
      - Include edge cases and failure modes discovered during testing
      - Amazon SageMaker Ground Truth Plus provides expert workforce for labeling
      - Minimum: 50-100 examples for initial validation; 500+ for robust evaluation
      
      **Step 2: Measure agreement metrics**
      - **Recall**: Does AI find what experts find?
      - **Precision**: Does AI avoid false positives experts would reject?
      - **F1 Score**: Balanced measure of both
      - **Win rate**: In head-to-head comparison, how often does AI match/beat expert?
      - **Confidence intervals**: Statistical significance of agreement
      - Target: >80% agreement with expert judgment (ρ > 0.8 correlation)
      
      **Step 3: Automate with LLM-as-a-Judge**
      - Use Amazon Nova LLM-as-a-Judge for unbiased cross-model evaluation
      - Use judge from *different model family* to avoid self-preference bias
      - Version control evaluation prompts in prompt registry
      - Validate judge outputs against human-labeled subset periodically
      - Integrate into CI/CD with threshold scores (stage-gate testing)
      
      **Step 4: Scale with RLAIF**
      - When expert time is limited, use RLAIF (AI-generated feedback)
      - Reduces SME workload by ~80% while maintaining quality
      - Still require periodic human audit of AI judge accuracy
      
      **Step 5: Production validation**
      - Blue-green deployment: route % of traffic to new model, compare outputs
      - Major releases: require full or partial human evaluation before rollout
      - Escalation-based HITL: route low-confidence outputs to human experts
      - Monitor agreement metrics continuously in production
      
      **PALETTE integration:**
      - Store Golden Set in RIU-021 (Golden Set + Offline Evaluation Harness)
      - Document evaluation thresholds in Success Metrics Charter (RIU-006)
      - Track expert disagreements as edge cases (RIU-014)
      - Log validation results in decisions.md when they affect deployment decisions
      
      Key insight: Human experts are ground truth, but they don't scale. Use experts to calibrate automated evaluation, then automate — but always maintain human audit loop.

## Evidence

- **Tier 1 (entry-level)**: [Ground truth generation and review best practices for evaluating generative AI with FMEval](https://aws.amazon.com/blogs/machine-learning/ground-truth-generation-and-review-best-practices-for-evaluating-generative-ai-question-answering-with-fmeval/)
- **Tier 1 (entry-level)**: [Ground truth curation and metric interpretation best practices with FMEval](https://aws.amazon.com/blogs/machine-learning/ground-truth-curation-and-metric-interpretation-best-practices-for-evaluating-generative-ai-question-answering-using-fmeval/)
- **Tier 1 (entry-level)**: [High-quality human feedback from Amazon SageMaker Ground Truth Plus](https://aws.amazon.com/blogs/machine-learning/high-quality-human-feedback-for-your-generative-ai-applications-from-amazon-sagemaker-ground-truth-plus/)
- **Tier 1 (entry-level)**: [Evaluating generative AI models with Amazon Nova LLM-as-a-Judge](https://aws.amazon.com/blogs/machine-learning/evaluating-generative-ai-models-with-amazon-nova-llm-as-a-judge-on-amazon-sagemaker-ai/)
- **Tier 1 (entry-level)**: [Model Evaluation and Selection Criteria Overview - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/2_0_technical_foundations_and_patterns/2_6_model_evaluation_and_selection_criteria/index.html)
- **Tier 1 (entry-level)**: [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (NeurIPS 2023)](https://arxiv.org/abs/2306.05685)
- **Tier 1 (entry-level)**: [Anthropic: Constitutional AI — Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-006](../rius/RIU-006.md)
- [RIU-014](../rius/RIU-014.md)
- [RIU-021](../rius/RIU-021.md)
- [RIU-540](../rius/RIU-540.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-022.
Evidence tier: 1.
Journey stage: evaluation.
