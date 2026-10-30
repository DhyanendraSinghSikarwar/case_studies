### Q23 ⭐⭐ 🟢 A seller cut the price of an item from 20.00 to 18.00 (-10% relative to the old price) and weekly units rose from 1,000 to 1,150 (+15% relative to the old units). Unit cost is 12.00. Compute revenue and gross profit before and after, and explain why revenue rose while profit fell.
**Asked at:** Pricing case-study guides (an Interview Query pricing case-study page, Dataford pricing and price-elasticity question pages for a food distributor and a fleet, 2026 pricing data scientist job postings at companies such as Target and Klook that list elasticity modelling and A/B or geo price tests); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Revenue rose 3.5% (20,000 to 20,700) but gross profit fell 13.7% (8,000 to 6,900), because each unit now earns 6 instead of 8 (25% less) and the 15% extra volume does not make up for that.

**Clarifying questions:**
- Was the price cut the only change that week (promotion, stock, season, competitor move)? A confounded +15% makes the whole calculation wrong.
- Is 12.00 the full variable cost per unit (including shipping, payment fee, returns)? The break-even moves with it.
- Do the extra 150 units come from new buyers or from pulling forward future purchases? Pull-forward means next weeks drop.
- Is this item a traffic driver or a cross-sell anchor? Basket effects can change the answer.
- Is it one week of data? Noise and a launch spike can fake a lift.

**Approach:**
1. Revenue before: 20.00 x 1,000 = 20,000. After: 18.00 x 1,150 = 20,700. Change +700 (+3.5%).
2. Gross profit before: (20 - 12) x 1,000 = 8,000. After: (18 - 12) x 1,150 = 6,900. Change -1,100 (-13.7%).
3. Explain the gap: unit margin fell from 8 to 6 (-25%), volume rose 15%. Profit change is roughly 0.75 x 1.15 = 0.8625, i.e. -13.7%.
4. Give the break-even: at price 18 you need 8,000 / 6 = 1,333 units (+33%) just to keep profit. The cut got only +15%.
5. Use elasticity: the point elasticity is +15% / -10% = -1.5. Revenue rises when |elasticity| is above 1. Profit rises only when |elasticity| is above p / (p - c) = 20 / 8 = 2.5.
6. Recommend: revert, or test a smaller cut, unless the item pulls other purchases or the goal is share, not profit. Check the basket and repeat effects before deciding (Q1 in this part uses the same logic for a price rise).

**Metrics:**
- Revenue = price x units. Gross profit = (price - unit cost) x units. Unit margin = price - unit cost.
- Elasticity = (% change in units) / (% change in price), both against the old base. Here 15% / -10% = -1.5.
- Profit break-even units = old profit / new unit margin = 8,000 / 6.
- Guardrails: gross profit per week (the decision metric), plus basket size, repeat rate, return rate.

**Risks:**
- Looking at revenue only. Revenue is the metric that flatters a price cut.
- Reading one week as a stable elasticity (seasonality, promotion, stock effects).
- Ignoring that a lower price can pull demand forward and leave a dip afterwards.
- Ignoring cross effects: cannibalising a sister product, or the opposite (the item drives other sales).
- A price cut is hard to reverse: customers remember it.

**What the interviewer scores:**
- Strong: computes both before and after numbers and states the break-even volume. Weak: says "revenue went up so it worked".
- Strong: links to margin, the profit rule is |elasticity| greater than p / (p - c). Weak: says elasticity above 1 means profitable.
- Strong: asks whether the lift is incremental and sustained. Weak: assumes the 15% is all caused by the cut.
- Strong: gives a decision and a next test (smaller cut, geo or A/B price test). Weak: stops at the arithmetic.

**Example:** illustrative numbers from the prompt.
- Weak: "Revenue is up 700, so the discount worked."
- Strong: "Revenue is up 700 but profit is down 1,100. At the new price I need 1,333 units to break even and got 1,150. Elasticity is -1.5, below the 2.5 that a margin of 8 on a price of 20 requires. I would revert unless the item drives basket value."
- In my run (code below): even with a unit cost of 8 instead of 12 the need is 1,200 units and 1,150 still falls short (profit -500).

**Code:**
```python
# Q23: price cut 20 -> 18, units 1,000 -> 1,150, unit cost 12 (illustrative numbers)
p0, p1, u0, u1, c = 20.00, 18.00, 1000, 1150, 12.00
rev0, rev1 = p0 * u0, p1 * u1
gp0, gp1 = (p0 - c) * u0, (p1 - c) * u1
print("revenue", rev0, "->", rev1, "change", rev1 - rev0, f"({(rev1/rev0-1)*100:.1f}%)")
print("gross profit", gp0, "->", gp1, "change", gp1 - gp0, f"({(gp1/gp0-1)*100:.1f}%)")
assert (rev0, rev1, gp0, gp1) == (20000.0, 20700.0, 8000.0, 6900.0)

# unit margin and the units needed just to stand still on profit
m0, m1 = p0 - c, p1 - c
be_units = gp0 / m1
print("unit margin", m0, "->", m1, f"({(m1/m0-1)*100:.0f}%); units needed to keep profit = {be_units:.1f} (+{(be_units/u0-1)*100:.1f}%)")
assert m0 == 8 and m1 == 6 and abs(be_units - 1333.33) < 0.01

# elasticity (point, using the old base) and the profit threshold p/(p-c)
e = ((u1 - u0) / u0) / ((p1 - p0) / p0)
thr = p0 / (p0 - c)
print(f"elasticity {e:.2f}; revenue rises if |e|>1, profit rises only if |e| > p/(p-c) = {thr:.2f}")
assert abs(e + 1.5) < 1e-9 and abs(thr - 2.5) < 1e-9 and abs(e) > 1 and abs(e) < thr

# sensitivity: what unit volume would make the cut profitable, and what if cost were 8?
for cost in (12.0, 8.0):
    need = (p0 - cost) * u0 / (p1 - cost)
    print(f"cost {cost}: units needed at price 18 to match old profit = {need:.0f}; actual 1,150 -> profit change {(p1-cost)*u1-(p0-cost)*u0:+.0f}")
assert (p1 - 8) * u1 - (p0 - 8) * u0 == 11500 - 12000
```

**Output (my run):**
```text
revenue 20000.0 -> 20700.0 change 700.0 (3.5%)
gross profit 8000.0 -> 6900.0 change -1100.0 (-13.7%)
unit margin 8.0 -> 6.0 (-25%); units needed to keep profit = 1333.3 (+33.3%)
elasticity -1.50; revenue rises if |e|>1, profit rises only if |e| > p/(p-c) = 2.50
cost 12.0: units needed at price 18 to match old profit = 1333; actual 1,150 -> profit change -1100
cost 8.0: units needed at price 18 to match old profit = 1200; actual 1,150 -> profit change -500
```

**Follow-ups:**
- *What price change would you try next?* A smaller cut, tested in a randomised price test. Required lift scales with the margin share lost: a 5% cut on this item (margin 8 to 7) needs about 14.3% more units to hold profit (8,000 / 7 = 1,143).
- *When is a loss-making discount still right?* When the item drives other purchases, to clear stock before it expires, or when the goal is acquisition with measured repeat value. Say the goal first.
- *Is revenue up always a good sign?* No. For elasticity between 1 and p / (p - c), a cut raises revenue and cuts profit. That is exactly this case.

**Common mistakes:**
- Quoting revenue growth and stopping.
- Computing the percentage change of margin against the wrong base.
- Saying "elastic, so the cut is good" without checking the margin threshold.
- Treating one week as the true elasticity.

