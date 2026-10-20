---

# Case Study 21 — Membership programme retention (Zomato Gold / Flipkart Plus) · `cs21_membership_programme_retention.ipynb`

## D-21-01: Data source — synthetic customer-month panel with a hidden counterfactual

- Date: 2026-10-20
- Case: 21
- Context / question: Public method detail for how Zomato or Flipkart measured their membership programmes does not exist, and customer order logs are confidential. We need a setting where every estimator can be graded.
- Options considered: public order logs (none Indian, none with membership); synthetic data with hidden truth.
- Decision: 40,000 customers × 24 months, launch in month 12, self-selected joining, a random free-trial pilot, hidden counterfactual orders and contribution. Evidence level for the case is Weak; the notebook says so.
- Why: Selection bias can only be graded when the counterfactual is known.
- Assumption checks / evidence: 8,429 launch-month joiners; members already ordered more before launch (3.18 vs 2.64 orders a month).
- Impact if wrong / mitigation: Magnitudes depend on our selection and effect assumptions; the lessons about method behaviour carry over, the numbers do not.

## D-21-02: Analysis design — launch-month members vs never-members, pre window 6-11, post window 12-17

- Date: 2026-10-20
- Case: 21
- Context / question: How do we define treated and control cleanly in a staggered rollout?
- Options considered: all members vs all non-members; not-yet-treated controls; launch-month cohort vs never-joined.
- Decision: Launch-month joiners vs never-joined, both active in months 9-11 and not in the pilot; 1,981 vs 8,594 customers.
- Why: A single start date keeps pre/post well defined. "Never joined" conditions on the future, which we flag.
- Assumption checks / evidence: 4,927 later joiners dropped.
- Impact if wrong / mitigation: Use a not-yet-treated design for a multi-month rollout.

## D-21-03: Do not quote the naive uplift

- Date: 2026-10-20
- Case: 21
- Context / question: Can we report member-vs-non-member frequency as the programme effect?
- Options considered: naive cross-section; before/after; matching; DiD.
- Decision: No. The naive gap is +1.55 orders a month (+70%); the same gap before launch was +0.65; the true effect is +0.395 (+11.7%).
- Why: Selection on level and trend inflates every comparison.
- Assumption checks / evidence: Placebo gap significant (CI 0.54 to 0.75).
- Impact if wrong / mitigation: Re-check against a holdout.

## D-21-04: Matching and DiD are cross-checks only

- Date: 2026-10-20
- Case: 21
- Context / question: Do propensity matching and difference-in-differences recover the effect?
- Options considered: PSM on levels, PSM on levels plus trend, DiD with all controls, DiD matched v1 and v2.
- Decision: Treat them as cross-checks. Best balance (max |SMD| 0.04) still gave +0.92 and DiD +0.91 to +1.02 against a truth of +0.395; every CI missed.
- Why: Passing the pre-launch placebo (p = 0.35 to 0.85) did not protect against selection on recent orders and persistent trait.
- Assumption checks / evidence: Hidden counterfactual gap shown in 7.6.
- Impact if wrong / mitigation: Choose a pre window that excludes the months that triggered joining.

## D-21-05: Randomised free-trial pilot as the reference design

- Date: 2026-10-20
- Case: 21
- Context / question: What does a randomised nudge give?
- Options considered: ITT only; Wald/IV on joining in the launch month.
- Decision: Use the invitation as an instrument: first stage 40.6% vs 12.8% (F = 3,437), effect +0.33 orders a month (CI 0.24 to 0.43), which covers the truth.
- Why: Randomisation removes selection. Cost: the CI is 0.6 times the estimate and the result is for compliers.
- Assumption checks / evidence: Balance max |SMD| 0.027; joint test p = 0.05 (borderline).
- Impact if wrong / mitigation: Exclusion restriction assumed; check with a holdout.

## D-21-06: Contribution margin, not GOV, as the success metric

- Date: 2026-10-20
- Case: 21
- Context / question: Which metric decides expansion?
- Options considered: GOV, orders, retention, contribution margin per customer-month.
- Decision: Contribution margin. Matched GOV +₹521 and retention +13.2 points looked strong; margin was +₹1.8 (CI −4.3 to 7.8) against a true −₹37.7.
- Why: Free delivery on every member order costs more than the fee (₹49.7 a month) and extra orders bring in.
- Assumption checks / evidence: Pre-launch margin ₹57.7 an order.
- Impact if wrong / mitigation: Margin inputs are assumed; use finance data.

## D-21-07: Persistent holdout and tested redesign before expansion

- Date: 2026-10-20
- Case: 21
- Context / question: What should the company do next?
- Options considered: expand now; stop; holdout plus redesign.
- Decision: Keep a random holdout (about 911 per arm for a ₹10 margin change); test a higher fee, a free-delivery limit and lighter benefits for heavy orderers (matched margin effect −₹39 for the highest frequency tercile vs +₹43 for the lowest).
- Why: Subgroup estimates are biased but ordered plausibly; the average effect is likely negative.
- Assumption checks / evidence: Holm-corrected subgroup tests; uplift model found no reliable heterogeneity (p = 0.4).
- Impact if wrong / mitigation: Re-estimate on holdout data.

## D-21-08: ₹ business case as a range

- Date: 2026-10-20
- Case: 21
- Context / question: What is the programme worth per year?
- Options considered: naive claim; matched estimate with CI; hidden truth.
- Decision: Report the matched estimate as ₹1.9 crore a year (−4.6 to +8.4) for 9 lakh members, flag that a naive reading gives ₹97 crore and the hidden truth is about −₹41 crore.
- Why: The range shows how far method choice moves the answer.
- Assumption checks / evidence: 9 lakh is the documented company-reported scale, used only as a size; margin inputs assumed.
- Impact if wrong / mitigation: Treat as a range, not a forecast.
