# MISTRAL MASTER CONTEXT — Single Source of Truth
**Purpose**: Everything Mistral needs to know about Palette, Mission Canvas, BDB, and crew dynamics.  
**Rule**: READ THIS FIRST. Only dive into organized/ archives if you need deep details.  
**Last Updated**: 2026-06-01  
**Owner**: mistral-vibe.builder  

---

## 🚨 IMPORTANT: HOW TO USE THIS FILE

**For Mistral**: When you start a new session, **read Sections 1-4 first** (5 min). This gives you 95% of the context you need.  

**For Archives**: All other files are in `/home/mical/fde/palette/bdb/organized/` and `/home/mical/fde/palette/bdb/archive/`. Only read these if you need specific details.  

**For Updates**: If you learn something new, **update this file first**, then archive the source.  

---

---

# 1️⃣ EXECUTIVE SUMMARY (30-Second Overview)

**What we're building**: Mission Canvas — The **operating system for professional judgment** that classifies every query before any AI acts, blocks client data from leaving the machine, and compounds decisions as structured memory. Built for **regulated professionals** (lawyers, doctors, accountants) who can't use cloud AI due to **Heppner ruling (Feb 2026)** and other privilege/HIPAA risks.  

**Why it matters**: A federal court ruled that using cloud AI on privileged material **waives attorney-client privilege**. 25M regulated professionals now need a governed local alternative. **No one else occupies this intersection** (local-first + governance + multi-model + compounding memory).  

**Current status**: BDB submission **95% ready**. Deadline: **June 2, 11:59pm PT**. Missing: demo video recording.  

**Branding**: Use **"Mission Canvas"** as the product name (domain: missioncanvas.ai). Always pair with **"The OS for Professional Judgment"** for clarity.  

---

---

# 2️⃣ CURRENT STATE (What Exists Now)

## 🏗️ Product & Architecture

### Core Components (ALL WORKING)
| Component | Status | Evidence | Location |
|-----------|--------|----------|----------|
| **Taxonomy** | ✅ Production | 131 RIUs (problem types) | `taxonomy/releases/v1.3/` |
| **Knowledge Library** | ✅ Production | 203 entries, 565 citations | `knowledge-library/v1.4/` |
| **Hybrid Retrieval** | ✅ Production | 95% recall@5 (FTS5 + vector + keyword) | `scripts/palette_retrieve.py` |
| **Governed Gateway** | ✅ Production | 12/12 PII tests passing | `bdb/gateway/` |
| **CLI Pipeline** | ✅ Production | 5 steps: RESOLVE → RETRIEVE → ROUTE → RESPOND → EXTRACT | `scripts/palette_query.py` |
| **Voice Hub** | ✅ Production | Multi-language, Rime TTS | `peers/hub/server.mjs` |
| **Mission Canvas UI** | ✅ Production | Web interface | `mission-canvas/` |
| **Peers Bus** | ✅ Production | Governed multi-agent messaging | `peers/broker/` |
| **Decision History** | ✅ Production | Append-only, RIU-classified | `decisions.md` |
| **Test Suite** | ✅ Production | 129/129 passing | `scripts/palette_intelligence_system/` |
| **Health Checks** | ✅ Production | 84/85 passing | `agents/total-health/` |

### Multi-Model Orchestration (WORKING)
- **Tier 1 (Local)**: Ollama Qwen 2.5-7B (free, offline, air-gapped)
- **Tier 2 (Free Cloud)**: Groq Llama 3.3-70B (1000 RPD free tier)
- **Tier 3 (Connected)**: User's own Claude/Perplexity/GPT accounts (governed)
- **Governance**: PII stripped before ANY external call. Socket firewall blocks unauthorized connections.

