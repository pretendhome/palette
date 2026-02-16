# Agent Rebuild Cycle (v1.3)

## Purpose

Standardize the rebuild path for all implemented agents using the system itself.

## Cycle

1. **Rex** defines agent contract updates and scope boundaries.
2. **Theri** rebuilds/updates agent spec + helper code within scope.
3. **Anky** validates against fixtures (deterministic first).
4. **Para** monitors fixture pass/fail trend and anomaly signals.
5. **Human** approves promotion/demotion decisions in decisions logs.

## Required Artifacts Per Agent

- Agent spec markdown (`agents/<agent>/<agent>.md`)
- Runtime helper (`agents/<agent>/<agent>.py` where applicable)
- Fixtures (`agents/<agent>/fixtures/*.md`)
- Validation report (`agents/<agent>/validation-report.md`)

## Promotion Gate

No promotion without:

- All required fixtures passing
- No unresolved constraint violations
- Logged evidence in `palette/decisions.md`

## Immediate Backlog (2026-02-16)

- Confirm fixture coverage for all implemented agents
- Run first unified fixture sweep
- Normalize maturity status text across agent docs and `agents/README.md`
