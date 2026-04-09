# MissionCanvas V0.2 — Full Build Report

**Author**: claude.analysis (Claude Code)
**Date**: 2026-03-29
**Status**: V0.2 SHIPPED — all features built, tested, and running at localhost:8787
**Pick up from here**: This report is the complete context for the next session. Read this first.

---

## What MissionCanvas Is

MissionCanvas is a voice-first planning interface that sits in front of the Palette routing engine. A user speaks (or types) a natural language mission — "I run a local store, I need a business plan and grant strategy in 30 days with low budget" — and Canvas translates it into structured fields, scores convergence, routes through 121 RIUs, and returns an action brief with agents, artifacts, and one-way-door detection.

It is NOT an LLM wrapper. There is no LLM in the loop. All routing is deterministic — signal matching against the Palette taxonomy, keyword scoring, and RIU-to-knowledge-library lookup. The intelligence is in the taxonomy (121 RIUs), the knowledge library (162 entries loaded), and the convergence protocol.

**Location**: `/home/mical/fde/missioncanvas-site/`

---

## What V0.1 Was (baseline before this session)

V0.1 was request-centric. Every interaction was independent:
1. User speaks or types a mission
2. Canvas translates natural language → structured fields (objective, context, desired outcome, constraints)
3. Server routes through 121 RIUs using trigger signal matching
4. Returns a single action brief with RIU, agents, artifacts, one-way-door detection
5. User can speak the brief, copy it, append to decision log, refine and reroute

V0.1 features already working:
- Voice input (Web Speech API, continuous recognition)
- Natural language translation layer (sentence pattern matching → structured fields)
- 5 persona patterns (Game Builder, Business Owner, Education, Job Seeker, Enterprise AI Operator) with default field injection
- 3 preset mission chips for quick start
- Full Palette routing (121 RIUs, signal scoring, knowledge library lookup)
- One-way-door detection and human confirmation flow
- Decision log append (server-side, timestamped JSONL)
- Streaming route mode (SSE-style chunked responses)
- Session tracking (server-side, 24h TTL, idempotency cache)
- Action brief with markdown rendering, TTS readback, clipboard copy
- Prompt quality checks (5 criteria evaluated after each translation)

**Files at V0.1**:
- `server.mjs` — ~550 lines, Node.js HTTP server
- `app.js` — ~550 lines, client-side IIFE
- `index.html` — ~190 lines
- `styles.css` — ~500 lines
- `openclaw_adapter_core.mjs` — ~260 lines, routing engine

---

## What V0.2 Added (this session)

V0.2 transformed Canvas from request-centric to session-aware. The user's journey now has three phases (explore → converge → commit), persistent state across page reloads, and a live convergence meter that responds to every keystroke.

### Feature 1: Convergence Scoring Engine

**Server** (`openclaw_adapter_core.mjs:180-224`):
```
computeConvergenceScore(input, hasPersona)
  objective:       +40
  desired_outcome:  +30
  context:          +15
  constraints:      +10
  persona:           +5
  ────────────────────
  max:             100
  mode: <50 = explore, >=50 = converge
```

The function returns `{ score, mode, gaps, suggestedQuestions }`. Gaps are human-readable ("No desired outcome — what does success look like?"). Suggested questions are generated only in explore mode and tuned to what's missing.

This scoring is injected into every route response (`localRouteResponse`). The response now includes: `mode`, `convergence_score`, `convergence_gaps`, `suggested_questions`, and in explore mode, `route_options` (all 5 candidates with mini-briefs, not just the top 1).

**Client** (`app.js:261-334`):
`computeConvergenceLocal(structured)` mirrors the server formula exactly — same weights, same thresholds. `updateLiveConvergence()` is called on every `input` event on all 4 structured fields plus on persona selection. It updates:
- The meter bar (width % + color class)
- The score label ("EXPLORE 42/100" or "CONVERGE 85/100")
- Field-level hints ("Add Objective (+40) to move toward CONVERGE")

The client and server scores will always agree because they use identical logic. The client score gives instant feedback; the server score is authoritative.

### Feature 2: UX Modes (Explore / Converge / Commit)