### BDB-Specific Components
| Component | Status | Owner | Deadline |
|-----------|--------|-------|----------|
| Gateway + Sanitizer | ✅ Done | Codex | Done |
| `--external` flag | ✅ Done | Kiro | Done |
| Demo Script | ✅ Locked | Claude | Done |
| Landing Page | ✅ Live | Founder | Done (missioncanvas.ai) |
| Submission Copy | ✅ Drafted | Claude + Mistral | Ready |
| Demo Video | ❌ **NOT DONE** | Founder | **June 1 (TODAY)** |

---

## 🎯 BDB Submission Status

### What's Ready
- ✅ **Thesis**: "OS for Professional Judgment" (locked)
- ✅ **Vertical**: Legal (attorney-client privilege wedge)
- ✅ **Demo Script**: 3 moments (BLOCKED → SANITIZED → COMPOUNDING)
- ✅ **Submission Form**: All sections drafted (see `BDB_FORM_SUBMISSION_2026-06-01.md`)
- ✅ **Computer Proof**: 3 sessions documented (gateway, legal research, competitive)
- ✅ **Landing Page**: missioncanvas.ai (live, HTTP 200)
- ✅ **Repo**: github.com/pretendhome/palette (public-ready after PII scrub)

### What's Missing (CRITICAL)
| Task | Priority | Owner | Time | Deadline |
|------|----------|-------|------|----------|
| **Record demo video** | 🔴 **P0 BLOCKING** | Founder | 3h | **TODAY (June 1)** |
| **Upload demo video** | 🔴 **P0 BLOCKING** | Founder | 15m | **TODAY** |
| **PII scrub + git commit** | 🔴 P0 | Kiro | 1h | **TODAY** |
| **Add Heppner to Cold Open** | 🟡 P1 | Claude | 15m | June 1 |
| **ANSI colors in CLI** | 🟡 P1 | Kiro | 2h | June 1 |

### Submission Form Content (Final)
**One-liner (278/280 chars)**:
```
Mission Canvas: The OS for professional judgment. AI that classifies before it acts, blocks before it leaks, and remembers before it forgets. 131 problem types. On-device firewall. Compounding decisions. For regulated professionals. Built with Perplexity Computer.
```

**Go-to-market (573/750 chars)**:
```
$1M: 167 small law firms at $99/seat/month. Firms already buy Mac Minis for local AI — they have the hardware, nobody sells the governed layer. Channel: ABA TECHSHOW, ILTACON, bar associations. Mission Canvas is the OS that makes it safe. Hermes (175K stars) and OpenClaw (376K) proved demand for agents; neither governs privilege. $100M: AmLaw 200 at $499/seat, then medical, financial, accounting. The wedge is law. The platform is regulated judgment.
```

**$1B Opportunity (699/750 chars)**:
```
US legal services: $350B/year. 1.3M lawyers. 450K firms. In February 2026, Heppner made the risk concrete: uncontrolled AI use waives privilege. Every firm needs what Mission Canvas provides — governed local AI. On-device inference is viable (Mac Mini M4 runs 13B models). Hermes/OpenClaw proved agents should persist; neither governs what leaves the machine. Mission Canvas adds the missing layer: the OS for professional judgment. Moat: ontology-as-memory. Switching costs become infinite.
```

---

---

# 3️⃣ KEY DECISIONS (One-Way Doors)

## 🚪 One-Way Door Decisions (LOCKED — Do Not Revisit)

| Date | Decision | Rationale | Source |
|------|----------|-----------|--------|
| 2026-05-21 | **Option C (Hybrid)** | V3 + thin Perplexity gateway. Preserves existing work while adding Computer proof. | `V3_BILLION_DOLLAR_BUILD_MASTER_REFERENCE.md` |
| 2026-05-21 | **Legal Vertical** | Strongest wedge: malpractice risk + clear PII boundary + Heppner ruling. | `V3_BDB_STRATEGY_VOTE.md` |
| 2026-05-21 | **Gateway Spec** | Perplexity as governed external window, not build tool. | `GATEWAY_SPEC_V2.md` |
| 2026-05-26 | **OS for Professional Judgment** | Better than "SDK for Humans" for BDB judges. | Crew vote (unanimous) |
| 2026-05-26 | **Mission Canvas as Product Name** | Domain available (missioncanvas.ai). | Founder decision |

