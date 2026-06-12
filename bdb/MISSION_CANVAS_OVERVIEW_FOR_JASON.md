# Mission Canvas — Overview for Jason Covington
**Date**: 2026-06-02

---

## Part 1: What Mission Canvas Is

Mission Canvas is a governed agent OS that runs on your machine. It sits between a professional and all their AI models — classifying every query before any model acts, governing what can leave the machine, and storing every decision as a judgment trail that compounds over time.

### The core loop:

```
User asks a question
  → CLASSIFY: 131-node taxonomy routes the problem (local, instant)
  → REASON: On-device model does initial analysis (Ollama, zero external)
  → GOVERN: Is this safe to send externally? PII check, strategy language detection
  → RESEARCH: If safe, sanitized query goes to Perplexity (citations returned)
  → SYNTHESIZE: Intent-specific model connects research to context
  → STORE: Decision logged, linked to prior decisions, judgment compounds
```

Every step is visible. Every boundary is architectural, not contractual. The user sees governance chips in real-time showing what happened at each step.

### What makes it different from every other AI product:

| Everyone else | Mission Canvas |
|---|---|
| One model behind an API | Multiple models orchestrated per query |
| Trust the prompt to be safe | Trust the architecture — socket firewall, PII sanitizer, classification gate |
| Chat history as memory | Structured ontology as memory — 131 nodes classify, 203 knowledge entries ground |
| One mode: ask a question | 6 governed intents: PROTECT, RESEARCH, DECIDE, CREATE, DIAGNOSE, REFLECT |
| Data goes to the cloud | Local by default. External only after classification + sanitization |

### What exists today (live, working):

- **missioncanvas.ai** — voice-first web interface, 6 intents, pipeline visible
- **CLI**: `palette protect`, `palette research`, `palette decide`, etc.
- **One-command install**: `curl -fsSL https://missioncanvas.ai/install.sh | bash`
- **LiteLLM integration**: local model router, BYO keys, 100+ providers
- **131 taxonomy nodes**, 203 knowledge entries, 565 citations
- **12/12 PII boundary tests**, socket firewall, append-only decision log
- **4 models in the pipeline**: Ollama (local) → Perplexity (research) → Mistral/Claude (synthesis) → Rime (voice)
- **MIT license**, open source: github.com/pretendhome/palette

---

## Part 2: BDB Positioning (Perplexity Billion Dollar Build)

**The competition**: Perplexity's startup competition. Build with Perplexity Computer, demonstrate a $1B opportunity. Deadline: June 2, 2026 11:59pm PT. Winner gets investment from Perplexity Fund.

### Our submission angle:

> Mission Canvas is the governed agent OS for sensitive professional work. Perplexity is the governed research layer — the bridge between local safety and global knowledge.

**Why this wins BDB specifically**: Most submissions are "I used Computer to build a thing" (one-time use) or "I integrated Sonar into my app" (API wrapper). Mission Canvas makes Perplexity architecturally load-bearing — the OS literally cannot function at full capacity without it. The taxonomy classifies, the sanitizer strips, Perplexity fills the knowledge gaps, the OS integrates and compounds.

### The demo (2 minutes):

1. **PROTECT**: Ask a privileged strategy question → BLOCKED. Zero data leaves. Ollama answers locally.
2. **RESEARCH**: Ask a public legal question → classified, sanitized, routed to Perplexity, synthesized with citations. Four models. None know the client.
3. **DECIDE/REFLECT**: Switch intents → different models fire, different governance behavior. The pipeline is visible.
4. **Close**: "Four AI models worked this case. None of them know the client exists."

### Key lines:

- "Legal is the two-minute proof case, not the company boundary."
- "The same pattern applies anywhere the useful context is also the dangerous context."
- "HermesOS makes agents easy to run. Mission Canvas makes agents safe to trust."

---

## Part 3: Go-Forward Positioning

Jason's framework is right: vertical-first, outcome-led, services-to-product. Here's how Mission Canvas maps to it:

### Where Jason's doc and Mission Canvas converge:

| Jason's framework | Mission Canvas reality |
|---|---|
| "What expensive problem are we solving?" | Regulated professionals can't use AI on their most valuable work because the data can't touch the cloud |
| "What can we do that competitors cannot easily replicate?" | Ontology-as-memory — 131-node taxonomy + evidence-tiered knowledge library + append-only decisions + governed boundary. Built over 4 months with 5 AI agents. |
| "Select a vertical market" | Law first (privilege makes the boundary obvious in 2 minutes). Then medical, finance, accounting, startup GTM. |
| "Lead with outcomes, not architecture" | "Four models worked this case. None know the client." |
| "Services-led revenue model" | Assessment → Pilot → Implementation with domain ontology integration (e.g., Access Innovations medical taxonomy) |

### The vertical strategy:

**Wedge: Law** — $350B US market, 1.3M lawyers, 450K firms. Heppner ruling (Feb 2026) made it concrete: uncontrolled AI use can waive attorney-client privilege.

**Expansion**: Same architecture, different domain packs:

| Vertical | Sensitive context | What Mission Canvas does |
|---|---|---|
| Legal | Client strategy, case facts | Block strategy locally, research public law externally |
| Medical | Patient data, treatment plans | Keep PHI on-device, research public protocols externally |
| Finance | Portfolio data, MNPI | Separate public market research from private facts |
| Aerospace | Program data, classified info | Governed workflows with clearance boundaries |
| Enterprise PMO | Board strategy, financial projections | Decision trail with reversibility checks |

### The moat:

1. **Ontology-as-memory** — switching costs become infinite. The judgment trail is the lock-in.
2. **Multi-model governance** — nobody else runs multiple models per query with classification checkpoints between each step.
3. **Domain packs** — partner with taxonomy companies (Access Innovations has 70+ built) to seed vertical knowledge.

### Revenue model (aligns with Jason's services-led approach):

| Phase | What | Price range |
|---|---|---|
| Assessment | Map client's workflows to Mission Canvas intents | $15K-$30K |
| Pilot | Deploy with one domain pack, 5-10 users | $30K-$75K |
| Production | Full deployment + custom domain ontology | $75K-$250K |
| SaaS (later) | $99-$499/seat/month for self-service | After PMF |

### Partnership strategy:

- **Access Innovations** — 70+ domain taxonomies. They have the ontologies, we have the OS. Active conversation, NDA pending.
- **LiteLLM** — local model router, open source, no vendor lock-in
- **Perplexity** — governed external research layer (BDB relationship)
- **Rime** — voice/TTS for the voice-first interface

### What's NOT the play:

- Generic "AI for everyone" platform (Jason's doc is right — this loses)
- Competing with Hermes/OpenClaw on agent autonomy (they optimize for autonomy, we optimize for governance)
- Building a model (we route models, we don't train them)
- Enterprise sales before PMF (services first, product later)

---

## The One-Sentence Version

**For Jason**: Mission Canvas is the governed agent OS that makes AI safe for the work that matters most — and the judgment trail it builds becomes the reason nobody switches.
