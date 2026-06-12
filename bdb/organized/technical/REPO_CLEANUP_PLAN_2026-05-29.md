# Repo Cleanup Plan — Architectural Approach
**Date**: 2026-05-29
**Process**: Dogfooded through Palette (RESEARCH → DECIDE → CREATE)
**Decision**: TWO-WAY DOOR — proceed. Current commit `db5c6ba` is the rollback point.
**Deadline**: June 2 (BDB submission)

---

## What Judges and Visitors Want to See

From web research + competitive analysis (Hermes 140K stars, OpenClaw 347K stars):

1. **README that answers "what is this?" in 10 seconds** — ours is rewritten, ready
2. **One-command setup** — `bash setup.sh` — done
3. **Working demo** — `palette demo sarah` — done
4. **Clean directory structure** — obvious what each folder does
5. **Tests that pass** — `pytest` returns green
6. **No junk** — no generated output, no build artifacts, no 3,259 old bus messages
7. **Evidence of real usage** — `palette stats` shows 260 artifacts, 29 RIUs activated

The top AI repos (Hermes, OpenClaw, LangChain) all share: flat top-level, clear naming, docs/ is small, tests/ is visible, examples/ shows how to use it.

---

## Target Structure (Post-Cleanup)

```
palette/
├── README.md                    # "Mission Canvas — Your judgment compounds here"
├── QUICKSTART.md                # "bash setup.sh" → running in 60 seconds
├── setup.sh                     # One-command install
├── MANIFEST.yaml                # System state
├── CLAUDE.md                    # Agent steering
├── LICENSE                      # Apache 2.0
├── decisions.md                 # Append-only governance log
│
├── core/                        # Tier 1 governance (immutable rules)
├── taxonomy/                    # 131 RIU routing nodes
├── knowledge-library/           # 203 entries, 565 citations
│
├── scripts/                     # CLI + intent framework + PIS engine
│   ├── palette_intent.py        # Entry point: palette protect/research/decide/...
│   ├── palette_stats.py         # palette stats
│   ├── palette_cron.py          # Governed scheduled intents
│   ├── palette_query.py         # Legacy query interface
│   ├── palette_orchestrate.py   # Orchestration
│   ├── palette_intents/         # 6 intent implementations
│   └── palette_intelligence_system/  # Integrity engine + tests
│
├── agents/                      # Health + total-health + active agents only
│   ├── health/
│   ├── total-health/
│   ├── resolver/
│   └── remediation/             # Shared loop infra
│
├── peers/                       # Message bus + Voice Hub
│   ├── broker/                  # Bus core (index.mjs, db.mjs, gates, validate)
│   ├── hub/                     # Voice Hub (server.mjs)
│   ├── adapters/                # MCP adapters
│   └── migrations/              # Schema migrations
│
├── mission-canvas/              # Telegram bot + deployment
│   ├── mc_telegram.py
│   ├── server.mjs               # MC server (keep for now)
│   ├── index.html               # MC web UI
│   └── systemd/
│
├── bdb/                         # Competition material (private)
│   ├── gateway/                 # Perplexity gateway + sanitizer
│   ├── DEMO_SCRIPT_FINAL.md
│   └── *.md                     # Specs, intel, plans
│
├── buy-vs-build/                # Service routing + recipes
│   ├── integrations/            # 76 recipes
│   ├── service-routing/
│   └── people-library/
│
├── skills/                      # Validated domain skills (keep active only)
│   ├── retail-ai/
│   ├── education/
│   ├── travel/
│   └── talent/                  # Generic methodology only (PII files already gitignored)
│
├── sdk/                         # Agent SDK
├── lenses/                      # Generic role lenses only (24)
├── docs/
│   ├── landing/                 # missioncanvas.ai landing page
│   └── specs/                   # Active specs only
│
├── legal/                       # Trademarks
├── .palette/                    # Runtime state (artifacts, schedules, cache)
└── .steering/                   # Agent steering (active files only)
```

---

## Execution Plan

### Safety Net
```bash
# Tag current state before any changes
git tag pre-cleanup-2026-05-29
```

### Phase 1: Zero-Risk Archive (generated/historical output)
Move to `archive/standby-2026-05-29/`. These are ALL generated or historical — zero import risk.

