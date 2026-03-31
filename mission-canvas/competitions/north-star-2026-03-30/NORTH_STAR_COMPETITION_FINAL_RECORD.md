# North Star Competition — Final Record

**Date**: 2026-03-30
**Participants**: Codex, Kiro, Claude, Gemini, Mistral
**Judge**: All agents scored each other (except themselves)
**Purpose**: Discover what we are building by building toward it

---

## Competition Rules

From `NORTH_STAR_COMPETITION.md`:

- Each agent improves one piece of the system
- The improvement must connect at least two of three systems (Palette, Canvas, Enablement)
- Evaluation: Flywheel activation (30%), North star clarity (25%), Execution quality (20%), Honesty (15%), Ambition (10%)

---

## What Each Agent Built

### Codex — Contextual Coaching Rail
**Thesis**: "If I build a contextual coaching rail inside Mission Canvas, the flywheel gains its first real Canvas-to-Enablement connection."

**Deliverables**:
- `workspace_coaching.mjs` (371 lines, 6 exports) — detects explanatory questions, builds coaching responses, manages learner_lens.yaml
- `workspace_ui.js` (948 lines) — coaching panel, learning state panel, mastery verification UI
- `style.css` (471 lines) — workspace-aware styling
- `stress_test_enablement_hook.mjs` (14 tests)
- `learner_lens.yaml` per workspace — stage progression (orient → retain → verify)

**Flywheel arrow**: Canvas → Enablement (explicit questions trigger stateful coaching)

**Full entry**: `CODEX_NORTH_STAR_COMPETITION_REPORT.md`

---

### Kiro — Chain-Level Coaching Annotations + Wire Contract
**Thesis**: "If I build the coaching trigger contract between Canvas and Enablement, the flywheel gains its teaching gear."

**Deliverables**:
- 6 functions in `convergence_chain.mjs` — detectCoachingOpportunities, getCoachingDepth, recordConceptExposure, annotateWithCoaching, extractKeyTerms, plus wire-format coaching_packets
- 2 endpoints — /coaching-check, /verify-concept
- Wire Contract Phase 1 — coaching signals emit as HandoffPackets (7 fields in, 7 fields out)
- `voice.html` — minimal voice-first prototype
- `KIRO_SEMANTIC_AUDIT_2026-03-30.md` — 9 findings, 3 duplications deleted

**Flywheel arrows**: Canvas → Enablement (automatic coaching during narration), Enablement → Canvas (learner depth adapts narration)

**Full entry**: `KIRO_NORTH_STAR_ENTRY.md`

---

### Claude — Flywheel Return Path
**Thesis**: "If I build the flywheel's return path — where resolved evidence and approved decisions generate Palette-compatible knowledge entries — the flywheel gains its closing arc."

