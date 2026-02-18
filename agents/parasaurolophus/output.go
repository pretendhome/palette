package main

import (
	"fmt"
	"strings"
)

func statusIcon(s SignalStatus) string {
	switch s {
	case SignalNormal:
		return "✓"
	case SignalWarn:
		return "~"
	case SignalAlert, SignalError:
		return "✗"
	}
	return "?"
}

// printSignalLine prints a single metric result.
// Passing metrics are suppressed unless verbose is true.
func printSignalLine(sig MetricSignal, verbose bool) {
	if sig.Status == SignalNormal && !verbose {
		return
	}
	route := ""
	if sig.Status != SignalNormal && sig.RouteTo != "" {
		route = fmt.Sprintf("  [→%s]", sig.RouteTo)
	}
	fmt.Printf("  [%s] %-20s  %s%s\n",
		statusIcon(sig.Status), sig.Name, sig.Detail, route)
}

// printCheckSummary prints a formatted table of all metric results.
func printCheckSummary(sigs []MetricSignal) {
	fmt.Println()
	fmt.Println("PARA — metric check")
	fmt.Println(strings.Repeat("─", 70))
	for _, sig := range sigs {
		route := ""
		if sig.Status != SignalNormal && sig.RouteTo != "" {
			route = fmt.Sprintf("  [→%s]", sig.RouteTo)
		}
		fmt.Printf("  [%s] %-20s  %s%s\n",
			statusIcon(sig.Status), sig.Name, sig.Detail, route)
	}
	fmt.Println()
}

// printList prints every configured metric and its expected baseline.
func printList() {
	fmt.Println()
	fmt.Println("PARA — configured metrics")
	fmt.Println(strings.Repeat("─", 70))
	fmt.Printf("  %-22s  %s\n", "METRIC", "BASELINE")
	fmt.Println(strings.Repeat("─", 70))
	for _, m := range metricChain {
		fmt.Printf("  %-22s  %s\n", m.Name, m.Baseline)
	}
	fmt.Println()
}
