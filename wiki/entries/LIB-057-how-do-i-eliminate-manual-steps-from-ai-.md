---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-057
source_hash: sha256:9f5215c3e72c9078
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, automation, ci-cd, deployment, efficiency, knowledge-entry]
related: [RIU-060, RIU-120, RIU-121, RIU-122, RIU-520]
handled_by: [architect, builder, debugger]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I eliminate manual steps from AI deployment pipelines?

Manual steps are deployment bottlenecks and error sources. Automate in priority order: triggers, testing, deployment, rollback. Keep human approval only for ONE-WAY DOORs.

## Definition

Manual steps are deployment bottlenecks and error sources. Automate in priority order: triggers, testing, deployment, rollback. Keep human approval only for ONE-WAY DOORs.
      
      **Manual steps to automate (priority order):**
      
      | Priority | Manual Step | Automation Approach | AWS Service |
      |----------|-------------|---------------------|-------------|
      | 1 | Triggering deployments | Git commit/merge triggers | CodePipeline |
      | 2 | Running tests | Automated test suites | CodeBuild |
      | 3 | Evaluation scoring | Automated eval pipeline | Bedrock Evaluations |
      | 4 | Building artifacts | Container/Lambda packaging | CodeBuild |
      | 5 | Deploying to staging | IaC deployment | CloudFormation/CDK |
      | 6 | Promoting to production | Automated gates with criteria | CodePipeline |
      | 7 | Rollback on failure | Automatic rollback triggers | CodeDeploy |
      | 8 | Post-deploy validation | Smoke tests + monitoring | Lambda + CloudWatch |
      
      **Fully automated GenAI pipeline:**
      
      ```
      ┌─────────────────────────────────────────────────────────────────┐
      │                    AUTOMATED CI/CD PIPELINE                      │
      ├─────────────────────────────────────────────────────────────────┤
      │                                                                 │
      │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
      │  │ TRIGGER │──▶│  BUILD  │──▶│  TEST   │──▶│  EVAL   │        │
      │  └─────────┘   └─────────┘   └─────────┘   └─────────┘        │
      │       │             │             │             │              │
      │   Git push     Container      Unit tests   Golden set         │
      │   Prompt reg   Lambda pkg     Integration  LLM-as-judge       │
      │   Schedule     Config         Contract     Quality score      │
      │                                                                │
      │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
      │  │ STAGING │──▶│ APPROVE │──▶│  PROD   │──▶│ VERIFY  │        │
      │  └─────────┘   └─────────┘   └─────────┘   └─────────┘        │
      │       │             │             │             │              │
      │   Deploy IaC   Auto-gate     Canary/BG    Smoke tests        │
      │   Shadow test  (criteria)    Traffic      Metrics check       │
      │   Load test    Manual (1WD)  shift        Auto-rollback      │
      │                                                                │
      └─────────────────────────────────────────────────────────────────┘
      ```
      
      **Automation by component:**
      
      **1. Trigger automation:**
      ```yaml
      triggers:
        code_change:
          source: "CodeCommit/GitHub"
          events: ["push to main", "PR merge"]
          action: "Start pipeline"
          
        prompt_change:
          source: "Prompt Registry (S3/DynamoDB)"
          events: ["New version published"]
          action: "Start evaluation + deploy pipeline"
          
        scheduled:
          source: "EventBridge"
          schedule: "Weekly model evaluation"
          action: "Run full evaluation suite"
          
        manual:
          source: "Console/CLI"
          use_case: "Emergency hotfix"
          action: "Start pipeline with expedited gates"
      ```
      
      **2. Evaluation automation:**
      ```yaml
      automated_evaluation:
        # Run automatically on every change
        stages:
          - name: "Unit tests"
            type: "Fast, deterministic"
            duration: "<5 min"
            gate: "100% pass"
            
          - name: "Golden set evaluation"
            type: "Quality scoring"
            tool: "Bedrock Evaluations / FMEval"
            metrics: ["accuracy", "relevance", "safety"]
            gate: "Score >= baseline - 5%"
            
          - name: "LLM-as-judge"
            type: "Quality assessment"
            tool: "Amazon Nova as evaluator"
            gate: "Score >= 4.0/5.0"
            
          - name: "Cost estimation"
            type: "Token usage projection"
            gate: "Cost increase < 20%"
      ```
      
      **3. Deployment automation:**
      ```yaml
      deployment_automation:
        staging:
          trigger: "All tests pass"
          method: "CloudFormation/CDK"
          validation: "Automated smoke tests"
          duration: "~10 minutes"
          
        production:
          trigger: "Staging validation pass + approval gate"
          method: "Canary deployment"
          phases:
            - traffic: "10%"
              duration: "15 min"
              validation: "Error rate < 1%, latency < baseline"
              
            - traffic: "50%"
              duration: "30 min"
              validation: "Quality score stable"
              
            - traffic: "100%"
              duration: "Complete"
              validation: "All metrics nominal"
      ```
      
      **4. Automated rollback:**
      ```yaml
      auto_rollback:
        triggers:
          - condition: "Error rate > 5%"
            window: "5 minutes"
            action: "Immediate rollback"
            
          - condition: "Latency p99 > 3x baseline"
            window: "10 minutes"
            action: "Rollback + alert"
            
          - condition: "Quality score < 70%"
            window: "30 minutes"
            action: "Rollback + review queue"
            
        rollback_procedure:
          - "Shift traffic to previous version"
          - "Alert on-call"
          - "Preserve failed version for analysis"
          - "Log rollback reason"
      ```
      
      **What to keep manual (ONE-WAY DOORs):**
      
      | Change Type | Automation Level | Why |
      |-------------|------------------|-----|
      | Prompt tweaks | Fully automated | TWO-WAY DOOR, easy rollback |
      | Model version update | Auto-test, manual approve | Higher risk |
      | New capability | Auto-test, manual approve | Business decision |
      | Production data access | Manual approval required | Compliance |
      | Cost increase >50% | Manual approval required | Budget impact |
      | Breaking API change | Manual approval required | ONE-WAY DOOR |
      
      **CodePipeline example:**
      ```yaml
      # AWS CDK Pipeline with automated stages
      pipeline = CodePipeline(
          synth=ShellStep("Synth", commands=["npm ci", "npm run build"]),
          
          # Automated test stage
          pre_production_steps=[
              ShellStep("UnitTests", commands=["npm test"]),
              ShellStep("Evaluation", commands=["python run_eval.py"]),
          ],
          
          # Automated deployment to staging
          stages=[
              DeployStage(self, "Staging", env=staging_env),
          ],
          
          # Manual approval only for production
          post_production_steps=[
              ManualApprovalStep("ProductionApproval",
                  comment="Approve production deployment?"),
          ]
      )
      ```
      
      **Metrics for automation success:**
      - Deployment frequency: Target weekly → daily
      - Lead time (commit → production): Target <1 day
      - Change failure rate: Target <5%
      - MTTR: Target <1 hour
      - Manual steps per deployment: Target 0-1
      
      **PALETTE integration:**
      - Automate RIU-060 (Deployment Readiness) checks
      - Version prompts in RIU-520 (Prompt Version Control)
      - Track deployments in RIU-121 (Deployment Template)
      - Auto-populate RIU-122 (Deployment Registry)
      
      Key insight: Every manual step is a delay, an error opportunity, and a scaling bottleneck. Automate everything except decisions that require human judgment — and even those should have automated gates that only escalate when criteria aren't met.

## Evidence

- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Build an automated generative AI solution evaluation pipeline with Amazon Nova](https://aws.amazon.com/blogs/machine-learning/build-an-automated-generative-ai-solution-evaluation-pipeline-with-amazon-nova/)
- **Tier 1 (entry-level)**: [Automate the machine learning model approval process with Amazon SageMaker](https://aws.amazon.com/blogs/machine-learning/automate-the-machine-learning-model-approval-process-with-amazon-sagemaker-model-registry-and-amazon-sagemaker-pipelines/)
- **Tier 1 (entry-level)**: [How to add notifications and manual approval to an AWS CDK Pipeline](https://aws.amazon.com/blogs/devops/how-to-add-notifications-and-manual-approval-to-an-aws-cdk-pipeline/)
- **Tier 1 (entry-level)**: [Google Cloud: MLOps Continuous Delivery and Automation Pipelines](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-060](../rius/RIU-060.md)
- [RIU-120](../rius/RIU-120.md)
- [RIU-121](../rius/RIU-121.md)
- [RIU-122](../rius/RIU-122.md)
- [RIU-520](../rius/RIU-520.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-057.
Evidence tier: 1.
Journey stage: all.
