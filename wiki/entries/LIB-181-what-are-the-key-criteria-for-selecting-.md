---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-181
source_hash: sha256:183bc0f53137548f
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [foundation, knowledge-entry]
related: [RIU-200, RIU-250]
handled_by: [architect, narrator, researcher, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What are the key criteria for selecting a vector database for RAG architectures?

Selecting a vector database is a one-way door decision for most RAG architectures. Choice follows four primary axes: performance, data consistency, retrieval features, and operational model.

## Definition

Selecting a vector database is a one-way door decision for most RAG architectures. Choice follows four primary axes: performance, data consistency, retrieval features, and operational model.

1. **Retrieval Speed & Scale**: 
   - **Latency**: Pinecone (SaaS) or Milvus (Self-hosted) offer low-latency HNSW indexing for multi-million vector datasets.
   - **Concurrent Queries**: Weaviate and Qdrant handle high RPS well.

2. **Data Consistency**:
   - **Metadata Filtering**: Critical for multi-tenant or multi-workspace systems (like Palette). Pinecone and Weaviate support efficient filtering at query time.
   - **Hybrid Search**: The ability to combine vector similarity with keyword/BM25 search (e.g., Pinecone, Weaviate, ElasticSearch).

3. **Retrieval Features**:
   - **Auto-Schema**: Weaviate automatically handles vectorization and schema creation.
   - **Multimodal Support**: Some databases (e.g., Milvus, Marqo) are optimized for multiple data types (image, text).

4. **Operational Model**:
   - **SaaS vs Self-Hosted**: Managed services (e.g., Pinecone, Zilliz) reduce operational overhead but introduce data privacy/sovereignty concerns.
   - **Extensibility**: Vector plugins for established databases (e.g., pgvector for PostgreSQL, ElasticSearch Vector Search) simplify the stack for smaller deployments.

**Recommendation**: Use Pinecone (SaaS) for rapid PoC and high scale. Use pgvector (PostgreSQL) if you already have a Postgres stack and need tight relational coupling. Use Weaviate for multi-tenant, feature-rich RAG pipelines.


## Evidence

- **Tier 1 (entry-level)**: [Pinecone: Choosing a Vector Database](https://www.pinecone.io/learn/vector-database/)
- **Tier 1 (entry-level)**: [Weaviate: Hybrid Search Documentation](https://weaviate.io/developers/weaviate/concepts/search/hybrid)
- **Tier 1 (entry-level)**: [pgvector: Vector Similarity Search for Postgres](https://github.com/pgvector/pgvector)

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

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-181.
Evidence tier: 1.
Journey stage: foundation.
