---

# Case Study 15 — Wallet-behaviour score and BNPL limits (MobiKwik MobiScore) · `cs15_bnpl_limit_assignment.ipynb`

## D-15-01: Data source — synthetic wallet users in historical and randomised-limit cohorts

- Date: 2026-10-16
- Case: 15
- Context / question: We need wallet behaviour plus credit outcomes, and a way to learn limit effects.
- Options considered: historical data only (confounded); a randomised limit test (simulated).
- Decision: 132k pre-approved users; half with rule-based limits, half with random ₹1k/2k/3k/5k limits.
- Why: Limit effects are identifiable only under randomisation.
- Assumption checks / evidence: SRM p = 0.90; max |SMD| = 0.03.
- Impact if wrong / mitigation: A real test is needed; sample sizes are given.

## D-15-02: Synthetic parameters

- Date: 2026-10-16
- Case: 15
- Context / question: How do behaviour, limits and engagement drive outcomes?
- Options considered: limit affects spend only; limit affects spend and default, more so for low quality.
- Decision: The second option. Engagement drives cure strongly and default weakly. Revenue = 2% of spend + late fees; loss = 85% of utilised on default.
- Why: Documented engagement features; standard credit-line economics.
- Assumption checks / evidence: Default 5.7%; cure 47% vs 23% by contactability.
- Impact if wrong / mitigation: Margins are thin by assumption; the policy ranking is the transferable result.

## D-15-03: Score building — Mann–Whitney screening; logistic vs GBM; out-of-cohort test

- Date: 2026-10-16
- Case: 15
- Context / question: How should the score be built and validated?
- Options considered: in-sample AUC; train historical → test experiment.
- Decision: Train on the historical cohort, test on the experiment cohort; the limit is excluded from the score.
- Why: The score must describe the customer, not the decision.
- Assumption checks / evidence: Logistic AUC 0.714 vs GBM 0.702; bands from 2.0% to 15.6% default.
- Impact if wrong / mitigation: None.

## D-15-04: Engagement features — LR tests on default vs cure models

- Date: 2026-10-16
- Case: 15
- Context / question: Why include contactability and responsiveness?
- Options considered: default model only; separate cure model.
- Decision: Test both.
- Why: The documented interpretation (collections feasibility).
- Assumption checks / evidence: Default OR 0.88; cure OR 2.99 (LR χ² 1,393).
- Impact if wrong / mitigation: None.

## D-15-05: Causal limit effect — historical (naive/adjusted) vs randomised

- Date: 2026-10-16
- Case: 15
- Context / question: What does a higher limit do to default?
- Options considered: historical regression; the experiment.
- Decision: Report all three and use the experiment.
- Why: Confounding by the old rule.
- Assumption checks / evidence: Historical OR 0.89 (wrong sign); experiment OR 1.47 per +₹1k; heterogeneity by band p ≈ 3e-18.
- Impact if wrong / mitigation: None.

## D-15-06: Limit policy — design/evaluation split, IPW value, bootstrap

- Date: 2026-10-16
- Case: 15
- Context / question: Which limit per band?
- Options considered: uniform limits; old-rule tiers; the profit-optimal policy chosen on the design half.
- Decision: Evaluate on the other half with IPW (assignment probability 1/4) and a paired bootstrap.
- Why: Honest out-of-sample policy evaluation.
- Assumption checks / evidence: Optimal ₹30.1 vs uniform ₹1k ₹27.6 (+₹2.5, CI −1.4 to +6.1); old-rule tiers ₹23.2.
- Impact if wrong / mitigation: A larger holdout is needed (power table).

## D-15-07: ₹ translation

- Date: 2026-10-16
- Case: 15
- Context / question: How should results be expressed in ₹?
- Options considered: per user; scaled.
- Decision: Profit per user × 10 lakh pre-approved users per 6 months.
- Why: Comparable cycle figure.
- Assumption checks / evidence: Optimal ≈ ₹3.0 crore; old-rule tiers ₹2.3 crore; uniform ₹5k −₹14.5 crore.
- Impact if wrong / mitigation: Linear in volume; margin assumptions are stated.
