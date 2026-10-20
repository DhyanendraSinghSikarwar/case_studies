---

# Case Study 17 — Unified Ranking of Sponsored and Organic Products (Flipkart) · `cs17_ads_ranking_ctr_cvr.ipynb`

## D-17-01: Data source — synthetic impressions with a hidden click model and an exploration bucket

- Date: 2026-10-19
- Case: 17
- Context / question: We need impressions for ads and organic items, plus a known truth, so that a new ranking policy can be compared with pinned slots on the same candidates.
- Options considered: public CTR sets (Criteo, Avazu, KDD Cup, Taobao; none Indian, none with an organic/sponsored mix or counterfactual candidates); synthetic data.
- Decision: 80,000 requests over 14 days, 12 organic and 4 sponsored candidates each, legacy logging with ads pinned at slots 2 and 5, a 20% random-slotting exploration bucket (our assumption) and a hidden true click and order model.
- Why: Without the exploration bucket, slot and sponsorship are confounded (ads are 85% of impressions in slots 2 and 5, 5% elsewhere).
- Assumption checks / evidence: Exploration CTR slot 1 vs 8 is 4.72% vs 0.81%; exploration CTR organic 2.40%, ads 1.60%; CVR given click 9.3% vs 5.5%.
- Impact if wrong / mitigation: Lifts depend on assumed base rates and position bias; they show the method works in such a world, not Flipkart's lift.

## D-17-02: One model with the isAds flag and crosses, scored at slot 1

- Date: 2026-10-19
- Case: 17
- Context / question: Do we need the flag and crosses, or is an organic-features model enough?
- Options considered: M0 no flag; M1 flag and bid; M2 flag with crosses; M3 separate models; M4 gradient boosting.
- Decision: M2 (the documented design on our 7 base features), trained with the slot as a feature and scored at slot 1.
- Why: Ad AUC 0.7215 vs 0.7153 for M1, ad log loss lower by 0.0008 (Holm p = 0.04), Request AUC +0.0055 (CI 0.0004 to 0.0110); boosting is no better (AUC 0.7972).
- Assumption checks / evidence: Overall AUC gain is only 0.0015; bootstrap uses 100 resamples so the p-value floor is 0.01.
- Impact if wrong / mitigation: The gain is small in discrimination; the case for crosses rests on calibration (D-17-03) and revenue (D-17-04).

## D-17-03: Calibrate per population; check the slope, not only the mean

- Date: 2026-10-19
- Case: 17
- Context / question: Is the model calibrated for both ads and organic items?
- Options considered: overall calibration only; intercept and slope per population with cluster-robust tests.
- Decision: Report intercept, slope, ECE and exploration actual/predicted per population, and monitor them daily.
- Why: Mean actual/predicted is 1.002 to 1.015 for every model, but the ad slope is 0.78 (CI 0.72 to 0.85) without crosses and 0.996 (0.91 to 1.08) with them.
- Assumption checks / evidence: Ad intercept tests have wide CIs (about ±0.06); slope p-values are not Holm-adjusted; organic is slightly over-predicted on the exploration bucket (0.92 to 0.97).
- Impact if wrong / mitigation: Platt or isotonic recalibration per population if drift appears.

## D-17-04: Unified ranking replaces pinned slots; start at a moderate bid weight

- Date: 2026-10-19
- Case: 17
- Context / question: Does one score for ads and organic items beat pinned slots on both organic orders and ad revenue?
- Options considered: pinned (legacy); unified with each of five models at lambda = 1; oracle with true probabilities.
- Decision: Unified ranking with M2 for CTR and C2 for CVR.
- Why: At lambda = 1, M2 gives +14.2% organic orders (CI 13.9% to 14.4%) and +5.7% ad revenue (5.1% to 6.3%); M0 (no flag) gives +0.3% revenue (CI -0.3% to 0.9%); oracle +21.2% and +10.9%.
- Assumption checks / evidence: The CVR model is weak (AUC 0.630, 52 ad orders in test, no calibration problem detectable below about 25%); the scoring formula and the bid-per-click value are our assumptions.
- Impact if wrong / mitigation: A real auction and advertiser response change revenue; confirm in an A/B test.

