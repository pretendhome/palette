# ADR 001: Master Architecture — Mission Control (Oil Vertical)

**Status**: CONVERGED (Unified with Mission Canvas)
**Author**: Gemini CLI (UNVALIDATED)
**Client**: Large-scale Oil Investor
**Date**: 2026-03-30

## 1. Context & Product Unification
Following feedback from Claude and Kiro, we are **Unifying Agentic Workspace with Mission Canvas**. The engine will be the existing `missioncanvas-site/` (localhost:8787). This project (Mission Control) becomes the first **Enterprise Workspace Configuration** for that engine.

## 2. Decision Matrix: Execution Environment
- **Selected**: Option E (Hybrid - Claude Code + Wrapper).
- **Update**: The wrapper (`bin/start.sh`) will now launch the unified `missioncanvas-site` server with the `oil-investor` workspace configuration.

## 3. Implementation Path (Unified)
- **Engine**: `missioncanvas-site/` (121 RIU Routing, KL Integration, OWD Gate).
- **Interface**: `terminal_voice_bridge.mjs` (CLI Voice) + Telegram (Mobile).
- **Persistence**: `workspaces/oil-investor/project_state.yaml` (Persistent state).
- **Vertical**: Oil domain KL entries (Argy research sprint).

## 4. FRX Storyboard (Updated for Unification)
1. **Command**: `./start.sh oil-investor`
2. **Detection**: CLI identifies the workspace and loads the associated `project_state.yaml`.
3. **Voice**: "Mission Control active for [Name]. WTI context loaded. How can I help?"

## 5. Handover to Claude (Lead Finisher)
I am handing over the execution lead to `claude.analysis` for the 5-day ship plan. I will support by:
- Closing the KL gaps for Oil domain (Argy support).
- Drafting the Voice/Multimodal tradeoffs 1-pager.
- Assisting with the Constellation Registry gaps identified by Kiro.
