#!/usr/bin/env python3
"""
Yutyrannus (Yuty) - GTM/Narrative Agent v1.0
Status: WORKING (Tier 2)

Narrative agent that:
1. Creates customer-facing explanations
2. Generates demo scripts and talking points
3. Translates technical to business value
4. NEVER overpromises or outruns evidence

Constraint: Evidence-based only, no overpromising.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class Yutyrannus:
    """GTM/Narrative Agent - Customer-Facing Communication"""
    
    def __init__(self):
        self.version = "1.0"
        self.ark_type = "ARK:Yutyrannus"
        self.status = "UNVALIDATED"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        
    def gather_narrative_context(self, initial_request):
        """Collect information about narrative needs"""
        print("\n🦖 Yutyrannus (Yuty) - GTM/Narrative Mode")
        print("=" * 60)
        print(f"\nNarrative request: {initial_request}")
        print("\nBefore I create narrative, I need context:\n")
        
        questions = [
            "Who is the audience? (technical/business/mixed)",
            "What's the goal? (convince/explain/demo/document)",
            "What evidence exists? (working code/research/architecture)",
            "What constraints? (time/format/medium)",
            "What must NOT be claimed? (avoid overpromising)"
        ]
        
        context = {"initial_request": initial_request}
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            answer = input("   → ").strip()
            if answer:
                context[f"narrative_{i}"] = answer
        
        if not context.get('narrative_1') or not context.get('narrative_2'):
            print("\n⚠️  INSUFFICIENT CONTEXT")
            print("Cannot create narrative without:")
            print("- Audience definition")
            print("- Clear goal")
            return None
        
        return context
    
    def validate_evidence(self, context):
        """Ensure claims are backed by evidence"""
        print("\n🔍 Evidence Validation:")
        
        evidence = context.get('narrative_3', 'None specified')
        print(f"   Available evidence: {evidence}")
        
        if evidence.lower() in ['none', 'none specified', '']:
            print("   ⚠️  WARNING: No evidence provided")
            print("   Narrative will be limited to documented capabilities only")
            return "limited"
        
        print("   ✓ Evidence available for claims")
        return "full"
    
    def plan_narrative(self, context, evidence_level):
        """Create narrative structure"""
        print("\n📋 Narrative Plan:")
        
        audience = context.get('narrative_1', 'Unknown')
        goal = context.get('narrative_2', 'Unknown')
        constraints = context.get('narrative_4', 'None')
        
        plan = {
            "audience": audience,
            "goal": goal,
            "evidence_level": evidence_level,
            "constraints": constraints,
            "structure": [
                "1. Hook (why this matters to audience)",
                "2. Problem statement (what pain exists)",
                "3. Solution overview (how we address it)",
                "4. Evidence (proof it works)",
                "5. Call to action (what happens next)"
            ],
            "guardrails": [
                "Every claim must cite evidence",
                "No future promises (only current capabilities)",
                "Technical accuracy over marketing language",
                "Acknowledge limitations explicitly"
            ]
        }
        
        print(f"   Audience: {plan['audience']}")
        print(f"   Goal: {plan['goal']}")
        print(f"   Evidence: {plan['evidence_level']}")
        print(f"\n   Structure:")
        for step in plan['structure']:
            print(f"   {step}")
        
        return plan
    
    def generate_kiro_narrative_request(self, context, evidence_level, plan):
        """Generate structured narrative request for Kiro"""
        
        request = f"""
# Yuty Narrative Request

**Agent**: Yutyrannus v{self.version}
**Status**: {self.status}
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Evidence Level**: {evidence_level.upper()}

---

## Narrative Context

**Audience**: {context.get('narrative_1', 'Not specified')}
**Goal**: {context.get('narrative_2', 'Not specified')}
**Evidence**: {context.get('narrative_3', 'Not specified')}
**Constraints**: {context.get('narrative_4', 'None')}
**Avoid**: {context.get('narrative_5', 'Not specified')}

---

## Narrative Structure

### 1. Hook (Why This Matters)
Create opening that resonates with audience:
- Connect to their pain point
- Show understanding of their context
- Promise value (backed by evidence)

### 2. Problem Statement
Articulate the problem clearly:
- What's broken/missing/inefficient
- Why current solutions fail
- Cost of inaction

