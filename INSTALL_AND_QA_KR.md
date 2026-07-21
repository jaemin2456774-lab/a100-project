# 설치 및 QA

1. ZIP의 `main.py`를 현재 배포 파일과 교체합니다.
2. Railway에 재배포합니다.
3. 아래 순서로 확인합니다.

```text
/version
/buildinfo
/versionaudit
/commandcert
/commandcert status
/commandcert batch 1 run
/commandcert status
/commandcert
/commandmatrix
/trustgate
/errors
```

## 정상 기대값
- Registry 341/341
- Version Audit PASS
- Priority Queue 0 이상
- Counter reconciliation PASS
- Historical reconciliation PASS
- Promotion transitions는 실제 PASS 전환 수와 동일
- 단순 `/commandcert`, `/trustgate` 조회 시 ledger 불필요 증가 없음
