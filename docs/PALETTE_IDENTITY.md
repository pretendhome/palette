# What Is Palette?

**Version**: 1.0
**Date**: 2026-03-26
**Status**: Living document — updated as the system evolves

---

## One Sentence

Palette is a governed intelligence system for AI adoption that routes decisions through structured knowledge, specialized agents, and human learning paths — built and validated through real enterprise enablement work.

---

## The Three Layers

Palette is not one thing. It is three tightly coupled systems that share a common ontology:

### Layer 1: Decision Intelligence (PIS)

**What it does**: Routes any AI implementation question to the right combination of internal knowledge and external services.

**Components**:
- **Taxonomy** — 121 classified problem types (RIUs) across 6 workstreams, each with reversibility classification, failure modes, and agent assignments
- **Knowledge Library** — 168 sourced entries with 466 citations, three-tier evidence bar, journey stage progression
- **Service Routing** — 40 routed RIUs with ranked external service recommendations, cost logic, and integration paths
- **Integration Recipes** — 69 service-specific recipes with auth, rate limits, code examples, and evaluation verdicts
- **People & Company Signals** — 21 active profiles, 43 tracked tools, signal quality ratings, cluster analysis

**What it replaces**: The research tax. Teams don't have to re-evaluate dozens of tools for every new use case. The PIS already knows the landscape, checks internal knowledge first, routes to external services only when they materially improve the outcome, and returns governed recommendations with citations.

### Layer 2: Machine Enablement (SDK + Agents)

**What it does**: Teaches machines how to route AI decisions the way an expert practitioner would.

**Components**:
- **12 Specialized Agents** — Resolver, Researcher, Architect, Builder, Narrator, Validator, Monitor, Debugger, Orchestrator, Business Plan, Health, Total Health — each with bounded scope and role constraints
- **SDK** — AgentBase, IntegrityGate, GraphQuery — shared execution model with pre-emit validation
- **Wire Contract** — 7 fields in, 7 fields out, fixed protocol across Python/Go/MCP/HTTP
- **Integrity Engine** — Validates that agent outputs reference real RIUs, real services, real knowledge entries
- **Health Agent** — 68 checks across 7 sections, continuous system state verification
- **Relationship Graph** — 2,013+ quads mapping every entity to every other entity for bidirectional traversal

**What it replaces**: Ad-hoc agent design. Instead of each agent being a standalone script with implicit assumptions, the SDK gives them a shared contract, validated outputs, and traceable handoffs.

### Layer 3: Human Enablement (Curriculum + Content Engine)

**What it does**: Teaches humans how to think about AI adoption — from first principles through production certification.

**Components**:
- **117 Curriculum Modules** — Each hand-crafted with learning objectives, rubric dimensions, exercises with failure modes, and certification thresholds
- **5 Constellations** — Named learning arcs (Build→Test→Ship, Clarify→Evaluate→Automate, etc.) with sequential progression
- **5 Published Learning Paths** — Paste-into-any-AI-tool exercises at 3 difficulty levels (Quick Start, Applied, Production)
- **Content Engine v2.1** — Parameterized path generation from template with quality bar, routing rules, and constellation display
- **Certification Tracks** — 5 tracks (AI Foundations, RAG Engineer, Agent Architect, AI Governance, AI Operations) with portfolio-based assessment

**What it replaces**: Generic training. Instead of "watch a video and take a quiz," learners build real artifacts that are evaluated against rubrics by both AI and human calibrators.

---

## How the Three Layers Connect

The ontology is the binding layer. All three systems share:

1. **The same taxonomy** — A knowledge library entry (Layer 1) maps to the same RIU that a curriculum module (Layer 3) teaches and that an agent (Layer 2) routes to
2. **The same journey stages** — foundation → retrieval → orchestration → specialization, encoded in taxonomy, knowledge library, and curriculum
3. **The same governance model** — Reversibility classification, convergence protocol, and glass-box transparency apply to machine decisions, human learning, and service routing equally

