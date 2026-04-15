# Codex Architecture Review: Voice Hub v2

Date: 2026-04-14

Reviewed files:

- `palette/peers/hub/server.mjs`
- `palette/peers/hub/index.html`
- `palette/peers/hub/palette_retrieve.py`
- `.env` handling via gitignore rules only

## Executive Summary

The architecture is workable for local testing, but it is still fragile in the exact places that matter for a voice interface: subprocess control, timeout behavior, queue growth, and stream lifecycle. The main production blockers are:

1. synchronous, per-request retrieval with a broken subprocess wrapper
2. no hard timeouts or cancellation for upstream LLM/TTS calls
3. no backpressure or queue limits for streamed audio
4. no rate limiting, health endpoint, or persistent conversation state

## Findings

### 1. High: Palette retrieval path is functionally unsafe and can stall the first token

Files:

- `server.mjs:294-322`
- `palette_retrieve.py:33-103`

The retrieval step runs before any LLM token is streamed, so the browser sees no response until retrieval completes or fails. That means retrieval latency is directly on the critical path for perceived responsiveness.

More importantly, the subprocess wrapper is incorrect. `server.mjs` imports `spawn` but aliases it as `spawnSync`, then treats the returned child like a synchronous result and also like an event emitter:

- `server.mjs:297-309`

`spawn()` does not support the `timeout` option the way `execFile` does, and it returns immediately. The code then listens to `stdout` and `close`, but never kills the child on timeout. If `uv run python3 ...` hangs or blocks on imports, the request can sit indefinitely before the first token. The `5s timeout` described in the prompt is not actually enforced here.

Impact:

- first-token latency can become unbounded
- browser appears hung waiting for `/api/chat`
- orphan retrieval subprocesses are possible under failure conditions

Recommendation:

- replace this with `execFile`/`spawn` plus an explicit timer and kill path
- decouple retrieval from first token by racing it against a short budget, for example 300-800 ms
- emit a non-fatal `palette_timeout` or `palette_unavailable` event when retrieval misses budget

### 2. High: Claude CLI subprocess has no timeout, no stderr handling, and no non-zero exit check

File:

- `server.mjs:573-592`

Claude is run through `claude -p ... --model ...` and the code simply yields stdout chunks until stdout ends, then waits for `close`.

Problems:

- no timeout or abort if the CLI hangs
- no stderr capture or structured error propagation
- no exit-code check after `close`
- `CLAUDE_TOKEN` is loaded in `loadKeys()` but never injected into the Claude subprocess environment, so this flow depends entirely on ambient CLI auth state rather than the loaded credential

If Claude hangs, `/api/chat` hangs. The browser’s `directChat()` loop in `index.html:595-704` waits forever because there is no client-side abort, timeout, or synthetic completion event.

Recommendation:

- wrap Claude CLI in explicit timeout plus `proc.kill()`
- capture stderr and include it in server-side logs
- fail closed on non-zero exit and emit an SSE `error` event
- decide whether this server should rely on Claude CLI ambient auth or a passed credential, then make that explicit

### 3. High: Upstream LLM fetches have no timeout or cancellation, so mid-stream stalls can pin connections indefinitely

Files:

- `server.mjs:334-404`
- `server.mjs:593-813`
- `index.html:595-704`

All non-Claude providers use `fetch(..., { stream: true })` with no `AbortController` and no idle timeout. If a provider accepts the request, starts streaming, and then stalls mid-stream, the server remains inside the `for await` loop and never sends `done` or `error` until the fetch fails at the TCP layer.

Current behavior:

- if the provider throws, the outer `catch` emits `event: error` and closes the stream (`server.mjs:405-412`)
- if the provider just stops making progress, neither side has a timeout
- client `directChat()` does not handle `event: error` at all (`index.html:647-699`), so even when the server sends an error event, the UI only logs if the whole fetch rejects

Impact:

- browser can look frozen mid-answer
- no “partial answer recovered” UI state
- hung sockets accumulate under upstream degradation

Recommendation:

- add per-provider request timeout and idle-stream timeout
- track last token timestamp and abort stalled streams
- handle `event: error` and `event: done` explicitly in the client
- show a visible partial-response/error state instead of silent console-only failure

### 4. Medium-High: TTS failures are isolated per sentence, but they are silent and can permanently desynchronize voice/text UX

Files:

- `server.mjs:349-372`
- `server.mjs:376-400`
- `index.html:619-637`
- `index.html:696-699`

The good part: one Rime failure does not kill the whole response. Each sentence TTS call is wrapped in its own `try/catch`, so text streaming continues.

