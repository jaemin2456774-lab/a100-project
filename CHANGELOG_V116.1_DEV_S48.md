# A100 V116.1 DEV S48

## Core Market Producer Recovery

- S47 Result/dict Runtime Object Bridge 유지
- 기존 CoinGlass 렌더링 필드의 Funding/OI 복구 유지
- live scanner `vol_ratio`를 Volume Activity Evidence로 연결
- 실제 price/stop 또는 기존 ATR 필드로 Volatility State 산출
- 기존 prob24/prob3d/prob7d, RSI, buy ratio로 Momentum State 산출
- 후보별 Core Producer ON/MISS 및 Connected/Missing 표시
- 전체 Evidence 차원을 9개에서 12개로 확장
- Runtime First / Read Only / Evidence Only 유지
- Synthetic Evidence, Synthetic PASS, Gate mutation, Order authority 없음
- Schema 1 / Registry 341 / Paper 20 / Shadow 60 / Live OFF 유지

## 미해결 범위

- Macro, News, Capital Rotation, Multi-Timeframe은 실제 feed가 없으면 MISSING 유지
- ReleaseGate Structural mismatch는 별도 Sprint에서 복구
- 최종 PASS는 Railway 실제 Runtime 캡처로만 판정
