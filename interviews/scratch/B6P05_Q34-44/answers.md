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