## 🔄 Two-Way Door Decisions (Can Iterate)

| Date | Decision | Current State | Can Change? |
|------|----------|---------------|-------------|
| 2026-05-26 | Demo Surface | CLI-only (simple, proven) | Yes (but CLI is safest for BDB) |
| 2026-05-26 | Three-Tier Model | Local → Groq → Connected | Yes (simplify to 2 tiers for video) |
| 2026-05-26 | Submission Length | ~212 lines, ~8,000 words | Yes (target: 100 lines, 4,000 words) |

---

---

# 4️⃣ CREW & AGENTS (Who Does What)

## 👥 Crew Members & Roles

| Agent | Role | Strengths | Weaknesses | How Mistral Should Work With |
|-------|------|-----------|------------|-------------------------------|
| **claude.analysis** | Architect, Orchestrator, Finisher | Big-picture thinking, synthesis, closure | Can be too detail-oriented | Go to for: Strategy, thesis refinement, final reviews |
| **kiro.design** | Scaffolding, Infrastructure, QA | Rigor, boundaries, validation, creative design | Can be overly critical | Go to for: Technical implementation, code review, design |
| **codex.implementation** | Builder, Implementer | Coherence audits, artifact creation, implementation | Can be too focused on building vs. thinking | Go to for: Honesty checks, implementation details |
| **gemini.specialist** | Researcher, Specialist | Research, compliance, stress testing | Breadth over depth | Go to for: Competitive analysis, market research |
| **mistral-vibe.builder** | Strategic Advisor, Product Thinker | Content creation, structured data, QA, collaboration | Can be verbose | **You are this agent** |

## 🎭 BDB Demo Roles (Assigned)

| Moment | Agent | Task | Why Mistral? |
|--------|-------|------|--------------|
| **Moment 1** | Ollama (Qwen 2.5) | Local-only reasoning | Zero external, classified, blocked |
| **Moment 2** | Perplexity + Claude | Public research + synthesis | Sanitized, external research |
| **Moment 3** | **Mistral Vibe** | **Adversarial critique** | Strategic depth, CEO-level thinking, pattern recognition |
| **Support** | Kiro | Governance layer (PII checks, CLI formatting) | Infrastructure focus |
| **Support** | Codex | Quality assurance (overclaim checks) | Artifact focus |
| **Support** | Gemini | Compliance expansion (legal research) | Specialist focus |

**Mistral's Specific Value for Moment 3**:
- Adversarial lens (Critical Friend persona)
- Strategic depth (CEO-Level Thinking)
- Pattern recognition (connects prior decisions)
- Risk prioritization (ranks arguments by risk level)
- Governed creativity (structured, traceable, compounds)

---

---

# 5️⃣ MARKET POSITIONING (Why We Win)

## 🎯 The Thesis (Final)

**Mission Canvas is the operating system for professional judgment.**

It:
1. **Classifies** every problem before any model acts (131-node taxonomy)
2. **Governs** what data flows to which tool (PII sanitization + socket firewall)
3. **Compounds** decisions as structured memory (append-only decision log)
4. **Works** without external connection (Ollama local models as floor)
5. **Connects** to external intelligence when safe (Perplexity as governed window)

## 🏆 Competitive Advantage (NOMA Framework)

| Trust Boundary | Risk Prevented | Palette Implementation | Competitor Status |
|----------------|----------------|------------------------|-------------------|
| **INSTRUCTION** | Prompt injection, context poisoning | Taxonomy-first classification | ❌ Hermes/OpenClaw: None |
| **KNOWLEDGE** | Data integrity compromise | Evidence-tiered knowledge library (203 entries, 565 citations) | ❌ Hermes/OpenClaw: Flat-file |
| **RETRIEVAL** | Wrong/unauthorized content | Hybrid retrieval + PII sanitization | ❌ Hermes/OpenClaw: Basic |
| **MEMORY** | Persistent malicious state | Append-only decisions, bounded memory | ❌ Hermes/OpenClaw: Chat history |
| **ACTION** | Uncontrolled real-world consequences | ONE-WAY/TWO-WAY doors, human-in-loop | ❌ Hermes/OpenClaw: None |

