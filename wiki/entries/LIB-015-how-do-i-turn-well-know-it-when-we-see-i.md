---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-015
source_hash: sha256:d5113900fd5e0b98
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [acceptance-criteria, evaluation, knowledge-entry, measurement, quality-definition, validation]
related: [RIU-001, RIU-006, RIU-021]
handled_by: [architect, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I turn 'we'll know it when we see it' into measurable acceptance criteria?

"We'll know it when we see it" signals subjective quality expectations. Use these techniques to make them measurable:

## Definition

"We'll know it when we see it" signals subjective quality expectations. Use these techniques to make them measurable:
      
      **Step 1: Extract concrete examples**
      - Ask: "Show me 3 examples of good output and 3 examples of bad output"
      - Ask: "What specifically makes this one good? What's missing from the bad one?"
      - Document these as your initial Golden Set (RIU-021)
      
      **Step 2: Apply the 4 evaluation frameworks**
      1. **LLM-as-a-Judge**: Use Amazon Bedrock Evaluations with custom metrics — define your own criteria alongside built-in metrics
      2. **Rubric-Based Evaluation**: Create scoring rubric (1-5 scale) with explicit criteria for each level
      3. **Traditional Metrics**: Where applicable, add objective measures (latency, cost, format compliance)
      4. **Domain-Specific**: Map to business outcomes (response time → resolution rate → customer satisfaction)
      
      **Step 3: Build measurable proxies**
      For each subjective criterion, identify 2-3 quantifiable proxies:
      - "Sounds professional" → No grammar errors + formal tone score (LLM-judge) + no slang detected
      - "Helpful response" → Contains action items + answers the question asked + user follow-up rate
      - "Accurate" → Factual claims verified against source + no hallucinated entities + citation coverage
      
      **Step 4: Validate with stakeholders**
      - Run evaluation on 50+ examples, show results
      - Ask: "Does a score of 4.2 on this rubric match what you'd call 'good enough'?"
      - Adjust thresholds until metrics align with human judgment (target ρ > 0.8 correlation)
      
      **PALETTE integration:**
      - Document criteria in Success Metrics Charter (RIU-006)
      - Store Golden Set in RIU-021 for regression testing
      - Define exit criteria: "Acceptance requires score ≥ X on rubric across Y% of test cases"
      
      Key insight: Evaluation is the single most important component for GenAI success — without it, you risk deploying models that fail silently.

## Evidence

- **Tier 1 (entry-level)**: [Model Evaluation and Selection Criteria Overview - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/2_0_technical_foundations_and_patterns/2_6_model_evaluation_and_selection_criteria/index.html)
- **Tier 1 (entry-level)**: [Evaluation Techniques - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/2_0_technical_foundations_and_patterns/2_6_model_evaluation_and_selection_criteria/2_6_3_evaluation_technique/2_6_3_evaluation_techniques.html)
- **Tier 1 (entry-level)**: [Use custom metrics to evaluate your generative AI application with Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/use-custom-metrics-to-evaluate-your-generative-ai-application-with-amazon-bedrock/)
- **Tier 1 (entry-level)**: [Beyond pilots: A proven framework for scaling AI to production](https://aws.amazon.com/blogs/machine-learning/beyond-pilots-a-proven-framework-for-scaling-ai-to-production/)
- **Tier 1 (entry-level)**: [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (NeurIPS 2023)](https://arxiv.org/abs/2306.05685)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-006](../rius/RIU-006.md)
- [RIU-021](../rius/RIU-021.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise
- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-015.
Evidence tier: 1.
Journey stage: evaluation.
