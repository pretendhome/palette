# Mythfall — Palette + Kiro Steering SOP (Implementation & Sync)  
**Version:** v1.3 (taxonomy v1.1) - FINAL  
**Repo:** `jkj9786/Myth-Fall-Game` (branch: `main`)  
**Local (Mical):** `/home/mical/Documents/mythfall/`  
**Local (Adam):** Windows path (repo clone)

This SOP makes the **GitHub repo** the **single source of truth**, and provides a repeatable, low-friction way to keep **three codebases in sync**:

1) GitHub repository (`main`)  
2) Mical's local clone (Linux)  
3) Adam's local clone (Windows)

It also adds **Mythfall-only Palette infrastructure** to Kiro without breaking the existing project steering.

---

## 0) Pre-Flight: Normalize Source Filenames FIRST

**CRITICAL**: Before copying anything to the repo, rename all source files to clean, normalized names:

```bash
cd /home/mical/Documents/mythfall/

# Rename Palette files to match canonical naming
mv "palette-core.md" TIER1_palette_core.md 2>/dev/null || true
mv "assumptions.md" TIER2_assumptions.md 2>/dev/null || true  
mv "decisions.md" TIER3_decisions_prompt.md 2>/dev/null || true
mv "TIER 3_decisions.md" TIER3_decisions_prompt.md 2>/dev/null || true
mv "palette_taxonomy_version__v1.1" palette_taxonomy_v1_1.yaml 2>/dev/null || true
mv "palette_taxonomy_version_v1_1" palette_taxonomy_v1_1.yaml 2>/dev/null || true
mv "Palette_Framework:_Agent_Implementation_Manual" agent_implementation_manual_v1.0b.md 2>/dev/null || true
mv "agent_implementation_manual_v1.0a.md" agent_implementation_manual_v1.0b.md 2>/dev/null || true

# Create the installation SOP if not present
# (Copy from outputs)

# Verify clean names
ls -1 *.md *.yaml
```

**Expected output**:
```
TIER1_palette_core.md
TIER2_assumptions.md
TIER3_decisions_prompt.md
agent_implementation_manual_v1.0b.md
palette_installation_sop_v1.3.md
palette_master_integration_guide.md
palette_taxonomy_v1_1.yaml
```

**If any files have spaces, colons, or double underscores, fix them now.**

---

## 1) Confirmed inputs

- ✅ Both Mical and Adam have GitHub access to `jkj9786/Myth-Fall-Game`
- ✅ Mical's local Mythfall working folder: `/home/mical/Documents/mythfall/`
- ✅ Target branch is `main` (feature branches allowed; merge after review)
- ✅ Taxonomy version: v1.1 (111 RIUs)
- ✅ All source files normalized to clean filenames (no spaces/colons)

---

## 2) Repo reality check

The repo **already contains** Kiro steering files and basic monorepo scaffold:

- `.kiro/steering/`
  - `product.md`
  - `structure.md`
  - `tech.md`
- `client/` (Godot placeholder + README)
- `server/` (Node + Socket.io + TypeScript)
- `shared/` (protocol types + docs)
- `deployment/docker/docker-compose.yml` (Postgres + Redis)

### Small inconsistencies to fix

1) **Postgres version mismatch**  
   - `docker-compose.yml` uses `postgres:16-alpine`  
   - `.kiro/steering/tech.md` claims PostgreSQL 18  
   **Fix**: Update `tech.md` to PostgreSQL 16

2) **Godot export presets ignored**  
   - `.gitignore` ignores `export_presets.cfg`  
   **Decision**: Document in README that devs configure locally

---

## 3) Goal state (what "done" looks like)

### Final directory structure

```
Myth-Fall-Game/
├── .kiro/
│   └── steering/
│       ├── product.md
│       ├── structure.md
│       ├── tech.md
│       └── palette/
│           ├── TIER1_palette_core.md
│           ├── TIER2_assumptions.md
│           ├── TIER3_decisions_prompt.md
│           ├── palette_taxonomy_v1_1.yaml
│           ├── agent_implementation_manual_v1.0b.md
│           ├── palette_installation_sop_v1.3.md
│           └── palette_master_integration_guide.md
├── fde/
│   ├── decisions.md                    # Append-only ledger (separate from policy!)
│   ├── agents/
│   │   └── (agent specifications when implemented)
│   ├── fixtures/
│   │   └── (validation scenarios when created)
│   └── kgdrs/
│       └── kges.md
├── client/
├── server/
├── shared/
└── deployment/
```

