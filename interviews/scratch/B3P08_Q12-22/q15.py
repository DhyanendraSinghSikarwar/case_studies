# Q15: stickiness (DAU/MAU) for March 2024 with a date spine
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','US',0),
 (4,'2024-01-01','US',0),(5,'2024-01-01','UK',0),(6,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-01 09:00:00','open'),(1,'2024-03-02 09:00:00','open'),(1,'2024-03-03 09:00:00','open'),
 (1,'2024-03-10 09:00:00','open'),(1,'2024-03-31 09:00:00','open'),
 (2,'2024-03-01 10:00:00','open'),(2,'2024-03-10 10:00:00','open'),(2,'2024-03-15 10:00:00','open'),
 (2,'2024-04-01 10:00:00','open'),
 (3,'2024-03-02 11:00:00','open'),(3,'2024-03-02 11:30:00','click'),(3,'2024-03-31 11:00:00','open'),
 (4,'2024-03-31 12:00:00','open'),
 (5,'2024-02-28 08:00:00','open'),(5,'2024-03-01 08:00:00','open'),
 (6,'2024-03-01 07:00:00','open'),(6,'2024-03-02 07:00:00','open');
"""

SQL_MAIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), act AS (
  SELECT DISTINCT e.user_id, date(e.event_ts) AS d
  FROM events e
  JOIN users u ON u.user_id = e.user_id
  WHERE u.is_test = 0
    AND date(e.event_ts) BETWEEN '2024-02-01' AND '2024-03-31'
), daily AS (
  SELECT s.d, COUNT(a.user_id) AS dau
  FROM spine s
  LEFT JOIN act a ON a.d = s.d
  GROUP BY s.d
)
SELECT (SELECT COUNT(*) FROM daily)                                   AS days,
       (SELECT SUM(dau) FROM daily)                                   AS user_days,
       ROUND((SELECT AVG(dau) FROM daily), 4)                         AS avg_dau,
       (SELECT COUNT(DISTINCT user_id) FROM act
         WHERE d BETWEEN '2024-03-01' AND '2024-03-31')               AS mau_calendar,
       ROUND((SELECT AVG(dau) FROM daily) * 1.0 /
             (SELECT COUNT(DISTINCT user_id) FROM act
               WHERE d BETWEEN '2024-03-01' AND '2024-03-31'), 4)     AS stickiness_avg_dau,
       (SELECT dau FROM daily WHERE d = '2024-03-31')                 AS dau_last_day,
       (SELECT COUNT(DISTINCT user_id) FROM act
         WHERE d BETWEEN date('2024-03-31', '-29 days') AND '2024-03-31') AS mau_trailing_30,
       ROUND(1.0 * (SELECT dau FROM daily WHERE d = '2024-03-31') /
             (SELECT COUNT(DISTINCT user_id) FROM act
               WHERE d BETWEEN date('2024-03-31', '-29 days') AND '2024-03-31'), 4) AS stickiness_last_day
"""

SQL_NO_SPINE = """
SELECT ROUND(AVG(dau), 4) AS avg_dau_active_days_only, COUNT(*) AS days_counted
FROM (SELECT date(e.event_ts) AS d, COUNT(DISTINCT e.user_id) AS dau
      FROM events e JOIN users u ON u.user_id = e.user_id
      WHERE u.is_test = 0 AND date(e.event_ts) BETWEEN '2024-03-01' AND '2024-03-31'
      GROUP BY date(e.event_ts))
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.T.to_string(header=False))
print("wrong, no spine (average only over days that have events):")
print(pd.read_sql_query(SQL_NO_SPINE, con).to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
a = events.merge(users[users["is_test"] == 0], on="user_id")
a["d"] = pd.to_datetime(a["event_ts"]).dt.normalize()
a = a[(a["d"] >= pd.Timestamp("2024-02-01")) & (a["d"] <= pd.Timestamp("2024-03-31"))]
a = a[["user_id", "d"]].drop_duplicates()
spine = pd.date_range("2024-03-01", "2024-03-31", freq="D")
dau = a.groupby("d")["user_id"].nunique().reindex(spine, fill_value=0)
in_month = a[a["d"] >= pd.Timestamp("2024-03-01")]
mau = in_month["user_id"].nunique()
trail = a[a["d"] >= pd.Timestamp("2024-03-31") - pd.Timedelta(days=29)]["user_id"].nunique()
pd_df = pd.DataFrame([{
    "days": len(dau), "user_days": int(dau.sum()), "avg_dau": round(dau.mean(), 4),
    "mau_calendar": mau, "stickiness_avg_dau": round(dau.mean() / mau, 4),
    "dau_last_day": int(dau.iloc[-1]), "mau_trailing_30": trail,
    "stickiness_last_day": round(dau.iloc[-1] / trail, 4)}])
# pd:end
print(pd_df.T.to_string(header=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # one row, same column order
print("pandas without the spine reindex, mean over active days only:",
      round(a[a["d"] >= pd.Timestamp("2024-03-01")].groupby("d")["user_id"].nunique().mean(), 4))
print("days with DAU > 0:", {k.strftime("%m-%d"): int(v) for k, v in dau[dau > 0].items()})
print("asserts passed")
