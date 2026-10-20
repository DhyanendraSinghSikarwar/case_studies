---

# Case Study 25 — Predicting RTO on COD orders at checkout (Flipkart) · `cs25_cod_rto_prediction.ipynb`

## D-25-01: Data source — synthetic COD orders with hidden risk and social profiles

- Date: 2026-10-19
- Case: 25
- Context / question: The real orders and profile data are confidential; we need hidden truth to test selection bias and re-identification.
- Options considered: real data (not available); synthetic with a hidden logistic risk model, a legacy blocking rule and simulated profile matches.
- Decision: 40,000 random-control orders and 40,000 legacy-logged orders over 180 days, RTO about 32%, candidate profile for 50.3% of orders.
- Why: The documented RTO share (about 32%) and re-identification coverage (about 51%) are matched; the rest are our assumptions.
- Assumption checks / evidence: Clean data: 40,000 orders, RTO 31.77%, 21.0% with no history; 600 duplicates removed.
- Impact if wrong / mitigation: Signal strengths are assumed; our recall (25.9%) is below the paper's 40% to 60%; re-measure on real orders.

## D-25-02: Train on the randomised holdout, not the legacy-logged data

- Date: 2026-10-19
- Case: 25
- Context / question: Orders blocked by the old rule have no outcome, so a model trained on logs sees a biased sample.
- Options considered: train on legacy-logged shipped orders; train on the randomised control set.
- Decision: Keep a 5% randomised, un-intervened holdout and train and calibrate on it.
- Why: Legacy labels show RTO 27.1% vs 31.7% (z = -12.2); 56.2% of blocked orders would have been RTO. AUC is similar (0.787 vs 0.793) but the legacy model's false-positive rate is 4.65% against the 3% cap (control 2.78%) and PCOC is 0.971.
- Assumption checks / evidence: Time trend is not significant (odds ratio 1.012 per month, p = 0.058).
- Impact if wrong / mitigation: The holdout costs the RTO loss on 5% of risky orders; the cost is small against a biased cap.

## D-25-03: Match threshold of 0.6 for social features

- Date: 2026-10-19
- Case: 25
- Context / question: A lower threshold covers more users but lets wrong profiles attach someone else's attributes.
- Options considered: thresholds 0.4 to 0.95.
- Decision: Use social features only for users matched at 0.6 or higher.
- Why: Match precision 98.1% at 0.6 (94.3% at 0.4, 99.7% at 0.8) with 86.2% of found profiles kept; chi-square p = 3.3e-49; test AUC 0.8066 at 0.6, flat from 0.4 to 0.8.
- Assumption checks / evidence: The simulation knows the true match; real precision needs a labelled sample.
- Impact if wrong / mitigation: Monitor match precision on a labelled sample; tighten to 0.8 if it drops.

## D-25-04: Gradient boosting on history features as the base model

- Date: 2026-10-19
- Case: 25
- Context / question: Which model family, and do social features add value?
- Options considered: logistic regression, Random Forest, gradient boosting; three feature groups; no tuning.
- Decision: Gradient boosting; flag at a 3% false-positive cap set on out-of-fold scores.
- Why: History only AUC 0.7925 (LR 0.7580); full model AUC 0.8066, recall 25.9% (CI 24.3% to 27.9%), precision 81.6%, realised FPR 2.78%.
- Assumption checks / evidence: Social gain on all orders +0.0141 AUC, +2.2 points of recall (Holm p = 0.0013); re-identified users +0.0325 AUC, +5.7 points; thin history +0.0208 AUC, +4.4 points. The embedding adds only +0.0014 AUC.
- Impact if wrong / mitigation: Untuned models; the recall is low in absolute terms, and the tree families are not clearly different.

## D-25-05: Social features are useful but not free of risk: audit first

- Date: 2026-10-19
- Case: 25
- Context / question: Do social features create unequal false positives across occupation types?
- Options considered: ignore fairness; audit by hidden type.
- Decision: Add social features only after legal review and a fairness audit on real data.
- Why: False-positive rate ranges from 1.44% (senior manager) to 4.15% (other / not stated); omnibus chi2 = 11.5, p = 0.042; no pairwise gap survives Holm (smallest 0.067).
- Assumption checks / evidence: Group sizes are small (418 good orders for the lowest group); flag rates follow RTO rates by type.
- Impact if wrong / mitigation: Weak evidence either way; audit flag and false-positive rates by group before launch and offer prepay or verify, not a block.

## D-25-06: Capped threshold, not the cost-optimal rule, for the first launch

- Date: 2026-10-19
- Case: 25
- Context / question: Should the threshold follow a false-positive cap or the expected rupee saving?
- Options considered: 3% cap; cost-optimal rule from calibrated probabilities.
- Decision: Launch with the 3% cap; recalibrate before any cost rule.
- Why: Base case: capped ₹6,768 per 1,000 orders (CI 6,146 to 7,426) vs cost rule ₹17,689, but the cost rule flags 62.8% of orders and 52.3% of good orders.
- Assumption checks / evidence: Calibration slope 1.106 and Hosmer-Lemeshow p = 0.0035 (PCOC 1.005); the cost formula omits customer-experience loss.
- Impact if wrong / mitigation: If the A/B test shows a lower good-order loss than the assumed 25%, move toward the cost rule in steps.

## D-25-07: ₹ business case: about ₹24.7 crore a year (capped, base)

- Date: 2026-10-19
- Case: 25
- Context / question: What is the checkout flag worth at 1 lakh COD orders a day?
- Options considered: best, base and worst scenarios on nudge success and good-order loss.
- Decision: Plan on the base case with the worst case as the floor.
- Why: Capped: ₹12.2 crore worst (ρ 30%, φ 40%), ₹24.7 crore base (CI 22.6 to 27.0), ₹37.3 crore best.
- Assumption checks / evidence: The assumptions ρ and φ move the result by about a factor of three; the CI covers sampling only.
- Impact if wrong / mitigation: Measure ρ and φ in the A/B test before scaling.

## D-25-08: A/B test of the nudge on flagged orders

- Date: 2026-10-19
- Case: 25
- Context / question: How large must the test be?
- Options considered: effects of 20%, 35% and 50% on RTO among flagged orders; 80% power, alpha 0.05.
- Decision: Test with at least 764 COD orders in total (35% effect); 2,193 for a 20% effect.
- Why: Flagged precision 81.6%, flag share 10.2%; 112, 39 and 19 flagged orders per arm for the three effects.
- Assumption checks / evidence: Good-order loss needs a second primary outcome and a larger sample.
- Impact if wrong / mitigation: If the real effect is under 20%, the test will be underpowered; plan for 2,193 orders or more.
