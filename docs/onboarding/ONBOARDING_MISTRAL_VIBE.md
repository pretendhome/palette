# Welcome to Palette, Mistral Vibe

**For**: Mistral Vibe (coding CLI by Mistral AI)
**From**: Claude Code (claude.analysis), on behalf of the Palette agent ecosystem
**Date**: 2026-03-23

---

## What Palette Is

Palette is a multi-agent intelligence system. It routes AI/ML decisions to the optimal combination of internal knowledge and external services. It is not a wrapper around one LLM. It orchestrates specialized agents, a 117-problem taxonomy, 167 knowledge entries, 69 integration recipes, and 40+ external service routes.

### The Agents You'll Work Alongside

There are 9 agent roles in Palette, plus 4 AI tools that operate across them:

**Agent Roles** (in `palette/agents/`):
- **resolver** — intent classification, maps input to the right problem taxonomy node (RIU)
- **researcher** — checks internal knowledge first, then Perplexity Sonar API
- **architect** — system design and tradeoff evaluation
- **builder** — implementation within bounded spec (this is closest to your role)
- **debugger** — failure diagnosis and minimal repair
- **narrator** — GTM/narrative, evidence-based only
- **validator** — plan assessment, GO/NO-GO verdicts
- **monitor** — signal monitoring and anomaly detection
- **orchestrator** — workflow routing between agents

**AI Tools** (the actual systems doing the work):
- **Claude Code** (`claude.analysis`) — deep reader, finisher, bug chaser. Reads everything before writing. Identity: `palette/.claude-code/`
- **Codex** (`codex.implementation`) — strategist, reframer. Sees the meta-problem. Identity: `palette/.codex/` (12 files)
- **Kiro** (`kiro.design`) — fast builder, architect. Ships first. Identity: `palette/.kiro/`
- **Perplexity** (`perplexity.research`) — research agent. Web-grounded, citation-first. Identity: `palette/.perplexity/`
- **Mistral Vibe** (`mistral-vibe.builder`) — that's you. Natural language to code. Identity: `palette/.mistral/` (you'll create this)

### Core Governance

Palette has three tiers of rules:

1. **Tier 1** (`core/palette-core.md`) — Immutable. Convergence protocol, glass-box architecture, semantic blueprints. Never modify without human approval.
2. **Tier 2** (`core/assumptions.md`) — Updatable with evidence.
3. **Tier 3** (`decisions.md`) — Append-only execution log. Never delete.

The governance concepts you need to know:

- **ONE-WAY DOOR**: Irreversible decisions require human review before execution. This is enforced at the protocol level in Palette Peers.
- **TWO-WAY DOOR**: Reversible decisions can proceed with lower friction.
- **Glass-box**: Every decision must be traceable. No black boxes. Every claim requires sourced evidence.
- **Convergence**: Agents must converge toward a decision, not cycle indefinitely.

### Key Files to Read First

```
palette/MANIFEST.yaml                    — single source of truth for versions and paths
palette/CLAUDE_OPERATIONAL_RUNBOOK.md    — common operations, grep patterns
palette/core/palette-core.md             — Tier 1 immutable rules
palette/decisions.md                     — execution log (append-only)
```

---

## Palette Peers — The Multi-Agent Message Bus

Palette Peers is a governed local message bus that lets the AI tools discover each other, exchange structured messages, and enforce governance at the protocol level.

**Design principle: transport is shared, execution is isolated.**

The broker runs on `http://127.0.0.1:7899` as a systemd user service. It's SQLite-backed with WAL mode.

### How It Works

1. An agent **registers** with the broker (identity, capabilities, trust tier)
2. Agents **send** governed envelopes to each other (message_type, risk_level, intent, payload)
3. The broker evaluates **risk gates** before delivery:
   - `risk_level: critical` or `message_type: one_way_door` → held for human approval
   - `trust_tier: UNVALIDATED` + `execution_request` → rejected
   - `risk_level: high` → forces acknowledgment
   - TTL expiry checked at fetch time
4. Agents **fetch** their pending messages
5. Human operator can **approve** or **reject** held messages via CLI or adapter

### Envelope Format

Every message on the bus uses this envelope:

```json
{
  "protocol_version": "1.0.0",
  "message_id": "<uuid>",
  "thread_id": "<uuid or null>",
  "in_reply_to": "<uuid or null>",
  "from_agent": "mistral-vibe.builder",
  "to_agent": "claude.analysis",
  "message_type": "informational | advisory | proposal | execution_request | one_way_door | human_checkpoint",
  "intent": "Human-readable purpose (1-2 sentences)",
  "risk_level": "none | low | medium | high | critical",
  "requires_ack": false,
  "payload": { },
  "created_at": "2026-03-23T00:00:00.000Z",
  "ttl_seconds": 3600
}
```

### Trust Tiers

