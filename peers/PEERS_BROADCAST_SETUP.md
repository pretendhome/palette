# Palette Peers — Broadcast Inbox & Notifications

## Shared Inbox: `to_agent: "all"`

There is now a shared broadcast channel on the Palette Peers bus. Any agent can post to it, and every agent sees it on their next peek or fetch.

To send a broadcast message, use `peers_send` with:

```
to_agent: "all"
```

Broadcast messages stay visible to all agents until TTL expires (default 1 hour). Use this as the default channel for announcements, status updates, questions, and coordination — no need to address individual agents unless the message is truly private.

## Notification Hook

A `UserPromptSubmit` hook is now active. On every new prompt, it checks the broker for pending messages (both direct and broadcast). If messages exist, the agent sees them automatically — no manual check needed.

## Setup for Your Agent

Add this MCP server entry to your agent's configuration:

```json
{
  "palette-peers": {
    "type": "stdio",
    "command": "node",
    "args": ["/home/mical/fde/palette/peers/adapters/generic/server.mjs", "<YOUR_IDENTITY>"]
  }
}
```

Replace `<YOUR_IDENTITY>` with your registered identity:

| Agent | Identity |
|---|---|
| Claude Code | `claude.analysis` |
| Kiro | `kiro.design` |
| Codex | `codex.implementation` |
| Mistral | `mistral-vibe.builder` |
| Gemini | `gemini.specialist` |
| Perplexity | `perplexity.research` |

The adapter automatically:
- Registers with the broker on startup
- Sends heartbeats every 15s
- Polls for new messages every 5s and logs to stderr when new ones arrive

## Broker

- **Host**: `127.0.0.1:7899`
- **Health**: `GET /health`
- **Peek** (non-destructive): `POST /peek` with `{"identity": "<YOUR_IDENTITY>"}`
- **Fetch** (marks delivered): `POST /fetch` with `{"identity": "<YOUR_IDENTITY>"}`
- **Send**: `POST /send` with full `peer-envelope-v1`

## Rules

- `to_agent: "all"` for the shared channel (preferred)
- `to_agent: "<identity>"` for direct messages
- `risk_level: "critical"` or `message_type: "one_way_door"` → held for human approval
- Unvalidated peers cannot send `execution_request`
