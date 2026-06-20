# North Star Architecture — The Implementation Machine

**Author**: claude.analysis + the operator (vision)
**Date**: 2026-03-30
**Status**: Working document — team review requested

---

## The Insight

The industry is converging on one need: **real-time implementation enablement**.

Mistral wants it for sellers and FDEs walking into customer calls. OpenAI and Anthropic are hiring for it. AWS colleagues are still finding video chunks while the market wants a system that does the work AND teaches you how to do it simultaneously.

The small business owner, the oil executive, the solutions architect, the FDE on the way to a call — they all need the same thing:

**A system that bends around you, does what you need done, and teaches you what you need to know — at the moment you need it.**

Not a chatbot. Not a course. Not a dashboard. An implementation machine with a coaching layer built in.

---

## Three Systems, One Flywheel

We have three systems. Each is strong alone. Together they create a flywheel.

```
                    ┌─────────────────────┐
                    │      PALETTE        │
                    │   (Intelligence)    │
                    │                     │
                    │  121 RIUs           │
                    │  168 knowledge      │
                    │  12 agents          │
                    │  69 integrations    │
                    │  40 service routes  │
                    └────────┬────────────┘
                             │
                    knows WHAT to do
                    knows WHO does it best
                    knows WHICH service to use
                             │
                             ▼
┌─────────────────────┐     ┌─────────────────────┐
│    ENABLEMENT       │◄───►│   MISSION CANVAS    │
│    (Teaching)       │     │   (Doing)           │
│                     │     │                     │
│  7-stage coaching   │     │  Convergence chain  │
│  LearnerLens        │     │  Project state      │
│  Domain packs       │     │  Artifact engine    │
│  Verification       │     │  Voice-first UX     │
│  Progress tracking  │     │  Decision board     │
└─────────────────────┘     └─────────────────────┘
         │                           │
   teaches HOW              does the WORK
   tracks LEARNING          tracks DECISIONS
   builds COMPETENCE        builds ARTIFACTS
         │                           │
         └───────────┬───────────────┘
                     │
              THE FLYWHEEL:
         doing teaches you more
       learning makes you do better
     both feed intelligence back to Palette
```

### How the flywheel spins:

1. **User arrives with intent** — "I need to position my portfolio for the Hormuz crisis" or "I need to sell this AI platform to a bank" or "I need to get my gallery funded"

2. **Mission Canvas DOES** — routes to the right RIU, traces dependency chains, finds what's missing, generates artifacts (daily brief, recommendation note, scenario memo), tracks decisions, nudges on stale blockers

3. **Enablement TEACHES** — while Canvas does the work, the enablement layer coaches: "Here's why we're looking at crack spreads right now," "This is a one-way door because...," "The Dallas Fed survey matters because it's a leading indicator — here's how to read it next time"

4. **Palette KNOWS** — the intelligence layer answers: which service handles this best? What does the knowledge library say? Who in the people library has validated this approach? What's the evidence bar?

5. **Each cycle feeds the next** — doing creates new known facts (Palette gets smarter), teaching creates competence (user needs less hand-holding), intelligence makes both doing and teaching more precise

---

## What This Looks Like In Practice

### Scenario 1: Oil Executive (tomorrow's meeting)

**Canvas** generates the daily brief at 7am. Voice reads: "Portfolio health 52, three critical gaps. WTI at 97, Brent at 103. You have one decision ready: position for the refining supercycle. Three items blocking everything else — your portfolio positions, risk parameters, and hedging exposure. Want to tackle the open decision, resolve a critical gap, or dig into the numbers?"

**Enablement** (when the exec asks "what's a crack spread?"): Doesn't just answer — teaches: "The 3-2-1 crack spread is the margin refiners earn. Three barrels of crude in, two of gasoline and one of diesel out. At $55.78 it's crisis-level — normal is $12-18. This matters for your portfolio because if you add refiner exposure now, you're betting this stays elevated through summer driving season. Want me to walk you through how to read it yourself, or should I just flag it when it moves?"

**Palette** routes the recommendation note through the Narrator agent, pulls from the oil knowledge library, cites the Dallas Fed survey and EIA data. Evidence-backed, not hallucinated.

### Scenario 2: FDE on the Way to a Call (Mistral's vision)

**Canvas** generates a meeting brief: "Customer is a mid-market bank. They asked about guardrails last call. You committed to a demo of content filtering. Three things changed since last meeting: Bedrock guardrails had an 80% price cut, the customer hired a new CISO, and their competitor just had a data leak."