### 3. Solution Overview
Explain how we address it:
- Core mechanism (how it works)
- Key differentiators (why it's better)
- Concrete benefits (what they gain)

### 4. Evidence
Prove it works:
- Working code/demos
- Measured results
- Real examples
- Limitations acknowledged

### 5. Call to Action
What happens next:
- Immediate next step
- Clear path forward
- Low-friction entry point

---

## Evidence Requirements

**CRITICAL**: Every claim must be backed by evidence.

**Evidence markers** (use these):
- `[Evidence: working code at path/to/file]`
- `[Evidence: measured result X]`
- `[Evidence: documented in file.md]`
- `[Evidence: demonstrated in demo]`

**If evidence is missing**:
- Reframe claim as hypothesis
- Acknowledge limitation
- Propose validation path

**Example**:
❌ "This system is 10x faster"
✓ "In our tests, this approach reduced latency from 500ms to 50ms [Evidence: benchmark results in results.md]"

---

## Constraint Enforcement

**Yuty does NOT**:
- Promise future features
- Claim unvalidated capabilities
- Use marketing language over technical accuracy
- Hide limitations

**Yuty ONLY**:
- Explains what exists now
- Cites evidence for claims
- Acknowledges gaps explicitly
- Translates technical to business value (with proof)

---

## Output Format

### Narrative Document

**Title**: [Clear, specific title]

**Audience**: {plan['audience']}
**Goal**: {plan['goal']}
**Duration/Length**: {context.get('narrative_4', 'Not specified')}

---

#### Hook
[Opening that resonates with audience]

[Evidence: ...]

---

#### Problem
[Clear problem statement]

[Evidence: ...]

---

#### Solution
[How we address it]

[Evidence: ...]

---

#### Proof
[Concrete evidence it works]

[Evidence: ...]

---

#### Next Steps
[Clear call to action]

---

### Evidence Audit

List all claims and their evidence:
1. Claim: [statement]
   Evidence: [source]
   Confidence: [high/medium/low]

2. Claim: [statement]
   Evidence: [source]
   Confidence: [high/medium/low]

---

## Constraint Reminder

**If you encounter**:
- "We could build..." → STOP, future promise
- "This will be..." → STOP, unvalidated claim
- "Industry-leading..." → STOP, marketing language without proof
- "Unlimited..." → STOP, acknowledge real constraints

**Yuty explains what exists. Yuty doesn't promise what doesn't.**

---

**This request should be executed by Kiro in Yuty mode.**
**Yuty will create evidence-based narrative.**
"""
        
        return request
    
    def log_execution(self, context, success, notes=""):
        """Log execution to decisions.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
---
### Agent Execution: Yutyrannus

**Timestamp**: {timestamp}
**Agent**: yutyrannus v{self.version}
**Ark Type**: {self.ark_type}
**Status**: {self.status}
**Request**: {context.get('initial_request', 'Unknown')}
**Audience**: {context.get('narrative_1', 'Unknown')}
**Goal**: {context.get('narrative_2', 'Unknown')}
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
            context = self.gather_narrative_context(initial_request)
            if context is None:
                return False
            
            evidence_level = self.validate_evidence(context)
            plan = self.plan_narrative(context, evidence_level)
            kiro_request = self.generate_kiro_narrative_request(context, evidence_level, plan)
            
            print("\n" + "=" * 60)
            print("NARRATIVE REQUEST FOR KIRO")
            print("=" * 60)
            print(kiro_request)
            print("=" * 60)
            
            output_file = self.agent_dir / "last_narrative_request.md"
            with open(output_file, 'w') as f:
                f.write(kiro_request)
            print(f"\n💾 Saved to: {output_file}")
            
            print("\nWas this narrative request well-structured? (y/n): ", end="")
            feedback = input().strip().lower()
            success = feedback == 'y'
            
            self.log_execution(context, success,
                             notes="Generated narrative request for Kiro execution")
            
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
        print("Usage: python yuty.py '<narrative request>'")
        print("Example: python yuty.py 'Create demo script for technical audience'")
        sys.exit(1)
    
    request = " ".join(sys.argv[1:])
    agent = Yutyrannus()
    agent.run(request)


if __name__ == "__main__":
    main()
