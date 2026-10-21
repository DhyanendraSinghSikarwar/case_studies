# Book 1 Part 03 review notes

Reviewed: Q1-Q48 (all). No ANSWER_PENDING. All 48 have Say this first / Then explain / Example / Follow-ups / Common mistakes. CRLF line endings preserved.

## Header
- Added star counts (17 x 3-star, 21 x 2-star, 10 x 1-star = 48; recounted by grep). Removed stale "star counts may be stale" remark.

## Fixes
- Q19: added missing Example field (AP 0.340601 = sklearn; prf values).
- Q25: at_k run; code made standalone; example numbers were not reproducible, replaced (p@500 0.382, recall@500 0.317, cutoff 0.26, lift 6.3).
- Q32: code made standalone (defines cost, data, test used once); example replaced with run numbers.
- Q37: focal_loss run; added standalone training code (analytic gradient, L-BFGS); example numbers replaced with run numbers.
- Q40: kappa 0.70 verified (needs 50/50 marginals for both raters); wording fixed to state that assumption; snippet now builds the example and prints 0.85 / 0.70; human-human 0.78 labelled assumed.
- Q45: "8.9% positives" wording fixed. Original numbers not reproducible; regenerated: 9.4% in full set and stratified test split; buggy vs fixed numbers rerun; accuracy sentence corrected; fixed code made standalone; buggy snippet marked as fragment.
- Q30, Q31, Q39, Q41: hand arithmetic verified exact (0.486/0.083; 1.6% and 0.08% FPR; Rs 160,000 = Rs 16/customer; 1/21). Q39 labelled hand-computed/assumed. Added print to Q39 code.
- Q8, Q10, Q11, Q12, Q20, Q21, Q22, Q23, Q24, Q26, Q27, Q28, Q29, Q33, Q35, Q36, Q42, Q43, Q44, Q46, Q48: quoted numbers could not be reproduced from the shown code (no data/seed in the block); blocks made standalone with seeded synthetic data and quoted numbers replaced by the numbers actually printed. Material changes of story: Q8/Q11 class weights/SMOTE now tie with plain LR (0.222/0.225/0.225); Q12 test F1 slightly above validation (text said optimistic); Q20 example switched from RF to naive Bayes (RF was already well calibrated on the data); Q22 text says RF distortion is mild; Q35 data changed so boosting clearly beats logistic, DeLong number removed (not run); Q42 example now shows full AUC favours RF by 0.02 while TPR at 1% FPR is equal (original claim of a 33% gain not reproducible); Q46 c is biased low (0.222 vs true 0.30), stated.
- Q15, Q16, Q34, Q47: examples labelled illustrative/hand-built.

## Code run
- Re-extracted from the file and ran 26 blocks standalone (Q8,9,10,12,19,20,21,23-27,29,32,33,35,36,37,40,42-48): 25 pass; 1 expected non-standalone (Q45 buggy fragment, now marked). Output numbers match text.
- Blocks from my first scratch scripts that were not re-extracted but were run equivalently and matched: Q1, Q2, Q4, Q5, Q6, Q7, Q13, Q14, Q17, Q18, Q30, Q31, Q38, Q39, Q41 (all pass, numbers match).
- Not re-run: Q11 xgboost one-liner (marked not executed; xgboost is installed but no data), Q3/Q16/Q22/Q34 fragments (Q16, Q34 use undefined y_val/df/scores: illustrative skeletons, not marked individually), Q41 only function; Q2 etc fine.

## Unresolved / not verified
- Q16 and Q34 code blocks are fragments relying on undefined variables (y_val, scores, df); not run, not individually marked.
- Citations (Guo et al. 2017 temperature scaling; Kleinberg et al./Chouldechova impossibility; Hand & Till OvO; Elkan-Noto; RetinaNet gamma=2) are standard and kept; not web-verified.
- Q35 DeLong: no numeric result quoted.
- Q9, Q47 print little; Q47 outlier scores approximate.
