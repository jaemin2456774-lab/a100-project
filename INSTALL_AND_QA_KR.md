# A100 V118.0 RC3.4 설치 및 검수

`main.py`를 기존 저장소에 덮어쓴 뒤 Railway에서 재배포한다.

## 검수 순서
아래 각 쌍은 60초 이내 연속 실행한다.

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

## 정상 기준
- Registry 341/341
- Architecture Guard PASS
- Version Audit PASS
- 각 캐시 대상 두 번째 호출 `Cache HIT`
- `/performance`에서 Hits 증가, Last HIT, TTL 양수 표시
- 동일 Projection 의미 상태에서는 stable hash 유지
