package main

import (
	"fmt"
	"strings"
)

func icon(s ProbeStatus) string {
	if s == ProbePass {
		return "✓"
	}
	return "✗"
}

func printDiagnosis(d Diagnosis) {
	fmt.Println()
	fmt.Println("🔍 PROBE CHAIN")
	fmt.Println("  auto-recursive — deepest failure = root cause")
	fmt.Println("  ─────────────────────────────────────────────────────────────")
	for i, r := range d.Results {
		marker := ""
		if r.RootCause {
			marker = "  ← ROOT CAUSE"
		}
		fmt.Printf("  %d. [%s] %-30s %s%s\n", i+1, icon(r.Status), r.Name, r.Detail, marker)
	}
	fmt.Println()
	fmt.Printf("🔬 DIAGNOSIS:  %s\n", d.RootCause)
	if d.FixMode != "" {
		fmt.Printf("   Fix mode:    %s\n", d.FixMode)
	}
	if d.FixReady {
		fmt.Printf("   Auto-fix:    available\n")
	}
	fmt.Println()
}

func printFixResult(fr FixResult, cfg Config) {
	if !fr.Applied {
		fmt.Printf("✗ FIX NOT APPLIED\n  %s\n\n", fr.Err)
		return
	}
	fmt.Printf("✓ BRIDGE ACTIVE\n")
	fmt.Printf("  Bridge IP:  %s\n", fr.BridgeIP)
	fmt.Printf("  Bridge URL: %s\n", fr.BridgeURL)
	if fr.BridgePID != "" {
		fmt.Printf("  Bridge PID: %s  (ephemeral — see 'debugger persist')\n", fr.BridgePID)
	}
	fmt.Println()
	fmt.Println("📋 NEXT STEPS:")
	fmt.Printf("  1. SSH tunnel:   ssh -N -f -L %d:%s:%d %s\n",
		cfg.TunnelPort, fr.BridgeIP, cfg.BridgePort, cfg.Remote)
	fmt.Printf("     or run:       debugger tunnel --remote %s --bridge-ip %s\n", cfg.Remote, fr.BridgeIP)
	fmt.Printf("  2. Verify:       debugger verify\n")
	fmt.Printf("  3. Persist:      debugger persist --remote %s\n\n", cfg.Remote)
	fmt.Println("⚠️  Bridge is ephemeral — dies on container restart.")
	fmt.Println("   'debugger persist' installs a systemd unit that recreates it automatically.")
	fmt.Println()
}

func printTunnelResult(tr TunnelResult) {
	if !tr.Active {
		fmt.Printf("✗ TUNNEL FAILED\n  %s\n\n", tr.Err)
		return
	}
	fmt.Printf("✓ TUNNEL ACTIVE\n")
	fmt.Printf("  localhost:%d → %s:%d\n\n", tr.LocalPort, tr.BridgeIP, tr.BridgePort)
}

func printRunbook(cfg Config) {
	remoteIP := cfg.RemoteIP
	if remoteIP == "" && strings.Contains(cfg.Remote, "@") {
		remoteIP = strings.SplitN(cfg.Remote, "@", 2)[1]
	}
	if remoteIP == "" {
		remoteIP = "<VPS_IP>"
	}
	payload := strings.ReplaceAll(string(probePayload(cfg)), "'", `'"'"'`)
	routePayload := strings.ReplaceAll(cfg.RoutePayload, "'", `'"'"'`)

	fmt.Printf(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DEBUGGER RUNBOOK (manual steps)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

── ON VPS: ssh root@%s ──────────────────────────

# 1. Install socat:
apt-get install -y socat

# 2. Get container PID (must be non-zero):
CPID=$(docker inspect --format '{{.State.Pid}}' %s)
echo "PID=$CPID"

# 3. Create socat bridge in container's network namespace:
#    Binds to 0.0.0.0:%d inside container netns → Docker bridge can reach it.
#    Forwards to the service's loopback-only port.
nohup nsenter --net=/proc/$CPID/ns/net -- \
  socat TCP-LISTEN:%d,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:%d \
  > /tmp/debugger-bridge.log 2>&1 &
echo "Bridge PID: $!"

# 4. Get container bridge IP:
CNET=$(docker inspect --format \
  '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' %s)
echo "Bridge IP=$CNET"

# 5. Verify bridge (expect any JSON response):
curl -s -o /dev/null -w '%%{http_code}' \
  -X POST http://$CNET:%d%s \
  -H 'Content-Type: application/json' \
  -d '%s'

── ON LOCAL MACHINE ──────────────────────────────

# 6. Kill old tunnel, start new one (use CNET value from step 4):
fuser -k %d/tcp
ssh -N -f -L %d:<CNET>:%d root@%s

# 7. Verify tunnel:
curl -s -X POST http://127.0.0.1:%d%s \
  -H 'Content-Type: application/json' \
  -d '%s'

# 8. Test full stack (look for "source" != "local_fallback"):
curl -sS -X POST %s%s \
  -H 'Content-Type: application/json' \
  -d '%s'

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AUTOMATION: debugger fix --remote root@%s
 PERSISTENCE: debugger persist --remote root@%s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`,
		remoteIP,
		cfg.Container,
		cfg.BridgePort, cfg.BridgePort, cfg.ServicePort,
		cfg.Container,
		cfg.BridgePort, cfg.APIPath, payload,
		cfg.TunnelPort,
		cfg.TunnelPort, cfg.BridgePort, remoteIP,
		cfg.TunnelPort, cfg.APIPath, payload,
		strings.TrimRight(cfg.AdapterURL, "/"), cfg.RoutePath, routePayload,
		remoteIP, remoteIP,
	)
}

// ─── Shared string utilities ─────────────────────────────────────────────────

func clampStr(b []byte, n int) string {
	if len(b) > n {
		return string(b[:n]) + "..."
	}
	return string(b)
}

func shortErr(err error) string {
	if err == nil {
		return ""
	}
	s := err.Error()
	for _, pfx := range []string{"Post \"", "Get \"", "dial tcp "} {
		if i := strings.Index(s, pfx); i >= 0 {
			s = s[i+len(pfx):]
		}
	}
	if len(s) > 90 {
		s = s[:90] + "..."
	}
	return s
}
