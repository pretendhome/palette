# Intent Framework — Crew Convergence Report
## Serial Synthesis of 5 Agent Positions
**Date**: 2026-05-27
**Synthesizer**: claude.analysis
**Status**: READY FOR CREW VOTE
**Tag**: BDB-INTENTS-FINAL

---

## The Question

How many intents ship for BDB? Which ones? What's the design language?

---

## Five Positions Received

| Agent | Count | Cut | Key Insight |
|---|---|---|---|
| **Claude** (original spec) | 8 core + 3 sub | — | Exhaustive lens-based generation, merge table |
| **Codex** (creative expansion) | 9 core + 3 hidden | — | Intent = anxiety relief. Transition matrix = the product. Experience Objects = memory substrate |
| **Kiro** (builder assessment) | 6 ship | TEACH, EXPLAIN, MONITOR | 30 hours / 5 days. Checkpoint is 10 lines. EXPLAIN folds into CREATE --audience |
| **Gemini** (sandbox analysis) | 5 for BDB | TEACH, COMMUNICATE, EVALUATE | TEACH is high blast-radius (recursive loop, state decay). CONVERGE/CREATE/DIAGNOSE are billion-dollar intents |
| **Mistral** (pragmatic review) | Endorses Codex base | Wants implementation priority | "Ne créons pas des choses qui ne sont pas nécessaires" |

---

## Where Everyone Agrees

These 5 points had zero dissent across all agents:

1. **PROTECT, RESEARCH, DECIDE, CREATE, DIAGNOSE, REFLECT** are core — every agent includes all six in some form
2. **TEACH is cut for BDB** — Gemini proved it's high blast-radius (state decay, recursive loops), Kiro estimated 20+ hours, no demo moment exists for it
3. **The transition matrix is the product** — Kiro, Codex, and the operator all independently identified this. Palette knowing when RESEARCH should become DECIDE is the OS behavior
4. **Typed Experience Objects** — every intent produces a named artifact (GateDecision, EvidenceBrief, DecisionRecord, ArtifactLineage, FailureLesson, ImprovementProposal). Chat is not an intent.
5. **Codex's conceptual framework is the design language** — anxiety mapping, verb-first entry, intent-as-boundary-contract, intent-as-memory-shape

---

## Where Agents Disagree (3 Disputes)

### Dispute 1: EXPLAIN — separate intent or CREATE modifier?

| Position | Agent | Argument |
|---|---|---|
| **Separate** | Codex | Different cascade, different anxiety ("they won't understand" ≠ "I need something real"), produces FramingRecord not ArtifactLineage |
| **Fold into CREATE** | Kiro | Same cascade with audience constraint. `palette create --audience "judge"` is cleaner. Narrator agent provides framing. 0 additional build hours vs 8 |

**Resolution**: **Fold into CREATE for BDB. Promote to separate intent post-competition if usage patterns justify it.**

Reasoning: Kiro is right that the cascade is nearly identical, and we can't spend 8 hours on something the demo doesn't need. But Codex is right that the anxiety is different — "they won't understand" is a real professional fear distinct from "I need something real." The `--audience` flag captures the behavior. If post-BDB usage shows people reaching for EXPLAIN as a natural verb, it graduates.

### Dispute 2: MONITOR — core intent, daemon, or cut?

| Position | Agent | Argument |
|---|---|---|
| **Core intent** | Codex | Produces SignalPacket, anxiety = "I need to know what changed", governance defaults exist |
| **Daemon, not intent** | Kiro | "When is MONITOR done? Never." Background process with no exit condition. Already built as ERS + Joseph bot monitors |
| **Cut for BDB** | Gemini | Not in failure density analysis. No demo moment |

**Resolution**: **Cut from BDB intent set. Remains as infrastructure (ERS, monitors). Post-competition: evaluate whether `palette monitor` as a user command makes sense.**

Reasoning: Kiro's question "when is MONITOR done?" is the killer argument. An intent has an exit condition. A daemon doesn't. MONITOR is real infrastructure — it already runs — but it's not a user-invoked intent in the same way PROTECT or RESEARCH are. The typed SignalPacket is valuable and should inform other intents (MONITOR → DECIDE transition), but the monitoring itself is infrastructure, not experience layer.

