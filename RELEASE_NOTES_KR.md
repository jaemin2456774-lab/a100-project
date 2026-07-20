# A100 V116.2 RC1.5

## 수정
- Legacy installer 이후 Registry 신규 키 제거, 기존 341개 membership 고정
- /papershadowperformance 180초 bounded read-only QA cache
- Binance cache 동시 저장 충돌 수정: lock + unique tmp + fsync + os.replace
- 부팅 live trading/identity 배너 RC1.5 통일

## 불변
Runtime First, Strict Read Only, Live OFF, Gate/Threshold/TP/SL/Learning store mutation 없음.
