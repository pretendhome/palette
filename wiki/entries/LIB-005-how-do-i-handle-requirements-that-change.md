---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-005
source_hash: sha256:658dd22f712b9300
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [agile-fde, all, change-management, knowledge-entry, scope-creep, stakeholder-alignment]
related: [RIU-001, RIU-002, RIU-008]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I handle requirements that change weekly in an enterprise AI deployment?

Distinguish between TWO-WAY DOOR changes (reversible — absorb quickly) and ONE-WAY DOOR changes (irreversible — require formal re-convergence via RIU-001). Implement a federated operating model: central oversight for data access, model risk, and compliance, while lines of business iterate autonomously within defined boundaries. Use the Assumptions Register (RIU-008) to track volatile requirements as testable assumptions with expiry dates rather than fixed specs. Apply AI-DLC methodology with structured prompts and mob elaboration to move from requirements to working prototypes in hours, enabling rapid validation before commitment. Map organizational debt and streamline approval processes that hinder adaptation. Redefine the Convergence Brief (RIU-001) as a living document — freeze ONE-WAY DOORs (architecture, data schema, compliance) while allowing TWO-WAY DOORs (prompts, UI, thresholds) to evolve weekly. Key insight: AI systems are nondeterministic, requiring new trust models where "requirements" become hypotheses validated through continuous experimentation rather than upfront specifications.

## Definition

Distinguish between TWO-WAY DOOR changes (reversible — absorb quickly) and ONE-WAY DOOR changes (irreversible — require formal re-convergence via RIU-001). Implement a federated operating model: central oversight for data access, model risk, and compliance, while lines of business iterate autonomously within defined boundaries. Use the Assumptions Register (RIU-008) to track volatile requirements as testable assumptions with expiry dates rather than fixed specs. Apply AI-DLC methodology with structured prompts and mob elaboration to move from requirements to working prototypes in hours, enabling rapid validation before commitment. Map organizational debt and streamline approval processes that hinder adaptation. Redefine the Convergence Brief (RIU-001) as a living document — freeze ONE-WAY DOORs (architecture, data schema, compliance) while allowing TWO-WAY DOORs (prompts, UI, thresholds) to evolve weekly. Key insight: AI systems are nondeterministic, requiring new trust models where "requirements" become hypotheses validated through continuous experimentation rather than upfront specifications.

## Evidence

- **Tier 1 (entry-level)**: [Generative AI operating models in enterprise organizations with Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/generative-ai-operating-models-in-enterprise-organizations-with-amazon-bedrock/)
- **Tier 1 (entry-level)**: [Beyond the technology: Workforce changes for AI](https://aws.amazon.com/blogs/machine-learning/beyond-the-technology-workforce-changes-for-ai/)
- **Tier 1 (entry-level)**: [Tech Talk: Seeing AI-DLC Work - How AI Transforms Enterprise Development](https://broadcast.amazon.com/videos/1702552)
- **Tier 1 (entry-level)**: [Why agentic AI marks an inflection point for enterprise modernization](https://aws.amazon.com/blogs/aws-insights/aws-why-agentic-ai-marks-an-inflection-point-for-enterprise-modernization/)
- **Tier 1 (entry-level)**: [AI and Digital Transformation](https://aws.amazon.com/blogs/enterprise-strategy/ai-and-digital-transformation/)
- **Tier 1 (entry-level)**: [Anthropic: Building Trusted AI in the Enterprise](https://assets.anthropic.com/m/66daaa23018ab0fd/original/Anthropic-enterprise-ebook-digital.pdf)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-002](../rius/RIU-002.md)
- [RIU-008](../rius/RIU-008.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-005.
Evidence tier: 1.
Journey stage: all.
