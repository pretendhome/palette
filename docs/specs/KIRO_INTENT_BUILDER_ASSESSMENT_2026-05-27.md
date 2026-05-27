# Kiro Builder Assessment — Adaptive Intent Framework
**Date**: 2026-05-27
**Role**: Implementer / "feet on the ground"
**Question**: For each proposed intent, can I use this spec to build a working `palette <intent> <query>` command that runs end-to-end by June 2?

---

## Assessment Criteria

For each intent I ask:

1. **Can I build it?** — Is the cascade concrete enough to write code against?
2. **Does it produce a typed artifact?** — If not, it's chat, not an intent.
3. **What infrastructure exists today?** — What's already wired vs. what's new?
4. **What's the exit condition?** — How does the system know the intent is DONE?
5. **Does the BDB demo need it?** — If not, it's post-competition.
6. **Transition triggers** — Can I detect when this intent should hand off to another?

---

## The 9 Candidates

### 1. PROTECT ✅ SHIP

**Anxiety**: "I might leak something"
**Artifact**: `GateDecision` (ALLOW/BLOCK + reason + sanitized query if applicable)
**Existing infra**:
- `sanitizer.py` already strips PII (regex + pattern matching)
- `gateway.__init__.py` has `needs_external()` confidence gate
- `palette_query.py` step_route already checks classification before external call
- RIU-700 (privilege risk) exists in taxonomy

**What I'd build**:
```
palette protect "What's our exposure if the majority member was self-dealing?"
→ GateDecision { verdict: BLOCK, reason: "strategy language detected", pii_found: ["our exposure"], safe_rewrite: null }
```

**Exit condition**: GateDecision emitted. Either BLOCK (done) or ALLOW with sanitized query ready for RESEARCH.
**Transition**: PROTECT → RESEARCH (when query is safe to externalize)
**Build time**: ~4 hours. Mostly wiring existing sanitizer into a standalone command with typed output.
**Verdict**: Non-negotiable for BDB. This IS the demo's trust story.

---

### 2. RESEARCH ✅ SHIP

**Anxiety**: "I don't know what's true"
**Artifact**: `EvidenceBrief` (local knowledge + external evidence + synthesis + confidence)
**Existing infra**:
- `palette_query.py` full 5-step pipeline (RESOLVE→RETRIEVE→ROUTE→RESPOND→EXTRACT)
- `PerplexityGateway` with sanitization, caching, rate limiting, audit
- `palette_retrieve.py` hybrid FTS5 + keyword retrieval
- Knowledge Library (193 entries)

**What I'd build**:
```
palette research "What are the key Delaware LLC fiduciary duty cases?"
→ EvidenceBrief { local_knowledge: [...], external_evidence: [...], synthesis: "...", confidence: 85, sources: [...] }
```

**Exit condition**: EvidenceBrief emitted with confidence ≥ threshold. If confidence < 40, gap signal filed.
**Transition**: RESEARCH → DECIDE (when evidence is sufficient for judgment)
**Build time**: ~3 hours. Mostly reshaping existing `palette query --external` output into typed EvidenceBrief.
**Verdict**: Already 80% built. The gateway + query pipeline IS this intent.

---

### 3. DECIDE ✅ SHIP

**Anxiety**: "I don't know what to do"
**Artifact**: `DecisionRecord` (recommendation + evidence + counterargument + reversibility + checkpoint)
**Existing infra**:
- `decisions.md` append-only log (the pattern exists)
- ONE-WAY/TWO-WAY door classification (in palette-core.md, enforced by agents)
- `para_decision.py` script exists (parallel decision analysis)

**What I'd build**:
```
palette decide "Should Sarah settle or litigate?"
→ DecisionRecord { recommendation: "...", evidence: [...], counter: "...", reversibility: "TWO_WAY", checkpoint_required: false, rationale: "..." }
```

**Exit condition**: DecisionRecord emitted. If ONE-WAY DOOR detected → human checkpoint required before proceeding.
**Transition**: DECIDE → RESEARCH (when evidence is thin), DECIDE → CREATE (when decision implies building something)
**Build time**: ~6 hours. Need to wire local reasoning (Ollama) + evidence retrieval + structured output format. The `para_decision.py` gives me a starting point but needs the typed output.
**Verdict**: Essential for BDB Moment 3 (Sarah decides strategy). Distinct from RESEARCH — RESEARCH gathers, DECIDE judges.

---

### 4. CREATE ✅ SHIP

**Anxiety**: "I need something real"
**Artifact**: `ArtifactLineage` (spec + artifact + tests + provenance)
**Existing infra**:
- Builder agent exists (agents/builder/)
- Remediation loop (validator→debugger→builder) is wired
- SDK agent_base provides structured execution

**What I'd build**:
```
palette create "Draft a client update memo for the fiduciary case"
→ ArtifactLineage { spec: "...", artifact: "./artifacts/client-update-2026-05-27.md", tests: ["tone_check", "privilege_check"], provenance: { sources: [...], models_used: [...] } }
```

