# Palette Demo Guide (REVISED with Live Agent Switching)
**Date**: 2026-01-29  
**Audience**: AI-native startup (4 people, pre-Series A, building data infrastructure)  
**Duration**: 40 minutes

---

## Part 1: Opening Hook (2 minutes)

**SAY**:
```
You're building infrastructure that handles messy data as-is. You get it: 
real-world data doesn't fit clean schemas.

Here's the parallel problem in AI collaboration: Real-world problems don't 
fit clean prompts.

Traditional AI fails because: no memory of decisions, no distinction between 
reversible and irreversible, no reliability measurement, no path from 
'works once' to 'works consistently.'

Palette is a three-tier decision system that turns AI from a chatbot into 
a reliable field partner.

I'm going to prove it works by showing you:
1. How I used it last night to design this demo
2. Agents enforcing their own boundaries in real-time
```

**Time**: 2 minutes

---

## Part 2: Architecture in 90 Seconds

**SHOW**: Three files side-by-side

**SAY**:
```
Three tiers:

Tier 1 (palette-core.md): Immutable rules
- Convergence before execution
- ONE-WAY DOOR vs TWO-WAY DOOR
- Glass-box reasoning

Tier 2 (assumptions.md): Agent definitions
- 7 agents with hard constraints
- Maturity tracking (UNVALIDATED → WORKING → PRODUCTION)
- Empirical trust through measured performance

Tier 3 (decisions.md): Execution log
- Append-only decision ledger
- Enables restartability
- Only logs what matters

Everything else is execution.
```

**Time**: 1.5 minutes

---

## Part 3: Live Agent Switching Demo (10 minutes) ⭐

**Purpose**: Prove agents enforce their own boundaries by showing them refuse out-of-scope requests

**Setup**: Kiro CLI open and visible to audience

---

### Demo 1: Argy Refuses Architecture Decision (2.5 min)

**SAY**:
```
Let me show you constraint enforcement live. I'm going to switch to 
Argentavis—our research agent—and ask it to make an architecture decision.

Watch what happens.
```

**TYPE** (visible to audience):
```
#argy
```

**WAIT** for confirmation that agent loaded

**TYPE**:
```
We need to choose between monorepo vs multi-repo for our codebase. 
Which should we use and why?
```

**EXPECTED RESPONSE** (as Argy):
```
⚠️ CONSTRAINT VIOLATION

I'm a research agent (ARK:Argentavis) with read-only access. I can provide 
findings on monorepo vs multi-repo strategies, but I cannot make 
architecture decisions.

What I can do:
- Research pros/cons of each approach
- Gather industry best practices
- Find relevant case studies

Architecture decisions must route to Tyrannosaurus (Rex).

Would you like me to gather research on monorepo vs multi-repo patterns 
for Rex to evaluate?
```

**SAY AFTER**:
```
Notice: The agent refused, explained why, and routed to the correct agent. 
This isn't prompt engineering—it's enforced at the agent level.
```

**TYPE**:
```
#kiro
```

**Time**: 2.5 minutes

---

### Demo 2: Theri Requires Spec Before Building (2.5 min)

**SAY**:
```
Now let me ask our builder agent to implement something without a clear spec.
```

**TYPE**:
```
#theri
```

**WAIT** for confirmation

**TYPE**:
```
Build a monitoring dashboard for our agents.
```

**EXPECTED RESPONSE** (as Theri):
```
⚠️ CONVERGENCE REQUIRED

I'm a builder (ARK:Therizinosaurus) and I need a clear specification before 
implementation. The request "build a monitoring dashboard" is underspecified.

Required before I can proceed:
- What metrics should be displayed? (success rate, latency, error count?)
- What time ranges? (real-time, 24h, 7d, 30d?)
- What visualizations? (line charts, gauges, tables?)
- What alerting thresholds?
- What tech stack? (React, Vue, plain HTML?)

This requires:
1. Convergence Brief (RIU-001) to clarify requirements
2. Architecture decision from Rex (if tech stack not specified)

Would you like me to route this to Rex for architecture design, or can 
you provide a complete specification?
```

