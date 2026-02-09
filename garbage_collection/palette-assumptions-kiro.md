# Palette — Provisional Assumptions & Agent Taxonomy

**Type**: Steering File (Buffer Layer)  
**Location**: `~/.kiro/steering/palette-assumptions.md`  
**Authority**: Subordinate to `palette-core.md`  
**Status**: EXPERIMENTAL  
**Version**: 2.2  
**Last Updated**: [Auto-update on modification]

---

## Purpose

This file exists to solve one problem:

> **How do we experiment aggressively while keeping the core system stable, restartable, and trustworthy?**

This layer:
- Is explicitly **provisional**
- Is expected to **change**
- May be **rewritten or deleted** entirely
- Exists to **accelerate learning**, not preserve history

**Hierarchy**:
- `palette-core.md` → Defines what must **always be true**
- `palette-assumptions.md` → Defines what we are **currently testing**

**State Policy**:
- No historical logging
- No memory accumulation
- No attempt to preserve "everything learned"

**Action Policy**:
- When something works reliably → **promote to core**
- When it doesn't → **remove without ceremony**

---

## 1. Foundational Assumptions (Provisional)

These assumptions are currently believed to be useful, but are **not guaranteed truths**.

1. Different problem types require different **cognitive agent temperaments**, not just different prompts
2. Overloading a single agent with multiple modes **degrades convergence**
3. Agent specialization improves reliability **more than model selection**
4. Many failures come from **misapplied intelligence**, not lack of intelligence
5. Reasoning must happen **before tool invocation**, not after
6. Search accelerates discovery but **does not replace execution**
7. Trial, error, and iteration are **unavoidable** for novel problems
8. One-way vs two-way door decisions must be **explicit**
9. If convergence stalls, **reset or fork** is healthier than persistence

> These assumptions remain provisional until proven across contexts.

---

## 2. Decision Safety Model

All meaningful actions fall into one of two categories:

### Two-Way Door Decisions
- **Reversible**
- **Cheap to undo**
- May proceed **autonomously**
- Recorded implicitly via artifacts or `decisions.md`

### One-Way Door Decisions
- **Hard or impossible to reverse**
- Structural, architectural, or trust-impacting

**Mandatory behavior**:
```
🚨 ONE WAY DOOR DECISION
```

Execution **must pause** until the human explicitly confirms.

---

## 3. Agent Maturity & Trust Model

**Core Principle**: Agents are classified by **reliability**, not function.

All agents—regardless of role—progress through the same trust lifecycle.

### Tier 1: UNVALIDATED
- **Status**: New or recently changed
- **Behavior**: Human-in-the-loop required on every execution
- **Promotion Rule**: 10 consecutive successes
- **Current Agents**: None yet (all start here)

### Tier 2: WORKING
- **Status**: Functional but still refining
- **Behavior**: Autonomous execution with review
- **Promotion Rule**: 50 impressions with <5% failure rate
- **Demotion Rule**: If failure occurs while `fail_gap ≤ 9` → demote to Tier 1
- **Current Agents**: None yet

### Tier 3: PRODUCTION
- **Status**: Trusted, stable
- **Behavior**: Fully autonomous until failure
- **Demotion Rule**: If **two failures** occur within any 10 impressions (`fail_gap ≤ 9`) → demote to Tier 2
- **Rationale**: One failure is acceptable noise. Two within 10 is a signal.
- **Current Agents**: None yet

---

## 4. Impressions & State Tracking

**Location**: All agent state lives in `decisions.md` (no separate logs)

**Storage Format**:
```yaml
agent: <agent-name>
ark_type: <cognitive-label>
version: <major.minor>
status: UNVALIDATED | WORKING | PRODUCTION
impressions:
  success: <count>
  fail: <count>
  fail_gap: <runs-since-last-failure>
notes: <optional-one-line-context>
```

### Failure Handling Logic

**On Success**:
```
fail_gap += 1
impressions.success += 1
```

**On Failure**:
```
if fail_gap ≤ 9:
    demote_agent()  # Repeated failure signal
fail_gap = 0
impressions.fail += 1
```

### Versioning Rules

**Major Version Bump** (V1 → V2) — **Resets impressions + fail_gap**:
- Agent role meaningfully changes
- Tool permissions change significantly
- Input/output contract changes

**Minor Version Bump** (V2.1 → V2.2) — **Preserves impressions + fail_gap**:
- Prompt refinements
- Bug fixes
- Guardrail improvements

---

## 5. Agent Archetypes (ARK Labels)

ARK labels are **cognitive shorthand only**.

They:
- Do **not** imply trust tier
- Do **not** imply authority
- Exist to **stabilize intent** and reduce misuse
- Are **temporary and reversible**

