# A100 V116.0 LTS RC4.9.1 Startup Integrity Hotfix

## 원인
RC4.9 최종 preflight가 RC4.7/RC4.8 preflight 결과를 계승하면서, 최신 버전에서 의도적으로 교체된 VersionManager 및 Telegram handler의 객체 동일성 검사를 과거 기준으로 계속 평가했습니다.
그 결과 기능 회귀가 아닌 정상적인 handler supersession을 실패로 오판하여 Railway 컨테이너 시작을 차단했습니다.

## 수정
- RC4.9 최종 preflight에서 아래의 폐기된 과거 객체 동일성/버전 고정 검사를 제거했습니다.
  - v1160_rc47_version_manager
  - v1160_rc47_pipeline_read_only
  - v1160_rc48_version_manager
  - v1160_rc48_ltscert
  - v1160_rc48_live_release_gate
- 활성 RC4.9 Registry, VersionManager, Release Gate, LTS Certification, Repository Audit, Health Score 검사는 그대로 유지했습니다.
- 실제 기능 및 데이터 무결성 검사는 완화하지 않았습니다.

## 검증
- Python compile: PASS
- v91_preflight(): PASS, failed=[]
- RC4.8/RC4.9 tests: 9 PASS
- Paper 20 / Shadow 60 / Live OFF / Schema 1 유지
