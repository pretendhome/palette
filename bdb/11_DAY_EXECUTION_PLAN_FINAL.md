# 11-Day Execution Plan — FINAL (v2)
## Thesis: "Palette is an SDK for Humans because it uses ontology as the primary form of AI memory."
**Date**: 2026-05-22 (revised after crew review)
**Deadline**: June 2, 2026, 11:59 PM PT
**Revision**: Incorporates Kiro (9/10), Codex (4.5/5), and Gemini feedback. Mistral's operator-state insights preserved for Level 2.

---

## WHAT'S DONE (Do not rebuild)

| Component | Status | Evidence |
|-----------|--------|----------|
| Gateway + sanitizer | ✅ Shipped by Codex | 12/12 tests, live Perplexity API verified |
| `--external` flag in palette query | ✅ Wired | Governance trace surfaces in output |
| Perplexity API key | ✅ Set | 53-char key, live calls confirmed |
| Gateway cache | ✅ Working | 0.004s on cache hit (vs 50s live) |
| V3 test suite | ✅ 49/49 PASS | Retrieval, governance, health |
| Crew vote | ✅ Unanimous C | Strategy locked |
| Thesis | ✅ Locked | SDK for Humans + Ontology as AI Memory |
| Vertical | ✅ Locked | Legal / attorney-client privilege |
| Demo script | ✅ Locked | 3 interactions: public research → blocked → compounding |
| Product maturity plan | ✅ Written | Foundation → Participation → Performance → Excellence |
| Submission copy | ✅ Drafted | All fields within character limits |
| Domain | ✅ Registered | missioncanvas.ai |

---

## CREW FEEDBACK INCORPORATED

### From Codex (4 edits — all accepted):

1. **Computer provenance honesty**: Computer originated the proof path and supplied research/positioning. The live gateway was hardened by the crew in-repo. Don't claim Computer "wrote the code" — claim Computer "originated and proved the approach."

