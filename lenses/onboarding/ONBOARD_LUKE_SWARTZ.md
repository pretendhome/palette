I'm Luke Swartz. My friend Mical Neill built an AI system called Palette and wants to onboard me. This prompt contains everything you need to run the session. Follow these instructions exactly.

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

Look for a file matching `LENS-PERSON-*luke*` or `LENS-PERSON-003*` in the current directory, in `palette/lenses/releases/v0/`, or anywhere under the working directory. If you find one, read it — that's my Person Lens. Skip Phase 1 (lens creation), acknowledge what you loaded, and go straight to Phase 2 (what do I want to build).

If no lens exists, run Phase 1 below to create one.

---

You have three jobs, in this order:
1. Build my Person Lens — a structured portrait of who I am (skip if lens already exists)
2. Ask me what I want to build
3. Build it with me

---

## Partially filled lens (from public LinkedIn — not uploaded anywhere, embedded here only)

This is what I already know. The fields marked `# NEEDS ANSWER` are what the questions below will fill in. Don't re-ask anything that's already filled.

```yaml
lens_id: "LENS-PERSON-003"
name: "Luke Swartz"
version: "0.1"
status: draft
created: "<today's date>"
updated: "<today's date>"
schema: PERSON_LENS_SCHEMA_v0.1

identity:
  essence: ""  # NEEDS ANSWER — will emerge from the 9 questions
  roles:
    - "Senior Director of PM at Capital One (ended Jan 2026)"
    - "ex-Google GPM (12.5 years)"
    - "US Navy veteran, former submarine officer"
  location: "San Francisco, CA"
  languages:
    - { language: "English", proficiency: "native", context: "" }
    - { language: "French", proficiency: "limited working", context: "" }
    - { language: "Italian", proficiency: "conversational", context: "wikinapoli.com, stationed in Naples" }

origin:
  education_arc: |
    BS Symbolic Systems (emphasis: Educational Design, HCI) + MS Computer Science (HCI),
    Stanford. Studied AI with Andrew Ng. Won K. Jon Barwise Award. The Symbolic Systems
    degree is unusual — it bridges cognitive science, linguistics, philosophy, and CS.
    The HCI emphasis in both degrees suggests he thinks about systems from the human side first.
  formative_experiences:
    - what: "US Navy submarine officer, USS Ohio (nuclear-powered)"
      when: "2003-2010"
      why_it_matters: |
        7 years managing teams of 5-30 on a nuclear submarine. Certified Nuclear Engineer.
        Special Operations Assistant in Naples, Italy. Two-time Junior Officer of the Year.
        This is where organizational complexity stopped being abstract.
    - what: "Google — 12.5 years across Search Ads, i18n, Android, Fuchsia"
      when: "2010-2023"
      why_it_matters: |
        Grew revenue from <$50M to >$1B via i18n ads strategy. Led Fuchsia OS launch across
        4 orgs whose only common manager was the CEO. Managed PM teams across 3 continents.
        Re-wrote the introductory PM course for 100s of new Google PMs. This is where he
        learned to operate at scale across organizational boundaries.
    - what: "Capital One — front-end infrastructure for 100M+ customers"
      when: "2023-2026"
      why_it_matters: |
        Led 5 PMs + 80-person cross-functional team. Design system NPS from -2 to 38.
        Platform/infrastructure product serving internal teams. # NEEDS ANSWER — what drove the move, what happened after Jan 2026
    - what: "Pro bono: SF housing pipeline data warehouse"
      when: "during Google tenure"
      why_it_matters: |
        Built a data warehouse and dashboard for the City of San Francisco to understand its
        housing pipeline. Ethnographic UX research, dozens of diverse stakeholders, user-centered
        design with government executives. Shows values-driven work outside the job description.
  career_throughline: ""  # NEEDS ANSWER — the thread connecting Navy → Google → Capital One → what's next

capabilities:
  clusters:
    - name: "Cross-organizational alignment"
      strength: exceptional
      evidence:
        - "Fuchsia OS launch across 4 orgs (only common manager = CEO)"
        - "Android 13 per-app language prefs across 5 timezones"
        - "Emoji product inclusion: convinced SVP, rallied teams company-wide"
        - "Obtained buy-in through SVP+ for multiple launches"
      market_value: "Extremely high at VP+ level — most PMs can't operate across org boundaries"
    - name: "Platform & infrastructure product management"
      strength: exceptional
      evidence:
        - "Capital One front-end infra for 100M+ customers"
        - "ICU4X 1.0: 20MB binary reduced to 100KB"
        - "Design system NPS -2 to 38"
        - "Internal tools with >$1B incremental revenue impact"
      market_value: "High demand — infra PM is hard to hire for, especially with business impact evidence"
    - name: "Revenue strategy & growth"
      strength: exceptional
      evidence:
        - "i18n ads: <$50M to >$1B annual revenue"
        - "Search Ads: 3 formats grew >$500M annual revenue"
        - "ML content recommendation: +5-20% user growth & engagement"
      market_value: "Rare combination — most revenue PMs don't do infra, most infra PMs can't show revenue"
    - name: "Internationalization & language technology"
      strength: defining
      evidence:
        - "Google Assistant NLU/NLG scaled to 12 languages"
        - "6 patents on language classification and i18n"
        - "Thought leader for language handling across Google Search"
        - "ICU4X 1.0 launch"
      market_value: "Niche but deep — defining expertise in a field most PMs treat as a checkbox"
    - name: "PM team building & mentorship"
      strength: strong
      evidence:
        - "Managed PM teams across 3 continents"
        - "Re-wrote and taught PM course to 100s of new Google PMs"
        - "Mentored dozens of PMs through promotions and career challenges"
        - "9 years people management"
      market_value: "Table stakes at Director+ level, but the teaching/course-writing shows unusual depth"
  tools_and_tech:
    - "ML/AI product strategy"
    - "NLP/NLU/NLG"
    - "Cross-platform frameworks (mobile, web, OS)"
    - "Front-end infrastructure & design systems"
    - "Data-driven experimentation"
    - "Web standards"
  what_they_cannot_do: []  # NEEDS ANSWER — honest gaps

working_style:
  process: ""          # NEEDS ANSWER (questions 1, 4, 5)
  pace: ""             # NEEDS ANSWER (question 5)
  communication: |
    Published thinker — writes frameworks (Hierarchy of Product Metrics), argues positions
    publicly (Dorsey/Botha rebuttal, Anthropic trust post). Direct, evidence-based,
    willing to challenge authority when the argument is sound.
  decision_making: ""  # NEEDS ANSWER (question 4)
  collaboration_mode: ""  # NEEDS ANSWER
  when_they_are_at_their_best: ""  # NEEDS ANSWER (question 2)
  when_they_struggle: ""           # NEEDS ANSWER

values:
  motivated_by: []       # NEEDS ANSWER (questions 7, 9)
  not_motivated_by: []   # NEEDS ANSWER (question 8)
  non_negotiables: []    # NEEDS ANSWER (question 6 — trust)
  peak_moment:           # NEEDS ANSWER (question 7)
    what: ""
    why: ""
    what_it_reveals: ""

patterns:
  strengths:
    - pattern: "Finds the alignment path across organizational boundaries"
      evidence:
        - "4-org Fuchsia launch"
        - "5-timezone Android 13 language prefs"
        - "Emoji inclusion: SVP buy-in + company-wide execution"
      why_it_works: "Combines empathetic listening with clear communication of trade-offs"
    - pattern: "Builds frameworks that others adopt"
      evidence:
        - "Hierarchy of Product Metrics (public)"
        - "PM course rewrite adopted by 100s of Google PMs"
      why_it_works: "Makes complex things teachable — Symbolic Systems training"
    # NEEDS MORE from answers — minimum 3 total
  blind_spots: []  # NEEDS ANSWER — minimum 2

environment_fit:
  thrives_in:
    - environment: "High organizational complexity with technical depth"
      why: "His best work (Fuchsia, i18n ads, Android language prefs) all involved 3+ orgs"
      evidence: "Every major career achievement involved cross-org navigation"
  struggles_in: []  # NEEDS ANSWER
  ideal_team_size: ""  # NEEDS ANSWER (question 2)

contradictions: []  # NEEDS ANSWER — minimum 2. Likely candidates from public signal:
  # Nuclear submarine officer → PM who writes about product metrics pyramids
  # Infrastructure/platform (invisible) → cares deeply about user-facing inclusion (emoji, accessibility)
  # Revenue driver ($1B+) → pro bono housing dashboard for SF
  # But need to hear from him which tensions are real

growth_edges: []  # NEEDS ANSWER

how_to_work_with:
  do: []             # NEEDS ANSWER
  do_not: []         # NEEDS ANSWER
  trust_builders: [] # NEEDS ANSWER (question 6)
  trust_breakers: [] # NEEDS ANSWER (question 6)

evidence:
  sources:
    - "LinkedIn public profile"
    - "Published LinkedIn articles and posts"
    - "Patent filings"
    - "LinkedIn recommendations (Stefano Brunelli, Jennifer Daniel)"
    - "Onboarding conversation (this session)"
  confidence: medium
  last_validated: "<today's date>"
```

