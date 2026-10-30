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
