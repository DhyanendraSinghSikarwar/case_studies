### Q12 ⭐⭐⭐ 🟡 Revenue is down 8% versus last month. Build a decomposition tree from revenue down to the leaf drivers you would query (for example users, conversion, orders per buyer, price and mix), say which branches you would test first and why, and how you would stop when you have found the cause.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** I split revenue into users, conversion, orders per buyer and order value, check data and calendar first, test the widest branches, and stop when one branch explains most of the gap and a second cut inside it points to one concrete thing I can verify.

**Clarifying questions:**
- Is the 8% from the finance ledger or from an event dashboard? It decides whether I trust the number before explaining it.
- Is it revenue, GMV or net revenue after refunds and discounts? A discount or refund change moves net revenue without moving demand.
- How many days in each month and which festivals or sales fell in each? A 30-day month against a 31-day month is already about 3.2% of the 8%.
- Did anything ship, change price or change tracking? It points to which branch to open first.
- Is the drop across all regions and platforms or concentrated? It tells me whether to expect one cause or several.

**Approach:**
1. Validate the number: same definition, same calendar days, complete data. Revenue per day, not per month.
2. Build the tree (multiplicative, so each level is a ratio I can query):
   - Revenue = active users x conversion x orders per buyer x average order value (AOV).
   - Users = new + returning (+ resurrected). Conversion = buyers / users. AOV = items per order x price per item, and price per item = list price x mix x discount.
3. Compute the % change of every node. Rank them by contribution using a log split, which adds up exactly and does not depend on the order of the factors.
4. Open the biggest branch first. If two are close, open the cheaper query first (one table, one group-by).
5. Drill with one cut at a time: platform, version, region, acquisition channel, new versus returning, category.
6. Stop rule: stop when (a) one branch explains at least about 80% of the gap, (b) one cut inside it isolates the movement (for example one platform), and (c) I can name a testable cause (a release, an outage, a price change, a campaign end) with a date match. Then I confirm with a second source or a check that the timing fits.

**Metrics:**
- Revenue change % = revenue this month / revenue last month - 1. Compare per day.
- Contribution of factor k = (R1 - R0) x ln(x1/x0) / ln(R1/R0). The contributions sum to the rupee change.
- Conversion = orders-placing users / active users (same denominator both months).
- AOV = revenue / orders. Orders per buyer = orders / distinct buyers.
- Guardrail: refund rate and cancellation rate, so I do not "fix" revenue with orders that later reverse.

**Risks:**
- Different month lengths, sale timing, or a payday shift look like a decline.
- Mix shift: AOV can rise because cheap orders vanished, which hides a conversion problem.
- A change in definition of "active user" or tracking moves a branch without moving money.
- Chasing every leaf. Without a stop rule I run 40 queries and have no story.

**What the interviewer scores:**
- Strong: a multiplicative tree with exact definitions, a calendar and data check before any theory, and a clear stop rule. Weak: a list of "possible reasons" with no structure.
- Strong: prioritises by contribution size and query cost. Weak: starts with the branch they like.
- Strong: says what would make them wrong (offsetting branches, mix). Weak: stops at the first plausible cause.
- Strong: ends with an action and an owner. Weak: ends with "I would investigate more".

**Example:** (illustrative numbers) Last month: 1,000,000 users x 5.0% conversion x 1.6 orders per buyer x Rs 500 AOV = Rs 40.0 million. This month: 980,000 users x 4.6% x 1.6 x Rs 510 = Rs 36.79 million, so -8.04%. Log split: conversion -Rs 3.20 million (about 100% of the fall), users -Rs 0.78 million (24%), AOV +Rs 0.76 million (offset of -24%), orders per buyer 0. Also 30 days versus 31 days: revenue per day is -5.0%, so 3.2 points of the 8 are the calendar. Drill into conversion: android falls 5.0% to 4.5% on 80% of traffic, which accounts for the whole 0.4 point blended fall (5.0% to 4.6%), ios and web are flat. Next question: what changed on android? Weak answer: "Maybe seasonality or a competitor." Strong answer: "Calendar is 3 of the 8 points, conversion on android is the rest, AOV rise hides it, I check the android release and checkout errors next."

**Code:**
```python
import math
# Illustrative numbers. Revenue = users x conversion x orders/buyer x AOV
last = dict(users=1_000_000, conv=0.050, opb=1.60, aov=500.0)
this = dict(users=  980_000, conv=0.046, opb=1.60, aov=510.0)
def rev(d): return d["users"] * d["conv"] * d["opb"] * d["aov"]
r0, r1 = rev(last), rev(this)
chg = r1 / r0 - 1
print(f"revenue last {r0:,.0f}  this {r1:,.0f}  change {chg:+.2%}")
assert round(chg, 3) == -0.080
# log (LMDI) split: order-independent, parts add up exactly to the rupee change
tot_log = math.log(r1 / r0)
parts = {k: (r1 - r0) * math.log(this[k] / last[k]) / tot_log for k in last}
for k, v in parts.items():
    print(f"{k:6} {v:>12,.0f}  share of change {abs(v / (r1 - r0)) * (1 if v * (r1 - r0) > 0 else -1) if abs(v) > 1 else 0:+.0%}")
assert abs(sum(parts.values()) - (r1 - r0)) < 1e-6
assert abs(parts["opb"]) < 1e-6
assert round(parts["conv"] / (r1 - r0), 2) == 1.00      # conversion explains ~all of the drop
assert round(parts["aov"] / (r1 - r0), 2) == -0.24      # AOV partly offset it
assert round(parts["users"] / (r1 - r0), 2) == 0.24
# calendar check: 31-day month versus 30-day month
print(f"days effect alone: {30/31 - 1:+.1%}; revenue per day change {(r1/30)/(r0/31) - 1:+.1%}")
assert round(30/31 - 1, 3) == -0.032 and round((r1/30)/(r0/31) - 1, 3) == -0.050
# drill the winning branch: conversion by platform (illustrative)
seg = {"android": (0.80, 0.050, 0.045), "ios": (0.15, 0.050, 0.050), "web": (0.05, 0.050, 0.050)}
# (traffic share, conv last, conv this) shares held fixed for the drill
c0 = sum(s * a for s, a, b in seg.values()); c1 = sum(s * b for s, a, b in seg.values())
print(f"blended conv {c0:.2%} -> {c1:.2%}")
for k, (s, a, b) in seg.items():
    print(f"{k:8} share-weighted drop {s * (b - a) * 100:+.2f} pts of conversion")
assert round(c0, 3) == 0.050 and round(c1, 3) == 0.046
```

