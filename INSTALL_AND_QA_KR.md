# V117.0 RC5 설치 및 QA

1. 기존 main.py를 백업합니다.
2. 이 패치의 main.py로 교체 후 기존 requirements로 배포합니다.
3. 검증 순서:

```text
/version
/buildinfo
/versionaudit
/commandcert status
/commandcert batch 1 run
/commandcert status
/commandcert
/commandmatrix
/trustgate
/errors
```

기대값: Registry 341/341, QA/Unknown 신규 증가 0, 안전한 Promotion만 append, 격리 명령은 MANUAL_REVIEW/PARTIAL 유지, Trust Historical Integrity 100%.
