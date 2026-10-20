---

# Case Study 14 — Segmented underwriting vs one global model (Kissht) · `cs14_segmented_underwriting.ipynb`

## D-14-01: Data source — synthetic booked loans with structural segments

- Date: 2026-10-16
- Case: 14
- Context / question: We need loans with bureau depth, employment, repeat status and bank-statement features.
- Options considered: UCI Taiwan / German (no structure); Lending Club (Kaggle); synthetic data.
- Decision: 120k loans over 12 months; 12 segments; 17 features; 60+ DPD in 6 months.
- Why: No public Indian data with this structure.
- Assumption checks / evidence: Bad rate 7% (1.3–16% by segment).
- Impact if wrong / mitigation: Booked loans only, so approvals are a proxy.

## D-14-02: Synthetic parameters — segment-specific drivers

- Date: 2026-10-16
- Case: 14
- Context / question: How should heterogeneity be built in?
- Options considered: common drivers; segment-specific drivers.
- Decision: Thick files driven by bureau/DPD; thin/NTC by bounces, balances and digital score; self-employed by volatility/GST; repeat by own history. Repeat share grows over the year.
- Why: The premise of the documented segmentation.
- Assumption checks / evidence: LR χ² 1,168 confirms heterogeneity.
- Impact if wrong / mitigation: On real data, test heterogeneity first.

## D-14-03: Heterogeneity test — LR (Chow-type) with collinearity-safe interactions

- Date: 2026-10-16
- Case: 14
- Context / question: Do drivers differ by segment?
- Options considered: compare segment bad rates; an interaction LR test.
- Decision: Logit with segment dummies vs added segment × driver interactions. Bureau terms use a thick-file indicator because they are zero for NTC.
- Why: Differences in average bad rate alone do not justify separate models.
- Assumption checks / evidence: p ≈ 1e-238; slopes differ about 2× (bureau) and 0 vs 0.9 (bounces).
- Impact if wrong / mitigation: None.

## D-14-04: Model comparison — 5 scorers out-of-time; DeLong + Holm; within-segment BH

- Date: 2026-10-16
- Case: 14
- Context / question: Global or segmented, logistic or GBM?
- Options considered: bureau-only; global logit; global GBM; 12 segmented logit; 12 segmented GBM.
- Decision: Train months 1–9, test 10–12; pooled and within-segment AUC.
- Why: The decision is model architecture.
- Assumption checks / evidence: Segmented logit 0.857 ≈ global GBM 0.854 > global logit 0.847; segmented GBM 0.834.
- Impact if wrong / mitigation: None.

## D-14-05: Fragmentation sweep — 1 to 72 segments with EPV

- Date: 2026-10-16
- Case: 14
- Context / question: How many sub-models?
- Options considered: fixed 12; sweep 1–72.
- Decision: Segmented logistic at each granularity with bootstrap AUC CIs and min EPV.
- Why: The documented "39 sub-models" question.
- Assumption checks / evidence: Peak at 12 (0.857); 72 segments drop back to 0.847 with 66 segments below EPV 10.
- Impact if wrong / mitigation: The ceiling scales with defaults in the book.

## D-14-06: Top/bottom ratio, calibration, rank ordering, stability

- Date: 2026-10-16
- Case: 14
- Context / question: Is the documented ratio comparable, and is the model fit for use?
- Options considered: report the ratio alone; report it with definition sensitivity plus model-risk checks.
- Decision: Ratio by quintile/decile/ventile and population (bottom bucket with zero bads = ∞); per-segment CITL z-tests (Holm); Cochran–Armitage; PSI.
- Why: Model-risk standards.
- Assumption checks / evidence: Ratio 36× to ∞ for the same model; calibration MAE 0.42 pp; z = 42.6; PSI 0.003.
- Impact if wrong / mitigation: None.

## D-14-07: ₹ translation — approval rate at a 3% bad-rate target

- Date: 2026-10-16
- Case: 14
- Context / question: What is better ranking worth?
- Options considered: AUC only; approvals at a fixed loss (first tried 5%, too loose to discriminate).
- Decision: Largest safest-first approval share with cumulative bad ≤ 3%; ₹2,800 margin per good loan, 75% LGD; scaled to 1 lakh applicants/month.
- Why: The business lever is more approvals at the same risk.
- Assumption checks / evidence: Best models +₹3.2 crore/year vs global logit; bureau-only −₹115 crore.
- Impact if wrong / mitigation: Booked-loan proxy; use reject inference for real cut-offs.
