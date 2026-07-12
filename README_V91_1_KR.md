# A100 V91.1 Paper Stability Engine

V91.0에서 확인된 `datetime is not defined` 런타임 오류를 수정하고 Paper Trading 핵심 경로를 재검증한 안정화 패치입니다.

## 핵심 수정
- 전역 `datetime`, `timedelta`, `timezone` 명시적 import
- Paper 일자 키는 `time.gmtime()` 기반으로 변경하여 전역 이름 오염 영향 제거
- 시작 전 UTC 일자 키와 Paper 핵심 함수 callable 검사 추가
- 기존 114개 명령 유지
- `/arkm`, `/syn`, `/sent`, `/futures` 복원·추가 검토 제외 유지
- 실계좌 주문 기능 미구현·비활성 유지

## 배포
GitHub 저장소 루트에 다음 파일을 올립니다.
- `main.py`
- `requirements.txt`
- `railway.json`

## 배포 후 확인
1. `/selfcheck`
2. `/watchdog`
3. `/paperstatus`
4. `/paperon`
5. `/paperopen BTC LONG 100 2 4`
6. `/paperpositions`
7. `/paperclose BTC`
8. `/paperhistory`

## 오프라인 회귀 테스트
의존성 설치 후:

```bash
python test_v91_stability.py
```
