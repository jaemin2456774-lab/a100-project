# A100 V116.0 LTS RC4.9.6 릴리스 보고서

## 수정
- Dashboard RC4.7 하드코딩 표시를 RC4.9.6 중앙 버전으로 교체
- 명령 사용시간처럼 변동하는 필드를 캐시 서명에서 제외
- 반복 `/status` 캐시 HIT 및 Age/MISS 사유 표시
- LTS Score Progress와 Mandatory Gates 분리
- Queue Wait, Handler, End-to-End Latency 실계측
- `/commandcert detail` 추가 압축 및 `/commandcert warn engine` 필터
- GitHub 덮어쓰기 패키지 정리

## 보존
- Schema 1
- Paper 20 / Shadow 60
- Live Trading OFF
- 기존 상태 및 학습 데이터 경로

## 검증
- Python compile: PASS
- RC4.9.6 targeted tests: 4/4 PASS
- Startup preflight: PASS
- Registry sync: PASS
