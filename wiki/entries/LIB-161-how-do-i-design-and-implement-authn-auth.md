---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-161
source_hash: sha256:46ba835edaea0749
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [agent-identity, authentication, authorization, delegated-access, knowledge-entry, orchestration, security]
related: [RIU-010, RIU-029, RIU-322, RIU-327]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design and implement AuthN/AuthZ for AI agent systems where agents act on behalf of users?

RIU-327 addresses the unique AuthN/AuthZ challenges of agentic AI systems. Challenge 1 — Agent Identity: every agent must have a distinct identity (service principal, IAM role, or managed identity) separate from the user it serves. This enables audit trails that distinguish "User A requested action X" from "Agent B executed action X on behalf of User A." Never share credentials between agents. Challenge 2 — Delegated Authorization: use OAuth 2.0 token exchange (RFC 8693) to create delegated tokens where the agent acts with a subset of the user's permissions. The agent should never have broader permissions than the user. Implement scope narrowing: if the user has read-write access, the agent may only need read access for its current task. Challenge 3 — Least Privilege Per Task: agent permissions should be task-scoped, not session-scoped. When an agent performs a tool call, it should request only the permissions needed for that specific call. Use just-in-time access provisioning where possible. Challenge 4 — Audit Requirements: log every authentication event (agent login, token refresh, token exchange) and every authorization decision (access granted, access denied, scope narrowed). These logs must be tamper-proof and retained per compliance requirements. Cross-reference with RIU-029 (Tool-Calling Safety Envelope) for the tool-level permission model. Common failure: agents with long-lived, broad-scope tokens that persist across sessions. Implement token lifetime limits and automatic revocation when the user session ends.

## Definition

RIU-327 addresses the unique AuthN/AuthZ challenges of agentic AI systems. Challenge 1 — Agent Identity: every agent must have a distinct identity (service principal, IAM role, or managed identity) separate from the user it serves. This enables audit trails that distinguish "User A requested action X" from "Agent B executed action X on behalf of User A." Never share credentials between agents. Challenge 2 — Delegated Authorization: use OAuth 2.0 token exchange (RFC 8693) to create delegated tokens where the agent acts with a subset of the user's permissions. The agent should never have broader permissions than the user. Implement scope narrowing: if the user has read-write access, the agent may only need read access for its current task. Challenge 3 — Least Privilege Per Task: agent permissions should be task-scoped, not session-scoped. When an agent performs a tool call, it should request only the permissions needed for that specific call. Use just-in-time access provisioning where possible. Challenge 4 — Audit Requirements: log every authentication event (agent login, token refresh, token exchange) and every authorization decision (access granted, access denied, scope narrowed). These logs must be tamper-proof and retained per compliance requirements. Cross-reference with RIU-029 (Tool-Calling Safety Envelope) for the tool-level permission model. Common failure: agents with long-lived, broad-scope tokens that persist across sessions. Implement token lifetime limits and automatic revocation when the user session ends.

## Evidence

- **Tier 1 (entry-level)**: [RFC 8693: OAuth 2.0 Token Exchange](https://datatracker.ietf.org/doc/html/rfc8693)
- **Tier 1 (entry-level)**: [Anthropic: Building Effective Agents — Security Considerations](https://docs.anthropic.com/en/docs/build-with-claude/agent-patterns)
- **Tier 1 (entry-level)**: [NIST SP 800-63: Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-010](../rius/RIU-010.md)
- [RIU-029](../rius/RIU-029.md)
- [RIU-322](../rius/RIU-322.md)
- [RIU-327](../rius/RIU-327.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-161.
Evidence tier: 1.
Journey stage: orchestration.
