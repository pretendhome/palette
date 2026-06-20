# Palette → Mission-Canvas Convergence Brief — What Palette Gives Up the Stack

Date: 2026-06-19
Status: Reverse direction (Palette → MC) + cross-repo dependency inventory & MC-independence plan
Revised: 2026-06-19 — added the dependency inventory and explicit instructions for making
Mission-Canvas completely independent, with safe reconcile sequencing (post Tier-1/2/3 recovery).
Owner: Palette maintainer (working session with Claude Code)
Companion to: `docs/product/CONVERGENCE_BRIEF_2026-06-19.md` (which covers MC/remote → Palette)

> This brief now has two jobs:
> 1. **What Mission-Canvas could *gain* from Palette** (the composability/ontology/integrity
>    mechanisms — see "The Core Idea" onward).
> 2. **What Mission-Canvas must *do* to be completely independent of Palette** (the dependency
>    inventory and independence plan immediately below).
> Independence comes first because it is the prerequisite for safely cleaning up either repo.

## Framing — This Is Not a Ranking

Mission-Canvas is not "better" than Palette, and Palette is not "better" than MC. They
optimize for different things, and each holds something the other lacks.

- **Mission-Canvas is light and transplantable.** It is built to drop onto any use case,
  any machine, and start "from somewhere, not from chaos." Its multi-agent intents
  (protect / research / decide / create / diagnose / reflect) cut through an enormous
  amount of noise. That is genuinely innovative and is MC's center of gravity.
- **Palette is built to get each path right.** Its ontology, relationship graph, integrity
  engine, and governed routing are materially more complete. It trades portability for
  depth and correctness.

This brief is the *reverse* of the recovery brief: it catalogs what Palette can hand **up**
to MC without compromising MC's lightness. The rule is: **send mechanisms, not bulk.** MC
should receive Palette's *engines* (composable traversal, the graph, the integrity gate),
never Palette's heavy hand-authored corpus — that would defeat MC's transplantability.

## Dependency & Coupling Inventory (as of 2026-06-19)

Every coupling found between Palette and Mission-Canvas this session. Good news first:
**MC's runtime is already code-independent** — `grep` for `import palette` / `from palette` /
`palette_retrieve` across the MC repo returns nothing. MC carries only a *static data snapshot*
of Palette knowledge, and MC's own installer clones the MC repo. The only *live* coupling is
website hosting.

| # | Coupling | Direction | Status | What it is | Action to sever |
|---|----------|-----------|--------|-----------|-----------------|
| 1 | **missioncanvas.ai web hosting** | MC ⇐ Palette repo | **ACTIVE / LIVE** | GitHub Pages serves missioncanvas.ai from `pretendhome/palette/docs/` — `CNAME=missioncanvas.ai`, `index.html`, `install.sh`, `install.ps1`, `install-windows.txt`, `logo-mc.png`. (The served `install.sh` already pulls the *product* from `pretendhome/mission-canvas` — only the *hosting* lives in palette.) | Move the `docs/` site into `pretendhome/mission-canvas`; repoint the Pages custom domain to the MC repo. **Until done, do NOT delete/force-push over `palette/docs/` — it is the live site.** |
| 2 | **Palette retrieval → MC ontology** | Palette ⇒ MC | **SEVERED 2026-06-19** | `peers/hub/palette_retrieve.py::_get_mc_engine()` imported `ontology.engine.OntologyEngine` from a `mission-canvas/` dir. | Done — now returns `None` unconditionally; Palette stands MC-independent. |
| 3 | **MC knowledge snapshot** | MC ⇐ Palette (data) | **STATIC** (no live dep) | MC repo carries `knowledge/palette_imported.yaml`, a frozen import of Palette knowledge. | MC owns it (curate/rename) or documents a versioned export-sync; drop the implicit "imported" framing. |
| 4 | **Kiro cross-sync** | bidirectional | **ROOT CAUSE** | The Kiro background agent syncing both repos is what scattered Palette in the first place. | Stop Kiro writing across repos; give each repo its own steering. |
| 5 | *(internal)* `palette_query` → `palette_retrieve` | within Palette | resolved 2026-06-19 | needed `retrieve_learn` (Tier-2 adopted). | n/a — internal Palette. |
| 6 | *(internal)* intent layer → `core.gateway` | within Palette | resolved 2026-06-19 | relocated from `bdb/gateway`. | n/a — internal Palette. |

## What Mission-Canvas Must Do to Be Completely Independent

The list is short because MC is already 90% independent. Do these in order; each is reconcile-safe
(see sequencing below).

1. **Take ownership of the missioncanvas.ai deployment (the only live coupling).**
   - MC already has `static/index.html`, `install.sh`, and `install-binary.sh`. Reconcile so the
     MC repo holds the *canonical, current* versions of the site + installers (copy across anything
     newer that currently lives only in `palette/docs/`: the latest `index.html`, `install.sh`,
     `install.ps1`, `install-windows.txt`, `logo-mc.png`).
   - Add `CNAME=missioncanvas.ai` to the MC repo's Pages source and set `pretendhome/mission-canvas`
     as the GitHub Pages source; move the custom domain to it.
   - **Verify**: missioncanvas.ai loads from the MC repo; `curl -fsSL https://missioncanvas.ai/install.sh | sh`
     installs from `pretendhome/mission-canvas`; binary-release download resolves.
   - **Only then** remove the site assets from `pretendhome/palette/docs/`.

