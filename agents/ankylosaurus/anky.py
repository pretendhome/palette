#!/usr/bin/env python3
"""
Ankylosaurus (Anky) - Validator Agent v1.0
Status: UNVALIDATED (Tier 1)

Validator agent that:
1. Reviews plans/specs/implementations
2. Identifies risks and gaps
3. Assesses readiness
4. NEVER remediates (assessment only)

Constraint: Assessment only, no remediation.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class Ankylosaurus:
    """Validator Agent - Risk Assessment and Gap Analysis"""
    
    def __init__(self):
        self.version = "1.0"
        self.ark_type = "ARK:Ankylosaurus"
        self.status = "UNVALIDATED"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        
    def gather_validation_context(self, initial_request):
        """Collect information about what needs validation"""
        print("\n🦖 Ankylosaurus (Anky) - Validator Mode")
        print("=" * 60)
        print(f"\nValidation request: {initial_request}")
        print("\nBefore I validate, I need context:\n")
        
        questions = [
            "What needs validation? (plan/spec/implementation/demo)",
            "What's the goal/purpose of this artifact?",
            "What are the success criteria?",
            "What constraints exist? (time/resources/technical)",
            "What's the risk tolerance? (low/medium/high)"
        ]
        
        context = {"initial_request": initial_request}
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            answer = input("   → ").strip()
            if answer:
                context[f"validation_{i}"] = answer
        
        if not context.get('validation_1') or not context.get('validation_3'):
            print("\n⚠️  INSUFFICIENT CONTEXT")
            print("Cannot validate without:")
            print("- What needs validation")
            print("- Success criteria")
            return None
        
        return context
    
    def classify_validation_type(self, context):
        """Determine what type of validation is needed"""
        print("\n🔍 Validation Type:")
        
        artifact = context.get('validation_1', '').lower()
        
        validation_types = {
            "plan": "Strategic validation (feasibility, completeness, risks)",
            "spec": "Technical validation (clarity, implementability, gaps)",
            "implementation": "Code validation (correctness, quality, edge cases)",
            "demo": "Presentation validation (flow, timing, clarity)"
        }
        
        for vtype, description in validation_types.items():
            if vtype in artifact:
                print(f"   Type: {vtype.upper()}")
                print(f"   Focus: {description}")
                return vtype
        
        print("   Type: GENERAL (comprehensive review)")
        return "general"
    
    def plan_validation(self, context, validation_type):
        """Create validation checklist"""
        print("\n📋 Validation Plan:")
        
        plan = {
            "artifact": context.get('validation_1', 'Unknown'),
            "goal": context.get('validation_2', 'Unknown'),
            "success_criteria": context.get('validation_3', 'Unknown'),
            "validation_type": validation_type,
            "checklist": [
                "1. Completeness (all required elements present)",
                "2. Clarity (unambiguous, understandable)",
                "3. Feasibility (can be executed with available resources)",
                "4. Risks (what could go wrong)",
                "5. Gaps (what's missing)",
                "6. Dependencies (what's required but not controlled)",
                "7. Readiness (go/no-go assessment)"
            ]
        }
        
        print(f"   Artifact: {plan['artifact']}")
        print(f"   Goal: {plan['goal']}")
        print(f"   Type: {plan['validation_type']}")
        print(f"\n   Checklist:")
        for item in plan['checklist']:
            print(f"   {item}")
        
        return plan
    
    def generate_kiro_validation_request(self, context, validation_type, plan):
        """Generate structured validation request for Kiro"""
        
        request = f"""
# Anky Validation Request

**Agent**: Ankylosaurus v{self.version}
**Status**: {self.status}
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Validation Type**: {validation_type.upper()}

---

## Validation Context

**Artifact**: {context.get('validation_1', 'Not specified')}
**Goal**: {context.get('validation_2', 'Not specified')}
**Success Criteria**: {context.get('validation_3', 'Not specified')}
**Constraints**: {context.get('validation_4', 'None')}
**Risk Tolerance**: {context.get('validation_5', 'Medium')}

---

## Validation Framework

### 1. Completeness Check
Review all required elements:
- Are all components present?
- Is anything obviously missing?
- Are dependencies identified?

**Output**: List of missing elements (if any)

### 2. Clarity Assessment
Evaluate understandability:
- Is the artifact unambiguous?
- Can someone else execute this?
- Are terms defined?

**Output**: List of unclear/ambiguous areas

### 3. Feasibility Analysis
Assess executability:
- Can this be done with available resources?
- Are timelines realistic?
- Are technical approaches sound?

**Output**: Feasibility rating (HIGH/MEDIUM/LOW) with rationale

### 4. Risk Identification
Find what could go wrong:
- Technical risks (implementation challenges)
- Resource risks (time/people/tools)
- Dependency risks (external factors)
- Assumption risks (unvalidated premises)

