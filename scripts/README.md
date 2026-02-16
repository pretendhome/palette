# Palette Scripts

## `sync-impressions.py`

**Purpose**: Aggregate agent impressions from implementation decision logs to global agent maturity tracker.

**Location**: `/home/mical/fde/palette/scripts/sync-impressions.py`

---

## Usage

```bash
# Dry run (see what would change)
python3 palette/scripts/sync-impressions.py --dry-run

# Sync for real
python3 palette/scripts/sync-impressions.py

# Review changes
cd palette && git diff agents/README.md

# Commit if looks good
git add agents/README.md
git commit -m "sync: Update agent maturity from project impressions"
```

---

## What It Does

1. **Scans** all implementation decision logs:
   - `implementations/*/decisions.md`
   - `implementations/*/*/execution_summary.md`

2. **Extracts** agent impressions:
   - Looks for `**Impressions**: X success, Y fail` format
   - Matches to agent names (Argentavis, Tyrannosaurus, etc.)

3. **Aggregates** across projects:
   - Sums success/fail counts per agent
   - Tracks which projects contributed

4. **Calculates** maturity tier:
   - UNVALIDATED: 0-9 successes
   - WORKING: 10+ successes, <5% failure
   - PRODUCTION: 50+ successes, <5% failure

5. **Updates** `/palette/agents/README.md`:
   - Replaces "Current Status" section
   - Shows impressions, tier, next milestone

---

## When To Run

**After project work** that logs agent impressions:
- Completed a multi-agent workflow
- Agent succeeded/failed on a task
- Want to see global maturity status

**Before releases**:
- Validate agent maturity before tagging version
- Update README for accurate status

**Weekly** (recommended):
- Keep global status in sync with project work
- Catch promotion opportunities (agents reaching 10 or 50 impressions)

---

## Expected Output

```
Scanning project decision logs...
  Parsing implementations/dev-mythfall-game/decisions.md...
  Parsing implementations/retail-rossi-store/decisions.md...
  Parsing implementations/talent-gap-interview/execution_summary.md...

Found impressions for 4 agents:
  Yutyrannus: 10 success, 0 fail
  Argentavis: 6 success, 0 fail
  Tyrannosaurus: 1 success, 0 fail
  Ankylosaurus: 1 success, 0 fail

Generating status table...

Updating agents/README.md...
✅ Updated /home/mical/fde/palette/agents/README.md

✅ Sync complete. Review changes and commit.
```

---

## Troubleshooting

**No impressions found?**
- Check decision logs use format: `**Impressions**: X success, Y fail`
- Check agent headers use format: `### AgentName (shortname)`
- Run with `--dry-run` to see which files are scanned

**Wrong counts?**
- Verify decision logs have correct numbers
- Script sums across all projects (intentional)
- Check for duplicate entries in same file

**Script fails?**
- Ensure running from `/home/mical/fde/` directory
- Check Python 3.11+ installed
- Verify file paths haven't changed

---

## `validate_palette_state.py`

**Purpose**: Drift guard that checks path consistency, taxonomy count consistency, duplicate library IDs, and Orchestrator guardrails.

### Usage

```bash
python3 palette/scripts/validate_palette_state.py
```

### CI Integration

This script is wired into `.github/workflows/palette-integrity.yml` and runs on pushes/PRs that touch `palette/**` or `implementations/**`.

---

## `company_intel_report.py`

**Purpose**: Generate `company_intel_report.md` from the company-RIU mapping to support build-vs-buy and pattern adoption analysis.

### Usage

```bash
python3 palette/scripts/company_intel_report.py
```

---

## Future: Git Hook Automation

**✅ IMPLEMENTED** (2026-02-10)

Git hook installed at `.git/hooks/post-commit`:

```bash
# Automatically runs when you commit decision log changes
# 1. Detects changes to decisions.md or execution_summary.md
# 2. Runs sync-impressions.py
# 3. Amends commit with updated agents/README.md
# 4. Pushes to GitHub
```

**How it works:**
- Commit any decision log → Hook auto-syncs → GitHub updated
- No manual sync needed
- Recursion-safe (won't trigger on amended commits)

**To disable:**
```bash
rm .git/hooks/post-commit
```

**To re-enable:**
```bash
cp palette/scripts/post-commit.sh .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```
