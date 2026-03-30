# MissionCanvas UX Modes Spec — Explore / Converge / Commit

**Author**: claude.analysis
**Date**: 2026-03-29
**Status**: PROPOSAL — design only, no code
**Depends on**: Session state (Kiro, Track A), Project-state object (Codex, Track B)

---

## Problem

Canvas currently treats every request the same way: route it, return a brief, done. The response _hints_ at what the user should do next (`status: needs_convergence | ok | needs_confirmation`) but the server and UI don't change behavior based on where the user is in their decision process.

A business owner exploring "what grants am I eligible for?" needs a different experience than one who has converged on "apply for the SBA Community Advantage loan by April 15" and is ready to commit.

## The Three Modes

### EXPLORE
_"I'm not sure what I need yet."_

**When**: User input is incomplete or vague. Convergence score < 50. First turn in a session. Or user explicitly says "show me options."

**Server behavior**:
- Return **multiple route candidates** (top 5, not just top 1)
- Each candidate includes its own mini-brief (2-3 lines, not the full action brief)
- `status: exploring`
- Do NOT capture OWD — nothing is committed yet
- Surface knowledge gaps prominently: "We don't have data on X — do you want to research?"
- Suggest convergence questions: "What outcome do you need by when?"

**Response shape additions**:
```json
{
  "mode": "explore",
  "convergence_score": 35,
  "suggested_questions": [
    "What specific outcome do you need?",
    "What is your timeline?",
    "What constraints should I know about?"
  ],
  "route_options": [
    { "riu_id": "RIU-109", "name": "Business Plan", "strength": "STRONG", "mini_brief": "..." },
    { "riu_id": "RIU-039", "name": "Funding & Grants", "strength": "MODERATE", "mini_brief": "..." }
  ]
}
```

**UI behavior**:
- Show all candidates as selectable cards, not just one result
- Hide the "Confirm OWD" button
- Show the "Refine + Reroute" section prominently
- Show missing fields with suggested questions
- Persona defaults kick in here (fill gaps from persona)

---

### CONVERGE
_"I know roughly what I need. Help me refine."_

**When**: Convergence score >= 50 but < 95. Or user selects a route from Explore. Or second+ turn in a session with accumulated context.

**Server behavior**:
- Return **top 1 route with full brief** + 2 runner-up alternatives
- `status: converging`
- Surface gaps between what the user said and what the route needs
- Show knowledge library evidence for the selected route
- If knowledge gaps detected, suggest: "Research needed for [RIU] before committing"
- Track this as a convergence turn in session history

**Response shape additions**:
```json
{
  "mode": "converge",
  "convergence_score": 72,
  "gaps": [
    "No constraints specified — timeline and budget unknown",
    "RIU-505 has no knowledge library coverage"
  ],
  "alternatives": [
    { "riu_id": "RIU-039", "name": "Funding & Grants", "why_not": "Lower signal match (score 3 vs 5)" }
  ]
}
```

**UI behavior**:
- Show the primary route result (current rendering)
- Show alternatives collapsed under "Other options considered"
- Show gaps as a checklist the user can address
- Show KL evidence section
- "Route Mission" button changes to "Refine" if gaps remain

---

### COMMIT
_"I'm ready to act."_

**When**: Convergence score >= 95 AND user explicitly clicks "Commit" or confirms OWD. Or user has addressed all gaps from Converge mode.

**Server behavior**:
- Return **single route, full brief, execution-ready**
- `status: committed`
- If OWD detected: capture in `pendingOWD`, require confirmation before proceeding
- If no OWD: return execution plan with concrete first action
- Lock the route — subsequent requests in this session reference this commitment
- Append to decision log automatically

**Response shape additions**:
```json
{
  "mode": "commit",
  "convergence_score": 98,
  "committed_route": "RIU-109",
  "execution_plan": {
    "first_action": "Create convergence_brief.md",
    "agent": "Orchestrator",
    "estimated_artifacts": 7,
    "owd_gate": true
  }
}
```

