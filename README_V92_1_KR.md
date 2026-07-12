# A100 V92.1 Precision Intelligence Engine

V92.0의 AI Score 및 Explainable Confidence 결과를 재사용하여 판단 감사, 자동 복기, AI Memory, Precision Gate를 추가한 버전입니다.

## 신규 명령어
- `/audit BTC` : 현재 점수·신뢰도·가격·구성요소를 감사 기록으로 저장
- `/audit_top` : Precision Gate를 통과한 상위 후보 일괄 기록
- `/review` : 평가 시간이 지난 감사 기록을 현재 가격으로 복기
- `/memory` : 전체 및 Precision 통과군의 승률·평균수익·실패 원인 조회

기존 `/score BTC`에는 Precision Gate PASS/WAIT와 보류 원인이 함께 표시됩니다.

## Precision Gate
다음 기준을 동시에 검사합니다.
- A100 Score 및 Confidence 최소 기준
- 진입 단계 ENTRY/READY
- Meta SKIP 및 Risk HALT 차단
- Pattern, Liquidity, Market, Timing 최소 품질
- 엔진 구성점수 간 불일치 제한

기본값은 환경변수로 조정할 수 있습니다.
- `A100_PRECISION_MIN_SCORE=85`
- `A100_PRECISION_MIN_CONFIDENCE=78`
- `A100_REVIEW_HOURS=24`
- `A100_REVIEW_MOVE_PCT=0.5`
- `A100_AUDIT_DEDUP_HOURS=6`

## 데이터 호환성
기존 상태 파일과 schema를 변경하지 않습니다.
- 파일: `a100_v91_paper_state.json`
- schema: `1`

기존 데이터에 `decision_audits`, `ai_memory` 키만 안전하게 추가합니다. 실계좌 주문 기능은 포함하지 않습니다.
