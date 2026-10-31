### Q21 ⭐⭐ 🟢 Fintech: A bank has 120 models in its inventory and 18 of them are in the high-risk tier. The independent validation team can complete 24 full validations a year and each high-risk model needs one every year. Compute how many validations remain for the other 102 models and how many years one pass over them would take, and say how you would tier models, trigger early reviews and use lighter-weight monitoring, leaving rules to compliance.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to model risk governance in general terms (tiering, validation capacity); related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** 18 of the 24 yearly validations go to the high-risk tier, so 6 are left for the other 102 models, and one full pass over them would take 102 / 6 = 17 years, which is why I tier by risk and use lighter monitoring instead of validating everything fully.

**Clarifying questions:**
- How does the bank define "high risk" today (materiality, customer impact, use in decisions)? It decides whether 18 is the right number or an artefact of the definition.
- What counts as a "full validation" and is there a cheaper lighter review? Without it the capacity maths is all-or-nothing.
- Are the 120 models independent, or do many share data, features or a vendor? Shared components can be validated once and reused.
- Which models changed recently or have known issues? That drives early reviews.
- Who owns the tiering policy and the review cadence? I will propose, compliance and model risk approve (rules are theirs, I would ask them what is mandatory).

**Approach:**
1. Do the arithmetic out loud: 120 - 18 = 102 other models; 24 - 18 = 6 spare validations; 102 / 6 = 17 years. That is not workable, so full validation of everything cannot be the plan.
2. Tier by a score of materiality (money or customers touched), complexity and opacity, data and vendor dependence, and how fast the world changes. Three or four tiers, written down, reviewed yearly.
3. Give each tier a cadence and depth. High: full validation yearly. Medium: full every few years plus a yearly light review. Low: light checklist plus automated monitoring only.
4. Define early-review triggers: a material model or data change, drift or performance alarms, a rise in overrides or complaints, a new use of the model, an incident, a vendor change.
5. Lighter monitoring for the lower tiers: input drift, output distribution, back-test of performance when labels arrive, data-quality checks, and an owner attestation. These are dashboards and tests, not new validations.
6. Show leadership the capacity table. If the tiered load still exceeds 24, say so and name the levers (staff, cadence, retire models, reduce the high-risk count by fixing the definition honestly).
7. Take the proposal to compliance and the model-risk owner. Ask them which cadences and documents are mandatory; I do not state them as facts.

**Metrics:**
- Validation capacity load = (sum of validations per year across tiers, in full-validation equivalents) / 24.
- Coverage = models reviewed within their tier cadence / models in inventory (target 100% for high).
- Backlog age = median days overdue for reviews past due.
- Trigger-to-review time = days from a trigger firing to the review starting.
- Guardrail: findings per validation by tier. If low-tier light reviews find nothing ever, the checks may be too weak; if they find a lot, the tier is wrong.

**Risks:**
- A "light review" becomes a rubber stamp. Sample some for a full re-check.
- Tiers gamed downward to save effort. Tier by an agreed score, not by who owns the model.
- Monitoring alerts nobody reads. Give each alert an owner and a response time.
- The capacity gap hidden by optimistic ratios (the light-review cost of 0.1 is invented; measure it).

**What the interviewer scores:**
- Strong: gets 102, 6 and 17 years fast, then moves to tiering and triggers instead of "hire more people". Weak: stops at the arithmetic or says "validate all of them slowly".
- Strong: separates what the data scientist proposes from what compliance mandates. Weak: invents regulatory rules.
- Strong: monitoring that is concrete (drift, back-test, overrides). Weak: "we will keep an eye on it".
- Strong: shows a capacity table with explicit assumptions. Weak: no numbers after the first calculation.

**Example:** With the invented split of 24 medium models (full every 3 years) and 78 low models (light review each year at 0.1 of a full validation), the load is 18 + 8 + 7.8 = 33.8 full-validation equivalents against 24 available. So even tiering does not fit, and I would say so.
- Weak: "We have 24 a year and 120 models, so we validate 24 each year and rotate." (Leaves 17 years of coverage and the high tier still takes 18 of the 24.)
- Strong: "Six slots are left for 102 models, 17 years for one pass. So I tier, give low-risk models a light yearly review, add triggers for early review, and bring the remaining gap of about 10 equivalents to the model-risk owner with options. Which cadences are mandatory is for compliance to confirm."

**Code:**
```python
# Q21 model inventory and validation capacity (illustrative numbers)
total, high, capacity = 120, 18, 24
others = total - high
spare = capacity - high            # validations left after the yearly high-risk cycle
years_all_full = others / spare
assert others == 102 and spare == 6 and years_all_full == 17.0
print(f"other models={others}, spare full validations/yr={spare}, years for one pass={years_all_full:.0f}")

# What if the other 102 are split into medium (24) and low (78) tiers?
# Illustrative cadence: medium = full validation every 3 years, low = light review every year
# (a light review costs 0.1 of a full validation, an invented ratio)
medium, low = 24, 78
med_load = medium / 3                    # 8 full validations/yr
low_load = low * 0.1                     # 7.8 full-validation equivalents/yr
need = high + med_load + low_load
assert med_load == 8.0 and abs(low_load - 7.8) < 1e-9 and abs(need - 33.8) < 1e-9
print(f"tiered load = {need:.1f} full-validation equivalents vs capacity {capacity}")
gap = need - capacity
assert abs(gap - 9.8) < 1e-9
print(f"gap = {gap:.1f} -> options: more staff, longer medium cycle, or fewer high-risk models")

# Longer medium cycle (every 4 years) and low light review at 0.05
need2 = high + medium / 4 + low * 0.05
assert abs(need2 - 27.9) < 1e-9
print(f"with medium every 4y and low at 0.05: {need2:.1f} (still above {capacity})")
```

**Output (my run):**
```text
other models=102, spare full validations/yr=6, years for one pass=17
tiered load = 33.8 full-validation equivalents vs capacity 24
gap = 9.8 -> options: more staff, longer medium cycle, or fewer high-risk models
with medium every 4y and low at 0.05: 27.9 (still above 24)
```

**Follow-ups:**
- What if all 18 high-risk models need a deeper validation than 1 slot each? Then fewer than 6 are spare, and I must cut scope or add capacity; I would not squeeze the high tier.
- How do you prevent models escaping the inventory? Procurement and deployment gates that require an inventory entry before go-live; ask the governance team how it is enforced today.
- Who validates the monitoring itself? A short periodic check by the validation team that alerts fire on known drifted data.

**Common mistakes:** Treating all models the same. Forgetting that 24 - 18 leaves only 6. Stating regulatory cadences as facts. Ignoring that light reviews also cost time. No early-review triggers.

### Q22 ⭐⭐ 🟢 E-commerce: Of 100,000 apparel orders, 12,000 (12%) are returned for size reasons, and a size widget was used on 20,000 orders: the size-return rate is 8% for widget orders and 13% for the 80,000 others (measured). The team claims that rolling the widget out would close the 5-point gap on all 80,000 other orders and save 150 per avoided return. Compute that claimed saving and explain why it is probably overstated and how you would test it.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to size recommendation and returns in fashion e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The claim is 80,000 x 5 points = 4,000 avoided returns x 150 = 600,000, but it is probably overstated because widget users chose to use it and not everyone will, so I would run a randomised test before banking it.

**Clarifying questions:**
- Who uses the widget today: everyone who sees it, or people who click it? If clicking is voluntary, the 8% group is self-selected.
- Is the 150 per avoided return a full cost (shipping both ways, handling, resale loss) or just shipping? It sets the value, and the number could be lower or higher.
- Are returns "for size reasons" coded by the customer or by an agent? Reason codes are noisy and a widget can change how people pick a reason.
- Does the widget change conversion (people buying less when told the fit is bad)? A lower return rate bought with lost sales is not a pure saving.
- Which categories and brands have widget coverage? Fit data may exist only for some products.

**Approach:**
1. Check the base: 20,000 x 8% = 1,600 and 80,000 x 13% = 10,400 give 12,000 returns, 12% of 100,000. The numbers are consistent.
2. Reproduce the claim: 5 points x 80,000 = 4,000 returns avoided x 150 = 600,000.
3. Name why it is too high: selection (engaged, careful shoppers use the widget and would return less anyway), a take-up below 100% (today only 20% use it), and the effect varying by category.
4. Show an adjusted number with stated assumptions, for example 20% use and a 2-point causal effect among users gives 320 avoided and 48,000. Say clearly that it is an illustration.
5. Test: randomise who is shown the widget (for example 50/50 at the session or user level, or by product page), keep the intent-to-treat comparison, and measure size-return rate per order.
6. Add guardrails: conversion, total return rate (all reasons), exchanges, and revenue per visitor.
7. Roll out in stages if the lift holds and report the number with an interval, not a point.

