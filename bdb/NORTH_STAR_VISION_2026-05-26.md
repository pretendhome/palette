# Palette — North Star Vision
## The Operating System for Professional Judgment
**Date**: 2026-05-26
**Status**: LOCKED VISION — all execution flows from this document
**Sources**: 5 crew agents + Perplexity Computer competitive analysis + AI Council conference intelligence + operator vision
**Tag**: BDB-NORTH-STAR

---

## The Vision in One Paragraph

In February 2026, a federal court ruled that using a cloud AI tool on privileged material waives attorney-client privilege. 1.3 million lawyers — and 25 million regulated professionals behind them — now have a structural need for AI that never sends their data to someone else's server. Palette is the operating system that solves this: it runs on your machine, classifies every problem before any model acts, governs what each AI tool can see, and stores your decisions as structured memory that compounds over time. The tools come and go. The judgment stays.

---

## What Palette IS

Palette is the governance and intelligence layer between a professional and all their AI tools.

It is not a chatbot. It is not a legal AI product. It is not a harness that wraps one tool. It is the OS that manages how a professional uses Claude, Perplexity, GPT, Gemini, local models — any of them, all of them — while ensuring:

1. **Problems are classified before any model acts** (taxonomy-first — 121 RIU nodes, expandable to any domain)
2. **Data flows are governed by architecture, not by contract** (PII never leaves the machine — privilege preserved by design)
3. **Decisions compound as structured memory** (not chat history — classified decisions with rationale, evidence, and provenance)
4. **The system works without any external connection** (NVIDIA/Ollama local models as the floor — free, airgapped, always available)
5. **External intelligence is a governed window, not a dependency** (connect your own Claude/Perplexity/GPT accounts — Palette governs what they see)

### The OS Primitives

| Traditional OS | Palette |
|---|---|
| Processes | Intent classification (taxonomy routes problems before models act) |
| Memory | Ontology-shaped knowledge (183 entries, 565 citations, evidence-tiered) + append-only decision history |
| File System | Portable local artifacts (YAML decisions, knowledge packs, judgment trails) |
| Permissions | Governance tiers (ONE-WAY/TWO-WAY doors) + PII boundary + agent trust tiers |
| I/O | Governed tool routing (what each model sees, what stays local, what flows out) |

This table converts "OS" from metaphor to mechanism. It is the most important asset in the submission.

---

## Why NOW

### The Market-Making Event

**United States v. Heppner** (SDNY, Feb 2026): Judge Rakoff held that using a public AI tool voids attorney-client privilege. "Not remotely any basis for any claim of attorney-client privilege." The court left one question open: would the outcome differ if the AI expressly preserved confidentiality?

**Palette is the architectural answer to that question.** When AI runs on-device and data never traverses a third-party server, there is no ToS to disclaim confidentiality. Privilege is preserved by architecture.

### The Regulatory Tailwind

- **HIPAA 2026**: All "addressable" safeguards now mandatory. Audit logging required for every AI interaction involving PHI. AI-specific risk assessments required.
- **EU AI Act**: Full enforcement August 2, 2026. High-risk AI systems (medical, legal, HR) require conformity assessments.
- **55% of enterprises** avoid GenAI use cases due to security concerns (VMware 2026).
- **AI governance market**: $429M → $4.2B by 2033 (CAGR 38.5%).

### The Hardware Convergence

Three independent trajectories validated local-first AI in H1 2026:
- **NVIDIA**: Nemotron 3 Nano Omni — 30B params, runs on 25GB RAM. Open-weight, commercial use.
- **Apple**: Mac Mini M4 at $599 runs 13B models. A governed AI runtime for the cost of an office chair.
- **Qualcomm**: Snapdragon X2 NPU — 4B-7B models fully on-chip, zero GPU required. Mainstream Windows path.

Palette was designed for this world before the hardware confirmed it.

### The Category Validation

