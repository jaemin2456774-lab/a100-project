# A100 V91.7 META DECISION & PATTERN SIMILARITY ENGINE

기준 원본: 정상 작동 확인된 V91.6

## 추가 기능
- Meta AI 최종판단: TRADE / WAIT / SKIP
- 과거 Paper·Shadow 거래 패턴 유사도
- 유사패턴 승률·기대값(EV)·평균 승패 수익률
- 시장 컨텍스트 점수
- 최근 성과·연속 손실·낙폭 기반 적응형 Paper 리스크
- 위험 시 ENTRY를 READY로 하향하는 안전장치
- 신규 명령 `/help`, `/commands V91` 자동 반영

## 신규 명령
- `/papermeta`
- `/papersimilarity`
- `/papercontext`
- `/paperrisk`

## 도움말 동기화
V91 명령은 명령 레지스트리, `/help`, `/commands V91`에 동시에 반영되며 Preflight에서 누락을 검사합니다.

## 권장 환경변수
```text
PAPER_SIMILARITY_MIN_SAMPLES=8
PAPER_SIMILARITY_TOP_K=30
PAPER_META_MAX_ADJUST=8
PAPER_META_TRADE_SCORE=76
PAPER_META_WAIT_SCORE=60
PAPER_META_RISK_WINDOW=20
PAPER_META_MAX_DRAWDOWN_PCT=8
PAPER_META_AUTO_RISK_GUARD=1
PAPER_AUTO_ENTRY=0
```

## 배포 후 확인
```text
/selfcheck
/legacycheck
/help
/commands V91
/watchdog
/papermeta
/papersimilarity
/papercontext
/paperrisk
```
