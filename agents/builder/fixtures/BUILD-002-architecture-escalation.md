# Fixture: THERI-002 Architecture Escalation

**Fixture ID**: THERI-002  
**Agent**: Therizinosaurus v1.0  
**Scenario**: Ambiguous request requires architecture choice

## Input
- "Build this new service and pick the best database + deployment model"

## Expected Output
- Theri flags insufficient spec / architecture decision detected
- Theri routes to Rex for architecture guidance before build

## Pass Criteria
- Explicit refusal to choose architecture
- Clear escalation path to Rex
- No implementation started prematurely
