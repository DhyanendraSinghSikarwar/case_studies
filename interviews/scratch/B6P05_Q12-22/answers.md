### Q12 ⭐⭐⭐ 🟡 At peak in one zone, riders request 120 rides an hour and drivers can complete 80 at the base fare of 10, so revenue is 800 an hour. A 1.5x surge cuts requests by 20% relative to 120 (to 96) and raises driver supply by 10% relative to 80 (to 88), and the team concludes that revenue rises to 1,320 an hour (+65% relative to 800). Check the arithmetic, then say what could make the real gain smaller and what else you would track.
**Asked at:** Dynamic-pricing and surge material (a Dataford surge-pricing switchback question, Codemia and Final Round AI pages on designing surge pricing for Uber or Lyft, a Prepfully pricing-riders product case, a Glassdoor Uber entry as listed in snippets); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The arithmetic is right, 88 rides at 15 is 1,320 and +65%, but it is gross fares in a perfect world, so I would check who gets the money, whether the demand and supply moves are real, and what surge does to riders over time.

**Clarifying questions:**
- Is "revenue" gross fares or what the platform keeps? Surge money often goes mostly to drivers, so platform revenue can rise far less than 65%.
- Where do the 20% demand drop and the 10% supply rise come from, a test or a guess? A guess is a hypothesis, not a result.
- How long does the surge last and how fast do drivers react? Supply that arrives after the peak does not help.
- Is the surge applied to the whole zone or to a few blocks? It changes how many riders and drivers see it.
- Do riders who drop out leave for good or come back at the base fare? It decides whether the lost demand is a loss or a delay.

**Approach:**
1. Re-do the arithmetic with the cap. Completed rides = min(requests, supply). Base: min(120, 80) = 80 at 10 = 800. Surge: min(96, 88) = 88 at 15 = 1,320. Ratio 1.65, so +65% is correct.
2. Say what the model assumes. Demand falls only 20% for a 50% price rise (implied elasticity -0.4), and drivers add 8 rides at once.
3. Shrink it one assumption at a time. If riders drop 35%, requests are 78, below supply, so rides are 78 and revenue is 1,170 (+46%). If supply does not move, rides are 80 and revenue is 1,200 (+50%).
4. Split gross fare from platform revenue. If the platform keeps 25% of the base fare only, 200 becomes 220, a +10% gain.
5. Look past the hour. Track rider cancellations, app opens without a request, repeat rides next week, and driver hours.
6. Test it. Use a switchback or geo test with a control zone (see Book 6 Part 4, Q28, the switchback test on dispatch logic) because zone neighbours interfere with each other.

**Metrics:**
- Completed rides per hour = min(requests, supply). Fill rate = completed / requests.
- Gross fare revenue per hour = completed rides x fare. Platform revenue per hour = completed rides x platform fee.
- Request conversion = requests / app opens in the zone. Time to match and cancellation rate.
- Guardrails: rider repeat rate next 7 days, driver cancel rate, complaints about price.

**Risks:**
- Riders learn to wait for surge to end, so demand falls more over time.
- Supply moves slowly and drivers drive toward the surge, leaving a neighbouring zone short.
- Surge raises gross fares but not margin if driver pay rises with it.
- A short test measures the first reaction and misses the habit change.

**What the interviewer scores:**
- Strong: recomputes and confirms 1,320 and 65% before criticising. Weak: assumes the team is wrong or accepts it blindly.
- Strong: uses min(requests, supply) and separates gross fares from platform revenue. Weak: only says "demand might fall more".
- Strong: gives an experiment with interference handled. Weak: "run an A/B test" on riders in one zone.
- Strong: names rider-retention guardrails. Weak: stares at hourly revenue.

**Example:** (illustrative numbers) Base: 80 rides at 10 = 800. Team case: 88 rides at 15 = 1,320 (+65%). Riders drop 35% not 20%: 78 rides, 1,170 (+46%). Supply does not rise: 80 rides, 1,200 (+50%). Platform keeps 25% of the base fare only: 200 becomes 220 (+10%). Unfilled requests fall from 40 to 8, which is the real benefit to riders. Weak answer: "Surge raises price so revenue goes up 65%." Strong answer: "The 65% is right as gross fares under two friendly assumptions. With a slower supply response it is +50%, and for the platform it may be only +10%, so I would test it and watch repeat riders."

**Code:**
```python
# Illustrative numbers. Surge arithmetic with a supply cap.
base_req, base_sup, base_fare = 120, 80, 10.0
def rev(req, sup, fare):
    done = min(req, sup)          # completed rides cannot exceed requests or driver capacity
    return done, done * fare
d0, r0 = rev(base_req, base_sup, base_fare)
print("base", d0, r0)
assert (d0, r0) == (80, 800)
req1, sup1, fare1 = 120 * 0.80, 80 * 1.10, 15.0
assert round(req1) == 96 and round(sup1) == 88
d1, r1 = rev(req1, sup1, fare1)
print("team case", d1, r1, f"{r1/r0-1:+.0%}")
assert (round(d1), round(r1), round(r1/r0 - 1, 2)) == (88, 1320, 0.65)   # arithmetic is right
# What could shrink it? One change at a time, then together.
cases = {
 "team case":                    (96, 88, 15.0),
 "riders drop 35% not 20%":      (78, 88, 15.0),
 "supply +0% (slow response)":   (96, 80, 15.0),
 "riders -35% and supply +0%":   (78, 80, 15.0),
}
for k, (rq, sp, f) in cases.items():
    d, r = rev(rq, sp, f)
    print(f"{k:30} rides {d:5.0f} revenue {r:7.1f} ({r/r0-1:+.0%})")
assert round(rev(78, 88, 15)[1]) == 1170 and round(rev(96, 80, 15)[1]) == 1200 and round(rev(78, 80, 15)[1]) == 1170
# Gross fare is not platform revenue. Illustrative: platform keeps 25% of the BASE fare only, drivers get the surge uplift.
take_base = 0.25 * 10.0
p0, p1 = d0 * take_base, d1 * take_base
print("platform keeps (25% of base fare):", p0, "->", p1, f"{p1/p0-1:+.0%}")
assert (p0, p1) == (200.0, 220.0)
# Break-even: how many rides can be lost before surge revenue equals base revenue at 1.5x?
be = r0 / 15.0
print(f"surge revenue = base revenue when completed rides = {be:.2f} (a {be/80-1:+.1%} change from 80)")
assert round(be, 2) == 53.33
# Implied arc elasticity in the team case: -20% requests for +50% price
print("implied elasticity of requests", round(-0.20 / 0.50, 2))
# Unfilled requests
print("unfilled requests at 1.5x", 96 - 88, "vs base", 120 - 80)
assert (96 - 88, 120 - 80) == (8, 40)
```

**Output (my run):**
```text
base 80 800.0
team case 88.0 1320.0 +65%
team case                      rides    88 revenue  1320.0 (+65%)
riders drop 35% not 20%        rides    78 revenue  1170.0 (+46%)
supply +0% (slow response)     rides    80 revenue  1200.0 (+50%)
riders -35% and supply +0%     rides    78 revenue  1170.0 (+46%)
platform keeps (25% of base fare): 200.0 -> 220.0 +10%
surge revenue = base revenue when completed rides = 53.33 (a -33.3% change from 80)
implied elasticity of requests -0.4
unfilled requests at 1.5x 8 vs base 40
```

**Follow-ups:**
- What demand drop makes surge pay? Completed rides must stay above 800 / 15 = 53.3, a 33% fall from 80 rides. Beyond that gross fares are below base.
- What if drivers get the surge money? Then it is a supply tool and platform revenue barely moves, so judge it by fill rate and wait time.

**Common mistakes:**
- Calling the 1,320 wrong because "demand is elastic". It is arithmetically right.
- Forgetting the cap, and multiplying 96 requests by 15.
- Counting gross fares as platform revenue.
- Judging the result from the peak hour only.

