# Q17: purchase within 7 days after the first view, mature viewers only (as-of 2024-03-31)
import sqlite3
import pandas as pd

AS_OF_END = "2024-04-01 00:00:00"   # data complete up to (not including) this instant

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-08 10:00:00','purchase'),
 (2,'2024-03-01 10:00:00','view'),(2,'2024-03-08 10:01:00','purchase'),
 (3,'2024-03-01 09:00:00','purchase'),(3,'2024-03-01 10:00:00','view'),
 (4,'2024-03-02 08:00:00','view'),(4,'2024-03-03 08:00:00','purchase'),
 (5,'2024-03-20 12:00:00','view'),
 (6,'2024-03-28 12:00:00','view'),(6,'2024-03-29 12:00:00','purchase'),
 (7,'2024-03-05 09:00:00','view'),(7,'2024-03-12 09:00:00','view'),(7,'2024-03-13 09:00:00','purchase'),
 (8,'2024-02-28 10:00:00','purchase'),(8,'2024-03-10 10:00:00','view'),(8,'2024-03-12 10:00:00','purchase'),
 (9,'2024-03-15 10:00:00','purchase');
"""

SQL_MAIN = """
WITH fv AS (
  SELECT user_id, MIN(event_ts) AS first_view
  FROM events
  WHERE event_name = 'view'
  GROUP BY user_id
), mature AS (
  SELECT user_id, first_view
  FROM fv
  WHERE datetime(first_view, '+7 days') < :as_of_end
), flagged AS (
  SELECT m.user_id,
         CASE WHEN EXISTS (
                SELECT 1 FROM events p
                WHERE p.user_id = m.user_id
                  AND p.event_name = 'purchase'
                  AND p.event_ts >= m.first_view
                  AND p.event_ts <= datetime(m.first_view, '+7 days')
              ) THEN 1 ELSE 0 END AS converted
  FROM mature m
)
SELECT COUNT(*) AS mature_viewers,
       SUM(converted) AS converted_7d,
       ROUND(100.0 * SUM(converted) / COUNT(*), 1) AS conversion_pct
FROM flagged
"""

# per-user detail for the walk-through (includes the julianday check)
SQL_DETAIL = """
WITH fv AS (SELECT user_id, MIN(event_ts) AS first_view FROM events WHERE event_name = 'view' GROUP BY user_id)
SELECT fv.user_id, fv.first_view,
       datetime(fv.first_view, '+7 days') AS window_end,
       CASE WHEN datetime(fv.first_view, '+7 days') < :as_of_end THEN 1 ELSE 0 END AS mature,
       (SELECT MIN(p.event_ts) FROM events p WHERE p.user_id = fv.user_id AND p.event_name = 'purchase'
          AND p.event_ts >= fv.first_view) AS first_purchase_after_view,
       (SELECT MIN(unixepoch(p.event_ts) - unixepoch(fv.first_view)) FROM events p
         WHERE p.user_id = fv.user_id AND p.event_name = 'purchase' AND p.event_ts >= fv.first_view) AS secs_after_view
FROM fv ORDER BY fv.user_id
"""

# anchoring on the latest view before each purchase: a purchase converts if ANY view lies in the 7 days before it
SQL_LATEST_VIEW = """
WITH fv AS (SELECT user_id, MIN(event_ts) AS first_view FROM events WHERE event_name = 'view' GROUP BY user_id),
mature AS (SELECT user_id FROM fv WHERE datetime(first_view, '+7 days') < :as_of_end)
SELECT COUNT(*) AS mature_viewers,
       SUM(CASE WHEN EXISTS (
             SELECT 1 FROM events p JOIN events v
               ON v.user_id = p.user_id AND v.event_name = 'view'
              AND v.event_ts <= p.event_ts AND p.event_ts <= datetime(v.event_ts, '+7 days')
             WHERE p.user_id = m.user_id AND p.event_name = 'purchase'
           ) THEN 1 ELSE 0 END) AS converted_latest_view_anchor
FROM mature m
"""

# the julianday version for comparison
SQL_JULIAN = """
SELECT user_id, (julianday(p) - julianday(v)) * 86400 AS secs, (julianday(p) - julianday(v)) <= 7 AS within_7_julianday
FROM (SELECT e.user_id, MIN(CASE WHEN e.event_name='view' THEN e.event_ts END) AS v,
             MIN(CASE WHEN e.event_name='purchase' THEN e.event_ts END) AS p
      FROM events e GROUP BY e.user_id) WHERE user_id = 1
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"as_of_end": AS_OF_END}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))
print(pd.read_sql_query(SQL_DETAIL, con, params=P).to_string(index=False))
print("latest-view anchor:", pd.read_sql_query(SQL_LATEST_VIEW, con, params=P).to_dict("records"))
print("julianday check, user 1 (exactly 7 days):", con.execute(SQL_JULIAN).fetchall())

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
ev = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
fv = (ev[ev["event_name"] == "view"].groupby("user_id", as_index=False)["event_ts"].min()
        .rename(columns={"event_ts": "first_view"}))
fv = fv[fv["first_view"] + pd.Timedelta(days=7) < pd.Timestamp(AS_OF_END)]
pu = ev[ev["event_name"] == "purchase"][["user_id", "event_ts"]].rename(columns={"event_ts": "purchase_ts"})
j = fv.merge(pu, on="user_id", how="left")
j["ok"] = (j["purchase_ts"] >= j["first_view"]) & (j["purchase_ts"] <= j["first_view"] + pd.Timedelta(days=7))
converted = int(j.groupby("user_id")["ok"].max().sum())
pd_df = pd.DataFrame([{"mature_viewers": len(fv), "converted_7d": converted,
                       "conversion_pct": round(100.0 * converted / len(fv), 1)}])
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # one row
# without the maturity rule, everyone who viewed counts, including user 6
fv_all = (ev[ev["event_name"] == "view"].groupby("user_id", as_index=False)["event_ts"].min()
            .rename(columns={"event_ts": "first_view"}))
j2 = fv_all.merge(pu, on="user_id", how="left")
j2["ok"] = (j2["purchase_ts"] >= j2["first_view"]) & (j2["purchase_ts"] <= j2["first_view"] + pd.Timedelta(days=7))
print("no maturity rule: viewers", len(fv_all), "converted", int(j2.groupby("user_id")["ok"].max().sum()),
      "rate", round(100.0 * int(j2.groupby("user_id")["ok"].max().sum()) / len(fv_all), 1))
print("asserts passed")
