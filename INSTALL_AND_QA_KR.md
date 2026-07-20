# Railway 적용 및 QA

기존 프로젝트의 main.py를 이 패치의 main.py로 덮어쓴 뒤 Railway에서 재배포합니다.
기존 /data, 환경변수 및 설정은 삭제하지 않습니다.

## 검증 순서
/version
/buildinfo
/papershadowperformance
/papershadowperformance
/runtimehealth
/versionaudit
/papershadow
/coverageplan
/errors

## 기대 결과
- /version, /buildinfo, /runtimehealth, /versionaudit 모두 V116.2 RC1.2
- Lifetime Outcome/Attribution/Performance가 실제 durable store 수치로 표시
- 두 번째 /papershadowperformance에서 Revision Cache H1 이상
- Handler Total 2000ms 이하
- Registry 341/341, Error 0