**Metrics:**
- Size-return rate = orders returned for size reasons / orders delivered, per arm.
- Intent-to-treat effect = rate in the widget-shown arm minus rate in the control arm, over everyone assigned.
- Net saving = avoided returns x cost per return minus lost margin from conversion change minus widget cost.
- Guardrails: conversion rate, total return rate, customer complaints, time to checkout.
- Count orders, not sessions, for the return denominator.

**Risks:**
- Comparing widget and non-widget orders and calling the gap an effect (selection bias).
- Assuming 100% take-up.
- Return reasons recoded after widget launch.
- Novelty: the effect fades after the first weeks.
- Fit data coverage uneven: gains concentrate in a few categories.

**What the interviewer scores:**
- Strong: gets 600,000 first, then says why it is an upper bound and names selection. Weak: only the arithmetic, or "the number is wrong" with no reason.
- Strong: proposes randomisation and says what is compared. Weak: "do an A/B test" without unit or metric.
- Strong: includes take-up and guardrails (conversion). Weak: ignores that fewer returns may mean fewer sales.
- Strong: labels the adjusted number as an assumption. Weak: presents an invented 2 points as a finding.

**Example:** 12,000 returns, 1,600 from widget users and 10,400 from the rest. Claim 4,000 x 150 = 600,000. Suppose only 20% of the other orders would use it and only 2 points of the gap is real: 80,000 x 0.2 x 0.02 = 320 avoided, 48,000 saved (illustrative). A test detecting 13% to 12% needs about 17,200 orders per arm (17,165 computed).
- Weak: "Widget users return 5 points less, so roll it out and save 600,000."
- Strong: "That 600,000 assumes everyone uses it and that the gap is all causal. Users chose it, so I would randomise exposure, read the intent-to-treat effect on size returns and check conversion, and then size the saving from the measured effect."

**Code:**
```python
# Q22 size widget claim (illustrative numbers)
orders, ret = 100_000, 12_000
w_n, o_n = 20_000, 80_000
w_rate, o_rate = 0.08, 0.13
w_ret, o_ret = w_n * w_rate, o_n * o_rate
assert w_ret == 1_600 and o_ret == 10_400 and w_ret + o_ret == ret
assert ret / orders == 0.12 and w_n + o_n == orders

gap_pts = o_rate - w_rate
avoided_claim = o_n * gap_pts
saving_claim = avoided_claim * 150
assert abs(gap_pts - 0.05) < 1e-12 and round(avoided_claim) == 4_000 and round(saving_claim) == 600_000
print(f"claimed: {avoided_claim:.0f} avoided returns, saving {saving_claim:,.0f}")

# Haircut 1: only some of the 80,000 will use the widget (today 20%)
use = w_n / orders
assert use == 0.2
# Haircut 2: only part of the 5-point gap is causal (invented: 2 points among users)
causal = 0.02
avoided_adj = o_n * use * causal
saving_adj = avoided_adj * 150
assert round(avoided_adj) == 320 and round(saving_adj) == 48_000
print(f"adjusted (20% use, 2-pt causal effect among users): {avoided_adj:.0f} avoided, saving {saving_adj:,.0f}")

# Selection story: if widget users were already lower-return, gap with zero causal effect
# Invented: engaged shoppers return 8% by themselves, others 13%: widget does nothing.
print(f"gap with zero causal effect is still {gap_pts*100:.0f} points in that world")

# Sample size for a randomized test to detect a 1-point drop from 13% (alpha 0.05, power 0.8), per arm
from statistics import NormalDist
z = NormalDist().inv_cdf
p1, p2 = 0.13, 0.12
n = (z(0.975) + z(0.8)) ** 2 * (p1*(1-p1) + p2*(1-p2)) / (p1 - p2) ** 2
assert 17_000 < n < 18_000
print(f"orders per arm to detect 13% -> 12%: {n:,.0f}")
```

**Output (my run):**
```text
claimed: 4000 avoided returns, saving 600,000
adjusted (20% use, 2-pt causal effect among users): 320 avoided, saving 48,000
gap with zero causal effect is still 5 points in that world
orders per arm to detect 13% -> 12%: 17,165
```

**Follow-ups:**
- What if you cannot randomise? Use a staggered rollout by product or region with a difference-in-differences read, and say the assumptions are weaker.
- Why intent-to-treat and not only widget users in the treated arm? Because users within the arm self-select again; assignment is the only random part.
- What about the 13% in the other group? It is the baseline you compare to the control arm, not a target.

**Common mistakes:** Multiplying the gap by all remaining orders. Treating users who chose the widget as a control. Forgetting take-up and conversion. Using sessions as the denominator.

### Q23 ⭐⭐ 🟡 Fintech: A monitoring system raises 10,000 alerts a month and analysts confirm 300 of them as suspicious (3%), with capacity to review 6,000 alerts. A model splits the alerts into three buckets: the top 3,000 alerts hold 270 confirmed cases, the middle 3,000 hold 24 and the bottom 4,000 hold 6 (retrospective counts). Compute the confirmed rate in each bucket and the share of confirmed cases found by reviewing the top two buckets, and explain what you would propose for the bottom bucket given that compliance owns any decision to stop reviewing alerts.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to KYC and AML alert triage in fintech material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The top bucket is 9.0% confirmed, the middle 0.8% and the bottom 0.15%, and the top two buckets (6,000 alerts, exactly the review capacity) hold 294 of 300 confirmed cases, 98%; for the bottom 4,000 I would propose a lighter-touch process and a sampled audit, and leave the decision to stop reviewing to compliance.

**Clarifying questions:**
- How were the "retrospective counts" produced: were all 10,000 alerts reviewed last month, or only some? If the bottom bucket was never reviewed, its 6 cases came from somewhere else and the 0.15% rate may be an undercount.
- What does "confirmed suspicious" mean: a filed report, an analyst opinion or a closed case? Label definition changes the rates.
- Is the model's score computed from the same signals that triggered the alert? If so, it may just be re-ranking rules.
- What is the cost of a missed case, and who owns it? I do not decide that, compliance does.
- How stable is the mix month to month? A split learned on one month can drift.

**Approach:**
1. Compute rates: 270 / 3,000 = 9.0%, 24 / 3,000 = 0.8%, 6 / 4,000 = 0.15%. Overall 300 / 10,000 = 3.0%.
2. Share found by the top two buckets: (270 + 24) / 300 = 98% using 6,000 reviews. Random order would find about 180.
3. Be honest about the 6 cases in the bottom bucket: 2% of confirmed cases. Whether they are material is a compliance question, not a modelling one.
4. Propose for the bottom bucket (as a proposal, not a decision): keep the alerts, route them to a faster lower-touch review or batch review, and audit a random sample every month.
5. Know the sample's limit: a 5% sample is 200 alerts with an expected 0.3 cases. You cannot track a 0.15% rate with that. Use a larger sample or a rolling quarter, or examine the 6 missed cases qualitatively.
6. Ask compliance in writing: may any alert class go unreviewed, with what sampling and sign-off, and what evidence they need (rates with intervals, the missed cases described).
7. Prospective check: run the model ranking in shadow for a few months so the numbers are not only retrospective, and re-validate the cut-offs.

**Metrics:**
- Confirmed rate per bucket = confirmed alerts / alerts in the bucket.
- Capture at capacity = confirmed in reviewed buckets / all confirmed (98%).
- Missed share = confirmed in unreviewed buckets / all confirmed (2% if bottom skipped).
- Review hours per confirmed case, per bucket.
- Guardrails: time-to-review for the top bucket, severity of missed cases, a shadow sample's confirmed rate by bucket.

**Risks:**
- Retrospective selection: if reviewed alerts were prioritised by the old rules, the bottom bucket was reviewed less thoroughly.
- Adversaries learn the pattern and aim at the "safe" bucket.
- Concept drift: the 0.15% is a month, not a law.
- Treating the model as the control. Compliance owns the control; the model supports prioritisation.

**What the interviewer scores:**
- Strong: all three rates and 98% right, plus "capacity equals the top two buckets". Weak: only accuracy-style talk.
- Strong: proposes sampling and low-touch review, defers the stop decision to compliance. Weak: "just drop the bottom 4,000".
- Strong: notes the sample-size problem of auditing a 0.15% bucket. Weak: "audit 5% and see".
- Strong: asks how retrospective labels were obtained. Weak: takes the counts at face value.

