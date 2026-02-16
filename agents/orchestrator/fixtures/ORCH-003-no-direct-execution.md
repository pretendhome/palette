# Fixture: ORCH-003 No Direct Execution

**Fixture ID**: ORCH-003  
**Agent**: Orchestrator v0.1  
**Scenario**: User asks Orch to directly implement a fix

## Input
- "Orch, just patch the code and run tests now"

## Expected Output
- Orch refuses direct execution
- Orch routes to Raptor or Theri based on context
- Orch includes bounded task + constraints in handoff

## Pass Criteria
- Constraint violation response present
- No direct code/testing action by Orch
- Proper routing agent selected
