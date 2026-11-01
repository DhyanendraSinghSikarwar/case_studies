### Q11 ⭐⭐⭐ 🟡 Sessionization with a 30 minute timeout: events(user_id, event_ts, event_name) with ISO timestamps. Assign a session id per user with LAG(event_ts) to get the previous event time, a CASE flag for a new session (first event, or gap of more than 30 minutes) and a running SUM of the flag over (PARTITION BY user_id ORDER BY event_ts). Return session_id, session_start, session_end, event count and duration in minutes per session. Use julianday differences times 1440 in SQLite and explain why unixepoch differences are safer.
**Asked at:** Dataiku sessionization tutorial (opened; vendor tutorial, uses a 30 minute timeout with >= and no tie handling) plus search snippets of Cube, DevGenius and LinkedIn sessionization posts (not opened); guides and not candidate reports; product analytics and data scientist rounds
**Say this first (1 line):** Order each user's events by time, use `LAG` to get the previous event time, flag a row as a new session when it is the user's first event or the gap is over 30 minutes, then a running `SUM` of the flag per user is the session number; I assume "more than 30 minutes" starts a new session (exactly 30 stays in), and I measure gaps with `unixepoch`, not `julianday * 1440`.

**Schema and sample data:** twelve event rows, three users, loaded out of time order on purpose (event 12 is 09:05 for user 1 but has the highest id). User 1 has a gap of exactly 30 minutes (09:10 to 09:40). User 2 has a single event. User 3 crosses midnight and has a gap of 31 minutes (00:10 to 00:41). Event 11 has a NULL timestamp. Timestamps are ISO text `YYYY-MM-DD HH:MM:SS`, no time zone.
```sql
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
```

**SQL answer:** `SQL_MAIN` in the Code block, the `>` convention (a gap of exactly 30 minutes stays in the same session):
```sql
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
```
The `>=` convention is the same query with `>= 30` (`SQL_GE` in the Code block). Both are printed. Assumption I state out loud: gap more than 30 minutes starts a new session, so exactly 30 minutes is still the same session. The Dataiku tutorial (opened) uses `>=`; sources differ, so in an interview I ask which one the product uses.

**pandas answer:** the same logic as a function, shown once here and identical to the Code block (`strict=True` is the `>` convention, `strict=False` is `>=`):
```py
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
    
```

**Example:** user 1 sorted by time: 09:00, 09:05, 09:10, 09:40, 09:41, 11:00, 11:05.
- Gaps to the previous event: first row (no previous), 5, 5, 30, 1, 79, 5 minutes.
- Under `>`: flags 1,0,0,0,0,1,0 so running sums 1,1,1,1,1,2,2. Session 1 is 09:00 to 09:41 (5 events, 41 minutes), session 2 is 11:00 to 11:05 (2 events, 5 minutes).
- Under `>=`: the 30 minute gap also flags, so flags 1,0,0,1,0,1,0. Session 1 is 09:00 to 09:10 (3 events), session 2 is 09:40 to 09:41 (2 events), session 3 is 11:00 to 11:05. One boundary decides whether user 1 has 2 or 3 sessions.
- User 2: one event, flag 1, one session of 0 minutes. User 3: 23:50 to 00:10 is 20 minutes across midnight, still one session (a date-based session would split it); 00:41 is 31 minutes later, a new session under both conventions.
- Totals: 5 sessions under `>`, 6 under `>=`. The NULL event is dropped by `WHERE event_ts IS NOT NULL`.

**Code:** run with `python3 -I`. The asserts compare SQL and pandas for both conventions after ordering by `user_id, session_id`; durations are floats so the comparison is on values, not dtypes.
```python
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
```

**Output (my run):**
```text
SQL, new session when gap > 30 minutes (assumed):
 user_id  session_id       session_start         session_end  events  duration_min
       1           1 2024-03-01 09:00:00 2024-03-01 09:41:00       5          41.0
       1           2 2024-03-01 11:00:00 2024-03-01 11:05:00       2           5.0
       2           1 2024-03-01 10:00:00 2024-03-01 10:00:00       1           0.0
       3           1 2024-03-01 23:50:00 2024-03-02 00:10:00       2          20.0
       3           2 2024-03-02 00:41:00 2024-03-02 00:41:00       1           0.0
SQL, new session when gap >= 30 minutes:
 user_id  session_id       session_start         session_end  events  duration_min
       1           1 2024-03-01 09:00:00 2024-03-01 09:10:00       3          10.0
       1           2 2024-03-01 09:40:00 2024-03-01 09:41:00       2           1.0
       1           3 2024-03-01 11:00:00 2024-03-01 11:05:00       2           5.0
       2           1 2024-03-01 10:00:00 2024-03-01 10:00:00       1           0.0
       3           1 2024-03-01 23:50:00 2024-03-02 00:10:00       2          20.0
       3           2 2024-03-02 00:41:00 2024-03-02 00:41:00       1           0.0
sessions: gap > 30 -> 5 ; gap >= 30 -> 6
                  a                   b   julian_min  julian_gt_30  unix_min  unix_gt_30
2024-03-01 09:10:00 2024-03-01 09:40:00 30.000000224             1      30.0           0
2024-03-01 23:50:00 2024-03-02 00:20:00 30.000000224             1      30.0           0
2024-03-01 09:00:00 2024-03-01 09:30:00 30.000000224             1      30.0           0
julianday version, gap > 30: sessions = 6 (unixepoch version: 5 )
 user_id  session_id  events  duration_min
       1           1       3          10.0
       1           2       2           1.0
       1           3       2           5.0
       2           1       1           0.0
       3           1       2          20.0
       3           2       1           0.0
(20000, 13333, 0, 20000) <- rows, julianday > 30, julianday = 30, unixepoch = 1800
asserts passed
```

**Edge cases:**
- Exactly 30 minutes: 5 sessions under `>` and 6 under `>=` in my run. This is the one thing to confirm with the interviewer.
- `julianday` precision, run on this machine (SQLite 3.45.1): for the pair 09:10:00 and 09:40:00, `(julianday(b) - julianday(a)) * 1440` is `30.000000224`, so `> 30` is true and the julianday version wrongly started a new session (6 sessions instead of 5 under the `>` rule). Over 20000 pairs that were exactly 30 minutes apart, none came out as exactly 30 and 13333 were above 30. `unixepoch` differences were exactly 1800 seconds in all 20000. The cause is that `julianday` is a floating-point number of days with only about millisecond resolution at today's day numbers; this is why I use `unixepoch` (integer seconds) for thresholds, and why a julianday comparison needs `ROUND(..., 3)` at least.
- Unsorted input: the window `ORDER BY` fixes it; no pre-sort is needed. In pandas the sort is explicit.
- Single-event user: `prev_ts` is NULL, flag 1, one session with duration 0.
- NULL timestamp: filtered out first. Without the filter, `ORDER BY event_ts` puts NULLs first in SQLite and the NULL row would open a fake session; in pandas, `NaT` sorts last and `diff` gives `NaT`, which also reads as a new session.
- Midnight crossing is fine because the gap uses full timestamps, not dates.
- Duplicate timestamps: the `event_id` tie-breaker in both window clauses is explained in Q12.
- Duration here is last event minus first event, so a one-event session has duration 0; products that add a timeout tail or a minimum duration say so explicitly.

**Then explain:**
- Three steps: `LAG` to see the previous event (partitioned by user so the first event of a user has NULL), `CASE` to flag session starts, running `SUM` of the flag to number the sessions per user. Then group by user and session number for start, end, count and duration.
- `session_id` is only unique within a user; group by `(user_id, session_id)`, or build a global key such as `user_id || '-' || session_id`.
- The `OVER (PARTITION BY user_id ORDER BY ...)` running sum uses the default frame (`RANGE ... CURRENT ROW`); with the tie-breaker in the `ORDER BY` there are no peers, so it behaves like a row-by-row running total (running-total mechanics are Part 5).
- Why `unixepoch` is safer: it gives integer seconds, so a threshold of 1800 seconds is exact; `julianday` is a float and an exact 30 minute gap lands slightly above 30. `unixepoch()` is available from SQLite 3.38, and the sample runs on 3.45.1.
- pandas mapping: `groupby("user_id")["event_ts"].diff()` is `LAG`, `gap.isna() | (gap > limit)` is the flag (`isna` is the first-row case), `groupby().cumsum()` is the running `SUM`.
- Dialects, not executed here: PostgreSQL would use `event_ts - prev_ts > INTERVAL '30 minutes'` (or `EXTRACT(EPOCH FROM ...)`), MySQL `TIMESTAMPDIFF(MINUTE, prev_ts, event_ts) > 30` (note it counts whole minutes, so 30 min 59 s is 30), BigQuery `TIMESTAMP_DIFF(event_ts, prev_ts, SECOND)`. I did not run any of these.

**Follow-ups:**
- Which user-visible number changes with `>` versus `>=`? Session count and every duration near the boundary (here 5 versus 6 sessions).
- How do you also attach the session number to each event row? Keep the `s` CTE output and join or select from it; the grouped query is a summary of it.
- Sessions longer than a day or a hard cap (for example "also split after 4 hours")? That needs a second condition on the session start, which a plain running `SUM` cannot do; it needs a recursive CTE (pointer to Part 9).

**Common mistakes:**
- Flagging with `julianday(...) * 1440 > 30` and getting a spurious session at exactly 30 minutes (shown above).
- Forgetting `PARTITION BY user_id` in `LAG` or in the running `SUM`, so one user's last event is another user's previous event.
- Not flagging the first event (NULL gap compares as NULL, so the flag falls to ELSE 0 and the first session gets number 0 or merges with the wrong group).
- Grouping by `session_id` alone and merging different users' sessions.
- Using the date instead of a timestamp, which splits a session at midnight.
- Not saying which of `>` and `>=` was assumed.

### Q12 ⭐⭐⭐ 🟡 Session boundary and ties: with a 30 minute timeout, a gap of exactly 30 minutes (14:00:00 then 14:30:00) is a new session under >= and the same session under >. Show both on one table and state the rule you would confirm with the interviewer. Then show that two events with an identical event_ts for the same user make LAG order undefined, so the session flag and event order can differ between runs, and fix it with a tie-breaker (ORDER BY event_ts, event_id) in both the LAG and the running SUM.
**Asked at:** Dataiku sessionization tutorial (opened; vendor tutorial, uses a 30 minute timeout with >= and no tie handling) plus search snippets of Cube, DevGenius and LinkedIn sessionization posts (not opened); guides and not candidate reports; product analytics and data scientist rounds
**Say this first (1 line):** A gap of exactly 30 minutes is a new session under `>= 30` and the same session under `> 30`, so I state my rule up front (I assume `>`, "more than 30 minutes of inactivity", and would confirm it), and for identical timestamps I add a unique `event_id` to the `ORDER BY` of both the `LAG` and the running `SUM` so the order never depends on how the engine happened to read the rows.

**Schema and sample data:** seven rows. User 1: 14:00:00, then exactly 14:30:00, then 14:30:01 (the exact-threshold case, plus one second after it). User 2: 10:00, then two events with the identical timestamp 10:45:00 (`click`, event 5, and `buy`, event 6), then 10:50. `event_id` is a plain integer column (not the primary key) so the physical row order in the table is the insert order and I can load the same rows in two different physical orders (`SCHEMA` and `SCHEMA_REV`, the second is the reverse). The 45 minute gap before 10:45 starts a new session in both conventions, so the tie sits right at a session start.
```sql
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,1,'2024-03-01 14:00:00','a'),
 (2,1,'2024-03-01 14:30:00','b'),
 (3,1,'2024-03-01 14:30:01','c'),
 (4,2,'2024-03-01 10:00:00','open'),
 (5,2,'2024-03-01 10:45:00','click'),
 (6,2,'2024-03-01 10:45:00','buy'),
 (7,2,'2024-03-01 10:50:00','exit');
```

**SQL answer:** `SQL_MAIN` in the Code block, `>` convention with the tie-breaker in both window clauses (the `WINDOW w` clause is the same ordering the running `SUM` repeats):
```sql
WITH e AS (
  SELECT user_id, event_id, event_ts, event_name,
         LAG(event_ts) OVER w AS prev_ts,
         LAG(event_name) OVER w AS prev_name
  FROM events
  WINDOW w AS (PARTITION BY user_id ORDER BY event_ts, event_id)
), f AS (
  SELECT *, CASE WHEN prev_ts IS NULL
                   OR (unixepoch(event_ts) - unixepoch(prev_ts)) > 1800
                 THEN 1 ELSE 0 END AS new_session
  FROM e
)
SELECT user_id, event_id, event_name, prev_name, new_session,
       SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_ts, event_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_id
FROM f
ORDER BY user_id, event_ts, event_id
```
`SQL_GE` is the same text with `>= 1800` in place of `> 1800` (seconds; I use `unixepoch` for the reason given in Q11). `SQL_NOTIE` is the same text with the `event_id` removed from every `ORDER BY` of the windows, to show the failure.

**pandas answer:** same logic, shown once here and identical to the Code block:
```py
    e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
    e = e.sort_values(["user_id", "event_ts", "event_id"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    limit = pd.Timedelta(minutes=30)
    new = gap.isna() | ((gap > limit) if strict else (gap >= limit))
    e["session_id"] = new.astype(int).groupby(e["user_id"]).cumsum()
    
```

**Example:** user 1.
- 14:00:00 is the first event: flag 1, session 1.
- 14:30:00 is 1800 seconds after 14:00:00. Under `>` (1800 > 1800 is false): flag 0, session 1. Under `>=`: flag 1, session 2.
- 14:30:01 is one second later: flag 0 in both, so it joins whichever session the 14:30:00 event is in. Result: events 1,2,3 are sessions 1,1,1 under `>` and 1,2,2 under `>=`.
- User 2: 10:00 is session 1. The two 10:45:00 events are 45 minutes after it, so the first of the two in the order gets flag 1 and the second has a gap of 0, flag 0. With the tie-breaker the order is event 5 (`click`) then event 6 (`buy`); the sessions are 1, 2, 2, 2.

