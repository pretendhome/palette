---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-049
source_hash: sha256:83bd31147e536c1b
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [architecture, cascading-failures, fault-isolation, knowledge-entry, orchestration, pipeline-reliability]
related: [RIU-063, RIU-069, RIU-100, RIU-101]
handled_by: [architect, builder, monitor, narrator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I handle cascading failures in multi-model AI pipelines?

Cascading failures occur when one component's failure propagates to dependent components. In multi-model pipelines, this is especially dangerous — Model A's timeout can exhaust Model B's connection pool, which crashes Model C. Design for isolation, not just redundancy.

## Definition

Cascading failures occur when one component's failure propagates to dependent components. In multi-model pipelines, this is especially dangerous — Model A's timeout can exhaust Model B's connection pool, which crashes Model C. Design for isolation, not just redundancy.
      
      **Cascade failure patterns in AI pipelines:**
      ```
      Model A fails (timeout)
           ↓
      Model B retries exhaustively (no backoff)
           ↓
      Model B exhausts connection pool / hits rate limit
           ↓
      Model C waiting on B times out
           ↓
      Entire pipeline fails
           ↓
      Users retry → amplifies load → system collapse
      ```
      
      **Defense-in-depth architecture:**
      ```
                    ┌─────────────────────────────────────────┐
                    │           LOAD SHEDDING                 │
                    │    (reject excess requests early)       │
                    └─────────────────────────────────────────┘
                                      ↓
                    ┌─────────────────────────────────────────┐
                    │           BULKHEADS                     │
                    │    (isolate resources per model)        │
                    └─────────────────────────────────────────┘
                                      ↓
      ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
      │   Model A    │    │   Model B    │    │   Model C    │
      │   + Circuit  │    │   + Circuit  │    │   + Circuit  │
      │   Breaker    │    │   Breaker    │    │   Breaker    │
      └──────────────┘    └──────────────┘    └──────────────┘
                                      ↓
                    ┌─────────────────────────────────────────┐
                    │        GRACEFUL DEGRADATION             │
                    │    (fallback when models fail)          │
                    └─────────────────────────────────────────┘
      ```
      
      **Pattern 1: Circuit Breakers (stop calling failing models)**
      
      ```yaml
      circuit_breaker_config:
        model_a:
          failure_threshold: 5        # Open after 5 failures
          success_threshold: 3        # Close after 3 successes
          timeout_seconds: 30         # Half-open test interval
          
          states:
            closed: "Normal operation, requests pass through"
            open: "Failures detected, requests fail fast (don't call model)"
            half_open: "Testing if model recovered"
      ```
      
      **AWS Implementation (Lambda + DynamoDB):**
      ```python
      # Lambda extension checks circuit status before calling model
      def check_circuit(model_name):
          status = dynamodb.get_item(Key={'model': model_name})
          if status['state'] == 'OPEN':
              if time.now() > status['retry_after']:
                  return 'HALF_OPEN'  # Try one request
              raise CircuitOpenError("Model unavailable")
          return 'CLOSED'
      
      def call_model_with_circuit_breaker(model_name, input):
          state = check_circuit(model_name)
          try:
              result = invoke_model(model_name, input)
              if state == 'HALF_OPEN':
                  record_success(model_name)  # Close circuit
              return result
          except Exception:
              record_failure(model_name)
              raise
      ```
      
      **Pattern 2: Bulkheads (isolate resources per model)**
      
      ```yaml
      bulkhead_config:
        model_a:
          max_concurrent_requests: 50
          connection_pool_size: 20
          queue_size: 100
          
        model_b:
          max_concurrent_requests: 30
          connection_pool_size: 15
          queue_size: 50
          
        # Model A exhausting resources won't affect Model B
      ```
      
      **AWS Implementation:**
      - Separate Lambda functions per model (isolated concurrency)
      - Separate SQS queues per pipeline stage
      - App Mesh for EKS workloads with per-model resource limits
      
      **Pattern 3: Timeouts (fail fast, don't wait forever)**
      
      ```yaml
      timeout_strategy:
        # Cascading timeouts: each stage shorter than previous
        api_gateway: 29s    # API Gateway max
        orchestrator: 25s   # Total pipeline budget
        model_a: 10s        # Individual model budgets
        model_b: 8s         # Leave headroom for retry
        model_c: 5s
        
        # If Model A times out at 10s, we still have 15s for fallback
      ```
      
      **Pattern 4: Load Shedding (reject excess early)**
      
      ```yaml
      load_shedding:
        triggers:
          - queue_depth > 1000
          - error_rate > 10%
          - latency_p99 > 5s
          
        actions:
          - reject_new_requests: true
          - return_code: 503
          - message: "System overloaded, retry in 30 seconds"
          - preserve_capacity_for: "in-flight requests"
      ```
      
      **Pattern 5: Graceful Degradation (fallback chain)**
      
      ```yaml
      degradation_strategy:
        model_a_failure:
          fallback_1: "Use smaller/faster model (reduced quality)"
          fallback_2: "Return cached response if fresh enough"
          fallback_3: "Route to human review"
          fallback_4: "Return error with retry guidance"
          
        rag_failure:
          fallback_1: "Answer without retrieval (warn user)"
          fallback_2: "Return 'I don't have enough context'"
          
        full_pipeline_failure:
          action: "Queue request for later processing"
          notify_user: "Your request is queued, ETA: 30 minutes"
      ```
      
      **Step Functions orchestration with resilience:**
      ```yaml
      # Step Functions state machine with circuit breakers
      States:
        CheckModelACircuit:
          Type: Choice
          Choices:
            - Variable: "$.circuitStatus"
              StringEquals: "OPEN"
              Next: ModelAFallback
          Default: InvokeModelA
          
        InvokeModelA:
          Type: Task
          Resource: "arn:aws:lambda:...:invoke-model-a"
          Retry:
            - ErrorEquals: ["TransientError"]
              IntervalSeconds: 2
              MaxAttempts: 3
              BackoffRate: 2
          Catch:
            - ErrorEquals: ["States.ALL"]
              Next: RecordModelAFailure
              
        RecordModelAFailure:
          Type: Task
          Resource: "arn:aws:lambda:...:update-circuit-breaker"
          Next: ModelAFallback
      ```
      
      **Testing cascading failure resilience:**
      - Use AWS Fault Injection Simulator to inject failures
      - Test each circuit breaker opens correctly
      - Verify bulkheads isolate failures
      - Confirm fallbacks activate appropriately
      - Load test to find actual breaking points
      
      **PALETTE integration:**
      - Document failure modes in RIU-101 (Failure Mode Catalog)
      - Define circuit breaker configs in RIU-063 (Performance Baselines)
      - Include fallback procedures in RIU-069 (Runbook)
      - Track cascade incidents in RIU-100 (Incident Log)
      
      Key insight: The goal isn't preventing all failures — it's containing blast radius. A well-designed pipeline degrades gracefully: one model failing shouldn't take down the whole system.

## Evidence

- **Tier 1 (entry-level)**: [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents/)
- **Tier 1 (entry-level)**: [Using the circuit-breaker pattern with AWS Lambda extensions and Amazon DynamoDB](https://aws.amazon.com/blogs/compute/using-the-circuit-breaker-pattern-with-aws-lambda-extensions-and-amazon-dynamodb/)
- **Tier 1 (entry-level)**: [Using the circuit breaker pattern with AWS Step Functions and Amazon DynamoDB](https://aws.amazon.com/blogs/compute/using-the-circuit-breaker-pattern-with-aws-step-functions-and-amazon-dynamodb/)
- **Tier 1 (entry-level)**: [Building a fault tolerant architecture with a Bulkhead Pattern on AWS App Mesh](https://aws.amazon.com/blogs/containers/building-a-fault-tolerant-architecture-with-a-bulkhead-pattern-on-aws-app-mesh/)
- **Tier 1 (entry-level)**: [Planning for failure: How to make generative AI workloads more resilient](https://aws.amazon.com/blogs/publicsector/planning-for-failure-how-to-make-generative-ai-workloads-more-resilient/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-063](../rius/RIU-063.md)
- [RIU-069](../rius/RIU-069.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Narrator](../agents/narrator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-049.
Evidence tier: 1.
Journey stage: orchestration.
