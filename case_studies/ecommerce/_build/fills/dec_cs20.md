---

# Case Study 20 — Predicting new-customer value before the first order (Swiggy) · `cs20_customer_lifetime_value.ipynb`

## D-20-01: Data source — synthetic customers with hidden true value

- Date: 2026-10-19
- Case: 20
- Context / question: We need pre-order signals, a 180-day outcome and a known true value so that bidding strategies can be compared.
- Options considered: public logs (none with acquisition context); synthetic data with a hidden latent value and an auction clearing price.
- Decision: 60,600 simulated customers (52 weeks of signups), 52 signals including 20 pure-noise columns, Food and Instamart outcomes, hidden columns prefixed `_`.
- Why: Swiggy's data and model details are not public; the evidence level is medium.
- Assumption checks / evidence: 40.0% zero 180-day value, mean ₹1,573 vs median ₹436, top 10% hold 58.1% of value.
- Impact if wrong / mitigation: Signal strengths and the auction are assumptions; re-measure on real data.

## D-20-02: Cleaning — drop refunds and bulk accounts, keep zeros

- Date: 2026-10-19
- Case: 20
- Context / question: Which rows are not ordinary new customers?
- Options considered: keep all; drop duplicates only; drop duplicates, negative-value and bulk accounts.
- Decision: Remove 600 duplicates, 14 negative-value rows and 38 bulk accounts (above ₹1 lakh); keep the true zeros.
- Why: Bulk accounts hold 12.2% of all value and would dominate any fit; zeros are 40.0% of customers and are real.
- Assumption checks / evidence: 59,948 customers remain; time-ordered split 41,560 / 9,246 / 9,142.
- Impact if wrong / mitigation: Bulk accounts need their own policy outside this model.

## D-20-03: Target handling — log and hurdle models, rank-based metrics

- Date: 2026-10-19
- Case: 20
- Context / question: How do we model a zero-inflated, heavy-tailed target?
- Options considered: squared error in rupees; log value with smearing; hurdle (P(any order) × value if active).
- Decision: Compare seven models and score by Spearman, top-decile capture and normalised Gini, not MAE.
- Why: Dispersion index 10.9; Gini 0.754; the best ranker (OLS-log) has MAE ₹9,709 against ₹1,807 for a constant mean.
- Assumption checks / evidence: Spearman 0.469 (OLS-log), 0.456 (hurdle GBM), 0.452 (MLP), 0.228 (segment mean), 0.241 (vendor-like).
- Impact if wrong / mitigation: The top four differ by 0.008 to 0.042; model choice should rest on calibration and cost.

## D-20-04: Calibrated model for any rupee decision

- Date: 2026-10-19
- Case: 20
- Context / question: Can the best ranker also set bid levels in rupees?
- Options considered: OLS-log; GBM on log value; hurdle GBM; GBM on raw value.
- Decision: Use OLS-log for ranking only; use hurdle GBM or raw-value GBM where the level matters.
- Why: OLS-log predicts 6.8× the actual total (CI 4.5 to 10.5); hurdle GBM 0.96 (CI 0.93 to 1.00); raw-value GBM 1.04.
- Assumption checks / evidence: Calibration slope hurdle 1.13 (p = 0.032), raw 1.00 (p = 0.94).
- Impact if wrong / mitigation: A budget-tuned multiplier removes the level problem for pure ranking bids.

## D-20-05: Bid on pLTV, not on 30-day conversion

- Date: 2026-10-19
- Case: 20
- Context / question: Does a long-horizon value score beat a short-term conversion model at equal spend?
- Options considered: flat bid; segment-mean pLTV; OLS-log; MLP; vendor-like 30-day model; oracle.
- Decision: Bid on the ranked pLTV score.
- Why: ROAS 49.1 vs 38.7 flat (+10.4, CI 7.9 to 12.6) and 40.9 vendor-like (+8.2, CI 6.1 to 10.8), Holm p = 0.02; zero-order share 19.8% vs 45.7%.
- Assumption checks / evidence: Second-price auction, clearing price from coarse signals; oracle ROAS 75.6.
- Impact if wrong / mitigation: Real auctions differ; run a randomised bidding holdout.

## D-20-06: Multi-task MLP kept for cost, not accuracy

- Date: 2026-10-19
- Case: 20
- Context / question: Does the documented multi-task structure (Food and Instamart heads) help?
- Options considered: one multi-task MLP; two single-task MLPs; three seeds each.
- Decision: Prefer the multi-task network only if parameter count or serving cost matters.
- Why: Total Spearman 0.4489 vs 0.4495 (paired p = 0.81); parameters 14,498 vs 28,930; ROAS vs OLS-log +0.80 (CI -0.25 to 1.95).
- Assumption checks / evidence: Three seeds, low power; permutation importance ignores noise columns (largest drop 0.0003).
- Impact if wrong / mitigation: Re-test with more seeds and richer features.

## D-20-07: Keep the 30-day proxy as an early indicator only

- Date: 2026-10-19
- Case: 20
- Context / question: Can 30-day orders replace the 180-day label?
- Options considered: 30-day orders as target; 180-day value as target.
- Decision: Train on 180-day value; use 30-day orders only for early monitoring.
- Why: Spearman 0.755 between 30-day orders and 180-day value, but 23.2% of customers with no 30-day order still order later and hold 20.3% of value.
- Assumption checks / evidence: 20.4% of top-decile customers had no order in 30 days.
- Impact if wrong / mitigation: A proxy must be validated against matured 180-day results.

## D-20-08: ₹ business case and holdout test size

- Date: 2026-10-19
- Case: 20
- Context / question: What is the value and how do we confirm it?
- Options considered: scenarios on the lower bound, estimate and upper bound of the ROAS gain.
- Decision: Assume ₹200 crore a year of spend and 8% margin; report ₹166 crore a year of extra contribution over flat bids (CI ₹127 to ₹201 crore); test with about 7,200 customers per arm for a 10% difference.
- Why: ROAS gain +10.4 (CI 7.9 to 12.6); SD/mean of value 2.1 gives 28,778 per arm for 5% and 7,195 for 10%.
- Assumption checks / evidence: The model buys 42% fewer customers (2,630 vs 4,553), so volume targets change.
- Impact if wrong / mitigation: The rupee level scales simulated ROAS; rely on the ranking of strategies.
