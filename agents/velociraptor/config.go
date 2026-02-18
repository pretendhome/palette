package main

import (
	"encoding/json"
	"flag"
	"os"
)

// Config holds all runtime configuration for Raptor.
// Flags override defaults; env vars fill in token/URL if flags not set.
type Config struct {
	// Container / service
	Container   string // Docker container name
	ServicePort int    // Port service binds inside container
	BridgePort  int    // Port socat exposes on 0.0.0.0 in container netns

	// Remote VPS
	Remote   string // SSH target: user@host
	RemoteIP string // VPS public IP (for tunnel, if different from Remote host)

	// Local SSH tunnel
	TunnelPort int // Local port forwarded to bridge

	// Adapter (local HTTP proxy, e.g. MissionCanvas)
	AdapterURL   string
	HealthPath   string
	RoutePath    string
	RoutePayload string

	// Upstream service (e.g. OpenClaw)
	UpstreamURL   string
	UpstreamToken string
	APIPath       string
	APIPayload    string // overrides generated payload if set
	APIModel      string

	// Misc
	EnvFile string
	DryRun  bool
	Verbose bool
}

func defaultConfig() Config {
	return Config{
		Container:     "openclaw-fcup-openclaw-1",
		ServicePort:   18789,
		BridgePort:    19000,
		TunnelPort:    18889,
		AdapterURL:    "http://localhost:8787",
		HealthPath:    "/v1/missioncanvas/health",
		RoutePath:     "/v1/missioncanvas/route",
		RoutePayload:  `{"input":{"objective":"raptor connectivity probe"}}`,
		UpstreamURL:   os.Getenv("OPENCLAW_BASE_URL"),
		UpstreamToken: os.Getenv("OPENCLAW_API_KEY"),
		APIPath:       "/v1/chat/completions",
		APIModel:      "openclaw:main",
		EnvFile:       "",
	}
}

// probePayload returns the JSON body to use when probing the upstream API.
func probePayload(cfg Config) []byte {
	if cfg.APIPayload != "" {
		return []byte(cfg.APIPayload)
	}
	p, _ := json.Marshal(map[string]interface{}{
		"model": cfg.APIModel,
		"messages": []map[string]string{
			{"role": "user", "content": "ping"},
		},
	})
	return p
}

func buildFlags(cfg *Config) *flag.FlagSet {
	fs := flag.NewFlagSet("raptor", flag.ExitOnError)
	fs.StringVar(&cfg.Container, "container", cfg.Container, "")
	fs.IntVar(&cfg.ServicePort, "service-port", cfg.ServicePort, "")
	fs.IntVar(&cfg.BridgePort, "bridge-port", cfg.BridgePort, "")
	fs.IntVar(&cfg.TunnelPort, "tunnel-port", cfg.TunnelPort, "")
	fs.StringVar(&cfg.Remote, "remote", cfg.Remote, "")
	fs.StringVar(&cfg.RemoteIP, "remote-ip", cfg.RemoteIP, "")
	fs.StringVar(&cfg.AdapterURL, "adapter-url", cfg.AdapterURL, "")
	fs.StringVar(&cfg.UpstreamURL, "upstream-url", cfg.UpstreamURL, "")
	fs.StringVar(&cfg.UpstreamToken, "token", cfg.UpstreamToken, "")
	fs.StringVar(&cfg.APIPath, "api-path", cfg.APIPath, "")
	fs.StringVar(&cfg.APIModel, "api-model", cfg.APIModel, "")
	fs.StringVar(&cfg.APIPayload, "api-payload", cfg.APIPayload, "")
	fs.StringVar(&cfg.EnvFile, "env-file", cfg.EnvFile, "")
	fs.BoolVar(&cfg.DryRun, "dry-run", false, "")
	fs.BoolVar(&cfg.Verbose, "verbose", false, "")
	return fs
}
