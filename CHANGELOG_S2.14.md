# A100 V116.0 LTS-S2.14
## Unified Certification Score Engine Patch

### 변경 사항
- Status, Runtime Health, Dashboard, Release Gate가 하나의 공유 인증 스냅샷을 사용하도록 통합했습니다.
- Runtime Raw Score와 Calibrated Score 계산 경로를 단일화했습니다.
- Runtime 점수, Confidence, Stability Forecast, Regression Probability가 모든 화면에서 동일한 원본을 사용합니다.
- Structural Risk, Operational Risk, Prediction Risk를 분리했습니다.
- 기존 `Runtime Analytics S2.10` 표기를 제거하고 `UNIFIED RUNTIME SCORE ENGINE`으로 교체했습니다.
- Mandatory Gate는 기존 기준을 그대로 유지하며 Calibration이 차단 Gate를 우회하지 못하도록 유지했습니다.
- `/version`, `/status`, `/runtimehealth`, `/dashboard`, `/releasegate`를 S2.14 핸들러로 연결했습니다.

### 유지 정책
- Schema 1
- Paper 20
- Shadow 60
- Live Trading OFF
- Feature Freeze ACTIVE
- Release Freeze ACTIVE
- Registry 341/341 구조 유지
- 기존 데이터 및 저장 경로 변경 없음
