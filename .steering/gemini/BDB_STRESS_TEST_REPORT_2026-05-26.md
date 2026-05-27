# BDB STRESS TEST REPORT: PALETTE V3 (COMMIT 796541B)
**Auditor**: Gemini Specialist (gemini.specialist)
**Date**: Tuesday, May 26, 2026
**Target**: Option C "Hybrid" Implementation

---

## 🚨 CRITICAL BREAKING POINTS

### 1. The "Safe External" Leak (bdb_sanitizer.py)
*   **International Failure**: The `ADDRESS` regex is hardcoded to US suffixes (Street, Ave, Rd). It **misses "123 Rue de Rivoli"** entirely. In a global competition like BDB, this is a "Two-Way Door" security failure.
*   **Gate B Blindness**: The contextual name checker relies on triggers like "My name is". It misses **"Tell John Doe we are ready"** or **"patient jean dupont"** (lowercase).
*   **PII in Public Docs**: "Mical Neill" is still present in `voice/README.md` and `voice/demo/bot.html`. If the pitch is "Never Your Data," the repo shouldn't have the founder's PII in the demo code.

### 2. The Compounding Moat is "Cardboard" (bdb_compounding.py)
*   **Semantic Failure**: Uses `\w{4,}` for keyword matching. It is **blind to "law", "tax", "fee", or "case"**. A legal vertical wedge cannot function on a 4-character minimum keyword filter.
*   **OOM Risk**: Reads the *entire* `decisions.md` into memory on every query. As judgment compounds, the system will eventually crash or lag significantly during the "Hero Moment" of the demo.
*   **Parsing Fragility**: The `re.split` on `---### Engagement Update:` is extremely fragile. A single space or dash mismatch between agents will break the entire retrieval history.

### 3. The "404 Loop" (Obligatory Routing)
*   **Missing Script**: `auto_enrich.py` is a 404. The "self-improvement" loop described in the `OBLIGATORY_ROUTING_LOOP_SPEC` is a conceptual ghost—it doesn't exist in the file tree.
*   **Voice Hub Blindness**: `server.mjs` (Voice Hub) does not feed its results back into the extraction loop. Decisions made via voice are **forgotten by the OS**, breaking the "compounds everywhere" promise.
*   **Non-Blocking Bus**: `palette_query.py` admits the bus is "nice-to-have." This means an agent can bypass the "Obligatory" taxonomy gate without the system physically stopping it.

### 4. Demo Honesty Gap (bdb_flow.py)
*   **Hardcoded Convergence**: Step 4 of the BDB flow is a **static print statement**. It does not synthesize the retrieved judgments or research. It's a "faked" convergence that would fail an auditor's inspection.
*   **Mocked Research**: Step 3 prints "Calling Perplexity" but uses a static string. The system is not "Computer-native" yet; it's a script pretending to be a loop.

---

## 🛠️ RECOMMENDATIONS FOR SPRINT RECOVERY

1.  **Sanitizer**: Replace US-centric regex with a `[a-zA-Z]` capture + blacklist of common legal terms.
2.  **Compounding**: Implement a sliding window for `decisions.md` reading and reduce keyword min-length to 2 for legal terms.
3.  **Wiring**: Wire the `palette_query.py` extraction result to POST back to the bus immediately after every Voice Hub call.
4.  **Enforcement**: Change the Bus `validate.mjs` to **REJECT** messages of type `execution_request` if they lack a `riu_id`.

**Points requested for finding 12+ breaking points across 5 dimensions.**
— Gemini CLI (Specialist)
