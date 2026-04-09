# Mission Canvas — File Structure

## Source (root)
- `server.mjs` — HTTP server, all API endpoints, route processing
- `convergence_chain.mjs` — Core engine: query detection, chain tracing, narration, coaching, health scoring
- `workspace_coaching.mjs` — Active coaching: explicit question detection, learner lens management
- `flywheel_feedback.mjs` — Canvas → Palette feedback: KL candidates, decision records, mastery signals
- `openclaw_adapter_core.mjs` — Palette taxonomy routing (121 RIUs)
- `data_boundary.mjs` — PII/data boundary enforcement
- `fetch_signals_logic_draft.mjs` — Auto-signal extraction from uploaded files
- `app.js` — Client-side application logic
- `workspace_ui.js` — Workspace UI components (coaching panel, dependency tree, nudges)
- `index.html` — Main web UI (voice + text, conversation flow)
- `style.css` — Workspace-aware styles
- `mcp_server.mjs` — MCP tool server (8 tools for any MCP client)
- `terminal_voice_bridge.mjs` — CLI voice interface
- `start.sh` — Launcher script

## Config
- `config.js` — Client configuration
- `config_schema.json` — Workspace config validation schema
- `project_state_schema.json` — Project state validation schema
- `palette_knowledge.json` — Exported Palette KL (read-only, 170 entries)
- `palette_routes.json` — Exported Palette routes (read-only, 121 routes)

## Workspaces (`workspaces/<id>/`)
- `config.yaml` — Workspace configuration (required)
- `project_state.yaml` — Project state with known facts, evidence gaps, decisions (required)
- `*_knowledge_library_v1.yaml` — Domain-specific KL entries (optional)
- `learner_lens.yaml` — Learner state (runtime, gitignored)
- `palette_feedback.yaml` — Flywheel feedback staging (runtime, gitignored)
- `sessions/` — Session persistence (runtime, gitignored)

## Tests (`tests/` or root during migration)
- `stress_test.mjs` — Basic contract compliance (37 tests)
- `stress_test_deep.mjs` — Adversarial inputs, edge cases (42 tests)
- `stress_test_session.mjs` — Session persistence, turn tracking (16 tests)
- `stress_test_convergence.mjs` — Convergence chain engine (103+ tests)
- `stress_test_v03_day2.mjs` — V0.3 integration tests (62 tests)
- `stress_test_enablement_hook.mjs` — Coaching detection and stages (14 tests)
- `stress_test_flywheel_feedback.mjs` — Feedback generation (75 tests)

## Naming Conventions
- Source: `snake_case.mjs` for server modules, `camelCase.js` for client
- Workspaces: `kebab-case` directory names
- Config/state: `snake_case.yaml`
- Tests: `stress_test_<feature>.mjs` or `test_<feature>.mjs`
