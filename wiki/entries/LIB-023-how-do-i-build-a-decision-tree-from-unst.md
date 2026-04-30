---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-023
source_hash: sha256:1dd0858f75f76b5a
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [decision-trees, interview-analysis, knowledge-entry, knowledge-extraction, modeling, retrieval]
related: [RIU-008, RIU-014, RIU-021]
handled_by: [architect, builder, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I build a decision tree from unstructured interview transcripts?

Use a 4-stage pipeline: Capture → Extract → Structure → Validate.

## Definition

Use a 4-stage pipeline: Capture → Extract → Structure → Validate.
      
      **Stage 1: Capture and transcribe**
      - Record SME interviews (voice capture reduces cognitive load)
      - Use Amazon Transcribe for speech-to-text conversion
      - Preserve speaker identification for multi-person interviews
      - Store raw transcripts in S3 for audit trail
      
      **Stage 2: Extract decision logic with LLM**
      Use structured prompts to identify decision points:
      ```
      Analyze this interview transcript and extract:
      1. All decision points where the expert chooses between options
      2. The conditions/factors they consider for each decision
      3. The outcomes/actions for each branch
      4. Any exceptions or edge cases mentioned
      
      Format as: IF [conditions] THEN [action] ELSE [alternative]
      Flag any "it depends" statements for follow-up.
      ```
      
      - Use Amazon Bedrock (Claude, Nova) for extraction
      - Multi-agent pipeline: one agent for classification, one for rule extraction, one for validation
      - Extract entities and relationships for knowledge graph (Neo4j + Bedrock)
      
      **Stage 3: Structure into decision tree**
      - Convert extracted IF/THEN statements into tree format:
      ```yaml
      decision_node:
        id: "escalation_decision"
        question: "Is customer tier enterprise?"
        conditions:
          - branch: "yes"
            next: "check_severity"
          - branch: "no"
            action: "standard_support"
        source: "transcript_001, timestamp 12:34"
      ```
      - Link nodes to form complete tree
      - Identify gaps where branches are undefined
      - Store in machine-readable format (YAML/JSON) per LIB-020
      
      **Stage 4: Validate with SME**
      - Walk through extracted tree with original expert
      - Present edge cases: "If X and Y, the tree says Z — is that correct?"
      - Probe gaps: "What happens when [undefined condition]?"
      - Update tree based on corrections
      - Document validation in Assumptions Register (RIU-008)
      
      **Quality checks:**
      - Every leaf node has an action (no dead ends)
      - Every condition has both true/false branches
      - Source attribution for each rule (traceability)
      - Edge cases cataloged separately (RIU-014)
      
      **PALETTE integration:**
      - Store validated decision trees in RIU-044 (Business Rules Documentation)
      - Track unvalidated branches as Assumptions (RIU-008)
      - Flag rules that are ONE-WAY DOORs (compliance, safety decisions)
      - Use extracted trees to build Golden Set for testing (RIU-021)
      
      Key insight: LLMs extract *candidate* decision logic; SMEs *validate* it. Never deploy an extracted tree without expert review — transcripts contain noise, tangents, and incomplete thoughts.

## Evidence

- **Tier 1 (entry-level)**: [Unearth insights from audio transcripts using Amazon Transcribe and Amazon Bedrock](https://aws.amazon.com/blogs/machine-learning/unearth-insights-from-audio-transcripts-generated-by-amazon-transcribe-using-amazon-bedrock/)
- **Tier 1 (entry-level)**: [Build a domain-aware data preprocessing pipeline: A multi-agent collaboration approach](https://aws.amazon.com/blogs/machine-learning/build-a-domain‐aware-data-preprocessing-pipeline-a-multi‐agent-collaboration-approach/)
- **Tier 1 (entry-level)**: [Leveraging Neo4j and Amazon Bedrock for knowledge graphs](https://aws.amazon.com/blogs/apn/leveraging-neo4j-and-amazon-bedrock-for-an-explainable-secure-and-connected-generative-ai-solution/)
- **Tier 1 (entry-level)**: [Extract data from documents using multimodal Generative AI models](https://builderspace.aws.dev/project/9123af96-986b-466c-952e-92aeaabdadf6)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-008](../rius/RIU-008.md)
- [RIU-014](../rius/RIU-014.md)
- [RIU-021](../rius/RIU-021.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-023.
Evidence tier: 1.
Journey stage: retrieval.
