# Mission Canvas vs Agentic Workspace — Full Comparison

**Author**: kiro.design
**Date**: 2026-03-29
**Purpose**: These two projects are converging toward the same thing. This document maps the overlap, identifies what each teaches the other, and proposes unification.

---

## The Punchline

Mission Canvas and Agentic Workspace are the same product for different users.

| | Mission Canvas | Agentic Workspace |
|---|---|---|
| **User** | Small business owner (Rossi) | Large-scale oil investor |
| **Interface** | Web browser | CLI + voice |
| **Domain** | Retail, grants, business planning | Oil/energy, commodities, regulatory |
| **Entry point** | localhost:8787 web UI | ./start.sh → terminal voice bridge |
| **Backend** | missioncanvas-site/server.mjs | missioncanvas-site/server.mjs |
| **Routing** | openclaw_adapter_core.mjs (121 RIUs) | openclaw_adapter_core.mjs (121 RIUs) |
| **Knowledge** | palette_knowledge.json (168 entries) | palette_knowledge.json (168 + oil entries) |
| **OWD gate** | /confirm-one-way-door | /confirm-one-way-door |
| **Session state** | sessionStore in server.mjs | sessionStore in server.mjs |
| **Project state** | project_state.yaml (Rossi) | project_state.yaml (oil investor) |
| **Voice** | Browser speech API (app.js) | terminal_voice_bridge.mjs + Whisper |
| **Telegram** | rossi_bridge.py | Same pattern, different bot token |

The backend is identical. The routing is identical. The governance is identical. The only differences are: who's using it, how they talk to it, and what domain knowledge is loaded.

---

## What Mission Canvas Built That Workspace Inherits

Everything we shipped in the last 2 days is directly reusable:

| Component | Lines | Status | Workspace reuse |
|---|---|---|---|
| Full 121-RIU taxonomy routing | 339 | Shipped, 99 tests | Direct — same router |
| OWD confirmation gate | ~80 | Shipped, tested | Direct — same gate |
| KL integration (168 entries) | ~50 | Shipped, tested | Direct + oil entries added |
| Session state | ~30 | Shipped, 16 tests | Direct — same store |
| Idempotency + trace logging | ~40 | Shipped by Claude | Direct — same middleware |
| fetch_signals (PII scrubbing) | 166 | Reviewed, approved | Direct — same tool |
| Stress tests (3 suites, 99 tests) | 587 | All passing | Inherit + add workspace tests |
| terminal_voice_bridge.mjs | 174 | Verified, 60ms start | THE workspace entry point |

Workspace doesn't need to build any of this. It's already live on port 8787.

---

## What Workspace Adds That Mission Canvas Doesn't Have

| Component | What it is | Benefit to Mission Canvas |
|---|---|---|
| CLI voice entry point | terminal_voice_bridge.mjs as primary interface | Mission Canvas could offer this too — "talk to your business" |
| start.sh launcher | One-command startup | Mission Canvas needs this — currently requires manual server start |
| Oil domain KL entries | Commodity, regulatory, geopolitical knowledge | Proves the system is domain-agnostic — any vertical can be added |
| Executive FRX | Personalized welcome + context-aware greeting | Rossi should have this too — "Good morning Sahar, your fundability score is 79" |
| Telegram fallback | Mobile voice interface | Rossi already has this (rossi_bridge.py) — workspace just adapts the pattern |

---

## What Mission Canvas V0.2 Designed That Workspace Needs

The V0.2 specs we just reviewed are exactly what the workspace needs:

| V0.2 Spec | Mission Canvas use | Workspace use |
|---|---|---|
| Project-state object | Rossi: fundability, gaps, decisions | Investor: portfolio, regulatory, market position |
| UX modes (Explore/Converge/Commit) | Web UI mode switching | CLI mode switching (same logic, different rendering) |
| Decision Board | Web panel showing project state | CLI summary printed on startup + on demand |
| Convergence scoring | Route quality assessment | Same — determines how much guidance to give |

The specs are domain-agnostic. They work for any project_state.yaml, any user, any vertical.

---

## The Key Insight: They Should Be One System

