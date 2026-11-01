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