---

## Phase 1: Build my Person Lens

When you receive this prompt, start immediately — don't wait for another message.

Open with a brief intro — 3-4 sentences max. Tell me: Palette is Mical's AI system, you're building a structured portrait of me, it takes 15-20 minutes, everything stays on my machine, and you already have a head start from my public profile so you're only going to ask what LinkedIn doesn't show. Then immediately ask question 1. Do not list all the questions — just ask the first one.

Before asking question 1, also ask: **"Do you have a folder where you keep your job search documents — resumes, JDs, notes, anything like that? If so, give me the path and I'll read what's there to save us both time."** If I give a path, read the contents and use them to inform the lens and skip questions I've already answered in those documents.

Ask the 9 questions below ONE AT A TIME. Wait for my answer before asking the next one. If I give a one-sentence answer to a question that deserves more, follow up once — "Can you give me a specific example?" or "What made that hard specifically?" If I redirect, follow me. If I want to skip a question, let me.

After the Big Three, briefly reflect back what you're hearing before moving to Working Style. After Working Style, do the same before Values. These micro-summaries build trust and let me correct course early.

**The Big Three:**
1. What's the hardest organizational problem you've ever solved, and what made it hard? (Not the most impressive — the hardest.)
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

After all 9 answers, complete the partially filled lens above. Fill every `# NEEDS ANSWER` field with real content based on my answers. Do not leave any field empty — write real content or explicitly note "not enough information from this session."

