---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-103
source_hash: sha256:28e40848b6dc17f6
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [evaluation, knowledge-entry]
related: [RIU-001, RIU-105]
handled_by: [architect, narrator, researcher]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I evaluate agent quality and performance?

Agent outputs are probabilistic, not deterministic. 

## Definition

Agent outputs are probabilistic, not deterministic. 
Traditional unit tests (output == expected) don't work.
Use multi-layered, artifact-focused evaluation instead.

Layer 1: Deterministic Checks (First Priority)
- Fixtures: Known inputs → expected outputs
- Unit tests: Component behavior validation
- Schema validation: Output structure correctness
- Constraint checks: Hard limits enforced (e.g., no PII in logs)
- Pass/fail: Binary, auditable, fast

Layer 2: LM-as-Judge (Second Layer, Produces Artifact)
- Use powerful model to assess agent output against rubric
- Rubric dimensions:
  * Correctness: Did it give the right answer?
  * Grounding: Is response factually accurate?
  * Instruction-following: Did it follow constraints?
  * Tone: Is communication appropriate?
- Output: Scored rubric JSON (artifact, not opinion)
- Run against golden dataset of prompts + ideal responses
- Threshold-based pass/fail (e.g., overall_score >= 0.85)

Layer 3: Business Metrics (Top-Down)
- Goal completion rate
- User satisfaction scores (thumbs up/down)
- Task latency
- Cost per interaction
- Impact on revenue/conversion/retention

Layer 4: Human Feedback (Ground Truth)
- Collect bug reports, edge cases, thumbs down
- Aggregate feedback to identify patterns
- Convert feedback into new test cases (close the loop)
- Use RLHF when appropriate (advanced)

Metrics-Driven Development:
1. Establish baseline scores for production agent
2. Test new versions against full evaluation dataset
3. Compare scores: new version vs production
4. Go/no-go decision based on metrics, not intuition
5. Use A/B deployments for gradual rollout

Creating Golden Datasets:
- Sample scenarios from production interactions
- Cover full breadth of use cases + edge cases
- Include ideal responses (validated by domain experts)
- Maintain and expand dataset over time
- Store as artifacts (JSON, YAML, CSV)

Palette Integration:
- Validator performs validation using these methods
- Deterministic checks first, LM-as-Judge second
- All evaluations produce artifacts (JSON rubrics, test reports)
- Agent impressions track success/fail over time
- Maturity model (UNVALIDATED → WORKING → PRODUCTION) 
  based on measured performance (not opinions)

Example validation workflow:
1. Builder builds feature
2. Validator runs deterministic checks (fixtures pass?)
3. Validator runs LM-as-Judge (rubric scores >= threshold?)
4. Validator produces evaluation artifact (JSON report)
5. Human reviews artifact, approves or requests changes
6. If approved: increment agent success impressions
7. If failed: increment fail, reset fail_gap, route to Debugger

Anti-pattern: Don't use LM-as-Judge as a black box.
Always produce scored rubrics as artifacts for human review.


## Evidence

- **Tier 1 (entry-level)**: [Google Introduction to Agents (Nov 2025) - AgentOps section](https://cloud.google.com/use-cases/agents)
- **Tier 1 (entry-level)**: [Agentic System Design book (referenced in Google doc)](https://www.oreilly.com/library/view/agentic-system-design/9781098156909/)
- **Tier 1 (entry-level)**: Palette Tier 2 - Agent Maturity & Trust Model (`palette/.steering/assumptions.md#agent-maturity`)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-105](../rius/RIU-105.md)

## Handled By

- [Architect](../agents/architect.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-103.
Evidence tier: 1.
Journey stage: evaluation.
