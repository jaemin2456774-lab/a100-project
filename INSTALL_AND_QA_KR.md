# 설치 및 QA

1. ZIP을 기존 prebuilt patch와 동일한 방식으로 Railway에 배포합니다.
2. 다음 순서로 실행합니다.

```text
/version
/buildinfo
/commandcert autorun
/commandcert status
/commandcert status
/commandcert stop
/commandcert status
/commandcert
/commandmatrix
/errors
```

## 기대 결과
- 버전 `V116.2-RC2.4.4`
- `/ai` 등 느린 명령이 제한시간을 넘겨도 Runner가 다음 명령으로 진행
- Status에 `Timeout`, `Slow`, `Promoted`, `Failed`가 분리 표시
- Timeout만 발생한 경우 `/errors`에 Telegram TimedOut이 추가되지 않음
- Probe 완료 후 PASS/Runtime/Evidence/Store/Output 수가 즉시 재평가됨
- Gate/Threshold/Live mutation 없음
