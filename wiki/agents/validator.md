---
source_file: MANIFEST.yaml
source_id: validator
source_hash: sha256:7f9675e7d55ebc9f
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: agent
tags: [agent, validator]
related: [RIU-012, RIU-014, RIU-016, RIU-020, RIU-021, RIU-028, RIU-029, RIU-066, RIU-080, RIU-081, RIU-082, RIU-083, RIU-084, RIU-086, RIU-087, RIU-088, RIU-232, RIU-250, RIU-326, RIU-327]
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# Validator

plan/spec assessment, GO/NO-GO verdicts

## Handles

- [RIU-012: PII/Compliance Triage (Controls Plan)](../rius/RIU-012.md)
- [RIU-014: Data Sampling + Edge-Case Catalog](../rius/RIU-014.md)
- [RIU-016: API Contract Review + Versioning Plan](../rius/RIU-016.md)
- [RIU-020: Baseline Behavior Snapshot](../rius/RIU-020.md)
- [RIU-021: Golden Set + Offline Evaluation Harness](../rius/RIU-021.md)
- [RIU-028: Schema-Constrained Generation](../rius/RIU-028.md)
- [RIU-029: Tool-Calling Safety Envelope](../rius/RIU-029.md)
- [RIU-066: Secrets Handling + Rotation Expectations](../rius/RIU-066.md)
- [RIU-080: Contract Tests (Input/Output)](../rius/RIU-080.md)
- [RIU-081: End-to-End Smoke Tests (Critical Path)](../rius/RIU-081.md)
- [RIU-082: LLM Safety Guardrails (Content + Tool Use)](../rius/RIU-082.md)
- [RIU-083: Red Team Scenarios (Abuse + Failure)](../rius/RIU-083.md)
- [RIU-084: Data Quality Checks (Nulls, Duplicates, Ranges)](../rius/RIU-084.md)
- [RIU-086: Regression Suite (Golden + Metamorphic)](../rius/RIU-086.md)
- [RIU-087: Human Review Gate (One-Way Doors)](../rius/RIU-087.md)
- [RIU-088: Privacy Redaction Pipeline](../rius/RIU-088.md)
- [RIU-108: Agent Security & Access Control](../rius/RIU-108.md)
- [RIU-109: Business Plan Creation](../rius/RIU-109.md)
- [RIU-232: Deduplication System](../rius/RIU-232.md)
- [RIU-250: Security Review Packet](../rius/RIU-250.md)
- [RIU-322: Authentication/Authorization Integration](../rius/RIU-322.md)
- [RIU-326: Threat Model + Attack Surface Map](../rius/RIU-326.md)
- [RIU-327: AuthN/AuthZ Integration](../rius/RIU-327.md)
- [RIU-400: KB Content Audit (Coverage + Gaps)](../rius/RIU-400.md)
- [RIU-501: Image/Vision Processing Integration](../rius/RIU-501.md)
- [RIU-503: Cross-Modal Validation Pattern](../rius/RIU-503.md)
- [RIU-514: Agent Capability Boundary Enforcement](../rius/RIU-514.md)
- [RIU-522: Token Budget Management](../rius/RIU-522.md)
- [RIU-524: LLM Output Quality Monitoring](../rius/RIU-524.md)
- [RIU-530: AI System Risk Classification](../rius/RIU-530.md)
- [RIU-531: Algorithmic Bias Detection](../rius/RIU-531.md)
- [RIU-533: Fundamental Rights Impact Assessment (FRIA)](../rius/RIU-533.md)
- [RIU-534: AI Audit Trail Requirements](../rius/RIU-534.md)
- [RIU-540: Validation Gate Design](../rius/RIU-540.md)
- [RIU-541: Compliance Audit Preparation](../rius/RIU-541.md)
- [RIU-606: Brand Safety for AI-Generated Content](../rius/RIU-606.md)
- [RIU-607: Context Compaction for Long Engagements](../rius/RIU-607.md)
- [RIU-608: Workflow Definition for Multi-Agent Engagements](../rius/RIU-608.md)

## Protocol

- SDK module: `agents/validator/test_validator_v2.py`
- SDK module: `agents/validator/validator.py`
- SDK module: `agents/validator/validator_v2.py`
- Wire contract: HandoffPacket (7 fields) / HandoffResult (7 fields)

## Provenance

Agent: validator. Role: plan/spec assessment, GO/NO-GO verdicts.
