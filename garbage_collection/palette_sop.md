# Mythfall — Palette + Kiro Steering SOP (Implementation & Sync)  
**Version:** v1.2 (taxonomy v1.1)  
**Repo:** `jkj9786/Myth-Fall-Game` (branch: `main`)  
**Local (Mical):** `/home/mical/Documents/mythfall/`  
**Local (Adam):** Windows path (repo clone)  

This SOP makes the **GitHub repo** the **single source of truth**, and provides a repeatable, low-friction way to keep **three codebases in sync**:

1) GitHub repository (`main`)  
2) Mical’s local clone (Linux)  
3) Adam’s local clone (Windows)

It also adds **Mythfall-only Palette infrastructure** to Kiro without breaking the existing project steering.

---

## 0) Confirmed inputs (already answered)

- ✅ Both Mical and Adam have GitHub access to the repo.
- ✅ Mical’s local Mythfall working folder contains the Palette base files shown in the screenshot.
- ✅ Target branch is `main` (feature branches allowed; merge after resolving conflicts).
- ✅ Taxonomy file renamed to: `palette_taxonomy_version_v1_1` (v1.1).

---

## 1) Repo reality check (from your scrape)

The repo **already contains** Kiro steering files and a basic monorepo scaffold:

- `.kiro/steering/`
  - `product.md`
  - `structure.md`
  - `tech.md`
- `client/` (Godot placeholder + README)
- `server/` (Node + Socket.io + TypeScript starter)
- `shared/` (protocol types + docs)
- `deployment/docker/docker-compose.yml` (Postgres + Redis)
- `README.md`, `SETUP.md`, root `package.json`

### 1.1 Small inconsistencies to fix (recommended before Palette integration)

1) **Postgres version mismatch**  
   - `deployment/docker/docker-compose.yml` uses `postgres:16-alpine`  
   - `.kiro/steering/tech.md` claims PostgreSQL 18  
   **Decision:** update `tech.md` to PostgreSQL 16 to match the compose file.

2) **Godot export presets are ignored**  
   - `.gitignore` ignores `export_presets.cfg`, but Godot export config is often shared across the team.  
   **Decision:** either (A) keep ignored and document local setup, or (B) commit it so HTML5 export is consistent.

---

## 2) Goal state (what “done” looks like)

### 2.1 Single-source-of-truth layout

We keep existing steering files **as-is**, and add **Palette-for-Mythfall** under the steering folder:

```
Myth-Fall-Game/
└── .kiro/
    └── steering/
        ├── product.md
        ├── structure.md
        ├── tech.md
        └── palette/
            ├── Palette_SOP.md
            ├── TIER1_palette_core.md
            ├── TIER2_assumptions.md
            ├── TIER3_decisions.md
            ├── palette_taxonomy_version_v1_1.md
            └── Palette_Framework_Agent_Implementation_Manual.md
```

### 2.2 Why this layout

- **Kiro already expects** steering docs in `.kiro/steering/`
- Palette becomes a **scoped “module”** under `.kiro/steering/palette/`
- Easy to sync: one directory is the “install target” for both Mical and Adam.

---

## 3) Step-by-step implementation plan (the actual work)

> You will do this once on a feature branch, then merge into `main`.

### 3.1 Create a feature branch (both devs)

```bash
git checkout main
git pull
git checkout -b chore/palette-steering-v1_1
```

### 3.2 Verify what exists BEFORE creating anything new

Run from repo root:

```bash
ls -la .kiro/steering
find .kiro -maxdepth 3 -type f | sed 's|^./||'
```

Confirm there is **no existing** `.kiro/steering/palette/` folder.  
If it exists already, STOP and compare contents before overwriting.

### 3.3 Add Mythfall-only Palette infra to the repo

Create the folder:

```bash
mkdir -p .kiro/steering/palette
```

Copy in the updated files from Mical’s local folder (`/home/mical/Documents/mythfall/`):

```bash
# From repo root
cp /home/mical/Documents/mythfall/Palette_SOP.md .kiro/steering/palette/Palette_SOP.md
cp /home/mical/Documents/mythfall/TIER1_palette_core.md .kiro/steering/palette/TIER1_palette_core.md
cp /home/mical/Documents/mythfall/TIER2_assumptions.md .kiro/steering/palette/TIER2_assumptions.md
cp /home/mical/Documents/mythfall/TIER\ 3_decisions.md .kiro/steering/palette/TIER3_decisions.md
cp /home/mical/Documents/mythfall/palette_taxonomy_version_v1_1 .kiro/steering/palette/palette_taxonomy_version_v1_1.md
cp /home/mical/Documents/mythfall/Palette_Framework:_Agent_Implementation_Manual .kiro/steering/palette/Palette_Framework_Agent_Implementation_Manual.md
```

