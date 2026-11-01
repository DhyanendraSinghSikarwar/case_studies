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
