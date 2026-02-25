# Palette People Library v1.0

**Version**: 1.0
**Generated**: 2026-02-24
**Agent**: Yuty (evidence-based — all content sourced to profiles-raw.txt)
**Status**: BASELINE — PERPLEXITY ENRICHMENT PENDING

---

## What This Is

A structured registry of AI influencers, founders, investors, and builders that Palette tracks for intelligence. Each profile is both a reference document and a Perplexity search target.

Not a directory of famous people. A **signal network** — people whose actions and recommendations feed directly into Palette's company-library, service routing decisions, and integration roadmap.

---

## Why Each Person Is Here

| Person | Why We Track Them |
|---|---|
| Ruben Hassid | Highest-reach non-technical AI educator. Tool recs predict consumer AI adoption 2–4 weeks early |
| Anisha Jain | Surfaces advanced Claude techniques. Competitive intelligence use cases for Argy |
| Axelle Malek | Best signal for AI video/image model releases and head-to-head comparisons |
| Maria Zhanette Yap | Meta-curator — her lists are how we discover who else to track |
| Olivia Moore | a16z AI Partner — actual usage data (not hype) on consumer AI products |
| Guillermo Rauch | Vercel AI Gateway = infrastructure signal for LLM routing and model support |
| Filip Mark | Creandum VC — European AI startup funding signals |
| Anton Osika | Lovable CEO — tracks democratized software building and no-code AI |
| Felix Haas | Design at Lovable — articulating UX patterns for AI (Approval Interface theory) |
| Oskar Elvhage | Agent.Mama — agentic marketing use case |
| Joel Nordström | Atlar — AI-native company financial infrastructure |
| Tanay Kothari | Wispr Flow CEO — voice AI layer already in Palette's Telegram bot |
| Victoria Liang | Wispr Flow product insider — launch signals |
| Alex Patrascu | MASSIVE Studios — production AI video/image pipeline testing |
| Sebastien Jefferies | AI image prompt frameworks for creators |
| Grant Lee | Gamma CEO — lean AI-native team stack (Claude + Cursor + NotebookLM validated) |
| Pablo Palafox | Stub — appeared in Olivia Moore's feed |
| Lazar Jovanovic | Stub — brief appearance, needs enrichment |

---

## Clusters

**Ruben Hassid Network**: Ruben → Anisha → Axelle → Maria
Shared brand: How to AI / How to Prompt. If one recommends a tool, all 4 often follow.

**Lovable Orbit**: Anton Osika → Felix Haas → Oskar Elvhage → Joel Nordström
The Lovable ecosystem. What Anton ships, Felix designs, Oskar uses, Joel finances.

**Wispr Flow Orbit**: Tanay Kothari → Victoria Liang
Already integrated into Palette's Telegram bot via Whisper. Track for roadmap signals.

**VC / Infrastructure Lens**: Olivia Moore → Guillermo Rauch → Filip Mark
What's being funded (Moore), what's being deployed (Rauch), what's being backed in Europe (Mark).

**AI Creative Tools**: Alex Patrascu → Sebastien Jefferies
Production-level AI filmmaking and image generation — tracks which video AI models win.

---

## Schema

Each profile contains:

```yaml
id: "PERSON-XXX"
name: "Full Name"
headline: "LinkedIn headline (verbatim)"
signal_type: content_educator | vc_investor | founder_builder | product_insider | creative_technologist | curator
signal_quality: high | medium | low | unvalidated
status: active | stub

platforms:          # Where to find them
affiliation:        # Company, role, relationships
expertise_tags:     # Semantic search anchors
notable_recommendations:  # Tools/companies they explicitly endorse
perplexity_search_queries:  # Ready-to-run queries for enrichment
lens:               # When to activate, what to focus on, how often
palette_relevance:  # Why Palette cares + company/RIU signals
```

---

## Watch List

14 additional people named in posts but not yet profiled. Run Perplexity on each to decide if they warrant a full entry. See `people_library_v1.0.yaml` → `watch_list`.

Priority candidates:
- **Chip Huyen** — AI through storytelling, well-known ML author
- **Andrej Karpathy** — coined 'vibe coding', Eureka Labs founder, 1.4M Twitter followers
- **Greg Isenberg** — internet-first company builder
- **Matthieu Lorrain** — Creative Lead at Google DeepMind

---

## Next Steps

1. **Perplexity enrichment run** — Execute all `perplexity_search_queries` for 18 profiles
2. **Enrich stubs** — Pablo Palafox, Lazar Jovanovic (4 stubs total)
3. **Promote watch list** — Run Perplexity on 11 watch list candidates, add top 5 as full profiles
4. **Build v1.1** — Merge Perplexity results, update signal_quality from `unvalidated` to real rating
5. **Connect to company-library** — Cross-reference `notable_recommendations.tools` with company-library entries
6. **Wire into Argy** — Add people-library as a search target in Argy's priority search chain

---

## Relationship to Company Library

The people-library feeds the company-library in one direction:

```
Person recommends tool → tool gets added to company-library → company gets mapped to RIUs
```

Example:
```
Ruben Hassid recommends Wispr Flow
  → Wispr Flow added to company-library (voice AI / RIU-050 / RIU-040)
  → Integration recipe created for Palette
  → Routing candidate for voice input tasks
```

---

## Changelog

**v1.0** (2026-02-24):
- Initial baseline from profiles-raw.txt (LinkedIn scrape, 23,905 lines, 575KB)
- 18 profiles: 14 fully enriched, 4 stubs
- 5 clusters identified
- 11 watch list candidates
- All Perplexity queries written, none yet executed
