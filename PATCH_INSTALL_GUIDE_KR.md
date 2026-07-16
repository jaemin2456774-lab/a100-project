# S2.17.50 패치 설치 안내

1. Railway 연결 GitHub 저장소의 프로젝트 루트 `main.py`를 패치 파일로 덮어씁니다.
2. 변경 문서와 manifest를 함께 커밋합니다.
3. Railway 새 Deployment를 확인합니다.
4. `/data` 볼륨, 환경변수, DB 및 설정 파일은 삭제하거나 초기화하지 않습니다.

## 배포 후 확인
```
/version
/help
/help signals
/help god
/commands sniper
/versionaudit
/commandcert
/runtimehealth
/errors
```

## 성공 기준
- Version S2.17.50
- Help Categorized 341/341
- Help Searchable 341/341
- `/god`, `/sniper`, `/ultimate`가 Signals에서 검색됨
- Registry / Callable / Expected 341/341/341
- Recent Errors 0