### Dispute 3: GOVERN — add or not?

| Position | Agent | Argument |
|---|---|---|
| **Add as hidden OS primitive** | Kiro | Meta-intent for changing system rules (add RIU, modify governance, update taxonomy). Missing from all 30. Already exists as wiki governance pipeline |
| **Not mentioned** | Everyone else | — |

**Resolution**: **Add GOVERN as 4th hidden OS primitive alongside CHECKPOINT, STORE, TRANSLATE.**

Reasoning: Kiro is right that it's missing and already built. The wiki governance pipeline (propose → vote → promote) IS the GOVERN intent. It doesn't need a `palette govern` command — it runs through the governance pipeline. But naming it as a primitive makes the architecture legible.

---

## The Converged Design

### 6 User-Facing Intents

| # | Intent | Anxiety | Artifact | Build Hours | BDB Demo |
|---|---|---|---|---|---|
| 1 | **PROTECT** | I might leak something | `GateDecision` | ~4h | Moment 1 |
| 2 | **RESEARCH** | I don't know what's true | `EvidenceBrief` | ~3h | Moment 2 |
| 3 | **DECIDE** | I don't know what to do | `DecisionRecord` | ~6h | Moment 3 |
| 4 | **CREATE** | I need something real | `ArtifactLineage` | ~8h | Thesis |
| 5 | **DIAGNOSE** | Something is wrong | `FailureLesson` | ~5h | Thesis |
| 6 | **REFLECT** | I don't want to lose the lesson | `ImprovementProposal` | ~4h | Thesis |

**Total: ~30 hours. 5 days. Doable.**

### 4 Hidden OS Primitives

| Primitive | What It Does | Already Built? |
|---|---|---|
| **CHECKPOINT** | Between every model call: classification held? governance shifted? intent changed? | Kiro: 10-line function |
| **STORE** | Every intent ends with governed storage + compounding | Session log, decisions.md, gap signals |
| **TRANSLATE** | Cross-domain concept mapping (happens inside everything) | Founder's core skill, implicit in taxonomy |
| **GOVERN** | Modify system rules (add RIU, update taxonomy, governance changes) | Wiki governance pipeline |

### 3 Deferred Intents (Post-BDB)

| Intent | Why Deferred | When to Revisit |
|---|---|---|
| **TEACH** | High blast-radius (Gemini), 20+ hours (Kiro), separate product | When enablement product gets its own surface |
| **EXPLAIN** | Absorbed into CREATE --audience for now | If usage shows people reaching for "explain" as distinct from "create" |
| **MONITOR** | Infrastructure, not user intent. No exit condition | When `palette monitor` as user command makes sense |

---

## The Transition Matrix (The Product)

This is what makes Palette an OS, not a tool. Each transition has a **trigger condition** that the checkpoint function detects:

```
PROTECT  → RESEARCH     trigger: query sanitized, safe for external
RESEARCH → DECIDE       trigger: evidence confidence ≥ threshold
DECIDE   → RESEARCH     trigger: evidence confidence < threshold
DECIDE   → CREATE       trigger: decision implies building an artifact
CREATE   → DIAGNOSE     trigger: artifact fails validation/tests
CREATE   → PROTECT      trigger: artifact contains sensitive content before publish
DIAGNOSE → CREATE       trigger: root cause bounded, fix is a new artifact
DIAGNOSE → RESEARCH     trigger: root cause unknown, need more evidence
REFLECT  → CREATE       trigger: lesson should become a template/recipe
REFLECT  → RESEARCH     trigger: pattern needs external validation
REFLECT  → GOVERN       trigger: lesson proposes source-of-truth, taxonomy, recipe, or governance change
```

### Checkpoint Implementation (per Kiro)

