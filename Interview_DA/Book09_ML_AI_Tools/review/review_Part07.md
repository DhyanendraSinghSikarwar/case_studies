# Review Part 07 (Book 9, forecasting basics), Wave C

## Counts
- Answers checked: 45 of 45 (Q1 to Q45).
- Code blocks run: 29 Python blocks now in the part (28 original plus the new Q30 block), all run on Python 3.13, pandas 3.0.5, numpy 2.5.3, statsmodels 0.15.0, sklearn 1.9.1. Every pasted Output matched after the fixes below.
- Hand-arithmetic answers recomputed by script (Q5, Q7, Q9, Q10, Q15 to Q24, Q28, Q32, Q33, Q39, Q40, Q41, Q44): all matched except the items below.
- Answers wrong or changed: 10 (Q2, Q5, Q7, Q13, Q22, Q25, Q30, Q33, Q35, Q37).

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q7 | Common mistake said averaging all six months gives 140.0; correct value is 135.0 | Changed to 135.0 |
| Q13 | Code used undefined `sales_series` (hidden data), so the block could not run as shown | Added a seeded generator (invented data) so the block runs; regenerated output (only Jan 0.89 became 0.88); December values now 1,291 / 1,354 / 1,447; prose "11 to 12%" became "12%" |
| Q2 | Yearly averages (1,056 / 1,120 / 1,182) belonged to hidden, non-reproducible data | Changed to 1,045 / 1,110 / 1,175 (the Q13 series) and cross-referenced Q13; Dec +23%, Feb -12% still hold |
| Q22 | "Same total error idea" is false (total absolute error is 8 vs 6) | Reworded to "Different shape of error" |
| Q25 | `adfuller(...)[1]` emits a FutureWarning on statsmodels 0.15 (tuple return changing in 0.16) | Switched to `adfuller(..., result_object=True).pvalue`; outputs unchanged (0.916, 0.0) |
| Q30 | Table said "computed by script" but no script or data existed; numbers (0.096 / 0.222 / 0.079) could not be reproduced | Added seeded runnable code and real output; table now 0.066 / 0.099 / 0.046 MAE; biggest miss 0.09, range stated as plus or minus 0.1; seasonal naive still wins |
| Q35 | Fitted weights on the seeded data are all about 0 (level 1.5e-8, trend 0, seasonal 0), a degenerate fit not mentioned; damped_trend labelled "unverified" though it runs | Added a plain-words note on the degenerate fit; damped_trend now stated as running without error on 0.15.0 |
| Q37 | Weight names given loosely | Clarified they are keys of `fit.params` (verified on 0.15.0) |
| Q5 | Prophet interval claim not labelled | Marked "from memory, unverified" |
| Q33 | "computed by script" claim | Reworded to "recomputed on the installed numpy" (slope 3.295, R-squared 0.869, month-36 value 223.6, overstatement 62%: verified) |

## Verified as correct (no change)
Q3 rolling output; Q4 MAEs 10.0 / 13.3; Q5 SD 25.4 and plus or minus 33 (1.28 x 25.4 = 32.6); Q6/Q9 MAE 8.33, RMSE 8.66, MAPE 7.47, bias -1.67; Q8 dates; Q10 210 / 187.5; Q11 table; Q15 indices; Q18 slope 2.2, intercept 7.8, forecast 21; Q20 118; Q23; Q24 (3.25, 62.8, 12.4); Q26 TimeSeriesSplit folds; Q27 decomposition numbers (seasonal sums to 0); Q29, Q36, Q40, Q41, Q44; Q45 ACF (0.31, -0.26, 0.79, limit 0.26); Q35 error messages for 12 rows and zero values; Q35 forecast values.

## Unresolved / report only
- Q23 heading says errors "are given" but the data is actual and forecast; answer handles it. Heading left unchanged per rules.
- Q41: with level 100 versus base 101.29 the forecast is 80.96, shown as 81.0; fine, but the assumption is already noted.
- Overlap: Q9 and Q6 share the same worked numbers (intentional cross-reference); Q29/Q36 overlap on leakage; Q40 and Q29 use the same daily orders. Ordering/numbering: stars descend 3, 2, 1 in order; no issues. Target 38 vs 45 actual, noted in header.
- Q8 "Asked at" Tiger Analytics and Q26 are supported by Book09_Part07_sources.md (anonymous, unverified); all others say "commonly asked (no company-specific report found)".

## Claims left unverified (labelled in the text)
Prophet behaviour and origin (Q5, Q43); Excel FORECAST.LINEAR (Q18); sklearn `train_test_split(shuffle=False)` (Q8); DPDP Act / GDPR and public-chatbot privacy principles (Q42); prep-site frequency claims in "Asked at" lines.

Style: no em dashes in answer text (only the part-title line); code fences balanced; tables followed by blank lines.
