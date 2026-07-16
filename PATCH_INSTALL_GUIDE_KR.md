# S2.17.46 패치 설치 안내

1. Railway에 연결된 GitHub 저장소의 기존 `main.py`를 패치 ZIP의 `main.py`로 덮어씁니다.
2. 기존 `/data`, 데이터베이스, 환경 변수와 Railway Volume은 삭제하거나 초기화하지 않습니다.
3. 변경 파일을 커밋하고 Railway에서 새 Deployment를 실행합니다.
4. 시작 로그에서 `S2.17.46`, 등록 명령 341개, dispatcher 1개, startup preflight PASS를 확인합니다.

## 배포 후 확인 명령
```text
/version
/versionaudit
/commandcert
/coach
/coach detail
/evidence
/evidence detail
/ltsreadiness
/ltsreadiness detail
/runtimehealth
/errors
```

Authoritative PASS는 5/5 Mandatory Gates, persisted 72H 100%, structural PASS를 모두 충족해야 합니다.
