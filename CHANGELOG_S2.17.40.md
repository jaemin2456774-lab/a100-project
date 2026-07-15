# A100 V116.0 LTS S2.17.40
## Final UI Polish & Production Release Candidate

### 변경 사항
- `/versionaudit`를 그룹형 최종 RC 감사 화면으로 정리했습니다.
- `/commandcert`에 성공률, Release Freeze, Regression Risk, Gate Formula, Live OFF 상태를 추가했습니다.
- `/runtimehealth`에 마지막 Evidence 갱신 시각과 Snapshot age를 추가했습니다.
- Dashboard/Release Gate/LTS Certification의 `LTS FINAL SUMMARY`에 Version Audit, Command Cert, Pipeline 상태를 추가했습니다.
- 릴리스 식별 경로 4개(`/version`, `/versionaudit`, `/commandcert`, `/runtimehealth`)를 S2.17.40으로 자동 정합합니다.

### 변경하지 않은 항목
- Release Gate 공식 및 임계값
- Runtime First / Strict Read Only / Evidence Worker
- Registry 341
- Schema 1 / Paper 20 / Shadow 60 / Live Trading OFF
- 기존 데이터와 설정
