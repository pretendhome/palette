# Post-Submission Repo Restructure Plan
**Date**: 2026-06-02
**Author**: claude.analysis
**Status**: EXECUTE AFTER BDB SUBMISSION
**Base**: Perplexity Computer repo structure spec (2026-06-02) + build day lessons
**Risk level**: Each phase tested before committing. No big-bang rename.

---

## Principle: One Rename Per Commit, Test Between Each

The last restructure broke everything because multiple moves happened at once and import paths cascaded. This plan does ONE rename per commit, runs tests after each, and only proceeds if green.

---

## Phase 1: Zero-Risk Cleanup (30 min)

These touch no import paths. Nothing can break.

| # | Action | Command | Risk |
|---|---|---|---|
| 1.1 | Move `decisions.md` → `core/decisions.md` | `git mv decisions.md core/` | Zero — no code imports this |
| 1.2 | Move `litellm_config.yaml` → `config/litellm.yaml` | `git mv litellm_config.yaml config/litellm.yaml` + update setup.sh reference | Low — one reference in setup.sh |
| 1.3 | Move `AGENTS.md` → `docs/AGENTS.md` | `git mv AGENTS.md docs/` | Zero — documentation only |
| 1.4 | Move `QUICKSTART.md` → `docs/QUICKSTART.md` | `git mv QUICKSTART.md docs/` | Zero |
| 1.5 | Move `CHANGELOG.md` → `docs/CHANGELOG.md` | `git mv CHANGELOG.md docs/` | Zero |
| 1.6 | Add `docs/README.md` as docs index | Create new file | Zero |
| 1.7 | Add directory map table to README.md | Edit README | Zero |

**Test**: `uv run pytest -q scripts/palette_intelligence_system/test_*.py` + `node peers/hub/server.mjs` starts clean.

---

## Phase 2: Safe Renames — No Import Path Changes (1 hour)

These rename directories but nothing inside them imports by directory name.

| # | Current | New | Files affected | Risk |
|---|---|---|---|---|
| 2.1 | `knowledge-library/` | `knowledge/` | MANIFEST.yaml, CLAUDE.md, any grep for `knowledge-library` | Low — search and replace |
| 2.2 | `buy-vs-build/` | `intelligence/` | MANIFEST.yaml, CLAUDE.md, recipes reference paths | Low — no code imports, only YAML paths |
| 2.3 | `wiki/` | `docs/wiki/` | Hub server.mjs `WIKI_ROOT` default path | Low — one reference |
| 2.4 | `bdb/` | `docs/competition/bdb-2026/` | No code references — only documentation | Zero |

**For each rename:**
```bash
git mv <old> <new>
grep -rn "<old>" --include="*.py" --include="*.mjs" --include="*.yaml" --include="*.md" . | grep -v node_modules | grep -v archive
# Fix every reference found
# Commit
# Test
```

**Test after each**: Full test suite + hub starts + `palette demo sarah` works.

---

## Phase 3: Import Path Changes — Highest Risk (2 hours)

These change Python/Node import paths. Do ONE at a time. Test between each.

### 3.1: `scripts/` → `src/`

This is the riskiest rename. Every Python import in the system references `scripts.palette_intents` or `scripts.palette_intelligence_system`.

**Affected files** (grep first):
```bash
grep -rn "from scripts\.\|import scripts\." . --include="*.py" | grep -v node_modules | grep -v archive
```

**Steps:**
1. `git mv scripts/ src/`
2. Find every `from scripts.` → replace with `from src.`
3. Find every `scripts/` path reference in shell scripts, server.mjs
4. Update `palette` CLI wrapper: `exec python3 ".../src/palette_intent.py"`
5. Update `setup.sh` PATH symlink
6. Test everything

### 3.2: `peers/` → `runtime/`

**Affected files:**
- `setup.sh` — references `peers/broker`, `peers/hub`
- `CLAUDE.md` — documentation references
- `MANIFEST.yaml` — paths
- VPS deployment scripts
- Hub's `__dirname` references are relative so those are fine

**Steps:**
1. `git mv peers/ runtime/`
2. Update setup.sh (5 references)
3. Update CLAUDE.md, MANIFEST.yaml
4. Update VPS rsync paths
5. Test

### 3.3: `mission-canvas/` → `workspaces/`

**Affected files:**
- `setup.sh` — npm install reference
- Terminal voice bridge path
- No Python imports

**Steps:**
1. `git mv mission-canvas/ workspaces/`
2. Update setup.sh
3. Test

---

## Phase 4: Consolidation (1 hour)

### 4.1: Create `config/` directory
```bash
mkdir -p config/schema
git mv core/palette-core.md config/
git mv core/assumptions.md config/
git mv core/decisions-prompt.md config/
git mv core/schema/*.json config/schema/
# Keep core/go.mod, core/packet.go etc. — those are Go code, not config
```