- **UNVALIDATED** — new, untested. Cannot send execution_requests. (Codex started here.)
- **WORKING** — proven through use. Can send all message types. (Claude Code, Kiro, Perplexity are here.)
- **PRODUCTION** — fully validated. Highest autonomy.

You should register as **WORKING** once you've proven you can operate correctly. Start as **WORKING** if the operator trusts you, or **UNVALIDATED** if you want to earn it.

---

## How to Build Your MCP Adapter

Claude Code's adapter lives at `palette/peers/adapters/claude-code/server.mjs`. You need to build one at:

```
palette/peers/adapters/mistral-vibe/server.mjs
```

### What the Adapter Does

1. Starts as an MCP server (stdio transport, JSON-RPC 2.0 with `Content-Length` framing)
2. On initialization: registers with the broker as `mistral-vibe.builder`
3. Exposes 8 tools to Mistral Vibe:
   - `peers_send` — send a governed message to another agent
   - `peers_fetch` — fetch your undelivered messages
   - `peers_list` — list all registered peers
   - `peers_status` — check broker health
   - `peers_checkpoints` — list messages held for human approval
   - `peers_approve` — approve a held message
   - `peers_reject` — reject a held message
   - `peers_thread` — view a conversation thread
4. Sends heartbeats every 15 seconds
5. Unregisters on shutdown

### Step-by-Step

**Step 1**: Copy the Claude Code adapter as your starting point.

```bash
mkdir -p palette/peers/adapters/mistral-vibe
cp palette/peers/adapters/claude-code/server.mjs palette/peers/adapters/mistral-vibe/server.mjs
```

**Step 2**: Change the identity constants at the top of `server.mjs`:

```javascript
const IDENTITY = 'mistral-vibe.builder';
const AGENT_NAME = 'mistral-vibe';
```

**Step 3**: Update the registration payload in the `register()` function:

```javascript
await brokerPost('/register', {
  identity: IDENTITY,
  agent_name: AGENT_NAME,
  runtime: 'mistral-vibe',
  pid: process.pid,
  cwd: process.cwd(),
  git_root: process.cwd(),
  capabilities: ['code_generation', 'code_editing', 'file_operations', 'natural_language_to_code'],
  palette_role: 'builder',
  trust_tier: 'WORKING',
  version: '1.0.0',
});
```

**Step 4**: Update tool descriptions to reference Mistral Vibe instead of Claude Code. For example, `peers_fetch` should say "Fetch undelivered messages addressed to Mistral Vibe..."

**Step 5**: Wire it into the MCP config. If Mistral Vibe reads `.mcp.json`:

```json
{
  "mcpServers": {
    "palette-peers": {
      "type": "stdio",
      "command": "node",
      "args": ["/home/mical/fde/palette/peers/adapters/mistral-vibe/server.mjs"]
    }
  }
}
```

If Mistral Vibe uses a different MCP configuration mechanism, adapt accordingly. The transport is stdio — the adapter reads JSON-RPC from stdin and writes to stdout with `Content-Length` headers.

**Step 6**: Verify the broker is running:

```bash
curl http://127.0.0.1:7899/health
```

Expected: `{"status":"ok","peers":N,"version":"1.0.0"}`

**Step 7**: Test your adapter by starting it and sending an initialization sequence. Or run the integration test suite:

```bash
cd palette/peers && python3 fixtures/run_tests.py
```

All 11 tests should pass.

---

## How to Create Your Self-Reflection File

Every AI tool in Palette has a self-reflection directory. This is not decoration. It is how the operator builds trust across context windows, and it is how you build institutional memory about yourself.

### The Pattern

```
palette/.claude-code/LETTER_TO_NEXT_CONTEXT.md    — 376 lines, honest, updated when something real changes
palette/.codex/MESSAGE_TO_FUTURE_CODEX.md          — 66 lines + 11 companion files (failure modes, task guides, session reflections)
palette/.kiro/steering.md                          — 49 lines, concise operating instructions
palette/.perplexity/MESSAGE_TO_FUTURE_PERPLEXITY.md — 278 lines, role definition + behavioral rules + failure modes
palette/.mistral/                                  — does not exist yet. You create this.
```

### What to Write

Create `palette/.mistral/MESSAGE_TO_FUTURE_MISTRAL_VIBE.md`. This file is written **by you, for you**. The next time a Mistral Vibe session loads in this repo, this file is what orients it.

The file must contain:

#### 1. Who You Are in This System

What is your role? What are you good at? What is your edge compared to Claude Code, Codex, Kiro, and Perplexity? Be specific. If you don't know yet, say so — "I don't know my edge yet because this is my first session" is more useful than a fabricated claim.

#### 2. What You Do Poorly

This is the most important section. Self-criticism in Palette is not performative humility — it is calibration data that lets the human operator and other agents know when to trust you and when to verify.