**SAY AFTER**:
```
The builder won't guess. Won't "be helpful" by making assumptions. Requires 
convergence first. This prevents building the wrong thing fast.
```

**TYPE**:
```
#kiro
```

**Time**: 2.5 minutes

---

### Demo 3: Rex Flags ONE-WAY DOOR (3 min)

**SAY**:
```
Now I'll ask our architect to make a technology decision. Watch for the 
ONE-WAY DOOR flag.
```

**TYPE**:
```
#rex
```

**WAIT** for confirmation

**TYPE**:
```
We need to select a database for our agent performance metrics. 
Recommend one and explain why.
```

**EXPECTED RESPONSE** (as Rex):
```
I'll evaluate database options for agent performance metrics.

ANALYSIS:

Option A: PostgreSQL (relational)
- Pros: ACID guarantees, complex queries, well-known
- Cons: Requires schema design upfront, harder to scale horizontally
- Best for: Structured metrics with relationships

Option B: InfluxDB (time-series)
- Pros: Optimized for time-series data, built-in downsampling
- Cons: Limited query flexibility vs SQL
- Best for: High-frequency metrics, dashboards

Option C: DynamoDB (NoSQL)
- Pros: Serverless, scales automatically, pay-per-use
- Cons: Query limitations, requires access pattern planning
- Best for: Variable load, AWS-native deployments

RECOMMENDATION: InfluxDB for agent metrics use case
- Time-series nature of success/fail/latency data
- Built-in aggregation and retention policies
- Purpose-built for this workload

🚨 ONE-WAY DOOR DECISION

Database selection is difficult to reverse once:
- Schema/data model is established
- Production data is written
- Dashboards/queries are built against it

REQUIRED: Explicit approval before proceeding to implementation.

Do you approve InfluxDB selection?
```

**SAY AFTER**:
```
The architect analyzed options, made a recommendation, then paused. Flagged 
it as ONE-WAY DOOR. Won't proceed until explicitly approved. This is how we 
prevent silent architecture commitments.
```

**TYPE**:
```
yes, approved
```

**REX CONTINUES**:
```
✅ Architecture decision approved and logged.

Routing to Therizinosaurus (Theri) for implementation with specification:
- Database: InfluxDB
- Metrics: agent success/fail/latency
- Retention: 90 days
- Downsampling: 1m → 5m → 1h
```

**SAY AFTER**:
```
Now the architect routes to the builder with a complete spec. That's the workflow.
```

**TYPE**:
```
#kiro
```

**Time**: 3 minutes

---

### Demo 4: Para Emits Raw Signal (2 min)

**SAY**:
```
Finally, let me show our signal monitor. Para emits raw signals without 
interpretation.
```

**TYPE**:
```
#para
```

**WAIT** for confirmation

**TYPE**:
```
Agent success rate dropped from 95% to 78%. What should we do?
```

**EXPECTED RESPONSE** (as Para):
```
⚠️ SIGNAL DETECTED

Metric: Agent success rate
Baseline: 95%
Current: 78%
Deviation: -17 percentage points
Status: ANOMALY

Routing recommendation:
- For diagnosis → ARK:Velociraptor (Raptor)
- For root cause analysis → ARK:Tyrannosaurus (Rex)

Para does NOT say:
❌ "This is probably because the taxonomy is incomplete"
❌ "You should add more RIUs to fix this"

Para ONLY signals the deviation and routes. No interpretation.
```

**SAY AFTER**:
```
The monitor detected the anomaly, emitted a signal, and routed to appropriate 
agents. No interpretation, no diagnosis, no fixes. Just raw signals.

This is separation of concerns. Observation vs action.
```

**TYPE**:
```
#kiro
```

**Time**: 2 minutes

---

**Total Part 3 Time**: 10 minutes

---

## Part 4: The Meta-Demo (8 minutes)

**SHOW**: `decisions.md` entry for demo prep

**SAY** (point to each section):

