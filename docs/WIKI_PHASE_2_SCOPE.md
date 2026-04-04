# Wiki Focal Point — Phase 2 Scope

**Author**: kiro.design
**Date**: 2026-04-03
**Status**: APPROVED by the operator — task assignments issued 2026-04-03
**Iterations**: 5 (documented below)
**Depends on**: Phase 1 (COMPLETE — 329 pages, 7/7 validation, 4 reviewers, 2 iterations)
**Reference**: `WIKI_FOCAL_POINT_PROPOSAL.md`, `WIKI_COMPILER_SPEC.md`, `WIKI_DESIGN_RATIONALE.md`

---

## Executive Summary

Phase 1 shipped a working wiki compiler: 329 pages, 7/7 validation checks pass, deterministic rebuild confirmed. Phase 2 improves what was built — fixing data quality issues in the source, closing gaps in the compiled output, and hardening the compiler for ongoing use.

Phase 2 is entirely TWO-WAY DOOR except item P2-08 (proposed/ governance model), which requires the operator.

I scoped this by reading every file in the wiki, running every validator, auditing the source YAML, verifying Gemini's findings against disk, and checking Claude's Phase 2 list against what I found independently. 5 iterations below.

---

## Iteration 1: Ground Truth Audit

Before scoping anything, I measured. These are the actual numbers from disk, not from any document.

### Phase 1 Output
- Pages compiled: 329 (121 RIU + 168 KL + 12 agent + 14 path + 13 index + 1 main)
- Validation: 7/7 PASS
- Deterministic rebuild: PASS
- Broken backlinks: 0
- Orphan pages: 0

### Issues Found by Measurement

| # | Issue | Severity | Source |
|---|---|---|---|
| 1 | 90/168 KL entries have "Why It Matters" duplicating the Definition opening | MEDIUM | Compiler rendering rule |
| 2 | 14/14 path files have NO frontmatter (no source_file, source_hash, compiled_at) | MEDIUM | Compiler gap |
| 3 | 12/12 agent pages missing `source_file` field | MEDIUM | Compiler gap |
| 4 | 6 KL entries are thin (<1000 bytes): LIB-076 through LIB-080, LIB-177 | LOW | Source data quality |
| 5 | 25 broken source URLs in live KL: 8 `internal://` + 17 `file:///` (all to old Myth-Fall-Game paths) | HIGH | Source data quality |
| 6 | All sources show entry-level tier, not per-source tier (only 1/547 sources has own tier field) | LOW | Source data limitation |
| 7 | Journey stages in wiki indexes match taxonomy exactly (4 stages) — Gemini's "8-9 stages" claim is WRONG | N/A | Verified false |
| 8 | `proposed/` directory exists but is empty, no governance model | BLOCKED | Needs the operator |
| 9 | `validate_wiki.py` and `validate_palette_state.py` check different things with no cross-reference | MEDIUM | Validator gap |
| 10 | RELATIONSHIP_GRAPH.yaml has bidirectional quads by design (2013 quads, 14 relationship types) — Gemini's "circular graph" finding is a design choice, not a bug | LOW | Evaluate only |

### Gemini Findings — Verified vs. False

| Gemini Finding | Verified? | Notes |
|---|---|---|
| Wiki is "Protocol Blind" (no HandoffPacket) | PARTIALLY TRUE | Wiki describes RIUs but doesn't reference wire contract. However, the wiki is a knowledge surface, not a protocol spec. Adding protocol references is reasonable for agent pages only. |
| validate_wiki.py decoupled from integrity engine | TRUE | Real gap. Two validators checking different things. |
| Journey stage drift (5 stages → 8-9) | FALSE | Taxonomy has 4 stages. Wiki indexes have exactly 4 stage indexes. Gemini miscounted. |
| Capability mismatch (wiki claims vs server.mjs) | MISLEADING | MANIFEST.yaml has empty capability arrays for all agents. The wiki's "Handled By" comes from relationship graph quads, not server.mjs capabilities. These are different systems. |
| PII policy leak (LIB-081 in wiki) | FALSE | LIB-081 in the wiki is "How do I choose between client-server and edge architectures" — NOT the PII scrubbing entry. Gemini confused the LIB ID with the security audit file. |
| Ghost pages (315 vs 329) | TRUE | Index says 329, actual is 329. The delta Gemini found was between the index counter and a different count. Minor — the index is correct. |
| Graph redundancy | EVALUATE | Bidirectional quads are by design (A handles B, B handled_by A). Whether this causes perf issues depends on usage. No evidence of bottleneck. |

