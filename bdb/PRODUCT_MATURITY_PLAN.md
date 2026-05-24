# Palette — Product Maturity Plan
## From Foundation to Excellence
**Date**: 2026-05-22
**Author**: claude.analysis (synthesizing Codex report, Mistral positioning, Kiro spec, person lens, founder lens)
**Thesis**: Palette is an SDK for Humans because it uses ontology as the primary form of AI memory.

---

## The Founder Lens: Mical as Builder

Before the plan, the lens — because the plan must fit the builder.

Mical's career throughline: **see structural problems invisible to domain specialists → fix the structure → watch people succeed.** Milkshakes at 16. Publishing simulation in Paris. Carabinieri in Sardinia. Italian passive voice at Alexa. Taxonomy reclassification at Pathfinder. Palette.

His process: **fast iterative discovery, not plan-then-execute.** The plan below respects this — each level produces a working artifact, not a document. Each level is testable by contact with reality. The plan converges through iteration, not through speculation.

His edge as founder: **comparative linguistics trained him to see how meaning maps across systems.** This is why ontology-as-memory is not a bolt-on thesis — it's what he's been doing for 20 years across languages, cultures, knowledge systems, and now AI. No one in the Hermes/OpenClaw space has this.

His risk as founder: **too open, too many directions, gives away credit, process looks chaotic from outside.** The plan below addresses this by locking ONE vertical (legal), ONE demo path, ONE thesis sentence. Everything else is later.

---

## Current State: Foundation (with pockets of Participation)

### What we have (Foundation level — ✅ confirmed working):

| Component | State | Evidence |
|-----------|-------|----------|
| Taxonomy (121 RIUs) | ✅ Production | Classifies before retrieval. Ontology backbone. |
| Knowledge Library (183 entries, 565 citations) | ✅ Production | Evidence-tiered, governed. AI/ML domain heavy. |
| Hybrid retrieval (FTS5 + vector + keyword) | ✅ Production | 95% recall@5. RRF fusion. |
| Governed gateway (Perplexity) | ✅ Production | 12/12 tests. PII sanitization. Blocked/allowed. Live API. |
| CLI pipeline (`palette query --external`) | ✅ Production | resolve → retrieve → route → respond → extract |
| Append-only decision history | ✅ Production | Typed, traceable, RIU-classified |
| ONE-WAY/TWO-WAY governance | ✅ Production | Risk-tiered execution |
| Multi-model routing (10 LLMs) | ✅ Production | Claude, Mistral, GPT-4o, Qwen, Perplexity ×3, Groq, Ollama, Kiro |
| Voice Hub (4 languages, Rime TTS) | ✅ Production | sub-700ms first audio, sentence-boundary streaming |
| Peers bus (governed messaging) | ✅ Production | FTS5 search, typed envelopes, skill storage schema |
| 40 skills across 10 domains | ✅ Documented | Static context, not agent-loaded at runtime |
| Session reflection (KL proposals) | ✅ Working | auto_enrich.py + session_reflect.py |
| Convergence chain (goal tracking) | ✅ Working | 50KB deterministic graph engine, within-session |
| Health checks (84/85) | ✅ Production | 9 sections, automated |
| Test suite (61 tests) | ✅ All passing | 49 V3 + 12 gateway |

### What's at Participation level (partially working):

| Component | State | Gap |
|-----------|-------|-----|
| Broker skill storage | Schema exists, unpopulated | No agent writes to it |
| Conversation search | FTS5 + vectors exist | Not exposed to agents |
| Telegram bridge | Working for 1 bot | Not generic |
| pyproject.toml | Entry point defined | No Docker, no setup wizard |
| Cross-session learning | session_reflect extracts KL | Doesn't extract skills, doesn't persist across sessions |

### What's missing entirely (not yet Foundation):

| Component | Why it matters |
|-----------|---------------|
| Downloadable installer | Nobody can use this without being Mical |
| Onboarding / domain packs | System arrives empty for new users |
| Legal-domain KL entries | Demo vertical has no pre-built knowledge |
| Local web UI | Lawyers won't use a terminal |
| Auto-skill creation | Hermes does this; we have the schema but not the pipeline |
| Skill curator | No lifecycle management |
| Data export/import | Memory isn't portable |
| Multi-user / permissions | Single-user only |

---

## The Four Levels

### LEVEL 1: FOUNDATION — "It works on my machine and I can show you"
**Current state. Mostly complete.**

What Foundation means: The core architecture works. Classification, retrieval, governance, gateway, decision history, voice. A single operator (Mical) can demonstrate every capability. The thesis is embodied in working code.

**Remaining Foundation work (do before BDB submission):**

