# A100 V115.8 STRATEGY PERFORMANCE INTELLIGENCE DEVELOPMENT

V115.7을 안정 베이스로 전략별 실제 성과를 독립 추적하고, 충분한 표본과 세대 안정성이 확인된 전략만 Champion 후보로 추천하는 개발 버전입니다.

## 신규 명령
- `/strategyperformance`: 전략별 표본·승률·기대값·RR·PF·MDD·안정성
- `/championstability`: Champion 최소 표본 및 세대 안정성
- `/overfitaudit`: 과최적화 위험 점검
- `/ltsreadiness`: V116.0 LTS 준비도와 차단 사유

## 안전 원칙
- 기존 기능 및 학습 데이터 보존
- Paper 20 / Shadow 60 유지
- Live Trading OFF
- 자동 Paper 승격 금지
- Shadow → Paper → Stable 검증 유지
- V116.0 LTS 안정화 이후에만 자동매매 계층 개발
