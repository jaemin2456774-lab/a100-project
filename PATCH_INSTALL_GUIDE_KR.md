# S2.17.47 패치 설치 안내

1. Railway에 연결된 저장소의 프로젝트 루트에 ZIP의 변경 파일을 덮어씁니다.
2. `/data`, 데이터베이스, 환경 변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
3. 변경 내용을 커밋하고 Railway에서 새 Deployment를 실행합니다.
4. 시작 로그에서 `S2.17.47`, Registry 341, startup preflight PASS를 확인합니다.

## 배포 후 검증
```
/version
/versionaudit
/commandcert
/ltsreadiness
/ltsreadiness detail
/runtimehealth
/errors
```

`/evidence`는 동결된 341개 Registry에 포함되지 않으므로 더 이상 지원 명령으로 안내하지 않습니다. Evidence 성숙도와 72시간 인증 정보는 `/ltsreadiness detail`에서 확인합니다.
