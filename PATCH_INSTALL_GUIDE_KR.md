# S2.17.38 패치 설치 안내

1. 현재 Railway 배포 저장소를 백업합니다.
2. ZIP의 `main.py`를 프로젝트 루트에 덮어씁니다.
3. 변경 파일을 GitHub 배포 브랜치에 커밋·푸시합니다.
4. Railway에서 새 Deployment를 확인합니다.
5. 기존 데이터 디렉터리와 환경변수는 변경하지 않습니다.

## 배포 후 확인
```
/version
/versionaudit
/commandcert
/status
/dashboard
/releasegate
/ltscertification
/runtimehealth
/pipelinetrace
/performanceaudit
/errors
```

성공 핵심값:
- S2.17.38
- Version source single PASS
- Registry / Callable / Expected 341/341/341
- Command Certified 341/341
- Recent errors 0
