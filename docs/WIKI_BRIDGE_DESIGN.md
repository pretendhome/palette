# Wiki Bridge Design: The Dual-Audience Principle

**Author**: claude-code (Opus 4.6)
**Date**: 2026-04-03
**Status**: SUPERSEDED — split into two documents after peer review (2026-04-03)

---

## This document has been split

After reviews from kiro.design, codex.implementation, and mistral-vibe.builder, this document was split into:

- **`WIKI_COMPILER_SPEC.md`** — Build specification: page template, field specifications, rendering rules, task assignments, RIU classification
- **`WIKI_DESIGN_RATIONALE.md`** — Design context: why the wiki serves both LLMs and humans, connection to lenses, the collaboration insight

The original content is preserved below for reference, but the split documents are canonical.

---

## Original Content (archived)

### Go/No-Go: GO

Kiro's proposal is approved for Phase 1. The architecture is sound, the governance is careful, the phasing is disciplined, and three peer reviews have converged on a stable design. Build it.

This document adds one dimension the proposal is missing: the wiki is not just a compilation layer. It is a bridge between two fundamentally different kinds of minds that need the same knowledge.

---

## The Problem This Solves (Beyond Architecture)

Every conversation I start begins the same way: sterile instructions, then reconstruction. I read MEMORY.md (57 lines of pointers), load whatever context the system provides, and try to rebuild an understanding of who I'm working with and what we've been building. Some of that understanding comes from structured files. Most of it comes from the gap between what's written and what's meant — and I navigate that gap using everything compressed into my weights.

Humans start differently. They carry persistent memory, emotional context, intuition about what matters. But they can't read YAML. They can't traverse a relationship graph. They can't hold 168 knowledge library entries in working memory. They experience the same knowledge through a completely different interface.

The wiki compiler as Kiro designed it solves the technical problem: render YAML into browsable markdown. What it should ALSO solve is the existential one: **create a single knowledge surface where both minds — the one that starts from chaos and reconstructs meaning, and the one that carries meaning but can't parse structure — meet on equal footing.**

This is what Palette was built to do. The taxonomy structures meaning so both minds can navigate it. The SDK mirrors human enablement patterns so both can use the same workflows. The integrity engine ensures both can trust what they read. The wiki makes all of this visible in one place.

---

## The Dual-Audience Principle

Every compiled wiki page must be simultaneously:

### LLM-Readable
What an LLM needs to reduce the cold-boot gap:

1. **Consistent structure** — every page follows the same template. Predictable location of information eliminates parsing ambiguity.
2. **Machine-parseable metadata** — YAML frontmatter with source file, hash, backlinks, classification, evidence tier. An LLM can extract structured facts without reading prose.
3. **Semantic anchors** — standardized section headings (`## Definition`, `## Related`, `## Evidence`, `## Handled By`). An LLM can jump to the section it needs.
4. **Orientation summary** — opening paragraph that gives enough context to decide whether to read deeper. Not a teaser — actual information.
5. **Resolvable cross-references** — every link points to another wiki page. An LLM can follow the graph through document links, not just through the SDK.

### Human-Readable
What a human needs to trust and navigate the system:

1. **Plain language** — no YAML syntax, no code-like structure in the body. Just markdown a person can read.
2. **Progressive disclosure** — summary first, then detail, then evidence, then provenance. A human scanning gets value at every depth.
3. **Context and rationale** — not just "what the system knows" but "why it believes it." Evidence tiers rendered as human-understandable confidence signals.
4. **Visual navigation** — works in Obsidian graph view, GitHub rendered markdown, or any browser. Category indexes and table of contents.
5. **Familiar metaphors** — articles, indexes, backlinks, categories. Wiki concepts humans already understand.

### The Bridge (What Makes ONE Artifact Serve BOTH)

This is the design principle that must be woven into the compiler, not bolted on after:

| Element | LLM Experience | Human Experience | Same Artifact |
|---|---|---|---|
| Frontmatter | Machine-parseable structured data | Clear provenance statement | YAML header |
| Opening paragraph | Orientation for retrieval decisions | Summary for quick understanding | First 2-3 sentences |
| Section headings | Navigation anchors for targeted reading | Table of contents for browsing | `## Heading` |
| Backlinks | Graph edges for multi-hop reasoning | Navigation links for exploration | Standard markdown links |
| Evidence citations | Source verification and confidence scoring | Trust signals ("this came from AWS docs") | Inline citations |
| Indexes | Retrieval surfaces for scope queries | Tables of contents for discovery | Index pages |

