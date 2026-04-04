---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-177
source_hash: sha256:41ffe8cd984db869
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [classification, information-design, knowledge-architecture, knowledge-entry, taxonomy]
related: []
handled_by: []
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design a taxonomy that an AI system can use for consistent, accurate classification?

Define taxonomy nodes as problem-solution pairs, not abstract categories. Each node should answer: 'What problem does this solve?' and 'What is the execution approach?' Use mutually exclusive categories at each level — if an item could belong to two categories, the taxonomy is ambiguous. Add trigger signals to each node: specific phrases, keywords, or patterns that indicate this category applies. Test the taxonomy with real queries: give 50 real user questions to the classifier and measure precision and recall per node. A taxonomy with 80% accuracy on 20 nodes is better than one with 60% accuracy on 100 nodes. Version the taxonomy and track classification accuracy over time. When accuracy drops below threshold, the taxonomy needs revision, not the classifier.

## Definition

Define taxonomy nodes as problem-solution pairs, not abstract categories. Each node should answer: 'What problem does this solve?' and 'What is the execution approach?' Use mutually exclusive categories at each level — if an item could belong to two categories, the taxonomy is ambiguous. Add trigger signals to each node: specific phrases, keywords, or patterns that indicate this category applies. Test the taxonomy with real queries: give 50 real user questions to the classifier and measure precision and recall per node. A taxonomy with 80% accuracy on 20 nodes is better than one with 60% accuracy on 100 nodes. Version the taxonomy and track classification accuracy over time. When accuracy drops below threshold, the taxonomy needs revision, not the classifier.

## Evidence

- **Tier 1**: Palette Taxonomy v1.3 — 120 RIUs across 6 workstreams

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-177.
Evidence tier: 1.