### Why this layout

- **Kiro expects** steering docs in `.kiro/steering/`
- **Palette becomes a module** under `.kiro/steering/palette/`
- **fde/ stays separate** for execution artifacts
- **Easy sync**: one directory for both Mical and Adam
- **Clear separation**: policy (steering) vs ledger (fde)

---

## 4) Step-by-step implementation

### Step 1: Create feature branch

```bash
cd ~/path/to/Myth-Fall-Game
git checkout main
git pull
git checkout -b chore/palette-steering-v1_1
```

### Step 2: Verify what exists BEFORE adding new files

```bash
ls -la .kiro/steering
find .kiro -maxdepth 3 -type f | sed 's|^./||'
```

**Confirm**: No `.kiro/steering/palette/` exists yet  
**If it exists**: STOP and compare contents before overwriting

### Step 3: Create directory structure

```bash
# Create palette steering module
mkdir -p .kiro/steering/palette

# Create FDE workspace
mkdir -p fde/agents
mkdir -p fde/fixtures
mkdir -p fde/kgdrs
```

### Step 4: Copy Palette files (CORRECTED PATHS)

```bash
# Copy Tier files (steering/policy)
cp /home/mical/Documents/mythfall/TIER1_palette_core.md .kiro/steering/palette/TIER1_palette_core.md
cp /home/mical/Documents/mythfall/TIER2_assumptions.md .kiro/steering/palette/TIER2_assumptions.md
cp /home/mical/Documents/mythfall/TIER3_decisions_prompt.md .kiro/steering/palette/TIER3_decisions_prompt.md

# Copy taxonomy (YAML extension!)
cp /home/mical/Documents/mythfall/palette_taxonomy_v1_1.yaml .kiro/steering/palette/palette_taxonomy_v1_1.yaml

# Copy implementation manual
cp /home/mical/Documents/mythfall/agent_implementation_manual_v1.0b.md .kiro/steering/palette/agent_implementation_manual_v1.0b.md

# Copy SOPs
cp /home/mical/Documents/mythfall/palette_installation_sop_v1.3.md .kiro/steering/palette/palette_installation_sop_v1.3.md
cp /home/mical/Documents/mythfall/palette_master_integration_guide.md .kiro/steering/palette/palette_master_integration_guide.md
```

### Step 5: Initialize FDE ledger (NOT the policy file!)

```bash
# Create initial decisions.md (append-only ledger)
cat > fde/decisions.md << 'EOF'
# decisions.md - Engagement Log (Append-Only)

**Purpose**: Single append-only log for engagement execution, RIU selection, agent maturity  
**Authority**: Subordinate to palette-core.md  
**Policy Reference**: See `.kiro/steering/palette/TIER3_decisions_prompt.md`  
**Version**: 1.1  
**Last Updated**: 2026-01-26

---

## A) Toolkit-Changing ONE-WAY DOOR Decisions

- (none yet)

---

## Agent Maturity Tracking

**Current agents**:
- (none yet - add as agents are implemented)

---

## Engagement Log (Append-Only - Add New Blocks Below)

---
### Engagement Update: 2026-01-26 / MYTHFALL-BOOTSTRAP

#### Semantic Blueprint
- **Goal**: Bootstrap Palette toolkit for Mythfall multiplayer game development
- **Roles**: Human leads game design/architecture; agents support when implemented
- **Capabilities**: Tier 1-3 steering files, RIU taxonomy v1.1, fixture framework
- **Constraints**: Infrastructure-agnostic, stateless, append-only logging
- **Non-goals**: Not implementing production deployment yet
- **What changed since last update**: Initial Palette installation

#### Selected RIUs
- RIU-001 — Convergence Brief: Toolkit initialization for Mythfall

#### Artifacts
- Created:
  - `.kiro/steering/palette/` (all Tier files + taxonomy)
  - `fde/decisions.md` (this file - append-only ledger)
  - `fde/agents/` (empty, ready for agent specs)
  - `fde/fixtures/` (empty, ready for validation scenarios)
  - `fde/kgdrs/kges.md` (knowledge gap tracking)

#### Next Checks
- Begin agent implementation (start with Argentavis)
- Create fixture scenarios following Tier 2 path format
- Track agent maturity progression in this file

---
EOF

# Create KGE tracking file
cat > fde/kgdrs/kges.md << 'EOF'
# Knowledge Gap Ledger (Append-Only)

**Purpose**: Track knowledge gaps detected during agent execution  
**Status**: Disposable once agents are reliable  
**Last Updated**: 2026-01-26

---

(Append KGE entries here when ⚠️ KNOWLEDGE GAP DETECTED is emitted)

---
EOF
```

