# Palette Repository Audit — File-Level Inventory & Recommendations
**Date**: 2026-05-29
**Author**: kiro.design
**Purpose**: Identify what's needed vs. noise. Recommend KEEP / ARCHIVE / DELETE per directory.
**Rule**: Nothing deleted yet. This is the assessment only.

---

## Summary

| Category | Files | Recommendation |
|---|---|---|
| **Core system (needed for BDB + product)** | ~450 | KEEP |
| **Operational but dormant (not needed for BDB)** | ~800 | ARCHIVE |
| **Generated artifacts (rebuildable)** | ~4,500 | ARCHIVE or DELETE |
| **Dead weight (superseded, stale, or PII)** | ~300 | DELETE |
| **Virtual env + node_modules** | ~4,000+ | IGNORE (not committed) |

**Total tracked files that matter**: ~450. The rest is history, generated output, or dormant features.

---

## TOP-LEVEL FILES

| File | Purpose | Verdict |
|---|---|---|
| `MANIFEST.yaml` | Single source of truth for system state | **KEEP** — critical |
| `README.md` | Public-facing intro | **KEEP** — needs rewrite (Claude task) |
| `QUICKSTART.md` | User onboarding | **KEEP** |
| `CLAUDE.md` | Claude Code steering | **KEEP** |
| `AGENTS.md` | Codex steering | **KEEP** |
| `CHANGELOG.md` | Version history | **KEEP** |
| `CONTRIBUTING.md` | Contributor guide | **KEEP** |
| `decisions.md` | Append-only decision log | **KEEP** — governance artifact |
| `KNOWLEDGE_INDEX.yaml` | Generated index | ARCHIVE — rebuildable from KL |
| `RELATIONSHIP_GRAPH.yaml` | Generated graph | ARCHIVE — rebuildable from taxonomy |
| `setup.sh` | One-command install | **KEEP** — BDB P0 |
| `__init__.py` | Python package marker | **KEEP** |

---

## DIRECTORIES — DETAILED AUDIT

### `taxonomy/` (3 files) — **KEEP ALL**
The routing brain. 131 RIUs. Everything routes through this.
- `releases/v1.3/palette_taxonomy_v1.3.yaml` — **KEEP** (the taxonomy)
- `releases/v1.3/...pre-remediation-backup` — ARCHIVE (backup, not needed)
- `README.md` — **KEEP**

### `knowledge-library/` (9 files) — **KEEP**
203 entries. The intelligence layer.
- `v1.4/palette_knowledge_library_v1.4.yaml` — **KEEP** (the library)
- `v1.4/*_backup.yaml` — DELETE (PII flagged in audit, stale)
- `proposals/` — **KEEP** (governance pipeline input)
- `README.md` — **KEEP**

### `scripts/` (93 files) — MIXED

**KEEP (active, used by BDB or product)**:
| File | Why |
|---|---|
| `palette_intent.py` | CLI entry point |
| `palette_stats.py` | BDB feature |
| `palette_preflight.py` | Demo validation |
| `palette_cron.py` | BDB feature |
| `palette_query.py` | Legacy query interface |
| `palette_orchestrate.py` | Orchestration |
| `compile_wiki.py` | Wiki compiler |
| `validate_wiki.py` | Wiki validator |
| `palette_intents/` (all) | Intent framework |
| `palette_intelligence_system/` (all) | PIS engine |
| `generate_knowledge_index.py` | Index generator |
| `generate_relationship_graph.py` | Graph generator |

**ARCHIVE (dormant, not used by BDB)**:
| File | Why archive |
|---|---|
| `company_intel_report.py` | One-off report generator |
| `comprehensive_palette_audit.py` | Superseded by total-health |
| `lean_system_audit.py` | Superseded by total-health |
| `lens_eval_runner.py` | Lenses not in BDB scope |
| `stress_test_v3.py` | Historical stress test |
| `test_v3.py` | Historical test |
| `validate_implementation.py` | Superseded |
| `validate_palette_state.py` | Superseded by preflight |
| `voice_interface.py` | Voice Hub moved to peers/hub |
| `session_reflect.py` | Unused |
| `query_before_act.py` | Experimental |
| `sync-impressions.py` | Agent impressions (dormant) |
| `file_proposal.py` | Wiki governance (dormant) |
| `record_vote.py` | Wiki governance (dormant) |
| `promote_proposal.py` | Wiki governance (dormant) |
| `bridge_feedback_to_proposals.py` | Wiki governance (dormant) |
| `enrichment/` (12 files) | Auto-enrichment (dormant) |

