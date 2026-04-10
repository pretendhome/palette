---
description: /fit — Score resume-to-job fit using research-grounded HR science
id: SKILL-TALENT-004
name: Job Fit Scorer
domain: talent
for_agents: [resolver, validator]
triggers: [RIU-601, RIU-602]
impressions: 3
status: WORKING
validated_on: "2026-04-03: scored LangChain (79%), Apple (83%), Anthropic (79%) — all aligned with tailored resume quality"
---

# /fit — Job Fit Scorer

Score how well a resume matches a job description using validated selection science (Sackett et al. 2022, O*NET, Kristof-Brown 2005).

## Invocation

```bash
python3 ~/fde/implementations/talent/_shared/job_fit_scorer.py \
  --resume <resume.md> --jd <jd.md> [--json]
```

## Methodology

### Input Preparation
1. Resume must be markdown (single source of truth for content)
2. JD must be markdown or plain text with recognizable sections (Required/Preferred/Responsibilities)
3. If user pastes JD text, save to temp file first

### Scoring Dimensions (research-grounded weights)
| Dimension | Weight | Source |
|---|---|---|
| Required skills | 30% | Sackett: job knowledge r=.40 |
| Experience relevance | 20% | O*NET proximity |
| Preferred skills | 10% | Complementary D-A fit |
| Role/title alignment | 10% | ATS seniority |
| Industry/domain | 10% | Person-Vocation fit |
| Evidence of impact | 10% | Biodata r=.38 |
| Education/certs | 5% | Schmidt r=.10 |
| Years of experience | 5% | Sackett r=.07 |

### Verdict Scale
- STRONG MATCH (88+) | GOOD MATCH (78+) | COMPETITIVE (68+) | STRETCH (55+) | WEAK (40+) | POOR FIT (<40)

### Post-Score Actions
- **Score >= 78**: Confirm competitive, flag easy wins from missing signals
- **Score 55-77**: Identify top 3 resume edits, re-score after changes
- **Score < 55**: Recommend skip unless role has strategic value worth the stretch

## Constraints
- No API calls (pure Python, standard library only)
- Resume is READ-ONLY input — scorer never modifies content
- Only measures visible competency layers (skills, knowledge, experience) — NOT motives, traits, or cognitive ability (Spencer iceberg model)
- Evidence-based weights only — every dimension weight has a published citation

## Integration
- `/job-search`: Use /fit to score found roles before investing application time
- `/new-resume`: Run /fit after generating to validate JD alignment
- Batch: Score multiple JDs against one resume to prioritize applications
