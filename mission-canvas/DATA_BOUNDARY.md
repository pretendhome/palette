# Mission Canvas — Data Boundary Policy
# Classification: TIER 1 (IMMUTABLE) — ONE-WAY DOOR
# Changing this policy requires explicit human approval.
# Date: 2026-03-31
# Applies to: ALL workspaces, ALL users, ALL channels (MCP, Telegram, Web UI)

---

## Rule 1: No Personal Data on the VPS — EVER

The VPS is a shared relay. It runs workspace intelligence (facts, decisions,
health scores, monitors, alerts). It MUST NEVER contain:

### BANNED from VPS (hard block)
- Full legal names (use first name or alias only)
- Email addresses
- Phone numbers
- Street addresses (number + street)
- Social Security / Tax ID / passport numbers
- Bank account / routing numbers
- Credit card numbers
- Dates of birth
- Exact portfolio positions (dollar amounts, share counts, cost basis)
- Exact revenue/income figures
- Deal memos, term sheets, contracts
- Medical or health information
- Login credentials, API keys belonging to the user
- Any file uploaded from the user's local machine

### ALLOWED on VPS (sanitized only)
- First name or chosen alias ("Joseph", "Investor")
- City only, no street ("San Francisco", "London")
- Industry and domain ("oil & gas", "AI investments")
- Role description ("energy sector investor")
- Risk posture (low / medium / high / aggressive)
- Investment horizon ("3-5 years")
- Portfolio exposure by category ("upstream-heavy", "evaluating midstream")
- Revenue/position ranges ONLY ("$100K-250K range", "significant exposure")
- Growth indicators (up / down / stable)
- Business structure (LLC, fund, personal)
- Abstract investment thesis ("positioned for Hormuz crisis refining supercycle")
- Health scores, decisions, evidence gaps (workspace metadata)
- Alerts from public market data (Perplexity research results)
- Facts added by the user (user controls what they share)

---

## Rule 2: The User Controls What Gets Shared

The `add-fact` and `resolve-evidence` endpoints accept free text from the user.
The user decides what to share. The system MUST:

1. Never auto-extract facts from local files and push to VPS
2. Never send file contents to the VPS
3. Never include file paths from the user's machine in VPS data
4. Always require explicit user action to add data to the workspace

Claude/Codex reading local files on the user's laptop is fine — that stays
local. The MCP remote server only sends what the user approves.

---

## Rule 3: The Lens Stays Local

Each user has a `lens.yaml` on their local machine. This contains the full
context built from their private files. It NEVER goes to the VPS.

What goes to the VPS instead: `profile.md` — a sanitized summary with ONLY
the ALLOWED fields listed above.

```
LOCAL (user's laptop)              VPS (shared relay)
├── lens.yaml (FULL — private)     ├── profile.md (SANITIZED)
├── deal_memos/ (private)          ├── project_state.yaml
├── financials/ (private)          ├── monitors/
├── contracts/ (private)           ├── alerts/
└── Claude reads all of this       └── NO personal files ever
```

---

## Rule 4: Monitors Use Public Data Only

The monitor daemon searches public sources (via Perplexity API) for market
news and company updates. It NEVER accesses or references user's private data.
Monitor alerts contain only publicly available information.

---

## Rule 5: Telegram Bridge Is Read-Only Relay

The Telegram bridge relays messages between the user and the VPS workspace.
It MUST NOT:
- Access local files on any machine
- Store message content beyond the session log (which lives on VPS, contains
  only the user's own messages to the bot — no private file data)
- Forward messages to any third party
- Share chat IDs or user identifiers externally

---

## Rule 6: Enforcement

### Code-level enforcement (hard blocks):
- `data_boundary.mjs` validates ALL data before it enters `project_state.yaml`
- PII regex patterns block: SSN, phone, email, credit card, full addresses
- Dollar amounts with more than 4 digits are blocked (use ranges)
- File paths from user machines are blocked

### Policy-level enforcement:
- This document is TIER 1 (immutable without human approval)
- Changing scrubbing rules is a ONE-WAY DOOR — requires human review
- Once PII leaks into logs, it CANNOT be recalled
- Any agent or tool that touches user data must respect this boundary

### Audit:
- All `add-fact` and `resolve-evidence` calls are logged with timestamp
- Logs can be audited for PII violations
- Any violation triggers immediate alert to workspace owner

---

## Rule 7: ONE-WAY DOORS (require human approval)

| Action | Risk | Gate |
|--------|------|------|
| Publishing workspace data externally | Data exposure | Human approval required |
| Sending data to external API (not Perplexity public search) | PII leak | Blocked in v1 |
| Changing this data boundary policy | Retroactive exposure | Tier 1 — human approval |
| Sharing workspace between users | Cross-user data leak | Human approval required |
| Deleting scrubbing rules | PII could enter logs | Tier 1 — human approval |

---

## Summary

**The VPS knows WHAT you're working on (abstract). It never knows WHO you are
(specific) or WHAT you have (specific amounts).** The user's private data
stays on their laptop. Always. No exceptions.