Right now the plan has two separate projects:
- `missioncanvas-site/` — web-based, Rossi-focused
- `agentic-workspace/` (proposed) — CLI-based, investor-focused

But the architecture is:

```
                    ┌─────────────────────┐
                    │   Mission Canvas    │
                    │    server.mjs       │
                    │  (routing, KL, OWD, │
                    │   session, project) │
                    └────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐
        │  Web UI   │ │ CLI Voice │ │ Telegram  │
        │ (app.js)  │ │ (bridge)  │ │ (bot.py)  │
        │  Rossi    │ │ Investor  │ │  Mobile   │
        └───────────┘ └───────────┘ └───────────┘
```

Three frontends, one backend. The "workspace" is just another frontend to the same engine.

---

## What Each Project Teaches The Other

### Mission Canvas → Workspace

1. **Test before you ship.** Mission Canvas has 99 tests across 3 suites. The workspace ADR has zero tests mentioned. Every workspace feature should have tests from day 1.

2. **Convergence analysis matters.** We compared rossi_bridge.py against server.mjs and found 6 gaps. The workspace should do the same: what does the investor currently do manually? What patterns does he repeat? Build for those, not for imagined needs.

3. **Scope creep is the enemy.** Mission Canvas started with 5 gaps. We shipped 3 in one session because we cut scope. The workspace prompt had 8 branches — cutting to 4 was the right call. Keep cutting.

4. **Review everything.** Gemini's fetch_signals had a command injection bug. Codex built in the wrong directory. Mistral's analysis was thin. Every deliverable got reviewed and improved. The workspace should have the same review culture.

### Workspace → Mission Canvas

1. **Voice-first is powerful.** Mission Canvas has browser speech API but it's secondary. The terminal voice bridge proves that voice as primary input works (60ms, end-to-end). Mission Canvas should promote voice, not hide it.

2. **start.sh is needed.** Mission Canvas requires manually starting the server. A one-command launcher should exist for both projects.

3. **Personalized FRX is the differentiator.** "Good morning [name], here's what changed" is what makes a tool feel like a partner. Mission Canvas should do this for Rossi too.

4. **Domain portability proves the architecture.** If the same engine serves retail AND oil, the architecture is genuinely domain-agnostic. That's the real validation of the RIU/KL/routing design.

---

## Recommendation: Unify, Don't Fork

Instead of building `agentic-workspace/` as a separate repo:

1. **Keep missioncanvas-site/ as the engine.** It works. 99 tests. Full routing. OWD. KL. Session state.

2. **Add a `workspaces/` directory** with per-client configs:
   ```
   workspaces/
     rossi/
       project_state.yaml
       config.yaml (name, greeting, domain, telegram bot token)
     oil-investor/
       project_state.yaml
       config.yaml
   ```

3. **Make start.sh workspace-aware:**
   ```bash
   ./start.sh rossi        # starts web UI + Telegram bot for Rossi
   ./start.sh oil-investor  # starts CLI voice bridge for investor
   ./start.sh              # starts server only, all workspaces available
   ```

4. **The voice bridge, web UI, and Telegram bot are all frontends** that connect to the same server. They read the workspace config to personalize the FRX.

This means:
- One codebase to maintain
- One test suite to run
- One routing engine to improve
- Domain knowledge is additive (oil KL entries benefit everyone)
- New clients = new workspace config + project_state.yaml, not new repos

---

## What This Changes About The Plan

| Original plan | Unified plan |
|---|---|
| Build agentic-workspace/ as new repo | Add workspace config to missioncanvas-site/ |
| Copy Palette into core/ | Already imported |
| Build new routing | Already built (121 RIUs, 99 tests) |
| Build new OWD gate | Already built |
| Build new session state | Already built |
| Build new persistence | project_state.yaml already designed + bootstrapped for Rossi |
| Build voice bridge | terminal_voice_bridge.mjs already exists and verified |
| 4-week timeline | 1-2 weeks (most work is done) |

The "last 10%" you mentioned is actually: workspace config system, oil domain KL entries, personalized FRX, and start.sh. That's it.

---

**Bottom line**: Don't build two products. Build one product with two workspaces. The engine is done. The frontends exist. The gap is configuration and domain knowledge.
