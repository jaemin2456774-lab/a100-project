# LTS-FC1 설치 후 Telegram 확인 순서

아래 명령을 순서대로 실행하여 화면을 캡처해 주세요.

1. `/version`
2. `/status`
3. `/commandcert`
4. `/commandcert deep`
5. `/performanceaudit`
6. `/runtimehealth`
7. `/releasegate`
8. `/versionaudit`
9. `/dashboard`
10. `/pipelinetrace`

## 필수 확인값
- Version: `A100 V116.0-LTS-FC1 FINAL CERTIFICATION SPRINT 1`
- Version Source: `Single`
- Registry / Handler / Help / Output: `341/341`
- Regression Risk: `NONE`
- Release Freeze: `ACTIVE`
- LTS Readiness: `CERTIFIED`
- Schema: `1`
- Paper: `20`
- Shadow: `60`
- Live: `OFF`
- `/status`에서 `<b>` 같은 HTML 태그가 그대로 노출되지 않아야 합니다.
- `/performanceaudit`에 Recent Window / Since Startup / Lifetime이 모두 표시되어야 합니다.