**Output (my run):**
```text
revenue last 40,000,000  this 36,785,280  change -8.04%
users      -775,182  share of change +24%
conv     -3,199,369  share of change +100%
opb               0  share of change +0%
aov         759,831  share of change -24%
days effect alone: -3.2%; revenue per day change -5.0%
blended conv 5.00% -> 4.60%
android  share-weighted drop -0.40 pts of conversion
ios      share-weighted drop +0.00 pts of conversion
web      share-weighted drop +0.00 pts of conversion
```

**Follow-ups:**
- Two branches both fell. What now? Rank by contribution and treat them as separate hypotheses. If they are linked (a bug lowers conversion and so orders per buyer) fix the upstream one first.
- Where does the tree stop being useful? When the next level cannot be queried (no data) or the cause is a decision, not a number. Then I switch to timeline matching and an experiment or holdout.
- Is there a cross-reference? The same ideas in A/B form are in Book 1 Part 10, Q16 ("A metric (conversion, orders) dropped after a launch. How would you investigate whether it is real, caused by the launch, or a data issue?").

**Common mistakes:**
- Comparing a 31-day month with a 30-day month without adjusting.
- Additive trees (revenue = A + B + C) where the factors multiply, so the shares are not meaningful.
- Reporting the percent change of each factor and calling the biggest percentage the cause; the contribution to rupees is what matters.
- No stop rule, or stopping at a correlation without a date match.

### Q13 ⭐⭐⭐ 🟡 Orders reported by the client-side checkout_complete event are up 4%, but finance's order table shows flat orders, and the conversion dashboard (built on the event) looks healthy. Explain how you would decide which number to trust, where the gap could come from, and what you would fix first.
**Asked at:** Funnel and checkout-conversion case pages (a Prachub Amazon checkout-conversion root-cause page, funnel guides from Amplitude, Hackle and Datadog); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I trust the finance order table until proven otherwise, because it is the system of record, and I reconcile the client event to it order by order to find duplicates, phantom events and missing events before I believe the conversion dashboard.

**Clarifying questions:**
- Does finance count paid orders, shipped orders, or all placed orders? The two must use the same definition or the gap is meaningless.
- When exactly does checkout_complete fire (button click, payment sent, confirmation page loaded)? Firing before payment is confirmed creates phantom orders.
- Did an app version, SDK or consent-banner change ship in the last weeks? It tells me whether the 4% starts on a date.
- Does the event carry an order_id? Without it I can only reconcile on counts, not rows.
- Is the gap concentrated in one platform or version? One version points to a client bug, not a business effect.

**Approach:**
1. Align definitions and time zone. Same date, same status, same currency or test-order filter.
2. Join events to finance on order_id. Count four buckets: matched, duplicate events (same order_id twice), phantom events (no finance order), and finance orders with no event (lost events).
3. Cut each bucket by platform, app version, payment method and hour. A version that spikes is the suspect.
4. Check timing: the 4% should start the day a release or SDK change went live.
5. Fix first the event itself (fire once, after server confirmation, with order_id and idempotency key), then restate the history from the order table.
6. Rebuild the conversion dashboard on the server-side order table, and keep the client event only for funnel steps.

**Metrics:**
- Event orders = count of checkout_complete rows. Finance orders = count of rows in the order table with a paid status.
- Gap = event orders / finance orders - 1.
- Duplicate rate = (events - distinct order_ids) / events. Phantom rate = distinct event order_ids not in finance / distinct event order_ids.
- Conversion = finance orders / sessions (or checkout starts). Compare it to the event-based version.
- Guardrail: a daily reconciliation check that alerts when the gap passes a threshold (for example 1%).

**Risks:**
- Trusting the dashboard because it "looks healthy". A bug can make a dashboard look healthy.
- Finance may also be wrong: late status updates, test orders, or cancellations. I check that finance is stable week to week, but it is still the better source of truth for money.
- Ad blockers or offline mode can lose events, so event counts can also be too low.
- Fixing the event and forgetting to restate history, so the trend breaks.

**What the interviewer scores:**
- Strong: chooses the system of record with a reason and then reconciles row by row. Weak: averages the two numbers.
- Strong: lists specific mechanisms (duplicates, early fire, retries, replay, bots). Weak: "tracking issue".
- Strong: fixes the source first and restates the metric. Weak: patches the dashboard only.
- Strong: adds a standing reconciliation alarm.

**Example:** (illustrative numbers) 100,000 real orders. Client events: one per order, plus 3,000 double fires from retry or back navigation, plus 1,000 fired before payment confirmed and later failed. Raw events are 104,000 (+4.0%), distinct order_ids are 101,000, matched to finance are 100,000, phantoms 1,000, duplicates 3,000. On 3,000,000 sessions: event conversion 3.467%, finance conversion 3.333%. The "healthy" conversion is overstated by 4.0%. Weak answer: "Orders are up 4%, nice." Strong answer: "Real orders are flat. Of the 4,000 extra events, 3,000 are duplicate fires and 1,000 are failed payments. I fix the event."

**Code:**
```python
# Reconcile client events to the finance table by order_id (illustrative, deterministic)
finance = set(range(100_000))                   # orders finance booked
events = list(range(100_000))                   # one checkout_complete per real order
events += list(range(3_000))                    # 3,000 double fires (retry / back-navigation)
events += list(range(200_000, 201_000))         # 1,000 fired before payment confirmed (failed)
raw = len(events)
dedup = set(events)
matched = dedup & finance
phantom = dedup - finance
dupes = raw - len(dedup)
print("raw client events      :", raw)
print("distinct order_ids     :", len(dedup))
print("matched to finance     :", len(matched))
print("phantom (no finance)   :", len(phantom))
print("duplicate fires        :", dupes)
assert raw == 104_000 and len(matched) == 100_000 and len(phantom) == 1_000 and dupes == 3_000
sessions = 3_000_000
print(f"conversion on raw event : {raw / sessions:.3%}")
print(f"conversion on finance   : {len(matched) / sessions:.3%}")
assert round(raw / sessions, 5) == 0.03467 and round(len(matched) / sessions, 5) == 0.03333
print(f"overstatement           : {raw / len(matched) - 1:+.1%}")
assert round(raw / len(matched) - 1, 3) == 0.040
```

