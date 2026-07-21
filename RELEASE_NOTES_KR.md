# A100 V116.2 RC2.4.4 릴리스 노트

## 목적
RC2.4.3 Safe QA Runner에서 확인된 개별 명령 Timeout을 Runner 전체 장애와 분리하고, 각 Probe 직후 Command Certification을 재평가합니다.

## 변경 사항
- 명령별 Timeout 정책: 기본 15초, 느린 조회 명령 30초
- `asyncio.TimeoutError` 및 Telegram `TimedOut`을 `TIMEOUT / PARTIAL`로 격리
- `NetworkError`를 `NETWORK_PARTIAL`로 격리
- Timeout/Network Partial은 V88 시스템 오류로 기록하지 않고 Runner 진단 Trace에 기록
- 예상하지 못한 예외만 `FAILED` 및 `/errors` 대상
- `PROBED`, `SLOW`, `TIMEOUT`, `NETWORK_PARTIAL`, `FAILED`, `SKIPPED` 분류 저장
- 각 Probe 직후 Ledger refresh 및 Command Matrix snapshot 재생성
- 실측 5개 증거가 모두 충족된 명령은 즉시 PASS 승격
- Runner Status에 Timeout, Slow, Network Partial, Promoted, 마지막 결과/지연 표시

## 불변 사항
Registry 341/341, Runtime First, Strict Read Only, Gate/Threshold, Learning, Paper/Live 주문 경로는 변경하지 않습니다.
