# LTS FC1.2 설치 후 캡처 순서

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

## 집중 확인
- `/performanceaudit`: 30표본 미만이면 `WARMING UP`
- `/commandcert`: 단계별 ms, %, `Longest Stage`
- `/dashboard`: `AI LEARNING TARGET GATES`와 `SYSTEM RELEASE READINESS` 분리
- Footer: `Sprint 1 CERTIFIED`, `FC1.2 Product Polish`, `Ready for Sprint 2`
