import unittest
from v930_ai_intelligence_core import classify_regime, adaptive_weights, build_core, summarize_history

class V930CoreTests(unittest.TestCase):
    def setUp(self):
        self.item={"symbol":"BTCUSDT","side":"SHORT","components":{"Pattern":72,"Liquidity":61,"Momentum":76,"Market":68,"Risk":64,"Timing":73,"Learning":55,"Meta":60}}
        self.decision={"verdict":"WATCH","memory":{"completion":40},"risks":["Precision Gate 미통과"]}
    def test_regime(self): self.assertIn(classify_regime(self.item)["name"],{"BREAKOUT","TREND"})
    def test_weights(self): self.assertAlmostEqual(sum(adaptive_weights(self.item,{"completion":40}).values()),100,delta=.3)
    def test_core(self):
        c=build_core(self.item,self.decision,[]); self.assertEqual(c["version"],"V93.0"); self.assertTrue(c["explanation"]); self.assertTrue(c["contributions"])
    def test_history(self):
        h=summarize_history([{"return_pct":1},{"return_pct":-1,"close_reason":"SL"}]); self.assertEqual(h["windows"][50]["n"],2)

if __name__=='__main__': unittest.main()
