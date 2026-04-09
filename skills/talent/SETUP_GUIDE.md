# Job Search Tool — Setup Guide

An AI-powered job search tool that finds real jobs online, scores them against your profile, and tracks your pipeline. First time you run it, it reads your resume and builds your profile. After that, it searches the internet for matching jobs and ranks them by fit.

---

## Option A: Claude Code (recommended)

Searches the internet for you, saves your profile across sessions, tracks your pipeline. Requires a Claude Pro subscription ($20/month).

### Setup (one time, ~10 minutes)

**1. Install Node.js**

Mac — open Terminal (search "Terminal" in Spotlight) and run:
```bash
brew install node
```
If that fails, install Homebrew first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Windows — download and run the installer from https://nodejs.org (choose LTS).

**2. Install Claude Code**
```bash
npm install -g @anthropic-ai/claude-code
```

**3. Download the job search tool**

Mac/Linux:
```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/job-search.md https://raw.githubusercontent.com/pretendhome/palette/main/skills/talent/job-search-command.md
```

Windows (PowerShell):
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\commands"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/pretendhome/palette/main/skills/talent/job-search-command.md" -OutFile "$env:USERPROFILE\.claude\commands\job-search.md"
```

**4. Start Claude Code**
```bash
claude
```
First time: it will ask you to log in with your Claude account.

**5. Run the tool**

Type `/job-search` and hit enter. Have your resume ready (file on your computer or text to paste).

### What to expect

- **First run**: It asks for your resume, then 5 quick questions. Takes ~5 minutes. Saves your profile locally.
- **Permission prompts**: Claude Code will ask your permission before searching the web or saving files. This is normal — just say yes (or type `y`). You can also type "always allow" so it stops asking.
- **After setup**: `/job-search find` to search, `/job-search score` to evaluate a posting, `/job-search pipeline` to track.

### Example output

```
| # | Score | Verdict        | Company    | Role               | Location | Top Match          | Top Gap        |
|---|-------|----------------|------------|--------------------|----------|--------------------|----------------|
| 1 | 91    | STRONG FIT     | Anthropic  | Solutions Engineer | SF       | AI systems, Python | Startup exp    |
| 2 | 83    | WORTH APPLYING | Databricks | Field Engineer     | Remote   | Data + enablement  | Spark depth    |
| 3 | 71    | STRETCH        | Stripe     | Technical PM       | SF       | Cross-functional   | Payments exp   |
```

---

## Option B: Claude Cowork (easiest setup — no terminal needed)

If you have the Claude Desktop app on Mac or Windows with a Pro, Max, or Team plan, Cowork is the easiest path. No terminal, no install commands.

**1.** Make sure you have the latest Claude Desktop app (download from https://claude.ai/download)

**2.** Create a folder on your computer for the job search tool. For example:
- Mac: `~/Documents/job-search/`
- Windows: `Documents\job-search\`

**3.** Download the tool file into that folder:
- Go to: https://raw.githubusercontent.com/pretendhome/palette/main/skills/talent/job-search-command.md
- Right-click → "Save As" → save it as `job-search-command.md` in your job-search folder
- Also save your resume (PDF, Word, or text) in the same folder

**4.** Open Claude Desktop and start a Cowork session. Point it at your job-search folder.

**5.** Tell Claude:

```
Read the file job-search-command.md and follow those instructions.
Set me up — my resume is in this folder.
```

Claude will read the tool instructions, read your resume, and walk you through setup.

**After setup, you can say things like:**
- "Find jobs that match my profile"
- "Score this job posting: [paste URL]"
- "Optimize my resume for this job: [paste URL]"
- "Run a mock interview for [company] [role]"
- "Research [company] before my interview"
- "Give me a glance sheet for my interview tomorrow"
- "Debrief — I just finished an interview at [company]"

Everything saves in your job-search folder. Claude Cowork remembers your context within a project.

---

## Option C: Claude.ai (free, no install)

Can't search for you or save your profile, but scores job postings you paste in. Works with the free Claude account.

**1.** Go to https://claude.ai and log in (or create a free account)

**2.** Start a new conversation and paste this (replace `[PASTE YOUR RESUME HERE]` with your actual resume text):

```
You are my job search assistant. Score job postings I give you against my resume.

For each posting, score these dimensions (weighted average, 0-100):
- Title match (20%): how close to my target level and function?
- Skills match (25%): what % of their required skills do I have?
- Experience level (15%): am I in the sweet spot, over, or underqualified?
- Domain fit (15%): is this my industry or adjacent?
- Location (10%): does it work for me?
- Differentiator (15%): does this role benefit from what makes me unique?

Give me: score, verdict (STRONG FIT / WORTH APPLYING / STRETCH / PASS),
top 3 strengths, top 3 gaps. Be honest — don't inflate scores.

My resume:
[PASTE YOUR RESUME HERE]
```

**3.** Each time you find a job posting, paste it into the conversation and ask Claude to score it.

---

## Tips

- **Run `/job-search find` weekly.** New jobs post constantly.
- **Score before you apply.** Below 65 = pass. Discipline beats volume.
- **Bring results to JSC meetings.** Run a search before the meeting, bring your top 5, discuss with the group.
- **Your data stays on your computer.** Profile at `~/.job-search/profile.yaml`, pipeline at `~/.job-search/pipeline.csv`. Nothing is uploaded. Delete anytime.
- **Options A and B remember you.** Option C starts fresh each conversation — re-paste your resume each time.
- **Update your profile as you learn.** After Listening Tour conversations or CMF work, run `/job-search update` to sharpen your targeting.

---

## Troubleshooting

**"command not found" when running `claude`**: Node.js or Claude Code didn't install correctly. Try `node --version` to check Node is installed, then re-run `npm install -g @anthropic-ai/claude-code`.

**"/job-search not found" inside Claude Code**: The command file isn't in the right place. Check that `~/.claude/commands/job-search.md` exists. Re-run the curl command from step 3.

**"Permission denied" errors**: Claude Code asks before doing things (searching, saving files). Type `y` to allow, or "always allow" to stop being asked.

**Can't read my resume file**: Try pasting the text directly instead. Some PDF formats are harder to parse than others.

---

## Questions?

Ask the operator in our next JSC meeting or message in our group channel.
