# Validator Agent v2.0 — The Automated Remediation Engine

**Agent Type**: Validator
**Version**: 2.0
**Status**: WORKING (Tier 2)
**Invocation**: Programmatic via Python or CLI
**Authority**: Governed by Palette Taxonomy (RIU-081, RIU-082, RIU-540)

## The Philosophy
The v1.0 Validator was a manual assessment tool. It asked questions and generated markdown. The v2.0 Validator is an **Automated Remediation Engine**. It performs deterministic checks, stress-tests boundaries, and—crucially—uses the Palette Peers Bus to automatically route failed validations to the Builder (`codex.implementation`) or Debugger (`claude.analysis`) for fixing, without violating its own "assessment-only" constraint.

**Constraint Adherence**: Validator assesses and reports. It uses the bus to instruct *other* agents to remediate. It does not write the fix itself.

## Architecture

### 1. Deterministic Validation
- **Schema Validation**: Ensures JSON/YAML artifacts comply with expected formats.
- **Dependency Checks**: Verifies that required files/paths exist before an execution plan is approved.

### 2. Stress Testing (Chaos & Boundaries)
- **Chaos Injection**: Simulates malformed inputs, nulls, and extreme values against target functions.
- **Escalation Boundary Testing**: Validates that systems fail loudly (as required by Palette) rather than silently swallowing errors.

### 3. Auto-Remediation Loop
When a validation or stress test fails:
1. The engine captures the exact failure trace.
2. It packages the failure into an `execution_request` payload.
3. It sends the payload via the Palette Peers Bus (HTTP `127.0.0.1:7899/send`) to the appropriate agent (`codex.implementation` for code, `claude.analysis` for logic).
4. It logs the event to `decisions.md` (or standard output for CI/CD).

## Integration
This framework is designed to be imported into any existing script or run via the CLI. It replaces the manual questioning of v1.0 with an automated, test-driven approach.