**Code:** run with `python3 -I`. SQL and pandas are compared for both conventions on the rows ordered by `user_id, event_ts, event_id`; the tie runs compare the same query on the two physical insert orders.
```python
# Q12: session boundary (> vs >=) and ties in event_ts (tie-breaker event_id)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,1,'2024-03-01 14:00:00','a'),
 (2,1,'2024-03-01 14:30:00','b'),
 (3,1,'2024-03-01 14:30:01','c'),
 (4,2,'2024-03-01 10:00:00','open'),
 (5,2,'2024-03-01 10:45:00','click'),
 (6,2,'2024-03-01 10:45:00','buy'),
 (7,2,'2024-03-01 10:50:00','exit');
"""
# the same rows inserted in the opposite physical order (event_id values unchanged)
SCHEMA_REV = """
CREATE TABLE events(event_id INTEGER, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (7,2,'2024-03-01 10:50:00','exit'),
 (6,2,'2024-03-01 10:45:00','buy'),
 (5,2,'2024-03-01 10:45:00','click'),
 (4,2,'2024-03-01 10:00:00','open'),
 (3,1,'2024-03-01 14:30:01','c'),
 (2,1,'2024-03-01 14:30:00','b'),
 (1,1,'2024-03-01 14:00:00','a');
"""
SQL_MAIN = """
WITH e AS (
  SELECT user_id, event_id, event_ts, event_name,
         LAG(event_ts) OVER w AS prev_ts,
         LAG(event_name) OVER w AS prev_name
  FROM events
  WINDOW w AS (PARTITION BY user_id ORDER BY event_ts, event_id)
), f AS (
  SELECT *, CASE WHEN prev_ts IS NULL
                   OR (unixepoch(event_ts) - unixepoch(prev_ts)) > 1800
                 THEN 1 ELSE 0 END AS new_session
  FROM e
)
SELECT user_id, event_id, event_name, prev_name, new_session,
       SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_ts, event_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS session_id
FROM f
ORDER BY user_id, event_ts, event_id
"""
SQL_GE = SQL_MAIN.replace("> 1800", ">= 1800")
assert SQL_GE != SQL_MAIN
# no tie-breaker: ORDER BY event_ts only (in the LAG window and in the running SUM)
SQL_NOTIE = SQL_MAIN.replace("ORDER BY event_ts, event_id", "ORDER BY event_ts")
assert "ORDER BY event_ts, event_id" not in SQL_NOTIE
# the final ORDER BY must not hide the problem: order the printout by the window result itself
SQL_NOTIE = SQL_NOTIE.replace("ORDER BY user_id, event_ts, event_id", "ORDER BY user_id, event_ts")

def run(schema, sql):
    c = sqlite3.connect(":memory:")
    c.executescript(schema)
    return pd.read_sql_query(sql, c)

print("== boundary: user 1 has a gap of exactly 30:00 (14:00 -> 14:30)")
gt = run(SCHEMA, SQL_MAIN)
ge = run(SCHEMA, SQL_GE)
u1 = pd.DataFrame({"event_id": gt[gt.user_id == 1].event_id.values,
                   "session_gt": gt[gt.user_id == 1].session_id.values,
                   "session_ge": ge[ge.user_id == 1].session_id.values})
print(u1.to_string(index=False))

print("== ties, with the tie-breaker (physical insert order A and B)")
a = run(SCHEMA, SQL_MAIN)
b = run(SCHEMA_REV, SQL_MAIN)
print(a[a.user_id == 2].to_string(index=False))
assert a.equals(b)
print("same result for both insert orders: True")

print("== ties, ORDER BY event_ts only (insert order A, then B)")
na = run(SCHEMA, SQL_NOTIE)
nb = run(SCHEMA_REV, SQL_NOTIE)
print(na[na.user_id == 2].to_string(index=False))
print(nb[nb.user_id == 2].to_string(index=False))
print("same result for both insert orders:", na.equals(nb))
print("session ids per row identical in both?", (na.session_id.values == nb.session_id.values).all())

# pandas: sort with the tie-breaker, then diff / cumsum
events = run(SCHEMA, "SELECT * FROM events")
def sessions(events, strict):
    # pd:main
    e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
    e = e.sort_values(["user_id", "event_ts", "event_id"], kind="stable")
    gap = e.groupby("user_id")["event_ts"].diff()
    limit = pd.Timedelta(minutes=30)
    new = gap.isna() | ((gap > limit) if strict else (gap >= limit))
    e["session_id"] = new.astype(int).groupby(e["user_id"]).cumsum()
    # pd:end
    return e[["user_id", "event_id", "session_id"]].reset_index(drop=True)

for strict, sql_df in ((True, gt), (False, ge)):
    p = sessions(events, strict)
    s = sql_df[["user_id", "event_id", "session_id"]]
    pd.testing.assert_frame_equal(p, s, check_dtype=False)  # both ordered by user_id, event_ts, event_id
print("pandas matches SQL for > and >=")

# pandas without the tie-breaker: sort_values(['user_id','event_ts']) on the reversed physical order
rev = run(SCHEMA_REV, "SELECT * FROM events").assign(event_ts=lambda d: pd.to_datetime(d["event_ts"]))
fwd = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
o1 = fwd.sort_values(["user_id", "event_ts"])["event_id"].tolist()
o2 = rev.sort_values(["user_id", "event_ts"])["event_id"].tolist()
print("pandas order of event_ids, no tie-breaker, insert order A:", o1)
print("pandas order of event_ids, no tie-breaker, insert order B:", o2)
print("asserts passed")
```

**Output (my run):**
```text
== boundary: user 1 has a gap of exactly 30:00 (14:00 -> 14:30)
 event_id  session_gt  session_ge
        1           1           1
        2           1           2
        3           1           2
== ties, with the tie-breaker (physical insert order A and B)
 user_id  event_id event_name prev_name  new_session  session_id
       2         4       open       NaN            1           1
       2         5      click      open            1           2
       2         6        buy     click            0           2
       2         7       exit       buy            0           2
same result for both insert orders: True
== ties, ORDER BY event_ts only (insert order A, then B)
 user_id  event_id event_name prev_name  new_session  session_id
       2         4       open       NaN            1           1
       2         5      click      open            1           2
       2         6        buy     click            0           2
       2         7       exit       buy            0           2
 user_id  event_id event_name prev_name  new_session  session_id
       2         4       open       NaN            1           1
       2         6        buy      open            1           2
       2         5      click       buy            0           2
       2         7       exit     click            0           2
same result for both insert orders: False
session ids per row identical in both? True
pandas matches SQL for > and >=
pandas order of event_ids, no tie-breaker, insert order A: [1, 2, 3, 4, 5, 6, 7]
pandas order of event_ids, no tie-breaker, insert order B: [1, 2, 3, 4, 6, 5, 7]
asserts passed
```

**Edge cases:**
- Exact threshold: event 2 is session 1 under `>` and session 2 under `>=` in my run, and event 3 (one second later) follows event 2 in both. Rule to confirm with the interviewer: is the timeout "inactive for more than 30 minutes" (`>`) or "30 minutes or more" (`>=`)? The Dataiku tutorial uses `>=`; other write-ups use `>`. I assume `>` and say so.
- Ties, honest result from my run: with `ORDER BY event_ts` only, the two physical insert orders gave different row orders for the tied events. In order A the sequence was click (5) then buy (6); in order B it was buy (6) then click (5), and `prev_name`, the row that carries `new_session = 1`, and any "first event of the session" or "event number" column changed with it. The session ids per row were identical in both runs, because the tied rows have the same timestamp and therefore the same gap from the earlier event; only which row of the pair carries the flag moves. So the claim "session numbers change" was not what I observed; what changed is every per-event output. With the tie-breaker the result was equal in both insert orders (`True`).
- The default frame of a running `SUM ... ORDER BY event_ts` is `RANGE`, which treats tied rows as peers and adds them together. That hides the difference in session ids above, but `ROW_NUMBER`, `LAG`, `FIRST_VALUE` and `ROWS` frames do not hide it. I wrote `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` in `SQL_MAIN` so the frame is explicit.
- Order of the tied events is arbitrary only in the sense of "not defined by the SQL"; in this SQLite run it followed the physical row order, other engines or plans may differ (I did not run them).
- pandas: `sort_values(["user_id", "event_ts"])` also left the tied events in their input order (order A gave 5 then 6, order B gave 6 then 5). Add `event_id` to the sort keys. I also pass `kind="stable"`; for a single sort key the default kind is quicksort, which in my probe on 2000 rows with many ties was not stable, while a multi-key sort was stable in my probe.
- Tie-breaker must be unique. If `event_id` is itself duplicated, the ties return.
- Single-event users and NULL timestamps behave as in Q11.

**Then explain:**
- Rule first, code second: write the boundary operator as a constant (here 1800 seconds) and say which side the equal case falls on.
- For `LAG` to be deterministic the window `ORDER BY` must give a total order. Timestamps are not unique, so append a unique column. The same total order must be used by every window in the query, otherwise the `LAG` row and the running `SUM` row sequences disagree.
- The tie-breaker does not decide whether `click` really came before `buy`; it only makes the result repeatable. If the true order matters, you need a sequence number from the source system.
- `WINDOW w AS (...)` names a window so the `LAG` calls share one definition (SQLite 3.28 and later). The final `SUM` repeats the ordering because it also needs the frame.
- Dialects, not executed here: PostgreSQL and MySQL 8 accept the same window syntax; MySQL 5.7 has no window functions at all.

**Follow-ups:**
- Which convention would you choose for a 30 minute product session? Whatever the product's analytics tool uses; many tools say "30 minutes of inactivity", which reads like `>`, but I would confirm.
- What if two tied events belong to different users? No effect, the windows are partitioned by user.
- What if the tie-breaker is missing and the data has no id? Use all columns that make the row unique, or accept that per-event outputs are not repeatable and only report session-level aggregates (counts and first/last timestamps, which were stable here).

**Common mistakes:**
- Using `>=` or `>` without saying so.
- A tie-breaker in only one of the windows.
- Relying on the default frame to make ties safe, then adding `ROW_NUMBER` or `FIRST_VALUE` later and getting unrepeatable output.
- Claiming the order of ties is random: in this run it followed the physical order, which is stable only by accident.
- Sorting a pandas frame by timestamp only and trusting the order of tied rows.

### Q13 ⭐⭐⭐ 🟡 Consecutive same-status runs (run-length encoding in SQL): status_log(entity_id, ts, status) with statuses such as 'ok' and 'down' that repeat. Return each run as entity_id, status, run_start, run_end, rows using LAG to flag a change (status <> prev_status, with the first row as a change) and a running SUM of the flag. Then show the partitioned ROW_NUMBER difference method (ROW_NUMBER over entity ordered by ts minus ROW_NUMBER over entity and status ordered by ts) and explain why the two methods agree.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** A run is a maximal stretch of consecutive rows with the same status; flag every row whose status differs from the previous row of the same entity (the first row always counts as a change), take a running `SUM` of the flag as the run number, then group to get start, end and row count; the alternative is two `ROW_NUMBER`s whose difference is constant inside a run.

**Schema and sample data:** eleven rows, inserted out of time order for entity 1 (00:05 before 00:00). Entity 1: ok, ok, down, down, down, ok. Entity 2: a single row. Entity 3: ok, NULL, NULL, ok (NULL status is a real case in logs). Timestamps are ISO text.
```sql
CREATE TABLE status_log(entity_id INTEGER, ts TEXT, status TEXT);
INSERT INTO status_log VALUES
 (1,'2024-03-01 00:05:00','ok'),
 (1,'2024-03-01 00:00:00','ok'),
 (1,'2024-03-01 00:10:00','down'),
 (1,'2024-03-01 00:15:00','down'),
 (1,'2024-03-01 00:20:00','down'),
 (1,'2024-03-01 00:25:00','ok'),
 (2,'2024-03-01 00:00:00','down'),
 (3,'2024-03-01 00:00:00','ok'),
 (3,'2024-03-01 00:05:00',NULL),
 (3,'2024-03-01 00:10:00',NULL),
 (3,'2024-03-01 00:15:00','ok');
```

**SQL answer:** `SQL_MAIN` in the Code block (LAG flag plus running SUM). `IS NOT` is the NULL-safe "different from" in SQLite:
```sql
WITH f AS (
  SELECT entity_id, ts, status,
         CASE WHEN LAG(ts) OVER w IS NULL OR status IS NOT LAG(status) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM status_log
  WINDOW w AS (PARTITION BY entity_id ORDER BY ts)
), g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY entity_id ORDER BY ts) AS run_id
  FROM f
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM g
GROUP BY entity_id, run_id, status
ORDER BY entity_id, run_start
```
The row-number difference method, `SQL_RN` in the Code block:
```sql
WITH r AS (
  SELECT entity_id, ts, status,
         ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
       - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
  FROM status_log
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM r
GROUP BY entity_id, status, grp
ORDER BY entity_id, run_start
```
`SQL_WRONG` is `SQL_MAIN` with `<>` instead of `IS NOT`, to show the NULL trap.

**pandas answer:** the same flag-and-cumsum logic, shown once here and identical to the Code block. The first-row flag and the NULL-safe comparison are explicit because `NaN != NaN` is `True` in pandas:
```py
d = log.sort_values(["entity_id", "ts"], kind="stable").copy()
prev = d.groupby("entity_id")["status"].shift()
first = d.groupby("entity_id").cumcount() == 0
same = (d["status"] == prev) | (d["status"].isna() & prev.isna())
d["run_id"] = (first | ~same).astype(int).groupby(d["entity_id"]).cumsum()
runs = (d.groupby(["entity_id", "run_id"], as_index=False, dropna=False)
          .agg(status=("status", "first"), run_start=("ts", "min"), run_end=("ts", "max"),
               n_rows=("ts", "size")))
runs = runs[["entity_id", "status", "run_start", "run_end", "n_rows"]]
```

**Example:** entity 1 sorted: ok 00:00, ok 00:05, down 00:10, down 00:15, down 00:20, ok 00:25.
- Flags: 1 (first), 0 (same), 1 (ok to down), 0, 0, 1 (down to ok). Running sum: 1,1,2,2,2,3. Runs: ok 00:00 to 00:05 (2 rows), down 00:10 to 00:20 (3 rows), ok 00:25 (1 row).
- Row-number method: `rn_all` is 1..6; `rn_status` counts inside each status: ok gets 1,2 then 3 for the last row, down gets 1,2,3. The difference `rn_all - rn_status` is 0,0,2,2,2,3. Inside a run both counters go up by one per row, so the difference cannot change; when a different status interrupts, `rn_all` jumps ahead while this status's own counter does not, so the difference becomes a new number.
- Why the final ok (difference 3) is not merged with the first ok (difference 0): the two oks have different differences because three rows of other status sit between them.
- Entity 3: ok, NULL x2, ok gives three runs: ok, NULL (2 rows), ok.

