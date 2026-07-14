# S2.11.1 긴급 패치 설치

기준 버전: A100 V116.0 LTS-S2.11

1. 압축을 풉니다.
2. 저장소 루트의 `main.py`를 이 패치의 `main.py`로 교체합니다.
3. GitHub에 변경 파일만 업로드하고 Railway 재배포를 실행합니다.
4. 배포 로그에서 `NameError: V1160VersionManager`가 재발하지 않는지 확인합니다.
5. 배포 성공 후 `/version`, `/status`, `/runtimehealth`, `/releasegate`, `/errors`를 우선 실행합니다.

데이터 파일과 환경변수는 변경하지 않습니다.