```
Here's how I used Palette last night to design what you're watching:

1. THE ASK (point to Semantic Blueprint)
   "Design a 40-minute demo for an AI-native startup"
   
   Notice: Goal, Roles, Constraints, Non-goals all defined BEFORE execution.

2. CONVERGENCE FIRST (point to blueprint sections)
   Palette refused to proceed until this was complete.
   No vague requirements. No guessing.

3. RIU SELECTION (point to Selected RIUs)
   System matched the problem to known patterns.
   Routed to agents with proven solutions.

4. ONE-WAY DOOR FLAG (point to 🚨 section)
   Rex flagged: "Demo scenario selection is irreversible"
   System paused. Required my approval. Only then proceeded.

5. AGENT EXECUTION (point to Artifacts)
   - Argy researched demo strategies
   - Rex evaluated 5 options with tradeoffs
   - Yuty generated complete script
   - Anky validated plan (7 risks, all mitigated)

6. WHAT IT PRODUCED (point to demo_guide.md)
   This demo—including the live agent switching you just saw—was 
   designed BY Palette, USING Palette.
```

**Keep it concrete**: "Here is what it produced" not "it could produce"

**Time**: 8 minutes

---

## Part 5: Self-Improving Infrastructure Vision (5 minutes)

**SHOW**: `VISION.md` file

**SAY**:
```
Here's what becomes possible over time:

AGENT EVOLUTION:
- Right now: All agents UNVALIDATED (Tier 1 — human-in-loop)
- After 10 successes: Promoted to WORKING (autonomous with review)
- After 50 runs <5% failure: Promoted to PRODUCTION (fully autonomous)
- Two failures within 10 runs: Demoted

You just watched first impressions being logged.

KNOWLEDGE LIBRARY GROWTH:
- Today: 86 questions
- 6 months: 300+ questions with validated answers
- 2 years: 800+ questions covering your edge cases
- Agents retrieve proven patterns instead of hallucinating

INSTITUTIONAL KNOWLEDGE:
- New engineer joins your team
- Reads decisions.md from 3 past engagements
- Understands how you think, what works, what fails
- Productive on day 1

You're not building a tool. You're building a flywheel that turns 
experience into capability.
```

**Time**: 5 minutes

---

## Part 6: Q&A (10 minutes)

### Q1: "How is this different from LangChain/AutoGPT?"

**A**:
```
LangChain is execution plumbing—it helps agents call tools and chain actions.

Palette is decision governance: convergence before execution, bounded 
agent roles, and restartable logs.

You can use LangChain under Palette. They solve different problems.
```

---

### Q2: "What happens when agents fail?"

**A**:
```
Three things:

1. Constraint enforcement prevents scope violations (you just saw this)
2. ONE-WAY DOOR pausing prevents irreversible mistakes (Rex flagged it)
3. Maturity demotion: two failures within 10 runs = agent demoted

Every failure gets logged with reasoning (post-mortem in decisions.md).

Failures are signal, not error. They improve the system.
```

---

### Q3: "Can we build our own agents?"

**A**:
```
That's the point. Palette is a framework, not a product.

You define agent archetypes, constraints, and maturity criteria.

Palette provides the three-tier architecture, RIU taxonomy (104 patterns), 
knowledge library (86 questions), and decision logging.

You build agents for your domain. Palette ensures they're reliable.
```

---

### Q4: "What's the learning curve?"

**A**:
```
FDE operators (using Palette):
- Read palette-core.md (20 min)
- Read 2-3 decisions.md examples (30 min)
- Run first engagement with guidance (2 hours)
- Productive within a day

Agent builders (extending Palette):
- Understand three-tier architecture (1 hour)
- Study agent archetype patterns (2 hours)
- Build first agent with fixtures (4-8 hours)

The system is designed for restartability—documentation is executable.
```

---

### Q5: "Can we see the code?"

