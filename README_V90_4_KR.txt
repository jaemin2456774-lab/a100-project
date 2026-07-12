A100 V90.4 ULTIMATE STABLE

기준: V90.3 전체 기능과 명령 레지스트리를 그대로 유지하고 회귀 방지 계층을 추가했습니다.

핵심 수정
1. Result.get/items/to_dict 호환을 최종 시작 단계에서 재보증
2. math/NaN/Infinity 안전 변환 도우미 추가
3. 등록 명령, 콜백, 핵심 명령, 단일 디스패처, 심볼 가드, 공통 캐시, Polling 잠금의 시작 전 검사
4. 정의되지 않은 콜백이나 핵심 명령 누락 시 봇이 불완전한 상태로 실행되지 않고 명확한 오류를 출력
5. /health, /selfcheck, /legacycheck를 V90.4 회귀 감사판으로 강화
6. V90.3 Binance 심볼 자동 갱신, 마지막 정상 캐시, 공통 분석 캐시 유지
7. 기존 V90.3 명령 레지스트리와 분석 기능은 삭제하지 않음

배포
- ZIP을 먼저 압축 해제합니다.
- main.py, requirements.txt, render.yaml을 GitHub 저장소 루트에 덮어씁니다.
- ZIP 파일 자체를 GitHub 실행 파일로 올리지 않습니다.

배포 후 순서
/selfcheck
/legacycheck
/commands
/health
/v90 BTC
/pulse BTC
/risk BTC
/whale87 BTC
/alertplan BTC
