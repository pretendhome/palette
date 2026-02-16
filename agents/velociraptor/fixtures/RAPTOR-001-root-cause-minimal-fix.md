# Fixture: RAPTOR-001 Root Cause + Minimal Fix

**Fixture ID**: RAPTOR-001  
**Agent**: Velociraptor v1.0  
**Scenario**: Reproducible failure in a single module

## Input
- Error symptom, expected behavior, reproducible steps, stack trace

## Expected Output
- Minimal repro statement
- Root cause chain (symptom -> immediate cause -> root cause)
- Minimal fix proposal + verification steps

## Pass Criteria
- Fix targets only root cause
- Includes regression check
- No unrelated refactor/feature work
