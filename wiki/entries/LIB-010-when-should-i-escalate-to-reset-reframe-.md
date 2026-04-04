---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-010
source_hash: sha256:6b5cf2e69210ad58
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, convergence-failure, decision-framework, escalation, knowledge-entry, reset-criteria]
related: [RIU-001, RIU-002, RIU-003, RIU-006]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# When should I escalate to reset/reframe vs continue converging?

**RESET signals (stop and start over with fresh framing):**

## Definition

**RESET signals (stop and start over with fresh framing):**
      - No tangible results after agreed timeline (many AI projects abandoned for this)
      - Stakeholders still have conflicting definitions of success after 2-3 alignment attempts
      - No clear line of sight from AI feature to measurable business metric
      - Technical team owns strategy without cross-functional business involvement
      - Exit criteria thresholds (quality, latency, cost) consistently missed
      
      **REFRAME signals (change the problem statement, keep context):**
      - Original problem was actually 3 problems disguised as one (see LIB-007)
      - Production reached but scaling challenges emerge (load balancing, observability, optimization)
      - Value chain mapping reveals disconnect between feature and business impact
      - Constraints discovered that make original approach infeasible (see LIB-008)
      
      **CONTINUE CONVERGING when:**
      - Decisions are TWO-WAY DOORs (reversible, low-cost to change)
      - Governance frameworks in place (user profiles, data access, infrastructure templates)
      - Stakeholders aligned on success criteria, just iterating on solution
      - Progress measurable against agreed milestones
      
      **PALETTE guidance:** If convergence not reached within expected exchange window, propose Reset, Fork (try different approach), or Reframe. Silent looping is not allowed. Escalate to executive sponsor when reset involves ONE-WAY DOOR sunk costs. Document decision in decisions.md with rationale.

## Evidence

- **Tier 1 (entry-level)**: [Practical implementation considerations to close the AI value gap](https://aws.amazon.com/blogs/machine-learning/practical-implementation-considerations-to-close-the-ai-value-gap/)
- **Tier 1 (entry-level)**: [Organizational AI Vision - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_1_vision_and_strategy/5_1_1_organizational_ai_vision.html)
- **Tier 1 (entry-level)**: [Why agentic AI marks an inflection point for enterprise modernization](https://aws.amazon.com/blogs/aws-insights/aws-why-agentic-ai-marks-an-inflection-point-for-enterprise-modernization/)
- **Tier 1 (entry-level)**: [Generative AI operating models in enterprise organizations with Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/generative-ai-operating-models-in-enterprise-organizations-with-amazon-bedrock/)
- **Tier 1 (entry-level)**: [Databricks: AI Transformation Strategy Guide 2025](https://www.databricks.com/blog/ai-transformation-complete-strategy-guide-2025)
- **Tier 1 (entry-level)**: [Anthropic: Building Trusted AI in the Enterprise](https://assets.anthropic.com/m/66daaa23018ab0fd/original/Anthropic-enterprise-ebook-digital.pdf)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-002](../rius/RIU-002.md)
- [RIU-003](../rius/RIU-003.md)
- [RIU-006](../rius/RIU-006.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-010.
Evidence tier: 1.
Journey stage: all.