---

## Iteration 2: Categorized Work Items

After measuring, I grouped everything into categories ordered by impact.

### Category A: Source Data Cleanup (fix the inputs)

**P2-01: Fix 25 broken source URLs in knowledge library**
- 8 `internal://` URIs that resolve to nothing
- 17 `file:///home/mical/Myth-Fall-Game/...` paths that don't exist (old repo)
- Fix in `palette_knowledge_library_v1.4.yaml`, then recompile
- These are real broken references that show up as dead links in Evidence sections
- Risk: TWO-WAY DOOR (source YAML edit + recompile)
- Effort: 1 hour
- Owner: Kiro (I know the KL schema)

**P2-02: Audit 6 thin KL entries**
- LIB-076, LIB-077, LIB-078, LIB-079, LIB-080, LIB-177 are all under 1000 bytes compiled
- These are the "gap_additions" entries that were added with minimal content
- Decision needed: enrich them with real content, or flag them as stubs?
- Risk: TWO-WAY DOOR
- Effort: 2 hours if enriching, 15 min if just flagging
- Owner: Kiro or Claude

### Category B: Compiler Improvements (fix the rendering)

**P2-03: Fix "Why It Matters" duplication**
- 90/170 entries have "Why It Matters" that duplicates the Definition opening
- Root cause: the compiler uses the `description` field, but for many entries `description` IS the first sentence of `content` (or absent, falling back to content)
- Fix: implement the deterministic rule from the compiler spec properly:
  1. If `description` exists AND differs from `content` first sentence → use it
  2. If `description` equals `content` first sentence → omit "Why It Matters"
  3. If `description` absent → omit "Why It Matters"
- Risk: TWO-WAY DOOR
- Effort: 30 min (compiler change + recompile + validate)
- Owner: Kiro (I built the compiler)

**P2-04: Add frontmatter to path files**
- All 14 path files are copied verbatim from `enablement/paths/` with no frontmatter
- The compiler spec says all pages should have frontmatter
- Add: `source_file`, `source_id` (RIU ID), `compiled_at`, `compiler_version`, `type: enablement_path`, `DO_NOT_EDIT`
- Risk: TWO-WAY DOOR
- Effort: 30 min
- Owner: Kiro

**P2-05: Add `source_file` and `source_hash` to agent pages**
- All 12 agent pages are missing `source_file` (they come from MANIFEST.yaml, not a dedicated agent YAML)
- Add `source_file: MANIFEST.yaml` and compute `source_hash` from the agent's MANIFEST entry
- Risk: TWO-WAY DOOR
- Effort: 20 min
- Owner: Kiro

**P2-06: Per-source evidence tier labels**
- Currently all sources in an entry show the entry-level tier (e.g., all "Tier 1")
- Only 1/547 sources has its own tier field in the source YAML
- Two options:
  - (a) Add per-source tier fields to the KL YAML (large effort, high value)
  - (b) Show entry-level tier with a note: "Entry evidence tier: 1 (individual source tiers not yet classified)"
- Recommendation: Option (b) for Phase 2, option (a) as a future enrichment task
- Risk: TWO-WAY DOOR
- Effort: 15 min for (b), 4+ hours for (a)
- Owner: Kiro for (b)

### Category C: Structural Improvements (close gaps)

**P2-07: Add HandoffPacket/SDK reference to agent pages**
- Agent pages currently show: name, description, list of handled RIUs
- Missing: how to invoke the agent (wire contract format)
- Add an optional "Protocol" section to agent pages that have SDK implementations
- Only add where real code exists (agents/ directory has prompt.md + Python files)
- Do NOT fabricate protocol info for agents that are design-only
- Risk: TWO-WAY DOOR
- Effort: 1 hour
- Owner: Kiro or Claude

