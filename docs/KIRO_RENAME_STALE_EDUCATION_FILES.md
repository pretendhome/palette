# Kiro Task: Rename Stale Dinosaur-Named Files in Education Sources

## Context
The Palette agent rename (dinosaur → role-based names) is complete across all palette/ files.
Some files in `implementations/education/` still use old dinosaur filenames. These are historical
artifacts from La Scuola work that reference the old agent names.

## Files to Rename

All paths relative to `/home/mical/fde/`:

```bash
# La Scuola artifacts
git mv implementations/education/adaptive-learning-architecture/sources/education-la-scuola/artifacts/rex_architecture_framework.md \
      implementations/education/adaptive-learning-architecture/sources/education-la-scuola/artifacts/architect_architecture_framework.md

git mv implementations/education/adaptive-learning-architecture/sources/education-la-scuola/artifacts/rex_architecture_framework_v1.1_FINAL.md \
      implementations/education/adaptive-learning-architecture/sources/education-la-scuola/artifacts/architect_architecture_framework_v1.1_FINAL.md

git mv implementations/education/adaptive-learning-architecture/sources/education-la-scuola/artifacts/anky_validation_assessment.md \
      implementations/education/adaptive-learning-architecture/sources/education-la-scuola/artifacts/validator_validation_assessment.md

git mv implementations/education/adaptive-learning-architecture/sources/education-la-scuola/research/argy_research_findings.md \
      implementations/education/adaptive-learning-architecture/sources/education-la-scuola/research/researcher_research_findings.md

# Claudia sources (old agent workflow files)
git mv implementations/education/adaptive-learning-architecture/sources/claudia-canu/phase1_yuty_strategy.md \
      implementations/education/adaptive-learning-architecture/sources/claudia-canu/phase1_narrator_strategy.md

git mv implementations/education/adaptive-learning-architecture/sources/claudia-canu/phase2_argy_research.md \
      implementations/education/adaptive-learning-architecture/sources/claudia-canu/phase2_researcher_research.md

git mv implementations/education/adaptive-learning-architecture/sources/claudia-canu/phase3_rex_strategy.md \
      implementations/education/adaptive-learning-architecture/sources/claudia-canu/phase3_architect_strategy.md
```

## After Renaming

Update any internal references to the old filenames in these directories. Grep for the old filenames and fix any cross-references.

## Do Not Touch

- `decisions.md` — append-only historical log, old names are accurate for when they were recorded
- `archive/` — superseded content
- `scripts/palette_intelligence_system/state/tasks/` — historical execution data
- `knowledge-library/v1.4/palette_knowledge_library_v1.4_backup.yaml` — backup file
