#!/usr/bin/env python3
"""
market_stress.py — Financial Failure Probability Model

Computes a composite market stress score from three valuation metrics:
  1. Shiller PE (CAPE) — cyclically adjusted P/E, 10-year smoothed earnings
  2. Buffett Indicator — total market cap / GDP
  3. S&P 500 P/S ratio — price-to-sales

Each metric is scored against historical distributions, then combined into a
probability estimate of significant market drawdown (>20%) within 12 months.

The model is calibrated against historical crash frequencies at each valuation
band. It is NOT a timing tool — it measures structural overvaluation risk.

Usage:
    from market_stress import compute_stress, format_stress_report

    result = compute_stress(cape=33.5, buffett=185, ps_ratio=2.8)
    print(format_stress_report(result))
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


# ── Scoring bands ──────────────────────────────────────────────────────────
# Each band maps a metric range to a conditional probability of >20% drawdown
# within 12 months, calibrated from S&P 500 history (1900-2025 for CAPE,
# 1970-2025 for Buffett/PS).
#
# These are NOT precise — they're informed estimates from historical frequency
# analysis. The uncertainty is large, which is why the report includes ranges.

CAPE_BANDS = [
    # (upper_bound, risk_score, label)
    (15,   0.08, "Undervalued"),
    (20,   0.12, "Fair value"),
    (25,   0.18, "Elevated"),
    (30,   0.28, "High"),
    (35,   0.38, "Very high"),
    (40,   0.48, "Extreme"),
    (999,  0.58, "Unprecedented"),
]

BUFFETT_BANDS = [
    (75,   0.06, "Undervalued"),
    (90,   0.10, "Fair value"),
    (115,  0.16, "Elevated"),
    (150,  0.28, "High"),
    (180,  0.40, "Very high"),
    (999,  0.55, "Extreme"),
]

PS_BANDS = [
    (1.0,  0.06, "Undervalued"),
    (1.5,  0.10, "Fair value"),
    (2.0,  0.18, "Elevated"),
    (2.5,  0.30, "High"),
    (3.0,  0.42, "Very high"),
    (999,  0.55, "Extreme"),
]


@dataclass
class MetricScore:
    name: str
    value: float
    label: str
    risk: float
    historical_avg: float
    deviation: str  # e.g. "2.1x historical average"


@dataclass
class StressResult:
    cape: MetricScore
    buffett: MetricScore
    ps_ratio: MetricScore
    composite_risk: float
    risk_label: str
    agreement: int  # how many metrics agree on "elevated or higher" (0-3)
    methodology_note: str


def _score_metric(value: float, bands: list, name: str, hist_avg: float) -> MetricScore:
    """Score a single metric against its bands."""
    for upper, risk, label in bands:
        if value <= upper:
            ratio = value / hist_avg
            return MetricScore(
                name=name,
                value=value,
                label=label,
                risk=risk,
                historical_avg=hist_avg,
                deviation=f"{ratio:.1f}x historical average",
            )
    # Shouldn't reach here given 999 upper bounds
    last = bands[-1]
    return MetricScore(name, value, last[2], last[1], hist_avg, f"{value/hist_avg:.1f}x")


def compute_stress(
    cape: float,
    buffett: float,
    ps_ratio: float,
) -> StressResult:
    """Compute composite financial stress score.

    Args:
        cape: Shiller PE (CAPE) ratio
        buffett: Buffett Indicator (market cap / GDP as percentage, e.g., 185 = 185%)
        ps_ratio: S&P 500 price-to-sales ratio

    Returns:
        StressResult with individual and composite scores
    """
    cape_score = _score_metric(cape, CAPE_BANDS, "Shiller PE (CAPE)", 16.5)
    buffett_score = _score_metric(buffett, BUFFETT_BANDS, "Buffett Indicator", 80.0)
    ps_score = _score_metric(ps_ratio, PS_BANDS, "S&P 500 P/S", 1.4)

    # Composite: weighted average with correlation bonus
    # When all three agree, risk is higher than simple average suggests
    weights = [0.40, 0.35, 0.25]  # CAPE, Buffett, P/S
    risks = [cape_score.risk, buffett_score.risk, ps_score.risk]
    weighted_avg = sum(w * r for w, r in zip(weights, risks))

    # Count agreement on "elevated or higher" (risk >= 0.16)
    elevated_count = sum(1 for r in risks if r >= 0.16)

    # Correlation adjustment: when all three flash high, add convergence premium
    if elevated_count == 3:
        composite = min(weighted_avg * 1.15, 0.70)  # cap at 70%
    elif elevated_count == 2:
        composite = min(weighted_avg * 1.05, 0.65)
    else:
        composite = weighted_avg

    # Risk label
    if composite < 0.12:
        risk_label = "LOW"
    elif composite < 0.20:
        risk_label = "MODERATE"
    elif composite < 0.35:
        risk_label = "ELEVATED"
    elif composite < 0.50:
        risk_label = "HIGH"
    else:
        risk_label = "SEVERE"

    return StressResult(
        cape=cape_score,
        buffett=buffett_score,
        ps_ratio=ps_score,
        composite_risk=composite,
        risk_label=risk_label,
        agreement=elevated_count,
        methodology_note=(
            "Based on historical frequency of >20% S&P 500 drawdowns at comparable "
            "valuation levels. CAPE calibrated from 1900-2025 data, Buffett/PS from "
            "1970-2025. This is a structural overvaluation measure, not a timing tool. "
            "Crashes require catalysts — high valuations increase vulnerability but "
            "don't predict when."
        ),
    )


def format_stress_report(result: StressResult) -> str:
    """Format a StressResult as a Telegram-friendly markdown report."""
    lines = [
        f"*Market Stress: {result.risk_label}*",
        f"Probability of >20% drawdown within 12 months: *{result.composite_risk:.0%}*",
        "",
    ]

    for m in [result.cape, result.buffett, result.ps_ratio]:
        bar = _risk_bar(m.risk)
        lines.append(f"*{m.name}*: {m.value:.1f} ({m.label})")
        lines.append(f"  {bar}  {m.risk:.0%} | {m.deviation}")
        lines.append("")

    if result.agreement == 3:
        lines.append("All 3 metrics signal elevated or higher — convergence premium applied.")
    elif result.agreement == 2:
        lines.append(f"{result.agreement}/3 metrics signal elevated or higher.")
    else:
        lines.append(f"{result.agreement}/3 metrics signal elevated or higher — mixed signal.")

    lines.append("")
    lines.append(f"_{result.methodology_note}_")

    return "\n".join(lines)


def _risk_bar(risk: float) -> str:
    """Visual risk bar using Unicode blocks."""
    filled = int(risk * 10)
    return "\u2588" * filled + "\u2591" * (10 - filled)


# ── Perplexity-based data fetcher ──────────────────────────────────────────

FETCH_PROMPT = """You are a financial data assistant. I need exactly three current market metrics.
Reply with ONLY three lines, each with the label, a colon, and the numeric value. Example format:

CAPE: 33.5
BUFFETT: 185.2
PS: 2.7

CAPE is the Shiller PE (cyclically adjusted price-to-earnings) for the S&P 500.
BUFFETT is the Buffett Indicator: total US stock market capitalization divided by US GDP, expressed as a percentage (e.g. 185 means 185%).
PS is the S&P 500 price-to-sales ratio.

Use the most recent data available. Every line MUST have a real number, not a placeholder."""

FETCH_QUERY = (
    "What is the current Shiller PE CAPE ratio? "
    "What is the current Buffett Indicator (total US market cap to GDP ratio as a percentage)? "
    "What is the current S&P 500 price-to-sales ratio? "
    "Give the most recent figures available as of today."
)


def fetch_current_metrics(perplexity_key: str) -> dict[str, float] | None:
    """Fetch current metric values via Perplexity Sonar API.

    Returns dict with keys 'cape', 'buffett', 'ps_ratio' or None on failure.
    """
    import re as _re

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {"role": "system", "content": FETCH_PROMPT},
                        {"role": "user", "content": FETCH_QUERY},
                    ],
                },
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None

    # Parse the structured response — try exact format first, then fuzzy
    values = {}
    for key, label in [("cape", "CAPE"), ("buffett", "BUFFETT"), ("ps_ratio", "PS")]:
        match = _re.search(rf'{label}\s*[:=]\s*([\d.]+)', content)
        if match:
            val = float(match.group(1))
            # Sanity check: reject placeholder-like values
            if val > 0:
                values[key] = val

    if len(values) == 3:
        return values

    # Fallback: try to find numbers near keyword mentions
    fallback_patterns = [
        ("cape", r'(?:shiller|cape|cyclically adjusted)[^.]*?([\d]{2,3}(?:\.\d+)?)'),
        ("buffett", r'(?:buffett|market.cap.to.gdp|market.cap.?.gdp)[^.]*?([\d]{2,3}(?:\.\d+)?)'),
        ("ps_ratio", r'(?:price.to.sales|p/s ratio|p.s ratio)[^.]*?([\d](?:\.\d+)?)'),
    ]
    for key, pattern in fallback_patterns:
        if key not in values:
            match = _re.search(pattern, content, _re.IGNORECASE)
            if match:
                values[key] = float(match.group(1))

    if len(values) == 3:
        return values
    return None
