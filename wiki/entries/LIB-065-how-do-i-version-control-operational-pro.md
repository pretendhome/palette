---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-065
source_hash: sha256:bfcea83d7f83bc83
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, change-management, governance, knowledge-entry, sops, version-control]
related: [RIU-004, RIU-060, RIU-069, RIU-121, RIU-520, RIU-532]
handled_by: [architect, builder, debugger, narrator, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I version control operational procedures for AI systems?

Treat operational procedures like code: version control, review, test, and deploy. Unversioned procedures lead to drift, confusion, and incidents.

## Definition

Treat operational procedures like code: version control, review, test, and deploy. Unversioned procedures lead to drift, confusion, and incidents.
      
      **What to version control:**
      
      | Artifact Type | Example | Version Control Method |
      |---------------|---------|------------------------|
      | Runbooks | Incident response procedures | Git (markdown) |
      | SOPs | Daily operations guide | Git (markdown) |
      | Prompts | System prompts, templates | Git + Prompt Registry |
      | Configurations | Model settings, thresholds | Git (YAML/JSON) |
      | Infrastructure | IaC templates | Git (Terraform/CDK) |
      | Dashboards | CloudWatch configs | Git (JSON) |
      | Alerts | Alarm definitions | Git (YAML) |
      
      **Repository structure:**
      
      ```
      ai-operations/
      ├── README.md                    # Overview and quick links
      ├── CHANGELOG.md                 # Change history
      │
      ├── runbooks/
      │   ├── incident-response/
      │   │   ├── quality-degradation.md
      │   │   ├── model-failure.md
      │   │   └── rag-retrieval-issues.md
      │   ├── deployment/
      │   │   ├── standard-deployment.md
      │   │   ├── rollback-procedure.md
      │   │   └── emergency-hotfix.md
      │   └── maintenance/
      │       ├── knowledge-base-update.md
      │       └── model-version-upgrade.md
      │
      ├── sops/
      │   ├── daily-operations.md
      │   ├── on-call-handbook.md
      │   └── change-management.md
      │
      ├── prompts/
      │   ├── system-prompts/
      │   │   ├── v1.0.0/
      │   │   ├── v1.1.0/
      │   │   └── current -> v1.1.0
      │   └── templates/
      │
      ├── configurations/
      │   ├── guardrails/
      │   ├── thresholds/
      │   └── model-configs/
      │
      └── infrastructure/
          ├── terraform/
          └── cdk/
      ```
      
      **Version control workflow:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │              OPERATIONAL PROCEDURE LIFECYCLE                 │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐    │
      │  │ CREATE  │──▶│ REVIEW  │──▶│  TEST   │──▶│ PUBLISH │    │
      │  └─────────┘   └─────────┘   └─────────┘   └─────────┘    │
      │       │             │             │             │          │
      │   Branch      Pull Request   Validation    Merge to       │
      │   from main   + Approval     (if appl.)   main + tag      │
      │                                                            │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **Change management process:**
      
      ```yaml
      change_management:
        minor_changes:
          examples: ["Typo fixes", "Clarifications", "Contact updates"]
          process:
            - "Create branch"
            - "Make changes"
            - "Submit PR"
            - "1 reviewer approval"
            - "Merge"
          turnaround: "Same day"
          
        major_changes:
          examples: ["New procedures", "Process changes", "Threshold updates"]
          process:
            - "Create branch"
            - "Make changes"
            - "Submit PR with description of impact"
            - "2 reviewer approvals (including subject matter expert)"
            - "Test in staging (if applicable)"
            - "Merge + announce to team"
          turnaround: "1-3 days"
          
        critical_changes:
          examples: ["Security procedures", "Compliance updates", "Escalation paths"]
          process:
            - "Create branch"
            - "Make changes"
            - "Submit PR with impact assessment"
            - "Review by: Tech lead, Security, Compliance (as applicable)"
            - "Approval from AI Governance Lead"
            - "Staged rollout with communication plan"
          turnaround: "3-7 days"
      ```
      
      **Pull request template:**
      
      ```markdown
      ## Change Type
      - [ ] Minor (typo, clarification)
      - [ ] Major (new procedure, process change)
      - [ ] Critical (security, compliance, escalation)
      
      ## Description
      [What is being changed and why]
      
      ## Impact
      [Who is affected, what changes for them]
      
      ## Testing
      - [ ] Reviewed by someone who will use this procedure
      - [ ] Tested steps (if applicable)
      - [ ] Links updated and working
      
      ## Rollout
      - [ ] Team notified (Slack/email)
      - [ ] Training needed? [Yes/No]
      - [ ] CHANGELOG updated
      
      ## Reviewers
      - Technical: @[name]
      - SME: @[name] (if applicable)
      - Governance: @[name] (if critical)
      ```
      
      **CHANGELOG format:**
      
      ```markdown
      # Changelog
      
      ## [2024-06-15] - v1.2.0
      ### Added
      - New runbook: RAG retrieval troubleshooting (runbooks/incident-response/rag-retrieval-issues.md)
      - Emergency hotfix procedure (runbooks/deployment/emergency-hotfix.md)
      
      ### Changed
      - Updated escalation contacts in on-call-handbook.md
      - Revised quality degradation thresholds (lowered warning from 85% to 80%)
      
      ### Deprecated
      - Old deployment procedure (use standard-deployment.md instead)
      
      ## [2024-06-01] - v1.1.0
      ...
      ```
      
      **Linking procedures to deployments:**
      
      ```yaml
      deployment_metadata:
        deployment_id: "deploy-2024-06-15-001"
        git_commit: "abc123def456"
        
        procedures_version:
          runbooks: "v1.2.0"
          prompts: "v1.1.0"
          configurations: "v2.3.1"
          
        links:
          deployment_runbook: "runbooks/deployment/standard-deployment.md@v1.2.0"
          rollback_procedure: "runbooks/deployment/rollback-procedure.md@v1.2.0"
          incident_response: "runbooks/incident-response/@v1.2.0"
      ```
      
      **Automated validation (CI/CD):**
      
      ```yaml
      procedure_validation:
        on_pull_request:
          - check: "Markdown linting"
            tool: "markdownlint"
            
          - check: "Link validation"
            tool: "markdown-link-check"
            
          - check: "Required sections present"
            tool: "Custom script"
            sections: ["Purpose", "Prerequisites", "Steps", "Rollback", "Contacts"]
            
          - check: "CHANGELOG updated"
            tool: "Custom script"
            
        on_merge:
          - action: "Tag release"
          - action: "Update 'current' symlink"
          - action: "Notify team via Slack"
          - action: "Update documentation portal"
      ```
      
      **AWS Systems Manager integration:**
      
      ```yaml
      ssm_automation:
        # Convert markdown runbooks to executable automation
        pattern:
          - "Store runbooks in Git (source of truth)"
          - "Sync to SSM Documents for automation"
          - "Manual steps remain in markdown"
          - "Automated steps execute via SSM Runbooks"
          
        benefits:
          - "Executable procedures reduce human error"
          - "Audit trail of procedure execution"
          - "Approval gates in SSM"
      ```
      
      **PALETTE integration:**
      - Store procedures in RIU-069 (Runbook)
      - Version prompts in RIU-520 (Prompt Version Control)
      - Track configurations in RIU-532 (Model Registry)
      - Link from RIU-060 (Deployment Readiness)
      
      Key insight: The question isn't whether to version control procedures — it's whether you can answer "what version of this runbook was in effect when this incident happened?" If not, you have a traceability gap.

## Evidence

- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [AI Ops Overview - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_9_AIOps/index.html)
- **Tier 1 (entry-level)**: [Achieving Operational Excellence using automated playbook and runbook](https://aws.amazon.com/blogs/mt/achieving-operational-excellence-using-automated-playbook-and-runbook/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-004](../rius/RIU-004.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-069](../rius/RIU-069.md)
- [RIU-121](../rius/RIU-121.md)
- [RIU-520](../rius/RIU-520.md)
- [RIU-532](../rius/RIU-532.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-065.
Evidence tier: 1.
Journey stage: all.
