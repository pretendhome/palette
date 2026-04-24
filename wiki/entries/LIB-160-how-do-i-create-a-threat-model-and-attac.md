---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-160
source_hash: sha256:9891ce35654c4d71
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [ai-safety, all, attack-surface, knowledge-entry, security, stride, threat-model]
related: [RIU-029, RIU-250, RIU-326]
handled_by: [architect, builder, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I create a threat model and attack surface map for an AI system?

RIU-326 applies threat modeling specifically to AI systems using an extended STRIDE framework. Step 1 — Define Trust Boundaries: draw the system architecture and mark every trust boundary where data or control crosses between components owned by different parties or at different privilege levels. For AI systems, key trust boundaries include: user input to prompt, prompt to model API, model output to application logic, tool calls to external systems, and training data to model weights. Step 2 — AI-Specific Threats (extending STRIDE): Prompt Injection (Information Disclosure + Elevation of Privilege): attacker manipulates model behavior through crafted inputs. Mitigate with input sanitization, system prompt isolation, and output validation. Training Data Poisoning (Tampering): compromised training data causes model misbehavior. Mitigate with data provenance tracking and anomaly detection. Model Extraction (Information Disclosure): attacker reverse-engineers model through API queries. Mitigate with rate limiting and output perturbation. Supply Chain Attack (Tampering): compromised model weights or dependencies. Mitigate with checksum verification and dependency scanning. Step 3 — Risk Assessment: for each threat, score likelihood (1-5) and impact (1-5). Priority = likelihood x impact. Focus mitigations on threats with priority > 12. Step 4 — Mitigation Plan: for each high-priority threat, document the control, its implementation status, and the residual risk after mitigation. Present to security review (RIU-250).

## Definition

RIU-326 applies threat modeling specifically to AI systems using an extended STRIDE framework. Step 1 — Define Trust Boundaries: draw the system architecture and mark every trust boundary where data or control crosses between components owned by different parties or at different privilege levels. For AI systems, key trust boundaries include: user input to prompt, prompt to model API, model output to application logic, tool calls to external systems, and training data to model weights. Step 2 — AI-Specific Threats (extending STRIDE): Prompt Injection (Information Disclosure + Elevation of Privilege): attacker manipulates model behavior through crafted inputs. Mitigate with input sanitization, system prompt isolation, and output validation. Training Data Poisoning (Tampering): compromised training data causes model misbehavior. Mitigate with data provenance tracking and anomaly detection. Model Extraction (Information Disclosure): attacker reverse-engineers model through API queries. Mitigate with rate limiting and output perturbation. Supply Chain Attack (Tampering): compromised model weights or dependencies. Mitigate with checksum verification and dependency scanning. Step 3 — Risk Assessment: for each threat, score likelihood (1-5) and impact (1-5). Priority = likelihood x impact. Focus mitigations on threats with priority > 12. Step 4 — Mitigation Plan: for each high-priority threat, document the control, its implementation status, and the residual risk after mitigation. Present to security review (RIU-250).

## Evidence

- **Tier 1 (entry-level)**: [OWASP: LLM Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- **Tier 1 (entry-level)**: [Microsoft: AI Threat Modeling — Failure Modes in Machine Learning](https://learn.microsoft.com/en-us/security/engineering/failure-modes-in-machine-learning)
- **Tier 1 (entry-level)**: [NIST AI 100-2: Adversarial Machine Learning — Taxonomy and Terminology](https://csrc.nist.gov/pubs/ai/100/2/e2023/final)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-029](../rius/RIU-029.md)
- [RIU-250](../rius/RIU-250.md)
- [RIU-326](../rius/RIU-326.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-160.
Evidence tier: 1.
Journey stage: all.