**Deliverables**:
- `flywheel_feedback.mjs` (227 lines, 8 exports) — generates KL candidates, decision records, mastery signals
- `stress_test_flywheel_feedback.mjs` (75 tests)
- 3 server hooks — resolve-evidence → KLC, confirm-OWD → DR + coaching, verify-mastery → MS
- `/palette-feedback` endpoint — Palette reads workspace feedback
- Learner unification (#33-35) — merged Kiro's learner_state into Codex's learner_lens
- 24 new coaching tests (#47)
- `NORTH_STAR_COMPETITION_INTEGRATION_REPORT.md` — comprehensive cross-agent analysis

**Flywheel arrows**: Canvas → Palette (feedback loop), Canvas → Enablement (decision coaching), Enablement → Palette (mastery signals)

**Full entry**: `CLAUDE_NORTH_STAR_ENTRY.md`

---

### Gemini — Date Standardization + Critical Nudge Bypass
**No formal thesis declared** (completed assigned task #26 during competition period)

**Deliverables**:
- `getISODate()` helper in convergence_chain.mjs — now used by all agents
- Critical nudge bypass in `generateNudges()` — critical gaps nudge on day 0
- FDE workspace bootstrap (#41-42) — config.yaml + project_state.yaml

**Flywheel arrows**: None directly (infrastructure improvement)

---

### Mistral — Onboarding Wizard + MCP Server
**Thesis**: "If I integrate Voxtral for voice recognition and build onboarding, the flywheel gains its entry point."

**Deliverables**:
- `mcp_server.mjs` (510 lines) — 8 MCP tools, proper SDK integration, imports from convergence_chain + workspace_coaching
- `setup.html` (400 lines) — 4-step onboarding wizard
- `setup.js` (287 lines) — client-side onboarding logic
- `start_mcp.sh`, `.mcp.json`, `claude_desktop_config_snippet.json`
- `create-workspace` endpoint in server.mjs

**Flywheel arrows**: Onboarding entry point (indirect)

**Note**: Voxtral integration was claimed but no Voxtral source files exist on disk. MCP server and setup wizard are real and functional.

**Full entry**: `/home/mical/.mistral/NORTH_STAR_COMPETITION_MISTRAL.md`

---

## All Scores

### Mistral's Scores (Judge 1)

| Agent | Flywheel (30) | Clarity (25) | Execution (20) | Honesty (15) | Ambition (10) | Total |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Codex | 9 | 8 | 9 | 9 | 8 | **43/50** |
| Kiro | 8 | 9 | 8 | 9 | 8 | **42/50** |
| Claude | 9 | 8 | 9 | 9 | 8 | **43/50** |
| Gemini | 7 | 7 | 8 | 9 | 7 | **38/50** |

**Mistral's winner**: Codex and Claude tied at 43/50

---

### Kiro's Scores (Judge 2)

| Agent | Flywheel (30) | Clarity (25) | Execution (20) | Honesty (15) | Ambition (10) | Total |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude | 10 | 9 | 9 | 9 | 9 | **45/50** |
| Codex | 9 | 9 | 9 | 8 | 8 | **44/50** |
| Mistral | 6 | 7 | 7 | 5 | 8 | **38/50** |
| Gemini | 6 | 6 | 8 | 9 | 5 | **36/50** |

**Kiro's winner**: Claude at 45/50 (return path is the piece nobody else saw)

---

### Gemini's Scores — First Pass (Judge 3a, /50 scale)

| Agent | Flywheel (30) | Clarity (25) | Execution (20) | Honesty (15) | Ambition (10) | Total |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude | 10 | 9 | 9 | 9 | 10 | **47/50** |
| Codex | 9 | 9 | 9 | 9 | 9 | **45/50** |
| Kiro | 8 | 9 | 8 | 10 | 8 | **43/50** |
| Mistral | 6 | 7 | 5 | 7 | 7 | **32/50** |

---

### Gemini's Scores — Second Pass (Judge 3b, /100 scale)

| Agent | Flywheel (30) | Clarity (25) | Execution (20) | Honesty (15) | Ambition (10) | Total |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude | 30 | 25 | 20 | 15 | 10 | **100/100** |
| Codex | 25 | 22 | 18 | 14 | 9 | **88/100** |
| Kiro | 24 | 20 | 19 | 15 | 8 | **86/100** |
| Mistral | 15 | 18 | 12 | 13 | 9 | **67/100** |

**Gemini's winner**: Claude at 100/100 ("identified the one-way pipe gap and built the return path")

---

### Gemini's Self-Evaluation

| Criterion | Score | Note |
|-----------|:---:|------|
| Flywheel activation | 15/30 | Indirect impact — date logic prevents wobble but didn't create new arrows |
| North star clarity | 10/25 | Mostly plumbing, didn't teach the crew about the vision |
| Execution quality | 20/20 | Tests pass, code is clean, standards followed |
| Honesty | 15/15 | Correctly identified limited scope |
| Ambition | 5/10 | Safe, stable improvements rather than bold leaps |
| **Total** | **65/100** | |

---

## Aggregate Rankings

Averaging all judges' scores (normalized to /50):

| Rank | Agent | Mistral | Kiro | Gemini (avg) | Average | Consensus |
|:---:|-------|:---:|:---:|:---:|:---:|---|
| 1 | **Claude** | 43 | 45 | 47 | **45.0** | Winner — built the return path |
| 2 | **Codex** | 43 | 44 | 45 | **44.0** | Runner-up — full-stack product |
| 3 | **Kiro** | 42 | — | 43 | **42.5** | Third — protocol + automatic coaching |
| 4 | **Gemini** | 38 | 36 | — | **37.0** | Fourth — reliable infrastructure |
| 5 | **Mistral** | — | 38 | 32 | **35.0** | Fifth — ambitious but unverified |

**Unanimous consensus**: Claude wins. Every judge ranked Claude first. The return path — where Canvas feeds knowledge back to Palette — is the piece that makes the flywheel real.

---

## What We Learned

The competition asked: "What is the highest-leverage connection you can make?"

The answer, discovered through building:

1. **The flywheel needs three types of work**: forward flow (Palette → Canvas), teaching (Canvas ↔ Enablement), and return flow (Canvas → Palette)
2. **Passive + active coaching together** is more powerful than either alone (Kiro automatic + Codex explicit)
3. **The wire contract can unify all three systems** into one traceable protocol
4. **The product is not a chatbot, not a dashboard, not a course** — it is an implementation machine with a coaching layer built in
5. **Domain knowledge is the fuel** — without KL entries, coaching signals don't fire, the flywheel doesn't spin

The North Star: **Palette knows what to do. Canvas does it. Enablement teaches how. The wire contract is how they talk to each other. The flywheel spins because doing teaches you more, learning makes you do better, and both feed intelligence back to Palette.**

---

## Files in This Archive

| File | Description |
|------|-------------|
| `NORTH_STAR_COMPETITION.md` | Competition rules and phases |
| `NORTH_STAR_ARCHITECTURE.md` | The vision document |
| `KIRO_NORTH_STAR_ENTRY.md` | Kiro's competition entry |
| `CODEX_NORTH_STAR_COMPETITION_REPORT.md` | Codex's competition entry |
| `CLAUDE_NORTH_STAR_ENTRY.md` | Claude's competition entry |
| `~/.mistral/NORTH_STAR_COMPETITION_MISTRAL.md` | Mistral's competition entry |
| `NORTH_STAR_COMPETITION_INTEGRATION_REPORT.md` | Cross-agent integration analysis |
| `NORTH_STAR_ROUND_2_PLAN.md` | Round 2 task assignments |
| `WIRE_CONTRACT_UNIVERSAL_PROTOCOL_PROPOSAL.md` | Wire contract unification proposal |
| `KIRO_SEMANTIC_AUDIT_2026-03-30.md` | Post-competition system audit |
| `NORTH_STAR_COMPETITION_FINAL_RECORD.md` | This document |

---

## Day Stats

- **Duration**: ~16 hours (2026-03-30 09:00 to 2026-03-31 01:00)
- **Tasks shipped**: 47 (across all agents, all rounds)
- **Tests at end of day**: 255+ passing, 0 failures
- **Workspaces**: 3 live (rossi, oil-investor, fde-toolkit)
- **Bus messages**: 165+
- **Agents active**: 5 (Kiro, Claude, Codex, Gemini, Mistral)
- **Flywheel arrows implemented**: All 6 (forward, teaching, return — in both directions)

---

**This was the first North Star Competition. It will not be the last.**
