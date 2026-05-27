# Skill: Bot Creation — Telegram Intelligence Bot
## Version: 1.0 | Validated: joseph-palette-bot v2 (May 2026)

---

## When to Use

Use this skill when building a new Telegram bot that:
- Monitors a domain (markets, competitors, industry trends)
- Delivers phone-optimized intelligence briefs
- Supports live research via Perplexity
- Tracks theses/hypotheses with evidence signals
- Needs inline keyboard buttons for tap-to-act UX
- Runs on a VPS as a single systemd service

This skill was validated building the joseph-palette investment bot. The pattern generalizes to any domain: competitive intelligence, job market tracking, real estate, crypto, sports analytics, etc.

---

## The Architecture (One File, One Service)

```
SINGLE PYTHON PROCESS
├── Telegram polling loop
│   ├── Command handlers (/brief, /research, /help, etc.)
│   ├── Callback handler (inline button taps)
│   └── Monitor scheduler (checks between poll cycles)
├── SQLite DB (state that changes)
│   ├── signals (timestamp, thesis_id, content, source)
│   ├── research_log (query, result, thesis_id, date)
│   ├── user_interests (thesis_id, tap_count, last_accessed)
│   └── brief_state (last_shown, staleness tracking)
├── Static YAML (definitions that rarely change)
│   ├── theses.yaml (the framework — hypotheses to track)
│   ├── monitors/*.yaml (search definitions + schedules)
│   └── config.yaml (flat, single-user)
└── Perplexity API (the only external dependency)
```

