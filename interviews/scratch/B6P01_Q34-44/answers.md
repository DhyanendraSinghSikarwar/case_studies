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
