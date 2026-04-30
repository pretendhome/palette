---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-012
source_hash: sha256:28d819344157e97d
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, checkpoints, convergence-validation, knowledge-entry, phase-gates, quality-criteria]
related: [RIU-001, RIU-002, RIU-003, RIU-007, RIU-008]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the checklist for 'good enough' convergence before moving to architecture?

Use this checklist before proceeding from Convergence to Architecture phase. All items should be documented or explicitly marked "N/A with rationale."

## Definition

Use this checklist before proceeding from Convergence to Architecture phase. All items should be documented or explicitly marked "N/A with rationale."
      
      **Semantic Blueprint Complete (RIU-001):**
      - [ ] Goal: Measurable business outcome stated (not technical metric)
      - [ ] Roles: Decision authority clear (RACI-lite, RIU-002)
      - [ ] Capabilities: Required tools/agents identified
      - [ ] Constraints: Hard boundaries documented (budget, compliance, timeline)
      - [ ] Non-goals: Explicit exclusions prevent scope creep
      
      **Stakeholder Alignment:**
      - [ ] No conflicting definitions of success remain
      - [ ] Executive sponsor identified and committed
      - [ ] Non-technical stakeholders can explain the goal back to you
      - [ ] Sign-off obtained on Convergence Brief
      
      **Risk & Constraints Surfaced (RIU-007, RIU-008):**
      - [ ] ONE-WAY DOOR decisions identified and flagged (RIU-003)
      - [ ] Compliance requirements assessed (HIPAA, GDPR, EU AI Act)
      - [ ] Data governance framework confirmed (critical ONE-WAY DOOR)
      - [ ] Hidden constraints discovered (see LIB-008 questions)
      - [ ] Assumptions documented with validation plan
      
      **Technical Readiness:**
      - [ ] Proof of value demonstrated (PoC exit criteria met)
      - [ ] Data availability and quality confirmed
      - [ ] Proven architectural patterns identified (e.g., RAG vs. fine-tuning)
      - [ ] Unit economics estimated (cost per request, token usage)
      
      **AWS Phase Gate Alignment:**
      Per Gen AI Adoption framework: Use Case Discovery ✓ → Business Case with Success Criteria ✓ → Data/Model Foundation → Security/Compliance → Responsible AI → Development → Deployment
      
      **Gate criteria:** If any checkbox is incomplete and not "N/A with rationale," you haven't converged — return to discovery.

## Evidence

- **Tier 1 (entry-level)**: [Implementation Considerations and Challenges - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/1_0_generative_ai_fundamentals/1_3_implementation_consideration_and_challenges/1_3_implementation_consideration_and_challenges.html)
- **Tier 1 (entry-level)**: [AI Pitch Deck for Business Decision Makers](https://aws.highspot.com/items/632e4908931439bbe94f83c9#1)
- **Tier 1 (entry-level)**: [Bridging the Knowledge Gap: Using Generative AI on AWS to Preserve Critical Expertise](https://aws.amazon.com/blogs/industries/bridging-the-knowledge-gap-using-generative-ai-on-aws-to-preserve-critical-expertise/)
- **Tier 1 (entry-level)**: [Business Value and use cases - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/1_0_generative_ai_fundamentals/1_2_business_value_and_use_cases/1_2_business_value_and_use_cases.html)
- **Tier 1 (entry-level)**: [Google Cloud AI Adoption Framework](https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf)
- **Tier 1 (entry-level)**: [Databricks: GenAI Developer Workflow](https://docs.databricks.com/aws/en/generative-ai/tutorials/ai-cookbook/genai-developer-workflow)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-002](../rius/RIU-002.md)
- [RIU-003](../rius/RIU-003.md)
- [RIU-007](../rius/RIU-007.md)
- [RIU-008](../rius/RIU-008.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-012.
Evidence tier: 1.
Journey stage: all.
