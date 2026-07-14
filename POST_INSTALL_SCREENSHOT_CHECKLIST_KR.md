# RC4.9.19 설치 후 캡처 체크리스트

아래 명령은 한 메시지에 몰아서 보내지 말고 순서대로 개별 실행하십시오.

1. `/version`
2. `/versionaudit`
3. `/commandcert`
4. `/performanceaudit`
5. `/runtimehealth`
6. `/releasegate`
7. `/pipelinetrace`
8. `/dashboard`
9. `/status`

정밀 재인증은 일반 점검이 끝난 뒤 한 번만 실행합니다.

10. `/commandcert deep`
11. `/versionaudit`

확인 기준:
- Version: 116.0-RC4.9.19
- Registry/Handler/Help: 341/341
- Route Certification: 341/341, errors 0
- 일반 `/versionaudit`와 `/commandcert`는 빠르게 응답
- `/commandcert deep` 실행 중에도 다른 Telegram 명령이 멈추지 않음
- Deep 완료 후 Certification Cache age가 갱신됨
- Schema 1, Paper 20, Shadow 60, Live OFF
