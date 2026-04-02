# Job Search Assistant — Setup Guide

An AI-powered job search tool that finds real jobs, scores them against your profile, and tracks your pipeline. First time you run it, it reads your resume and builds your profile. After that, it searches the internet for matching jobs and ranks them by fit. There's a free option (Option B) and a more powerful option that requires a Claude Pro subscription (Option A).

---

## What you need

- A computer (Mac, Windows, or Linux)
- A Claude account — Option A (Claude Code) requires a paid plan (Pro at $20/month or Max). Option B (claude.ai) works with the free tier.

---

## Option A: Claude Code (full experience — recommended)

Claude Code is a command-line tool that runs on your computer. It gives you the `/job-search` command which has the full NSA methodology built in.

### Step 1: Install Node.js

Claude Code requires Node.js 18 or higher.

**Mac:**
```bash
brew install node
```

If you don't have Homebrew, install it first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Windows:**
Download and run the installer from https://nodejs.org (choose the LTS version).

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Step 2: Install Claude Code

Open a terminal (Mac: Terminal app, Windows: PowerShell, Linux: any terminal) and run:

```bash
npm install -g @anthropic-ai/claude-code
```

### Step 3: Download the job search command

Create the folder and download the command file directly from GitHub:

**Mac/Linux:**
```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/job-search.md https://raw.githubusercontent.com/pretendhome/palette/main/skills/talent/job-search-command.md
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\commands"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/pretendhome/palette/main/skills/talent/job-search-command.md" -OutFile "$env:USERPROFILE\.claude\commands\job-search.md"
```

### Step 4: Start Claude Code

```bash
claude
```

It will ask you to log in with your Claude account the first time.

### Step 5: Use it

Once Claude Code is running, type:

```
/job-search
```

**First time**: It will ask for your resume (paste the text or give a file path), then ask a few questions to build your profile. This takes about 5 minutes. Your profile is saved locally on your computer at `~/.job-search/profile.yaml`.

**After setup, you can:**
- `/job-search find` — search the internet for jobs matching your profile, scored and ranked
- `/job-search score` — paste a job posting URL and get a detailed fit breakdown
- `/job-search pipeline` — view and manage your tracked opportunities
- `/job-search update` — edit your profile (new skills, change target roles, etc.)

**Example results:**
```
| # | Score | Company    | Role              | Location | Key Match          | Key Gap       |
|---|-------|------------|-------------------|----------|--------------------|---------------|
| 1 | 92%   | Anthropic  | Solutions Engineer| SF       | AI systems, Python | Startup exp   |
| 2 | 87%   | Databricks | Field Engineer    | Remote   | Data + enablement  | Spark depth   |
| 3 | 78%   | Stripe     | Technical PM      | SF       | Cross-functional   | Payments exp  |
```

---

## Option B: Claude.ai (simpler setup, no install needed)

If you don't want to install anything, you can use Claude directly at https://claude.ai. The web version can't save your profile or search the internet for you, but it can still score jobs and help with prep.

### Step 1: Go to claude.ai and log in (or create a free account)

### Step 2: Start a new conversation and paste this prompt:

```
You are my job search assistant. I'm going to paste my resume below,
then I'll paste job postings for you to evaluate.

For each job posting, score it against my resume on these dimensions
(weighted average, 0-100):
- Title match (20%) — how close to my experience level and function?
- Skills match (25%) — what % of required skills do I have?
- Experience level (15%) — am I in the sweet spot, over, or under?
- Domain/industry (15%) — is this my industry or adjacent?
- Location (10%) — does it match my constraints?
- Differentiator (15%) — does this role benefit from what makes me unique?

Give me: overall score, verdict (STRONG FIT / WORTH APPLYING / STRETCH / PASS),
top 3 strengths for this role, top 3 gaps to address.

Be honest. Don't inflate scores.

Here is my resume:
[PASTE YOUR RESUME HERE]
```

### Step 3: Paste job postings

Each time you find a job posting, paste the URL or text into the conversation and Claude will score it against your resume.

---

## Tips

- **Set up your profile first.** The tool gets better the more it knows about you. Spend 5 minutes on the initial setup — it's worth it.
- **Run `/job-search find` weekly.** New jobs get posted constantly. Make it a habit.
- **Score before you apply.** Don't waste time on <65% matches. Discipline > volume.
- **Use it between JSC meetings.** Run a search, bring the top results to the group, discuss which ones are worth pursuing.
- **Your profile stays on YOUR computer.** Nothing is uploaded or shared. The file is at `~/.job-search/profile.yaml` — you can read it, edit it, or delete it anytime.
- **Option A remembers you across sessions.** Option B (claude.ai) starts fresh each time — you'll need to re-paste your resume.

---

## Questions?

Ask Mical in our next JSC meeting or message in our group channel.
