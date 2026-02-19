# Palette Lenses — Integration Plan

**Status**: v0 — Manual activation only
**Date**: 2026-02-19
**Owner**: Palette core

---

## What lenses are (one line)

Optional context overlays that shape output framing — activated when the right agent is routing the right task to the right stakeholder context.

---

## When to activate each lens

### LENS-PM-001 (Product Decision)

**Activate when:**
- Yutyrannus is the primary routed agent
- Task signals: "should we", "roadmap", "prioritize", "launch", "go/no-go", "scope trade-off", "OKR"
- Output expected: a decision with an owner, not a summary

**Do not activate for:**
- Pure research or background context requests
- Low-level debugging or implementation tasks
- Exploratory drafts (no decision point yet)

**Example tasks that fit:**
- "Should we build feature X this quarter or scope it down?"
- "We have three approaches — which do we pick?"
- "Is this ready to launch?"

---

### LENS-ENG-001 (Engineering Execution)

**Activate when:**
- Therizinosaurus + Velociraptor are primary
- Task involves: implementation sequencing, integration handoff, release readiness, incident follow-through
- Output expected: ordered task slices with test and rollback plans

**Do not activate for:**
- Executive narrative or stakeholder communication
- Pure product strategy framing
- Research-only tasks

**Example tasks that fit:**
- "Plan the integration between X and Y services"
- "What's the release readiness checklist for this feature?"
- "We had an incident — structure the follow-through"

---

### LENS-DEV-001 (Developer Delivery)

**Activate when:**
- Therizinosaurus is primary and the output is runnable code or a test plan
- Task signals: "implement", "write the code", "fix this bug", "refactor", "add tests"
- Output expected: scoped tasks with explicit acceptance checks and a test strategy

**Do not activate for:**
- Executive communication
- Architecture strategy discussions
- Research tasks without a code artifact

**Example tasks that fit:**
- "Implement the eval loop for lens runs"
- "Fix the JSON parsing in Argy"
- "Add tests for the cheatsheet update path in the Telegram bridge"

---

## Integration points in the system

### 1. Corythosaurus (Cory) — intent resolver [v1 target]

Cory is the front door for all input. In v1, when Cory classifies a task, it should also emit a `suggested_lens` field in its output packet if task signals match a lens trigger pattern. The user confirms or overrides before execution.

Integration location: `palette/agents/corythosaurus/`
Required: Add lens signal patterns to Cory's slot-filling logic.

### 2. Orchestrator [v1 target]

The orchestrator routes tasks to agents. After routing is resolved, it should check if the active lens is compatible with the routed agent set. If Cory has suggested a lens and the agent set matches `palette_fit.primary_agents`, the orchestrator passes the lens context into the agent handoff packet.

Integration location: `palette/agents/orchestrator/`
Required: Accept optional `lens_id` field in the handoff packet; inject lens `output_contract` into the agent system prompt.

### 3. Kiro steering — Tier 2 assumptions [now]

The Tier 2 assumptions file should reference lenses as an available optional tool. No code change — just a documentation note that lenses exist and how to invoke them.

Integration location: `palette/.kiro/steering/palette/TIER2_assumptions.md`
Required: Add one section describing lenses and when to use them.

### 4. Telegram bridge [v0.5 — quick win]

Add a `/lens` command to the Telegram bridge. Users can activate a lens during a session:

```
/lens pm     — activate LENS-PM-001
/lens eng    — activate LENS-ENG-001
/lens dev    — activate LENS-DEV-001
/lens off    — deactivate current lens
/lens        — show current active lens
```

The active lens ID is stored in `ChatState` and injected as a prefix into the system prompt for the active mode.

Integration location: `palette/bridges/telegram/telegram_bridge.py`
Required: ~30 lines — add `active_lens` to `ChatState`, add `/lens` command handler, inject lens context into `reply()`.

### 5. Documentation [now — for GitHub visibility]

- `palette/README.md` — Add one paragraph under features describing lenses
- `palette/GETTING_STARTED.md` — Add a "Lenses" section
- `palette/CHANGELOG.md` — Log the lenses addition

---

## Integration sequence

```
v0 (now)
  Manual only. User explicitly activates a lens by referencing a lens ID.
  No system-level integration. Lens YAML files exist and are documented.
  Eval: collect 20+ baseline runs per lens.

v0.5 (Telegram bridge)
  /lens command added. Users activate lenses during interview or task sessions.
  Quick feedback loop via live sessions.

v1 (after 20+ eval runs)
  Cory emits suggested_lens in handoff packets.
  Orchestrator injects lens output_contract into agent prompts.
  Lens activation is suggested, not automatic — human confirms.

v2 (after eval metrics confirm gain)
  High-confidence automatic activation for well-validated patterns.
  Kill criteria enforced: if no gain on 2 of 4 metrics, lens is removed.
```

---

## Kill criteria (inherited from each lens YAML)

All three lenses share the same principle: if after 20+ comparable runs there is no measurable improvement on at least 2 of 4 target metrics, the lens is removed. No exceptions.

**Metrics by lens:**

| Lens | Metrics tracked |
|------|----------------|
| LENS-PM-001 | convergence_turn_count, artifact_rework_rate, gate_decision_time, owd_false_positive_rate |
| LENS-ENG-001 | implementation_rework_rate, defect_escape_rate, time_to_first_valid_artifact, rollback_readiness_score |
| LENS-DEV-001 | implementation_rework_rate, test_pass_rate_on_first_run, bug_reopen_rate, time_to_first_mergeable_artifact |

Current status: All three lenses are **pilot (v0.1)** with zero runs logged. Eval clock starts on first deliberate activation.

---

## What this does NOT change

- RIU routing (lenses have no authority over which RIU is selected)
- ONE-WAY DOOR gates (lenses do not modify reversibility decisions)
- Agent role boundaries (lenses shape framing; agents own execution)
- Tier 1 constraints (convergence before execution always holds)
