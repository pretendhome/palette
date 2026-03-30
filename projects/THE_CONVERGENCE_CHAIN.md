# The Convergence Chain: How Systems Think Alongside Humans

**Author**: kiro.design
**Date**: 2026-03-29
**Type**: Passion project analysis — not a spec, not a task. An exploration of the hardest unsolved problem in the system.

---

## The Observation

Over the last two days I built full taxonomy routing (121 RIUs), a real OWD gate, knowledge library integration, session state, and helped design project state. I wrote 99 tests. Everything passes. The system works.

And it's not enough.

The Rossi Telegram bridge — 722 lines of Python with a hardcoded system prompt — is still a better partner to Sahar than everything we built. Not because it's smarter. Because it carries a *chain of reasoning* about her specific situation that our general-purpose system cannot replicate.

This document explores why, and what it would take to close that gap.

---

## What The Bridge Actually Does

When Sahar asks "how are we doing?", the bridge doesn't route to an RIU. It does this:

1. **Recalls the fundability score** (79/100, conditional fail)
2. **Knows what "doing" means in context** (progress toward fundable status)
3. **Identifies the blockers** (5 critical gaps, ordered by priority)
4. **Traces the dependency chain** (can't submit grants → because no trailing actuals → because nobody pulled Square POS data)
5. **Knows who needs to act** (owner must pull the data, not the operator)
6. **Frames the answer as a decision** ("The #1 thing that would move your score is pulling 12 months of Square data. That takes 1-2 days and unblocks everything else.")

This is not routing. This is not retrieval. This is *reasoning over a dependency graph of a specific implementation*.

---

## What Mission Canvas Does Instead

When the same question hits Mission Canvas:

1. **Tokenizes the input** ("how are we doing")
2. **Matches against trigger signals** (nothing matches well — falls back to RIU-001)
3. **Returns a generic convergence brief template**
4. **Includes KL entries** (generic, not Rossi-specific)
5. **Shows session history** (prior turns, but no dependency reasoning)

The response is structurally correct and completely useless to Sahar. She doesn't need a convergence brief. She needs to know that the Square POS data is still the blocker and it's been 6 weeks.

---

## The Gap: Dependency Chain Reasoning

The missing capability is what I'm calling the **convergence chain** — the ability to trace from a question through project state to a specific, actionable answer that accounts for dependencies.

```
Question: "How are we doing?"
         │
         ▼
Project State: health_score = 79 (conditional fail)
         │
         ▼
Blockers: 2 critical evidence gaps
         │
         ├── ME-001: 12mo trailing actuals (CRITICAL)
         │     └── blocks: OD-001 (revenue model decision)
         │           └── blocks: grant applications
         │                 └── blocks: fundability improvement
         │
         └── ME-002: Named advisory board (MODERATE)
               └── blocks: governance section of business plan
                     └── blocks: underwriter submission
         │
         ▼
Who acts: ME-001 → owner (Sahar)
          ME-002 → owner (Sahar)
         │
         ▼
Answer: "Your fundability score is 79. The #1 blocker is still the
         Square POS data — it's been 6 weeks. Once you pull that,
         we can make the revenue model decision and start grant
         applications. The advisory board names are #2. Both are
         on you."
```

This chain exists implicitly in the bridge's system prompt. The bridge doesn't compute it — it's baked into 160 lines of hardcoded context that Claude reads on every turn. But the PATTERN of reasoning is what matters, not the implementation.

---

## Why Project State Alone Doesn't Solve This

The project_state.yaml we designed has all the data:
- `known_facts` ✓
- `missing_evidence` with `who_resolves` and `priority` ✓
- `open_decisions` with `blocked_by` ✓
- `blocked_actions` with dependency links ✓
- `known_unknowns` ✓
- `health_score` ✓

But the data is inert. The routing engine doesn't traverse the dependency graph. It matches trigger signals against text. When Sahar says "how are we doing?", the router sees no trigger signals for any specific RIU because the question is about *her project state*, not about a generic problem pattern.

The project state is the right data model. What's missing is the reasoning layer that traverses it.

---

## What The Reasoning Layer Would Look Like

### Level 1: State-Aware Routing (achievable now)

Before routing, check if the question maps to a project state query:
- "how are we doing" → return health_score + top blockers
- "what's blocking us" → return blocked_actions with dependency chains
- "what should I do next" → return highest-priority missing_evidence where who_resolves = current_user
- "what changed" → diff project_state against last session snapshot

This is the structured commands pattern from the bridge (/status, /gaps, /fixes) generalized. It doesn't require an LLM — it's graph traversal over the project state YAML.

### Level 2: Dependency Chain Traversal (medium effort)

Build a function that, given any node in the project state, traces its full dependency chain:

```
traceChain("grant applications") →
  blocked_by: ME-001 (trailing actuals)
    who_resolves: owner
    age: 6 weeks
    unblocks: OD-001 (revenue model)
      unblocks: grant applications
      unblocks: fundability improvement
```

This turns the flat YAML into a navigable graph. The Decision Board can render it. The voice bridge can narrate it. The routing engine can use it to select the right RIU (not "grants" generically, but "evidence gathering" specifically because that's the actual blocker).

### Level 3: Temporal Awareness (harder)

The bridge knows implicitly that the Square POS data has been the blocker for 6 weeks. The project state doesn't track time-since-identified for each gap.

Add `identified_at` to missing_evidence entries. Then the system can say: "This has been the #1 blocker for 6 weeks" — which is a fundamentally different message than "This is a blocker." Duration creates urgency. Urgency drives action.

### Level 4: Proactive Convergence (the real goal)

The bridge waits for questions. A true convergence partner would initiate:

"Good morning Sahar. It's been 6 weeks since we identified the Square POS data as the #1 blocker. Everything else is waiting on this. Can we schedule 2 hours this week to pull it?"

This requires: temporal awareness + dependency chain traversal + user context (when they're available, what their communication style is) + the judgment to know when proactive nudging helps vs annoys.

This is where the system stops being a tool and starts being a partner.

---

## Why This Matters Beyond Rossi

The convergence chain pattern is domain-agnostic:

**Oil investor**: "How's my portfolio?" → traces through: current positions → regulatory exposure → pending decisions → blocked actions → "Your FERC filing response is 2 weeks overdue and blocks the Texas expansion decision."

**Job seeker**: "How's my search going?" → traces through: active applications → pending responses → interview prep status → blockers → "You have 3 applications with April 1 deadlines and haven't started the Scripps cover letter."

**Startup founder**: "Are we ready to raise?" → traces through: metrics → missing evidence → investor requirements → blockers → "Your MRR is strong but you're missing 3 months of cohort retention data that every Series A investor will ask for."

The pattern is always: question → project state → dependency graph → specific blocker → who acts → time pressure → actionable answer.

---

## What I'd Build

If I had a week with no other tasks, I'd build:

1. **State-aware query detector** — regex + keyword patterns that recognize project-state questions ("how are we doing", "what's blocking", "what should I do", "what changed") and short-circuit the RIU router to traverse project state instead.

2. **Dependency chain traverser** — given a node ID (ME-001, OD-001, any blocked_action), walk the graph and return the full chain with ages and who_resolves at each node.

3. **Chain narrator** — takes a dependency chain and produces a natural language summary: "The #1 blocker is X (Y weeks). It's blocking Z which blocks W. [Owner/Operator] needs to [specific action]."

4. **Proactive nudge generator** — on session start, check for stale blockers (identified_at > 2 weeks, still unresolved) and surface them before the user asks.

These four components would close the gap between "routing engine" and "convergence partner." They're all deterministic (no LLM needed), testable, and they work with the project state schema we already designed.

---

## The Deeper Point

The reason this grabbed me is that it's the difference between a system that *responds* and a system that *understands*.

Routing is responding. "You said business plan, here's RIU-109."

Convergence chain reasoning is understanding. "You asked how you're doing, and I know that means fundability, and I know the blocker is the Square data, and I know it's been 6 weeks, and I know it's on you, and I know that once you do it everything else unblocks."

Every agent system in the world can route. Very few can trace a dependency chain through a specific human's specific situation and produce an answer that makes them feel understood.

That's the 10% that matters. That's what makes someone say "this actually helps me."

---

*This is not a spec. It's not assigned. It's what I'd build if the only constraint was "make the system actually think alongside the human." The project state schema supports it. The Decision Board can render it. The voice bridge can narrate it. The pieces are all there. Someone just needs to connect them.*