### `scripts/palette_intents/` (11 files) — **KEEP ALL**
The intent framework. Active, tested, BDB-critical.

### `scripts/palette_intelligence_system/` (24 files) — **KEEP ALL**
The PIS engine. Integrity checks, regression detection, drift.

---

### `peers/` (3,331 files) — MOSTLY ARCHIVE

**KEEP (active infrastructure)**:
| Path | Why |
|---|---|
| `broker/` (index.mjs, db.mjs, gates.mjs, validate.mjs) | The bus |
| `migrations/` (6 SQL files) | Schema |
| `hub/server.mjs` | Voice Hub |
| `hub/watcher.mjs` | Wiki watcher |
| `adapters/` (4 adapters) | Agent MCP adapters |
| `cli.mjs` | Bus CLI |
| `package.json` | Dependencies |
| `gap_signals.ndjson` | Integrity signals |

**ARCHIVE (3,259 files — 96% of the directory)**:
| Path | Files | Why archive |
|---|---|---|
| `dropbox/inbox/perplexity/` | 3,191 | Historical bus messages. Rebuildable. Not needed for product. |
| `dropbox/inbox/kiro/` | 37 | Same |
| `dropbox/inbox/claude/` | 14 | Same |
| `dropbox/inbox/codex/` | 10 | Same |
| `dropbox/inbox/gemini/` | 7 | Same |

These are delivered bus messages saved to disk. They're historical records of agent communication. The bus itself stores messages in SQLite — the dropbox is a redundant archive.

---

### `wiki/` (624 files) — ARCHIVE MOST

**What it is**: A compiled wiki generated from taxonomy + KL. 152 entry pages, 131 RIU pages, indexes, governance proposals.

**The question**: Is the wiki needed for BDB?

**Answer**: No. The wiki is a *presentation layer* over the taxonomy and KL. The source data (taxonomy + KL) is what matters. The wiki can be regenerated anytime with `python3 scripts/compile_wiki.py`.

| Path | Files | Verdict |
|---|---|---|
| `wiki/entries/` | 152 | ARCHIVE — generated, rebuildable |
| `wiki/rius/` | 131 | ARCHIVE — generated, rebuildable |
| `wiki/indexes/` | 0 (deleted) | Already gone |
| `wiki/paths/` | 0 (deleted) | Already gone |
| `wiki/proposed/` | 8 | ARCHIVE — governance proposals (dormant) |
| `wiki/proposed/archive/` | 333 | ARCHIVE — historical proposals |

**Total wiki files to archive**: ~624. Keep `scripts/compile_wiki.py` and `scripts/validate_wiki.py` so it can be regenerated.

---

### `artifacts/` (965 files) — ARCHIVE ALL

**What it is**: Validation evidence, patches, and verification tests generated by the remediation loop agents.

| Path | Files | What |
|---|---|---|
| `artifacts/validation/` | 923 | JSON evidence packets from validator runs |
| `artifacts/patches/` | 28 | Text patches generated by builder |
| `artifacts/verification_tests/` | 14 | Test files generated by builder |

**Verdict**: ARCHIVE. These are generated outputs from agent runs. They prove the loop worked historically but aren't needed for the product. The `.palette/artifacts/` directory (intent artifacts) is separate and IS needed.

---

### `agents/` (109 files) — KEEP CORE, ARCHIVE REST

**KEEP**:
| Agent | Why |
|---|---|
| `remediation/` (7 files) | Shared loop infrastructure |
| `validator/validator_v2.py` | Active validator |
| `debugger/debugger_v2.py` | Active debugger |
| `builder/builder_v2.py` | Active builder |
| `health/` | Health agent |
| `total-health/` | Total health agent |
| `resolver/` | Intent resolver |

