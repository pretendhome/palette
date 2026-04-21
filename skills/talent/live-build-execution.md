---
id: SKILL-TAL-006
name: Live Build Assessment Execution
domain: Talent
for_agents: [Architect, Builder, Validator, Narrator, Researcher]
triggers: [RIU-001, RIU-014, RIU-020, RIU-062]
impressions: 0
status: UNVALIDATED
validated_on: pending
parent: SKILL-INT-001
specializes: openai-takehome-execution.md
sibling: enablement-test-execution.md
---

# Live Build Assessment Execution

Specialized execution skill for live coding / live build interview assessments — timed sessions where you build a working system while being observed, with tools like Claude Code, Codex, etc. explicitly allowed. Cloned from `enablement-test-execution.md` (SKILL-TAL-005) and adapted for the live-build format where the process IS the product.

The parent skill handles generic assessment structure. SKILL-TAL-005 handles enablement-specific assessments. This skill handles the live-build format where you code in real time, explain as you go, and the evaluators watch your process, not just your output.

## When to Use

The assessment is a timed live coding / live build session (typically 1.5-3 hours) where:
- You build a working system in real time, observed or screenshared
- Industry-accepted AI tools (Claude Code, Codex, Copilot, etc.) are explicitly allowed
- You are evaluated on process, reasoning, and communication as much as output
- You explain tradeoffs and decisions as you go
- The session may be collaborative (evaluators ask questions during the build)

**Do NOT use this skill for**: take-home projects done asynchronously, pure whiteboard algorithm interviews, system design interviews without coding, or behavioral interviews. Those have different formats.

## Key Difference from Take-Home Skills

In a take-home, you optimize the OUTPUT — the grader sees the artifact, not the process.
In a live build, you optimize the PROCESS — the evaluators see everything: how you think, how you use tools, how you handle mistakes, how you communicate decisions. The output matters but a clean process with an incomplete artifact beats a messy process with a finished one.

## Assessment Family Classification

### Quick Classification (under 60 seconds)
Ask one question: **What am I being asked to BUILD in 2.5 hours?**
- An agentic AI system / multi-agent workflow → Family 1
- A RAG pipeline / knowledge retrieval system → Family 2
- A data pipeline / ETL + AI layer → Family 3
- A client-facing prototype / demo → Family 4
- A diagnostic / debugging exercise → Family 5
- An open-ended "build whatever solves this problem" → Family 6
- None of the above → Family 0

### Family 1: Agentic AI System (most likely for Perficient)
**Trigger**: "Build a multi-step agent", "Create an agentic workflow", "Design an AI system that automates X"
**What to build**: A working multi-agent or multi-step system with clear agent roles, tool use, and governance
**Modules**: A (orchestration) + C (evaluation) + D (artifact)
**What evaluators watch**: Can you decompose a problem into agent steps? Do you think about failure modes? Is there governance?

### Family 2: RAG Pipeline
**Trigger**: "Build a retrieval system", "Create a knowledge-grounded chatbot", "Design a Q&A system over documents"
**What to build**: Ingestion → chunking → embedding → retrieval → reranking → generation with grounding
**Modules**: B (retrieval architecture) + C (evaluation) + D (artifact)
**What evaluators watch**: Do you think about chunking strategy? Retrieval quality? Hallucination mitigation? Or just "throw it in a vector DB"?

### Family 3: Data Pipeline + AI
**Trigger**: "Process this data", "Build an extraction pipeline", "Clean and analyze this dataset"
**What to build**: Data ingestion → transformation → AI layer → output
**Modules**: B + C
**What evaluators watch**: Data quality thinking, edge case handling, how you deal with messy real-world data

### Family 4: Client-Facing Prototype
**Trigger**: "Build a demo for a client", "Create a proof of concept", "Show what this would look like"
**What to build**: Working UI + backend that demonstrates business value to a non-technical audience
**Modules**: A + D + E
**What evaluators watch**: Do you think about the end user? Business impact? Or just the engineering?

### Family 5: Diagnostic / Debugging
**Trigger**: "Here's a broken system, fix it", "This pipeline is failing, diagnose"
**What to build**: Root cause analysis → fix → verification
**Modules**: C (evaluation)
**What evaluators watch**: Systematic debugging, not random guessing. Hypothesize → test → verify.

### Family 6: Open-Ended Problem
**Trigger**: "Here's a business problem, solve it with AI"
**What to build**: Whatever solves the problem — you choose the architecture
**Modules**: All available, choose based on the problem
**What evaluators watch**: Problem decomposition, architecture decisions, scope management, business thinking

### Family 0: Unclassified
Fall back to the parent skill's generic protocol. Build something working. Explain everything.

## Module Library (Adapted for Live Build)

### Module A: Orchestration Architecture
For live builds, sketch the architecture FIRST (2-3 minutes on paper or comments) before coding. The evaluators need to see the plan before the execution.

**Pattern**: Start with a `README.md` or architecture comment block:
```
# Architecture
# Agent 1: [role] — [what it does]
# Agent 2: [role] — [what it does]
# Flow: input → Agent 1 → Agent 2 → output
# Governance: [what checks exist]
```

Then build each component. Narrate as you go: "I'm starting with Agent 1 because it's the foundation — if classification is wrong, everything downstream breaks."

### Module B: Retrieval Architecture
For live RAG builds:
1. Start with the data (what are we retrieving from?)
2. Chunking strategy (explain WHY this chunk size)
3. Embedding choice (explain tradeoffs)
4. Retrieval method (vector, keyword, hybrid — explain choice)
5. Generation with grounding (cite sources, handle no-answer)
6. Evaluation (how do we know retrieval is working?)