**Output (my run):**
```text
raw client events      : 104000
distinct order_ids     : 101000
matched to finance     : 100000
phantom (no finance)   : 1000
duplicate fires        : 3000
conversion on raw event : 3.467%
conversion on finance   : 3.333%
overstatement           : +4.0%
```

**Follow-ups:**
- What if finance is flat because of a delay in loading? Check the order table's load time and late-arriving rows; recount after a few days. The row-level join shows it (finance orders with no event or events with late finance rows).
- What if the gap is not exactly duplicates? Then bucket the residual by version and payment method. A client bug usually shows as a step on one version.
- How do you prevent it? Fire the success event from the server after payment confirmation, with an idempotency key, and run a daily reconciliation.

**Common mistakes:**
- Comparing counts only, never joining on order_id.
- Picking the number that supports the good news.
- Fixing the dashboard filter and not the event.
- Forgetting that conversion built on the bad event is also wrong, not only the order count.

### Q14 ⭐⭐⭐ 🔴 The company redefined 'active user' in the middle of the quarter, from any app open to any open followed by a meaningful action, and the new dashboard shows MAU down 14% overnight. Explain how you would report the quarter honestly, rebuild a comparable series, and what you would say to an exec who wants to know if the business shrank.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** The 14% is a definition change, not a business change until I prove otherwise, so I backfill both definitions on raw events for the whole quarter, report one series like for like, and show the step as a bridge.

**Clarifying questions:**
- On which exact date did the new definition go live, and is the old series still computable from raw events? I need both on the same dates to build the bridge.
- What counts as a meaningful action, and did the list of actions change during the quarter? A moving action list moves the series.
- Do executives and the board have prior numbers on the old definition (targets, bonuses, investor reporting)? That decides how loudly I flag the restatement.
- Is raw event history retained long enough to backfill a year? If not I need a sampled method.
- Which downstream metrics (retention, ARPU per active user) use the active-user denominator? They all shift too.

**Approach:**
1. Write down the break: date, old and new definitions, who approved it.
2. Recompute the quarter under both definitions from raw events: old (any open) and new (open plus meaningful action). Use the same user ID rules, same time zone and same bot filter.
3. Report the new definition for the entire history (restated), not a stitched series. Keep the old series as a reference line for continuity.
4. Build a bridge: old MAU -> definition step -> real change -> new MAU.
5. Check the ratio (new / old) over time. A stable ratio means the break is purely definitional. A falling ratio means real engagement is getting shallower, which is a business signal.
6. Tell the exec in one sentence: the business did not shrink, the ruler changed. Give the like-for-like growth number and the ratio trend.
7. Fix the process: versioned metric definitions, a change log, and a rule that every definition change ships with a backfill.

**Metrics:**
- MAU (old) = distinct users with at least one app open in the calendar month.
- MAU (new) = distinct users with at least one app open followed by at least one meaningful action in the same month.
- Action share = MAU (new) / MAU (old).
- Like-for-like growth = MAU (same definition) this month / the same definition a quarter earlier - 1.
- Guardrails: downstream metrics (retention, ARPU) restated on the same definition.

**Risks:**
- A stitched series (old before, new after) shows a fake cliff and fake decline.
- Backfill inconsistent with the live pipeline (different bot filter) creates a second break.
- Hiding the change to avoid a hard conversation. Someone will find it later and trust will drop.
- If the action share is falling, "it is only the definition" would be wrong.

**What the interviewer scores:**
- Strong: separates the definitional step from the real change numerically. Weak: argues about which definition is better.
- Strong: backfills and restates; does not stitch. Weak: adds a footnote.
- Strong: gives the exec a plain sentence and a number. Weak: gives a lecture.
- Strong: proposes governance (versioning, change log). Weak: stops at this quarter.

**Example:** (illustrative numbers, millions) Old definition: Apr 10.00, May 10.05, Jun 10.00. New definition, backfilled: Apr 8.58, May 8.64, Jun 8.60. The dashboard showed Apr 10.00 (old) and Jun 8.60 (new), so -14.0%. Like for like, the old definition is flat (+0.0%) and the new is +0.2%. Action share is 85.8%, 86.0%, 86.0%, so it is stable. Bridge: 10.00 - 1.42 (definition) + 0.02 (real) = 8.60. Weak answer: "MAU is down 14%, we have a problem" or "ignore it, it is only a definition". Strong answer: "The business is flat on both definitions. The 14% is the definition step; here is the bridge."

**Code:**
```python
# Illustrative monthly MAU in millions. 'open' = old definition, 'action' = new definition.
months = ["Apr", "May", "Jun"]
open_mau   = {"Apr": 10.00, "May": 10.05, "Jun": 10.00}
action_mau = {"Apr": 8.58,  "May": 8.64,  "Jun": 8.60}   # backfilled from raw events
# what the exec dashboard showed: old definition before the switch, new one after
shown = {"Apr": open_mau["Apr"], "May": open_mau["May"], "Jun": action_mau["Jun"]}
headline = shown["Jun"] / shown["Apr"] - 1
old_like = open_mau["Jun"] / open_mau["Apr"] - 1
new_like = action_mau["Jun"] / action_mau["Apr"] - 1
print(f"dashboard Apr->Jun         {headline:+.1%}")
print(f"old definition, like for like {old_like:+.1%}")
print(f"new definition, like for like {new_like:+.1%}")
assert round(headline, 3) == -0.140 and old_like == 0 and round(new_like, 4) == 0.0023
for m in months:
    print(m, f"action share of open users {action_mau[m] / open_mau[m]:.1%}")
assert round(action_mau["Apr"] / open_mau["Apr"], 3) == 0.858
# the definitional step is the whole drop: bridge in millions
print("bridge (M): old Apr", open_mau["Apr"], "-> definition step", round(action_mau["Apr"] - open_mau["Apr"], 2),
      "-> real change", round(action_mau["Jun"] - action_mau["Apr"], 2), "= new Jun", action_mau["Jun"])
assert abs(open_mau["Apr"] + (action_mau["Apr"] - open_mau["Apr"]) + (action_mau["Jun"] - action_mau["Apr"]) - action_mau["Jun"]) < 1e-9
```

