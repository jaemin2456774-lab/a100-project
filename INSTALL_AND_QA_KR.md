# Railway 설치 및 QA

## 설치
기존 Railway 저장소의 `main.py`만 이 패치의 `main.py`로 덮어쓴 뒤 커밋·푸시하여 재배포합니다. `/data`와 환경변수는 삭제하거나 초기화하지 않습니다.

## 부팅 로그 확인
다음 3줄이 현재 식별자로 표시되는지 확인합니다.

```text
A100 V116.2 RC1.1 runtime identity: CURRENT
A100 V116.2 RC1.1 build: V116.2-RC1.1-20260720-PERFORMANCE-IDENTITY-HARDENING-01
A100 V116.2 RC1.1 live trading: OFF
```

다음 과거 식별자 배너는 더 이상 표시되지 않아야 합니다.
- V116.1 DEV S59.7.2 continuity/live trading
- V90.2 webhook/auto alert/polling startup
- V92.5 learning report loop startup
- V116.0-LTS-S2.17.4 snapshot warmup

기능 자체는 제거하지 않고 배너만 억제했습니다.

## Telegram 검증 순서
```text
/version
/buildinfo
/papershadowperformance
/papershadowperformance
/runtimehealth
/versionaudit
/papershadow
/commandcert
/errors
```

`/papershadowperformance`는 연속 2회 실행합니다. 첫 실행은 revision cache MISS, 두 번째는 HIT가 정상입니다.

## 합격 기준
- Version/Build ID가 V116.2 RC1.1로 일치
- Registry 341/341
- `/papershadowperformance` Handler/Route/Runtime/Evidence/Learning/Output PASS
- 두 번째 실행 latency 2000ms 이하 목표
- Revision Cache hit 증가
- Runtime/Version Audit PASS
- System Error 0
- Threshold/Gate/Live mutation NONE
