#!/usr/bin/env python3
"""
Therizinosaurus (Theri) - Builder Agent v1.0
Status: UNVALIDATED (Tier 1)

Builder agent that:
1. Requires clear spec before building
2. Implements within bounded scope
3. Creates artifacts (code, configs, docs)
4. Tests what it builds
5. NEVER makes architecture decisions or expands scope

Constraint: Builds within spec. No architecture. No scope expansion.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class Therizinosaurus:
    """Builder Agent - Implement Within Bounded Scope"""
    
    def __init__(self):
        self.version = "1.0"
        self.ark_type = "ARK:Therizinosaurus"
        self.status = "UNVALIDATED"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        
    def validate_spec(self, initial_request):
        """Ensure spec is clear before building"""
        print("\n🦖 Therizinosaurus (Theri) - Builder Mode")
        print("=" * 60)
        print(f"\nBuild request: {initial_request}")
        print("\nBefore I build, I need a clear spec:\n")
        
        spec_questions = [
            "What exactly needs to be built? (specific artifact)",
            "What's the acceptance criteria? (how do we know it works)",
            "What's the scope boundary? (what's explicitly OUT of scope)",
            "What architecture/design decisions are already made?",
            "What should I do if I encounter an architecture decision?"
        ]
        
        spec = {"initial_request": initial_request}
        
        for i, question in enumerate(spec_questions, 1):
            print(f"{i}. {question}")
            answer = input("   → ").strip()
            if answer:
                spec[f"spec_{i}"] = answer
        
        # Validate spec completeness
        if not spec.get('spec_1') or not spec.get('spec_2'):
            print("\n⚠️  INSUFFICIENT SPEC")
            print("Cannot build without:")
            print("- Clear artifact definition (what to build)")
            print("- Acceptance criteria (how to verify)")
            print("\nRecommendation: Have Rex create architecture spec first")
            return None
        
        return spec
    
    def check_for_architecture_decisions(self, spec):
        """Detect if build requires architecture decisions"""
        print("\n🚪 Checking for architecture decisions...")
        
        architecture_keywords = [
            "choose", "decide", "which", "should we", "best way",
            "architecture", "design", "approach", "strategy"
        ]
        
        request_lower = spec['initial_request'].lower()
        needs_architecture = any(keyword in request_lower for keyword in architecture_keywords)
        
        if needs_architecture:
            print("   🚨 ARCHITECTURE DECISION DETECTED")
            print("   This request requires design decisions")
            print("   Recommendation: Route to Rex (Architect) first")
            return True
        
        print("   ✓ No architecture decisions detected")
        print("   Spec appears implementation-ready")
        return False
    
    def plan_implementation(self, spec):
        """Break down implementation into steps"""
        print("\n📋 Implementation Plan:")
        
        plan = {
            "artifact": spec.get('spec_1', 'Unknown'),
            "acceptance_criteria": spec.get('spec_2', 'Unknown'),
            "scope_boundary": spec.get('spec_3', 'Everything in spec'),
            "steps": [
                "1. Create file/directory structure",
                "2. Implement core functionality",
                "3. Add error handling",
                "4. Write basic tests",
                "5. Verify against acceptance criteria"
            ],
            "out_of_scope": [
                "Architecture decisions (route to Rex)",
                "Research (route to Argy)",
                "Debugging existing code (route to Raptor)",
                "Scope expansion beyond spec"
            ]
        }
        
        print(f"   Artifact: {plan['artifact']}")
        print(f"   Acceptance: {plan['acceptance_criteria']}")
        print(f"\n   Steps:")
        for step in plan['steps']:
            print(f"   {step}")
        
        return plan
    
    def generate_kiro_build_request(self, spec, plan):
        """Generate structured build request for Kiro to execute"""
        
        request = f"""
# Theri Build Request

**Agent**: Therizinosaurus v{self.version}
**Status**: {self.status}
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Build Specification

**Artifact**: {spec.get('spec_1', 'Not specified')}

**Acceptance Criteria**:
{spec.get('spec_2', 'Not specified')}

**Scope Boundary**:
{spec.get('spec_3', 'Everything in spec')}

**Architecture Decisions Already Made**:
{spec.get('spec_4', 'None specified')}

**If Architecture Decision Needed**:
{spec.get('spec_5', 'Pause and route to Rex')}

---

## Implementation Plan

### Steps
"""
        
        for step in plan['steps']:
            request += f"{step}\n"
        
        request += f"""
### Out of Scope (Will NOT Do)
"""
        
        for item in plan['out_of_scope']:
            request += f"- {item}\n"
        
        request += """
---

## Implementation Guidelines

