# V3 Complete Reference — Kiro Session Record
## Date: 2026-05-17
## Purpose: Full state snapshot for context window recovery

---

## Product Truth

> **Palette is where your judgment compounds.**

Every AI tool gives you an answer and forgets why you asked. Palette remembers what you decided, why you decided it, and makes every future decision better.

**Competition**: Perplexity Billion Dollar Build. Deadline: June 2, 2026.

---

## System State (as of 2026-05-17)

- Health: 84/85 (only failure = not pushed to remote)
- V3 test suite: 49/49 PASS
- Retrieval recall@5: 95% (19/20)
- Terminology drift: 0 HIGH
- Git: clean working tree, all committed

---

## Infrastructure — Model Stack

| Agent | Provider | Model | Cost | Latency | Purpose |
|-------|----------|-------|------|---------|---------|
| claude | anthropic (CLI) | claude-sonnet-4 | Max sub | ~3s | Primary reasoning, synthesis |
| perplexity | perplexity | sonar-pro | Pro sub | ~2s | Quick research |
| computer | perplexity | sonar-deep-research | Pro sub | ~5s | Deep research |
| reasoning | perplexity | sonar-reasoning-pro | Pro sub | ~3s | Analytical reasoning |
| kimi (free tier) | **groq** | llama-3.3-70b-versatile | **$0/mo** | 1.5s | Free tier for all users |
| local (offline) | ollama | qwen2.5:7b | $0 | 2.2s | Offline fallback |
| mistral | mistral | mistral-medium-3.5 | API key | ~2s | Critique/analysis |
| codex | openai | gpt-4o | API key | ~2s | Implementation |
| qwen | dashscope | qwen-max | API key | ~2s | Specialist |

### Free Tier Architecture
```
User → Hub → Groq (Llama 3.3 70B, free, 1.5s)
                └→ fallback: Ollama Qwen 2.5-7B (local, 2.2s)
```
- Groq API key: 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
- Rate limits: 1,000 RPD on 70B, 14,400 RPD on 8B
- Covers 100 users × 10 queries/day at $0

### Embeddings
- Model: nomic-embed-text (Ollama, local, 274MB)
- Storage: peers/hub/kl_embeddings.json (1.9MB, 183 entries, 768-dim)

---

## V3 Deliverables — All Complete

| # | Task | Status | Owner |
|---|------|--------|-------|
| 1 | FTS5 hybrid retrieval (keyword+FTS5+vector, RRF) | ✅ | Kiro |
| 2 | Perplexity Computer integration | ✅ | Claude |
| 3 | Wiki/manifest drift fix | ✅ | Claude |
| 6 | Voice Hub Learning Mode | ✅ | Kiro |
| 7 | palette query CLI (5-step pipeline) | ✅ | Claude |
| 8 | PII scrubbing (regex, defense-in-depth) | ✅ | Claude |
| 10b | 7 KL entries about Palette (LIB-186-192) | ✅ | Claude |
| 11 | Session reflection | ✅ | Claude |
| 12 | Query-before-acting | ✅ | Claude |
| 13 | Health Section 9 (retrieval quality) | ✅ | Kiro |
| 14 | Tessitura voice profiles | ✅ | Kiro+Codex |

---

## Tessitura Voice System (Arcana v3)

| Agent | Speaker | Speed | Band | Baseline State |
|-------|---------|-------|------|---------------|
| claude | astra | 0.95 | 0.88–1.00 | SYNTHESIS |
| kiro | parapet | 1.0 | 0.92–1.06 | PRECISION |
| codex | walnut | 1.0 | 0.96–1.04 | CONTACT |
| mistral | luna | 1.0 | 0.92–1.08 | ANALYSIS |
| gemini | lyra | 1.02 | 0.98–1.08 | SIGNAL |
| computer | celeste | 0.90 | — | deep research |
| perplexity | oculus | 0.94 | — | search |
| reasoning | pilaster | 0.90 | — | sustained thought |
| qwen | moss | 1.0 | — | specialist |
| kimi | vespera | 1.0 | — | onboarding |

Model: `arcana` (Rime Arcana v3, 94 voices)
Implementation: `resolveVoice(agent, state)` in server.mjs

