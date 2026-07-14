# A100 V116.0 LTS-S2.2.1 Status Command Hotfix

## 수정 원인
`/status` 핸들러가 Recovery timestamp를 출력하면서 초기화되지 않은 지역 변수 `st`를 참조해 `NameError`가 발생했습니다.

## 수정 내용
- `status1160ltss21_cmd()`에서 `st = rv["state"]`를 명시적으로 초기화
- `/status` 실제 호출 회귀 테스트 추가
- Registry가 수정된 `/status` 핸들러를 가리키는지 검증
- 기능/Schema/Paper/Shadow/Live 정책 변경 없음

## 검증
- 신규 Hotfix 테스트 2/2 PASS
- 전체 테스트 83/83 PASS 출력 확인
- Registry 341/341 유지
