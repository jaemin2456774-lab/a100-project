from v931_self_learning_ai import calibrated_probability, grouped_memory, apply_learning, explain

def rows(n=20):
    out=[]
    for i in range(n):
        win=i%3!=0
        out.append({'symbol':'BTCUSDT' if i%2 else 'ETHUSDT','side':'LONG' if i%2 else 'SHORT',
          'realized_pct':1.2 if win else -0.8,'regime_at_entry':{'regime':'TREND' if i%2 else 'RANGE'},
          'sample_type':'SHADOW','components':{'Pattern':75 if win else 35,'Risk':60 if win else 30}})
    return out

def test_calibration_and_ci():
    c=calibrated_probability(70,rows())
    assert c['n']==20 and 0<=c['ci_low']<=c['ci_high']<=100

def test_grouped_memory():
    g=grouped_memory(rows())
    assert g['side'] and g['regime'] and g['symbol']

def test_learned_weights_normalized():
    w,l=apply_learning({'Pattern':50,'Risk':50},rows())
    assert abs(sum(w.values())-100)<=0.2 and l['Pattern']['n']==20

def test_explain():
    c=calibrated_probability(65,rows())
    text=explain('BTCUSDT','LONG','WATCH','TREND',[{'engine':'Pattern','contribution':2}],c,{'n':10,'win_rate':60})
    assert '예상승률' in text and '95%' in text
