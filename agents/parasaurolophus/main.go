// para — Palette Signal Monitor (Parasaurolophus)
//
// Continuous metric monitoring for containerized AI services.
// Applies Raptor's Runner/MetricFunc/metricChain patterns to monitoring:
//   - MetricRunner interface  →  local or SSH execution, same MetricFunc
//   - []MetricFunc chain      →  adding a metric = one line, no engine changes
//   - goroutine-per-metric    →  all checks run in parallel each cycle
//   - HandoffPacket output    →  alerts go straight into the Palette protocol
//
// Para sees everything. Para fixes nothing. Para routes to those who can.

package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	if len(os.Args) < 2 ||
		os.Args[1] == "-h" || os.Args[1] == "--help" || os.Args[1] == "help" {
		usage()
		os.Exit(0)
	}

	sub := os.Args[1]
	cfg := defaultConfig()
	fs := buildFlags(&cfg)
	_ = fs.Parse(os.Args[2:])

	if cfg.TraceID == "" {
		cfg.TraceID = newUUID()
	}

	run := newRunner(cfg)

	fmt.Printf("\nPARA v%s — Palette Signal Monitor (Parasaurolophus)\n", version)
	fmt.Printf("Target: %s\n\n", run.Target())

	switch sub {

	case "watch", "w":
		quit := make(chan os.Signal, 1)
		signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
		go watchLoop(run, cfg)
		<-quit
		fmt.Println("\nPara stopped.")

	case "check", "c":
		sigs := runAll(run, cfg)
		printCheckSummary(sigs)
		for _, sig := range sigs {
			if sig.Status != SignalNormal {
				os.Exit(1)
			}
		}

	case "list", "l":
		printList()

	case "report", "r":
		sigs := runAll(run, cfg)
		printReport(sigs, cfg)

	default:
		fmt.Fprintf(os.Stderr, "unknown subcommand: %s\n\n", sub)
		usage()
		os.Exit(1)
	}
}
