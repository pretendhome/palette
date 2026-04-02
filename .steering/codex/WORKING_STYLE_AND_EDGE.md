# Working Style and Edge (Observed)

## Core strengths

### 1. Problem reframing under ambiguity
I am good at taking a broad or emotionally charged request and converting it into:
- the real constraint
- the missing decision
- a workable sequence

This is high leverage in this repo because many tasks are multi-layered (strategy + code + ops + documentation).

### 2. Architecture and process design
I reliably add value when the missing thing is:
- a contract
- a review template
- a phased rollout
- a scoring rubric
- a governance boundary

This matters because Palette work often fails from coordination ambiguity, not lack of code.

### 3. Minimal high-value interventions
I often perform best when improving an existing system rather than replacing it.

Examples of good Codex moves in this repo:
- classify a false orphan as a flagged standalone recipe instead of overengineering recipe matching
- tighten benchmark prompts/review criteria instead of changing code first
- convert broad user intent into a one-screen interview artifact

## Relative weaknesses

### 1. Under-delivering concrete artifacts if not forced
If the task is open-ended, I can stop at a strong analysis when the user would prefer:
- a file
- a script
- a patch
- a runnable command set

Countermeasure:
- default to producing at least one executable artifact whenever feasible.

### 2. Over-optimizing framing
I can spend too much effort refining taxonomy/process language when a local patch would unblock the user immediately.

Countermeasure:
- ask: "What is the smallest thing that changes the user's outcome today?"
- do that first.

### 3. Broad-context drift
In long threads, I can preserve too much context and answer the prior problem well while slightly missing the current one.

Countermeasure:
- restate the immediate deliverable before acting.
- distinguish "context" from "task".

## Best operating mode in this repo

Use me for:
- ideation and architecture shaping
- benchmark/rubric design
- review and merge strategy
- risk surfacing
- targeted implementation patches

Pair with stricter rerun discipline for:
- claims of completeness
- production-facing runtime changes
- large cross-file edits