The problem: all TTS failures are silent. No event is emitted to tell the browser that one sentence was skipped, and no server log is generated. That makes debugging impossible and leaves the user with partial audio and full text with no explanation.

Recommendation:

- keep the per-sentence isolation
- emit a lightweight `tts_error` SSE event with sentence index or excerpt
- log provider status and latency for each TTS chunk

### 5. Medium-High: Audio queue has no backpressure, no size bound, and no cancellation when users interrupt

Files:

- `index.html:421-458`
- `index.html:616-637`
- `index.html:696-699`

Both the general TTS queue and direct-chat audio queue drain sequentially. That preserves order, but there is no limit on queue length and no policy for interruption.

If sentences arrive faster than Rime can synthesize, or faster than the browser can play them:

- base64 audio events keep accumulating in memory
- playback can lag far behind text
- starting a new query does not clear stale queued audio from the previous answer

Recommendation:

- add bounded queue sizes
- drop, coalesce, or cancel old audio when a new user utterance starts
- consider separate text and audio pacing policies

### 6. Medium: Sentence splitting regex is too naive for spoken English and multilingual input

Files:

- `server.mjs:331-343`

The active splitter is:

- `/(?<=[.!?])\s+/`

This will incorrectly split on abbreviations and decimals, including the examples you called out:

- `Mr. Smith`
- `3.14`
- `U.S.A. policy`

The unused `SENTENCE_END` regex at `server.mjs:331` suggests the implementation changed midstream and the heuristic was never finished.

Impact:

- unnatural audio segmentation
- duplicate or premature TTS generation
- poor behavior in French/Italian/Spanish where punctuation and abbreviations differ

Recommendation:

- use a real sentence boundary detector or a guarded heuristic
- at minimum, suppress splits for common honorifics, initials, decimals, and acronym chains

### 7. Medium: Base64 audio over SSE is acceptable for local testing, but inefficient at scale

Files:

- `server.mjs:367-370`
- `server.mjs:395-398`
- `index.html:623-627`

Base64 adds roughly 33% payload overhead and forces extra copies:

- provider audio buffer
- base64 string
- JSON event payload
- browser decode back into bytes

For localhost demos this is fine. For longer responses or multiple concurrent users, it becomes expensive in memory, CPU, and wire size.

Recommendation:

- keep SSE audio for local prototyping
- for production, switch to one of:
  - separate audio endpoint with chunk identifiers
  - MediaSource/WebSocket/WebRTC path
  - pre-signed object URLs for completed sentence clips

### 8. Medium: `/api/chat` agent selection is not shell-injection prone today, but authorization is too loose

Files:

- `server.mjs:272-285`
- `index.html:518-531`

The endpoint rejects unknown agents by looking up `AGENT_APIS[agent]`, so arbitrary shell injection through the `agent` field is not present in the current code path. That is the right basic shape.

However:

- any localhost caller can invoke any configured provider
- there is no per-agent authorization, quota, or audit
- CORS is `*`, so any webpage opened in the same browser can call the hub if it can reach `localhost:7890`

For a local single-user tool, that may be acceptable. For anything beyond that, it is too open.

Recommendation:

- keep the allowlist lookup
- restrict CORS to known localhost origins
- add a local session token or CSRF-style nonce if browser trust matters

### 9. Medium: `.env` is properly gitignored in multiple places, but the runtime still centralizes secrets in a plain-text file

Gitignore coverage found:

- `fde/.gitignore:9-12`
- `fde/palette/.gitignore:48`
- `fde/palette/peers/.gitignore:1`

So the specific ask is satisfied: `hub/.env` is ignored, and broader `.env` patterns are also ignored.

Residual risk:

- secrets live in a plaintext file readable by the local account
- `loadKeys()` logs which providers are configured (`server.mjs:69-77`), which is not secret leakage by itself but does reveal capability surface

Recommendation:

- acceptable for local development
- for production, move to environment injection or secret manager instead of repo-adjacent `.env`

### 10. Medium: Reading `~/.claude/.credentials.json` increases blast radius if the process is compromised

Files:

- `server.mjs:63-67`

The code reads the Claude OAuth token from the user’s home directory. It does not print the token, which is good. But pulling personal CLI credentials into an HTTP server process means any SSRF/local-RCE issue in the hub inherits access to that subscription token.

Recommendation:

- for local experimentation this is tolerable
- for production, use a dedicated service credential path or isolate Claude access behind a worker process with tighter permissions

### 11. Medium: No health endpoint, and bus failures are mostly silent

