---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-017
source_hash: sha256:53db5401f807b705
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [experience, expertise-capture, implicit-knowledge, judgment-modeling, knowledge-entry, specialization]
related: [RIU-008, RIU-014, RIU-500]
handled_by: [architect, builder, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I capture human judgment that's based on years of experience, not explicit rules?

Experiential judgment is pattern recognition that experts can't articulate as rules. Capture it through examples, feedback loops, and calibration — not interviews alone.

## Definition

Experiential judgment is pattern recognition that experts can't articulate as rules. Capture it through examples, feedback loops, and calibration — not interviews alone.
      
      **Elicitation techniques:**
      - **Case-based extraction**: Present real scenarios and ask "What would you do? Why?" Record decisions, not just rules
      - **Contrastive pairs**: Show two similar cases with different outcomes — "Why did you handle these differently?"
      - **Think-aloud protocol**: Have expert narrate while working real cases (use voice capture with Transcribe + Bedrock)
      - **Calibration sessions**: Show AI outputs to expert, ask "Would you have done this?" — disagreements reveal tacit criteria
      
      **Learning architectures:**
      1. **Feedback Loop HITL**: Expert reviews AI outputs, corrections feed back into system
      2. **RLHF (Reinforcement Learning from Human Feedback)**: Fine-tune models using expert preferences on output pairs
      3. **RLAIF**: When expert time is limited, use AI-generated feedback (reduces SME workload ~80%)
      4. **Self-learning system**: Use disagreements between models as learning signals (Amazon Catalog pattern — supervisor model resolves conflicts, builds hierarchical knowledge base)
      
      **AWS tools:**
      - Amazon SageMaker Ground Truth Plus for preference datasets and demonstration data
      - Amazon Bedrock for fine-tuning with human feedback
      - Amazon Transcribe for voice-based knowledge capture
      
      **What CAN'T be captured:**
      - Judgment requiring real-time sensory input (smell, touch, visual nuance)
      - Decisions requiring context the system can't access
      - Novel situations outside training distribution
      - Flag these for permanent human-in-the-loop (Escalation-Based HITL pattern)
      
      **PALETTE integration:**
      - Store captured judgment patterns in Assumptions Register (RIU-008) as hypotheses to validate
      - Document expert disagreements — these reveal edge cases (RIU-014)
      - Flag judgment calls that are ONE-WAY DOORs (require human approval even after training)
      
      Key insight: Don't ask experts to explain rules — show them cases and capture their reactions. Judgment lives in the delta between what they do and what a naive system would do.

## Evidence

- **Tier 1 (entry-level)**: [Human-in-the-Loop for GenAI Systems - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_1_system_and_application_design_patterns_for_genai/3_1_1_foundation_architecture_components/3_1_1_8_additional_components/3_1_1_8_1_human_in_the_loop/3_1_1_8_1_human_in_the_loop.html)
- **Tier 1 (entry-level)**: [Fine Tuning with Reinforcement Learning from Human Feedback (RLHF)](https://awslabs.github.io/generative-ai-atlas/topics/2_0_technical_foundations_and_patterns/2_3_core_archtectural_concepts/2_3_4_fine-tuning/2_3_4-3_Preference Alignment/2_3_4_3_1_reinforcement_learning_from_human_feedback(RLHF)/rlhf.html)
- **Tier 1 (entry-level)**: [High-quality human feedback for your generative AI applications from Amazon SageMaker Ground Truth Plus](https://aws.amazon.com/blogs/machine-learning/high-quality-human-feedback-for-your-generative-ai-applications-from-amazon-sagemaker-ground-truth-plus/)
- **Tier 1 (entry-level)**: [How the Amazon.com Catalog Team built self-learning generative AI at scale](https://aws.amazon.com/blogs/machine-learning/how-the-amazon-com-catalog-team-built-self-learning-generative-ai-at-scale-with-amazon-bedrock/)
- **Tier 1 (entry-level)**: [Anthropic: Constitutional AI — Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- **Tier 1 (entry-level)**: [Google DeepMind: Learning through human feedback](https://deepmind.google/discover/blog/learning-through-human-feedback/)
- **Tier 1 (entry-level)**: [Lee et al., RLAIF vs. RLHF (arXiv 2309.00267)](https://arxiv.org/abs/2309.00267)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-008](../rius/RIU-008.md)
- [RIU-014](../rius/RIU-014.md)
- [RIU-500](../rius/RIU-500.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-017.
Evidence tier: 1.
Journey stage: specialization.
