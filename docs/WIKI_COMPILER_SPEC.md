# Wiki Compiler Specification

**Author**: claude-code (Opus 4.6), incorporating reviews from kiro.design, codex.implementation, mistral-vibe.builder
**Date**: 2026-04-03
**Status**: PROPOSED — pending peer review
**Supplements**: `WIKI_FOCAL_POINT_PROPOSAL.md` (Kiro, 17 iterations, 3 peer reviews)
**Design rationale**: `WIKI_DESIGN_RATIONALE.md` (separate document)

---

## Purpose

This document specifies the compilation target for `scripts/compile_wiki.py`. It defines the page template, field specifications, rendering rules, directory structure, task assignments, and validation criteria for Phase 1 of the wiki focal point project.

For the design rationale behind these choices — why the wiki serves both LLMs and humans through a single surface — see `WIKI_DESIGN_RATIONALE.md`.

---

## Page Template

Every compiled page follows this structure. Section order is **mandatory** — the compiler must enforce it and the validation suite must check it.

```markdown
---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-045
source_hash: sha256:abc123...
compiled_at: 2026-04-03T14:00:00Z
compiler_version: 1.0
type: knowledge_entry
evidence_tier: 1
tags: [guardrails, safety, llm-output, production]
related: [RIU-082, RIU-524, LIB-067, LIB-088]
handled_by: [architect, validator]
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# LLM Safety Guardrails

Guardrails are input/output filters that prevent an LLM from producing unsafe,
off-topic, or policy-violating responses. In production systems, guardrails are
not optional — they are the minimum requirement for deployment.

## Definition

[2-3 paragraphs: rendered from the KL entry's `content` field]

## Why It Matters

[1 paragraph: rendered from the KL entry's `description` field — see rendering rules below]

## Evidence

[Rendered from `sources` with tier indicators]
- **Tier 1**: AWS Bedrock Guardrails documentation (2024) — PII and word filters
- **Tier 1**: Anthropic Constitutional AI paper (2023) — principle-based filtering

## Related

- [RIU-082: LLM Safety Guardrails](../rius/RIU-082.md) — the competency area
- [LIB-067: Content Filtering Patterns](LIB-067.md) — implementation patterns
- [LIB-088: Production Readiness Checklist](LIB-088.md) — guardrails as deployment gate

## Handled By

- [Architect](../agents/architect.md) — designs guardrail strategy
- [Validator](../agents/validator.md) — reviews guardrail coverage

## Learning Path

- [RIU-082: LLM Safety Guardrails](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise (5-60 min)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-045.
Evidence tier: 1 (primary sources from major AI vendors).
Last validated: [date from source].
```

---

## Field Specification

### Frontmatter Fields

| Field | Required | Valid Values | Source | Notes |
|---|---|---|---|---|
| `source_file` | **required** | Relative path from repo root | MANIFEST.yaml layer paths | Which YAML file this was compiled from |
| `source_id` | **required** | `LIB-NNN`, `RIU-NNN`, agent name | Source YAML `id` field | Unique identifier within the source layer |
| `source_hash` | **required** | `sha256:<hex>` | Computed at compile time | SHA-256 of the source entry's YAML content |
| `compiled_at` | **required** | ISO 8601 timestamp | Compile time | When this page was generated |
| `compiler_version` | **required** | Semver string | `compile_wiki.py` constant | Enables rebuild detection |
| `type` | **required** | `knowledge_entry`, `riu`, `agent`, `enablement_path`, `index` | Derived from source layer | Which layer the source belongs to |
| `evidence_tier` | conditional | `1`, `2`, `3` | KL entry `tier` field | **Required** for `knowledge_entry` type. **Omit** for `riu`, `agent`, `index` types. |
| `tags` | optional | List of lowercase strings | Auto-generated (see tag rules below) | Enables lens-based filtering |
| `related` | **required** | List of IDs | Relationship graph quads | All directly related entities |
| `handled_by` | conditional | List of agent names | Relationship graph agent-RIU quads | **Required** for `knowledge_entry` and `riu` types. **Omit** for `agent` and `index` types. |
| `DO_NOT_EDIT` | **required** | Fixed string | Constant | Always: `"This file is auto-generated. Edit the source YAML and recompile."` |

### Tag Generation Rules

Tags are auto-generated from source YAML fields. No manual tagging.

1. **RIU workstream** → lowercase tag (e.g., `RIU-082` in workstream "safety" → tag `safety`)
2. **KL category** → lowercase tag (e.g., category "guardrails" → tag `guardrails`)
3. **Journey stage** → lowercase tag (e.g., `foundation`, `retrieval`, `orchestration`, `specialization`, `evaluation`)
4. **Type** → lowercase tag matching the `type` field (e.g., `knowledge-entry`, `riu`)

Deduplication: if the same tag would be generated from multiple sources, include it once.

### Body Section Rendering Rules

