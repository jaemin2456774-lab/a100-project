# A100 V118.0 RC2 설치 및 QA

## 수정 목적
V118 코드보다 앞선 RC5 실행 블록이 먼저 실행되어 V118 정의가 로드되지 않던 실행 순서 회귀를 수정합니다.

## 설치
기존 main.py를 백업한 뒤 이 패키지의 main.py로 교체하고 재배포합니다.

## 배포 후 확인
1. /version
2. /buildinfo
3. /versionaudit
4. /commandcert
5. /commandcert
6. /commandmatrix
7. /commandmatrix
8. /trustgate
9. /trustgate
10. /performance
11. /errors

## 기대 결과
- Running V118.0-RC2
- Build ID V118.0-RC2-20260722-AUTHORITATIVE-TAIL-BOOT-PERFORMANCE-ROUTE-01
- Architecture Guard PASS
- Registry 341/341
- 반복 조회 Cache HIT
- /performance에서 P50/P95/Hit Rate 표시
- Trust 조회 Ledger append NONE
