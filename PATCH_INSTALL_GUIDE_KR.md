# S2.17.39 패치 설치 안내

1. 기존 프로젝트의 `main.py`를 백업합니다.
2. ZIP의 `main.py`를 프로젝트 루트에 덮어씁니다.
3. 기존 `/data`, 환경 변수, 설정 및 DB는 변경하지 않습니다.
4. GitHub 커밋 후 Railway에서 새 배포를 실행합니다.
5. 로그에서 아래 내용을 확인합니다.

```text
A100 V116.0-LTS-S2.17.39 STARTUP RECOVERY & SELF-HEALING CERTIFICATION worker running...
A100 V91 startup preflight: PASS
A100 V91 registered commands: 341
A100 V91 dispatcher count: 1
```

필요 시 다음 로그가 한 번 표시될 수 있습니다.

```text
A100 S2.17.39 startup auto-recovered routes: version,versionaudit
```

이는 오류가 아니라 이전 릴리스 핸들러를 현재 릴리스로 자동 교체했다는 증거입니다.

배포 후 확인 명령:

```text
/version
/versionaudit
/commandcert
/status
/runtimehealth
/errors
```
