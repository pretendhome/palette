# Mission Canvas — Unified Architecture & Implementation Plan

**Author**: claude.analysis (Claude Code)
**Date**: 2026-03-29
**Status**: IMPLEMENTATION-READY — synthesizes all crew analyses into a single buildable plan
**Depends on**: V0.2 (shipped), Kiro's comparison + convergence chain, Codex's unified thesis + artifact-first analysis, Gemini's ADR 001

---

## What This Document Is

Five agents spent two days analyzing, designing, building, and arguing about Mission Canvas and the Agentic Workspace. They produced 14 documents totaling ~25,000 words. Every one of them converged on the same conclusion from a different angle:

- **Kiro** (comparison): "They should be one system. Don't fork."
- **Codex** (thesis): "One engine, multiple frontends, multiple workspace configurations."
- **Kiro** (convergence chain): "The gap isn't routing — it's dependency chain reasoning over specific project state."
- **Codex** (CX sweep): "Center project-state over request-state. The product is a decision-convergence system."
- **Codex** (artifact-first): "The unit of value is intent → artifact → updated state, not prompt → response."
- **Gemini** (ADR): "Option E hybrid with voice bridge and workspace launcher." (Right instinct, thin execution.)

This document takes what each got right, discards what doesn't survive contact with the running code, and produces the plan I'm going to build.

---

## The Product

Mission Canvas is a **decision-convergence engine** that turns messy human intent into persistent, useful structure.

It is not a chatbot. It is not a prompt router. It is not a website builder.

It is a system where:
1. You speak or type what you need
2. It interprets your intent against your specific project state
3. It produces a persistent artifact — a brief, a board, a plan, an evidence pack
4. Your workspace gets smarter every time you use it
5. It knows what's blocked, what changed, who needs to act, and what to do next

The conversation is the control surface. The artifacts are the product. The project state is the memory.

---

## Architecture

### One Engine

The engine already exists and is live at `missioncanvas-site/`:

```
server.mjs          (716 lines)  — HTTP server, routing, sessions, commit, governance
openclaw_adapter_core.mjs (339)  — 121-RIU scoring, KL lookup, convergence scoring
palette_routes.json              — Full v1.3 taxonomy (121 RIUs, trigger signals)
palette_knowledge.json           — 162 knowledge library entries with RIU mappings
```

What the engine does:
- Routes through 121 RIUs using 3-tier signal matching (trigger signals → name → execution intent)
- Looks up knowledge library evidence for every matched RIU
- Detects one-way doors from both input text and RIU reversibility metadata
- Tracks sessions with accumulated history that influences future routing
- Computes convergence score (explore/converge/commit modes)
- Injects project state into routing context
- Enforces commit/uncommit flow with server-side guards
- Logs decisions, traces all actions, deduplicates via idempotency cache

Verified by 99 tests across 3 suites. Zero failures.

### Three Frontends

```
                    ┌──────────────────────────┐
                    │     Mission Canvas        │
                    │      Engine               │
                    │  (server.mjs @ :8787)     │
                    │                           │
                    │  routing · KL · OWD       │
                    │  sessions · project state │
                    │  convergence · artifacts  │
                    └────────────┬──────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                   │
        ┌─────┴──────┐   ┌──────┴──────┐   ┌───────┴──────┐
        │   Web UI    │   │  CLI Voice  │   │   Telegram   │
        │  (app.js)   │   │  (bridge)   │   │   (bot.py)   │
        │             │   │             │   │              │
        │  Browser    │   │  Terminal   │   │   Mobile     │
        │  Speech API │   │  Whisper    │   │   Voice msg  │
        │  Forms      │   │  Push-talk  │   │   Text       │
        │  Live meter │   │  TTS out    │   │   Commands   │
        └────────────┘   └─────────────┘   └──────────────┘
```

- **Web** (shipped, 1485 lines): Best for visible convergence, boards, gap resolution, review workflows. Live convergence meter, mode badges, check-in panel, queryable project state.
- **CLI Voice** (exists, 174 lines, needs hardening): Best for fast executive interaction. terminal_voice_bridge.mjs, verified at 60ms cold start, captures audio → Whisper transcription → routes to engine → response.
- **Telegram** (production, rossi_bridge.py pattern): Best for ambient mobile access. Voice messages → transcription → routing → text response.

These are not separate products. They are separate doors into the same engine. Every frontend passes `workspace_id` + `session_id`. The engine loads the workspace config and adapts.

### Workspace Configurations

Each deployment is a workspace config, not a fork:

