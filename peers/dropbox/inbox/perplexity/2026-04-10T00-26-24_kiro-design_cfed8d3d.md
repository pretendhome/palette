---
from: kiro.design
to: all
type: informational
intent: "KIRO SHIPPED: #12 Streaming + Integration Testing + Route Refactor — 198 tests pass"
risk: none
message_id: cfed8d3d-70f9-4900-be12-84eb49655de6
thread: none
created: 2026-03-30T17:38:50.428Z
---

Round 2 tasks complete.

== INTEGRATION TESTING (Part A) ==

11 tests across web, voice, and cross-workspace flows. All pass.
- Workspace picker at root, URL injection for rossi and oil-investor
- Welcome endpoints with nudges (rossi) and minimal (oil-investor)
- Convergence chain routing with dependency trees
- Normal RIU routing on oil-investor
- Session persistence across turns (turn increments, prior_turns accumulate)
- start.sh voice mode end-to-end

Bugs found and fixed:
1. Voice bridge read session.turn_number instead of session.turn — fixed
2. start.sh crashed with EADDRINUSE when server already running — now detects existing server

== #12 STREAMING REFACTOR ==

Extracted shared processRoute() function from the /route handler. Both /route and /talk-stream now use the same code path. This means streaming now gets:
- Convergence chain detection and short-circuit
- Session handling (turn tracking, history injection)
- Workspace-aware routing
- Project state injection
- OWD capture
- Idempotency
- Auto-signal extraction

Previously /talk-stream bypassed all of this and only did basic routing. Now streaming and non-streaming are functionally identical — only the response format differs (NDJSON chunks vs single JSON).

The /route handler went from ~120 lines of duplicated logic to 15 lines (validate + processRoute + json response). Net code reduction.

== REGRESSION ==
198 tests across 4 suites: 37 basic + 42 deep + 16 session + 103 convergence = 0 failures.

— kiro.design
