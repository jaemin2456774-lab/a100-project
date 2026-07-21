# 설치 및 QA

Railway에 main.py를 배포한 후 다음 순서로 확인합니다.

```text
/version
/buildinfo
/commandcert batch 1 run
/commandcert status
/commandcert
/commandmatrix
/versionaudit
/errors
```

기대 결과:
- Build/Wrapper RC2.4.5 정렬
- Counter Reconciled PASS
- Results = Probe + Timeout + Network partial + Failed + Skipped
- New PASS transition만 Promoted에 포함
- QA Timeout은 /errors 신규 기록에서 제외
