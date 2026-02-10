# Palette Framework - Windows Quick Start

**Platform**: Windows, macOS, Linux (platform-agnostic)  
**Requirements**: Any AI assistant (Claude Desktop, Cursor, GitHub Copilot, ChatGPT)  
**No installation needed** - Just markdown files

---

## What You Downloaded

This is **not software** - it's a **decision framework** (markdown files).

Palette works with **any AI assistant** on **any platform**:
- ✅ Windows (Claude Desktop, Cursor, VS Code + Copilot)
- ✅ macOS (Claude Desktop, Cursor, VS Code + Copilot)
- ✅ Linux (Kiro CLI, Cursor, VS Code + Copilot)

---

## 5-Minute Setup (Windows)

### Option 1: Claude Desktop (Recommended)

1. **Extract this zip** to `C:\Users\YourName\palette\`

2. **Open Claude Desktop**

3. **Start a project**, paste this:
   ```
   I'm using the Palette framework. Load these files:
   - .kiro/steering/palette-core.md
   - .kiro/steering/assumptions.md
   
   I want to [describe your problem]
   ```

4. **Claude will use Palette** to help you solve it

---

### Option 2: Cursor / VS Code

1. **Extract this zip** to `C:\Users\YourName\palette\`

2. **Open folder in Cursor/VS Code**

3. **Add to AI context** (Ctrl+L in Cursor):
   ```
   @palette-core.md @assumptions.md
   
   I want to [describe your problem]
   ```

4. **AI will use Palette** to help you solve it

---

### Option 3: Any AI (ChatGPT, Copilot, etc.)

1. **Extract this zip** anywhere

2. **Copy/paste** `.kiro/steering/palette-core.md` into your AI chat

3. **Ask your question**

4. **AI will follow Palette principles**

---

## What's Inside

```
palette/
├── .kiro/steering/          # Core framework (3 files)
│   ├── palette-core.md      # Tier 1: Immutable principles
│   ├── assumptions.md       # Tier 2: Agent definitions
│   └── TIER3_decisions_prompt.md  # Tier 3: Decision template
│
├── taxonomy/                # 105 problem patterns
│   └── releases/v1.2/
│       └── palette_taxonomy_v1.2.yaml
│
├── knowledge-library/       # 93 validated Q&A
│   └── v1.2/
│       └── palette_knowledge_library_v1.2.yaml
│
├── company-library/         # 127 companies → RIUs
│   └── v1.0/
│       └── palette_company_riu_mapping_v1.0.yaml
│
├── agents/                  # 8 agent implementations
│   ├── argentavis/          # Research
│   ├── rex/                 # Architecture
│   ├── therizinosaurus/     # Build
│   ├── velociraptor/        # Debug
│   ├── yutyrannus/          # Narrative
│   ├── ankylosaurus/        # Validate
│   ├── parasaurolophus/     # Monitor
│   └── business-plan-creation/  # Composite agent
│
├── GETTING_STARTED.md       # Full guide
├── README.md                # Overview
└── WINDOWS_QUICK_START.md   # This file
```

---

## Common Confusion: "It's Linux-only"

**Not true.** Palette is markdown files - they work everywhere.

**What might be Linux-specific:**
- `.git/hooks/` (optional automation, not required)
- `scripts/*.sh` (optional tools, not required)
- `scripts/*.py` (optional, Python works on Windows too)

**Core Palette (what you need):**
- ✅ `.kiro/steering/*.md` - Works on Windows
- ✅ `taxonomy/*.yaml` - Works on Windows
- ✅ `knowledge-library/*.yaml` - Works on Windows
- ✅ `agents/*.md` - Works on Windows

---

## Example: Using Palette on Windows

**Scenario**: You want to build a customer support chatbot

**Step 1**: Open Claude Desktop, paste:
```
I'm using Palette. Load .kiro/steering/palette-core.md

I want to build a customer support chatbot for my SaaS product.
Help me converge on the problem first.
```

**Step 2**: Claude will:
1. Force convergence (Semantic Blueprint)
2. Match to RIU (probably RIU-031: Customer Support Automation)
3. Route to agents (Argy researches, Rex designs, Theri builds)
4. Log decisions (you track in decisions.md)

**Step 3**: You get:
- Clear problem definition
- Architecture options
- Implementation plan
- Decision log (restartable)

---

## Why It Works on Windows

Palette is **not a CLI tool** - it's a **collaboration framework**.

**What it is:**
- Markdown files with principles
- YAML files with patterns
- Agent definitions (text)

**What it's NOT:**
- A binary executable
- A Linux-specific tool
- Something that needs installation

**Think of it like:**
- A style guide (works everywhere)
- A design system (platform-agnostic)
- A decision framework (just text)

---

## Mythfall Example (Windows User)

Adam (Mythfall developer) uses Palette on Windows successfully:
- Uses Cursor on Windows
- Loads Palette agents as context
- Builds game features with agent help
- Logs decisions in `decisions.md`

**No Linux required.** Just AI + Palette files.

---

## If You're Still Stuck

**Problem**: "I can't integrate it with my Windows machine"

**Solution**: You don't "integrate" Palette - you **reference it**.

1. Extract zip to `C:\Users\YourName\palette\`
2. Open your AI tool (Claude, Cursor, Copilot)
3. Reference Palette files in your prompts
4. AI uses Palette to help you

**That's it.** No integration, no installation, no Linux.

---

## Next Steps

1. **Read** `GETTING_STARTED.md` (5 minutes)
2. **Try** a simple problem with your AI + Palette
3. **Log** your decision in `decisions.md`
4. **See** if it helps

If it doesn't work, the issue is **not Windows** - it's understanding what Palette is.

---

## Questions?

**"Do I need Python?"** - No (unless you want optional scripts)  
**"Do I need Git?"** - No (unless you want version control)  
**"Do I need Linux?"** - No (works on Windows, macOS, Linux)  
**"Do I need to install anything?"** - No (just extract and reference)

**Palette is text files.** If your AI can read text, Palette works.

---

**Welcome to Palette.** 🎨
