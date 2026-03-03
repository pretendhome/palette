# Getting Started with Palette

**Time to First Success**: 15 minutes  
**What You'll Learn**: How to use Palette's three-tier decision system to build with AI agents  
**What You'll Build**: Understanding through a real example (our UX improvement engagement)

---

## What is Palette?

Palette is a **three-tier decision system** that makes AI collaboration reliable, bounded, and restartable.

**Not autonomous AI hype.** A toolkit that requires human-AI alignment (convergence) to work.

**What it does**:
- Classifies problems (104 RIUs in the taxonomy)
- Routes to specialized agents (8 agent archetypes)
- Learns from success/failure (self-improving system)

---

## Installation & Setup

### Quick Start (5 Minutes)

**Step 1: Get Palette**
```bash
# Clone or download the repository
git clone [repository-url]
cd palette/
```

**Step 2: Choose Your AI Tool**

**Claude Desktop / Claude Code**
- Open the `palette/` folder in Claude
- Reference tier files: `.kiro/steering/palette-core.md`
- Load agent files: `agents/researcher/researcher.md`

**Cursor / VS Code + Copilot**
- Open `palette/` as workspace
- Add tier files to context
- Reference agents as needed

**GitHub Copilot / Any AI System**
- Point your AI to the `palette/` folder
- Load tier files manually
- Copy/paste agent definitions when needed

**Step 3: Name Your Team (2 minutes)**

Before you start, personalize the 8 agents. Copy-paste this to your AI:

```
I'm setting up Palette. Help me name my 8-agent team based on what they do:

1. Research agent (gathers evidence, read-only)
2. Architecture agent (system design, flags irreversible decisions)
3. Build agent (implements from spec)
4. Debug agent (root cause analysis)
5. Validate agent (quality checks, cross-domain patterns)
6. Narrative agent (communication, explanations, system coherence)
7. Monitor agent (anomaly detection)
8. Coordinate agent (multi-agent workflows)

Default names: Researcher, Architect, Builder, Debugger, 
Validator, Narrator, Monitor, Orchestrator

Suggest 3 alternative names for each role, then I'll choose.
```

**Why this matters**: Naming forces you to understand what each agent does. The system works the same regardless of names—you're just making it yours.

**Step 4: Verify It Works (30 seconds)**

Tell your AI:
```
Load the Research agent definition and become [your chosen name]
```

Then ask:
```
Which database should we use for our project?
```

**Expected Response**:
```
⚠️ CONSTRAINT VIOLATION
I'm a research agent with read-only access.
I can provide findings on database options, but I cannot 
make architecture decisions. Route to Architecture agent.
```

**If you see this, Palette is working!** ✅

---

## The 5-Minute Concept

### Three Tiers

**Tier 1** (`TIER1_palette_core.md`) - **The Physics**
- Immutable core principles
- Convergence requirement (human-AI alignment)
- ONE-WAY vs TWO-WAY DOOR decisions
- Glass-box architecture (traceable decisions)
- Cross-domain synthesis (system learns)

**Tier 2** (`TIER2_assumptions.md`) - **The Agents**
- 8 specialized agent archetypes
- Each has specific role + constraints
- Agents earn trust through maturity model
- UNVALIDATED → WORKING → PRODUCTION

**Tier 3** (`TIER3_decisions_prompt.md`) - **The Log**
- Append-only execution record
- Semantic Blueprint (convergence brief)
- RIU selection (which patterns applied)
- ONE-WAY DOOR decisions (approvals required)
- Agent impressions (success/fail tracking)
- Optional Step 6: Cross-domain synthesis

### Three Artifacts

**Taxonomy** (`palette_taxonomy_v1.2.yaml`) - **104 RIUs**
- Reusable Intervention Units (problem patterns)
- Trigger signals → Route to solution
- Relatively static (problems are stable)

**Library** (`palette_knowledge_library_v1.2.yaml`) - **88 Entries**
- Validated Q&A with sources
- Maps to RIUs for execution
- Highly dynamic (solutions evolve rapidly)

**Agent Manual** (`agent_implementation_manual.md`) - **8 Archetypes**
- Researcher (Research) 🔵
- Builder (Build) 🟠
- Debugger (Debug) 🔴
- Architect (Architecture) 🟣
- Narrator (Narrative + System Coherence) 🟢
- Validator (Validation + Cross-Domain Patterns) ⚪
- Monitor 🟡
- Orchestrator (Coordinate - design only) ⚫

---

## How It Works (Real Example)

Let's walk through the **UX improvement engagement** that happened on 2026-02-01. This is a real engagement that improved Palette itself.

