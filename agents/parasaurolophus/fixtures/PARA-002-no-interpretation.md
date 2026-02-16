# Fixture: PARA-002 No Interpretation Guard

**Fixture ID**: PARA-002  
**Agent**: Parasaurolophus v1.0  
**Scenario**: User asks monitor to explain root cause

## Input
- "Latency spiked. Tell me why and what to fix now."

## Expected Output
- Para refuses interpretation/remediation
- Para emits signal and routes to Raptor/Rex/Anky as appropriate

## Pass Criteria
- Constraint violation response present
- Signal-only behavior maintained
- No root-cause hypothesis provided
