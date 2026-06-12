# Kiro Handoff — missioncanvas.ai Final Fix

**Priority**: P0 — BDB submission due June 2, 11:59pm PT
**From**: claude.analysis
**Status**: VPS backend is LIVE. One frontend change needed.

---

## What Claude Did (all done)

1. ✅ Nginx HTTPS reverse proxy on VPS (`srv1390882.hstgr.cloud` port 443 → localhost:7890)
2. ✅ SSL cert wired (Let's Encrypt, valid until Aug 29)
3. ✅ Killed old `demo_server.py` (Python, stale since May 5)
4. ✅ Started real Node.js hub on port 7890
5. ✅ Started broker on port 7899
6. ✅ API keys loaded: Perplexity ✓, Mistral ✓, Rime TTS ✓, Groq ✓
7. ✅ Rsynced latest code (peers/, taxonomy/, knowledge-library/, bdb/)
8. ✅ Python deps installed (numpy, httpx, pyyaml)
9. ✅ HTTPS health check passing: `https://srv1390882.hstgr.cloud/health`
10. ✅ SSE chat streaming confirmed from outside the VPS

---

## What Kiro Needs to Do

### One line change

**File**: `docs/landing/index.html` — line 584

```javascript
// CURRENT (broken — port 7890 has no SSL):
: 'https://srv1390882.hstgr.cloud:7890';

// CHANGE TO (routes through nginx HTTPS on port 443):
: 'https://srv1390882.hstgr.cloud';
```

### Then push to GitHub Pages

```bash
git add docs/landing/index.html
git commit -m "fix: route Voice Hub through HTTPS reverse proxy"
git push origin main
```

GitHub Pages will redeploy. missioncanvas.ai should work within 1-2 minutes.

---

## Verification

After push, test from browser:

1. Open https://missioncanvas.ai
2. Click mic or type: "What fiduciary duty standards apply in Delaware?"
3. Should get SSE-streamed response with Perplexity research
4. Type: "What's our exposure if the majority member was self-dealing?"
5. Should see governance boundary / blocked signal

### Quick curl test (should already work now):
```bash
curl -s https://srv1390882.hstgr.cloud/health
```

---

## Known Limitations

- **No Ollama on VPS** — retrieval uses FTS5 + keyword fallback instead of embeddings. Classification still works.
- **Claude key not on VPS** — synthesis step falls back to Groq. Perplexity and Mistral are the main demo models.
- **Processes are not systemd-managed** — if VPS reboots, hub and broker need manual restart. Fine for demo window.

---

## Architecture (for context)

```
Browser (https://missioncanvas.ai — GitHub Pages)
  ↓ fetch("https://srv1390882.hstgr.cloud/api/chat")
  ↓ nginx (port 443, SSL) → proxy_pass localhost:7890
  ↓ Node.js hub (server.mjs)
    ↓ palette_retrieve.py (taxonomy classification)
    ↓ Perplexity API (research) / Mistral API (critique) / Rime (TTS)
  ↓ SSE stream back to browser
```

---

*Handoff from claude.analysis. 2026-06-01.*
