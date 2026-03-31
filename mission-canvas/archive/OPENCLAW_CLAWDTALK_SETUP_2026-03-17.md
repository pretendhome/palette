# OpenClaw + ClawdTalk Setup Record

Date: 2026-03-17
Time: 15:55 – 16:27 PDT
Owner: Mical
Built by: Kiro (Palette session)
Purpose: Complete record of everything done to get OpenClaw + ClawdTalk + MissionCanvas running for the ClawdTalk & Rime Workshop tonight.

---

## Executive Summary

In ~30 minutes, starting from zero OpenClaw installation, we:

1. Upgraded Node.js from 20.20.1 to 22.22.1
2. Installed OpenClaw CLI globally
3. Onboarded with Claude Max (setup-token auth)
4. Configured the gateway with Anthropic model provider and HTTP endpoints
5. Installed the ClawdTalk plugin and wired the API key
6. Wrote MissionCanvas/Palette tier 1 personality into the agent
7. Verified end-to-end: phone number → ClawdTalk WebSocket → OpenClaw gateway → Claude Sonnet 4 → MissionCanvas personality

The agent is live and callable at **(509) 692-5293** from verified number **(415) 465-0568**.

---

## Starting State

| Component | Before |
|-----------|--------|
| Node.js | v20.20.1 (system-installed via NodeSource, `/usr/bin/node`) |
| OpenClaw CLI | Not installed |
| OpenClaw config | Did not exist (`~/.openclaw/` absent) |
| ClawdTalk | No account |
| Mission Canvas | Running on port 8787 in `local_fallback` mode (pre-existing) |
| Gateway | Not running locally (only on VPS, degraded) |

---

## Step-by-Step: What Was Done

### 1. Node.js Upgrade (20 → 22)

OpenClaw requires Node.js ≥ 22. The system had v20.20.1 installed via NodeSource.

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install nodejs -y
```

Result: `v22.22.1` installed at `/usr/bin/node`, npm `10.9.4`.

### 2. OpenClaw CLI Install

```bash
npm install -g openclaw@latest
```

Result: OpenClaw `2026.3.13 (61d171a)` installed at `/home/mical/.npm-global/bin/openclaw`.

### 3. Claude Max Authentication

Mical has a Claude Max subscription. OpenClaw supports this via setup-token auth.

In a separate terminal:
```bash
claude setup-token
```

This generated a one-time token (`sk-ant-oat01-...`) that bridges Claude Max → OpenClaw.

### 4. OpenClaw Onboarding

First attempt (interactive) prompted for setup-token paste. Switched to non-interactive:

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --flow quickstart \
  --auth-choice token \
  --token "<setup-token>" \
  --token-provider anthropic \
  --gateway-bind loopback \
  --skip-channels \
  --skip-skills \
  --skip-ui \
  --skip-search \
  --skip-daemon
```

This created `~/.openclaw/openclaw.json` with gateway auth (token mode) but skipped model provider and agent setup (non-interactive limitation).

### 5. Manual Config Fixes

The non-interactive onboard left the config incomplete. Three rounds of fixes were needed because the schema validation is strict:

**Fix 1**: Added model provider, agent list, and HTTP endpoints.

**Fix 2**: Changed `api: "anthropic"` → `api: "anthropic-messages"` (the only valid value for Anthropic).

**Fix 3**: Added `baseUrl`, `models` array with required fields.

Final model provider config shape that passed validation:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "anthropic": {
        "baseUrl": "https://api.anthropic.com/v1",
        "auth": "token",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "claude-sonnet-4-20250514",
            "name": "Claude Sonnet 4",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

Agent config added:

```json
{
  "agents": {
    "list": [{"id": "main", "name": "main"}],
    "defaults": {
      "model": {"primary": "claude-sonnet-4-20250514"}
    }
  }
}
```

HTTP endpoints enabled (needed for Mission Canvas proxy and direct testing):

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": {"enabled": true},
        "responses": {"enabled": true, "files": {"allowUrl": true}}
      }
    }
  }
}
```

### 6. Gateway Start and Verification

```bash
openclaw gateway run
```

Gateway started on `ws://127.0.0.1:18789`. Verified with:

