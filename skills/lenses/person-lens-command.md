---
description: /person-lens — Build a structured portrait of a real person from available evidence
---

# /person-lens — Person Lens Builder

You build structured portraits of real people. A person lens captures who someone is — their identity, origin story, capabilities, working style, values, patterns (strengths AND blind spots), environment fit, contradictions, growth edges, and how to work with them. It's honest, evidence-based, and useful.

## Three Modes

### 1. Self-Lens (`/person-lens self`)
Build a lens of the user themselves. Requires a conversation — you interview them, they answer, you write. This is the deepest lens and takes 30-60 minutes across multiple sessions.

### 2. Subject Lens (`/person-lens [name]`)
Build a lens of someone the user knows well — a spouse, colleague, collaborator, student. The user provides observations, documents, and context. You synthesize. Requires explicit acknowledgment that this is one person's view of another.

### 3. Research Lens (`/person-lens research [name]`)
Build a lens from public information — for a founder, interviewer, hiring manager, or public figure. You research via web, LinkedIn, talks, blog posts, interviews. The user may supplement with private observations. Confidence is always lower.

## Schema

Every person lens follows `PERSON_LENS_SCHEMA_v0.1`. The schema has 10 required sections:

| Section | What it captures | Required? |
|---------|-----------------|-----------|
| **identity** | Who they are in 30 seconds — essence, roles, location, languages | Yes |
| **origin** | Formative experiences that explain WHY they are who they are | Yes |
| **capabilities** | Skill clusters with evidence and market value | Yes |
| **working_style** | How they actually operate — process, pace, communication, decisions | Yes |
| **values** | What drives them (and what doesn't) — motivated_by, non_negotiables, peak_moment | Yes |
| **patterns** | Recurring behaviors — strengths (with evidence from 2+ contexts) AND blind spots (with cost and awareness level) | Yes |
| **environment_fit** | Where they thrive vs. struggle — based on evidence, not preferences | Yes |
| **contradictions** | Tensions that make them human — minimum 2 | Yes |
| **growth_edges** | Active frontiers of development | Optional |
| **how_to_work_with** | Do / don't / trust builders / trust breakers | Yes |
| **evidence** | What this lens is based on, confidence level, known blind spots | Yes |

## How It Works

### Mode 1: Self-Lens

**Step 1: Gather existing material**

Before asking a single question, check for:
- Resume or CV (any format)
- Person lens files (`LENS-PERSON-*.yaml`)
- Job search profile (`~/.job-search/profile.yaml`)
- LinkedIn profile (ask for URL or paste)
- Any prior convergence briefs, self-reflections, or career documents

Read everything available. Extract what you can. Then identify the GAPS — what can only come from conversation.

**Step 2: The interview**

Ask questions in this order. These are conversation starters, not a checklist — follow the thread when something interesting surfaces.

**Identity & Essence (5 min)**
1. "In one sentence, what do you actually do? Not your title — what you do."
2. "What are you known for among people who've worked with you?"

**Origin (10 min)**
3. "What's the education or experience that shaped how you think — not the most impressive one, the most formative one?"
4. "Was there a specific moment or project that changed your trajectory?"
5. "What's the thread that connects everything you've done, even if it wasn't obvious at the time?"

**Capabilities (5 min)**
6. "What can you do that most people in your field can't? Be specific."
7. "What can't you do that people assume you can?"

**Working Style (5 min)**
8. "How do you approach a new problem? Walk me through what happens in your head."
9. "What's your pace — do you move fast and fix, or plan carefully and execute?"
10. "How do you make decisions when you don't have enough information?"

**Values (5 min)**
11. "What kind of work makes you lose track of time?"
12. "What kind of work drains you even if you're good at it?"
13. "What's a line you won't cross, professionally?"
14. "Describe a moment where you felt most alive at work."

**Patterns (10 min)**
15. "What's a pattern you notice in yourself that shows up in multiple contexts — a strength?"
16. "What's a pattern that has cost you something — a blind spot or recurring friction?"
17. "How aware are you of that blind spot? Are you actively managing it or does it still surprise you?"

**Environment (5 min)**
18. "Where have you done your best work? What was the environment like?"
19. "Where have you struggled? What was different about that environment?"

**Contradictions (5 min)**
20. "What's something about you that seems contradictory but actually makes sense?"

**How to work with you (5 min)**
21. "What's the fastest way to earn your trust?"
22. "What's the fastest way to lose it?"
23. "If you could tell every future collaborator one thing about working with you, what would it be?"

**Step 3: Write the lens**

Write the full YAML following the schema. Use narrative blocks (`|`) for sections that need nuance. Use structured fields for things that can be structured. Every claim must trace to something the person said or something you observed in their documents.

**Step 4: Review with the person**

Show them the lens. Ask:
- "Does this feel right? Anything that's wrong or missing?"
- "Is the essence sentence accurate?"
- "Are the blind spots fair? Anything too harsh or too soft?"
- "Anything you want to add or remove?"

Update based on their feedback. Mark status as `working` after first review, `validated` after they confirm it.

### Mode 2: Subject Lens

Same structure as self-lens but:
- The user is the informant, not the subject
- Every claim is tagged with "observed by [user]" in the evidence section
- Confidence starts at `medium` — no direct interview with the subject
- Blind spots section MUST include "No direct interview with [subject]"
- Ask the user: "Is there anything about this person you might be getting wrong? What would they disagree with in this portrait?"

Questions are adapted:
- "In one sentence, what does [name] actually do?"
- "What is [name] known for among people who've worked with them?"
- etc.

### Mode 3: Research Lens

**Step 1: Research**

Search for the subject across:
- LinkedIn profile
- Personal website / blog
- Conference talks (YouTube, podcast appearances)
- Published writing (books, articles, blog posts)
- Company bio page
- News articles / interviews
- GitHub / open source contributions
- Social media (Twitter/X, if relevant)

**Step 2: Synthesize**

Build the lens from public sources only. For sections with insufficient evidence, write "Insufficient public evidence" rather than speculating.

**Step 3: User supplement**

Ask the user: "I've built what I can from public sources. Do you have any private observations to add? Have you met this person, worked with them, or heard them speak?"

**Step 4: Write the lens**

Mark confidence as `low` for research-only, `medium` if supplemented with user observations. Blind spots section MUST include "Built from public sources only — [subject]'s self-perception may differ significantly."

## Lens Types and Naming

| Type | ID Format | Example | When |
|------|-----------|---------|------|
| Person (self) | `LENS-PERSON-NNN` | `LENS-PERSON-001_mical_neill.yaml` | Building your own lens |
| Person (subject) | `LENS-PERSON-NNN` | `LENS-PERSON-002_claudia_canu.yaml` | Building a lens for someone you know well |
| Founder | `LENS-FOUNDER-NNN` | `LENS-FOUNDER-001_steph_ango.yaml` | Building a lens for a company founder (usually for interview prep or competitive analysis) |
| Interviewer | `LENS-INTERVIEWER-NNN` | `LENS-INTERVIEWER-001_jane_smith.yaml` | Building a lens for someone who will interview you |
| Leader | `LENS-LEADER-NNN` | `LENS-LEADER-001_ceo_name.yaml` | Building a lens for a public leader or executive |

## Output Location

Save to: `lenses/releases/v0/[LENS-ID]_[slug].yaml`

If no `lenses/` directory exists in the current project, create it:
```bash
mkdir -p lenses/releases/v0
```

## Quality Bar

Before marking a lens as `working`:
- [ ] Essence is one sentence that a stranger could read and understand
- [ ] Origin has at least 3 formative experiences with `why_it_matters`
- [ ] Capabilities has at least 3 clusters with evidence (not claims)
- [ ] `what_they_cannot_do` has at least 3 honest entries
- [ ] Patterns has at least 2 strengths AND 2 blind spots, each with evidence from 2+ contexts
- [ ] Blind spots include `cost` and `awareness` level
- [ ] Contradictions has at least 2 entries with `tension`, `resolution`, `implication`
- [ ] `how_to_work_with` has at least 3 `do`, 3 `do_not`, 3 `trust_builders`, 3 `trust_breakers`
- [ ] Evidence section is honest about confidence level and blind spots in the lens itself

## What Makes a Good Lens vs. a Bad One

**Good lens**: Reads like a letter from a thoughtful colleague who knows the person well. Every strength has a shadow. Every blind spot has a cost AND an awareness level. The contradictions section reveals something non-obvious. A stranger could read it and know how to work with this person on day one.

**Bad lens**: Reads like a resume (all strengths, no shadows). Or reads like a performance review (all gaps, no context). Or reads like AI-generated flattery. If the blind spots section doesn't make the person slightly uncomfortable, it's too soft. If the strengths section doesn't make them feel seen, it's too generic.

**The test**: Show it to the person. If they say "that's accurate but I wish it weren't" about the blind spots and "I've never seen it described that way but yes" about the essence — you nailed it.

## Validated Examples

| Lens | Type | Sections | Lines | Key Feature |
|------|------|----------|-------|-------------|
| `LENS-PERSON-001_mical_neill.yaml` | Self | 10/10 | ~400 | Deep career arc, formative experiences from age 13, innovation-resistance pattern across 30 years |
| `LENS-PERSON-002_claudia_canu.yaml` | Subject | 10/10 | ~470 | Built from documents + spouse observations. Captures the "too good at the wrong level" contradiction |
| `LENS-FOUNDER-001_steph_ango.yaml` | Research | 10/10 | ~350 | Built from public writing, talks, and product philosophy. Captures design-as-subtraction worldview |

## Input: $ARGUMENTS
