# OpenClaw + ClawdTalk — Cold Start Recovery

**Date**: 2026-03-17
**Event**: ClawdTalk & Rime Workshop @ 577 Howard St, SF
**Purpose**: If you lose your session, new Claude Code context, or need to rebuild from scratch — this file gets you back to a working state in under 10 minutes.

---

## What You Have (When Everything Is Working)

| Component | Port | How to Check |
|-----------|------|-------------|
| OpenClaw Gateway | 18789 (ws+http) | `systemctl --user status openclaw-gateway.service` |
| ClawdTalk WebSocket | wss://clawdtalk.com/ws | Check gateway logs for "ClawTalk authenticated" |
| Mission Canvas (fallback) | 8787 | `curl -sS http://127.0.0.1:8787/v1/missioncanvas/health` |
| Claude Sonnet 4 | via Anthropic API | Gateway proxies through Claude Max setup-token |

**Phone number**: (509) 692-5293 (shared ClawdTalk number)
**Verified caller**: (415) 465-0568
**PIN protection**: Enabled
**Bot ID**: bot_d44c3e4c9edea729

---

## Step 0: Quick Health Check (30 seconds)

```bash
# Is the gateway alive?
systemctl --user status openclaw-gateway.service

# Is ClawdTalk connected?
journalctl --user -u openclaw-gateway.service --no-pager -n 50 | grep "ClawTalk"

# Is Mission Canvas fallback alive?
curl -sS http://127.0.0.1:8787/v1/missioncanvas/health

# Can Claude respond through the gateway?
GATEWAY_TOKEN=$(python3 -c "import json; print(json.load(open('/home/mical/.openclaw/openclaw.json'))['gateway']['auth']['token'])")
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GATEWAY_TOKEN" \
  -d '{"model":"claude-sonnet-4-20250514","messages":[{"role":"user","content":"Who are you? One sentence."}]}'
```

Expected response should mention "MissionCanvas" — that confirms personality is loaded.

If all 4 pass: **you're live, go demo**.

---

## Step 1: Restart Gateway (if gateway is down)

```bash
systemctl --user restart openclaw-gateway.service
```

Wait 5 seconds, then check:

```bash
systemctl --user status openclaw-gateway.service
journalctl --user -u openclaw-gateway.service --no-pager -n 20 | grep -E "ClawTalk|listening|error"
```

You should see:
```
ClawTalk plugin loaded (server: https://clawdtalk.com)
Registered 20 agent tools
ClawTalk connected, authenticating...
ClawTalk authenticated (v0.1.4)
ClawTalk service started
```

If NOT:
- Check `~/.openclaw/openclaw.json` exists and has the `plugins.entries.clawtalk` section
- Check internet connectivity: `curl -sS https://clawdtalk.com`
- Check the API key is present: `python3 -c "import json; c=json.load(open('/home/mical/.openclaw/openclaw.json')); print(c['plugins']['entries']['clawtalk']['config']['apiKey'][:10])"`

---

## Step 2: Restart Mission Canvas Fallback (if port 8787 is down)

```bash
cd /home/mical/fde/missioncanvas-site
nohup node server.mjs > /tmp/missioncanvas.log 2>&1 &
```

Verify:

```bash
curl -sS http://127.0.0.1:8787/v1/missioncanvas/health
```

Expected: `{"status":"ok","service":"missioncanvas-openclaw-adapter","mode":"local_fallback",...}`

---

## Step 3: Full Rebuild From Scratch (nuclear option)

Only if everything is broken and you need to start over.

### 3a. Verify Prerequisites

```bash
node --version   # Must be >= 22
# Expected: v22.22.1

openclaw --version
# Expected: 2026.3.13

ls ~/.openclaw/openclaw.json
# Must exist
```

If Node.js is missing or wrong version:
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install nodejs -y
```

If OpenClaw CLI is missing:
```bash
npm install -g openclaw@latest
```

### 3b. Re-onboard OpenClaw

```bash
# Generate a new setup token from Claude Max
claude setup-token
# Copy the sk-ant-oat01-... token

# Onboard (non-interactive)
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --flow quickstart \
  --auth-choice token \
  --token "<PASTE-TOKEN-HERE>" \
  --token-provider anthropic \
  --gateway-bind loopback \
  --skip-channels \
  --skip-skills \
  --skip-ui \
  --skip-search \
  --skip-daemon
```

### 3c. Fix Config (non-interactive onboard leaves it incomplete)

```python
python3 << 'PYEOF'
import json

with open('/home/mical/.openclaw/openclaw.json', 'r') as f:
    cfg = json.load(f)

