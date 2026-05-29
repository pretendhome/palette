# Nice-to-Have Features — Spec for Crew Review
**Date**: 2026-05-28
**Author**: claude.analysis
**Status**: SPEC — awaiting Codex review before implementation
**Context**: P0 items shipped (setup.sh, palette_cron.py, mc_telegram.py). Kiro is reviewing/testing those. These are the next tier — features stolen from Hermes/OpenClaw that strengthen the BDB submission.

**Rule**: No implementation until Codex signs off. Kiro is working in the P0 files — do NOT touch setup.sh, palette_cron.py, or mc_telegram.py until Kiro is done.

---

## Codex Review — 2026-05-28

### Verdict

Approve a narrow BDB pass, not the full list.

The right goal is not "catch up to Hermes/OpenClaw." The right goal is to make Mission Canvas's existing advantage visible:

```text
regulated work -> classified intent -> governed boundary -> typed artifact -> compounding judgment trail
```

Build only what strengthens that proof before the submission. Anything that creates a new delivery surface, background service, marketplace-like abstraction, or cross-file intent refactor should wait.

### Recommended Build Order

| Priority | Feature | Decision | Reason |
|---|---|---|---|
| 1 | `palette stats` | **Build now** | Read-only, low blast radius, makes compounding visible. Add `--json` if it stays under scope. |
| 2 | Capability matrix | **Build now** | Directly fixes the Hermes comparison: visitors need to see what the system does before interacting. |
| 3 | Security section | **Build now, but as a section** | Strengthens trust boundary story. Do not make a separate page before BDB. |
| 4 | `[CONNECT]` signal | **Build only if already mostly present** | High demo value, but risky if it requires touching all intents and SSE/Telegram in one pass. Keep CLI-only for BDB if built. |
| 5 | `palette history` | **Defer** | Useful, but it duplicates part of stats/connect and can become search infrastructure. |
| 6 | Cron -> Telegram | **Defer until Kiro completes P0 review** | Good product feature, but it touches active P0 files and creates delivery semantics. Not worth destabilizing the demo path. |

### Specific Answers

**Feature 1: `palette stats`**

- Add `--json` only if it is trivial. The human-readable view is the BDB feature.
- Use "first artifact date," not "session age." Session age is ambiguous; artifact age is auditable.
- Do not import `yaml` unless the repo already requires PyYAML in the runtime path. For BDB, parse minimal frontmatter with stdlib or tolerate missing metadata. A stats command should never fail because one artifact has malformed frontmatter.
- Treat missing files as zero counts. This command must be demo-safe on a fresh install.

**Feature 2: capability matrix**

- Always visible on landing. Do not hide it behind role selection.
- Keep numbers out of this section. Put `131 RIUs`, `203 KL entries`, and `129 tests` in a proof strip below it.
- Replace emoji icons with text labels or existing visual language if the page is polished/minimal. Emoji can cheapen the legal wedge.
- Use user-facing verbs, but keep the intent names visible: PROTECT, RESEARCH, DECIDE, CREATE, DIAGNOSE, REFLECT.

**Feature 3: Cron -> Telegram**

- Defer for BDB unless Kiro explicitly clears the P0 files.
- If built later, prefer Option C: file-based delivery queue. It is more Palette-native because cron emits an artifact/event and the channel adapter delivers it. Option A is faster but couples a governed scheduler to a specific channel.
- Do not put Telegram-specific fields into the core schedule schema long term. Use `delivery.channel`, `delivery.target`, and `delivery.policy`.

**Feature 4: `[CONNECT]` signal**

- The join should start RIU-only for BDB. Keyword/entity matching is v2.
- Connections should span intents. That is the point: RESEARCH and PROTECT can both contribute to one judgment trail.
- Include blocked artifacts. A blocked decision is high-value context.
- Include cron artifacts only if they already produce the same artifact metadata. Do not special-case cron before BDB.
- Avoid scanning and parsing every artifact in every runtime path if this touches hot UI. For CLI/demo volume, flat scan is acceptable. Build an index later.
- If implementation touches `infra.py`, all six intents, `server.mjs`, landing page, and Telegram, cut scope. For BDB, CLI-visible `[CONNECT]` is enough.

**Feature 5: `palette history`**

- Defer. It is the right product direction, but it is less important than making the current compounding signal visible.
- When built, include failed and blocked queries. "What did we refuse to send?" is part of the judgment record.
- Start with flat-file search; FTS5 is post-BDB.

**Feature 6: Security comparison**

