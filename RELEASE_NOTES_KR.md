# A100 V116.2 RC1.1 Performance & Runtime Identity Hardening

## 기준
- Base: `A100_V116_2_RC1_INTEGRATED_PRODUCT_HARDENING_BASE.zip`
- Reference: `A100_V116_1_DEV_S59_7_22_SHADOW_ENTRY_GATE_TRACE_LEARNING_SOURCE_ALIGNMENT_HOTFIX_PREBUILT_PATCH.zip`
- 변경 파일: `main.py` 1개

## 수정 내용
1. `/papershadowperformance`를 RC1.1 전용 authoritative route로 교체했습니다.
2. Durable learning revision과 Shadow close/review/performance 수를 결합한 read-only revision cache를 추가했습니다.
3. Current Shadow Session과 Lifetime Durable Learning 통계를 분리했습니다.
4. LONG/SHORT 승격 표본 진행률을 표시합니다. 기본 최소 표본은 50이며 환경변수 `A100_PROMOTION_MIN_SAMPLES`로 표시 기준만 조정할 수 있습니다.
5. 표본 부족 전략에 `INSUFFICIENT SAMPLE`을 우선 표시합니다.
6. Snapshot Read / Aggregation / Output Render / Handler Total 진단을 추가했습니다.
7. 과거 코드의 실행 동작은 보존하면서 부팅 콘솔의 DEV S59.7.2, V90.2, V92.5, LTS S2.17.4 레거시 배너만 억제하고 RC1.1 현재 식별자를 단일 표시합니다.

## 변경하지 않은 항목
- Entry Gate 계산식 및 Threshold
- TP/SL 및 Shadow/Paper 실행 로직
- Learning/Attribution 저장 구조
- Registry 항목 수
- Live Trading OFF
- 기존 데이터 및 환경설정
