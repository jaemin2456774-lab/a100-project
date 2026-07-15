# S2.18.2 설치 안내

1. 현재 프로젝트와 `/data` 볼륨을 그대로 유지합니다.
2. ZIP의 `main.py`만 프로젝트 루트에 덮어씁니다.
3. 데이터, 환경변수, 설정 파일은 삭제하거나 초기화하지 않습니다.
4. Railway 재배포 후 시작 로그를 확인합니다.

정상 로그:
- A100 V116.0-LTS-S2.18.2 ... worker running
- A100 V91 startup commands: 341
- A100 S2.18.2 unified state prewarm: PASS 또는 WARMING
- A100 V91 startup preflight: PASS

확인 명령:
/version
/versionaudit
/status
/status
/runtimehealth
/runtimehealth
/releasegate
/releasegate
/ltscertification
/pipelinetrace
/commandperformance
/errors

동일 Snapshot ID + Unified Hash에서는 Runtime Score, Memory Health, Evidence와 Gate 값이 동일해야 합니다.
Snapshot ID가 변경되면 실제 데이터 변화에 따라 점수가 달라질 수 있습니다.
