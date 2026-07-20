# 설치 및 QA

기존 프로젝트에 `main.py`를 덮어쓰고 Railway를 재배포합니다. `/data`와 환경변수는 유지합니다.

## 검증 순서
```text
/version
/buildinfo
/runtimehealth
/versionaudit
/commandcert
/commandcert batch 1
/commandcert batch 1 run
/commandcert status
/commandcert
/commandmatrix
/errors
```

전체 Safe 배치는 `/commandcert autorun`으로 시작하고 `/commandcert stop`으로 중지합니다. 자동 검수는 기존 Coverage Planner가 SAFE로 분류한 조회 명령만 실행합니다.
