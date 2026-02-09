# Intelligent Data Prelayer (IDP)
**Type**: Experimental Problem-Solving Framework  
**Authority**: Subordinate to `palette-core.md`  
**Status**: ACTIVE – TESTING GROUNDS  
**Purpose**: Map and test agent structures for solving problems of unknown complexity

---

## What This Is

The Intelligent Data Prelayer is Palette's **experimentation sandbox**—a structured methodology for decomposing problems, testing agent configurations, and discovering the minimal viable agent roster needed to solve a given challenge.

This is where you:
- Test agent specializations before committing to them
- Map problem domains to agent types
- Validate or discard organizational metaphors (like ARK)
- Learn what actually works under real pressure

**Core Principle**: Every problem-solving approach is provisional until proven in production.

---

## The IDP Process

### Phase 1: Problem Decomposition
Before spawning agents, decompose the problem into discrete operations.

**Ask**:
1. What are the **distinct types of work** required? (retrieval, computation, synthesis, validation)
2. Which operations are **parallelizable**? (can run independently)
3. Which operations are **sequential**? (depend on prior outputs)
4. What are the **irreversible decisions** (one-way doors)?
5. What are the **reversible experiments** (two-way doors)?

**Output**: A dependency graph showing work types and their relationships.

---

### Phase 2: Agent Hypothesis
Based on the decomposition, hypothesize the minimal agent set.

**Template**:
```
Problem: [Brief description]

Hypothesized Agents:
1. [Agent Name] (Role: [Type])
   - Responsibility: [Single clear task]
   - Tools Needed: [List]
   - Success Metric: [Observable outcome]
   - Risk: [What could go wrong]

2. [Agent Name] (Role: [Type])
   ...

Expected Bottlenecks:
- [Where will this likely fail?]

Exit Criteria:
- [How do we know when this is solved?]
```

**Rule**: Start with 1-3 agents maximum. Add more only when proven necessary.

---

### Phase 3: Agent Maturity Tiers (Lifecycle-Based)

Agents are NOT classified by function—they're classified by **trust level**.

#### Tier 1: UNVALIDATED (Human-in-Loop Required)
**Status**: Experimental, untested, or broken  
**Behavior**: Requires human validation on EVERY execution  
**Examples**: New agents, agents that failed in production  
**Promotion Rule**: After 10+ successful executions with zero human corrections → Move to Tier 2

#### Tier 2: WORKING (Refinement Phase)
**Status**: Functional but needs improvement  
**Behavior**: Can run autonomously, but outputs require review  
**Examples**: Agents with edge cases, inconsistent quality, or unclear boundaries  
**Promotion Rule**: After 50+ executions with <5% correction rate → Move to Tier 3  
**Demotion Rule**: If failure rate exceeds 10% → Move to Tier 1

#### Tier 3: PRODUCTION (Fully Automated)
**Status**: Validated, stable, trusted  
**Behavior**: Runs autonomously until failure detected  
**Examples**: Agents that consistently deliver expected results  
**Demotion Rule**: ANY unexpected failure → Automatic move to Tier 2 for diagnosis

**Migration Protocol**:
- Tier 1 → Tier 2: Requires 10 consecutive successes
- Tier 2 → Tier 3: Requires 50 executions with <5% human intervention
- Tier 3 → Tier 2: Automatic on first failure
- Tier 2 → Tier 1: Manual demotion if refinement stalls

**Note**: This is a maturity ladder, not a capability hierarchy. A "simple" search agent and a "complex" architecture agent both start at Tier 1 and climb the same ladder.

---

### Phase 4: Agent Definition (Kiro Format)
For each agent, create a `.kiro/agents/<name>.json` file:

