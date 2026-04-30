---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-167
source_hash: sha256:e0bacfb55871ce76
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [foundation, knowledge-entry, portfolio, prioritization, responsible-ai, use-case, wsjf]
related: [RIU-001, RIU-004, RIU-602]
handled_by: [architect, researcher]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I build an AI use case prioritization matrix that balances business impact, feasibility, and responsible AI considerations?

RIU-602 implements a structured prioritization framework. Phase 1 — Use Case Collection: gather candidate use cases from all departments/brands. For each, require: a one-sentence description, the business metric it impacts, the estimated annual value ($ or time saved), and the data availability status. Reject use cases without a clear business metric — "improve productivity" is not a metric; "reduce processing time from 4 hours to 30 minutes" is. Phase 2 — Multi-Dimensional Scoring: score each use case 1-10 on five dimensions. Business Impact: revenue lift, cost reduction, or risk mitigation in dollar terms. Feasibility: data exists, technical complexity is manageable, team has skills. Risk: brand safety, compliance exposure, customer impact if it fails. Strategic Alignment: fits organizational AI vision and brand strategy. Time to Value: months to measurable impact. Phase 3 — WSJF Sequencing: apply Weighted Shortest Job First. Priority = (Business Value + Time Criticality + Risk Reduction) / Job Size. This naturally surfaces quick wins and deprioritizes large, uncertain bets. Phase 4 — Responsible AI Assessment: before finalizing, assess each top-10 use case for: bias risk (does it affect different populations differently?), transparency requirement (do users need to know AI is involved?), and reversibility (can decisions be undone?). Use cases with high responsible AI risk may need to be deprioritized or scoped differently. Phase 5 — Red Flags: deprioritize use cases with no executive sponsor, no clear metric, data that does not exist yet, or ONE-WAY DOOR decisions without sufficient research.

## Definition

RIU-602 implements a structured prioritization framework. Phase 1 — Use Case Collection: gather candidate use cases from all departments/brands. For each, require: a one-sentence description, the business metric it impacts, the estimated annual value ($ or time saved), and the data availability status. Reject use cases without a clear business metric — "improve productivity" is not a metric; "reduce processing time from 4 hours to 30 minutes" is. Phase 2 — Multi-Dimensional Scoring: score each use case 1-10 on five dimensions. Business Impact: revenue lift, cost reduction, or risk mitigation in dollar terms. Feasibility: data exists, technical complexity is manageable, team has skills. Risk: brand safety, compliance exposure, customer impact if it fails. Strategic Alignment: fits organizational AI vision and brand strategy. Time to Value: months to measurable impact. Phase 3 — WSJF Sequencing: apply Weighted Shortest Job First. Priority = (Business Value + Time Criticality + Risk Reduction) / Job Size. This naturally surfaces quick wins and deprioritizes large, uncertain bets. Phase 4 — Responsible AI Assessment: before finalizing, assess each top-10 use case for: bias risk (does it affect different populations differently?), transparency requirement (do users need to know AI is involved?), and reversibility (can decisions be undone?). Use cases with high responsible AI risk may need to be deprioritized or scoped differently. Phase 5 — Red Flags: deprioritize use cases with no executive sponsor, no clear metric, data that does not exist yet, or ONE-WAY DOOR decisions without sufficient research.

## Evidence

- **Tier 1 (entry-level)**: [SAFe: WSJF — Weighted Shortest Job First](https://scaledagileframework.com/wsjf/)
- **Tier 1 (entry-level)**: [AWS: Incorporating Responsible AI into Generative AI Project Prioritization](https://aws.amazon.com/blogs/machine-learning/incorporating-responsible-ai-into-generative-ai-project-prioritization/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-004](../rius/RIU-004.md)
- [RIU-602](../rius/RIU-602.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-167.
Evidence tier: 1.
Journey stage: foundation.