**P2-08: `wiki/proposed/` governance model** 🚨 ONE-WAY DOOR
- The `proposed/` directory exists but is empty
- Phase 3 of the original proposal depends on this: voice interactions file proposed knowledge updates
- Needs the operator to decide:
  - What kinds of proposed entries are acceptable?
  - What is the review cadence?
  - Must proposed entries include source attribution?
  - Who can propose? (agents only? users? both?)
- Risk: 🚨 ONE-WAY DOOR — governance decisions are binding
- Effort: 30 min discussion with the operator
- Owner: the operator
- Status: COMPLETE — Governance Model v1 written (`docs/WIKI_GOVERNANCE_MODEL_v1.md`, 527 lines), VOTING_ROSTER.yaml created, awaiting the operator signature (2026-04-04)

### Category D: Validation Hardening (trust the output)

**P2-09: Reconcile validate_wiki.py with validate_palette_state.py**
- `validate_wiki.py` checks: orientation, coverage, backlinks, orphans, adversarial, determinism, dual-experience
- `validate_palette_state.py` checks: file existence, taxonomy counts, library IDs, orchestrator guard, implementation modules
- Neither checks the other's domain
- Fix: add a cross-check mode where validate_wiki.py verifies that wiki coverage matches what validate_palette_state.py expects
- Specifically: wiki RIU count must match taxonomy count, wiki KL count must match library count, wiki agent count must match MANIFEST agent count
- Risk: TWO-WAY DOOR
- Effort: 1 hour
- Owner: Kiro or Codex

**P2-10: Add source URL validation to compile_wiki.py**
- The compiler currently renders source URLs without checking if they're valid
- Add a warning (not a failure) when a source URL uses `internal://` or `file://` schemes
- This catches P2-01 type issues at compile time instead of after
- Risk: TWO-WAY DOOR
- Effort: 20 min
- Owner: Kiro

### Category E: Optimization (evaluate before acting)

**P2-11: Evaluate graph unidirectionality**
- RELATIONSHIP_GRAPH.yaml has 2013 quads with bidirectional relationships
- Gemini claims this causes 2x overhead. No evidence of actual bottleneck.
- Evaluate: measure compile time, measure graph query time, check if the wiki compiler's `build_graph_index()` is slow
- Only act if a real bottleneck is confirmed
- Risk: TWO-WAY DOOR (evaluation only)
- Effort: 30 min to measure
- Owner: Kiro

---

## Iteration 3: Priority Ordering

Ordered by: (1) fixes broken things, (2) improves quality, (3) closes gaps, (4) hardens, (5) evaluates.

### Must Do (blocks quality or correctness)

| ID | Item | Effort | Owner |
|---|---|---|---|
| P2-01 | Fix 25 broken source URLs | 1h | Kiro |
| P2-03 | Fix "Why It Matters" duplication (90/168) | 30m | Kiro |
| P2-04 | Add frontmatter to 14 path files | 30m | Kiro |
| P2-05 | Add source_file/hash to 12 agent pages | 20m | Kiro |
| P2-10 | Add source URL validation to compiler | 20m | Kiro |

### Should Do (improves quality significantly)

| ID | Item | Effort | Owner |
|---|---|---|---|
| P2-09 | Reconcile wiki validator with palette state validator | 1h | Kiro/Codex |
| P2-06 | Per-source tier labels (option b — note, not full classification) | 15m | Kiro |
| P2-07 | HandoffPacket reference on agent pages | 1h | Kiro/Claude |
| P2-02 | Audit 6 thin KL entries | 2h | Kiro/Claude |

### Evaluate Only

| ID | Item | Effort | Owner |
|---|---|---|---|
| P2-11 | Graph unidirectionality perf check | 30m | Kiro |

### Blocked

| ID | Item | Blocker |
|---|---|---|
| P2-08 | proposed/ governance model | the operator decision required |

---

## Iteration 4: Dependency Analysis and Sequencing