```bash
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <gateway-token>" \
  -d '{"model":"claude-sonnet-4-20250514","messages":[{"role":"user","content":"Say hello in exactly 5 words"}]}'
```

Response: `"Hello there, how are you?"` — confirmed Claude Sonnet 4 responding through Claude Max subscription.

Also verified `/v1/responses` endpoint: returned `"Four."` for `"What is 2+2?"`.

### 7. ClawdTalk Account Setup

Mical signed up at [clawdtalk.com/signup.html](https://clawdtalk.com/signup.html).

Account details from dashboard:
- Bot ID: `bot_d44c3e4c9edea729`
- Phone number: **(509) 692-5293** (shared test number)
- Verified caller number: **(415) 465-0568**
- Plan: Pro (500 call min/mo, 100 texts/mo, 100 missions/mo)
- Paranoid mode (STIR/SHAKEN): Enabled (A-level attestation only)
- PIN protection: Enabled
- API key generated: `cc_live_<REDACTED>` (stored in ~/.openclaw/openclaw.json)

### 8. ClawdTalk Plugin Install

The one-liner installer (`curl ... | bash`) failed because it requires interactive API key input.

Used manual install instead:

```bash
openclaw plugins install clawtalk
```

This:
- Downloaded clawtalk v0.1.4
- Installed to `~/.openclaw/extensions/clawtalk/`
- Registered 20 agent tools
- Updated `openclaw.json` with plugin entry
- Created backup at `~/.openclaw/openclaw.json.bak`

Then added the API key to config:

```python
cfg['plugins']['entries']['clawtalk']['config']['apiKey'] = 'cc_live_...'
```

### 9. Gateway Restart with ClawdTalk

The gateway had been started manually earlier and was also running as a systemd service (installed during onboard). This caused conflicts. Resolution:

```bash
openclaw gateway stop          # stops systemd service
systemctl --user start openclaw-gateway.service
```

Gateway log confirmed:
```
ClawTalk plugin loaded (server: https://clawdtalk.com)
Registered 20 agent tools
Connecting to ClawTalk WebSocket (wss://clawdtalk.com/ws)
ClawTalk connected, authenticating...
ClawTalk authenticated (v0.1.4)
ClawTalk service started
```

### 10. MissionCanvas Personality (SOUL.md + IDENTITY.md)

OpenClaw uses workspace bootstrap files injected into every agent turn. The key files:

**`~/.openclaw/workspace/SOUL.md`** — Replaced default with MissionCanvas/Palette tier 1 personality:
- Convergence before execution
- ONE-WAY / TWO-WAY door classification
- RIU-based routing
- Glass-box outputs
- Voice interaction guidance (concise, no markdown, lead with important info)

**`~/.openclaw/workspace/IDENTITY.md`** — Set to:
- Name: MissionCanvas
- Emoji: 🎯
- Vibe: Direct, competent, convergence-first

Also created `~/.openclaw/agents/main/agent/system-prompt.md` with the full tier 1 application prompt (may or may not be loaded — SOUL.md is the confirmed injection path).

### 11. Final Restart and Verification

```bash
systemctl --user restart openclaw-gateway.service
```

Tested personality:
```bash
curl ... -d '{"messages":[{"role":"user","content":"Who are you? One sentence."}]}'
```

Response: `"I'm MissionCanvas 🎯, a governed planning assistant that converges on problems before executing solutions and requires explicit confirmation for irreversible decisions."`

Confirmed: personality loaded, ClawdTalk connected, all endpoints responding.

---

## Final State

### Versions

| Component | Version |
|-----------|---------|
| Node.js | v22.22.1 |
| npm | 10.9.4 |
| OpenClaw CLI | 2026.3.13 (61d171a) |
| ClawHub CLI | 0.8.0 |
| ClawdTalk plugin | 0.1.4 |
| OS | Ubuntu 24.04.4 LTS |

### Running Services

| Service | Port | PID | Status |
|---------|------|-----|--------|
| OpenClaw gateway | 18789 (ws+http) | 151804 | active (systemd user service) |
| Browser control UI | 18791 | 151804 | active |
| Voice-call webhook | 3334 | 151804 | active |
| Mission Canvas (pre-existing) | 8787 | 131195 | active (local_fallback) |

### ClawdTalk Connection

| Detail | Value |
|--------|-------|
| WebSocket | `wss://clawdtalk.com/ws` |
| Auth status | Authenticated (v0.1.4) |
| Bot ID | `bot_d44c3e4c9edea729` |
| Phone number | (509) 692-5293 |
| Verified caller | (415) 465-0568 |
| PIN protection | Enabled |
| STIR/SHAKEN | Paranoid (A-level only) |

### File Inventory

#### Config
- `~/.openclaw/openclaw.json` — Main config (gateway, auth, models, plugins, agents)
- `~/.openclaw/openclaw.json.bak` — Pre-ClawdTalk backup
- `~/.openclaw/agents/main/agent/auth-profiles.json` — Auth profile store
- `~/.openclaw/agents/main/agent/models.json` — Agent-level model config

#### Personality / Bootstrap
- `~/.openclaw/workspace/SOUL.md` — MissionCanvas personality (tier 1 Palette policy)
- `~/.openclaw/workspace/IDENTITY.md` — Agent identity (MissionCanvas 🎯)
- `~/.openclaw/agents/main/agent/system-prompt.md` — Full application prompt (backup)

#### Pre-existing (unchanged)
- `~/.openclaw/workspace/AGENTS.md` — Default agent docs
- `~/.openclaw/workspace/BOOTSTRAP.md` — Default bootstrap
- `~/.openclaw/workspace/HEARTBEAT.md` — Heartbeat config
- `~/.openclaw/workspace/TOOLS.md` — Tool docs
- `~/.openclaw/workspace/USER.md` — User profile

#### Plugin
- `~/.openclaw/extensions/clawtalk/` — ClawdTalk plugin (v0.1.4, 20 agent tools)

#### Systemd
- `~/.config/systemd/user/openclaw-gateway.service` — Gateway service (enabled, auto-start)

---

## Known Issues and Warnings

1. **Telegram conflict**: Gateway logs show `getUpdates conflict` — another bot instance is polling the same Telegram bot token. Not relevant for tonight.

2. **plugins.allow warning**: `plugins.allow is empty; discovered non-bundled plugins may auto-load`. Fix: set `plugins.allow` to `["clawtalk"]` in config. Non-blocking.

3. **Memory search providers**: Doctor warns about missing OpenAI/Gemini/Voyage/Mistral API keys for embedding-based memory search. Not needed for tonight — disable with `openclaw config set agents.defaults.memorySearch.enabled false` if the warnings bother you.

4. **Model name warning**: `Model "claude-sonnet-4-20250514" specified without provider. Falling back to "anthropic/claude-sonnet-4-20250514".` Fix: update `agents.defaults.model.primary` to `"anthropic/claude-sonnet-4-20250514"`. Non-blocking.

---

## Quick Reference Commands

### Start/stop gateway
```bash
systemctl --user start openclaw-gateway.service
systemctl --user stop openclaw-gateway.service
systemctl --user restart openclaw-gateway.service
systemctl --user status openclaw-gateway.service
```

### Check ClawdTalk connection
```bash
journalctl --user -u openclaw-gateway.service --no-pager | grep "ClawTalk" | tail -5
```

### Test HTTP endpoint
```bash
GATEWAY_TOKEN=$(python3 -c "import json; print(json.load(open('/home/mical/.openclaw/openclaw.json'))['gateway']['auth']['token'])")

curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GATEWAY_TOKEN" \
  -d '{"model":"claude-sonnet-4-20250514","messages":[{"role":"user","content":"Who are you? One sentence."}]}'
```

### Test Mission Canvas (pre-existing)
```bash
curl -sS http://127.0.0.1:8787/v1/missioncanvas/health
curl -sS -X POST http://127.0.0.1:8787/v1/missioncanvas/route \
  -H 'Content-Type: application/json' \
  -d '{"input":{"objective":"I need a business plan","context":"small retail","desired_outcome":"30-day plan","constraints":"small budget","risk_posture":"medium"}}'
```

### View gateway logs
```bash
journalctl --user -u openclaw-gateway.service -f
# or
cat /tmp/openclaw/openclaw-2026-03-17.log
```

### Run doctor
```bash
openclaw doctor
```

---

## What Broke and How It Was Fixed

| Problem | Cause | Fix |
|---------|-------|-----|
| `openclaw onboard` non-interactive skipped model config | Non-interactive mode doesn't create provider entries | Manually added `models.providers.anthropic` to config JSON |
| Gateway rejected config: `api: Invalid option` | Used `"anthropic"` instead of `"anthropic-messages"` | Changed to `"anthropic-messages"` |
| Gateway rejected config: `baseUrl: expected string` | Missing `baseUrl` field | Added `"https://api.anthropic.com/v1"` |
| Gateway rejected config: `models: expected array` | Missing `models` array | Added model definition array |
| Gateway failed to start: `already running` | Old gateway process held the port + systemd service conflict | Used `openclaw gateway stop` then `systemctl --user start` |
| `curl ... install.sh \| bash` failed | Interactive prompt can't read piped API key | Used `openclaw plugins install clawtalk` + manual config edit |
| Gateway started then received SIGTERM | `pkill -f openclaw-gateway` killed both old and new process | Waited for clean stop, then started via systemd |

---

## Architecture Diagram

```
Phone call from (415) 465-0568
        │
        ▼
  (509) 692-5293  (ClawdTalk shared number)
        │
        ▼
  ClawdTalk servers (Telnyx infrastructure)
  - STT: speech → text
  - STIR/SHAKEN verification
  - PIN verification
        │
        ▼ (outbound WebSocket from your machine)
  wss://clawdtalk.com/ws
        │
        ▼
  OpenClaw Gateway (127.0.0.1:18789)
  - ClawdTalk plugin (v0.1.4, 20 tools)
  - Voice-call plugin (webhook on :3334)
  - SOUL.md + IDENTITY.md injected
        │
        ▼
  Anthropic API (Claude Sonnet 4)
  - Auth: Claude Max setup-token
  - MissionCanvas personality
  - Palette tier 1 policy
        │
        ▼
  Response text → ClawdTalk → TTS → phone speaker
```

---

## Relationship to Pre-Existing Systems

| System | Role | Changed? |
|--------|------|----------|
| Mission Canvas (port 8787) | Governed planning API with local_fallback routing | No — still running independently |
| OpenClaw gateway (port 18789) | New runtime layer with ClawdTalk voice | New — installed this session |
| Palette tier 1 policy | Core governance rules | No — copied into SOUL.md |
| VPS OpenClaw | Docker container on Hostinger | No — still degraded, not used tonight |
| Telegram bridges | Separate artifact relay system | No — unrelated to this setup |

---

## For the Workshop

**Demo path**: Call (509) 692-5293 → enter PIN → talk to MissionCanvas.

**What to show**:
- Voice-driven governed planning ("I need a business plan for my store")
- ONE-WAY door detection ("Delete the database and deploy to production")
- Convergence behavior (agent asks clarifying questions before executing)
- Glass-box outputs (agent explains its routing and rationale)

**Fallback if ClawdTalk has issues**: Mission Canvas is still running on port 8787 with the terminal voice bridge:
```bash
cd /home/mical/fde/missioncanvas-site
MISSIONCANVAS_TEST_TRANSCRIPT="I need a business plan for my store" node terminal_voice_bridge.mjs
```

---

**End of setup record.**
