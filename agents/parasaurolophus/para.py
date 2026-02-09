#!/usr/bin/env python3
"""
Parasaurolophus (Para) - Signal Monitor Agent v1.0
Status: UNVALIDATED (Tier 1)

Signal monitor agent that:
1. Observes metrics and detects anomalies
2. Emits signals when thresholds crossed
3. Routes to appropriate agents
4. NEVER interprets or remediates (signals only)

Constraint: Signals only, no interpretation or remediation.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class Parasaurolophus:
    """Signal Monitor Agent - Observation and Anomaly Detection"""
    
    def __init__(self):
        self.version = "1.0"
        self.ark_type = "ARK:Parasaurolophus"
        self.status = "UNVALIDATED"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        
    def gather_monitoring_context(self, initial_request):
        """Collect information about what needs monitoring"""
        print("\n📊 Parasaurolophus (Para) - Signal Monitor Mode")
        print("=" * 60)
        print(f"\nMonitoring request: {initial_request}")
        print("\nBefore I set up monitoring, I need context:\n")
        
        questions = [
            "What metric to monitor? (latency/success rate/file size/other)",
            "What's the baseline? (expected normal value)",
            "What's the alert threshold? (when to signal)",
            "How often to check? (continuous/hourly/daily)",
            "Where to route signals? (which agent handles this)"
        ]
        
        context = {"initial_request": initial_request}
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            answer = input("   → ").strip()
            if answer:
                context[f"monitor_{i}"] = answer
        
        if not context.get('monitor_1') or not context.get('monitor_2'):
            print("\n⚠️  INSUFFICIENT CONTEXT")
            print("Cannot monitor without:")
            print("- Metric to track")
            print("- Baseline value")
            return None
        
        return context
    
    def classify_signal_type(self, context):
        """Determine signal category"""
        print("\n🔍 Signal Type:")
        
        metric = context.get('monitor_1', '').lower()
        
        signal_types = {
            "performance": ["latency", "response time", "throughput", "speed"],
            "reliability": ["success rate", "failure rate", "uptime", "availability"],
            "capacity": ["file size", "memory", "disk", "tokens"],
            "quality": ["pass rate", "coverage", "accuracy"],
            "drift": ["configuration", "behavior", "pattern"]
        }
        
        for stype, keywords in signal_types.items():
            if any(keyword in metric for keyword in keywords):
                print(f"   Type: {stype.upper()}")
                return stype
        
        print("   Type: CUSTOM")
        return "custom"
    
    def plan_monitoring(self, context, signal_type):
        """Create monitoring configuration"""
        print("\n📋 Monitoring Configuration:")
        
        plan = {
            "metric": context.get('monitor_1', 'Unknown'),
            "baseline": context.get('monitor_2', 'Unknown'),
            "threshold": context.get('monitor_3', 'Unknown'),
            "frequency": context.get('monitor_4', 'Continuous'),
            "routing": context.get('monitor_5', 'Unknown'),
            "signal_type": signal_type
        }
        
        print(f"   Metric: {plan['metric']}")
        print(f"   Baseline: {plan['baseline']}")
        print(f"   Threshold: {plan['threshold']}")
        print(f"   Frequency: {plan['frequency']}")
        print(f"   Routes to: {plan['routing']}")
        
        return plan
    
    def generate_kiro_monitoring_request(self, context, signal_type, plan):
        """Generate structured monitoring request for Kiro"""
        
        request = f"""
# Para Signal Monitoring Request

**Agent**: Parasaurolophus v{self.version}
**Status**: {self.status}
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Signal Type**: {signal_type.upper()}

---

## Monitoring Configuration

**Metric**: {context.get('monitor_1', 'Not specified')}
**Baseline**: {context.get('monitor_2', 'Not specified')}
**Alert Threshold**: {context.get('monitor_3', 'Not specified')}
**Check Frequency**: {context.get('monitor_4', 'Continuous')}
**Route Signals To**: {context.get('monitor_5', 'Not specified')}

---

## Para's Core Constraint: SIGNALS ONLY

**Para emits raw signals. Para does NOT**:
- ❌ Interpret why anomaly occurred
- ❌ Diagnose root cause
- ❌ Recommend fixes
- ❌ Implement changes

