# S54 Railway 설치 안내

1. 기존 S53 저장소를 백업합니다.
2. 패치의 main.py만 기존 main.py에 덮어씁니다.
3. 기존 /data, 환경변수, 설정 파일은 변경하지 않습니다.
4. Railway에 배포하고 Startup 로그에서 S54 connectivity audit PASS 및 registered commands 341을 확인합니다.

## 배포 후 캡처 명령

/version
/status
/runtimehealth
/sniper
/sniper detail
/ultimate
/ultimate detail
/evidence
/releasegate
/releasegate detail
/errors

핵심 확인값은 Runtime Connectivity의 Connected N/16, Coverage, Nested recovery, Missing입니다.
