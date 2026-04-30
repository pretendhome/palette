# Voice — Multilingual Agent Voice Evaluation & Design

Tools and research for evaluating, comparing, and designing voice experiences across languages and providers.

## Voice Evaluation Workbench

**[Live Demo](https://pretendhome.github.io/palette/voice-workbench/)** | [MVP Spec](VOICE_EVALUATION_WORKBENCH_MVP.md)

A multilingual tool for comparing, scoring, and choosing the right AI agent voice for each customer journey stage.

- **3 journey stages**: Acceptance (first-impression trust), Resolution (clear problem-solving), Satisfaction (confident close)
- **4 languages**: English, French, Spanish, Portuguese — with native-speaker voices per language
- **Structured rubric**: Naturalness, Trust, Cultural Fit, Brand Fit, Clarity — weighted scoring
- **TTFA measurement**: Time to First Audio per voice variant
- **Locale watchouts**: Curated cultural notes per language
- **Exportable scorecard**: Markdown decision artifact documenting voice selection rationale

## Voice Hub (peers/hub/)

Multi-agent voice interface connecting 5 LLM agents through voice in 4 languages. Rime Arcana v2 TTS, Whisper local STT, sentence-boundary streaming for sub-700ms first audio. Every query classified through the 121-node taxonomy and grounded in the knowledge library before the agent responds.

## Research

- [Alpine Voice Infrastructure Intelligence](ALPINE_VOICE_INTELLIGENCE.md) — Technical analysis of Alpine AI's voice stack, TTS providers, evaluation methodology, and Voice Sims architecture
