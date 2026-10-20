---

# Case Study 22 — Personalised coupons under a budget (Meituan Bike) · `cs22_coupon_allocation_uplift_budget.ipynb`

## D-22-01: Data source — synthetic customers with a hidden price-response model

- Date: 2026-10-19
- Case: 22
- Context / question: We need coupon-response data with a price ladder, a budget and a known truth, so every policy can be scored and an A/B test simulated.
- Options considered: public sets (Criteo Uplift, Hillstrom, Starbucks; none Indian, none with a price ladder or known truth); Meituan's data (confidential); synthetic data.
- Decision: 199,791 clean random-traffic users, 80,000 users under a targeting rule, 240,000 online users; price ladder ₹59 to ₹99; 12 features.
- Why: The twin gives exact expected revenue for any policy.
- Assumption checks / evidence: Random-arm conversion 13.08% (documented 12.93% in one Meituan city); balance tests 0 of 12 significant after Holm.
- Impact if wrong / mitigation: The size of personalisation gains depends on the assumed spread of price sensitivity; rerun on a real random-traffic experiment.

## D-22-02: Train on random traffic, keep a random slice

- Date: 2026-10-19
- Case: 22
- Context / question: Can we train the conversion model on logged, targeted data?
- Options considered: logs under a targeting rule; random traffic of the same size.
- Decision: Train and calibrate on random traffic; keep about 20% of traffic random (as Meituan did).
- Why: The model trained on logs sent everyone to ₹99 and earned ₹9.02 per user (-8.4% vs random); the random-traffic model earned ₹10.13 (+2.9%); difference ₹1.11 (CI 1.10 to 1.12).
- Assumption checks / evidence: 0% of log-trained curves fall with price vs 91% for the random-traffic model.
- Impact if wrong / mitigation: A random slice costs some revenue; size it against the retraining need.

## D-22-03: Isotonic calibration and monotone price curves

- Date: 2026-10-19
- Case: 22
- Context / question: Does the optimiser need calibrated, price-monotone probabilities?
- Options considered: raw gradient boosting; isotonic calibration plus a non-increasing-in-price step.
- Decision: Keep calibration and monotonicity as the safe default but re-examine it.
- Why: Raw curves rose with price for 5.2% of customers; after the fix 0%, PCOC 0.999. But calibration slope fell to 0.926 and revenue fell (₹10.17 vs ₹10.26 raw).
- Assumption checks / evidence: AUC 0.695 raw vs 0.694 calibrated; ECE 0.0041 vs 0.0071.
- Impact if wrong / mitigation: Try monotone constraints inside the model instead of pooled isotonic.

## D-22-04: Lagrangian solver with trisection

- Date: 2026-10-19
- Case: 22
- Context / question: How do we solve the budgeted allocation fast enough for real time?
- Options considered: exact linear programme; Lagrangian dual with trisection on the multiplier.
- Decision: Lagrangian with trisection.
- Why: Within 0.08% of the LP optimum and about 10 times faster (148 ms vs 1,553 ms on 3,000 customers); 240,000 customers solve in 6.96 s.
- Assumption checks / evidence: Lagrangian value ₹11.195 vs LP ₹11.186 per customer, at an average price of ₹78.76.
- Impact if wrong / mitigation: Integer rounding can leave a small budget gap; the PID controller corrects it.

## D-22-05: Do not replace the incumbent group-level allocation

- Date: 2026-10-19
- Case: 22
- Context / question: Should LDM-IR replace the 20-group allocation?
- Options considered: keep group-level; switch to LDM-IR; keep the manual rule.
- Decision: Keep the incumbent for now; do not ship LDM-IR.
- Why: LDM-IR ₹10.17 vs group-level ₹10.27 per user (-₹0.108, CI -0.115 to -0.099, Holm p < 0.001); it captures 22% of the oracle gain vs 29%. It does beat random by 3.3%.
- Assumption checks / evidence: Spearman of offered price with true sensitivity only -0.120 (oracle -0.878); the result runs against Meituan's reported gain.
- Impact if wrong / mitigation: The twin may understate what real features can capture; retest with real data.

## D-22-06: A/B test size and power

- Date: 2026-10-19
- Case: 22
- Context / question: Could a live test settle LDM-IR vs the incumbent?
- Options considered: 80,000 per arm; larger tests.
- Decision: Plan for about 1 million customers per arm for a 1% gap, or test a larger improvement.
- Why: The 80,000-per-arm test showed -₹0.20 (CI -0.47 to +0.06, p = 0.13); formula needs about 985,000 per arm; simulated power 3.5% to 12% at 10,000 to 80,000.
- Assumption checks / evidence: Revenue per user s.d. ₹26.9.
- Impact if wrong / mitigation: Use variance reduction or sequential testing to cut the size.

## D-22-07: Business case and assumptions

- Date: 2026-10-19
- Case: 22
- Context / question: What is the rupee value?
- Options considered: best, base (70% of point) and worst (CI low × 50%) scenarios.
- Decision: Assume 2 crore exposed users a month and 10% variable cost; report both comparisons.
- Why: Versus random: ₹4.9 crore a year base (₹3.4 to ₹7.0 crore); versus the incumbent: -₹1.6 crore base (-₹1.2 to -₹2.3 crore).
- Assumption checks / evidence: Exposure and cost are our assumptions, not documented.
- Impact if wrong / mitigation: Revenue is not profit; discounts may change reference prices and churn.

## D-22-08: Adopt PID control of the multiplier

- Date: 2026-10-19
- Case: 22
- Context / question: How do we stay on budget when traffic differs from plan?
- Options considered: fixed lambda planned offline; PID-adjusted lambda.
- Decision: Adopt PID control regardless of the allocator.
- Why: Fixed lambda ended at ₹77.81 (1.5% below budget) and below budget on 100% of 200 days; PID ended at ₹78.995 (error 0.006%), 0% of days below.
- Assumption checks / evidence: Maximum intraday deviation ₹1.45 vs ₹0.85.
- Impact if wrong / mitigation: Gains and gain size depend on the simulated traffic shift; tune on real traffic patterns.
