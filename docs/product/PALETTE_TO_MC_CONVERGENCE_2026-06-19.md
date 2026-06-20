# Palette → Mission-Canvas Convergence Brief — What Palette Gives Up the Stack

Date: 2026-06-19
Status: Fresh convergence pass — reverse direction (Palette → MC contributions)
Owner: Palette maintainer (working session with Claude Code)
Companion to: `docs/product/CONVERGENCE_BRIEF_2026-06-19.md` (which covers MC/remote → Palette)

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
