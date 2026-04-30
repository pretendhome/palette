# Talent Skill — Palette Job Search & Interview System

> From discovery to offer in one repeatable process. **Profile-driven.** Learnings compound.

## Architecture

```
skills/talent/
├── README.md                        ← You are here
├── role-profiles.yaml               ← 6 role profiles: search patterns, fit lenses, playbooks, learnings
├── experience-inventory.yaml        ← Structured career data (5 ERAs, 7 stories, stats, positioning)
├── methodology.md                   ← 7-phase process (discover → fit → resume → apply → prep → day-of → post-mortem)
├── build_resume.py                  ← Parameterized resume builder (reads inventory, outputs .docx)
├── interview-prep-methodology.md    ← [SUPERSEDED by methodology.md — kept for reference]
└── openai-takehome-execution.md     ← Takehome-specific protocol (still valid)
```

Related local Talent workspace sources:

- `implementations/talent/talent-job-search/nsa/index.yaml` ← NSA query map and Mical-specific positioning
- `implementations/talent/talent-job-search/nsa/README.md` ← where to start for NSA questions
- `implementations/talent/talent-nsa-moderator/` ← full downloaded NSA program corpus and moderator artifacts

## How It Works

**Everything flows through `profile_id`.**

A role profile is the lens through which your entire career gets framed. Discovery, fit scoring, resume generation, interview prep, and post-mortem all inherit from the same profile. Learnings compound: every interview for a profile type makes the next one better.

### Three files work together:

| File | Purpose |
|------|---------|
| `role-profiles.yaml` | 6 profiles with search patterns, fit lenses, interview playbooks, accumulated learnings |
| `experience-inventory.yaml` | Structured career data — 5 ERAs, 7 stories, stat verification, bullet variants |
| `build_resume.py` | Resume builder — each profile selects headline, summary, bullets, Palette framing |

### NSA operating layer

For Never Search Alone requests, the skill should query the local NSA corpus before using general knowledge:

- methodology/process questions → `implementations/talent/talent-job-search/nsa/index.yaml`
- Mical positioning/CMF questions → `implementations/talent/talent-nsa-moderator/CMF_SYNTHESIS_2026-04-03.md`
- self-discovery/wants questions → `implementations/talent/talent-nsa-moderator/MNOOKIN_TWO_PAGER_MICAL.md`
- moderator/JSC questions → `implementations/talent/talent-nsa-moderator/program/MODERATOR_PROGRAM.md`

### Six Role Profiles:

| Profile | One-liner | Example Companies |
|---------|-----------|-------------------|
| `forward_deployed_engineer` | Build and deploy AI systems at customer sites | Perplexity, Google Cloud, Dust |
| `enablement_strategy` | Drive AI adoption at scale — strategy + measurement | Gap, TaskRabbit, Databricks |
| `enablement_systems_builder` | Build enablement infrastructure — curriculum, assessment, credentialing | Mistral, Anthropic, LangChain, Cognition |
| `customer_success_ai` | Own customer outcomes with AI — deployment + expansion | OpenAI, Glean, Perplexity CSM |
| `knowledge_data_engineer` | Build knowledge architectures, ontologies, retrieval systems | iBusiness, Gusto, Airbnb |
| `certification_architect` | Design certification programs and assessment systems | Anthropic |

## Quick Start: New Role Comes In

0. **Classify** — match JD to a profile in `role-profiles.yaml`. Assign `profile_id`.
1. **Score fit** — use the profile's `fit_lens`. Map requirements to ERAs. Score 0-100.
2. **Build resume** — `python3 build_resume.py --profile <profile_id> --output ~/Downloads/resume.docx`
3. **Write answers** — use profile's `lead_eras` routing. Each answer features a DIFFERENT era.
4. **Create application dir** — `implementations/talent/talent-<company>-<role>/`
5. **Interview prep** — use profile's `interview_playbook` + `accumulated_learnings`. Build 5-6 modular docs.
6. **Day-of** — fill glance sheet using profile's `anchor_messages`.
7. **Post-mortem** — capture learnings → update `role-profiles.yaml > accumulated_learnings`.

## Resume Builder

```bash
# Forward Deployed Engineer
python3 build_resume.py --profile forward_deployed_engineer --output ~/Downloads/resume.docx

# Enablement Strategy
python3 build_resume.py --profile enablement_strategy --output ~/Downloads/resume.docx

# Enablement Systems Builder (uses TME profile)
python3 build_resume.py --profile technical_marketing_engineer --output ~/Downloads/resume.docx

# Customer Success & AI Deployment
python3 build_resume.py --profile customer_success_ai --output ~/Downloads/resume.docx

# Knowledge/Data Engineer
python3 build_resume.py --profile knowledge_data_engineer --output ~/Downloads/resume.docx

# Certification Architect
python3 build_resume.py --profile certification_architect --output ~/Downloads/resume.docx
```

## Key Principles

1. **Profile-first.** Classify the opportunity before doing anything else. The profile drives everything.
2. **Learnings compound.** Every post-mortem feeds back into the profile. Next interview starts smarter.
3. **Query, don't write from scratch.** The inventory has the data. Assemble, don't create.
4. **Each answer features a different ERA.** Never repeat the same system across multiple questions.
5. **Fit-first.** Score before investing time. <65% = pass. Don't chase bad-fit roles.
6. **Modular materials.** 5-6 focused documents beat 1-2 monolithic ones (validated on Glean).
7. **Same proof points, different framing.** Ask Pathfinder + Palette serve every role type — only the emphasis changes.
8. **Stat-verified.** Every number is GREEN (cite freely) or YELLOW (hedge). Never cite RED.
9. **Honest about tradeoffs.** Every approach has problems. Name them and how you solved them.

## Weekly Sweep

Run a market sweep weekly using each profile's `search_patterns`:
1. Search LinkedIn, company boards, referrals using profile-specific `titles` and `keywords`
2. Classify each opportunity → assign `profile_id`
3. Score fit using the profile's `fit_lens`
4. Add to pipeline tracker: `| Company | Role | profile_id | Fit | Tier | Status | Deadline |`
5. EU opportunities tracked via `eu_search` section (language advantage: French, Italian, Spanish)

## Adding a New Role Profile

1. Add a new profile in `role-profiles.yaml` (search patterns, fit lens, story bank, playbook)
2. Add positioning entry in `experience-inventory.yaml > positioning`
3. Add bullet variants for each ERA in `eras > [era] > bullets > <new_key>` (if existing keys don't fit)
4. Add a new PROFILES dict entry in `build_resume.py`
5. Test: `python3 build_resume.py --profile <new_id> --output /tmp/test.docx`

## Updating After Interviews

After every interview cycle:
1. **Profile learnings** → add patterns/anti-patterns to `role-profiles.yaml > accumulated_learnings`
2. **Stats** → new metrics verified? Add to GREEN in `experience-inventory.yaml`
3. **Stories** → new story validated? Add to stories section
4. **Questions** → new question type? Add to profile's `common_questions`
5. **Anchor messages** → better framing discovered? Update the profile

## Implementations

Active applications live in `implementations/talent/talent-<company>-<role>/`. Each gets its own directory with role-specific prep materials. The skill provides the methodology and profiles; implementations are the execution.

## Lineage

Built from learnings across: OpenAI ADM, Perplexity CSM/FDE, Glean AI Outcomes Manager, Gap Inc Sr Manager, Mistral TME, Anthropic Cert Architect, iBusiness AI KDE, FriendliAI FDE, Baseten, Lenovo, ModelOp, TaskRabbit.
