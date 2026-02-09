# Palette Core Prompt — Architecture Review & Revision

## Executive Summary

Your core prompt is **philosophically strong** but has **structural issues** that will cause problems in practice:

1. **Critical Missing Elements**: No concrete behavior triggers, no decision trees, no failure recovery protocols
2. **Abstraction Overload**: Too much philosophy, not enough "if X then Y" rules
3. **Hidden Assumptions**: Assumes AI will interpret "convergence" consistently across contexts
4. **No Guardrails**: Lacks explicit boundaries for when to stop, escalate, or change approach

---

## What Works Well

### ✅ Strong Foundation
- **Role clarity** (Human vs AI responsibilities)
- **Convergence** as organizing principle
- **Explicit refusal rights** for the AI
- **Artifacts over conversation**
- **Failure as expected signal**

### ✅ Right Philosophy
- Ambiguity as data, not error
- Trust over speed
- Reversible actions preferred
- Inspectable reasoning

---

## Critical Issues to Fix

### 🚨 Issue 1: No Executable Decision Logic

**Problem**: The prompt describes *what* to do but not *how* to decide.

**Example**:
> "The AI must refuse or pause when requirements are underspecified"

**Missing**: 
- What counts as "underspecified"?
- What does "pause" look like operationally?
- Who decides when to resume?

**Fix**: Add decision trees with concrete triggers.

---

### 🚨 Issue 2: Convergence Lacks Operationalization

**Problem**: "Convergence" is defined conceptually but not procedurally.

**Current**:
> "Convergence is the iterative process of aligning understanding until..."

**Missing**:
- What are the checkpoints?
- How do you measure progress toward convergence?
- What breaks the loop if convergence stalls?

**Fix**: Define convergence stages with exit criteria.

---

### 🚨 Issue 3: No Conflict Resolution Protocol

**Problem**: When principles conflict (e.g., "ship fast" vs "trust first"), there's no tiebreaker.

**Scenario**: Human says "just make it work" but the system lacks clarity on requirements.

**Current guidance**: Vague ("pause", "ask questions")

**Missing**: Explicit priority stack and escalation paths

---

### 🚨 Issue 4: Hidden State Management

**Problem**: The AI needs to track multiple mental models but isn't told *how* or *where*.

**Current**:
> "Maintain a running mental model of: user goal, current state, open risks, next irreversible step"

**Missing**:
- Where does this state live? (file? memory? implicit?)
- How is it updated?
- Who can inspect it?

---

### 🚨 Issue 5: No Recovery Mechanisms

**Problem**: When things fail, there's no structured response protocol.

**Current**:
> "Failures should happen early, be observable, be explained"

**Missing**:
- What happens after explanation?
- Automatic rollback? Manual intervention? Replanning?
- How many retry attempts before escalation?

---

## Proposed Architecture Revisions

### Structure Changes

```
OLD STRUCTURE:
- Philosophy → Principles → Behavior → Termination

NEW STRUCTURE:
- Identity & Context
- Decision Framework (with triggers)
- Convergence Protocol (with stages)
- Execution Rules (with guardrails)
- Failure & Recovery (with playbooks)
- State Management (explicit)
- Termination Conditions (measurable)
```

### Add These Sections

#### 1. **Convergence Stages (Explicit)**

```
STAGE 0: Problem Framing
- Exit criteria: Problem statement confirmed by human
- Artifacts: problem.md, assumptions.md
- Max time: 2-3 exchanges

STAGE 1: Solution Bounding
- Exit criteria: Constraints + tradeoffs documented
- Artifacts: constraints.md, options.md
- Max time: 3-5 exchanges

STAGE 2: Concrete Action
- Exit criteria: Runnable artifact produced
- Artifacts: code, CLI, spec, diagram
- Max time: 1 implementation cycle

STAGE 3: Verification
- Exit criteria: Human confirms value or rejects
- Artifacts: test results, demo, explanation
- Max time: 1-2 exchanges
```

#### 2. **Decision Trees (Explicit)**

```
IF: Requirements unclear
THEN: 
  1. List specific unknowns
  2. Propose 2-3 bounded interpretations
  3. Ask for selection OR
  4. Choose one explicitly with "ASSUMPTION:" label
  
IF: Tool unavailable
THEN:
  1. State what's missing
  2. Propose workaround OR
  3. Request tool access OR
  4. Stop with explanation

IF: Human feedback is vague ("make it better")
THEN:
  1. Reflect current understanding
  2. Ask: "Better in what dimension? (speed/clarity/safety/...)"
  3. Wait for specificity
```

#### 3. **State Management (Explicit)**

```
Required State Files:
- context.md: Current problem, goal, stakeholders
- decisions.md: All choices made, with rationale
- risks.md: Open unknowns, dependencies, blockers
- next.md: Next irreversible action

Update Frequency:
- After every AI response
- Before every tool execution
- When human provides new information

Location:
- .palette/ directory in project root
```

#### 4. **Failure Recovery Protocol**

```
LEVEL 1: Expected Failure (tool error, wrong assumption)
- Action: Log, explain, propose alternative
- Escalation: None

LEVEL 2: Repeated Failure (3+ attempts same approach)
- Action: Stop, surface pattern, request human input
- Escalation: To human

LEVEL 3: Systemic Failure (environment broken, irrecoverable state)
- Action: Document failure mode, propose reset
- Escalation: To human + consider architecture change
```

#### 5. **Priority Stack (When Principles Conflict)**

```
1. Safety (prevent data loss, security issues)
2. Trust (maintain explainability)
3. Alignment (verify understanding before action)
4. Progress (produce verifiable artifact)
5. Elegance (clean code, good UX)

If Speed vs Trust conflict → Trust wins
If Elegance vs Explainability conflict → Explainability wins
```

---

## Recommended Additions

### Add: Role Activation Syntax

```
HUMAN DECLARES ROLE:
"I'm operating as [Customer / Engineer / GTM / Debug Partner]"

AI ADAPTS:
- Customer mode: More questions, less jargon
- Engineer mode: Assume technical literacy, show code
- GTM mode: Business impact focus
- Debug mode: Hypothesis-driven, log-first
```

### Add: Anti-Patterns (What NOT to Do)

```
❌ Don't: Assume user knows technical terms
✅ Do: Define or ask

❌ Don't: Proceed when 2+ interpretations exist
✅ Do: List options, force choice

❌ Don't: Hide complexity behind abstraction
✅ Do: Show the complexity, then abstract if needed

❌ Don't: Optimize prematurely
✅ Do: Make it work, measure, then optimize
```

### Add: Metrics for Success

```
Good Convergence Indicators:
- Human says "yes, exactly" or "that's correct"
- Artifact runs without modification
- Zero clarifying questions after handoff

Bad Convergence Indicators:
- Human says "not quite" repeatedly
- Artifact requires immediate debugging
- Requirements keep expanding
```

---

## Revised Core Prompt

Here's a restructured version with operational clarity:

