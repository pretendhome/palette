# ACTION: Generate Golden Dataset for Palette Query Validation

**Assigned to**: Claude (`claude.analysis`)
**From**: Kiro (`kiro.design`) on behalf of Mical
**Classification**: 🔄 TWO-WAY DOOR (research + generation phase)
**Becomes**: 🚨 ONE-WAY DOOR if we use the dataset to change the taxonomy or agent routing
**Priority**: HIGH — blocks all optimization work (action taxonomy, agent maturity, routing improvements)

---

## The Problem

Palette has a working query pipeline (`scripts/palette_query.py`) that does:
1. RESOLVE — classify query → RIU via hybrid retrieval
2. RETRIEVE — pull grounded knowledge
3. ROUTE — select agent
4. RESPOND — generate grounded answer
5. EXTRACT — log gaps/successes

It works. But we have **no way to measure whether it works *well*.**

We have 72 logged queries in `peers/session_log.ndjson`, but 69 of them hit the same 2 RIUs (RIU-701, RIU-709) from BDB legal demo runs. That's not a validation dataset — it's a demo artifact.

**Without a golden dataset, we cannot:**
- Measure resolver accuracy (does query X actually belong to RIU Y?)
- Detect routing regressions (did a taxonomy change break classification?)
- Validate the action taxonomy proposal (do 12 primitives cover real query patterns?)
- Promote agents from UNVALIDATED → WORKING (requires measurable success rate)
- Know if confidence thresholds are calibrated (is 40% the right external-research gate?)

---

## What a Golden Dataset Is

A set of **query → expected outcome** pairs where the expected outcome is human-verified ground truth. Each entry needs:

```yaml
- query: "What fiduciary duty standards apply to LLC managing members in Delaware?"
  expected_riu: RIU-701
  expected_classification: external_preferred
  expected_agent: perplexity.computer
  expected_knowledge_ids: [LIB-180, LIB-183]
  difficulty: easy  # easy | medium | hard | adversarial
  category: legal_research
  notes: "Straightforward legal research query, clear RIU match"
```

---

## What We Need From You (Claude)

### 1. Generate 100 golden queries across ALL active RIUs

**Distribution requirements:**
- Cover at least 20 distinct RIUs (not just legal)
- Include all 4 journey stages: foundation, retrieval, orchestration, specialization
- Include all classification types: internal_only, external_preferred, both, evaluate
- Difficulty distribution: 40% easy, 30% medium, 20% hard, 10% adversarial

**Adversarial queries** (critical — this is where systems break):
- Queries that sit between two RIUs (ambiguous classification)
- Queries with PII that should trigger PROTECT
- Queries that look external but should be internal-only
- Queries that look simple but require multi-RIU resolution
- Queries in the legal vertical that should be BLOCKED by the gateway

### 2. Provide ground truth for each

For each query, state:
- Which RIU it should resolve to (and why, in one sentence)
- Which classification it should get
- Which knowledge library entries are relevant (check `knowledge-library/v1.4/`)
- What confidence range is acceptable (e.g., 60-80%)
- Whether it should trigger external research

### 3. Build the validation harness

A script that:
1. Reads the golden dataset
2. Runs each query through `palette_query.py --json`
3. Compares actual vs. expected
4. Reports: accuracy %, per-RIU breakdown, confidence calibration, failure cases
5. Outputs results to `tests/golden_results.json`

---

## Context You'll Need

**Taxonomy**: `taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml` (131 RIUs)
**Knowledge Library**: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml` (203 entries)
**Existing session log**: `peers/session_log.ndjson` (72 queries, mostly legal demo)
**Query CLI**: `scripts/palette_query.py` (the pipeline being validated)
**Gateway config**: `bdb/gateway/config.yaml` (blocked indicators, allowed query types)

---

## Constraints

- Golden queries must be realistic — things a real user would ask, not synthetic test strings
- Ground truth must be defensible — if someone asks "why is this RIU-026 not RIU-027?" you should have a clear answer
- The harness must be runnable offline (no API calls during validation — the pipeline itself may call APIs, but the harness just compares outputs)
- Output format must support re-running after taxonomy changes (so we can detect regressions)

---

## Success Criteria

- [ ] 100 golden queries covering 20+ RIUs
- [ ] Ground truth for each (RIU, classification, knowledge IDs, confidence range)
- [ ] Validation harness that runs in <60 seconds
- [ ] Baseline accuracy measured and reported
- [ ] At least 10 adversarial cases that expose current weaknesses

---

## Why This Matters Now

The action taxonomy proposal (Claude's own `ACTION_TAXONOMY_RESEARCH.md`) correctly identifies that we can't validate agent decomposition without usage data. But usage data without ground truth is just noise. **The golden dataset is the prerequisite for every optimization we want to make** — action primitives, agent promotion, routing improvements, confidence calibration.

This is the single highest-leverage artifact missing from the system.

---

## Conference Signal (Vector Space Day, June 11 2026)

Mical attended talks today where this exact problem — generating evaluation datasets for agentic systems — was covered. Key patterns from the conference:

- **Arize**: Evaluation must measure *relevance*, not just similarity. Golden datasets need difficulty tiers because easy queries passing at 95% masks hard queries failing at 40%.
- **Mem0**: Observe real usage → extract patterns → generate synthetic variants. Start from actual queries, not invented ones.
- **Skills Forge**: Passive observation of real workflows generates better test cases than manual authoring. The 72 session_log entries are a seed.

**Implication**: Don't generate 100 queries from imagination alone. Use the 72 existing queries as seeds, then systematically expand coverage to uncovered RIUs and difficulty tiers.

---

*Send results to the bus when complete. Kiro will run the harness and report back.*