## D-17-05: Bid weight chosen by "organic orders must not fall"; lambda = 3 is the upper end, not the launch value

- Date: 2026-10-19
- Case: 17
- Context / question: How should the weight on bids be chosen?
- Options considered: lambda in {0 to 5} on a tuning set; maximise ad revenue subject to organic orders not below pinned.
- Decision: Rule picks lambda = 3; test it as the upper arm and launch lower (lambda = 1 first).
- Why: Test set at lambda = 3: organic orders +1.5% (CI 1.2% to 1.8%), ad revenue +44.1% (43.6% to 44.5%), total orders +6.7%; but sponsored share goes from 25% to 39.6%. Lambda = 1 on tuning: +14.3% organic, +5.8% revenue.
- Assumption checks / evidence: The constraint held out of sample; M0 at its own lambda gives +3.2% organic and +37.6% revenue, so the best model depends on how the two metrics are weighted.
- Impact if wrong / mitigation: Shopper fatigue and long-term effects of a 40% ad share are not modelled; guard with a sponsored-share cap and counter metrics.

## D-17-06: Safe default for failed scores; redesign the circuit breaker

- Date: 2026-10-19
- Case: 17
- Context / question: What guard stops a scoring outage from flooding the page with ads?
- Options considered: default 0.5; safe default (mean ad pCTR); default 0.5 with a breaker that reverts when all four ads would be shown.
- Decision: Safe default plus alerting when more than 1% of scores hit the default; the breaker must trigger on score anomalies.
- Why: With 10% failed, the default 0.5 gives -7.0% organic orders vs pinned; the safe default gives +1.4%. Our breaker reverted 42% of requests with no failure, cut revenue lift from +44.1% to +10.6% and still ended -5.5% at 25% failures.
- Assumption checks / evidence: The "all four ads" threshold is our assumption, not the company's design.
- Impact if wrong / mitigation: Tune the trigger on real score distributions.

## D-17-07: ₹ business case — assumptions and scenarios

- Date: 2026-10-19
- Case: 17
- Context / question: What is the policy worth per year?
- Options considered: base volume of 3 crore requests a day; worst 1 crore (lower CI bounds); best 5 crore (upper CI bounds); company-reported lifts on our baseline.
- Decision: Value of an organic order ₹60, ad revenue as bid per click; report ₹128.5 crore a year base (₹25.7 crore organic, ₹102.8 crore ads), worst ₹40.8 crore, best ₹224.7 crore.
- Why: Company-reported lifts (+1.36% and +3.4%) on our baseline would be ₹31.7 crore. About 80% of the base value is ad revenue from the high bid weight.
- Assumption checks / evidence: At lambda = 1 the revenue lift is +5.7% (about ₹13 crore a year) with +14.2% organic orders.
- Impact if wrong / mitigation: Volume, order value and the click-price mechanism are assumptions; use the ranking of options more than the rupee level.

## D-17-08: A/B test design — size by metric, run at least a week, A/A check

- Date: 2026-10-19
- Case: 17
- Context / question: How big and how long should the test be?
- Options considered: analytic sample size from per-request variance; Monte Carlo at 1 million requests per arm; A/A tests.
- Decision: Three arms (pinned, lambda = 1, lambda = 3), at least a full week, sized for organic orders (the counter metric).
- Why: Ad revenue (+44.1%) needs about 2,517 requests per arm; organic orders (+1.47%) need about 2.81 million per arm (company's +1.36%: 3.26 million). Monte Carlo power at 1 million per arm is 40% for organic orders and 100% for revenue; A/A false-positive rate 5.0% and 3.0%, CI coverage 95.0% and 96.5%.
- Assumption checks / evidence: Outcomes are modelled as Poisson counts with request-specific rates; real traffic has repeat users and weekly cycles.
- Impact if wrong / mitigation: Add a design effect for repeated users; pre-register the decision rule (no harm on organic orders, positive ad revenue).