Files:

- `server.mjs:156-170`
- `server.mjs:817-826`
- `index.html:270-273`

Bus polling failures are swallowed silently. The browser toggles the badge to offline when the SSE connection itself errors, but not when the hub is up and only the bus is down. There is also no `/health` endpoint exposing:

- process liveness
- bus reachability
- key/provider readiness
- recent retrieval/TTS/LLM failure counts

Recommendation:

- add `/health` and ideally `/ready`
- include dependency status and last successful upstream contact timestamps

### 12. Medium: No conversation memory or request-scoped history

Files:

- `server.mjs:327-335`
- `server.mjs:643-650`, `686-693`, `730-737`, `774-781`

Every direct LLM call sends only one system prompt and one user message. There is no rolling history, no server-side session context, and no summarization strategy. This is fine for one-shot voice turns, but it will feel stateless very quickly.

Recommendation:

- add per-session memory with truncation/summarization
- separate ephemeral spoken context from durable project memory

### 13. Medium: No rate limiting or abuse controls

Files:

- `server.mjs:189-541`

There is no concurrency limit, IP throttle, per-provider rate budget, or request accounting. On localhost this is mostly accidental self-DoS risk; in any shared environment it becomes a real abuse path.

Recommendation:

- add simple in-memory token bucket per IP/session first
- add per-provider concurrency caps

## Answers To The Specific Questions

### Reliability

- API times out mid-stream:
  There is no explicit timeout. If the provider throws, the server sends `event: error` and ends the stream (`server.mjs:405-412`). If the provider just stalls, the browser can hang waiting indefinitely.
- Rime TTS fails on one sentence:
  The whole response does not die. That sentence’s audio is dropped silently and text continues (`server.mjs:349-372`, `376-400`).
- `palette_retrieve.py` takes >5 seconds:
  The intended 5s timeout is not reliably enforced by the current subprocess code (`server.mjs:297-309`). In practice the request can block before the first token.
- Claude CLI hangs:
  No safeguard. `/api/chat` can hang indefinitely because the Claude subprocess has no timeout or kill path (`server.mjs:573-592`).

### Security

- `.env` gitignored:
  Yes. The ignore coverage is adequate for local use.
- Claude OAuth token exposure risk:
  Not printed, but loading a user-scoped OAuth token into a long-running HTTP server broadens exposure if the server is compromised.
- `/api/chat` accepts any agent name:
  Unknown names are rejected by allowlist lookup, so direct injection risk is low. The bigger issue is that any reachable localhost origin can invoke allowed providers.
- `CORS: *` for localhost:
  Tolerable only for single-user local development. Not acceptable for production or even semi-shared workstation use.

### Performance

- Sentence regex:
  Too naive for abbreviations, decimals, and acronym chains.
- Base64 audio over SSE:
  Fine for a local prototype, inefficient for production.
- Python subprocess per retrieval:
  Expensive and adds cold-start cost. A persistent worker process or in-process cache would be better once retrieval matters to latency.

### Streaming Architecture

- Claude one big chunk vs token streaming elsewhere:
  Yes, this creates a real UX inconsistency. Claude will often appear “silent then dump,” while others feel live.
- Audio queue sequential drain:
  Preserves order, but with no backpressure. If TTS is slower than text generation, lag grows without bound.

## What Is Missing For Production

### Error recovery

- upstream timeouts and aborts
- retry strategy for transient provider failures
- client-visible partial-response states
- structured logging and metrics

### Conversation history / memory

- session-scoped turn history
- summarization when context grows
- distinction between short-term conversation state and durable project memory

### Rate limiting

- per-IP and per-session throttles
- per-provider concurrency caps
- request budget accounting

### Health endpoint

- `/health` for liveness
- `/ready` for dependency readiness
- status for bus, retrieval worker, TTS provider, and each LLM provider

## Recommended Priority Order

1. Fix retrieval subprocess control and move retrieval off the critical path for first token.
2. Add timeout, abort, and exit-code handling for Claude CLI and all streaming fetches.
3. Handle `error` and `done` events explicitly in the browser and surface degraded states in UI.
4. Add bounded audio queues with cancellation on new user turns.
5. Add `/health`, basic rate limiting, and minimal structured logging.
6. Replace sentence splitting heuristic with a safer boundary detector.
7. Add conversation memory once transport reliability is stable.

## Bottom Line

Voice Hub v2 is good enough for local live testing, but not yet resilient enough for unattended use. The biggest gap is not model quality. It is control-plane discipline around subprocesses, stream timeouts, and queue management.
