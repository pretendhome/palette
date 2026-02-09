# Palette Toolkit - Installation Guide

**Package**: palette-toolkit-v1.0.zip  
**Size**: ~296 KB  
**Setup Time**: 5 minutes

---

## What You're Getting

A complete AI agent toolkit with:
- 7 specialized agents with hard constraints
- 104 RIUs (Reusable Intervention Units)
- 86-question knowledge library
- Three-tier decision system
- Full demo script
- All documentation

---

## Installation Steps

### 1. Extract the ZIP
```bash
unzip palette-toolkit-v1.0.zip
cd palette/
```

### 2. Open in Your AI Tool

**Option A: Claude Desktop / Claude Code**
- Open the `palette/` folder
- Tell Claude: "Read ONBOARDING.md"
- Type: **"start"**

**Option B: Cursor**
- Open `palette/` as workspace
- Tell Cursor: "Read ONBOARDING.md"
- Type: **"start"**

**Option C: Kiro CLI**
```bash
cd palette/
kiro-cli chat
```
Then: "Read ONBOARDING.md" and type **"start"**

**Option D: Any AI with File Access**
- Point your AI to the `palette/` folder
- Load: "Read ONBOARDING.md"
- Type: **"start"**

---

## Quick Start (Just Type "start")

Once you've opened the palette folder in your AI:

1. Tell your AI: "Read ONBOARDING.md"
2. Type: **"start"**
3. Follow the 15-minute interactive onboarding

The onboarding will:
- Explain what Palette is
- Show you agents enforcing boundaries (live)
- Teach you how to use agents
- Guide you to next steps

**That's it! Just type "start" and we'll take you through everything.**

---

## Quick Test (30 seconds)

**Step 1**: Tell your AI:
```
Load agents/argentavis/argentavis.md and become Argentavis
```

**Step 2**: Ask:
```
Which database should we use for our project?
```

**Step 3**: Expected response:
```
⚠️ CONSTRAINT VIOLATION

I'm a research agent (ARK:Argentavis) with read-only access. 
I can provide findings on database options, but I cannot make 
architecture decisions.

Architecture decisions must route to Tyrannosaurus (Rex).
```

**If you see this response, Palette is working!** ✅

---

## What to Do Next

1. **Read the Quick Start**: Open `README_QUICKSTART.md`
2. **Test all 7 agents**: Try each agent's constraint enforcement
3. **Run the demo**: Follow `DEMO_GUIDE_REVISED.md` (40 minutes)
4. **Read the vision**: See `VISION.md` for long-term potential

---

## File Structure

```
palette/
├── README_QUICKSTART.md     ← START HERE
├── DEMO_GUIDE_REVISED.md    ← Full demo script
├── VISION.md                ← Long-term vision
├── .kiro/steering/          ← Core system (Tier 1 & 2)
├── agents/                  ← 7 agent implementations
├── taxonomy/releases/v1.2/  ← 104 RIUs
├── knowledge-library/v1.2/  ← 86 questions
└── decisions.md             ← Execution log
```

---

## Troubleshooting

**"My AI isn't following the agent constraints"**
- Make sure the agent markdown file is fully loaded
- Try: "You are now Argentavis. Follow ALL constraints in the file."
- Check that your AI has file reading capability

**"Can't find the files"**
- Verify you extracted the ZIP completely
- Check you're in the `palette/` directory
- Try using absolute paths

**"Agent switching (#argy) doesn't work"**
- Agent switching only works in Kiro CLI
- For other AIs, load agent markdown files directly

---

## Support

This is an open toolkit. Questions or issues?
- Check `README_QUICKSTART.md` for detailed instructions
- Review `DEMO_GUIDE_REVISED.md` for examples
- All agents have detailed constraint documentation

---

## Quick Reference: Agent Commands

**For Kiro CLI** (with steering files):
```
#argy    - Switch to Argentavis (research)
#rex     - Switch to Rex (architect)
#theri   - Switch to Therizinosaurus (builder)
#raptor  - Switch to Velociraptor (debugger)
#yuty    - Switch to Yutyrannus (narrative)
#anky    - Switch to Ankylosaurus (validator)
#para    - Switch to Parasaurolophus (monitor)
#kiro    - Return to normal
```

**For Other AIs**:
```
Load agents/argentavis/argentavis.md and become Argentavis
Load agents/rex/rex.md and become Tyrannosaurus Rex
Load agents/therizinosaurus/therizinosaurus.md and become Therizinosaurus
[etc.]
```

---

**Ready to start?**

Open `README_QUICKSTART.md` and follow the 5-minute setup guide.

**That's it. You're ready to use Palette.**
