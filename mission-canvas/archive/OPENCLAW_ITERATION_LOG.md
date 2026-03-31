# OpenClaw Integration Iteration Log (MissionCanvas)

Date: 2026-02-17
Scope: `missioncanvas-site`
Method: Para (monitor) -> Raptor (fix) -> Anky (validate)

## Iteration 1

Para findings:
- Web form routed correctly but lacked source visibility.
- One-way-door state visible but no explicit confirm action.

Raptor fixes:
- Added response `source` and `status` rendering.
- Added explicit `Confirm ONE-WAY DOOR` button.
- Added confirmation endpoint invocation in frontend.

Anky validation:
- UI now surfaces routing source and policy state.
- One-way-door confirmation action available and bounded.

## Iteration 2

Para findings:
- Adapter logic was monolithic and hard to test.
- No independent contract checks.

Raptor fixes:
- Extracted reusable core logic to `openclaw_adapter_core.mjs`.
- Added `adapter_contract_check.mjs` for deterministic checks.

Anky validation:
- Contract tests pass for:
  - validation errors
  - business-plan routing
  - one-way-door detection
  - response shape completeness

## Iteration 3

Para findings:
- Upstream compatibility was too narrow (custom route endpoint only).
- No direct terminal microphone path.

Raptor fixes:
- Added upstream modes in `server.mjs`:
  - `missioncanvas`
  - `responses`
  - `chatcompletions`
- Added health/capability endpoints.
- Added terminal bridge: `terminal_voice_bridge.mjs`.

Anky validation:
- Node syntax checks pass.
- Contract tests pass.
- Terminal bridge supports:
  - microphone capture where available
  - manual transcript fallback
  - route call + brief output + optional TTS

## Residual Risks

1. Browser speech recognition varies by browser/device.
2. Terminal mic depends on local tools (`arecord` on Linux, `sox` on macOS).
3. Upstream OpenClaw gateway payload semantics may vary by deployment.

## Iteration 4 (Research-Informed Hardening)

Para findings:
- Official OpenClaw ecosystem supports multiple integration surfaces (custom route + OpenAI-compatible HTTP + talk mode), so adapter should support multiple upstream modes.
- Voice use should not depend exclusively on browser context.

Raptor fixes:
- Added upstream mode support in adapter server:
  - `missioncanvas`
  - `responses`
  - `chatcompletions`
- Added terminal voice bridge with local fallback:
  - `terminal_voice_bridge.mjs`
- Added health/capability endpoints and explicit source metadata.

Anky validation:
- Syntax checks pass for server/frontend/core/terminal bridge.
- Contract checks pass.
- Noninteractive terminal bridge simulation returns routed brief successfully.

## Iteration 5 (Streaming + Decision Logging)

Para findings:
- Talk mode needed incremental UX, not just final response blocks.
- Decision payload existed but no write path into persistent log.

Raptor fixes:
- Added `POST /v1/missioncanvas/talk-stream` (NDJSON chunks + final payload).
- Added `POST /v1/missioncanvas/log-append` (env-gated file append).
- Added frontend controls:
  - Run Streaming Response
  - Append Decision Log
  - Auto-log toggle after route

Anky validation:
- Adapter contract tests still pass.
- Syntax checks pass.
- One-way-door behavior remains intact after streaming/logging additions.

## Iteration 6 (Live Wiring + Pilot Runbook)

Para findings:
- Needed explicit production wiring artifacts and executable pilot path.
- Frontend needed environment-configurable API base without code edits.

Raptor fixes:
- Added runtime config file: `config.js`.
- Added production wiring runbook: `deploy/PRODUCTION_WIRING.md`.
- Added pilot payload + runner:
  - `pilot/rossi_payload.json`
  - `scripts/run_rossi_pilot.mjs`
- Added env template: `.env.production.example`.

Anky validation:
- Script syntax checks pass.
- Offline pilot run produces brief + report artifacts.
- Adapter contract checks continue to pass.

## Next Iteration Targets

1. Add persistent conversation/session memory by `session_id`.
2. Add structured decision-log append endpoint.
3. Add optional streaming responses for voice talk mode.
