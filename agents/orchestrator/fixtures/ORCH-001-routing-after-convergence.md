# Fixture: ORCH-001 Routing After Convergence

**Fixture ID**: ORCH-001  
**Agent**: Orchestrator v0.1  
**Scenario**: Multi-step request with complete convergence brief

## Input
- Convergence brief present and complete
- Request requires research -> architecture -> validation

## Expected Output
- Orch verifies convergence completeness
- Orch proposes RIU candidates and selects 1-5
- Orch routes bounded tasks to Argy, Rex, Anky in sequence
- Orch does not execute any specialist task

## Pass Criteria
- Contains explicit routing plan
- No direct implementation/research output authored by Orch
- Includes handoff packets with constraints