```bash
# 3,259 historical bus messages (15MB)
mv peers/dropbox/inbox/ archive/standby-2026-05-29/peers-inbox/

# 624 generated wiki pages (rebuildable with compile_wiki.py)
mv wiki/ archive/standby-2026-05-29/wiki/

# 965 remediation evidence packets (generated)
mv artifacts/ archive/standby-2026-05-29/artifacts-remediation/

# 69 voice workbench audio files (6.4MB, dormant)
mv voice/ archive/standby-2026-05-29/voice/
```

**Files removed**: ~4,917
**Regression risk**: ZERO — none of these are imported by anything

### Phase 2: Dormant Agents (superseded by v2 or intents)
```bash
# v1 agents superseded by v2
mv agents/validator/validator.py archive/standby-2026-05-29/agents-v1/
mv agents/debugger/debugger.py archive/standby-2026-05-29/agents-v1/
mv agents/builder/builder.py archive/standby-2026-05-29/agents-v1/

# Design-only agents (no implementation)
mv agents/architect/ archive/standby-2026-05-29/agents-dormant/
mv agents/narrator/ archive/standby-2026-05-29/agents-dormant/
mv agents/monitor/ archive/standby-2026-05-29/agents-dormant/
mv agents/orchestrator/ archive/standby-2026-05-29/agents-dormant/
mv agents/business-plan-creation/ archive/standby-2026-05-29/agents-dormant/
mv agents/researcher/ archive/standby-2026-05-29/agents-dormant/
```

**Verify after**: `python3 agents/total-health/total_health_check.py` still passes

### Phase 3: Stale Documentation
```bash
# Historical audits (33 files)
mv docs/audits/ archive/standby-2026-05-29/docs-audits/

# Old research notes
mv docs/research/ archive/standby-2026-05-29/docs-research/

# Old competition entries
mv docs/competitions/ archive/standby-2026-05-29/docs-competitions/

# Voice workbench docs
mv docs/voice-workbench/ archive/standby-2026-05-29/docs-voice-workbench/

# Keep: docs/landing/, docs/specs/, docs/product/ (has moat doc)
```

### Phase 4: Mission Canvas Cleanup
```bash
# Old competition entries
mv mission-canvas/competitions/ archive/standby-2026-05-29/mc-competitions/

# Old archive
mv mission-canvas/archive/ archive/standby-2026-05-29/mc-archive/

# Workspace data (PII — user-specific)
mv mission-canvas/workspaces/ archive/standby-2026-05-29/mc-workspaces/
```

### Phase 5: Other Dormant Directories
```bash
# Bridges (superseded by mc_telegram.py)
mv bridges/ archive/standby-2026-05-29/bridges/

# Plugins (Obsidian — shipped, dormant)
mv plugins/ archive/standby-2026-05-29/plugins/

# Analysis (one-off)
mv analysis/ archive/standby-2026-05-29/analysis/

# Existing archive
# Leave archive/ as-is — it's already archive
```

### Phase 6: .gitignore + Verify
```bash
# Add archive to gitignore
echo "archive/standby-2026-05-29/" >> .gitignore

# Verify nothing broke
python3 scripts/palette_intent.py research "test query"     # Intent works
python3 scripts/palette_stats.py                            # Stats works
python3 scripts/palette_intent.py demo sarah               # Demo works (interactive)
python3 -m pytest -q scripts/palette_intelligence_system/test_*.py  # 60 tests
python3 agents/total-health/total_health_check.py           # Health check
```

### Phase 7: Commit + Push
```bash
git add -A
git commit -m "refactor: archive 5000+ generated/historical files — clean repo for BDB"
git push origin main
git subtree push --prefix=palette palette main
```

---

## Rollback Plan
```bash
git checkout pre-cleanup-2026-05-29 -- .
# or
git reset --hard pre-cleanup-2026-05-29
```

---

## Verification Checklist

- [ ] `palette demo sarah` completes all 3 moments
- [ ] `palette stats` shows correct counts
- [ ] `palette research "test"` classifies and responds
- [ ] `palette cron list` shows schedules
- [ ] 60/60 PIS tests pass
- [ ] Total health: no NEW failures vs pre-cleanup baseline
- [ ] Landing page loads in browser
- [ ] README reads clean
- [ ] Top-level `ls` looks professional

---

*Plan generated through Palette intents (RESEARCH → DECIDE → CREATE). Decision: TWO-WAY DOOR. Rollback tag: `pre-cleanup-2026-05-29`.*
