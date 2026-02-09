# Palette Demo Guide
**Date**: 2026-01-28  
**Audience**: AI-native startup (4 people, pre-Series A, building data infrastructure)  
**Duration**: 40 minutes

---

## Part 1: What Is Palette? (5-Minute Elevator Pitch)

### The Origin Story

I spent 7 years building knowledge architecture at AWS. Started on a science team working on a POI knowledge graph—25 billion nodes. The whole team spent our time curating one main prompt, testing changes, iterating.

I kept thinking: **There has to be a better way than a team of language engineers babysitting a single prompt.**

So I built a two-tier system: one tier for testing changes at scale, one tier for the final prompt.

When I started building agents at AWS, I added a middle tier—agents that take decisions from testing and actually build what's needed before hitting the core prompt. I call that middle tier "assumptions."

**I've been building this for 2.5 years.** Optimized it. Validated it extensively. Ran it through AWS Solutions Engineering proof-of-concept validation tools. Made it as robust as I could.

### The Problem It Solves

You're building infrastructure that handles messy data as-is. You get it: real-world data doesn't fit clean schemas.

**Here's the parallel problem**: Real-world problems don't fit clean prompts.

Traditional AI collaboration fails because:
- Teams waste time curating prompts manually
- No distinction between reversible and irreversible decisions
- No way to measure if an agent is actually reliable
- No path from "works once" to "works consistently"

### The Solution

**Palette is a three-tier agent toolkit that does the work of a team of language engineers.**

#### Tier 1: Core Prompt (palette-core.md)
The final prompt. The physics of collaboration. Never changes.
- **Convergence before execution** — Force clarity, no guessing
- **Glass-box reasoning** — Every decision is traceable
- **ONE-WAY DOOR vs TWO-WAY DOOR** — Distinguish reversible from irreversible
- **Semantic blueprints** — Goal, Roles, Capabilities, Constraints, Non-goals

#### Tier 2: Agents (assumptions.md)
The middle tier. Agents that test problems against solutions and build what's needed.
- **Agent archetypes** — Argy searches, Theri builds, Rex architects, Raptor debugs
- **Maturity tracking** — UNVALIDATED → WORKING → PRODUCTION
- **Empirical trust** — Agents earn autonomy through measured performance
- **Automatic demotion** — Two failures within 10 runs = demote tier

#### Tier 3: Testing at Scale (decisions.md)
The testing tier. Logs what works, what doesn't, and why.
- Captures: what was decided, why, what was built, what's next
- Anyone can pick up where you left off
- Only logs what matters (no exhaustive logs)

### The Two Artifacts That Make It Work

**1. Optimized Taxonomy (104 RIUs in YAML)**

I designed what I would build for AWS if I could start from scratch.

Uses AWS "use cases"—problems connected to proven solutions. Hard-fought, battle-tested solutions that cover everything you can build on a cloud platform.

**Current version**: v1.2 with 104 RIUs (94 core + 10 essential FDE patterns)

**Why this doesn't get outdated**: While technology changes (LLMs can do X, agents can do Y), the core customer problems and desired solutions are relatively static.

**2. Knowledge Library (86 Questions + Answers + Sources)**

I helped build a chatbot at AWS that synthesized massive amounts of GTM knowledge—blog posts, POC documents, architectural frameworks, migration automation.

I'm not going to do better than that team on relevance. And I'm not going to take thousands of screenshots of internal code written by half-wit Solutions Architects just to get a sale across the line.

So I created a curated library:
- Came up with robust questions
- Asked that chatbot in three iterations
- Validated with internal tooling
- Got Question + Answer + Source + metadata connecting to taxonomy
- Many sources are public (GTM knowledge has to be shared with customers)
- Sources are verifiable, updated, cross-referenceable

**How it stays current**: GTM knowledge is plentiful. Manually add sources when we find them. Do deep dives when areas feel lacking.

### What Makes It Different

**Not agentic AI hype.** It's a **battle-tested agent toolkit** that:
- Does the work of a team of language engineers
- Routes problems through a taxonomy to agents with proven solutions
- Agents have access to massive amounts of GTM knowledge
- When agents do good work long enough, we promote them
- Optimizes for restartability, not autonomy

