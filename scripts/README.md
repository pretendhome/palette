# Impression Sync Script

**Purpose**: Aggregate agent impressions from project decision logs to global agent maturity tracker.

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

1. **Scans** all project decision logs:
   - `projects/*/decisions.md`
   - `projects/*/*/execution_summary.md`

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
  Parsing projects/myth-fall-game/decisions.md...
  Parsing projects/rossi-mission/decisions.md...
  Parsing projects/agent-class/interview-prep/execution_summary.md...

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
- Check Python 3.12+ installed
- Verify file paths haven't changed

---

## Future: Git Hook Automation

Once validated, can add post-commit hook:

```bash
# .git/hooks/post-commit
#!/bin/bash
if git diff --name-only HEAD~1 | grep -q "projects/.*/decisions.md"; then
    python3 palette/scripts/sync-impressions.py
    git add palette/agents/README.md
    git commit --amend --no-edit
fi
```

**Not implemented yet** - validating manual workflow first.