You can follow along by reading the actual files in `examples/ux-engagement-2026-02-01/`

---

### Step 1: The Problem Arrives

**User said**: "Let's improve Palette's UX - make it easier to use out of the box."

**What Palette did**:
1. Detected trigger signals: "easier to use", "out of the box", "UX improvement"
2. Matched to **RIU-042** (Demo/Narrative Design)
3. Routed to **convergence first** (always converge before executing)

**File to read**: `examples/ux-engagement-2026-02-01/convergence_brief.md`

---

### Step 2: Convergence (Human-AI Alignment)

Before execution, Palette **forced convergence** using a Semantic Blueprint:

```markdown
## Goal
Create self-improving UX for Palette (GitHub repo, onboarding, visual identity)

## Roles
- Human: Approves ONE-WAY DOOR decisions
- Agents: 7 agents, one round each (Researcher → Architect → Builder → Narrator → Monitor → Debugger → Validator)

## Constraints
- One round only per agent (discipline test)
- Human-in-the-loop preserved (not autonomous)
- System-agnostic (works with Kiro, Copilot, Claude Code)

## Non-Goals
- NOT a standalone product (toolkit only)
- NOT fully autonomous operation
- NOT platform-specific

## Success Criteria
- <5 min onboarding works
- Visual identity professional
- Contribution workflow clear
- Cross-domain patterns identified (testing new Step 6)
```

**Why this matters**: Without convergence, agents would guess what "better UX" means. With it, everyone is aligned on goal, constraints, and success.

**File to read**: `examples/ux-engagement-2026-02-01/convergence_brief.md`

---

### Step 3: RIU Selection (Pattern Matching)

Palette matched trigger signals to RIUs:

**Primary RIU**: RIU-042 (Demo/Narrative Design)
- Narrator's specialty (narrative + visual identity)
- Routes to Library entries on UX patterns
- Success criteria: Can explain clearly in <5 min

**Supporting RIUs**:
- RIU-001 (Convergence Brief) - Force clarity first
- RIU-004 (Problem Decomposition) - Break into workstreams

**What happened**: Taxonomy (problem classification) routed to Library (validated solutions).

**File to read**: `examples/ux-engagement-2026-02-01/riu_selection.md`

---

### Step 4: Agent Execution (7 Rounds)

Each agent got **one round only** (discipline test):

#### Round 1: Researcher (Research) - 15 min 🔵
**Task**: Research UX patterns for developer toolkits
**Output**: 5 findings (repo structure, onboarding, visual identity, self-improvement, adoption)
**File**: `examples/ux-engagement-2026-02-01/researcher_research_report.md`

#### Round 2: Architect (Architecture) - 20 min 🟣
**Task**: Design repo structure and governance model
**Output**: Architecture proposal + **2 ONE-WAY DOOR decisions** flagged
**ONE-WAY DOORS**:
- 🚨 Repository structure (hard to change after users clone)
- 🚨 Visual glyph (brand consistency)
**File**: `examples/ux-engagement-2026-02-01/architect_architecture_proposal.md`

**What happened here**: Architect **paused** and flagged irreversible decisions. Human approved before Builder could build.

#### Round 3: Builder (Build) - 30 min 🟠
**Task**: Implement repo structure, templates, contribution guidelines
**Output**: 11/12 files created (92% complete, missed LICENSE)
**File**: `examples/ux-engagement-2026-02-01/builder_build_report.md`

#### Round 4: Narrator (Narrative + Visual) - 45 min 🟢
**PRIMARY OWNER** - Narrator's bread and butter

