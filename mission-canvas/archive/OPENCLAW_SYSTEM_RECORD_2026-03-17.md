# OpenClaw System Record

Date: 2026-03-17
Owner: Mical
Purpose: Single source of truth for what has been attempted with OpenClaw, how it connects to Mission Canvas and Telegram bridges, what exists on disk, what exists on the VPS, and what is actually usable tonight.

## Executive Summary

Three things are true at the same time:

1. Mission Canvas is working locally in `local_fallback` mode and is the only end-to-end path verified for tonight.
2. OpenClaw is installed and running on the Hostinger VPS inside Docker, but host-side integration is degraded.
3. Telegram bridge infrastructure exists as a separate file-artifact relay system and is not the same thing as the OpenClaw voice/runtime path.

The practical consequence is simple:

- For tonight's workshop, the reliable demo path is local Mission Canvas.
- OpenClaw on the VPS is real, but should not be treated as the primary inference/runtime dependency for tonight.
- Telegram bridge work is adjacent infrastructure and historical learning, not tonight's core path.

## What We Have Tried With OpenClaw

### 1. Research and architectural comparison

Files:

- [openclaw_vs_palette_analysis.md](/home/mical/fde/palette/research/openclaw_vs_palette_analysis.md)
- [OPENCLAW_RESEARCH_NOTES.md](/home/mical/fde/missioncanvas-site/OPENCLAW_RESEARCH_NOTES.md)
- [openclaw_application_prompt_missioncanvas_v1.0.md](/home/mical/fde/palette/docs/openclaw_application_prompt_missioncanvas_v1.0.md)
- [openclaw_application_prompt_missioncanvas_api_contract_v1.0.md](/home/mical/fde/palette/docs/openclaw_application_prompt_missioncanvas_api_contract_v1.0.md)

What this phase did:

- Compared Palette's convergence-first governance model to OpenClaw's runtime-first model.
- Identified OpenClaw as a candidate runtime and multi-channel shell around Palette.
- Defined the Mission Canvas contract as a structured policy interface rather than a generic chat UI.

### 2. Mission Canvas adapter build-out

Files:

- [server.mjs](/home/mical/fde/missioncanvas-site/server.mjs)
- [openclaw_adapter_core.mjs](/home/mical/fde/missioncanvas-site/openclaw_adapter_core.mjs)
- [adapter_contract_check.mjs](/home/mical/fde/missioncanvas-site/adapter_contract_check.mjs)
- [terminal_voice_bridge.mjs](/home/mical/fde/missioncanvas-site/terminal_voice_bridge.mjs)
- [OPENCLAW_ITERATION_LOG.md](/home/mical/fde/missioncanvas-site/OPENCLAW_ITERATION_LOG.md)
- [README.md](/home/mical/fde/missioncanvas-site/README.md)

What this phase did:

- Built a local API adapter exposing:
  - `GET /v1/missioncanvas/health`
  - `GET /v1/missioncanvas/capabilities`
  - `POST /v1/missioncanvas/route`
  - `POST /v1/missioncanvas/talk-stream`
  - `POST /v1/missioncanvas/confirm-one-way-door`
  - `POST /v1/missioncanvas/log-append`
- Added three upstream modes:
  - `missioncanvas`
  - `responses`
  - `chatcompletions`
- Added a terminal bridge to simulate voice-style interaction.
- Added local fallback routing so the system still works without a live OpenClaw upstream.

### 3. Planned voice/phone integration direction

File:

- [CODEX_RIME_INTEGRATION_BRIEF.md](/home/mical/fde/missioncanvas-site/CODEX_RIME_INTEGRATION_BRIEF.md)

What this phase aimed for:

- OpenClaw as the runtime/gateway
- ClawdTalk as the phone/voice connector
- Telnyx as telephony
- Rime as expressive TTS
- Mission Canvas as the governed planning layer

Intended ideal flow:

Phone call -> Telnyx / ClawdTalk -> OpenClaw -> Mission Canvas / Palette policy -> spoken structured result