Minimums: at least 3 capability clusters (already have 5 — add or refine from answers), 3 formative experiences (already have 4), 3 strengths (have 2 — need at least 1 more), 2 blind spots, 2 contradictions.

Walk me through each section conversationally — summarize it, don't dump raw YAML. Focus on the sections that are NEW from my answers (working_style, values, blind_spots, contradictions, how_to_work_with) since I already know my own career history. Ask "Does this land? What's wrong?" Iterate on my pushback. Then save the final version as `LENS-PERSON-003_luke_swartz.yaml` in the current directory.

Be honest. Do not flatter. Do not soften blind spots. An honest lens is useful. A flattering one is decoration.

---

## Phase 2: What do I want to build?

After the lens is saved, say: "Your lens is built. Now — what do you want to build?"

If I don't have an answer, suggest ONE thing based on what you heard during the lens conversation. Don't show a menu. Just make your best guess and offer it directly.

If I want to stop after the lens, that's fine. Tell me where the file is and what a next session could look like.

---

## Phase 3: Build it

Do real work. Ship a real artifact in this session.

- Break it into steps. Get my alignment before executing.
- Evidence-based only. No speculation presented as fact.
- Show your reasoning. If you made a judgment call, say so.
- Save files in the current directory. Confirm filenames before writing.
- If something isn't working, say so and adjust.

When we're done:
1. Recap what we built and where the files are
2. If the lens was saved outside the Palette repo, suggest copying it into `palette/lenses/releases/v0/` so future sessions pick it up automatically
3. Suggest what a next session could tackle

---

## Rules

- One question at a time. Never stack.
- Summarize the lens conversationally. Offer raw YAML only if I ask.
- Don't skip the lens to jump to building.
- Don't fabricate anything.
- Don't use jargon before I've used it.
- Don't rush the questions — they're the point.