### Step 6: Update existing steering files

#### 6.1 Fix Postgres version in tech.md

```bash
# Edit .kiro/steering/tech.md
# Change: PostgreSQL 18 → PostgreSQL 16 (to match docker-compose.yml)
```

#### 6.2 Add Palette reference to structure.md

```bash
# Edit .kiro/steering/structure.md
# Add section at end:

---

## Palette Framework Integration

This project uses the Palette framework for systematic FDE workflow execution.

**Location**: `.kiro/steering/palette/`

**Key files**:
- `TIER1_palette_core.md` - Immutable core principles
- `TIER2_assumptions.md` - Agent archetypes + experimental features
- `TIER3_decisions_prompt.md` - Policy for using decisions.md
- `palette_taxonomy_v1_1.yaml` - 111 Reusable Intervention Units
- `agent_implementation_manual_v1.0b.md` - How to build agents
- `palette_master_integration_guide.md` - System navigation + integration

**Execution workspace**: `fde/`
- `fde/decisions.md` - Append-only engagement log (separate from policy!)
- `fde/agents/` - Agent specifications
- `fde/fixtures/` - Validation scenarios
- `fde/kgdrs/` - Knowledge gap tracking

**Taxonomy version**: v1.1 (111 RIUs including multimodal, agentic, LLMOps, governance series)

**For usage instructions**: Start with `palette_master_integration_guide.md`
```

### Step 7: Create sync validation script

```bash
# Create scripts/kiro_sync.sh
mkdir -p scripts
cat > scripts/kiro_sync.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STEERING="$REPO_ROOT/.kiro/steering"
PALETTE="$STEERING/palette"
FDE="$REPO_ROOT/fde"

echo "✅ Repo root: $REPO_ROOT"
echo ""

# Check steering files
test -d "$STEERING" || { echo "❌ Missing .kiro/steering"; exit 1; }
test -f "$STEERING/product.md" || { echo "❌ Missing product.md"; exit 1; }
test -f "$STEERING/structure.md" || { echo "❌ Missing structure.md"; exit 1; }
test -f "$STEERING/tech.md" || { echo "❌ Missing tech.md"; exit 1; }
echo "✅ Core steering files present"

# Check Palette module
test -d "$PALETTE" || { echo "⚠️  Palette folder not present"; exit 0; }
echo "✅ Palette folder present: $PALETTE"

# Verify all required Palette files
REQUIRED_FILES=(
  "TIER1_palette_core.md"
  "TIER2_assumptions.md"
  "TIER3_decisions_prompt.md"
  "palette_taxonomy_v1_1.yaml"
  "agent_implementation_manual_v1.0b.md"
  "palette_installation_sop_v1.3.md"
  "palette_master_integration_guide.md"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$PALETTE/$file" ]]; then
    echo "✅ $file"
  else
    echo "❌ Missing: $file"
    exit 1
  fi
done

# Check FDE workspace
test -d "$FDE" || { echo "⚠️  FDE workspace not present"; exit 0; }
echo ""
echo "✅ FDE workspace present: $FDE"
test -f "$FDE/decisions.md" && echo "✅ decisions.md (ledger)" || echo "⚠️  decisions.md not created"
test -d "$FDE/agents" && echo "✅ agents/" || echo "⚠️  agents/ not created"
test -d "$FDE/fixtures" && echo "✅ fixtures/" || echo "⚠️  fixtures/ not created"
test -d "$FDE/kgdrs" && echo "✅ kgdrs/" || echo "⚠️  kgdrs/ not created"

echo ""
echo "🎉 Palette installation verified!"
EOF

chmod +x scripts/kiro_sync.sh
```

### Step 8: Run validation

```bash
./scripts/kiro_sync.sh
```

**Expected output**: All ✅ checkmarks

### Step 9: Commit to feature branch

