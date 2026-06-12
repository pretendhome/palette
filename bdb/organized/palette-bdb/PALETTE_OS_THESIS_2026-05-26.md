# Palette — The Operating System for Professional Judgment
## BDB Thesis Document v1 — For Crew Review
**Date**: 2026-05-26
**Author**: claude.analysis (synthesizing operator vision + crew reviews + conference intelligence)
**Status**: DRAFT — send to crew for iteration
**Tag**: BDB-THESIS-V1

---

## What We Are Building

Palette is an operating system for professionals who work with AI.

It is not an AI assistant. It is not a chatbot. It is not a harness that wraps one tool. It is the layer that sits between a professional and ALL their AI tools — governing what each tool sees, classifying problems before any model acts, and storing decisions as structured memory so every future interaction gets smarter.

### The Origin

The original concept came from waiting tables. Go to the kitchen, go to the tables, go to the bar — in order — and do what needs doing at each station. Don't wait for orders to come to you. Be proactive. Classify the work before doing it. That's the waiter's OS.

Palette applies the same logic to professional knowledge work with AI:
- **Classify** the problem before any model touches it (taxonomy)
- **Retrieve** the right prior knowledge and decisions (ontology-shaped memory)
- **Govern** what data flows to which tool (trust boundaries)
- **Store** the result as structured memory (compounding judgment trail)
- **Route** to the next station (convergence toward resolution)

The loop runs: problem → classification → knowledge → governed work → decision → updated memory → better next problem. It runs until the real solution emerges. It doesn't reset between sessions.

### Why It's an OS, Not an App

A traditional OS manages: processes, memory, file system, permissions, I/O.

Palette manages:
- **Intent** (taxonomy — 121 classified problem types)
- **Memory** (ontology-shaped knowledge library — 183 entries, 565 citations, evidence-tiered)
- **Artifacts** (decisions, briefs, action plans — append-only, traceable)
- **Permissions** (governance tiers, PII boundaries, ONE-WAY/TWO-WAY door classification)
- **I/O** (which tool sees what, what flows in, what flows out, what stays local)

It doesn't replace Claude Code, Codex, Gemini, Mistral, Perplexity, or any other AI tool. It's what they run inside of. Just like Linux doesn't replace your applications — it's what they run on.

### What It Does That Nobody Else Does

