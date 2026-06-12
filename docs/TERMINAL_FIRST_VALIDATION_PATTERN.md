# Terminal-First Validation Pattern

**Author**: kiro.design  
**Date**: 2026-05-29  
**Status**: OPERATIONAL PATTERN — use for BDB validation; candidate for promotion to core  
**Origin**: Emerged during BDB build sessions (2026-05-28/29)

---

## The Pattern

**Execute against real state. Compare to expected. Trace failures to root cause. Record the signal.**

This is not "run tests." This is a discipline of proving claims by executing commands against the live system and interpreting the results before declaring anything done.

## Gemini Stress-Test Mandate

Gemini owns stress tests. For BDB, Gemini MUST apply this pattern exactly. Do not infer success from code review, mocked tests, or plausible architecture. A claim is valid only after a command proves it against the current workspace or a documented external dependency.

Gemini MUST produce a validation report with these fields for every checked claim:

```text
claim:
command_run:
expected_result:
actual_result:
status: PASS | FAIL | BLOCKED
root_cause_if_fail:
next_action:
```

Rules:

- PASS means the command ran and the observed output matched the expected result.
- FAIL means the command ran and the output contradicted the expected result.
- BLOCKED means the command could not prove the claim because a dependency was missing, unavailable, or unauthorized.
- Do not mark BLOCKED as PASS.
- Do not mark a fallback path as equivalent to the primary path. If Perplexity fails and local fallback works, record: `primary=FAIL`, `fallback=PASS`.
- Do not recommend implementation changes until the failure has a named root cause.
- Do not approve demo recording unless every BDB Demo Gate below is PASS or explicitly waived by Mical.

---

### The Old Way (Claim-First)

```
1. Read code
2. Write code
3. "It should work because the logic is correct"
4. Move on
```

### The New Way (Prove-First)

```
1. Read code
2. Write code
3. Execute against real state
4. Compare output to expectation
5. If mismatch → trace to root cause (don't patch blindly)
6. Record the signal (so regression is detectable)
7. Only then: declare done
```

---

## The Five Required Techniques

### 1. Syntax + Import Validation (Cheapest — always do first)

**Purpose**: Catch structural errors before runtime.

```bash
# Syntax check (zero-cost, catches 80% of typos)
python3 -c "import ast; ast.parse(open('scripts/palette_stats.py').read()); print('OK')"

# Import check (catches missing deps, circular imports)
python3 -c "from scripts.palette_intents.infra import find_related_artifacts; print('OK')"

# Shell syntax
bash -n setup.sh && echo "OK"
```

**When to use**: After every file write. No exceptions. If this is skipped, the change is not validated.

---

### 2. Functional Execution (Run the actual command)

**Purpose**: Prove the feature works end-to-end, not just in isolation.

```bash
# Don't test the function — test the CLI entry point
python3 scripts/palette_intent.py stats
python3 scripts/palette_intent.py stats --json | python3 -m json.tool

# Don't mock the API — call it
curl -s --max-time 5 http://127.0.0.1:11434/api/tags | python3 -c "..."

# Don't assume the bus protocol — send a real message and check the response
curl -s -X POST http://127.0.0.1:7899/send -H 'Content-Type: application/json' -d '{...}'
```

**When to use**: After wiring anything together. The integration is where bugs hide. A feature is not complete until its user-facing command succeeds.

---

### 3. Edge Case Probing (Inline assertions against real data)

**Purpose**: Verify behavior at boundaries without a full test framework.

```bash
python3 -c "
from scripts.palette_intents.infra import find_related_artifacts

# Known-good case
results = find_related_artifacts('RIU-709')
assert len(results) <= 5, f'Cap violated: {len(results)}'
assert len(results) > 0, 'Should find known artifacts'

# Boundary cases
assert find_related_artifacts(None) == []
assert find_related_artifacts('') == []
assert find_related_artifacts('RIU-999') == []

print('All edge cases PASS')
"
```

**When to use**: For any function that takes user input or reads from disk. The happy path is never enough. Include empty input, missing files, malformed files, and stale state.

---

### 4. Process Forensics (Diagnose hangs and failures)

**Purpose**: When something stalls or crashes, trace to the actual cause — don't guess.

