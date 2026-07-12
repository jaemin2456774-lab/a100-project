# A100 V91.8 Scenario Decision Engine

V91.7의 Meta Decision과 Pattern Similarity 결과를 실제 행동 판단용 다중 시나리오로 변환하는 Paper 분석 버전입니다.

## 신규 명령어

- `/scenario BTC` : 현재 후보에 포함된 종목의 시나리오, 확률, 진입 구간, 목표가, 무효화 가격을 출력합니다.
- `/scenario_top` : 현재 시나리오 우선순위 상위 종목을 출력합니다.

기존 `/decision BTC` 명령은 변경하지 않았습니다.

## 진입 상태

- `WATCH`: 관찰 단계
- `READY`: 눌림 또는 돌파 확인 대기
- `TRIGGERED`: 조건 충족
- `LATE`: 과열 또는 추격 위험
- `INVALID`: 위험모드 또는 시나리오 무효

## 성능 보호

시나리오 엔진은 별도 대규모 시장 API 호출을 추가하지 않고 기존 V91.7 enriched candidate 결과를 재사용합니다. 기본 캐시 시간은 120초이며 환경변수 `PAPER_SCENARIO_CACHE_SECONDS`로 조절할 수 있습니다.

## 데이터 호환성

- 파일명: `a100_v91_paper_state.json`
- schema: `1`
- 기존 Railway Volume과 상태 파일을 그대로 사용합니다.

## 안전성

본 버전은 Paper 분석 전용입니다. 실계좌 주문 함수 및 주문 실행 경로를 추가하지 않았습니다.
