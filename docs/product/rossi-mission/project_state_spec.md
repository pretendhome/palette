# Project-State Object Spec — Mission Canvas V0.2

**Author**: kiro.design
**Date**: 2026-03-29
**Status**: PROPOSAL — requires team review + the operator approval before implementation

---

## Problem

Mission Canvas V0.1 is request-centric. Each interaction is independent (now with session history, but still shallow). The Rossi bridge works because it carries deep implementation state — fundability score, critical gaps, open decisions, known unknowns. Canvas needs the same.

Codex nailed it: "routing convergence" vs "implementation convergence." We have the first. This spec adds the second.

---

## Schema

```yaml
project_state:
  # Identity
  id: "rossi-mission"
  name: "Rossi Mission Project"
  owner: "sahar"          # who makes decisions
  operator: "the_operator"       # who executes
  created_at: "2026-02-01"
  last_updated: "2026-03-29"

  # Current objective (what we're working toward)
  objective: "Get Rossi to fundable status (80/100 → 95/100)"
  
  # Known facts (things we've confirmed)
  known_facts:
    - "791 Valencia Street, San Francisco"
    - "Graffiti art gallery + streetwear brand"
    - "50/50 profit split with artists"
    - "Fundability score: 79/100 (conditional fail)"
    - "Revenue model: retail-heavy, needs grant flip"

  # Missing evidence (things we need but don't have)
  missing_evidence:
    - id: "ME-001"
      what: "12 months trailing actuals from Square/Shopify POS"
      why: "Cannot validate $500K Year 1 projection without baseline"
      who_resolves: "owner"
      priority: "critical"
    - id: "ME-002"
      what: "Named advisory board members (3-5)"
      why: "Funders require governance visibility"
      who_resolves: "owner"
      priority: "moderate"

  # Open decisions (choices waiting on a human)
  open_decisions:
    - id: "OD-001"
      decision: "Flip revenue model from retail-heavy to grant-heavy?"
      options: ["Keep current (64% retail)", "Flip to Creative Growth model (45% retail, 26% grants)"]
      who_decides: "owner"
      blocked_by: "ME-001"
    - id: "OD-002"
      decision: "Which 2-3 artists to document for pipeline validation?"
      who_decides: "owner"
      blocked_by: null

  # Blocked actions (things we can't do yet and why)
  blocked_actions:
    - action: "Submit grant applications"
      blocked_by: "ME-001"
      unblocks: "OD-001"
    - action: "Finalize business plan for underwriter"
      blocked_by: ["ME-001", "ME-002", "OD-001"]

  # Known unknowns (things we know we don't know)
  known_unknowns:
    - "Actual monthly cash flow timing (burn rate vs grant arrival)"
    - "Whether artist pipeline thesis has any informal validation"
    - "Grant application status for any prior submissions"

  # Route hypothesis (current best guess for next RIU)
  route_hypothesis:
    riu_id: "RIU-109"
    confidence: "moderate"
    reason: "Business plan creation is the umbrella — but blocked on evidence"

  # Metrics
  health_score: 79
  health_label: "CONDITIONAL FAIL"
  turns_in_session: 0
```

---

## Where It Lives

**Per-project, persisted to disk.**

- Path: `projects/<project-id>/project_state.yaml`
- Loaded on first request with matching project_id
- Updated after each route response (append new facts, update decisions)
- Session state (in-memory) is ephemeral conversation. Project state is persistent knowledge.

The distinction:
- **Session**: "what did we talk about in the last 20 turns" (in-memory, dies with server)
- **Project**: "what do we know about Rossi" (on disk, survives restarts)

---

## How It Feeds Into Routing

On each request, if `project_id` is in the payload:

1. Load `project_state.yaml` from disk
2. Inject into `input.context`:
   - Known facts as searchable text
   - Missing evidence as "needs: X"
   - Open decisions as "decision pending: X"
   - Blocked actions as "blocked: X because Y"
3. This enriched context feeds into `pickRoutes()` — trigger signals match against the real project state
4. Response includes `project_state` summary so the UI can render the Decision Board

---

## How It Updates

After each route response:
- If the user provided new facts → append to `known_facts`
- If a decision was made → move from `open_decisions` to a `resolved_decisions` log
- If evidence was supplied → remove from `missing_evidence`
- If OWD was approved → update `blocked_actions`
- Write updated YAML to disk

Updates are TWO-WAY DOOR (reversible — we can always edit the YAML). The project state itself is never a ONE-WAY DOOR.

---

## API Contract Extension

```json
{
  "input": { ... },
  "session_id": "browser-session-123",
  "project_id": "rossi-mission"
}
```

New response field:
```json
{
  "project": {
    "id": "rossi-mission",
    "health_score": 79,
    "health_label": "CONDITIONAL FAIL",
    "missing_evidence": 2,
    "open_decisions": 2,
    "blocked_actions": 2,
    "known_unknowns": 3,
    "next_action": "Supply 12 months trailing actuals (ME-001)"
  }
}
```

---

## Relationship to Other V0.2 Specs

- **UX Modes (Claude)**: Project state determines mode. No project → Explore. Project loaded but incomplete → Converge. Project complete + route selected → Commit.
- **Decision Board (Mistral)**: The Decision Board IS the project state rendered. Beliefs = known_facts. Unknowns = known_unknowns. Blocked = blocked_actions. Needs owner = open_decisions where who_decides = owner.
- **Session state**: Session is conversation memory. Project is implementation memory. Both feed into routing context, but project persists across sessions.

---

## Bootstrap: Rossi

First implementation: load from existing Rossi data.

The bridge's ROSSI_SYSTEM prompt already contains all the project state — fundability score, 5 gaps, 3 fixes, open decisions. Extract it into `projects/rossi-mission/project_state.yaml` and the Canvas immediately knows everything the bridge knows.

---

## What This Enables

With project state, Canvas can answer like the bridge:
- "What's blocking funding?" → reads blocked_actions + missing_evidence
- "What should I do next?" → reads highest-priority missing_evidence or open_decision
- "How are we doing?" → reads health_score + known_facts
- "What changed?" → diffs project_state against last session

Without project state, Canvas can only route. With it, Canvas converges.