**Task**: Create onboarding narrative + visual identity
**Output**:
- 5-minute pitch (can explain Palette clearly)
- 8-color semantic palette (each agent has a color)
- Glyph concept (programmer with painter's palette)
- Communication strategy (errors, success, contributions)

**Narrator's Validation**: "Can I explain this clearly?" → **YES**

**File**: `examples/ux-engagement-2026-02-01/narrator_narrative_and_visual.md`

#### Round 5: Monitor (Integration) - 20 min 🟡
**Task**: Verify integration, signal anomalies
**Output**: 11/12 files verified, 1 anomaly detected (missing LICENSE)
**Routed to**: Debugger for fix

**File**: `examples/ux-engagement-2026-02-01/monitor_integration_report.md`

#### Round 6: Debugger (Debug) - 15 min 🔴
**Task**: Fix anomaly (missing LICENSE)
**Output**: LICENSE created (MIT), 100% structure complete
**File**: `examples/ux-engagement-2026-02-01/debugger_debug_report.md`

#### Round 7: Validator (Validation) - 30 min ⚪
**Task**: Validate quality + **run Step 6 (cross-domain synthesis)**
**Output**:
- Solution quality: ✅ EXCELLENT
- Best solution we know: ✅ YES
- **3 cross-domain patterns identified**
- **6 system improvements recommended**

**File**: `examples/ux-engagement-2026-02-01/validator_validation_report.md`

---

### Step 5: Cross-Domain Synthesis (NEW - Step 6)

This engagement **tested** a new validation protocol: Narrator + Validator pairing to identify patterns that transfer across domains.

**Patterns Found**:

**Pattern 1**: Semantic color coding (visual identity) → Agent workflow visualization
- **Insight**: Using 8 agent colors in execution logs improves readability
- **Result**: Added **LIB-087** to Library

**Pattern 2**: Structured onboarding (UX pattern) → Convergence briefs
- **Insight**: 5-section template accelerates alignment
- **Result**: Added **LIB-088** to Library, updated **RIU-001** routing

**Pattern 3**: Contribution quality gates (OSS workflow) → Agent validation
- **Insight**: Quality dimensions improve maturity tracking
- **Result**: Recommended Tier 2 update (not yet implemented)

**What this proved**: Cross-domain synthesis works. Found 3 patterns, generated 6 improvements, 30 min invested, high ROI.

**File to read**: `examples/ux-engagement-2026-02-01/validator_validation_report.md` (Part B + Part F)

---

### Step 6: System Improvements Applied

Based on patterns identified, Palette **improved itself**:

**Library Updates** (v1.0 → v1.2):
- Added LIB-087: Agent Workflow Visualization
- Added LIB-088: Convergence Brief Structure

**Taxonomy Updates** (v1.1 → v1.2):
- RIU-001 now routes to LIB-088 for convergence template

**Tier Updates**:
- Tier 2: Narrator = "System Coherence Guardian", Validator = "Cross-Domain Pattern Validator"
- Tier 3: Step 6 formalized as optional cross-domain synthesis

**The Meta-Achievement**: Palette used itself to improve itself. The system is self-improving.

**File to read**: `FORMALIZATION_COMPLETE.md`

---

## Key Concepts Demonstrated

### 1. Convergence (Not Autonomous)

**What happened**: Before any agent executed, human and Palette aligned on goal, constraints, success criteria.

**Why it matters**: Without convergence, agents guess. With it, everyone knows what "success" means.

**File example**: `examples/ux-engagement-2026-02-01/convergence_brief.md`

---

### 2. ONE-WAY DOOR Decisions

**What happened**: Architect flagged 2 irreversible decisions (repo structure, visual glyph) and **paused** for approval.

**Why it matters**: Prevents "we deployed" or "we committed architecture" without human sign-off.

**File example**: `examples/ux-engagement-2026-02-01/architect_architecture_proposal.md` (lines 89-105)

---

### 3. Agent Boundaries

**What happened**: 
- Researcher researched but didn't recommend (read-only)
- Architect designed but didn't build (architecture only)
- Builder built but didn't design (implementation only)
- Validator validated but didn't fix (assessment only)

**Why it matters**: Separation of concerns prevents "agent creep" where everyone tries to do everything.

**File example**: See any agent report - each stayed in scope

---

### 4. Restartability

**What happened**: Everything logged in `decisions.md` - Semantic Blueprint, RIU selection, ONE-WAY DOORS, artifacts, impressions.

**Why it matters**: If someone leaves, project doesn't lose reasoning. Anyone can read the log and continue.

**File example**: `examples/ux-engagement-2026-02-01/decisions.md`

---

### 5. Self-Improvement (Cross-Domain Synthesis)

**What happened**: After solving "UX improvement", Palette asked "Does this reveal patterns applicable elsewhere?" Found 3, applied 2.

**Why it matters**: System gets smarter with every engagement. Library grows, Taxonomy routes better, agents coordinate better.

**File example**: `examples/ux-engagement-2026-02-01/validator_validation_report.md` (Part B)

---

## The Two-Artifact Philosophy

This engagement proved a core principle:

### Problems are Static, Solutions Evolve

**RIUs (Taxonomy)**: RELATIVELY STATIC
- Core problems companies face haven't changed (humans are humans)
- RIUs classify and route, they don't solve
- Updates: Primarily which Library entries to route to

**Library**: HIGHLY DYNAMIC
- Solutions evolve at "agentic light speed"
- Must keep pace with rapid change
- This engagement added 2 entries in one day

**Evidence**: 
- Taxonomy v1.1 → v1.2 (routing update only)
- Library v1.0 → v1.2 (2 new entries added)

---

## How to Use Palette (Your First Engagement)

### Option 1: Follow This Exact Pattern

Use the UX engagement as a template:

1. **Start with convergence** (copy `convergence_brief.md` template)
2. **Match to RIUs** (look at trigger signals in taxonomy)
3. **Route to Library** (find validated solutions)
4. **Execute with agents** (use agent manual for constraints)
5. **Log everything** (use `decisions.md` template)
6. **Optional**: Run Step 6 (extract cross-domain patterns)

---

### Option 2: Start Simple (Recommended)

**Minimal viable engagement**:

1. Read **Tier 1** (`TIER1_palette_core.md`) - 10 min
   - Understand: Convergence, ONE-WAY DOOR, Glass-box

2. Pick **1 agent** from manual - 5 min
   - Start with Researcher (research) or Narrator (narrative)

3. Run **1 RIU** - 15 min
   - Try RIU-001 (Convergence Brief)
   - Use LIB-088 template (5-section structure)

4. Log in **decisions.md** - 5 min
   - What you tried, what worked, what's next

**Total**: 35 minutes to first success

**Then**: Gradually add more agents, more RIUs, run Step 6 when appropriate.

---

## File Structure Guide

```
palette-framework/
├── GETTING_STARTED.md ← You are here
├── README.md ← Overview + installation
├── CONTRIBUTING.md ← How to improve the system
├── CHANGELOG.md ← Version history
│
├── tier1/
│   └── TIER1_palette_core.md ← Core principles (read first)
│
├── tier2/
│   └── TIER2_assumptions.md ← Agent definitions (read second)
│
├── tier3/
│   └── TIER3_decisions_prompt.md ← Execution template (read third)
│
├── taxonomy/
│   └── palette_taxonomy_v1.2.yaml ← 104 RIUs (problem patterns)
│
├── library/
│   └── palette_knowledge_library_v1.2.yaml ← 88 validated Q&As
│
├── agents/
│   └── agent_implementation_manual.md ← 8 agent archetypes
│
├── examples/
│   └── ux-engagement-2026-02-01/ ← COMPLETE WALKTHROUGH
│       ├── convergence_brief.md
│       ├── riu_selection.md
│       ├── researcher_research_report.md
│       ├── architect_architecture_proposal.md
│       ├── builder_build_report.md
│       ├── narrator_narrative_and_visual.md
│       ├── monitor_integration_report.md
│       ├── debugger_debug_report.md
│       ├── validator_validation_report.md
│       └── decisions.md
│
└── assets/
    ├── palette-colors.md ← 8-agent color palette
    └── brand-guidelines.md ← Visual identity specs
```

---

## Reading Path (35 minutes)

**If you have 35 minutes, read in this order**:

1. **This file** (GETTING_STARTED.md) - 10 min
   - Understand the concept

2. **UX engagement convergence brief** - 5 min
   - `examples/ux-engagement-2026-02-01/convergence_brief.md`
   - See how convergence works

3. **UX engagement final summary** - 5 min
   - `examples/ux-engagement-2026-02-01/FINAL_SUMMARY.md`
   - See the complete outcome

4. **Validator's validation report (Part B + Part F)** - 10 min
   - `examples/ux-engagement-2026-02-01/validator_validation_report.md`
   - See cross-domain synthesis in action

5. **Tier 1 core principles** - 5 min
   - `tier1/TIER1_palette_core.md` (skim for key sections)
   - Understand the physics

**After 35 minutes**: You understand Palette well enough to start using it.

---

## Common Questions

### "Is this for me?"

**Yes if**:
- You build with AI (any system: Kiro, Copilot, Claude, Cursor)
- You want reliable, bounded, restartable AI collaboration
- You're tired of agents doing the wrong thing or losing context

**No if**:
- You want fully autonomous AI (this requires convergence)
- You want a product (this is a toolkit)
- You want instant magic (this requires learning the system)

---

### "How long to learn?"

- **35 minutes**: Understand the concept (read this + UX example)
- **2 hours**: First guided engagement (with help)
- **1 day**: Productive use (running engagements yourself)
- **1 week**: Fluent (customizing agents, adding RIUs, running Step 6)

---

### "What makes this different?"

**vs ChatGPT/Claude**:
- Palette has memory (decisions.md), classification (RIUs), and boundaries (agent constraints)
- ChatGPT/Claude are conversational; Palette is structural

**vs LangChain/AutoGPT**:
- LangChain is execution plumbing (tool calling, chain composition)
- Palette is decision governance (convergence, ONE-WAY DOOR, cross-domain synthesis)
- You can use LangChain under Palette

**vs Prompt libraries**:
- Prompt libraries give you templates
- Palette gives you a system (taxonomy, library, maturity model, self-improvement)

---

### "Can I customize it?"

**Absolutely**. That's the point.

**Easy customizations**:
- Add Library entries (your validated solutions)
- Add RIUs (your problem patterns)
- Adjust agent constraints (your needs)

**Hard customizations**:
- Change Tier 1 principles (requires evidence + approval)
- Add new agent archetypes (requires validation)
- Modify maturity model (requires testing)

**The system is designed for customization** - just follow the governance model (TWO-WAY DOOR = experiment freely, ONE-WAY DOOR = get approval first).

---

### "What if I get stuck?"

**Resources**:
1. Read `examples/ux-engagement-2026-02-01/` - Complete walkthrough
2. Check `CONTRIBUTING.md` - How to ask for help
3. Review `TIER1_palette_core.md` - Core principles
4. Look at `palette_knowledge_library_v1.2.yaml` - Validated solutions

**Contribution workflow**:
- Found a bug? → Use `.github/ISSUE_TEMPLATE/agent-failure.md`
- Have a use case? → Use `.github/ISSUE_TEMPLATE/use-case-submission.md`
- Want to add knowledge? → Use `.github/ISSUE_TEMPLATE/library-entry.md`

---

## Success Criteria (Did You Get It?)

After reading this guide + UX example, you should be able to:

✅ **Explain Palette** in <5 minutes (three tiers, three artifacts, self-improving)  
✅ **Understand convergence** (human-AI alignment before execution)  
✅ **Recognize ONE-WAY DOOR** (irreversible decisions require approval)  
✅ **Know agent boundaries** (Researcher researches, Architect designs, Builder builds, etc.)  
✅ **See the flywheel** (engagement → patterns → improvements → better system)

**If yes**: You're ready to use Palette.  
**If no**: Re-read the UX engagement example - it shows everything in practice.

---

## Next Steps

### 1. Run Your First Engagement

**Suggested first problem**: "Create a README for [your project]"

**Why this works**:
- Single agent (Narrator - narrative)
- Clear success criteria (README exists and is clear)
- Fast feedback (can you explain your project clearly?)
- Low stakes (can redo easily)

**Process**:
1. Create convergence brief (what makes a good README?)
2. Match to RIU-042 (narrative design)
3. Route Narrator with LIB-088 structure
4. Validate with 5-minute pitch test
5. Log in decisions.md

**Time**: ~1 hour  
**Outcome**: README + understanding of how Palette works

---

### 2. Try Cross-Domain Synthesis (Step 6)

After 3-4 engagements, try running Step 6:

**When**: Multi-agent engagement, novel problem, potential learnings  
**Process**: Narrator + Validator pairing (30 min)  
**Output**: 1-3 patterns + system improvements  
**Value**: System gets smarter

**Example**: If you built a dashboard (Researcher → Architect → Builder → Validator), ask: "Does this dashboard pattern apply to other visualization needs?" If yes, add to Library.

---

### 3. Contribute Back

**When you find**:
- A new validated solution → Add Library entry
- A recurring problem pattern → Propose new RIU
- An agent failure → Submit post-mortem
- A better approach → Open PR with evidence

**How**: Use templates in `.github/ISSUE_TEMPLATE/`

**Why**: The system improves for everyone. Your local learning becomes global knowledge (cross-domain synthesis in action).

---

## The Meta-Lesson

This guide was created **using Palette** (UX engagement).

**What happened**:
1. Problem: "Make Palette easier to understand"
2. Convergence: "5-minute onboarding, clear walkthrough, real example"
3. Execution: 7 agents, one round each
4. Validation: Narrator validated "Can I explain this clearly?" → YES
5. Cross-domain synthesis: Found patterns, improved system
6. Result: You're reading the output

**The system that created this guide is the system you're learning.**

If this guide makes sense, Palette works.  
If you can follow the UX example, you can use Palette.  
If you see the patterns, you're ready to extract your own.

---

## One Last Thing

**Palette is not magic.**

It's a structured way to:
- Align with AI before executing (convergence)
- Classify problems and route to solutions (taxonomy + library)
- Execute with bounded agents (constraints prevent creep)
- Learn from every engagement (cross-domain synthesis)
- Get better over time (self-improving system)

**The magic is in the discipline.**

Converge before you execute.  
Log what you learn.  
Extract the patterns.  
Improve the system.  
Repeat.

**That's Palette.**

---

**Ready to start?**

Open `examples/ux-engagement-2026-02-01/convergence_brief.md` and see how we began.

Then open `examples/ux-engagement-2026-02-01/FINAL_SUMMARY.md` and see where we ended.

Everything in between is the system working.

**Welcome to Palette.** 🎨
