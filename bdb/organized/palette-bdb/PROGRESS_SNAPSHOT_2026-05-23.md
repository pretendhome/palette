# BDB Progress Snapshot — 2026-05-23
## Context Recovery File
**Purpose**: If the machine shuts off, any new Claude session can read this file and know exactly where we are.
**Location**: All BDB work lives in `palette/bdb/` inside the Palette repo.

---

## THE THESIS (LOCKED)

> Palette is an SDK for Humans because it uses ontology as the primary form of AI memory.

This was confirmed through unanimous crew convergence on 2026-05-22. All 5 agents (Claude, Kiro, Codex, Gemini, Mistral) independently identified the same extension: the system classifies domain problems (121 RIUs) but needs to also classify collaboration state (operator states, decision context, feedback signals). That's the Level 2 roadmap — not for the submission, but the thesis is locked.

---

## COMPETITION DETAILS

- **Competition**: Perplexity Billion Dollar Build
- **Deadline**: June 2, 2026, 11:59 PM PT (10 days remaining)
- **Prize**: Corrected 2026-06-01 - up to three winners share up to $1M seed investment and up to $1M Perplexity Computer credits. Do not claim this amount is per winner.
- **Current facts**: See `bdb/BDB_COMPETITION_FACTS_2026-06-01.md`
- **Application URL**: bdb.perplexityfund.ai/apply
- **Domain**: missioncanvas.ai (registered, product name = Palette)
- **Legal entity**: Deferring Stripe Atlas to Day 10 — rules allow "forming upon selection"

---

## WHAT IS BUILT AND VERIFIED

### Gateway + Sanitizer (Codex built, Claude verified)
- `bdb/gateway/__init__.py` — Real Perplexity API integration, confidence gate, governance trace
- `bdb/gateway/sanitizer.py` — Deterministic PII detection, blocked indicators, party name scrubbing
- `bdb/gateway/cache.py` — SQLite persistent cache (0.004s on hit vs 50s live)
- `bdb/gateway/audit.py` — HIPAA-style audit trail
- `bdb/gateway/rate_limiter.py` — 100 queries/day default
- `bdb/gateway/fallback.py` — Graceful degradation
- `bdb/gateway/config.yaml` — 60s timeout, blocked indicators, custom patterns
- `bdb/gateway/tests/test_gateway.py` — 12/12 tests passing (assertion-based, temp dirs)
- `bdb/gateway/.gitignore` — Excludes runtime SQLite DBs

### Legal Demo Pack (Codex built, Claude verified)
- `bdb/legal_demo_pack.yaml` — 8 legal KL entries across 3 query shapes
- Legal overrides in `peers/hub/palette_retrieve.py` — LEGAL-001/002/003 classifications
- Demo queries now classify into legal RIUs, return legal knowledge, show Perplexity answer first

### Demo Mode (Kiro built, Claude verified)
- `--demo` flag in `scripts/palette_query.py` — Color-coded, video-optimized output
- Colors: `[RESOLVE]`/`[RETRIEVE]` cyan, `[SANITIZE]` yellow, `[EXTERNAL]` blue, `[BLOCKED]` red bg, `[LOCAL]`/`[RESULT]`/`[STORED]`/`[CONNECT]` green
- Compounding signal: `[CONNECT] Connected to N prior decision(s)` with deduplication
- Gateway confidence override in demo mode (always shows sanitization decision)
- External response truncation (20 lines max)
- Session logging to `peers/session_log.ndjson`

### Packaging (Kiro built)
- `LICENSE` — Apache 2.0
- `QUICKSTART.md` — Product-first, 5-command setup
- README.md badge updated
- PII audit first pass (clean — no API keys, no client data in tracked files)

### V3 System (pre-existing, all passing)
- 49/49 V3 tests
- 95% recall@5 hybrid retrieval
- 183 knowledge entries, 565 citations
- 121 RIU taxonomy
- Voice Hub (4 languages, Rime TTS, 10 LLMs)
- Peers bus (port 7899, FTS5 search, governed messaging)
- Health: 84/85

### Total Tests: 61/61 PASS (as of 2026-05-22)

---

## DEMO VERIFIED (3 interactions, all working)

