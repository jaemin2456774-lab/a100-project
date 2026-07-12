# A100 V92.3 Dashboard & Action UX Engine

V92.2의 기존 데이터와 schema 1을 유지하면서 Telegram 출력과 사용 흐름을 개선한 버전입니다.

## 핵심 명령
- `/dashboard BTC`: Score, Confidence, Precision Gate, Risk, Action, Scenario, Entry, TP, SL을 한 화면에 표시
- `/final BTC`: 핵심 최종 판단만 간결하게 표시
- `/coach BTC`: 현재 행동, 대기 조건, 취소 조건을 행동 중심으로 표시
- `/topscore`: 등급, Confidence, Gate, Risk, Action을 함께 표시
- `/help core|precision|paper|system`: 카테고리별 도움말

## 데이터 호환
- 상태 파일: `a100_v91_paper_state.json`
- schema: `1`
- 기존 Paper, Shadow, Scenario, Meta, Similarity, Audit, Review, Memory, Confidence History 유지

## 설치 후 권장 테스트
```
/health
/help
/help core
/help precision
/help paper
/help system
/commands V92
/dashboard BTC
/final BTC
/coach BTC
/topscore
/paper
/shadow
/market
/meta
/ev
/ai
/confidence_history BTC
/memory
/review
```
