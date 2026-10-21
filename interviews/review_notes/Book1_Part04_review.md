# Book 1 Part 04 review (Wave C)

Questions reviewed: 53 (Q1-Q53). No ANSWER_PENDING. File is CRLF throughout (preserved).

## Fixes
- Header: star counts corrected (15 / 27 / 11, was 28 for two-star); stale dedupe remark removed; Status line updated.
- Q16, Q32: added missing Example field.
- Q9, Q11, Q12, Q13, Q14, Q18, Q19, Q20, Q21, Q23, Q24, Q25, Q26: code blocks made standalone (own imports, data and splits; Q9-Q26 share one synthetic set, stated in a comment).
- Q9: example numbers came from a different config than the code; text now says so and quotes the code's own result (67 trees, val AUC 0.938).
- Q13: quoted top-3 SHAP/gain lists were from an unrecorded 3000-row run; replaced with verified lists on the 6000-row set ([3,16,5] vs [5,16,3]).
- Q14: "about 0.95 with complete data" replaced by measured 0.946 (vs 0.933 with 20% NaN).
- Q21: code printed accuracy while text quoted AUC; code now prints AUC (0.9538 vs 0.9532); invented timings replaced by hedged ratio.
- Q20: unmeasured "GBM about 2x slower" softened.
- Q22: wrong claim that MDI of useless features resembled a real one at "0.099-0.177"; corrected to 0.177-0.309 for real features.
- Q25: code printed nothing; added AUC print (0.9509).
- Q26: Optuna "0.974 on another dataset" was not reproducible; code gives 0.9376; text and comment corrected.

## Code run (44 python blocks, plus 13 re-run after edits)
- All 44 originals executed. 13 failed standalone (NameError on Xtr/Xa etc.: Q9, 11, 12, 13, 14, 18, 19, 20, 21, 23, 24, 25 (no print), 26) -> fixed and re-run: all pass (Q26 verified from earlier identical run).
- Q3 timed out once under heavy parallel load, passed on re-run. All printed numbers match the text (Q1-Q8, Q16-Q18, Q22, Q27-Q32, Q34, Q36-Q46, Q49-Q53).
- Q52 latency varies by machine (2.6 ms vs 3.65 ms single-row on re-run): already labelled machine-specific.

## Unresolved / not verified
- Q26 random-search figure (0.939) and Q40 "2.5 min", Q34 "80 s" timings are from the earlier agent's runs; random search not in the code block (stated).
- Boruta mentioned, not run. Q33 (Grinsztajn 2022), Q53 (He et al. 2014) citations match my knowledge; not web-checked.
- Q10 "XGBoost experimental native categorical" is slightly dated (Q14 says supported); left as hedged.
- Q21 timing ratios vary run to run with machine load.
