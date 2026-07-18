# S53 증분 패치 설치 안내

1. Railway에 연결된 GitHub 저장소에서 ZIP의 파일을 기존 프로젝트 루트에 덮어씁니다.
2. 기존 `/data`, 환경변수, 설정 및 학습 데이터는 삭제하지 않습니다.
3. Railway 배포 완료 후 Startup 로그에서 S53 preflight PASS와 Registry 341을 확인합니다.
4. 아래 명령을 순서대로 실행합니다.

/version
/status
/runtimehealth
/sniper
/sniper detail
/ultimate
/ultimate detail
/evidence
/releasegate
/releasegate detail
/errors

확인 핵심: 16칸 그래프, Decision Quality `/100` 게이지, Compact Evidence, Missing Evidence 요약.
