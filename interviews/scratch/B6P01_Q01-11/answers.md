### Q1 ⭐⭐⭐ 🟢 Daily active users fell 10% week over week. The dashboard shows 1.00 million DAU two weeks ago, 0.98 million last week and 0.90 million this week, with no release notes anywhere. Walk through how you would find out whether the drop is real and what caused it, and what you would check in the first hour.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** First I check the number is real (pipeline, definition, a one-off day), then I split the drop by platform, country, version, user type and day, and the segment that holds most of the drop tells me where to dig.

**Clarifying questions:**
- Is "DAU" the same definition and the same query as before? Why: a changed definition or a broken job looks exactly like a drop.
- Did the drop start on one day (a step) or slide down (a trend)? Why: a step points to a release, outage or logging change; a slide points to behaviour or mix.
- Is the drop in all products and regions or only some? Why: it picks the first cut.
- Do other numbers move too (installs, sessions, backend requests, revenue)? Why: if revenue and server traffic are flat, suspect tracking.
- What changed outside the product (marketing spend, a holiday, a competitor, an OS update)? Why: "no release notes" does not mean no change.

**Approach:**
1. Restate the numbers. 1.00M to 0.98M to 0.90M is -8.2% week over week and -10.0% over two weeks. The "10% week over week" is really 10% over two weeks; the latest week is -8.2%. I would say out loud which one I am diagnosing.
2. Hour one, validate the data: pipeline freshness, event volume by hour, duplicate or missing partitions, a second source (backend logins, server logs). If the sources disagree, stop and fix the measurement first.
3. Judge noise: compare to the usual week-over-week wobble. An 8% move against a 1% wobble is not noise.
4. Cut by time (which day did it step), platform, app version, country, new versus existing, acquisition channel. Rank segments by share of the absolute drop, not by percent change.
5. Form two or three hypotheses from the top segment (release, outside event, tracking), and test each with one query.
6. Quantify the cause (how many DAU it explains) and say what you do next: roll back, fix tracking, or watch.
7. Stop when the explained part covers most of the drop and the story fits the timing.

**Metrics:**
- DAU = distinct users with a qualifying action on that calendar day (state the action and time zone).
- Share of drop for a segment = (segment change) / (total change). The shares add to 100%.
- WoW change = this week / last week - 1. Compare to the history of WoW changes.
- Guardrails while you dig: backend order or login counts, crash rate, event volume per active user.

**Risks:**
- Chasing a pipeline problem as a product problem (or the other way round).
- Reading percent change by segment: a small segment with -40% looks bigger than a big segment with -8%.
- Calendar traps: a holiday, a weekday mix, a time-zone cut-off.
- Stopping at the first plausible story without timing evidence.

**What the interviewer scores:**
- Strong: validates the data before theorising, uses a decomposition ranked by share of drop, states the first-hour checklist.
- Strong: separates internal causes (release, tracking) from external ones (season, competitor) and names the evidence for each.
- Weak: jumps to "marketing must have cut spend" with no check.
- Weak: lists causes with no order and no way to decide between them.
- Cross-reference: Book 1 Part 10 has "A metric (conversion, orders) dropped after a launch. How would you investigate whether it is real, caused by the launch, or a data issue?"; this question is the dashboard-first version with no launch to blame.

**Example:** (illustrative numbers) DAU 1.00M, 0.98M, 0.90M. History says weekly wobble is about 0.8%, so -8.2% is about 10 sigma, not noise. By platform (million DAU, last week to this week): Android 0.44 to 0.37, iOS 0.40 to 0.40, Web 0.14 to 0.13. Android is 87.5% of the drop. Next query: Android by app version and by day. Weak answer: "Probably seasonality, let us wait a week." Strong answer: "The data is real, 88% of it is Android, I am checking Android versions and the start day, and a tracking break is my second hypothesis."

**Code:**
```python
# Q1: is the DAU drop real, and where is it? (illustrative numbers)
import numpy as np

two_weeks_ago, last_week, this_week = 1.00, 0.98, 0.90   # million DAU
wow = this_week / last_week - 1
vs2w = this_week / two_weeks_ago - 1
print(f"WoW change: {wow:.1%}   vs two weeks ago: {vs2w:.1%}")
assert round(wow, 3) == -0.082 and round(vs2w, 3) == -0.100

# Noise check: 8 earlier weeks of weekly DAU with ~1% natural wobble (seeded, illustrative)
rng = np.random.default_rng(7)
hist = 1.00 * (1 + rng.normal(0, 0.01, 8))
wow_hist = hist[1:] / hist[:-1] - 1
sd = wow_hist.std(ddof=1)
z = wow / sd
print(f"history WoW sd: {sd:.2%}   this week's z: {z:.1f}")
assert abs(z) > 3

# Decomposition by platform (million DAU)
seg = {"Android": (0.45, 0.44, 0.37), "iOS": (0.40, 0.40, 0.40), "Web": (0.15, 0.14, 0.13)}
tot_change = this_week - last_week
print(f"{'segment':8} {'last':>5} {'this':>5} {'delta':>6} {'share of drop':>14}")
for k, (a, b, c) in seg.items():
    d = c - b
    print(f"{k:8} {b:5.2f} {c:5.2f} {d:6.2f} {d / tot_change * 100 + 0.0:13.1f}%")
assert abs(sum(v[0] for v in seg.values()) - 1.00) < 1e-9
assert abs(sum(v[1] for v in seg.values()) - 0.98) < 1e-9
assert abs(sum(v[2] for v in seg.values()) - 0.90) < 1e-9
assert round((0.37 - 0.44) / tot_change, 3) == 0.875
```

**Output (my run):**
```text
WoW change: -8.2%   vs two weeks ago: -10.0%
history WoW sd: 0.79%   this week's z: -10.3
segment   last  this  delta  share of drop
Android   0.44  0.37  -0.07          87.5%
iOS       0.40  0.40   0.00           0.0%
Web       0.14  0.13  -0.01          12.5%
```

**Follow-ups:**
- Android is the culprit and the drop began on a Tuesday. Next? Line up the Tuesday with releases, OS updates and Play Store events, then compare crash rate and event volume per active user on the affected version.
- Everything checks out and the drop is real but spread evenly. Then it is likely behavioural or external: look at frequency (days per user), new-user inflow and the competitor or seasonal calendar.

**Common mistakes:** Starting with hypotheses instead of validation. Ranking segments by percent change. Using one comparison week. Forgetting a second data source. Not saying how you would stop.

### Q2 ⭐⭐⭐ 🟢 Success metrics for a new bill-splitting feature in a UPI payments app. The product team wants to know after four weeks whether it worked. Name the north star, two or three input metrics, and two guardrails, and say which one you would put in the launch review.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** I would pick "users with at least one settled split per week" as the north star, use the funnel steps as input metrics, guard core payment success and complaint rate, and bring the north star plus the repeat rate to the launch review.

**Clarifying questions:**
- What is the feature meant to do: drive more payments, bring new users through invites, or only improve satisfaction? Why: it sets the north star.
- What counts as "settled": the friend pays back inside the app, or any payment? Why: it is the difference between a real outcome and a request that went unanswered.
- Is there a holdout or a staged launch? Why: without a comparison group I cannot attribute anything to the feature.
- Who owns payment success and fraud? Why: they own the guardrails and the veto.
- Are invited friends counted as new users? Why: referral value needs separate treatment.

**Approach:**
1. Name the user value: a group expense gets settled with less friction. The north star must measure a completed settlement, not a tap.
2. North star: weekly users with at least one settled split / eligible users.
3. Input metrics (what the team can move): exposure rate (saw entry point / eligible), start rate (started / saw), settle rate (settled within 7 days / started), 4-week repeat (week-1 settlers who settle again in weeks 2-4 / week-1 settlers).
4. Guardrails: core UPI payment success rate, and complaints or spam reports per 100,000 collect requests. Add latency of the pay flow.
5. Compare treatment and holdout on the guardrails with a confidence interval, not a glance.
6. Launch review: show the north star and the repeat rate, with the guardrails as a pass or fail line.

