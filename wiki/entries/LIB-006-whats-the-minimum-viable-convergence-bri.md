---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-006
source_hash: sha256:cec3a96007358ad8
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, knowledge-entry, lightweight-process, mvp, poc, rapid-delivery]
related: [RIU-001, RIU-003]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the minimum viable convergence brief for a 2-week AI proof of concept?

Even a 2-week PoC requires all five Semantic Blueprint elements (RIU-001), but scoped minimally:

## Definition

Even a 2-week PoC requires all five Semantic Blueprint elements (RIU-001), but scoped minimally:
      
      **Goal**: One measurable outcome (e.g., "80% accuracy on 50 test cases" or "< 3s latency at < $0.02/request").
      **Roles**: One human sponsor + one technical lead — skip full RACI.
      **Capabilities**: Single AI capability being validated (e.g., "Document classification via Bedrock Claude").
      **Constraints**: Hard boundaries — budget cap, data restrictions, no production deployment, token limits.
      **Non-goals**: 2-3 explicit exclusions to prevent scope creep.
      
      Per AWS guidance, add **exit criteria** with specific thresholds for quality, latency, and cost — know when to pivot or stop. Validate only core components before full integration to isolate failure points. Track unit economics early (per-request cost, token usage, compute). Document ethical AI considerations even for short pilots. Use ONE-WAY DOOR check: if PoC requires irreversible decisions (data grants, vendor commits), get sign-off first. Brief should fit one page — if not, you're overscoping.

## Evidence

- **Tier 1 (entry-level)**: [Beyond pilots: A proven framework for scaling AI to production](https://aws.amazon.com/blogs/machine-learning/beyond-pilots-a-proven-framework-for-scaling-ai-to-production/)
- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [AI/ML Organizational Adoption Framework](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/index.html)
- **Tier 1 (entry-level)**: [Databricks: GenAI Developer Workflow](https://docs.databricks.com/aws/en/generative-ai/tutorials/ai-cookbook/genai-developer-workflow)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-003](../rius/RIU-003.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-006.
Evidence tier: 1.
Journey stage: all.
