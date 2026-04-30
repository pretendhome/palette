---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-037
source_hash: sha256:01e99989f8738769
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [evaluation, knowledge-entry, metrics, performance-prediction, validation]
related: [RIU-021, RIU-063, RIU-082, RIU-083, RIU-540]
handled_by: [architect, builder, monitor, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What evaluation metrics actually predict production AI performance?

Most offline metrics don't predict production success. Focus on metrics that correlate with business outcomes and user satisfaction, not just technical accuracy.

## Definition

Most offline metrics don't predict production success. Focus on metrics that correlate with business outcomes and user satisfaction, not just technical accuracy.
      
      **The metric hierarchy (predictive power):**
      
      | Metric Type | Predicts Production Success? | Why |
      |-------------|------------------------------|-----|
      | Business outcome metrics | ✅ High | Directly measures what matters |
      | User satisfaction proxies | ✅ High | Correlates with adoption |
      | Task completion rate | ✅ Medium-High | Measures real utility |
      | Domain-specific quality | ✅ Medium | Captures use-case fit |
      | Generic accuracy benchmarks | ⚠️ Low | May not reflect your data/use case |
      | Perplexity/loss | ❌ Very Low | Technical, not business-relevant |
      
      **Three-dimensional evaluation framework:**
      
      **1. Behavior metrics (does it work correctly?)**
      - **Correctness**: Factual accuracy, verifiable claims
      - **Completeness**: Answers the full question
      - **Faithfulness**: Grounded in provided context (RAG)
      - **Coherence**: Logical, well-structured responses
      - **Safety**: Toxicity, bias, harmful content detection
      - **Brand voice**: Tone and style alignment
      
      **2. Cost metrics (is it economically viable?)**
      - Cost per request (tokens + compute)
      - Cost per successful task completion
      - Token efficiency (output quality per token)
      - Infrastructure cost at projected scale
      
      **3. Speed metrics (is it fast enough?)**
      - Time to first token (TTFT)
      - End-to-end latency (p50, p95, p99)
      - Throughput at peak load
      
      **Metrics by application type:**
      
      | Application | Priority Metrics |
      |-------------|------------------|
      | RAG/Q&A | Context relevance, correctness, faithfulness, citation accuracy |
      | Healthcare | Correctness, completeness, helpfulness, logical coherence |
      | Customer support | Resolution rate, escalation rate, CSAT correlation |
      | Content generation | Brand voice, originality, factual accuracy |
      | Classification | Precision, recall, F1 (but validate on production distribution) |
      | Agents | Task completion rate, tool use accuracy, error recovery |
      
      **Metrics that actually predict production success:**
      
      1. **Task completion rate on realistic scenarios**
         - Not synthetic benchmarks — real user intents
         - Include edge cases from production logs
      
      2. **Human preference alignment**
         - Win rate vs. baseline in blind comparisons
         - Correlation coefficient with human ratings (target: ρ > 0.8)
      
      3. **Error rate on high-stakes decisions**
         - Where mistakes have real consequences
         - False positive/negative rates for your use case
      
      4. **Latency under production-like load**
         - Not just average — p99 matters for user experience
      
      5. **Cost per successful outcome**
         - Not cost per request — cost per value delivered
      
      **Validating offline metrics predict production:**
      ```
      1. Deploy to shadow/canary environment
      2. Collect production inputs, run through new model
      3. Compare offline evaluation scores to:
         - User feedback (thumbs up/down, escalations)
         - Task completion rates
         - Business metrics (conversion, resolution)
      4. Calculate correlation — if low, your offline metrics are wrong
      ```
      
      **AWS implementation:**
      - **Amazon Bedrock Evaluations**: Programmatic + model-as-judge
      - **Custom metrics**: Define business-specific criteria
      - **Automated pipelines**: Amazon Nova for continuous evaluation
      - **CloudWatch**: Cost and latency monitoring
      
      **Red flags your metrics don't predict production:**
      - High offline scores but poor user feedback
      - Model "wins" on benchmarks but users prefer old system
      - Metrics improve but business KPIs don't move
      - Different ranking on test set vs. production sample
      
      **PALETTE integration:**
      - Define metrics in RIU-083 (Evaluation Metric Selection)
      - Track in RIU-063 (Performance Baselines)
      - Validate with RIU-021 (Golden Set + Offline Evaluation)
      - Monitor production correlation in RIU-540 (Evaluation Harness)
      
      Key insight: The best metric is the one that, when it improves offline, business outcomes improve in production. If you don't know this correlation, you're optimizing blind.

## Evidence

- **Tier 1 (entry-level)**: [Going beyond vibes: Evaluating your Amazon Bedrock workloads for production](https://aws.amazon.com/blogs/publicsector/going-beyond-vibes-evaluating-your-amazon-bedrock-workloads-for-production/)
- **Tier 1 (entry-level)**: [Use custom metrics to evaluate your generative AI application with Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/use-custom-metrics-to-evaluate-your-generative-ai-application-with-amazon-bedrock/)
- **Tier 1 (entry-level)**: [Evaluate healthcare generative AI applications using LLM-as-a-judge on AWS](https://aws.amazon.com/blogs/machine-learning/evaluate-healthcare-generative-ai-applications-using-llm-as-a-judge-on-aws/)
- **Tier 1 (entry-level)**: [Build an automated generative AI solution evaluation pipeline with Amazon Nova](https://aws.amazon.com/blogs/machine-learning/build-an-automated-generative-ai-solution-evaluation-pipeline-with-amazon-nova/)
- **Tier 1 (entry-level)**: [MLflow: LLM Evaluation](https://mlflow.org/docs/latest/llms/llm-evaluate/index.html)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-063](../rius/RIU-063.md)
- [RIU-082](../rius/RIU-082.md)
- [RIU-083](../rius/RIU-083.md)
- [RIU-540](../rius/RIU-540.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise
- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-037.
Evidence tier: 1.
Journey stage: evaluation.