**Metrics:**
- North star = users with a settled split in the week / eligible users.
- Settle rate = splits with at least one payback within 7 days / splits started.
- 4-week repeat = week-1 settlers with another settled split in weeks 2-4 / week-1 settlers.
- Guardrails: payment success = successful payments / attempted payments; complaints per 100,000 requests.

**Risks:**
- Counting split creations as success: a person can start many splits that nobody pays.
- Cannibalisation: splits may replace ordinary P2P payments, so total payments may not grow. Check payments per user, not just the feature.
- Novelty: week-1 use is high, week-4 is the truth.
- Spam: friends flooded with requests.

**What the interviewer scores:**
- Strong: a north star that is a completed outcome, inputs that decompose it, guardrails that name the real harm.
- Strong: picks one number for the launch review and says why.
- Weak: a list of ten metrics with no priority.
- Weak: taps, clicks or "feature users" as the north star.
- Cross-reference: Book 1 Part 10 has "How do you choose the primary metric, guardrail metrics and secondary metrics for an experiment? Give an example."; this answer applies the same rule to a launch.

**Example:** (illustrative numbers) 500,000 eligible users. 120,000 saw the entry point (24%), 30,000 started (25% of those who saw), 21,000 settled (70% of started). In week 4, 12,000 users settled a split, so the north star is 2.4%. Of 6,000 week-1 settlers, 2,100 settled again (35%). Payment success is 98.20% in the holdout and 98.15% in treatment, a -0.05pp gap with z = -1.87 (not significant at the 5% level, but I would keep watching). Complaints rose from 40 to 42 per 100,000 (+5%). Weak answer: "30,000 splits were created, great." Strong answer: "2.4% of users settle a split weekly and 35% repeat, guardrails hold."

**Code:**
```python
# Q2: bill-splitting feature, four-week read (illustrative numbers)
import math

eligible = 500_000          # active UPI users in the treatment group
saw_entry = 120_000         # saw the split entry point
started = 30_000            # started a split
settled = 21_000            # split where at least one friend paid back within 7 days
print(f"exposure {saw_entry/eligible:.0%}  start {started/saw_entry:.0%}  settle {settled/started:.0%}")
assert saw_entry / eligible == 0.24 and started / saw_entry == 0.25 and settled / started == 0.70

# north star: weekly users with a settled split, among eligible
week4_settlers = 12_000
print(f"north star (week 4 settled splitters / eligible): {week4_settlers/eligible:.1%}")
assert round(week4_settlers / eligible, 3) == 0.024

# input: repeat. week-1 settlers who settle another split in weeks 2-4
w1, w1_repeat = 6_000, 2_100
print(f"4-week repeat among week-1 settlers: {w1_repeat/w1:.0%}")
assert w1_repeat / w1 == 0.35

# guardrail: core UPI payment success, treatment vs holdout (same size)
n = 500_000
p_c, p_t = 0.9820, 0.9815
pool = (p_c + p_t) / 2
se = math.sqrt(pool * (1 - pool) * (2 / n))
z = (p_t - p_c) / se
print(f"payment success: holdout {p_c:.2%} treatment {p_t:.2%} diff {(p_t-p_c)*100:.2f}pp z={z:.2f}")
assert abs(z) < 1.96   # not a significant move

# guardrail: unwanted collect-request complaints per 100k requests
print(f"complaints per 100k requests: before 40 after 42 -> {42/40-1:.0%} relative")
assert round(42/40 - 1, 2) == 0.05
```

**Output (my run):**
```text
exposure 24%  start 25%  settle 70%
north star (week 4 settled splitters / eligible): 2.4%
4-week repeat among week-1 settlers: 35%
payment success: holdout 98.20% treatment 98.15% diff -0.05pp z=-1.87
complaints per 100k requests: before 40 after 42 -> 5% relative
```

**Follow-ups:**
- The north star is flat but splits are up. Probably cannibalised ordinary payments or one-time use; check payments per user and repeat rate.
- Why not use payment volume? It rewards big bills, not the number of settled groups, and it is easy to move with a few large splits.

**Common mistakes:** Counting starts as success. No holdout. Guardrails with no definition. Ten metrics and no choice. Forgetting that "not significant" on a guardrail is not "safe", only "not shown".

### Q3 ⭐⭐⭐ 🟢 Pick a north-star metric for a food-delivery app and defend it. Candidates the team floated are orders per week, GMV, weekly active ordering users and 4-week repeat rate. Choose one, add two guardrails, and say what each rejected candidate would hide.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** I would pick weekly active ordering users as the north star, guard it with the repeat share and an on-time delivery or cancellation rate, because it is the one candidate that is hard to inflate with a few heavy users or a big basket.

**Clarifying questions:**
- Is the company aiming for growth, profit or both this year? Why: a growth company leans to users, a profit-focused one adds margin per order.
- What is the business model (commission, delivery fee, ads)? Why: it decides whether GMV is even a good proxy for revenue.
- Is the goal frequency (existing users) or reach (new users)? Why: it decides between users and orders per user.
- How much of the order volume comes from discounts? Why: discounted users can inflate every candidate.
- Who will use the metric (a product team weekly, or the board)? Why: the metric has to move on the team's time scale.

**Approach:**
1. Define the user value: a hungry person gets food on time, and comes back. So the number should count people served, repeatedly.
2. Test each candidate for what it hides.
3. Choose weekly active ordering users (WAOU) = distinct users with at least one completed order in the week. It moves in weeks and is bounded by real people.
4. Add guardrails that stop WAOU being bought: repeat share (of this week's ordering users, the share who also ordered in the previous 3 weeks) and on-time delivery rate plus cancellation rate.
5. Review contribution margin per order alongside, so growth is not unprofitable.

**Metrics:**
- WAOU = distinct users with at least one delivered order in the week.
- Repeat share = ordering users this week who also ordered in the prior 3 weeks / ordering users this week. (My proxy; a cohort 4-week repeat rate is the standard version but lags by 4 weeks.)
- On-time rate = orders delivered within the promised time / delivered orders.
- Cancellation rate = cancelled orders / placed orders.

**Risks:**
- WAOU can be pumped by one-time promo users: that is why the repeat share sits beside it.
- Orders per week hides concentration: it can rise while users are flat.
- GMV rises with price, basket size and fees, with no more customers.
- Repeat rate alone is slow and ignores new users.

**What the interviewer scores:**
- Strong: chooses one, says what each rejected metric would hide, and gives a guardrail that targets the chosen metric's weakness.
- Strong: connects the metric to customer value and to a time scale a team can act on.
- Weak: "GMV, because it is revenue" with no thought for price effects.
- Weak: no guardrails, or guardrails unrelated to the north star's weakness.

**Example:** (illustrative numbers, 200 users, 4 weeks, Rs 300 per order, seeded) Baseline week 4: 153 orders, GMV Rs 45,900, 93 ordering users, repeat share 86.0%. World A (push heavy users from 2 to 3 orders): orders 213 and GMV Rs 63,900 jump about 39%, but ordering users stay 93. World B (40 one-time promo users): ordering users 133 (+43%), repeat share falls to 60.2%. So orders and GMV would celebrate World A where no new customer arrived, and WAOU alone would celebrate World B where the customers did not stay. Weak answer: "Orders per week, simple." Strong answer: "WAOU, with repeat share guarding against bought users."

**Code:**
```python
# Q3: how each north-star candidate behaves in two invented worlds (seeded)
import numpy as np

W = 4                      # weeks in window; week index 3 is "this week"
AOV = 300

def make_base():
    rng = np.random.default_rng(3)
    users = 200
    m = np.zeros((users, W), dtype=int)
    m[:60, :] = 2                                  # 60 loyal users: 2 orders every week
    casual = rng.random((140, W)) < 0.25           # 140 casual users: 25% chance per week
    m[60:, :] = casual.astype(int)
    return m

def metrics(m):
    last = m[:, 3]
    orders = int(last.sum())
    gmv = orders * AOV
    waou = int((last > 0).sum())
    active_last = last > 0
    prior = m[:, :3].sum(axis=1) > 0
    repeat_share = (active_last & prior).sum() / active_last.sum()
    return orders, gmv, waou, repeat_share

base = make_base()

heavy = base.copy()                  # world A: push heavy users harder
heavy[:60, 3] = 3

promo = np.vstack([base, np.zeros((40, W), dtype=int)])   # world B: 40 one-time promo users
promo[200:, 3] = 1

print(f"{'world':14} {'orders':>6} {'GMV':>7} {'WAOU':>5} {'repeat share':>13}")
res = {}
for name, m in [("baseline", base), ("A heavy push", heavy), ("B promo users", promo)]:
    res[name] = metrics(m)
    o, g, w, r = res[name]
    print(f"{name:14} {o:6d} {g:7d} {w:5d} {r:13.1%}")

b, a, p = res["baseline"], res["A heavy push"], res["B promo users"]
assert a[0] > b[0] and a[1] > b[1]            # orders and GMV rise in A
assert a[2] == b[2]                            # users did not change in A
assert p[2] > b[2]                             # WAOU rises in B
assert p[3] < b[3]                             # but repeat share falls in B
print("A: orders and GMV up, users flat.  B: users up, repeat share down.")
```

**Output (my run):**
```text
world          orders     GMV  WAOU  repeat share
baseline          153   45900    93         86.0%
A heavy push      213   63900    93         86.0%
B promo users     193   57900   133         60.2%
A: orders and GMV up, users flat.  B: users up, repeat share down.
```

**Follow-ups:**
- Why not 4-week repeat rate as the north star? It is the best measure of loyalty but it lags a month, so a team cannot steer with it; keep it as the guardrail and the quarterly health check.
- What would make you change the choice? A mature market where growth is frequency: then orders per active user or margin per user may deserve to lead.

**Common mistakes:** Choosing GMV and ignoring price and fees. Choosing a metric with no guardrail. Counting orders placed rather than delivered. Defending the metric with "everyone uses it".

### Q4 ⭐⭐⭐ 🟢 The DAU to MAU ratio (stickiness) fell from 0.30 to 0.26 while MAU stayed flat at 20 million. Explain what this tells you that a DAU or MAU chart alone would not, and list the three or four hypotheses you would test first.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** DAU/MAU is average active days divided by the days in the window, so it tells you about how often people come back; MAU flat with the ratio down means the same-sized audience visits less, or the audience quietly changed.

**Clarifying questions:**
- Is MAU a rolling 30-day or a calendar month? Why: a rolling window and a calendar month give different ratios and different seasonality.
- Is the DAU a monthly average or one day? Why: a single weekday can move the ratio a lot.
- Did the definition of "active" change for either DAU or MAU? Why: if only one of them changed, the ratio moves with no behaviour change.
- Was there a big acquisition push or a reactivation campaign? Why: it adds MAU users who come once.
- Which platforms and countries moved? Why: it points to a release or a market cause.

**Approach:**
1. Translate: DAU = ratio x MAU = 0.26 x 20M = 5.2M, down from 6.0M, so DAU fell 13.3% while MAU is flat.
2. Say what the ratio tells you: it is a frequency measure. DAU alone could be a size change, MAU alone hides frequency.
3. Hypotheses to test, in order:
   - H1: everyone visits a bit less (engagement or habit loss).
   - H2: low-intent users replaced loyal ones (paid installs, bot traffic, one-off reactivations) so MAU is held up by one-visit users.
   - H3: a definition or tracking change hit DAU but not MAU, or the reverse.
   - H4: a calendar effect (fewer weekend days, a holiday, a cricket season).
4. One cut separates H1 from H2: the distribution of active days per user, split by cohort age and channel. H1 shifts the whole distribution; H2 adds a spike at one day.
5. Check the event pipeline for H3 and the calendar for H4.

**Metrics:**
- Stickiness = average DAU over the window / MAU for the same window.
- Active days per MAU user = sum of active days across users / MAU. Since DAU = (sum of active days) / days in window, ratio = (active days per MAU user) / days.
- Share of one-day users = MAU users active on exactly one day / MAU.
- Guardrail: new-user share of MAU, and retention by cohort.

**Risks:**
- Reading the ratio alone: two different stories give the same value.
- A rolling MAU lags a change in DAU, so the ratio can drift for weeks.
- A weekend-heavy month makes the ratio look worse.
- Mixing a daily DAU with a monthly MAU (different windows).

**What the interviewer scores:**
- Strong: explains what the ratio adds (frequency) and shows two stories with the same ratio.
- Strong: names the cut that separates the hypotheses.
- Weak: "stickiness fell, so engagement fell" with no alternative.
- Weak: ignores definition and calendar checks.

**Example:** (illustrative numbers) MAU 20M, 30-day window. Before: average 9.0 active days per user gives DAU = 20 x 9 / 30 = 6.0M (ratio 0.30). H1: everyone visits 7.8 days, DAU = 5.2M (0.26). H2: 3M loyal users (9 days each) are replaced by 3M one-visit users; DAU = (17 x 9 + 3 x 1) / 30 = 5.2M (0.26). Same DAU, same MAU, same ratio, very different fixes. Weak answer: "People are less engaged." Strong answer: "Either frequency fell or low-intent users diluted MAU; the active-days distribution by channel will tell me which."

**Code:**
```python
# Q4: DAU/MAU 0.30 -> 0.26 with MAU flat at 20M (illustrative)
mau = 20.0                       # million
dau_before, dau_after = 0.30 * mau, 0.26 * mau
print(f"DAU before {dau_before:.1f}M after {dau_after:.1f}M change {dau_after/dau_before-1:.1%}")
assert round(dau_before, 1) == 6.0 and round(dau_after, 1) == 5.2

days = 30
# DAU = sum over users of active days / days in window
before_avg_days = 9.0
print(f"before: avg active days per MAU = {before_avg_days} -> DAU {mau*before_avg_days/days:.2f}M")
assert abs(mau * before_avg_days / days - 6.0) < 1e-9

# H1: everyone is a bit less frequent
h1_days = 7.8
dau_h1 = mau * h1_days / days
print(f"H1 less frequent: avg days {h1_days} -> DAU {dau_h1:.2f}M, stickiness {dau_h1/mau:.2f}")
assert abs(dau_h1 - 5.2) < 1e-9

# H2: 3M core users left, 3M one-visit users arrived (paid installs, bots, reactivations)
core, junk = 17.0, 3.0
dau_h2 = (core * 9.0 + junk * 1.0) / days
print(f"H2 low-intent mix: MAU {core+junk:.0f}M, DAU {dau_h2:.2f}M, stickiness {dau_h2/(core+junk):.2f}")
assert abs(dau_h2 - 5.2) < 1e-9 and core + junk == mau
print("Same DAU, same MAU, same ratio: the ratio alone cannot tell H1 from H2.")
print("Cut: distribution of active days per user, by cohort age and channel.")
```

**Output (my run):**
```text
DAU before 6.0M after 5.2M change -13.3%
before: avg active days per MAU = 9.0 -> DAU 6.00M
H1 less frequent: avg days 7.8 -> DAU 5.20M, stickiness 0.26
H2 low-intent mix: MAU 20M, DAU 5.20M, stickiness 0.26
Same DAU, same MAU, same ratio: the ratio alone cannot tell H1 from H2.
Cut: distribution of active days per user, by cohort age and channel.
```

**Follow-ups:**
- Why not just track DAU? DAU does not show whether a drop is a smaller audience or a less frequent one.
- A product manager wants to "improve stickiness". Where would you aim? At the habit loop for existing users (reminders, content freshness); buying more MAU lowers the ratio.

**Common mistakes:** Treating the ratio as proof of engagement loss. Comparing a rolling-window ratio to a calendar-month one. Forgetting that adding casual users lowers stickiness without harming the business. Not asking about the definitions.

### Q5 ⭐⭐⭐ 🟢 Weekly orders on an e-commerce app fell 20% in the week after a big sale ended, compared with the sale week. Leadership asks if this is a problem. Explain how you would tell a normal post-sale hangover from a real decline, and which baselines you would compare against.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
**Say this first (1 line):** A drop right after a sale is expected, so I compare to a sale-adjusted baseline, last year's post-sale shape and the next two or three weeks, and call it a decline only if orders fall below the pre-sale trend and stay there.

**Clarifying questions:**
- How big was the sale lift and how long was the sale? Why: a big lift means a big pull-forward and a bigger hangover.
- What do last year's and last quarter's post-sale weeks look like? Why: it is the cleanest baseline for the same event.
- Did new-user acquisition, delivery speed or stock-outs change this week? Why: they would mean a real problem hiding behind the hangover.
- Are we measuring orders placed or delivered? Why: returns and cancellations after a sale change the delivered count.
- What is leadership's concern: volume, profit or customer loyalty? Why: it sets what "a problem" means.

**Approach:**
1. Say the obvious: comparing with the sale week is the wrong baseline, since the sale week was the peak.
2. Use three baselines. (a) Pre-sale average: the level normal weeks sit at. (b) Last year's same event: the usual size of the drop. (c) Trend minus an estimate of pull-forward (demand brought into the sale week).
3. Look at weeks 2 and 3: a hangover recovers to the baseline within a few weeks; a decline stays below.
4. Segment: new versus existing buyers, categories, cities. A decline hides in a segment (for example repeat buyers down) while the total looks fine.
5. Check supply and service: stock-outs, delivery times, ratings.
6. Conclude with a rule: if orders return to within a few percent of the trend by week 3, it is a hangover; if not, investigate.

**Metrics:**
- Post-sale change vs sale week = post / sale - 1 (not decision-useful, shown only because leadership quotes it).
- Post-sale vs pre-sale = post / pre-sale average - 1.
- Excess over expectation = actual - (trend - estimated pull-forward share).
- Guardrails: repeat-buyer orders, delivery time, cancellation rate.

**Risks:**
- Comparing to the peak week.
- Assuming the pull-forward share without testing it; it is a guess to be checked against last year.
- A week-1 recovery can hide a fall in repeat buyers.
- Calendar shifts (festival dates move each year).

**What the interviewer scores:**
- Strong: rejects the sale-week baseline, offers more than one baseline, and names the recovery pattern that separates hangover from decline.
- Strong: splits new versus repeat buyers.
- Weak: says "20% down is alarming" or "it is just seasonal" with no baseline.
- Weak: no time horizon for the decision.

**Example:** (illustrative numbers, thousands of orders) Pre-sale weeks 100, 101, 102; sale week 150; post-sale weeks 120, 108, 103. Post-sale vs sale week is -20%, but vs the pre-sale average of 101 it is +18.8%. Last year the same drop was -22%, so this year is slightly better. Assume 20% of the sale's 47k excess (150 - 103 trend) was pulled forward: 9.4k, spread over three weeks, so expected weeks are 99.9, 100.9 and 101.9; actual minus expected is +20.1, +7.1 and +1.1. By week 3 orders are back at the baseline. It is a normal hangover. Weak answer: "Orders fell 20%, escalate." Strong answer: "Against any sensible baseline we are fine; I will recheck in two weeks and look at repeat buyers."

**Code:**
```python
# Q5: post-sale week, three baselines (illustrative orders per week, thousands)
pre_sale = [100, 101, 102]            # three normal weeks before the sale
sale_week = 150
post_weeks = [120, 108, 103]          # post-sale week 1, 2, 3
print(f"post-sale week vs sale week: {post_weeks[0]/sale_week-1:.0%}")
assert round(post_weeks[0] / sale_week - 1, 2) == -0.20

pre_avg = sum(pre_sale) / 3
print(f"pre-sale average {pre_avg:.1f}; post-sale week 1 vs pre-sale: {post_weeks[0]/pre_avg-1:+.1%}")
assert round(pre_avg, 1) == 101.0

# baseline 2: same event last year, same shape
ly_sale, ly_post1 = 100, 78
print(f"last year post-sale vs sale week: {ly_post1/ly_sale-1:.0%}")
assert round(ly_post1 / ly_sale - 1, 2) == -0.22

# baseline 3: trend plus pull-forward.
# extra sale-week orders over trend = 150 - 103 = 47. Assume 20% of that was pulled from the next 3 weeks.
trend = [103, 104, 105]
pulled = 0.20 * (sale_week - 103)
expected = [t - pulled / 3 for t in trend]
print(f"pull-forward estimate {pulled:.1f}k over 3 weeks; expected weeks {[round(e,1) for e in expected]}")
print(f"actual  {post_weeks}")
gap = [a - e for a, e in zip(post_weeks, expected)]
print(f"actual minus expected: {[round(g,1) for g in gap]}")
assert round(pulled, 1) == 9.4
assert all(g > 0 for g in gap)          # no shortfall versus expectation: a normal hangover
# a real decline would look like actual falling BELOW pre-sale level and staying there
print("weeks 2-3 settle back to pre-sale level (108, 103 vs 101): hangover, not decline")
```

**Output (my run):**
```text
post-sale week vs sale week: -20%
pre-sale average 101.0; post-sale week 1 vs pre-sale: +18.8%
last year post-sale vs sale week: -22%
pull-forward estimate 9.4k over 3 weeks; expected weeks [99.9, 100.9, 101.9]
actual  [120, 108, 103]
actual minus expected: [20.1, 7.1, 1.1]
weeks 2-3 settle back to pre-sale level (108, 103 vs 101): hangover, not decline
```

**Follow-ups:**
- What would make you say it is a real decline? Week 3 actual below the trend minus pull-forward, or repeat-buyer orders falling while new buyers rise.
- How do you pick the pull-forward share? Calibrate it on last year's sale: the dip below trend in the three weeks after, divided by the sale excess.

**Common mistakes:** Comparing to the peak. One baseline only. Reporting week 1 as the conclusion. Ignoring that a deep discount can train customers to wait for the next sale.

### Q6 ⭐⭐⭐ 🟡 Checkout conversion dropped from 3.1% to 2.6% and the drop appears only on Android, starting the day version 8.4 shipped, while the crash rate is flat. Describe how you would narrow the cause, what you would compare by app version, and how you would decide between a product bug and a measurement bug.
**Asked at:** Funnel and checkout-conversion case pages (a Prachub Amazon checkout-conversion root-cause page, funnel guides from Amplitude, Hackle and Datadog); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I narrow it by version, step and source: if the backend order table also fell on 8.4, it is a product bug; if only the app event fell, it is a measurement bug.

**Clarifying questions:**
- Is 3.1% to 2.6% the Android number or the blended number? Why: if it is blended with iOS flat, Android fell by more than half a point.
- What is the denominator: sessions that reached the cart, or all sessions? Why: a denominator change alone can move conversion.
- Which funnel step moved (cart to address, address to payment, payment to confirmation)? Why: it tells you which screen to look at.
- Is there a server-side order count (payment gateway, order table)? Why: it is the independent check on the event.
- Did 8.4 change checkout code, the SDK or event names? Why: it points at the likely bug.

**Approach:**
1. Check it is real: two-proportion test on the Android before/after (with 400,000 cart sessions each side, a drop from 3.1% to 2.6% is about z = -13).
2. Split Android by app version: 8.3 versus 8.4. If 8.3 users are unchanged on the same days, it is version-specific.
3. Compare the backend order count and the client event count, per version, per day.
4. If both fell: product bug. Walk the funnel step by step by version; check payment success rate, errors, load time, a button that is hidden on some screens.
5. If only the event fell: measurement bug. Check the event fire rate per version and a sample of session replays or logs.
6. Decide using a rule: backend flat and event down = tracking; both down = product. Then roll back, hotfix or fix the event, and report with the corrected number.

**Metrics:**
- Conversion = orders / cart sessions, by app version and OS.
- Event capture ratio = client events / backend orders (expected near 1; a drop on one version is the tracking tell).
- Step conversion = users at step k+1 / users at step k.
- Guardrails: payment success rate, crash rate, API error rate, checkout latency.

**Risks:**
- Crash rate flat does not mean the screen works: a button can be hidden without crashing.
- Version adoption mixes in different user types: early adopters of 8.4 may behave differently. Compare same days and same user groups.
- The two-proportion p-value is tiny with 400,000 sessions; look at size and a segment-level story, not the p-value.

**What the interviewer scores:**
- Strong: separates product bug from measurement bug with a concrete independent source (backend orders).
- Strong: asks about the version cut and the step cut before theories.
- Weak: blames "users" or seasonality when the drop is only on one version and platform.
- Weak: says "check the logs" with no decision rule.
- Cross-reference: Book 1 Part 10 has "A metric (conversion, orders) dropped after a launch. How would you investigate whether it is real, caused by the launch, or a data issue?"

**Example:** (illustrative numbers, per 100,000 v8.4 cart sessions) Product-bug world: event orders 2,600 and backend orders 2,600, conversion 2.6% in both. Measurement-bug world: event orders 2,600 but backend orders 3,100, so event conversion is 2.6% and true conversion is 3.1%. If Android is 60% of cart sessions and iOS stays at 3.1%, Android at 2.6% gives a blended 2.80%. Weak answer: "Roll back 8.4." Strong answer: "First compare backend orders for 8.4; rolling back a tracking bug fixes nothing."

**Code:**
```python
# Q6: Android conversion drop, product bug or measurement bug? (illustrative)
import math

def z_two_prop(p1, n1, p2, n2):
    pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    return (p2 - p1) / se

n = 400_000   # Android cart sessions per period
z = z_two_prop(0.031, n, 0.026, n)
print(f"Android conversion 3.1% -> 2.6%, n={n:,} each: z = {z:.1f}")
assert abs(z) > 10

# blended number if iOS stays 3.1% and Android is 60% of cart sessions
blended = 0.6 * 0.026 + 0.4 * 0.031
print(f"blended conversion with Android at 2.6%: {blended:.2%}")
assert round(blended, 4) == 0.0280

# Two worlds on v8.4 (per 100,000 cart sessions); backend = payment-gateway/order table
sessions = 100_000
worlds = {
    "product bug (button hard to tap)": dict(backend_orders=2600, event_orders=2600),
    "measurement bug (event not fired)": dict(backend_orders=3100, event_orders=2600),
}
print(f"{'world':36} {'event conv':>11} {'backend conv':>13}")
for name, w in worlds.items():
    print(f"{name:36} {w['event_orders']/sessions:11.1%} {w['backend_orders']/sessions:13.1%}")
prod, meas = worlds.values()
assert prod["event_orders"] == prod["backend_orders"]
assert meas["backend_orders"] / sessions == 0.031 and meas["event_orders"] / sessions == 0.026
print("Rule: event and backend both fall = product problem; only event falls = tracking problem.")
```

**Output (my run):**
```text
Android conversion 3.1% -> 2.6%, n=400,000 each: z = -13.4
blended conversion with Android at 2.6%: 2.80%
world                                 event conv  backend conv
product bug (button hard to tap)            2.6%          2.6%
measurement bug (event not fired)           2.6%          3.1%
Rule: event and backend both fall = product problem; only event falls = tracking problem.
```

**Follow-ups:**
- The backend order count is also down, but only for one payment method. Product bug in that payment path: check the gateway integration and error codes on 8.4.
- How would you protect against this next time? Alert on event capture ratio per version and add a release check that compares client events with server orders.

**Common mistakes:** Rolling back before checking the backend. Treating flat crash rate as "no bug". Mixing up the blended and Android numbers. Using only a p-value to call it real.

### Q7 ⭐⭐⭐ 🟡 DAU rose 5% after a feature launch but total time spent per day fell 8%. A PM calls it a win because the headline is DAU. Explain how both can be true, what additional cuts you would run, and how you would decide whether this is good or bad for the product.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Both can be true if the new DAU are light users or existing users now finish faster, so I split the change by existing and new users and ask whether the time lost was wasted time or value.

**Clarifying questions:**
- Is "time spent" total minutes per day or minutes per active user? Why: they are different numbers and the answer depends on it.
- What does the feature do (a shortcut, a new content type, a notification)? Why: a shortcut should lower time and a content feature should raise it.
- Who are the extra DAU: new, returning or existing users moving their visit time? Why: it decides whether this is growth or cannibalisation.
- What does the product earn on (time, orders, ads, subscriptions)? Why: time is only good if it earns.
- Is there a holdout? Why: before/after comparisons mix the launch with other changes.

**Approach:**
1. Show how it can happen: total = DAU x average time per DAU. DAU +5% and total -8% means average time per DAU fell about 12.4%.
2. Cut: existing versus new DAU; time per DAU by segment; the heavy-user decile (are our best users spending less?).
3. Check what the time bought: task success, orders, content completed, return rate over the next 7 and 28 days.
4. Decide with the product's value metric, not with the headline: if the feature made tasks faster and orders or retention are up, lower time is good; if the heavy users are leaving, it is bad.
5. If unsure, keep a holdout and wait for the 4-week retention read.

**Metrics:**
- Total time per day = sum of minutes across all users that day.
- Average time per DAU = total time / DAU.
- Time change decomposition = existing users x change in their time + new users x their time.
- Guardrails: orders (or the value event) per DAU, D7 and D28 retention of the new users, heavy-user share.

**Risks:**
- The extra DAU may be accidental visits (a notification opens the app and the user leaves).
- Time can fall because of a bug or faster pages; that is not a loss of interest.
- Averages hide the heavy tail: a 10% drop among the top decile can cost more value than the new light users add.
- The headline metric is the PM's, which creates a conflict of interest to handle tactfully.

**What the interviewer scores:**
- Strong: writes total = DAU x average time and shows the arithmetic, then splits existing versus new.
- Strong: judges by the product's value metric and retention, not by DAU or time alone.
- Weak: "DAU is the goal, so it is good" or "time fell, so it is bad".
- Weak: no cuts offered.
- Cross-reference: Book 1 Part 10 has "The test shows the primary metric up but revenue (or a guardrail) down or flat. How do you interpret and decide?"

**Example:** (illustrative numbers) Before: 1,000,000 DAU at 30 minutes is 30.0M minutes. After: existing users 1,000,000 at 27 minutes (27.0M) plus 50,000 new users at 12 minutes (0.6M) is 27.6M minutes. DAU is +5.0%, total time is -8.0%, and average per DAU is 26.29 minutes (-12.4%). Existing users lost 3.0M minutes and new users added 0.6M. The whole loss is in the existing base. Weak answer: "DAU is the goal, ship it." Strong answer: "Existing users spend 10% less, I need to know if they got what they wanted faster or stopped enjoying it."

**Code:**
```python
# Q7: DAU +5% but total time -8% (illustrative, minutes per day)
before_dau, before_min = 1_000_000, 30.0
total_before = before_dau * before_min
print(f"before: DAU {before_dau:,}, avg {before_min} min, total {total_before/1e6:.1f}M min")

existing_dau, existing_min = 1_000_000, 27.0     # existing users spend a bit less
new_dau, new_min = 50_000, 12.0                  # new/returning light users
dau_after = existing_dau + new_dau
total_after = existing_dau * existing_min + new_dau * new_min
print(f"after:  DAU {dau_after:,}, total {total_after/1e6:.1f}M min")
print(f"DAU {dau_after/before_dau-1:+.1%}, total time {total_after/total_before-1:+.1%}, "
      f"avg per DAU {total_after/dau_after:.2f} min ({total_after/dau_after/before_min-1:+.1%})")
assert round(dau_after / before_dau - 1, 4) == 0.05
assert round(total_after / total_before - 1, 3) == -0.08
assert round(total_after / dau_after, 2) == 26.29

# split of the change in total time
effect_existing = existing_dau * (existing_min - before_min)
effect_new = new_dau * new_min
print(f"existing users: {effect_existing/1e6:+.1f}M min; new users: {effect_new/1e6:+.1f}M min")
assert effect_existing == -3_000_000 and effect_new == 600_000
print("The whole loss sits in existing users; the new users add a little.")
```

**Output (my run):**
```text
before: DAU 1,000,000, avg 30.0 min, total 30.0M min
after:  DAU 1,050,000, total 27.6M min
DAU +5.0%, total time -8.0%, avg per DAU 26.29 min (-12.4%)
existing users: -3.0M min; new users: +0.6M min
The whole loss sits in existing users; the new users add a little.
```

**Follow-ups:**
- Time spent is down because the feature is a search shortcut. Is that bad? Not if task success and orders per session rise; judge by outcome per minute.
- How do you decide without waiting months? Compare retention and value events in the first 7 and 14 days for the new and the existing users separately.

**Common mistakes:** Using DAU as the only judge. Mixing total and per-user time. Not splitting existing and new users. Calling lower time bad without asking what the user achieved.

### Q8 ⭐⭐⭐ 🟡 A notification experiment sends more pushes to the treatment group: sessions per user rise 6% and DAU rises 2%, but 30-day uninstalls rise from 1.2% to 1.5% and notification opt-outs double. Decide whether to ship, which metric is the goal and which is the guardrail, and what extra analysis you want.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would not ship it as is: a 2% DAU gain bought with more uninstalls and doubled opt-outs destroys reach permanently, so I want a frequency-capped variant and a longer retention read.

**Clarifying questions:**
- What is the goal metric of the team: DAU, retention or revenue? Why: it sets the goal versus guardrail split.
- How long did the experiment run and is the 30-day uninstall read complete? Why: uninstalls and opt-outs show up with a delay.
- What is the sample size per arm? Why: it tells me whether 1.2% to 1.5% is noise (it is not at 200,000 per arm).
- What are opt-outs of: all pushes or only this category? Why: a lost channel affects every future campaign.
- Is there a cap on pushes per day in the treatment? Why: the dose is the lever I can change.

**Approach:**
1. Goal metric: DAU (or better, 28-day active days per user). Guardrails: 30-day uninstall rate and push opt-out rate. Sessions per user is secondary.
2. Test the guardrail properly: uninstall rate 1.2% versus 1.5% with 200,000 users per arm is +0.30pp (95% interval 0.23 to 0.37pp), z about 8. This is a real harm, not noise.
3. Net it out: do the extra sessions and DAU last longer than the lost users cost? If the uninstall hazard repeats monthly and the 2% lift stays, DAU in treatment falls below control by month 7.
4. Cut by segment: heavy versus light users, new versus old, by push frequency received. Often heavy users like it and light users uninstall.
5. Look for the dose-response: test a cap (for example 2 pushes a day) or smarter targeting.
6. Recommend: do not ship the current arm; run the capped variant for at least 4 to 6 weeks and compare 28-day retention.

**Metrics:**
- DAU = distinct users with a qualifying action per day (goal).
- 30-day uninstall rate = users who uninstalled within 30 days of assignment / users assigned (guardrail).
- Opt-out rate = users who turned off notifications / users assigned (guardrail).
- Sessions per user = sessions / users (secondary; it can rise from push-driven opens that do not matter).
- Net reach = users with push enabled and app installed / users assigned.

**Risks:**
- Novelty: the 2% DAU lift may fade while the uninstalls remain.
- Opt-outs are hard to reverse and also hurt future sends.
- Averaging over users hides segments that are hurt.
- A short test only sees the first 30 days.

**What the interviewer scores:**
- Strong: names DAU as the goal and uninstalls and opt-outs as guardrails, tests the guardrail statistically, and proposes the net effect over time.
- Strong: suggests a modified variant, not just a yes or no.
- Weak: "DAU is up, ship it" or "uninstalls are up, kill it" with no numbers.
- Weak: ignores that opt-outs reduce every future campaign.
- Cross-reference: Book 1 Part 10 has "The test shows the primary metric up but revenue (or a guardrail) down or flat. How do you interpret and decide?"

**Example:** (illustrative numbers) 200,000 users per arm. Uninstalls 1.2% versus 1.5%: 600 extra uninstalls per arm, 95% interval 0.23 to 0.37pp, z = 8.2. Treat the 2% DAU lift as constant and the monthly uninstall gap as repeating: the DAU index (treatment / control) is 1.0169 at month 1, 1.0107 at month 3, 1.0016 at month 6 and 0.9985 at month 7. The lift is gone by month 7. Weak answer: "Ship, DAU is the goal." Strong answer: "The guardrail breach is real and the lift decays against it; I want a capped variant."

**Code:**
```python
# Q8: notification experiment (illustrative numbers)
import math

n = 200_000  # users per arm
p_c, p_t = 0.012, 0.015
pool = (p_c + p_t) / 2
se = math.sqrt(pool * (1 - pool) * 2 / n)
z = (p_t - p_c) / se
diff = p_t - p_c
ci = (diff - 1.96 * se, diff + 1.96 * se)
print(f"uninstalls 30d: {p_c:.1%} vs {p_t:.1%}; diff {diff*100:.2f}pp CI [{ci[0]*100:.2f}, {ci[1]*100:.2f}] z={z:.1f}")
assert z > 4 and ci[0] > 0
extra = diff * n
print(f"extra uninstalls per arm of {n:,}: {extra:.0f}")
assert round(extra) == 600

# Does a 2% DAU lift survive the uninstalls? Monthly uninstall hazard as measured, lift held constant.
lift = 0.02
print("month  DAU index (treatment / control)")
cross = None
for m in range(1, 13):
    idx = (1 + lift) * ((1 - p_t) / (1 - p_c)) ** m
    print(f"{m:5d}  {idx:.4f}")
    if cross is None and idx < 1:
        cross = m
print(f"crossover month: {cross}")
assert cross == 7
print("Assumes the lift stays 2% and the uninstall rate repeats monthly: both are things to measure.")
```

**Output (my run):**
```text
uninstalls 30d: 1.2% vs 1.5%; diff 0.30pp CI [0.23, 0.37] z=8.2
extra uninstalls per arm of 200,000: 600
month  DAU index (treatment / control)
    1  1.0169
    2  1.0138
    3  1.0107
    4  1.0077
    5  1.0046
    6  1.0016
    7  0.9985
    8  0.9955
    9  0.9925
   10  0.9894
   11  0.9864
   12  0.9834
crossover month: 7
Assumes the lift stays 2% and the uninstall rate repeats monthly: both are things to measure.
```

**Follow-ups:**
- What if the business insists on shipping? Ship to light-touch segments only, keep a holdout, and set a rollback trigger on opt-outs.
- Why not just use sessions? Sessions can rise when pushes pull users in for a second and out again; DAU and retention are closer to value.

**Common mistakes:** Treating the lift and the harm as comparable without a time horizon. Skipping the significance test on the guardrail. Forgetting opt-outs reduce future reach. Choosing ship or kill with no middle option.

### Q9 ⭐⭐⭐ 🟡 Day-7 retention for the last three weekly signup cohorts is 18%, 17% and 14%, versus a steady 20% earlier. Explain how you would separate a true product regression from a change in who is signing up, and which cohort cuts you would build.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** I check who signed up before I blame the product: I recompute the last three cohorts at the old signup mix, and if retention is back near 20% it is a mix change, if not it is a regression inside segments.

**Clarifying questions:**
- Did marketing spend, channels, geographies or the signup flow change in the last three weeks? Why: those change who arrives.
- Did the app release, onboarding or notifications change in the same weeks? Why: those change what arrived users experience.
- How is Day-7 retention defined (active on day 7 exactly, or on or after day 7)? Why: a definition or logging change moves it with no behaviour change.
- How large are the cohorts? Why: with small cohorts the 18, 17, 14 could be noise.
- Is there a Day-1 or Day-3 retention for the same cohorts? Why: it shows where the loss starts.

**Approach:**
1. Check that the decline is not noise: with about 10,000 signups per cohort, a 14% vs 20% gap is far outside sampling error.
2. Build cohort cuts: acquisition channel, platform and OS, country or city, app version, signup source (organic, referral, paid), device price band, signup weekday.
3. Standardise: recompute each recent cohort's retention using the old mix weights (direct standardisation). If the standardised number is about 20%, mix explains it.
4. Split the gap: total change = within-segment change + mix change.
5. If the within-segment part is large, look for a product cause: a release that week, onboarding step completion, early activation (first key action in day 1), crash rate.
6. Use Day-1 and Day-3 curves to see how early the loss starts. A flow break shows at Day 1; a weaker habit shows later.

**Metrics:**
- Day-7 retention = users in the signup cohort active on day 7 / users in the cohort.
- Standardised retention = sum over segments of (old mix share x segment retention in the new cohort).
- Mix effect = blended retention minus standardised retention.
- Guardrails: activation rate (first key action within 24 hours), cohort size by channel.

**Risks:**
- A segment cut can itself hide a mix shift one level down (Simpson-type effects).
- Cohorts that are too small make the trend a noise story.
- Retention by cohort age is immature for the newest week: be sure all cohorts have a full 7 days.
- Changing the retention definition during the window.

**What the interviewer scores:**
- Strong: names mix versus regression, uses standardisation, and says how to split the gap.
- Strong: asks about definition and cohort age.
- Weak: "retention is down, let us improve onboarding."
- Weak: no segmentation plan.
- Cross-reference: Book 1 Part 10 has "What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment."; this is the same trap met in a cohort chart.

**Example:** (illustrative numbers) Organic users retain 30% and paid users 10% at Day 7. The old mix is 50% organic: 0.5 x 30 + 0.5 x 10 = 20%. Recent cohorts have organic shares of 40%, 35% and 20%, which gives 18%, 17% and 14%, exactly the numbers in the question, with no change in either channel. Standardised to the old mix, the last cohort is 20.0%: mix explains all of it. In a regression world where organic fell to 26% and paid to 8.5% on the same 20% organic mix, blended retention is 12.0%, standardised retention is 17.2%, and the total fall of 8.0 points splits into 2.75 within-channel and 5.25 mix. Weak answer: "Fix onboarding." Strong answer: "Standardise to the old mix first; it separates what changed in who came from what changed in the product."

**Code:**
```python
# Q9: mix change or regression? D7 retention by channel (illustrative)
ret_organic, ret_paid = 0.30, 0.10
cohorts = {"old (typical)": 0.50, "W1": 0.40, "W2": 0.35, "W3": 0.20}   # organic share of signups
size = 10_000
print(f"{'cohort':14} {'organic':>8} {'paid':>6} {'blended D7':>11}")
blend = {}
for k, s in cohorts.items():
    blend[k] = s * ret_organic + (1 - s) * ret_paid
    print(f"{k:14} {s:8.0%} {1-s:6.0%} {blend[k]:11.1%}")
assert [round(blend[k], 3) for k in ["old (typical)", "W1", "W2", "W3"]] == [0.20, 0.18, 0.17, 0.14]

# Standardise to the old mix: within-channel retention weighted by 50/50
std = 0.5 * ret_organic + 0.5 * ret_paid
print(f"W3 standardised to old mix: {std:.1%}  (unchanged -> mix explains the whole drop)")
assert round(std, 3) == 0.20

# Regression world: same W3 mix, but each channel got worse
reg_org, reg_paid = 0.26, 0.085
reg_blend = 0.20 * reg_org + 0.80 * reg_paid
reg_std = 0.5 * reg_org + 0.5 * reg_paid
print(f"regression world W3: blended {reg_blend:.1%}, standardised {reg_std:.1%}")
assert round(reg_blend, 3) == 0.120 and round(reg_std, 4) == 0.1725
print(f"total fall {reg_blend - 0.20:+.2%}: within-channel {reg_std - 0.20:+.2%}, mix {reg_blend - reg_std:+.2%}")

# Noise check: is 14% vs 20% outside sampling error for n=10,000 signups?
se = (0.17 * 0.83 / size) ** 0.5
print(f"standard error of a ~17% rate with n={size:,}: {se:.2%}; the 6-point gap is about {0.06/se:.0f} se")
assert 0.06 / se > 10
```

**Output (my run):**
```text
cohort          organic   paid  blended D7
old (typical)       50%    50%       20.0%
W1                  40%    60%       18.0%
W2                  35%    65%       17.0%
W3                  20%    80%       14.0%
W3 standardised to old mix: 20.0%  (unchanged -> mix explains the whole drop)
regression world W3: blended 12.0%, standardised 17.2%
total fall -8.00%: within-channel -2.75%, mix -5.25%
standard error of a ~17% rate with n=10,000: 0.38%; the 6-point gap is about 16 se
```

**Follow-ups:**
- What if the mix shift is the result of a deliberate paid push? Then report retention by channel, and judge paid acquisition on payback, not on blended retention.
- How would you check an onboarding regression quickly? Compare step completion by version and the Day-1 activation rate, since a flow break appears there first.

**Common mistakes:** Reporting only blended retention. Skipping a standardisation step. Comparing a cohort without a full 7 days to older ones. Treating the mix effect as "not a real problem" when the paid users are poor value.

### Q10 ⭐⭐⭐ 🟡 Average order value on a grocery app fell 15% quarter over quarter, from Rs 520 to about Rs 442, while order count rose 9%. Is this bad? Show how you would decompose the change and decide which part, if any, needs action.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
**Say this first (1 line):** AOV down 15% with orders up 9% is not automatically good or bad: GMV is down 7.4%, so I split the AOV change into a within-segment part and a mix part and act only on the part that hurts.

**Clarifying questions:**
- Is order count up because of new users, more frequency from existing users, or a promo? Why: it tells me whether the mix part is healthy growth.
- Did prices, coupons, delivery fees or minimum order values change? Why: they act directly on basket size.
- What is the margin by order size? Why: small orders may be unprofitable, so smaller AOV with more orders could lower profit.
- Is the comparison like for like (same weeks, same categories)? Why: a seasonal category mix can move AOV.
- What is the goal: GMV, profit or new-user growth? Why: it defines "bad".

**Approach:**
1. Start with the arithmetic: revenue = orders x AOV. 1.09 x 0.85 = 0.9265, so GMV is down 7.4%. So yes, something needs attention.
2. Decompose AOV: AOV = items per order x average item price, and by segment (new versus existing, category, city, channel).
3. Split the change into within-segment (baskets shrank in the same type of user) and mix (more of the orders are from small-basket users).
4. Read each part: mix toward new users with small first baskets can be healthy; within-segment drops in existing users (fewer items, trading down, coupons) need action.
5. Check profit: contribution margin per order and total contribution, not only GMV.
6. Recommend: act on the within-segment part (for example a basket-building nudge, a free-delivery threshold), watch the new users' second-order basket.

**Metrics:**
- AOV = GMV / orders.
- GMV = orders x AOV.
- Within-segment effect = sum over segments of (old order share x change in segment AOV).
- Mix effect = sum over segments of (change in order share x new segment AOV).
- Guardrails: contribution margin per order, repeat rate of new users, orders per existing user.

**Risks:**
- Using AOV as a goal makes teams push basket size and hurt conversion.
- A mix effect can hide a within-segment problem (and the reverse).
- Order count rose, so a lazy reading says "fine".
- Order of decomposition changes the split slightly (mixed terms); state the convention.

**What the interviewer scores:**
- Strong: notices GMV fell despite the order rise, decomposes into within-segment and mix, and ties action to the part that matters.
- Strong: brings in margin and new-user value.
- Weak: "AOV fell so basket size is a problem."
- Weak: "orders rose 9%, so it is fine."

**Example:** (illustrative numbers, orders per 1,000-order base) Last quarter: existing users 800 orders at Rs 600, new users 200 orders at Rs 200: GMV Rs 520,000, AOV Rs 520. This quarter: existing 760 at Rs 560, new 330 at Rs 170: GMV Rs 481,700, AOV Rs 441.9, orders +9.0%, GMV -7.4%. Convention: within effect at old shares and new AOVs minus old AOVs, mix effect at new shares with new AOVs. Within = -Rs 38.0, mix = -Rs 40.1, total -Rs 78.1. The new-user share rose from 20% to 30%. About half of the AOV fall is mix, which is mostly healthy growth; the other half (existing baskets 600 to 560, new baskets 200 to 170) needs a cause. Weak answer: "AOV is down 15%, panic." Strong answer: "Half is mix from new users, half is real basket shrinkage; GMV is still down 7.4% so I would fix the existing-user baskets."

**Code:**
```python
# Q10: AOV fell 15% while orders rose 9% (illustrative, orders per 1,000 base)
q1 = {"existing": (800, 600), "new": (200, 200)}    # (orders, AOV Rs)
q2 = {"existing": (760, 560), "new": (330, 170)}

def tot(q):
    o = sum(v[0] for v in q.values()); rev = sum(v[0] * v[1] for v in q.values())
    return o, rev, rev / o
o1, r1, a1 = tot(q1); o2, r2, a2 = tot(q2)
print(f"Q1: orders {o1}, GMV Rs {r1:,}, AOV Rs {a1:.0f}")
print(f"Q2: orders {o2}, GMV Rs {r2:,}, AOV Rs {a2:.1f}")
print(f"orders {o2/o1-1:+.1%}, AOV {a2/a1-1:+.1%}, GMV {r2/r1-1:+.1%}")
assert a1 == 520 and round(a2) == 442 and round(o2 / o1 - 1, 2) == 0.09
assert round(r2 / r1 - 1, 3) == -0.074

# AOV change = within-segment (price/basket) effect + mix effect
share1 = {k: v[0] / o1 for k, v in q1.items()}
share2 = {k: v[0] / o2 for k, v in q2.items()}
within = sum(share1[k] * (q2[k][1] - q1[k][1]) for k in q1)     # old mix, new AOVs
mix = sum((share2[k] - share1[k]) * q2[k][1] for k in q1)        # new share, new AOVs
print(f"within-segment effect Rs {within:+.1f}, mix effect Rs {mix:+.1f}, total Rs {within+mix:+.1f} (actual {a2-a1:+.1f})")
assert abs(within + mix - (a2 - a1)) < 1e-9
print(f"new-user share of orders: {share1['new']:.0%} -> {share2['new']:.0%}")
print(f"mix is {mix/(a2-a1):.0%} of the AOV fall")
```

**Output (my run):**
```text
Q1: orders 1000, GMV Rs 520,000, AOV Rs 520
Q2: orders 1090, GMV Rs 481,700, AOV Rs 441.9
orders +9.0%, AOV -15.0%, GMV -7.4%
within-segment effect Rs -38.0, mix effect Rs -40.1, total Rs -78.1 (actual -78.1)
new-user share of orders: 20% -> 30%
mix is 51% of the AOV fall
```

**Follow-ups:**
- What if margin is higher on small orders? Then the lower AOV may not hurt profit; I would judge on contribution, not GMV.
- How would you validate the new users' small baskets? Follow them to their second and third order and see whether baskets grow.

**Common mistakes:** Ignoring that GMV fell. Treating AOV as the target. Not stating the decomposition convention. Looking only at the average and not at segment baskets.

### Q11 ⭐⭐⭐ 🟡 Overall conversion went from 4.0% to 3.8% this month, yet conversion rose on both mobile (from 2.0% to 2.2%) and desktop (from 6.0% to 6.2%). Explain how that is possible with a small worked example of traffic shares, and what you would tell the exec who only read the headline number.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
**Say this first (1 line):** This is a mix shift: more of the traffic is now on mobile, which converts lower, so the blended rate falls even though each segment improved; here mobile went from a 50% to a 60% share of sessions.

**Clarifying questions:**
- Are the two segments exhaustive (mobile plus desktop is all traffic)? Why: tablets or apps left out would break the arithmetic.
- Is the conversion rate sessions-based or users-based, with the same denominator in both months? Why: different denominators produce fake paradoxes.
- What drove the traffic shift (a marketing push, a new app, a seasonal pattern)? Why: it decides whether the shift is permanent.
- What is the goal metric: overall conversion or orders and revenue? Why: the right reading depends on what the exec cares about.
- Is there a third dimension (country, channel)? Why: the same trap can repeat one level down.

**Approach:**
1. Say it is possible: the overall rate is a weighted average of the segment rates, and the weights changed.
2. Solve for the traffic mix. Before: 2.0m + 6.0(1-m) = 4.0 gives m = 50%. After: 2.2m + 6.2(1-m) = 3.8 gives m = 60%.
3. Show the worked example with sessions: before 5,000 mobile + 5,000 desktop; after 6,000 mobile + 4,000 desktop.
4. Split the change: within-segment effect = +0.20pp (both segments improved by 0.2pp at the old mix); mix effect = -0.40pp (10 points of traffic moved to the lower-converting segment, valued at the new rates). Total -0.20pp.
5. Tell the exec: the product got better in both channels; the headline fell because more visits come from mobile. Report by segment and the standardised overall (at a fixed mix).
6. Suggest an action: a question about mobile traffic quality or the mobile funnel, not a rollback.

**Metrics:**
- Overall conversion = orders / sessions (the weighted average of segment conversions).
- Mix share = segment sessions / all sessions.
- Within-segment effect = sum over segments of (old share x change in conversion).
- Mix effect = sum over segments of (change in share x new conversion).
- Guardrail: orders and revenue totals, not only rates.

**Risks:**
- Quoting only the headline.
- Quoting only the segments and missing that overall orders per visit fell (that matters if the goal is blended).
- Splitting into more segments can reverse the story again.
- Decomposition convention changes the split slightly; state it.

**What the interviewer scores:**
- Strong: solves for the shares, shows the table, splits within versus mix, and gives the exec a clear message.
- Strong: says which number to use for decisions (segment rates and total orders).
- Weak: only names "Simpson's paradox" with no numbers.
- Weak: tells the exec the headline is wrong instead of incomplete.
- Cross-reference: Book 1 Part 10 has "What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment."; here it is a dashboard rollup.

**Example:** (illustrative numbers) Before: 5,000 mobile sessions at 2.0% plus 5,000 desktop at 6.0%: 100 + 300 = 400 orders, 4.0%. After: 6,000 mobile at 2.2% plus 4,000 desktop at 6.2%: 132 + 248 = 380 orders, 3.8%. Both segment rates rose by 0.2pp and the overall fell by 0.2pp. Within effect is +0.20pp, mix effect is -0.40pp. Weak answer: "The data must be wrong." Strong answer: "The mix moved 10 points to mobile; the product improved everywhere, and I would show the exec the table."

**Code:**
```python
# Q11: both segments up, overall down (illustrative sessions)
before = {"mobile": (5_000, 0.020), "desktop": (5_000, 0.060)}
after  = {"mobile": (6_000, 0.022), "desktop": (4_000, 0.062)}

def overall(d):
    s = sum(v[0] for v in d.values()); c = sum(v[0] * v[1] for v in d.values())
    return c / s
b, a = overall(before), overall(after)
print(f"overall {b:.1%} -> {a:.1%}")
assert round(b, 4) == 0.04 and round(a, 4) == 0.038
for k in before:
    print(f"{k:8} share {before[k][0]/10_000:.0%} -> {after[k][0]/10_000:.0%}, conv {before[k][1]:.1%} -> {after[k][1]:.1%}")

# split: within-segment effect at old mix, mix effect at new rates
w0 = {k: v[0] / 10_000 for k, v in before.items()}
w1 = {k: v[0] / 10_000 for k, v in after.items()}
within = sum(w0[k] * (after[k][1] - before[k][1]) for k in w0)
mix = sum((w1[k] - w0[k]) * after[k][1] for k in w0)
print(f"within-segment effect {within*100:+.2f}pp, mix effect {mix*100:+.2f}pp, total {(within+mix)*100:+.2f}pp")
assert round(within, 4) == 0.002 and round(mix, 4) == -0.004
assert abs(within + mix - (a - b)) < 1e-12

# what mobile share is needed for overall 3.8% with these rates?
m = (0.062 - 0.038) / (0.062 - 0.022)
print(f"mobile share that gives 3.8%: {m:.0%}")
assert round(m, 2) == 0.60
```

**Output (my run):**
```text
overall 4.0% -> 3.8%
mobile   share 50% -> 60%, conv 2.0% -> 2.2%
desktop  share 50% -> 40%, conv 6.0% -> 6.2%
within-segment effect +0.20pp, mix effect -0.40pp, total -0.20pp
mobile share that gives 3.8%: 60%
```

**Follow-ups:**
- Which number should the exec track? Segment conversions plus a mix-adjusted overall (fixed weights), and total orders.
- Can it go the other way (overall up while every segment falls)? Yes, with the same arithmetic reversed.

**Common mistakes:** Calling it a data error. Not giving the traffic shares. Averaging the two segment rates without weights. Not offering a mix-adjusted number.
