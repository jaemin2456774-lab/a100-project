"""A100 V92.7 learning confidence calibration helpers.

Pure functions only: no network calls, no state writes, no live-order path.
"""
from __future__ import annotations


def calibrated_confidence(raw_confidence: float, evaluated: int, adjusted_win_rate: float,
                          completion: float, min_samples: int = 20) -> dict:
    raw = max(0.0, min(99.0, float(raw_confidence)))
    n = max(0, int(evaluated))
    win = max(0.0, min(100.0, float(adjusted_win_rate)))
    comp = max(0.0, min(100.0, float(completion)))

    # Bayesian-style sample trust. Before min_samples, changes remain deliberately small.
    trust = min(1.0, n / max(1.0, float(min_samples)))
    maturity = min(1.0, comp / 100.0)
    weight = min(0.35, 0.08 + 0.27 * trust * maturity)
    learned = raw * (1.0 - weight) + win * weight
    max_shift = 2.0 if n < min_samples else 8.0
    learned = max(raw - max_shift, min(raw + max_shift, learned))
    learned = max(0.0, min(99.0, learned))
    delta = learned - raw
    return {
        "raw": round(raw, 1),
        "calibrated": round(learned, 1),
        "delta": round(delta, 1),
        "trust": round(trust * 100.0, 1),
        "sample_guard": n < min_samples,
        "min_samples": int(min_samples),
    }
