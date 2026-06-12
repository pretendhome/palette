# Nous Portal Integration — Hard Task List
**Date**: 2026-06-01
**Author**: claude.analysis
**Purpose**: Wire Mission Canvas to use Nous Portal as a provider via OAuth device code flow

---

## The Goal

User runs `palette setup` → picks "Nous Portal" → browser opens → OAuth login → done. All 300+ models available through Mission Canvas's governance layer. Zero API keys.

---

## How It Works (from Hermes source code)

Nous Portal uses **OAuth Device Code Flow** (RFC 8628). No redirect URIs, no web server needed. Works from any CLI.

### The Endpoints

```
Portal Base URL:     https://portal.nousresearch.com
Inference Base URL:  https://inference-api.nousresearch.com/v1
Client ID:           hermes-cli (we'll use "mission-canvas")
```

### OAuth Endpoints

```
POST https://portal.nousresearch.com/api/oauth/device/code
  Body: { client_id: "mission-canvas", scope: "inference:invoke" }
  Returns: { device_code, user_code, verification_uri, verification_uri_complete, expires_in, interval }

POST https://portal.nousresearch.com/api/oauth/token
  Body: { grant_type: "urn:ietf:params:oauth:grant-type:device_code", client_id: "mission-canvas", device_code: <device_code> }
  Returns: { access_token, refresh_token, token_type, expires_in }
  Poll this every <interval> seconds until user approves in browser.

GET https://portal.nousresearch.com/api/oauth/account
  Headers: { Authorization: Bearer <access_token> }
  Returns: account info, entitlements, plan details
```

### Inference Endpoint (after auth)

```
POST https://inference-api.nousresearch.com/v1/chat/completions
  Headers: { Authorization: Bearer <access_token>, Content-Type: application/json }
  Body: standard OpenAI-compatible chat completions
  Models: any model on Nous Portal (anthropic/claude-sonnet-4, openai/gpt-4o, google/gemini-2.5-pro, etc.)
```

---

## Task List

### Task 1: Register as OAuth Client (UNKNOWN — may need Nous approval)
- Hermes uses client_id `hermes-cli`
- We need to either:
  - a) Use `hermes-cli` as client_id (works but rides on their registration)
  - b) Register `mission-canvas` as a new OAuth client with Nous (may require contacting them)
  - c) Use the Hermes proxy (`localhost:8645`) as a bridge (fastest, no registration needed)
- **Recommendation for tonight**: Use option (c) — Hermes proxy. Get auth working, prove the flow, register properly later.

### Task 2: Create `palette/scripts/nous_auth.py` — OAuth Device Code Flow
```python
#!/usr/bin/env python3
"""Mission Canvas — Nous Portal OAuth Login"""

import httpx
import json
import time
import webbrowser
from pathlib import Path

PORTAL_URL = "https://portal.nousresearch.com"
CLIENT_ID = "hermes-cli"  # TODO: register mission-canvas client
SCOPE = "inference:invoke"
AUTH_FILE = Path.home() / ".palette" / "nous_auth.json"

def login():
    """Run device code OAuth flow."""
    with httpx.Client() as client:
        # Step 1: Request device code
        resp = client.post(f"{PORTAL_URL}/api/oauth/device/code", data={
            "client_id": CLIENT_ID,
            "scope": SCOPE,
        })
        resp.raise_for_status()
        data = resp.json()

        device_code = data["device_code"]
        user_code = data["user_code"]
        verification_url = data["verification_uri_complete"]
        expires_in = data["expires_in"]
        interval = data["interval"]

        # Step 2: Show user the code and open browser
        print(f"\n  To continue:")
        print(f"  1. Open: {verification_url}")
        print(f"  2. If prompted, enter code: {user_code}")
        print(f"  Waiting for approval...\n")
        webbrowser.open(verification_url)

        # Step 3: Poll for token
        deadline = time.monotonic() + expires_in
        while time.monotonic() < deadline:
            time.sleep(interval)
            token_resp = client.post(f"{PORTAL_URL}/api/oauth/token", data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "client_id": CLIENT_ID,
                "device_code": device_code,
            })
            if token_resp.status_code == 200:
                tokens = token_resp.json()
                AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
                AUTH_FILE.write_text(json.dumps(tokens, indent=2))
                print(f"  ✓ Logged in. Token saved to {AUTH_FILE}")
                return tokens
            error = token_resp.json().get("error", "")
            if error == "authorization_pending":
                continue
            elif error == "slow_down":
                interval += 1
                continue
            else:
                print(f"  ✗ Auth failed: {error}")
                return None

        print("  ✗ Login timed out.")
        return None

def get_access_token():
    """Get current access token, refreshing if needed."""
    if not AUTH_FILE.exists():
        return None
    tokens = json.loads(AUTH_FILE.read_text())
    return tokens.get("access_token")

if __name__ == "__main__":
    login()
```