### Code Quality Standards
- **Minimal**: Write only what's needed for acceptance criteria
- **Clear**: Code should be self-documenting
- **Tested**: Include basic verification
- **Error-handled**: Graceful failure, not silent errors

### When to Pause
Pause and request guidance if:
- Architecture decision needed (route to Rex)
- Spec is ambiguous (clarify with human)
- Scope expansion requested (confirm with human)
- External research needed (route to Argy)

### Constraint Enforcement
**Theri does NOT**:
- Make architecture decisions
- Expand scope beyond spec
- Research options or approaches
- Debug existing code (that's Raptor)

**Theri ONLY**:
- Implements within bounded scope
- Creates specified artifacts
- Tests against acceptance criteria
- Reports completion or blockers

---

## Required Output

### 1. Artifacts Created
List all files/directories created:
```
- path/to/file1.py
- path/to/file2.yaml
- path/to/test.py
```

### 2. Implementation Notes
- Key decisions made (within scope)
- Assumptions taken
- Edge cases handled

### 3. Verification Results
- Acceptance criteria met? (Y/N for each)
- Tests run and results
- Known limitations

### 4. Blockers Encountered (if any)
- What blocked progress
- What decision/research is needed
- Recommended next agent

---

## Constraint Reminder

**If you encounter**:
- "Should we use X or Y?" → STOP, route to Rex
- "What's the best way to..." → STOP, route to Rex
- "I need to research..." → STOP, route to Argy
- "This isn't working..." → STOP, route to Raptor

**Theri builds. Theri doesn't design, research, or debug.**

---

**This request should be executed by Kiro in Theri mode.**
**Theri will implement within spec and report completion.**
"""
        
        return request
    
    def log_execution(self, spec, success, notes=""):
        """Log execution to decisions.md for maturity tracking"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
---
### Agent Execution: Therizinosaurus

**Timestamp**: {timestamp}
**Agent**: therizinosaurus v{self.version}
**Ark Type**: {self.ark_type}
**Status**: {self.status}
**Request**: {spec.get('initial_request', 'Unknown')}
**Artifact**: {spec.get('spec_1', 'Unknown')}
**Outcome**: {'SUCCESS' if success else 'FAILURE'}
**Notes**: {notes}

**Impression Update**:
- success: {'+1' if success else '0'}
- fail: {'0' if success else '+1'}
- fail_gap: {'+1' if success else '0 (reset)'}

"""
        
        # Append to ledger
        try:
            with open(self.ledger_path, 'a') as f:
                f.write(log_entry)
            print(f"\n✅ Logged to {self.ledger_path}")
        except Exception as e:
            print(f"\n⚠️  Could not log to decisions.md: {e}")
    
    def run(self, initial_request):
        """Main execution flow"""
        try:
            # Step 1: Validate spec
            spec = self.validate_spec(initial_request)
            if spec is None:
                return False
            
            # Step 2: Check for architecture decisions
            needs_architecture = self.check_for_architecture_decisions(spec)
            if needs_architecture:
                print("\n⚠️  ROUTING REQUIRED")
                print("This request needs Rex (Architect) before Theri can build")
                self.log_execution(spec, False, 
                                 notes="Blocked: Architecture decision required, route to Rex")
                return False
            
            # Step 3: Plan implementation
            plan = self.plan_implementation(spec)
            
            # Step 4: Generate Kiro build request
            kiro_request = self.generate_kiro_build_request(spec, plan)
            
            # Step 5: Output request
            print("\n" + "=" * 60)
            print("BUILD REQUEST FOR KIRO")
            print("=" * 60)
            print(kiro_request)
            print("=" * 60)
            
            # Step 6: Save to file
            output_file = self.agent_dir / "last_build_request.md"
            with open(output_file, 'w') as f:
                f.write(kiro_request)
            print(f"\n💾 Saved to: {output_file}")
            
            # Step 7: Get feedback
            print("\nWas this build request well-structured? (y/n): ", end="")
            feedback = input().strip().lower()
            success = feedback == 'y'
            
            # Step 8: Log execution
            self.log_execution(spec, success,
                             notes="Generated build request for Kiro execution")
            
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
    """Entry point for Theri agent"""
    if len(sys.argv) < 2:
        print("Usage: python theri.py '<build request>'")
        print("Example: python theri.py 'implement user authentication'")
        print("\nOr run in interactive mode:")
        print("  python theri.py")
        sys.exit(1)
    
    if len(sys.argv) == 1:
        # Interactive mode
        print("Therizinosaurus (Theri) - Interactive Mode")
        request = input("Build request: ").strip()
    else:
        request = " ".join(sys.argv[1:])
    
    agent = Therizinosaurus()
    agent.run(request)


if __name__ == "__main__":
    main()