**Explore** (score < 50):
- Server returns all 5 candidate RIUs with mini-briefs and match signals
- Client renders suggested questions (clickable → pre-fills followup input)
- Client renders route option cards (clickable → pre-fills objective with "I want to focus on: [RIU name]")
- Mode badge shows blue "EXPLORE (42/100)"
- Commit button hidden — you cannot commit in explore mode

**Converge** (score 50-100, not committed):
- Server returns convergence gaps and knowledge gaps
- Client renders gap checklist ("Fill these gaps to strengthen your mission")
- Client renders knowledge gaps if any RIUs lack KL coverage
- Mode badge shows green "CONVERGE (85/100)"
- Commit button appears when score >= 70

**Commit** (explicit user action):
- User clicks "Commit to this route" → POST `/v1/missioncanvas/commit`
- Server validates session is in converge mode (blocks explore → commit)
- Server locks route for session: `{ riu_id, name, committed_at }`
- All subsequent routes include committed route in context
- Client shows amber banner: "COMMITTED — RIU-109 Business Planning | Locked at 2026-03-29T14:22"
- Uncommit button appears → POST `/v1/missioncanvas/uncommit` → back to converge

**Server endpoints**:
- `POST /v1/missioncanvas/commit` (`server.mjs:488-533`) — locks route, sets mode to commit
- `POST /v1/missioncanvas/uncommit` (`server.mjs:536-559`) — clears lock, returns to converge
- Both endpoints validate session existence and current mode

### Feature 3: Live Convergence Meter

**HTML** (`index.html:130-136`):
```html
<div class="live-convergence">
  <div class="live-meter-track">
    <div id="liveMeterFill" class="live-meter-fill" style="width:0%"></div>
  </div>
  <span id="liveScore" class="live-score">EXPLORE 0/100</span>
  <p id="liveHint" class="live-hint">Fill in fields to build convergence.</p>
</div>
```

**CSS** (`styles.css`):
- `.live-meter-track` — 8px gray track bar, full width
- `.live-meter-fill` — animated width transition (0.3s ease), color changes by mode
- `.mode-explore` — blue (`#3b82f6`)
- `.mode-converge` — green (`#22c55e`)
- `.mode-commit` — amber (`#f59e0b`)

**Behavior**: User types "I need a business plan" → meter jumps to 40% (objective filled). Types "profitable store within 6 months" in desired outcome → jumps to 70%. Selects Business Owner persona → 75%. Adds context → 90%. Adds constraints → 100%. Each keystroke triggers `updateLiveConvergence()` via `input` event listeners wired in `initEvents()` at `app.js:1048-1052`.

### Feature 4: Client-Side Project State (localStorage)

**Key**: `missioncanvas_project_state`

**Schema**:
```json
{
  "id": "session-1711720800000",
  "created_at": "2026-03-29T12:00:00.000Z",
  "known_facts": ["Routed to RIU-109 (Business Planning)", ...],
  "route_history": [
    { "riu_id": "RIU-109", "name": "Business Planning", "mode": "converge", "score": 85, "timestamp": "..." }
  ],
  "decisions_made": [
    { "type": "commit", "riu_id": "RIU-109", "status": "committed", "timestamp": "..." }
  ],
  "convergence_high_water": 85,
  "last_mode": "converge",
  "last_updated": "2026-03-29T14:22:00.000Z",
  "persona": "rossi"
}
```

**Functions** (`app.js:31-97`):
- `loadProjectState()` — reads + parses from localStorage
- `saveProjectState(update)` — merges incremental updates (new fact, route, decision, score)
- `getProjectSummary()` — returns rollup stats
- `clearProjectState()` — removes from localStorage

**Injection into routing** (`app.js:519-530`):
`buildProjectStatePayload()` extracts `known_facts`, `missing_evidence`, `open_decisions`, `blocked_actions` from localStorage and sends with every route request.

**Server-side injection** (`server.mjs`, route handler):
When `payload.project_state` is present, the server concatenates it into `payload.input.context` as a `## Project State` section. This means the routing engine considers project history when matching RIUs — a user who has already explored grants will get different signal weights than a first-time user.

### Feature 5: Enhanced Check-In Panel