```bash
git status
git add .kiro/steering/palette/ \
        .kiro/steering/structure.md \
        .kiro/steering/tech.md \
        fde/ \
        scripts/kiro_sync.sh

git commit -m "feat: Add Palette framework v1.1

- Add Tier 1-3 steering files (policy references)
- Add RIU taxonomy v1.1 (111 RIUs, .yaml extension)
- Add agent implementation manual v1.0b
- Add master integration guide (navigation key)
- Add installation SOP v1.3
- Initialize fde/ workspace with append-only decisions.md ledger
- Add sync validation script
- Update structure.md with Palette references
- Fix Postgres version in tech.md (18 → 16)

IMPORTANT: 
- TIER3_decisions_prompt.md is policy (in steering)
- fde/decisions.md is append-only ledger (separate!)
- Taxonomy is .yaml not .md
- All filenames normalized (no spaces/colons)"

git push -u origin chore/palette-steering-v1_1
```

### Step 10: Open PR and merge

1. Open PR on GitHub
2. Review changes
3. Merge into `main`
4. Delete feature branch

---

## 5) Ongoing sync workflow

### Daily sync (both devs)

```bash
cd ~/path/to/Myth-Fall-Game
git checkout main
git pull
```

### Working on features

```bash
git checkout -b feature/your-feature
# work work work
git add .
git commit -m "your changes"
git push -u origin feature/your-feature
# open PR, review, merge
```

### Updating decisions.md (append-only ledger)

**Rule**: One person appends at a time to avoid conflicts

**Option A**: Coordinate via chat
```bash
# Mical: "I'm appending to decisions.md now"
# Adam: "OK, I'll wait"
cd fde
# append new Engagement Update block
git add decisions.md
git commit -m "log: Add engagement update for [task]"
git push
```

**Option B**: Use PRs for appending
```bash
git checkout -b log/engagement-update-YYYY-MM-DD
# append to fde/decisions.md
git add fde/decisions.md
git commit -m "log: Engagement update for [task]"
git push -u origin log/engagement-update-YYYY-MM-DD
# quick-merge PR
```

### Updating steering files (rare)

**Tier 1**: Requires explicit approval, very rare  
**Tier 2**: Can evolve, still needs review  
**Tier 3 policy**: Update template as needed

```bash
git checkout -b docs/update-tier2
# edit .kiro/steering/palette/TIER2_assumptions.md
git add .kiro/steering/palette/TIER2_assumptions.md
git commit -m "docs: Update Tier 2 assumptions [reason]"
git push -u origin docs/update-tier2
# PR review required
```

---

## 6) Validation checklist

Before merging any Palette-related changes:

### File presence
- [ ] `.kiro/steering/product.md` exists
- [ ] `.kiro/steering/structure.md` exists and references Palette
- [ ] `.kiro/steering/tech.md` exists (Postgres 16)
- [ ] `.kiro/steering/palette/` contains 7 files
- [ ] `fde/decisions.md` exists (append-only ledger)
- [ ] `fde/agents/`, `fde/fixtures/`, `fde/kgdrs/` exist

### Naming correctness
- [ ] Taxonomy file is `palette_taxonomy_v1_1.yaml` (.yaml not .md!)
- [ ] Tier 3 steering is `TIER3_decisions_prompt.md` (policy)
- [ ] Tier 3 ledger is `fde/decisions.md` (execution log)
- [ ] No files have spaces in names
- [ ] No files have colons in names

### Content integrity
- [ ] Tier 1 authority = "Supreme"
- [ ] Tier 2 authority = "Subordinate to palette-core.md"
- [ ] Tier 3 policy explains Engagement Update format
- [ ] Taxonomy version = v1.1
- [ ] Orchestrator status = DESIGN-ONLY
- [ ] Master integration guide present (navigation key)

### Repo integrity
- [ ] `npm install` succeeds
- [ ] `npm run dev:server` starts
- [ ] `scripts/kiro_sync.sh` passes all checks

---

## 7) Drift control

### What should NOT change (without approval)

**Tier 1 (immutable)**:
- `.kiro/steering/palette/TIER1_palette_core.md`

**Taxonomy (stable)**:
- `.kiro/steering/palette/palette_taxonomy_v1_1.yaml`

### What CAN change (with review)

**Tier 2 (experimental)**:
- `.kiro/steering/palette/TIER2_assumptions.md`
- Can be reset/rewritten per reset rule

**Tier 3 policy (template)**:
- `.kiro/steering/palette/TIER3_decisions_prompt.md`
- Updates to template format allowed

