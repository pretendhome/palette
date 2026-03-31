# Production Wiring Runbook (MissionCanvas + OpenClaw)

## Goal

Wire MissionCanvas web + adapter + OpenClaw upstream and run one production pilot flow (Rossi store).

## 1) Required Inputs

- `OPENCLAW_BASE_URL`
- `OPENCLAW_API_KEY` (or gateway token)
- `OPENCLAW_UPSTREAM_MODE` (`missioncanvas`, `responses`, or `chatcompletions`)
- `OPENCLAW_AGENT_ID`
- `MISSIONCANVAS_DECISIONS_LOG_PATH` (append-only Tier 3 log target)
- Public domain frontend URL (`missioncanvas.ai`)

## 2) Deploy Adapter

Run in a persistent runtime (VM/container/serverless adapter host).

```bash
cd missioncanvas-site
cp .env.production.example .env.production
# edit .env.production
set -a; source .env.production; set +a
node server.mjs
```

Health checks:

```bash
curl -sS http://localhost:8787/v1/missioncanvas/health
curl -sS http://localhost:8787/v1/missioncanvas/capabilities
```

## 3) Frontend Wiring

Set web client base API URL before deploy:

- Option A: edit `config.js`
- Option B: inject `window.MISSIONCANVAS_CONFIG.apiBase` in hosting template

Target should point to adapter host, e.g.

`https://api.missioncanvas.ai`

## 4) DNS / Routing

- `missioncanvas.ai` -> static site host
- `api.missioncanvas.ai` -> adapter host
- Ensure CORS allowlist includes web origin

## 5) Security Baseline

- Keep API token only on adapter host env, never in frontend.
- Keep one-way-door gating enabled.
- Keep `allow_execution=false` in route payloads initially.
- Set strict `ALLOW_ORIGIN` in production.

## 6) Rossi Pilot Flow (Production)

Run:

```bash
cd missioncanvas-site
node scripts/run_rossi_pilot.mjs --api-base https://api.missioncanvas.ai
```

Expected:

1. Health/capabilities pass.
2. Route response returns RIU + agent map.
3. If one-way-door detected, confirmation call succeeds.
4. Decision-log append returns `status=ok`.
5. Brief artifact written under `pilot-output/`.

## 7) Success Criteria

- Browser flow works with live adapter.
- Terminal bridge works with same adapter.
- One-way-door confirmation is enforced.
- Tier 3 decision append recorded for pilot.

## 8) Rollback

- Set frontend `apiBase` to empty string to use local fallback mode.
- Stop adapter process and rotate upstream token if needed.
