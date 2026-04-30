# Interview Prep Bot — 3-Step Quickstart

## What You Get
Three deliverables, nothing else:
1. **CHEATSHEET.md** — Dense spoken answers about YOU + your fit for THIS role
2. **COMPANY_SYSTEMS.md** — Dense spoken answers about THE COMPANY (products, leadership, domain vocabulary)
3. **[company]-interview-bot.html** — Local interview drill tool (open in browser, practice with timer + pressure mode)

All three land in: `~/.job-search/applications/active/[company-slug]/prep-bot/`

---

## Prerequisites (one-time setup)

You need two things on file before your first prep:

| What | Where | How to create |
|------|-------|---------------|
| **Profile** | `~/.job-search/profile.yaml` | Run `/job-search` — it walks you through setup |
| **Answer Backbone** | `~/.job-search/ANSWER_BACKBONE.md` | Your career experiences organized by topic. One experience per topic. Verified numbers. See template below. |

Optional but recommended:
- **Person Lens** (`LENS-PERSON-*.yaml`) — captures your voice so the cheatsheet sounds like you, not AI
- **Format Spec** (`~/.job-search/format-spec.md`) — an example of YOUR preferred dense-answer style. If absent, the system uses the default dense paragraph format.

---

## The 3 Steps

### Step 1: Pull your prep

```
/job-search prep-bot
```

It asks: "Which role?" — you provide ONE of:
- A pipeline number (e.g., `#3`)
- A URL to the job posting
- Paste the full JD text

### Step 2: Drop in the JD + interviewer info

When prompted, provide:
- **Job Description** — paste it or give a URL
- **Interviewer LinkedIn** — paste the URL if you have it (optional but makes COMPANY_SYSTEMS sharper)
- **Any notes** — "this is a recruiter screen", "technical round", "the hiring manager is the VP of Education", etc.

The system then:
1. Reads your format spec (how your answers should sound)
2. Reads your ANSWER_BACKBONE (your experience library)
3. Maps JD requirements → your experiences (one per topic, no double-dipping)
4. Researches the company (products, leadership, recent news)
5. Generates all three deliverables

### Step 3: Open and practice

```bash
# Open the interview bot in your browser
open ~/.job-search/applications/active/[company-slug]/prep-bot/[company]-interview-bot.html

# Read these side by side during practice (and during the call)
cat ~/.job-search/applications/active/[company-slug]/prep-bot/CHEATSHEET.md
cat ~/.job-search/applications/active/[company-slug]/prep-bot/COMPANY_SYSTEMS.md
```

**Practice protocol**:
- Read CHEATSHEET.md once silently — internalize the structure
- Read COMPANY_SYSTEMS.md once — learn the vocabulary
- Open the HTML bot — do 2-3 timed runs
- The bot grades you on: (1) company vocabulary used? (2) concrete evidence cited? (3) stayed specific or drifted?

---

## What the Cheatsheet Looks Like

NOT coaching notes. NOT bullets. Dense spoken paragraphs — the actual words you say:

```markdown
## TELL ME ABOUT YOURSELF
"I spent 12 years building knowledge systems at Amazon, then left to build
Palette — a 121-node taxonomy, 176-entry sourced library, and 12-agent
orchestration system that routes any AI decision to the right knowledge.
What that taught me is that the model is replaceable but the knowledge
architecture is the moat. That is why [Company]'s approach interests me..."

## WHY [COMPANY]
"What fascinates me about [Company] is [specific structural insight about
their system]. In this domain, the advantage is not just the model, it is
[specific thing about their data/approach]..."

## [KEY TOPIC FROM JD]
Dense paragraph with: what I did → where → specific numbers → closest
parallel to their domain → closing line. 30-90 seconds spoken.

## AVOID SAYING
"chatbot" · "just prompt it better" · [company-specific terms to avoid]

## ANCHOR PHRASES
"The model is replaceable. The knowledge architecture is the moat." ·
"I did not build Palette to demonstrate Palette. I built it to demonstrate
the discipline." · [3-5 more quotable closers]
```

**The test**: Read every section out loud. If it sounds like advice TO you, it's wrong. If it sounds like YOU talking to the interviewer, it's right.

---

## ANSWER_BACKBONE Template

If you don't have one yet, build it. One section per major interview topic. Multiple experiences per section. Verified numbers only.

```markdown
# ANSWER_BACKBONE — [Your Name]
# Topic-indexed experience library. Pick ONE per cheatsheet section.

## SQL / DATA ANALYSIS
### Experience 1: [Project Name] (ERA-N)
- Context: ...
- What I did: ...
- Result: [specific number]
- Best for: roles asking about data-driven decision making
- Source: [how you verified the number]

### Experience 2: [Project Name] (ERA-N)
...

## PROGRAM EXECUTION / MULTI-WORKSTREAM
### Experience 1: ...

## [ADD TOPICS MATCHING YOUR TARGET ROLES]
```

---

## FAQ

**Q: Can I edit the cheatsheet after it's generated?**
Yes — and you should. The system gives you V1. You tighten it until it sounds exactly like you.

**Q: What if I don't have an ANSWER_BACKBONE yet?**
Run `/job-search stories` first — it walks you through building your story bank, which becomes the backbone.

**Q: What if the interviewer changes?**
Re-run `/job-search prep-bot` with the new interviewer info. The CHEATSHEET stays mostly the same; COMPANY_SYSTEMS may need updating.

**Q: Do I need palette-voice for the HTML bot?**
No. The HTML bot runs in any browser. palette-voice is only for the terminal voice practice wrapper (optional).
