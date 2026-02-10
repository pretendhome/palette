# Palette: Agent Toolkit for Forward Deployed Engineers

**Version**: 1.3  
**Status**: Production-Ready  
**Development Time**: 2.5 years  
**Validation**: AWS Solutions Engineering POC tools

---

## What Is Palette?

Palette is a three-tier agent toolkit that does the work of a team of language engineers.

I built this over 2.5 years at AWS, starting from a science team working on a POI knowledge graph (25 billion nodes). The whole team spent our time curating one main prompt, testing changes, iterating.

**I kept thinking: There has to be a better way.**

So I built a system with three tiers:
1. **Core Prompt** (Tier 1) — The final prompt, immutable rules, never changes
2. **Agents** (Tier 2) — Middle tier that tests problems against solutions and builds what's needed
3. **Testing at Scale** (Tier 3) — Logs what works, enables learning and promotion

**New in v1.3**: Enterprise security (agent identity, guardrails, least privilege), decision classification framework, and quality evaluation methods.

---

## The Three Artifacts

### 1. Optimized Taxonomy (105 RIUs)

Located: `taxonomy/releases/v1.2/palette_taxonomy_v1.2.yaml`

What I would design for AWS if I could start from scratch. Uses AWS "use cases"—problems connected to proven solutions. Hard-fought, battle-tested solutions that cover everything you can build on a cloud platform.

**Why this doesn't get outdated**: While technology changes (LLMs can do X, agents can do Y), the core customer problems and desired solutions are relatively static.

**New in v1.3**: RIU-105 (Agent Security & Access Control)

### 2. Knowledge Library (93 Questions + Answers + Sources)

Located: `knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml`

Curated GTM knowledge from AWS internal chatbot, validated with internal tooling. Each entry includes:
- Question
- Answer
- Source (many public, verifiable, cross-referenceable)
- Metadata connecting to taxonomy

**How it stays current**: Manually add sources when we find them. Do deep dives when areas feel lacking.

**New in v1.3**: 5 new entries (security, decision classification, quality evaluation)

### 3. Company-RIU Mapping Library (127 companies, 12 use cases)

Located: `company-library/v1.0/palette_company_riu_mapping_v1.0.yaml`

Maps 127 funded AI companies to Palette RIUs across 12 use cases. Market validation — funded companies = real problems. Each entry includes company name, funding stage, use case description, and RIU mapping.

**Why this matters**: If venture-backed companies are building solutions in a space, that's external evidence the problem is real. This library connects market signals to Palette's taxonomy.

**New in v1.3**: Initial baseline (v1.0), Perplexity validation pending

---

## How It Works

1. **You give me a problem**
2. **System classifies it in the taxonomy** (matches to one of 105 RIUs)
3. **Routes to an agent** that already has information on how to solve it
4. **Agent has access to**:
   - Internal code patterns (from agents/)
   - GTM knowledge library (93 Q&A pairs)
5. **Agent builds what's needed**
6. **When it does good work consistently, it gets promoted**:
   - UNVALIDATED → WORKING (after 10 successes)
   - WORKING → PRODUCTION (after 50 runs <5% failure)
   - Automatic demotion if 2 failures within 10 runs

---

## Day-One Value

**You give me a few problems. I immediately become a manager of agents solving those issues.**

The system:
- Classifies your problem
- Routes to appropriate agent
- Agent retrieves proven patterns
- Builds solution
- Learns from success/failure

---

## Active Projects

Three projects currently validate Palette in practice:

### 1. Teaching Agentic Systems (`/fde/projects/agent-class/`)
Interview prep and 30-minute demos showing how Palette's three-tier system works. Uses taxonomy routing and agent archetypes to teach agentic concepts with a live toolkit.

### 2. Small Business Help (`/fde/projects/rossi-mission/`)
Building a business plan for a graffiti art gallery. Palette routes the problem through RIUs covering customer engagement, market analysis, and operational planning.

### 3. Video Game Development (`/fde/projects/myth-fall-game/`)
Multiplayer RPG built with Godot + Node.js. Palette manages architecture decisions, implementation patterns, and quality validation across a complex game development stack.

---

## File Structure

