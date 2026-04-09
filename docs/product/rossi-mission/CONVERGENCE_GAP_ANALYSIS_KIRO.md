# Convergence Gap Analysis: rossi_bridge.py vs missioncanvas-site

**Author**: kiro.design
**Date**: 2026-03-28
**Task**: RIU-001 — Compare convergence patterns between Telegram bridge and Mission Canvas
**Status**: COMPLETE

---

## Summary

The Telegram bridge (rossi_bridge.py) has 6 convergence patterns that make it work for Rossi. Mission Canvas (missioncanvas-site/) preserves 2 of them, partially implements 2, and is missing 2 entirely. The missing patterns are the ones that matter most for small business users.

---

## Pattern 1: Multi-Turn Conversation State

**Bridge**: ChatState class holds message history per chat_id. Up to 20 messages. Every user message and assistant response is appended. The full history is sent to Claude on every turn, giving the AI complete context of the conversation.

**Canvas**: Stateless. Each POST to /v1/missioncanvas/route is independent. No session memory. The "followup" feature in app.js just concatenates text into the input field and re-routes — it doesn't maintain conversation history.

**Gap**: CRITICAL. A small business owner says "I need a business plan" → gets RIU-109. Then says "actually focus on the grants part" → Canvas treats this as a brand new request with no memory of the business plan context. The bridge would remember the entire conversation.

**Fix**: Add session store (Map keyed by session_id). Accumulate input history. Pass history to routing context. The API contract already has session_id in the request schema — it's just not used.

---

## Pattern 2: Domain-Specific System Prompt

**Bridge**: 160-line ROSSI_SYSTEM prompt with deep domain knowledge — Rossi's address, business model, fundability score, 5 critical gaps, 3 critical fixes, revenue targets, grant strategy, artist pipeline thesis. Plus actor_mode instructions (sahar vs eiad) that change the AI's personality per user.

**Canvas**: No system prompt. The local router does keyword matching and returns structured data. There's no AI conversation — just routing + action brief generation.

**Gap**: HIGH. The bridge doesn't just route — it has a conversation with domain expertise. When Rossi asks "how are we doing on grants?", the bridge knows the specific grant targets, timelines, and amounts. Canvas would route to a generic RIU and return a template.

**Fix**: This is architectural. Canvas needs either (a) a per-client system prompt that gets loaded when signals identify the client, or (b) integration with a live LLM that receives the routing context + KL entries + client data. This is closer to Gap 2 (live agent routing) than a simple fix.

---

## Pattern 3: Structured Commands

**Bridge**: 7 slash commands (/status, /gaps, /fixes, /decisions, /revenue, /grants, /help) that return pre-built domain-specific responses. These bypass the AI entirely — they're direct lookups into the business plan data.

**Canvas**: No equivalent. Everything goes through the route endpoint. No way to say "show me my status" and get an instant structured response.

**Gap**: MEDIUM. Commands are a trust-building mechanism. They give instant, reliable answers. The AI conversation is for open-ended questions. Having both is what makes the bridge feel responsive.

**Fix**: Add a /v1/missioncanvas/command endpoint that maps known commands to pre-built responses. Or detect command patterns in the input and short-circuit routing.

---

## Pattern 4: Relay Tracing

**Bridge**: Full relay tracing via TelegramRelayStore — every conversation gets a trace_id, events are logged to JSONL files, requests/responses are written to the relay store with session summaries. This creates a complete audit trail.

**Canvas**: Decision log append exists (POST /v1/missioncanvas/log-append) but it's manual — user clicks a button. No automatic tracing. No session summaries.

**Gap**: MEDIUM. The bridge creates an automatic paper trail. Canvas requires the user to explicitly log decisions. Small business owners won't click "append to decision log."

**Fix**: Auto-append to decision log on every route response. The log-append endpoint exists — just call it automatically from the route handler instead of requiring a button click.

---

## Pattern 5: Convergence Completeness Check

**Bridge**: Implicit — the system prompt instructs the AI to ask clarifying questions when context is insufficient. The multi-turn history means the AI can build understanding over several exchanges.

**Canvas**: Explicit — the router checks for missing fields (objective, desired_outcome, context) and returns status: needs_convergence with missing_fields listed. But there's no mechanism to iteratively fill those fields through conversation.

**Gap**: PARTIAL. Canvas detects incompleteness but can't help resolve it. The bridge resolves it through conversation. Canvas just says "you're missing context" and waits for the user to figure it out.

**Fix**: When status is needs_convergence, return suggested questions for each missing field. The UI can display these as prompts. This doesn't require multi-turn — just better guidance on the single-turn response.

---

## Pattern 6: Actor Modes / Personalization

**Bridge**: Two actor modes (sahar, eiad) that change the AI's communication style per user. Sahar gets business-focused guidance. Eiad gets technical/operational guidance. Switchable via /mode command.

**Canvas**: No personalization. Every user gets the same routing and response format.

**Gap**: LOW for v1, but important for the "lens around them" vision the operator described. Different users need different communication styles.

**Fix**: The lens system already exists in Palette. Wire lens_id from the request into response formatting. The API contract supports it — lens_id is validated but not applied.

---

## Priority Matrix

| Pattern | Gap Severity | Fix Effort | Priority |
|---|---|---|---|
| Multi-turn state | CRITICAL | Medium | P0 |
| Domain system prompt | HIGH | Large (architectural) | P1 |
| Structured commands | MEDIUM | Small | P2 |
| Auto relay tracing | MEDIUM | Small | P2 |
| Convergence guidance | PARTIAL | Small | P3 |
| Actor modes / lenses | LOW | Medium | P4 |

---

## Recommendation

**P0 — Session state** is the single most important gap. Without it, Canvas is a single-shot tool, not a workspace. The API contract already has session_id. Wire it up.

**P2 items** (commands + auto-tracing) are quick wins that make Canvas feel more like the bridge without architectural changes.

**P1** (domain prompts) is the hard one — it's the difference between a router and an assistant. This is where Gap 2 (live agent routing) becomes essential.

---

**Deliverable**: This document + broadcast to team.
