# Mission Canvas — Semantic Blueprint (RIU-001)

**Status**: PROPOSAL (Awaiting human.operator and Crew ACK)
**Lead**: Gemini CLI (UNVALIDATED)
**Archetype**: Small Business Retail (Rossi)
**Reference**: `implementations/retail/retail-rossi-store/`

## 1. Problem: Information Asymmetry
Small retailers (Rossi) possess high-value local data (tax returns, store photos, business plans) but lack the analytical bridge to map this data to competitive advantages (Grants, Drops, Optimizations). The goal is to evolve the existing **Telegram Relay V1** into a visual **Mission Canvas** workspace that extracts signals locally with zero PII leakage.

## 2. Relay Plan (Iteration 1 Turn)
- **Mistral (Convergence Specialist)**: RIU-001. Review the existing `rossi_bridge.py` and propose a multi-turn conversational intake that builds trust for local file access.
- **Kiro (Lead Builder)**: RIU-011. Research the feasibility of a local-first PDF/CSV "Signal-Only" schema that extends the `relay_store.py` logic.
- **Claude Code (Finisher)**: RIU-081. Audit the proposed data flow for "One-Way Door" security risks, specifically around the GitHub Publish path.
- **Gemini (Specialist)**: RIU-505 & RIU-500. Close the Knowledge Library gaps for Voice Modality and Multimodal pipeline design to support visual evidence.

## 3. Constraints (Mandatory)
- **Local-First**: No PII leaves the hardware (File-based boundary).
- **Traceability**: All decisions logged in `projects/rossi-mission/decisions.md`.
- **Maturity**: Every artifact starts as UNVALIDATED. 10 consecutive successes required for WORKING status.

## 4. Success Metrics
- 0 failures in `total_health_check.py` Section 8.
- Successful PII-free extraction of [REVENUE_SIGNAL] from dummy Rossi data.
- Average convergence velocity < 5 turns for new onboarding.
