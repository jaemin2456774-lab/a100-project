# Railway 배포 안내

1. ZIP 압축을 해제합니다.
2. 저장소 루트의 동일 파일을 덮어씁니다.
3. GitHub에 커밋/푸시합니다.
4. Railway 배포 완료 후 Bot 로그에서 Registry 341/341 및 오류 0건을 확인합니다.
5. 아래 명령을 순서대로 실행합니다.

/version
/versionaudit
/paper
/papershadowperformance
/learning
/review
/accuracytracker
/memoryhealth
/strategytrust
/errors

기대 결과:
- S59.7.7, Registry 341/341, Version Audit PASS
- /learning LONG 또는 SHORT 표본이 실제 종료 거래 방향에 따라 증가
- Shadow 종료 거래가 있으면 /papershadowperformance 표본과 /learning 표본에 함께 반영
- 동일 거래 재조회 시 표본이 중복 증가하지 않음
