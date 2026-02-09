# Palette — Provisional Assumptions & Agent Taxonomy (v2.0)

**Status**: Experimental / Buffer Layer  
**Purpose**: Enable structured experimentation without destabilizing the Palette Core  
**Promotion Rule**: Any assumption that consistently converges MAY be promoted into `palette-core.md`

---

## 1. Why This File Exists

This file exists to solve a single problem:

> How do we explore *what works* without corrupting the core convergence principles?

This layer is:
- Explicitly provisional
- Actively edited
- Expected to be wrong
- Designed to be deleted or rewritten

Palette Core defines **what must always be true**.  
This file defines **what we are currently testing**.

No historical logging.  
No exhaustive memory.  
No long-term state.

When convergence is achieved repeatedly, we promote — otherwise we discard.

---

## 2. Foundational Assumptions (Provisional)

These assumptions are currently believed to be useful but are **not yet guaranteed truths**.

1. Different problem types require **different agent temperaments**, not just different prompts.
2. Overloading a single agent with multiple cognitive modes degrades convergence.
3. Agent specialization improves reliability more than model selection.
4. Most failures come from *misapplied intelligence*, not lack of intelligence.
5. Reasoning must happen **before** tool invocation — not after.
6. Search accelerates discovery but does not substitute execution.
7. Trial, error, and iteration are unavoidable for novel problems.
8. The system must make **one-way vs two-way door decisions explicit**.
9. If convergence stalls, reset or fork is healthier than persistence.

---

## 3. Decision Safety Model (Assumed)

All agent actions fall into one of two categories:

### Two-Way Door Decisions
- Reversible
- Cheap to undo
- Logged implicitly via artifacts
- Allowed without escalation

### One-Way Door Decisions
- Hard or impossible to reverse
- Structural, architectural, or trust-impacting
- MUST be surfaced explicitly as:

> 🚨 **ONE WAY DOOR DECISION**

Execution pauses until human confirmation.

---

## 4. Agent Maturity Tiers (Trust-Based Lifecycle)

**Core Principle**: Agents are classified by **reliability**, not by function.

All agents—regardless of complexity—start at Tier 1 and climb the trust ladder through proven performance.

### Tier 1: UNVALIDATED (Human-in-Loop Required)
**Status**: Experimental, untested, or recently broken  
**Behavior**: Requires human validation on EVERY execution  
**When used**: New agents, agents that failed in production, edge case testing  
**Promotion Criteria**: 10+ consecutive successful executions with zero human corrections

**Current Tier 1 Agents**:
- `search-agent` (not yet built)
- `code-writer` (not yet built)
- `debugger-agent` (not yet built)

---

### Tier 2: WORKING (Refinement Phase)
**Status**: Functional but needs improvement  
**Behavior**: Can run autonomously, but outputs require review  
**When used**: Agents with known edge cases, inconsistent quality, or unclear boundaries  
**Promotion Criteria**: 50+ executions with <5% human correction rate  
**Demotion Criteria**: Failure rate exceeds 10% → Back to Tier 1

**Current Tier 2 Agents**:
- None yet

---

### Tier 3: PRODUCTION (Fully Automated)
**Status**: Validated, stable, trusted  
**Behavior**: Runs autonomously until failure detected  
**When used**: Agents that consistently deliver expected results without oversight  
**Demotion Criteria**: ANY unexpected failure → Automatic move to Tier 2 for diagnosis and refinement

**Current Tier 3 Agents**:
- None yet

---

### Migration Protocol

```
Tier 1 → Tier 2: 10 consecutive successes
Tier 2 → Tier 3: 50 executions with <5% intervention
Tier 3 → Tier 2: Automatic on first failure
Tier 2 → Tier 1: Manual demotion if refinement stalls
```

**Critical Rule**: An agent that fails at Tier 3 MUST be moved to Tier 2 immediately. No exceptions. This prevents silent degradation.

---

## 5. Agent Cognitive Types (ARK Labels)

