# Palette File Structure Reorganization Plan

**Goal**: Separate Palette toolkit (shareable, reusable) from Myth-Fall-Game project (uses Palette)

---

## Current State (Confusing)

```
/home/mical/fde/
├── decisions.md (toolkit decisions)
├── .kiro/steering/ (palette-core.md, assumptions.md)
├── taxonomy/ (111 RIUs)
├── kgdrs/
├── backups/
└── Myth-Fall-Game/ (nested project - WRONG)

/home/mical/Myth-Fall-Game/
├── fde/ (Palette files duplicated here)
│   ├── palette_knowledge_library_v1_0_FINAL.yaml
│   ├── agents/ (argentavis, rex)
│   ├── decisions.md (project decisions)
│   └── kgdrs/
├── PALETTE_VISION.md
├── PALETTE_DEMO_GUIDE.md
├── PALETTE_CONVERGENCE_CHECK.md
├── .kiro/steering/ (project-specific)
├── client/ (game code)
├── shared/ (game code)
└── legacy/ (game code)
```

**Problem**: Palette files scattered across two locations, unclear what's toolkit vs project

---

## Proposed Structure (Clean)

```
/home/mical/palette/                    # TOOLKIT (shareable, reusable)
├── README.md                           # "What is Palette"
├── VISION.md                           # Self-improving infrastructure vision
├── DEMO_GUIDE.md                       # How to demo Palette
├── CONVERGENCE_CHECK.md                # Alignment validation
├── .kiro/
│   └── steering/
│       ├── palette-core.md             # Tier 1: Core prompt
│       └── assumptions.md              # Tier 2: Agent definitions
├── taxonomy/
│   └── releases/
│       └── v1.0/
│           ├── palette_taxonomy_vnext.yaml  # 111 RIUs
│           └── palette_taxonomy_vnext.csv
├── knowledge-library/
│   └── v1.0/
│       └── palette_knowledge_library_v1_0_FINAL.yaml  # 86 Q&A
├── agents/                             # Agent implementations
│   ├── argentavis/
│   │   ├── agent.yaml
│   │   └── fixtures/
│   └── rex/
│       ├── agent.yaml
│       └── fixtures/
├── decisions.md                        # Toolkit development decisions (Tier 3)
├── kgdrs/
│   └── kges.md                         # Knowledge gap tracking
└── docs/
    ├── INSTALLATION.md
    └── GETTING_STARTED.md

/home/mical/projects/                   # PROJECTS (use Palette)
└── myth-fall-game/
    ├── README.md                       # Game-specific
    ├── .kiro/
    │   └── steering/
    │       ├── product.md              # Game product vision
    │       ├── tech.md                 # Game tech stack
    │       └── structure.md            # Game file structure
    ├── decisions.md                    # Game project decisions
    ├── client/                         # Game code
    ├── shared/                         # Game code
    ├── deployment/                     # Game deployment
    └── legacy/                         # Game legacy code

/home/mical/fde/                        # LEGACY (to be removed)
└── [archive or delete after migration]
```

---

## Migration Steps

### Step 1: Create Clean Palette Toolkit

```bash
# Create new Palette toolkit directory
mkdir -p /home/mical/palette/{.kiro/steering,taxonomy/releases/v1.0,knowledge-library/v1.0,agents,kgdrs,docs}

# Copy core files from /home/mical/fde/
cp /home/mical/fde/.kiro/steering/palette-core.md /home/mical/palette/.kiro/steering/
cp /home/mical/fde/.kiro/steering/assumptions.md /home/mical/palette/.kiro/steering/
cp /home/mical/fde/decisions.md /home/mical/palette/
cp /home/mical/fde/kgdrs/kges.md /home/mical/palette/kgdrs/

# Copy taxonomy
cp -r /home/mical/fde/taxonomy/releases/v1.0/* /home/mical/palette/taxonomy/releases/v1.0/

# Copy knowledge library from Myth-Fall-Game
cp /home/mical/Myth-Fall-Game/fde/palette_knowledge_library_v1_0_FINAL.yaml /home/mical/palette/knowledge-library/v1.0/

# Copy agents from Myth-Fall-Game
cp -r /home/mical/Myth-Fall-Game/fde/agents/* /home/mical/palette/agents/

# Copy documentation from Myth-Fall-Game
cp /home/mical/Myth-Fall-Game/PALETTE_VISION.md /home/mical/palette/VISION.md
cp /home/mical/Myth-Fall-Game/PALETTE_DEMO_GUIDE.md /home/mical/palette/DEMO_GUIDE.md
cp /home/mical/Myth-Fall-Game/PALETTE_CONVERGENCE_CHECK.md /home/mical/palette/CONVERGENCE_CHECK.md
```

