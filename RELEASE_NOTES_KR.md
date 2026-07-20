# A100 V116.2 RC2.4.1 릴리스 노트

- Historical Growth Trace: 신규 duplicate/attribution growth의 ID 샘플·revision·delta를 bounded 기록합니다.
- Safe QA Batch Runner: 기존 Coverage Planner의 SAFE 배치만 명시적 실행합니다.
- `/commandcert batch N run`, `/commandcert autorun`, `/commandcert status`, `/commandcert stop` 지원.
- 실제 Runtime+Evidence+Store+Output+Replay가 모두 존재하면 matrix state와 무관하게 PASS 승격.
- 거래/주문/Gate/Threshold/설정 변경 명령은 자동 검수에서 제외합니다.
- Registry 341/341, Runtime First, Strict Read Only, Live OFF 유지.