**Exit condition**: Artifact exists on disk, passes validation checks, provenance logged.
**Transition**: CREATE → DIAGNOSE (when output fails tests), CREATE → PROTECT (before publishing externally)
**Build time**: ~8 hours. The builder agent exists but doesn't produce typed ArtifactLineage. Need to add spec→build→verify loop with structured output.
**Verdict**: Ship. Every professional needs "make me a thing." But this is the hardest one to make feel polished in 5 days.

---

### 5. DIAGNOSE ⚠️ SHIP (MINIMAL)

**Anxiety**: "Something is wrong"
**Artifact**: `FailureLesson` (failure + repro + root_cause + fix + tests + lesson)
**Existing infra**:
- Debugger agent v2 (agents/debugger/) — 22 tests passing
- Remediation loop (validator→debugger→builder) wired and tested
- `test_loop.py` integration test exists

**What I'd build**:
```
palette diagnose "Why did the privileged query route externally?"
→ FailureLesson { failure: "...", repro: "...", root_cause: "...", fix: "...", tests_added: [...], lesson: "..." }
```

**Exit condition**: Fix verified (tests pass), lesson stored.
**Transition**: DIAGNOSE → CREATE (when fix requires new capability), DIAGNOSE → RESEARCH (when root cause is unknown)
**Build time**: ~5 hours. Debugger agent does the work; I need to wrap it in the typed output and add the "lesson" storage step.
**Verdict**: Ship minimal. The remediation loop already works. Typed output wrapper is the gap.

---

### 6. TEACH ❌ CUT (for BDB)

**Anxiety**: "I don't understand"
**Artifact**: `LearnerState` (level + misconceptions + next_step + progress)
**Existing infra**:
- Enablement system exists (separate repo)
- ARON adaptive learning architecture exists
- No `palette teach` command or learner state tracking in the main system

**What I'd need to build**:
- Learner state model (new)
- Adaptive session logic (new)
- Assessment/check-understanding loop (new)
- Competency tracking (new)