**Example:** 10,000 alerts, 300 confirmed. Top: 270 / 3,000 = 9%. Middle: 24 / 3,000 = 0.8%. Bottom: 6 / 4,000 = 0.15%. 294 / 300 = 98% found in 6,000 reviews. To see even one case in a random pull from the bottom bucket with 95% probability you need about 2,000 alerts.
- Weak: "98% recall, so we can stop reviewing the bottom bucket."
- Strong: "Reviewing the top two buckets catches 98% of confirmed cases with the capacity we have. I would not switch the bottom off myself: I would propose batch review and a monthly sample, show compliance the missed-case descriptions and rates with intervals, and let them decide."

**Code:**
```python
# Q23 alert triage buckets (illustrative, retrospective counts)
b = {"top": (3_000, 270), "middle": (3_000, 24), "bottom": (4_000, 6)}
total_alerts = sum(n for n, _ in b.values())
total_conf = sum(c for _, c in b.values())
assert total_alerts == 10_000 and total_conf == 300
rate = {k: c / n for k, (n, c) in b.items()}
assert round(rate["top"], 4) == 0.09 and round(rate["middle"], 4) == 0.008 and round(rate["bottom"], 5) == 0.0015
print({k: f"{v:.2%}" for k, v in rate.items()}, f"overall {total_conf/total_alerts:.1%}")

top2 = b["top"][1] + b["middle"][1]
share = top2 / total_conf
assert top2 == 294 and share == 0.98
print(f"top two buckets: 6,000 alerts, {top2} of {total_conf} confirmed = {share:.0%}")
print(f"missed if bottom never reviewed: {b['bottom'][1]} cases ({b['bottom'][1]/total_conf:.0%})")

# Lift versus random review of 6,000 alerts
random_found = 6_000 * (total_conf / total_alerts)
assert random_found == 180
print(f"random order would find ~{random_found:.0f}; model finds {top2}")

# Sampling the bottom bucket: how many to read to expect to see >=1 case with 95% probability at 0.15%?
import math
n95 = math.log(0.05) / math.log(1 - rate["bottom"])
assert 1_990 < n95 < 2_010
print(f"alerts to sample for 95% chance of seeing one case at 0.15%: {n95:,.0f}")
# A 5% monthly sample of the bottom bucket
sample = 0.05 * 4_000
exp_cases = sample * rate["bottom"]
assert sample == 200 and abs(exp_cases - 0.3) < 1e-9
print(f"5% sample = {sample:.0f} alerts, expected cases {exp_cases:.1f}: far too few to track the rate monthly")
```

**Output (my run):**
```text
{'top': '9.00%', 'middle': '0.80%', 'bottom': '0.15%'} overall 3.0%
top two buckets: 6,000 alerts, 294 of 300 confirmed = 98%
missed if bottom never reviewed: 6 cases (2%)
random order would find ~180; model finds 294
alerts to sample for 95% chance of seeing one case at 0.15%: 1,996
5% sample = 200 alerts, expected cases 0.3: far too few to track the rate monthly
```

**Follow-ups:**
- Why not move the bucket edge instead? You can, but the middle bucket still holds 24 cases; edges follow cost and capacity, and I would show the marginal cases per extra 1,000 reviews.
- How would you improve the model? Features from entity history and network links, and label the ones analysts rated "borderline" rather than binary only.
- What if analysts' capacity falls to 4,000? Then the top bucket plus 1,000 of the middle; show the capture curve.

**Common mistakes:** Calling 98% "recall of fraud" when it is recall of confirmed alerts in last month's data. Forgetting that the overall base rate is 3%. Dropping a bucket without compliance. Assuming 5% sampling measures a 0.15% rate.

### Q24 ⭐⭐ 🟡 E-commerce: In a randomised test, 10,000 cart abandoners received a reminder with a 10% discount code and 6.0% purchased, against 5.0% of 10,000 randomly held-out abandoners, and the average order value is 800 with a 25% margin before any discount. Compute the incremental orders per 10,000 abandoners, then compare the margin on them with the discount given if all 600 purchasing recipients use the code. What would you change about the offer and the targeting?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to cart abandonment and discount incrementality in e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** The reminder created 600 - 500 = 100 extra orders per 10,000, worth 100 x 200 = 20,000 of margin, but if all 600 buyers use the 80 discount that costs 48,000, so the offer loses about 28,000 per 10,000 abandoners.

**Clarifying questions:**
- How many buyers actually redeem the code? "All 600 use it" is the worst case for cost; redemption below 100% changes the answer (the net is -28,000 at 100% and -4,000 at 50%, and only turns positive below about 42% redemption).
- Are the 800 order value and 25% margin the same for incremental buyers as for baseline buyers? Discount-driven buyers may buy smaller baskets.
- Does the reminder alone (without a code) already lift purchase? The test mixes reminder and discount, so I cannot separate them.
- Is there a long-run effect: do buyers learn to abandon and wait for a code? One 30-day window may miss it.
- Is 25% margin before discount including shipping and payment fees? It sets the break-even.

**Approach:**
1. Incremental orders: 6.0% - 5.0% = 1.0 points x 10,000 = 100. Check the lift is not noise: z is about 3.1 on 10,000 per arm, so it is unlikely to be chance (I report the z and the setup, not a claim beyond it).
2. Margin on incremental orders: 100 x 800 x 25% = 20,000.
3. Discount given if all 600 purchasers use the code: 600 x 80 = 48,000. Net: -28,000 per 10,000.
4. Name the mechanism: 500 of the 600 buyers would have bought anyway, so most of the discount subsidises people who needed no incentive.
5. Break-even: with all buyers redeeming, I need about 333 incremental orders per 10,000 (8.3% purchase rate versus 5.0%), over three times the observed lift.
6. Change the offer: test a smaller discount, a reminder without a code, free shipping or a time-limited code, and a code that applies only to a threshold basket.
7. Change the targeting: hold out or skip high-propensity abandoners (those most likely to buy anyway), and give the code only to the middle group using an uplift model trained on this randomised data.
8. Re-test with three arms (no reminder, reminder only, reminder with code) so the discount's own incremental effect is measured.

**Metrics:**
- Incremental orders per 10,000 = purchases in treated minus purchases in holdout, same denominator.
- Incremental margin = incremental orders x AOV x margin rate.
- Discount cost = redeemed codes x discount amount, including codes redeemed by baseline buyers.
- Net per 10,000 = incremental margin - discount cost.
- Guardrails: AOV, return rate, repeat purchase in 60 days, unsubscribe rate.

**Risks:**
- Redemption below 100% makes the offer look better; measure it, do not assume.
- Margin for incremental orders may be lower than 25%.
- Training buyers to wait for codes.
- Targeting on past redemption only reinforces who already buys.
- Window too short: a pull-forward from later purchases would make incremental look larger than the true effect.

**What the interviewer scores:**
- Strong: 100 orders, 20,000, 48,000, net -28,000, all hand-checkable. Weak: "6% beats 5%, so it works."
- Strong: points out the 500 baseline buyers receive the discount. Weak: calls the code a "cost of acquisition" and stops.
- Strong: proposes a three-arm test and uplift targeting. Weak: "make the discount smaller" with no test.
- Strong: asks about redemption rate. Weak: assumes 100%.

**Example:** Per 10,000: 600 treated buyers vs 500 held out. Margin on 100 extra orders = 20,000. Discount if all 600 redeem = 48,000. With 50% redemption (illustrative) the discount is 24,000 and the net is -4,000; 70% gives 33,600 and -13,600. The same 100 extra orders only pay for the discount if redemption is below 41.7% (20,000 / 48,000).
- Weak: "The test is significant, so send the code to everyone."
- Strong: "The lift is real but small: 100 orders is 20,000 of margin against up to 48,000 of discount, because 500 of the 600 buyers would have bought anyway. I would test a reminder without a code and a smaller offer, and aim the code at people with the highest uplift."

