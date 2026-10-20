---

# Case Study 1 — Delivery-time promise and live ETA (Swiggy) · `cs01_delivery_eta_prediction.ipynb`

## D-1-01: Data source — synthetic sessions, delivery legs, and a randomised promise offset

- Date: 2026-10-17
- Case: 1
- Context / question: We need cart sessions with both the shown promise and the outcome, plus a causal handle on what a promised minute costs.
- Options considered: public delivery datasets (none Indian, none with the shown promise or conversion); synthetic data.
- Decision: 220,000 sessions across 3 cities with four delivery legs, a legacy promise and a ±3 min randomised offset.
- Why: The conversion cost of a promised minute cannot be learned from observational logs alone.
- Assumption checks / evidence: Legs add up to the total within 0.02 min; covariates balanced across offsets.
- Impact if wrong / mitigation: Magnitudes are illustrative; the method transfers. Re-estimate with a real randomised test.

## D-1-02: Synthetic parameters — last mile dominates, legs negatively correlated

- Date: 2026-10-17
- Case: 1
- Context / question: How should delivery legs be modelled?
- Options considered: independent legs; legs linked through a rider-waiting mechanism.
- Decision: The second, so a rider who arrives early waits longer.
- Why: The documented stage-wise structure and the practical failure of summing independent leg models.
- Assumption checks / evidence: Last mile 54% of variance; wait vs first mile correlation −0.47.
- Impact if wrong / mitigation: Real correlations differ; test on real stage logs.

## D-1-03: Model choice — direct model for the total, joint network for stage-wise ETAs

- Date: 2026-10-17
- Case: 1
- Context / question: Predict the total directly, sum independent leg models, or use a joint model?
- Options considered: legacy promise, restaurant-hour mean, gradient boosting, four independent leg models, joint multi-output network.
- Decision: Gradient boosting for the cart promise; the joint network where stage consistency matters.
- Why: Boosting MAE 4.63 vs legacy 9.52 (paired ΔMAE −4.9, CI −4.96 to −4.82); summing independent legs 4.99 and biased by −2.8 min.
- Assumption checks / evidence: Time-based split (train to day 20, test the last week); Wilcoxon p < 1e-4.
- Impact if wrong / mitigation: Drift would erode the gain; monitor MAE and coverage weekly.

## D-1-04: Promise is a quantile — calibrate by binomial test

- Date: 2026-10-17
- Case: 1
- Context / question: What number should the customer see?
- Options considered: predicted mean; mean plus padding; quantile model at level τ.
- Decision: Quantile gradient boosting; coverage is checked against τ.
- Why: Coverage 50.3 / 60.4 / 70.3 / 79.9 / 89.8% for τ = 0.5…0.9, all binomial p > 0.14.
- Assumption checks / evidence: Calibration holds in almost every segment; fast-prep kitchens over-covered (81.5%, q = 0.0008).
- Impact if wrong / mitigation: Rain calibration is untested (dry test week); test before the monsoon.

## D-1-05: Estimate the cost of a promised minute from the randomised arm

- Date: 2026-10-17
- Case: 1
- Context / question: How much does a longer promise reduce orders?
- Options considered: observational slope; randomised ±3 min offset.
- Decision: Randomised logistic estimate, with the observational slope as a check.
- Why: OR 0.960 per minute (CI 0.954 to 0.967) vs observational 0.957; placement 69.3 / 66.8 / 63.9% at −3 / 0 / +3 min.
- Assumption checks / evidence: Covariates balanced across offsets.
- Impact if wrong / mitigation: Real observational slopes are usually more biased; keep the randomisation running.

## D-1-06: Pick the percentile by expected margin with a service guardrail

- Date: 2026-10-17
- Case: 1
- Context / question: Which τ should we ship?
- Options considered: τ = 0.5 to 0.9 on the test week.
- Decision: τ = 0.7 (+₹1.81 per session, 10.6% late by more than 5 min) over τ = 0.5 (+₹2.20, 20.0% late).
- Why: Legacy is already late 14.5% of the time; a rise to 20% is not acceptable when lateness costs are assumed small.
- Assumption checks / evidence: Margin ₹55, care contact ₹40, cancellation ₹180; 5 lakh orders a day.
- Impact if wrong / mitigation: Replace assumed costs with measured ones; the choice may move toward a higher τ.

## D-1-07: Live ETA — chain the stage models, accept real jumps

- Date: 2026-10-17
- Case: 1
- Context / question: Do chained stage models reduce ETA jumps?
- Options considered: independent stage models; chained models.
- Decision: Chained models; no extra smoothing at pickup.
- Why: Early-stage jumps fall ~10% (1.21 vs 1.35 min) but the pickup jump is 3.6 min either way, with 23% of customers seeing > 5 min.
- Assumption checks / evidence: Wilcoxon p < 1e-4.
- Impact if wrong / mitigation: A damper may hide real information; test the customer experience.

## D-1-08: Validation — switchback test, not a session-level A/B

- Date: 2026-10-17
- Case: 1
- Context / question: How should we test the new promise live?
- Options considered: session-level randomisation; city-hour switchback.
- Decision: Switchback with about 463 blocks per arm (about 9 days) for +1 pp conversion.
- Why: Sessions in a city-hour share rider supply and demand, so session-level randomisation understates variance; between-block SD of conversion is 0.054.
- Assumption checks / evidence: Session-level needs 34,550 per arm for +1 pp (138,746 for +0.5 pp).
- Impact if wrong / mitigation: Carry-over between blocks; add a washout period.
