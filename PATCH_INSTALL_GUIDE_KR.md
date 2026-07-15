# S2.17.28 패치 설치 안내

1. 현재 Railway 프로젝트와 `/data` 볼륨을 유지합니다.
2. ZIP의 파일을 기존 프로젝트 루트에 덮어씁니다.
3. 환경변수와 설정 파일은 수정하지 않습니다.
4. Railway를 재배포합니다.

## 정상 시작 로그

```text
A100 V116.0-LTS-S2.17.28 REAL-TIME MONITORING STABILIZATION worker running...
A100 V91 startup commands: 341
A100 V91 startup preflight: PASS
A100 S2.17.28 live runtime worker: ACTIVE · interval 2.0s
A100 S2.17.28 certification evidence refresh: ACTIVE · interval 30.0s
```

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
/commandperformance
/errors
```

## 합격 기준

- Runtime source: `LIVE_RUNTIME`
- Monitor worker: `RUNNING · FRESH`
- Telegram isolation: `PASS · STRICT READ ONLY`
- User-path scans/gates: `DISABLED`
- 동일 Evidence 갱신 주기 안에서 Runtime Score와 Gate 값 일치
- Registry 341/341
- 신규 RuntimeError 및 Timeout 없음

실제 인증 데이터가 부족하면 Gate가 BLOCKED로 표시되는 것이 정상입니다.
