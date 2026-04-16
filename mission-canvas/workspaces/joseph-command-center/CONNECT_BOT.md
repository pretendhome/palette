# Connect Joseph Palette Bot — Direct Setup

No GitHub push needed. The bot connects directly to Telegram from your laptop.

## Prerequisites

Make sure you have:
- Node.js installed
- Python 3 installed
- The palette repo cloned locally

## Step 1: Install dependencies

```bash
cd palette/mission-canvas
npm install
pip install httpx
```

## Step 2: Start the MissionCanvas server

```bash
cd palette/mission-canvas
node server.mjs &
```

You should see: `MissionCanvas server running at http://localhost:8787`

## Step 3: Start the Telegram bot

In the same `palette/mission-canvas` directory:

```bash
export JOSEPH_BOT_TOKEN="8748740444:AAHgW3EoRnmTDqNhZ62RYeIOxL-IYcLh4mI"
export MC_WORKSPACE="joseph-command-center"
export MC_SERVER="http://localhost:8787"
python3 joseph_bridge.py
```

You should see the bot start polling.

## Step 4: Open Telegram

Search for `@joseph_palette_bot` and send `/start`.

## Commands

- `/start` — welcome and command list
- `/brief` — daily brief (priorities, blockers, nudges)
- `/gaps` — missing evidence
- `/decisions` — open decisions
- `/health` — health score
- `/research` — research a question with Perplexity
- `/help` — full command list

Any other message gets routed through the workspace. Voice messages are transcribed automatically.

## Stopping

To stop everything:

```bash
pkill -f joseph_bridge.py
pkill -f "node server.mjs"
```

## Troubleshooting

- **"push to GitHub"** — you do NOT need to push anything. The bot connects directly to Telegram via polling. No VPS, no deploy.
- **Bot not responding** — make sure both `server.mjs` AND `joseph_bridge.py` are running. The bridge needs the server.
- **Port 8787 in use** — kill the old process: `lsof -i :8787 -t | xargs kill`
- **Missing httpx** — `pip install httpx`