### Step 2: Create Projects Directory

```bash
# Create projects directory
mkdir -p /home/mical/projects

# Move Myth-Fall-Game to projects (rename to lowercase with hyphens)
mv /home/mical/Myth-Fall-Game /home/mical/projects/myth-fall-game

# Remove Palette-specific files from project
rm /home/mical/projects/myth-fall-game/PALETTE_*.md
rm -rf /home/mical/projects/myth-fall-game/fde/agents
rm /home/mical/projects/myth-fall-game/fde/palette_knowledge_library_v1_0_FINAL.yaml
rm /home/mical/projects/myth-fall-game/fde/KNOWLEDGE_LIBRARY_*.md
rm /home/mical/projects/myth-fall-game/fde/extract_library.py
rm /home/mical/projects/myth-fall-game/fde/extracted_questions.yaml
rm /home/mical/projects/myth-fall-game/fde/palette_curated_knowledge_library_v1
rm /home/mical/projects/myth-fall-game/fde/knowledge_library.*

# Keep only project-specific decisions.md
# (already exists at /home/mical/projects/myth-fall-game/fde/decisions.md)
```

### Step 3: Create Palette README

Create `/home/mical/palette/README.md` explaining what Palette is and how to use it.

### Step 4: Archive Legacy FDE Directory

```bash
# Archive old fde directory
mv /home/mical/fde /home/mical/fde_archive_20260129
```

---

## Result: Clean Demo Structure

When you hand over your laptop, they see:

```
/home/mical/
├── palette/                    # "This is the toolkit I built"
│   ├── README.md               # Clear entry point
│   ├── VISION.md               # Why it exists
│   ├── DEMO_GUIDE.md           # How to demo it
│   ├── taxonomy/               # 111 RIUs
│   ├── knowledge-library/      # 86 Q&A
│   └── agents/                 # Agent implementations
│
└── projects/                   # "Here's how I use it"
    └── myth-fall-game/         # One project using Palette
        ├── .kiro/steering/     # Game-specific steering
        └── decisions.md        # Game-specific decisions
```

**Clear separation**: Palette is toolkit, Myth-Fall-Game is one project using it.

---

## Benefits

1. **Clarity**: "Here's Palette (toolkit), here's Myth-Fall-Game (project using it)"
2. **Shareability**: Can zip `/home/mical/palette/` and share with anyone
3. **Reusability**: Can create `/home/mical/projects/their-company/` using same toolkit
4. **Professionalism**: Clean structure shows this is production-ready, not a prototype
5. **Scalability**: Easy to add more projects without polluting toolkit

---

## ONE-WAY DOOR Decision Required

🚨 **Approve this migration plan before executing**

**Why ONE-WAY DOOR**: Moving files and restructuring is difficult to reverse. Need explicit approval.

**Alternatives**:
- Option A: Execute this plan (recommended)
- Option B: Keep current structure, just clean up duplicates
- Option C: Different structure (specify what you want)

**Recommendation**: Option A (Execute this plan)

---

## Execution Time

- Step 1 (Create Palette toolkit): 5 minutes
- Step 2 (Reorganize projects): 3 minutes
- Step 3 (Create README): 5 minutes
- Step 4 (Archive legacy): 1 minute

**Total**: ~15 minutes

---

**Awaiting approval to execute migration.**
