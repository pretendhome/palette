# Voice Hub — Multi-Agent Voice Interface

A voice-first interface for talking to multiple AI agents through a single multilingual surface.

## What It Does

Select an agent, select a language, speak. The agent responds through voice.

- **5 agents**: Claude, Mistral, Codex/GPT, Qwen, Perplexity — each with a distinct voice
- **4 languages**: English, French, Italian, Spanish — STT recognition and TTS output
- **Taxonomy-routed retrieval**: Every query classified through 121 RIU nodes and grounded in 168 knowledge entries before the agent responds
- **Sentence-boundary streaming**: Rime Arcana v2 TTS fires at each sentence boundary for sub-700ms time to first audio
- **Governed message bus**: SQLite bus with risk gates, human checkpoints, and audit trails

## Architecture

```
User speaks → Whisper STT → Hub server → Palette taxonomy retrieval
                                       → LLM API (streaming)
                                       → Sentence boundary detection
                                       → Rime TTS per sentence
                                       → Audio chunks → Browser playback
```

## Running

```bash
voice-hub        # start hub + bus + watcher, open browser
voice-hub stop   # stop everything
voice-hub status # check agents and connectivity
```

Requires: Node.js, Python 3, Whisper, API keys in `.env` (see `.env.example`).

## Files

| File | Purpose |
|------|---------|
| `server.mjs` | HTTP server — LLM routing, TTS proxy, retrieval, health |
| `index.html` | Frontend — chat UI, STT, TTS playback, convergence |
| `style.css` | Dark theme |
| `palette_retrieve.py` | Taxonomy classification + knowledge retrieval |
