---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-016
source_hash: sha256:5eec7159dac1047c
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [compliance, foundation, knowledge-entry, llm-behavior, policy-translation, prompt-engineering]
related: [RIU-007, RIU-022, RIU-500, RIU-501, RIU-520]
handled_by: [architect, builder, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What prompt engineering patterns work for translating policy documents into LLM behavior?

Use a layered approach combining prompt structure, guardrails, and validation:

## Definition

Use a layered approach combining prompt structure, guardrails, and validation:
      
      **Prompt structure for policies:**
      - **System prompt**: Set role and global constraints ("You are a compliance assistant. Never provide advice that violates [Policy X].")
      - **Context section**: Include relevant policy excerpts (use RAG for large policy corpora)
      - **Instruction**: Specific task with policy reference ("Answer the user's question following Section 3.2 guidelines")
      - **Constraints**: Explicit prohibitions ("Do NOT discuss [prohibited topics]. If asked, respond with [approved deflection].")
      - **Examples**: Few-shot samples showing compliant vs. non-compliant responses
      
      **Parameter settings for compliance:**
      - Temperature: 0.0-0.3 (prioritize consistency over creativity)
      - Top_p: 0.5-0.7 (restrict output variance)
      - Use deterministic settings for policy-critical responses
      
      **Guardrails layer (Amazon Bedrock Guardrails):**
      - Content filters for harmful/inappropriate content
      - Denied topics aligned with policy prohibitions
      - Word filters for restricted terminology
      - Sensitive information filters (PII/PHI detection and masking)
      - IAM policy-based enforcement for mandatory guardrails on every inference call
      
      **Validation approach:**
      - **Positive testing**: Legitimate policy-compliant queries pass correctly
      - **Negative testing**: Prohibited content/topics are blocked
      - Test edge cases where policies conflict or are ambiguous
      - Version control prompts (RIU-520) for audit trail and controlled updates
      
      **PALETTE integration:**
      - Document policy-to-prompt mapping in RIU-022 (Prompt Interface Contract)
      - Store prompt versions in RIU-520 (Prompt Version Control)
      - Define guardrail requirements in Constraint Profile (RIU-007)
      - Flag policy interpretations that are ONE-WAY DOORs (require legal/compliance sign-off)
      
      Key insight: Prompts alone aren't sufficient — use Bedrock Guardrails as a defense-in-depth layer that enforces policies even if prompts are bypassed or jailbroken.

## Evidence

- **Tier 1 (entry-level)**: [The Input Interface - Prompts and common LLM Parameters](https://awslabs.github.io/generative-ai-atlas/topics/2_0_technical_foundations_and_patterns/2_1_key_primitives/2_1_1_prompt/2_1_1_prompt.html)
- **Tier 1 (entry-level)**: [Implement model-independent safety measures with Amazon Bedrock Guardrails](https://aws.amazon.com/blogs/machine-learning/implement-model-independent-safety-measures-with-amazon-bedrock-guardrails/)
- **Tier 1 (entry-level)**: [Amazon Bedrock Guardrails announces IAM Policy-based enforcement](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-guardrails-announces-iam-policy-based-enforcement-to-deliver-safe-ai-interactions/)
- **Tier 1 (entry-level)**: [Risk and Compliance Management for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_3_risk_and_compliance_mngmt.html)
- **Tier 1 (entry-level)**: [Anthropic: Constitutional AI — Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- **Tier 1 (entry-level)**: [Generative AI on AWS](https://www.oreilly.com/library/view/generative-ai-on/9781098159214/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-007](../rius/RIU-007.md)
- [RIU-022](../rius/RIU-022.md)
- [RIU-500](../rius/RIU-500.md)
- [RIU-501](../rius/RIU-501.md)
- [RIU-520](../rius/RIU-520.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-022](../paths/RIU-022-prompt-interface-contract.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-016.
Evidence tier: 1.
Journey stage: foundation.