### The End Result

**Day one value**: You give me a few problems. I immediately become a manager of agents solving those issues.

The system:
1. Classifies your problem in the taxonomy
2. Routes to an agent that already has information on how to solve it
3. Agent has access to internal code patterns and GTM knowledge library
4. Agent builds what's needed
5. When it does good work consistently, it gets promoted

**Palette doesn't just solve problems — it learns which solutions work, then teaches itself to get better.**

- Knowledge library grows (86 questions → 300 → 800)
- Agents evolve (UNVALIDATED → PRODUCTION)
- Cross-domain patterns emerge
- Institutional knowledge that doesn't leave when people do

**You're not building a tool. You're building a flywheel that turns experience into capability.**

---

## Part 2: What This Demo Is (2-Minute Explanation)

### The Meta-Approach

**I used Palette last night to design this demo.**

This isn't a slide deck. This is a recording of Palette solving a real FDE problem:
- **Problem**: Design a compelling 40-minute demo for an AI-native startup under time pressure with uncertain requirements
- **Solution**: Use Palette's three-tier system to converge, coordinate agents, and produce artifacts

### What You'll See

1. **Convergence Brief** — Semantic blueprint created before any execution
2. **Four Agents Coordinating**:
   - **Argentavis (Argy)** — Researched demo strategies for technical audiences
   - **Tyrannosaurus (Rex)** — Evaluated 5 demo options, recommended meta-approach
   - **Yutyrannus (Yuty)** — Generated complete demo script with timing
   - **Ankylosaurus (Anky)** — Validated plan, identified 7 risks, all mitigated
3. **ONE-WAY DOOR Enforcement** — Rex flagged irreversible decision (demo scenario selection), required my approval
4. **decisions.md Logging** — Entire conversation logged for restartability
5. **Agent Maturity Tracking** — First impressions logged for all 4 agents (success=1, fail=0, fail_gap=1)

### Why This Proves Palette Works

- ✓ Real problem solved (not a toy example)
- ✓ All three tiers demonstrated (convergence, agents, logging)
- ✓ Constraints enforced (agents stayed in scope)
- ✓ Decisions traceable (anyone can read decisions.md and understand why)
- ✓ Restartable (if I got hit by a bus, someone else could continue)

**You're not watching slides. You're watching Palette think.**

---

## Part 3: Exact Prompts to Execute Demo

### Setup (Before Demo Starts)

**Open these files in separate tabs/windows**:
1. `/home/mical/palette/decisions.md` (scroll to bottom for recent engagements)
2. `/home/mical/palette/.kiro/steering/palette-core.md` (for Tier 1 reference)
3. `/home/mical/palette/.kiro/steering/assumptions.md` (for Tier 2 agent definitions)
4. `/home/mical/palette/knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml` (for knowledge library)
5. `/home/mical/palette/taxonomy/releases/v1.2/palette_taxonomy_v1.2.yaml` (for RIU taxonomy)
6. `/home/mical/palette/VISION.md` (for self-improving infrastructure vision)

---

### Prompt 1: Opening Hook (2 min)

**SAY THIS**:

"You're building infrastructure that handles messy data as-is. You understand the problem: real-world data doesn't fit clean schemas.

Here's the parallel problem in AI collaboration: **Real-world problems don't fit clean prompts.**

Traditional AI fails because no memory of decisions, no distinction between reversible and irreversible, no reliability measurement, no path from 'works once' to 'works consistently.'

**Palette is a three-tier decision system that turns AI from a chatbot into a reliable field partner.**

And I'm going to prove it works by showing you how I used it last night to design this demo."

---

### Prompt 2: Architecture Overview (3 min)

**SHOW**: `palette-core.md`, `assumptions.md`, `decisions.md` files

**SAY THIS**:

"Three tiers:

**Tier 1: Immutable Rules** (palette-core.md)
- Convergence before execution — no guessing
- Glass-box reasoning — every decision traceable
- ONE-WAY DOOR vs TWO-WAY DOOR — reversible vs irreversible
- Semantic blueprints — Goal, Roles, Capabilities, Constraints, Non-goals