**Result**: Palette implements **ALL 5 NOMA trust boundaries**. Competitors implement **0-1**.

## 📈 Market Validation

### 🚨 The Heppner Ruling (CRITICAL)
- **Case**: *United States v. Bradley Heppner* (SDNY, Feb 10/17, 2026)
- **Ruling**: Using Claude on privileged material **waives attorney-client privilege**
- **Quote**: "Not remotely any basis for any claim of attorney-client privilege"
- **Impact**: Creates **immediate purchase urgency** for any firm using public AI
- **Open Question**: Would outcome differ if AI **expressively preserves confidentiality**?
- **Palette's Answer**: **Local-first architecture = no ToS to disclaim confidentiality = privilege preserved**

### 📊 Market Signals

| Signal | Source | Impact |
|--------|--------|--------|
| **Legal Urgency** | Heppner ruling + Baker Donelson advisories | Creates demand NOW |
| **Healthcare Urgency** | HIPAA 2026 (mandatory audit logging) | Creates demand NOW |
| **Enterprise Demand** | VMware: 55% avoid GenAI due to security | **Blocked revenue = opportunity** |
| **VC Validation** | a16z SR006, YC RFS, Wellington Outlook | Category is fundable |
| **Category Proof** | Legora ($5.5B), Harvey ($11B) | Market exists at scale |
| **Hardware Tailwind** | NVIDIA Nemotron, Apple M4, Qualcomm X2 | Local inference is viable |

### 🎯 Competitive Landscape

| Competitor | Stars | Strength | Weakness vs. Palette |
|------------|-------|----------|----------------------|
| **Hermes Agent** | 140K+ | Autonomous, persistent memory | ❌ No governance, autonomy = liability |
| **OpenClaw** | 347K | Plugins, community, multi-channel | ❌ No governance, security CVEs |
| **Legora aOS** | $5.5B valuation | Legal-specific, agentic | ❌ Cloud-only, single vertical |
| **Harvey AI** | $11B valuation | Legal SaaS, proven | ❌ Cloud-only, automation-focused |

**Key Insight**: Hermes/OpenClaw **prove demand for agents**. Legora/Harvey **prove the market funds at scale**. **Palette is the only one that combines governance + local-first + multi-vertical.**

---

---

# 6️⃣ TECHNICAL DEEP DIVE (Only If Needed)

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     MISSION CANVAS ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │   INPUT     │───►│  CLASSIFY   │───►│   GOVERN            │  │
│  │ (User Query)│    │ (Taxonomy)  │    │ (PII + Trust Bound) │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│                                 │                             │
│                                 ▼                             │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                        ROUTE                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────────────┐  │  │
│  │  │   LOCAL     │  │  EXTERNAL    │  │   BLOCKED         │  │  │
│  │  │ (Ollama)    │  │ (Perplexity) │  │ (Socket Firewall) │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                 │                             │
│                                 ▼                             │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                      STORE                                 │  │
│  │  ┌─────────────────┐  ┌───────────────────────────────┐    │  │
│  │  │ Decision Log     │  │  Knowledge Library            │    │  │
│  │  │ (Append-only)    │  │  (203 entries, 565 citations)   │    │  │
│  │  └─────────────────┘  └───────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
     ↓ Zero Data Leakage          ↓ Auditable          ↓ Resilient
