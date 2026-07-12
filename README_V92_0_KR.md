# A100 V92.0 AI Score & Explainable Confidence Engine

## 목적
V91.8의 Meta Decision·Pattern Similarity·Scenario Decision 결과를 하나의 A100 Score로 통합하고, 점수와 신뢰도의 근거를 Telegram에서 바로 확인할 수 있도록 개선한 버전입니다.

## 신규 명령어
- `/score BTC` : 종합점수, 등급, Confidence 2.0, 8개 구성 점수
- `/explain BTC` : 긍정 근거, 위험·감점, Confidence 구성
- `/topscore` : 현재 후보 중 A100 Score 상위 종목

## A100 Score 구성
Pattern, Liquidity, Momentum, Market, Risk, Timing, Learning, Meta를 가중 합산하고 기존 V91 최종점수를 일부 반영해 연속성을 유지합니다.

## 등급
- S+ : 95 이상
- S : 90 이상
- A+ : 85 이상
- A : 80 이상
- B : 70 이상
- C : 70 미만

## 속도 보호
- 기존 enriched candidate 결과 재사용
- 별도 대규모 API 호출 없음
- 기본 캐시 120초
- 환경변수 `A100_SCORE_CACHE_SECONDS`로 조정 가능

## 데이터 호환
- 상태 파일: `a100_v91_paper_state.json`
- schema: `1`
- Paper, Shadow, Learning, Lifecycle, Adaptive, Meta, Similarity 데이터 유지

## 안전 원칙
실계좌 주문 경로는 추가하지 않았습니다. 본 버전은 분석·설명 전용입니다.
