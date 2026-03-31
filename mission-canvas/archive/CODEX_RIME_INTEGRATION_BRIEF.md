# Codex Brief: Mission Canvas x Rime Voice Integration

**Status**: Active — workshop tonight (March 17, 2026), office visit Wednesday
**Owner**: Mical
**For**: Codex creative ideation before implementation

---

## Context: What We're Walking Into

### Tonight (March 17, 5:30-8:30 PM, 577 Howard St SF)
ClawdTalk & Rime Workshop hosted by Telnyx. Build session — deploy an OpenClaw agent, connect it to ClawdTalk for live voice, and demo something working by 8:15 PM. **Prize: Mac mini for best demo.**

### Wednesday (March 19, ~4 PM, Rime office in Oakland)
Mical visits Brooke Larson at Rime. Brooke is Rime's founder — she and Mical were colleagues at Amazon (2019-2022), rode the shuttle together, built Alexa. She left Amazon in April 2022 to start Rime. They've stayed in touch (coffee in the Mission, Sept 2022). Mical messaged her about Palette on March 2 — "I've been building an agentic Applied Intelligence Toolkit... I've been thinking about doing a voice-only interface... I would love to see if I could use your system as the interface somehow."

### The Company: Rime
- Founded April 2023 by Brooke Larson (PhD Linguistics, UMD; former Harvard/Iowa linguistics professor; Amazon Language Engineer)
- CEO: Lily Clifford
- **Revenue doubling every 3 months** as of Feb 2026. 4x daily usage.
- Won "Most Innovative Use of AI" at Enterprise Connect (beat Zoom and Five9)
- Arcana V3: 94 voices, 11 languages, native code-switching, laughs/sighs/hums, sub-200ms latency
- Mist V2: 70ms latency, deterministic pronunciation
- Pricing: ~$0.02-0.03/min
- Partnerships: Telnyx (native integration), SLNG (global edge), Together AI (WebSocket streaming)
- Just hired: Head of Marketing (Megan Dorcey), ML Researcher from Amazon (Guillermo Cámbara), Speech Scientist from Meta/Amazon (Che-Wei Huang)

---

## What Already Exists: Mission Canvas

### Architecture (built Feb 2026, 6 iterations)
```
missioncanvas-site/
├── index.html          — Voice-first UI with browser Web Speech API
├── app.js              — Frontend routing, persona chips, streaming
├── server.mjs          — API adapter (Node.js) with 3 upstream modes
├── openclaw_adapter_core.mjs — Shared validation, local routing fallback
├── terminal_voice_bridge.mjs — CLI microphone → route → TTS
├── config.js           — Runtime configuration
├── styles.css          — Space Grotesk + IBM Plex Mono
├── for-business-owners.html — Landing page variant
├── deploy/PRODUCTION_WIRING.md — Deployment runbook
├── pilot-output/       — Rossi pilot artifacts
└── CNAME              — missioncanvas.ai
```

### API Endpoints (v1.2)
```
GET  /v1/missioncanvas/health
GET  /v1/missioncanvas/capabilities
POST /v1/missioncanvas/route          — structured Palette routing
POST /v1/missioncanvas/talk-stream    — NDJSON streaming
POST /v1/missioncanvas/confirm-one-way-door
POST /v1/missioncanvas/log-append     — decision log
```

### What It Does Today
1. User speaks (browser Web Speech API) or types
2. Speech is translated into structured fields (objective, context, desired outcome, constraints, risk posture)
3. Fields are routed through Palette policy (convergence → RIU selection → agent assignment → one-way-door check)
4. Returns: selected RIUs, agent map, action brief, validation checks, decision log payload
5. Brief can be spoken back (browser Speech Synthesis) or streamed

### What It DOESN'T Do (Yet)
- No real phone number (browser-only)
- No production-grade TTS (browser Speech Synthesis is robotic)
- No persistent voice conversations (stateless per request)
- No Rime integration
- No ClawdTalk/Telnyx wiring
- No real OpenClaw deployment (uses local fallback routing)

### Palette Policy (Non-Negotiable in Any Integration)
- Convergence before execution
- One-way-door gating (irreversible decisions require human confirmation)
- Glass-box outputs (explain route, rationale, artifact, next check)
- RIU-first routing (117 problem-solution pairs)
- Evidence-based only (no speculative claims)

---

## The OpenClaw + ClawdTalk + Rime Stack

### How It Works (Full Pipeline)
```
Phone call (or WebRTC)
    ↓
Telnyx PSTN/SIP (carrier-grade, <100ms network latency)
    ↓
ClawdTalk Server (managed by Telnyx)
    ├── STT: Telnyx Whisper / Deepgram
    ├── TTS: Rime Arcana V3 (natively available on Telnyx)
    ↓
WebSocket → OpenClaw Gateway (ws://127.0.0.1:18789)
    ├── /v1/chat/completions endpoint
    ├── Agent processes with full tool access
    ├── Memory, skills, multi-channel context
    ↓
Response text → Rime Arcana V3 TTS → Audio back to caller
```