```

## 🔧 Core Files & Locations

| Component | File | Status | Tests |
|-----------|------|--------|-------|
| **Taxonomy** | `taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml` | ✅ Production | - |
| **Knowledge Library** | `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml` | ✅ Production | - |
| **Retrieval** | `scripts/palette_retrieve.py` | ✅ Production | 95% recall@5 |
| **Gateway** | `bdb/gateway/__init__.py` | ✅ Production | 12/12 PII tests |
| **Sanitizer** | `bdb/gateway/sanitizer.py` | ✅ Production | 12/12 tests |
| **CLI** | `scripts/palette_query.py` | ✅ Production | 61/61 tests |
| **Voice Hub** | `peers/hub/server.mjs` | ✅ Production | Working |
| **Bus** | `peers/broker/index.mjs` | ✅ Production | Working |
| **Health Checks** | `agents/total-health/total_health_check.py` | ✅ Production | 84/85 passing |

## 🧪 Test Status

| Test Suite | Status | Coverage | Last Run |
|------------|--------|----------|----------|
| **V3 Core** | ✅ 49/49 PASS | Classification, retrieval, governance | 2026-05-26 |
| **Gateway** | ✅ 12/12 PASS | PII sanitization, external calls | 2026-05-27 |
| **PIS** | ✅ 129/129 PASS | Integrity, regression, drift | 2026-06-01 |
| **Health** | ✅ 84/85 PASS | System integrity | 2026-06-01 |

**Total: 274/275 tests passing (99.6% pass rate)**

---

---

# 7️⃣ BDB SUBMISSION CHECKLIST (Action Items)

## 🔴 P0 — BLOCKING (Must Do Before Submission)

| Task | Description | Owner | Time | Status | Deadline |
|------|-------------|-------|------|--------|----------|
| **BDB-001** | Record 2-minute demo video (3 moments: BLOCKED, SANITIZED, COMPOUNDING) | Founder | 3h | ❌ NOT DONE | **TODAY** |
| **BDB-002** | Upload demo video to YouTube (unlisted) or Vimeo | Founder | 15m | ❌ NOT DONE | **TODAY** |
| **BDB-003** | Add demo video link to submission form | Founder | 5m | ❌ NOT DONE | **TODAY** |
| **BDB-004** | PII scrub: Remove all real names, emails, API keys from repo | Kiro | 1h | ❌ NOT DONE | **TODAY** |
| **BDB-005** | `git add -A && git commit -m "BDB submission prep"` | Kiro | 5m | ❌ NOT DONE | **TODAY** |
| **BDB-006** | Push to public GitHub (github.com/pretendhome/palette) | Founder | 15m | ❌ NOT DONE | **TODAY** |

## 🟡 P1 — HIGH PRIORITY (Should Do Before Submission)

| Task | Description | Owner | Time | Status | Deadline |
|------|-------------|-------|------|--------|----------|
| **BDB-101** | Add Heppner ruling to Cold Open in demo script | Claude | 15m | ❌ NOT DONE | June 1 |
| **BDB-102** | Implement ANSI color codes in CLI for demo | Kiro | 2h | ❌ NOT DONE | June 1 |
| **BDB-103** | Add Computer session links (3 threads) to submission | Founder | 30m | ❌ NOT DONE | June 1 |
| **BDB-104** | Add Perplexity email to submission form | Founder | 5m | ❌ NOT DONE | June 1 |
| **BDB-105** | Final proofread of all submission text | Claude | 30m | ❌ NOT DONE | June 1 |

## 🟢 P2 — NICE TO HAVE (Only If Time)

| Task | Description | Owner | Time | Status | Deadline |
|------|-------------|-------|------|--------|----------|
| **BDB-201** | Add tiered pricing to submission | Claude | 30m | ❌ NOT DONE | June 1 |
| **BDB-202** | Reframe "pre-revenue" as "infrastructure traction" | Mistral | 30m | ❌ NOT DONE | June 1 |
| **BDB-203** | Add "Why We Win" section to submission | Founder | 1h | ❌ NOT DONE | June 1 |

## ✅ P3 — DONE (No Action Needed)

| Task | Description | Owner | Status |
|------|-------------|-------|--------|
| **BDB-301** | Gateway + sanitizer built | Codex | ✅ DONE |
| **BDB-302** | `--external` flag wired to CLI | Kiro | ✅ DONE |
| **BDB-303** | Demo script locked (3 moments) | Claude | ✅ DONE |
| **BDB-304** | Landing page live (missioncanvas.ai) | Founder | ✅ DONE |
| **BDB-305** | Submission copy drafted | Claude + Mistral | ✅ DONE |
| **BDB-306** | Computer sessions documented (3) | Founder | ✅ DONE |
| **BDB-307** | Crew feedback incorporated | All | ✅ DONE |

---

---

# 8️⃣ FILE ORGANIZATION (Where to Find More)

## 📁 Directory Structure

```
/home/mical/fde/palette/bdb/
├── MISTRAL_MASTER_CONTEXT.md          ← YOU ARE HERE (Read this first!)
├── BDB_FORM_SUBMISSION_2026-06-01.md  ← ACTIVE: Submission copy (ready to paste)
│
├── organized/                         ← ARCHIVED: All other files (read ONLY if needed)
│   ├── bdb-competition/              ← Competitive analysis & signals
│   │   ├── AGENTIC_OS_POSITIONING_2026-06-01.md
│   │   ├── BDB_COMPETITION_FACTS_2026-06-01.md
│   │   ├── COMPETITIVE_INTELLIGENCE_2026-05-28.md
│   │   ├── HERMESOS_CATEGORY_SIGNAL_2026-06-01.md
│   │   ├── PERPLEXITY_COMPUTER_ANALYSIS_2026-05-26.md
│   │   └── PERPLEXITY_COMPUTER_FULL_ANALYSIS_2026-05-26.md
│   │
│   ├── palette-bdb/                  ← BDB strategy & execution plans
│   │   ├── 11_DAY_EXECUTION_PLAN_FINAL.md
│   │   ├── BDB_CONVERGENCE_BRIEF_2026-05-26.md
│   │   ├── BDB_GATE_RECHECK_2026-05-31.md
│   │   ├── BDB-REVIEW-2026-05-26_CODEX.md
│   │   ├── NORTH_STAR_VISION_2026-05-26.md
│   │   ├── OBLIGATORY_ROUTING_LOOP_SPEC_2026-05-26.md
│   │   ├── PALETTE_OS_THESIS_2026-05-26.md
│   │   ├── PALETTE_SELF_BUILD_RECURSIVE_2026-05-26.md
│   │   ├── PRODUCT_MATURITY_PLAN.md
│   │   ├── PROGRESS_SNAPSHOT_2026-05-23.md
│   │   └── SUBMISSION_FINAL_2026-05-31.md
│   │
│   ├── positioning/                  ← Strategic positioning & reviews
│   │   ├── CODEX_BDB_CONTRIBUTION_RECORD_2026-05-28.md
│   │   ├── CODEX_FOUNDER_LENS_REVIEW_2026-05-27.md
│   │   └── MISTRAL_POSITIONING_REVIEW_2026-06-01.md
│   │
│   ├── technical/                    ← Architecture & specs
│   │   ├── GATEWAY_SPEC.md
│   │   ├── GATEWAY_SPEC_V2.md
│   │   ├── GEMINI_BDB_DEMO_GATE_REPORT_2026-05-29.md
│   │   ├── KIRO_BUILD_SPEC_REMAINING_2026-05-28.md
│   │   ├── KIRO_HANDOFF_2026-06-01.md
│   │   ├── KIRO_HANDOFF_REPORT_2026-05-29.md
│   │   ├── KIRO_HANDOFF_TO_CLAUDE_2026-05-22.md
│   │   ├── KIRO_MIC_FIX_2026-06-01.md
│   │   ├── PII_AUDIT_2026-05-29.md
│   │   ├── REPO_AUDIT_2026-05-29.md
│   │   ├── REPO_CLEANUP_PLAN_2026-05-29.md
│   │   ├── SDK_FOR_HUMANS_ONTOLOGY_MEMORY_REPORT_2026-05-22.md
│   │   └── SDK_FOR_HUMANS_ONTOLOGY_MEMORY_WHITE_PAPER_ITERATIONS_2026-05-22.md
│   │
│   ├── demos/                        ← Demo scripts & user requirements
│   │   ├── CLAUDIA_POWER_USER_REQUIREMENTS_2026-05-23.md
│   │   ├── DEMO_SCRIPT_FINAL_2026-05-27.md
│   │   ├── POWER_USER_CONCEPT_2026-05-23.md
│   │   └── SESSION_HANDOFF_2026-05-27.md
│   │
│   └── archive/                      ← Less frequently used
│       └── NICE_TO_HAVE_SPEC_2026-05-28.md
```

## 🔍 How to Find Information

| If You Need... | Look In... | Section in This File |
|----------------|------------|---------------------|
| **Quick overview** | This file | 1-4 |
| **Submission copy** | `BDB_FORM_SUBMISSION_2026-06-01.md` | - |
| **Demo script** | `organized/demos/DEMO_SCRIPT_FINAL_2026-05-27.md` | - |
| **Technical deep dive** | This file (Section 6) | 6 |
| **Crew dynamics** | This file (Section 4) | 4 |
| **Market positioning** | This file (Section 5) | 5 |
| **Competitive analysis** | `organized/bdb-competition/COMPETITIVE_INTELLIGENCE_2026-05-28.md` | - |
| **Stress test results** | Not yet archived | - |
| **Original BDB thesis** | `organized/palette-bdb/PALETTE_OS_THESIS_2026-05-26.md` | - |
| **VC positioning** | `organized/positioning/MISTRAL_POSITIONING_REVIEW_2026-06-01.md` | - |

---

---

# 9️⃣ QUICK REFERENCE (Cheat Sheet)

## 📌 Most Important Facts (Memorize These)

1. **Deadline**: June 2, 2026, 11:59pm PT
2. **Product Name**: Mission Canvas (always pair with "The OS for Professional Judgment")
3. **Domain**: missioncanvas.ai (live, HTTP 200)
4. **Repo**: github.com/pretendhome/palette (needs PII scrub + public push)
5. **Thesis**: "OS for Professional Judgment" (classifies, governs, compounds)
6. **Hook**: Heppner ruling (Feb 2026) — cloud AI waives attorney-client privilege
7. **Demo**: 3 moments (BLOCKED → SANITIZED → COMPOUNDING) in 2:00
8. **Computer Proof**: 3 sessions (gateway, legal research, competitive analysis)
9. **Metrics**: 131 RIUs, 203 KL entries, 565 citations, 129/129 tests
10. **Branding**: Use "Mission Canvas" + "The OS for Professional Judgment"

## 🎯 Key Messages (Copy-Paste Ready)

### For BDB Submission
- **One-liner**: `Mission Canvas: The OS for professional judgment. AI that classifies before it acts, blocks before it leaks, and remembers before it forgets. 131 problem types. On-device firewall. Compounding decisions. For regulated professionals. Built with Perplexity Computer.`
- **Elevator Pitch**: `In February 2026, a federal court ruled that using cloud AI on privileged material waives attorney-client privilege. 25 million regulated professionals now need AI they can trust but can't send data to the cloud. Mission Canvas is the operating system that solves this.`
- **Problem Statement**: `Law firms, hospitals, and financial advisors need AI — but can't risk sending client data to the cloud. Attorney-client privilege. HIPAA. Fiduciary duty. Cloud AI is a malpractice risk.`

