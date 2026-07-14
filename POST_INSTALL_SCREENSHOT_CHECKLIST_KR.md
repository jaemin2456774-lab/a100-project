# RC4.9.20 설치 후 캡처 체크리스트

명령은 한 메시지에 몰아서 보내지 말고 아래 순서대로 개별 실행합니다.

/version
/versionaudit
/commandcert
/performanceaudit
/runtimehealth
/releasegate
/pipelinetrace
/dashboard
/status

일반 명령 확인 후 정밀 인증은 한 번만 실행합니다.

/commandcert deep
/versionaudit

확인 기준:
- Version 116.0-RC4.9.20
- Registry / Handler / Help 341/341
- Route Certification 341/341
- Errors 0
- Workers 2 이상
- Reused 341 / Rescanned 0 (코드 변경이 없는 Deep 재검사 기준)
- Schema 1 / Paper 20 / Shadow 60 / Live OFF
