# A100 V118.0 RC3.2 릴리즈 노트

Build ID: `V118.0-RC3.2-20260722-AUTHORITATIVE-STARTUP-IDENTITY-LOG-UNIFICATION-01`

## 수정 사항

- Railway 시작 로그의 authoritative identity를 V118.0 RC3.2로 단일화했습니다.
- `V117.0-RC6 worker running`, 과거 `BUILD_ID=...`, V116/V90/V92 고정 버전 배너를 숨깁니다.
- 레거시 초기화와 worker 기능은 제거하지 않고 그대로 실행합니다.
- 일반 운영 로그와 오류 로그는 계속 출력합니다.
- Registry 341/341, Runtime First, Strict Read Only, Live Trading OFF를 유지합니다.

## 기대 시작 로그

```text
A100 V118.0 RC3.2 runtime identity: CURRENT
A100 V118.0 RC3.2 build: V118.0-RC3.2-20260722-AUTHORITATIVE-STARTUP-IDENTITY-LOG-UNIFICATION-01
A100 V118 architecture guard: PASS registry=341
A100 V118 query kernel: PROJECTION HASH CACHE · PERFORMANCE SAMPLE VERDICT
A100 V118.0 RC3.2 live trading: OFF
```
