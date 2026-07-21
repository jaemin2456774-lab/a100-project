# A100 V117.0 RC2 릴리스 노트

## 목표
V117 RC1에서 확인된 느린 기동과 반복 Identity 로그를 제거한다.

## 핵심 변경
- 역사적 RC `main()` wrapper 연쇄 호출 제거
- 최종 Runtime main으로 단일 진입
- Identity, Route, Recovery, Banner 프로세스당 1회 실행
- Certification Projection과 Trust 계산을 최초 명령 호출까지 지연
- Startup Event를 startup session + payload hash로 중복 방지
- Event Ledger chain head를 메모리에 캐시하여 매 append 시 전체 JSONL 재독 제거
- Registry 341/341 및 기존 명령 유지

## 비변경 영역
- Trading Gate / Threshold / Orders
- Learning / Attribution producer
- Historical data
- Safe QA mutation firewall
- Live Trading OFF
