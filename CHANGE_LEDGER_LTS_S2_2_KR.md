# LTS S2.2 변경 원장

- 목적: 초기 표본의 오판정 방지와 장시간 인증 설명력 강화
- 영향 모듈: main.py 장시간 Runtime 계측/출력 계층
- 영향 명령: /version /status /runtimehealth /performanceaudit /dashboard
- 변경: Warm-up Gate, 단계형 Runtime 상태, ETA, 가중치, Recovery timestamps
- 회귀: 전체 pytest PASS, Registry 341/341 유지
- 데이터 정책: Schema 1, Paper 20, Shadow 60, Live OFF 유지
