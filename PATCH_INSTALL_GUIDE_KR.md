# S2.17.43 패치 설치 안내

1. Railway에 연결된 저장소 프로젝트 루트의 `main.py`를 패치 파일로 덮어씁니다.
2. 테스트 파일과 문서는 선택적으로 저장소에 반영합니다.
3. `/data`, 환경 변수, DB, 설정 파일은 삭제하거나 초기화하지 않습니다.
4. Railway에서 새 배포를 실행합니다.
5. 시작 로그와 아래 명령을 확인합니다.

```text
/version
/versionaudit
/commandcert
/coach
/coach detail
/intelligence
/intelligence detail
/ltsreadiness
/runtimehealth
/errors
```
