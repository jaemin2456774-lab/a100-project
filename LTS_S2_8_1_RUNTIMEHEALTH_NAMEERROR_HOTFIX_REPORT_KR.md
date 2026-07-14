# A100 V116.0 LTS-S2.8.1 Runtimehealth NameError Hotfix

## 현상
`/runtimehealth`가 기본 인증 본문을 전송한 뒤 `NameError` 오류 메시지를 추가로 출력했습니다.

## 원인
S2.8 Runtime Trend 계산에서 존재하지 않는 `_v1160_s26_load_evidence()` 함수를 호출했습니다. 실제 Evidence 로더는 `_v1160_s24_load_evidence()`입니다.

## 수정
- 잘못된 함수 참조를 실제 Evidence 로더로 교체했습니다.
- `/runtimehealth` 전체 핸들러를 직접 호출하는 회귀 테스트를 추가했습니다.
- Registry 341/341, Schema 1, Paper 20, Shadow 60, Live OFF를 유지했습니다.
