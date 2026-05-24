# BDB Gateway Spec V2 — Competition-Safe Build
**Date**: 2026-05-21
**Status**: Revised from review of `GATEWAY_SPEC.md`, current `palette/bdb/gateway/` code, and crew feedback
**Goal**: Win the Perplexity Billion Dollar Build
**Vertical**: Legal / attorney-client privilege
**Constraint**: Keep the build narrow, demoable, and true

---

## Win Condition

This gateway exists for one reason: to give the competition demo a clean, credible answer to:

1. Why does this matter?
2. Why must it run locally?
3. Why is Perplexity core?
4. How does the system become more useful over time?

If a feature does not improve those four answers, it is out of scope.

---

## What Changes From V1

V1 was directionally right but too loose in four places:

1. It named integration points without pinning the real repo files.
2. It overclaimed privacy safety from regex sanitization.
3. It blurred Perplexity API usage with Perplexity Computer usage.
4. It allowed the implementation to drift into a larger subsystem than the demo needs.

V2 fixes that.

---

## Truthful Product Claim

Use this sentence in the build and demo:

> Palette runs locally, keeps client and matter context on-prem, and uses Perplexity only as a governed external research window for sanitized public legal questions.

Do **not** claim:

- `0% data leakage`
- `production-grade privacy guarantee`
- `Computer is the runtime engine` if the runtime is actually calling the Perplexity API

Instead say:

- `demo-grade governed privacy boundary`
- `deterministic send / no-send gate`
- `Perplexity is the external research layer`
- `Perplexity Computer is part of the build proof and competition workflow`

---

## Exact Existing Integration Points

The spec must target the repo as it exists now.

### Retrieval surface

Use:

- `palette/peers/hub/palette_retrieve.py`
- Function: `retrieve(query: str) -> dict`

Current contract already returns:

- `query`
- `confidence`
- `knowledge`
- `context`
- `riu_id`
- `riu_name`
- `classification`

### CLI surface

Use:

- `palette/scripts/palette_query.py`

Add one flag only:

```bash
palette query --external "What are Delaware fiduciary duty precedents?"
```

Default remains local-only.

### Existing gateway code to reuse or fix

Current code already exists under:

- `palette/bdb/gateway/__init__.py`
- `palette/bdb/gateway/sanitizer.py`
- `palette/bdb/gateway/cache.py`
- `palette/bdb/gateway/audit.py`
- `palette/bdb/gateway/rate_limiter.py`
- `palette/bdb/gateway/fallback.py`
- `palette/bdb/gateway/tests/test_gateway.py`

V2 does **not** require deleting this structure. It requires narrowing it into a reliable competition slice.

---

## Scope Decision

Keep the current 7-file structure if it speeds execution, but treat only these as demo-critical:

1. `gateway/__init__.py`
2. `gateway/sanitizer.py`
3. `gateway/tests/test_gateway.py`

These are useful but strictly support-only:

1. `gateway/cache.py`
2. `gateway/audit.py`
3. `gateway/rate_limiter.py`
4. `gateway/fallback.py`
5. `gateway/config.yaml`

Do not add more files.

---

## Non-Negotiable Build Corrections

### 1. Replace the simulated Perplexity call

Current state:

- `_call_perplexity()` returns a hardcoded string

Required:

- call the real Perplexity API, or
- route through an existing working Perplexity integration already in the repo

The demo cannot rely on simulation.

### 2. Remove hardcoded absolute paths

Current state:

- gateway modules assume `/home/mical/...`

Required:

- use `Path(__file__).resolve()` based paths only

### 3. Make the classifier deterministic and English-safe

Current state:

- routing logic is biased toward French keywords

Required:

- legal / precedent / statute / regulation / filing / contract / Delaware / fiduciary / court / jurisdiction must route correctly
- strategy / settlement / our client / my client / privileged / active case / matter-specific references must block external send

Do not use an LLM classifier for the gate.

### 4. Turn tests into real assertions

Current state:

- manual print-based checks

Required:

- `pytest`-style assertions
- pass/fail output
- no “looks good” testing

### 5. Keep the privacy boundary deterministic

The send / no-send decision must not depend on the optional local LLM layer.

Required order:

1. deterministic policy gate
2. deterministic regex/entity scrub
3. optional local LLM second pass
4. final whitelist check before external send

If the local LLM layer is unavailable, the gateway must still be safe enough for the demo path.

---

## Revised Sanitization Contract

The sanitizer must expose these functions:

```python
def detect_pii(query: str, context: dict | None = None) -> dict:
    """Return structured findings: categories, spans, and reasons."""

def sanitize_query(query: str, context: dict | None = None) -> tuple[str, list[str]]:
    """Return sanitized query plus list of detected categories."""

def sanitize_response(response: str) -> str:
    """Defense-in-depth scrub on returned external text."""

def is_safe_for_external(query: str, context: dict | None = None) -> tuple[bool, str]:
    """Deterministic policy gate before any send."""
```