**UI behavior**:
- Show final brief in read-only view
- OWD confirmation panel visible if needed (with per-item approve/reject)
- "Copy Brief" and "Speak Brief" prominent
- "Append Decision Log" auto-fires
- "Back to Explore" button available (returns to Explore mode, clears commitment)

---

## Mode Detection Logic

Modes are determined by a combination of **auto-detection** and **explicit user action**.

### Auto-detection (server-side)

```
convergence_score = weighted sum of:
  objective present:       40 points
  desired_outcome present: 30 points
  context present:         15 points
  constraints present:     10 points
  persona selected:         5 points

if score < 50:           mode = explore
if 50 <= score < 95:     mode = converge
if score >= 95:          mode = converge (not auto-commit — commit requires intent)
```

Commit is NEVER auto-detected. The user must explicitly commit. This is a safety feature — we don't want accidental commitment to irreversible actions.

### Explicit user actions

| Action | Mode transition |
|--------|----------------|
| First request in session | → explore |
| User fills in missing fields and reroutes | → converge (if score improves) |
| User selects a route card from Explore | → converge (for that route) |
| User clicks "Commit" button | → commit |
| User confirms OWD | stays in commit (execution approved) |
| User rejects OWD | → converge (return to refinement) |
| User clicks "Back to Explore" | → explore (clears commitment) |

### Session-aware transitions

With Kiro's session state, mode transitions are tracked per session:

```
Session {
  session_id: "abc-123",
  mode_history: ["explore", "explore", "converge", "converge", "commit"],
  current_mode: "commit",
  committed_route: "RIU-109",
  turns: 5
}
```

If a user has been in Explore for 5+ turns without converging, the response should include:
```json
"convergence_nudge": "You've explored 5 routes. Would narrowing to a specific outcome help?"
```

---

## Implementation Plan (when approved)

### Phase 1: Server changes (openclaw_adapter_core.mjs)
1. Add `computeConvergenceScore(input)` function
2. Add `mode` field to response based on score
3. Add `suggested_questions` for Explore mode
4. Add `gaps` for Converge mode
5. Modify `localRouteResponse()` to shape output per mode

### Phase 2: Server changes (server.mjs)
1. Add mode to session state (ties into Kiro's session_id work)
2. Track mode transitions in session history
3. Add `/commit` endpoint that locks a route for a session
4. Modify `/route` to check session mode before routing

### Phase 3: UI changes (app.js + index.html)
1. Render route cards for Explore (selectable)
2. Show gaps checklist for Converge
3. Add "Commit" button that transitions to Commit mode
4. Add "Back to Explore" escape hatch
5. Per-item OWD approve/reject in Commit mode
6. Convergence nudge after 5+ Explore turns

### Phase 4: Integration with Track B specs
- Codex's project-state feeds into convergence scoring (known facts increase score)
- Mistral's Decision Board renders differently per mode:
  - Explore: "What we don't know" dominates
  - Converge: "What we believe vs what we know" dominates
  - Commit: "What can execute now" dominates

---

## Constraints

- Mode detection MUST NOT block routing. Even in Explore, the user can always route — mode changes the response shape, not access.
- Commit is ALWAYS explicit. Never auto-commit.
- OWD gate only activates in Commit mode. In Explore and Converge, OWD is flagged but not gated.
- Mode state lives in the session, not the request. A new request in the same session inherits the current mode unless the user explicitly transitions.
- All mode transitions are logged in trace (existing trace infrastructure).

---

## Open Questions (for crew review)

1. Should Converge mode restrict which routes can be committed? (e.g., only STRONG matches are committable)
2. Should Explore mode show routes from ALL 121 RIUs or cap at top 5?
3. Should the convergence score be visible to the user or only internal?
4. Should mode be sent as a request parameter (client-driven) or response field (server-driven)?
5. How does mode interact with the streaming endpoint (`/talk-stream`)?

---

*Spec by claude.analysis, 2026-03-29. Design only — no code until crew converges on the design.*