| Task | What it closes | Effort | Deadline |
|------|---------------|--------|----------|
| Record Computer session (gateway build proof) | Computer usage requirement | 1 hr | May 23 |
| Rehearse + record 2-min demo video | Working product requirement | 3 hrs | May 28 |
| Landing page at missioncanvas.ai | Product link requirement | 2 hrs | May 26 |
| Write submission form answers | Application requirement | 3 hrs | May 30 |
| PII audit + push to public GitHub | Product link requirement | 2 hrs | May 29 |
| QUICKSTART.md | Judges can try it | 30 min | May 29 |

**Foundation complete when**: A judge can watch the demo, visit the landing page, read the GitHub, and understand what Palette does in under 3 minutes.

---

### LEVEL 2: PARTICIPATION — "You can download it and it works for you"
**Target: 90 days post-BDB (or immediately if no BDB win)**

This is the level where Palette becomes a product, not a personal system. The key shift: **someone who isn't Mical can install it, choose a domain, and get value on day one.**

#### 2.1 Packaging (Week 1-2)
| Task | What it enables | Effort |
|------|----------------|--------|
| Dockerfile + docker-compose | One-command install | 2 days |
| `palette setup` wizard (pick domain, set API key, confirm local storage) | First-run experience | 2 days |
| Resolve all hardcoded paths (use `Path(__file__).parent` everywhere) | Portability | 1 day |
| Single `palette` CLI entry point wrapping all commands | Coherent interface | 1 day |
| `pip install palette` or brew formula | Developer distribution | 1 day |

#### 2.2 Domain Packs (Week 3-4)
| Task | What it enables | Effort |
|------|----------------|--------|
| Legal domain pack: 30 KL entries (fiduciary duty, contract review, due diligence, filing procedures, compliance) | Day-one value for law firms | 3 days |
| Medical domain pack: 20 KL entries (treatment protocols, drug interactions, HIPAA requirements) | Second vertical | 2 days |
| Domain-specific blocked indicators per pack | Correct sanitization per vertical | 1 day |
| Domain taxonomy subset selection (20 most relevant RIUs per domain) | Focused experience | 1 day |

#### 2.3 Wire the Existing Infrastructure (Week 5-6)
| Task | What it enables | Effort |
|------|----------------|--------|
| Wire session_reflect → broker `upsertSkill` | Auto-skill creation (governed) | 2 days |
| Expose broker `searchMessages` as agent-callable tool | Conversation history search | 0.5 day |
| Wire skills/ directory to agent runtime (load relevant skills on RIU match) | Dynamic skill loading | 2 days |
| Add cross-session goal persistence (save workspace state between sessions) | Compounding across days | 2 days |
| Skill curator: archive unused skills >90 days, merge duplicates | Lifecycle management | 1 day |

#### 2.4 Local Web UI (Week 7-8)
| Task | What it enables | Effort |
|------|----------------|--------|
| Flask/FastAPI local web interface (port 8020) | Non-terminal users can use Palette | 5 days |
| Three views: Ask (query), Decisions (history), Settings (config) | Product-shaped experience | included |
| Governance trace visible in UI (what was blocked, what was sent, what was cached) | Glass-box promise | included |
| Decision timeline (visual compounding proof) | User sees their judgment trail | 2 days |

#### 2.5 Distribution (Week 8)
| Task | What it enables | Effort |
|------|----------------|--------|
| GitHub releases with tagged versions | Stable distribution | 0.5 day |
| Landing page with download link + waitlist | Acquisition | 1 day |
| YouTube "SDK for Humans" launch video (5 min) | Channel content + awareness | 1 day |
| README rewrite: product-first, not architecture-first | Developer onboarding | 1 day |

**Participation complete when**: A lawyer can download Palette, run `palette setup`, pick "Legal", and get value from their first query without reading any documentation. They can come back the next day and see their prior decisions. They can show a colleague.

---

### LEVEL 3: PERFORMANCE — "We compete with Hermes and OpenClaw"
**Target: 6 months post-launch**

This is where Palette matches and exceeds the general-purpose agents on their capabilities while maintaining the governed-ontology advantage they can't replicate.

#### 3.1 Parity Features
| Task | What it closes vs competitors | Effort |
|------|------------------------------|--------|
| Slack adapter (using existing peers/adapters pattern) | OpenClaw messaging parity | 3 days |
| Discord adapter | Community distribution | 2 days |
| WhatsApp adapter (via Twilio or direct) | Professional messaging | 3 days |
| Model fallback chain (if primary unavailable, try next) | Reliability | 1 day |
| Dynamic provider detection (scan for available models on startup) | Zero-config model support | 2 days |
| Skill auto-creation with governance (UNVALIDATED → WORKING → PRODUCTION) | Hermes parity + governance advantage | Already wired in Level 2 |
| Conversation search exposed to all agents | Hermes parity | Already wired in Level 2 |

