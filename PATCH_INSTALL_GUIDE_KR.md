# A100 V116.1 DEV S59.7.22 설치 가이드

1. Railway 배포 소스의 기존 `main.py`를 백업합니다.
2. 이 패키지의 `main.py`로 교체합니다.
3. 기존 Runtime/Learning 데이터 볼륨은 삭제하거나 초기화하지 않습니다.
4. Railway를 재배포합니다.
5. `/version`, `/versionaudit`, `/papershadow`, `/errors` 순서로 확인합니다.

## 정상 기대 결과

- Registry 341/341
- Version Audit PASS
- Shadow Candidate Snapshot 정상
- ENTRY GATE TRACE 표시
- Shadow Review/Accuracy 수치가 종료 표본과 연결
- 신규 시스템 오류 0건

이 패치는 점수 임계값, Stage 분류, Gate Formula, Paper/Live 주문 조건을 변경하지 않습니다.