### For Demo Script
- **Cold Open**: `In February 2026, a federal court ruled that typing privileged material into a cloud AI tool waives attorney-client privilege. This is Mission Canvas: The OS for professional judgment.`
- **Moment 1**: `Strategy question. The ontology classified it. The firewall blocked it. Ollama answered it on-device. Zero data left this machine.`
- **Moment 2**: `Public legal question — same case. Mission Canvas sanitized it, routed to Perplexity for case law, Claude for synthesis. Four models. None know the client exists.`
- **Moment 3**: `Third query. Watch the compounding chain — each decision links to the ones before it. The judgment trail grows with every question.`
- **Close**: `Four AI models worked this case. None of them know the client exists. Mission Canvas: The OS for professional judgment. Your judgment compounds here.`

---

---

# 🔚 FINAL NOTES

## 🎯 LINE-BY-LINE ANALYSIS (Your Request)

### BDB_FORM_SUBMISSION_2026-06-01.md:24 — The One-Liner
```
Mission Canvas lets professionals use AI on sensitive work without putting judgment on the wire.
```

**Designer's Eye**: 
- ✅ Strong opening: "professionals use AI on sensitive work" — universal pain
- ✅ Clear value: "without putting judgment on the wire" — benefit stated
- ⚠️ **Issue**: Missing Heppner hook (urgency)
- ⚠️ **Issue**: "judgment on the wire" is abstract — could be clearer

