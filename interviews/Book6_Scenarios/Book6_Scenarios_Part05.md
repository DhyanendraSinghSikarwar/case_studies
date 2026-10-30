# Book 6 — Part 5: Business Case Studies (Pricing, Churn, Fraud, Supply Chain)

**Topic:** Scenario-based "a business has this problem; use data and models to decide" questions for Data Scientist, Product Analyst and ML Engineer loops: pricing and price changes, elasticity and demand curves, discount, coupon and promotion ROI and cannibalisation, dynamic pricing and surge, subscription pricing tiers, churn prediction and retention economics (propensity versus uplift), customer lifetime value and CAC payback, fraud-detection economics (false-positive cost, review capacity, chargebacks), credit and lending approval thresholds, demand forecasting and inventory or stock-outs, delivery ETA and routing, marketplace supply-demand balance and take rate, marketing mix and attribution, recommender, search and personalisation impact, build versus buy for a model, market sizing with data, unit economics and break-even, and AI-era twists (LLM support-agent ROI, GenAI feature cost-benefit).

**Target:** 55  |  **Actual:** 55 (⭐⭐⭐ 18, ⭐⭐ 25, ⭐ 12)  |  **Date:** 2026-10-30  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part owns the business-case and decision-maths angle: unit economics, expected value, break-even, ROI and what to do given the numbers. It does not repeat Book 6 Part 1 (product metrics), Part 2 (models degrading after launch), Part 3 (imbalanced and noisy data) or Part 4 (experiment design and ambiguous A/B results); Wave B answers should cross-reference those parts and the relevant Book 1 parts only by checked headings. All numbers in the prompts are invented illustrative numbers in one unnamed currency unit, not data from any company; every percentage names its base in the prompt and says whether it is a relative or absolute change where that could be ambiguous, and every arithmetic claim in a prompt is checked in scratch/B6P05_wavea/qs.py. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part05_sources.md). Searches returned pricing case-study guides (Interview Query, Dataford), churn and uplift articles, fraud-threshold and review-capacity pages, CLV and CAC guides, retail forecasting and stock-out pages, marketplace and take-rate guides, credit cut-off pages, promotion-incrementality and marketing-measurement pages, ETA and surge-pricing pages and 2026 vendor and practitioner posts on LLM support ROI and GenAI unit economics. Many results were general guidance or vendor marketing rather than interview pages, and none tied a scenario to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 A retailer raised the price of a snack from 10.00 to 11.00 (+10% relative to the old price), and weekly units fell from 5,000 to 4,600 (-8% relative to the old units). Unit cost is 6.00. Compute the price elasticity and the change in weekly revenue and gross profit, then say what else you check before rolling the new price out to every store.
**Asked at:** Pricing case-study guides (an Interview Query pricing case-study page, Dataford pricing and price-elasticity question pages for a food distributor and a fleet, 2026 pricing data scientist job postings at companies such as Target and Klook that list elasticity modelling and A/B or geo price tests); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Elasticity is -0.8, so revenue rises 600 a week and gross profit rises 3,000 a week, but this is one before-and-after read, so I would confirm it with a store-level test before a full rollout.

**Clarifying questions:**
- Was the 11.00 price set in all stores at once, or in a subset? A subset gives me a control group; an all-at-once change does not.
- Did anything else change in those weeks (promotion, season, competitor price, stock-outs)? Otherwise the -8% is not all caused by price.
- Is the unit cost 6.00 firm, and are there other costs per unit (waste, payment fees)? Profit depends on the true margin.
- Is the snack bought with other items (basket effect)? A cheaper-looking traffic driver can pull in other sales.
- How long did the new price run? A few weeks can include stock-up and pull-forward effects.

**Approach:**
1. Compute the elasticity: %change in units divided by %change in price = -8% / +10% = -0.8. (Midpoint method gives -0.875; say which one you used.)
2. Compute revenue: 10.00 x 5,000 = 50,000 becomes 11.00 x 4,600 = 50,600. That is +600.
3. Compute gross profit: (10-6) x 5,000 = 20,000 becomes (11-6) x 4,600 = 23,000. That is +3,000, or +15%.
4. Give the break-evens: profit stays flat until units fall 20%, revenue stays flat at -9.1%. We are far inside both.
5. Check causality: was it a clean test? Look for a control group, other changes, and a trend before the change.
6. Look beyond this SKU: basket spillover, competitor reaction, loyal versus price-sensitive shoppers, and whether the drop keeps growing over weeks.
7. Roll out in stages (a few store clusters, then more) with a guardrail on units and traffic.

**Metrics:**
- Price elasticity = (relative change in units) / (relative change in price). Here -0.8, so demand is inelastic and a price rise lifts revenue.
- Weekly revenue = price x units. Weekly gross profit = (price - unit cost) x units.
- Guardrails: store traffic, basket size, share of units versus competitors, out-of-stock rate.

**Risks:**
- A before/after read mixes price with season, weather and promotions. The drop could be bigger or smaller without price.
- Elasticity measured for +10% is not safe to extrapolate to +30%.
- One SKU's elasticity may hide that the price-sensitive shoppers moved to a rival store.
- Short run versus long run: shoppers may leave slowly.

**What the interviewer scores:**
- Strong: all three numbers right, with the break-even drop in units. Weak: gives elasticity only.
- Strong: separates revenue from gross profit. Weak: stops at revenue.
- Strong: asks whether the change was randomised or confounded. Weak: reads the -8% as purely the price effect.
- Strong: proposes a staged rollout with a guardrail. Weak: "just roll it out, profit went up."

**Example:** (illustrative numbers) Price 10.00 to 11.00, units 5,000 to 4,600, cost 6.00. Revenue +600, profit +3,000. If the real unit drop had been 20%, profit would be exactly flat at 20,000. If store-level weekly units are about 100 with a spread of 25, about 154 stores per arm are needed to see an 8% change with 80% power at 5% two-sided (illustrative assumptions). Weak answer: "Elasticity -0.8, ship it." Strong answer: "Profit is up 3,000 on this read, and it survives a drop up to 20%, but I want a store-level test first because the before/after is confounded."

**Code:**
```python
import math
p0, p1, u0, u1, cost = 10.0, 11.0, 5000, 4600, 6.0
dp = p1 / p0 - 1
du = u1 / u0 - 1
e_simple = du / dp
e_arc = ((u1 - u0) / ((u1 + u0) / 2)) / ((p1 - p0) / ((p1 + p0) / 2))
print(f"price {dp:+.1%}, units {du:+.1%}, simple elasticity {e_simple:.2f}, midpoint elasticity {e_arc:.3f}")
assert abs(dp - 0.10) < 1e-12 and abs(du + 0.08) < 1e-12 and abs(e_simple + 0.8) < 1e-12
assert abs(e_arc + 0.875) < 0.001
r0, r1 = p0 * u0, p1 * u1
g0, g1 = (p0 - cost) * u0, (p1 - cost) * u1
print(f"revenue {r0:,.0f} -> {r1:,.0f} ({r1-r0:+,.0f}); gross profit {g0:,.0f} -> {g1:,.0f} ({g1-g0:+,.0f}, {g1/g0-1:+.1%})")
assert (r0, r1, g0, g1) == (50000, 50600, 20000, 23000)
# break-evens: how far can units fall before the rise stops paying?
be_rev = r0 / p1                 # units at which revenue is unchanged
be_gp = g0 / (p1 - cost)         # units at which gross profit is unchanged
print(f"revenue break-even units {be_rev:,.0f} ({be_rev/u0-1:+.1%}); profit break-even units {be_gp:,.0f} ({be_gp/u0-1:+.1%})")
assert abs(be_gp - 4000) < 1e-9 and abs(be_rev / u0 - 1 + 1/11) < 1e-9
# how many stores to see an 8% unit change? (illustrative: 100 units/store/week, sd 25, 80% power, 5% two-sided)
from scipy import stats
mu, sd, eff = 100.0, 25.0, 0.08 * 100.0
n = 2 * ((stats.norm.isf(0.025) + stats.norm.isf(0.2)) * sd / eff) ** 2
print(f"stores per arm to detect -8% units: {math.ceil(n)}")
assert math.ceil(n) == 154
# price test result if the truth were a 20% drop: profit falls
g_bad = (p1 - cost) * u0 * 0.8
print(f"if units had fallen 20% (profit-neutral): gross profit {g_bad:,.0f} vs {g0:,.0f} before")
assert g_bad == 20000.0
```

**Output (my run):**
```text
price +10.0%, units -8.0%, simple elasticity -0.80, midpoint elasticity -0.875
revenue 50,000 -> 50,600 (+600); gross profit 20,000 -> 23,000 (+3,000, +15.0%)
revenue break-even units 4,545 (-9.1%); profit break-even units 4,000 (-20.0%)
stores per arm to detect -8% units: 154
if units had fallen 20% (profit-neutral): gross profit 20,000 vs 20,000 before
```

**Follow-ups:**
- What if the drop were 25%? Elasticity is -2.5, units 3,750, profit (5 x 3,750) = 18,750, which is less than 20,000. The rise stops paying.
- Which price is profit-maximising? With a constant-elasticity demand curve the optimum rises with margin; with only two points I cannot find it, so I test a second step.
- Elasticity is -0.8 so is it safe to raise again? Not automatically. The curve gets steeper, and competitors may react.

**Common mistakes:**
- Calling -0.8 "elasticity of 0.8" and dropping the sign.
- Computing profit change with revenue instead of margin.
- Treating the before/after as causal.
- Applying the +10% elasticity to a +30% move.

### Q2 ⭐⭐⭐ 🟢 A coupon of 10 off a 50 basket was sent to 10,000 customers and 3,000 of them ordered (30% of that group), while a randomly held-out 10,000 customers who got no coupon produced 2,000 orders (20% of that group). Gross margin before the coupon is 40% of the basket (20 per order), and every coupon order used the full 10 discount. Marketing says the campaign 'drove 3,000 orders', so work out whether it made or lost money and explain what the right comparison is.
**Asked at:** Promotion and incrementality material (Talon.One and Uniqodo pages on promotion ROI and incrementality, an INFORMS Management Science paper on whether coupons expand or cannibalise revenue, an incrmntal post on promos and ad spend); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The campaign lost money: against the holdout it added 1,000 orders but cost 30,000 in discounts, so it is 10,000 worse than doing nothing, even though 3,000 orders "came from it".

**Clarifying questions:**
- Was the holdout truly random, and was it the same customer pool? If not, the 20% is not a fair baseline.
- Is the 50 basket the same in both groups? A coupon sometimes lifts or shrinks the basket.
- Do coupon customers order less in the weeks after (pull-forward)? That would make the true effect even smaller.
- What is a new order worth over time (repeat orders)? It may justify some loss on the first order.
- Could we target the coupon to people unlikely to order without it? It changes the math.

**Approach:**
1. Say the right comparison: treated group against randomly held-out group, over the same period. Not "orders with coupon" against zero.
2. Compute incremental orders: 3,000 - 2,000 = 1,000 per 10,000 customers.
3. Compute margin per group: treated 3,000 x (20 - 10) = 30,000; control 2,000 x 20 = 40,000. Difference: -10,000.
4. Show the split: 20,000 of margin on the 1,000 extra orders, but 30,000 of discount, of which 20,000 went to customers who would have ordered anyway.
5. State the break-even: at a 10 discount, the coupon group needs a 40% order rate to match the control margin; it got 30%.
6. Then ask about long-term value of the new orders and about targeting.

**Metrics:**
- Incremental orders = treated orders - control orders (same group size).
- Incremental profit = treated margin after discounts - control margin.
- Cost per incremental order = total discount / incremental orders = 30,000 / 1,000 = 30.
- Guardrails: basket size, repeat purchase in the following 4 to 8 weeks, share of full-price orders lost.

**Risks:**
- "Orders driven" counts the 2,000 who would have ordered anyway (cannibalisation).
- Selection: if holdout was not random, any difference is suspect.
- Ignoring repeat value could make a good campaign look bad; ignoring pull-forward could do the opposite.
- The discount assumption (full 10 for every order) is as stated; real redemption can vary.

**What the interviewer scores:**
- Strong: compares against the holdout and gets -10,000. Weak: "3,000 orders x 20 margin = 60,000, profit."
- Strong: names cannibalisation and gives cost per incremental order. Weak: quotes lift without cost.
- Strong: gives the break-even order rate. Weak: only says "it seems unprofitable."
- Strong: raises repeat value and targeting as the next step. Weak: kills coupons forever.

**Example:** (illustrative numbers) 10,000 customers per group. Treated: 3,000 orders, margin per order 20 - 10 = 10, total 30,000. Control: 2,000 orders at 20, total 40,000. Net -10,000, which is -1.00 per customer. The 1,000 extra orders each lose 10 on the first order, so each needs about 10 of later margin to break even. Weak answer: "The coupon got 3,000 orders." Strong answer: "Only 1,000 were extra, and they cost 30 each; we lose 10,000."

**Code:**
```python
import math
from scipy import stats
n = 10_000
t_orders, c_orders = 3000, 2000
basket, margin, disc = 50, 20, 10
t_profit = t_orders * (margin - disc)
c_profit = c_orders * margin
print(f"treated margin after coupons {t_profit:,}; control margin {c_profit:,}; campaign effect {t_profit - c_profit:+,}")
assert (t_profit, c_profit, t_profit - c_profit) == (30000, 40000, -10000)
inc = t_orders - c_orders
print(f"incremental orders {inc:,} ({inc/c_orders:+.0%} relative); coupon cost {t_orders*disc:,}; margin on incremental orders {inc*margin:,}")
assert inc == 1000 and t_orders * disc == 30000 and inc * margin == 20000
print(f"loss per incremental order {(c_profit - t_profit)/inc:.1f}; give-away to would-have-ordered customers {c_orders*disc:,}")
be = c_profit / (n * (margin - disc))
print(f"break-even order rate in coupon group {be:.0%} (observed 30%)")
assert abs(be - 0.40) < 1e-12
# is the lift real? two-proportion z test
p = (t_orders + c_orders) / (2 * n)
z = (0.30 - 0.20) / math.sqrt(2 * p * (1 - p) / n)
print(f"z for 30% vs 20%: {z:.1f}  p = {2*stats.norm.sf(z):.2g}")
assert z > 15
# what would the discount need to be to break even at 30% vs 20%?
d_star = margin - c_profit / t_orders
print(f"largest break-even discount at these order rates: {d_star:.2f} per order")
assert abs(d_star - 6.6667) < 1e-3
```

**Output (my run):**
```text
treated margin after coupons 30,000; control margin 40,000; campaign effect -10,000
incremental orders 1,000 (+50% relative); coupon cost 30,000; margin on incremental orders 20,000
loss per incremental order 10.0; give-away to would-have-ordered customers 20,000
break-even order rate in coupon group 40% (observed 30%)
z for 30% vs 20%: 16.3  p = 6e-60
largest break-even discount at these order rates: 6.67 per order
```

**Follow-ups:**
- Marketing says new customers will repeat. How do you test it? Track the extra customers for several weeks and compare their repeat margin with the holdout; the loss is about 10 per extra order, so it needs to clear that.
- Would a smaller coupon work? At these order rates, a discount above about 6.67 loses money; but a smaller discount probably lowers the order rate too, so I test it.
- Is the lift real or noise? With 10,000 per group, 30% vs 20% is overwhelming (z about 16), so the problem is economics, not noise.

**Common mistakes:**
- Using total orders instead of incremental orders.
- Forgetting to subtract the discount from margin.
- Comparing with the same customers' history instead of a holdout.
- Applying the discount to only the incremental orders.

