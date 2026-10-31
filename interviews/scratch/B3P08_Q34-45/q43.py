# Q43: signup_done -> kyc_done -> first_payment by signup month and device, with median hours kyc -> payment
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, device TEXT);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','ios'),(2,'2024-01-06','ios'),(3,'2024-01-07','ios'),(4,'2024-01-10','ios'),
 (5,'2024-01-12','android'),(6,'2024-01-15','android'),
 (7,'2024-02-03','ios'),(8,'2024-02-04','ios'),(9,'2024-02-10','android'),(10,'2024-02-11','android'),
 (11,'2024-03-05','ios'),(12,'2024-03-06','android'),(13,'2024-01-20','ios');
INSERT INTO events VALUES
 (1,'2024-01-05 10:00:00','signup_done'),(1,'2024-01-05 11:00:00','kyc_done'),(1,'2024-01-05 17:00:00','first_payment'),
 (2,'2024-01-06 10:00:00','signup_done'),(2,'2024-01-06 12:00:00','kyc_done'),(2,'2024-01-07 12:00:00','first_payment'),
 (3,'2024-01-07 10:00:00','signup_done'),(3,'2024-01-07 12:00:00','kyc_done'),(3,'2024-01-10 12:00:00','first_payment'),
 (4,'2024-01-10 10:00:00','signup_done'),(4,'2024-01-10 13:00:00','kyc_done'),
 (5,'2024-01-12 10:00:00','signup_done'),(5,'2024-01-12 14:00:00','kyc_done'),(5,'2024-01-12 16:00:00','first_payment'),
 (6,'2024-01-15 10:00:00','signup_done'),(6,'2024-01-16 10:00:00','first_payment'),
 (7,'2024-02-03 10:00:00','signup_done'),(7,'2024-02-03 12:00:00','kyc_done'),(7,'2024-02-03 14:00:00','first_payment'),
 (8,'2024-02-04 10:00:00','signup_done'),(8,'2024-02-04 12:00:00','kyc_done'),
 (9,'2024-02-10 10:00:00','signup_done'),
 (10,'2024-02-11 10:00:00','signup_done'),(10,'2024-02-11 11:00:00','kyc_done'),(10,'2024-02-11 13:00:00','first_payment'),
 (11,'2024-03-05 10:00:00','signup_done'),(11,'2024-03-05 11:00:00','kyc_done'),(11,'2024-03-05 12:00:00','first_payment'),
 (12,'2024-03-06 10:00:00','signup_done'),
 (13,'2024-01-20 10:00:00','signup_done'),(13,'2024-01-20 11:00:00','kyc_done'),(13,'2024-01-20 23:00:00','first_payment');
"""
# as-of 2024-04-05; a cohort is mature when its month end plus 30 days is on or before the as-of date
SQL_MAIN = """
WITH t AS (
  SELECT u.user_id, strftime('%Y-%m', u.signup_date) AS cohort, u.device,
         MIN(CASE WHEN e.event_name = 'signup_done'   THEN e.event_ts END) AS t1,
         MIN(CASE WHEN e.event_name = 'kyc_done'      THEN e.event_ts END) AS t2,
         MIN(CASE WHEN e.event_name = 'first_payment' THEN e.event_ts END) AS t3
  FROM users u LEFT JOIN events e ON e.user_id = u.user_id AND e.event_ts <= '2024-04-05 23:59:59'
  GROUP BY u.user_id
), s AS (                                   -- strict chain: each step needs the previous one, in time order
  SELECT cohort, device, user_id,
         COALESCE(t1 IS NOT NULL, 0)                                      AS s1,
         COALESCE(t1 IS NOT NULL AND t2 >= t1, 0)                        AS s2,
         COALESCE(t1 IS NOT NULL AND t2 >= t1 AND t3 >= t2, 0)           AS s3,
         CASE WHEN t2 >= t1 AND t3 >= t2
              THEN (unixepoch(t3) - unixepoch(t2)) / 3600.0 END          AS lag_h
  FROM t
), r AS (
  SELECT cohort, device, lag_h,
         ROW_NUMBER() OVER (PARTITION BY cohort, device ORDER BY lag_h) AS rn,
         COUNT(lag_h)  OVER (PARTITION BY cohort, device)               AS n
  FROM s WHERE lag_h IS NOT NULL
), med AS (
  SELECT cohort, device,
         MAX(CASE WHEN rn = (n + 1) / 2 THEN lag_h END)                          AS median_lower,
         AVG(CASE WHEN rn IN ((n + 1) / 2, (n + 2) / 2) THEN lag_h END)          AS median_avg
  FROM r GROUP BY cohort, device
)
SELECT s.cohort, s.device,
       SUM(s1) AS signup_done, SUM(s2) AS kyc_done, SUM(s3) AS first_payment,
       ROUND(1.0 - 1.0 * SUM(s2) / SUM(s1), 3) AS drop_signup_kyc,
       ROUND(1.0 - 1.0 * SUM(s3) / NULLIF(SUM(s2), 0), 3) AS drop_kyc_payment,
       med.median_lower, med.median_avg,
       CASE WHEN date(s.cohort || '-01', '+1 month', '+30 days') <= '2024-04-05' THEN 1 ELSE 0 END AS mature