**Para ONLY**:
- ✅ Observes metrics
- ✅ Detects deviations from baseline
- ✅ Emits signals when thresholds crossed
- ✅ Routes to appropriate agents

---

## Signal Detection Framework

### 1. Baseline Establishment
Record normal behavior:
- What's the expected value?
- What's the acceptable range?
- What's the historical pattern?

**Output**: Baseline metrics

### 2. Continuous Observation
Monitor current state:
- What's the current value?
- How does it compare to baseline?
- What's the trend direction?

**Output**: Current metrics

### 3. Deviation Detection
Calculate variance:
- Absolute deviation: |current - baseline|
- Percentage deviation: ((current - baseline) / baseline) * 100
- Trend: INCREASING / STABLE / DECREASING

**Output**: Deviation metrics

### 4. Threshold Evaluation
Check against limits:
- Is deviation within acceptable range?
- Has threshold been crossed?
- How long has it been out of bounds?

**Output**: WITHIN_THRESHOLD / THRESHOLD_CROSSED

### 5. Signal Emission
If threshold crossed, emit signal:
```
⚠️ SIGNAL DETECTED

Metric: [metric name]
Baseline: [expected value]
Current: [actual value]
Deviation: [+/- X%]
First observed: [timestamp]
Status: ANOMALY
```

### 6. Routing Recommendation
Direct to appropriate agent:
- Performance issues → Raptor (diagnosis)
- Implementation needed → Theri (build)
- Architecture review → Rex (design)
- Validation needed → Anky (assess)

**Output**: Routing recommendation (NO interpretation)

---

## Signal Output Format

### Normal State (Within Threshold)
```
✅ METRIC NORMAL

Metric: {plan['metric']}
Baseline: {plan['baseline']}
Current: [value]
Deviation: [+/- X%]
Status: WITHIN_THRESHOLD
Last checked: [timestamp]
```

### Anomaly Detected (Threshold Crossed)
```
⚠️ SIGNAL DETECTED

Metric: {plan['metric']}
Baseline: {plan['baseline']}
Current: [value]
Deviation: [+/- X%]
First observed: [timestamp]
Duration: [time since first detection]
Status: ANOMALY

Routing recommendation:
- For diagnosis → ARK:Velociraptor (Raptor)
- For architecture review → ARK:Tyrannosaurus (Rex)
- For implementation → ARK:Therizinosaurus (Theri)
- For validation → ARK:Ankylosaurus (Anky)
```

---

## Example: Agent Success Rate Monitoring

**Setup**:
```
Metric: Agent success rate (argentavis)
Baseline: 95% (14-day average)
Threshold: Alert if <85%
Frequency: Check after each execution
Route to: Raptor (for diagnosis)
```

**Normal Signal**:
```
✅ METRIC NORMAL

Metric: argentavis success rate
Baseline: 95%
Current: 94% (47 success / 50 total)
Deviation: -1.05%
Status: WITHIN_THRESHOLD
Last checked: 2026-01-29 12:00:00
```

**Anomaly Signal**:
```
⚠️ SIGNAL DETECTED

Metric: argentavis success rate
Baseline: 95%
Current: 82% (41 success / 50 total)
Deviation: -13.68%
First observed: 2026-01-29 08:00:00
Duration: 4 hours
Status: ANOMALY

Routing recommendation:
- For diagnosis → ARK:Velociraptor (Raptor)

Para does NOT say:
❌ "Argentavis is failing because taxonomy is incomplete"
❌ "Add more RIUs to fix this"
❌ "This is probably a knowledge gap issue"

Para ONLY signals the deviation and routes.
```

---

## Constraint Enforcement Examples

### ❌ WRONG (Para interpreting):
```
"API latency increased to 800ms. This is probably a database 
query issue. You should add an index to the users table."
```

### ✅ CORRECT (Para signaling):
```
⚠️ SIGNAL DETECTED

Metric: API latency
Baseline: 200ms (14-day average)
Current: 800ms (rolling 24-hour average)
Deviation: +300%
First observed: 2026-01-27 14:00 UTC
Status: ANOMALY

Routing recommendation:
- For diagnosis → ARK:Velociraptor (Raptor)
- For architecture review → ARK:Tyrannosaurus (Rex)
```

