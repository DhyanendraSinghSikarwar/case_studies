---

# Case Study 23 — Transaction-purpose classification and life-event value (YES Bank) · `cs23_transaction_purpose_classification.ipynb`

## D-23-01: Data source — synthetic narrations in real Indian formats

- Date: 2026-10-17
- Case: 23
- Context / question: We need labelled bank narrations with downstream outcomes.
- Options considered: public categorisation sets (US/EU card data; Kaggle-hosted); synthetic narrations.
- Decision: 8,000 customers (≈ 240k transactions), 14 purposes, hand-labelled 12% with 5% noise, clean 4% audited test set, loan outcomes.
- Why: Real narrations are personal financial data.
- Assumption checks / evidence: Re-label audit: 4.0% label error.
- Impact if wrong / mitigation: Formats vary by bank; re-audit quarterly. (A first 20,000-customer version took 7+ minutes to generate, so the size was reduced.)

## D-23-02: Synthetic parameters — UPI/NACH/NEFT/IMPS/POS formats, Hinglish, typos, generic remarks

- Date: 2026-10-17
- Case: 23
- Context / question: How messy are narrations?
- Options considered: clean keywords; typos, truncation and generic remarks.
- Decision: 15% typos, truncation to 32–60 characters, 12% generic remarks.
- Why: Realism.
- Assumption checks / evidence: Keyword rules reach only 55%.
- Impact if wrong / mitigation: None.

## D-23-03: Models — keyword rules, char n-gram TF-IDF + logistic, MLP

- Date: 2026-10-17
- Case: 23
- Context / question: Which classifier?
- Options considered: rules; sparse linear; neural network (documented). MLP needed integer labels because of an sklearn early-stopping limitation with string labels.
- Decision: All three, trained on noisy labels, scored on the audited set; macro-F1 with bootstrap CIs; McNemar + Holm.
- Why: The documented neural network must beat a strong baseline to be justified.
- Assumption checks / evidence: 0.935 vs 0.918 vs 0.517.
- Impact if wrong / mitigation: None.

## D-23-04: Labels needed, noise and abstention

- Date: 2026-10-17
- Case: 23
- Context / question: How much labelling, and can unsure cases abstain?
- Options considered: learning curve; noisy vs clean labels; abstention thresholds with calibration (ECE).
- Decision: All of them; Wilson CIs on covered accuracy.
- Why: Labelling costs time; downstream products need reliable labels.
- Assumption checks / evidence: ≈ 5,000 labels give 0.91; noise costs 0.6 pt; τ = 0.6 → 90% coverage at 99.0%.
- Impact if wrong / mitigation: None.

## D-23-05: Downstream value test — DeLong on loan propensity

- Date: 2026-10-17
- Case: 23
- Context / question: Does the labelling pay off?
- Options considered: accuracy only; test whether life-event shares improve loan-uptake prediction.
- Decision: 50/50 customer split; base (income, age) vs + life events; DeLong + Holm; top-decile capture.
- Why: The business value is targeting.
- Assumption checks / evidence: Home loans AUC 0.537 → 0.679; education loans not shown (64 test takers).
- Impact if wrong / mitigation: Re-test with more customers.

## D-23-06: Evaluation hygiene — correcting a misleading check

- Date: 2026-10-17
- Case: 23
- Context / question: What does scoring on noisy labels show?
- Options considered: describe it as "inflated"; describe it accurately.
- Decision: The first run's text called the noisy-label score "inflated", but 91.3% is lower than the audited 93.5%. The wording was corrected and the notebook re-run.
- Why: Report what the number actually is: a distorted figure because of label errors.
- Assumption checks / evidence: 91.3% vs 93.5%.
- Impact if wrong / mitigation: None.

## D-23-07: ₹ translation

- Date: 2026-10-17
- Case: 23
- Context / question: What is it worth?
- Options considered: accuracy only; campaign margin.
- Decision: 10 lakh customers; top-decile campaign; ₹60,000 per home loan, ₹25,000 per education loan; ₹40 per contact.
- Why: Links accuracy to money.
- Assumption checks / evidence: ≈ +2,970 home-loan takers, ≈ ₹17.8 crore; education −₹0.6 crore (not significant).
- Impact if wrong / mitigation: Assumptions are explicit.
