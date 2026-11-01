# Q29: concurrent sessions peak via the +1/-1 sweep in SQL and pandas; ties at the same timestamp
import sqlite3
import pandas as pd

AS_OF = "2024-03-01 12:30:00"
SCHEMA = """
CREATE TABLE sessions(user_id INTEGER, login_ts TEXT, logout_ts TEXT);
INSERT INTO sessions VALUES
 (3,'2024-03-01 10:00:00','2024-03-01 11:00:00'),
 (1,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (2,'2024-03-01 09:30:00','2024-03-01 10:30:00'),
 (4,'2024-03-01 10:00:00','2024-03-01 10:15:00'),
 (7,'2024-03-01 09:00:00','2024-03-01 10:00:00'),
 (5,'2024-03-01 12:00:00',NULL),
 (6,'2024-03-01 13:00:00','2024-03-01 13:00:00');
"""
SQL_MAIN = """
WITH ev AS (
  SELECT login_ts AS ts, 1 AS delta FROM sessions
  UNION ALL
  SELECT COALESCE(logout_ts, '2024-03-01 12:30:00') AS ts, -1 AS delta FROM sessions
), r AS (
  SELECT ts, delta,
         SUM(delta) OVER (ORDER BY ts, delta
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS concurrent
  FROM ev
)
SELECT (SELECT MAX(concurrent) FROM r) AS peak,
       (SELECT MIN(ts) FROM r WHERE concurrent = (SELECT MAX(concurrent) FROM r)) AS first_reached
"""
SQL_STARTS_FIRST = SQL_MAIN.replace("ORDER BY ts, delta\n", "ORDER BY ts, delta DESC\n")
SQL_TSONLY_ROWS = SQL_MAIN.replace("ORDER BY ts, delta\n", "ORDER BY ts\n")
SQL_TSONLY_RANGE = SQL_MAIN.replace("ORDER BY ts, delta\n", "ORDER BY ts\n").replace("ROWS BETWEEN", "RANGE BETWEEN")
SQL_TRACE = SQL_MAIN.split("SELECT (SELECT MAX")[0] + "SELECT ts, delta, concurrent FROM r ORDER BY ts, delta"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("event trace (ends before starts at equal timestamps):")
print(pd.read_sql_query(SQL_TRACE, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL peak:")
print(sql_df.to_string(index=False))
print("wrong, starts before ends at ties (ORDER BY ts, delta DESC):", con.execute(SQL_STARTS_FIRST).fetchone())
print("ORDER BY ts only with ROWS frame (arbitrary tie order):", con.execute(SQL_TSONLY_ROWS).fetchone())
print("ORDER BY ts only with the default-style RANGE frame (ties netted together):", con.execute(SQL_TSONLY_RANGE).fetchone())

sessions = pd.read_sql_query("SELECT * FROM sessions", con)
def peak_pandas(sessions, as_of=AS_OF, sort_cols=("ts", "delta"), concat_order=("start", "end"), kind=None):
    # pd:main
    logout = sessions["logout_ts"].fillna(as_of)
    starts = pd.DataFrame({"ts": pd.to_datetime(sessions["login_ts"]), "delta": 1})
    ends = pd.DataFrame({"ts": pd.to_datetime(logout), "delta": -1})
    parts = {"start": starts, "end": ends}
    ev = pd.concat([parts[k] for k in concat_order], ignore_index=True)
    ev = ev.sort_values(list(sort_cols), **({"kind": kind} if kind else {})).reset_index(drop=True)
    ev["concurrent"] = ev["delta"].cumsum()
    peak = int(ev["concurrent"].max())
    first_reached = ev.loc[ev["concurrent"] == peak, "ts"].min()
    # pd:end
    return peak, first_reached.strftime("%Y-%m-%d %H:%M:%S")
peak, first = peak_pandas(sessions)
print("pandas peak:", peak, first)
assert (peak, first) == (int(sql_df["peak"][0]), sql_df["first_reached"][0])  # scalar result, no row order
# ties: sorting by time alone depends on the input order of the concatenated frames
print("sort by ts only, stable, starts concatenated first:", peak_pandas(sessions, sort_cols=("ts",), concat_order=("start", "end"), kind="stable"))
print("sort by ts only, stable, ends concatenated first:", peak_pandas(sessions, sort_cols=("ts",), concat_order=("end", "start"), kind="stable"))
print("sort by ts only, default kind, starts first:", peak_pandas(sessions, sort_cols=("ts",), concat_order=("start", "end")))
print("sort by ts, delta, either concat order:", peak_pandas(sessions, concat_order=("start", "end")), peak_pandas(sessions, concat_order=("end", "start")))
# edge cases: empty and single row
one = sessions.iloc[:1]
print("single session:", peak_pandas(one))
print("asserts passed")