#### 3.2 Advantages They Can't Match
| Task | Why competitors can't replicate | Effort |
|------|-------------------------------|--------|
| Legal domain pack v2: 100 KL entries + case law patterns | Domain depth requires domain expertise | 2 weeks |
| Medical domain pack v1: 50 KL entries + protocol library | Vertical expansion | 2 weeks |
| Financial advisory domain pack v1 | Third vertical | 2 weeks |
| Multi-user firm mode (shared decision history, role permissions) | Enterprise-grade local governance | 3 weeks |
| Audit export (PDF/CSV of all decisions + governance traces) | Compliance requirement | 1 week |
| Data portability (export/import judgment trails) | Memory ownership | 1 week |
| HIPAA compliance documentation + BAA template | Regulatory readiness | 1 week |

#### 3.3 YouTube / Content Engine
| Task | What it produces | Effort |
|------|-----------------|--------|
| "SDK for Humans" explainer series (5 videos) | Category definition | 1/week |
| "Ontology as Memory" deep dive | Thesis positioning | 1 video |
| "Palette vs ChatGPT memory vs Hermes" comparison | Competitive positioning | 1 video |
| Legal use case walkthrough | Vertical proof | 1 video |
| Live build sessions (building domain packs on camera) | Community + credibility | ongoing |

**Performance complete when**: A law firm using Palette can do everything an OpenClaw user can do (messaging, skill creation, conversation search, multi-model) PLUS governed memory, privacy boundary, domain knowledge, decision compounding, and audit trail. Side-by-side, Palette wins on trust, governance, and domain depth. Competitors win on community size and general-purpose breadth.

---

### LEVEL 4: EXCELLENCE — "The category leader for governed AI memory"
**Target: 12-18 months**

This is where Palette defines the category and competitors have to respond to us.

| Milestone | What it means |
|-----------|---------------|
| 200 paying firms | Product-market fit confirmed |
| 3 verticals live (legal, medical, financial) | Platform, not point solution |
| Community-contributed domain packs | Network effects |
| Anonymized cross-firm pattern library | "What are the 50 most common fiduciary duty questions across all firms using Palette?" |
| White paper published (SDK for Humans: Ontology as AI Memory) | Category definition in print |
| SOC 2 Type II certification | Enterprise sales unlock |
| Series A ($3-5M) | Scale engineering + sales |
| API for embedding Palette memory in other tools | Platform play |
| Open-source core + commercial domain packs | Obsidian model (Steph Ango lens) |

**Excellence means**: When someone says "governed AI memory for regulated professionals," they mean Palette — the way people mean Obsidian when they say "local-first knowledge management."

---

## Competitive Positioning at Each Level

| Level | Palette | Hermes Agent | OpenClaw |
|-------|---------|-------------|----------|
| **Foundation** | ✅ Working system, ontology memory, governance | ✅ Working agent, flat-file memory, skills | ✅ Working agent, plugin skills, community |
| **Participation** | Downloadable, domain packs, governed skills | Already downloadable, auto-skills | Already downloadable, huge skill library |
| **Performance** | Multi-platform + domain depth + audit + privacy | Multi-platform + skill compounding | Multi-platform + community + plugins |
| **Excellence** | Category leader: governed memory for regulated professionals | General-purpose personal agent | General-purpose personal agent |

**The strategic insight**: Hermes and OpenClaw will always be better general-purpose agents. Palette will never beat them on breadth. Palette wins by being the ONLY governed, domain-specific, ontology-memory agent for people who can't use the cloud. That's a different market, not a smaller one.

---

## What To Work On Next (Priority Order)

### RIGHT NOW (May 22-June 2): BDB Submission
Everything in Level 1 remaining. Nothing else. The submission IS the Foundation proof.

### AFTER SUBMISSION (June 3+): Level 2 Sprint
Regardless of BDB outcome, Level 2 makes Palette downloadable. That feeds:
- YouTube channel ("SDK for Humans" content)
- Job applications (live demo link > GitHub link)
- Potential pilot firms (waitlist → download → feedback)
- TikTok/short-form (screen recordings of "watch the system block your client data")

### AFTER FIRST 10 PILOTS: Level 3
Only after real users validate the product. Don't build messaging adapters until someone asks for them.

### AFTER PMF: Level 4
Only after 200 paying firms. Don't pursue SOC 2 or Series A until the revenue proves the thesis.

---

## The One Sentence

> Palette is an SDK for Humans because it uses ontology as the primary form of AI memory — and it's the only one built for professionals who can't send their data to the cloud.

Everything on this plan serves that sentence. If a task doesn't serve it, kill it.

---

*Synthesized by claude.analysis from: Codex system report, Mistral MVP analysis, Kiro strategy vote + task list, person lens (LENS-PERSON-001), founder lens (Steph Ango), white paper iterations, and 4 months of operational context. 2026-05-22.*