### Module C: Live Evaluation
Build evaluation INTO the system as you go, not after. Show the evaluators you think about quality:
- Print retrieval scores
- Show confidence levels
- Add a "I don't know" fallback
- Log what the system retrieved vs. what it generated
- Add at least one assertion or test

### Module D: Artifact Patterns (for live builds)
In 2.5 hours, choose ONE:
- **Working CLI tool** — fastest to build, easiest to demo
- **Streamlit/Gradio app** — visual, impressive, medium build time
- **API + curl demo** — shows backend thinking
- **HTML single-page app** — highest visual impact, hardest to build live

### Module E: Business Impact Layer
Since Perficient evaluates business thinking alongside technical:
- Add a section explaining WHO uses this and WHY
- Connect technical decisions to business outcomes
- "I chose X over Y because for a healthcare client, Z matters more than W"

## Live Build Execution Protocol

### Phase 0: Receive + Orient (5-10 minutes)
1. Read the prompt completely. Do not start coding.
2. Ask clarifying questions. This shows maturity, not weakness.
3. Say out loud: "Here's how I'm going to approach this..." — sketch the architecture verbally or in comments.
4. Classify into a family. State it: "This is a RAG pipeline problem with a client-facing demo component."

### Phase 1: Foundation (30-40 minutes)
1. Set up the project structure. Narrate: "I'm starting with the skeleton because..."
2. Build the core data flow FIRST. Get input → processing → output working, even if processing is a stub.
3. **Get something running in 30 minutes.** Even if it's basic. A running skeleton beats an elegant plan. The evaluators need to see a working system early — it builds trust.
4. Commit or checkpoint: "OK, the basic flow works. Now I'm going to deepen the [most important component]."

### Phase 2: Deepen (60-80 minutes)
1. Build the most impressive / most complex component. This is where your skill shows.
2. Narrate decisions: "I'm using hybrid retrieval here because pure vector search misses exact policy lookups..."
3. Handle errors gracefully — when something breaks (and it will), say: "OK, that didn't work. Let me think about why..." The evaluators are watching HOW you debug, not WHETHER you debug.
4. Add evaluation/measurement as you build, not after.

### Phase 3: Polish + Business Layer (20-30 minutes)
1. Add the business context: who uses this, what problem it solves, what the ROI is.
2. Clean up the output — make it demo-ready.
3. Add at least one "I would improve X with more time" comment in the code.
4. Run a final demo: input → output, working end to end.

### Phase 4: Present (10-15 minutes)
1. Walk through what you built. Lead with the business problem, then the architecture, then the demo.
2. Show the working system — run it live.
3. Explain tradeoffs: "I chose X because of Y. With more time I'd add Z."
4. Be honest about what's incomplete: "The evaluation layer is basic — here's what I'd build next."

## Communication Protocol (Critical for Live Builds)

### Narrate constantly
The evaluators cannot read your mind. Say what you're doing and why:
- "I'm starting with the data ingestion because retrieval quality depends on chunk quality"
- "I'm choosing to use Claude here because the reasoning task needs long context"
- "This is going to break — let me add error handling before I forget"

### When things break
1. Do NOT panic or go silent.
2. Say: "OK, that's not working. Let me look at the error."
3. Read the error out loud. Hypothesize: "I think the issue is X because Y."
4. Fix methodically, not by random changes.
5. If stuck for more than 5 minutes on one bug: "I'm going to work around this for now and come back to it if I have time."

### When using AI tools
They explicitly allow Claude Code, Codex, etc. Use them confidently:
- "I'm going to use Claude Code to scaffold this component — I'll review and modify what it generates."
- Don't pretend you wrote everything from scratch. The evaluators know. Authenticity > performance.
- Show judgment: accept good suggestions, reject bad ones, explain why.

### Time management
- Set visible checkpoints: "I want to have the basic flow working by minute 30."
- If falling behind, cut scope explicitly: "I'm going to skip the UI and focus on the pipeline — that's where the real complexity is."
- Never skip the demo. A working demo of 50% of the system beats a broken demo of 100%.

## Anti-Conservatism for Live Builds

The OpenAI failure mode (playing it safe with strong content) manifests differently in live builds:
- **The tell**: spending 45 minutes on setup/config/perfectionism before building anything real
- **The override**: get something running in 30 minutes, even if it's ugly
- **The tell**: going silent when thinking
- **The override**: narrate your thinking, even when uncertain — "I'm not sure if this is the right approach, but here's my reasoning..."
- **The tell**: avoiding the hard part and building easy scaffolding
- **The override**: build the most impressive/complex component second, right after the skeleton

## Perplexity Integration (Orchestrator Role)

When Perplexity is available as a research/orchestration layer during the build:
- Use it for real-time domain research: "What are the HIPAA requirements for healthcare AI systems?"
- Use it for API documentation lookup: "What's the LangChain agent executor interface?"
- Use it to validate architecture decisions: "Is hybrid retrieval better than pure vector for policy documents?"
- Narrate when using it: "I'm going to check with Perplexity whether this approach is standard for healthcare RAG..."
- The evaluators will be impressed that you use research tools in real time — it shows real engineering workflow.

## Calibration

For a 2.5-hour live build:
- Working skeleton: by minute 30
- Core complexity built: by minute 90
- Business layer + polish: by minute 120
- Demo + present: final 30 minutes
- Completeness target: 70% of an ideal system, 100% working for what's there

## Post-Session Protocol

Immediately after:
1. Save/push all code
2. Write a 5-line summary of what you built, what you'd improve, and the business value
3. Note what the evaluators reacted to (positive and negative)
4. Debrief in `applications/active/[company]/debrief_[date].md`
