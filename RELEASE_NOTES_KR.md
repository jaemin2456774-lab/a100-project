# A100 V116.2 RC1.6 릴리스 노트

## 수정 목적
- RC1.5에서 유지된 Registry 344/341 회귀를 canonical 341 명령 집합으로 복구합니다.
- 부팅 중 legacy route installer가 성능 명령을 RC1.4 핸들러로 되돌리는 문제를 차단합니다.
- 첫 `/papershadowperformance` 호출의 저장소 읽기 지연을 줄이기 위해 read-only 사전 워밍을 추가합니다.

## 변경 내용
- `_v1161_s59755_exact_canonical_names()`를 authoritative registry membership source로 사용합니다.
- installer 실행 전후로 canonical 341 membership을 재확정합니다.
- `/papershadowperformance`를 모든 installer 경계 뒤 RC1.6 핸들러로 다시 고정합니다.
- 180초 bounded QA cache와 비동기 read-only prewarm을 적용합니다.
- RC1.5 atomic Binance cache save 수정은 그대로 유지합니다.

## 변경하지 않은 항목
- Entry Gate, Threshold, TP/SL, 전략 및 Learning/Attribution 저장 로직
- Shadow/Paper 데이터와 `/data` 경로
- Live Trading OFF, Runtime First, Strict Read Only
