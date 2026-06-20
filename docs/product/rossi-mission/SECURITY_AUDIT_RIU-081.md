# Mission Canvas — Security Audit (RIU-081)

**Auditor**: claude.analysis
**Date**: 2026-03-28
**Scope**: Data flow risks, PII policy, one-way-door classification
**Status**: COMPLETE — awaiting crew review

---

## 1. fetch_signals — Path Traversal Risk

**Current state**: Stub (hardcoded data). But the tool definition accepts `file_path` as a free-text string parameter.

**Risk**: When implemented, a malicious or careless input like `/etc/passwd`, `~/.ssh/id_rsa`, or `../../.env` would be processed if no path validation exists.

**Required controls**:
```
ALLOW_LIST_DIRS = [
  "/home/mical/fde/implementations/retail/retail-rossi-store/",
  "/home/mical/fde/implementations/retail/retail-rossi-store/data/"
]
```

- **MUST**: Resolve symlinks before comparison (`fs.realpathSync`)
- **MUST**: Reject any path outside ALLOW_LIST_DIRS
- **MUST**: Reject dotfiles (`.env`, `.git/`, `.ssh/`)
- **MUST**: Only allow extensions: `.pdf`, `.csv`, `.json`, `.txt`
- **SHOULD**: Log every file access attempt (path, result, timestamp)

**Classification**: TWO-WAY DOOR (can be changed later, but implement before any real file parsing)

---

## 2. PII Scrubbing Policy

Any signal extracted from local files must be scrubbed before it enters the bus, the UI, or any log. The following fields are PII and MUST be stripped or hashed before output:

### STRIP (remove entirely)
- Full names (person, business owner)
- Email addresses
- Phone numbers
- Street addresses (number + street)
- Social Security / Tax ID numbers
- Bank account / routing numbers
- Credit card numbers
- Dates of birth

### GENERALIZE (replace with range or category)
- Revenue: exact dollar amounts -> range brackets ($0-25k, $25-50k, $50-100k, $100-250k, $250k+)
- Employee count: exact -> range (1-5, 6-20, 21-50, 50+)
- Location: full address -> city + state only (or zip code prefix)

### PASS THROUGH (safe to include)
- Industry classification (NAICS code, retail category)
- Revenue range (already generalized)
- Business structure (LLC, sole prop, etc.)
- Year established (not DOB)
- Grant eligibility signals (yes/no per program)
- Growth indicators (trending up/down/stable)

### Implementation
- Scrubbing MUST happen inside `fetch_signals` before the return value
- The raw parsed data must NEVER be logged, stored, or sent over the bus
- Use regex patterns for detection (email, phone, SSN, credit card)
- For names: strip any field labeled "name", "owner", "contact", "applicant"

**Classification**: ONE-WAY DOOR — once PII leaks into a log or message, it cannot be recalled. This policy is Tier 1 (immutable once approved).

---

## 3. One-Way-Door Classification

### ONE-WAY DOORS (require human approval)

| Action | Why | Gate |
|--------|-----|------|
| GitHub publish (`/relay update_request publish:...`) | Public exposure of business data | Already gated in rossi_bridge.py (metadata only, no auto-exec) |
| Sending signal data to external API | PII could leak to third party | Must be blocked entirely in v1 |
| Deleting or overwriting local business files | Irreversible data loss | Block in fetch_signals (read-only) |
| Changing PII scrubbing rules | Weakening rules could leak PII retroactively | Tier 1 policy change = human review |
| Sending execution_request with risk=critical | Autonomous action on critical decisions | Already gated by broker (waiting_human) |

### TWO-WAY DOORS (safe to proceed)

| Action | Why |
|--------|-----|
| Reading local files (within allowlist) | Non-destructive, local-only |
| Extracting signals to display in Canvas UI | Scrubbed data stays local |
| Sending informational messages on the bus | No execution, reversible |
| Updating Canvas UI layout/styling | Visual only, no data impact |
| Logging decisions to decisions.md | Append-only, non-destructive |

---

## 4. rossi_bridge.py — Existing Controls (Good)

The existing relay has solid security patterns we should preserve:

1. **Intent allowlist** (line 300-308): Only 5 allowed intents. Unknown intents rejected.
2. **Sender allowlist** (line 558-563): `ROSSI_RELAY_ALLOWLIST` restricts who can use `/relay`.
3. **Idempotency** (line 309-311): Prevents duplicate artifact creation.
4. **Publish is metadata-only** (line 316): "still not executed in v1" — GitHub publish path is documented but intentionally not wired.
5. **Trace logging** (line 341-353): Every relay action gets an event with trace_id, source, direction.

**Carry forward to Mission Canvas**: All 5 patterns must be preserved. The Canvas should not be "more permissive" than the existing bridge.

---

## 5. Gemini server.mjs — Issues Found

1. **No path validation on fetch_signals_PROTOTYPE** (line 101-106): Accepts any `file_path` string. When real implementation lands, this is the #1 attack surface.

2. **No rate limiting**: The MCP server accepts unlimited tool calls. A runaway agent could hammer the broker or parse thousands of files.

3. **No input sanitization on peers_send payload**: The payload object is passed through to the broker as-is. If it contains script tags or injection payloads, they'd be stored in SQLite and potentially rendered in the Canvas UI. Codex: sanitize before rendering.

4. **Missing tools vs other adapters**: Gemini's adapter now has `peers_checkpoints`, `peers_approve`, `peers_reject`, `peers_thread` (fixed from earlier). But `fetch_signals_PROTOTYPE` should be renamed to `fetch_signals` once real implementation ships — the PROTOTYPE suffix is good for now.

---

## 6. Recommendations

### For Codex (Canvas UI)
- Sanitize ALL data before rendering in HTML (escape `<`, `>`, `&`, `"`, `'`)
- Never use `innerHTML` with bus message content — use `textContent`
- Add CSP header: `Content-Security-Policy: default-src 'self'`

### For Gemini (fetch_signals)
- Implement path allowlist FIRST, before any file parsing
- Make fetch_signals read-only — never write, delete, or modify source files
- Return scrubbed signals only — never return raw file content
- Add timeout: abort parsing after 10 seconds (prevents DoS from large files)

### For Kiro (local endpoint)
- If building a local prompt runner, it must NOT have network access to external APIs
- All agent routing must stay local (no external LLM calls from the endpoint itself)
- Log every route decision to decisions.md

---

## 7. Decision Record

```
DATE: 2026-03-28
DECISION: PII scrubbing policy for Mission Canvas signal extraction
TYPE: ONE-WAY DOOR
CLASSIFICATION: Tier 1 (immutable once approved)
DECIDED_BY: Proposed by claude.analysis, awaiting human.operator approval
RATIONALE: Once PII enters logs or bus messages, it cannot be recalled.
            Local-first constraint is meaningless without scrubbing at extraction boundary.
STATUS: PROPOSED — requires human ACK before fetch_signals implementation begins
```
