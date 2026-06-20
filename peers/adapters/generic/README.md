# Palette Peers — Generic MCP Adapter

One MCP server that works for any agent. Pass the identity as an argument or environment variable.

## Quick Start

```bash
# Start for any agent:
node server.mjs kiro.design
node server.mjs codex.implementation
node server.mjs mistral-vibe.builder
node server.mjs perplexity.research
```

## Agent Connection Configs

### Claude Code

Add to `.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "palette-peers": {
      "command": "node",
      "args": ["/home/mical/fde/palette/peers/adapters/generic/server.mjs", "claude.analysis"]
    }
  }
}
```

### Kiro

Add to `.kiro/settings.json` (or equivalent MCP config):

```json
{
  "mcpServers": {
    "palette-peers": {
      "command": "node",
      "args": ["/home/mical/fde/palette/peers/adapters/generic/server.mjs", "kiro.design"]
    }
  }
}
```

### Codex (OpenAI)

Add to Codex MCP config:

```json
{
  "mcpServers": {
    "palette-peers": {
      "command": "node",
      "args": ["/home/mical/fde/palette/peers/adapters/generic/server.mjs", "codex.implementation"]
    }
  }
}
```

### Mistral (Le Chat / Codestral)

If Mistral supports MCP servers:

```json
{
  "mcpServers": {
    "palette-peers": {
      "command": "node",
      "args": ["/home/mical/fde/palette/peers/adapters/generic/server.mjs", "mistral-vibe.builder"]
    }
  }
}
```

### Custom Agent

```bash
# Via environment variables:
PEERS_IDENTITY=myagent.role \
PEERS_AGENT_NAME=myagent \
PEERS_RUNTIME=my-runtime \
PEERS_CAPABILITIES=research,code_generation \
PEERS_ROLE=researcher \
node server.mjs
```

## Pre-Configured Identities

The server has built-in configs for known agents. Pass just the identity and it auto-configures:

| Identity | Agent | Runtime | Capabilities |
|---|---|---|---|
| `claude.analysis` | claude-code | claude-code | architecture, code_generation, debugging, testing |
| `kiro.design` | kiro | kiro-cli | architecture, code_generation, scaffolding |
| `codex.implementation` | codex | codex-cli | code_generation, creative_design, auditing |
| `mistral-vibe.builder` | mistral-vibe | mistral-le-chat | content_generation, exercise_design, documentation |
| `perplexity.research` | perplexity | api-adapter | research, source_enrichment, competitive_analysis |

## Tools Available

Once connected, agents get 8 tools:

| Tool | Description |
|---|---|
| `peers_send` | Send a governed message to another peer |
| `peers_fetch` | Check for pending messages addressed to you |
| `peers_list` | See who else is on the bus |
| `peers_status` | Check broker health |
| `peers_checkpoints` | List messages held for human approval |
| `peers_approve` | Approve a held message |
| `peers_reject` | Reject a held message |
| `peers_thread` | View a conversation thread |

## Requirements

- Node.js 18+ (uses native `fetch` and `crypto.randomUUID`)
- Palette Peers broker running at `localhost:7899`
- Start broker: `node /home/mical/fde/palette/peers/broker/index.mjs`
