# S59.7.3 Railway 증분 패치 설치 가이드

1. Railway에 연결된 GitHub 저장소의 기존 `main.py`를 백업합니다.
2. ZIP의 `main.py`만 저장소 루트의 동일 파일에 덮어씁니다.
3. 문서 파일은 배포 패키지와 분리 보관해도 됩니다.
4. 커밋 후 Railway 배포 로그에서 S59.7.3 Build ID와 Registry 341을 확인합니다.
5. 기존 `/data` Runtime/Learning 파일은 삭제하거나 초기화하지 않습니다.

## 검증 순서
/version
/versionaudit
/engineaudit
/crossengineaudit
/evidencereplay
/commandmatrix
/rcpreflight
/verifyall
/errors

## 정상 기대
- `/versionaudit` S59.7.3
- Runtime Identity PASS
- Authoritative Routes PASS
- Replay PASS 또는 실제 source 미존재 시 MEASURING
- Drift는 실제 실패 항목만 Active
- V88 신규 오류 0건
