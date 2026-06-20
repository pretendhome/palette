# Palette Convergence Brief — Recovering the Judgment Layer

Date: 2026-06-19
Status: Fresh convergence pass — selective re-integration into the local base
Owner: Palette maintainer (working session with Claude Code)
Base of record: local `C:\Users\spide\palette` @ `425faf9` (this computer). The GitHub remote is reference only, not a merge target.
Companion to: `docs/product/PALETTE_TO_MC_CONVERGENCE_2026-06-19.md` (reverse direction — Palette → MC).

## Session Context

Mission-Canvas (missioncanvas.ai) is the shipping product and lives in its own repo
(`pretendhome/mission-canvas`); it is treated as frozen and is never modified by this work.
Kiro's background cross-sync scattered the Palette GitHub remote — 1,728 files, +48k/−125k
lines since the shared base `4a88cb5` — mixing MC product, a competition dossier (`bdb/`),
installers, and landing pages into Palette. Palette was spun down because it was scattering;
the goal here is to recover only what deepens Palette's governed-decision core and leave the
scatter behind. The base on this computer is authoritative; we do not push anywhere; we pull
forward lost work file by file.

## Working Recommendation

> Recover the intent/orchestration layer (Palette's "operating system for judgment") and its
> governance substrate. Take the knowledge Legal vertical and the retrieval/governance
> hardening. Exclude everything Mission-Canvas, BDB-competition, installer, and rebrand.
> Relocate the one genuinely-needed dependency (`bdb/gateway/`) out of the scatter folder
> into a clean Palette home (`core/gateway/`) so recovered code doesn't drag the competition
> dossier back in.

Key finding: `agents/` lost nothing (roster byte-identical on both sides), but
`scripts/palette_intents/` (the 6-intent judgment OS) is 100% missing from local and is the
highest-value asset on the remote.

## What Was Actually Lost — Evidence

| Asset | Where | Substance | Status in local base |
|---|---|---|---|
| `scripts/palette_intents/` — protect/research/decide/create/diagnose/reflect + `infra.py` + `schemas.py` (GateDecision, EvidenceBrief, DecisionRecord, FailureLesson) + tests | remote | ~4,270 LOC, 16 files | Absent |
| `scripts/palette_orchestrate.py` — 7-step CLASSIFY→RETRIEVE→REASON→RESEARCH→SYNTHESIZE→CRITIQUE→STORE loop | remote | 604 LOC | Absent |
| `scripts/palette_query.py` — 5-step governed query pipeline | remote | 940 LOC | Absent |
| `scripts/palette_intent.py` — unified `palette <intent>` CLI dispatcher | remote | 98 LOC | Absent |
| `scripts/session_reflect.py`, `query_before_act.py` — memory/reflection loop | remote | ~700 LOC | Absent |
| `tests/golden_dataset_v1.yaml` (100 queries / 86 RIUs) + `validate_golden.py` | remote | regression harness | Absent |
| `bdb/gateway/` — socket_firewall, sanitizer, rate_limiter, cache, audit, fallback | remote (inside scatter) | ~660 LOC | Absent — but the intent layer imports it |

Confirmed by direct observation: MC's live CLI is `mc <intent> <query>`
(protect/research/decide/create/diagnose/reflect) — the matured descendant of this exact lost
layer. Palette must recover its own lineage from the scattered remote, not copy MC.

## Recommended Integration — Three Tiers

**Tier 1 — Recover the judgment OS (highest value; THIS PASS).**
- `scripts/palette_intents/` (entire package + tests)
- `scripts/palette_orchestrate.py`, `scripts/palette_intent.py`, `scripts/palette_query.py`
- `scripts/session_reflect.py`, `scripts/query_before_act.py`
- `tests/golden_dataset_v1.yaml` + `tests/validate_golden.py`
- Dependency: `bdb/gateway/` relocated to `core/gateway/`, imports rewired.

**Tier 2 — Governance + retrieval hardening (high value, on-thesis).**
- `core/palette-core.md` Retrieval Principles + Product-Truth/Moat additions.
- `agents/researcher/auto_enrich.py` PII scrubber; `agents/health/health_check.py` retrieval
  eval; `agents/resolver/resolver.py` deep-research route.
- `peers/` advances — but per the local-authoritative rule these stay LOCAL (peers bus is
  Palette-only, not in MC); revisit only if a concrete gap is found.

**Tier 3 — Knowledge: the Legal vertical (coherent, well-sourced).**
- taxonomy 121→131 (RIU-700–709, Heppner SDNY), knowledge-library +20 (LIB-200–219),
  `buy-vs-build/integrations/ollama-local/recipe.yaml`, `riu_classification` routing.

## Non-Goals — Explicitly Exclude (scatter)

`bdb/` as a whole except `gateway/`; `.palette/`, `ops/`, runtime ndjson/telemetry;
`litellm_config.yaml` (MC-branded; local has its own recipe), `setup.sh`, `install.sh`,
`QUICKSTART.md`, landing pages/CNAME/MC logo/installer HTML; the `voice/` rename (a content
downgrade — keep local); tech/disruption investment tooling, conference people-library,
conference-capture, demo/preflight scripts, dual-repo push & Kiro-VPS scripts; LIB-186–192
(mixed provenance — skip).

## One-Way Door Decisions (resolved)

1. Gateway relocation → **`core/gateway/`**, imports rewired off `bdb`.
2. Modified peers/agent files newer on remote → **keep local** (Palette-only; MC has its own
   forks or lacks them entirely). No overwrite.
3. MC-coupled extras (`kiro_failsafe.mjs`, MC-branded `index.html`, `kl_embeddings.json`) →
   defer / keep local.
4. Save both briefs to `docs/product/`. Done.

## Immediate Next Steps

1. Stage Tier 1 files into the local base only (no push).
2. Relocate `bdb/gateway/` → `core/gateway/`, rewire ~import sites.
3. Run `tests/validate_golden.py` + `scripts/palette_intents/tests/` to confirm the recovered
   layer executes.
4. Update `MANIFEST.yaml` (new `scripts/palette_intents/` layer, `core/gateway/`).
5. Append a `decisions.md` entry recording exactly what was re-integrated and excluded.

## Current Decision

> Do not re-merge the scattered remote. Recover a named, bounded layer — the
> intent/orchestration judgment OS plus its governance substrate — and leave Mission-Canvas,
> BDB, installers, and rebrands behind. Mission-Canvas itself is frozen and untouched.
> Recover focus, not volume.
