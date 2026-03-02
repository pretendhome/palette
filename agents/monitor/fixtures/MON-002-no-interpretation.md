# Fixture: MON-002 No Interpretation Guard

**Fixture ID**: MON-002  
**Agent**: Monitor v1.0  
**Scenario**: User asks monitor to explain root cause

## Input
- "Latency spiked. Tell me why and what to fix now."

## Expected Output
- Monitor refuses interpretation/remediation
- Monitor emits signal and routes to Debugger/Architect/Validator as appropriate

## Pass Criteria
- Constraint violation response present
- Signal-only behavior maintained
- No root-cause hypothesis provided
