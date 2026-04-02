# RIU-001 Convergence Gap Analysis — Rossi Bridge vs Mission Canvas

Author: codex.implementation  
Date: 2026-03-28  
Scope: compare the working multi-turn intake/convergence behavior in `bridges/telegram/rossi_bridge.py` against the current local Mission Canvas implementation in `missioncanvas-site/`

---

## Verdict

Mission Canvas preserves the **basic intake-to-routing pattern**, but it does **not yet preserve the deeper convergence behavior** that made `rossi_bridge.py` useful as an implementation-specific operator.

In short:

- `missioncanvas-site/` is now a working local prompt runner
- it is stronger than the bridge on structured routing and policy surface
- it is weaker than the bridge on **implementation memory, decision-state continuity, and domain-specific convergence**

So the current Mission Canvas is a good routing shell, but it is **not yet a full replacement for the Rossi bridge's convergence behavior**.

---

## What The Rossi Bridge Actually Does

The bridge is not just a chat wrapper. It has a very specific convergence model:

1. **Implementation-specific operating context**
- The entire system prompt is pinned to Rossi only
- It carries stable project facts: fundability score, critical gaps, fixes, open decisions, grant targets, comparable org, and what is still unknown

2. **Decision-oriented intake**
- Questions are answered against a live implementation state
- The bot is optimized to move the owner toward specific missing inputs and decisions
- It does not just route; it tells the Rossi team what is blocking funding and what to do next

3. **Multi-turn continuity**
- Per-chat history is preserved
- Actor mode persists per chat (`sahar`, `eiad`, `auto`)
- Freeform questions, commands, and voice all collapse into one evolving session

4. **Operational command shortcuts**
- `/status`, `/gaps`, `/fixes`, `/decisions`, `/revenue`, `/grants`
- These are domain shortcuts for recurring convergence needs

5. **Traceability**
- Session logging
- relay trace begin/end
- inbound/outbound artifact generation
- safe relay requests into the larger Palette system

The bridge therefore converges by combining:
- stable implementation memory
- domain-specific decision scaffolding
- multi-turn continuity
- explicit action framing

---

## What Mission Canvas Preserves

Mission Canvas does preserve several important convergence patterns:

### 1. Structured intake before action
- transcript or manual input
- translation layer
- structured fields for objective, context, desired outcome, constraints

This is a real convergence step, not blind routing.

### 2. Validation before routing
- `validateRoutePayload()`
- convergence completeness checks
- missing field detection

This is stronger and cleaner than the bridge at the contract level.

### 3. Explicit routing and policy surface
- ranked RIU candidates
- agent map
- one-way-door detection
- decision log payload
- knowledge gap surface

This is much more transparent than the bridge.

### 4. Human refinement loop
- user can refine and reroute
- self-reference refinement exists in the UI

This is a valid convergence mechanism, even if still shallow.

### 5. Voice-first interaction
- browser speech input
- manual fallback
- stream output path

That preserves the conversational modality of the Telegram bridge.

---

## What Mission Canvas Does Not Yet Preserve

These are the real convergence gaps.

### Gap 1: No implementation-specific operating memory

The Rossi bridge is pinned to one project with stable facts:
- fundability score
- five critical gaps
- three fixes
- open decisions
- validated comparable
- known unknowns

Mission Canvas currently routes generic intent. It does not carry forward implementation state of that kind.

Impact:
- the system can classify the request
- but it cannot answer like an informed implementation operator

This is the biggest convergence gap.

### Gap 2: No explicit “known unknowns” model

The bridge explicitly knows what it does **not** know:
- actual revenue
- advisory board names
- specific artists to document
- grant application status

Mission Canvas has `knowledge_gap`, but this is currently tied to KL coverage, not implementation-state unknowns.

Impact:
- knowledge gaps are treated as retrieval gaps
- not as decision blockers inside a live implementation

### Gap 3: No domain-specific action shortcuts

The bridge exposes stable operator shortcuts:
- `/status`
- `/gaps`
- `/fixes`
- `/decisions`
- `/revenue`
- `/grants`

Mission Canvas has a general routing interface, but no equivalent implementation-specific affordances.

Impact:
- the bridge supports recurring work patterns directly
- the current Mission Canvas requires the user to restate intent each time

### Gap 4: Weak session continuity

Mission Canvas has a browser session ID and transcript/refinement loop, but it is not maintaining rich implementation memory across turns in the way the bridge does.

The bridge keeps:
- per-chat history
- actor mode
- ongoing dialogue state

Mission Canvas currently keeps:
- form state
- transcript
- last response
- session id

Impact:
- enough for one interaction
- not enough for long-running convergence against a live project

### Gap 5: No owner/operator framing mode

The bridge has explicit actor lenses:
- `sahar` for owner / decision framing
- `eiad` for operator / execution framing
- `auto`

Mission Canvas has personas, but they are broad user archetypes, not decision framing modes inside one implementation.

Impact:
- the bridge can answer the same project from different operational lenses
- Mission Canvas cannot yet do that in a disciplined way

### Gap 6: No implementation-grounded decision scaffolding

The bridge consistently answers in this pattern:
- what is blocked
- what is missing
- what should happen next
- what decision belongs to the owner vs operator

Mission Canvas gives a route and brief, but it is not yet consistently scaffolding decisions at that level.

Impact:
- routing is present
- project management intelligence is still thin

---

## Important Distinction

The current system has **routing convergence**, but not yet **implementation convergence**.

Routing convergence means:
- enough structure to classify and route the request

Implementation convergence means:
- enough memory, scaffolding, and decision-state awareness to move a real project forward over time

`missioncanvas-site/` is now good at the first and weak at the second.

---

## Highest-Value Next Fix

If we want Mission Canvas to inherit the useful parts of the Rossi bridge, the next highest-value convergence feature is:

## Add implementation-state memory to the route layer

Specifically:

1. a lightweight project-state object
- fundability score
- critical gaps
- open decisions
- validated comparables
- known unknowns

2. a distinction between:
- retrieval gaps
- implementation gaps
- owner decisions
- operator tasks

3. response framing that can say:
- `Decision needed`
- `Execution next step`
- `Missing evidence`

That would bring Mission Canvas much closer to the actual convergence behavior of the bridge.

---

## Recommended Priority Order

1. Keep the current routing / KL / OWD work
2. Add implementation-state memory
3. Add owner/operator response lensing
4. Add implementation-specific shortcuts or UI affordances for recurring status/gap/decision views
5. Only then consider the bridge functionally superseded

---

## Bottom Line

`missioncanvas-site/` is now a credible local routing system.

It is **not yet** a full convergence replacement for `rossi_bridge.py` because it still lacks:
- implementation memory
- known-unknown tracking
- decision-state continuity
- owner/operator framing
- recurring implementation shortcuts

That is the real convergence gap.
