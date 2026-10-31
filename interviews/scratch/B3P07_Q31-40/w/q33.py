# Q33: subscription active periods from daily snapshots, SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sub_snapshot(user_id TEXT, snap_date TEXT, is_active INTEGER);
INSERT INTO sub_snapshot VALUES
 ('U1','2024-03-05',1),('U1','2024-03-01',1),('U1','2024-03-02',1),('U1','2024-03-02',1),('U1','2024-03-03',1),
 ('U1','2024-03-04',0),('U1','2024-03-06',1),
 ('U2','2024-03-01',1),('U2','2024-03-02',1),('U2','2024-03-04',1),
 ('U3','2024-03-01',0),('U3','2024-03-02',0),
 ('U4','2024-03-03',1),
 ('U5','2024-03-01',1),('U5','2024-03-02',NULL),('U5','2024-03-03',1),('U5','2024-03-04',1);
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, snap_date FROM sub_snapshot WHERE is_active = 1
),
r AS (
  SELECT user_id, snap_date,
         julianday(snap_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS k
  FROM d
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM r
GROUP BY user_id, k
ORDER BY user_id, active_from
"""
SQL_ROWBASED = """
WITH t AS (
  SELECT user_id, snap_date, is_active,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS rn_all
  FROM (SELECT DISTINCT user_id, snap_date, is_active FROM sub_snapshot)
),
f AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS rn_act
  FROM t WHERE is_active = 1
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM f
GROUP BY user_id, rn_all - rn_act
ORDER BY user_id, active_from
"""
SQL_WRONG = """
WITH t AS (
  SELECT user_id, snap_date, is_active,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY snap_date) AS rn_all
  FROM (SELECT DISTINCT user_id, snap_date, is_active FROM sub_snapshot)
)
SELECT user_id, MIN(snap_date) AS active_from, MAX(snap_date) AS active_to, COUNT(*) AS days
FROM t WHERE is_active = 1
GROUP BY user_id, julianday(snap_date) - rn_all
ORDER BY user_id, active_from
"""
SQL_RESUB = """
WITH p AS (""" + SQL_MAIN.replace("ORDER BY user_id, active_from", "") + """)
SELECT u.user_id, COUNT(p.user_id) AS periods,
       MAX(COUNT(p.user_id) - 1, 0) AS resubscribed
FROM (SELECT DISTINCT user_id FROM sub_snapshot) u
LEFT JOIN p ON p.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main (filter first, date-based key):")
print(sql_df.to_string(index=False))
print("SQL row-based (ROW_NUMBER over all rows minus over active rows):")
print(pd.read_sql_query(SQL_ROWBASED, con).to_string(index=False))
print("wrong: date minus ROW_NUMBER over all rows, then filter:")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))
sql_res = pd.read_sql_query(SQL_RESUB, con)
print("periods and resubscriptions per user:")
print(sql_res.to_string(index=False))

snap = pd.read_sql_query("SELECT * FROM sub_snapshot", con)
# pd:main
a = snap[snap["is_active"] == 1][["user_id", "snap_date"]].drop_duplicates()
a = a.assign(d=pd.to_datetime(a["snap_date"])).sort_values(["user_id", "d"])
a["k"] = (a["d"] - pd.Timestamp("1970-01-01")).dt.days - a.groupby("user_id").cumcount()
pd_df = (a.groupby(["user_id", "k"])
          .agg(active_from=("snap_date", "min"), active_to=("snap_date", "max"), days=("snap_date", "size"))
          .reset_index().drop(columns="k").sort_values(["user_id", "active_from"]).reset_index(drop=True))
users = pd.DataFrame({"user_id": sorted(snap["user_id"].unique())})
cnt = pd_df.groupby("user_id").size().rename("periods")
pd_res = users.merge(cnt, on="user_id", how="left").fillna({"periods": 0}).astype({"periods": "int64"})
pd_res["resubscribed"] = (pd_res["periods"] - 1).clip(lower=0)
# pd:end
print("pandas periods:")
print(pd_df.to_string(index=False))
# compare after sorting by user_id, active_from (and user_id for the summary)
assert pd_df.equals(sql_df)
assert pd_res.equals(sql_res.astype({"periods": "int64", "resubscribed": "int64"}))
print("asserts passed")
