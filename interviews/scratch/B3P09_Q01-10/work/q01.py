# Q1: how WITH RECURSIVE executes: counter 1..5, round-by-round queue, stop rule, guards, forbidden constructs
import sqlite3
import pandas as pd

SQL_MAIN = """
WITH RECURSIVE counter(n) AS (
  SELECT 1                                  -- anchor member
  UNION ALL
  SELECT n + 1 FROM counter WHERE n < 5     -- recursive member
)
SELECT n FROM counter ORDER BY n
"""
SQL_NO_STOP = """
WITH RECURSIVE counter(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM counter            -- no WHERE: never returns an empty round
)
SELECT n FROM counter LIMIT 8          -- the outer LIMIT is what makes this demo terminate
"""
SQL_DEPTH_CAP = """
WITH RECURSIVE counter(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM counter LIMIT 8    -- LIMIT inside the recursive select (SQLite allows it)
)
SELECT n FROM counter
"""

con = sqlite3.connect(":memory:")
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL result:", sql_df["n"].tolist())

# Round by round: run the same two SELECTs by hand on a one-table working set.
con.execute("CREATE TABLE work(n INTEGER)")
con.execute("INSERT INTO work SELECT 1")                      # round 0: the anchor member runs once
rounds = [[r[0] for r in con.execute("SELECT n FROM work")]]
while True:
    new = [r[0] for r in con.execute("SELECT n + 1 FROM work WHERE n < 5")]   # recursive member on the previous round only
    if not new:                                               # empty round: recursion stops
        break
    con.execute("DELETE FROM work")
    con.executemany("INSERT INTO work VALUES (?)", [(v,) for v in new])
    rounds.append(new)
for i, r in enumerate(rounds):
    print(f"round {i}: working table = {r}  ->  recursive member returns {[v + 1 for v in r if v < 5]}")

# pandas: the same loop with a frontier DataFrame
# pd:main
frontier = pd.DataFrame({"n": [1]})
frames = [frontier]
while not frontier.empty:
    frontier = frontier[frontier["n"] < 5].assign(n=lambda d: d["n"] + 1)
    if not frontier.empty:
        frames.append(frontier)
pd_df = pd.concat(frames, ignore_index=True)
# pd:end
flat = [v for r in rounds for v in r]
assert flat == pd_df["n"].tolist() == sql_df["n"].tolist() == [1, 2, 3, 4, 5]   # compared after ORDER BY n

# What if WHERE n < 5 is removed (bounded demos only)
print("no stop, outer LIMIT 8:", [r[0] for r in con.execute(SQL_NO_STOP)])
print("no stop, LIMIT inside the recursive select:", [r[0] for r in con.execute(SQL_DEPTH_CAP)])

# Rules for the recursive member: what SQLite 3.45.1 says
bad = {
 "aggregate": "WITH RECURSIVE c(n) AS (SELECT 1 UNION ALL SELECT max(n) + 1 FROM c WHERE n < 5) SELECT n FROM c",
 "window":    "WITH RECURSIVE c(n) AS (SELECT 1 UNION ALL SELECT row_number() OVER () + n FROM c WHERE n < 5) SELECT n FROM c",
 "two refs":  "WITH RECURSIVE c(n) AS (SELECT 1 UNION ALL SELECT a.n + b.n FROM c a JOIN c b WHERE a.n < 5) SELECT n FROM c",
 "recursive first": "WITH RECURSIVE c(n) AS (SELECT n + 1 FROM c WHERE n < 5 UNION ALL SELECT 1) SELECT n FROM c",
}
for k, q in bad.items():
    try:
        con.execute(q).fetchall(); print(k, "-> ran")
    except sqlite3.Error as e:
        print(f"{k} -> error: {e}")

# Row order: only the outer ORDER BY guarantees it
print("outer ORDER BY 1 DESC:", [r[0] for r in con.execute(SQL_MAIN.replace("ORDER BY n", "ORDER BY 1 DESC"))])
# Edge cases: empty anchor, and WITH without the RECURSIVE keyword
print("empty anchor:", con.execute("WITH RECURSIVE c(n) AS (SELECT 1 WHERE 0 UNION ALL SELECT n + 1 FROM c WHERE n < 5) SELECT n FROM c").fetchall())
print("anchor only (stop rule false at once):", con.execute("WITH RECURSIVE c(n) AS (SELECT 9 UNION ALL SELECT n + 1 FROM c WHERE n < 5) SELECT n FROM c").fetchall())
print("without the RECURSIVE keyword on SQLite:", con.execute("WITH c(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM c WHERE n < 5) SELECT count(*) FROM c").fetchone()[0], "rows")
print("asserts passed")