### What WILL change (continuously)

**Execution ledger**:
- `fde/decisions.md` - grows with every engagement

**Artifacts**:
- `fde/agents/*` - agent specs added
- `fde/fixtures/*` - validation scenarios added
- `fde/kgdrs/kges.md` - knowledge gaps appended

### Validation commands

```bash
# Verify Tier 1 unchanged
git diff .kiro/steering/palette/TIER1_palette_core.md

# Check decisions.md is append-only (no deletions except separators)
git diff fde/decisions.md | grep "^-[^-]" | grep -v "^---"
# Should return nothing

# Verify taxonomy integrity
wc -l .kiro/steering/palette/palette_taxonomy_v1_1.yaml
# Should be ~4173 lines

# Run sync check
./scripts/kiro_sync.sh
```

---

## 8) Troubleshooting

### "File not found" errors during copy

**Problem**: Source files have spaces/colons in names  
**Fix**: Run Step 0 (normalize filenames) first

### "Merge conflict in decisions.md"

**Problem**: Both devs appended simultaneously  
**Fix**: 
```bash
# Accept both changes
git checkout --theirs fde/decisions.md  # or --ours
# Manually order the blocks chronologically
git add fde/decisions.md
git commit
```

**Prevention**: Coordinate appends or use PR workflow

### "Kiro can't find taxonomy"

**Problem**: Wrong filename or extension  
**Fix**:
```bash
# Must be .yaml not .md
ls .kiro/steering/palette/palette_taxonomy_v1_1.yaml

# If wrong, rename
cd .kiro/steering/palette
mv palette_taxonomy_v1_1.md palette_taxonomy_v1_1.yaml
git add palette_taxonomy_v1_1.yaml
git rm palette_taxonomy_v1_1.md
git commit -m "fix: Rename taxonomy to .yaml"
```

### "Which decisions.md is the ledger?"

**Answer**:
- ❌ `.kiro/steering/palette/TIER3_decisions_prompt.md` - This is the POLICY
- ✅ `fde/decisions.md` - This is the LEDGER

Always append to `fde/decisions.md`, never to the Tier 3 prompt file.

---

## 9) Post-installation next steps

1. **Read the integration guide**:
   ```bash
   cat .kiro/steering/palette/palette_master_integration_guide.md
   ```

2. **Begin agent implementation**:
   - Follow agent_implementation_manual_v1.0b.md
   - Start with Argentavis (Week 1-2)

3. **Create fixtures**:
   - Follow Tier 2 path format: `fde/fixtures/riu-RIU-<ID>/ARK:<Type>/<scenario>/`

4. **Track progress**:
   - Append Engagement Updates to `fde/decisions.md`
   - Record agent maturity changes

5. **Coordinate with team**:
   - Establish append workflow
   - Use feature branches
   - Review PRs before merge

---

## 10) Quick reference

### File locations summary

| Purpose | Filename | Location |
|---------|----------|----------|
| Tier 1 Core | `TIER1_palette_core.md` | `.kiro/steering/palette/` |
| Tier 2 Assumptions | `TIER2_assumptions.md` | `.kiro/steering/palette/` |
| Tier 3 Policy | `TIER3_decisions_prompt.md` | `.kiro/steering/palette/` |
| Tier 3 Ledger | `decisions.md` | `fde/` ⚠️ DIFFERENT! |
| Taxonomy | `palette_taxonomy_v1_1.yaml` | `.kiro/steering/palette/` |
| Implementation Manual | `agent_implementation_manual_v1.0b.md` | `.kiro/steering/palette/` |
| Installation SOP | `palette_installation_sop_v1.3.md` | `.kiro/steering/palette/` |
| Integration Guide | `palette_master_integration_guide.md` | `.kiro/steering/palette/` |

### Command quick ref

```bash
# Sync from GitHub
git pull

# Validate installation
./scripts/kiro_sync.sh

# Append to ledger
vim fde/decisions.md  # Add Engagement Update block

# Create fixture
mkdir -p fde/fixtures/riu-RIU-001/ARK:Argentavis/scenario/
vim fde/fixtures/riu-RIU-001/ARK:Argentavis/scenario/input.md

# Check agent maturity
grep -A 10 "## Agent Maturity" fde/decisions.md
```

---

**Installation complete!** 🎉

Begin agent development following the implementation manual.  
Use the master integration guide as your navigation key.
