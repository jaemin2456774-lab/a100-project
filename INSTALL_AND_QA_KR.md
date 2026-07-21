# 설치 및 QA

1. ZIP을 기존 Railway 소스 루트에 덮어쓴다.
2. 기존 `/data` volume을 보존한다.
3. 재배포 후 startup 로그를 확인한다.

## 기대 startup 로그
아래 Identity 블록은 컨테이너당 한 번만 출력되어야 한다.

```text
A100 V117.0 RC2 runtime identity: CURRENT
A100 V117.0 RC2 build: ...
A100 V117 certification authority: SSOT RULE ENGINE · LAZY
A100 V117 immutable event ledger: APPEND ONLY · STARTUP DEDUPE
A100 V117.0 RC2 live trading: OFF
```

## 검증 명령
```text
/version
/buildinfo
/runtimehealth
/versionaudit
/commandcert
/trustgate
/errors
```

## 성능 검증
- 컨테이너 시작부터 `worker running`까지 시간을 RC1과 비교
- 동일 Identity 블록 반복 여부 확인
- `/commandcert` 첫 호출은 lazy projection 계산으로 후속 호출보다 느릴 수 있음
- 두 번째 `/commandcert` 및 `/trustgate`는 projection cache를 사용해야 함