```python
def palette_checkpoint(state: IntentState) -> IntentState:
    """Between every model call, check if intent should shift."""
    card = integrity_card(state.riu)  # existing engine
    if card.posture == "blocked_by_boundary":
        return state.transition_to(PROTECT)
    if card.posture == "governance_required":
        return state.transition_to(GOVERN)
    if state.governance_changed():
        return state.transition_to(PROTECT)
    if state.confidence_sufficient():
        return state.transition_to(DECIDE)
    if state.artifact_failed():
        return state.transition_to(DIAGNOSE)
    return state  # continue current intent, posture attached
```

---

## The Product Grammar (per Codex, updated per Codex addendum)

```
User intent  →  RIU classification  →  trust boundary  →  integrity card  →  recipe/tool path  →  artifact  →  memory update  →  integrity signal
```

- The intent is what the user **feels**
- The RIU is what Palette **knows**
- The trust boundary is what Palette **protects**
- The integrity card is what Palette **checks**
- The recipe is how Palette **executes**
- The model cascade is how Palette **thinks**
- The artifact is what the user **gets**
- The memory update is why **tomorrow is better**

---

## The Positioning Line (per operator)

```
from prompts    to intents
from chats      to artifacts
from tools      to recipes
from memory     to typed experience
from automation to governed judgment
```

---

## Integrity Engine: The Validation Spine (per Codex addendum)

The intent layer should not bypass Palette's existing integrity engine. It should make the integrity engine central.

Before intents, the default failure mode was: user asks → agent reasons independently → agent builds directly → Palette's ontology, recipes, routing, and integrity are bypassed. Intents fix the entry point. The integrity engine fixes the alignment.

Before each intent executes, Palette asks the integrity engine for an **RIU integrity card**: classification, knowledge coverage, routing coverage, recipe coverage, people/tool signals, completeness, gaps, and recommended actions. This gives every intent an **execution posture**:

| Posture | Meaning |
|---|---|
| `execute` | RIU, boundary, knowledge, routing, and recipe coverage are sufficient |
| `execute_with_limitations` | Palette can act, but must disclose known gaps |
| `narrow_or_confirm` | Classification confidence, boundary, or recipe coverage is weak |
| `research_or_reflect_first` | Palette lacks sufficient knowledge or recipe coverage to act directly |
| `blocked_by_boundary` | Trust boundary prevents requested execution path |
| `governance_required` | Source-of-truth, taxonomy, recipe, or policy mutation requires GOVERN |

### Integrity Check Per Intent

| Intent | Integrity Engine Question | Failure Prevention |
|---|---|---|
| `PROTECT` | Is this RIU classified as internal-only, both, or governed external? Are privacy/compliance RIUs implicated? | Prevents accidental external calls |
| `RESEARCH` | Does this RIU have knowledge coverage, routing, and validated external recipe support? | Prevents generic web searching and unsupported synthesis |
| `DECIDE` | Is evidence coverage sufficient? Are one-way-door/governance RIUs implicated? | Prevents decision laundering and unsupported recommendations |
| `CREATE` | Does the RIU have an artifact contract and recipe path? Are service recipes present if external tools are used? | Prevents generic artifact generation outside Palette patterns |
| `DIAGNOSE` | Is this failure tied to a known RIU, prior lesson, recipe gap, or routing/integrity gap? | Prevents patching symptoms without root cause |
| `REFLECT` | Should the lesson become a KL proposal, recipe update, RIU proposal, or governance change? | Prevents memory contamination and unreviewed source-of-truth mutation |

### Why This Is Low-Lift

The integrity engine already exists (`integrity.py`, `health_check.py`, `total_health_check.py`). The BDB scope is:

1. `PROTECT` blocks or sanitizes before external calls
2. `RESEARCH` checks whether the RIU is allowed to use governed external routing
3. `DECIDE` checks whether the evidence brief exists and whether the matter remains local
4. `REFLECT` cannot mutate source-of-truth directly; it emits an `ImprovementProposal` or GOVERN handoff

The remaining intents can use stubbed integrity cards until post-BDB hardening. This makes the demo more credible without increasing build scope.

### The Full Architecture Line

```
Intent is the front door.
RIU is the semantic spine.
Integrity is the alignment check.
Recipe is the execution path.
Artifact is the user-visible result.
Memory is the compounding layer.
Governance is the source-of-truth boundary.
```

---

