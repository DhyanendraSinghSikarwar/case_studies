# Review Part 02 (Wave C): Linear and logistic regression with sklearn

Environment: Python 3.13, pandas 3.0.5, scikit-learn 1.9.1, statsmodels 0.15.0.

## Counts
- Answers checked: 84 of 84.
- Python blocks extracted and run: 71 after edits (69 before; 2 added). 68 reproduce the pasted Output exactly. The other 3 are question-statement snippets, not answer code (Q14 stem, Q35 stem, Q36 `features` list), so they were not expected to run alone.
- Answers changed: 8 (Q8, Q27, Q38, Q45, Q54, Q56, Q73, Q81). Wrong figures or claims found: 4 (Q27, Q38, Q45, Q56). The other 4 were clarity or hygiene fixes.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q8 | Follow-up repeated the same clause twice | Reworded to one clear sentence |
| Q27 | Worked example ("coefficient 6.4, accuracy 1.0 then 0.68, script, seed 42") could not be reproduced and had no code | Added runnable code and output (seed 42): 1.0 with the leak, 0.69 without, largest coefficient 6.3, always-"stayed" baseline 0.65. Prose notes that 0.69 is only a little above the baseline |
| Q38 | Worked example ("intercept 19,900, slope 1,190, seed 42") was hidden-data and not reproducible | Replaced with a 5-person hand-checkable example (`np.polyfit`: slope 1,186, intercept 20,347; centred at 40 gives 67,800) |
| Q45 | Squared error 7.35 for the "flatter line with slope 0.5" was unexplained; it is only true with the same intercept 1.8 (the mean-through line gives 3.30). "Five employees who left (0,0,1,0,1)" contradicted the zeros | Stated the same intercept; reworded to "where 1 means left". Rechecked: SSE 2.4, log loss 0.39 and 0.69 are correct |
| Q54 | Code printed `3.4999999999999996`, then needed an apology sentence | `round(coef / std_err, 2)`, output `3.5`, sentence removed |
| Q56 | Worked example (R2 0.13, McFadden 0.127, log loss 0.44 vs 0.51, AUC 0.75, seed 42) not reproducible | Added runnable code and output: R2 0.10, McFadden 0.09, log loss 0.51 vs 0.56, AUC 0.70, about 25% leave, scored on training rows (stated) |
| Q73 | "used for logistic regression in some solvers" overstated (lbfgs is quasi-Newton) | Changed to "some solvers use gradient-style steps" |
| Q81 | `random_split` and the `train_test_split` import were unused test scaffolding | Removed both; output unchanged (AUC 0.929 and 0.58) |

## Verified and left as is
- Hand arithmetic rechecked: Q4, Q13, Q15, Q16, Q21, Q22, Q24, Q28, Q30, Q32 (slope 6, intercept -8), Q33, Q39, Q45, Q47, Q54 (CI 1.36 to 2.98), Q58 (break-even 0.00498), Q62, Q63, Q72, Q74.
- Q44 weights 0.62 and 2.61, training 1,500 rows with 287 leavers, test 95 leavers: confirmed by script.
- Q55 group means (10.1, 12.6, 15.0, 37.9) and the no-interaction overtime coefficient (15.75, "about 16"): confirmed.
- API claims checked on the installed versions:
  - Q35: the pandas Series and NumPy error wordings are exactly as stated.
  - Q46: `C=1.0`, `l1_ratio=0.0`, `penalty` deprecated since 1.8 with a warning (also for `penalty=None`).
  - Q48: the `multi_class` argument is absent.
  - Q60: statsmodels gives PerfectSeparationWarning and ConvergenceWarning, coefficient 19.27, std err 10,826.
  - Q73: `LinearRegression.fit` calls `linalg.lstsq`.
  - Q77: the ConvergenceWarning appears with 100 of 100 iterations.
  - Q82: `SGDClassifier.eta0` exists.
- Template: all 84 have Asked at, interviewer check, Say this, Explain simply, Likely follow-ups, Common mistakes. 18 conceptual answers have no "What it means" because they have no code or output (acceptable; 2 of these, Q27 and Q56, now have one).
- Style: balanced code fences (278 markers after edits, even); no em dashes in answer text (only the part-title line); numbering Q1 to Q84 complete; stars 3, 2, 1 in order.
- "Asked at" lines say "commonly asked (no company-specific report found)" with unverified snippet-level notes. Tiger Analytics, Fractal and similar mentions match `research/Book09_Part02_sources.md`.

## Unresolved or report-only
- Overlap: Q47 and Q72 reuse the same 30/70 vs 10/90 table (Q72 adds the rare-case contrast); Q9, Q30 and Q66 all show why linear fails on yes/no; Q5, Q19 and Q7 share the same six-employee data. Intentional cross-references, but could be trimmed. Q18, Q44 and Q58 also overlap on imbalance. Check against Book 5 Part 7 and other Book 9 parts was not done.
- Q83, Q81 and Q70 use customer or churn framing rather than HR. This is acceptable but inconsistent with the HR theme.
- Header says "Target 85, Actual 84" (a documented shortfall of one).

## Claims left unverified (marked in the text)
- Excel `LINEST`, ToolPak, Google Sheets and Power BI trendline behaviour (Q61); not run.
- Poisson-library details, `RidgeCV`/`LassoCV`, `CalibratedClassifierCV` (Platt/isotonic), zero-inflated models, robust or quantile regression.
- McFadden "0.2 to 0.4 is good" rule of thumb (Q56); VIF thresholds of 5 to 10 and Cook's D "4/n" rule of thumb.
- DPDP Act and GDPR (Q69): principle only, labelled "from memory, unverified".