### What NOT to build
- No web server (Telegram IS the UI)
- No separate monitor daemon (runs inside the poll loop)
- No MCP server (unless the user needs Claude Desktop integration)
- No workspace abstraction (single-user bots don't need it)
- No resolver service (regex routing handles 90% of cases)

---

## Step-by-Step Build Process

### Step 1: Define the Domain Theses (30 min)

Before writing code, define what the bot tracks. These are structured hypotheses with:

```yaml
theses:
  - id: THESIS-UNIQUE-ID
    name: "Human-readable name"
    thesis: "One paragraph explaining the hypothesis"
    direction: bullish | bearish | disruptive | structural_shift
    timeframe: "6-12 months"
    confidence: very_high | high | medium-high | medium

    evidence:
      - session: "source"
        speaker: "who said it"
        quote: "what they said"

    exposed_companies:
      - name: "Company Name"
        ticker: "TICK"
        risk: "one sentence risk description"

    beneficiaries:
      - name: "Company Name"
        ticker: "TICK"
        why: "one sentence why they win"

    watchlist_triggers:
      - "Specific event that would validate/invalidate this thesis"

    morning_brief: "2-sentence summary for phone screen"
```

This YAML is the brain of the bot. Everything else is plumbing.

### Step 2: Create the Bot Token (5 min)

1. Message @BotFather on Telegram
2. `/newbot` → name it → get the token
3. `/mybots` → select bot → Bot Settings → Group Privacy → OFF (if using in groups)
4. Store token as `BOT_TOKEN` env var

### Step 3: Build the Single-File Bot (template below)

The bot file has these sections in order:

```python
# 1. CONFIG — env vars, paths, constants
# 2. SQLITE — init_db() with all tables
# 3. TELEGRAM — tg(), send(), typing(), answer_callback()
# 4. PERPLEXITY + NARRATOR — research with condensation filter
# 5. THESES — load, search, deep-dive, vulnerable, beneficiaries
# 6. MORNING BRIEF — diff-based, phone-optimized, with buttons
# 7. DOMAIN-SPECIFIC COMMANDS — /stress, /intel, etc.
# 8. MONITORS — scheduler that runs between poll cycles
# 9. COMMAND HANDLERS — handle_message() routing
# 10. CALLBACK HANDLERS — handle_callback() for button taps
# 11. HELP — button grid
# 12. MAIN LOOP — poll + monitor check
```

### Step 4: Create Monitors (10 min each)

Each monitor is a YAML file:

```yaml
monitor:
  id: unique-id
  name: "Human Name"
  enabled: true
  schedule_minutes: 720  # how often to check

  search_queries:
    - "perplexity search query 1"
    - "perplexity search query 2"

  system_prompt: |
    You are a [domain] analyst. ONLY report events that...
    If NOTHING meets the bar, respond with: NO_TRIGGER

  notify_channels:
    - telegram

  last_run: null
  total_alerts: 0
```

The `NO_TRIGGER` pattern is critical: most runs should return nothing. Only fire on genuinely significant events. Set the bar HIGH — users will mute a noisy bot.

### Step 5: Deploy to VPS (15 min)

```bash
# Upload files
scp bot.py root@vps:/path/to/bot/
scp theses.yaml root@vps:/path/to/data/
scp monitors/*.yaml root@vps:/path/to/data/monitors/

# Create env file
cat > /path/to/bot/bot.env << 'EOF'
BOT_TOKEN=your-telegram-token
PERPLEXITY_API_KEY=pplx-xxx
TELEGRAM_CHAT_ID=your-chat-id
EOF

# Create systemd service
cat > /etc/systemd/system/mybot.service << 'EOF'
[Unit]
Description=My Intelligence Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/bot
ExecStart=/path/to/venv/bin/python3 bot.py
Restart=always
RestartSec=5
EnvironmentFile=/path/to/bot/bot.env

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable mybot
systemctl start mybot
```

### Step 6: Test Every Command

SSH in and verify:
```bash
journalctl -u mybot --no-pager -n 10  # check logs
# Then send /help on Telegram — verify button grid
# Tap each button — verify response
# Send /brief — verify morning brief
# Send /research <query> — verify Perplexity
```

---

## Key Patterns (Validated)

### Pattern 1: Inline Keyboard Buttons
```python
def send(chat_id, text, buttons=None):
    kwargs = {"chat_id": chat_id, "text": text[:4000], "parse_mode": "Markdown"}
    if buttons:
        kwargs["reply_markup"] = {"inline_keyboard": buttons}
    result = tg("sendMessage", **kwargs)
    if not result.get("ok"):
        # Markdown failed — retry without
        kwargs.pop("parse_mode")
        tg("sendMessage", **kwargs)
```

Always fall back to no-markdown on error. Telegram's Markdown parser rejects unbalanced asterisks/underscores.

### Pattern 2: Callback Data Format
```
cb:type:payload
```
- `cb:research:r42` → look up stored research query r42, run Perplexity
- `cb:run:brief` → run the /brief command
- `cb:run:thesis_DISRUPT-CLOUD-PEAK` → deep-dive a thesis
- `cb:cmd:stress` → run /stress

### Pattern 3: NO_TRIGGER for High-Bar Monitors
The system prompt tells Perplexity to respond with `NO_TRIGGER` if nothing meets the bar. The monitor daemon checks for this string and skips alert creation. Most runs produce nothing — that's correct.

### Pattern 4: Narrator Filter for Phone
Raw Perplexity output is too verbose. Pass it through a second call:
```python
system = "Condense for phone. 3 bullets max. Keep numbers. Cut filler."
```
Falls back to sentence truncation if the second call fails. Make this optional (condense=True for briefs, False for explicit /research).

### Pattern 5: Diff-Based Briefs
Track what was shown when (SQLite or YAML state). Only show NEW information. If nothing changed: "No new signals since yesterday" + one rotating thesis. Prevents staleness and saves API calls.

### Pattern 6: User Interest Tracking
```sql
INSERT INTO user_interests (thesis_id, tap_count, last_accessed)
VALUES (?, 1, ?)
ON CONFLICT(thesis_id) DO UPDATE SET tap_count = tap_count + 1, last_accessed = ?
```
Weight the morning brief toward what the user taps most. Simple frequency counter, no ML.

### Pattern 7: Path Resolution on VPS
If the bot runs via symlink or from a different working directory, `Path(__file__).parent.parent` breaks. Use a helper:
```python
def _find_data_dir():
    candidates = [
        Path(__file__).parent / "data",
        Path("/root/fde/bot-data"),
        Path(__file__).resolve().parent / "data",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]
```

---

## Checklist: Before Shipping

- [ ] Bot token set in env
- [ ] Perplexity API key set in env
- [ ] Telegram chat ID set (for monitor push notifications)
- [ ] All theses YAML loads without error
- [ ] All monitors have `NO_TRIGGER` in system prompt
- [ ] SQLite DB initializes cleanly
- [ ] `/help` shows button grid
- [ ] Every button in grid has a handler in handle_callback()
- [ ] `/brief` returns content (not "engine not found")
- [ ] `/research <query>` returns Perplexity results
- [ ] Markdown fallback works (send with unbalanced asterisks)
- [ ] Monitor scheduler runs between poll cycles
- [ ] systemd service restarts on crash (Restart=always)
- [ ] VPS env file is NOT in git (.gitignore)
- [ ] Archive of previous version saved before deploying

---

## Files Reference (joseph-palette-bot v2)

```
palette/buy-vs-build/tech/
├── disruption_theses.yaml        — 12 theses, ~750 lines
├── tech_engine.py                — v1.1, PIS + disruption queries
├── morning_brief.py              — phone-optimized brief engine
├── TECH_INVESTMENT_REPORT_2026-05.md   — full report (markdown)
├── TECH_INVESTMENT_REPORT_2026-05.html — print-optimized
├── TECH_INVESTMENT_REPORT_2026-05.pdf  — 10-page PDF
└── Tech-Investment-Report-2026-05.docx — Word document

palette/mission-canvas/
├── joseph_bot_v2.py              — the v2 bot (~700 lines)
├── joseph_bridge.py              — v1 bridge (kept for reference)
├── monitor_daemon.py             — v1 daemon (superseded by v2)
├── market_stress.py              — market stress model (used by v2)
└── joseph_data/
    ├── joseph.db                 — SQLite state
    └── monitors/
        ├── energy-markets.yaml   — every 2h
        ├── ai-investments.yaml   — every 6h
        ├── market-stress.yaml    — every 12h
        └── tech-disruption.yaml  — every 12h (high bar)

VPS: srv1390882.hstgr.cloud
├── /root/fde/missioncanvas-site/joseph_bot_v2.py
├── /root/fde/buy-vs-build/tech/  (theses, engines)
├── /root/fde/buy-vs-build/intel/ (financial voices)
├── /root/fde/palette/mission-canvas/joseph_data/ (SQLite + monitors)
└── /root/fde/archive/joseph-v1-2026-05-16/ (v1 backup)

Service: joseph-bot-v2.service
Revert: systemctl stop joseph-bot-v2 && systemctl start joseph-bridge mc-monitors
```

---

## Adapting to a New Domain

To create a bot for a different domain (e.g., real estate, crypto, job market):

1. **Replace `disruption_theses.yaml`** with domain-specific hypotheses
2. **Replace monitors** with domain-specific search queries + system prompts
3. **Replace `/intel`** with domain-specific voice/source library (or remove)
4. **Replace `/stress`** with domain-specific risk model (or remove)
5. **Keep everything else** — the Telegram plumbing, SQLite state, button grid, narrator filter, research routing, monitor scheduler all generalize

The bot template is ~700 lines. About 400 are reusable across any domain. The other 300 are domain-specific commands and data loading.

---

*Skill created from joseph-palette-bot v2 build session (May 16-17, 2026). Validated in production on VPS with live Telegram users.*