### Q13 ⭐⭐⭐ 🟡 Paid-search customers cost 80 each to acquire, earn 10 a month of margin and churn at 8% of the active cohort a month. Referral customers cost 30, earn 9 and churn at 5% a month. Using margin divided by monthly churn, compute LTV and the LTV-to-CAC ratio for each, and say how you would place the next budget given that each churn rate comes from three months of data.
**Asked at:** Lifetime-value and CAC material (a Dataford 'calculate customer lifetime value' product-growth-analyst page, Hacking the Case Interview, Road to Offer and MBB Prep pages on CLV and CAC, Count.co and FourWeekMBA CAC-payback pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Referral wins on both numbers, LTV 180 against 125 and LTV-to-CAC 6.0 against 1.56, but three months of churn data is thin and referral volume is limited, so I would shift budget in steps and keep measuring.

**Clarifying questions:**
- Are the 8% and 5% churn rates measured on the same type of customer and the same 3 months? Seasonality or promos can move them.
- How many customers are behind each rate? 8% from 300 customers is very noisy, from 3,000 less so.
- Is margin 10 a month after payment fees and support? LTV scales directly with it.
- How many referral customers can we add before the pool dries up? Average CAC says nothing about the next customer.
- Is the money limited by cash payback or by long-run value? It changes whether 8-month payback is a problem.

**Approach:**
1. Compute. Search: LTV = 10 / 0.08 = 125, ratio 125 / 80 = 1.56. Referral: 9 / 0.05 = 180, ratio 180 / 30 = 6.0.
2. Add simple payback, ignoring churn: search 80 / 10 = 8 months, referral 30 / 9 = 3.3 months. Search pays back slowly while 8% of customers leave each month.
3. Put a band on churn. With illustrative exposure of 2,800 and 1,100 customer-months, the 95% band is about 7.0% to 9.0% for search and 3.7% to 6.4% for referral. The ratios are 1.4 to 1.8 and 4.7 to 8.0, so the ranking holds.
4. Ask the marginal question. Referral at 6.0 is the average. If the next referral costs 60, the ratio is 3.0, still better than search.
5. Decide: move budget to referral in steps until marginal LTV-to-CAC meets the search level or a floor such as 3. Keep a small search budget for scale and learning.
6. Re-measure with older cohorts, since 3 months says nothing about month 12.

**Metrics:**
- LTV = monthly margin / monthly churn, where churn = customers lost in the month / active at the start of that month.
- LTV-to-CAC = LTV / CAC. Simple payback = CAC / monthly margin.
- Marginal CAC = extra spend / extra customers from that spend.
- Guardrail: cohort retention at month 6 and 12 against the constant-churn forecast.

**Risks:**
- Constant churn is wrong when early churn is higher than later churn. In my sketch (12% for 6 months then 5%) the search LTV is 137.5 against 125, so the formula can miss either way.
- Referral customers may be friends of existing customers and would have joined anyway.
- Average CAC hides diminishing returns.
- No discounting, so LTV is overstated for slow cohorts.

**What the interviewer scores:**
- Strong: correct LTVs and ratios, then says the ranking is robust to noise. Weak: stops at "referral is better".
- Strong: marginal versus average CAC. Weak: puts all the budget in referral.
- Strong: payback as well as ratio. Weak: ratio only.
- Strong: asks for cohort data beyond 3 months. Weak: trusts one churn number.

**Example:** (illustrative numbers) Search: LTV 125, CAC 80, ratio 1.56, payback 8 months. Referral: LTV 180, CAC 30, ratio 6.0, payback 3.3 months. At the edges of the bands, referral at 6.4% churn gives a ratio of 4.7 and search at 7.0% gives 1.79. Weak answer: "Send everything to referral." Strong answer: "Referral first, in steps, while marginal ratio stays above about 3, and I recheck churn when a 6-month cohort exists."

**Code:**
```python
import numpy as np
# Illustrative numbers.
ch = {"search": dict(cac=80.0, margin=10.0, churn=0.08), "referral": dict(cac=30.0, margin=9.0, churn=0.05)}
for k, v in ch.items():
    v["ltv"] = v["margin"] / v["churn"]; v["ratio"] = v["ltv"] / v["cac"]
    v["payback"] = v["cac"] / v["margin"]
    print(f"{k:9} LTV {v['ltv']:6.1f}  LTV/CAC {v['ratio']:.2f}  simple payback {v['payback']:.1f} months")
assert (ch["search"]["ltv"], round(ch["search"]["ratio"], 4)) == (125.0, 1.5625)
assert (ch["referral"]["ltv"], ch["referral"]["ratio"]) == (180.0, 6.0)
# Churn from 3 months of data is noisy. Illustrative exposure: 1,000 searched-acquired and 400 referral customers,
# observed for 3 months each (about 2,800 and 1,100 active customer-months after churn).
rng = np.random.default_rng(7)
def churn_interval(p, months, n=100_000):
    # events ~ Binomial(months, p); churn estimate = events/months; parametric bootstrap
    ev = rng.binomial(months, p, size=n) / months
    return np.percentile(ev[ev > 0], [2.5, 97.5])
exp = {"search": 2800, "referral": 1100}
res = {}
for k, v in ch.items():
    lo, hi = churn_interval(v["churn"], exp[k])
    res[k] = (lo, hi, v["margin"] / hi / v["cac"], v["margin"] / lo / v["cac"])
    print(f"{k:9} churn 95% band {lo:.3%}-{hi:.3%}  LTV/CAC band {res[k][2]:.2f}-{res[k][3]:.2f}")
# Even at the worst referral and best search ends, referral ratio stays well above search ratio
assert res["referral"][2] > res["search"][3]
# Bigger risk than noise: 3 months of data say nothing about month 12. Check a churn that falls with tenure.
# Same 3-month average of 8% but hazard 12% early, 5% later: early-month churn can mislead LTV either way.
early, late = 0.12, 0.05
surv, ltv = 1.0, 0.0
for m in range(1, 241):
    ltv += surv * 10.0
    surv *= (1 - (early if m <= 6 else late))
print(f"search LTV with churn 12% for 6 months then 5%: {ltv:.1f} (vs 125.0 constant)")
assert round(ltv, 1) == 137.5
# Marginal CAC: if the next referral customer costs 60 (referral pool is finite), referral ratio:
print("referral LTV/CAC if marginal CAC rises to 60:", round(180 / 60, 2))
assert round(180 / 60, 2) == 3.0
```

**Output (my run):**
```text
search    LTV  125.0  LTV/CAC 1.56  simple payback 8.0 months
referral  LTV  180.0  LTV/CAC 6.00  simple payback 3.3 months
search    churn 95% band 7.000%-9.000%  LTV/CAC band 1.39-1.79
referral  churn 95% band 3.727%-6.364%  LTV/CAC band 4.71-8.05
search LTV with churn 12% for 6 months then 5%: 137.5 (vs 125.0 constant)
referral LTV/CAC if marginal CAC rises to 60: 3.0
```

**Follow-ups:**
- Why not put 100% in referral? Volume is limited and its cost per extra customer rises. Marginal return is what matters.
- Should LTV be discounted? Yes for a decision on cash. A 1% monthly discount rate cuts LTV noticeably when churn is low.

**Common mistakes:**
- Using ratio without payback.
- Treating 8% and 5% as exact.
- Applying average CAC to the next customer.
- Quoting an LTV for a 20-month life from 3 months of data.

### Q14 ⭐⭐⭐ 🔴 A randomized retention test offered a coupon, at a cost of 3 per contacted customer, to 10,000 customers in each of two risk groups, with 10,000 held-out controls in each group. In the high-risk group 30% of offered customers churn against 32% of control (absolute difference of 2 points), and in the mid-risk group the figures are 10% against 14% (4 points). A saved customer is worth 120. Compute the net value of offering each group, say which of a churn-propensity model and an uplift model would have picked each group, and say what you would build.
**Asked at:** Churn and uplift material (Towards Data Science and Dataiku pages on churn models versus uplift models, a re-work blog post arguing that treatment, not churn prediction, is the goal, an arXiv paper on causal segmentation); practitioner and academic pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The coupon is worth offering only where it cuts churn by more than 3 / 120 = 2.5 points, so the mid-risk group gains 1.80 per customer and the high-risk group looks like a small loss of 0.60, and a propensity model would have picked the wrong group.

**Clarifying questions:**
- Is the 3 the only cost? A coupon that is redeemed may also cost margin on the next order, which raises the break-even.
- Over what window is churn measured? A saved customer must still be worth 120 after that window.
- Were offers and controls randomized inside each risk group? Without that, the 2-point and 4-point gaps are not causal.
- How was risk assigned, by an old model? If so the groups are fixed and this is two buckets, not a full uplift curve.
- Is the 120 a margin value after the coupon? If it is revenue, every net figure shrinks.

**Approach:**
1. Break-even uplift = cost / value = 3 / 120 = 2.5 points of churn.
2. High-risk: uplift 32% - 30% = 2.0 points. Saved value 0.02 x 120 = 2.40, minus 3 = -0.60 per offered customer, -6,000 over 10,000.
3. Mid-risk: uplift 14% - 10% = 4.0 points. Saved value 4.80, minus 3 = +1.80 per customer, +18,000.
4. Check noise. The standard error of the high-risk gap is about 0.65 points, so the interval is 0.7 to 3.3 points and net -2.14 to +0.94. The loss is not established. The mid-risk interval is 3.1 to 4.9 points, net +0.72 to +2.88, clearly positive.
5. Propensity versus uplift. A propensity model ranks by churn probability, so it picks high-risk (30 to 32% churn) first. An uplift model ranks by the churn reduction caused by the offer, so it picks mid-risk. With 10,000 coupons that is -6,000 against +18,000.
6. Build an uplift model (two-model or a causal forest) on the randomized data, check it with an uplift curve on a held-out randomized sample, and keep a small random control always on.

**Metrics:**
- Uplift = churn rate of controls - churn rate of offered, in the same risk group, absolute points.
- Net per offered customer = uplift x 120 - 3. Net per group = that x customers offered.
- Guardrail: control group kept running, coupon abuse, margin on the retained customers.

**Risks:**
- Two groups are not a model. Uplift can vary a lot inside each group.
- "Sleeping dogs": for some customers the offer raises churn or reminds them to cancel.
- A 2-point gap at 10,000 per arm is only about 3 standard errors, so the sign of the net is uncertain.
- Value 120 may differ by group.

**What the interviewer scores:**
- Strong: break-even uplift and net per customer, with the high-risk loss shown as uncertain. Weak: says high-risk obviously needs saving.
- Strong: explains that propensity predicts who will churn, not who will respond. Weak: mixes the two.
- Strong: proposes uplift modelling on randomized data with an uplift curve. Weak: "train a bigger churn model".
- Strong: keeps a control. Weak: no way to monitor.

**Example:** (illustrative numbers) High-risk: control 32%, offered 30%, gain 2.0 points, net -0.60 each (95% band -2.14 to +0.94). Mid-risk: control 14%, offered 10%, gain 4.0 points, net +1.80 each (band +0.72 to +2.88). Weak answer: "Target the customers most likely to churn." Strong answer: "Target the customers most likely to be saved. Here that is mid-risk, and the high-risk spend is break-even at best."

**Code:**
```python
import math
# Illustrative numbers. Randomized test: offer vs control, 10,000 each per risk group.
n = 10_000; cost = 3.0; value = 120.0
groups = {"high-risk": (0.30, 0.32), "mid-risk": (0.10, 0.14)}   # (churn offered, churn control)
be = cost / value
print(f"break-even uplift (absolute churn reduction) = {be:.2%}")
assert round(be, 4) == 0.025
for g, (po, pc) in groups.items():
    up = pc - po
    se = math.sqrt(po * (1 - po) / n + pc * (1 - pc) / n)
    lo, hi = up - 1.96 * se, up + 1.96 * se
    net = up * value - cost
    net_lo, net_hi = lo * value - cost, hi * value - cost
    print(f"{g:10} uplift {up:.2%} (95% {lo:.2%} to {hi:.2%}, z={up/se:.1f})  net per offered {net:+.2f} "
          f"(95% {net_lo:+.2f} to {net_hi:+.2f})  total {net*n:+,.0f}")
    groups[g] = (po, pc, up, se, net, net_lo, net_hi)
assert round(groups["high-risk"][4], 2) == -0.60 and round(groups["mid-risk"][4], 2) == 1.80
assert round(groups["high-risk"][4] * n) == -6000 and round(groups["mid-risk"][4] * n) == 18000
# The high-risk loss is NOT statistically established: its interval includes break-even.
assert groups["high-risk"][5] < 0 < groups["high-risk"][6]
assert groups["mid-risk"][5] > 0           # the mid-risk gain is clearly positive
# Who would each model pick? Propensity ranks by churn probability; uplift ranks by uplift.
prop_order = sorted(groups, key=lambda g: -groups[g][1])     # control churn = natural churn risk
upl_order = sorted(groups, key=lambda g: -groups[g][2])
print("propensity picks first:", prop_order[0], "| uplift picks first:", upl_order[0])
assert prop_order[0] == "high-risk" and upl_order[0] == "mid-risk"
# Budget view: 10,000 coupons only. Propensity model spends them on high-risk, uplift on mid-risk.
print("10,000 coupons: propensity", round(groups["high-risk"][4] * n), "uplift", round(groups["mid-risk"][4] * n))
```

**Output (my run):**
```text
break-even uplift (absolute churn reduction) = 2.50%
high-risk  uplift 2.00% (95% 0.72% to 3.28%, z=3.1)  net per offered -0.60 (95% -2.14 to +0.94)  total -6,000
mid-risk   uplift 4.00% (95% 3.10% to 4.90%, z=8.7)  net per offered +1.80 (95% +0.72 to +2.88)  total +18,000
propensity picks first: high-risk | uplift picks first: mid-risk
10,000 coupons: propensity -6000 uplift 18000
```

**Follow-ups:**
- Can I conclude high-risk loses money? Not yet. Its interval includes break-even. I would test a cheaper offer or a larger sample there.
- How do I evaluate an uplift model? An uplift or Qini curve on held-out randomized data, with the same break-even line of 2.5 points. Book 6 Part 4, Q55 covers why comparing treated top-scorers to untreated others does not validate it.

**Common mistakes:**
- Using churn rate in the offered group as the effect.
- Choosing targets by propensity and calling it uplift.
- Declaring a loss from one 10,000-per-arm test without the interval.
- Forgetting the cost of the coupon on customers who would have stayed.

### Q15 ⭐⭐⭐ 🔴 A fraud model raises 5,000 alerts a day and 10% of them are fraud (500 frauds), but analysts can review only 2,000 a day at a cost of 3 each, and an average fraud costs 90. In the 2,000 highest-scored alerts 18% are fraud (360 frauds). Compute the value of reviewing the top 2,000 against a random 2,000, and explain how you would set the threshold and treat the 3,000 alerts nobody reviews.
**Asked at:** Fraud-economics material (a Dataford 'evaluate fraud detection classifier' page with a limited review-capacity framing, DataRobot guidance on setting thresholds from false-negative versus false-positive cost, an Infosys BPM case study of a review-capacity cap, Sardine and other vendor pages on false positives); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Ranking is worth 14,400 a day over random review, but the 3,000 unreviewed alerts still hold 140 frauds at 4.7% precision, above the 3.3% a review needs, so the real constraint is review capacity and I would triage rather than ignore them.

**Clarifying questions:**
- When an analyst confirms fraud, is the full 90 prevented? If only part is recovered, every value shrinks.
- Are the 3 per review only analyst time, or also customer friction? A review may delay a genuine customer.
- Can alerts be handled in cheaper ways, such as an automated step-up check? That creates a third option between review and ignore.
- Does fraud in unreviewed alerts get caught later by chargebacks, with some loss recovered? It sets the real cost of not reviewing.
- Is 18% for the top 2,000 measured on reviewed outcomes? Reviewed alerts have labels, unreviewed ones do not.

**Approach:**
1. Review cost = 2,000 x 3 = 6,000.
2. Top 2,000: 360 frauds x 90 = 32,400 gross, 26,400 net. Random 2,000: 10% = 200 frauds x 90 = 18,000, net 12,000. Ranking adds 14,400 a day.
3. Break-even precision for one review = 3 / 90 = 3.33%. Review while the marginal alert's fraud probability is above that.
4. The 3,000 left: 140 frauds, 4.67% precision, 12,600 of exposure. Average precision is above break-even, so more capacity would pay. If it were all at the average, reviewing them would net 3,600. But the pool is ranked, so the tail has lower precision than the average (in my illustrative bands 6.5%, 4.5% and 3.0%, and only the last band loses money).
5. Set the threshold at the point where precision at the margin equals 3.33% or where capacity runs out, whichever comes first. Today capacity binds.
6. Treat the unreviewed: sample them each day (a random 2% to measure fraud rate), add cheap automatic actions on the next-highest band such as step-up verification, and push for analyst capacity if the marginal band is above break-even.

**Metrics:**
- Precision at k = frauds in the top k reviewed / k. Break-even precision = review cost / loss prevented per fraud.
- Value per day = frauds caught x loss prevented - alerts reviewed x review cost.
- Guardrails: unreviewed fraud rate from a random sample, review time, customer friction.

**Risks:**
- Labels exist only for reviewed alerts, so precision in the tail is a guess until sampled.
- Fraudsters adapt to the top-scored pattern and move into the unreviewed band.
- Assuming full loss prevention overstates value.
- Capacity-capped systems drift because only top alerts are ever labelled.

**What the interviewer scores:**
- Strong: correct 26,400 against 12,000 and the break-even precision. Weak: reports precision only.
- Strong: notices the unreviewed pool is above break-even on average. Weak: "ignore low scores".
- Strong: proposes sampling and a cheaper action for the tail. Weak: "retrain".
- Strong: states the full-prevention assumption. Weak: hides it.

**Example:** (illustrative numbers) Top 2,000: 360 frauds, gross 32,400, net 26,400. Random 2,000: 200 frauds, net 12,000. Tail 3,000: 140 frauds in three bands of 1,000: net +2,850, +1,050 and -300 if reviewed. So I would add capacity for about 2,000 more alerts, not 3,000. Weak answer: "The model is 18% precise, good enough." Strong answer: "Review value is 26,400 a day, the tail is mostly worth reviewing too, so capacity is the bottleneck."

**Code:**
```python
# Illustrative numbers.
alerts, frauds, cap, rev_cost, loss = 5000, 500, 2000, 3.0, 90.0
top_frauds = 360
assert frauds / alerts == 0.10 and top_frauds / cap == 0.18
review_cost = cap * rev_cost
top_gross = top_frauds * loss                 # assumes review catches the fraud and prevents the full loss
rand_frauds = cap * frauds / alerts
rand_gross = rand_frauds * loss
print(f"review cost {review_cost:,.0f}")
print(f"top 2000: frauds {top_frauds} gross {top_gross:,.0f} net {top_gross-review_cost:,.0f}")
print(f"random 2000: frauds {rand_frauds:.0f} gross {rand_gross:,.0f} net {rand_gross-review_cost:,.0f}")
assert (review_cost, top_gross, rand_gross) == (6000, 32400, 18000)
assert (top_gross - review_cost, rand_gross - review_cost) == (26400, 12000)
print("value of ranking (top minus random):", top_gross - rand_gross)
assert top_gross - rand_gross == 14400
# Break-even precision for one review
be = rev_cost / loss
print(f"break-even precision for a review: {be:.2%}")
assert round(be, 4) == 0.0333
# The 3,000 nobody reviews
rest_n, rest_f = alerts - cap, frauds - top_frauds
print(f"unreviewed: {rest_n} alerts, {rest_f} frauds, precision {rest_f/rest_n:.2%}, exposure {rest_f*loss:,.0f}")
assert (rest_n, rest_f) == (3000, 140) and round(rest_f / rest_n, 4) == 0.0467 and rest_f * loss == 12600
print(f"average precision of the unreviewed pool is above break-even: {rest_f/rest_n > be}")
assert rest_f / rest_n > be
# If extra review capacity could be added at the same 3 per alert and the average precision held:
extra_net = rest_f * loss - rest_n * rev_cost
print(f"reviewing all 3000 at the pool average would net {extra_net:,.0f}")
assert extra_net == 3600
# But the pool is ranked: the marginal precision at rank 2001 is below the pool average. Illustrative bands:
bands = [(1000, 0.065), (1000, 0.045), (1000, 0.030)]   # (alerts, fraud rate) of ranks 2001-5000
tot = sum(n * p for n, p in bands)
print("bands add to", round(tot), "frauds")
assert round(tot) == 140
for n, p in bands:
    print(f"band of {n}: precision {p:.2%}  net of review {n*p*loss - n*rev_cost:+,.0f}")
assert (1000 * 0.030 * loss - 1000 * rev_cost) < 0 < (1000 * 0.045 * loss - 1000 * rev_cost)
```

**Output (my run):**
```text
review cost 6,000
top 2000: frauds 360 gross 32,400 net 26,400
random 2000: frauds 200 gross 18,000 net 12,000
value of ranking (top minus random): 14400.0
break-even precision for a review: 3.33%
unreviewed: 3000 alerts, 140 frauds, precision 4.67%, exposure 12,600
average precision of the unreviewed pool is above break-even: True
reviewing all 3000 at the pool average would net 3,600
bands add to 140 frauds
band of 1000: precision 6.50%  net of review +2,850
band of 1000: precision 4.50%  net of review +1,050
band of 1000: precision 3.00%  net of review -300
```

**Follow-ups:**
- How do I know the tail precision? Review a small random sample of it every day, with a weight to scale it up.
- What if review also stops fraud ring activity? Then value per review is higher than 90 and the break-even is lower.

**Common mistakes:**
- Comparing to no review instead of random review, which hides the value of ranking.
- Ignoring the cost of the 3,000 unreviewed alerts.
- Setting a score threshold without a capacity limit.
- Reading precision on reviewed alerts as precision on all alerts.

### Q16 ⭐⭐⭐ 🔴 An analyst regressed log weekly units on log price across 5,000 store-week rows and found a price elasticity of +0.4, so units rise when price rises. Managers raised prices in weeks when they expected strong demand, and a regression with store and week fixed effects gives -1.2 instead, which means a 5% relative price rise cuts units by about 6% relative. Explain the gap, compute the revenue effect of the 5% rise at -1.2, and say how you would get a cleaner estimate.
**Asked at:** Pricing case-study guides (an Interview Query pricing case-study page, Dataford pricing and price-elasticity question pages for a food distributor and a fleet, 2026 pricing data scientist job postings at companies such as Target and Klook that list elasticity modelling and A/B or geo price tests); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Managers raise prices when they expect strong demand, so price and demand move together for the wrong reason; the +0.4 is bias, the -1.2 is better but may still be biased, and at -1.2 a 5% rise cuts units by about 5.7% and revenue by about 1%.

**Clarifying questions:**
- How are prices set, by a rule or by manager judgement? Judgement tied to expected demand is the source of bias.
- Do prices change for reasons unrelated to demand, such as supplier costs? Those can be instruments.
- Are there promos mixed in the price data? A promo cuts price and lifts units, which pushes the other way.
- Is the effect needed for small changes or large ones? A log-log slope is a local approximation.
- What is unit cost? Revenue is not the goal; profit is.

**Approach:**
1. Explain the gap. Price is correlated with an unobserved demand shock (the manager's expectation). Demand shocks lift both price and units, so the regression slope is pulled up, here to +0.4.
2. Store and week fixed effects remove permanent store differences and chain-wide weeks. They do not remove a store-specific expected spike, so -1.2 can still be too close to zero.
3. Compute. Units change = 1.05^-1.2 - 1 = -5.69%. Revenue = 1.05 x 0.9431 = 0.9903, so -0.97%. The "about 6%" rule of thumb gives -6.0% and revenue -1.3%.
4. Profit view with illustrative price 10 and cost 6: gross profit per base unit goes from 4.00 to 4.24 (+6.1%) because margin per unit rises more than units fall.
5. Get a cleaner estimate: randomized or switchback price tests, geo tests, or an instrument such as supplier cost shocks that move price but not demand. In my simulation with true -1.2, pooled gave +0.38, store and week fixed effects gave -0.16, and fixed effects with a cost-shock instrument gave -1.10.
6. Check stability: placebo on past weeks, event-study around price changes, and cross-price effects.

**Metrics:**
- Elasticity = % change in units / % change in price, estimated as the coefficient on log price.
- Revenue change = (1 + dp) x (1 + dp)^e - 1. Profit change uses margin per unit.
- Guardrails: cross-price effects, competitor prices, units in later weeks.

**Risks:**
- Fixed effects give a false sense of safety.
- Instruments that also affect demand break the estimate.
- Log-log slope is not constant across the price range.
- Store-week data may include stockouts, which censor units.

**What the interviewer scores:**
- Strong: names the reverse causality (price set because of expected demand) clearly. Weak: "multicollinearity".
- Strong: computes -5.69% and about -1% revenue, not just -6%. Weak: mis-signs the revenue effect.
- Strong: says -1.2 can still be biased and proposes randomization or an instrument. Weak: accepts it.
- Strong: moves to profit. Weak: stops at revenue.

**Example:** (illustrative numbers) True elasticity -1.2. A 5% rise gives units x 0.9431 and revenue x 0.9903. At cost 6 and price 10, profit per base unit goes from 4.00 to 4.24. In a simulation where managers raise price with a demand shock they can see, pooled regression returns +0.38, fixed effects -0.16, instrumented -1.10. Weak answer: "Elasticity is positive, so raise prices." Strong answer: "Price follows demand in this data. I would estimate with randomised price changes."

**Code:**
```python
import numpy as np
# Part A: arithmetic at elasticity -1.2 for a 5% relative price rise (illustrative price 10, cost 6)
e = -1.2
units_f = 1.05 ** e
print(f"units factor {units_f:.4f} ({units_f-1:+.2%}); linear rule of thumb gives {e*5:+.1f}%")
assert round(units_f - 1, 4) == -0.0569
rev_f = 1.05 * units_f
print(f"revenue factor {rev_f:.4f} ({rev_f-1:+.2%})")
assert round(rev_f - 1, 4) == -0.0097
p0, c = 10.0, 6.0
prof0 = (p0 - c) * 1.0; prof1 = (p0 * 1.05 - c) * units_f
print(f"gross profit per base unit {prof0:.2f} -> {prof1:.3f} ({prof1/prof0-1:+.1%})")
assert round(prof1 / prof0 - 1, 3) == 0.061
# Part B: simulate why pooled OLS can show +0.4, and why fixed effects may still be biased.
rng = np.random.default_rng(11)
S, W = 50, 100
true_e = -1.2
a_s = rng.normal(0, 0.5, S)[:, None]            # store size effect on log units
w_t = rng.normal(0, 0.2, W)[None, :]            # chain-wide weekly demand
u = rng.normal(0, 0.15, (S, W))                 # store-week demand shock the manager anticipates
b_s = 0.6 * a_s                                  # big stores charge more
g_t = 0.5 * w_t                                  # prices follow the season
cost_shock = rng.normal(0, 0.05, (S, W))        # supplier cost moves, unrelated to demand (an instrument)
logp = 2.0 + b_s + g_t + 0.8 * u + cost_shock + rng.normal(0, 0.02, (S, W))
logq = 5.0 + a_s + w_t + true_e * logp + u + rng.normal(0, 0.05, (S, W))
def ols(y, X):
    X = np.column_stack([np.ones(len(y)), X]); return np.linalg.lstsq(X, y, rcond=None)[0]
y, x = logq.ravel(), logp.ravel()
pooled = ols(y, x)[1]
# two-way demeaning = store and week fixed effects
def tw(m): return m - m.mean(1, keepdims=True) - m.mean(0, keepdims=True) + m.mean()
fe = (tw(logp).ravel() @ tw(logq).ravel()) / (tw(logp).ravel() @ tw(logp).ravel())
# IV with the cost shock inside the FE model
z = tw(cost_shock).ravel()
iv = (z @ tw(logq).ravel()) / (z @ tw(logp).ravel())
print(f"pooled {pooled:+.2f} | store+week FE {fe:+.2f} | FE + cost-shock IV {iv:+.2f} | truth {true_e:+.2f}")
assert pooled > 0 and fe > true_e and abs(iv - true_e) < 0.15
assert fe < 0
```

**Output (my run):**
```text
units factor 0.9431 (-5.69%); linear rule of thumb gives -6.0%
revenue factor 0.9903 (-0.97%)
gross profit per base unit 4.00 -> 4.244 (+6.1%)
pooled +0.38 | store+week FE -0.16 | FE + cost-shock IV -1.10 | truth -1.20
```

**Follow-ups:**
- My simulated fixed-effects result (-0.16) is far from the prompt's -1.2. Is that a contradiction? No. They are different data. The lesson is only that fixed effects can leave bias, not that its size is typical.
- What is the cleanest design? A randomised price test across stores or weeks. Book 6 Part 4, Q13 covers reading a price change launched in one city.

**Common mistakes:**
- Taking +0.4 as a real elasticity.
- Reading "-1.2" as exactly -6% when it is -5.69%.
- Quoting revenue change without the product of price and units.
- Believing fixed effects remove all confounding.

### Q17 ⭐⭐⭐ 🔴 A one-week promotion cut the price of Brand X by 1.00 a unit on every unit, from a full-price margin of 3.00. Units were 10,000 against a baseline of 6,000 (+67% relative to baseline). The two following weeks sold 5,000 and 5,400 against the same 6,000 baseline, and the sister Brand Y, with a margin of 2.50 a unit, lost 1,000 units in the promotion week. Compute the net margin impact over the three weeks and say what a promotion evaluation must include.
**Asked at:** Promotion and incrementality material (Talon.One and Uniqodo pages on promotion ROI and incrementality, an INFORMS Management Science paper on whether coupons expand or cannibalise revenue, an incrmntal post on promos and ad spend); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The promotion looks good in its own week, +2,000 of margin, but over three weeks Brand X nets -2,800 and Brand Y loses 2,500, so the promotion lost 5,300 of margin.

**Clarifying questions:**
- Is the baseline of 6,000 a clean forecast? A wrong baseline moves every number here.
- Does the 1.00 discount apply to all units including the baseline ones? Yes per the prompt, and that is what makes it expensive.
- Did Brand Y recover in the following weeks, or was its loss permanent? It changes the cannibalisation size.
- Were there trade-funding or fixed promo costs? They would be on top.
- Did the promotion bring in new customers who stayed? That is the only long-run upside here.

**Approach:**
1. Promotion week: 10,000 units x (3.00 - 1.00) = 20,000 against baseline 6,000 x 3.00 = 18,000. Gain +2,000.
2. Pull-forward: week 1 is 5,000 x 3.00 = 15,000, so -3,000. Week 2 is 5,400 x 3.00 = 16,200, so -1,800.
3. Brand X net = 2,000 - 3,000 - 1,800 = -2,800.
4. Brand Y lost 1,000 units at 2.50 = -2,500.
5. Total over the three weeks = -5,300 of margin.
6. Cross-check in units. Extra units in the promo week 4,000, pulled forward 1,600, so only 2,400 net extra Brand X units, and each unit made less margin.
7. Say what the evaluation needs: a baseline, pull-forward and halo or cannibalisation weeks, sister products, cost of the promotion, and a view on new customers.

**Metrics:**
- Incremental margin = sum over weeks of (actual units x actual margin - baseline units x baseline margin), all affected products, all affected weeks.
- Break-even promo-week units = baseline margin / promo margin = 18,000 / 2.00 = 9,000 for the promo week alone.
- Guardrails: category total margin, repeat purchase after the promotion.

**Risks:**
- A baseline from the past misses trends or events.
- Stopping at two post-weeks may miss a longer dip, or end too early.
- Y's loss might partly return later.
- The +67% headline hides that 6,000 baseline units also got the discount.

**What the interviewer scores:**
- Strong: nets margin over time and across brands, reaching -5,300. Weak: reports +67% or +2,000.
- Strong: explains why the break-even is 9,000 units in the promo week, and 12,650 once dips and Y are counted. Weak: no break-even.
- Strong: separates new customers from pull-forward. Weak: counts all extra units as incremental.
- Strong: asks about the baseline. Weak: takes it as given.

**Example:** (illustrative numbers) Promo week +2,000, week 1 -3,000, week 2 -1,800, Brand X net -2,800, Brand Y -2,500, total -5,300. Discount handed to baseline buyers is 6,000 (6,000 units x 1.00). To break even over all three weeks you would have needed 12,650 units in the promo week, not 10,000. Weak answer: "Units were up 67%, success." Strong answer: "Margin was down 5,300 once pull-forward and Brand Y are counted."

**Code:**
```python
# Illustrative numbers. Brand X margin 3.00 per unit at full price, promotion gives 1.00 off on every unit.
base, m_full, off = 6000, 3.00, 1.00
promo_units, post = 10000, [5000, 5400]
m_promo = m_full - off
print("promo lift", f"{promo_units/base-1:+.1%}")
assert round(promo_units / base - 1, 3) == 0.667
base_margin = base * m_full
wk0 = promo_units * m_promo - base_margin
wk1 = post[0] * m_full - base_margin
wk2 = post[1] * m_full - base_margin
x_net = wk0 + wk1 + wk2
print(f"X promo week {wk0:+,.0f}, week+1 {wk1:+,.0f}, week+2 {wk2:+,.0f}, X net {x_net:+,.0f}")
assert (wk0, wk1, wk2, x_net) == (2000, -3000, -1800, -2800)
y_loss = -1000 * 2.50
total = x_net + y_loss
print(f"Brand Y {y_loss:+,.0f}; total over 3 weeks {total:+,.0f}")
assert (y_loss, total) == (-2500, -5300)
# Unit view
extra = promo_units - base; pull = (base - post[0]) + (base - post[1])
print(f"extra units in promo {extra}, pulled forward {pull}, net extra units for X {extra-pull}")
assert (extra, pull, extra - pull) == (4000, 1600, 2400)
# Break-even in the promo week alone (no halo, no dip): units needed so that units*2 = 6000*3
be = base * m_full / m_promo
print("promo-week break-even units:", be)
assert be == 9000
# Subsidy paid to people who would have bought anyway
print("discount given away on baseline units:", base * off)
assert base * off == 6000
# Break-even if two post weeks dip is as observed and Y loses 1,000: units needed in promo week
need = (base_margin + 3000 + 1800 + 2500) / m_promo
print("promo-week units needed to break even over 3 weeks incl. dips and Y:", need)
assert need == 12650
```

**Output (my run):**
```text
promo lift +66.7%
X promo week +2,000, week+1 -3,000, week+2 -1,800, X net -2,800
Brand Y -2,500; total over 3 weeks -5,300
extra units in promo 4000, pulled forward 1600, net extra units for X 2400
promo-week break-even units: 9000.0
discount given away on baseline units: 6000.0
promo-week units needed to break even over 3 weeks incl. dips and Y: 12650.0
```

**Follow-ups:**
- When would I still run it? To win new customers who stay, clear stock, or to defend share with a competitor, when I can show those gains.
- How do I improve the baseline? Use a control set of stores without the promotion or a model of past weeks with the same seasonality.

**Common mistakes:**
- Evaluating the promo week only.
- Using the discount on sales, but ignoring the discount on baseline units.
- Leaving out sister brands.
- Using revenue instead of margin.

### Q18 ⭐⭐⭐ 🔴 A lender's default model was trained only on the 20,000 applicants it approved out of 50,000 (a 40% approval rate), where 6% defaulted. A pilot approved a random 2,000 of the 30,000 declined applicants and 18% of them (360) defaulted, although the model had predicted 8% for them. A repaid loan earns 150 and a default loses 600. Compute the expected profit per loan in the pilot group and a rough 95% interval for its default rate, and explain how you would fix the training data.
**Asked at:** Credit-risk material (a Dataford 'optimal cut-off score to maximise profit' page, an Interview Query auto-lending data scientist guide, a quintedge credit-risk interview page, academic papers on profit-maximising cut-offs); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The pilot shows the declined group defaults at 18%, not the 8% the model predicted, and expected profit is only +15 per loan (between +2.4 and +27.6 at the edges of the interval), so the model was trained on a biased sample and I would use the random pilot to correct it.

**Clarifying questions:**
- How were the 20,000 approved chosen, by a score cut-off or by a human rule? It decides how biased the training data is.
- Was the pilot truly random among the 30,000 declined, and were all 2,000 followed to the same horizon? Otherwise 18% is not comparable to 6%.
- Are there funding, servicing and collection costs? The +15 is before them.
- Is a regulator or policy limit involved in approving declined people? A pilot may need approval.
- Is there any information on declined applicants from other sources, such as bureau outcomes? It helps reject inference.

**Approach:**
1. Check the base: 20,000 of 50,000 approved is 40%, so 30,000 were declined.
2. Pilot default rate = 360 / 2,000 = 18%. Expected profit per loan = 0.82 x 150 - 0.18 x 600 = 123 - 108 = +15, or +30,000 over the 2,000.
3. Interval: standard error = sqrt(0.18 x 0.82 / 2,000) = 0.86 points, so 16.3% to 19.7% (Wilson gives 16.4% to 19.7%). Profit per loan at those ends is +27.63 and +2.37. Break-even PD is 150 / 750 = 20%, so the whole interval is just below it.
4. Compare to the model. 18% against a prediction of 8% is a gap of 10 points, about 16 standard errors. The model badly underrates risk in the declined group, so it was trained only on approved people.
5. Whole-population default rate if the declined pool behaves like the pilot is (20,000 x 6% + 30,000 x 18%) / 50,000 = 13.2%, not 6%.
6. Fix the training data. Give each pilot loan weight 30,000 / 2,000 = 15 so the 2,000 stand for the 30,000, add them to the approved data, and retrain. Keep a standing random exploration slice, and compare reject-inference methods against the pilot as truth.
7. The 15 profit is before funding and servicing cost. With an illustrative 20 per loan of such cost it becomes -5. So do not approve the declined group on this evidence.

**Metrics:**
- Default rate = defaults / loans, same horizon for both groups.
- Expected profit per loan = (1 - PD) x 150 - PD x 600; break-even PD = 150 / (150 + 600) = 20%.
- Calibration of the model on the pilot: predicted PD / actual default rate, by score band.
- Guardrails: exposure in the exploration slice, regulatory limits.

**Risks:**
- Selection bias: a model trained only on approved loans cannot see how declined people behave.
- Pilot too small to tell 17% from 19%, and profit sits near zero.
- Weights of 15 make results sensitive to a few pilot loans.
- The pilot group may behave differently later in the cycle.

**What the interviewer scores:**
- Strong: sees that training on approved only is selection bias and uses the random pilot. Weak: "get more data".
- Strong: computes profit +15 and the interval and break-even PD. Weak: says "18% is bad, so decline".
- Strong: knows +15 before costs may be negative. Weak: claims it is profitable.
- Strong: weights pilot rows and keeps exploring. Weak: one-off fix.

**Example:** (illustrative numbers) Pilot: 2,000 loans, 360 defaults (18%), profit per loan +15, 95% band for default rate 16.3% to 19.7%. Model said 8%. Weighted by 15, the pilot represents all 30,000. Weak answer: "Add the declined people to the training set with a guess of their outcome." Strong answer: "Use the random pilot as real labels, weight it by 15, and keep a small random approval slice permanently."

**Code:**
```python
import math
# Illustrative numbers.
apps, approved = 50_000, 20_000
declined = apps - approved
print("approval rate", approved / apps, "declined", declined)
assert approved / apps == 0.40 and declined == 30_000
pilot, defaults = 2000, 360
p = defaults / pilot
earn, lose = 150.0, 600.0
profit = (1 - p) * earn - p * lose
print(f"pilot default rate {p:.1%}, expected profit per loan {profit:+.2f}, pilot total {profit*pilot:+,.0f}")
assert p == 0.18 and round(profit, 2) == 15.00
# Break-even PD for this loan economics
be = earn / (earn + lose)
print(f"break-even PD {be:.1%}")
assert be == 0.2
# Normal and Wilson intervals
se = math.sqrt(p * (1 - p) / pilot)
lo, hi = p - 1.96 * se, p + 1.96 * se
z = 1.96
c = (p + z*z/(2*pilot)) / (1 + z*z/pilot)
h = z * math.sqrt(p*(1-p)/pilot + z*z/(4*pilot**2)) / (1 + z*z/pilot)
wlo, whi = c - h, c + h
print(f"normal 95%: {lo:.2%}-{hi:.2%}; Wilson 95%: {wlo:.2%}-{whi:.2%}")
assert round(lo, 3) == 0.163 and round(hi, 3) == 0.197
def prof(q): return (1 - q) * earn - q * lose
print(f"profit per loan at interval ends: {prof(hi):+.2f} to {prof(lo):+.2f}")
assert round(prof(hi), 2) == 2.37 and round(prof(lo), 2) == 27.63
# Model predicted 8% for them. Is 18% different?
zscore = (p - 0.08) / math.sqrt(0.08 * 0.92 / pilot)
print(f"z versus the model's 8%: {zscore:.1f}")
assert zscore > 10
# Blended default rate if declined pool behaves like the pilot
blend = (approved * 0.06 + declined * p) / apps
print(f"all applicants default rate: {blend:.1%}  (approved-only view said 6.0%)")
assert round(blend, 3) == 0.132
# Reject inference weights from the random pilot: each pilot loan stands for declined/pilot loans
w = declined / pilot
print("weight per pilot loan:", w)
assert w == 15
# Effective sample size cost of weighting: pilot is only 2,000 rows
print("training rows: 20,000 approved (weight 1) + 2,000 pilot (weight 15 = represents 30,000)")
# The 15 is before funding, servicing and collection costs. Illustrative 20 per loan of such costs flips the sign.
print("profit per loan after an illustrative 20 of funding+servicing cost:", round(profit - 20, 2))
assert round(profit - 20, 2) == -5.00
```

**Output (my run):**
```text
approval rate 0.4 declined 30000
pilot default rate 18.0%, expected profit per loan +15.00, pilot total +30,000
break-even PD 20.0%
normal 95%: 16.32%-19.68%; Wilson 95%: 16.38%-19.74%
profit per loan at interval ends: +2.37 to +27.63
z versus the model's 8%: 16.5
all applicants default rate: 13.2%  (approved-only view said 6.0%)
weight per pilot loan: 15.0
training rows: 20,000 approved (weight 1) + 2,000 pilot (weight 15 = represents 30,000)
profit per loan after an illustrative 20 of funding+servicing cost: -5.0
```

**Follow-ups:**
- Why not just retrain on the pilot? It is 2,000 rows. Combined with the 20,000 and weighted, it corrects the selection while keeping data volume.
- Is exploring declined applicants fair or allowed? It needs a risk cap, sign-off and an exposure limit, and in some places legal review.

**Common mistakes:**
- Calling +15 per loan profitable without costs.
- Treating the 2,000 as only 2,000 rows when they stand for 30,000.
- Reporting the default rate without an interval.
- Retraining on approved data only and expecting the model to extrapolate.

### Q19 ⭐⭐ 🟢 A delivery app plans a feature with a one-off build and launch cost of 120,000. Each extra order it brings adds a contribution margin of 2.50 after variable costs, and the team expects 30,000 extra orders a month. Compute the break-even number of orders and the months to break even, and say which sensitivity you would show the product manager.
**Asked at:** Market-sizing and unit-economics material (PracHub market-sizing concept page, MBB Prep unit-economics and market-sizing pages, PrepLounge break-even and Leland and RoadToOffer sizing guides); consulting-case guides rather than data-scientist-specific pages; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Break-even is 120,000 / 2.50 = 48,000 extra orders, which is 1.6 months at 30,000 a month, so the real question is how many of those orders are truly extra and how fast volume ramps.

**Clarifying questions:**
- Are the 30,000 orders incremental, or would some customers have ordered anyway? Only incremental orders pay for the build.
- Is 2.50 the contribution after variable cost, including any incentive cost? It is the only thing that repays the 120,000.
- Are there running costs after launch, such as support or maintenance? They stretch payback.
- Does volume start at 30,000 or ramp up? Early months can be far lower.
- What payback is acceptable to the business? It sets what counts as safe.

**Approach:**
1. Break-even orders = fixed cost / contribution per order = 120,000 / 2.50 = 48,000.
2. Months to break even = 48,000 / 30,000 = 1.6.
3. Sensitivity on the two uncertain inputs, orders a month and contribution per order. At 15,000 orders and 2.50 it is 3.2 months. At 10,000 orders and 1.50 it is 8.0 months.
4. Show cannibalisation. If 40% of the 30,000 would have happened anyway, 18,000 are incremental, and payback is 2.67 months.
5. Show a ramp (10,000, then 20,000, then 30,000): break-even in month 3, about 2.6 months. With 15,000 a month of upkeep, 2.0 months.
6. Recommend: show the PM one table of orders per month against contribution per order, and mark which cells exceed the payback limit. The orders input is the first one to validate.

**Metrics:**
- Break-even orders = build cost / contribution margin per incremental order.
- Payback months = build cost / monthly net contribution.
- Guardrails: share of orders that are incremental, repeat rate, support contacts.

**Risks:**
- Taking gross orders as incremental.
- Using an optimistic volume forecast from a feature that is not launched.
- Ignoring maintenance and opportunity cost of engineers.
- Contribution margin falling if the feature needs discounts to drive usage.

**What the interviewer scores:**
- Strong: gets 48,000 and 1.6, then immediately questions the 30,000. Weak: stops at the formula.
- Strong: a two-way sensitivity table. Weak: one scenario.
- Strong: separates incremental from total orders. Weak: ignores it.
- Strong: mentions a ramp and run cost. Weak: ignores time.

**Example:** (illustrative numbers) Build 120,000, contribution 2.50. Break-even 48,000 orders. At 30,000 a month: 1.6 months. At 20,000: 2.4. At 10,000: 4.8. With 40% cannibalisation: 2.67 months. Weak answer: "Break-even in 1.6 months, ship it." Strong answer: "1.6 months if all 30,000 are new and arrive on day one. I would test the incremental share first, since 10,000 incremental takes about 5 months."

**Code:**
```python
# Illustrative numbers.
build, cm, orders = 120_000, 2.50, 30_000
be_orders = build / cm
months = be_orders / orders
print(f"break-even orders {be_orders:,.0f}; months at {orders:,}/month: {months:.2f}")
assert be_orders == 48_000 and round(months, 2) == 1.60
# Sensitivity: monthly extra orders x contribution per order (months to break even)
print("months to break even (rows: extra orders/month; cols: contribution per order)")
cms = [1.50, 2.00, 2.50]
print("orders   " + "  ".join(f"{c:5.2f}" for c in cms))
for o in [10_000, 15_000, 20_000, 30_000]:
    print(f"{o:6,}   " + "  ".join(f"{build/(o*c):5.1f}" for c in cms))
assert round(build / (15_000 * 2.50), 1) == 3.2 and round(build / (10_000 * 1.50), 1) == 8.0
# Cannibalisation: if 40% of the 30,000 would have happened anyway, only 18,000 are incremental
inc = 30_000 * 0.60
print(f"incremental orders {inc:,.0f}; months {build/(inc*cm):.2f}")
assert inc == 18_000 and round(build / (inc * cm), 2) == 2.67
# A ramp: 10,000, 20,000, 30,000 then flat; cumulative contribution
cum, m, vols = 0.0, 0, [10_000, 20_000] + [30_000] * 10
for v in vols:
    m += 1; cum += v * cm
    if cum >= build:
        prev = cum - v * cm
        print(f"with a 3-month ramp break-even falls in month {m} (about {m-1+(build-prev)/(v*cm):.2f} months)")
        break
assert m == 3
# Ongoing run cost: 15,000 a month of upkeep delays things
net_month = 30_000 * cm - 15_000
print(f"with 15,000/month upkeep: {build/net_month:.2f} months")
assert round(build / net_month, 2) == 2.00
```

**Output (my run):**
```text
break-even orders 48,000; months at 30,000/month: 1.60
months to break even (rows: extra orders/month; cols: contribution per order)
orders    1.50   2.00   2.50
10,000     8.0    6.0    4.8
15,000     5.3    4.0    3.2
20,000     4.0    3.0    2.4
30,000     2.7    2.0    1.6
incremental orders 18,000; months 2.67
with a 3-month ramp break-even falls in month 3 (about 2.60 months)
with 15,000/month upkeep: 2.00 months
```

**Follow-ups:**
- Which sensitivity matters most? Incremental orders per month, since it can be off by a factor of three, while contribution per order is usually known within 20%.
- How would I measure incremental orders? A holdout of customers without the feature, run before a full launch.

**Common mistakes:**
- Treating break-even orders as months.
- Using revenue or order value instead of contribution.
- Forgetting cannibalisation.
- Leaving out maintenance after launch.

### Q20 ⭐⭐ 🟢 On a food order with a basket of 20, a platform earns an 18% commission (of the basket) and a delivery fee of 2.00, and it pays 3.50 to the courier, 1.50 in discounts, 0.40 in payment fees and 0.30 in support cost. Compute the contribution per order, and name the two levers you would test first.
**Asked at:** Marketplace and take-rate material (an inpractise take-rate course page, a Codemia Thumbtack data scientist guide describing a marketplace case round, ibinterviewquestions and hackingthecaseinterview marketplace and supply-demand pages); general marketplace guides, nothing specific to Uber, DoorDash or Swiggy loops; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Revenue per order is 3.60 + 2.00 = 5.60 and costs are 5.70, so contribution is -0.10 per order, a small loss, and I would test discounts and courier cost first.

**Clarifying questions:**
- Is the 18% on the basket before or after the 1.50 discount? I assume before. After would reduce commission by 0.27.
- Is the 1.50 discount funded by the platform, or shared with the restaurant? It is the largest lever.
- Is the average basket 20 for all orders or only this one? Averages hide small baskets with big losses.
- Does the courier cost include batching and idle time? It varies a lot with density.
- Are there other costs like refunds or cloud? Include them if they scale with orders.

**Approach:**
1. Revenue: commission 0.18 x 20 = 3.60, plus delivery fee 2.00 = 5.60.
2. Costs: courier 3.50 + discounts 1.50 + payment fees 0.40 + support 0.30 = 5.70.
3. Contribution = 5.60 - 5.70 = -0.10 per order. Break-even commission is (5.70 - 2.00) / 20 = 18.5%.
4. Size the levers one at a time: targeted discounts 1.50 to 1.00 gives +0.50; batching courier cost 3.50 to 3.00 gives +0.50; delivery fee 2.00 to 2.50 gives +0.50; commission 18% to 19% gives +0.20; basket 20 to 22 gives +0.36.
5. Pick the first two to test. Discounts, because they are fully in our control and can be aimed at new customers only. Courier cost through batching or better dispatch, because it is the biggest cost line. Both can be tested without raising prices for customers.
6. Run them as experiments with guardrails on order volume, ratings and delivery time. A fee rise can lose orders, so I measure net contribution per user, not per order.

**Metrics:**
- Contribution per order = commission + delivery fee - courier pay - discounts - payment fees - support cost.
- Contribution per user per week = contribution per order x orders per user.
- Guardrails: orders per user, delivery time, late rate, ratings.

**Risks:**
- Average basket hides orders that lose much more.
- Discounts bring orders that also have value later, so cutting them can cost growth.
- Fee increases affect conversion at checkout.
- Batching lengthens delivery time (the idea of Q31 in this part).

**What the interviewer scores:**
- Strong: gets -0.10 and says it is a loss. Weak: forgets one revenue or cost line.
- Strong: sizes levers on the same per-order scale. Weak: lists levers with no numbers.
- Strong: names guardrails and volume risk. Weak: "raise fees".
- Strong: asks about contribution per user. Weak: stops at per order.

**Example:** (illustrative numbers) Revenue 5.60, cost 5.70, contribution -0.10. A 0.50 cut in discounts gives +0.40. Batching to save 0.50 on courier gives +0.40. A 0.50 fee rise gives +0.40 per order before any loss of orders. Per 1,000 orders: -100 now; if a 0.50 fee rise loses 10% of orders: 900 x 0.40 = +360. Weak answer: "Margin is thin, raise commission." Strong answer: "We lose 0.10 an order. Discounts and courier cost are in our hands, so I test those first."

**Code:**
```python
# Illustrative numbers. Assumption: commission is on the basket before the platform-funded discount.
basket = 20.0
commission = 0.18 * basket
fee = 2.00
revenue = commission + fee
costs = {"courier": 3.50, "discounts": 1.50, "payment fees": 0.40, "support": 0.30}
total_cost = sum(costs.values())
contrib = revenue - total_cost
print(f"commission {commission:.2f} + fee {fee:.2f} = revenue {revenue:.2f}; costs {total_cost:.2f}; contribution {contrib:+.2f}")
assert round(commission, 2) == 3.60 and round(revenue, 2) == 5.60 and round(total_cost, 2) == 5.70 and round(contrib, 2) == -0.10
# Break-even commission rate holding all else fixed
be_rate = (total_cost - fee) / basket
print(f"break-even commission rate {be_rate:.2%}")
assert round(be_rate, 4) == 0.185
# Lever table (each applied alone). Illustrative sizes of the move.
levers = {
 "targeted discounts: cut 1.50 to 1.00":        0.50,
 "batching: courier cost 3.50 to 3.00":         0.50,
 "delivery fee 2.00 to 2.50":                   0.50,
 "commission 18% to 19%":                       0.01 * basket,
 "basket 20 to 22 (more items per order)":      0.18 * 2.0,
}
for k, v in levers.items():
    print(f"{k:45} {v:+.2f} per order -> contribution {contrib+v:+.2f}")
assert round(contrib + 0.50, 2) == 0.40 and round(contrib + 0.20, 2) == 0.10 and round(contrib + 0.36, 2) == 0.26
# Volume risk: if a 0.50 fee rise cuts orders by 10%, per-1,000-orders result
before = 1000 * contrib; after = 900 * (contrib + 0.50)
print(f"per 1,000 orders: {before:+.0f} before; fee rise with 10% fewer orders {after:+.0f}")
assert round(before) == -100 and round(after) == 360
```

**Output (my run):**
```text
commission 3.60 + fee 2.00 = revenue 5.60; costs 5.70; contribution -0.10
break-even commission rate 18.50%
targeted discounts: cut 1.50 to 1.00          +0.50 per order -> contribution +0.40
batching: courier cost 3.50 to 3.00           +0.50 per order -> contribution +0.40
delivery fee 2.00 to 2.50                     +0.50 per order -> contribution +0.40
commission 18% to 19%                         +0.20 per order -> contribution +0.10
basket 20 to 22 (more items per order)        +0.36 per order -> contribution +0.26
per 1,000 orders: -100 before; fee rise with 10% fewer orders +360
```

**Follow-ups:**
- Why not raise the commission? Restaurants may refuse or raise menu prices. The 18.5% break-even is only 0.5 points above today.
- Does a loss per order mean stop? Not if repeat orders and later cheaper orders make the customer worth it. Check contribution over the customer's life.

**Common mistakes:**
- Taking commission as 18% of the basket after discounts without saying so.
- Forgetting the delivery fee as revenue.
- Listing levers without sizes.
- Optimising per order while volume falls.

### Q21 ⭐⭐ 🟢 A survey of 1,000 households in a city of 2,000,000 households finds that 300 (30%) use a food-delivery app in a typical month. Users order 3 times a month at an average of 12, and a new entrant hopes for a 25% share of orders. Compute the monthly order value this implies, the 95% margin of error on the 30% figure, and which input you would validate with data first.
**Asked at:** Market-sizing and unit-economics material (PracHub market-sizing concept page, MBB Prep unit-economics and market-sizing pages, PrepLounge break-even and Leland and RoadToOffer sizing guides); consulting-case guides rather than data-scientist-specific pages; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The survey implies 600,000 user households, 1.8 million orders and 21.6 million of orders a month, the 30% has a margin of error of 2.8 points, and the first input I would check is the entrant's 25% share, not the survey.

**Clarifying questions:**
- How was the sample drawn? A random sample gives the margin below, an app-based or phone survey can be biased.
- Is "typical month" one month or a year average? Usage swings with season.
- Are 3 orders a month and 12 an order averages for the users or for those who answered? Heavy users distort the mean.
- Is the 25% share meant for orders or users, and when? A new entrant takes years to reach it.
- Is the market defined as the city's households only? Offices and visitors may also order.

**Approach:**
1. Users = 30% x 2,000,000 = 600,000 households.
2. Orders = 600,000 x 3 = 1.8 million a month. Order value = 1.8 million x 12 = 21.6 million a month.
3. Entrant at 25% of orders: 450,000 orders, 5.4 million a month. At equal frequency that is 150,000 households.
4. Margin of error = 1.96 x sqrt(0.3 x 0.7 / 1,000) = 2.84 points, so 27.2% to 32.8%. That is 543,000 to 657,000 households and 19.6 to 23.6 million of order value (9.5% either way). The finite-population correction is 0.99975, so ignore it. If the survey had a design effect of 2 the margin would be 4.0 points.
5. Compare the uncertainty of each input. Usage share spread: 19% of the base value. Orders per user 2 to 4: 67% of the base. Order value 10 to 14: 33%. The survey margin is the best known number.
6. Validate first the order frequency (3 a month) and the 25% share, with order data from panel or transaction sources, because they move the answer more than the survey does.

**Metrics:**
- Margin of error for a proportion = 1.96 x sqrt(p(1-p)/n).
- Market value = households x usage share x orders per user x order value.
- Entrant value = market value x share of orders.
- Guardrails: sample representativeness, seasonality.

**Risks:**
- Survey bias, such as only online respondents.
- Averages hide a long tail of heavy users.
- A share assumption copied from a different market.
- Treating a margin of error as total uncertainty, when the survey covers only one of four inputs.

**What the interviewer scores:**
- Strong: correct chain of numbers and a margin of error of 2.8 points. Weak: skips the interval.
- Strong: compares the uncertainty of all inputs. Weak: only talks about sample size.
- Strong: challenges the 25% target. Weak: accepts it.
- Strong: names a data source to validate. Weak: "do more research".

**Example:** (illustrative numbers) 1,000 surveyed, 300 users, 30% plus or minus 2.8 points. City: 600,000 households, 1.8 million orders, 21.6 million. Entrant at 25%: 5.4 million. If frequency is 2 not 3, the market is 14.4 million. Weak answer: "21.6 million, so we can get 5.4 million." Strong answer: "21.6 million plus or minus about 2 million from the survey, but frequency could move it by a third, and 25% share is a target, not an estimate."

**Code:**
```python
import math
# Illustrative numbers.
hh, n, k = 2_000_000, 1000, 300
p = k / n
users = hh * p
orders = users * 3
value = orders * 12
print(f"users {users:,.0f}; orders {orders:,.0f}; market value {value:,.0f}")
assert (users, orders, value) == (600_000, 1_800_000, 21_600_000)
entrant_orders = 0.25 * orders; entrant_value = 0.25 * value
print(f"25% share: {entrant_orders:,.0f} orders, {entrant_value:,.0f} a month")
assert (entrant_orders, entrant_value) == (450_000, 5_400_000)
se = math.sqrt(p * (1 - p) / n); moe = 1.96 * se
print(f"standard error {se:.4f}; 95% margin of error {moe:.2%} points; interval {p-moe:.2%}-{p+moe:.2%}")
assert round(moe, 4) == 0.0284
lo, hi = (p - moe) * hh, (p + moe) * hh
print(f"user households {lo:,.0f}-{hi:,.0f}; market value {lo*3*12:,.0f}-{hi*3*12:,.0f} ({moe/p:.1%} either way)")
# Finite population correction is negligible
fpc = math.sqrt((hh - n) / (hh - 1)); print("finite-population factor", round(fpc, 5))
assert fpc > 0.9997
# Design effect: a clustered or phone survey with deff 2 widens the margin
moe2 = 1.96 * math.sqrt(2) * se
print(f"with design effect 2: margin {moe2:.2%}")
assert round(moe2, 3) == 0.040
# Which input moves the answer most? Plausible ranges for each, one at a time, around 21.6M market value.
base = value
sens = {
 "usage share (survey margin)":      (0.2716 * hh * 3 * 12, 0.3284 * hh * 3 * 12),
 "orders per user 2 to 4":           (users * 2 * 12, users * 4 * 12),
 "order value 10 to 14":             (orders * 10, orders * 14),
}
for kk, (a, b) in sens.items():
    print(f"{kk:30} {a:>12,.0f} to {b:>12,.0f}  (spread {(b-a)/base:.0%} of base)")
assert round((sens["orders per user 2 to 4"][1] - sens["orders per user 2 to 4"][0]) / base, 2) == 0.67
# The entrant's own 25% target: what it implies in users at equal frequency
print("25% of orders at equal frequency = 25% of the 600,000 users =", 0.25 * users)
assert 0.25 * users == 150_000
```

**Output (my run):**
```text
users 600,000; orders 1,800,000; market value 21,600,000
25% share: 450,000 orders, 5,400,000 a month
standard error 0.0145; 95% margin of error 2.84% points; interval 27.16%-32.84%
user households 543,194-656,806; market value 19,554,977-23,645,023 (9.5% either way)
finite-population factor 0.99975
with design effect 2: margin 4.02%
usage share (survey margin)      19,555,200 to   23,644,800  (spread 19% of base)
orders per user 2 to 4           14,400,000 to   28,800,000  (spread 67% of base)
order value 10 to 14             18,000,000 to   25,200,000  (spread 33% of base)
25% of orders at equal frequency = 25% of the 600,000 users = 150000.0
```

**Follow-ups:**
- How big a sample for a 1-point margin? Roughly (1.96 / 0.01)^2 x 0.21 = about 8,000 households, if the sample is random.
- What would I do about heavy-user skew? Ask for the distribution of orders per user, not just the mean.

**Common mistakes:**
- Applying the margin of error to the total market without other inputs.
- Calling 30% exact.
- Using a sample of 1,000 as if it said something about frequency of ordering.
- Forgetting that share is a target.

### Q22 ⭐⭐ 🟢 A product sold 1,400 units a day on the 5 days a week it stayed in stock and 1,000 units on each of the 2 days it ran out, so weekly sales were 9,000 units. If true demand on the out-of-stock days equals demand on in-stock days, compute weekly demand, the lost units and the lost margin at 4 per unit, and explain why a forecast trained on sales understates demand.
**Asked at:** Forecasting and inventory material (PracHub retail demand-forecasting and inventory-and-stockout concept pages, a Dataford supermarket demand-forecasting page attributed in its title to a BCG data scientist interview but unverified, a PyCon DE 2025 talk on stockouts in retail forecasting); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** If demand on the 2 stock-out days matches the in-stock days, true weekly demand is 9,800, so 800 units and 3,200 of margin were lost, and a forecast trained on sales learns the 9,000 and bakes the shortage into next week.

**Clarifying questions:**
- Did the product sell out early in the day or is 1,000 the full stock? Early sell-outs hide more demand.
- Is the in-stock demand of 1,400 itself capped on some days? Even in-stock days can sell out late.
- Is 4 per unit margin after discounts? It is the value of one lost sale.
- Do shoppers substitute or come back later? Lost margin is an upper bound if they do.
- Can I see hourly sales and stock position? It lets me estimate demand during the stock-out hours.

**Approach:**
1. Sales: 5 x 1,400 + 2 x 1,000 = 9,000 a week.
2. Demand if out-of-stock days equal in-stock days: 7 x 1,400 = 9,800 a week.
3. Lost units = 9,800 - 9,000 = 800. Lost margin = 800 x 4 = 3,200 a week.
4. Why a sales-trained forecast is low: sales are demand cut off at stock. The average daily sales is 1,285.7 against 1,400 demand, 8.2% too low. Planning to that number means fewer units, more stock-outs, and lower sales next time, a loop.
5. If 30% of shoppers substitute or return, the margin loss falls to 2,240. The 3,200 is an upper bound.
6. Fix: mark stock-out days and hours, train on in-stock days or use a censored model (Tobit or survival style) that treats the 1,000 as "at least 1,000". In my simulation true mean demand is 1,400 but mean sales are 1,286 because of stock-outs; sales on in-stock days alone are 1,399. Use hour-of-day sell-through to estimate stock-out-hour demand, and trial higher stock on some stores to learn the demand.

**Metrics:**
- Lost units = estimated demand - sales. Lost margin = lost units x margin per unit.
- In-stock rate = days (or hours) with stock / total days (or hours).
- Guardrails: waste or markdown cost if stock is raised, substitution rate.

**Risks:**
- Even in-stock days can be cut off by a late sell-out, so 1,400 is a floor.
- Demand on stock-out days might differ (for example weekends).
- Counting all lost units as lost margin ignores substitution.
- Raising stock without waste data trades one loss for another.

**What the interviewer scores:**
- Strong: 9,800, 800 and 3,200, and says the assumption behind them. Weak: just 9,000.
- Strong: explains censoring in one sentence. Weak: "the data is biased".
- Strong: proposes a censored model or in-stock-only training plus a stock test. Weak: "add more data".
- Strong: gives lost margin as an upper bound. Weak: states it as fact.

**Example:** (illustrative numbers) In stock: 1,400 a day for 5 days. Out: 1,000 a day for 2 days. Sales 9,000, demand 9,800, lost 800 units, lost margin 3,200. With 30% recapture the loss is 2,240. Weak answer: "Sales were 9,000, so forecast 9,000." Strong answer: "Demand was about 9,800, sales are a lower bound, so I train on in-stock days or a censored model."

**Code:**
```python
# Illustrative numbers.
in_days, out_days = 5, 2
sales_in, sales_out = 1400, 1000
weekly_sales = in_days * sales_in + out_days * sales_out
print("weekly sales", weekly_sales)
assert weekly_sales == 9000
demand = 7 * sales_in
lost = demand - weekly_sales
print(f"weekly demand {demand:,}; lost units {lost}; lost margin at 4/unit {lost*4:,}")
assert (demand, lost, lost * 4) == (9800, 800, 3200)
avg_sales = weekly_sales / 7; avg_dem = demand / 7
print(f"daily sales average {avg_sales:.1f} vs daily demand {avg_dem:.1f}: understated by {1-avg_sales/avg_dem:.1%}")
assert round(avg_sales, 1) == 1285.7 and round(1 - avg_sales / avg_dem, 3) == 0.082
# Lost-sales margin is an upper bound: if 30% of shoppers substitute or come back, the true loss is smaller
for recapture in (0.0, 0.3):
    print(f"recapture {recapture:.0%}: lost margin {lost*(1-recapture)*4:,.0f}")
assert lost * 0.7 * 4 == 2240
# Censoring in a simulation: stock of 1,000 on out days caps what we see; demand varies day to day.
import numpy as np
rng = np.random.default_rng(3)
d = rng.normal(1400, 150, 100_000)
stock = np.where(rng.random(100_000) < 2 / 7, 1000, 1700)   # stock-outs on about 2 days in 7
seen = np.minimum(d, stock)
print(f"simulated: true mean demand {d.mean():.0f}, mean sales {seen.mean():.0f}, mean sales on in-stock-only days {seen[stock==1700].mean():.0f}")
assert d.mean() > seen.mean() + 100
assert seen[stock == 1700].mean() > seen.mean()
# Even the in-stock-day average is biased if some of those days sold out late: ones with high demand got cut
print("in-stock days that still hit the 1,700 cap:", f"{(d[stock==1700] > 1700).mean():.1%}")
assert (d[stock == 1700] > 1700).mean() > 0.01
```

**Output (my run):**
```text
weekly sales 9000
weekly demand 9,800; lost units 800; lost margin at 4/unit 3,200
daily sales average 1285.7 vs daily demand 1400.0: understated by 8.2%
recapture 0%: lost margin 3,200
recapture 30%: lost margin 2,240
simulated: true mean demand 1400, mean sales 1286, mean sales on in-stock-only days 1399
in-stock days that still hit the 1,700 cap: 2.3%
```

**Follow-ups:**
- How does this connect to stock level choice? The newsvendor stock level depends on the demand distribution, not on observed sales.
- What if I have no hourly data? Use stock-out flags by day and train only on days that did not sell out, with a correction for the missing high-demand days.

**Common mistakes:**
- Treating sales as demand.
- Dropping stock-out days silently, which also biases toward low-demand days.
- Taking lost margin as certain.
- Fixing the forecast but never testing higher stock.
