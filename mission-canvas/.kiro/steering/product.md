# Mission Canvas — Product Context

Mission Canvas is a voice-first implementation machine with a coaching layer. It routes user intent through a 121-RIU taxonomy, traces dependency chains through project state, teaches domain concepts adaptively, and tracks decisions with one-way-door governance.

## Architecture

- **Convergence Chain Engine** (`convergence_chain.mjs`): Deterministic dependency graph — detect project queries, trace chains, narrate status, generate nudges, annotate with coaching signals
- **Workspace System**: Per-client config + project state + domain knowledge library. Adding a workspace = create folder + YAML files
- **Coaching**: Passive (inline hints during narration) + Active (explicit question responses). Unified learner store in `learner_lens.yaml`
- **Wire Contract**: 7 fields in (HandoffPacket), 7 fields out (HandoffResult). Universal protocol across all three systems
- **Flywheel Feedback**: Canvas → Palette via `palette_feedback.yaml`. Evidence resolutions become KL candidates

## Key Patterns

- `processRoute()` in server.mjs is the shared route handler for both `/route` and `/talk-stream`
- Project-state queries (how are we doing, what's blocking us) go through convergence chain FIRST, coaching intercept SECOND
- All state mutations must call `invalidateIndex()` and `workspaceCache.delete()` after writing
- Coaching signals emit as wire packets (`coaching_packets`) alongside legacy `coaching_signals`
- Tests must pass: stress_test.mjs, stress_test_session.mjs, stress_test_convergence.mjs (minimum)

## Do NOT

- Break existing test suites (255+ tests)
- Modify the wire contract schema (7 in, 7 out)
- Put runtime state in git (sessions, learner_lens, palette_feedback)
- Duplicate the Palette Knowledge Library (168 entries in palette/knowledge-library/v1.4/)
- Make one-way-door decisions without flagging them
