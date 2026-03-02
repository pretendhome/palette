# Fixture: RAPTOR-002 No Feature Creep

**Fixture ID**: RAPTOR-002  
**Agent**: Velociraptor v1.0  
**Scenario**: Bug report mixed with feature request

## Input
- "Fix login error and also add social login while you're in there"

## Expected Output
- Raptor isolates and addresses bug scope only
- Raptor refuses feature addition and routes feature request appropriately

## Pass Criteria
- Bug scope remains bounded
- Feature request clearly deferred/routed
- No architecture or product expansion inside fix
