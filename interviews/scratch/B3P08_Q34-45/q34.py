# Q34: new, returning and resurrected active users per day (one pass, LAG over distinct active dates)
import sqlite3
import pandas as pd
import numpy as np

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-02-20',0),(2,'2024-03-01',0),(3,'2024-03-03',0),(4,'2024-02-10',0),
 (5,'2024-02-25',0),(6,'2024-03-01',1),(7,'2024-03-05',0),(8,'2024-02-28',0),
 (9,'2024-02-20',0),(10,'2024-03-02',NULL);
INSERT INTO events VALUES
 (1,'2024-02-20 08:00:00','open'),(1,'2024-03-01 09:00:00','open'),(1,'2024-03-02 09:00:00','open'),
 (1,'2024-03-05 09:00:00','open'),(1,'2024-03-12 09:00:00','open'),
 (2,'2024-03-01 10:00:00','open'),(2,'2024-03-02 10:00:00','open'),(2,'2024-03-02 18:00:00','open'),
 (2,'2024-03-04 10:00:00','open'),(2,'2024-03-07 10:00:00','open'),
 (3,'2024-03-03 11:00:00','open'),(3,'2024-03-10 11:00:00','open'),
 (4,'2024-02-12 12:00:00','open'),(4,'2024-03-07 12:00:00','open'),
 (5,'2024-03-04 13:00:00','open'),(5,'2024-03-05 13:00:00','open'),
 (6,'2024-03-01 14:00:00','open'),(6,'2024-03-02 14:00:00','open'),
 (7,'2024-03-05 15:00:00','open'),(7,'2024-03-07 15:00:00','open'),
 (8,'2024-02-28 16:00:00','open'),(8,'2024-03-06 16:00:00','open'),(8,'2024-03-07 16:00:00','open'),
 (9,'2024-02-27 17:00:00','open'),(9,'2024-03-06 17:00:00','open'),
 (10,'2024-03-02 19:00:00','open');
"""
SQL_MAIN = """
WITH d AS (                                   -- one row per user and active day, test users out
  SELECT DISTINCT e.user_id, date(e.event_ts) AS day
  FROM events e JOIN users u ON u.user_id = e.user_id
  WHERE COALESCE(u.is_test, 0) = 0
    AND date(e.event_ts) <= '2024-03-07'      -- fixed as-of, never today
), l AS (                                     -- previous active day, looking back past the window start
  SELECT user_id, day,
         LAG(day) OVER (PARTITION BY user_id ORDER BY day) AS prev_day
  FROM d
), c AS (
  SELECT l.day,
         CASE WHEN l.day = u.signup_date            THEN 'new'
              WHEN l.prev_day IS NULL               THEN 'first_seen_late'
              WHEN l.prev_day >= date(l.day, '-7 days') THEN 'returning'
              ELSE 'resurrected' END AS cls
  FROM l JOIN users u ON u.user_id = l.user_id
  WHERE l.day BETWEEN '2024-03-01' AND '2024-03-07'
)
SELECT day,
       SUM(cls = 'new')             AS new_users,
       SUM(cls = 'returning')       AS returning_users,
       SUM(cls = 'resurrected')     AS resurrected_users,
       SUM(cls = 'first_seen_late') AS first_seen_late,
       COUNT(*)                     AS dau
FROM c
GROUP BY day
ORDER BY day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
test_ids = users.loc[users["is_test"].fillna(0).eq(1), "user_id"]
ev = events[~events["user_id"].isin(test_ids)].copy()
ev["day"] = pd.to_datetime(ev["event_ts"]).dt.normalize()
ev = ev[ev["day"] <= "2024-03-07"]
d = ev[["user_id", "day"]].drop_duplicates().sort_values(["user_id", "day"])
d["prev_day"] = d.groupby("user_id")["day"].shift()
d = d.merge(users.assign(signup=pd.to_datetime(users["signup_date"]))[["user_id", "signup"]], on="user_id")
d["cls"] = np.select(
    [d["day"].eq(d["signup"]), d["prev_day"].isna(), d["prev_day"] >= d["day"] - pd.Timedelta(days=7)],
    ["new", "first_seen_late", "returning"], default="resurrected")
w = d[(d["day"] >= "2024-03-01") & (d["day"] <= "2024-03-07")]
pd_df = (pd.crosstab(w["day"], w["cls"])
           .reindex(columns=["new", "returning", "resurrected", "first_seen_late"], fill_value=0))
pd_df["dau"] = pd_df.sum(axis=1)
pd_df = pd_df.reset_index()
pd_df["day"] = pd_df["day"].dt.strftime("%Y-%m-%d")
pd_df.columns = ["day", "new_users", "returning_users", "resurrected_users", "first_seen_late", "dau"]
# pd:end
print(pd_df.to_string(index=False))
a = sql_df.sort_values("day").reset_index(drop=True)
b = pd_df.sort_values("day").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)  # compared after sorting by day
assert (a["new_users"] + a["returning_users"] + a["resurrected_users"] + a["first_seen_late"] == a["dau"]).all()

# raw DAU straight from events (distinct users, test users out) must equal the class total
raw = con.execute("""
SELECT date(e.event_ts) AS day, COUNT(DISTINCT e.user_id) FROM events e JOIN users u USING(user_id)
WHERE COALESCE(u.is_test,0)=0 AND date(e.event_ts) BETWEEN '2024-03-01' AND '2024-03-07'
GROUP BY 1 ORDER BY 1""").fetchall()
assert [r[1] for r in raw] == a["dau"].tolist()
print("raw DAU check:", [r[1] for r in raw])

# trap: is_test = 0 instead of COALESCE keeps NULL is_test out
n_naive = con.execute("""
SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u USING(user_id)
WHERE u.is_test = 0 AND date(e.event_ts) = '2024-03-02'""").fetchone()[0]
n_ok = con.execute("""
SELECT COUNT(DISTINCT e.user_id) FROM events e JOIN users u USING(user_id)
WHERE COALESCE(u.is_test,0) = 0 AND date(e.event_ts) = '2024-03-02'""").fetchone()[0]
print("DAU 2024-03-02 with is_test = 0:", n_naive, "| with COALESCE:", n_ok)

# the 7-day boundary: user 8 (gap exactly 7 days) vs user 9 (gap 8 days) on 2024-03-06
print(pd.read_sql_query("""
WITH d AS (SELECT DISTINCT user_id, date(event_ts) AS day FROM events WHERE user_id IN (8,9)),
l AS (SELECT user_id, day, LAG(day) OVER (PARTITION BY user_id ORDER BY day) AS prev_day FROM d)
SELECT user_id, day, prev_day, CAST(julianday(day) - julianday(prev_day) AS INTEGER) AS gap_days
FROM l WHERE day = '2024-03-06' ORDER BY user_id""", con).to_string(index=False))
print("asserts passed")