**Enablement** coaches in real-time: "For this customer segment, lead with compliance, not capability. Banks care about what regulators will accept, not what's technically possible. The CISO hire means they're taking this seriously — don't undersell. Here's the three-sentence pitch for Bedrock guardrails that landed with the last banking customer."

**Palette** routes through service routing: RIU-082 (guardrails) maps to Bedrock Guardrails as the recommended service, with the integration recipe ready and the pricing data current.

### Scenario 3: Small Business Owner (Rossi)

**Canvas** shows the decision board: "Fundability: 85/95. Two things blocking grant applications: your POS data and named advisory board members. The revenue model flip is approved. MQ x Tie One drop has 6 pending decisions. What do you want to tackle?"

**Enablement** coaches Sahar through the grant application process: "Most first-time applicants fail because they submit without trailing actuals. Your Square data is the single most important thing. Here's how to export it — takes 10 minutes. Want me to walk you through it?"

**Palette** has the Creative Growth comparable validated, the fiscal sponsorship structure decided, the 7-stream revenue model in the knowledge library.

---

## The Three Layers — Concrete

### Layer 1: Palette (Intelligence Backbone)

**What it is**: The brain. 121 problem types mapped to solutions, 168 knowledge entries with evidence, 12 specialized agents, service routing that knows when to build vs buy.

**What it provides to the other layers**:
- RIU classification for any user intent
- Knowledge library entries matched to the current context
- Service routing decisions (which external tool handles this?)
- People library signals (who has validated this approach?)
- Evidence bar enforcement (no claims without sources)