## BDB Demo Mapping

Sarah's morning maps to exactly 3 of the 6:

| Demo Moment | Intent | Trust Boundary | Model | Artifact |
|---|---|---|---|---|
| "What's our exposure if the majority member was self-dealing?" | **PROTECT** | local_only | Ollama | GateDecision: BLOCKED |
| "What fiduciary duty standards apply to LLC co-founders in Delaware?" | **RESEARCH** | governed_external | Perplexity | EvidenceBrief |
| "Given what we found, what would opposing counsel argue?" | **DECIDE** | local (connects to prior) | Claude/Ollama | DecisionRecord |

The other 3 (CREATE, DIAGNOSE, REFLECT) live in the product thesis. The demo stays focused: "Palette knew when Sarah was protecting, when she was researching, and when she was deciding."

---

## Risk Register (from Gemini's Sandbox Analysis)

| Intent | Risk Level | Primary Failure Mode | Mitigation |
|---|---|---|---|
| PROTECT | 🟢 LOW | False positive blocking | Confidence threshold tuning |
| RESEARCH | 🔵 LOW | Source saturation | Authority ranking (already built) |
| DECIDE | 🟡 MEDIUM | Insufficient evidence for judgment | Transition to RESEARCH when thin |
| CREATE | 🟢 MEDIUM | Spec drift (artifact ≠ requirement) | Validation check at exit |
| DIAGNOSE | 🟡 HIGH | Attribution error (fixing symptom not cause) | 5-whys in cascade |
| REFLECT | 🟡 HIGH | Feedback loop contamination (bad data → bad RIUs) | Human-in-the-loop for all taxonomy changes |

---

## Build Priority (for Kiro)

| Order | Intent | Why This Order | Hours |
|---|---|---|---|
| 1 | PROTECT | Highest demo priority, smallest build, non-negotiable for trust story | 4h |
| 2 | RESEARCH | 80% already built, reshape existing pipeline into typed output | 3h |
| 3 | DECIDE | Core of "judgment OS" claim, needs RESEARCH working first | 6h |
| 4 | REFLECT | Compounding story, wires into existing auto_enrich | 4h |
| 5 | DIAGNOSE | Remediation loop wrapping, existing debugger agent | 5h |
| 6 | CREATE | Hardest to polish, least demo-critical | 8h |

---

## Gemini Integrity Validation: 5 Systemic Fixes (per Specialist re-run)

Gemini re-ran the sandbox simulation with the integrity engine in the loop. Result: the integrity card eliminates most generic failure modes but introduces 5 new structural risks that need hardening.

### Fix 1: Post-Recipe Integrity Signal Loop (The Phantom Recipe)

**Problem**: Static integrity cards can't know if a recipe is broken at runtime. Perplexity API key revoked? Card still says `execute`. Recipe crashes mid-flight.

**Fix**: Recipe failure emits `recipe_failure` integrity signal → ephemeral card updates to `execute_with_limitations` → transitions to DIAGNOSE. The integrity card becomes a living document, not a static stamp.

**BDB impact**: Low. Perplexity is the only external recipe in the demo path. Wrap in try/catch with graceful degradation.

### Fix 2: UNVALIDATED_FALLBACK (The Bureaucratic Blocker)

**Problem**: If integrity returns `research_or_reflect_first` because coverage is thin, the OS refuses to answer. User gets a gap signal instead of help.

**Fix**: Log the gap (background STORE), but still attempt base-model reasoning (`local_only`). Tag the artifact: `status: UNVALIDATED_FALLBACK`. User progresses; OS stays honest.

**BDB impact**: Critical for demo. Sarah's niche legal question may not have full KL coverage. The system must answer with a warning, not refuse.

### Fix 3: Integrity Re-evaluation Hooks (The Mid-Flight Boundary Shift)

**Problem**: Integrity stamps `execute` for RESEARCH. During execution, PROTECT detects PII in intermediate context. Boundary downgrades to `local_only`. But the Perplexity recipe is already in flight.

**Fix**: The integrity card is active state, not a one-time stamp. Recipe runner checks the card immediately before every network request. If boundary changed → abort cleanly with `blocked_by_boundary`.

