# RC4.9.18 설치 후 필수 캡처 체크리스트

아래 순서대로 Telegram 명령을 실행하고 전체 화면을 캡처해 보내주세요.

```text
/version
/help
/commands
/versionaudit
/commandcert
/commandcert deep
/performanceaudit
/releasegate
/runtimehealth
/pipelinetrace
/strategytrust
/outcomequality
/memoryhealth
/intelligencescore
/dashboard
/status
```

## 확인 기준
- 모든 헤더가 `116.0-RC4.9.18`로 표시
- Registry / Handler / Help가 `341/341`
- Read-only Route Certification `341/341`, Errors `0`
- Preflight `PASS`
- Schema 1 / Paper 20 / Shadow 60 / Live OFF
- `/help`, `/commands` 장문 출력이 중간에서 잘리지 않음
- `/performanceaudit`의 Recent Samples가 시간순 최근 데이터로 표시
- Release Gate, Dashboard, Pipeline Trace의 Snapshot/Revision 불일치가 없음

실제 Telegram Live Evidence는 명령을 실행할수록 누적되므로 `/commandcert`의 Structural Certification과 별도로 확인합니다.
