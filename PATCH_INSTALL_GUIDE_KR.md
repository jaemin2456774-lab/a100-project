# S2.17.51 패치 설치 안내

1. Railway 연결 GitHub 저장소의 프로젝트 루트 `main.py`를 패치 파일로 덮어씁니다.
2. `/data`, DB, 환경변수 및 Railway Volume은 변경하거나 삭제하지 않습니다.
3. 커밋·푸시 후 Railway 배포 로그에서 S2.17.51 시작 문구를 확인합니다.
4. Telegram에서 검증 명령을 순서대로 실행합니다.

```text
/version
/help
/help signals
/help god
/help sniper
/help ultimate
/commands god
/versionaudit
/commandcert
/runtimehealth
/errors
```

정상 로그:
```text
A100 V116.0-LTS-S2.17.51 FINAL HELP CONTRACT POLISH & ALIAS INTEGRITY worker running...
A100 V91 registered commands: 341
A100 V91 startup preflight: PASS · warnings 0 (S2.17.51)
A100 S2.17.51 final help contract: PASS · 341/341
```
