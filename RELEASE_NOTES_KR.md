# A100 V116.2 RC2.3.5 릴리스 노트

## 목적
현재 완료 체인의 Same-ID 정합성과 과거 durable-store anomaly를 분리하여 인증합니다.

## 변경
- Current Completed Same-ID 체인 별도 PASS 판정
- Historical anomaly baseline 진단 파일 추가
- 승인 가능한 최초 기준선: orphan ≤12, duplicate ≤1, revision-only 0, performance-unlinked 0, Attribution delta ≤1
- 기준선 이후 anomaly 증가 시 Version Audit FAIL
- 과거 anomaly 삭제/수정 및 synthetic completion 없음

## 불변 조건
Registry 341/341, Runtime First, Strict Read Only, Live Trading OFF, Gate/Threshold/Learning/Order 로직 불변.
