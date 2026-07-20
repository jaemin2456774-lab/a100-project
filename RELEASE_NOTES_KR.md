# A100 V116.2 RC2.3.6 릴리스 노트

## 목적
RC2.3.5에서 historical anomaly가 승인 한도를 초과하면 baseline을 만들지 못해 영구적으로 `MISSING`이 되던 bootstrap 결함을 수정합니다.

## 변경
- 현재 Completed Same-ID 체인이 일치할 때 현재 historical anomaly 상태를 최초 baseline으로 저장
- 최초 저장 이후 증가분만 FAIL 처리
- 기존 orphan/duplicate/Attribution 초과 데이터 삭제·수정 없음
- 새 baseline 파일: `/data/a100_rc236_historical_anomaly_baseline.json`
- Gate, Threshold, Learning, Attribution, Shadow/Paper/Live 로직 변경 없음

## 기대 결과
첫 `/versionaudit`: Baseline State `CREATED` 또는 `ACTIVE`
두 번째 `/versionaudit`: Baseline State `ACTIVE`, Post-baseline Delta 0, Version Audit PASS