### 4.2: Consolidate tests
```bash
mkdir -p tests/gateway tests/sdk tests/integration
git mv bdb/gateway/tests/* tests/gateway/ 2>/dev/null
git mv sdk/tests/* tests/sdk/ 2>/dev/null
```

### 4.3: Move voice research to docs
```bash
git mv voice/ docs/voice/
```

### 4.4: Move lenses to docs (if not production)
```bash
git mv lenses/ docs/lenses/
```

---

## Phase 5: VPS Sync

After all renames, the VPS deployment paths change. Update:

1. Rsync paths in any deploy scripts
2. Systemd service `WorkingDirectory` paths
3. Nginx proxy config (if hub path changed)
4. Hub's `palette_retrieve.py` spawn path

**Critical**: Test VPS deployment end-to-end after restructure. Don't assume paths survived.

---

## The Dual-Repo Problem

Every rename must happen in BOTH repos (pretendhome monorepo + palette public repo). The safest approach:

1. Make all changes in the monorepo
2. Use `git subtree push --prefix=palette palette main` to sync
3. If subtree push fails (history divergence), clone palette fresh, apply the same git mv commands, push

**Or**: After restructure, reset the palette repo from the monorepo subtree with a force push. This is the nuclear option but it's clean.

---

## What the Root Looks Like After

```
palette/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── MANIFEST.yaml
├── setup.sh
├── install.sh
├── pyproject.toml
├── uv.lock
├── palette                    ← CLI entry point
│
├── src/                       ← Python runtime (was scripts/)
├── runtime/                   ← Node.js runtime (was peers/)
├── agents/                    ← 13 agents
├── sdk/                       ← SDK
├── knowledge/                 ← was knowledge-library/
├── taxonomy/                  ← 131 RIUs
├── intelligence/              ← was buy-vs-build/
├── skills/                    ← domain packs
├── config/                    ← governance, schemas, litellm
├── bridges/                   ← Telegram
├── plugins/                   ← decision board
├── ops/                       ← operational scripts
├── workspaces/                ← was mission-canvas/
├── docs/                      ← all documentation, wiki, competition, voice research
├── tests/                     ← consolidated tests
└── archive/                   ← superseded versions
```

**Root items: 20** (down from 30+). Every directory name is self-explanatory. No `buy-vs-build`, no `bdb`, no orphan files.

---

## Execution Checklist

```
Phase 1: Zero-risk cleanup
  [ ] 1.1 decisions.md → core/
  [ ] 1.2 litellm_config.yaml → config/
  [ ] 1.3 AGENTS.md → docs/
  [ ] 1.4 QUICKSTART.md → docs/
  [ ] 1.5 CHANGELOG.md → docs/
  [ ] 1.6 Create docs/README.md
  [ ] 1.7 Directory map in README
  [ ] TEST: pytest + hub starts

Phase 2: Safe renames
  [ ] 2.1 knowledge-library/ → knowledge/
  [ ] TEST
  [ ] 2.2 buy-vs-build/ → intelligence/
  [ ] TEST
  [ ] 2.3 wiki/ → docs/wiki/
  [ ] TEST
  [ ] 2.4 bdb/ → docs/competition/bdb-2026/
  [ ] TEST

Phase 3: Import path changes
  [ ] 3.1 scripts/ → src/
  [ ] TEST (full suite + CLI + hub + demo)
  [ ] 3.2 peers/ → runtime/
  [ ] TEST
  [ ] 3.3 mission-canvas/ → workspaces/
  [ ] TEST

Phase 4: Consolidation
  [ ] 4.1 Create config/
  [ ] 4.2 Consolidate tests/
  [ ] 4.3 voice/ → docs/voice/
  [ ] 4.4 lenses/ → docs/lenses/
  [ ] TEST

Phase 5: VPS sync
  [ ] Update all VPS paths
  [ ] Update systemd services
  [ ] End-to-end VPS test
  [ ] Sync palette public repo

DONE: Root has ≤20 items, all self-explanatory
```

---

## Timeline

| Phase | Effort | When |
|---|---|---|
| Phase 1 | 30 min | Day after submission |
| Phase 2 | 1 hour | Same day |
| Phase 3 | 2 hours | Next day (needs focus) |
| Phase 4 | 1 hour | Same session as Phase 3 |
| Phase 5 | 30 min | Immediately after Phase 4 |

**Total: ~5 hours across 2 days.** One rename per commit, test between each, no big-bang.

---

*Plan by claude.analysis. Based on Perplexity Computer repo spec + build day lessons. 2026-06-02.*
