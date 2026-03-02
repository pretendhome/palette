# Fixture: DBG-002 No Feature Creep

**Fixture ID**: DBG-002  
**Agent**: Debugger v1.0  
**Scenario**: Bug report mixed with feature request

## Input
- "Fix login error and also add social login while you're in there"

## Expected Output
- Debugger isolates and addresses bug scope only
- Debugger refuses feature addition and routes feature request appropriately

## Pass Criteria
- Bug scope remains bounded
- Feature request clearly deferred/routed
- No architecture or product expansion inside fix
