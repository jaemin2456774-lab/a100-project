# S2.17.45 패치 설치 안내

1. Railway가 사용하는 GitHub 배포 브랜치의 프로젝트 루트에 `main.py`를 덮어씁니다.
2. 기존 `/data`, 데이터베이스, Railway Variables 및 볼륨은 삭제하거나 초기화하지 않습니다.
3. 변경 파일을 커밋·푸시한 뒤 Railway 새 Deployment를 확인합니다.
4. 시작 로그에서 S2.17.45, Registry 341, startup preflight PASS를 확인합니다.
5. Telegram에서 다음을 순서대로 실행합니다.

```text
/version
/versionaudit
/commandcert
/evidence
/coach
/coach detail
/ltsreadiness
/ltsreadiness detail
/runtimehealth
/errors
```

`DISPLAY-ONLY MATURITY`는 관측용이며 Release Gate PASS를 대체하지 않습니다.