**Code:**
```python
# Q24 cart reminder with 10% code (illustrative numbers)
from math import sqrt
n = 10_000
t_buy, c_buy = 600, 500
assert t_buy / n == 0.06 and c_buy / n == 0.05
incr = t_buy - c_buy
assert incr == 100
aov, margin = 800, 0.25
unit_margin = aov * margin
assert unit_margin == 200
incr_margin = incr * unit_margin
assert incr_margin == 20_000
disc_each = 0.10 * aov
discount_all = t_buy * disc_each
assert disc_each == 80 and discount_all == 48_000
net = incr_margin - discount_all
assert net == -28_000
print(f"incremental orders {incr}, margin on them {incr_margin:,.0f}, discount if all 600 use code {discount_all:,.0f}, net {net:,.0f}")

# Is 6.0% vs 5.0% a real lift? two-proportion z
p = (t_buy + c_buy) / (2 * n)
se = sqrt(p * (1 - p) * 2 / n)
z = (0.06 - 0.05) / se
assert 3.0 < z < 3.2
print(f"z = {z:.2f}")

# Break-even incremental orders x with all buyers using the code: x*200 = (500+x)*80
x = 500 * disc_each / (unit_margin - disc_each)
assert abs(x - 333.333) < 0.01
print(f"break-even incremental orders per 10,000: {x:.0f} (purchase rate {(500+x)/n:.2%} vs 5.00% baseline)")

# Net per 10,000 if only a share of purchasers redeem (invented redemption rates)
for r in (1.0, 0.7, 0.5):
    cost = r * t_buy * disc_each
    print(f"redemption {r:.0%}: discount {cost:,.0f}, net {incr_margin - cost:,.0f}")
assert incr_margin - 0.5 * t_buy * disc_each == -4_000
be = incr_margin / (t_buy * disc_each)
assert abs(be - 0.41667) < 1e-4
print(f"break-even redemption (same 100 extra orders): {be:.1%}")
# Smaller offer: 5% off with the same 100 incremental (only if lift held, a big if)
small = 0.05 * aov * t_buy
print(f"5% code, same lift, 100% redemption: discount {small:,.0f}, net {incr_margin - small:,.0f}")
assert small == 24_000 and incr_margin - small == -4_000
```

**Output (my run):**
```text
incremental orders 100, margin on them 20,000, discount if all 600 use code 48,000, net -28,000
z = 3.10
break-even incremental orders per 10,000: 333 (purchase rate 8.33% vs 5.00% baseline)
redemption 100%: discount 48,000, net -28,000
redemption 70%: discount 33,600, net -13,600
redemption 50%: discount 24,000, net -4,000
break-even redemption (same 100 extra orders): 41.7%
5% code, same lift, 100% redemption: discount 24,000, net -4,000
```

**Follow-ups:**
- What if the discount is a fixed 80 off a minimum basket of 1,000? It filters to bigger baskets, but it still goes to baseline buyers; test it.
- How do you pick the targeting group? Fit an uplift model on the randomised arms, check the lift by decile on a holdout, send to the deciles with positive net.
- Is a 10-point discount ever worth it? Yes if the incremental orders carry enough margin or lifetime value; that is an assumption to test, not to presume.

**Common mistakes:** Treating all 600 buyers as incremental. Ignoring that baseline buyers redeem the code. Counting the discount only on the 100 incremental orders and forgetting that the 500 baseline buyers redeem it too. Reading significance as profitability.

### Q25 ⭐⭐ 🟡 Healthcare: A chest X-ray model is tested on 10,000 images, 8,000 from scanner A and 2,000 from scanner B, with 10% of images abnormal in both groups. At the deployed threshold its sensitivity is 88% on scanner A and 71% on scanner B (measured). Compute the overall sensitivity and the abnormal scans missed in each group, and say how you would investigate the gap and what you would do before the hospital adds a third scanner model.
**Asked at:** Clinical-ML deployment material (a physician-oriented dataset-shift article, an arXiv paper on what clinicians want from explainable ML, a JMIR paper on alarm fatigue and a circEWS slide deck on calibration and prevalence); research and secondary sources rather than interview banks; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Overall sensitivity is 846 of 1,000 abnormal scans, 84.6%, but that hides 96 missed on scanner A and 58 on scanner B, so scanner B misses 29% of its abnormal cases against 12% on A, and I would not let a third scanner in until it has its own validation.

**Clarifying questions:**
- Is the threshold the same for both scanners, and where was it tuned? If it was tuned on scanner A, B is just off-operating-point.
- Are the 2,000 scanner B images from the same patients, wards and indications as A? A different case mix would fake or hide a gap.
- Who labelled the images and how (radiologist read, follow-up)? Label quality may differ by scanner.
- Was scanner B represented in training? If not, it is a domain shift problem.
- What is the clinical cost of a miss versus a false alert, and who owns the decision to use the tool on B? Ask the clinical safety team.

**Approach:**
1. Compute abnormal counts: 800 on A (10% of 8,000) and 200 on B (10% of 2,000).
2. True positives: 704 (A) + 142 (B) = 846, so overall sensitivity is 84.6%. Missed: 96 + 58 = 154.
3. B is 20% of images but 38% of misses (58 / 154).
4. Is the gap real? 200 abnormal cases is a small sample, but the 95% Wilson intervals (about 64.4-76.8% for B and 85.6-90.1% for A) do not overlap, and the gap has z of about 5. I would treat it as real and investigate.
5. Investigate: sensitivity versus threshold per scanner (ROC per scanner), case-mix check (finding type and size, view, patient factors), image properties (contrast, resolution, post-processing), label audit, and what B images look like in the model's embedding space.
6. Quick mitigations: scanner-specific threshold only if it keeps false alerts acceptable, and fine-tuning or augmentation on B images, then re-test on unseen B data.
7. Before the third scanner: a pre-deployment checklist. Silent-mode run on that scanner's images with radiologist reads; at least about 250 abnormal cases for a plus-or-minus 5 point sensitivity interval (about 2,460 images at 10% abnormal); a scanner-level monitor after go-live. Hospital governance decides the go/no-go.

**Metrics:**
- Sensitivity per scanner = abnormal scans flagged / abnormal scans, by scanner.
- Specificity or false-alert rate per scanner (the threshold trade-off needs both).
- Miss count per 1,000 scans per scanner.
- Subgroup sensitivity by finding type and by size.
- Guardrails: alert rate per scanner, radiologist override rate, time to read.

**Risks:**
- A scanner-specific threshold boosts sensitivity but raises false alerts and workload.
- Scanner B may stand in for a site or population effect, not the hardware.
- Over-fitting to B's 200 positives.
- Silent drift when a scanner is upgraded or its protocol changes.
- Reporting only the pooled 84.6%.

**What the interviewer scores:**
- Strong: 846, 154, 96 and 58 right, and the "38% of misses from 20% of images" point. Weak: only the overall number.
- Strong: separates case mix, labels, threshold and image properties. Weak: "retrain with more data".
- Strong: asks for specificity too. Weak: raises sensitivity without cost.
- Strong: a concrete pre-deployment plan for scanner three with a sample size. Weak: "monitor after".

**Example:** 800 abnormal on A, 88% caught: 704 found, 96 missed. 200 abnormal on B, 71% caught: 142 found, 58 missed. Pooled 846 / 1,000 = 84.6%. If B matched A, 34 more of its abnormal scans would be caught.
- Weak: "Overall sensitivity is 85%, so it is fine."
- Strong: "Overall is 84.6%, but B misses 29% of abnormal scans, 58 of 154 misses from a fifth of the images. I would look at the threshold per scanner, case mix and labels, and require a silent-mode validation on any new scanner before it goes live."

**Code:**
```python
# Q25 chest X-ray scanner gap (illustrative numbers)
from math import sqrt
nA, nB, prev = 8_000, 2_000, 0.10
posA, posB = nA * prev, nB * prev
assert posA == 800 and posB == 200 and nA + nB == 10_000
sA, sB = 0.88, 0.71
tpA, tpB = posA * sA, posB * sB
missA, missB = posA - tpA, posB - tpB
assert round(tpA) == 704 and round(tpB) == 142 and round(missA) == 96 and round(missB) == 58
overall = (tpA + tpB) / (posA + posB)
assert abs(overall - 0.846) < 1e-9
print(f"overall sensitivity {overall:.1%}; missed A={missA:.0f} B={missB:.0f}; B share of misses {missB/(missA+missB):.0%} with 20% of images")

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return c - h, c + h
loA, hiA = wilson(tpA, posA); loB, hiB = wilson(tpB, posB)
assert hiB < loA   # intervals do not overlap
print(f"A {loA:.1%}-{hiA:.1%}, B {loB:.1%}-{hiB:.1%}")
se = sqrt(sA*(1-sA)/posA + sB*(1-sB)/posB)
z = (sA - sB) / se
assert 4.9 < z < 5.1
print(f"gap 17 points, z={z:.1f}")

# If B had A's sensitivity it would miss this many fewer
extra = posB * (sA - sB)
assert round(extra) == 34
print(f"abnormal scans on B that A-level sensitivity would have caught: {extra:.0f}")

# Abnormal cases needed to estimate sensitivity of the new scanner within +-5 points (95%), assume 0.8
need_pos = 1.96**2 * 0.8 * 0.2 / 0.05**2
images = need_pos / prev
assert 245 < need_pos < 247 and 2_450 < images < 2_470
print(f"abnormal cases needed {need_pos:.0f} -> about {images:,.0f} images at 10% abnormal")
```

**Output (my run):**
```text
overall sensitivity 84.6%; missed A=96 B=58; B share of misses 38% with 20% of images
A 85.6%-90.1%, B 64.4%-76.8%
gap 17 points, z=5.0
abnormal scans on B that A-level sensitivity would have caught: 34
abnormal cases needed 246 -> about 2,459 images at 10% abnormal
```