### Q24 ⭐⭐ 🟢 A streaming plan has revenue of 10 per subscriber a month at a 70% gross margin, and 5% of active subscribers churn each month. CAC is 60. Compute LTV with margin divided by churn, the LTV-to-CAC ratio and the simple payback in months, and explain why the formula can mislead when churn falls with tenure.
**Asked at:** Lifetime-value and CAC material (a Dataford 'calculate customer lifetime value' product-growth-analyst page, Hacking the Case Interview, Road to Offer and MBB Prep pages on CLV and CAC, Count.co and FourWeekMBA CAC-payback pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Margin per month is 7, LTV is 7 / 0.05 = 140, LTV to CAC is 140 / 60 = 2.33, and simple payback is 60 / 7 = 8.6 months; the formula assumes one constant churn rate, so it misleads when churn falls with tenure.

**Clarifying questions:**
- Is the 5% churn of the whole active base, or of a new cohort month by month? They are different numbers when churn changes with tenure.
- Is the 70% margin after content, payment and support costs? LTV uses contribution, not revenue.
- Does CAC include all acquisition cost (paid, promotions, free trials)? An understated CAC flatters the ratio.
- Do we discount cash flows, and what is the planning horizon? Many teams cap LTV at 2 to 3 years.
- Do subscribers upgrade, pause or come back? Reactivation breaks the "churn is final" idea.

**Approach:**
1. Contribution per subscriber-month = 10 x 0.70 = 7.00.
2. Expected lifetime = 1 / churn = 1 / 0.05 = 20 months. LTV = 7 / 0.05 = 140.
3. LTV / CAC = 140 / 60 = 2.33. Simple payback = 60 / 7 = 8.57 months.
4. Check payback honestly: with 5% monthly churn, the average acquired subscriber's cumulative margin reaches 60 only in month 11 (60.4), not month 9, because some leave before paying back.
5. Say why the formula can mislead: it needs a constant churn. If churn is high in the first months and low later, the base-wide churn mixes old, stable people with new, risky ones. Plugging first-month churn gives too small an LTV; plugging late-tenure churn gives too large a one; the right number is the cohort's own average (churn events divided by subscriber-months).
6. Fix: use cohort survival curves, cap the horizon, discount, and report payback on a cohort basis.

**Metrics:**
- LTV (simple) = monthly contribution / monthly churn. Numerator: revenue x gross margin. Denominator: churned subscribers / active subscribers at the start of the month.
- LTV / CAC. CAC = acquisition spend / new paying subscribers in the same period.
- Payback (simple) = CAC / monthly contribution. Payback (cohort) = first month in which cumulative contribution per acquired subscriber is at least CAC.
- Guardrails: cohort retention curves by acquisition channel, discounted LTV, share of LTV earned after month 24.

**Risks:**
- Constant churn assumption (the point of the question).
- Averaging across channels: cheap channels often bring cheaper, faster-churning customers.
- A small churn estimate makes LTV explode: 3% gives 233, 4% gives 175. The ratio is very sensitive to a number that is hard to measure.
- Using revenue instead of margin, or ignoring discounting and cost of capital.
- Survivorship: the base you can see is the one that stayed.

**What the interviewer scores:**
- Strong: gets 140, 2.33, 8.6 and notes that churn-adjusted payback is later (month 11). Weak: stops at 140.
- Strong: explains tenure-dependent churn with a number. Weak: says "churn is not constant" and no more.
- Strong: proposes cohort survival curves and discounting. Weak: proposes a more complex formula without data.
- Strong: asks which churn the 5% is. Weak: assumes it is the new-cohort churn.

**Example:** illustrative numbers.
- Weak: "LTV is 140, CAC is 60, great, scale spend."
- Strong: "2.33 is a rough first read. On a cohort basis payback is month 11, not 8.6. If churn is 12% for three months and 3% afterwards, true LTV is 177.6, but the formula with first-month churn says 58 and with late churn says 233. I would build the cohort retention curve before setting a spend limit."
- In my run (below): cumulative margin per acquired subscriber crosses 60 in month 11 (60.4); with 1% monthly discounting the constant-churn LTV falls from 140 to 117.8.

**Code:**
```python
# Q24: streaming LTV and CAC payback (illustrative)
import numpy as np
rev, gm, churn, cac = 10.0, 0.70, 0.05, 60.0
margin = rev * gm                       # 7.0 per subscriber-month
ltv = margin / churn
print(f"margin/month {margin:.2f}  LTV (margin/churn) {ltv:.1f}  LTV/CAC {ltv/cac:.2f}  simple payback {cac/margin:.2f} months  mean lifetime {1/churn:.0f} months")
assert abs(margin - 7) < 1e-9 and abs(ltv - 140) < 1e-9 and abs(ltv / cac - 2.3333) < 1e-3 and abs(cac / margin - 8.5714) < 1e-3

# payback WITH churn: cumulative margin per acquired subscriber, month m collects margin * survival
months = np.arange(1, 400)
surv = (1 - churn) ** (months - 1)      # first month paid in full
cum = np.cumsum(margin * surv)
pay = int(months[np.argmax(cum >= cac)])
print("payback with 5% constant churn: month", pay, f"(cumulative margin {cum[pay-1]:.1f})")
assert pay == 11 and cum[pay - 2] < cac <= cum[pay - 1]
assert abs(cum[-1] - ltv) < 1e-6        # the sum of margin x survival converges to margin/churn

# churn that falls with tenure: 12% in months 1-3, 3% afterwards
def cohort_ltv(hazards, n=2000):
    s, tot = 1.0, 0.0
    for m in range(1, n + 1):
        tot += margin * s
        s *= 1 - hazards(m)
    return tot
h = lambda m: 0.12 if m <= 3 else 0.03
true_ltv = cohort_ltv(h)
# the cohort-average churn = churn events / subscriber-months, i.e. weighted by survival
s, base, w = 1.0, [], []
for m in range(1, 3000):
    base.append(h(m)); w.append(s); s *= 1 - h(m)
blend = float(np.average(base, weights=w))
print(f"hazard 12% for 3 months then 3%: true cohort LTV {true_ltv:.1f}")
for name, c in (("first-month churn 12%", 0.12), ("late-tenure churn 3%", 0.03), (f"cohort-average churn {blend:.4f}", blend)):
    print(f"  formula with {name}: {margin/c:.1f}")
assert abs(margin / blend - true_ltv) < 0.01
assert margin / 0.12 < true_ltv < margin / 0.03
assert abs(true_ltv - (margin * (1 + .88 + .88**2) + margin * .88**3 / 0.03)) < 1e-6

# discounting at 1% a month (a monthly rate of about 12.7% a year) with the plain 5% churn
d = 0.01
ltv_d = margin * (1 + d) / (churn + d)      # first month undiscounted
print(f"with 1%/month discounting, constant 5% churn: LTV {ltv_d:.1f}")
assert 110 < ltv_d < 120
```

**Output (my run):**
```text
margin/month 7.00  LTV (margin/churn) 140.0  LTV/CAC 2.33  simple payback 8.57 months  mean lifetime 20 months
payback with 5% constant churn: month 11 (cumulative margin 60.4)
hazard 12% for 3 months then 3%: true cohort LTV 177.6
  formula with first-month churn 12%: 58.3
  formula with late-tenure churn 3%: 233.3
  formula with cohort-average churn 0.0394: 177.6
with 1%/month discounting, constant 5% churn: LTV 117.8
```

**Follow-ups:**
- *Which churn would you plug in for a new cohort?* The cohort's average churn so far, or better the full survival curve; not the base-wide number, which is weighted towards old subscribers.
- *Is 2.33 good?* Depends on the company's own target and cash position; ask for it rather than quote a rule of thumb. Compare channels instead.
- *How would you shorten payback?* Raise margin (cost to serve, pricing), cut CAC, or improve early retention. Early churn is the lever that matters most for payback.

**Common mistakes:**
- Using revenue, not margin, in the numerator.
- Reporting simple payback as if nobody churned.
- Applying one blended churn to every channel and tenure.
- Quoting LTV to CAC with no horizon, no discounting and no uncertainty.

### Q25 ⭐⭐ 🟢 A recommender raised click-through on its carousel to 8% from 5% of impressions (3 points absolute). A 4-week holdout shows, for the 2,000,000 users the model serves, revenue per user of 40.0 with the model against 39.0 with a popularity list (+2.6% relative to the popularity list), at a 30% margin. The model and its team cost 250,000 for the 4 weeks. Compute the incremental margin and net value, and explain why the click-through lift overstates the value.
**Asked at:** Recommender and personalisation business-value material (a Jannach and Jugovac arXiv survey on the business value of recommenders, a Smart Insights personalisation case, vendor case studies from Blast Analytics and Recolize that report self-claimed ROI); vendor numbers are upper bounds; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The model adds about 1.0 of revenue per user, which is 600,000 of incremental margin over the 4 weeks and 350,000 net of the 250,000 cost; click-through up 60% relative overstates it because most clicks would have happened anyway or do not become purchases.

**Clarifying questions:**
- Was the holdout randomised at user level, and were both arms the same size? Without that, +1.0 is not causal.
- Does the +1.0 per user hold for all 2,000,000 users the model serves? I assume yes; a lift measured on a sample may not carry over to every user.
- Is "revenue per user" over the 4 weeks, and is it net of returns and cancellations? Gross revenue can include later refunds.
- Is the 30% margin the contribution on revenue after variable costs? It sets the break-even.
- What happens to the lift after the novelty fades? A 4-week test can overstate the long-run effect.

**Approach:**
1. Start from the right metric: revenue (then margin) per randomised user, intention to treat. Not clicks.
2. Lift: 40.0 - 39.0 = +1.0 per user. Relative to the popularity list this is 1 / 39 = +2.56%.
3. Incremental revenue = 1.0 x 2,000,000 = 2,000,000. Incremental margin = 2,000,000 x 0.30 = 600,000.
4. Net value = 600,000 - 250,000 = 350,000 for the 4 weeks.
5. Break-even: the model needs only 250,000 / (2,000,000 x 0.30) = 0.417 of revenue per user, a 1.07% lift.
6. Check noise: with no standard deviation given, state an assumption. If the standard deviation of revenue per user is 60 and the two arms have 1,000,000 users each, the standard error is about 0.085 and +1.0 is about 12 standard errors. Revenue data are skewed; use a bootstrap or CUPED in practice.
7. Explain the overstatement: CTR counts clicks the popularity list would also have earned, clicks that shift traffic from other page areas, and clicks that do not buy. The relative revenue lift (2.56%) is only about 4% of the relative click lift (60%).

**Metrics:**
- Primary: incremental margin per user = (revenue per user, treatment - control) x margin rate. Denominator: users randomised, not users who clicked.
- Net value = incremental margin x users - cost of model and team. Report per period and annualised separately.
- Guardrails: return rate, other-category sales (cannibalisation), page latency, diversity, long-term retention.

**Risks:**
- Comparing to the wrong baseline: "no recommender" versus "popularity list" give different lifts; here it is the popularity list, a strong baseline.
- Novelty effect in 4 weeks; the lift may decay.
- Measuring clicks or CTR on exposed users only (selection bias).
- Including only the model's cost of the test period, not its ongoing cost.
- Interference between users (inventory, popularity feedback loops).

**What the interviewer scores:**
- Strong: computes 600,000 and 350,000 and the 0.417 break-even. Weak: celebrates "+60% CTR".
- Strong: says why clicks overstate value (baseline clicks, cannibalisation, non-buying clicks). Weak: "CTR is a vanity metric" with no mechanism.
- Strong: uses the right base (39.0, the popularity list) and asks about the sample. Weak: divides by the wrong base or repeats numbers uncritically.
- Strong: asks for the interval and the horizon. Weak: treats a point estimate as certain.

**Example:** illustrative numbers.
- Weak: "CTR went from 5% to 8%, a 60% improvement, so the recommender is a big win."
- Strong: "Revenue per user is up 1.0, which is 2.6%. At a 30% margin that is 600,000 for the test period. After the 250,000 cost, 350,000. Break-even is a 0.42 lift per user, so we have a margin of safety, if the interval holds. I would keep a small holdout running to see whether it decays."
- In my run (below): the lift passes break-even by more than 3 standard errors even with an assumed sd of 120.

**Code:**
```python
# Q25: recommender, CTR lift vs money (illustrative)
ctr0, ctr1 = 0.05, 0.08
print(f"CTR {ctr0:.0%} -> {ctr1:.0%}: +{(ctr1-ctr0)*100:.0f} points absolute, +{(ctr1/ctr0-1)*100:.0f}% relative")
assert abs((ctr1 - ctr0) - 0.03) < 1e-12 and abs(ctr1 / ctr0 - 1.6) < 1e-12

users, rpu_m, rpu_p, margin, cost = 2_000_000, 40.0, 39.0, 0.30, 250_000
rel = rpu_m / rpu_p - 1
inc_rev = (rpu_m - rpu_p) * users
inc_margin = inc_rev * margin
net = inc_margin - cost
print(f"revenue per user +{rpu_m-rpu_p:.1f} = +{rel*100:.2f}% relative to 39.0 (base is 39.0, the popularity list)")
print(f"incremental revenue {inc_rev:,.0f}; incremental margin {inc_margin:,.0f}; cost {cost:,}; net value {net:,.0f}")
assert abs(rel - 0.02564) < 1e-4 and inc_rev == 2_000_000 and inc_margin == 600_000 and net == 350_000

# break-even revenue lift per user, and noise check with an ASSUMED standard deviation
be_rpu = cost / (users * margin)
print(f"break-even lift in revenue per user = {be_rpu:.3f} ({be_rpu/rpu_p*100:.2f}% of 39.0)")
assert abs(be_rpu - 0.41667) < 1e-4
import math
for sd in (30, 60, 120):
    n_arm = users / 2           # if the 2,000,000 users were split evenly between the two arms
    se = sd * math.sqrt(2 / n_arm)
    print(f"assumed sd {sd}: SE of the difference {se:.3f}; observed 1.0 is {1.0/se:.1f} SEs; break-even 0.417 is {(1.0-be_rpu)/se:.1f} SEs below it")
assert 1.0 / (60 * math.sqrt(2 / 1_000_000)) > 10

# the click lift is 60% relative; the revenue lift is 2.56% relative
print(f"revenue lift / click lift (both relative) = {rel/(ctr1/ctr0-1):.3f}")
assert abs(rel / 0.6 - 0.0427) < 1e-3
```

**Output (my run):**
```text
CTR 5% -> 8%: +3 points absolute, +60% relative
revenue per user +1.0 = +2.56% relative to 39.0 (base is 39.0, the popularity list)
incremental revenue 2,000,000; incremental margin 600,000; cost 250,000; net value 350,000
break-even lift in revenue per user = 0.417 (1.07% of 39.0)
assumed sd 30: SE of the difference 0.042; observed 1.0 is 23.6 SEs; break-even 0.417 is 13.7 SEs below it
assumed sd 60: SE of the difference 0.085; observed 1.0 is 11.8 SEs; break-even 0.417 is 6.9 SEs below it
assumed sd 120: SE of the difference 0.170; observed 1.0 is 5.9 SEs; break-even 0.417 is 3.4 SEs below it
revenue lift / click lift (both relative) = 0.043
```

**Follow-ups:**
- *Why not just report CTR?* It is a diagnostic: it tells you the model changes behaviour, not that behaviour is worth money.
- *The lift decays in weeks 5 to 8. What now?* Re-run the numbers with the decayed lift. At a long-run lift of 0.417 per user the net value is exactly zero for that period.
- *What would an interleaving test add?* Faster sensitivity to ranking quality, but it does not give revenue or incrementality; the holdout does.

**Common mistakes:**
- Taking the click lift as the business lift.
- Dividing the revenue gain by the wrong base (40 instead of 39).
- Netting the cost of the team for 4 weeks but ignoring ongoing serving cost.
- Reading a point estimate with no interval.

### Q26 ⭐⭐ 🟢 An LLM feature uses 3,000 input tokens and 500 output tokens per query, priced at 2.00 per million input tokens and 10.00 per million output tokens, plus 0.001 of retrieval cost. Subscribers pay 3.00 a month with a 3% payment fee. Light users (95% of subscribers) send 100 queries a month and heavy users (5%) send 1,000. Compute cost per query, margin per light and heavy subscriber and the blended margin, then suggest two controls.
**Asked at:** AI-era support and GenAI cost material (2026 vendor and practitioner pages from Lorikeet, Twig, Voiceflow, aitimejournal, CloudZero, nOps, tianpan.co and a Gartner press-release headline on inference costs); mostly vendor-sourced, an emerging interview theme rather than a confirmed bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** A query costs 0.012, so a light user (100 queries) earns 1.71 a month, a heavy user (1,000 queries) loses 9.09, and the blended margin is 1.17; the 5% heavy users drive 34% of the cost, so I would cap or price them and cut tokens per query.

**Clarifying questions:**
- Is the 0.001 retrieval cost per query, and are there other costs (embedding, storage, moderation, human review)? Missing costs flatter the margin.
- Are input tokens the same every time, or does context grow in a conversation? Long chats make later queries dearer.
- Is the 3.00 the whole subscription, or is the AI feature one part of a bundle? It decides which margin we judge.
- Are heavy users heavy by choice, or by automation (scripts, resale)? That points to abuse controls or to a higher tier.
- Can we use a cheaper model or caching for some queries without hurting quality? That is the strongest cost lever.

**Approach:**
1. Cost per query = 3,000 x 2.00 / 1e6 + 500 x 10.00 / 1e6 + 0.001 = 0.006 + 0.005 + 0.001 = 0.012.
2. Net revenue per subscriber = 3.00 x (1 - 0.03) = 2.91.
3. Light: 2.91 - 100 x 0.012 = 1.71. Heavy: 2.91 - 1,000 x 0.012 = -9.09.
4. Blended = 0.95 x 1.71 + 0.05 x (-9.09) = 1.6245 - 0.4545 = 1.17.
5. Break-even: 2.91 / 0.012 = 242.5 queries a month. Any subscriber above that loses money.
6. Where the cost sits: per average subscriber the light group costs 1.14 and the heavy 0.60, so 5% of users cause 34.5% of the cost.
7. Two controls: (a) a usage cap, rate limit or paid overage: a cap of 200 queries makes a heavy user worth 0.51 and lifts the blend to 1.65; (b) cut cost per query: shorter context, retrieval of fewer chunks, a cache, or a smaller model for easy queries. Halving the input tokens takes the cost to 0.009 and the blend to 1.605 without touching the heavy users.
8. Also set per-user cost monitoring and alerts, and a heavier tier.

**Metrics:**
- Cost per query = (input tokens x input price + output tokens x output price) + retrieval and other per-query cost.
- Margin per subscriber = price x (1 - payment fee) - queries x cost per query. Blended margin is weighted by the share of subscribers in each group.
- Guardrails: share of subscribers with negative margin, p95 queries per user, cost per active user by tier, satisfaction after a cap (complaints, churn).

**Risks:**
- Using a mean usage figure (145 queries) hides the tail; the tail is the problem.
- Token counts may grow (long chats, larger documents), so cost per query is not constant.
- A hard cap can hurt your best customers and cause churn. Test caps on a small share first.
- Prices change; keep cost per query as a configurable number, not a hard-coded one.
- Heavy users may be the most engaged and most valuable ones; do not assume they are bad.

**What the interviewer scores:**
- Strong: gets 0.012, 1.71, -9.09, 1.17 and the 242.5 break-even. Weak: stops at the average.
- Strong: points at the tail, not the mean. Weak: suggests only "use a cheaper model".
- Strong: two concrete controls with a number for each. Weak: vague "limit usage".
- Strong: mentions the customer-impact guardrail. Weak: ignores the churn risk of a cap.

**Example:** illustrative numbers.
- Weak: "Average usage is 145 queries, cost 1.74, so we are fine."
- Strong: "The average hides it. The break-even is 242 queries; 5% of users sit at 1,000 and lose 9.09 each. A cap at 200 or an overage price fixes that, and cutting context from 3,000 to 1,500 tokens saves a quarter of the cost."
- In my run (below): cap 200 gives blended margin 1.65; halving input tokens gives 1.605.

**Code:**
```python
# Q26: LLM feature unit economics (illustrative prices)
tin, tout = 3000, 500
p_in, p_out = 2.00 / 1e6, 10.00 / 1e6
retr = 0.001
cpq = tin * p_in + tout * p_out + retr
print(f"cost per query: input {tin*p_in:.4f} + output {tout*p_out:.4f} + retrieval {retr:.4f} = {cpq:.4f}")
assert abs(cpq - 0.012) < 1e-12

price, fee = 3.00, 0.03
net_rev = price * (1 - fee)
light_q, heavy_q, f_heavy = 100, 1000, 0.05
m_light = net_rev - light_q * cpq
m_heavy = net_rev - heavy_q * cpq
blend = (1 - f_heavy) * m_light + f_heavy * m_heavy
print(f"net revenue per subscriber {net_rev:.2f}; light margin {m_light:.2f}; heavy margin {m_heavy:.2f}; blended {blend:.4f}")
assert abs(net_rev - 2.91) < 1e-9 and abs(m_light - 1.71) < 1e-9 and abs(m_heavy + 9.09) < 1e-9 and abs(blend - 1.17) < 1e-9

be_q = net_rev / cpq
print(f"break-even queries per subscriber per month: {be_q:.1f}")
assert abs(be_q - 242.5) < 1e-9

# share of cost from the 5% heavy users
cost_light = (1 - f_heavy) * light_q * cpq
cost_heavy = f_heavy * heavy_q * cpq
print(f"cost per average subscriber: light {cost_light:.3f}, heavy {cost_heavy:.3f}; heavy share {cost_heavy/(cost_light+cost_heavy)*100:.1f}% of cost from 5% of users")
assert abs(cost_heavy / (cost_light + cost_heavy) - 0.3448) < 1e-3

# control 1: cap at 200 queries a month (heavy users above 200 are throttled or pay overage)
cap = 200
m_heavy_cap = net_rev - cap * cpq
blend_cap = (1 - f_heavy) * m_light + f_heavy * m_heavy_cap
print(f"cap 200: heavy margin {m_heavy_cap:.2f}; blended {blend_cap:.4f}")
assert abs(m_heavy_cap - 0.51) < 1e-9 and abs(blend_cap - 1.65) < 1e-9
# control 2: cheaper path (here: shorter context, 3,000 -> 1,500 input tokens)
cpq2 = 1500 * p_in + tout * p_out + retr
blend2 = net_rev - ((1 - f_heavy) * light_q + f_heavy * heavy_q) * cpq2
print(f"shorter context: cost per query {cpq2:.4f}; blended margin without a cap {blend2:.4f}")
assert abs(cpq2 - 0.009) < 1e-12 and abs(blend2 - 1.605) < 1e-9
# follow-up: all token prices halve (retrieval cost unchanged)
cpq3 = tin * p_in / 2 + tout * p_out / 2 + retr
print(f"token prices halved: cost per query {cpq3:.4f}; heavy user cost {heavy_q*cpq3:.2f} vs net revenue {net_rev:.2f}")
assert abs(cpq3 - 0.0065) < 1e-12 and heavy_q * cpq3 > net_rev
```

**Output (my run):**
```text
cost per query: input 0.0060 + output 0.0050 + retrieval 0.0010 = 0.0120
net revenue per subscriber 2.91; light margin 1.71; heavy margin -9.09; blended 1.1700
break-even queries per subscriber per month: 242.5
cost per average subscriber: light 1.140, heavy 0.600; heavy share 34.5% of cost from 5% of users
cap 200: heavy margin 0.51; blended 1.6500
shorter context: cost per query 0.0090; blended margin without a cap 1.6050
token prices halved: cost per query 0.0065; heavy user cost 6.50 vs net revenue 2.91
```

**Follow-ups:**
- *What would you do instead of a hard cap?* A soft limit with a slower model after the quota, or an add-on pack, so heavy use is paid for.
- *How would you pick the cap?* From the usage distribution and the break-even (242 queries); test caps at 200, 300 and 500 on small groups and watch churn and complaints.
- *If the price of tokens halves?* Cost per query falls to 0.0065 (retrieval is fixed). A heavy user still costs 1,000 x 0.0065 = 6.50, more than the 2.91 net revenue.

**Common mistakes:**
- Forgetting the payment fee, or applying it to cost instead of revenue.
- Mixing up price per million input and output tokens.
- Judging a feature on average margin while the tail is negative.
- Hard-coding a price that will change.

### Q27 ⭐⭐ 🟡 At the Friday dinner peak a delivery marketplace gets 1,200 order requests an hour and its couriers can complete 1,000 an hour (83% of requests filled). A courier incentive of 1.00 per delivery raises capacity by 10% relative to 1,000, to 1,100, but is paid on all 1,100 deliveries, and each extra completed order earns 2.50 of margin before the incentive. Compute the incentive cost and the extra margin, and propose a cheaper design.
**Asked at:** Marketplace and take-rate material (an inpractise take-rate course page, a Codemia Thumbtack data scientist guide describing a marketplace case round, ibinterviewquestions and hackingthecaseinterview marketplace and supply-demand pages); general marketplace guides, nothing specific to Uber, DoorDash or Swiggy loops; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The flat 1.00 incentive costs 1,100 an hour to earn 250 of extra margin, a loss of 850 an hour, because it pays 1,000 deliveries that would have happened anyway; pay only for the extra capacity, or target the peak.

**Clarifying questions:**
- Where does the "capacity +10%" come from: a test, a model or a guess? It is the key number in the case.
- Is capacity limited by courier hours online, by acceptance of offers, or by distance and zones? The right lever depends on it.
- What happens to the unfilled 200 orders an hour: cancelled, delayed, or served at a worse experience? That sets what an extra order is worth.
- Is the 2.50 margin per extra order after refunds, support and the courier's base pay?
- Can we raise customer fees or use a surge instead of paying couriers? That is the other side of the market.

**Approach:**
1. Fill rate now = 1,000 / 1,200 = 83.3%. With the incentive: 1,100 / 1,200 = 91.7%.
2. Incentive cost = 1.00 x 1,100 = 1,100 an hour (paid on all deliveries).
3. Extra margin = (1,100 - 1,000) x 2.50 = 250 an hour.
4. Net = 250 - 1,100 = -850 an hour. The incentive costs 11.00 per extra order against a margin of 2.50.
5. Break-even flat rate: 250 / 1,100 = 0.23 per delivery, if the 10% capacity response did not shrink.
6. Cheaper design: pay a bonus only on deliveries above a threshold (the 1,000 baseline, per courier or per zone and hour). If the same 100 extra orders appear, cost is 1.00 x 100 = 100 and net is +150 an hour. The rate can go up to 2.50 per extra delivery and still break even.
7. Other options: peak-hour surge on the customer side (moves demand, funds courier pay), guaranteed minimum for logging in at peak, targeted zones where the gap is largest. Test any design with a switchback or a zone-level experiment before rolling out.
8. Check the capacity claim: do couriers respond to threshold bonuses as they do to flat ones? That is the thing to test.

**Metrics:**
- Fill rate = orders completed / order requests, per hour and zone.
- Incentive cost per incremental delivery = total incentive paid / (deliveries with incentive - deliveries without).
- Net value per hour = incremental deliveries x margin per delivery - incentive paid.
- Guardrails: courier supply hours, delivery time, cancellations, courier earnings and retention, customer re-order rate.

**Risks:**
- A paid-on-everything incentive is mostly a transfer to couriers (90.9% of the spend goes to deliveries that would have happened).
- Threshold bonuses can be gamed (timing deliveries around the cut-off) and may pay people who would have exceeded the threshold anyway.
- Capacity may be limited by zones or distance, not by pay, so the 10% may not appear.
- Marketplace feedback: a better fill rate may lift demand next week, which is an upside not in the numbers; a cut in incentive may lose couriers.
- Measuring with before-and-after instead of a controlled test (Fridays differ).

**What the interviewer scores:**
- Strong: gets -850 and spots that the incentive is paid on the full 1,100. Weak: compares only 100 x 2.50 with 100 x 1.00 and says it pays off.
- Strong: proposes a design that pays on the margin (threshold, peak-only, targeted) with a number. Weak: "reduce the incentive".
- Strong: questions where the 10% came from and proposes a test. Weak: accepts it.
- Strong: mentions both sides of the market (surge, fees). Weak: only courier pay.

**Example:** illustrative numbers.
- Weak: "Each extra order earns 2.50 and costs 1.00, so the incentive is profitable."
- Strong: "The 1.00 is paid on 1,100 deliveries, not 100. That is 1,100 for 250 of margin, minus 850 an hour. I would pay only above the 1,000 baseline: 100 for the same 250, +150 an hour, if couriers respond that way. I would test it zone by zone."
- In my run (below): even if the threshold bonus draws only 40 extra orders, the net is still +60 an hour at a bonus of 1.00.

**Code:**
```python
# Q27: courier incentive at the dinner peak (illustrative)
req, cap0 = 1200, 1000
cap1 = cap0 * 1.10
print(f"fill rate {cap0/req:.1%} -> {cap1/req:.1%}; capacity {cap0} -> {cap1:.0f}")
assert abs(cap0 / req - 0.8333) < 1e-3 and cap1 == 1100

inc, m = 1.00, 2.50
cost_all = inc * cap1
extra_orders = cap1 - cap0
extra_margin = extra_orders * m
print(f"uniform incentive: cost {cost_all:.0f}/h, extra margin {extra_margin:.0f}/h, net {extra_margin-cost_all:+.0f}/h; cost per extra order {cost_all/extra_orders:.2f} vs margin {m}")
assert cost_all == 1100 and extra_margin == 250 and extra_margin - cost_all == -850 and cost_all / extra_orders == 11.0

# break-even uniform incentive and a threshold design (pay only above the 1,000 baseline)
print(f"break-even uniform incentive per delivery: {extra_margin/cap1:.3f}")
assert abs(extra_margin / cap1 - 0.2273) < 1e-3
cost_thr = inc * extra_orders
print(f"threshold design (pay 1.00 only on deliveries above 1,000): cost {cost_thr:.0f}/h, net {extra_margin-cost_thr:+.0f}/h; max rate that breaks even {m:.2f}")
assert cost_thr == 100 and extra_margin - cost_thr == 150

# if the threshold design only draws half the capacity response (50 extra orders), at the same 1.00
for resp in (100, 50, 40):
    print(f"  extra orders {resp}: margin {resp*m:.0f}, cost {inc*resp:.0f}, net {resp*(m-inc):+.0f}")
assert 100 * (m - inc) == 150 and 40 * (m - inc) == 60
# the 1.00 is paid on 1,100 in the uniform case: what share of the spend is a windfall to riders who would have worked anyway?
print(f"share of uniform spend paid on deliveries that would have happened anyway: {cap0/cap1:.1%}")
assert abs(cap0 / cap1 - 0.909) < 1e-3
```

**Output (my run):**
```text
fill rate 83.3% -> 91.7%; capacity 1000 -> 1100
uniform incentive: cost 1100/h, extra margin 250/h, net -850/h; cost per extra order 11.00 vs margin 2.5
break-even uniform incentive per delivery: 0.227
threshold design (pay 1.00 only on deliveries above 1,000): cost 100/h, net +150/h; max rate that breaks even 2.50
  extra orders 100: margin 250, cost 100, net +150
  extra orders 50: margin 125, cost 50, net +75
  extra orders 40: margin 100, cost 40, net +60
share of uniform spend paid on deliveries that would have happened anyway: 90.9%
```

**Follow-ups:**
- *How would you measure the real capacity response?* Randomise incentive designs by zone and hour block (switchbacks), keeping a control; measure completed deliveries per hour and fill rate.
- *What if couriers game the threshold?* Use a rolling or per-courier baseline from past behaviour, or pay for peak-slot availability instead of deliveries.
- *What does a surge price do?* It trims demand (fewer low-value orders) and funds the courier side; it is an option when the 1,200 requests include orders that would walk away at a higher fee.

**Common mistakes:**
- Costing the incentive on the extra orders only, for the flat design.
- Ignoring that the 10% capacity gain is an assumption.
- Treating the fill rate as the objective instead of contribution.
- Ignoring courier retention and fairness effects of changing pay.

### Q28 ⭐⭐ 🟡 A marketplace has 100 million of annual GMV, of which the top sellers contribute 40 million and all others 60 million, at a 12% take rate. A rise to 15% (3 points absolute) is projected to cut top-seller GMV by 25% relative to their 40 million and other sellers' GMV by 3% relative to their 60 million. Compute revenue before and after, and say what the projection leaves out about the top sellers.
**Asked at:** Marketplace and take-rate material (an inpractise take-rate course page, a Codemia Thumbtack data scientist guide describing a marketplace case round, ibinterviewquestions and hackingthecaseinterview marketplace and supply-demand pages); general marketplace guides, nothing specific to Uber, DoorDash or Swiggy loops; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** On the projection, revenue goes from 12.00 million to 13.23 million (+10.3%), but the projection says nothing about the top sellers' behaviour, which can turn it negative: a top-seller loss of 45% or a knock-on loss among other sellers would wipe the gain out.

**Clarifying questions:**
- Where do the -25% and -3% come from: a test, a survey, a model? Top sellers are few, so their reaction is the least predictable number.
- Is the rise for everyone at once or for new sellers only? The response differs.
- Can top sellers move off-platform (own site, rival marketplace, direct deals)? That is the leakage risk.
- Do buyers come for particular top sellers? If so, losing them hurts other sellers' sales too.
- Is the 15% before or after seller incentives, fees and refunds? Net take rate is what matters.

**Approach:**
1. Before: 12% x (40 + 60) = 12.00 million.
2. After: top sellers 40 x 0.75 = 30.0; others 60 x 0.97 = 58.2; GMV = 88.2 million (-11.8%). Revenue = 15% x 88.2 = 13.23 million (+10.25%).
3. Say what is left out: the -25% is a single guess for a few large, well-informed sellers who can negotiate, multi-home or leave. They are also the ones who bring buyers.
4. Show the sensitivity: revenue is flat if top-seller GMV falls 45.5% (others -3%), or if everybody's GMV falls 20%. If top sellers fall 60%, revenue drops 7.3%.
5. Add the knock-on: if buyers who came for top sellers leave and other sellers lose 15% instead of 3%, revenue is 12.15 million, a gain of only 1.2%.
6. Recommend: not a blanket rise. Raise gradually, test by segment or region, keep a negotiated rate or a tiered rate for top sellers, and watch GMV, active sellers and buyer retention as guardrails. Report the result as a range.

**Metrics:**
- Take rate = marketplace revenue / GMV. Revenue = take rate x GMV after seller response.
- Seller response = change in GMV by seller segment against a control (not a before-and-after).
- Guardrails: active sellers, new-seller listings, buyer conversion and retention, share of GMV leaking off platform, seller-support complaints, and long-run GMV (not only the first month).

**Risks:**
- Treating the segment responses as fixed numbers when they are guesses with a wide range.
- Short-run measurement: seller exit can take months (they set up elsewhere first).
- Two-sided effects: fewer top sellers means fewer reasons for buyers to come, which also lowers other sellers' GMV.
- Concentration: the top sellers are 40% of GMV, so the platform loses bargaining power if they go.
- Selection: a test among small sellers does not tell you what top sellers do.

**What the interviewer scores:**
- Strong: 12.00 to 13.23 correctly, and notes GMV falls 11.8%. Weak: multiplies 15% by 100 million.
- Strong: gives the break-even loss (45.5% of top sellers) to show how fragile the gain is. Weak: says "top sellers are risky" without a number.
- Strong: names off-platform leakage, buyer-side effects and negotiation. Weak: only "they might churn".
- Strong: proposes a segmented rollout and guardrails. Weak: recommends the full rise on the number.

**Example:** illustrative numbers in millions.
- Weak: "Revenue grows by 3 points of 100 million, so +3 million."
- Strong: "After the response, GMV is 88.2, so revenue is 13.23, up 1.23. But 1.23 is only 3% of the top sellers' GMV; if they lose 45% instead of 25% the gain is gone. I would test a tiered rate with the top sellers separately."
- In my run (below): with a 60% top-seller loss, revenue falls to 11.13 (-7.3%).

**Code:**
```python
# Q28: take rate 12% -> 15% (illustrative, millions)
gmv_top, gmv_oth, tr0, tr1 = 40.0, 60.0, 0.12, 0.15
rev0 = tr0 * (gmv_top + gmv_oth)
top1, oth1 = gmv_top * (1 - 0.25), gmv_oth * (1 - 0.03)
rev1 = tr1 * (top1 + oth1)
print(f"before: GMV {gmv_top+gmv_oth:.1f}, revenue {rev0:.2f}")
print(f"after: top {top1:.1f}, others {oth1:.1f}, GMV {top1+oth1:.1f} ({(top1+oth1)/100-1:+.1%}), revenue {rev1:.3f} ({rev1/rev0-1:+.2%})")
assert abs(rev0 - 12.0) < 1e-9 and top1 == 30.0 and abs(oth1 - 58.2) < 1e-9 and abs(rev1 - 13.23) < 1e-9

# break-even top-seller loss (others -3%) for revenue to stay at 12.0
x = 1 - (rev0 / tr1 - oth1) / gmv_top
print(f"revenue is flat if top-seller GMV falls {x:.1%} (others -3%)")
assert abs(x - 0.455) < 1e-3
# break-even uniform GMV loss
u = 1 - rev0 / (tr1 * 100)
print(f"or if GMV falls {u:.0%} across everyone")
assert abs(u - 0.20) < 1e-9

# sensitivity of revenue to the top-seller loss
for loss in (0.25, 0.35, 0.455, 0.60):
    r = tr1 * (gmv_top * (1 - loss) + oth1)
    print(f"  top sellers -{loss:.1%}: revenue {r:.2f} ({r/rev0-1:+.1%})")
assert tr1 * (gmv_top * (1 - 0.60) + oth1) < rev0

# if top-seller loss also drags other sellers' GMV (buyers who came for the top sellers leave): others -3% -> -15%
r2 = tr1 * (top1 + gmv_oth * 0.85)
print(f"top -25% and others -15%: revenue {r2:.2f} ({r2/rev0-1:+.1%})")
assert abs(r2 - 0.15 * (30 + 51)) < 1e-9 and r2 > rev0
# share of take from top sellers, and the margin they keep
print(f"top sellers pay {tr0*gmv_top:.2f} of 12.00 now ({tr0*gmv_top/rev0:.0%}) and {tr1*top1:.2f} of {rev1:.2f} after ({tr1*top1/rev1:.0%})")
```

**Output (my run):**
```text
before: GMV 100.0, revenue 12.00
after: top 30.0, others 58.2, GMV 88.2 (-11.8%), revenue 13.230 (+10.25%)
revenue is flat if top-seller GMV falls 45.5% (others -3%)
or if GMV falls 20% across everyone
  top sellers -25.0%: revenue 13.23 (+10.2%)
  top sellers -35.0%: revenue 12.63 (+5.2%)
  top sellers -45.5%: revenue 12.00 (+0.0%)
  top sellers -60.0%: revenue 11.13 (-7.3%)
top -25% and others -15%: revenue 12.15 (+1.2%)
top sellers pay 4.80 of 12.00 now (40%) and 4.50 of 13.23 after (34%)
```

**Follow-ups:**
- *How would you test the rise?* Randomise by seller or by region among small and mid sellers; for top sellers, negotiate case by case (they are too few to randomise), and compare with matched sellers.
- *Is take rate the right objective?* Revenue is take rate x GMV; the long-run objective also includes liquidity and trust, which GMV loss weakens.
- *What about a tiered rate?* A lower rate for top sellers, or a rate that falls with volume, protects the large accounts and still lifts the revenue from the long tail.

**Common mistakes:**
- Forgetting that GMV falls, so revenue grows less than 25% (rate rises 25% relative: 12 to 15).
- Using one blended response for all sellers.
- Ignoring the buyer side.
- Reporting a point estimate with no sensitivity.

### Q29 ⭐⭐ 🟡 A lender wants to lower its score cut-off, which would approve 4,000 more loans a month in a marginal band. A repaid loan earns 150 and a default loses 600. The band's default rate is estimated at 12% of its loans from data collected in a different economy, with a plausible range up to 22%. Compute the monthly profit of the band at 12% and at 22%, and say how you would decide and monitor.
**Asked at:** Credit-risk material (a Dataford 'optimal cut-off score to maximise profit' page, an Interview Query auto-lending data scientist guide, a quintedge credit-risk interview page, academic papers on profit-maximising cut-offs); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** At a 12% default rate the band makes 240,000 a month, at 22% it loses 60,000, and the break-even default rate is 20%, so the plausible range straddles the line; I would not open the whole band, I would pilot it and watch early defaults.

**Clarifying questions:**
- What do 150 and 600 cover: interest, fees, funding cost, servicing, recoveries? The break-even rate depends on them (Q4 in this part builds the same break-even).
- How was the 12% estimated, and in which economy? A model trained in another economy may be badly calibrated here.
- How long until a default is visible (label delay)? That decides how quickly a pilot can answer.
- Can we cap exposure (smaller limits, shorter tenor, higher price) for the marginal band? That reduces the loss side.
- Are there fair-lending, regulatory or portfolio-concentration limits on lowering the cut-off?

**Approach:**
1. Profit per loan = (1 - PD) x 150 - PD x 600. At 12%: 0.88 x 150 - 0.12 x 600 = 132 - 72 = +60. Monthly: 60 x 4,000 = +240,000.
2. At 22%: 0.78 x 150 - 0.22 x 600 = 117 - 132 = -15 per loan. Monthly: -60,000.
3. Break-even default rate = 150 / (150 + 600) = 20%. The plausible range 12% to 22% crosses it, so the decision depends on which end is true.
4. Do not decide on the point estimate. The number comes from a different economy, so treat 12% as optimistic until measured; calibrate the score on local outcomes.
5. Decide in stages: approve a small random slice of the band (for example 1,000 loans) with tight limits; the worst-case loss of that pilot is 1,000 x 15 = 15,000 against 60,000 for the full band.
6. Monitor: early-delinquency and first-payment default by vintage, compare observed with predicted by score decile, and set a stop rule (for example pause if early default is running above the path implied by 20% lifetime default).
7. Expand when the local default rate is credibly below 20% with room for funding and servicing cost; otherwise raise price or cut limits for the band instead of opening it.

**Metrics:**
- Default rate = loans in default within a fixed window / loans originated in the vintage.
- Profit per loan = (1 - default rate) x gain on repaid - default rate x loss on default.
- Break-even PD = gain / (gain + loss).
- Guardrails: calibration (predicted versus observed default by band), approval rate, portfolio loss by vintage, share of the book in the marginal band, fairness checks across groups.

**Risks:**
- Label delay: the pilot's defaults arrive months later, so early indicators are proxies.
- Selection: the band's applicants may differ from the training population (different economy), so the score's ranking is also less reliable.
- A random pilot is small: with 300 loans, the chance of seeing under 20% when the truth is 22% is 18%, with 1,000 loans it is 6%, with 3,000 loans 0.4%.
- Assuming the 150 and 600 are fixed; they may vary with loan size and recovery.
- Adverse selection: a looser cut-off can attract riskier applicants over time.

**What the interviewer scores:**
- Strong: computes 240,000 and -60,000 and the 20% break-even. Weak: uses 12% only.
- Strong: treats the range as a decision problem and proposes a staged test with a stop rule. Weak: "I would trust the model".
- Strong: names label delay and calibration. Weak: monitors accuracy or AUC only.
- Strong: mentions price, limits and tenor as levers. Weak: only approve or reject.

**Example:** illustrative numbers.
- Weak: "12% default gives 240,000 a month, so approve all 4,000."
- Strong: "Break-even is 20%, and the plausible range reaches 22%, where I lose 60,000 a month. I would approve 1,000 loans at first (worst case -15,000), track early delinquency by vintage, and only then widen."
- In my run (below): if 12% and 22% were equally likely the expected profit is +90,000, but the downside is real and the data to settle it will arrive within a few months.

**Code:**
```python
# Q29: lowering a credit cut-off (illustrative)
n, gain, loss = 4000, 150.0, 600.0
def band(pd_):
    per = (1 - pd_) * gain - pd_ * loss
    return per, per * n
for pd_ in (0.12, 0.22):
    per, tot = band(pd_)
    print(f"default rate {pd_:.0%}: profit per loan {per:+.2f}; monthly band profit {tot:+,.0f}")
assert abs(band(0.12)[0] - 60) < 1e-9 and abs(band(0.12)[1] - 240_000) < 1e-6
assert abs(band(0.22)[0] + 15) < 1e-9 and abs(band(0.22)[1] + 60_000) < 1e-6
be = gain / (gain + loss)
print(f"break-even default rate {be:.1%} (the interval 12% to 22% straddles it)")
assert abs(be - 0.2) < 1e-12 and 0.12 < be < 0.22

# monitoring: how many loans do you need to tell 12% from 20%? pilot default counts with a binomial
from scipy import stats
for m in (300, 1000, 3000):
    se = (0.12 * 0.88 / m) ** 0.5
    # one-sided: P(observed rate >= break-even 20% | true 12%)
    k = int(be * m)
    p_fp = stats.binom.sf(k - 1, m, 0.12)
    # P(observed rate < 20% | true 22%): would wrongly look fine
    p_fn = stats.binom.cdf(k - 1, m, 0.22)
    print(f"pilot {m}: SE at 12% = {se*100:.2f} pts; P(see >=20% if truth 12%) = {p_fp:.4f}; P(see <20% if truth 22%) = {p_fn:.3f}")
assert stats.binom.sf(int(be*1000) - 1, 1000, 0.12) < 1e-4
assert stats.binom.cdf(int(be*1000) - 1, 1000, 0.22) < 0.25

# expected loss of a 1,000-loan pilot at the worst case vs full launch at the worst case
pilot_loss = band(0.22)[0] * 1000
print(f"worst-case pilot of 1,000 loans: {pilot_loss:+,.0f}; worst-case full month: {band(0.22)[1]:+,.0f}")
assert pilot_loss == -15000
# expected value at 50/50 between 12% and 22%
ev = 0.5 * band(0.12)[1] + 0.5 * band(0.22)[1]
print(f"expected monthly profit if 12% and 22% are equally likely: {ev:+,.0f}")
assert ev == 90_000
```

**Output (my run):**
```text
default rate 12%: profit per loan +60.00; monthly band profit +240,000
default rate 22%: profit per loan -15.00; monthly band profit -60,000
break-even default rate 20.0% (the interval 12% to 22% straddles it)
pilot 300: SE at 12% = 1.88 pts; P(see >=20% if truth 12%) = 0.0001; P(see <20% if truth 22%) = 0.183
pilot 1000: SE at 12% = 1.03 pts; P(see >=20% if truth 12%) = 0.0000; P(see <20% if truth 22%) = 0.058
pilot 3000: SE at 12% = 0.59 pts; P(see >=20% if truth 12%) = 0.0000; P(see <20% if truth 22%) = 0.004
worst-case pilot of 1,000 loans: -15,000; worst-case full month: -60,000
expected monthly profit if 12% and 22% are equally likely: +90,000
```

**Follow-ups:**
- *How would you recalibrate the score for this economy?* Compare predicted and observed defaults on local loans (calibration curve), and re-fit or adjust the score with local data; use a holdout vintage.
- *Which is worse: a 22% rate with 12% assumed, or the reverse?* The first costs real money (-60,000 a month); the second only misses profit. The costs are asymmetric, so pilot first.
- *Would you also change the price?* Yes: for a marginal band, a higher rate or a smaller limit can move the break-even and keep the loans profitable.

**Common mistakes:**
- Using AUC to decide the cut-off; the cut-off is an economic decision.
- Forgetting that default rates from another economy do not transfer.
- Ignoring funding and servicing cost in the 150 and 600.
- Declaring a pilot a success after a few weeks of data, before defaults mature.

### Q30 ⭐⭐ 🟡 A food platform takes 100,000 orders a day. Promising the median predicted delivery time makes 50% of orders late (50,000), and promising the 80th percentile makes 20% of the remaining orders late (19,800) but the longer promise cuts orders by 1% relative to 100,000, at a margin of 1.50 per order. A late order costs 3.00 in refunds and lost goodwill. Compute the daily difference between the two promises and say which input is least certain.
**Asked at:** Delivery, ETA and routing material (an AlgoMaster ETA-prediction design walkthrough, a DoorDash careers post and an Uber Eats ETA write-up as described in snippets, an Appinventiv case study using an asymmetric loss, a quantile-regression delivery-time slide deck); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The 80th-percentile promise is better by 89,100 a day, because the median promise earns 150,000 of margin and pays 150,000 in late costs; the least certain input is the 3.00 late cost, with the 1% order loss second.

**Clarifying questions:**
- How was the 3.00 per late order built: refunds (hard number) plus goodwill (soft number)? The goodwill part is the guess.
- Where does the 1% order loss come from: a promise-length experiment or an assumption? Longer promises can lose far more orders in some segments.
- Are the late shares (50% and 20%) measured on current predictions, or assumed from percentile definitions? Real calibration drifts.
- Do late orders also lower repeat orders? That is not in the 3.00 unless included.
- Is the promise shown at checkout, so users can walk away, or only afterwards? It decides whether the order loss is real.

**Approach:**
1. Median promise (A): margin 100,000 x 1.50 = 150,000. Late orders 50,000 x 3.00 = 150,000. Net 0.
2. 80th percentile (B): orders 99,000, margin 99,000 x 1.50 = 148,500. Late 20% x 99,000 = 19,800, cost 59,400. Net 89,100.
3. Difference: B - A = +89,100 a day. Per order, A nets 0.00 and B nets 0.90.
4. Sensitivity: B stays ahead unless the late cost falls below about 0.05. If the late cost were 1.00, B is ahead by 28,700. At 3.00, even a 50% order loss leaves B ahead by 45,000; at 1.00 the order loss that wipes out the gain is 23%.
5. So the late cost drives the answer, and the order loss is second. I would measure both: late cost from refund data and a repeat-rate analysis, order loss from a randomised promise-length test.
6. Recommend: promise a high percentile, display it honestly, and also work on actually reducing the time (so the percentile itself falls). A later step is to choose the percentile that maximises net value (an asymmetric loss), by segment and time of day.

**Metrics:**
- Net daily value = orders x margin per order - late orders x cost per late order.
- Late rate = orders delivered after the promised time / orders delivered.
- Conversion at checkout by promise shown (to measure the order loss).
- Guardrails: promised time versus actual time distribution, repeat-order rate for late orders, support contacts per order.

**Risks:**
- The late cost is partly goodwill and hard to measure; it is the number that moves the answer.
- Longer promises lose orders unevenly (urgent orders, competitors): the 1% may be an average over very different groups.
- Calibration: if the model is not calibrated, the "80th percentile" is late more or less than 20% of the time.
- Gaming: padding every promise reduces trust in the number.
- Ignoring that fewer late orders also improves retention.

**What the interviewer scores:**
- Strong: gets A = 0 and B = +89,100, applying the 20% to the 99,000 remaining orders. Weak: ignores the lost orders.
- Strong: runs the sensitivity and names the late cost as the swing input. Weak: names demand only.
- Strong: links to quantile (asymmetric) loss and calibration. Weak: says "use the mean prediction".
- Strong: proposes the randomised promise test. Weak: relies on the 1% as fact.

**Example:** illustrative numbers.
- Weak: "Median is the most accurate; promise that."
- Strong: "A median promise is late half the time. At 3.00 a late order that costs the whole 1.50 margin. The 80th percentile gives up 1% of orders and gains about 89,000 a day. The decision only flips if a late order costs under about 0.05, so I would measure the 3.00 and the order loss, then tune the percentile."
- In my run (below): at a late cost of 1.00, B is still ahead by 28,700, but a 30% order loss would flip it (-9,000).

**Code:**
```python
# Q30: delivery promise, median vs 80th percentile (illustrative)
orders, margin, late_cost = 100_000, 1.50, 3.00
# A: median promise
lateA = 0.50 * orders
netA = orders * margin - lateA * late_cost
# B: 80th percentile promise, 1% fewer orders
ordersB = orders * 0.99
lateB_exact = 0.20 * ordersB          # 20% of the orders that remain = 19,800
for name, lb in (("20% of 99,000 = 19,800", lateB_exact),):
    netB = ordersB * margin - lb * late_cost
    print(f"B with {name}: margin {ordersB*margin:,.0f} - refunds {lb*late_cost:,.0f} = {netB:,.0f}; A = {netA:,.0f}; B - A = {netB-netA:+,.0f}")
assert netA == 0 and ordersB * margin == 148_500
assert abs(lateB_exact - 19_800) < 1e-9
assert abs((ordersB * margin - lateB_exact * late_cost) - 89_100) < 1e-6

# per-order view
print(f"per order: A {margin-0.5*late_cost:.2f}; B {margin-0.2*late_cost:.2f}")
assert abs((margin - 0.5 * late_cost)) < 1e-12 and abs(margin - 0.2 * late_cost - 0.9) < 1e-12

# sensitivity to the late cost c and the order loss d
def net(share_late, d, c): 
    o = orders * (1 - d)
    return o * (margin - share_late * c)
print("late cost c: B-A")
for c in (3.0, 1.0, 0.5, 0.05, 0.0):
    print(f"  c={c:4.2f}: {net(0.2, 0.01, c) - net(0.5, 0.0, c):+,.0f}")
c_flip = (margin - margin * 0.99) / (0.5 - 0.2 * 0.99)
print(f"break-even late cost {c_flip:.4f}")
assert abs(c_flip - 0.0497) < 1e-3
print("order loss d: B-A at c=3.00 and at c=1.00")
for d in (0.01, 0.10, 0.30, 0.50):
    print(f"  d={d:.0%}: c=3.00 {net(0.2, d, 3.0) - net(0.5, 0, 3.0):+,.0f}; c=1.00 {net(0.2, d, 1.0) - net(0.5, 0, 1.0):+,.0f}")
d_flip = 1 - net(0.5, 0, 1.0) / net(0.2, 0, 1.0)
print(f"order loss that wipes out the gain at c=1.00: {d_flip:.1%}")
assert abs(d_flip - 0.2308) < 1e-3 and net(0.2, 0.30, 3.0) > net(0.5, 0, 3.0)
```

**Output (my run):**
```text
B with 20% of 99,000 = 19,800: margin 148,500 - refunds 59,400 = 89,100; A = 0; B - A = +89,100
per order: A 0.00; B 0.90
late cost c: B-A
  c=3.00: +89,100
  c=1.00: +28,700
  c=0.50: +13,600
  c=0.05: +10
  c=0.00: -1,500
break-even late cost 0.0497
order loss d: B-A at c=3.00 and at c=1.00
  d=1%: c=3.00 +89,100; c=1.00 +28,700
  d=10%: c=3.00 +81,000; c=1.00 +17,000
  d=30%: c=3.00 +63,000; c=1.00 -9,000
  d=50%: c=3.00 +45,000; c=1.00 -35,000
order loss that wipes out the gain at c=1.00: 23.1%
```

**Follow-ups:**
- *Why is the median a bad promise?* By definition half of orders arrive after it; the promise is a commitment, so the cost is asymmetric (late is worse than early).
- *How would you pick the percentile?* Choose the quantile q that maximises net value per order; with a linear late cost, the optimum is where the marginal order loss and refund saving balance. Train a quantile model and test several percentiles.
- *What if the promise is only shown after ordering?* Then there is no order loss at all, and the longer promise is a pure gain on refunds; but customers may feel misled when they see it.

**Common mistakes:**
- Costing late orders on the original 100,000 after orders have fallen.
- Forgetting the lost margin on the 1,000 orders.
- Calling the 1% an input that is known.
- Predicting the mean time and promising it.

### Q31 ⭐⭐ 🟡 A dispatcher can send one courier per order at 3.50 a delivery, or batch two orders per courier at 2.40 a delivery. Batching raises the share of late deliveries from 8% to 14% of deliveries (6 points absolute), and a late delivery costs 4.00 in refunds. Compute the net saving per delivery and the break-even late rate, and say what the refund figure misses.
**Asked at:** Delivery, ETA and routing material (an AlgoMaster ETA-prediction design walkthrough, a DoorDash careers post and an Uber Eats ETA write-up as described in snippets, an Appinventiv case study using an asymmetric loss, a quantile-regression delivery-time slide deck); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Batching saves 1.10 on courier cost and adds 0.24 of expected refunds (6 points x 4.00), so the net saving is 0.86 per delivery; batching stays worthwhile until the late rate reaches 35.5%, but the refund is only part of what late deliveries cost.

**Clarifying questions:**
- Is 3.50 and 2.40 the courier cost per delivery, all in (pay, incentive, idle time)? A batched courier may also wait for the second order.
- Does the 14% late rate apply to both orders in the batch or only to the second one? Food orders delivered second go cold.
- Are all orders eligible for batching (distance, restaurant pairs), or only some? Savings scale with the share batched.
- Is the 4.00 only the refund, or does it include goodwill and repeat loss? The break-even depends on it.
- What is a late delivery: more than 5 minutes past the promise, or 20? Severity matters.

**Approach:**
1. Courier saving = 3.50 - 2.40 = 1.10 per delivery.
2. Extra late share = 14% - 8% = 6 points absolute. Extra expected refund = 0.06 x 4.00 = 0.24 per delivery.
3. Net saving = 1.10 - 0.24 = 0.86 per delivery. Check: total cost single = 3.50 + 0.08 x 4.00 = 3.82; batched = 2.40 + 0.14 x 4.00 = 2.96; difference 0.86.
4. Break-even late rate: 2.40 + L x 4.00 = 3.82, so L = 35.5%. Batching only loses money once the late rate is 27.5 points higher than today's 8%.
5. Equivalent view: the late delivery would have to cost 1.10 / 0.06 = 18.33 each (at 14% versus 8%) to cancel the saving. So the refund figure is not the only issue: the question is whether the real cost of lateness is that high.
6. What the refund misses: repeat orders lost after a late or cold delivery, ratings and complaints, support cost, restaurant and courier relations, and the long tail (how late, not only whether late). Refunds also undercount: many late customers do not claim.
7. Recommend: batch where the late rate is lowest (short distances, same-restaurant pairs, off-peak), keep a lateness cap in the batching rule, and run a randomised test measuring repeat orders for four weeks.

**Metrics:**
- Cost per delivery = courier cost per delivery + late rate x cost per late delivery.
- Late rate = deliveries later than promise / deliveries (by arm and by order position in the batch).
- Net saving per delivery = (single cost per delivery - batched cost per delivery), with all lateness costs.
- Guardrails: repeat-order rate within 28 days, rating, refund and complaint rate, courier earnings per hour, delivery time (p50 and p90).

**Risks:**
- Counting only refunds as the cost of lateness.
- Averaging over all orders when late risk is concentrated in a few (the second order, long detours).
- Courier pay per delivery may rise if batching stretches the trip.
- Peak versus off-peak: late risk rises with load.
- A before-and-after comparison; use randomised dispatch rules.

**What the interviewer scores:**
- Strong: 0.86, the 35.5% break-even, and the equivalent late-cost break-even of 18.33. Weak: only the first line.
- Strong: lists the costs that refunds miss and how to measure them (repeat-order test). Weak: "customer experience".
- Strong: proposes a conditional batching rule with a lateness cap. Weak: all or nothing.
- Strong: asks which order in the batch is late. Weak: treats the 14% as uniform.

**Example:** illustrative numbers.
- Weak: "Batching saves 1.10 a delivery, so do it."
- Strong: "Net is 0.86 after expected refunds. Batching only fails at a 35.5% late rate, so we have room, but lateness also costs repeat orders. I would batch short, same-area pairs with a lateness cap, and measure repeat orders in a randomised test."
- In my run (below): if only half of orders are batchable, the overall net saving is 0.43 per delivery.

**Code:**
```python
# Q31: batching two orders per courier (illustrative)
single, batch = 3.50, 2.40
late0, late1, refund = 0.08, 0.14, 4.00
saving = single - batch
extra_late_cost = (late1 - late0) * refund
net = saving - extra_late_cost
print(f"courier saving {saving:.2f}; extra expected refund {extra_late_cost:.2f}; net saving per delivery {net:.2f}")
assert abs(saving - 1.10) < 1e-9 and abs(extra_late_cost - 0.24) < 1e-9 and abs(net - 0.86) < 1e-9
assert abs((late1 - late0) - 0.06) < 1e-12

# totals per delivery (courier + expected refunds)
tot0 = single + late0 * refund
tot1 = batch + late1 * refund
print(f"total cost per delivery: single {tot0:.2f}; batched {tot1:.2f}; difference {tot0-tot1:.2f}")
assert abs(tot0 - 3.82) < 1e-9 and abs(tot1 - 2.96) < 1e-9

# break-even late rate for batching
be_late = (single + late0 * refund - batch) / refund
print(f"break-even late rate for batching {be_late:.1%} ({(be_late-late0)*100:.1f} points above 8%)")
assert abs(be_late - 0.355) < 1e-9

# if each late order really costs more (refund + goodwill + lost repeat), break-even refund at 14% late
be_refund = saving / (late1 - late0)
print(f"break-even cost per late delivery at 14% vs 8% late: {be_refund:.2f}")
assert abs(be_refund - 18.3333) < 1e-3
# batching only half of orders: saving scales with batched share
for share in (1.0, 0.5, 0.25):
    print(f"  batch share {share:.0%}: net saving per delivery overall {share*net:.3f}")
assert abs(0.5 * net - 0.43) < 1e-9
```

**Output (my run):**
```text
courier saving 1.10; extra expected refund 0.24; net saving per delivery 0.86
total cost per delivery: single 3.82; batched 2.96; difference 0.86
break-even late rate for batching 35.5% (27.5 points above 8%)
break-even cost per late delivery at 14% vs 8% late: 18.33
  batch share 100%: net saving per delivery overall 0.860
  batch share 50%: net saving per delivery overall 0.430
  batch share 25%: net saving per delivery overall 0.215
```

**Follow-ups:**
- *How would you decide which orders to batch?* Predict the late probability for each pair (distance, prep time, courier location), and batch only when the expected saving exceeds the expected lateness cost.
- *What is the long-run cost of a late order?* The lost future margin of the customers who stop ordering; estimate it from a holdout comparing repeat orders of late and on-time customers, adjusting for who gets late deliveries.
- *Would you ever raise the promise instead?* Yes, a longer promise on batched orders lowers the late share (see Q30 in this part for the trade-off).

**Common mistakes:**
- Using 6 percent instead of 6 points, or applying 14% to the wrong base.
- Treating the refund as the full cost of lateness.
- Forgetting that the saving applies only to the batched share.
- Reading a short test as a long-run result.

### Q32 ⭐⭐ 🟡 A store sells 50 units a day on average with a daily standard deviation of 10, and restocking takes 4 days. Assuming independent days, compute the standard deviation of lead-time demand, the safety stock for a 95% service level (z = 1.645) and the reorder point, and say what breaks the independence assumption.
**Asked at:** Forecasting and inventory material (PracHub retail demand-forecasting and inventory-and-stockout concept pages, a Dataford supermarket demand-forecasting page attributed in its title to a BCG data scientist interview but unverified, a PyCon DE 2025 talk on stockouts in retail forecasting); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Lead-time demand has a mean of 200 and a standard deviation of 10 x sqrt(4) = 20, so the safety stock is 1.645 x 20 = 32.9 and the reorder point is about 233 units; independence is the fragile assumption, because promotions, trends and weekday patterns link the days.

**Clarifying questions:**
- Is the 4-day lead time fixed, or does it vary by supplier? Lead-time variability usually adds more risk than demand variability.
- Is the 95% a cycle service level (chance of no stockout in a cycle) or a fill rate (share of units served)? They are different targets.
- Is the daily sd of 10 measured around a flat mean, or around a forecast? Seasonal or promotional swings inflate it.
- What are the costs of a stockout versus holding stock? The service level should come from them, not be a default.
- Are lost sales or backorders the result of a stockout? That sets how costly a miss is.

**Approach:**
1. Lead-time demand: mean 50 x 4 = 200.
2. With independent days the variances add: variance 4 x 10^2 = 400, so sd = 20 (10 x sqrt(4)).
3. Safety stock = z x sd = 1.645 x 20 = 32.9 units.
4. Reorder point = 200 + 32.9 = 232.9, so order when stock position reaches about 233.
5. Check by simulation: with normal independent days the chance that lead-time demand stays under 232.9 is 95.0%.
6. What breaks independence: (a) positive autocorrelation (a busy day follows a busy day: promotions, paydays, weather, trends); with correlation 0.3 between neighbouring days the sd becomes 24.9, the safety stock 41.0, and the same reorder point gives only about 90.6% service; (b) weekday and seasonal patterns; (c) lead-time variability: with a lead-time sd of 1 day, sd rises to 53.9 and safety stock to 88.6; (d) stockouts that censor the demand you observe (see Q22 in this part); (e) demand shared across stores or products.
7. Fix: estimate the sd of the forecast error over the lead time directly from history (not daily sd x sqrt(L)), include lead-time variance, and review service levels by item class.

**Metrics:**
- Lead-time demand sd = sqrt(L x sigma_d^2 + mu_d^2 x sigma_L^2) when both vary; here sigma_L = 0 so it reduces to 10 x sqrt(4).
- Safety stock = z x sd of lead-time demand error. Reorder point = mean lead-time demand + safety stock.
- Cycle service level = share of replenishment cycles without a stockout. Fill rate = units supplied from stock / units demanded.
- Guardrails: stockout days, inventory days of cover, waste or markdown, forecast bias.

**Risks:**
- Independence and normality both assumed; skewed or intermittent demand makes the normal tail wrong.
- Daily sd estimated on a calm period understates peak risk.
- Using sales instead of demand (stockout days hide demand).
- A single 95% for every item ignores differences in margin and holding cost.
- Lead-time variance can matter more than demand variance.

**What the interviewer scores:**
- Strong: 20, 32.9, 232.9, and square-root rule explained (variances add). Weak: multiplies 10 by 4.
- Strong: names several concrete breaks of independence with the effect direction. Weak: "demand is not independent".
- Strong: separates cycle service level from fill rate. Weak: treats them as the same.
- Strong: proposes estimating the lead-time error directly and including lead-time variability. Weak: only increases z.

**Example:** illustrative numbers.
- Weak: "Demand is 50 a day, 4 days, so reorder at 200 plus some buffer."
- Strong: "Reorder point 233: mean 200 plus 32.9 of safety stock from sd 20. If neighbouring days are positively correlated (0.3), the true sd is nearer 25 and I need 41 of safety stock; with the 233 reorder point I would be at about 91% service, not 95%."
- In my run (below): with a lead-time sd of 1 day the safety stock rises from 32.9 to 88.6.

**Code:**
```python
# Q32: lead-time demand and safety stock (illustrative)
import numpy as np
mu, sd, L, z = 50.0, 10.0, 4, 1.645
sd_L = sd * np.sqrt(L)
ss = z * sd_L
mean_L = mu * L
rop = mean_L + ss
print(f"lead-time demand mean {mean_L:.0f}, sd {sd_L:.1f}; safety stock {ss:.2f}; reorder point {rop:.2f}")
assert sd_L == 20.0 and abs(ss - 32.9) < 1e-9 and abs(rop - 232.9) < 1e-9

rng = np.random.default_rng(32)
N = 400_000
d = rng.normal(mu, sd, (N, L)).sum(axis=1)
print("simulated cycle service level at ROP 232.9 with independent days:", round((d <= rop).mean(), 4))
assert abs((d <= rop).mean() - 0.95) < 0.003

# positively autocorrelated days (AR(1), rho=0.3), same daily mean and sd
rho = 0.3
e = rng.normal(0, 1, (N, L))
x = np.zeros((N, L)); x[:, 0] = e[:, 0]
for t in range(1, L):
    x[:, t] = rho * x[:, t-1] + np.sqrt(1 - rho**2) * e[:, t]
dd = (mu + sd * x).sum(axis=1)
var_formula = sd**2 * (L + 2 * sum((L - k) * rho**k for k in range(1, L)))
print(f"rho=0.3: simulated sd {dd.std():.2f}, formula {np.sqrt(var_formula):.2f} (independence said 20.0)")
print("service level at the same ROP:", round((dd <= rop).mean(), 4), "; safety stock needed for 95%:", round(z * np.sqrt(var_formula), 1))
assert abs(dd.std() - np.sqrt(var_formula)) < 0.2 and (dd <= rop).mean() < 0.95 - 0.01
assert abs(z * np.sqrt(var_formula) - 41.0) < 0.2

# lead time itself varies (mean 4, sd 1 day), independent days
sd_Lt = 1.0
var2 = L * sd**2 + mu**2 * sd_Lt**2
print(f"with lead-time sd 1 day: sd of lead-time demand {np.sqrt(var2):.1f}; safety stock {z*np.sqrt(var2):.1f}")
assert abs(np.sqrt(var2) - np.sqrt(400 + 2500)) < 1e-9 and z * np.sqrt(var2) > 85
```

**Output (my run):**
```text
lead-time demand mean 200, sd 20.0; safety stock 32.90; reorder point 232.90
simulated cycle service level at ROP 232.9 with independent days: 0.9499
rho=0.3: simulated sd 24.89, formula 24.93 (independence said 20.0)
service level at the same ROP: 0.9064 ; safety stock needed for 95%: 41.0
with lead-time sd 1 day: sd of lead-time demand 53.9; safety stock 88.6
```

**Follow-ups:**
- *How do you get a 99% service level?* z = 2.326, so safety stock is 46.5 under independence; the cost rises faster than the benefit as the target approaches 100%.
- *What if sales understate demand?* Fit demand with censoring (days with stockouts are lower bounds), or use only in-stock days to estimate the sd.
- *Is the sqrt(L) rule right for weekly lead times?* Only if weekly demand has no autocorrelation; check the autocorrelation of residuals first.

**Common mistakes:**
- Multiplying the daily sd by 4 instead of 2.
- Using the formula with a service level that is really a fill-rate target.
- Ignoring lead-time variability.
- Estimating sd from sales on stockout days.

### Q33 ⭐⭐ 🟡 Marketing-mix modelling on three years of weekly data says that raising paid-search spend from 100,000 to 200,000 a month raises total monthly revenue (all sources) from 500,000 to 650,000, and gross margin is 40% of revenue. Compute the average ROAS at each spend level, the marginal ROAS and the marginal profit, and list what could make the fitted curve wrong.
**Asked at:** Marketing measurement material (a datainterview.com paid-social incrementality case, an aitrainer.work marketing data scientist question page, Triple Whale and Eppo GeoLift pages, a Medium post on geo-experiments, a PyData Boston 2025 talk description); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Average ROAS is 5.00 at 100,000 and 3.25 at 200,000, but the extra 100,000 of spend buys 150,000 of revenue, a marginal ROAS of 1.5, which is 60,000 of margin for 100,000 of spend: a loss of 40,000 a month at the margin.

**Clarifying questions:**
- Is the 500,000 and 650,000 total revenue from all sources, or revenue attributed to paid search? The figures are total revenue (all sources), so "average ROAS" here is total revenue per unit of spend, which includes revenue that would arrive with no search spend.
- Was spend ever really at 200,000 in the three years, or is that point an extrapolation? Predictions outside the observed range are weak.
- Is the 40% gross margin before or after variable costs such as shipping, returns and payment fees?
- Did spend move with demand (more budget in peak weeks)? If so, the model confuses cause and effect.
- Do we value repeat purchases after the first order? A customer won today may be worth more than the first-order margin.

**Approach:**
1. Average ROAS = revenue / spend: 500,000 / 100,000 = 5.00 and 650,000 / 200,000 = 3.25. Say what it is: total revenue over spend, which is not the effect of search.
2. Marginal ROAS = (650,000 - 500,000) / (200,000 - 100,000) = 1.50 extra revenue per extra 1 of spend.
3. Marginal profit = 1.50 x 0.40 - 1.00 = -0.40 per 1 of spend. Over the extra 100,000: margin 60,000 minus spend 100,000 = -40,000 a month.
4. Break-even marginal ROAS = 1 / 0.40 = 2.5. The extra 100,000 would need to bring 250,000 of revenue, not 150,000.
5. Decide: on this fit do not increase to 200,000, and consider whether 100,000 is itself right; the average ROAS of 5.00 says nothing about the last pound or rupee spent.
6. Challenge the fit (list below), then validate with an experiment: a geo-holdout or spend-scaling test in randomly chosen regions, then re-calibrate the model.

**Metrics:**
- Average ROAS = revenue / spend (specify total or attributable). Marginal ROAS = change in revenue / change in spend.
- Marginal profit per 1 of spend = marginal ROAS x margin - 1. Break-even marginal ROAS = 1 / margin.
- Incrementality (geo-lift) = revenue per region with the spend change minus the control regions' revenue, over the spend difference.
- Guardrails: new-customer share, repeat-purchase rate, brand-search share, CAC by channel.

**Risks (what could make the curve wrong):**
- Endogeneity: marketers raise spend in good weeks, so revenue looks caused by spend. Seasonality and promotions confound the fit.
- Extrapolation: only a few weeks at the high spend, and the 200,000 level may not have been observed at all.
- Shape: two points do not give a curve; a linear, concave or S-shaped fit would imply different marginals. Diminishing returns usually make the marginal ROAS smaller than the average.
- Overlap: search, social, email and offline channels move together (collinearity), and brand search captures demand that other channels created.
- Lags and carry-over (adstock): spend this month affects next month's revenue; ignoring it mis-attributes.
- Structural change over three years: prices, competitors, algorithm updates, tracking changes.
- Lifetime value: first-order margin ignores repeat purchases, which could make the 40,000 loss smaller.

**What the interviewer scores:**
- Strong: 5.00, 3.25, 1.50, -0.40 and the break-even of 2.5, with the loss of 40,000. Weak: says "ROAS is 3.25, which is good".
- Strong: separates average from marginal and explains why the average hides saturation. Weak: calls both "ROAS".
- Strong: lists specific ways the fit could be wrong, and the fix (geo experiment, calibration). Weak: "the model might be wrong".
- Strong: mentions lifetime value as the reason a negative marginal profit might still be acceptable. Weak: ignores it.

**Example:** illustrative numbers.
- Weak: "ROAS is 3.25 at 200,000, above 2.5, so increase spend."
- Strong: "3.25 is total revenue over spend; it includes revenue that comes anyway. The extra 100,000 brings 150,000 of revenue and 60,000 of margin, so -40,000. I would hold spend, and run a geo test to check the 1.5."
- In my run (below): a sqrt-shaped curve through the same two points puts the marginal ROAS at 1.81 near 100,000 and 1.28 near 200,000, all below the 2.5 break-even; if 350,000 of revenue arrived with no search spend, attributable ROAS would be 1.5 at both levels.

**Code:**
```python
# Q33: paid-search ROAS from a marketing-mix fit (illustrative)
s0, s1, r0, r1, gm = 100_000, 200_000, 500_000, 650_000, 0.40
roas0, roas1 = r0 / s0, r1 / s1
mroas = (r1 - r0) / (s1 - s0)
mprofit = mroas * gm - 1
print(f"average ROAS (total revenue / spend): {roas0:.2f} at 100k, {roas1:.2f} at 200k")
print(f"marginal ROAS {mroas:.2f}; marginal gross margin per 1 of spend {mroas*gm:.2f}; marginal profit per 1 of spend {mprofit:+.2f}")
print(f"extra revenue {r1-r0:,}; extra margin {(r1-r0)*gm:,.0f}; extra spend {s1-s0:,}; net {(r1-r0)*gm-(s1-s0):+,.0f} a month")
assert (roas0, roas1) == (5.0, 3.25) and abs(mroas - 1.5) < 1e-12 and abs(mprofit + 0.4) < 1e-12
assert (r1 - r0) * gm - (s1 - s0) == -40_000

# break-even marginal ROAS and the revenue the extra 100k would need
be = 1 / gm
need = (s1 - s0) * be
print(f"break-even marginal ROAS {be:.2f}; extra revenue needed for the extra 100k to pay for itself {need:,.0f} (fitted: {r1-r0:,})")
assert abs(be - 2.5) < 1e-12 and need == 250_000

# average ROAS includes baseline (non-search) revenue: if the baseline were 350k at zero spend,
# search-attributable revenue is 150k at 100k and 300k at 200k
for base in (0, 350_000):
    print(f"  baseline {base:,}: attributable ROAS {(r0-base)/s0:.2f} at 100k, {(r1-base)/s1:.2f} at 200k")
assert (500_000 - 350_000) / 100_000 == 1.5 and (650_000 - 350_000) / 200_000 == 1.5

# the 1.5 is an average over the 100k to 200k stretch; a diminishing-returns curve through the same two points
# (R = a + b*sqrt(S)) has a higher marginal ROAS at 100k and a lower one at 200k
import numpy as np
b = (r1 - r0) / (np.sqrt(s1) - np.sqrt(s0))
for s_ in (100_000, 150_000, 200_000):
    m = b / (2 * np.sqrt(s_))
    print(f"  sqrt curve, marginal ROAS at {s_:,}: {m:.2f} -> marginal profit per 1 spent {m*gm-1:+.2f}")
assert b / (2 * np.sqrt(100_000)) > 1.5 > b / (2 * np.sqrt(200_000))
assert b / (2 * np.sqrt(100_000)) * gm - 1 < 0          # even the best point on that curve is below break-even 2.5
```

**Output (my run):**
```text
average ROAS (total revenue / spend): 5.00 at 100k, 3.25 at 200k
marginal ROAS 1.50; marginal gross margin per 1 of spend 0.60; marginal profit per 1 of spend -0.40
extra revenue 150,000; extra margin 60,000; extra spend 100,000; net -40,000 a month
break-even marginal ROAS 2.50; extra revenue needed for the extra 100k to pay for itself 250,000 (fitted: 150,000)
  baseline 0: attributable ROAS 5.00 at 100k, 3.25 at 200k
  baseline 350,000: attributable ROAS 1.50 at 100k, 1.50 at 200k
  sqrt curve, marginal ROAS at 100,000: 1.81 -> marginal profit per 1 spent -0.28
  sqrt curve, marginal ROAS at 150,000: 1.48 -> marginal profit per 1 spent -0.41
  sqrt curve, marginal ROAS at 200,000: 1.28 -> marginal profit per 1 spent -0.49
```

**Follow-ups:**
- *How would you validate the marginal ROAS?* A geo-holdout: change spend in randomly chosen regions, keep matched control regions, and compare revenue after the lag (4 to 8 weeks), with an interval.
- *Could a negative marginal profit still be right?* Yes, if customers repeat (lifetime value above first-order margin), if it protects share, or if the model underestimates the effect; each of these has to be shown with data.
- *What is the right spend level?* Where marginal ROAS equals 1 / margin (2.5 here), on a curve fitted with experiments; 100,000 may be above or below that.

**Common mistakes:**
- Reading average ROAS as the return on extra spend.
- Treating total revenue as search revenue.
- Trusting a fit that was never tested at the proposed spend.
- Ignoring the margin: a marginal ROAS of 1.5 loses money at a 40% margin.