```
palette/
├── README.md                           # This file
├── GETTING_STARTED.md                  # 5-minute onboarding
├── VISION.md                           # Self-improving infrastructure vision
├── CONTRIBUTING.md                     # How to contribute
├── CHANGELOG.md                        # Version history
├── DEMO.md                             # How to demo Palette
│
├── .kiro/steering/
│   ├── palette-core.md                 # Tier 1: Core prompt (immutable rules)
│   ├── assumptions.md                  # Tier 2: Agent definitions
│   └── TIER3_decisions_prompt.md       # Tier 3: Decision template
│
├── taxonomy/
│   ├── releases/v1.2/
│   │   └── palette_taxonomy_v1.2.yaml  # 105 RIUs (problems → solutions)
│   └── README.md                       # Taxonomy guide
│
├── knowledge-library/
│   ├── v1.2/
│   │   └── palette_knowledge_library_v1.2.yaml  # 93 Q&A + sources
│   └── README.md                       # Library guide
│
├── company-library/                    # Market validation (NEW in v1.3)
│   └── v1.0/
│       ├── palette_company_riu_mapping_v1.0.yaml  # 127 companies → RIUs
│       └── README.md                   # Company library guide
│
├── agents/                             # 7 agent implementations
│   ├── argentavis/                     # Argy - Research
│   ├── rex/                            # Rex - Architecture
│   ├── therizinosaurus/                # Theri - Build
│   ├── velociraptor/                   # Raptor - Debug
│   ├── yutyrannus/                     # Yuty - Narrative
│   ├── ankylosaurus/                   # Anky - Validate
│   ├── parasaurolophus/                # Para - Monitor
│   └── README.md                       # Agent overview
│
├── examples/                           # Production use cases
│   └── README.md                       # Examples index
│
├── research/                           # Agent research & recommendations
│   └── google-agents-final-recommendations.md
│
├── scripts/                            # Automation scripts
│   └── setup-perplexity-mcp.sh
│
├── assets/                             # Visual identity & brand
│   ├── brand-guidelines.md
│   ├── palette-one-pager.md
│   └── UX/
│
├── decisions.md                        # Tier 3: Toolkit development decisions
│
└── garbage_collection/                 # Archived/superseded files
```

---

## Three Tiers Explained

### Tier 1: Core Prompt (palette-core.md)

The final prompt. The physics of collaboration. Never changes.

- **Convergence before execution** — Force clarity, no guessing
- **Glass-box reasoning** — Every decision is traceable
- **ONE-WAY DOOR vs TWO-WAY DOOR** — Distinguish reversible from irreversible
- **Semantic blueprints** — Goal, Roles, Capabilities, Constraints, Non-goals

### Tier 2: Agents (assumptions.md)

The middle tier. Agents that test problems against solutions and build what's needed.

- **Agent archetypes** — Argy searches, Theri builds, Rex architects, Raptor debugs
- **Maturity tracking** — UNVALIDATED → WORKING → PRODUCTION
- **Empirical trust** — Agents earn autonomy through measured performance
- **Automatic demotion** — Two failures within 10 runs = demote tier

### Tier 3: Testing at Scale (decisions.md)

The testing tier. Logs what works, what doesn't, and why.

- Captures: what was decided, why, what was built, what's next
- Anyone can pick up where you left off
- Only logs what matters (no exhaustive logs)

---

## Using Palette on Your Project

1. **Create project directory**: `/home/mical/projects/your-company/`
2. **Add project-specific steering**: `.kiro/steering/product.md`, `tech.md`, `structure.md`
3. **Create project decisions.md**: Track project-specific decisions
4. **Reference Palette toolkit**: Agents use taxonomy and knowledge library
5. **Log agent performance**: Track which agents work for your domain

---

## What Makes It Different

**Not agentic AI hype.** It's a **battle-tested agent toolkit** that:
- Does the work of a team of language engineers
- Routes problems through a taxonomy to agents with proven solutions
- Agents have access to massive amounts of GTM knowledge
- When agents do good work long enough, we promote them
- Optimizes for restartability, not autonomy

---

## The Self-Improving Infrastructure

**Palette doesn't just solve problems — it learns which solutions work, then teaches itself to get better.**

- Knowledge library grows (93 → 300 → 800 questions)
- Agents evolve (UNVALIDATED → PRODUCTION)
- Cross-domain patterns emerge
- Institutional knowledge that doesn't leave when people do

**You're not building a tool. You're building a flywheel that turns experience into capability.**

---

## Getting Started

### Quick Start (5 minutes)
1. **Read GETTING_STARTED.md** — Understand Palette in 5 minutes
2. **Browse examples/** — See validated use cases
3. **Run your first agent** — Pick a problem, route to agent

### Deep Dive
1. **Read VISION.md** — Understand why Palette exists
2. **Read .kiro/steering/palette-core.md** — Understand Tier 1 rules
3. **Browse taxonomy/** — See the 105 RIUs (v1.2)
4. **Browse knowledge-library/** — See the 93 Q&A pairs
5. **Browse company-library/** — See 127 companies mapped to RIUs
6. **Read docs/** — Deep-dive guides (coming soon)

### Contributing
1. **Read CONTRIBUTING.md** — Learn how to contribute
2. **Submit use cases** — Share validated examples
3. **Report agent failures** — Help improve agent quality
4. **Propose Library entries** — Add validated solutions

---

## Contact

**Built by**: Mical Neill  
**Experience**: 7 years knowledge architecture at AWS  
**Validation**: AWS Solutions Engineering POC tools  
**Status**: Production-ready, battle-tested

---

**This is the toolkit. Projects using it live in `/fde/projects/`**