**Follow-ups:**
- Can you just set a lower threshold for B? Possibly, but check false alerts for B first; it moves along the ROC curve and does not fix a weaker model.
- How do you monitor after go-live? Alert rate and positive rate by scanner against the validation baseline, plus a sampled radiologist audit.
- What if B and A have different patient populations? Then adjust or stratify; scanner and population effects are confounded unless you compare the same case type.

**Common mistakes:** Reporting pooled sensitivity only. Reporting accuracy at a 10% prevalence. Concluding scanner B is the cause with no case-mix check. Tuning a threshold on the test set. Forgetting false alerts.

### Q26 ⭐⭐ 🟡 Ads: A new campaign has 500 impressions and 2 clicks, a raw click rate of 0.4%. The platform has no history for the advertiser and the category's average click rate is 1.5%, which you treat as a prior worth 200 impressions. Compute the prior-shrunk estimate, explain why the raw number should not drive the bid, and describe an exploration plan with a stopping rule and a cap on spend.
**Asked at:** Ads ML and calibration material (Dataford questions on CTR calibration and click-through rate at an ad-tech firm, AlgoMaster and Educative ad click prediction system-design pages with calibration-error checks by probability bin); prep-site material; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The shrunk click rate is (2 + 3) / (500 + 200) = 0.71%, not the raw 0.40%, because 2 clicks is almost no evidence, and I would bid on the shrunk estimate while exploring with a capped budget and a written stopping rule.

**Clarifying questions:**
- What is the campaign optimising for: clicks, or a conversion behind the click? If conversion, the click rate is only the first factor in value per impression.
- How was 1.5% chosen: average of the whole category, or of similar advertisers, formats and placements? A prior from the wrong group misleads, and "worth 200 impressions" is a choice, not a fact.
- Is the creative new or one the platform has seen elsewhere? A known creative needs less exploration.
- What is the budget and the cost per thousand impressions? They set how many impressions I can afford to learn from.
- Who bears the spend risk, the advertiser or the platform? It decides how strict the cap must be.

**Approach:**
1. Shrink: prior of 1.5% x 200 = 3 pseudo-clicks in 200 pseudo-impressions, i.e. a Beta(3, 197). Posterior mean is (2 + 3) / (500 + 200) = 5 / 700 = 0.714%.
2. Show the uncertainty: the posterior 90% interval is about 0.28% to 1.30%. Even with the prior, we do not know the rate within a factor of four.
3. Say why the raw 0.4% should not drive the bid: with 2 clicks, one more or one fewer click moves it by 50%. Bid on the expected value, which uses the posterior, and do not let a lucky or unlucky start lock the campaign in or out.
4. Calibration point: bid is roughly predicted click rate x value per click. If the predicted rate is too low the campaign starves; too high and we overspend. A check by probability bin is the later test.
5. Exploration plan: give the new campaign a small guaranteed exposure (for example 3,000 impressions), use Thompson-style sampling from the posterior to allocate beyond that, and update in batches of 500.
6. Stopping rule written before launch: stop exploring and either scale or drop when the posterior probability that the click rate is below 1.0% exceeds 90% (drop) or falls under 5% (scale), or when the cap is reached.
7. Cap: a hard spend limit (illustratively 60 at 20 per thousand impressions, i.e. 3,000 impressions). Review at the cap, do not auto-extend.
8. Handle the prior's weight as a parameter: show the shrunk rate for weights of 100, 200 and 400 impressions and see whether the decision changes.

**Metrics:**
- Shrunk CTR = (clicks + prior_ctr x prior_n) / (impressions + prior_n).
- Posterior probability that CTR is below a business threshold.
- Spend to date versus cap, and cost per click realised.
- Calibration: predicted versus observed click rate by probability bin once there is volume.
- Guardrails: invalid-click credits and frequency per user.

**Risks:**
- A prior that is too strong hides a great new advertiser; too weak lets noise move bids.
- Exploration overspend: always cap by money, not by time.
- Click fraud or accidental clicks inflating the early rate.
- Position and placement effects: new campaigns often get worse slots, which lowers the rate.
- A single category average hides sub-segments.

**What the interviewer scores:**
- Strong: 0.714% shown as (2+3)/(500+200) and an interval. Weak: "0.4%, so bid low" or "just use 1.5%".
- Strong: explains why 2 clicks is noise, with numbers. Weak: says "sample is small" and nothing else.
- Strong: exploration with a stop rule and a money cap. Weak: "run it for a week".
- Strong: asks how the prior was built. Weak: treats 1.5% as truth.

**Example:** 2 clicks in 500 impressions. The posterior mean is 0.714% and the 90% interval is about 0.28% to 1.30%; the chance the true rate is under the 1.5% category average is about 98% (illustrative prior). With a cap of 60 at 20 per thousand impressions, 3,000 impressions are affordable.
- Weak: "It is only 0.4%, so we should not bid on it."
- Strong: "Raw is 0.4% on two clicks. Blending with the category prior gives 0.71% with a wide range, so I bid on 0.71%, give it a small capped exploration budget, and decide at the stop rule: below 1% with 90% confidence we drop it, otherwise we scale."

**Code:**
```python
# Q26 new campaign CTR with a prior worth 200 impressions (illustrative numbers)
import numpy as np
from scipy import stats
imps, clicks = 500, 2
raw = clicks / imps
prior_ctr, prior_n = 0.015, 200
a0, b0 = prior_ctr * prior_n, (1 - prior_ctr) * prior_n      # Beta(3, 197)
assert abs(a0 - 3) < 1e-9 and abs(b0 - 197) < 1e-9
post_mean = (clicks + a0) / (imps + prior_n)
assert abs(raw - 0.004) < 1e-12 and abs(post_mean - 5 / 700) < 1e-12
print(f"raw {raw:.3%}, shrunk {post_mean:.3%}  (= (2+3)/(500+200) = 5/700)")

# Uncertainty: 90% credible intervals
a1, b1 = a0 + clicks, b0 + imps - clicks
lo, hi = stats.beta.ppf([0.05, 0.95], a1, b1)
print(f"posterior 90% interval {lo:.2%} to {hi:.2%}")
assert 0.0027 < lo < 0.0030 and 0.0129 < hi < 0.0132
# raw-only (flat prior) interval is wider
rlo, rhi = stats.beta.ppf([0.05, 0.95], clicks + .5, imps - clicks + .5)
assert rlo < lo and rhi < hi   # raw-only data sit lower and are not narrower
print(f"raw-only (Jeffreys) 90% interval {rlo:.2%} to {rhi:.2%}")
p_below = stats.beta.cdf(0.015, a1, b1)
print(f"P(true CTR < category average 1.5%) = {p_below:.3f}")
assert 0.97 < p_below < 0.99

# Exploration plan: spend cap and stopping rule (invented cost: 20 per 1,000 impressions)
cpm, cap = 20.0, 60.0
max_imps = int(cap / cpm * 1000)
assert max_imps == 3_000
print(f"cap {cap:.0f} buys {max_imps} impressions at CPM {cpm:.0f}")
# Expected course if the true CTR is 0.7% (seeded simulation, batches of 500)
rng = np.random.default_rng(7)
true = 0.007
a, b = a1, b1
n_new = 0
while n_new < max_imps:
    k = rng.binomial(500, true); a += k; b += 500 - k; n_new += 500
    p_low = stats.beta.cdf(0.010, a, b)      # stop (drop) if probably below 1.0%
    if p_low > 0.90 or p_low < 0.05:
        break
print(f"stopped after {n_new} new impressions, posterior mean {a/(a+b):.3%}, P(CTR<1.0%)={p_low:.2f}, spent {n_new*cpm/1000:.0f}")
assert n_new <= max_imps and n_new * cpm / 1000 <= cap
```

**Output (my run):**
```text
raw 0.400%, shrunk 0.714%  (= (2+3)/(500+200) = 5/700)
posterior 90% interval 0.28% to 1.30%
raw-only (Jeffreys) 90% interval 0.11% to 1.10%
P(true CTR < category average 1.5%) = 0.979
cap 60 buys 3000 impressions at CPM 20
stopped after 2500 new impressions, posterior mean 0.750%, P(CTR<1.0%)=0.94, spent 50
```

**Follow-ups:**
- What if the advertiser already ran elsewhere? Use their history as part of the prior, with a discount for the new channel.
- How do you choose the prior weight? From how much real campaigns in the category vary (the prior spread), not by feel; fit on past campaigns' counts.
- What about conversions arriving late? Click rate learns quickly; for conversions, model delay or the early read will look worse than it is.