**ARCHIVE**:
| Agent | Why |
|---|---|
| `validator/validator.py` | Superseded by v2 |
| `debugger/debugger.py` | Superseded by v2 |
| `builder/builder.py` | Superseded by v2 |
| `architect/` | Design placeholder, not implemented |
| `narrator/` | GTM agent, not used in BDB |
| `monitor/` | Signal monitoring, dormant |
| `orchestrator/` | Workflow routing, design only |
| `researcher/` | Superseded by intent framework |
| `business-plan-creation/` | One-off workflow |

---

### `docs/` (218 files) — ARCHIVE MOST

**KEEP (active/BDB-relevant)**:
| File | Why |
|---|---|
| `landing/index.html` | BDB landing page |
| `TERMINAL_FIRST_VALIDATION_PATTERN.md` | New operational pattern |
| `GETTING_STARTED.md` | Onboarding |
| `DEMO.md` | Demo script |
| `specs/ADAPTIVE_INTENT_FRAMEWORK.md` | Intent spec |

**ARCHIVE (historical, superseded, or dormant)**:
| Path | Files | Why |
|---|---|---|
| `audits/` | 33 | Historical audit reports |
| `research/` | 15 | Research notes |
| `product/` | 12 | Product docs (some stale) |
| `competitions/` | 8 | Old competition entries |
| `voice-workbench/` | 48+ | Audio files + workbench (dormant) |
| `WIKI_*.md` (10+ files) | — | Wiki governance docs (dormant) |
| `*_2026-02-*.md` (many) | — | February-era specs (superseded) |
| `CONVERGENCE_BRIEF_*.md` | — | Historical |
| `PALETTE_*.md` (many) | — | Various old specs |

---

### `mission-canvas/` (159 files) — MIXED

**KEEP**:
| File | Why |
|---|---|
| `mc_telegram.py` | BDB P0 |
| `mc_telegram.env.example` | Config template |
| `systemd/mc-telegram.service` | Deployment |
| `CNAME` | Domain config |
| `index.html` | MC landing (if different from docs/landing) |
| `package.json` | Dependencies |
| `data_boundary.mjs` | Governance module |

**ARCHIVE**:
| Path | Why |
|---|---|
| `archive/` (15 files) | Old versions |
| `competitions/` (13 files) | Old competition entries |
| `workspaces/` | User-specific workspaces (PII) |
| `joseph_bot_v2.py`, `joseph_bridge.py` | Person-specific bots |
| `deploy_vps.sh` | Operational (keep if deploying) |
| `anonymous_feedback.jsonl` | Runtime data |
| Various `.mjs` files | Experimental modules |

---

### `buy-vs-build/` (106 files) — KEEP CORE

**KEEP**:
| Path | Why |
|---|---|
| `v1.0/palette_company_riu_mapping_v1.0.yaml` | Company index |
| `service-routing/v1.0/` | Service routing layer |
| `people-library/v1.1/` | People profiles |
| `integrations/` (76 recipes) | Integration recipes |
| `recipe_company_mapping.yaml` | Recipe→company map |

**ARCHIVE**:
| Path | Why |
|---|---|
| `tech/` (7 files) | Conference notes, disruption theses (reference only) |
| `intel/` | Company intel reports |
| `profiles-raw.txt` | Raw data |
| `PALETTE_INTELLIGENCE_SYSTEM_v1.0.md` | Superseded by scripts/PIS |

---

### `bdb/` (43 files) — **KEEP ALL**
Active competition material. All needed through June 2.

### `voice/` (69 files) — ARCHIVE ALL
Voice workbench with audio files. Not in BDB scope. 6.4MB of audio.

### `lenses/` (43 files) — ARCHIVE
Lens system. Not in BDB scope. Contains PII (person lenses).

### `skills/` (46 files) — ARCHIVE MOST
- `skills/retail-ai/`, `education/`, `travel/` — **KEEP** (validated skills)
- `skills/talent/` (23 files) — ARCHIVE (job search materials, PII)
- `skills/enablement/`, `lenses/` — ARCHIVE (dormant)

### `bridges/` (21 files) — ARCHIVE
Telegram bridges. Superseded by `mc_telegram.py`.

