# Q19: sessions per user with a 30-minute timeout (a gap of exactly 30:00 starts a new session)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-01 09:10:00'),(1,'2025-03-01 09:40:00'),(1,'2025-03-01 09:50:00'),(1,'2025-03-01 10:30:00'),
 (2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:29:59'),(2,'2025-03-01 11:00:00'),
 (3,'2025-03-01 12:00:00');
""")
sql = """
WITH l AS (
  SELECT user_id, event_ts,
         strftime('%s', event_ts) - strftime('%s', LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts)) AS gap_s
  FROM events),
f AS (SELECT user_id, event_ts, CASE WHEN gap_s IS NULL OR gap_s >= 1800 THEN 1 ELSE 0 END AS new_sess FROM l),
s AS (SELECT user_id, SUM(new_sess) OVER (PARTITION BY user_id ORDER BY event_ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sess FROM f),
per AS (SELECT user_id, sess, COUNT(*) AS n FROM s GROUP BY user_id, sess)
SELECT user_id, COUNT(*) AS sessions, SUM(n) AS events, ROUND(1.0 * SUM(n) / COUNT(*), 2) AS avg_events_per_session
FROM per GROUP BY user_id ORDER BY user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

e = pd.read_sql("SELECT * FROM events", con)
e["ts"] = pd.to_datetime(e.event_ts)
e = e.sort_values(["user_id", "ts"])
gap = e.groupby("user_id")["ts"].diff()
e["new_sess"] = gap.isna() | (gap >= pd.Timedelta(minutes=30))
e["sess"] = e.groupby("user_id")["new_sess"].cumsum()
per = e.groupby(["user_id", "sess"]).size().rename("n").reset_index()
p = per.groupby("user_id").agg(sessions=("sess", "size"), events=("n", "sum")).reset_index()
p["avg_events_per_session"] = (p.events / p.sessions).round(2)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by user_id")

# boundary check: > 1800 instead of >= 1800 would merge user 1's second session into the first
print("\nif the rule were gap > 30 min (strict), user 1 would have",
      int(((gap.isna()) | (gap > pd.Timedelta(minutes=30)))[e.user_id == 1].groupby(e.user_id).sum().iloc[0]), "sessions")