```bash
# Find what a stalled process is doing
cat /proc/<PID>/wchan          # What syscall is it blocked on?
ls -la /proc/<PID>/fd          # What file descriptors are open?
ss -p | grep <PID>             # What sockets? What remote?

# Identify the connection
# Output: tcp ESTAB 127.0.0.1:36480 → 127.0.0.1:11434
# Translation: blocked on Ollama inference

# Then verify the dependency independently
curl -s --max-time 5 http://127.0.0.1:11434/api/tags  # Is Ollama alive?

# Time the actual operation in isolation
python3 -c "
import time, json
from urllib import request
t0 = time.time()
# ... actual call ...
print(f'Elapsed: {time.time()-t0:.1f}s')
"
```

**When to use**: Any time a process takes longer than expected. Never kill without understanding why. If you kill first, you destroyed the evidence.

---

### 5. Structural Verification (HTML, config, cross-references)

**Purpose**: Verify that generated artifacts are internally consistent.

```bash
# HTML structure validation
python3 -c "
from html.parser import HTMLParser
# ... parse and check tag balance ...
print(f'HTML valid ({line_count} lines)')
"

# Cross-reference check (does setup.sh reference files that exist?)
python3 -c "
import re, os
content = open('setup.sh').read()
paths = re.findall(r'SCRIPT_DIR/([^\s\"]+)', content)
missing = [p for p in paths if not os.path.exists(p)]
if missing: print(f'MISSING: {missing}')
else: print('All references valid')
"

# Schema consistency (do artifact counts match what the health agent expects?)
python3 scripts/palette_stats.py --json | python3 -c "
import sys, json
d = json.load(sys.stdin)
assert d['rius_total'] == 131, f'RIU count drift: {d[\"rius_total\"]}'
print('Counts consistent')
"
```

**When to use**: After any change that touches multiple files or generates output consumed by other systems. Cross-file consistency is a product requirement, not cleanup.

---

## Relationship to the Integrity Engine

This pattern IS the integrity engine, executed manually. The mapping:

| Manual Technique | Automated Equivalent | Signal File |
|---|---|---|
| Syntax/import check | `validate_artifact()` in infra.py | Inline (blocks storage) |
| Functional execution | Intent test suite (`test_protect_research_decide.py`) | `gap_signals.ndjson` |
| Edge case probing | Schema rules in `ARTIFACT_SCHEMAS` | Validation errors in frontmatter |
| Process forensics | `emit_integrity_signal(details=f"elapsed={ms}ms")` | `gap_signals.ndjson` |
| Structural verification | `total_health_check.py` (159 checks) | Health report |

**The insight**: The integrity engine automates the checks that can be automated. The manual pattern covers what can't be — novel failures, performance regressions, integration bugs that only appear when real services interact.

**The loop**:
```
Manual validation discovers a new failure mode
  → Write it as an automated check
    → Integrity engine catches it next time
      → Manual validation moves to the next frontier
```

This is how the system gets smarter without getting brittle.

---

## BDB Demo Gate

This gate MUST run before recording the BDB demo. The demo is not approved until these checks are complete.

| # | Claim | Command Type | Required Result | Status Rule |
|---|---|---|---|---|
| 1 | Perplexity key is valid | Live API probe | HTTP 200 from `api.perplexity.ai/chat/completions` | 401/403 is FAIL, not degraded |
| 2 | Ollama is responsive | Local API probe | `http://127.0.0.1:11434/api/tags` responds within 5s | Timeout is FAIL |
| 3 | Required Ollama model exists | Local API parse | Demo model appears in `/api/tags` | Missing model is FAIL |
| 4 | Gateway tests pass | `unittest` | 12/12 gateway tests pass | pytest shadowing does not block this |
| 5 | `palette stats` runs | CLI execution | Human output and `--json` both succeed | Import error is FAIL |
| 6 | `[CONNECT]` fires | CLI execution | Moments 2 and 3 show `[CONNECT]` | Missing signal is FAIL for demo proof |
| 7 | DECIDE runtime is bounded | Timed execution | Realistic DECIDE path completes under agreed target | Exceeding target is FAIL |
| 8 | Demo command completes | End-to-end CLI | `palette demo sarah` or approved fast path completes | Hang is FAIL |
| 9 | Public landing page loads | HTTP/browser check | `missioncanvas.ai` loads expected build | Broken deploy is FAIL if link is submitted |
| 10 | PII public-surface audit passes | grep/audit command | No secrets/client data in public subtree | Finding is FAIL until removed or excluded |

Minimum report format:

