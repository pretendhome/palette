---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-138
source_hash: sha256:c1ac0d9b7b6d8111
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [agent, blast-radius, guardrails, knowledge-entry, orchestration, safety, tool-calling]
related: [RIU-012, RIU-029, RIU-087]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design a tool-calling safety envelope for AI agents that limits blast radius while preserving utility?

RIU-029 defines four safety layers for agent tool calling. Layer 1 — Tool Allowlist: enumerate every tool the agent can call. Each tool entry includes: name, description, parameter schema, rate limit (calls per minute), cost ceiling (per call and per session), and data classification (what sensitivity level of data the tool can access). Any tool not on the allowlist is denied by default. Layer 2 — Parameter Validation: before executing a tool call, validate parameters against the schema. Reject calls with unexpected parameters, out-of-range values, or injection patterns (e.g., SQL injection in a database query tool). Layer 3 — Redaction: apply output redaction rules to tool responses before returning them to the agent. PII, credentials, and internal system details must be redacted from tool outputs. Cross-reference with RIU-012 (PII/Compliance Triage). Layer 4 — Audit Trail: log every tool call with timestamp, agent_id, tool_name, parameters (redacted), response_code, and latency. This audit trail is required for compliance and debugging. Anthropic's guidance on building effective agents emphasizes that tool calls are the highest-risk surface area in agentic systems. The safety envelope must be a ONE-WAY DOOR decision: once defined, it should only be relaxed through a formal review process (RIU-087). Rate limits prevent runaway costs; cost ceilings prevent individual expensive operations; the allowlist prevents capability creep.

## Definition

RIU-029 defines four safety layers for agent tool calling. Layer 1 — Tool Allowlist: enumerate every tool the agent can call. Each tool entry includes: name, description, parameter schema, rate limit (calls per minute), cost ceiling (per call and per session), and data classification (what sensitivity level of data the tool can access). Any tool not on the allowlist is denied by default. Layer 2 — Parameter Validation: before executing a tool call, validate parameters against the schema. Reject calls with unexpected parameters, out-of-range values, or injection patterns (e.g., SQL injection in a database query tool). Layer 3 — Redaction: apply output redaction rules to tool responses before returning them to the agent. PII, credentials, and internal system details must be redacted from tool outputs. Cross-reference with RIU-012 (PII/Compliance Triage). Layer 4 — Audit Trail: log every tool call with timestamp, agent_id, tool_name, parameters (redacted), response_code, and latency. This audit trail is required for compliance and debugging. Anthropic's guidance on building effective agents emphasizes that tool calls are the highest-risk surface area in agentic systems. The safety envelope must be a ONE-WAY DOOR decision: once defined, it should only be relaxed through a formal review process (RIU-087). Rate limits prevent runaway costs; cost ceilings prevent individual expensive operations; the allowlist prevents capability creep.

## Evidence

- **Tier 1 (entry-level)**: [Anthropic: Building Effective Agents](https://docs.anthropic.com/en/docs/build-with-claude/agent-patterns)
- **Tier 1 (entry-level)**: [OWASP: LLM Top 10 — Insecure Plugin Design](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **Tier 1 (entry-level)**: [NIST AI RMF: AI Risk Management Framework](https://www.nist.gov/artificial-intelligence/ai-risk-management-framework)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-012](../rius/RIU-012.md)
- [RIU-029](../rius/RIU-029.md)
- [RIU-087](../rius/RIU-087.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-138.
Evidence tier: 1.
Journey stage: orchestration.
