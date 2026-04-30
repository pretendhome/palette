---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-098
source_hash: sha256:03528194dc79ab51
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [agentic, all, knowledge-entry, platform, tco, tool-sprawl]
related: [RIU-510, RIU-601, RIU-604]
handled_by: [architect, orchestrator, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I prevent AI tool sprawl in an enterprise and make the case for one agentic interface instead of 100 tools?

The Problem: Enterprises buy AI tools reactively. Each team gets its own.

## Definition

The Problem: Enterprises buy AI tools reactively. Each team gets its own.
Result: 50-100 tools, $2-5M/year in licenses, each requiring training,
integration, maintenance. Nobody knows which tool to use for what.

The Alternative: One agentic interface with core capabilities:
- Research (find information, gather context)
- Architecture (design solutions, evaluate tradeoffs)
- Build (implement within scope)
- Validate (quality check, compliance)
- Monitor (observe, detect drift)

TCO Comparison:
Tool Sprawl (100 tools): $2-5M/year licenses, 100 training programs,
100 integrations, fragmented knowledge, manual improvement per tool.
Agentic Platform (1 system): $500K-1M/year, 1 interface with role-based
recipes, 1 platform with modular capabilities, unified knowledge base,
auto-improves with usage.

Budget Trajectory:
- Year 1: Platform investment (higher)
- Year 2: Platform + reduced tools (neutral)
- Year 3: Platform only, tools eliminated (30-40% lower)

PALETTE integration: RIU-604 models the TCO comparison.
RIU-510 designs the agentic platform architecture.


## Evidence

- **Tier 1 (entry-level)**: [Why agentic AI marks an inflection point for enterprise modernization](https://aws.amazon.com/blogs/aws-insights/aws-why-agentic-ai-marks-an-inflection-point-for-enterprise-modernization/)
- **Tier 1 (entry-level)**: [Databricks: AI Transformation Strategy Guide 2025](https://www.databricks.com/blog/ai-transformation-complete-strategy-guide-2025)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-510](../rius/RIU-510.md)
- [RIU-601](../rius/RIU-601.md)
- [RIU-604](../rius/RIU-604.md)

## Handled By

- [Architect](../agents/architect.md)
- [Orchestrator](../agents/orchestrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-510](../paths/RIU-510-multi-agent-workflow-design.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-098.
Evidence tier: 1.
Journey stage: all.