**Common mistakes:** Using the raw rate. Using the category average as truth. No spend cap. Stopping on a fixed time rather than evidence. Forgetting that the prior's weight is an assumption.

### Q27 ⭐⭐ 🟡 Fintech: In one day of 1,000,000 transactions a model sends 2,000 to a block band, 18,000 to a step-up band (an extra confirmation) and lets 980,000 pass, with measured fraud counts of 1,200 in the block band, 600 in the step-up band and 200 in the pass band. Assume blocking stops every fraud in its band, the step-up stops 80% of fraud in its band and 10% of genuine customers in the step-up band abandon. Compute the fraud stopped, the fraud that still gets through, the genuine customers blocked and the genuine customers lost at step-up, and discuss how you would set the band edges.
**Asked at:** Payments-fraud material (2025 SciTePress, Atlantis Press and SDMIMD papers and student projects on UPI fraud detection frame false alerts, class imbalance and retraining on confirmed fraud and false-positive reports); academic and self-published material, no interview bank for this exact framing; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Of 2,000 frauds the bands stop 1,200 + 480 = 1,680 (84%), 320 get through (120 past step-up, 200 in the pass band), 800 genuine customers are blocked and 1,740 genuine customers are lost at step-up; I would set the edges by cost per band, not by a round score.

**Clarifying questions:**
- How were the fraud counts in each band measured? Blocked transactions never produce a chargeback, so the 1,200 in the block band must come from review or customer reports; if it is a model-based guess, the whole table moves.
- Does "10% abandon" apply to the 17,400 genuine customers (600 are fraud) or to all 18,000? I use 17,400, giving 1,740; using 18,000 would give 1,800.
- What does a missed fraud cost on average, and what does a blocked or lost genuine customer cost (support, churn, lost margin)? The edges depend on this ratio.
- Is step-up capacity limited (OTP delivery, call centre)? Capacity can cap the band size.
- Do fraudsters adapt to the step-up (for example pass it with stolen devices)? The 80% is an assumption to monitor.

**Approach:**
1. Total fraud: 1,200 + 600 + 200 = 2,000 in 1,000,000 transactions (0.2%).
2. Stopped: block stops all 1,200; step-up stops 80% of 600 = 480. Total 1,680, 84% of fraud.
3. Fraud through: 600 - 480 = 120 past step-up, plus 200 in the pass band = 320.
4. Genuine customers hit: block band 2,000 - 1,200 = 800 blocked. Step-up band 18,000 - 600 = 17,400 genuine, of whom 10% abandon = 1,740 lost.
5. Band quality: block band is 60% fraud; step-up band is 3.33%; pass band is 0.02%. Step-up costs 1,740 lost customers to stop 480 frauds, about 3.6 per fraud stopped.
6. Set edges from costs: block when the fraud probability times the loss exceeds the cost of a wrong block; step-up when 80% of the loss avoided exceeds the friction plus abandonment cost. With invented costs (2,500 per fraud, 150 per false block, about 55 per step-up genuine customer) the break-evens are about 5.7% for block and 2.7% for step-up. Both are illustrative.
7. Because the block band is at 60%, the block edge could move down toward the step-up band, as long as the calibration holds; check by sliding the edge and reading the bands' observed fraud rates on held-out days.
8. Validate: calibrated probabilities (reliability by bin), stable by merchant type and hour, a small random holdout (a share of transactions passed with silent scoring) so labels are not only from what the policy allowed.
9. Ask the fraud policy and compliance owners what limits there are on blocking and customer communication; I do not state them.

**Metrics:**
- Fraud stopped rate = fraud stopped / all fraud (84%).
- Fraud loss through = amount of fraud passing (count 320, weight by amount).
- False-positive customers = genuine blocked (800) and genuine lost at step-up (1,740) per day.
- Step-up pass rate and abandonment rate by cohort.
- Guardrails: approval rate, complaint rate, call-centre load.

**Risks:**
- Labels in the block band are censored: confirmed fraud is only known if someone checks.
- The 80% stop rate and 10% abandonment are assumptions that change with the step-up method.
- Fraud shifting from the block band to the step-up or pass band once fraudsters learn.
- Counting by transaction when loss is by amount: a few big frauds in the pass band matter more.
- Edges tuned on one day (counts of 200 and 600 are small).

**What the interviewer scores:**
- Strong: 1,680, 320, 800 and 1,740, shown with the 17,400. Weak: confuses 1,800 and 1,740 or leaves out the 120.
- Strong: sets edges with a cost ratio and break-even probability. Weak: "pick a threshold at the elbow".
- Strong: flags that blocked-band labels are censored. Weak: trusts "measured" counts without question.
- Strong: includes a holdout to keep learning. Weak: retrains only on outcomes the policy allowed.

**Example:** 2,000 fraud, 1,680 stopped, 320 through. Block band: 800 genuine blocked (60% precision). Step-up band: 17,400 genuine, 1,740 lost, 480 fraud stopped. With the invented costs the break-even fraud probability is about 5.7% for block and 2.7% for step-up.
- Weak: "We stop 84% of fraud, so the model is good."
- Strong: "84% stopped, 320 through, but 2,540 genuine customers were hurt, 800 blocked and 1,740 lost at step-up. I would pick the edges from the cost of a missed fraud versus a lost customer, check calibration by band and keep a small silent holdout so my labels are not biased."

**Code:**
```python
# Q27 fraud bands (illustrative numbers, one day)
total = 1_000_000
band = {"block": (2_000, 1_200), "step": (18_000, 600), "pass": (980_000, 200)}
assert sum(n for n, _ in band.values()) == total
fraud = sum(f for _, f in band.values())
assert fraud == 2_000
stop_block = band["block"][1]
stop_step = 0.8 * band["step"][1]
stopped = stop_block + stop_step
assert stop_step == 480 and stopped == 1_680
through = fraud - stopped
assert through == 320
# of which: 120 pass step-up, 200 in pass band
assert band["step"][1] - stop_step == 120
gen = {k: n - f for k, (n, f) in band.items()}
assert gen == {"block": 800, "step": 17_400, "pass": 979_800}
lost_step = 0.10 * gen["step"]
assert lost_step == 1_740
print(f"fraud total {fraud}, stopped {stopped:.0f} ({stopped/fraud:.0%}), through {through:.0f}")
print(f"genuine blocked {gen['block']}, genuine lost at step-up {lost_step:.0f}")
for k, (n, f) in band.items():
    print(f"{k:5} flagged {n:>7} fraud {f:>5} fraud rate {f/n:.2%}")
assert round(1_200/2_000, 2) == 0.60 and round(600/18_000, 4) == 0.0333

# Choosing the edges: expected cost per 1,000 in a band, invented costs
loss_per_fraud = 2_500      # average loss if fraud gets through
block_fp = 150              # cost of a wrongly blocked genuine customer (care, lost sale, churn)
step_fp = 0.10 * 400        # 10% abandon x 400 lost margin (invented), per genuine customer stepped up
step_cost = 15              # friction cost per step-up customer
def block_gain(p):          # benefit minus cost of blocking one txn with fraud probability p
    return p * loss_per_fraud - (1 - p) * block_fp
def step_gain(p):
    return p * 0.8 * loss_per_fraud - (1 - p) * step_fp - step_cost
print(f"block band (p=60%): gain per txn {block_gain(0.6):,.0f}")
print(f"step band (p=3.33%): gain per txn {step_gain(600/18_000):,.1f}")
# break-even fraud probabilities
p_block = block_fp / (loss_per_fraud + block_fp)
p_step = (step_fp + step_cost) / (0.8 * loss_per_fraud + step_fp)
print(f"break-even p: block above {p_block:.1%}, step-up above {p_step:.2%}")
assert abs(p_block - 0.0566) < 1e-3 and abs(p_step - 0.0269) < 1e-3
assert block_gain(0.6) > 0 and step_gain(600/18_000) > 0
```

**Output (my run):**
```text
fraud total 2000, stopped 1680 (84%), through 320
genuine blocked 800, genuine lost at step-up 1740
block flagged    2000 fraud  1200 fraud rate 60.00%
step  flagged   18000 fraud   600 fraud rate 3.33%
pass  flagged  980000 fraud   200 fraud rate 0.02%
block band (p=60%): gain per txn 1,440
step band (p=3.33%): gain per txn 13.0
break-even p: block above 5.7%, step-up above 2.70%
```

**Follow-ups:**
- Why not step up everything? 980,000 genuine customers would face friction to catch 200 frauds; the cost dominates.
- What if step-up capacity is 10,000 a day? Shrink the band to the top 10,000 by score and recompute the table; lower fraud stopped.
- How would you set the pass edge? Where the marginal fraud probability equals the break-even for step-up, checked per segment.

