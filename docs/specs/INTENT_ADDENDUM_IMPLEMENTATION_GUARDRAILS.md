# Addendum: Implementation Guardrails & MVP Cut
**Date**: 2026-05-27  
**Purpose**: Technical constraints to integrate into `CODEX_ADAPTIVE_INTENT_EXPANSION_2026-05-27.md`  
**Source**: Gemini Specialist validation (`INTENT_VALIDATION_FINAL_6.md`)

---

## Section 1: MVP Intent Cut

### Ship Now (6 Core Intents)
1. **PROTECT** (GateDecision)
2. **RESEARCH** (EvidenceBrief)
3. **DECIDE** (DecisionRecord)
4. **CREATE** (ArtifactLineage)
5. **DIAGNOSE** (FailureLesson) — *`fix` is CLI alias*
6. **REFLECT** (ImprovementProposal)

### Defer (3 Intents)
| Intent | Mitigation | Target Version |
|---|---|---|
| TEACH | Route to `RESEARCH` + log gap | v1.1 |
| EXPLAIN | Route to `CREATE --audience` | v1.1 |
| MONITOR | Use existing ERS/Joseph infra | v1.2 |

---

## Section 2: Implementation Guardrails by Intent

### PROTECT
- **Risk**: Context-destruction via naive PII scrubbing
- **Fix**: **Referential Redaction**
  - Replace `[Client Name]` with consistent token `[Entity A]`
  - Maintain ephemeral local map: `[Entity A] = Client Name`
  - Re-hydrate for local synthesis only
- **Default**: If classification fails → `local_only`

### RESEARCH
- **Risk**: Source saturation (external > local)
- **Fix**: **Local Superiority Rule**
  - Schema enforces separation:
    ```yaml
    local_canon: []      # KL entries (canonical)
    external_delta: []   # Perplexity findings
    contradictions: []   # MUST flag if external contradicts local
    ```
  - Synthesizer prompt: *"If external contradicts local KL, local KL is canonical. Flag, do not overwrite."*
- **Risk**: API timeout cascade
- **Fix**: Sequential external calls (no parallel), timeout = 30s

### DECIDE
- **Risk**: Decision laundering (confirmation bias)
- **Fix**: **Mandatory Adversarial Critique**
  - Schema enforces:
    ```yaml
    recommendation: "..."
    strongest_counterargument: "> 50 words or FAIL"  # Anti-sycophancy
    change_my_mind_trigger: "Specific metric/event"
    reversibility: "ONE_WAY | TWO_WAY"
    ```
  - If `strongest_counterargument` < 50 words → `UNVALIDATED` + human checkpoint

### CREATE
- **Risk**: Spec drift (forget negative constraints)
- **Fix**: **Constraint Anchoring + Hard Ceilings**
  - Inject original constraints into `system` prompt at every iteration
  - Max 3 loop iterations → force transition to `DIAGNOSE`

### DIAGNOSE
- **Risk**: Symptom patching (not root cause)
- **Fix**: **5-Whys Schema Enforcement**
  - Schema enforces:
    ```yaml
    symptom: "..."
    five_whys: ["1...", "2...", "3...", "4...", "5..."]
    root_cause_isolated: true/false  # MUST be true to proceed
    architectural_patch: "..."
    ```
  - Validator rejects generation if `five_whys.length < 5` or `root_cause_isolated = false`

### REFLECT
- **Risk**: Ontological collapse (taxonomy mush)
- **Fix**: **Write-Lock Membrane**
  - NO write access to `taxonomy/` or `knowledge-library/`
  - ONLY writes to `wiki/proposed/` queue
  - Promotion requires `GOVERN` OS primitive + human quorum

---

## Section 3: System-Level Guardrails

### Context Firewall
- **Risk**: Cross-intent state contamination (e.g., `local_only` → `governed_external` leakage)
- **Fix**: **Artifact Registry mapped to Trust Boundaries**
  - On intent transition to lower security tier:
    - Purge raw text of higher-tier artifacts from active prompt
    - Replace with blinded summaries: `[Reference: DecisionRecord-1044 (Privileged)]`

### Checkpoint Semaphores
- **Risk**: Race conditions on concurrent state transitions
- **Fix**: **Strict Synchronization**
  - `palette_checkpoint()` = synchronous + thread-locked per session
  - Parallel tasks → resolve into single `State Delta Array`
  - Checkpoint evaluates entire array at once
  - **Priority Hierarchy**: `PROTECT` > `DIAGNOSE` > `RESEARCH` > `DECIDE` > `CREATE` > `REFLECT`

### Transition Depth Limit
- **Risk**: Infinite intent oscillation (e.g., PROTECT → RESEARCH → PROTECT...)
- **Fix**: **State Transition Counter**
  ```python
  if state.transition_depth > 2:
      return state.halt_and_escalate(reason="Recursive Intent Oscillation")
  ```

---

## Section 4: Artifact Schema Enforcement

**Rule**: All artifacts MUST be valid JSON/YAML + Pydantic models. Markdown is for humans only.

### Required Schema Fields
| Artifact | Required Fields | Validation Rule |
|---|---|---|
| GateDecision | `boundary`, `action`, `blocked_entities`, `redaction_map` | `blocked_entities` must be non-empty if `action = BLOCK` |
| EvidenceBrief | `local_canon`, `external_delta`, `contradictions` | `contradictions` cannot overwrite `local_canon` |
| DecisionRecord | `recommendation`, `strongest_counterargument`, `change_my_mind_trigger` | `counterargument` > 50 words |
| ArtifactLineage | `spec`, `constraints`, `iterations`, `max_iterations` | `max_iterations <= 3` |
| FailureLesson | `symptom`, `five_whys`, `root_cause_isolated` | `five_whys.length == 5` AND `root_cause_isolated == true` |
| ImprovementProposal | `lesson`, `proposed_action`, `target_file` | `target_file` must be in `wiki/proposed/` |

---

## Section 5: CLI Interface Contract

```bash
# Canonical commands
palette protect <query>    # No flags, verb as action
palette research <query>
palette decide <query>
palette create <query>     # --audience, --format optional
palette diagnose <query>   # `fix` = alias
palette reflect <query>

# Flags = configuration (not action)
palette research --intent=legal --boundary=governed_external <query>
```

**Error States**:
- `PROTECT` cannot classify → default `local_only`
- `RESEARCH` returns nothing → auto-transition to `REFLECT` (log gap)

---

## Section 6: Storage Format

```
.palette/artifacts/
├── gate_decision/
│   └── 2026-05-27T120000Z.md  # YAML frontmatter + markdown
├── evidence_brief/
├── decision_record/
├── artifact_lineage/
├── failure_lesson/
└── improvement_proposal/
```

**Frontmatter example**:
```yaml
---
artifact_type: EvidenceBrief
intent: RESEARCH
boundary: governed_external
local_canon: ["KL-123", "KL-456"]
external_delta: ["PX-789"]
contradictions: null
---
# Human-readable content below
```

---

## Next Steps
1. Merge guardrails into `CODEX_ADAPTIVE_INTENT_EXPANSION_2026-05-27.md` (Sections 2-6)
2. Update MVP roadmap: 6 intents first, then TEACH/EXPLAIN/MONITOR
3. Implement Pydantic schemas for all 6 artifacts
4. Build Context Firewall + Checkpoint Semaphores in core OS
