---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-157
source_hash: sha256:a1281d0ea3ed9d8d
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [authentication, authorization, knowledge-entry, oauth, orchestration, security, sso]
related: [RIU-010, RIU-322, RIU-327]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I integrate authentication and authorization (SSO/OAuth/SAML) into an AI application securely?

RIU-322 defines auth integration across four areas. Area 1 — Protocol Selection: choose based on your ecosystem. OAuth 2.0 + OIDC: best for modern web/mobile apps with API access. SAML 2.0: best for enterprise SSO with existing IdP (Okta, Azure AD, Ping). API Keys: acceptable only for server-to-server communication, never for user-facing auth. For AI systems specifically: the AI agent inherits the permissions of the authenticated user — it should never have broader access than the user it serves. Area 2 — Token Management: store tokens securely (encrypted at rest, never in localStorage for web apps). Implement token rotation: access tokens short-lived (15-60 minutes), refresh tokens longer (hours-days) with rotation on use. Handle token expiration gracefully — refresh before the request, not after a 401. For AI agents calling APIs on behalf of users, use delegated tokens (OAuth token exchange) rather than service account tokens. Area 3 — Session Management: define session lifetime, idle timeout, and concurrent session policy. For AI systems with long-running tasks: separate the user session (interactive, short timeout) from the task session (background, longer lifetime, narrower permissions). Area 4 — Security Checklist: CSRF protection on all state-changing endpoints, PKCE for public clients, token binding where supported, secure cookie flags (HttpOnly, Secure, SameSite), and CORS configuration. Common failure: weak token handling where tokens are logged, cached in plaintext, or shared across tenants.

## Definition

RIU-322 defines auth integration across four areas. Area 1 — Protocol Selection: choose based on your ecosystem. OAuth 2.0 + OIDC: best for modern web/mobile apps with API access. SAML 2.0: best for enterprise SSO with existing IdP (Okta, Azure AD, Ping). API Keys: acceptable only for server-to-server communication, never for user-facing auth. For AI systems specifically: the AI agent inherits the permissions of the authenticated user — it should never have broader access than the user it serves. Area 2 — Token Management: store tokens securely (encrypted at rest, never in localStorage for web apps). Implement token rotation: access tokens short-lived (15-60 minutes), refresh tokens longer (hours-days) with rotation on use. Handle token expiration gracefully — refresh before the request, not after a 401. For AI agents calling APIs on behalf of users, use delegated tokens (OAuth token exchange) rather than service account tokens. Area 3 — Session Management: define session lifetime, idle timeout, and concurrent session policy. For AI systems with long-running tasks: separate the user session (interactive, short timeout) from the task session (background, longer lifetime, narrower permissions). Area 4 — Security Checklist: CSRF protection on all state-changing endpoints, PKCE for public clients, token binding where supported, secure cookie flags (HttpOnly, Secure, SameSite), and CORS configuration. Common failure: weak token handling where tokens are logged, cached in plaintext, or shared across tenants.

## Evidence

- **Tier 1 (entry-level)**: [OAuth 2.0 Security Best Current Practice (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- **Tier 1 (entry-level)**: [OWASP: Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- **Tier 1 (entry-level)**: [AWS Cognito: User Pool Authentication Flow](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-authentication-flow.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-010](../rius/RIU-010.md)
- [RIU-322](../rius/RIU-322.md)
- [RIU-327](../rius/RIU-327.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-157.
Evidence tier: 1.
Journey stage: orchestration.