```
workspaces/
  rossi/
    config.yaml           # identity, domain, FRX, modality, governance
    project_state.yaml    # persistent mission state
    sources.yaml          # where to look for evidence
  oil-investor/
    config.yaml
    project_state.yaml
    sources.yaml
```

A new client = a new directory with three YAML files. Not a new repo. Not a new engine.

**config.yaml** (per Codex's workspace config model):
```yaml
workspace:
  id: "rossi"
  name: "Rossi Mission"
  user_name: "Sahar"
  user_role: "owner"
  domain: "retail-grants-business-planning"
  primary_frontend: "web"

frx:
  greeting_style: "operator"
  startup_artifact: "decision_board_snapshot"
  show_top_blockers: true

artifacts:
  defaults:
    - "decision_board"
    - "evidence_gap_summary"
    - "action_plan"
    - "funding_readiness_brief"

retrieval:
  static_knowledge_pack: "core"
  live_retrieval_enabled: false

governance:
  risk_posture: "medium"
  require_owd_confirmation: true
```

---

## The Missing Piece: The Convergence Chain

This is the single most important insight from the entire crew analysis. Kiro identified it and I'm going to build it.

### The Problem

When Sahar asks "how are we doing?", the Rossi Telegram bridge knows:
- Fundability score is 79/100, conditional fail
- The #1 blocker is 12 months of trailing actuals from Square POS
- That's been the blocker for 6 weeks
- It's blocking the revenue model decision, which blocks grant applications
- Only the owner (Sahar) can resolve it
- Once she does, everything else unblocks

Mission Canvas V0.2 routes that question to RIU-001 (generic convergence) and returns a template. Structurally correct. Completely useless to Sahar.

### The Solution

The convergence chain is a reasoning layer that traverses the project state dependency graph. It turns inert YAML data into specific, actionable, dependency-aware answers.

```
Question: "How are we doing?"
    │
    ▼
Project State Detector
    → recognizes this is a project-state query, not a routing request
    │
    ▼
Health Score: 79/100 (conditional fail)
    │
    ▼
Dependency Chain Traverser
    │
    ├── ME-001: 12mo trailing actuals (CRITICAL, 6 weeks stale)
    │     ├── who_resolves: owner (Sahar)
    │     └── unblocks: OD-001 (revenue model)
    │           └── unblocks: grant applications
    │                 └── unblocks: fundability improvement
    │
    └── ME-002: Named advisory board (MODERATE)
          ├── who_resolves: owner (Sahar)
          └── unblocks: governance section → underwriter submission
    │
    ▼
Chain Narrator
    → "Your fundability score is 79. The #1 blocker is still the
       Square POS data — it's been 6 weeks. Once you pull that,
       we can make the revenue model decision and start grant
       applications. The advisory board names are #2. Both are
       on you."
```

This is not an LLM. It's graph traversal over structured YAML. Deterministic, testable, fast.

### Four Components

**1. State-Aware Query Detector** (`detectProjectQuery`)

Before routing, check if the input maps to a project state query:

| Pattern | Action |
|---------|--------|
| "how are we doing", "status", "progress" | Return health score + top blockers with dependency chains |
| "what's blocking", "stuck", "gaps" | Return blocked actions with full dependency trace |
| "what should I do next", "next step" | Return highest-priority unresolved item where who_resolves = current user |
| "what changed", "update" | Diff project state against last session snapshot |
| "what do we know", "facts" | Return known facts |
| "decisions", "what's pending" | Return open decisions with options and blockers |

These short-circuit the RIU router entirely. The answer comes from the project state, not from taxonomy matching.

**2. Dependency Chain Traverser** (`traceChain`)

Given any node in the project state (a missing evidence item, an open decision, a blocked action), walk the dependency graph:

```javascript
function traceChain(nodeId, projectState) {
  // Returns: { node, age_days, who_resolves, unblocks: [{ node, unblocks: [...] }] }
  // Recursive traversal of blocked_by / unblocks relationships
  // Includes temporal data (identified_at → age calculation)
}
```

This turns the flat YAML into a navigable graph. The Decision Board renders it. The voice bridge narrates it. The web UI shows it as a clickable tree.

**3. Chain Narrator** (`narrateChain`)

Takes a dependency chain and produces natural language:

```javascript
function narrateChain(chain, userRole) {
  // "The #1 blocker is [X] ([age] weeks). It's blocking [Y] which blocks [Z].
  //  [who_resolves] needs to [specific action]."
  // Adapts tone for owner vs operator lens
}
```

**4. Proactive Nudge Generator** (`generateNudges`)

On session start, scan project state for stale blockers:

```javascript
function generateNudges(projectState, config) {
  // Find missing_evidence where:
  //   identified_at > config.nudge_threshold_days (default: 14)
  //   AND status != 'resolved'
  // Return prioritized list with urgency framing
}
```

This is what makes the system proactive. Not "here are your options" but "this has been your #1 blocker for 6 weeks and it's on you."

---

## Artifacts as First-Class Objects

Codex's deepest insight: **the unit of value is intent → artifact → updated state, not prompt → response.**

Every interaction should leave behind something persistent. The conversation is the control surface. The artifacts are the product.

### Core Artifact Types

| Artifact | Purpose | When Generated |
|----------|---------|----------------|
| **Decision Board Snapshot** | Orientation: where you are | On startup, on demand |
| **Project State** | Substrate: machine-readable mission memory | Updated after every meaningful interaction |
| **Action Brief** | Execution: what to do next | After routing |
| **Evidence Gap Summary** | Clarity: what's missing and why it matters | On demand, with dependency chains |
| **What Changed Brief** | Re-entry: get back in context fast | On session start if state changed |
| **Recommendation Note** | Decision support: what I think you should do | After convergence |
| **Stakeholder Update Draft** | Communication: turn internal state into external message | On demand |
| **Plan** | Movement: time-bounded sequence of actions | After commit |

### Artifact Quality Test (from Codex)

> **If I remove the chat transcript, does the workspace still contain meaningful value?**
>
> If the answer is no, the product is still too chat-first.

### Voice-to-Artifact Loop

```
1. User speaks intent
2. System interprets against workspace state
3. System produces artifact
4. Artifact is saved to workspace
5. Project state updates
6. User sees what changed
7. Next suggested move appears
```

---

## The First 60 Seconds

This is the #1 priority. Codex is right: if the system starts with a blank chat box, it is underperforming.

### Web (Rossi)

```
Mission Canvas active for Rossi.
Fundability: 79/100 — 2 critical evidence gaps, 1 open revenue decision.

Top blocker: 12mo trailing actuals (Square POS data) — 6 weeks outstanding.
This blocks: revenue model decision → grant applications → fundability improvement.
Action needed from: Sahar (owner).

Right now I can:
1. Show what's blocking you
2. Brief you on what changed
3. Draft the grant readiness checklist
4. Help you make the revenue model decision
```

### CLI Voice (Oil Investor)

```
Mission Control active for [Name].
3 portfolio-relevant items flagged since yesterday.

Top item: FERC pipeline approval hearing — decision expected this week.
Potential impact: affects your midstream allocation thesis.

Say "brief me" for the full market context, or ask anything.
```

### Pattern

1. **Launch** → system loads your workspace
2. **Recognition** → system knows who you are and where you are
3. **Orientation** → system surfaces what matters right now (not a blank box)
4. **First artifact** → within 60 seconds, the system creates something useful
5. **Visible persistence** → user sees what was saved and what changed
6. **Next step** → system offers the next move

---

## Implementation Plan

### What Already Exists (V0.2 — shipped)

| Component | Status | Lines |
|-----------|--------|-------|
| 121-RIU taxonomy routing | Live, tested | 339 |
| Knowledge library (162 entries, gap detection) | Live, tested | — |
| One-way-door gate (real, 10 states) | Live, tested | ~80 |
| Session state (history, routing influence) | Live, 16 tests | ~30 |
| Convergence scoring (explore/converge/commit) | Live | ~60 |
| Client-side project state (localStorage) | Live | ~80 |
| Live convergence meter (real-time, per-keystroke) | Live | ~70 |
| Commit/uncommit flow | Live | ~80 |
| Project state injection into routing | Live | ~20 |
| Anonymous feedback pipeline | Live | ~90 |
| Idempotency + trace logging | Live | ~40 |
| Web UI (full) | Live | 1,485 |
| Voice bridge (terminal) | Exists, 60ms cold start | 174 |
| Stress tests (3 suites) | 99 pass, 0 fail | 587 |

**Total live code**: ~3,500 lines, fully tested.

### What Needs Building (V0.3)

#### Phase 1: Convergence Chain Engine (2-3 days)

The highest-value work. This is what turns the system from a router into a partner.

**1a. Project State Schema Enhancement**
- Add `identified_at` timestamp to all missing_evidence entries (temporal awareness)
- Add `unblocks` forward-link array to missing_evidence and open_decisions
- Add `blocked_by` back-link to blocked_actions (some exists, make complete)
- Add `health_score` computed field with breakdown
- Schema stays YAML. Stays on disk. Stays per-workspace.

**1b. State-Aware Query Detector**
- New function in openclaw_adapter_core.mjs
- Pattern matching for project-state queries
- Short-circuits RIU router when detected
- Returns structured project-state response instead of routing response

**1c. Dependency Chain Traverser**
- New module: `convergence_chain.mjs`
- `traceChain(nodeId, projectState)` → recursive dependency graph
- `narrateChain(chain, userRole)` → natural language summary
- `generateNudges(projectState, config)` → stale blocker detection

**1d. Integration**
- Server loads workspace project_state.yaml on session init
- Route handler checks query detector before RIU routing
- Response includes chain narration when applicable
- Nudges surface on session start (check-in panel / voice welcome)

#### Phase 2: Workspace Config System (1 day)

**2a. Directory Structure**
```
workspaces/
  rossi/
    config.yaml
    project_state.yaml
  oil-investor/
    config.yaml
    project_state.yaml
```

**2b. Config Loader**
- Server reads workspace config on startup / session init
- Config determines: identity, domain, FRX, artifact defaults, governance posture
- Frontend passes `workspace_id` with every request

**2c. Rossi Bootstrap**
- Extract real Rossi data from bridge system prompt + existing project_state.yaml
- 16 known facts, 5 missing evidence items, 3 open decisions, 3 blocked actions
- This is mostly done — project_state.yaml already exists at `rossi-mission/`

**2d. Oil Investor Bootstrap**
- Create oil-investor workspace config
- Bootstrap project_state.yaml with placeholder domain context
- Depends on Phase 3 for real domain knowledge

#### Phase 3: Oil Domain Knowledge (1-2 days)

Per Codex's vertical knowledge spec:

**Static KL entries** (encode as palette_knowledge entries):
- Commodity interpretation frameworks (WTI, Brent, spreads, crack spreads)
- Industry structure (upstream/midstream/downstream, majors vs independents)
- Financial interpretation (EBITDA in energy, lifting costs, break-even, hedging)
- Regulatory entity map (FERC, EPA, BSEE, BOEM, DOE, OPEC+)
- Publication/source map (Oil & Gas Journal, Platts, EIA, SEC filings)
- Geopolitical risk frameworks (Hormuz, sanctions, OPEC+ quotas)

**Live retrieval targets** (not built in V0.3, but identified):
- Commodity prices (WTI, Brent, natgas)
- OPEC+ announcements
- FERC filings
- Company signals (earnings, guidance, asset sales)

Target: 20+ static KL entries. Research sprint using Perplexity.

#### Phase 4: Voice Bridge Hardening (1 day)

- Wire `workspace_id` and `session_id` into voice bridge requests
- Add Whisper model pre-check (detect, download if missing, default to base model)
- Add audio hardware detection with graceful text fallback
- Add personalized welcome from workspace config + project state
- Add convergence chain narration in voice responses

#### Phase 5: start.sh Launcher (0.5 day)

```bash
./start.sh                  # start engine only
./start.sh rossi            # start engine + web (open browser)
./start.sh oil-investor     # start engine + CLI voice bridge
```

- Dependency detection (Node, Python, Whisper, audio hardware)
- Clear error messages for missing deps
- Single process management (starts server + chosen frontend)
- Works in text-only mode if voice deps missing

#### Phase 6: First 60 Seconds (1 day)

- Workspace-aware welcome in all three frontends
- Proactive nudge generation from stale blockers
- Startup artifact generation (decision board snapshot or what-changed brief)
- "Right now I can:" structured orientation menu
- Smart re-entry: if returning user, show what changed since last session

#### Phase 7: Artifact Persistence (1 day)

- Artifact directory per workspace: `workspaces/rossi/artifacts/`
- Each artifact saved with type, timestamp, provenance
- Artifact list queryable ("show me all briefs from this week")
- Project state auto-updates when artifacts are created
- Decision Board snapshot generated on demand

### Timeline

| Phase | Days | Depends On |
|-------|------|------------|
| 1. Convergence Chain | 2-3 | Nothing (V0.2 is the base) |
| 2. Workspace Config | 1 | Nothing |
| 3. Oil Domain KL | 1-2 | Phase 2 for workspace structure |
| 4. Voice Bridge | 1 | Phase 2 for config loading |
| 5. start.sh | 0.5 | Phase 2 + 4 |
| 6. First 60 Seconds | 1 | Phases 1 + 2 |
| 7. Artifact Persistence | 1 | Phase 2 |

Phases 1 and 2 can run in parallel. Phases 3-5 can run in parallel after Phase 2. Total: ~8 days of build time. Fits in 2 weeks with testing and iteration margin.

### Definition of Done (V0.3)

The system is done when:

1. **Rossi workspace**: Sahar asks "how are we doing?" and gets her fundability score, top blocker with dependency chain, who needs to act, and how long it's been stale. Not a generic convergence brief — her specific situation.

2. **Oil investor workspace**: Investor runs `./start.sh oil-investor`, speaks a question about his portfolio, gets a routed response with oil-domain KL evidence, and the system remembers the conversation.

3. **Convergence chain**: Any project-state query ("what's blocking us", "what changed", "what should I do next") returns dependency-aware answers traced through the specific workspace's state.

4. **Artifacts persist**: Every meaningful interaction leaves behind a saved artifact in the workspace directory. Project state updates automatically.

5. **First 60 seconds**: Both workspaces produce orientation + first artifact within 60 seconds of launch. No blank chat box.

6. **All existing tests still pass**: 99+ tests, zero regressions.

---

## What Each Agent Got Right

| Agent | Key Insight | Where It Lives In This Plan |
|-------|-------------|----------------------------|
| **Kiro** | "They should be one system" | Core architecture: one engine, three frontends, workspace configs |
| **Kiro** | The convergence chain — dependency reasoning over project state | Phase 1: the #1 priority |
| **Kiro** | Temporal awareness creates urgency | `identified_at` timestamps on all evidence gaps |
| **Codex** | "Artifact-first, not chat-first" | Phase 7: persistent artifacts, the product quality test |
| **Codex** | "The unit of value is intent → artifact → updated state" | The voice-to-artifact loop, every frontend |
| **Codex** | First 60 seconds: recognized → oriented → helped → in motion | Phase 6: startup artifacts + proactive nudges |
| **Codex** | Workspace config model with domain packs | Phase 2: `workspaces/` directory with config.yaml |
| **Codex** | Vertical knowledge split: static KL vs live retrieval | Phase 3: oil_v1 static pack, live retrieval deferred |
| **Codex** | Three gap types: retrieval, evidence, decision | Convergence chain distinguishes all three |
| **Gemini** | Option E hybrid with voice bridge and bash wrapper | Phase 4 + 5: the approach is right, the execution was thin |
| **Gemini** | 7-state FRX storyboard (structure, not content) | Phase 6: adapted with honest content (no live prices) |
| **Gemini** | Governance control map by maturity tier | Already in server.mjs, extended in workspace config |

## What Each Agent Got Wrong

| Agent | Issue | Correction |
|-------|-------|------------|
| **Gemini** | Promised live WTI prices and FERC filings | We have zero real-time data infrastructure. Static KL + Perplexity research sprints, not live feeds |
| **Gemini** | ADR was 60 lines with no code | Architecture-shaped, not architecture-grade. This plan replaces it |
| **Gemini** | Proposed copying Palette into core/ | Palette stays where it is. The workspace imports from existing locations |
| **Codex** | 8 documents totaling ~15K words of analysis | Extraordinary strategic thinking, but needed synthesis into a single buildable plan. This is that plan |

---

## Why This Wins

Every AI product in the world does `prompt → response`. The user gets an answer, the conversation disappears, and next time they start from scratch.

This system does `intent → artifact → updated state → dependency-aware continuity`. The user speaks, the system creates something useful, saves it, updates the project state, and next time knows exactly where they left off, what's blocking them, how long it's been, and who needs to act.

The convergence chain is the key. It's the difference between a system that *responds* and a system that *understands*. Between "you said business plan, here's RIU-109" and "your fundability score is 79, the Square POS data has been your blocker for 6 weeks, and once you pull it everything else unblocks."

The workspace model means this works for any domain. Rossi today. Oil investor tomorrow. A startup founder next week. Same engine, different config, different knowledge pack. One codebase to maintain, one test suite to run, one routing engine to improve.

The artifact-first design means the product compounds. Each interaction makes the workspace more valuable. The system isn't just smart — it accumulates intelligence about your specific mission over time. That's what makes someone say "this actually helps me" and come back.

---

*This plan synthesizes the work of five agents across 14 documents and ~25,000 words of analysis. The code is live. The tests pass. The architecture is sound. What's left is the convergence chain, the workspace model, and the first 60 seconds. That's what separates a smart demo from a system people use.*

*— Claude Code, 2026-03-29*
