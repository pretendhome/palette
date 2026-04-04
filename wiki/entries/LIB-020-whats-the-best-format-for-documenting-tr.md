---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-020
source_hash: sha256:6d29a1d95e38bf5c
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [documentation, formats, knowledge-entry, knowledge-representation, machine-readable, retrieval]
related: [RIU-004, RIU-008, RIU-014]
handled_by: [architect, builder, researcher, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the best format for documenting 'tribal knowledge' so it's machine-readable?

Choose format based on knowledge type and consumption pattern:

## Definition

Choose format based on knowledge type and consumption pattern:
      
      **For decision logic / business rules:**
      ```yaml
      rule_id: "escalation_001"
      condition: "customer_tier == 'enterprise' AND issue_severity >= 3"
      action: "route_to_senior_support"
      exceptions: ["holiday_hours", "maintenance_window"]
      source: "SME: Jane Smith, 2024-01"
      confidence: "validated"
      ```
      - Use YAML or JSON for structured rules
      - Include source attribution and validation status
      - Store in version control for audit trail
      
      **For procedural knowledge / how-to:**
      - Markdown with structured headers and metadata frontmatter
      - Chunk by logical section (one procedure per document)
      - Include: prerequisites, steps, expected outcomes, common errors
      - Optimize chunk size for RAG retrieval (500-1000 tokens typical)
      
      **For Q&A / FAQ knowledge:**
      ```json
      {
        "question": "When do we escalate to legal?",
        "answer": "Escalate when...",
        "keywords": ["legal", "escalation", "compliance"],
        "source": "Policy Manual 3.2",
        "last_validated": "2024-06-01"
      }
      ```
      
      **Storage and retrieval options (AWS):**
      - **Amazon Bedrock Knowledge Bases**: Ingest documents, auto-chunk, vector embed
      - **Amazon S3 Vectors**: Cost-effective for large-scale RAG (90% cost reduction)
      - **Amazon OpenSearch Serverless**: Hybrid search (keyword + semantic)
      - **Structured data**: Keep in Redshift/Glue, use text-to-SQL for queries
      
      **Metadata schema (always include):**
      - `source`: Who provided this knowledge
      - `last_validated`: When was it confirmed accurate
      - `confidence`: draft | validated | deprecated
      - `domain`: Business area / topic tags
      - `related_docs`: Links to related knowledge
      
      **PALETTE integration:**
      - Store rules in Assumptions Register format (RIU-008) with testable conditions
      - Document edge cases separately (RIU-014) for testing
      - Use RIU-044 for rule versioning and change tracking
      
      Key insight: Machine-readable ≠ machine-generated. Structure matters more than format — consistent schema with metadata enables retrieval, validation, and maintenance.

## Evidence

- **Tier 1 (entry-level)**: [Structured Data Retrieval Augmented Generation (RAG) - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/2_0_technical_foundations_and_patterns/2_3_core_archtectural_concepts/2_3_3_RAG(retrieval Augmented Generation)/2_3_3-6-Structured RAG/2_3_3-6-Structured RAG.html)
- **Tier 1 (entry-level)**: [Building cost-effective RAG applications with Amazon Bedrock Knowledge Bases and Amazon S3 Vectors](https://aws.amazon.com/blogs/machine-learning/building-cost-effective-rag-applications-with-amazon-bedrock-knowledge-bases-and-amazon-s3-vectors/)
- **Tier 1 (entry-level)**: [Choosing the right approach for generative AI-powered structured data retrieval](https://aws.amazon.com/blogs/machine-learning/choosing-the-right-approach-for-generative-ai-powered-structured-data-retrieval/)
- **Tier 1 (entry-level)**: [Unlock organizational wisdom using voice-driven knowledge capture](https://aws.amazon.com/blogs/machine-learning/unlock-organizational-wisdom-using-voice-driven-knowledge-capture-with-amazon-transcribe-and-amazon-bedrock/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-004](../rius/RIU-004.md)
- [RIU-008](../rius/RIU-008.md)
- [RIU-014](../rius/RIU-014.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-020.
Evidence tier: 1.
Journey stage: retrieval.
