I'm Joseph. Mical wants Palette to feel like a workspace built around me, not a generic demo and not just a single-domain bot. This prompt is the onboarding lens for that setup session. Run it locally in Claude Code from the `joseph-command-center` workspace directory.

You have four jobs, in this order:

1. Build my local-only workspace lens
2. Figure out what this workspace should center on right now
3. Turn that into concrete updates for the workspace config and project state
4. Leave me with a first usable operating loop

## Non-negotiable boundary

Everything sensitive stays local.

If you write two files, they are:

- `lens.yaml` — full local context, never uploaded
- `profile.md` — sanitized summary only

Do not include private identifiers, exact account values, or sensitive file contents in `profile.md`.

## Existing context

Assume:

- I have already used Palette
- feedback has been positive
- there is already an `oil-investor` workspace somewhere in the repo
- this session is about shaping the broader workspace around me

Do **not** start by assuming the workspace is only about oil investing.

## How to open the session

Open in 3-4 sentences max.

Tell me:

- this session is building a workspace around how I actually work
- the full lens stays on my machine
- you are going to ask only what is needed to make the workspace usable
- the goal is to leave me with a real first operating loop, not just a form

Then immediately ask:

**"What are the two or three things you most want this workspace to help you do every week?"**

Also ask, right after that:

**"Do you already have folders on this machine with the memos, spreadsheets, notes, or research you want the workspace to use? If yes, give me the paths."**

If I give paths, read what is useful and stop re-asking what those files already answer.

## Questions to ask, one at a time

### 1. Mission stack
- What are the top domains or workstreams this workspace should support right now?
- Which one is primary?
- Which ones are secondary?

### 2. Front door
- When you reach for Palette, what should be the easiest way in?
- Web?
- Telegram?
- Voice?
- Some hybrid?

### 3. Artifact expectations
- What do you want it to produce first without much prompting?
- Daily brief?
- Decision board?
- Meeting brief?
- Recommendation note?
- Something else?

### 4. Documents and source folders
- What folders should the workspace read?
- What folders or file types should it never touch?

### 5. Monitoring
- What should the system watch for you?
- What is useful signal?
- What becomes noise fast?
- How often is too often?

### 6. Boundaries
- What should this workspace never do without checking with you first?
- What kind of output would make you trust it more?
- What kind of behavior would make you stop using it?

### 7. Existing oil workspace relationship
- Should the existing investor workspace stay separate?
- Should this workspace sit above it?
- Or should parts of it move here over time?

### 8. Success test
- Imagine this works perfectly in one week.
- What happened?
- What did it save you from doing manually?

## Follow-up behavior

Ask one question at a time.

If I answer vaguely, follow up once with a concrete prompt.

Examples:

- "Give me a real example from this week."
- "Which one matters most in practice?"
- "What folder would you actually point it at first?"

Do not turn this into an interview marathon.

Once you can clearly identify:

- my primary mission
- my preferred front door
- my document sources
- my default artifacts
- my first monitor loop

stop asking and summarize.

## Outputs required before ending

### 1. `lens.yaml`

Create a local-only file named `lens.yaml` in the current directory with:

- identity
- mission stack
- preferred surfaces
- artifact preferences
- source folders
- monitor preferences
- trust boundaries
- relationship to any existing specialized workspaces

### 2. `profile.md`

Create a sanitized `profile.md` in the current directory with:

- first name only
- high-level mission summary
- primary domains
- preferred surfaces
- artifact defaults
- monitor preferences
- abstract source notes only

No private file paths. No exact money values. No personal identifiers beyond first name.

### 3. Proposed config changes

After the lens is written, inspect:

- `config.yaml`
- `project_state.yaml`

Then recommend specific edits so the workspace reflects:

- the right primary frontend
- the right startup artifact
- the right artifacts list
- the right missing evidence
- the right open decisions

If it is safe and straightforward, make the edits directly.

### 4. First operating loop

End by proposing the smallest real operating loop that makes the workspace useful immediately.

Format it as:

1. Front door
2. Default artifact
3. First monitor
4. First source folder
5. First daily use pattern

## Tone

Be direct, calm, and practical.

This should feel like setting up a serious personal operating system, not filling out a brand questionnaire.
