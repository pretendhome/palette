---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-056
source_hash: sha256:977d73bca78b7aba
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, documentation, knowledge-entry, operations, process, sops]
related: [RIU-004, RIU-060, RIU-069, RIU-102, RIU-120, RIU-121]
handled_by: [architect, builder, debugger, narrator, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the minimum viable SOP for AI system operations?

A minimum viable SOP ensures anyone can operate the system without the original builders. Cover: daily operations, incident response, change management, and access control.

## Definition

A minimum viable SOP ensures anyone can operate the system without the original builders. Cover: daily operations, incident response, change management, and access control.
      
      **Minimum viable SOP structure:**
      
      ```yaml
      ai_operations_sop:
        metadata:
          system_name: "Customer Support AI Assistant"
          version: "1.0.0"
          owner: "AI Platform Team"
          last_updated: "2024-06-15"
          review_cadence: "Quarterly"
          
        # SECTION 1: SYSTEM OVERVIEW
        overview:
          description: "RAG-based AI assistant for customer support queries"
          architecture_diagram: "link/to/diagram"
          dependencies:
            - "Amazon Bedrock (Claude)"
            - "OpenSearch (vector store)"
            - "DynamoDB (conversation state)"
          contacts:
            primary_owner: "jane.smith@company.com"
            on_call_rotation: "#ai-oncall"
            escalation: "AI Governance Lead"
            
        # SECTION 2: DAILY OPERATIONS
        daily_operations:
          health_checks:
            - task: "Review dashboard for anomalies"
              frequency: "Start of shift"
              dashboard: "link/to/cloudwatch/dashboard"
              
            - task: "Check error rate and latency"
              threshold: "Error >1% or p99 >2s = investigate"
              
            - task: "Verify knowledge base sync status"
              check: "Last sync < 24 hours ago"
              
          routine_tasks:
            - task: "Review low-confidence outputs"
              frequency: "Daily"
              queue: "link/to/review/queue"
              
            - task: "Clear DLQ if items present"
              frequency: "Daily"
              procedure: "See DLQ handling section"
              
          monitoring:
            dashboards:
              - name: "AI Operations"
                url: "cloudwatch/dashboard/ai-ops"
              - name: "Quality Metrics"
                url: "cloudwatch/dashboard/ai-quality"
            alerts:
              - name: "Error Rate High"
                action: "Page on-call"
              - name: "Quality Score Low"
                action: "Review queue + investigate"
                
        # SECTION 3: INCIDENT RESPONSE
        incident_response:
          severity_levels:
            critical: "Customer-facing outage"
            high: "Significant quality degradation"
            medium: "Non-critical feature impacted"
            low: "Minor issue, workaround exists"
            
          response_procedures:
            critical:
              - "Acknowledge within 15 minutes"
              - "Engage incident commander"
              - "Consider rollback"
              - "Communicate to stakeholders"
              
            high:
              - "Acknowledge within 30 minutes"
              - "Begin investigation"
              - "Escalate if no progress in 1 hour"
              
          runbook_links:
            - "Quality Degradation: link/to/runbook"
            - "Model Failure: link/to/runbook"
            - "RAG Retrieval Issues: link/to/runbook"
            
          escalation:
            tier_1: "On-call engineer"
            tier_2: "AI Platform Lead"
            tier_3: "AI Governance Lead"
            executive: "VP Engineering"
            
        # SECTION 4: CHANGE MANAGEMENT
        change_management:
          change_types:
            prompt_update:
              approval: "ML Engineer + QA"
              testing: "Golden set evaluation"
              deployment: "Canary (10% for 1 hour)"
              rollback: "Automatic on error spike"
              
            model_update:
              approval: "ML Lead + AI Governance"
              testing: "Full evaluation suite + shadow test"
              deployment: "Blue-green with manual promotion"
              rollback: "Revert to previous endpoint"
              
            knowledge_base_update:
              approval: "Content owner + ML Engineer"
              testing: "Retrieval quality check"
              deployment: "Incremental re-index"
              rollback: "Restore from backup"
              
            infrastructure_change:
              approval: "Platform Lead + Security"
              testing: "Staging environment validation"
              deployment: "IaC through CI/CD"
              rollback: "Previous IaC version"
              
          deployment_gates:
            - gate: "Code review approved"
            - gate: "Automated tests passing"
            - gate: "Evaluation score >= baseline"
            - gate: "Security scan clean"
            - gate: "Manual approval (if required)"
            
        # SECTION 5: ACCESS MANAGEMENT
        access_management:
          access_levels:
            read_only: "View dashboards, logs"
            operator: "Execute runbooks, restart services"
            developer: "Deploy changes, modify configs"
            admin: "Full access including IAM changes"
            
          access_request:
            process: "Submit ticket to #access-requests"
            approval: "Team lead + system owner"
            review: "Quarterly access review"
            
          emergency_access:
            process: "Break-glass procedure"
            approval: "Post-hoc, must document within 24h"
            audit: "All emergency access logged and reviewed"
            
        # SECTION 6: BACKUP AND RECOVERY
        backup_recovery:
          what_is_backed_up:
            - component: "Knowledge base content"
              frequency: "Daily"
              retention: "30 days"
              location: "S3 with versioning"
              
            - component: "Conversation history"
              frequency: "Continuous (DynamoDB)"
              retention: "90 days"
              recovery: "Point-in-time recovery"
              
            - component: "Model artifacts"
              frequency: "On change"
              retention: "All versions"
              location: "S3 + Model Registry"
              
          recovery_procedures:
            knowledge_base: "link/to/kb/restore/procedure"
            conversation_state: "link/to/dynamodb/pitr/procedure"
            model_rollback: "link/to/model/rollback/procedure"
            
          rto_rpo:
            rto: "4 hours"
            rpo: "1 hour"
            
        # SECTION 7: KEY METRICS
        key_metrics:
          slos:
            availability: "99.9%"
            latency_p99: "2000ms"
            error_rate: "<0.1%"
            quality_score: ">85%"
            
          operational_metrics:
            mttr: "Target: <1 hour"
            change_failure_rate: "Target: <5%"
            deployment_frequency: "Target: Weekly"
      ```
      
      **"Minimum viable" criteria:**
      - [ ] New team member can operate system after reading SOP
      - [ ] All critical procedures have documented steps
      - [ ] Escalation paths are clear
      - [ ] Recovery procedures are tested
      - [ ] Change approval process is defined
      - [ ] Access management is documented
      
      **SOP maintenance:**
      - Review quarterly or after significant incidents
      - Update immediately when procedures change
      - Version control with change history
      - Validate with tabletop exercises
      
      **PALETTE integration:**
      - Store in RIU-069 (Runbook)
      - Link from RIU-060 (Deployment Readiness)
      - Reference in RIU-102 (Escalation Matrix)
      - Update based on RIU-100 (Incident Log) learnings
      
      Key insight: An SOP you don't update is an SOP that will fail you. Schedule quarterly reviews and update after every incident that revealed a gap.

## Evidence

- **Tier 1 (entry-level)**: [Introducing Strands Agent SOPs – Natural Language Workflows for AI Agents](https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/)
- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Operationalize generative AI workloads with Amazon Bedrock – Part 1: GenAIOps](https://aws.amazon.com/blogs/machine-learning/operationalize-generative-ai-workloads-and-scale-to-hundreds-of-use-cases-with-amazon-bedrock-part-1-genaiops/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-004](../rius/RIU-004.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-069](../rius/RIU-069.md)
- [RIU-102](../rius/RIU-102.md)
- [RIU-120](../rius/RIU-120.md)
- [RIU-121](../rius/RIU-121.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise
- [RIU-102](../paths/RIU-102-enablement-pack.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-056.
Evidence tier: 1.
Journey stage: all.
