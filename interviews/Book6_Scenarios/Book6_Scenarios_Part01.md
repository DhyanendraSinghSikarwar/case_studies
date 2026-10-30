# Book 6 — Part 1: Product Metrics and Metric Drops

**Topic:** Scenario-based product-metrics questions for Data Scientist, Product Analyst and ML Engineer loops at Indian product companies, GCCs and global tech: DAU, WAU and MAU drops, conversion, retention and revenue drops, one metric up while another is down, Simpson's paradox and mix shift, metric definition and instrumentation changes, seasonality and holidays, new versus existing users, platform, version and geography breakdowns, notification, ranking and pricing changes, success metrics for a new feature, north-star and guardrail metrics, funnel and cohort diagnosis, decomposition trees, SQL-flavoured follow-ups at concept level, and AI-era twists (metrics for a GenAI feature).

**Target:** 55  |  **Actual:** 55 (⭐⭐⭐ 18, ⭐⭐ 25, ⭐ 12)  |  **Date:** 2026-10-30  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part owns diagnosing and defining metrics in product settings. It does not repeat the experiment theory in Book 1 Part 10 (choosing primary and guardrail metrics for a test, the Simpson's paradox definition inside an A/B test, reading a test where the primary metric and a guardrail disagree); the questions here are the same ideas met as live business situations (a dashboard drop, a rollup, a launch review), so Wave B answers should cross-reference those Book 1 questions only by checked headings. Book 6 Part 4 owns ambiguous experiment situations; Book 3 owns the full SQL; Book 2 owns GenAI internals (here only the metrics of a GenAI feature). All numbers in the prompts are invented illustrative numbers, not data from any company. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part01_sources.md). Searches returned metric-drop and root-cause question banks (Interview Query, Prachub, Codemia), product-sense and north-star pages (Dataford, datainterview.com), Simpson's-paradox prompts, metric trade-off guides, a checkout-conversion case page, Indian analyst interview guides (Interview Query, AmbitionBox, Dataford) and GenAI-chatbot metric posts. No result tied a single scenario to a named employer, so 'Asked at' lines name guide families only ('commonly reported in public guides'); scenarios marked as editor-designed have no located public page. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

### Q1 ⭐⭐⭐ 🟢 Daily active users fell 10% over two weeks (8.2% in the latest week). The dashboard shows 1.00 million DAU two weeks ago, 0.98 million last week and 0.90 million this week, with no release notes anywhere. Walk through how you would find out whether the drop is real and what caused it, and what you would check in the first hour.
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

### Q6 ⭐⭐⭐ 🟡 Android checkout conversion dropped from 3.1% to 2.6% while iOS is flat, starting the day version 8.4 shipped, while the crash rate is flat. Describe how you would narrow the cause, what you would compare by app version, and how you would decide between a product bug and a measurement bug.
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

### Q19 ⭐⭐ 🟢 Define 'active user' for a ride-hailing app and for a B2B analytics tool, and explain why the two definitions should differ. For each, say what action qualifies, over what window, and which fake-activity cases you would exclude.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** "Active" should mean the user got the core value of the product, so for ride-hailing it is a completed, genuine ride in a short window, and for a B2B analytics tool it is a real person doing a key analysis action, counted per account, over a weekly window.

**Clarifying questions:**
- What is the core value event for each product (a completed trip, a saved query or shared dashboard)? "Active" must point at it.
- How often should a healthy user come back? Frequency sets the window: a daily commute and a monthly report are different.
- Who is the customer: the rider (B2C) or the company that pays (B2B)? In B2B I count accounts as well as users.
- What fake activity exists (bots, emulators, internal staff, scheduled jobs, auto-refresh)? They must be excluded by rule.
- Is this metric for a growth target, an exec dashboard or a billing seat count? The purpose can change the definition.

**Approach:**
1. Start from value: list user actions, rank by closeness to value, pick the one that cannot happen by accident.
2. Pick the window from natural frequency: weekly or 28-day for rides (people ride a few times a month), weekly for a B2B tool with accounts as the unit.
3. Ride-hailing: active rider = at least one completed, paid ride in the last 28 days (and a weekly active version with 7 days). An app open alone is "visitor", not "active".
4. B2B analytics: active user = a real (non-service-account) user who ran a query or viewed a shared dashboard in the week. Active account = at least 2 distinct such users in the week, because one user alone may be a champion with no team adoption.
5. Exclusions: rides cancelled within seconds, bot or emulator devices (GPS spoofing, device farms), staff test accounts, duplicate accounts per device; for B2B, scheduled jobs and service accounts, logins with no action, auto-refresh dashboards.
6. Publish the definition with its owner and version, and keep a "visitors" metric next to it so reach is not lost.

**Metrics:**
- Ride-hailing 28-day active riders = distinct rider_ids with at least one completed, paid, non-test ride in the trailing 28 days.
- Stickiness = daily active riders / 28-day active riders.
- B2B weekly active accounts = accounts with at least 2 distinct real users who ran a key action in the week; weekly active users = distinct such users.
- Guardrails: share of activity removed by filters (a sudden jump means a filter bug), and the ratio of active to visitors.

**Risks:**
- A too-loose definition (app open) inflates numbers and hides churn.
- A too-strict one (only paid rides) hides engagement in a market where rides are rare.
- The window is arbitrary and moves the plateau and growth rates.
- Fraud filters can drop genuine users in some regions.

**What the interviewer scores:**
- Strong: defines by value event, window, unit, exclusions, and says why they differ. Weak: "any login".
- Strong: gives different windows for different natural frequencies. Weak: uses 30 days for everything.
- Strong: lists specific fake-activity cases. Weak: "bots".
- Strong: mentions versioning and reach alongside active.

**Example:** (illustrative) Toy log of 7 riders over 28 days: u1 two clean rides, u2 only opened the app, u3 a ride cancelled in 20 seconds, u4 clean ride, u5 a device-farm ride, u6 an employee test ride, u7 clean ride. Any event counts 7 users. Completed and clean counts 3 (u1, u4, u7). B2B toy week: four accounts have events; acme (2 users run a query or open a dashboard) and delta (2 users run queries) are active; beta has only one user and a login; gamma has only a scheduled service account. Active accounts are 2, not 4. Weak answer: "Anyone who logs in." Strong answer: "Completed clean ride in 28 days; accounts with two real users doing key actions in a week."

**Code:**
```python
# Toy 28-day log. Each row: (user, kind, detail)
ride_events = [
 ("u1", "ride_completed", "ok"), ("u1", "ride_completed", "ok"),
 ("u2", "app_open", ""),                          # only opened the app
 ("u3", "ride_completed", "cancel_in_20s"),       # cancelled almost at once, still logged
 ("u4", "ride_completed", "ok"),                
 ("u5", "ride_completed", "device_farm"),         # emulator / GPS-spoof pattern
 ("u6", "ride_completed", "employee_test"),
 ("u7", "ride_completed", "ok"),
]
naive_ride = {u for u, k, d in ride_events}                                  # any event
good_ride  = {u for u, k, d in ride_events if k == "ride_completed" and d == "ok"}
print("ride, any event       :", len(naive_ride))
print("ride, completed+clean :", len(good_ride), sorted(good_ride))
assert len(naive_ride) == 7 and good_ride == {"u1", "u4", "u7"}
# B2B tool: weekly active ACCOUNT = at least 2 distinct users ran a saved query or opened a shared dashboard
b2b = [
 ("acme", "u1", "run_query", "2026-10-05"), ("acme", "u2", "view_dashboard", "2026-10-06"),
 ("beta", "u3", "login", "2026-10-05"),                       # login only
 ("beta", "u3", "run_query", "2026-10-06"),                   # one user only
 ("gamma", "svc", "run_query", "2026-10-07"),                 # scheduled job, not a person
 ("gamma", "svc", "run_query", "2026-10-08"),
 ("delta", "u9", "run_query", "2026-10-07"), ("delta", "u10", "run_query", "2026-10-07"),
]
service = {"svc"}
valid = {"run_query", "view_dashboard"}
from collections import defaultdict
users = defaultdict(set)
for acct, u, act, day in b2b:
    if act in valid and u not in service:
        users[acct].add(u)
active = sorted(a for a, us in users.items() if len(us) >= 2)
print("B2B weekly active accounts (>=2 real users, key action):", active)
assert active == ["acme", "delta"]
print("accounts with any login/event:", len({a for a, *_ in b2b}))
assert len({a for a, *_ in b2b}) == 4
```

**Output (my run):**
```text
ride, any event       : 7
ride, completed+clean : 3 ['u1', 'u4', 'u7']
B2B weekly active accounts (>=2 real users, key action): ['acme', 'delta']
accounts with any login/event: 4
```

**Follow-ups:**
- Why a threshold of two users for accounts? One user can be a champion without adoption; two means a team uses it. The threshold is a choice; test it against renewal.
- Should the definition change when the product changes? Yes, but version it and backfill; see Book 6 Part 1 Q14.
- Seat-based billing active user? That is a different definition (billing), do not reuse it for engagement.

**Common mistakes:**
- Using the same window for products with different natural frequency.
- Counting app opens, logins or page views as activity.
- No exclusion rules, so bots and internal users inflate the base.
- Counting B2B only by user, never by account.

### Q20 ⭐⭐ 🟢 A retention curve for a new app flattens at 12% after day 30, while a competitor's guide quotes a higher plateau. Explain what a flattening curve means, what you would compare (cohorts, channels, definitions) before concluding anything, and what a curve that never flattens would imply.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** A curve that flattens at 12% means a stable core of users who found lasting value; before I compare it to a competitor's number I check that the cohorts, channels and the definition of "retained" are the same.

**Clarifying questions:**
- Is retention "opened on exactly day N" (classic) or "opened any time in the days after" (bracket or range)? The same users give very different numbers.
- Which cohorts, and how many users? A 12% on a small cohort has a wide interval.
- What does the competitor's guide measure (installs versus signups versus activated users, which category, which market)? Different denominators.
- Which channels brought the users (organic, paid, referral)? Paid cohorts usually retain worse.
- What counts as retained: any open, or a meaningful action?

**Approach:**
1. Read the curve: the drop up to about day 7 is mostly casual users leaving; the flat part is the loyal core. The plateau is the share who stuck.
2. Make sure it is flat in the data: look at the last few points, with confidence intervals, and use enough cohort age (not a cohort that has only 30 days of data).
3. Compare like with like: same definition (classic vs range), same denominator (installs vs activated), same period, same market and category.
4. Split by cohort (signup week), channel, platform and country. A blend can hide a good organic cohort and a poor paid cohort.
5. Check the stability of the plateau across cohorts. A rising plateau means the product is improving; a falling one means newer cohorts are worse.
6. Use the plateau and the drop speed: early drop = onboarding problem, plateau height = long-term fit.
7. Conclude only on the like-for-like comparison, and say what would change the view.

**Metrics:**
- Classic day-N retention = users active on day N / users in the cohort. Bracket retention = users active in days N to N+6 / users in the cohort.
- Plateau = value at which the curve stops falling (compare points a few weeks apart).
- Cohort size n and the interval: 12% +/- 1.96 x sqrt(0.12 x 0.88 / n).
- Guardrail: activation rate (the denominator), so "retention" is not improved by a stricter denominator.

**Risks:**
- Quoting competitor numbers from guides: different definitions, markets and audiences.
- Averaging cohorts that differ in channel mix (see Book 6 Part 1 Q26).
- Calling a slow decline a plateau when the cohort is too young.
- Survivorship: flat only because the base is already the loyal core.

**What the interviewer scores:**
- Strong: explains the curve in words (core and casual users) and tests flatness. Weak: "12% is low/high" with no comparison.
- Strong: raises definition and cohort differences before judging. Weak: accepts the competitor figure.
- Strong: knows a never-flattening curve implies no durable core. Weak: says it means "retention is falling" only.
- Strong: gives intervals for small cohorts.

**Example:** (illustrative model) 20% of users are "core" and open the app on 60% of days forever; 80% are casual and fade out with a 5-day time constant. Classic retention is 44.7% on day 1, 21.9% on day 7, 14.4% on day 14, 12.1% on day 30 and 12.0% on day 60 and 90. The same users under a 7-day bracket definition show a plateau of 20.0%. So a competitor quoting 20% may measure the same quality with a different ruler. Sampling: 12% on 1,000 users is +/- 2.0 points, on 10,000 users +/- 0.6 points. A curve with no core group (decay only) falls to 11.2% at day 30, 2.5% at day 60 and 0.6% at day 90 in the model. Weak answer: "The competitor is better." Strong answer: "Same product, bracket definition gives 20%; I compare like with like first."

**Code:**
```python
from math import sqrt, exp
# Illustrative mixture: 20% 'core' users who return on 60% of days forever; 80% casual who fade out (decay 5 days)
core, p_core = 0.20, 0.60
casual, p_cas, tau = 0.80, 0.50, 5.0
def classic(day):            # opened the app ON day N
    return core * p_core + casual * p_cas * exp(-day / tau)
def bracket(day):            # opened ANY day in N..N+6
    return core * (1 - (1 - p_core) ** 7) + casual * (1 - (1 - p_cas * exp(-day / tau)) ** 7)
print("day  classic  7-day-bracket")
for d in (1, 7, 14, 30, 60, 90):
    print(f"{d:>3}  {classic(d):6.1%}  {bracket(d):6.1%}")
assert round(classic(30), 3) == 0.121 and round(classic(90), 3) == 0.120
assert round(bracket(30), 3) == 0.207 and round(bracket(60), 3) == 0.200
print(f"plateau classic {core * p_core:.1%}, bracket {core * (1 - 0.4 ** 7):.1%}")
assert round(core * p_core, 3) == 0.12 and round(core * (1 - 0.4 ** 7), 3) == 0.200
# sampling noise on a 12% number
for n in (1_000, 10_000):
    h = 1.96 * sqrt(0.12 * 0.88 / n)
    print(f"n={n:>6}: 12% +/- {h * 100:.1f} pts")
assert round(1.96 * sqrt(0.12 * 0.88 / 1000) * 100, 1) == 2.0
assert round(1.96 * sqrt(0.12 * 0.88 / 10000) * 100, 1) == 0.6
# a curve that never flattens: no core group
def no_core(day): return 0.5 * exp(-day / 20)
print("no-core curve day 30/60/90:", [f"{no_core(d):.1%}" for d in (30, 60, 90)])
assert no_core(90) < no_core(60) < no_core(30)
```

**Output (my run):**
```text
day  classic  7-day-bracket
  1   44.7%   98.0%
  7   21.9%   68.1%
 14   14.4%   35.5%
 30   12.1%   20.7%
 60   12.0%   20.0%
 90   12.0%   20.0%
plateau classic 12.0%, bracket 20.0%
n=  1000: 12% +/- 2.0 pts
n= 10000: 12% +/- 0.6 pts
no-core curve day 30/60/90: ['11.2%', '2.5%', '0.6%']
```

**Follow-ups:**
- What does a curve that never flattens imply? No durable habit: every cohort drains to zero, so growth needs constant acquisition and unit economics usually fail.
- How do you raise the plateau? Only product value does it; onboarding changes raise early points but often not the plateau (Book 6 Part 1 Q33 covers an early lift that fades).
- Are retention curves safe for a new app with 30 days of data? Only up to day 30; do not extrapolate the plateau without older cohorts.

**Common mistakes:**
- Comparing across definitions or denominators.
- Reading a small cohort as precise.
- Mixing channels and calling the blend "the product".
- Calling a curve flat because it looks flat on a long log axis.

### Q21 ⭐⭐ 🟢 The order cancellation rate on a delivery app rose from 4% to 6% over two weeks. List how you would break it down (who cancels, at what stage, for what reason) and which one or two cuts would most quickly separate a supply problem from a customer problem.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
**Say this first (1 line):** I break cancellations down by who cancelled and at what stage, then use two cuts, initiator by stage and supply tightness by zone and hour, to see in minutes whether the extra 2 points come from not having partners (supply) or from customers changing their minds (customer).

**Clarifying questions:**
- Is the rate cancelled orders / placed orders, and did the definition of "placed" change? A changed denominator moves the rate.
- Do cancellations carry a reason code and initiator (customer, restaurant, system, support)? Without them I must infer.
- Did the two weeks include rain, a festival, a strike, or a policy change (fees, ETA display)? Context for the cut.
- Is the rise spread evenly across cities or concentrated? Concentration points to local supply.
- What does the customer see at cancellation (a "no partner found" message, a long ETA)? It tells me whether the product caused it.

**Approach:**
1. Confirm it is real: same definition, same denominator, daily series, no data lag.
2. Who cancels: customer, restaurant, system (no partner assigned), support or payment.
3. At what stage: before restaurant accepts, after accept (preparing), after pickup (in transit).
4. Why: reason codes, and the quoted ETA and fee at the time of order.
5. Where and when: city, zone, hour, restaurant, new versus returning customers.
6. The two fast cuts:
   - Initiator x stage: shows which cell moved. "System / no partner assigned" points to supply. "Customer / before accept" points to the customer or product side (price, fee, ETA).
   - Cancel rate by supply tightness (orders per available partner in the zone-hour). If the rise is only in tight zone-hours it is supply. If it is spread evenly across loose and tight zones it is customer or product.
7. Confirm with timing: did the rise start on a date (fee change, ETA display change, partner payout cut)?

**Metrics:**
- Cancellation rate = cancelled orders / placed orders, in the same period.
- Contribution of a cell = (after count - before count) / total rise in cancellations.
- Partner pressure = orders placed / partners online in the zone-hour.
- Guardrails: delivery time, refund rate, repeat order rate (cancellation hurts repeat).

**Risks:**
- Reason codes are self-reported (customers pick "changed my mind" when the ETA was long).
- Supply and demand are linked: a strike raises ETAs, which makes customers cancel; the initiator column says "customer" but the root cause is supply.
- Mix: a growth in new users or a cheap category may change the base rate.
- Late-arriving cancellation records, so the last days look better.

**What the interviewer scores:**
- Strong: three-way breakdown plus two decisive cuts. Weak: a long list of cuts with no priority.
- Strong: notices the link between supply and customer cancellations. Weak: takes reason codes at face value.
- Strong: quantifies contribution to the 2-point rise. Weak: "some in each".
- Strong: suggests actions per cause (incentivise partners, change ETA display, fix stock).

**Example:** (illustrative numbers) 100,000 orders in each fortnight. Cancellations rise from 4,000 to 6,000 (4.0% to 6.0%). The cell "system / no delivery partner assigned" rises from 900 to 2,650, which is 1,750 of the 2,000 extra cancellations, or 88%. The others each rise by about 50 to 100. Second cut: 20,000 orders sit in tight-supply zone-hours, where the cancel rate goes from 7.5% to 19.0%; the 80,000 balanced orders go from 3.1% to 2.8%. So it is a supply problem in specific zone-hours. Weak answer: "Customers are cancelling more, improve the app." Strong answer: "88% of the rise is no partner assigned, all in tight zone-hours; fix partner supply, then re-measure."

**Code:**
```python
# Illustrative: 100,000 orders per fortnight. Cancellation counts by initiator and stage.
rows = [  # (initiator, stage, before, after)
 ("customer",   "before restaurant accepts",       1_300, 1_350),
 ("customer",   "after pickup (wrong/late)",         400,   450),
 ("restaurant", "after accept (item out of stock)",  900,   950),
 ("system",     "no delivery partner assigned",      900, 2_650),
 ("support",    "payment/other",                     500,   600),
]
n = 100_000
b = sum(r[2] for r in rows); a = sum(r[3] for r in rows)
print(f"cancel rate {b / n:.1%} -> {a / n:.1%}")
assert b == 4_000 and a == 6_000
print(f"{'initiator / stage':<46}{'before':>8}{'after':>8}{'delta pts':>10}{'share of rise':>15}")
for who, stage, x, y in rows:
    print(f"{who + ' / ' + stage:<46}{x / n:>8.1%}{y / n:>8.1%}{(y - x) / n * 100:>+10.2f}{(y - x) / (a - b):>15.0%}")
assert (2_650 - 900) / (a - b) == 0.875
# second cut: same orders by partner supply at the time of order (orders per available partner in zone-hour)
cut = {"tight supply (>=3 orders/partner)": (20_000, 1_500, 3_800),
       "balanced (<3)":                    (80_000, 2_500, 2_200)}   # (orders in each period, cancels before, cancels after); 20k/80k split assumed same both periods
for k, (m, c0, c1) in cut.items():
    print(f"{k:<36} orders {m:>6,}  cancel rate {c0 / m:.1%} -> {c1 / m:.1%}")
assert sum(v[1] for v in cut.values()) == 4_000 and sum(v[2] for v in cut.values()) == 6_000
assert round(1_500 / 20_000, 3) == 0.075 and round(3_800 / 20_000, 3) == 0.190 and round(2_200 / 80_000, 4) == 0.0275
```

**Output (my run):**
```text
cancel rate 4.0% -> 6.0%
initiator / stage                               before   after delta pts  share of rise
customer / before restaurant accepts              1.3%    1.4%     +0.05             2%
customer / after pickup (wrong/late)              0.4%    0.4%     +0.05             2%
restaurant / after accept (item out of stock)     0.9%    0.9%     +0.05             2%
system / no delivery partner assigned             0.9%    2.6%     +1.75            88%
support / payment/other                           0.5%    0.6%     +0.10             5%
tight supply (>=3 orders/partner)    orders 20,000  cancel rate 7.5% -> 19.0%
balanced (<3)                        orders 80,000  cancel rate 3.1% -> 2.8%
```

**Follow-ups:**
- What if it is a customer problem? Then look at fee, ETA shown, price changes, and first-time customers; test with an experiment on the display.
- How fast can you tell? Both cuts come from one table grouped by initiator, stage, zone and hour, so within the first hour.
- What action for supply? Surge payout, rider onboarding, batching, or limiting orders in tight zone-hours so promised ETAs are honest.

**Common mistakes:**
- Using only reason codes without checking stage and timing.
- Averaging across zones so the local supply spike disappears.
- Forgetting the denominator (orders placed may have changed).
- Treating the "customer cancelled" label as a customer problem.

### Q22 ⭐⭐ 🟢 A funnel for a lending app shows visit to signup 40%, signup to KYC 55%, KYC to approval 70%, approval to disbursal 80%. Disbursal volume fell 10% month over month. Explain how you would find which step changed, and why step conversion and absolute counts need to be read together.
**Asked at:** Funnel and checkout-conversion case pages (a Prachub Amazon checkout-conversion root-cause page, funnel guides from Amplitude, Hackle and Datadog); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I compare each step's rate and absolute count month against month, because a fall in disbursals can come from fewer people entering, a worse step conversion, or a change in who enters, and rates alone or counts alone each hide one of these.

**Clarifying questions:**
- Are the funnel steps cohort-based (the same people followed through) or period-based (events in the month)? Lags between steps (KYC today, approval next week) mix cohorts in a period view.
- Did anything change in policy: credit rules, KYC vendor, approval thresholds, disbursal partners? Approval and disbursal steps are rule-driven.
- Did traffic sources change (more paid, new partner channel)? A new audience changes every rate.
- What is the typical time lag between steps? It sets whether this month's disbursals come from last month's approvals.
- Are the counts de-duplicated by user, and is the 10% in count or in rupees disbursed? Rupees add loan-size effects.

**Approach:**
1. Write the funnel for both months with counts and rates: visits, signups, KYC done, approved, disbursed. Overall visit to disbursal here is 0.40 x 0.55 x 0.70 x 0.80 = 12.32%.
2. Compute the change in each step ratio and in each absolute count. Since overall = product of step rates x visits, a 10% fall must come from visits or from one or more step rates; a log split attributes it.
3. Read rates and counts together:
   - Rates unchanged, counts down everywhere: the top of the funnel shrank (traffic).
   - One rate down, upstream counts unchanged: a step problem (KYC vendor, policy).
   - A rate down but upstream counts up: a mix change (cheap traffic brought low-quality users); the rate fall is not a product failure.
4. Use cohort view with lags: follow the same signup cohort to disbursal so timing does not fake a step change.
5. Segment the step that moved: channel, device, KYC method, city, loan product.
6. Pair with rupees disbursed, since average loan size can offset counts.

**Metrics:**
- Step rate = users reaching step k+1 / users reaching step k (same cohort, same window).
- Overall conversion = disbursed / visits. Disbursal volume = overall conversion x visits.
- Contribution of a step to the fall = ln(rate ratio) / ln(disbursal ratio).
- Guardrails: approval rate quality (default rate of newly approved), KYC rejection reasons, time between steps.

**Risks:**
- Period-based funnels with lags show a step change that is only timing.
- A rate that fell because of traffic mix gets "fixed" by a product change.
- Comparing counts with different traffic volumes.
- Rule changes (tighter credit policy) lower approval on purpose; the fix may be to leave it.

**What the interviewer scores:**
- Strong: separates count, rate and mix, and says which is which. Weak: "KYC is the biggest drop-off, fix KYC".
- Strong: uses cohorts and lags. Weak: month totals only.
- Strong: notes that the largest drop-off step is not necessarily the one that changed.
- Strong: asks about policy changes and risk quality.

**Example:** (illustrative numbers) Last month: 1,000,000 visits, 400,000 signups, 220,000 KYC done, 154,000 approved, 123,200 disbursed (12.32%). This month all three of these scenarios give 110,880 disbursals (-10.0%):
- A: visits fall 10% to 900,000, all rates the same. Rates show nothing, counts show it.
- B: KYC to approval falls from 70% to 63%, counts above that step are unchanged. The rate shows it.
- C: cheap traffic brings 1,250,000 visits (+25%), visit to signup falls to 28.8%. Every count from signup down is lower and the rate fell, but visits rose.
Each needs a different action: marketing, credit or KYC operations, and channel quality. Weak answer: "KYC to approval is 70%, the lowest, so fix it." Strong answer: "Which rate or count moved? Rates are unchanged in A, so it is traffic."

**Code:**
```python
rates0 = [0.40, 0.55, 0.70, 0.80]
names = ["visit>signup", "signup>KYC", "KYC>approval", "approval>disbursal"]
def run(visits, rates):
    c = [visits]
    for r in rates: c.append(c[-1] * r)
    return c
base = run(1_000_000, rates0)
print("last month counts:", [round(x) for x in base])
overall = 1
for r in rates0: overall *= r
print(f"overall visit>disbursal {overall:.2%}")
assert round(overall, 4) == 0.1232 and round(base[-1]) == 123_200
scen = {
 "A: traffic -10%, all rates same":      run(900_000, rates0),
 "B: KYC>approval 70% -> 63%":           run(1_000_000, [0.40, 0.55, 0.63, 0.80]),
 "C: cheap traffic +25%, signup 28.8%":  run(1_250_000, [0.288, 0.55, 0.70, 0.80]),
}
for k, c in scen.items():
    r = [c[i + 1] / c[i] for i in range(4)]
    print(k)
    print("   counts:", [round(x) for x in c], f"disbursal {c[-1] / base[-1] - 1:+.1%}")
    print("   rates :", [f"{x:.1%}" for x in r])
    assert round(c[-1]) == 110_880
```

**Output (my run):**
```text
last month counts: [1000000, 400000, 220000, 154000, 123200]
overall visit>disbursal 12.32%
A: traffic -10%, all rates same
   counts: [900000, 360000, 198000, 138600, 110880] disbursal -10.0%
   rates : ['40.0%', '55.0%', '70.0%', '80.0%']
B: KYC>approval 70% -> 63%
   counts: [1000000, 400000, 220000, 138600, 110880] disbursal -10.0%
   rates : ['40.0%', '55.0%', '63.0%', '80.0%']
C: cheap traffic +25%, signup 28.8%
   counts: [1250000, 360000, 198000, 138600, 110880] disbursal -10.0%
   rates : ['28.8%', '55.0%', '70.0%', '80.0%']
```

**Follow-ups:**
- What if both traffic and one rate changed? Use the log split to give each its share, and confirm with a cohort for each channel.
- How do you handle the lag? Follow signup cohorts weekly to disbursal and compare cohorts of the same age.
- Should you worry that approval is lower? Check the default rate of approved loans before pushing approval up; a lower approval rate may be intended risk control.

**Common mistakes:**
- Optimising the biggest drop-off step without checking it changed.
- Reading rates when the mix changed.
- Reading counts without the denominator.
- Ignoring lags between funnel steps.

### Q23 ⭐⭐ 🟢 Define success metrics for a referral programme that gives Rs 100 to both sides. List the metrics, the guardrails, and the abuse patterns, and say which number you would present to finance to prove the programme is not just buying users who leave.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** I would show finance one number, the contribution earned per rupee of reward on genuine, incremental users still active at day 90, because that is the only number that shows the programme is not buying users who leave.

**Clarifying questions:**
- When is the Rs 100 paid: at signup, first order, or after a minimum spend? It decides how much abuse we pay for before we can catch it.
- Is there a clawback if the referred user is later flagged or refunds? It caps the loss from fraud.
- What does a user normally cost us through paid channels? We need a benchmark to say "cheap" or "dear".
- Can we hold out a small random slice of users from seeing the offer? Without a holdout we cannot say who would have joined anyway.
- What is a "retained" user for this business (order, session, payment)? The metric has to match how we earn money.

**Approach:**
1. Draw the funnel: invites sent, invites opened, signups, qualified (met the reward rule), rewarded.
2. Split every qualified user into genuine and suspicious using rules (same device, same payment instrument, same address, burst signups, referrer with an unusual number of referrals).
3. Compare genuine referred users with a matched or held-out group on day-30 and day-90 activity, orders and margin.
4. Estimate incrementality: the share of referred users who would not have joined without the offer (from a holdout of users not shown the programme).
5. Put cost, retention, incrementality and margin into one ratio, and compare cost per incremental retained user with the paid-channel cost.

**Metrics:**
| Metric | Definition | Role |
|---|---|---|
| Qualified referral rate | qualified referred users / invites sent | Funnel health |
| Abuse share | flagged qualified users / all qualified users | Guardrail |
| D90 active rate | genuine referred users active on day 90 / genuine referred users | Quality |
| Incrementality | referred users who would not have joined anyway / genuine referred users (holdout estimate) | Causal |
| Cost per incremental D90-active user | total reward cost / (D90-active genuine users x incrementality) | Efficiency |
| **Contribution per Rs of reward** | (incremental D90-active users x 90-day margin per retained user) / total reward cost | **Number for finance** |

Guardrails: abuse share, refund and chargeback rate of referred users, support tickets per referred user, the referred users' share of promo-only orders.

**Risks:**
- Paying on signup rewards fake accounts, not value.
- Referrers are already heavy users, so their friends look good (selection). Compare with a holdout, not with the all-user average.
- Counting rewards as marketing but not as the cost of a discount on the first order (double benefit).
- Day-90 data is late. Use day-30 as a leading read, but label it so.

**What the interviewer scores:**
- Strong: separates genuine from abusive users and uses an incrementality estimate. Weak: reports invites and signups only.
- Strong: picks one finance number with a defined numerator and denominator. Weak: lists ten metrics and no decision.
- Strong: names concrete abuse patterns and a rule for the payout (pay after first order, clawback). Weak: says "monitor fraud".
- Strong: compares with another channel's cost. Weak: gives cost per signup alone.

**Example:** (illustrative numbers) 1,250 users qualify and Rs 100 goes to both sides, so the reward cost is 1,250 x Rs 200 = Rs 2,50,000. Rules flag 250 as abusive (20%), leaving 1,000 genuine. 35% of them are active on day 90, that is 350. A holdout says 60% would not have joined without the offer, so 210 are incremental. Cost per incremental D90-active user is Rs 2,50,000 / 210 = about Rs 1,190. If a retained user is worth Rs 1,500 of margin in 90 days, contribution is Rs 3,15,000, which is Rs 1.26 per rupee of reward.
- Weak: "Cost per qualified user is Rs 200, great, scale it."
- Strong: "Rs 200 per qualified user is really Rs 1,190 per incremental retained user, and it returns Rs 1.26 per rupee, so it pays for itself but with thin headroom, and abuse is 20%."

**Code:**
```python
# Q23 referral programme unit economics (illustrative numbers)
reward_each_side = 100            # Rs per side, paid on qualification
qualified_pairs = 1250            # referred users who met the qualifying rule
abusive = 250                     # flagged as self-referral / fake / device-sharing
genuine = qualified_pairs - abusive
reward_cost = qualified_pairs * 2 * reward_each_side   # paid before detection
d90_active_rate = 0.35            # genuine referred users active on day 90
incrementality = 0.60             # share who would NOT have joined without the offer (holdout estimate)
margin_per_retained_90d = 1500    # Rs contribution per retained user over 90 days (assumed)

d90_active = genuine * d90_active_rate
incremental_active = d90_active * incrementality
cost_per_incr_active = reward_cost / incremental_active
net_contribution = incremental_active * margin_per_retained_90d
ratio = net_contribution / reward_cost

print("genuine referred users:", genuine)
print("reward cost (Rs):", reward_cost)
print("abuse share of qualified:", abusive / qualified_pairs)
print("D90-active genuine:", d90_active)
print("incremental D90-active:", incremental_active)
print("cost per incremental D90-active (Rs):", round(cost_per_incr_active, 1))
print("net contribution (Rs):", net_contribution)
print("contribution per Rs of reward:", round(ratio, 3))

assert genuine == 1000 and reward_cost == 250000
assert abusive / qualified_pairs == 0.2
assert round(d90_active) == 350 and round(incremental_active) == 210
assert round(cost_per_incr_active, 1) == 1190.5
assert net_contribution == 315000 and round(ratio, 2) == 1.26
# naive view that finance would reject: cost per qualified user ignores abuse, retention, incrementality
print("naive cost per qualified pair (Rs):", reward_cost / qualified_pairs)
assert reward_cost / qualified_pairs == 200
```

**Output (my run):**
```text
genuine referred users: 1000
reward cost (Rs): 250000
abuse share of qualified: 0.2
D90-active genuine: 350.0
incremental D90-active: 210.0
cost per incremental D90-active (Rs): 1190.5
net contribution (Rs): 315000.0
contribution per Rs of reward: 1.26
naive cost per qualified pair (Rs): 200.0
```

**Follow-ups:**
- How do you get incrementality without a holdout? Compare against users with similar tenure and activity who did not get the offer, and say that it is weaker. See Book 1 Part 10 Q24 (holdout / long-term holdout) for the idea.
- Which side of the reward matters more? Test the split: referrer-only, referee-only and both. Costs differ and so do the abuse patterns.
- What if D90 is positive but the margin number is a guess? Show the ratio at a low, base and high margin and say where it breaks even.

**Common mistakes:** Presenting signups as success. Using cost per signup. Ignoring abuse in the denominator. No holdout. Using the all-users retention as the comparison.

### Q24 ⭐⭐ 🟢 Email open rate jumped from 20% to 45% overnight with no change in content. Explain what you would suspect first, how you would check it using downstream metrics such as clicks and conversions, and what you would do to the metric definition.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** A jump from 20% to 45% overnight with no content change is almost always a measurement change, most likely mail clients pre-fetching the tracking pixel, so I would not celebrate, I would check clicks and rebuild the metric.

**Clarifying questions:**
- Did anything change on the sending side (new email platform, new tracking domain, new image-loading setup)? A vendor or template change can move opens by itself.
- Is the jump across all audiences or in some mail clients or domains? A localised jump points to the client, not to the people.
- Did clicks, conversions and unsubscribes move too? These do not depend on the pixel.
- Is it the open rate on delivered or on sent emails, and did the denominator change? A bounce-handling change also moves it.
- Is this campaign-level or one sender? It tells me whether it is a pipeline-wide issue.

**Approach:**
1. Suspect the measurement first. An "open" is only a request for a tiny image. Some mail clients and privacy features fetch images automatically (Apple Mail Privacy Protection since 2021 is the best-known example), so a machine can create an open with no human reading.
2. Check downstream metrics. Clicks, click-to-open rate, conversions and unsubscribes should rise if people truly engaged more. If they are flat, the extra opens are not people.
3. Segment opens by mail client, user agent, IP ranges, and time between send and open. Machine opens come within seconds of delivery and from a small set of proxy addresses.
4. Compare with a client that does not pre-fetch. If its open rate is unchanged, the jump lives in the pre-fetching segment.
5. Fix the definition: report click rate per delivered email as the headline, keep opens only as a directional signal, exclude known proxy opens where possible, and annotate the date.

**Metrics:**
- Open rate = unique opens / delivered emails (inflated by machine opens).
- Click rate = unique clicks / delivered emails (not pixel-based).
- Click-to-open rate = unique clicks / unique opens (falls when opens are inflated).
- Conversion rate per delivered email = conversions attributed to the email / delivered emails.
- Guardrails: unsubscribe rate, spam-complaint rate, bounce rate.

**Risks:**
- A real change can coincide (a better subject line). Segment before you decide.
- Excluding proxy opens removes some real opens too. Say that the new series is a different, smaller measure.
- Old open-rate-based rules (send-time optimisation, "engaged user" lists) can now be wrong. List them.

**What the interviewer scores:**
- Strong: says "suspect measurement before behaviour" and gives one concrete mechanism. Weak: explains the jump as better content.
- Strong: uses downstream metrics that do not rely on the pixel. Weak: checks only the same metric on more cuts.
- Strong: changes the definition and annotates the break. Weak: leaves it as is and reports a win.

**Example:** (illustrative numbers) 100,000 emails, half go to a client that pre-fetches. After the change that client shows a 70% open rate and the other stays at 20%, so the blend is 0.5 x 70% + 0.5 x 20% = 45%. Clicks are 2,000 both before and after (2% of delivered). Opens went from 20,000 to 45,000, so click-to-open fell from 10.0% to 4.4%.
- Weak: "Opens more than doubled, the new subject lines work."
- Strong: "Opens rose 125%, clicks are flat, click-to-open fell from 10% to 4.4% and the clients that do not pre-fetch are unchanged, so this is machine opens, and I will switch the headline to clicks per delivered."

**Code:**
```python
# Q24 open rate 20% -> 45% from machine opens (illustrative numbers)
sends = 100_000
apple_share = 0.5                  # share of sends delivered to a client that pre-fetches the pixel
open_before = {"proxy": 0.20, "other": 0.20}
open_after = {"proxy": 0.70, "other": 0.20}   # proxy opens now include machine opens
click_rate_per_send = 0.02         # unchanged in both groups, both periods

def blended(d):
    return apple_share * d["proxy"] + (1 - apple_share) * d["other"]

ob, oa = blended(open_before), blended(open_after)
opens_b, opens_a = round(ob * sends), round(oa * sends)
ob, oa = round(ob, 4), round(oa, 4)
clicks = round(click_rate_per_send * sends)
ctor_b, ctor_a = clicks / opens_b, clicks / opens_a
print("open rate before/after:", ob, oa)
print("opens before/after:", opens_b, opens_a)
print("clicks (both periods):", clicks)
print("click-to-open before/after:", round(ctor_b, 3), round(ctor_a, 3))
print("open rate non-proxy only, before/after:", open_before["other"], open_after["other"])
assert round(ob, 2) == 0.20 and round(oa, 2) == 0.45
assert opens_b == 20000 and opens_a == 45000
assert clicks == 2000
assert round(ctor_b, 3) == 0.100 and round(ctor_a, 3) == 0.044
assert open_after["other"] == open_before["other"]
# proxy-adjusted metric: count opens only from non-proxy clients, or use clicks per delivered
print("clicks per delivered:", clicks / sends)
assert clicks / sends == 0.02
```

**Output (my run):**
```text
open rate before/after: 0.2 0.45
opens before/after: 20000 45000
clicks (both periods): 2000
click-to-open before/after: 0.1 0.044
open rate non-proxy only, before/after: 0.2 0.2
clicks per delivered: 0.02
```

**Follow-ups:**
- Can you still use opens? As a trend within a client that does not pre-fetch, or as a rough signal, never as a precise level.
- What if clicks also jumped? Then check for link scanners and bots that click links (security gateways), which the same segmentation by user agent and timing would show.

**Common mistakes:** Reporting the jump as a win. Looking only at open rate by segment and not at clicks. Changing the definition without annotating the date, which breaks the trend.

### Q25 ⭐⭐ 🟡 DAU fell 6% during the week of a major festival and a cricket tournament. Describe how you would test whether this is seasonal, which prior periods to line up (same festival last year, same weekday), and what you would say to a PM who wants an alert raised.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** I would not raise an alert yet: first I line this week up against the same festival in earlier years, the same weekday, and the cricket schedule, and only call it abnormal if it falls outside what those weeks did.

**Clarifying questions:**
- Which days fell and how much per day? A festival often cuts the festival day itself and lifts the evening after.
- Is the festival date fixed by a lunar calendar? If so, last year's festival sits in a different calendar week and a same-week-last-year comparison is wrong.
- Did cricket matches fall on the same days, and are they new this year (a tournament cycle)? It tells me whether to treat it as a second seasonal factor.
- Is the drop in all regions and platforms or in a few? A festival hits some regions harder.
- Do we have clean data for at least two or three past years? With one year the seasonal estimate is thin.

**Approach:**
1. Rule out data problems first (pipeline, tracking), then ask whether the drop is large against normal noise.
2. Build a baseline per day: the average of the same weekday in the 4 weeks before the event, so a weekday pattern does not leak in.
3. Compute the ratio "event week / baseline" for the same festival in past years, aligned by the festival date and not by the calendar week.
4. Compare this year's ratio to the past ratios. If it is inside the range, call it seasonal.
5. Layer the cricket effect: look at the hours of match time versus normal hours (traffic drops during play and rises at breaks).
6. Agree an alert rule with the PM: alert only when the ratio is below the seasonal range for two consecutive days, or when the drop is in segments that festivals do not explain.

**Metrics:**
- Event-week ratio = DAU in the event week / mean DAU of the same weekdays in the 4 prior weeks.
- Excess drop = this year's ratio - mean of past ratios (in points).
- z-score = excess drop / standard deviation of past ratios (with 3 years it is rough, so I also check the range).
- Guardrail: next-week recovery. A seasonal dip rebounds. A real loss does not.

**Risks:**
- Using last year's calendar week for a lunar festival.
- Growth: compare ratios, not raw counts.
- Very few past years, so the standard deviation is fragile.
- Declaring "seasonal" and never checking that DAU recovers.

**What the interviewer scores:**
- Strong: aligns on the festival, the same weekday and uses ratios. Weak: compares to last week or the same calendar week last year.
- Strong: gives a rule for the alert (range, two days, recovery). Weak: "I will wait and see".
- Strong: separates festival and cricket effects. Weak: lumps all causes into one.

**Example:** (illustrative numbers) Baseline DAU this year is 10.0 million and the festival week shows 9.4 million, a 6% fall, ratio 0.94. In the three earlier years the same festival gave ratios 0.950, 0.940 and 0.955 (mean 0.9483, standard deviation 0.0076). This year is 0.83 points below the mean, z about -1.1, and inside the past range.
- Weak: "DAU fell 6%, raise the alert."
- Strong: "Past festivals fell between 4.5% and 6%, we fell 6%, which is inside that range. No alert now. I will alert if DAU has not recovered to within 1% of baseline by the next Monday."

**Code:**
```python
# Q25 festival-week DAU: compare with the same festival in past years (illustrative numbers)
import statistics as st
# ratio = DAU in festival week / DAU baseline (average of the same weekday over the 4 prior weeks)
past = {"year-1": 0.950, "year-2": 0.940, "year-3": 0.955}
this_year = round(9.4 / 10.0, 4)
vals = list(past.values())
mean, sd = st.mean(vals), st.stdev(vals)
print("past ratios:", vals)
print("mean:", round(mean, 4), "sd:", round(sd, 4))
print("this year ratio:", this_year, " drop:", round(1 - this_year, 3))
excess = this_year - mean
z = excess / sd
print("excess vs seasonal mean (pts):", round(excess * 100, 2), " z:", round(z, 2))
inside_range = min(vals) <= this_year <= max(vals)
print("inside past range:", inside_range)
# calendar-week comparison (wrong): same ISO week last year, festival fell in another week
print("a plain week-over-week view calls it a drop of", round((1 - this_year) * 100, 1), "pts")
assert round(mean, 4) == 0.9483 and round(sd, 4) == 0.0076
assert round(excess * 100, 2) == -0.83 and round(z, 2) == -1.09
assert inside_range
```

**Output (my run):**
```text
past ratios: [0.95, 0.94, 0.955]
mean: 0.9483 sd: 0.0076
this year ratio: 0.94  drop: 0.06
excess vs seasonal mean (pts): -0.83  z: -1.09
inside past range: True
a plain week-over-week view calls it a drop of 6.0 pts
```

**Follow-ups:**
- What if there are only two prior years? Say the estimate is rough, use the range, and lean on segment checks.
- How do you automate it? A baseline model with weekday and holiday terms and an alert on the residual. Q44 of this part covers building an alert baseline.

**Common mistakes:** Comparing to the previous week. Using calendar weeks for moving festivals. Using raw counts instead of ratios. Raising an alert with no recovery check.

### Q26 ⭐⭐ 🟡 New-user retention looks worse this month, but marketing shifted spend from organic and referral to paid social. Explain how channel mix can lower blended retention without any product change, and how you would report retention fairly across the mix shift.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
**Say this first (1 line):** Blended retention is a weighted average of channel retentions, so when marketing buys more low-retention paid users the blend falls even if every channel improved, and I would report retention by channel plus a mix-standardised number.

**Clarifying questions:**
- How are channels defined, and has attribution changed? A new attribution rule can move users between channels without any real change.
- What did spend shift look like (share of new users by channel)? I need the mix before and after.
- Which retention day or window is being used (day 7, day 30)? The effect size depends on it.
- Has the product or onboarding changed in the same month? I need to rule out a true product effect.
- What is the cost per signup per channel? Lower retention may still be fine if the user is cheap.

**Approach:**
1. Split new-user retention by channel for both months.
2. Compute the mix: share of signups by channel each month.
3. Decompose the change in blended retention into a mix effect (the shares moved) and a rate effect (the channel retentions moved).
4. Standardise: take this month's channel retentions and weight them with last month's mix. That is the fair like-for-like number.
5. Go below channel when needed: campaign, creative, geography and device, because paid social is itself a mix.
6. Report retained users per rupee spent, so marketing and product read the same number.

**Metrics:**
- Channel D7 retention = users in the channel active on day 7 / signups in the channel.
- Blended D7 = sum over channels of (share of signups x channel D7).
- Mix effect = blended this month - blended at last month's mix.
- Rate effect = blended at last month's mix - blended last month.
- Cost per D7-retained user = spend / retained users.
- Guardrail: signup volume, so we do not trade volume for a nicer-looking rate.

**Risks:**
- Simpson's paradox: every channel improves but the total falls (the same pattern as Q11 of this part).
- The mix standardisation hides that paid users are weaker. Say that it is a like-for-like view, not a statement that the new mix is fine.
- Small channels give noisy rates.
- A channel's quality can drift as spend scales (the marginal paid user is worse than the average).

**What the interviewer scores:**
- Strong: decomposes into mix and rate with numbers. Weak: says "check segments".
- Strong: proposes the standardised metric and a cost-per-retained user. Weak: asks marketing to stop paid.
- Strong: notes marginal versus average quality. Weak: treats a channel as a single fixed quality.

**Example:** (illustrative numbers) Last month: 60% organic and referral at 30.0% D7, 40% paid social at 12.0%, blended 22.8%. This month: 40% organic at 30.5% and 60% paid at 12.5%, blended 19.7%. Blended fell 3.1 points. Mix effect is -3.6 points, rate effect is +0.5 points. At last month's mix, this month would be 23.3%.
- Weak: "Retention fell 3 points, onboarding is broken."
- Strong: "Both channels got slightly better. The fall is a mix effect of 3.6 points. Like-for-like retention is up 0.5 points. The real question for marketing is cost per retained user: at Rs 250 a signup and 12.5% retention, paid costs Rs 2,000 per D7-retained user."

**Code:**
```python
# Q26 channel mix and blended D7 retention (illustrative numbers)
last = {"organic+referral": (0.60, 0.300), "paid social": (0.40, 0.120)}   # (share of signups, D7 retention)
this = {"organic+referral": (0.40, 0.305), "paid social": (0.60, 0.125)}

def blend(d):
    return sum(s * r for s, r in d.values())

b_last, b_this = blend(last), blend(this)
print("blended last:", round(b_last, 4), " blended this:", round(b_this, 4), " change pts:", round((b_this - b_last) * 100, 2))
# standardise: this month's channel rates at last month's mix
std = sum(last[k][0] * this[k][1] for k in last)
print("this month at last month's mix:", round(std, 4), " change pts:", round((std - b_last) * 100, 2))
mix_effect = b_this - std
rate_effect = std - b_last
print("mix effect pts:", round(mix_effect * 100, 2), " rate effect pts:", round(rate_effect * 100, 2))
assert round(b_last, 3) == 0.228 and round(b_this, 3) == 0.197
assert round(std, 3) == 0.233
assert abs(mix_effect + rate_effect - (b_this - b_last)) < 1e-12
assert round(mix_effect * 100, 2) == -3.6 and round(rate_effect * 100, 2) == 0.5
assert all(this[k][1] > last[k][1] for k in last)   # every channel improved
# cost lens: retained users per Rs 100k spend (paid CAC Rs 250 per signup, organic costs 0) -> only paid is bought
paid_cac = 250
paid_signups = 100_000 / paid_cac
retained_per_100k = paid_signups * this["paid social"][1]
print("paid signups per Rs 100k:", paid_signups, " D7-retained:", retained_per_100k, " Rs per D7-retained:", 100_000 / retained_per_100k)
assert paid_signups == 400 and retained_per_100k == 50 and 100_000 / retained_per_100k == 2000
```

**Output (my run):**
```text
blended last: 0.228  blended this: 0.197  change pts: -3.1
this month at last month's mix: 0.233  change pts: 0.5
mix effect pts: -3.6  rate effect pts: 0.5
paid signups per Rs 100k: 400.0  D7-retained: 50.0  Rs per D7-retained: 2000.0
```

**Follow-ups:**
- How does this differ from Q11? Same arithmetic (weights shift), different setting: there it is traffic by device, here it is signups by channel.
- What if paid retention is lower but the CAC is low? Use contribution per spend, not retention alone.

**Common mistakes:** Reading the blended number as a product failure. Reporting only the average. Showing the standardised number without saying what it hides.

### Q27 ⭐⭐ 🟡 After a new OS release, DAU is down 5% only on iOS and only for users on the latest OS version. Describe the breakdowns, the logs and the checks you would use to decide between a real engagement loss and a tracking break, and who you would loop in.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** A drop confined to one OS version right after the release smells like a tracking break, so I would first size the segment, then check a second source that does not use the client event, and only then talk about real engagement loss.

**Clarifying questions:**
- Is "5%" of total DAU, of iOS DAU, or of the segment? The three readings imply very different segment drops (see the example).
- How is DAU defined: an app-open event, a foreground session, or any authenticated call? It tells me what could stop firing.
- Did our own app release go out around the same time, or only the OS update? A bug in our SDK on the new OS is the usual suspect.
- Do we have a server-side active measure (API calls, push delivery, orders)? That is the independent source.
- Are crashes, app store ratings and support tickets moving? They tell me about real user pain.

**Approach:**
1. Size it: how many users are in the segment and how much of the total drop would the segment have to explain?
2. Break down by OS version (latest, previous), app version, device model, country and time of day. A break that follows the OS version and not the app version points to the OS.
3. Compare client events with a server-side measure for the same users. If client DAU falls but backend DAU does not, events are being lost.
4. Look at the raw logs: event counts per user, session start events, the SDK init event, the error rate of the analytics endpoint, new-OS user-agent strings that a parser might drop.
5. Check real-engagement signals: orders, push open rates, crashes and ratings for that segment.
6. Loop in the mobile engineers, the analytics-SDK owner, and QA. If it is real, product and the app-store team.
7. Fix: patch the SDK or parser, then backfill if the raw events exist, and annotate the dashboard.

**Metrics:**
- Segment DAU change = DAU(segment, after) / DAU(segment, before) - 1.
- Client/backend ratio = users with the client event / users with any backend call, same segment and day.
- Event-loss indicator: events per active user and the share of backend-active users with zero client events.
- Guardrails: crash-free sessions, orders in the segment, push delivery rate.

**Risks:**
- Real causes can overlap, for example a crash on the new OS that is a true loss.
- Backend activity can include background syncs, so check that it is user-driven.
- Fixing the tracking and forgetting to restate the past dashboard.

**What the interviewer scores:**
- Strong: does the sizing sum first, then names an independent source. Weak: begins with "run a survey".
- Strong: separates a client-event break from a real loss with a concrete ratio. Weak: argues from intuition.
- Strong: names the people and the fix with backfill. Weak: stops at "find the cause".

**Example:** (illustrative numbers) Total DAU is 10 million, iOS 4 million, latest-OS users 1.2 million. If total DAU is down 5% (500,000 users) and everything sits in the segment, the segment would have fallen 42%, which real engagement almost never does. If the 5% is of iOS DAU, the segment fell 17%. If the segment itself is down 5%, that is 60,000 users and only 0.6% of total DAU. Second source: client DAU in the segment went from 1,200,000 to 1,140,000 (-5%) while backend DAU went from 1,260,000 to 1,257,000 (-0.2%), so the client/backend ratio fell from 0.952 to 0.907.
- Weak: "iOS users on the new OS are losing interest."
- Strong: "Backend activity is flat and the client ratio fell, so events are being lost for that OS. I would ask mobile engineering about the SDK on the new OS."

**Code:**
```python
# Q27 sanity check: how big would the segment loss have to be? (illustrative numbers)
total_dau = 10_000_000
ios_dau = 4_000_000
latest_os_dau = 1_200_000        # iOS users on the newest OS, before the drop

# reading A: total DAU is down 5% and all of it sits in the latest-OS segment
lost_A = 0.05 * total_dau
seg_drop_A = lost_A / latest_os_dau
# reading B: iOS DAU down 5%, all of it in the segment
lost_B = 0.05 * ios_dau
seg_drop_B = lost_B / latest_os_dau
# reading C: the segment itself is down 5%
lost_C = 0.05 * latest_os_dau
print("A lost users:", lost_A, " implied segment drop:", round(seg_drop_A, 3))
print("B lost users:", lost_B, " implied segment drop:", round(seg_drop_B, 3))
print("C lost users:", lost_C, " share of total DAU:", lost_C / total_dau)
assert lost_A == 500_000 and round(seg_drop_A, 3) == 0.417
assert lost_B == 200_000 and round(seg_drop_B, 3) == 0.167
assert lost_C == 60_000 and lost_C / total_dau == 0.006

# cross-check with a second source: backend active users (any authenticated API call) in the same segment
client_event_dau_before, client_event_dau_after = 1_200_000, 1_140_000   # app-open event
backend_dau_before, backend_dau_after = 1_260_000, 1_257_000             # server logs
ratio_before = client_event_dau_before / backend_dau_before
ratio_after = client_event_dau_after / backend_dau_after
print("client/backend ratio before:", round(ratio_before, 3), " after:", round(ratio_after, 3))
print("client DAU change:", round(client_event_dau_after / client_event_dau_before - 1, 3),
      " backend DAU change:", round(backend_dau_after / backend_dau_before - 1, 4))
assert round(ratio_before, 3) == 0.952 and round(ratio_after, 3) == 0.907
assert round(client_event_dau_after / client_event_dau_before - 1, 3) == -0.05
assert round(backend_dau_after / backend_dau_before - 1, 4) == -0.0024
# a falling client/backend ratio with flat backend points to lost events, not lost users
```

**Output (my run):**
```text
A lost users: 500000.0  implied segment drop: 0.417
B lost users: 200000.0  implied segment drop: 0.167
C lost users: 60000.0  share of total DAU: 0.006
client/backend ratio before: 0.952  after: 0.907
client DAU change: -0.05  backend DAU change: -0.0024
```

**Follow-ups:**
- What if backend DAU also falls? Then treat it as real: look at crashes, a launch failure, push token loss or an incompatible API call.
- How would you prevent it next time? Test the analytics SDK on beta OS versions and alert on the client/backend ratio per segment.

**Common mistakes:** Not sizing the segment. Trusting one data source. Assuming it is real because the dashboard says so. Forgetting to annotate and backfill.

### Q28 ⭐⭐ 🟡 A delivery fee change raised the fee from Rs 20 to Rs 30 on small orders. Orders fell 6%, but revenue rose 4%. Say how you would judge whether the change was good, what guardrails and time horizon you would use, and which customers you would look at separately.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
**Say this first (1 line):** I would judge the fee change by the contribution it adds after the orders it loses, over several weeks and including the customers who then stop ordering larger baskets, not by the revenue line alone.

**Clarifying questions:**
- What does "revenue" mean here: fee revenue only, or total platform revenue (commission plus fees)? The prompt does not say, and it changes the sums.
- Which orders are "small" (a threshold) and what share are they? The effect lives there.
- What does a small order cost us to deliver? Revenue up on a loss-making order is not the same as profit.
- Was the change tested with a control or rolled out everywhere? Without control, season and promotions are confounded.
- Which customers are price-sensitive: new users, low-frequency users, users who always order small?

**Approach:**
1. Write the economics per order: commission + fee - delivery cost - discounts = contribution.
2. Compare treated and control, or against a pre-trend, for orders, revenue and contribution.
3. Look for substitution: do customers merge small orders into bigger ones (good), order less (bad), or move to a competitor (worse)?
4. Check the halo: do the same customers reduce large orders or visits too?
5. Cut by customer type: new versus repeat, high versus low frequency, city.
6. Extend the horizon: 4 to 8 weeks, so the first reaction does not hide the lasting one.
7. Decide with a break-even: how many large orders can we lose before the gain is gone?

**Metrics:**
- Orders per active user per week = orders / users active that week.
- Contribution per order = commission + fee - delivery cost - discount.
- Total contribution = sum over orders of contribution (the decision metric).
- Small-order share and average basket = share of orders below the threshold; AOV.
- Guardrails: weekly active users, repeat rate, complaints about fees, app rating.

**Risks:**
- Revenue up on fewer orders can still mean fewer customers a month later.
- Fee revenue vs total revenue confusion in the quote.
- Mix: if the lost orders are low-margin ones, the picture improves, which is fine, but say so.
- Short horizon: the harm to repeat behaviour appears later.

**What the interviewer scores:**
- Strong: converts the prompt to contribution per order and a break-even. Weak: says "revenue went up, ship".
- Strong: names a halo check and segment cuts. Weak: looks at one average.
- Strong: asks what revenue means. Weak: assumes.

**Example:** (illustrative numbers) 100,000 weekly orders: 60,000 small (basket Rs 150, commission 20% = Rs 30, fee Rs 20) and 40,000 large (basket Rs 375, commission Rs 75, no fee). Revenue is Rs 60,00,000. After the change small orders drop 10% to 54,000, so total orders fall 6% to 94,000 and revenue becomes Rs 62,40,000, up 4%. With a rider cost of Rs 60 per small order, small-order contribution moves from -Rs 6,00,000 to Rs 0. The Rs 2,40,000 gain would be wiped out if large orders fell by 3,200, that is 8% of them.
- Weak: "Orders fell 6%, so it is bad."
- Strong: "Revenue is up 4% and small-order contribution went from negative to zero. I would ship if the large-order loss stays below 8% and repeat rate holds, and I would watch new users separately."

**Code:**
```python
# Q28 delivery fee Rs 20 -> Rs 30 on small orders (illustrative numbers)
small0, large0 = 60_000, 40_000        # weekly orders before
small_aov, large_aov = 150, 375
commission = 0.20
fee0, fee1 = 20, 30
small1 = 54_000                        # small orders fall 10%; large unchanged -> total falls 6%
large1 = 40_000

def rev(small, large, fee):
    return small * (small_aov * commission + fee) + large * (large_aov * commission)

r0, r1 = rev(small0, large0, fee0), rev(small1, large1, fee1)
print("orders before/after:", small0 + large0, small1 + large1, " change:", round((small1 + large1) / (small0 + large0) - 1, 3))
print("revenue before/after:", r0, r1, " change:", round(r1 / r0 - 1, 3))
assert small0 + large0 == 100_000 and small1 + large1 == 94_000
assert r0 == 6_000_000 and r1 == 6_240_000 and round(r1 / r0 - 1, 3) == 0.04

# contribution after a rider cost of Rs 60 per small order
rider = 60
c0 = small0 * (small_aov * commission + fee0 - rider)
c1 = small1 * (small_aov * commission + fee1 - rider)
print("small-order contribution before/after (Rs):", c0, c1)
assert c0 == -600_000 and c1 == 0

# halo: how many large orders can be lost before the revenue gain is gone?
gain = r1 - r0
large_order_rev = large_aov * commission
breakeven_orders = gain / large_order_rev
print("revenue gain:", gain, " breakeven lost large orders:", breakeven_orders, " as share of large:", breakeven_orders / large0)
assert gain == 240_000 and breakeven_orders == 3200 and breakeven_orders / large0 == 0.08
```

**Output (my run):**
```text
orders before/after: 100000 94000  change: -0.06
revenue before/after: 6000000.0 6240000.0  change: 0.04
small-order contribution before/after (Rs): -600000.0 0.0
revenue gain: 240000.0  breakeven lost large orders: 3200.0  as share of large: 0.08
```

**Follow-ups:**
- What if new users react much more? Exempt them for the first orders and measure again.
- How would you test? A holdout of cities or users at the old fee, so seasonality cancels.

**Common mistakes:** Treating revenue as profit. Ignoring the delivery cost. One-week horizon. Averaging all customers together.

### Q29 ⭐⭐ 🟡 Subscription churn rose from 3% to 4.5% a month after a price increase. Describe how you would find which segments churned, tell price effects from the usual seasonality or a product issue, and estimate the revenue impact over the next year.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** I would isolate the price effect with a comparison group that did not get the new price, find who churned by segment, and then model the year ahead two ways, because higher price with higher churn can raise 12-month revenue and still lower lifetime value.

**Clarifying questions:**
- Did everyone get the price increase on the same date, or was there a control group or grandfathered plan? A control is the only clean way to separate price from season.
- Is the 3% to 4.5% churn voluntary cancellation, failed payments or both? Payment failures have a different fix.
- What did the competitor and the product do that month? A rival promotion or an outage can look like a price effect.
- How is churn measured (share of subscribers at month start who left in the month)? The base matters.
- Was the increase announced in advance? Notice period changes when the churn shows up.

**Approach:**
1. Check the data first: same churn definition, no billing glitch, no change in how cancellations are logged.
2. Find who churned: by plan, tenure, price paid, region, payment method, usage level and cancellation reason. Price-driven churn usually concentrates in low-usage and short-tenure users.
3. Separate price from season: use difference-in-differences against a control (for example a region or plan still on the old price) and the same month in previous years.
4. Check for a product issue: usage, support tickets and ratings among churned users before they left.
5. Estimate the revenue impact: run the 12-month revenue under old price, new price with persistent churn, and new price with churn that fades.
6. Also compute the lifetime view and the break-even churn.

**Metrics:**
- Monthly churn = subscribers who cancelled in the month / subscribers at the start of the month.
- Price effect on churn = (treated after - treated before) - (control after - control before).
- 12-month revenue = sum over months of active subscribers x price (closed cohort, no new adds).
- Simple lifetime value = price / monthly churn.
- Guardrails: new subscriber volume, downgrades to a cheaper plan, support contacts.

**Risks:**
- The control group may differ from the treated group (for example by region), which biases the difference-in-differences.
- A closed cohort leaves out new subscribers, who also respond to the higher price.
- Short-run churn spikes can be pull-forward of cancellations that would have come later.
- Revenue over 12 months looks good while the lifetime value falls.

**What the interviewer scores:**
- Strong: separates price from season with a control and a number. Weak: says "churn went up because of price".
- Strong: gives a revenue model with scenarios and a break-even. Weak: a single guess.
- Strong: raises lifetime value versus 12-month revenue. Weak: stops at the short term.

**Example:** (illustrative numbers) 100,000 subscribers, price Rs 199 to Rs 249, churn 3.0% to 4.5%. A control region stayed on Rs 199 and moved 3.0% to 3.4%, so the price effect is 1.5 - 0.4 = 1.1 points. Over 12 months the old plan earns Rs 20.31 crore (a closed cohort). The new price with 4.5% persistent churn earns Rs 23.49 crore (+15.7%), with churn fading back to 3% after 3 months Rs 24.47 crore (+20.5%). The break-even constant churn at the new price is about 7.4% a month. The lifetime value per subscriber is Rs 199 / 0.03 = Rs 6,633 before and Rs 249 / 0.045 = Rs 5,533 after, 16.6% lower.
- Weak: "Churn rose 50%, the price increase failed."
- Strong: "About 1.1 of the 1.5 points are price. Revenue over a year is up even if the churn persists, but lifetime value is down about 17%, so I would check if segments with high usage tolerate the price and the low-usage segment does not."

**Code:**
```python
# Q29 price increase and churn: DiD and 12-month revenue (illustrative numbers)
subs0 = 100_000
old_price, new_price = 199, 249
# difference-in-differences: treated users saw the new price, a control region still on old price
treated_before, treated_after = 0.030, 0.045
control_before, control_after = 0.030, 0.034
did = (treated_after - treated_before) - (control_after - control_before)
print("raw churn change pts:", round((treated_after - treated_before) * 100, 2), " DiD price effect pts:", round(did * 100, 2))
assert round(did * 100, 2) == 1.10

def year_revenue(price, churn_by_month, subs=subs0):
    total = 0.0
    for c in churn_by_month:
        total += subs * price          # revenue from subscribers active this month
        subs *= (1 - c)                # churn at month end (closed cohort, no new adds)
    return total

old = year_revenue(old_price, [0.03] * 12)
persist = year_revenue(new_price, [0.045] * 12)
# price effect only: churn at 4.5% for 3 months then back to 3%
revert = year_revenue(new_price, [0.045] * 3 + [0.03] * 9)
# DiD view: only 3.0% + 1.1 pts = 4.1% is due to price; the rest is seasonality that hits old price too
did_view = year_revenue(new_price, [0.041] * 12)
old_season = year_revenue(old_price, [0.034] * 12)
for name, v in [("old price, 3.0% churn", old), ("new price, 4.5% persists", persist),
                ("new price, 4.5% for 3 months then 3.0%", revert),
                ("new price, 4.1% (DiD price effect)", did_view), ("old price, 3.4% (seasonal baseline)", old_season)]:
    print(f"{name:42} Rs {v/1e6:8.2f} m   vs old {v/old - 1:+.1%}")
assert persist > old and revert > persist and did_view > persist
assert round(persist / old - 1, 3) == 0.157 and round(revert / old - 1, 3) == 0.205
assert round(did_view / old - 1, 3) == 0.181 and round(old_season / old - 1, 3) == -0.021
# breakeven constant monthly churn at which 12-month revenue equals the old plan
lo, hi = 0.03, 0.30
for _ in range(60):
    mid = (lo + hi) / 2
    if year_revenue(new_price, [mid] * 12) > old:
        lo = mid
    else:
        hi = mid
print("breakeven monthly churn at new price:", round(lo, 4))
assert 0.07 < lo < 0.10

# lifetime view (simple geometric lifetime = price / churn, per subscriber, undiscounted)
ltv_old, ltv_new = old_price / 0.03, new_price / 0.045
print("LTV old:", round(ltv_old), " LTV new:", round(ltv_new), " change:", round(ltv_new / ltv_old - 1, 3))
assert round(ltv_old) == 6633 and round(ltv_new) == 5533 and round(ltv_new / ltv_old - 1, 3) == -0.166
```

**Output (my run):**
```text
raw churn change pts: 1.5  DiD price effect pts: 1.1
old price, 3.0% churn                      Rs   203.08 m   vs old +0.0%
new price, 4.5% persists                   Rs   234.89 m   vs old +15.7%
new price, 4.5% for 3 months then 3.0%     Rs   244.72 m   vs old +20.5%
new price, 4.1% (DiD price effect)         Rs   239.83 m   vs old +18.1%
old price, 3.4% (seasonal baseline)        Rs   198.84 m   vs old -2.1%
breakeven monthly churn at new price: 0.0737
LTV old: 6633  LTV new: 5533  change: -0.166
```

**Follow-ups:**
- How would you test a future price change? A randomised price test on a share of new users, with 90-day churn as a guardrail. Book 1 Part 10 Q19 (cannot randomize) covers the options when you cannot randomise.
- What would you add to the model? New subscribers, plan downgrades, discounting for win-backs and discounting future revenue.

**Common mistakes:** Reading raw churn change as the price effect. Ignoring season. Using only 12-month revenue. Forgetting the tenure mix of the churners.

### Q30 ⭐⭐ 🟡 In a two-sided marketplace, new seller listings grew 25% this quarter but buyer conversion fell from 5% to 4.2%. Explain the possible reasons, how you would tell a supply-quality dilution from a search or ranking problem, and which metrics you would add to monitor both sides.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** More supply and lower conversion can come from weaker new listings diluting the results or from search and ranking not handling the larger catalogue, and I would tell them apart by comparing conversion for sessions that mostly show old listings with sessions that mostly show new ones.

**Clarifying questions:**
- Where did the 25% more listings come from (new sellers, existing sellers listing more, a bulk upload)? Quality differs a lot by source.
- Did search, ranking or the filters change this quarter? A ranking change is the other main suspect.
- Is the conversion drop everywhere or in some categories and cities? Dilution and ranking problems show different footprints.
- Did buyer traffic mix change (more new buyers, more paid traffic)? Buyer mix can lower conversion on its own.
- How is conversion defined (sessions with a search that end in an order)? The denominator matters.

**Approach:**
1. Check data and the buyer mix first, so I am not chasing the supply when the cause is traffic.
2. Segment sessions by how much of the top results are new listings.
3. Compare conversion in those segments. Dilution says: old-heavy sessions convert as before and new-heavy sessions convert badly. A search or ranking problem says: conversion fell in all segments, including old-heavy ones.
4. Look at listing quality: photo count, price versus category median, response time, cancellation rate, duplicate listings.
5. Look at search itself: zero-result rate, click-through on the first page, depth of scroll, query reformulation rate.
6. Look at the seller side: orders per listing and the share of listings with no order in 30 days.
7. Decide the action: quality gates for new listings, a ranking penalty for low-quality supply, or search fixes.

**Metrics:**
- Buyer conversion = sessions with an order / sessions with a search.
- Conversion by exposure = the same, within sessions grouped by share of new listings in the top 10.
- Orders per listing = orders / active listings (supply health).
- Search success = sessions with a click on a result / sessions with a search; zero-result rate.
- Guardrails: seller churn, cancellation rate, buyer repeat rate.

**Risks:**
- Selection: sessions with many new listings may be different sessions (broader queries).
- Both causes can be present, so the segment table can show both.
- New listings may need a few weeks to attract orders, so "low conversion" might be a cold-start effect.

**What the interviewer scores:**
- Strong: gives a test that separates the two stories. Weak: lists reasons.
- Strong: names metrics for both sides of the marketplace. Weak: only buyer conversion.
- Strong: proposes an action tied to each cause. Weak: "improve quality".

**Example:** (illustrative numbers) 1,000,000 sessions. Before, conversion 5% (50,000 orders). After, 42,000 orders (4.2%). Suppose 75% of sessions are old-heavy and 25% new-heavy. World A (dilution): old-heavy 5.0%, new-heavy 1.8%, blended 0.75 x 5.0 + 0.25 x 1.8 = 4.2%. World B (ranking or search problem): both segments 4.2%. The blended number is 4.2% in both worlds, and the segment table tells them apart. Supply side: orders per listing fell from 0.50 to 0.336 (-33%).
- Weak: "More listings is good, conversion fell, it is noise."
- Strong: "The blended 4.2% is the same in both stories, so I split by new-listing exposure. Old-heavy sessions at 5.0% mean dilution, so I would gate quality. If they are at 4.2% too, I would look at ranking and search."

**Code:**
```python
# Q30 marketplace: listings +25%, buyer conversion 5.0% -> 4.2% (illustrative numbers)
sessions = 1_000_000
share_old_heavy, share_new_heavy = 0.75, 0.25   # sessions whose top results are mostly old / mostly new listings

worlds = {
    "A: quality dilution":  {"old-heavy": 0.050, "new-heavy": 0.018},
    "B: ranking/search bug": {"old-heavy": 0.042, "new-heavy": 0.042},
}
for name, w in worlds.items():
    blended = share_old_heavy * w["old-heavy"] + share_new_heavy * w["new-heavy"]
    print(f"{name:24} old-heavy {w['old-heavy']:.1%}  new-heavy {w['new-heavy']:.1%}  blended {blended:.2%}  orders {blended*sessions:,.0f}")
    assert round(blended, 4) == 0.042
    assert round(blended * sessions) == 42_000
print("orders before:", 0.05 * sessions)
assert 0.05 * sessions == 50_000
# supply side: listings +25% -> avg listings per query result slot competing; sellers' orders per listing
orders_before, orders_after = 50_000, 42_000
listings_before, listings_after = 100_000, 125_000
opl_b, opl_a = orders_before / listings_before, orders_after / listings_after
print("orders per listing before/after:", opl_b, round(opl_a, 3), " change:", round(opl_a / opl_b - 1, 3))
assert opl_b == 0.5 and round(opl_a, 3) == 0.336 and round(opl_a / opl_b - 1, 3) == -0.328
```

**Output (my run):**
```text
A: quality dilution      old-heavy 5.0%  new-heavy 1.8%  blended 4.20%  orders 42,000
B: ranking/search bug    old-heavy 4.2%  new-heavy 4.2%  blended 4.20%  orders 42,000
orders before: 50000.0
orders per listing before/after: 0.5 0.336  change: -0.328
```

**Follow-ups:**
- How would you confirm causation? A small experiment that ranks new listings lower or applies a quality score for a share of traffic. Book 1 Part 10 Q13 (primary metric up, guardrail down) covers weighing the two sides.
- What would you monitor going forward? Conversion by listing age and quality tier, plus orders per listing.

**Common mistakes:** Blaming noise. One blended conversion number. Monitoring only the buyer side. Not asking where the new supply came from.

### Q31 ⭐⭐ 🟡 A new ETA model improved ETA accuracy by 15%, but orders in the treatment group are 2% lower. Explain how a better prediction can reduce orders, what you would look at by segment, and how you would pick the metric that decides the launch.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** A more accurate ETA can reduce orders because the old one was optimistic: honest, longer estimates lose some orders at checkout but remove late deliveries, cancellations and bad experiences, so I would decide on delivered orders, repeat rate and satisfaction over several weeks, not on checkout orders alone.

**Clarifying questions:**
- What does "accuracy improved by 15%" mean (mean absolute error down 15%, share within 5 minutes, bias)? The prompt does not say, and a lower error can hide a bias shift.
- Did the displayed ETA go up on average? That is the likely mechanism.
- Is the 2% drop in orders placed or in delivered orders? Cancellations change the picture.
- Which segments are affected (short versus long distance, peak versus off-peak, new versus repeat users)?
- How long did the test run? Repeat behaviour needs weeks.

**Approach:**
1. Check the experiment is clean (sample ratio, same exposure period).
2. Split the accuracy gain into error and bias: did the shown ETA get longer on average?
3. Look at the funnel: from ETA view to checkout, by ETA bucket shown. Orders fall where the shown ETA moved up.
4. Follow what happens after checkout: late-delivery rate, cancellations, refunds, complaints, rating.
5. Look at repeat orders over the next 4 to 8 weeks per user.
6. Cut by segment: orders may fall mostly where the old ETA was most optimistic.
7. Pick the deciding metric: delivered orders per exposed user over several weeks (and contribution), with satisfaction and late rate as guardrails.

**Metrics:**
- ETA bias = mean (shown ETA - actual time).
- ETA MAE = mean of |shown ETA - actual time|.
- Late rate = orders delivered later than shown ETA + 5 minutes / delivered orders.
- Delivered orders per exposed user over 4 weeks.
- Guardrails: cancellation rate, refund rate, support contacts, repeat rate.

**Risks:**
- Accuracy is a model metric. The product metric is orders and satisfaction.
- Short test hides the repeat benefit.
- Segment mix: the loss may be in new users, who have no experience to correct for the optimistic ETA.

**What the interviewer scores:**
- Strong: gives the mechanism (honest ETA shown longer) and a test of it. Weak: "the model must be wrong".
- Strong: chooses a decision metric over a longer horizon. Weak: picks checkout orders.
- Strong: asks what accuracy means. Weak: takes it at face value.

**Example:** (illustrative numbers) 100,000 sessions, 30% convert. Average actual time is 30 minutes. Old ETA shown averaged 24 (bias -6), new 28 (bias -2). Assume each extra displayed minute lowers conversion by 0.5% relative: 4 minutes x 0.5% = 2%, so orders go from 30,000 to 29,400. Late rate falls from 30% to 12%. If late orders cancel 10% of the time and on-time orders 2%, the cancellation rate falls from 4.4% to 2.96%, so delivered orders are 28,680 before and 28,530 after, only 0.5% lower. A 0.5% repeat-purchase gain would close it. Mean absolute error 6.0 to 5.1 minutes is the 15%.
- Weak: "Orders are down 2%, roll back the model."
- Strong: "Orders placed are down 2% because the promise got honest. Delivered orders are down 0.5% and cancellations fell by a third. I would hold the decision for a 4-week repeat and satisfaction read, and consider showing a range."

**Code:**
```python
# Q31 better ETA, fewer orders (illustrative numbers)
sessions = 100_000
conv0 = 0.30
shown_old, shown_new = 24, 28      # average ETA shown, minutes
actual = 30                        # average actual delivery time, minutes
elasticity = -0.005                # relative drop in conversion per extra displayed minute (assumed)
conv1 = conv0 * (1 + elasticity * (shown_new - shown_old))
orders0, orders1 = sessions * conv0, sessions * conv1
print("bias old/new (min, shown - actual):", shown_old - actual, shown_new - actual)
print("orders before/after:", round(orders0), round(orders1), " change:", round(orders1 / orders0 - 1, 3))
assert round(orders0) == 30_000 and round(orders1) == 29_400 and round(orders1 / orders0 - 1, 3) == -0.02

late0, late1 = 0.30, 0.12          # share of orders delivered later than shown + 5 min
cancel_late, cancel_ontime = 0.10, 0.02
cr0 = late0 * cancel_late + (1 - late0) * cancel_ontime
cr1 = late1 * cancel_late + (1 - late1) * cancel_ontime
d0, d1 = orders0 * (1 - cr0), orders1 * (1 - cr1)
print("cancel rate before/after:", round(cr0, 4), round(cr1, 4))
print("delivered orders before/after:", round(d0), round(d1), " change:", round(d1 / d0 - 1, 4))
assert round(cr0, 3) == 0.044 and round(cr1, 4) == 0.0296
assert round(d0) == 28_680 and round(d1) == 28_530 and round(d1 / d0 - 1, 4) == -0.0052
# what repeat-rate gain from fewer late orders would turn delivered orders positive over 8 weeks?
repeat_uplift_needed = d0 / d1 - 1
print("delivered-order gain needed from repeat purchases:", round(repeat_uplift_needed, 4))
assert round(repeat_uplift_needed, 4) == 0.0053
# the "15% better accuracy" in the prompt, read as mean absolute error falling 15%
mae_old, mae_new = 6.0, 5.1
print("MAE change:", round(mae_new / mae_old - 1, 3))
assert round(mae_new / mae_old - 1, 3) == -0.15
```

**Output (my run):**
```text
bias old/new (min, shown - actual): -6 -2
orders before/after: 30000 29400  change: -0.02
cancel rate before/after: 0.044 0.0296
delivered orders before/after: 28680 28530  change: -0.0052
delivered-order gain needed from repeat purchases: 0.0053
MAE change: -0.15
```

**Follow-ups:**
- Could you keep accuracy and recover orders? Yes: speed up delivery, show a range, offer a cheaper slower option.
- Which metric decides the launch? The one tied to the goal over a long window, here delivered orders per user plus a satisfaction guardrail. See Q16 of this part for the same pattern with a ranking change.

**Common mistakes:** Treating model accuracy as the business goal. Reading placed orders only. Short test window. Not checking the shown-ETA shift.

### Q32 ⭐⭐ 🟡 Sessions per DAU jumped 20% overnight while DAU stayed flat. Explain which causes you would test (bots, a logging change, a new auto-refresh, a real engagement spike), and which two checks would settle it fastest.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Flat DAU with 20% more sessions per user overnight is more likely a definition or logging change than real behaviour, and two checks settle it: does the jump line up with an app or SDK version, and are actions or active time per DAU flat.

**Clarifying questions:**
- How is a session defined (timeout, foreground event) and did that change? A changed timeout splits one visit into more sessions.
- Did a release or SDK update go out that night? It would explain a step change.
- Is the jump uniform across platforms, versions and countries? Instrumentation changes are usually localised to a version.
- Did any feature with background refresh or auto-play ship? These create sessions with no user action.
- Is time spent or orders per user also up? Real engagement lifts them.

**Approach:**
1. Treat it as a measurement question first, since the change is overnight and DAU did not move.
2. Check the timeline against releases, SDK changes, config flags and the session-timeout setting.
3. Break sessions per DAU by platform, app version, country and new versus old users. A step change in one version is a logging cause.
4. Compare sessions with other measures per DAU: events per DAU, actions (orders, messages, plays) per DAU, total active time per DAU. If they are flat, sessions were split or inflated.
5. Look at session length and events per session: a fall in both with a rise in session count means splitting.
6. Look for bots and automation: very high session counts per user, identical timings, data-centre IPs, no touch events.
7. If real, find which feature drove it and check quality (is it good engagement or notification-driven opening).

**Metrics:**
- Sessions per DAU = sessions / daily active users.
- Events per DAU, actions per DAU and active time per DAU (independent of how sessions are cut).
- Events per session = events / sessions (falls when sessions split).
- Share of users above a high session-count threshold (bot indicator).
- Guardrails: DAU, retention, crash rate.

**Risks:**
- Several causes at once (a new refresh and a timeout change).
- Fixing only the dashboard and not warning the teams whose goals use sessions.
- Bot filtering removing real heavy users.

**What the interviewer scores:**
- Strong: names four causes and the two fastest checks. Weak: starts a long analysis plan.
- Strong: uses an independent measure (actions or time per DAU). Weak: relies on the same inflated metric.
- Strong: says what to do next either way. Weak: stops at diagnosis.

**Example:** (illustrative numbers) 5,000 simulated users, same events, seeded. Changing the timeout from 30 to 15 minutes raised sessions per user from 1.54 to 1.96 (+26.8%), the same order as the 20% in the prompt, while events per user stayed 18.91 and events per session dropped from 12.26 to 9.66.
- Weak: "Users are 20% more engaged, great."
- Strong: "DAU and actions per DAU are flat while events per session fell, which is what session splitting does. I will check the version and the timeout config before anyone celebrates."

**Code:**
```python
# Q32 sessions per DAU +20% with flat DAU: a session-timeout change splits sessions (seeded simulation)
import random
random.seed(7)
users = 5000
def make_events():
    ev = []
    t = random.uniform(8, 10) * 60.0            # minutes since midnight
    for _ in range(random.randint(8, 30)):      # events in the day
        ev.append(t)
        # most gaps are short; 3% are real breaks (35-120 min); 1.7% are mid gaps of 16-29 minutes
        r = random.random()
        if r < 0.03:
            t += random.uniform(35, 120)
        elif r < 0.047:
            t += random.uniform(16, 29)
        else:
            t += random.expovariate(1 / 3.0)
    return ev

data = [make_events() for _ in range(users)]

def sessions(events, timeout):
    n = 1
    for a, b in zip(events, events[1:]):
        if b - a > timeout:
            n += 1
    return n

s30 = sum(sessions(e, 30) for e in data) / users
s15 = sum(sessions(e, 15) for e in data) / users
events_per_user = sum(len(e) for e in data) / users
active_span30 = sum(e[-1] - e[0] for e in data) / users
print("users (DAU, unchanged):", users)
print("sessions per DAU, 30-min timeout:", round(s30, 2))
print("sessions per DAU, 15-min timeout:", round(s15, 2), " change:", round(s15 / s30 - 1, 3))
print("events per DAU (unchanged by the timeout):", round(events_per_user, 2))
print("events per session 30 vs 15:", round(events_per_user / s30, 2), round(events_per_user / s15, 2))
assert 1.15 < s15 / s30 < 1.30    # a pure definition change moves the ratio by roughly 20%
assert abs(events_per_user - sum(len(e) for e in data) / users) < 1e-9
# fastest check 2: events or orders per DAU is identical under both definitions
orders_proxy_30 = sum(len(e) for e in data)
orders_proxy_15 = sum(len(e) for e in data)
assert orders_proxy_30 == orders_proxy_15
```

**Output (my run):**
```text
users (DAU, unchanged): 5000
sessions per DAU, 30-min timeout: 1.54
sessions per DAU, 15-min timeout: 1.96  change: 0.268
events per DAU (unchanged by the timeout): 18.91
events per session 30 vs 15: 12.26 9.66
```

**Follow-ups:**
- The two checks again? One, split by app version and platform to see whether the step lines up with a release. Two, compare actions or active time per DAU, which do not depend on how sessions are cut.
- What if it is real? Then break down by feature and check retention and satisfaction, because refresh-driven opens are not value.

**Common mistakes:** Calling it engagement. Checking only sessions. Missing that the definition changed. No annotation on the dashboard.

### Q33 ⭐⭐ 🟡 A new onboarding flow lifts day-1 retention by 4 points, but day-30 retention is unchanged. Explain the likely story, how you would check for a novelty effect, and what you would recommend to the team that wants to ship it everywhere.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Day-1 up and day-30 flat usually means the new flow gets people through the first day (a reward, a nudge, a shorter path) without building a habit, so I would look at the full retention curve for a fade, check the effect by cohort week, and recommend a staged rollout with a long holdout, not shipping it everywhere as a retention win.

**Clarifying questions:**
- How many users per arm and how long has it run? The day-30 data must cover enough users and full weeks.
- What changed in the flow (incentive, fewer steps, forced permission prompts)? It points to the mechanism.
- What is the activation event that predicts value (first order, first message)? Day-1 return is only a proxy.
- Are there guardrails: uninstall rate, permission opt-in, support tickets, time to first value?
- Is the flow costly (rewards, extra engineering, notifications)? It changes the bar to ship.

**Approach:**
1. Draw the retention curve for both arms on days 1, 3, 7, 14, 30 and compute the gap with a confidence interval at each point.
2. A gap that shrinks smoothly to zero is consistent with a transient or novelty effect. A gap that stays is a lasting one.
3. Check the novelty and primacy pattern: compare the earliest-enrolled cohort with later ones, and look at repeat exposure within a user. Book 1 Part 10 Q8 covers the novelty effect and the primacy effect.
4. Ask what the 4 points are: users who return on day 1 and then leave. Check activation (first key action) and depth: did the extra returners do anything useful?
5. Segment by acquisition channel, platform and intent. The flow may help one group.
6. Check whether the day-30 result is "no effect" or "not enough data": the confidence interval says how large an effect it could still hide.
7. Recommend: do not ship to everyone as a retention win. Ship if it improves activation or cost with no harm, keep a long-term holdout to day 60 or 90, and iterate on what carries users from day 1 to the habit.

**Metrics:**
- Day-N retention = users in the arm active on day N / users in the arm that started onboarding.
- Gap at day N = treatment - control retention, with a 95% confidence interval from a two-proportion standard error.
- Activation rate = users completing the first key action within a set window / users starting onboarding.
- Guardrails: uninstall rate, permission opt-in, support contacts.

**Risks:**
- Reading "unchanged" as "no effect": the interval at day 30 is wide.
- Multiple days tested, so one significant day is not a finding. Q14 of Book 1 Part 10 (insignificant results) covers reading a null properly.
- Novelty versus true effect needs time, which the team does not want to spend.

**What the interviewer scores:**
- Strong: uses the curve, the interval and a mechanism. Weak: says "the flow is bad" or "ship it".
- Strong: separates "no effect" from "not enough data" with a number. Weak: reads the point estimate.
- Strong: a staged rollout and holdout. Weak: ship everywhere or kill it.

**Example:** (illustrative numbers) 20,000 users per arm. Retention control versus treatment: day 1 40% vs 44%, day 3 28% vs 30%, day 7 20% vs 21%, day 14 15% vs 15.5%, day 30 12% vs 12%. The gap runs 4.0, 2.0, 1.0, 0.5, 0.0 points, and the day-30 confidence interval is -0.64 to +0.64 points, so a gain of more than about 0.6 points is unlikely. Detecting a 1-point gain at day 30 would need about 17,166 users per arm for 80% power.
- Weak: "Day-1 retention is up 4 points, ship it."
- Strong: "The gap decays to zero by day 30 and the interval excludes a gain over 0.64 points, so this is not a habit lever. I would ship it only for the activation benefit, hold out 5% to day 90 and try to carry users from day 1 into week 2."

**Code:**
```python
# Q33 onboarding flow: day-1 up 4 pts, day-30 unchanged (illustrative numbers)
import math
n = 20_000                                       # users per arm
days = [1, 3, 7, 14, 30]
control = [0.40, 0.28, 0.20, 0.15, 0.12]
treat = [0.44, 0.30, 0.21, 0.155, 0.12]

def ci_diff(p1, p0, n):
    d = p1 - p0
    se = math.sqrt(p1 * (1 - p1) / n + p0 * (1 - p0) / n)
    return d, d - 1.96 * se, d + 1.96 * se

print("day  control treat  diff(pts)  95% CI (pts)")
rows = {}
for dday, c, t in zip(days, control, treat):
    d, lo, hi = ci_diff(t, c, n)
    rows[dday] = (d, lo, hi)
    print(f"{dday:>3}  {c:.3f}   {t:.3f}  {d*100:6.2f}    [{lo*100:5.2f}, {hi*100:5.2f}]")
d1, lo1, hi1 = rows[1]
d30, lo30, hi30 = rows[30]
assert round(d1 * 100, 2) == 4.0 and lo1 > 0
assert d30 == 0 and lo30 < 0 < hi30
print("day-30 half-width (pts):", round((hi30 - d30) * 100, 2))
assert round((hi30 - d30) * 100, 2) == 0.64
# diffs shrink with time -> consistent with a transient effect
diffs = [rows[d][0] for d in days]
assert all(a >= b for a, b in zip(diffs, diffs[1:]))
# users per arm needed to detect a 1-point day-30 gain (80% power, alpha 0.05, p=0.12)
z_a, z_b = 1.96, 0.8416
p0, p1 = 0.12, 0.13
n_need = ((z_a + z_b) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1))) / (p1 - p0) ** 2
print("users per arm to detect +1 pt at day 30:", math.ceil(n_need))
assert math.ceil(n_need) == 17_166
```

**Output (my run):**
```text
day  control treat  diff(pts)  95% CI (pts)
  1  0.400   0.440    4.00    [ 3.03,  4.97]
  3  0.280   0.300    2.00    [ 1.11,  2.89]
  7  0.200   0.210    1.00    [ 0.21,  1.79]
 14  0.150   0.155    0.50    [-0.20,  1.20]
 30  0.120   0.120    0.00    [-0.64,  0.64]
day-30 half-width (pts): 0.64
users per arm to detect +1 pt at day 30: 17166
```

**Follow-ups:**
- Could day-1 retention still matter? Yes, if it lifts activation or revenue, or lowers acquisition waste, but then name that benefit and measure it.
- How long should the holdout be? Long enough to cover the horizon you care about (day 60 or 90), see Book 1 Part 10 Q24 (long-term holdout).

**Common mistakes:** Calling a flat point estimate "no effect". Judging on day 1 only. Ignoring the fade pattern. Shipping everywhere with no holdout.

### Q34 ⭐⭐ 🟡 The ads team raised ad load by one slot per feed, and ad revenue per user rose 9%, but app ratings fell and next-week sessions per user fell 2%. Explain how you would trade off the two, which horizon you would use, and what you would propose as the guardrail threshold.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** I would not ship on the 9% alone: I would price the revenue gain against the retention it costs over a long horizon, and agree a session and rating guardrail before the launch review, not after.

**Clarifying questions:**
- Is the 9% revenue per user measured over the same week as the 2% session drop, or is it a first-week number? It matters because ad load effects are often front-loaded.
- Was this a randomised test, and how long has it run? Without that, I cannot separate the ad change from a calendar effect.
- Is the rating drop from store reviews or in-app prompts? Store ratings come from a skewed, self-selected group and lag.
- Who owns the guardrail: the ads team or the app-health team? A trade-off needs one owner of the final call.
- Is there a long-term holdout or can we keep one? It is the cleanest way to see the cumulative effect.

**Approach:**
1. Put both effects in one unit: revenue per starting user over a horizon, not per active user per week.
2. Check the 2% session fall is real: a confidence interval on the relative change, with users as the unit.
3. Pick a horizon: read week 1 for safety, but decide on the cumulative curve at 8 to 12 weeks at least, plus a long-term holdout (Book 1 Part 10, Q24, "What is a holdout / long-term holdout group and why would a company keep one?").
4. Look for a decay: does the gap in sessions widen week by week (users leaving) or stay flat (users adjusting)?
5. Cut by segment: new users and light users usually churn faster on heavier ad load.
6. Propose the guardrail in advance: a threshold on the confidence interval, not on the point estimate.

**Metrics:**
- Goal metric: ad revenue per starting user over the horizon = total ad revenue in the arm / users assigned to the arm (not active users, so churn counts).
- Retention input: sessions per user next week = sessions in week 2 / users assigned.
- Guardrails: sessions per user (relative change, upper end of the 95% CI must stay above -1%), 28-day retention, rating or negative-feedback rate (per 1,000 sessions), ad-hide and uninstall rates.
- Illustrative guardrail: block the launch if the CI for sessions per user excludes -1% on the bad side. Always say "illustrative, agree it with the owners before looking at results".

**Risks:**
- Per-active-user revenue hides churn: the users who left are no longer in the denominator.
- Week-1 numbers can be a novelty or a one-off auction effect.
- Rating drops can be driven by a vocal minority; I still treat them as a signal.
- Ad load can hurt the advertiser side later (lower click value), which a user-side test will not show.

**What the interviewer scores:**
- Strong: puts revenue and retention in one unit and computes a break-even horizon. Weak: "revenue is up, ship".
- Strong: asks for a CI-based guardrail with a number agreed in advance. Weak: "I would watch ratings".
- Strong: names a long-term holdout. Weak: only a longer test, no mechanism.
- Strong: segments (new, light, heavy users). Weak: one blended number.

**Example:** Illustrative. Revenue per active user is 1.00 in control and 1.09 in treatment. Weekly retention is 97.0% versus 96.5%. Per starting user, treatment is ahead early (week 4 ratio 1.082) and falls behind control by about week 46 on cumulative revenue. Weak answer: "Revenue is up 9%, ship it." Strong answer: "The gain is real this month and negative by week 46 if the retention gap persists, so I would test longer and cap ad load growth."

**Code:**
```python
# Q34 ad load up: ad revenue per user +9%, sessions per user -2%, ratings down (illustrative numbers)
import numpy as np
rng = np.random.default_rng(34)

# 1) Is the -2% sessions move real? simulate 200k users per arm, sessions/user/week
n = 200_000
ctrl = rng.poisson(10.0, n)
trt = rng.poisson(9.8, n)
d = trt.mean() - ctrl.mean()
se = np.sqrt(trt.var(ddof=1)/n + ctrl.var(ddof=1)/n)
rel = d / ctrl.mean()
lo, hi = (d - 1.96*se)/ctrl.mean(), (d + 1.96*se)/ctrl.mean()
print(f"sessions/user rel change {rel:+.2%}  95% CI [{lo:+.2%}, {hi:+.2%}]")
assert hi < -0.01          # even the optimistic end is worse than -1%

# 2) Cumulative revenue per starting user over weeks: control vs treatment
# revenue per ACTIVE user per week: 1.00 control, 1.09 treatment; weekly retention 97.0% vs 96.5% (invented)
def cum(rev, ret, weeks):
    alive, total = 1.0, 0.0
    for _ in range(weeks):
        total += alive * rev
        alive *= ret
    return total
cross = None
for w in range(1, 105):
    if cum(1.09, 0.965, w) < cum(1.00, 0.970, w):
        cross = w
        break
print("cumulative revenue crossover week:", cross)
for w in (4, 12, 26, 52):
    c, t = cum(1.00, 0.970, w), cum(1.09, 0.965, w)
    print(f"week {w:3d}: control {c:6.2f}  treatment {t:6.2f}  ratio {t/c:.3f}")
assert cum(1.09, 0.965, 4) > cum(1.00, 0.970, 4)
assert cross is not None and 20 <= cross <= 80
# 3) break-even weekly retention drop: treatment per-week revenue gain 9% is wiped out when
# (0.965/0.97)^t * 1.09 < 1 -> t > ln(1/1.09)/ln(0.965/0.97)
t_even = np.log(1/1.09)/np.log(0.965/0.97)
print(f"per-week revenue per starting user falls below control after {t_even:.1f} weeks")
assert 16 < t_even < 17.5
# 4) guardrail rule example
rule_ok = bool(hi > -0.01)    # CI upper bound must stay above -1%
print("guardrail 'sessions not worse than -1%' passes:", rule_ok)
assert not rule_ok
```

**Output (my run):**
```text
sessions/user rel change -1.92%  95% CI [-2.12%, -1.73%]
cumulative revenue crossover week: 46
week   4: control   3.82  treatment   4.14  ratio 1.082
week  12: control  10.21  treatment  10.83  ratio 1.062
week  26: control  18.23  treatment  18.81  ratio 1.032
week  52: control  26.49  treatment  26.26  ratio 0.991
per-week revenue per starting user falls below control after 16.7 weeks
guardrail 'sessions not worse than -1%' passes: False
```

The 2% session fall is real in the simulation (CI about -2.1% to -1.7%, so it fails a -1% guardrail). Treatment leads cumulative revenue for the first weeks, then crosses below control at week 46.

**Follow-ups:**
- What if the retention gap shrinks over time? Then the crossover moves out or never happens; that is why I read the weekly curve, not one number.
- How do you pick the guardrail threshold? From what the business would pay: the revenue gain divided by the value of a retained user gives the break-even loss; set the guardrail tighter than that.
- Book 1 Part 10, Q13 ("The test shows the primary metric up but revenue (or a guardrail) down or flat. How do you interpret and decide?") covers the test-side reading of the same shape.

**Common mistakes:** Dividing revenue by active users. Calling a 2% session drop "small" without a CI or a per-week compounding view. Picking the guardrail after seeing the result. Treating the rating drop as noise because it is not statistically tested.

### Q35 ⭐⭐ 🟡 A push-notification cap of three per day is proposed. Describe the metrics you would use to judge the cap (goal, input and guardrail metrics), the segments where the cap might hurt most, and what result would make you reject it.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** I would judge the cap on sessions and opt-outs per user, not on notification opens, and I would reject it if a high-value segment (new or transaction users) or total sessions fall past a threshold fixed in advance.

**Clarifying questions:**
- What is the cap's goal: fewer opt-outs, less annoyance, or lower send cost? The goal decides the primary metric.
- Does the cap count all pushes or only marketing ones? Order and delivery alerts should not be capped the same way.
- Who gets the three: the first three by time, or the three highest-scoring? It changes who is hurt.
- Can we randomise at user level and run at least 2 to 4 weeks? Opt-out and uninstall effects show up late.
- What is the current distribution of pushes per user per day? If few users get more than three, the effect is small.

**Approach:**
1. Goal metric: sessions per user per week (or the product's core action), not push opens.
2. Input metrics: pushes sent per user, push-attributed sessions, open rate per push.
3. Guardrails: opt-out (push permission off) rate, uninstall rate, orders or core actions, time-sensitive message delivery.
4. Segment: new users in their first 14 days, heavy-notified users, transaction-alert users, and users with a history of opt-out.
5. Run a user-level randomised test with a long enough window to see opt-outs; pre-register the reject rule.
6. Decide: ship, ship with exceptions (transaction pushes exempt), or reject.

**Metrics:**
- Sessions per user per week = sessions in week / users assigned to the arm (denominator fixed at assignment, so lost users count).
- Push opt-out rate = users who turned push off / users assigned.
- Open rate per push = opens / pushes delivered (diagnostic only: a cap raises it mechanically because the pushes that remain are the better ones).
- Guardrails: uninstalls per 1,000 users, 28-day retention, orders per user.

**Risks:**
- Open rate rises after the cap even when value falls: the metric rewards sending less.
- Push-attributed sessions overstate the loss: some of those sessions would have happened anyway.
- Short tests miss slow opt-out effects, in both directions.
- A flat average can hide harm to new users or to transaction alerts.

**What the interviewer scores:**
- Strong: goal, input and guardrail metrics named, with open rate called a diagnostic. Weak: "track open rate".
- Strong: segments with a reason (new users, time-sensitive, heavy-notified). Weak: "all users".
- Strong: a numeric reject rule written before the test. Weak: "if it looks bad".
- Strong: separate marketing from transactional pushes. Weak: one cap for everything.

**Example:** Illustrative. Segments: new users 15% at 2 pushes/day, regular 55% at 3, heavy-notified 20% at 6, transaction 10% at 4. Average pushes now 3.55 a day. The cap bites only for heavy and transaction users. Push-attributed sessions lost: 0.027 per user per day, or 0.189 per week. If 27% of those are truly incremental, net loss is 0.051 sessions per week on a base of 8, about -0.6%. Reject rule: reject if the lower CI bound for sessions is below -2%, or any key segment is down more than 3%. Weak answer: "Open rate went up, so the cap works." Strong answer: "Sessions are down 0.7% (CI -1.1% to -0.2%), opt-outs fall in the heavy segment, but transaction users lose the most per push, so I would exempt them."

**Code:**
```python
# Q35 push cap of 3/day (illustrative segment model + seeded readout)
import numpy as np
rng = np.random.default_rng(35)
# segment: share, pushes/day now, sessions-per-push (marginal for pushes above the cap), opt-out per 100 pushes above cap
segs = {
 "new users (<14d)":   (0.15, 2.0, 0.060, 0.30),
 "regular users":      (0.55, 3.0, 0.030, 0.10),
 "heavy-notified":     (0.20, 6.0, 0.020, 0.45),
 "txn/time-sensitive": (0.10, 4.0, 0.150, 0.05),   # e.g. delivery or price alerts, cap drops useful ones
}
cap = 3
tot_lost = 0.0; tot_saved_optouts = 0.0; base_pushes = 0.0
print(f"{'segment':20}{'pushes/d':>9}{'dropped/d':>10}{'sess lost/user/d':>18}{'optouts saved/1000u/d':>23}")
for k, (sh, p, spp, oo) in segs.items():
    dropped = max(0.0, p - cap)
    lost = dropped * spp
    saved = dropped * oo / 100 * 1000
    tot_lost += sh * lost; tot_saved_optouts += sh * saved; base_pushes += sh * p
    print(f"{k:20}{p:9.1f}{dropped:10.1f}{lost:18.3f}{saved:23.2f}")
print(f"avg pushes/day now {base_pushes:.2f}; avg sessions lost per user per day {tot_lost:.4f}")
assert round(base_pushes, 2) == 3.55
assert abs(tot_lost - 0.0270) < 1e-9

# seeded readout: sessions/user/week 7-day, control vs capped; decision rule pre-registered
n = 50_000
ctrl = rng.poisson(8.0, n)
attributed_week = tot_lost * 7                 # push-attributed sessions lost per user per week
incremental_share = 0.27                      # invented: share that would not have happened anyway
print(f"push-attributed loss {attributed_week:.3f}/user/week; net after substitution {attributed_week*incremental_share:.3f}")
assert abs(attributed_week*incremental_share - 0.051) < 0.001
trt = rng.poisson(8.0 - attributed_week*incremental_share, n)
d = (trt.mean()-ctrl.mean())/ctrl.mean()
se = np.sqrt(trt.var(ddof=1)/n+ctrl.var(ddof=1)/n)/ctrl.mean()
lo, hi = d-1.96*se, d+1.96*se
print(f"sessions/user rel change {d:+.2%} CI [{lo:+.2%}, {hi:+.2%}]")
reject = lo < -0.02          # reject if the lower bound is worse than -2%
print("reject cap on sessions guardrail (lower bound < -2%):", reject)
assert not reject
```

**Output (my run):**
```text
segment              pushes/d dropped/d  sess lost/user/d  optouts saved/1000u/d
new users (<14d)          2.0       0.0             0.000                   0.00
regular users             3.0       0.0             0.000                   0.00
heavy-notified            6.0       3.0             0.060                  13.50
txn/time-sensitive        4.0       1.0             0.150                   0.50
avg pushes/day now 3.55; avg sessions lost per user per day 0.0270
push-attributed loss 0.189/user/week; net after substitution 0.051
sessions/user rel change -0.68% CI [-1.11%, -0.24%]
reject cap on sessions guardrail (lower bound < -2%): False
```

The cap bites only for heavy and transaction users, and the transaction segment loses the most sessions per dropped push (0.150). The seeded readout stays inside the -2% rule, so the cap passes on total sessions; the segment rule is the one to watch.

**Follow-ups:**
- What would make you reject it? Sessions CI lower bound below -2%, a key segment down by more than 3%, or a rise in time-sensitive message failures.
- Why not use open rate as the goal? The cap raises it by construction.
- Related: Book 1 Part 10, Q3 ("How do you choose the primary metric, guardrail metrics and secondary metrics for an experiment? Give an example.").

**Common mistakes:** Using open rate as success. Capping transactional alerts. Reading only the average. Running one week and missing opt-out effects.

### Q36 ⭐⭐ 🟡 Two teams report different MAU for the same month: 24.1 million versus 22.8 million. Explain the usual sources of such gaps (definition, deduplication across devices, time zone, bots, event source), and how you would reconcile them and prevent a repeat.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Two MAU numbers for one month almost always mean two definitions, so I would line up the definitions, rebuild both from the same raw events, and bridge the 1.3 million gap step by step.

**Clarifying questions:**
- What is "active" in each team: any event, a logged-in event, or a qualifying action? The biggest gaps come from this.
- Unit of counting: device ID, cookie, or user ID? Devices overcount people.
- Which time zone defines the month and which dates? A month ends at different instants in UTC and IST.
- Are bots, internal traffic and test accounts filtered, and by what rule?
- Which event source: client SDK, server logs or the warehouse table? They lose different events.

**Approach:**
1. Write both definitions side by side: unit, event filter, window, time zone, bot rule, source.
2. Rebuild both from one raw events table to see how much is definition versus data.
3. Bridge the gap as a waterfall, changing one choice at a time, stating the order.
4. Whatever is left over is a data-quality gap (missing events, late loads, duplicate IDs): compare counts per day and per source.
5. Pick one governed definition and publish it with a name (for example "MAU, logged-in, IST").
6. Prevent a repeat: one metric table owned by a team, a metric dictionary, and a daily reconciliation check.

**Metrics:**
- MAU (governed) = distinct user_id with at least one qualifying event in the calendar month in the agreed time zone, bots excluded.
- Gap explained = sum of waterfall steps / total gap (target: above 95%).
- Reconciliation guardrail: difference between the two published numbers should stay under an agreed tolerance such as 0.5%.

**Risks:**
- Fixing one team's number to match the other without understanding why.
- Waterfall steps depend on order; state the order or the argument becomes a debate.
- Deduplicating across devices needs a login: logged-out users cannot be merged.
- Changing the definition silently breaks the trend line; show old and new for one overlap month.

**What the interviewer scores:**
- Strong: lists the five usual sources and rebuilds from raw events. Weak: "ask the teams to check".
- Strong: a waterfall with numbers that adds to the gap. Weak: a list of guesses.
- Strong: prevention through a single governed definition. Weak: stops at the diagnosis.

**Example:** Illustrative. Team A 24.1 million counts devices, UTC month, bots in. Team B 22.8 million counts people, IST month, bots out. Gap 1.3 million. In a 20,000-user simulation the same pattern appears: devices to people removes the largest block, then bots, then a small month-boundary shift. Weak answer: "One of them is wrong." Strong answer: "Both can be right under different definitions; here is the bridge, and here is the one definition we will publish."

**Code:**
```python
# Q36 two MAU numbers: simulate raw events, show each definition choice moves the count
import numpy as np, pandas as pd
rng = np.random.default_rng(36)
N = 20_000
users = pd.DataFrame({"user_id": np.arange(N)})
users["n_dev"] = rng.choice([1, 2, 3], N, p=[0.75, 0.2, 0.05])
rows = []
for u, nd in zip(users.user_id, users.n_dev):
    for dv in range(nd):
        k = rng.integers(1, 6)
        # event times across March 2026 UTC, plus some at the edges
        t = pd.Timestamp("2026-03-01") + pd.to_timedelta(rng.uniform(-0.3, 31.3, k), unit="D")
        for tt in t:
            rows.append((u, f"{u}-{dv}", tt, 0, rng.random() < 0.9))
ev = pd.DataFrame(rows, columns=["user_id", "device_id", "ts_utc", "is_bot", "logged_in"])
bots = pd.DataFrame({"user_id": np.arange(N, N + 600)})
brow = []
for u in bots.user_id:
    for tt in pd.Timestamp("2026-03-01") + pd.to_timedelta(rng.uniform(0, 31, 3), unit="D"):
        brow.append((u, f"b-{u}", tt, 1, False))
ev = pd.concat([ev, pd.DataFrame(brow, columns=ev.columns)], ignore_index=True)
ev["ts_ist"] = ev.ts_utc + pd.Timedelta(hours=5, minutes=30)

def in_month(ts):
    return (ts >= "2026-03-01") & (ts < "2026-04-01")
A = ev[in_month(ev.ts_utc)].device_id.nunique()                          # team A: devices, UTC, bots in
B = ev[in_month(ev.ts_ist) & (ev.is_bot == 0)].user_id.nunique()        # team B: people, IST, bots out
print("A (devices, UTC, bots in):", A, " B (people, IST, bots out):", B, " gap:", A - B)

# waterfall, fixed order; each step changes one definition
s0 = ev[in_month(ev.ts_utc)].device_id.nunique()
s1 = ev[in_month(ev.ts_utc)].user_id.nunique()                                   # dedupe devices to user_id (bots count as users)
s2 = ev[in_month(ev.ts_utc) & (ev.is_bot == 0)].user_id.nunique()                # drop bots
s3 = ev[in_month(ev.ts_ist) & (ev.is_bot == 0)].user_id.nunique()                # month boundary in IST
steps = [("devices in UTC month", s0), ("-> distinct user_id", s1), ("-> drop bots", s2), ("-> IST month", s3)]
prev = None
for name, v in steps:
    print(f"{name:24}{v:8d}" + ("" if prev is None else f"  step {v-prev:+d}"))
    prev = v
assert s0 == A and s3 == B
assert (s0 - s1) + (s1 - s2) + (s2 - s3) == A - B
print('note: state the order of the waterfall steps when you present it')
```

**Output (my run):**
```text
A (devices, UTC, bots in): 26456  B (people, IST, bots out): 19934  gap: 6522
devices in UTC month       26456
-> distinct user_id        20543  step -5913
-> drop bots               19943  step -600
-> IST month               19934  step -9
note: state the order of the waterfall steps when you present it
```

In this seeded simulation, going from devices to people is the largest step (-5,913 of a 6,522 gap), bots are -600 and the time-zone shift only -9. Real gaps will have different proportions; the method (one change at a time, add to the gap) is what carries over.

**Follow-ups:**
- What if the gap does not close after definitions are aligned? Compare per-day counts by event source to find lost or duplicated events.
- How do you handle logged-out users? Report them separately (device-based) rather than mixing them into a people count.

**Common mistakes:** Debating which number is right instead of bridging. Mixing steps so the waterfall does not add up. Ignoring time zones near the month boundary. Leaving two published definitions after the meeting.

### Q37 ⭐⭐ 🔴 A daily metric is down 2% and an alert fired. The metric usually moves 1.5% day to day, with a weekend dip. Explain how you would decide whether this is noise, what baseline and interval you would use, and how you would set an alert that does not fire every Monday.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** A 2% drop on a metric with 1.5% daily noise is well within noise, so I compare to the same weekday over the last several weeks, work in standard deviations, and alert only on a multi-sigma miss.

**Clarifying questions:**
- Is "1.5%" a standard deviation of daily change or an average absolute change? It sets the z-score; I would compute it from history.
- Which day of the week is the alert on, and what is the weekend dip size? It sets the baseline.
- Is the metric a ratio or a count? Ratios need a stable denominator.
- How costly is a false alarm versus a miss? That sets the threshold.
- Any known events (release, holiday, outage) in the window?

**Approach:**
1. Baseline: the same weekday over the previous 4 to 8 weeks, adjusted for trend if there is growth.
2. Noise: standard deviation of those same-weekday values; add a little for baseline uncertainty.
3. Compute z = (today - baseline) / (sd * sqrt(1 + 1/k)), with k baseline weeks.
4. Alert on a z below -3 (or a confidence band), and require persistence (for example two days) for softer alerts.
5. Check for a data issue first: late data, a broken pipeline, or a deploy.
6. Review the alert quarterly: count false alerts and misses.

**Metrics:**
- z-score = (today - mean of same weekday, last k weeks) / (sd of those values * sqrt(1 + 1/k)).
- False alert rate = alerts with no real cause / days monitored; target under about 1 a month.
- Detection rate = injected or real drops that alerted / total drops; check with injected tests.

**Risks:**
- Naive day-over-day and "versus last 7 days" rules fire on the weekend dip every week.
- With only six baseline points, a z of -3 is a t-distribution tail, which is fatter than the normal tail.
- Trend and holidays inflate the sd or bias the baseline.
- Alerting on a single day at -2% would fire constantly.

**What the interviewer scores:**
- Strong: same-weekday baseline and a z-score with a stated interval. Weak: "compare to yesterday".
- Strong: knows 2% on 1.5% noise is not a surprise. Weak: "2% is big, investigate".
- Strong: tests the rule on simulated or historical data. Weak: picks a threshold by feel.

**Example:** Illustrative. With sd 1.5% and a six-week baseline, a -2% day has z = -0.02 / (0.015 * sqrt(1 + 1/6)) = -1.23. About 11% of normal days are that low or lower, so it is noise. The weekend dip is built into the baseline, so Monday's report does not fire. Weak answer: "It is down 2%, raise an alert." Strong answer: "z is about -1.2, it happens one day in nine, I will wait and watch."

**Code:**
```python
# Q37 down 2% vs noise: same-weekday baseline vs naive rules (illustrative simulation)
import numpy as np
rng = np.random.default_rng(37)
dow = np.array([1.00, 1.00, 1.00, 1.00, 1.00, 0.93, 0.90])   # Mon..Sun weekend dip
days = 7 * 60
t = np.arange(days)
level = 100_000 * (1 + 0.0002 * t)
y = level * dow[t % 7] * (1 + rng.normal(0, 0.015, days))    # 1.5% noise sd

# naive rule A: today vs yesterday, alert if down more than 2%
# naive rule B: today vs mean of previous 7 days, alert if down more than 2%
# good rule: today vs same weekday over previous 6 weeks, alert if z < -3
fireA = np.zeros(days, bool); fireB = np.zeros(days, bool)
for i in range(60, days):
    fireA[i] = y[i] / y[i-1] - 1 < -0.02
    fireB[i] = y[i] / y[i-7:i].mean() - 1 < -0.02
# simpler, transparent baseline: same weekday, last 6 weeks, scaled by the level growth over those weeks
fireC = np.zeros(days, bool); z_all = np.full(days, np.nan)
for i in range(60, days):
    base = y[[i - 7*k for k in range(1, 7)]]
    mu = base.mean(); sd = base.std(ddof=1)
    z = (y[i] - mu) / (sd * np.sqrt(1 + 1/6))
    z_all[i] = z; fireC[i] = z < -3
rng_idx = np.arange(60, days)
names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
print("alert rate by weekday (percent of days), naive A | naive B | same-weekday z<-3")
for d_ in range(7):
    m = (rng_idx % 7 == d_)
    print(f"{names[d_]}: {fireA[rng_idx][m].mean()*100:5.1f} | {fireB[rng_idx][m].mean()*100:5.1f} | {fireC[rng_idx][m].mean()*100:5.1f}")
print(f"overall: {fireA[rng_idx].mean()*100:.1f}% | {fireB[rng_idx].mean()*100:.1f}% | {fireC[rng_idx].mean()*100:.1f}%")
# the pure noise arithmetic for a 2% drop
from scipy.stats import norm
z2 = -0.02 / (0.015 * np.sqrt(1 + 1/6))
print(f"z for a -2% day with 1.5% sd and a 6-week baseline: {z2:.2f}, one-sided p = {norm.cdf(z2):.3f}")
from scipy.stats import t as tdist
print(f"with only 6 baseline points the z=-3 tail is a t(5) tail: P(t<-3) = {tdist.cdf(-3,5):.3f} (normal says {norm.cdf(-3):.4f})")
assert abs(tdist.cdf(-3,5)-0.015)<0.001
assert abs(z2 + 1.23) < 0.01 and 0.10 < norm.cdf(z2) < 0.12
assert fireA[rng_idx].mean() > 0.10 and fireC[rng_idx].mean() < 0.03
```

**Output (my run):**
```text
alert rate by weekday (percent of days), naive A | naive B | same-weekday z<-3
Mon:   0.0 |   0.0 |   0.0
Tue:  15.7 |   0.0 |   0.0
Wed:  13.7 |   0.0 |   2.0
Thu:  13.7 |   0.0 |   0.0
Fri:  21.2 |   0.0 |   1.9
Sat: 100.0 |  94.2 |   0.0
Sun:  69.2 | 100.0 |   5.8
overall: 33.6% | 28.1% | 1.4%
z for a -2% day with 1.5% sd and a 6-week baseline: -1.23, one-sided p = 0.109
with only 6 baseline points the z=-3 tail is a t(5) tail: P(t<-3) = 0.015 (normal says 0.0013)
```

The naive rules fire most weekends (Saturday and Sunday 69% to 100%), while the same-weekday z rule fires 1.4% overall. That is slightly above the normal-tail 0.13% because six baseline points give a heavier tail (P(t<-3) = 0.015).

**Follow-ups:**
- How do you cut false alerts further? A longer baseline (8 to 12 weeks), a robust sd (MAD), and a two-day persistence rule.
- What if the metric has a trend? Fit a trend or use ratios to a rolling level.
- For statistical-test follow-ups, see Book 1 Part 10, Q27 ("Ratio metrics (CTR, revenue per session) and per-session vs per-user analysis: what goes wrong with the variance and how do you fix it (delta method)?").

**Common mistakes:** A fixed percentage threshold. Using the 7-day average as a baseline with a weekly cycle. Using the normal tail with few baseline points. Alerting without checking the pipeline first.

### Q38 ⭐⭐ 🔴 Conversion rate rose from 3.0% to 3.6% after a bot filter and a page-speed fix, but orders are flat. Explain how the denominator can change without the business improving, and how you would restate the metric so that the before and after periods are comparable.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
**Say this first (1 line):** Conversion is orders divided by sessions, so if the filter removed non-buying bot sessions the ratio rises with no change in orders; I would restate the earlier period with the same filter and compare like with like.

**Clarifying questions:**
- What exactly is the denominator: sessions, visits, or users? The denominator definition decides what a filter can change.
- Does the bot filter apply only from the launch date or was it back-applied? A mismatch makes the before and after periods different metrics.
- Did traffic volume change, or only the filtered count? It tells me if the page-speed fix did anything.
- How many orders per day before and after? Flat orders are the key clue.
- Is there any chance the filter removes real users (false positives)? That would inflate the new rate further.

**Approach:**
1. Decompose: conversion = orders / sessions. Orders are flat, so the whole change is in the denominator.
2. Ask what changed the denominator: the bot filter and the page-speed fix (which can change session splitting and bounce counting).
3. Restate: apply the same bot filter and the same session definition to the before period.
4. Compare like with like. If orders are flat and the restated rates match, the business did not change.
5. Add metrics that do not depend on the session denominator: orders per 1,000 filtered sessions, orders per logged-in user, buyers per active user.
6. Check the page-speed fix separately, for example with a holdout, since it targets the actual conversion step.

**Metrics:**
- Conversion = orders / eligible sessions, with "eligible" frozen as one definition (humans, after the bot filter).
- Restated conversion for period P = orders in P / sessions in P under the new filter.
- Guardrails: orders per day, revenue per day, share of sessions filtered as bots (watch for a jump), buyers per active user.

**Risks:**
- Silent definition change makes before and after non-comparable.
- A filter that removes real non-buying humans (false positives) raises the rate further.
- A page-speed fix can change how sessions are counted (a faster page may merge or split visits).
- Celebrating the rate while orders are flat.

**What the interviewer scores:**
- Strong: identifies the denominator as the cause from "orders are flat". Weak: credits the page-speed fix.
- Strong: restates the earlier period with the same filter. Weak: compares unrestated numbers.
- Strong: proposes a denominator-free companion metric. Weak: a different ratio with the same fragility.
- Related reading: Book 1 Part 10, Q10 ("What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment.").

**Example:** Illustrative. Before: 1,000,000 sessions of which 166,667 are bots, 30,000 orders: 3.0%. After: the filter removes the same bots, 833,333 sessions, 30,000 orders: 3.6%. Restating the before period with the filter gives 30,000 / 833,333 = 3.6%. Like-for-like change: zero. Weak answer: "Conversion rose 20%, great." Strong answer: "Orders did not move, so the improvement is the denominator; like for like it is flat."

**Code:**
```python
# Q38 conversion 3.0% -> 3.6% with orders flat (illustrative numbers)
before = dict(sessions=1_000_000, bot_sessions=166_667, orders=30_000)
after_ = dict(sessions=1_000_000, bot_sessions=166_667, orders=30_000)   # same traffic; filter now removes bots

raw_before = before["orders"] / before["sessions"]
filtered_after = after_["orders"] / (after_["sessions"] - after_["bot_sessions"])
restated_before = before["orders"] / (before["sessions"] - before["bot_sessions"])
print(f"reported before (no filter): {raw_before:.2%}")
print(f"reported after  (filter on): {filtered_after:.2%}")
print(f"restated before (filter on): {restated_before:.2%}")
print(f"like-for-like change: {filtered_after - restated_before:+.3%} points; orders change: {after_['orders']-before['orders']:+d}")
assert round(raw_before, 4) == 0.03 and round(filtered_after, 4) == 0.036 and round(restated_before, 4) == 0.036
assert after_["orders"] == before["orders"]

# if the filter also removes some real humans (false positives that never buy), the restated lift is partly an artefact
# 10,000 humans wrongly removed, none of them buyers: denominator shrinks further with no extra orders
human = before["sessions"] - before["bot_sessions"]
fp = 10_000
with_fp = before["orders"] / (human - fp)
print(f"with 10,000 non-buying humans wrongly filtered: {with_fp:.3%} (versus {restated_before:.3%} without)")
assert with_fp > restated_before

# a more honest primary metric when denominators are fragile: orders per eligible user (or per 1,000 humans)
print("orders per 1,000 filtered sessions after:", round(after_['orders'] / (after_['sessions'] - after_['bot_sessions']) * 1000, 1))
# per-user view: distinct buyers / distinct logged-in visitors is less exposed to session-definition changes
```

**Output (my run):**
```text
reported before (no filter): 3.00%
reported after  (filter on): 3.60%
restated before (filter on): 3.60%
like-for-like change: +0.000% points; orders change: +0
with 10,000 non-buying humans wrongly filtered: 3.644% (versus 3.600% without)
orders per 1,000 filtered sessions after: 36.0
```

Restating the before period with the filter gives 3.60%, exactly the after number, so the like-for-like change is zero. If the filter also removes 10,000 non-buying humans, the rate would read 3.644% with no extra orders.

**Follow-ups:**
- What if orders were up 2% and conversion up 20%? Then most of the move is the denominator and only about 2% is demand; restate before reading.
- How do you prevent this? Version the metric definition, back-apply changes, and show old and new together for an overlap period.

**Common mistakes:** Reporting the new rate against an old, unfiltered baseline. Crediting the page-speed fix without a holdout. Not checking if the filter removed real users. Using a ratio when orders are the cleaner number.

### Q39 ⭐⭐ 🔴 A recommendation model refresh raised click-through rate by 5%, but catalogue diversity fell and 8-week retention in the treatment is down 0.5 point. Say how you would weigh a short-term lift against long-term harm, and what metrics and holdout you would set up to decide.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** A 5% click lift that comes with lower diversity and 0.5 points lower 8-week retention is not a win until I price the lost retention and confirm it with a long-term holdout.

**Clarifying questions:**
- Is the 8-week retention drop statistically solid and from a randomised test? A 0.5 point change needs a big sample to detect.
- What is the baseline retention? A 0.5 point drop is a different size relative to 20% or 60%.
- How is diversity measured (categories per user, exposure entropy)? I need a number to track.
- What do clicks lead to: purchases, watch time? CTR alone is a weak value proxy.
- Can the new model run to a holdout for several months? It decides how sure we can be.

**Approach:**
1. Translate both effects into one unit, such as value per exposed user over six months.
2. Compute the break-even: what a retained user must be worth for the click gain to pay for the retention loss.
3. Look for the mechanism: lower diversity (a narrower feed) is a plausible cause of later churn, so check retention by exposure entropy.
4. Set up the decision test: a long-term holdout (a small share of users kept on the old model) and a pre-agreed retention guardrail.
5. Consider a blended ranker: keep the CTR gain but add a diversity or exploration term, and test that.
6. Decision: no full rollout until retention is within the guardrail.

**Metrics:**
- CTR = clicks / impressions (diagnostic).
- Retention at week 8 = users active in week 8 / users assigned (assignment-based, so churn counts).
- Diversity = entropy of item or category exposure per user; also catalogue coverage = distinct items shown at least once / catalogue size.
- Value per user = clicks x value per click - (retention loss x future value per retained user).
- Guardrails: retention (lower CI bound no worse than -0.2 points, illustrative), session length, complaints.

**Risks:**
- CTR can rise because the model shows easy clicks, not valuable content.
- Short experiments miss the retention effect completely.
- Value per retained user is an assumption; show the break-even rather than hide it.
- The holdout can be contaminated if users see old-model effects through shared catalogue changes.

**What the interviewer scores:**
- Strong: a common unit and a break-even number. Weak: "retention matters more".
- Strong: a holdout with a sample size. Weak: "run it longer".
- Strong: proposes a diversity term or a blended ranker. Weak: ship or revert only.
- Related: Book 1 Part 10, Q40 ("How do you run experiments for a feature with a long-term outcome (retention, LTV) when you cannot wait months? (surrogate metrics, holdouts)") and Q38 on testing ranking algorithms.

**Example:** Illustrative. Clicks per user go from 20 to 21 over 8 weeks at 0.02 per click: gain 0.02 per exposed user. Retention 40.0% to 39.5% with a retained user worth 6.0 over six months: loss 0.005 x 6 = 0.03. Net -0.01 per user, about -10,000 for 1,000,000 users. Break-even value per retained user is 0.02 / 0.005 = 4.0. Weak answer: "CTR is up 5%, ship." Strong answer: "At any retained-user value above 4 this loses money; I will hold out and measure retention."

**Code:**
```python
# Q39 CTR +5% vs 8-week retention -0.5pt (illustrative)
import numpy as np
from scipy.stats import norm
users = 1_000_000
clicks_ctrl, clicks_trt = 20.0, 21.0            # clicks per user in 8 weeks, +5%
value_per_click = 0.02                           # invented
click_gain = (clicks_trt - clicks_ctrl) * value_per_click
ret_ctrl, ret_trt = 0.400, 0.395
future_value_per_retained = 6.0                  # invented value of a retained user over the next 6 months
retention_loss = (ret_ctrl - ret_trt) * future_value_per_retained
print(f"short-term gain per exposed user: {click_gain:.4f}")
print(f"long-term loss per exposed user : {retention_loss:.4f}")
print(f"net per user {click_gain-retention_loss:+.4f}; net for 1M users {(click_gain-retention_loss)*users:+,.0f}")
be = click_gain / (ret_ctrl - ret_trt)
print(f"break-even future value per retained user: {be:.2f}")
assert abs(click_gain - 0.02) < 1e-12 and abs(retention_loss - 0.03) < 1e-12 and abs(be - 4.0) < 1e-9

# holdout size to detect a 0.5pt retention difference at 40% base, alpha 0.05 two-sided, 80% power
p = 0.40; d = 0.005
n = 2 * (norm.ppf(0.975) + norm.ppf(0.80))**2 * p * (1 - p) / d**2
print(f"users per arm needed: {n:,.0f}")
assert 150_000 < n < 152_000

# diversity metric: entropy of item exposure share, two feeds over 1,000 items
ranks = np.arange(1, 1001)
def entropy(alpha):
    w = ranks**(-alpha); w = w/w.sum()
    return -(w*np.log2(w)).sum()
h0, h1 = entropy(0.8), entropy(1.1)
print(f"exposure entropy (bits): old feed {h0:.2f}, new feed {h1:.2f}, change {h1/h0-1:+.1%}")
assert h1 < h0
```

**Output (my run):**
```text
short-term gain per exposed user: 0.0200
long-term loss per exposed user : 0.0300
net per user -0.0100; net for 1M users -10,000
break-even future value per retained user: 4.00
users per arm needed: 150,698
exposure entropy (bits): old feed 8.65, new feed 6.80, change -21.3%
```

The break-even is 4.00 against an assumed 6.0, so the model loses money under these invented inputs. Detecting a 0.5 point change at a 40% base needs about 150,700 users per arm, so a small holdout cannot answer this.

**Follow-ups:**
- What if the retention drop is not significant? A wide CI means we do not know; keep the holdout running and do not ship on silence.
- How do you protect diversity directly? Add a diversity term or exploration quota, and measure the cost in CTR.

**Common mistakes:** Treating CTR as value. No common unit between the two effects. A holdout too small to see 0.5 points. Ignoring the mechanism (narrower feed).

### Q40 ⭐⭐ 🔴 A quick-commerce tab inside a shopping app grew to 80,000 daily orders while the parent grocery tab lost 30,000. Explain how you would measure true incremental orders versus cannibalisation, and what you would report to leadership.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** 80,000 minus 30,000 is a naive 50,000, but the parent tab was also drifting for other reasons, so I would measure true incrementality against matched control cities and report a range.

**Clarifying questions:**
- Did the tab launch everywhere at once or city by city? Staggered launches give a control group.
- Is there a tab-level or user-level exposure flag? I need to know who could see the new tab.
- Over what window did the parent lose 30,000, and what was its trend before launch? Without a trend, I cannot say what the parent would have done anyway.
- Are the same users buying in both? User-level data lets me see shifted baskets, not just totals.
- Do I measure orders, GMV or margin? Quick-commerce orders are usually smaller and cost more to fulfil.

**Approach:**
1. Define the counterfactual: what parent orders would be if the tab had not launched.
2. Pick a design: staggered city rollout or matched control cities (difference-in-differences); at user level, a holdout that does not see the tab (see Book 1 Part 10, Q44, "How would you design and read a geo / city-level experiment when user-level randomization is not possible? (synthetic control, matched markets)").
3. Estimate cannibalisation = change in parent orders in launch cities minus change in control cities.
4. Incremental orders = quick-commerce orders + that (negative) parent effect.
5. Check the other directions: total orders per user, order frequency, new users who came only for the tab.
6. Report orders, GMV and contribution margin, each as a range.

**Metrics:**
- Incremental orders per day = quick orders + (parent change in launch cities - parent change in matched control cities, scaled to the same base).
- Incrementality share = incremental orders / quick orders (here 60,000 / 80,000).
- Cannibalisation rate = parent orders lost because of the tab / quick orders.
- Guardrails: total orders per active user, contribution margin per order, delivery time, cancellation rate.

**Risks:**
- Pre/post in launch cities blames the tab for market-wide drift.
- Matched cities can differ in unobserved ways; check pre-trends.
- Spillover: control cities may also see the tab through marketing.
- Orders may be incremental but unprofitable; margin changes the verdict.

**What the interviewer scores:**
- Strong: names the counterfactual and a control group. Weak: "80k minus 30k".
- Strong: reports a range and a margin view. Weak: one number.
- Strong: checks order frequency per user. Weak: only counts.

**Example:** Illustrative. Launch cities parent orders: 600,000 to 570,000. Matched control cities: 600,000 to 590,000. Difference-in-differences on the parent: -30,000 - (-10,000) = -20,000. Incremental = 80,000 - 20,000 = 60,000, or 75% of the tab. The naive view says 50,000 (62.5%). Weak answer: "Net 50,000 new orders." Strong answer: "About 60,000 incremental, 75% incrementality, with a range, and a margin view next."

**Code:**
```python
# Q40 quick-commerce tab: incremental orders vs cannibalisation (illustrative)
import numpy as np
rng = np.random.default_rng(40)
# deterministic hand-check
parent_before_t, parent_after_t = 600_000, 570_000   # launch cities, daily parent orders
parent_before_c, parent_after_c = 600_000, 590_000   # matched control cities (no tab yet)
quick = 80_000
did = (parent_after_t - parent_before_t) - (parent_after_c - parent_before_c)
naive_incr = quick - 30_000
incr = quick + did
print(f"naive incremental = {quick} - 30000 = {naive_incr}")
print(f"DiD parent effect = {did}; incremental = {incr}; incrementality share = {incr/quick:.1%}")
assert did == -20_000 and incr == 60_000 and naive_incr == 50_000 and incr / quick == 0.75

# seeded city-level simulation: 10 launch cities, 20 control cities, true cannibalisation 20k/day total
launch = 10; ctrl = 20
base = rng.normal(60_000, 8_000, launch + ctrl).clip(30_000)          # parent orders per city before
trend = -0.0167                                                         # market-wide drift
noise = rng.normal(0, 0.01, launch + ctrl)
after = base * (1 + trend + noise)
true_cannibal_per_city = 2_000
after[:launch] -= true_cannibal_per_city
d_city = after - base
did_pct = d_city[:launch].sum() - base[:launch].sum() * (d_city[launch:].sum() / base[launch:].sum())
# bootstrap over cities
est = []
for _ in range(2000):
    li = rng.integers(0, launch, launch); ci = rng.integers(0, ctrl, ctrl)
    bl, dl = base[:launch][li], d_city[:launch][li]
    bc, dc = base[launch:][ci], d_city[launch:][ci]
    est.append(dl.sum() - bl.sum() * dc.sum() / bc.sum())
lo, hi = np.percentile(est, [2.5, 97.5])
print(f"DiD cannibalisation estimate {did_pct:,.0f}/day (true -20,000), 95% bootstrap CI [{lo:,.0f}, {hi:,.0f}]")
naive_pre_post = d_city[:launch].sum()
print(f"naive pre/post parent change in launch cities: {naive_pre_post:,.0f}")
assert lo < -20_000 < hi
assert naive_pre_post < did_pct       # the pre/post view over-states the loss because of the market drift
```

**Output (my run):**
```text
naive incremental = 80000 - 30000 = 50000
DiD parent effect = -20000; incremental = 60000; incrementality share = 75.0%
DiD cannibalisation estimate -20,849/day (true -20,000), 95% bootstrap CI [-26,113, -16,471]
naive pre/post parent change in launch cities: -30,030
```

The hand-check gives 60,000 incremental. In the seeded city simulation the true cannibalisation is 20,000 per day and the difference-in-differences estimate is -20,849 with a bootstrap CI of about -26,100 to -16,500 (it contains the truth). The naive pre/post change is -30,030 because it includes the market drift.

**Follow-ups:**
- What if there are no control cities? Use a user-level holdout or a synthetic control from earlier launches.
- What if cannibalised orders are higher margin? Report contribution margin: 60,000 incremental low-margin orders can be worth less than 20,000 lost high-margin ones.

**Common mistakes:** Reporting 80,000 as new demand. Subtracting only the visible parent drop. Ignoring market trend. Not checking margin.

### Q41 ⭐⭐ 🔴 An LLM re-ranker is proposed for product search. Define the primary metric, a query-level ratio metric and guardrails (latency, zero-result rate, cost per query), and say what would worry you about the metric choice, for example sessions that end without a click because the answer was good.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** For an LLM re-ranker my primary metric is query success rate (queries that reach a defined successful outcome / queries), with latency, zero-result rate and cost per query as guardrails, and I would not use clicks alone because a good answer can end the session without a click.

**Clarifying questions:**
- What counts as success for a search query: add to cart, a click with long dwell, no reformulation, or an explicit satisfaction signal? The metric is only as good as this definition.
- Does the results page show enough (price, stock) that users can be satisfied without clicking? That decides how much click metrics mislead.
- Where does the re-ranker sit and what is the latency budget? It sets a hard guardrail.
- What is the cost budget per query? LLM calls cost money in a way old rankers do not.
- Is randomisation by user possible? Queries from one user are correlated, so the unit matters.

**Approach:**
1. Primary: query success rate, with the unit of analysis the user (users are the independent unit; queries are clustered within them).
2. Query-level ratio metric: success queries / queries, analysed with the delta method over users (Book 1 Part 10, Q27, "Ratio metrics (CTR, revenue per session) and per-session vs per-user analysis: what goes wrong with the variance and how do you fix it (delta method)?").
3. Guardrails: p95 latency, zero-result rate, cost per query.
4. Diagnostics: click-through rate, reformulation rate, position of first click, abandonment.
5. Validate the success definition with a human or labelled sample before trusting it.
6. Segment: head versus tail queries; the LLM may help the tail and hurt navigational queries.

**Metrics:**
- Query success rate = queries meeting the success rule / queries issued.
- Zero-result rate = queries with no results / queries issued.
- p95 latency = 95th percentile of end-to-end search latency in ms.
- Cost per query = total model and serving cost / queries.
- Guardrails: latency, zero-result rate and cost each pre-agreed (illustrative cost budget 0.0025 per query).

**Risks:**
- "Good answer, no click": clicks fall while satisfaction rises. Click-only metrics punish the good case.
- The reverse also happens: a poor answer leads to abandonment that looks like a clean session.
- Per-query standard errors are too small because queries within a user are correlated.
- The LLM can be slow on rare queries and hide a tail-latency problem.

**What the interviewer scores:**
- Strong: defines success independent of clicks and explains why. Weak: "CTR up is good".
- Strong: names the ratio metric's variance problem. Weak: standard errors per query.
- Strong: cost per query as a guardrail. Weak: only quality metrics.
- Strong: a plan to validate the metric. Weak: assumes the metric is the truth.

**Example:** Illustrative. In the simulation, success per query rises from 0.501 to 0.522 (+0.021, CI +0.015 to +0.026) while click rate falls from 0.496 to 0.471. p95 latency goes from 346 to 477 ms, and cost per query 0.0020 is inside the 0.0025 budget. Weak answer: "Clicks fell 2.5 points, reject." Strong answer: "Clicks are the wrong lens here; success per query is up by 2 points; latency is the real cost to negotiate."

**Code:**
```python
# Q41 LLM re-ranker: query-level success ratio, delta method vs naive SE, guardrails (illustrative simulation)
import numpy as np
rng = np.random.default_rng(41)
n = 20_000
def arm(p_succ, p_click, mean_q=4.0, lat_mu=5.0, lat_sigma=0.35):
    # per-user query counts and a user-level propensity so queries within a user are correlated
    q = 1 + rng.poisson(mean_q - 1, n)
    prop = np.clip(rng.normal(p_succ, 0.12, n), 0.02, 0.98)
    succ = rng.binomial(q, prop)
    clicks = rng.binomial(q, np.clip(prop * p_click / p_succ, 0, 1))
    return q, succ, clicks
qc, sc, cc = arm(0.50, 0.50)
qt, st, ct = arm(0.52, 0.47)           # more queries succeed, fewer end in a click
def ratio(num, den):
    r = num.sum()/den.sum()
    m = den.mean()
    resid = num - r*den
    se_delta = np.sqrt(resid.var(ddof=1)/n)/m               # users are the unit
    return r, se_delta
rc, sec = ratio(sc, qc); rt, set_ = ratio(st, qt)
diff = rt - rc; se = np.hypot(sec, set_)
print(f"success per query: control {rc:.3f} treatment {rt:.3f} diff {diff:+.4f} CI [{diff-1.96*se:+.4f}, {diff+1.96*se:+.4f}] (user-level delta method)")
# naive SE treats every query as independent
p_c, p_t = rc, rt
nq_c, nq_t = qc.sum(), qt.sum()
se_naive = np.sqrt(p_c*(1-p_c)/nq_c + p_t*(1-p_t)/nq_t)
print(f"naive per-query SE {se_naive:.5f} vs delta-method SE {se:.5f}")
assert se > se_naive
# click-based view moves the other way
clc, clt = cc.sum()/qc.sum(), ct.sum()/qt.sum()
print(f"click per query: control {clc:.3f} treatment {clt:.3f} diff {clt-clc:+.4f}")
assert clt < clc and rt > rc
# latency guardrail p95 and cost per query (invented)
lat_c = rng.lognormal(np.log(180), 0.4, 50_000); lat_t = lat_c * 1.0 + rng.lognormal(np.log(90), 0.5, 50_000)
print(f"p95 latency ms: control {np.percentile(lat_c,95):.0f} treatment {np.percentile(lat_t,95):.0f}")
cost_per_query = 0.0020; budget = 0.0025
print(f"cost per query {cost_per_query} vs budget {budget}: ok = {cost_per_query <= budget}")
assert np.percentile(lat_t, 95) > np.percentile(lat_c, 95)
```

**Output (my run):**
```text
success per query: control 0.501 treatment 0.522 diff +0.0209 CI [+0.0154, +0.0263] (user-level delta method)
naive per-query SE 0.00250 vs delta-method SE 0.00276
click per query: control 0.496 treatment 0.471 diff -0.0254
p95 latency ms: control 346 treatment 477
cost per query 0.002 vs budget 0.0025: ok = True
```

The user-level delta-method SE (0.00276) is larger than the naive per-query SE (0.00250), so ignoring the clustering would make the result look more certain than it is.

**Follow-ups:**
- How would you check that "success" is real? Sample queries, label them, and compare the metric with the labels.
- What if latency breaches the guardrail? Cache, use the LLM on a subset of queries, or distil; the metric stays the same.

**Common mistakes:** Using CTR as the goal. Per-query standard errors. No cost guardrail. Never validating the success rule.

### Q42 ⭐⭐ 🔴 GMV rose 30% in one month, but a growth analyst notices that a coupon code was used by a cluster of new accounts. Describe how you would test for promo abuse or fraud, which guardrail metrics you would have wanted in the launch review, and how you would restate the month.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** A 30% GMV jump with a cluster of new accounts on one coupon looks like promo abuse until proven otherwise, so I would flag the cluster with a rule, check it against returns and device data, and restate the month without it.

**Clarifying questions:**
- How was the coupon distributed, and was it meant for new users only? An open coupon is easier to abuse.
- Are the orders delivered and paid, or later cancelled or returned? GMV counts orders placed, not money kept.
- What signals do we have: device ID, address, payment instrument, phone number, IP? They decide how strong a link I can build.
- How did GMV from the cluster compare with usual new-user GMV? A baseline avoids over-flagging genuine growth.
- Is there a fraud team with existing rules or labels? I should not rebuild what exists.

**Approach:**
1. Split GMV growth into the flagged cluster and everything else.
2. Test for abuse: new account age, coupon use, many accounts per device or address, repeated order patterns, high cancellation or return rates.
3. Build a transparent rule, then measure its precision and recall on a labelled sample (from the fraud team or a manual review).
4. Compare rates: coupon use by account age cohort, first-order GMV, repeat rate after the coupon.
5. Restate the month: GMV excluding flagged orders and net of returns, shown next to the reported figure.
6. Fix the process: abuse guardrails in the launch checklist.

**Metrics:**
- Flagged share = flagged GMV / total GMV.
- Rule precision = true abuse orders flagged / all orders flagged; recall = true abuse orders flagged / all abuse orders.
- Restated GMV growth = (GMV excluding flagged orders) / (prior month GMV) - 1.
- Guardrails I wanted in the launch review: share of orders per device or address, new-account share of coupon use, coupon redemption per account, cancellation and return rate, contribution margin per order.

**Risks:**
- A rule with low recall under-restates the abuse (it leaves part of the ring in).
- A rule with low precision punishes genuine users: for example students sharing a device.
- GMV is gross: coupons and returns can turn a high GMV month into a loss.
- Restating without telling the business hides the issue; show reported and restated side by side.

**What the interviewer scores:**
- Strong: concrete signals and a rule with precision and recall. Weak: "check for fraud".
- Strong: restates GMV and growth and names the margin impact. Weak: leaves GMV as reported.
- Strong: names the missing launch guardrails. Weak: only a clean-up.

**Example:** Illustrative. Last month GMV 10.5M. This month 13.67M, reported growth +30.2%. A rule (account under 7 days old, coupon used, device shared by 5+ accounts) flags 2.06M. Excluding that gives +10.6%. But the rule has recall near 0.6, so some abuse remains. Weak answer: "GMV is up 30%." Strong answer: "Reported +30%, about +11% after the rule, probably lower still because the rule misses some of the ring; here is the range."

**Code:**
```python
# Q42 GMV +30% with a coupon cluster: detect abuse, restate month (illustrative simulation)
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
# 20,000 genuine accounts, 600 ring accounts on 40 shared devices
g = pd.DataFrame({"acct": np.arange(20_000), "age_days": rng.integers(0, 720, 20_000),
                  "device": rng.integers(0, 18_000, 20_000), "ring": False})
r = pd.DataFrame({"acct": np.arange(20_000, 20_600), "age_days": rng.integers(0, 6, 600),
                  "device": 100_000 + rng.integers(0, 40, 600), "ring": True})
# fuzz the ring: 20% older accounts, 20% with a unique device
old = rng.random(600) < 0.20; r.loc[old, "age_days"] = rng.integers(8, 25, old.sum())
uni = rng.random(600) < 0.20; r.loc[uni, "device"] = 200_000 + np.arange(uni.sum())
# genuine look-alikes: 300 new accounts in a hostel sharing 10 devices, many use the welcome coupon
h = pd.DataFrame({"acct": np.arange(20_600, 20_900), "age_days": rng.integers(0, 6, 300),
                  "device": 300_000 + rng.integers(0, 10, 300), "ring": False})
acc = pd.concat([g, r, h], ignore_index=True)
orders = []
hostel = set(range(20_600, 20_900))
for row in acc.itertuples():
    if row.acct in hostel:
        for _ in range(rng.poisson(1.2)):
            orders.append((row.acct, rng.lognormal(np.log(400), 0.4), rng.random() < 0.7, rng.random() < 0.04))
    elif row.ring:
        k = rng.integers(4, 9)
        for _ in range(k):
            orders.append((row.acct, rng.normal(900, 80), rng.random() < 0.92, rng.random() < 0.55))   # coupon_used, later cancelled/returned
    else:
        k = rng.poisson(0.9)
        for _ in range(k):
            orders.append((row.acct, rng.lognormal(np.log(500), 0.5), rng.random() < 0.06, rng.random() < 0.04))
o = pd.DataFrame(orders, columns=["acct", "gmv", "coupon", "returned"]).merge(acc, on="acct")
# rule: new account (<7d) + coupon + device shared by >=5 accounts
dev_n = acc.groupby("device").acct.transform("count")
acc["shared_device"] = dev_n >= 5
o = o.merge(acc[["acct", "shared_device"]], on="acct")
o["flag"] = (o.age_days < 7) & o.coupon & o.shared_device
tot = o.gmv.sum()
print(f"total GMV {tot/1e6:.2f}M; flagged GMV {o[o.flag].gmv.sum()/1e6:.2f}M ({o.flag.mean():.1%} of orders)")
tp = (o.flag & o.ring).sum(); fp = (o.flag & ~o.ring).sum(); fn = (~o.flag & o.ring).sum()
print(f"rule on orders: precision {tp/(tp+fp):.3f} recall {tp/(tp+fn):.3f}")
# cohort contrast
print(o.groupby(pd.cut(o.age_days, [-1, 6, 30, 720])).coupon.mean().round(3).to_string())
# restate: drop flagged orders and returned orders
clean = o[~o.flag & ~o.returned].gmv.sum()
print(f"restated GMV (no flagged, no returned) {clean/1e6:.2f}M vs reported {tot/1e6:.2f}M: change {clean/tot-1:+.1%}")
prev_month = 10.5e6      # last month's gross GMV, invented
gross_clean = o[~o.flag].gmv.sum()
print(f"reported growth {tot/prev_month-1:+.1%}; growth excluding flagged orders {gross_clean/prev_month-1:+.1%}")
true_clean = o[~o.ring].gmv.sum()
print(f"growth excluding true ring orders (known only in this simulation): {true_clean/prev_month-1:+.1%}")
assert 0.29 < tot/prev_month-1 < 0.31
assert gross_clean < tot
```

**Output (my run):**
```text
total GMV 13.67M; flagged GMV 2.06M (11.0% of orders)
rule on orders: precision 0.899 recall 0.596
age_days
(-1, 6]      0.856
(6, 30]      0.481
(30, 720]    0.055
restated GMV (no flagged, no returned) 10.48M vs reported 13.67M: change -23.3%
reported growth +30.2%; growth excluding flagged orders +10.6%
growth excluding true ring orders (known only in this simulation): -1.1%
```

The rule has precision 0.899 and recall 0.596. It flags most of the ring but also some genuine hostel accounts and misses about 40% of the ring. In this simulation the true GMV excluding the ring is -1.1% versus last month, while the rule-based restatement is +10.6%: a partial rule under-restates.

**Follow-ups:**
- How would you improve recall? Link accounts by address, phone, payment instrument and behaviour, not only device.
- What do you tell leadership? Reported growth, restated range, abuse cost, and what guardrail we will add.

**Common mistakes:** Celebrating GMV. Using a rule without testing its precision and recall. Blocking genuine shared-device users. Restating once and not fixing the launch checklist.

### Q43 ⭐⭐ 🔴 The team wants to know if a new habit-forming feature improves 90-day retention, but the launch review is in three weeks. Explain how you would choose an early leading indicator, validate that it predicts 90-day retention, and state how much confidence it deserves.
**Asked at:** Product-sense and metric-design question banks (Dataford north-star and guardrail prompts, Prachub product-metrics pages, datainterview.com and Interview Query product-metrics guides); commonly reported in public guides for product-company and GCC analytics loops; search snippets only, not opened
**Say this first (1 line):** I would pick an early behaviour that history says predicts 90-day retention, check that its experiment-level effects have tracked the 90-day effects in past launches, and tell the review board it is a forecast with a range, not a result.

**Clarifying questions:**
- Do we have past cohorts and past experiments with both early and 90-day data? Without them, a leading indicator is a guess.
- What does the feature try to change: a habit (frequency), a core action, or a reminder? It tells me which early behaviour to test.
- Is the feature randomised? A comparison of adopters and non-adopters is biased.
- What decision is made at the review: ship, hold, or ship with a holdout? It sets how much confidence I need.
- What is the smallest 90-day retention change the business cares about?

**Approach:**
1. Shortlist candidates from the product logic: active days in week 1, a core action count, return on day 2 to 7.
2. User-level check: in historical cohorts, how well does the candidate predict 90-day retention (AUC, lift by decile)?
3. Experiment-level check, the one that matters: across past launches, regress the 90-day effect on the early effect, and look at R squared and the prediction interval (Book 1 Part 10, Q40, "How do you run experiments for a feature with a long-term outcome (retention, LTV) when you cannot wait months? (surrogate metrics, holdouts)").
4. Apply it: measure the early effect in the randomised test, predict the 90-day effect and its interval.
5. State the confidence: the interval, the number of past launches behind it, and the caveat that this feature may be different.
6. Keep a long-term holdout so the actual 90-day result arrives after the launch.

**Metrics:**
- Leading indicator = share of users with at least 4 active days in their first 7 days = such users / users assigned.
- Predictive check, user level = AUC of the indicator for 90-day retention.
- Predictive check, experiment level = R squared and slope of 90-day effect on early effect across past launches.
- Prediction interval = forecast 90-day effect with a 95% interval from that regression.
- Guardrails: early-period engagement shifts that do not carry over (novelty), complaint rate.

**Risks:**
- Correlation at the user level does not mean the feature's effect on the indicator transfers to retention (Book 1 Part 10, Q11, "Explain correlation vs causation. How would you establish causality for the claim 'users who use feature X retain better'?").
- A small number of past launches gives a wide interval.
- Novelty effects can lift week-1 activity without any habit forming.
- Optimising the indicator can make it stop predicting (Goodhart effect).

**What the interviewer scores:**
- Strong: separates user-level prediction from experiment-level transfer. Weak: "week-1 correlates with D90".
- Strong: quotes a prediction interval and a confidence level. Weak: a point forecast.
- Strong: plans a holdout to confirm. Weak: treats the proxy as final.
- Strong: mentions selection bias for adopters. Weak: compares adopters to non-adopters.

**Example:** Illustrative. In a simulation, active days in week 1 predicts D90 retention with an AUC of 0.679. Across 12 past launches, the slope from early effect to 90-day effect is 0.27 with R squared 0.66. A new feature with a 3-point early lift forecasts a 0.74-point 90-day lift, with a 95% prediction interval of -0.69 to +2.17 points. Weak answer: "Week-1 activity is up, so D90 will be up." Strong answer: "My best guess is about 0.7 points, the interval includes zero, so ship behind a holdout and confirm at day 90."

**Code:**
```python
# Q43 leading indicator for 90-day retention (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(43)
# (a) user-level: does early activity predict D90 retention in historical cohorts?
n = 40_000
habit = rng.normal(0, 1, n)
d7_days = np.clip(np.round(3 + 1.5*habit + rng.normal(0, 1, n)), 0, 7)     # active days in first 7
p90 = 1/(1+np.exp(-(-1.0 + 0.9*habit)))
d90 = rng.random(n) < p90
def auc(score, y):
    r = stats.rankdata(score); n1 = y.sum(); n0 = len(y)-n1
    return (r[y].sum() - n1*(n1+1)/2)/(n1*n0)
a = auc(d7_days, d90)
print(f"user-level AUC of 'active days in week 1' for D90 retention: {a:.3f}")
assert 0.62 < a < 0.78

# (b) experiment-level: 12 past launches, early effect on the indicator vs the later 90-day retention effect
k = 12
early = rng.normal(0.02, 0.03, k)                  # lift in share with >=4 active days in week 1 (points)
true90 = 0.25*early + rng.normal(0, 0.004, k)      # real 90-day effect (points)
obs90 = true90 + rng.normal(0, 0.002, k)           # measured with noise
res = stats.linregress(early, obs90)
print(f"across {k} past launches: slope {res.slope:.2f}, R^2 {res.rvalue**2:.2f}")
# prediction interval for a new feature with an early lift of 0.03
x0 = 0.03
resid = obs90 - (res.intercept + res.slope*early)
s = np.sqrt((resid**2).sum()/(k-2))
sxx = ((early-early.mean())**2).sum()
se_pred = s*np.sqrt(1 + 1/k + (x0-early.mean())**2/sxx)
t = stats.t.ppf(0.975, k-2)
pred = res.intercept + res.slope*x0
print(f"predicted D90 lift for early lift 0.03: {pred:.4f}  95% PI [{pred-t*se_pred:.4f}, {pred+t*se_pred:.4f}]")
assert pred - t*se_pred < pred < pred + t*se_pred
print("PI width in points:", round(2*t*se_pred*100, 2))
# (c) the trap: observational user-level link says nothing about causal effect of THIS feature (selection)
# users who adopt the feature are higher-habit; naive adopter vs non-adopter gap overstates
adopt = rng.random(n) < 1/(1+np.exp(-(habit-0.5)))
gap = d90[adopt].mean() - d90[~adopt].mean()
print(f"naive adopter vs non-adopter D90 gap {gap:.3f} with zero true feature effect in this simulation")
assert gap > 0.10
```

**Output (my run):**
```text
user-level AUC of 'active days in week 1' for D90 retention: 0.679
across 12 past launches: slope 0.27, R^2 0.66
predicted D90 lift for early lift 0.03: 0.0074  95% PI [-0.0069, 0.0217]
PI width in points: 2.86
naive adopter vs non-adopter D90 gap 0.140 with zero true feature effect in this simulation
```

Even with a decent user-level AUC (0.679) and R squared (0.66), the interval for the forecast is nearly 3 points wide with only 12 past launches. The naive adopter gap (0.140) shows the selection trap: it is large even though the true feature effect is zero in that simulation.

**Follow-ups:**
- How many past launches do you want? More is better; a handful gives a wide interval, so say so.
- What if no history exists? Use the early metric as a diagnostic only, and rely on a holdout for the decision.

**Common mistakes:** Picking the indicator by correlation alone. Comparing adopters with non-adopters. A point forecast with no interval. Claiming a 90-day result in three weeks.

### Q44 ⭐ 🟢 Build a baseline for an alert on daily active users that has a weekly cycle, a yearly festival pattern and steady growth. Explain how you would model the expected value, what you would do with holidays, and how you would pick the alert threshold.
**Asked at:** Metric-drop and root-cause question banks (an Interview Query metrics-drop guide, Prachub root-cause pages, Codemia 'Diagnose a drop in DAU' practice problems); commonly reported in public guides for data scientist and product analyst loops at global tech and Indian product companies; search snippets only, not opened
**Say this first (1 line):** I would model expected DAU as trend plus a weekly pattern plus festival effects on a log scale, alert on the residual in robust standard deviations, and tell the model about festival dates in advance.

**Clarifying questions:**
- How many years of clean history do we have, and are there past outages or launches inside it? They corrupt the baseline.
- Which festivals matter and do their dates come from a calendar? Moving dates must be inputs, not guesses.
- Is DAU the global total or by market? Festivals differ by region, so alerts may need to be per market.
- Do we alert on drops only or on rises too? Rises can be bot traffic or a logging bug.
- What is the cost of a miss versus a false alert?

**Approach:**
1. Work on log DAU so effects are percentages and growth is a slope.
2. Model: log DAU = intercept + trend + weekday effects + festival indicators (the day and the days before).
3. Fit on past data; exclude known outages and launch days from the fit.
4. Holidays: flag them from a calendar, give the model a dummy, and for rare ones apply a manual override rather than learning from one or two points.
5. Threshold: residual divided by a robust sd (MAD based); alert at about z of -3, tune by replaying history, and require two consecutive days for softer alerts.
6. Validate: inject known drops into held-out days and count catches and false alerts.

**Metrics:**
- Expected DAU = exp(fitted log DAU).
- z = (log actual - log expected) / robust sd.
- False alert rate = alerts on clean days / days monitored.
- Detection rate = injected drops that alerted / injected drops.
- Guardrails: model refit date, residual sd drift, share of days under manual override.

**Risks:**
- Festival dates move each year, so a "same date last year" baseline fails.
- A single yearly sample per festival is thin; keep the festival dummy simple.
- Trend breaks (a product launch) shift the baseline; refit after known structural changes.
- Fitting on data that includes undiagnosed incidents teaches the model to ignore them.

**What the interviewer scores:**
- Strong: log scale, weekday and festival terms, a robust sd. Weak: "average of last 4 weeks".
- Strong: handles moving holidays with a calendar input. Weak: "same date last year".
- Strong: tunes the threshold with replay and injected drops. Weak: picks 2 sigma by habit.

**Example:** Illustrative. A simulation has 1,000,000 base DAU, 0.06% daily growth, a weekend bump and a festival lift of 12% on the day and 6% on the two days before (moving dates). With the festival flag the model has a robust sigma of 1.3%; a threshold of z < -3 means about 3.9% below expected. It caught all 10 injected 8% drops and raised 2 false alerts over 365 clean days. Weak answer: "Compare to last week." Strong answer: "Compare to a model that knows the weekday and the festival; last-week comparisons fire a week after the festival, as the table shows."

**Code:**
```python
# Q44 DAU baseline with weekly cycle, moving festival dates and growth (illustrative simulation)
import numpy as np
rng = np.random.default_rng(44)
D = 365 * 3
t = np.arange(D)
dow = np.array([1.0, 1.0, 1.0, 1.0, 1.02, 1.08, 1.06])
fest_days = {0: [300, 301, 302], 1: [330, 331, 332], 2: [320, 321, 322]}   # moves each year (day offsets within the year)
fest = np.zeros(D)
for yr, ds in fest_days.items():
    for d in ds:
        fest[yr*365 + d] = 1
# festival lift 12% on the day, 6% in the two days before
lift = np.zeros(D)
for i in np.where(fest == 1)[0]:
    lift[i] = 0.12
    lift[max(0, i-2):i] += 0.06
true = 1_000_000 * np.exp(0.0006*t) * dow[t % 7] * (1 + lift)
y = true * np.exp(rng.normal(0, 0.012, D))

# model: log y = a + b t + dow dummies + festival indicators; fit on first two years, test on year three
def design(idx, use_fest=True):
    cols = [np.ones(len(idx)), idx.astype(float)]
    for k in range(1, 7):
        cols.append(((idx % 7) == k).astype(float))
    if use_fest:
        cols.append((lift[idx] > 0).astype(float))
    return np.column_stack(cols)
tr = np.arange(0, 730); te = np.arange(730, D)
res = {}
for flag in (False, True):
    X = design(tr, flag)
    # festival dates of the next year are known in advance from the calendar, so the flag is available at test time
    beta, *_ = np.linalg.lstsq(X, np.log(y[tr]), rcond=None)
    r = np.log(y[tr]) - X @ beta
    # robust sigma from MAD on non-festival days
    sd = 1.4826*np.median(np.abs(r - np.median(r)))
    pred = design(te, flag) @ beta
    z = (np.log(y[te]) - pred)/sd
    res[flag] = (z, sd)
    print(f"festival flag {flag}: robust sigma {sd:.4f}; share of test days with z<-3: {(z<-3).mean():.3%}; z>3: {(z>3).mean():.3%}")
# one-sided alerts; inject an 8% drop on 10 random normal days
z_f, sd_f = res[True]
normal_days = np.array([i for i in range(len(te)) if lift[te[i]] == 0])
inj = rng.choice(normal_days, 10, replace=False)
y2 = y[te].copy(); y2[inj] *= 0.92
Xte = design(te, True)
beta, *_ = np.linalg.lstsq(design(tr, True), np.log(y[tr]), rcond=None)
z2 = (np.log(y2) - Xte @ beta)/sd_f
caught = (z2[inj] < -3).sum()
print(f"threshold z<-3 (about {3*sd_f*100:.1f}% below expected): caught {caught}/10 injected 8% drops; false alerts in 365 clean days: {(z_f<-3).sum()}")
assert (res[False][0] < -3).sum() + (res[False][0] > 3).sum() > (z_f < -3).sum() + (z_f > 3).sum()
assert caught >= 8
# naive same-day-last-week rule around festival days
naive = y[te][7:]/y[te][:-7]-1                      # naive[j]: day j+7 versus day j
fday = np.array([i for i in range(len(te)) if lift[te[i]] > 0])
up = naive[fday[fday >= 7] - 7]                     # festival-affected day vs the same weekday a week earlier
down = naive[fday[fday < len(naive)]]               # one week LATER vs the festival-affected day
print(f"naive week-over-week on festival-affected days: {up.min():+.1%} to {up.max():+.1%}")
print(f"naive week-over-week one week later (comparing with the festival day): {down.min():+.1%} to {down.max():+.1%}")
assert down.min() < -0.05
```

**Output (my run):**
```text
festival flag False: robust sigma 0.0133; share of test days with z<-3: 0.274%; z>3: 1.370%
festival flag True: robust sigma 0.0131; share of test days with z<-3: 0.548%; z>3: 0.548%
threshold z<-3 (about 3.9% below expected): caught 10/10 injected 8% drops; false alerts in 365 clean days: 2
naive week-over-week on festival-affected days: +8.5% to +24.9%
naive week-over-week one week later (comparing with the festival day): -20.4% to -8.0%
```

Without the festival flag, upward residual alerts appear on 1.37% of test days; with the flag, both tails drop to 0.55%. The naive week-over-week rule shows swings of +8.5% to +24.9% on festival days and -20.4% to -8.0% one week later, which is why it cannot be used.

**Follow-ups:**
- How do you handle a festival you have never seen? Treat it as a manual override with a wider band, and learn from it afterwards.
- Why a robust sd? Past incidents would otherwise inflate it and blunt the alert.
- Related: Book 6 Part 1 elsewhere covers the noise-versus-signal reasoning for a single alert (see Q37 in this part).

**Common mistakes:** Same-date-last-year baselines. Fitting through old outages. A threshold chosen without replay. Treating the festival lift as an anomaly every year.

### Q45 ⭐ 🟢 At concept level, describe how you would compute day-7 retention from a raw events table with user_id, event_time and event_name. Explain the grain, how you define the cohort day, the join back to events, deduplication, and what could silently inflate or deflate the number.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** Day-7 retention is the share of a signup cohort that is active on exactly day 7, so I fix the grain at one row per user per day, define day 0 once in one timezone, left-join back to activity, and divide by the full mature cohort.

**Clarifying questions:**
- Exactly day 7, or any time in days 1 to 7? These are different numbers. Exact day 7 is the usual "D7". The window version is higher.
- What is the cohort event: signup, first open, or first event of any kind? It sets who is in the denominator.
- Which events count as "active"? A push received by the phone is not the user coming back. It matters because system events inflate the number.
- Which timezone defines a day: UTC, user local, or the business timezone? A late-evening user can move a whole day.
- Is the table complete up to today? A cohort whose day 7 has not happened cannot be scored.
- Are test, internal and bot users already filtered? They are usually very sticky or very dead.

**Approach:**
1. Fix the grain. Build `user_day(user_id, activity_date)` from events: filter to meaningful event names, convert to the chosen timezone, take the date, `SELECT DISTINCT`. One row per user per day.
2. Define the cohort. `d0 = MIN(date of first qualifying event)` per user (or the signup date from the users table). One row per user.
3. Keep only mature cohorts: `d0 + 7 days` must be fully before the data cut-off. Do not score a cohort whose day 7 is still in the future.
4. Left join cohort to `user_day` on `user_id` and `activity_date = d0 + 7`. Left, so non-returning users stay in the denominator.
5. Numerator: `COUNT(DISTINCT user_id)` with a match. Denominator: `COUNT(DISTINCT user_id)` in the cohort.
6. Report by cohort day (a curve for D1, D3, D7, D14) and slice by platform and channel. Sanity check: retention must be between 0 and 100%.

**Metrics:**
- D7 retention (cohort d) = users in cohort d with activity on d+7, divided by users in cohort d.
- Window retention (days 1 to 7) is a separate metric. Name it differently.
- Pooled D7 over many cohorts = sum of retained divided by sum of cohort sizes. Do not average the percentages unweighted.
- Guardrails: cohort size, share of cohorts that are mature, share of events from system names.

**Risks:**
- Inflate: duplicate rows (joining to raw events, so a user with two events on day 7 counts twice), counting system or background events, letting users with no signup event be assigned a later "first" day, bots and test users, a window metric labelled as D7.
- Deflate: scoring immature cohorts as zero, a stricter event filter on the numerator than on the cohort, a timezone cut that pushes a return a day early or late, missing events from a logging gap.
- Silent: changing the cohort definition between dashboards. Both are "D7" and neither is wrong, but they cannot be compared.

**What the interviewer scores:**
- Strong: states the grain (user-day), says DISTINCT before the join, uses a left join and the full cohort as denominator, handles immature cohorts and timezone out loud.
- Strong: separates exact day 7 from a 7-day window and picks one name for each.
- Weak: "count users who have an event 7 days after signup" with no denominator, no dedupe and no mention of what counts as an event.
- Weak: does a join on raw events and never notices retention above 100% is impossible.

**Example:** Illustrative numbers. Five users signed up on 1 Jan: A, B, C, D, E. On 8 Jan (day 7): A opens the app twice, C sends a message, E only receives a notification, B was last seen on day 3, D returns on day 8.
- Correct D7: A and C are retained, so 2 / 5 = 40%.
- Count rows instead of users: A counts twice, so 3 / 5 = 60%.
- Count the notification as activity: E joins, so 3 / 5 = 60%.
- Two more users G, H signed up on 5 Jan and the data ends on 10 Jan. Their day 7 is 12 Jan. If they stay in the denominator as non-returners: 2 / 7 = 28.6%.
- Timezone: user F first appears at 19:00 UTC on 1 Jan, which is 00:30 on 2 Jan in India. F returns at 10:00 UTC on 8 Jan. In UTC that is day 7 (retained). In India time the signup is 2 Jan and the return is 8 Jan, day 6 (not retained).
- Weak answer: "Retention is people who come back after a week." Strong answer: "Exact day 7, user-day grain, distinct users, mature cohorts only, one named timezone: 40% here, and I can show how three honest-looking mistakes give 60% or 29%."

**Code:**
```python
# Q45: day-7 retention from a raw events table (illustrative toy data, hand-checkable)
import pandas as pd

rows = [
 # user, timestamp (UTC), event_name
 ("A","2026-01-01 09:00","app_open"), ("A","2026-01-08 10:00","app_open"), ("A","2026-01-08 10:05","app_open"),
 ("B","2026-01-01 11:00","app_open"), ("B","2026-01-04 12:00","app_open"),
 ("C","2026-01-01 08:00","app_open"), ("C","2026-01-08 21:00","message_sent"),
 ("D","2026-01-01 07:00","app_open"), ("D","2026-01-09 07:00","app_open"),
 ("E","2026-01-01 06:00","app_open"), ("E","2026-01-08 06:00","notification_received"),
 ("G","2026-01-05 06:00","app_open"), ("H","2026-01-05 07:00","app_open"),
]
ev = pd.DataFrame(rows, columns=["user_id","event_time","event_name"])
ev["event_time"] = pd.to_datetime(ev["event_time"])
DATA_CUTOFF = pd.Timestamp("2026-01-10")          # data is complete up to here
SYSTEM = {"notification_received"}                 # not user activity

def d7(ev, tz="UTC", meaningful=True, dedupe=True, drop_immature=True):
    e = ev[~ev.event_name.isin(SYSTEM)] if meaningful else ev
    # cohort day = date of the user's first event, in ONE chosen timezone
    allev = ev.assign(day=ev.event_time.dt.tz_localize("UTC").dt.tz_convert(tz).dt.normalize().dt.tz_localize(None))
    cohort = allev.groupby("user_id").day.min().rename("d0").reset_index()
    act = e.assign(day=e.event_time.dt.tz_localize("UTC").dt.tz_convert(tz).dt.normalize().dt.tz_localize(None))
    act = act[["user_id","day"]]
    if dedupe: act = act.drop_duplicates()         # grain: one row per user per day
    cohort["target"] = cohort.d0 + pd.Timedelta(days=7)
    if drop_immature:                              # day 7 must have fully happened
        cohort = cohort[cohort.target + pd.Timedelta(days=1) <= DATA_CUTOFF]
    j = cohort.merge(act, left_on=["user_id","target"], right_on=["user_id","day"], how="left")
    retained = j.day.notna().sum() if not dedupe else j.user_id[j.day.notna()].nunique()
    n = cohort.user_id.nunique()
    return int(retained), int(n), round(float(retained) / n, 4)

r = d7(ev)
print("strict D7, meaningful, deduped, mature cohorts:", r)
assert r[0] == 2 and r[1] == 5 and r[2] == 0.4

r = d7(ev, dedupe=False)
print("no dedupe (row count in numerator):", r)
assert r[0] == 3 and r[2] == 0.6       # A's duplicate row counted twice

r = d7(ev, meaningful=False)
print("count notification_received as activity:", r)
assert r[0] == 3 and r[2] == 0.6

r = d7(ev, drop_immature=False)
print("keep immature cohort in denominator:", r)
assert r[1] == 7 and r[2] == round(2/7, 4)

# "within 7 days" (any day 1..7) is a different metric
e2 = ev[~ev.event_name.isin(SYSTEM)].assign(day=lambda d: d.event_time.dt.normalize())
c = ev.groupby("user_id").event_time.min().dt.normalize().rename("d0").reset_index()
c = c[c.d0 == pd.Timestamp("2026-01-01")]
j = c.merge(e2[["user_id","day"]].drop_duplicates(), on="user_id")
j["k"] = (j.day - j.d0).dt.days
within7 = j[(j.k >= 1) & (j.k <= 7)].user_id.nunique() / len(c)
print("within-7-days (days 1..7) retention:", within7)
assert abs(within7 - 0.60) < 1e-9

# timezone flip: one user, signup 19:00 UTC Jan 1 (00:30 IST Jan 2), returns 10:00 UTC Jan 8
f = pd.DataFrame({"user_id":["F","F"],"event_time":pd.to_datetime(["2026-01-01 19:00","2026-01-08 10:00"]),"event_name":["app_open"]*2})
ru = d7(f, tz="UTC", drop_immature=False)
ri = d7(f, tz="Asia/Kolkata", drop_immature=False)
print("user F retained at D7 in UTC:", ru[0], "| in IST:", ri[0])
assert ru[0] == 1 and ri[0] == 0
```

**Output (my run):**
```text
strict D7, meaningful, deduped, mature cohorts: (2, 5, 0.4)
no dedupe (row count in numerator): (3, 5, 0.6)
count notification_received as activity: (3, 5, 0.6)
keep immature cohort in denominator: (2, 7, 0.2857)
within-7-days (days 1..7) retention: 0.6
user F retained at D7 in UTC: 1 | in IST: 0
```

**Follow-ups:**
- What about "day 7" for a product used only on weekdays? Use a window such as days 6 to 8 or "week 1" retention, name it, and say it in the definition. Exact day 7 punishes weekday-only products on a weekend.
- How do you extend this to a retention curve? Same cohort, join at offsets 1, 3, 7, 14, 30; one row per cohort and offset; cohorts not yet mature at an offset show blank, not zero.
- SQL shape? A CTE for `user_day`, a CTE for `cohort`, then a `LEFT JOIN` on `activity_date = d0 + INTERVAL 7 DAY`. Book 3 owns the SQL detail.

**Common mistakes:** Joining to raw events and counting rows. Using an inner join, which drops non-returners and makes retention 100%. Counting push-received or background events. Scoring cohorts whose day 7 has not happened. Mixing timezones between cohort day and activity day. Averaging cohort percentages without weights.

### Q46 ⭐ 🟡 At concept level, describe how you would write a query for week-over-week DAU by platform that does not lie. Cover the date spine for days with no events, window functions versus self-joins, timezone handling, and why partial current-week data distorts the last point.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** I build DAU as distinct users per platform per day, force every platform-day to exist with a date spine, join each day to the same weekday a week earlier, use one named timezone, and never compare a partial current week with a full last week.

**Clarifying questions:**
- WoW of what: average DAU over the week, or weekly active users (WAU)? They are different. WAU is distinct users over seven days and is not the sum of DAU.
- Which timezone is a "day"? It moves users between days, and between the last day and today.
- What is a "platform" for a user on two devices: first, last, or counted in both? Platform rows will not add up to the total if users appear twice.
- What counts as active: any event or only a meaningful one? Background events inflate DAU.
- Is the latest day complete? Late events and the batch schedule decide whether the last point is real (see Q47 in this part).

**Approach:**
1. Grain: `daily_active(platform, day, user_id)` with `SELECT DISTINCT`, day computed in the agreed timezone. Then `COUNT(*)` per platform per day.
2. Date spine: generate every date and every platform, then LEFT JOIN the counts and fill missing with 0 (or NULL if I know it was an outage). A day with no events otherwise has no row, so it vanishes from charts and from averages.
3. Week-over-week: join each day to `day - 7` (self-join on date), or `LAG(dau, 7)` over `PARTITION BY platform ORDER BY day`. The window version is only right after the spine, because it counts rows. A self-join on the date is safe either way.
4. Weekly view: average DAU per week, or true WAU. Never "sum DAU per week" as a user count.
5. Partial week: drop the incomplete week or compare like with like (this Mon to Wed against last Mon to Wed). Grey out the last point.
6. Add a total row computed as distinct users across platforms, not the sum of platform rows.

**Metrics:**
- DAU(platform, day) = distinct user_id with a qualifying event on that day in that platform.
- WoW % = (DAU_this - DAU_same_weekday_last_week) / DAU_same_weekday_last_week.
- Weekly average DAU = sum of daily DAU over 7 days divided by 7 (zeros included).
- Guardrails: number of rows per platform-day (must equal the spine), share of the last day's data that is complete, platform sum minus total distinct (overlap).

**Risks:**
- Missing days drop out of the average and make it look higher. Lagging by 7 rows picks the wrong day after a gap.
- Partial week compared with a full week mixes weekday and weekend. If weekends are lower, a Mon to Wed average looks like growth.
- Timezone: a user active at 20:00 and 02:00 UTC is two UTC days but one India day.
- Self-join on a big table is expensive. A spine plus window is cheaper, but only when the spine is complete.
- Platform sum double counts people on two devices.

**What the interviewer scores:**
- Strong: names the user-day grain, the spine, row lag versus date lag, and the partial-week trap without being asked.
- Strong: picks like-for-like comparison and says the timezone is a business decision.
- Weak: `COUNT(DISTINCT user_id) GROUP BY week` and nothing else.
- Weak: uses `LAG(7)` on data with missing days and never mentions it.

**Example:** Illustrative numbers. Android DAU is 100 on weekdays, 70 on Saturday and 60 on Sunday, flat week to week, so the weekly average is (500 + 130) / 7 = 90. This week we only have Monday to Wednesday, average 100.
- Naive WoW: 100 / 90 - 1 = +11.1%. Nothing happened. It is the weekday mix.
- Like for like: Mon to Wed this week (100) against Mon to Wed last week (100) is 0%.
- iOS has a tracking outage on Thursday: no rows at all. Without a spine, the week average is over 6 rows (49.0). With the spine it is over 7 days (42.0) and the hole is visible. Lagging 7 rows from iOS Tuesday 13 Jan picks Monday 5 Jan (50) instead of Tuesday 6 Jan (52).
- Weak answer: "Group by week and compare." Strong answer: "Spine, date-lag, one timezone, and the last week is compared only on the days that exist."

**Code:**
```python
# Q46: week-over-week DAU by platform that does not lie (illustrative toy data)
import pandas as pd

days = pd.date_range("2026-01-05", "2026-01-18")            # Mon 5 Jan .. Sun 18 Jan
base = {"android": [100]*5 + [70, 60], "ios": [50, 52, 54, 56, 58, 40, 40]}  # Mon..Sun, each platform flat week over week
rows = []
for p, pat in base.items():
    for d in days:
        if p == "ios" and d == pd.Timestamp("2026-01-08"):    # tracking outage: no rows at all
            continue
        for i in range(pat[d.dayofweek]):
            rows.append((f"{p[0]}{d:%m%d}_{i}", p, d + pd.Timedelta(hours=12)))
ev = pd.DataFrame(rows, columns=["user_id", "platform", "ts"])
ev = ev[ev.ts < pd.Timestamp("2026-01-15")]                 # data cut: this week only through Wed 14 Jan

# 1) DAU = distinct users per platform per day, then a date spine so empty days are visible
dau = ev.assign(day=ev.ts.dt.normalize()).groupby(["platform", "day"]).user_id.nunique()
spine = pd.MultiIndex.from_product([["android", "ios"], pd.date_range("2026-01-05", "2026-01-14")], names=["platform", "day"])
dau_s = dau.reindex(spine, fill_value=0)
print("rows without spine:", len(dau), "| rows with spine:", len(dau_s))
assert len(dau) == 19 and len(dau_s) == 20
assert dau_s[("ios", pd.Timestamp("2026-01-08"))] == 0

# 2) week-over-week: lag by 7 DAYS (join on date - 7), not by 7 ROWS
s = dau_s.rename("dau").reset_index()
selfjoin = s.merge(s.assign(day=s.day + pd.Timedelta(days=7)), on=["platform", "day"], how="left", suffixes=("", "_prev"))
window = s.assign(dau_prev=s.groupby("platform").dau.shift(7))   # valid only because the spine makes rows = days
assert (selfjoin.dau_prev.fillna(-1).values == window.dau_prev.fillna(-1).values).all()
# without the spine, shift(7) rows picks the wrong day after the gap
nos = dau.rename("dau").reset_index()
nos["dau_prev_rows"] = nos.groupby("platform").dau.shift(7)
wrong = nos[(nos.platform == "ios") & (nos.day == "2026-01-13")].dau_prev_rows.iloc[0]
right = s[(s.platform == "ios") & (s.day == "2026-01-13")].merge(selfjoin, on=["platform", "day"]).dau_prev.iloc[0]
print("ios Tue 13 Jan, last week's value: shift(7 rows) =", wrong, "| join on date-7 =", right)
assert wrong == 50.0 and right == 52.0

# 3) the partial-week trap: this week has Mon-Wed only
w1 = dau_s.loc["android"].loc["2026-01-05":"2026-01-11"].mean()
w2_partial = dau_s.loc["android"].loc["2026-01-12":"2026-01-14"].mean()
naive = w2_partial / w1 - 1
w1_same = dau_s.loc["android"].loc["2026-01-05":"2026-01-07"].mean()
fair = w2_partial / w1_same - 1
print(f"android avg DAU: last full week {w1:.1f}, this week Mon-Wed {w2_partial:.1f}, naive WoW {naive:+.1%}")
print(f"like-for-like (Mon-Wed vs Mon-Wed): {fair:+.1%}")
assert round(w1, 1) == 90.0 and w2_partial == 100.0 and round(naive, 3) == 0.111 and fair == 0

# 4) gap visible on iOS: average with spine vs without
i_spine = dau_s.loc["ios"].loc["2026-01-05":"2026-01-11"].mean()
i_obs = dau.loc["ios"].loc["2026-01-05":"2026-01-11"].mean()
print(f"ios week-1 avg DAU: with spine {i_spine:.1f}, over observed rows only {i_obs:.1f}")
assert round(i_spine, 1) == 42.0 and round(i_obs, 1) == 49.0

# 5) timezone: same events, different day boundaries
tz = pd.DataFrame({"user_id": ["u"]*2, "ts": pd.to_datetime(["2026-01-05 20:00", "2026-01-06 02:00"])})
utc_days = tz.ts.dt.normalize().nunique()
ist_days = tz.ts.dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata").dt.normalize().nunique()
print("one user, two events: active days in UTC =", utc_days, "| in IST =", ist_days)
assert utc_days == 2 and ist_days == 1
```

**Output (my run):**
```text
rows without spine: 19 | rows with spine: 20
ios Tue 13 Jan, last week's value: shift(7 rows) = 50.0 | join on date-7 = 52.0
android avg DAU: last full week 90.0, this week Mon-Wed 100.0, naive WoW +11.1%
like-for-like (Mon-Wed vs Mon-Wed): +0.0%
ios week-1 avg DAU: with spine 42.0, over observed rows only 49.0
one user, two events: active days in UTC = 2 | in IST = 1
```

**Follow-ups:**
- Window function or self-join? Window is faster and cleaner on a complete spine. Self-join on date is safer when days can be missing, at the cost of a join. Use a range window by interval where the engine supports it.
- How do you show the last point? Mark it provisional, or plot only completed days. Never alert on it (Q47 covers the dip).
- Why can platform DAU not be summed? A user on phone and tablet is in both rows, so the sum is above the distinct total.

**Common mistakes:** No spine, so missing days vanish. `LAG` over rows with gaps. Comparing a partial week with a full one. Mixing UTC for the day and local time for the user. Summing platforms for the total. Using `COUNT(*)` instead of distinct users.

### Q47 ⭐ 🟡 A daily dashboard shows a dip in the last hours of every day that fills in by the next morning. Explain how late-arriving events, time zones and batch loads cause this, how you would confirm it, and how you would change the reporting so no one raises false alarms.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** A dip that always heals overnight is almost never users. It is data that has not arrived yet, so I prove it by comparing event time with arrival time, and then I stop showing or alerting on hours that are not complete.

**Clarifying questions:**
- Is the chart bucketed by event time (when it happened) or load time (when it landed)? A dip that heals only exists in the first.
- How are events sent: real-time stream, or phone batches uploaded later? Offline phones send late. It sets the lag shape.
- When does the batch or ETL job run, and in which timezone? A job cut at midnight UTC shows a "day" ending at 05:30 India time.
- Does the dip show on every platform and every day, or only some? Every day, same hours, points to the pipeline. One platform points to one SDK.
- Who reacts to the dashboard, and is there an alert on it? It tells me how costly a false alarm is.

**Approach:**
1. State the hypothesis: the newest hours are incomplete, not low. Three causes. (a) Late events: phones offline, SDK retries, queue backlog. (b) Batch schedule: the last load has not run, so the latest hours are only partly loaded. (c) Timezone cut: the dashboard day is in one zone and the load cut-off in another, so a slice of "today" is not in yet. The hour still in progress is also partial by definition.
2. Confirm with data. Store both `event_time` and `ingest_time`. Compute lag percentiles and the share of events visible by age (age = snapshot time minus event time). If the share rises with age and is about 100% after N hours, the dip is lag. Take two snapshots of the same hour (now and tomorrow) and compare. Check the dip is the same shape on other days.
3. Rule out a real drop. Compare with a source that is not lagged (server-side logs, payments). If those are flat while the app events dip, it is arrival delay.
4. Fix the reporting. Show a "complete through" watermark and grey or cut hours younger than the age at which about 99% of events have arrived. Add a completeness rate next to every latest point.
5. Fix the alerting. Alert only on hours past the watermark, or alert on a nowcast: `visible / completeness(age)`, with a wider band for young hours.
6. Fix the pipeline where cheap. More frequent loads, a late-arrival window that reprocesses the last 1 to 2 days, and the same timezone everywhere.

**Metrics:**
- Lag = ingest_time - event_time (percentiles p50, p90, p99).
- Completeness(age a) = share of events with lag <= a.
- Completeness at hour h = events visible now for hour h / events visible in the final count for hour h.
- Nowcast = visible count / completeness(age of that hour).
- Guardrails: false-alarm rate of the alert, size of revisions between first view and final.

**Risks:**
- Gating at p99 hides a real outage for several hours. Keep a separate fast alert on raw arrival volume (events ingested per minute), which cares about the pipe, not the hour's content.
- Nowcasting assumes the lag shape is stable. A release that changes batching changes it.
- Lag differs by platform and by country. Use one curve per segment.
- Changing the dashboard silently moves numbers people have already quoted. Label the change.

**What the interviewer scores:**
- Strong: separates event time from ingest time, proposes a measurable confirmation, and fixes both the chart and the alert.
- Strong: names the in-progress hour as a separate partial effect.
- Weak: "check if users really dropped" with no test; or "just wait until morning".
- Weak: only fix is a pipeline rewrite, with no change to what people see.

**Example:** Illustrative simulation, flat truth of about 1,000 events an hour; 30% of events come from phones that upload later (mean 2 hours), the rest arrive within minutes. At 23:30 the dashboard shows, against the final count the next morning: hour 18 at 97%, hour 19 at 95%, hour 20 at 92%, hour 21 at 88%, hour 22 at 80%. Hour 23 is only half elapsed (294 of 936). So the right edge slopes down every night and "fills in" by morning, with the real traffic completely flat.
- The completeness curve: 76.6% of events are visible within 30 minutes, 81.8% within 1 hour, 98.5% within 6 hours, 99.9% within 12 hours. The p99 lag is 6.8 hours.
- Nowcast (visible / completeness at that age) lands within 2% of the final number for hours 18 to 22.
- Weak answer: "Traffic drops in the evening, let me look at causes." Strong answer: "It heals every night, so I compare event time with arrival time; the newest hours are 80% complete, so I will hide them behind a watermark and alert on the nowcast."

**Code:**
```python
# Q47: late-arriving events make the newest hours look like a dip (illustrative simulation)
import numpy as np
rng = np.random.default_rng(47)

HOURS = 24 * 8                       # 8 days of hourly data
PER_HOUR = 1000                      # true events per hour (flat on purpose: any dip is fake)
n = rng.poisson(PER_HOUR, HOURS)
event_h = np.repeat(np.arange(HOURS), n) + rng.random(n.sum())          # event time in hours
offline = rng.random(n.sum()) < 0.30                                    # 30% sit on the phone first
lag_h = np.where(offline, rng.exponential(2.0, n.sum()), rng.exponential(0.05, n.sum()))
ingest_h = event_h + lag_h                                              # when the warehouse sees it
print("lag percentiles in hours p50/p90/p99:", np.round(np.percentile(lag_h, [50, 90, 99]), 2))

def visible_per_hour(now_h):
    """what the dashboard shows at time now_h: events ingested by then, bucketed by EVENT hour"""
    m = ingest_h <= now_h
    return np.bincount(event_h[m].astype(int), minlength=HOURS)[:HOURS]

# dashboard viewed at 23:30 on the last full day (day index 6): look at its last hours
now = 24 * 7 - 0.5
shown = visible_per_hour(now)
final = visible_per_hour(1e9)
last = range(24 * 7 - 6, 24 * 7 - 1)       # completed hours 18..22; hour 23 is still in progress at 23:30
print("hour 23 is still running at 23:30, so only half of it can exist:", shown[24*7-1], "of", final[24*7-1])
print("hour-of-day | shown at 23:30 | final next morning | shown/final")
for h in last:
    print(f"{h % 24:>11} | {shown[h]:>14} | {final[h]:>18} | {shown[h] / final[h]:.2f}")
ratio = np.array([shown[h] / final[h] for h in last])
assert ratio[-1] < 0.85 and ratio[0] > 0.9 and ratio[-1] == ratio.min()   # newest completed hour is the thinnest
assert abs(final[24*7 - 2] / PER_HOUR - 1) < 0.1                               # truth is flat: ~1000

# confirm the cause: completeness by age, learned from earlier days
ages = np.array([0.5, 1, 2, 4, 6, 12])
comp = np.array([np.mean(lag_h <= a) for a in ages])
print("share of events visible by age (h):", dict(zip(ages.tolist(), np.round(comp, 3).tolist())))
assert comp[0] < 0.9 and comp[-1] > 0.99

# fix 1: only report hours older than the p99 lag (the watermark)
p99 = np.percentile(lag_h, 99)
print("watermark age (h) to report at p99 completeness:", round(float(p99), 1))
# fix 2: nowcast = shown / completeness(age), with an interval flag, for alerting
def comp_at(age): return np.mean(lag_h <= age)
est = [shown[h] / comp_at(now - (h + 0.5)) for h in last]
err = [abs(e / final[h] - 1) for e, h in zip(est, last)]
print("nowcast error vs final by hour:", np.round(err, 3).tolist())
assert max(err) < 0.1
```

**Output (my run):**
```text
lag percentiles in hours p50/p90/p99: [0.06 2.22 6.8 ]
hour 23 is still running at 23:30, so only half of it can exist: 294 of 936
hour-of-day | shown at 23:30 | final next morning | shown/final
         18 |            916 |                943 | 0.97
         19 |            914 |                960 | 0.95
         20 |            900 |                983 | 0.92
         21 |            831 |                939 | 0.88
         22 |            830 |               1034 | 0.80
share of events visible by age (h): {0.5: 0.766, 1.0: 0.818, 2.0: 0.889, 4.0: 0.959, 6.0: 0.985, 12.0: 0.999}
watermark age (h) to report at p99 completeness: 6.8
nowcast error vs final by hour: [0.004, 0.007, 0.018, 0.005, 0.018]
```

**Follow-ups:**
- Is a bigger watermark always better? No. It delays real incidents. Pair a slow, accurate metric with a fast pipeline-health alert.
- What if the lag is also changing over time? Track lag percentiles as a monitored metric. A rising p99 lag is itself an incident.
- How do you restate numbers? Reprocess a rolling late-arrival window (for example two days), and show "provisional" versus "final" with a revision history.

**Common mistakes:** Treating the dip as real and starting a root-cause hunt. Bucketing on load time and event time in different charts. Hiding the cause by smoothing. Alerting on the newest hour. Forgetting the hour still in progress. Using one lag curve for all platforms.

### Q48 ⭐ 🟡 A publisher platform launches an AI summary box. Click-through to articles falls 18%, but time on site per session rises and satisfaction scores improve. Explain which metrics you would pick to judge the feature for users and for publishers, and what the guardrail should be.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Falling clicks is not automatically bad here. I judge the box on whether users got their answer, and I protect publishers with a guardrail on referral clicks and revenue, because the feature is only sustainable if the publishers it summarises still get value.

**Clarifying questions:**
- Is this a randomised test, or a launch with before and after? It decides how much I can trust the -18%.
- What does CTR mean here: sessions with an article click divided by sessions? Or clicks per impression? The denominator changes the story.
- Is "satisfaction" a survey, thumbs, or a proxy? Who answers it? Only people who stayed on the page may answer.
- How does the publisher earn from us: ad share, subscriptions, referral traffic? It sets the publisher metric.
- Is the summary produced from the publisher's content, and are sources shown and linked? It drives both trust and clicks.
- Why did time per session rise: reading the summary, or being confused and searching again?

**Approach:**
1. Say the trade-off out loud: fewer clicks can be "good abandonment" (answer found) or "bad abandonment" (gave up). Click-based metrics cannot tell them apart.
2. User metrics: successful-session rate (clicked and stayed, or no-click and satisfied or no reformulation within the session), task completion, reformulation rate, 7-day return, summary accuracy from a sampled human review.
3. Publisher metrics: article click sessions per 100 sessions, publisher revenue per 100 sessions, source-link click rate inside the box, share of traffic from the platform to each publisher, and complaint or opt-out rate.
4. Platform metrics: cost per summary, latency. Keep them as a guardrail, not the goal.
5. Guardrails: publisher referral clicks and revenue must not fall more than a pre-agreed amount (say 10%); summary error rate under a bar; no drop in 7-day return.
6. Decision: if users win and publishers breach the guardrail, do not ship as is. Change the design (prominent source links, "read more") and re-test. Check whether the time-on-site rise is real use by looking at re-searches.

**Metrics:**
- CTR = sessions with an article click / sessions. Report relative change.
- Successful-session rate = (good-click sessions + satisfied no-click sessions) / sessions.
- Publisher revenue per 100k sessions = click sessions x revenue per click session.
- Guardrail: relative loss in publisher click sessions <= 10% (illustrative threshold, set with partners).
- Summary error rate = sampled summaries with a wrong or unsupported claim / sampled summaries.

**Risks:**
- Survey bias: only people who read the summary answer. Sample no-click sessions randomly.
- Time on site is ambiguous. More time can mean more confusion.
- Short-run user happiness hurts the supply side over time, and the publishers can block the crawler.
- Novelty: satisfaction often looks best in week one.
- A good summary of a wrong article is still wrong. Accuracy needs human labels.

**What the interviewer scores:**
- Strong: separates good from bad abandonment and defines a no-click success metric.
- Strong: gives the publisher a metric and a number-based guardrail, and says what to do when it breaches.
- Weak: "CTR fell so it is bad", or "satisfaction rose so ship".
- Weak: ignores the supply side or cost.

**Example:** Illustrative numbers, 100,000 sessions per arm. Click sessions: 20,000 to 16,400 (CTR 20.0% to 16.4%, which is -18%). A survey of 2,000 no-click sessions per arm gives 55.1% satisfied versus 70.0% (my run, with sampling error about 3 points). Assume 85% of clicks are good ones.
- Successful-session rate: 0.61 to 0.725.
- Publisher revenue at an assumed Rs 4 per click session: Rs 80,000 to Rs 65,600 per 100k sessions (-18%).
- Guardrail 10%: breach. To get inside it, each 100k sessions needs 1,600 more click sessions, so the design must make the source links work harder.
- Weak answer: "Clicks fell 18%, roll it back." Strong answer: "Users succeed more (61% to 72.5%) but publishers lose 18%, above my 10% guardrail, so I ship the next variant with stronger source links, not this one."

**Code:**
```python
# Q48: AI summary box. Click-through -18%, satisfaction up. Illustrative numbers only.
import numpy as np
rng = np.random.default_rng(48)

N = 100_000                                   # sessions per arm
ctr_c, ctr_t = 0.200, 0.164                   # share of sessions with an article click
assert round(ctr_t / ctr_c - 1, 3) == -0.18
click_c, click_t = int(N * ctr_c), int(N * ctr_t)
noclick_c, noclick_t = N - click_c, N - click_t
print("click sessions:", click_c, "->", click_t, "| no-click sessions:", noclick_c, "->", noclick_t)

# survey on no-click sessions (n=2000 per arm, true satisfied rates 55% vs 70%)
sat_c = rng.binomial(2000, 0.55) / 2000
sat_t = rng.binomial(2000, 0.70) / 2000
se = np.sqrt(sat_c*(1-sat_c)/2000 + sat_t*(1-sat_t)/2000)
diff = sat_t - sat_c
print(f"no-click satisfied: {sat_c:.3f} -> {sat_t:.3f}, diff {diff:+.3f}, 95% CI +/- {1.96*se:.3f}")
assert diff - 1.96*se > 0.10

# user-side metric: successful sessions = clicked and stayed (assume 85% of clicks are good) + satisfied no-click
good_click = 0.85
succ_c = (click_c*good_click + noclick_c*0.55) / N
succ_t = (click_t*good_click + noclick_t*0.70) / N
print(f"successful-session rate: {succ_c:.3f} -> {succ_t:.3f}")
assert round(succ_c, 3) == 0.610 and round(succ_t, 3) == 0.725      # 0.17+0.44 ; 0.1394+0.5852 = 0.7246 -> 0.725

# publisher side: value per 100k sessions at an assumed Rs 4 of publisher revenue per click session
rev_c, rev_t = click_c * 4, click_t * 4
print(f"publisher revenue per 100k sessions (Rs): {rev_c} -> {rev_t} ({rev_t/rev_c-1:+.0%})")
assert rev_c == 80_000 and rev_t == 65_600 and round(rev_t/rev_c - 1, 2) == -0.18

# guardrail rule: ship only if publisher click share loss <= 10% unless source-link clicks recover it
loss = 1 - click_t / click_c
guard = 0.10
print(f"publisher click loss {loss:.0%} vs guardrail {guard:.0%} ->", "BREACH, fix source links" if loss > guard else "ok")
assert loss > guard
# what source-link prominence must recover to get back inside the guardrail
need = click_c * (1 - guard) - click_t
print("extra click sessions per 100k needed to meet the guardrail:", int(need))
assert int(need) == 1600
```

**Output (my run):**
```text
click sessions: 20000 -> 16400 | no-click sessions: 80000 -> 83600
no-click satisfied: 0.551 -> 0.700, diff +0.148, 95% CI +/- 0.030
successful-session rate: 0.610 -> 0.725
publisher revenue per 100k sessions (Rs): 80000 -> 65600 (-18%)
publisher click loss 18% vs guardrail 10% -> BREACH, fix source links
extra click sessions per 100k needed to meet the guardrail: 1600
```

**Follow-ups:**
- Which is the north star? A user success metric for the product, with publisher value as a hard constraint. A one-sided north star breaks the ecosystem.
- How would you test it? Randomise users, run long enough for novelty to fade, and keep a long-term holdout (Book 1 Part 10, Q24, heading: "What is a holdout / long-term holdout group and why would a company keep one?"). For AI-feature specifics see Book 1 Part 10, Q17 ("AI-era: How would you A/B test an LLM-powered feature...").
- What if time on site rose but successful sessions did not? Then the rise is friction, not value.

**Common mistakes:** Treating CTR as the only success metric. Reading time on site as always good. Surveying only people who clicked. No publisher metric. Picking a guardrail number with no reason or no action when it breaches.

### Q49 ⭐ 🟡 A GenAI assistant raised weekly task completions by 12%, but inference cost per active user doubled to Rs 6 a month. Explain how you would frame a unit-economics metric, what cost guardrail you would set, and how you would find the segment where the feature does and does not pay for itself.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** I judge the assistant on net value per active user: the value of the extra tasks completed minus the inference cost, and I find the segments where cost per extra completion is above the value of a completion.

**Clarifying questions:**
- What is one extra completed task worth in rupees (retention, conversion, ad or fee revenue, support saved)? Without it there is no break-even.
- Why did cost double: longer prompts, a bigger model, more calls per task, or more heavy users? It points to the fix.
- Is the +12% from a randomised test? A raw before and after mixes in seasonality.
- How is "active user" defined? If the feature drove inactive users out, cost per active user rises with no change in total cost.
- Is the Rs 6 average over all active users or only users who used the assistant? The denominator changes the number.
- Is cost per month fixed per user, or heavy-tailed by usage? Tails decide whether a cap or routing helps.

**Approach:**
1. Frame unit economics: contribution per active user per month = (extra completions x value per completion) - inference cost per user.
2. Define a break-even rule: cost per extra completion <= value per completion. Report overall and by segment.
3. Segment by usage intensity, plan, task type and cohort (not by outcome). Use incremental completions from the experiment control, not raw totals.
4. Find the segments that lose: usually light users (small uplift, fixed overhead) and a few very costly task types.
5. Cost guardrail: cost per extra completion <= value (with a margin), and total AI cost <= a stated share of the revenue attributable to the feature. Add a hard cap alert on cost per user at the tail (p95).
6. Levers: route simple tasks to a cheaper model, cache, shorten context, cap or throttle heavy free usage, move heavy use to a paid plan. Then re-measure uplift, since a cheaper path may lower quality.

**Metrics:**
- Extra completions per user = completions with the assistant - completions in control (same period).
- Net per active user = extra completions x value - inference cost.
- Cost per extra completion = inference cost per user / extra completions per user.
- Guardrails: p95 cost per user, quality (task success and error rate) so cost cuts do not hide a drop, and total cost.

**Risks:**
- Value per completion is an assumption. Show a range, not a point.
- Averages hide the tail. A 6 rupee average can be 3 for most and 24 for a few.
- Cost cuts reduce quality and the uplift quietly.
- Uplift measured on engaged users who opt in overstates the effect for everyone. Use the randomised comparison.
- The per-active denominator can move for reasons that are not cost.

**What the interviewer scores:**
- Strong: turns "cost doubled" into a break-even with a rupee value for the benefit, and splits by segment.
- Strong: names levers and a guardrail with an owner and an action.
- Weak: "cost is too high, reduce it" or "uplift is good, ignore cost."
- Weak: segments by outcome (post-treatment) instead of by pre-launch traits.

**Example:** Illustrative numbers. Value of an extra completion is Rs 3. Three user segments:

| Segment | Share of users | Extra completions per user per month | Cost per user | Value | Net |
|---|---|---|---|---|---|
| Light | 60% | 0.4 | Rs 3 | Rs 1.2 | -1.8 |
| Mid | 30% | 2.4 | Rs 6 | Rs 7.2 | +1.2 |
| Heavy | 10% | 8.2 | Rs 24 | Rs 24.6 | +0.6 |

- Overall: baseline completions 14.8 per user, extra 1.78 (+12.0%), cost Rs 6.00 per active user, net -Rs 0.66 per user per month.
- Cost per extra completion: light 7.5, mid 2.5, heavy 2.93. Overall 3.37 against value 3. Overall loses, mid and heavy pay for themselves.
- If the large model is not served to light users, net per original user becomes +Rs 0.42 (assuming no other change, and ignoring the lost light-user uplift's side benefits).
- Weak answer: "Raise the revenue or cut the cost." Strong answer: "Break-even is Rs 3 per extra completion. We are at 3.37 overall, light users are at 7.5. I route light users to a small model or free-tier limit and re-test uplift."

**Code:**
```python
# Q49: unit economics of a GenAI assistant by segment (illustrative numbers)
import pandas as pd

VALUE = 3.0   # Rs of value per extra completed task (assumed: retained revenue + conversion), illustrative
seg = pd.DataFrame({
    "segment":  ["light", "mid", "heavy"],
    "share":    [0.60, 0.30, 0.10],       # share of active users
    "base":     [8.0, 20.0, 40.0],         # completions per user per month without the assistant
    "extra":    [0.4, 2.4, 8.2],           # extra completions per user per month with it
    "cost":     [3.0, 6.0, 24.0],          # inference Rs per user per month
})
seg["uplift_pct"] = seg.extra / seg.base * 100
seg["value"] = seg.extra * VALUE
seg["net"] = seg.value - seg.cost
seg["cost_per_extra"] = seg.cost / seg.extra
print(seg.round(2).to_string(index=False))

tot_base = (seg.share * seg.base).sum()
tot_extra = (seg.share * seg.extra).sum()
tot_cost = (seg.share * seg.cost).sum()
tot_net = (seg.share * seg.net).sum()
print(f"\noverall uplift {tot_extra/tot_base:.1%}, cost per active user Rs {tot_cost:.2f}, "
      f"extra completions/user {tot_extra:.2f}, net per user Rs {tot_net:.2f}, cost per extra completion Rs {tot_cost/tot_extra:.2f}")
assert round(tot_extra / tot_base, 2) == 0.12 and round(tot_cost, 2) == 6.0
assert round(tot_extra, 2) == 1.78 and round(tot_net, 2) == -0.66 and round(tot_cost / tot_extra, 2) == 3.37

# who pays for itself: cost per extra completion below VALUE
pays = seg[seg.cost_per_extra <= VALUE].segment.tolist()
print("segments with cost per extra completion <= Rs", VALUE, ":", pays)
assert pays == ["mid", "heavy"]

# what-if: stop serving the light segment with the big model (serve nothing, so cost 0 and extra 0)
keep = seg[seg.segment != "light"]
net_keep = (keep.share * keep.net).sum()              # per original active user
print(f"net per original active user if light is not served: Rs {net_keep:.2f}")
assert round(net_keep, 2) == 0.42
```

**Output (my run):**
```text
segment  share  base  extra  cost  uplift_pct  value  net  cost_per_extra
  light    0.6   8.0    0.4   3.0         5.0    1.2 -1.8            7.50
    mid    0.3  20.0    2.4   6.0        12.0    7.2  1.2            2.50
  heavy    0.1  40.0    8.2  24.0        20.5   24.6  0.6            2.93

overall uplift 12.0%, cost per active user Rs 6.00, extra completions/user 1.78, net per user Rs -0.66, cost per extra completion Rs 3.37
segments with cost per extra completion <= Rs 3.0 : ['mid', 'heavy']
net per original active user if light is not served: Rs 0.42
```

**Follow-ups:**
- What cost guardrail would you set? Cost per extra completion at or below value with a margin, and a p95 per-user cost cap, both reviewed monthly. The number comes from finance, not from me.
- What if value per completion is uncertain? Show the break-even value per segment and let the business pick. Here the break-even is Rs 7.5 for light, 2.5 for mid and 2.93 for heavy.
- Does cheaper always win? No. A cheaper path that cuts the uplift can destroy net value. Test the cheaper path as its own arm.

**Common mistakes:** Using total completions instead of incremental. Dividing cost by all users instead of the same denominator on both sides. Averaging across segments and stopping. Segmenting on post-launch behaviour. Setting a cost cap with no quality guardrail.

### Q50 ⭐ 🔴 Retention is reported as the share of last month's active users who are active this month, and it rose from 55% to 62%. Explain how survivorship, resurrected users and a shrinking base could make this look good while growth is stalling, and what companion metrics you would add.
**Asked at:** Statistics-trap and Simpson's-paradox question banks (Codemia and Prachub Simpson's paradox prompts, an Educative data-science course page, a KDnuggets traps article); commonly reported in public guides for global tech loops; search snippets only, not opened
**Say this first (1 line):** A higher month-over-month retention rate can come from who is left in the base, not from users liking the product more, so I break it by segment and add count-based metrics: retained users, new and resurrected users, churned users and net change in actives.

**Clarifying questions:**
- Exactly how is it computed: users active in both months divided by last month's actives? Does "active" mean the same thing in both months? It decides what resurrected users do to the number.
- Did the base size change? A smaller denominator moves a percentage a lot.
- Did acquisition change (a marketing cut, a new channel, a changed onboarding)? Fewer casual signups makes the base more loyal and the rate higher.
- Did the definition of "active" change (a stricter bar removes casual users from the base)? That alone lifts retention.
- Is total monthly active users up, flat or down? It shows whether the rate is helping.
- Is retention by tenure or segment available? I need it to check whether any single group got better.

**Approach:**
1. Write the identity. This month's actives = retained + new + resurrected. Retention only tells me about the retained slice divided by the base.
2. Check the base: size and composition (new, tenured, casual, core). Survivorship: months of churn have already removed weak users, so a base of survivors retains well.
3. Mix-standardise. Keep last period's segment weights and apply this period's segment retention. If it stays at 55%, the rise is pure mix.
4. Check resurrected users. They are not in last month's base, so they cannot raise this ratio if it is computed correctly. A leaky definition (counting them in the numerator) does inflate it.
5. Add counts: retained users, new users, resurrected users, churned users, net adds, and a quick ratio = (new + resurrected) / churned.
6. Show cohort retention curves by signup month, and retention by tenure, so a single blended percentage is never the headline.

**Metrics:**
- MoM retention = users active in both month t-1 and month t / users active in t-1.
- Net adds = actives(t) - actives(t-1). Quick ratio = (new + resurrected) / churned.
- Mix-standardised retention = sum over segments of (last period's share x this period's segment retention).
- Guardrails: base size, share of new users in the base, active count.

**Risks:**
- Mix shift: the rate rises while every segment is unchanged (Simpson-style; see Book 1 Part 10, Q10, heading: "What is Simpson's paradox? Give an A/B-test example where the variant wins overall but loses in every segment.").
- Survivorship: only survivors are measured (Book 1 Part 10, Q42, heading: "Explain selection bias and survivorship bias with experiment or observational examples.").
- Resurrected users hide a weak acquisition engine. Activity count looks fine, but it is old users coming back.
- A definition leak (resurrected in the numerator) can push a ratio near or above plausible limits.

**What the interviewer scores:**
- Strong: gives the identity, tests mix versus real improvement with standardisation, and adds counts, not only another ratio.
- Strong: points out that a rising rate and a shrinking base can both be true.
- Weak: celebrates 62%, or just says "retention is a lagging metric".
- Weak: adds companion metrics that are also ratios on the same shrunken base.

**Example:** Illustrative numbers. Two segments with unchanged monthly retention: core 85%, casual 25%.
- Before: base 100,000 (50,000 core, 50,000 casual). Retained 42,500 + 12,500 = 55,000, so 55%. With 20,000 new and 5,000 resurrected, actives next month are 80,000.
- After: acquisition was cut, casual users thinned out. Base 65,000 (40,000 core, 25,000 casual). Retained 34,000 + 6,250 = 40,250, so 61.9%, reported as 62%. With 8,000 new and 7,000 resurrected, actives next month are 55,250.
- The rate rose 7 points and retained users fell from 55,000 to 40,250. Standardised to last period's mix, retention is still 55%.
- Quick ratio: 0.56 before, 0.61 after. Both below 1, so the product is shrinking.
- Leaky definition: adding the 7,000 resurrected users to the numerator gives 72.7%.
- Weak answer: "Retention improved 7 points, great." Strong answer: "Same segment rates, fewer people. I would report retained users and the quick ratio next to the rate."

**Code:**
```python
# Q50: month-over-month retention rises 55% -> 62% while the product is not growing (illustrative)
import pandas as pd

# Two month-to-month transitions. Within each segment, retention is IDENTICAL in both.
RET = {"core": 0.85, "casual": 0.25}
t = {
  "before": dict(base={"core": 50_000, "casual": 50_000}, new=20_000, resurrected=5_000),
  "after":  dict(base={"core": 40_000, "casual": 25_000}, new=8_000,  resurrected=7_000),
}
res = {}
for k, v in t.items():
    base = sum(v["base"].values())
    retained = sum(v["base"][s] * RET[s] for s in RET)
    actives_next = retained + v["new"] + v["resurrected"]
    churned = base - retained
    res[k] = dict(base=base, retained=retained, retention=retained / base, actives_next=actives_next,
                  churned=churned, quick_ratio=(v["new"] + v["resurrected"]) / churned,
                  core_share=v["base"]["core"] / base)
df = pd.DataFrame(res).T
print(df.round(3).to_string())

assert round(res["before"]["retention"], 2) == 0.55 and round(res["after"]["retention"], 2) == 0.62
assert res["before"]["retained"] == 55_000 and res["after"]["retained"] == 40_250      # fewer retained PEOPLE
assert res["before"]["actives_next"] == 80_000 and res["after"]["actives_next"] == 55_250
assert round(res["before"]["quick_ratio"], 2) == 0.56 and round(res["after"]["quick_ratio"], 2) == 0.61

# mix-standardised retention: apply the BEFORE mix to the AFTER segment rates
w = {s: t["before"]["base"][s] / 100_000 for s in RET}
std_after = sum(w[s] * RET[s] for s in RET)
print("after, holding last period's mix:", round(std_after, 3), "(unchanged: the rise is pure mix)")
assert round(std_after, 2) == 0.55

# a leaky definition: counting resurrected users in the numerator of "last month's actives"
leak = (res["after"]["retained"] + t["after"]["resurrected"]) / res["after"]["base"]
print("leaky 'retention' with resurrected users in the numerator:", round(leak, 3))
assert round(leak, 3) == 0.727
```

**Output (my run):**
```text
            base  retained  retention  actives_next  churned  quick_ratio  core_share
before  100000.0   55000.0      0.550       80000.0  45000.0        0.556       0.500
after    65000.0   40250.0      0.619       55250.0  24750.0        0.606       0.615
after, holding last period's mix: 0.55 (unchanged: the rise is pure mix)
leaky 'retention' with resurrected users in the numerator: 0.727
```

**Follow-ups:**
- What is a resurrected user? Active this month, inactive last month, but seen before. Track them separately from new users.
- Which one chart do you show leadership? Active users split into retained, new and resurrected, stacked by month, with the retention rate as a line.
- Could the rise ever be real? Yes, if segment rates themselves went up. The standardised rate tells you.

**Common mistakes:** Treating the rate as the whole story. No counts. Letting the "active" definition change without a restatement. Mixing resurrected into the numerator. Comparing blended rates across periods with different base mixes.

### Q51 ⭐ 🔴 For a group-chat product, the value of the app to one user depends on their friends being active. Explain how you would define engagement and success metrics when users are interconnected, why simple per-user averages can mislead, and what you would add to track network health.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** In a group product the unit of value is the group, not the user, so I measure engagement and health at the group and connection level, because a per-user average can rise while the network is breaking up.

**Clarifying questions:**
- What is the core action: sending a message, getting a reply, or a conversation with at least two people? It defines "value delivered".
- What is a group in the data: explicit chat groups, or friend graphs? It defines the unit I aggregate to.
- Are users in many groups, or one? Overlap makes group metrics double count people.
- Is growth driven by invites? Invited users bring their group with them, so the spread matters.
- What is the goal: more groups, deeper groups, or more messages? I do not want to optimise one at the expense of the others.

**Approach:**
1. Define the unit of value: a conversation that involves two or more people and gets a reply. A message with no reader is not value.
2. Per-user metrics stay, but I pair them with group metrics: active groups per week, share of healthy groups (for example 3 or more active members this week), median group size, reply rate within an hour, and the share of users with at least 2 active friends.
3. Look at structure, not only averages: size distribution of components, share of users in the largest connected component, and the share of groups below the healthy threshold.
4. Track dependency: probability that a member stays active as a function of how many group members are active. This shows a tipping point, below which groups decay.
5. Success metric: healthy-group retention (a group stays healthy over 4 weeks), with messages per active user as secondary, never the headline.
6. Experiments: a per-user test leaks because friends see each other. Randomise by group or cluster of connected users, and measure spillover (see Book 1 Part 10, Q12, heading: "Explain network effects / interference (SUTVA violation). How do you run experiments on a social product or a two-sided marketplace?").

**Metrics:**
- Healthy-group share = groups with >= 3 active members in the week / groups with any activity.
- Healthy-group 4-week survival = groups healthy in week 1 that are still healthy in week 4 / groups healthy in week 1.
- Reply rate within 1 hour = messages answered in an hour / messages sent that expect an answer.
- Friends-active ratio = for each user, active friends / friends; report the median and the share below 0.2.
- Guardrails: invite spam rate, mute or leave-group rate, block rate.

**Risks:**
- Per-user averages: when weak groups shrink, the remaining few chat more, so messages per active user can go up while the network degrades.
- Cannibalisation: new groups can pull activity from old ones.
- Heavy groups dominate sums. Use medians and distributions, not just means.
- A group threshold (3 members) is a choice. Check the result with 2 and 4.
- Spillover: a test on some users changes others' behaviour. Control users are contaminated.

**What the interviewer scores:**
- Strong: moves the unit from user to group or connection and shows how the average misleads.
- Strong: names health and dependency metrics, such as healthy-group share and active-friend ratio, and says how to test with cluster randomisation.
- Weak: DAU and messages per DAU only.
- Weak: lists graph jargon but no metric a team could compute.

**Example:** Illustrative numbers. Week 1: 20 groups of 5, everyone active, 10 messages each. DAU 100, messages 1,000, 10.0 messages per active user, 100% of groups healthy. Week 2: 10 groups unchanged, and 10 groups where only 2 of 5 members are active, but those two message 14 times each.
- DAU 70, messages 780, so 11.14 messages per active user, up 11%. Healthy-group share dropped to 50%.
- In a seeded simulation (leave chance 5% per week in a healthy group and 30% in a weak one), after 8 weeks a group that started with 5 active members averages 3.16 active, and one that started with 2 averages 0.12. Weak groups are not a stable state, they are a decline.
- Reply rate within an hour by group: 80%, 90%, 70%, 20%, 10%, so the mean 54% hides two broken groups.
- Weak answer: "Messages per user is up 11%, engagement is healthy." Strong answer: "Half of the groups fell below 3 active members and those do not recover. The per-user average is the survivors chatting more."

**Code:**
```python
# Q51: group-chat metrics when users depend on each other (illustrative numbers + a seeded simulation)
import numpy as np
rng = np.random.default_rng(51)

# Week 1: 20 groups of 5, everyone active, 10 messages each.
# Week 2: 10 groups stay intact; 10 groups have only 2 of 5 members active, and those 2 message 14 each.
w1 = dict(groups=[(5, 10)] * 20)                       # (active members, messages per active member)
w2 = dict(groups=[(5, 10)] * 10 + [(2, 14)] * 10)

def summarize(groups):
    dau = sum(a for a, _ in groups)
    msgs = sum(a * m for a, m in groups)
    healthy = sum(1 for a, _ in groups if a >= 3)      # a group is "healthy" if >= 3 members active
    return dau, msgs, msgs / dau, healthy / len(groups)

for name, w in (("week 1", w1), ("week 2", w2)):
    dau, msgs, per_user, healthy = summarize(w["groups"])
    print(f"{name}: DAU {dau}, messages {msgs}, messages per active user {per_user:.2f}, healthy-group share {healthy:.0%}")
s1, s2 = summarize(w1["groups"]), summarize(w2["groups"])
assert s1[:3] == (100, 1000, 10.0) and s2[:2] == (70, 780) and round(s2[2], 2) == 11.14
assert s1[3] == 1.0 and s2[3] == 0.5

# Why the weak groups matter: leaving depends on how many friends are still active.
def simulate(start_active, weeks=8, n_groups=2000, size=5):
    active = np.full(n_groups, start_active)
    for _ in range(weeks):
        # chance an active member leaves this week: 5% if >=3 active in the group, 30% otherwise
        p = np.where(active >= 3, 0.05, 0.30)
        active = active - rng.binomial(active, p)
    return active.mean()
healthy_end = simulate(5)
weak_end = simulate(2)
print(f"after 8 weeks, mean active members: group that started with 5 = {healthy_end:.2f}, started with 2 = {weak_end:.2f}")
assert weak_end < 0.5 and healthy_end > 3.0 and weak_end < healthy_end / 5

# Edge-level metric: share of messages answered within an hour (reciprocity), per-user vs per-group
replied = np.array([8, 9, 7, 2, 1])                    # per group of 5 chats, replies within 1h out of 10 messages each
print("reply-within-1h rate by group:", (replied / 10).tolist(), "mean", replied.mean() / 10)
assert replied.mean() / 10 == 0.54
```

**Output (my run):**
```text
week 1: DAU 100, messages 1000, messages per active user 10.00, healthy-group share 100%
week 2: DAU 70, messages 780, messages per active user 11.14, healthy-group share 50%
after 8 weeks, mean active members: group that started with 5 = 3.16, started with 2 = 0.12
reply-within-1h rate by group: [0.8, 0.9, 0.7, 0.2, 0.1] mean 0.54
```

**Follow-ups:**
- How would you test a new feature in this product? Randomise by group or friend cluster, and measure group-level metrics. A per-user split underestimates network effects because treated and control users talk to each other.
- How do you pick the healthy threshold? From the data: where the next-week retention curve bends against active-member count.
- What about a growth metric? Invites sent that lead to an active member in a group, not signups alone.

**Common mistakes:** Aggregating at the user level only. Treating more messages as more value. Ignoring the dependency between users. Randomising users inside the same group. Reporting a mean when the distribution is bimodal.

### Q52 ⭐ 🔴 A notification team lifted push click-through rate by 25% using more urgent wording, and its own bonus is tied to that number. Explain how this metric can be gamed, which counter-metrics and holdouts would expose it, and how you would redesign the metric system so incentives line up.
**Asked at:** Metric trade-off ('one metric up, another down') guides (Interview Query metric trade-offs path, Exponent analytical-execution course, a Facebook product-execution write-up on Substack); commonly reported in public guides; search snippets only, not opened
**Say this first (1 line):** Click-through rate on pushes is easy to game and says nothing about value, so I would judge the team on incremental sessions and long-term retention against a no-push holdout, with opt-outs and uninstalls as hard counter-metrics.

**Clarifying questions:**
- Is CTR clicks divided by pushes sent, or by pushes delivered or seen? Sending fewer pushes to better people raises CTR with no gain.
- Is the +25% from a randomised test of wording alone, or did volume and targeting change too? It decides whether wording is the cause.
- Is there a holdout that gets no pushes? Without it I cannot measure incremental value.
- What is the notification meant to achieve: a return visit, a purchase, a message read? It defines the real success metric.
- How many pushes per user per week, and is there a frequency cap? Volume is the easiest lever to pull.
- How is the bonus computed, and over what period? A quarterly bonus on CTR rewards short-term tactics.

**Approach:**
1. List how CTR can be gamed: urgent or clickbait wording that clicks and disappoints; fewer sends to likely clickers only (a higher ratio, fewer total clicks); sending at the moment a user would open the app anyway (steals the click, adds no session); changing the denominator (delivered versus sent); counting accidental or auto-dismissed taps.
2. Measure incremental value with a holdout: a small share of users get no pushes (or the old wording). Compare sessions per user, retention and downstream actions.
3. Counter-metrics, all reported with CTR: opt-out or disable-notifications rate, uninstall rate, post-click engagement (bounce within 10 seconds, session depth, conversion), push volume per user, complaint rate.
4. Evaluate over a longer window than the bonus period: cumulative value per starting user, because opt-outs shrink reach.
5. Redesign the metric system: the team's goal becomes incremental sessions or conversions per 1,000 users in the holdout comparison, with opt-out rate as a gate (a result that breaches the gate does not count).
6. Governance: a global per-user notification budget so teams cannot trade each other's reach for their own CTR.

**Metrics:**
- CTR = push opens / pushes sent (state the denominator).
- Incremental sessions per user per week = sessions(push arm) - sessions(holdout).
- Opt-out rate = users turning push off in the week / users with push on at the start of the week.
- Value per starting user over T weeks = sum over weeks of sends x CTR x value per click x remaining reach.
- Guardrails: opt-out rate, uninstalls, bounce after click, pushes per user per week.

**Risks:**
- Holdouts cost some value in the short term. Keep them small and rotate.
- Long-run effects need long tests. Use a long-term holdout (Book 1 Part 10, Q24, heading: "What is a holdout / long-term holdout group and why would a company keep one?").
- Goodhart: any metric tied to a bonus gets optimised. Rotating or paired metrics help.
- Value per click is an assumption. Show a range.

**What the interviewer scores:**
- Strong: gives at least three specific ways to game CTR, and the metric that exposes each.
- Strong: asks for a holdout and talks about incremental value and opt-outs as a gate.
- Weak: "add a guardrail" with no name, no number, no action.
- Weak: blames the team instead of redesigning the incentive.

**Example:** Illustrative numbers. Old wording CTR 4.0%, urgent wording 5.0% (+25%). 100,000 users in each of three arms (holdout, old, urgent).
- Sessions per user per week: old is +0.283 over the holdout, urgent is +0.305 (my run). Urgent beats old by only +0.022 (95% CI about +/- 0.016), under 1% of a baseline near 3.3 sessions, for a 25% CTR gain.
- Assume weekly opt-out is 0.3% with the old wording and 1.0% with urgent, 5 pushes per week, and urgent clicks are 15% shallower. Cumulative value per starting user: after 4 weeks urgent is 1.05 times old, after 12 weeks 1.02, after 52 weeks 0.90 and after 104 weeks 0.77. Urgent falls behind after week 19.
- The team's bonus is paid in the quarter where urgent looks better.
- Weak answer: "CTR up 25%, ship it." Strong answer: "CTR is up but incremental sessions are about flat and opt-outs triple. I would pay the team on holdout-measured incremental sessions with opt-out as a gate."

**Code:**
```python
# Q52: push CTR +25% from urgent wording. Does it help? (illustrative numbers, seeded)
import numpy as np
rng = np.random.default_rng(52)

# 1) CTR is a ratio on pushes SENT, not value. 3 arms, 100k users each, 4 weeks.
N = 100_000
ctr_old, ctr_new = 0.040, 0.050
assert round(ctr_new / ctr_old - 1, 2) == 0.25

# incremental sessions per user per week: holdout (no push) vs old wording vs urgent wording
base_rate = 3.0                                 # sessions/user/week with no push
sess_h = rng.poisson(base_rate, N)
sess_a = rng.poisson(base_rate + 0.30, N)       # old wording adds 0.30 sessions
sess_b = rng.poisson(base_rate + 0.32, N)       # urgent wording: CTR up 25% but only +0.02 more incremental sessions
def diff_ci(x, y):
    d = x.mean() - y.mean()
    se = np.sqrt(x.var(ddof=1)/len(x) + y.var(ddof=1)/len(y))
    return d, 1.96 * se
for name, a, b in (("old vs holdout", sess_a, sess_h), ("urgent vs holdout", sess_b, sess_h), ("urgent vs old", sess_b, sess_a)):
    d, h = diff_ci(a, b)
    print(f"{name}: {d:+.3f} sessions/user/week, 95% CI +/- {h:.3f}")
d_ba, h_ba = diff_ci(sess_b, sess_a)
assert abs(d_ba) < 0.1 and diff_ci(sess_a, sess_h)[0] > 0.25          # pushes add sessions; urgency adds little beyond that

# 2) what the CTR hides: opt-outs shrink reach over time
sends_per_week = 5
d_old, d_new = 0.003, 0.010                      # weekly share of users who turn pushes off
value_per_click_old, value_per_click_new = 1.00, 0.85   # urgent-click sessions are shallower (assumption)
def cum_value(ctr, drop, vpc, weeks):
    reach = (1 - drop) ** np.arange(weeks)
    return float(np.sum(sends_per_week * ctr * vpc * reach))
for w in (4, 12, 52, 104):
    a = cum_value(ctr_old, d_old, value_per_click_old, w)
    b = cum_value(ctr_new, d_new, value_per_click_new, w)
    print(f"{w:>3} weeks: value per starting user old {a:6.2f}, urgent {b:6.2f}, urgent/old {b/a:.2f}")
cross = next(w for w in range(1, 600) if cum_value(ctr_new, d_new, value_per_click_new, w) < cum_value(ctr_old, d_old, value_per_click_old, w))
print("urgent wording falls behind cumulatively after week", cross)
assert cum_value(ctr_new, d_new, value_per_click_new, 4) > cum_value(ctr_old, d_old, value_per_click_old, 4)
assert cum_value(ctr_new, d_new, value_per_click_new, 104) < cum_value(ctr_old, d_old, value_per_click_old, 104)
```

**Output (my run):**
```text
old vs holdout: +0.283 sessions/user/week, 95% CI +/- 0.016
urgent vs holdout: +0.305 sessions/user/week, 95% CI +/- 0.016
urgent vs old: +0.022 sessions/user/week, 95% CI +/- 0.016
  4 weeks: value per starting user old   0.80, urgent   0.84, urgent/old 1.05
 12 weeks: value per starting user old   2.36, urgent   2.41, urgent/old 1.02
 52 weeks: value per starting user old   9.64, urgent   8.65, urgent/old 0.90
104 weeks: value per starting user old  17.89, urgent  13.78, urgent/old 0.77
urgent wording falls behind cumulatively after week 19
```

**Follow-ups:**
- Which single metric would you give them? Incremental sessions (or conversions) per 1,000 users versus holdout, gated by opt-out rate.
- How big a holdout? Large enough to detect the smallest worthwhile effect. In this run 100,000 users per arm gave about +/- 0.016 on sessions per week.
- What if the team says the holdout costs them reach? Rotate a small holdout (a few percent) and share the learning, since it is the only way to know the value.

**Common mistakes:** Trusting CTR with no denominator. No holdout. Measuring over four weeks when opt-outs build over months. Setting a counter-metric with no threshold. Tying a bonus to a ratio that is easy to move.

### Q53 ⭐ 🔴 Revenue grew from Rs 100 crore to Rs 112 crore. Volume rose 6%, like-for-like price within each tier rose 2%, and the mix moved toward a premium tier. Show how you would split the change into volume, price and mix effects with a small numeric table, state the assumption behind the order of the split, and explain what you would tell leadership.
**Asked at:** Indian consumer-internet analyst guides (Interview Query Swiggy, Flipkart and Meesho analyst guides, AmbitionBox and Dataford interview pages) that list revenue-drop, order-drop and AOV-drop cases; community-posted, not confirmed company questions; search snippets only, not opened
**Say this first (1 line):** I split the Rs 12 crore into volume, mix and price using a fixed order. In my illustrative table that gives Rs 6.0 crore from volume, Rs 3.8 crore from mix and Rs 2.2 crore from price, and I tell leadership that half of the growth is volume and only a fifth is price.

**Clarifying questions:**
- Is "+2% price" the like-for-like price of each tier, or the change in blended average price? The wording matters, see the risks. The numbers only add up to Rs 112 crore if it is like-for-like.
- What is a "unit" and are tiers comparable (same pack, same product)? Mix is only meaningful across defined tiers.
- Is revenue gross or net of discounts and returns? A price effect can be a discount effect.
- How many tiers, and is the premium tier new this year? New tiers have no base price.
- Same period last year or the previous period? Seasonal mix can move the comparison.
- Who uses the answer: pricing, sales, or finance? It decides how much detail.

**Approach:**
1. Define the pieces. Revenue = sum over tiers of units x price.
2. Volume effect: change in total units valued at the base average price (base mix, base prices).
3. Mix effect: with total units fixed at the new level, move from the base mix to the new mix, valued at base prices.
4. Price effect: the rest, price changes valued at new volume and new mix.
5. State the order and check that the three add to the total change (Rs 12 crore here).
6. Re-run with the opposite order to see how much the split moves. Report the range and the interaction, and do not present one order as truth.
7. Tell leadership what is driving growth, how repeatable it is, and what to watch.

**Metrics:**
- Volume effect = (V1 - V0) x average revenue per unit at base (R0 / V0).
- Mix effect = revenue of the new units at base tier prices - V1 x R0 / V0.
- Price effect = R1 - revenue of the new units at base tier prices.
- Check: volume + mix + price = R1 - R0.
- Guardrails: premium share of units, units by tier, discount rate, margin by tier.

**Risks:**
- Order of the split changes the answer. Volume first, then mix, then price gives 6.00 / 3.80 / 2.20. Price first, then volume, then mix gives price 2.00, volume 6.12, mix 3.88. The total is the same, the story is not.
- Wording problem: if +2% were the blended average price, 6% volume and 2% price would give only Rs 108.12 crore, so Rs 3.88 crore would be unexplained. With mix shifting toward premium, the blended average price rose 5.66% (Rs 105.66 per unit against Rs 100), so mix is already inside the blended number. I use +2% as like-for-like.
- Tier definitions: if tiers are too coarse, mix inside a tier hides in price.
- Premium mix can be bought with discounts, and the revenue may carry less margin.

**What the interviewer scores:**
- Strong: gives the formulas, shows a table that adds up, states the order assumption and checks it with the opposite order.
- Strong: translates it for leadership: how much is repeatable, what to watch, and notes the ambiguity in the prompt.
- Weak: "6% + 2% = 8%, so mix must be 4%." (Multiplicative, not additive; also ignores order.)
- Weak: a table with no check that the parts sum to the total.

**Example:** Illustrative numbers. Two tiers. Base: standard 75 lakh units at Rs 80 (Rs 60 crore), premium 25 lakh at Rs 160 (Rs 40 crore). Total 100 lakh units, Rs 100 crore, average Rs 100. New: total units 106 lakh (+6%), each tier's price +2% (Rs 81.6 and Rs 163.2), premium share of units rises from 25.0% to 29.5% (standard 74.75, premium 31.25 lakh). Revenue Rs 112.0 crore.

| Step (order: volume, mix, price) | Calculation | Rs crore |
|---|---|---|
| Volume | 6 lakh extra units x Rs 100 average / 100 | 6.00 |
| Mix | new units at base prices = 74.75x80 + 31.25x160 = Rs 109.80 crore, minus 106 x 100 / 100 = Rs 106.00 crore | 3.80 |
| Price | Rs 112.00 - Rs 109.80 | 2.20 |
| Total | | 12.00 |

- Opposite order (price first, then volume, then mix): 2.00 / 6.12 / 3.88. Same total. Volume moves by Rs 0.12 crore, mix by Rs 0.08 crore and price by Rs 0.20 crore.
- Leadership message: about half the growth is volume (6.0 of 12), about a third is a richer mix (3.8), under a fifth is price (2.2). The mix gain depends on premium share staying near 29.5%, and the price gain is a one-off step.
- Weak answer: "Revenue grew 12%, mostly price and volume." Strong answer: "6.0 volume, 3.8 mix, 2.2 price, in that order; the other order moves mix to 3.88; the Rs 112 crore only reconciles if the 2% is like-for-like."

**Code:**
```python
# Q53: volume / price / mix split of a Rs 100 crore -> Rs 112 crore revenue change (illustrative numbers)
# units in lakh, price in Rs per unit, revenue crore = lakh units x Rs / 100
tiers = ["standard", "premium"]
u0 = {"standard": 75.0, "premium": 25.0}          # base units
p0 = {"standard": 80.0, "premium": 160.0}         # base price
R = lambda u, p: sum(u[t] * p[t] for t in tiers) / 100
V0 = sum(u0.values()); R0 = R(u0, p0)
assert V0 == 100.0 and R0 == 100.0

V1 = V0 * 1.06                                     # volume +6%
price_up = 1.02                                    # like-for-like price +2% in every tier
p1 = {t: p0[t] * price_up for t in tiers}
# choose the new premium share so that revenue is exactly 112 crore
s = (112 * 100 / V1) / p1["standard"] - 1          # avg price = p_std1 * (1 + s) since premium = 2x standard
u1 = {"standard": V1 * (1 - s), "premium": V1 * s}
R1 = R(u1, p1)
print(f"new units: standard {u1['standard']:.2f}, premium {u1['premium']:.2f} lakh; premium share {s:.1%} (was 25.0%); revenue {R1:.3f} crore")
assert abs(R1 - 112) < 1e-9 and abs(s - 0.2948) < 5e-4

# ORDER 1: volume (at base mix and base price) -> mix (at base prices) -> price (at new volume and mix)
vol1 = (V1 - V0) * R0 / V0
mix1 = R(u1, p0) - V1 * R0 / V0
price1 = R1 - R(u1, p0)
print(f"order 1 volume, mix, price: {vol1:.2f}  {mix1:.2f}  {price1:.2f}  total {vol1+mix1+price1:.2f}")
assert round(vol1, 2) == 6.00 and round(mix1, 2) == 3.80 and round(price1, 2) == 2.20
assert abs(vol1 + mix1 + price1 - 12) < 1e-9

# ORDER 2: price (at base volume and mix) -> volume (at new price) -> mix (the rest)
price2 = R(u0, p1) - R0
vol2 = (V1 - V0) * R(u0, p1) / V0
mix2 = (R1 - R0) - price2 - vol2
print(f"order 2 price, volume, mix: {price2:.2f}  {vol2:.2f}  {mix2:.2f}  total {price2+vol2+mix2:.2f}")
assert round(price2, 2) == 2.00 and round(vol2, 2) == 6.12 and round(mix2, 2) == 3.88

# the wording check: if "+2%" were the BLENDED average price, volume x price alone gives:
print("volume x blended price only:", round(100 * 1.06 * 1.02, 2), "crore (not 112)")
assert round(100 * 1.06 * 1.02, 2) == 108.12
print("realised average price change:", round((R1 / V1) / (R0 / V0) - 1, 4))
assert round((R1 / V1) / (R0 / V0) - 1, 4) == 0.0566
```

**Output (my run):**
```text
new units: standard 74.75, premium 31.25 lakh; premium share 29.5% (was 25.0%); revenue 112.000 crore
order 1 volume, mix, price: 6.00  3.80  2.20  total 12.00
order 2 price, volume, mix: 2.00  6.12  3.88  total 12.00
volume x blended price only: 108.12 crore (not 112)
realised average price change: 0.0566
```

**Follow-ups:**
- Why does order matter? Because volume, price and mix multiply. The cross terms have to be given to one effect, and the order decides which one.
- How do you remove the order issue? Use averages of the two orders, or a symmetric method, and say so. The aim is a stable story, not a perfect split.
- Is mix good news? Only if the premium tier is profitable and not bought with discounts. Check margin by tier.

**Common mistakes:** Adding percentages instead of compounding. Using blended average price and mix together (double counting). Not saying the order. A table whose parts do not add up. Telling leadership "price drove growth" when price is under 20% of it.

### Q54 ⭐ 🔴 An AI support agent reports a 70% deflection rate (conversations not handed to a human), but complaints about the same issues are rising. Explain why deflection can overstate success, how you would measure true resolution with sampling and human labelling, and which guardrails you would add.
**Asked at:** GenAI and AI-feature metric guides (a Substack AI product-manager interview post on measuring a chatbot, a Prachub generative-AI north-star page, a Dataford GenAI-chatbot metrics page, Galileo and dscout blog posts); AI-era twist reported in public guides, not tied to a named employer; search snippets only, not opened
**Say this first (1 line):** Deflation only counts conversations that did not reach a human, so a customer who gave up counts as a success. I would measure true resolution with human labels on a stratified sample, and put guardrails on recontact, complaints and how easily people can reach a human.

**Clarifying questions:**
- What exactly counts as deflated: no human handoff in the session, or no human contact within 7 days? Short windows overstate it.
- Can the user reach a human easily, or is the button hidden? A hard-to-find handoff raises deflation by itself.
- Which issues are the complaints about, and do they match the topics the agent handles? It points me to the strata to sample.
- Is there a satisfaction question and who answers it? Unhappy people rarely answer.
- How are conversations sampled, and is there a way for people to label them (support leads, QA team)? Labelling capacity sets the sample size.
- Was the deflation target set as a goal for the team? Targets bend the number.

**Approach:**
1. Say why deflation overstates success: it counts abandonment, wrong answers that the user did not notice, the user giving up and going to another channel, and hidden handoffs as wins. It measures cost avoided, not problems solved.
2. Define the real metric: AI resolution rate = conversations where the issue was actually solved by the agent / all conversations that started with the agent.
3. Measure it by sampling. Stratify by topic and by outcome type (handoff or not, complaint risk), sample a few hundred conversations per stratum, and have trained humans label with a fixed rubric: resolved, partly resolved, wrong answer, abandoned. Double-label a subset to measure agreement.
4. Reweight by stratum size to estimate the overall rate, with a confidence interval.
5. Add behavioural signals that do not need labels: recontact on the same issue within 7 days, repeat complaints, channel switching, thumbs, and time to a human when asked.
6. Guardrails: complaint rate per 1,000 conversations, recontact rate, wrong-answer rate from sampled labels, share of users who asked for a human and did not get one, and CSAT on deflated conversations.
7. Report deflation next to resolution, never alone.

**Metrics:**
- Deflation rate = conversations not handed to a human / conversations started with the agent.
- True resolution rate = labelled resolved conversations (reweighted) / conversations started with the agent.
- Recontact rate (7 days) = issue-matched returns within 7 days / conversations in the group.
- Wrong-answer rate = sampled conversations labelled wrong / sampled conversations.
- Guardrails: complaints per 1,000 conversations, time to human, CSAT.

**Risks:**
- Labelling is slow and costly. Keep the sample small but stratified, and use the labels also to calibrate cheaper signals.
- Label noise. Measure labeller agreement and refresh the rubric.
- An LLM used as a judge can be biased and needs validating against human labels first (see Book 1 Part 10, Q56 heading: "AI-era: How do you validate an LLM-as-judge metric before using it as an experiment outcome (bias, agreement with humans, variance)?").
- Making handoff easy lowers deflation and raises the real quality. Expect the headline number to fall.

**What the interviewer scores:**
- Strong: explains how deflation can be inflated and gives a measurable replacement with a sampling design and an interval.
- Strong: guardrails with names and actions, and an honest statement that the headline will drop.
- Weak: "ask users for ratings".
- Weak: more automated metrics with no human labels.

**Example:** Illustrative numbers. 100,000 conversations, 70,000 deflated. Two topics among the deflated: billing 28,000 conversations (45% truly resolved) and FAQ 42,000 (70% truly resolved), so 60% of deflated are resolved, and 42% of all conversations are resolved by the agent. A labelled sample of 200 per topic estimates 61.3% resolved among deflated (+/- 4.6 points), so about 43% of all conversations (+/- 3.2 points) in my run.
- Reported 70%, estimated true resolution 43%.
- Recontact within 7 days: 28% for deflated conversations versus 10% for human-handled (assumed figures), a 2.8x gap that supports the complaints.
- Weak answer: "70% deflation, great." Strong answer: "70% is the share that avoided a human. About 43% were actually solved. Billing is the weak topic, I would fix that and keep a visible path to a human."

**Code:**
```python
# Q54: deflation 70% vs true resolution, estimated by stratified human labelling (illustrative, seeded)
import numpy as np
rng = np.random.default_rng(54)

N = 100_000
deflated = 70_000                                  # 70% not handed to a human
assert deflated / N == 0.70
# truth (unknown to the analyst): by topic, share of deflated conversations really resolved
topics = {"billing": dict(n=28_000, p_resolved=0.45), "faq": dict(n=42_000, p_resolved=0.70)}
assert sum(t["n"] for t in topics.values()) == deflated
true_resolved = sum(t["n"] * t["p_resolved"] for t in topics.values())
print("true resolved among deflated:", true_resolved / deflated, "| true resolution rate over all conversations:", true_resolved / N)
assert true_resolved / deflated == 0.60 and true_resolved / N == 0.42

# human labelling: 200 per topic, stratified, then reweight by topic size
est = 0.0; var = 0.0
for name, t in topics.items():
    k = rng.binomial(200, t["p_resolved"])
    p = k / 200
    w = t["n"] / deflated
    est += w * p
    var += w * w * p * (1 - p) / 200
half = 1.96 * np.sqrt(var)
print(f"labelled estimate among deflated: {est:.3f} +/- {half:.3f}  -> resolution rate over all: {est*0.70:.3f} +/- {half*0.70:.3f}")
assert abs(est - 0.60) < 3 * np.sqrt(var)
assert half < 0.05

# reported vs real
print(f"reported deflation {deflated/N:.0%} vs estimated true resolution about {est*0.70:.0%}")

# a second signal: recontact within 7 days on the same issue
recontact_deflated, recontact_human = 0.28, 0.10
print("recontact within 7 days: deflated", recontact_deflated, "vs human-handled", recontact_human)
assert round(recontact_deflated / recontact_human, 1) == 2.8
```

**Output (my run):**
```text
true resolved among deflated: 0.6 | true resolution rate over all conversations: 0.42
labelled estimate among deflated: 0.613 +/- 0.046  -> resolution rate over all: 0.429 +/- 0.032
reported deflation 70% vs estimated true resolution about 43%
recontact within 7 days: deflated 0.28 vs human-handled 0.1
```

**Follow-ups:**
- How many to label? Enough for a half-width you can act on. 200 per stratum gave about 4.6 points here. Use more for topics with more weight or risk.
- Why stratify? Topics differ a lot. A simple random sample would under-sample the weak small topics.
- What if leadership likes the deflation target? Keep it as a cost metric and make resolution rate and recontact the quality gate for the same team.

**Common mistakes:** Treating "no handoff" as "solved". Asking only happy users for ratings. Labelling without a rubric. One average for all topics. Making handoff hard to raise deflation. Reporting only the number that improved.

### Q55 ⭐ 🔴 A platform-wide policy change (for example a new OS permission prompt) permanently resets a core metric's baseline in one week, so trend comparisons break. Explain how you would document the break, estimate what the metric would have been without it, and keep exec reporting honest for the next year.
**Asked at:** No public page located for this exact scenario; editor-designed from standard metric-diagnosis patterns (measurement validity, definitions, segmentation) that the metric-drop guides describe in general terms; search snippets only, not opened
**Say this first (1 line):** I mark the break on every chart, split the series into before and after versions of the metric, estimate the step with a counterfactual from an unaffected group or the pre-trend, publish a bridge factor with an error range, and report year-over-year on a bridged basis for the next 12 months.

**Clarifying questions:**
- Is the change in measurement (we now see fewer events) or in real behaviour (fewer people grant permission)? A bridge is only for the first. For the second the drop is real.
- Which users are affected: one OS, one version, one country? An unaffected group gives me a control.
- Did the change land on one date for everyone, or roll out in stages? A staged rollout gives a natural experiment.
- Is any old and new definition collected in parallel for a while? A parallel run gives an exact bridge.
- Who consumes the metric, and is it in targets or bonuses? Targets must be re-based before the next period.
- Which downstream metrics (revenue, ads) were also hit? It tells me whether the break is local or ripples outward.

**Approach:**
1. Document the break the same day: date, cause, affected segments, owner. Put it in the metric dictionary and annotate every chart. Version the metric (v1 before, v2 after).
2. Separate cause types: instrumentation change (the metric reads lower), or behaviour change (the world is lower). They are reported differently.
3. Estimate the counterfactual with more than one method:
   - Unaffected group (difference-in-differences): compare the affected series with an unaffected one before and after.
   - Interrupted time series: fit the pre-break trend and seasonality, project it, and compare with actual.
   - Staged rollout or parallel run: the cleanest, if it exists.
4. Report the step as a range, not a point, and say which assumptions each method needs (parallel trends; trend and seasonality unchanged).
5. Publish a bridge: restated history = old values x (1 + step), or restated new values = new / (1 + step), with the range. Use it for year-over-year, targets and forecasts for the next 12 months.
6. Governance: executive reports show a break marker and a bridged line next to the raw line. Targets are re-based. When the break is 12 months old, the raw year-over-year becomes comparable again and the footnote can go.

**Metrics:**
- Step = actual level after the break / counterfactual level - 1.
- Bridged value = new-definition value / (1 + step).
- Bridged YoY = bridged current / prior-year value - 1.
- Guardrails: width of the step estimate, parallel-trend check before the break, share of reports that carry the break annotation.

**Risks:**
- Trend or seasonality changes at the same time as the break, so the pre-trend projection is wrong.
- The control group is also partly affected (spillover).
- Choosing the method that gives the preferred answer. Report all of them.
- A bridge factor assumes the same proportional effect everywhere. It can differ by segment.
- Quietly dropping the break marker after a few quarters.

**What the interviewer scores:**
- Strong: distinguishes measurement change from real change, offers two or more estimation methods with their assumptions, and gives an uncertainty range.
- Strong: a practical reporting rule for the next year: annotations, bridged lines, re-based targets, an end date for the footnote.
- Weak: "adjust the numbers by x%" with no method.
- Weak: leaves exec dashboards raw and hopes people remember.

**Example:** Illustrative simulation, weekly series, break in week 40 on the affected platform (true step -15%), steady growth of 0.3% a week, mild seasonality, 1% noise, and an unaffected platform for comparison.
- Estimates of the step in my run: naive last-8-weeks versus first-8-weeks -13.8% (it hides growth), interrupted time series -17.1%, difference-in-differences -16.1%. Both model-based estimates land within about two points of the true -15%, and both overshoot a little. Say the range, not the point.
- Year-over-year at week 60: raw -0.9% (looks flat), bridged +19.6%. The underlying growth over the 52 weeks is +16.9%. So without a bridge, leadership would read the year as flat when it grew.
- Weak answer: "The drop is the OS change, ignore it." Strong answer: "The step is about -16% (range about -14% to -17%); I publish a bridged line and re-base the targets, and for twelve months year-over-year is shown on both bases."

**Code:**
```python
# Q55: a platform change resets a metric's baseline in week 40; estimate the counterfactual (illustrative, seeded)
import numpy as np
rng = np.random.default_rng(55)

T = 80; BREAK = 40; TRUE_DROP = 0.15; GROWTH = 0.003
t = np.arange(T)
season = 1 + 0.02 * np.sin(2 * np.pi * t / 52)
def series(level, affected):
    y = level * (1 + GROWTH) ** t * season * rng.normal(1, 0.01, T)
    if affected: y = np.where(t >= BREAK, y * (1 - TRUE_DROP), y)
    return y
ios = series(100, True)         # affected platform (new permission prompt)
andr = series(150, False)       # unaffected platform, same underlying trend

# 1) naive: last 8 pre weeks vs first 8 post weeks on the affected series
naive = ios[BREAK:BREAK+8].mean() / ios[BREAK-8:BREAK].mean() - 1
# 2) interrupted time series: fit log-linear trend on pre-break weeks only, project, compare
X = np.c_[np.ones(BREAK), t[:BREAK], np.sin(2*np.pi*t[:BREAK]/52), np.cos(2*np.pi*t[:BREAK]/52)]
beta = np.linalg.lstsq(X, np.log(ios[:BREAK]), rcond=None)[0]
Xp = np.c_[np.ones(8), t[BREAK:BREAK+8], np.sin(2*np.pi*t[BREAK:BREAK+8]/52), np.cos(2*np.pi*t[BREAK:BREAK+8]/52)]
its = np.mean(ios[BREAK:BREAK+8] / np.exp(Xp @ beta)) - 1
# 3) difference-in-differences against the unaffected platform (in logs)
did = np.exp((np.log(ios[BREAK:BREAK+8]).mean() - np.log(ios[BREAK-8:BREAK]).mean())
             - (np.log(andr[BREAK:BREAK+8]).mean() - np.log(andr[BREAK-8:BREAK]).mean())) - 1
print(f"true step {-TRUE_DROP:+.1%} | naive pre/post {naive:+.1%} | interrupted time series {its:+.1%} | diff-in-diff {did:+.1%}")
assert abs(its + TRUE_DROP) < 0.03 and abs(did + TRUE_DROP) < 0.03

# 4) bridge factor and honest YoY at week 60 (4-week averages)
factor = 1 + its                                      # estimated level step
raw_yoy = ios[56:60].mean() / ios[4:8].mean() - 1                  # compares post-break with pre-break
bridged_yoy = (ios[56:60].mean() / factor) / ios[4:8].mean() - 1   # restate to the old definition
true_yoy = (1 + GROWTH) ** 52 - 1
print(f"year-over-year at week 60: raw {raw_yoy:+.1%} | bridged {bridged_yoy:+.1%} | underlying growth {true_yoy:+.1%}")
assert abs(raw_yoy) < 0.06 and 0.10 < bridged_yoy < 0.24 and abs(true_yoy - 0.169) < 0.002
```

**Output (my run):**
```text
true step -15.0% | naive pre/post -13.8% | interrupted time series -17.1% | diff-in-diff -16.1%
year-over-year at week 60: raw -0.9% | bridged +19.6% | underlying growth +16.9%
```

**Follow-ups:**
- Which method is best? A parallel run beats a control group, which beats a pure time-series projection. Use two and compare. Book 1 Part 10, Q28 covers difference-in-differences (heading: "Explain difference-in-differences. What is the parallel-trends assumption and how do you test it?").
- What if no control exists? Use interrupted time series, widen the range, and say the assumption (no other change at the same time).
- How do you stop people comparing raw numbers across the break? A permanent annotation, a bridged series by default, and a retired raw series after 12 months.

**Common mistakes:** Comparing post-break to pre-break without a trend. One method, no range. Applying one factor to all segments. Forgetting to re-base targets. Dropping the annotation after a quarter. Treating a real behaviour change as a measurement fix.

