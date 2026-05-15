---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-191
source_hash: sha256:ddfabdd3b9aa302c
compiled_at: 2026-05-15T15:33:55Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 2
tags: [agent-communication, bus, knowledge-entry, orchestration, token-efficiency, wire-contracts]
related: [RIU-062, RIU-513]
handled_by: [architect, builder, debugger]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What are wire contracts and how do they prevent lossy handoffs between agents?

Wire contracts are the fixed envelope schema that defines exactly what data flows between agents on the peers bus. Every message must conform to the schema — malformed envelopes are rejected.

## Definition

Wire contracts are the fixed envelope schema that defines exactly what data flows between agents on the peers bus. Every message must conform to the schema — malformed envelopes are rejected.

**Required fields**: protocol_version, message_id (UUID), from_agent, to_agent, message_type (from enum: informational/advisory/proposal/execution_request/one_way_door/ack/ human_checkpoint), intent, risk_level (from enum: none/low/medium/high/critical), requires_ack (boolean), payload (object), created_at (ISO timestamp).

**Why wire contracts matter**: Without them, agent-to-agent communication is a 'game of telephone' — one agent summarizes for another, detail gets lost, fidelity degrades through the chain. Wire contracts prevent this by enforcing structured data at every handoff.

**Validation**: The broker's validate.mjs (58 lines) checks every envelope before delivery. Critical risk requires one_way_door message_type. Execution requests require a handoff_packet with id/from/to/task fields.

**Token efficiency**: Unlike MCP which forces token-heavy tool descriptions and discovery, wire contracts are a fixed schema. The agent knows exactly what it receives and produces. Zero discovery overhead.

**Conference validation**: Three sessions at AI Council 2026 confirmed this approach — 'MCP forces a lot of token usage. CLIs are better.' (Redis S13), 'Game of telephone — detail lost between agents' (Linus Lee S02).

## Evidence

- **Tier 2 (entry-level)**: Palette Bus Envelope Validation (`peers/broker/validate.mjs`)
- **Tier 2 (entry-level)**: [Redis Session — 'MCP forces a lot of token usage. CLIs are better.'](https://aicouncil.com)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-062](../rius/RIU-062.md)
- [RIU-513](../rius/RIU-513.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-191.
Evidence tier: 2.
Journey stage: orchestration.
