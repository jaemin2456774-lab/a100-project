# A100 V94.1 GitHub Clean Release

기준 버전: **V94.0 AI Learning Visualization**

이 배포본은 기존 기능과 schema 1을 유지하면서 GitHub 저장소를 깨끗하게 교체할 수 있도록 정리한 업로드 전용 릴리스입니다.

## 업로드 핵심

1. 기존 GitHub 저장소의 파일을 모두 삭제하고 커밋합니다.
2. 이 폴더 안의 내용만 저장소 루트에 업로드합니다.
3. `.env`와 `a100_v91_paper_state.json`은 업로드하지 않습니다.
4. Railway 변수와 영구 볼륨의 상태 파일은 그대로 유지합니다.

파일 수를 100개 미만으로 줄였으며 캐시, 과거 README, 과거 변경 기록, 과거 manifest 중복본은 제거했습니다.

## 실행 파일

- `main.py`
- `v925_decision_intelligence.py`
- `v926_learning_intelligence.py`
- `v927_learning_calibration.py`
- `v930_ai_intelligence_core.py`
- `v931_self_learning_ai.py`
- `v940_ai_visualization.py`

## 데이터 호환성

- schema 1 유지
- 상태 파일명 `a100_v91_paper_state.json` 유지
- 기존 데이터 마이그레이션 없음
- 상태 파일은 GitHub에 포함하지 않음
