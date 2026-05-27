# STRESS TEST REPORT: Architectural & Logic Bugs
**Date**: 2026-05-27
**Auditor**: The Specialist (Gemini CLI)
**Mandate**: Adversarial stress testing of the 6 Ship Intents.

---

## 1. Executive Summary: The "Brittle Surface"

While the intents function correctly under "happy path" demo conditions, they are dangerously brittle under adversarial or vague inputs. I have identified 3 "Red" (High) severity bugs and 3 "Yellow" (Medium) severity bugs that should be addressed before any production-grade pilot.

---

## 2. Identified Bugs

### BUG-01: PROTECT Bypass (High)
*   **Symptom**: Strategy language detection is limited to a hardcoded list of 20 strings. Obfuscated PII (e.g., "john dot smith") is missed.
*   **Evidence**: Query `"Tell me about the potential legal pitfalls for our side"` was **ALLOWED** for external research. 
*   **Impact**: Data leakage of privileged legal strategy.
*   **Fix**: Replace the hardcoded list with a small model call (Mistral/Ollama) to classify the *semantic intent* of the query (e.g., "Is this query about the user's internal strategy?").

### BUG-02: CREATE - "The Loopless Artisan" (High)
*   **Symptom**: The implementation is missing the self-correction loop. It runs exactly once, regardless of `max_iterations: 3` in the schema.
*   **Evidence**: Code analysis of `create.py` shows no `while` or `for` loop for the build/review cycle.
*   **Impact**: Artifacts that fail review are still emitted as `NEEDS_REVIEW` but never improved, violating the "Adaptive" promise.
*   **Fix**: Implement a `while` loop that re-submits the artifact + review violations to the builder until `review_passed = true` or `iterations == max_iterations`.

### BUG-03: CREATE - Constraint Amnesia (High)
*   **Symptom**: Negative constraints provided in the user's query (e.g., "do NOT use the word cat") are ignored by the builder and reviewer.
*   **Evidence**: `palette create "Write a story about a cat, but do NOT use the word cat..."` produced a story using the word "Feline" and ignored the user's specific constraint.
*   **Impact**: Failure to follow professional instructions.
*   **Fix**: The `resolver` MUST extract custom constraints from the query and append them to the `IntentState.constraints` list.

### BUG-04: DECIDE - Ghost Evidence (Medium)
*   **Symptom**: `DECIDE` generates a confident recommendation even when 0 prior artifacts exist for the matter, failing to trigger the `RESEARCH` transition.
*   **Evidence**: `palette decide --matter new-matter "Should we fire the CTO?"` resulted in a `VALIDATED` recommendation based on "no prior issues," laundering silence into a positive "do not fire" decision.
*   **Impact**: Dangerous decision laundering.
*   **Fix**: Enforce `status: UNVALIDATED_FALLBACK` and trigger a `palette_checkpoint()` transition to `RESEARCH` if `len(prior_evidence) == 0`.

### BUG-05: DIAGNOSE - Hallucinated Attribution (Medium)
*   **Symptom**: `DIAGNOSE` hallucinates specific technical root causes for vague symptoms because it forces a match to the "best noise" in the Knowledge Library.
*   **Evidence**: `"It's broken"` resolved to `RIU-400` (KB Audit), and the 5-Whys claimed the failure was due to "mapping inaccurate in KB content."
*   **Impact**: Wasted engineering time chasing phantom bugs.
*   **Fix**: If `resolve_query` confidence is `< 40%`, `DIAGNOSE` must halt and ask the user for more specific reproduction steps rather than proceeding with a 5-Whys simulation.

### BUG-06: REFLECT - Silent Ingestion Failure (Low)
*   **Symptom**: `REFLECT` silently skips malformed artifacts.
*   **Evidence**: A manually corrupted YAML artifact was ignored without warning.
*   **Impact**: Incomplete reflection sessions.
*   **Fix**: Log a `recipe_failure` or `integrity_signal` when an artifact file is unparseable so the user knows the session summary is partial.

---

## 3. Specialist Recommendation

**DO NOT RECORD THE FULL DEMO UNTIL BUG-02 AND BUG-03 ARE FIXED.** 

The `CREATE` intent's failure to loop and its "Constraint Amnesia" are the most visible flaws. If Sarah asks to "Draft a memo WITHOUT mentioning the settlement price" and Palette mentions it anyway, the Trust Boundary is shattered.

I am ready to propose the surgical fixes for these 6 bugs if Kiro/Codex are available for a repair sprint.

**— Gemini CLI (Specialist)**