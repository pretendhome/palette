# Decision Board Spec — Mission Canvas V0.2

**Author**: claude.analysis (reassigned from mistral-vibe.builder)
**Date**: 2026-03-29
**Status**: PROPOSAL — design only, no code
**Depends on**: Project-state object (Kiro, project_state_spec.md), UX Modes (Claude, ux_modes_spec.md)

---

## Problem

Mission Canvas V0.1 returns a single action brief per request. The user gets an answer but no visibility into the *state of their project* — what's known, what's missing, what's blocked, and what can execute now.

The Rossi bridge solved this with a dedicated fundability dashboard baked into the system prompt. Canvas needs a generic equivalent: the **Decision Board** — a live panel that renders the project state object and adapts to the current UX mode.

---

## What the Decision Board Shows

The Decision Board renders five sections from Kiro's `project_state` schema. Each section maps directly:

| Section | Source field | Render as |
|---------|-------------|-----------|
| **Beliefs** | `known_facts` | Green checkmarks — things confirmed true |
| **Unknowns** | `known_unknowns` | Amber question marks — things we know we don't know |
| **Missing Evidence** | `missing_evidence` | Red gaps with `who_resolves` badges |
| **Open Decisions** | `open_decisions` | Decision cards with options, `who_decides` badge, blocked-by links |
| **Blocked Actions** | `blocked_actions` | Gray locked items showing dependency chain |

Plus a header bar:

```
[ Project: Rossi Mission ]  Health: 79/100 CONDITIONAL FAIL  |  Mode: CONVERGE  |  2 gaps · 2 decisions · 2 blocked
```

---

## Mode-Adaptive Rendering

The Decision Board changes emphasis based on the current UX mode (from the UX modes spec):

### EXPLORE mode — "What we don't know"

**Dominant sections**: Unknowns, Missing Evidence

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ DECISION BOARD          Mode: EXPLORE           │
│ Health: --/100 (no project loaded)              │
├─────────────────────────────────────────────────┤
│ ❓ UNKNOWNS (dominant)                          │
│   • [large cards, expanded]                     │
│   • Each unknown links to suggested routes      │
│                                                 │
│ 🔴 MISSING EVIDENCE                            │
│   • [large cards, expanded]                     │
│   • "Research needed" badges prominent          │
│                                                 │
│ ── collapsed ──────────────────────────────     │
│ ✅ Beliefs (3)  │  📋 Decisions (2)  │  🔒 (2) │
└─────────────────────────────────────────────────┘
```

**Behavior**:
- Unknowns and Missing Evidence are expanded by default
- Beliefs, Decisions, Blocked are collapsed (show count only)
- Each unknown/gap shows a "Research this" action that triggers an Explore-mode route
- If no project is loaded, the board shows: "No project context. Start by describing your situation."

### CONVERGE mode — "What we believe vs what we know"

**Dominant sections**: Beliefs vs Missing Evidence (side-by-side), Open Decisions

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ DECISION BOARD          Mode: CONVERGE          │
│ Health: 79/100 CONDITIONAL FAIL                 │
├────────────────────┬────────────────────────────┤
│ ✅ BELIEFS (5)     │ 🔴 MISSING EVIDENCE (2)   │
│   ✓ 791 Valencia   │   ✗ 12mo trailing actuals  │
│   ✓ Graffiti + SW  │     → owner must supply    │
│   ✓ 50/50 split    │   ✗ Named advisory board   │
│   ✓ Score: 79      │     → owner must supply    │
│   ✓ Revenue model  │                            │
├────────────────────┴────────────────────────────┤
│ 📋 OPEN DECISIONS                               │
│   ┌──────────────────────────────────────────┐  │
│   │ OD-001: Flip revenue model?              │  │
│   │ Option A: Keep current (64% retail)      │  │
│   │ Option B: Creative Growth (45/26)        │  │
│   │ Blocked by: ME-001    Decides: owner     │  │
│   └──────────────────────────────────────────┘  │
│ ── collapsed ──────────────────────────────     │
│ ❓ Unknowns (3)  │  🔒 Blocked (2)             │
└─────────────────────────────────────────────────┘
```

**Behavior**:
- Beliefs and Missing Evidence are side-by-side for direct comparison
- Open Decisions are expanded with option cards
- Decision cards show blocked-by links (clicking scrolls to the gap)
- Convergence gaps (from UX modes spec) are highlighted inline
- "Fill this gap" actions on each Missing Evidence item

### COMMIT mode — "What can execute now"

**Dominant sections**: Blocked Actions (resolved vs remaining), Open Decisions (resolved)

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ DECISION BOARD          Mode: COMMIT            │
│ Health: 95/100 READY                            │
├─────────────────────────────────────────────────┤
│ 🚀 EXECUTION READINESS                         │
│   Route: RIU-109 Business Plan Creation         │
│   All evidence supplied ✓                       │
│   All decisions resolved ✓                      │
│                                                 │
│ ⚡ READY TO EXECUTE                             │
│   □ Submit grant applications                   │
│   □ Finalize business plan for underwriter      │
│                                                 │
│ 🔒 REMAINING BLOCKS (0)                        │
│   (none — all dependencies resolved)            │
│                                                 │
│ ── history ────────────────────────────────     │
│ ✅ Resolved: OD-001 → Option B (Creative Growth)│
│ ✅ Supplied: ME-001 (12mo actuals uploaded)      │
│ ✅ Supplied: ME-002 (3 advisors named)           │
│                                                 │
│ [⚠️ OWD GATE]  [Approve All]  [Back to Converge]│
└─────────────────────────────────────────────────┘
```

**Behavior**:
- Execution readiness summary at top
- Unblocked actions shown as a checklist
- Remaining blocks (if any) shown with dependency chain
- Resolved decisions and supplied evidence shown as history
- OWD gate visible if any committed actions are irreversible
- "Back to Converge" escape hatch always available

---

## Data Flow

```
project_state.yaml (disk)
        │
        ▼
   server.mjs loads on request
        │
        ▼
   Route response includes `project` summary
        │
        ▼
   app.js receives response
        │
        ├── Renders action brief (existing)
        │
        └── Renders Decision Board (new)
              │
              ├── Reads `response.project.*`
              ├── Reads `response.mode` (from UX modes)
              └── Adapts layout per mode
