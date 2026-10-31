# Q40: attempt-level funnel: each purchase attributed to the most recent view in the previous 7 days
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-02 10:00:00','view'),(1,'2024-03-03 10:00:00','view'),(1,'2024-03-03 12:00:00','purchase'),
 (2,'2024-03-01 09:00:00','view'),(2,'2024-03-05 09:00:00','view'),
 (3,'2024-03-01 08:00:00','view'),(3,'2024-03-08 08:00:00','purchase'),
 (4,'2024-03-01 08:00:00','view'),(4,'2024-03-10 08:00:00','purchase'),
 (5,'2024-03-02 09:00:00','view'),(5,'2024-03-04 09:00:00','purchase'),(5,'2024-03-05 09:00:00','purchase'),
 (6,'2024-03-06 09:00:00','purchase'),
 (7,'2024-03-07 09:00:00','view'),(7,'2024-03-07 09:00:00','purchase'),(7,'2024-03-09 09:00:00','view');
"""
SQL_MAIN = """
WITH v AS (SELECT DISTINCT user_id, event_ts AS view_ts FROM events WHERE event_name = 'view'),
p AS (SELECT user_id, event_ts AS buy_ts FROM events WHERE event_name = 'purchase'),
m AS (                                         -- each purchase to its most recent earlier view within 7 days
  SELECT p.user_id, p.buy_ts, v.view_ts,
         ROW_NUMBER() OVER (PARTITION BY p.user_id, p.buy_ts ORDER BY v.view_ts DESC) AS rn
  FROM p JOIN v ON v.user_id = p.user_id
               AND v.view_ts < p.buy_ts
               AND unixepoch(p.buy_ts) - unixepoch(v.view_ts) <= 7 * 86400
), a AS (SELECT user_id, buy_ts, view_ts FROM m WHERE rn = 1)
SELECT (SELECT COUNT(*) FROM v)                          AS view_attempts,
       (SELECT COUNT(DISTINCT user_id || '|' || view_ts) FROM a) AS converted_attempts,
       (SELECT COUNT(*) FROM a)                          AS attributed_purchases,
       (SELECT COUNT(*) FROM p) - (SELECT COUNT(*) FROM a) AS unattributed_purchases,
       ROUND(1.0 * (SELECT COUNT(DISTINCT user_id || '|' || view_ts) FROM a) / (SELECT COUNT(*) FROM v), 4) AS attempt_conversion
"""
SQL_MAXV = """
WITH v AS (SELECT DISTINCT user_id, event_ts AS view_ts FROM events WHERE event_name = 'view'),
p AS (SELECT user_id, event_ts AS buy_ts FROM events WHERE event_name = 'purchase'),
a AS (
  SELECT p.user_id, p.buy_ts,
         (SELECT MAX(v.view_ts) FROM v WHERE v.user_id = p.user_id AND v.view_ts < p.buy_ts
            AND unixepoch(p.buy_ts) - unixepoch(v.view_ts) <= 7 * 86400) AS view_ts
  FROM p
)
SELECT COUNT(DISTINCT user_id || '|' || view_ts) AS converted_attempts, COUNT(view_ts) AS attributed_purchases FROM a
"""
SQL_USER = """
WITH f AS (SELECT user_id, MIN(event_ts) AS first_view FROM events WHERE event_name = 'view' GROUP BY user_id)
SELECT COUNT(*) AS users_with_view,
       SUM(EXISTS (SELECT 1 FROM events e WHERE e.user_id = f.user_id AND e.event_name = 'purchase'
                   AND e.event_ts > f.first_view
                   AND unixepoch(e.event_ts) - unixepoch(f.first_view) <= 7 * 86400)) AS converted_users,
       ROUND(1.0 * SUM(EXISTS (SELECT 1 FROM events e WHERE e.user_id = f.user_id AND e.event_name = 'purchase'
                   AND e.event_ts > f.first_view
                   AND unixepoch(e.event_ts) - unixepoch(f.first_view) <= 7 * 86400)) / COUNT(*), 4) AS user_conversion
FROM f
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("attempt level (join + ROW_NUMBER):"); print(sql_df.to_string(index=False))
print("correlated MAX:", con.execute(SQL_MAXV).fetchone())
print("user level, first view:"); print(pd.read_sql_query(SQL_USER, con).to_string(index=False))
# window arithmetic: datetime(x,'-7 days') versus unixepoch seconds on the exact 7-day boundary (user 3 buys 7 days after the view)
print("boundary user 3, datetime modifier says in window:",
      con.execute("SELECT '2024-03-01 08:00:00' >= datetime('2024-03-08 08:00:00','-7 days')").fetchone()[0],
      "| unixepoch diff <= 604800:", con.execute("SELECT unixepoch('2024-03-08 08:00:00') - unixepoch('2024-03-01 08:00:00') <= 7*86400").fetchone()[0])

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.assign(ts=pd.to_datetime(events["event_ts"]))
views = e.loc[e["event_name"].eq("view"), ["user_id", "ts"]].drop_duplicates().rename(columns={"ts": "view_ts"})
buys = e.loc[e["event_name"].eq("purchase"), ["user_id", "ts"]].rename(columns={"ts": "buy_ts"})
att = pd.merge_asof(buys.sort_values("buy_ts"), views.sort_values("view_ts"),
                    left_on="buy_ts", right_on="view_ts", by="user_id",
                    direction="backward", allow_exact_matches=False,
                    tolerance=pd.Timedelta(days=7))
n_views = len(views)
conv = att.dropna(subset=["view_ts"]).drop_duplicates(["user_id", "view_ts"])
pd_df = pd.DataFrame({"view_attempts": [n_views], "converted_attempts": [len(conv)],
                      "attributed_purchases": [int(att["view_ts"].notna().sum())],
                      "unattributed_purchases": [int(att["view_ts"].isna().sum())],
                      "attempt_conversion": [round(len(conv) / n_views, 4)]})
first = views.groupby("user_id")["view_ts"].min().rename("first_view").reset_index()
j = first.merge(buys, on="user_id", how="left")
hit = j[(j["buy_ts"] > j["first_view"]) & ((j["buy_ts"] - j["first_view"]) <= pd.Timedelta(days=7))]
user_conv = hit["user_id"].nunique() / len(first)
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # one row each
assert round(user_conv, 4) == pd.read_sql_query(SQL_USER, con)["user_conversion"][0]
mx = con.execute(SQL_MAXV).fetchone()
assert mx == (len(conv), int(att["view_ts"].notna().sum()))
print("pandas user-level conversion:", round(user_conv, 4), "| asserts passed")
