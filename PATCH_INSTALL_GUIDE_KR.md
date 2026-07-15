# S2.17.29 설치 안내

1. 기존 Railway 프로젝트와 `/data` 볼륨을 그대로 유지합니다.
2. ZIP의 `main.py`만 프로젝트의 기존 `main.py`에 덮어씁니다.
3. 환경변수와 설정 파일은 수정하지 않습니다.
4. 재배포 후 시작 로그에서 아래를 확인합니다.

```text
A100 V116.0-LTS-S2.17.29 ... worker running...
A100 V91 startup commands: 341
A100 V91 startup preflight: PASS
A100 V91 registered commands: 341
```

5. 다음 명령을 순서대로 실행합니다.

```text
/version
/versionaudit
/runtimehealth
/runtimehealth
/releasegate
/releasegate
/status
/commandperformance
/errors
```

Gate 점수가 기준 미달로 BLOCKED인 것은 정상이며 임의 PASS 처리하지 않습니다.
