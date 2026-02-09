#!/usr/bin/env python3
"""
Tyrannosaurus Rex (Rex) - Architect Agent v1.0
Status: UNVALIDATED (Tier 1)

Architecture agent that:
1. Clarifies constraints before designing
2. Evaluates multiple options (never just one)
3. Surfaces tradeoffs explicitly
4. Flags ONE-WAY DOOR decisions
5. Recommends with reasoning (but doesn't decide)

Constraint: Proposes designs, doesn't implement or decide.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class TyrannosaurusRex:
    """Architect Agent - Options, Tradeoffs, Recommendations"""
    
    def __init__(self):
        self.version = "1.0"
        self.ark_type = "ARK:Tyrannosaurus"
        self.status = "UNVALIDATED"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        
    def clarify_constraints(self, initial_request):
        """Understand problem and constraints before designing"""
        print("\n🦖 Tyrannosaurus Rex (Rex) - Architect Mode")
        print("=" * 60)
        print(f"\nArchitecture request: {initial_request}")
        print("\nBefore I design, let me understand the constraints:\n")
        
        questions = [
            "What system or decision needs architecture?",
            "What constraints exist? (technical, budget, timeline, team size)",
            "What are the success criteria?",
            "What have you already ruled out or decided?",
            "What's the risk tolerance? (experimental vs proven tech)"
        ]
        
        context = {"initial_request": initial_request}
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            answer = input("   → ").strip()
            if answer:
                context[f"constraint_{i}"] = answer
        
        return context
    
    def classify_decision(self, context):
        """Determine if this is a ONE-WAY DOOR or TWO-WAY DOOR decision"""
        print("\n🚪 Decision Classification:")
        
        one_way_indicators = [
            "database", "engine", "platform", "architecture", "network",
            "authentication", "deployment", "core", "foundation"
        ]
        
        request_lower = context['initial_request'].lower()
        is_one_way = any(indicator in request_lower for indicator in one_way_indicators)
        
        if is_one_way:
            print("   🚨 ONE-WAY DOOR detected")
            print("   This decision is difficult/expensive to reverse")
            print("   Will require explicit confirmation before proceeding")
            return "ONE_WAY_DOOR"
        else:
            print("   🔄 TWO-WAY DOOR")
            print("   This decision is reversible with reasonable effort")
            return "TWO_WAY_DOOR"
    
    def generate_options(self, context):
        """Generate 2-4 viable options with initial assessment"""
        print("\n📋 Generating Architecture Options...")
        print("   (This would normally involve research or knowledge base lookup)")
        print("   For standalone mode, outputting template for Kiro execution")
        
        # In standalone mode, we generate a template
        # In Kiro mode, this would actually evaluate options
        
        options_template = {
            "context": context,
            "options_needed": "2-4 viable options",
            "for_each_option": {
                "name": "Option name",
                "description": "What it is",
                "pros": ["Advantage 1", "Advantage 2"],
                "cons": ["Disadvantage 1", "Disadvantage 2"],
                "best_for": "Specific use case",
                "worst_for": "Specific use case",
                "complexity": "LOW | MEDIUM | HIGH",
                "cost": "$ | $$ | $$$",
                "team_size": "Estimate",
                "reversibility": "Easy | Moderate | Hard",
                "examples": ["Real-world example 1", "Real-world example 2"]
            },
            "note": "Rex needs Argy research or knowledge base to populate real options"
        }
        
        return options_template
    
    def generate_kiro_architecture_request(self, context, decision_type, options_template):
        """Generate structured architecture request for Kiro to execute"""
        
        request = f"""
# Rex Architecture Request

**Agent**: Tyrannosaurus Rex v{self.version}
**Status**: {self.status}
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Decision Type**: {decision_type}

---

## Architecture Problem
{context['initial_request']}

## Constraints
- **System/Decision**: {context.get('constraint_1', 'Not specified')}
- **Constraints**: {context.get('constraint_2', 'Not specified')}
- **Success Criteria**: {context.get('constraint_3', 'Not specified')}
- **Already Decided**: {context.get('constraint_4', 'Not specified')}
- **Risk Tolerance**: {context.get('constraint_5', 'Not specified')}

---

## Decision Classification

**{decision_type}**

"""
        
        if decision_type == "ONE_WAY_DOOR":
            request += """
⚠️ This is an irreversible or high-cost-to-change decision.

**Implications**:
- Requires explicit human confirmation before proceeding
- Must document reasoning in decisions.md
- Should evaluate 3-4 options minimum
- Must surface risks and mitigation strategies

"""
        
        request += """
---

## Required Analysis

### Stage 1: Gradient Descent (Find Options)
Identify 2-4 viable options. For each option:
- What it is (brief description)
- Why it's viable (passes hard constraints)
- Initial assessment (rough pros/cons)

Eliminate non-starters and explain why.