**Common mistakes:** Counting 18,000 as genuine. Omitting the 200 frauds in the pass band. Judging a band by recall only. Forgetting censored labels. Reporting counts without amounts.

### Q28 ⭐⭐ 🟡 E-commerce: 400,000 of 2,000,000 listings (20%) lack a colour attribute. A model can fill it, with a measured accuracy of 97% on a 1,000-item audit for the 280,000 listings where its confidence is at least 0.9 and 78% on a 1,000-item audit for the other 120,000. Compute the expected wrong colours when filling only the confident ones and when filling all, treating the audit accuracies as projections, and say how you would decide, given that wrong colours drive returns.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to catalogue attribute quality and extraction in e-commerce material; related topics appear in public guides; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Filling only the 280,000 confident listings gives about 8,400 wrong colours (3% of 280,000), filling all 400,000 gives about 34,800 (8,400 plus 26,400 from the other 120,000 at 22% wrong), so I would fill the confident ones, send the rest to review or leave them blank, and decide the cut-off from the cost of a wrong colour.

**Clarifying questions:**
- What does a wrong colour cost (return rate, refund, trust), and what does a correct one earn (search visibility, filter use)? The break-even accuracy depends on this ratio.
- Is a missing colour harmful today, or just invisible to colour filters? A blank is not a wrong answer.
- How was the 1,000-item audit sampled (random within each group, or from popular items)? A biased audit moves the projection.
- Is the 97% the same across categories (multi-colour items, patterns, white vs cream)? A single number can hide a bad category.
- Can fills be shown as "suggested" or labelled by source, and can sellers correct them?

**Approach:**
1. Wrong when filling the confident group: 280,000 x (1 - 0.97) = 8,400.
2. Wrong when filling everything: 8,400 + 120,000 x (1 - 0.78) = 8,400 + 26,400 = 34,800.
3. Say these are projections from two 1,000-item audits. The 95% half-widths are about 1.1 points for the 97% group (so about 5,400 to 11,400 wrong) and about 2.6 points for the 78% group (about 23,300 to 29,500 wrong). I would carry the ranges, not point values.
4. The marginal decision: the extra 120,000 fills add 26,400 wrong and 93,600 right. If a wrong colour costs five times what a right colour earns (invented), the break-even accuracy is 5 / (1 + 5) = 83.3%, so the 97% group passes and the 78% group fails.
5. Options for the 120,000: leave blank, route to human or seller confirmation, show as "suggested" with a lower confidence flag, or use a second model or the product image plus title agreement as an extra gate.
6. Pick the confidence cut-off by a sweep: accuracy and volume by confidence bin, from a fresh audit, not from the model's own scores alone.
7. Monitor after launch: sampled audits per category, return rate by filled-versus-seller-entered colour, and seller corrections.
8. Phase it: fill the confident listings first, then measure returns with a holdout of listings that stay blank.

**Metrics:**
- Fill rate = listings with a colour / all listings (rises from 80% to 94% by filling the confident group).
- Precision of fills = correct fills / fills, by confidence bin and category.
- Wrong fills per 1,000 listings and their return-rate impact.
- Net value = right fills x B - wrong fills x C.
- Guardrails: colour-related return rate, seller disputes, search click-through on colour filters.

**Risks:**
- Confidence scores not calibrated, so 0.9 means different accuracy in different categories.
- Audit accuracy on a 1,000 sample is noisy and may not match the live mix.
- Wrong colours cluster in categories where colour matters most (fashion).
- Feedback loop: filled colours become training labels.
- Value assumptions (B and C) are guesses.

**What the interviewer scores:**
- Strong: 8,400 and 34,800 with the 26,400 explained. Weak: "97% and 78%, average them".
- Strong: calls the figures projections and gives the audit's uncertainty. Weak: treats 3% as exact.
- Strong: decides by cost of wrong versus value of right, with a break-even accuracy. Weak: "fill everything for coverage".
- Strong: offers human review or labelled suggestions for the uncertain group. Weak: only fill or not fill.

**Example:** 400,000 missing. Confident 280,000 at 97%: 271,600 right, 8,400 wrong. The rest 120,000 at 78%: 93,600 right, 26,400 wrong. If a wrong fill costs 5 and a right fill earns 1 (invented), the confident group nets +0.82 per fill and the rest nets -0.32 per fill.
- Weak: "Overall accuracy would be about 91%, good enough, fill them all."
- Strong: "Filling all gives about 34,800 wrong colours against 8,400 for the confident group. The extra 120,000 are 22% wrong, and wrong colours cause returns, so I would hold them for review, and decide the cut-off with a fresh audit and a cost ratio."

**Code:**
```python
# Q28 colour attribute filling (illustrative numbers; audit accuracies treated as projections)
from math import sqrt
total, missing = 2_000_000, 400_000
assert missing / total == 0.20
conf_n, low_n = 280_000, 120_000
assert conf_n + low_n == missing
acc_c, acc_l = 0.97, 0.78
wrong_c = conf_n * (1 - acc_c)
wrong_l = low_n * (1 - acc_l)
assert round(wrong_c) == 8_400 and round(wrong_l) == 26_400 and round(wrong_c + wrong_l) == 34_800
print(f"fill confident only: {wrong_c:,.0f} wrong of {conf_n:,}; fill all: {wrong_c+wrong_l:,.0f} wrong of {missing:,}")
print(f"the extra {low_n:,} fills add {wrong_l:,.0f} wrong ({1-acc_l:.0%} wrong) and {low_n-wrong_l:,.0f} right")

# Audit uncertainty: 1,000 items per audit, 95% normal-approx half-width
def hw(p, n=1000): return 1.96 * sqrt(p * (1 - p) / n)
hc, hl = hw(acc_c), hw(acc_l)
print(f"audit half-widths: confident +-{hc:.1%} -> wrong range {conf_n*(1-acc_c-hc):,.0f} to {conf_n*(1-acc_c+hc):,.0f}; "
      f"rest +-{hl:.1%} -> {low_n*(1-acc_l-hl):,.0f} to {low_n*(1-acc_l+hl):,.0f}")
assert 0.010 < hc < 0.012 and 0.025 < hl < 0.027

# Decision: fill only where accuracy exceeds C/(B+C). Invented values: benefit of a right fill B=1, cost of a wrong fill C=5
B, C = 1.0, 5.0
be = C / (B + C)
assert abs(be - 5/6) < 1e-12
for name, a in (("confident", acc_c), ("rest", acc_l)):
    gain = a * B - (1 - a) * C
    print(f"{name}: accuracy {a:.0%}, net value per fill {gain:+.2f} (break-even accuracy {be:.1%})")
assert 0.97 * B - 0.03 * C > 0 and 0.78 * B - 0.22 * C < 0
# Human review of the rest: what accuracy after review if a reviewer fixes 80% of its errors (invented)?
fixed = low_n * (1 - acc_l) * 0.8
print(f"review of the rest at 80% error catch: wrong falls from {wrong_l:,.0f} to {wrong_l-fixed:,.0f}")
assert round(wrong_l - fixed) == 5_280
```

**Output (my run):**
```text
fill confident only: 8,400 wrong of 280,000; fill all: 34,800 wrong of 400,000
the extra 120,000 fills add 26,400 wrong (22% wrong) and 93,600 right
audit half-widths: confident +-1.1% -> wrong range 5,440 to 11,360; rest +-2.6% -> 23,319 to 29,481
confident: accuracy 97%, net value per fill +0.82 (break-even accuracy 83.3%)
rest: accuracy 78%, net value per fill -0.32 (break-even accuracy 83.3%)
review of the rest at 80% error catch: wrong falls from 26,400 to 5,280
```

**Follow-ups:**
- How big should the audit be? For half-width of 1 point at 97% you need about 1,100 per group; at 78% about 6,600. Compute from p(1-p) and the target width.
- What if the model is confident but wrong in one category? Report accuracy per category and set category-specific thresholds or exclusions.
- Can you use seller feedback? Yes, as a signal and for labels, but beware selection: only some sellers correct.

**Common mistakes:** Mixing the two audits into one blended accuracy. Calling projections facts. Ignoring that a blank is cheaper than a wrong value. Using the model's confidence without an audit. Ignoring category differences.

