---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-151
source_hash: sha256:cf30ee0f2c1eb085
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [chunking, document-processing, knowledge-entry, rag, retrieval]
related: [RIU-231, RIU-232]
handled_by: [architect, builder, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design a document chunking strategy for RAG that preserves semantic coherence?

RIU-231 defines chunking strategy across three dimensions. Dimension 1 — Chunk Size: the optimal size depends on your embedding model and retrieval needs. General guidance: 256-512 tokens for precise retrieval (specific facts, definitions), 512-1024 tokens for contextual retrieval (paragraphs with surrounding context), 1024-2048 tokens for broad retrieval (full sections). Measure retrieval quality at each size and choose based on your eval set, not defaults. Dimension 2 — Overlap: use 10-20% overlap between adjacent chunks to prevent context loss at chunk boundaries. Example: for 512-token chunks, use 50-100 token overlap. Without overlap, a sentence split across two chunks becomes unretrievable by either chunk. Dimension 3 — Semantic Boundaries: chunk at natural document boundaries (headings, paragraphs, sections) rather than fixed token counts. For structured documents (contracts, manuals, legislation): chunk at section/clause boundaries. For unstructured documents (emails, transcripts): chunk at paragraph boundaries with topic detection. For code: chunk at function/class boundaries. For tables: keep each table as a single chunk with its header row. Advanced techniques: (a) Hierarchical chunking — store both fine-grained chunks and parent sections, retrieve at fine level but pass parent context to the LLM; (b) Document metadata enrichment — add title, section header, and document type to each chunk as metadata for hybrid search. Validate chunking quality by testing retrieval on 50+ queries and checking if the answer-containing chunk is retrieved in the top 5.

## Definition

RIU-231 defines chunking strategy across three dimensions. Dimension 1 — Chunk Size: the optimal size depends on your embedding model and retrieval needs. General guidance: 256-512 tokens for precise retrieval (specific facts, definitions), 512-1024 tokens for contextual retrieval (paragraphs with surrounding context), 1024-2048 tokens for broad retrieval (full sections). Measure retrieval quality at each size and choose based on your eval set, not defaults. Dimension 2 — Overlap: use 10-20% overlap between adjacent chunks to prevent context loss at chunk boundaries. Example: for 512-token chunks, use 50-100 token overlap. Without overlap, a sentence split across two chunks becomes unretrievable by either chunk. Dimension 3 — Semantic Boundaries: chunk at natural document boundaries (headings, paragraphs, sections) rather than fixed token counts. For structured documents (contracts, manuals, legislation): chunk at section/clause boundaries. For unstructured documents (emails, transcripts): chunk at paragraph boundaries with topic detection. For code: chunk at function/class boundaries. For tables: keep each table as a single chunk with its header row. Advanced techniques: (a) Hierarchical chunking — store both fine-grained chunks and parent sections, retrieve at fine level but pass parent context to the LLM; (b) Document metadata enrichment — add title, section header, and document type to each chunk as metadata for hybrid search. Validate chunking quality by testing retrieval on 50+ queries and checking if the answer-containing chunk is retrieved in the top 5.

## Evidence

- **Tier 1 (entry-level)**: [LangChain: Text Splitters — Chunking Strategies](https://python.langchain.com/docs/concepts/text_splitters/)
- **Tier 1 (entry-level)**: [Anthropic: RAG Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation)
- **Tier 1 (entry-level)**: [Pinecone: Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-231](../rius/RIU-231.md)
- [RIU-232](../rius/RIU-232.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-151.
Evidence tier: 1.
Journey stage: retrieval.