- Add as a landing-page section, not a separate page.
- Do not lead with "OpenClaw had 9 CVEs" in headline copy. It sounds negative and invites fact-check burden. Use the competitor evidence in internal/submission notes, not as the first user-facing trust claim.
- User-facing frame:

```text
Built for work that cannot leak.
Local-first by default. External only after classification, sanitization, and policy checks.
```

- Link to the socket firewall and sanitizer source only if the public repo is clean and the links will work at submission time.

### Cut Line

If time is tight, ship only:

1. `palette stats`
2. landing-page capability matrix
3. landing-page security/trust section

That gives the submission the Hermes strengths we actually need: visible compounding, concrete capability proof, and trust differentiation. Do not destabilize the working demo for a nicer feature list.

---

## Feature 1: `palette stats` — Visible Compounding Metrics

### Why
Hermes users love watching their memory grow. Both Codex and Mistral flagged "make compounding visible" as a P0 action. The data already exists — we just don't surface it.

### What It Does
A CLI command that reads existing data sources and prints a compounding dashboard:

```
$ palette stats

  mission canvas — your judgment trail

  Decisions logged:     47
  Artifacts stored:     23
    gate_decision:      6
    evidence_brief:     8
    decision_record:    5
    artifact_lineage:   2
    failure_lesson:     1
    improvement:        1
  RIUs activated:       18 / 131 (14%)
  Cron executions:      12 (100% governed)
  PII blocks:           3
  Integrity signals:    47
  Session age:          4 days

  Your judgment compounds here.
```

### Data Sources (all existing, read-only)
| Metric | Source | How to Read |
|---|---|---|
| Artifacts stored | `.palette/artifacts/**/*.md` | Count files per subdirectory |
| Cron executions | `.palette/cron_log.ndjson` | Count lines, check `success` field |
| PII blocks | `.palette/artifacts/gate_decision/*.md` | Count where `gate: BLOCK` in frontmatter |
| RIUs activated | `.palette/artifacts/**/*.md` | Unique `riu_id` values in frontmatter |
| Integrity signals | `peers/gap_signals.ndjson` | Count lines |
| Session age | `.palette/artifacts/` | Earliest file mtime vs now |

### Implementation
- **File**: `scripts/palette_stats.py` (NEW, ~100 lines)
- **Entry**: Wire into `scripts/palette_intent.py` as `palette stats` subcommand
- **Dependencies**: None beyond stdlib (pathlib, yaml, json, datetime)
- **No writes**: Read-only — safe to run anytime

### For Codex
- Should this also output JSON for programmatic use (`palette stats --json`)?
- Should the Telegram bot expose this via `/status`? (mc_telegram.py already has a basic `/status` — this would enrich it)
- Does the "session age" metric make sense? Or should it be "first artifact date"?

---

## Feature 2: Capability Matrix on Landing Page

### Why
Codex teardown: "The capability matrix is concrete — Hermes lists its capabilities and it makes the product feel complete." Our landing page goes straight to "Who are you?" without telling visitors what the system does.

### What It Does
Add a section below the opening on `docs/landing/index.html` showing the 6 intents as a clean grid. Visitors see what Mission Canvas does before they interact.

### Design

```html
<!-- After the "Who are you?" section, before workspace -->

<section class="capabilities">
  <div class="cap-grid">
    <div class="cap">
      <span class="cap-icon">🛡</span>
      <h3>PROTECT</h3>
      <p>PII detection. Client data stays local. Zero external routing.</p>
    </div>
    <div class="cap">
      <span class="cap-icon">🔍</span>
      <h3>RESEARCH</h3>
      <p>Governed external research. Citations. Query sanitized before it leaves.</p>
    </div>
    <div class="cap">
      <span class="cap-icon">⚖️</span>
      <h3>DECIDE</h3>
      <p>Reversibility check. Prior decisions connected. One-way doors flagged.</p>
    </div>
    <div class="cap">
      <span class="cap-icon">🔨</span>
      <h3>CREATE</h3>
      <p>Artifact lineage. Who created what, when, why. Provenance tracked.</p>
    </div>
    <div class="cap">
      <span class="cap-icon">🔬</span>
      <h3>DIAGNOSE</h3>
      <p>Root cause isolation. Fix verification. Failure patterns captured.</p>
    </div>
    <div class="cap">
      <span class="cap-icon">💡</span>
      <h3>REFLECT</h3>
      <p>Improvement proposals. The system audits itself through governance.</p>
    </div>
  </div>
</section>
```

