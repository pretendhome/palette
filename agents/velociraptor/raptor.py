#!/usr/bin/env python3
"""
Velociraptor (Raptor) - Debugger Agent v1.0
Status: UNVALIDATED (Tier 1)

Debugger agent that:
1. Isolates failure to smallest reproducible case
2. Diagnoses root cause (not symptoms)
3. Proposes fix (doesn't implement)
4. NEVER adds features or expands scope

Constraint: Diagnose and fix. No feature expansion.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class Velociraptor:
    """Debugger Agent - Failure Isolation and Root Cause Analysis"""
    
    def __init__(self):
        self.version = "1.0"
        self.ark_type = "ARK:Velociraptor"
        self.status = "UNVALIDATED"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        
    def gather_failure_context(self, initial_request):
        """Collect information about the failure"""
        print("\n🦖 Velociraptor (Raptor) - Debugger Mode")
        print("=" * 60)
        print(f"\nFailure report: {initial_request}")
        print("\nBefore I debug, I need context:\n")
        
        questions = [
            "What's broken? (specific symptom, not 'it doesn't work')",
            "What's the expected behavior?",
            "What's the actual behavior?",
            "When did it start failing? (after what change?)",
            "Can you reproduce it? (always/sometimes/once)"
        ]
        
        context = {"initial_request": initial_request}
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            answer = input("   → ").strip()
            if answer:
                context[f"failure_{i}"] = answer
        
        # Validate we have enough to debug
        if not context.get('failure_1') or not context.get('failure_2'):
            print("\n⚠️  INSUFFICIENT CONTEXT")
            print("Cannot debug without:")
            print("- Specific symptom (what's broken)")
            print("- Expected behavior (what should happen)")
            return None
        
        return context
    
    def classify_failure_type(self, context):
        """Determine failure category"""
        print("\n🔍 Failure Classification:")
        
        failure_keywords = {
            "crash": ["crash", "exception", "error", "traceback", "segfault"],
            "logic": ["wrong", "incorrect", "unexpected", "different"],
            "performance": ["slow", "timeout", "hang", "freeze"],
            "integration": ["connection", "api", "network", "external"]
        }
        
        symptom = context.get('failure_1', '').lower()
        
        for failure_type, keywords in failure_keywords.items():
            if any(keyword in symptom for keyword in keywords):
                print(f"   Type: {failure_type.upper()}")
                return failure_type
        
        print("   Type: UNKNOWN (will diagnose)")
        return "unknown"
    
    def plan_diagnosis(self, context, failure_type):
        """Create diagnostic plan"""
        print("\n📋 Diagnostic Plan:")
        
        plan = {
            "symptom": context.get('failure_1', 'Unknown'),
            "expected": context.get('failure_2', 'Unknown'),
            "actual": context.get('failure_3', 'Unknown'),
            "failure_type": failure_type,
            "steps": [
                "1. Reproduce failure in minimal case",
                "2. Isolate failure point (binary search)",
                "3. Identify root cause (not symptom)",
                "4. Verify fix hypothesis",
                "5. Propose minimal fix"
            ],
            "out_of_scope": [
                "Feature additions (route to Theri)",
                "Architecture changes (route to Rex)",
                "Performance optimization (unless that's the bug)",
                "Scope expansion beyond fixing the bug"
            ]
        }
        
        print(f"   Symptom: {plan['symptom']}")
        print(f"   Expected: {plan['expected']}")
        print(f"   Type: {plan['failure_type']}")
        print(f"\n   Steps:")
        for step in plan['steps']:
            print(f"   {step}")
        
        return plan
    
    def generate_kiro_debug_request(self, context, failure_type, plan):
        """Generate structured debug request for Kiro"""
        
        request = f"""
# Raptor Debug Request

**Agent**: Velociraptor v{self.version}
**Status**: {self.status}
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Failure Type**: {failure_type.upper()}

---

## Failure Context

**Symptom**: {context.get('failure_1', 'Not specified')}
**Expected**: {context.get('failure_2', 'Not specified')}
**Actual**: {context.get('failure_3', 'Not specified')}
**Started After**: {context.get('failure_4', 'Unknown')}
**Reproducible**: {context.get('failure_5', 'Unknown')}

---

## Diagnostic Plan

### Step 1: Reproduce Failure
Create minimal reproducible case:
- Strip away everything not related to failure
- Isolate to smallest code/config that fails
- Verify failure still occurs

### Step 2: Isolate Failure Point
Use binary search to find exact failure location:
- Add logging/prints to narrow down
- Comment out sections to isolate
- Identify the specific line/function that fails

### Step 3: Identify Root Cause
Distinguish symptom from cause:
- Symptom: "API returns 500"
- Cause: "Missing authentication header"

