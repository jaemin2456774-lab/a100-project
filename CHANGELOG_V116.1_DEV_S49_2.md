# A100 V116.1 DEV S49.2

## Explainable AI Consensus Score Linkage & Compact Runtime Explanation Hotfix

- Explainable AI의 LONG/SHORT/WAIT 점수를 AI Debate 2.0 `consensus_judge.scores`와 직접 동기화했습니다.
- 구조화 Brain 객체, Judge 점수, 기존 숫자 필드, Runtime 후보 필드를 순서대로 읽는 bounded fallback을 추가했습니다.
- 실제 방향 점수가 존재할 때만 WAIT 보완값을 계산하며 Synthetic Evidence는 생성하지 않습니다.
- WAIT 원인을 Safety reason, Missing Evidence, Debate edge 기준으로 명확하게 표시합니다.
- `/ultimate detail`의 중복된 전체 레거시 상세 출력을 줄이고 핵심 후보 카드 + Evidence + Explain + Notebook 중심으로 최적화했습니다.
- `/sniper`를 Consensus-linked 핵심 설명 중심으로 간결화했습니다.
- Runtime First, Strict Read Only, Schema 1, Registry 341, Paper 20, Shadow 60, Live OFF를 유지합니다.
- ReleaseGate 공식 계산식과 인증 상태는 변경하지 않습니다.
