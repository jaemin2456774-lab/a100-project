# S2.17.7 패치 설치 안내

1. ZIP을 해제합니다.
2. 내부 `main.py`를 GitHub 저장소 루트의 기존 `main.py`에 덮어씁니다.
3. 데이터 및 설정 파일은 삭제하지 않습니다.
4. Railway 배포 완료 후 아래 명령을 순서대로 실행합니다.

```
/version
/releasegate
/versionaudit
/errors
```

정상 기준:
- 버전 `V116.0-LTS-S2.17.7`
- 최초 요청은 `REFRESHED`, TTL 내 후속 요청은 `CACHE HIT`
- Snapshot Age 증가, Expires In 감소
- `/releasegate`와 `/versionaudit`의 Snapshot ID/Unified Hash 일치
- 신규 timeout 및 runtime error 없음
