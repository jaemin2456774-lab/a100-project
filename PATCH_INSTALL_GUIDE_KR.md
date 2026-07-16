# S2.17.48 Railway 패치 설치 안내

1. 기존 프로젝트 루트의 `main.py`를 백업합니다.
2. ZIP의 `main.py`를 프로젝트 루트에 덮어씁니다.
3. `/data`, Railway Volume, 환경 변수, DB 파일은 삭제하거나 변경하지 않습니다.
4. GitHub 커밋 후 Railway에서 새 Deployment를 실행합니다.
5. 시작 로그에서 S2.17.48과 Registry 341, preflight PASS를 확인합니다.

## 배포 후 검증 명령
```
/version
/versionaudit
/commandcert
/releasegate
/releasegate detail
/ltsreadiness
/ltsreadiness detail
/runtimehealth
/errors
```

## 최종 CERTIFIED 조건
- Mandatory Gates 5/5
- Persisted 72H 100%
- Structural Integrity PASS
- Registry 341/341
- Recent Errors 0
