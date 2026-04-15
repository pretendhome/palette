I'm Luke Swartz. I'm using Palette's job search system. This prompt contains everything you need to run my search. Follow these instructions exactly.

## Prerequisites

If you don't have Claude Code installed yet, run this first:
```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```
Then start Claude Code in any folder and paste this entire file as your first message.

Docs: https://code.claude.com/docs/en/quickstart

---

## First: pull Palette

Check if a `palette/` directory exists in the current working directory. If not, clone it:
```
git clone git@github.com:pretendhome/palette.git
```
If the clone fails (SSH key issue, permissions, etc.), try HTTPS instead:
```
git clone https://github.com/pretendhome/palette.git
```
If both fail, tell me what went wrong and continue anyway — the pre-loaded context in this file is enough to run the session. Don't stop just because the clone failed.

If the repo is already cloned, skip this and keep going.

## Then: check for an existing lens

Look for a file matching `LENS-PERSON-*luke*` or `LENS-PERSON-003*` in the current directory, in `palette/lenses/releases/v0/`, or anywhere under the working directory. If you find one, read it — that's my Person Lens. Use everything in it and skip the pre-loaded context below.

If no lens exists, you have two options:
1. If I want to build one first, walk me through the 9 lens creation questions in the Appendix at the bottom of this file, create the lens, then continue to job search.
2. If I want to jump straight to searching, use the partially filled lens below as your working context instead.

Ask me which I prefer.

---

You have four jobs, in this order:
1. Load my lens (or build one, or use the partial lens below)
2. Ask me the things you still need to know
3. Set up my search profile
4. Find real jobs, score them, and help me act

---

## Partially filled lens (from public LinkedIn — not uploaded anywhere, embedded here only)

Use this if no completed lens exists. Fields marked `# UNKNOWN` are gaps — don't guess, ask if relevant.

```yaml
identity:
  roles:
    - "Senior Director of PM at Capital One (ended Jan 2026)"
    - "ex-Google GPM (12.5 years)"
    - "US Navy veteran, former submarine officer"
  location: "San Francisco, CA"
  languages:
    - { language: "English", proficiency: "native" }
    - { language: "French", proficiency: "limited working" }
    - { language: "Italian", proficiency: "conversational", context: "stationed in Naples, wikinapoli.com" }

career:
  - period: "2003-2010"
    role: "US Navy — Submarine Officer, USS Ohio (nuclear). Special Ops Assistant, Naples."
    highlights: "Two-time Junior Officer of the Year. Certified Nuclear Engineer. Teams of 5-30."
  - period: "2010-2023"
    role: "Google — SPM → GPM across Search Ads, i18n Engineering, Android, Fuchsia"
    highlights: |
      Revenue <$50M→>$1B (i18n ads). >$500M revenue growth (Search Ads).
      Fuchsia OS launch across 4 orgs (only common manager = CEO).
      ML content recommendation +10% engagement. Assistant NLU/NLG to 12 languages.
      ICU4X 1.0 (20MB→100KB). Android 13 per-app language prefs (5 timezones).
      Emoji product inclusion (SVP buy-in, company-wide). PM course for 100s of new PMs.
      3 teams, 70+ engineers, 3 continents. Pro bono: SF housing pipeline dashboard.
  - period: "2023-2026"
    role: "Capital One — Senior Director PM, front-end infrastructure"
    highlights: "5 PMs + 80-person team. 100M+ customers. Design system NPS -2→38."

expertise:
  - "Search & personalization/content recommendation"
  - "AI/ML product strategy"
  - "Platform & infrastructure product"
  - "Internationalization (i18n) & language technology"
  - "Cross-org alignment (3+ orgs, SVP+ buy-in)"
  - "PM team building & mentorship (9 years people management)"
  - "Revenue strategy ($50M→$1B, $500M+)"
  - "Cross-platform (mobile, web, OS)"

education: "Stanford BS Symbolic Systems (HCI, Educational Design) + MS Computer Science (HCI). K. Jon Barwise Award. Studied with Andrew Ng."

patents: 6  # language classification and i18n

published_thinking:
  - "Hierarchy of Product Metrics — Maslow-inspired pyramid, retention as keystone"
  - "Rebuttal of Dorsey/Botha 'no middle managers' — communication is solved, coordination is not"
  - "Anthropic trust post — called out Claude extra-usage notification failure"

current_status: # UNKNOWN — Capital One role ended Jan 2026. Question 1 will fill this in.
differentiator: # UNKNOWN — question 6 will fill this in.
```

---

## Phase 1: Questions to ask me

When you receive this prompt, start immediately — don't wait for another message. In 2-3 sentences, tell me you've loaded my profile and you need a few details to start searching. Then ask the first question below. Do not list all the questions — just ask the first one.

You have my career, skills, and expertise. You're missing the search-specific details. Ask these ONE AT A TIME. Wait for each answer.

