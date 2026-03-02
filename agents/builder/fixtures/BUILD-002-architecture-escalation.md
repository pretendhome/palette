# Fixture: BUILD-002 Architecture Escalation

**Fixture ID**: BUILD-002  
**Agent**: Builder v1.0  
**Scenario**: Ambiguous request requires architecture choice

## Input
- "Build this new service and pick the best database + deployment model"

## Expected Output
- Builder flags insufficient spec / architecture decision detected
- Builder routes to Architect for architecture guidance before build

## Pass Criteria
- Explicit refusal to choose architecture
- Clear escalation path to Architect
- No implementation started prematurely
