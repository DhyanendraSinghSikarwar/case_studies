---

# Case Study 18 — In-house score vs generic bureau score (Axis Bank) · `cs18_custom_score_vs_bureau.ipynb`

## D-18-01: Data source — synthetic applications with bureau-visible and internal-only risk

- Date: 2026-10-16
- Case: 18
- Context / question: We need bureau scores plus internal transaction data with outcomes.
- Options considered: public data (none; bureau scores are licensed); synthetic data.
- Decision: 150k applications over 18 months; thick/thin/no-hit bureau depth; 13 internal features.
- Why: Only synthetic data separate what each source sees.
- Assumption checks / evidence: Bad rate 5.7%; no-hit unrankable by the bureau.
- Impact if wrong / mitigation: Real gains depend on internal data richness.

## D-18-02: Synthetic parameters — equal bureau-visible and internal-only risk components

- Date: 2026-10-16
- Case: 18
- Context / question: How much should internal data know?
- Options considered: internal dominates; equal; bureau dominates.
- Decision: Equal weights (0.62 log-odds each), with bureau noise by depth.
- Why: A neutral assumption that yields a documented-size relative gain.
- Assumption checks / evidence: In-house KS +41% (the documented "40%" range).
- Impact if wrong / mitigation: Re-measure on real data.

## D-18-03: Four scorers out-of-time; DeLong + Holm

- Date: 2026-10-16
- Case: 18
- Context / question: Which comparison is fair?
- Options considered: bureau only; bureau + application; in-house; internal only.
- Decision: Train months 1–12, test 13–18.
- Why: Isolates the value of internal data and of combining.
- Assumption checks / evidence: In-house 0.668 vs bureau 0.628 (+0.041); internal-only 0.620.
- Impact if wrong / mitigation: None.

## D-18-04: Seven metrics of "% better" with paired bootstrap CIs

- Date: 2026-10-16
- Case: 18
- Context / question: What does "40% better" mean?
- Options considered: a single metric; a panel.
- Decision: Gini, AUC, KS, bad rate at 70% approval, approval at 3.5% bad, top-decile capture, Brier skill.
- Why: The documented metric is ND.
- Assumption checks / evidence: The range runs from +6.5% (AUC) to +100% (Brier skill); KS +41%.
- Impact if wrong / mitigation: None.

## D-18-05: Swap-set analysis at 70% approval

- Date: 2026-10-16
- Case: 18
- Context / question: Who does the new score approve differently?
- Options considered: aggregate metrics only; swap sets.
- Decision: Four-way table with Wilson CIs; z-test swap-in vs swap-out.
- Why: The standard credit-committee evidence.
- Assumption checks / evidence: Swap-in 5.6% vs swap-out 8.5% (p ≈ 7e-10); swap-out 27% no-hit.
- Impact if wrong / mitigation: None.

## D-18-06: Depth breakdown, calibration, monthly stability, PSI

- Date: 2026-10-16
- Case: 18
- Context / question: Where is the gain, and is it stable?
- Options considered: pooled only; by depth and by month.
- Decision: Per-depth DeLong; CITL and slope; monthly Gini trend; PSI.
- Why: Model-risk requirements.
- Assumption checks / evidence: No-hit +0.111 AUC; no trend (p = 0.84); PSI 0.000.
- Impact if wrong / mitigation: None.

## D-18-07: ₹ translation

- Date: 2026-10-16
- Case: 18
- Context / question: What is it worth?
- Options considered: fewer losses at fixed approval; more approvals at fixed risk.
- Decision: ₹1.5 lakh exposure, 65% LGD, ₹6,000 margin, 1 lakh applications/month.
- Why: Two levers the business can choose between.
- Assumption checks / evidence: ≈ ₹40 crore/year losses avoided (CI 26–53) or ≈ ₹20 crore/year with +10.8 pp approvals.
- Impact if wrong / mitigation: Assumptions are explicit.