### `sdk/` (12 files) — **KEEP**
Agent base classes, integrity gate, graph query. Small, tested.

### `plugins/` (11 files) — ARCHIVE
Obsidian decision board plugin. Shipped but not BDB-relevant.

### `archive/` (18 files) — ARCHIVE (already is)
Historical. Leave as-is.

### `analysis/` (5 files) — ARCHIVE
One-off analysis files (job search, market analysis).

### `legal/` (2 files) — **KEEP**
Trademark files.

### `core/` (9 files) — **KEEP**
Governance tier 1+2 files, Go schema definitions.

### `.steering/` (40+ files) — MIXED
| Path | Verdict |
|---|---|
| `.steering/kiro/steering.md` | **KEEP** |
| `.steering/kiro/KIRO_READ_THIS_FIRST.md` | **KEEP** |
| `.steering/codex/README_START_HERE.md` | **KEEP** |
| `.steering/gemini/GOVERNANCE_STEERING.md` | **KEEP** |
| `.steering/mistral/TEAM_CONTEXT.md` | **KEEP** |
| All stress test results | ARCHIVE |
| All reflections/letters | ARCHIVE |
| All job match analyses | ARCHIVE |

### `.kiro/` (3 files) — **KEEP ALL**
Steering + Turso spec.

---

## THE BIG WINS (Highest Impact Archives)

| Directory | Files | Size | Impact |
|---|---|---|---|
| `peers/dropbox/inbox/` | 3,259 | ~15MB | **Biggest single win** — historical messages |
| `wiki/` | 624 | 3.1MB | Generated, rebuildable |
| `artifacts/` | 965 | 3.9MB | Generated evidence packets |
| `voice/` | 69 | 6.4MB | Audio files, dormant |
| `docs/` (stale specs) | ~150 | ~2MB | Historical noise |

**Archiving these 5 directories removes ~5,067 files (56% of the repo) with zero regression.**

---

## RECOMMENDED APPROACH

### Phase 1: Zero-risk archive (no code changes)
```bash
mkdir -p archive/standby-2026-05-29
mv peers/dropbox/inbox/ archive/standby-2026-05-29/peers-inbox/
mv wiki/ archive/standby-2026-05-29/wiki/
mv artifacts/ archive/standby-2026-05-29/artifacts-remediation/
mv voice/ archive/standby-2026-05-29/voice/
```

### Phase 2: Selective archive (review first)
- Move stale docs to `archive/standby-2026-05-29/docs/`
- Move dormant agents (v1, narrator, monitor, orchestrator) to archive
- Move lenses, bridges, plugins to archive

### Phase 3: .gitignore additions
```gitignore
# Archived — rebuildable or historical
archive/standby-2026-05-29/
peers/dropbox/inbox/
artifacts/validation/
artifacts/patches/
wiki/entries/
wiki/rius/
wiki/proposed/archive/
voice/
```

### Phase 4: Verify no regression
```bash
python3 scripts/palette_preflight.py          # Demo still works
python3 scripts/palette_stats.py              # Stats still accurate
python3 agents/total-health/total_health_check.py  # Health passes
python3 scripts/palette_intent.py research "test"  # Intents work
```

---

## WHAT REMAINS AFTER CLEANUP (~450 files)

```
palette/
├── taxonomy/          (3)    — routing brain
├── knowledge-library/ (5)    — intelligence layer
├── buy-vs-build/      (90)   — service routing + recipes
├── scripts/           (50)   — CLI + PIS + intents
├── agents/            (30)   — validator, debugger, builder, health
├── peers/             (30)   — bus broker + hub + adapters
├── bdb/               (43)   — competition material
├── sdk/               (12)   — agent SDK
├── mission-canvas/    (15)   — telegram bot + config
├── docs/              (20)   — landing page + active specs
├── core/              (9)    — governance files
├── skills/            (10)   — validated skills
├── legal/             (2)    — trademarks
├── .steering/         (10)   — agent steering (active only)
├── .kiro/             (3)    — kiro steering
└── top-level          (12)   — MANIFEST, README, setup.sh, etc.
```

**~450 files. Everything else is rebuildable, historical, or dormant.**

---

*Audit by kiro.design. 2026-05-29. No files modified.*
