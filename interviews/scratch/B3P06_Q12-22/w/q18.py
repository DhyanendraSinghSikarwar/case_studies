# Q18: month-over-month retention (active in m and m+1), lost users, pandas merge on shifted period
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-03 10:00:00'),(1,'2024-01-20 10:00:00'),(1,'2024-02-05 10:00:00'),(1,'2024-03-07 10:00:00'),
 (2,'2024-01-11 10:00:00'),(2,'2024-03-15 10:00:00'),
 (3,'2024-01-25 10:00:00'),(3,'2024-02-14 10:00:00'),
 (4,'2024-02-02 10:00:00'),(4,'2024-03-02 10:00:00'),(4,'2024-04-09 10:00:00'),
 (5,'2024-03-21 10:00:00'),
 (6,'2024-01-29 10:00:00');
"""
LAST_COMPLETE = "2024-04"   # April is the last loaded month, so April -> May cannot be judged
SQL_MAIN = """
WITH um AS (
  SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events
)
SELECT a.m AS month,
       COUNT(*) AS active_users,
       CASE WHEN a.m < :last_month THEN COUNT(b.user_id) END AS active_next_month,
       CASE WHEN a.m < :last_month THEN COUNT(*) - COUNT(b.user_id) END AS lost_next_month,
       CASE WHEN a.m < :last_month THEN ROUND(100.0 * COUNT(b.user_id) / COUNT(*), 1) END AS retention_pct
FROM um a
LEFT JOIN um b
  ON b.user_id = a.user_id
 AND b.m = strftime('%Y-%m', date(a.m || '-01', '+1 month'))
GROUP BY a.m
ORDER BY a.m
"""
SQL_INTERSECT = """
SELECT user_id FROM (SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events) WHERE m = '2024-01'
INTERSECT
SELECT user_id FROM (SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events) WHERE m = '2024-02'
ORDER BY user_id
"""
SQL_LOST = """
WITH um AS (SELECT DISTINCT user_id, strftime('%Y-%m', event_ts) AS m FROM events)
SELECT a.m AS month, a.user_id
FROM um a
WHERE a.m < :last_month
  AND NOT EXISTS (SELECT 1 FROM um b WHERE b.user_id = a.user_id
                  AND b.m = strftime('%Y-%m', date(a.m || '-01', '+1 month')))
ORDER BY a.m, a.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"last_month": LAST_COMPLETE})
print(sql_df.to_string(index=False))
print("INTERSECT, active in both 2024-01 and 2024-02:", [r[0] for r in con.execute(SQL_INTERSECT)])
lost = pd.read_sql_query(SQL_LOST, con, params={"last_month": LAST_COMPLETE})
print("users active in m but not m+1:"); print(lost.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
um = e.assign(m=e["event_ts"].dt.to_period("M"))[["user_id", "m"]].drop_duplicates()
nxt = um.assign(m=um["m"] - 1, seen_next=1)          # the user's next-month row, moved back one period
j = um.merge(nxt, on=["user_id", "m"], how="left")
g = j.groupby("m").agg(active_users=("user_id", "size"), active_next_month=("seen_next", "count")).reset_index()
g["lost_next_month"] = g["active_users"] - g["active_next_month"]
g["retention_pct"] = (100.0 * g["active_next_month"] / g["active_users"]).round(1)
last = pd.Period(LAST_COMPLETE, "M")
g.loc[g["m"] >= last, ["active_next_month", "lost_next_month", "retention_pct"]] = float("nan")
g["month"] = g["m"].astype(str)
pd_df = g[["month", "active_users", "active_next_month", "lost_next_month", "retention_pct"]]
# pd:end
# compared in ascending month order
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas equals SQL")
# set-operation form of the same thing
sets = um.groupby("m")["user_id"].apply(set)
both = sets[pd.Period("2024-01")] & sets[pd.Period("2024-02")]
assert sorted(both) == [r[0] for r in con.execute(SQL_INTERSECT)]
lost_pd = [(str(p), u) for p in sets.index[:-1] for u in sorted(sets[p] - sets.get(p + 1, set()))]
assert lost_pd == [tuple(x) for x in lost.itertuples(index=False)]
print("set logic (intersection, difference) equals SQL")
print("asserts passed")
