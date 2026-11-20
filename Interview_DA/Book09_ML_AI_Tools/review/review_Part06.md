# Review: Book 9 Part 6 (overfitting, train/test split, feature engineering basics)
Reviewer: Wave C. Environment: Python 3.13, pandas 3.0.5, numpy 2.5.3, scikit-learn 1.9.1.

## Counts
- Answers checked: 39 of 39 (Q1 to Q39).
- Code blocks run: 27 interview code blocks (Q7, Q8, Q10, Q11, Q12, Q13, Q16, Q19, Q20, Q22, Q23, Q24, Q25, Q26, Q27, Q28, Q30, Q31, Q32, Q33, Q34, Q37, Q38, Q39 and the new Q1 block, plus Q10 and Q11 data-building blocks), plus script re-computation of every worked-example number, the Q21/Q22/Q20 arithmetic, TimeSeriesSplit blocks, and API claims.
- Answers with a wrong, unreproducible or changed item: 14 (Q1, Q2, Q3, Q4, Q6, Q10, Q11, Q13, Q14, Q15, Q16, Q18, Q19, Q23); Q31, Q37, Q39, Q12 got wording or label fixes only.
- All visible-code outputs (Q7, 8, 12, 16, 19, 20, 22 to 28, 30 to 34, 37 to 39) reproduced exactly on the installed versions. No visible output needed changing.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q1 | "Simulated 1,000 employees, seed 3" had no code; the numbers (100/64.8, 77.7/72.4) could not be reproduced | Wrote a seeded generator and the tree code, ran it, pasted code and real output into Q1; new numbers 100/66.0 and 73.6/69.2; flagged as invented, illustrative data |
| Q2 | Same hidden data (baseline 54.4/51.6, tree 77.7/72.4) | Recomputed on the Q1 data: baseline 52.3/56.4, depth 1 67.1/60.4, unlimited 100/66.0, depth 3 73.6/69.2 |
| Q3 | 64.8% held-out score, "wrong by 35 points" | 66.0%, 34 points |
| Q4 | Leaf-30 numbers (0.784/0.692, gaps 35.2 to 9.2) unreproducible | 0.739/0.708; gap 34.0 to 3.1; test score rose |
| Q14 | Same hidden numbers, gap 35.2 to 5.3 and +7.6 | Leaf 30: 0.739/0.708; depth 3: 0.736/0.692; gap 34.0 to 3.1 or 4.4; test +4.8 or +3.2 |
| Q15 | Depth table unreproducible; claimed test "falls" after depth 3 | New table (1: .671/.604, 3: .736/.692, 6: .805/.668, none: 1.0/.660); wording softened because depths 4 to 10 wobble (0.648 to 0.684) |
| Q18 | 0.808/0.652 vs 0.817/0.616 unreproducible and single-seed | Recomputed: 0.740/0.684 vs 0.768/0.657 (mean over 20 random-column draws; single draws 0.62 to 0.68 test). Noise-draw loop not shown in the answer |
| Q6, Q10 | Churn simulation had no code; "67% without the leaking column" not reproducible | Added data-building block to Q10; reran: 100% with the has-closed-date column (importance 1.0), 60% without; crosstab output (545/0/0/455) reproduced exactly |
| Q11 | Code not runnable (no imports, X and y undefined); output (50809, 43 / 50952, 45) unreproducible; scientific-notation risk | Added data block and imports; output now shows training-only vs all-rows means with labels (49996.9/46.1 vs 49634.5/45.6) |
| Q13 | Ten ages not given; code not runnable | Added ten ages and split (seed 42 puts both blanks in training). Verified median 33 (train 25,45,33,52,29) vs all-rows median 35.5 |
| Q16, Q19 | X and y undefined in code | Added sample-data blocks; output reproduced |
| Q23 | "Employee 3 / employee 2" ambiguous with zero-based row labels | Reworded to row 3 and row 2 with hire dates |
| Q31 | "I checked" noise claim (0.70 vs 0.50) vague | Reran with SelectKBest on 5 seeds: 0.70 to 0.80 leaky vs 0.39 to 0.57 in Pipeline; stated it is a separate script |
| Q37 | Random-forest claim 0.45 for group split | Reran: 0.96 random vs 0.42 group; described the generator |
| Q39 | TargetEncoder cross-fitting "from memory" | Verified on 1.9.1: fit_transform differs from fit().transform(); class params checked. (Note: `random_state` and `shuffle` args on TargetEncoder are deprecated in 1.9, not mentioned in answer) |
| Q12 | handle_unknown="ignore" "unverified" | Verified: unseen category gives all zeros |

## Confirmed correct (no change)
Q7 (800/200), Q8 (250/20/60), Q9 (60/20/20 arithmetic), Q20 (mean 0.8, sample sd 0.032, population 0.028), Q21 gaps, Q22 (z 2.4; distances 2000.2, 10000.0, 3.03, 2.00), Q24 (6 columns, Finance dropped), Q25 (fence 80), Q26 metrics, Q27 TimeSeriesSplit blocks, Q30 coefficients, Q33 skew 2.63 to 1.41, Q34 ratios, Q38 (depth 2, 0.818 CV, 0.787 test), 5-fold 400/100.

## Unresolved / for the chief editor
- Q1, Q2, Q3, Q4, Q10, Q14, Q15, Q18 numbers come from invented data and are labelled illustrative; Q18's 20-draw averaging and Q10's "60% without the column" and Q31/Q37 side checks are described but not shown as code.
- Q6 and Q10 share the churn simulation; Q1 to Q4, Q14, Q15, Q18 share the attrition simulation (cross-references kept).
- Overlap (report only): Q3/Q9/Q38 (test-set use), Q11/Q28/Q31 (preprocessing leakage), Q6/Q10/Q36 (leakage), Q1/Q2/Q15/Q21 (fit curves), Q12/Q24/Q39 (encoding). Intentional spiral but note for Book 9 dedupe.
- Ordering: stars descending and numbering continuous; Q19 to Q31 (2 stars) mix green/yellow/red order slightly (Q31 red before 1-star yellow is fine). Q16/Q17 (green) correctly lead the 2-star block.
- Asked-at lines follow the sources file ("commonly asked, no company-specific report"; Tiger Analytics bias-variance snippet in Q15 marked unverified). Not independently re-verified (no web).

## Claims left unverified (from memory)
SMOTE/imbalanced-learn (Q26, labelled), nested cross-validation (Q38, labelled), VIF thresholds and 0.8 to 0.9 correlation warning levels (rules of thumb, labelled), India DPDP Act and GDPR points and legal view on gender/age use in hiring (Q35, labelled, confirm with legal), model-family scaling rules (k-NN, SVM etc., standard knowledge, not run), Tukey 1.5 x IQR convention.