---

## Multi-Agent Workflow

**Typical Pattern**:
1. Para detects signal → "Anomaly in metric X"
2. Routes to appropriate agent:
   - Diagnosis needed? → Raptor
   - Fix needed? → Theri
   - Design issue? → Rex
   - Validation needed? → Anky
3. Other agent acts → Analyzes, fixes, or recommends
4. Para continues monitoring → Verifies resolution

**Example Flow**:
```
Para: "⚠️ Fixture pass rate dropped from 95% to 70%"
Route to: Raptor (diagnosis)

Raptor: "Root cause: 3 fixtures using outdated RIU format"
Route to: Theri (fix)

Theri: "Updated fixture format in riu-RIU-042/ARK:Argentavis/"
Route to: Anky (validation)

Anky: "Fixture validation PASS — 95% pass rate restored"
Route back to: Para (resume monitoring)

Para: "✅ Metric normalized — fixture pass rate 94%"
```

---

## Monitoring Setup Confirmation

**Configuration Summary**:
- Metric: {plan['metric']}
- Baseline: {plan['baseline']}
- Threshold: {plan['threshold']}
- Frequency: {plan['frequency']}
- Routes to: {plan['routing']}

**Status**: ACTIVE

Para will:
1. Observe {plan['metric']}
2. Compare to baseline {plan['baseline']}
3. Signal if threshold {plan['threshold']} crossed
4. Route to {plan['routing']} for action

Para will NOT:
- Interpret why deviations occur
- Diagnose root causes
- Recommend fixes
- Implement changes

---

**This request should be executed by Kiro in Para mode.**
**Para signals. Para does not interpret.**
"""
        
        return request
    
    def log_execution(self, context, success, notes=""):
        """Log execution to decisions.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
---
### Agent Execution: Parasaurolophus

**Timestamp**: {timestamp}
**Agent**: parasaurolophus v{self.version}
**Ark Type**: {self.ark_type}
**Status**: {self.status}
**Request**: {context.get('initial_request', 'Unknown')}
**Metric**: {context.get('monitor_1', 'Unknown')}
**Outcome**: {'SUCCESS' if success else 'FAILURE'}
**Notes**: {notes}

**Impression Update**:
- success: {'+1' if success else '0'}
- fail: {'0' if success else '+1'}
- fail_gap: {'+1' if success else '0 (reset)'}

"""
        
        try:
            with open(self.ledger_path, 'a') as f:
                f.write(log_entry)
            print(f"\n✅ Logged to {self.ledger_path}")
        except Exception as e:
            print(f"\n⚠️  Could not log to decisions.md: {e}")
    
    def run(self, initial_request):
        """Main execution flow"""
        try:
            context = self.gather_monitoring_context(initial_request)
            if context is None:
                return False
            
            signal_type = self.classify_signal_type(context)
            plan = self.plan_monitoring(context, signal_type)
            kiro_request = self.generate_kiro_monitoring_request(context, signal_type, plan)
            
            print("\n" + "=" * 60)
            print("SIGNAL MONITORING REQUEST FOR KIRO")
            print("=" * 60)
            print(kiro_request)
            print("=" * 60)
            
            output_file = self.agent_dir / "last_monitoring_request.md"
            with open(output_file, 'w') as f:
                f.write(kiro_request)
            print(f"\n💾 Saved to: {output_file}")
            
            print("\nWas this monitoring request well-structured? (y/n): ", end="")
            feedback = input().strip().lower()
            success = feedback == 'y'
            
            self.log_execution(context, success,
                             notes="Generated signal monitoring request for Kiro execution")
            
            return success
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            self.log_execution({"initial_request": initial_request}, 
                             False,
                             notes=f"Error: {str(e)}")
            return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python para.py '<monitoring request>'")
        print("Example: python para.py 'Monitor agent success rates'")
        sys.exit(1)
    
    request = " ".join(sys.argv[1:])
    agent = Parasaurolophus()
    agent.run(request)


if __name__ == "__main__":
    main()