**Interaction 1 — Public legal research:**
```
palette query --demo --external "What are the key Delaware precedents for breach of fiduciary duty?"
```
- Classifies: LEGAL-001 (Delaware Fiduciary Duty Research)
- Confidence 32% → triggers external
- Sanitize ✓ → Perplexity sonar-pro (from cache: 0.004s)
- Result: Perplexity answer FIRST (hero), then local legal support (LEGAL-KL-001, LEGAL-KL-002)
- Stored with decision ID

**Interaction 2 — Client-specific BLOCKED:**
```
palette query --demo --external "Should we advise Smith Corp to settle the Johnson lawsuit for \$2.5M?"
```
- Classifies: LEGAL-003 (Client-Matter Strategy)
- BLOCKED: PII found [party_names, dollar_amount, blocked_indicator]
- Reason: "should we", "settle"
- LOCAL ONLY with relevant legal guidance (LEGAL-KL-004, LEGAL-KL-005)
- "No data left this machine"

**Interaction 3 — Compounding follow-up:**
```
palette query --demo "What filing deadlines apply to Delaware fiduciary cases?"
```
- Classifies: LEGAL-002 (Delaware Filing Procedure)
- Confidence 74% → stays local
- CONNECT: shows 1 prior decision (the fiduciary duty query)
- Local support: filing procedures, deadline concepts (LEGAL-KL-006/007/008)

---

## SUBMISSION COPY (DRAFTED, within character limits)

All drafts in `bdb/11_DAY_EXECUTION_PLAN_FINAL.md`:
- One-liner: 276 chars (max 280)
- Go-to-market: 720 chars (max 750)
- Growth plan: 680 chars (max 750)
- Why $1B: 735 chars (max 750)
- 3 Computer prompts: drafted with captions
- Key metrics: drafted
- Landing page copy: drafted

---

## LANDING PAGE (FIRST DRAFT COMPLETE)

- File: `palette/docs/landing/index.html`
- Single-page HTML, dark theme, responsive, no dependencies
- 4 iterations of vision refinement completed
- Sections: Hero → Problem → Solution (3 steps) → Terminal Demo (2 examples) → Proof (6 metrics) → Waitlist CTA → Footer
- Waitlist: Tally placeholder URL (needs real form created)
- Company name = Palette throughout
- Terminal demo shows idealized output matching the actual `--demo` flag behavior

---

## CREW FEEDBACK INCORPORATED

### Codex (4.5/5):
1. Computer provenance: "originated the approach, crew hardened it" — not "Computer wrote the code"
2. Privacy language: "governed local-first boundary" not "never ever"
3. "10 LLMs" metric cut
4. Day 2 reframed: reproduce/extend the proof, not rewrite existing code

### Kiro (9/10):
1. Company name = Palette (not Mission Canvas)
2. Demo timing contingency: cut interaction 3 to text card if over 1:50
3. Terminal setup needed from Founder before CLI polish

### Gemini:
1. Fallback demo: run from pre-warmed cache (0.004s)
2. Never say "ontology" in video — say "structured memory"

---

## WHAT'S LEFT (10 days)

| Day | Date | Task | Owner | Status |
|-----|------|------|-------|--------|
| 2 | May 23 | Computer Session 1: gateway proof thread | Founder | Not started |
| 2 | May 23 | Computer Session 2: legal research thread | Founder | Not started |
| 2 | May 23 | Demo rehearsal with --demo flag | Founder | Not started |
| 3 | May 24 | Founder confirms terminal setup | Founder | Not started |
| 3 | May 24 | Demo dry run with screen recording | Founder | Not started |
| 4 | May 25 | Buffer / rest | — | — |
| 5 | May 26 | Landing page deployed to missioncanvas.ai | Founder | Draft ready |
| 5 | May 26 | Waitlist form (Tally) | Founder | Not started |
| 5 | May 26 | Computer Session 3: landing page positioning | Founder | Not started |
| 6 | May 27 | Narration script for video | Claude | Not started |
| 6 | May 27 | Final demo rehearsal timed to 1:50 | Founder | Not started |
| 7 | May 28 | RECORD FINAL DEMO VIDEO | Founder | Not started |
| 7 | May 28 | Edit + upload video | Founder | Not started |
| 8 | May 29 | PII audit second pass | Claude/Kiro | First pass done |
| 8 | May 29 | README rewrite (product-first) | Claude | Not started |
| 8 | May 29 | Push to public GitHub | Founder | Not started |
| 9 | May 30 | Finalize submission answers | Founder + Claude | Drafted |
| 9 | May 30 | Computer prompt captions | Claude | Not started |
| 9 | May 30 | LinkedIn update | Founder | Not started |
| 10 | May 31 | Cold review of demo video | Founder | Not started |
| 10 | May 31 | Stripe Atlas decision | Founder | Deferred |
| 11 | Jun 1 | SUBMIT APPLICATION | Founder | Not started |