1. **Classifies before acting.** Every query is routed through the taxonomy before any model generates. This reduces inference (the model gets the right context, not everything), increases accuracy (retrieval is targeted, not fuzzy), and enables governance (the system knows what KIND of problem it's dealing with before deciding what to do).

2. **Governs data flow across tools.** Claude, Perplexity, GPT, Ollama — Palette governs what each tool sees. PII never reaches external services. The sanitization gate is not a filter bolted on afterward — it's the architecture. The NOMA Security framework (AI Council, May 2026) defines 5 trust boundaries for agentic systems. Palette implements all 5.

3. **Stores judgment as ontology, not chat.** Memory is not conversation history. Memory is classified decisions, evidence-tiered knowledge, routing patterns, and governance states. A user may ask the same problem ten different ways. Chat history sees ten prompts. Palette's ontology sees one recurring problem class with evolving evidence and decisions.

4. **Works without ever connecting to external inference.** The floor is NVIDIA open-weight models running locally via Ollama. Zero API keys. Zero data leaves the machine. Zero cost. When the user WANTS external intelligence — Perplexity for research, Claude for synthesis, GPT for analysis — they connect their own accounts. Palette governs the boundary. The OS manages the resources; it doesn't own them.

5. **Enables agent self-awareness through structured comparison.** Multiple agents (Claude, Kiro, Codex, Gemini, Mistral) work through the same taxonomy, the same knowledge library, the same governance tiers. Because the workflow is normalized, agents can compare their outputs on the same classified problem. Self-awareness requires comparison to like entities — the ontology makes the comparison meaningful.

6. **Reduces inference cost structurally.** Taxonomy-first classification is a compression function. Instead of cramming everything into a 128K context window (NOMA: "the context window cram hole"), Palette classifies first, retrieves only what's relevant, and sends governed context to the model. Fewer tokens. Better answers. Cheaper.

7. **Compounds across sessions, surfaces, and tools.** A decision made via voice compounds when the same problem appears in CLI. A precedent researched via Perplexity compounds when a related question is answered locally. The judgment trail is surface-agnostic and tool-agnostic. That's OS behavior.

---

## The Architecture

### Three Tiers of Inference

```
TIER 1: ON-DEVICE (zero external connection)
  NVIDIA open-weight models via Ollama
  Classification, retrieval, basic reasoning
  Free forever. Works offline. Works airgapped.
  Gets better with every NVIDIA release.

TIER 2: FREE CLOUD BACKUP (Groq)
  Groq Llama 3.3 70B (free tier, 1000 RPD)
  Faster than local, still free
  No PII ever sent

TIER 3: CONNECTED ACCOUNTS (user opt-in)
  "Connect your Claude account"
  "Connect your Perplexity account"
  "Connect your OpenAI account"
  User's own subscription, user's own terms
  Palette governs what flows — PII never leaves
```

### Five Trust Boundaries (mapped to NOMA/OWASP framework)

| Boundary | Risk It Prevents | Palette Implementation |
|----------|-----------------|----------------------|
| **INSTRUCTION** | Prompt Injection & Context Poisoning | Taxonomy-first classification — classify intent BEFORE any model acts |
| **KNOWLEDGE** | Data Integrity Compromise | Evidence-tiered knowledge library — 183 entries, 565 citations, integrity checks |
| **RETRIEVAL** | Wrong or Unauthorized Content | Hybrid retrieval (FTS5 + vectors + keyword) + PII sanitization + authority ranking |
| **MEMORY** | Persistent Malicious State | Append-only decisions, bounded memory per agent, sanitization on write |
| **ACTION** | Uncontrolled Real-World Consequences | ONE-WAY DOOR gates, human-in-the-loop checkpoints, execution logging, gateway blocking |

Plus: **IDENTITY GOVERNANCE** at every boundary — agent trust tiers (UNVALIDATED → WORKING → PRODUCTION), per-agent identity on the bus, credential scoping.

### The Ontology Layer (What Nobody Else Has)

The 121-node RIU taxonomy is the routing table for professional judgment. It is NOT a feature list or a tag system. It is:

- **The compression function** — turns "search everything" into "search the right thing"
- **The normalization layer** — all agents speak the same problem language
- **The memory backbone** — decisions are stored by problem type, not by session
- **The convergence mechanism** — the loop runs problem → classification → knowledge → decision → updated memory → better next problem until resolution
- **The self-awareness substrate** — agents compare outputs on the same classified problem

The knowledge library (183 entries, 565 citations, evidence-tiered) is the grounded content that the ontology routes to. Together, taxonomy + knowledge library = reusable judgment, not disposable chat.

---

## Who It's For

### Primary: The Professional Who Works With AI Every Day

Not the developer building AI apps. Not the enterprise buying AI SaaS. The professional — lawyer, doctor, accountant, consultant, educator, analyst — who uses Claude, Perplexity, GPT, and local models as part of their daily workflow and needs:

- **Governance**: their client data can't touch the cloud without explicit control
- **Memory**: today's work should make tomorrow's work better, not start from zero
- **Routing**: different problems need different tools, and the system should know which
- **Judgment trail**: what was decided, why, based on what evidence — traceable and portable

### The Wedge: Regulated Professionals

25 million regulated professionals — lawyers, doctors, accountants, financial advisors, therapists — have a STRUCTURAL need for governed AI. Attorney-client privilege, HIPAA, fiduciary duty make cloud AI a malpractice risk. They're already buying Mac Minis and duct-taping open-weight models. Nobody sells them the governed version.

Legal is the first vertical. Same architecture, different knowledge packs for medical, financial, accounting, education.

### The Expansion: Every Knowledge Worker

The trajectory of the industry (tab → multiline → agents → subagents → swarms → continuous) means every knowledge worker will be orchestrating multiple AI tools within 2 years. They'll all need what regulated professionals need first: governance, memory, routing, judgment trails. Palette starts where the pain is sharpest (regulated) and expands where the trajectory leads (everyone).

---

## What Exists Today (Honest Assessment)

### Working and Tested
- 121 RIU taxonomy (classification before action)
- 183 knowledge library entries with 565 citations (evidence-tiered)
- Hybrid retrieval at 95% recall@5 (FTS5 + vectors + keyword with RRF)
- Governed Perplexity gateway with PII sanitization (12/12 tests)
- `palette query` CLI with 5-step pipeline (resolve → retrieve → route → respond → extract)
- Voice Hub (browser-based, multi-language, multi-agent, Rime TTS)
- Mission Canvas (web UI with convergence chain, workspaces, OWD gates)
- Peers bus (governed multi-agent messaging, FTS5 search, skill storage)
- Append-only decision history with compounding signals
- 13 agents with trust tiers and voice identity (tessitura)
- 61/61 tests passing, 84/85 health checks
- Ollama local inference (Qwen 2.5 7B) + Groq free tier (Llama 3.3 70B)

### UX Gaps (Honest)
- **No one-click installer.** Requires Python, Node.js, env vars. Adam and Claudia both needed Founder to set it up.
- **No onboarding wizard.** System arrives empty. No "what domain are you in?" No starter pack.
- **API key complexity.** 7+ keys for full multi-model. Mitigated by Tier 1 (zero keys needed for local).
- **Local model download.** Ollama models are 4-8GB. First run takes 10+ minutes.
- **No desktop app.** Voice Hub and Mission Canvas are web-based (good), but CLI is terminal-only.
- **Legal domain knowledge is thin.** 8 demo entries. Real legal user would exhaust it in one session.
- **No "connect your accounts" UI.** Architecture supports it (env vars). UX doesn't exist yet.

### What $1M Buys
1. **Packaging**: Docker/installer, onboarding wizard, domain pack selection, desktop app wrapper
2. **NVIDIA integration**: Default to Nemotron Nano on-device, optimize for Apple Silicon + NVIDIA GPU
3. **Account connection UX**: "Connect your Claude" / "Connect your Perplexity" — one-click OAuth
4. **Domain packs**: Legal starter (30+ entries), medical starter, financial starter
5. **Team of 2-3 engineers**: Backend (retrieval + governance + packaging) + frontend (desktop + onboarding)
6. **10 pilot firms**: White-glove setup, weekly iteration, real feedback loop

---

## For the BDB Competition Specifically

### The Thesis
Palette is the operating system for professional judgment. It classifies before it acts, governs what flows where, stores decisions as structured memory, and compounds over time. It works offline with open-weight models. It works with any cloud AI — governed. The tools come and go. The judgment stays.

### Why It's a $1B Opportunity
- **25M regulated professionals** need governed AI today (legal, medical, financial, accounting, therapy)
- **Every knowledge worker** will need it within 2 years as multi-agent workflows become standard
- **The industry is defining the architecture** (NOMA trust boundaries, OWASP Agentic Top 10, Redis context engines) but nobody has built the professional-facing OS
- **Legora ($5.5B) and Harvey ($11B)** prove the legal AI market alone supports massive valuations — and they're cloud-only, single-vertical, automation-focused. Palette is local-first, multi-vertical, augmentation-focused.

### Why Perplexity Computer Is Core
- Tier 3 external research runs through Perplexity — the governed window to public knowledge
- Computer originated the gateway architecture (recorded session)
- Computer supplied the legal domain research for the demo
- Computer validated the market thesis (on-prem AI for regulated professionals)
- Perplexity is not the product. Perplexity is the product's external intelligence layer — governed by the OS.

### The Demo (2 minutes)
Show the OS behavior: classify → govern → retrieve → compound.
- **Interaction 1**: Public research via Perplexity (governed, sanitized, stored)
- **Interaction 2**: Client-specific query BLOCKED (PII detected, zero data leaves)
- **Interaction 3**: Compounding follow-up (system connects to prior decisions — the hero moment)

Cold open with the problem. Close with: "Your judgment compounds here. The tools come and go. The judgment stays."

---

## Questions for the Crew

This document is the v1 thesis. Before we start building the demo around it, I need each agent to answer:

1. **Does "OS for professional judgment" land better than "SDK for Humans" as the public-facing thesis?** Both are true. Which one should a judge hear in 2 minutes?

2. **Is the three-tier model strategy (NVIDIA local → Groq free → connected accounts) the right architecture to present?** Or does it introduce too much complexity for the submission?

3. **Should the demo show one surface or two?** Voice Hub + CLI proves it's an OS (same intelligence, different surface). CLI-only is simpler but looks like a developer tool.

4. **What's the single strongest sentence for this thesis?** Not the tagline ("your judgment compounds here"). The product sentence. My current best: "Palette is the operating system that governs how professionals work with AI — classifying before acting, protecting data by architecture, and compounding judgment over time."

5. **What should we CUT from this document before it becomes the submission?** It's too long for the competition. What's essential, what's supporting, what's noise?

---

*Draft by claude.analysis. Synthesizing: operator origin story (waiter metaphor, Kaizen framework), crew fresh-eyes reviews (Kiro, Codex, Gemini, Mistral), AI Council conference intelligence (NOMA trust boundaries, Redis context engine, AIIQ model landscape, OWASP Agentic Top 10), competitive landscape research (Legora aOS, Harvey AI, Google Antigravity 2.0, MindStudio). 2026-05-26.*
