---

# Case Study 19 — A/B testing, variance reduction, peeking and switchback experiments (Cabify; Flipkart) · `cs19_experimentation_ab_testing.ipynb`

## D-19-01: Data source — two synthetic worlds with a hidden true effect

- Date: 2026-10-19
- Case: 19
- Context / question: We need experiments where the true effect is known, so that bias and coverage of each method can be measured.
- Options considered: public uplift or marketing A/B sets (no shared supply, no known truth); synthetic data.
- Decision: A homepage test (119,955 user rows, 14 days) and a minute-level marketplace (40,620 rows) with a hidden global-rollout effect.
- Why: No Indian company publishes experiment logs; only a simulation can show whether a method recovers the truth.
- Assumption checks / evidence: Data-quality issues injected and found: 1,500 duplicates, 25 users above ₹1 lakh holding 47% of revenue, 81 minutes with missing counts.
- Impact if wrong / mitigation: Effect sizes and the congestion curve are assumptions; re-estimate with an A/A switchback in each real marketplace.

## D-19-02: Check the sample ratio before reading any effect

- Date: 2026-10-19
- Case: 19
- Context / question: Is the homepage test valid enough to analyse?
- Options considered: analyse as is; exclude the affected cells; stop and fix.
- Decision: Exclude web users on days 5 and 6 from both arms (4,893 users) and ask engineering to fix the logging fault.
- Why: Overall treatment share was 49.1% (SRM p = 1.7e-9), concentrated in those cells (31% and 34% treated).
- Assumption checks / evidence: After exclusion share 49.8% (p = 0.262); joint covariate balance p = 0.688, all SMDs below 0.01.
- Impact if wrong / mitigation: The exclusion is only valid if the loss is unrelated to outcomes; keep an SRM gate (p < 0.001) on every test.

## D-19-03: Homepage — ramp on conversion, judge revenue on a holdback

- Date: 2026-10-19
- Case: 19
- Context / question: Do we ship the new homepage?
- Options considered: ship now; ship on conversion with a revenue holdback; extend the test.
- Decision: Ramp 10% to 50% to 100% and keep a 5% holdback for 4 to 6 weeks.
- Why: Conversion +8.6% relative (CI +0.32 to +0.94 points, Holm p = 0.0004); winsorised revenue +₹4.36 (CI -₹0.81 to +₹9.53) is not significant.
- Assumption checks / evidence: Guardrails non-inferior (page load +1.0%, support contacts +0.14 points with p = 0.047, close to its margin).
- Impact if wrong / mitigation: A conversion gain with no revenue gain would mean cheaper orders; the holdback tests that.

## D-19-04: Handling heavy-tailed revenue — winsorise at the 99.9th percentile

- Date: 2026-10-19
- Case: 19
- Context / question: How do we report revenue when a few users dominate it?
- Options considered: raw mean; Mann-Whitney; winsorised mean with bootstrap CI.
- Decision: Report winsorised revenue (cap ₹6,324) beside raw.
- Why: The raw difference (₹78.41, CI ₹8.84 to ₹147.99) comes from 25 users above ₹1 lakh (18 treated, 7 control); winsorising cuts the SE from 35.5 to 2.6.
- Assumption checks / evidence: Bootstrap CI for the winsorised mean -0.59 to 9.33 agrees with the analytic CI.
- Impact if wrong / mitigation: Winsorising hides real whale effects; keep the raw figure in the report.

## D-19-05: Variance reduction — linear ANCOVA by default; CUPAC not needed

- Date: 2026-10-19
- Case: 19
- Context / question: Which adjustment shortens tests?
- Options considered: CUPED (one covariate), ANCOVA (all pre-period covariates), CUPAC (gradient boosting, cross-fitted).
- Decision: ANCOVA by default.
- Why: Variance reduction is 7.6% (conversion) and 4.9% (revenue); CUPAC gives 8.1% and 4.9%, so the model adds almost nothing.
- Assumption checks / evidence: 400 A/A tests: false-positive rate 4.3% to 6.0%, mean estimates near zero.
- Impact if wrong / mitigation: The gain is small because pre-spend is weakly predictive (R² 0.05 to 0.08); test richer behavioural history.

## D-19-06: Sequential monitoring — O'Brien-Fleming boundaries if the team peeks

- Date: 2026-10-19
- Case: 19
- Context / question: What do we do about daily looks at the results?
- Options considered: fixed test; naive peeking; Bonferroni; Pocock; O'Brien-Fleming.
- Decision: O'Brien-Fleming with 5 looks when peeking is needed; otherwise a fixed test.
- Why: Naive peeking gives a 14.3% false-positive rate; O'Brien-Fleming gives 5.1% with 79.0% power (fixed 80.2%).
- Assumption checks / evidence: 20,000 A/A and 20,000 effect simulations per rule; first-look boundary 4.56.
- Impact if wrong / mitigation: Looks must be pre-planned and equally spaced; unplanned looks need an alpha-spending approach.

## D-19-07: Marketplace changes — paired-random switchback, not a user-level A/B

- Date: 2026-10-19
- Case: 19
- Context / question: How do we test a change that affects shared supply?
- Options considered: user-level A/B; alternating slots; random slots; paired-random slots with washout.
- Decision: Paired-random 53-minute slots, 10-minute washout, at least 14 days (28 preferred).
- Why: User-level A/B showed +7.2% against a true +4.1% and no success-rate loss against a true -1.49 points; alternating 60-minute slots had 0% coverage.
- Assumption checks / evidence: 120 replications: chosen design bias -0.6 points, RMSE 0.87, coverage 92%, A/A false-positive rate 4.2%; 29-minute slots had 13% coverage.
- Impact if wrong / mitigation: Residual bias of about -0.6 points does not shrink with duration; treat switchback estimates as a lower bound.

## D-19-08: Business case — ₹ ranges and the cost of the naive test

- Date: 2026-10-19
- Case: 19
- Context / question: What are the changes worth, and what does a wrong method cost?
- Options considered: point estimates only; worst/base/best scenarios.
- Decision: Homepage base case ₹16.3 crore a year contribution (range -₹0.3 to +₹41.3 crore); marketplace truth ₹44.5 crore a year.
- Why: The naive A/B implies ₹77.8 crore, an overstatement of ₹33.3 crore; the switchback gives ₹33.4 crore (CI ₹15 to ₹52 crore).
- Assumption checks / evidence: 2 crore users, 26 windows a year, 8% margin; 3 crore orders a month at ₹30 contribution; 50% to 100% of the effect persists.
- Impact if wrong / mitigation: Rupee levels depend on assumed volumes and margins; rely on the comparison between methods.