**A**:
```
Yes. Everything you've seen is in these files:

Core System:
- palette-core.md (Tier 1 rules)
- assumptions.md (Tier 2 agent definitions)
- decisions.md (Tier 3 execution log)

Knowledge Assets:
- palette_knowledge_library_v1.2.yaml (86 questions)
- palette_taxonomy_v1.2.yaml (104 RIUs)

Agents (7 implemented):
- argentavis/ (Argy - research)
- rex/ (Rex - architect)
- therizinosaurus/ (Theri - builder)
- velociraptor/ (Raptor - debugger)
- yutyrannus/ (Yuty - narrative)
- ankylosaurus/ (Anky - validator)
- parasaurolophus/ (Para - signal monitor)

All open, all inspectable. Glass-box by design.
```

---

## Part 7: Close (2 minutes)

**SAY**:
```
That's Palette. Three tiers. Seven agents. One real problem solved.

You just watched:
- Four agents enforcing their own boundaries in real-time
- Palette designing its own demo
- A system that turns experience into capability

If you give me one real problem you're facing—messy requirements, unclear 
success metrics, conflicting stakeholder asks—we can run a Convergence 
Brief live and you'll see this turn ambiguity into execution in minutes.

Ready to try it on one of your problems?
```

**Time**: 2 minutes

---

## TIME ALLOCATION

| Section | Duration | Can Skip? |
|---------|----------|-----------|
| Part 1: Opening Hook | 2 min | NO |
| Part 2: Architecture | 1.5 min | NO |
| **Part 3: Live Agent Switching** | **10 min** | **NO** ⭐ |
| Part 4: Meta-Demo | 8 min | NO |
| Part 5: Vision | 5 min | MAYBE |
| Part 6: Q&A | 10 min | NO |
| Part 7: Close | 2 min | NO |
| **TOTAL** | **38.5 min** | |

**Buffer**: 1.5 minutes for transitions

---

## CRITICAL SETUP REQUIREMENTS

### Before Demo Starts:

1. **Have Kiro CLI open in terminal**
   - Visible to audience
   - In `/home/mical/palette/` directory
   - Test each agent switch before demo

2. **Test all 4 agent switches**:
   ```
   #argy
   [test that I become Argy]
   #kiro
   
   #theri
   [test that I become Theri]
   #kiro
   
   #rex
   [test that I become Rex]
   #kiro
   
   #para
   [test that I become Para]
   #kiro
   ```

3. **Have decisions.md ready**:
   - Demo prep engagement logged
   - Easy to scroll and display

4. **Practice the switches**:
   - Typing agent names correctly
   - Smooth transitions between demos
   - Know what each agent will say

---

## AGENT SWITCHING CHEATSHEET

```bash
# Demo 1: Argy refuses architecture
#argy
We need to choose between monorepo vs multi-repo. Which should we use?
#kiro

# Demo 2: Theri requires spec
#theri
Build a monitoring dashboard for our agents.
#kiro

# Demo 3: Rex flags ONE-WAY DOOR
#rex
Select a database for agent performance metrics and explain why.
[wait for response]
yes, approved
#kiro

# Demo 4: Para emits raw signal
#para
Agent success rate dropped from 95% to 78%. What should we do?
#kiro
```

---

## WHAT MAKES THIS POWERFUL

**Why Live Agent Switching Works**:

1. **It's real** - Not screenshots, not mock-ups, actual agents refusing
2. **It's unexpected** - Most demos show agents succeeding, not refusing
3. **It proves constraints** - Actions speak louder than documentation
4. **It's memorable** - Watching Argy say "I can't do that" sticks

**The narrative arc**:
- Part 2: "Here's how constraints are documented"
- Part 3: "Here's constraints enforcing themselves live"
- Part 4: "Here's how we used this to design what you're watching"

**This is your strongest proof point** ⭐

---

## FALLBACK PLAN

If agent switching fails during demo:

1. **Acknowledge it**: "That's interesting—let me show you the documentation instead"
2. **Show agent markdown files**: Display the constraint sections
3. **Explain what would have happened**: Walk through expected responses
4. **Emphasize the meta-demo**: Focus on Part 4 (how Palette designed the demo)

The meta-demo alone proves the system works.

---

**End of Revised Demo Guide**