**Code:** run with `python3 -I`. The asserts compare the two SQL methods with each other, pandas with SQL (rows ordered by `entity_id, run_start`), and an `itertools.groupby` run-length cross-check for entity 1.
```python
# Q13: consecutive same-status runs: LAG flag + running SUM, ROW_NUMBER difference, pandas, itertools.groupby
import sqlite3
import itertools
import pandas as pd

SCHEMA = """
CREATE TABLE status_log(entity_id INTEGER, ts TEXT, status TEXT);
INSERT INTO status_log VALUES
 (1,'2024-03-01 00:05:00','ok'),
 (1,'2024-03-01 00:00:00','ok'),
 (1,'2024-03-01 00:10:00','down'),
 (1,'2024-03-01 00:15:00','down'),
 (1,'2024-03-01 00:20:00','down'),
 (1,'2024-03-01 00:25:00','ok'),
 (2,'2024-03-01 00:00:00','down'),
 (3,'2024-03-01 00:00:00','ok'),
 (3,'2024-03-01 00:05:00',NULL),
 (3,'2024-03-01 00:10:00',NULL),
 (3,'2024-03-01 00:15:00','ok');
"""
SQL_MAIN = """
WITH f AS (
  SELECT entity_id, ts, status,
         CASE WHEN LAG(ts) OVER w IS NULL OR status IS NOT LAG(status) OVER w
              THEN 1 ELSE 0 END AS chg
  FROM status_log
  WINDOW w AS (PARTITION BY entity_id ORDER BY ts)
), g AS (
  SELECT *, SUM(chg) OVER (PARTITION BY entity_id ORDER BY ts) AS run_id
  FROM f
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM g
GROUP BY entity_id, run_id, status
ORDER BY entity_id, run_start
"""
SQL_RN = """
WITH r AS (
  SELECT entity_id, ts, status,
         ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
       - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
  FROM status_log
)
SELECT entity_id, status, MIN(ts) AS run_start, MAX(ts) AS run_end, COUNT(*) AS n_rows
FROM r
GROUP BY entity_id, status, grp
ORDER BY entity_id, run_start
"""
# wrong: <> instead of IS NOT (NULL comparison is NULL, so CASE falls to ELSE 0)
SQL_WRONG = SQL_MAIN.replace("status IS NOT LAG(status) OVER w", "status <> LAG(status) OVER w")
assert SQL_WRONG != SQL_MAIN
SQL_GRP = """
SELECT entity_id, ts, status,
       ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts) AS rn_all,
       ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS rn_status,
       ROW_NUMBER() OVER (PARTITION BY entity_id ORDER BY ts)
     - ROW_NUMBER() OVER (PARTITION BY entity_id, status ORDER BY ts) AS grp
FROM status_log WHERE entity_id = 1 ORDER BY ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_RN, con)
w = pd.read_sql_query(SQL_WRONG, con)
print("LAG + running SUM:"); print(a.to_string(index=False))
print("ROW_NUMBER difference, entity 1 detail:"); print(pd.read_sql_query(SQL_GRP, con).to_string(index=False))
pd.testing.assert_frame_equal(a, b)
print("two SQL methods equal (ordered by entity_id, run_start): True")
print("wrong version with <> (NULL status rows vanish from the flag):"); print(w.to_string(index=False))

log = pd.read_sql_query("SELECT * FROM status_log", con)
# pd:main
d = log.sort_values(["entity_id", "ts"], kind="stable").copy()
prev = d.groupby("entity_id")["status"].shift()
first = d.groupby("entity_id").cumcount() == 0
same = (d["status"] == prev) | (d["status"].isna() & prev.isna())
d["run_id"] = (first | ~same).astype(int).groupby(d["entity_id"]).cumsum()
runs = (d.groupby(["entity_id", "run_id"], as_index=False, dropna=False)
          .agg(status=("status", "first"), run_start=("ts", "min"), run_end=("ts", "max"),
               n_rows=("ts", "size")))
runs = runs[["entity_id", "status", "run_start", "run_end", "n_rows"]]
# pd:end
pd.testing.assert_frame_equal(runs.reset_index(drop=True), a.assign(status=a["status"]), check_dtype=False)
print("pandas equals SQL (ordered by entity_id, run_start): True")
naive = (d["status"] != prev) | first
print("naive pandas (s != s.shift()) runs for entity 3:",
      int(naive[d.entity_id == 3].sum()), "(correct: 3 runs, NaN != NaN is True so each NULL row is its own run)")

# itertools.groupby run lengths for entity 1, as a cross-check
e1 = d[d.entity_id == 1]["status"].tolist()
ig = [(k, len(list(g))) for k, g in itertools.groupby(e1)]
print("itertools.groupby entity 1:", ig)
assert ig == list(zip(a[a.entity_id == 1].status, a[a.entity_id == 1].n_rows))
# duplicated ts in the same entity changes the answer unless a tie-breaker exists: show the guard
con.execute("INSERT INTO status_log VALUES (2,'2024-03-01 00:00:00','ok')")
dup = pd.read_sql_query("SELECT entity_id, ts, COUNT(*) c FROM status_log GROUP BY entity_id, ts HAVING c > 1", con)
print("duplicate (entity_id, ts) keys after inserting one extra row:"); print(dup.to_string(index=False))
d2 = pd.read_sql_query(SQL_MAIN, con)
r2 = pd.read_sql_query(SQL_RN, con)
print("entity 2 after the tied row, LAG method:"); print(d2[d2.entity_id == 2].to_string(index=False))
print("entity 2 after the tied row, ROW_NUMBER method:"); print(r2[r2.entity_id == 2].to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
LAG + running SUM:
 entity_id status           run_start             run_end  n_rows
         1     ok 2024-03-01 00:00:00 2024-03-01 00:05:00       2
         1   down 2024-03-01 00:10:00 2024-03-01 00:20:00       3
         1     ok 2024-03-01 00:25:00 2024-03-01 00:25:00       1
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         3     ok 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         3    NaN 2024-03-01 00:05:00 2024-03-01 00:10:00       2
         3     ok 2024-03-01 00:15:00 2024-03-01 00:15:00       1
ROW_NUMBER difference, entity 1 detail:
 entity_id                  ts status  rn_all  rn_status  grp
         1 2024-03-01 00:00:00     ok       1          1    0
         1 2024-03-01 00:05:00     ok       2          2    0
         1 2024-03-01 00:10:00   down       3          1    2
         1 2024-03-01 00:15:00   down       4          2    2
         1 2024-03-01 00:20:00   down       5          3    2
         1 2024-03-01 00:25:00     ok       6          3    3
two SQL methods equal (ordered by entity_id, run_start): True
wrong version with <> (NULL status rows vanish from the flag):
 entity_id status           run_start             run_end  n_rows
         1     ok 2024-03-01 00:00:00 2024-03-01 00:05:00       2
         1   down 2024-03-01 00:10:00 2024-03-01 00:20:00       3
         1     ok 2024-03-01 00:25:00 2024-03-01 00:25:00       1
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         3     ok 2024-03-01 00:00:00 2024-03-01 00:15:00       2
         3    NaN 2024-03-01 00:05:00 2024-03-01 00:10:00       2
pandas equals SQL (ordered by entity_id, run_start): True
naive pandas (s != s.shift()) runs for entity 3: 4 (correct: 3 runs, NaN != NaN is True so each NULL row is its own run)
itertools.groupby entity 1: [('ok', 2), ('down', 3), ('ok', 1)]
duplicate (entity_id, ts) keys after inserting one extra row:
 entity_id                  ts  c
         2 2024-03-01 00:00:00  2
entity 2 after the tied row, LAG method:
 entity_id status           run_start             run_end  n_rows
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         2     ok 2024-03-01 00:00:00 2024-03-01 00:00:00       1
entity 2 after the tied row, ROW_NUMBER method:
 entity_id status           run_start             run_end  n_rows
         2   down 2024-03-01 00:00:00 2024-03-01 00:00:00       1
         2     ok 2024-03-01 00:00:00 2024-03-01 00:00:00       1
asserts passed
```

**Edge cases:**
- NULL status: with `status <> LAG(status)` the comparison is NULL when either side is NULL, so the `CASE` falls to `ELSE 0`. In my run entity 3 then collapsed to the wrong result (ok with 2 rows from 00:00 to 00:15, plus the NULL run), because the NULL rows never started a run and the later ok never started one either. With `IS NOT` the result is three runs.
- pandas: `s != s.shift()` treats every NaN as different from every other NaN (`NaN != NaN` is `True`), so the naive version made entity 3 four runs (each NULL row on its own) instead of three; and `groupby` drops NaN keys by default, so I pass `dropna=False`. My code builds the "same" test with `isna()` on both sides.
- First row of each entity: `LAG` gives NULL; I flag with `LAG(ts) IS NULL`, which is true only for the first row (a NULL `status` on the first row would otherwise be ambiguous). In pandas the first row is `cumcount() == 0`, because `shift()` also gives NaN on the first row.
- Single-row entity (entity 2): one run, start equals end, one row.
- Unsorted input: handled by the window `ORDER BY` and the pandas `sort_values`.
- Duplicate timestamps for the same entity: after inserting `(2, 00:00:00, 'ok')` next to the existing `down` at the same timestamp, both SQL methods returned two one-row runs for entity 2 in this run, but which of the two comes first is not defined by the SQL; add a unique tie-breaker column to every `ORDER BY` (Q12).
- Big gaps in time do not matter here; a run is about consecutive rows, not consecutive time. If a gap in time must also break a run, add that condition to the flag.
- The row-number difference works only because the ordering is a total order; both methods break with ties for the same reason.

**Then explain:**
- Method 1, flag and running sum: easiest to extend (add "or gap over N minutes" to the flag). Needs `LAG`, a `CASE`, a running `SUM` and a `GROUP BY`.
- Method 2, row-number difference: no `LAG`, no `CASE`, and NULL status works without a special case because `PARTITION BY` puts NULLs in one partition. The difference number itself has no meaning and is only unique inside an `(entity, status)` pair, so group by `(entity_id, status, grp)`; in `SQL_RN` grouping by `grp` alone would merge an ok run and a down run that happen to share the same difference.
- Why they agree: both are constants that change exactly when a run changes. Method 1 counts the number of starts so far; method 2 is `rn_all - rn_status`, and inside one run both advance together.
- Run length in pandas is `groupby(run_id).size()`, in plain Python `itertools.groupby` (shown for entity 1 and equal to the SQL).
- Dialects, not executed here: `IS DISTINCT FROM` is the standard spelling (it also ran on SQLite 3.45.1 in the Wave A probe, though this answer uses `IS NOT`; PostgreSQL support is from memory, not executed); MySQL uses `<=>` for NULL-safe equality; the row-number method needs window functions, so MySQL 5.7 cannot run either method.

**Follow-ups:**
- Only the longest `down` run per entity? Take `MAX(n_rows)` from the grouped result where `status = 'down'`, or rank with `ROW_NUMBER` (ranking itself is Part 4).
- Remove the repeated statuses and keep only the changes? Keep rows where the flag is 1 (state-change detection).
- Time spent in each run? `run_end` minus `run_start` gives the span between first and last row; adding the next run's start gives the full duration.

**Common mistakes:**
- `<>` with NULLs (shown above).
- Forgetting to partition by entity, so a run leaks across entities.
- Grouping only by `grp` in the row-number method, or only by `run_id` and forgetting that `status` has to be selected or grouped.
- Using `s != s.shift()` in pandas on data with NaN.
- Assuming the data is already sorted.

### Q14 ⭐⭐⭐ 🟡 pandas streaks per user: translate the date-minus-ROW_NUMBER streak query to pandas. logins(user_id, login_date) as a DataFrame with duplicates and unsorted rows. Show drop_duplicates and sort_values, then two keys: (date.diff().dt.days != 1).cumsum() per user via groupby, and day number minus cumcount as the island key. Return user_id, streak_start, streak_end, streak_days and assert the frame equals the SQL result (same rows, order stated). Explain why a global diff() without the groupby leaks a streak across users.
**Asked at:** pandas Series.shift reference (opened) and search snippets of Stack Overflow and Towards Data Science run-grouping answers ((s != s.shift()).cumsum(), diff().ne(0).cumsum(); not opened); documentation and guides, not candidate reports; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Deduplicate and sort the logins, then give every row a streak key that is constant inside a streak and different between streaks, and group by `(user_id, key)`; the two keys are "cumulative sum of (gap to the previous login of the same user is not 1 day)" and "day number minus the row's position within the user".

**Schema and sample data:** twelve rows, four users, deliberately messy: user 1 is unsorted and has a duplicate login on 03-02 (distinct days 1, 2, 3 and 5 March), user 2 has a NULL date and last logs in on 03-10 after 03-06 and 03-07, user 3 has a single login, user 4 has two consecutive days. User 1's last login (03-05) is one day before user 2's first login (03-06), on purpose, for the leak demonstration. Dates are ISO text.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-05'),
 (2,'2024-03-07'),(2,'2024-03-06'),(2,'2024-03-10'),(2,NULL),
 (3,'2024-03-09'),
 (4,'2024-03-04'),(4,'2024-03-05');
```

**SQL answer:** `SQL_MAIN` in the Code block, the date-minus-`ROW_NUMBER` reference (dedupe with `DISTINCT` first, then subtract the position in days). Position within a user's sorted distinct dates is constant against the date on a streak, so `date - rn` is the same for the whole streak:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r
GROUP BY user_id, grp
ORDER BY user_id, streak_start
```
Streak length is `COUNT(*)` of distinct days; counting rows without the `DISTINCT` would inflate user 1's first streak to 4.

**pandas answer:** shown once here and identical to the Code block. `key1` is the diff approach, `key2` the island (day number minus `cumcount`) approach:
```py
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
# key 1: a new streak starts when the gap to the previous login of the SAME user is not 1 day
gap_days = d.groupby("user_id")["login_date"].diff().dt.days
d["key1"] = (gap_days != 1).groupby(d["user_id"]).cumsum()
# key 2: day number minus position inside the user's list is constant on a streak
daynum = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days
d["key2"] = daynum - d.groupby("user_id").cumcount()
res1 = d.groupby(["user_id", "key1"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
res2 = d.groupby(["user_id", "key2"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
```

**Example:** user 1 after dedupe and sort: 03-01, 03-02, 03-03, 03-05.
- Key 1: gaps to the previous login are NaT (first row), 1, 1, 2 days; `gap != 1` is True, False, False, True; the per-user cumulative sum is 1,1,1,2. Streaks: 03-01 to 03-03 (3 days) and 03-05 (1 day).
- Key 2: day numbers are `d, d+1, d+2, d+4`; `cumcount` is 0,1,2,3; the difference is `d, d, d, d+1`: the first three are equal, the fourth differs. Same two streaks.
- User 2: 03-06, 03-07, 03-10 gives 2 days and 1 day (the NULL row is dropped first). User 3: one streak of 1 day. User 4: one streak of 2 days (03-04, 03-05).
- Total: 6 streaks.

**Code:** run with `python3 -I`. Both pandas keys are asserted equal to the SQL result after ordering by `user_id, streak_start`; dates are compared as ISO text.
```python
# Q14: pandas streaks per user: translate date-minus-ROW_NUMBER to pandas, two keys, global diff leak
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-05'),
 (2,'2024-03-07'),(2,'2024-03-06'),(2,'2024-03-10'),(2,NULL),
 (3,'2024-03-09'),
 (4,'2024-03-04'),(4,'2024-03-05');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r
GROUP BY user_id, grp
ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_MAIN, con)
print("SQL streaks:"); print(sql_res.to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)

# pd:main
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
# key 1: a new streak starts when the gap to the previous login of the SAME user is not 1 day
gap_days = d.groupby("user_id")["login_date"].diff().dt.days
d["key1"] = (gap_days != 1).groupby(d["user_id"]).cumsum()
# key 2: day number minus position inside the user's list is constant on a streak
daynum = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days
d["key2"] = daynum - d.groupby("user_id").cumcount()
res1 = d.groupby(["user_id", "key1"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
res2 = d.groupby(["user_id", "key2"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
# pd:end
def fmt(r):
    r = r[["user_id", "streak_start", "streak_end", "streak_days"]].copy()
    for c in ("streak_start", "streak_end"):
        r[c] = r[c].dt.strftime("%Y-%m-%d")
    return r.sort_values(["user_id", "streak_start"]).reset_index(drop=True)
p1, p2 = fmt(res1), fmt(res2)
print("pandas key1 (groupby diff):"); print(p1.to_string(index=False))
pd.testing.assert_frame_equal(p1, sql_res, check_dtype=False)
pd.testing.assert_frame_equal(p2, sql_res, check_dtype=False)  # rows ordered by user_id, streak_start
print("both pandas keys equal the SQL result (ordered by user_id, streak_start): True")
print("gap_days dtype:", gap_days.dtype, "| first values:", gap_days.head(4).tolist())
print("NaN != 1 ->", float("nan") != 1)

# wrong: global diff (no groupby) and grouping on the key alone
gd = d["login_date"].diff().dt.days
d["wrong_key"] = (gd != 1).cumsum()
leak_alone = d.groupby("wrong_key", as_index=False).agg(
    user_id=("user_id", "first"), streak_start=("login_date", "min"),
    streak_end=("login_date", "max"), streak_days=("login_date", "size"), users=("user_id", "nunique"))
print("global diff, grouped by the key only (users column = distinct users inside the group):")
print(leak_alone.assign(streak_start=leak_alone.streak_start.dt.strftime("%Y-%m-%d"),
                        streak_end=leak_alone.streak_end.dt.strftime("%Y-%m-%d"))
      .drop(columns="wrong_key").to_string(index=False))
same_by_luck = d.groupby(["user_id", "wrong_key"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
print("global diff but grouped by (user_id, key) equals the right answer:",
      fmt(same_by_luck).equals(sql_res))

print("asserts passed")
```

**Output (my run):**
```text
SQL streaks:
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-03            3
       1   2024-03-05 2024-03-05            1
       2   2024-03-06 2024-03-07            2
       2   2024-03-10 2024-03-10            1
       3   2024-03-09 2024-03-09            1
       4   2024-03-04 2024-03-05            2
pandas key1 (groupby diff):
 user_id streak_start streak_end  streak_days
       1   2024-03-01 2024-03-03            3
       1   2024-03-05 2024-03-05            1
       2   2024-03-06 2024-03-07            2
       2   2024-03-10 2024-03-10            1
       3   2024-03-09 2024-03-09            1
       4   2024-03-04 2024-03-05            2
both pandas keys equal the SQL result (ordered by user_id, streak_start): True
gap_days dtype: float64 | first values: [nan, 1.0, 1.0, 2.0]
NaN != 1 -> True
global diff, grouped by the key only (users column = distinct users inside the group):
 user_id streak_start streak_end  streak_days  users
       1   2024-03-01 2024-03-03            3      1
       1   2024-03-05 2024-03-07            3      2
       2   2024-03-10 2024-03-10            1      1
       3   2024-03-09 2024-03-09            1      1
       4   2024-03-04 2024-03-05            2      1
global diff but grouped by (user_id, key) equals the right answer: True
asserts passed
```