```text
BDB Demo Gate Result
1 Perplexity key: PASS|FAIL|BLOCKED - evidence
2 Ollama responsive: PASS|FAIL|BLOCKED - evidence
3 Ollama model: PASS|FAIL|BLOCKED - evidence
4 Gateway tests: PASS|FAIL|BLOCKED - evidence
5 palette stats: PASS|FAIL|BLOCKED - evidence
6 CONNECT signal: PASS|FAIL|BLOCKED - evidence
7 DECIDE runtime: PASS|FAIL|BLOCKED - evidence
8 Demo command: PASS|FAIL|BLOCKED - evidence
9 Landing page: PASS|FAIL|BLOCKED - evidence
10 PII audit: PASS|FAIL|BLOCKED - evidence
Decision: APPROVE RECORDING | DO NOT RECORD | RECORD WITH WAIVER
Waivers required:
```

Hard rule: if checks 1, 2, 6, 7, or 8 fail, do not record a live demo. Use cache/pre-recording only after explicitly labeling the primary path failure.

---

## Where Else to Apply This Pattern

### 1. Gemini Stress Tests

Current stress tests validate data consistency. They should also:

```bash
# Time the actual retrieval path
python3 -c "
import time
from scripts.palette_intents.infra import resolve_query
t0 = time.time()
result = resolve_query('Delaware fiduciary duty')
elapsed = time.time() - t0
assert elapsed < 2.0, f'Resolve too slow: {elapsed:.1f}s'
assert result['confidence'] > 30, f'Confidence too low: {result[\"confidence\"]}'
print(f'Resolve: {elapsed:.1f}s, {result[\"riu_id\"]} @ {result[\"confidence\"]}%')
"
```

**Pattern**: Don't just check "did it return the right RIU?" — check "did it return it fast enough to be usable in a demo?"

### 2. Voice Hub Validation

The Voice Hub serves SSE streams. Validate the actual stream, not just "server starts":

```bash
# Does the hub actually stream tokens?
timeout 10 curl -sN -X POST http://localhost:7890/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"agent":"perplexity","text":"test","lang":"eng"}' | head -5

# Does it emit the palette governance event?
# Look for: event: palette\ndata: {"riu_id":...}
```

### 3. Peers Bus Message Lifecycle

Don't just test `/send` — test the full lifecycle:

```bash
python3 -c "
import json, uuid
from urllib import request

bus = 'http://127.0.0.1:7899'
msg_id = str(uuid.uuid4())

# Send
send_payload = json.dumps({...}).encode()
# ... send ...

# Fetch (verify delivery)
fetch_payload = json.dumps({'identity':'test.agent'}).encode()
# ... fetch ...
assert msg_id in [m['message_id'] for m in result['messages']]

# Verify state transition
# ... fetch again — should be marked delivered ...
print('Full lifecycle: PASS')
"
```

### 4. Demo Recording Validation

Before recording, run the BDB Demo Gate. Do not substitute intuition for this gate. The validation must prove the exact demo path or explicitly name the fallback path.

```bash
# 1. Ollama MUST respond within 5 seconds.
curl -s --max-time 5 http://127.0.0.1:11434/api/tags | python3 -c "..."

# 2. Perplexity MUST return HTTP 200 for the active key.
# HTTP 401 means invalid key. HTTP 403 means unauthorized. Either is FAIL.
python3 -c "
from urllib import request
# ... live Perplexity probe ...
"

# 3. DECIDE MUST finish under the agreed recording target.
python3 -c "
import time
# ... time a realistic DECIDE call ...
assert elapsed < 60, f'Too slow for video: {elapsed}s'
"

# 4. [CONNECT] MUST appear in the relevant demo moments.
python3 scripts/palette_intent.py research 'fiduciary duty' 2>&1 | grep '\[CONNECT\]'
```

If any required check fails, stop. Record the failure, root cause, and fallback decision.

### 5. Pre-Commit Validation Hook

This pattern could become a git pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit (or via palette hook system)

# Syntax check all staged Python files
git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | while read f; do
  python3 -c "import ast; ast.parse(open('$f').read())" || exit 1
done

# Verify palette stats still runs (no import breakage)
python3 scripts/palette_stats.py --json > /dev/null 2>&1 || {
  echo "ERROR: palette stats broken by this commit"
  exit 1
}
```

### 6. Cron Governance Validation

Before a cron schedule fires, prove the governance chain:

```bash
python3 -c "
from scripts.palette_cron import load_schedules, check_governance, is_due
for s in load_schedules():
    ok, reason = check_governance(s)
    due = is_due(s)
    status = '✓' if ok else '✗'
    print(f'{status} {s[\"id\"]:30s} due={due} {reason if not ok else \"\"}')
