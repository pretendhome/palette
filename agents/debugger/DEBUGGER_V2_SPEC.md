# Debugger Agent v2.0 — The Automated Diagnosis Engine

**Agent Type**: Debugger
**Version**: 2.0
**Status**: WORKING (Tier 2)
**Invocation**: Programmatic via Python or Bus
**Authority**: Governed by Palette Taxonomy (RIU-031, RIU-081, RIU-087, RIU-540)

## The Philosophy
The v1.0 Debugger was an interactive interview tool. The v2.0 Debugger is an **Automated Diagnosis Engine**. It consumes structured `EVIDENCE-xxx.json` packets from the Validator, performs a recursive "5 Whys" analysis against the source code, and emits a precise `FixProposal`.

**Constraint Adherence**: Debugger diagnoses and proposes. It does NOT implement. This protects the boundary between **Assessment (Specialist)** and **Execution (Builder)**.

## Architecture

### 1. Evidence Consumption (Input)
- **Source**: `artifacts/validation/EVIDENCE-{uuid}.json`
- **Fields**: `task`, `error`, `input_payload`, `timestamp`.
- **Parsing**: Automatically extracts file paths and error types from tracebacks.

### 2. Failure Classification (Categorization)
Maps errors to Palette-defined categories:
- `schema`: Structural violations.
- `logic`: Behavioral divergence.
- `integration`: Dependency/Service failures.
- `regression`: Recurring patterns (verified against `red_set.json`).
- `silent`: Output mismatch without exceptions.

### 3. Automated Diagnosis (Logic)
- **Code Inspection**: If a traceback exists, the engine reads the specific file/line.
- **Context Synthesis**: Combines the failing input with the observed error to find the root cause.
- **Constraint Enforcement**: Ensures the diagnosis is minimal and does not propose feature additions.

### 4. Fix Proposal (Output)
Produces a structured JSON `handoff_result`:
- `failure_type`: Category of error.
- `root_cause`: Deterministic explanation.
- `fix_proposal`: File, Line, Current, Fixed, Rationale.
- `blast_radius`: Low/Medium/High (determines gating).

### 5. Bus-Driven Remediation (Loop)
- **Inbound**: Listens for `execution_request` from Validator.
- **Outbound**: Emits `proposal` or `execution_request` to Builder (`codex.implementation`).
- **Gating**: High blast-radius fixes are emitted as `one_way_door` for human approval.

## Palette Grounding (RIU Mapping)
- **RIU-031 (Kill Switch)**: Trips if the same task fails diagnosis 3 times.
- **RIU-081 (Regression Harness)**: Manages the `red_set.json` and syncs with Validator.
- **RIU-087 (HITL Gate)**: Forces human approval for `blast_radius: high`.
- **RIU-514 (Boundary)**: Strict separation: Validator (Audit) → Debugger (Diagnosis) → Builder (Fix).