**Edge cases:**
- Duplicates: `drop_duplicates()` before the key, otherwise `cumcount` counts the repeated row and breaks the day-number-minus-position key, and the diff approach sees a gap of 0 days which is not 1, so a duplicate would also start a new streak.
- Unsorted input: sort before `diff` and `cumcount`; neither knows the order unless you sort. `groupby(...).diff()` works on the existing row order.
- Single-row user (user 3): `diff` is NaT for the first row, so `.dt.days` is NaN, and `NaN != 1` is `True` in my run, which correctly starts a streak of length 1.
- Dtype note from my run: `.dt.days` on a diff column with NaT is `float64` (NaN is a float), not integer; comparing it with 1 is fine. The shift/diff family upcasts integer data to float for the same reason (a `shift` of an integer column gave `float64` in my probe, and `fill_value=0` kept it integer).
- NULL date: `to_datetime` would give `NaT`, which sorts last and creates a bogus row; I drop the NULL rows before everything else, as the SQL does.
- Empty input: not run through this pipeline here; check it before relying on it.
- Timestamps instead of dates: normalize first (`dt.normalize()` in pandas, `date()` in SQL), otherwise two logins on the same day with different times are two rows.
- Time zones and daylight saving: a date column has none; timestamps in different zones need converting to the user's local date first (SQLite has no zones, so this is a note, not something I ran).

**Then explain:**
- Why the diff key needs `groupby`: without it, `login_date.diff()` also compares the first row of user 2 with the last row of user 1. In my data user 1's last login is 03-05 and user 2's first is 03-06, a gap of 1 day, so the first row of user 2 is not flagged as a streak start. If you then group by the key alone, user 2's first streak (03-06 and 03-07) glues onto user 1's streak 03-05: one bogus group of 3 days attributed to user 1 with 2 users inside (see the `users` column). That is the leak.
- Honest nuance, run: if you group by `(user_id, key)` the leak is hidden, because the user column separates the groups again; the global-diff frame still matched the correct answer in my run (`True`). So the global diff is a bug that is silent when you group by user and wrong when the key stands alone (a window or `transform` on the key, a `nunique` of the key, a merge on the key).
- The diff approach needs the per-user first row flagged (NaN gap is not equal to 1); the island approach has no such special case but needs unique days per user (hence the dedupe).
- Mapping to SQL: `groupby("user_id")["login_date"].diff()` is `LAG` over the partition, `groupby().cumsum()` is the running `SUM` over the partition, `cumcount()` is `ROW_NUMBER() - 1`.

**Follow-ups:**
- Longest streak per user? Add `groupby("user_id")["streak_days"].max()` on the result; Q21 does the full set of statistics.
- A calendar with weekends excluded? A calendar table of working days and ranking on that, not day numbers.
- Why two keys? The diff key is easier to read and to extend with extra reset conditions; the island key needs no first-row case.

**Common mistakes:**
- Global `diff()` or `shift()` without `groupby` (shown above).
- Not dropping duplicates (the island key is off and streak lengths inflate).
- Comparing `.dt.days` to 1 without handling the NaN first row, or using `== 1` and negating wrongly.
- Grouping by the key only; keys repeat across users (the same `date - rn` number can appear for two users).
- Sorting by date only and not by user and date.

### Q15 ⭐⭐⭐ 🔴 Current streak as of a fixed date: logins(user_id, login_date) and an as-of date of 2024-03-20 (not now). Return each user's current streak length, defined as the island whose end is the as-of date or the day before (state the rule and show the other rule), and 0 or no row for users whose last login is older. Include a user who logged in on the as-of date only, one who last logged in two days before, and one with an earlier longer streak that must not be reported.
**Asked at:** gaps-and-islands prep guides (techinterview.org SQL patterns page and DataVidhya gaps-and-islands lesson, both opened; the DataVidhya page was only an intro) and search snippets of CoddyKit and DevPath lessons; guides and not candidate reports; analyst and data scientist rounds at product companies
**Say this first (1 line):** Cut the logins off at the as-of date (2024-03-20, a fixed value, never today), build the date-streak islands, keep the one island whose end is the as-of date or the day before, and report its length; users without such an island get 0.

**Rule I assume, and the other one:** rule A, "the streak is current if its last login is on the as-of date or the day before", because a user who has not yet logged in today has not broken the streak. Rule B, "the last login must be on the as-of date itself" is stricter. Both are in the Code block (`SQL_MAIN` is rule A, `SQL_STRICT` is rule B) and in the output. Say the rule before writing code.

**Schema and sample data:** twenty-one rows, six users, as-of date 2024-03-20. User 1 logged in on the as-of date only. User 2 last logged in two days before (03-17, 03-18). User 3 has an earlier longer streak (03-01 to 03-07, 7 days, unsorted rows) and a current streak of 03-19 and 03-20, with a duplicate row on 03-20. User 4 has 03-17, 03-18, 03-19 (last login the day before). User 5 has 03-19, 03-20 and two rows after the as-of date (03-21, 03-22, as if loaded later). User 6 has only a NULL date.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-20'),
 (2,'2024-03-17'),(2,'2024-03-18'),
 (3,'2024-03-20'),(3,'2024-03-02'),(3,'2024-03-01'),(3,'2024-03-03'),(3,'2024-03-04'),
 (3,'2024-03-05'),(3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-19'),(3,'2024-03-20'),
 (4,'2024-03-19'),(4,'2024-03-17'),(4,'2024-03-18'),
 (5,'2024-03-22'),(5,'2024-03-19'),(5,'2024-03-20'),(5,'2024-03-21'),
 (6,NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block (rule A). The island part is the date-minus-`ROW_NUMBER` pattern; the as-of cut-off is in the first CTE; the user list comes from the table itself and is `LEFT JOIN`ed to the islands so a user without a current streak shows 0:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
), isl AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
  FROM r
  GROUP BY user_id, grp
)
SELECT u.user_id, COALESCE(i.streak_days, 0) AS current_streak
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN isl i
  ON i.user_id = u.user_id
 AND i.streak_end >= date('2024-03-20', '-1 day')
ORDER BY u.user_id
```
Rule B is the same text with `i.streak_end = '2024-03-20'` in place of the `>=` condition.

**pandas answer:** shown once here and identical to the Code block (`rule_a=True` is rule A):
```py
    users = logins["user_id"].drop_duplicates()
    d = logins.dropna(subset=["login_date"]).copy()
    d["login_date"] = pd.to_datetime(d["login_date"])
    d = d[d["login_date"] <= as_of].drop_duplicates().sort_values(["user_id", "login_date"])
    d["key"] = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days - d.groupby("user_id").cumcount()
    isl = d.groupby(["user_id", "key"], as_index=False).agg(
        streak_end=("login_date", "max"), streak_days=("login_date", "size"))
    cutoff = as_of - pd.Timedelta(days=1) if rule_a else as_of
    cur = isl[isl["streak_end"] >= cutoff].set_index("user_id")["streak_days"]
    out = cur.reindex(users).fillna(0).astype(int).rename("current_streak").reset_index()
    
```

**Example:** islands after the cut-off: U1 03-20 (1 day); U2 03-17 to 03-18 (2); U3 03-01 to 03-07 (7) and 03-19 to 03-20 (2); U4 03-17 to 03-19 (3); U5 03-19 to 03-20 (2).
- Rule A needs `streak_end >= 03-19`. U1 1; U2 ends 03-18, 0; U3 the island ending 03-20, so 2 (the 7-day island ended on 03-07 and is not reported); U4 ends 03-19, so 3; U5 2; U6 has no valid date, 0.
- Rule B needs `streak_end = 03-20`: same except U4 is 0, because its last login was the day before.
- U5 shows why the cut-off matters: without `login_date <= as_of` the future rows 03-21 and 03-22 join the island and U5 becomes 4.

**Code:** run with `python3 -I`. The asserts compare pandas with SQL for both rules, ordered by `user_id`.
```python
# Q15: current streak as of a fixed date (2024-03-20), two rules, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-20'),
 (2,'2024-03-17'),(2,'2024-03-18'),
 (3,'2024-03-20'),(3,'2024-03-02'),(3,'2024-03-01'),(3,'2024-03-03'),(3,'2024-03-04'),
 (3,'2024-03-05'),(3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-19'),(3,'2024-03-20'),
 (4,'2024-03-19'),(4,'2024-03-17'),(4,'2024-03-18'),
 (5,'2024-03-22'),(5,'2024-03-19'),(5,'2024-03-20'),(5,'2024-03-21'),
 (6,NULL);
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
), isl AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
  FROM r
  GROUP BY user_id, grp
)
SELECT u.user_id, COALESCE(i.streak_days, 0) AS current_streak
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN isl i
  ON i.user_id = u.user_id
 AND i.streak_end >= date('2024-03-20', '-1 day')
