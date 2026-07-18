# S49 증분 패치 설치 안내 (Railway)

1. 현재 저장소와 `/data` 백업을 확인합니다.
2. ZIP의 파일을 저장소 루트에 덮어씁니다.
3. GitHub에 커밋·푸시한 뒤 Railway 배포를 확인합니다.
4. `/data`, 환경변수, 기존 설정·학습 데이터는 삭제하지 않습니다.

## 예상 시작 로그
- A100 V116.1 DEV S49 worker running...
- A100 V116.1 DEV S49 Evidence/Explainability audit: PASS
- A100 V116.1 DEV S49 real runtime evidence expansion: ACTIVE
- A100 V116.1 DEV S49 Explainable AI 2.1: ACTIVE
- A100 V116.1 DEV S49 Research Notebook 2.1 bounded cache: ACTIVE
- A100 V116.1 DEV S49 producer/gate diagnostics: READ ONLY
- A100 V116.1 DEV S49 synthetic evidence/pass: DISABLED
- A100 V116.1 DEV S49 live trading: OFF

## 검증 명령
/version
/runtimehealth
/ultimate
/ultimate detail
/sniper
/god
/releasegate detail
/errors

10~15초 내 반복:
/ultimate detail
/god

실제 Runtime 증거가 없는 항목은 MISSING이 정상이며, Coverage나 Certification을 임의 PASS로 판단하지 않습니다.
