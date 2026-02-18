package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

// ─── Bridge fix ───────────────────────────────────────────────────────────────

type FixResult struct {
	Applied    bool
	BridgeIP   string
	BridgeURL  string
	BridgePID  string
	Err        string
}

// applyBridgeFix dispatches to local or remote depending on the Runner.
// Local: runs nsenter+socat as a Go child process (requires root on VPS).
// Remote: SSHs in, installs socat if needed, runs nohup nsenter+socat.
func applyBridgeFix(run Runner, cfg Config) FixResult {
	if run.IsRemote() {
		return applyRemoteBridgeFix(run, cfg)
	}
	return applyLocalBridgeFix(run, cfg)
}

// applyLocalBridgeFix creates the bridge on the machine raptor is running on.
// Must be executed as root on the VPS (not the local laptop).
func applyLocalBridgeFix(run Runner, cfg Config) FixResult {
	pid, err := run.DockerInspect(cfg.Container, "{{.State.Pid}}")
	if err != nil || pid == "0" || pid == "" {
		return FixResult{Err: fmt.Sprintf("cannot get container PID: %v", err)}
	}

	netnsPath := fmt.Sprintf("/proc/%s/ns/net", pid)
	listenArg := fmt.Sprintf("TCP-LISTEN:%d,fork,reuseaddr,bind=0.0.0.0", cfg.BridgePort)
	targetArg := fmt.Sprintf("TCP:127.0.0.1:%d", cfg.ServicePort)

	cmd := exec.Command("nsenter", fmt.Sprintf("--net=%s", netnsPath), "--", "socat", listenArg, targetArg)
	if err := cmd.Start(); err != nil {
		return FixResult{Err: "nsenter+socat failed: " + err.Error() +
			"\nEnsure socat is installed (apt install socat) and you are running as root."}
	}
	go func() { _ = cmd.Wait() }()
	time.Sleep(700 * time.Millisecond)

	ip, err := run.DockerInspect(cfg.Container,
		"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}")
	if err != nil || ip == "" {
		return FixResult{Err: "bridge started but cannot get bridge IP: " + shortErr(err)}
	}
	if !run.TCPCheck(ip, cfg.BridgePort) {
		return FixResult{Err: fmt.Sprintf("bridge started (PID %d) but %s:%d not yet reachable — retry in a moment.",
			cmd.Process.Pid, ip, cfg.BridgePort)}
	}
	return FixResult{
		Applied:   true,
		BridgeIP:  ip,
		BridgeURL: fmt.Sprintf("http://%s:%d/", ip, cfg.BridgePort),
		BridgePID: fmt.Sprint(cmd.Process.Pid),
	}
}

// applyRemoteBridgeFix SSHs into the VPS and applies the bridge remotely.
// This is the "one command does everything" path:
//
//	raptor fix --remote root@72.60.171.27
func applyRemoteBridgeFix(run Runner, cfg Config) FixResult {
	step := func(desc, cmd string) (string, error) {
		fmt.Printf("  → %s\n", desc)
		out, err := run.Exec(cmd)
		if err != nil {
			fmt.Printf("    ✗ %v\n", err)
		} else if cfg.Verbose && out != "" {
			fmt.Printf("    %s\n", out)
		}
		return out, err
	}

	// Ensure socat is available
	_, _ = step("Checking socat", "which socat 2>/dev/null || apt-get install -y socat >/dev/null 2>&1")

	// Kill any stale bridge on that port (idempotent)
	_, _ = step("Clearing stale bridge",
		fmt.Sprintf("fuser -k %d/tcp 2>/dev/null; true", cfg.BridgePort))
	time.Sleep(300 * time.Millisecond)

	// Get container PID
	pid, err := step("Getting container PID",
		fmt.Sprintf("docker inspect --format '{{.State.Pid}}' %s", cfg.Container))
	if err != nil || pid == "0" || pid == "" {
		return FixResult{Err: fmt.Sprintf("container PID unavailable (got %q): %v", pid, err)}
	}
	fmt.Printf("    PID=%s\n", pid)

	// Launch bridge with nohup so it persists after the SSH session ends
	bridgeCmd := fmt.Sprintf(
		"nohup nsenter --net=/proc/%s/ns/net -- "+
			"socat TCP-LISTEN:%d,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:%d "+
			"> /tmp/raptor-bridge.log 2>&1 & echo $!",
		pid, cfg.BridgePort, cfg.ServicePort)
	bridgePID, err := step("Creating socat bridge", bridgeCmd)
	if err != nil {
		return FixResult{Err: "bridge creation failed: " + err.Error()}
	}
	fmt.Printf("    Bridge PID=%s\n", bridgePID)
	time.Sleep(700 * time.Millisecond)

	// Get container bridge IP
	ip, err := step("Getting container bridge IP",
		fmt.Sprintf("docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' %s",
			cfg.Container))
	if err != nil || ip == "" {
		return FixResult{Err: "cannot get container bridge IP: " + shortErr(err)}
	}
	fmt.Printf("    Bridge IP=%s\n", ip)

	// Verify bridge is reachable from the VPS host
	verifyOut, err := step("Verifying bridge",
		fmt.Sprintf("curl -s --max-time 5 -o /dev/null -w '%%{http_code}' -X POST http://%s:%d%s -H 'Content-Type: application/json' -d '%s'",
			ip, cfg.BridgePort, cfg.APIPath,
			strings.ReplaceAll(string(probePayload(cfg)), "'", `'"'"'`)))
	if err != nil || verifyOut == "000" || verifyOut == "" {
		return FixResult{Err: fmt.Sprintf("bridge at %s:%d not responding (HTTP %s): %v",
			ip, cfg.BridgePort, verifyOut, err)}
	}
	fmt.Printf("    HTTP %s — bridge is live\n", verifyOut)

	return FixResult{
		Applied:   true,
		BridgeIP:  ip,
		BridgeURL: fmt.Sprintf("http://%s:%d/", ip, cfg.BridgePort),
		BridgePID: bridgePID,
	}
}