```json
{
  "name": "agent-name",
  "description": "[One sentence: what this agent does and does not do]",
  "prompt": "[Core instruction: narrow role, explicit boundaries, output format]",
  "tools": ["tool1", "tool2"],
  "toolsSettings": {
    "tool1": {
      "constraint": "value"
    }
  },
  "resources": [
    "file://.kiro/steering/palette-core.md",
    "file://.kiro/steering/domain-specific-context.md"
  ]
}
```

**Rules**:
- Description must fit in one sentence
- Prompt must define what the agent **does not do** (boundaries matter more than capabilities)
- Tools must be minimal (add more only when agent explicitly requests them)
- Resources must include `palette-core.md` to inherit convergence protocol

---

### Phase 5: Orchestration Strategy
Decide how agents interact.

#### Pattern A: Serial Handoff
```
Human → Agent1 → decisions.md → Human → Agent2 → decisions.md
```
**When to use**: Each step depends on prior results; high-stakes decisions  
**Pros**: Maximum control, clear accountability  
**Cons**: Slower, requires human-in-loop

#### Pattern B: Parallel Fan-Out
```
Human → [Agent1, Agent2, Agent3] → Merge Results → decisions.md
```
**When to use**: Independent tasks, time-sensitive  
**Pros**: Fast, efficient  
**Cons**: Harder to debug, requires merge logic

#### Pattern C: Hierarchical Delegation
```
Human → Orchestrator-Agent → [Specialist1, Specialist2] → Orchestrator → Human
```
**When to use**: Complex workflows with many sub-tasks  
**Pros**: Scalable  
**Cons**: Orchestrator becomes single point of failure

**Default**: Start with Pattern A (Serial Handoff). Upgrade only when speed becomes a proven bottleneck.

---

### Phase 6: Execution & Observation
Run the agent configuration against the real problem.

**Required Artifacts**:
1. `decisions.md` – Updated after every agent interaction
2. `assumptions.md` – Updated when provisional choices are made
3. `lessons.md` – Updated when something breaks or succeeds unexpectedly

**Observation Protocol**:
- After each agent call, ask: "Did this agent do exactly what I expected?"
- If yes → confidence increases
- If no → capture the delta in `lessons.md`

**One-Way Door Rule**: If an agent proposes an irreversible action:
1. Agent MUST flag it with `⚠️ ONE-WAY DOOR`
2. Human MUST explicitly approve
3. Decision MUST be logged in `decisions.md`

---

### Phase 7: Retrospective & Refinement
After the problem is solved (or abandoned), conduct a retrospective.

**Questions**:
1. Which agents were **essential**?
2. Which agents were **redundant**?
3. Which agents were **missing**?
4. Did the taxonomy help or hinder?
5. What surprised you?

**Output**: Update `assumptions.md` with:
- Validated patterns (promote to `palette-core.md` if proven repeatedly)
- Discarded patterns (move to Graveyard)
- New hypotheses to test next time

---

## Current Agent Roster (Experimental)

### Tier 3: PRODUCTION (Fully Automated)
*None yet - all agents start at Tier 1*

### Tier 2: WORKING (Refinement Phase)
*None yet - agents must prove themselves at Tier 1 first*

### Tier 1: UNVALIDATED (Human Validation Required)
1. **`search-agent`**
   - Role: Fast information retrieval from APIs, docs, web
   - ARK Type: Resource Gatherer (Argentavis)
   - Status: Not yet built
   - Hypothesis: Will be used in 80%+ of workflows

2. **`code-writer`**
   - Role: Write/refactor code in bounded domains
   - ARK Type: Specialized Builder (Therizinosaurus)
   - Status: Not yet built
   - Hypothesis: Essential for FDE simulations

3. **`debugger-agent`**
   - Role: Diagnose and fix specific bugs
   - ARK Type: Specialized Builder (Raptor)
   - Status: Not yet built
   - Hypothesis: Critical for iteration speed

### Proposed Future Agents (Not Yet Prioritized)
- `architect-agent` (Strategic Orchestrator / Rex)
- `gtm-agent` (Strategic Orchestrator / Yutyrannus)
- `data-miner` (Resource Gatherer / Ankylosaurus)
- `doc-writer` (Specialized Builder / Mammoth)

