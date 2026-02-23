# Telegram Relay V1 (Per-Implementation Artifacts)

## Goal
Add a safe bidirectional relay between Telegram and Palette using file artifacts, without granting direct shell access from Telegram.

## V1 Scope
- Per-implementation relay folders under `implementations/<impl-id>/telegram/`
- Append-only event trace (`events/*.jsonl`)
- Session summaries (`sessions/*.md`)
- Async handoff via `inbox/*.md` and `outbox/*.md`
- Trace IDs + idempotency keys
- Explicit provenance (`live_call` true/false)

## Folder Layout
```text
implementations/<impl-id>/telegram/
  events/
  sessions/
  inbox/
  outbox/
  archive/
  index/
    idempotency_seen.jsonl
  STATE.md
```

## Safety Rules (V1)
- Telegram is a constrained interface by default
- No direct shell execution from Telegram
- No hidden Orch dispatch; any dispatch must be explicit and logged
- Repo mutations require a separate approval-controlled path
- Redact secrets before writing artifacts

## Explicit GitHub Publish Choice (Supported as Metadata Only)
- Requests/responses can carry:
  - `publish_to_github_requested`
  - `publish_to_github_approved`
  - `publish_target_path`
- V1 relay consumer does **not** publish to GitHub.
- A separate publisher must require explicit approval before any repo write/commit.

## Local Scaffold
```bash
cd /home/mical/fde/palette/bridges/telegram
python3 relay_scaffold.py --impl-id retail-rossi-store
```

## Next Integration Step
Wire the Telegram bridge to:
1. append inbound/outbound events,
2. create request artifacts for allowlisted intents (e.g. `orch_summary_request`),
3. leave existing conversational behavior unchanged when no intent matches.

## Outbox Delivery (Telegram Replies)
Manual one-shot delivery (safe):
```bash
ROSSI_BOT_TOKEN=... \
python3 /home/mical/fde/palette/bridges/telegram/outbox_deliver.py \
  --impl-id retail-rossi-store \
  --once
```

Dry-run (no Telegram send, updates artifact delivery status to `dry_run_sent`):
```bash
python3 /home/mical/fde/palette/bridges/telegram/outbox_deliver.py \
  --impl-id retail-rossi-store \
  --dry-run \
  --once
```

Background poll loop (non-destructive, pending-only):
```bash
ROSSI_BOT_TOKEN=... \
nohup python3 /home/mical/fde/palette/bridges/telegram/outbox_deliver.py \
  --impl-id retail-rossi-store \
  --watch --poll-sec 5 \
  > /tmp/rossi_outbox_deliver.log 2>&1 &
```

### systemd Service (Recommended)
Service template:
- `palette/bridges/telegram/systemd/rossi-outbox-deliver.service`

Env template:
- `palette/bridges/telegram/systemd/rossi-outbox-deliver.env.example`

Install steps (server):
```bash
cp /home/mical/fde/palette/bridges/telegram/systemd/rossi-outbox-deliver.env.example \
   /home/mical/fde/palette/bridges/telegram/systemd/rossi-outbox-deliver.env

# edit and set ROSSI_BOT_TOKEN
nano /home/mical/fde/palette/bridges/telegram/systemd/rossi-outbox-deliver.env

sudo cp /home/mical/fde/palette/bridges/telegram/systemd/rossi-outbox-deliver.service \
        /etc/systemd/system/rossi-outbox-deliver.service
sudo systemctl daemon-reload
sudo systemctl enable --now rossi-outbox-deliver.service
sudo systemctl status rossi-outbox-deliver.service
```

Logs:
```bash
sudo journalctl -u rossi-outbox-deliver.service -f
```

## Inbox Consumer (Relay Processing)
Manual one-shot:
```bash
python3 /home/mical/fde/palette/bridges/telegram/relay_consumer.py \
  --impl-id retail-rossi-store --once
```

Watch loop:
```bash
python3 /home/mical/fde/palette/bridges/telegram/relay_consumer.py \
  --impl-id retail-rossi-store --watch --poll-sec 5
```

### systemd Service (Recommended)
Service template:
- `palette/bridges/telegram/systemd/rossi-relay-consumer.service`

Env template:
- `palette/bridges/telegram/systemd/rossi-relay-consumer.env.example`

Install steps (server):
```bash
cp /home/mical/fde/palette/bridges/telegram/systemd/rossi-relay-consumer.env.example \
   /home/mical/fde/palette/bridges/telegram/systemd/rossi-relay-consumer.env

# optionally enable Orch handoff in safe mode (plan/route only)
nano /home/mical/fde/palette/bridges/telegram/systemd/rossi-relay-consumer.env

sudo cp /home/mical/fde/palette/bridges/telegram/systemd/rossi-relay-consumer.service \
        /etc/systemd/system/rossi-relay-consumer.service
sudo systemctl daemon-reload
sudo systemctl enable --now rossi-relay-consumer.service
sudo systemctl status rossi-relay-consumer.service
```

Logs:
```bash
sudo journalctl -u rossi-relay-consumer.service -f
```

### Optional Request Syntax (metadata only)
```text
/relay update_request publish:implementations/retail-rossi-store/updates/2026-02-23.md | Draft today's Rossi update from our chat
```
This records a publish request in artifact metadata, but does not write to GitHub in v1.
