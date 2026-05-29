---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-187
source_hash: sha256:95913840f1d9b410
compiled_at: 2026-05-27T22:42:24Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 2
tags: [bm25, fts5, hybrid-search, knowledge-entry, retrieval, vector-search]
related: [RIU-200, RIU-250]
handled_by: [architect, narrator, researcher, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How does Palette's hybrid retrieval work and what are the three retrieval modes?

Palette V3 retrieves knowledge using three complementary modes, applied after taxonomy routing selects the domain:

## Definition

Palette V3 retrieves knowledge using three complementary modes, applied after taxonomy routing selects the domain:

1. **keyword_resolve** (existing, V2): Token-prefix matching against knowledge library questions. Fast, deterministic, zero dependencies. Handles exact-term queries well but misses semantic similarity.

2. **FTS5 full-text search** (V3): SQLite FTS5 with Porter stemming on KL questions and answers. Handles morphological variants (evaluate/evaluation/evaluating). BM25 ranking. Zero new dependencies — extends the existing bus message search pattern.

3. **Vector similarity** (V3): Ollama nomic-embed-text embeddings stored as JSON. Handles paraphrase and concept queries ('irreversible choice' finds 'one-way door'). Local, free, 274MB model.

**Reranking**: Results from all three modes are combined using reciprocal rank fusion, then weighted by (0.4 × relevance) + (0.3 × authority_tier) + (0.3 × freshness).

**Measured performance**: keyword_resolve alone = 28% recall. FTS5 alone = 39%. Hybrid (all three + fusion) targets ≥70%.

**Key principle**: Taxonomy routing selects the DOMAIN (which RIUs). Hybrid retrieval selects the ENTRY (which knowledge). Two layers, both local, both auditable.

## Evidence

- **Tier 2 (entry-level)**: Kiro V3 Deep Analysis — FTS5 and vector retrieval testing (`Documents/conference/V3_DEEP_ANALYSIS_KIRO.md`)
- **Tier 2 (entry-level)**: [Linus Lee — 'BM25 does better than vector. Hybrid search: BM25 FTS K×2 + Vector K×2 + rerank'](https://aicouncil.com)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-200](../rius/RIU-200.md)
- [RIU-250](../rius/RIU-250.md)

## Handled By

- [Architect](../agents/architect.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-187.
Evidence tier: 2.
Journey stage: retrieval.