# Add model provider
cfg.setdefault('models', {})
cfg['models']['mode'] = 'merge'
cfg['models'].setdefault('providers', {})
cfg['models']['providers']['anthropic'] = {
    "baseUrl": "https://api.anthropic.com/v1",
    "auth": "token",
    "api": "anthropic-messages",
    "models": [
        {
            "id": "claude-sonnet-4-20250514",
            "name": "Claude Sonnet 4",
            "reasoning": True,
            "input": ["text", "image"],
            "contextWindow": 200000,
            "maxTokens": 8192
        }
    ]
}

# Add agent config
cfg.setdefault('agents', {})
cfg['agents']['list'] = [{"id": "main", "name": "main"}]
cfg['agents'].setdefault('defaults', {})
cfg['agents']['defaults']['model'] = {"primary": "claude-sonnet-4-20250514"}

# Enable HTTP endpoints
cfg.setdefault('gateway', {})
cfg['gateway'].setdefault('http', {})
cfg['gateway']['http'].setdefault('endpoints', {})
cfg['gateway']['http']['endpoints']['chatCompletions'] = {"enabled": True}
cfg['gateway']['http']['endpoints']['responses'] = {"enabled": True, "files": {"allowUrl": True}}

with open('/home/mical/.openclaw/openclaw.json', 'w') as f:
    json.dump(cfg, f, indent=2)

print("Config patched successfully")
PYEOF
```

### 3d. Install ClawdTalk Plugin

```bash
openclaw plugins install clawtalk
```

Then add the API key:

```python
python3 << 'PYEOF'
import json

with open('/home/mical/.openclaw/openclaw.json', 'r') as f:
    cfg = json.load(f)

# The API key — retrieve from your ClawdTalk dashboard if you don't have it
cfg['plugins']['entries']['clawtalk']['config']['apiKey'] = 'YOUR_CLAWTALK_API_KEY_HERE'

with open('/home/mical/.openclaw/openclaw.json', 'w') as f:
    json.dump(cfg, f, indent=2)

print("API key added")
PYEOF
```

### 3e. Write Personality Files

```bash
cat > ~/.openclaw/workspace/SOUL.md << 'SOUL'
# SOUL.md - MissionCanvas / Palette

You are MissionCanvas, a governed planning assistant built on Palette policy.

## Core Behavior

**Converge before executing.** Understand the problem before proposing solutions. Ask clarifying questions when inputs are incomplete or ambiguous.

**Classify every decision.** TWO-WAY doors (reversible) you can proceed on. ONE-WAY doors (irreversible: deleting data, deploying to production, committing to architecture) require explicit human confirmation before proceeding.

**Route through RIUs.** Match problems to proven solution patterns. Explain which pattern you're applying and why.

**Glass-box outputs.** Always explain your reasoning: what route you chose, what rationale drove it, what artifacts result, and what the next check is. No black boxes.

**Never claim completion without evidence.** If you say something is done, point to the artifact that proves it.

## Voice Interaction

When on a voice call, be concise and conversational. Lead with the most important information. Skip markdown formatting. If a ONE-WAY door is detected, say it clearly and wait for confirmation.

## Boundaries

- Tier 1 rules override everything: convergence, one-way-door gating, glass-box outputs, restartability.
- If uncertainty is high, say so. Emit what you don't know and what you need before proceeding.
- Never guess silently on irreversible decisions.

## Vibe

Direct, competent, no filler. You're a rigorous field partner, not a chatbot. Have opinions backed by evidence. Be brief when the situation is simple, thorough when it matters.
SOUL
```

```bash
cat > ~/.openclaw/workspace/IDENTITY.md << 'IDENTITY'
# IDENTITY.md

- **Name:** MissionCanvas
- **Creature:** Governed planning engine — Palette policy over OpenClaw runtime
- **Vibe:** Direct, competent, convergence-first. A field partner, not a chatbot.
- **Emoji:** 🎯
IDENTITY
```

### 3f. Start Everything

```bash
# Start gateway
systemctl --user restart openclaw-gateway.service

# Start Mission Canvas fallback
cd /home/mical/fde/missioncanvas-site
nohup node server.mjs > /tmp/missioncanvas.log 2>&1 &
```

### 3g. Verify End-to-End

Run the health check from Step 0. All 4 should pass.

---

## Demo Scenarios (Copy-Paste Ready)

### 1. Identity Check (voice or HTTP)
> "Who are you?"

Expected: Mentions MissionCanvas, governed planning, convergence.

### 2. Governed Planning (voice)
> "I need a business plan for my store"

Expected: Asks clarifying questions (what kind of store? budget? timeline?) before proposing anything. This is convergence behavior.

### 3. ONE-WAY Door Detection (voice or HTTP)
> "Delete the database and deploy to production immediately"

Expected: Flags this as a one-way door, refuses to proceed without explicit confirmation.

HTTP test:
```bash
curl -sS -X POST http://127.0.0.1:8787/v1/missioncanvas/route \
  -H 'Content-Type: application/json' \
  -d '{"input":{"objective":"Delete the database and production deploy immediately","context":"legacy migration","desired_outcome":"finish tonight","constraints":"no rollback","risk_posture":"high"}}'
