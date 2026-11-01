# Q38: duplicates and dedup in funnels: (a) event_id, (b) one row per user and step, (c) 5-second near-duplicate with LAG
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,1,'2024-03-01 10:00:00','view'),
 (2,1,'2024-03-01 10:01:00','cart'),
 (3,1,'2024-03-01 10:02:00','purchase'),
 (3,1,'2024-03-01 10:02:00','purchase'),
 (4,1,'2024-03-01 13:00:00','purchase'),
 (5,2,'2024-03-01 11:00:00','view'),
 (6,2,'2024-03-01 11:00:00','cart'),
 (7,2,'2024-03-01 11:00:04','cart'),
 (7,2,'2024-03-01 11:00:05','cart'),
 (8,2,'2024-03-01 11:00:08','cart'),
 (9,3,'2024-03-01 12:00:00','view'),
 (10,3,'2024-03-01 12:05:00','purchase'),
 (11,3,'2024-03-01 12:05:02','purchase');
"""
# (a) exact duplicates by event_id: keep the earliest row per event_id
A = """
SELECT event_id, user_id, event_ts, event_name FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY event_ts) AS rn FROM events
) WHERE rn = 1
"""
# (b) one row per user and step
B = """
SELECT user_id, event_name, MIN(event_ts) AS event_ts, COUNT(*) AS raw_rows FROM events GROUP BY user_id, event_name
"""
# (c) 5-second rule: drop a row if the previous row of the same user and step is 5 seconds or less earlier
C = """
SELECT event_id, user_id, event_ts, event_name FROM (
  SELECT *, LAG(event_ts) OVER (PARTITION BY user_id, event_name ORDER BY event_ts, event_id) AS prev_ts
  FROM (SELECT event_id, user_id, event_ts, event_name FROM (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY event_ts) AS rn FROM events) WHERE rn = 1)
) WHERE prev_ts IS NULL OR unixepoch(event_ts) - unixepoch(prev_ts) > 5
"""
SQL_MAIN = """
WITH raw AS (SELECT 'raw' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users FROM events GROUP BY event_name),
a AS (SELECT 'a_event_id' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name),
b AS (SELECT 'b_user_step' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name),
c AS (SELECT 'c_5s_lag' AS method, event_name, COUNT(*) AS rows_, COUNT(DISTINCT user_id) AS users
      FROM (%s) GROUP BY event_name)
SELECT method,
       SUM(CASE WHEN event_name='view' THEN rows_ END)     AS view_rows,
       SUM(CASE WHEN event_name='cart' THEN rows_ END)     AS cart_rows,
       SUM(CASE WHEN event_name='purchase' THEN rows_ END) AS purchases,
       SUM(CASE WHEN event_name='purchase' THEN users END) AS purchasers,
       ROUND(1.0 * SUM(CASE WHEN event_name='purchase' THEN rows_ END)
                 / SUM(CASE WHEN event_name='purchase' THEN users END), 2) AS per_purchaser
FROM (SELECT * FROM raw UNION ALL SELECT * FROM a UNION ALL SELECT * FROM b UNION ALL SELECT * FROM c)
GROUP BY method
ORDER BY CASE method WHEN 'raw' THEN 0 WHEN 'a_event_id' THEN 1 WHEN 'b_user_step' THEN 2 ELSE 3 END
""" % (A, B, C)
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("SELECT DISTINCT * rows:", con.execute("SELECT COUNT(*) FROM (SELECT DISTINCT * FROM events)").fetchone()[0],
      "| rows:", con.execute("SELECT COUNT(*) FROM events").fetchone()[0],
      "| distinct event_id:", con.execute("SELECT COUNT(DISTINCT event_id) FROM events").fetchone()[0])
print("cart rows kept by (c) for user 2 (event_ids):", [r[0] for r in con.execute("SELECT event_id FROM (%s) WHERE user_id=2 AND event_name='cart' ORDER BY event_ts" % C)])

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
def summarise(df, method):
    g = df.groupby("event_name")
    rows, users = g.size(), g["user_id"].nunique()
    return {"method": method, "view_rows": int(rows.get("view", 0)), "cart_rows": int(rows.get("cart", 0)),
            "purchases": int(rows.get("purchase", 0)), "purchasers": int(users.get("purchase", 0)),
            "per_purchaser": round(rows.get("purchase", 0) / users.get("purchase", 1), 2)}
ev = events.assign(ts=pd.to_datetime(events["event_ts"]))
a = ev.sort_values("ts", kind="stable").drop_duplicates("event_id", keep="first")
b = ev.drop_duplicates(["user_id", "event_name"], keep="first")
c = a.sort_values(["user_id", "event_name", "ts", "event_id"], kind="stable")
prev = c.groupby(["user_id", "event_name"])["ts"].shift()
c = c[prev.isna() | ((c["ts"] - prev).dt.total_seconds() > 5)]
pd_df = pd.DataFrame([summarise(ev, "raw"), summarise(a, "a_event_id"),
                      summarise(b, "b_user_step"), summarise(c, "c_5s_lag")])
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # same method order in both
assert len(ev.drop_duplicates(["event_id", "user_id", "event_ts", "event_name"])) == 12  # same as SELECT DISTINCT *: event 7 survives twice
print("asserts passed")