**Tier 2: Agent Maturity** (assumptions.md)
- Agent archetypes with constraints (Argy searches, Rex architects, etc.)
- Maturity tracking: UNVALIDATED → WORKING → PRODUCTION
- Empirical trust: 10 successes → WORKING, 50 runs <5% failure → PRODUCTION
- Automatic demotion: 2 failures within 10 runs = demote

**Tier 3: Execution Log** (decisions.md)
- Append-only decision ledger
- Captures: what, why, what's next
- Enables restartability — anyone can continue your work

These three files are the entire system. Everything else is execution."

---

### Prompt 3: Show Convergence Brief (3 min)

**SHOW**: `decisions.md` — scroll to "Semantic Blueprint (Convergence Brief)" section

**SAY THIS**:

"Last night I gave Palette this problem: Design a 40-minute demo for an AI-native startup.

Before any agent executed, Palette forced convergence. Here's the semantic blueprint:

- **Goal**: Design demo that convinces you to adopt Palette (success = you say 'we could build this, but they already did it better')
- **Roles**: I approve ONE-WAY DOORS, agents execute within constraints
- **Capabilities**: Full codebase, knowledge library, RIU taxonomy, live coding
- **Constraints**: 40 min, laptop-executable, no access to your codebase yet, exceptionally technical audience
- **Non-goals**: Not a basic ChatGPT demo, not a sales pitch, not explaining from first principles

Notice what's NOT here: vague requirements. Palette refuses to proceed without clarity.

Only after I approved this blueprint did agents start executing."

---

### Prompt 4: Show Agent Coordination (12 min)

**SHOW**: `decisions.md` — scroll through "Agent Execution Log" section

#### Agent 1: Argentavis (Argy) — 3 min

**SAY THIS**:

"First agent: **Argentavis (Argy)** — research specialist.

**Constraint**: Read-only, no synthesis-as-decision.

**Task**: Research demo strategies for technical audiences.

**What Argy did**:
- Checked knowledge library first (86 questions) — PARTIAL HIT
- Researched externally: HashiCorp, Temporal, Modal demo patterns
- Found: Technical audiences trust failure transparency over perfection claims
- Recommended: Meta-demo with 60/40 deep/breadth split

**Key insight**: Argy stayed within constraints. Didn't make architecture decisions, just provided research. That's enforced by Palette.

**Status**: SUCCESS — first impression logged (success=1, fail=0, fail_gap=1, status=UNVALIDATED)"

---

#### Agent 2: Tyrannosaurus (Rex) — 4 min

**SAY THIS**:

"Second agent: **Tyrannosaurus (Rex)** — architect.

**Constraint**: Must flag ONE-WAY DOOR decisions, proposes but doesn't commit.

**Task**: Evaluate demo flow options with tradeoff analysis.

