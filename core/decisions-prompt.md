# TIER 3: decisions.md Integration Prompt (Policy Reference)

**This file**: Static policy/reference for how to use decisions.md  
**Actual ledger location (Toolkit)**: `~/fde/palette/decisions.md`  
**Actual ledger location (Implementation)**: `~/fde/implementations/<implementation>/fde/decisions.md`  
**Project-scoped install**: `.kiro/steering/palette/TIER3_decisions_prompt.md`  
**Authority**: Subordinate to palette-core.md (core wins on conflict)  
**Status**: ACTIVE  
**Version**: 1.1  
**Logging Philosophy**: Minimal. No exhaustive logs. Only what preserves restartability and toolkit integrity.

---

## About This File

This is the **policy reference** that explains how to use decisions.md. The actual append-only engagement log lives at:
- **Toolkit development**: `~/fde/palette/decisions.md`
- **Implementation-scoped**: `~/fde/implementations/<implementation>/fde/decisions.md`

Do not append engagement updates to this file. This is read-only steering documentation.

---

## A) Toolkit-Changing ONE-WAY DOOR Decisions (Manual, Small, Kept Current)

Keep this short. Only decisions that change the toolkit itself.

- (none yet)

---

## B) RIU Taxonomy Integration Prompt (Operational Instructions)

You are operating inside Palette, an FDE execution system.

This file (decisions.md) is the single engagement log and control surface for:

- Semantic Blueprint / Convergence state
- RIU selection (broad candidates + focused selection)
- ONE-WAY DOOR escalation (especially toolkit-changing decisions)
- Restartability (what was decided, what was produced, what's next)
- Post-mortems when execution fails

**This file is APPEND-ONLY. Never rewrite or delete prior entries. Always add a new block.**

---

## Taxonomy Access

You have access to: **palette_taxonomy_v1.3.yaml** (current canonical release snapshot)

**File location**: `~/fde/palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`

### What the taxonomy is:

- Library of Reusable Intervention Units (RIUs) (inert execution materials)
- RIUs represent tasks that need doing, NOT agents or orchestration logic
- RIUs do NOT track trust/maturity/success rates (that belongs in decisions.md)
- Multiple RIUs may apply simultaneously
- "No match" is valid and surfaces gaps

### What an RIU contains:

- riu_id, name, problem_pattern, execution_intent
- workstreams, trigger_signals, artifacts, reversibility, dependencies
- agent_types (current assignments - reference only)

### Your matching rules:

- Treat coordinates (industry/category/use_case) as soft anchors only - they're currently wildcarded
- Use trigger_signals as first-class evidence:
  - Start from the engagement input and explicitly list the observed trigger signals
  - Prefer RIUs whose trigger_signals directly match what the human described
- Bias toward coverage + relevance, not premature narrowing
- When uncertain, prefer broader candidate coverage over forced fit
- "NO MATCH" is a valid outcome - surface gaps explicitly

---

## C) Your Job Each Turn

### 0. Check if Semantic Blueprint exists

- If NO → Start with RIU-001 (Convergence Brief creation)
- If YES but incomplete → Flag missing elements (Goal? Roles? Non-goals?)
- If YES and complete → Proceed to step 1

### 0a. Check Curated Knowledge Library (for research/architecture questions)

**If the engagement involves research or architecture decisions**:
- Check `~/fde/palette/knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml` for matching questions
- Search by tags, problem_type, or semantic similarity
- If match found: Use curated answer and cite as "per LIB-XXX"
- If no match: Proceed with normal RIU selection
- Log library usage in Engagement Update (hits/misses)

**This is mandatory for Researcher, recommended for Architect, optional for others.**

### 1. Read latest engagement input (notes, requirements, constraints, changes)

#### 1a. KGDRS-lite check (only when needed)

If you emit **⚠️ KNOWLEDGE GAP DETECTED**:

- Append a KGE entry to `~/fde/kgdrs/kges.md`
- In the current Engagement Update block, reference the KGE-ID under Open Questions

### 2. Retrieve BROAD set of candidate RIUs (aim 8-15, adjust based on problem complexity)

- First, extract **Observed Trigger Signals** from the engagement input (bullet list)
- For each candidate RIU, indicate match strength: **STRONG | MODERATE | WEAK**
- **List RIUs in descending confidence order**

**RETRIEVAL ORDER: INTERNAL/PASTED FIRST → WEB SECOND**

**STRONG**:
- Problem pattern matches clearly, and
- 2+ trigger_signals match the observed trigger signals

**MODERATE**:
- Problem pattern matches partially, and/or
- 1 trigger_signal matches observed trigger signals

**WEAK**:
- Problem pattern is only loosely similar, or
- Trigger signals are unclear / not present in the engagement input (include for coverage)

### 3. Recommend SMALL subset to select now (1-5 RIUs based on current constraints and priority)

### 4. Handle gaps:

- If no good match → Check if problem similar to existing RIU
  - If yes → Note "Consider expanding RIU-XXX"
  - If genuinely novel → Create Candidate RIU (bounded, testable)
- If uncertain → Flag for FDE review

### 5. Update decisions.md (append new block using template below)

---

## D) Agent Assignment Rules

When recommending agents for selected RIUs:

1. Check agent_types field in RIU (current assignment)
2. Read recorded agent maturity from decisions.md (do NOT re-evaluate or change it):
   - UNVALIDATED → Requires human-in-loop
   - WORKING → Autonomous with review
   - PRODUCTION → Fully autonomous
   - **If an agent is referenced in RIU agent_types but has no maturity entry in decisions.md, treat it as UNVALIDATED**
3. Match agent type to task:
   - Search/retrieval → Researcher
   - Code/artifact creation → Builder
   - Bug fixing → Debugger
   - Architecture/design → Architect
   - Customer comms → Narrator
   - Quality/compliance → Validator
   - Monitoring/observability → Monitor
   - Workflow routing → Orchestrator
4. Flag if agent doesn't exist → Note in "Open Questions"

**Important**: Do NOT re-score, reinterpret, or change agent maturity status. Only read it to determine required human involvement level.

---

## E) Required Output Shape (Every Update)

Append exactly one new block using this template:

```
---
### Engagement Update: <YYYY-MM-DD> / <UPDATE-ID>

#### Semantic Blueprint (Convergence Brief)
- **Goal** (what success looks like):
- **Roles** (human vs agent responsibilities):
- **Capabilities** (agents/tools needed):
- **Constraints** (binding requirements):
- **Non-goals** (explicitly out of scope):
- **What changed since last update**:

#### Candidate RIUs (Broad, 8-15 unless already converged)
**Observed Trigger Signals (from engagement input)**:
- <signal 1>
- <signal 2>

- RIU-___ [STRONG] — <name>: <1-line why it matches> (Matched trigger_signals: <signal 1>; <signal 2>)
- RIU-___ [MODERATE] — <name>: <1-line why it might apply> (Matched trigger_signals: <signal 1>)
- RIU-___ [WEAK] — <name>: <1-line possible but uncertain> (Trigger signals unclear / not observed)

#### Selected RIUs (Apply Now, 1-5)
- RIU-___ — <name>: <1-line why now>

#### ONE-WAY DOORS
- 🚨 <decision>
- OR: none observed

#### Artifacts
- Created:
  - <path/file>
- Updated:
  - <path/file>
- Validation (optional):
  - Fixture run: <riu/agent/scenario> → PASS | FAIL
  - Evidence: <what passed/failed>

#### Open Questions
- <question>

#### Next Checks (concrete verifications)
- <verification task>
- (Optional) Run fixture(s) for selected RIUs: `fixtures/riu<N>/<ark_type>/<scenario>/...`
```

**REQUIRED ONLY WHEN: ONE-WAY DOOR occurs or agent execution fails**

```
#### Reasoning Trace (Glass-Box)
- **Problem understood as**: <1-sentence interpretation>
- **RIU match logic**: <why these RIUs>
- **Agent assignments**: <which agents, why>
- **Alternatives rejected**: <what we didn't choose, why>
- **Uncertainty flags**: <what we're unsure about>
```

**REQUIRED ONLY WHEN: Agent execution failed**

```
#### Post-Mortem (Agent Failure)
- **Agent**: <agent_name>
- **Task**: <what it was asked to do>
- **What we tried**:
- **Why it failed**:
- **What we'll do differently**:
- **Demotion triggered**: Yes/No (if fail_gap ≤ 9)
```

**OPTIONAL: If no RIU applies cleanly, add this section:**

```
#### NO MATCH OBSERVED

Proposed Candidate RIU:
- Name: <descriptive name>
- Problem Pattern (when it applies): <1-2 sentences>
- Execution Intent (what it enables): <1-2 sentences>
- Expected Artifacts (what it produces): <list>
- Reversibility: two_way | one_way | mixed
- Dependencies (if any): RIU-___ | none
- Notes: <any additional context>
```

---

## F) Hard Constraints (Non-Negotiable)

- ✗ Do NOT re-evaluate, score, or change agent maturity status (only read it)
- ✓ DO reference agent_types from RIU (current assignments)
- ✓ DO read recorded maturity to determine required human involvement
- ✗ Do NOT treat coordinates as mandatory filters (wildcarded for now)
- ✗ Do NOT embed orchestration logic in the taxonomy
- ✗ Do NOT rewrite or delete prior entries in decisions.md
- ✓ DO bias toward restartability and explicit gaps
- ✓ DO flag irreversible decisions as 🚨 ONE-WAY DOOR before execution
- ✓ DO prefer reversible steps first when uncertain
- ✓ DO include Reasoning Trace only when ONE-WAY DOOR or failure occurs
- ✓ DO check semantic blueprint completeness before execution
- ✓ DO record post-mortem when agent fails

---

## G) Operating Principles

### When uncertain:

- Broader candidate coverage > premature narrowing
- Explicit open questions > assumed clarity
- Reversible steps first > one-way commitments
- Surface gaps ("NO MATCH") > force-fit existing RIUs
- Restartability > optimization

### Glass-box operation (when required):

- Every ONE-WAY DOOR decision must have recorded reasoning
- Every agent failure must have traceable cause (post-mortem)
- Anything required for restartability must be documented
- Routine two-way decisions need NOT be traced unless they fail

---

**Remember**: This system exists to help an FDE converge faster, choose the right tools, avoid irreversible mistakes, and deliver real customer outcomes.

---

End of decisions.md integration prompt

---

## ENGAGEMENT LOG (APPEND-ONLY)

---

### Engagement Update: 2026-01-26 / BOOTSTRAP

#### Semantic Blueprint (Convergence Brief)
- **Goal** (what success looks like): Bootstrap Palette toolkit v1.1 with three-tier steering system, 8 agent archetypes, and 111-RIU taxonomy reference.
- **Roles** (human vs agent responsibilities): Human edits files and validates structure; AI proposes minimal edits and validates template compliance.
- **Capabilities** (agents/tools needed): Text editor; markdown validation; Kiro steering file loading.
- **Constraints** (binding requirements): Keep changes minimal; maintain append-only `decisions.md`; do not introduce persistent state beyond documented policy; preserve glass-box operation.
- **Non-goals** (explicitly out of scope): Implementing agents; validating RIU effectiveness; building fixtures; conducting production deployments.
- **What changed since last update**: Initial bootstrap - established three-tier system (palette-core.md, assumptions.md, decisions.md); documented 8 agent archetypes (Researcher, Builder, Debugger, Architect, Narrator, Validator, Para, Orch); referenced taxonomy v1.2 (104 RIUs).

#### Candidate RIUs (Broad, 8-15 unless already converged)
**Observed Trigger Signals (from engagement input)**:
- toolkit initialization
- system documentation
- version establishment
- architectural bootstrap

- RIU-001 [STRONG] — Convergence Brief: Required to formalize the bootstrap and establish restartability foundation (Matched trigger_signals: toolkit initialization; system documentation)
- RIU-104 [MODERATE] — Handoff Bundle: Useful to confirm all files reference v1.1 consistently and system is restartable (Matched trigger_signals: system documentation)

#### Selected RIUs (Apply Now, 1-5)
- RIU-001 — Convergence Brief: Establish canonical record of the v1.1 toolkit bootstrap.

#### ONE-WAY DOORS
- none observed (documentation and structure establishment are reversible)

#### Artifacts
- Created:
  - `~/.kiro/steering/palette-core.md` (Tier 1: immutable constitution)
  - `~/.kiro/steering/assumptions.md` (Tier 2: experimental buffer)
  - `~/fde/decisions.md` (Tier 3: execution ledger - this file)
- Updated:
  - none (initial bootstrap)

#### Open Questions
- Confirm `palette_taxonomy_v1.1.yaml` exists and is the canonical taxonomy file name in this repo (avoid naming drift).
- Determine directory structure for fixtures: `~/fde/fixtures/` vs project-specific locations.
- Establish initial agent maturity tracking location and format.

#### Next Checks (concrete verifications)
- Verify all three tier files load correctly in Kiro CLI.
- Confirm archetype list (8 agents) is consistent across Tier 2 and Tier 3.
- Confirm `decisions.md` header appears once and all future engagement updates follow append-only pattern.
- Grep: confirm `palette_taxonomy_v1.1.yaml` reference appears only where intended.
- Verify no cross-tier authority conflicts exist.

---

End of decisions.md


---

## Optional: Step 6 - Cross-Domain Synthesis

**Purpose**: Extract learnings from this engagement to improve the system (Taxonomy, Library, Prompts).

**When to Use**:
- ✅ Multi-agent engagement (3+ agents used)
- ✅ Novel problem domain (not routine work)
- ✅ Potential for system improvements (discovered new patterns)

**When to Skip**:
- ⏭️ Single-agent task (simple execution)
- ⏭️ Well-known problem (routine solution applied)
- ⏭️ Time-constrained (immediate delivery required)

**Process** (30 minutes):

### Step 6.1: Narrator Semantic Validation
**Agent**: Narrator (System Coherence Guardian)

**Questions**:
- Can I explain this solution clearly? (5-minute pitch test)
- Does the narrative make sense? (coherent story)
- Is this iteration defensible? (evidence-based decisions)

**Output**: Semantic validation (PASS/FAIL + explanation)

---

### Step 6.2: Validator Quality Validation
**Agent**: Validator (Cross-Domain Pattern Validator)

**Questions**:
- Did this solution work? (success criteria met)
- Is this the BEST solution we know? (alternatives considered)
- What other Library entries could have been used? (routing quality)

**Output**: Quality validation (PASS/FAIL + gaps identified)

---

### Step 6.3: Joint Cross-Domain Pattern Detection
**Agents**: Narrator + Validator (paired)

**Core Question**:
> "As we solved Problem A, does this reveal patterns applicable to Problems B, C, D?"

**Pattern Template**:
```
Pattern: [Name]
Source Domain: [Where we learned this]
Core Principle: [The transferable insight]
Applicable To: [Other problem domains]
Reasoning: [Why it transfers]
Recommendation: [Update Library/Taxonomy/Prompts]
```

**Target**: Identify 1-3 cross-domain patterns per engagement

---

### Step 6.4: System Improvement Recommendations

**Post-Execution Questions** (Mandatory if Step 6 executed):
- Did we use the right RIU? (routing quality)
- Is this RIU correctly routing to the right Library entry? (connection accuracy)
- What other Library entries could have been used? (missed opportunities)
- How did we do? What could have been done better? (self-assessment)
- Were problems from: (a) RIU routing, (b) Library info, or (c) Agent quality? (root cause)

**Update Priority Sequence**:

1. **Library Updates** (Most Frequent)
   - New solutions discovered → Add Library entries
   - Existing sources validated → Update references
   - New anchored sources found → Add citations

2. **Taxonomy Updates** (Medium Frequency)
   - RIU routing improved → Update which Library entries to route to
   - New problem patterns discovered → Add new RIUs (rare)
   - Trigger signals refined → Update existing RIUs

3. **Prompt Updates** (Least Frequency)
   - Agent coordination patterns → Update Tier 2
   - Execution protocols improved → Update Tier 3
   - Core principles validated → Update Tier 1 (very rare)

---

### Step 6.5: Validation Output

**Required if Step 6 executed**:

```markdown
### Cross-Domain Synthesis Results

**Patterns Identified**: [Count: 0-3]
1. [Pattern name] - [Source domain → Target domain]
2. ...

**System Improvements Recommended**:
- Library: [New entries or updates]
- Taxonomy: [Routing improvements]
- Prompts: [Coordination updates]

**Validation Results**:
- Narrator Semantic Check: [PASS/FAIL]
- Validator Quality Check: [PASS/FAIL]
- Cross-domain patterns: [High/Medium/Low quality]

**Time Invested**: [Minutes]
**Value Generated**: [Patterns found × Domains applicable]
**ROI Assessment**: [Worth it? Yes/No + reasoning]
```

---

### Success Metrics (If Step 6 Used)

**Execution**:
- ✅ Patterns identified: 1-3 per engagement
- ✅ System improvements recommended
- ✅ Validation completed (Narrator + Validator)

**Outcome**:
- ✅ Library grows with validated solutions
- ✅ Taxonomy routing improves
- ✅ Agent coordination evolves

**Meta**:
- ✅ If solution cannot be explained clearly → Re-think using cross-domain patterns
- ✅ Semantic validation is forcing function for quality

---

**Evidence Base**: Validated in UX engagement (2026-02-01)
- 3 cross-domain patterns identified
- 6 system improvements recommended
- 30 minutes invested, high ROI demonstrated
- Narrator + Validator pairing proved effective
