---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-162
source_hash: sha256:7e286e8270315043
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [error-handling, knowledge-entry, messaging-standards, specialization, support, ux]
related: [RIU-012, RIU-330]
handled_by: [architect, builder, narrator, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I define error messaging standards that reduce support burden and help users recover from failures?

RIU-330 defines error messaging in three tiers. Tier 1 — User-Facing Errors: every error message must answer three questions: (a) What happened? (b) Why? (c) What can the user do next? Bad example: "Error 500: Internal Server Error." Good example: "We could not process your request because the document format is not supported. Please upload a PDF, DOCX, or TXT file and try again." Structure: [What went wrong] + [Why it happened, if knowable] + [Specific action to resolve]. Use active voice. Avoid technical jargon. Never blame the user. Tier 2 — Developer/Operator Errors: include technical detail for debugging. Structure: error code (machine-parseable, e.g., ERR_DOC_FORMAT_UNSUPPORTED), error message (human-readable), request_id (for log correlation), timestamp, and suggested fix. Return in structured format (JSON) with consistent schema across all API endpoints. Tier 3 — Internal Logging: log full context including stack trace, input parameters (redacted per RIU-012), system state, and correlation IDs. Never expose Tier 3 information in Tier 1 or Tier 2 responses — stack traces and internal paths are security vulnerabilities. AI-Specific Considerations: (a) when an LLM call fails, distinguish between model errors (content filtered, context too long) and infrastructure errors (API timeout, rate limit); (b) when an agent tool call fails, include the tool name and a user-understandable description of what the tool was trying to do; (c) never expose raw model outputs in error messages — they may contain prompt fragments or system information. Measure error messaging effectiveness by tracking: support tickets per error type, self-resolution rate, and repeat error rate.

## Definition

RIU-330 defines error messaging in three tiers. Tier 1 — User-Facing Errors: every error message must answer three questions: (a) What happened? (b) Why? (c) What can the user do next? Bad example: "Error 500: Internal Server Error." Good example: "We could not process your request because the document format is not supported. Please upload a PDF, DOCX, or TXT file and try again." Structure: [What went wrong] + [Why it happened, if knowable] + [Specific action to resolve]. Use active voice. Avoid technical jargon. Never blame the user. Tier 2 — Developer/Operator Errors: include technical detail for debugging. Structure: error code (machine-parseable, e.g., ERR_DOC_FORMAT_UNSUPPORTED), error message (human-readable), request_id (for log correlation), timestamp, and suggested fix. Return in structured format (JSON) with consistent schema across all API endpoints. Tier 3 — Internal Logging: log full context including stack trace, input parameters (redacted per RIU-012), system state, and correlation IDs. Never expose Tier 3 information in Tier 1 or Tier 2 responses — stack traces and internal paths are security vulnerabilities. AI-Specific Considerations: (a) when an LLM call fails, distinguish between model errors (content filtered, context too long) and infrastructure errors (API timeout, rate limit); (b) when an agent tool call fails, include the tool name and a user-understandable description of what the tool was trying to do; (c) never expose raw model outputs in error messages — they may contain prompt fragments or system information. Measure error messaging effectiveness by tracking: support tickets per error type, self-resolution rate, and repeat error rate.

## Evidence

- **Tier 1 (entry-level)**: [Nielsen Norman Group: Error Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/)
- **Tier 1 (entry-level)**: [Google API Design Guide: Errors](https://cloud.google.com/apis/design/errors)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-012](../rius/RIU-012.md)
- [RIU-330](../rius/RIU-330.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-162.
Evidence tier: 1.
Journey stage: specialization.