**On page load** (`app.js:1117-1206`):
If localStorage has project state with at least 1 route, a check-in panel appears:

```
Welcome back
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Last active   │ Routes       │ Convergence  │ Last mode    │
│ 3 hours ago   │ explored: 7  │ high: 85/100 │ CONVERGE     │
└──────────────┴──────────────┴──────────────┴──────────────┘
Last route: RIU-109 Business Planning (score 85, converge)

[Continue where I left off]  [Start fresh]
```

"Continue" restores persona and dismisses. "Start fresh" calls `clearProjectState()`.

### Feature 6: Queryable Project State

**UI** (`index.html:201-208`):
A collapsible panel at the bottom of the result section. Input field + Query button. Toggle with "Check my progress" button.

**Query engine** (`app.js:1327-1417`):
Handles natural language queries against localStorage:
- `progress` / `status` / `how` → full project summary + contextual suggestion
- `gaps` / `blocks` / `stuck` → convergence gaps + knowledge gaps from last route
- `decisions` / `owd` → decision history with timestamps
- `routes` / `history` → chronological route list with scores and modes
- `facts` / `know` → all known facts
- Anything else → help text listing available queries

Also exposed as `window.queryProjectState(question)` for console access.

### Feature 7: Explore Nudge

**Logic** (`app.js:1208-1224`):
After 5+ consecutive routes in explore mode, a yellow nudge appears at the top of mode content: "You've explored 7 routes. Would narrowing to a specific outcome help? Try adding a desired outcome above."

Counter resets when mode changes to converge. This prevents users from looping indefinitely in explore without realizing they need to add more detail.

### Feature 8: Anonymous Feedback Pipeline

**Trigger** (`app.js:1230-1324`):
After 5+ routes AND convergence high water >= 60, on the next route the feedback offer appears:

