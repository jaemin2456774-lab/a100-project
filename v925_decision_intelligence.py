"""A100 V92.5 pure decision-intelligence calculations.

No Telegram, exchange, state-file, or live-order dependency is allowed here.
This keeps V92.5 independently testable and prevents legacy runtime slowdown.
"""
from __future__ import annotations


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


def learning_quality(*, evaluated: int, wins: int, losses: int, precision_n: int,
                     target_samples: int = 100) -> dict[str, float | int | str]:
    evaluated=max(0,int(evaluated)); wins=max(0,int(wins)); losses=max(0,int(losses)); precision_n=max(0,int(precision_n))
    target=max(1,int(target_samples)); decisive=wins+losses
    sample_score=min(100.0,evaluated/target*100.0)
    decisive_score=min(100.0,decisive/max(1,target*0.7)*100.0)
    precision_score=min(100.0,precision_n/max(1,target*0.4)*100.0)
    completion=round(sample_score*0.55+decisive_score*0.25+precision_score*0.20,1)
    adjusted_wr=round((wins+5.0)/max(1.0,decisive+10.0)*100.0,1)
    if evaluated<10: level="초기 학습"
    elif completion<40: level="기초 학습"
    elif completion<70: level="중간 학습"
    elif completion<90: level="고도화"
    else: level="운영 검증"
    return {"completion":completion,"adjusted_win_rate":adjusted_wr,"level":level,
            "decisive":decisive,"remaining":max(0,target-evaluated)}


def intelligence_score(*, score: float, confidence: float, consensus: float,
                       adjusted_win_rate: float, completion: float) -> float:
    base=clamp(score)*0.42+clamp(confidence)*0.25+clamp(consensus)*0.23+clamp(adjusted_win_rate)*0.10
    maturity=0.88+0.12*clamp(completion)/100.0
    return round(clamp(base*maturity),1)