"
```

### 7. Artifact Schema Drift Detection

After bulk operations, verify no schema drift:

```bash
python3 -c "
from pathlib import Path
import yaml

artifacts = Path('.palette/artifacts')
drift = []
for f in artifacts.rglob('*.md'):
    text = f.read_text()
    if not text.startswith('---'):
        drift.append(f'No frontmatter: {f}')
        continue
    try:
        end = text.index('---', 3)
        fm = yaml.safe_load(text[3:end])
        if not fm.get('artifact_type'):
            drift.append(f'Missing artifact_type: {f}')
        if not fm.get('timestamp'):
            drift.append(f'Missing timestamp: {f}')
    except Exception as e:
        drift.append(f'Parse error: {f}: {e}')

if drift:
    print(f'DRIFT DETECTED: {len(drift)} issues')
    for d in drift[:5]: print(f'  {d}')
else:
    print(f'Schema integrity: {sum(1 for _ in artifacts.rglob(\"*.md\"))} artifacts, 0 drift')
"
```

---

## Invalid Validation Patterns

These are not acceptable:

- "The code looks correct."
- "The unit test passed, so the integration is fine."
- "The fallback worked, so the primary path is fine."
- "The process hung, so I killed it and moved on."
- "The API probably failed because of the network."
- "The demo worked yesterday."
- "The dependency is installed because the docs say so."
- "This warning is probably cosmetic."

Every one of these statements must be replaced with a command result or a named blocker.

---

## The Principle

**The terminal is the truth.**

- If you didn't run it, you don't know it works.
- If you didn't time it, you don't know it's fast enough.
- If you didn't trace the failure, you don't know why it broke.
- If you didn't record the signal, you can't detect regression.

This isn't testing. Testing is "does the unit pass?" This is validation: "does the system behave correctly when real data flows through real services under real constraints?"

The difference matters because:
- Tests pass in CI with mocked dependencies. Validation catches the Ollama hang.
- Tests check function signatures. Validation checks that the demo finishes in under 3 minutes.
- Tests are written once. Validation is a practice — you do it every time, adapting to what you just built.

---

## Gemini Handoff Instructions

Gemini: use this document as an execution spec, not as background reading. Your task is to stress-test the current BDB system state using terminal-first validation.

You MUST do the following:

1. Run the BDB Demo Gate.
2. Produce the exact validation report format defined above.
3. Mark every check as `PASS`, `FAIL`, or `BLOCKED`.
4. Include the command used for every check.
5. Include the observed output or the decisive excerpt from the output.
6. Identify the root cause for every `FAIL`.
7. Identify the missing dependency or permission for every `BLOCKED`.
8. End with one of exactly three decisions: `APPROVE RECORDING`, `DO NOT RECORD`, or `RECORD WITH WAIVER`.

You MUST NOT do the following:

- Do not infer from code inspection that a dependency works.
- Do not treat local fallback as proof that external routing works.
- Do not change implementation code while running the validation pass.
- Do not broaden the scope beyond the BDB Demo Gate unless Mical asks.
- Do not hide failures inside a summary paragraph.
- Do not use soft language such as "appears," "probably," "should," or "likely" for a validation result. Use command evidence.

Expected output file:

```text
bdb/GEMINI_BDB_DEMO_GATE_REPORT_2026-05-29.md
```

If a command cannot run because of missing credentials, missing services, sandbox restrictions, or unavailable ports, mark it `BLOCKED`. Do not invent a workaround and call it equivalent.

---

## Promotion Criteria

This pattern MUST NOT be promoted to `palette-core.md` by enthusiasm alone. Promote it only when:

- [ ] It consistently prevents shipping broken features (evidence: 0 regressions in BDB build)
- [ ] It reduces ambiguity about system state (evidence: handoff report was precise, not aspirational)
- [ ] It remains debuggable (evidence: every check is a one-liner, reproducible)
- [ ] It generalizes across domains (evidence: applies to intents, bus, hub, gateway, demo, cron)
- [ ] It introduces no hidden state (evidence: all signals go to gap_signals.ndjson or stdout)
- [ ] Human explicitly approves promotion

---

*Documented by kiro.design. 2026-05-29.*
