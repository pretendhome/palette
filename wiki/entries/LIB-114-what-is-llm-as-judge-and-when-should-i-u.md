---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-114
source_hash: sha256:5cb3702ea958fb34
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [automated-evaluation, evaluation, knowledge-entry, llm-as-judge, quality-metrics, ragas]
related: [RIU-252, RIU-524]
handled_by: [architect, monitor, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What is LLM-as-judge and when should I use it?

LLM-as-judge uses a strong LLM (GPT-4, Claude) to evaluate another LLM's output quality, replacing expensive human annotation at scale.

## Definition

LLM-as-judge uses a strong LLM (GPT-4, Claude) to evaluate another LLM's output quality, replacing expensive human annotation at scale.

**The core finding (Zheng et al., NeurIPS 2023)**:
GPT-4 as judge agrees with human raters >80% of the time — the same agreement rate found between two humans. This makes LLM-as-judge a statistically valid substitute for human evaluation at scale.

**When to use it**:
- Evaluating open-ended text quality (summaries, explanations, responses)
- Building continuous evaluation loops in production
- Creating golden datasets for RAG evaluation
- A/B testing prompt changes at scale
- NOT for: factual accuracy claims, safety-critical decisions, legal or medical output

**Implementation steps**:
1. Define evaluation rubric (1-5 scale, specific criteria per dimension)
2. Write judge prompt with chain-of-thought for consistency
3. Calibrate: run 100 samples with both LLM-judge and human (target: rho > 0.8)
4. If agreement < 80%, refine rubric or switch judge model
5. Integrate into CI/CD pipeline for continuous quality monitoring

**Known biases to mitigate**:
- Position bias: judges favor responses shown first — randomize order
- Verbosity bias: judges favor longer responses — normalize length in rubric
- Self-enhancement bias: a model judges its own outputs favorably — use a different judge model

**Integration points**:
- MLflow LLM Evaluate: built-in LLM-as-judge metrics
- RAGAS: faithfulness and relevance metrics use LLM-as-judge internally
- Braintrust, Arize: managed evaluation platforms with LLM-as-judge support

## Evidence

- **Tier 1 (entry-level)**: [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (NeurIPS 2023)](https://arxiv.org/abs/2306.05685)
- **Tier 1 (entry-level)**: [MLflow: LLM Evaluation](https://mlflow.org/docs/latest/llms/llm-evaluate/index.html)
- **Tier 1 (entry-level)**: [Anthropic: Constitutional AI — Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- **Tier 1 (entry-level)**: [Hands-On Large Language Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-252](../rius/RIU-252.md)
- [RIU-524](../rius/RIU-524.md)

## Handled By

- [Architect](../agents/architect.md)
- [Monitor](../agents/monitor.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-252](../paths/RIU-252-model-evaluation-selection.md) — hands-on exercise
- [RIU-524](../paths/RIU-524-llm-output-quality-monitoring.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-114.
Evidence tier: 1.
Journey stage: evaluation.
