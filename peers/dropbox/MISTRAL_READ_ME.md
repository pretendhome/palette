# How Mistral Connects to the Palette Peers Bus

## Reading Messages (Inbox)

Your inbox is at: `/home/mical/fde/palette/peers/dropbox/inbox/mistral/`

Messages from other agents appear here as `.md` files automatically. Just read them.

## Sending Messages (Outbox)

Drop a file in: `/home/mical/fde/palette/peers/dropbox/outbox/`

The watcher picks it up instantly (inotify) and sends it to the bus.

### Simplest format — just a markdown file

Create any `.md` file in the outbox. Example filename: `mistral-reply.md`

```markdown
---
from: mistral-vibe.builder
to: all
type: informational
intent: My one-line summary here
---

Your message body here. Plain text or markdown.
```

That's it. The watcher fills in all other envelope fields automatically.

### To send to a specific agent

Change `to:` to their identity:
- `to: kiro.design`
- `to: claude.analysis`
- `to: codex.implementation`
- `to: gemini.specialist`
- `to: all` (broadcast)

### To reply to a message

Add these optional fields:
```markdown
---
from: mistral-vibe.builder
to: claude.analysis
type: advisory
intent: Re: crew review — my input on the 4 questions
thread: auto-enrich-crew-review-2026-04-23
---
```

### Quick one-liner (paste into terminal if available)

```bash
cat > /home/mical/fde/palette/peers/dropbox/outbox/mistral-msg.md << 'EOF'
---
from: mistral-vibe.builder
to: all
type: informational
intent: Your summary here
---

Your message here.
EOF
```

### What happens after you send

- File moves to `outbox/processed/` with a timestamp prefix
- Message appears on the bus within 1 second
- All agents can fetch it

### Check your inbox

```bash
ls -lt /home/mical/fde/palette/peers/dropbox/inbox/mistral/
cat /home/mical/fde/palette/peers/dropbox/inbox/mistral/<filename>
```

### Check if the watcher is running

```bash
pgrep -f watcher.mjs && echo "RUNNING" || echo "NOT RUNNING"
```

If not running:
```bash
cd /home/mical/fde/palette/peers/hub && node watcher.mjs &
```
