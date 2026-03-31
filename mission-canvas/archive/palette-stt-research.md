# Speech-to-Text Research Brief for Palette

**Prepared:** March 30, 2026  
**Subject:** Evaluating in-browser STT options for voice-driven agent queries  
**Project:** [Palette](https://github.com/pretendhome/palette) — multi-agent knowledge architecture (12 agents, Python/Go CLI + Node.js broker)

---

## 1. Executive Summary

Palette needs in-browser speech-to-text so users can speak queries to its agent system without a server round-trip for audio. Of the three options evaluated, **Voxtral Realtime is the clear winner for this use case**: it is the only option with a production-ready, natively streaming, in-browser WebGPU implementation via [Transformers.js](https://huggingface.co/spaces/mistralai/Voxtral-Realtime-WebGPU), requires zero server infrastructure, supports 13 languages at sub-500ms latency, and ships under Apache 2.0. IBM Granite 4.0 1B Speech is the accuracy leader (5.52% avg WER, [#1 on OpenASR](https://huggingface.co/ibm-granite/granite-4.0-1b-speech)) but requires a Python server backend and is not streaming-native. Rime is a text-to-speech platform — excellent for *speaking responses back* to users, but not applicable to the speech *input* problem.

---

## 2. Use Case Definition

### What Palette Needs

Palette is a [knowledge architecture with 12 specialized agents](https://github.com/pretendhome/palette) (resolver, researcher, architect, builder, debugger, narrator, validator, monitor, orchestrator, and others). Today it operates via CLI. The goal is to add a browser-based voice input layer so users can:

- **Speak queries** to Palette agents instead of typing
- **Get real-time transcription** as they speak (not upload-then-wait)
- **Use domain vocabulary** accurately — agent names ("resolver," "narrator"), model names, API terms
- **Run without a dedicated STT server** if possible — Palette's architecture is already Python CLI + Node.js broker; adding a GPU-backed transcription server is overhead

### Constraints

| Constraint | Detail |
|---|---|
| **Deployment** | Browser-based; no native app |
| **Latency** | Real-time or near-real-time (<500ms) — users expect live transcription |
| **Server infra** | Minimal; ideally zero additional servers for STT |
| **Privacy** | Audio stays on-device if possible (no external API calls with voice data) |
| **Browser support** | Chrome/Edge required; Safari/Firefox nice-to-have |
| **License** | Permissive (Apache 2.0 preferred for an open-source project) |

---

## 3. Option Comparison

| Dimension | IBM Granite 4.0 1B Speech | Rime (Arcana v3) | Voxtral Realtime |
|---|---|---|---|
| **Primary function** | Speech-to-text (ASR) | **Text-to-speech (TTS)** | Speech-to-text (ASR) |
| **Solves the STT problem?** | Yes | **No** — wrong direction | Yes |
| **Browser-native (no server)?** | No — requires Python/torch backend | No — server API or on-prem | **Yes** — [Transformers.js + WebGPU](https://huggingface.co/spaces/mistralai/Voxtral-Realtime-WebGPU) |
| **Streaming?** | No — batch/upload model | N/A | **Yes** — natively streaming architecture |
| **Parameters** | ~1B (total ~2B with encoder) | N/A (proprietary) | [4B (3.4B LM + 970M encoder)](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) |
| **Avg WER (English)** | **5.52%** ([OpenASR #1](https://huggingface.co/ibm-granite/granite-4.0-1b-speech)) | N/A | ~8.72% at 480ms delay ([Fleurs benchmark](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)) |
| **Latency** | Batch (not real-time) | 120–300ms TTFB (TTS) | [Configurable: 80ms–2400ms](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602); sweet spot 480ms |
| **Languages** | [6](https://huggingface.co/ibm-granite/granite-4.0-1b-speech) (EN, FR, DE, ES, PT, JA) | [10–11](https://rime.ai/resources/arcana-v3) (TTS) | [13](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) (EN, ZH, HI, ES, AR, FR, PT, RU, DE, JA, KO, IT, NL) |
| **Keyword/context biasing** | [Yes — keyword list biasing](https://huggingface.co/ibm-granite/granite-4.0-1b-speech) | N/A | [Yes — up to 100 terms via API](https://mistral.ai/news/voxtral-transcribe-2); available on batch model, API-level for realtime |
| **License** | [Apache 2.0](https://huggingface.co/ibm-granite/granite-4.0-1b-speech) | Proprietary/enterprise | [Apache 2.0](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) |
| **Model download size** | ~1.4 GB (WebGPU demo) | N/A | [~2.8 GB (cached in browser)](https://huggingface.co/spaces/mistralai/Voxtral-Realtime-WebGPU) |
| **Server required?** | Yes (Python + torch or vLLM) | Yes (cloud API or on-prem) | **No** (runs entirely in browser) |

---

## 4. Deep Dive: Each Option

### 4.1 IBM Granite 4.0 1B Speech

**Released:** March 6, 2026 — [model card on Hugging Face](https://huggingface.co/ibm-granite/granite-4.0-1b-speech)

Granite 4.0 1B Speech is IBM's compact ASR model. It currently holds the [#1 position on the HuggingFace Open ASR Leaderboard](https://huggingface.co/ibm-granite/granite-4.0-1b-speech) with an average WER of 5.52% across standard English benchmarks, beating models with far more parameters.

**Architecture:**
- 16 conformer blocks (CTC-trained speech encoder) + 2-layer window Q-former projector + [granite-4.0-1b-base LLM](https://huggingface.co/ibm-granite/granite-4.0-1b-base)
- Total ~2B parameters (half the size of its predecessor granite-speech-3.3-2b, with better accuracy)
- [Speculative decoding](https://huggingface.co/ibm-granite/granite-4.0-1b-speech) for faster inference
- [Keyword list biasing](https://huggingface.co/ibm-granite/granite-4.0-1b-speech): append `"Keywords: agent1, agent2 ..."` to the prompt to boost recognition of specific terms — directly useful for Palette's agent and tool vocabulary

**Deployment options:**
- `transformers >=4.52.1` with `torchaudio` (GPU or CPU)
- [vLLM server](https://huggingface.co/ibm-granite/granite-4.0-1b-speech) (online mode with OpenAI-compatible API)
- [mlx-audio on Apple Silicon](https://huggingface.co/ibm-granite/granite-4.0-1b-speech)
- A [WebGPU demo exists](https://huggingface.co/spaces/webml-community/granite-4.0-1b-speech-webgpu) (requires ~1.4 GB GPU memory, desktop browser only), but it is **batch-mode** — you upload or record audio, then get a transcription back. It is not streaming.

**Why it's not the first choice for Palette:**
1. **Not streaming-native.** The model processes complete audio segments, not live mic input. Adapting it for real-time transcription would require chunked audio uploads to a server endpoint.
2. **Requires a server backend.** Even the WebGPU demo is a [local server + web UI setup](https://www.youtube.com/watch?v=0crS8x-1zgs) (Node.js frontend, Python backend), not a pure in-browser solution.
3. **Integration pattern:** Upload audio → POST to `/api/transcribe` → receive text. This adds latency and infrastructure.

**When Granite is the right choice:**
- Palette later needs highest-accuracy batch transcription (meeting recordings, long-form audio)
- Compliance-sensitive deployments where WER accuracy is paramount
- Edge server deployments where a Python backend is already available
- Keyword biasing is critical and cannot be handled at the application layer

---

### 4.2 Rime (Arcana v3)

**Released:** February 4, 2026 — [announcement on rime.ai](https://rime.ai/resources/arcana-v3)

**Critical clarification: Rime is a text-to-speech (TTS) platform, not speech-to-text.** Rime Arcana v3 converts text into spoken audio — it is an *output* layer, not an *input* layer. If the goal is to let users speak queries *to* Palette, Rime does not solve that problem.

**What Rime does well (for future reference):**
- [120ms on-prem / 200–300ms cloud TTFB](https://rime.ai/resources/arcana-v3) — fast enough for real-time voice responses
- [94+ voices](https://rime.ai/resources/arcana-v3) with paralinguistic modeling (laughs, sighs, hesitations)
- [SOC 2 Type II, HIPAA compliant](https://rime.ai/resources/arcana-v3) — enterprise-grade security
- On-prem, VPC, and cloud API deployment — [single node supports 100+ concurrent generations](https://rime.ai/resources/arcana-v3)
- [10–11 languages with natural code-switching](https://www.together.ai/blog/rime-arcana-v3-turbo-and-rime-arcana-v3-now-available-on-together-ai)
- Available on [Together AI](https://www.together.ai/blog/rime-arcana-v3-turbo-and-rime-arcana-v3-now-available-on-together-ai) co-located with LLM and STT workloads

**Where Rime fits in Palette's future:**
If Palette ever wants agents to *speak responses back* to users (voice output), Rime Arcana v3 is a strong candidate for that half of the pipeline. But it is not a speech-to-text solution and should not be evaluated as one.

---

### 4.3 Voxtral Realtime (Mistral AI)

**Released:** February 4, 2026 — [model card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) | [announcement](https://mistral.ai/news/voxtral-transcribe-2)

Voxtral Realtime is purpose-built for exactly what Palette needs: live, streaming, in-browser speech-to-text.

**Architecture:**
- [4B parameters total](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602): ~3.4B language model (based on Ministral-3B) + ~970M custom causal audio encoder
- **Natively streaming** — unlike offline models adapted for streaming via chunking, Voxtral uses a [custom causal audio encoder with sliding window attention](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) that processes audio as it arrives
- Throughput exceeds [12.5 tokens/second](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602), enabling real-time transcription on modest hardware
- Max context: [131,072 tokens (~3 hours of audio)](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

**Browser deployment (the key differentiator):**
- [Transformers.js + WebGPU demo](https://huggingface.co/spaces/mistralai/Voxtral-Realtime-WebGPU) already exists and works — live on Hugging Face Spaces
- [~2.8 GB model download](https://huggingface.co/spaces/mistralai/Voxtral-Realtime-WebGPU), cached in the browser after first load
- Runs **entirely in the browser** — no server, no API calls, no audio data leaves the device
- [Merged into Transformers.js v4 demos](https://www.reddit.com/r/LocalLLaMA/comments/1rqz53r/voxtral_webgpu_realtime_speech_transcription/) as of March 2026
- Requires WebGPU: Chrome/Edge fully supported; Safari partial; Firefox limited

**Performance:**
- [Configurable latency from 80ms to 2400ms](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) (multiples of 80ms)
- Sweet spot: [480ms delay matches leading offline models](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)
- At 480ms: [8.72% avg WER on Fleurs](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602) (13 languages); English-specific WER around 4.9%
- [13 languages](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602): English, Chinese, Hindi, Spanish, Arabic, French, Portuguese, Russian, German, Japanese, Korean, Italian, Dutch

**Context biasing:**
- [Up to 100 words/phrases](https://mistral.ai/news/voxtral-transcribe-2) for proper nouns, technical terms, domain vocabulary
- Available via [Mistral API](https://mistral.ai/news/voxtral-transcribe-2) for both batch (Transcribe V2) and realtime modes
- For in-browser WebGPU deployment: context biasing is an API-level feature — implementing it in the local WebGPU inference path would require custom prompt engineering or model adaptation
- [Optimized for English; other languages experimental](https://mistral.ai/news/voxtral-transcribe-2)

**License:** [Apache 2.0](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

---

## 5. Recommended Architecture for Palette

### Voice Input (STT): Voxtral Realtime via WebGPU

```
┌──────────────────────────────────────────────────────────┐
│  Browser                                                  │
│                                                           │
│  Microphone → Web Audio API → Voxtral Realtime (WebGPU)  │
│                                  ↓                        │
│                          Transcribed text                  │
│                                  ↓                        │
│                    Palette Agent Interface                 │
│                    (send text to resolver)                 │
│                                                           │
│  [All audio processing on-device — nothing leaves browser]│
└──────────────────────────────────────────────────────────┘
          ↕ WebSocket / HTTP
┌──────────────────────────────────────────────────────────┐
│  Palette Backend (existing Python CLI + Node.js broker)   │
│                                                           │
│  Resolver → Researcher → Architect → Builder → ...        │
│                          ↓                                │
│                   Agent response (text)                    │
└──────────────────────────────────────────────────────────┘
```

### Voice Output (TTS) — Future Phase

When Palette is ready to speak responses back to users, two options:

| Option | Latency | License | Languages | Deployment |
|---|---|---|---|---|
| [Voxtral TTS](https://mistral.ai/news/voxtral-tts) (March 23, 2026) | [70ms model latency](https://mistral.ai/news/voxtral-tts), ~100ms TTFA | [CC BY-NC 4.0](https://www.marktechpost.com/2026/03/28/mistral-ai-releases-voxtral-tts-a-4b-open-weight-streaming-speech-model-for-low-latency-multilingual-voice-generation/) (open weights) | [9 languages](https://mistral.ai/news/voxtral-tts) | API or self-hosted |
| [Rime Arcana v3](https://rime.ai/resources/arcana-v3) | [120ms on-prem](https://rime.ai/resources/arcana-v3) | Proprietary/enterprise | [10–11 languages](https://rime.ai/resources/arcana-v3) | API, on-prem, VPC |

**Note on Voxtral TTS license:** The open-weight release is CC BY-NC 4.0, which prohibits commercial use. For commercial Palette deployments, you'd use the [Mistral API ($0.016/1k chars)](https://mistral.ai/news/voxtral-tts) or license Rime. For open-source/non-commercial use, self-hosting is an option.

### Full Voice Pipeline (Future State)

```
User speaks → Voxtral Realtime WebGPU (browser, Apache 2.0)
                    ↓
            Transcribed query text
                    ↓
            Palette agents process query
                    ↓
            Agent response text
                    ↓
         Voxtral TTS API  or  Rime Arcana v3
                    ↓
           Audio played in browser
```

This architecture keeps audio *input* fully on-device (privacy, zero server cost) while using an API only for the *output* voice synthesis where privacy concerns are lower (it's Palette's response, not the user's voice).

---

## 6. Implementation Path

### Phase 1: Fork the Voxtral WebGPU Demo (Week 1)

1. **Clone the [Hugging Face Space](https://huggingface.co/spaces/mistralai/Voxtral-Realtime-WebGPU)** — it contains a complete working implementation of Voxtral Realtime running in-browser via Transformers.js + WebGPU.
2. **Strip the demo UI** and extract the core STT pipeline:
   - Model loading and caching (~2.8 GB, one-time download)
   - Web Audio API microphone capture
   - WebGPU inference with streaming token output
3. **Add a loading state** — first-time users will wait for the ~2.8 GB model download. Show progress and cache status. Subsequent loads are instant from browser cache.
4. **Test on target browsers:**
   - Chrome/Edge: full WebGPU support ✅
   - Safari: partial WebGPU (test thoroughly)
   - Firefox: limited WebGPU (may not work; document as unsupported)

### Phase 2: Integrate with Palette (Week 2)

1. **Build the bridge:** Transcribed text from Voxtral → Palette's resolver agent. This is a simple text handoff — the STT output is a string, the resolver accepts natural language input.
2. **Wire up the Node.js broker:** Palette's existing peer broker can receive transcribed text the same way it receives CLI input. The browser UI sends transcribed queries over WebSocket.
3. **Handle partial transcripts:** Voxtral Realtime emits incremental text as the user speaks. Decide on UX: show live transcription, or buffer and send on silence detection / button press.

### Phase 3: Vocabulary Optimization (Week 3)

1. **Application-layer vocabulary hints:** Since in-browser WebGPU doesn't expose Voxtral's API-level context biasing, implement a lightweight post-processing layer:
   - Maintain a dictionary of Palette-specific terms (agent names, model names, API terms)
   - Apply fuzzy matching / correction on transcription output
   - Example: "resolver" misheard as "resolve her" → auto-correct to "resolver"
2. **Alternatively, proxy through Mistral API** for queries where vocabulary accuracy is critical — this adds server dependency but gains [context biasing (up to 100 terms)](https://mistral.ai/news/voxtral-transcribe-2) and potentially better accuracy.

### Phase 4: Voice Output (Optional, Week 4+)

1. Integrate [Voxtral TTS API](https://mistral.ai/news/voxtral-tts) or [Rime Arcana v3](https://rime.ai/resources/arcana-v3) for agent responses
2. Implement streaming audio playback in browser
3. Add voice selection and language preferences

---

## 7. Tradeoffs & When to Reconsider

### Known Tradeoffs of the Voxtral Realtime Approach

| Tradeoff | Impact | Mitigation |
|---|---|---|
| **2.8 GB model download** | Poor first-load experience on slow connections | Browser caching makes subsequent loads instant; show download progress; consider offering a "text-only" mode while model loads |
| **WebGPU browser requirement** | Excludes Firefox users and older browsers | Chrome/Edge cover ~75% of desktop users; provide graceful fallback to text input |
| **No native context biasing in local mode** | Domain terms may be misrecognized | Post-processing dictionary; optional Mistral API proxy for high-accuracy needs |
| **WER gap vs. Granite** | 8.72% avg vs. 5.52% (Granite) on benchmarks | Voxtral's English WER is ~4.9% at 480ms, competitive for conversational input; Granite's edge is larger on noisy/accented audio |
| **4B params in browser** | Requires decent GPU (not mobile-friendly) | [Granite WebGPU demo needs only ~1.4 GB](https://huggingface.co/spaces/webml-community/granite-4.0-1b-speech-webgpu); Voxtral needs more; target desktop browsers |

### When to Switch to Granite

- Palette adds a **Python server component** anyway (e.g., for agent orchestration), making a vLLM backend low-cost to add
- **Keyword biasing** becomes critical and post-processing can't reliably fix domain vocabulary errors
- **Accuracy requirements tighten** (e.g., Palette is used for medical or legal dictation where WER matters more)
- **Offline/edge server** deployment is needed (no browser, embedded system)

### When to Add Rime

- Palette wants **voice output** — agents speaking responses to users
- **Enterprise compliance** requirements (SOC 2, HIPAA) mandate a certified TTS vendor
- **Voice quality** matters — Rime's [94+ voices with paralinguistic features](https://rime.ai/resources/arcana-v3) are more natural than current open-source TTS options

### Alternative Not Evaluated: Whisper.js via WebAssembly

For completeness: [OpenAI's Whisper](https://github.com/openai/whisper) can also run in-browser via WebAssembly (whisper.cpp compiled to WASM). It's a viable fallback if WebGPU is unavailable, but it's batch-mode (not streaming), slower than WebGPU inference, and lacks Voxtral's native streaming architecture. Worth keeping as a fallback path for browsers without WebGPU support.

---

## Sources

All claims in this document link to their primary sources inline. Key references:

- [IBM Granite 4.0 1B Speech — HuggingFace Model Card](https://huggingface.co/ibm-granite/granite-4.0-1b-speech)
- [Voxtral Mini 4B Realtime 2602 — HuggingFace Model Card](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)
- [Voxtral Realtime WebGPU Demo — HuggingFace Spaces](https://huggingface.co/spaces/mistralai/Voxtral-Realtime-WebGPU)
- [Voxtral Transcribe 2 Announcement — Mistral AI](https://mistral.ai/news/voxtral-transcribe-2)
- [Voxtral TTS Announcement — Mistral AI](https://mistral.ai/news/voxtral-tts)
- [Rime Arcana v3 Announcement — rime.ai](https://rime.ai/resources/arcana-v3)
- [Rime on Together AI — together.ai](https://www.together.ai/blog/rime-arcana-v3-turbo-and-rime-arcana-v3-now-available-on-together-ai)
- [Granite Speech WebGPU Demo — HuggingFace Spaces](https://huggingface.co/spaces/webml-community/granite-4.0-1b-speech-webgpu)
- [Transformers.js Voxtral Integration — Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1rqz53r/voxtral_webgpu_realtime_speech_transcription/)
- [Palette Repository — GitHub](https://github.com/pretendhome/palette)
