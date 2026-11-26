# Review report: Book 9 Part 3 (decision trees, random forest), Wave C

## Counts
- Answers checked: 43 of 43.
- Code blocks run: 22 (Q1, Q14 test, Q16, Q24, Q26, Q28, Q29, Q30 check, Q31 check, Q32, Q34, Q35, Q36, Q39, Q40 table, Q41, Q43, Q27 simulation, plus the Q3 generator and Q6/Q12 numbers). All hand arithmetic recomputed by script: Q4, Q7, Q13, Q18, Q20, Q21, Q22, Q23 table, Q27 table, Q33, Q42 table, Q9 gaps (all correct).
- Answers changed: 20 (Q1, Q3, Q6, Q8, Q12, Q16, Q24, Q26, Q27, Q28, Q29, Q31, Q32, Q34, Q35, Q36, Q39, Q40, Q41, Q43). Answers with wrong numbers: 14.

## Main finding
The "synthetic attrition table" outputs came from a generator that was not in the file and could not be reproduced (the Q3/Q16 table also claimed 56% leavers while later answers said 24%). I wrote one documented generator `make_attrition(n_rows, seed=42, base=-1.4)` (given in Q3), re-ran every dependent answer with it, and replaced all outputs. Q29 (stores) reproduced exactly with the seed now stated.

## Fixes
| Q | Wrong or missing | Fix |
|---|---|---|
| Q1 | `employees` undefined | comment says the table is loaded as a DataFrame |
| Q3 | hidden data, 0.67/0.71 unreproducible | generator code added; now 1.00 train, tree 0.76, forest 0.79 test |
| Q6 | 0.76 train / 0.67 test unreproducible | rerun: 0.86 train, 0.80 test, gap 0.24 to 0.06 |
| Q8 | output line looked real | labelled illustrative |
| Q12 | 0.71 vs 0.67 | 0.79 vs 0.76 |
| Q16 | table, output 0.71, baseline "56% left" | real head rows, 0.79, baseline 75% stayed |
| Q24 | output 0.81/0.42/0.11 | rerun (stratified): plain 0.95/0/0, balanced 0.80/0.67/0.15 (8 of 12, 54 flagged); data recipe stated |
| Q26 | outputs and employee_id recipe | rerun; employee_id 0.280 built-in vs -0.020 permutation; recipe stated; pandas import added |
| Q27 | seed unspecified | `default_rng(42)` stated (363 reproduced) |
| Q28 | 50 flagged, 62% hit rate, rows | rerun: 52 flagged (ties), 44% vs 24% (1.9x); numpy import, sample rows |
| Q29 | pandas import, seed recipe | added (output reproduced exactly) |
| Q31 | 0.804 to 0.98 | rerun: 0.78 to 0.984 |
| Q32 | pandas import missing | added (output matches) |
| Q34 | 0.772 / 0.804 | 0.756 / 0.768 |
| Q35 | best 300 trees, F1 0.511/0.602 | best 100 trees, CV F1 0.424, test 0.447; "30 fits plus refit" |
| Q36 | 0.973/0.80/93 leaves | 0.983/0.76/77 leaves |
| Q39 | 0.972/0.804; fix code lacked import | 0.993/0.768, baseline 0.764 (so only barely above); import added |
| Q40 | whole table | rerun: 218, 45, 6, 3, 2 leaves; test 0.716 to 0.808 at alpha 0.005; text rewritten |
| Q41 | cut-offs 26.5/21.5/31.5 not reproducible, no code | code added; results 28.5, 28.5, 30.5; prose softened |
| Q43 | CV recall, 62%, 2.6x, 38% | rerun: recall 0.30-0.42, top 20% hit rate 44%, 1.9x, 56% of offers wasted; numpy import |

## Checked and correct (no change)
Q2, Q4, Q5, Q7, Q9, Q10, Q11, Q13, Q14 (scaling and string error verified), Q15, Q17, Q18, Q19, Q20, Q21, Q22, Q23 (default gini, table), Q25, Q30 (1 leaf for 9 rows; 2 leaves for 12), Q33, Q37, Q38, Q42 (default max_features sqrt, 100 trees verified on 1.9.1).

## Unresolved / report only
- Q3 and Q12 compare tree vs forest on 100 test rows (0.76 vs 0.79); text already calls it noisy.
- Q9 and Q25 tables are given in the question (not generated); only their arithmetic was checked.
- Q8 numbers are illustrative by design; Q43's "99% train" is an exercise value.
- Overlap: Q3, Q10, Q12, Q37, Q42 all touch forest vs tree and variance; Q6/Q36/Q40 overlap on overfitting controls; Q22 and Q33 repeat the same regression-split numbers. Intentional cross-references, not removed.
- Part title/target line says 38 target, 43 actual; ordering and stars untouched.

## Unverified claims (left as labelled)
Tiger Analytics, Fractal and Flipkart "reported" prompts and prep-site claims are snippet-level and marked unverified; XGBoost/LightGBM/CatBoost, DPDP Act/GDPR, `SimpleImputer`/`Pipeline` and native missing-value handling statements are marked "from memory, unverified". No em dashes in answer text; code fences balanced (64 fence lines).
