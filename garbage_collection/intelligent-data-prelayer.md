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

### Phase 3: Agent Taxonomy (Current: ARK)
Classify each hypothesized agent by operational type.

#### Tier 1: Resource Gatherers (High-Volume, Low-Decision)
**Characteristics**: Stateless, parallel-friendly, narrow output format  
**Examples**: `search-agent`, `data-miner`, `context-builder`  
**When to use**: Need to extract/retrieve large amounts of information quickly  
**Cost profile**: Low per-call, high volume

#### Tier 2: Specialized Builders (Medium Complexity)
**Characteristics**: Bounded scope, testable outputs, iterative  
**Examples**: `code-writer`, `debugger-agent`, `doc-writer`  
**When to use**: Need to create artifacts (code, docs, diagrams)  
**Cost profile**: Medium per-call, medium volume

#### Tier 3: Strategic Orchestrators (High Complexity)
**Characteristics**: High reasoning, low execution, requires approval  
**Examples**: `architect-agent`, `gtm-agent`, `validator-agent`  
**When to use**: Need system-level design or stakeholder translation  
**Cost profile**: High per-call, low volume

#### Tier 4: Compute-Heavy Specialists (Boss Fighters)
**Characteristics**: Expensive, asynchronous, results-oriented  
**Examples**: `compute-agent`, `reasoning-agent`  
**When to use**: Need massive parallelization or deep multi-step reasoning  
**Cost profile**: Very high per-call, occasional use

**Exit Criteria for ARK Taxonomy**:
- If you consistently pick the wrong tier, the taxonomy is broken
- If all agents end up in one tier, the taxonomy adds no value
- If a simpler organizing principle emerges, migrate immediately

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

### Validated Agents (None Yet)
*Agents that have solved real problems reliably*

### Testing Agents
1. **`search-agent`** (Tier 1: Resource Gatherer)
   - Role: Fast information retrieval from APIs, docs, web
   - Status: Untested
   - Hypothesis: Will be used in 80%+ of workflows

2. **`code-writer`** (Tier 2: Specialized Builder)
   - Role: Write/refactor code in bounded domains
   - Status: Untested
   - Hypothesis: Essential for FDE simulations

3. **`debugger-agent`** (Tier 2: Specialized Builder)
   - Role: Diagnose and fix specific bugs
   - Status: Untested
   - Hypothesis: Critical for iteration speed

### Proposed Agents (Not Yet Built)
- `architect-agent` (Tier 3)
- `gtm-agent` (Tier 3)
- `compute-agent` (Tier 4)
- `reasoning-agent` (Tier 4)

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

### ❌ Taxonomy Paralysis
**Symptom**: Spending hours debating which tier an agent belongs in  
**Cause**: Treating taxonomy as truth instead of tool  
**Fix**: Pick a tier, test it, move on. Taxonomy is disposable.

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
