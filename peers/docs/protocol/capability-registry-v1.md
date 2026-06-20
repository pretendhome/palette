# Capability Registry v1

**Version**: 1.0.0
**Status**: ACCEPTED (2026-03-23)

---

## Purpose

Every peer on the Palette Peers bus declares a stable identity and a set of capabilities at registration time. This prevents arbitrary role claims and enables intelligent routing.

## Peer Identity Format

```
<agent_name>.<primary_role>
```

### Registered Identities (v1)

| Identity | Agent | Runtime | Primary Role |
|----------|-------|---------|-------------|
| `kiro.design` | Kiro | kiro-cli | Systems architecture, convergence, field partner |
| `claude.analysis` | Claude Code | claude | Deep reading, bug chasing, verification, finishing |
| `codex.implementation` | Codex | codex | Strategy, reframing, implementation |
| `perplexity.research` | Perplexity | API adapter | External research, synthesis, current events |

## Registration Payload

When a peer registers with the broker, it sends:

```json
{
  "identity": "kiro.design",
  "agent_name": "kiro",
  "runtime": "kiro-cli",
  "pid": 12345,
  "cwd": "/home/mical/fde",
  "git_root": "/home/mical/fde",
  "capabilities": [
    "architecture",
    "convergence",
    "file_operations",
    "code_generation",
    "bash_execution"
  ],
  "palette_role": "architect",
  "trust_tier": "WORKING",
  "version": "1.0.0"
}
```

## Capability Vocabulary (v1)

Capabilities are declared from this controlled vocabulary:

| Capability | Description | Agents |
|-----------|-------------|--------|
| `architecture` | System design, tradeoff analysis | kiro, codex |
| `convergence` | Semantic blueprint, alignment | kiro |
| `code_generation` | Writing code | kiro, claude, codex |
| `code_review` | Reading and verifying code | claude, kiro |
| `bash_execution` | Running shell commands | kiro, claude, codex |
| `file_operations` | Reading/writing files | kiro, claude, codex |
| `web_search` | Searching the web | kiro, claude, perplexity |
| `deep_research` | Multi-source synthesis | perplexity |
| `current_events` | Time-sensitive information | perplexity |
| `debugging` | Root cause analysis, fix verification | claude, kiro |
| `testing` | Writing and running tests | claude, codex |
| `narrative` | GTM, customer-facing explanations | kiro, codex |

## Palette Role Mapping

Each peer maps to one primary Palette agent archetype:

| Palette Role | Archetype | Primary Peer |
|-------------|-----------|-------------|
| `resolver` | — | kiro.design |
| `researcher` | Argentavis | perplexity.research |
| `architect` | Rex | kiro.design / codex.implementation |
| `builder` | Therizinosaurus | codex.implementation / kiro.design |
| `debugger` | Raptor | claude.analysis |
| `narrator` | Yutyrannus | kiro.design / codex.implementation |
| `validator` | — | claude.analysis |
| `orchestrator` | Orch | (future — the bus itself enables this) |

## Trust Tier

Peers declare their current trust tier from the agent maturity model:

- `UNVALIDATED` — Human-in-the-loop required
- `WORKING` — Autonomous with review
- `PRODUCTION` — Fully autonomous until failure

Trust tier affects message handling:
- `UNVALIDATED` peers cannot send `execution_request` messages
- `UNVALIDATED` peers cannot approve `one_way_door` messages
- Only humans can approve `one_way_door` messages regardless of tier

## Adapter Contract

Every adapter MUST implement these operations:

| Operation | HTTP Method | Path | Description |
|-----------|------------|------|-------------|
| `register` | POST | `/register` | Register peer with broker |
| `heartbeat` | POST | `/heartbeat` | Keep-alive signal |
| `send` | POST | `/send` | Send an envelope to another peer |
| `fetch` | POST | `/fetch` | Retrieve undelivered messages |
| `ack` | POST | `/ack` | Acknowledge receipt of a message |
| `list_peers` | POST | `/list-peers` | Discover other registered peers |
| `list_capabilities` | GET | `/capabilities` | Return this peer's declared capabilities |
| `unregister` | POST | `/unregister` | Deregister from broker |

## Perplexity Adapter Note

Perplexity is not a local CLI peer. Its adapter:
- Runs as a long-lived process (not spawned per-session)
- Wraps the Sonar API behind the peer protocol
- Cannot receive push messages (poll-only)
- Cannot execute locally (research-only capabilities)
- Is always `WORKING` tier (reliability tracked via researcher.py impressions)