### OpenClaw Basics
- TypeScript/Node.js, runs as daemon
- Config: `~/.openclaw/openclaw.json`
- Agent identity: AGENTS.md, SOUL.md, IDENTITY.md
- Memory: daily logs + MEMORY.md (long-term)
- Skills: bundled, managed, workspace-local
- Channels: 20+ (Telegram, Slack, WhatsApp, Discord, etc.)

### ClawdTalk Setup
1. Clone `clawdtalk-client` to `~/clawd/skills/clawdtalk-client`
2. Run `./setup.sh` (API key, gateway config)
3. `./scripts/connect.sh start` → persistent outbound WebSocket
4. Get a phone number (free tier: shared number, 10 min/month)
5. Call the number → talk to your OpenClaw agent

### Rime Integration Paths
1. **Via Telnyx** (easiest): Rime Arcana V3 is natively available as a TTS provider in Telnyx AI Assistants
2. **Via ClawdTalk**: ClawdTalk uses Telnyx NaturalHD by default; may be able to swap to Rime
3. **Via rime-reader skill**: Dedicated OpenClaw skill at `rimelabs/rime-reader-openclaw` — processes text through Rime API, outputs OGG Opus
4. **Direct API**: `POST https://users.rime.ai/v1/rime-tts` with `Authorization: Bearer API_KEY`

---

## The Demo Opportunity (Tonight)

### What Would Win
A working demo where someone **calls a phone number**, describes a business problem in plain speech, and gets back:
1. A Palette-routed plan (RIU selection, agent assignment, action brief)
2. Spoken in a natural, expressive Rime Arcana V3 voice
3. With one-way-door detection ("This decision is irreversible — I need your confirmation before proceeding")
4. And the caller can say "yes, confirm" to approve

**Why this wins**: It's not a chatbot. It's not a demo of TTS. It's a **governed AI decision system with voice as the interface**. Nobody else at the workshop will have the policy layer (convergence, one-way-door gating, RIU routing). They'll have voice agents that chat. We'll have a voice agent that plans.

### Minimum Viable Demo (if time is tight)
- Deploy OpenClaw with Palette AGENTS.md/SOUL.md
- Connect ClawdTalk
- Call the number, say "I need a business plan for my store"
- Get back a structured response spoken in Rime Arcana V3

### Stretch Demo
- Multiple persona modes ("I'm a business owner" / "I'm a teacher" / "I'm an AI operator")
- One-way-door voice confirmation flow
- Knowledge gap detection ("I don't have enough information — can you tell me your budget and timeline?")
- Italian language support (Rime Arcana V3 supports Italian natively — cross with La Scuola/education persona)

---

## The Larger Vision: Mission Canvas x Rime

### What Mical Has Been Thinking About
"I've been thinking about doing a voice-only interface... I would love to see if I could use your system as the interface somehow."

### The Thesis
Palette is an applied intelligence toolkit that routes any problem to the best service at the lowest cost. Mission Canvas is its interface layer. Today that interface is web-based. The vision is **voice-first**: a single phone number (or WebRTC endpoint) that anyone can call and get a governed AI decision.

Voice is the right modality because:
1. **Small business owners** don't sit at computers — they're in their stores, driving, on the floor. Phone is their interface.
2. **Education** (ARON, Tuck) — voice bypasses reading/writing bottlenecks entirely. Tuck's processing speed is 56 (extremely low) but his verbal comprehension is 98 (average). ARON's verbal reasoning is 130 (98th percentile) but her word reading is 50 (0.1st percentile). Voice IS the accommodation.
3. **Speed** — speaking is 3-4x faster than typing. Convergence briefs that take 5 minutes to fill out in a form take 30 seconds to speak.
4. **Trust** — Rime's voices are expressive, not robotic. An AI that sounds human builds more trust than one that sounds like a machine. This matters for the one-way-door confirmation flow — you need to trust the voice telling you "this decision is irreversible."

### What Rime Brings That Others Don't
- **Expressiveness**: Laughs, sighs, natural disfluencies ("um"), mid-utterance prosody control. Not just words — emotion.
- **Code-switching**: 11 languages natively. Italian + English in the same utterance. Perfect for La Scuola.
- **Speed**: Arcana V3 at ~200ms cloud, Mist V2 at ~70ms. Fast enough for real-time conversation.
- **Brooke**: A linguistics PhD who built speech at Amazon. She understands what Mical built (comparative linguistics background → knowledge engineering → applied intelligence). This isn't just a vendor relationship — it's two linguists who took different paths (one into speech synthesis, one into knowledge systems) converging.

### Potential Integration Architectures