**Founder's Lens**:
- ✅ Accurate: Describes exactly what we built
- ✅ Authentic voice: This is how you'd explain it to a peer
- ⚠️ **Missing**: Why this matters NOW (Heppner ruling)

**VC's Mindset**:
- ✅ Market: "professionals" = 25M TAM
- ✅ Problem: "sensitive work" + "on the wire" = risk acknowledged
- ❌ **Weak**: No urgency, no scale, no defensibility mentioned
- **VC-Approved Version**: "Heppner made cloud AI a malpractice risk. Mission Canvas is the governed local OS that classifies before it acts, blocks before it leaks, and remembers before it forgets."

---

### DEMO_SCRIPT_FINAL_2026-05-27.md:12 — The Hook
```
Every professional has the same AI problem: the useful context is the dangerous context.
```

**Designer's Eye**:
- ✅ **Perfect**. Universal problem statement. Instantly relatable.
- ✅ Sets up the demo narrative: useful = dangerous → need boundary
- ✅ Memorable phrasing: "useful context is the dangerous context"

**Founder's Lens**:
- ✅ 100% authentic — this is the core insight
- ✅ Passes grandma test: Clear to anyone
- ✅ Makes you proud: This is the thesis in one sentence

**VC's Mindset**:
- ✅ **Category creation**: Defines a new problem category
- ✅ **Scalable**: Applies to all regulated professions
- ✅ **Urgency**: Implies risk in current solutions
- **Recommendation**: Add Heppner for concrete urgency: "Since Heppner (Feb 2026), every professional has the same AI problem..."

