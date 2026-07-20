# S59.7.21 설치 안내

1. Railway 현재 소스와 데이터 볼륨을 백업합니다.
2. ZIP의 `main.py` 및 문서를 기존 프로젝트에 덮어씁니다.
3. 기존 `/data` Runtime/Learning 파일은 삭제하지 않습니다.
4. Railway를 재배포합니다.
5. 배포 후 `/version`, `/versionaudit`, `/papershadow`, `/errors`를 실행합니다.
6. 다음 Producer 주기(최대 약 120초) 후 `/papershadow`를 다시 확인합니다.

정상 기대값:
- Registry 341/341
- Candidate Snapshot 생성
- 잘못된 심볼은 `quarantined`로 집계
- 다른 유효 후보는 계속 처리
- 신규 System Producer 오류 0건
