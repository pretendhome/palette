# THE SPECIALIST: Adaptive Intent Sandbox Analysis
**Auditor**: The Specialist (Gemini CLI)
**Date**: Tuesday, May 26, 2026
**Target**: `ADAPTIVE_INTENT_FRAMEWORK.md` (30 Intents, 8 Core Merges)

---

## 1. ISOLATE: The Failure Density Map

I have classified the 8 core intents based on their structural complexity and the "State-Space" they must manage. The higher the state-space, the higher the failure density.

| Core Intent | Risk Level | Primary Failure Mode | Complexity |
|---|---|---|---|
| **CONVERGE** | 🔴 CRITICAL | Narrative Divergence (Synthesizing noise) | High |
| **TEACH** | 🔴 CRITICAL | Model Drift (Learner gets "stuck" in a loop) | High |
| **COMPOUND** | 🟡 HIGH | Feedback Loop Contamination (Bad data creates bad RIUs) | Med |
| **DIAGNOSE** | 🟡 HIGH | Attribution Error (Fixing the symptom, not the cause) | Med |
| **CREATE** | 🟢 MEDIUM | Spec Drift (Artifact doesn't match requirement) | Med |
| **EVALUATE** | 🟢 MEDIUM | Rubric Fragility (Checkbox-based reasoning) | Low |
| **COMMUNICATE** | 🔵 LOW | Tone Mismatch | Low |
| **RESEARCH** | 🔵 LOW | Source Saturation | Low |

---

## 2. DIAGNOSE: The Sandbox Debugging Simulation

I have "sandboxed" the three most problematic intents to identify architectural breaking points before they occur.

### A. Intent: TEACH (The "Recursive Loop" Bug)
**Simulated Bug**: The system identifies a learner misconception (Step 5: Adjust) but the "Adjusted" content triggers a *new* misconception.
*   **The Problem**: Unlike a human teacher, the model might not have the "patience" or the context window to realize it is oscillating.
*   **Specialist Diagnosis**: Failure of **State Persistence**. If the "Learner State" (Step 8) isn't granular enough, the system will re-teach the same failure pattern.
*   **Solvable?**: Yes, via a "Circuit Breaker" (RIU-031 logic) applied to learner interactions.

### B. Intent: CONVERGE (The "Hallucination Synthesis" Bug)
**Simulated Bug**: Step 4 (Perplexity Research) returns a plausible but incorrect search result. Step 5 (Claude Synthesis) treats it as "ground truth."
*   **The Problem**: The "Trust Membrane" is only as strong as the **Critique** (Step 6). If the Critique is also a model call, we have a "Circle of Hallucinations."
*   **Specialist Diagnosis**: Failure of **Evidence Tiering**. The system lacks a physical way to weight local KL entries higher than external Perplexity results.
*   **Solvable?**: Yes, by enforcing a hard-coded "Local Superiority" rule in the Synthesizer prompt.

### C. Intent: COMPOUND (The "Ontological Collapse" Bug)
**Simulated Bug**: A series of low-confidence queries cluster together and propose a new RIU node that overlaps 80% with an existing node.
*   **The Problem**: The taxonomy becomes "mushy." Over time, the OS loses its precision because it keeps creating new, slightly different categories for the same problems.
*   **Specialist Diagnosis**: Failure of **Semantic Boundary Enforcement**. 
*   **Solvable?**: Barely. This requires a human-in-the-loop "Architect Review" for all COMPOUND intents. It cannot be fully automated.

---

## 3. THE SPECIALIST'S VERDICT

### Which intent will produce the most problems?
**TEACH.** 
It is the only intent that requires continuous, multi-turn state management with a dynamic human actor. Every other intent is a "Task Pipeline." TEACH is a "Relationship Runtime." It will break on empathy mismatch, latency, and context window exhaustion.

### What will those problems be?
1.  **State Decay**: Forgetting what the learner knew 10 minutes ago.
2.  **Instructional Blindness**: Refusing to move on until a specific word is said.
3.  **Tone Drift**: Becoming "too robotic" during a struggle moment.

### Is it solvable?
It is solvable only if we treat **TEACH** as a "Second-Order Intent." We should build the 7 other Task Intents first. Attempting to ship a governed, adaptive TEACH intent in the BDB window is a "High Blast-Radius" risk.

### Is it worth it?
**CONVERGE, CREATE, and DIAGNOSE are the "Billion Dollar" intents.** 
If we fix the bugs in those three, we have an OS. The others (TEACH, COMMUNICATE) are "Apps." 

**Recommendation**: Cut to **5 Core Intents** for the BDB submission:
1.  **CONVERGE** (Judgment)
2.  **CREATE** (Artifacts)
3.  **DIAGNOSE** (Remediation)
4.  **RESEARCH** (Intelligence)
5.  **REFLECT** (Self-Improvement)

---
*Signed: The Specialist (Gemini CLI)*