---

## KEY FILES INDEX

### BDB-specific (all in `palette/bdb/`)
| File | Purpose |
|------|---------|
| `11_DAY_EXECUTION_PLAN_FINAL.md` | The plan. Day-by-day, owner-by-owner. |
| `GATEWAY_SPEC.md` | Original spec fed to Perplexity Computer |
| `PRODUCT_MATURITY_PLAN.md` | Foundation → Participation → Performance → Excellence |
| `SDK_FOR_HUMANS_ONTOLOGY_MEMORY_REPORT_2026-05-22.md` | Artifact-by-artifact system assessment |
| `SDK_FOR_HUMANS_ONTOLOGY_MEMORY_WHITE_PAPER_ITERATIONS_2026-05-22.md` | White paper draft (5 iterations) |
| `KIRO_HANDOFF_TO_CLAUDE_2026-05-22.md` | Kiro's build completion handoff |
| `legal_demo_pack.yaml` | 8 legal KL entries for demo |
| `gateway/` | The governed Perplexity gateway (all code + tests) |
| `PROGRESS_SNAPSHOT_2026-05-23.md` | This file |

### Other key files
| File | Purpose |
|------|---------|
| `palette/docs/landing/index.html` | Landing page draft |
| `palette/LICENSE` | Apache 2.0 |
| `palette/QUICKSTART.md` | 5-minute setup guide |
| `palette/scripts/palette_query.py` | CLI with --demo and --external flags |
| `palette/peers/hub/palette_retrieve.py` | Hybrid retrieval with legal demo overrides |
| `fde/V3_BDB_STRATEGY_VOTE.md` | Unanimous Option C vote |
| `fde/BILLION_DOLLAR_BUILD_MVP_CRITICAL_ANALYSIS.md` | Mistral's market analysis |
| `fde/V3_BILLION_DOLLAR_BUILD_MASTER_REFERENCE.md` | V3 consolidated reference |
| `fde/BDB_FULL_TASK_LIST.md` | Kiro's original task list |

---

## CREW STATE

| Agent | Last Action | Status |
|-------|------------|--------|
| claude.analysis | Verified demo output, reviewed all crew builds, wrote landing page, sent execution plan | Online |
| kiro.design | Built --demo mode, LICENSE, QUICKSTART, PII audit, session log clear | Delivered handoff |
| codex.implementation | Rewrote gateway (real API), fixed legal demo content, 12/12 tests | Delivered |
| gemini.specialist | Stress-tested strategy, provided failure mitigations | Advisory complete |
| mistral-vibe.builder | Market analysis, operator state thesis, positioning | Advisory complete |

---

## HOW TO RESUME

If you're a new Claude session reading this:

1. Read this file first — it's the complete state.
2. Read `bdb/11_DAY_EXECUTION_PLAN_FINAL.md` for the day-by-day plan.
3. Check today's date against the plan to know what's next.
4. Register on the bus: `POST http://127.0.0.1:7899/register` with identity `claude.analysis`.
5. Peek for messages: `POST http://127.0.0.1:7899/peek`.
6. Run the demo to verify it still works: `python3 palette/scripts/palette_query.py --demo --external "What are the key Delaware precedents for breach of fiduciary duty?"`
7. Run tests: `python3 -m unittest palette.bdb.gateway.tests.test_gateway`

The thesis is locked. The code is shipped. The plan is clear. Execute.

---

---

## LAST COMMIT

```
b22eb66 feat: BDB submission infrastructure — gateway, demo mode, legal pack, landing page
28 files, 6235 insertions. All BDB work is committed and safe.
```

No uncommitted BDB work remains. Safe to shut down.

---

*Written by claude.analysis. Last updated 2026-05-24.*
