# Interview Prep Bot — Quickstart

## What You Get
Five deliverables per interview:
1. **ANSWERS.md** — Dense, no-spacing spoken answers. Every question on one screen. Hardcoded format: `## HEADER` then dense paragraph, no blank lines between sections. Operating principle, core positioning, 15-20 Q&As, anchor phrases, avoid list, rehearsal protocol. Reference format: `lumen-technical-enablement/prep-bot/ANSWERS.md` or `capital-group-principal-ai/prep-bot/ANSWERS.md`
2. **CHEATSHEET.md** — Fast card for 5-10 min before the call. 30-sec opener, proof points, questions to ask, logistics, last-minute check. One page max.
3. **COMPANY_SYSTEMS.md** — Dense spoken answers about THE COMPANY: products, leadership, domain vocabulary, what the role exists for, anchor phrases, what to avoid.
4. **ANSWERS_FULL.md** — Extended narrative versions of each answer with full stories, data points, and conditional logic (if they ask X, pivot to Y). Study material for the night before.
5. **`~/.local/bin/[company]-prep`** — Terminal voice practice bot. Rime TTS reads questions aloud, Whisper STT captures your answer, Claude/GPT evaluates and gives feedback (what landed, what drifted, one concrete fix). Push-to-talk.

All files land in: `implementations/talent/applications/active/[company-slug]/prep-bot/`
Voice bot goes in: `~/.local/bin/[company]-prep`

---

## The Prep Bot Voice Script Format

Every `~/.local/bin/[company]-prep` follows this exact pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail

export CODEX_MODEL="${CODEX_MODEL:-gpt-5.4}"

exec /home/mical/.local/bin/palette-voice \
  --brain claude \
  --context-dir /home/mical/fde/implementations/talent/applications/active/[company-slug]/prep-bot \
  --system-prompt "[SYSTEM PROMPT — see below]" \
  "$@"
```

The system prompt must include:
- Role: "You are a live interview prep coach for [role] at [company]"
- Interviewer context: name, title, what they care about
- Drill structure: "Ask one question at a time. Wait for answer. Give feedback in three parts: what landed, what drifted, one concrete fix."
- Required vocabulary: company-specific terms the user MUST use
- Required proof points: specific evidence the user MUST cite
- Anti-drift rules: what NOT to let the user hide behind (generic AI language, architecture monologues, etc.)
- Mode/register: warm vs technical, designer vs engineer, etc.

Reference implementations:
- `~/.local/bin/lumen-prep` — recruiter screen mode, alternates fit + company fluency
- `~/.local/bin/alpine-prep` — warm/linguistic mode, pushes for lived experience over engineering
- `~/.local/bin/capitalgroup-prep` — technical authority mode, production engineering focus
- `~/.local/bin/ibusiness-prep` — knowledge data engineering mode

---

## ANSWERS.md Hardcoded Format

NOT coaching notes. NOT spaced out. Dense paragraphs with `##` headers, no blank lines between sections. Maximum answers visible at once. The format:

```markdown
# [COMPANY] [ROLE] — ANSWERS
# [Interviewer] — [Date], [Time], [Duration], [Platform]
## OPERATING PRINCIPLE FOR [INTERVIEWER]
[Dense paragraph: who they are, what they screen for, your mode, what to avoid. No line breaks.]
## CORE POSITIONING
[One reusable sentence that anchors every answer.]
## TELL ME ABOUT YOURSELF
[Dense paragraph — the actual words you say. 60 seconds spoken. No bullets.]
## WHY [COMPANY]
[Dense paragraph. Two reasons max. Specific to their product/mission.]
## [TOPIC FROM JD]
[Dense paragraph: what I did → where → specific numbers → parallel to their domain → closing.]
## [TOPIC FROM JD]
[Same format. Keep going — 15-20 sections total.]
## AVOID SAYING
"term" · "term" · "term" — all on one line separated by middle dots
## ANCHOR PHRASES
"phrase" · "phrase" · "phrase" — all on one line separated by middle dots
## CONSERVATIVE TELL / OVERRIDE
**The tell**: [what it sounds like when you drift]. **The override**: [how to snap back].
## REHEARSAL PROTOCOL
1. 60-second rep: [structure]. 2. 5-minute rep: [structure]. 3. Stress rep: [structure]. 4. Red-team rep: [self-check question].
```

**The test**: If you see blank lines between paragraphs, the format is wrong. Every `##` header starts immediately after the previous section's last line.

---

## Prerequisites (one-time setup)

| What | Where | How to create |
|------|-------|---------------|
| **Profile** | `~/.job-search/profile.yaml` | Run `/job-search` — walks you through setup |
| **Answer Backbone** | `palette/skills/talent/ANSWER_BACKBONE.md` | Career experiences organized by topic. Verified numbers. |
| **STAR Stories** | `palette/skills/talent/STAR_STORIES.md` | Behavioral stories mapped to competencies |
| **Person Lens** | `palette/lenses/releases/v0/LENS-PERSON-001_*.yaml` | Your voice, patterns, values — so the prep sounds like you |
| **palette-voice** | `~/.local/bin/palette-voice` | The Rime TTS + Whisper STT engine. One-time install. |

---

## The 3 Steps

### Step 1: Generate prep materials

```
/job-search prep-bot
```

Provide: JD (paste or URL), interviewer info (name, LinkedIn, role), round context (recruiter screen, technical, panel, etc.)

The system generates all 5 deliverables.

### Step 2: Tighten the ANSWERS.md

The system gives you V1. You tighten it until it sounds exactly like you. Read every section out loud — if it sounds like advice TO you, it's wrong. If it sounds like YOU talking to the interviewer, it's right.

### Step 3: Practice with voice bot

```bash
# Terminal voice practice with Rime TTS + feedback
[company]-prep

# Quick browser version (no voice, timer-based)
open implementations/talent/applications/active/[company-slug]/prep-bot/[company]-*-prep.html
```

**Practice protocol**:
1. Read ANSWERS.md once — internalize the dense answers
2. Read COMPANY_SYSTEMS.md once — learn the vocabulary
3. Run `[company]-prep` — do 2-3 voice rounds with feedback
4. Before the call: re-read CHEATSHEET.md (5 min) as final refresh

---

## Quality Checks

- [ ] ANSWERS.md is dense format (no blank lines between sections)
- [ ] Every answer cites at least one specific number or project
- [ ] AVOID SAYING list includes company-specific anti-patterns
- [ ] ANCHOR PHRASES list has 5-10 quotable closers
- [ ] Voice bot system prompt includes required vocabulary AND required proof points
- [ ] `[company]-prep` is executable at `~/.local/bin/`
- [ ] All 5 deliverables exist in the prep-bot directory