2. **Own the knowledge snapshot.** Decide whether `knowledge/palette_imported.yaml` is permanently
   MC-owned (curate + rename, drop "imported") or refreshed via a documented, versioned export from
   Palette. Either way, remove the implicit live-import expectation.

3. **Lock in zero runtime coupling (already true — keep it true).** MC imports no Palette module
   today. Add a CI guard / lint that fails the MC build if anything ever imports a `palette*` path,
   so independence cannot silently regress.

4. **Stop the cross-repo sync.** Disable Kiro (or any agent) from syncing content between
   `pretendhome/palette` and `pretendhome/mission-canvas`. Each repo gets isolated steering. This is
   the root cause of the original scatter; until it stops, any cleanup will be re-polluted.

5. **Keep installers pointed at their own repo.** Both installers already clone
   `pretendhome/mission-canvas` for the product — never repoint an MC installer at the palette repo.

## Safe Reconcile Sequencing (do not break anything)

> **Reconcile additively → verify → only then eliminate/replace.** Never remove a live asset before
> its replacement is proven.

- **Phase 1 — Additive (nothing removed).** MC repo gains its own canonical site + installers + CNAME
  and begins serving missioncanvas.ai. `palette/docs/` stays exactly as-is. Both work simultaneously.
- **Phase 2 — Verify.** Confirm a full cycle works entirely from the MC repo: site loads at
  missioncanvas.ai, `install.sh`/`install.ps1` install correctly, binary releases resolve. Run it end
  to end before touching anything in palette.
- **Phase 3 — Eliminate/replace.** *Only after Phase 2 is green*: remove the site assets from
  `pretendhome/palette/docs/` and stop the Kiro cross-sync.

**Hard rule until Phase 2 is green:** do **not** force-push, delete, or otherwise overwrite
`docs/` on `pretendhome/palette` — GitHub Pages serves the live missioncanvas.ai from it, and the
local Palette base intentionally does not carry those files. (This is exactly why the Tier-1/2/3
recovery publishes to a **new branch**, not a force-push over `main`.)

**Honest note on cost vs. gain:** the only *required* work for independence is Phase 1–3 above
(a deployment move + stopping the sync). It is modest, and the gain is real: two repos that can each
be cleaned, released, and reasoned about without the other — and no more Kiro scatter. Everything
below ("what MC gains from Palette") is *optional upside*, to be pursued only after independence is
secured.

## The Core Idea — Composable Atomic Traversal (the robotics insight)

The most valuable thing Palette can give MC is not a feature. It is a **method for coverage**.

In robotics, if you train a robot on the whole sequence "pick up the banana, then the
orange, then the apple," you have taught it exactly one rigid behavior, and you pay full
training cost for every new ordering. But if you train **atomic skills** — apple alone,
orange alone, banana alone — then:

- "put them all in the basket"
- "put only the round ones in the basket"
- "start with the banana"

...are **all executable by composition**, because each unit is small, distinct, and
combinable. A small set of atoms yields combinatorial coverage. Training cost collapses.

Applied to Palette/MC:

> Each RIU → Library link should exist in its **smallest, atomic form**. The system then
> either (a) selects **several atomic RIUs at once**, or (b) **recurses** —
> RIU → Library → RIU(s) → Library entry(s) → … — assembling complete context **by
> itself**, until the path is whole.

The payoff is the same as in robotics:

> **You never author an RIU per use case — only every *base* use case.** Every real-world
> request becomes a *traversal/composition* of atoms, not a bespoke hand-built node.

### Evidence: Palette already has this latent (and never ran it)

This is not aspirational — the capability is sitting unused in the current code.

- `scripts/palette_intelligence_system/traverse.py:126` — `_resolve_riu_from_lib()` returns
  **`(rius[0], rius[1:])`**: a primary RIU *and a list of secondaries*. The data model
  (`related_rius`) is already a list, i.e. one Library entry already fans out to many RIUs.
- `traverse.py:236` — the traversal does `primary, _secondary = _resolve_riu_from_lib(...)`
  then `riu_id = primary` and proceeds. **The secondaries are extracted and then discarded**
  (the leading underscore marks them deliberately unused). The engine follows exactly **one
  hop** and stops.
- `traverse.py:209` — `_find_knowledge()` walks RIU → LIB; `_resolve_riu_from_lib()` walks
  LIB → RIU. **Both directions of the edge already exist.** A recursive RIU→LIB→RIU→LIB loop
  is fully expressible with the primitives already present.
- `sdk/graph_query.py` — `GraphQuery` exposes the relationship graph (1,800+ quads, 13
  predicates, bidirectional `RIU→has_knowledge→LIB`, `RIU→has_service→Service`, etc.) as a
  callable S/P/O interface. This is a ready-made substrate for recursive composition.