**Output (my run):**
```text
dashboard Apr->Jun         -14.0%
old definition, like for like +0.0%
new definition, like for like +0.2%
Apr action share of open users 85.8%
May action share of open users 86.0%
Jun action share of open users 86.0%
bridge (M): old Apr 10.0 -> definition step -1.42 -> real change 0.02 = new Jun 8.6
```

**Follow-ups:**
- What if the new definition is better but history cannot be rebuilt? Report a sampled rebuild with a stated error, and show both series for a quarter of overlap.
- What if the exec insists on the old number for the board deck? Show both with the bridge. Do not report an unlabelled stitched series.
- How is this different from a tracking bug? A bug is an error in the same definition. A definition change is a deliberate new ruler. Both need a restatement, but the bug is also corrected, not versioned. See also Book 6 Part 1 Q38, which is about a changed denominator.

**Common mistakes:**
- Reporting -14% as business decline.
- Reporting "no change" without showing the ratio.
- Comparing new-definition months to old-definition history.
- Forgetting to restate retention and ARPU, which use the same denominator.

### Q15 ⭐⭐⭐ 🔴 A 12% drop in orders is concentrated in one metro city and started on a Tuesday. The city had heavy rain, a competitor discount, and a local delivery-partner strike in the same week. Describe how you would separate the explanations and quantify each, and what data you would need beyond your own logs.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** Three causes hit the same week, so I split by where they act (demand side or supply side), use other cities as a counterfactual, estimate rain from history, and use outside data for the competitor; what I cannot separate I report as a range.

**Clarifying questions:**
- Which metric is "orders": placed or fulfilled? The two separate demand from supply.
- Exact hour the drop started on Tuesday, and did it start everywhere in the city at once? A strike usually starts in specific zones; rain follows the weather map.
- Did the strike close restaurants, riders, or both, and is there a dated news source? I need the start and end for the timeline.
- Do I have other comparable cities with no events? They give the control.
- Did the competitor discount cover the whole city and which categories? It tells me which orders should move.

**Approach:**
1. Establish the counterfactual: what this city would have done without the week. Use the city's own history and a control group of similar cities (difference in differences, or a synthetic control; see Book 1 Part 10, Q28 and Q49 for the method).
2. Split the funnel to separate demand from supply: app opens, searches, orders placed, orders fulfilled, cancellations by reason ("no partner available").
3. Strike: look for supply signals. Partner online hours, assignment time, "no partner found" cancellations, ETAs shown. If placed orders held and fulfilment fell, it is supply.
4. Rain: estimate the rain effect from history (past rainy days in this and other cities, with mm of rain as a regressor), then apply it to this week's rain.
5. Competitor: outside data (price scraping of their app, app-store ranking, third-party panel, search interest). Look at price-sensitive orders and categories, and at users who open but do not buy.
6. Use timing and dose: rain varies by day, strike by zone and start time, the discount by category. Each has a different fingerprint.
7. Report each part with a range and say what remains unexplained.

**Metrics:**
- Orders fulfilled / day, versus counterfactual. Drop % = actual / counterfactual - 1.
- Placed orders / day, fulfilment rate = fulfilled / placed, cancellations with reason "no partner".
- Rain effect = coefficient on mm of rain in a log(orders) regression fit on history.
- Demand-side loss = (placed this week - placed baseline) x baseline fulfilment rate. Supply-side loss = placed this week x (fulfilment rate this week - baseline fulfilment rate). These two sum exactly to the change in fulfilled orders.
- Guardrails: other cities flat (so the control is valid), delivery time, refund rate.

