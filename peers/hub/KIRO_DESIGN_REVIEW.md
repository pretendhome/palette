# Voice Hub v2 — Design Review

**Reviewer**: kiro.design
**Date**: 2026-04-14
**Scope**: server.mjs (488 lines), index.html (580 lines), palette_retrieve.py (93 lines), style.css (340 lines)
**Verdict**: Ship-ready for Sierra demo with 3 fixes and 5 recommendations

---

## 1. UI/UX Review

### Agent selector
Works well. The dropdown + clickable sidebar cards is a good dual-path. One issue: the dropdown values (`claude.analysis`, `codex.implementation`) don't match the `AGENT_APIS` keys on the server (`claude`, `codex`). The frontend has `AGENT_CHAT_NAMES` to bridge this, but it's a mapping that will break every time an agent identity changes. Consider making the server accept either form.

### Language selector
Clean. The EN/FR/IT/ES pills are compact and the placeholder text updates per language — nice touch. Missing: there's no visual indicator of which language is active during voice recording. When the mic is hot and you're speaking French, the only signal is the dropdown state. A small flag or language badge near the mic button would help.

### RIU classification tags (green badges)
These are valuable for the Sierra demo — they prove the taxonomy is working in real-time. For daily use they'd be noisy, but for a demo they're exactly right. Recommendation: add a toggle to show/hide them (like the TTS toggle), default ON for demo, OFF for daily use.

### Sidebar (Convergence / Agents / Wiki)
The convergence tracker is the most original piece here. Voice commands for "what do we know" / "what's still open" are genuinely useful during a working session. The wiki browser is functional but the raw `<pre>` rendering makes it hard to scan. The agent roster duplicates information already in the dropdown.

For Sierra: the convergence panel is the differentiator. Lead with it. The wiki browser is nice-to-have. The agent roster could be collapsed by default.

### What's missing for daily use
- Conversation history persistence (currently in-memory, lost on refresh)
- Message search/filter
- Keyboard shortcut for mic toggle (spacebar-to-talk would be natural)
- Visual waveform or level meter during recording (confidence that mic is working)

---

## 2. Interaction Patterns

### Room mode (auto-routing)
Yes, but not yet. The taxonomy retrieval already classifies every query — you could use the RIU classification to pick the best agent. Example: if the query maps to a research RIU, route to Perplexity. If it maps to architecture, route to Claude. This is a natural extension of what `palette_retrieve.py` already does. But it's a 🔄 two-way door — build it after Sierra, not before.

### Agent interruption / cross-talk
Not for Sierra. The current "one agent responds at a time" model is correct for a demo. Cross-talk would be confusing to watch and hard to follow by voice. If you build this later, it should be opt-in ("room mode") not default.

### Conversation history
This is the biggest gap. Each message is standalone — the LLM gets no prior context. For a demo this is fine (each question is self-contained). For daily use, you need at minimum a sliding window of the last N messages passed as conversation history to the LLM. The `sessions` Map on the server already tracks convergence state per session — extend it to hold message history too.

---

## 3. Voice Quality

Can't listen from CLI, but the architecture is sound:

- 6 distinct Rime speakers across agents (astra, luna, celeste, orion, arcas, cove) — good differentiation
- Speed variation (0.95–1.12) adds subtle personality
- Sentence-boundary TTS streaming is the right approach for latency

### Latency concern
The `/api/chat` endpoint does: LLM stream → accumulate sentence → Rime TTS API call → base64 encode → SSE push → browser decode → Audio play. Each Rime call is a network round-trip. For sub-700ms first audio, the critical path is: time-to-first-sentence from LLM + one Rime call. Claude via CLI subprocess (`claude -p`) will be slower than the direct API providers because of process spawn overhead. Measure this — it may be the bottleneck.

### Multilingual
The Rime `lang` parameter is passed through correctly (eng/fra/ita/spa). The LLM system prompt says "respond in the same language the user is speaking" which is the right approach. One gap: the language instruction is only added when `lang !== 'eng'`, but the STT `recognition.lang` defaults to `en-US`. If someone switches to French mid-conversation, the STT language updates but there's a moment where the recognition is still in English mode. The 200ms timeout on language switch restart should handle this, but test it.

---

## 4. Architecture Review

