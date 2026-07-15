# S2.17.33 설치 안내

1. 현재 프로젝트와 `/data` 볼륨을 백업합니다.
2. ZIP의 파일을 프로젝트 루트에 덮어씁니다.
3. `/data`, 환경변수, 기존 설정 파일은 삭제하거나 초기화하지 않습니다.
4. Railway를 재배포합니다.
5. 시작 로그에서 S2.17.33, 341 commands, startup preflight PASS, live runtime worker ACTIVE를 확인합니다.

## 공식 검수 순서
/version
/versionaudit
/status
/status
/runtimehealth
/runtimehealth
/releasegate
/releasegate
/dashboard
/dashboard
/ltscertification
/pipelinetrace
/commandperformance
/errors

## 합격 기준
- Runtime authority LIVE MONITORING WORKER
- Telegram path STRICT READ ONLY
- Registry/Routes 341/341
- Recent errors 0
- 동일 Evidence에서 Gate 점수와 Trend 불변
- Live age와 heartbeat만 정상 갱신
- Snapshot은 SUPPORTING EVIDENCE ONLY
