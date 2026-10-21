# Book 1 Part 01 review

35 questions reviewed (14 x 3-star, 16 x 2-star, 5 x 1-star; header now states this). No ANSWER_PENDING. CRLF preserved.

## Fixes
- Q10, Q12: added missing **Example** fields (code was previously labelled with the output).
- Q11: quoted numbers were not reproducible (dataset unspecified). Added a demo to the code; numbers now 0.677 / 0.48 / 0.46 / 10.522 and coefficients [1.5 0.16 -0.05 -1.24 2.91], matching sklearn.
- Q12: inertia 733.9 not reproducible; now 1043.8 = sklearn 1043.8 (make_blobs 600, 4 centres), demo added.
- Q6: U-shape and outlier numbers were not in the code; added to code, numbers corrected (0.07/0.05; outlier 0.87->0.69, 0.99->0.96; old text said pearson flipped to -0.89).
- Q7/Q21: grouped-leakage numbers not reproducible; Q21 code made standalone (KNN, 200 users): random KFold 1.00, GroupKFold 0.54. Q7 text corrected and points to Q21.
- Q8: KNN scaling example now has code; 0.97 -> 0.66, tree 0.97 (old 0.86/0.49/0.83 unreproducible).
- Q14: "weights exploded to ~1e58" softened to what was measured (millions after 20 steps).
- Q22: added code; AUC 0.702 -> 0.865 (old 0.855/0.985 unreproducible).
- Q23: added data setup; nested 0.47 vs best_score_ 0.53 (old 0.41).
- Q25: timing claim replaced by measured noisy range (3-60x).
- Q30: added a standalone runnable demo. Old R2 0.756 / -0.907 were not reproducible (data undefined); now 0.983 vs -1.995 with defined synthetic data. Excerpts labelled as not standalone.
- Q32: variance 0.078 single vs 0.045 bagged; OOB 0.368 = 1/e; code extended.
- Q33: added demo; 2.8e-11 correct, 0.333 with doubled gradient.
- Q35: bias^2 = 0.002 (~0) with note not to read it as "trees unbiased"; variance 0.101; predicted 0.352 vs measured 0.353. No code block in the answer (derived by a script I ran, not included).
- Q20: rerun matches (1.0/0.88 vs 0.855/0.842); text already says the unconstrained forest is better on validation.
- Q28 already labelled illustrative. Header stale-star remark replaced.

## Code blocks (28 incl. new demos)
All runnable blocks run and match quoted numbers: Q1, 2, 5, 6, 7, 8, 10, 11, 12, 13 (matches sklearn, via separate harness), 14, 16, 17, 19, 20, 21, 22, 23, 25, 26, 27, 30 demo, 32, 33. Q18 is a fragment (needs df); its example (0.000-0.060 vs 0.020) was reproduced separately. Q30 buggy/fixed excerpts are not standalone (labelled). Q13 class block has no driver; iris example reproduced separately (1.0/.978, .962/1.0, .924/.978).
Failures found: none crashed; the failures were unreproducible numbers (above).

## Unresolved / not verified
- Q35 example and Q13/Q18 examples rely on scripts not embedded in the answer.
- Q3, Q24 (Ng & Jordan), Q23 (Bergstra & Bengio) citations are standard and recalled from memory, not web-checked.
- Q1 code prints "-0." for the tree train error (cosmetic).