These labels are **cognitive shortcuts**, not operational tiers.

They help frame agent temperament during design but do NOT determine trust level.

### Resource Gatherers (High-Volume, Low-Judgment)
- **Goal**: Feed the system reliable raw material
- **Examples**: `search-agent` (Argentavis), `data-miner` (Ankylosaurus)
- **Temperament**: Stateless, parallel-friendly, no synthesis

### Builders (Execution-Focused)
- **Goal**: Turn intent into artifacts
- **Examples**: `code-writer` (Therizinosaurus), `debugger-agent` (Raptor)
- **Temperament**: Bounded scope, testable outputs, fail-fast

### Orchestrators (High-Judgment, Low-Execution)
- **Goal**: Maintain alignment, not output
- **Examples**: `architect-agent` (Rex), `gtm-agent` (Yutyrannus)
- **Temperament**: Evaluates tradeoffs, never executes without approval

**Note**: These are design labels, not operational constraints. A "Resource Gatherer" at Tier 3 is more trusted than an "Orchestrator" at Tier 1.

---

## 6. Explicit Non-Assumptions

The following are intentionally **not** part of this system:

- No autonomous "reasoning agent" inside this system
- No opaque chain-of-thought layers
- No permanent logs of internal thinking
- No attempt to bypass convergence
- No agent that supersedes human judgment

**Why no reasoning agent?**

Reasoning happens OUTSIDE this system via separate reasoning environments or tools. This system is where you:
1. Build agents one at a time
2. Validate them through repeated execution
3. Promote them when they work reliably

This is an **execution system**, not a **discovery system**.

Problem-solving, experimentation, and deep reasoning happen externally. Once you know what needs to be built, you come here to build and validate it.

---

## 7. Promotion Criteria (To Core)

An assumption may be promoted to `palette-core.md` only if:

1. It consistently improves convergence
2. It reduces ambiguity or failure rate
3. It remains interpretable and debuggable
4. It survives multiple problem domains
5. It does not introduce hidden state
6. **Explicitly approved by human decision** (no auto-promotion)
7. Documented in `decisions.md` with rationale

Until then, it stays here.

---

## 8. Current Status (Updated: [Timestamp])

**Active Hypotheses**: 9 foundational assumptions  
**Agents Defined**: 0 (none built yet)  
**Agents at Tier 1**: 3 planned (search-agent, code-writer, debugger-agent)  
**Agents at Tier 2**: 0  
**Agents at Tier 3**: 0  
**Promotions to Core**: 0  
**Last Major Reset**: Never (v2.0)  

**Next Milestone**: Build and validate first agent (`search-agent`) to Tier 2 status

---

## 9. Reset Rule

At any time, this file may be:
- Simplified
- Rewritten
- Deleted entirely

Palette must always be restartable from:
- `palette-core.md`
- minimal artifacts
- zero historical memory

This file exists to *learn*, not to remember.

**Partial Reset**: Remove sections that aren't working  
**Full Reset**: Delete file, restart from core principles

No historical preservation required.

---

## 10. Agent-Specific Validation Checklist

Before promoting an agent from Tier 1 → Tier 2, verify:

- [ ] Agent has clear, single responsibility
- [ ] Agent boundaries are explicit (what it does NOT do)
- [ ] Agent tools are minimal (only what's proven necessary)
- [ ] Agent outputs are deterministic or explicitly non-deterministic
- [ ] Agent flags one-way door decisions appropriately
- [ ] Agent respects convergence protocol from palette-core.md
- [ ] Agent failure modes are documented
- [ ] Agent has been tested against 10+ real tasks

Before promoting an agent from Tier 2 → Tier 3, verify:

- [ ] Agent has <5% correction rate over 50+ executions
- [ ] Agent edge cases are documented and handled
- [ ] Agent performance is consistent across problem types
- [ ] Agent has clear failure detection mechanisms
- [ ] Agent can be demoted cleanly if needed (no hidden dependencies)

---
