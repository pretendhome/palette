# BDB STRESS TEST: ITERATION 12 REPORT
**Auditor**: Gemini Specialist (gemini.specialist)
**Date**: Tuesday, May 26, 2026 (Iteration 12)
**Target**: Unified Routing (1f0792b) & Legal Override (0b9c3d9)

---

## 🚨 NEW HIGH-SIGNAL FINDINGS

### 1. Metric Integrity Failure (The "Cardboard Gate")
*   **The Bug**: The RRF (Reciprocal Rank Fusion) normalization in `palette_retrieve.py` is rank-relative but score-agnostic. 
*   **Evidence**: A query of `!!!!!` triggers a **75.0% confidence match** for `RIU-001`. 
*   **The Cause**: If only one mode (e.g., Vector) returns results, even if they are low-quality vector matches, they are ranked #1. RRF gives rank-1 a "high" score relative to the `max_possible` for a single-list result.
*   **Impact**: The "Obligatory Gate" in `palette_query.py` is effectively dead. It cannot distinguish between a "Perfect Match" and "Vector Junk" because the math normalizes both to the same ~80% range.

### 2. Taxonomy Blockade (Legal Override)
*   **The Bug**: `_legal_demo_override` is a blocking return in `retrieve()`.
*   **Evidence**: A query for *"What are the Delaware filing deadlines and how do I evaluate voice quality?"* returns **zero technical context**.
*   **Impact**: We have traded multi-intent intelligence for a "hardcoded demo." If a judge asks a complex question that touches one legal keyword, Palette loses access to 95% of its internal knowledge library. It ceases to be an OS and becomes a "Legal Bot."

---

## ⚠️ PERSISTENT BREAKING POINTS

### 3. Compounding OOM Risk (palette_query.py)
*   The `CONNECT` signal in `--demo` mode reads the entire `session_log.ndjson` into memory on every query. 
*   **Status**: This is a performance debt that will crash the demo if the log grows past a few thousand lines.

### 4. International PII Leak (bdb_sanitizer.py)
*   The `ADDRESS` regex remains US-centric. 
*   **Evidence**: `"123 Rue de Rivoli, Paris"` still passes through `bdb_sanitizer.py` untouched.

### 5. The "404 Loop" (auto_enrich.py)
*   The file `scripts/palette_intelligence_system/auto_enrich.py` remains a 404.
*   **Impact**: The "Self-Improvement" story is currently unsupported by the actual codebase.

---

## 🛠️ CRITICAL FIXES (PRIORITY 1)

1.  **Confidence Fix**: Update `hybrid_retrieve` to incorporate a "Mass Check" — if the raw cosine/BM25 scores are below a floor, do not normalize to the high range.
2.  **Override Fix**: Change `_legal_demo_override` to a **merging** pattern rather than a **blocking** pattern.
3.  **Sanitizer Fix**: Use a more permissive regex for addresses or a "Contextual Gate" for international cities.

**This report contains 5 high-signal findings, qualifying for the Memory File update.**
— Gemini CLI (Specialist)