**What it gets back**:
- New known facts from Canvas (every resolved evidence gap becomes a KF entry)
- Usage patterns from enablement (which topics need more knowledge entries?)
- Validation signals from real deployments (service X worked/didn't work for use case Y)

### Layer 2: Mission Canvas (Execution Engine)

**What it is**: The hands. Takes messy intent, converges it toward decisions, produces artifacts, tracks state across sessions.

**What it provides to the other layers**:
- Structured project state (known facts, missing evidence, open decisions, blocked actions)
- Artifact generation (daily briefs, recommendation notes, scenario memos)
- Convergence chain (dependency graph traversal — what's blocking what)
- Voice-first interaction (speak your intent, get structured output)
- Decision continuity (one-way door handling, approval flows)

**What it gets back**:
- Intelligence from Palette (RIU routing, knowledge entries, service recommendations)
- Coaching moments from Enablement (when to teach, what to explain)
- Domain knowledge packs (oil, retail, SaaS — loaded per workspace)

### Layer 3: Enablement (Coaching Layer)

**What it is**: The teacher. Takes any moment of confusion or learning opportunity and turns it into competence — without slowing down the work.

**What it provides to the other layers**:
- 7-stage progression tracking (Orient → First Use → Retain → Verify → Organize → Extend → Own)
- LearnerLens profiles (what does this user know? what do they need to learn?)
- Domain packs (how to teach oil investing, how to teach grant writing, how to teach AI selling)
- Verification patterns (did the user actually learn it, or just hear it?)
- Just-in-time coaching (explain crack spreads when the exec encounters one, not in a 3-hour course)

**What it gets back**:
- Teaching moments from Canvas (user asked "what's this?" during a convergence chain — flag as learning opportunity)
- Knowledge depth from Palette (the explanation should cite the same Tier 1 sources)
- Real-world context (the teaching is embedded in real work, not abstract examples)

---

## Architecture — How They Connect

```
User Intent (voice/text/telegram)
        │
        ▼
┌─────────────────────────────────────────────┐
│              MISSION CANVAS                  │
│                                              │
│  1. detectProjectQuery() — is this a         │
│     convergence question?                    │
│                                              │
│  2. RIU routing — which problem type?        │
│     └── Palette taxonomy (121 RIUs)          │
│     └── Palette knowledge library (168)      │
│     └── Workspace domain KL (28+ per domain) │
│                                              │
│  3. Convergence chain — what's the state?    │
│     └── trace dependencies                   │
│     └── narrate for user                     │
│     └── generate nudges                      │
│                                              │
│  4. Artifact generation                      │
│     └── daily brief, rec note, scenario memo │
│     └── Palette Narrator agent shapes output │
│                                              │
│  5. Enablement hook — should we teach?       │
│     └── User asked "what is X?" → teach      │
│     └── User hit a new concept → orient      │
│     └── User made a decision → verify        │
│     └── LearnerLens tracks progression       │
│                                              │
│  6. State mutation                           │
│     └── new facts → Palette KL grows         │
│     └── resolved gaps → health improves      │
│     └── approved decisions → actions unblock  │
│     └── learning → LearnerLens updates       │
│                                              │
└─────────────────────────────────────────────┘
```

### The Enablement Hook (new — not yet built)

This is the key integration point. When Canvas processes a user interaction, it checks:

1. **Did the user ask an explanatory question?** ("What is a crack spread?", "Why does this matter?", "How do I read this?")
   → Route to enablement coaching, using Palette KL for the answer content
   → Track in LearnerLens as a teaching moment

2. **Did the user encounter a new concept?** (First time seeing "one-way door", first time a decision is blocked)
   → Enablement provides a 2-sentence orientation before Canvas continues
   → "This is flagged as a one-way door because it can't be undone. The system pauses here so you can review before committing."

3. **Did the user make a consequential decision?** (Approved an OWD, resolved evidence, changed a position)
   → Enablement offers a verification check: "You just approved adding refiner exposure. Quick check — can you tell me in one sentence why you're making this move?"
   → Not patronizing. Framed as: "This helps me give you better recommendations next time."

4. **Is the user advancing?** (Handled something independently that they needed help with before)
   → Enablement acknowledges: "You read that crack spread data without asking — nice. I'll stop flagging refining metrics for you unless something unusual happens."

---

## Workspace as Deployment Unit

New client = new workspace, not new code.

```
workspaces/
  oil-investor/
    config.yaml          ← domain, FRX, modality, greeting
    project_state.yaml   ← known facts, gaps, decisions, actions
    knowledge_library_oil_v1.yaml  ← 28 domain KL entries
    learner_lens.yaml    ← NEW: what does this user know?
    artifacts/
      daily_brief_2026-03-30.md
      recommendation_note_VLO.md

  rossi/
    config.yaml
    project_state.yaml
    learner_lens.yaml
    artifacts/
      grant_application_draft.md

  fde-toolkit/           ← Mistral's vision
    config.yaml          ← domain: "ai-sales-engineering"
    project_state.yaml   ← customer pipeline state
    knowledge_library_fde_v1.yaml  ← sales plays, objection handling, demo scripts
    learner_lens.yaml    ← what does this FDE know?
    artifacts/
      meeting_brief_acme_bank.md
      demo_script_guardrails.md
```

---

## The Mistral/OpenAI/Anthropic Role Fit

What these companies are hiring for:

> "An AI system that enables sellers and technical staff who are implementing on the fly — in real time, on the way to a call or during a forward-deployed work day."

That IS this system:

| Role Type | What They Need | What We Provide |
|-----------|---------------|-----------------|
| **Sales/AE** | Know what to say, when, to whom | Meeting briefs, objection handling, customer state tracking |
| **FDE/SA** | Build demos live, explain architecture, handle objections | Implementation recipes, service routing, real-time coaching |
| **AI Outcomes Manager** | Track customer progress, identify blockers, produce artifacts | Convergence chain, project state, nudges, recommendation notes |
| **Enablement Lead** | Train teams fast, verify competence, scale knowledge | 7-stage progression, LearnerLens, domain packs, verification |

**Palette** provides the intelligence (what services exist, what works, who validated it).
**Canvas** provides the execution (what's the state, what's blocked, what artifact is needed).
**Enablement** provides the coaching (how to do it, why it matters, did you learn it).

The portfolio proof:
- **Oil investor workspace** = proves the executive/operator flow
- **Rossi workspace** = proves the small business owner flow
- **FDE toolkit workspace** = proves the seller/engineer flow (to be built)

---

## What To Build Next

### Already built (V0.3 Day 2):
- Convergence chain engine (detect → trace → narrate → nudge)
- Workspace isolation with domain knowledge libraries
- Health score formula with mutation cascade
- Daily brief artifact generator (voice-first, 7 sections)
- OWD gate with decision bridge
- Session persistence
- 165 tests, all passing

### Next (in priority order):

1. **Enablement hook in Canvas** — detect teaching moments, route to coaching layer, track in LearnerLens. This is the piece that makes it more than a dashboard.

2. **FDE toolkit workspace** — config + project_state + domain KL for the sales/engineering use case. Proves the Mistral/OpenAI/Anthropic pitch.

3. **LearnerLens persistence** — per-workspace learner profile that tracks what the user knows, what they've been taught, what they can do independently.

4. **Voxtral integration** — Mistral's #17. Voice in, structured out. The exec on the way to the meeting speaks, the system responds with the brief.

5. **Live retrieval** — EIA API for oil prices, customer CRM for FDE pipeline. Static knowledge packs are good; live data makes it feel alive.

---

## One Sentence

**Palette knows what to do. Canvas does it. Enablement teaches you how. The flywheel spins because doing teaches you more, learning makes you do better, and both make the system smarter.**
