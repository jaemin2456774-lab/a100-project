"""A100 V94.0 AI Learning Visualization.
Pure text visualization helpers for Telegram. No network, disk mutation, or trading path.
"""
from __future__ import annotations

FULL = "█"
EMPTY = "░"


def clamp(value, low=0.0, high=100.0):
    try:
        value = float(value)
    except Exception:
        value = 0.0
    return max(low, min(high, value))


def bar(value, width=10, maximum=100.0):
    """Return a fixed-width Unicode bar. O(width), width capped for message safety."""
    width = max(4, min(20, int(width)))
    maximum = float(maximum) if maximum else 100.0
    ratio = clamp(float(value) / maximum * 100.0) / 100.0
    filled = int(round(ratio * width))
    return FULL * filled + EMPTY * (width - filled)


def percent_line(label, value, *, width=10, suffix="", count=None):
    value = clamp(value)
    tail = f" {value:.1f}%"
    if count is not None:
        tail += f" · {int(count)}건"
    if suffix:
        tail += f" · {suffix}"
    return f"{label}\n{bar(value, width)} {tail.strip()}"


def signed_score_bar(value, *, width=10, limit=10.0):
    """Visualize signed contribution by magnitude while retaining sign in text."""
    try:
        value = float(value)
    except Exception:
        value = 0.0
    magnitude = min(abs(value), limit) / limit * 100.0
    sign = "+" if value > 0 else ("-" if value < 0 else "±")
    return f"{bar(magnitude, width)} {sign}{abs(value):.1f}"


def performance_health(rows):
    """Compact health metric from sample size, win rate, and average return."""
    vals = []
    for row in rows:
        try:
            vals.append(float(row))
        except Exception:
            pass
    n = len(vals)
    if not n:
        return 0.0
    wins = sum(v > 0 for v in vals)
    win_rate = wins / n * 100.0
    sample_score = min(100.0, n / 150.0 * 100.0)
    avg = sum(vals) / n
    return round(clamp(0.55 * win_rate + 0.30 * sample_score + 0.15 * clamp(50 + avg * 10)), 1)