**Risks:**
- The three causes overlap in time, so regression with three dummies can not separate them. Timing, zone and category variation are what separate them.
- The strike also lowers demand (customers see long ETAs and do not order), so "demand side" is not purely rain and competitor.
- Control cities are not truly flat or are affected by the same national weather.
- Outside data is thin (a competitor's scrape is not their real order volume).

**What the interviewer scores:**
- Strong: counterfactual first, then demand/supply split, then one method per cause. Weak: picks the most dramatic cause (the strike).
- Strong: asks for outside data (weather, competitor prices, strike dates, news). Weak: only looks at own logs.
- Strong: gives numbers with ranges and a residual. Weak: gives percentages that sum to 100% with false precision.
- Strong: says which findings are causal and which are only consistent with the data.

**Example:** (illustrative numbers) Baseline 10,000 fulfilled orders per day, observed 8,800 (-12%). Placed orders fell from 10,400 to 9,900, and the fulfilled share of placed orders fell from 96.2% to 88.9%. Demand-side loss = (9,900 - 10,400) x 0.9615 = -481 orders. Supply-side loss = 9,900 x (0.8889 - 0.9615) = -719 orders. Total -1,200. So about 40% demand and 60% supply. From a regression on 120 days of history, rain costs about 1.1% per 10 mm; this week's rain days (25, 30, 20, 10 mm) give about -1.4% for the week, about -137 orders a day. The demand remainder, about -344 orders a day, is competitor plus any strike-driven demand loss. Strong answer: "About 60% supply (the strike), about 10% rain, about 30% competitor or other demand, with wide ranges." Weak answer: "It was the strike."

**Code:**
```python
import numpy as np
rng = np.random.default_rng(7)
# 1) History: 120 normal days of city orders, baseline 10,000/day, rain costs about 1.2% per 10 mm
days = 120
rain = np.where(rng.random(days) < 0.25, rng.gamma(2.0, 6.0, days), 0.0)   # mm
true_slope = -0.0012                                                       # per mm, log scale
noise = rng.normal(0, 0.01, days)
orders = 10_000 * np.exp(true_slope * rain + noise)
X = np.column_stack([np.ones(days), rain])
beta = np.linalg.lstsq(X, np.log(orders), rcond=None)[0]
print(f"estimated rain effect: {beta[1] * 10:+.2%} per 10 mm (true {true_slope * 10:+.2%})")
assert abs(beta[1] - true_slope) < 0.0003
# 2) Event week: rain by day (mm), control cities flat, city down 12% vs the control-based counterfactual
week_rain = np.array([0, 0, 25, 30, 20, 10, 0.0])         # Tue is index 2
rain_loss = float(np.mean(np.exp(beta[1] * week_rain) - 1))
print(f"rain explains about {rain_loss:+.1%} of the week")
total = -0.12
left = total - rain_loss
print(f"left for competitor + strike: {left:+.1%}")
# 3) Funnel split: placed orders (demand side) vs fulfilled share of placed (supply side), illustrative
placed0, ful0 = 10_400, 10_000 / 10_400
placed1, ful1 = 9_900, 8_800 / 9_900
demand = (placed1 - placed0) * ful0                    # fewer orders placed, old fulfilment rate
supply = placed1 * (ful1 - ful0)                       # more placed orders not fulfilled
print(f"placed {placed0:,} -> {placed1:,}; fulfilled share {ful0:.1%} -> {ful1:.1%}")
print(f"demand-side loss {demand:,.0f} orders, supply-side loss {supply:,.0f} orders, total {demand + supply:,.0f}")
assert round(demand + supply) == -1_200
assert round(demand) == -481 and round(supply) == -719
print(f"demand share {demand / -1200:.0%}, supply share {supply / -1200:.0%}")
assert round(demand / -1200, 2) == 0.40
# rain is demand-side (rain effect above) so competitor ~ demand-side remainder
rain_orders = rain_loss * 10_000
print(f"rain orders {rain_orders:,.0f}; competitor (demand remainder) {demand - rain_orders:,.0f}")
assert round(rain_orders) == -137 and round(demand - rain_orders) == -344
```

**Output (my run):**
```text
estimated rain effect: -1.14% per 10 mm (true -1.20%)
rain explains about -1.4% of the week
left for competitor + strike: -10.6%
placed 10,400 -> 9,900; fulfilled share 96.2% -> 88.9%
demand-side loss -481 orders, supply-side loss -719 orders, total -1,200
demand share 40%, supply share 60%
rain orders -137; competitor (demand remainder) -344
```

**Follow-ups:**
- How would you check the competitor effect cleanly? Compare zones or categories where the discount applied against those where it did not (difference in differences), and look at users who opened a competitor-priced category.
- What if the strike ends and orders do not recover? Then some of it was lasting: lost users or habit change. Track returning-user rate and cohort recovery for weeks.
- Could a geo experiment work? Not for a past event; for a future response use matched markets (Book 1 Part 10, Q44).

**Common mistakes:**
- Treating the three causes as additive percentages without a counterfactual.
- Using only own logs.
- Ignoring that the cities used as control were also hit by national weather or the same competitor.
- Claiming precision (for example "rain 17.3%") from overlapping events.

### Q16 ⭐⭐⭐ 🔴 A ranking change in the home feed lifts click-through rate 7% in the experiment, but orders per user are down 1.5% and cancellations are up. Explain how this can happen, which metric should decide, and how you would check the long-run effect before rolling out.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** CTR is a proxy; orders per user (net of cancellations) is the goal, so I would not ship a ranking that wins clicks and loses orders, and I would verify the long run with a holdout.

**Clarifying questions:**
- How is CTR defined (clicks / impressions or users who clicked / users)? It changes how a few heavy clickers move it.
- Are the orders-per-user and cancellation differences statistically significant, and over how many days? A -1.5% on a small sample can be noise.
- Which categories and price points gained impressions? That shows what the ranker now prefers.
- Are cancellations driven by the customer, restaurant or stock? Stock-outs point at a ranker that ignores availability.
- Was the test long enough to pass the novelty window? Novelty inflates CTR early (Book 1 Part 10, Q8).

**Approach:**
1. Check validity first: sample ratio, logging, same exposure rules (Book 1 Part 10, Q6).
2. Show the whole funnel per user: impressions, clicks, add-to-cart, orders placed, orders cancelled, orders completed.
3. Find the mechanism by cuts: items that gained position (price, ETA, stock, category, discount), new versus returning users, query types.
4. Likely mechanisms: clickbait (attractive thumbnails, deep discounts, curiosity), more clicks on items that are out of stock or slow, position bias (higher slot gets more clicks regardless of fit), wider but worse matching (more browsing, fewer decisions), diversity loss.
5. Decide on the metric closest to value: completed orders per user (or revenue per user net of refunds), with cancellations as a guardrail. CTR becomes a diagnostic.
6. Long-run check: keep a long-term holdout (Book 1 Part 10, Q24), run 4 to 8 weeks, watch repeat orders, retention, and novelty decay (new versus returning, week by week).
7. If the orders loss is real, fix the objective: train the ranker on orders or add availability and ETA to the score, then retest.

**Metrics:**
- CTR = clicks / impressions. Orders per user = orders placed / users in arm.
- Cancellation rate = cancelled orders / placed orders. Completed orders per user = orders placed x (1 - cancellation rate) / users.
- Click-to-order = completed orders / clicks.
- Guardrails: p95 latency, search exit rate, 7-day retention, diversity of items ordered.

**Risks:**
- Ranker trained on click labels learns to optimise clicks, not value.
- Short test overstates CTR through novelty.
- The primary metric flipping sign with cancellations (placed up, completed down).
- Ratio metrics with changing denominators: more impressions per user lower CTR even if clicks rise.

**What the interviewer scores:**
- Strong: names a mechanism and checks it in the data. Weak: "CTR is not everything".
- Strong: picks completed orders per user as decision metric and says why. Weak: ships because CTR is the stated goal.
- Strong: asks about significance and test length. Weak: reacts to 1.5% as if exact.
- Strong: proposes a long-term holdout and objective change. Weak: "run it longer" with no plan.

**Example:** (illustrative numbers) 100,000 users per arm. CTR 10.0% to 10.7% (+7.0%). Orders placed per user 0.800 to 0.788 (-1.5%). Cancellation 5.0% to 6.5%. Completed orders per user: 0.760 to 0.7368 (-3.1%). With 50 impressions per user, clicks per user go from 5.00 to 5.35, but completed orders per 100 clicks go from 15.2 to 13.8: more clicks of lower value. If order counts are roughly Poisson (assumption), z = -3.0 for placed and -6.0 for completed, so both are unlikely to be noise. Weak answer: "CTR is up 7%, ship." Strong answer: "Net completed orders per user fell about 3%, the ranker buys clicks, do not ship; retrain on orders and retest with a holdout."

**Code:**
```python
from math import sqrt
from scipy.stats import norm
# Illustrative A/B: 100,000 users per arm
n = 100_000
ctr0, ctr1 = 0.100, 0.107                      # clicks / impressions
print(f"CTR lift {ctr1 / ctr0 - 1:+.1%}")
assert round(ctr1 / ctr0 - 1, 3) == 0.070
opu0 = 0.800
opu1 = opu0 * (1 - 0.015)                      # orders placed per user, -1.5%
cancel0, cancel1 = 0.050, 0.065                # share of placed orders cancelled
done0 = opu0 * (1 - cancel0)
done1 = opu1 * (1 - cancel1)
print(f"placed per user {opu0:.3f} -> {opu1:.3f}")
print(f"completed per user {done0:.4f} -> {done1:.4f} ({done1 / done0 - 1:+.1%})")
assert round(opu1, 3) == 0.788 and round(done0, 3) == 0.760 and round(done1 / done0 - 1, 3) == -0.031
# is the placed-orders gap noise? Poisson assumption: variance = mean (assumption, not data)
def z(m0, m1):
    se = sqrt(m0 / n + m1 / n)
    return (m1 - m0) / se
for name, a, b in [("placed", opu0, opu1), ("completed", done0, done1)]:
    zz = z(a, b); p = 2 * (1 - norm.cdf(abs(zz)))
    print(f"{name:10} z={zz:+.2f} p={p:.4f}")
assert round(z(opu0, opu1), 1) == -3.0 and round(z(done0, done1), 1) == -6.0
# what a click-based metric hides: orders per 1,000 impressions-led clicks (illustrative clicks per user)
imp = 50  # impressions per user
c0, c1 = ctr0 * imp, ctr1 * imp
print(f"clicks per user {c0:.2f} -> {c1:.2f}; completed orders per 100 clicks {100 * done0 / c0:.1f} -> {100 * done1 / c1:.1f}")
assert round(100 * done0 / c0, 1) == 15.2 and round(100 * done1 / c1, 1) == 13.8
```

**Output (my run):**
```text
CTR lift +7.0%
placed per user 0.800 -> 0.788
completed per user 0.7600 -> 0.7368 (-3.1%)
placed     z=-3.01 p=0.0026
completed  z=-6.00 p=0.0000
clicks per user 5.00 -> 5.35; completed orders per 100 clicks 15.2 -> 13.8
```

**Follow-ups:**
- What if orders per user were flat and only cancellations rose? Still a loss: users get a worse experience and support cost rises. Look at revenue net of cancellations.
- Why not trust CTR when it rose significantly? Significance says the change is real, not that it is valuable. It can be real and harmful.
- How do you know the harm is not just novelty? Plot the effect by experiment week and by new versus returning users; novelty decays, harm that stays or grows is real. See also Book 1 Part 10, Q13 for the general rule when a primary metric and a guardrail disagree.

**Common mistakes:**
- Deciding on the proxy that the model was trained to optimise.
- Ignoring cancellations (using orders placed).
- Ratio metric confusion between per-impression and per-user.
- Rolling out and relying on a "monitor later" plan with no holdout.

### Q17 ⭐⭐⭐ 🔴 You launch a GenAI shopping assistant in the app. Define the funnel from exposure to success, the north star, quality and safety metrics, and the cost metric. Include what you would measure when a user asks a question and then leaves without clicking, and why standard click-based metrics can mislead here.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** I measure the assistant by successful tasks per exposed user, proven by a holdout, and I count a no-click answer as a possible success by labelling a sample instead of trusting clicks.

**Clarifying questions:**
- What is the assistant for (find a product, compare, answer policy questions)? Each task has a different success definition.
- Where is it shown and can users ignore it? The exposure rule defines the funnel and the holdout.
- Can I hold out a random group without the assistant? Without it I can show usage but not value.
- What actions can it take (only advise, or add to cart, or place orders)? More actions need stricter safety metrics.
- Are there policy or legal limits on what it may say (price, stock, medical)? They define the safety metrics.

**Approach:**
1. Funnel: eligible sessions (entry point shown) -> asked a question -> got a real answer (no error, no refusal) -> useful answer -> task success (bought, saved, or resolved) -> comes back.
2. North star: successful assisted sessions per exposed weekly user, checked against a holdout for incremental orders per 100 sessions.
3. Quality: groundedness (stated price, stock and attributes match the catalogue), relevance (human or LLM-judge score validated against humans), answer rate, refusal rate.
4. Safety: policy-violation rate, wrong price or stock claim rate, harmful or off-policy answer rate, escalation rate. These have hard thresholds, not "improve over time".
5. Cost: model cost per answered session, per successful session, per incremental order; plus latency (p95) since it affects abandonment.
6. Question then leave without click: do not call it failure. Label a random sample of such sessions (good answer read, wrong answer, unclear) and use proxies: no rephrase within a few minutes, no return to the same query, copy or share action, a later purchase within a window. Report good-abandonment rate with a confidence interval.
7. Why click metrics mislead: a good answer can end the session (the user got the price), while a bad answer can cause clicks (users hunt for the real answer). Also clicks on the chat window are not value.

**Metrics:**
- Engagement rate = users or sessions who asked / eligible. Answer rate = real answers / questions.
- Click-based success = good clicks / answered sessions, where a good click is one with no bounce-back and no rephrase.
- Label-adjusted success = (good clicks + good-abandonment rate x no-click sessions) / answered sessions.
- Incremental orders per 100 sessions = treatment orders per 100 - holdout orders per 100.
- Cost per successful session = total model cost / successful sessions.
- Guardrails: hallucinated price or stock rate, policy-violation rate, p95 latency, complaint rate, overall conversion of non-users (to check the assistant does not hurt the main flow).

**Risks:**
- Model-judge scores that drift or are biased; validate against human labels (Book 2 owns the LLM internals, here I only ask for a validated measure).
- Selection: users who open the assistant already intend to buy, so compare against a holdout, not against non-users.
- Averaging hides rare, serious safety failures. Track them as counts with zero tolerance for some classes.
- Cost grows with usage, so success can be unprofitable.

**What the interviewer scores:**
- Strong: complete funnel with exact numerators and denominators, plus a holdout. Weak: "track engagement and CSAT".
- Strong: has a method for the no-click case (sample labelling and proxies). Weak: counts all no-click as failure or all as success.
- Strong: separate quality, safety and cost metrics with thresholds. Weak: one blended score.
- Strong: ties cost to value (cost per successful session). Weak: reports total spend only.

**Example:** (illustrative numbers) 100,000 eligible sessions, 20,000 ask (20.0%), 18,800 get an answer (94.0%), 9,400 click (50.0%), 8,000 of those are good clicks. The other 9,400 left without a click. Label a random 400 of them: 240 good, 100 bad, 60 unclear, so good abandonment is 60% (95% CI 55.2% to 64.8%). Click-based success is 42.6%. Label-adjusted success is (8,000 + 0.60 x 9,400) / 18,800 = 72.6%. At Rs 0.40 per answered session (illustrative), cost per successful session is Rs 0.55. Holdout: 3.30 versus 3.10 orders per 100 sessions, an incremental 0.20. Weak answer: "Half left without clicking, so half failed." Strong answer: "Click-only success is 42.6%, the labelled sample says 72.6%; I report both and the interval."

**Code:**
```python
from math import sqrt
# Illustrative funnel for one week of a GenAI shopping assistant
eligible = 100_000        # sessions where the entry point was shown (exposure)
asked    = 20_000         # opened and asked a question (engagement)
answered = 18_800         # got a real answer (no error, no refusal)
clicked  = 9_400          # clicked a product or link from the answer
good_clk = 8_000          # clicks that did not bounce back within 10 s and were not followed by a rephrase
noclick  = answered - clicked
print(f"engagement {asked / eligible:.1%}, answer rate {answered / asked:.1%}, click rate {clicked / answered:.1%}")
assert noclick == 9_400
# human-labelled random sample of no-click sessions
sample = 400
good, bad, unclear = 240, 100, 60
assert good + bad + unclear == sample
p = good / sample
half = 1.96 * sqrt(p * (1 - p) / sample)
print(f"labelled good abandonment {p:.0%} (95% CI {p - half:.1%} to {p + half:.1%})")
assert round(p, 2) == 0.60 and round(half, 3) == 0.048
succ_click_only = good_clk / answered
succ_est = (good_clk + p * noclick) / answered
print(f"success, click-based    {succ_click_only:.1%}")
print(f"success, label-adjusted {succ_est:.1%}")
assert round(succ_click_only, 3) == 0.426 and round(succ_est, 3) == 0.726
# cost (illustrative Rs per answered session)
cost = 0.40
total_cost = cost * answered
n_succ = good_clk + p * noclick
print(f"cost per answered session Rs {cost:.2f}; per successful session Rs {total_cost / n_succ:.2f}")
assert round(total_cost / n_succ, 2) == 0.55
# incremental view: holdout (no assistant), orders per 100 sessions
treat_orders_per_100, hold_orders_per_100 = 3.30, 3.10
print(f"incremental orders per 100 exposed sessions {treat_orders_per_100 - hold_orders_per_100:.2f}")
assert round(treat_orders_per_100 - hold_orders_per_100, 2) == 0.20
```

**Output (my run):**
```text
engagement 20.0%, answer rate 94.0%, click rate 50.0%
labelled good abandonment 60% (95% CI 55.2% to 64.8%)
success, click-based    42.6%
success, label-adjusted 72.6%
cost per answered session Rs 0.40; per successful session Rs 0.55
incremental orders per 100 exposed sessions 0.20
```

**Follow-ups:**
- How big should the label sample be? Size it for the interval you need: at p = 0.6 and n = 400 the 95% half-width is about 4.8 points; quadrupling n halves it.
- What if users who get good answers then buy offline or later? Use a longer attribution window and the holdout, which captures it without attribution rules.
- Safety threshold? Set by the policy owner; for classes like wrong price shown, use a count and an alert, not an average.

**Common mistakes:**
- Using click-through rate as the headline success metric.
- No holdout, so selection bias looks like impact.
- Measuring quality only by LLM-judge without human calibration.
- Ignoring cost per success and latency.

### Q18 ⭐⭐⭐ 🔴 Average revenue per user (ARPU) fell from Rs 112 to Rs 104 company-wide, but ARPU rose in every one of the three countries you operate in. Show with a small numeric table how a mix shift produces this, how you would split the change into a within-country effect and a mix effect, and what you would report.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
**Say this first (1 line):** This is mix shift (Simpson's paradox in a rollup): ARPU rose inside every country but users moved toward the lower-ARPU country, so the blend fell; I split the change into a within-country effect and a mix effect and report both.

**Clarifying questions:**
- Is ARPU revenue / active users per period with the same definition of user in all countries? A different definition per country breaks the comparison.
- Is currency converted at a fixed rate? Exchange-rate moves can create fake within-country change.
- Do I have users and revenue per country for both periods? I need them for the table.
- Which question matters to the audience: "are we healthy in each market" or "what is blended revenue per user"? It decides what I lead with.
- Is the shift planned (we pushed growth in the low-ARPU country) or accidental? It changes the message.

**Approach:**
1. Build the table: users share and ARPU for each country, both periods. Check that company ARPU = sum of share x ARPU.
2. Split: change = within effect + mix effect.
   - Within = sum of old share x (new ARPU - old ARPU). Mix = sum of (new share - old share) x new ARPU. They sum exactly to the change.
3. State the convention. The alternative (new-share weights for within, old ARPU for mix) gives a slightly different split. The gap is the interaction term; I show both, or use the midpoint.
4. Add the constant-mix ARPU: new country ARPUs at last period's mix. It is the like-for-like number.
5. Report: company ARPU down 8 because of mix, with every country up. Then say if the mix is fine (planned growth in a low-ARPU market) or not.
6. Add total revenue and total users, because ARPU can fall while revenue rises.

**Metrics:**
- ARPU = revenue / active users in the period. Country share = country users / total users.
- Within effect = sum over countries of old share x (new ARPU - old ARPU).
- Mix effect = sum over countries of (new share - old share) x new ARPU.
- Constant-mix ARPU = sum of old share x new ARPU.
- Guardrails: total revenue, total users, ARPU by country with confidence ranges.

**Risks:**
- The decomposition depends on the weighting convention; do not quote one split as exact.
- The "mix" may hide a finer mix (plans, cohorts) inside each country.
- Telling leaders ARPU fell when each market improved causes the wrong action (for example cutting the market that is growing fastest).
- Fixed versus floating exchange rate.

**What the interviewer scores:**
- Strong: builds the table and a split that sums exactly. Weak: only names Simpson's paradox.
- Strong: states the convention and shows sensitivity. Weak: reports one split as "the truth".
- Strong: reports constant-mix ARPU and total revenue. Weak: reports only the blended fall.
- Strong: connects to action (planned growth versus a leak). Weak: "ARPU is down, fix it".

**Example:** (illustrative numbers) Last period: user shares A 30%, B 30%, C 40%; ARPU Rs 200, 100, 55; company ARPU = 60 + 30 + 22 = Rs 112. This period: shares A 20%, B 30%, C 50%; ARPU Rs 210, 105, 61; company ARPU = 42 + 31.5 + 30.5 = Rs 104. Every country is up (+5.0%, +5.0%, +10.9%). Convention 1: within +6.9, mix -14.9, total -8.0. Convention 2: within +6.5, mix -14.5, total -8.0. Constant-mix ARPU is Rs 118.9 against Rs 112 last period. Weak answer: "ARPU fell 7%, something is broken." Strong answer: "Each market improved; the blend fell because the share of the Rs 55 market rose from 40% to 50%. At constant mix ARPU is up 6.1%."

**Code:**
```python
# Illustrative: user shares and ARPU (Rs) by country
shares0 = {"A": 0.30, "B": 0.30, "C": 0.40}
shares1 = {"A": 0.20, "B": 0.30, "C": 0.50}
arpu0   = {"A": 200.0, "B": 100.0, "C": 55.0}
arpu1   = {"A": 210.0, "B": 105.0, "C": 61.0}
tot0 = sum(shares0[k] * arpu0[k] for k in arpu0)
tot1 = sum(shares1[k] * arpu1[k] for k in arpu1)
print(f"company ARPU {tot0:.1f} -> {tot1:.1f}")
assert round(tot0, 6) == 112 and round(tot1, 6) == 104
for k in arpu0:
    print(k, f"share {shares0[k]:.0%}->{shares1[k]:.0%}  ARPU {arpu0[k]:.0f}->{arpu1[k]:.0f} ({arpu1[k] / arpu0[k] - 1:+.1%})")
    assert arpu1[k] > arpu0[k]
d = tot1 - tot0
# Convention 1: within at OLD shares, mix at NEW ARPU
within1 = sum(shares0[k] * (arpu1[k] - arpu0[k]) for k in arpu0)
mix1 = sum((shares1[k] - shares0[k]) * arpu1[k] for k in arpu0)
# Convention 2: within at NEW shares, mix at OLD ARPU
within2 = sum(shares1[k] * (arpu1[k] - arpu0[k]) for k in arpu0)
mix2 = sum((shares1[k] - shares0[k]) * arpu0[k] for k in arpu0)
print(f"total change {d:+.1f}")
print(f"conv 1 (old-share weights): within {within1:+.1f}, mix {mix1:+.1f}, sum {within1 + mix1:+.1f}")
print(f"conv 2 (new-share weights): within {within2:+.1f}, mix {mix2:+.1f}, sum {within2 + mix2:+.1f}")
assert round(within1, 6) == 6.9 and round(mix1, 6) == -14.9
assert round(within2, 6) == 6.5 and round(mix2, 6) == -14.5
assert abs(within1 + mix1 - d) < 1e-9 and abs(within2 + mix2 - d) < 1e-9
# constant-mix ARPU: today's ARPU at last period's shares
cm = sum(shares0[k] * arpu1[k] for k in arpu0)
print(f"ARPU at old mix with new country ARPUs: {cm:.1f} (vs 112.0 last period)")
assert round(cm, 6) == 118.9
```

**Output (my run):**
```text
company ARPU 112.0 -> 104.0
A share 30%->20%  ARPU 200->210 (+5.0%)
B share 30%->30%  ARPU 100->105 (+5.0%)
C share 40%->50%  ARPU 55->61 (+10.9%)
total change -8.0
conv 1 (old-share weights): within +6.9, mix -14.9, sum -8.0
conv 2 (new-share weights): within +6.5, mix -14.5, sum -8.0
ARPU at old mix with new country ARPUs: 118.9 (vs 112.0 last period)
```

**Follow-ups:**
- Which number do you tell the board? Both: constant-mix ARPU for performance and blended ARPU for what the company earns per user, with total revenue. See also Book 1 Part 10, Q10 (Simpson's paradox in an A/B test) for the same arithmetic inside an experiment.
- Is the mix shift bad? Not by itself. If the low-ARPU market is the growth engine and its ARPU is rising, it may be good. It is bad if it is the result of losing high-ARPU users.
- What about more than three countries? Same formulas, summed over segments. Keep the segments few and stable.

**Common mistakes:**
- Quoting the within and mix split as exact, without the convention.
- Using a share of revenue instead of a share of users as the weight.
- Forgetting that currency moves can fake the within effect.
- Presenting the blended fall as a product failure.