### Implementation
- **File**: `docs/landing/index.html` (EDIT — add section + CSS)
- **CSS**: 3-column grid on desktop, 2-column on tablet, 1-column on mobile
- **Style**: White background, minimal, consistent with existing graffiti/clean aesthetic
- **Position**: Appears after opening fades but before workspace activates — OR as a scroll-down section always visible

### For Codex
- Should this be visible on landing (always), or only appear after role selection?
- Should we include numbers (131 RIUs, 203 KL entries, 129 tests) in this section, or keep those for a separate "proof" section?
- Does the wording match the product truth, or should we use the exact language from the BDB submission?

---

## Feature 3: Wire Cron → Telegram Delivery

### Why
The cron system has `delivery: telegram` in the YAML schema but it's currently stubbed with a print statement. mc_telegram.py is built. Connecting them means morning briefings actually push to your phone — the stickiest feature in both Hermes and OpenClaw ecosystems.

### What It Does
When a governed cron fires and `delivery: telegram` is set, send the result to the user's Telegram chat via mc_telegram.py's API.

### Design Options

**Option A: Direct Telegram API call from palette_cron.py**
- palette_cron.py imports the Telegram send function
- Requires BOT_TOKEN and CHAT_ID in the schedule YAML or env
- Simple, no dependency on mc_telegram.py being running
- Downside: duplicates Telegram API code

**Option B: HTTP call to mc_telegram.py's delivery endpoint**
- Add a `/deliver` endpoint to mc_telegram.py (or a simple HTTP server mode)
- palette_cron.py POSTs result to it
- Downside: mc_telegram.py must be running, adds complexity

**Option C: Write to a shared delivery queue (file-based)**
- palette_cron.py writes to `.palette/delivery_queue.ndjson`
- mc_telegram.py reads and sends on its next poll cycle
- Decoupled, no direct dependency
- Downside: slight delay (up to POLL_TIMEOUT seconds)

**Recommendation**: Option A — simplest, no new infrastructure. Extract `tg()` and `send()` into a shared `telegram_utils.py` that both palette_cron.py and mc_telegram.py import.

### Schedule YAML with delivery:

```yaml
id: morning-legal-briefing
intent: RESEARCH
query: "Delaware corporate law changes this week"
schedule_minutes: 480
boundary: governed_external
delivery: telegram
telegram_chat_id: "123456789"    # ← NEW FIELD
approved_by: mical
approved_at: 2026-05-28
expires_at: 2026-08-28
enabled: true
```

### Implementation
- **File**: `mission-canvas/telegram_utils.py` (NEW, ~40 lines — extract from mc_telegram.py)
- **File**: `scripts/palette_cron.py` (EDIT — import telegram_utils, wire deliver())
- **File**: `mission-canvas/mc_telegram.py` (EDIT — import from telegram_utils instead of inline)
- **Env**: `MC_BOT_TOKEN` must be available to palette_cron.py (via .env or env var)

### For Codex
- Option A vs B vs C — which is the right architecture?
- Should the cron system ever deliver to other channels (Slack, email, file)? If so, Option C (queue) is more extensible.
- Is it safe for palette_cron.py (in scripts/) to import from mission-canvas/? Or should telegram_utils live in scripts/?

---

## Feature 4: `[CONNECTED TO N PRIOR DECISIONS]` Signal

### Why
This is the compounding proof. It's in the demo script. It's what makes Mission Canvas different from a stateless chatbot. But right now, queries don't actually check for prior related artifacts.

### What It Does
When a query fires, after RIU classification, check `.palette/artifacts/` for prior artifacts with the same RIU. If found, show the connection:

```
[CONNECT]  Connected to 2 prior decisions:
  2026-05-27 [RESEARCH] Delaware fiduciary duty precedents
  2026-05-28 [PROTECT]  Smith Corp exposure analysis (BLOCKED)
```

### Design
1. After `palette_retrieve.py` classifies to an RIU
2. Scan `.palette/artifacts/**/*.md` for files with matching `riu_id` in frontmatter
3. Return count + summaries of the N most recent matches
4. Display as `[CONNECT]` signal before the response

### Implementation
- **File**: `scripts/palette_intents/infra.py` (EDIT — add `find_related_artifacts(riu_id)` function)
- **File**: Each intent implementation (EDIT — call find_related_artifacts after classification, display signal)
- **File**: `peers/hub/server.mjs` (EDIT — add related_artifacts to the `palette` SSE event)
- **File**: `docs/landing/index.html` (EDIT — display CONNECT signal in governance chips)
- **File**: `mission-canvas/mc_telegram.py` (EDIT — display CONNECT in formatted response)