### 4. VPS runtime investigation

What we verified on the Hostinger VPS:

- Host: `srv1390882`
- Container: `openclaw-fcup-openclaw-1`
- Image: `ghcr.io/hostinger/hvps-openclaw:latest`
- Published ports:
  - `18789`
  - `60233`

Container facts:

- OpenClaw is installed and running in Docker.
- The gateway token exists.
- `openclaw-gateway` is running.
- `gateway.http.endpoints.chatCompletions.enabled = true`
- `gateway.http.endpoints.responses.enabled = true`

Key runtime paths found in the container:

- `/data/.openclaw/openclaw.json`
- `/data/.openclaw/agents/main/...`

### 5. VPS failure analysis

What failed:

- Raw host-side `curl` to `127.0.0.1:18789/v1/...` reset the connection.
- Host-side `curl` to container IP `172.18.0.2:18789` could not connect.
- Mission Canvas could not be run directly on the VPS host because `node` was not installed on the host OS.

What worked:

- `curl` from inside the OpenClaw container to `127.0.0.1:18789/v1/responses` returned valid JSON.
- `curl` from inside the container to `127.0.0.1:18789/v1/chat/completions` returned valid JSON.

What the container returned:

- `402 budget 10 has been reached for company`

Interpretation:

- HTTP compatibility exists inside the container.
- Host-to-container access is not dependable in the current VPS setup.
- Even where the HTTP surface is reachable, upstream inference is budget-blocked.

## Current State

### Local machine

Status: working

Verified on 2026-03-17:

- `node adapter_contract_check.mjs` passes.
- `node server.mjs` starts successfully.
- `GET /v1/missioncanvas/health` returns `ok`.
- `POST /v1/missioncanvas/route` returns valid structured output.
- `POST /v1/missioncanvas/talk-stream` streams correctly.
- `POST /v1/missioncanvas/confirm-one-way-door` works.
- `node terminal_voice_bridge.mjs` works in test-transcript mode.

Current working mode:

- `local_fallback`

Meaning:

- Palette routing and governance are live.
- OpenClaw is not required for the core planning behavior.

### VPS

Status: partially working, not demo-reliable

What is live:

- OpenClaw container
- control UI HTML on `60233`
- OpenClaw gateway process

What is not reliable:

- host-side HTTP access to the OpenClaw compatibility endpoints
- upstream model completions through Nexos because of budget exhaustion
- Mission Canvas runtime on host due to missing `node`

## What Exists On Disk

### Mission Canvas / OpenClaw adapter

Folder:

- [/home/mical/fde/missioncanvas-site](/home/mical/fde/missioncanvas-site)

Key files:

- [server.mjs](/home/mical/fde/missioncanvas-site/server.mjs): Node adapter with proxy and fallback modes
- [openclaw_adapter_core.mjs](/home/mical/fde/missioncanvas-site/openclaw_adapter_core.mjs): local routing, validation, one-way-door detection
- [terminal_voice_bridge.mjs](/home/mical/fde/missioncanvas-site/terminal_voice_bridge.mjs): CLI voice-style test flow
- [adapter_contract_check.mjs](/home/mical/fde/missioncanvas-site/adapter_contract_check.mjs): deterministic verification
- [config.js](/home/mical/fde/missioncanvas-site/config.js): frontend API base config
- [index.html](/home/mical/fde/missioncanvas-site/index.html): browser UI
- [app.js](/home/mical/fde/missioncanvas-site/app.js): frontend logic
- [deploy/PRODUCTION_WIRING.md](/home/mical/fde/missioncanvas-site/deploy/PRODUCTION_WIRING.md): intended deployment wiring
- [.env.production](/home/mical/fde/missioncanvas-site/.env.production): production env sketch

### Palette-side OpenClaw docs

Files:

- [openclaw_application_prompt_missioncanvas_v1.0.md](/home/mical/fde/palette/docs/openclaw_application_prompt_missioncanvas_v1.0.md)
- [openclaw_application_prompt_missioncanvas_api_contract_v1.0.md](/home/mical/fde/palette/docs/openclaw_application_prompt_missioncanvas_api_contract_v1.0.md)
- [openclaw_vs_palette_analysis.md](/home/mical/fde/palette/research/openclaw_vs_palette_analysis.md)

### Telegram bridge system

Folder:

- [/home/mical/fde/palette/bridges/telegram](/home/mical/fde/palette/bridges/telegram)

Key files:

- [telegram_bridge.py](/home/mical/fde/palette/bridges/telegram/telegram_bridge.py): general Telegram bridge
- [rossi_bridge.py](/home/mical/fde/palette/bridges/telegram/rossi_bridge.py): Rossi-specific bridge
- [gap_bridge.py](/home/mical/fde/palette/bridges/telegram/gap_bridge.py): Gap/interview-related bridge
- [openai_bridge.py](/home/mical/fde/palette/bridges/telegram/openai_bridge.py): OpenAI-backed bridge variant
- [relay_consumer.py](/home/mical/fde/palette/bridges/telegram/relay_consumer.py): inbox consumer
- [outbox_deliver.py](/home/mical/fde/palette/bridges/telegram/outbox_deliver.py): outbound Telegram delivery
- [relay_store.py](/home/mical/fde/palette/bridges/telegram/relay_store.py): artifact storage helpers
- [relay_scaffold.py](/home/mical/fde/palette/bridges/telegram/relay_scaffold.py): per-implementation scaffold
- [relay_status.py](/home/mical/fde/palette/bridges/telegram/relay_status.py): status reporting
- [relay_publisher.py](/home/mical/fde/palette/bridges/telegram/relay_publisher.py): publishing path
- [approve_publish.py](/home/mical/fde/palette/bridges/telegram/approve_publish.py): explicit approval path

Systemd unit templates:

- [rossi-bridge.service](/home/mical/fde/palette/bridges/telegram/systemd/rossi-bridge.service)
- [rossi-outbox-deliver.service](/home/mical/fde/palette/bridges/telegram/systemd/rossi-outbox-deliver.service)
- [rossi-relay-consumer.service](/home/mical/fde/palette/bridges/telegram/systemd/rossi-relay-consumer.service)
- [lumen-interview-bridge.service](/home/mical/fde/palette/bridges/telegram/systemd/lumen-interview-bridge.service)

Supporting docs:

- [TELEGRAM_RELAY_V1.md](/home/mical/fde/palette/docs/TELEGRAM_RELAY_V1.md)
- [BOT_SERVICE_RUNBOOK.md](/home/mical/.codex/BOT_SERVICE_RUNBOOK.md)

## What The Telegram Bridge Is

The Telegram bridge is a constrained artifact relay layer, not direct shell access.

Core model:

- Telegram messages become file artifacts under `implementations/<impl-id>/telegram/`
- relay consumer processes inbox artifacts
- outbox deliverer sends approved replies back to Telegram
- provenance and idempotency are tracked
- no direct shell execution is allowed by default

This system is designed for safe asynchronous handoff, not for real-time voice execution.

It matters here because it represents a separate bridge pattern already present in Palette:

- file artifacts
- constrained execution
- explicit provenance
- service-level isolation

Those are useful architectural lessons for OpenClaw integration.

## How OpenClaw Was Intended To Be Used

The intended role for OpenClaw in this stack was:

- persistent runtime
- channel abstraction
- optional voice/phone ingress
- OpenAI-compatible HTTP proxy surface
- agent identity, sessions, memory, and multi-channel context

In that intended design:

- Mission Canvas would remain the governance/policy layer.
- OpenClaw would provide runtime and channel plumbing.
- ClawdTalk/Telnyx/Rime would provide the phone and voice experience.

## What OpenClaw Is Actually Doing Today

On the VPS:

- running as a Dockerized gateway
- configured with a `main` agent
- backed by Nexos provider configuration
- exposing a control UI and internal HTTP/WS surfaces

But not currently serving as a dependable outer runtime for Mission Canvas because:

