#!/usr/bin/env python3
"""
Argentavis (Argy) - Resource Gatherer Agent v1.0
Status: WORKING (Tier 2)

Conversational research agent that:
1. Checks knowledge library first
2. Clarifies intent before searching
3. Searches strategically
4. Synthesizes for decision-making
5. NEVER makes decisions or recommendations

Constraint: Read-only. No synthesis-as-decision. No execution.
"""

import json
import sys
import yaml
from datetime import datetime
from pathlib import Path


class Argentavis:
    """Resource Gatherer Agent - Clarify, Search, Synthesize"""
    
    def __init__(self):
        self.version = "1.0"
        self.ark_type = "ARK:Argentavis"
        self.status = "UNVALIDATED"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        self.knowledge_library_path = self.palette_root / "knowledge-library" / "v1.2" / "palette_knowledge_library_v1.2.yaml"
        
    def load_system_prompt(self):
        """Load agent personality and constraints"""
        prompt_path = self.agent_dir / "prompts" / "system.md"
        with open(prompt_path, 'r') as f:
            return f.read()
    
    def check_knowledge_library(self, request):
        """Check knowledge library before external search"""
        print("\n📚 Checking knowledge library first...")
        
        if not self.knowledge_library_path.exists():
            print("   ⚠️  Knowledge library not found")
            return None
        
        try:
            with open(self.knowledge_library_path, 'r') as f:
                library = yaml.safe_load(f)
            
            # Simple keyword matching (can be improved)
            request_lower = request.lower()
            matches = []
            
            for question in library.get('library_questions', []):
                q_text = question.get('question', '').lower()
                # Check if key terms overlap
                if any(word in q_text for word in request_lower.split() if len(word) > 4):
                    matches.append({
                        'id': question.get('id'),
                        'question': question.get('question'),
                        'answer': question.get('answer', '')[:200] + '...',  # Preview
                        'related_rius': question.get('related_rius', [])
                    })
            
            if matches:
                print(f"   ✓ Found {len(matches)} potentially relevant entries")
                for i, match in enumerate(matches[:3], 1):  # Show top 3
                    print(f"   {i}. {match['id']}: {match['question'][:80]}...")
                return matches
            else:
                print("   ℹ️  No direct matches in library")
                return None
                
        except Exception as e:
            print(f"   ⚠️  Error reading library: {e}")
            return None
    
    def clarify_intent(self, initial_request):
        """Ask clarifying questions before searching"""
        print("\n🔍 Argentavis (Argy) - Resource Gatherer")
        print("=" * 60)
        print(f"\nInitial request: {initial_request}")
        print("\nBefore I search, let me clarify:\n")
        
        questions = [
            "What decision is this research informing?",
            "What have you already tried or know?",
            "What would 'good enough' look like?",
            "What's the timeline/urgency?",
            "What will you do with these findings?"
        ]
        
        context = {"initial_request": initial_request}
        
        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            answer = input("   → ").strip()
            if answer:
                context[f"q{i}"] = answer
        
        return context
    
    def plan_search_strategy(self, context):
        """Plan multi-step search strategy"""
        print("\n🎯 Search Strategy:")
        
        strategy = {
            "primary_query": self._build_primary_query(context),
            "search_phases": [
                {
                    "phase": 1,
                    "focus": "Official documentation and technical specs",
                    "sources": ["AWS docs", "GitHub repos", "official guides"]
                },
                {
                    "phase": 2,
                    "focus": "Real-world examples and case studies",
                    "sources": ["Blog posts", "conference talks", "production stories"]
                },
                {
                    "phase": 3,
                    "focus": "Comparative analyses and tradeoffs",
                    "sources": ["Technical comparisons", "architecture reviews"]
                }
            ],
            "stop_conditions": [
                "Found 3+ reliable sources with consistent patterns",
                "Identified clear tradeoffs",
                "Answered the decision question"
            ]
        }
        
        print(f"   Primary query: {strategy['primary_query']}")
        for phase in strategy['search_phases']:
            print(f"   Phase {phase['phase']}: {phase['focus']}")
        
        return strategy
    
    def _build_primary_query(self, context):
        """Build focused search query from clarified context"""
        request = context['initial_request']
        decision = context.get('q1', '')
        
        # Combine request with decision context
        if decision:
            return f"{request} {decision}"
        return request
    
    def generate_kiro_search_request(self, context, strategy, library_matches=None):
        """Generate structured search request for Kiro to execute"""
        
        request = f"""
# Argentavis Research Request

**Agent**: Argentavis v{self.version}
**Status**: {self.status}
**Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Original Question
{context['initial_request']}

## Context
- **Decision**: {context.get('q1', 'Not specified')}
- **Already known**: {context.get('q2', 'Not specified')}
- **Success criteria**: {context.get('q3', 'Not specified')}
- **Timeline**: {context.get('q4', 'Not specified')}
- **Next action**: {context.get('q5', 'Not specified')}

---

## Knowledge Library Check
"""
        
        if library_matches:
            request += f"✓ Found {len(library_matches)} relevant entries:\n"
            for match in library_matches[:3]:
                request += f"- {match['id']}: {match['question']}\n"
                request += f"  RIUs: {', '.join(match['related_rius'])}\n"
            request += "\n**Recommendation**: Review these entries before external search.\n"
        else:
            request += "ℹ️  No direct matches in knowledge library. Proceeding to external search.\n"
        
        request += f"""
---

## Search Strategy

**Primary Query**: `{strategy['primary_query']}`

### Search Phases
"""
        
        for phase in strategy['search_phases']:
            request += f"\n**Phase {phase['phase']}**: {phase['focus']}\n"
            request += f"Sources: {', '.join(phase['sources'])}\n"
        
        request += """
### Stop Conditions
"""
        for condition in strategy['stop_conditions']:
            request += f"- {condition}\n"
        
        request += """
---

## Required Output Format

### 1. Key Findings (3-5 main points)
- Finding 1: [description]
  - Source: [URL]
  - Confidence: [High/Medium/Low]
  
### 2. Patterns Observed
- Pattern 1: [what multiple sources agree on]
- Pattern 2: [emerging trends]

### 3. Tradeoffs & Considerations
- Tradeoff 1: [X vs Y]
- Consideration 1: [important factor]

### 4. Gaps & Uncertainties
- What we still don't know
- Where sources conflict

### 5. Recommended Next Steps
- Immediate: [what to do now]
- Follow-up: [what to research next]

---

## Constraint Reminder
**Argy does NOT**:
- Make decisions or recommendations
- Synthesize findings into "you should do X"
- Execute or commit to actions

**Argy ONLY**:
- Gathers information
- Identifies patterns
- Surfaces tradeoffs
- Presents options

---

**This request should be executed by Kiro using web_search tool.**
**Argy will review and structure results once search completes.**
"""
        
        return request
    
    def log_execution(self, context, success, notes=""):
        """Log execution to decisions.md for maturity tracking"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
---
### Agent Execution: Argentavis

**Timestamp**: {timestamp}
**Agent**: argentavis v{self.version}
**Ark Type**: {self.ark_type}
**Status**: {self.status}
**Request**: {context['initial_request']}
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
            # Step 1: Check knowledge library
            library_matches = self.check_knowledge_library(initial_request)
            
            # Step 2: Clarify intent
            context = self.clarify_intent(initial_request)
            
            # Step 3: Plan search strategy
            strategy = self.plan_search_strategy(context)
            
            # Step 4: Generate Kiro search request
            kiro_request = self.generate_kiro_search_request(context, strategy, library_matches)
            
            # Step 5: Output request
            print("\n" + "=" * 60)
            print("SEARCH REQUEST FOR KIRO")
            print("=" * 60)
            print(kiro_request)
            print("=" * 60)
            
            # Step 6: Save to file for easy copy-paste
            output_file = self.agent_dir / "last_search_request.md"
            with open(output_file, 'w') as f:
                f.write(kiro_request)
            print(f"\n💾 Saved to: {output_file}")
            
            # Step 7: Get feedback
            print("\nWas this research request well-structured? (y/n): ", end="")
            feedback = input().strip().lower()
            success = feedback == 'y'
            
            # Step 8: Log execution
            self.log_execution(context, success, 
                             notes="Generated search request for Kiro execution")
            
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
    """Entry point for Argentavis agent"""
    if len(sys.argv) < 2:
        print("Usage: python argy.py '<research request>'")
        print("Example: python argy.py 'multiplayer game networking patterns'")
        print("\nOr run in interactive mode:")
        print("  python argy.py")
        sys.exit(1)
    
    if len(sys.argv) == 1:
        # Interactive mode
        print("Argentavis (Argy) - Interactive Mode")
        request = input("Research request: ").strip()
    else:
        request = " ".join(sys.argv[1:])
    
    agent = Argentavis()
    agent.run(request)


if __name__ == "__main__":
    main()
