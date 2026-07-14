# 설치 후 확인 순서

1. `/version`
2. `/status`
3. `/runtimehealth`
4. `/performanceaudit`
5. `/dashboard`
6. `/commandcert`
7. `/commandcert deep`
8. `/releasegate`
9. `/versionaudit`
10. `/pipelinetrace`

중점 확인:
- `/version`: 버전/빌드 정보 전용 출력
- `/status`: Engineering Certification과 AI Learning Targets 분리
- Runtime: Elapsed / Remaining / Progress 분리
- Warm-up: Samples / Runtime 기준 표시
- `/runtimehealth`: 30m~72h Timeline과 Recovery Rate
- `/dashboard`: Certification Stage / Next Stage