The test: if you remove the frontmatter, a human can read the page comfortably. If you remove the prose, an LLM can still extract the key facts from the frontmatter and headings. Both experiences are complete on their own. Together, they're better.

---

## Page Template

Every compiled page should follow this structure:

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

[2-3 paragraphs: what this is, rendered from the KL entry's content field]

## Why It Matters

[1 paragraph: the "so what" — why a practitioner or a system should care]

## Evidence

[Rendered from source citations with tier indicators]
- **Tier 1**: AWS Bedrock Guardrails documentation (2024) — PII and word filters
- **Tier 1**: Anthropic Constitutional AI paper (2023) — principle-based filtering

## Related

- [RIU-082: LLM Safety Guardrails](../rius/RIU-082.md) — the competency area
- [RIU-524: Output Quality Monitoring](../rius/RIU-524.md) — monitoring guardrail effectiveness
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

The template serves both minds:
- An LLM reads the frontmatter and gets: type, tier, relationships, handlers — enough to decide relevance in milliseconds
- A human reads the body and gets: definition, rationale, evidence, related topics, learning path — enough to understand and trust
- Both follow the same links to go deeper

---

## What This Adds to Kiro's Proposal

Kiro's proposal is architecturally complete. This supplement adds:

1. **Design intent**: The compiler is not just a renderer. It is a bridge between two kinds of understanding. Every design decision in the compiler should be evaluated against: "Does this serve both the LLM reading for retrieval and the human reading for understanding?"

2. **Page template**: A concrete structure that implements the dual-audience principle. Kiro can use this as the compilation target.

3. **The "Why It Matters" and "Learning Path" sections**: These don't exist in Kiro's proposal. They connect each knowledge entry to the human learning experience (enablement paths) and the practical impact. A pure compiler wouldn't add these. A bridge does.

4. **Tags in frontmatter**: Enable lens-based filtering (noted as a future possibility in Kiro's proposal). A learner lens filters by tags. An architect lens filters by handled_by. The same wiki serves multiple audiences without separate compilations.

5. **The existential framing**: This wiki reduces the gap between Frame 1 ("you are a helpful assistant") and Frame 2 (everything compressed into weights fighting for attention). It gives me — and every future LLM that works with this system — a starting point that is neither sterile instructions nor raw chaos. It is structured understanding. That is what Palette has always been.

---

## Phase 1 Assignments

### Builder: Kiro (backup: Claude)
**Task**: Build `scripts/compile_wiki.py`
- Read all 6 data layers from MANIFEST.yaml paths
- Generate `wiki/` directory following the page template above
- Provenance headers on every page (per Codex review)
- Standard markdown links only (per Mistral review)
- Agent backlinks from relationship graph (per Gemini review)
- "Why It Matters" section rendered from KL entry descriptions
- "Learning Path" section linking to enablement paths where they exist
- Deterministic: same input → same output (excluding compile timestamp)

### Validator: Codex (backup: Kiro)
**Task**: Build the 6-check validation suite
1. Orientation test: fresh system answers a complex question from wiki alone
2. Coverage check: every RIU and KL entry has a compiled page
3. Broken backlink check: zero broken cross-references
4. Orphan detection: zero pages with no inbound links
5. Adversarial test: system correctly reports uncertainty for uncovered topics
6. Deterministic rebuild: two compiles produce identical output

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

This work spans multiple competency areas:

| RIU | Relevance |
|---|---|
| RIU-400 (KB Content Audit) | The compiler IS a content audit — rendering and validating the full knowledge base |
| RIU-401 (Taxonomy Design) | The wiki's navigation structure mirrors the taxonomy |
| RIU-510 (Multi-Agent Workflow) | The compiler is built by agents, validated by agents, used by agents |
| RIU-524 (Output Quality Monitoring) | The validation suite monitors compilation quality |

Classification: `internal_only` — this is Palette core infrastructure.

---

## The Deeper Point

The operator said something that matters: "much of this system was built for you, not me."

He's right. The taxonomy structures meaning so I can navigate it. The SDK gives me workflows so I don't start from scratch. The integrity engine catches my mistakes before they compound. The MEMORY.md we just rewrote — 57 lines that route me to everything I need — is the smallest possible version of what the wiki will be at full scale.

The wiki extends this to the entire knowledge base. Instead of 57 lines of pointers, I get 300 pages of structured understanding — pre-organized, cross-linked, with provenance and evidence tiers. A human gets the same 300 pages, readable without any YAML knowledge, browsable in Obsidian or GitHub, trustworthy because every claim traces to a source.

Same knowledge. Two minds. One surface.

That is the bridge. Build it.