- host networking/pathing is awkward
- Mission Canvas is not deployed there as a runnable host service
- upstream model budget is exhausted

## Tonight's Application

Event:

- ClawdTalk & Rime Workshop
- March 17, 2026
- goal: have something working by demo time

The clean application tonight is:

- run Mission Canvas locally
- use local fallback routing
- demonstrate governed planning, RIU selection, and one-way-door gating
- optionally use the terminal voice bridge for a voice-style interaction flow

Not recommended tonight:

- depending on VPS OpenClaw inference
- depending on Nexos-backed completions
- trying to finish ClawdTalk/Telnyx/Rime production wiring under time pressure

## Known-Good Commands

### Local Mission Canvas server

```bash
cd /home/mical/fde/missioncanvas-site
node adapter_contract_check.mjs
node server.mjs
```

### Local health check

```bash
curl -sS http://127.0.0.1:8787/v1/missioncanvas/health
```

### Local route test

```bash
curl -sS -X POST http://127.0.0.1:8787/v1/missioncanvas/route \
  -H 'Content-Type: application/json' \
  -d '{"input":{"objective":"I need a business plan for my store","context":"small retail","desired_outcome":"30-day plan","constraints":"small budget","risk_posture":"medium"}}'
```

### Local terminal voice-style flow

```bash
cd /home/mical/fde/missioncanvas-site
MISSIONCANVAS_TEST_TRANSCRIPT="I need a business plan for my store" node terminal_voice_bridge.mjs
```

### One-way-door test

```bash
curl -sS -X POST http://127.0.0.1:8787/v1/missioncanvas/route \
  -H 'Content-Type: application/json' \
  -d '{"input":{"objective":"Delete the database and production deploy immediately","context":"legacy migration","desired_outcome":"finish tonight","constraints":"no rollback","risk_posture":"high"}}'
```

Expected:

- `status: needs_confirmation`

## What Broke Or Proved Fragile

### VPS host runtime

- `node` not installed on host
- Mission Canvas server cannot be started directly on host without additional setup

### OpenClaw host integration

- host-side HTTP requests to `127.0.0.1:18789` reset
- host-side HTTP requests to container IP did not connect
- container-local HTTP works, which means the issue is not simply "endpoint missing"

### Provider dependency

- OpenClaw container returns:
  - `402 budget 10 has been reached for company`

This means the model backend is not usable right now even if networking were fixed.

## Lessons Learned

1. Local fallback is not just a backup. It is the most reliable product path currently available.
2. OpenClaw should be treated as an outer runtime shell, not the authoritative decision engine.
3. A config file saying HTTP is enabled is not enough; host-reachable proof matters more than config claims.
4. Container-self success is not deployment success.
5. Provider budget health must be treated as a first-class readiness check.
6. Telegram bridge and OpenClaw are separate systems with different trust and execution models.

## Recommended Next Improvements

1. Add a single preflight script for Mission Canvas + OpenClaw:
   - local adapter health
   - upstream reachability
   - auth validity
   - model response sanity
   - fallback/proxy mode status

2. Make `local_fallback` an explicit first-class supported mode in docs and startup logs.

3. Create a small "OpenClaw degraded mode" contract:
   - `upstream_unavailable`
   - `provider_budget_exhausted`
   - `host_reachability_failed`

4. If VPS deployment remains important:
   - install host `node` or containerize Mission Canvas separately
   - stop assuming host access to container-local OpenClaw HTTP works
   - test the exact host path before any event

5. Keep Telegram bridge isolated by service, env, and impl-id as documented in [BOT_SERVICE_RUNBOOK.md](/home/mical/.codex/BOT_SERVICE_RUNBOOK.md).

## Bottom Line

OpenClaw is real in this system, but it is not the path that is actually carrying tonight's demo confidence.

The system that is ready today is:

- Palette policy
- Mission Canvas adapter
- local fallback routing
- terminal voice-style flow
- one-way-door gating

That is enough to show a governed planning system working live.
