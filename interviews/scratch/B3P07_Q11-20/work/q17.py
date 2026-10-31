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
