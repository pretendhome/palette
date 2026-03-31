# Mission Canvas

Voice-first execution platform for [Palette](https://github.com/pretendhome/palette). Speak a question, get structured intelligence back — routing, coaching, workspace health, and governed decisions.

---

## Architecture

```
  Voice / Text Input
        ↓
  ┌─────────────────────┐
  │   Unified Voice UI   │   index.html — conversation flow,
  │   (Browser)          │   FFT visualizer, TTS, text fallback
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │   Server (Node.js)   │   server.mjs — 10 API endpoints
  │                      │   Wire contract, convergence chain,
  │                      │   coaching, workspace state, OWD gates
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │   Palette            │   Intelligence layer — taxonomy,
  │   (Intelligence)     │   knowledge library, service routing
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │   Peers Broker       │   Governed message bus connecting
  │   (Message Bus)      │   Claude, Kiro, Codex, Mistral, Gemini
  └─────────────────────┘
```

## Quick Start

```bash
node server.mjs
# → http://localhost:8787
```

## Voice UI

The unified voice interface (`index.html`) merges work from three agents (Claude, Kiro, Codex) via a multi-agent design competition:

- **Conversation flow** — Hero orb with 48-bar FFT frequency visualization transitions to chat bubbles
- **Wire contract** — Full routing payload with session, user, policy, and runtime fields
- **Dual-endpoint first message** — `/who-are-you` + `/route` + `/workspace-welcome` in parallel
- **Coaching hints** — Indigo panels for coaching packets where `depth === "full"`
- **Workspace health** — Status line showing health score and items needing attention
- **Offline fallback** — Hardcoded identity answer when backend is unreachable
- **Debug mode** — `?debug=1` or double-tap header to show broker relay metadata
- **TTS** — Auto-speaks first response, manual Speak button on subsequent messages
- **Text input** — Auto-resizing textarea with Enter-to-send

## API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/v1/missioncanvas/health` | Connection check |
| GET | `/v1/missioncanvas/capabilities` | Supported features |
| POST | `/v1/missioncanvas/route` | Primary routing with convergence chain |
| POST | `/v1/missioncanvas/talk-stream` | NDJSON streaming route |
| POST | `/v1/missioncanvas/who-are-you` | Identity + peers broker relay |
| POST | `/v1/missioncanvas/workspace-welcome` | Health, nudges, workspace context |
| POST | `/v1/missioncanvas/coach` | Coaching response for learner lens |
| POST | `/v1/missioncanvas/verify-mastery` | Concept mastery verification |
| POST | `/v1/missioncanvas/confirm-one-way-door` | OWD approval/rejection gate |
| POST | `/v1/missioncanvas/log-append` | Decision log persistence |

## Wire Contract

Route requests use the full Palette wire contract:

```json
{
  "request_id": "voice-1711929600000",
  "timestamp": "2026-03-31T12:00:00.000Z",
  "session_id": "voice-session-oil-investor",
  "workspace_id": "oil-investor",
  "user": { "id": "voice-user", "role": "owner" },
  "input": { "objective": "...", "risk_posture": "medium" },
  "policy": {
    "enforce_convergence": true,
    "enforce_one_way_gate": true,
    "max_selected_rius": 5
  },
  "runtime": {
    "mode": "planning",
    "allow_execution": false
  }
}
```

## Project Structure

```
missioncanvas-site/
├── index.html                    # Unified voice UI
├── setup.html                    # Workspace onboarding flow
├── for-business-owners.html      # Business owner landing page
├── server.mjs                    # API server (10 endpoints)
├── openclaw_adapter_core.mjs     # Route/validation core (121 RIUs)
├── convergence_chain.mjs         # Workspace state, health, nudges
├── workspace_coaching.mjs        # Learner lens coaching + mastery
├── flywheel_feedback.mjs         # KL candidate generation, decision records
├── data_boundary.mjs             # PII validation (14 patterns, 3 severity levels)
├── mcp_server.mjs                # Local MCP server
├── mcp_server_remote.mjs         # Remote MCP server
├── competitions/                 # Multi-agent design competitions
│   └── north-star-2026-03-30/    # First competition: flywheel return path
├── workspaces/                   # Workspace YAML state files
├── archive/                      # Superseded UI entries
└── stress_test*.mjs              # Contract and load test suites
```

## Competitions

Multi-agent design competitions where Claude, Kiro, Codex, Mistral, and Gemini tackle architectural challenges. See [competitions/README.md](competitions/README.md).

## Workspace Engine

Each workspace tracks:
- **Known facts** — What the system knows about the user's situation
- **Missing facts** — What it still needs to ask
- **Decisions** — Tracked with one-way-door classification
- **Health score** — Calculated from state completeness (0-100)
- **Nudges** — Actionable next steps generated from gaps

## Deployment

```bash
# Local
node server.mjs

# With upstream proxy
OPENCLAW_BASE_URL="https://your-gateway" \
OPENCLAW_API_KEY="token" \
node server.mjs

# VPS with Cloudflare tunnel
./start.sh
```

## Validation

```bash
node stress_test.mjs              # 41-point contract + load test
node stress_test_convergence.mjs  # Convergence chain scenarios
node stress_test_enablement_hook.mjs  # Coaching integration
```

---

*Part of the [Palette](https://github.com/pretendhome/palette) intelligence system. Voice in, governed action out.*
