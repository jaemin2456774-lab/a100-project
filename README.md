# A100 V113.1 Command Integrity & Version Sync Development

## Critical hotfix
- Moved the executable `__main__` block to the physical end of `main.py`.
- Ensures V113 queue/execution commands are registered before the Telegram application starts.
- Added `/versionaudit` for runtime callback/version verification.
- Startup now fails fast when required callbacks, registry snapshot, version, limits, or schema checks fail.
- Active `/help` and `/commands` outputs are synchronized to V113.1.

# A100 V113.1 Entry Execution & Paper Queue Intelligence Development

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


## V113.1 핵심 변경
- LEARNING 모드에서는 legacy PAPER_AUTO_ENTRY 값과 무관하게 Paper 자동 진입 파이프라인 활성화
- ENTRY 통과 후보를 영구 Paper Queue에 저장
- Scanner → ENTRY → Queue → Paper Create 전 과정 추적
- 일시적 생성 오류는 8초 후 1회 제한 재시도
- 중복, 쿨다운, 포지션 한도, Kill Switch, BTC Shock 등 안전장치 유지
- 신규 명령: /entrytrace, /paperqueue, /entryrecovery, /entryexecution
