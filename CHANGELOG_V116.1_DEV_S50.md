# A100 V116.1 DEV S50

## Decision Clarity, Symbol Recovery & Compact Consensus Runtime Integration

- Explainable AI output now separates directional probability from the final safety decision.
- LONG/SHORT probability can remain directional while WAIT is shown separately with explicit reasons.
- Candidate identity recovery supports symbol, sym, coin, ticker, market, asset and pair schemas, including nested runtime payloads.
- UNKNOWN is replaced by the real runtime symbol when one exists; otherwise the honest label CANDIDATE is used.
- Missing evidence is deduplicated, translated to readable names and compacted with a count.
- Cross-engine summary displays existing engine verdicts without manufacturing scores.
- /ultimate and /ultimate detail replace the oversized legacy candidate card with a bounded compact runtime card.
- /sniper uses the same decision, score, symbol and evidence source as /ultimate.
- Existing Runtime First, Evidence Only, Strict Read Only, Registry 341, Schema 1, Paper 20, Shadow 60 and Live OFF rules remain unchanged.
- Release Gate thresholds and certification state are not mutated.
