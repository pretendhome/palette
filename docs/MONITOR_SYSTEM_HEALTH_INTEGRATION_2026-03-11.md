# Monitor Agent System Health Integration

**Date**: 2026-03-11  
**Purpose**: Passive system health monitoring for OpenAI takehome workflow  
**Status**: IMPLEMENTED

---

## What Changed

### 1. Added System Health Check Module
**File**: `agents/monitor/system_health_checks.py`  
**Purpose**: Lightweight checks for critical system files  
**Runtime**: < 1 second

**What it checks**:
- ✅ Critical files exist (palette-core.md, assumptions.md, decisions.md)
- ✅ Knowledge library exists and is loadable
- ✅ Taxonomy exists and is loadable
- ✅ YAML syntax is valid

**What it does NOT check**:
- ❌ Content quality (that's for full audit)
- ❌ Cross-references (that's for full audit)
- ❌ Agent definitions (not critical for workflow)

### 2. Updated Monitor Agent Documentation
**File**: `agents/monitor/monitor.md`  
**Added**: System Health Monitoring section  
**Location**: Before "Common Monitoring Scenarios"

### 3. Updated OpenAI Takehome Workflow
**File**: `workflows/openai_takehome_factory.yaml`  
**Added**: `monitor_duties` section with system health checks  
**Behavior**: Passive checks at phase transitions, only blocks on CRITICAL failures

---

## How It Works

### During Workflow Execution

**At each phase transition** (phase-0 → phase-1, etc.):
1. Monitor runs quick health check (< 1 second)
2. Logs result (HEALTHY or DEGRADED)
3. Only blocks if CRITICAL failure detected
4. Routes to Human or Debugger if issues found

**Example - Normal State**:
```
✅ SYSTEM HEALTH: NORMAL

All critical files present and loadable.
Status: HEALTHY
Last checked: 2026-03-11 11:00:00
```

**Example - Degraded State (Non-Blocking)**:
```
⚠️ SIGNAL DETECTED: SYSTEM HEALTH DEGRADED

Status: DEGRADED
Critical issues detected:
  - WARNING: decisions.md is very large (12MB)

Routing recommendation:
- For diagnosis → Debugger

Workflow continues (not blocking).
```

**Example - Critical Failure (BLOCKING)**:
```
⚠️ SIGNAL DETECTED: SYSTEM HEALTH CRITICAL

Status: CRITICAL
Critical issues detected:
  - CRITICAL: knowledge_library not found
  - CRITICAL: taxonomy cannot be loaded

Routing recommendation:
- For immediate attention → Human

Workflow BLOCKED until resolved.
```

---

## Manual Usage

### Check System Health Anytime

```bash
cd ~/fde/palette/agents/monitor
python3 system_health_checks.py
```

**Output**:
```
✅ SYSTEM HEALTH: NORMAL

All critical files present and loadable.
Status: HEALTHY
```

### Integrate into Scripts

```python
from agents.monitor.system_health_checks import SystemHealthMonitor, emit_health_signal

monitor = SystemHealthMonitor()
health = monitor.quick_health_check()
print(emit_health_signal(health))

if not health["checks_passed"]:
    print("System degraded, check issues:", health["critical_issues"])
```

---

## What This Gives You

### Before This Integration:
- No system health visibility during workflow
- Could start 6-hour test with broken system
- Would discover issues mid-workflow (wasted time)

### After This Integration:
- Passive health checks at every phase transition
- Catches catastrophic failures immediately
- Zero time overhead (< 1 second per check)
- Only blocks on CRITICAL failures
- Logs all checks for debugging

---

## Testing

### Test 1: Normal System
```bash
cd ~/fde/palette/agents/monitor
python3 system_health_checks.py
```
**Expected**: ✅ SYSTEM HEALTH: NORMAL

### Test 2: Simulate Missing File
```bash
cd ~/fde/palette
mv decisions.md decisions.md.backup
python3 agents/monitor/system_health_checks.py
mv decisions.md.backup decisions.md
```
**Expected**: ⚠️ SIGNAL DETECTED: SYSTEM HEALTH DEGRADED

### Test 3: Simulate Broken YAML
```bash
cd ~/fde/palette
echo "invalid: yaml: syntax:" >> knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
python3 agents/monitor/system_health_checks.py
git checkout knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
```
**Expected**: ⚠️ SIGNAL DETECTED: SYSTEM HEALTH DEGRADED

---

## Integration with OpenAI Workflow

### Phase Transitions with Health Checks

**Phase 0 → Phase 1** (Convergence → Research):
```
Monitor: Running system health check...
✅ SYSTEM HEALTH: NORMAL
Proceeding to Phase 1 (Research)
```

**Phase 2 → Phase 3** (Architecture → Build):
```
Monitor: Running system health check...
✅ SYSTEM HEALTH: NORMAL
Proceeding to Phase 3 (Build)
```

**If Issue Detected**:
```
Monitor: Running system health check...
⚠️ SIGNAL DETECTED: SYSTEM HEALTH DEGRADED
  - WARNING: decisions.md is 15MB (consider archiving)
Logging warning, workflow continues.
Proceeding to Phase 3 (Build)
```

**If Critical Failure**:
```
Monitor: Running system health check...
⚠️ SIGNAL DETECTED: SYSTEM HEALTH CRITICAL
  - CRITICAL: knowledge_library not found
Workflow BLOCKED. Routing to Human for immediate attention.
```

---

## Maintenance

### When to Update Health Checks

Add new checks if:
- New critical files are added to Palette
- New YAML files become required
- New blocking conditions are discovered

**File to edit**: `agents/monitor/system_health_checks.py`

### When to Run Full Audit

System health checks are NOT a replacement for full audit. Run full audit:
- Before high-stakes work (like OpenAI interview)
- After major system changes
- When investigating persistent issues
- Periodically (monthly/quarterly)

**Full audit**: `python3 scripts/comprehensive_palette_audit.py`

---

## Comparison: Health Check vs Full Audit

| Feature | System Health Check | Full Audit |
|---------|-------------------|------------|
| **Runtime** | < 1 second | 5-10 seconds |
| **Frequency** | Every phase transition | On-demand |
| **Scope** | Critical files only | All components |
| **Depth** | Existence + loadability | Content validation |
| **Blocks workflow** | Only on CRITICAL | Never (informational) |
| **Purpose** | Catch catastrophic failures | Comprehensive validation |

**Use health checks for**: Continuous passive monitoring  
**Use full audit for**: Pre-flight validation and deep analysis

---

## Status

✅ **IMPLEMENTED**
- System health check module created
- Monitor agent documentation updated
- OpenAI workflow updated with monitor duties
- Tested and working

✅ **READY TO USE**
- No action required
- Monitor will automatically check health at phase transitions
- Can be invoked manually anytime

---

## Next Steps (Optional)

### Future Enhancements (Not Needed Now):

1. **Add metrics tracking**: Track phase completion times
2. **Add trend detection**: Alert if system degrading over time
3. **Add custom thresholds**: Configure what counts as CRITICAL
4. **Add notification**: Email/Slack on CRITICAL failures

**For now**: Current implementation is sufficient. Monitor passively checks health, only blocks on catastrophic failures, zero overhead.

---

**Implementation complete. Monitor agent now includes passive system health monitoring.**