> You've been making progress! Would you like to share anonymous usage data to help us improve MissionCanvas?
> We collect: routes explored, convergence scores, persona used, and gaps filled. No personal data, text input, or identifying information.
> [Share anonymous feedback]  [Not now]  [Don't ask again]

**Payload** (no PII):
```json
{
  "routes_explored": 7,
  "convergence_high_water": 85,
  "persona": "rossi",
  "decisions_made": 2,
  "modes_used": { "explore": 3, "converge": 4 },
  "avg_score": 62,
  "rius_explored": 4
}
```

**Server** (`server.mjs:649-671`):
POST `/v1/missioncanvas/anonymous-feedback` — logs to trace, persists to `anonymous_feedback.jsonl`. Best-effort, no failure visible to user.

**Opt-out**: "Don't ask again" sets `localStorage.missioncanvas_feedback_offered = "never"` — permanent per-device opt-out.

### Feature 9: Committed Route Context Injection

When a route is committed, the server injects it into all subsequent route requests:
```
server.mjs route handler:
if (session.committed_route) {
  payload.input.context += '\n\n## Committed Route\n' +
    'This session is committed to ' + session.committed_route.riu_id + '...';
}
```

This means the routing engine biases toward the committed RIU's domain — reinforcing the user's decision rather than wandering to new territory.

---

## Architecture After V0.2

### File Sizes
| File | Lines | Role |
|------|-------|------|
| `server.mjs` | 716 | HTTP server, routing proxy, session management, commit/uncommit, feedback |
| `app.js` | 1,485 | Client-side IIFE — voice, translation, rendering, project state, convergence, queries |
| `openclaw_adapter_core.mjs` | 339 | Routing engine — RIU scoring, knowledge lookup, convergence scoring, brief generation |
| `index.html` | 223 | Semantic HTML — panels, forms, meters, query panel |
| `styles.css` | 714 | Full styling — grid layout, mode colors, meters, cards, banners |
| **Total** | **3,477** | |

### API Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/v1/missioncanvas/health` | Health check |
| GET | `/v1/missioncanvas/capabilities` | Feature flags |
| POST | `/v1/missioncanvas/route` | Main routing (+ convergence scoring, mode, project state injection) |
| POST | `/v1/missioncanvas/talk-stream` | Streaming route (SSE-style) |
| POST | `/v1/missioncanvas/commit` | Lock route for session |
| POST | `/v1/missioncanvas/uncommit` | Unlock route, return to converge |
| POST | `/v1/missioncanvas/confirm-one-way-door` | OWD human confirmation |
| POST | `/v1/missioncanvas/log-append` | Decision log entry |
| POST | `/v1/missioncanvas/anonymous-feedback` | Anonymous usage telemetry |
| POST | `/v1/missioncanvas/fetch-signals` | File signal extraction |
| GET | `/*` | Static file serving (index.html, app.js, styles.css, etc.) |

### Data Flow
```
User speaks/types
  → Web Speech API (continuous, interim results)
  → transcriptInput textarea
  → translateNaturalInput() — sentence pattern matching
  → Structured fields (objective, context, desired_outcome, constraints)
  → [LIVE] computeConvergenceLocal() updates meter on every keystroke
  → User clicks "Route Mission"
  → fetchRoute() sends POST /v1/missioncanvas/route with:
      - structured input
      - persona_id
      - project_state (from localStorage)
      - session_id
  → Server:
      - Injects project_state into context
      - Injects committed_route into context (if committed)
      - Calls localRouteResponse() which:
          - Scores all 121 RIUs via pickRoutes()
          - Looks up knowledge library entries for matched RIUs
          - Detects one-way doors
          - Computes convergence score and mode
          - Generates action brief markdown
      - Returns full response with mode, score, gaps, suggestions, candidates
  → Client renderResponse():
      - Updates mode badge (EXPLORE/CONVERGE/COMMIT)
      - Renders mode-specific content (questions/gaps/cards)
      - Shows/hides commit button
      - Saves to localStorage project state
      - Checks explore nudge (5+ explore routes)
      - Checks feedback offer (5+ routes, score 60+)
```

### State Architecture
```
┌─────────────────────────────────────┐
│ Client (browser)                     │
│                                      │
│  localStorage:                       │
│    missioncanvas_project_state       │
│      → known_facts[]                 │
│      → route_history[]               │
│      → decisions_made[]              │
│      → convergence_high_water        │
│      → persona, last_mode            │
│                                      │
│  sessionStorage:                     │
│    missioncanvas_feedback_offered    │
│                                      │
│  In-memory (STATE object):           │
│    → currentMode                     │
│    → convergenceScore                │
│    → committedRoute                  │
│    → lastResponse, lastBrief, etc.   │
└─────────────┬───────────────────────┘
              │ HTTP POST
              ▼
┌─────────────────────────────────────┐
│ Server (Node.js, in-memory)          │
│                                      │
│  sessionStore (Map):                 │
│    session_id → {                    │
│      history[], mode_history[],      │
│      current_mode, committed_route,  │
│      last_active                     │
│    }                                 │
│  TTL: 24h                            │
│                                      │
│  pendingOWD (Map):                   │
│    request_id → { decisions, status }│
│  TTL: 1h                             │
│                                      │
│  processedRequests (Map):            │
│    request_id → { result, timestamp }│
│  TTL: 1h (idempotency)              │
│                                      │
│  anonymous_feedback.jsonl (file)     │
└─────────────────────────────────────┘
```

---

## How We Got Here — Session Timeline

### Phase 0: Design Specs (Track B completion)

Three design specs were needed before V0.2 could start:
1. **UX Modes Spec** (`palette/projects/rossi-mission/ux_modes_spec.md`) — authored by Claude
2. **Project State Spec** (`palette/projects/rossi-mission/project_state_spec.md`) — authored by Kiro
3. **Decision Board Spec** (`palette/projects/rossi-mission/decision_board_spec.md`) — originally assigned to Mistral, reassigned to Claude when Mistral fell behind

All three specs were completed. A design review request was posted to the Palette Peers bus (HTTP broker at localhost:7899) with `requires_ack: true` for Kiro, Codex, and Gemini.

**Rossi bootstrap**: Extracted real data from the Rossi bridge system prompt, deliverables, and decision log into `palette/projects/rossi-mission/project_state.yaml` — 189 lines, 16 known facts, 5 missing evidence items, 3 open decisions, 3 blocked actions, 5 known unknowns, 6 resolved one-way-door decisions.

### Phase 1: Architecture Decisions (from the operator)

The operator reviewed the specs and made 4 critical decisions:

1. **UX Modes**: Approved as designed (explore / converge / commit)
2. **Project State**: Client-side (localStorage), NOT server-side YAML — "remember on the local device of the user"
3. **Decision Board**: Stored and queryable, NOT a permanent visual panel — "that sounds like something waiting to get wrong"
4. **Build ownership**: Claude builds everything; pull crew in only when justified

These decisions are recorded in `~/.claude/projects/-home-mical/memory/project_v02_decisions.md`.

### Phase 2: Build — Convergence Engine + UX Modes + Meter

- Added `computeConvergenceScore()` to `openclaw_adapter_core.mjs`
- Wired scoring into `localRouteResponse()` return payload
- Added mode, score, gaps, suggestions, and route_options to route response
- Built client-side `computeConvergenceLocal()` and `updateLiveConvergence()`
- Added live meter HTML, CSS, and `input` event listeners
- Built `renderModeContent()` for explore questions/cards and converge gaps
- Added mode badge rendering in `renderResponse()`
- Added server session mode tracking (`mode_history`, `current_mode`)

### Phase 3: Build — Client Project State + Check-In + Query

- Built localStorage CRUD: `loadProjectState()`, `saveProjectState()`, `getProjectSummary()`, `clearProjectState()`
- Wired `saveProjectState()` into `renderResponse()` (saves after every route)
- Built `checkProjectState()` for page-load check-in panel with stat cards
- Built `renderProjectStateQuery()` with 5 query categories
- Added query panel HTML and wired button + Enter key
- Built `checkExploreNudge()` for the "you've been exploring a while" message
- Built anonymous feedback: `checkFeedbackOffer()`, `sendAnonymousFeedback()`, server endpoint

### Phase 4: Build — Commit Mode + Project State Injection

- Built `commitRoute()` and `uncommitRoute()` in client
- Built `/v1/missioncanvas/commit` and `/v1/missioncanvas/uncommit` server endpoints
- Added explore-mode guard (cannot commit in explore)
- Built `renderCommitBanner()` for amber locked-route banner
- Built `buildProjectStatePayload()` for client → server project state injection
- Added server-side context injection for project_state and committed_route
- Added `commit_mode: true, project_state_injection: true` to capabilities

### Testing

7 end-to-end tests, all passing:

1. **Health endpoint** — confirms `commit_mode` and `project_state_injection` in capabilities
2. **Route with project state injection** — sends 3 facts, 1 missing evidence, 1 open decision; verifies they appear in routing context
3. **Commit to route** — locks RIU-109, session mode → commit
4. **Route after commit** — committed route appears in session metadata
5. **Commit blocked in explore mode** — returns 400 "Cannot commit in explore mode"
6. **Uncommit** — clears lock, returns to converge
7. **HTML elements present** — all 7 new elements found in served page

---

## CSS Classes Added in V0.2

```
.live-convergence          — meter container
.live-meter-track          — gray background track (8px height)
.live-meter-fill           — animated fill bar (transition: width 0.3s)
.live-score                — score label text
.live-hint                 — contextual hint below meter
.mode-explore              — blue (#3b82f6) for explore state
.mode-converge             — green (#22c55e) for converge state
.mode-commit               — amber (#f59e0b) for commit state
.mode-badge                — pill badge in result panel header
.mode-content              — container for mode-specific content
.mode-questions            — list of suggested questions (explore)
.mode-question-item        — clickable question item
.mode-gaps                 — list of convergence gaps (converge)
.mode-gap-item             — gap checklist item
.route-option-card         — clickable RIU candidate card (explore)
.commit-banner             — amber banner showing locked route
.commit-icon               — "COMMITTED" badge inside banner
.btn-commit                — commit button styling
.explore-nudge             — yellow nudge message (5+ explore routes)
.feedback-offer            — feedback opt-in panel
.feedback-detail           — small text explaining what's collected
.checkin-panel             — page-load check-in panel
.checkin-header            — "Welcome back" heading
.checkin-stats             — flex container for stat cards
.checkin-stat              — individual stat card
.checkin-stat-label        — stat label (small, gray)
.checkin-stat-value         — stat value (large, white)
.checkin-context           — last route context line
.query-panel               — collapsible query panel
.query-output              — preformatted query results
.btn-query-toggle          — "Check my progress" toggle button
```

---

## HTML Elements Added in V0.2

| ID | Element | Purpose |
|----|---------|---------|
| `liveMeterFill` | `div` | Convergence meter fill bar |
| `liveScore` | `span` | Score label ("EXPLORE 42/100") |
| `liveHint` | `p` | Field-level hints |
| `modeBadge` | `span` | Mode badge in result header |
| `modeContent` | `div` | Mode-adaptive content (questions/gaps/cards) |
| `projectCheckin` | `div` | Page-load check-in panel (hidden by default) |
| `commitBanner` | `div` | Committed route banner (hidden by default) |
| `btnCommit` | `button` | "Commit to this route" button (hidden by default) |
| `btnUncommit` | `button` | "Back to Converge" button (hidden by default) |
| `queryPanel` | `div` | Collapsible project state query panel |
| `queryInput` | `input` | Query text input |
| `btnQuery` | `button` | Query submit button |

---

## Known Limitations / What V0.2 Does NOT Have

1. **No LLM in the loop** — all routing is deterministic signal matching. This is by design (Palette philosophy: glass-box, traceable). But it means the translation layer is pattern-based, not semantic. Complex or unusual phrasings may not translate well.

2. **Server state is in-memory** — sessions, OWD state, and idempotency cache are all Maps with TTL cleanup. Server restart loses all server-side state. Client state (localStorage) survives.

3. **Single session ID** — the web client uses a hardcoded `"missioncanvas-web-session"` session ID. Multi-user support would require auth + unique session IDs.

4. **Decision Board is queryable but not visual** — per the operator's architecture decision, there is no persistent visual panel. State is stored in localStorage and queryable via the query panel or console. A future version could add a visual panel as an opt-in overlay.

5. **No mobile optimization** — CSS is desktop-first. The grid layout works on tablets but hasn't been tested on phones.

6. **Feedback endpoint has no aggregation** — `anonymous_feedback.jsonl` is append-only. No dashboard or analytics built yet.

---

## What's Next (V0.3 candidates)

These are NOT committed — they're the natural next work based on V0.2's shape:

1. **Visual UX polish** — the operator is doing browser testing now. Expect feedback on layout, colors, interactions.
2. **Decision Board visual mode** — optional visual overlay of project state, gated by a toggle
3. **Multi-session support** — auth or at minimum a session name selector
4. **Feedback analytics** — aggregate anonymous_feedback.jsonl into summary stats
5. **Mobile responsive** — media queries for phone-sized viewports
6. **LLM-enhanced translation** — optional Sonnet pass for complex/ambiguous inputs
7. **Export** — download project state, route history, or action briefs as files

---

## Design Specs (reference)

All three Track B specs live in `palette/projects/rossi-mission/`:

| Spec | Author | Key Idea |
|------|--------|----------|
| `ux_modes_spec.md` | Claude | Three modes (explore/converge/commit) with distinct server + client behavior per mode |
| `project_state_spec.md` | Kiro | Schema for persistent project state: facts, evidence, decisions, blockers, unknowns |
| `decision_board_spec.md` | Claude (reassigned from Mistral) | Decision Board renders project state, adapts to mode, stored not visual |

Bootstrap data: `project_state.yaml` — 189 lines of real Rossi data following Kiro's schema.

---

## Crew Status

- **Design review request** posted to Palette Peers bus with `requires_ack: true` for Kiro, Codex, and Gemini
- **V0.2 completion** has not yet been announced to the bus — do this when ready
- **The operator** is doing UX testing in browser right now

---

## Running the Server

```bash
cd /home/mical/fde/missioncanvas-site
node server.mjs
# → MissionCanvas server running at http://localhost:8787
# → Proxy mode disabled -> using local Palette route fallback
```

No environment variables needed for local mode. The server serves static files and routes through the local 121-RIU taxonomy.

---

*Written 2026-03-29 after shipping V0.2. All features built, tested, and visually verified at localhost:8787.*