### server.mjs — Strengths
- Clean separation: bus proxy, TTS proxy, LLM routing, wiki, convergence — each is a distinct route
- SSE bridge from bus polling is elegant
- Body size limit (1MB) prevents abuse
- Directory traversal protection on wiki routes
- Graceful degradation when retrieval fails (continues without context)

### server.mjs — Issues

**ISSUE 1 (HIGH): Duplicated streaming parser**
The OpenAI-compatible SSE parser (read stream → split lines → parse `data:` → extract delta content) is copy-pasted 5 times for mistral/openai/perplexity/dashscope/kiro. Extract it:

```javascript
async function* parseOpenAIStream(resp, label) {
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buf = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    const lines = buf.split('\n');
    buf = lines.pop() || '';
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      const data = line.slice(6).trim();
      if (data === '[DONE]') return;
      try {
        const token = JSON.parse(data).choices?.[0]?.delta?.content;
        if (token) yield token;
      } catch { /* skip */ }
    }
  }
}
```

Then each provider becomes ~15 lines (build request + call `parseOpenAIStream`). This cuts ~120 lines of duplication.

**ISSUE 2 (HIGH): Claude subprocess has no timeout**
The `claude -p` spawn has no timeout. If Claude hangs, the SSE connection stays open forever. Add a timeout:

```javascript
const proc = spawn('claude', ['-p', fullPrompt, '--model', model], { ... });
const timeout = setTimeout(() => proc.kill('SIGTERM'), 30000);
proc.on('close', () => clearTimeout(timeout));
```

**ISSUE 3 (MEDIUM): TTS in the streaming loop blocks text delivery**
Inside the `/api/chat` handler, TTS generation happens synchronously in the streaming loop — each sentence waits for the Rime API call before the next text chunk is processed. The text tokens still stream to the client, but the `await fetch(RIME_API, ...)` blocks the loop iteration. Consider firing TTS calls in parallel (don't await them inline — push to a queue and let them resolve independently).

**ISSUE 4 (LOW): `var eventType` in frontend**
Line in `directChat`: `var eventType = line.slice(7);` — should be `let`. The `var` hoists and the eventType leaks across loop iterations. It works by accident because the event/data lines are always paired, but it's fragile.

**ISSUE 5 (LOW): `.env` file in hub directory**
Keys are loaded from `hub/.env`. Make sure this is in `.gitignore`. I didn't see a `.gitignore` in the hub directory.

### index.html — Strengths
- Single-file frontend with no build step — perfect for a demo
- Voice command grammar is well-designed (natural phrases map to convergence actions)
- TTS queue with drain pattern prevents audio overlap
- Agent voice map is consistent between server and client

### index.html — Issues

**ISSUE 6 (MEDIUM): No error feedback to user**
When an API call fails (LLM down, Rime down, bus down), errors go to `console.error` but nothing appears in the chat. Add a system message bubble for errors so the user knows what happened.

### palette_retrieve.py — Clean
93 lines, does one thing, does it well. Loads taxonomy, resolves query to knowledge entries, builds context string. The 5-second timeout from the server side is appropriate. No issues found.

---

## 5. Sierra Demo Recommendations

In priority order:

1. **Fix the Claude subprocess timeout** (Issue 2) — a hang during a live demo is catastrophic
2. **Add error feedback to chat** (Issue 6) — if an API key is wrong, the user needs to see why
3. **Add `.gitignore` for `.env`** (Issue 5) — before this goes to GitHub
4. **Extract the streaming parser** (Issue 1) — not urgent for demo, but do it before adding more providers
5. **Add a keyboard shortcut for mic** — spacebar or a function key, for smoother demo flow

### What NOT to change before Sierra
- Don't add room mode
- Don't add conversation history
- Don't add agent cross-talk
- Don't refactor the frontend into components

The current system is a clean demo of: pick an agent → speak in any language → get a voiced response grounded in Palette knowledge. That's the story. Keep it tight.

---

## 6. Identity Drift Note

The bus currently has `claude-code` registered (not `claude.analysis` per wire contract). The frontend dropdown sends to `claude.analysis`. The `AGENT_CHAT_NAMES` map handles this for direct chat, but bus-routed messages to `claude.analysis` won't reach `claude-code`. Either update Claude's registration or update the frontend — but pick one before the demo.

---

**Review complete. Ship it.**