**What Rex did**:
- Evaluated 5 options:
  - Option A: Meta-demo (use Palette to design its own demo)
  - Option B: Solve real problem live (too risky — don't know your problem)
  - Option C: Show failure and recovery (too narrow)
  - Option D: Build mini-agent live (too narrow)
  - Option E: Combination (meta-demo + constraint enforcement + vision)
- Recommended Option E with clear rationale

**Here's the critical part**:"

**SHOW**: Scroll to "🚨 ONE-WAY DOOR" flag in Rex's output

**SAY THIS**:

"Rex flagged this as **ONE-WAY DOOR** — can't pivot demo scenario mid-presentation.

Palette PAUSED execution and required my explicit approval.

I approved Option E, and only then did we proceed.

**This is how Palette prevents silent failures** — force explicit confirmation on high-stakes decisions.

**Status**: SUCCESS — impression logged (success=1, fail=0, fail_gap=1, status=UNVALIDATED)"

---

#### Agent 3: Yutyrannus (Yuty) — 3 min

**SAY THIS**:

"Third agent: **Yutyrannus (Yuty)** — narrative specialist.

**Constraint**: Evidence-based only, no overpromising.

**Task**: Generate demo script with timing and talking points.

**Input**: Argy's research + Rex's architecture.

**Output**: Complete demo script (0-45 min breakdown, meta-commentary, Q&A prep).

**Key insight**: Every claim Yuty makes must be backed by evidence. The script includes 'Evidence:' markers throughout — that's enforced.

**Status**: SUCCESS — impression logged (success=1, fail=0, fail_gap=1, status=UNVALIDATED)"

---

#### Agent 4: Ankylosaurus (Anky) — 2 min

**SAY THIS**:

"Fourth agent: **Ankylosaurus (Anky)** — validator.

**Constraint**: Assessment only, no remediation.

**Task**: Review entire plan, identify risks and gaps.

**What Anky found**:
- 7 risks identified (timing overrun, inception confusion, overstating maturity, etc.)
- All mitigated with 5 recommendations
- Critical risks: NONE (no blockers)
- Overall assessment: **DEMO PLAN IS EXECUTABLE**

**Key insight**: Anky doesn't fix problems — just identifies them. Separation of concerns. Assessment vs execution.

**Status**: SUCCESS — impression logged (success=1, fail=0, fail_gap=1, status=UNVALIDATED)"

---

### Prompt 5: Show decisions.md Logging (3 min)

**SHOW**: Scroll through entire `decisions.md` entry

**SAY THIS**:

"Everything we just did is logged here:
- Convergence brief — complete semantic blueprint
- Agent executions — Argy/Rex/Yuty/Anky with inputs/outputs
- ONE-WAY DOOR decisions — flagged and approved
- Agent impressions — success/fail/fail_gap tracking
- Next steps — what happens after this planning session

**If I get hit by a bus tomorrow, someone else can read this file and continue exactly where we left off.**

That's restartability.

Not exhaustive logs — just what matters for institutional memory.

**Note**: The actual demo planning engagement would be logged in decisions.md. For this demo, we're showing the meta-approach — using Palette to design the demo itself."

---

### Prompt 6: Constraint Enforcement Deep Dive (5 min)

**SAY THIS**:

"Let me show you what happens when an agent tries to exceed its scope."

**EXAMPLE 1**: Argy Boundary Violation

**SAY THIS**:

"If I asked Argy: 'Which demo approach should we use?'

Argy would respond:
> ⚠️ CONSTRAINT VIOLATION — I'm a research agent (read-only). I can provide findings on demo strategies, but architecture decisions must route to Tyrannosaurus (Rex). Recommendation: Route this to Rex with my research as input.

Argy refuses. Not because it can't answer, but because Palette enforces boundaries.

This prevents scope creep and maintains reliability."

---

**EXAMPLE 2**: ONE-WAY DOOR Pause

**SHOW**: Rex's ONE-WAY DOOR flag again

**SAY THIS**:

"When Rex identified an irreversible decision, Palette paused.

Required my approval before proceeding.

This is how Palette prevents silent failures — force explicit confirmation on high-stakes decisions.

**Constraints aren't limitations — they're reliability guarantees.** You know exactly what each agent will and won't do."

---

### Prompt 7: Self-Improving Infrastructure Vision (5 min)

**SHOW**: `PALETTE_VISION.md` file

**SAY THIS**:

"Here's what becomes possible over time:

**Agent Evolution**:
- Right now: All agents UNVALIDATED (Tier 1 — human-in-loop)
- After 10 successes: Promoted to WORKING (Tier 2 — autonomous with review)
- After 50 runs <5% failure: Promoted to PRODUCTION (Tier 3 — fully autonomous)
- Two failures within 10 runs: Demoted

You're watching first impressions being logged right now.

**Knowledge Library Growth**:
- Today: 86 questions across 7 problem types
- 6 months: 300+ questions with validated answers
- 2 years: 800+ questions covering edge cases you've actually encountered
- Agents retrieve proven patterns instead of hallucinating

**Cross-Domain Pattern Recognition**:
- Use Palette on game dev, data infrastructure, ed-tech
- Taxonomy shows you: 'RIU-042 appears in 80% of successful engagements'
- You're discovering deep structure of how problems get solved

**Institutional Knowledge**:
- New engineer joins your team
- Reads decisions.md from 3 past engagements
- Understands how you think, what works, what fails
- Productive on day 1

**The Compounding Effect**:
- Year 1: 5 agents, 10 engagements, 200 decisions
- Year 2: Agents at PRODUCTION tier, 3x faster
- Year 3: Library of proven patterns across industries

**You're not building a tool. You're building a flywheel that turns experience into capability.**"

---

### Prompt 8: Q&A (7 min)

**Prepare for these 5 questions**:

---

#### Q1: "How is this different from LangChain/AutoGPT/other agent frameworks?"

**ANSWER**:

"Those are execution frameworks — they help agents call tools and chain actions.

Palette is a **decision framework** — it helps humans and AI converge on the right problem before executing.

Key differences:
- **Convergence-first**: Palette refuses to proceed without semantic blueprint
- **Glass-box**: Every decision is traceable (not black-box agent chains)
- **Empirical trust**: Agents earn autonomy through measured performance
- **Restartability**: decisions.md enables anyone to continue your work

You could use LangChain as an execution layer underneath Palette agents. They solve different problems."

---

#### Q2: "What if we want to build our own agents?"

**ANSWER**:

"That's the point. Palette is a framework, not a product.

You define:
- Agent archetypes (what they do, what they don't do)
- Constraints (boundaries they can't cross)
- Maturity criteria (how they earn trust)

Palette provides:
- Three-tier architecture (convergence, maturity, logging)
- RIU taxonomy (104 reusable intervention patterns in v1.2)
- Knowledge library (86 questions, growing)
- Decision logging system

You build agents that fit your domain. Palette ensures they're reliable and improvable."

---

#### Q3: "How do you handle agent failures?"

**ANSWER**:

"Three ways:

1. **Constraint enforcement** (prevention): Agents refuse out-of-scope tasks
2. **ONE-WAY DOOR pausing** (prevention): System requires human approval on irreversible decisions
3. **Maturity demotion** (response): Two failures within 10 runs = demote to lower tier

Every failure gets logged with reasoning (post-mortem in decisions.md).

Failures are treated as signal, not error. They improve the system."

---

#### Q4: "What's the learning curve for our team?"

**ANSWER**:

"Depends on role:

**FDE operators** (using Palette):
- Read palette-core.md (20 min)
- Read 2-3 decisions.md examples (30 min)
- Run first engagement with guidance (2 hours)
- Productive within a day

**Agent builders** (extending Palette):
- Understand three-tier architecture (1 hour)
- Study agent archetype patterns (2 hours)
- Build first agent with fixtures (4-8 hours)
- Iterate based on impressions

The system is designed for restartability — documentation is executable, not just explanatory."

---

#### Q5: "Can we see the code?"

**ANSWER**:

"Yes. Everything you've seen is in these files:

**Core System**:
- `/home/mical/palette/.kiro/steering/palette-core.md` — Tier 1 rules
- `/home/mical/palette/.kiro/steering/assumptions.md` — Tier 2 agent definitions
- `/home/mical/palette/decisions.md` — Tier 3 execution log

**Knowledge Assets**:
- `/home/mical/palette/knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml` — 86 questions + answers + sources
- `/home/mical/palette/taxonomy/releases/v1.2/palette_taxonomy_v1.2.yaml` — 104 RIUs (Reusable Intervention Units)

**Agents** (4 implemented):
- `/home/mical/palette/agents/argentavis/` — Argy (research)
- `/home/mical/palette/agents/rex/` — Rex (architect)
- `/home/mical/palette/agents/therizinosaurus/` — Theri (builder)
- `/home/mical/palette/agents/velociraptor/` — Raptor (debugger)

All open, all inspectable. Glass-box by design.

Want to walk through any specific file?"

---

### Closing (1 min)

**SAY THIS**:

"That's Palette. Three tiers. Four agents. One real problem solved.

You just watched Palette design its own demo — proving it works while showing how it works.

**Questions? Or want to use Palette on one of your actual problems next?**"

---

## Post-Demo Actions

After the demo:
1. **Log execution to decisions.md** (record whether demo was successful)
2. **Update agent impressions** (success/fail for each agent based on demo outcome)
3. **Capture new questions** for knowledge library
4. **Propose follow-up engagement** if they're interested

---

**End of Demo Guide**