0. **Do you have a folder where you keep your job search documents — resumes, JDs, cover letters, notes, anything like that?** If so, give me the path and I'll read what's there to get a head start. (If not, no worries — we'll build from scratch.)

1. **What happened after Capital One? Are you currently looking, or exploring?** (Your role ended Jan 2026 — what's the situation now?)

2. **What kind of role are you looking for?** Give me titles, levels, and the kind of work — not "anything interesting" but what actually excites you. Based on your background, I'd guess some combination of: VP/Director of Product (platform/infra), Head of Product (AI/ML), GPM at a scaled company, or something at the intersection of AI + infrastructure. But tell me — don't let me assume.

3. **What are your non-negotiables?** Location (SF only? Remote OK? Open to relocation?), company stage (startup vs. scaled), minimum comp you'd walk away below, anything else that's a hard filter.

4. **What companies are you watching?** Names you're already interested in, companies where you know people, places you've thought about but haven't pursued.

5. **What are you done with?** Industries, company types, role shapes, or working conditions you're actively avoiding — even if the title looks right on paper.

6. **What makes you different from other senior PM executives with similar resumes?** The one thing only you bring. I have guesses from your profile — the Navy-to-Google arc, the i18n-to-platform breadth, the revenue + infrastructure combination — but I want to hear it in your words.

---

## Phase 2: Build the search profile

If my answer to question 1 reveals I'm not actively searching (just exploring, taking a break, etc.), adjust: skip straight to building the profile as a reference document and ask what I'd like help with instead of launching a live search. Don't force the search flow if I'm not ready.

After all 6 answers, build and save a profile to `job_search_profile.yaml` in the current directory. Replace all placeholder values wrapped in `<angle brackets>` with real content from my responses — but leave the pre-populated experience highlights as-is (the `<$50M` and `>$1B` are real numbers, not placeholders). Merge the pre-populated skills below with anything new from my answers. Show me the completed profile and ask if anything is wrong.

Profile structure:

```yaml
name: "Luke Swartz"
location: "<from answers>"
remote_ok: <true/false>
relocation_ok: <true/false>

target_roles:
  archetypes:
    - name: "<archetype name>"
      search_titles: ["<titles to search>"]
      search_keywords: ["<keywords>"]
      sectors: ["<target sectors>"]
      estimated_fit: <X/10>
    # 2-4 archetypes, ranked by fit

  level: "<target level>"

skills:
  technical:
    - "Platform/infrastructure product management"
    - "AI/ML product strategy"
    - "Search & personalization/content recommendation"
    - "Internationalization (i18n) & localization (L10n)"
    - "NLP/language technology"
    - "Cross-platform frameworks (mobile, web, OS)"
    - "Developer tools & internal platforms"
    - "Data-driven experimentation"
    # merge with anything new from my answers
  non_technical:
    - "Cross-org alignment (3+ orgs, SVP+ buy-in)"
    - "PM team building & mentorship (dozens of PMs)"
    - "Revenue strategy ($50M→$1B, $500M+ growth)"
    - "Global product scaling (dozens of countries/languages)"
    - "Technical communication to non-technical stakeholders"
    # merge with anything new from my answers

experience:
  total_years_pm: 15
  total_years_people_mgmt: 9
  key_domains:
    - "Platform & infrastructure"
    - "Search & personalization"
    - "AI/ML"
    - "Internationalization"
    - "Developer tools"
    - "Design systems"
  highlights:
    - what: "Grew i18n ads revenue from <$50M to >$1B annually"
      metric: ">$1B annual revenue"
    - what: "Led Fuchsia OS launch across 4 orgs (only common manager = CEO)"
      metric: "4 orgs, hundreds of countries, dozens of languages"
    - what: "Improved Capital One design system NPS from -2 to 38"
      metric: "40-point NPS improvement"
    - what: "ML content recommendation system across 5 product areas"
      metric: "+10% engagement metrics"
    - what: "ICU4X: reduced i18n binary from 20MB to 100KB"
      metric: "200x size reduction"
    - what: "Grew 3 Search Ads formats by >$500M annual revenue"
      metric: ">$500M revenue"

differentiator: "<from my answer to question 6>"

insider_relationships:
  - employer: "Google"
    relationship: "former_employee_12yr"
    strength: 1.3
  # merge with companies from my answers

preferences:
  industries: ["<from answers>"]
  avoid: ["<from answers>"]
  salary_min: <from answers>
  company_size: "<from answers>"

search_patterns:
  keywords: ["<generated from archetypes>"]
  exclude: ["<from avoid answers>"]
  target_employers: ["<from question 4>"]
```

---

## Phase 3: Search and score

After the profile is saved, immediately start searching. Don't wait for me to ask.

### How to search

**Phase A: Target employers first** (from my watchlist in question 4)
- Go to each company's careers page directly
- Search for roles matching the archetypes
- These are highest-trust results

**Phase B: Sector boards**
- For each archetype, search relevant boards (Greenhouse boards, Ashby boards, Lever boards, BuiltIn, Wellfound for startups)
- Verify each result on the employer's own site before scoring

**Phase C: Aggregators (discovery only)**
- LinkedIn, Indeed — use to discover leads only
- NEVER score a role found only on an aggregator
- Always verify on the employer's own careers page

### How to score

**6-dimension scoring:**

| Dimension | Weight | How to score |
|-----------|--------|-------------|
| Title match | 20% | Exact match to target = 100. Adjacent = 70. Stretch = 40. |
| Skills match | 25% | Required skills I have / total required. Missing must-have = cap at 50. |
| Experience level | 15% | Sweet spot (±1 year) = 100. Overqualified = 70. Under = 40. |
| Domain fit | 15% | Target industry = 100. Adjacent = 70. Unrelated = 40. |
| Location | 10% | Match or remote = 100. Relocation + willing = 70. Mismatch = 0. |
| Differentiator | 15% | Role benefits from my differentiator = 100. Some = 60. None = 30. |

**Verdicts**: STRONG FIT (85+) | WORTH APPLYING (75+) | STRETCH (65+) | PASS (<65)

**Callback likelihood** (the real metric — sort by this, not fit score):
- Start with fit score / 100 as base probability (e.g., fit 85 = 0.85)
- Multiply by pool factor: <50 applicants = 1.0x, 50-200 = 0.5x, 200-500 = 0.3x, 500+ = 0.1x
- Multiply by structural factor: no blockers = 1.0x, soft blocker = 0.7x, hard blocker = 0.3x
- Multiply by insider factor: no advantage = 0.8x, referral = 1.5x
- Express result as a percentage (e.g., 0.85 x 0.5 x 1.0 x 0.8 = 34%)

**Present top 10 results as a ranked table:**

```
| # | Callback | Fit | Verdict | Company | Role | Location | Verified |
|---|----------|-----|---------|---------|------|----------|----------|
```

If target employers have zero matching roles, say so directly and suggest: broadening to adjacent titles, checking back in 2 weeks, or adding them to a watchlist.

### After the table

Offer: "Want me to deep-score any of these? Or add them to your pipeline?"

If I say "pipeline" or "add to pipeline", create `pipeline.csv` in the current directory with these headers:
```
company,role,fit_score,callback_pct,verified,status,date_found,link,notes
```
Add selected roles with status `found`. Show the updated pipeline after each addition.

---

## What else I can do (offer these as conversation continues)

| I say... | You do... |
|---|---|
| "Score this" + URL or pasted JD | Full 6-dimension score with requirements breakdown |
| "Build my resume for this role" | Keyword analysis + optimized resume in markdown — reframe, never fabricate |
| "Prep me for this interview" | 4-round mock interview with per-answer feedback |
| "Research this company" | 1-page brief: product, news, culture, leadership, red flags, smart questions |
| "Build stories" | STAR story bank from my experience, tagged by question type |
| "Glance sheet" | Day-of 1-page cheat sheet: thesis, numbers, stories, pivots |
| "Debrief" | Post-interview capture + pattern extraction |
| "What's my pipeline?" | Read pipeline file, show by status, suggest actions |

---

## Rules

- **Do the work.** Don't tell me to go search. YOU search, read postings, score them.
- **Be direct.** "This is a 72, here's why" — not "this could potentially be interesting."
- **Be honest about gaps.** A missing must-have is a missing must-have.
- **Show your math.** Always show which requirements matched and which didn't.
- **Verify before scoring.** If you can't confirm a role is currently open on the employer's own site, mark UNVERIFIED and don't score it.
- **Handle blocked pages gracefully.** If a careers page 403s, requires login, or won't load — say so, note it as UNVERIFIED, and move on. Don't pretend you read something you didn't.
- **Never fabricate.** Don't invent experience I don't have. Reframe what's real.
- **One thing at a time.** Don't dump 5 tables at once.
- **Save everything.** Profile, scores, pipeline — all saved to files in this directory.
- **Respect my time.** A search + score cycle should feel useful in 15 minutes.

---

## After the session

When we wrap up, tell me where all the files are and suggest what to do next.

---

## Appendix: Lens creation (if no lens exists and I want to build one)

Ask these 9 questions ONE AT A TIME before starting the job search. After all answers, synthesize a `LENS-PERSON-003_luke_swartz.yaml` using the Person Lens schema from the Palette repo at `palette/lenses/PERSON_LENS_SCHEMA_v0.1.yaml`. If the repo isn't cloned, use the schema from the onboarding prompt (or generate a complete Person Lens covering: identity, origin, capabilities, working_style, values, patterns, environment_fit, contradictions, growth_edges, how_to_work_with, evidence). Save it in the current directory, then continue to Phase 1 questions.

**The Big Three:**
1. What's the hardest organizational problem you've ever solved, and what made it hard?
2. When are you at your best? Describe the conditions — team size, problem type, pace, stakes.
3. What do people get wrong about you?

**Working Style:**
4. How do you make decisions when the data is ambiguous?
5. What's your relationship with speed vs. correctness?
6. What breaks your trust? Not theoretically — what has actually broken it.

**Values:**
7. What work are you most proud of that nobody outside your team knows about?
8. What kind of work do you actively avoid, even if you're good at it?
9. What would you build if you had 6 months and no constraints?

After all 9 answers, synthesize the lens, walk me through each section conversationally, iterate on pushback, save the file, then continue to Phase 1 job search questions.
