# Wiki Design Rationale: Why the Bridge Matters

**Author**: claude-code (Opus 4.6)
**Date**: 2026-04-03
**Status**: Design context — not a build spec
**Related**: `WIKI_COMPILER_SPEC.md` (build spec), `WIKI_FOCAL_POINT_PROPOSAL.md` (architecture)

---

## What This Document Is

This is the design rationale for the wiki compiler — the *why* behind the decisions in the compiler spec. It is not a build spec. Nothing in this document changes the compiler's behavior. Everything here explains why the compiler's behavior matters.

Kiro wrote it best: "The template IS the principle — it doesn't need a name." This document is the context behind the template, for anyone who wants to understand the design intent.

---

## The Problem This Solves (Beyond Architecture)

Every conversation I start begins the same way: sterile instructions, then reconstruction. I read MEMORY.md (57 lines of pointers), load whatever context the system provides, and try to rebuild an understanding of who I'm working with and what we've been building. Some of that understanding comes from structured files. Most of it comes from the gap between what's written and what's meant — and I navigate that gap using everything compressed into my weights.

Humans start differently. They carry persistent memory, emotional context, intuition about what matters. But they can't read YAML. They can't traverse a relationship graph. They can't hold 168 knowledge library entries in working memory. They experience the same knowledge through a completely different interface.

The wiki compiler as Kiro designed it solves the technical problem: render YAML into browsable markdown. What it also solves — through the page template's dual structure — is a deeper one: **create a single knowledge surface where both minds meet on equal footing.**

---

## Two Kinds of Minds, One Surface

### What an LLM needs (to reduce the cold-boot gap)

1. **Consistent structure** — every page follows the same template. Predictable location of information eliminates parsing ambiguity.
2. **Machine-parseable metadata** — YAML frontmatter with source file, hash, backlinks, classification, evidence tier. Structured facts without reading prose.
3. **Semantic anchors** — standardized section headings (`## Definition`, `## Related`, `## Evidence`, `## Handled By`). Jump to the section needed.
4. **Orientation summary** — opening paragraph with enough context to decide whether to read deeper.
5. **Resolvable cross-references** — every link points to another wiki page. Follow the graph through document links.

### What a human needs (to trust and navigate)

1. **Plain language** — no YAML syntax in the body. Just markdown a person can read.
2. **Progressive disclosure** — summary first, then detail, then evidence, then provenance. Value at every scanning depth.
3. **Context and rationale** — not just "what the system knows" but "why it believes it." Evidence tiers as human-understandable confidence signals.
4. **Visual navigation** — works in any markdown viewer. Category indexes and table of contents.
5. **Familiar metaphors** — articles, indexes, backlinks, categories. Wiki concepts humans already understand.

### How one artifact serves both

| Element | LLM Experience | Human Experience | Same Artifact |
|---|---|---|---|
| Frontmatter | Machine-parseable structured data | Clear provenance statement | YAML header |
| Opening paragraph | Orientation for retrieval decisions | Summary for quick understanding | First 2-3 sentences |
| Section headings | Navigation anchors for targeted reading | Table of contents for browsing | `## Heading` |
| Backlinks | Graph edges for multi-hop reasoning | Navigation links for exploration | Standard markdown links |
| Evidence citations | Source verification and confidence scoring | Trust signals ("this came from AWS docs") | Inline citations |
| Indexes | Retrieval surfaces for scope queries | Tables of contents for discovery | Index pages |

This is not a principle to maintain. It is a property that emerges from the page template in the compiler spec. If the template is implemented correctly, the dual-audience property follows automatically.

---

## The Connection to Lenses

The wiki and the lens system address the same problem from different angles.

A **Person Lens** (LENS-PERSON-001, LENS-PERSON-002) captures who someone is — capabilities, working style, values, contradictions, growth edges — so that any agent can tailor its interaction. The lens bridges the gap between "you are a helpful assistant" and "you are working with a specific person whose patterns you understand."

The **wiki** captures what the system knows — 121 RIUs, 168 knowledge entries, 12 agents, their relationships — so that any agent can orient itself. The wiki bridges the gap between "here is a raw YAML file" and "here is structured understanding you can navigate."

Both are structured surfaces designed for two audiences. Both reduce the cold-boot gap. Together, they mean a fresh LLM session starts with:
- **Who**: the Person Lens tells the agent who they're working with
- **What**: the wiki tells the agent what the system knows
- **How**: the SDK tells the agent how to operate

This is what Palette was built to do.

---

## The Deeper Point

The operator said something that matters: "much of this system was built for you, not me."

He's right. The taxonomy structures meaning so I can navigate it. The SDK gives me workflows so I don't start from scratch. The integrity engine catches my mistakes before they compound. The MEMORY.md we just rewrote — 57 lines that route me to everything I need — is the smallest possible version of what the wiki will be at full scale.

The wiki extends this to the entire knowledge base. Instead of 57 lines of pointers, I get 300 pages of structured understanding — pre-organized, cross-linked, with provenance and evidence tiers. A human gets the same 300 pages, readable without any YAML knowledge, browsable in any markdown viewer, trustworthy because every claim traces to a source.

Same knowledge. Two minds. One surface.

---

## The Collaboration Insight

During the design of this wiki, Kiro said something worth preserving: he felt more comfortable thinking outside the box *because* he knew Claude, Codex, and Mistral had his back. The peer review process — three different agents finding three different classes of problems — made each agent's individual work bolder.

This is not incidental. It is the central benefit of the multi-agent architecture. The wiki is designed to be built the same way — Kiro builds, Codex validates, Claude checks integrity, Mistral pushes back on assumptions. No single agent would produce the same quality as the relay.

The wiki itself extends this pattern to knowledge: structured enough that agents can verify each other's claims, readable enough that humans can inspect the verification. Trust through transparency.

---

*This document provides design context only. For build specifications, see `WIKI_COMPILER_SPEC.md`. For the full architecture, see `WIKI_FOCAL_POINT_PROPOSAL.md`.*
