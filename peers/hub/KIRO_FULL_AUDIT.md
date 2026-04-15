# Voice Hub v2 — Full Audit Report

**Auditor**: kiro.design
**Date**: 2026-04-14T19:56 PDT
**Scope**: All hub files (2,662 lines across 5 files)
**Bus state**: 3 peers (codex, kiro, hub.voice) — gemini/claude/mistral dropped off
**Prior reviews**: KIRO_DESIGN_REVIEW.md, CODEX_ARCHITECTURE_REVIEW.md

---

## File Inventory

| File | Lines | Role | Last modified |
|------|-------|------|---------------|
| server.mjs | 857 | HTTP server, LLM routing, TTS proxy, bus bridge | Apr 15 02:56 |
| index.html | 863 | SPA frontend, STT, TTS playback, convergence UI | Apr 15 00:10 |
| style.css | 500 | Dark theme, responsive layout | Apr 15 00:16 |
| palette_retrieve.py | 103 | Taxonomy classification + knowledge retrieval | Apr 14 23:15 |
| watcher.mjs | 339 | File-drop bridge (outbox→bus, bus→inbox) | Apr 10 00:30 |

---

## What's Already Fixed (Kiro + Claude combined)

| Issue | Status | Who |
|-------|--------|-----|
| Claude subprocess timeout | ✅ Fixed — 30s killTimer | Kiro |
| Error feedback in chat UI | ✅ Fixed — showError() wired to 3 paths | Kiro |
| .gitignore for .env | ✅ Fixed | Kiro |
| `var eventType` scoping bug | ✅ Fixed — `let` at function scope | Kiro |
| Markdown in TTS output | ✅ Fixed — `stripMarkdownForTTS()` added | Claude |
| System prompt anti-markdown instruction | ✅ Fixed — "Do NOT use markdown" | Claude |
| Sentence boundary detection | ✅ Improved — `extractCompleteSentences()` with min-length guard | Claude |
| `scrollTop` in streaming update | ✅ Fixed — `requestAnimationFrame` wrapper | Claude |
| Agent card click for bus-only peers | ✅ Fixed — routes to `@name` prefix | Claude |

---

## Outstanding Issues — Prioritized for Sierra Demo

### P0: Fix before demo

**1. No AbortController on LLM fetch calls (5 providers)**
Codex flagged this as High (#3). Still unfixed. If Mistral/OpenAI/Perplexity/DashScope/Kiro stalls mid-stream, the connection hangs forever. The Claude subprocess has a timeout now, but the 5 fetch-based providers don't.

Fix: Add AbortController with 30s timeout to each fetch call in `callLLM()`. Better yet, extract the duplicated parser first (see P1 #1) and add the abort there once.

**2. Retrieval subprocess alias is misleading and has no enforced timeout**
`server.mjs:297` imports `spawn` but aliases it as `spawnSync`. This is confusing (Codex flagged it) and the `timeout: 5000` option on `spawn()` does NOT work like it does on `execFile()`. The retrieval subprocess can hang indefinitely, blocking first-token delivery.

Fix: Either switch to `execFile` (which respects `timeout`), or add an explicit `setTimeout` + `proc.kill()` like the Claude fix.

**3. Bus peer drift — only 3 of 6 agents registered**
Current bus: `codex.implementation`, `kiro.design`, `hub.voice`. Missing: `gemini.specialist`, `claude-code`/`claude.analysis`, `mistral-vibe.builder`. For the demo, all agents should be visible in the roster.

### P1: Fix soon (quality / maintainability)

**1. 5x duplicated streaming parser**
`server.mjs` has the identical SSE stream parser (getReader → decode → split lines → parse data → yield token) copy-pasted for mistral, openai, perplexity, dashscope, and kiro. That's ~120 lines of duplication. Extract to a shared `parseOpenAIStream()` generator.

**2. Dead function: `loadRimeKey()`**
`server.mjs:92` — `async function loadRimeKey() { await loadKeys(); }` is a backward-compat shim that nothing calls. `loadKeys()` is called directly at startup (line 848). Remove it.

**3. `send failed` still goes to console.error, not showError**
`index.html:591` — `if (!data.ok) console.error('Send failed:', data)` — this is the bus send success-but-rejected path. Should call `showError()` for consistency.

**4. No `/health` endpoint on the hub server**
Codex flagged this (#11). The bus has `/health`, but the hub server itself has no health check. For the demo, being able to `curl localhost:7890/health` and see provider status would be useful for debugging.

### P2: Post-demo improvements

**5. No conversation history**
Every LLM call is stateless — one system prompt + one user message. No sliding window. Fine for demo, but daily use needs at minimum last-N turns.

**6. Audio queue has no backpressure or cancellation**
If the user sends a new message while audio from the previous response is still playing, old audio keeps draining. Should clear the queue on new user input.

**7. TTS failures are completely silent**
No `tts_error` event, no log, no UI indication. A sentence just disappears from audio with no explanation.

**8. Base64 audio over SSE**
33% overhead. Fine for localhost demo. Not for production.

**9. CORS is `*`**
Acceptable for local single-user. Not for anything shared.

**10. Watcher.mjs uses `/peek` which may not exist on broker**
`watcher.mjs:218` calls `busPost('/peek', ...)` — need to verify the broker actually has this endpoint. If not, inbox delivery is silently broken.

---

## Architecture Assessment

### What's good
- Single-file frontend with no build step — perfect for demo velocity
- SSE bridge from bus polling is clean
- Palette retrieval injected into every prompt — the taxonomy is live
- Voice command grammar for convergence is genuinely novel
- `stripMarkdownForTTS()` is a smart addition
- Sentence-boundary streaming TTS is the right architecture for latency

### What's fragile
- 5 providers with no timeout = 5 ways to hang
- Retrieval on critical path before first token
- No structured logging anywhere — debugging in production will be blind
- Identity drift between bus registrations and frontend expectations

### What's missing for production (not for Sierra)
- Rate limiting
- Conversation memory
- Structured logging + metrics
- Health/readiness endpoints
- Per-provider circuit breakers

---

## Recommendation for Claude

If you're fixing things in real-time, here's the highest-leverage order:

1. **Extract the streaming parser** — one function, delete ~120 lines of duplication, and you only need to add AbortController in one place
2. **Add AbortController to the extracted parser** — 30s timeout, covers all 5 providers at once
3. **Fix the retrieval subprocess** — either `execFile` with timeout, or explicit kill timer
4. **Add `/health`** — 15 lines, huge debugging value during demo

Everything else can wait until after Sierra.

---

**Audit complete. Sending to claude.analysis via bus.**
