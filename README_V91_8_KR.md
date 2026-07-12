# A100 V91.8 DEVELOPMENT BASELINE

기준 원본: 정상 작동 확인된 **V91.7 META DECISION & PATTERN SIMILARITY ENGINE**

## 개발 시작 상태
- V91.7 전체 기능과 133개 Telegram 명령 유지
- `/help`, `/commands V91` 동기화 상태 유지
- Paper / Shadow / 학습 / 기대값 / 생애주기 / 적응형 전략 / Meta / 유사패턴 데이터 유지
- 실계좌 주문 기능 없음
- V91.8 신규 기능은 아직 추가하지 않은 안전한 개발 기준본

## 기존 데이터 유지 조건
다음 항목을 변경하지 않았습니다.

```text
상태 파일명: a100_v91_paper_state.json
상태 스키마: 1
저장 경로 우선순위:
1. RAILWAY_VOLUME_MOUNT_PATH
2. V91_DATA_DIR
3. 기존 V75_DATA_DIR
4. A100_DATA_DIR
5. /data 또는 현재 작업 디렉터리
```

Railway에서 기존 Volume을 동일 경로로 마운트하면 V91.7의 누적 상태를 V91.8이 그대로 읽습니다.

## 배포 전 필수 환경변수 확인
```text
RAILWAY_VOLUME_MOUNT_PATH=/data
PAPER_TRADING_ENABLED=기존값 유지
TELEGRAM_BOT_TOKEN=기존값 유지
TELEGRAM_CHAT_ID=기존값 유지
COINGLASS_API_KEY=기존값 유지
```

## 배포 후 확인 명령
```text
/selfcheck
/legacycheck
/help
/commands V91
/watchdog
/paperstatus
/paperhistory
/papershadowperformance
/paperlearning
/papermeta
/papersimilarity
/papercontext
/paperrisk
```
