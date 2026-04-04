---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-053
source_hash: sha256:43433aff6b4aa54a
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, chaos-engineering, failure-injection, knowledge-entry, production-testing, reliability]
related: [RIU-069, RIU-100, RIU-101, RIU-540]
handled_by: [architect, builder, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I test failure scenarios that only happen in production?

Production-only failures (scale, timing, real data patterns) require controlled chaos engineering. Use fault injection to create failures safely, shadow testing to observe without impact, and traffic replay to reproduce issues.

## Definition

Production-only failures (scale, timing, real data patterns) require controlled chaos engineering. Use fault injection to create failures safely, shadow testing to observe without impact, and traffic replay to reproduce issues.
      
      **Why some failures only happen in production:**
      - Scale effects (concurrency, rate limits, resource exhaustion)
      - Real data patterns (edge cases not in test data)
      - Timing issues (race conditions, timeouts under load)
      - Integration failures (third-party services, network)
      - User behavior (unexpected inputs, usage patterns)
      
      **Testing strategy pyramid:**
      ```
                    ┌─────────────────────────────────────┐
                    │  PRODUCTION CHAOS                   │
                    │  (Fault injection in prod)          │
                    ├─────────────────────────────────────┤
                    │  SHADOW TESTING                     │
                    │  (Observe prod traffic, no impact)  │
                    ├─────────────────────────────────────┤
                    │  STAGING CHAOS                      │
                    │  (Fault injection in staging)       │
                    ├─────────────────────────────────────┤
                    │  LOAD TESTING                       │
                    │  (Production-like scale)            │
                    └─────────────────────────────────────┘
                    │  INTEGRATION TESTING                │
                    │  (Component interactions)           │
                    └─────────────────────────────────────┘
      ```
      
      **Tool 1: AWS Fault Injection Simulator (FIS)**
      
      Inject controlled failures into AWS resources:
      ```yaml
      fis_experiment:
        name: "AI-Pipeline-Latency-Test"
        description: "Test AI pipeline resilience to model latency"
        
        targets:
          - name: "ai-inference-lambda"
            resource_type: "aws:lambda:function"
            selection_mode: "ALL"
            
        actions:
          - name: "inject-latency"
            action_id: "aws:lambda:function:invocation-add-delay"
            parameters:
              duration: "PT5M"  # 5 minutes
              delay_millis: "3000"  # 3 second delay
            targets: ["ai-inference-lambda"]
            
        stop_conditions:
          - source: "aws:cloudwatch:alarm"
            value: "arn:aws:cloudwatch:...:alarm:AI-Error-Rate-Critical"
            
        role_arn: "arn:aws:iam::...:role/FISRole"
      ```
      
      **AI-specific failure scenarios to test:**
      
      | Scenario | FIS Action | What You Learn |
      |----------|------------|----------------|
      | Model latency spike | Lambda delay injection | Timeout handling, fallbacks |
      | Model unavailable | Lambda invocation error | Circuit breaker activation |
      | Rate limiting | Throttle API calls | Queue behavior, retry logic |
      | RAG retrieval failure | Network disruption | Fallback to non-RAG response |
      | Vector DB latency | EBS I/O pause | Timeout configuration |
      | Memory pressure | Resource constraints | Graceful degradation |
      | Region failover | AZ/region disruption | Cross-region resilience |
      
      **Tool 2: Shadow Testing (SageMaker)**
      
      Compare new model against production without user impact:
      ```yaml
      shadow_test:
        production_variant: "model-v1.2.3"
        shadow_variant: "model-v1.3.0"
        traffic_to_shadow: "100%"  # All traffic mirrored
        duration: "7 days"
        
        comparison_metrics:
          - latency_p99
          - error_rate
          - output_quality_score
          
        promotion_criteria:
          - "shadow.latency_p99 <= production.latency_p99 * 1.1"
          - "shadow.error_rate <= production.error_rate"
          - "shadow.quality_score >= production.quality_score * 0.95"
      ```
      
      **Tool 3: Traffic Replay**
      
      Reproduce production issues in staging:
      ```yaml
      traffic_replay:
        source: "s3://logs/api-requests/2024-06-15/"
        target: "staging-endpoint"
        
        filters:
          - "status_code >= 500"  # Replay only errors
          - "latency > 5000"      # Replay slow requests
          
        transformation:
          - anonymize_pii: true
          - sample_rate: 0.1  # 10% of matching requests
      ```
      
      **5-step chaos experiment process:**
      
      ```
      1. DEFINE STEADY STATE
         └─ "Error rate < 1%, latency p99 < 500ms, quality score > 85%"
         
      2. FORM HYPOTHESIS
         └─ "If model latency increases 3x, circuit breaker activates
             and fallback model serves requests within 1 minute"
             
      3. INJECT FAILURE
         └─ Run FIS experiment with Lambda delay injection
         
      4. OBSERVE BEHAVIOR
         └─ Monitor dashboards, verify hypothesis
         └─ Did circuit breaker open? Did fallback activate?
         
      5. IMPROVE & DOCUMENT
         └─ If hypothesis failed: fix the gap
         └─ If passed: document as validated resilience
      ```
      
      **Safe production chaos (guardrails):**
      
      ```yaml
      safety_guardrails:
        stop_conditions:
          - "Error rate > 5%"
          - "Customer complaints received"
          - "On-call manually stops experiment"
          
        blast_radius_limits:
          - "Affect max 10% of traffic"
          - "Duration max 15 minutes"
          - "Single AZ only (not region-wide)"
          
        timing:
          - "Run during low-traffic hours"
          - "Avoid during deployments"
          - "Have rollback ready"
          
        communication:
          - "Notify on-call before experiment"
          - "Post in #ops channel"
          - "Have incident commander available"
      ```
      
      **CI/CD integration (automate chaos):**
      
      ```yaml
      # CodePipeline with FIS
      pipeline:
        stages:
          - name: "Deploy"
            actions: [deploy_to_staging]
            
          - name: "ChaosTest"
            actions:
              - run_fis_experiment: "latency-test"
              - run_fis_experiment: "failure-test"
              - validate_recovery
              
          - name: "PromoteOrRollback"
            actions:
              - if_chaos_passed: promote_to_prod
              - else: rollback_and_alert
      ```
      
      **Reproducing production-only bugs:**
      
      | Bug Type | Reproduction Strategy |
      |----------|----------------------|
      | Scale issues | Load test with production traffic volume |
      | Edge case inputs | Replay production requests that caused errors |
      | Timing bugs | FIS delay injection at various points |
      | Integration failures | Mock third-party with FIS network disruption |
      | Data patterns | Shadow test with production data |
      
      **PALETTE integration:**
      - Document failure scenarios in RIU-101 (Failure Mode Catalog)
      - Track chaos experiments in RIU-540 (Evaluation Harness)
      - Update runbooks based on findings (RIU-069)
      - Log results in RIU-100 (Incident Log) as "proactive tests"
      
      Key insight: If you haven't tested a failure mode, you haven't proven resilience — you're just hoping. Chaos engineering converts unknown-unknowns into known-knowns before they become incidents.

## Evidence

- **Tier 1 (entry-level)**: [Verify the resilience of your workloads using Chaos Engineering](https://aws.amazon.com/blogs/architecture/verify-the-resilience-of-your-workloads-using-chaos-engineering/)
- **Tier 1 (entry-level)**: [Generative AI Resilience: Chaos Engineering with AWS Fault Injection Service Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/d56fd754-5e56-43c5-addc-d69ac130a099)
- **Tier 1 (entry-level)**: [Introducing AWS Fault Injection Service Actions to Inject Chaos in Lambda functions](https://aws.amazon.com/blogs/mt/introducing-aws-fault-injection-service-actions-to-inject-chaos-in-lambda-functions/)
- **Tier 1 (entry-level)**: [Minimize the production impact of ML model updates with Amazon SageMaker shadow testing](https://aws.amazon.com/blogs/machine-learning/minimize-the-production-impact-of-ml-model-updates-with-amazon-sagemaker-shadow-testing/)
- **Tier 1 (entry-level)**: [GitHub - awslabs/chaos-machine](https://github.com/awslabs/chaos-machine)
- **Tier 1 (entry-level)**: [Principles of Chaos Engineering](https://principlesofchaos.org/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-069](../rius/RIU-069.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-540](../rius/RIU-540.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-053.
Evidence tier: 1.
Journey stage: all.
