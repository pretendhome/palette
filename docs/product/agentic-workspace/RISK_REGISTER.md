# Mission Control Risk Register

| Risk | Likelihood | Impact | Mitigation |
| :--- | :---: | :---: | :--- |
| **Audio Hardware Friction** | High | Critical | Fallback to text input immediately if `arecord` fails. |
| **Oil KL Depth Gap** | High | Medium | Assign Perplexity (Argy) to a 2-hour research sprint in Week 0. |
| **Claude Code Setup** | Medium | High | Script the Node/Dependency install into `./start.sh` with clear status bars. |
| **One-Way Door Error** | Low | Critical | Human-in-the-loop gate mandatory for all decision log appends. |
| **Voice Latency** | Medium | Medium | Use local `faster-whisper` baseline; avoid cloud transcription for core loop. |