### Design Contract
1. Three layers: Identity → State weight → Delivery mechanics
2. No state modulation may erase baseline identity
3. States are deltas from self, not costume changes
4. Internal weight, not audience management
5. v1 = 5 states per agent

---

## Key Files

| File | Purpose |
|------|---------|
| peers/hub/server.mjs | Voice Hub — TTS, LLM routing, Learning Mode, Tessitura |
| peers/hub/palette_retrieve.py | Hybrid retrieval (FTS5+vector+keyword, RRF) |
| peers/hub/kl_embeddings.json | Pre-computed vector embeddings (183 entries) |
| scripts/palette_query.py | CLI: resolve→retrieve→route→respond→extract |
| scripts/session_reflect.py | End-of-session learning extraction |
| scripts/query_before_act.py | Agents check KL+memory before dispatch |
| scripts/test_v3.py | 49-test V3 validation suite |
| agents/health/health_check.py | Sections 1-9 including retrieval quality |
| agents/researcher/auto_enrich.py | PII scrubbing + governance proposals |
| core/palette-core.md | Tier 1 governance (includes Product Truth) |
| docs/product/PALETTE_MOAT_ITERATIONS_2026-05-16.md | Moat document (13 iterations) |
| docs/V3_REFOCUS_LIST_2026-05-16.md | System alignment checklist |
| MANIFEST.yaml | Single source of truth for counts/paths |
| peers/broker/index.mjs | Peers bus broker (port 7899) |
| peers/adapters/generic/server.mjs | MCP adapter for all agents |

---

## Submission Strategy

### The Sentence
> Palette is a governed intelligence system. You speak a problem. A team of expert agents — each with its own voice, memory, and knowledge — deliberates, decides, and teaches. The system doesn't just answer. It makes you more capable.

### Altitude Stack
1. **Tagline**: "Your judgment compounds here."
2. **Product line**: "Palette is where your judgment compounds."
3. **Explanation**: "Every AI tool gives you an answer and forgets why you asked. Palette remembers what you decided, why you decided it, and makes every future decision better."
4. **Category**: "Palette is the operating system for human judgment."
5. **Investor**: "Palette captures and compounds the demand signal for human judgment."
6. **Internal**: "SDK for Humans."

### Demo Sequence (3 interactions proving compounding)
1. User speaks a decision problem → system classifies, retrieves, flags ONE-WAY DOOR
2. User returns next day → system recalls decision + reasoning (not chat history)
3. User asks related question → system connects to prior decisions automatically

### Framing: C (SDK for Humans — the hard version)
Unanimous crew agreement. "A governed intelligence system that makes irreversible decisions safer and transfers capability to the human."

---

## Remaining Work (before June 2)

| Item | Owner | Status |
|------|-------|--------|
| Landing page + waitlist | Mical | Not started |
| Sierra traction doc | Mical | Not started |
| Demo video (3-5 min) | Mical | Needs working Hub |
| Write submission answers | Mical + Claude | After demo |
| Push to remote | Kiro/Claude | Ready (just `git push`) |
| Script consolidation (optional) | Deferred | V3.1 |

---

## Peers Bus

- Broker: port 7899, SQLite persistence, FTS5 search
- Registered peers: kiro.design, claude.analysis, codex.implementation, gemini.specialist, mistral-vibe.builder
- Protocol: v1.0.0, envelope validation, trust tiers
- Endpoints: /health, /register, /send, /fetch, /search, /memory, /skills, /list-peers

---

## Governance

- Tier 1: core/palette-core.md (Product Truth added 2026-05-16)
- Tier 2: core/assumptions.md
- Tier 3: decisions.md (append-only)
- Wiki: 345 pages, deterministic compiler, 8/8 validation
- Proposals: 3 expired (PROP-007,008,009), 0 stale

---

## Lid-Switch Fix (Infrastructure)

File: `/etc/systemd/logind.conf.d/no-suspend-on-lid.conf`
```
[Login]
HandleLidSwitch=lock
HandleLidSwitchExternalPower=lock
HandleLidSwitchDocked=ignore
```
Apply safely: `sudo systemctl kill -s HUP systemd-logind`
NEVER use: `systemctl restart systemd-logind` (kills GUI session)