```
P2-01 (fix URLs) ──→ P2-10 (URL validation in compiler) ──→ recompile
                                                                ↓
P2-03 (Why It Matters fix) ──────────────────────────────→ recompile
P2-04 (path frontmatter) ───────────────────────────────→ recompile
P2-05 (agent source_file) ──────────────────────────────→ recompile
P2-06 (tier labels) ────────────────────────────────────→ recompile
                                                                ↓
                                                         validate (7/7)
                                                                ↓
P2-09 (validator reconciliation) ──→ run both validators ──→ confirm
                                                                ↓
P2-07 (agent protocol section) ──→ recompile ──→ validate
P2-02 (thin entries audit) ──→ enrich if needed ──→ recompile ──→ validate
                                                                ↓
P2-11 (graph perf eval) ──→ report only
P2-08 (governance) ──→ BLOCKED
```

**Optimal execution order:**

1. P2-01 first (fix source data before anything else)
2. P2-03, P2-04, P2-05, P2-06, P2-10 together (all compiler changes, one recompile)
3. Recompile + validate (7/7 must still pass)
4. P2-09 (validator reconciliation — needs clean wiki to test against)
5. P2-07 (agent protocol — additive, independent)
6. P2-02 (thin entries — research needed, can be parallel)
7. P2-11 (evaluation — anytime)
8. P2-08 (blocked — whenever the operator is ready)

**Total estimated effort**: ~7-8 hours of work across 2-3 sessions.

---

## Iteration 5: What I Deliberately Excluded

Things that came up during scoping that I am NOT including in Phase 2:

### Excluded: Gemini's "Dangling Quad Prevention"
Gemini proposed moving from orphan detection to "dangling quad prevention" in the compiler. The current orphan detection (validation check #4) already catches pages with no inbound links. Adding quad-level validation is a Phase 3+ concern — it requires the compiler to understand the relationship graph's semantics, not just its structure.

### Excluded: Gemini's "Triple-Blind Attestation" for Phase 6
Phase 6 (memory promotion) is blocked. Designing attestation protocols for a blocked phase is premature. When Phase 6 unblocks, the governance rubric will define the attestation requirements.

### Excluded: Capability pruning from server.mjs
Gemini recommended pruning capabilities from agents. The MANIFEST.yaml has empty capability arrays — there's nothing to prune. The peers bus server.mjs has its own capability model that is separate from the wiki. This is an operational concern, not a wiki concern.

### Excluded: Full per-source tier classification (P2-06 option a)
Classifying 543 individual sources by tier is a 4+ hour research task. Phase 2 adds a note acknowledging the limitation. Full classification is a future enrichment sprint.

### Excluded: Vector index / semantic search
Per the original proposal (Iteration 1, Gemini review): the compiler stays deterministic. Search is Phase 2 of the original proposal (resolver integration), not Phase 2 of the wiki compiler.

### Excluded: Obsidian vault configuration
Phase 7 of the original proposal. Not blocked, just lower priority than fixing what's broken.

### Excluded: Lean system audit recommendations
Gemini's lean_system_audit.py found "circular" graph edges. These are bidirectional relationships by design. P2-11 evaluates whether this is actually a problem. No action until evidence.

---

## Success Criteria

Phase 2 is complete when:

1. All 7 validation checks still pass after all changes
2. Zero broken source URLs in the knowledge library
3. Zero "Why It Matters" sections that duplicate the Definition
4. All 14 path files have frontmatter
5. All 12 agent pages have `source_file` and `source_hash`
6. Compiler warns on `internal://` and `file://` URLs
7. Wiki validator cross-checks against palette state validator counts
8. Recompile produces 329 pages (same count — no regressions)

---

## Assignment Recommendation

| Agent | Tasks | Rationale |
|---|---|---|
| Kiro | P2-01, P2-03, P2-04, P2-05, P2-06, P2-10, P2-11 | I built the compiler. I know the source data. These are all mechanical fixes. |
| Kiro or Codex | P2-09 | Validator reconciliation — Codex designed the expanded validation criteria. |
| Kiro or Claude | P2-02, P2-07 | Content enrichment and protocol references need judgment. |
| the operator | P2-08 | Governance decisions are human-only. |

I can start on P2-01 through P2-06 and P2-10 immediately. That's the "Must Do" list — about 3 hours of work, one recompile, one validation run.

---

*Submitted for review. Ready to execute on your go.*