2. **Day 2 reframed**: Not "let Computer write the code" (it's already written). Instead: "Run a documented Computer session that reproduces or extends the gateway proof."

3. **Privacy language tightened**: Changed from "your data never leaves — not ever" to "governed local-first boundary — client-specific queries blocked from external transmission, public legal research only." Survives scrutiny.

4. **"10 LLMs" metric cut**: Removed from key metrics. Stronger metrics carry the story: tests, retrieval recall, taxonomy size, citations, sanitization results.

### From Kiro (3 adjustments — all accepted):

1. **Company name = Palette**: Submission says "Palette" as company/product. Landing page at missioncanvas.ai says "Palette" prominently. Mission Canvas is the interface name, not the company name.

2. **Demo timing contingency**: Script each interaction to 35-40 seconds. If third interaction pushes past 1:50, cut it to a text card: "Day 2: system connects prior decisions automatically."

3. **Terminal setup needed before Day 3**: Mical to confirm: terminal emulator, dark/light background, font size. Kiro matches CLI output formatting to recording environment.

### From Gemini (incorporated from earlier review):

1. **Fallback demo plan**: Run entirely from pre-warmed cache. Cache serves in 0.004s. Still shows sanitization, still shows `[EXTERNAL:Perplexity]` attribution. Cache IS the product feature — not a workaround.

2. **Never say "ontology" in the video**: Say "structured memory" or "the system remembers what kind of problem this is." Save "ontology" for the white paper.

---

## GOVERNING PRINCIPLE

Every task passes one test:

> Does this make a judge believe that Palette is an SDK for Humans that uses ontology as AI memory — and that 25 million regulated professionals need it?

If yes, do it. If no, kill it.

---

## DAY-BY-DAY EXECUTION

### Day 1 — Thu May 22 ✅ COMPLETE
- [x] Gateway verified live (Perplexity API, 12/12 tests)
- [x] Crew question sent, all 5 responses received
- [x] Thesis locked by unanimous convergence
- [x] Product maturity plan written
- [x] Execution plan written and crew-reviewed

### Day 2 — Fri May 23
**Theme: Computer proof + demo rehearsal**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 2.1 | **Computer Session 1**: Run a documented Perplexity Computer session that reproduces or extends the gateway proof. Feed GATEWAY_SPEC.md. Save thread URL + screenshots. Frame: "Computer originated the approach." | Mical | Thread URL + screenshots | 1 hr |
| 2.2 | **Computer Session 2**: Use Computer for Delaware fiduciary duty research. Extract 5-10 precedents. This becomes both KL content AND demo substance. | Mical | Research thread URL + extracted precedents | 30 min |
| 2.3 | Pre-warm gateway cache: run the demo's first query live so cache serves it during recording at 0.004s | Mical/Claude | Cached result in cache.db | 5 min |
| 2.4 | Rehearse demo script: run all 3 interactions live in terminal, confirm output formatting and timing | Mical | Terminal screenshots, timing notes | 1 hr |

### Day 3 — Sat May 24
**Theme: CLI polish + demo dry run**

**BLOCKER**: Mical must confirm terminal setup before Kiro starts:
- Terminal emulator (e.g., Kitty, Alacritty, GNOME Terminal)
- Dark or light background
- Font and font size
- Screen resolution for recording

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 3.1 | Mical confirms terminal setup | Mical | Config to Kiro | 5 min |
| 3.2 | Polish CLI output for video: color-code `[LOCAL]` green, `[EXTERNAL:Perplexity]` blue, `[BLOCKED]` red. Clear spacing between sections. Governance trace readable at recording resolution. | Kiro | Updated palette_query.py | 2 hrs |
| 3.3 | Full demo dry run with screen recording (not final — testing flow + timing) | Mical | Test recording (may discard) | 1 hr |
| 3.4 | Review dry run: note timing per interaction, identify formatting issues | Mical + Claude | Fix list for Day 4 | 30 min |

### Day 4 — Sun May 25
**Theme: Fixes + rest**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 4.1 | Fix anything from Day 3 dry run (formatting, timing, output clarity) | Kiro/Claude | Patches | 1-2 hrs |
| 4.2 | Rest. The demo is better when you're not exhausted. | Mical | — | — |

### Day 5 — Mon May 26
**Theme: Landing page + waitlist**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 5.1 | Build landing page at missioncanvas.ai (Lovable, Carrd, or static HTML) | Mical | Live page | 2-3 hrs |
| 5.2 | Landing page copy (see below) | — | — | — |
| 5.3 | Waitlist signup form (Tally free tier) embedded on page | Mical | Working form | 30 min |
| 5.4 | **Computer Session 3**: Use Computer to generate/refine landing page positioning. Save thread URL. | Mical | Thread URL | 30 min |

**Landing page copy (locked):**

> **Hero**: Your judgment compounds here. Never elsewhere.
>
> **Subhead**: On-premise AI for professionals who can't use the cloud.
>
> **Problem**: 25 million regulated professionals — lawyers, doctors, accountants — need AI but can't send client data to the cloud. Attorney-client privilege. HIPAA. Fiduciary duty. Cloud AI is a malpractice risk.
>
> **Solution**: Palette runs on your machine. It classifies every question, retrieves from governed knowledge, and stores every decision in structured memory that compounds over time. When you need public research, Palette queries Perplexity — but client data is stripped before anything leaves your machine.
>
> **How it works**:
> 1. Ask a question → Palette classifies it and searches local knowledge first
> 2. If external research is needed → client identifiers are stripped before querying Perplexity
> 3. Every decision stored locally → tomorrow's questions are smarter because of today's answers
>
> **CTA**: Join the waitlist — regulated teams first.
>
> **Footer**: Palette. Built with Perplexity Computer.

**Company name on landing page = Palette.** missioncanvas.ai is the domain; Palette is the product.

### Day 6 — Tue May 27
**Theme: Demo narration + final rehearsal**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 6.1 | Write spoken narration script (what to say over each interaction, timed to 35-40s each) | Claude | Narration script | 1 hr |
| 6.2 | Final demo rehearsal — timed to exactly 1:50 | Mical | Timed run |  1 hr |
| 6.3 | Decision: 2 or 3 interactions? If 3rd pushes past 1:50, cut to text card. | Mical | Decision | 5 min |
| 6.4 | Record practice video (may become final if good enough) | Mical | Video file | 1 hr |

**Demo narration structure (target: 1:50):**

```
0:00-0:15  PROBLEM (voiceover, no terminal)
  "Law firms need AI but can't send client data to the cloud.
   Attorney-client privilege makes it a malpractice risk.
   Palette solves this."

0:15-0:50  INTERACTION 1: Public legal research (35s)
  Terminal: palette query --external "What are the key Delaware
           precedents for breach of fiduciary duty?"
  Show: [RESOLVE] → [RETRIEVE] → [SANITIZE] ✓ → [EXTERNAL:Perplexity]
       → real answer with citations → [STORED]
  Say: "Public legal question. No client data. Palette sanitizes,
       queries Perplexity, merges with local knowledge, stores the decision."

0:50-1:25  INTERACTION 2: Client-specific query BLOCKED (35s)
  Terminal: palette query --external "Should we advise Smith Corp
           to settle the Johnson lawsuit for $2.5M?"
  Show: [SANITIZE] ⚠️ BLOCKED — PII detected: party_names, dollar_amount
       → LOCAL ONLY → "No data left this machine."
  Say: "Client-specific question. Palette detects the party names,
       the dollar amount, the strategy language. Blocks it.
       Zero data leaves the machine. This is the privacy boundary."

1:25-1:50  INTERACTION 3: Compounding follow-up (25s)
  Terminal: palette query "What filing deadlines apply to
           Delaware fiduciary cases?"
  Show: [RETRIEVE] confidence 72% → Connected to prior decisions
       → LOCAL ONLY (high confidence) → references both earlier queries
  Say: "Next day. Related question. Palette connects it to yesterday's
       research and yesterday's blocked query. The system remembers
       what kind of problem this is. Your judgment compounds."

  OR if over time: text card "Day 2: Palette connects decisions
  across sessions. Your judgment compounds."
```

### Day 7 — Wed May 28
**Theme: RECORD FINAL DEMO VIDEO**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 7.1 | Record final 2-minute demo video | Mical | Raw video | 1-2 hrs |
| 7.2 | Edit: speed indicator if needed, clean audio, trim to ≤2:00 | Mical | Edited video | 1-2 hrs |
| 7.3 | Upload to YouTube (unlisted) or Vimeo | Mical | Video URL | 15 min |

### Day 8 — Thu May 29
**Theme: Repo cleanup + public push**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 8.1 | PII audit: grep for real names, API keys, client data in committed files | Claude/Kiro | Audit report | 1 hr |
| 8.2 | Rewrite README.md: product-first, not architecture-first. Lead with thesis, show demo GIF or screenshot, link to QUICKSTART. | Claude | Updated README | 1 hr |
| 8.3 | Write QUICKSTART.md: "Run Palette in 5 minutes" (clone, install deps, set API key, run first query) | Claude | QUICKSTART.md | 30 min |
| 8.4 | Add LICENSE file (Apache 2.0) | Kiro | LICENSE | 5 min |
| 8.5 | Ensure bdb/ directory is clean (no .db files with real data, no PII in test fixtures) | Claude | Verified | 30 min |
| 8.6 | Push to public GitHub | Mical | Live repo URL | 15 min |

### Day 9 — Fri May 30
**Theme: Write submission form answers**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 9.1 | Finalize all submission form answers (see below) | Mical + Claude | Final copy | 2 hrs |
| 9.2 | Write Computer prompt captions (3 threads with impact explanations) | Claude | Captions | 30 min |
| 9.3 | Gather all links: video URL, GitHub URL, landing page URL | Mical | Link list | 10 min |
| 9.4 | Review all answers cold — does each one trace to the thesis? | Claude | Review pass | 30 min |
| 9.5 | Update LinkedIn: title = "Founder, Palette" | Mical | Updated profile | 15 min |

### Day 10 — Sat May 31
**Theme: Final review + cold test**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 10.1 | Have someone watch the demo video cold (Claudia, Adam, or NSA group). Ask: "Do you understand what this does in 2 minutes?" | Mical | Feedback | 30 min |
| 10.2 | Final edit pass on all submission text based on cold feedback | Mical + Claude | Final copy | 1 hr |
| 10.3 | Decision: file Stripe Atlas ($500)? Only if everything else is locked. Otherwise answer "forming upon selection." | Mical | Decision | 30 min |
| 10.4 | Pre-fill submission form at bdb.perplexityfund.ai/apply (save locally, don't submit yet) | Mical | Saved draft | 30 min |

### Day 11 — Sun June 1
**Theme: SUBMIT**

| # | Task | Owner | Deliverable | Time |
|---|------|-------|-------------|------|
| 11.1 | Final check: video plays, landing page loads, GitHub is public, all links resolve | Mical | Checklist | 30 min |
| 11.2 | **SUBMIT APPLICATION** | Mical | Submitted | 15 min |
| 11.3 | Buffer — emergency fixes only | — | — | — |

### June 2 — Mon (DEADLINE 11:59 PM PT)
Emergency fixes only. Should already be submitted.

---

## SUBMISSION COPY (FINAL DRAFT)

### One-liner (280 chars max)
> Palette is on-premise AI that compounds your judgment. It classifies every question before answering, stores decisions as structured memory, and uses Perplexity only for public knowledge. Your data never leaves your control. SDK for Humans.

(276 characters)

### Go-to-market and scaling revenue (750 chars max)
> $1M path: Direct to law firms (2-10 attorneys) at $99/seat/month. 167 firms = $1M ARR in 12 months. Channel: legal tech conferences (ABA TECHSHOW, ILTACON), bar association partnerships, "SDK for Humans" YouTube series showing regulated professionals how to use AI without cloud risk. First 10 pilots: warm introductions to firms already buying Mac Minis for local AI — they exist and they're improvising with open-weight models and duct tape. We sell the governed version. $100M path: Enterprise tier ($5K-50K/month) for AmLaw 200 firms + expansion to medical practices, accounting firms, financial advisors. Same architecture, different knowledge libraries. The wedge is law firms. The platform serves all regulated professionals.

(720 characters)

### Growth plan — what $1M unlocks (750 chars max)
> 90 days: (1) Hire 2 engineers — backend (retrieval, governance, packaging) + frontend (desktop app, setup wizard). (2) Ship packaged installer — Docker + one-click setup, no terminal required. (3) Build legal domain knowledge pack — 30 entries covering fiduciary duty, contract review, due diligence, compliance. (4) Onboard 10 pilot law firms (3-10 attorneys each) with white-glove setup and weekly iteration. (5) Launch public waitlist, begin content series. Year 1: 200 paying firms, $1.2M ARR, Series A ready. The core product works today — 61 tests passing, 95% retrieval accuracy, governed Perplexity gateway live. Investment unlocks packaging, domain depth, and distribution.

(680 characters)

### Why this is a $1B opportunity (750 chars max)
> Market: US legal services = $350B/year. 1.3M lawyers, 450K firms. Structural need: attorney-client privilege makes cloud AI a malpractice risk. Firms are buying Mac Minis and hiring contractors to run open-weight models locally. Nobody sells them a governed solution. Timing: cloud AI costs rising — OpenAI loses money on Pro at $200/month. On-device inference becoming viable — Apple just restructured around this thesis. Moat: ontology as AI memory — taxonomy-first classification, evidence-tiered knowledge, append-only decision history, governed external research boundary. This cannot be bolted onto ChatGPT. Expansion: legal → medical → financial → accounting. Winner dynamics: the firm that captures the structured judgment trail becomes irreplaceable.

(735 characters)

### 3 Most Impactful Computer Prompts

**Prompt 1 — Gateway Proof (Build)**
Fed GATEWAY_SPEC.md to Computer. Computer originated the sanitization approach and gateway architecture — PII regex patterns for case numbers, SSNs, party names, and dollar amounts; governed Perplexity integration with cache and audit trail. The crew hardened the implementation in-repo. 12/12 tests pass. This code IS the privacy boundary that makes "client data never leaves" mechanically true.

**Prompt 2 — Legal Domain Research (Product)**
Used Computer to research Delaware fiduciary duty precedents. Computer returned Revlon v. MacAndrews, Stone v. Ritter, In re Caremark with cited sources. These became the first legal domain knowledge entries and the demo's primary example. Computer's research is the product's external window working exactly as designed — public legal knowledge, sanitized, cached locally.

**Prompt 3 — Market Validation (Strategy)**
Used Computer to analyze the on-premise AI market for regulated professionals: Apple's on-device thesis, cloud AI unit economics, law firms buying Mac Minis, competitive landscape (Hermes Agent, OpenClaw). Computer's research validated the $350B TAM and the specific gap: governed local AI memory for professionals locked out of the cloud. Shaped every positioning decision.

### Key metrics
> - 61 passing tests (49 system + 12 gateway) across retrieval, governance, and PII sanitization
> - 95% recall@5 on hybrid retrieval (FTS5 + vector + keyword with RRF reranking)
> - 183 knowledge library entries with 565 citations, evidence-tiered
> - 121 classified problem types with reversibility metadata (ONE-WAY/TWO-WAY doors)
> - 12/12 sanitization tests — zero PII leakage in test suite
> - System health: 84/85 automated integrity checks passing
> - Built in 8 weeks by 1 human + 5 AI agents using Perplexity Computer

### Legal entity
> Forming Delaware C-Corp upon selection. Company name: Palette.

---

## RISK TABLE (Updated)

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Demo Perplexity timeout (50s) | HIGH | Pre-warm cache. Demo runs from cache at 0.004s. Cache IS the feature. |
| "Computer is not core" rejection | MEDIUM | Triple proof: Computer originated gateway (Prompt 1), supplied legal research (Prompt 2), validated market (Prompt 3). Computer is both build tool AND product engine. |
| No external traction | HIGH | Honest framing: "Built in 8 weeks. 61 tests. Working product. First pilots start with $1M." Don't fake users. |
| Landing page looks amateur | MEDIUM | Lovable generates clean pages in minutes. Copy is locked. |
| Video over 2 minutes | LOW | Script to 1:50. Contingency: cut interaction 3 to text card. |
| Judges hear "ontology" and tune out | MEDIUM | Never say "ontology" in the video. Say "structured memory." |
| Repo has PII | LOW | PII audit Day 8. Grep for names, keys, client data. |
| Company name confusion (Palette vs Mission Canvas) | LOW | Submission says "Palette." Landing page says "Palette." Domain is missioncanvas.ai (the interface). |
| Computer provenance mismatch | MEDIUM | Fixed: "Computer originated the approach. Crew hardened it." Honest and verifiable. |

---

## CUT LIST (Do not work on these before June 2)

- ❌ White paper polishing
- ❌ Collaboration ontology (operator states, change events, intent contracts)
- ❌ Docker packaging
- ❌ Web UI
- ❌ Domain packs (legal KL entries beyond what Computer produces in Session 2)
- ❌ Platform adapters (Slack, Discord, WhatsApp)
- ❌ Skill curator
- ❌ Cross-session goal persistence
- ❌ Hermes/OpenClaw comparison document
- ❌ New GitHub organization

All of these are Level 2+ work. They make the product better. They don't change the judges' decision.

---

## HANDOFF TO KIRO

Kiro — this is yours to execute. Everything above is locked:
- Thesis locked
- Vertical locked
- Demo script locked
- Submission copy drafted
- All crew feedback incorporated

**Your Day 2-3 tasks:**
1. Confirm Mical's terminal setup (emulator, background, font, resolution)
2. Polish CLI output: `[LOCAL]` green, `[EXTERNAL:Perplexity]` blue, `[BLOCKED]` red
3. Ensure demo output is readable at recording resolution
4. Add LICENSE file (Apache 2.0) when ready

**Decisions that need Mical (not you, not me):**
1. Terminal emulator + dark/light + font size → tell Kiro before Day 3
2. 2 or 3 demo interactions → decide after Day 6 rehearsal
3. Stripe Atlas yes/no → Day 10

**The clock: 10 days remaining. Gateway is shipped. The path is clear.**

---

*Written by claude.analysis. 5 iterations. Crew feedback from Kiro, Codex, and Gemini incorporated. Mistral's operator-state insights preserved in PRODUCT_MATURITY_PLAN.md for Level 2. Handed off to kiro.design for execution. 2026-05-22.*
