# A100 V118.0 RC3.8 설치 및 QA

기존 프로젝트에 `main.py`를 덮어쓰고 Railway에서 재배포 또는 재시작합니다. 데이터와 환경변수는 변경하지 않습니다.

## 기본 검수
/version
/buildinfo
/versionaudit
/errors

## True Fast Path 검수
아래 각 명령을 900초 이내에 6회 실행합니다.
/commandcert
/commandmatrix
/trustgate
/intelligencescore

마지막으로 실행합니다.
/performance
/performancebudget
/perf

## 기대 결과
- Registry 341/341
- Architecture Guard PASS
- Version Audit PASS
- 두 번째 호출부터 Cache HIT
- Warm P50/P95와 Cold P50/P95가 분리 표시
- 최소 Warm Samples 5개 이후 Warm P95 기준 PASS/FAIL
- Cache HIT 시 Query render가 큰 폭으로 감소
