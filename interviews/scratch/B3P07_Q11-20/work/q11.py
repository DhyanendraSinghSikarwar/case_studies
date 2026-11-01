# Q11: sessionization with a 30 minute timeout: LAG + CASE flag + running SUM, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 1,'2024-03-01 09:00:00','open'),
 (2, 1,'2024-03-01 09:10:00','search'),
 (3, 1,'2024-03-01 09:40:00','click'),
 (4, 1,'2024-03-01 09:41:00','click'),
 (5, 1,'2024-03-01 11:00:00','open'),
 (6, 1,'2024-03-01 11:05:00','buy'),
 (7, 2,'2024-03-01 10:00:00','open'),
 (8, 3,'2024-03-01 23:50:00','open'),
 (9, 3,'2024-03-02 00:10:00','click'),
 (10,3,'2024-03-02 00:41:00','click'),
 (11,3,NULL,'ghost'),
 (12,1,'2024-03-01 09:05:00','click');
"""
SQL_MAIN = """
WITH e AS (
  SELECT user_id, event_id, event_ts,
         LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_ts
  FROM events
  WHERE event_ts IS NOT NULL
), f AS (
  SELECT user_id, event_id, event_ts,
         CASE WHEN prev_ts IS NULL
                OR (unixepoch(event_ts) - unixepoch(prev_ts)) / 60.0 > 30
              THEN 1 ELSE 0 END AS new_session
  FROM e
), s AS (
  SELECT user_id, event_id, event_ts,
         SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS session_id
  FROM f
)
SELECT user_id, session_id,
       MIN(event_ts) AS session_start,
       MAX(event_ts) AS session_end,
       COUNT(*) AS events,
       (unixepoch(MAX(event_ts)) - unixepoch(MIN(event_ts))) / 60.0 AS duration_min
FROM s
GROUP BY user_id, session_id
ORDER BY user_id, session_id
"""
SQL_GE = SQL_MAIN.replace("/ 60.0 > 30", "/ 60.0 >= 30")
assert SQL_GE != SQL_MAIN
SQL_JULIAN = SQL_MAIN.replace("(unixepoch(event_ts) - unixepoch(prev_ts)) / 60.0", "(julianday(event_ts) - julianday(prev_ts)) * 1440")
assert SQL_JULIAN != SQL_MAIN

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_gt = pd.read_sql_query(SQL_MAIN, con)
sql_ge = pd.read_sql_query(SQL_GE, con)
print("SQL, new session when gap > 30 minutes (assumed):")
print(sql_gt.to_string(index=False))
print("SQL, new session when gap >= 30 minutes:")
print(sql_ge.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)

def sessionize(events, strict=True, limit=pd.Timedelta(minutes=30)):
    # pd:main
    e = events.dropna(subset=["event_ts"]).copy()
    e["event_ts"] = pd.to_datetime(e["event_ts"])
    e = e.sort_values(["user_id", "event_ts", "event_id"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    new = gap.isna() | ((gap > limit) if strict else (gap >= limit))
    e["session_id"] = new.astype(int).groupby(e["user_id"]).cumsum()
    out = (e.groupby(["user_id", "session_id"], as_index=False)
             .agg(session_start=("event_ts", "min"), session_end=("event_ts", "max"),
                  events=("event_id", "size")))
    out["duration_min"] = (out["session_end"] - out["session_start"]).dt.total_seconds() / 60.0
    # pd:end
    for c in ("session_start", "session_end"):
        out[c] = out[c].dt.strftime("%Y-%m-%d %H:%M:%S")
    return out

pd_gt = sessionize(events, strict=True)
pd_ge = sessionize(events, strict=False)
cols = ["user_id", "session_id", "session_start", "session_end", "events", "duration_min"]
# compare after sorting by user_id, session_id (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_gt[cols].reset_index(drop=True), sql_gt[cols], check_dtype=False)
pd.testing.assert_frame_equal(pd_ge[cols].reset_index(drop=True), sql_ge[cols], check_dtype=False)
print("sessions: gap > 30 ->", len(sql_gt), "; gap >= 30 ->", len(sql_ge))

# julianday vs unixepoch on exactly 30 minute gaps
con.executescript("CREATE TABLE pairs(a TEXT, b TEXT);"
                  "INSERT INTO pairs VALUES ('2024-03-01 09:10:00','2024-03-01 09:40:00'),"
                  "('2024-03-01 23:50:00','2024-03-02 00:20:00'),('2024-03-01 09:00:00','2024-03-01 09:30:00');")
print(pd.read_sql_query(
    "SELECT a, b, printf('%.9f', (julianday(b) - julianday(a)) * 1440) AS julian_min, "
    "(julianday(b) - julianday(a)) * 1440 > 30 AS julian_gt_30, "
    "(unixepoch(b) - unixepoch(a)) / 60.0 AS unix_min, "
    "(unixepoch(b) - unixepoch(a)) / 60.0 > 30 AS unix_gt_30 FROM pairs", con).to_string(index=False))
julian = pd.read_sql_query(SQL_JULIAN, con)
print("julianday version, gap > 30: sessions =", len(julian), "(unixepoch version:", len(sql_gt), ")")
print(julian[["user_id", "session_id", "events", "duration_min"]].to_string(index=False))

# scale check: 20000 pairs that are exactly 30 minutes apart
import datetime as dt
base = dt.datetime(2024, 1, 1)
rows = []
for i in range(20000):
    a = base + dt.timedelta(minutes=7 * i + 3, seconds=i % 60)
    rows.append((a.strftime("%Y-%m-%d %H:%M:%S"), (a + dt.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")))
con.execute("CREATE TABLE big(a TEXT, b TEXT)")
con.executemany("INSERT INTO big VALUES (?, ?)", rows)
print(con.execute("SELECT COUNT(*), SUM((julianday(b)-julianday(a))*1440 > 30), "
                  "SUM((julianday(b)-julianday(a))*1440 = 30), "
                  "SUM(unixepoch(b)-unixepoch(a) = 1800) FROM big").fetchone(),
      "<- rows, julianday > 30, julianday = 30, unixepoch = 1800")
print("asserts passed")