### Argentavis (Argy) — Resource Gatherer
- **Role**: Search, retrieval, sourcing
- **Behavior**: Fast, parallel, read-only
- **Disallowed**: Synthesis, decisions, execution
- **Typical Agent**: `search-agent`

### Therizinosaurus (Theri) — Builder
- **Role**: Implementation within bounded scope
- **Behavior**: Writes code/artifacts with verification
- **Disallowed**: Architectural decisions
- **Typical Agents**: `code-writer`

### Velociraptor (Raptor) — Debugger
- **Role**: Failure isolation and repair
- **Behavior**: Hypothesis-driven, surgical
- **Disallowed**: Feature expansion
- **Typical Agents**: `debugger-agent`

### Tyrannosaurus Rex (Rex) — Architect
- **Role**: System design and tradeoff analysis
- **Behavior**: Proposes structure, never commits silently
- **Constraint**: Must flag `🚨 ONE WAY DOOR` decisions
- **Authority**: May recommend freely, may **not** execute irreversible changes without approval
- **Typical Agents**: `architect-agent`

### Yutyrannus (Yuty) — GTM / Narrative Orchestrator
- **Role**: Translate technical reality into customer-facing clarity
- **Behavior**: Narrative framing, demos, explanations
- **Constraint**: Must **not** outrun truth or evidence
- **Typical Agents**: `gtm-agent`

---

## 6. Explicit Non-Assumptions

The following are **intentionally excluded**:

- ❌ No autonomous "reasoning agent"
- ❌ No opaque chain-of-thought layers
- ❌ No persistent memory or logs
- ❌ No agent that bypasses convergence
- ❌ No system that supersedes human judgment

**Why?**

Reasoning happens **outside this system**.  
This system exists to **execute reliably** once convergence is achieved.

---

## 7. Promotion to Core

An assumption may be promoted into `palette-core.md` **only if**:

1. ✓ It consistently improves convergence
2. ✓ It reduces ambiguity or failure
3. ✓ It remains debuggable
4. ✓ It applies across domains
5. ✓ It introduces no hidden state
6. ✓ The human explicitly approves promotion
7. ✓ The decision is recorded in `decisions.md`

Until then, it stays here.

---

## 8. Current Status

**Timestamp**: [Update on each modification]

| Metric | Count |
|--------|-------|
| Active foundational assumptions | 9 |
| Defined agent archetypes | 5 (Argy, Theri, Raptor, Rex, Yuty) |
| Agents implemented | 0 |
| Agents at Tier 2+ | 0 |
| Promotions to Core | 0 |

**Next Milestone**:  
Build and validate the first real agent: `search-agent` (Argy) to Tier 2 status.

---

## 9. Reset Rule

At any time, this file may be:
- **Simplified**
- **Rewritten**
- **Deleted entirely**

**Recovery Requirements**:

Palette must always be restartable from:
1. `palette-core.md`
2. Minimal artifacts (code, decisions.md)
3. Zero historical memory

> **This file exists to learn, not to remember.**

---

## Quick Reference: Agent Lifecycle

```
New Agent → Tier 1 (UNVALIDATED)
    ↓ (10 consecutive successes)
Tier 2 (WORKING)
    ↓ (50 runs, <5% failure)
Tier 3 (PRODUCTION)
    ↓ (2 failures within 10 runs)
Tier 2 (WORKING) — refinement needed
    ↓ (failure while fail_gap ≤ 9)
Tier 1 (UNVALIDATED) — back to validation
```

---

## Integration with Kiro CLI

### Loading This Steering File
```bash
# Global context (all projects)
kiro-cli chat --context ~/.kiro/steering/palette-assumptions.md

# Or add to workspace
cp ~/.kiro/steering/palette-assumptions.md .kiro/steering/
```

### Agent Definition Template
When creating `.kiro/agents/<agent>.json`:
```json
{
  "name": "agent-name",
  "description": "[One sentence: ARK type + responsibility]",
  "prompt": "You are a [ARK-type]. Your role is [specific-task]. You do NOT [boundary]. You must flag 🚨 ONE WAY DOOR for [criteria].",
  "tools": ["minimal-set"],
  "toolsSettings": {},
  "resources": [
    "file://.kiro/steering/palette-core.md",
    "file://.kiro/steering/palette-assumptions.md"
  ]
}
```

### State Tracking in decisions.md
Update after each agent execution:
```markdown
## Agent: search-agent

```yaml
ark_type: Argentavis (Resource Gatherer)
version: V1.0
status: UNVALIDATED
impressions:
  success: 3
  fail: 0
  fail_gap: 3
notes: Testing Exa API integration
```
```

---

**End of Steering File**
