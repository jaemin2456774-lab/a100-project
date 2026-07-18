# S47 패치 설치 가이드

1. Railway에 연결된 GitHub 저장소에서 ZIP의 파일을 동일 경로에 덮어씁니다.
2. 기존 `/data`, 환경변수, DB, 설정 파일은 삭제하지 않습니다.
3. Railway 배포 완료 후 시작 로그에서 S47 Runtime Producer Bridge audit PASS를 확인합니다.
4. `/version`, `/runtimehealth`, `/ultimate detail`, `/sniper`, `/god`, `/releasegate detail`, `/errors`를 실행합니다.

성공 기준은 `Evidence Runtime S47`의 Coverage가 기존 0.0%보다 상승하고, Object bridge가 `Result` 또는 실제 행 타입으로 표시되는 것입니다. Macro/News 등 실제 Feed가 없는 항목은 계속 Missing이어야 정상입니다.