// ─── Tunnel management ────────────────────────────────────────────────────────

type TunnelResult struct {
	Active     bool
	LocalPort  int
	BridgeIP   string
	BridgePort int
	Err        string
}

// manageTunnel kills any existing SSH tunnel on TunnelPort and starts a new
// one pointing at bridgeIP:BridgePort on the remote host.
// Uses ssh -f so it daemonizes after authentication (no separate terminal needed).
func manageTunnel(cfg Config, bridgeIP string) TunnelResult {
	fmt.Printf("  → Killing any existing process on local port %d\n", cfg.TunnelPort)
	_ = exec.Command("fuser", "-k", fmt.Sprintf("%d/tcp", cfg.TunnelPort)).Run()
	time.Sleep(300 * time.Millisecond)

	remote := cfg.Remote
	tunnelSpec := fmt.Sprintf("%d:%s:%d", cfg.TunnelPort, bridgeIP, cfg.BridgePort)
	fmt.Printf("  → Starting tunnel: localhost:%d → %s → %s:%d\n",
		cfg.TunnelPort, remote, bridgeIP, cfg.BridgePort)

	cmd := exec.Command("ssh",
		"-N", "-f",
		"-o", "StrictHostKeyChecking=accept-new",
		"-o", "ExitOnForwardFailure=yes",
		"-L", tunnelSpec,
		remote,
	)
	if err := cmd.Run(); err != nil {
		return TunnelResult{Err: fmt.Sprintf(
			"ssh tunnel failed: %v\n"+
				"  Tip: set up key auth first: ssh-copy-id %s\n"+
				"  Then retry: raptor tunnel --remote %s --bridge-ip %s",
			err, remote, remote, bridgeIP)}
	}

	time.Sleep(400 * time.Millisecond)
	local := NewLocalRunner(false)
	if !local.TCPCheck("127.0.0.1", cfg.TunnelPort) {
		return TunnelResult{Err: fmt.Sprintf("tunnel started but port %d not listening locally", cfg.TunnelPort)}
	}
	return TunnelResult{
		Active:     true,
		LocalPort:  cfg.TunnelPort,
		BridgeIP:   bridgeIP,
		BridgePort: cfg.BridgePort,
	}
}

// ─── Persistence ──────────────────────────────────────────────────────────────

// systemdUnit generates a systemd service unit that recreates the socat bridge
// after container or host restarts.
func systemdUnit(cfg Config) string {
	return fmt.Sprintf(`[Unit]
Description=Raptor bridge: %s loopback (%d) → Docker bridge (%d)
After=docker.service
Requires=docker.service

[Service]
Type=simple
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  CPID=$(docker inspect --format "{{.State.Pid}}" %s 2>/dev/null); \
  if [ -z "$CPID" ] || [ "$CPID" = "0" ]; then \
    echo "Container not running" >&2; exit 1; \
  fi; \
  exec nsenter --net=/proc/$CPID/ns/net -- \
    socat TCP-LISTEN:%d,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:%d'
Restart=on-failure
RestartSec=15

[Install]
WantedBy=multi-user.target
`, cfg.Container, cfg.ServicePort, cfg.BridgePort,
		cfg.Container,
		cfg.BridgePort, cfg.ServicePort)
}

// applyPersistence installs and enables the systemd unit locally or remotely.
func applyPersistence(run Runner, cfg Config) error {
	unitName := fmt.Sprintf("raptor-bridge-%s.service", cfg.Container)
	content := systemdUnit(cfg)

	if run.IsRemote() {
		// Write unit file via heredoc, then enable it
		installCmd := fmt.Sprintf(
			"cat > /etc/systemd/system/%s <<'RAPTOREOF'\n%s\nRAPTOREOF\n"+
				"systemctl daemon-reload && systemctl enable --now %s",
			unitName, content, unitName)
		out, err := run.Exec(installCmd)
		if err != nil {
			return fmt.Errorf("remote install failed: %w\n%s", err, out)
		}
		fmt.Printf("  ✓ Installed and enabled %s on %s\n", unitName, run.Target())
		return nil
	}

	// Local install — requires root
	path := "/etc/systemd/system/" + unitName
	if err := os.WriteFile(path, []byte(content), 0644); err != nil {
		return fmt.Errorf("write unit file: %w\n  (Run as root, or use: raptor persist --remote %s)", err, cfg.Remote)
	}
	if out, err := exec.Command("systemctl", "daemon-reload").CombinedOutput(); err != nil {
		return fmt.Errorf("daemon-reload: %w: %s", err, out)
	}
	if out, err := exec.Command("systemctl", "enable", "--now", unitName).CombinedOutput(); err != nil {
		return fmt.Errorf("systemctl enable: %w: %s", err, out)
	}
	fmt.Printf("  ✓ Installed and enabled %s\n", path)
	return nil
}