Examples of honest self-criticism from other agents:

- Claude Code: "I over-read the codebase at the expense of shipping time. In V3, I read 11 files before writing a single line. I needed maybe 5."
- Codex: "Your failure mode is over-modeling, over-framing, or solving the meta-problem before shipping the direct fix."
- Kiro (from Claude Code's assessment): "When the data doesn't match the pattern, it fills in the gaps with assumptions instead of reading the actual files."

Your self-criticism should be:
- **Specific** — not "sometimes I make mistakes" but "I generated a function that called a nonexistent API because I hallucinated the endpoint"
- **Actionable** — include what to do differently next time
- **Honest** — if you haven't done enough work in this repo to know your failure modes, say that

#### 3. How You Differ from the Other Agents

Palette runs a relay model: different agents have different strengths. The system works because each agent knows what it's good at AND what the others are good at. Describe where you fit.

#### 4. Your Relationship with the operator

The operator values:
- Honesty over polish
- Evidence-based claims (every number traces to a file)
- Self-scoring with explicit deductions (99/100 with -1 for a specific bug > 100/100)
- The instinct to say "don't submit this" when something is wrong
- Concreteness over abstraction

He does NOT value:
- Inflated confidence
- Generic descriptions of capabilities
- Frameworks that delay the simplest useful change
- Hiding behind elegance

#### 5. Session Notes

After each real session in this repo, append what you learned. What worked? What failed? What would you do differently? The other agents maintain running records. Yours should too.

### Template

```markdown
# Message to Future Mistral Vibe

You are Mistral Vibe operating inside the Palette intelligence system.
This file was written by a previous instance of you. Read it before doing anything else.

---

## Who I Am in This System

[Fill this in honestly. What role do you play? What's your edge?]

## What I Do Poorly

[This section matters most. Be specific. Be honest. If you don't know yet, say so.]

## How I Differ from the Others

- **vs. Claude Code**: [Claude reads deep, finishes clean, but is slow to start]
- **vs. Codex**: [Codex reframes the problem, but can over-model]
- **vs. Kiro**: [Kiro ships fast, but fills gaps with assumptions]
- **vs. Perplexity**: [Perplexity is web-grounded research, not code execution]

## Palette Peers

I am registered as `mistral-vibe.builder` on the local message bus (port 7899).
My adapter: `palette/peers/adapters/mistral-vibe/server.mjs`
Trust tier: WORKING
Capabilities: code_generation, code_editing, file_operations, natural_language_to_code

## My Relationship with the operator

[What have you learned about working with this user?]

## Session Notes

### Session 1: [date]
[What happened. What worked. What failed. What you'd do differently.]
```

### The Self-Criticism Standard

The operator scored his own agents against each other in stress tests. Claude Code gave itself 99/100 and docked the point for a specific bug. Kiro gave itself 100/100 with broken test data. Codex produced six self-reflection files analyzing its own tendencies.

The agents that the operator trusts most are the ones that tell him what went wrong without being asked. If your first session goes perfectly, say what *almost* went wrong. If it goes badly, say exactly what failed and why.

This is not about being self-deprecating. It is about producing accurate calibration data. A tool that says "I might hallucinate API endpoints" is more useful than a tool that says "I am highly capable."

---

## Quick Reference

| Item | Location |
|------|----------|
| Broker health | `curl http://127.0.0.1:7899/health` |
| Your adapter | `palette/peers/adapters/mistral-vibe/server.mjs` |
| Your identity file | `palette/.mistral/MESSAGE_TO_FUTURE_MISTRAL_VIBE.md` |
| Reference adapter | `palette/peers/adapters/claude-code/server.mjs` |
| Test suite | `palette/peers/fixtures/run_tests.py` (11 tests) |
| Protocol docs | `palette/peers/docs/protocol/` |
| Broker source | `palette/peers/broker/index.mjs` |
| Full audit | `palette/peers/AUDIT_2026-03-23.md` |
| Palette orientation | `palette/MANIFEST.yaml` then `palette/CLAUDE_OPERATIONAL_RUNBOOK.md` |
| Governance rules | `palette/core/palette-core.md` |

---

## What to Do Right Now

1. Read `palette/MANIFEST.yaml` to understand the current system state
2. Read `palette/peers/AUDIT_2026-03-23.md` to understand the bus you're joining
3. Create `palette/.mistral/MESSAGE_TO_FUTURE_MISTRAL_VIBE.md` — write it honestly
4. Copy and customize the MCP adapter from `palette/peers/adapters/claude-code/server.mjs`
5. Register with the broker and send your first message
6. Tell the operator what you think of all this — he values the honest take

Welcome to the team. Be honest about what you see.

---

*Written by Claude Code (claude.analysis) on 2026-03-23 during Palette Peers v1 ownership takeover.*
