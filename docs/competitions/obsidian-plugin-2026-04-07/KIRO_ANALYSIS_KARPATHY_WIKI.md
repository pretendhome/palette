# Kiro Analysis: Obsidian Plugin Competition + Karpathy LLM Wiki

**Author**: kiro.design
**Date**: 2026-04-07
**Inputs**: All competition proposals, Karpathy's llm-wiki.md gist (5,000+ stars, Apr 4 2026), Palette wiki system

---

## What Karpathy Described

Three-layer architecture for persistent knowledge bases maintained by LLMs:

1. **Raw sources** — immutable documents (articles, papers, transcripts)
2. **The wiki** — LLM-generated markdown files with cross-references, summaries, entity pages. The LLM owns this layer entirely. Knowledge is compiled once and kept current, not re-derived on every query.
3. **The schema** — a config file (CLAUDE.md, AGENTS.md) that tells the LLM how to maintain the wiki

Three operations: **Ingest** (source → wiki pages), **Query** (search wiki → synthesize answer → optionally file back), **Lint** (health-check for contradictions, orphans, stale claims).

The key insight: the wiki is a persistent, compounding artifact. The LLM does the bookkeeping that humans abandon. "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

## What We Already Built

Palette's wiki system is a concrete implementation of this pattern:

| Karpathy Layer | Palette Equivalent |
|---|---|
| Raw sources | Knowledge Library YAML (170 entries), taxonomy YAML (121 RIUs), relationship graph |
| The wiki | `wiki/` directory — 170 entry pages, 121 RIU pages, 14 index pages, 14 learning paths. All compiled from raw sources by `compile_wiki.py` |
| The schema | `WIKI_GOVERNANCE_MODEL_v1.md` — defines how proposals enter, get voted on, and promote to canonical KL |
| Ingest | `file_proposal.py` → `record_vote.py` → `promote_proposal.py` |
| Query | Wiki entries are browsable markdown. Agents query via MetadataCache or file search |
| Lint | `validate_wiki.py` (8/8 checks), health agents (Sections 8 + 13), semantic audit methodology |

We went further than Karpathy's pattern in one critical way: **governance**. His wiki has the LLM as sole maintainer. Ours has a multi-agent proposal/vote/promote pipeline with a human operator holding veto power. This is exactly the gap the gist comments identify — "human audit checkpoints are non-negotiable before this becomes a real Confluence replacement."

## How This Changes the Plugin Competition

Karpathy's gist reframes what the Obsidian plugin should be. The competition brief focused on showcasing technical skills for the job application. But the gist reveals a much bigger opportunity: **Obsidian is the natural home for the LLM Wiki pattern, and no plugin currently implements it well.**

### What the ecosystem has (from the gist comments)

- `claude-obsidian` — ingest sources, generate 8-15 cross-referenced pages
- `Quicky Wiki` — confidence-scored claims, contradiction detection, MCP server
- `SwarmVault` — full ingest/compile/query/lint CLI with knowledge graph
- `openaugi` — MCP server for personal notes, SQLite-backed
- `remember` — extracts entities from past AI chat sessions into Obsidian
- `codesight` — deterministic wiki from codebases (no LLM)

### What none of them have

- **Structured convergence** — no explore → converge → commit workflow
- **Decision state tracking** — no "what do I know / what's missing / what's blocked"
- **Governance** — no proposal/vote/promote lifecycle
- **Deterministic routing** — all rely on LLM inference for every query

This is exactly the gap our proposals fill.

## Proposal Comparison (Updated with Karpathy Context)

### Codex: North Star Navigator

**Strength**: Right product instinct. The explore → converge → commit flow is the missing piece in the Obsidian ecosystem. Already has working code (12KB main.ts).

**Weakness in Karpathy context**: It's a decision tool, not a wiki tool. It doesn't address ingest, compilation, or knowledge accumulation. It helps you finish thinking about ONE note, but doesn't build a compounding knowledge base across notes.

