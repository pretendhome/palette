---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-009
source_hash: sha256:ffd7c6e1b3fcdb04
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, documentation, interviews, knowledge-capture, knowledge-entry, tacit-knowledge]
related: [RIU-001, RIU-003, RIU-004, RIU-008, RIU-014]
handled_by: [architect, builder, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I document tribal knowledge that exists only in stakeholder heads?

**Elicitation techniques:**

## Definition

**Elicitation techniques:**
      - Use voice-based capture (Amazon Transcribe + Bedrock) — reduces cognitive load and captures natural explanations better than asking SMEs to write documentation
      - Ask scenario-based questions: "Walk me through what you do when X happens" rather than "What are the rules for X?"
      - Probe "it depends" answers: "What specifically does it depend on? Give me the last 3 examples"
      - Shadow SMEs during real work to capture decision-making in context
      - Use "teach-back" validation: document your understanding and have SME correct it
      
      **4-step capture workflow:**
      1. **Capture**: Record conversations with experienced workers (voice preferred)
      2. **Transcribe**: Convert to structured text using Amazon Transcribe
      3. **Structure**: Use Bedrock to extract decision trees, rules, and edge cases
      4. **Validate**: Review with SME to confirm accuracy before finalizing
      
      **PALETTE integration:**
      - Store validated rules in Assumptions Register (RIU-008) with testable conditions
      - Document decision logic in Decision Log (RIU-003) for future reference
      - Feed into Edge-Case Catalog (RIU-014) for testing
      - Flag assumptions that are ONE-WAY DOORs if they drive architecture decisions
      
      Critical: Capture *why* decisions are made, not just *what* — the reasoning is often more valuable than the rule itself.

## Evidence

- **Tier 1 (entry-level)**: [Unlock organizational wisdom using voice-driven knowledge capture with Amazon Transcribe and Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/unlock-organizational-wisdom-using-voice-driven-knowledge-capture-with-amazon-transcribe-and-amazon-bedrock/)
- **Tier 1 (entry-level)**: [Bridging the Knowledge Gap: Using Generative AI on AWS to Preserve Critical Expertise](https://aws.amazon.com/blogs/industries/bridging-the-knowledge-gap-using-generative-ai-on-aws-to-preserve-critical-expertise/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-003](../rius/RIU-003.md)
- [RIU-004](../rius/RIU-004.md)
- [RIU-008](../rius/RIU-008.md)
- [RIU-014](../rius/RIU-014.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-009.
Evidence tier: 1.
Journey stage: all.