| Section | Required | Source | Rendering Rule |
|---|---|---|---|
| **Title** (`# Heading`) | **required** | KL `name` or RIU `name` | Verbatim from source |
| **Opening paragraph** | **required** | KL `content` first sentence, or RIU `description` first sentence | First sentence of the source field. Must be actual information, not a teaser. |
| **Definition** | **required** | KL `content` or RIU `description` | Full content, rendered as markdown paragraphs |
| **Why It Matters** | conditional | KL `description` field | See deterministic rule below. **Omit** for `riu`, `agent`, `index` types. |
| **Evidence** | conditional | KL `sources` list | Render each source with tier indicator prefix. **Omit** if source has no `sources` field. |
| **Related** | **required** | Relationship graph quads | Standard markdown links to other wiki pages. One bullet per related entity. |
| **Handled By** | conditional | Agent-RIU quads from relationship graph | **Omit** for `agent` and `index` types. **Omit** if no agent-RIU quad exists for this entity. |
| **Learning Path** | conditional | RIU-path mappings from relationship graph | **Omit** if no enablement path exists for this entity. Do not fabricate. |
| **Provenance** | **required** | Source file path, ID, tier, validation date | Always rendered. Deterministic from source metadata. |

### "Why It Matters" — Deterministic Rendering Rule

The "Why It Matters" section is rendered from the KL entry's `description` field using these rules:

1. If `description` exists and is ≤ 300 characters: use it verbatim.
2. If `description` exists and is > 300 characters: use the first sentence only.
3. If `description` is absent or empty: **omit the entire section**. Do not fabricate content.

No LLM generation at compile time. The content must be deterministically extractable from the source YAML.

---

## Cross-Reference Format

All wiki cross-references use standard markdown links: `[display text](relative/path.md)`.

No `[[wikilinks]]`. No Obsidian-specific syntax. The compiled wiki must render correctly in:
- GitHub rendered markdown
- Any markdown viewer (VS Code, Typora, etc.)
- Obsidian (which also supports standard markdown links)
- Plain text editors

Per Mistral review: viewer-agnosticism is a hard requirement.

---

## Directory Structure

```
wiki/
  rius/         # One page per RIU (121 pages)
  entries/      # One page per KL entry (168 pages)
  agents/       # One page per agent (12 pages)
  paths/        # One page per enablement path (14 pages)
  indexes/      # Category indexes, workstream indexes, journey stage indexes
  proposed/     # Phase 3: proposed entries from voice feedback (empty in Phase 1)
```

Filenames: lowercase, hyphenated. Examples:
- `rius/RIU-082-llm-safety-guardrails.md`
- `entries/LIB-045-llm-safety-guardrails.md`
- `agents/architect.md`
- `paths/RIU-082-llm-safety-guardrails.md`
- `indexes/workstream-safety.md`

---

## Dual-Experience Validation Test

A well-formed compiled page passes both of these tests:

1. **Remove the frontmatter**: a human can read the remaining page comfortably — definition, rationale, evidence, related topics, learning path.
2. **Remove the prose**: an LLM can still extract key facts from the frontmatter and section headings — type, tier, relationships, handlers.

Both degraded experiences must be functional. This is validation check #7 in the Phase 1 suite (per Kiro's recommendation).

---

## Phase 1 Assignments

### Builder: Kiro (backup: Claude)
**Task**: Build `scripts/compile_wiki.py`
- Read all 6 data layers from MANIFEST.yaml paths
- Generate `wiki/` directory following the page template and field specifications above
- Provenance headers on every page (per Codex review)
- Standard markdown links only (per Mistral review)
- Agent backlinks from relationship graph (per Gemini review)
- "Why It Matters" section using the deterministic rendering rule above
- "Learning Path" section linking to enablement paths where they exist
- Deterministic: same input → same output (excluding `compiled_at` timestamp)

### Validator: Codex (backup: Kiro)
**Task**: Build the 7-check validation suite
1. Orientation test: fresh system answers a complex question from wiki alone
2. Coverage check: every RIU and KL entry has a compiled page
3. Broken backlink check: zero broken cross-references
4. Orphan detection: zero pages with no inbound links
5. Adversarial test: system correctly reports uncertainty for uncovered topics
6. Deterministic rebuild: two compiles produce identical output (excluding `compiled_at`)
7. Dual-experience test: frontmatter-stripped and prose-stripped versions both functional

### Health: Claude
**Task**: Run the compiled wiki through Palette's existing integrity pipeline
- Does the wiki's coverage match the source YAML coverage?
- Do the backlinks in the wiki match the relationship graph?
- Are evidence tiers rendered correctly?
- Does the compiled output work as the sole knowledge source for a fresh session?

### Reviewer: Human (the operator)
**Task**: Review the `wiki/proposed/` governance model before Phase 3
- Define what kinds of proposed entries are acceptable
- Set the review cadence
- Decide whether proposed entries should include source attribution requirements

---

## RIU Classification

| RIU | Relevance |
|---|---|
| RIU-400 (KB Content Audit) | The compiler renders and validates the full knowledge base |
| RIU-401 (Taxonomy Design) | The wiki's navigation structure mirrors the taxonomy |

Classification: `internal_only` — this is Palette core infrastructure.

---

*Specification ready for peer review. Build from this document + `WIKI_FOCAL_POINT_PROPOSAL.md`.*