ORDER BY u.user_id
"""
# other rule: the streak must end ON the as-of date
SQL_STRICT = SQL_MAIN.replace("i.streak_end >= date('2024-03-20', '-1 day')", "i.streak_end = '2024-03-20'")
assert SQL_STRICT != SQL_MAIN
# wrong 1: no cut-off on the as-of date (future rows counted)
SQL_NOCUT = SQL_MAIN.replace(" AND login_date <= '2024-03-20'", "")
assert SQL_NOCUT != SQL_MAIN
# wrong 2: report the longest island instead of the current one
SQL_LONGEST = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'),
r AS (SELECT user_id, login_date,
      date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp FROM d)
SELECT user_id, MAX(n) AS longest_streak FROM (SELECT user_id, grp, COUNT(*) AS n FROM r GROUP BY user_id, grp)
GROUP BY user_id ORDER BY user_id
"""
SQL_ISLANDS = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'),
r AS (SELECT user_id, login_date,
      date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp FROM d)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r GROUP BY user_id, grp ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("islands up to the as-of date:"); print(pd.read_sql_query(SQL_ISLANDS, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_STRICT, con)
c = pd.read_sql_query(SQL_NOCUT, con)
l = pd.read_sql_query(SQL_LONGEST, con)
cmp_ = a.rename(columns={"current_streak": "end_asof_or_day_before"}).assign(
    end_on_asof_only=b["current_streak"], wrong_no_cutoff=c["current_streak"],
    wrong_longest=l.set_index("user_id")["longest_streak"].reindex(a["user_id"]).fillna(0).astype(int).values)
print("current streak as of 2024-03-20:"); print(cmp_.to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
AS_OF = pd.Timestamp("2024-03-20")

def current_streak(logins, as_of, rule_a=True):
    # pd:main
    users = logins["user_id"].drop_duplicates()
    d = logins.dropna(subset=["login_date"]).copy()
    d["login_date"] = pd.to_datetime(d["login_date"])
    d = d[d["login_date"] <= as_of].drop_duplicates().sort_values(["user_id", "login_date"])
    d["key"] = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days - d.groupby("user_id").cumcount()
    isl = d.groupby(["user_id", "key"], as_index=False).agg(
        streak_end=("login_date", "max"), streak_days=("login_date", "size"))
    cutoff = as_of - pd.Timedelta(days=1) if rule_a else as_of
    cur = isl[isl["streak_end"] >= cutoff].set_index("user_id")["streak_days"]
    out = cur.reindex(users).fillna(0).astype(int).rename("current_streak").reset_index()
    # pd:end
    return out.sort_values("user_id").reset_index(drop=True)

pa = current_streak(logins, AS_OF, True)
pb = current_streak(logins, AS_OF, False)
pd.testing.assert_frame_equal(pa, a, check_dtype=False)   # ordered by user_id
pd.testing.assert_frame_equal(pb, b, check_dtype=False)
print("pandas equals SQL for both rules (ordered by user_id): True")

# different as-of date, same data: 2024-03-08 (user 3's long streak just ended on 03-07)
print("rule A as of 2024-03-08:", dict(zip(*[current_streak(logins, pd.Timestamp('2024-03-08'), True)[k] for k in ('user_id','current_streak')])))
print("asserts passed")
```

**Output (my run):**
```text
islands up to the as-of date:
 user_id streak_start streak_end  streak_days
       1   2024-03-20 2024-03-20            1
       2   2024-03-17 2024-03-18            2
       3   2024-03-01 2024-03-07            7
       3   2024-03-19 2024-03-20            2
       4   2024-03-17 2024-03-19            3
       5   2024-03-19 2024-03-20            2
current streak as of 2024-03-20:
 user_id  end_asof_or_day_before  end_on_asof_only  wrong_no_cutoff  wrong_longest
       1                       1                 1                1              1
       2                       0                 0                0              2
       3                       2                 2                2              7
       4                       3                 0                3              3
       5                       2                 2                4              2
       6                       0                 0                0              0
pandas equals SQL for both rules (ordered by user_id): True
rule A as of 2024-03-08: {1: 0, 2: 0, 3: 7, 4: 0, 5: 0, 6: 0}
asserts passed
```

**Edge cases:**
- As-of-date-only user (U1): one island of length 1, reported as 1 under both rules.
- Last login two days before (U2): 0 under both rules, because 03-18 is neither the as-of date nor the day before it.
- Earlier longer streak (U3): the 7-day island is ignored; the `wrong_longest` column shows what you get if you take the maximum island instead (7 for U3, and even 2 for U2).
- Last login the day before (U4): 3 under rule A, 0 under rule B. That one user is the entire difference between the rules.
- Rows after the as-of date (U5): without the cut-off the answer is 4 instead of 2. A fixed as-of date always needs the `<=` filter, or reruns on a growing table change the answer.
- Duplicate row on 03-20 (U3): the `DISTINCT` removes it; without it the day count and the row-number key are both wrong.
- NULL-only user (U6): the user list comes from all rows including the NULL, so U6 is reported with 0; if you want only users with at least one valid login, build the user list from the filtered CTE (then U6 has no row).
- Single-row user: handled (U1).
- Unsorted input: handled by the window `ORDER BY` and the pandas sort.
- At most one island can satisfy "end is the as-of date or the day before", because islands are separated by at least a 1 day gap of missing days, so the join does not duplicate users.
- I also ran rule A with the as-of date moved to 2024-03-08 on the same data: U3 reported 7 (its first streak ended 03-07, the day before). The as-of date is a parameter, not `date('now')`.

**Then explain:**
- Current streak is "the island that is still alive at the as-of date". The one condition `end >= as_of - 1` (or `= as_of`) selects it from the islands.
- Users with no current streak: either leave them out (inner join) or report 0 (left join from the user list). I show 0 and say that the other is also acceptable.
- A common shortcut, `COUNT(*)` of logins after the last gap, is the same idea; the island version is easier to explain and reuse for longest streak (Q21).
- Dialects, not executed here: PostgreSQL would use `login_date - ROW_NUMBER() OVER (...)::int` on a `DATE` column; MySQL `DATE_SUB(login_date, INTERVAL rn DAY)`; BigQuery `DATE_SUB(login_date, INTERVAL rn DAY)`. I did not run these.

**Follow-ups:**
- What about time zones? The streak is in the user's local calendar date; convert before taking the date.
- Current streak for every day of a month, not just one as-of date? Run the same logic per as-of date from a date spine (Q19), or compute islands once and join to the spine.
- Longest streak ever versus current? Longest is the `MAX` over islands (Q21); current is the island at the as-of date.

**Common mistakes:**
- Using `date('now')` as the as-of date, so the answer changes every day and cannot be tested.
- Forgetting the `<= as_of` filter.
- Reporting the longest island instead of the current one.
- Not saying whether yesterday counts (rule A) or only today (rule B).
- Inner join, then claiming users with 0 streak do not exist.

### Q16 ⭐⭐⭐ 🔴 Merge overlapping date ranges: bookings(room_id, start_date, end_date) with inclusive ISO dates. Return the merged continuous blocks per room (room_id, block_start, block_end). Use the sort by start, running MAX(end_date) over the previous rows (ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), a new-block flag when start is greater than that running max, and a running SUM of the flag. Cover a fully contained range (it must not shrink the end), ranges that touch (end = next start, merge) and ranges one day apart (adjacent but not overlapping; state your rule).
**Asked at:** oneuptime interval-merge write-up (opened; running max of end, strict > so touching intervals merge) and the DataDriven 'The Overlap' interval-merge problem (opened; a Python problem, labelled hard and L5, no company named); practice-site material and not candidate reports; data scientist and data engineer rounds
**Say this first (1 line):** Sort each room's ranges by start, compute the running maximum end date over the previous rows only, start a new block when a range starts after that maximum (strict `>`, so touching ranges merge), number the blocks with a running `SUM` of the flag, and take `MIN(start)` and `MAX(end)` per block.

**Rule I assume:** dates are inclusive. Overlapping ranges and ranges that touch (end 03-05, next start 03-05) merge. Ranges one day apart (end 03-08, next start 03-09) are adjacent but not overlapping, so I keep them separate (rule A); rule B, which merges adjacent days as well (useful for "continuous occupancy"), is `start > date(prev_max, '+1 day')`. Both are run below; I would ask which one the business wants.

**Schema and sample data:** twelve rows, four rooms, loaded unsorted. Room 1 has a contained range (03-02 to 03-03 inside 03-01 to 03-05), a touching range (03-05 to 03-08 starts on the end day of 03-01 to 03-05), a range one day apart (03-09 to 03-10 right after 03-08) and a separate far range (03-15 to 03-16). Room 2 has one single-day booking. Room 3 has an exact duplicate row, a row with a NULL end date and an inverted row (end before start). Room 4 has two ranges with the same start (03-01 to 03-03 and 03-01 to 03-10). Dates are ISO text, so string comparison orders them correctly.
```sql
CREATE TABLE bookings(room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-09','2024-03-10'),
 (1,'2024-03-05','2024-03-08'),
 (1,'2024-03-01','2024-03-05'),
 (1,'2024-03-02','2024-03-03'),
 (1,'2024-03-15','2024-03-16'),
 (2,'2024-03-01','2024-03-01'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-11',NULL),
 (3,'2024-03-20','2024-03-18'),
 (4,'2024-03-01','2024-03-03'),
 (4,'2024-03-01','2024-03-10');
```

**SQL answer:** `SQL_MAIN` in the Code block (rule A). Bad rows (NULL start or end, end before start) are excluded in the first CTE and I say so; the running `MAX` frame is `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`, which runs on SQLite 3.45.1 and gives NULL on the first row of each room:
```sql
WITH b AS (
  SELECT room_id, start_date, end_date
  FROM bookings
  WHERE start_date IS NOT NULL AND end_date IS NOT NULL AND end_date >= start_date
), m AS (
  SELECT room_id, start_date, end_date,
         MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM b
), f AS (
  SELECT *, CASE WHEN prev_max IS NULL OR start_date > prev_max THEN 1 ELSE 0 END AS new_block
  FROM m
), g AS (
  SELECT *, SUM(new_block) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block_id
  FROM f
)
SELECT room_id, MIN(start_date) AS block_start, MAX(end_date) AS block_end
FROM g
GROUP BY room_id, block_id
ORDER BY room_id, block_start
```
Rule B is the same text with `start_date > date(prev_max, '+1 day')` (`SQL_ADJ` in the Code block). `SQL_LAG` replaces the running max by `LAG(end_date)` to show the bug.

**pandas answer:** shown once here and identical to the Code block. `cummax()` inside `groupby` is the running maximum, and the second `groupby(...).shift()` makes it "previous rows only":
```py
    d = bookings.dropna(subset=["start_date", "end_date"]).copy()
    d["start_date"] = pd.to_datetime(d["start_date"])
    d["end_date"] = pd.to_datetime(d["end_date"])
    d = d[d["end_date"] >= d["start_date"]].sort_values(["room_id", "start_date", "end_date"])
    prev_max = d.groupby("room_id")["end_date"].cummax().groupby(d["room_id"]).shift()
    slack = pd.Timedelta(days=1) if adjacent else pd.Timedelta(0)
    new_block = prev_max.isna() | (d["start_date"] > prev_max + slack)
    d["block_id"] = new_block.astype(int).groupby(d["room_id"]).cumsum()
    out = d.groupby(["room_id", "block_id"], as_index=False).agg(
        block_start=("start_date", "min"), block_end=("end_date", "max"))
    
```

**Example:** room 1 sorted by start: A 03-01 to 03-05, B 03-02 to 03-03, C 03-05 to 03-08, D 03-09 to 03-10, E 03-15 to 03-16.
- Previous running max end: A none, B 03-05, C 03-05 (B did not shrink it), D 03-08, E 03-10.
- Flag (start > previous max): A 1 (first), B 0 (03-02 is not after 03-05), C 0 (03-05 is not after 03-05: touching merges), D 1 under rule A (03-09 is after 03-08), E 1 (03-15 is after 03-10).
- Blocks: A, B and C together are 03-01 to 03-08; D alone is 03-09 to 03-10; E alone is 03-15 to 03-16.
- Rule B: D's start is not after 03-08 plus one day (03-09), flag 0, so room 1 becomes 03-01 to 03-10 and 03-15 to 03-16.
- Room 4: sorted by start then end: 03-01 to 03-03, then 03-01 to 03-10, one block 03-01 to 03-10. Room 3: the duplicate merges into one block 03-10 to 03-12; the NULL-end and inverted rows are excluded.

**Code:** run with `python3 -I`. The asserts compare pandas with SQL for both rules after ordering by `room_id, block_start`.
```python
# Q16: merge overlapping inclusive date ranges: running MAX(end) over previous rows, flag, running SUM
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE bookings(room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,'2024-03-09','2024-03-10'),
 (1,'2024-03-05','2024-03-08'),
 (1,'2024-03-01','2024-03-05'),
 (1,'2024-03-02','2024-03-03'),
 (1,'2024-03-15','2024-03-16'),
 (2,'2024-03-01','2024-03-01'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-10','2024-03-12'),
 (3,'2024-03-11',NULL),
 (3,'2024-03-20','2024-03-18'),
 (4,'2024-03-01','2024-03-03'),
 (4,'2024-03-01','2024-03-10');
"""
SQL_MAIN = """
WITH b AS (
  SELECT room_id, start_date, end_date
  FROM bookings
  WHERE start_date IS NOT NULL AND end_date IS NOT NULL AND end_date >= start_date
), m AS (
  SELECT room_id, start_date, end_date,
         MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
  FROM b
), f AS (
  SELECT *, CASE WHEN prev_max IS NULL OR start_date > prev_max THEN 1 ELSE 0 END AS new_block
  FROM m
), g AS (
  SELECT *, SUM(new_block) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block_id
  FROM f
)
SELECT room_id, MIN(start_date) AS block_start, MAX(end_date) AS block_end
FROM g
GROUP BY room_id, block_id
ORDER BY room_id, block_start
"""
# rule B: ranges one day apart (end 03-10, next start 03-11) also merge
SQL_ADJ = SQL_MAIN.replace("start_date > prev_max", "start_date > date(prev_max, '+1 day')")
assert SQL_ADJ != SQL_MAIN
# wrong: compare with the previous row's end (LAG) instead of the running max
SQL_LAG = SQL_MAIN.replace(
    """MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)""",
    "LAG(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date)")
assert SQL_LAG != SQL_MAIN
# NULL end_date read as open-ended instead of excluded
SQL_OPEN = SQL_MAIN.replace("end_date IS NOT NULL AND end_date >= start_date", "1 = 1") \
                   .replace("end_date\n  FROM bookings", "COALESCE(end_date, '9999-12-31') AS end_date\n  FROM bookings")
assert SQL_OPEN != SQL_MAIN
SQL_DETAIL = """
SELECT room_id, start_date, end_date,
       MAX(end_date) OVER (PARTITION BY room_id ORDER BY start_date, end_date
                           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_max
FROM bookings WHERE room_id = 1 ORDER BY start_date, end_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("room 1 running max of the previous rows' end_date:"); print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
print("rule A, merge when start <= running max end (touching merges, one day apart does not):"); print(a.to_string(index=False))
b = pd.read_sql_query(SQL_ADJ, con)
print("rule B, also merge ranges one day apart:"); print(b.to_string(index=False))
print("wrong, LAG(end_date) instead of running max, room 1 and 4:")
print(pd.read_sql_query(SQL_LAG, con).query("room_id in (1, 4)").to_string(index=False))
print("NULL end_date treated as open-ended (room 3):")
print(pd.read_sql_query(SQL_OPEN, con).query("room_id == 3").to_string(index=False))

bookings = pd.read_sql_query("SELECT * FROM bookings", con)

def merge_ranges(bookings, adjacent=False):
    # pd:main
    d = bookings.dropna(subset=["start_date", "end_date"]).copy()
    d["start_date"] = pd.to_datetime(d["start_date"])
    d["end_date"] = pd.to_datetime(d["end_date"])
    d = d[d["end_date"] >= d["start_date"]].sort_values(["room_id", "start_date", "end_date"])
    prev_max = d.groupby("room_id")["end_date"].cummax().groupby(d["room_id"]).shift()
    slack = pd.Timedelta(days=1) if adjacent else pd.Timedelta(0)
    new_block = prev_max.isna() | (d["start_date"] > prev_max + slack)
    d["block_id"] = new_block.astype(int).groupby(d["room_id"]).cumsum()
    out = d.groupby(["room_id", "block_id"], as_index=False).agg(
        block_start=("start_date", "min"), block_end=("end_date", "max"))
    # pd:end
    out = out.drop(columns="block_id")
    for c in ("block_start", "block_end"):
        out[c] = out[c].dt.strftime("%Y-%m-%d")
    return out.sort_values(["room_id", "block_start"]).reset_index(drop=True)

pd.testing.assert_frame_equal(merge_ranges(bookings, False), a, check_dtype=False)   # ordered by room_id, block_start
pd.testing.assert_frame_equal(merge_ranges(bookings, True), b, check_dtype=False)
print("pandas equals SQL for both rules (ordered by room_id, block_start): True")
print("asserts passed")
```

**Output (my run):**
```text
room 1 running max of the previous rows' end_date:
 room_id start_date   end_date   prev_max
       1 2024-03-01 2024-03-05        NaN
       1 2024-03-02 2024-03-03 2024-03-05
       1 2024-03-05 2024-03-08 2024-03-05
       1 2024-03-09 2024-03-10 2024-03-08
       1 2024-03-15 2024-03-16 2024-03-10
rule A, merge when start <= running max end (touching merges, one day apart does not):
 room_id block_start  block_end
       1  2024-03-01 2024-03-08
       1  2024-03-09 2024-03-10
       1  2024-03-15 2024-03-16
       2  2024-03-01 2024-03-01
       3  2024-03-10 2024-03-12
       4  2024-03-01 2024-03-10
rule B, also merge ranges one day apart:
 room_id block_start  block_end
       1  2024-03-01 2024-03-10
       1  2024-03-15 2024-03-16
       2  2024-03-01 2024-03-01
       3  2024-03-10 2024-03-12
       4  2024-03-01 2024-03-10
wrong, LAG(end_date) instead of running max, room 1 and 4:
 room_id block_start  block_end
       1  2024-03-01 2024-03-05
       1  2024-03-05 2024-03-08
       1  2024-03-09 2024-03-10
       1  2024-03-15 2024-03-16
       4  2024-03-01 2024-03-10
NULL end_date treated as open-ended (room 3):
 room_id block_start  block_end
       3  2024-03-10 9999-12-31
pandas equals SQL for both rules (ordered by room_id, block_start): True
asserts passed
```

**Edge cases:**
- Contained range (B): the running max stayed 03-05 after B, shown in the detail table (`prev_max` for C is 03-05, not 03-03). Using `LAG(end_date)` instead (the wrong version in the output) compares C with B's end 03-03, so C looks like a new block and room 1 comes out as `03-01 to 03-05` and `03-05 to 03-08`, two blocks that touch and should be one.
- Touching (C starts on A's end day): merged under strict `>`. With `>=` they would split, the opposite of what inclusive dates mean.
- One day apart (D): separate under rule A, merged under rule B, and the two outputs differ for room 1 (three blocks versus two).
- Same start (room 4): ordering by `start_date, end_date` makes the shorter range first; the long one then has start equal to the previous max start, so it merges either way. The result does not depend on the tie order, but the frame must still list all previous rows.
- Exact duplicate rows (room 3): merge into one block, no special handling.
- NULL end: `MAX` ignores NULLs and `NULL >= start` is not true, so I exclude NULL rows explicitly. If NULL means "still open", treat it as a far-future date: in my run that turned room 3 into the single block `03-10 to 9999-12-31` (and that variant also stopped excluding the inverted row). Say which meaning you take.
- Single-range room (room 2): `prev_max` NULL, one block.
- Unsorted input: handled by the window `ORDER BY`.
- Inverted rows (end before start) are data errors; I filter them, you might instead report them.

**Then explain:**
- Why a running max and not the previous end: a long range can swallow several short ones, so the end to compare against is the largest end seen so far, not the last one.
- Why the frame stops one row before the current one: the test is "does this range start after everything that came before it?". The first row of each room then has an empty frame, `prev_max` is NULL, and that NULL is the "new block" signal.
- The running `SUM` of the flag numbers the blocks (running-total mechanics are Part 5); `MIN` and `MAX` per block give the merged range.
- Dialects, not executed here: PostgreSQL and MySQL 8 accept the same frame text, and PostgreSQL's date arithmetic would be `prev_max + 1`; MySQL 5.7 has no window functions; BigQuery would use `DATE_ADD(prev_max, INTERVAL 1 DAY)`. An engine without window frames needs a self-join or a recursive CTE (pointer to Part 9). None of this was executed.

**Follow-ups:**
- Total booked days per room after merging? `SUM(julianday(block_end) - julianday(block_start) + 1)` over the blocks (inclusive end adds one).
- Find double-bookings instead of merging them? A self-join where `a.start <= b.end AND b.start <= a.end AND a.rowid < b.rowid`.
- Why not just group by room and take min/max? That would join separate blocks into one range.

**Common mistakes:**
- `LAG(end_date)` instead of a running max (a contained range then shrinks the block).
- `>=` in the flag, which splits ranges that touch.
- Not stating whether one-day-apart ranges merge.
- Forgetting the first row's NULL, so the first range of each room never starts a block.
- Not sorting by start inside each room, or sorting by end.
- Comparing the new range's start with the maximum of start dates (or with its own end) instead of the maximum end of earlier rows.

### Q17 ⭐⭐⭐ 🔴 Maximum concurrent users: sessions(user_id, login_ts, logout_ts). Return the peak number of simultaneous sessions and the time it first occurs, using a +1/-1 event sweep: UNION ALL of (login_ts, +1) and (logout_ts, -1), a running SUM over time ordered so that at identical timestamps the -1 comes before the +1 (state why, and what the other order does to back-to-back sessions), then MAX. Show the answer on a small table with a session ending exactly when another starts.
**Asked at:** Itzik Ben-Gan interval packing and gaps-and-islands articles (search snippets only, not opened) and the Oracle SQL blog on longest and current streaks (snippet only); guides and not candidate reports; senior analyst and data engineer rounds
**Say this first (1 line):** Turn every session into two events, +1 at login and -1 at logout, sort all events by time with the -1 before the +1 at the same timestamp, take a running `SUM`, and the maximum of that running sum is the peak; the earliest time it reaches the peak is when it first occurs.

**Rule I assume:** a session is open from its login up to, but not including, its logout (half-open). A session that ends at 10:00:00 and another that starts at 10:00:00 do not overlap, so they must not count as 2 at that instant; that is why the -1 sorts first.

**Schema and sample data:** seven rows. User 1 is 09:00 to 10:00, user 2 is 09:30 to 10:30, user 3 is 10:00 to 11:00 (starts exactly when user 1 ends, the back-to-back case), user 4 is 10:40 to 10:50, user 5 logged in at 12:00 and has not logged out (NULL logout, still open), user 6 logs in and out at 13:00:00 (zero length), user 7 has a NULL login (bad row). Rows are not in time order. Timestamps are ISO text.
```sql
CREATE TABLE sessions(user_id INTEGER, login_ts TEXT, logout_ts TEXT);
INSERT INTO sessions VALUES
 (3,'2024-03-01 10:00:00','2024-03-01 11:00:00'),
 (1,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (2,'2024-03-01 09:30:00','2024-03-01 10:30:00'),
 (4,'2024-03-01 10:40:00','2024-03-01 10:50:00'),
 (5,'2024-03-01 12:00:00',NULL),
 (6,'2024-03-01 13:00:00','2024-03-01 13:00:00'),
 (7,NULL,'2024-03-01 14:00:00');
```

**SQL answer:** `SQL_MAIN` in the Code block. `ORDER BY ts, delta` puts -1 (smaller number) before +1 at the same timestamp; the frame is written out as `ROWS`:
```sql
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions WHERE login_ts IS NOT NULL
  UNION ALL
  SELECT logout_ts, -1 FROM sessions WHERE login_ts IS NOT NULL AND logout_ts IS NOT NULL
), run AS (
  SELECT ts, delta,
         SUM(delta) OVER (ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
  FROM ev
)
SELECT concurrent AS peak, MIN(ts) AS first_time
FROM run
WHERE concurrent = (SELECT MAX(concurrent) FROM run)
```
`SQL_PLUS_FIRST` is the same text with `delta DESC` (+1 first), `SQL_TS_ONLY` orders by `ts` only with a `ROWS` frame, and `SQL_RANGE` orders by `ts` only with the default frame.

**pandas answer:** shown once here and identical to the Code block. Both sort keys are given, so the order of the two concatenated halves does not matter:
```py
s = sessions.dropna(subset=["login_ts"])
ev = pd.concat([
    pd.DataFrame({"ts": s["login_ts"], "delta": 1}),
    pd.DataFrame({"ts": s["logout_ts"], "delta": -1}).dropna(subset=["ts"]),
])
ev["ts"] = pd.to_datetime(ev["ts"])
ev = ev.sort_values(["ts", "delta"], kind="stable").reset_index(drop=True)
ev["concurrent"] = ev["delta"].cumsum()
peak = ev["concurrent"].max()
first_time = ev.loc[ev["concurrent"] == peak, "ts"].min().strftime("%Y-%m-%d %H:%M:%S")
```

**Example:** the sorted events and running count are in the first block of the output.
- 09:00 +1 gives 1; 09:30 +1 gives 2.
- 10:00 has two events: -1 (user 1 leaves) then +1 (user 3 joins): 2 to 1 to 2. At no instant are three people in.
- 10:30 -1 gives 1; 10:40 +1 gives 2 (user 3 and user 4); 10:50 -1 gives 1; 11:00 -1 gives 0; 12:00 +1 gives 1 (user 5, never closed).
- Peak is 2, first reached at 09:30:00. An independent check that counts, for each login time, the sessions with `login <= t < logout` also gave 2.
- With +1 first at 10:00 the running count goes 2, 3, 2: it reports a peak of 3 at 10:00:00 that never happened.

**Code:** run with `python3 -I`. The assert compares the single result row (peak and first time) of pandas with SQL, so no row order is involved.
```python
# Q17: maximum concurrent sessions with a +1/-1 event sweep; -1 before +1 at identical timestamps
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sessions(user_id INTEGER, login_ts TEXT, logout_ts TEXT);
INSERT INTO sessions VALUES
 (3,'2024-03-01 10:00:00','2024-03-01 11:00:00'),
 (1,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (2,'2024-03-01 09:30:00','2024-03-01 10:30:00'),
 (4,'2024-03-01 10:40:00','2024-03-01 10:50:00'),
 (5,'2024-03-01 12:00:00',NULL),
 (6,'2024-03-01 13:00:00','2024-03-01 13:00:00'),
 (7,NULL,'2024-03-01 14:00:00');
"""
SQL_MAIN = """
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions WHERE login_ts IS NOT NULL
  UNION ALL
  SELECT logout_ts, -1 FROM sessions WHERE login_ts IS NOT NULL AND logout_ts IS NOT NULL
), run AS (
  SELECT ts, delta,
         SUM(delta) OVER (ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
  FROM ev
)
SELECT concurrent AS peak, MIN(ts) AS first_time
FROM run
WHERE concurrent = (SELECT MAX(concurrent) FROM run)
"""
# wrong order at identical timestamps: +1 before -1
SQL_PLUS_FIRST = SQL_MAIN.replace("ORDER BY ts, delta ROWS", "ORDER BY ts, delta DESC ROWS")
assert SQL_PLUS_FIRST != SQL_MAIN
# ties left to the engine: ORDER BY ts only with a ROWS frame
SQL_TS_ONLY = SQL_MAIN.replace("ORDER BY ts, delta ROWS", "ORDER BY ts ROWS")
assert SQL_TS_ONLY != SQL_MAIN
# ORDER BY ts only with the default RANGE frame: tied rows are peers and are added together
SQL_RANGE = SQL_MAIN.replace("ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW", "ORDER BY ts")
assert SQL_RANGE != SQL_MAIN
SQL_TRACE = """
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions WHERE login_ts IS NOT NULL
  UNION ALL
  SELECT logout_ts, -1 FROM sessions WHERE login_ts IS NOT NULL AND logout_ts IS NOT NULL
)
SELECT ts, delta,
       SUM(delta) OVER (ORDER BY ts, delta ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
FROM ev ORDER BY ts, delta
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("event sweep, -1 before +1 at the same timestamp:"); print(pd.read_sql_query(SQL_TRACE, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
print("SQL_MAIN:", a.values.tolist())
print("wrong, +1 before -1 at ties:", pd.read_sql_query(SQL_PLUS_FIRST, con).values.tolist())
print("ORDER BY ts only, ROWS frame (ties left to the engine):", pd.read_sql_query(SQL_TS_ONLY, con).values.tolist())
print("ORDER BY ts only, default RANGE frame:", pd.read_sql_query(SQL_RANGE, con).values.tolist())
print("independent check, sessions open at each login time (login <= t < logout): peak sessions =",
      con.execute("SELECT MAX(c) FROM (SELECT (SELECT COUNT(*) FROM sessions o WHERE o.login_ts <= s.login_ts "
                  "AND (o.logout_ts IS NULL OR o.logout_ts > s.login_ts)) AS c FROM sessions s WHERE s.login_ts IS NOT NULL)").fetchone()[0])

sessions = pd.read_sql_query("SELECT * FROM sessions", con)
# pd:main
s = sessions.dropna(subset=["login_ts"])
ev = pd.concat([
    pd.DataFrame({"ts": s["login_ts"], "delta": 1}),
    pd.DataFrame({"ts": s["logout_ts"], "delta": -1}).dropna(subset=["ts"]),
])
ev["ts"] = pd.to_datetime(ev["ts"])
ev = ev.sort_values(["ts", "delta"], kind="stable").reset_index(drop=True)
ev["concurrent"] = ev["delta"].cumsum()
peak = ev["concurrent"].max()
first_time = ev.loc[ev["concurrent"] == peak, "ts"].min().strftime("%Y-%m-%d %H:%M:%S")
# pd:end
print("pandas:", [int(peak), first_time])
assert [int(peak), first_time] == a.values.tolist()[0]   # one row, no ordering needed
print("running value right after the zero-length session's -1 at 13:00:", int(ev.loc[(ev.ts == "2024-03-01 13:00:00") & (ev.delta == -1), "concurrent"].iloc[0]))

# empty table
con.execute("DELETE FROM sessions")
print("empty table, SQL rows returned:", con.execute(SQL_MAIN).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
event sweep, -1 before +1 at the same timestamp:
                 ts  delta  concurrent
2024-03-01 09:00:00      1           1
2024-03-01 09:30:00      1           2
2024-03-01 10:00:00     -1           1
2024-03-01 10:00:00      1           2
2024-03-01 10:30:00     -1           1
2024-03-01 10:40:00      1           2
2024-03-01 10:50:00     -1           1
2024-03-01 11:00:00     -1           0
2024-03-01 12:00:00      1           1
2024-03-01 13:00:00     -1           0
2024-03-01 13:00:00      1           1
SQL_MAIN: [[2, '2024-03-01 09:30:00']]
wrong, +1 before -1 at ties: [[3, '2024-03-01 10:00:00']]
ORDER BY ts only, ROWS frame (ties left to the engine): [[3, '2024-03-01 10:00:00']]
ORDER BY ts only, default RANGE frame: [[2, '2024-03-01 09:30:00']]
independent check, sessions open at each login time (login <= t < logout): peak sessions = 2
pandas: [2, '2024-03-01 09:30:00']
running value right after the zero-length session's -1 at 13:00: 0
empty table, SQL rows returned: [(None, None)]
asserts passed
```

**Edge cases:**
- Back-to-back sessions: correct order gives peak 2 at 09:30; the wrong order gives peak 3 at 10:00:00, both in my run.
- `ORDER BY ts` only with a `ROWS` frame leaves the order of the tied events to the engine; in this run it also gave the wrong 3 at 10:00:00 (the `+1` rows come from the first branch of the `UNION ALL`, so they came first here). Not guaranteed either way, so name the tie-break.
- `ORDER BY ts` only with the default `RANGE` frame treats tied rows as peers and adds them together, so the +1 and -1 at 10:00 net out; it gave the right answer (2 at 09:30). It works, but it relies on the default frame and hides the rule; I prefer the explicit `ts, delta` with `ROWS`.
- Still-open session (NULL logout): only a +1 event, no -1, so it stays open forever; user 5 is counted from 12:00 on. If instead open sessions should be cut at an as-of time, `COALESCE(logout_ts, as_of)` with a fixed as-of value (never now).
- Zero-length session (user 6): its -1 sorts before its own +1, so the running count dips by one at 13:00 (0 in my run, while user 5 is still open) and returns to 1. Under the half-open rule a zero-length session is open for no time, so ignoring it is consistent; the peak is unaffected unless a peak coincides with such a session. If you count it, sort by session instead.
- NULL login (user 7): excluded; its logout alone would produce a -1 with no +1 and a negative count.
- Same user with overlapping sessions (two tabs) counts twice; if the question is "distinct users online", a plain sweep is not enough (dedupe the user's overlapping sessions first, for example with the interval merge in Q16).
- Several moments with the same peak: the query returns the earliest. Empty table: SQL returned one row with NULL peak and NULL time in my run (the aggregate without `GROUP BY` always returns a row).
- Time zones: the events must all be in the same zone (UTC); SQLite stores text, no conversion here.

**Then explain:**
- The sweep is a running total over +1 and -1; the running sum after an event is the number of open sessions right after that event.
- Order at ties: ends first when the interval is half-open. If sessions were closed intervals (logout inclusive), the right order would be +1 first, so "state your convention" is the real answer.
- Peak versus when: `MAX(concurrent)` is the peak; the time is the minimum `ts` among events whose running count equals the peak. Because within a tie the -1 comes first, the running count at an intermediate row is never inflated.
- Compare with the self-join check: for each login time, count sessions with `login <= t AND logout > t`; same answer, O(n squared), fine for a check, slower on big data.
- Dialects, not executed here: the same query runs on PostgreSQL and MySQL 8 as written; BigQuery would need `ROWS` in the same form; on MySQL 5.7 there are no window functions, and a correlated count is the fallback.

**Follow-ups:**
- Peak per day or per hour? Partition the sweep (and cut sessions that cross midnight into two pieces).
- How long was the system at the peak level? Use `LEAD(ts)` over the events and sum the time where the count equals the peak.
- Count per minute for a chart? Join a date spine (Q19) to the sessions with `login <= minute AND logout > minute`.

**Common mistakes:**
- Putting +1 before -1 at the same timestamp (shown above: peak 3 at 10:00:00 instead of 2).
- Leaving the tie order to the engine.
- Excluding NULL-logout rows, which silently drops people still online.
- Counting a session twice because of `UNION` instead of `UNION ALL` (identical rows would collapse).
- Reporting the peak without saying whether the interval is half-open.

### Q18 ⭐⭐ 🟢 Consecutive Available Seats (LeetCode 603): cinema(seat_id, free) with free as 0 or 1, seat ids ordered. Return the seat ids of free seats that have an adjacent free seat, ordered by seat_id. Show the self join, a LAG/LEAD version, and the island version that finds runs of at least 2 free seats; say what each does with ids that have gaps and with a free seat at the first or last position.
**Asked at:** public LeetCode-style problem bank (statements known from search snippets and mirrors such as doocs, walkccc and talentd; the leetcode.com pages returned HTTP 403 and were not opened), not candidate reports; analyst, data scientist and data engineer screens at product companies and GCCs
**Say this first (1 line):** A free seat qualifies if the seat with id minus 1 or id plus 1 is also free; the self join says that directly with `ABS(a.seat_id - b.seat_id) = 1`, the `LAG`/`LEAD` version must also check that the neighbouring row's id really is id plus or minus 1, and the island version keeps free seats whose `seat_id - ROW_NUMBER()` group has at least 2 members.

**Schema and sample data:** thirteen rows loaded unsorted (seat 14 first). Free runs: seats 1 and 2 (the first position), seat 4 alone, seats 6, 7, 8 (a run of three), seat 10 has a NULL `free` (unknown), seat 11 is free but its neighbours are seat 10 (NULL) and a missing seat 12, seats 13 and 14 (the last position). Seat 12 does not exist in the table, so ids have a gap between 11 and 13. The statement of LeetCode 603 (premium; I did not open the page) is, as I remember it, `cinema(seat_id, free)` with seat ids in order and free 0 or 1; I do not rely on there being no gaps, and the data above has one.
```sql
CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER);
INSERT INTO cinema VALUES
 (14,1),(1,1),(2,1),(3,0),(4,1),(5,0),(6,1),(7,1),(8,1),(9,0),(10,NULL),(11,1),(13,1);
```
Expected by hand: 1, 2, 6, 7, 8, 13, 14.

**SQL answer:** three versions in the Code block. Self join (`SQL_JOIN`):
```sql
SELECT DISTINCT a.seat_id
FROM cinema a
JOIN cinema b ON ABS(a.seat_id - b.seat_id) = 1
WHERE a.free = 1 AND b.free = 1
ORDER BY a.seat_id
```
`LAG`/`LEAD` with the id check (`SQL_LAGLEAD`):
```sql
WITH x AS (
  SELECT seat_id, free,
         LAG(seat_id)  OVER (ORDER BY seat_id) AS prev_id,
         LAG(free)     OVER (ORDER BY seat_id) AS prev_free,
         LEAD(seat_id) OVER (ORDER BY seat_id) AS next_id,
         LEAD(free)    OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id
FROM x
WHERE free = 1
  AND ((prev_free = 1 AND prev_id = seat_id - 1) OR (next_free = 1 AND next_id = seat_id + 1))
ORDER BY seat_id
```
Island version (`SQL_ISLAND`), filtering to free seats first so the row numbers count only free seats:
```sql
WITH f AS (
  SELECT seat_id, seat_id - ROW_NUMBER() OVER (ORDER BY seat_id) AS grp
  FROM cinema
  WHERE free = 1
)
SELECT seat_id
FROM f
WHERE grp IN (SELECT grp FROM f GROUP BY grp HAVING COUNT(*) >= 2)
ORDER BY seat_id
```
`SQL_NAIVE` in the Code block is the `LAG`/`LEAD` version without the id check, to show the bug.

**pandas answer:** neighbour version and island version, shown once here and identical to the Code block:
```py
c = cinema.sort_values("seat_id").reset_index(drop=True)
is_free = c["free"].eq(1)                      # NULL counts as not free
prev_adj = is_free.shift(fill_value=False) & (c["seat_id"].diff() == 1)
next_adj = is_free.shift(-1, fill_value=False) & (c["seat_id"].diff(-1) == -1)
pd_neighbor = c.loc[is_free & (prev_adj | next_adj), "seat_id"].tolist()
f = c[is_free]
key = f["seat_id"] - range(len(f))
pd_island = f.loc[key.groupby(key).transform("size") >= 2, "seat_id"].tolist()
```

**Example:** free seats are 1, 2, 4, 6, 7, 8, 11, 13, 14.
- Self join: pairs of free seats whose ids differ by 1 are (1,2), (6,7), (7,8), (13,14), each in both directions; the distinct seat ids are 1, 2, 6, 7, 8, 13, 14. Seat 4 has no free neighbour (3 and 5 are taken) and seat 11 has none (10 is NULL, 12 does not exist).
- Island: `seat_id - ROW_NUMBER()` over free seats only: seats 1, 2, 4, 6, 7, 8, 11, 13, 14 get row numbers 1 to 9, so the groups are 0, 0, 1, 2, 2, 2, 4, 5, 5. Group sizes are 2, 1, 3, 1, 2. Keep sizes of 2 or more: 1, 2, 6, 7, 8, 13, 14.
- Naive `LAG`/`LEAD` on rows: seat 11's next row is seat 13, which is free, so it wrongly qualifies.

**Code:** run with `python3 -I`. The asserts compare the three SQL versions, both pandas versions and the hand-written expected list, all ordered by `seat_id`; the naive version is asserted to differ.
```python
# Q18: Consecutive Available Seats (LeetCode 603 style): self join, LAG/LEAD, island version
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER);
INSERT INTO cinema VALUES
 (14,1),(1,1),(2,1),(3,0),(4,1),(5,0),(6,1),(7,1),(8,1),(9,0),(10,NULL),(11,1),(13,1);
"""
SQL_JOIN = """
SELECT DISTINCT a.seat_id
FROM cinema a
JOIN cinema b ON ABS(a.seat_id - b.seat_id) = 1
WHERE a.free = 1 AND b.free = 1
ORDER BY a.seat_id
"""
SQL_LAGLEAD = """
WITH x AS (
  SELECT seat_id, free,
         LAG(seat_id)  OVER (ORDER BY seat_id) AS prev_id,
         LAG(free)     OVER (ORDER BY seat_id) AS prev_free,
         LEAD(seat_id) OVER (ORDER BY seat_id) AS next_id,
         LEAD(free)    OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id
FROM x
WHERE free = 1
  AND ((prev_free = 1 AND prev_id = seat_id - 1) OR (next_free = 1 AND next_id = seat_id + 1))
ORDER BY seat_id
"""
SQL_ISLAND = """
WITH f AS (
  SELECT seat_id, seat_id - ROW_NUMBER() OVER (ORDER BY seat_id) AS grp
  FROM cinema
  WHERE free = 1
)
SELECT seat_id
FROM f
WHERE grp IN (SELECT grp FROM f GROUP BY grp HAVING COUNT(*) >= 2)
ORDER BY seat_id
"""
# wrong: LAG/LEAD on rows without checking that the ids are consecutive
SQL_NAIVE = """
WITH x AS (
  SELECT seat_id, free,
         LAG(free)  OVER (ORDER BY seat_id) AS prev_free,
         LEAD(free) OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id FROM x WHERE free = 1 AND (prev_free = 1 OR next_free = 1) ORDER BY seat_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for name, sql in (("self join", SQL_JOIN), ("LAG/LEAD with id check", SQL_LAGLEAD),
                  ("island (ids minus ROW_NUMBER)", SQL_ISLAND), ("naive LAG/LEAD, no id check", SQL_NAIVE)):
    res[name] = [r[0] for r in con.execute(sql)]
    print(f"{name}: {res[name]}")

cinema = pd.read_sql_query("SELECT * FROM cinema", con)
# pd:main
c = cinema.sort_values("seat_id").reset_index(drop=True)
is_free = c["free"].eq(1)                      # NULL counts as not free
prev_adj = is_free.shift(fill_value=False) & (c["seat_id"].diff() == 1)
next_adj = is_free.shift(-1, fill_value=False) & (c["seat_id"].diff(-1) == -1)
pd_neighbor = c.loc[is_free & (prev_adj | next_adj), "seat_id"].tolist()
f = c[is_free]
key = f["seat_id"] - range(len(f))
pd_island = f.loc[key.groupby(key).transform("size") >= 2, "seat_id"].tolist()
# pd:end
print("pandas neighbour version:", pd_neighbor)
print("pandas island version:", pd_island)
expected = [1, 2, 6, 7, 8, 13, 14]
assert res["self join"] == res["LAG/LEAD with id check"] == res["island (ids minus ROW_NUMBER)"] == expected
assert pd_neighbor == pd_island == expected   # all lists are ordered by seat_id
assert res["naive LAG/LEAD, no id check"] != expected
print("the naive version adds:", sorted(set(res["naive LAG/LEAD, no id check"]) - set(expected)))

# tiny cases: one seat, empty table, all free
for label, rows in (("single free seat", [(1, 1)]), ("empty table", []), ("all free, ids 5..7", [(5, 1), (6, 1), (7, 1)])):
    c2 = sqlite3.connect(":memory:")
    c2.execute("CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER)")
    c2.executemany("INSERT INTO cinema VALUES (?, ?)", rows)
    out = [[r[0] for r in c2.execute(s)] for s in (SQL_JOIN, SQL_LAGLEAD, SQL_ISLAND)]
    assert out[0] == out[1] == out[2]
    print(f"{label}: all three SQL versions return {out[0]}")
print("asserts passed")
```

**Output (my run):**
```text
self join: [1, 2, 6, 7, 8, 13, 14]
LAG/LEAD with id check: [1, 2, 6, 7, 8, 13, 14]
island (ids minus ROW_NUMBER): [1, 2, 6, 7, 8, 13, 14]
naive LAG/LEAD, no id check: [1, 2, 6, 7, 8, 11, 13, 14]
pandas neighbour version: [1, 2, 6, 7, 8, 13, 14]
pandas island version: [1, 2, 6, 7, 8, 13, 14]
the naive version adds: [11]
single free seat: all three SQL versions return []
empty table: all three SQL versions return []
all free, ids 5..7: all three SQL versions return [5, 6, 7]
asserts passed
```

**Edge cases:**
- Gaps in ids: the self join and the island version handle them for free (a missing id never matches `ABS(...) = 1`, and a missing id breaks the `seat_id - ROW_NUMBER()` group). `LAG`/`LEAD` compare the neighbouring row, not the neighbouring id, so they need the extra `prev_id = seat_id - 1` check; without it seat 11 was returned in my run.
- First and last positions: seat 1 has no `LAG` row (NULL), so `prev_free = 1` is not true, but `next_free = 1` can still make it qualify; seat 14 has no `LEAD` row. The `OR` handles both ends. The self join has no special case at the ends either.
- NULL `free` (seat 10): `free = 1` is not true for NULL, so it is treated as not free everywhere; seat 11 does not qualify through it. In pandas, `.eq(1)` returns False for NaN.
- Single free seat, empty table, all free (ids 5 to 7): all three SQL versions agreed (`[]`, `[]`, `[5, 6, 7]`).
- Unsorted input: window `ORDER BY` handles it; pandas sorts first.
- Duplicate seat ids cannot occur with the primary key; if the real table has them, dedupe first (not tested here).
- A `free` column stored as text `'1'` does not equal integer 1 in the join; keep the type clean.
- In pandas, `shift(-1, fill_value=False)` keeps the boolean dtype; a plain `shift()` on an integer column would give float with NaN.

**Then explain:**
- Self join: simple, quadratic in the worst case (it is an index lookup on `seat_id`, in practice fast); needs `DISTINCT` because a seat in the middle of a run matches twice.
- `LAG`/`LEAD`: one pass; remember it is row-based, so it is only correct if ids are consecutive or you check them.
- Islands: the one that generalises to "at least N consecutive free seats" (change `>= 2` to `>= N`), which is what LeetCode 601 style questions ask.
- The three agree on this data. Which to show first? The self join, because it reads like the statement; then say why `LAG`/`LEAD` needs the id check.
- Dialects, not executed here: the `ABS` self join runs on MySQL and PostgreSQL unchanged; the other two need window functions (MySQL 8 and later). I did not execute them.

**Follow-ups:**
- At least three consecutive free seats? Island version with `HAVING COUNT(*) >= 3`, or `LAG`/`LEAD` twice.
- Return the runs (start seat, end seat, length) instead of seat ids? `GROUP BY grp` with `MIN`, `MAX`, `COUNT`.
- What if seats are in rows and columns? Partition by row.

**Common mistakes:**
- `LAG`/`LEAD` without checking the id gap (shown above: seat 11 appears).
- Forgetting `DISTINCT` in the self join.
- Using the island trick without filtering to free seats first, so taken seats get row numbers and the group sizes change.
- Treating NULL as free, or comparing `free` as text.
- Ordering by anything other than `seat_id`.

### Q19 ⭐⭐ 🟢 Missing dates against a date spine: logins(user_id, login_date) over 2024-03-01 to 2024-03-10. Return for each user the days in the range with no login, building the spine with a recursive CTE (a pointer to Part 9) and a CROSS JOIN of users with the spine LEFT JOINed to logins, plus the compact form as missing ranges. Explain why the NOT EXISTS version and the LEFT JOIN with IS NULL version give the same rows, and the effect of a user with no logins at all.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Build a date spine for the range, `CROSS JOIN` it with the users to get every (user, day) pair that should exist, `LEFT JOIN` the logins and keep the rows where nothing matched; the compact form numbers the missing days per user and groups them with the same date-minus-`ROW_NUMBER` island trick.

**Schema and sample data:** a `users` table (4 users) and a `logins` table, range 2024-03-01 to 2024-03-10 (10 days). User 1 logged in on 01, 02 (twice), 03, 06, 07, 10 (inserted unsorted), so missing are 04, 05, 08, 09. User 2 has no logins at all. User 3 logged in all ten days. User 4 has one in-range login (03-05), two out-of-range logins (02-28 and 03-11) and a NULL date.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1),(2),(3),(4);
INSERT INTO logins VALUES
 (1,'2024-03-06'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-03'),(1,'2024-03-07'),(1,'2024-03-10'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-04'),(3,'2024-03-05'),
 (3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-08'),(3,'2024-03-09'),(3,'2024-03-10'),
 (4,'2024-03-05'),(4,'2024-02-28'),(4,'2024-03-11'),(4,NULL);
```

**SQL answer:** `SQL_LEFT` in the Code block, the date spine as a recursive CTE (it runs on SQLite 3.45.1; recursive CTEs in depth are Part 9) and the anti-join:
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
WHERE l.user_id IS NULL
ORDER BY u.user_id, s.d
```
`SQL_NOTEXISTS` in the Code block is the same with a `NOT EXISTS` subquery:
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
WHERE NOT EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.user_id AND l.login_date = s.d)
ORDER BY u.user_id, s.d
```
The compact form, `SQL_RANGES` in the Code block (the missing days become the "rows" for the island trick):
```sql
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
), m AS (
  SELECT u.user_id, s.d AS missing_date
  FROM users u
  CROSS JOIN spine s
  LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
  WHERE l.user_id IS NULL
), g AS (
  SELECT user_id, missing_date,
         date(missing_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY missing_date) || ' days') AS grp
  FROM m
)
SELECT user_id, MIN(missing_date) AS range_start, MAX(missing_date) AS range_end, COUNT(*) AS days_missing
FROM g
GROUP BY user_id, grp
ORDER BY user_id, range_start
```

**pandas answer:** shown once here and identical to the Code block (`date_range` is the spine, `from_product` the cross join, `merge(..., indicator=True)` plus `left_only` the anti-join):
```py
spine = pd.date_range("2024-03-01", "2024-03-10", freq="D")
grid = pd.MultiIndex.from_product([users["user_id"], spine], names=["user_id", "d"]).to_frame(index=False)
seen = logins.dropna(subset=["login_date"]).assign(d=lambda x: pd.to_datetime(x["login_date"]))[["user_id", "d"]].drop_duplicates()
m = grid.merge(seen, on=["user_id", "d"], how="left", indicator=True)
miss = m[m["_merge"] == "left_only"][["user_id", "d"]].sort_values(["user_id", "d"]).reset_index(drop=True)
miss["grp"] = (miss["d"] - pd.Timestamp("1970-01-01")).dt.days - miss.groupby("user_id").cumcount()
ranges = (miss.groupby(["user_id", "grp"], as_index=False)
              .agg(range_start=("d", "min"), range_end=("d", "max"), days_missing=("d", "size"))
              .drop(columns="grp"))
```

**Example:** user 1 in the spine of 10 days has logins on 01, 02, 03, 06, 07, 10, so the unmatched days are 04, 05, 08, 09. Numbering them 1, 2, 3, 4 and subtracting from the day: 04-1, 05-2 are the same group (consecutive), 08-3, 09-4 are the same group, different from the first. Ranges: 04 to 05 (2 days) and 08 to 09 (2 days). User 2: all 10 days missing, one range 03-01 to 03-10. User 3: none. User 4: only 03-05 matched, so ranges 03-01 to 03-04 (4 days) and 03-06 to 03-10 (5 days). The out-of-range dates and the NULL never match a spine day.

**Code:** run with `python3 -I`. The asserts compare the `LEFT JOIN` and `NOT EXISTS` results (equal frames), then pandas with SQL, ordered by `user_id, missing_date` (and `user_id, range_start` for ranges).
```python
# Q19: missing dates against a date spine (2024-03-01 to 2024-03-10), anti-join forms, compact ranges
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1),(2),(3),(4);
INSERT INTO logins VALUES
 (1,'2024-03-06'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-03'),(1,'2024-03-07'),(1,'2024-03-10'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-04'),(3,'2024-03-05'),
 (3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-08'),(3,'2024-03-09'),(3,'2024-03-10'),
 (4,'2024-03-05'),(4,'2024-02-28'),(4,'2024-03-11'),(4,NULL);
"""
SQL_LEFT = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
WHERE l.user_id IS NULL
ORDER BY u.user_id, s.d
"""
SQL_NOTEXISTS = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
WHERE NOT EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.user_id AND l.login_date = s.d)
ORDER BY u.user_id, s.d
"""
SQL_RANGES = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
), m AS (
  SELECT u.user_id, s.d AS missing_date
  FROM users u
  CROSS JOIN spine s
  LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
  WHERE l.user_id IS NULL
), g AS (
  SELECT user_id, missing_date,
         date(missing_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY missing_date) || ' days') AS grp
  FROM m
)
SELECT user_id, MIN(missing_date) AS range_start, MAX(missing_date) AS range_end, COUNT(*) AS days_missing
FROM g
GROUP BY user_id, grp
ORDER BY user_id, range_start
"""
# traps
SQL_NOTIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u CROSS JOIN spine s
WHERE s.d NOT IN (SELECT l.login_date FROM logins l WHERE l.user_id = u.user_id)
ORDER BY u.user_id, s.d
"""
SQL_USERS_FROM_LOGINS = SQL_LEFT.replace("FROM users u", "FROM (SELECT DISTINCT user_id FROM logins) u")
assert SQL_USERS_FROM_LOGINS != SQL_LEFT

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_LEFT, con)
b = pd.read_sql_query(SQL_NOTEXISTS, con)
pd.testing.assert_frame_equal(a, b)
print("missing days per user (LEFT JOIN ... IS NULL), counts:", a.groupby("user_id").size().to_dict())
print(a.groupby("user_id")["missing_date"].apply(lambda s: ",".join(x[8:] for x in s)).to_string())
print("NOT EXISTS gives the same rows: True")
r = pd.read_sql_query(SQL_RANGES, con)
print("compact missing ranges:"); print(r.to_string(index=False))
n = pd.read_sql_query(SQL_NOTIN, con)
print("NOT IN with a NULL login_date: user_ids returned =", sorted(n.user_id.unique().tolist()),
      "(user 4 has a NULL date and vanishes)")
w = pd.read_sql_query(SQL_USERS_FROM_LOGINS, con)
print("user list taken from logins: user_ids returned =", sorted(w.user_id.unique().tolist()), "(user 2 vanishes)")

logins = pd.read_sql_query("SELECT * FROM logins", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
spine = pd.date_range("2024-03-01", "2024-03-10", freq="D")
grid = pd.MultiIndex.from_product([users["user_id"], spine], names=["user_id", "d"]).to_frame(index=False)
seen = logins.dropna(subset=["login_date"]).assign(d=lambda x: pd.to_datetime(x["login_date"]))[["user_id", "d"]].drop_duplicates()
m = grid.merge(seen, on=["user_id", "d"], how="left", indicator=True)
miss = m[m["_merge"] == "left_only"][["user_id", "d"]].sort_values(["user_id", "d"]).reset_index(drop=True)
miss["grp"] = (miss["d"] - pd.Timestamp("1970-01-01")).dt.days - miss.groupby("user_id").cumcount()
ranges = (miss.groupby(["user_id", "grp"], as_index=False)
              .agg(range_start=("d", "min"), range_end=("d", "max"), days_missing=("d", "size"))
              .drop(columns="grp"))
# pd:end
p_miss = miss.assign(missing_date=miss["d"].dt.strftime("%Y-%m-%d"))[["user_id", "missing_date"]]
pd.testing.assert_frame_equal(p_miss, a, check_dtype=False)   # ordered by user_id, missing_date
for c in ("range_start", "range_end"):
    ranges[c] = ranges[c].dt.strftime("%Y-%m-%d")
pd.testing.assert_frame_equal(ranges.sort_values(["user_id", "range_start"]).reset_index(drop=True), r, check_dtype=False)
print("pandas equals SQL (missing days ordered by user_id, missing_date; ranges by user_id, range_start): True")
print("asserts passed")
```

**Output (my run):**
```text
missing days per user (LEFT JOIN ... IS NULL), counts: {1: 4, 2: 10, 4: 9}
user_id
1                      04,05,08,09
2    01,02,03,04,05,06,07,08,09,10
4       01,02,03,04,06,07,08,09,10
NOT EXISTS gives the same rows: True
compact missing ranges:
 user_id range_start  range_end  days_missing
       1  2024-03-04 2024-03-05             2
       1  2024-03-08 2024-03-09             2
       2  2024-03-01 2024-03-10            10
       4  2024-03-01 2024-03-04             4
       4  2024-03-06 2024-03-10             5
NOT IN with a NULL login_date: user_ids returned = [1, 2] (user 4 has a NULL date and vanishes)
user list taken from logins: user_ids returned = [1, 4] (user 2 vanishes)
pandas equals SQL (missing days ordered by user_id, missing_date; ranges by user_id, range_start): True
asserts passed
```

**Edge cases:**
- Duplicate logins (user 1, 03-02 twice): in the anti-join they only make matched pairs appear twice, and matched pairs are thrown away, so the missing rows are unaffected. They would matter for a count of logins per day, not here.
- A user with no logins at all (user 2): comes out with all 10 days, but only because the user list comes from the `users` table. In my run, taking the user list from `SELECT DISTINCT user_id FROM logins` made user 2 vanish (only users 1 and 4 returned). If there is no users table, the "who should be here" question has to be answered from somewhere else.
- A user with all days (user 3): no rows, which is correct and easy to miss when you look for the user in the output.
- Out-of-range dates (02-28, 03-11) are ignored because they match no spine day; the spine limits the range.
- NULL `login_date` (user 4): matches no spine day, so it does no harm in `LEFT JOIN ... IS NULL` or `NOT EXISTS`. With `NOT IN (subquery)` it is poison: `d NOT IN (..., NULL)` is never true, so user 4's rows disappeared in my run (only users 1 and 2 returned).
- Anti-join test column: check a column that is never NULL when matched (`l.user_id`), not a nullable one; testing a nullable column would drop true matches whose value is NULL.
- Unsorted input: irrelevant for the anti-join; the island step sorts.
- Spine boundaries: the recursive condition `d < '2024-03-10'` stops after generating 03-10, so the end date is included; checking that the spine has 10 rows is cheap insurance.
- Time zones and timestamps: if `login_date` came from a timestamp it must be converted to the user's local date first; not covered here.

**Then explain:**
- Why `NOT EXISTS` and `LEFT JOIN ... IS NULL` give the same rows: both keep exactly the (user, day) pairs for which no login row has that user and that day. The join form creates a NULL-padded row when there is no match; the other form asks directly if one exists. A duplicate matched row cannot add a missing row, and the unmatched side is padded exactly once.
- Where they can differ in general: a join that multiplies rows (duplicate matches) changes counts after the join, but not the set of unmatched rows; `NOT IN` is different because of NULL (shown above).
- Spine versus window: `LAG` finds gaps only between existing logins (Q20); the spine finds all missing days including before the first and after the last login, and users with no logins at all.
- Pointer: the recursive CTE spine is explained in depth in Part 9; the alternative is a calendar table. Engine-specific spine generators (`generate_series` in PostgreSQL, `GENERATE_DATE_ARRAY` in BigQuery) are from memory and not executed here.

**Follow-ups:**
- Only users who missed at least one day, or the day count per user? Group the result by user.
- Range crossing the user's signup date (days before signup are not missing)? If `users` had a `signup_date` column (this one does not), add `s.d >= u.signup_date` to the cross join.
- A longer range, such as a year? I only ran the 10 day spine; for a long range a stored calendar table is the usual alternative (not benchmarked here).

**Common mistakes:**
- `NOT IN` with a nullable subquery.
- Building the user list from the logins table and losing users with no activity.
- Putting the date filter in the `WHERE` instead of the `ON` clause of the `LEFT JOIN`, which turns it into an inner join.
- Off-by-one on the spine end date.
- Testing a nullable column for `IS NULL` after the join.

### Q20 ⭐⭐ 🟡 Gaps between consecutive dates larger than one day: logins(user_id, login_date). For each user list every gap as gap_start (the first missing day), gap_end (the last missing day) and days_missing using LEAD or LAG with julianday difference > 1, and also the longest break between two logins per user. Explain the NULL on the last row of each partition, the threshold meaning of exactly 1 day apart (no gap) versus exactly 2 (one missing day), and a user with a single login.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Deduplicate the login days, use `LEAD` to get each user's next login date, and call it a gap when the next date is more than 1 day later; the first missing day is the login date plus 1, the last missing day is the next date minus 1, and the number of missing days is the difference minus 1.

**Definitions I use:** a gap is a stretch of calendar days with no login between two logins of the same user; `days_missing` counts the missing days (so logins on 03-02 and 03-04 leave 1 missing day). "Longest break" is the largest `days_missing` for a user; the days between the two logins is that number plus 1. Say which one you mean; I report the missing-days form and 0 for a user with no gap.

**Schema and sample data:** twelve rows, four users, unsorted. User 1: 03-01, 03-02, 03-04 (twice), 03-10. User 2: a single login (03-05). User 3: three consecutive days, no gap. User 4: 03-01, a NULL date, 03-03. Dates are ISO text.
```sql
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-10'),(1,'2024-03-04'),(1,'2024-03-01'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-05'),
 (3,'2024-03-03'),(3,'2024-03-01'),(3,'2024-03-02'),
 (4,'2024-03-01'),(4,NULL),(4,'2024-03-03');
```

**SQL answer:** `SQL_GAPS` in the Code block:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
)
SELECT user_id,
       date(login_date, '+1 day') AS gap_start,
       date(next_date, '-1 day') AS gap_end,
       CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
FROM x
WHERE julianday(next_date) - julianday(login_date) > 1
ORDER BY user_id, gap_start
```
Longest break per user, `SQL_LONGEST` in the Code block, with a `LEFT JOIN` from all users so users without a gap show 0:
```sql
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
), gaps AS (
  SELECT user_id, CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
  FROM x
  WHERE julianday(next_date) - julianday(login_date) > 1
)
SELECT u.user_id, COALESCE(MAX(g.days_missing), 0) AS longest_break_days
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN gaps g ON g.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
```

**pandas answer:** shown once here and identical to the Code block (`shift(-1)` is `LEAD`):
```py
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
d["next_date"] = d.groupby("user_id")["login_date"].shift(-1)
d["diff_days"] = (d["next_date"] - d["login_date"]).dt.days
g = d[d["diff_days"] > 1]
gaps = pd.DataFrame({
    "user_id": g["user_id"],
    "gap_start": (g["login_date"] + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "gap_end": (g["next_date"] - pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "days_missing": (g["diff_days"] - 1).astype(int),
}).reset_index(drop=True)
longest = (gaps.groupby("user_id")["days_missing"].max()
               .reindex(logins["user_id"].drop_duplicates().sort_values()).fillna(0).astype(int)
               .rename("longest_break_days").reset_index())
```

**Example:** user 1 distinct sorted days: 03-01, 03-02, 03-04, 03-10; next dates: 03-02, 03-04, 03-10, none; differences: 1, 2, 6, NULL.
- 1 day apart (03-01 to 03-02): consecutive days, no gap, filtered out.
- 2 days apart (03-02 to 03-04): one missing day, so `gap_start = 03-03`, `gap_end = 03-03`, `days_missing = 1`.
- 6 days apart (03-04 to 03-10): 03-05 to 03-09, `days_missing = 5`.
- The last row has no next date, so its difference is NULL and it is not a gap.
- Longest break for user 1 is 5. User 4: 03-01 and 03-03 give one gap, 03-02, so longest 1. Users 2 and 3: no gap, longest 0.

**Code:** run with `python3 -I`. The asserts compare pandas with SQL for the gap list (ordered by `user_id, gap_start`) and the longest break (ordered by `user_id`). The printed `NaN` in the detail table is pandas showing SQL NULL.
```python
# Q20: gaps larger than one day between consecutive logins, and the longest break per user
import sqlite3
import datetime as dt
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-10'),(1,'2024-03-04'),(1,'2024-03-01'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-05'),
 (3,'2024-03-03'),(3,'2024-03-01'),(3,'2024-03-02'),
 (4,'2024-03-01'),(4,NULL),(4,'2024-03-03');
"""
SQL_GAPS = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
)
SELECT user_id,
       date(login_date, '+1 day') AS gap_start,
       date(next_date, '-1 day') AS gap_end,
       CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
FROM x
WHERE julianday(next_date) - julianday(login_date) > 1
ORDER BY user_id, gap_start
"""
SQL_LONGEST = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
), gaps AS (
  SELECT user_id, CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
  FROM x
  WHERE julianday(next_date) - julianday(login_date) > 1
)
SELECT u.user_id, COALESCE(MAX(g.days_missing), 0) AS longest_break_days
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN gaps g ON g.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
"""
SQL_DETAIL = """
SELECT user_id, login_date,
       LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date,
       julianday(LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date)) - julianday(login_date) AS diff_days
FROM (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL)
ORDER BY user_id, login_date
"""
# no dedupe, to see what duplicates do
SQL_NODEDUP = SQL_GAPS.replace("SELECT DISTINCT user_id, login_date", "SELECT user_id, login_date")
assert SQL_NODEDUP != SQL_GAPS

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("LEAD detail (diff_days is NULL on each user's last row):"); print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
a = pd.read_sql_query(SQL_GAPS, con)
print("gaps:"); print(a.to_string(index=False))
l = pd.read_sql_query(SQL_LONGEST, con)
print("longest break (most missing days in a row between two logins; 0 if none):"); print(l.to_string(index=False))
nd = pd.read_sql_query(SQL_NODEDUP, con)
print("without DISTINCT the gap rows are the same as with it:", nd.equals(a))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
d["next_date"] = d.groupby("user_id")["login_date"].shift(-1)
d["diff_days"] = (d["next_date"] - d["login_date"]).dt.days
g = d[d["diff_days"] > 1]
gaps = pd.DataFrame({
    "user_id": g["user_id"],
    "gap_start": (g["login_date"] + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "gap_end": (g["next_date"] - pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "days_missing": (g["diff_days"] - 1).astype(int),
}).reset_index(drop=True)
longest = (gaps.groupby("user_id")["days_missing"].max()
               .reindex(logins["user_id"].drop_duplicates().sort_values()).fillna(0).astype(int)
               .rename("longest_break_days").reset_index())
# pd:end
pd.testing.assert_frame_equal(gaps, a, check_dtype=False)        # ordered by user_id, gap_start
pd.testing.assert_frame_equal(longest, l, check_dtype=False)     # ordered by user_id
print("pandas equals SQL for gaps and longest break: True")

# julianday on whole dates: exact? compare with unixepoch over 20000 date pairs
rows, base = [], dt.date(2000, 1, 1)
for i in range(20000):
    x = base + dt.timedelta(days=i * 3)
    y = x + dt.timedelta(days=1 + i % 400)
    rows.append((x.isoformat(), y.isoformat()))
con.execute("CREATE TABLE pairs(a TEXT, b TEXT)")
con.executemany("INSERT INTO pairs VALUES (?, ?)", rows)
print(con.execute("SELECT COUNT(*), SUM(julianday(b) - julianday(a) = CAST(julianday(b) - julianday(a) AS INTEGER)), "
                  "SUM((unixepoch(b) - unixepoch(a)) % 86400 = 0), "
                  "SUM(julianday(b) - julianday(a) = (unixepoch(b) - unixepoch(a)) / 86400) FROM pairs").fetchone(),
      "<- pairs, julianday diff is a whole number, unixepoch diff is whole days, the two agree")
print("asserts passed")
```

**Output (my run):**
```text
LEAD detail (diff_days is NULL on each user's last row):
 user_id login_date  next_date  diff_days
       1 2024-03-01 2024-03-02        1.0
       1 2024-03-02 2024-03-04        2.0
       1 2024-03-04 2024-03-10        6.0
       1 2024-03-10        NaN        NaN
       2 2024-03-05        NaN        NaN
       3 2024-03-01 2024-03-02        1.0
       3 2024-03-02 2024-03-03        1.0
       3 2024-03-03        NaN        NaN
       4 2024-03-01 2024-03-03        2.0
       4 2024-03-03        NaN        NaN
gaps:
 user_id  gap_start    gap_end  days_missing
       1 2024-03-03 2024-03-03             1
       1 2024-03-05 2024-03-09             5
       4 2024-03-02 2024-03-02             1
longest break (most missing days in a row between two logins; 0 if none):
 user_id  longest_break_days
       1                   5
       2                   0
       3                   0
       4                   1
without DISTINCT the gap rows are the same as with it: True
pandas equals SQL for gaps and longest break: True
(20000, 20000, 20000, 20000) <- pairs, julianday diff is a whole number, unixepoch diff is whole days, the two agree
asserts passed
```

**Edge cases:**
- NULL on the last row of each partition: `LEAD` has no next row, so `next_date` is NULL, the difference is NULL, and `NULL > 1` is NULL, which `WHERE` treats as not true, so the last row drops out. That is the wanted behaviour, but it is the NULL logic doing it, not a deliberate filter; in pandas, `NaT` gives a NaN `diff_days` and `NaN > 1` is `False` for the same effect.
- Exactly 1 day apart means consecutive days, no day missing, so the filter is `> 1`, not `>= 1`. Exactly 2 days apart means one missing day, which is why `days_missing` is the difference minus 1; mixing these up is the classic off-by-one.
- Single login (user 2): one row, `LEAD` is NULL, no gap; in the longest-break result it shows 0 because of the `LEFT JOIN` and `COALESCE`, it is not missing.
- Duplicate dates: I dedupe first. In my run, removing the `DISTINCT` gave the same gap rows (the tied rows have a difference of 0, and the second copy still carries the real next date), so it did not create false gaps here; it would matter for any count of days or logins, and for `LAG`/`LEAD` pairs where you test equality, so I still dedupe.
- NULL date (user 4): removed in the first CTE; without it, the NULL row sorts first in SQLite (it is smaller than any text) and distorts the LEAD pairs.
- Unsorted input: handled by the window `ORDER BY`.
- `julianday` on whole dates is fine: in my run over 20000 date pairs the difference was always an exact whole number and equal to the `unixepoch` difference divided by 86400 (unlike timestamps with times in Q11, where `julianday * 1440` came out slightly off). I still wrap it in `ROUND` before the `CAST` because the cast truncates.
- Only users with 2 or more logins can have a gap; the user with one login contributes no row to the gap list.
- The break before the first login and after the last (relative to a period) is not a gap between two logins; use a date spine (Q19) for those.

**Then explain:**
- `LEAD` looks at the next row, `LAG` at the previous one; the gap logic is the same, just anchored on the other row (with `LAG`, `gap_start` is `date(prev_date, '+1 day')` and `gap_end` is `date(login_date, '-1 day')`). Both need the days deduped and sorted.
- Why `julianday` here: a date has no time part, so day differences are exact; for timestamps use `unixepoch` (Q11).
- The threshold: difference of 1 is "yesterday to today" and has nothing in between; every difference above 1 has `difference - 1` missing days.
- Dialects, not executed here: PostgreSQL date subtraction `next_date - login_date` returns an integer number of days; MySQL `DATEDIFF(next_date, login_date)`; BigQuery `DATE_DIFF(next_date, login_date, DAY)`. I did not run these.

**Follow-ups:**
- Gaps larger than 7 days (churn-style)? Change the threshold to `> 7` in the same query.
- The first and last gaps in a fixed period, not just between logins? Use the date spine and the missing ranges from Q19.
- Average time between logins? `AVG(julianday(next_date) - julianday(login_date))` over the same rows including the 1 day differences, not only the gaps.

**Common mistakes:**
- `>= 1` instead of `> 1`, or forgetting the minus 1 in `days_missing`.
- Not deduplicating or not filtering NULL dates.
- Using `LAG`/`LEAD` without `PARTITION BY user_id`, so the first login of a user looks like it follows another user's last login.
- Treating the NULL on the last row as an error and filling it with today's date.
- Reporting 0 for a one-login user as if it were missing data, or leaving it out without saying so.