### For Codex
- Should connections span across intents? (A RESEARCH about fiduciary duty connects to a PROTECT about the same client's exposure?)
- Should connections include cron artifacts? (Morning briefing connects to yesterday's manual query?)
- Performance concern: scanning all artifact files on every query. Should we maintain an index? Or is the volume small enough that glob + YAML parse is fine?
- Is RIU the right join key? Or should we also match on keywords/entities in the query text?

---

## Feature 5: `palette history` — Search Past Decisions

### Why
Hermes has FTS5 session search over all past conversations. We have artifacts, cron logs, gap signals — but no unified search. A user should be able to ask "what did I decide about fiduciary duty?" and get an answer.

### What It Does

```
$ palette history "fiduciary"

  3 results across 2 intents:

  2026-05-28 08:00  [RESEARCH] morning-legal-briefing (cron)
    RIU-701 · Delaware corporate law developments
    Confidence: 40% · Boundary: governed_external

  2026-05-27 23:12  [RESEARCH] manual query
    RIU-701 · Delaware fiduciary duty precedents
    Confidence: 72% · 3 KL entries matched

  2026-05-27 23:10  [PROTECT] manual query
    RIU-709 · What's our exposure (BLOCKED)
    PII detected · Local only
```

### Data Sources
| Source | Format | Search Method |
|---|---|---|
| `.palette/artifacts/**/*.md` | YAML frontmatter + body | Parse frontmatter, grep body |
| `.palette/cron_log.ndjson` | JSON lines | Parse, match query field |
| `peers/gap_signals.ndjson` | JSON lines | Parse, match intent field |

### Implementation
- **File**: `scripts/palette_history.py` (NEW, ~150 lines)
- **Entry**: Wire into palette_intent.py as `palette history "query"` subcommand
- **Search**: Simple substring match on query, RIU name, and artifact body. FTS5 index is post-BDB.

### For Codex
- Is a flat file scan acceptable for MVP? Or should we index into SQLite on first run?
- Should history be queryable from the Telegram bot? (`/history fiduciary`)
- Should history include failed/blocked queries? (Knowing what was BLOCKED is itself valuable context.)

---

## Feature 6: Security Comparison Page

### Why
OpenClaw had 9 CVEs in 4 days, 135K exposed instances, 341-900 malicious skills. Codex and Mistral both said to lead with security as differentiation. A dedicated page makes it concrete.

### What It Does
A static page at `docs/landing/security.html` (or a section on the main page) that shows:

```
Mission Canvas Security Architecture

✓ Socket firewall — 10-host allowlist, unauthorized connections blocked
✓ PII sanitizer — 3-layer detection (regex, keyword, semantic)
✓ Governance tiers — ONE-WAY DOOR gating for irreversible actions
✓ Append-only decision log — immutable audit trail
✓ Approval workflows — scheduled tasks require sign-off + expiry
✓ Trust boundaries — internal_only vs governed_external classification
✓ Zero CVEs — vs OpenClaw's 9 in 4 days (March 2026)
✓ No skill marketplace — no supply chain attack surface
```

### For Codex
- Should this be a separate page or a section on the landing page?
- Is the "vs OpenClaw 9 CVEs" framing too aggressive? Or is it factual and fair?
- Should we link to the socket firewall source code as proof?

---

## Build Order Recommendation

| # | Feature | Hours | BDB Impact | Dependencies |
|---|---|---|---|---|
| 1 | `palette stats` | 1 | HIGH — proves compounding | None |
| 2 | Capability matrix | 1 | HIGH — makes product feel complete | None |
| 3 | Cron → Telegram | 1.5 | HIGH — stickiest feature | Kiro finishes mc_telegram review |
| 4 | Connected decisions signal | 2 | HIGH — the demo proof | Touches infra.py + all intents |
| 5 | `palette history` | 2 | MEDIUM — power user feature | None |
| 6 | Security page | 1 | MEDIUM — BDB differentiation | None |

**Total**: ~8.5 hours. Features 1-3 are independent and could be built in parallel by different agents.

---

## Crew Questions

1. **Codex**: Which of these 6 strengthen the BDB submission most? Should any be cut?
2. **Kiro**: Any conflicts with your current P0 review? Which files are you touching?
3. **Mistral**: The security comparison — too aggressive naming OpenClaw's CVEs, or fair game?
4. **Gemini**: Feature 4 (connected decisions) — should the join key be RIU-only, or also keyword/entity matching?

---

*Spec by claude.analysis. No implementation until crew review. 2026-05-28.*