**Note**: ARK types (Argentavis, Rex, etc.) are just cognitive labels. They don't determine tier placement. All agents start at Tier 1 regardless of complexity.

---

## Decision Rules (Inherited from Palette Core)

### When to Add a New Agent
**Only add when**:
1. An existing agent is consistently overloaded (handling 3+ distinct tasks)
2. A task type appears repeatedly and has unique tool requirements
3. Parallelization would provide 2x+ speed improvement

**Do NOT add when**:
- You're just bored with the current agent
- You think specialization sounds "cleaner"
- You haven't tried solving it with existing agents first

### When to Merge Agents
**Merge when**:
1. Two agents are always called sequentially (no branching)
2. The boundary between them is arbitrary or unclear
3. Managing them separately creates more overhead than value

### When to Delete an Agent
**Delete immediately when**:
1. Unused for 2+ problem-solving cycles
2. Consistently produces lower-quality results than general-purpose agents
3. Requires more oversight than doing the task yourself

---

## Anti-Patterns (Learned Through Failure)

### ❌ Agent Sprawl
**Symptom**: 10+ agents, each used once  
**Cause**: Premature specialization  
**Fix**: Consolidate to 3-5 generalists, specialize only under proven load

### ❌ The God Agent
**Symptom**: One agent with 15+ tools and vague responsibilities  
**Cause**: Fear of coordination overhead  
**Fix**: Split into focused agents with explicit handoff points

### ❌ Invisible State
**Symptom**: Agents "remember" things not in `decisions.md`  
**Cause**: Relying on conversational memory instead of explicit state  
**Fix**: Enforce stateless agents; all context in files

### ❌ Reasoning as Agent Role
**Symptom**: Trying to build a "reasoning agent" inside the system  
**Cause**: Confusing problem-solving with execution  
**Fix**: Reasoning happens OUTSIDE this system (via separate tools/sessions). This system executes validated solutions, it doesn't discover them.

**Important**: Deep reasoning, experimentation, and problem decomposition happen in external reasoning environments. This system is where you BUILD and VALIDATE individual agents one at a time. Once an agent works reliably, it gets promoted to production (Tier 3). This is an execution system, not a discovery system.

---

## Graveyard (Discarded Assumptions)

*As experiments fail, document them here to prevent rediscovery.*

### ❌ [Pattern Name] (Tried: [Date], Removed: [Date])
**What it was**: [Description]  
**Why removed**: [Failure mode]  
**Lesson**: [What we learned]

---

## Exit Criteria for IDP Itself

This framework should be replaced when:

1. **Convergence is Automatic**: You no longer need explicit decomposition; problem → agent mapping is intuitive
2. **Taxonomy is Stable**: Agent types haven't changed in 10+ problem-solving cycles
3. **Overhead > Value**: The process of documenting experiments takes longer than just solving problems
4. **Better Framework Emerges**: A simpler or more powerful organizing principle is discovered

**Current Status**: Active experimentation. Expect rapid iteration.

---

## Quick Reference: Problem → Agent Workflow

```
1. Receive problem
2. Decompose into work types (retrieval, build, validate, compute)
3. Hypothesize minimal agent set (start with 1-3)
4. Define agents in .kiro/agents/
5. Choose orchestration pattern (default: serial handoff)
6. Execute with continuous logging to decisions.md
7. Observe: did agents do what you expected?
8. Retrospective: what worked, what didn't?
9. Update assumptions.md and agent roster
10. Repeat
```

**Remember**: This is a testing ground. Nothing here is sacred. Optimize for learning velocity, not ideological purity.

---

**Last Updated**: [Timestamp]  
**Next Review**: After first 3 problem-solving cycles  
**Owner**: Human (Mical) + AI (Claude via Kiro)
