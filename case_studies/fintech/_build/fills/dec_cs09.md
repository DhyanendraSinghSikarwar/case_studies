---

# Case Study 9 — Cross-bank typology-first mule model (RBIH MuleHunter.AI) · `cs09_mule_typology_alert_precision.ipynb`

## D-9-01: Data source — synthetic account aggregates for 6 banks + transaction-hour sample

- Date: 2026-10-16
- Case: 9
- Context / question: We need mule labels across several banks with typology behaviour.
- Options considered: public data (none; RTI declined); IBM AMLworld (transaction-level, Kaggle); synthetic data.
- Decision: 144k accounts, 6 banks, 8 typologies, 85% label coverage; a 28.8k-row hour sample.
- Why: Only synthetic data allows cross-bank and leave-one-typology tests.
- Assumption checks / evidence: Prevalence 0.8–1.8% by bank.
- Impact if wrong / mitigation: The method transfers; magnitudes are illustrative.

## D-9-02: Synthetic parameters — typologies, sleepers, hard negatives

- Date: 2026-10-16
- Case: 9
- Context / question: How hard should detection be?
- Options considered: strong typologies; 40% sleepers at 35% intensity plus genuine look-alikes.
- Decision: The second option, with a bank-specific typology mix and 3% of genuine accounts receiving one-off large credits.
- Why: The first calibration gave AUC 0.99 (too easy).
- Assumption checks / evidence: Raw AUC 0.90, typology AUC 0.96; legacy rule precision 4.7%.
- Impact if wrong / mitigation: Rules here are worse than the documented 20% precision.

## D-9-03: Night-activity test — circular statistics + KS + per-account Mann–Whitney

- Date: 2026-10-16
- Case: 9
- Context / question: How should "peak 11 PM–1 AM" be tested?
- Options considered: t-test on hours (wrong for clock data); circular statistics.
- Decision: Circular mean/R + Rayleigh; KS on hours; per-account window share with Mann–Whitney (clustering).
- Why: Hours wrap around; there are 12 transactions per account.
- Assumption checks / evidence: 21% vs 6% in the window; the circular mean is misleading because the distribution is bimodal.
- Impact if wrong / mitigation: Report the mode and window share.

## D-9-04: Typology-first vs raw; precision@k with paired bootstrap; DeLong

- Date: 2026-10-16
- Case: 9
- Context / question: Does expert feature design add value?
- Options considered: raw only; raw + 9 typology features.
- Decision: The same HGB, 2-fold cross-fitting, evaluated against hidden truth.
- Why: The documented "typology-first" claim.
- Assumption checks / evidence: AUC +0.062 (p ≈ 1e-60); precision@500 +22 pp.
- Impact if wrong / mitigation: None.

## D-9-05: Pooled vs bank-own; leave-one-bank-out; heterogeneity

- Date: 2026-10-16
- Case: 9
- Context / question: Does a central model help each bank, including new joiners?
- Options considered: bank-own models; pooled; LOBO.
- Decision: Per-bank PR-AUC/precision@0.5% with bootstrap; sign test; Cochran Q/I²; LOBO vs own.
- Why: The documented roll-out from 6 to 26+ banks.
- Assumption checks / evidence: Pooled wins 6/6 (p = 0.016); LOBO beats own by 4–25 pp; I² = 86%.
- Impact if wrong / mitigation: Per-bank monitoring is required.

## D-9-06: Generalisation and verification — leave-one-typology-out; label noise; audit design

- Date: 2026-10-16
- Case: 9
- Context / question: What are the model's limits, and how should "90% precision" be verified?
- Options considered: trust confirmed labels; random audit.
- Decision: LOTO recall; precision–volume curve vs truth and vs confirmed labels; n = 139 audit for ±5 pp.
- Why: Labels are incomplete and patterns grow (19 → 90).
- Assumption checks / evidence: Unseen typology −6 to −48 pp; confirmed-label precision understates by ~15 pp; simulated audit 98.6% vs truth 96.4%.
- Impact if wrong / mitigation: Maintain the library; audit quarterly.

## D-9-07: ₹ translation — investigator cost and mule inflow stopped

- Date: 2026-10-16
- Case: 9
- Context / question: How should the value be expressed?
- Options considered: precision only (documented); ₹ with stated assumptions.
- Decision: Scale to 10 crore accounts per 90 days; 45 min per alert; ₹600 per hour; 30% of a month's inflow stopped.
- Why: Leaders need capacity and ₹.
- Assumption checks / evidence: Same volume: 4.3× mules, ₹850 vs ₹196 crore stopped. At 90% precision: ₹0.6 crore wasted vs ₹198 crore.
- Impact if wrong / mitigation: The assumptions are explicit and adjustable.
