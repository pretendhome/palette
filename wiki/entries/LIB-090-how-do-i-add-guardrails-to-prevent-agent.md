---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-090
source_hash: sha256:b1c3507f257b7737
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [knowledge-entry, orchestration]
related: [RIU-105]
handled_by: [narrator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I add guardrails to prevent agent misuse?

Guardrails are deterministic rules that constrain agent behavior 

## Definition

Guardrails are deterministic rules that constrain agent behavior 
outside the model's reasoning (defense-in-depth).

Two-layer approach:

Layer 1: Deterministic Guardrails (code-based)
- Hard limits on agent actions (e.g., no purchases >$100)
- Require human confirmation for irreversible actions (ONE-WAY DOOR)
- Block access to sensitive APIs without explicit approval
- Validate tool parameters before execution
- Enforce rate limits and resource quotas

Layer 2: Reasoning-Based Defenses (AI-powered)
- Use "LM as Judge" to screen inputs/outputs for policy violations
- Adversarial training to resist prompt injection
- Specialized guard models flag risky plans before execution
- Context-aware policy evaluation

Best practice: Combine both layers. Code provides predictable limits,
AI provides contextual awareness.

Example guardrail implementation:
Before agent sends email:
1. Check: Is recipient on approved list? (deterministic)
2. Check: Does content violate tone policy? (LM judge)
3. Check: Does email contain PII without consent? (deterministic + LM)
4. If any check fails: Block action, log attempt, alert human

Integration with Palette:
- Architect designs guardrail architecture (what to constrain)
- Builder implements guardrails (code + configuration)
- Validator validates guardrails work as intended
- Monitor monitors for guardrail violations in production


## Evidence

- **Tier 1 (entry-level)**: [Google Introduction to Agents (Nov 2025) - Security section](https://cloud.google.com/use-cases/agents)
- **Tier 1 (entry-level)**: [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **Tier 1 (entry-level)**: Palette Tier 2 - Agent Security section (`palette/.steering/assumptions.md#agent-security`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-105](../rius/RIU-105.md)

## Handled By

- [Narrator](../agents/narrator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-090.
Evidence tier: 1.
Journey stage: orchestration.