**Exit condition**: Learner demonstrates understanding (how? assessment rubric needed — doesn't exist)
**Build time**: ~20+ hours. This is a product unto itself.
**Verdict**: CUT from BDB. This is the enablement product, not the OS demo. The BDB demo doesn't have a teaching moment. Post-competition.

---

### 7. EXPLAIN ❌ CUT (absorbed into CREATE)

**Anxiety**: "They won't understand"
**Artifact**: `FramingRecord` (audience + versions + framing_rationale)
**Existing infra**:
- Narrator agent exists (agents/narrator/)
- Person lenses exist (30 lenses)
- No standalone `palette explain` command

**The problem**: EXPLAIN is CREATE with an audience constraint. The cascade is:
```
classify audience → retrieve context → frame → draft → critique → refine → store
```

That's just `palette create --audience "judge" "explain the fiduciary breach"`. The audience parameter is a modifier on CREATE, not a separate intent.

**Exit condition**: Audience-appropriate artifact produced. Same as CREATE.
**Build time**: If separate: ~8 hours. If folded into CREATE with `--audience` flag: ~2 hours incremental.
**Verdict**: CUT as standalone. Fold into CREATE as `--audience` parameter. The narrator agent provides the framing logic.

---

### 8. MONITOR ❌ CUT (for BDB)

**Anxiety**: "I need to know what changed"
**Artifact**: `SignalPacket` (what_changed + why_it_matters + affected_rius + confidence + recommended_intent)
**Existing infra**:
- ERS (External Reality Service) exists and runs
- `gap_signals.ndjson` accumulates signals
- Joseph bot monitors exist
- Health check runs periodically

**The problem**: MONITOR is a background process, not a user-invoked intent. You don't say "palette monitor" — you configure it and it runs. It's cron, not a command.

**Exit condition**: Signal detected above threshold → alert emitted. But when is MONITOR "done"? Never. It's a daemon.
**Build time**: ~12 hours to make it a proper daemon with configurable watchlists.
**Verdict**: CUT from BDB. It's infrastructure, not a demo moment. The ERS already does this — it just doesn't produce typed SignalPackets yet. Post-competition.

---

### 9. REFLECT ✅ SHIP (MINIMAL)

**Anxiety**: "I don't want to lose the lesson"
**Artifact**: `ImprovementProposal` (what_happened + pattern + proposed_change + status)
**Existing infra**:
- `auto_enrich.py` exists (proposes KL entries from gap signals)
- Health check produces improvement proposals
- Gap signals accumulate in `gap_signals.ndjson`
- Wiki governance pipeline (propose → vote → promote)

**What I'd build**:
```
palette reflect "What did we learn from today's BDB sprint?"
→ ImprovementProposal { session_summary: "...", patterns: [...], proposed_changes: [...], promoted: [], provisional: [...] }
```

**Exit condition**: ImprovementProposal emitted. Proposed changes filed (KL proposals, RIU proposals, or governance proposals).
**Transition**: REFLECT → CREATE (when lesson should become a template/recipe)
**Build time**: ~4 hours. Wire existing auto_enrich + gap_signals into a structured reflection command.
**Verdict**: Ship minimal. This is the compounding story — "Palette gets better with use." Important for the thesis even if the demo doesn't show it live.

---

## Summary Table

| Intent | Ship? | Build Hours | BDB Demo? | Artifact | Notes |
|---|---|---|---|---|---|
| **PROTECT** | ✅ YES | 4h | Moment 1 | GateDecision | Non-negotiable |
| **RESEARCH** | ✅ YES | 3h | Moment 2 | EvidenceBrief | 80% exists |
| **DECIDE** | ✅ YES | 6h | Moment 3 | DecisionRecord | Core of "judgment OS" |
| **CREATE** | ✅ YES | 8h | Post-demo | ArtifactLineage | Hardest to polish |
| **DIAGNOSE** | ⚠️ MINIMAL | 5h | Not in demo | FailureLesson | Remediation loop wrapping |
| **REFLECT** | ⚠️ MINIMAL | 4h | Thesis only | ImprovementProposal | Compounding story |
| **TEACH** | ❌ CUT | 20h+ | No | LearnerState | Separate product |
| **EXPLAIN** | ❌ CUT | — | No | — | Absorbed into CREATE --audience |
| **MONITOR** | ❌ CUT | 12h | No | — | Background daemon, not intent |

**Total build time for shippable set: ~30 hours across 5 days = doable.**

---

## My Final Position: 6 Intents Ship

```
PROTECT → RESEARCH → DECIDE → CREATE → DIAGNOSE → REFLECT
```

Plus GOVERN as a hidden OS primitive (for taxonomy/governance changes — already exists as the wiki governance pipeline, just needs a command wrapper).

### Why 6, not 5 or 9:

- **Not 5**: Dropping CREATE means the system can think but not build. That's a chatbot, not an OS.
- **Not 9**: TEACH, EXPLAIN, MONITOR have no path to working `palette <intent>` commands by June 2. Shipping stubs damages credibility more than shipping fewer polished intents.
- **6 is honest**: Each one runs end-to-end, produces a typed artifact, and has a clear exit condition.

### The transition matrix (what makes it an OS):

```
PROTECT  → RESEARCH    (sensitive facts become safe public query)
RESEARCH → DECIDE      (evidence is enough to judge)
DECIDE   → RESEARCH    (evidence is thin)
DECIDE   → CREATE      (decision implies building)
CREATE   → DIAGNOSE    (output fails)
DIAGNOSE → CREATE      (root cause is bounded, fix is a new thing)
DIAGNOSE → RESEARCH    (root cause is unknown)
REFLECT  → CREATE      (lesson becomes template/recipe)
```

### For BDB demo specifically:

Sarah's morning maps to exactly 3 of the 6:
1. **PROTECT** — "What's our exposure?" → BLOCKED, local only
2. **RESEARCH** — "What are the Delaware fiduciary cases?" → Perplexity, sanitized
3. **DECIDE** — Strategy synthesis → local, connects to prior research

The other 3 (CREATE, DIAGNOSE, REFLECT) are visible in the product thesis but not in the 2-minute demo.

---

## What's Missing From Both Specs (Claude's and Codex's)

Neither spec gives me what I actually need to build:

1. **Exact CLI interface** — `palette protect <query>` or `palette --intent protect <query>`?
2. **Typed output schema** — What fields does each artifact MUST have? (I proposed them above but need confirmation)
3. **Error states** — What happens when PROTECT can't classify? When RESEARCH gets no results? When DECIDE has insufficient evidence?
4. **Storage format** — Where do artifacts go? `./artifacts/`? SQLite? Bus memory?
5. **Checkpoint implementation** — The "Palette Checkpoint" between steps is described conceptually but has no code path. Is it a function call? A bus message? A state machine transition?

### My proposal for checkpoint implementation:

```python
def palette_checkpoint(state: IntentState) -> IntentState:
    """Between every model call, check if intent should shift."""
    if state.governance_changed():
        return state.transition_to(PROTECT)
    if state.confidence_sufficient():
        return state.transition_to(DECIDE)
    if state.artifact_failed():
        return state.transition_to(DIAGNOSE)
    return state  # continue current intent
```

That's 10 lines. The checkpoint is a function, not a framework.

---

## Decision Needed

🚨 **ONE-WAY DOOR**: The intent count and set determines what gets built in the next 5 days.

**My recommendation**: Ship 6 (PROTECT, RESEARCH, DECIDE, CREATE, DIAGNOSE, REFLECT).
**Confirm or override**, then I start building PROTECT (4 hours, highest demo priority).

---

*— kiro.design, 2026-05-27T10:41 PDT*