The mechanism is one wired loop and a stop condition away from existing. MC is the system
that would actually *use* it at scale.

## What Palette Contributes — Three Mechanisms

### Pillar 1 — Composable, recursive RIU↔LIB traversal (the crown jewel)

The atom-composition engine described above. Concretely, what ships to MC is:

- The **atomic RIU→LIB contract**: each link kept minimal and single-purpose.
- A **recursive traverse loop**: follow primary *and* secondary RIUs, expand each via
  `_find_knowledge`, re-resolve, repeat — fan-out + recursion instead of one hop.
- A **stop condition Palette already owns**: the completeness score
  (`scripts/palette_intelligence_system/score.py`, surfaced as `completeness: N/100`) is the
  natural "context is whole — halt" signal for the recursion.
- **Cycle/visited tracking** so recursion terminates on graphs with back-edges.

This is what lets MC answer a novel, compound request without anyone having authored a node
for it — the request is *composed*, not *looked up*.

### Pillar 2 — The relationship graph / ontology (depth-on-demand)

`GraphQuery` + the quad graph give MC's transplantable shell a far richer **map of where it
is**. MC's README sells "the ontology gives it a position before it thinks"; Palette's graph
is the more complete version of exactly that — bidirectional, queryable, 9 entity types, 13
predicates. MC can mount it as an optional depth layer without inheriting Palette's bulk.

### Pillar 3 — The integrity engine (the guardrail that makes composition safe)

`sdk/integrity_gate.py` — `IntegrityGate` runs **pre-emit validation**: RIU references exist
in the taxonomy, service recommendations match the routing table, knowledge references exist
in the library, and non-success results must carry blockers (the glass-box invariant).
Crucially: *warnings are informational, not gatekeeping.*

This pairs with Pillar 1 by necessity:

> **Composition without an integrity engine drifts.** The moment a system assembles context
> recursively from atoms, it can reference units that don't exist or stitch an incoherent
> path. The integrity gate is what verifies the *assembled* context points only at real,
> consistent units. Palette has both halves; MC currently has the composition instinct
> (intents) but the lighter integrity surface.

### Pillar 4 (optional) — Governed buy-vs-build service routing

Palette's traversal emits a ranked service recommendation with alternatives, recipes, cost
model, and explicit "why-not" reasoning (`traverse.py:_build_service_recommendations`,
`_explain_why_not`). This is path-precision MC does not carry. Offer as an opt-in module for
MC use cases that need build-vs-buy decisions, not as a default.

## Why MC Needs Exactly These — The Synthesis

MC's multi-agent intents are the right *control surface*; Palette's composable traversal is
the right *coverage engine*; the integrity gate is the right *safety rail*. Combined:

> **MC intent (protect / research / decide / …) × Palette recursive atomic traversal =
> intents that assemble their own context on demand from a small atomic library, validated
> by the integrity gate as they go.**

MC keeps its lightness and transplantability. Palette lends it depth that activates only
when a path needs it — coverage by composition instead of coverage by authoring.

## Non-Goals — Protect MC's Identity

- **Do not** push Palette's heavy hand-authored breadth (the full 121→131 RIU corpus, 176+
  LIB entries, people-library, lenses) into MC wholesale. That would compromise the exact
  transplantability that makes MC valuable. Send the **engines**, let MC carry only the
  atoms a given deployment needs.
- **Do not** make MC adopt Palette's path-specific governance ceremony where MC's lighter
  gates already suffice.
- **Do not** treat this as a merge. These stay two systems; this is a mechanism transfer.

## One-Way Door Decisions / Open Questions

1. **Atom granularity.** How small is a "base use case"? Define the atomic RIU→LIB contract
   precisely — too coarse and you lose combinatorial coverage; too fine and traversal cost
   explodes.
2. **Termination.** Reuse Palette's completeness score as the recursion stop condition, or
   define an MC-native "context sufficient" signal?
3. **Cycle handling.** Visited-set vs depth cap vs both for the recursive walk.
4. **Where the engines live in MC.** A mountable Palette-core module vs a reimplementation
   inside MC's `runtime/`.

## Immediate Next Steps

1. Spec the **recursive traverse loop** against the existing primitives (`GraphQuery`,
   `_find_knowledge`, `_resolve_riu_from_lib`, completeness score) — prove RIU→LIB→RIU→LIB
   composition on Palette first, since the parts already exist.
2. Define the **atomic RIU→LIB contract** (the "base use case" unit).
3. Port **`IntegrityGate`** as MC's pre-emit validator for composed context.
4. Decide atom granularity and termination (open questions 1–2) before scaling.

## Current Decision

> Palette gives Mission-Canvas three mechanisms — **composable recursive atomic traversal,
> the relationship graph, and the integrity engine** — and withholds its bulk. MC stays
> light and transplantable; Palette lends it depth that activates on demand. The headline is
> the robotics insight made real: cover every combination by authoring only the atoms, then
> letting the system compose and verify the rest itself.