This is not accidental. It means:
- When the taxonomy adds a new RIU, the knowledge library can cover it, the curriculum can teach it, and the agents can route to it
- When a human completes a learning path, the competency maps directly to the same decision domain the agents operate in
- When the system discovers a gap (a question with no matching RIU), the gap is visible across all three layers

---

## What Palette Is Not

- **Not a chatbot wrapper** — It routes problems, not prompts. The output is a governed decision, not a generated paragraph.
- **Not a single-agent system** — 12 agents with bounded roles, not one agent that tries to do everything.
- **Not generated from prompts** — The knowledge library started from 250+ real AWS enablement sessions and 20,000+ annual AI tool queries. The taxonomy was built from 12 FDE use cases and recurring real-world patterns.
- **Not a product (yet)** — It is a working system, proof-of-work, and methodology. It demonstrates architecture that could become a product.

---

## Positioning by Audience

| Audience | Lead With |
|----------|-----------|
| Technical interviewer | "I built a governed multi-agent intelligence system with 121 classified problem types, 12 specialized agents, an SDK with 146 passing tests, and a wire contract across Python and Go." |
| Engineering leader | "Palette eliminates the research tax on AI decisions by routing problems through pre-validated knowledge, ranked external services, and traceable governance — like a decision cache for the AI landscape." |
| AI/ML practitioner | "It's an ontology-driven routing system: 121 RIUs classify the problem, a knowledge library provides fast-path answers, service routing ranks external tools, and an integrity engine validates everything before it ships." |
| Educator/enablement | "Palette teaches AI adoption through hands-on building at three difficulty levels, with portfolio-based assessment and AI-augmented evaluation — the human mirror of the machine intelligence system." |
| Startup/product audience | "One agentic interface that routes any AI implementation decision to the cheapest/best service, governed and traceable." |

---

## The FDE Question

Palette started as an FDE toolkit. It is no longer one.

An FDE toolkit would be templates, research notes, and scripts for running enablement sessions. Palette has three things that push it past that:

1. **A domain model** — 121 classified problem types with routing logic, governance rules, and reversibility classification is not a toolkit. It is an ontology for AI adoption decisions.
2. **A machine-readable intelligence layer** — The SDK, wire contract, and integrity engine teach machines how to route decisions. That is not helping a human do FDE work faster. It is codifying the expert's judgment into executable logic.
3. **A pedagogical system** — The curriculum, constellations, and learning paths codify how to teach AI adoption, not just how to do it.

The honest framing: **Palette is an AI decision intelligence system that was built and validated through FDE work.** The FDE context is the proving ground — it is where the 250+ sessions, 168 knowledge entries, and 121 RIUs came from. But the architecture is domain-portable. Swap the knowledge library and retrain the taxonomy, and it works for healthcare AI adoption, fintech AI adoption, or manufacturing AI adoption.

"I built it as proof that I can ship what I advise" — that remains the strongest interview framing. What changed is the scale of what was shipped.

---

## System Health (as of 2026-03-26)

| Metric | Value |
|--------|-------|
| Taxonomy RIUs | 121 (was 117) |
| Knowledge library entries | 168 |
| Integration recipes | 69 |
| Service routing entries | 40 (80 internal_only, 40 both) |
| People profiles | 21 active |
| Company signals | 43 tools |
| Agents | 12 (9 specialized + 3 system: health, total-health, business-plan-creation) |
| SDK tests | 86 passing |
| PIS integrity tests | 60 passing |
| Enablement modules | 117 |
| Published learning paths | 5 |
| Constellations | 5 (1 complete) |
| Relationship graph quads | 2,013+ |
| Known taxonomy gaps | 0 (4 closed) |

---

*Built by Mical Neill. Architecture, orchestration, and finishing by Claude Code. Scaffolding and content by Kiro. Creative design by Codex. Research by Perplexity.*