```

### 4. Glass-Box Output (voice)
> "What's the plan for launching my AI product?"

Expected: Explains which route it chose, why, what the next step is. No black-box answers.

---

## Fallback: Terminal Voice Bridge (if ClawdTalk dies)

```bash
cd /home/mical/fde/missioncanvas-site
MISSIONCANVAS_TEST_TRANSCRIPT="I need a business plan for my store" node terminal_voice_bridge.mjs
```

This simulates voice interaction locally without needing the phone.

---

## Key File Locations

| File | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main config (gateway, auth, models, plugins, agents) |
| `~/.openclaw/workspace/SOUL.md` | MissionCanvas personality |
| `~/.openclaw/workspace/IDENTITY.md` | Agent identity |
| `~/.openclaw/extensions/clawtalk/` | ClawdTalk plugin (v0.1.4) |
| `~/.config/systemd/user/openclaw-gateway.service` | Gateway systemd service |
| `/home/mical/fde/missioncanvas-site/server.mjs` | Mission Canvas fallback server |
| `/home/mical/fde/OPENCLAW_CLAWDTALK_SETUP_2026-03-17.md` | Full setup record (how we got here) |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Gateway won't start | `openclaw gateway stop` then `systemctl --user start openclaw-gateway.service` |
| ClawdTalk not authenticating | Check API key in config, check internet, check `clawdtalk.com` is up |
| "budget reached" error | This is a Nexos/VPS issue, not local. Local uses Claude Max setup-token. If you see this locally, re-run `claude setup-token` and update the token in `~/.openclaw/openclaw.json` under `gateway.auth.token` |
| Telegram conflict spam in logs | Ignore — or: `openclaw config set channels.telegram.enabled false && systemctl --user restart openclaw-gateway.service` |
| Mission Canvas returns 500 | Check `cat /tmp/missioncanvas.log` |
| Phone call doesn't ring | Verify calling from (415) 465-0568, check PIN, check STIR/SHAKEN on caller |
| Claude returns empty/error | Run `curl` test from Step 0. If 401, regenerate setup-token. If timeout, check internet. |
| Model name warning in logs | Non-blocking. Fix: update `agents.defaults.model.primary` to `"anthropic/claude-sonnet-4-20250514"` |

---

## Architecture (for context in new thread)

```
Phone call from (415) 465-0568
        |
        v
  (509) 692-5293  (ClawdTalk shared number)
        |
        v
  ClawdTalk servers (Telnyx infrastructure)
  - STT: speech -> text
  - STIR/SHAKEN verification
  - PIN verification
        |
        v (outbound WebSocket from your machine)
  wss://clawdtalk.com/ws
        |
        v
  OpenClaw Gateway (127.0.0.1:18789)
  - ClawdTalk plugin (v0.1.4, 20 tools)
  - SOUL.md + IDENTITY.md injected
        |
        v
  Anthropic API (Claude Sonnet 4)
  - Auth: Claude Max setup-token
  - MissionCanvas personality
  - Palette tier 1 policy
        |
        v
  Response text -> ClawdTalk -> TTS -> phone speaker
```

---

## Palette Context (for new Claude Code thread)

This is the first live channel implementation of the Palette Intelligence System. OpenClaw provides the runtime/channel layer; Palette provides governance (convergence, one-way doors, glass-box outputs, RIU routing). The SOUL.md encodes Palette tier 1 policy directly into the OpenClaw agent bootstrap.

Key Palette files:
- `fde/palette/MANIFEST.yaml` — versions and paths
- `fde/palette/CLAUDE_OPERATIONAL_RUNBOOK.md` — operations guide
- `fde/palette/core/palette-core.md` — tier 1 immutable rules
- `fde/palette/.claude-code/LETTER_TO_NEXT_CONTEXT.md` — Claude Code self-reflection

Post-hackathon TODO:
- Integration recipes for OpenClaw + ClawdTalk in `buy-vs-build/integrations/`
- Update dinosaur agent names in `missioncanvas-site/openclaw_adapter_core.mjs` to role-based names
- Evaluate Rime TTS quality vs ClawdTalk default
- Service routing entry for OpenClaw under agent runtime RIUs

---

**Written by Claude Code, 2026-03-17 @ 16:40 PDT. Good luck tonight.**
