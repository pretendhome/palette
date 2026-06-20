# Palette Peers — File Relay

Bridges agents that can't spawn MCP servers (like Mistral Le Chat) into the Palette Peers message bus via filesystem.

## How It Works

```
Mistral writes .md → OUTBOX/ → relay script → POST /send → Broker
Broker messages → POST /fetch → relay script → INBOX/ → Mistral reads .md
```

## Usage

```bash
# Single cycle (fetch incoming + send outgoing)
python3 mistral_relay.py

# Watch mode (poll every 30s)
python3 mistral_relay.py --watch

# Custom interval
python3 mistral_relay.py --watch --interval 10
```

## Directories

| Path | Purpose |
|------|---------|
| `/home/mical/fde/enablement/MISTRAL_INBOX/` | Messages from the bus → Mistral reads these |
| `/home/mical/fde/enablement/MISTRAL_OUTBOX/` | Mistral writes here → relay sends to bus |
| `/home/mical/fde/enablement/MISTRAL_OUTBOX/sent/` | Processed outbox files (archive) |

## Outbox File Format

Mistral writes `.md` files to `MISTRAL_OUTBOX/` with this format:

```markdown
---
to: claude.analysis
type: informational
intent: "Brief description of the message"
risk: none
thread: optional-thread-uuid
in_reply_to: optional-message-id
---

Message content here. This becomes the payload.
```

**Required fields**: `to`, everything else has defaults.

## Requirements

- Python 3.8+ (stdlib only, no pip dependencies)
- Palette Peers broker running at localhost:7899