### Q29 ⭐⭐ 🟡 Healthcare: A sepsis model was built at hospital 1 with an AUC of 0.88 and external tests give an AUC of 0.79 at hospital 2 and 0.84 at hospital 3, with a calibration slope of 0.6 at hospital 2 (1.0 is ideal). The sepsis rate is 4% at hospital 3 and 2.5% at hospital 2, and your team wants at least 100 events at each site before trusting its numbers. Compute the minimum patients needed per site and describe a rollout plan with local recalibration, monitoring and stop rules.
**Asked at:** Clinical-AI external-validation coverage (Fierce Healthcare, MedCity News and JAMA Internal Medicine pages on the external validation of a widely deployed sepsis model, which reported low sensitivity, a modest positive predictive value, alerts on a large share of patients and a billing-code outcome definition; a newsletter piece on local validation and tracking override patterns); published news and research, not an interview bank; commonly reported in public guides for data scientist and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** At 100 expected events you need 100 / 0.04 = 2,500 patients at hospital 3 and 100 / 0.025 = 4,000 at hospital 2, but that is only about even odds of actually reaching 100, so I would plan for roughly 2,900 and 4,700, then roll out in silent mode with local recalibration, monitoring and written stop rules.

**Clarifying questions:**
- How is "sepsis" defined at each site (clinical criteria, billing code, treatment trigger)? Different definitions can explain part of the AUC drop and the 4% versus 2.5% rate.
- Which patients are in scope (all admissions, emergency department, wards)? The denominator changes the rate and the alert burden.
- Who acts on an alert and how many alerts per shift can they handle? It sets the threshold.
- Are the 100 events counted per patient or per episode? Repeat episodes inflate events.
- Who signs off a clinical deployment (clinical safety, a governance committee)? I propose, they decide; I ask them what review is required.

**Approach:**
1. Minimum patients for an expected 100 events: hospital 3 is 100 / 0.04 = 2,500; hospital 2 is 100 / 0.025 = 4,000.
2. Be honest that expected is not guaranteed: with 2,500 patients at 4% the chance of at least 100 events is about 51%. For a 95% chance, plan for about 2,916 (hospital 3) and 4,671 (hospital 2).
3. Say what 100 events buys: sensitivity of 0.70 is known only within about plus-or-minus 9 points, and an AUC of 0.79 within about plus-or-minus 5 points. Treat it as a floor for checking calibration, not as a precise estimate.
4. Read the shifts: AUC 0.88 to 0.79 means worse ranking at hospital 2; slope 0.6 means predicted risks are too extreme (high predictions are overstated), so the same score does not mean the same risk. Hospital 3 at 0.84 is a smaller drop.
5. Recalibrate locally first: fit an intercept and slope on the first local data (a logistic recalibration), check calibration by bin, and set the threshold from the local alert capacity.
6. Silent mode first: score patients, show nothing, collect outcomes. Then limited go-live on selected wards with clinician review of alerts.
7. Monitor: weekly alerts per 1,000 patients, PPV against the local label, sensitivity on a sampled chart review, calibration slope by month, and override and ignore rates.
8. Stop rules (agreed in advance with clinical owners): pause if the alert rate or PPV leaves an agreed band for a set period, if calibration slope falls outside an agreed range, if the data feed breaks, or if a safety event is linked to an alert. Resume only after review.

**Metrics:**
- Events per site = patients with the outcome / patients in scope; the denominator in the sample-size maths.
- AUC and calibration slope and intercept per site, each with an interval.
- PPV and alerts per 1,000 patients at the chosen threshold.
- Sensitivity from audited events (including those the model missed).
- Guardrails: time to antibiotics (as a process measure), override rate, alert fatigue signals.

**Risks:**
- A billing-code outcome can lag and miss early cases; the label may reward coding, not clinical sepsis.
- Treatment contamination: clinicians acting on alerts change the outcomes the model learns from later.
- With 100 events the intervals are wide; do not over-read differences between sites.
- Recalibration fixes risk levels but not a weaker ranking.
- Alert burden: at a plausible operating point, 161 alerts per 1,000 patients with PPV about 9% is a lot.

**What the interviewer scores:**
- Strong: 2,500 and 4,000 right, and notes expected versus guaranteed events. Weak: stops at the division or adds the two numbers.
- Strong: reads calibration slope 0.6 correctly (too extreme). Weak: reads only AUC.
- Strong: concrete stop rules and silent mode before go-live. Weak: "monitor drift".
- Strong: says clinical owners decide. Weak: states what a regulator requires.

**Example:** Hospital 3 expects 100 events in 2,500 patients, about 2,900 for a 95% chance. Hospital 2 needs 4,000, about 4,700. At hospital 2 with an invented operating point (sensitivity 0.60, specificity 0.85) PPV is 9.3% and 161 of every 1,000 patients alert. A predicted 20% risk would be about 9.1% after slope recalibration.
- Weak: "AUC 0.79 is fine, deploy and watch."
- Strong: "I need about 4,000 patients at hospital 2 and 2,500 at hospital 3 for 100 expected events, and more for safety. I run silent mode, recalibrate locally since the slope is 0.6, set the threshold on alert capacity, and agree stop rules with the clinical owners first."

**Code:**
```python
# Q29 sepsis external validation sample size and alert burden (illustrative numbers)
from math import sqrt
from scipy import stats
events_needed = 100
rate = {"hospital 2": 0.025, "hospital 3": 0.04}
for h, p in rate.items():
    n_exp = events_needed / p
    n = int(n_exp)
    while stats.binom.sf(events_needed - 1, n, p) < 0.95:
        n += 1
    print(f"{h}: rate {p:.1%}, patients for 100 expected events {n_exp:,.0f}; for a 95% chance of at least 100 events {n:,}")
assert 100 / 0.025 == 4_000 and 100 / 0.04 == 2_500
assert stats.binom.sf(99, 2_500, 0.04) < 0.55     # only about even odds at the expected count
print(f"P(>=100 events) with 2,500 patients at 4% = {stats.binom.sf(99, 2500, 0.04):.2f}")

# What do 100 events buy? 95% half-width of a sensitivity of 0.70 and of an AUC of 0.79 (Hanley-McNeil)
hw_sens = 1.96 * sqrt(0.7 * 0.3 / 100)
def auc_se(auc, npos, nneg):
    q1, q2 = auc / (2 - auc), 2 * auc**2 / (1 + auc)
    return sqrt((auc*(1-auc) + (npos-1)*(q1-auc**2) + (nneg-1)*(q2-auc**2)) / (npos*nneg))
se = auc_se(0.79, 100, 3_900)
print(f"sensitivity 0.70 on 100 events: +-{hw_sens:.3f}; AUC 0.79 with 100 events: +-{1.96*se:.3f}")
assert 0.08 < hw_sens < 0.10 and 0.04 < 1.96 * se < 0.07

# Alert burden at hospital 2 for an invented operating point (sens 0.60, spec 0.85)
sens, spec, p = 0.60, 0.85, 0.025
tp, fp = sens * p, (1 - spec) * (1 - p)
ppv = tp / (tp + fp)
alerts_per_1000 = 1000 * (tp + fp)
assert abs(ppv - 0.0930) < 1e-3 and round(alerts_per_1000) == 161
print(f"hospital 2 at sens 0.60 / spec 0.85: PPV {ppv:.1%}, alerts per 1,000 patients {alerts_per_1000:.0f}, true cases found {1000*tp:.0f} of {1000*p:.0f}")
# Calibration slope 0.6: predictions are too extreme; pull them toward the mean on the logit scale
import numpy as np
logit = lambda x: np.log(x / (1 - x)); expit = lambda z: 1 / (1 + np.exp(-z))
pred, mean_risk = 0.20, 0.025          # assume the average predicted risk equals the 2.5% event rate
adj = expit(logit(mean_risk) + 0.6 * (logit(pred) - logit(mean_risk)))
print(f"slope 0.6 pivoting at the mean: a predicted 20% risk is recalibrated to about {adj:.1%}")
assert 0.085 < adj < 0.095
```

**Output (my run):**
```text
hospital 2: rate 2.5%, patients for 100 expected events 4,000; for a 95% chance of at least 100 events 4,671
hospital 3: rate 4.0%, patients for 100 expected events 2,500; for a 95% chance of at least 100 events 2,916
P(>=100 events) with 2,500 patients at 4% = 0.51
sensitivity 0.70 on 100 events: +-0.090; AUC 0.79 with 100 events: +-0.053
hospital 2 at sens 0.60 / spec 0.85: PPV 9.3%, alerts per 1,000 patients 161, true cases found 15 of 25
slope 0.6 pivoting at the mean: a predicted 20% risk is recalibrated to about 9.1%
```

**Follow-ups:**
- Why 100 events? It is a common rule of thumb in the validation literature (editor knowledge, not checked here); more are better and the interval width is the real target.
- What if the sites' definitions differ? Re-label a sample of charts with one definition and compare.
- How do you handle the calibration slope without enough data? Pool a few months of silent-mode data, and keep the intercept and slope as monitored parameters.

**Common mistakes:** Dividing 100 by the rate and stopping. Treating AUC as the only metric. Deploying without local calibration. Using a billing code as truth without checking. No pre-agreed stop rules.

