# OpenClaw Research Notes (for MissionCanvas Integration)

Date: 2026-02-17
Purpose: Capture external references used to harden OpenClaw integration choices.

## Primary Sources

1. OpenClaw official docs
- https://docs.openclaw.ai/
- Signals used: gateway model IDs, OpenAI-compatible API direction, plugin/runtime architecture, auth/security sections.

2. OpenClaw GitHub repository
- https://github.com/openclaw/openclaw
- Signals used: implementation examples, deployment patterns, current ecosystem activity.

## Secondary Signals (Ecosystem)

3. OpenClaw on YouTube (implementation walkthroughs)
- https://www.youtube.com/results?search_query=OpenClaw
- Used as ecosystem signal only; technical behavior validated against primary docs/repo.

4. Aggregated transcript references for rapid skimming
- https://www.listennotes.com/search/?q=OpenClaw
- Not treated as authoritative implementation spec.

## Design Decisions Informed by Research

1. Support multiple upstream API modes in adapter (`missioncanvas`, `responses`, `chatcompletions`) rather than a single custom endpoint.
2. Keep strict one-way-door gating in frontend and adapter responses.
3. Provide fallback local routing to maintain continuity when upstream unavailable.
4. Add direct terminal voice bridge so microphone access is possible outside browser.

## Validation Rule

When docs and ecosystem examples diverge:
- prefer official docs/repo behavior,
- keep adapter mode-configurable,
- fail safe to local fallback with explicit source tagging.
