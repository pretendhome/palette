---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-042
source_hash: sha256:15bd91c1638f9358
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [data-lineage, knowledge-entry, mlops, reproducibility, specialization, version-control]
related: [RIU-021, RIU-083, RIU-520, RIU-532]
handled_by: [architect, builder, narrator, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I version control datasets and models together for reproducibility?

Reproducibility requires linking exact dataset versions to exact model versions. Version them together with shared lineage, not separately.

## Definition

Reproducibility requires linking exact dataset versions to exact model versions. Version them together with shared lineage, not separately.
      
      **The reproducibility equation:**
      ```
      Model v1.2.3 = Code v1.2.3 + Data v2024-06-15 + Config v1.2.3
      
      If any component changes without versioning → reproducibility broken
      ```
      
      **Version control strategy:**
      
      | Component | Tool | What to Track |
      |-----------|------|---------------|
      | Code | Git | Training scripts, prompts, configs |
      | Small datasets (<1GB) | Git LFS or DVC | CSVs, JSONs, evaluation sets |
      | Large datasets | LakeFS, S3 versioning, DVC | Training data, embeddings |
      | Models | SageMaker Model Registry | Model artifacts, hyperparameters |
      | Experiments | SageMaker Experiments | Metrics, parameters, lineage |
      
      **Dataset versioning patterns:**
      
      **Pattern 1: Immutable snapshots (recommended)**
      ```
      s3://data-bucket/datasets/
        ├── customers/
        │   ├── v2024-06-01/
        │   ├── v2024-06-15/  ← Training data for model v1.2.3
        │   └── v2024-07-01/
        └── orders/
            ├── v2024-06-01/
            └── v2024-06-15/
      ```
      - Never modify existing versions
      - Create new version for any change
      - Reference by version ID in training config
      
      **Pattern 2: Git-like branches with LakeFS**
      ```
      lakefs://repo/main/datasets/customers/
      lakefs://repo/experiment-123/datasets/customers/  ← Branch for experiment
      ```
      - Branch for experiments, merge when validated
      - Full Git semantics (commit, diff, merge)
      - Works with existing S3-compatible tools
      
      **Pattern 3: DVC + Git (code + data together)**
      ```bash
      # Track data with DVC, metadata in Git
      dvc add data/training.csv
      git add data/training.csv.dvc
      git commit -m "Training data v2024-06-15"
      
      # Reproduce exact experiment
      git checkout v1.2.3
      dvc checkout  # Pulls matching data version
      ```
      
      **Linking models to data (lineage):**
      
      ```yaml
      model_metadata:
        model_id: "order-risk-v1.2.3"
        model_artifact: "s3://models/order-risk/v1.2.3/"
        
        training_data:
          dataset: "customers"
          version: "v2024-06-15"
          s3_path: "s3://data-bucket/datasets/customers/v2024-06-15/"
          row_count: 1250000
          hash: "sha256:abc123..."
          
        evaluation_data:
          dataset: "eval-set-v3"
          version: "v2024-06-10"
          
        code:
          git_commit: "abc123def456"
          git_repo: "https://github.com/org/ml-pipeline"
          
        config:
          hyperparameters: {learning_rate: 0.001, epochs: 10}
          prompt_version: "v2.1"
      ```
      
      **AWS implementation with SageMaker:**
      ```python
      # Register model with lineage
      from sagemaker.model import Model
      from sagemaker.model_registry import ModelPackage
      
      model_package = ModelPackage(
          model_package_arn=model_arn,
          model_data=model_s3_uri,
          
          # Link to data version
          customer_metadata_properties={
              "training_data_version": "v2024-06-15",
              "training_data_s3": "s3://bucket/datasets/v2024-06-15/",
              "training_data_hash": "sha256:abc123...",
              "git_commit": "abc123def456"
          }
      )
      ```
      
      **For GenAI/RAG systems:**
      - Version source documents separately from embeddings
      - Track embedding model version (changing it invalidates all vectors)
      - Include chunk strategy and parameters in version metadata
      ```yaml
      rag_version:
        knowledge_base_id: "kb-v2024-06-15"
        source_documents: "s3://docs/v2024-06-01/"
        embedding_model: "amazon.titan-embed-text-v2"
        chunk_size: 512
        chunk_overlap: 50
        vector_store_snapshot: "opensearch-index-v2024-06-15"
      ```
      
      **Minimum viable versioning checklist:**
      - [ ] Dataset versions are immutable (never modified in place)
      - [ ] Model metadata includes exact dataset version used
      - [ ] Code commit hash recorded with each training run
      - [ ] Hyperparameters and configs versioned
      - [ ] Can reproduce any past model from stored artifacts
      
      **PALETTE integration:**
      - Track dataset versions in RIU-520 (Prompt/Data Version Control)
      - Register models in RIU-532 (Model Registry Integration)
      - Document lineage in RIU-083 (Evaluation Metric Selection)
      - Store evaluation sets in RIU-021 (Golden Set)
      
      Key insight: "Versioning" means nothing if you can't answer: "What exact data trained this exact model?" If you don't record that link, you can't reproduce or debug.

## Evidence

- **Tier 1 (entry-level)**: [Data Management - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_9_AIOps/aiops_datamanagement.html)
- **Tier 1 (entry-level)**: [Tracking and managing assets used in AI development with Amazon SageMaker AI](https://aws.amazon.com/blogs/machine-learning/tracking-and-managing-assets-used-in-ai-development-with-amazon-sagemaker-ai/)
- **Tier 1 (entry-level)**: [Track your ML experiments end to end with Data Version Control and Amazon SageMaker Experiments](https://aws.amazon.com/blogs/machine-learning/track-your-ml-experiments-end-to-end-with-data-version-control-and-amazon-sagemaker-experiments/)
- **Tier 1 (entry-level)**: [DVC: Versioning Data and Models](https://doc.dvc.org/use-cases/versioning-data-and-models)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-083](../rius/RIU-083.md)
- [RIU-520](../rius/RIU-520.md)
- [RIU-532](../rius/RIU-532.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-042.
Evidence tier: 1.
Journey stage: specialization.
