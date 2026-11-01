# Q42: rolling 30-day distinct active users in pandas: spine + merge, rolling().nunique, difference array; versus SQL range join
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-28 09:00:00'),(1,'2024-02-20 09:00:00'),(1,'2024-03-15 09:00:00'),
 (2,'2024-02-05 10:00:00'),(2,'2024-02-06 10:00:00'),
 (3,'2024-03-01 11:00:00'),(3,'2024-03-02 11:00:00'),(3,'2024-03-02 15:00:00'),
 (4,'2024-02-02 12:00:00'),
 (5,'2024-03-20 13:00:00');
"""
SQL_MAIN = """
WITH RECURSIVE sp(day) AS (
  SELECT '2024-03-01' UNION ALL SELECT date(day, '+1 day') FROM sp WHERE day < '2024-03-31'
), d AS (SELECT DISTINCT user_id, date(event_ts) AS day FROM events)
SELECT sp.day, COUNT(DISTINCT d.user_id) AS rolling_30d_users
FROM sp LEFT JOIN d ON d.day BETWEEN date(sp.day, '-29 days') AND sp.day
GROUP BY sp.day
ORDER BY sp.day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
events = pd.read_sql_query("SELECT * FROM events", con)

# does rolling().nunique exist in this pandas?
print("pandas", pd.__version__, "| Rolling has nunique:", hasattr(pd.Series([1]).rolling(2), "nunique"))

# pd:main
ev = events.assign(day=pd.to_datetime(events["event_ts"]).dt.normalize())[["user_id", "day"]].drop_duplicates()
spine = pd.DataFrame({"day": pd.date_range("2024-03-01", "2024-03-31")})
# (1) spine x events merge, filter to the 30-day window, groupby().nunique()
x = spine.merge(ev, how="cross", suffixes=("", "_ev"))
x = x[(x["day_ev"] <= x["day"]) & (x["day_ev"] >= x["day"] - pd.Timedelta(days=29))]
merge_df = (x.groupby("day")["user_id"].nunique().reindex(spine["day"], fill_value=0)
              .rename("rolling_30d_users").reset_index())
# (2) per-day set union over a sliding window of daily user sets
by_day = ev.groupby("day")["user_id"].agg(set)
sets_df = pd.DataFrame({"day": spine["day"], "rolling_30d_users": [
    len(set().union(*[by_day.get(t, set()) for t in pd.date_range(dd - pd.Timedelta(days=29), dd)]))
    for dd in spine["day"]]})
# (3) difference array: a user is counted from an active day until 30 days after it, or until their next active day
e = ev.sort_values(["user_id", "day"]).copy()
e["nxt"] = e.groupby("user_id")["day"].shift(-1)
e["end"] = np.minimum(e["day"] + pd.Timedelta(days=30), e["nxt"].fillna(pd.Timestamp.max))
idx = pd.date_range("2024-01-01", "2024-04-30")
delta = pd.Series(0, index=idx, dtype="int64")
delta = delta.add(e.groupby("day").size(), fill_value=0).sub(e.groupby("end").size(), fill_value=0)
diff_df = (delta.cumsum().reindex(spine["day"]).astype(int).rename("rolling_30d_users").reset_index())
# (4) rolling('30D').nunique over events plus one spine row (NaN user) at the end of each day
rows = pd.concat([ev.assign(ts=ev["day"]), pd.DataFrame({"user_id": np.nan, "ts": spine["day"] + pd.Timedelta(hours=23, minutes=59)})])
rows = rows.sort_values("ts", kind="stable")
r = rows.rolling("30D", on="ts")["user_id"].nunique()
roll_df = (rows.assign(n=r)[rows["user_id"].isna()][["ts", "n"]]
              .assign(day=lambda d: d["ts"].dt.normalize())[["day", "n"]]
              .rename(columns={"n": "rolling_30d_users"}).reset_index(drop=True))
roll_df["rolling_30d_users"] = roll_df["rolling_30d_users"].astype(int)
# pd:end
sql_cmp = sql_df.assign(day=pd.to_datetime(sql_df["day"]))
for name, got in [("merge", merge_df), ("sets", sets_df), ("diff array", diff_df), ("rolling.nunique + spine", roll_df)]:
    pd.testing.assert_frame_equal(sql_cmp.sort_values("day").reset_index(drop=True),
                                  got.sort_values("day").reset_index(drop=True), check_dtype=False, check_freq=False)
    print("equal to SQL:", name)
print(sql_df.to_string(index=False))
print("cross-merge rows:", len(spine.merge(ev, how="cross")), "| after window filter:", len(x), "| distinct user-days:", len(ev))
# naive wrong version: rolling('30D').nunique over event rows only, then ffill onto the spine (users never expire on quiet days)
naive = (ev.sort_values("day").rolling("30D", on="day")["user_id"].nunique().groupby(ev.sort_values("day")["day"]).last())
naive = naive.reindex(spine["day"]).ffill().fillna(0).astype(int)
bad = (naive.to_numpy() != sql_df["rolling_30d_users"].to_numpy())
print("days where the event-only rolling + ffill is wrong:", [str(d.date()) for d in spine["day"][bad]])
print("asserts passed")
