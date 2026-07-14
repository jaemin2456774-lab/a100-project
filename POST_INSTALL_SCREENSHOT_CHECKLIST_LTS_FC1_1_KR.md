# LTS-FC1.1 설치 후 Telegram 확인 순서

아래 순서대로 실행 후 캡처해 주세요.

1. `/version`
2. `/status`
3. `/commandcert`
4. `/commandcert deep`
5. `/performanceaudit`
6. `/dashboard`
7. `/runtimehealth`
8. `/releasegate`
9. `/versionaudit`
10. `/pipelinetrace`

## 필수 확인값
- Version: `A100 V116.0-LTS-FC1.1 PRODUCT POLISH & CERTIFICATION`
- Engineering Baseline / Sprint 1.5 표시
- Registry / Handler / Help / Output: `341/341`
- Build Breakdown와 Evidence Summary 표시
- Recent Window / Since Startup / Lifetime 표시
- Release Readiness가 실측값으로 표시
- Regression Risk: `NONE`
- Release Freeze: `ACTIVE`
- Schema 1 / Paper 20 / Shadow 60 / Live OFF
- `<b>` 같은 HTML 태그가 일반 텍스트 화면에 노출되지 않을 것