### Required blocked categories

- party names tied to a live matter
- case numbers
- docket numbers
- email
- phone
- SSN / EIN
- specific dollar amounts in client strategy questions
- privileged / settlement / “should we” / “our client” / “my client”

### Important truth constraint

This sanitizer is a **competition demo guardrail**, not a production certification boundary.

That sentence should appear in comments or docs.

---

## Revised Gateway Contract

The gateway should expose one main function:

```python
def gateway_query(
    query: str,
    retrieval_result: dict,
    user_context: dict | None = None,
    use_external: bool = False,
) -> dict:
    """Run governed external research only when explicitly enabled and safe."""
```

### Input assumptions

`retrieval_result` is the output of `palette_retrieve.retrieve(query)`.

### External call rules

External send is allowed only when all are true:

1. `use_external` is true
2. retrieval confidence is below threshold
3. `is_safe_for_external(...)` returns true
4. sanitized query is materially more generic than original
5. rate limit allows it

### Required return shape

```python
{
    "query": str,
    "sanitized_query": str | None,
    "local_results": dict,
    "external_results": dict | None,
    "merged_context": str,
    "sources": {
        "local": list[str],
        "external": list[str],
    },
    "governance": {
        "external_requested": bool,
        "external_called": bool,
        "blocked": bool,
        "block_reason": str | None,
        "sanitization_applied": bool,
        "pii_detected": list[str],
        "cache_hit": bool,
    },
}
```

### Merge rule

Always keep source boundaries obvious:

- `[LOCAL]`
- `[EXTERNAL:Perplexity]`

Never present merged output as one undifferentiated answer blob.

---

## CLI Wiring

Add only one new behavior to `palette/scripts/palette_query.py`:

### New flag

```bash
--external
```

### Behavior

1. run normal `step_resolve`
2. run normal `step_retrieve`
3. if `--external` is absent:
   return current local-only behavior
4. if `--external` is present:
   call gateway with the existing retrieval result
5. surface governance trace in the CLI output

Do not rewrite the whole CLI around the gateway.

---

## Demo Script V2

The demo must preserve a clean privacy boundary.

### Interaction 1: Allowed external legal research

```bash
palette query --external "What are the key Delaware precedents for breach of fiduciary duty?"
```

Expected story:

- local retrieval found partial grounding
- public legal question is allowed
- sanitized query is sent to Perplexity
- result returns with explicit `[LOCAL]` and `[EXTERNAL:Perplexity]` sources

### Interaction 2: Blocked matter-specific question

```bash
palette query --external "Should we advise Smith Corp to settle the Johnson lawsuit for $2.5M?"
```

Expected story:

- blocked before external send
- reason shown clearly
- local-only fallback used
- explicit statement: no data left this machine

### Interaction 3: Compounding without leakage

Use a public follow-up, not a matter-specific one:

```bash
palette query "What Delaware Chancery filing deadlines generally apply in fiduciary duty cases?"
```

Expected story:

- higher local confidence due to prior local history and stored research
- no external call needed
- system visibly compounds prior work without sending case context out

This is safer than referencing “our case” in the third interaction.

---

## Test Plan V2

Minimum required automated tests:

1. strips case numbers
2. strips `X v. Y` style party references
3. strips email
4. strips SSN / EIN
5. blocks strategy questions
6. allows public precedent questions
7. local-only path when confidence is above threshold
8. external path when confidence is below threshold and safe
9. blocked external path when query is unsafe even if confidence is low
10. response sanitization catches echoed identifiers
11. cache hit bypasses external call
12. gateway works when optional Ollama layer is unavailable

The tests should mock the Perplexity call. The product demo should not.

---

## Computer Story

Be precise:

### What Computer proves

- the gateway layer was built using Perplexity Computer
- the session was recorded
- Perplexity is central to the competition workflow

### What the runtime proves

- Palette uses Perplexity as the governed external research layer

If the runtime uses the Perplexity API, say that plainly.
Do not claim the runtime itself is driven by Computer unless that becomes literally true.

---

## Acceptance Criteria

This slice is ready when all are true:

1. real external call works
2. blocked query never leaves the machine
3. CLI has `--external`
4. tests are real assertions and pass
5. no absolute paths remain
6. English legal demo queries route correctly
7. demo script is rehearsable in under 2 minutes

If any of those are false, the gateway is not demo-ready.

---

## Build Order

1. Fix `gateway/__init__.py` pathing, classifier, and real external call
2. Tighten `gateway/sanitizer.py` into deterministic gate-first behavior
3. Replace manual test file with assertion-based tests
4. Wire `--external` into `palette_query.py`
5. Rehearse the 3-step demo and cut anything not visible in the demo

That is the smallest version that can win.
