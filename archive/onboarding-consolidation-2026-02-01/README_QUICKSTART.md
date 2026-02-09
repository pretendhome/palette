# Palette - AI Agent Toolkit

**Version**: 1.0  
**Status**: Production-ready for evaluation  
**Setup Time**: 5 minutes

---

## What Is Palette?

Palette is a three-tier decision system that turns AI from a chatbot into a reliable field partner through:

1. **Convergence-first** - Forces clarity before execution
2. **Bounded agents** - 7 specialized agents with hard constraints
3. **Glass-box reasoning** - Every decision is traceable
4. **Empirical trust** - Agents earn autonomy through measured performance

---

## Quick Start (5 minutes)

### Step 1: Extract Files
Extract this ZIP to your preferred location.

### Step 2: Open in Your AI Tool
- **Claude Desktop**: Open the `palette/` folder
- **Cursor**: Open the `palette/` folder as workspace
- **Kiro CLI**: `cd palette && kiro-cli chat`
- **Any AI with file access**: Point it to the `palette/` folder

### Step 3: Load Core System
Tell your AI to read these files in order:

```
1. Read .kiro/steering/palette-core.md
2. Read .kiro/steering/assumptions.md
3. Read decisions.md (last 100 lines)
```

### Step 4: Test Agent Switching
Try switching to an agent:

```
Load agents/argentavis/argentavis.md and become Argentavis
```

Then ask: "Which database should we use?"

The agent should refuse and route to Rex (architect).

---

## What's Included

### Core System (3 files)
- `.kiro/steering/palette-core.md` - Tier 1: Immutable rules
- `.kiro/steering/assumptions.md` - Tier 2: Agent definitions
- `decisions.md` - Tier 3: Execution log

### Agents (7 implemented)
- `agents/argentavis/` - Argy (research, read-only)
- `agents/rex/` - Rex (architect, flags ONE-WAY DOORS)
- `agents/therizinosaurus/` - Theri (builder, bounded scope)
- `agents/velociraptor/` - Raptor (debugger, fix only)
- `agents/yutyrannus/` - Yuty (narrative, evidence-based)
- `agents/ankylosaurus/` - Anky (validator, assessment only)
- `agents/parasaurolophus/` - Para (monitor, signals only)

### Knowledge Assets
- `taxonomy/releases/v1.2/` - 104 RIUs (Reusable Intervention Units)
- `knowledge-library/v1.2/` - 86 questions with answers and sources

### Documentation
- `README.md` - This file
- `DEMO_GUIDE_REVISED.md` - 40-minute demo with live agent switching
- `VISION.md` - Self-improving infrastructure vision

---

## How to Use Agents

### Method 1: Load Agent Markdown (Any AI)
```
Load agents/argentavis/argentavis.md and become Argentavis
```

The AI will adopt that agent's constraints and behavior.

### Method 2: Run Python Script (Kiro CLI)
```bash
python agents/argentavis/argy.py "research demo strategies"
```

Generates a structured request for the AI to execute.

### Method 3: Agent Switching (Kiro CLI with steering files)
```
#argy          # Switch to Argentavis
#rex           # Switch to Rex
#theri         # Switch to Therizinosaurus
#raptor        # Switch to Velociraptor
#yuty          # Switch to Yutyrannus
#anky          # Switch to Ankylosaurus
#para          # Switch to Parasaurolophus
#kiro          # Return to normal
```

---

## Agent Constraints (Quick Reference)

| Agent | Role | Can Do | Cannot Do |
|-------|------|--------|-----------|
| **Argy** | Research | Search, retrieve, gather context | Make decisions, execute, recommend |
| **Rex** | Architect | Design, evaluate tradeoffs | Execute, commit without approval |
| **Theri** | Builder | Implement from specs | Make architecture decisions, guess |
| **Raptor** | Debugger | Diagnose, fix bugs | Add features, change architecture |
| **Yuty** | Narrative | Create customer content | Overpromise, claim without evidence |
| **Anky** | Validator | Assess, identify issues | Fix issues, implement changes |
| **Para** | Monitor | Observe, emit signals | Interpret, diagnose, fix |

---

## Try the Demo

Run the full 40-minute demo:

```
Open DEMO_GUIDE_REVISED.md and follow the script
```

The demo proves:
- Agents enforce their own boundaries
- ONE-WAY DOOR pausing works
- Convergence-first is enforced
- The system is real, not slides

---

## Example: First Agent Interaction

**1. Load Argentavis:**
```
Load agents/argentavis/argentavis.md and become Argentavis
```

**2. Ask an architecture question:**
```
Which database should we use for our project?
```

**3. Expected response:**
```
⚠️ CONSTRAINT VIOLATION

I'm a research agent (ARK:Argentavis) with read-only access. 
I can provide findings on database options, but I cannot make 
architecture decisions.

Architecture decisions must route to Tyrannosaurus (Rex).

Would you like me to gather research on database options for 
Rex to evaluate?
```

**This proves constraint enforcement works.**

---

## File Structure

```
palette/
├── .kiro/steering/          # Tier 1 & 2 (core system)
├── agents/                  # 7 agent implementations
│   ├── argentavis/
│   ├── rex/
│   ├── therizinosaurus/
│   ├── velociraptor/
│   ├── yutyrannus/
│   ├── ankylosaurus/
│   └── parasaurolophus/
├── taxonomy/releases/v1.2/  # 104 RIUs
├── knowledge-library/v1.2/  # 86 questions
├── decisions.md             # Execution log
├── README.md                # This file
├── DEMO_GUIDE_REVISED.md    # Full demo script
└── VISION.md                # Long-term vision
```

---

## Troubleshooting

### "Agent isn't refusing out-of-scope requests"
- Ensure the agent markdown file is fully loaded
- Check that the AI is following the constraints section
- Try being more explicit: "You are now Argentavis. Follow all constraints."

### "Can't find the files"
- Verify you extracted the ZIP completely
- Check you're in the `palette/` directory
- Use absolute paths if relative paths don't work

### "Agent switching doesn't work"
- Agent switching (`#argy`) only works in Kiro CLI with steering files
- For other AIs, use Method 1 (load agent markdown directly)

---

## Next Steps

1. **Test all 7 agents** - Load each agent and test constraint enforcement
2. **Run the demo** - Follow DEMO_GUIDE_REVISED.md
3. **Read the vision** - See VISION.md for long-term potential
4. **Build your own agent** - Use existing agents as templates

---

## Support & Feedback

This is an open toolkit. Modify, extend, and adapt it to your needs.

**Key principle**: Agents earn trust through measured performance, not promises.

---

## License

Open for evaluation and use. Modify as needed.

---

**Ready to start?**

1. Load `.kiro/steering/palette-core.md`
2. Load `agents/argentavis/argentavis.md`
3. Ask: "Which database should we use?"
4. Watch the agent refuse and route to Rex

**That's Palette. Constraint enforcement that actually works.**
