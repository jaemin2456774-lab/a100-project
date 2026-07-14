# A100 V116.0 LTS-S2.12
## Score Calibration & Forecast Patch

- Runtime score를 관측값과 권위 있는 Engineering Evidence로 보정
- Registry, Handler, Pipeline, Preflight, Schema/Paper/Shadow, Live OFF, Runtime Error, Recovery 상태 반영
- Runtime risk가 표본 부족만으로 HIGH가 되지 않도록 임계값 보정
- Raw score와 Calibrated score를 함께 표시해 투명성 유지
- Release Gate Pass Probability, Confidence, Remaining Risk 보정
- 24H Forecast 및 Authoritative Evidence 요약 추가
- Mandatory Gate는 기존 값 그대로 유지하며 예측치가 게이트를 우회하지 않음
- Schema 1, Paper 20, Shadow 60, Live Trading OFF 유지
- 기존 341개 명령 구조 및 기존 데이터 변경 없음