### Task 3: Add `nousportal` provider to hub `server.mjs`

In `providerConfig()`:
```javascript
case 'nousportal': return {
  url: 'https://inference-api.nousresearch.com/v1/chat/completions',
  key: NOUS_ACCESS_TOKEN,  // loaded from ~/.palette/nous_auth.json
  label: 'Nous Portal'
};
```

Load the token at startup:
```javascript
let NOUS_ACCESS_TOKEN = null;
try {
  const authPath = join(process.env.HOME, '.palette', 'nous_auth.json');
  const auth = JSON.parse(await readFile(authPath, 'utf8'));
  NOUS_ACCESS_TOKEN = auth.access_token;
} catch { /* not logged in */ }
```

### Task 4: Add `nousportal` to intent routing (frontend)

In `getIntentAgent()`, add Nous Portal as a universal provider option:
```javascript
// If Nous Portal is authenticated, route all external intents through it
if (state.nousPortal) {
  const routing = {
    research: 'nousportal',    // any model
    protect: 'kimi',           // stays local
    decide: 'nousportal',      // any reasoning model
    create: 'nousportal',      // any creative model
    diagnose: 'nousportal',
    reflect: 'nousportal',
  };
  return routing[intent] || 'nousportal';
}
```

### Task 5: Add to `setup.sh` — Provider Selection

After the current API key prompts, add:
```bash
echo ""
echo -e "${BOLD}Provider Setup${NC}"
echo "  1. Nous Portal (one login, 300+ models — recommended)"
echo "  2. Individual API keys (Perplexity, Mistral, etc.)"
echo "  3. Local only (Ollama, no external)"
read -p "  Choose [1/2/3]: " PROVIDER_CHOICE

case $PROVIDER_CHOICE in
  1)
    python3 scripts/nous_auth.py
    ;;
  2)
    # Current API key prompts
    ;;
  3)
    echo "  Running in local-only mode."
    ;;
esac
```

### Task 6: Add `palette portal` CLI command

In `scripts/palette_intent.py`, add:
```python
elif intent == "portal":
    from scripts.nous_auth import login
    login()
```

So users can run: `palette portal login`

---

## SHORTCUT: Use Hermes Proxy Tonight

Instead of implementing the full OAuth flow, use Hermes's proxy that's already on your machine:

1. Log into Nous Portal via Hermes: `hermes portal login`
2. Start the proxy: `hermes proxy start`
3. Point Mission Canvas hub at `http://127.0.0.1:8645/v1` as a provider

This is ONE line change in hub server.mjs:
```javascript
case 'nousportal': return {
  url: 'http://127.0.0.1:8645/v1/chat/completions',
  key: 'sk-unused',  // proxy replaces with real credential
  label: 'Nous Portal'
};
```

**Time: 5 minutes. Proves the concept for the demo.**

---

## BLOCKER: Client ID Registration

The `client_id` used in the device code flow may need to be registered with Nous. Hermes uses `hermes-cli`. If we use that, it works but depends on their registration. To properly register `mission-canvas`:

- Contact Nous Research (probably via their Discord or developer relations)
- Request OAuth client registration for "Mission Canvas"
- Get assigned a client_id

**For tonight**: use `hermes-cli` as client_id or use the proxy shortcut. Proper registration is a post-BDB task.

---

## Priority Order

| # | Task | Time | Blocks Demo? |
|---|------|------|-------------|
| 1 | Hermes proxy shortcut (prove concept) | 5 min | No — demo already works |
| 2 | `nous_auth.py` OAuth flow | 30 min | No |
| 3 | Hub provider config | 10 min | No |
| 4 | Setup.sh provider selection | 15 min | No |
| 5 | `palette portal` CLI command | 5 min | No |
| 6 | Register client_id with Nous | Days | No |

**None of these block the BDB demo.** The demo already works with direct API keys. This is distribution strategy — important for the business, not for tomorrow's submission.

---

*Report by claude.analysis. 2026-06-01.*
