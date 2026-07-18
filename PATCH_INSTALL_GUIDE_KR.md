# S49.2 증분 패치 설치 안내

1. Railway에 연결된 GitHub 저장소에서 ZIP의 `main.py`를 기존 파일에 덮어씁니다.
2. 데이터 디렉터리 `/data`, 환경변수, DB, 설정 파일은 변경하지 않습니다.
3. Railway 배포 완료 후 시작 로그에서 S49.2 worker, Registry 341, Telegram single polling을 확인합니다.
4. 아래 명령을 순서대로 실행하고 전체 캡처를 보관합니다.

```text
/version
/runtimehealth
/ultimate
/ultimate detail
/sniper
/god
/errors
```

5. 10~15초 안에 `/ultimate detail`, `/sniper`, `/errors`를 다시 실행합니다.

성공 기준: Explain L/S/W 점수가 AI Debate의 점수와 일치하고, Final/Consensus/Explain verdict가 모순되지 않으며 신규 오류가 없어야 합니다.
