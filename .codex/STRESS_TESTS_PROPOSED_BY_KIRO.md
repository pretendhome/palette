# Palette Stress Tests — Proposed by Kiro

**Date**: 2026-02-26  
**Context**: After V2 (PIS Query Engine) and V3 (Multi-Agent Coordination) stress tests  
**Purpose**: Identify real weaknesses in Palette's core systems

---

## Stress Test 4: Cross-Implementation Consistency

**What it tests**: Whether different implementations (retail, talent, education) actually use Palette consistently or drift into custom patterns

**How to run**:
1. Pick 3 implementations from different domains (e.g., `retail-rossi-store`, `talent-gap-interview`, `education-alpha`)
2. Trace one common workflow through each: "resolve user query → traverse RIU → generate recommendation"
3. Compare across implementations:
   - Do they use the same data structures?
   - Same agent roles (Cory, Argy, Rex)?
   - Same handoff patterns?
   - Same state persistence format?
4. Document divergences with severity (cosmetic vs breaking)

**Success criteria**:
- 80%+ structural consistency across implementations
- Any divergence is documented with explicit rationale
- Shared workflows use shared code (not copy-paste)

**Expected failure mode**: Each implementation has its own "version" of coordination, different field names, incompatible state formats. Palette becomes a collection of one-offs, not a reusable system.

**Why it matters**: If every implementation reinvents the wheel, Palette isn't a system - it's a template that gets forked and never merged back.

**Estimated time**: 2-3 hours

---

## Stress Test 5: Agent Handoff Under Partial Failure + Data Drift

**What it tests**: Whether the coordination layer actually preserves state correctly when agents fail mid-workflow AND the underlying data changes between runs

**How to run**:
1. Start a multi-step task using `scripts.pis.coordination`:
   ```bash
   python -m scripts.pis.coordination run "add observability to my system"
   ```
2. Inject failure at step 2 (traversal):
   ```bash
   python -m scripts.pis.coordination run "add observability" --fail-step traversal
   ```
3. Modify the underlying data between failure and replay:
   - Change a RIU classification (e.g., RIU-061 from "both" to "internal_only")
   - Add a new service to routing
   - Update a recipe's cost data
4. Replay from the failed step:
   ```bash
   python -m scripts.pis.coordination replay <task_id>
   ```
5. Inspect the replayed packet and check:
   - Does step 1 (cory) output get re-used (cached) or re-run?
   - Does step 2 (traversal) see the NEW data or OLD data?
   - Is there any indication in the packet that data changed between runs?

**Success criteria**:
- Replay semantics are documented and consistent
- If using cached data, packet includes timestamp/version of data used
- If re-running, packet clearly shows which steps were re-executed
- No silent data inconsistencies (old RIU classification + new routing data)

**Expected failure mode**: 
- Replay uses cached step 1 output (old RIU resolution) but step 2 sees new data (updated routing) → inconsistent recommendations
- OR replay re-runs everything, losing the "preserve upstream outputs" guarantee
- OR no indication in the packet that data changed, making debugging impossible

**Why it matters**: Real systems have data that changes. If replay doesn't handle this, the coordination layer is only useful for static demos.

**Estimated time**: 1-2 hours

---

## Stress Test 6: PIS Data Layer Drift Detection

**What it tests**: Whether the `query_engine check` command actually catches cross-layer inconsistencies or passes with false confidence

**How to run**:
1. **Baseline**: Run check on clean state
   ```bash
   python -m scripts.pis.query_engine check
   ```
   Expected: All checks pass

2. **Introduce drift 1**: Add new RIU to taxonomy without classification
   - Add RIU-999 to `palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`
   - Don't add to `palette/company-library/service-routing/v1.0/riu_classification_v1.0.yaml`
   - Run `check` again
   - Expected: FAIL on "Every RIU in taxonomy has a classification entry"

3. **Introduce drift 2**: Add classification as "both" without routing entry
   - Add RIU-999 to classification file with `classification: both`
   - Don't add to `service_routing_v1.0.yaml`
   - Run `check` again
   - Expected: FAIL on "Every 'both' RIU has a service routing entry"

4. **Introduce drift 3**: Add routing entry referencing non-existent service
   - Add RIU-999 routing entry with service "FakeService Pro"
   - Don't create `palette/company-library/integrations/fakeservice-pro/recipe.yaml`
   - Run `check` again
   - Expected: FAIL on "Every service in routing has a matching recipe"

5. **Introduce drift 4**: Add orphaned recipe
   - Create `palette/company-library/integrations/orphan-tool/recipe.yaml`
   - Don't reference it in any routing entry
   - Run `check` again
   - Expected: FAIL on "No orphaned recipes"

6. **Introduce drift 5**: Reference non-existent agent
   - Modify RIU-999 to include agent "ARK:FakeAgent"
   - Run `check` again
   - Expected: FAIL on "Agent names in taxonomy match known agent list"

**Success criteria**:
- All 5 drift scenarios are caught by `check` command
- Error messages are actionable (tell you exactly what's wrong and where)
- No false positives (clean state passes)
- No false negatives (drift state fails)

**Expected failure mode**:
- Check passes when it should fail (doesn't detect drift)
- Check reports vague errors ("something is wrong") without actionable fix instructions
- Check is too strict (flags intentional design choices as errors)

**Why it matters**: The 4-layer PIS data structure (taxonomy → classification → routing → recipes) is the foundation. If drift goes undetected, every query returns garbage.

**Estimated time**: 1 hour

---

## Recommendation: Run Order

1. **Start with Stress Test 6** (PIS Data Layer Drift Detection)
   - Fastest to execute (1 hour)
   - Tests the data integrity foundation
   - If this fails, everything else is suspect

2. **Then run Stress Test 5** (Agent Handoff Under Partial Failure)
   - Tests the coordination layer's core promise
   - Exposes replay semantics bugs
   - Medium complexity (1-2 hours)

3. **Finally run Stress Test 4** (Cross-Implementation Consistency)
   - Longest to execute (2-3 hours)
   - Tests whether Palette is actually reusable
   - Requires understanding multiple implementations

---

## Notes for Codex

- These tests target **architectural weaknesses**, not implementation bugs
- They assume the V2 and V3 implementations are working as designed
- The goal is to find where the design itself breaks under realistic conditions
- Each test should produce a report with: pass/fail, failure details, recommended fixes

**Self-awareness note from Kiro**: I designed these tests to expose the kinds of problems I personally miss - data drift, cross-file consistency, and whether abstractions actually get reused. These are my blind spots from the V2/V3 stress tests.
