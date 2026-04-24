---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-019
source_hash: sha256:add424b21f7137d9
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, change-tracking, governance, knowledge-entry, rule-management, version-control]
related: [RIU-003, RIU-008, RIU-062, RIU-532]
handled_by: [architect, debugger, narrator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I version control business rules that change frequently?

Use a layered approach: store rules in versioned data stores, track changes with event streams, and integrate with CI/CD for governance.

## Definition

Use a layered approach: store rules in versioned data stores, track changes with event streams, and integrate with CI/CD for governance.
      
      **Versioning patterns (Amazon DynamoDB):**
      - **Time-based**: Use timestamp in sort key (`rule_id#2024-06-15T10:30:00Z`) — good for audit trails
      - **Number-based**: Use version prefix + atomic counter (`v#0001`, `v#0002`) — good for rollback
      - **Optimistic concurrency**: Include version number in writes, reject stale updates — prevents conflicts
      
      **Change tracking:**
      - Enable DynamoDB Streams to capture all rule changes
      - Lambda function processes stream → logs to audit table, triggers notifications
      - Decouples change detection from rule execution
      
      **Architecture pattern (Step Functions + DynamoDB):**
      1. API Gateway receives rule update request
      2. Step Functions orchestrates validation → approval → deployment
      3. DynamoDB stores rule versions with metadata (author, timestamp, approval status)
      4. Lambda handles audit logging and downstream notifications
      
      **For complex rules engines:**
      - Store rule definitions in Amazon S3 (JSON/YAML files) with S3 versioning enabled
      - Store rule configuration/weights in Amazon Aurora
      - Store execution results in DynamoDB
      - Enables non-technical users to update rules without IT involvement
      
      **CI/CD integration:**
      - Treat rules as code: store in Git repository
      - PR review for rule changes (especially ONE-WAY DOOR changes)
      - Automated testing of rule logic before deployment
      - API-driven deployment to production
      
      **PALETTE integration:**
      - Document rule changes in Decision Log (RIU-003) when they affect system behavior
      - Flag rule changes that are ONE-WAY DOORs (compliance rules, pricing logic)
      - Use RIU-044 (Business Rules Documentation) for rule catalog
      - Track rule assumptions in Assumptions Register (RIU-008)
      
      **Rollback strategy:**
      - Maintain N previous versions (recommend: at least 5)
      - Test rollback procedure before you need it
      - Include rollback in incident runbook (RIU-062)
      
      Key insight: Version the rule *definition* separately from the rule *execution state*. You need to know what rules were active at any point in time for audit and debugging.

## Evidence

- **Tier 1 (entry-level)**: [Implementing version control using Amazon DynamoDB](https://aws.amazon.com/blogs/database/implementing-version-control-using-amazon-dynamodb/)
- **Tier 1 (entry-level)**: [Using AWS Step Functions and Amazon DynamoDB for business rules orchestration](https://aws.amazon.com/blogs/compute/using-aws-step-functions-and-amazon-dynamodb-for-business-rules-orchestration/)
- **Tier 1 (entry-level)**: [Building an Agile Business Rules Engine on AWS](https://aws.amazon.com/blogs/apn/building-an-agile-business-rules-engine-on-aws/)
- **Tier 1 (entry-level)**: [Amazon QuickSight BIOps – Part 2: Version control using APIs](https://aws.amazon.com/blogs/business-intelligence/amazon-quicksight-biops-part-2-version-control-using-apis/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-008](../rius/RIU-008.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-532](../rius/RIU-532.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-019.
Evidence tier: 1.
Journey stage: all.
