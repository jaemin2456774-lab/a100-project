# A100 V118.0 RC3.8 릴리스 노트

Build ID: `V118.0-RC3.8-20260722-WARM-COLD-ISOLATION-TRUE-RENDER-FASTPATH-01`

## 변경 사항
- Render Cache HIT 시 Projection, Trust, Ledger, Matrix를 다시 계산하지 않는 Full-Text Fast Path 적용
- 부팅 Warmup에서 생성한 Stable Semantic Projection Hash를 Active Generation으로 고정
- `/versionaudit`, `/commandcert`, `/commandmatrix`, `/trustgate`, `/intelligencescore`가 Active Generation 캐시를 우선 조회
- Warm/Cold 성능 통계 분리
- 운영 성능 판정은 Warm P95 기준
- Cold P95는 진단 지표로만 유지
- 캐시 진단을 Last Result, Last Miss Reason, Entry Age, TTL Remaining, Warm Used, Generation으로 분리
- `/performancebudget`, `/perf` Registry-neutral alias 유지

## 불변 원칙
Registry 341/341, Runtime First, Strict Read Only, Ledger Append Only, Live Trading OFF를 유지합니다.
