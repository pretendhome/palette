# Raptor — Palette Debug Agent (Velociraptor v1.0)

Auto-recursive connectivity debugger for containerized AI services.

## What it does

Raptor implements the Palette velociraptor archetype as a compiled Go CLI.
It runs a self-deepening probe chain: each failed layer triggers a more specific
probe, terminating at the root cause. No guessing, no logs to read manually.

## The Problem It Was Built For

OpenClaw (Hostinger) forces its gateway to bind `ws://127.0.0.1:18789` inside
the Docker container. Docker port mapping physically cannot forward to a
container's loopback interface — it uses the bridge network. This makes
the gateway unreachable from outside, causing MissionCanvas to return
`"source": "local_fallback"` indefinitely.

**Fix**: `nsenter` enters the container's network namespace from the host,
runs `socat` there bound to `0.0.0.0:19000`, and the bridge network can
then reach port 19000. The SSH tunnel then targets the bridge IP:19000.

## Build

```bash
# Install Go if needed:
curl -fsSL https://go.dev/dl/go1.22.5.linux-amd64.tar.gz | tar -C ~/go-sdk -xz

# Build:
cd /home/mical/fde/raptor
~/go-sdk/go/bin/go build -o raptor .
```

## Usage

```bash
# Run full probe chain (non-destructive):
./raptor diagnose

# Print VPS commands for the fix:
./raptor runbook

# Apply fix (run on VPS as root):
./raptor fix

# Preview fix commands without running them:
./raptor fix --dry-run

# Verify end-to-end after fix:
./raptor verify

# Generate Palette decisions.md entry:
./raptor report
```

## The Fix Runbook (Manual)

Run these commands **on the VPS** (`ssh root@72.60.171.27`):

```bash
# Step 1: Get container PID
CPID=$(docker inspect --format '{{.State.Pid}}' openclaw-fcup-openclaw-1)
echo "PID: $CPID"

# Step 2: Create socat bridge in container's network namespace
#         socat binds to 0.0.0.0:19000 — reachable via Docker bridge
#         and forwards to the container's loopback:18789
nsenter --net=/proc/$CPID/ns/net -- \
  socat TCP-LISTEN:19000,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:18789 &

# Step 3: Get container bridge IP
CNET=$(docker inspect --format \
  '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' openclaw-fcup-openclaw-1)
echo "Bridge IP: $CNET"

# Step 4: Verify from VPS host
curl -s http://$CNET:19000/v1/models
```

Then on **local machine** — update the SSH tunnel (use $CNET from above):

```bash
# Kill old tunnel if running
pkill -f "18889.*18789"

# New tunnel targets bridge IP:19000 (not VPS loopback)
ssh -N -L 18889:<CNET>:19000 root@72.60.171.27 &

# Verify
curl -s http://127.0.0.1:18889/v1/models
```

`.env.production` stays the same: `OPENCLAW_BASE_URL=http://127.0.0.1:18889/`

## Why the Previous Tunnel Returned Empty Reply

The old tunnel was:
```
ssh -N -L 18889:127.0.0.1:18789 root@72.60.171.27
```
This forwarded local:18889 → VPS:127.0.0.1:18789. On the VPS, Docker's
userland proxy listens there and attempts to connect to the container via the
bridge network. But the container's service is on its own loopback, not on
the bridge — so the docker-proxy accepted the TCP connection and immediately
closed it. Hence: "empty reply from server" (curl 52).

## Persistence

The socat bridge dies when the container restarts. For persistence, add to VPS:

```bash
# /etc/systemd/system/openclaw-bridge.service
[Unit]
Description=OpenClaw loopback bridge
After=docker.service
Requires=docker.service

[Service]
Type=simple
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  CPID=$(docker inspect --format "{{.State.Pid}}" openclaw-fcup-openclaw-1); \
  exec nsenter --net=/proc/$CPID/ns/net -- \
    socat TCP-LISTEN:19000,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:18789'
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Palette Alignment

- Agent: Velociraptor / Raptor
- Tier: 1 (UNVALIDATED)
- Role: Isolate failure, diagnose root cause, propose minimal fix
- Constraint: Does not add features or expand scope
- Output: decisions.md log entry via `raptor report`
