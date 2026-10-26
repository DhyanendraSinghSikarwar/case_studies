# Q15: trailing 7-day distinct active users with a date spine
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_date TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01'),(1,'2025-03-01'),(1,'2025-03-02'),(1,'2025-03-08'),(1,'2025-03-09'),
 (2,'2025-03-01'),(2,'2025-03-03'),
 (3,'2025-03-02'),(3,'2025-03-02'),(3,'2025-03-12'),
 (4,'2025-03-05'),(4,'2025-03-06'),(4,'2025-03-06'),(4,'2025-03-13'),
 (5,'2025-03-09'),(5,'2025-03-14'),
 (6,'2025-03-10');
""")
sql = """
WITH RECURSIVE spine(d) AS (
  SELECT '2025-03-07' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2025-03-14')
SELECT s.d AS day, COUNT(DISTINCT e.user_id) AS active_7d
FROM spine s LEFT JOIN events e ON e.event_date BETWEEN date(s.d, '-6 days') AND s.d
GROUP BY s.d ORDER BY s.d
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

# the plain 7-row window on daily distinct counts: sums users more than once
wrong = """
WITH RECURSIVE spine(d) AS (
  SELECT '2025-03-01' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2025-03-14'),
daily AS (SELECT s.d, COUNT(DISTINCT e.user_id) AS dau FROM spine s LEFT JOIN events e ON e.event_date = s.d GROUP BY s.d),
daily_nospine AS (SELECT event_date AS d, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY event_date)
SELECT x.d AS day, x.w_spine, y.w_nospine FROM
 (SELECT d, SUM(dau) OVER (ORDER BY d ROWS 6 PRECEDING) AS w_spine FROM daily) x
 LEFT JOIN (SELECT d, SUM(dau) OVER (ORDER BY d ROWS 6 PRECEDING) AS w_nospine FROM daily_nospine) y ON y.d = x.d
WHERE x.d >= '2025-03-07' ORDER BY x.d
"""
w = pd.read_sql(wrong, con)
print("\nwrong windows (sum of daily distinct counts; w_nospine is NULL on days that have no events, 03-07 and 03-11, because that table has no row for them)")
print(w.to_string(index=False))

ev = pd.read_sql("SELECT * FROM events", con)
ev["event_date"] = pd.to_datetime(ev.event_date)
spine = pd.DataFrame({"day": pd.date_range("2025-03-07", "2025-03-14")})
m = spine.merge(ev, how="cross")
m = m[(m.event_date >= m.day - pd.Timedelta(days=6)) & (m.event_date <= m.day)]
cnt = m.groupby("day")["user_id"].nunique().reindex(spine.day, fill_value=0)
p = cnt.rename("active_7d").reset_index()
p["day"] = p.day.dt.strftime("%Y-%m-%d")
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows in day order")