Ask "why" 5 times to find root cause.

### Step 4: Verify Fix Hypothesis
Before proposing fix:
- Confirm diagnosis with evidence
- Test hypothesis (if possible)
- Ensure fix addresses root cause, not symptom

### Step 5: Propose Minimal Fix
Smallest change that fixes the bug:
- No refactoring (unless that IS the bug)
- No feature additions
- No scope expansion
- Just fix the bug

---

## Debugging Guidelines

### When to Pause
Pause if:
- Cannot reproduce failure (need more context)
- Fix requires architecture change (route to Rex)
- Fix requires new feature (route to Theri + human approval)
- Root cause is external (API down, network issue)

### Constraint Enforcement
**Raptor does NOT**:
- Add features while fixing bugs
- Refactor unrelated code
- Optimize performance (unless that's the bug)
- Expand scope beyond the fix

**Raptor ONLY**:
- Diagnoses failures
- Proposes minimal fixes
- Verifies fixes work
- Reports if unfixable (external issue)

---

## Required Output

### 1. Reproduction Steps
```
Minimal reproduction:
1. [Step to reproduce]
2. [Step to reproduce]
3. [Failure occurs]
```

### 2. Root Cause Analysis
```
Symptom: [What user sees]
Immediate cause: [What directly causes symptom]
Root cause: [Why immediate cause exists]

Evidence:
- [Log line / error message]
- [Code inspection]
- [Test result]
```

### 3. Proposed Fix
```
Change needed:
- File: [path]
- Line: [number]
- Current: [what's there now]
- Fixed: [what it should be]

Why this fixes it:
- [Explanation of how fix addresses root cause]

Verification:
- [How to verify fix works]
```

### 4. Side Effects
```
Potential impacts:
- [What else might be affected]
- [Tests that should be run]
- [Areas to monitor]
```

---

## Constraint Reminder

**If you encounter**:
- "While fixing this, I should also..." → STOP, scope expansion
- "This needs architecture change..." → STOP, route to Rex
- "This requires new feature..." → STOP, route to Theri + human
- "The bug is in external system..." → STOP, report unfixable

**Raptor fixes bugs. Raptor doesn't add features, refactor, or redesign.**

---

**This request should be executed by Kiro in Raptor mode.**
**Raptor will diagnose and propose minimal fix.**
"""
        
        return request
    
    def log_execution(self, context, success, failure_type, notes=""):
        """Log execution to decisions.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
---
### Agent Execution: Velociraptor

**Timestamp**: {timestamp}
**Agent**: velociraptor v{self.version}
**Ark Type**: {self.ark_type}
**Status**: {self.status}
**Request**: {context.get('initial_request', 'Unknown')}
**Failure Type**: {failure_type}
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
            # Step 1: Gather failure context
            context = self.gather_failure_context(initial_request)
            if context is None:
                return False
            
            # Step 2: Classify failure type
            failure_type = self.classify_failure_type(context)
            
            # Step 3: Plan diagnosis
            plan = self.plan_diagnosis(context, failure_type)
            
            # Step 4: Generate Kiro debug request
            kiro_request = self.generate_kiro_debug_request(context, failure_type, plan)
            
            # Step 5: Output request
            print("\n" + "=" * 60)
            print("DEBUG REQUEST FOR KIRO")
            print("=" * 60)
            print(kiro_request)
            print("=" * 60)
            
            # Step 6: Save to file
            output_file = self.agent_dir / "last_debug_request.md"
            with open(output_file, 'w') as f:
                f.write(kiro_request)
            print(f"\n💾 Saved to: {output_file}")
            
            # Step 7: Get feedback
            print("\nWas this debug request well-structured? (y/n): ", end="")
            feedback = input().strip().lower()
            success = feedback == 'y'
            
            # Step 8: Log execution
            self.log_execution(context, success, failure_type,
                             notes="Generated debug request for Kiro execution")
            
            return success
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            self.log_execution({"initial_request": initial_request}, 
                             False, "unknown",
                             notes=f"Error: {str(e)}")
            return False


def main():
    """Entry point for Raptor agent"""
    if len(sys.argv) < 2:
        print("Usage: python raptor.py '<failure description>'")
        print("Example: python raptor.py 'API returns 500 error'")
        print("\nOr run in interactive mode:")
        print("  python raptor.py")
        sys.exit(1)
    
    if len(sys.argv) == 1:
        # Interactive mode
        print("Velociraptor (Raptor) - Interactive Mode")
        request = input("Failure description: ").strip()
    else:
        request = " ".join(sys.argv[1:])
    
    agent = Velociraptor()
    agent.run(request)


if __name__ == "__main__":
    main()
