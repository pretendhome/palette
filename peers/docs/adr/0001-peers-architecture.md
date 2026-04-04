# ADR-0001: Palette Peers Architecture

**Status**: ACCEPTED
**Date**: 2026-03-23
**Decision**: 🚨 ONE-WAY DOOR — foundational architecture for multi-agent communication
**Decided by**: the operator (human), with Kiro (proposer)

---

## Context

Palette operates with four AI agents across three CLI tools and one API service:

| Agent | Runtime | Interface |
|-------|---------|-----------|
| Kiro | kiro-cli | MCP servers (stdio) |
| Claude Code | claude | MCP servers (stdio) + channels |
| Codex | codex | tools + sandbox |
| Perplexity | API | HTTP (Sonar API via researcher.py) |

Today, coordination between agents requires the human to copy-paste context between terminals. The relay model (Codex designs → Kiro builds → Claude Code finishes) works but is manually orchestrated.

The [claude-peers-mcp](https://github.com/louislva/claude-peers-mcp) project proves that peer-to-peer messaging between AI agent instances is viable using a local broker + MCP. However, it is Claude-only, unstructured, and ungoverned.

## Decision

Build **Palette Peers**: a governed local message bus for multi-agent coordination.

### Design Principles

1. **Transport is shared, execution is isolated** — One broker, one protocol, four adapters with different affordances. No agent can execute on behalf of another.
2. **Structured envelopes, not free chat** — Every message has identity, intent, risk classification, and reply threading.
3. **Broker and governance are separate** — The broker handles registration, delivery, persistence, ack, and subscription. A separate policy layer classifies risk and enforces gates.
4. **Adapters are first-class** — Each agent gets a purpose-built adapter that maps the shared protocol to its native interface.
5. **Directed messaging, not broadcast** — v1 supports direct send, reply, and optional topic subscription. No unrestricted room-chat.
6. **Identity and trust boundaries** — Each agent has a stable identity with declared capabilities. No arbitrary role claims at runtime.

### What This Is NOT

- Not a clone of claude-peers-mcp
- Not an "agent-to-agent free chat" system
- Not the full Orchestrator agent from assumptions.md
- Not a replacement for the relay model (it's the infrastructure that makes relay programmable)

## Consequences

- All inter-agent communication becomes auditable and replayable
- ONE-WAY DOOR decisions get protocol-level enforcement (not just prose labels)
- The Orchestrator agent (when built) has a real transport layer to operate on
- Each agent adapter must be maintained separately as agent CLIs evolve

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|-------------|
| Unix sockets | Worse multi-client compatibility and debugging for v1 |
| Shared filesystem (file-drop) | No real-time delivery, race conditions |
| Clone claude-peers-mcp directly | Unstructured, Claude-only, no governance |
| Full Orchestrator agent first | Needs transport layer to exist first |

---

**Recorded in**: `palette/peers/docs/adr/0001-peers-architecture.md`