### Stage 2: Game Theory (Competitive Analysis)
Play options against each other:
- Option A vs Option B: When does each win?
- Option A vs Option C: What weakness in A does C expose?
- Option A vs Option D: What scenarios favor D?

Result: Which option survives competitive analysis and why?

### Stage 3: Integration Reasoning (System Fit)
For the leading option(s):
- **Constrains future decisions**: What becomes harder/impossible?
- **Integrates with existing**: How does this fit current architecture?
- **Enables downstream**: What becomes possible?
- **Prevents downstream**: What becomes impossible?
- **Conflicts detected**: Any integration issues?
- **Cooperation opportunities**: How does this strengthen the system?

---

## Required Output Format

For each viable option:

```
## Option [N]: [Name]

**What it is**: [Brief description]

**Pros**:
- [Advantage with context]
- [Advantage with context]

**Cons**:
- [Disadvantage with context]
- [Disadvantage with context]

**Best for**: [Specific use case]
**Worst for**: [Specific use case]
**Complexity**: LOW | MEDIUM | HIGH
**Cost**: $ | $$ | $$$
**Team size needed**: [Estimate]
**Reversibility**: Easy | Moderate | Hard
**Real-world examples**: [Projects that used this]
```

---

## Recommendation Format

```
## Recommendation

Based on your constraints:
- [Constraint 1]
- [Constraint 2]

I recommend: **[Option X]**

**Why**:
- [Reason tied to constraints]
- [Reason tied to success criteria]

**Risks**:
- [What could go wrong]
- [Mitigation strategy]

**If this is wrong**:
- Signal: [What would indicate this choice failed]
- Pivot: [How to change course if needed]
```

"""
        
        if decision_type == "ONE_WAY_DOOR":
            request += """
🚨 **ONE-WAY DOOR CONFIRMATION REQUIRED**

Before proceeding with implementation, human must explicitly confirm:
- Understands this decision is difficult to reverse
- Has reviewed all options and tradeoffs
- Accepts the risks and mitigation strategies
- Approves moving forward with recommended option

"""
        
        request += """
---

## Constraint Reminder

**Rex does NOT**:
- Implement solutions (that's Theri's job)
- Research options (that's Argy's job)
- Make final decisions (human confirms)
- Present only one option (always show alternatives)

**Rex ONLY**:
- Evaluates options
- Surfaces tradeoffs
- Recommends with reasoning
- Flags ONE-WAY DOORS

---

**This request should be executed by Kiro in Rex mode.**
**Rex will review and refine architecture once analysis completes.**
"""
        
        return request
    
    def log_execution(self, context, success, decision_type, notes=""):
        """Log execution to decisions.md for maturity tracking"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
---
### Agent Execution: Tyrannosaurus Rex

**Timestamp**: {timestamp}
**Agent**: rex v{self.version}
**Ark Type**: {self.ark_type}
**Status**: {self.status}
**Request**: {context['initial_request']}
**Decision Type**: {decision_type}
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
            # Step 1: Clarify constraints
            context = self.clarify_constraints(initial_request)
            
            # Step 2: Classify decision type
            decision_type = self.classify_decision(context)
            
            # Step 3: Generate options template
            options_template = self.generate_options(context)
            
            # Step 4: Generate Kiro architecture request
            kiro_request = self.generate_kiro_architecture_request(
                context, decision_type, options_template
            )
            
            # Step 5: Output request
            print("\n" + "=" * 60)
            print("ARCHITECTURE REQUEST FOR KIRO")
            print("=" * 60)
            print(kiro_request)
            print("=" * 60)
            
            # Step 6: Save to file
            output_file = self.agent_dir / "last_architecture_request.md"
            with open(output_file, 'w') as f:
                f.write(kiro_request)
            print(f"\n💾 Saved to: {output_file}")
            
            # Step 7: Get feedback
            print("\nWas this architecture request well-structured? (y/n): ", end="")
            feedback = input().strip().lower()
            success = feedback == 'y'
            
            # Step 8: Log execution
            self.log_execution(context, success, decision_type,
                             notes="Generated architecture request for Kiro execution")
            
            return success
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            self.log_execution({"initial_request": initial_request}, 
                             False, "UNKNOWN",
                             notes=f"Error: {str(e)}")
            return False


def main():
    """Entry point for Rex agent"""
    if len(sys.argv) < 2:
        print("Usage: python rex.py '<architecture request>'")
        print("Example: python rex.py 'multiplayer networking architecture'")
        print("\nOr run in interactive mode:")
        print("  python rex.py")
        sys.exit(1)
    
    if len(sys.argv) == 1:
        # Interactive mode
        print("Tyrannosaurus Rex (Rex) - Interactive Mode")
        request = input("Architecture request: ").strip()
    else:
        request = " ".join(sys.argv[1:])
    
    agent = TyrannosaurusRex()
    agent.run(request)


if __name__ == "__main__":
    main()
