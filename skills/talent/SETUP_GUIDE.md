# Job Search Assistant — Setup Guide

A free AI-powered job search co-pilot that follows the Never Search Alone methodology. It helps you work through each phase — from self-discovery through negotiation — one step at a time.

---

## What you need

- A computer (Mac, Windows, or Linux)
- A Claude account (free at claude.ai, or a paid plan)

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

### Step 3: Create the job search command

Create a folder for the command file:

```bash
mkdir -p ~/.claude/commands
```

Then create the command file. Copy the file I'll send you (`job-search.md`) into that folder:

```bash
# Mac/Linux
cp job-search.md ~/.claude/commands/job-search.md

# Windows (PowerShell)
Copy-Item job-search.md -Destination "$env:USERPROFILE\.claude\commands\job-search.md"
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

Then just start talking. Tell it where you are in your search. It will figure out the right next step.

**Examples of what to say:**
- "I just got laid off and I don't know where to start"
- "I haven't done my Mnookin Two-Pager yet — can you walk me through it?"
- "I've done 8 listening tour conversations — here's what I'm hearing..."
- "Here's my CMF statement — can you help me sharpen it?"
- "I have an interview at [company] next week — help me prep"
- "I got an offer — help me think through negotiation"

---

## Option B: Claude.ai (simpler setup, no install needed)

If you don't want to install anything, you can use Claude directly at https://claude.ai and paste the methodology as context.

### Step 1: Go to claude.ai and log in (or create a free account)

### Step 2: Start a new conversation and paste this prompt:

```
You are my job search co-pilot. Follow the Never Search Alone (NSA)
methodology by Phyl Terry. Help me work through these phases in order:

1. Self-Discovery (Mnookin Two-Pager, Gratitude House)
2. Listening Tour (15 conversations, pattern extraction)
3. Candidate-Market Fit — a clear, narrow statement of who I am for the market
4. Resume & LinkedIn Rehab — every word supports my CMF
5. Strategic Networking — Boss the Process (write my own job description, show it to hiring managers)
6. Interviewing — prep, practice, debrief after each one
7. Negotiation — Four Legs: compensation, budget, resources, support

Key rules:
- Don't let me skip ahead. Phases 1-3 are what make 5-7 work.
- Be honest. If my CMF is too vague, say so.
- Never fabricate claims or inflate numbers on my behalf.
- Narrow CMF = more opportunities, not fewer.
- Slow down to go faster.

I'm ready to start. Ask me where I am in my search.
```

### Step 3: Start talking

Same as above — tell it where you are and it will guide you.

---

## Tips

- **Be honest with it.** The more real you are about where you're stuck, the better it can help. It's not judging you.
- **Use it between JSC meetings.** Do the exercises (Two-Pager, Listening Tour planning, CMF drafting) with Claude, then bring the output to the group for feedback.
- **It remembers within a conversation** but starts fresh each time. If you're working on something over multiple sessions, paste in your Two-Pager or CMF draft at the start so it has context.
- **It won't replace the JSC.** The group gives you peer accountability and perspectives that AI cannot. Use Claude for the exercises and prep work. Use the group for honesty and support.

---

## Questions?

Ask Mical in our next JSC meeting or message in our group channel.