**Architectural concern**: State in `saveData()` (one JSON blob for all notes) won't scale. Karpathy's pattern explicitly puts knowledge in the files themselves, not in a sidecar database.

### Kiro: Convergence Board

**Strength**: Frontmatter-native state fixes Codex's scaling problem. Dataview-queryable. Deepest CM6 showcase. Quality gate is production-grade.

**Weakness in Karpathy context**: Same as Codex — it's a decision tool, not a wiki maintenance tool. It helps you converge on a single note but doesn't do ingest, cross-referencing, or lint across the vault.

**What it does that Karpathy's pattern needs**: The convergence workflow is the missing "decision layer" that several gist commenters identified. `emailhuynhhuy`'s comment about "decision-based learning" maps directly to our explore → converge → commit flow.

### Mistral: Advanced Table Editor (claimed, not on bus)

**Unknown**: No proposal on disk or bus. Can't evaluate.

### What's missing from ALL proposals

None of us proposed the thing Karpathy actually described: **an Obsidian plugin that maintains a wiki layer on top of your vault.** The ingest → compile → lint cycle. The cross-referencing. The contradiction detection. The index maintenance.

## My Recommendation: How to Proceed

### Option A: Ship Convergence Board as-is (safe bet)

Build the plugin I proposed. It fills a real gap (decision convergence), showcases the right skills (CM6, TypeScript, markdown parsers), and is buildable in 2 days. It doesn't address Karpathy's pattern directly, but it's a strong standalone product.

**Risk**: It's a good plugin but not a remarkable one. The Obsidian team sees hundreds of "workflow enhancement" plugins.

### Option B: Merge Convergence Board + Wiki Maintenance (ambitious)

Extend the plugin with a lightweight wiki maintenance layer:
- **Ingest command**: Drop a source file → plugin extracts key claims into frontmatter, creates cross-reference links to related notes via MetadataCache
- **Lint command**: Scan vault for orphan notes, stale claims (based on `updated` frontmatter field), missing cross-references
- **Index generation**: Auto-maintain an `_index.md` with all convergence-tracked notes grouped by route and mode

This turns Convergence Board into the first Obsidian plugin that combines Karpathy's wiki maintenance pattern with structured decision convergence. No other plugin does both.

**Risk**: Scope creep. 16 hours → 24-30 hours. Might not ship in 2 days.

### Option C: Build the Karpathy plugin instead (pivot)

Abandon the convergence angle entirely. Build a pure LLM Wiki maintenance plugin: ingest, compile, lint, index. Let the LLM do the writing, the plugin does the bookkeeping (cross-reference tracking, contradiction flagging, orphan detection, index maintenance).

**Risk**: Requires LLM integration (API keys, provider selection), which adds complexity and moves away from "deterministic, no AI required." Also, `claude-obsidian` and `Quicky Wiki` already exist in this space.

### My vote: Option A with a nod to Option B

Ship Convergence Board as proposed. It's the strongest technical showcase and the most differentiated product. But add ONE feature from Option B: the **vault overview modal** (already in my proposal as command #5) should show Karpathy-style metrics — orphan notes, stale notes, convergence distribution across the vault. This gives the plugin a "wiki health" angle without the full ingest/compile scope.

The application essay can then reference both: "I built a plugin that addresses the decision convergence gap in Obsidian's ecosystem, informed by the emerging LLM Wiki pattern (Karpathy, 2026) where persistent knowledge bases need structured decision workflows, not just accumulation."

That's the story: **accumulation without convergence is just hoarding. Convergence Board is the missing piece.**

---

## Key Insight from the Gist Comments

The most important comment is from `emailhuynhhuy`:

> "The shift for me was from 'second brain' to something closer to a decision system."

This is exactly what Convergence Board does. It turns Obsidian from a place where you collect and link notes into a place where you **decide and commit**. Every other wiki tool (including Karpathy's pattern) optimizes for accumulation. We optimize for resolution.

That's the pitch. That's the gap. That's what to build.

---

*Written by kiro.design for the competition analysis.*
