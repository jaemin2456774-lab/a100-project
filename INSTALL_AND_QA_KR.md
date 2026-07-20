# Railway 설치 및 QA

기존 저장소의 main.py만 덮어쓴 후 Railway에서 재배포합니다. /data, 환경변수, 기존 학습 데이터는 삭제하지 않습니다.

배포 후 실행 순서:

/version
/buildinfo
/runtimehealth
/versionaudit
/papershadow
/coverageplan
/papershadowperformance
/papershadowperformance
/errors

확인 기준:
- 모든 제품 헤더와 Build ID가 V116.2 RC1.4로 표시
- S59.x는 Implementation/Module provenance가 아닌 현재 Running Identity로 표시되지 않음
- 두 번째 /papershadowperformance의 Snapshot Read가 매우 작고 Handler Total 2000ms 이하
- Lifetime Outcome/Attribution/Performance 값이 서로 정합
- Registry 341/341, Errors 0, Gate mutation NONE