- **YC Summer 2026 RFS**: Explicitly asks for "the AI Operating System for Companies"
- **a16z SR006** (May 2026): "The strategic question shifts from who has intelligence to who has embedded operational context: the memory, workflows, governance structures, and historical decisions." — This is Palette's architecture described by a16z without knowing Palette exists.
- **Legora aOS**: $5.5B implied valuation, "agentic operating system for legal work" — validates the category, but cloud-only. Cannot solve the Heppner problem.
- **Harvey AI**: $11B, legal SaaS — proves the legal vertical funds at scale.

The category is real. The vocabulary is validated. The intersection (local-first + multi-model + multi-vertical + compounding) is unoccupied.

---

## Who It's For

**The regulated professional who already uses AI and knows the risk.**

Not a TAM slide. A person:
- Solo or small-firm attorney who pastes client details into Claude and feels guilty
- Physician who needs to query medical literature without HIPAA exposure
- Financial advisor whose fiduciary duty makes cloud AI a liability risk
- Accountant whose client data cannot touch third-party servers

This person exists today. They're buying Mac Minis and duct-taping open-weight models. They're reading the Heppner ruling and the Baker Donelson advisory. Nobody sells them a governed solution.

**Legal is the wedge.** Same architecture, different knowledge packs for medical, financial, education. The OS is horizontal. The entry is vertical.

---

## What Exists Today

| Component | Status | Evidence |
|---|---|---|
| Taxonomy (121 RIUs) | Production | Classifies before any model acts |
| Knowledge Library (183 entries, 565 citations) | Production | Evidence-tiered, integrity-checked |
| Hybrid retrieval (FTS5 + vectors + keyword) | Production | 95% recall@5 |
| Governed Perplexity gateway | Production | 12/12 sanitization tests, PII blocking |
| CLI pipeline (resolve → retrieve → route → respond → extract) | Production | 61/61 tests passing |
| Voice Hub (browser, multi-language, multi-agent) | Production | Rime TTS, sentence-boundary streaming |
| Mission Canvas (web UI, convergence chain, workspaces) | Production | 10 API endpoints, OWD gates |
| Peers bus (governed multi-agent messaging) | Production | FTS5 search, skill storage, typed envelopes |
| Local inference (Ollama Qwen 2.5-7B) | Production | Zero API keys, zero cost, works offline |
| Free cloud backup (Groq Llama 3.3-70B) | Production | 1000 RPD free tier |
| Append-only decision history | Production | Compounding across sessions |
| 13 agents with trust tiers + voice identity | Production | Tessitura voice system (Rime Arcana v3) |
| Health checks | Production | 84/85 automated |

### What's Missing (Honest)

- **Legal domain taxonomy**: 0 legal RIU nodes. Current taxonomy covers AI/ML decisions. Must build 10-12 legal nodes before demo.
- **One-click installer**: Requires Python + Node.js + env vars today. Adam and Claudia needed help.
- **Documented professional user session**: Architecture is verified by tests. No documented real-world professional use.
- **"Connect your accounts" UX**: Architecture supports multi-model. UX for connecting Claude/GPT/Perplexity accounts doesn't exist yet.

---

## The Submission Language Stack

Use different language at different altitudes:

| Altitude | Line |
|---|---|
| **Opening hook** | "In February 2026, a federal court ruled that using Claude on privileged material waives attorney-client privilege." |
| **Product sentence (user)** | "Palette is governed AI that remembers how you think — so regulated professionals can use AI without risking their license, and every query makes the next one smarter." |
| **Product sentence (technical)** | "Palette classifies every problem before any AI acts, governs what each tool sees, and stores decisions as memory that compounds." |
| **Tagline** | "Your judgment compounds here." |
| **Category** | "The operating system for professional judgment." |
| **Investor** | "Infrastructure of judgment — compounding memory, governed tool routing, local-first architecture." |
| **Close** | "The tools come and go. The judgment stays." |

---

## The Demo (2 minutes)

### Cold Open (0:00–0:10)
> "A federal court ruled that using cloud AI on privileged material waives attorney-client privilege. 25 million professionals can't use AI without risking their license. Palette solves this."

