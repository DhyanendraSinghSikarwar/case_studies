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