**Architecture A: ClawdTalk as Managed Voice Layer**
- Pros: Least work. Telnyx manages infra. Get a phone number in 5 minutes.
- Cons: Less control over the conversation flow. ClawdTalk is stateless per utterance.
- Best for: Tonight's demo. Quick proof of concept.

**Architecture B: Telnyx AI Assistant + Rime + Custom Backend**
- Pros: Full control. Telnyx AI Assistant has tool execution, speaking plan tuning, noise suppression.
- Cons: More setup. Need Telnyx account, AI assistant config, webhook wiring.
- Best for: Production system. The "real" Mission Canvas voice interface.

**Architecture C: Direct WebRTC + Rime API**
- Pros: Maximum control. Browser-based, no phone number needed. Can integrate directly into missioncanvas.ai.
- Cons: Most work. Need to handle STT, conversation state, audio streaming yourself.
- Best for: Web-first experience that also works on mobile.

**Architecture D: Hybrid (Phone + Web)**
- ClawdTalk for phone access (inbound calls)
- WebRTC + Rime for web access (missioncanvas.ai)
- Same OpenClaw agent backend for both
- Best for: The full vision. Meet users where they are.

---

## For Codex: The Creative Brief

Take your time with this. Don't implement — think.

### Questions to Consider

1. **What's the cleverest demo we could build tonight in 2 hours?** We have: working OpenClaw adapter, Palette routing with 117 RIUs, one-way-door gating, persona chips (Game Builder, Business Owner, Education, Job Seeker, Enterprise AI Operator). What combination of these + Rime voice + live phone call would make judges say "this is different from everything else we've seen tonight"?

2. **What would a production Mission Canvas voice interface look like?** Not tonight's hack — the real thing. How does voice change the interaction model? What does convergence sound like? What does a one-way-door confirmation sound like when spoken? How do you handle the "translation layer" (unstructured speech → structured fields) in real-time?

3. **What does the Brooke meeting look like?** Mical and Brooke are both linguists who went to Amazon and then diverged (she → speech synthesis, he → knowledge engineering). What's the partnership pitch? Is it: "Rime is the voice of Palette"? Is it: "Mission Canvas is a reference customer for Rime's agent platform"? Is it: "We should build something together for La Scuola (Italian-English bilingual education + Rime's code-switching)"?

4. **What's the Italian angle?** Rime Arcana V3 does native Italian code-switching. La Scuola is an Italian immersion school. The Italian Bridge concept (using Italian's transparent orthography to scaffold English phonological development) is already designed. What would it look like if Coach Stella (ARON's voice AI tutor) spoke in Rime's voice instead of ChatGPT's? What if TUCK's Coach T spoke with a Rime voice via Telegram voice messages?

5. **What would Mission Canvas look like as a company?** Mical has been building Palette as a toolkit. Mission Canvas is the branded interface layer. If Rime is the voice, Palette is the brain, and Telnyx is the infrastructure — what's the business? Who pays? For what?

### What I'd Focus On

If I were Codex, I'd think about the **"call a number, get a plan" demo** as the centerpiece for tonight, because:
- It's concrete (not a slide deck)
- It's novel (nobody else will have governed AI routing behind a phone call)
- It leverages everything we've built (Palette routing is real, not mocked)
- It uses Brooke's product in the most flattering way (expressive voice delivering structured intelligence, not just reading text)

And for the Wednesday meeting, I'd think about the **education angle** as the partnership hook, because:
- Brooke is a linguistics PhD. Education is linguistically native to her.
- Rime's Italian code-switching is a differentiator no other TTS has.
- La Scuola is a real school with a real need (the AI Classroom Proposal was just written).
- This isn't "we want to use your API" — it's "we have a school, we have students, we have a system, your voice makes it work."

---

## Files to Read (For Full Context)

| File | What It Contains |
|------|-----------------|
| `missioncanvas-site/server.mjs` | Current adapter implementation |
| `missioncanvas-site/openclaw_adapter_core.mjs` | Routing logic and validation |
| `missioncanvas-site/index.html` | Current web UI |
| `missioncanvas-site/app.js` | Frontend logic |
| `palette/docs/openclaw_application_prompt_missioncanvas_v1.0.md` | Palette policy integration |
| `palette/docs/openclaw_application_prompt_missioncanvas_api_contract_v1.0.md` | API contract |
| `implementations/education/claudia-ai-classroom/la-scuola/AI_CLASSROOM_PROPOSAL.md` | La Scuola proposal |
| `implementations/education/adaptive-learning-architecture/aron/ARON_CHATGPT_VOICE_LEARNING_PATH.md` | ARON's voice learning system |
| `implementations/education/adaptive-learning-architecture/tuck/TUCK_LEARNING_PATH.md` | TUCK's Coach T system |
| `palette/MANIFEST.yaml` | Current system state |

---

*This brief is for Codex to think with. No implementation until we align on direction.*
