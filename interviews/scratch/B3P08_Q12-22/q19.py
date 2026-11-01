# Q19: reconcile two DAU numbers for 2024-03-05, one cause at a time
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE identity_map(alias_id INTEGER, user_id INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts_utc TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','IN',0),(4,'2024-01-01','IN',0),
 (5,'2024-01-01','IN',0),(6,'2024-01-01','IN',0),(7,'2024-01-01','IN',1),(8,'2024-01-01','IN',1),
 (9,'2024-01-01','IN',0);
INSERT INTO identity_map VALUES (101,1),(102,3);
INSERT INTO events VALUES
 (1,'2024-03-05 04:00:00','open'),
 (2,'2024-03-05 05:00:00','heartbeat'),(2,'2024-03-05 05:30:00','heartbeat'),
 (3,'2024-03-05 06:00:00','click'),
 (4,'2024-03-05 20:00:00','click'),
 (5,'2024-03-04 19:00:00','click'),
 (7,'2024-03-05 07:00:00','open'),
 (101,'2024-03-05 08:00:00','open'),
 (102,'2024-03-05 09:00:00','click'),
 (6,'2024-03-05 12:00:00','click'),(6,'2024-03-05 13:00:00','click'),
 (8,'2024-03-05 10:00:00','heartbeat'),
 (9,'2024-03-05 22:00:00','click');
"""

# parameters: :day (local day), :tz_min (0 = UTC day, 330 = IST day), :excl_test, :intent_only, :merge
SQL_MAIN = """
WITH ev AS (
  SELECT CASE WHEN :merge = 1 THEN COALESCE(m.user_id, e.user_id) ELSE e.user_id END AS uid,
         e.event_name,
         date(datetime(e.event_ts_utc, '+' || :tz_min || ' minutes')) AS d
  FROM events e
  LEFT JOIN identity_map m ON m.alias_id = e.user_id
)
SELECT COUNT(*) AS events, COUNT(DISTINCT ev.uid) AS users
FROM ev
LEFT JOIN users u ON u.user_id = ev.uid
WHERE ev.d = :day
  AND (:excl_test = 0 OR COALESCE(u.is_test, 0) = 0)
  AND (:intent_only = 0 OR ev.event_name <> 'heartbeat')
"""

BASE = dict(day="2024-03-05", tz_min=0, excl_test=0, intent_only=0, merge=0)
CUM = [
    ("growth dashboard: UTC day, every event, raw ids, test users in", {}),
    ("+ exclude test users", {"excl_test": 1}),
    ("+ intent events only (drop heartbeat)", {"intent_only": 1}),
    ("+ merge alias ids (identity_map)", {"merge": 1}),
    ("+ IST day instead of UTC day (finance definition)", {"tz_min": 330}),
]
ALONE = [("UTC day only", {}), ("IST day only", {"tz_min": 330}), ("excl test only", {"excl_test": 1}),
         ("intent only", {"intent_only": 1}), ("merge ids only", {"merge": 1})]

# pd:main
def pd_dau(events, users, idmap, day, tz_min, excl_test, intent_only, merge):
    e = events.merge(idmap, left_on="user_id", right_on="alias_id", how="left", suffixes=("", "_m"))
    e["uid"] = e["user_id_m"].fillna(e["user_id"]) if merge == 1 else e["user_id"]
    e["d"] = (pd.to_datetime(e["event_ts_utc"]) + pd.Timedelta(minutes=tz_min)).dt.strftime("%Y-%m-%d")
    e = e.merge(users[["user_id", "is_test"]].rename(columns={"user_id": "uid"}), on="uid", how="left")
    e["is_test"] = e["is_test"].fillna(0)
    e = e[e["d"] == day]
    if excl_test == 1:
        e = e[e["is_test"] == 0]
    if intent_only == 1:
        e = e[e["event_name"] != "heartbeat"]
    return len(e), e["uid"].nunique()
# pd:end

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
users = pd.read_sql_query("SELECT * FROM users", con)
idmap = pd.read_sql_query("SELECT * FROM identity_map", con)
events = pd.read_sql_query("SELECT * FROM events", con)

def run(change):
    p = {**BASE, **change}
    s = con.execute(SQL_MAIN, p).fetchone()
    q = pd_dau(events, users, idmap, **p)
    assert s == q, (change, s, q)
    return s

cum, acc, rows = [], {}, []
for name, change in CUM:
    acc.update(change)
    ev_n, us_n = run(acc)
    rows.append({"step (cumulative)": name, "events": ev_n, "users": us_n})
print(pd.DataFrame(rows).to_string(index=False))
base_users = run({})[1]
rows = []
for name, change in ALONE:
    ev_n, us_n = run(change)
    rows.append({"one change from the growth definition": name, "events": ev_n, "users": us_n, "delta_users": us_n - base_users})
print(pd.DataFrame(rows).to_string(index=False))
print("sum of the four single-cause deltas:", sum(r["delta_users"] for r in rows[1:]),
      "| actual cumulative gap:", run({})[1] - run({"excl_test": 1, "intent_only": 1, "merge": 1, "tz_min": 330})[1])
print("who is active on the IST day:", sorted(r[0] for r in con.execute(
    "SELECT DISTINCT COALESCE(m.user_id, e.user_id) FROM events e LEFT JOIN identity_map m ON m.alias_id = e.user_id "
    "LEFT JOIN users u ON u.user_id = COALESCE(m.user_id, e.user_id) "
    "WHERE date(datetime(e.event_ts_utc,'+330 minutes')) = '2024-03-05' AND COALESCE(u.is_test,0)=0 AND e.event_name <> 'heartbeat'")))
print("asserts passed")
