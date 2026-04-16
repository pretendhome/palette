# Connect Joseph Palette Bot

The bot is already running on the VPS. Joseph just needs to open Telegram.

## Quickest Path (bot is live now)

1. Open Telegram
2. Search for `@joseph_palette_bot`
3. Send `/start`
4. That's it — the bot is connected and running on the VPS

## Commands

- `/start` — welcome and command list
- `/brief` — morning brief (futures, pre-market, oil, gold, macro)
- `/midday` — mid-day pulse (index movers, breaking news, BTC)
- `/close` — session close (volume, earnings, SMA levels)
- `/gaps` — missing evidence
- `/decisions` — open decisions
- `/health` — health score
- `/research <question>` — research anything with Perplexity
- `/help` — full command list

Any other message gets routed through the workspace. Voice messages are transcribed automatically.

## Scheduled Briefs (automated delivery)

| Time (PST) | Brief | Content |
|---|---|---|
| 6:00 AM | Morning | Futures, pre-market, earnings, Oil/Gold/USD-JPY/10Y/BTC, Fed, Trump, geo, macro |
| 12:00 PM | Mid-day | Index pulse, movers, breaking news, BTC |
| 1:30 PM | Close | Session close, volume, earnings after bell, SMA levels |

These are delivered automatically when the monitor daemon is running.

## If the Bot Stops Responding

Ask Laith to restart it. He runs this from his terminal:

```bash
ssh root@srv1390882.hstgr.cloud "bash /tmp/start_joseph.sh"
```

Or if Laith is not available, SSH to the VPS yourself:

```bash
ssh root@srv1390882.hstgr.cloud
cd /root/fde/palette/mission-canvas
source /root/fde/venv/bin/activate

# Kill old processes
pkill -f joseph_bridge.py
pkill -f "node server.mjs"
sleep 2

# Start server
export PERPLEXITY_API_KEY="<ask Laith for the key>"
nohup node server.mjs > /tmp/mc-server.log 2>&1 &
sleep 3

# Start bot
export JOSEPH_BOT_TOKEN="8748740444:AAHgW3EoRnmTDqNhZ62RYeIOxL-IYcLh4mI"
export MC_WORKSPACE="joseph-command-center"
export MC_SERVER="http://localhost:8787"
nohup python3 joseph_bridge.py > /tmp/joseph-bot.log 2>&1 &
sleep 3

# Verify
tail -3 /tmp/joseph-bot.log
```

You should see: `[mc-bot] starting` and `[mc-bot] server health: ok`

## Running Locally Instead (optional)

If you want to run the bot from your own laptop instead of the VPS:

```bash
cd palette/mission-canvas
npm install
pip install httpx

node server.mjs &

export JOSEPH_BOT_TOKEN="8748740444:AAHgW3EoRnmTDqNhZ62RYeIOxL-IYcLh4mI"
export MC_WORKSPACE="joseph-command-center"
export MC_SERVER="http://localhost:8787"
python3 joseph_bridge.py
```

Note: scheduled briefs won't fire if your laptop is asleep. Use the VPS for 24/7 delivery.