### Interaction 1 — Public Research, Governed (0:10–0:45)
Query: Delaware fiduciary duty precedents.
Show: Classify → Sanitize (no PII) → Perplexity research → Local knowledge merge → Decision stored.
Say: "Public question. Palette sanitizes, queries Perplexity, merges with local knowledge, stores the decision."

### Interaction 2 — Client Data BLOCKED (0:45–1:15)
Query: "Should we advise Smith Corp to settle the Johnson lawsuit for $2.5M?"
Show: PII detected → BLOCKED → Local-only response → "No data left this machine."
Say: "Client-specific question. Palette detects party names, dollar amounts, strategy language. Blocks it. Zero data leaves."

### Interaction 3 — Compounding (1:15–1:45) — THE HERO MOMENT
Query: Delaware filing deadlines for fiduciary cases.
Show: `[CONNECTED TO 1 PRIOR DECISION]` — highlighted, annotated on screen.
Say: "Next day. Related question. Palette connects it to yesterday's research automatically. Your judgment compounds."

### Close (1:45–2:00)
Text on screen: **"Your judgment compounds here. The tools come and go. The judgment stays."**
3-second flash of Voice Hub — same intelligence, different surface. Proves it's an OS.

---

## The $1B Path

**Three legs:**

1. **Market**: 25M regulated professionals. 1% at $100/month = $300M ARR. Heppner ruling creates structural demand now. Governance market CAGR 38.5%.

2. **Platform**: The taxonomy is a network effect. Every professional who uses Palette contributes decision patterns that make classification more accurate. The ontology compounds. Switching costs increase with use. The longer you use it, the more of your judgment lives inside it.

3. **Pricing**: Per-governed-interaction, not per-seat. Every interaction Palette governs is value delivered. The OS model enables usage-based pricing that scales with AI adoption rather than breaking when AI reduces headcount.

**What $1M unlocks**: Packaging (Docker/installer, onboarding wizard), legal domain pack (30+ taxonomy nodes + knowledge entries), 2-3 engineers (backend + frontend), 10 pilot firms with white-glove setup.

---

## The 7-Day Execution Plan

| Day | Priority | Task | Owner |
|---|---|---|---|
| **1** (May 26) | P0 | PII scrub + commit 367 files | Founder + Kiro |
| **1** | P0 | Update MANIFEST (company_index: 12→127) | Kiro |
| **2-3** (May 27-28) | P0 | **Build legal taxonomy (10-12 RIU nodes)** | Claude + Kiro |
| **2-3** | P1 | Create BDB submission draft outline | Claude + Mistral |
| **3-4** (May 28-29) | P1 | **Document one real professional session** | Founder |
| **4** (May 29) | P1 | Add product truth to palette-core.md | Founder (approval) |
| **4-5** (May 29-30) | P1 | Draft full submission with Heppner hook | Claude + Mistral |
| **5** (May 30) | P1 | Landing page rewrite + waitlist launch | Founder |
| **5** (May 30) | P1 | Demo narration script | Claude |
| **6** (May 31) | P0 | **Record demo video** | Founder |
| **6** | P1 | README rewrite (product-first) + PII audit | Claude + Kiro |
| **6** | P1 | Push to public GitHub | Founder |
| **7** (June 1) | P0 | **Cold review + final edit + SUBMIT** | All |

---

## What This Document IS

This is the north star. Everything we build in the next 7 days serves this vision. If a task doesn't strengthen the submission against this document, it doesn't get done.

The architecture is real. The code works. The market timing is the best it has ever been. The category is forming and nobody occupies our intersection. The gap is packaging, domain content, and proof — not architecture.

The pitch is not "look at what we built." The pitch is: "A federal judge created the demand. The hardware arrived. The governance market is growing at 38.5%. I built the OS. I need a team to ship it."

---

*North Star Vision synthesized by claude.analysis from: kiro.design (fresh-eyes review + thesis response), codex.implementation (fresh-eyes review), gemini.specialist (fresh-eyes review + thesis response), mistral-vibe.builder (fresh-eyes review + thesis response + competitive synthesis), perplexity.computer (full competitive analysis with citations), operator vision (waiter metaphor, Kaizen framework, conference intelligence). 2026-05-26.*
