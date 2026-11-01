# Q25: sessions per user per day, events per session, bounce sessions; both timeout conventions; midnight crossing
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 09:40:00','view'),(1,'2024-03-01 09:00:00','open'),(1,'2024-03-01 09:10:00','view'),(1,'2024-03-01 15:00:00','open'),
 (2,'2024-03-01 23:50:00','open'),(2,'2024-03-02 00:05:00','view'),(2,'2024-03-02 00:20:00','click'),(2,'2024-03-02 10:00:00','open'),
 (3,'2024-03-01 12:00:00','open'),(3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:20:00','click'),
 (4,'2024-03-01 08:00:00','open'),
 (5,NULL,'open'),(5,'2024-03-01 08:00:00','open'),
 (6,'2024-03-01 10:00:00','open'),(6,'2024-03-01 10:30:01','view');
"""
# {OP} is > (convention A: exactly 30 minutes still same session) or >= (convention B: exactly 30 minutes starts a new session)
SQL_TEMPLATE = """
WITH e AS (
  SELECT user_id, event_ts, unixepoch(event_ts) AS t
  FROM events
  WHERE event_ts IS NOT NULL
), f AS (
  SELECT user_id, event_ts, t,
         CASE WHEN LAG(t) OVER (PARTITION BY user_id ORDER BY t) IS NULL
                OR t - LAG(t) OVER (PARTITION BY user_id ORDER BY t) {OP} 1800
              THEN 1 ELSE 0 END AS new_session
  FROM e
), g AS (
  SELECT user_id, event_ts,
         SUM(new_session) OVER (PARTITION BY user_id ORDER BY t
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_no
  FROM f
), s AS (
  SELECT user_id, session_no, MIN(event_ts) AS session_start, MAX(event_ts) AS session_end, COUNT(*) AS n_events
  FROM g
  GROUP BY user_id, session_no
)
SELECT user_id,
       date(session_start) AS day,
       COUNT(*) AS sessions,
       ROUND(AVG(n_events), 2) AS avg_events,
       SUM(n_events = 1) AS bounce_sessions
FROM s
GROUP BY user_id, date(session_start)
ORDER BY user_id, day
"""
SQL_A = SQL_TEMPLATE.replace("{OP}", ">")
SQL_B = SQL_TEMPLATE.replace("{OP}", ">=")
SQL_WRONG_BYEVENTDAY = """
SELECT user_id, date(event_ts) AS day, COUNT(*) AS events_on_day
FROM events WHERE user_id = 2 GROUP BY user_id, date(event_ts) ORDER BY day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_a = pd.read_sql_query(SQL_A, con)
sql_b = pd.read_sql_query(SQL_B, con)
print("SQL convention A (gap > 30 min starts a new session):")
print(sql_a.to_string(index=False))
print("SQL convention B (gap >= 30 min starts a new session):")
print(sql_b.to_string(index=False))
print("user 2 events counted by event date (wrong way to date a session):")
print(pd.read_sql_query(SQL_WRONG_BYEVENTDAY, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
def sessions_pandas(events, ge):
    # pd:main
    e = events.dropna(subset=["event_ts"]).copy()
    e["event_ts"] = pd.to_datetime(e["event_ts"])
    e = e.sort_values(["user_id", "event_ts"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    limit = pd.Timedelta(minutes=30)
    new = gap.isna() | ((gap >= limit) if ge else (gap > limit))
    e["session_no"] = new.astype(int).groupby(e["user_id"]).cumsum()
    s = (e.groupby(["user_id", "session_no"])
           .agg(session_start=("event_ts", "min"), n_events=("event_ts", "size"))
           .reset_index())
    s["day"] = s["session_start"].dt.strftime("%Y-%m-%d")
    out = (s.groupby(["user_id", "day"])
             .agg(sessions=("n_events", "size"), avg_events=("n_events", "mean"),
                  bounce_sessions=("n_events", lambda x: int((x == 1).sum())))
             .round({"avg_events": 2}).reset_index())
    # pd:end
    return out
pa = sessions_pandas(events, ge=False)
pb = sessions_pandas(events, ge=True)
for sql, p in ((sql_a, pa), (sql_b, pb)):
    pd.testing.assert_frame_equal(sql.sort_values(["user_id", "day"]).reset_index(drop=True),
                                  p.sort_values(["user_id", "day"]).reset_index(drop=True), check_dtype=False)  # sorted by user_id, day
print("pandas convention A:")
print(pa.to_string(index=False))
print("pandas convention B:")
print(pb.to_string(index=False))

# julianday float arithmetic versus unixepoch integer seconds at the exact 30 minute threshold
n_bad_julian = con.execute("""
WITH RECURSIVE n(i) AS (SELECT 0 UNION ALL SELECT i + 1 FROM n WHERE i < 20000),
p AS (SELECT datetime('2020-01-01 00:00:00', '+' || (i * 7919) || ' seconds') AS a FROM n)
SELECT SUM((julianday(datetime(a, '+30 minutes')) - julianday(a)) * 1440 > 30),
       SUM((julianday(datetime(a, '+30 minutes')) - julianday(a)) * 1440 < 30),
       SUM((julianday(datetime(a, '+30 minutes')) - julianday(a)) * 1440 = 30),
       SUM(unixepoch(datetime(a, '+30 minutes')) - unixepoch(a) = 1800),
       COUNT(*)
FROM p""").fetchone()
print("20001 exact 30 minute pairs: julianday*1440 > 30, < 30, = 30; unixepoch diff = 1800; total:", n_bad_julian)
print("asserts passed")
