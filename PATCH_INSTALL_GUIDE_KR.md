# S2.18.1 증분 패치 설치 안내

1. 기존 S2.18.0 프로젝트를 백업합니다.
2. 패치 ZIP의 `main.py`와 테스트·문서 파일만 기존 저장소에 덮어씁니다.
3. `/data`, Railway Volume, 환경변수 및 사용자 설정은 삭제하거나 초기화하지 않습니다.
4. Railway에서 재배포합니다.

## 정상 시작 로그

```text
A100 V116.0-LTS-S2.18.1 ... worker running...
A100 V91 startup commands: 341
A100 S2.18.1 unified state prewarm: PASS 또는 WARMING
A100 V91 startup preflight: PASS
```

`WARMING`은 시작 시 공유 Snapshot이 아직 준비되지 않았다는 뜻이며 오류가 아닙니다.

## 설치 후 확인 명령

```text
/version
/versionaudit
/status
/status
/runtimehealth
/runtimehealth
/releasegate
/releasegate
/ltscertification
/pipelinetrace
/commandperformance
/errors
```

동일 Snapshot ID에서는 Runtime Score, Memory Health, Evidence, 5개 Gate 값이 모든 명령에서 동일해야 합니다.
