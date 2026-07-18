# S55 Railway 증분 패치 설치

1. 기존 S54 저장소에 이 ZIP의 파일을 덮어씁니다.
2. `/data` 볼륨과 기존 환경변수는 그대로 유지합니다.
3. Railway에서 재배포 또는 재시작합니다.
4. Telegram에서 아래만 실행합니다.

```text
/version
/verifyall
/verifyall detail
```

`/verifyall detail`은 `/data/a100_verify_S55_*.json`과 `.txt`를 생성합니다.
캡처 대신 텍스트 결과를 복사하거나 리포트 파일 하나를 첨부하면 됩니다.