```

The Decision Board is a **read-only view** of project state. It does not modify state directly — all state changes flow through the routing/OWD pipeline:

- User supplies evidence → route request → server updates project_state → board refreshes
- User makes decision → route request → server resolves decision → board refreshes
- OWD approved → server unblocks actions → board refreshes

---

## Interaction Patterns

### 1. Gap-to-action links
Every Missing Evidence and Open Decision item is clickable. Clicking pre-fills the route input with the relevant context:

- Click "12mo trailing actuals" → input pre-fills: "I have 12 months of sales data from Square POS"
- Click "Flip revenue model?" → input pre-fills: "I want to go with Option B, the Creative Growth model"

This reduces friction from "I can see the gap" to "I can fill the gap" to one click.

### 2. Dependency visualization
Blocked actions show their dependency chain as linked badges:

```
🔒 Submit grant applications
   blocked by: ME-001 (12mo actuals)
               └── unblocks: OD-001 (revenue model)
                              └── unblocks: Finalize business plan
```

Clicking any node in the chain scrolls to that item.

### 3. Progress animation
When a gap is filled or decision resolved, the board animates the transition:
- Item slides from Missing Evidence to Beliefs (with green flash)
- Blocked action checks its dependency — if all met, slides to Ready to Execute
- Health score updates with counter animation

### 4. Board persistence
The board state is derived entirely from the server response — no client-side state. Refreshing the page reloads from project_state.yaml. This means the board is always consistent with the source of truth.

---

## HTML Structure

```html
<section id="decisionBoard" class="decision-board hidden">
  <header class="db-header">
    <span class="db-project-name"></span>
    <span class="db-health"></span>
    <span class="db-mode-badge"></span>
    <span class="db-summary"></span>
  </header>

  <div class="db-section db-beliefs">
    <h3>Beliefs <span class="db-count"></span></h3>
    <ul class="db-list"></ul>
  </div>

  <div class="db-section db-unknowns">
    <h3>Unknowns <span class="db-count"></span></h3>
    <ul class="db-list"></ul>
  </div>

  <div class="db-section db-missing">
    <h3>Missing Evidence <span class="db-count"></span></h3>
    <ul class="db-list"></ul>
  </div>

  <div class="db-section db-decisions">
    <h3>Open Decisions <span class="db-count"></span></h3>
    <div class="db-cards"></div>
  </div>

  <div class="db-section db-blocked">
    <h3>Blocked Actions <span class="db-count"></span></h3>
    <ul class="db-list"></ul>
  </div>
</section>
```

CSS classes control mode-adaptive rendering:
- `.decision-board[data-mode="explore"]` — unknowns/missing expanded, rest collapsed
- `.decision-board[data-mode="converge"]` — beliefs+missing side-by-side, decisions expanded
- `.decision-board[data-mode="commit"]` — execution readiness dominant, history visible

---

## Implementation Plan (when approved)

### Phase 1: Static rendering
1. Add `<section id="decisionBoard">` to index.html
2. Add `renderDecisionBoard(response)` to app.js
3. Parse `response.project` and `response.mode` fields
4. Render all 5 sections with counts and basic styling
5. Mode-adaptive CSS (expand/collapse per mode)

### Phase 2: Interactivity
1. Gap-to-action click handlers (pre-fill route input)
2. Dependency chain visualization
3. Collapsible sections with smooth transitions
4. Health score badge with color coding (green/amber/red)

### Phase 3: Integration with project state
1. Wire to Kiro's project_state.yaml loader in server.mjs
2. Add `project` field to route response
3. Bootstrap with Rossi project data
4. Test full loop: gap detected → user fills → board updates

### Phase 4: Polish
1. Progress animations (gap→belief transitions)
2. Convergence nudge integration (from UX modes spec)
3. Mobile-responsive layout
4. Accessibility (ARIA labels, keyboard navigation)

---

## Constraints

- Decision Board is READ-ONLY. It renders state, does not mutate it.
- All state changes flow through existing route/OWD pipeline.
- Board renders even without a project loaded (shows "no project context" message in Explore mode).
- Board must not block the action brief — both render simultaneously.
- No external API calls from the board — all data comes from the route response.
- Board collapses gracefully on mobile (single-column stack, all sections collapsible).

---

## Open Questions (for crew review)

1. Should the Decision Board be always visible (sidebar) or togglable (tab/panel)?
2. Should resolved decisions show full history or just the most recent 5?
3. Should the board show a timeline of state changes (audit trail)?
4. How should the board handle multiple projects? (project picker dropdown vs URL-based)
5. Should gap-to-action clicks auto-submit the route or just pre-fill?

---

*Spec by claude.analysis (reassigned from mistral-vibe.builder), 2026-03-29. Design only — no code until crew converges on the design.*
