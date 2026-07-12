"""A100 V92.6 pure learning-intelligence helpers.
No Telegram, exchange, state-file, or live-order dependency.
"""
from __future__ import annotations


def stage_weight(stage: str) -> float:
    """Weight low-quality WATCH samples below READY/ENTRY samples."""
    return {"WATCH": 0.25, "READY": 0.60, "ENTRY": 1.00}.get(str(stage).upper(), 0.25)


def confidence_delta(adjusted_win_rate: float, recent_win_rate: float, recent_n: int) -> str:
    """Human-readable trend marker with a minimum recent sample guard."""
    if int(recent_n) < 5:
        return "→"
    delta = float(recent_win_rate) - float(adjusted_win_rate)
    if delta >= 3.0:
        return f"▲ {delta:.1f}%p"
    if delta <= -3.0:
        return f"▼ {abs(delta):.1f}%p"
    return "→"