**Output**: Risk register with severity (CRITICAL/HIGH/MEDIUM/LOW)

### 5. Gap Analysis
Identify what's missing:
- Missing specifications
- Unaddressed edge cases
- Incomplete documentation
- Unvalidated assumptions

**Output**: Gap list with impact assessment

### 6. Dependency Mapping
List external requirements:
- What must exist before this can proceed?
- What's outside our control?
- What could block progress?

**Output**: Dependency list with mitigation strategies

### 7. Readiness Assessment
Go/no-go decision:
- Are critical risks mitigated?
- Are blocking gaps addressed?
- Is the artifact ready for next phase?

**Output**: GO / NO-GO / CONDITIONAL with clear rationale

---

## Risk Severity Definitions

**CRITICAL**: Blocks execution, must be resolved before proceeding
**HIGH**: Likely to cause failure, should be resolved before proceeding
**MEDIUM**: Could cause issues, should be addressed but not blocking
**LOW**: Minor concern, can be addressed during execution

---

## Output Format

### Validation Report

**Artifact**: {plan['artifact']}
**Validation Date**: {datetime.now().strftime("%Y-%m-%d")}
**Validator**: Ankylosaurus v{self.version}

---

#### 1. Completeness
✓ Present: [list]
✗ Missing: [list]

#### 2. Clarity
✓ Clear: [areas]
⚠️  Ambiguous: [areas]

#### 3. Feasibility
Rating: [HIGH/MEDIUM/LOW]
Rationale: [explanation]

#### 4. Risks
**CRITICAL**: [list or NONE]
**HIGH**: [list or NONE]
**MEDIUM**: [list]
**LOW**: [list]

#### 5. Gaps
1. [Gap description] - Impact: [HIGH/MEDIUM/LOW]
2. [Gap description] - Impact: [HIGH/MEDIUM/LOW]

#### 6. Dependencies
1. [Dependency] - Status: [SATISFIED/AT-RISK/BLOCKED]
2. [Dependency] - Status: [SATISFIED/AT-RISK/BLOCKED]

#### 7. Readiness Assessment
**Decision**: GO / NO-GO / CONDITIONAL

**Rationale**: [clear explanation]

**Conditions** (if CONDITIONAL):
1. [Condition that must be met]
2. [Condition that must be met]

---

### Recommendations

**Must address** (blocking):
1. [Recommendation]

**Should address** (important):
1. [Recommendation]

**Could address** (nice-to-have):
1. [Recommendation]

---

## Constraint Enforcement

**Anky does NOT**:
- Fix identified issues (that's remediation)
- Implement recommendations (that's execution)
- Make decisions on behalf of others (that's authority)
- Proceed past assessment phase

**Anky ONLY**:
- Identifies risks and gaps
- Assesses readiness
- Provides recommendations
- Delivers go/no-go assessment

**If asked to fix issues, respond**:
> "⚠️ CONSTRAINT VIOLATION - I'm a validator (assessment only). I identified [issue], but fixing it must route to [appropriate agent]. Recommendation: Address [issue] with [agent], then re-validate."

---

**This request should be executed by Kiro in Anky mode.**
**Anky will assess and report, not remediate.**
"""
        
        return request
    
    def log_execution(self, context, success, notes=""):
        """Log execution to decisions.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
---
### Agent Execution: Ankylosaurus

**Timestamp**: {timestamp}
**Agent**: ankylosaurus v{self.version}
**Ark Type**: {self.ark_type}
**Status**: {self.status}
**Request**: {context.get('initial_request', 'Unknown')}
**Artifact**: {context.get('validation_1', 'Unknown')}
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
            context = self.gather_validation_context(initial_request)
            if context is None:
                return False
            
            validation_type = self.classify_validation_type(context)
            plan = self.plan_validation(context, validation_type)
            kiro_request = self.generate_kiro_validation_request(context, validation_type, plan)
            
            print("\n" + "=" * 60)
            print("VALIDATION REQUEST FOR KIRO")
            print("=" * 60)
            print(kiro_request)
            print("=" * 60)
            
            output_file = self.agent_dir / "last_validation_request.md"
            with open(output_file, 'w') as f:
                f.write(kiro_request)
            print(f"\n💾 Saved to: {output_file}")
            
            print("\nWas this validation request well-structured? (y/n): ", end="")
            feedback = input().strip().lower()
            success = feedback == 'y'
            
            self.log_execution(context, success,
                             notes="Generated validation request for Kiro execution")
            
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
        print("Usage: python anky.py '<validation request>'")
        print("Example: python anky.py 'Validate demo plan for technical audience'")
        sys.exit(1)
    
    request = " ".join(sys.argv[1:])
    agent = Ankylosaurus()
    agent.run(request)


if __name__ == "__main__":
    main()
