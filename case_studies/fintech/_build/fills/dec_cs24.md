---

# Case Study 24 — Validating CV motor inspection and auto-settlement triage (ICICI Lombard) · `cs24_motor_inspection_cv_validation.ipynb`

## D-24-01: Data source — simulated validation records, not images

- Date: 2026-10-16
- Case: 24
- Context / question: What data does the business decision depend on?
- Options considered: public damage images (research sets, Kaggle; no costs or claim outcomes) and training a CV model (outside the library list); simulate validation records.
- Decision: 24k inspections × 10 parts with model probabilities, surveyor re-inspection on 20%, costs.
- Why: Validation statistics are model-agnostic.
- Assumption checks / evidence: Part accuracy 93.7%; dents 59%, cracks 92%.
- Impact if wrong / mitigation: Re-run on real vendor output.

## D-24-02: Synthetic parameters — realistic CV failure modes

- Date: 2026-10-16
- Case: 24
- Context / question: How does the model fail?
- Options considered: uniform noise; class- and quality-dependent confusion.
- Decision: Dents mistaken for scratches, glare creating false scratches, accuracy rising with quality, 3% surveyor error.
- Why: Typical of damage-detection models.
- Assumption checks / evidence: κ = 0.70 vs surveyors.
- Impact if wrong / mitigation: Confusion patterns are assumed.

## D-24-03: Part-level validation — Wilson CIs, κ, error model on photo quality

- Date: 2026-10-16
- Case: 24
- Context / question: What are the model's strengths and weaknesses?
- Options considered: overall accuracy; per-class metrics.
- Decision: Per-class sensitivity/precision with Wilson CIs; κ; logistic LR test for photo quality.
- Why: Overall accuracy hides the dent weakness.
- Assumption checks / evidence: Photo-quality OR 0.80 per +0.1 (p ≈ 8e-23).
- Impact if wrong / mitigation: None.

## D-24-04: Pre-registered fit-for-purpose criteria

- Date: 2026-10-16
- Case: 24
- Context / question: What does "fit for purpose" mean?
- Options considered: accuracy threshold; business-risk criteria.
- Decision: ≤ 2% complex among auto-settled (one-sided 95% Clopper–Pearson); cost within ±₹3,000 for ≥ 80%; renewal sensitivity ≥ 90%.
- Why: Ties validation to decisions.
- Assumption checks / evidence: Criterion 1 UB 2.02% (not certified); criterion 3 met.
- Impact if wrong / mitigation: Report the shortfall rather than relax the criterion.

## D-24-05: Cost agreement — Bland–Altman

- Date: 2026-10-16
- Case: 24
- Context / question: Are cost estimates good enough?
- Options considered: MAE; Bland–Altman.
- Decision: Bias, limits of agreement, share within ±₹3,000 / ±15%, size-dependence regression.
- Why: Clinical-style method agreement analysis.
- Assumption checks / evidence: Bias −₹304; LoA ±₹10k; 55% within ±₹3k.
- Impact if wrong / mitigation: Restrict auto-settlement to low-cost claims.

## D-24-06: Triage rule — grid with Clopper–Pearson bound; sample-size table

- Date: 2026-10-16
- Case: 24
- Context / question: Which claims can be auto-settled?
- Options considered: cost cap × confidence grid.
- Decision: Choose the highest coverage meeting both criteria; otherwise report the closest. Rule-of-three sample sizes.
- Why: Safety with explicit uncertainty.
- Assumption checks / evidence: No rule certified; closest covers 5.4% (UB 2.02%); ≥ 600 checks needed.
- Impact if wrong / mitigation: Extend validation.

## D-24-07: ₹ translation

- Date: 2026-10-16
- Case: 24
- Context / question: What is it worth?
- Options considered: coverage only; ₹ with leakage.
- Decision: 80,000 claims/month; ₹1,500 per surveyor visit; ₹20,000 leakage per complex claim wrongly settled.
- Why: Leaders weigh savings against leakage.
- Assumption checks / evidence: ≈ ₹0.65 crore/month saved; leakage 0 measured (upper bound ≈ ₹3.5 crore).
- Impact if wrong / mitigation: Assumptions are explicit.
