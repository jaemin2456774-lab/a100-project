# A100 V116.0 LTS-S2.10 패치 설치 안내

기준 버전: **A100 V116.0 LTS-S2.9**

1. 실행 중인 봇을 중지합니다.
2. 현재 프로젝트를 백업합니다.
3. 이 패치의 `main.py`를 기존 프로젝트 루트의 `main.py`에 덮어씁니다.
4. 테스트 파일은 프로젝트 루트에 함께 복사합니다.
5. 기존 `data/`, `.env`, DB, JSON, 학습 데이터와 사용자 설정은 삭제하지 않습니다.
6. 재시작 후 아래 명령을 확인합니다.

```text
/version
/status
/runtimehealth
/dashboard btc
/releasegate
/commandcert
/commandcert deep
/versionaudit
/pipelinetrace
```

핵심 확인 항목:
- Runtime Health Previous / Current / Delta
- Memory Baseline / Current / Peak / Delta
- Runtime Score Delta 30m / 1h / 6h / 24h
- Learning ETA Source 및 Selected Velocity
- 음수 ETA 또는 NameError가 발생하지 않는지 확인
