---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-185
source_hash: sha256:95e3699d2ed5f513
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

# What are graph-based knowledge retrieval (GraphRAG) techniques and how do they differ from vector RAG?

GraphRAG combines the semantic similarity of vector search with the structured relationships of a knowledge graph (KG) to enable more complex, multi-hop reasoning. While vector RAG retrieves isolated chunks based on similarity, GraphRAG retrieves clusters of related entities and their context.

## Definition

GraphRAG combines the semantic similarity of vector search with the structured relationships of a knowledge graph (KG) to enable more complex, multi-hop reasoning. While vector RAG retrieves isolated chunks based on similarity, GraphRAG retrieves clusters of related entities and their context.

1. **Key Differences**:
   - **Vector RAG**: Best for finding specific facts or answering simple questions based on document similarity. Fails on global, thematic questions or queries requiring multi-hop reasoning.
   - **GraphRAG**: Best for understanding relationships, global themes, and indirect connections. Can answer questions like 'What are the three common failure modes across all 12 projects?' by traversing edges.

2. **Core Techniques**:
   - **Entity Extraction**: Use an LLM to identify and extract entities (nodes) and their relationships (edges) from unstructured text.
   - **Knowledge Graph Construction**: Build a graph from the extracted data (e.g., in Neo4j, FalkorDB).
   - **Global Retrieval (Map-Reduce)**: Use community detection algorithms (e.g., Leiden) to group the graph into clusters. Summarize each cluster, then use an LLM to synthesize an answer from the cluster summaries.
   - **Local Retrieval (Multi-hop Search)**: Starting from a detected entity in the query, traverse the graph to find neighboring nodes and their properties.

3. **Implementation Benefits**:
   - **Lower Hallucination Rate**: By grounding the response in a verified relationship graph, GraphRAG reduces the likelihood of the LLM inventing non-existent links.
   - **Improved Explainability**: Responses can cite specific nodes and edges as evidence, providing a clear audit trail.

**Implementation Threshold**: Transition from vector RAG to GraphRAG when your system requires 'summarization' of large datasets or 'connection detection' across disparate domains.


## Evidence

- **Tier 1 (entry-level)**: [Microsoft Research: From Local to Global: A GraphRAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130)
- **Tier 1 (entry-level)**: [Neo4j: Knowledge Graphs for RAG](https://neo4j.com/generative-ai/knowledge-graphs-for-rag/)
- **Tier 1 (entry-level)**: [Why GraphRAG is better than Vector RAG](https://www.falkordb.com/blog/graphrag-vs-vectorrag/)

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

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-185.
Evidence tier: 1.
Journey stage: foundation.
