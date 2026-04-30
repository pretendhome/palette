---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-062
source_hash: sha256:8405ebad786174f1
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [configuration, customization, knowledge-entry, multi-tenancy, scaling, specialization]
related: [RIU-120, RIU-121, RIU-520]
handled_by: [architect, builder, debugger]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the best pattern for handling customer-specific AI customizations at scale?

Customer customizations at scale require a layered configuration approach: shared platform → customer overrides → environment-specific settings. Don't fork code — parameterize everything.

## Definition

Customer customizations at scale require a layered configuration approach: shared platform → customer overrides → environment-specific settings. Don't fork code — parameterize everything.
      
      **The customization challenge:**
      ```
      1 customer:   Hand-crafted configuration
      10 customers: Copy-paste configurations, drift begins
      100 customers: Unmaintainable mess
      
      Solution: Configuration inheritance with overrides
      ```
      
      **Customization layer architecture:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │                    CONFIGURATION LAYERS                      │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  ┌───────────────────────────────────────────────────────┐ │
      │  │ LAYER 4: ENVIRONMENT OVERRIDES                        │ │
      │  │ (dev/staging/prod settings)                           │ │
      │  └───────────────────────────────────────────────────────┘ │
      │                          ▲                                  │
      │  ┌───────────────────────────────────────────────────────┐ │
      │  │ LAYER 3: CUSTOMER-SPECIFIC                            │ │
      │  │ (customer prompts, guardrails, KB, branding)          │ │
      │  └───────────────────────────────────────────────────────┘ │
      │                          ▲                                  │
      │  ┌───────────────────────────────────────────────────────┐ │
      │  │ LAYER 2: INDUSTRY/VERTICAL DEFAULTS                   │ │
      │  │ (healthcare, finance, retail templates)               │ │
      │  └───────────────────────────────────────────────────────┘ │
      │                          ▲                                  │
      │  ┌───────────────────────────────────────────────────────┐ │
      │  │ LAYER 1: PLATFORM DEFAULTS                            │ │
      │  │ (base prompts, guardrails, models)                    │ │
      │  └───────────────────────────────────────────────────────┘ │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      
      Resolution: Layer 4 → Layer 3 → Layer 2 → Layer 1 (first defined wins)
      ```
      
      **What can be customized:**
      
      | Layer | What's Customized | Example | Stored In |
      |-------|-------------------|---------|-----------|
      | **Prompts** | System prompts, templates | "You are a {company} assistant..." | Prompt Registry |
      | **Guardrails** | Safety filters, blocked topics | Industry-specific compliance | Bedrock Guardrails |
      | **Knowledge Base** | Customer-specific content | Product docs, policies | Per-tenant S3/OpenSearch |
      | **Model Selection** | Model preferences | Claude vs. Nova | Config DB |
      | **Branding** | Tone, terminology | Company voice guide | Config DB |
      | **Integrations** | External systems | CRM, ticketing connections | Secrets Manager |
      | **Thresholds** | Confidence, escalation | When to involve humans | Config DB |
      
      **Configuration storage pattern:**
      
      ```yaml
      customer_configuration:
        # Stored in DynamoDB / Parameter Store
        customer_id: "acme-corp"
        
        # Inheritance
        inherits_from: "healthcare"  # Industry template
        
        # Prompt customizations
        prompts:
          system_prompt_override: |
            You are ACME Corp's healthcare assistant. 
            Always recommend consulting a physician for medical advice.
            Use these approved product names: {product_list}
          
          greeting_override: "Welcome to ACME Health Support!"
          
        # Guardrail customizations
        guardrails:
          guardrail_id: "acme-healthcare-guardrail"
          blocked_topics:
            - "competitor products"
            - "off-label drug use"
          required_disclaimers:
            - "This is not medical advice"
            
        # Knowledge base
        knowledge_base:
          kb_id: "acme-kb-prod"
          s3_prefix: "s3://kb-bucket/acme-corp/"
          
        # Model preferences
        model:
          primary: "anthropic.claude-3-sonnet"
          fallback: "amazon.nova-pro"
          
        # Thresholds
        thresholds:
          confidence_for_auto_response: 0.85
          escalation_after_turns: 5
          
        # Feature flags
        features:
          enable_product_recommendations: true
          enable_appointment_scheduling: false
      ```
      
      **Runtime configuration resolution:**
      
      ```python
      def get_config(customer_id: str, key: str) -> Any:
          """
          Resolve configuration with inheritance.
          Customer → Industry → Platform defaults
          """
          # Layer 3: Customer-specific
          customer_config = config_store.get(f"customer/{customer_id}")
          if key in customer_config:
              return customer_config[key]
          
          # Layer 2: Industry defaults
          industry = customer_config.get("inherits_from")
          if industry:
              industry_config = config_store.get(f"industry/{industry}")
              if key in industry_config:
                  return industry_config[key]
          
          # Layer 1: Platform defaults
          platform_config = config_store.get("platform/defaults")
          return platform_config.get(key)
      
      # Usage
      system_prompt = get_config("acme-corp", "prompts.system_prompt")
      guardrail_id = get_config("acme-corp", "guardrails.guardrail_id")
      ```
      
      **Multi-tenant isolation patterns:**
      
      | Pattern | Customization Isolation | Resource Efficiency | Use When |
      |---------|------------------------|---------------------|----------|
      | **Siloed** | Separate infrastructure per customer | Low | Regulated, enterprise |
      | **Pooled** | Shared infra, config-based customization | High | Standard customers |
      | **Hybrid** | Shared compute, isolated data/KB | Medium | Most common |
      
      ```yaml
      hybrid_pattern:
        shared:
          - "Model endpoints (Bedrock)"
          - "Inference compute"
          - "Deployment pipeline"
          - "Monitoring infrastructure"
          
        per_customer:
          - "Configuration (DynamoDB)"
          - "Knowledge base content (S3)"
          - "Conversation history"
          - "Guardrail rules"
          - "Usage tracking (inference profiles)"
      ```
      
      **Deploying customizations:**
      
      ```yaml
      customization_deployment:
        # Separate from application deployment
        pipeline:
          trigger: "Config change in repo"
          
          stages:
            - name: "Validate"
              actions:
                - "Schema validation"
                - "Prompt syntax check"
                - "Guardrail compatibility"
                
            - name: "Test"
              actions:
                - "Run against customer's golden set"
                - "Verify guardrails activate appropriately"
                - "Check for regressions"
                
            - name: "Deploy"
              actions:
                - "Update config store (DynamoDB)"
                - "Invalidate caches"
                - "Update guardrail if changed"
                
            - name: "Verify"
              actions:
                - "Smoke test with customer context"
                - "Monitor for errors"
      ```
      
      **Testing customizations at scale:**
      
      ```yaml
      customization_testing:
        per_customer_tests:
          - "Golden set specific to customer"
          - "Brand voice validation"
          - "Guardrail effectiveness"
          - "Integration connectivity"
          
        cross_customer_tests:
          - "Platform regression suite"
          - "Performance benchmarks"
          - "Cost projections"
          
        automation:
          - "Run customer tests on config change"
          - "Weekly full regression across all customers"
          - "A/B testing infrastructure for prompt experiments"
      ```
      
      **Self-service customization portal:**
      
      ```yaml
      self_service_capabilities:
        # What customers can customize themselves
        tier_1_self_service:
          - "Greeting and sign-off messages"
          - "Product/service list updates"
          - "FAQ content in knowledge base"
          - "Basic tone adjustments"
          
        tier_2_assisted:
          - "System prompt modifications"
          - "Custom guardrail rules"
          - "Integration configurations"
          
        tier_3_platform_team:
          - "Model selection changes"
          - "New capability enablement"
          - "Custom fine-tuning"
      ```
      
      **PALETTE integration:**
      - Document customization options in RIU-044 (Business Rules Documentation)
      - Store templates in RIU-121 (Deployment Template)
      - Track per-customer configs in RIU-120 (Integration Mode Selection)
      - Version prompts per customer in RIU-520 (Prompt Version Control)
      
      Key insight: Every customer-specific code path is technical debt. Instead: one codebase, many configurations. The platform team maintains the engine; customers configure the behavior.

## Evidence

- **Tier 1 (entry-level)**: [Building multi-tenant architectures for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-multitenant/introduction.html)
- **Tier 1 (entry-level)**: [Building generative AI applications - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_9_AIOps/aiops_applicationbuilding.html)
- **Tier 1 (entry-level)**: [Tailored support at scale: Turning a unified Salesforce KB into LOB-focused AI agents](https://aws.amazon.com/blogs/contact-center/tailored-support-at-scale-turning-a-unified-salesforce-kb-into-lob-focused-ai-agents/)
- **Tier 1 (entry-level)**: [Advanced fine-tuning techniques for multi-agent orchestration: Patterns from Amazon at scale](https://aws.amazon.com/blogs/machine-learning/advanced-fine-tuning-techniques-for-multi-agent-orchestration-patterns-from-amazon-at-scale/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-120](../rius/RIU-120.md)
- [RIU-121](../rius/RIU-121.md)
- [RIU-520](../rius/RIU-520.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-062.
Evidence tier: 1.
Journey stage: specialization.
