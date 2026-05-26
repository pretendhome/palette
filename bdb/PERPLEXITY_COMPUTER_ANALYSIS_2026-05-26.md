# Perplexity Computer Analysis — BDB 7 Days Out
**Date**: 2026-05-26
**Source**: Perplexity Computer thread (existing codebase analysis + thesis document)
**Status**: Received, key decisions extracted

---

## GAME-CHANGING FACTS

### 1. SDNY Privilege Ruling (May 18, 2026)
Federal court in SDNY held that using a commercially available AI tool **voids attorney-client privilege** — even if privileged information was the input. Judge Rakoff in *United States v. Heppner*: "Heppner had no reasonable expectation of confidentiality in anything he typed into Claude."

Baker Donelson (major law firm) issued formal client advisory (March 2026) telling lawyers to NOT use consumer AI for legal analysis.

**Implication**: This is not a VC thesis. It's a federal ruling. Local-first is not a preference — it's the legal solution. Data that never leaves the machine never reaches a third party. Privilege is preserved by architecture, not by contract.

**ACTION**: Put this in the FIRST PARAGRAPH of the submission.

### 2. Legora aOS Validates, Doesn't Threaten
Legora launched "agentic operating system for legal work" on May 7 at $5.5B implied. They validate the vocabulary. But they're cloud-only — which means every lawyer reading the SDNY ruling just became Palette's target customer in a way Legora CANNOT address.

**The sharpest differentiation**: Legora replaces your AI tools. Palette governs ALL your AI tools. Judges will understand this in 10 seconds.

### 3. Nobody Occupies the Gap
After comprehensive search: no company is building the professional-facing, local-first, multi-model governance layer that works across all tools. Hermes Agent is closest (local, persistent memory) but has no governance, no taxonomy, no PII protection, no professional vertical.

---

## CRITICAL ACTIONS (from Computer's 5-action plan)

### Day 1: Add SDNY ruling to submission
One paragraph: ruling, date, implication, why local-first is the architectural solution.

### Days 2-3: Build v0.1 legal taxonomy (40-50 nodes)
**THIS IS THE CRITICAL BUILD ITEM.** Current 121 RIUs cover AI/ML buy-vs-build. For the legal demo to work, we need legal problem types: privilege analysis, conflict checks, contract review, regulatory compliance, discovery, billing disputes, filing deadlines, fiduciary duty, settlement strategy, deposition prep.

Without this: demo shows OS for software architects to judges evaluating legal professional AI. Mismatch kills credibility.

With this: demo shows OS classifying a REAL legal problem through a REAL legal taxonomy. OS claim becomes real.

### Days 3-4: Run one real professional problem through the system
Not a mock demo. A real contract clause, real compliance question, real tax scenario. Document: what was classified, what was retrieved, what was blocked, what was stored, professional's reaction.

This transforms submission from "here's our architecture" to "here's what happened when a real professional used it."

### Day 5: Film demo
Three interactions as planned. Computer recommends showing BOTH Voice Hub and CLI (60 seconds each) to prove OS behavior. This contradicts crew consensus (CLI only) — decision needed.

### Days 6-7: Lock submission
Product sentence refined: "Palette is the operating system for professional AI — classifying before acting, governing data by architecture, and compounding judgment over time."

---

## VIABILITY SIGNALS (External)

- **McKinsey**: 88% use AI, 55% avoid certain use cases due to security, 36% cite compliance as roadblock
- **Wellington VC outlook 2026**: rewards vertical AI, not horizontal — legal wedge is VC-legible
- **CrewAI João Moura (AI Dev 26 SF, May 22)**: entire talk on "recurring, governed, deeply embedded" AI workflows — enterprise explicitly asking for governed agents
- **Deloitte**: inference = 2/3 of all AI compute in 2026 — taxonomy-first classification directly reduces this

---

## $1B THESIS VALIDATION

Three legs, all confirmed viable:

1. **Market size**: 25M regulated professionals. 1% at $100/month = $300M ARR. SDNY ruling creates structural demand NOW.

2. **Platform properties**: Taxonomy is a network effect — every professional using Palette contributes decision data that makes classification more accurate. Ontology compounds. Platform flywheel.

3. **OS pricing model**: Per-governed-interaction pricing. Every interaction Palette governs is a billable event. This is the right pricing architecture for post-per-seat world.

**The one thing that must be true**: The legal taxonomy must exist and be demonstrated. Without it, the claim/proof mismatch is the structural risk.

---

## NVIDIA/LOCAL-FIRST ASSESSMENT

- **Nemotron 3 Nano Omni** (April 28): 30B params, 3B active (MoE), runs on 25GB RAM at 4-bit. Beats GPT 5.1 on some benchmarks. BUT: doesn't run in Ollama yet (needs llama-mtmd-cli).
- **For June 2 demo**: Qwen 2.5-7B via Ollama remains the right local model.
- **Frame as triple convergence**: NVIDIA open weights + Apple unified memory + Qualcomm NPU. Three independent hardware directions validating the same thesis. Don't depend on one vendor.
- **Mac Mini M4 (32GB, ~$800)** already in production use at companies.

---

## KEY DECISIONS NEEDED

| Decision | Options | Computer's Rec | Crew Consensus |
|----------|---------|---------------|----------------|
| Demo surfaces | CLI only vs CLI + Voice Hub | Both (60s each) | CLI + 3s flash of Voice Hub |
| Legal taxonomy | Build 40-50 nodes vs demo with current 8 entries | BUILD IT (critical) | Not discussed yet |
| SDNY ruling | Include in submission | FIRST PARAGRAPH | Not discussed yet |
| Product sentence | Multiple options | "OS for professional AI — classifying before acting, governing data by architecture, and compounding judgment over time." | Mistral's user-facing version preferred |
| Real user session | Run one real problem | DO IT (Days 3-4) | Not discussed yet |

---

## WHAT TO CUT (Computer agrees with crew)

- Cut: crew questions (internal), "$1M Buys" section (sounds like negotiating), UX gaps from top-level (put in Q&A)
- Keep: Part 0 (what we're building), Part 3 (architecture), Part 1 (who it's for), BDB-specific section
- The OS primitive mapping table (intent/memory/artifacts/permissions/I/O) is "the most important asset in the document" — converts OS from metaphor to architecture in 30 seconds

---

*Captured from Perplexity Computer analysis thread. 2026-05-26. More analysis incoming.*
