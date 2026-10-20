---

# Case Study 21 — Bayesian trend filtering for homepage personalisation (Paytm Labs) · `cs21_bayesian_trend_personalisation.ipynb`

## D-21-01: Data source — synthetic click logs with affinities and trends

- Date: 2026-10-16
- Case: 21
- Context / question: We need user × category click histories with platform trends.
- Options considered: MovieLens/RetailRocket/Open Bandit (no payment categories or festival trends; some Kaggle-hosted); synthetic data.
- Decision: 50k users × 12 categories × 56 days; true probabilities kept for a twin.
- Why: Indian payment-service categories and festival dynamics.
- Assumption checks / evidence: 1.31M clicks; median 15 per user.
- Impact if wrong / mitigation: The model form favours the documented formula, so a live A/B is required.

## D-21-02: Synthetic parameters — affinity × trend^r; heavy-tailed activity

- Date: 2026-10-16
- Case: 21
- Context / question: How do clicks arise?
- Options considered: affinity only; affinity × trend with heterogeneous responsiveness.
- Decision: The second option, with festival trends (gold ×5, movies ×3.5, flights ×3).
- Why: It captures the documented "interests + trending" idea.
- Assumption checks / evidence: Oracle top-3 CTR 65%.
- Impact if wrong / mitigation: Cross-category patterns are not simulated.

## D-21-03: DQ — remove bot first, then detect logging gaps

- Date: 2026-10-16
- Case: 21
- Context / question: What corrupts trend estimates?
- Options considered: check gaps on raw totals; remove bots and duplicates first.
- Decision: The second; exclude gap days from evaluation.
- Why: The bot's 4,800 daily clicks masked a 50% event loss.
- Assumption checks / evidence: Day 20 flagged only after bot removal.
- Impact if wrong / mitigation: Run monitoring in this order.

## D-21-04: Tuning — α and w on validation; empirical-Bayes α check

- Date: 2026-10-16
- Case: 21
- Context / question: How should the two dials be set?
- Options considered: fixed guesses; validation grid; Dirichlet–multinomial marginal likelihood.
- Decision: Grid on days 36–42; compare with the EB α.
- Why: Data-driven, with no test leakage.
- Assumption checks / evidence: α = 10 (grid) vs 10.9 (EB); w = 1 day.
- Impact if wrong / mitigation: Re-estimate monthly.

## D-21-05: Evaluation — next-day hit@3/NDCG/MRR/log loss; paired Wilcoxon + Holm; segments; spike days

- Date: 2026-10-16
- Case: 21
- Context / question: How should rankers be compared?
- Options considered: pooled metrics; per-user paired tests.
- Decision: Per-user mean hit@3 over 14 test days; Wilcoxon signed-rank with rank-biserial effect sizes; history segments (BH); spike vs normal days (Mann–Whitney).
- Why: Users are the unit; metrics are skewed and bounded.
- Assumption checks / evidence: Bayes +0.40 pp vs affinity (small), +11.1 vs trending, +9.2 vs MF; festival boost p = 0.054.
- Impact if wrong / mitigation: None.

## D-21-06: Digital-twin A/B on expected top-3 CTR

- Date: 2026-10-16
- Case: 21
- Context / question: What would an online test show?
- Options considered: offline only; twin with true probabilities.
- Decision: Expected top-3 CTR per policy with a paired bootstrap; oracle as headroom.
- Why: A noise-free online proxy.
- Assumption checks / evidence: Bayes at 93% of oracle; +0.26 pp vs affinity.
- Impact if wrong / mitigation: A live A/B is still needed.

## D-21-07: ₹ translation

- Date: 2026-10-16
- Case: 21
- Context / question: What are the gains worth?
- Options considered: CTR only; ₹ with assumptions.
- Decision: 1 crore visits/day; 35% conversion; ₹3 take per transaction.
- Why: Business-readable.
- Assumption checks / evidence: ≈ ₹50 crore/yr vs trending; ₹36 crore vs MF; ₹1 crore vs affinity; ₹18.5 crore headroom.
- Impact if wrong / mitigation: Linear in the assumptions.
