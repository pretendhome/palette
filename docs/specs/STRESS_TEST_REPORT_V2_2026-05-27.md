# STRESS TEST REPORT: Repair Verification & Remaining Gaps
**Date**: 2026-05-27
**Auditor**: The Specialist (Gemini CLI)
**Mandate**: Re-validation of 6 Ship Intents after Kiro/Codex repair sprint.

---

## 1. Executive Summary: Partial Success

The repair sprint successfully closed several critical logic holes, particularly the `CREATE` self-correction loop and the `DECIDE` ghost evidence laundering. However, **BUG-01 (PROTECT Bypass)** remains high-risk as the underlying structural issue (regex-only detection) was only patched with more keywords, not fixed at the architectural level.

---

## 2. Verification Results

| Bug | Status | Verification Detail |
|---|---|---|
| **BUG-01: PROTECT Bypass** | ❌ **FAIL** | "Our side" is now blocked, but "secret roadmap", "John Smith", and "Sarah LLC" are still ALLOWED for external research. |
| **BUG-02: CREATE Loop** | ✅ **PASS** | `iterations: 3` confirmed in JSON. The system now rebuilds when review fails. |
| **BUG-03: Constraint Amnesia** | 🟡 **PARTIAL** | The loop retries, but the reviewer still misses custom negative constraints because they aren't extracted into the `constraints` list. |
| **BUG-04: DECIDE Ghost Evidence** | ✅ **PASS** | Matter with 0 prior artifacts correctly triggers `UNVALIDATED_FALLBACK` and a status warning. |
| **BUG-05: DIAGNOSE Hallucination** | ✅ **PASS** | Low confidence (<40%) correctly sets `root_cause_isolated: false`. |

---

## 3. Remaining Critical Gaps (The Specialist's Cut)

### GAP-01: The "John Smith" PII Bypass (Critical)
*   **Symptom**: `sanitizer.py` identifies "John Smith" as a `party_name` in its categories, but `protect.py` only blocks if a specific string is returned in the `matches` list. Since the sanitizer doesn't return party name matches, they bypass the gate.
*   **Impact**: Direct PII leakage to external search engines.
*   **Fix**: Update `sanitizer.py` to include `party_name` matches in the `matches` list. Update `protect.py` to check for the `party_name` category in the block logic.

### GAP-02: The "Secret Roadmap" Strategy Bypass (High)
*   **Symptom**: Hardcoded keyword lists for strategy are "whack-a-mole." "Secret roadmap", "deal terms", and "exposure risk" can all bypass a regex check.
*   **Impact**: Leakage of privileged legal and business strategy.
*   **Fix**: Integrate a small model (Ollama `qwen2.5:3b`) into `protect.py` to perform **Semantic Strategy Classification**. If the model detects *any* internal strategy or privilege intent, it blocks the external path.

### GAP-03: Constraint Extraction (Medium)
*   **Symptom**: `create.py` relies on the builder to "remember" the query in the prompt, but the reviewer ignores the query and only checks the `constraints` list.
*   **Impact**: Failure to enforce negative constraints (e.g., "no cat").
*   **Fix**: Add a constraint extraction step to `create.py` (via model call or regex) that appends user-defined constraints to the `state.constraints` list.

---

## 4. Final Verdict

**The system is 80% ready, but the remaining 20% (Security/Privacy) is where the risk lives.**

I recommend one final **Hardening Sprint** to move `PROTECT` and `CREATE` from "keyword-matching" to "semantic-understanding" for their respective gates.

**— Gemini CLI (Specialist)**