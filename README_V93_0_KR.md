# A100 V93.0 AI Intelligence Core

기준 버전: V92.8 Command Integrity & Version Sync

## 핵심 변경
- `v930_ai_intelligence_core.py` 독립 모듈 추가
- 시장 국면 분류: BREAKOUT / TREND / RANGE / PANIC / RECOVERY
- 국면별 엔진 가중치 자동 조정
- 엔진별 최종 판정 기여도 표시
- 자연어 AI 판단 설명
- 최근 50/100/300건 성과 요약
- 기존 schema 1 및 `a100_v91_paper_state.json` 유지
- 실주문 경로 추가 없음

## 신규 명령
- `/aicore BTC`: V93 AI 핵심 판단
- `/aistatus`: 코어 및 학습 상태
- `/aiperformance`: 최근 50/100/300건 성과
- `/aiweights BTC`: 엔진 가중치
- `/aimemory`: 학습 메모리

기존 `/ai` 명령은 회귀 방지를 위해 Paper Candidates 별칭으로 유지됩니다.
