---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-095
source_hash: sha256:1aa44959d405499c
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, convergence, knowledge-entry, planning, requirements, semantic-blueprint]
related: [RIU-001, RIU-002]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What are the required elements of a Semantic Blueprint (Convergence Brief)?

Per Palette Tier 1, every engagement MUST produce a Semantic Blueprint with these five elements:

## Definition

Per Palette Tier 1, every engagement MUST produce a Semantic Blueprint with these five elements:

**1. Goal** (What success looks like - concrete, measurable):
- Must be measurable: "Reduce churn 5%" not "Improve experience"
- Must be concrete: "80% accuracy on 50 test cases" not "Good performance"
- Must be business outcome: "Launch before Q3" not "Build feature X"
- Examples: "Reduce ML inference latency to <200ms at p95", "Process 10K transactions/sec with <0.1% error rate", "Deploy compliant HIPAA solution by Q2"

**2. Roles** (Who/what is responsible - human vs agent boundaries):
- Decision authority: Who makes final calls?
- Execution responsibility: Who builds what?
- Review authority: Who validates?
- Examples: "FDE designs architecture, Kiro implements, customer validates", "Data scientist owns model, MLOps owns deployment, compliance owns audit"

**3. Capabilities** (What tools/agents are needed):
- Required agents: Researcher for research, Architect for architecture, Builder for building
- Required tools: web_search, fs_write, execute_bash, use_aws
- Required infrastructure: Cloud services, databases, APIs, frameworks
- Examples: "Need Researcher (research), Architect (architecture), AWS CDK, PostgreSQL", "Need web_search, SageMaker, Lambda, DynamoDB"

**4. Constraints** (What cannot be changed - technical, policy, timeline):
- Hard boundaries: Budget cap, compliance requirements, timeline
- Technical limits: Team size, existing infrastructure, data restrictions
- Policy limits: Security requirements, regulatory compliance
- Examples: "3-person team, $5K/month budget, 8-week timeline, must use existing VPC", "HIPAA compliance required, no PII in logs, SOC 2 audit in 6 months"

**5. Non-goals** (What is explicitly out of scope):
- Critical for preventing scope creep
- Must be explicit to prevent expansion
- Examples: "NOT building mobile apps, NOT supporting real-time streaming, NOT migrating legacy systems", "NOT implementing custom ML models, NOT building admin UI, NOT handling multi-region"

**Why this matters**:
- Forces clarity before execution
- Prevents scope creep
- Enables restartability (new person can read and continue)
- Provides decision framework for ONE-WAY DOOR calls

**Implementation**: The Convergence Brief (RIU-001) serves as the semantic blueprint. Must be documented in decisions.md before execution begins.

**Validation test**: If you can't fill all 5 elements, you haven't converged yet.


## Evidence

- **Tier 3 (entry-level)**: Palette Tier 1 - Semantic Blueprint (`palette/.steering/palette-core.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-002](../rius/RIU-002.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-095.
Evidence tier: 3.
Journey stage: all.
