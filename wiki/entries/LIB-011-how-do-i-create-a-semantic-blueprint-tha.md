---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-011
source_hash: sha256:10557793229e8929
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [accessibility, all, communication, documentation, knowledge-entry, stakeholder-validation]
related: [RIU-001, RIU-004, RIU-006]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I create a semantic blueprint that non-technical stakeholders can validate?

Translate the 5 Semantic Blueprint elements (RIU-001) into business language:

## Definition

Translate the 5 Semantic Blueprint elements (RIU-001) into business language:
      
      **Goal**: Use OGSM framework — state business outcome, not technical metric. Say "Reduce customer churn by 5%" not "Achieve 85% model accuracy." Avoid vague objectives like "improve productivity."
      
      **Roles**: Name people and departments, not systems. "Marketing owns data input; AI team owns model; Legal approves before launch" — skip technical architecture.
      
      **Capabilities**: Describe what the system *does for users*, not how it works. "Automatically flags high-risk accounts for review" not "Uses gradient boosting classifier."
      
      **Constraints**: Frame as business boundaries. "Must not access customer PII without consent; Budget capped at $50K; Must launch before Q3."
      
      **Non-goals**: Critical for scope control. Explicitly state "This will NOT replace human decision-making / integrate with System X / handle edge case Y."
      
      **Validation techniques:**
      - Use AIR workshop format with cross-functional team (business + technical)
      - Walk through each element verbally — if stakeholder can't explain it back, rewrite it
      - Provide visual assessment showing feasibility, budget, ROI, data quality, risks
      - Get explicit sign-off: "Do you agree this is what we're building and what success looks like?"
      
      **Format**: One page maximum. Use bullet points, not paragraphs. If it requires technical glossary, it's too complex.

## Evidence

- **Tier 1 (entry-level)**: [Organizational AI Vision - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_1_vision_and_strategy/5_1_1_organizational_ai_vision.html)
- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Custom Intelligence: Building AI that matches your business DNA](https://aws.amazon.com/blogs/machine-learning/custom-intelligence-building-ai-that-matches-your-business-dna/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-004](../rius/RIU-004.md)
- [RIU-006](../rius/RIU-006.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-011.
Evidence tier: 1.
Journey stage: all.
