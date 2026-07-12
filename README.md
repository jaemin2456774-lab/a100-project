# A100 V112.0 Score Calibration & Learning Boost Development

V111.0을 기준으로 Paper LEARNING 모드의 후보 점수 분포를 보정하고, 초기 학습 단계에서 상위 후보를 제한적으로 ENTRY로 전환하는 개발 릴리스입니다.

핵심 명령:
- `/scorecalibration`
- `/scorebreakdown BTC`
- `/learningboost`
- `/papertracescan`
- `/papertrace BTC`
- `/thresholdreview`

안전 원칙:
- 보정은 Paper LEARNING 모드에만 적용
- 후보당 점수 보정 최대 +12점
- 목표 ENTRY 통과율 5~15%
- 최대 포지션 20, Shadow 60, 중복·쿨다운·Kill Switch·시장 데이터·BTC Shock Guard 유지
- 실주문 기능 및 실주문 기준 변경 없음
