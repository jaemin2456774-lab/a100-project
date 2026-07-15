# S2.17.34 패치 설치 안내

기준 버전: **A100 V116.0 LTS S2.17.33**

1. Railway 또는 GitHub의 현재 `main.py`를 백업합니다.
2. 패치 ZIP의 `main.py`를 프로젝트 루트에 덮어씁니다.
3. 데이터 폴더, 환경변수, 설정 파일은 변경하거나 삭제하지 않습니다.
4. 재배포 후 시작 로그에서 아래 항목을 확인합니다.

```text
A100 V116.0-LTS-S2.17.34 FINAL POLISH & PRODUCTION READINESS worker running...
A100 V91 startup commands: 341
A100 V91 startup preflight: PASS
A100 S2.17.34 live runtime worker: ACTIVE
A100 S2.17.34 evidence change detector: ACTIVE
```

## 설치 후 캡처 명령

아래 순서대로 실행해 주세요.

```text
/version
/status
/dashboard
/dashboard
/releasegate
/ltscertification
/runtimehealth
/versionaudit
/pipelinetrace
/errors
```

특히 `/dashboard`는 두 번 연속 실행하여 첫 응답과 캐시 응답 속도를 비교합니다.