**Important:** standardize filenames (no spaces/colons) inside the repo.

### 3.4 Patch steering cross-links (so Kiro can “discover” Palette)

Update `.kiro/steering/structure.md` to include a short Palette section near the end:

- Where to find Palette docs
- What each tier doc means
- The “taxonomy version” used

Also update `.kiro/steering/product.md` and/or `.kiro/steering/tech.md` **only if** you want Palette to enforce decision logging, assumptions, and protocols for Mythfall.

**Minimal-change recommendation:**  
Add Palette references to **structure.md only**, to avoid changing the product/tech story while the project is early.

### 3.5 Fix the Postgres version mismatch (quick win)

Edit `.kiro/steering/tech.md`:

- Change “PostgreSQL 18” → “PostgreSQL 16” (to match docker-compose)

### 3.6 Add a team sync script (GitHub → Local Kiro steering install)

Create: `scripts/kiro_sync.sh`

**Purpose:** a single command that copies `.kiro/steering/` into each dev’s preferred local “Kiro steering folder” (if they keep one outside the repo), or simply validates steering is present.

If you use **the repo folder itself** as the canonical Kiro steering location, the script can be mainly a validator.

Example (Linux-friendly):

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/.kiro/steering"

echo "✅ Repo root: $REPO_ROOT"
echo "✅ Steering source: $SRC"

test -d "$SRC" || { echo "❌ Missing $SRC"; exit 1; }
test -f "$SRC/product.md" || { echo "❌ Missing product.md"; exit 1; }
test -f "$SRC/structure.md" || { echo "❌ Missing structure.md"; exit 1; }
test -f "$SRC/tech.md" || { echo "❌ Missing tech.md"; exit 1; }

echo "✅ Steering files present."
echo "ℹ️  Palette steering: $SRC/palette"
test -d "$SRC/palette" && echo "✅ Palette folder present." || echo "⚠️ Palette folder not present."
```

Then:

```bash
chmod +x scripts/kiro_sync.sh
./scripts/kiro_sync.sh
```

> For Adam on Windows: either run via Git Bash, WSL, or create an equivalent `scripts/kiro_sync.ps1`.

### 3.7 Commit and open PR into `main`

```bash
git status
git add .kiro/steering/palette .kiro/steering/structure.md .kiro/steering/tech.md scripts/kiro_sync.sh
git commit -m "Add Palette steering module (taxonomy v1.1) + sync script"
git push -u origin chore/palette-steering-v1_1
```

Open PR → review → merge into `main`.

---

## 4) Ongoing sync workflow (Mical ↔ Adam ↔ GitHub)

### 4.1 Golden rules

- **Never edit steering files directly on GitHub UI** unless it’s an emergency hotfix.
- Always:
  1) `git pull`
  2) branch
  3) change
  4) PR
  5) merge to `main`

### 4.2 Daily sync (both devs)

```bash
git checkout main
git pull
```

If working on a branch:

```bash
git checkout <your-branch>
git rebase main
# resolve conflicts
git push --force-with-lease
```

### 4.3 If Adam and Mical have local “base files” outside the repo

- Treat those as **build artifacts** or **drafts**.
- The repo is the source of truth.
- If you want to keep the external folder, only update it by **pulling from the repo** via script.

---

## 5) Validation checklist (before merging)

### 5.1 Steering sanity

- [ ] `.kiro/steering/product.md` exists
- [ ] `.kiro/steering/structure.md` exists and references Palette
- [ ] `.kiro/steering/tech.md` exists and matches actual infra (Postgres version consistent)
- [ ] `.kiro/steering/palette/` contains all tier docs + SOP + taxonomy v1.1

### 5.2 Repo integrity

- [ ] `npm install` succeeds at repo root
- [ ] `npm run dev:server` starts
- [ ] `curl http://localhost:3000/health` returns ok (or browser hits it)

### 5.3 Drift control

- [ ] No duplicate/competing Palette SOPs in other folders
- [ ] Taxonomy filename is consistent everywhere: `palette_taxonomy_version_v1_1.md`

---

## 6) What I need from you next (so I can finalize the SOP fully)

Paste these outputs from **Mical’s repo clone** (not screenshots):

1) Repo tree (first ~3 levels):
```bash
find . -maxdepth 3 -type f | sed 's|^./||'
```

2) Current `.kiro/steering/structure.md` (after you add Palette references)

3) Your intended “Kiro steering install location”, if any, **outside** the repo  
   - If “none”, we’ll keep it repo-native and skip copy steps.

---

## Appendix — recommended naming normalization

**In repo (preferred):**
- `TIER3_decisions.md` (no spaces)
- `Palette_Framework_Agent_Implementation_Manual.md` (no colons)
- `palette_taxonomy_version_v1_1.md`

