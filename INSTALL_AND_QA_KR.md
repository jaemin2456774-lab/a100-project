# 설치 및 QA

기존 저장소에 패치 파일을 덮어쓴 뒤 Railway에서 재배포합니다.

## 필수 확인
/version
/buildinfo
/versionaudit
/commandcert
/commandcert
/commandmatrix
/commandmatrix
/trustgate
/trustgate
/intelligencescore
/intelligencescore
/performance
/errors

## 기대 결과
- Registry 341/341
- Architecture Guard PASS
- Version Audit PASS
- Boot Phases에 recovery_core / projection_warmup / trust_warmup 표시
- 동일 명령 두 번째 호출 Cache HIT
- /performance에 Hits와 Misses가 분리 표시
