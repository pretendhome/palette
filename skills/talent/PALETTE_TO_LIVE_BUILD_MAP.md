# Palette → Live Build Map
## How every piece of Palette contributes to SKILL-TAL-006 (Live Build Assessment)
## The question: for each component, how does THIS help Mical pass a 2.5-hour live coding interview?

---

## The Principle

The live build interview tests whether you can solve an engineering problem end-to-end in real time. Palette is not a demo you show — it is the machine you use to solve the problem. Every component either:
- **Accelerates the build** (you don't start from zero)
- **Improves the output** (the solution has depth competitors can't match)
- **Demonstrates the discipline** (the process itself is the proof)

---

## Layer 1: Core (`core/`)

### `palette-core.md` — Tier 1 Governance Rules
**Contribution to live build**: The glass-box principle. When you build in the interview, every decision is traceable — you explain WHY you chose this architecture, not just WHAT you built. The one-way-door classification means you naturally pause at irreversible decisions and name them. Interviewers see engineering maturity, not just coding speed.

**In the 2.5 hours**: When you make an architecture choice, say out loud: "This is a two-way door — I can change it later" or "This is a one-way door — let me explain why I'm committing to this." That language comes from core. It signals senior judgment.

### `assumptions.md` — Tier 2 Working Assumptions
**Contribution**: When the interviewer gives you an ambiguous prompt, you don't freeze — you state your assumptions explicitly before building. "I'm assuming X, Y, Z. If any of those are wrong, the architecture changes here." This comes from the assumptions discipline.

### `decisions.md` — Tier 3 Execution Log
**Contribution**: You narrate decisions as you make them. This IS the interview. The decision log discipline means you naturally think in terms of "I decided X because Y, the alternative was Z, I chose this because of tradeoff W." That narration is what scores highest in live builds.

---

## Layer 2: Taxonomy (`taxonomy/releases/v1.3/`)

### 121 RIUs — Problem Classification
**Contribution to live build**: Before you write a line of code, you classify the problem. "This is a retrieval problem with a governance constraint" or "This is an orchestration problem with a client-facing demo component." The taxonomy gives you a vocabulary for problem decomposition that no other candidate has.

**In the 2.5 hours**: Minute 1-5: "Let me classify this. The core challenge is [X], which means the architecture needs [Y]." You've been classifying problems against 121 categories for months. That pattern-matching is instant.

### Journey Stages (foundation, retrieval, orchestration, specialization)
**Contribution**: You know which problems are foundational (solve first) vs specialized (solve last). This drives your build order. Foundation work in the first 30 minutes, retrieval/orchestration in the middle, specialization if time allows. The journey stages ARE a project plan.

---

## Layer 3: Knowledge Library (`knowledge-library/v1.4/`)

### 176 Sourced Entries with 565 Citations
**Contribution to live build**: When you need to make an architecture decision during the build — "should I use hybrid retrieval or pure vector?" — you already know the answer because you've catalogued 176 decisions with evidence. You don't google it. You don't guess. You cite.

**In the 2.5 hours**: "I'm choosing hybrid retrieval here because in my experience, pure vector search misses exact policy lookups. I documented this when building retrieval systems across 47 providers." The knowledge library is internalized expertise that surfaces as confident, evidence-backed decisions under time pressure.

### Evidence Bar (Tier 1/2/3 Sources)
**Contribution**: When you make a claim during the build, it's sourced. "This approach is recommended by [Anthropic/Google/AWS docs]" vs "I think this might work." The evidence bar makes you credible under scrutiny.

---

## Layer 4: Agents (`agents/`)

### Resolver (731 lines, Python)
**Contribution to live build**: You know how to build a classifier from scratch. Input → classify → route. The resolver pattern is the front door of any agentic system. If the prompt is "build a multi-agent system," you start with the resolver pattern because you've built one.

**In the 2.5 hours**: "The first thing I need is intake classification. I'm going to build a lightweight resolver that maps the input to the right processing path." Then you build it — because you've built one before.

### Researcher (983 lines, Python — Perplexity backend)
**Contribution**: You know how to wire an LLM to external search with structured output. The researcher pattern (query → backend selection → findings with confidence → gap identification) is reusable in any RAG system. You can build a research component in 20 minutes because you've built one at 983 lines.

**In the 2.5 hours**: If the prompt involves research or retrieval, you scaffold the researcher pattern: query classification → backend call → structured findings → confidence scoring. The code structure is in your muscle memory.

### Architect (380 lines)
**Contribution**: You know how to decompose a problem into components with tradeoff analysis. The architect agent's pattern — compare 2+ response shapes before committing, produce a thesis not just a structure — is how you THINK during the build.

### Builder (353 lines)
**Contribution**: You know how to implement within a bounded spec. The builder agent only builds what the architect approved. In the live build, this discipline prevents scope creep — you build what the prompt asked, not what's interesting.

### Validator (378 lines)
**Contribution**: You add validation AS you build, not after. Every component gets a check. The validator pattern (requirement coverage → product depth → adversarial questions) runs in your head during the build.

### Debugger (378 lines Python + Go)
**Contribution**: When something breaks in the live build (and it will), you debug methodically — not by random changes. The debugger pattern: hypothesize → test → verify → fix narrowest issue first. The interviewers watch HOW you debug.

### Narrator (372 lines)
**Contribution**: You can explain what you built. The narrator discipline — structure for the first 60 seconds, evidence over claims, audience-appropriate language — is how you present at the end of the 2.5 hours.

### Health Agent (753 lines, 81 checks)
**Contribution**: You build self-checking systems. During the live build, you add at least one health check or assertion. "Let me add a quick check that this component is working before I move on." This signals production thinking, not demo thinking.

### Total Health (1115 lines, 107 cross-layer checks)
**Contribution**: You think about cross-layer integrity. "Does the retrieval layer's output schema match what the generation layer expects?" That kind of cross-component thinking is what separates senior from mid-level.

### Orchestrator (Go, design spec)
**Contribution**: You know how to route work between components. The orchestrator pattern — receive task, select agent, dispatch, collect result, route next — is the backbone of any multi-agent system you'd build in 2.5 hours.

### Monitor (Python + Go)
**Contribution**: You think about observability from the start. "I'm going to add logging here so we can see what the system retrieved and why it made this decision." Production engineers add monitoring. Demo builders don't.

---

## Layer 5: Buy-vs-Build (`buy-vs-build/`)

### 75 Integration Recipes
**Contribution to live build**: When you need to choose a tool — "should I use Pinecone or Chroma? LangChain or build my own?" — you have 75 evaluated recipes with tradeoff analysis. You make the decision in 30 seconds with reasoning, not 10 minutes of googling.

**In the 2.5 hours**: "I'm going to use [X] here because [tradeoff]. I've evaluated the alternatives and [X] is the right choice for this use case because [reason]." That's 75 recipes of internalized buy-vs-build thinking.

### Service Routing (40 routed RIUs)
**Contribution**: You know which problems to solve internally vs delegate to an API. In the live build, you don't build everything from scratch — you use the right external service where it's faster and explain why.

### Company Index (127 companies)
**Contribution**: You know the landscape. If the prompt involves a specific domain, you can reference real companies, their approaches, and their limitations. "This is similar to how [company] approaches [problem], but for [this client] we'd want [different tradeoff]."

### People Library (21 profiles)
**Contribution**: You can reference real practitioners and their approaches. "Harrison Chase's pattern for stateful agent workflows is relevant here" — shows you're embedded in the community, not just building in isolation.

---

## Layer 6: Skills (`skills/`)

### Talent Skills (interview prep, takehome execution, live build execution, enablement test)
**Contribution**: The live build skill (SKILL-TAL-006) itself — the execution protocol, the time budget, the communication protocol, the anti-conservatism rules. But also: every other skill you've built proves you can codify methodology into reusable frameworks. That IS what the Perficient incubator wants.

### Retail-AI, Education, Travel Skills
**Contribution**: You've applied the same architecture pattern across 4 different domains. In the live build, you can say: "I've used this retrieval + governance + measurement pattern for retail business planning, adaptive learning, travel planning, and interview preparation. The domain changes, the architecture doesn't." That's reusable framework thinking — exactly what the incubator JD asks for.

### Enablement Skill (SKILL-TAL-005)
**Contribution**: The module library (system architecture, knowledge map, measurement framework, day-1 artifacts, interactive components) is reusable in ANY build. The measurement framework alone — activity → behavior → outcome — applies to whatever you build in 2.5 hours.

---

## Infrastructure Layer

### Peers Bus (Node.js, localhost:7899, SQLite)
**Contribution to live build**: You've built a real-time message bus with governed communication between agents. If the prompt involves multi-agent coordination, you can describe (and potentially demo) how agents communicate through typed envelopes with validation, threading, and delivery tracking.

**In the 2.5 hours**: The bus architecture is a reference design. Even if you don't run it, you can sketch the pattern: "Agents communicate through a governed message bus. Each message has a typed envelope with sender, receiver, intent, risk level, and payload. The bus validates before delivery." That's 30 seconds of senior architectural fluency.

### Agent Memory (bounded, 2200 chars, SQLite)
**Contribution**: You understand how to give agents persistent memory without unbounded state. "Memory is bounded to 2200 characters per agent, which forces curation instead of hoarding." This is a production design decision, not a demo choice.

### Agent Skills (procedural memory, per-agent)
**Contribution**: You understand how agents learn from experience. "After completing a complex task, the agent can save the procedure as a reusable skill." This is the Hermes insight — and it's the difference between a system that starts from scratch every time and one that compounds.

### FTS5 Search (message search index)
**Contribution**: You built full-text search into the bus. If the prompt involves search, you can reference this: "I added FTS5 indexing so messages are searchable across the full history. Same pattern applies to any document retrieval system."

### SDK (`sdk/`)
**Contribution**: You built an SDK with base classes, integrity gates, and graph queries. 86 tests. This shows you think about developer experience and reusability, not just one-off scripts.

---

## Voice Layer

### Voice Hub (5 LLMs, 4 languages, Rime TTS, Whisper STT)
**Contribution to live build**: If the prompt involves voice, you've built it. Sub-700ms first-audio latency, sentence-boundary streaming, multi-model routing through the taxonomy. But even if it doesn't involve voice: the voice hub demonstrates that you can build real-time, low-latency systems that work across languages.

### Voice Evaluation Workbench (4 languages, 5 dimensions)
**Contribution**: You've built evaluation tooling. The workbench pattern (structured rubric → multi-dimension scoring → exportable results) applies to any evaluation system you'd build in the interview.

---

## Mission Canvas

### Convergence Engine (3 modes, deterministic routing, 198 tests)
**Contribution to live build**: MissionCanvas is a working web application with a convergence protocol — explore → converge → commit. If the prompt involves a user-facing system, the MissionCanvas architecture (Node.js server + client-side state + deterministic routing + workspace management) is a reference design you can scaffold from.

### 198 Stress Tests
**Contribution**: You know how to write comprehensive tests. During the live build, you add at least one test. "Let me add a quick test that this retrieval path returns the right result." 198 tests across 4 suites shows this is habit, not performance.

---

## Lenses (28)

### Role Lenses (22)
**Contribution to live build**: If you need to think from a specific perspective during the build — "how would a product manager evaluate this?" or "how would a security engineer review this?" — the lenses give you structured thinking from 22 different roles. This is how you catch your own blind spots in real time.

### Person Lenses (Mical, Claudia, Steph Ango)
**Contribution**: The person lens methodology itself is demonstrable. "I built a structured portrait system that captures capabilities, contradictions, and evidence for real people." This shows human-centered systems thinking.

### Interviewer Lenses (Antun, Jenn, etc.)
**Contribution**: You've built lenses for the people evaluating you. Meta-level systems thinking. If the prompt involves user research or stakeholder analysis, the lens methodology is directly applicable.

---

## Governance Pipeline

### Proposals → Votes → Promotion
**Contribution to live build**: You've built a governance system with quality gates. If the prompt involves any kind of review, approval, or trust system, you can scaffold from the governance pipeline: propose → review → vote → promote. The 5-layer architecture (propose, review, vote, promote, bridge feedback) is a reusable pattern for any system with human-in-the-loop quality control.

---

## Wiki System

### Deterministic Compiler + Validator (337 pages, 8/8 validation)
**Contribution**: You've built a documentation system that compiles from structured data and validates its own integrity. If the prompt involves knowledge management or documentation, this is a working reference.

---

## Portfolio Generator

### YAML → HTML Generator (5 templates)
**Contribution to live build**: If you need to build a demo UI in the interview, the portfolio generator pattern (structured data → templated HTML) is the fastest path. You've done it before. 30-60 minutes from config to page.

---

## What This Means for the 2.5-Hour Build

The interview prompt will be some variant of: "Build an agentic AI system that solves [business problem]."

Here is what you bring that no other candidate does:

| Time | What You Do | Which Palette Component Drives It |
|------|-------------|----------------------------------|
| 0:00-0:05 | Classify the problem | **Resolver pattern + Taxonomy** — instant problem decomposition |
| 0:05-0:10 | State assumptions, sketch architecture | **Core governance + Architect agent** — traceable decisions, 2+ shapes compared |
| 0:10-0:30 | Build the skeleton (input → classify → process → output) | **Resolver + Orchestrator pattern** — you've built this exact flow |
| 0:30-1:00 | Build the core complexity (retrieval, agents, or pipeline) | **Researcher + Knowledge Library** — you know retrieval failure modes, evidence tiers, multi-backend routing |
| 1:00-1:30 | Add evaluation and governance | **Validator + Health Agent + Governance Pipeline** — evaluation as control plane, not afterthought |
| 1:30-2:00 | Add business layer, clean up, demo-ready | **Narrator + Skills (reusable frameworks)** — business framing, measurement, who uses this and why |
| 2:00-2:15 | Run the demo | **MissionCanvas pattern** — working end-to-end, tested |
| 2:15-2:30 | Present: what you built, tradeoffs, what's next | **Narrator + Core decisions discipline** — structured walk-through, honest about gaps |

**The meta-insight**: You're not building from scratch in 2.5 hours. You're assembling from patterns you've built, tested, and validated across 12 agents, 121 problem categories, 176 knowledge entries, 75 integration recipes, 6 skill domains, and 198 stress tests. The live build is Palette applied to whatever problem they give you.

**The sentence for the interview**: "I don't start from zero. I start from patterns I've validated across multiple domains — classification, retrieval, orchestration, governance, measurement. The domain changes. The discipline doesn't."
