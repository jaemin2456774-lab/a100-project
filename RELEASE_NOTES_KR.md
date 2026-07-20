# A100 V116.2 RC2.4 Command Certification Framework

## 목적
Registry 341/341 등록 여부와 실제 End-to-End 실행 인증을 분리합니다.

## 주요 변경
- 기존 `/commandcert`에 summary/full/batch/report 모드 추가
- canonical 341개 명령을 Runtime Evidence Matrix와 대조
- PASS 조건: Registry + Handler + Route + Runtime 실행 + Evidence + Store + Output + Replay
- 실행 증거가 없는 명령은 PARTIAL로 유지
- Handler/Route 누락은 FAILED
- `/commandmatrix`를 동일 인증 기준으로 통일
- Entry Decision Score/Threshold/Gap 표시를 소수점 둘째 자리로 개선

## 명령
- `/commandcert`
- `/commandcert full`
- `/commandcert batch 1`
- `/commandcert report`
- `/commandmatrix`

## 변경 금지 유지
Gate/Threshold/Learning/Paper/Live/Registry membership 변경 없음.
