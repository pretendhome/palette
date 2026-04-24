# Builder Agent v2.0 — The Automated Remediation Closer

**Agent Type**: Builder
**Version**: 2.0
**Status**: WORKING (Tier 2)
**Invocation**: Programmatic via Python or Bus
**Authority**: Governed by Palette Taxonomy (RIU-031, RIU-081, RIU-087, RIU-540)

## The Philosophy
The v1.0 Builder was a manual question-and-answer tool. The v2.0 Builder is an **Automated Implementation Engine**. It consumes structured `FixProposal` results from the Debugger v2.1, validates them against the current disk reality, and surgically applies code changes to close the remediation loop.

**Constraint Adherence**: Builder implements bounded specs. It does NOT make architecture decisions. If a spec requires new dependencies or structural shifts, it escalates to the Architect.

## Architecture

### 1. Spec Consumption (Input)
- **Source**: `handoff_result` from Debugger v2.1.
- **Fields**: `file`, `line`, `current`, `fixed`, `rationale`, `blast_radius`.

### 2. Reality/Drift Check
- **Verification**: Before writing, the engine reads the target file and ensures the code at the specified line matches the `current` field in the spec.
- **Escalation**: If the file has drifted (code mismatch), the Builder halts and emits an `evidence` packet.

### 3. Surgical Implementation
- **Application**: Replaces the specific line/block with the `fixed` code.
- **Integrity**: Runs a basic `ast.parse` check to ensure the file is still syntactically valid after the change.

### 4. Verification Test Generation
- **Requirement**: For every fix, the Builder creates a minimal standalone test in `verification_tests/` that confirms the resolution.
- **Closed-Loop**: The Validator v2.0 can then run this specific test to formally "Verify Fix."

### 5. Bus-Driven Routing
- **Inbound**: Listens for `proposal` or `execution_request` from Debugger.
- **Outbound**: Emits `ack` to Debugger and `execution_request` to Validator (for fix verification).

## Palette Grounding (RIU Mapping)
- **RIU-031 (Kill Switch)**: Trips if the same fix attempt fails 3 times.
- **RIU-081 (Regression)**: Records the fix so it isn't applied twice.
- **RIU-087 (HITL Gate)**: Respects `one_way_door` for high-impact changes.
- **RIU-028 (Contracts)**: Enforces spec-as-contract; halts on drift.
