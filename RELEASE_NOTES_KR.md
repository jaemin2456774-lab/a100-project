# A100 V118.0 RC1 LTS Foundation

## 목적
기존 V117 RC6의 SSOT·Immutable Ledger·Safe Runner를 보존하면서 조회 응답성과 구조 회귀 감지를 강화합니다.

## 변경 사항
- BootManager 단일 초기화 계층
- Architecture Guard: Registry 341, Projection/Ledger/Historical 핵심 계약 확인
- Projection Hash 기반 Zero-Rebuild Render Cache
- 명령별 Performance Budget 및 P50/P95/Cache Hit 계측
- 이벤트 payload에 trace_id와 platform_version 자동 부여
- Trust 출력에 preserved baseline과 post-baseline delta 구분
- 기존 `/profiling` 또는 `/performance` 슬롯을 재사용하여 Registry 증가 없음

## 비변경 사항
- Registry 341/341
- Runtime First / Strict Read Only
- Historical 삭제·정규화 없음
- Gate/Threshold/Order mutation 없음
- Safe QA Runner와 slow queue 유지
- Live Trading OFF
