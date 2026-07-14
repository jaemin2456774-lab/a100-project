# RC4.9.17 설치 후 필수 캡처 체크리스트

아래 순서대로 Telegram에서 실행하고 전체 출력 화면을 캡처합니다.

## 1. 버전 및 Startup 무결성
/version
/versionaudit

확인: 모든 화면 RC4.9.17, Schema1, Paper20, Shadow60, Live OFF, Preflight PASS.

## 2. Command Certification 및 순환 Probe
/commandcert
/commandcert deep
/commandcert deep
/commandcert deep

확인: Registry/Handler/Help 341/341, Background dry route probe가 50개씩 증가, 오류 0.

## 3. 출력 형식
/commandcert warn engine 10
/commandcert warn output 10
/commandcert warn repository 10
/commandcert warn runtime 10

확인: `<b>` 같은 HTML 태그가 노출되지 않고 PARTIAL_ENGINE 같은 내부 상태명이 노출되지 않음.

## 4. Dynamic Help와 Command Index
/help
/commands

확인: 헤더가 RC4.9.17이며 RC4.2 문자열이 없음, 활성 명령 341개.

## 5. 동일 Snapshot 및 Release Gate
/dashboard BTC
/status
/releasegate

확인: 점수들이 같은 시점 기준으로 일치, Priority Recommendation 출력, Paper20/Shadow60/Live OFF.

## 6. 성능 및 연속 실행
아래 5개를 한 메시지에 줄바꿈하여 실행:
/dashboard BTC
/dashboard ETH
/status
/releasegate
/performanceaudit

그 다음 단독 실행:
/performanceaudit

확인: Recent Avg/P95와 All-time Avg/P95가 분리되고 Batch Backlog는 등급에서 제외됨.

## 7. Railway 로그
배포 직후 다음 로그 구간 캡처:
- Preflight PASS
- Dispatcher Ready
- Polling Started
- Scheduler Started
- Health/Watchdog
- Startup Complete
- ERROR, Exception, Traceback, Timeout, SIGTERM, Recovery 발생 시 해당 전후 로그
