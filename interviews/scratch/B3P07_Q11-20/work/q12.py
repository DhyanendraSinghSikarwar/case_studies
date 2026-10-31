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