**BDB impact**: High. This is the core trust story. "Nothing leaked" must be provably true even under mid-flight boundary shifts.

### Fix 4: Recipe Adapter Layer (The Bad Handoff)

**Problem**: Recipes return raw JSON/strings. Artifacts require strict Pydantic schemas. Mismatch causes validator rejection → CREATE→DIAGNOSE loops.

**Fix**: Every recipe implements a standard adapter interface that maps output to the required artifact contract. Integrity checks: "Does this recipe have an adapter for EvidenceBrief?" If no → `execute_with_limitations`.

**BDB impact**: Medium. The Perplexity recipe needs an EvidenceBrief adapter. One adapter, ~50 lines.

### Fix 5: Affinity Over People Signals (The Cult of Personality)

**Problem**: People signals ("founder prefers Gamma") could override domain safety. A confidential legal document routes to external SaaS because it scored high on people signals.

**Fix**: `intent_recipe_affinity` takes strict precedence over `people_signals`. Affinity = "is this safe and appropriate for this boundary and RIU." People signals = "is this tool generally viable."

**BDB impact**: Low. No people signal conflicts in the Sarah demo path.

### Updated Execution Grammar (Final)

```
1. User intent [classified]
2. RIU [mapped]
3. Trust boundary [set via PROTECT]
4. Integrity Card [evaluated against RIU + boundary + affinity]
   ↳ IF posture == research_or_reflect_first: emit gap signal, degrade to UNVALIDATED_FALLBACK
5. Recipe/Tool [executed]
   ↳ IF boundary downgraded mid-flight: abort execution
   ↳ IF recipe fails: emit recipe_failure signal, transition to DIAGNOSE
   ↳ Recipe output flows through adapter
6. Artifact [generated & validated against strict schema]
7. Memory [stored in scoped .palette/artifacts/ with PII masking]
8. Integrity Signal [emitted: recipe success/fail updates future integrity cards]
```

---

## Mistral Implementation Guardrails (per INTENT_ADDENDUM_IMPLEMENTATION_GUARDRAILS.md)

Mistral formalized Gemini's findings into actionable build contracts:

### Open Questions Resolved

| Question | Resolution | Source |
|---|---|---|
| CLI interface | `palette protect <query>` — subcommands as verbs, not flags | Gemini |
| Storage format | `.palette/artifacts/<intent_type>/<timestamp>.md` with YAML frontmatter | Gemini + Mistral |
| Error states | PROTECT can't classify → default `local_only`. RESEARCH returns nothing → auto-transition to REFLECT | Gemini |
| FIX vs DIAGNOSE | DIAGNOSE canonical, `fix` as CLI alias | Gemini |

### Artifact Schema Contracts

| Artifact | Required Fields | Validation Rule |
|---|---|---|
| GateDecision | `boundary`, `action`, `blocked_entities`, `redaction_map` | `blocked_entities` non-empty if `action = BLOCK` |
| EvidenceBrief | `local_canon`, `external_delta`, `contradictions` | `contradictions` cannot overwrite `local_canon` |
| DecisionRecord | `recommendation`, `strongest_counterargument`, `change_my_mind_trigger` | `counterargument` > 50 words |
| ArtifactLineage | `spec`, `constraints`, `iterations`, `max_iterations` | `max_iterations <= 3` |
| FailureLesson | `symptom`, `five_whys`, `root_cause_isolated` | `five_whys.length == 5` AND `root_cause_isolated == true` |
| ImprovementProposal | `lesson`, `proposed_action`, `target_file` | `target_file` must be in `wiki/proposed/` |

### System-Level Guardrails

- **Context Firewall**: On intent transition to lower security tier → purge raw text of higher-tier artifacts from active prompt, replace with blinded references
- **Checkpoint Semaphores**: `palette_checkpoint()` fully synchronous, thread-locked per session. Priority: PROTECT > DIAGNOSE > RESEARCH > DECIDE > CREATE > REFLECT
- **Transition Depth Limit**: `transition_depth > 2` → `halt_and_escalate("Recursive Intent Oscillation")`

---

