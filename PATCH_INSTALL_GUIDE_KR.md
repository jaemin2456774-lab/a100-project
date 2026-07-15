# A100 V116.0 LTS S2.17.31 설치 및 검수 안내

## 설치
1. Railway/GitHub의 기존 프로젝트에 ZIP 내부 파일을 동일 경로로 덮어씁니다.
2. `/data`, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
3. 재배포 후 재시작 루프 없이 Polling이 유지되는지 확인합니다.

## 정상 시작 로그
```text
A100 V116.0-LTS-S2.17.31 LTS FINAL UNIFIED DASHBOARD & GAUGE POLISH worker running...
A100 V91 startup commands: 341
A100 V91 startup preflight: PASS · warnings 0 (S2.17.31)
A100 S2.17.31 live runtime worker: ACTIVE · interval 2.0s
A100 S2.17.31 evidence change detector: ACTIVE · check interval 30.0s
```

## 공식 설치 후 검수 순서
```text
/version
/versionaudit
/status
/status
/runtimehealth
/runtimehealth
/releasegate
/releasegate
/dashboard
/dashboard
/ltscertification
/pipelinetrace
/commandperformance
/errors
```

## 캡처 필수 항목
1. Railway 시작 로그 전체
2. `/version`, `/versionaudit`
3. `/status` 2회
4. `/runtimehealth` 2회
5. `/releasegate` 2회
6. `/dashboard` 2회
7. `/ltscertification`
8. `/pipelinetrace`
9. `/commandperformance`
10. `/errors`

## 합격 기준
- 버전 출력이 모두 S2.17.31
- Registry/Routes 341/341
- Runtime source LIVE_RUNTIME
- Worker freshness PASS
- Telegram Strict Read Only
- Snapshot SUPPORTING EVIDENCE ONLY
- 두 번째 호출에서도 Runtime/Gate 값의 내부 일관성 유지
- `/dashboard`에 Runtime, 5개 Gate, 72H milestones 표시
- 신규 Timeout, RecursionError, RuntimeError 없음
