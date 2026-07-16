# S2.17.44 패치 설치 안내

1. Railway에 연결된 저장소의 프로젝트 루트에서 `main.py`를 덮어씁니다.
2. 데이터 볼륨 `/data`, 환경 변수, DB 및 설정 파일은 변경하지 않습니다.
3. 커밋 후 Railway 새 배포를 실행합니다.
4. 시작 로그에서 S2.17.44, Registry 341, preflight PASS, runtime performance monitor ACTIVE를 확인합니다.

## 확인 명령
`/version`, `/versionaudit`, `/commandcert`, `/coach`, `/coach detail`, `/runtimehealth`, `/ltsreadiness`, `/errors`

`/runtimehealth`의 평균/P95/최대 값은 배포 직후 표본이 적으므로 수분 이상 운영한 뒤 다시 확인하십시오.
