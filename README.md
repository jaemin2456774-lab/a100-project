# A100 V114.0 PATTERN MEMORY, REGIME & ADAPTIVE LEARNING DEVELOPMENT

기준 버전 V113.4의 운영 안정성과 학습 가시성을 유지하면서 Pattern Memory, Market Regime AI, Adaptive Entry Threshold, Post Trade Learning 2.0을 추가한 개발 릴리스입니다.

## 배포 후 검증 순서
`/versionaudit` → `/runtimehealth` → `/learningdashboard` → `/marketregime` → `/adaptivethreshold` → `/patternmemory` → `/postlearning` → `/papertracescan` → `/entrytrace`

## 핵심 안전 정책
- Paper-only
- Paper 포지션 20개
- Shadow 포지션 60개
- Adaptive Threshold는 55~70 범위의 권장값으로 시작
- 기존 상태 및 학습 데이터 보존

# A100 V113.4 OPERATIONS & LEARNING OBSERVABILITY DEVELOPMENT

기준 버전 V113.3을 기반으로 운영 상태와 AI 학습 가시성을 강화한 개발 릴리스입니다.

## 배포 후 검증 순서
`/versionaudit` → `/runtimehealth` → `/learningdashboard` → `/papertracescan` → `/papertrace` → `/entrytrace` → `/paperqueue` → `/entryexecution`

## 핵심 변경
- 중앙 버전 V113.4 동기화
- Entry Pipeline 단계 표시
- Queue 평균/P95 및 24시간 통계
- AI 점수 추세와 24시간 최고·최저
- Runtime Health 및 AI Learning Dashboard 신규 명령

# A100 V113.3 CENTRAL VERSION MANAGER & RUNTIME TRACE INTELLIGENCE DEVELOPMENT

## 핵심 변경
- `/versionaudit` 런타임 검증 확장: 명령 누락, 활성 핸들러, 큐 만료 정리, 실행 성공률, 최근 명령 감사
- `/entrytrace`, `/paperqueue`, `/entryexecution` 표준 예외 처리 및 실행 감사 로그
- 6시간 이상 정체된 활성 Paper Entry Queue 자동 `EXPIRED` 처리
- 테스트 루트 경로 정상화 및 최신 유지보수 회귀군 기본 실행
- Paper-only 원칙, 기존 데이터 스키마, Paper 20개, Shadow 60개 유지


## Critical hotfix
- Moved the executable `__main__` block to the physical end of `main.py`.
- Ensures V113 queue/execution commands are registered before the Telegram application starts.
- Added `/versionaudit` for runtime callback/version verification.
- Startup now fails fast when required callbacks, registry snapshot, version, limits, or schema checks fail.
- Active `/help` and `/commands` outputs are synchronized to V113.1.

# A100 V113.1 Entry Execution & Paper Queue Intelligence Development

# A100 V112.0 Score Calibration & Learning Boost Development

V111.0을 기준으로 Paper LEARNING 모드의 후보 점수 분포를 보정하고, 초기 학습 단계에서 상위 후보를 제한적으로 ENTRY로 전환하는 개발 릴리스입니다.

핵심 명령:
- `/scorecalibration`
- `/scorebreakdown BTC`
- `/learningboost`
- `/papertracescan`
- `/papertrace BTC`
- `/thresholdreview`

안전 원칙:
- 보정은 Paper LEARNING 모드에만 적용
- 후보당 점수 보정 최대 +12점
- 목표 ENTRY 통과율 5~15%
- 최대 포지션 20, Shadow 60, 중복·쿨다운·Kill Switch·시장 데이터·BTC Shock Guard 유지
- 실주문 기능 및 실주문 기준 변경 없음


## V113.1 핵심 변경
- LEARNING 모드에서는 legacy PAPER_AUTO_ENTRY 값과 무관하게 Paper 자동 진입 파이프라인 활성화
- ENTRY 통과 후보를 영구 Paper Queue에 저장
- Scanner → ENTRY → Queue → Paper Create 전 과정 추적
- 일시적 생성 오류는 8초 후 1회 제한 재시도
- 중복, 쿨다운, 포지션 한도, Kill Switch, BTC Shock 등 안전장치 유지
- 신규 명령: /entrytrace, /paperqueue, /entryrecovery, /entryexecution


## V113.3
주요 운영 명령의 버전 배너를 중앙 관리하며 런타임 감사와 Paper Trace 전망 정보를 강화했습니다.

## V114.1 Explainable AI & Similarity Intelligence
신규 명령: `/similarity`, `/decisionreason`, `/memoryweight`, `/selfevaluation`.
적응형 Threshold는 Shadow 검증에만 적용되며 Paper 실제 진입 기준은 변경하지 않습니다.
