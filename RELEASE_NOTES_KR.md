# A100 V118.0 RC3.4 릴리즈 노트

## 목적
RC3.3에서 동일한 화면상 Projection Hash에도 Render Cache가 반복 MISS하던 문제를 수정한다.

## 변경 사항
- 인증 의미값만 사용하는 Stable Semantic Projection Hash 도입
- timestamp, trace ID, runtime freshness 등 변동 필드를 캐시 키에서 제외
- 명령 이름을 소문자 및 슬래시 제거 형식으로 정규화
- Render Cache 조회 키와 저장 키를 동일 함수에서 생성
- 동일 명령의 이전 Projection 캐시만 bounded 제거
- `/performance`에 Last HIT/NOT_FOUND/EXPIRED, Entries, TTL 표시
- Rule Engine 표시를 `v118.ssot.rule.v1`로 통일

## 유지 사항
- Registry 341/341
- Runtime First / Strict Read Only
- Ledger Append Only
- Live Trading OFF
- 기존 데이터 및 환경변수 보존