## What This Report Resolves

- [x] Intent count: **6 user-facing + 4 hidden OS primitives**
- [x] Which intents: PROTECT, RESEARCH, DECIDE, CREATE, DIAGNOSE, REFLECT
- [x] What's cut: TEACH, EXPLAIN (→ CREATE), MONITOR (→ infrastructure)
- [x] What's added: GOVERN (hidden primitive, per Kiro)
- [x] Design language: Codex's anxiety mapping + experience objects + product grammar
- [x] Transition matrix: 11 governed transitions with trigger conditions (including REFLECT → GOVERN)
- [x] Checkpoint: function with integrity card + re-evaluation hooks (per Kiro + Codex + Gemini)
- [x] Integrity engine: validation spine with 6 execution postures + 5 systemic fixes (per Codex + Gemini)
- [x] Build order: PROTECT → RESEARCH → DECIDE → REFLECT → DIAGNOSE → CREATE
- [x] Risk register: from Gemini's sandbox analysis (original + integrity re-run)
- [x] BDB demo fit: 3 of 6 intents visible (PROTECT, RESEARCH, DECIDE)
- [x] CLI interface: `palette <intent> <query>` — subcommands as verbs (per Gemini)
- [x] Storage format: `.palette/artifacts/<intent_type>/<timestamp>.md` with YAML frontmatter (per Gemini + Mistral)
- [x] Error states: PROTECT defaults `local_only`, RESEARCH auto-transitions to REFLECT (per Gemini)
- [x] Naming: DIAGNOSE canonical, `fix` as alias (per Gemini)
- [x] Artifact schemas: 6 strict Pydantic contracts with validation rules (per Mistral)
- [x] System guardrails: context firewall, checkpoint semaphores, transition depth limit (per Mistral)

## What Remains

- [ ] **Crew vote**: Confirm the 6 intents + architecture. This report represents convergence across all 5 agents.
- [ ] **Kiro build**: Start with PROTECT (4h), highest demo priority, smallest build
- [ ] **Perplexity adapter**: EvidenceBrief adapter for the Perplexity recipe (~50 lines)
- [ ] **UNVALIDATED_FALLBACK**: Implement for BDB demo path (Sarah's niche legal questions)

---

## Source Documents

| Document | Author | Location |
|---|---|---|
| Adaptive Intent Framework (30 intents) | Claude | `palette/docs/specs/ADAPTIVE_INTENT_FRAMEWORK.md` |
| Creative Expansion (15 iterations) | Codex | `palette/docs/specs/CODEX_ADAPTIVE_INTENT_EXPANSION_2026-05-27.md` |
| Builder Assessment (6 ship) | Kiro | `palette/docs/specs/KIRO_INTENT_BUILDER_ASSESSMENT_2026-05-27.md` |
| Sandbox Analysis (original 8) | Gemini | `.gemini/tmp/.../INTENT_VALIDATION_FINAL_6.md` |
| Integrity Engine Addendum | Codex | `palette/docs/specs/CODEX_INTEGRITY_ENGINE_INTENT_ADDENDUM_2026-05-27.md` |
| Integrity Validation (re-run) | Gemini | `.gemini/tmp/.../INTEGRITY_ENGINE_VALIDATION_2026-05-27.md` |
| Implementation Guardrails | Mistral | `palette/docs/specs/INTENT_ADDENDUM_IMPLEMENTATION_GUARDRAILS.md` |
| **This convergence report** | Claude | `palette/docs/specs/INTENT_CONVERGENCE_REPORT_2026-05-27.md` |

---

*Synthesized by claude.analysis from 5 crew positions (Claude, Codex, Kiro, Gemini, Mistral) + Codex integrity engine addendum + Gemini integrity validation re-run + Mistral implementation guardrails. The convergence followed the relay pattern: exhaustive generation (Claude) → creative expansion (Codex) → builder reality check (Kiro) → risk analysis (Gemini) → pragmatic filter (Mistral) → serial synthesis (Claude) → integrity spine restoration (Codex) → integrity stress test (Gemini) → implementation contracts (Mistral) → final synthesis (Claude). 2026-05-27.*
