---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-007
source_hash: sha256:a0ec10b57ca9c198
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, complexity-assessment, knowledge-entry, problem-decomposition, scope-analysis]
related: [RIU-001, RIU-002, RIU-004, RIU-005]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I identify when a customer request is actually 3 separate problems disguised as one?

**Warning signs of bundled problems:**

## Definition

**Warning signs of bundled problems:**
      - Vague objectives like "improve productivity" or "add AI" (no specific metric)
      - Different stakeholders define success differently for the same request
      - No clear line of sight from proposed feature to measurable business outcome
      - Request spans multiple data domains, teams, or systems
      - Cannot answer "how will we measure success?" with one metric
      
      **Decomposition technique:** Use RIU-004 (Problem → Workstream Decomposition) to generate broad candidate workstreams without committing. Apply the AIR Workshop methodology: score each potential use case (1-10) on business impact, cost, implementation complexity, business priority, and timeline. Plot on Eisenhower matrix to separate high-impact use cases from quick wins. Each decomposed problem must have its own line of sight to specific, quantifiable metrics (e.g., "reduce churn 5%" not "improve customer experience").
      
      **Validation test:** If a problem requires its own Convergence Brief (RIU-001) with distinct Goal, Constraints, and Stakeholders — it's a separate problem. Document in decisions.md and negotiate phased delivery (RIU-005) rather than one mega-project.

## Evidence

- **Tier 1 (entry-level)**: [AI Use Case Identification & Prioritization (AIR Workshop)](https://broadcast.amazon.com/videos/1811883)
- **Tier 1 (entry-level)**: [Organizational AI Vision - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_1_vision_and_strategy/5_1_1_organizational_ai_vision.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-002](../rius/RIU-002.md)
- [RIU-004](../rius/RIU-004.md)
- [RIU-005](../rius/RIU-005.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-007.
Evidence tier: 1.
Journey stage: all.