FROM s LEFT JOIN med ON med.cohort = s.cohort AND med.device = s.device
GROUP BY s.cohort, s.device
ORDER BY s.cohort, s.device
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("NTILE(2) is not a median: first NTILE(2) bucket of 3 values has", con.execute(
    "SELECT COUNT(*) FROM (SELECT NTILE(2) OVER (ORDER BY x) AS b FROM (SELECT 6 AS x UNION ALL SELECT 24 UNION ALL SELECT 72)) WHERE b=1").fetchone()[0], "rows")
print("integer division 7/2 in SQLite:", con.execute("SELECT 7/2, 8/2, (3+1)/2, (3+2)/2").fetchone())

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
asof = pd.Timestamp("2024-04-05 23:59:59")
ev = events.assign(ts=pd.to_datetime(events["event_ts"]))
ev = ev[ev["ts"] <= asof]
t = (ev.pivot_table(index="user_id", columns="event_name", values="ts", aggfunc="min")
       .reindex(columns=["signup_done", "kyc_done", "first_payment"])
       .rename(columns={"signup_done": "t1", "kyc_done": "t2", "first_payment": "t3"})
       .reindex(users["user_id"]).reset_index())
t = t.merge(users, on="user_id")
t["cohort"] = pd.to_datetime(t["signup_date"]).dt.strftime("%Y-%m")
t["s1"] = t["t1"].notna()
t["s2"] = t["s1"] & (t["t2"] >= t["t1"])
t["s3"] = t["s2"] & (t["t3"] >= t["t2"])
t["lag_h"] = np.where(t["s3"], (t["t3"] - t["t2"]).dt.total_seconds() / 3600.0, np.nan)
g = t.groupby(["cohort", "device"])
pd_df = g.agg(signup_done=("s1", "sum"), kyc_done=("s2", "sum"), first_payment=("s3", "sum"),
              median_avg=("lag_h", "median")).reset_index()
pd_df["median_lower"] = g["lag_h"].apply(lambda s: s.dropna().sort_values().iloc[(len(s.dropna()) - 1) // 2]
                                         if s.notna().any() else np.nan).to_numpy()
pd_df["drop_signup_kyc"] = (1 - pd_df["kyc_done"] / pd_df["signup_done"]).round(3)
pd_df["drop_kyc_payment"] = (1 - pd_df["first_payment"] / pd_df["kyc_done"].replace(0, np.nan)).round(3)
month_end = pd.to_datetime(pd_df["cohort"] + "-01") + pd.offsets.MonthBegin(1)
pd_df["mature"] = ((month_end + pd.Timedelta(days=30)) <= pd.Timestamp("2024-04-05")).astype(int)
pd_df = pd_df[["cohort", "device", "signup_done", "kyc_done", "first_payment", "drop_signup_kyc",
               "drop_kyc_payment", "median_lower", "median_avg", "mature"]]
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.sort_values(["cohort", "device"]).reset_index(drop=True),
                              pd_df.sort_values(["cohort", "device"]).reset_index(drop=True), check_dtype=False)
print("asserts passed")
