A100 V90.2 BOOT & COMMAND RELIABILITY ENGINE

현재 Railway 로그의 핵심 오류:
NameError: name 'commands90_cmd' is not defined

정확한 원인:
V90_COMMAND_REGISTRY 딕셔너리를 만들 때 Python이 commands90_cmd를 즉시 평가합니다.
그런데 기존 V90/V90.1 파일은 commands90_cmd를 정의하기 전에 레지스트리를 만들었습니다.
그래서 Telegram polling에 진입하기도 전에 main.py 로딩 단계에서 컨테이너가 종료됐습니다.

V90.2 수정 내용:
- commands90_cmd
- legacycheck90_cmd
- health90_cmd
- selfcheck90_cmd
- v90_cmd
- help90_cmd

위 6개 신규 함수가 모두 정의된 뒤에 V90_COMMAND_REGISTRY를 생성하도록 순서를 바로잡았습니다.

유지된 기능:
- 기존 104개 명령
- 단일 명령 디스패처
- 여러 줄 명령 처리
- 대기 중 Telegram 명령 보존
- 명령별 오류 격리
- 180초 명령 타임아웃

검증:
- Python 문법 검사 통과
- AST 파싱 통과
- 레지스트리 생성 시점의 미정의 콜백 0개
- 단일 __main__ 실행점 확인
- 단일 디스패처 유지 확인
- drop_pending_updates=False 유지 확인

배포 후 정상 로그:
A100 V90.2 BOOT & COMMAND RELIABILITY ENGINE worker running...
A100 V90.2 registered commands: 104
A100 V90.2 dispatcher count: 1
A100 V90.2 registry validation: OK
A100 V90.2: Telegram single polling started

주의:
현재 검증 환경에는 apscheduler 같은 배포 의존성이 설치되어 있지 않아
전체 import 실행 테스트는 하지 못했습니다.
대신 이번 실제 실패 원인인 함수 정의 순서와 모든 레지스트리 콜백을 AST로 검사했습니다.
