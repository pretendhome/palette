# Palette People Library v1.1

**Version**: 1.1
**Date**: 2026-02-24
**Status**: CURRENT — supersedes v1.0
**Agent**: Yuty (enrichment) + Argy (web research)
**Source**: v1.0 + Phase 1 web enrichment pass

---

## What Changed

### Enrichment (all 18 original profiles)
- All 18 profiles now have validated `signal_quality` ratings
- 13 profiles enriched with full web research (new tools, metrics, sources)
- 5 profiles enriched with updated data (PERSON-012 to 016)
- New fields added: `perplexity_enrichment_status`, `enrichment_date`, `enrichment_notes`

### Signal Quality Changes

| Profile | v1.0 | v1.1 | Reason |
|---|---|---|---|
| PERSON-002 Anisha Jain | high | **low** | No independently indexed content; derivative of Ruben |
| PERSON-004 Maria Zhanette Yap | medium | **low** | Community manager; minimal footprint |
| PERSON-011 Joel Nordström | medium | **high** | AI treasury agents launch Feb 2026; major customers added |
| PERSON-013 Victoria Liang | medium | **low** | CORRECTION: Not CTO. Product Marketing Lead. Actual CTO is Sahaj Garg |

### New Profiles (4 from watch list)

| ID | Name | Signal | Cluster | Unique coverage |
|---|---|---|---|---|
| PERSON-019 | Andrej Karpathy | high | frontier_ai_engineering | Paradigm-setter (vibe coding, agentic engineering) |
| PERSON-020 | Chip Huyen | high | frontier_ai_engineering | Production ML systems, AI engineering architecture |
| PERSON-021 | Matthieu Lorrain | high | ai_production_commercial | Google DeepMind creative insider |
| PERSON-022 | PJ Accetturo | high | ai_production_commercial | AI-native advertising with real cost benchmarks |

### Stub Resolutions

| ID | Name | Action |
|---|---|---|
| PERSON-007 Filip Mark | Promoted to full profile | Creandum AI portfolio (10 companies mapped) |
| PERSON-017 Pablo Palafox | Promoted to full profile | HappyRobot CEO, a16z-backed, $44M Series B |
| PERSON-018 Lazar Jovanovic | Archived | Derivative Lovable signal, no unique coverage |

### New Clusters (2)
- `frontier_ai_engineering`: Karpathy + Chip Huyen
- `ai_production_commercial`: Matthieu Lorrain + PJ Accetturo

---

## By the Numbers

| Metric | v1.0 | v1.1 |
|---|---|---|
| Total profiles | 18 | 21 |
| Fully enriched | 14 | 21 |
| Stubs | 4 | 0 |
| Archived | 0 | 1 |
| Clusters | 5 | 7 |
| HIGH signal profiles | 7 | 13 |
| MEDIUM signal profiles | 5 | 4 |
| LOW signal profiles | 0 | 3 |
| Unvalidated | 6 | 0 |
| Intelligence flags | 0 | 10 |

---

## Key Intelligence Flags

1. **Krea.ai double signal** — in both Olivia Moore's AI stack AND Creandum portfolio
2. **Vercel AI Gateway vs nexos.ai** — direct competitors routing 100+ LLM endpoints
3. **Ruben Hassid → Claude** — newsletter shift from ChatGPT to Claude (consumer adoption signal)
4. **Wispr Flow validated** — $700M valuation, $10M ARR, 80% 6-month retention
5. **MASSIVE Studios + Roger Avary** — VFX cost $5K/min vs $1M/min (service routing gold)
6. **Victoria Liang correction** — actual Wispr CTO is Sahaj Garg (consider adding in v1.2)

---

## Watch List Status

- **Promoted (4)**: Karpathy, Chip Huyen, Matthieu Lorrain, PJ Accetturo
- **Hold for Phase 2 (1)**: Greg Isenberg (3/5 — overlaps VC cluster)
- **Not promoted (5)**: Tatiana Tsiguleva, Wyndo Mitra Buwana, Rory Flynn, Simon Meyer, David Blagojevic

---

## What's Next

- **Phase 2**: Service routing completion for 37 `both` RIUs
- **v1.2 candidates**: Sahaj Garg (Wispr CTO), Greg Isenberg (pending Phase 2)
- **Company library updates**: Add Krea, Granola, Julius AI, HappyRobot to company signals
