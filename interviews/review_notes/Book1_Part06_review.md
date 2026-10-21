# Book 1 Part 06 review (Time Series & Forecasting)

Reviewed: 54 questions (Q1-Q54). No ANSWER_PENDING. All questions have the full template. Header counts (Target 45 / Actual 54 / Stars 16-26-12) re-counted and correct; no "Dedupe pass" note present. CRLF endings preserved.

## Code blocks
- 47 python blocks in file. 44 executed standalone (own imports/seed; a few marked "continuation of Q5 / Q10 / buggy snippet" and run with that prelude). 3 not executed by design: Q22 (prophet not installed), Q34 (illustrative), Q49 (chronos not available). Q43 prose mention of Prophet CV also marked not executed.
- Initial state: ~29 blocks could not run standalone (undefined variables) or printed numbers different from the text. Fixed by adding data generators/imports and re-running. Final run: 44 pass, 0 fail (Q23 failed once on undefined `c`, fixed and re-run OK; Q7 re-run OK after adding the MA(1) line).

## Fixes (Q, what, why)
- Q2: block made standalone; numbers corrected (resid sd 0.008, additive seasonal -9.8 to 10.1).
- Q5: standalone generator; numbers corrected (naive 7.55, 12-m avg 6.78, snaive 6.66, HW 1.36). Same series reused as `train`/`test` in Q8, Q9, Q20, Q21, Q25 (continuation comments added).
- Q6: variances 73.6 / 1.03 / 2.11, ACF -0.51 (text had 79/1.05/2.04/-0.49).
- Q7: ACF/PACF values corrected to code output; MA(1) line added to code (text quoted MA numbers with no code behind them).
- Q8, Q20: AICs and MAE corrected (572.0 / 475.5 / 371.9; MAE 1.46).
- Q9: walk-forward folds numbers corrected (6.01 / 1.30 / 1.36); code now prints them.
- Q10, Q26, Q27: standalone panel generator; WAPE 0.072 vs seasonal naive 0.088 (text said GBM lost to snaive 0.065, which could not be reproduced and is implausible for 8% noise); quantile coverage 74% (text 63.8%); unverifiable "bootstrap [94.2, 107.0]" sentence removed.
- Q11: MASE sentence was inconsistent with the example errors; reworded; code prints MAPE/WAPE.
- Q13, Q14: code made standalone; Q14 interpolation example corrected to [1,2,3,4,5,5.5,6].
- Q15: replaced fragment with runnable recursive-vs-direct code; direct did NOT beat recursive in the run (2.00 vs 2.11); text now says tied.
- Q17: MAEs 0.80 / 14.1.
- Q18: made standalone.
- Q21: damped vs undamped both run (1.36 vs 2.33); previous text quoted an undamped number next to damped code.
- Q25: p = 0.50 (SARIMA) and ~3e-57 (AR(1)); standalone.
- Q29: standalone, numbers corrected (19.2 vs true 21.2, mean 16.6).
- Q30: standalone; numbers corrected (1.41 / 1.34 / 1.27; after zeros Croston 1.41, TSB 0.10).
- Q32: standalone; WAPE after shift 10.8% (text 11.2%); alarm at week 83 and 2 false alarms confirmed.
- Q33: example numbers could not be reproduced; replaced with reproducible simulation numbers and explicit caveat (gap small on this easy series).
- Q35: MAEs replaced by expected values averaged over 2,000 draws (single-draw values were not reproducible); window means 101.9/107.0/112.4 confirmed.
- Q36 (known item): MLP vs seasonal naive; now reproducible code with sklearn MLPRegressor: train WAPE 4.4%, held-out 9.1%, seasonal naive 9.0% (text said train 0.1%, 7.8% vs 8.2%; not reproducible). Message unchanged: no real gain.
- Q31: example now cites the Q36 numbers instead of an unverifiable 6.5% figure.
- Q39: standalone generator; naive 1.60x vs GLM 1.35x (true 1.35x).
- Q40 (known item): code now prints DW, OLS p, HAC p, differenced p; all match text (1.3e-1, 7e-58, 4e-15, 0.61); 500-pair simulation checked separately (82% significant, R2 0.24, DW 0.09; R2 corrected from 0.23). Differencing/HAC note kept and is correct.
- Q41: original combo claim (average beats best) was not reproducible; replaced by a standalone example where the average (2.07) beats two members and is near the best (2.01); say-first softened to "often matches or beats the best".
- Q43: single-series standalone code (original applied TimeSeriesSplit on a panel); numbers 3.50-3.81% CV, 3.43% holdout.
- Q45 (known item): standalone buggy and fixed code; buggy 2.9%, fixed 7.7%, seasonal naive 2.0% (fixed code does not beat the baseline); differenced-target fix 1.7% beats it. Text updated.
- Q46: numbers corrected (0.81 coverage, 3.07/3.28/3.55, CRPS 5.62/6.08/6.54); demo loop added to code.
- Q47 (known item): wording of guarantee kept (needs exchangeability, average coverage only); example rewritten with reproducible design: static 0.87 overall with blocks 1.00/1.00/0.75/0.74, rolling-250 0.87 (0.99/0.88/0.72/0.89), ACI 0.90 (0.94/0.90/0.85/0.89). Honest note that ACI can still under-cover a volatile block. Rolling-window numbers come from a separate script not included in the code block.
- Q48: N-BEATS "M4 winner-level" softened (reported to beat the winning entry).
- Q49: stale reason ("torch not installed") corrected.
- Q50 (known item): "not measured by me" label kept; LLMTime citation kept as a general reference.
- Q51: standalone; y->x p = 0.89, independent-walk coint p = 0.06 (borderline, stated).
- Q52: standalone; level -12.18 for both, K 0.39, ML variances 4.02 / 1.38.
- Q53: standalone; LB p 0.41 / 9e-49; MLE 0.071 / 0.087 / 0.877.
- Q54: standalone; effect 4.74, placebo -0.24, naive interval 4.54-4.95.
- Q22, Q43 Prophet: left marked not executed (kept as instructed).

## Verified without change
Q1, Q19, Q24, Q28 (54% stockout, 17.04/19.86/20.78), Q37 (28.29 / 12.71), Q42 (99 / 40.67 / 33.67 / 24.67; OLS 101.5 checked), Q44 (outputs match, ACF/SES match statsmodels per text).

## Unresolved / not verified
- Q47 rolling-window and static-conformal figures were produced by throwaway scripts, not by the shown block (comment in block says how).
- Q40 500-pair simulation (82%, R2 0.24, DW 0.09) verified by a separate script; the block only shows one pair.
- Q22/Q43-Prophet/Q49 not executed (libraries unavailable). Statements about Chronos/TimesFM/Moirai architectures and the LLMTime/"Are Transformers Effective..." references are from memory, not web-verified.
- Q16, Q4, Q12 etc. cite M5 (LightGBM dominated), not web-verified this pass.
- Illustrative numbers in Q38 (70% completion) and Q3 (5% vs 14% MAPE) are hand-picked illustrations; labelled "example" but not explicitly "illustrative" except where noted.