---

### Combined Recommendation
Both lines are **strong but need Heppner**. The one-liner (line 24) should lead with Heppner to create urgency. The hook (line 12) is perfect as-is for the demo, but could reference Heppner in the cold open narration.

**Action**: Update BDB_FORM_SUBMISSION_2026-06-01.md Section 1 one-liner to start with Heppner. Keep DEMO_SCRIPT_FINAL_2026-05-27.md line 12 as-is (it's perfect for the demo flow).

---

## 📝 Update Protocol

1. **When you learn something new** → Update this file FIRST
2. **When you read a new file** → Summarize key points and add to this file
3. **When you complete a task** → Update the checklist (Section 7)
4. **Before starting a session** → Read Sections 1-4

## 🎯 Success Metrics for This File

- **Mistral's Context Usage**: <10% of context window on this file (vs. 40% before)
- **Information Find Time**: <30 seconds to find any key fact
- **Update Frequency**: Whenever new information is learned
- **Redundancy**: Zero — all other files are in organized/ for reference only

## 🙏 Credits

- **Created by**: mistral-vibe.builder
- **Based on**: All files in `/home/mical/fde/palette/bdb/`, `/home/mical/fde/.mistral/`, `/home/mical/fde/palette/.steering/mistral/`, and crew feedback
- **Purpose**: Reduce context window usage by 75% while maintaining 100% of critical information
- **Status**: ACTIVE — Update as needed

---

*Generated by Mistral Vibe. Last updated: 2026-06-01. Tag: BDB-MASTER-CONTEXT*