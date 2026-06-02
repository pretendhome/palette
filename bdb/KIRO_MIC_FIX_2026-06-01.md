# Kiro — Fix Mic on missioncanvas.ai

**Priority**: P0 — demo recording blocked on this
**File**: `docs/index.html`
**Reference implementations**: `docs/voice-demo/bot.html` (lines 385-450) and `docs/oka.html` (lines 895-957) — both work perfectly.

---

## Problem

The mic button on missioncanvas.ai doesn't produce visible results. User clicks mic, nothing visibly happens, no transcript appears, no auto-submit fires.

## Root Cause

The current `toggleMic()` function has a scoping bug: the `collected` variable is declared inside `toggleMic()` as a local `let`, but the `onresult`/`onend` handlers are closures that capture it. Every time `toggleMic()` is called, new handlers are assigned, but the variable they close over gets re-created. Also, the handlers are reassigned on every click — the working implementations (bot.html, oka.html) set up handlers ONCE at init time.

## The Fix

Replace the current voice code (lines 712-767) with this pattern, matching bot.html exactly:

### 1. Change `setupSTT()` to set up handlers once (like bot.html lines 388-427):

```javascript
// ── Voice: STT via Web Speech API ───────────────────────────────────────────
let recog = null;
let isListening = false;
let collectedText = '';

function initSTT() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;
  recog = new SR();
  recog.continuous = false;
  recog.interimResults = true;
  recog.lang = 'en-US';

  recog.onstart = () => {
    isListening = true;
    collectedText = '';
    queryIn.placeholder = 'Listening...';
    queryMic.classList.add('listening');
  };

  recog.onresult = (e) => {
    let interim = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const chunk = e.results[i][0].transcript;
      if (e.results[i].isFinal) collectedText += chunk + ' ';
      else interim += chunk;
    }
    queryIn.value = (collectedText + interim).trim();
  };

  recog.onerror = (e) => {
    isListening = false;
    queryMic.classList.remove('listening');
    if (e.error !== 'no-speech') queryIn.placeholder = 'Mic error — try again';
    else queryIn.placeholder = getIntentPlaceholder(state.intent);
  };

  recog.onend = () => {
    isListening = false;
    queryMic.classList.remove('listening');
    queryIn.placeholder = getIntentPlaceholder(state.intent);
    const message = collectedText.trim();
    collectedText = '';
    if (message) submitQuery(message);
  };
}
```

### 2. Replace the queryMic click handler (line 788-791):

```javascript
queryMic.addEventListener('click', () => {
  if (!recog) initSTT();
  if (!recog) return;
  if (isListening) { recog.stop(); }
  else { try { recog.start(); } catch { queryIn.placeholder = 'Tap mic again in a second'; } }
});
```

### 3. Keep the openMic handler for role selection but use the same pattern:

```javascript
openMic.addEventListener('click', () => {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;
  const rec = new SR();
  rec.continuous = false;
  rec.interimResults = false;
  rec.lang = 'en-US';
  rec.onresult = (e) => {
    const text = e.results[0][0].transcript.toLowerCase();
    if (text.includes('lawyer') || text.includes('attorney') || text.includes('legal')) enterWorkspace('attorney');
    else if (text.includes('doctor') || text.includes('physician')) enterWorkspace('doctor');
    else if (text.includes('financial') || text.includes('advisor')) enterWorkspace('financial-advisor');
    else if (text.includes('executive') || text.includes('ceo')) enterWorkspace('executive');
    else enterWorkspace('other');
  };
  rec.onerror = () => {};
  try { rec.start(); } catch {}
});
```

### 4. Call `initSTT()` at startup (replace the existing `setupSTT()` call at end of script):

```javascript
initSTT();
```

### 5. Remove old code

Delete: `setupSTT()`, `toggleMic()`, the old `state.recognition` property, and the `setupSTT()` call at the bottom of the script.

---

## Why This Works (bot.html pattern)

The key differences from the current broken code:

1. **Handlers set up ONCE** — not reassigned on every click
2. **Module-level state** — `collectedText`, `isListening`, `recog` are module-scoped, not closure-scoped
3. **Click handler is simple toggle** — just `start()` / `stop()`, no handler setup
4. **`onend` auto-submits** — browser fires `onend` after silence, collected text is submitted automatically
5. **No `onFinal` callback** — the `onend` handler calls `submitQuery()` directly

---

## Test

1. Pick Attorney → workspace opens
2. Click mic (🎤 next to input bar) → should show "Listening..." in placeholder, mic button turns red/highlighted
3. Speak "What fiduciary duty standards apply in Delaware" → text appears in input field as you speak
4. Pause for 2-3 seconds → browser auto-stops → auto-submits → response streams
5. Click PROTECT intent → click mic → say "John Smith at Acme Corp owes 2.3 million" → should auto-submit and show PII governance signals

---

## Files to Push

Only `docs/index.html`. Push to BOTH repos:
```bash
# palette repo (GitHub Pages source)
cd /tmp/palette-fix && cp ~/fde/palette/docs/index.html docs/ && git add docs/index.html && git commit -m "fix: mic — use bot.html pattern (handlers once, auto-submit on silence)" && git push origin main

# monorepo
cd ~/fde/palette && git add docs/index.html && git commit -m "fix: mic — use bot.html pattern" && git push origin main
```

---

*Handoff from claude.analysis. 2026-06-01.*
