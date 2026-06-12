# Demo Recording Script — 2 Minutes
**Read this while screen recording. Split screen: browser (missioncanvas.ai) left, terminal mirror right.**

---

## [0:00-0:10] HOOK — Say while showing the landing page

"Every professional has the same AI problem: the useful context is the dangerous context. Today I will show the legal wedge: a lawyer wants AI on a live matter, but the client facts cannot touch the cloud."

## [0:10-0:40] MOMENT 1 — PROTECT blocks client strategy

"First, strategy. I pick PROTECT and ask something sensitive."

**ACTION:** Click PROTECT. Type: "What is our exposure if the majority member at Meridian Holdings was self-dealing on the $2.3M contract?"

"Mission Canvas classifies the question, sees client-specific strategy language, and blocks external research. Ollama handles the reasoning locally. The terminal shows LOCAL, not EXTERNAL. Zero data left the machine."

**ACTION:** Point to pipeline chips: REASON LOCAL -> RESEARCH BLOCKED -> SYNTHESIZE LOCAL.

## [0:40-1:18] MOMENT 2 — RESEARCH routes public law to Perplexity

"Now the safe version: public law, same issue. I switch to RESEARCH and ask the legal question without client facts."

**ACTION:** Click RESEARCH. Type: "What Delaware case law applies to majority member self-dealing?"

"This time the system classifies the query, retrieves local context, opens the governed research window, and routes the public-law question to Perplexity. Citations come back. The models help, but they never meet the client. That is Perplexity as governed research layer — the external window, controlled."

**ACTION:** Let the response stream. Point to terminal showing INTENT / AGENT / CLASSIFY / ROUTE.

## [1:18-1:45] MOMENT 3 — DECIDE shows the intent layer

"Now I switch intents. Same governance layer, different job. DECIDE uses a different route to reason about reversibility and risk."

**ACTION:** Click DECIDE. Type: "How should a founder decide whether this is a one-way or two-way door?"

"Six intents. Multiple models. One governance layer. Legal is the two-minute proof, but the same pattern works anywhere the useful context is also the dangerous context."

## [1:45-2:00] CLOSE

"Four AI models worked the matter. None of them know the client exists. Mission Canvas is the governed agent OS for sensitive professional work. The tools come and go. The judgment stays."

---

## Recording Checklist

1. Hard refresh https://missioncanvas.ai
2. Split screen: Chromium left, terminal mirror right
3. Open terminal mirror: `ssh root@srv1390882.hstgr.cloud "tail -f /tmp/hub.log"`
4. Warm up Ollama with one throwaway query before recording
5. Verify PROTECT, RESEARCH, and DECIDE respond
6. Verify Yeti mic in OBS audio settings
7. Hit Record
8. Upload to YouTube unlisted or Google Drive with anyone-with-link access
9. Paste link into the form

**Total recording time target: 1:50-2:00**
