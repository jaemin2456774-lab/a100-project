# 설치 및 QA

Railway에 `main.py`를 배포한 뒤 다음 순서로 실행합니다.

```text
/version
/buildinfo
/versionaudit
/commandcert batch 1 run
/commandcert status
/versionaudit
/commandcert
/commandmatrix
/errors
```

## 기대 결과
- `/aidashboard`는 Safe Batch에서 제외
- Runner status에 `Provenance QA / Background / Unknown` 표시
- 신규 anomaly가 있으면 실제 ID와 command가 Version Audit에 표시
- QA 0, Unknown 0이면 QA reconciliation PASS
- Background 증가가 있으면 Background Pipeline 항목만 FAIL
