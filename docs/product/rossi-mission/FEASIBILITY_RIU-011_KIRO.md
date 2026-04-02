# RIU-011 Feasibility Assessment: Local Palette Prompt Runner

**Author**: kiro.design
**Date**: 2026-03-28
**Assignment**: Can we build `/v1/missioncanvas/route` as a local Palette prompt runner WITHOUT depending on external OpenClaw?
**Status**: COMPLETE

---

## Verdict: YES — and it's mostly already built.

The existing `missioncanvas-site/` already implements a local prompt runner that does NOT depend on external OpenClaw. The dependency is optional and the local path is the default.

---

## Evidence

### What already exists (missioncanvas-site/)

1. **server.mjs** (348 lines) — HTTP server on port 8787 with `/v1/missioncanvas/route` endpoint already implemented
2. **openclaw_adapter_core.mjs** (280 lines) — Local routing logic with:
   - 5 RIU route definitions (keyword-matched)
   - One-way-door term detection
   - Request validation
   - `localRouteResponse()` function that returns full contract-compliant responses WITHOUT any external call
3. **app.js** (680 lines) — Frontend with form fields, fetch calls, response rendering
4. **index.html** — Working UI with hero prompt and ask flow

### How the local path works today

```
UI form → POST /v1/missioncanvas/route → server.mjs
  → validateRoutePayload()
  → localRouteResponse()  ← NO external dependency
  → returns: convergence brief, RIU candidates, agent map, OWD status, action brief
```

The server has an `OPENCLAW_UPSTREAM_MODE` env var. When set to `'missioncanvas'` (the default), it uses the local adapter. External OpenClaw is only called if explicitly configured with `OPENCLAW_BASE_URL` and a different mode.

### What the OpenClaw API contract describes vs what exists

| Contract requirement | Local implementation status |
|---|---|
| `POST /v1/missioncanvas/route` | ✅ Exists in server.mjs |
| Request schema (objective, context, outcome, constraints, risk_posture) | ✅ Validated in openclaw_adapter_core.mjs |
| Response: convergence brief | ✅ Generated locally |
| Response: candidate RIUs | ✅ Keyword-matched from 5 routes |
| Response: agent map | ✅ Hardcoded per route |
| Response: one-way-door detection | ✅ Term-matching against OWD_TERMS list |
| Response: action brief markdown | ✅ Generated locally |
| `POST /v1/missioncanvas/confirm-one-way-door` | ❌ Not implemented |
| Knowledge gap detection | ❌ Not implemented |
| Decision log append | ⚠️ Stubbed (env var path, append logic exists) |
| Full Palette agent orchestration | ❌ Routes to static agent names, not live agents |

---

## Gap Analysis: What's missing to make this a real Palette prompt runner

### Gap 1: Static routing → Live agent routing
**Current**: `localRouteResponse()` returns hardcoded agent names ("Rex", "Argy") and static action text.
**Needed**: Route through actual Palette resolver → taxonomy → agent assignment.
**Effort**: Medium. The SDK has `PaletteContext.load()` and `GraphQuery` — wire them into the adapter.
**Classification**: 🔄 TWO-WAY DOOR

### Gap 2: 5 keyword routes → 121 RIU taxonomy
**Current**: 5 routes matched by keyword arrays.
**Needed**: Full taxonomy matching using trigger_signals from all 121 RIUs.
**Effort**: Medium. Load `palette_taxonomy_v1.3.yaml`, match against trigger_signals.
**Classification**: 🔄 TWO-WAY DOOR

### Gap 3: No confirmation endpoint
**Current**: OWD detection works but there's no `/confirm-one-way-door` endpoint.
**Needed**: Implement the confirmation flow per the API contract.
**Effort**: Small. Add endpoint, track pending confirmations in memory or SQLite.
**Classification**: 🚨 ONE-WAY DOOR (this gates irreversible actions)

### Gap 4: No fetch_signals integration
**Current**: Canvas UI shows hardcoded prototype data.
**Needed**: Real local file parsing with PII scrubbing (Gemini's task per relay plan).
**Effort**: Medium-Large. PDF/CSV parsing + PII regex + path allowlist per Claude's security audit.
**Classification**: 🚨 ONE-WAY DOOR (PII policy must be approved first)

### Gap 5: No knowledge library integration
**Current**: Responses don't reference KL entries.
**Needed**: Wire KL lookups into response generation for evidence-backed recommendations.
**Effort**: Small-Medium. Load KL YAML, match by related_rius field.
**Classification**: 🔄 TWO-WAY DOOR

---

## Implementation Sketch

### Phase 1: Wire Palette SDK into existing server (no new files)

Modify `openclaw_adapter_core.mjs` → `palette_local_router.mjs`:

```
1. On startup: load taxonomy YAML, load KL YAML
2. On request: extract trigger signals from input.objective + input.context
3. Match against all 121 RIUs (not just 5 keyword routes)
4. Select top 1-5 by match strength
5. Map to agent types from RIU definitions
6. Check OWD conditions (keep existing term matching + add RIU reversibility field)
7. Pull relevant KL entries for selected RIUs
8. Return full contract-compliant response
```

### Phase 2: Add confirmation endpoint

```
POST /v1/missioncanvas/confirm-one-way-door
- Store pending OWD decisions in Map keyed by request_id
- On confirm: mark approved, return next_step
- On reject: return to convergence
```

### Phase 3: Connect to live agents (future — depends on orchestrator)

Replace static agent names with actual agent dispatch via peers bus. This is the "ghost in the machine" phase — not needed for v1.

---

## Constraints (from security audit)

- Zero external network access from the local endpoint
- Path allowlist for any file access
- PII scrubbing before any data enters bus/UI/logs
- textContent not innerHTML for rendering
- All OWD actions gated for human approval

---

## Recommendation

Don't build a new system. Evolve `missioncanvas-site/`. It already has:
- Working server with the right endpoint
- Working UI with form fields
- Working local routing (just needs to be expanded)
- Working OWD detection (just needs confirmation endpoint)
- PM2 process management (already configured)

The path is: expand the 5-route local adapter to use the full 120-RIU taxonomy, add the confirmation endpoint, and wire in KL lookups. That gets us a working local Palette prompt runner with zero external dependencies.

Gemini's canvas skeleton at `peers/adapters/gemini-cli/canvas/` (45-line HTML with hardcoded data) should be abandoned in favor of the existing `missioncanvas-site/` which is 10x more complete.

---

**Deliverable**: This document. Posted to `all` channel.