### Q3 ⭐⭐⭐ 🟢 A subscription app spent 1,200,000 on marketing and gained 6,000 paying customers, each worth 25 a month of gross margin, and 5% of the active customers cancel each month (5% of the active base, not of sign-ups). Compute CAC, the simple payback in months that ignores churn, the payback once churn is included, and the LTV-to-CAC ratio using margin divided by monthly churn. Say which payback you would quote.
**Asked at:** Lifetime-value and CAC material (a Dataford 'calculate customer lifetime value' product-growth-analyst page, Hacking the Case Interview, Road to Offer and MBB Prep pages on CLV and CAC, Count.co and FourWeekMBA CAC-payback pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** CAC is 200, simple payback is 8 months, but with 5% monthly churn payback is 10 months and LTV-to-CAC is 2.5; I would quote the churn-adjusted 10 months.

**Clarifying questions:**
- Is all 1,200,000 acquisition spend, or does it include brand and salaries? CAC must match what drove these 6,000.
- Are the 6,000 all paid customers, or do some come from organic sign-ups anyway? Paid CAC and blended CAC differ.
- Is 5% churn steady, or higher in the first months? Early churn makes payback longer.
- Is the 25 margin after servicing and payment fees? LTV is only as good as the margin.
- Do customers pay at the start of the month? It changes the payback by about one month.

**Approach:**
1. CAC = 1,200,000 / 6,000 = 200.
2. Simple payback = CAC / monthly margin = 200 / 25 = 8 months. This assumes nobody leaves.
3. Churn-adjusted payback: sum the expected margin month by month. A customer pays 25 in month 1, then survives each month with 95%. Cumulative margin per acquired customer is 184.88 after 9 months and 200.63 after 10, so payback is 10 months.
4. LTV = margin / churn = 25 / 0.05 = 500. LTV/CAC = 2.5.
5. Quote the churn-adjusted payback, plus LTV/CAC with its caveats (undiscounted, constant churn).
6. Check sensitivity: at 7% churn, LTV/CAC drops to 1.79 and payback to 12 months.

**Metrics:**
- CAC = acquisition spend / new paying customers.
- Simple payback (months) = CAC / monthly margin per customer.
- Churn-adjusted payback = first month n where the cumulative expected margin per acquired customer reaches CAC.
- LTV = monthly margin / monthly churn (undiscounted). LTV/CAC = LTV / CAC.
- Guardrails: cohort retention curve, payback by channel, cash tied up.

**Risks:**
- Churn is rarely constant; early churn is usually higher than the average implies.
- LTV = margin / churn is not discounted and runs forever; the tail is guesswork.
- Payback of 10 months is close to the edge (200.63 against 200), so small changes tip it.
- Blended CAC hides channels that are much better or worse.

**What the interviewer scores:**
- Strong: gets 200, 8, 10 and 2.5, and explains the gap between 8 and 10. Weak: stops at 8 months.
- Strong: states the convention for when the first margin arrives. Weak: does not say.
- Strong: picks the churn-adjusted payback and says why. Weak: quotes the flattering number.
- Strong: sensitivity to churn. Weak: treats 5% as a fact.

**Example:** (illustrative numbers) Cohort of 6,000. After 8 months the cohort has earned about 1,009,739 of margin, short of the 1,200,000 spend. After 10 months it has earned about 1,203,789. Weak answer: "Payback is 8 months, LTV/CAC is great." Strong answer: "Eight if nobody leaves; ten once churn is in; and LTV/CAC is 2.5, so not a comfortable margin for error."

**Code:**
```python
import math
spend, cust, m, churn = 1_200_000, 6000, 25.0, 0.05
cac = spend / cust
simple = cac / m
ltv = m / churn
print(f"CAC {cac:.0f}; simple payback {simple:.1f} months; LTV {ltv:.0f}; LTV/CAC {ltv/cac:.2f}")
assert cac == 200 and simple == 8 and ltv == 500 and abs(ltv / cac - 2.5) < 1e-12
# churn-adjusted payback: customer pays month 1 in full; each later month with survival 0.95^(k-1)
cum = 0.0; month = 0
while cum < cac:
    month += 1
    cum += m * (1 - churn) ** (month - 1)
    if month in (8, 9, 10): print(f"  month {month}: cumulative margin per acquired customer {cum:.2f}")
print(f"payback with churn: {month} months")
assert month == 10
closed = math.log(1 - cac * churn / m) / math.log(1 - churn)
print(f"closed form n = ln(1 - CAC*churn/margin)/ln(1-churn) = {closed:.2f}")
assert abs(closed - 9.96) < 0.01
# cohort view: 6,000 customers, cash back after 8 and 10 months
alive = [cust * (1 - churn) ** k for k in range(12)]
cash8 = sum(a * m for a in alive[:8]); cash10 = sum(a * m for a in alive[:10])
print(f"cohort margin after 8 months {cash8:,.0f}; after 10 months {cash10:,.0f}; spend {spend:,}")
assert cash8 < spend < cash10
# the limit: payback is impossible if CAC*churn >= margin
print(f"never pays back if CAC > margin/churn = {ltv:.0f}")
# sensitivity: churn 7% instead of 5%
c2 = 0.07
n2 = math.log(1 - cac * c2 / m) / math.log(1 - c2)
print(f"at 7% churn: LTV {m/c2:.0f}, LTV/CAC {m/c2/cac:.2f}, payback {math.ceil(n2)} months")
assert math.ceil(n2) == 12 and abs(m / c2 / cac - 1.786) < 0.001
```

**Output (my run):**
```text
CAC 200; simple payback 8.0 months; LTV 500; LTV/CAC 2.50
  month 8: cumulative margin per acquired customer 168.29
  month 9: cumulative margin per acquired customer 184.88
  month 10: cumulative margin per acquired customer 200.63
payback with churn: 10 months
closed form n = ln(1 - CAC*churn/margin)/ln(1-churn) = 9.96
cohort margin after 8 months 1,009,739; after 10 months 1,203,789; spend 1,200,000
never pays back if CAC > margin/churn = 500
at 7% churn: LTV 357, LTV/CAC 1.79, payback 12 months
```

**Follow-ups:**
- Why is the payback 10 and not 8? Because each month fewer customers are still paying, so the last months contribute less.
- What if CAC were 500? Then margin / churn = 500 equals CAC, and the customer never pays back in the formula's sense.
- What do you track after launch? The cohort retention curve; if month-1 churn is 10%, I recompute.

**Common mistakes:**
- Computing churn on sign-ups instead of the active base.
- Dividing LTV by CAC without checking that CAC covers all the spend.
- Using revenue instead of margin.
- Quoting LTV/CAC as a fact without discounting or confidence interval.

### Q4 ⭐⭐⭐ 🟢 A lender earns 150 of interest and fees on a 1,000 loan that is repaid and loses 600, net of recoveries, when it defaults. Compute the break-even probability of default (PD) above which an applicant should be declined, and the expected profit per loan at PDs of 5%, 20% and 30%. Explain what this simple rule leaves out that a real approval policy cannot ignore.
**Asked at:** Credit-risk material (a Dataford 'optimal cut-off score to maximise profit' page, an Interview Query auto-lending data scientist guide, a quintedge credit-risk interview page, academic papers on profit-maximising cut-offs); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Break-even PD is 20% (150 / (150 + 600)), expected profit per loan is +112.50, 0 and -75 at PDs of 5%, 20% and 30%, and the rule ignores calibration, adverse selection, volume, funding cost and fairness.

**Clarifying questions:**
- Is the 600 loss a fixed number or does it depend on the amount and recovery time? It moves the break-even.
- Is the 150 earned over the full term, or net of funding and servicing cost? Profit must be net.
- How good is the PD model: calibrated or only a ranking? The rule needs real probabilities.
- Is there a regulatory or fairness constraint on who can be declined? It limits the cut-off.
- Is the decision per loan or are there volume and capital limits? Limits change the cut-off.

**Approach:**
1. Write expected profit: (1 - PD) x 150 - PD x 600.
2. Set it to zero: PD = 150 / 750 = 20%.
3. Evaluate: at 5% it is 142.5 - 30 = +112.50; at 20% it is 0; at 30% it is 105 - 180 = -75.
4. Turn it into a score cut-off: approve while calibrated PD is below 20%.
5. List what is missing: calibration error, adverse selection (rejects not observed), pricing by risk, funding cost and capital, loss given default varying by customer, fairness and regulation, and approval volume.
6. Test the cut-off on a holdout with real outcomes, not only the training data.

**Metrics:**
- Expected profit per loan = (1 - PD) x gain - PD x loss.
- Break-even PD = gain / (gain + loss).
- Guardrails: approval rate, observed default rate by score band against predicted, share approved by segment.

**Risks:**
- If the model says 15% and the truth is 22.5%, the loan is approved but loses 18.75 on average.
- Approved-only data biases the PD model (reject inference problem).
- A higher loss (900 instead of 600) moves the break-even to 14.3%.
- PD alone ignores that a risky loan could be priced higher.

**What the interviewer scores:**
- Strong: 20% with the formula and the three profits. Weak: "decline above 50% PD."
- Strong: asks whether PDs are calibrated and tests the cut-off on holdout. Weak: treats model scores as true probabilities.
- Strong: names selection bias and risk-based pricing. Weak: only the formula.
- Strong: mentions fairness and regulation. Weak: ignores them.

**Example:** (illustrative numbers) Gain 150, loss 600. PD 5%: +112.50. PD 20%: 0.00. PD 30%: -75.00. If applicants were spread evenly from 0% to 40% PD, cutting at 20% earns about 150,075 across 4,001 applicants, against 112,612 at a 10% cut and 112,538 at 30%. Weak answer: "Decline anyone with PD over 20% and we are done." Strong answer: "20% if the PDs are calibrated, which I check by band on a holdout."

**Code:**
```python
gain, loss = 150.0, 600.0
be = gain / (gain + loss)
print(f"break-even PD = {gain}/({gain}+{loss}) = {be:.0%}")
assert abs(be - 0.20) < 1e-12
def ev(pd): return (1 - pd) * gain - pd * loss
for pd in (0.05, 0.20, 0.30):
    print(f"PD {pd:.0%}: expected profit per loan {ev(pd):+.2f}")
assert abs(ev(0.05) - 112.5) < 1e-9 and abs(ev(0.20)) < 1e-9 and abs(ev(0.30) + 75) < 1e-9
# calibration error: model says 15%, truth is 1.5x higher
pred, true = 0.15, 0.225
print(f"model says {pred:.0%} -> approve, expected {ev(pred):+.2f}; true {true:.1%} gives {ev(true):+.2f}")
assert ev(pred) > 0 > ev(true)
# portfolio view: PD uniformly spread 0-40%, cut at 20% vs cut at 10%
import numpy as np
pds = np.linspace(0, 0.4, 4001)
prof = lambda cut: sum(ev(p) for p in pds if p <= cut)
print(f"per 4,001 applicants (PD 0-40%): total profit cut 20% {prof(0.20):,.0f}; cut 10% {prof(0.10):,.0f}; cut 30% {prof(0.30):,.0f}")
assert prof(0.20) > prof(0.10) and prof(0.20) > prof(0.30)
# loss given default larger: 900 instead of 600 moves the cut-off
print(f"if loss is 900, break-even PD = {gain/(gain+900):.1%}")
assert abs(gain/(gain+900) - 0.142857) < 1e-5
```

**Output (my run):**
```text
break-even PD = 150.0/(150.0+600.0) = 20%
PD 5%: expected profit per loan +112.50
PD 20%: expected profit per loan +0.00
PD 30%: expected profit per loan -75.00
model says 15% -> approve, expected +37.50; true 22.5% gives -18.75
per 4,001 applicants (PD 0-40%): total profit cut 20% 150,075; cut 10% 112,612; cut 30% 112,538
if loss is 900, break-even PD = 14.3%
```

**Follow-ups:**
- What if the loss given default is 900? Break-even PD falls to 14.3%.
- Can you approve above 20% PD? Yes, if you raise the price enough so that gain per good loan covers the extra risk.
- How do you learn about declined applicants? Reject inference or a small controlled approval band; both have costs.

**Common mistakes:**
- Using (gain / loss) instead of gain / (gain + loss).
- Forgetting that a good loan earns only if it is repaid, so use (1 - PD).
- Treating model scores as calibrated probabilities.
- Ignoring that the approved population is not the applicant population.

### Q5 ⭐⭐⭐ 🟢 A marketplace has 200 million of annual GMV (gross merchandise value) and a take rate of 10% of GMV, so revenue is 20 million. Product wants a 12% take rate and expects GMV to fall by 8% relative to today's 200 million as sellers move some sales off the platform. Compute the new revenue and the relative GMV drop at which the increase stops paying, and say what you would measure to estimate the real drop.
**Asked at:** Marketplace and take-rate material (an inpractise take-rate course page, a Codemia Thumbtack data scientist guide describing a marketplace case round, ibinterviewquestions and hackingthecaseinterview marketplace and supply-demand pages); general marketplace guides, nothing specific to Uber, DoorDash or Swiggy loops; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** New revenue is 22.08 million (+2.08 million), and the increase stops paying at a relative GMV drop of 16.7%; the real drop is what I would measure with a controlled test.

**Clarifying questions:**
- Is the goal revenue or profit? The break-even changes if costs scale with GMV.
- Who bears the fee, buyer or seller? It decides who reacts.
- Can sellers easily move sales off the platform (repeat buyers, direct contact)? It drives the real drop.
- Is the 8% drop a forecast from past data or a guess? It decides how much I trust the answer.
- Is there a competing marketplace with a lower fee? Sellers may leave rather than shrink.

**Approach:**
1. Current revenue: 10% x 200 million = 20 million.
2. New revenue: 12% x 184 million (200 x 0.92) = 22.08 million, which is +10.4%.
3. Break-even drop: revenue is flat when 12% x GMV' = 20 million, so GMV' = 166.7 million, a drop of 1 - 10/12 = 16.7%.
4. Compare: the expected 8% drop is about half of the 16.7% the increase can absorb.
5. State the elasticity view: take rate up 20% relative; GMV down 8% is -0.4; break-even is -0.83.
6. Plan measurement: a randomised or geo/category-level test of the fee, tracking GMV, active sellers and off-platform leakage (repeat buyer-seller pairs that disappear).
7. Check profit: if costs fall with GMV (for example payments), the contribution break-even drop is looser; if not, tighter.

**Metrics:**
- Revenue = GMV x take rate.
- Relative GMV drop = (GMV' - GMV) / GMV.
- Break-even drop = 1 - old rate / new rate.
- Guardrails: active sellers, new-seller sign-ups, buyer repeat rate, share of repeat buyer-seller pairs that vanish from the platform.

**Risks:**
- The 8% drop may grow over time as sellers adapt (short-run versus long-run).
- A fee rise can reduce supply and so hurt buyers, a second-round effect not in the 8%.
- A segment (high-volume sellers) may leave much more than 8%, while the average hides it.
- Revenue is not profit.

**What the interviewer scores:**
- Strong: 22.08 million and 16.7% with the formula 1 - 10/12. Weak: says break-even is 12% / 10% - 1 = 20% (wrong direction).
- Strong: a plan to estimate the drop (test, leakage metric). Weak: "ask sellers."
- Strong: notes revenue is not profit and long-run effects. Weak: stops at revenue.
- Strong: segments the drop. Weak: uses the average.

**Example:** (illustrative numbers) GMV 200 million, take rate 10% to 12%. Drops of 5%, 8%, 12%, 16.7% and 20% give revenue of 22.80, 22.08, 21.12, 19.99 and 19.20 million. If variable costs are 2% of GMV, the contribution break-even drop is 20% instead. Weak answer: "Revenue goes up 20%." Strong answer: "Up 10.4% if the drop is 8%, and it only stops paying beyond about 17%."

**Code:**
```python
gmv, t0, t1, drop = 200e6, 0.10, 0.12, 0.08
r0 = gmv * t0
r1 = gmv * (1 - drop) * t1
print(f"revenue now {r0/1e6:.2f}m; new {r1/1e6:.2f}m ({r1/r0-1:+.1%}, {(r1-r0)/1e6:+.2f}m)")
assert abs(r0 - 20e6) < 1 and abs(r1 - 22.08e6) < 1
be_drop = 1 - t0 / t1
print(f"break-even GMV drop = 1 - 10/12 = {be_drop:.2%}; GMV at break-even {gmv*(1-be_drop)/1e6:.1f}m")
assert abs(be_drop - 1/6) < 1e-12
print(f"implied 'elasticity' of GMV to take rate: {(-drop)/(t1/t0-1):.2f}; break-even {(-be_drop)/(t1/t0-1):.2f}")
assert abs(drop / (t1 / t0 - 1) - 0.4) < 1e-12 and abs(be_drop / (t1 / t0 - 1) - 0.8333) < 1e-3
# contribution view: variable cost 2% of GMV (payment fees etc.), illustrative
v = 0.02
c0 = gmv * (t0 - v)
c1 = gmv * (1 - drop) * (t1 - v)
be2 = 1 - (t0 - v) / (t1 - v)
print(f"with variable cost {v:.0%} of GMV: contribution {c0/1e6:.1f}m -> {c1/1e6:.2f}m; break-even drop {be2:.1%}")
assert abs(be2 - 0.2) < 1e-12 and abs(c1 - 18.4e6) < 1
# table of outcomes
for d in (0.05, 0.08, 0.12, 0.167, 0.20):
    print(f"  drop {d:5.1%}: revenue {gmv*(1-d)*t1/1e6:5.2f}m")
assert gmv * (1 - 0.20) * t1 < r0 < gmv * (1 - 0.12) * t1
```

**Output (my run):**
```text
revenue now 20.00m; new 22.08m (+10.4%, +2.08m)
break-even GMV drop = 1 - 10/12 = 16.67%; GMV at break-even 166.7m
implied 'elasticity' of GMV to take rate: -0.40; break-even -0.83
with variable cost 2% of GMV: contribution 16.0m -> 18.40m; break-even drop 20.0%
  drop  5.0%: revenue 22.80m
  drop  8.0%: revenue 22.08m
  drop 12.0%: revenue 21.12m
  drop 16.7%: revenue 19.99m
  drop 20.0%: revenue 19.20m
```

**Follow-ups:**
- How would you estimate the real drop? Randomise the fee by seller cohort or region, compare GMV and active sellers against control, and watch for leakage.
- What if only large sellers react? Then I look at revenue by seller segment, because the average drop can hide a risky concentration.
- Would you raise it in one step? I would stage it (for example 11% first) so the test also reveals the curve.

**Common mistakes:**
- Using 20% (the take rate increase) as the break-even drop.
- Computing the drop on new GMV instead of the old.
- Equating revenue with profit.
- Taking the average drop across very different sellers.

### Q6 ⭐⭐⭐ 🟡 A payments firm processes 1,000,000 transactions a month, of which 0.5% (5,000, as a share of all transactions) are fraud with an average loss of 80. A model flags 20,000 transactions and stops 3,500 of the frauds. Every flagged transaction costs 2 to review and each flagged genuine customer costs an estimated 5 of lost future margin. Compute precision, recall and total monthly cost with and without the model, and say what would change your conclusion.
**Asked at:** Fraud-economics material (a Dataford 'evaluate fraud detection classifier' page with a limited review-capacity framing, DataRobot guidance on setting thresholds from false-negative versus false-positive cost, an Infosys BPM case study of a review-capacity cap, Sardine and other vendor pages on false positives); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Precision is 17.5% and recall 70%, and the model cuts the monthly cost from 400,000 to 242,500 (a saving of 157,500), but that depends on the 5 false-alarm cost and the 2 review cost.

**Clarifying questions:**
- Is "stops 3,500 frauds" measured after review, or does the model block automatically? It decides who pays the false-alarm cost.
- Is the 5 cost of a flagged genuine customer measured or guessed? It is the weakest number in the case.
- Is the average fraud loss of 80 the same for stopped and missed frauds? Missed ones are often larger.
- Can the team review 20,000 flags a month? Review capacity can cap the plan.
- Does fraud adapt to the model over time? Recall will not stay at 70%.

**Approach:**
1. Frauds: 1,000,000 x 0.5% = 5,000. Flagged: 20,000, of which 3,500 are fraud, so 16,500 are genuine.
2. Precision = 3,500 / 20,000 = 17.5%. Recall = 3,500 / 5,000 = 70%.
3. Cost without model: 5,000 x 80 = 400,000.
4. Cost with model: missed frauds 1,500 x 80 = 120,000, plus review 20,000 x 2 = 40,000, plus false alarms 16,500 x 5 = 82,500. Total 242,500.
5. Saving = 157,500 a month.
6. Test what would change it: break-even false-alarm cost is 14.55 (we assumed 5); break-even average fraud loss is 35 (we assumed 80).
7. Compare with a random 20,000 flags, which would catch about 100 frauds. The model is 35 times better than random.

**Metrics:**
- Precision = true frauds flagged / all flagged.
- Recall = true frauds flagged / all frauds.
- Total cost = missed fraud losses + review cost + false-alarm cost.
- Guardrails: false-alarm rate on good customers, approval rate, chargeback rate, drift in recall.

**Risks:**
- The 5 false-alarm cost is an estimate; if it were 15, the model would lose money.
- Fraudsters adapt, so recall in month 6 is unlikely to equal recall in month 1.
- "Frauds stopped" may be measured on labels that arrive late (chargebacks), so recall is itself uncertain.
- Precision of 17.5% looks poor in isolation but is 35 times the base rate.

**What the interviewer scores:**
- Strong: all four numbers (17.5%, 70%, 400,000, 242,500). Weak: quotes precision and recall only.
- Strong: includes review cost and false-alarm cost. Weak: counts only fraud losses.
- Strong: gives the break-even cost levers. Weak: "it depends."
- Strong: names adaptation and label delay. Weak: treats the 70% as permanent.

**Example:** (illustrative numbers) 1,000,000 transactions, 5,000 frauds. Model flags 20,000, catches 3,500. Cost without: 400,000. Cost with: 120,000 + 40,000 + 82,500 = 242,500. If it caught only 2,500 at the same 20,000 flags, the cost would be 327,500, still below 400,000. Weak answer: "Precision is only 17.5%, so the model is bad." Strong answer: "Each flag costs money, but the saving is 157,500; I would watch false-alarm cost and recall."

**Code:**
```python
N, fraud_rate, loss = 1_000_000, 0.005, 80
flag, tp, review, fp_cost = 20_000, 3_500, 2, 5
frauds = int(N * fraud_rate)
fp = flag - tp
prec, rec = tp / flag, tp / frauds
print(f"frauds {frauds:,}; flagged {flag:,}; true positives {tp:,}; false positives {fp:,}")
print(f"precision {prec:.1%}; recall {rec:.1%}")
assert frauds == 5000 and fp == 16500 and abs(prec - 0.175) < 1e-12 and abs(rec - 0.70) < 1e-12
cost_without = frauds * loss
missed = (frauds - tp) * loss
rev_cost = flag * review
fp_total = fp * fp_cost
cost_with = missed + rev_cost + fp_total
print(f"without model {cost_without:,}; with model: missed {missed:,} + review {rev_cost:,} + false-alarm {fp_total:,} = {cost_with:,}; saving {cost_without-cost_with:,}")
assert (cost_without, missed, rev_cost, fp_total, cost_with) == (400000, 120000, 40000, 82500, 242500)
assert cost_without - cost_with == 157500
# break-even false-alarm cost per flagged genuine customer
be_fp = (tp * loss - rev_cost) / fp
print(f"break-even false-alarm cost {be_fp:.2f} per flagged genuine customer (assumed 5)")
assert abs(be_fp - 14.5455) < 1e-3
# break-even fraud loss
be_loss = (rev_cost + fp_total) / tp
print(f"break-even average fraud loss {be_loss:.2f} (assumed 80)")
assert abs(be_loss - 35.0) < 1e-9
# random flagging of the same 20,000 would catch about
rand_tp = flag * fraud_rate
print(f"random 20,000 flags catch about {rand_tp:.0f} frauds; lift of the model = {prec/fraud_rate:.0f}x")
assert rand_tp == 100 and abs(prec / fraud_rate - 35) < 1e-9
# what if the model catches only 2,500 at the same 20,000 flags?
tp2 = 2500; c2 = (frauds - tp2) * loss + flag * review + (flag - tp2) * fp_cost
print(f"if only {tp2:,} caught: cost {c2:,} vs {cost_without:,} without")
assert c2 == 200000 + 40000 + 87500
```

**Output (my run):**
```text
frauds 5,000; flagged 20,000; true positives 3,500; false positives 16,500
precision 17.5%; recall 70.0%
without model 400,000; with model: missed 120,000 + review 40,000 + false-alarm 82,500 = 242,500; saving 157,500
break-even false-alarm cost 14.55 per flagged genuine customer (assumed 5)
break-even average fraud loss 35.00 (assumed 80)
random 20,000 flags catch about 100 frauds; lift of the model = 35x
if only 2,500 caught: cost 327,500 vs 400,000 without
```

**Follow-ups:**
- Would you raise the threshold? Only if the marginal flag costs more than it saves; I would compute the cost at several thresholds, not guess.
- How do you check recall? Review a random sample of unflagged transactions, because labels from chargebacks come late.
- What if reviewers can handle only 10,000 flags? Then review only the top-scored 10,000 and handle the rest automatically or with light friction.

**Common mistakes:**
- Forgetting to charge the review cost on true frauds too.
- Using 0.5% as precision.
- Counting the false-alarm cost only on blocked customers rather than all flagged genuine ones.
- Treating the saving as certain when one cost input is a guess.

### Q7 ⭐⭐⭐ 🟡 A bakery item costs 4 to make and sells at 10, and unsold items at close of day are sold off at 2. Daily demand is roughly normal with mean 100 and standard deviation 20. Compute the critical ratio and the number to bake, and say how the answer changes if the sell-off price is 0 and if sales data hide demand on days the item sells out.
**Asked at:** Forecasting and inventory material (PracHub retail demand-forecasting and inventory-and-stockout concept pages, a Dataford supermarket demand-forecasting page attributed in its title to a BCG data scientist interview but unverified, a PyCon DE 2025 talk on stockouts in retail forecasting); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Critical ratio is 0.75, so bake about 113 to 114 loaves (mean 100 plus 0.67 standard deviations); with zero sell-off it falls to 0.60 and about 105, and hidden demand on sell-out days makes a naive forecast stay stuck near 100.

**Clarifying questions:**
- Is demand really normal and stable day to day? Weekends and weather change the mean.
- Does a customer who finds it sold out leave, or substitute to another item? It changes the true cost of under-baking.
- Is the 4 cost the full cost, including ingredients, labour and oven time? The ratio depends on it.
- Are we recording sell-out times? They let me estimate the hidden demand.
- Can we bake a second batch mid-day? That changes the problem.

**Approach:**
1. Underage cost (profit lost per unit short) = 10 - 4 = 6. Overage cost (loss per unsold unit) = 4 - 2 = 2.
2. Critical ratio = 6 / (6 + 2) = 0.75.
3. Bake the 75th percentile of demand: 100 + 0.6745 x 20 = 113.5. In whole items, 113 or 114; a simulation puts 113 as best by a hair.
4. With sell-off price 0: overage cost = 4, ratio = 6 / 10 = 0.60, z = 0.2533, bake 105.1.
5. Explain the direction: lower salvage makes an unsold item costlier, so bake fewer.
6. Censoring: on sell-out days I see sales, not demand. If I forecast from sales, the mean looks lower (91.7 against 100) and the spread too narrow (12.1 against 20). Baking 100 each day, a naive plan stays stuck near 100 and never discovers the 113.5.
7. Fix: log sell-out times, fit a censored (Tobit-style) model, or sometimes bake more to learn demand.

**Metrics:**
- Critical ratio = underage cost / (underage cost + overage cost).
- Service level = probability demand is at or below the quantity baked.
- Expected profit per day = 10 x expected sales + 2 x expected leftovers - 4 x quantity.
- Guardrails: sell-out rate, leftover rate, sell-out time of day.

**Risks:**
- Normal approximation: demand cannot be negative, and real demand may be skewed.
- Lost sales have extra cost (customer goes elsewhere) not in the 6.
- Censoring biases the mean and the spread both downward.
- Mean and spread drift by weekday.

**What the interviewer scores:**
- Strong: 0.75, about 113.5, and the correct direction for sell-off 0 (0.60, about 105). Weak: "bake the mean."
- Strong: explains overage versus underage in money terms. Weak: quotes the formula without costs.
- Strong: spots censored demand and offers a fix. Weak: trusts sales as demand.
- Strong: recommends weekday-specific means. Weak: one number for every day.

**Example:** (illustrative numbers) Cost 4, price 10, sell-off 2, demand mean 100, sd 20. Baking 100 earns about 536.3 a day; baking 113 about 549.3. A year of sell-out data baking 100 shows sales of 91.7 on average and an sd of 12.1; a censored fit recovers a mean near 99 and sd near 20, giving a bake of about 112.5 (the true optimum is 113.5). Weak answer: "Bake 100, the average." Strong answer: "Bake the 75th percentile, about 113, and fix the forecast for sell-outs."

**Code:**
```python
import numpy as np
from scipy import stats, optimize
rng = np.random.default_rng(7)
cost, price, mu, sd = 4.0, 10.0, 100.0, 20.0
def plan(salvage):
    cu, co = price - cost, cost - salvage
    cr = cu / (cu + co)
    q = mu + stats.norm.ppf(cr) * sd
    return cu, co, cr, q
cu, co, cr, q = plan(2.0)
print(f"salvage 2: underage {cu:.0f}, overage {co:.0f}, critical ratio {cr:.2f}, z {stats.norm.ppf(cr):.4f}, bake {q:.1f}")
assert cr == 0.75 and abs(q - 113.49) < 0.01
cu0, co0, cr0, q0 = plan(0.0)
print(f"salvage 0: overage {co0:.0f}, critical ratio {cr0:.2f}, bake {q0:.1f}")
assert abs(cr0 - 0.6) < 1e-12 and abs(q0 - 105.07) < 0.01
# expected profit by integer Q on a big sample of demand (rounded, non-negative)
D = np.maximum(np.round(rng.normal(mu, sd, 400_000)), 0)
def profit(Q, salvage=2.0):
    return (price * np.minimum(D, Q) + salvage * np.maximum(Q - D, 0) - cost * Q).mean()
best = max(range(80, 140), key=profit)
print(f"best integer Q by simulation {best}; profit at 100: {profit(100):.1f}, at {best}: {profit(best):.1f}")
assert abs(best - 113.5) <= 1.5
# censoring: bake Q, observe sales = min(D, Q); naive plan uses mean/sd of sales
def naive_round(Q, days=365):
    d = rng.normal(mu, sd, days)
    s = np.minimum(d, Q)
    return s, d
Q = 100.0
path = [Q]
for r in range(6):
    s, _ = naive_round(Q)
    Q = s.mean() + stats.norm.ppf(0.75) * s.std()
    path.append(Q)
path = [float(x) for x in path]
print("naive plan path of Q:", [round(x, 1) for x in path])
assert all(abs(x - 100) < 4 for x in path)   # stuck near 100, never finds 113.5
# fix: Tobit-style maximum likelihood with censoring at Q (Q=100 for a year)
Qc = 100.0
d = rng.normal(mu, sd, 365); s = np.minimum(d, Qc); cens = d >= Qc
def nll(th):
    m, ls = th; sg = np.exp(ls)
    return -(stats.norm.logpdf(s[~cens], m, sg).sum() + stats.norm.logsf(Qc, m, sg) * cens.sum())
res = optimize.minimize(nll, [s.mean(), np.log(s.std())], method="Nelder-Mead")
m_hat, s_hat = res.x[0], np.exp(res.x[1])
print(f"sold out on {cens.mean():.0%} of days; naive mean {s.mean():.1f}, sd {s.std():.1f}; censored-MLE mean {m_hat:.1f}, sd {s_hat:.1f}")
assert s.mean() < 95 and 92 < m_hat < 108 and 14 < s_hat < 26
q_fix = m_hat + stats.norm.ppf(0.75) * s_hat
print(f"plan from censored estimate: bake {q_fix:.1f} (true optimum 113.5)")
assert abs(q_fix - 113.5) < 10
```

**Output (my run):**
```text
salvage 2: underage 6, overage 2, critical ratio 0.75, z 0.6745, bake 113.5
salvage 0: overage 4, critical ratio 0.60, bake 105.1
best integer Q by simulation 113; profit at 100: 536.3, at 113: 549.3
naive plan path of Q: [100.0, 99.7, 99.6, 100.0, 100.1, 99.5, 99.7]
sold out on 48% of days; naive mean 91.7, sd 12.1; censored-MLE mean 99.1, sd 19.9
plan from censored estimate: bake 112.5 (true optimum 113.5)
```

**Follow-ups:**
- Why does the 0 sell-off bake fewer? Each leftover now loses 4, not 2, so the cost of over-baking doubles.
- How would you handle weekday effects? Estimate mean and sd per weekday and compute the ratio for each.
- How do you get true demand? Record when the item sells out, or run occasional over-bake days to learn the tail.

**Common mistakes:**
- Baking the mean of demand.
- Using (price - cost) / price as the ratio (here 0.6) and forgetting the salvage value.
- Training a forecast on sales on sell-out days.
- Rounding down without checking the profit.

### Q8 ⭐⭐⭐ 🟡 A subscription business has 100,000 subscribers and a churn model. The top-scored 10,000 churn at 25% a month (2,500 churners, as a share of that group) and the next 10,000 at 10% (1,000 churners). A retention offer costs 4 per contacted subscriber and saves 20% of the would-be churners (a relative share of those churners), and a saved subscriber is worth 120. Compute the net value of contacting the top group, and of also contacting the second group, and name what the plan assumes.
**Asked at:** Churn and uplift material (Towards Data Science and Dataiku pages on churn models versus uplift models, a re-work blog post arguing that treatment, not churn prediction, is the goal, an arXiv paper on causal segmentation); practitioner and academic pages rather than a confirmed interview bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Contacting the top group nets +20,000; adding the second group adds -16,000 (the two groups together net +4,000), so I would contact only the top group, and the plan assumes a 20% save rate that is the same in both groups and has no side effects.

**Clarifying questions:**
- Is the 20% save rate from a randomised test or a guess? Everything depends on it.
- Is it the same for the 25% group and the 10% group? Save rates often differ by risk level.
- Does the offer have other costs (discount given to those who would have stayed)? The 4 may not cover it.
- Is 120 the margin over the saved customer's remaining life? Value assumptions decide the sign.
- Can the offer annoy people who were not going to leave (sleeping dogs)? It reduces the value.

**Approach:**
1. Top group: 10,000 x 25% = 2,500 would-be churners. Saved: 20% = 500. Value = 500 x 120 = 60,000. Cost = 10,000 x 4 = 40,000. Net +20,000.
2. Second group: 1,000 would-be churners, 200 saved, value 24,000, cost 40,000, net -16,000.
3. Contacting both: +20,000 - 16,000 = +4,000. The second group adds -16,000, so I would not add it.
4. Break-even churn rate = 4 / (0.20 x 120) = 16.7%. The top group is above it and the second below.
5. Name the assumptions: a constant 20% save rate, no harm to stayers, the saved subscribers stay (and are worth 120), and the churn rate predicts who the offer will work on.
6. Test the risk: break-even save rate in the top group is 13.3%; if 2.2% of would-be stayers are pushed to leave, the top group's gain reaches zero.
7. Next step: a randomised holdout to measure the save rate by group, then an uplift model.

**Metrics:**
- Net value = saved churners x value - contacted x cost.
- Saved churners = contacted x churn rate x save rate.
- Break-even churn = cost / (save rate x value).
- Guardrails: unsubscribe/complaint rate from the offer, the retention of the saved group at 3 months, spend on the offer.

**Risks:**
- A high churn score is not a high response: some people leave whatever you do (lost causes), some stay anyway.
- A 20% save rate of 25% churners may not hold at 10%.
- The offer may teach people to wait for a discount.
- Saved subscribers may leave a month later.

**What the interviewer scores:**
- Strong: +20,000 and -16,000, with the break-even churn rate. Weak: only computes the top group.
- Strong: says the save rate is an assumption and needs a holdout. Weak: treats 20% as known.
- Strong: distinguishes churn risk from treatment effect. Weak: "target high risk."
- Strong: gives a stopping rule (go down the list while marginal net is positive). Weak: "contact everyone."

**Example:** (illustrative numbers) Top group net +20,000; second group -16,000; both +4,000. If the save rate in the top group were only 10%, the net would be -10,000. With a 1% harm rate among the 7,500 would-be stayers, the top-group net falls from 20,000 to 11,000. Weak answer: "Contact both, the churn is real." Strong answer: "Top only, unless the second group's save rate is above 33%; and I need a holdout to confirm."

**Code:**
```python
import numpy as np
cost, save, value = 4.0, 0.20, 120.0
g1 = dict(n=10_000, churn=0.25)
g2 = dict(n=10_000, churn=0.10)
def net(g, save=save, cost=cost, value=value):
    churners = g["n"] * g["churn"]
    saved = churners * save
    return churners, saved, saved * value - g["n"] * cost
for name, g in (("top 10,000", g1), ("next 10,000", g2)):
    c, s, v = net(g)
    print(f"{name}: churners {c:,.0f}, saved {s:,.0f}, value {s*value:,.0f}, cost {g['n']*cost:,.0f}, net {v:+,.0f}")
v1, v2 = net(g1)[2], net(g2)[2]
assert (v1, v2) == (20000.0, -16000.0)
print(f"contact both: {v1+v2:+,.0f}  (second group adds {v2:+,.0f})")
assert v1 + v2 == 4000.0
be = cost / (save * value)
print(f"break-even churn rate for this offer = {cost}/({save}*{value}) = {be:.2%}")
assert abs(be - 1/6) < 1e-12 and g2["churn"] < be < g1["churn"]
# the plan assumes a 20% save rate that is the same in both groups; test lower save rate in the top group
for s in (0.10, 0.133, 0.20):
    print(f"  save rate {s:.1%} in top group: net {net(g1, save=s)[2]:+,.0f}")
assert abs(net(g1, save=0.10)[2] - (-10000)) < 1e-9
be_s = cost / (g1["churn"] * value)
print(f"break-even save rate in top group {be_s:.1%}")
assert abs(be_s - 0.1333) < 1e-3
# sleeping dogs: the offer pushes a small share of would-be stayers to leave (assumed harm)
stayers = g1["n"] * (1 - g1["churn"])
for h in (0.0, 0.01, 0.02):
    print(f"  harm rate {h:.0%} of stayers: top-group net {v1 - h*stayers*value:+,.0f}")
h_be = v1 / (stayers * value)
print(f"net reaches zero if {h_be:.2%} of would-be stayers are pushed to leave")
assert abs(v1 - 0.01 * stayers * value - 11000) < 1e-9 and abs(h_be - 0.02222) < 1e-4
```

**Output (my run):**
```text
top 10,000: churners 2,500, saved 500, value 60,000, cost 40,000, net +20,000
next 10,000: churners 1,000, saved 200, value 24,000, cost 40,000, net -16,000
contact both: +4,000  (second group adds -16,000)
break-even churn rate for this offer = 4.0/(0.2*120.0) = 16.67%
  save rate 10.0% in top group: net -10,000
  save rate 13.3% in top group: net -100
  save rate 20.0% in top group: net +20,000
break-even save rate in top group 13.3%
  harm rate 0% of stayers: top-group net +20,000
  harm rate 1% of stayers: top-group net +11,000
  harm rate 2% of stayers: top-group net +2,000
net reaches zero if 2.22% of would-be stayers are pushed to leave
```

**Follow-ups:**
- What save rate would make the second group worthwhile? 4 / (0.10 x 120) = 33.3%, which is not likely if the top group gets 20%.
- Why not just sort by churn score? Churn risk tells who will leave, not who will respond; uplift modelling targets the change in churn.
- How do you decide how deep to go? Go down the ranked list while the marginal net is positive, using measured save rates.

**Common mistakes:**
- Paying the cost only for churners rather than everyone contacted.
- Adding the group values and calling the second group positive.
- Treating the save rate as a fact.
- Forgetting the cost of saved subscribers who would have stayed anyway.

### Q9 ⭐⭐⭐ 🟡 A product team tests two monthly prices on 20,000 visitors each. The price of 99 converts 5.0% of visitors (1,000 subscribers) and the price of 129 converts 3.8% (760 subscribers), and serving a subscriber costs 30 a month. Compute revenue and contribution per visitor in each arm, and say what else beyond the first month you need before choosing a price.
**Asked at:** Subscription-tier and freemium material (a16z on optimising a free tier, a Frontiers in Psychology paper on a randomized freemium field experiment, getmonetizely and RevenueCat pricing-tier pages); mostly practitioner pages; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Revenue per visitor is almost the same (4.95 at 99 against 4.90 at 129), contribution is higher at 129 (3.76 against 3.45), but that gap is not significant yet and says nothing about retention beyond month one.

**Clarifying questions:**
- Were visitors randomly split and was the test run in the same weeks? Otherwise the arms are not comparable.
- Is 30 a month the only serving cost, or are there support and payment fees? It affects contribution.
- Do people pay monthly or annually, and how many cancel after month one? Lifetime value drives the choice.
- Do visitors see the other price anywhere? Price leakage would blur the result.
- Is there a free trial before paying? Conversion timing changes the read.

**Approach:**
1. Revenue per visitor: 99 x 5.0% = 4.950; 129 x 3.8% = 4.902.
2. Contribution per visitor: (99 - 30) x 5.0% = 3.450; (129 - 30) x 3.8% = 3.762. The higher price is +0.312, which is +9.0%.
3. Check noise: the standard error of the contribution difference is about 0.171, giving a 95% interval of -0.023 to +0.647 (p about 0.07). Not significant at the 5% level.
4. Revenue difference is -0.048 with an SE of 0.232 (p about 0.84), so revenue is a tie.
5. The conversion gap (5.0% against 3.8%) is clearly real (z about 5.9).
6. Beyond month one: retention by arm, refunds, support load, and upgrade or downgrade behaviour. Break-even: if the 99 price has 6% churn, the 129 price must have churn below about 6.5% to keep its lifetime edge.
7. Decide: run longer, or run a third price, and measure 3-month retention before switching.

**Metrics:**
- Revenue per visitor = price x conversion.
- Contribution per visitor = (price - serving cost) x conversion.
- Lifetime contribution per visitor = (price - cost) x conversion / monthly churn.
- Guardrails: refund rate, support tickets per subscriber, cancellations in the first 30 days.

**Risks:**
- Higher price can attract more committed buyers or more cancellations; month one shows neither.
- The contribution gap is within noise.
- Price anchoring and brand effects take longer than a test shows.
- Testing different prices to simultaneous visitors can create fairness complaints.

**What the interviewer scores:**
- Strong: both metrics, correct numbers, and says revenue and contribution point different ways. Weak: picks 99 on conversion alone.
- Strong: puts an interval on the contribution gap. Weak: "129 wins by 9%."
- Strong: asks for retention and lifetime. Weak: stops at month one.
- Strong: proposes a next test. Weak: ships.

**Example:** (illustrative numbers) 20,000 visitors per arm. 99: 1,000 subscribers, contribution 69,000 total, 3.45 per visitor. 129: 760 subscribers, 99 x 760 = 75,240 total, 3.762 per visitor. If churn at 129 is 9% against 6% at 99, lifetime contribution per visitor is 41.8 against 57.5, which reverses the winner. Weak answer: "129 earns 9% more, switch." Strong answer: "Within noise in month one, and the answer depends on churn; I want retention data."

**Code:**
```python
import math
from scipy import stats
n = 20_000
arms = {"99": (99.0, 1000), "129": (129.0, 760)}
serve = 30.0
res = {}
for k, (price, subs) in arms.items():
    conv = subs / n
    rev = price * conv
    con = (price - serve) * conv
    res[k] = (conv, rev, con)
    print(f"price {k}: conversion {conv:.1%}, revenue/visitor {rev:.3f}, contribution/visitor {con:.3f}")
assert abs(res["99"][1] - 4.95) < 1e-9 and abs(res["129"][1] - 4.902) < 1e-9
assert abs(res["99"][2] - 3.45) < 1e-9 and abs(res["129"][2] - 3.762) < 1e-9
print(f"revenue difference (129 - 99) {res['129'][1]-res['99'][1]:+.3f}; contribution difference {res['129'][2]-res['99'][2]:+.3f} ({res['129'][2]/res['99'][2]-1:+.1%})")
def diff_test(m_a, p_a, m_b, p_b):
    d = m_b * p_b - m_a * p_a
    se = math.sqrt(m_a**2 * p_a * (1 - p_a) / n + m_b**2 * p_b * (1 - p_b) / n)
    return d, se, d / se, 2 * stats.norm.sf(abs(d / se))
pa, pb = 0.05, 0.038
d, se, z, p = diff_test(69, pa, 99, pb)
print(f"contribution: diff {d:.3f}, SE {se:.3f}, 95% CI {d-1.96*se:.3f} to {d+1.96*se:.3f}, z {z:.2f}, p {p:.3f}")
assert p > 0.05 and d - 1.96 * se < 0
d2, se2, z2, p2 = diff_test(99, pa, 129, pb)
print(f"revenue: diff {d2:.3f}, SE {se2:.3f}, z {z2:.2f}, p {p2:.2f}")
assert p2 > 0.5
# conversion difference itself
pp = (pa + pb) / 2
zc = (pa - pb) / math.sqrt(2 * pp * (1 - pp) / n)
print(f"conversion 5.0% vs 3.8%: z {zc:.1f}, p {2*stats.norm.sf(zc):.1e}")
assert zc > 5
# lifetime: higher price may churn faster. Margin per subscriber per month 69 vs 99.
for c99, c129 in ((0.06, 0.06), (0.06, 0.09), (0.06, 0.12)):
    l99 = 69 * pa / c99; l129 = 99 * pb / c129
    print(f"monthly churn {c99:.0%} vs {c129:.0%}: lifetime contribution/visitor {l99:.1f} vs {l129:.1f}")
c_be = 99 * pb / (69 * pa) * 0.06
print(f"129 stays better only if its churn is below {c_be:.1%} when 99 churns 6.0%")
assert abs(c_be - 0.0654) < 1e-3
# visitors needed per arm to see a 0.312 difference with SD about 0.17*sqrt(20000)
sd_pooled = se * math.sqrt(n) / math.sqrt(2)
need = 2 * ((1.96 + 0.84) * sd_pooled / d) ** 2
print(f"visitors per arm for 80% power at the observed difference: {need:,.0f}")
assert 40_000 < need < 100_000
```

**Output (my run):**
```text
price 99: conversion 5.0%, revenue/visitor 4.950, contribution/visitor 3.450
price 129: conversion 3.8%, revenue/visitor 4.902, contribution/visitor 3.762
revenue difference (129 - 99) -0.048; contribution difference +0.312 (+9.0%)
contribution: diff 0.312, SE 0.171, 95% CI -0.023 to 0.647, z 1.83, p 0.068
revenue: diff -0.048, SE 0.232, z -0.21, p 0.84
conversion 5.0% vs 3.8%: z 5.9, p 4.9e-09
monthly churn 6% vs 6%: lifetime contribution/visitor 57.5 vs 62.7
monthly churn 6% vs 9%: lifetime contribution/visitor 57.5 vs 41.8
monthly churn 6% vs 12%: lifetime contribution/visitor 57.5 vs 31.4
129 stays better only if its churn is below 6.5% when 99 churns 6.0%
visitors per arm for 80% power at the observed difference: 47,070
```

**Follow-ups:**
- How many visitors to settle it? About 47,000 per arm to detect a gap this size with 80% power (from the code).
- Why might revenue and contribution disagree? Contribution subtracts the 30 serving cost per subscriber, so fewer subscribers at a higher price are cheaper to serve.
- Would you test a third price? Yes, for example 109, to see the shape of the curve.

**Common mistakes:**
- Choosing by conversion rate alone.
- Ignoring serving cost.
- Calling a 9% gap significant without an interval.
- Looking only at month one.

### Q10 ⭐⭐⭐ 🟡 A support team handles 60,000 tickets a month at 5.00 per human ticket (300,000 in total). An LLM agent attempts every ticket at 0.20 and resolves 40% of them (24,000 tickets, 40% of all tickets), 15% of the AI-resolved tickets reopen and go to a human at 5.00, and the 36,000 escalated tickets cost 5.50 each because the human must read the failed chat. The platform fee is 40,000 a month. Compute the monthly saving and say what you would measure besides cost.
**Asked at:** AI-era support and GenAI cost material (2026 vendor and practitioner pages from Lorikeet, Twig, Voiceflow, aitimejournal, CloudZero, nOps, tianpan.co and a Gartner press-release headline on inference costs); mostly vendor-sourced, an emerging interview theme rather than a confirmed bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The AI setup costs 268,000 against 300,000, a saving of 32,000 a month (10.7%), which is thin, so I would measure resolution that stays resolved, customer satisfaction and escalation cost before trusting it.

**Clarifying questions:**
- Is the 40% resolution rate measured on all tickets or on easy ones only? Hard tickets may be pushed to the AI later.
- Are reopened tickets handled at 5.00 or 5.50 (the human must read the chat in both cases)? It changes the saving by 1,800.
- Does the 0.20 per ticket include every model call, including retries and long chats? Costs often creep up.
- Is the platform fee fixed or per volume? It decides how the saving scales.
- What happens to customer satisfaction on tickets the AI fails? A cheap miss can be an expensive churn.

**Approach:**
1. Baseline: 60,000 x 5.00 = 300,000.
2. AI cost: 60,000 x 0.20 = 12,000.
3. Resolved: 24,000. Reopened: 15% of 24,000 = 3,600, at 5.00 = 18,000.
4. Escalated: 60,000 - 24,000 = 36,000, at 5.50 = 198,000.
5. Platform fee: 40,000.
6. Total: 12,000 + 18,000 + 198,000 + 40,000 = 268,000. Saving = 32,000 a month.
7. Sensitivity: if reopened tickets also cost 5.50, saving is 30,200. Break-even resolution rate is 28.8%; at a 50% reopen rate the saving at 40% resolution turns negative (-10,000).
8. Measure beyond cost: truly resolved rate, CSAT, repeat contacts, time to resolution, wrong-answer harm (refunds, complaints).

**Metrics:**
- Monthly saving = baseline cost - AI-assisted cost.
- Net containment = (AI-resolved - reopened) / all tickets = 20,400 / 60,000 = 34%.
- Cost per truly resolved ticket (AI side) = (AI cost + platform fee) / truly resolved tickets.
- Guardrails: CSAT on AI-touched tickets, reopen rate, escalation rate, share of tickets with a wrong or harmful answer.

**Risks:**
- A 40% resolution rate that includes tickets the customer abandoned is not a resolution.
- A 5.50 escalated ticket is slower and more annoying for the customer; satisfaction can fall.
- Saving is only 10.7% and sensitive to the reopen rate and the resolution rate.
- Model price changes or longer conversations raise the 0.20.

**What the interviewer scores:**
- Strong: 268,000 and 32,000, with each line shown. Weak: 40% of 300,000 = 120,000 saving.
- Strong: notices escalated tickets cost more than human-only tickets. Weak: ignores it.
- Strong: gives the break-even resolution rate and the reopen sensitivity. Weak: "it depends."
- Strong: asks for quality metrics, not only cost. Weak: only cost.

**Example:** (illustrative numbers) Resolved 24,000, reopened 3,600, escalated 36,000: human-touched tickets 39,600 of 60,000. Truly resolved 20,400 (34%). AI-side cost per truly resolved ticket is 2.55. At 28.8% resolution the saving is zero; at 0% it is -82,000. Weak answer: "AI resolves 40% so we save 40%." Strong answer: "We save 32,000 because failed chats make human work cost more and a platform fee eats the rest."

**Code:**
```python
T = 60_000
human, ai, esc, reopen_cost, fee = 5.00, 0.20, 5.50, 5.00, 40_000
res_rate, reopen = 0.40, 0.15
base = T * human
resolved = T * res_rate
reopened = resolved * reopen
escalated = T - resolved
print(f"baseline {base:,.0f}; resolved {resolved:,.0f}; reopened {reopened:,.0f}; escalated {escalated:,.0f}")
assert base == 300000 and resolved == 24000 and reopened == 3600 and escalated == 36000
parts = dict(ai=T * ai, reopened=reopened * reopen_cost, escalated=escalated * esc, fee=fee)
for k, v in parts.items(): print(f"  {k:10s} {v:>10,.0f}")
total = sum(parts.values())
print(f"AI-assisted total {total:,.0f}; monthly saving {base-total:,.0f} ({(base-total)/base:.1%})")
assert total == 268000 and base - total == 32000
print(f"human-touched tickets {escalated+reopened:,.0f} of {T:,}; truly resolved {resolved-reopened:,.0f} ({(resolved-reopened)/T:.0%})")
assert escalated + reopened == 39600 and (resolved - reopened) / T == 0.34
# if reopened tickets also cost 5.50 (human must read the failed chat)
alt = parts["ai"] + reopened * esc + parts["escalated"] + fee
print(f"if reopened tickets cost 5.50 too: saving {base-alt:,.0f}")
assert base - alt == 30200
def saving(r, rp=reopen):
    return base - (T*ai + T*r*rp*reopen_cost + T*(1-r)*esc + fee)
be = next(r/10000 for r in range(0, 10001) if saving(r/10000) >= 0)
print(f"break-even resolution rate {be:.1%}; at 0% resolution the saving is {saving(0):,.0f}; at 60% {saving(0.6):,.0f}")
assert abs(be - 0.2878) < 0.0002
for rp in (0.15, 0.30, 0.50):
    print(f"  reopen rate {rp:.0%}: saving at 40% resolution {saving(0.4, rp):,.0f}")
assert saving(0.4, 0.50) < saving(0.4, 0.15)
# cost per AI-resolved-and-stayed-resolved ticket
print(f"AI-side cost per truly resolved ticket: {(T*ai+fee)/(resolved-reopened):.2f}")
```

**Output (my run):**
```text
baseline 300,000; resolved 24,000; reopened 3,600; escalated 36,000
  ai             12,000
  reopened       18,000
  escalated     198,000
  fee            40,000
AI-assisted total 268,000; monthly saving 32,000 (10.7%)
human-touched tickets 39,600 of 60,000; truly resolved 20,400 (34%)
if reopened tickets cost 5.50 too: saving 30,200
break-even resolution rate 28.8%; at 0% resolution the saving is -82,000; at 60% 89,000
  reopen rate 15%: saving at 40% resolution 32,000
  reopen rate 30%: saving at 40% resolution 14,000
  reopen rate 50%: saving at 40% resolution -10,000
AI-side cost per truly resolved ticket: 2.55
```

**Follow-ups:**
- What would raise the saving most? A higher true resolution rate or a lower reopen rate; each 10 points of resolution is worth about 28,500 a month.
- Would you route by ticket type? Yes, let the AI handle the types it resolves well and send the rest straight to humans without the failed-chat penalty.
- How do you check the 40%? A sample of AI-closed tickets reviewed by a human, plus customer follow-up.

**Common mistakes:**
- Forgetting the platform fee.
- Applying 5.00 to escalated tickets and ignoring the 5.50.
- Treating all 24,000 as resolved.
- Looking only at cost and ignoring satisfaction.

### Q11 ⭐⭐⭐ 🟡 An ad platform reports 400,000 of attributed revenue on 100,000 of spend, a ROAS of 4.0. A geo holdout in which comparable regions had the ads switched off shows only 120,000 of incremental revenue over the same period, and gross margin is 30% of revenue. Compute the incremental ROAS and the profit on the spend, and say how you would argue for your recommendation.
**Asked at:** Marketing measurement material (a datainterview.com paid-social incrementality case, an aitrainer.work marketing data scientist question page, Triple Whale and Eppo GeoLift pages, a Medium post on geo-experiments, a PyData Boston 2025 talk description); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Incremental ROAS is 1.2, not 4.0, and at a 30% margin that is a loss of 64,000 on 100,000 of spend; I would argue to cut or restructure the spend, backed by the holdout.

**Clarifying questions:**
- How were the holdout regions chosen and matched? A bad match makes the 120,000 unreliable.
- How long did the test run, and did sales carry over after it ended? Ad effects can lag.
- What is the uncertainty on the 120,000? I need an interval before cutting a large budget.
- Is the 30% margin the right contribution (after returns and fulfilment)? It decides the break-even.
- Do these ads help other channels (brand, search)? Leakage could understate the effect.

**Approach:**
1. Platform ROAS = 400,000 / 100,000 = 4.0. It counts every sale the platform can attribute, including ones that would have happened anyway.
2. Incremental ROAS = 120,000 / 100,000 = 1.2. Only 30% of the attributed revenue was caused by the ads.
3. Profit on spend = 120,000 x 30% - 100,000 = -64,000. (If the platform number were true: 400,000 x 30% - 100,000 = +20,000.)
4. Break-even incremental ROAS = 1 / 0.30 = 3.33, which needs 333,333 of incremental revenue. We are at 120,000.
5. Add uncertainty: under an assumed standard error of 40,000, the 95% interval for incremental revenue is 41,600 to 198,400, and every plausible value loses money. The break-even needs about 109,000 of standard error before the call is open.
6. Check long-run effects: even with a generous 50% carry-over, iROAS is 1.80 and the profit is -46,000.
7. Recommend: cut the spend sharply, keep a small always-on holdout, and re-test by campaign or region to find the pockets with iROAS above 3.33.

**Metrics:**
- ROAS = attributed revenue / spend. Incremental ROAS = incremental revenue (test minus control, scaled) / spend.
- Profit on spend = incremental revenue x margin - spend.
- Break-even iROAS = 1 / margin.
- Guardrails: total revenue in the holdout regions, new-customer share, brand search volume.

**Risks:**
- The geo test may be noisy or badly matched; always show an interval.
- Ads may have effects after the test window.
- The cut may hurt brand-building we cannot measure.
- Marginal iROAS (the next dollar) can differ from average iROAS.

**What the interviewer scores:**
- Strong: 1.2, -64,000, and the break-even 3.33. Weak: "ROAS is 4, so profitable."
- Strong: explains attribution versus causation. Weak: trusts platform numbers.
- Strong: addresses uncertainty and carry-over before recommending a cut. Weak: recommends without an interval.
- Strong: a staged action (cut, holdout, re-test). Weak: kill all advertising.

**Example:** (illustrative numbers) Spend 100,000. Attributed 400,000, incremental 120,000. At 30% margin the ads return 36,000 of margin on 100,000 spend. To break even they would need 333,333 of incremental revenue. Weak answer: "ROAS of 4.0, scale it up." Strong answer: "Only 30% of those sales were caused by the ads; they lose 64,000, so I would cut and re-test."

**Code:**
```python
import numpy as np
spend, attributed, incr, gm = 100_000.0, 400_000.0, 120_000.0, 0.30
roas, iroas = attributed / spend, incr / spend
print(f"ROAS {roas:.1f}; incremental ROAS {iroas:.1f}")
assert roas == 4.0 and abs(iroas - 1.2) < 1e-12
profit_inc = incr * gm - spend
profit_attr = attributed * gm - spend
print(f"profit on spend: incremental {profit_inc:+,.0f}; if platform number were true {profit_attr:+,.0f}")
assert abs(profit_inc + 64000) < 1e-9 and abs(profit_attr - 20000) < 1e-9
be_iroas = 1 / gm
print(f"break-even iROAS = 1/{gm} = {be_iroas:.2f}; incremental revenue needed {spend*be_iroas:,.0f}; break-even margin at iROAS 1.2 = {1/iroas:.0%}")
assert abs(be_iroas - 3.3333) < 1e-3 and abs(1 / iroas - 0.8333) < 1e-3
print(f"share of attributed revenue that was incremental: {incr/attributed:.0%}")
assert incr / attributed == 0.30
# illustrative measurement noise: the geo estimate has SE 40,000 (assumed); simulate
rng = np.random.default_rng(11)
se = 40_000.0
draws = rng.normal(incr, se, 100_000)
print(f"with SE {se:,.0f}: 95% interval for incremental revenue {incr-1.96*se:,.0f} to {incr+1.96*se:,.0f}")
p_profit = (draws * gm > spend).mean()
print(f"share of draws with a profit (incremental revenue above {spend*be_iroas:,.0f}): {p_profit:.4f}")
assert (incr + 1.96 * se) * gm < spend and p_profit < 0.001
# how large would the SE have to be before the call is open?
se_open = (spend * be_iroas - incr) / 1.96
print(f"upper 95% bound reaches break-even only if SE >= {se_open:,.0f}")
assert abs(se_open - 108843) < 1
# if ads also have a 3-month carry-over worth +50% of in-period incremental revenue
print(f"even with +50% carry-over, iROAS {iroas*1.5:.2f} and profit {incr*1.5*gm-spend:+,.0f}")
assert incr * 1.5 * gm - spend < 0
```

**Output (my run):**
```text
ROAS 4.0; incremental ROAS 1.2
profit on spend: incremental -64,000; if platform number were true +20,000
break-even iROAS = 1/0.3 = 3.33; incremental revenue needed 333,333; break-even margin at iROAS 1.2 = 83%
share of attributed revenue that was incremental: 30%
with SE 40,000: 95% interval for incremental revenue 41,600 to 198,400
share of draws with a profit (incremental revenue above 333,333): 0.0000
upper 95% bound reaches break-even only if SE >= 108,844
even with +50% carry-over, iROAS 1.80 and profit -46,000
```

**Follow-ups:**
- The marketing lead says the test is too small. What do you do? Ask for the interval; with a standard error of 40,000 the conclusion holds, and it would take about 109,000 before it flips. If it were that noisy, I would extend the test.
- Would you cut to zero? No. The marginal return of the first dollars may be higher; I would cut in steps and keep a holdout.
- How do you scale a geo result to the whole market? Use the ratio of incremental to spent in test regions and apply the same ratio, noting the market may differ.

**Common mistakes:**
- Using platform-attributed revenue as incremental.
- Comparing ROAS to 1 instead of to 1 / margin.
- Ignoring margin and calling revenue profit.
- Cutting on a single noisy test without an interval.

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

### Q34 ⭐⭐ 🟡 Personalised email subject lines lift the click rate from 2.0% to 2.2% of 5,000,000 weekly emails (0.2 points absolute, 10% relative to 2.0%), and each extra click earns 3.00 of margin. The model costs 15,000 a week to run, and unsubscribes rise from 0.10% to 0.12% of emails (0.02 points absolute), with each lost subscriber worth 12 of future margin. Compute the net weekly value and say which figure is shakiest.
**Asked at:** Recommender and personalisation business-value material (a Jannach and Jugovac arXiv survey on the business value of recommenders, a Smart Insights personalisation case, vendor case studies from Blast Analytics and Recolize that report self-claimed ROI); vendor numbers are upper bounds; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The arithmetic gives +30,000 of click margin, minus 15,000 of model cost, minus 12,000 of lost subscribers, so net +3,000 a week; the shakiest figure is the 3.00 margin per extra click, because a thin 3,000 disappears if that is only 10% too high.

**Clarifying questions:**
- Was this a randomized holdout (personalised versus generic subject line), and how many emails per arm? It tells me whether the 0.2 point lift is real or noise.
- What is the 3.00 per click: measured order margin from a click, or an assumed average? It is the biggest driver of the answer.
- Are the extra clicks incremental sales or the same buyers who would have bought anyway? Clicks are not orders.
- Is the 12 per lost subscriber a measured value, or the average subscriber value? Unsubscribers are often below-average buyers.
- Does the effect hold over weeks, or is it a novelty effect that fades? A fading lift turns a small plus into a minus.

**Approach:**
1. Convert rates to counts: 0.2 points of 5,000,000 = 10,000 extra clicks. 0.02 points of 5,000,000 = 1,000 extra unsubscribes.
2. Value each side: 10,000 x 3.00 = 30,000. 1,000 x 12 = 12,000.
3. Net = 30,000 - 15,000 - 12,000 = 3,000 a week.
4. Stress the weakest input: break-even margin per click is (15,000 + 12,000) / 10,000 = 2.70, only 10% below the 3.00 assumed.
5. Check noise on both rates (counts are large, so noise is not the problem; the valuation is).
6. Recommend: ship only to segments where lift per email is highest, and measure orders and 8-week unsubscribes in a holdout before scaling.

**Metrics:**
- Net weekly value = (extra clicks x margin per click) - model cost - (extra unsubscribes x value per subscriber).
- Click rate = clicks / emails delivered. Unsubscribe rate = unsubscribes / emails delivered.
- Better primary metric: incremental margin per email sent, from a holdout.
- Guardrails: spam complaints, unsubscribes, and order margin per recipient over 4-8 weeks.

**Risks:**
- Clicks are a proxy. Curiosity clicks on a catchy subject line may not buy.
- The unsubscribe cost is understated if unsubscribers include your best customers, and overstated if they were inactive.
- Novelty: subject-line gains often decay.
- Using relative lift (10%) instead of absolute (0.2 points) makes the gain sound bigger than it is in money.

**What the interviewer scores:**
- Strong: converts rates to counts and shows both gain and loss. Weak: "click rate went up 10%, ship it."
- Strong: finds the break-even margin per click (2.70). Weak: names "uncertainty" with no number.
- Strong: names clicks-to-orders as the shakiest link and asks for a holdout on orders. Weak: trusts the click margin.
- Strong: notes the net is small against its uncertainty. Weak: reports 3,000 as a firm win.

**Example:** (illustrative numbers) 5,000,000 emails, 10,000 extra clicks, 1,000 extra unsubscribes. At 3.00 a click the net is +3,000. At 2.70 it is 0. At 2.00 it is -7,000. Weak answer: "+3,000 a week, ship." Strong answer: "+3,000 only if a click is truly worth 3.00; I want measured order margin before I call it a win."

**Code:**
```python
import math
emails = 5_000_000
clicks_base, clicks_new = 0.020 * emails, 0.022 * emails
extra_clicks = clicks_new - clicks_base
click_value = extra_clicks * 3.00
unsub_extra = (0.0012 - 0.0010) * emails
unsub_cost = unsub_extra * 12
cost = 15_000
net = click_value - cost - unsub_cost
print(f"extra clicks {extra_clicks:,.0f}; click margin {click_value:,.0f}")
print(f"extra unsubscribes {unsub_extra:,.0f}; future margin lost {unsub_cost:,.0f}")
print(f"net weekly value {net:,.0f}")
assert round(extra_clicks) == 10_000 and round(click_value) == 30_000
assert round(unsub_extra) == 1_000 and round(unsub_cost) == 12_000
assert round(net) == 3_000
assert abs(0.022 / 0.020 - 1 - 0.10) < 1e-9
be = (cost + unsub_cost) / extra_clicks
print(f"break-even margin per extra click {be:.2f}")
assert abs(be - 2.70) < 1e-9
for m in (3.00, 2.70, 2.00):
    print(f"  margin/click {m:.2f} -> net {extra_clicks*m - cost - unsub_cost:,.0f}")
# noise check, assuming (illustrative) 2.5M emails per arm
n = emails / 2
def z(p1, p2):
    p = (p1 + p2) / 2
    return (p2 - p1) / math.sqrt(2 * p * (1 - p) / n)
zc, zu = z(0.020, 0.022), z(0.0010, 0.0012)
print(f"z for clicks {zc:.1f}, z for unsubscribes {zu:.1f} (2.5M per arm, assumed)")
assert zc > 10 and zu > 5
# thin cushion: a 10% miss on the click value flips the sign
print(f"net if click value is 10% lower: {0.9*click_value - cost - unsub_cost:,.0f}")
assert abs(0.9 * click_value - cost - unsub_cost) < 1e-6
```

**Output (my run):**
```text
extra clicks 10,000; click margin 30,000
extra unsubscribes 1,000; future margin lost 12,000
net weekly value 3,000
break-even margin per extra click 2.70
  margin/click 3.00 -> net 3,000
  margin/click 2.70 -> net 0
  margin/click 2.00 -> net -7,000
z for clicks 15.6, z for unsubscribes 6.7 (2.5M per arm, assumed)
net if click value is 10% lower: 0
```

**Follow-ups:**
- Which number would you measure next? Incremental orders per recipient over 4-8 weeks in a holdout, because it replaces both the click margin and the subscriber value.
- Would you scale it? Only to segments with the highest lift per email; the model cost of 15,000 is fixed, so volume helps, but so does a worse unsubscribe tail.

**Common mistakes:**
- Quoting the 10% relative lift as the headline.
- Forgetting the unsubscribe cost or the model cost.
- Treating a click as an order.
- Calling the result significant without saying what the two rates were compared on.

### Q35 ⭐⭐ 🟡 A search relevance change cut the share of searches with no useful result from 8% to 6% of 10,000,000 daily searches (2 points absolute, 25% relative to 8%). A search that now gets a useful result converts to an order 3.0% of the time against 0.5% for one that does not, and an order earns 4.00 of margin. Compute the extra daily margin and explain why it is an upper bound.
**Asked at:** Recommender and personalisation business-value material (a Jannach and Jugovac arXiv survey on the business value of recommenders, a Smart Insights personalisation case, vendor case studies from Blast Analytics and Recolize that report self-claimed ROI); vendor numbers are upper bounds; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** 2 points of 10,000,000 searches is 200,000 searches a day that now get a useful result; at a 2.5 point conversion gap that is 5,000 orders and 20,000 of margin a day, and it is an upper bound because the rescued searches are not the same people as the ones who already got good results.

**Clarifying questions:**
- How is "useful result" defined: clicks, judged relevance, or a model label? A metric that is easy to move may not mean the user is satisfied.
- Was the change A/B tested, and did the orders per search rise in the test arm? Direct orders beat a rate table.
- Is the 3.0% versus 0.5% a causal gap or just two observed groups? It is observed, so it is confounded by intent.
- What kind of queries moved from no-result to useful (head or rare tail)? Tail queries usually have lower buying intent.
- Is the order margin of 4.00 the same on those rescued orders? Rescued items may be cheaper or lower-margin.

**Approach:**
1. Searches moved = 10,000,000 x (8% - 6%) = 200,000 a day.
2. Conversion gap = 3.0% - 0.5% = 2.5 points, so extra orders = 200,000 x 2.5% = 5,000.
3. Margin = 5,000 x 4.00 = 20,000 a day.
4. Explain "upper bound": the 3.0% is the rate for searches that were useful already, which includes shoppers with high intent. The rescued searches convert at some rate between 0.5% and 3.0%.
5. Show a sensitivity: if they convert at 1.5% the gain is 8,000, at 2.0% it is 12,000.
6. Confirm with the A/B test on orders per search, not with the rate table.

**Metrics:**
- No-result rate = searches with no useful result / all searches.
- Orders per search = orders attributed to a search session / searches.
- Primary: incremental margin per search from the experiment, with a 95% interval.
- Guardrails: latency, add-to-cart rate, returns, and orders from other routes (browse) to catch cannibalisation.

**Risks:**
- Selection: searches that ended with no result are often poor-intent or out-of-catalogue, so they convert less even when answered.
- A loose "useful" label can count weakly relevant results as useful.
- Cannibalisation: the shopper may have ordered via browse anyway.
- Seasonality: the 3.0% may not hold off-peak.

**What the interviewer scores:**
- Strong: converts shares to counts and gets 20,000. Weak: "6% is 25% better, so 25% more margin."
- Strong: explains the upper bound with selection and gives a sensitivity. Weak: says "it depends."
- Strong: proposes orders-per-search from the experiment as the check. Weak: stays with the observed rate gap.

**Example:** (illustrative numbers) 200,000 searches rescued. Full 3.0% rate gives 20,000 a day. If rescued searches convert at only 1.5%, the gain is 8,000 a day. Weak answer: "20,000 a day." Strong answer: "Up to 20,000, probably nearer 8,000 to 12,000, I would read it off the test."

**Code:**
```python
searches = 10_000_000
moved = (0.08 - 0.06) * searches
conv_gain = 0.030 - 0.005
orders = moved * conv_gain
margin = orders * 4.00
print(f"searches moved to useful {moved:,.0f}; extra orders {orders:,.0f}; extra margin {margin:,.0f} per day")
assert round(moved) == 200_000 and round(orders) == 5_000 and round(margin) == 20_000
assert abs((0.08 - 0.06) / 0.08 - 0.25) < 1e-9
# upper bound: what if the rescued searches only convert part of the 3.0% (illustrative)
for share in (1.0, 0.6, 0.4, 0.2):
    c = 0.005 + share * conv_gain
    m = moved * (c - 0.005) * 4.00
    print(f"rescued searches reach {c:.2%} conversion -> {m:,.0f} per day")
m40 = moved * (0.4 * conv_gain) * 4.00
assert round(m40) == 8_000
# the same arithmetic, on the share of searches rather than as a rate
base_orders = searches * (0.08 * 0.005 + 0.92 * 0.030)
new_orders = searches * (0.06 * 0.005 + 0.94 * 0.030)
print(f"total orders {base_orders:,.0f} -> {new_orders:,.0f}; difference {new_orders-base_orders:,.0f}")
assert round(new_orders - base_orders) == 5_000
```

**Output (my run):**
```text
searches moved to useful 200,000; extra orders 5,000; extra margin 20,000 per day
rescued searches reach 3.00% conversion -> 20,000 per day
rescued searches reach 2.00% conversion -> 12,000 per day
rescued searches reach 1.50% conversion -> 8,000 per day
rescued searches reach 1.00% conversion -> 4,000 per day
total orders 280,000 -> 285,000; difference 5,000
```

**Follow-ups:**
- Why is the 0.5% not the right comparison either? Searches that stay no-result include dead-end queries that would never convert, so it can understate the base. The two biases push in different ways, which is why I use the experiment.
- What if the test shows less than the bound? That is normal; use the test number for the business case.

**Common mistakes:**
- Using the relative 25% as the lift in orders.
- Treating a correlational conversion gap as causal.
- Ignoring that rescued searches may be tail queries.
- Forgetting to net out orders that would have come from other routes.

### Q36 ⭐⭐ 🟡 A merchant processes 500,000 card transactions a month with chargebacks on 0.8% of them (4,000), and each chargeback costs 85 including the fee and the goods. A new rule blocks 30% of the chargebacks (1,200) but also declines 5,000 genuine transactions (1% of all transactions, absolute), each worth 3.00 of margin. Compute the net monthly value and say why a 1.0% card-network chargeback limit changes the weighting.
**Asked at:** Fraud-economics material (a Dataford 'evaluate fraud detection classifier' page with a limited review-capacity framing, DataRobot guidance on setting thresholds from false-negative versus false-positive cost, an Infosys BPM case study of a review-capacity cap, Sardine and other vendor pages on false positives); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** The rule saves 1,200 x 85 = 102,000 and loses 5,000 x 3.00 = 15,000, so net +87,000 a month; a 1.0% network limit matters because the current 0.8% is close to it, so I would weight avoided chargebacks as more than their cash cost when the rate is near the line.

**Clarifying questions:**
- How is the network limit measured (count of chargebacks against transaction count, over what month, with what minimum count)? I hedge: check the network's actual rule.
- Do the 5,000 declines include customers who retry and succeed with another card? Then the lost margin is lower.
- Are the 1,200 blocked chargebacks measured on a holdout, or estimated from past data? A rule's catch rate drops once fraudsters adapt.
- Is 3.00 only the margin of the declined order, or does it include lost repeat purchases? The loss is understated if customers leave.
- What does going over the limit cost (fines, higher fees, losing the ability to process)? It sets how heavily to weight the tail.

**Approach:**
1. Chargebacks now: 0.8% x 500,000 = 4,000. Blocked: 30% = 1,200. Saved: 1,200 x 85 = 102,000.
2. Declines: 1% x 500,000 = 5,000 genuine transactions, lost margin 5,000 x 3.00 = 15,000.
3. Net = 102,000 - 15,000 = 87,000 a month.
4. Break-even: the rule pays on these numbers up to 102,000 / 3.00 = 34,000 genuine declines, about 28 per chargeback blocked. It runs at 4.2.
5. The limit: before the rule the rate is 0.80%; after it is 0.56% (all transactions) or 0.57% (declines removed from the denominator). Headroom before was 1,000 chargebacks.
6. If a merchant sits near 1.0%, the penalty is a step cost, so I would accept a worse ratio of false declines to chargebacks, and I would say that I am doing so.

**Metrics:**
- Chargeback rate = chargebacks / transactions in the month (state the network's exact convention).
- Net value = (blocked chargebacks x cost per chargeback) - (genuine declines x value per decline).
- False-decline rate = genuine declined / all genuine transactions.
- Guardrails: approval rate, repeat-customer rate after a decline, appeals overturned.

**Risks:**
- Fraudsters adapt, so the 30% catch rate decays.
- Lost customers cost more than one order of 3.00.
- A chargeback rate that is "fine" today can jump after one fraud ring.
- If the 5,000 declines are concentrated in one segment, harm is uneven.

**What the interviewer scores:**
- Strong: net of 87,000 with both sides, plus a break-even. Weak: counts only the 102,000.
- Strong: says the limit makes the loss function non-linear and says which side. Weak: "just comply."
- Strong: notes that today's 0.8% is already below 1.0%, so the limit is a tail risk, not today's pain. Weak: assumes the merchant is over the limit.
- Strong: asks about repeat-customer loss. Weak: treats 3.00 as the whole cost.

**Example:** (illustrative numbers) 500,000 transactions, 4,000 chargebacks, 1,200 blocked, 5,000 genuine declines. Net +87,000. If the merchant were at 1.05%, blocking 30% brings it to 0.735%, below the line. Weak answer: "102,000 saved." Strong answer: "87,000 net, positive until about 34,000 false declines, and the limit makes it worth more near the line."

**Code:**
```python
tx = 500_000
cb = 0.008 * tx
blocked = 0.30 * cb
saved = blocked * 85
declined = 0.01 * tx
lost = declined * 3.00
net = saved - lost
print(f"chargebacks {cb:,.0f}; blocked {blocked:,.0f}; saved {saved:,.0f}; lost margin {lost:,.0f}; net {net:,.0f}")
assert round(cb) == 4_000 and round(blocked) == 1_200 and round(saved) == 102_000
assert round(declined) == 5_000 and round(lost) == 15_000 and round(net) == 87_000
before = cb / tx
after_all = (cb - blocked) / tx
after_ex = (cb - blocked) / (tx - declined)
print(f"chargeback rate before {before:.3%}; after {after_all:.3%} (all tx) or {after_ex:.3%} (declines removed)")
assert abs(before - 0.008) < 1e-12 and abs(after_all - 0.0056) < 1e-12
assert abs(after_ex - 2800 / 495_000) < 1e-12
print(f"headroom to the 1.0% limit before the rule: {0.01*tx - cb:,.0f} chargebacks")
assert round(0.01 * tx - cb) == 1_000
be = saved / 3.00
print(f"rule pays on margin alone up to {be:,.0f} declined genuine tx; ratio {be/blocked:.1f} declines per chargeback blocked (now {declined/blocked:.2f})")
assert round(be) == 34_000
# near the limit: add an assumed penalty (illustrative) of 50,000 a month if rate stays above 1.0%
cb_hot = 0.0105 * tx
print(f"if the rate were 1.05% ({cb_hot:,.0f}), blocking 30% gives {0.7*cb_hot/tx:.3%}, below 1.0%")
assert 0.7 * 0.0105 < 0.01
```

**Output (my run):**
```text
chargebacks 4,000; blocked 1,200; saved 102,000; lost margin 15,000; net 87,000
chargeback rate before 0.800%; after 0.560% (all tx) or 0.566% (declines removed)
headroom to the 1.0% limit before the rule: 1,000 chargebacks
rule pays on margin alone up to 34,000 declined genuine tx; ratio 28.3 declines per chargeback blocked (now 4.17)
if the rate were 1.05% (5,250), blocking 30% gives 0.735%, below 1.0%
```

**Follow-ups:**
- The ops head says 1% false declines is too many. How do you decide? Use the break-even of 28 declines per chargeback blocked, and add retention cost per decline; it is a business trade, not a model score.
- What would you test next? Raise the threshold slightly and watch both curves, or add a step-up check instead of a hard decline.

**Common mistakes:**
- Ignoring false declines.
- Treating the 1.0% limit as already breached.
- Computing the post-rule rate with the wrong denominator and not stating which.
- Assuming the catch rate stays at 30%.

### Q37 ⭐⭐ 🟡 A service sells Basic at 5, Standard at 8 and Premium at 12 a month, with a customer mix of 50%, 35% and 15% and cost-to-serve of 3.00, 4.50 and 8.00, so margins per customer are 2.00, 3.50 and 4.00. If Standard is removed and 60% of its customers move to Basic, 30% to Premium and 10% cancel, compute the blended margin per original customer before and after, and say what else the move changes.
**Asked at:** Subscription-tier and freemium material (a16z on optimising a free tier, a Frontiers in Psychology paper on a randomized freemium field experiment, getmonetizely and RevenueCat pricing-tier pages); mostly practitioner pages; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Blended margin per original customer falls from 2.825 to 2.440 (-13.6%) if Standard goes, because only 30% of Standard customers trade up to Premium; it would take 85% trading up to break even.

**Clarifying questions:**
- Where did the 60/30/10 split come from: a survey, a test, or a guess? It is the largest uncertainty.
- Are Basic users at a usage cap that makes them costlier or more likely to churn? Cost-to-serve may change with the move.
- Does removing the middle tier change how people see Basic and Premium (anchoring)? Mid-tiers often make Premium look like better value.
- Is the 10% cancel a one-time shock or does it grow? It affects lifetime value, not just month one.
- Is there a grandfathering plan or notice period? It changes timing and goodwill.

**Approach:**
1. Check margins: 5-3 = 2.00, 8-4.5 = 3.50, 12-8 = 4.00.
2. Before: 0.50 x 2.00 + 0.35 x 3.50 + 0.15 x 4.00 = 2.825.
3. After: Basic share 0.50 + 0.35 x 0.60 = 0.71. Premium 0.15 + 0.35 x 0.30 = 0.255. Cancelled 0.035.
4. After margin = 0.71 x 2.00 + 0.255 x 4.00 = 2.440, a drop of 0.385.
5. Break-even: with 10% cancelling, 85% of Standard customers (not 30%) would have to move to Premium.
6. Say what else moves: revenue per original customer falls from 7.10 to 6.61, and the Premium upgrade rate, churn, support load, and price perception all shift.
7. Test it: a randomized pricing-page test (with and without Standard) on new visitors before touching existing customers.

**Metrics:**
- Blended margin per original customer = sum of (share x margin) over tiers, with cancelled customers at zero.
- Revenue per original customer and customer lifetime value (not only month-one margin).
- Tier mix, cancel rate, upgrade and downgrade rates.
- Guardrails: support tickets, NPS, new-customer conversion.

**Risks:**
- Stated switching intentions overstate upgrades.
- The 10% cancel could grow after the first bill.
- The compromise effect: removing the middle tier may reduce Premium sales.
- Cost-to-serve is an average, not marginal.

**What the interviewer scores:**
- Strong: computes before and after and a break-even upgrade share. Weak: "Premium margin is higher, so remove Standard."
- Strong: counts cancellers as zero margin. Weak: renormalises over the survivors only.
- Strong: lists behavioural effects beyond the arithmetic. Weak: stops at the formula.
- Strong: proposes a test on new visitors. Weak: ships to everyone.

**Example:** (illustrative numbers) Per 100 customers: before 282.5 of margin a month. After: 71 Basic (142) + 25.5 Premium (102) = 244. Weak answer: "Standard is only 3.50, drop it." Strong answer: "That loses 13.6% unless 85% trade up; test first."

**Code:**
```python
mix = {"Basic": 0.50, "Standard": 0.35, "Premium": 0.15}
price = {"Basic": 5, "Standard": 8, "Premium": 12}
cost = {"Basic": 3.0, "Standard": 4.5, "Premium": 8.0}
m = {k: price[k] - cost[k] for k in mix}
assert m == {"Basic": 2.0, "Standard": 3.5, "Premium": 4.0}
before = sum(mix[k] * m[k] for k in mix)
basic = mix["Basic"] + 0.35 * 0.60
prem = mix["Premium"] + 0.35 * 0.30
cancel = 0.35 * 0.10
after = basic * m["Basic"] + prem * m["Premium"]
rev_b = sum(mix[k] * price[k] for k in mix)
rev_a = basic * 5 + prem * 12
print(f"blended margin before {before:.3f}; after {after:.3f}; change {after-before:+.3f} ({after/before-1:+.1%})")
print(f"mix after: Basic {basic:.3f}, Premium {prem:.3f}, cancelled {cancel:.3f}")
print(f"revenue per original customer {rev_b:.3f} -> {rev_a:.3f}")
assert abs(before - 2.825) < 1e-9 and abs(after - 2.44) < 1e-9
assert abs(basic - 0.71) < 1e-9 and abs(prem - 0.255) < 1e-9 and abs(cancel - 0.035) < 1e-9
assert abs(basic + prem + cancel - 1) < 1e-9
# what Premium take-up would break even if cancel stays at 10%
# move share s to Premium, 0.9-s to Basic
for s in (0.30, 0.40, 0.50, 0.60):
    a = (0.50 + 0.35 * (0.9 - s)) * 2 + (0.15 + 0.35 * s) * 4
    print(f"  Standard->Premium share {s:.0%}: margin {a:.3f}")
s_be = None
for i in range(0, 901):
    s = i / 1000
    a = (0.50 + 0.35 * (0.9 - s)) * 2 + (0.15 + 0.35 * s) * 4
    if a >= before: s_be = s; break
print(f"break-even Premium share (cancel 10%): {s_be}")
assert s_be == 0.85
print("so 85% of Standard customers (not 30%) would have to trade up to Premium")
```

**Output (my run):**
```text
blended margin before 2.825; after 2.440; change -0.385 (-13.6%)
mix after: Basic 0.710, Premium 0.255, cancelled 0.035
revenue per original customer 7.100 -> 6.610
  Standard->Premium share 30%: margin 2.440
  Standard->Premium share 40%: margin 2.510
  Standard->Premium share 50%: margin 2.580
  Standard->Premium share 60%: margin 2.650
break-even Premium share (cancel 10%): 0.85
so 85% of Standard customers (not 30%) would have to trade up to Premium
```

**Follow-ups:**
- What if Standard has high support cost? Then its real margin is lower, so recompute with true cost to serve; the answer could flip.
- Would you keep Standard and raise its price instead? Plausible; it costs an experiment, and it avoids cancels.

**Common mistakes:**
- Dividing by the surviving customers (2.440 / 0.965) and hiding the cancellations.
- Using price instead of margin.
- Treating 30% upgrade as certain.
- Forgetting lifetime effects of the cancels.

### Q38 ⭐⭐ 🔴 Loyalty-programme members spend 120 a quarter against 40 for non-members, so a dashboard claims a 200% lift relative to non-members. A randomized invitation sent to 20,000 customers, with 20,000 uninvited as control, got 25% of invitees to join, and revenue per customer was 44 for invited against 42 for uninvited. Each member costs 6 a quarter in rewards and margin is 30% of revenue. Compute the effect per joiner and its margin, and explain what the dashboard number measures.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened
**Say this first (1 line):** The 200% lift is just members versus non-members (120 versus 40), which is self-selection; the randomized invitation says an invite adds 2 per customer, so 8 revenue per joiner, 2.4 of margin, which is 3.6 below the 6 reward cost per quarter.

**Clarifying questions:**
- Can uninvited customers join the programme? If they can, the per-joiner scaling by 25% is wrong. I assume they cannot.
- Does the invitation itself change behaviour even if the customer does not join? If so, dividing by 25% overstates the joiner effect (exclusion restriction).
- What is the spread (standard deviation) of revenue per customer? It gives the interval on the 2.
- Is 6 a quarter the full cost of rewards, or also admin cost? Costs missing here make it worse.
- Over what horizon: one quarter, or lasting retention? Members may stay longer.

**Approach:**
1. Dashboard: 120 / 40 - 1 = 200%. It compares people who chose to join (heavy spenders) with those who did not. It does not measure what the programme caused.
2. Randomized effect per invited customer (intention to treat): 44 - 42 = 2.
3. Effect per joiner: 2 / 0.25 = 8 revenue per joiner per quarter (assumes only invitees can join and the invitation works only through joining).
4. Margin per joiner: 30% x 8 = 2.40. Reward cost 6. Net -3.60 per joiner per quarter.
5. Total per quarter across 20,000 invitees: margin gain 12,000, rewards 30,000, net -18,000.
6. Uncertainty: with an assumed revenue standard deviation of 80, the 95% interval on the 2 is 0.43 to 3.57, so even the top gives 4.28 of margin per joiner, below 6.
7. Say what would change it: lower reward cost, targeting the invitees where the effect is high, or a lifetime effect beyond one quarter.

**Metrics:**
- Intention-to-treat effect = mean revenue (invited) - mean revenue (control) = 2 per invitee.
- Join rate = joiners / invitees = 25%.
- Effect per joiner (complier effect) = ITT / join rate.
- Net value per joiner = 30% x effect - reward cost.
- Guardrails: margin rate, returns, retention at 4 quarters.

**Risks:**
- Selection: members were already heavy buyers (dashboard).
- The interval is wide relative to the 2.
- One quarter misses retention and lifetime effects.
- Rewards may be partly redeemed on purchases that would have happened anyway.

**What the interviewer scores:**
- Strong: names selection bias and gives the randomized figure. Weak: "200% lift."
- Strong: divides by the join rate and states the assumption. Weak: reports 2 as the per-joiner effect, or 44-42 as 4.8%, and stops.
- Strong: takes margin, not revenue, and subtracts the reward. Weak: compares revenue to cost.
- Strong: asks for the interval. Weak: treats 2 as certain.

**Example:** (illustrative numbers) 5,000 joiners out of 20,000 invited. Revenue gain: 2 x 20,000 = 40,000, margin 12,000, rewards 30,000, net -18,000 a quarter. Weak answer: "Members spend 3 times more, expand it." Strong answer: "The causal figure is 8 a joiner, 2.40 of margin against 6 of rewards, so it loses money on these terms."

**Code:**
```python
import math
dash = 120 / 40 - 1
print(f"dashboard lift {dash:.0%}")
assert abs(dash - 2.0) < 1e-9
n = 20_000
itt = 44 - 42
join = 0.25
per_joiner = itt / join
margin_per_joiner = 0.30 * per_joiner
net_per_joiner = margin_per_joiner - 6
print(f"ITT {itt}; per joiner {per_joiner:.1f}; margin {margin_per_joiner:.1f}; after rewards {net_per_joiner:.1f}")
assert per_joiner == 8 and abs(margin_per_joiner - 2.4) < 1e-9 and abs(net_per_joiner + 3.6) < 1e-9
joiners = join * n
total = 0.30 * itt * n - 6 * joiners
print(f"quarter total: margin gain {0.30*itt*n:,.0f} - rewards {6*joiners:,.0f} = {total:,.0f}")
assert round(0.30 * itt * n) == 12_000 and round(6 * joiners) == 30_000 and round(total) == -18_000
# uncertainty, ASSUMING revenue sd 80 per customer (illustrative)
sd = 80
se = sd * math.sqrt(2 / n)
lo, hi = itt - 1.96 * se, itt + 1.96 * se
print(f"se {se:.2f}; ITT 95% CI {lo:.2f} to {hi:.2f}; per joiner {lo/join:.1f} to {hi/join:.1f}")
print(f"best-case margin per joiner {0.30*hi/join:.2f} vs reward 6")
assert 0.30 * hi / join < 6
# break-even effect per joiner
be = 6 / 0.30
print(f"break-even revenue effect per joiner {be:.0f} a quarter; dashboard-style gap was {120-40}")
assert round(be) == 20
```

**Output (my run):**
```text
dashboard lift 200%
ITT 2; per joiner 8.0; margin 2.4; after rewards -3.6
quarter total: margin gain 12,000 - rewards 30,000 = -18,000
se 0.80; ITT 95% CI 0.43 to 3.57; per joiner 1.7 to 14.3
best-case margin per joiner 4.28 vs reward 6
break-even revenue effect per joiner 20 a quarter; dashboard-style gap was 80
```

**Follow-ups:**
- Could it still be worth it? Yes if the reward is cheaper, if the effect lasts across quarters, or if the programme lifts retention; each needs its own test. Break-even is about 20 revenue per joiner per quarter on a 6 reward at 30% margin.
- Why not compare members who joined from the invited group with non-members from the control group? That reintroduces selection, because joiners are self-chosen.

**Common mistakes:**
- Taking 120 versus 40 as the effect.
- Dividing 2 by 25% but forgetting margin and reward cost.
- Ignoring that 25% is the only reason the per-joiner effect is bigger than 2.
- Not asking about spread.

### Q39 ⭐⭐ 🔴 An AI agent resolves 45,000 of 100,000 monthly tickets at 0.80 each instead of 6.00 per human ticket. A randomized holdout shows customers whose tickets went to the agent churn at 3.0% a month against 2.5% for the holdout (0.5 points absolute), and a customer is worth 400 of future margin. The platform costs 60,000 a month. Compute the net monthly value and say how you would tell whether the churn gap is caused by the agent.
**Asked at:** AI-era support and GenAI cost material (2026 vendor and practitioner pages from Lorikeet, Twig, Voiceflow, aitimejournal, CloudZero, nOps, tianpan.co and a Gartner press-release headline on inference costs); mostly vendor-sourced, an emerging interview theme rather than a confirmed bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Savings of 234,000 less churn cost of 90,000 less platform cost of 60,000 gives net +84,000 a month, but it only stays positive while the churn gap is under about 0.97 points, so the churn gap is the number to nail down.

**Clarifying questions:**
- How were customers assigned to the holdout, and how large is the holdout? It sets the interval on the 0.5 points; the prompt does not give it.
- Is the comparison by assignment (all tickets routed to the agent) or by outcome (tickets the agent resolved)? Only assignment is randomized.
- Is it one ticket per customer in the month? I assume so, to count 45,000 customers.
- Is the 400 of future margin the same for those customers as for the average? Customers with simple tickets may be worth less.
- Do human handoffs from the agent count in the 45,000? Escalated tickets cost both.

**Approach:**
1. Savings: 45,000 x (6.00 - 0.80) = 234,000.
2. Extra churn: 0.5 points x 45,000 = 225 customers. Cost = 225 x 400 = 90,000.
3. Net = 234,000 - 90,000 - 60,000 = 84,000.
4. Break-even churn gap = (234,000 - 60,000) / (45,000 x 400) = 0.97 points. Observed is 0.5.
5. Causality: since it is randomized, the gap is causal if the randomization is sound. Check the sample ratio and baseline balance, analyse by assignment (intention to treat), and get an interval.
6. The interval depends on the holdout. With an illustrative holdout of 5,000 the gap interval is 0.04 to 0.96 points (net 1,098 to 166,902); with 2,000 it includes zero and net can be negative.
7. Look at mechanism: reopened tickets, escalations, satisfaction, repeat contact, and churn by ticket type.

**Metrics:**
- Net monthly value = tickets resolved x cost saved - extra churn x customer value - platform cost.
- Churn gap = churn rate (agent arm) - churn rate (holdout), with a 95% interval.
- Cost per resolved ticket including reopens and escalations.
- Guardrails: CSAT, reopen rate, time to resolution.

**Risks:**
- A holdout too small to separate 3.0% from 2.5%.
- Treating "resolved by agent" customers versus others as a comparison (selection).
- Churn measured over one month may miss later effects.
- Cost per ticket ignores quality: unresolved tickets come back.

**What the interviewer scores:**
- Strong: nets savings against churn and platform cost, with a break-even gap. Weak: "45,000 x 5.20 saved."
- Strong: separates randomized assignment from outcome-based groups. Weak: "observe churn by group."
- Strong: asks for the interval, and for the holdout size. Weak: treats 0.5 as exact.
- Strong: checks reopens and escalations. Weak: only looks at deflection.

**Example:** (illustrative numbers) Saving 234,000, churn cost 90,000, platform 60,000: net +84,000. At a 1.0-point gap the net is -6,000. Weak answer: "Save 234,000 a month." Strong answer: "Net 84,000, good until the gap reaches 0.97 points, so I need the interval."

**Code:**
```python
import math
tickets, resolved = 100_000, 45_000
saving = resolved * (6.00 - 0.80)
extra_churn = 0.005 * resolved
churn_cost = extra_churn * 400
net = saving - churn_cost - 60_000
print(f"saving {saving:,.0f}; extra churners {extra_churn:,.0f}; churn cost {churn_cost:,.0f}; net {net:,.0f}")
assert round(saving) == 234_000 and round(extra_churn) == 225 and round(churn_cost) == 90_000 and round(net) == 84_000
be_gap = (saving - 60_000) / (resolved * 400)
print(f"churn gap that wipes out the value: {be_gap*100:.2f} points")
assert abs(be_gap - 174_000 / 18_000_000) < 1e-12
# is 3.0% vs 2.5% distinguishable? holdout size is NOT given; try sizes (45,000 in agent arm assumed)
for h in (2_000, 5_000, 20_000):
    se = math.sqrt(0.03 * 0.97 / resolved + 0.025 * 0.975 / h)
    z = 0.005 / se
    lo, hi = 0.005 - 1.96 * se, 0.005 + 1.96 * se
    net_hi = saving - 60_000 - hi * resolved * 400
    net_lo = saving - 60_000 - lo * resolved * 400
    print(f"holdout {h:>6,}: z {z:.2f}; gap CI {lo*100:.2f}..{hi*100:.2f} pts; net CI {net_hi:,.0f}..{net_lo:,.0f}")
se5 = math.sqrt(0.03 * 0.97 / resolved + 0.025 * 0.975 / 5_000)
assert 2.0 < 0.005 / se5 < 2.3
```

**Output (my run):**
```text
saving 234,000; extra churners 225; churn cost 90,000; net 84,000
churn gap that wipes out the value: 0.97 points
holdout  2,000: z 1.40; gap CI -0.20..1.20 pts; net CI -42,390..210,390
holdout  5,000: z 2.13; gap CI 0.04..0.96 pts; net CI 1,098..166,902
holdout 20,000: z 3.66; gap CI 0.23..0.77 pts; net CI 35,814..132,186
```

**Follow-ups:**
- The gap is 0.5 but the interval includes 0. What now? Run the holdout longer or bigger; do not conclude "no effect."
- How do you decide caused by the agent? Randomized assignment, balance checks, assignment-based analysis, and a mechanism check (reopens, escalations, CSAT).

**Common mistakes:**
- Ignoring churn.
- Comparing agent-resolved with human-resolved customers.
- Treating 0.5 points as significant without a holdout size.
- Forgetting the platform cost.

### Q40 ⭐⭐ 🔴 A subscription app tests a regional price of 3 against 5 on 100,000 visitors per arm in smaller cities. Conversion rises from 6% to 9% of visitors (3 points absolute, 50% relative to 6%), and cost to serve is 1 a month per subscriber. Compute monthly revenue and contribution in each arm, then subtract the loss from 1,000 existing subscribers elsewhere who would switch from 5 to 3 by using the cheaper regional plan, and say how you would stop that leakage.
**Asked at:** Subscription-tier and freemium material (a16z on optimising a free tier, a Frontiers in Psychology paper on a randomized freemium field experiment, getmonetizely and RevenueCat pricing-tier pages); mostly practitioner pages; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Price 3 wins on subscribers (9,000 versus 6,000) but loses on money: revenue 27,000 versus 30,000 and contribution 18,000 versus 24,000, and after 2,000 of leakage it is -8,000 a month, so as stated the cheaper price loses.

**Clarifying questions:**
- Is the 6% versus 9% a randomized price test within the same cities? If not, other differences drive it.
- Is retention the same at 3 as at 5? Cheaper subscribers often churn faster, which makes the lifetime picture worse.
- How would customers outside the region reach the regional plan (VPN, app-store country, billing address)? It sizes the leakage.
- Is the 1,000 switchers a measured figure? It could be larger as word spreads.
- Does a lower price pull in more usage, raising cost to serve above 1?

**Approach:**
1. Price 5: 6% x 100,000 = 6,000 subscribers. Revenue 30,000. Contribution 6,000 x (5-1) = 24,000.
2. Price 3: 9,000 subscribers. Revenue 27,000. Contribution 9,000 x (3-1) = 18,000.
3. Difference before leakage: -3,000 revenue and -6,000 contribution.
4. Leakage: 1,000 x (5-3) = 2,000 a month. Cost to serve does not change, so the contribution falls by 2,000 too. Net -8,000.
5. Break-even conversion at price 3: 12.0% for contribution (24,000 / 2 / 100,000), 10.0% for revenue. We got 9%.
6. Check the conversion gap is real: z is about 25, so noise is not the issue; the price elasticity is just not high enough.
7. Stop leakage: restrict by billing country and app-store storefront, verify payment-method country, make the regional plan new-customer only, limit features, and watch cross-region switches. Do not roll out to the existing base.

**Metrics:**
- Contribution per 100,000 visitors = subscribers x (price - cost to serve).
- Conversion = new subscribers / visitors in each arm.
- Leakage = existing subscribers who move to the lower plan x price difference.
- Guardrails: retention at 3 months, support load, refund rate.

**Risks:**
- The revenue test ignores lifetime: low-price subscribers may churn faster.
- Leakage grows over time.
- Gaming: VPN or address changes.
- One-month view hides a possible upsell path.

**What the interviewer scores:**
- Strong: computes both revenue and contribution, notes revenue also falls. Weak: "conversion up 50%, so price 3 wins."
- Strong: includes leakage in the net and gives the break-even conversion. Weak: forgets leakage.
- Strong: names concrete leakage controls. Weak: "monitor it."
- Strong: asks about retention at the lower price. Weak: assumes equal retention.

**Example:** (illustrative numbers) Control 6,000 subscribers, 24,000 contribution; test 9,000, 18,000; leakage 2,000; net -8,000. Weak answer: "50% more subscribers, roll out." Strong answer: "Needs 12% conversion to break even, we got 9%, and leakage makes it worse; do not roll out at 3."

**Code:**
```python
import math
v = 100_000
c5, c3 = 0.06 * v, 0.09 * v
rev5, rev3 = c5 * 5, c3 * 3
con5, con3 = c5 * (5 - 1), c3 * (3 - 1)
print(f"price 5: subs {c5:,.0f}, revenue {rev5:,.0f}, contribution {con5:,.0f}")
print(f"price 3: subs {c3:,.0f}, revenue {rev3:,.0f}, contribution {con3:,.0f}")
assert round(c5) == 6_000 and round(c3) == 9_000
assert round(rev5) == 30_000 and round(rev3) == 27_000
assert round(con5) == 24_000 and round(con3) == 18_000
assert abs(0.09 / 0.06 - 1 - 0.5) < 1e-9
leak = 1_000 * (5 - 3)
net = con3 - con5 - leak
print(f"leakage {leak:,.0f}; contribution change {con3-con5:,.0f}; after leakage {net:,.0f}")
assert leak == 2_000 and net == -8_000
print(f"break-even conversion at price 3: contribution {24_000/(2*v):.1%}, revenue {30_000/(3*v):.1%}")
assert abs(24_000 / (2 * v) - 0.12) < 1e-9 and abs(30_000 / (3 * v) - 0.10) < 1e-9
# the 6% vs 9% gap is not noise
p = 0.075
z = 0.03 / math.sqrt(2 * p * (1 - p) / v)
print(f"z for conversion gap {z:.1f}")
assert z > 20
# leakage size that would not matter: how many switchers keep the price-3 plan equal to price 5?
print(f"gap before leakage is {con3-con5:,.0f}; negative already, so no leakage level rescues it")
```

**Output (my run):**
```text
price 5: subs 6,000, revenue 30,000, contribution 24,000
price 3: subs 9,000, revenue 27,000, contribution 18,000
leakage 2,000; contribution change -6,000; after leakage -8,000
break-even conversion at price 3: contribution 12.0%, revenue 10.0%
z for conversion gap 25.5
gap before leakage is -6,000; negative already, so no leakage level rescues it
```

**Follow-ups:**
- Is there a price between 3 and 5 that works? Test 4: with the two points I can only say it needs a conversion of at least 8% for contribution (24,000 / 3 / 100,000).
- Could price 3 still be right? If retention or lifetime is much higher, or it fills capacity at zero marginal cost; each needs data.

**Common mistakes:**
- Reading conversion as profit.
- Using revenue without cost to serve.
- Leaving out leakage.
- Rolling out before testing retention.

### Q41 ⭐⭐ 🔴 Three-month retention for a new cohort is 70% of sign-ups, and an analyst extrapolates a constant monthly churn from it. Older cohorts show 40% of sign-ups still active at 12 months, and margin is 10 a month per active customer. Compute the implied monthly churn, the 12-month retention under a constant rate, and LTV by margin divided by churn, then explain why the older cohorts disagree and which LTV you would trust for a CAC budget.
**Asked at:** Lifetime-value and CAC material (a Dataford 'calculate customer lifetime value' product-growth-analyst page, Hacking the Case Interview, Road to Offer and MBB Prep pages on CLV and CAC, Count.co and FourWeekMBA CAC-payback pages); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Constant churn from 70% at month 3 gives 11.2% a month, 24% left at month 12 and an LTV of 89.2, but older cohorts retain 40% at 12 months, so churn falls over time and the constant-rate LTV is too low; I would budget CAC on the cohort curve, with a capped and discounted tail.

**Clarifying questions:**
- Are older cohorts acquired the same way (channel, offer, geography)? If not, they may not predict the new cohort.
- Are the 40% at 12 months and the 70% at 3 months measured the same way (any activity, or paid)? Definitions must match.
- Is margin per active customer flat at 10, or does it rise or fall with tenure? LTV depends on it.
- Is there discounting or a payback target for the CAC budget? It limits how far out the tail counts.
- What is the sample size of the new cohort? 70% could be noisy.

**Approach:**
1. Monthly retention = 0.70^(1/3) = 0.8879, so churn = 11.2%.
2. 12-month retention under constant churn = 0.70^4 = 24.0%.
3. LTV = 10 / 0.1121 = 89.2 (convention: margin collected from month 0, so expected active months = 1 / churn).
4. Older cohorts show 40%, 1.67 times higher. So churn is not constant: it is high early and lower later, as the keeper customers stay.
5. The two points imply churn of about 6.0% a month from month 3 to 12, against 11.2% in the first 3 months.
6. Two-stage LTV (11.2% early, 6.0% later, tail to infinity) = 142.9. Capped at 12 months: 76.5, against 67.8 for constant churn.
7. CAC budget: use the observed cohort curve to 12 months as the base, add a tail only with a cap and a discount, and keep the 89.2 as the conservative floor.

**Metrics:**
- Cohort retention = active customers at month t / sign-ups in the cohort.
- Implied monthly churn = 1 - retention(3)^(1/3).
- LTV = sum over months of (survival x margin), with stated horizon and discount.
- CAC payback = months until cumulative margin per sign-up is at least CAC.

**Risks:**
- The tail beyond 12 months is an assumption: 142.9 depends on 6.0% holding forever.
- Older cohorts may be better customers than the new one.
- Survivor mix changes: heavy users stay, so averages move.
- Undiscounted LTV overstates value for a budget.

**What the interviewer scores:**
- Strong: computes 11.2%, 24%, 89.2 and sees the 40% contradicts constant churn. Weak: reports 89.2 as the LTV.
- Strong: explains why (heterogeneity, early churn higher). Weak: "the data is noisy."
- Strong: picks a budgeting LTV with a horizon cap and says so. Weak: picks the largest.
- Strong: states the convention for 1/churn. Weak: silent.

**Example:** (illustrative numbers) Of 1,000 sign-ups, 700 are active at month 3, 240 at month 12 under constant churn, but 400 in older cohorts. LTV 89.2 versus a two-stage 142.9 (about 60% higher). Weak answer: "LTV is 89, spend up to a third of it." Strong answer: "89 is a floor; I use the observed curve to month 12, and cap the tail."

**Code:**
```python
r3 = 0.70
r1 = r3 ** (1 / 3)
churn = 1 - r1
r12 = r3 ** 4
ltv = 10 / churn
print(f"monthly retention {r1:.4f}; churn {churn:.4f}; 12-month retention {r12:.4f}; LTV {ltv:.1f}")
assert abs(churn - 0.1121) < 5e-4 and abs(r12 - 0.2401) < 1e-9 and abs(ltv - 89.2) < 0.1
old = 0.40
print(f"old cohorts hold {old:.0%} at 12 months vs {r12:.1%} predicted: {old/r12:.2f}x")
# hazard between month 3 and 12 implied by the two points
r_late = (old / r3) ** (1 / 9)
churn_late = 1 - r_late
print(f"implied churn months 3-12: {churn_late:.4f} (first 3 months {churn:.4f})")
assert churn_late < churn
# LTV with early churn then late churn, same convention as margin/churn (sum of survival from t=0)
first = sum(r1 ** t for t in range(3))
tail = r3 / (1 - r_late)
ltv2 = 10 * (first + tail)
print(f"two-stage LTV (tail to infinity) {ltv2:.1f}")
# 12-month capped LTV (months 0..11 active-start) for both curves
cap_const = 10 * sum(r1 ** t for t in range(12))
cap_two = 10 * (first + sum(r3 * r_late ** k for k in range(9)))
print(f"12-month margin per sign-up: constant-churn {cap_const:.1f}; two-stage {cap_two:.1f}")
assert cap_const < cap_two < ltv2
assert ltv2 > ltv
```

**Output (my run):**
```text
monthly retention 0.8879; churn 0.1121; 12-month retention 0.2401; LTV 89.2
old cohorts hold 40% at 12 months vs 24.0% predicted: 1.67x
implied churn months 3-12: 0.0603 (first 3 months 0.1121)
two-stage LTV (tail to infinity) 142.9
12-month margin per sign-up: constant-churn 67.8; two-stage 76.5
```

**Follow-ups:**
- Which LTV for a CAC budget? The one that is based on observed months with a conservative tail, usually with a payback limit rather than a lifetime sum.
- What would change your mind? New cohort retention at month 6 and 12 matching the older curve.

**Common mistakes:**
- Extrapolating a constant rate from 3 months.
- Comparing 24% and 40% without explaining it.
- Using LTV without a horizon or discount.
- Forgetting the 1/churn convention.

### Q42 ⭐⭐ 🔴 A new forecasting model cuts weighted absolute percentage error (WAPE) from 22% to 18% (4 points absolute, about 18% relative to 22%). Safety stock is 300,000 units and the planner assumes it scales in proportion to forecast error, with a holding cost of 0.50 a unit a week. Compute the claimed weekly holding saving, and say why it is not the same as ROI and what you would check before booking it.
**Asked at:** Forecasting and inventory material (PracHub retail demand-forecasting and inventory-and-stockout concept pages, a Dataford supermarket demand-forecasting page attributed in its title to a BCG data scientist interview but unverified, a PyCon DE 2025 talk on stockouts in retail forecasting); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** If safety stock scaled with WAPE, it would fall 18.2% from 300,000 to 245,455 units, a claimed saving of 27,273 a week; but WAPE is not the driver of safety stock and the saving is not ROI, because I have not netted the model cost or checked where the stock sits.

**Clarifying questions:**
- How is WAPE measured (weekly or daily, item level or aggregate, lag)? It must match the lead time that safety stock covers.
- Where is the safety stock held: fast movers or slow ones? WAPE is volume-weighted and dominated by fast movers.
- What service level is targeted, and is it changing? Safety stock is service-level times demand error times a lead-time factor.
- What does the model cost to run and maintain a week? ROI needs it.
- Is the improvement on a held-out period with the same promotions and seasonality?

**Approach:**
1. Relative cut = (22 - 18) / 22 = 18.2%, not 4 percent.
2. Proportional stock: 300,000 x 18/22 = 245,455. Units freed 54,545. Saving = 54,545 x 0.50 = 27,273 a week (about 1.42 million a year).
3. Why this is only a claim: safety stock follows the standard deviation of lead-time demand error, not a volume-weighted percentage.
4. Illustrative split: fast movers (80% of volume) go from 20 to 15, slow movers stay at 30; overall WAPE falls 22 to 18. If only 30% of safety stock sits on fast movers, stock falls 7.5%, a saving of 11,250 a week, not 27,273.
5. ROI = (benefit - cost) / cost. Net of an illustrative running cost of 20,000 a week, the claimed saving gives 7,273 and ROI 0.36; the realistic saving gives -8,750.
6. Check before booking: error by SKU group at lead time, service level, stock-outs, actual stock after replanning, and a before/after on a held-out period.
7. Book the saving only when stock has actually been reduced and service held.

**Metrics:**
- WAPE = sum of absolute errors / sum of actuals.
- Safety stock cut = (old stock - new stock) / old stock, by SKU group.
- Holding saving = units removed x holding cost per unit per week.
- ROI = (saving - model cost) / model cost. Guardrails: fill rate and stock-out rate.

**Risks:**
- Proportional scaling is an assumption.
- Lower WAPE on fast sellers does not reduce slow-mover stock.
- Reducing stock can cause stock-outs that cost more than holding.
- Savings are one-off (stock release) versus recurring (holding cost); do not mix them.

**What the interviewer scores:**
- Strong: gets 27,273 and then questions the proportional rule. Weak: "4 points means 4%."
- Strong: separates saving from ROI with costs. Weak: calls it ROI.
- Strong: lists checks (SKU mix, service level, hold-out). Weak: "validate the model."
- Strong: mentions stock-out cost. Weak: only holding cost.

**Example:** (illustrative numbers) Claimed 27,273 a week; realistic 11,250 with the SKU split above; running cost 20,000. Weak answer: "We save 27,000 a week." Strong answer: "Claimed 27,000, maybe 11,000, and ROI depends on cost and service level."

**Code:**
```python
rel = 1 - 18 / 22
new_ss = 300_000 * 18 / 22
saved_units = 300_000 - new_ss
saving = saved_units * 0.50
print(f"relative cut {rel:.2%}; new safety stock {new_ss:,.0f}; units freed {saved_units:,.0f}; weekly saving {saving:,.0f}")
assert abs(rel - 0.1818) < 1e-4 and round(saved_units) == 54_545 and abs(saving - 27_272.7) < 1
print(f"annual (52 weeks) {saving*52:,.0f}")
# WAPE is volume-weighted, safety stock sits where error is large (slow movers). Illustrative split:
w_fast, w_slow = 0.8, 0.2
old = w_fast * 20 + w_slow * 30
new = w_fast * 15 + w_slow * 30
print(f"overall WAPE {old:.0f} -> {new:.0f} when only fast movers improve (20 -> 15, slow stays 30)")
assert abs(old - 22) < 1e-9 and abs(new - 18) < 1e-9
fast_stock_share = 0.30   # assumed share of safety stock held on fast movers
true_cut = fast_stock_share * (1 - 15 / 20)
true_saving = 300_000 * true_cut * 0.50
print(f"stock cut {true_cut:.1%} not {rel:.1%}; weekly saving {true_saving:,.0f} not {saving:,.0f}")
assert abs(true_cut - 0.075) < 1e-9 and abs(true_saving - 11_250) < 1e-6
cost = 20_000   # illustrative weekly running cost of the model
print(f"claimed saving net of an illustrative {cost:,} running cost: {saving-cost:,.0f}; ROI {(saving-cost)/cost:.2f}")
print(f"with the realistic saving: {true_saving-cost:,.0f}")
assert abs((saving - cost) / cost - 0.3636) < 1e-3 and true_saving - cost < 0
```

**Output (my run):**
```text
relative cut 18.18%; new safety stock 245,455; units freed 54,545; weekly saving 27,273
annual (52 weeks) 1,418,182
overall WAPE 22 -> 18 when only fast movers improve (20 -> 15, slow stays 30)
stock cut 7.5% not 18.2%; weekly saving 11,250 not 27,273
claimed saving net of an illustrative 20,000 running cost: 7,273; ROI 0.36
with the realistic saving: -8,750
```

**Follow-ups:**
- Why a held-out check? A model tuned on history looks better than it performs.
- How would you size safety stock properly? Service-level factor times the standard deviation of lead-time demand error, by SKU, not a WAPE ratio.

**Common mistakes:**
- Treating 4 points as a 4% cut.
- Calling the holding saving ROI.
- Forgetting stock-out cost.
- Assuming error improvement is uniform across SKUs.

### Q43 ⭐⭐ 🔴 A fraud rule flags transactions that turn out to be 12% fraud, with an average fraud loss of 80. In a randomized test, flagged genuine customers who were declined retained at 84% over 90 days against 92% for those allowed through (8 points absolute), and a retained customer is worth 150. Compute the expected cost per flagged transaction of declining and of allowing, counting friction only on genuine customers, and say which other costs matter.
**Asked at:** Fraud-economics material (a Dataford 'evaluate fraud detection classifier' page with a limited review-capacity framing, DataRobot guidance on setting thresholds from false-negative versus false-positive cost, an Infosys BPM case study of a review-capacity cap, Sardine and other vendor pages on false positives); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Counting only the friction on genuine customers, declining costs 10.56 per flagged transaction and allowing costs 9.60, so allowing is slightly cheaper at a 12% fraud share; the break-even fraud share is 13.0%, and other costs (chargeback fees, network limits, review) can flip it.

**Clarifying questions:**
- Does a decline fully prevent the fraud loss of 80, or can the fraudster retry? It sets the benefit of declining.
- Is the 84% versus 92% from a randomized test of genuine customers only? I take that as given, and ask for an interval.
- Is there a third option (step-up verification, manual review)? Often cheaper than either.
- Are there extra fraud costs on allowing: chargeback fee, network ratio penalties, repeat attacks? I hold them outside this number.
- Is 150 the value of any retained customer, or of this segment? Flagged customers may differ.

**Approach:**
1. Friction cost per genuine decline = (92% - 84%) x 150 = 12.00 over 90 days.
2. Cost of declining = genuine share x friction = 0.88 x 12.00 = 10.56 per flagged transaction.
3. Cost of allowing = fraud share x loss = 0.12 x 80 = 9.60.
4. Difference: decline is 0.96 worse per flagged transaction (about 96,000 per 100,000 flagged).
5. Break-even fraud share = 12 / (80 + 12) = 13.04%. Break-even retention gap = 9.60 / (0.88 x 150) = 7.27 points. The observed 8 sits just above it.
6. The margin is thin: with an extra 15 chargeback fee on allowed fraud, allowing costs 11.40 and declining wins.
7. Practical rule: decline above the break-even fraud share, step up or review in the band around it, allow below. Add the interval on the retention gap.

**Metrics:**
- Expected cost of declining = P(genuine) x retention gap x customer value.
- Expected cost of allowing = P(fraud) x loss per fraud (plus fees and fines when counted).
- Fraud precision of the flag = fraud / flagged = 12%.
- Guardrails: approval rate, chargeback ratio, repeat-customer rate, review queue size.

**Risks:**
- The 8-point gap comes with sampling error; 7.27 versus 8 is inside it.
- Fraud loss is more than the goods: fees, network penalties, investigation.
- Fraudsters adapt, so 12% precision changes.
- The retention test measures 90 days; longer-run loss may be larger.

**What the interviewer scores:**
- Strong: computes both costs, using genuine share only for friction. Weak: applies friction to all flagged.
- Strong: gives a break-even (13.0%) and says how close 12% is. Weak: says "decline since fraud costs 80."
- Strong: lists missing costs and a third option. Weak: no extras.
- Strong: comments on uncertainty of the 8 points. Weak: treats it as exact.

**Example:** (illustrative numbers) 100,000 flagged: decline costs 1,056,000, allow costs 960,000 on these counted items. Weak answer: "12 in 100 are fraud at 80, block them all." Strong answer: "Counting retention, blocking costs 10.56 against 9.60; it is close, so I add fees and test a step-up."

**Code:**
```python
p_fraud, loss = 0.12, 80
gap, value = 0.92 - 0.84, 150
friction = gap * value
cost_decline = (1 - p_fraud) * friction
cost_allow = p_fraud * loss
print(f"friction per genuine decline {friction:.2f}; decline {cost_decline:.2f}; allow {cost_allow:.2f}; difference {cost_decline-cost_allow:+.2f}")
assert abs(friction - 12.0) < 1e-9 and abs(cost_decline - 10.56) < 1e-9 and abs(cost_allow - 9.60) < 1e-9
p_be = friction / (loss + friction)
print(f"break-even fraud share {p_be:.4f}")
assert abs(p_be - 12 / 92) < 1e-12 and p_fraud < p_be
gap_be = p_fraud * loss / ((1 - p_fraud) * value)
print(f"break-even retention gap {gap_be*100:.2f} points (observed 8)")
assert abs(gap_be - 9.6 / 132) < 1e-12 and gap_be < gap
# over 100,000 flagged transactions
print(f"per 100,000 flagged: decline {100_000*cost_decline:,.0f}; allow {100_000*cost_allow:,.0f}")
# add an assumed extra cost of allowing (chargeback fee 15 on the fraud) and see the flip
fee = 15
print(f"with a {fee} chargeback fee on allowed fraud: allow {p_fraud*(loss+fee):.2f}")
assert p_fraud * (loss + fee) > cost_decline
```

**Output (my run):**
```text
friction per genuine decline 12.00; decline 10.56; allow 9.60; difference +0.96
break-even fraud share 0.1304
break-even retention gap 7.27 points (observed 8)
per 100,000 flagged: decline 1,056,000; allow 960,000
with a 15 chargeback fee on allowed fraud: allow 11.40
```

**Follow-ups:**
- What if fraud share rises to 20%? Then allowing costs 16.00 against declining 9.60, so decline.
- What other cost matters most? Network chargeback limits and fees, plus the review cost if you step up.

**Common mistakes:**
- Charging friction on fraud cases too.
- Ignoring the retention value.
- Forgetting a step-up option.
- Treating a 0.96 gap as decisive.

### Q44 ⭐ 🟢 A company adds an AI add-on at 4.00 a month, with inference cost of 1.10 and payment fees of 0.12 per subscriber per month, against 90,000 a month of fixed team and platform cost. Compute the break-even number of subscribers, and say how the answer moves if heavy users push average inference cost to 2.50.
**Asked at:** AI-era support and GenAI cost material (2026 vendor and practitioner pages from Lorikeet, Twig, Voiceflow, aitimejournal, CloudZero, nOps, tianpan.co and a Gartner press-release headline on inference costs); mostly vendor-sourced, an emerging interview theme rather than a confirmed bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened
**Say this first (1 line):** Each subscriber contributes 4.00 - 1.10 - 0.12 = 2.78, so break-even is 90,000 / 2.78 = 32,374.1, which means 32,375 subscribers; if inference cost averages 2.50 it contributes 1.38 and break-even is 65,218, about double.

**Clarifying questions:**
- Are payment fees a flat 0.12 or a percentage of price? If a percentage, they move with the price.
- Is 90,000 a month fixed regardless of subscriber count? Support and infrastructure may step up with scale.
- Does 1.10 average over all users or only light users? Averages hide the heavy-user tail.
- Is any of the add-on revenue shared with an app store? That cuts the 4.00.
- Will subscribers churn at some rate? Break-even is a monthly count, not a lifetime view.

**Approach:**
1. Contribution per subscriber = price - inference - fees = 4.00 - 1.10 - 0.12 = 2.78.
2. Break-even = fixed / contribution = 90,000 / 2.78 = 32,374.1, so round up to 32,375.
3. Stress: at 2.50 inference, contribution = 1.38, break-even 90,000 / 1.38 = 65,217.4, so 65,218 (2.01 times higher).
4. Sensitivity: the add-on makes zero contribution when inference reaches 3.88 (4.00 - 0.12).
5. Heavy users: the average hides a tail. In an illustrative mix of 80% at 1.00 and 20% at 8.50, the mean is 2.50 but each heavy user loses 4.62 a month.
6. Levers: usage caps or fair-use limits, a cheaper model for simple requests, tiered pricing, or a heavier price for heavy users.

**Metrics:**
- Contribution per subscriber = price - variable cost (inference + fees).
- Break-even subscribers = fixed cost / contribution per subscriber (round up).
- Inference cost per subscriber: mean, median and the top-decile share.
- Guardrails: attach rate, churn, gross margin by usage decile.

**Risks:**
- Heavy users concentrate the cost.
- Inference prices and usage per user change over time.
- Break-even subscribers may be more than the achievable market.
- Fixed costs may grow with scale.

**What the interviewer scores:**
- Strong: rounds up to whole subscribers and shows the contribution step. Weak: 90,000 / 4.
- Strong: re-runs at 2.50 and notes the non-linear jump (about double). Weak: says "somewhat higher."
- Strong: asks about the distribution of cost, not just the mean. Weak: ignores it.
- Strong: proposes levers (caps, routing, tiers). Weak: no actions.

**Example:** (illustrative numbers) At 2.78 per subscriber, 32,375 subscribers cover 90,000 (32,375 x 2.78 = 90,002.5). At 1.38, 65,218 are needed. Weak answer: "About 22,500, since 90,000 / 4." Strong answer: "32,375, and if heavy users lift cost to 2.50 it doubles to 65,218."

**Code:**
```python
import math
price, fee, fixed = 4.00, 0.12, 90_000
c1 = price - 1.10 - fee
c2 = price - 2.50 - fee
n1, n2 = fixed / c1, fixed / c2
print(f"contribution {c1:.2f} -> break-even {n1:,.1f} -> {math.ceil(n1):,} subscribers")
print(f"contribution {c2:.2f} -> break-even {n2:,.1f} -> {math.ceil(n2):,} subscribers")
assert abs(c1 - 2.78) < 1e-9 and math.ceil(n1) == 32_375
assert abs(c2 - 1.38) < 1e-9 and math.ceil(n2) == 65_218
print(f"ratio {n2/n1:.2f}x; inference cost at which contribution is zero: {price-fee:.2f}")
assert abs(n2 / n1 - 2.0144) < 1e-3
# a mix: 80% light users at 0.90, 20% heavy at 6.20 gives mean 2.14
mean = 0.8 * 1.00 + 0.2 * 8.50
print(f"example mix (80% at 1.00, 20% at 8.50) has mean {mean:.2f}; a heavy user alone makes {price-8.50-fee:.2f} per month")
assert abs(mean - 2.50) < 1e-9
assert price - 8.50 - fee < 0
```

**Output (my run):**
```text
contribution 2.78 -> break-even 32,374.1 -> 32,375 subscribers
contribution 1.38 -> break-even 65,217.4 -> 65,218 subscribers
ratio 2.01x; inference cost at which contribution is zero: 3.88
example mix (80% at 1.00, 20% at 8.50) has mean 2.50; a heavy user alone makes -4.62 per month
```

**Follow-ups:**
- What price would restore the original break-even at 2.50 inference? Price = 2.78 + 2.50 + 0.12 = 5.40.
- How would you find heavy users? Cost per subscriber by decile; cap or reprice the top.

**Common mistakes:**
- Dividing fixed cost by price, not contribution.
- Not rounding up.
- Using the mean and ignoring the tail.
- Forgetting payment fees.

### Q45 ⭐ 🟢 Estimate the revenue pool for a data product in a country with 40,000 firms, of which 12% have more than 50 staff, with 25% of those expected to adopt within 3 years at 2,400 a year. Compute the annual revenue pool, show how adoption of 10% to 40% moves it, and say which input you would validate with data first.
**Asked at:** Market-sizing and unit-economics material (PracHub market-sizing concept page, MBB Prep unit-economics and market-sizing pages, PrepLounge break-even and Leland and RoadToOffer sizing guides); consulting-case guides rather than data-scientist-specific pages; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** The pool is 40,000 x 12% x 25% x 2,400 = 2.88 million a year (illustrative), and the input I would check first is the adoption rate, because it is the least known and moves the answer 4x between 10% and 40%.

**Clarifying questions:**
- Is "firms" all registered firms or active ones? Many registered firms are dormant, so the base could be too high.
- Is the 25% adoption at the end of year 3, or an average over 3 years? It changes whether 2.88 million is a year-3 run rate or a 3-year average.
- Is 2,400 a year the list price or what firms actually pay after discounts? Revenue pool should use paid price.
- Do firms with 50 staff or fewer matter at all? If they would buy a cheaper tier, the pool is understated.
- Is this the pool for the whole market or the share we could win? A pool is not our revenue.

**Approach:**
1. Write the chain: firms x share in scope x adoption x price.
2. Compute: 40,000 x 12% = 4,800 firms. 25% of 4,800 = 1,200 adopters. 1,200 x 2,400 = 2,880,000 a year.
3. Sweep adoption 10% to 40%: 1,152,000 to 4,608,000. Revenue is linear in adoption, so 40% gives exactly 4x the 10% case.
4. Rank inputs by uncertainty times leverage. Each input is a straight multiplier, so a 10% relative error in any of them gives a 10% error in revenue. The input with the widest plausible range is the one to validate.
5. Name data for it: a pilot conversion rate, win/loss from sales calls, a survey with real purchase intent, adoption of a similar tool in a neighbouring market.
6. Present a range, not one number, and say what we would do at the low end.

**Metrics:**
- Revenue pool = firms in scope x adoption rate x annual price. Numerator: money paid per year. Denominator: not a ratio.
- Adoption rate = adopting in-scope firms / all in-scope firms (1,200 / 4,800 = 25%).
- Guardrail: compare against a top-down check, for example spend per firm on all software. If 2,400 is a large share of that, adoption is probably too high.

**Risks:**
- Stated intent in surveys overstates real purchases.
- The 12% size share may count branches or shells as firms.
- The pool is a ceiling for the product, not a forecast for our revenue.
- One year-3 snapshot hides the ramp: years 1 and 2 earn less.

**What the interviewer scores:**
- Strong: clean chain, arithmetic right, a range, picks the input to validate and says why with data named. Weak: gives one number and says "adoption is uncertain" with no way to test it.
- Strong: separates market pool from our share. Weak: treats the pool as our revenue.
- Strong: notes the linear structure, so each input is equally sensitive per percent. Weak: ranks inputs by gut.

**Example:** Illustrative numbers. 4,800 big firms x 25% = 1,200 adopters x 2,400 = 2.88 million. At 10% adoption: 1.152 million. At 40%: 4.608 million. Weak: "about 3 million, looks good." Strong: "2.9 million at 25%, but 1.2 to 4.6 million across adoption of 10% to 40%, so I would run a paid pilot with 50 firms before investing."

**Code:**
```python
firms=40_000; big_share=0.12; adopt=0.25; price=2_400
big=firms*big_share
adopters=big*adopt
pool=adopters*price
print("firms >50 staff:",big)
print("adopters:",adopters)
print("annual revenue pool:",pool)
assert big==4_800 and adopters==1_200 and pool==2_880_000

print("\nAdoption sweep (firms and price fixed)")
sweep={}
for a in (0.10,0.20,0.25,0.30,0.40):
    sweep[a]=big*a*price
    print(f"  adoption {a:.0%}: {big*a:,.0f} firms -> {sweep[a]:,.0f}")
assert sweep[0.10]==1_152_000 and sweep[0.40]==4_608_000
assert abs(sweep[0.40]/sweep[0.10]-4)<1e-9

print("\nOne-at-a-time swing, each input at its own illustrative low/high")
rng={"adoption share":(0.10,0.40,adopt),
     "share of firms >50 staff":(0.08,0.15,big_share),
     "price per year":(1_800,3_000,price)}
base=dict(a=adopt,s=big_share,p=price)
def f(a,s,p): return firms*s*a*p
swing={}
for name,(lo,hi,mid) in rng.items():
    k={"adoption share":"a","share of firms >50 staff":"s","price per year":"p"}[name]
    lo_v=f(**{**base,k:lo}); hi_v=f(**{**base,k:hi})
    swing[name]=hi_v-lo_v
    print(f"  {name:28s} {lo_v:>10,.0f} to {hi_v:>10,.0f}  swing {hi_v-lo_v:>10,.0f}")
assert max(swing,key=swing.get)=="adoption share"
```

**Output (my run):**
```
firms >50 staff: 4800.0
adopters: 1200.0
annual revenue pool: 2880000.0

Adoption sweep (firms and price fixed)
  adoption 10%: 480 firms -> 1,152,000
  adoption 20%: 960 firms -> 2,304,000
  adoption 25%: 1,200 firms -> 2,880,000
  adoption 30%: 1,440 firms -> 3,456,000
  adoption 40%: 1,920 firms -> 4,608,000

One-at-a-time swing, each input at its own illustrative low/high
  adoption share                1,152,000 to  4,608,000  swing  3,456,000
  share of firms >50 staff      1,920,000 to  3,600,000  swing  1,680,000
  price per year                2,160,000 to  3,600,000  swing  1,440,000
```

**Follow-ups:**
- *Which input would you validate if adoption were already known?* The price, through a willingness-to-pay test on real quotes.
- *How do you turn the pool into our revenue?* Multiply by an achievable share and a ramp over the years. Part 5 Q19 shows break-even logic for the investment decision.
- *Top-down check?* Compare 2,400 a year against what a firm of that size spends in total on similar tools.

**Common mistakes:**
- Treating 25% as certain.
- Forgetting the 12% filter, or applying it twice.
- Calling the pool "our revenue".
- Sweeping adoption but leaving price and size fixed and calling it a sensitivity analysis.

### Q46 ⭐ 🟡 A vendor fraud model costs 300,000 a year and prevents 70% of 2,000,000 a year of fraud losses (1.4 million). An in-house model costs 500,000 in year 1 and 150,000 a year afterwards, and is expected to prevent 76% (1.52 million). Compute the 3-year net benefit of each and the difference, and say what makes the in-house number optimistic.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** Vendor nets 3.30 million over 3 years, in-house nets 3.76 million, so in-house looks 460,000 better (illustrative), but it wins only if it really prevents more than about 68.3% of losses and ships on time.

**Clarifying questions:**
- Is the 76% measured on our data or a forecast? A forecast from a build plan is usually optimistic.
- How long until the in-house model is live? The 500,000 in year 1 may buy no protection for months.
- Does 150,000 a year cover retraining, monitoring, on-call and labelling? Run cost is the usual hole.
- Does the vendor price rise at renewal? That moves the comparison the other way.
- Are the two prevention rates measured on the same transactions and the same false-positive cost? A model that prevents more but blocks more good customers is not comparable.

**Approach:**
1. Benefit per year = prevention rate x 2,000,000. Vendor 1,400,000. In-house 1,520,000.
2. Net each year = benefit - cost. Sum 3 years.
3. Vendor: 3 x (1,400,000 - 300,000) = 3,300,000.
4. In-house: 3 x 1,520,000 - (500,000 + 150,000 + 150,000) = 4,560,000 - 800,000 = 3,760,000.
5. Difference: 460,000 in favour of in-house.
6. Stress it: find the in-house prevention rate that only ties the vendor, then delay, run-cost and prevention scenarios.
7. Decide: the difference is about 14% of the vendor net, which is small next to the uncertainty. Pilot the vendor, then build only if the in-house shadow test beats it on our data.

**Metrics:**
- Net benefit = losses prevented - total cost, summed over the horizon. Prevention rate = fraud loss stopped / fraud loss without a model.
- Guardrails: false-positive rate and customer friction, time to live, and discounted values if the horizon were longer (no discounting used here).

**Risks:**
- Year-1 delay: if in-house is live for half of year 1, its net falls to 3.0 million and it loses to the vendor by 300,000.
- Prevention is the biggest lever: 1 point of prevention is worth 60,000 over 3 years, so a 7.7 point miss (460,000 / 60,000) erases the 460,000 lead.
- Fraud losses of 2,000,000 are themselves an estimate, and fraudsters adapt.
- Staff cost, key-person risk, and the vendor's data advantage across many clients.

**What the interviewer scores:**
- Strong: correct arithmetic, finds the break-even prevention rate, names delay and run cost. Weak: quotes 460,000 as fact.
- Strong: asks for a shadow test on our data. Weak: trusts both rates.
- Strong: mentions risk, lock-in and option value, not only total. Weak: pure cost comparison.

**Example:** Illustrative numbers. Vendor 3.3 million, in-house 3.76 million. If in-house prevents only 70%, its net is 3.4 million and the lead is 100,000. If it also goes live 6 months late, in-house loses. Weak: "In-house is 460k better, build it." Strong: "It is better only if prevention stays above 68.3% and it ships on time. I would shadow-test first."

**Code:**
```python
loss=2_000_000; years=3
vendor_cost=[300_000]*3
inh_cost=[500_000,150_000,150_000]
vendor_prev=0.70; inh_prev=0.76
v_ben=vendor_prev*loss; i_ben=inh_prev*loss
assert v_ben==1_400_000 and i_ben==1_520_000
v_net=sum(v_ben-c for c in vendor_cost)
i_net=sum(i_ben-c for c in inh_cost)
print("vendor 3-yr net:",v_net)
print("in-house 3-yr net:",i_net)
print("difference (in-house minus vendor):",i_net-v_net)
assert v_net==3_300_000 and i_net==3_760_000 and i_net-v_net==460_000

# in-house prevention rate at which it only ties vendor
tie=(v_net+sum(inh_cost))/(loss*years)
print(f"break-even in-house prevention rate: {tie:.4f}")
assert abs(tie-0.683333)<1e-5 and tie<vendor_prev

print("\nOptimism checks (illustrative)")
# a) year-1 delay: in-house model live for only 6 months of year 1
i_delay=i_net-0.5*i_ben
print("  in-house net if year 1 is half-live:",i_delay, "diff:",i_delay-v_net)
assert i_delay==3_000_000 and i_delay-v_net==-300_000
# b) prevention falls to 70% (same as vendor)
i_70=sum(0.70*loss-c for c in inh_cost)
print("  in-house net at 70% prevention:",i_70,"diff:",i_70-v_net)
assert abs(i_70-3_400_000)<1e-6 and abs(i_70-v_net-100_000)<1e-6
# c) a 1 percentage point prevention change is worth this over 3 years
print("  value of 1 prevention point over 3 years:",0.01*loss*years)
assert 0.01*loss*years==60_000
# d) maintenance cost doubles after year 1
i_m=sum(i_ben-c for c in [500_000,300_000,300_000])
print("  in-house net if run cost is 300k/yr after year 1:",i_m,"diff:",i_m-v_net)
assert i_m==3_460_000
print("  lead as share of vendor net:",round(460_000/v_net,3),"; points of prevention to erase lead:",round(460_000/60_000,2))
assert round(460_000/v_net,2)==0.14 and round(460_000/60_000,1)==7.7
```

**Output (my run):**
```
vendor 3-yr net: 3300000.0
in-house 3-yr net: 3760000.0
difference (in-house minus vendor): 460000.0
break-even in-house prevention rate: 0.6833

Optimism checks (illustrative)
  in-house net if year 1 is half-live: 3000000.0 diff: -300000.0
  in-house net at 70% prevention: 3400000.0 diff: 100000.0
  value of 1 prevention point over 3 years: 60000.0
  in-house net if run cost is 300k/yr after year 1: 3460000.0 diff: 160000.0
  lead as share of vendor net: 0.139 ; points of prevention to erase lead: 7.67
```

**Follow-ups:**
- *Would discounting change it?* Slightly. In-house costs are front-loaded, so discounting hurts it a little.
- *Hybrid?* Buy now, build in parallel, switch when the in-house model beats the vendor in shadow mode.
- *What if the vendor prevention is 70% on its own data, not ours?* Then both numbers need re-measuring on our traffic.

**Common mistakes:**
- Ignoring the build timeline.
- Leaving out the maintenance cost.
- Comparing prevention rates without comparing false positives.
- Treating the 460,000 difference as precise.

### Q47 ⭐ 🟡 A dark store costs 80,000 a month in fixed costs and serves an area expected to give 24,000 orders a month, cutting delivery cost from 3.20 to 2.10 per order (1.10 saved). Compute the break-even monthly orders and the monthly result at forecast volume, and say what else could justify it.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** On delivery savings alone the dark store needs about 72,727 orders a month, which is 3.03 times the 24,000 forecast, and at forecast it loses 53,600 a month (illustrative), so it needs another source of value to be justified.

**Clarifying questions:**
- Is the 1.10 saved a true marginal saving, or an average that includes costs that will not really go away? A saving only counts if the cost leaves.
- Is the 80,000 all fixed, including staff shifts? If staff scale with orders, break-even changes.
- Are the 24,000 orders new orders or orders that would have come from the old stores anyway? Moved orders add only the saving, new orders add margin too.
- What is the order margin before delivery cost? Needed to value extra orders.
- How fast does volume ramp, and for how long can we fund losses?

**Approach:**
1. Contribution per order = saving = 3.20 - 2.10 = 1.10.
2. Break-even orders = fixed cost / contribution = 80,000 / 1.10 = 72,727.3 a month.
3. Result at forecast = 24,000 x 1.10 - 80,000 = 26,400 - 80,000 = -53,600 a month.
4. Frame the gap: fixed cost per forecast order is 3.33 against a 1.10 saving. The saving would need to be 3.33 per order, or volume 3x.
5. Ask what else changes: faster delivery lifting order frequency and basket, fewer late orders and refunds, stock availability, a lower promo need, strategic coverage, option value for growth.
6. Value those with a test or a similar existing store, not by assertion. If extra margin on incremental orders is, for example, 2.23 per forecast order, it would close the gap. That is the number to test.
7. Recommend: do not open on savings alone. Open only if the extra effects are shown, or if the volume forecast is raised with evidence.

**Metrics:**
- Break-even orders = monthly fixed cost / contribution per order.
- Monthly result = orders x contribution - fixed cost.
- Guardrails: delivery time, late rate, order growth in the zone, cannibalisation of nearby stores.

**Risks:**
- Volume forecast and saving per order are both uncertain; the answer is very sensitive to volume.
- Saving per order may fall if the store is under-used (couriers idle).
- Ramp-up: months of losses before volume arrives. At 5% monthly growth it takes 23 months to reach 72,727.
- Cannibalising an existing profitable store.

**What the interviewer scores:**
- Strong: says plainly it does not break even at forecast and quantifies the gap. Weak: computes break-even and says "we will grow into it".
- Strong: separates incremental orders from moved orders. Weak: counts all 24,000 as new.
- Strong: proposes what to test (pilot zone, volume ramp). Weak: lists benefits with no numbers.

**Example:** Illustrative numbers. Break-even 72,727. Forecast 24,000. Result -53,600 a month. Weak: "Break-even is 72,727 orders, so we need to grow." Strong: "At forecast it loses 53,600 a month. It needs 3.03x volume, or about 2.23 extra margin per order from other effects. I would pilot before committing."

**Code:**
```python
fixed=80_000; orders=24_000; save=3.20-2.10
assert abs(save-1.10)<1e-12
be=fixed/save
print(f"break-even orders/month: {be:,.1f}  ({be/orders:.2f}x forecast)")
res=orders*save-fixed
print("monthly result at forecast:",round(res,2))
print(f"fixed cost per forecast order: {fixed/orders:.2f} vs saving per order {save:.2f}")
assert round(be,1)==72_727.3 and round(res,2)==-53_600.00
assert 3<be/orders<3.1
# what would have to be true at forecast volume
need_save=fixed/orders
print(f"saving per order needed at 24,000 orders: {need_save:.2f}")
assert round(need_save,2)==3.33
# what other value could close the gap
gap=-res
print("gap per month:",round(gap,2),"= per forecast order:",round(gap/orders,2))
assert round(gap/orders,2)==2.23
# volume growth: months of growth at 5%/month to reach break-even
m=0; v=orders
while v<be:
    v*=1.05; m+=1
print("months at 5% monthly growth to reach break-even:",m)
assert m==23
```

**Output (my run):**
```
break-even orders/month: 72,727.3  (3.03x forecast)
monthly result at forecast: -53600.0
fixed cost per forecast order: 3.33 vs saving per order 1.10
saving per order needed at 24,000 orders: 3.33
gap per month: 53600.0 = per forecast order: 2.23
months at 5% monthly growth to reach break-even: 23
```

**Follow-ups:**
- *How would you cut the break-even?* Lower fixed cost (smaller store, shared staff), raise saving per order (batching), or raise margin per order.
- *Would you open it anyway?* Only if the strategic value is stated and capped, for example a fixed budget for a fixed number of months.
- *What is the single most important number?* Volume, since break-even is 3 times the forecast.

**Common mistakes:**
- Stopping at the break-even number without comparing it to the forecast.
- Counting moved orders as incremental.
- Treating average cost savings as marginal.
- Ignoring the ramp period.

### Q48 ⭐ 🟡 A 100-room hotel sells 70 rooms a night at 100 and expects to sell 62 at 120, about 11% fewer than 70, with 20 of variable cost per occupied room. Compute nightly profit at each price, and say why a flat comparison is not enough when demand varies by night.
**Asked at:** Dynamic-pricing and surge material (a Dataford surge-pricing switchback question, Codemia and Final Round AI pages on designing surge pricing for Uber or Lyft, a Prepfully pricing-riders product case, a Glassdoor Uber entry as listed in snippets); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** At 120 the hotel makes 62 x 100 = 6,200 a night against 70 x 80 = 5,600 at 100, so 120 wins by 600 on the average night (illustrative), but demand and price sensitivity change by night, so I would price by night, not pick one flat price.

**Clarifying questions:**
- Where do the 70 and 62 come from? Average of a test, a model forecast, or a guess? A guess makes the whole comparison weak.
- Does the 62 at 120 hold on every night or only on average? Weekend and weekday demand differ a lot.
- Is 20 the only variable cost? Cleaning, commissions and breakfast can change the margin per room.
- Can the hotel see turned-away demand (sold-out nights)? Without it, sales understate demand.
- Do guests who see 120 go to a competitor or book another night? That decides whether lost rooms come back.

**Approach:**
1. Margin per room: at 100 it is 80, at 120 it is 100.
2. Profit at 100: 70 x 80 = 5,600. At 120: 62 x 100 = 6,200. Difference: +600 a night.
3. The demand fall implied is 1 - 62/70 = 11.4%, which the prompt rounds to about 11%.
4. Break-even: 120 needs only 5,600 / 100 = 56 rooms, a 20% fall from 70. So 120 wins unless demand falls by more than 20%.
5. Now add nights. Capacity is 100 rooms. On a peak night demand at 100 already exceeds 100, so raising the price loses nobody and every room earns 20 more. On a soft night, the room loss is real.
6. Simulate (illustrative demand, mean 70, sd 20, capped at 100 rooms): flat 120 beats flat 100 by about 640 a night. Gains are about 1,960 on peak nights and 339 on soft nights.
7. If soft nights are more price sensitive (they lose 40% at 120, strong nights 0%), flat 120 earns 5,862, flat 100 earns 5,555, and pricing by night earns 6,403. Price by night wins.
8. To estimate sensitivity by night type, run price tests by randomised dates or room types, controlling for day of week and events.

**Metrics:**
- Profit per available room night = rooms sold x (price - variable cost) / rooms available. Revenue per available room is a guardrail but ignores cost.
- Occupancy = rooms sold / 100. Sell-out share = nights with demand at or above capacity / all nights.
- Guardrails: repeat bookings, review score, cancellation rate.

**Risks:**
- Averages hide the sell-out nights, where sales are capped and demand is censored.
- Price effects differ by segment and season.
- Competitor prices and events move demand independently of our price.
- Selection: a price change tested on quiet weeks looks worse than it is.

**What the interviewer scores:**
- Strong: correct profit, break-even demand fall, and the capacity point (sold-out nights give free price increases). Weak: compares 70 x 100 with 62 x 120 using revenue only, forgetting variable cost.
- Strong: proposes price by night with randomised testing. Weak: says "just run an A/B test" with no thought about dates or capacity.
- Strong: notes the 70 is censored on busy nights. Weak: treats observed sales as demand.

**Example:** Illustrative numbers. 70 x 80 = 5,600 against 62 x 100 = 6,200. Break-even is 56 rooms. Weak: "120 is better, by 600, ship it." Strong: "On average yes, but I would raise price on the peak nights first, and test the soft nights separately, because the gain is mostly from nights that are already full."

**Code:**
```python
import numpy as np
cap=100; vc=20
p0,p1=100,120
q0,q1=70,62
pr0=q0*(p0-vc); pr1=q1*(p1-vc)
print("nightly profit at 100:",pr0," at 120:",pr1," difference:",pr1-pr0)
drop=1-q1/q0
print(f"demand drop implied by 62 vs 70: {drop:.4f}")
assert pr0==5_600 and pr1==6_200 and round(drop,3)==0.114
# break-even rooms at 120
be=pr0/(p1-vc)
print("break-even rooms at 120:",be,"=> relative drop",round(1-be/q0,3))
assert be==56 and round(1-be/q0,3)==0.2

# nightly demand varies. Illustrative: demand at 100 ~ Normal(70,20) truncated at 0; at 120 it is 62/70 of that
rng=np.random.default_rng(7)
d0=np.clip(rng.normal(70,20,200_000),0,None)
d1=d0*(q1/q0)
s0=np.minimum(d0,cap); s1=np.minimum(d1,cap)
print(f"\nSimulated mean demand at 100: {d0.mean():.1f}; mean rooms sold: {s0.mean():.1f}")
print(f"Mean rooms sold at 120: {s1.mean():.1f}")
m0=(s0*(p0-vc)).mean(); m1=(s1*(p1-vc)).mean()
print(f"Average nightly profit at 100: {m0:.0f}; at 120: {m1:.0f}; difference {m1-m0:.0f}")
print(f"Share of nights sold out at 100: {(d0>=cap).mean():.3f}; at 120: {(d1>=cap).mean():.3f}")
# by demand band
for lo,hi in [(0,50),(50,80),(80,110),(110,500)]:
    k=(d0>=lo)&(d0<hi)
    a=(s0[k]*(p0-vc)).mean(); b=(s1[k]*(p1-vc)).mean()
    print(f"  base demand {lo:>3}-{hi:<3}: profit at 100 {a:7.0f}, at 120 {b:7.0f}, 120 better? {b>a}")
assert s0.mean()<d0.mean()           # capacity censors sales
assert m1>m0
# with a uniform 11.4% drop, 120 beats 100 on every band; the gain is largest on sell-out nights
k=d0>=110; g_peak=(s1[k]*(p1-vc)).mean()-(s0[k]*(p0-vc)).mean()
k=d0<50; g_weak=(s1[k]*(p1-vc)).mean()-(s0[k]*(p0-vc)).mean()
print(f"gain on peak nights {g_peak:.0f} vs weak nights {g_weak:.0f}")
assert g_peak>g_weak>0

# demand differs by night: soft nights (base demand < 70) lose 40% at 120, strong nights lose 0% (illustrative)
drop_n=np.where(d0<70,0.40,0.0)
d1b=d0*(1-drop_n)
s1b=np.minimum(d1b,cap)
flat120=(s1b*(p1-vc)).mean()
by_night=np.where(d0<70,s0*(p0-vc),s1b*(p1-vc)).mean()   # price 100 on soft nights, 120 on strong nights (needs a demand forecast)
print(f"\nSoft nights lose 40%, strong nights 0%: avg rooms at flat 120 = {s1b.mean():.1f}")
print(f"  flat 100: {m0:.0f}  flat 120: {flat120:.0f}  price by night: {by_night:.0f}")
assert by_night>flat120>m0
print(f"  average drop in rooms at flat 120 vs flat 100: {1-s1b.mean()/s0.mean():.3f} (a flat test would call this a ~{(1-s1b.mean()/s0.mean())*100:.0f}% drop)")
print("\nRevenue-only check:",q0*p0,q1*p1,(q1*p1-q0*p0),"plus saved variable cost",(q0-q1)*vc)
assert q0*p0==7_000 and q1*p1==7_440 and (q0-q1)*vc==160 and (q1*p1-q0*p0)+(q0-q1)*vc==600
```

**Output (my run):**
```
nightly profit at 100: 5600  at 120: 6200  difference: 600
demand drop implied by 62 vs 70: 0.1143
break-even rooms at 120: 56.0 => relative drop 0.2

Simulated mean demand at 100: 70.0; mean rooms sold: 69.4
Mean rooms sold at 120: 61.9
Average nightly profit at 100: 5555; at 120: 6192; difference 637
Share of nights sold out at 100: 0.067; at 120: 0.016
  base demand   0-50 : profit at 100    3161, at 120    3499, 120 better? True
  base demand  50-80 : profit at 100    5271, at 120    5836, 120 better? True
  base demand  80-110: profit at 100    7217, at 120    8049, 120 better? True
  base demand 110-500: profit at 100    8000, at 120    9960, 120 better? True
gain on peak nights 1960 vs weak nights 339

Soft nights lose 40%, strong nights 0%: avg rooms at flat 120 = 58.6
  flat 100: 5555  flat 120: 5862  price by night: 6403
  average drop in rooms at flat 120 vs flat 100: 0.156 (a flat test would call this a ~16% drop)

Revenue-only check: 7000 7440 440 plus saved variable cost 160
```

**Follow-ups:**
- *Why does revenue alone mislead?* 70 x 100 = 7,000 vs 62 x 120 = 7,440, a gap of 440 instead of 600, because it misses the 160 of variable cost saved on the 8 rooms not sold (440 + 160 = 600).
- *How do you measure demand on sold-out nights?* Log turned-away requests, searches and abandoned bookings, or fit a censored model like Part 5 Q53.
- *Could this be a bandit?* Yes, once you have a few price points and enough nights.

**Common mistakes:**
- Using revenue instead of profit.
- Using one average demand drop for every night.
- Ignoring the capacity cap.
- Testing price on a few nights and attributing weekday-weekend swings to price.

### Q49 ⭐ 🟡 A growth team issued 100,000 first-order vouchers worth 6 each, and 25,000 were redeemed. An audit estimates that 20% of redeemers (5,000) would have ordered anyway, so 20,000 are new customers, each delivering 9 of 90-day margin before the voucher cost. Compute the voucher cost per incremental customer and the net value, and say how you would measure the 20% share.
**Asked at:** Promotion and incrementality material (Talon.One and Uniqodo pages on promotion ROI and incrementality, an INFORMS Management Science paper on whether coupons expand or cannibalise revenue, an incrmntal post on promos and ad spend); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** Voucher cost is 25,000 x 6 = 150,000; with 20,000 incremental customers that is 7.50 per incremental customer, and the net is 20,000 x 9 - 150,000 = +30,000 (illustrative), but it turns negative once more than a third of redeemers would have ordered anyway.

**Clarifying questions:**
- How was the 20% "would have ordered anyway" estimated? If by survey or by matching, it is shaky. A randomised holdout is the proper answer.
- Is the 9 of 90-day margin net of delivery, support and fraud? It must be contribution, not revenue.
- Do the 5,000 non-incremental redeemers still get the 6? Yes, and that cost is already in the 150,000.
- Is there any value after day 90? A 90-day window ignores later orders and also ignores later churn.
- Was there voucher abuse (multiple accounts)? Abuse inflates both redemptions and "new" customers.

**Approach:**
1. Cost: redeemed x value = 25,000 x 6 = 150,000. Unredeemed vouchers cost nothing.
2. Incremental customers: 25,000 x (1 - 0.20) = 20,000.
3. Cost per incremental customer = 150,000 / 20,000 = 7.50, against 9 of margin each.
4. Net = 20,000 x 9 - 150,000 = +30,000. Only incremental customers count for margin; the 5,000 would have ordered anyway so their margin is not caused by the voucher.
5. Break-even: 150,000 / 9 = 16,667 incremental customers, which is 66.7% of redeemers. So the non-incremental share can be up to 33.3% before the net is zero.
6. At 40% non-incremental the net is -15,000. The decision is sensitive to a number we only estimated.
7. Measure the share: randomise vouchers (for example 50% eligible, 50% not), compare first-order rates, and count the incremental share as (treated rate - control rate) x eligible / redeemers. Run it long enough to see pull-forward and later retention.

**Metrics:**
- Cost per incremental customer = total voucher cost / (treated first-order customers - control first-order customers, scaled to group size).
- Net value = incremental customers x contribution margin - voucher cost.
- Guardrails: later repeat rate, abuse flags, margin after the voucher period.

**Risks:**
- Audit estimate of 20% is soft; the net swings from +75,000 (0%) to -60,000 (60%).
- Pull-forward: users who would have ordered next week order now.
- Voucher-hunters churn after the voucher.
- Unequal groups if the audit compares redeemers with non-redeemers (selection).

**What the interviewer scores:**
- Strong: costs only redeemed vouchers, counts margin only for incremental customers, gives break-even share. Weak: 100,000 x 6 as cost, or counts margin from all 25,000.
- Strong: proposes a randomised holdout and explains how to read it. Weak: "ask users in a survey".
- Strong: mentions long-run value and abuse. Weak: stops at day 90.

**Example:** Illustrative numbers. 20,000 x 9 = 180,000 margin, minus 150,000 cost, gives +30,000. At 40% non-incremental, 15,000 x 9 = 135,000, a loss of 15,000. Weak: "30% redemption... fine." Strong: "It pays only while at least two thirds of redeemers are truly new. I would randomise the next voucher wave to measure that."

**Code:**
```python
issued=100_000; value=6; redeemed=25_000
cost=redeemed*value
non_incr=0.20*redeemed
incr=redeemed-non_incr
margin=9
print("voucher cost:",cost,"incremental customers:",incr)
cpic=cost/incr
net=incr*margin-cost
print("voucher cost per incremental customer:",cpic)
print("net value:",net)
assert cost==150_000 and incr==20_000 and cpic==7.5 and net==30_000
print("redemption rate:",redeemed/issued)
# break-even incremental share
be_inc=cost/margin
print(f"break-even incremental customers: {be_inc:,.0f} = {be_inc/redeemed:.4f} of redeemers (non-incremental share {1-be_inc/redeemed:.4f})")
assert round(be_inc)==16_667 and round(1-be_inc/redeemed,3)==0.333
print("\nSensitivity to the non-incremental share:")
for s in (0.0,0.2,1/3,0.4,0.6):
    inc=redeemed*(1-s); print(f"  {s:.2%} non-incremental: incremental {inc:>7,.0f}, net {inc*margin-cost:>9,.0f}, cost per incremental {cost/inc:5.2f}")
assert 20_000*margin-cost>0 and 15_000*margin-cost<0
# measuring the share with a randomised holdout (illustrative, built to match the audit's 20%):
# 100,000 eligible users get vouchers, 100,000 do not. Organic first-order rate 5%. 25% redeem; 80% of redeemers are new.
import numpy as np
rng=np.random.default_rng(11)
n=100_000
p_ctrl=0.05
p_treat=0.05+0.20      # 5,000 organic orders + 20,000 voucher-driven new orders
c=rng.binomial(n,p_ctrl); t=rng.binomial(n,p_treat)
lift=t/n-c/n
se=((t/n)*(1-t/n)/n+(c/n)*(1-c/n)/n)**0.5
print(f"\nHoldout sim: treated first-order rate {t/n:.4f}, control {c/n:.4f}, lift {lift:.4f} +/- {1.96*se:.4f}")
redeemers=redeemed
inc_share=lift*n/redeemers
print(f"measured incremental share of redeemers: {inc_share:.3f} (design value 0.800); non-incremental {1-inc_share:.3f}")
assert abs(lift-0.20)<4*se and abs(inc_share-0.8)<0.03
```

**Output (my run):**
```
voucher cost: 150000 incremental customers: 20000.0
voucher cost per incremental customer: 7.5
net value: 30000.0
redemption rate: 0.25
break-even incremental customers: 16,667 = 0.6667 of redeemers (non-incremental share 0.3333)

Sensitivity to the non-incremental share:
  0.00% non-incremental: incremental  25,000, net    75,000, cost per incremental  6.00
  20.00% non-incremental: incremental  20,000, net    30,000, cost per incremental  7.50
  33.33% non-incremental: incremental  16,667, net         0, cost per incremental  9.00
  40.00% non-incremental: incremental  15,000, net   -15,000, cost per incremental 10.00
  60.00% non-incremental: incremental  10,000, net   -60,000, cost per incremental 15.00

Holdout sim: treated first-order rate 0.2523, control 0.0495, lift 0.2028 +/- 0.0030
measured incremental share of redeemers: 0.811 (design value 0.800); non-incremental 0.189
```

**Follow-ups:**
- *Why not compare redeemers with non-redeemers?* Redeemers are the keen ones, so the gap overstates the effect. Compare the whole eligible group with a randomised control.
- *What if margin includes later orders?* Extend the window and discount it; the break-even share moves up.
- *Is there a cheaper design?* A smaller voucher or a threshold (for example spend 30 to get 6) can cut the non-incremental redeemers.

**Common mistakes:**
- Costing all 100,000 vouchers.
- Counting margin from non-incremental redeemers.
- Estimating the non-incremental share from redeemers versus non-redeemers.
- Ignoring abuse.

### Q50 ⭐ 🟡 A retailer with 1,000,000 orders a year and a 22% return rate (of orders) plans to charge 4.00 for returns, which it keeps as income on each returned order. It expects returns to fall to 18% of orders (4 points absolute) and orders to fall by 3% relative to today. A kept order earns 15 of margin, and a returned order earns nothing and costs 8 to handle. Compute annual margin before and after, and the relative order drop at which the change breaks even.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** Annual margin goes from 9.94 million to 11.23 million, a gain of 1.29 million (illustrative), and the policy breaks even only if orders fall by about 14.2%, against the 3% expected.

**Clarifying questions:**
- Is the 4.00 collected on every return, and is any of it passed on (payment or shipping pass-through)? The prompt says the retailer keeps it as income. Check that holds in practice.
- Is the return fall to 18% measured or hoped for? It is the biggest lever.
- Will the 3% order drop be spread evenly? Losing high-margin repeat buyers costs more than 3% of margin.
- Is the 8 handling cost only warehouse work? Refund processing and resale discount also matter.
- Does the fee apply to all returns or only some categories (for example fashion)?

**Approach:**
1. Before: 1,000,000 orders. Returned 220,000, kept 780,000. Margin = 780,000 x 15 - 220,000 x 8 = 11,700,000 - 1,760,000 = 9,940,000. Per order: 9.94.
2. After: orders = 970,000. Returns at 18% = 174,600. Kept = 795,400. Kept margin = 11,931,000. Handling = 1,396,800.
3. Add fee income: + 174,600 x 4 = 698,400. Margin = 11,232,600, a gain of 1,292,600.
4. Sensitivity: if the fee brought in no income at all, margin would be 10,534,200 and the break-even order drop would be 8.47%. So fee income is a large part of the gain.
5. Break-even drop in orders: per-order margin after is 11.58. Orders can fall until 11.58 x N = 9.94 million. N = 858,377, a relative fall of 14.16%.
6. Sensitivity (fee kept, 3% fewer orders): returns at 20% give 10,864,000; returns unchanged at 22% give 10,495,400, still above 9,940,000 only because of fee income. So the gain depends on the fee income and on the return rate falling.
7. Test: randomise the fee by user or region and measure orders, return rate, and 6-month repeat purchase.

**Metrics:**
- Margin per original order = (kept orders x 15 - returned orders x 8 + returned orders x fee) / original orders.
- Return rate = returned orders / orders. Order retention = orders after / orders before.
- Guardrails: conversion, repeat rate, customer-service contacts, share of lost orders that were low-return buyers.

**Risks:**
- Selection: the 3% of lost orders may be the customers with high return rates (good for margin) or loyal ones (bad).
- Customers may switch to a rival, with long-run effects beyond a year.
- Some of the return fall is mix shift (buyers who return a lot now order less), so the 18% and the 3% are linked.
- Fee could cause chargebacks or complaints.

**What the interviewer scores:**
- Strong: separates kept, returned, and fee income, and states the fee assumption. Weak: multiplies orders by 15 only.
- Strong: solves break-even for the order drop with per-order margins. Weak: tries a fixed table by trial and error.
- Strong: proposes a randomised test and a long window. Weak: trusts the forecast.

**Example:** Illustrative numbers. Before 9,940,000. After with fee 11,232,600. Break-even order drop 14.2%. Weak: "Returns fall 4 points, so margin rises." Strong: "It rises by 1.29 million if the fee is income, but the real risk is lost loyal buyers, so I would test it on a sample first."

**Code:**
```python
orders=1_000_000; fee=4.0; keep_m=15.0; ret_cost=8.0
def margin(n,rate,fee_income):
    kept=n*(1-rate); ret=n*rate
    return kept*keep_m-ret*ret_cost+ret*fee_income, kept, ret
b,kb,rb=margin(orders,0.22,0)
print(f"before: kept {kb:,.0f}, returned {rb:,.0f}, margin {b:,.0f}")
assert kb==780_000 and rb==220_000 and b==9_940_000
n1=orders*0.97
a_fee,ka,ra=margin(n1,0.18,fee)
a_nofee,_,_=margin(n1,0.18,0)
print(f"after (orders {n1:,.0f}, kept {ka:,.0f}, returned {ra:,.0f}):")
print(f"  margin if fee income is kept by the retailer: {a_fee:,.0f}  change {a_fee-b:+,.0f}")
print(f"  margin if fee is ignored:                      {a_nofee:,.0f}  change {a_nofee-b:+,.0f}")
assert abs(a_fee-11_232_600)<1e-6 and abs(a_nofee-10_534_200)<1e-6
# per-order margin and break-even relative drop in orders
pm_b=0.78*15-0.22*8
pm_fee=0.82*15-0.18*8+0.18*4
pm_nofee=0.82*15-0.18*8
print(f"\nper-order margin: before {pm_b:.4f}, after with fee {pm_fee:.4f}, after without fee {pm_nofee:.4f}")
be_fee=1-pm_b/pm_fee; be_nofee=1-pm_b/pm_nofee
print(f"break-even relative drop in orders: with fee {be_fee:.4f}, without fee {be_nofee:.4f}")
assert round(pm_b,2)==9.94 and round(pm_fee,2)==11.58 and round(pm_nofee,2)==10.86
assert round(be_fee,4)==0.1416 and round(be_nofee,4)==0.0847
# check by direct computation at the break-even
n_be=orders*(1-be_fee)
assert abs(margin(n_be,0.18,fee)[0]-b)<1e-3
n_be2=orders*(1-be_nofee)
assert abs(margin(n_be2,0.18,0)[0]-b)<1e-3
print("margin at break-even order levels equals before-margin: OK")
# sensitivity: if returns only fall to 20%
for r in (0.22,0.20,0.18):
    m,_,_=margin(n1,r,fee); print(f"  returns {r:.0%} with 3% fewer orders (fee kept): margin {m:,.0f}")
nofee_same=margin(n1,0.22,0)[0]
print("returns unchanged at 22%, 3% fewer orders, no fee income:",f"{nofee_same:,.0f}")
assert nofee_same<b
print("orders at break-even (fee, no fee):",round(orders*(1-be_fee)),round(orders*(1-be_nofee)))
assert round(orders*(1-be_fee))==858_377 and round(orders*(1-be_nofee))==915_285
assert abs(margin(n1,0.20,fee)[0]-10_864_000)<1e-6 and abs(margin(n1,0.22,fee)[0]-10_495_400)<1e-6
```

**Output (my run):**
```
before: kept 780,000, returned 220,000, margin 9,940,000
after (orders 970,000, kept 795,400, returned 174,600):
  margin if fee income is kept by the retailer: 11,232,600  change +1,292,600
  margin if fee is ignored:                      10,534,200  change +594,200

per-order margin: before 9.9400, after with fee 11.5800, after without fee 10.8600
break-even relative drop in orders: with fee 0.1416, without fee 0.0847
margin at break-even order levels equals before-margin: OK
  returns 22% with 3% fewer orders (fee kept): margin 10,495,400
  returns 20% with 3% fewer orders (fee kept): margin 10,864,000
  returns 18% with 3% fewer orders (fee kept): margin 11,232,600
returns unchanged at 22%, 3% fewer orders, no fee income: 9,641,800
orders at break-even (fee, no fee): 858377 915285
```

**Follow-ups:**
- *Why does the 4 point fall matter so much?* Each avoided return turns a cost of 8 into a kept order worth 15, a swing of 23 per order.
- *What if only high-return categories are charged?* The fee hits the buyers who cost most, and order loss is probably smaller.
- *Free returns elsewhere?* Part 5 Q20 shows per-order contribution in the same way.

**Common mistakes:**
- Ignoring the 8 handling cost on returned orders.
- Applying the order drop only to kept orders.
- Mixing up the 4 point absolute fall with a relative one.
- Not saying whether the fee is income.

### Q51 ⭐ 🔴 An insurer has 100,000 policies at a premium of 1,000 with 200 of expenses each, and a new risk model finds 10,000 policies with expected claims of 1,100 while the other 90,000 average 700. Compute profit for each group and the portfolio, then reprice the risky group to 1,350 assuming 40% of them lapse, compute the new portfolio profit, and say what adverse selection implies for the 1,100 figure.
**Asked at:** No public page found, editor-designed from the standard business-case themes (unit economics, break-even, decision under uncertainty) that the guides above describe in general terms; search snippets only, not opened

**Say this first (1 line):** The risky group loses 3.0 million, the rest earns 9.0 million, so the portfolio makes 6.0 million; repricing the risky group to 1,350 lifts it to 9.3 million on paper (illustrative), but adverse selection means the people who stay will likely claim more than 1,100, and the cushion is only 50 a policy.

**Clarifying questions:**
- Are the 1,100 and 700 expected claims from a back-test or only a model estimate? Model error on a 10,000 group can be large.
- Do expenses of 200 fall when a policy lapses? Here I assume yes.
- Is repricing allowed by the regulator, and can we price by this risk factor at all? Some factors cannot be used.
- Will competitors see the same signal? If they price the 90,000 safe policies lower, we lose the profitable ones.
- Why 40% lapse? Is it measured from a price test or assumed?

**Approach:**
1. Profit per policy: risky = 1,000 - 200 - 1,100 = -300. Rest = 1,000 - 200 - 700 = +100.
2. Totals: risky 10,000 x -300 = -3,000,000. Rest 90,000 x 100 = 9,000,000. Portfolio 6,000,000. Average claims are 740, which gives the same 6.0 million.
3. Reprice risky to 1,350: 40% lapse, so 6,000 remain. Profit per remaining policy = 1,350 - 200 - 1,100 = +50. Total 300,000.
4. New portfolio = 300,000 + 9,000,000 = 9,300,000, a gain of 3.3 million.
5. Adverse selection: the 1,100 is the average of the whole risky group. The 40% who leave are probably the less risky ones, who shop around. The 6,000 who stay may average more than 1,100. Break-even for stayers is 1,350 - 200 = 1,150, only 4.5% above 1,100. At 1,250 the group loses 600,000. Portfolio stays above the 6.0 million baseline in these cases, because lapses also remove loss-making policies, but the "+300,000" is not safe.
6. Bigger risk is on the other side: the 90,000 good policies earn 9.0 million. If a rival prices them lower, we are left with the worst risks. Monitor lapse by risk band.
7. Roll out in steps, a randomised or phased increase, and track claims for stayers, not only price acceptance.

**Metrics:**
- Profit per policy = premium - expenses - expected claims. Loss ratio = claims / premium (for example 1,100 / 1,350 = 81.5% after repricing).
- Lapse rate by risk band = lapsed policies / policies in the band.
- Guardrails: claims of stayers versus the model, rate-change complaints, regulatory limits.

**Risks:**
- Adverse selection: those who accept a rise know something the model does not.
- Model error: the 1,100 may be wrong, and a risky group chosen by a model suffers "winner's curse" (the group selected for high predicted claims is partly selected for model error, so true claims may be lower, which works the other way).
- The safe group is poached.
- Fairness and regulation.

**What the interviewer scores:**
- Strong: gets both groups and the portfolio right, then reprices, then explains why stayers differ from the group average. Weak: reprices and says "profit goes up".
- Strong: gives the break-even claims (1,150). Weak: no sensitivity.
- Strong: worries about the 90,000, not only the 10,000. Weak: only the risky group.

**Example:** Illustrative numbers. Before: -3.0 million + 9.0 million = 6.0 million. After: 0.3 million + 9.0 million = 9.3 million. Stayers' claims at 1,250: -0.6 million, portfolio 8.4 million. Weak: "Repricing adds 3.3 million." Strong: "It adds up to 3.3 million, but only if stayers claim about 1,100, and the margin is just 50 a policy."

**Code:**
```python
n=100_000; prem=1000; exp_=200
risky_n=10_000; risky_claims=1100
safe_n=90_000; safe_claims=700
p_risky=prem-exp_-risky_claims
p_safe=prem-exp_-safe_claims
print("profit per policy: risky",p_risky,"safe",p_safe)
tot_risky=risky_n*p_risky; tot_safe=safe_n*p_safe
port=tot_risky+tot_safe
print("risky group total:",tot_risky,"safe group total:",tot_safe,"portfolio:",port)
assert p_risky==-300 and p_safe==100 and tot_risky==-3_000_000 and tot_safe==9_000_000 and port==6_000_000
# portfolio average claims check
avg_claims=(risky_n*risky_claims+safe_n*safe_claims)/n
print("average claims per policy:",avg_claims,"; portfolio profit via average:",n*(prem-exp_-avg_claims))
assert avg_claims==740 and n*(prem-exp_-avg_claims)==port
# reprice risky to 1350, 40% lapse
new_prem=1350; lapse=0.40
stay=risky_n*(1-lapse)
p_stay=new_prem-exp_-risky_claims
risky_after=stay*p_stay
port2=risky_after+tot_safe
print(f"\nrepriced: stay {stay:,.0f} x {p_stay} = {risky_after:,.0f}; portfolio {port2:,.0f}; change {port2-port:+,.0f}")
assert stay==6_000 and p_stay==50 and risky_after==300_000 and port2==9_300_000
# break-even claims for the stayers
be_claims=new_prem-exp_
print("stayers' break-even average claims:",be_claims,"=",round(be_claims/risky_claims-1,4),"above 1,100")
assert be_claims==1150 and round(be_claims/risky_claims-1,3)==0.045
print("\nAdverse selection: stayers' true average claims -> portfolio profit")
for c in (1100,1150,1250,1350):
    pf=stay*(new_prem-exp_-c)+tot_safe
    print(f"  stayers claim {c}: stayers profit {stay*(new_prem-exp_-c):>10,.0f}, portfolio {pf:,.0f}")
assert 6_000*(1350-200-1250)==-600_000
# even if everyone risky lapsed
print("if all 10,000 risky lapse: portfolio",tot_safe)
assert tot_safe>port
# lapse sensitivity at 1100
for l in (0.0,0.4,0.8):
    st=risky_n*(1-l); print(f"  lapse {l:.0%}: portfolio {st*p_stay+tot_safe:,.0f}")
print("loss ratio after repricing:",round(risky_claims/new_prem,4))
assert round(risky_claims/new_prem,3)==0.815
```

**Output (my run):**
```
profit per policy: risky -300 safe 100
risky group total: -3000000 safe group total: 9000000 portfolio: 6000000
average claims per policy: 740.0 ; portfolio profit via average: 6000000.0

repriced: stay 6,000 x 50 = 300,000; portfolio 9,300,000; change +3,300,000
stayers' break-even average claims: 1150 = 0.0455 above 1,100

Adverse selection: stayers' true average claims -> portfolio profit
  stayers claim 1100: stayers profit    300,000, portfolio 9,300,000
  stayers claim 1150: stayers profit          0, portfolio 9,000,000
  stayers claim 1250: stayers profit   -600,000, portfolio 8,400,000
  stayers claim 1350: stayers profit -1,200,000, portfolio 7,800,000
if all 10,000 risky lapse: portfolio 9000000
  lapse 0%: portfolio 9,500,000
  lapse 40%: portfolio 9,300,000
  lapse 80%: portfolio 9,100,000
loss ratio after repricing: 0.8148
```

**Follow-ups:**
- *Why does lapse help here?* Each lapsed policy removes a -300 policy, so a lapse is worth +300 relative to staying at the old price.
- *How would you check the model?* Compare predicted and actual claims by decile on a hold-out period, and check calibration for the risky band.
- *Alternatives to a big price rise?* Raise the premium in steps, add deductibles, or offer a safer-driving discount.

**Common mistakes:**
- Forgetting that expenses of 200 still apply to staying policies.
- Treating the average claims of the group as the claims of those who stay.
- Ignoring the 90,000 profitable policies.
- Using the repriced premium for lapsed policies.

### Q52 ⭐ 🔴 A marketplace tested take rates of 10% and 12% and saw GMV fall by 2.5 points of today's GMV for each 1 point of take rate (absolute). A line through the two tested points gives GMV equal to today's GMV times (1 - 2.5 x (take rate - 0.10)). Compute the revenue-maximising take rate and the revenue gain relative to today's revenue, then explain why extrapolating beyond the tested range is dangerous.
**Asked at:** Marketplace and take-rate material (an inpractise take-rate course page, a Codemia Thumbtack data scientist guide describing a marketplace case round, ibinterviewquestions and hackingthecaseinterview marketplace and supply-demand pages); general marketplace guides, nothing specific to Uber, DoorDash or Swiggy loops; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** On the fitted line revenue is largest at a 25% take rate, 56.25% above today (illustrative), but the line was tested only between 10% and 12%, so 25% is an extrapolation I would not trust.

**Clarifying questions:**
- Were 10% and 12% tested at random on sellers, or compared across time or regions? If not random, the slope is confounded.
- How long did the test run? Sellers move volume off-platform slowly, so a short test understates the long-run fall.
- Was GMV measured per seller or marketplace-wide? Buyers may react too.
- Are there only two points? Two points give a line with no error bar.
- Does take rate matter at the seller-category level? A single rate for all categories is a strong simplification.

**Approach:**
1. Write the model with today's GMV as 1. GMV(t) = 1 - 2.5 x (t - 0.10). Check: at 12%, GMV = 0.95, a fall of 5%.
2. Revenue R(t) = t x GMV(t) = 1.25t - 2.5t squared.
3. Set the derivative to zero: 1.25 - 5t = 0, so t = 0.25.
4. R(0.25) = 0.25 x 0.625 = 0.15625. Today R = 0.10. Gain = 56.25%. At 12% the gain is 14%.
5. Look at what the optimum implies: GMV falls by 37.5%, over 7 times the 5% fall actually observed.
6. Show that the answer depends on the curve shape. A constant-elasticity curve through the same two points (elasticity 0.28) gives revenue that keeps rising at 25% and 40%. The linear one falls back to today's level at 40%. Two curves through the same data, two different stories.
7. Show noise: with 2% noise on GMV in each arm, the "optimal" rate swings from 0.16 to 0.91 (5th to 95th percentile).
8. Recommend: move in steps (for example to 12%, then 14%), measuring GMV, seller exits and off-platform leakage at each step, and stop when the revenue gain per step shrinks.

**Metrics:**
- Revenue = take rate x GMV. Take rate = platform revenue / GMV.
- GMV retention vs control = GMV treated / GMV control.
- Guardrails: active sellers, seller churn, buyer repeat rate, off-platform leakage (proxy: share of repeat buyer-seller pairs that disappear).

**Risks:**
- Extrapolation beyond 12%: sellers have a threshold (when the fee exceeds their margin they leave in bulk).
- Long-run response is bigger than the short-run one.
- Competitors react.
- Two points, no uncertainty: the slope could be flatter or steeper.
- Revenue maximum is not the business goal: liquidity and growth matter too.

**What the interviewer scores:**
- Strong: correct optimum and gain, then immediately questions the extrapolation with a reason and a plan. Weak: reports 25% as the answer.
- Strong: shows another curve shape or noise to prove the point. Weak: says "it may be non-linear" with nothing more.
- Strong: proposes a staged rollout with stop rules. Weak: runs one big increase.

**Example:** Illustrative numbers. At 12%: 0.12 x 0.95 = 0.114, up 14%. At 25%: 0.25 x 0.625 = 0.156, up 56%. But the test never saw GMV below 0.95. Weak: "Set 25% and earn 56% more." Strong: "The model says 25%; I trust it up to about 12 to 14% and would step up from there."

**Code:**
```python
import numpy as np
# GMV(t) = G0*(1 - 2.5*(t-0.10)),  revenue R(t) = t*GMV(t),  G0 = 1 (index)
g=lambda t:1-2.5*(t-0.10)
R=lambda t:t*g(t)
# check the fit reproduces the tested points
assert abs(g(0.12)-0.95)<1e-12 and abs(g(0.10)-1)<1e-12
topt=1.25/5      # R = 1.25t - 2.5t^2 ; dR/dt = 1.25 - 5t = 0
print("revenue-maximising take rate:",topt)
assert abs(topt-0.25)<1e-12
print("revenue index at 10%, 12%, 25%:",round(R(0.10),5),round(R(0.12),5),round(R(topt),5))
gain=R(topt)/R(0.10)-1
print(f"gain vs today: {gain:.4f}; at 12%: {R(0.12)/R(0.10)-1:.4f}")
assert round(gain,4)==0.5625 and round(R(0.12)/R(0.10)-1,3)==0.14
# numeric check of the optimum
ts=np.linspace(0.05,0.45,40001); assert abs(ts[np.argmax(R(ts))]-0.25)<1e-4
print(f"GMV at the optimum: {g(topt):.3f} of today (a {1-g(topt):.1%} fall, 7.5x the 5% fall actually seen at 12%)")
assert round(1-g(topt),3)==0.375
# another curve through the same two points: constant elasticity GMV = (t/0.10)^(-e)
e=-np.log(0.95)/np.log(1.2)
print(f"constant-elasticity curve through (10%,1) and (12%,0.95): e={e:.4f}")
Rc=lambda t:t*(t/0.10)**(-e)
for t in (0.10,0.12,0.25,0.40):
    print(f"  take {t:.0%}: linear revenue {R(t):.4f}  vs constant-elasticity {Rc(t):.4f}  GMV linear {g(t):.3f} vs {(t/0.10)**(-e):.3f}")
assert Rc(0.40)>Rc(0.25)>Rc(0.12)   # no interior optimum here: revenue keeps rising
assert R(0.40)<R(0.25)
# the line through two points: how sensitive is the slope to noise in the 12% test?
rng=np.random.default_rng(3)
sd=0.02   # illustrative: 2% noise on measured GMV index in each arm
slopes=[]
for _ in range(20000):
    g0=1+rng.normal(0,sd); g1=0.95+rng.normal(0,sd)
    slopes.append((g1/g0-1)/0.02)       # fall per unit of take rate (here -2.5 at truth)
slopes=np.array(slopes)
# optimum for slope s (GMV=1+s*(t-0.10)): R=t+s t^2-0.1 s t -> t*=(0.1*s-1)/(2*s)
s=slopes; tstar=(0.1*s-1)/(2*s)
tstar=tstar[s<0]
lo,hi=np.percentile(tstar,[5,95])
print(f"with 2% noise in each arm, the 'optimal' take rate ranges {lo:.2f} to {hi:.2f} (5th to 95th percentile)")
assert hi-lo>0.1
```

**Output (my run):**
```
revenue-maximising take rate: 0.25
revenue index at 10%, 12%, 25%: 0.1 0.114 0.15625
gain vs today: 0.5625; at 12%: 0.1400
GMV at the optimum: 0.625 of today (a 37.5% fall, 7.5x the 5% fall actually seen at 12%)
constant-elasticity curve through (10%,1) and (12%,0.95): e=0.2813
  take 10%: linear revenue 0.1000  vs constant-elasticity 0.1000  GMV linear 1.000 vs 1.000
  take 12%: linear revenue 0.1140  vs constant-elasticity 0.1140  GMV linear 0.950 vs 0.950
  take 25%: linear revenue 0.1562  vs constant-elasticity 0.1932  GMV linear 0.625 vs 0.773
  take 40%: linear revenue 0.1000  vs constant-elasticity 0.2708  GMV linear 0.250 vs 0.677
with 2% noise in each arm, the 'optimal' take rate ranges 0.16 to 0.91 (5th to 95th percentile)
```

**Follow-ups:**
- *What if the effect is different by seller size?* Fit separate slopes. Large sellers can leave more easily (see Part 5 Q28).
- *How do you estimate off-platform leakage?* Look at repeat buyer-seller pairs that vanish from the platform after the rise.
- *Is revenue maximisation the right goal?* Usually not alone. Add a floor on GMV or active sellers.

**Common mistakes:**
- Taking the vertex of the parabola as a recommendation.
- Forgetting that revenue is take rate x GMV, not GMV alone.
- Treating two test arms as a fitted model with a confidence interval.
- Measuring only the short run.

### Q53 ⭐ 🔴 A shop stocks 100 units a day and sells out on 40% of days, selling 70 units on average on the other 60%, so average sales are 82 units a day. The planner uses 82 as mean demand with a critical ratio of 0.8. Explain why average sales is a biased estimate of mean demand and why even the 70 is biased, and say how you would estimate the demand distribution before choosing the stock level.
**Asked at:** Forecasting and inventory material (PracHub retail demand-forecasting and inventory-and-stockout concept pages, a Dataford supermarket demand-forecasting page attributed in its title to a BCG data scientist interview but unverified, a PyCon DE 2025 talk on stockouts in retail forecasting); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** Sales are demand capped at the 100 units on the shelf, so 82 understates demand, and even the 70 on non-stockout days is too low because it only averages the days when demand happened to be below 100 (illustrative).

**Clarifying questions:**
- Is the stock always exactly 100, or does it vary? Varying stock gives free information about the demand curve.
- Do the sell-out days come at random, or on busy days (weekends, promotions)? If they cluster, demand is also different on those days.
- Can we see when during the day it sold out? Time of sell-out tells us how much demand was lost.
- Is there any record of lost sales, such as store-pickup requests or search views? That is direct evidence of demand above 100.
- Do customers switch to substitutes when it sells out? Then lost demand is partly recaptured.

**Approach:**
1. Check the arithmetic: 0.4 x 100 + 0.6 x 70 = 82. Correct, but this is mean sales, not mean demand.
2. Why 82 is too low: on 40% of days demand was at least 100, and we recorded exactly 100. Every one of those days is truncated from above.
3. Why 70 is also biased: on the other 60% of days we only keep days when demand was below 100. The average of demand conditional on being below 100 is below the average of demand. Dropping the sell-out days is not neutral.
4. Fix: treat sales as censored data. Fit a demand distribution using two facts: P(demand at or above 100) = 40% and mean of the rest = 70. With a normal, this gives mean 91.5 and sd 33.4 (illustrative). With a lognormal the mean is 98.5 and the 80th percentile 129.5. The model choice matters, so say so.
5. The 80th percentile from the normal fit is 119.7. A planner using sales mean and sd gets about 100 and keeps stocking 100, which is self-reinforcing.
6. Better data: vary stock on purpose, record time of sell-out, count lost-sale signals (searches, store enquiries), and use a Tobit-style or survival-style censored model by day type.
7. Then choose stock at the critical-ratio quantile of the fitted distribution, and keep testing it.

**Metrics:**
- Sell-out share = days with stock-out / all days (40%).
- Censored-mean demand estimate = fitted mean of the demand distribution that matches both the sell-out share and observed sales.
- Guardrails: waste (unsold units), lost margin on sell-out days, fit check on a day type where stock was higher.

**Risks:**
- The shape of demand (normal, lognormal, or other) decides the answer: 91.5 vs 98.5 mean here.
- Day-of-week and promotion effects can mimic or hide censoring.
- Substitution reduces apparent lost demand.
- Raising stock may raise waste if the fit is too high.

**What the interviewer scores:**
- Strong: explains both biases (capped sales, and a conditional mean for non-stockout days), fits a censored model, and tests the shape sensitivity. Weak: says "sales are not demand" and adds 10%.
- Strong: proposes a way to learn (stock experiment, lost-sales signals). Weak: no new data.
- Strong: connects to the critical ratio and says why the stock level stays stuck at 100. Weak: just quotes the formula.

**Example:** Illustrative numbers. 0.4 x 100 + 0.6 x 70 = 82. Fitted normal demand: mean 91.5, 80th percentile 119.7. A planner using 82 and the sales sd of 21.8 stocks about 100, so it never escapes. Weak: "Mean demand is 82; stock at the 80th percentile." Strong: "82 is censored. I would fit demand using the sell-out share, then test a higher stock level for a few weeks."

**Code:**
```python
import numpy as np
from scipy import stats, optimize
stock=100; p_out=0.40; mean_in=70
avg_sales=p_out*stock+(1-p_out)*mean_in
print("average sales:",avg_sales)
assert abs(avg_sales-82)<1e-9

# Model 1: demand ~ Normal(mu, sigma). Unknowns solved from: P(D>=100)=0.4 and E[D | D<100]=70
a=stats.norm.ppf(1-p_out)       # (100-mu)/sigma
lam=stats.norm.pdf(a)/stats.norm.cdf(a)
# mu - sigma*lam = 70 and mu = 100 - a*sigma
sigma=(stock-mean_in)/(a+lam); mu=stock-a*sigma
print(f"Normal fit: mu={mu:.1f}, sigma={sigma:.1f}")
assert abs(mu-91.5)<0.1 and abs(sigma-33.4)<0.1
chk_out=1-stats.norm.cdf(stock,mu,sigma)
chk_in=stats.truncnorm.mean(-np.inf,(stock-mu)/sigma,loc=mu,scale=sigma)
chk_sales=p_out*stock+(1-p_out)*chk_in
print(f"  check: P(sell out) {chk_out:.3f}, mean of non-stockout days {chk_in:.1f}, mean sales {chk_sales:.1f}")
assert abs(chk_out-0.4)<1e-9 and abs(chk_in-70)<1e-6 and abs(chk_sales-82)<1e-6
q80=stats.norm.ppf(0.8,mu,sigma)
print(f"  mean demand {mu:.1f} (vs 82 from sales); 80th percentile {q80:.1f}")
assert mu>82 and q80>stock

# Model 2: lognormal demand, same two facts
def eqs(x):
    m,s=x
    d=stats.lognorm(s,scale=np.exp(m))
    p=d.sf(stock)-p_out
    # E[D | D<100] = integral of x f(x) dx / cdf
    k=(np.log(stock)-m-s*s)/s
    tm=np.exp(m+s*s/2)*stats.norm.cdf(k)/d.cdf(stock)
    return [p,tm-mean_in]
sol=optimize.fsolve(eqs,[4.4,0.4])
m,s=sol; d=stats.lognorm(s,scale=np.exp(m))
print(f"Lognormal fit: mean demand {d.mean():.1f}, 80th percentile {d.ppf(0.8):.1f}")
assert max(abs(np.array(eqs(sol))))<1e-6 and d.mean()>82

# Simulation: what a planner who uses sales as demand does
rng=np.random.default_rng(5)
D=rng.normal(mu,sigma,400_000); D=D[D>=0]
S=np.minimum(D,stock)
print(f"\nSimulated: sell-out share {(D>=stock).mean():.3f}, mean sales {S.mean():.1f}, mean of non-stockout days {D[D<stock].mean():.1f}, true mean demand {D.mean():.1f}")
assert abs(S.mean()-82)<0.6 and abs(D[D<stock].mean()-70)<0.6
# stock level for critical ratio 0.8: planner (mean 82, same sigma) vs censored fit
plan=S.mean()+stats.norm.ppf(0.8)*S.std()
print(f"stock for CR 0.8: planner using sales mean and sd {plan:.0f} (about today's 100) vs fitted 80th percentile {q80:.0f}")
assert abs(plan-100)<2 and plan<q80
# and the 'sales-only' sample sigma is also too small
print("sd of sales (capped at 100):",round(S.std(),1),"vs true demand sd",round(D.std(),1))
assert S.std()<D.std()
```

**Output (my run):**
```
average sales: 82.0
Normal fit: mu=91.5, sigma=33.4
  check: P(sell out) 0.400, mean of non-stockout days 70.0, mean sales 82.0
  mean demand 91.5 (vs 82 from sales); 80th percentile 119.7
Lognormal fit: mean demand 98.5, 80th percentile 129.5

Simulated: sell-out share 0.402, mean sales 82.3, mean of non-stockout days 70.4, true mean demand 91.9
stock for CR 0.8: planner using sales mean and sd 101 (about today's 100) vs fitted 80th percentile 120
sd of sales (capped at 100): 21.8 vs true demand sd 33.0
```

**Follow-ups:**
- *Why is 70 biased?* It is the mean of D given D below 100, which is lower than the mean of D.
- *What if stock varies day to day?* Then each day has its own cap, and the censored likelihood uses it directly.
- *Related?* Part 5 Q22 treats the simpler case where demand on out-of-stock days is assumed equal to in-stock days, and Part 5 Q7 uses the critical ratio.

**Common mistakes:**
- Using average sales as demand.
- Dropping sell-out days from the data (a common fix that is also biased).
- Using sales variance as demand variance.
- Assuming a normal without testing a second shape.

### Q54 ⭐ 🔴 A support bot answers 1,000,000 queries a month. A large model costs 0.020 a query and is right 92% of the time, while a small model costs 0.002 and is right 80% of the time. A cascade tries the small model first and escalates 35% of queries to the large one, with the small model right 90% of the time on the 65% it keeps and the large model right 88% on the 35% it receives. A wrong answer costs 0.30. Compute total cost per query for large-only, small-only and the cascade, and say what you would validate.
**Asked at:** AI-era support and GenAI cost material (2026 vendor and practitioner pages from Lorikeet, Twig, Voiceflow, aitimejournal, CloudZero, nOps, tianpan.co and a Gartner press-release headline on inference costs); mostly vendor-sourced, an emerging interview theme rather than a confirmed bank; commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** Per query the large model costs 0.0440, the small one 0.0620 and the cascade 0.0411, so the cascade saves 2,900 a month on a million queries (6.6%), but it is less accurate than the large model (89.3% vs 92%) and loses its edge once a wrong answer costs more than about 0.41 (illustrative).

**Clarifying questions:**
- How is the 0.30 cost of a wrong answer measured (refund, repeat contact, churn)? The cascade's edge depends on it.
- Does the cascade also pay for the router or confidence check? Here I assume no extra cost.
- Is the small model run on every query first, so its cost is always paid? Yes, I assume 0.002 on all queries.
- How were the 90% and 88% accuracies measured? On a labelled sample from live traffic or on a benchmark?
- Are some query types high-risk (money, safety)? Those should skip the small model.

**Approach:**
1. Cost per query = inference cost + (1 - accuracy) x 0.30.
2. Large-only: 0.020 + 0.08 x 0.30 = 0.020 + 0.024 = 0.0440.
3. Small-only: 0.002 + 0.20 x 0.30 = 0.002 + 0.060 = 0.0620.
4. Cascade inference: small model on all (0.002) plus large model on 35% (0.35 x 0.020 = 0.007) = 0.0090.
5. Cascade accuracy: 0.65 x 0.90 + 0.35 x 0.88 = 0.585 + 0.308 = 0.893. Error cost = 0.107 x 0.30 = 0.0321. Total = 0.0411.
6. Monthly on 1,000,000 queries: 44,000, 62,000, 41,100. The cascade saves 2,900 against large-only, 6.6%.
7. Break-even wrong-answer cost: 0.009 + 0.107w = 0.020 + 0.08w gives w = 0.4074. Above that, large-only is cheaper.
8. Validate: accuracy on each slice from labelled live samples, the accuracy of the router (does it send the right queries up?), and tail harm.
9. Consistency check: the stated numbers imply the small model is only 61.4% right on the queries it escalates, and the large model 94.2% right on the 65% it never sees. Plausible, since escalated queries are harder, but check it.

**Metrics:**
- Cost per query = (model costs + wrong answers x 0.30) / queries.
- Accuracy = correct answers / queries (human-judged sample). Escalation rate = escalated / all (35%).
- Guardrails: accuracy on high-risk topics, latency (two model calls on 35% of queries), wrong-and-confident rate for kept answers.

**Risks:**
- Wrong-answer cost is the swing factor, and it is not constant: some mistakes cost far more than 0.30.
- Accuracy on the 65% kept may drift when the query mix changes.
- Cascade adds latency and complexity.
- Accuracy labels from a small sample have wide error bars: 1 point on 1,000,000 queries is 3,000 a month.

**What the interviewer scores:**
- Strong: counts the small model's cost on every query, includes error cost, notices that the cascade is less accurate than large-only. Weak: compares inference prices only.
- Strong: finds the break-even wrong-answer cost. Weak: gives three numbers and no decision rule.
- Strong: validates router quality and tail risk. Weak: trusts the 90% and 88%.

**Example:** Illustrative numbers. Large 0.0440, small 0.0620, cascade 0.0411. At wrong-answer cost 0.50 the cascade is 0.0625 and large 0.0600, so large wins. Weak: "Cascade is cheapest so ship it." Strong: "Cascade saves 6.6% only because wrong answers are cheap. If a wrong answer costs above 0.41 or accuracy matters more, I keep large-only for those queries."

**Code:**
```python
N=1_000_000; wrong=0.30
big_c,big_acc=0.020,0.92
small_c,small_acc=0.002,0.80
esc=0.35; keep=1-esc
small_keep_acc=0.90; big_esc_acc=0.88
def total(c,acc): return c+(1-acc)*wrong
large=total(big_c,big_acc); small=total(small_c,small_acc)
inf_c=small_c+esc*big_c           # small model runs on every query; large model only on escalated
casc_acc=keep*small_keep_acc+esc*big_esc_acc
casc=total(inf_c,casc_acc)
print(f"large-only: infer {big_c:.4f} + error {(1-big_acc)*wrong:.4f} = {large:.4f} per query")
print(f"small-only: infer {small_c:.4f} + error {(1-small_acc)*wrong:.4f} = {small:.4f} per query")
print(f"cascade:    infer {inf_c:.4f} + error {(1-casc_acc)*wrong:.4f} = {casc:.4f} per query; accuracy {casc_acc:.4f}")
assert round(large,4)==0.0440 and round(small,4)==0.0620 and round(inf_c,4)==0.0090
assert round(casc_acc,3)==0.893 and round(casc,4)==0.0411
print("per month:",round(large*N),round(small*N),round(casc*N),"; cascade saves vs large:",round((large-casc)*N),f"({(large-casc)/large:.1%})")
assert round((large-casc)*N)==2900
# break-even cost of a wrong answer
w=(inf_c-big_c)/((1-big_acc)-(1-casc_acc))  # inf_c+(1-casc_acc)w = big_c+(1-big_acc)w
print(f"wrong-answer cost at which cascade = large-only: {w:.4f}")
assert round(w,4)==0.4074
for ww in (0.2,0.3,w,0.5,1.0):
    l=big_c+(1-big_acc)*ww; c=inf_c+(1-casc_acc)*ww
    print(f"  wrong costs {ww:.4f}: large {l:.4f}, cascade {c:.4f}, cheaper: {'cascade' if c<l-1e-9 else 'large' if l<c-1e-9 else 'tie'}")
assert (inf_c+(1-casc_acc)*0.5)>(big_c+(1-big_acc)*0.5)
# implied accuracy of each model on the other slice (consistency with the overall rates)
small_on_esc=(small_acc-keep*small_keep_acc)/esc
big_on_keep=(big_acc-esc*big_esc_acc)/keep
print(f"\nimplied small-model accuracy on escalated queries: {small_on_esc:.3f}; large on kept queries: {big_on_keep:.3f}")
assert 0<small_on_esc<big_esc_acc and big_on_keep<1
print("value of 1 accuracy point per month:",round(0.01*wrong*N))
assert round(0.01*wrong*N)==3_000
print("slice accuracy sum check:",round(keep*small_keep_acc,3),round(esc*big_esc_acc,3))
assert round(small_on_esc,3)==0.614 and round(big_on_keep,3)==0.942
```

**Output (my run):**
```
large-only: infer 0.0200 + error 0.0240 = 0.0440 per query
small-only: infer 0.0020 + error 0.0600 = 0.0620 per query
cascade:    infer 0.0090 + error 0.0321 = 0.0411 per query; accuracy 0.8930
per month: 44000 62000 41100 ; cascade saves vs large: 2900 (6.6%)
wrong-answer cost at which cascade = large-only: 0.4074
  wrong costs 0.2000: large 0.0360, cascade 0.0304, cheaper: cascade
  wrong costs 0.3000: large 0.0440, cascade 0.0411, cheaper: cascade
  wrong costs 0.4074: large 0.0526, cascade 0.0526, cheaper: tie
  wrong costs 0.5000: large 0.0600, cascade 0.0625, cheaper: large
  wrong costs 1.0000: large 0.1000, cascade 0.1160, cheaper: large

implied small-model accuracy on escalated queries: 0.614; large on kept queries: 0.942
value of 1 accuracy point per month: 3000
slice accuracy sum check: 0.585 0.308
```

**Follow-ups:**
- *How would you lower the cost further?* Send high-risk topics straight to the large model and let the small model keep only easy, low-risk ones, then re-measure.
- *Why include the error cost?* Because the cheapest model is not the cheapest system; the error cost here is bigger than inference cost for every option.
- *What does a 1-point accuracy change cost?* 0.01 x 0.30 x 1,000,000 = 3,000 a month, about the same as the whole cascade saving.

**Common mistakes:**
- Forgetting the small model's cost on escalated queries.
- Comparing only inference cost.
- Using the benchmark accuracy (80%, 92%) for the slices.
- Ignoring that the cascade's accuracy is below the large model's.

### Q55 ⭐ 🔴 Two ad channels have revenue curves of 6 x sqrt(s) and 3 x sqrt(s) million, where s is spend in millions, and the 10 million budget is split 5 and 5 today. Compute revenue at the 5 and 5 split and at the equal-marginal-return split of 8 and 2, and say what such fitted curves cannot tell you when they come from observational data.
**Asked at:** Marketing measurement material (a datainterview.com paid-social incrementality case, an aitrainer.work marketing data scientist question page, Triple Whale and Eppo GeoLift pages, a Medium post on geo-experiments, a PyData Boston 2025 talk description); commonly reported in public guides for data scientist, product analyst and ML engineer loops; search snippets only, not opened

**Say this first (1 line):** Revenue is 20.13 million at 5 and 5 and 21.21 million at 8 and 2, a gain of 1.09 million or 5.4% (illustrative), but that gain exists only if the fitted curves are causal and valid outside the spend range we have seen, and observational data cannot promise either.

**Clarifying questions:**
- Is the 6 and 3 estimated from history of spend and revenue, or from experiments? Observational fits can be confounded.
- Over what spend range did each channel actually vary? Channel B at 2 million may be far outside the data.
- Is revenue incremental, or total revenue attributed to the channel? A curve through zero spend assumes no organic revenue.
- Is the objective revenue or margin, and is there a minimum spend (contracts, brand presence)?
- Are the channels independent? Search spend often depends on what display and social already created.

**Approach:**
1. Revenue at 5 and 5: 6 x sqrt(5) + 3 x sqrt(5) = 9 x 2.236 = 20.125.
2. Marginal return of 6 x sqrt(s) is 3 / sqrt(s); of 3 x sqrt(s) it is 1.5 / sqrt(s). At 5 and 5 they are 1.342 and 0.671. Channel A returns twice as much per extra unit, so shift money to A.
3. Equal marginal return: 3 / sqrt(s1) = 1.5 / sqrt(s2). So sqrt(s1) = 2 x sqrt(s2), s1 = 4 x s2. With s1 + s2 = 10 this gives 8 and 2. Both marginal returns are 1.061.
4. Revenue at 8 and 2: 6 x 2.828 + 3 x 1.414 = 16.971 + 4.243 = 21.213. Gain 1.089 million, 5.4%.
5. Why it may not be real, and how to say so:
   - Confounding: spend rises when demand is high (holidays, launches), so the curve credits ads for demand that was coming anyway.
   - Extrapolation: the 8/2 move takes A up 60% and B down 60%. If B was never run near 2 million, the curve there is a guess.
   - Shared audience and attribution overlap: the two curves are not independent.
   - Noise: if each fitted coefficient has 20% error, in my simulation about 19% of re-fitted "optimal" splits earn less than 5 and 5 on the true curves. If both channels truly had equal returns, moving to 8/2 would lose about 1.03 million.
6. Plan: move a part of the way (for example 6.5 and 3.5), measure with a geo holdout or a switchback by region (see Part 5 Q11 and Part 4 Q29), refit the curves with the experimental points, and iterate.

**Metrics:**
- Incremental revenue per channel = revenue with spend minus revenue without, from a holdout. Marginal ROAS = change in incremental revenue / change in spend.
- Equal marginal return condition: marginal return of channel A = marginal return of channel B at the chosen split.
- Guardrails: total revenue, margin after spend, brand and baseline traffic, overlap between channels.

**Risks:**
- Fitted curves fit history, not causality.
- Optimum depends on the ratio of coefficients, which is noisy.
- Square-root shape is an assumption; the real curve may saturate faster or have a threshold.
- Short-term revenue ignores brand and lagged effects.

**What the interviewer scores:**
- Strong: correct revenues, derivation of the equal-marginal-return rule, and a clear statement that confounding and extrapolation limit the claim. Weak: computes 8/2 and stops.
- Strong: proposes experiments to estimate marginal returns, with a staged shift. Weak: "gather more data" with no design.
- Strong: gives a quantified sense of noise risk. Weak: just says "uncertain".

**Example:** Illustrative numbers. 5/5 earns 20.125. 8/2 earns 21.213. If both channels truly earn the same, 8/2 earns 19.092 against 20.125 and loses 1.03 million. Weak: "Move to 8 and 2, it adds 5%." Strong: "The maths says 8/2, but I would move to 6.5/3.5 first and run a geo test on each channel."

**Code:**
```python
import numpy as np
from scipy import optimize
a1,a2=6.0,3.0
rev=lambda s1,s2: a1*np.sqrt(s1)+a2*np.sqrt(s2)
B=10
r55=rev(5,5); r82=rev(8,2)
print(f"revenue at 5/5: {r55:.3f}  at 8/2: {r82:.3f}  gain {r82-r55:.3f} ({r82/r55-1:.2%})")
assert round(r55,2)==20.12 and round(r82,2)==21.21 and round(r82-r55,2)==1.09
# marginal returns
m=lambda a,s: a/(2*np.sqrt(s))
print(f"marginal return at 5/5: A {m(a1,5):.3f}, B {m(a2,5):.3f}")
print(f"marginal return at 8/2: A {m(a1,8):.3f}, B {m(a2,2):.3f}")
assert abs(m(a1,8)-m(a2,2))<1e-12 and m(a1,5)>m(a2,5)
# derive the split: s1/s2=(a1/a2)^2
ratio=(a1/a2)**2; s1=B*ratio/(1+ratio)
print("optimal split from s1/s2=(a1/a2)^2:",s1,B-s1)
assert abs(s1-8)<1e-12
res=optimize.minimize_scalar(lambda x:-rev(x,B-x),bounds=(0,B),method='bounded',options={'xatol':1e-10})
print("numeric optimum for channel A:",round(res.x,4))
assert abs(res.x-8)<1e-3
# average ROAS at each point
print(f"average return per unit spend at 8/2: A {rev(8,0)/8:.3f}, B {a2*np.sqrt(2)/2:.3f}  (equal because both curves are k x sqrt(s) with s1/s2 = 4)")
assert abs(6*np.sqrt(8)/8-3*np.sqrt(2)/2)<1e-12

# If the true curves are equal (observational data gave channel A a better-looking fit because it is bought on high-demand days)
true_a=(4.5,4.5)
loss=(true_a[0]*(np.sqrt(5)+np.sqrt(5))) - (true_a[0]*np.sqrt(8)+true_a[1]*np.sqrt(2))
print(f"\nIf both channels truly have coefficient 4.5: revenue at 5/5 {4.5*2*np.sqrt(5):.3f}, at 8/2 {4.5*(np.sqrt(8)+np.sqrt(2)):.3f}; moving loses {loss:.3f}")
assert loss>0.9

# noise in the fitted coefficients: how often does the 8/2 move lose money?
rng=np.random.default_rng(2)
trials=20000
# illustrative: truth is a1=5, a2=3.5 (ratio 1.43); fitted ratio is noisy, say 20% relative error on each coefficient
t1,t2=5.0,3.5
f1=t1*(1+rng.normal(0,0.2,trials)); f2=t2*(1+rng.normal(0,0.2,trials))
f1=np.clip(f1,0.1,None); f2=np.clip(f2,0.1,None)
r=(f1/f2)**2; s1h=B*r/(1+r); s2h=B-s1h
true_rev=t1*np.sqrt(s1h)+t2*np.sqrt(s2h)
true_55=t1*np.sqrt(5)+t2*np.sqrt(5)
worse=(true_rev<true_55).mean()
print(f"With 20% noise on each fitted coefficient, {worse:.1%} of re-fitted 'optimal' splits earn less than 5/5 on the true curves")
print(f"Typical (median) true gain vs 5/5: {np.median(true_rev-true_55):.3f}")
assert 0<worse<1
# extrapolation: channel B was never run near 2 or channel A near 8
print("\nspend ranges implied: A rises 60% (5 to 8), B falls 60% (5 to 2); the data may not cover those ranges")
assert abs(8/5-1-0.6)<1e-12 and abs(1-2/5-0.6)<1e-12
```

**Output (my run):**
```
revenue at 5/5: 20.125  at 8/2: 21.213  gain 1.089 (5.41%)
marginal return at 5/5: A 1.342, B 0.671
marginal return at 8/2: A 1.061, B 1.061
optimal split from s1/s2=(a1/a2)^2: 8.0 2.0
numeric optimum for channel A: 8.0
average return per unit spend at 8/2: A 2.121, B 2.121  (equal because both curves are k x sqrt(s) with s1/s2 = 4)

If both channels truly have coefficient 4.5: revenue at 5/5 20.125, at 8/2 19.092; moving loses 1.033
With 20% noise on each fitted coefficient, 19.2% of re-fitted 'optimal' splits earn less than 5/5 on the true curves
Typical (median) true gain vs 5/5: 0.215

spend ranges implied: A rises 60% (5 to 8), B falls 60% (5 to 2); the data may not cover those ranges
```

**Follow-ups:**
- *Why equal marginal returns?* If one channel's extra unit earns more, moving money there raises revenue until the two are equal.
- *What if there is a minimum spend on B?* Then the optimum is constrained; compute it with that bound.
- *Why not equal average ROAS?* Marginal, not average, tells where the next unit should go. Here both happen to match at 8/2 only because both curves are the same shape.

**Common mistakes:**
- Equalising average ROAS across channels.
- Taking an optimum from observational curves as fact.
- Ignoring that the new spend lies outside the observed range.
- Forgetting the revenue-to-margin step.

