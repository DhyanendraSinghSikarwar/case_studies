# Book 3 — Part 9: Recursive CTEs, hierarchies and graphs in SQL, with pandas equivalents

**Topic:** WITH RECURSIVE syntax, anchor and recursive member, termination, UNION versus UNION ALL and cycles, depth counters and per-engine limits (SQLite LIMIT, MySQL cte_max_recursion_depth, SQL Server MAXRECURSION, PostgreSQL CYCLE and SEARCH, Oracle CONNECT BY, hedged); number and date series; toy recursion (factorial, Fibonacci, powers); employee-manager hierarchies (all reports, chain of command, level, path strings, leaf and root, org-size roll-ups); bill of materials with quantity multiplication; category trees and breadcrumbs; graph reachability, connected components, friends of friends, degrees of separation, flight routes with total cost and shortest paths with cycle guards; topological order of dependencies; state-dependent running calculations (reset by threshold, compound interest, loan amortisation, EWMA, depreciation); recursive CTE versus self-join and window alternatives; storage models (adjacency list, materialized path, nested sets, closure table); deleting and moving subtrees; cycle, orphan and multiple-root detection; performance and safety; and the pandas counterparts (iterative merges, while-loop frontiers, groupby and transform roll-ups, explode for paths, plain-Python BFS and DFS, networkx as a check).
**Target:** 30  |  **Actual:** 30 (⭐⭐⭐ 12, ⭐⭐ 11, ⭐ 7)  |  **Date:** 2026-10-25  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers recursion in SQL and its pandas and plain-Python counterparts. Generic window functions belong to Parts 4 and 5, gaps, islands and sessionization to Part 7 (Q24 there defers the threshold-reset running total to this part), calendar tables and cohorts to Part 6 (Q31 there builds a calendar table with a recursive CTE; the date-series question here points to it and does not repeat it), and graph algorithm libraries are out of scope beyond a library check. Every question states its tables so Wave B can build sample data; keep trees small enough to verify by hand.

Evidence limits: no candidate-reported SQL questions were found. Sources are official documentation (SQLite lang_with, PostgreSQL WITH queries and MySQL 8.4 recursive CTE pages, all opened), guides (jdsatpathy manager-chain article, DataVidhya recursive hierarchy page, LeetCode 1270 on the doocs mirror, all opened) and search snippets only (SQL Server MAXRECURSION threads, Oracle hierarchical query docs, storage-model blogs, threshold-reset forum threads, datadriven.io, Medium and a 300-questions LinkedIn guide). leetcode.com pages were not opened. 'Asked at' tags are source types, not company reports. Environment (checked by running): SQLite 3.45.1 supports WITH RECURSIVE, LIMIT in the recursive select, ORDER BY as queue order, and power, exp and ln here; it does not support the CYCLE or SEARCH clauses (syntax error), has no generate_series without an extension, and rejects a second reference to the CTE in the recursive member, including inside a subquery (error: multiple recursive references). networkx 3.6.1 is installed; scipy and duckdb are not. All other engines are hedged as not executed.

---

### Q1 ⭐⭐⭐ 🟢 How a recursive CTE executes: explain WITH RECURSIVE step by step using counter(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM counter WHERE n < 5). Name the anchor member and the recursive member, describe what the working table (queue) holds at each round, why the recursion stops (the recursive member returns no rows), what happens if the WHERE n < 5 is removed, and the rules the recursive member must follow (self-reference once, no aggregates or window functions in SQLite and MySQL). Show the round-by-round rows on this example and the same engine words for PostgreSQL (working table, intermediate table) and SQLite (queue). Say which row order is guaranteed (none without ORDER BY on the outer query).
**Asked at:** SQLite lang_with documentation (opened: compound SELECT with a non-recursive initial select, UNION discards rows already queued and stops cycles, UNION ALL needs little memory, LIMIT on the recursive select, ORDER BY in the recursive select as queue order for breadth-first or depth-first, no aggregates or windows in the recursive select, queue algorithm) plus PostgreSQL WITH queries documentation (opened: working table and intermediate table evaluation); official documentation, not candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** A recursive CTE is a loop: the anchor member runs once and seeds a queue, then the recursive member runs on the rows of the previous round only, adds what it returns to the result and the queue, and the whole thing stops the first time a round returns no rows; remove `WHERE n < 5` and a round never comes back empty, so it never stops.

**Schema and sample data:** no table is needed; the anchor is the constant 1. (The later questions use real tables.)

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
WITH RECURSIVE counter(n) AS (
  SELECT 1                                  -- anchor member
  UNION ALL
  SELECT n + 1 FROM counter WHERE n < 5     -- recursive member
)
SELECT n FROM counter ORDER BY n
```
- Anchor member: `SELECT 1`. It does not mention `counter`, runs once, and produces round 0.
- Recursive member: `SELECT n + 1 FROM counter WHERE n < 5`. Here `counter` means only the rows added in the previous round, not the whole result so far.
- The two parts are joined by `UNION ALL` (or `UNION`).

**pandas answer:** the same loop with a frontier DataFrame, identical to the Code block:
```py
frontier = pd.DataFrame({"n": [1]})
frames = [frontier]
while not frontier.empty:
    frontier = frontier[frontier["n"] < 5].assign(n=lambda d: d["n"] + 1)
    if not frontier.empty:
        frames.append(frontier)
pd_df = pd.concat(frames, ignore_index=True)
```

**Example:** the round-by-round table, taken from the real run (the Code block replays the same two SELECTs by hand on a one-row working table).

| Round | Rows the recursive member reads (working table) | Rows it returns | Rows in result so far |
|---|---|---|---|
| 0 (anchor) | none, the anchor runs once | 1 | 1 |
| 1 | 1 | 2 | 1, 2 |
| 2 | 2 | 3 | 1, 2, 3 |
| 3 | 3 | 4 | 1 to 4 |
| 4 | 4 | 5 | 1 to 5 |
| 5 | 5 (fails `n < 5`) | nothing | 1 to 5, stop |

- Why it stops: round 5 returns zero rows. The engine does not look at the result or count rounds; an empty round is the only stop signal.
- Without `WHERE n < 5`: the stop test is gone, every round returns one row, and the query runs until memory, a row limit, a timer or an engine recursion limit stops it. In my run a bounded demo (outer `LIMIT 8`, or `LIMIT 8` inside the recursive select) returns 1 to 8 and then stops.
- Terminology: SQLite calls the working set a queue (a row is taken out, the recursive member runs on it, new rows are added). PostgreSQL's documentation describes a working table (the previous round) and an intermediate table (the new round, where `UNION` discards duplicates) that replaces it. Same idea, different words; I read both pages, I did not run PostgreSQL.
- Row order: none is guaranteed. SQLite happened to return 1 to 5 in queue order, but only the outer `ORDER BY` is a promise (the run shows `ORDER BY 1 DESC` giving 5 to 1).

**Code:** run with `python3 -I`. The assert compares the manual round replay, the pandas loop and the SQL result as lists ordered by `n`; the bad queries are caught and their real SQLite error messages are printed.
```python
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
```

**Output (my run):**
```text
SQL result: [1, 2, 3, 4, 5]
round 0: working table = [1]  ->  recursive member returns [2]
round 1: working table = [2]  ->  recursive member returns [3]
round 2: working table = [3]  ->  recursive member returns [4]
round 3: working table = [4]  ->  recursive member returns [5]
round 4: working table = [5]  ->  recursive member returns []
no stop, outer LIMIT 8: [1, 2, 3, 4, 5, 6, 7, 8]
no stop, LIMIT inside the recursive select: [1, 2, 3, 4, 5, 6, 7, 8]
aggregate -> error: recursive aggregate queries not supported
window -> error: cannot use window functions in recursive queries
two refs -> error: multiple references to recursive table: c
recursive first -> error: circular reference: c
outer ORDER BY 1 DESC: [5, 4, 3, 2, 1]
empty anchor: []
anchor only (stop rule false at once): [(9,)]
without the RECURSIVE keyword on SQLite: 5 rows
asserts passed
```

**Edge cases:**
- Empty anchor (`SELECT 1 WHERE 0`): the queue starts empty, the recursive member never runs, the result is empty (printed `[]`).
- Anchor already fails the stop test (`SELECT 9 ... WHERE n < 5`): you still get the anchor row, 9, and nothing else. The stop condition is checked only in the recursive member, never against the anchor.
- `UNION ALL` versus `UNION`: `UNION` also drops a row that was already produced, which is the cycle protection discussed in Q7.
- Rules in SQLite 3.45.1, each verified by running: an aggregate in the recursive member gives `recursive aggregate queries not supported`; a window function gives `cannot use window functions in recursive queries`; a second reference to `counter` gives `multiple references to recursive table: c` (a self-join of the CTE is the usual way to hit it); a recursive select placed first gives `circular reference: c`. MySQL also forbids `GROUP BY`, `ORDER BY` and `DISTINCT` in the recursive part (opened documentation, not executed). The rule lists for other engines are from documentation only, not executed.
- SQLite accepted `WITH c(n) AS (...)` without the `RECURSIVE` keyword (5 rows). MySQL requires `RECURSIVE`; SQL Server writes plain `WITH` and does not accept `RECURSIVE` (documentation and search snippets, not executed). Write `WITH RECURSIVE` where the engine allows it.

**Then explain:**
- Two parts: an anchor member (no self-reference) and a recursive member (references the CTE once). Anchor first, then rounds.
- The recursive member sees only the previous round. That is why a running value has to be carried as a column (Q3).
- Termination is an empty round. Your job is to make an empty round inevitable: a `WHERE` on a growing value, a visited check, or a depth cap.
- Engine guards are a second line of defence, not a design: SQLite `LIMIT` in the recursive select, MySQL `cte_max_recursion_depth` (default 1000) and `max_execution_time`, SQL Server `MAXRECURSION` (default 100), all hedged, not executed here.
- Aggregates and windows go outside the CTE, in the final `SELECT`.

**Follow-ups:**
- Does the recursive member see the whole result so far? No, only the last round (the working table); the result is the union of all rounds.
- Is the order of rows guaranteed? No. Add `ORDER BY` on the outer query.
- How do you stop a runaway query while testing? An outer `LIMIT` in SQLite (shown above), or a depth column with `WHERE depth < N`.

**Common mistakes:**
- Putting the stop condition in the anchor or only in the outer query. The outer `WHERE n < 5` filters rows after the fact, but the recursion would still run forever; it must be in the recursive member.
- Thinking `UNION ALL` is "union of all rows so far". It only concatenates rounds.
- Using an aggregate such as `max(n)` in the recursive member to "carry the maximum".
- Relying on the order SQLite happens to return.

### Q2 ⭐⭐⭐ 🟢 Number series and calendar spine: sales(sale_date, amount) with gaps (no rows on some days between 2024-03-01 and 2024-03-10). Generate the integers 1 to 10 and then every date in the range with a recursive CTE (SQLite date(d, '+1 day')), LEFT JOIN sales to return one row per day with 0 for missing days, and the seven-day moving total on the filled series. State why the stop condition is on the date, what changes in MySQL (date + INTERVAL 1 DAY, cte_max_recursion_depth default 1000 for long ranges), PostgreSQL generate_series and SQL Server (MAXRECURSION default 100), all not executed, and point to Part 6 Q31 (calendar table) and the pandas pd.date_range equivalent with reindex.
**Asked at:** MySQL 8.4 recursive CTE documentation (opened: WITH RECURSIVE keyword, cte_max_recursion_depth default 1000, max_execution_time, LIMIT inside the recursive part, no aggregates, window functions, GROUP BY, ORDER BY or DISTINCT in the recursive part, column types fixed by the anchor, Fibonacci, date series and employee path examples) plus SQL Server MAXRECURSION search snippets (default 100, Msg 530, range 0 to 32767, hint on the outer statement, not opened); documentation and community answers, not candidate reports; analyst and data engineer rounds on MySQL and SQL Server stacks
**Say this first (1 line):** Generate the days with a recursive CTE that starts at the first date and adds `date(d, '+1 day')` until the last date, LEFT JOIN the daily sales onto that spine (summed per day first) with `COALESCE(..., 0)` for empty days, and take the seven-day total as a `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` sum over the filled series, because only a filled series makes "6 rows back" mean "6 days back".

**Schema and sample data:** nine sales rows on purpose messy: two rows on 03-02, a day (03-07) whose only amount is NULL, two rows outside the range (02-28 and 03-12), and no rows on 03-03, 03-05, 03-06 and 03-09. Dates are ISO text.
```sql
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('2024-02-28', 999),
 ('2024-03-01', 100),
 ('2024-03-02', 50), ('2024-03-02', 25),
 ('2024-03-04', 200),
 ('2024-03-07', NULL),
 ('2024-03-08', 70),
 ('2024-03-10', 30),
 ('2024-03-12', 500);
```

**SQL answer:** two queries in the Code block. First the integers 1 to 10 (`SQL_NUMS`):
```sql
WITH RECURSIVE nums(n) AS (
  SELECT 1 UNION ALL SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n FROM nums
```
Then the calendar spine and the moving total (`SQL_MAIN`, with `:start` and `:stop` bound to 2024-03-01 and 2024-03-10):
```sql
WITH RECURSIVE spine(d) AS (
  SELECT :start WHERE :start <= :stop
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < :stop
), daily AS (
  SELECT sale_date AS d, SUM(amount) AS amt FROM sales GROUP BY sale_date
)
SELECT spine.d AS day,
       COALESCE(daily.amt, 0) AS amount,
       SUM(COALESCE(daily.amt, 0)) OVER (ORDER BY spine.d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS total_7d
FROM spine LEFT JOIN daily ON daily.d = spine.d
ORDER BY spine.d
```
- The stop test is on the date (`d < :stop`), not on a count of rows: the recursion has to end because the date reached the end of the range, and then the number of days is whatever the range says. Writing `d <= :stop` would add one extra day (the recursive member adds a day after the test passes), and a stop on a row count would silently break when the range changes.
- The anchor has `WHERE :start <= :stop`, otherwise a reversed range returns one wrong row (checked below).
- Sales are summed per day in `daily` before the join. Joining raw rows would give two rows for 03-02 and break the moving total.

**pandas answer:** `pd.date_range` is the spine and `reindex` is the LEFT JOIN, identical to the Code block:
```py
days = pd.date_range("2024-03-01", "2024-03-10")
daily = (sales.assign(sale_date=pd.to_datetime(sales["sale_date"]))
              .groupby("sale_date")["amount"].sum())
filled = daily.reindex(days, fill_value=0).fillna(0)
pd_df = pd.DataFrame({"day": days.strftime("%Y-%m-%d"), "amount": filled.to_numpy(),
                      "total_7d": filled.rolling(7, min_periods=1).sum().to_numpy()})
```

**Example:** the 7-day window of day D is the seven rows D-6 to D (fewer at the start).
- Day sums after the join: 03-01 100, 03-02 75 (50 plus 25), 03-03 0, 03-04 200, 03-05 to 03-07 0 (03-07 had only a NULL amount: `SUM` of NULL is NULL, `COALESCE` makes it 0), 03-08 70, 03-09 0, 03-10 30.
- Running totals: 03-01 100; 03-02 175; 03-03 175; 03-04 375; 03-05 to 03-07 375.
- 03-08: window 03-02 to 03-08 is 75 + 0 + 200 + 0 + 0 + 0 + 70 = 345 (03-01 has dropped out).
- 03-09: window 03-03 to 03-09 is 0 + 200 + 70 = 270. 03-10: window 03-04 to 03-10 is 200 + 70 + 30 = 300.
- The 02-28 and 03-12 rows never appear because the spine is the range, and a join starting from the spine cannot add days.

**Code:** run with `python3 -I`. The assert compares SQL and pandas on all three columns after ordering by day; dtypes are not compared (SQL integers, pandas floats from the NULL).
```python
# Q2: number series and calendar spine with a recursive CTE, LEFT JOIN, 7-day moving total; pandas date_range + reindex
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('2024-02-28', 999),                       -- outside the range
 ('2024-03-01', 100),
 ('2024-03-02', 50), ('2024-03-02', 25),    -- two rows on one day
 ('2024-03-04', 200),
 ('2024-03-07', NULL),                      -- a day whose only amount is NULL
 ('2024-03-08', 70),
 ('2024-03-10', 30),
 ('2024-03-12', 500);                       -- outside the range
"""
SQL_NUMS = """
WITH RECURSIVE nums(n) AS (
  SELECT 1 UNION ALL SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n FROM nums
"""
SQL_MAIN = """
WITH RECURSIVE spine(d) AS (
  SELECT :start WHERE :start <= :stop
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < :stop
), daily AS (
  SELECT sale_date AS d, SUM(amount) AS amt FROM sales GROUP BY sale_date
)
SELECT spine.d AS day,
       COALESCE(daily.amt, 0) AS amount,
       SUM(COALESCE(daily.amt, 0)) OVER (ORDER BY spine.d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS total_7d
FROM spine LEFT JOIN daily ON daily.d = spine.d
ORDER BY spine.d
"""
P = {"start": "2024-03-01", "stop": "2024-03-10"}
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("integers:", [r[0] for r in con.execute(SQL_NUMS)])
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
days = pd.date_range("2024-03-01", "2024-03-10")
daily = (sales.assign(sale_date=pd.to_datetime(sales["sale_date"]))
              .groupby("sale_date")["amount"].sum())
filled = daily.reindex(days, fill_value=0).fillna(0)
pd_df = pd.DataFrame({"day": days.strftime("%Y-%m-%d"), "amount": filled.to_numpy(),
                      "total_7d": filled.rolling(7, min_periods=1).sum().to_numpy()})
# pd:end
pd.testing.assert_frame_equal(pd_df.reset_index(drop=True), sql_df, check_dtype=False)   # both ordered by day
print("pandas equals SQL (ordered by day)")

# Edge cases
r = con.execute(SQL_MAIN, {"start": "2024-03-10", "stop": "2024-03-01"}).fetchall()
print("start after stop with the anchor guard:", r)
r = con.execute(SQL_MAIN.replace("SELECT :start WHERE :start <= :stop", "SELECT :start"), {"start": "2024-03-10", "stop": "2024-03-01"}).fetchall()
print("start after stop WITHOUT the guard: rows =", len(r), "first =", r[0])
print("single day range:", con.execute(SQL_MAIN, {"start": "2024-03-04", "stop": "2024-03-04"}).fetchall())
print("bad date text '2024-3-1' through date():", con.execute("SELECT date('2024-3-1')").fetchone())
con.execute("DELETE FROM sales")
empty = con.execute(SQL_MAIN, P).fetchall()
print("empty sales: rows =", len(empty), "all zero =", all(a == 0 and t == 0 for _, a, t in empty))
print("asserts passed")
```

**Output (my run):**
```text
integers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
       day  amount  total_7d
2024-03-01     100       100
2024-03-02      75       175
2024-03-03       0       175
2024-03-04     200       375
2024-03-05       0       375
2024-03-06       0       375
2024-03-07       0       375
2024-03-08      70       345
2024-03-09       0       270
2024-03-10      30       300
pandas equals SQL (ordered by day)
start after stop with the anchor guard: []
start after stop WITHOUT the guard: rows = 1 first = ('2024-03-10', 30, 30)
single day range: [('2024-03-04', 200, 200)]
bad date text '2024-3-1' through date(): (None,)
empty sales: rows = 10 all zero = True
asserts passed
```

**Edge cases:**
- Reversed range: with the anchor guard the result is empty (`[]`); without it SQLite returned one row (`2024-03-10`), because an anchor always emits its row.
- Single-day range: one row, 03-04 with 200.
- Empty `sales`: all 10 days still come out, every amount and total 0. That is the point of the spine.
- NULL amounts: summed per day then `COALESCE`d, so they count as 0. pandas `groupby().sum()` also gives 0 for an all-NaN day (`min_count` default 0), so the two agree here; `SUM` over an all-NULL group in SQL is NULL, so the `COALESCE` matters.
- Bad date text: `date('2024-3-1')` returned NULL in SQLite, so the next `d < :stop` is NULL and the recursion ends early with no error. Check the input format.
- The first six days have partial windows. If the product wants only full 7-day windows, show NULL until the seventh row (in pandas `min_periods=7`).
- Timestamps instead of dates in `sale_date` would not match `daily.d`; cut them with `date(sale_ts)` first (not executed here).

**Then explain:**
- The spine is the left side; facts are joined to it. Gaps become 0 rather than missing rows.
- Other engines, all not executed here: MySQL 8 uses `d + INTERVAL 1 DAY` inside `WITH RECURSIVE` and stops at `cte_max_recursion_depth` (default 1000) on a long range, so a three-year daily spine needs the variable raised. SQL Server uses `DATEADD(day, 1, d)` without the word `RECURSIVE` and stops at `MAXRECURSION` (default 100) unless you add `OPTION (MAXRECURSION 0)` (0 means no limit) at the end of the outer statement. PostgreSQL has `generate_series('2024-03-01'::date, '2024-03-10', '1 day')`, no recursion needed. SQLite 3.45.1 has no `generate_series` here (checked: no such table).
- For a reusable spine, build a physical calendar table once; Part 6 Q31 builds that calendar table with the recursive CTE and the holiday join, so I do not repeat it here.
- In pandas, `reindex(days, fill_value=0)` after `groupby` is the whole idea; `asfreq("D")` and `resample("D").sum()` are other ways to get the same filled series.

**Follow-ups:**
- Why `ROWS` and not `RANGE`? On a gap-free series they agree; with the spine in place `ROWS 6 PRECEDING` is exactly seven calendar days. On the raw gappy table it would be seven rows, not seven days, which is the bug the spine fixes.
- How do you generate a spine for 10 years in MySQL? Raise `cte_max_recursion_depth` for the session, or use a calendar table.
- How would you also get months with no sales? Spine of month starts, same pattern (`date(d, '+1 month')`).

**Common mistakes:**
- Moving total on the raw table: seven rows is not seven days.
- Joining raw sales to the spine and getting two rows for a day with two sales.
- Filtering `WHERE sale_date BETWEEN ...` on the right-hand table after a LEFT JOIN, which removes the empty days again.
- Stopping on `d <= :stop` and getting an extra day, or forgetting the range guard.
- Letting a NULL amount turn the day's total into NULL.

### Q3 ⭐⭐⭐ 🟢 Toy recursion with carried state: with a recursive CTE produce (a) n and n! for n from 1 to 10, (b) the first 15 Fibonacci numbers using columns (n, fib, next_fib), (c) powers of 2 up to 2^20, and (d) the digits of a number split into rows. Explain why state is carried as extra columns (a recursive member sees only the previous row, not the history), what happens when the factorial grows past the 64-bit integer range in SQLite (it turns into a float) and in other engines (overflow error or exact numerics, hedged, not executed), and that these are teaching problems, not production uses. Include the pandas or Python loop check with asserts.
**Asked at:** MySQL 8.4 recursive CTE documentation (opened: WITH RECURSIVE keyword, cte_max_recursion_depth default 1000, max_execution_time, LIMIT inside the recursive part, no aggregates, window functions, GROUP BY, ORDER BY or DISTINCT in the recursive part, column types fixed by the anchor, Fibonacci, date series and employee path examples) plus SQL Server MAXRECURSION search snippets (default 100, Msg 530, range 0 to 32767, hint on the outer statement, not opened); documentation and community answers, not candidate reports; analyst and data engineer rounds on MySQL and SQL Server stacks
**Say this first (1 line):** The recursive member only sees the previous row, so any history it needs (the running product, the previous Fibonacci number, the remaining digits) has to travel as extra columns in every row; and in SQLite integer arithmetic that overflows 64 bits silently turns into a REAL (floating point) number, which I verified by running factorial to 40, so these are teaching problems, not production tools.

**Schema and sample data:** no tables; every query starts from constants. The digits query takes the number as a parameter (`:num`, 90210 in the main run).

**SQL answer:** four queries in the Code block (`SQL_FACT`, `SQL_FIB`, `SQL_POW`, `SQL_DIGITS`):
```sql
WITH RECURSIVE f(n, fact) AS (
  SELECT 1, 1
  UNION ALL
  SELECT n + 1, fact * (n + 1) FROM f WHERE n < 10
)
SELECT n, fact FROM f ORDER BY n
```
```sql
WITH RECURSIVE fib(n, fib, next_fib) AS (
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib, fib + next_fib FROM fib WHERE n < 15
)
SELECT n, fib FROM fib ORDER BY n
```
```sql
WITH RECURSIVE p(e, val) AS (
  SELECT 0, 1
  UNION ALL
  SELECT e + 1, val * 2 FROM p WHERE e < 20
)
SELECT e, val FROM p ORDER BY e
```
```sql
WITH RECURSIVE d(pos, rest, digit) AS (
  SELECT 1, abs(:num) / 10, abs(:num) % 10          -- anchor: the last digit, so 0 still gives one row
  UNION ALL
  SELECT pos + 1, rest / 10, rest % 10 FROM d WHERE rest > 0
)
SELECT pos, digit FROM d ORDER BY pos DESC          -- pos 1 is the last digit; DESC reads left to right
```
- Factorial: the carried column is `fact`; row n+1 is `fact * (n + 1)`.
- Fibonacci: the row is `(n, fib, next_fib)`. To compute the next number I need two earlier values, but the member sees only one row, so the row carries both. The new row is `(n + 1, next_fib, fib + next_fib)`, a shift by one.
- Powers of 2: `val * 2` per round, 21 rows for exponents 0 to 20.
- Digits: `rest / 10` and `rest % 10` (integer division in SQLite truncates for integers). Position 1 is the last digit, so I sort by `pos DESC` to read left to right. The anchor already emits the last digit, so the number 0 still returns one row.

**pandas answer:** plain Python loops and `math.factorial` as the check, identical to the Code block:
```py
n = pd.Series(range(1, 11))
pd_fact = pd.DataFrame({"n": n, "fact": [math.factorial(int(k)) for k in n]})
fibs = [0, 1]
while len(fibs) < 15:
    fibs.append(fibs[-1] + fibs[-2])
pd_fib = pd.DataFrame({"n": range(1, 16), "fib": fibs})
pd_pow = pd.DataFrame({"e": range(21), "val": [2 ** k for k in range(21)]})
pd_dig = pd.DataFrame({"pos": range(5, 0, -1), "digit": [int(c) for c in str(90210)]})
```

**Example:**
- Factorial: (1, 1), (2, 2), (3, 6), (4, 24), (5, 120) ... (10, 3628800). Each row is the previous `fact` times the new n.
- Fibonacci rows `(n, fib, next_fib)`: (1, 0, 1), (2, 1, 1), (3, 1, 2), (4, 2, 3), (5, 3, 5) ... so the first 15 values are 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377.
- Digits of 90210: anchor (pos 1, rest 9021, digit 0); then (2, 902, 1), (3, 90, 2), (4, 9, 0), (5, 0, 9); `rest > 0` fails for the last row and the recursion ends. Reading `pos DESC` gives 9, 0, 2, 1, 0.
- Powers: 1, 2, 4, ... 2^20 = 1048576.

**Code:** run with `python3 -I`. The asserts compare each SQL result with the plain Python result as frames ordered as in the SQL `ORDER BY`; the overflow section prints `typeof` and compares with Python's exact big integers.
```python
# Q3: toy recursion with carried state: factorial, Fibonacci, powers of 2, digits; overflow behaviour in SQLite
import math
import sqlite3
import pandas as pd

SQL_FACT = """
WITH RECURSIVE f(n, fact) AS (
  SELECT 1, 1
  UNION ALL
  SELECT n + 1, fact * (n + 1) FROM f WHERE n < 10
)
SELECT n, fact FROM f ORDER BY n
"""
SQL_FIB = """
WITH RECURSIVE fib(n, fib, next_fib) AS (
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib, fib + next_fib FROM fib WHERE n < 15
)
SELECT n, fib FROM fib ORDER BY n
"""
SQL_POW = """
WITH RECURSIVE p(e, val) AS (
  SELECT 0, 1
  UNION ALL
  SELECT e + 1, val * 2 FROM p WHERE e < 20
)
SELECT e, val FROM p ORDER BY e
"""
SQL_DIGITS = """
WITH RECURSIVE d(pos, rest, digit) AS (
  SELECT 1, abs(:num) / 10, abs(:num) % 10          -- anchor: the last digit, so 0 still gives one row
  UNION ALL
  SELECT pos + 1, rest / 10, rest % 10 FROM d WHERE rest > 0
)
SELECT pos, digit FROM d ORDER BY pos DESC          -- pos 1 is the last digit; DESC reads left to right
"""
con = sqlite3.connect(":memory:")
sql_fact = pd.read_sql_query(SQL_FACT, con)
sql_fib = pd.read_sql_query(SQL_FIB, con)
sql_pow = pd.read_sql_query(SQL_POW, con)
sql_dig = pd.read_sql_query(SQL_DIGITS, con, params={"num": 90210})
print("factorial:", dict(zip(sql_fact["n"], sql_fact["fact"])))
print("fibonacci:", sql_fib["fib"].tolist())
print("powers of 2:", sql_pow["val"].tolist()[:6], "...", sql_pow["val"].iloc[-1])
print("digits of 90210 left to right:", sql_dig["digit"].tolist())

# pd:main
n = pd.Series(range(1, 11))
pd_fact = pd.DataFrame({"n": n, "fact": [math.factorial(int(k)) for k in n]})
fibs = [0, 1]
while len(fibs) < 15:
    fibs.append(fibs[-1] + fibs[-2])
pd_fib = pd.DataFrame({"n": range(1, 16), "fib": fibs})
pd_pow = pd.DataFrame({"e": range(21), "val": [2 ** k for k in range(21)]})
pd_dig = pd.DataFrame({"pos": range(5, 0, -1), "digit": [int(c) for c in str(90210)]})
# pd:end
pd.testing.assert_frame_equal(pd_fact, sql_fact, check_dtype=False)   # all four compared in the SQL ORDER BY order
pd.testing.assert_frame_equal(pd_fib, sql_fib, check_dtype=False)
pd.testing.assert_frame_equal(pd_pow, sql_pow, check_dtype=False)
pd.testing.assert_frame_equal(pd_dig, sql_dig, check_dtype=False)

# Edge cases for digits: 0 and a negative number
print("digits of 0:", [r[1] for r in con.execute(SQL_DIGITS, {"num": 0})], "| of -705:", [r[1] for r in con.execute(SQL_DIGITS, {"num": -705})])

# Overflow: run factorial to 25 and Fibonacci to 95 and watch typeof()
big = con.execute("""
WITH RECURSIVE f(n, fact) AS (SELECT 1, 1 UNION ALL SELECT n + 1, fact * (n + 1) FROM f WHERE n < 40)
SELECT n, typeof(fact), fact, printf('%.0f', fact) FROM f WHERE n IN (19, 20, 21, 22, 25, 30, 40)""").fetchall()
for n_, t, v, s in big:
    exact = math.factorial(n_)
    print(f"n={n_}: typeof={t}, value={v!r}, digits equal exact n!: {int(v) == exact}")
print("max signed 64-bit integer:", 2 ** 63 - 1, "| 20! =", math.factorial(20), "| 21! =", math.factorial(21))
fibx = [0, 1]
while len(fibx) < 100:
    fibx.append(fibx[-1] + fibx[-2])
fibt = con.execute("""
WITH RECURSIVE fib(n, a, b) AS (SELECT 1, 0, 1 UNION ALL SELECT n + 1, b, a + b FROM fib WHERE n < 95)
SELECT n, typeof(a), a FROM fib WHERE n IN (92, 93, 94, 95)""").fetchall()
for n_, t, v in fibt:
    print(f"row n={n_} holds F({n_ - 1}): typeof={t}, value={v!r}, exact={fibx[n_ - 1]}")
# integer overflow outside recursion
print("9223372036854775807 + 1 =", con.execute("SELECT 9223372036854775807 + 1, typeof(9223372036854775807 + 1)").fetchone())
# Python loop check against SQL to n=25 (relative tolerance once SQLite switches to float)
rows = con.execute("WITH RECURSIVE f(n, fact) AS (SELECT 1, 1 UNION ALL SELECT n + 1, fact * (n + 1) FROM f WHERE n < 25) SELECT n, fact FROM f").fetchall()
for n_, v in rows:
    assert math.isclose(float(v), float(math.factorial(n_)), rel_tol=1e-12)
    if n_ <= 20:
        assert v == math.factorial(n_)
print("asserts passed")
```

**Output (my run):**
```text
factorial: {1: 1, 2: 2, 3: 6, 4: 24, 5: 120, 6: 720, 7: 5040, 8: 40320, 9: 362880, 10: 3628800}
fibonacci: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
powers of 2: [1, 2, 4, 8, 16, 32] ... 1048576
digits of 90210 left to right: [9, 0, 2, 1, 0]
digits of 0: [0] | of -705: [7, 0, 5]
n=19: typeof=integer, value=121645100408832000, digits equal exact n!: True
n=20: typeof=integer, value=2432902008176640000, digits equal exact n!: True
n=21: typeof=real, value=5.109094217170944e+19, digits equal exact n!: True
n=22: typeof=real, value=1.1240007277776077e+21, digits equal exact n!: True
n=25: typeof=real, value=1.5511210043330986e+25, digits equal exact n!: False
n=30: typeof=real, value=2.6525285981219103e+32, digits equal exact n!: False
n=40: typeof=real, value=8.159152832478977e+47, digits equal exact n!: False
max signed 64-bit integer: 9223372036854775807 | 20! = 2432902008176640000 | 21! = 51090942171709440000
row n=92 holds F(91): typeof=integer, value=4660046610375530309, exact=4660046610375530309
row n=93 holds F(92): typeof=integer, value=7540113804746346429, exact=7540113804746346429
row n=94 holds F(93): typeof=real, value=1.2200160415121877e+19, exact=12200160415121876738
row n=95 holds F(94): typeof=real, value=1.9740274219868226e+19, exact=19740274219868223167
9223372036854775807 + 1 = (9.223372036854776e+18, 'real')
asserts passed
```

**Edge cases:**
- Overflow in SQLite (run): `fact` is an integer up to 20! = 2432902008176640000 (below 9223372036854775807). 21! is returned as a REAL (`5.109094217170944e+19`), not an error. 21! and 22! still match the exact value digit for digit (they have many factors of 2, so a double holds them exactly), but 25!, 30! and 40! do not (`digits equal exact n!: False`): the float has lost the low digits. So the dangerous part is that nothing fails; the type quietly changes and the numbers become approximate.
- Fibonacci overflows later: F(92) fits as an integer, F(93) = 12200160415121876738 comes back as a REAL (`1.2200160415121877e+19`, not exact). A plain `SELECT 9223372036854775807 + 1` also returns a REAL in my run.
- Other engines, from memory and not executed: PostgreSQL `bigint` would raise "bigint out of range" and `numeric` is exact for large values; MySQL integer overflow raises an out-of-range error for `BIGINT` in strict mode; SQL Server raises an arithmetic overflow error. In all of these the fix is to cast the anchor to a wide exact type (for example `CAST(1 AS DECIMAL(38,0))` or `NUMERIC`), because the column type is fixed by the anchor in MySQL and SQL Server. MySQL's documentation (opened) says exactly that about anchor types.
- Digits of 0 return `[0]`; of -705 return `[7, 0, 5]` because of `abs()`. Without `abs`, `%` of a negative number returns a negative digit (`-705 % 10` is -5 in SQLite, checked).
- Stop conditions here are on the data (`n < 10`, `rest > 0`), so no guard is needed; still, a typo that drops the `WHERE` makes all four endless.

**Then explain:**
- State in columns: the member sees one previous row, so a "memory" is an extra column. Two-back history means carry two values.
- This is why a recursive CTE can express things a window cannot (Q12, Q18, Q19), and why these toy queries are still loops: one row per iteration.
- Production use: almost none for factorial or Fibonacci; the shapes carry over to running balances, compound interest and spines.
- Exactness: decide up front whether the number must be exact. If yes, use a decimal type or do it outside SQL.

**Follow-ups:**
- Why not `SELECT fib FROM fib WHERE n < 15` with a window `LAG`? A window sees stored columns, not values that depend on the previous output row.
- Do you ever do this for real? Not for factorials; the same carried-state shape is used for running balances (Q18) and spines (Q2).
- How do you get the digits in the original order? Carry the string, or sort by `pos DESC` as above.

**Common mistakes:**
- Trying to reference two earlier rows (`fib` of n-1 and n-2) by joining the CTE twice: SQLite rejects a second reference (see Q1), so carry both values in one row.
- Trusting a large factorial printed by SQL without checking `typeof`.
- Leaving out the `abs` or the zero case in digit splitting.
- Forgetting that `/` on two integers is integer division in SQLite (it truncates), but a division by a REAL is not.

### Q4 ⭐⭐⭐ 🟢 All reports under a manager: employees(emp_id, manager_id, name, salary) where the CEO has manager_id NULL. Return everyone who reports to manager 3 directly or indirectly, with their level below that manager (1 for direct reports). This is the general form of LeetCode 1270 (all people who report to the head, directly or indirectly, with at most three levels). Show the recursive CTE, the fixed two- or three-join version that works only for known depth, and why the recursive version needs no change when the org gets deeper. State whether the starting manager should appear in the output.
**Asked at:** LeetCode 1270 All People Report to the Given Manager (doocs mirror opened: head is employee 1, chain at most three managers, two self-joins; the 'given manager' framing at Hello Interview and DataVidhya seen only as search snippets, so a general version is an expert extension); public problem bank, not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Anchor on the direct reports of the manager (`manager_id = 3`, level 1), then join `employees` to the CTE on `e.manager_id = sub.emp_id` with level + 1, and the query stops by itself when a row has no reports; the fixed two- or three-join version gives the same answer only up to its built-in depth, and I leave the starting manager out of the output (level 1 means direct report) unless the interviewer wants him as level 0.

**Schema and sample data:** thirteen employees. Tim (1) is the CEO with a NULL manager. Hari (3) manages Ben (5) and Chen (6). Ben manages Dev (7) and Esha (8); Chen manages Farid (9); Dev manages Gita (10) and Hugo (11); Gita manages Ivy (12). Jay (13) is an orphan whose manager 99 is not in the table. Salaries are toy column data (used in Q9).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,  NULL, 'Tim',   500), (2, 1, 'Radha', 300), (3, 1, 'Hari', 300),
 (4,  2, 'Asha', 100), (5, 3, 'Ben', 200), (6, 3, 'Chen', 200),
 (7,  5, 'Dev', 150), (8, 5, 'Esha', 150), (9, 6, 'Farid', 120),
 (10, 7, 'Gita', 100), (11, 7, 'Hugo', 100), (12, 10, 'Ivy', 90),
 (13, 99, 'Jay', 80);
```
Ivy is four levels below Hari, which is the one the fixed three-join query cannot reach.

**SQL answer:** `SQL_MAIN` in the Code block (`:boss` is a bound parameter):
```sql
WITH RECURSIVE sub(emp_id, name, level) AS (
  SELECT emp_id, name, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20                                   -- depth guard
)
SELECT emp_id, name, level FROM sub ORDER BY level, emp_id
```
The fixed version for a known depth of three, `SQL_FIXED` in the Code block, one branch per level:
```sql
SELECT e1.emp_id, e1.name, 1 AS level FROM employees e1 WHERE e1.manager_id = :boss
UNION ALL
SELECT e2.emp_id, e2.name, 2 FROM employees e1 JOIN employees e2 ON e2.manager_id = e1.emp_id
WHERE e1.manager_id = :boss
UNION ALL
SELECT e3.emp_id, e3.name, 3 FROM employees e1 JOIN employees e2 ON e2.manager_id = e1.emp_id
JOIN employees e3 ON e3.manager_id = e2.emp_id WHERE e1.manager_id = :boss
ORDER BY level, emp_id
```
- The recursive member joins each new employee to the people reported by the previous round, so "deeper org" needs no change: no rewritten query, just more rounds.
- `WHERE s.level < 20` is the depth guard (the cycle demo is below).

**pandas answer:** a while loop that merges the current frontier to the edge frame until nothing new comes out, identical to the Code block (manager_id is converted from float to integer after `dropna`, because the CEO's NULL makes the column float):
```py
def reports_under(employees, boss, max_levels=20):
    edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
    frontier = edges[edges["manager_id"] == boss][["emp_id", "name"]].assign(level=1)
    seen = set(frontier["emp_id"])
    out = [frontier]
    while not frontier.empty and frontier["level"].iloc[0] < max_levels:
        nxt = (frontier[["emp_id", "level"]].rename(columns={"emp_id": "manager_id"})
               .merge(edges[["emp_id", "manager_id", "name"]], on="manager_id")
               .assign(level=lambda d: d["level"] + 1)[["emp_id", "name", "level"]])
        frontier = nxt[~nxt["emp_id"].isin(seen)]
        seen |= set(frontier["emp_id"])
        out.append(frontier)
    return pd.concat(out, ignore_index=True).sort_values(["level", "emp_id"]).reset_index(drop=True)
pd_df = reports_under(employees, 3)
```

**Example:** boss 3.
- Level 1: employees whose `manager_id` is 3: Ben (5) and Chen (6).
- Level 2: reports of 5 or 6: Dev (7), Esha (8), Farid (9).
- Level 3: reports of 7, 8 or 9: Gita (10), Hugo (11).
- Level 4: reports of 10 or 11: Ivy (12). Level 5 finds nobody, so the recursion stops. Total 8 rows. Hari himself is not in the output.
- The fixed 3-join query returns 7 rows and misses exactly Ivy (12), with no error, which is how a hard-coded depth fails when the org gets a fourth level.
- LeetCode 1270 (as summarised from the doocs mirror: head is employee 1, at most three levels, two self-joins) is this query with a hard-coded depth; the recursive form is the general version.

**Code:** run with `python3 -I`. The SQL and pandas results are compared after ordering by `level, emp_id`; the loop also checks bosses 7, 12, 42, 99 and 1.
```python
# Q4: all reports under a manager (recursive CTE), fixed-depth self-joins, pandas frontier loop, cycle demo
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,  NULL, 'Tim',   500),
 (2,  1,    'Radha', 300),
 (3,  1,    'Hari',  300),
 (4,  2,    'Asha',  100),
 (5,  3,    'Ben',   200),
 (6,  3,    'Chen',  200),
 (7,  5,    'Dev',   150),
 (8,  5,    'Esha',  150),
 (9,  6,    'Farid', 120),
 (10, 7,    'Gita',  100),
 (11, 7,    'Hugo',  100),
 (12, 10,   'Ivy',    90),
 (13, 99,   'Jay',    80);     -- orphan: manager 99 does not exist
"""
SQL_MAIN = """
WITH RECURSIVE sub(emp_id, name, level) AS (
  SELECT emp_id, name, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20                                   -- depth guard
)
SELECT emp_id, name, level FROM sub ORDER BY level, emp_id
"""
SQL_FIXED = """
SELECT e1.emp_id, e1.name, 1 AS level FROM employees e1 WHERE e1.manager_id = :boss
UNION ALL
SELECT e2.emp_id, e2.name, 2 FROM employees e1 JOIN employees e2 ON e2.manager_id = e1.emp_id
WHERE e1.manager_id = :boss
UNION ALL
SELECT e3.emp_id, e3.name, 3 FROM employees e1 JOIN employees e2 ON e2.manager_id = e1.emp_id
JOIN employees e3 ON e3.manager_id = e2.emp_id WHERE e1.manager_id = :boss
ORDER BY level, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"boss": 3})
print(sql_df.to_string(index=False))
fixed_df = pd.read_sql_query(SQL_FIXED, con, params={"boss": 3})
print("fixed 3-join version rows:", len(fixed_df), "| recursive rows:", len(sql_df),
      "| missed:", sorted(set(sql_df.emp_id) - set(fixed_df.emp_id)))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def reports_under(employees, boss, max_levels=20):
    edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
    frontier = edges[edges["manager_id"] == boss][["emp_id", "name"]].assign(level=1)
    seen = set(frontier["emp_id"])
    out = [frontier]
    while not frontier.empty and frontier["level"].iloc[0] < max_levels:
        nxt = (frontier[["emp_id", "level"]].rename(columns={"emp_id": "manager_id"})
               .merge(edges[["emp_id", "manager_id", "name"]], on="manager_id")
               .assign(level=lambda d: d["level"] + 1)[["emp_id", "name", "level"]])
        frontier = nxt[~nxt["emp_id"].isin(seen)]
        seen |= set(frontier["emp_id"])
        out.append(frontier)
    return pd.concat(out, ignore_index=True).sort_values(["level", "emp_id"]).reset_index(drop=True)
pd_df = reports_under(employees, 3)
# pd:end
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)     # both ordered by level, emp_id
print("pandas equals SQL")

# Edge cases
for boss in (7, 12, 42, 99, 1):
    r = pd.read_sql_query(SQL_MAIN, con, params={"boss": boss})
    p = reports_under(employees, boss)
    pd.testing.assert_frame_equal(p, r, check_dtype=False)
    print(f"boss {boss}: {len(r)} rows, levels {sorted(set(r['level']))}")
print("boss NULL (manager_id = NULL never matches):", con.execute(SQL_MAIN, {"boss": None}).fetchall())
# manager included? add him with level 0 via UNION ALL
print("with the manager as level 0:", con.execute("""
WITH RECURSIVE sub(emp_id, name, level) AS (
  SELECT emp_id, name, 0 FROM employees WHERE emp_id = :boss
  UNION ALL SELECT e.emp_id, e.name, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id WHERE s.level < 20)
SELECT count(*), min(level) FROM sub""", {"boss": 3}).fetchone())

# Cycle demo on a copy: Hari (3) now reports to Dev (7), who is below him
con.execute("CREATE TABLE emp_cyc AS SELECT * FROM employees")
con.execute("UPDATE emp_cyc SET manager_id = 7 WHERE emp_id = 3")
unguarded = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM emp_cyc WHERE manager_id = 3
  UNION ALL SELECT e.emp_id, s.level + 1 FROM emp_cyc e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id, level FROM sub LIMIT 14"""     # LIMIT is the only thing stopping this demo
rows = con.execute(unguarded).fetchall()
print("cycle, no guard, LIMIT 14 shows repeats:", rows)
guarded = pd.read_sql_query(SQL_MAIN.replace("employees", "emp_cyc"), con, params={"boss": 3})
print("cycle, depth cap 20: rows =", len(guarded), "| distinct emp_ids =", guarded.emp_id.nunique(), "| clean answer rows would be", len(sql_df))
print("asserts passed")
```

**Output (my run):**
```text
 emp_id  name  level
      5   Ben      1
      6  Chen      1
      7   Dev      2
      8  Esha      2
      9 Farid      2
     10  Gita      3
     11  Hugo      3
     12   Ivy      4
fixed 3-join version rows: 7 | recursive rows: 8 | missed: [12]
pandas equals SQL
boss 7: 3 rows, levels [1, 2]
boss 12: 0 rows, levels []
boss 42: 0 rows, levels []
boss 99: 1 rows, levels [1]
boss 1: 11 rows, levels [1, 2, 3, 4, 5]
boss NULL (manager_id = NULL never matches): []
with the manager as level 0: (9, 0)
cycle, no guard, LIMIT 14 shows repeats: [(5, 1), (6, 1), (7, 2), (8, 2), (9, 2), (3, 3), (10, 3), (11, 3), (5, 4), (6, 4), (12, 4), (7, 5), (8, 5), (9, 5)]
cycle, depth cap 20: rows = 59 | distinct emp_ids = 9 | clean answer rows would be 8
asserts passed
```

**Edge cases:**
- Leaf manager (12) or a manager id that does not exist (42): empty result. Boss NULL: `manager_id = NULL` never matches, so empty too (pandas would match NaN to NaN in a merge, so never pass a NaN boss; here the CEO's NaN is dropped before the merge).
- Orphan: boss 99 returns Jay, because the anchor is a filter on `manager_id`, not a join to the manager row. If you must require the manager to exist, join to `employees` for the boss first.
- Whole company: boss 1 returns 11 rows over five levels (Jay is not under Tim, since 99 is missing).
- Including the manager: change the anchor to `SELECT emp_id, name, 0 FROM employees WHERE emp_id = :boss` (that gives 9 rows for boss 3, the 8 reports plus Hari at level 0).
- Cycle: on a copy where Hari reports to Dev (his own descendant), the unguarded query with `LIMIT 14` keeps going (ids 5, 6, 7 ... then 3 and 5, 6 again); with only the depth cap it ends but returns 59 rows for 9 distinct people, because every lap around the loop repeats rows. A depth cap makes the query finish, it does not make the answer right. A visited-path check (Q8) does.
- Duplicate employee rows (no primary key) would repeat the whole subtree under them.

**Then explain:**
- Recursive: unknown depth, one query, cost grows with the rows visited. Fixed joins: depth baked in, wrong silently when the org changes.
- Index `manager_id`; each round is a lookup by manager (Q29 times it).
- SQL Server writes this without `RECURSIVE` and caps at 100 levels by default; MySQL needs `WITH RECURSIVE`; PostgreSQL and Oracle (`START WITH ... CONNECT BY PRIOR`) also do it (all hedged, not executed).
- Level 1 for direct reports is a convention; say it out loud.

**Follow-ups:**
- Give me the count only: `SELECT COUNT(*) FROM sub`, outside the CTE.
- What if two people appear twice because of two paths? In an employee table with one manager per row that cannot happen; in a DAG (Q10) it can.
- How do you make it parameter-free for all managers? Q9 does that with ancestor and descendant pairs.

**Common mistakes:**
- A fixed number of self-joins that silently truncates a deeper org.
- No depth or visited guard on data that can have a loop.
- `NOT IN` or `= NULL` on a nullable `manager_id`.
- Putting the boss in the output without saying so, or putting him in as level 1.

### Q5 ⭐⭐⭐ 🟢 Chain of command upwards: employees(emp_id, manager_id, name). For employee 'Ram' (emp_id 10) return every manager up to the CEO, with level 0 for Ram, 1 for his manager and so on, and the chain as one string 'Ram > Shyam > Hari > Radha > Tim'. Show the upward recursion (join e.emp_id = cte.manager_id), explain why it stops at the CEO (manager_id is NULL so the join finds nothing), what happens with an employee whose manager_id points to a missing row, and how to return the number of levels to the top for every employee at once rather than for one.
**Asked at:** employee-manager hierarchy guides: jdsatpathy Substack 'Find All Managers of an Employee Up to the CEO' (opened; anchor at the employee, join employee to manager, no cycle guard, UNION ALL), DataVidhya recursive hierarchy pattern page (opened; reports under a manager, ancestors of a category, paths in a dependency graph, depth tracking and cycle detection), and search snippets of datadriven.io and a Medium recursive CTE interview post (not opened); guides, not candidate reports; analyst and data engineer rounds at product companies, GCCs and consulting firms
**Say this first (1 line):** Anchor on Ram (level 0), then join `employees e ON e.emp_id = chain.manager_id` so each round fetches the manager of the previous row, appending the name to a path string; it stops at the CEO because his `manager_id` is NULL and `emp_id = NULL` never matches, and for "levels to the top for everyone" I anchor on all employees, carry the starting id along, and take `MAX(level)` per start.

**Schema and sample data:** ten employees: the chain Ram (10) to Shyam (4) to Hari (3) to Radha (2) to Tim (1, NULL manager), plus Sita (11) under Hari. Three bad rows on purpose: Orphan (20) with a missing manager 99, LoopA and LoopB (30 and 31) managing each other, and Self (40) managing himself.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1, NULL, 'Tim'), (2, 1, 'Radha'), (3, 2, 'Hari'), (4, 3, 'Shyam'),
 (10, 4, 'Ram'), (11, 3, 'Sita'),
 (20, 99, 'Orphan'), (30, 31, 'LoopA'), (31, 30, 'LoopB'), (40, 40, 'Self');
```

**SQL answer:** one employee, `SQL_CHAIN` in the Code block (`:emp` is 10). The last row's `path` is the string asked for:
```sql
WITH RECURSIVE chain(emp_id, manager_id, name, level, path, ids) AS (
  SELECT emp_id, manager_id, name, 0, name, ',' || emp_id || ','
  FROM employees WHERE emp_id = :emp
  UNION ALL
  SELECT e.emp_id, e.manager_id, e.name, c.level + 1, c.path || ' > ' || e.name, c.ids || e.emp_id || ','
  FROM employees e JOIN chain c ON e.emp_id = c.manager_id
  WHERE instr(c.ids, ',' || e.emp_id || ',') = 0        -- cycle guard: never visit an employee twice
)
SELECT emp_id, name, level, path FROM chain ORDER BY level
```
Everyone at once, `SQL_ALL` in the Code block:
```sql
WITH RECURSIVE up(start_id, mgr_id, level, ids) AS (
  SELECT emp_id, manager_id, 0, ',' || emp_id || ',' FROM employees
  UNION ALL
  SELECT u.start_id, e.manager_id, u.level + 1, u.ids || e.emp_id || ','
  FROM up u JOIN employees e ON e.emp_id = u.mgr_id
  WHERE instr(u.ids, ',' || e.emp_id || ',') = 0
)
SELECT start_id AS emp_id,
       MAX(level) AS levels_to_top,
       MAX(CASE WHEN mgr_id IS NULL THEN 1 ELSE 0 END) AS reached_ceo
FROM up GROUP BY start_id ORDER BY start_id
```
- The join direction is the reverse of Q4: Q4 asks "whose manager is this row?", here "which row is this row's manager?".
- `ids` is a comma-delimited list of visited ids, used as the cycle guard: an employee already in the list is not visited again.
- `reached_ceo` says whether the walk ended on a NULL manager. `levels_to_top = 0` alone cannot tell the CEO (0, reached) from an orphan (0, not reached).

**pandas answer:** a dict walk (employee to manager) with a visited set, identical to the Code block:
```py
mgr = dict(zip(employees["emp_id"], employees["manager_id"]))      # NaN for the CEO
nm = dict(zip(employees["emp_id"], employees["name"]))
def walk(emp):
    rows, seen, cur = [], set(), emp
    while cur not in seen:
        seen.add(cur)
        rows.append((cur, nm[cur], len(rows)))
        nxt = mgr[cur]
        if pd.isna(nxt) or int(nxt) not in mgr:                     # CEO (NaN) or missing manager: stop
            break
        cur = int(nxt)
    path = []
    out = []
    for e, n_, lvl in rows:
        path.append(n_)
        out.append((e, n_, lvl, " > ".join(path)))
    last_mgr = mgr[rows[-1][0]]
    return pd.DataFrame(out, columns=["emp_id", "name", "level", "path"]), bool(pd.isna(last_mgr))
pd_chain, _ = walk(10)
pd_all = pd.DataFrame([(e, len(walk(e)[0]) - 1, int(walk(e)[1])) for e in employees["emp_id"]],
                      columns=["emp_id", "levels_to_top", "reached_ceo"])
```

**Example:** Ram (10).
- Level 0: Ram, path `Ram`. His manager id is 4.
- Level 1: employee 4 Shyam, `Ram > Shyam`. Level 2: Hari. Level 3: Radha. Level 4: Tim, path `Ram > Shyam > Hari > Radha > Tim`. Tim's `manager_id` is NULL, `e.emp_id = NULL` matches nothing, so the next round is empty and the recursion ends.
- For everyone: Tim 0, Radha 1, Hari 2, Shyam 3, Ram 4, Sita 3 (Sita to Hari to Radha to Tim).
- Orphan (20): the join for manager 99 finds nothing, so the walk ends after level 0 with `reached_ceo = 0`. It looks like a top-level employee unless you check the flag.

**Code:** run with `python3 -I`. The chain is compared after ordering by `level`, the all-employee table after ordering by `emp_id`.
```python
# Q5: chain of command upwards for one employee and the levels-to-top for everyone; guards for loops and orphans
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,  NULL, 'Tim'),
 (2,  1,    'Radha'),
 (3,  2,    'Hari'),
 (4,  3,    'Shyam'),
 (10, 4,    'Ram'),
 (11, 3,    'Sita'),
 (20, 99,   'Orphan'),   -- manager 99 is missing
 (30, 31,   'LoopA'),    -- 30 and 31 manage each other
 (31, 30,   'LoopB'),
 (40, 40,   'Self');     -- manages himself
"""
SQL_CHAIN = """
WITH RECURSIVE chain(emp_id, manager_id, name, level, path, ids) AS (
  SELECT emp_id, manager_id, name, 0, name, ',' || emp_id || ','
  FROM employees WHERE emp_id = :emp
  UNION ALL
  SELECT e.emp_id, e.manager_id, e.name, c.level + 1, c.path || ' > ' || e.name, c.ids || e.emp_id || ','
  FROM employees e JOIN chain c ON e.emp_id = c.manager_id
  WHERE instr(c.ids, ',' || e.emp_id || ',') = 0        -- cycle guard: never visit an employee twice
)
SELECT emp_id, name, level, path FROM chain ORDER BY level
"""
SQL_ALL = """
WITH RECURSIVE up(start_id, mgr_id, level, ids) AS (
  SELECT emp_id, manager_id, 0, ',' || emp_id || ',' FROM employees
  UNION ALL
  SELECT u.start_id, e.manager_id, u.level + 1, u.ids || e.emp_id || ','
  FROM up u JOIN employees e ON e.emp_id = u.mgr_id
  WHERE instr(u.ids, ',' || e.emp_id || ',') = 0
)
SELECT start_id AS emp_id,
       MAX(level) AS levels_to_top,
       MAX(CASE WHEN mgr_id IS NULL THEN 1 ELSE 0 END) AS reached_ceo
FROM up GROUP BY start_id ORDER BY start_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_chain = pd.read_sql_query(SQL_CHAIN, con, params={"emp": 10})
print(sql_chain.to_string(index=False))
print("chain string:", sql_chain["path"].iloc[-1])
sql_all = pd.read_sql_query(SQL_ALL, con)
print(sql_all.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
mgr = dict(zip(employees["emp_id"], employees["manager_id"]))      # NaN for the CEO
nm = dict(zip(employees["emp_id"], employees["name"]))
def walk(emp):
    rows, seen, cur = [], set(), emp
    while cur not in seen:
        seen.add(cur)
        rows.append((cur, nm[cur], len(rows)))
        nxt = mgr[cur]
        if pd.isna(nxt) or int(nxt) not in mgr:                     # CEO (NaN) or missing manager: stop
            break
        cur = int(nxt)
    path = []
    out = []
    for e, n_, lvl in rows:
        path.append(n_)
        out.append((e, n_, lvl, " > ".join(path)))
    last_mgr = mgr[rows[-1][0]]
    return pd.DataFrame(out, columns=["emp_id", "name", "level", "path"]), bool(pd.isna(last_mgr))
pd_chain, _ = walk(10)
pd_all = pd.DataFrame([(e, len(walk(e)[0]) - 1, int(walk(e)[1])) for e in employees["emp_id"]],
                      columns=["emp_id", "levels_to_top", "reached_ceo"])
# pd:end
pd.testing.assert_frame_equal(pd_chain, sql_chain, check_dtype=False)               # ordered by level
pd.testing.assert_frame_equal(pd_all.sort_values("emp_id").reset_index(drop=True), sql_all, check_dtype=False)
print("pandas equals SQL (chain by level, all by emp_id)")

# Edge cases
print("CEO himself:", con.execute(SQL_CHAIN, {"emp": 1}).fetchall())
print("orphan chain stops at the missing manager:", con.execute(SQL_CHAIN, {"emp": 20}).fetchall())
print("unknown employee:", con.execute(SQL_CHAIN, {"emp": 777}).fetchall())
unguarded = SQL_CHAIN.replace("  WHERE instr(c.ids, ',' || e.emp_id || ',') = 0        -- cycle guard: never visit an employee twice\n", "").replace("ORDER BY level", "LIMIT 7")
print("loop employee 30 without the guard, LIMIT 7:", [(r[1], r[2]) for r in con.execute(unguarded, {"emp": 30})])
print("loop employee 30 with the guard:", [(r[1], r[2]) for r in con.execute(SQL_CHAIN, {"emp": 30})])
print("asserts passed")
```

**Output (my run):**
```text
 emp_id  name  level                             path
     10   Ram      0                              Ram
      4 Shyam      1                      Ram > Shyam
      3  Hari      2               Ram > Shyam > Hari
      2 Radha      3       Ram > Shyam > Hari > Radha
      1   Tim      4 Ram > Shyam > Hari > Radha > Tim
chain string: Ram > Shyam > Hari > Radha > Tim
 emp_id  levels_to_top  reached_ceo
      1              0            1
      2              1            1
      3              2            1
      4              3            1
     10              4            1
     11              3            1
     20              0            0
     30              1            0
     31              1            0
     40              0            0
pandas equals SQL (chain by level, all by emp_id)
CEO himself: [(1, 'Tim', 0, 'Tim')]
orphan chain stops at the missing manager: [(20, 'Orphan', 0, 'Orphan')]
unknown employee: []
loop employee 30 without the guard, LIMIT 7: [('LoopA', 0), ('LoopB', 1), ('LoopA', 2), ('LoopB', 3), ('LoopA', 4), ('LoopB', 5), ('LoopA', 6)]
loop employee 30 with the guard: [('LoopA', 0), ('LoopB', 1)]
asserts passed
```

**Edge cases:**
- The CEO: one row, level 0 (`[(1, 'Tim', 0, 'Tim')]`). An unknown employee id: no rows, because the anchor finds nothing.
- Missing manager (Orphan): the chain is just the employee; the query does not error. In the all-employees result Orphan has `levels_to_top = 0` and `reached_ceo = 0`; that is the data-quality signal (Q15 builds the full audit).
- Loop (LoopA and LoopB): without the guard the unguarded query kept going (`LoopA, LoopB, LoopA, LoopB ...`, stopped only by `LIMIT 7`); with the guard it returns two rows and `reached_ceo = 0`.
- Self-managed (Self): guard stops it after level 0.
- NULL manager is the normal CEO marker; a missing or loop manager is the bad data. Do not use `NOT IN (SELECT manager_id ...)` to find the top, because one NULL makes the whole `NOT IN` unknown (Q15).
- In pandas the `manager_id` column is float because of the NaN; `int()` is needed before looking up the dict, and `pd.isna` tests the CEO.

**Then explain:**
- Walking up is cheap: one row per level, at most the depth of that employee. Walking up for everyone is rows = sum of depths, which is fine for HR-sized tables.
- Stopping at the CEO needs no special code because NULL never equals anything. Stopping at a missing manager works the same way.
- The path string is built in the recursive member, by concatenating (`||` in SQLite, PostgreSQL; `CONCAT` or `+` in SQL Server; hedged, not executed).
- The levels-to-top count is an aggregate, so it sits outside the CTE (aggregates are not allowed in the recursive member).

**Follow-ups:**
- Which manager is the CEO of each employee? Take the row with the highest level per `start_id` (a window or a join back); only valid where `reached_ceo = 1`.
- How do you find the number of reports instead? Reverse the join; that is Q4 and Q9.
- Why a string path and not a list? SQLite has no array type; PostgreSQL has arrays (hedged, not executed).

**Common mistakes:**
- Joining the wrong way round (`e.manager_id = chain.emp_id`) and walking down instead of up.
- No guard on loops or self-managers.
- Reporting `level = 0` for an orphan as if it were the CEO.
- Concatenating without a delimiter, which makes ids 1 and 11 indistinguishable in a visited string.

### Q6 ⭐⭐⭐ 🟡 Level, path and leaf or root flags: employees(emp_id, manager_id, name, salary). Return for every employee the level (CEO = 0), the path of names from the CEO ('Tim/Radha/Hari'), an indented name for display, is_root and is_leaf flags (leaf = nobody reports to them), and sort the output so each manager is followed by their subtree (depth-first). Show how the path column is the sort key, why path strings sort wrongly for numeric ids ('10' before '2') and the zero-padded fix, how ORDER BY in the recursive member gives breadth-first or depth-first queue order in SQLite, and the PostgreSQL SEARCH DEPTH FIRST clause (not executed).
**Asked at:** SQLite lang_with documentation (opened: compound SELECT with a non-recursive initial select, UNION discards rows already queued and stops cycles, UNION ALL needs little memory, LIMIT on the recursive select, ORDER BY in the recursive select as queue order for breadth-first or depth-first, no aggregates or windows in the recursive select, queue algorithm) plus PostgreSQL WITH queries documentation (opened: working table and intermediate table evaluation); official documentation, not candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Start at the root (`manager_id IS NULL`, level 0) and carry three things down: the level, the name path and a sort key made of zero-padded ids; the final `ORDER BY` on that sort key gives depth-first order (each manager followed by his subtree), `is_leaf` is a `NOT EXISTS` on the table and `is_root` is level 0, and padding matters because the text `'14'` sorts before `'2'`.

**Schema and sample data:** fourteen employees: the Q4 tree (Tim at the root, ids 1 to 12), Jay (13, orphan with missing manager 99) and Kim (14, a direct report of Tim). Kim exists to expose the text sort bug: under Tim the siblings are 2, 3 and 14.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1, NULL, 'Tim', 500), (2, 1, 'Radha', 300), (3, 1, 'Hari', 300), (4, 2, 'Asha', 100),
 (5, 3, 'Ben', 200), (6, 3, 'Chen', 200), (7, 5, 'Dev', 150), (8, 5, 'Esha', 150),
 (9, 6, 'Farid', 120), (10, 7, 'Gita', 100), (11, 7, 'Hugo', 100), (12, 10, 'Ivy', 90),
 (13, 99, 'Jay', 80), (14, 1, 'Kim', 100);
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
WITH RECURSIVE t(emp_id, name, level, path, sortkey) AS (
  SELECT emp_id, name, 0, name, printf('%03d', emp_id)
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.level + 1, t.path || '/' || e.name, t.sortkey || '/' || printf('%03d', e.emp_id)
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 20                                        -- depth guard
)
SELECT t.emp_id,
       printf('%*s', 2 * t.level, '') || t.name AS display_name,
       t.level, t.path,
       (t.level = 0) AS is_root,
       NOT EXISTS (SELECT 1 FROM employees x WHERE x.manager_id = t.emp_id) AS is_leaf
FROM t
ORDER BY t.sortkey
```
- `path` is for display (`Tim/Hari/Ben`). `sortkey` is for sorting (`001/003/005`). They are separate columns on purpose: the name path would sort siblings alphabetically (that is a valid but different order), and an unpadded id path would sort wrongly.
- `printf('%*s', 2 * level, '')` makes the indent (SQLite's printf takes `*` as a width; checked in the run). `is_leaf` is evaluated outside the recursion with `NOT EXISTS`.
- The queue-order alternative, `SQL_QUEUE_DFS` in the Code block, puts `ORDER BY 4` inside the recursive member so that SQLite takes the smallest `sortkey` from its queue next:
```sql
WITH RECURSIVE t(emp_id, name, level, sortkey) AS (
  SELECT emp_id, name, 0, printf('%03d', emp_id) FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.level + 1, t.sortkey || '/' || printf('%03d', e.emp_id)
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  ORDER BY 4                                               -- queue order: the smallest sortkey is taken next
)
SELECT name FROM t                                         -- no outer ORDER BY: order is whatever the queue gave
```
 SQLite's documentation (opened) describes `ORDER BY` in the recursive select as the queue order, so `ORDER BY level` style variants give breadth-first and ordering by a depth-descending or path key gives depth-first. It returned the correct depth-first sequence on 3.45.1 in my run, but I would still sort in the final `SELECT`, because the order of an unordered outer query is not a promise.
- PostgreSQL 14+ writes this as `SEARCH DEPTH FIRST BY emp_id SET ordercol` and orders by `ordercol`; not executed here; the Wave A sources note records that SQLite 3.45.1 gives a syntax error on `SEARCH` and `CYCLE` clauses (checked by running there).

**pandas answer:** top-down merge loop that carries the same three columns, identical to the Code block:
```py
edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
cur = employees[employees["manager_id"].isna()].assign(level=0, path=lambda d: d["name"], sortkey=lambda d: d["emp_id"].map("{:03d}".format))
frames = [cur]
while not cur.empty and cur["level"].iloc[0] < 20:
    cur = (cur[["emp_id", "level", "path", "sortkey"]].rename(columns={"emp_id": "manager_id"})
           .merge(edges[["emp_id", "manager_id", "name"]], on="manager_id")
           .assign(level=lambda d: d["level"] + 1, path=lambda d: d["path"] + "/" + d["name"],
                   sortkey=lambda d: d["sortkey"] + "/" + d["emp_id"].map("{:03d}".format)))
    frames.append(cur)
t = pd.concat(frames, ignore_index=True)
t["display_name"] = ["  " * l + n for l, n in zip(t["level"], t["name"])]
t["is_root"] = (t["level"] == 0).astype(int)
t["is_leaf"] = (~t["emp_id"].isin(employees["manager_id"].dropna().astype(int))).astype(int)
pd_df = t.sort_values("sortkey")[["emp_id", "display_name", "level", "path", "is_root", "is_leaf"]].reset_index(drop=True)
```

**Example:** how the sort key orders the subtree of Tim.
- Keys: Tim `001`; Radha `001/002`; Asha `001/002/004`; Hari `001/003`; Ben `001/003/005`; Dev `001/003/005/007`; Gita `001/003/005/007/010`; Ivy `001/003/005/007/010/012`; Hugo `.../007/011`; Esha `001/003/005/008`; Chen `001/003/006`; Farid `001/003/006/009`; Kim `001/014`.
- Sorted as text these give the depth-first listing printed in the output: Tim, Radha, Asha, Hari, Ben, Dev, Gita, Ivy, Hugo, Esha, Chen, Farid, Kim. Each manager is followed by his entire subtree before his next sibling.
- Leaves (nobody reports to them): Asha, Ivy, Hugo, Esha, Farid, Kim. Root flag: Tim only.
- The unpadded text path (`1/14` against `1/2`) puts Kim straight after Tim and before Radha and Asha, which is not depth-first by id; padding every id to the same width fixes the comparison.
- Jay (13) never appears, because he is not reachable from the root: 13 rows out of 14.

**Code:** run with `python3 -I`. SQL and pandas are compared after ordering by the padded sort key; the queue-order variant and the naive sort are asserted against that sequence.
```python
# Q6: level, path, indentation, root/leaf flags and a depth-first sort; padded sort key; queue order in SQLite
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1, NULL, 'Tim', 500), (2, 1, 'Radha', 300), (3, 1, 'Hari', 300), (4, 2, 'Asha', 100),
 (5, 3, 'Ben', 200), (6, 3, 'Chen', 200), (7, 5, 'Dev', 150), (8, 5, 'Esha', 150),
 (9, 6, 'Farid', 120), (10, 7, 'Gita', 100), (11, 7, 'Hugo', 100), (12, 10, 'Ivy', 90),
 (13, 99, 'Jay', 80),          -- orphan: never reached from the CEO
 (14, 1, 'Kim', 100);          -- id 14 sorts before 2 as text
"""
SQL_MAIN = """
WITH RECURSIVE t(emp_id, name, level, path, sortkey) AS (
  SELECT emp_id, name, 0, name, printf('%03d', emp_id)
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.level + 1, t.path || '/' || e.name, t.sortkey || '/' || printf('%03d', e.emp_id)
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 20                                        -- depth guard
)
SELECT t.emp_id,
       printf('%*s', 2 * t.level, '') || t.name AS display_name,
       t.level, t.path,
       (t.level = 0) AS is_root,
       NOT EXISTS (SELECT 1 FROM employees x WHERE x.manager_id = t.emp_id) AS is_leaf
FROM t
ORDER BY t.sortkey
"""
SQL_QUEUE_DFS = """
WITH RECURSIVE t(emp_id, name, level, sortkey) AS (
  SELECT emp_id, name, 0, printf('%03d', emp_id) FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.level + 1, t.sortkey || '/' || printf('%03d', e.emp_id)
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  ORDER BY 4                                               -- queue order: the smallest sortkey is taken next
)
SELECT name FROM t                                         -- no outer ORDER BY: order is whatever the queue gave
"""
SQL_NAIVE = """
WITH RECURSIVE t(emp_id, name, idpath) AS (
  SELECT emp_id, name, CAST(emp_id AS TEXT) FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.idpath || '/' || e.emp_id FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE length(t.idpath) < 60                              -- guard
)
SELECT name FROM t ORDER BY idpath
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
for r in sql_df.itertuples():
    print(f"{r.emp_id:>2} [{r.display_name:<14}] level={r.level} root={r.is_root} leaf={r.is_leaf} path={r.path}")

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
cur = employees[employees["manager_id"].isna()].assign(level=0, path=lambda d: d["name"], sortkey=lambda d: d["emp_id"].map("{:03d}".format))
frames = [cur]
while not cur.empty and cur["level"].iloc[0] < 20:
    cur = (cur[["emp_id", "level", "path", "sortkey"]].rename(columns={"emp_id": "manager_id"})
           .merge(edges[["emp_id", "manager_id", "name"]], on="manager_id")
           .assign(level=lambda d: d["level"] + 1, path=lambda d: d["path"] + "/" + d["name"],
                   sortkey=lambda d: d["sortkey"] + "/" + d["emp_id"].map("{:03d}".format)))
    frames.append(cur)
t = pd.concat(frames, ignore_index=True)
t["display_name"] = ["  " * l + n for l, n in zip(t["level"], t["name"])]
t["is_root"] = (t["level"] == 0).astype(int)
t["is_leaf"] = (~t["emp_id"].isin(employees["manager_id"].dropna().astype(int))).astype(int)
pd_df = t.sort_values("sortkey")[["emp_id", "display_name", "level", "path", "is_root", "is_leaf"]].reset_index(drop=True)
# pd:end
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)        # both ordered by the padded sort key
print("pandas equals SQL (ordered by padded sort key)")

queue_order = [r[0] for r in con.execute(SQL_QUEUE_DFS)]
print("queue DFS (ORDER BY in recursive member):", queue_order)
assert queue_order == sql_df["display_name"].str.strip().tolist()
naive = [r[0] for r in con.execute(SQL_NAIVE)]
print("naive text sort of '1/14' vs '1/2':", naive[:4], "... differs from true DFS:", naive != queue_order)
assert naive != queue_order

# Edge cases
print("orphan Jay in output:", 13 in set(sql_df["emp_id"]), "| rows:", len(sql_df), "of", len(employees))
con.execute("UPDATE employees SET manager_id = NULL WHERE emp_id = 13")
print("after Jay becomes a second root:", len(pd.read_sql_query(SQL_MAIN, con)), "rows, roots:", int(pd.read_sql_query(SQL_MAIN, con)["is_root"].sum()))
print("asserts passed")
```

**Output (my run):**
```text
 1 [Tim           ] level=0 root=1 leaf=0 path=Tim
 2 [  Radha       ] level=1 root=0 leaf=0 path=Tim/Radha
 4 [    Asha      ] level=2 root=0 leaf=1 path=Tim/Radha/Asha
 3 [  Hari        ] level=1 root=0 leaf=0 path=Tim/Hari
 5 [    Ben       ] level=2 root=0 leaf=0 path=Tim/Hari/Ben
 7 [      Dev     ] level=3 root=0 leaf=0 path=Tim/Hari/Ben/Dev
10 [        Gita  ] level=4 root=0 leaf=0 path=Tim/Hari/Ben/Dev/Gita
12 [          Ivy ] level=5 root=0 leaf=1 path=Tim/Hari/Ben/Dev/Gita/Ivy
11 [        Hugo  ] level=4 root=0 leaf=1 path=Tim/Hari/Ben/Dev/Hugo
 8 [      Esha    ] level=3 root=0 leaf=1 path=Tim/Hari/Ben/Esha
 6 [    Chen      ] level=2 root=0 leaf=0 path=Tim/Hari/Chen
 9 [      Farid   ] level=3 root=0 leaf=1 path=Tim/Hari/Chen/Farid
14 [  Kim         ] level=1 root=0 leaf=1 path=Tim/Kim
pandas equals SQL (ordered by padded sort key)
queue DFS (ORDER BY in recursive member): ['Tim', 'Radha', 'Asha', 'Hari', 'Ben', 'Dev', 'Gita', 'Ivy', 'Hugo', 'Esha', 'Chen', 'Farid', 'Kim']
naive text sort of '1/14' vs '1/2': ['Tim', 'Kim', 'Radha', 'Asha'] ... differs from true DFS: True
orphan Jay in output: False | rows: 13 of 14
after Jay becomes a second root: 14 rows, roots: 2
asserts passed
```

**Edge cases:**
- Orphans and cycles are invisible to a top-down query, and so is any employee who is not reachable from the root: Jay is simply absent. Q15 finds them.
- Two roots (I set Jay's manager to NULL on a copy): 14 rows, 2 roots, and the sort key makes the second tree appear after the first, because every tree starts with its own padded id.
- A zero-padding width must cover the largest id (`%03d` is enough here up to 999). Larger ids need a wider format or a rank instead of the raw id.
- `is_leaf` by `NOT EXISTS` is safe with NULLs; `emp_id NOT IN (SELECT manager_id ...)` is not, because the CEO's NULL manager makes the whole `NOT IN` unknown and every employee would come back as not a leaf.
- Depth guard: `WHERE t.level < 20` keeps a bad loop from running forever (Q8 shows the visited-path check); on a looping row set a top-down query from a real root does not loop anyway, but a restart from a loop node would.

**Then explain:**
- The sort key does the depth-first ordering; the recursion only builds the rows. Without a key you get breadth-first order (level by level) in most engines, which is not what an org chart display wants.
- Name path versus id path: names for display, ids for ordering and joins.
- Level 0 for the CEO is a convention; Oracle's `LEVEL` and many guides start at 1.
- Other engines (not executed): Oracle `START WITH manager_id IS NULL CONNECT BY PRIOR emp_id = manager_id ORDER SIBLINGS BY ...` with `LEVEL`, `SYS_CONNECT_BY_PATH` and `CONNECT_BY_ISLEAF` does this natively (names from the Oracle documentation snippets in the sources note, `ORDER SIBLINGS BY` from memory); SQL Server uses `hierarchyid` or the same CTE with `+` and a padded string.

**Follow-ups:**
- Breadth-first instead? Order by `level, sortkey`.
- Only leaves? `WHERE is_leaf = 1` on the final result.
- How would you sort siblings by name? Put a rank of the name among siblings (`ROW_NUMBER() OVER (PARTITION BY manager_id ORDER BY name)`) into the key instead of the id.

**Common mistakes:**
- Sorting an unpadded id string.
- Computing `is_leaf` inside the recursive member (impossible: the member cannot aggregate or see the children).
- Trusting the order of the unordered outer query.
- Using `NOT IN` on a nullable column for leaf detection.

### Q7 ⭐⭐⭐ 🟡 UNION versus UNION ALL in recursion: edges(src, dst) is a small directed graph in which node D can be reached from A by two routes (A to B to D and A to C to D) and also contains a cycle D to A. Show what UNION ALL does (duplicate rows, then infinite loop on the cycle), what UNION does (dedups whole rows and so terminates on a cycle when no extra column makes rows unique), and why adding a depth or path column to the row defeats UNION's cycle protection. State the cost of UNION (it must remember every row produced) and the PostgreSQL and MySQL equivalents (UNION DISTINCT), with the limits hedged as not executed.
**Asked at:** PostgreSQL WITH queries documentation (opened: UNION versus UNION ALL on cycles, SEARCH DEPTH or BREADTH FIRST BY ... SET, CYCLE ... SET ... USING, LIMIT on the parent query as a test trick, not to be relied on) and the SQLite lang_with page (opened); official documentation, not candidate reports; analyst and data engineer rounds on PostgreSQL stacks
**Say this first (1 line):** `UNION ALL` keeps every row, so a node reached by two routes appears twice and a cycle never stops; `UNION` throws away any row it has already produced, so on a key-only row (`node`) the cycle ends by itself, but the moment you add a depth or path column every row is unique again and `UNION` protects nothing; the price is that `UNION` has to remember every row it ever produced.

**Schema and sample data:** five edges. A goes to B and to C; both B and C go to D (two routes to D); D goes back to A (a cycle).
```sql
CREATE TABLE edges(src TEXT, dst TEXT);
INSERT INTO edges VALUES ('A','B'), ('A','C'), ('B','D'), ('C','D'), ('D','A');
```

**SQL answer:** five variants in the Code block, all starting from A. With `UNION ALL` and a depth cap (`SQL_ALL_CAP`):
```sql
WITH RECURSIVE r(node, depth) AS (
  SELECT 'A', 0
  UNION ALL
  SELECT e.dst, r.depth + 1 FROM edges e JOIN r ON e.src = r.node
  WHERE r.depth < 4                                      -- depth cap: the only stop
)
SELECT node, depth FROM r ORDER BY depth, node
```
`UNION` on a key-only row (`SQL_UNION`):
```sql
WITH RECURSIVE r(node) AS (
  SELECT 'A'
  UNION                                                  -- drops a row that was already produced
  SELECT e.dst FROM edges e JOIN r ON e.src = r.node
)
SELECT node FROM r ORDER BY node
```
`UNION` with a depth column added (`SQL_UNION_DEPTH`, bounded only by an outer `LIMIT`):
```sql
WITH RECURSIVE r(node, depth) AS (
  SELECT 'A', 0
  UNION                                                  -- depth makes every row new, so nothing is dropped
  SELECT e.dst, r.depth + 1 FROM edges e JOIN r ON e.src = r.node
)
SELECT node, depth FROM r LIMIT 15                       -- LIMIT is the only reason this demo stops
```
`UNION ALL` without any guard (`SQL_UNION_ALL_LOOP`, bounded only by `LIMIT 12`):
```sql
WITH RECURSIVE r(node) AS (
  SELECT 'A' UNION ALL SELECT e.dst FROM edges e JOIN r ON e.src = r.node
)
SELECT node FROM r LIMIT 12
```
And the proper route-keeping version, `UNION ALL` with a visited check on a path column (`SQL_PATH`):
```sql
WITH RECURSIVE r(node, path) AS (
  SELECT 'A', ',A,'
  UNION ALL
  SELECT e.dst, r.path || e.dst || ','
  FROM edges e JOIN r ON e.src = r.node
  WHERE instr(r.path, ',' || e.dst || ',') = 0           -- visited check on the path
)
SELECT node, path FROM r ORDER BY path
```

**pandas answer:** the three terminating versions as frontier loops, identical to the Code block: (1) no de-duplication with a round cap, (2) a visited frame and an anti-join (the pandas form of `UNION` on a key), (3) a path guard:
```py
step = lambda f: f.merge(edges, left_on="node", right_on="src")[["dst"]].rename(columns={"dst": "node"})
# (1) UNION ALL with a depth cap: no de-duplication
frontier = pd.DataFrame({"node": ["A"], "depth": 0})
frames = [frontier]
for d in range(1, 5):
    frontier = step(frontier).assign(depth=d)
    frames.append(frontier)
pd_cap = pd.concat(frames, ignore_index=True).sort_values(["depth", "node"]).reset_index(drop=True)
# (2) UNION on a key-only row: keep a visited frame, anti-join the new rows against it
reach = pd.DataFrame({"node": ["A"]})
frontier = reach
while not frontier.empty:
    nxt = step(frontier).drop_duplicates()
    frontier = nxt[~nxt["node"].isin(reach["node"])]
    reach = pd.concat([reach, frontier], ignore_index=True)
pd_uni = reach.sort_values("node").reset_index(drop=True)
# (3) UNION ALL with a path guard
fr = pd.DataFrame({"node": ["A"], "path": [",A,"]})
rows = [fr]
while not fr.empty:
    nx = fr.merge(edges, left_on="node", right_on="src")
    nx = nx[[("," + d + ",") not in p for d, p in zip(nx["dst"], nx["path"])]]
    fr = pd.DataFrame({"node": nx["dst"].to_numpy(), "path": (nx["path"] + nx["dst"] + ",").to_numpy()})
    rows.append(fr)
pd_path = pd.concat(rows, ignore_index=True).sort_values("path").reset_index(drop=True)
```

**Example:** by hand from A.
- Round 0: A. Round 1: B, C. Round 2: D (from B) and D (from C). Round 3: A and A (from each D). Round 4: B, C, B, C ...
- `UNION ALL` with cap 4 gives 11 rows: A; BC; DD; AA; BBCC. D is in the output twice because it has two routes, and the later rounds multiply as the loop repeats. Without the cap it never ends: the run printed `ABCDDAABCBCD` before `LIMIT 12` cut it off.
- `UNION` on the node only: round 3 would produce A, but A was already produced in round 0, so it is dropped; the new round is empty and the query ends with A, B, C, D.
- `UNION` with `(node, depth)`: A at depth 0 and A at depth 3 are different rows, so nothing is dropped. The run returned 15 distinct rows and was still growing (`('A', 9), ('B', 10), ('C', 10)` at the end) when `LIMIT` stopped it.
- Path guard: routes ,A, ,A,B, ,A,B,D, ,A,C, ,A,C,D, (5 rows). The step D to A is refused because A is already on the path. D appears twice again, once per route, which is correct for a route list and wrong for a reachability list.

**Code:** run with `python3 -I`. The asserts compare the SQL and pandas results of variants 1, 2 and 3, each sorted as in its SQL `ORDER BY`; the unbounded variants are shown with `LIMIT` only.
```python
# Q7: UNION versus UNION ALL in recursion on a graph with two routes to D and a cycle D -> A
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE edges(src TEXT, dst TEXT);
INSERT INTO edges VALUES ('A','B'), ('A','C'), ('B','D'), ('C','D'), ('D','A');
"""
SQL_ALL_CAP = """
WITH RECURSIVE r(node, depth) AS (
  SELECT 'A', 0
  UNION ALL
  SELECT e.dst, r.depth + 1 FROM edges e JOIN r ON e.src = r.node
  WHERE r.depth < 4                                      -- depth cap: the only stop
)
SELECT node, depth FROM r ORDER BY depth, node
"""
SQL_UNION = """
WITH RECURSIVE r(node) AS (
  SELECT 'A'
  UNION                                                  -- drops a row that was already produced
  SELECT e.dst FROM edges e JOIN r ON e.src = r.node
)
SELECT node FROM r ORDER BY node
"""
SQL_UNION_DEPTH = """
WITH RECURSIVE r(node, depth) AS (
  SELECT 'A', 0
  UNION                                                  -- depth makes every row new, so nothing is dropped
  SELECT e.dst, r.depth + 1 FROM edges e JOIN r ON e.src = r.node
)
SELECT node, depth FROM r LIMIT 15                       -- LIMIT is the only reason this demo stops
"""
SQL_UNION_ALL_LOOP = """
WITH RECURSIVE r(node) AS (
  SELECT 'A' UNION ALL SELECT e.dst FROM edges e JOIN r ON e.src = r.node
)
SELECT node FROM r LIMIT 12
"""
SQL_PATH = """
WITH RECURSIVE r(node, path) AS (
  SELECT 'A', ',A,'
  UNION ALL
  SELECT e.dst, r.path || e.dst || ','
  FROM edges e JOIN r ON e.src = r.node
  WHERE instr(r.path, ',' || e.dst || ',') = 0           -- visited check on the path
)
SELECT node, path FROM r ORDER BY path
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
cap = pd.read_sql_query(SQL_ALL_CAP, con)
print("UNION ALL, depth cap 4:", cap.groupby("depth")["node"].apply(lambda s: "".join(s)).to_dict(), "| rows:", len(cap), "| D appears", int((cap.node == "D").sum()), "times")
uni = pd.read_sql_query(SQL_UNION, con)
print("UNION, node only:", uni["node"].tolist())
print("UNION ALL, no guard, LIMIT 12:", "".join(r[0] for r in con.execute(SQL_UNION_ALL_LOOP)))
ud = con.execute(SQL_UNION_DEPTH).fetchall()
print("UNION with a depth column, LIMIT 15:", len(ud), "rows, all distinct:", len(set(ud)) == len(ud), "| last 3:", ud[-3:])
path = pd.read_sql_query(SQL_PATH, con)
print("UNION ALL with path guard:", path["path"].tolist())

edges = pd.read_sql_query("SELECT * FROM edges", con)
# pd:main
step = lambda f: f.merge(edges, left_on="node", right_on="src")[["dst"]].rename(columns={"dst": "node"})
# (1) UNION ALL with a depth cap: no de-duplication
frontier = pd.DataFrame({"node": ["A"], "depth": 0})
frames = [frontier]
for d in range(1, 5):
    frontier = step(frontier).assign(depth=d)
    frames.append(frontier)
pd_cap = pd.concat(frames, ignore_index=True).sort_values(["depth", "node"]).reset_index(drop=True)
# (2) UNION on a key-only row: keep a visited frame, anti-join the new rows against it
reach = pd.DataFrame({"node": ["A"]})
frontier = reach
while not frontier.empty:
    nxt = step(frontier).drop_duplicates()
    frontier = nxt[~nxt["node"].isin(reach["node"])]
    reach = pd.concat([reach, frontier], ignore_index=True)
pd_uni = reach.sort_values("node").reset_index(drop=True)
# (3) UNION ALL with a path guard
fr = pd.DataFrame({"node": ["A"], "path": [",A,"]})
rows = [fr]
while not fr.empty:
    nx = fr.merge(edges, left_on="node", right_on="src")
    nx = nx[[("," + d + ",") not in p for d, p in zip(nx["dst"], nx["path"])]]
    fr = pd.DataFrame({"node": nx["dst"].to_numpy(), "path": (nx["path"] + nx["dst"] + ",").to_numpy()})
    rows.append(fr)
pd_path = pd.concat(rows, ignore_index=True).sort_values("path").reset_index(drop=True)
# pd:end
pd.testing.assert_frame_equal(pd_cap[["node", "depth"]], cap, check_dtype=False)
pd.testing.assert_frame_equal(pd_uni, uni, check_dtype=False)
pd.testing.assert_frame_equal(pd_path, path, check_dtype=False)
print("pandas equals SQL for all three (each sorted as its SQL ORDER BY)")

# Edge cases: duplicate edge, NULL destination, start node not in the graph
con.execute("CREATE TABLE edges_dup AS SELECT * FROM edges"); con.execute("INSERT INTO edges_dup VALUES ('A','B')")
dup_path = con.execute(SQL_PATH.replace("edges", "edges_dup")).fetchall()
dup_uni = con.execute(SQL_UNION.replace("edges", "edges_dup")).fetchall()
print("duplicate edge A->B: path rows", len(path), "->", len(dup_path), "| UNION node rows", len(uni), "->", len(dup_uni))
con.execute("CREATE TABLE edges_null AS SELECT * FROM edges"); con.execute("INSERT INTO edges_null VALUES ('D', NULL)")
print("edge D -> NULL, UNION:", con.execute(SQL_UNION.replace("edges", "edges_null").replace("ORDER BY node", "ORDER BY node IS NULL, node")).fetchall())
print("start node 'Z' not in the graph (literal anchor):", con.execute(SQL_UNION.replace("SELECT 'A'", "SELECT 'Z'")).fetchall())
print("start node 'Z' (anchor from the edge table):", con.execute(SQL_UNION.replace("SELECT 'A'", "SELECT dst FROM edges WHERE src = 'Z'")).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
UNION ALL, depth cap 4: {0: 'A', 1: 'BC', 2: 'DD', 3: 'AA', 4: 'BBCC'} | rows: 11 | D appears 2 times
UNION, node only: ['A', 'B', 'C', 'D']
UNION ALL, no guard, LIMIT 12: ABCDDAABCBCD
UNION with a depth column, LIMIT 15: 15 rows, all distinct: True | last 3: [('A', 9), ('B', 10), ('C', 10)]
UNION ALL with path guard: [',A,', ',A,B,', ',A,B,D,', ',A,C,', ',A,C,D,']
pandas equals SQL for all three (each sorted as its SQL ORDER BY)
duplicate edge A->B: path rows 5 -> 7 | UNION node rows 4 -> 4
edge D -> NULL, UNION: [('A',), ('B',), ('C',), ('D',), (None,)]
start node 'Z' not in the graph (literal anchor): [('Z',)]
start node 'Z' (anchor from the edge table): []
asserts passed
```

**Edge cases:**
- Duplicate edge (a second `A -> B` row): route rows grow from 5 to 7 (A>B and A>B>D are each duplicated), while the `UNION` node list stays at 4 rows. So `UNION` also cleans duplicate edges, a path guard does not. Dedupe the edge table first if duplicates are noise (Q28).
- NULL destination (`D -> NULL`): the NULL node is produced as a row (5 rows, one is `None`) and then goes nowhere, because `src = NULL` never matches. `UNION` treats the NULLs as one value.
- Start node not in the graph: with a literal anchor (`SELECT 'Z'`) you still get a row for Z; anchoring from the edge table (`SELECT dst FROM edges WHERE src = 'Z'`) gives an empty result. Pick on purpose.
- Empty edge table: the anchor alone, one row.
- `UNION` dedups on the entire row, so two different routes that arrive at D with the same extra columns collapse into one. Whether that is wanted decides the choice (Q10 shows a bill of materials where collapsing is a bug).

**Then explain:**
- Cycle protection by `UNION` works only when the row is exactly the identity you care about (a node id). A depth, path or cost column makes each row new. The PostgreSQL documentation (opened) says the same and adds that a `LIMIT` on the parent query can stop a loop in a test but is not to be relied on.
- Cost: `UNION` must keep and compare against every row produced so far (SQLite's documentation says `UNION ALL` needs little memory); `UNION ALL` only holds the current queue. I did not measure it here, Q29 compares route enumeration with distinct reachability.
- Use `UNION` for reachability and connected components (Q16). Use `UNION ALL` plus a visited path or a depth cap when the route itself matters (Q17, Q23).
- Other engines (not executed): MySQL and PostgreSQL accept `UNION` or `UNION ALL` (also written `UNION DISTINCT`) between the anchor and the recursive member; SQL Server (from memory) accepts only `UNION ALL` in a recursive CTE; PostgreSQL 14 and later has a `CYCLE ... SET ... USING` clause that tracks visited rows for you; Oracle uses `CONNECT BY NOCYCLE`. SQLite 3.45.1 has no `CYCLE` clause (syntax error, per the sources note's run).

**Follow-ups:**
- Why not just add `DISTINCT` in the recursive member? MySQL forbids it there (opened docs), SQLite's duplicate removal is only through `UNION`, and it would only dedupe within one round, not across rounds.
- How do you show the cycle edge itself? Keep the path guard but emit the row with `cycle = 1` when the next node is already on the path (PostgreSQL's `CYCLE` clause does that automatically).
- Which one is faster? `UNION ALL` per row; but `UNION` can produce far fewer rows when routes multiply, so total work can go either way.

**Common mistakes:**
- Using `UNION ALL` on a graph and hoping the depth column will fix it.
- Using `UNION` with a depth column and believing it is protected from cycles.
- Not noticing that `UNION` also merges legitimately equal rows.
- Treating the output of a path enumeration as a list of distinct nodes (D appears once per route).

### Q8 ⭐⭐⭐ 🟡 Debug: my recursive query never terminates. The query lists the subtree of manager 1 on employees(emp_id, manager_id) using UNION ALL, and the data has a loop (emp 7 reports to 9 and 9 reports to 7) plus an employee who is their own manager. Reproduce the hang safely (a LIMIT on the recursive select, or a depth counter), find the bad rows with a query, and fix the query three ways: a depth cap, a visited-path check (path NOT LIKE '%,' || id || ',%'), and UNION on a key-only row. Name the engine-level guards: SQLite LIMIT inside the recursive select, MySQL cte_max_recursion_depth and max_execution_time, SQL Server OPTION (MAXRECURSION n), PostgreSQL CYCLE clause, Oracle NOCYCLE (all hedged, not executed).
**Asked at:** cycle-handling guides (search snippets only, not opened: manual path string or array of visited ids with a flag, the itprotoday 'Cycling with CTEs' article, Oracle NOCYCLE and CONNECT_BY_ISCYCLE docs, PostgreSQL CYCLE); the opened PostgreSQL page says UNION cannot stop a cycle when a depth column makes every row unique; guides and documentation, not candidate reports; data engineer and analyst rounds
**Say this first (1 line):** First a premise check: with one `manager_id` per employee, the 7-and-9 loop and the self-managed row cannot hang "the subtree of manager 1", because nobody on a loop reports into it from outside (my run: boss 1 returns 5 rows and stops); the query hangs when the start is on a loop, when the CEO himself sits in a loop, or when you walk upward from below a loop; so I reproduce it with a `LIMIT` inside the recursive select, find the bad rows with an upward walk, and fix it with a depth cap, a visited-path check, or `UNION` on a key-only row, knowing that only the last two give the right answer.

**Schema and sample data:** twelve employees. A normal tree under Tim (1): 2, 3 (under 1), 4, 5 (under 2), 6 (under 3). A loop: 7 reports to 9 and 9 reports to 7. Below the loop: 8 reports to 7, 10 reports to 8. A self-managed employee: 15 reports to 15, with 16 below him.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES
 (1, NULL), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3),
 (7, 9), (9, 7), (8, 7), (10, 8), (15, 15), (16, 15);
```

**SQL answer:** the reproduction `SQL_HANG` (with `LIMIT 25` inside the recursive select as a safety net, otherwise it would run until memory or a timeout):
```sql
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  LIMIT 25                                              -- safety net for the reproduction only
)
SELECT emp_id, level FROM sub
```
The bad-row finder `SQL_BAD`, an upward walk that reports the start ids which meet themselves again (loop members, and the self-managed one):
```sql
WITH RECURSIVE up(start_id, cur_id, depth) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.start_id, e.manager_id, u.depth + 1
  FROM up u JOIN employees e ON e.emp_id = u.cur_id
  WHERE e.manager_id IS NOT NULL AND u.depth < 20      -- the finder needs its own guard
)
SELECT DISTINCT start_id AS emp_id,
       CASE WHEN start_id = (SELECT manager_id FROM employees WHERE emp_id = start_id) THEN 'self-managed' ELSE 'in a loop' END AS problem
FROM up WHERE cur_id = start_id ORDER BY emp_id
```
Fix 1, depth cap `SQL_DEPTH`:
```sql
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < :cap                                  -- fix 1: depth cap
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
```
Fix 2, visited-path check `SQL_PATH` (the boss is seeded into the path so he is not listed as his own report):
```sql
WITH RECURSIVE sub(emp_id, level, path) AS (
  SELECT emp_id, 1, ',' || :boss || ',' || emp_id || ',' FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1, s.path || e.emp_id || ','
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.path NOT LIKE '%,' || e.emp_id || ',%'        -- fix 2: visited-path check (boss seeded in the path)
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
```
Fix 3, `UNION` on a key-only row `SQL_UNION`:
```sql
WITH RECURSIVE sub(emp_id) AS (
  SELECT emp_id FROM employees WHERE manager_id = :boss
  UNION                                                 -- fix 3: key-only row, repeats are dropped
  SELECT e.emp_id FROM employees e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id FROM sub ORDER BY emp_id
```

**pandas answer:** the same walk with a visited set; seeding the boss as visited matches the path check, not seeding matches `UNION`. Identical to the Code block:
```py
edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
def subtree(boss, seed_boss=True):
    frontier = edges[edges["manager_id"] == boss][["emp_id"]].assign(level=1)
    seen = {boss} if seed_boss else set()
    out = []
    while not frontier.empty:
        frontier = frontier[~frontier["emp_id"].isin(seen)]          # visited set instead of a path string
        seen |= set(frontier["emp_id"])
        out.append(frontier)
        frontier = (frontier.rename(columns={"emp_id": "manager_id"})
                    .merge(edges, on="manager_id")[["emp_id", "level"]].assign(level=lambda x: x["level"] + 1))
    return pd.concat(out, ignore_index=True).sort_values(["level", "emp_id"]).reset_index(drop=True)
pd_path = subtree(7)                       # same as the path check: the boss is seeded as visited
pd_union = subtree(7, seed_boss=False)     # same as UNION on a key: the boss is not seeded
```

**Example:** boss 7.
- Direct reports of 7: employees 8 and 9. Round 2: reports of 8 (employee 10) and reports of 9 (employee 7, because 7 reports to 9). Round 3: reports of 10 (none), reports of 7 (8 and 9 again), and so on forever. The unguarded run printed `(8, 1), (9, 1), (10, 2), (7, 2), (8, 3), (9, 3), (10, 4), (7, 4) ...` until `LIMIT 25`.
- Depth cap 4: finishes with 8 rows for only 4 distinct people (8, 9, 7, 10 twice each). It terminates but it counts the same person every lap, so a count or a salary sum from it is wrong.
- Path check: 9 (path `,7,9,`) and 8 are reported; the step from 9 to employee 7 is refused because 7 is already in the path; 8 leads to 10. Result: 8 and 9 at level 1, 10 at level 2. That is the loop-aware answer.
- `UNION` on `emp_id`: 7, 8, 9, 10. It terminates and has no duplicates, but it lists 7 as his own subordinate because he does report to 9 (the boss was not seeded). Decide which you want, and say it.
- Boss 15: his only direct reports are himself (15) and 16, and 15 reports to himself, so the unguarded rows are `(15, 1), (16, 1), (15, 2), (16, 2) ...`.
- Bad rows by the finder: 7 and 9 are `in a loop`, 15 is `self-managed`. Employees 8, 10 and 16 hang an upward walk but are not on a loop themselves, so they are not listed; they are the victims.

**Code:** run with `python3 -I`. Every unguarded query is bounded by `LIMIT`. The asserts compare the pandas visited-set results with the SQL path check (ordered by level, emp_id) and with the sorted `UNION` ids.
```python
# Q8: debug a recursive query that never terminates: reproduce safely, find the bad rows, three fixes
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES
 (1, NULL), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3),
 (7, 9), (9, 7),            -- 7 and 9 report to each other
 (8, 7), (10, 8),           -- below the loop
 (15, 15), (16, 15);        -- 15 is his own manager, 16 reports to him
"""
SQL_HANG = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  LIMIT 25                                              -- safety net for the reproduction only
)
SELECT emp_id, level FROM sub
"""
SQL_DEPTH = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < :cap                                  -- fix 1: depth cap
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
"""
SQL_PATH = """
WITH RECURSIVE sub(emp_id, level, path) AS (
  SELECT emp_id, 1, ',' || :boss || ',' || emp_id || ',' FROM employees WHERE manager_id = :boss
  UNION ALL
  SELECT e.emp_id, s.level + 1, s.path || e.emp_id || ','
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.path NOT LIKE '%,' || e.emp_id || ',%'        -- fix 2: visited-path check (boss seeded in the path)
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
"""
SQL_UNION = """
WITH RECURSIVE sub(emp_id) AS (
  SELECT emp_id FROM employees WHERE manager_id = :boss
  UNION                                                 -- fix 3: key-only row, repeats are dropped
  SELECT e.emp_id FROM employees e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id FROM sub ORDER BY emp_id
"""
SQL_BAD = """
WITH RECURSIVE up(start_id, cur_id, depth) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.start_id, e.manager_id, u.depth + 1
  FROM up u JOIN employees e ON e.emp_id = u.cur_id
  WHERE e.manager_id IS NOT NULL AND u.depth < 20      -- the finder needs its own guard
)
SELECT DISTINCT start_id AS emp_id,
       CASE WHEN start_id = (SELECT manager_id FROM employees WHERE emp_id = start_id) THEN 'self-managed' ELSE 'in a loop' END AS problem
FROM up WHERE cur_id = start_id ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

# Premise check: does the subtree of manager 1 hang? (an unguarded query, safety LIMIT only)
r1 = con.execute(SQL_HANG, {"boss": 1}).fetchall()
print("boss 1 unguarded, LIMIT 25:", len(r1), "rows (fewer than 25 means it ended by itself):", sorted(e for e, _ in r1))
r7 = con.execute(SQL_HANG, {"boss": 7}).fetchall()
print("boss 7 unguarded, LIMIT 25:", len(r7), "rows, first 10:", r7[:10])
r15 = con.execute(SQL_HANG, {"boss": 15}).fetchall()
print("boss 15 unguarded, LIMIT 25:", len(r15), "rows, first 6:", r15[:6])

print("bad rows:", con.execute(SQL_BAD).fetchall())

d = pd.read_sql_query(SQL_DEPTH, con, params={"boss": 7, "cap": 4})
p = pd.read_sql_query(SQL_PATH, con, params={"boss": 7})
u = pd.read_sql_query(SQL_UNION, con, params={"boss": 7})
print("fix 1 depth cap 4:", len(d), "rows, distinct people", d.emp_id.nunique(), "->", d.emp_id.tolist())
print("fix 2 path check:", p.values.tolist())
print("fix 3 UNION key-only:", u.emp_id.tolist(), "(7 is in his own subtree because he reports to 9)")

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
def subtree(boss, seed_boss=True):
    frontier = edges[edges["manager_id"] == boss][["emp_id"]].assign(level=1)
    seen = {boss} if seed_boss else set()
    out = []
    while not frontier.empty:
        frontier = frontier[~frontier["emp_id"].isin(seen)]          # visited set instead of a path string
        seen |= set(frontier["emp_id"])
        out.append(frontier)
        frontier = (frontier.rename(columns={"emp_id": "manager_id"})
                    .merge(edges, on="manager_id")[["emp_id", "level"]].assign(level=lambda x: x["level"] + 1))
    return pd.concat(out, ignore_index=True).sort_values(["level", "emp_id"]).reset_index(drop=True)
pd_path = subtree(7)                       # same as the path check: the boss is seeded as visited
pd_union = subtree(7, seed_boss=False)     # same as UNION on a key: the boss is not seeded
# pd:end
pd.testing.assert_frame_equal(pd_path, p, check_dtype=False)                 # both ordered by level, emp_id
assert sorted(pd_union["emp_id"]) == u["emp_id"].tolist()                    # UNION answer, as a sorted id list
print("pandas visited-set versions equal the SQL path check and the UNION answer")

# a loop that includes the CEO: the 'subtree of manager 1' really hangs
con.execute("UPDATE employees SET manager_id = 5 WHERE emp_id = 1")
rr = con.execute(SQL_HANG, {"boss": 1}).fetchall()
print("CEO reports to his own descendant 5; boss 1 unguarded, LIMIT 25:", len(rr), "rows (hit the limit)")
print("same data, path check:", con.execute(SQL_PATH, {"boss": 1}).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
boss 1 unguarded, LIMIT 25: 5 rows (fewer than 25 means it ended by itself): [2, 3, 4, 5, 6]
boss 7 unguarded, LIMIT 25: 25 rows, first 10: [(8, 1), (9, 1), (10, 2), (7, 2), (8, 3), (9, 3), (10, 4), (7, 4), (8, 5), (9, 5)]
boss 15 unguarded, LIMIT 25: 25 rows, first 6: [(15, 1), (16, 1), (15, 2), (16, 2), (15, 3), (16, 3)]
bad rows: [(7, 'in a loop'), (9, 'in a loop'), (15, 'self-managed')]
fix 1 depth cap 4: 8 rows, distinct people 4 -> [8, 9, 7, 10, 8, 9, 7, 10]
fix 2 path check: [[8, 1], [9, 1], [10, 2]]
fix 3 UNION key-only: [7, 8, 9, 10] (7 is in his own subtree because he reports to 9)
pandas visited-set versions equal the SQL path check and the UNION answer
CEO reports to his own descendant 5; boss 1 unguarded, LIMIT 25: 25 rows (hit the limit)
same data, path check: [(2, 1), (3, 1), (4, 2), (5, 2), (6, 2)]
asserts passed
```

**Edge cases:**
- Premise check (run): `boss 1 unguarded` returned 5 rows (2, 3, 4, 5, 6) and ended by itself, so on this data the 7 and 9 loop is not what hangs a top-down query from manager 1. Cause: each employee has one manager, so a loop has no entry point from outside. A top-down query from manager 1 can only hang if manager 1 is himself inside a loop. I tested that by setting Tim's manager to 5 (his own descendant): unguarded it hit the limit (25 rows), and the path check returned 2, 3, 4, 5, 6.
- A node that reports into a loop only hangs queries that walk up (Q5) or that start from the loop.
- The depth cap must be higher than the true depth, or it truncates the answer silently; it cannot tell a deep tree from a loop.
- `NOT LIKE '%,' || id || ',%'` needs the comma on both sides, otherwise id 7 matches 17 and 70. Note `LIKE` treats `_` and `%` as wildcards (fine for numeric ids, not for names).
- The finder itself needs a guard (`depth < 20`), or the diagnostic query would hang too.
- NULL manager: the CEO's NULL is excluded in the finder (`manager_id IS NOT NULL`) and never matches in the join.

**Then explain:**
- Reproduce safely: `LIMIT` inside the recursive select in SQLite (opened documentation), or a depth counter. Never test an unguarded recursive query without one.
- Find the bad rows with data checks before you patch the query (Q15 gives the whole audit).
- Three fixes with different meanings: depth cap (terminates, duplicates), path check (correct for routes and loops, costs a growing string), `UNION` on a key (correct for reachability, remembers every row).
- Engine-level guards, hedged and not executed here: MySQL stops at `cte_max_recursion_depth` (default 1000, then an error) and `max_execution_time`; SQL Server stops at `OPTION (MAXRECURSION n)` with error 530 (default 100, 0 means unlimited; from search snippets); PostgreSQL 14+ has a `CYCLE` clause; Oracle `CONNECT BY NOCYCLE` with `CONNECT_BY_ISCYCLE` (snippets). They are a net, not a cure: the query fails instead of looping.

**Follow-ups:**
- How do you fix the data? Set the loop's manager to NULL or to the real manager, and add a check (trigger or load-time audit) that rejects a manager who is a descendant.
- Can the database prevent it? A foreign key stops orphans, but not loops; `CHECK (emp_id <> manager_id)` stops self-managers only.
- Which fix would you ship? Path check for correctness, plus a depth cap as a seat belt.

**Common mistakes:**
- Blaming the loop without checking that the start node can reach it.
- A depth cap and then believing the counts.
- A path check with no delimiters.
- Using `UNION` with a depth column.
- Leaving a diagnostic query unguarded.

### Q9 ⭐⭐⭐ 🟡 Org-size roll-up: employees(emp_id, manager_id, name, salary). For every manager return the number of reports at any depth and the total salary of that subtree, and then only the managers with at least 3 reports at any depth. Show the closure-style approach (a recursive CTE producing ancestor, descendant pairs, then GROUP BY ancestor), why a plain GROUP BY manager_id counts direct reports only, and why the aggregate must be applied outside the recursive CTE (aggregates are not allowed in the recursive member). Include the pandas version (iterative expansion of the pairs frame then groupby) and assert equality.
**Asked at:** employee-manager hierarchy guides: jdsatpathy Substack 'Find All Managers of an Employee Up to the CEO' (opened; anchor at the employee, join employee to manager, no cycle guard, UNION ALL), DataVidhya recursive hierarchy pattern page (opened; reports under a manager, ancestors of a category, paths in a dependency graph, depth tracking and cycle detection), and search snippets of datadriven.io and a Medium recursive CTE interview post (not opened); guides, not candidate reports; analyst and data engineer rounds at product companies, GCCs and consulting firms
**Say this first (1 line):** Build the closure pairs (ancestor, descendant) with a recursive CTE, then do the counting and summing outside the CTE with `GROUP BY ancestor` after joining the descendants' salaries; a plain `GROUP BY manager_id` counts direct reports only, and the aggregate cannot live in the recursive member because SQLite and MySQL forbid aggregates there.

**Schema and sample data:** the Q4 tree with two data traps: Ivy (12) has a NULL salary and Jay (13) is an orphan (manager 99 missing). Salaries are toy column data.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1, NULL, 'Tim', 500), (2, 1, 'Radha', 300), (3, 1, 'Hari', 300), (4, 2, 'Asha', 100),
 (5, 3, 'Ben', 200), (6, 3, 'Chen', 200), (7, 5, 'Dev', 150), (8, 5, 'Esha', 150),
 (9, 6, 'Farid', 120), (10, 7, 'Gita', 100), (11, 7, 'Hugo', 100),
 (12, 10, 'Ivy', NULL), (13, 99, 'Jay', 80);
```

**SQL answer:** `SQL_MAIN` in the Code block (one row per employee who has at least one report; `reports_salary` excludes the manager's own salary, `subtree_salary` includes it):
```sql
WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT manager_id, emp_id FROM employees WHERE manager_id IS NOT NULL
  UNION                                                   -- pairs are unique, so a loop cannot repeat forever
  SELECT p.ancestor, e.emp_id FROM pairs p JOIN employees e ON e.manager_id = p.descendant
)
SELECT m.emp_id, m.name,
       COUNT(*) AS reports,
       COALESCE(SUM(d.salary), 0) AS reports_salary,
       m.salary + COALESCE(SUM(d.salary), 0) AS subtree_salary
FROM pairs p
JOIN employees m ON m.emp_id = p.ancestor
JOIN employees d ON d.emp_id = p.descendant
GROUP BY m.emp_id, m.name, m.salary
ORDER BY m.emp_id
```
The "at least 3 reports" filter, `SQL_TOP3`, is the same query with `HAVING COUNT(*) >= 3` after the `GROUP BY` (the Code block builds it by inserting that line). The direct-only query, for contrast, is `SELECT manager_id, COUNT(*) FROM employees GROUP BY manager_id`.
- The CTE uses `UNION`, not `UNION ALL`: pairs are the identity, so duplicates and loops cannot grow forever (Q7). On a clean tree there is exactly one path to each descendant, so `UNION ALL` would give the same counts; on a DAG it would double count.
- The `GROUP BY` is outside the CTE because the recursive member may not aggregate (SQLite: `recursive aggregate queries not supported`, Q1).
- `COALESCE(SUM(...), 0)`: a manager whose only report has a NULL salary would otherwise show NULL.
- The inner join to the manager row drops the pair (99, 13), because there is no employee 99 to report on.

**pandas answer:** expand the pairs frame level by level (one merge per level, keeping only pairs not seen before), then merge in both salaries and group, identical to the Code block:
```py
def pairs_of(employees):
    e0 = (employees.dropna(subset=["manager_id"])[["manager_id", "emp_id"]]
          .astype("int64").rename(columns={"manager_id": "ancestor", "emp_id": "descendant"}))
    pairs, frontier = e0, e0
    while not frontier.empty:
        nxt = (frontier.merge(e0.rename(columns={"ancestor": "descendant", "descendant": "d2"}), on="descendant")
               [["ancestor", "d2"]].rename(columns={"d2": "descendant"}).drop_duplicates())
        frontier = nxt[~pd.MultiIndex.from_frame(nxt).isin(pd.MultiIndex.from_frame(pairs))]
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    return pairs
def rollup(employees, pairs):
    x = (pairs.merge(employees[["emp_id", "name", "salary"]], left_on="ancestor", right_on="emp_id")
              .merge(employees[["emp_id", "salary"]].rename(columns={"emp_id": "d_id", "salary": "d_salary"}),
                     left_on="descendant", right_on="d_id"))
    g = (x.groupby(["emp_id", "name", "salary"], as_index=False, dropna=False)    # dropna=False: a NaN salary must not drop the group
          .agg(reports=("d_id", "size"), reports_salary=("d_salary", "sum")))
    g["subtree_salary"] = g["salary"] + g["reports_salary"]
    return g[["emp_id", "name", "reports", "reports_salary", "subtree_salary"]].sort_values("emp_id").reset_index(drop=True)
pd_df = rollup(employees, pairs_of(employees))
pd_top3 = pd_df[pd_df["reports"] >= 3].reset_index(drop=True)
direct = employees.groupby("manager_id").size()
```

**Example:** by hand for Hari (3).
- Pairs with ancestor 3: direct reports 5 and 6; then 7, 8 (under 5) and 9 (under 6); then 10 and 11 (under 7); then 12 (under 10). That is 8 reports at depth 1 to 4.
- Salaries: 5 is 200, 6 is 200, 7 is 150, 8 is 150, 9 is 120, 10 is 100, 11 is 100, 12 is NULL (ignored by `SUM`): 1020. Subtree total with Hari's own 300: 1320.
- Tim (1): 11 reports (everyone except himself and Jay), reports salary 1720, subtree 2220.
- Managers with at least 3 reports at any depth: Tim (11), Hari (8), Ben (5) and Dev (3). Dev has only two direct reports (Gita and Hugo) but Ivy is below Gita, so he reaches 3.
- A plain `GROUP BY manager_id` says Hari has 2 reports, Ben 2 and Dev 2, and its NULL group (the CEO) shows 1 row; with it nobody would pass a threshold of 3 (the largest direct count is 2).

**Code:** run with `python3 -I`. SQL and pandas are compared after ordering by `emp_id` (full roll-up and the filtered one); a second run on a looped copy checks that both sides still end.
```python
# Q9: org-size roll-up with an ancestor/descendant pairs CTE, aggregated outside; pandas pair expansion
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1, NULL, 'Tim', 500), (2, 1, 'Radha', 300), (3, 1, 'Hari', 300), (4, 2, 'Asha', 100),
 (5, 3, 'Ben', 200), (6, 3, 'Chen', 200), (7, 5, 'Dev', 150), (8, 5, 'Esha', 150),
 (9, 6, 'Farid', 120), (10, 7, 'Gita', 100), (11, 7, 'Hugo', 100),
 (12, 10, 'Ivy', NULL),          -- salary not recorded
 (13, 99, 'Jay', 80);            -- orphan: manager 99 does not exist
"""
SQL_MAIN = """
WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT manager_id, emp_id FROM employees WHERE manager_id IS NOT NULL
  UNION                                                   -- pairs are unique, so a loop cannot repeat forever
  SELECT p.ancestor, e.emp_id FROM pairs p JOIN employees e ON e.manager_id = p.descendant
)
SELECT m.emp_id, m.name,
       COUNT(*) AS reports,
       COALESCE(SUM(d.salary), 0) AS reports_salary,
       m.salary + COALESCE(SUM(d.salary), 0) AS subtree_salary
FROM pairs p
JOIN employees m ON m.emp_id = p.ancestor
JOIN employees d ON d.emp_id = p.descendant
GROUP BY m.emp_id, m.name, m.salary
ORDER BY m.emp_id
"""
SQL_TOP3 = SQL_MAIN.replace("GROUP BY m.emp_id, m.name, m.salary\n", "GROUP BY m.emp_id, m.name, m.salary\nHAVING COUNT(*) >= 3\n")
assert SQL_TOP3 != SQL_MAIN
SQL_DIRECT = "SELECT manager_id, COUNT(*) AS direct_reports FROM employees GROUP BY manager_id ORDER BY manager_id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
top3 = pd.read_sql_query(SQL_TOP3, con)
print(sql_df.to_string(index=False))
print("managers with >= 3 reports at any depth:", top3["emp_id"].tolist())
print("plain GROUP BY manager_id (direct only):", con.execute(SQL_DIRECT).fetchall())

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def pairs_of(employees):
    e0 = (employees.dropna(subset=["manager_id"])[["manager_id", "emp_id"]]
          .astype("int64").rename(columns={"manager_id": "ancestor", "emp_id": "descendant"}))
    pairs, frontier = e0, e0
    while not frontier.empty:
        nxt = (frontier.merge(e0.rename(columns={"ancestor": "descendant", "descendant": "d2"}), on="descendant")
               [["ancestor", "d2"]].rename(columns={"d2": "descendant"}).drop_duplicates())
        frontier = nxt[~pd.MultiIndex.from_frame(nxt).isin(pd.MultiIndex.from_frame(pairs))]
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    return pairs
def rollup(employees, pairs):
    x = (pairs.merge(employees[["emp_id", "name", "salary"]], left_on="ancestor", right_on="emp_id")
              .merge(employees[["emp_id", "salary"]].rename(columns={"emp_id": "d_id", "salary": "d_salary"}),
                     left_on="descendant", right_on="d_id"))
    g = (x.groupby(["emp_id", "name", "salary"], as_index=False, dropna=False)    # dropna=False: a NaN salary must not drop the group
          .agg(reports=("d_id", "size"), reports_salary=("d_salary", "sum")))
    g["subtree_salary"] = g["salary"] + g["reports_salary"]
    return g[["emp_id", "name", "reports", "reports_salary", "subtree_salary"]].sort_values("emp_id").reset_index(drop=True)
pd_df = rollup(employees, pairs_of(employees))
pd_top3 = pd_df[pd_df["reports"] >= 3].reset_index(drop=True)
direct = employees.groupby("manager_id").size()
# pd:end
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)          # both ordered by emp_id
pd.testing.assert_frame_equal(pd_top3, top3, check_dtype=False)
print("pandas equals SQL (ordered by emp_id)")
print("pandas groupby(manager_id) direct counts (NaN key dropped):", direct.to_dict())

# Edge cases: pairs for the orphan manager 99, a loop, a NULL salary
pairs = pd.read_sql_query("""WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT manager_id, emp_id FROM employees WHERE manager_id IS NOT NULL
  UNION SELECT p.ancestor, e.emp_id FROM pairs p JOIN employees e ON e.manager_id = p.descendant)
SELECT * FROM pairs""", con)
print("pair rows:", len(pairs), "| pairs whose ancestor is 99:", pairs.loc[pairs.ancestor == 99].values.tolist(), "(dropped by the inner join to the manager row)")
print("Gita (10) reports_salary:", int(sql_df.loc[sql_df.emp_id == 10, "reports_salary"].iloc[0]), "(her only report Ivy has a NULL salary)")
con.execute("UPDATE employees SET manager_id = 12 WHERE emp_id = 5")      # loop 5 -> 7 -> 10 -> 12 -> 5
loop_df = pd.read_sql_query(SQL_MAIN, con)
loop_pd = rollup(pd.read_sql_query("SELECT * FROM employees", con), pairs_of(pd.read_sql_query("SELECT * FROM employees", con)))
pd.testing.assert_frame_equal(loop_pd, loop_df, check_dtype=False)
print("with a loop 5-7-10-12-5 the UNION version still ends:", loop_df.loc[loop_df.emp_id.isin([5, 7, 10, 12]), ["emp_id", "reports"]].values.tolist(), "(each loop member counts himself)")
print("asserts passed")
```

**Output (my run):**
```text
 emp_id  name  reports  reports_salary  subtree_salary
      1   Tim       11            1720            2220
      2 Radha        1             100             400
      3  Hari        8            1020            1320
      5   Ben        5             500             700
      6  Chen        1             120             320
      7   Dev        3             200             350
     10  Gita        1               0             100
managers with >= 3 reports at any depth: [1, 3, 5, 7]
plain GROUP BY manager_id (direct only): [(None, 1), (1, 2), (2, 1), (3, 2), (5, 2), (6, 1), (7, 2), (10, 1), (99, 1)]
pandas equals SQL (ordered by emp_id)
pandas groupby(manager_id) direct counts (NaN key dropped): {1.0: 2, 2.0: 1, 3.0: 2, 5.0: 2, 6.0: 1, 7.0: 2, 10.0: 1, 99.0: 1}
pair rows: 31 | pairs whose ancestor is 99: [[99, 13]] (dropped by the inner join to the manager row)
Gita (10) reports_salary: 0 (her only report Ivy has a NULL salary)
with a loop 5-7-10-12-5 the UNION version still ends: [[5, 6], [7, 6], [10, 6], [12, 6]] (each loop member counts himself)
asserts passed
```

**Edge cases:**
- Leaves are not rows: only employees with at least one report appear. Use a LEFT JOIN from `employees` to the roll-up with `COALESCE(..., 0)` if every employee must appear.
- NULL salary: Ivy's NULL is ignored; Gita's `reports_salary` is 0 only because of `COALESCE` (her sole report is Ivy). Treating "unknown" as 0 is a decision, state it. pandas `sum` skips NaN and gives 0 for an all-NaN group, which matches here.
- Honest surprise from building the pandas version: my first draft grouped by `emp_id, name, salary` and silently lost a manager whose own salary was NaN, because `groupby` drops NaN keys by default. `dropna=False` fixes it (the loop test below exercised it when Ivy became a manager). The SQL `GROUP BY` keeps NULL groups.
- Orphan: the pair (99, 13) exists in the CTE and is dropped by the join. 31 pairs in total here.
- Loop: I made Ben report to Ivy (5, 7, 10, 12 form a loop). The `UNION` pair CTE still ended, and each loop member is counted as his own descendant (reports = 6 for all four); the pandas loop also ended and agreed. A loop in the data does not give a meaningful org size; find it first (Q8, Q15).
- Duplicate employee rows (no primary key) would multiply a subtree; with a primary key on `emp_id` this cannot happen.
- Pandas `groupby(manager_id)` drops the NaN CEO group; SQL shows it as a NULL group of one row.

**Then explain:**
- Closure pairs turn a hierarchy into an ordinary two-column table, so any later question (count, sum, ancestors of X, ancestors who earn more than their reports) is a join and a `GROUP BY`.
- Size: the number of pairs equals the sum of every node's depth, roughly n times the average depth for a balanced tree, but a straight chain of n nodes has n(n-1)/2 pairs (arithmetic, not measured; Q24 and Q29 say more).
- The alternative is a bottom-up roll-up (children first), which needs ordering by depth and a loop; pairs plus one aggregate is simpler and set-based.
- Other engines (not executed): the same query runs in PostgreSQL, MySQL 8 (with `RECURSIVE`) and SQL Server (no `RECURSIVE`; `UNION` is not allowed in its recursive member, so use `UNION ALL` and a depth cap there, from memory); Oracle can use `CONNECT BY` with `CONNECT_BY_ROOT` for the ancestor column (from memory).

**Follow-ups:**
- How would you count only managers' direct reports and all reports side by side? Join the direct counts to the roll-up on `manager_id = emp_id`.
- How do you roll up without pairs? A top-down recursive CTE with the manager chain carried as a column, then group by an ancestor id after exploding; that is the same pairs idea.
- How would a new hire be reflected? Recompute, or maintain a closure table (Q24).

**Common mistakes:**
- `GROUP BY manager_id` and calling it the org size.
- Trying `COUNT(*)` or `SUM` in the recursive member.
- Joining raw `employees` twice and not realizing the pairs table is the whole point.
- Letting a NULL salary turn a subtree total into NULL, or dropping NaN groups in pandas.
- Including the manager's own row in the count without saying so.

### Q10 ⭐⭐⭐ 🟡 Bill of materials explosion with quantity multiplication: parts(part_id, sub_part_id, qty) means one part_id uses qty of sub_part_id, and a part with no row as part_id is a raw component. For top-level product 'BIKE' return the total quantity of every raw component needed to build one bike, multiplying quantities along each path and summing across paths when the same component appears under two sub-assemblies (a wheel shared by a front and rear assembly). Show the path-level rows first, then the SUM per component, and explain why this is a DAG and not a tree, and why UNION would silently collapse legitimate equal rows.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Anchor on the direct components of the product with their quantities, then in each round join the sub-part's own components and multiply the quantity carried so far by the new row's quantity, so every row means "this many of this part per one product via this path"; keep only the raw components (parts that never appear as a `part_id`) and `SUM` the quantity per component, which adds the paths together; use `UNION ALL`, because `UNION` would collapse two legitimately equal rows (the front wheel and the rear wheel) and halve the answer.

**Schema and sample data:** a bike. `BIKE` uses 1 `FRAME`, 1 `FRONT_ASSY`, 1 `REAR_ASSY`, 1 `SEAT`. `FRONT_ASSY` uses 1 `WHEEL`, 1 `FORK`, 1 `BRAKE`. `REAR_ASSY` uses 1 `WHEEL`, 1 `CHAIN`, 1 `BRAKE`. `WHEEL` uses 36 `SPOKE`, 1 `RIM`, 1 `TYRE`. Raw components are the parts that are never a `part_id`: `FRAME`, `SEAT`, `FORK`, `BRAKE`, `CHAIN`, `SPOKE`, `RIM`, `TYRE`.
```sql
CREATE TABLE parts(part_id TEXT, sub_part_id TEXT, qty INTEGER);
INSERT INTO parts VALUES
 ('BIKE','FRAME',1), ('BIKE','FRONT_ASSY',1), ('BIKE','REAR_ASSY',1), ('BIKE','SEAT',1),
 ('FRONT_ASSY','WHEEL',1), ('FRONT_ASSY','FORK',1), ('FRONT_ASSY','BRAKE',1),
 ('REAR_ASSY','WHEEL',1),  ('REAR_ASSY','CHAIN',1), ('REAR_ASSY','BRAKE',1),
 ('WHEEL','SPOKE',36), ('WHEEL','RIM',1), ('WHEEL','TYRE',1);
```

**SQL answer:** the path-level rows first, `SQL_PATHS` in the Code block (`:product` is `BIKE`), every row with the multiplied quantity and its path:
```sql
WITH RECURSIVE bom(part, mult, path) AS (
  SELECT sub_part_id, qty, :product || '>' || sub_part_id FROM parts WHERE part_id = :product
  UNION ALL
  SELECT p.sub_part_id, b.mult * p.qty, b.path || '>' || p.sub_part_id
  FROM parts p JOIN bom b ON p.part_id = b.part
  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0     -- cycle guard: no part inside itself
)
SELECT part, mult, path FROM bom ORDER BY path
```
Then the totals per raw component, `SQL_MAIN`:
```sql
WITH RECURSIVE bom(part, mult, path) AS (
  SELECT sub_part_id, qty, :product || '>' || sub_part_id FROM parts WHERE part_id = :product
  UNION ALL
  SELECT p.sub_part_id, b.mult * p.qty, b.path || '>' || p.sub_part_id
  FROM parts p JOIN bom b ON p.part_id = b.part
  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0
)
SELECT part, SUM(mult) AS total_qty, COUNT(*) AS paths
FROM bom
WHERE NOT EXISTS (SELECT 1 FROM parts x WHERE x.part_id = bom.part)      -- raw component: never used as a parent
GROUP BY part
ORDER BY part
```
The wrong version with `UNION`, `SQL_UNION_BAD`, shown for contrast:
```sql
WITH RECURSIVE bom(part, mult) AS (
  SELECT sub_part_id, qty FROM parts WHERE part_id = :product
  UNION                                                                  -- collapses equal (part, mult) rows from different paths
  SELECT p.sub_part_id, b.mult * p.qty FROM parts p JOIN bom b ON p.part_id = b.part
)
SELECT part, SUM(mult) AS total_qty FROM bom
WHERE NOT EXISTS (SELECT 1 FROM parts x WHERE x.part_id = bom.part)
GROUP BY part ORDER BY part
```
- The quantity multiplies down a path (`b.mult * p.qty`) and adds across paths (`SUM` outside the CTE).
- Raw component test: `NOT EXISTS (SELECT 1 FROM parts x WHERE x.part_id = bom.part)`. Not `NOT IN (SELECT part_id ...)`, which returns nothing if `part_id` ever holds a NULL.
- The path column is a cycle guard: a part may not appear inside itself. A bill of materials with a loop is a data error.

**pandas answer:** the same expansion with merge, a path column for the visited check, and a depth cap equal to the table length, identical to the Code block:
```py
def explode(parts, product):
    frontier = (parts[parts["part_id"] == product]
                .assign(path=lambda d: product + ">" + d["sub_part_id"])
                .rename(columns={"sub_part_id": "part", "qty": "mult"})[["part", "mult", "path"]])
    out = [frontier]
    for _ in range(len(parts)):                                  # depth cap: a path cannot be longer than the table
        if frontier.empty:
            break
        nxt = frontier.merge(parts, left_on="part", right_on="part_id")
        ok = pd.Series([(">" + d + ">") not in (">" + p + ">") for d, p in zip(nxt["sub_part_id"], nxt["path"])], index=nxt.index, dtype=bool)
        nxt = nxt[ok]                                            # visited check (an explicit bool Series: an empty list would select no columns)
        frontier = pd.DataFrame({"part": nxt["sub_part_id"], "mult": nxt["mult"] * nxt["qty"], "path": nxt["path"] + ">" + nxt["sub_part_id"]})
        out.append(frontier)
    return pd.concat(out, ignore_index=True)
pd_paths = explode(parts, "BIKE").sort_values("path").reset_index(drop=True)
raw = pd_paths[~pd_paths["part"].isin(parts["part_id"])]
pd_df = (raw.groupby("part", as_index=False).agg(total_qty=("mult", "sum"), paths=("mult", "size")))
```

**Example:** one bike, by hand.
- Direct: FRAME 1, FRONT_ASSY 1, REAR_ASSY 1, SEAT 1.
- Through FRONT_ASSY: WHEEL 1, FORK 1, BRAKE 1. Through REAR_ASSY: WHEEL 1, CHAIN 1, BRAKE 1.
- Through each WHEEL row: SPOKE 1 x 36 = 36, RIM 1, TYRE 1. Two WHEEL rows, so these appear twice: 2 rows each for SPOKE, RIM and TYRE (16 path rows in all, as the output shows).
- Totals: SPOKE 36 + 36 = 72, RIM 2, TYRE 2, BRAKE 2 (one per assembly), FORK 1, CHAIN 1, FRAME 1, SEAT 1.
- This is a DAG, not a tree: WHEEL (and BRAKE) have two parents, so they can be reached by more than one path. A tree would have exactly one path to every node, and a plain `GROUP BY` of the last level would have been enough.
- With `UNION`: the rows `(WHEEL, 1)` from the front and from the rear are identical, so the second is discarded, and so are the rows below it. The run printed SPOKE 36 (should be 72), RIM 1, TYRE 1 and BRAKE 1. No error, wrong numbers. The pandas `drop_duplicates` on `(part, mult)` makes the same mistake.

**Code:** run with `python3 -I`. The asserts compare the path rows (ordered by path) and the totals (ordered by part) between SQL and pandas, and check the hand-computed totals.
```python
# Q10: bill of materials explosion with quantity multiplication (a DAG, not a tree)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE parts(part_id TEXT, sub_part_id TEXT, qty INTEGER);
INSERT INTO parts VALUES
 ('BIKE','FRAME',1), ('BIKE','FRONT_ASSY',1), ('BIKE','REAR_ASSY',1), ('BIKE','SEAT',1),
 ('FRONT_ASSY','WHEEL',1), ('FRONT_ASSY','FORK',1), ('FRONT_ASSY','BRAKE',1),
 ('REAR_ASSY','WHEEL',1),  ('REAR_ASSY','CHAIN',1), ('REAR_ASSY','BRAKE',1),
 ('WHEEL','SPOKE',36), ('WHEEL','RIM',1), ('WHEEL','TYRE',1);
"""
SQL_PATHS = """
WITH RECURSIVE bom(part, mult, path) AS (
  SELECT sub_part_id, qty, :product || '>' || sub_part_id FROM parts WHERE part_id = :product
  UNION ALL
  SELECT p.sub_part_id, b.mult * p.qty, b.path || '>' || p.sub_part_id
  FROM parts p JOIN bom b ON p.part_id = b.part
  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0     -- cycle guard: no part inside itself
)
SELECT part, mult, path FROM bom ORDER BY path
"""
SQL_MAIN = """
WITH RECURSIVE bom(part, mult, path) AS (
  SELECT sub_part_id, qty, :product || '>' || sub_part_id FROM parts WHERE part_id = :product
  UNION ALL
  SELECT p.sub_part_id, b.mult * p.qty, b.path || '>' || p.sub_part_id
  FROM parts p JOIN bom b ON p.part_id = b.part
  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0
)
SELECT part, SUM(mult) AS total_qty, COUNT(*) AS paths
FROM bom
WHERE NOT EXISTS (SELECT 1 FROM parts x WHERE x.part_id = bom.part)      -- raw component: never used as a parent
GROUP BY part
ORDER BY part
"""
SQL_UNION_BAD = """
WITH RECURSIVE bom(part, mult) AS (
  SELECT sub_part_id, qty FROM parts WHERE part_id = :product
  UNION                                                                  -- collapses equal (part, mult) rows from different paths
  SELECT p.sub_part_id, b.mult * p.qty FROM parts p JOIN bom b ON p.part_id = b.part
)
SELECT part, SUM(mult) AS total_qty FROM bom
WHERE NOT EXISTS (SELECT 1 FROM parts x WHERE x.part_id = bom.part)
GROUP BY part ORDER BY part
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"product": "BIKE"}
paths = pd.read_sql_query(SQL_PATHS, con, params=P)
print(paths.to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))
bad = pd.read_sql_query(SQL_UNION_BAD, con, params=P)
print("UNION version (wrong):", dict(zip(bad.part, bad.total_qty)))

parts = pd.read_sql_query("SELECT * FROM parts", con)
# pd:main
def explode(parts, product):
    frontier = (parts[parts["part_id"] == product]
                .assign(path=lambda d: product + ">" + d["sub_part_id"])
                .rename(columns={"sub_part_id": "part", "qty": "mult"})[["part", "mult", "path"]])
    out = [frontier]
    for _ in range(len(parts)):                                  # depth cap: a path cannot be longer than the table
        if frontier.empty:
            break
        nxt = frontier.merge(parts, left_on="part", right_on="part_id")
        ok = pd.Series([(">" + d + ">") not in (">" + p + ">") for d, p in zip(nxt["sub_part_id"], nxt["path"])], index=nxt.index, dtype=bool)
        nxt = nxt[ok]                                            # visited check (an explicit bool Series: an empty list would select no columns)
        frontier = pd.DataFrame({"part": nxt["sub_part_id"], "mult": nxt["mult"] * nxt["qty"], "path": nxt["path"] + ">" + nxt["sub_part_id"]})
        out.append(frontier)
    return pd.concat(out, ignore_index=True)
pd_paths = explode(parts, "BIKE").sort_values("path").reset_index(drop=True)
raw = pd_paths[~pd_paths["part"].isin(parts["part_id"])]
pd_df = (raw.groupby("part", as_index=False).agg(total_qty=("mult", "sum"), paths=("mult", "size")))
# pd:end
pd.testing.assert_frame_equal(pd_paths, paths, check_dtype=False)            # ordered by path
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)              # ordered by part
assert dict(zip(sql_df.part, sql_df.total_qty)) == {"BRAKE": 2, "CHAIN": 1, "FORK": 1, "FRAME": 1, "RIM": 2, "SEAT": 1, "SPOKE": 72, "TYRE": 2}
print("pandas equals SQL (paths ordered by path, totals by part)")
print("pandas drop_duplicates on (part, mult) as the UNION analogue:",
      pd_paths[["part", "mult"]].drop_duplicates().pipe(lambda d: d[~d.part.isin(parts.part_id)]).groupby("part")["mult"].sum().to_dict())

# Edge cases
print("unknown product:", con.execute(SQL_MAIN, {"product": "UNICYCLE"}).fetchall(), "| raw part as product:", con.execute(SQL_MAIN, {"product": "SEAT"}).fetchall())
print("sub-assembly WHEEL on its own:", con.execute(SQL_MAIN, {"product": "WHEEL"}).fetchall())
con.execute("INSERT INTO parts VALUES ('BIKE','SEAT',1)")
print("duplicate BIKE-SEAT row: SEAT total =", {r[0]: r[1] for r in con.execute(SQL_MAIN, P)}["SEAT"])
con.execute("DELETE FROM parts WHERE rowid = (SELECT max(rowid) FROM parts)")
con.execute("UPDATE parts SET qty = NULL WHERE part_id = 'REAR_ASSY' AND sub_part_id = 'CHAIN'")
print("NULL qty on REAR_ASSY-CHAIN: CHAIN total =", [r for r in con.execute(SQL_MAIN, P) if r[0] == "CHAIN"])
con.execute("UPDATE parts SET qty = 1 WHERE part_id = 'REAR_ASSY' AND sub_part_id = 'CHAIN'")
con.execute("INSERT INTO parts VALUES ('WHEEL','BIKE',1)")      # a data error: a wheel contains a bike
print("cyclic BOM with the path guard:", [(r[0], r[1]) for r in con.execute(SQL_MAIN, P)])
unguarded = SQL_PATHS.replace("  WHERE instr('>' || b.path || '>', '>' || p.sub_part_id || '>') = 0     -- cycle guard: no part inside itself\n", "").replace("ORDER BY path", "LIMIT 40")
print("cyclic BOM, no guard, LIMIT 40: rows =", len(con.execute(unguarded, P).fetchall()), "| longest path:", max(len(r[2]) for r in con.execute(unguarded, P)), "characters")
print("asserts passed")
```

**Output (my run):**
```text
      part  mult                        path
     FRAME     1                  BIKE>FRAME
FRONT_ASSY     1             BIKE>FRONT_ASSY
     BRAKE     1       BIKE>FRONT_ASSY>BRAKE
      FORK     1        BIKE>FRONT_ASSY>FORK
     WHEEL     1       BIKE>FRONT_ASSY>WHEEL
       RIM     1   BIKE>FRONT_ASSY>WHEEL>RIM
     SPOKE    36 BIKE>FRONT_ASSY>WHEEL>SPOKE
      TYRE     1  BIKE>FRONT_ASSY>WHEEL>TYRE
 REAR_ASSY     1              BIKE>REAR_ASSY
     BRAKE     1        BIKE>REAR_ASSY>BRAKE
     CHAIN     1        BIKE>REAR_ASSY>CHAIN
     WHEEL     1        BIKE>REAR_ASSY>WHEEL
       RIM     1    BIKE>REAR_ASSY>WHEEL>RIM
     SPOKE    36  BIKE>REAR_ASSY>WHEEL>SPOKE
      TYRE     1   BIKE>REAR_ASSY>WHEEL>TYRE
      SEAT     1                   BIKE>SEAT
 part  total_qty  paths
BRAKE          2      2
CHAIN          1      1
 FORK          1      1
FRAME          1      1
  RIM          2      2
 SEAT          1      1
SPOKE         72      2
 TYRE          2      2
UNION version (wrong): {'BRAKE': 1, 'CHAIN': 1, 'FORK': 1, 'FRAME': 1, 'RIM': 1, 'SEAT': 1, 'SPOKE': 36, 'TYRE': 1}
pandas equals SQL (paths ordered by path, totals by part)
pandas drop_duplicates on (part, mult) as the UNION analogue: {'BRAKE': 1, 'CHAIN': 1, 'FORK': 1, 'FRAME': 1, 'RIM': 1, 'SEAT': 1, 'SPOKE': 36, 'TYRE': 1}
unknown product: [] | raw part as product: []
sub-assembly WHEEL on its own: [('RIM', 1, 1), ('SPOKE', 36, 1), ('TYRE', 1, 1)]
duplicate BIKE-SEAT row: SEAT total = 2
NULL qty on REAR_ASSY-CHAIN: CHAIN total = [('CHAIN', None, 1)]
cyclic BOM with the path guard: [('BRAKE', 2), ('CHAIN', 1), ('FORK', 1), ('FRAME', 1), ('RIM', 2), ('SEAT', 1), ('SPOKE', 72), ('TYRE', 2)]
cyclic BOM, no guard, LIMIT 40: rows = 40 | longest path: 48 characters
asserts passed
```

**Edge cases:**
- Unknown product (`UNICYCLE`) gives no rows. A raw part used as the product (`SEAT`) also gives no rows: nothing is below it. Say which you expect.
- A sub-assembly on its own works as a product: `WHEEL` returns SPOKE 36, RIM 1, TYRE 1.
- Duplicate row (`BIKE`, `SEAT`, 1) twice: SEAT total 2. Whether a repeated row means "2 seats" or "a loading error" is a business question; check for it with `GROUP BY part_id, sub_part_id HAVING COUNT(*) > 1`.
- NULL quantity (REAR_ASSY to CHAIN set to NULL): CHAIN total came back `None`. If the NULL is mixed with real quantities for the same component, `SUM` would ignore it and under-report silently; validate quantities (`qty > 0`) before exploding.
- Cycle (I added WHEEL contains BIKE): with the path guard the totals are unchanged; without it the run produced paths without end (stopped by `LIMIT 40`, the longest path already 48 characters).
- A product with no components is a raw part; a component that is both raw in one place and an assembly in another is impossible by the definition used here (a part is raw only if it never appears as a `part_id`).

**Then explain:**
- Multiply along, add across. The recursion multiplies; the final aggregate adds.
- The number of path rows grows with the number of paths, not with the number of parts. A part used in many sub-assemblies makes many path rows; to avoid that, aggregate level by level in a loop outside SQL, or by a topological order (Q22).
- `UNION` collapses on whole-row equality, which here is `(part, mult)`, not the path. That is a silent error. Including the path in the row would stop the collapsing, but then `UNION` is just a slower `UNION ALL`.
- Other engines (not executed): SQL Server writes `WITH bom(...) AS (...)` without `RECURSIVE` and caps at `MAXRECURSION 100` by default, so a deep BOM needs `OPTION (MAXRECURSION n)`; MySQL needs `RECURSIVE` and checks `cte_max_recursion_depth`; Oracle has `CONNECT BY` with `PRIOR`, and the multiplication along the path is awkward there (from memory).

**Follow-ups:**
- How would you cost the bike? Join the totals to a `component_cost` table and multiply: `SUM(total_qty * unit_cost)`.
- How would you find where a raw part is used (where-used)? Reverse the join direction, like the upward walk in Q5.
- Which components are shared by two assemblies? Those with `paths > 1` in the main query (`BRAKE`, `RIM`, `SPOKE`, `TYRE` here).

**Common mistakes:**
- `UNION` instead of `UNION ALL`, losing shared components.
- Summing quantities without multiplying along the path (SPOKE would be 2, one per path, not 72).
- Treating the BOM as a tree and using `DISTINCT`.
- `NOT IN` for the raw test on a nullable column.
- No cycle guard on data that can be edited by hand.

### Q11 ⭐⭐⭐ 🔴 Degrees of separation and friends of friends: friendships(user_a, user_b) stores each friendship once (a < b), so the graph is undirected. For user 1 return every user within 3 hops with the shortest distance, the friends-of-friends list (distance exactly 2, excluding existing friends and the user), and the count of mutual friends for each suggestion. Show how the edge list is made symmetric with UNION ALL, why a distance guard or visited check is required (friend loops are cycles), and why MIN(distance) over all paths is the shortest path in an unweighted graph.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Make the edge list symmetric with `UNION ALL`, walk outwards from user 1 with a recursive CTE that carries a distance and stops at 3, take `MIN(dist)` per user (in an unweighted graph the first level at which a user appears is the shortest path), then friends of friends are the users at distance exactly 2 and the mutual-friend count is the number of their friends who are also friends of user 1.

**Schema and sample data:** eleven friendship rows, each stored once with `user_a < user_b`. Users 1 to 8 are connected; users 11 and 12 are a separate pair (never reachable from user 1). User 1's friends are 2 and 3, who are also friends with each other (a triangle, so friend loops exist).
```sql
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER, PRIMARY KEY (user_a, user_b), CHECK (user_a < user_b));
INSERT INTO friendships VALUES
 (1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,6),(5,6),(6,7),(7,8),(11,12);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE e(src, dst) AS (
  SELECT user_a, user_b FROM friendships
  UNION ALL
  SELECT user_b, user_a FROM friendships
), walk(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.dst, w.dist + 1 FROM walk w JOIN e ON e.src = w.node WHERE w.dist < 3
), best AS (
  SELECT node AS user_id, MIN(dist) AS dist FROM walk WHERE node <> 1 GROUP BY node
), fof AS (
  SELECT f.user_id, COUNT(DISTINCT x.dst) AS mutual_friends
  FROM best f
  JOIN e x ON x.src = f.user_id
  JOIN e me ON me.src = 1 AND me.dst = x.dst
  WHERE f.dist = 2
  GROUP BY f.user_id
)
SELECT b.user_id, b.dist, COALESCE(f.mutual_friends, 0) AS mutual_friends
FROM best b LEFT JOIN fof f ON f.user_id = b.user_id
ORDER BY b.dist, b.user_id
```
How it works:
- `e` is the symmetric edge list: each stored pair is emitted once as (a, b) and once as (b, a), so one join `e.src = w.node` follows a friendship in either direction. `UNION ALL` is fine here because the two halves cannot overlap (a < b means (a, b) never equals (b, a)).
- `walk` is the recursion. Its row is only (node, dist). I use plain `UNION`, not `UNION ALL`, so a row already produced is discarded; and `WHERE w.dist < 3` is a depth cap. The pair (node, dist) can only take (number of users x 4) values, so the recursion has to end.
- `best` is `MIN(dist)` per user. `walk` contains a user once for each distance at which some walk reaches them (user 2 is reached at distance 1, and also at distance 2 and 3 by walking back and forth), so the minimum picks the shortest.
- `fof` takes the users at distance exactly 2 (which by construction are not friends and not user 1, because those appear at distance 1 or 0 and `MIN` is smaller) and counts the distinct neighbours of that user who are also neighbours of user 1.
- A second version, `SQL_PATH` in the Code block, tracks a path string `',1,2,'` and refuses a step when the next user is already in it. That enumerates every simple path, which is exact but exponential in a dense graph, and it also gives a free `COUNT(*)` of routes; I print it to show it agrees on the distances.

**pandas answer:** a frontier loop, one merge per hop (shown once, identical to the Code block):
```py
    edges = pd.concat([friend.rename(columns={"user_a": "src", "user_b": "dst"}),
                       friend.rename(columns={"user_b": "src", "user_a": "dst"})]).drop_duplicates()
    seen = {start: 0}
    frontier = pd.DataFrame({"node": [start]})
    for d in range(1, max_hops + 1):
        nxt = frontier.merge(edges, left_on="node", right_on="src")["dst"].drop_duplicates()
        nxt = nxt[~nxt.isin(list(seen))]
        if nxt.empty:
            break
        seen.update({n: d for n in nxt})
        frontier = pd.DataFrame({"node": nxt.to_numpy()})
    best = pd.DataFrame({"user_id": [n for n in seen if n != start], "dist": [d for n, d in seen.items() if n != start]})
    mine = set(edges.loc[edges["src"] == start, "dst"])
    nbrs = edges.groupby("src")["dst"].agg(set)
    best["mutual_friends"] = [len(nbrs[u] & mine) if d == 2 else 0 for u, d in zip(best["user_id"], best["dist"])]
    return best.sort_values(["dist", "user_id"]).reset_index(drop=True)
```

**Example:** by hand on the sample data.
- Level 0 is user 1. Friends of 1 are 2 and 3, so distance 1 is {2, 3}.
- Neighbours of 2 are 1, 3, 4; neighbours of 3 are 1, 2, 4, 5. New users are 4 and 5, so distance 2 is {4, 5}.
- Neighbours of 4 are 2, 3, 6; of 5 are 3, 6. New user is 6, distance 3. A fourth hop would add 7, which the cap of 3 excludes.
- Mutual friends: user 4 knows 2 and 3, both friends of 1, so 2. User 5 knows 3 (and 6, who is not a friend of 1), so 1.
- Final answer: 2 and 3 at distance 1; 4 (2 mutual) and 5 (1 mutual) at distance 2; 6 at distance 3. Users 7, 8, 11 and 12 are outside 3 hops.

**Code:** run with `python3 -I`. The asserts compare SQL and pandas after sorting by `dist, user_id`, compare the path-guard distances to the `UNION` version, and check that duplicate edge rows do not change the result.
```python
# Q11: degrees of separation and friends of friends on an undirected friendship graph
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER, PRIMARY KEY (user_a, user_b), CHECK (user_a < user_b));
INSERT INTO friendships VALUES
 (1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,6),(5,6),(6,7),(7,8),(11,12);
"""
SQL_MAIN = """
WITH RECURSIVE e(src, dst) AS (
  SELECT user_a, user_b FROM friendships
  UNION ALL
  SELECT user_b, user_a FROM friendships
), walk(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.dst, w.dist + 1 FROM walk w JOIN e ON e.src = w.node WHERE w.dist < 3
), best AS (
  SELECT node AS user_id, MIN(dist) AS dist FROM walk WHERE node <> 1 GROUP BY node
), fof AS (
  SELECT f.user_id, COUNT(DISTINCT x.dst) AS mutual_friends
  FROM best f
  JOIN e x ON x.src = f.user_id
  JOIN e me ON me.src = 1 AND me.dst = x.dst
  WHERE f.dist = 2
  GROUP BY f.user_id
)
SELECT b.user_id, b.dist, COALESCE(f.mutual_friends, 0) AS mutual_friends
FROM best b LEFT JOIN fof f ON f.user_id = b.user_id
ORDER BY b.dist, b.user_id
"""
# the same walk with a visited-path guard (enumerates every simple path, so it is the expensive version)
SQL_PATH = """
WITH RECURSIVE e(src, dst) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), walk(node, dist, path) AS (
  SELECT 1, 0, ',1,'
  UNION ALL
  SELECT e.dst, w.dist + 1, w.path || e.dst || ','
  FROM walk w JOIN e ON e.src = w.node
  WHERE w.dist < 3 AND w.path NOT LIKE '%,' || e.dst || ',%'
)
SELECT node AS user_id, MIN(dist) AS dist, COUNT(*) AS simple_paths
FROM walk WHERE node <> 1 GROUP BY node ORDER BY dist, node
"""
# the unguarded version: no distance cap, UNION ALL; bounded here only by LIMIT so the demo terminates
SQL_NOGUARD = """
WITH RECURSIVE e(src, dst) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), walk(node, dist) AS (
  SELECT 1, 0
  UNION ALL
  SELECT e.dst, w.dist + 1 FROM walk w JOIN e ON e.src = w.node
  LIMIT 1000
)
SELECT COUNT(*) AS rows_before_limit_stops_it, MAX(dist) AS deepest_level FROM walk
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (user 1, within 3 hops, mutual friends for distance 2):")
print(sql_df.to_string(index=False))
print("path-guard version (simple_paths = distinct routes found):")
print(pd.read_sql_query(SQL_PATH, con).to_string(index=False))
print("no guard, UNION ALL, stopped by LIMIT 1000:", con.execute(SQL_NOGUARD).fetchone())

friend = pd.read_sql_query("SELECT * FROM friendships", con)

def separation(friend, start, max_hops=3):
    # pd:main
    edges = pd.concat([friend.rename(columns={"user_a": "src", "user_b": "dst"}),
                       friend.rename(columns={"user_b": "src", "user_a": "dst"})]).drop_duplicates()
    seen = {start: 0}
    frontier = pd.DataFrame({"node": [start]})
    for d in range(1, max_hops + 1):
        nxt = frontier.merge(edges, left_on="node", right_on="src")["dst"].drop_duplicates()
        nxt = nxt[~nxt.isin(list(seen))]
        if nxt.empty:
            break
        seen.update({n: d for n in nxt})
        frontier = pd.DataFrame({"node": nxt.to_numpy()})
    best = pd.DataFrame({"user_id": [n for n in seen if n != start], "dist": [d for n, d in seen.items() if n != start]})
    mine = set(edges.loc[edges["src"] == start, "dst"])
    nbrs = edges.groupby("src")["dst"].agg(set)
    best["mutual_friends"] = [len(nbrs[u] & mine) if d == 2 else 0 for u, d in zip(best["user_id"], best["dist"])]
    return best.sort_values(["dist", "user_id"]).reset_index(drop=True)
    # pd:end

pd_df = separation(friend, 1)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after ORDER BY dist, user_id
print("pandas result equal to SQL")
# the path-guard version and the UNION version agree on the distances
pg = pd.read_sql_query(SQL_PATH, con)
assert pg[["user_id", "dist"]].equals(sql_df[["user_id", "dist"]])

# edge cases: duplicate friendship row (loaded without the primary key), a user with no friends, an unreachable component
con.executescript("CREATE TABLE f2(user_a INTEGER, user_b INTEGER); INSERT INTO f2 SELECT * FROM friendships; INSERT INTO f2 VALUES (1,2),(3,5);")
dup = pd.read_sql_query(SQL_MAIN.replace("friendships", "f2"), con)
assert dup.equals(sql_df), "COUNT(DISTINCT) keeps mutual counts right under duplicate edges"
print("duplicate edge rows (1,2) and (3,5): result unchanged =", dup.equals(sql_df))
naive = SQL_MAIN.replace("COUNT(DISTINCT x.dst)", "COUNT(x.dst)").replace("friendships", "f2")
print("same query with COUNT(x.dst) on the duplicated table:")
print(pd.read_sql_query(naive, con).query("dist == 2").to_string(index=False))
print("user 99 (no friends):", con.execute(SQL_MAIN.replace("SELECT 1, 0", "SELECT 99, 0").replace("<> 1", "<> 99").replace("me.src = 1", "me.src = 99")).fetchall())
allu = set(friend["user_a"]) | set(friend["user_b"])
print("users in the table but not within 3 hops of user 1:", sorted(allu - set(sql_df["user_id"]) - {1}), "(7 and 8 are 4 and 5 hops away, 11 and 12 are a separate component)")
print("pandas for user 99:", len(separation(friend, 99)), "rows")
print("asserts passed")
```

**Output (my run):**
```text
SQL (user 1, within 3 hops, mutual friends for distance 2):
 user_id  dist  mutual_friends
       2     1               0
       3     1               0
       4     2               2
       5     2               1
       6     3               0
path-guard version (simple_paths = distinct routes found):
 user_id  dist  simple_paths
       2     1             3
       3     1             3
       4     2             4
       5     2             2
       6     3             3
no guard, UNION ALL, stopped by LIMIT 1000: (1000, 7)
pandas result equal to SQL
duplicate edge rows (1,2) and (3,5): result unchanged = True
same query with COUNT(x.dst) on the duplicated table:
 user_id  dist  mutual_friends
       4     2               3
       5     2               2
user 99 (no friends): []
users in the table but not within 3 hops of user 1: [7, 8, 11, 12] (7 and 8 are 4 and 5 hops away, 11 and 12 are a separate component)
pandas for user 99: 0 rows
asserts passed
```
Honest notes from the run: the path-guard version shows user 4 reachable by 4 simple paths (1-2-4, 1-3-4, 1-2-3-4, 1-3-2-4), which is why path enumeration blows up on dense friend graphs while the (node, dist) version stays small. Without any guard the recursion produced 1000 rows and reached level 7 before the `LIMIT 1000` inside the recursive select stopped it; without the `LIMIT` it would run until memory or time ran out (the walk bounces between friends forever).

**Edge cases:**
- Cycles: any friendship is a 2-cycle (1 to 2 to 1) and the triangle 1-2-3 is a 3-cycle, so without a guard the walk never ends (demonstrated above, bounded by `LIMIT`). The guard here is the distance cap plus `UNION` on (node, dist); the path-string guard is the alternative.
- Duplicate friendship rows (loaded without the primary key): distances are unchanged, but a plain `COUNT(x.dst)` over-counts mutual friends (user 4 showed 3 instead of 2). `COUNT(DISTINCT x.dst)` is the fix; or deduplicate the edge list first.
- User with no friends (user 99) or an unknown user: the anchor row exists but nothing joins, and `best` excludes the start user, so the result is empty (the pandas version returns 0 rows too).
- A user within 3 hops but at distance 1 is never a suggestion, because suggestions need `dist = 2` from `MIN`; a friend who is also at distance 2 by another route is still distance 1.
- Mutual count is 0 for everyone not at distance 2 by design (the column is only meaningful for suggestions).
- Unreachable users (11, 12) simply never appear.

**Then explain:**
- Symmetric edges: storing each friendship once halves storage but the walk must be able to go both ways; `UNION ALL` of the table with its reversed copy is the standard trick. In SQLite the CTE `e` is a plain (non-recursive) CTE, so referencing it in the recursive member is allowed; the recursive CTE `walk` itself is referenced only once.
- Why the guard is required: undirected friendship is a cycle for every edge. A recursive CTE stops only when the recursive member returns no rows, and here it always can walk back.
- Why `MIN(dist)` is the shortest path: every edge costs 1 and `dist` counts the edges walked, so every row for a user is the length of some real walk to them, and the shortest walk is among the rows because the cap of 3 allows it. The minimum over all rows is therefore the shortest distance, whatever order the engine processes the queue in (SQLite does not guarantee a row order without `ORDER BY`). With weighted edges this reasoning fails (see Q23 in this part).
- Cost: the (node, dist) version is at most nodes x max_dist rows; the path version is the number of simple paths, which can be exponential.
- Other engines (not executed here): PostgreSQL 14+ has `CYCLE node SET is_cycle USING path`, MySQL 8 needs `WITH RECURSIVE` and caps recursion at `cte_max_recursion_depth` (default 1000), SQL Server omits the word `RECURSIVE` and stops at `MAXRECURSION` (default 100), and Oracle would use `CONNECT BY NOCYCLE`. Graph databases do this natively, but the interview answer is the SQL one.

**Follow-ups:**
- "People you may know ranked by mutual friends?" Order the `fof` rows by `mutual_friends DESC` and cap with `LIMIT`; ties need a deterministic second key such as `user_id`.
- "What about a million users?" The recursive CTE materialises each level; at scale use an adjacency table with an index on `src`, a depth of 2 only, or precompute friends-of-friends in a batch job (graph or Spark tools are out of scope here).
- "Directed follows instead of friends?" Drop the `UNION ALL` reversal; mutual then means follows in both directions.

**Common mistakes:**
- Forgetting the symmetric edge list and finding only friends with a larger id (a < b storage).
- No guard: the query never ends, or hits an engine recursion limit.
- Using `UNION` with a path or a distance column that makes every row unique and believing it still dedups (it does not remove cycles then; here `(node, dist)` is bounded only because the distance cap exists).
- Counting mutual friends with `COUNT(*)` on data that has duplicate edge rows.
- Taking friends of friends as "distance 2 or less" and so suggesting existing friends, or forgetting to exclude the user themself.

### Q12 ⭐⭐⭐ 🔴 Cumulative sum that resets once it passes a threshold: txns(acct_id, txn_id, amount) ordered by txn_id. Keep a running total and, when it reaches or exceeds 100, emit a flag and restart from 0 on the next row (so the total depends on where earlier resets happened). Show why a window function cannot do it (the group key depends on the output of the previous row), solve with a recursive CTE that carries (acct_id, rn, running, reset_flag) and joins to the next row number, and compare with the easy variant that resets on a stored flag (Part 7 Q24, solved there with a running SUM of is_reset as group key). Give the pandas loop version with an assert and say that a recursive CTE here is a row-by-row loop in disguise.
**Asked at:** threshold-reset running total threads (search snippets only, not opened: SQLServerCentral 'reset running total', Microsoft Q&A 'Reset sum() OVER PARTITION BY for condition' saying there is no set-based form and a recursive CTE is the workaround, a recursive running total that 'forgets' after two rows); forum posts, not candidate reports; the deferred problem from Part 7 Q24; data engineer and analyst rounds
**Say this first (1 line):** A window function cannot do it, because whether row n starts a new group depends on the running total of row n-1, which is itself the output; so I carry the state (running total and reset flag) in a recursive CTE that walks the rows in order, and I say plainly that it is a row-by-row loop written in SQL.

**Schema and sample data:** four accounts. A has 8 rows with overshoots (120, 110, 110), B has two exact hits of 100 in a row and an exact hit again at the end, C has a single row above the limit, D has a NULL amount. Reset rule used: the flag is set when the running total is `>= 100`, and the next row restarts from 0 (so the next row's amount is the new running total).
```sql
CREATE TABLE txns(acct_id TEXT, txn_id INTEGER, amount INTEGER);
INSERT INTO txns VALUES
 ('A',1,40),('A',2,30),('A',3,50),('A',4,20),('A',5,90),('A',6,10),('A',7,100),('A',8,5),
 ('B',1,100),('B',2,100),('B',3,60),('B',4,30),('B',5,10),
 ('C',1,150),
 ('D',1,50),('D',2,NULL),('D',3,60);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, txn_id, amount, running, reset_flag) AS (
  SELECT acct_id, rn, txn_id, amount, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END
  FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn, t.txn_id, t.amount,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
)
SELECT acct_id, txn_id, amount, running, reset_flag
FROM r
ORDER BY acct_id, rn
```
How it works:
- `t` numbers each account's rows with `ROW_NUMBER()`, so gaps in `txn_id` do not matter, and replaces a NULL amount by 0 (otherwise `running + NULL` is NULL and every later row stays NULL).
- The anchor is row 1 of every account: running total is its amount, flag is whether that alone reaches 100.
- The recursive member joins the previous output row `r` to the next row `t.rn = r.rn + 1` of the same account. If the previous flag was 1 the total restarts at this row's amount, otherwise it adds. The flag is computed from the same expression (the CASE is repeated because a column alias cannot be used in the same SELECT).
- The recursion ends by itself when there is no row `rn + 1`. No cycle is possible (`rn` only increases), so no cycle guard is needed here; the guard question is only the depth limit of the engine.

**pandas answer:** a plain loop per account (shown once, identical to the Code block):
```py
    t = txns.assign(amount=txns["amount"].fillna(0).astype(int)).sort_values(["acct_id", "txn_id"])
    rows = []
    for acct, g in t.groupby("acct_id", sort=True):
        running, flag = 0, 0
        for txn_id, amount in zip(g["txn_id"], g["amount"]):
            running = amount if flag == 1 else running + amount
            flag = 1 if running >= limit else 0
            rows.append((acct, txn_id, amount, running, flag))
    return pd.DataFrame(rows, columns=["acct_id", "txn_id", "amount", "running", "reset_flag"])
```

**Example:** account A, amounts 40, 30, 50, 20, 90, 10, 100, 5.
- 40 (total 40), 30 (70), 50 (120, reached 100, flag 1).
- The next row restarts: 20 (total 20), 90 (110, flag 1). Restart: 10 (10), 100 (110, flag 1). Restart: 5 (5).
- Totals: 40, 70, 120, 20, 110, 10, 110, 5; flags on rows 3, 5, 7.
- Account B: 100 (flag), restart 100 (flag), restart 60, 90, 100 (flag). Account C: 150 (flag). Account D: 50, then the NULL counts as 0 (50), then 110 (flag).
- Why a window cannot do it: after the first reset at 120 the second group starts at row 4, but you only know that row 4 starts a group by having computed row 3's total. Cutting the plain running total into buckets of 100 puts the resets in the wrong rows (the 20 left over from 120 is not carried; the code prints the rows where the buckets give a wrong running total).

**Code:** run with `python3 -I`. Asserts: pandas loop equals the recursive CTE (both sorted by `acct_id, txn_id`), and a window function equals it when the flags are supplied from the recursion.
```python
# Q12: running total that resets after it reaches a threshold (100): recursive CTE versus pandas loop
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE txns(acct_id TEXT, txn_id INTEGER, amount INTEGER);
INSERT INTO txns VALUES
 ('A',1,40),('A',2,30),('A',3,50),('A',4,20),('A',5,90),('A',6,10),('A',7,100),('A',8,5),
 ('B',1,100),('B',2,100),('B',3,60),('B',4,30),('B',5,10),
 ('C',1,150),
 ('D',1,50),('D',2,NULL),('D',3,60);
"""
SQL_MAIN = """
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, txn_id, amount, running, reset_flag) AS (
  SELECT acct_id, rn, txn_id, amount, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END
  FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn, t.txn_id, t.amount,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
)
SELECT acct_id, txn_id, amount, running, reset_flag
FROM r
ORDER BY acct_id, rn
"""
# a window function once the flags are known: the group key is the number of resets strictly before the row
SQL_WINDOW_GIVEN_FLAGS = """
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, running, reset_flag) AS (
  SELECT acct_id, rn, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
), g AS (
  SELECT t.acct_id, t.rn, t.txn_id, t.amount, r.reset_flag,
         COALESCE(SUM(r.reset_flag) OVER (PARTITION BY t.acct_id ORDER BY t.rn
                  ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), 0) AS grp
  FROM t JOIN r ON r.acct_id = t.acct_id AND r.rn = t.rn
)
SELECT acct_id, txn_id, amount,
       SUM(amount) OVER (PARTITION BY acct_id, grp ORDER BY rn) AS running, reset_flag
FROM g ORDER BY acct_id, rn
"""
# the tempting window-only answer: cut the plain running total into buckets of 100
SQL_NAIVE = """
WITH c AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         SUM(COALESCE(amount, 0)) OVER (PARTITION BY acct_id ORDER BY txn_id) AS cum
  FROM txns
)
SELECT acct_id, txn_id, amount, cum, cum % 100 AS naive_running, CASE WHEN cum / 100 > LAG(cum / 100, 1, 0) OVER (PARTITION BY acct_id ORDER BY txn_id) THEN 1 ELSE 0 END AS naive_flag
FROM c ORDER BY acct_id, txn_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("recursive CTE result:")
print(sql_df.to_string(index=False))

txns = pd.read_sql_query("SELECT * FROM txns", con)

def reset_running(txns, limit=100):
    # pd:main
    t = txns.assign(amount=txns["amount"].fillna(0).astype(int)).sort_values(["acct_id", "txn_id"])
    rows = []
    for acct, g in t.groupby("acct_id", sort=True):
        running, flag = 0, 0
        for txn_id, amount in zip(g["txn_id"], g["amount"]):
            running = amount if flag == 1 else running + amount
            flag = 1 if running >= limit else 0
            rows.append((acct, txn_id, amount, running, flag))
    return pd.DataFrame(rows, columns=["acct_id", "txn_id", "amount", "running", "reset_flag"])
    # pd:end

pd_df = reset_running(txns)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by acct_id, txn_id
print("pandas loop equal to recursive CTE")

win = pd.read_sql_query(SQL_WINDOW_GIVEN_FLAGS, con)
pd.testing.assert_frame_equal(win, sql_df, check_dtype=False)
print("window function with the flags supplied: equal (the flags still came from the recursion)")

naive = pd.read_sql_query(SQL_NAIVE, con)
m = naive.merge(sql_df[["acct_id", "txn_id", "running", "reset_flag"]], on=["acct_id", "txn_id"])
print("window-only buckets of 100, rows that disagree with the true result:")
print(m[(m.naive_running != m.running) | (m.naive_flag != m.reset_flag)][["acct_id", "txn_id", "amount", "running", "naive_running", "reset_flag", "naive_flag"]].to_string(index=False))

# long account: SQLite has no default depth limit like MySQL (1000) or SQL Server (100)
con.execute("CREATE TABLE big(acct_id TEXT, txn_id INTEGER, amount INTEGER)")
con.executemany("INSERT INTO big VALUES ('Z', ?, ?)", [(i, 7) for i in range(1, 5001)])
n = con.execute(SQL_MAIN.replace("FROM txns", "FROM big").replace("ORDER BY acct_id, rn", "ORDER BY acct_id, rn DESC LIMIT 1")).fetchone()
print("5000-row single account, last row:", n, "(5000 recursion levels ran in SQLite)")
bigdf = pd.read_sql_query("SELECT * FROM big", con)
assert reset_running(bigdf).iloc[-1].tolist() == list(n)
print("empty table:", con.execute(SQL_MAIN.replace("FROM txns", "FROM txns WHERE 1 = 0")).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
recursive CTE result:
acct_id  txn_id  amount  running  reset_flag
      A       1      40       40           0
      A       2      30       70           0
      A       3      50      120           1
      A       4      20       20           0
      A       5      90      110           1
      A       6      10       10           0
      A       7     100      110           1
      A       8       5        5           0
      B       1     100      100           1
      B       2     100      100           1
      B       3      60       60           0
      B       4      30       90           0
      B       5      10      100           1
      C       1     150      150           1
      D       1      50       50           0
      D       2       0       50           0
      D       3      60      110           1
pandas loop equal to recursive CTE
window function with the flags supplied: equal (the flags still came from the recursion)
window-only buckets of 100, rows that disagree with the true result:
acct_id  txn_id  amount  running  naive_running  reset_flag  naive_flag
      A       3      50      120             20           1           1
      A       4      20       20             40           0           0
      A       5      90      110             30           1           1
      A       6      10       10             40           0           0
      A       7     100      110             40           1           1
      A       8       5        5             45           0           0
      B       1     100      100              0           1           1
      B       2     100      100              0           1           1
      B       5      10      100              0           1           1
      C       1     150      150             50           1           1
      D       3      60      110             10           1           1
5000-row single account, last row: ('Z', 5000, 7, 35, 0) (5000 recursion levels ran in SQLite)
empty table: []
asserts passed
```
Honest notes from the run:
- A window query becomes possible once the flags exist: the group key is the count of resets strictly before the row (`SUM(flag)` over `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`), then `SUM(amount) OVER (PARTITION BY acct_id, grp)`. In the Code block the flags still come from the recursion, so this is only a presentation trick; it proves the loop is where the real work happens.
- The window-only bucket attempt gets the reset rows' flags right in this data by luck but the running total wrong on 11 rows: the overshoot is not carried and the exact-100 rows show 0.
- A 5000-row single account ran fine in SQLite (I did not look for its limit). Other engines cap recursion by default (SQL Server `MAXRECURSION` 100, MySQL `cte_max_recursion_depth` 1000; both not executed here), so a long account would need `OPTION (MAXRECURSION 0)` or a raised setting, or a loop outside SQL.

**Edge cases:**
- NULL amount: replaced with 0 here (a business choice; ignoring the row entirely would need to skip it in the numbering). Without `COALESCE` the total turns NULL and stays NULL for the rest of the account.
- Reaching exactly 100 resets (`>=`), as asked; use `>` if the rule is "exceeds".
- Overshoot (120) is not carried to the next row; the restart is from 0 as the question states. If the business rule is to carry the excess, the recursive member changes to `running - 100`.
- Ties or duplicate `txn_id` in an account: `ROW_NUMBER` needs a tie-break column, otherwise the order is arbitrary.
- Account with a single row (C) is just the anchor. Empty table: no anchor rows, empty result (printed).
- Negative amounts: allowed; the total can drop and a flag happens only when it is at least 100.

**Then explain:**
- Why not a window: the group id of row n is a function of the whole history through the output, not of the input columns. `SUM() OVER` and `LAG()` only see input columns.
- Compare with the easy variant (Part 7 Q24, checked: "Cumulative sum that resets by condition"): there the reset flag is a stored column, so the group key is a running `SUM(is_reset)` and it is a plain window query. Here the flag depends on the running total, so it must be computed row by row.
- A recursive CTE here is a loop in disguise: each round turns the previous output row into the next, one row per account per round, so the depth is the longest account, not the number of accounts.
- SQLite allows the recursive member to join another table (`t`) once the CTE is referenced only once; it must not use aggregates or windows (windows were already applied in `t`).
- Other engines (not executed here): PostgreSQL and MySQL 8 accept the same query shape; SQL Server drops the `RECURSIVE` keyword; for very long histories a procedural loop, a cursor, or a pandas/Python job is usually the practical choice.

**Follow-ups:**
- "Can you do it without recursion?" Not as a single window; a self-join cannot either. Some engines offer `MODEL`/`MATCH_RECOGNIZE` (Oracle, others) or procedural code (not executed here).
- "Reset at 100 and carry the excess?" Use `running - 100` after a flag instead of the new amount.
- "How would you scale it?" Partition by account (the recursion already does), limit depth, or run it in pandas or a stored procedure.

**Common mistakes:**
- Trying `SUM() OVER` with `FLOOR(cum / 100)` as a group key (wrong as soon as the total overshoots).
- Forgetting `COALESCE` on a NULL amount.
- Joining on `txn_id + 1` when the ids have gaps (use a row number).
- Ending the recursion with an unbounded long account on an engine with a default recursion cap.
- Starting the next group with the old running total instead of the new amount.

### Q13 ⭐⭐ 🟢 Category tree and breadcrumbs: categories(category_id, parent_id, name) and products(product_id, category_id). Return for each category its breadcrumb ('Electronics > Phones > Android'), its depth, and the number of products in it including all descendant categories (a roll-up to every ancestor). Show the top-down recursion building the breadcrumb, the closure-pair recursion for the roll-up, why a product count by category_id alone misses the descendants, and how to list only leaf categories.
**Asked at:** employee-manager hierarchy guides: jdsatpathy Substack 'Find All Managers of an Employee Up to the CEO' (opened; anchor at the employee, join employee to manager, no cycle guard, UNION ALL), DataVidhya recursive hierarchy pattern page (opened; reports under a manager, ancestors of a category, paths in a dependency graph, depth tracking and cycle detection), and search snippets of datadriven.io and a Medium recursive CTE interview post (not opened); guides, not candidate reports; analyst and data engineer rounds at product companies, GCCs and consulting firms
**Say this first (1 line):** Walk the tree top-down from the roots to build the breadcrumb and depth, build the ancestor-descendant pairs (including each category paired with itself) with a second recursion, join products to the descendant side and `GROUP BY ancestor` for the roll-up, and a leaf is a category that nobody lists as a parent.

**Schema and sample data:** eight categories in two trees (Electronics and Books), 14 products. Product 113 has a NULL category and product 114 points to a category that does not exist; both are deliberately outside every count. Tablets is an empty leaf.
```sql
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Electronics'),(2,1,'Phones'),(3,2,'Android'),(4,2,'iOS'),(5,1,'Laptops'),
 (6,NULL,'Books'),(7,6,'Fiction'),(8,1,'Tablets');
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category_id INTEGER);
INSERT INTO products VALUES
 (101,3),(102,3),(103,3),(104,4),(105,4),(106,5),(107,5),(108,2),
 (109,7),(110,7),(111,7),(112,7),(113,NULL),(114,99);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE tree(category_id, depth, breadcrumb) AS (
  SELECT category_id, 0, name FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.category_id, t.depth + 1, t.breadcrumb || ' > ' || c.name
  FROM categories c JOIN tree t ON c.parent_id = t.category_id
), closure(ancestor, descendant) AS (
  SELECT category_id, category_id FROM categories
  UNION ALL
  SELECT cl.ancestor, c.category_id
  FROM closure cl JOIN categories c ON c.parent_id = cl.descendant
), rollup AS (
  SELECT cl.ancestor AS category_id, COUNT(p.product_id) AS products_incl_descendants
  FROM closure cl LEFT JOIN products p ON p.category_id = cl.descendant
  GROUP BY cl.ancestor
)
SELECT t.category_id, t.breadcrumb, t.depth,
       COALESCE(r.products_incl_descendants, 0) AS products_incl_descendants,
       CASE WHEN EXISTS (SELECT 1 FROM categories k WHERE k.parent_id = t.category_id) THEN 0 ELSE 1 END AS is_leaf
FROM tree t LEFT JOIN rollup r ON r.category_id = t.category_id
ORDER BY t.category_id
```
How it works:
- `tree` is top-down: the anchor is every root (`parent_id IS NULL`) with depth 0 and the breadcrumb equal to its name; each recursive step joins a child to its parent's row, adds 1 to the depth and appends `' > ' || name`.
- `closure` holds (ancestor, descendant) pairs. The anchor pairs every category with itself, and the recursive step extends a pair by one child of the descendant, so a category ends up paired with itself, its children, their children and so on. The aggregate is applied outside the recursion, in `rollup` (aggregates are not allowed in the recursive member).
- `LEFT JOIN products` keeps categories with no products (Tablets gets 0 instead of vanishing); `COUNT(p.product_id)` counts only matched rows.
- Leaf: `NOT EXISTS` a child row. I avoid `NOT IN (SELECT parent_id ...)` because the roots have a NULL `parent_id`, which makes the whole `NOT IN` return nothing (printed: 0 rows).

**pandas answer:** a parent walk for the breadcrumb and a merge loop for the pairs (shown once, identical to the Code block):
```py
    name = dict(zip(cats["category_id"], cats["name"]))
    parent = dict(zip(cats["category_id"], cats["parent_id"].astype("Int64")))
    rows = []
    for cid in cats["category_id"]:
        crumbs, cur, depth = [name[cid]], cid, 0
        while pd.notna(parent[cur]):
            cur = int(parent[cur])
            crumbs.append(name[cur])
            depth += 1
        rows.append((cid, " > ".join(reversed(crumbs)), depth))
    rep = pd.DataFrame(rows, columns=["category_id", "breadcrumb", "depth"])
    pairs = pd.DataFrame({"ancestor": cats["category_id"], "descendant": cats["category_id"]})
    edges = cats.dropna(subset=["parent_id"]).astype({"parent_id": int})
    frontier = pairs
    while not frontier.empty:
        frontier = (frontier.merge(edges, left_on="descendant", right_on="parent_id")
                            [["ancestor", "category_id"]].rename(columns={"category_id": "descendant"}))
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    counts = (pairs.merge(prods, left_on="descendant", right_on="category_id", how="left")
                   .groupby("ancestor")["product_id"].count().rename("products_incl_descendants"))
    rep = rep.merge(counts, left_on="category_id", right_index=True, how="left")
    rep["is_leaf"] = (~rep["category_id"].isin(edges["parent_id"])).astype(int)
    return rep.sort_values("category_id").reset_index(drop=True)
```

**Example:** by hand.
- Breadcrumbs: Android's parent is Phones (2), whose parent is Electronics (1): 'Electronics > Phones > Android', depth 2. Books has no parent: 'Books', depth 0.
- Direct counts (a plain `GROUP BY category_id`): Phones 1, Android 3, iOS 2, Laptops 2, Fiction 4, others 0.
- Roll-up: Phones = its own 1 + Android 3 + iOS 2 = 6. Electronics = Phones 6 + Laptops 2 + Tablets 0 + itself 0 = 8. Books = Fiction 4 = 4.
- Leaves: Android, iOS, Laptops, Tablets, Fiction.
- Products 113 (NULL category) and 114 (unknown category) are in no total; the root totals 8 + 4 = 12 equal the 12 products with a valid category.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after sorting by `category_id`.
```python
# Q13: category tree: breadcrumb, depth, product count including descendants, leaf flag
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Electronics'),(2,1,'Phones'),(3,2,'Android'),(4,2,'iOS'),(5,1,'Laptops'),
 (6,NULL,'Books'),(7,6,'Fiction'),(8,1,'Tablets');
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category_id INTEGER);
INSERT INTO products VALUES
 (101,3),(102,3),(103,3),(104,4),(105,4),(106,5),(107,5),(108,2),
 (109,7),(110,7),(111,7),(112,7),(113,NULL),(114,99);
"""
SQL_MAIN = """
WITH RECURSIVE tree(category_id, depth, breadcrumb) AS (
  SELECT category_id, 0, name FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.category_id, t.depth + 1, t.breadcrumb || ' > ' || c.name
  FROM categories c JOIN tree t ON c.parent_id = t.category_id
), closure(ancestor, descendant) AS (
  SELECT category_id, category_id FROM categories
  UNION ALL
  SELECT cl.ancestor, c.category_id
  FROM closure cl JOIN categories c ON c.parent_id = cl.descendant
), rollup AS (
  SELECT cl.ancestor AS category_id, COUNT(p.product_id) AS products_incl_descendants
  FROM closure cl LEFT JOIN products p ON p.category_id = cl.descendant
  GROUP BY cl.ancestor
)
SELECT t.category_id, t.breadcrumb, t.depth,
       COALESCE(r.products_incl_descendants, 0) AS products_incl_descendants,
       CASE WHEN EXISTS (SELECT 1 FROM categories k WHERE k.parent_id = t.category_id) THEN 0 ELSE 1 END AS is_leaf
FROM tree t LEFT JOIN rollup r ON r.category_id = t.category_id
ORDER BY t.category_id
"""
SQL_DIRECT = """
SELECT c.category_id, COUNT(p.product_id) AS direct_products
FROM categories c LEFT JOIN products p ON p.category_id = c.category_id
GROUP BY c.category_id ORDER BY c.category_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("direct count only (GROUP BY category_id):", dict(con.execute(SQL_DIRECT).fetchall()))

cats = pd.read_sql_query("SELECT * FROM categories", con)
prods = pd.read_sql_query("SELECT * FROM products", con)

def category_report(cats, prods):
    # pd:main
    name = dict(zip(cats["category_id"], cats["name"]))
    parent = dict(zip(cats["category_id"], cats["parent_id"].astype("Int64")))
    rows = []
    for cid in cats["category_id"]:
        crumbs, cur, depth = [name[cid]], cid, 0
        while pd.notna(parent[cur]):
            cur = int(parent[cur])
            crumbs.append(name[cur])
            depth += 1
        rows.append((cid, " > ".join(reversed(crumbs)), depth))
    rep = pd.DataFrame(rows, columns=["category_id", "breadcrumb", "depth"])
    pairs = pd.DataFrame({"ancestor": cats["category_id"], "descendant": cats["category_id"]})
    edges = cats.dropna(subset=["parent_id"]).astype({"parent_id": int})
    frontier = pairs
    while not frontier.empty:
        frontier = (frontier.merge(edges, left_on="descendant", right_on="parent_id")
                            [["ancestor", "category_id"]].rename(columns={"category_id": "descendant"}))
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    counts = (pairs.merge(prods, left_on="descendant", right_on="category_id", how="left")
                   .groupby("ancestor")["product_id"].count().rename("products_incl_descendants"))
    rep = rep.merge(counts, left_on="category_id", right_index=True, how="left")
    rep["is_leaf"] = (~rep["category_id"].isin(edges["parent_id"])).astype(int)
    return rep.sort_values("category_id").reset_index(drop=True)
    # pd:end

pd_df = category_report(cats, prods)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by category_id
print("pandas equal to SQL; leaf categories:", list(pd_df.loc[pd_df.is_leaf == 1, "breadcrumb"]))
print("products not counted anywhere (NULL category or unknown category):",
      con.execute("SELECT product_id FROM products WHERE category_id IS NULL OR category_id NOT IN (SELECT category_id FROM categories)").fetchall())
# a leaf can be filtered with NOT IN only if parent_id has no NULLs: it has (roots), so show the trap
print("NOT IN version of the leaf filter returns:", con.execute("SELECT COUNT(*) FROM categories WHERE category_id NOT IN (SELECT parent_id FROM categories)").fetchone()[0], "rows (NULL parent_id of the roots poisons it)")
print("total rollup of roots:", int(pd_df.loc[pd_df.depth == 0, "products_incl_descendants"].sum()), "= products with a valid category:", int(prods["category_id"].isin(cats["category_id"]).sum()))
print("no root rows (anchor returns nothing) ->", pd.read_sql_query(SQL_MAIN.replace("FROM categories WHERE parent_id IS NULL", "FROM categories WHERE 1 = 0"), con).shape[0], "rows")
print("asserts passed")
```

**Output (my run):**
```text
 category_id                     breadcrumb  depth  products_incl_descendants  is_leaf
           1                    Electronics      0                          8        0
           2           Electronics > Phones      1                          6        0
           3 Electronics > Phones > Android      2                          3        1
           4     Electronics > Phones > iOS      2                          2        1
           5          Electronics > Laptops      1                          2        1
           6                          Books      0                          4        0
           7                Books > Fiction      1                          4        1
           8          Electronics > Tablets      1                          0        1
direct count only (GROUP BY category_id): {1: 0, 2: 1, 3: 3, 4: 2, 5: 2, 6: 0, 7: 4, 8: 0}
pandas equal to SQL; leaf categories: ['Electronics > Phones > Android', 'Electronics > Phones > iOS', 'Electronics > Laptops', 'Books > Fiction', 'Electronics > Tablets']
products not counted anywhere (NULL category or unknown category): [(113,), (114,)]
NOT IN version of the leaf filter returns: 0 rows (NULL parent_id of the roots poisons it)
total rollup of roots: 12 = products with a valid category: 12
no root rows (anchor returns nothing) -> 0 rows
asserts passed
```

**Edge cases:**
- Product with a NULL or unknown category: not counted under any category. Report them separately as a data-quality number.
- Category with no products or no children: the `LEFT JOIN` and `COALESCE` keep a 0 row (Tablets).
- A category whose parent_id points to a missing row never appears in `tree` (the top-down walk starts only at roots); Q15 in this part covers finding such orphans.
- Cycles in the category table would make both recursions loop; this data has none, and a depth cap or path guard (Q8) is the fix if the data cannot be trusted.
- Duplicate `(category_id)` rows would double counts; the primary key prevents it here.
- Multiple roots are normal (Electronics and Books).

**Then explain:**
- Why `GROUP BY category_id` alone misses descendants: a product is stored on its own category only, so Electronics shows 0 although it contains 8 products. The roll-up needs every ancestor to see the product, which is exactly what the closure pairs provide.
- Top-down versus pairs: the top-down walk carries one row per category (breadcrumb, depth), while the closure carries one row per (ancestor, descendant), which is about nodes x depth rows for a tree; fine for a catalogue, heavy for a huge deep tree.
- `' > '` is the separator; `||` is standard SQL concatenation (SQL Server uses `+` or `CONCAT`, MySQL uses `CONCAT` unless `PIPES_AS_CONCAT` is on; not executed here).
- MySQL 8 fixes the column type from the anchor, so the breadcrumb needs a `CAST(name AS CHAR(500))` in the anchor to avoid truncation (from the MySQL docs; not executed here).

**Follow-ups:**
- "Only leaf categories with products?" Filter `is_leaf = 1 AND products_incl_descendants > 0`.
- "Products per breadcrumb for a dashboard?" Join the report back to products on `category_id`.
- "Count distinct products if a product can sit in two categories?" Use `COUNT(DISTINCT p.product_id)` so a product in both Phones and Android is counted once under Electronics.

**Common mistakes:**
- `NOT IN` with NULL parents for the leaf filter.
- Counting products with an inner join and losing empty categories.
- Anchoring the closure without the self pair, so a category's own products are not counted.
- Counting a product twice at an ancestor when it belongs to two descendants and using `COUNT(*)` instead of `COUNT(DISTINCT ...)`.
- Aggregating inside the recursive member.

### Q14 ⭐⭐ 🟢 Recursive CTE versus self-join versus window: employees(emp_id, manager_id, name). For a company known to have at most three levels return each employee with manager and grand-manager names using LEFT JOINs, then the recursive version for unknown depth. State when each is right (fixed known depth and a tiny table versus unknown depth), why window functions (LAG, SUM OVER) cannot follow parent pointers by themselves, and one case where a window function beats recursion (a running total with no state dependence). Compare the readability, the query plan shape and the failure mode when the org gets a fourth level.
**Asked at:** LeetCode 1270 All People Report to the Given Manager (doocs mirror opened: head is employee 1, chain at most three managers, two self-joins; the 'given manager' framing at Hello Interview and DataVidhya seen only as search snippets, so a general version is an expert extension); public problem bank, not a candidate report; analyst and data scientist screens
**Say this first (1 line):** For a table known to have at most three levels, two `LEFT JOIN`s to the same table are the simplest, fastest and most readable answer; for unknown depth I use a recursive CTE that produces (employee, ancestor, distance) rows; window functions cannot follow a parent pointer, they only look at neighbouring rows in a sort order, so they are the right tool only for running or ranked calculations that need no per-row state.

**Schema and sample data:** six employees on three levels (Tim is CEO). Later in the Code block I insert Meera under Shyam to create a fourth level and show what the fixed join does then.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),(5,2,'Asha'),(6,3,'Ram');
```

**SQL answer:** two versions. The fixed-depth `SQL_FIXED` (in the Code block):
```sql
SELECT e.emp_id, e.name, m.name AS manager, g.name AS grand_manager,
       COALESCE(g.name, m.name, e.name) AS top_boss
FROM employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id
LEFT JOIN employees g ON g.emp_id = m.manager_id
ORDER BY e.emp_id
```
and the unknown-depth `SQL_MAIN` (in the Code block). It builds every (employee, ancestor, distance) pair with a depth cap of 20 as a guard, then picks distance 1, distance 2 and the farthest ancestor as the top boss:
```sql
WITH RECURSIVE anc(emp_id, anc_id, dist) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT a.emp_id, e.manager_id, a.dist + 1
  FROM anc a JOIN employees e ON e.emp_id = a.anc_id
  WHERE e.manager_id IS NOT NULL AND a.dist < 20
)
SELECT e.emp_id, e.name,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 1) AS manager,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 2) AS grand_manager,
       COALESCE((SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id
                 WHERE a.emp_id = e.emp_id ORDER BY a.dist DESC LIMIT 1), e.name) AS top_boss
FROM employees e
ORDER BY e.emp_id
```

**pandas answer:** the merge loop for the recursive result (shown once, identical to the Code block); the two-merge fixed-depth version is in the Code block too:
```py
    nm = emps.set_index("emp_id")["name"]
    pairs = emps.dropna(subset=["manager_id"]).assign(anc_id=lambda d: d["manager_id"].astype(int), dist=1)[["emp_id", "anc_id", "dist"]]
    allp, cur = [pairs], pairs
    while not cur.empty:
        nxt = cur.merge(emps.dropna(subset=["manager_id"]), left_on="anc_id", right_on="emp_id", suffixes=("", "_m"))
        cur = nxt.assign(anc_id=nxt["manager_id"].astype(int), dist=nxt["dist"] + 1)[["emp_id", "anc_id", "dist"]]
        allp.append(cur)
    anc = pd.concat(allp, ignore_index=True)
    out = emps[["emp_id", "name"]].copy()
    for label, k in (("manager", 1), ("grand_manager", 2)):
        s = anc[anc["dist"] == k].set_index("emp_id")["anc_id"].map(nm)
        out[label] = out["emp_id"].map(s)
    top = anc.sort_values("dist").groupby("emp_id")["anc_id"].last().map(nm)
    out["top_boss"] = out["emp_id"].map(top).fillna(out["name"])
    return out.sort_values("emp_id").reset_index(drop=True)
```

**Example:** on the three-level data, Ram reports to Hari, who reports to Tim: manager Hari, grand-manager Tim, top boss Tim. Tim has no manager (NULL, so the `LEFT JOIN` finds nothing): manager and grand-manager are NULL and the top boss falls back to Tim himself. Radha has a manager but no grand-manager, so her top boss is the manager, Tim. Both queries give the identical table here (asserted). Now insert Meera under Shyam: Tim > Radha > Shyam > Meera. The fixed join still shows manager Shyam and grand-manager Radha correctly (those two columns are what it was built for), but its top boss for Meera is Radha because it believes grand-manager is the top; the recursive version says Tim. No error is raised.

**Code:** run with `python3 -I`. Asserts: recursive equals fixed on three levels; the pandas loop equals the SQL recursive result and the pandas two-merge equals the fixed SQL on four levels (all sorted by `emp_id`).
```python
# Q14: recursive CTE versus fixed self-joins versus window functions on a manager hierarchy
import sqlite3
import pandas as pd

SCHEMA3 = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),(5,2,'Asha'),(6,3,'Ram');
"""
SQL_MAIN = """
WITH RECURSIVE anc(emp_id, anc_id, dist) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT a.emp_id, e.manager_id, a.dist + 1
  FROM anc a JOIN employees e ON e.emp_id = a.anc_id
  WHERE e.manager_id IS NOT NULL AND a.dist < 20
)
SELECT e.emp_id, e.name,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 1) AS manager,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 2) AS grand_manager,
       COALESCE((SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id
                 WHERE a.emp_id = e.emp_id ORDER BY a.dist DESC LIMIT 1), e.name) AS top_boss
FROM employees e
ORDER BY e.emp_id
"""
SQL_FIXED = """
SELECT e.emp_id, e.name, m.name AS manager, g.name AS grand_manager,
       COALESCE(g.name, m.name, e.name) AS top_boss
FROM employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id
LEFT JOIN employees g ON g.emp_id = m.manager_id
ORDER BY e.emp_id
"""
SQL_LAG = """
SELECT emp_id, name, LAG(name) OVER (ORDER BY emp_id) AS lag_as_manager, manager_id FROM employees ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA3)
rec3 = pd.read_sql_query(SQL_MAIN, con)
fix3 = pd.read_sql_query(SQL_FIXED, con)
print("three-level company, fixed LEFT JOINs:")
print(fix3.to_string(index=False))
pd.testing.assert_frame_equal(rec3, fix3)
print("recursive version gives the identical table on 3 levels")

con.execute("INSERT INTO employees VALUES (7, 4, 'Meera')")   # a fourth level: Tim > Radha > Shyam > Meera
rec4 = pd.read_sql_query(SQL_MAIN, con)
fix4 = pd.read_sql_query(SQL_FIXED, con)
print("after adding a fourth level (Meera reports to Shyam):")
diff = rec4.merge(fix4, on=["emp_id", "name"], suffixes=("_rec", "_fixed"))
print(diff[diff.top_boss_rec != diff.top_boss_fixed][["name", "manager_rec", "grand_manager_rec", "top_boss_rec", "top_boss_fixed"]].to_string(index=False))
print("rows where the fixed join disagrees with the recursive one:", int((diff.top_boss_rec != diff.top_boss_fixed).sum()), "(no error, just a wrong top boss)")
print("LAG over emp_id is not the manager:")
print(pd.read_sql_query(SQL_LAG, con).to_string(index=False))

emps = pd.read_sql_query("SELECT * FROM employees", con)

def hierarchy(emps):
    # pd:main
    nm = emps.set_index("emp_id")["name"]
    pairs = emps.dropna(subset=["manager_id"]).assign(anc_id=lambda d: d["manager_id"].astype(int), dist=1)[["emp_id", "anc_id", "dist"]]
    allp, cur = [pairs], pairs
    while not cur.empty:
        nxt = cur.merge(emps.dropna(subset=["manager_id"]), left_on="anc_id", right_on="emp_id", suffixes=("", "_m"))
        cur = nxt.assign(anc_id=nxt["manager_id"].astype(int), dist=nxt["dist"] + 1)[["emp_id", "anc_id", "dist"]]
        allp.append(cur)
    anc = pd.concat(allp, ignore_index=True)
    out = emps[["emp_id", "name"]].copy()
    for label, k in (("manager", 1), ("grand_manager", 2)):
        s = anc[anc["dist"] == k].set_index("emp_id")["anc_id"].map(nm)
        out[label] = out["emp_id"].map(s)
    top = anc.sort_values("dist").groupby("emp_id")["anc_id"].last().map(nm)
    out["top_boss"] = out["emp_id"].map(top).fillna(out["name"])
    return out.sort_values("emp_id").reset_index(drop=True)
    # pd:end

pd.testing.assert_frame_equal(hierarchy(emps), rec4)   # compared after sorting by emp_id
print("pandas ancestor loop equal to the SQL recursive result (4 levels)")
f = emps.merge(emps[["emp_id", "name", "manager_id"]].rename(columns={"emp_id": "mid", "name": "manager", "manager_id": "gid"}), left_on="manager_id", right_on="mid", how="left")
f = f.merge(emps[["emp_id", "name"]].rename(columns={"emp_id": "gid", "name": "grand_manager"}), on="gid", how="left")
f["top_boss"] = f["grand_manager"].fillna(f["manager"]).fillna(f["name"])
f = f[["emp_id", "name", "manager", "grand_manager", "top_boss"]].sort_values("emp_id").reset_index(drop=True)
pd.testing.assert_frame_equal(f, fix4)
print("pandas two-merge version equal to the fixed-join SQL")

for label, q in (("fixed joins", SQL_FIXED), ("recursive", SQL_MAIN)):
    print("EXPLAIN QUERY PLAN,", label)
    for r in con.execute("EXPLAIN QUERY PLAN " + q):
        print("  ", r[3])

# a window function where it wins: running total with no state dependence
con.executescript("CREATE TABLE sales(day TEXT, amount INTEGER); INSERT INTO sales VALUES ('2024-03-01',10),('2024-03-02',5),('2024-03-03',20);")
print(con.execute("SELECT day, amount, SUM(amount) OVER (ORDER BY day) FROM sales ORDER BY day").fetchall())
print("empty employees ->", con.execute(SQL_MAIN.replace("FROM employees e\nORDER", "FROM employees e WHERE 1 = 0\nORDER")).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
three-level company, fixed LEFT JOINs:
 emp_id  name manager grand_manager top_boss
      1   Tim     NaN           NaN      Tim
      2 Radha     Tim           NaN      Tim
      3  Hari     Tim           NaN      Tim
      4 Shyam   Radha           Tim      Tim
      5  Asha   Radha           Tim      Tim
      6   Ram    Hari           Tim      Tim
recursive version gives the identical table on 3 levels
after adding a fourth level (Meera reports to Shyam):
 name manager_rec grand_manager_rec top_boss_rec top_boss_fixed
Meera       Shyam             Radha          Tim          Radha
rows where the fixed join disagrees with the recursive one: 1 (no error, just a wrong top boss)
LAG over emp_id is not the manager:
 emp_id  name lag_as_manager  manager_id
      1   Tim            NaN         NaN
      2 Radha            Tim         1.0
      3  Hari          Radha         1.0
      4 Shyam           Hari         2.0
      5  Asha          Shyam         2.0
      6   Ram           Asha         3.0
      7 Meera            Ram         4.0
pandas ancestor loop equal to the SQL recursive result (4 levels)
pandas two-merge version equal to the fixed-join SQL
EXPLAIN QUERY PLAN, fixed joins
   SCAN e
   SEARCH m USING INTEGER PRIMARY KEY (rowid=?) LEFT-JOIN
   SEARCH g USING INTEGER PRIMARY KEY (rowid=?) LEFT-JOIN
EXPLAIN QUERY PLAN, recursive
   SCAN e
   CORRELATED SCALAR SUBQUERY 3
   MATERIALIZE anc
   SETUP
   SCAN employees
   RECURSIVE STEP
   SCAN a
   SEARCH e USING INTEGER PRIMARY KEY (rowid=?)
   BLOOM FILTER ON a (emp_id=? AND dist=?)
   SEARCH a USING AUTOMATIC PARTIAL COVERING INDEX (emp_id=? AND dist=?)
   SEARCH n USING INTEGER PRIMARY KEY (rowid=?)
   CORRELATED SCALAR SUBQUERY 4
   BLOOM FILTER ON a (emp_id=? AND dist=?)
   SEARCH a USING AUTOMATIC PARTIAL COVERING INDEX (emp_id=? AND dist=?)
   SEARCH n USING INTEGER PRIMARY KEY (rowid=?)
   CORRELATED SCALAR SUBQUERY 5
   BLOOM FILTER ON a (emp_id=?)
   SEARCH a USING AUTOMATIC COVERING INDEX (emp_id=?)
   SEARCH n USING INTEGER PRIMARY KEY (rowid=?)
   USE TEMP B-TREE FOR ORDER BY
[('2024-03-01', 10, 10), ('2024-03-02', 5, 15), ('2024-03-03', 20, 35)]
empty employees -> []
asserts passed
```
The query plan lines are what SQLite 3.45.1 printed here; other versions may word them differently.

**Edge cases:**
- CEO (NULL manager): the `LEFT JOIN` keeps the row with NULL manager columns; with an `INNER JOIN` the CEO and all second-level employees would disappear (a common bug).
- Orphan (manager_id pointing to a missing row): the fixed join gives a NULL manager name (looks like a CEO); the recursive version stops at the missing row. See Q15 for the checks.
- Cycle in the data: the fixed join is immune (it only goes two hops), the recursive version needs a guard; I used `a.dist < 20`.
- Empty table: both return no rows (printed for the recursive one).
- The LAG attempt shows why windows fail: `LAG(name) OVER (ORDER BY emp_id)` gives the previous row in id order, which happened to be right for Radha and wrong for everyone else (Hari gets Radha, Meera gets Ram).

**Then explain:**
- Readability: the two-join query is easy to read, but each extra level is another join and another `COALESCE`; the recursive version is longer once but does not change with depth.
- Query plan shape: the fixed version is one scan of `e` with one primary-key lookup per join (printed). The recursive plan has a `SETUP` and `RECURSIVE STEP` for the CTE, and SQLite built automatic indexes on the materialised result for the three correlated subqueries. For a tiny table both are instant; at scale, an index on `manager_id` matters for the recursive step.
- Failure mode on a fourth level: the fixed join does not fail, it silently answers for the first two levels only. The recursive version either gets it right or (on a cycle without guard) never ends, which is a loud failure.
- When each is right: fixed joins for a known shallow hierarchy and one-off reports; recursion for unknown depth, subtree or chain questions, and roll-ups.
- Where a window function wins: a running total such as `SUM(amount) OVER (ORDER BY day)` (printed: 10, 15, 35) needs no per-row state beyond the sort order, and it is a single pass with no recursion.

**Follow-ups:**
- "How many levels does the company have?" `MAX(dist) + 1` from the ancestor pairs, or a recursive depth query.
- "Can you flatten to a fixed number of columns for a BI tool?" Yes, with pivot-style `MAX(CASE WHEN dist = k ...)` columns, choosing a maximum k and accepting that deeper levels are cut off.
- "What changes in other engines?" PostgreSQL and MySQL 8 use `WITH RECURSIVE`, SQL Server omits `RECURSIVE` (default `MAXRECURSION` 100); all hedged, not executed.

**Common mistakes:**
- `INNER JOIN` to the manager, which drops the CEO.
- Assuming "at most three levels" stays true.
- Trying `LAG` or `SUM OVER` to climb parent pointers.
- Writing the top boss as the last non-NULL in a fixed chain and not noticing when the chain is longer.
- No depth cap or visited check when the data may contain loops.

### Q15 ⭐⭐ 🟡 Cycles, orphans and multiple roots in hierarchy data: employees(emp_id, manager_id, name) loaded from an HR export. Write queries that find (a) orphans (manager_id not NULL and not in the table), (b) self-managed rows, (c) rows with more than one root or no root, (d) employees whose upward chain loops (cycle membership, using a path or depth guard), and (e) employees unreachable from the CEO by a top-down walk. Explain why NOT IN with a NULL manager_id is a trap, why a cycle has no root and so is invisible to a top-down query, and give a data-quality summary row per problem type.
**Asked at:** cycle-handling guides (search snippets only, not opened: manual path string or array of visited ids with a flag, the itprotoday 'Cycling with CTEs' article, Oracle NOCYCLE and CONNECT_BY_ISCYCLE docs, PostgreSQL CYCLE); the opened PostgreSQL page says UNION cannot stop a cycle when a depth column makes every row unique; guides and documentation, not candidate reports; data engineer and analyst rounds
**Say this first (1 line):** One query per problem type, then a summary row each: orphans with `NOT EXISTS` (never `NOT IN`), self-managed with `manager_id = emp_id`, roots by counting `manager_id IS NULL` (should be exactly one), cycles by an upward walk with a step cap, and unreachable rows by a top-down walk from the CEO, because a cycle has no root so a top-down query never sees it.

**Schema and sample data:** twelve rows from an imaginary HR export, with every problem planted. Tim (1) is the CEO and has a proper tree (Radha, Hari, Shyam: 1 to 4). Employee 5 is an orphan (manager 99 does not exist) and 12 reports to the orphan. Employee 6 is self-managed. Employees 7, 8, 9 form a 3-cycle (7 reports to 8, 8 to 9, 9 to 7) and 10 reports into the cycle. Zed (11) is a second root.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),
 (5,99,'Orphan'),(6,6,'Selfie'),
 (7,8,'LoopA'),(8,9,'LoopB'),(9,7,'LoopC'),(10,7,'BelowLoop'),
 (11,NULL,'Zed'),(12,5,'BelowOrphan');
```

**SQL answer:** `SQL_MAIN` in the Code block, one row per problem type with a count and the ids:
```sql
WITH RECURSIVE n(n) AS (SELECT COUNT(*) FROM employees),
up(emp_id, cur, steps) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.emp_id, e.manager_id, u.steps + 1
  FROM up u JOIN employees e ON e.emp_id = u.cur
  WHERE e.manager_id IS NOT NULL AND u.steps < (SELECT n FROM n)
),
down(emp_id) AS (
  SELECT emp_id FROM employees WHERE emp_id = 1
  UNION
  SELECT e.emp_id FROM employees e JOIN down d ON e.manager_id = d.emp_id
),
issues(problem, emp_id) AS (
  SELECT 'a orphan (manager not in table)', e.emp_id FROM employees e
    WHERE e.manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
  UNION ALL SELECT 'b self-managed', emp_id FROM employees WHERE manager_id = emp_id
  UNION ALL SELECT 'c root rows (manager NULL)', emp_id FROM employees WHERE manager_id IS NULL
  UNION ALL SELECT 'd member of a cycle', emp_id FROM up WHERE cur = emp_id GROUP BY emp_id
  UNION ALL SELECT 'd chain never reaches a root', emp_id FROM up WHERE steps = (SELECT n FROM n) GROUP BY emp_id
  UNION ALL SELECT 'e unreachable from CEO (emp 1)', emp_id FROM employees WHERE emp_id NOT IN (SELECT emp_id FROM down)
)
SELECT problem, COUNT(*) AS n_rows,
       group_concat(emp_id, ',') AS emp_ids
FROM (SELECT * FROM issues ORDER BY problem, emp_id)
GROUP BY problem
ORDER BY problem
```
How it works:
- (a) Orphans: `manager_id` is not NULL and no row has that `emp_id`. `NOT EXISTS` is safe with NULLs.
- (b) Self-managed: `manager_id = emp_id`.
- (c) Roots: rows with `manager_id IS NULL`. A healthy table has exactly one. Two or more means multiple roots (here 1 and 11); zero means every row has a manager, which means there is a cycle somewhere (checked on a ring table below).
- (d) Cycles: `up` walks from each employee to their manager, then that manager's manager, and so on. A row with `cur = emp_id` means the walk came back to its own start, so the employee is a member of a cycle (a self-managed row is a cycle of length 1, so 6 is reported here as well as in (b)). The step cap is the guard: the walk stops after `n` (the row count) steps, because a chain without a cycle has at most n - 1 managers. A walk that reaches `n` steps never ended: that finds the members and also the rows hanging below a cycle (employee 10), which are not members but whose chain loops.
- (e) Unreachable from the CEO: walk down from emp 1 with `UNION` (dedups rows, so even a duplicate edge cannot loop) and list everyone not in the result. That finds the second root and its tree, the orphan subtree, the self-managed row and the whole cycle.
- The outer query groups the issue rows into one summary row per problem with `COUNT` and `group_concat` of the ids (the ids are sorted in the subquery; SQLite keeps that order here, but `group_concat` order is not guaranteed by the standard, which is why the pandas version sorts explicitly and the assert would catch a mismatch).

**pandas answer:** dict-based version of the same five checks (shown once, identical to the Code block):
```py
    ids = set(emps["emp_id"])
    par = dict(zip(emps["emp_id"], emps["manager_id"]))
    n = len(emps)
    found = {
        "a orphan (manager not in table)": [e for e, m in par.items() if pd.notna(m) and m not in ids],
        "b self-managed": [e for e, m in par.items() if pd.notna(m) and m == e],
        "c root rows (manager NULL)": [e for e, m in par.items() if pd.isna(m)],
    }
    cyc, never = [], []
    for e in par:
        cur, steps, hit = par[e], 0, False
        while pd.notna(cur) and cur in ids and steps < n:
            steps += 1
            if cur == e:
                hit = True
            cur = par[cur]
        if hit:
            cyc.append(e)
        if steps == n:
            never.append(e)
    found["d member of a cycle"] = cyc
    found["d chain never reaches a root"] = never
    kids = emps.dropna(subset=["manager_id"]).groupby("manager_id")["emp_id"].apply(list).to_dict()
    seen, stack = {ceo}, [ceo]
    while stack:
        for k in kids.get(stack.pop(), []):
            if k not in seen:
                seen.add(k)
                stack.append(k)
    found["e unreachable from CEO (emp 1)"] = [e for e in par if e not in seen]
    rows = [(p, len(v), ",".join(str(x) for x in sorted(v))) for p, v in found.items() if v]
    return pd.DataFrame(rows, columns=["problem", "n_rows", "emp_ids"]).sort_values("problem").reset_index(drop=True)
```

**Example:** by hand.
- Orphans: 5 (manager 99 missing). Self-managed: 6. Roots: 1 and 11 (two roots).
- Cycle: 7 to 8 to 9 to 7. Walking up from 7 gives 8, 9, 7, which is 7 itself, so 7, 8, 9 are members; 6 is a one-step cycle. Employee 10's walk goes 7, 8, 9, 7, ... and never reaches a root but is not a member; so "chain never reaches a root" is 6, 7, 8, 9, 10 (five rows) and "member of a cycle" is 6, 7, 8, 9 (four rows). Employee 12 walks 5, then 99 is missing and the walk stops, so 12 is an orphan-subtree row, not a cycle row.
- Top-down from 1 reaches 1, 2, 3, 4 only. Unreachable: 5, 6, 7, 8, 9, 10, 11, 12 (eight rows).

**Code:** run with `python3 -I`. The assert compares the SQL summary and the pandas summary after sorting by problem name; the NOT IN trap, the ring table and the unguarded loop are printed after.
```python
# Q15: data-quality checks on an HR hierarchy: orphans, self-managed, roots, cycles, unreachable rows
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),
 (5,99,'Orphan'),(6,6,'Selfie'),
 (7,8,'LoopA'),(8,9,'LoopB'),(9,7,'LoopC'),(10,7,'BelowLoop'),
 (11,NULL,'Zed'),(12,5,'BelowOrphan');
"""
SQL_MAIN = """
WITH RECURSIVE n(n) AS (SELECT COUNT(*) FROM employees),
up(emp_id, cur, steps) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.emp_id, e.manager_id, u.steps + 1
  FROM up u JOIN employees e ON e.emp_id = u.cur
  WHERE e.manager_id IS NOT NULL AND u.steps < (SELECT n FROM n)
),
down(emp_id) AS (
  SELECT emp_id FROM employees WHERE emp_id = 1
  UNION
  SELECT e.emp_id FROM employees e JOIN down d ON e.manager_id = d.emp_id
),
issues(problem, emp_id) AS (
  SELECT 'a orphan (manager not in table)', e.emp_id FROM employees e
    WHERE e.manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
  UNION ALL SELECT 'b self-managed', emp_id FROM employees WHERE manager_id = emp_id
  UNION ALL SELECT 'c root rows (manager NULL)', emp_id FROM employees WHERE manager_id IS NULL
  UNION ALL SELECT 'd member of a cycle', emp_id FROM up WHERE cur = emp_id GROUP BY emp_id
  UNION ALL SELECT 'd chain never reaches a root', emp_id FROM up WHERE steps = (SELECT n FROM n) GROUP BY emp_id
  UNION ALL SELECT 'e unreachable from CEO (emp 1)', emp_id FROM employees WHERE emp_id NOT IN (SELECT emp_id FROM down)
)
SELECT problem, COUNT(*) AS n_rows,
       group_concat(emp_id, ',') AS emp_ids
FROM (SELECT * FROM issues ORDER BY problem, emp_id)
GROUP BY problem
ORDER BY problem
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

emps = pd.read_sql_query("SELECT * FROM employees", con)

def quality(emps, ceo=1):
    # pd:main
    ids = set(emps["emp_id"])
    par = dict(zip(emps["emp_id"], emps["manager_id"]))
    n = len(emps)
    found = {
        "a orphan (manager not in table)": [e for e, m in par.items() if pd.notna(m) and m not in ids],
        "b self-managed": [e for e, m in par.items() if pd.notna(m) and m == e],
        "c root rows (manager NULL)": [e for e, m in par.items() if pd.isna(m)],
    }
    cyc, never = [], []
    for e in par:
        cur, steps, hit = par[e], 0, False
        while pd.notna(cur) and cur in ids and steps < n:
            steps += 1
            if cur == e:
                hit = True
            cur = par[cur]
        if hit:
            cyc.append(e)
        if steps == n:
            never.append(e)
    found["d member of a cycle"] = cyc
    found["d chain never reaches a root"] = never
    kids = emps.dropna(subset=["manager_id"]).groupby("manager_id")["emp_id"].apply(list).to_dict()
    seen, stack = {ceo}, [ceo]
    while stack:
        for k in kids.get(stack.pop(), []):
            if k not in seen:
                seen.add(k)
                stack.append(k)
    found["e unreachable from CEO (emp 1)"] = [e for e in par if e not in seen]
    rows = [(p, len(v), ",".join(str(x) for x in sorted(v))) for p, v in found.items() if v]
    return pd.DataFrame(rows, columns=["problem", "n_rows", "emp_ids"]).sort_values("problem").reset_index(drop=True)
    # pd:end

pd_df = quality(emps)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by problem
print("pandas equal to SQL")

# the NOT IN trap
print("leaf query with NOT IN (NULL manager_id in the list):",
      con.execute("SELECT COUNT(*) FROM employees WHERE emp_id NOT IN (SELECT manager_id FROM employees)").fetchone()[0], "rows")
print("same with NOT IN ... WHERE manager_id IS NOT NULL:",
      con.execute("SELECT COUNT(*) FROM employees WHERE emp_id NOT IN (SELECT manager_id FROM employees WHERE manager_id IS NOT NULL)").fetchone()[0], "rows")
con.executescript("CREATE TABLE raw(emp_id INTEGER, manager_id INTEGER); INSERT INTO raw SELECT emp_id, manager_id FROM employees; INSERT INTO raw VALUES (NULL, 1);")
print("orphans via NOT IN on an export whose emp_id has a NULL row:",
      con.execute("SELECT COUNT(*) FROM raw WHERE manager_id NOT IN (SELECT emp_id FROM raw)").fetchone()[0],
      "| via NOT EXISTS:", con.execute("SELECT COUNT(*) FROM raw r WHERE manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM raw m WHERE m.emp_id = r.manager_id)").fetchone()[0])

# no root at all: a table that is only a cycle looks fine to a top-down query
con.executescript("CREATE TABLE ring(emp_id INTEGER PRIMARY KEY, manager_id INTEGER); INSERT INTO ring VALUES (1,2),(2,3),(3,1);")
print("ring table: root rows =", con.execute("SELECT COUNT(*) FROM ring WHERE manager_id IS NULL").fetchone()[0],
      "| top-down walk from the root finds", con.execute("""
WITH RECURSIVE d(emp_id) AS (SELECT emp_id FROM ring WHERE manager_id IS NULL UNION SELECT r.emp_id FROM ring r JOIN d ON r.manager_id = d.emp_id)
SELECT COUNT(*) FROM d""").fetchone()[0], "rows")

# what happens without the guard: the upward walk from emp 7, bounded only by LIMIT
print("upward walk from emp 7 with UNION ALL and no step cap, stopped by LIMIT 12:",
      con.execute("""WITH RECURSIVE up(cur, steps) AS (SELECT manager_id, 1 FROM employees WHERE emp_id = 7
                     UNION ALL SELECT e.manager_id, u.steps + 1 FROM up u JOIN employees e ON e.emp_id = u.cur LIMIT 12)
                     SELECT COUNT(*), MAX(steps) FROM up""").fetchone())
con2 = sqlite3.connect(":memory:")
con2.execute("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT)")
print("empty table ->", len(pd.read_sql_query(SQL_MAIN, con2)), "problem rows; pandas:", len(quality(emps.iloc[0:0])), "rows")
print("asserts passed")
```

**Output (my run):**
```text
                        problem  n_rows            emp_ids
a orphan (manager not in table)       1                  5
                 b self-managed       1                  6
     c root rows (manager NULL)       2               1,11
   d chain never reaches a root       5         6,7,8,9,10
            d member of a cycle       4            6,7,8,9
 e unreachable from CEO (emp 1)       8 5,6,7,8,9,10,11,12
pandas equal to SQL
leaf query with NOT IN (NULL manager_id in the list): 0 rows
same with NOT IN ... WHERE manager_id IS NOT NULL: 5 rows
orphans via NOT IN on an export whose emp_id has a NULL row: 0 | via NOT EXISTS: 1
ring table: root rows = 0 | top-down walk from the root finds 0 rows
upward walk from emp 7 with UNION ALL and no step cap, stopped by LIMIT 12: (12, 12)
empty table -> 0 problem rows; pandas: 0 rows
asserts passed
```
In the run, the unguarded upward walk from employee 7 (UNION ALL, no step cap) produced 12 rows and reached step 12 before the `LIMIT 12` inside the recursive select stopped it; without the limit it would not terminate.

**Edge cases:**
- NULL `manager_id` is a legitimate root, not an orphan. Checks (a) and (b) require `manager_id IS NOT NULL` first.
- `NOT IN` trap, shown by running it: `emp_id NOT IN (SELECT manager_id FROM employees)` returns 0 rows because the subquery contains the CEO's NULL and `x NOT IN (..., NULL)` is never true (printed: 0 rows; filtering the NULL out gives 5 rows). The same happens on orphans when the export has a row with a NULL `emp_id`: `manager_id NOT IN (SELECT emp_id ...)` returned 0 while `NOT EXISTS` found 1.
- No root at all: the ring table (1 to 2 to 3 to 1) has 0 root rows and a top-down query from the roots returns 0 rows, so the whole table is invisible. A cycle has no root, so only the "unreachable" or "number of roots is not 1" checks reveal it.
- Duplicate rows: `emp_id` is a primary key here so none; if the export has no key, duplicates multiply every walk (use `UNION` for the downward walk and `SELECT DISTINCT` first).
- Empty table: no problem rows (printed, both engines).
- Which row is "the CEO" is an assumption (emp 1 here); if there are two roots you have to be told which is the real one.

**Then explain:**
- Why no root means no top-down visibility: a top-down recursion starts from rows with no manager and follows children; a cycle's rows all have managers and are children of each other, never of a root.
- Why a guard is mandatory here: the point of the query is to run on data that may be broken, so the walk has to terminate on a cycle by construction. The cap `steps < n` is simple and engine-independent; path tracking (as in Q8) is the alternative.
- A summary row per problem type is what a data-quality gate wants: fail the load if orphans, self-managed or cycle counts are non-zero, and if the root count is not 1.
- Other engines (not executed here): PostgreSQL 14+ has a `CYCLE ... SET ... USING` clause that marks rows which revisit a node; Oracle has `CONNECT BY NOCYCLE` with `CONNECT_BY_ISCYCLE` and raises ORA-01436 on a loop without NOCYCLE; MySQL stops at `cte_max_recursion_depth` and SQL Server at `MAXRECURSION` with an error (all from documentation and snippets, not run).

**Follow-ups:**
- "How would you break the cycle?" Pick the intended parent per cycle with the business, set one `manager_id` to NULL (or the right value), and rerun the checks; do not delete rows blindly.
- "How do you stop it happening?" A foreign key `manager_id` to `emp_id` removes orphans (not cycles or self-managed; a `CHECK (manager_id <> emp_id)` removes the self-managed rows), and a trigger or a load-time validation catches cycles.
- "Are two roots always wrong?" Not always (a holding structure, or a forest of trees); it is wrong only if the business says there is one CEO.

**Common mistakes:**
- `NOT IN` with a nullable column.
- Treating a NULL manager as an orphan.
- Running only a top-down query and concluding the data is clean because it returned no error.
- No step cap on the upward walk, so the check query itself never ends on the bad data it is meant to find.
- Counting roots with `COUNT(manager_id)`, which ignores NULLs and so counts non-roots.

### Q16 ⭐⭐ 🟡 Graph reachability and connected components: edges(a, b) lists undirected edges between nodes 1 to 9 forming three clusters and an isolated node listed in nodes(node_id). Return for every node its component id as the smallest node id it can reach, and the component sizes. Show the symmetric edge list, the reachability recursion with UNION to stop cycles, and MIN(reached) per start node as the component label. Explain why this is O(nodes x reachable) and not suitable for big graphs, and compare with networkx connected_components (installed in this environment, version stated in the answer) and a plain Python union-find.
**Asked at:** SQLite lang_with documentation (opened: compound SELECT with a non-recursive initial select, UNION discards rows already queued and stops cycles, UNION ALL needs little memory, LIMIT on the recursive select, ORDER BY in the recursive select as queue order for breadth-first or depth-first, no aggregates or windows in the recursive select, queue algorithm) plus PostgreSQL WITH queries documentation (opened: working table and intermediate table evaluation); official documentation, not candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Make the edge list symmetric, compute for every start node the set of nodes it can reach with a recursive CTE using plain `UNION` (so already-seen (start, node) pairs are dropped and cycles stop by themselves), and the component id of a node is the minimum node id it can reach; sizes are a count per component. It costs about the sum of component size squared, so it is a teaching and small-graph answer, not a big-graph one.

**Schema and sample data:** nine nodes, seven edge rows. Cluster {1,2,3} is a triangle and also contains a duplicate edge in the opposite direction ((1,2) and (2,1)). Cluster {4,5,6} is a chain. Cluster {7,8} is a pair. Node 9 is isolated: it is only in the `nodes` table (that is why the node list is needed; edges alone would never mention it).
```sql
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9);
CREATE TABLE edges(a INTEGER, b INTEGER);
INSERT INTO edges VALUES (1,2),(2,3),(1,3),(2,1),(4,5),(5,6),(7,8);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE e(src, dst) AS (
  SELECT a, b FROM edges
  UNION
  SELECT b, a FROM edges
), reach(start, node) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT r.start, e.dst FROM reach r JOIN e ON e.src = r.node
), label AS (
  SELECT start AS node_id, MIN(node) AS component FROM reach GROUP BY start
)
SELECT l.node_id, l.component,
       (SELECT COUNT(*) FROM label x WHERE x.component = l.component) AS component_size
FROM label l
ORDER BY l.node_id
```
How it works:
- `e` is the symmetric edge list; I used `UNION` (not `UNION ALL`) so the duplicate (1,2)/(2,1) pair collapses.
- `reach(start, node)` starts with every node reaching itself (that is what makes node 9 appear with itself as its only reached node) and follows edges. `UNION` discards a (start, node) pair that is already there, so the triangle cannot loop: the number of distinct pairs is finite and the queue empties.
- `label` takes `MIN(node)` per start: the smallest id in the component, the same for every member. The final select adds the component size as a count of nodes with the same label.
- The sizes table in the output is just a `GROUP BY component`.

**pandas answer:** label propagation with merges: start with each node labelled by itself, repeatedly set each node's label to the minimum label among itself and its neighbours until nothing changes (shown once, identical to the Code block):
```py
    sym = pd.concat([edges.rename(columns={"a": "src", "b": "dst"}),
                     edges.rename(columns={"b": "src", "a": "dst"})]).drop_duplicates()
    lab = nodes.rename(columns={"node_id": "node"}).assign(component=nodes["node_id"])
    while True:
        nb = sym.merge(lab, left_on="dst", right_on="node")[["src", "component"]]
        best = nb.groupby("src")["component"].min()
        new = pd.concat([lab["node"].map(best), lab["component"]], axis=1).min(axis=1).astype(int)
        if new.equals(lab["component"]):
            break
        lab = lab.assign(component=new)
    lab = lab.rename(columns={"node": "node_id"})
    lab["component_size"] = lab.groupby("component")["node_id"].transform("size")
    return lab.sort_values("node_id").reset_index(drop=True)
```

**Example:** by hand.
- Component 1: from node 1 you reach 1, 2, 3 (also back to 1, which is dropped by `UNION`); the minimum is 1. From 3 you reach 3, 1, 2; minimum 1. So nodes 1, 2, 3 are labelled 1 and the size is 3.
- Component 4: node 4 reaches 4, 5, 6; node 6 reaches 6, 5, 4; label 4, size 3. Component 7: label 7, size 2. Node 9 reaches only itself: label 9, size 1.
- Rows in `reach`: 3x3 + 3x3 + 2x2 + 1x1 = 23 (printed, equal to the sum of size squared).

**Code:** run with `python3 -I`. The asserts compare SQL, pandas, a plain Python union-find and networkx (all sorted by node id; the networkx components are mapped to their minimum id).
```python
# Q16: connected components: reachability recursion with UNION, MIN(reached) as the label; checks with union-find and networkx
import sqlite3
import pandas as pd
import networkx as nx

SCHEMA = """
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9);
CREATE TABLE edges(a INTEGER, b INTEGER);
INSERT INTO edges VALUES (1,2),(2,3),(1,3),(2,1),(4,5),(5,6),(7,8);
"""
SQL_MAIN = """
WITH RECURSIVE e(src, dst) AS (
  SELECT a, b FROM edges
  UNION
  SELECT b, a FROM edges
), reach(start, node) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT r.start, e.dst FROM reach r JOIN e ON e.src = r.node
), label AS (
  SELECT start AS node_id, MIN(node) AS component FROM reach GROUP BY start
)
SELECT l.node_id, l.component,
       (SELECT COUNT(*) FROM label x WHERE x.component = l.component) AS component_size
FROM label l
ORDER BY l.node_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
sizes = sql_df.groupby("component").size().rename("size").reset_index()
print("component sizes:")
print(sizes.to_string(index=False))
SQL_REACH_ROWS = """
WITH RECURSIVE e(src, dst) AS (SELECT a, b FROM edges UNION SELECT b, a FROM edges),
reach(start, node) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT r.start, e.dst FROM reach r JOIN e ON e.src = r.node
)
SELECT COUNT(*) FROM reach
"""
print("rows in reach (start, node) pairs:", con.execute(SQL_REACH_ROWS).fetchone()[0], "= sum of size squared:", int((sizes["size"] ** 2).sum()))

nodes = pd.read_sql_query("SELECT * FROM nodes", con)
edges = pd.read_sql_query("SELECT * FROM edges", con)

def components(nodes, edges):
    # pd:main
    sym = pd.concat([edges.rename(columns={"a": "src", "b": "dst"}),
                     edges.rename(columns={"b": "src", "a": "dst"})]).drop_duplicates()
    lab = nodes.rename(columns={"node_id": "node"}).assign(component=nodes["node_id"])
    while True:
        nb = sym.merge(lab, left_on="dst", right_on="node")[["src", "component"]]
        best = nb.groupby("src")["component"].min()
        new = pd.concat([lab["node"].map(best), lab["component"]], axis=1).min(axis=1).astype(int)
        if new.equals(lab["component"]):
            break
        lab = lab.assign(component=new)
    lab = lab.rename(columns={"node": "node_id"})
    lab["component_size"] = lab.groupby("component")["node_id"].transform("size")
    return lab.sort_values("node_id").reset_index(drop=True)
    # pd:end

pd_df = components(nodes, edges)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by node_id
print("pandas label propagation equal to SQL")

def union_find(nodes, edges):
    parent = {n: n for n in nodes["node_id"]}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in zip(edges["a"], edges["b"]):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    return {n: find(n) for n in parent}

uf = union_find(nodes, edges)
assert uf == dict(zip(sql_df["node_id"], sql_df["component"]))
G = nx.Graph()
G.add_nodes_from(nodes["node_id"])
G.add_edges_from(zip(edges["a"], edges["b"]))
nxc = {n: min(c) for c in nx.connected_components(G) for n in c}
assert nxc == uf
print("networkx", nx.__version__, "and union-find agree with SQL; networkx components:", sorted(sorted(c) for c in nx.connected_components(G)))

# cost: a chain of n nodes gives n*n reach rows
for n in (50, 100, 200):
    c = sqlite3.connect(":memory:")
    c.executescript("CREATE TABLE nodes(node_id INTEGER PRIMARY KEY); CREATE TABLE edges(a INTEGER, b INTEGER);")
    c.executemany("INSERT INTO nodes VALUES (?)", [(i,) for i in range(1, n + 1)])
    c.executemany("INSERT INTO edges VALUES (?, ?)", [(i, i + 1) for i in range(1, n)])
    rows = c.execute(SQL_REACH_ROWS).fetchone()[0]
    print(f"chain of {n} nodes: reach rows = {rows} (n squared = {n*n})")

# without UNION (UNION ALL) the walk never ends on this graph; capped by LIMIT
print("UNION ALL reach, stopped by LIMIT 500:", con.execute("""WITH RECURSIVE e(src,dst) AS (SELECT a,b FROM edges UNION SELECT b,a FROM edges),
  reach(start,node) AS (SELECT node_id,node_id FROM nodes UNION ALL SELECT r.start,e.dst FROM reach r JOIN e ON e.src=r.node LIMIT 500)
  SELECT COUNT(*) FROM reach""").fetchone()[0], "rows")
# edge to a node missing from nodes, and no edges at all
con.execute("INSERT INTO edges VALUES (9, 50)")
print("edge to unknown node 50: label of node 9 =", con.execute(SQL_MAIN.replace("ORDER BY l.node_id", "ORDER BY l.node_id")).fetchall()[8][1], "(50 is never a start, so it never gets its own row)")
con.execute("DELETE FROM edges")
print("no edges: components =", sorted(set(r[1] for r in con.execute(SQL_MAIN))), "(every node is its own component)")
print("asserts passed")
```

**Output (my run):**
```text
 node_id  component  component_size
       1          1               3
       2          1               3
       3          1               3
       4          4               3
       5          4               3
       6          4               3
       7          7               2
       8          7               2
       9          9               1
component sizes:
 component  size
         1     3
         4     3
         7     2
         9     1
rows in reach (start, node) pairs: 23 = sum of size squared: 23
pandas label propagation equal to SQL
networkx 3.6.1 and union-find agree with SQL; networkx components: [[1, 2, 3], [4, 5, 6], [7, 8], [9]]
chain of 50 nodes: reach rows = 2500 (n squared = 2500)
chain of 100 nodes: reach rows = 10000 (n squared = 10000)
chain of 200 nodes: reach rows = 40000 (n squared = 40000)
UNION ALL reach, stopped by LIMIT 500: 500 rows
edge to unknown node 50: label of node 9 = 9 (50 is never a start, so it never gets its own row)
no edges: components = [1, 2, 3, 4, 5, 6, 7, 8, 9] (every node is its own component)
asserts passed
```
The environment has networkx 3.6.1; scipy is not installed, so no `scipy.sparse.csgraph` here. `nx.connected_components` and `nx.Graph.add_nodes_from`/`add_edges_from` were called exactly as written in the Code block.

**Edge cases:**
- Isolated node: only the `nodes` table gives it a row; derive nodes from the edge list and it disappears.
- Duplicate or reversed edges: harmless with `UNION`; with `UNION ALL` they would multiply rows (and, on a cycle, never end; the Code block shows the unguarded `UNION ALL` run, stopped at 500 rows by a `LIMIT`).
- Self-loop edge (a = b): harmless.
- Edge to a node missing from `nodes` (I inserted (9, 50)): node 9 now reaches 50 internally but 50 is never a start, so it gets no row of its own; the label of 9 stays 9. Clean the data or add endpoints to the node list with a `UNION`.
- No edges at all: every node is its own component (printed).
- Directed edges would need a different definition (strongly connected components), not covered by this query.

**Then explain:**
- Why `UNION` works here: the row is just (start, node), and there are at most nodes x nodes of those; a pair already produced is not produced again, so every cycle is cut.
- Cost: O(nodes x reachable). A chain of 50, 100 and 200 nodes produced exactly 2500, 10000 and 40000 reach rows (printed): quadratic growth in the component size. A component with a million nodes would need 10 to the power 12 rows, which is why this is not a big-graph tool. Real systems use union-find (near linear) or a library.
- Plain Python union-find: keep a parent map, `find` with path compression, `union` by the smaller root; one pass over the edges. It is the interview-friendly alternative, and it scales.
- networkx `connected_components` (checked here, version 3.6.1) returns one set of nodes per component (I believe it is a breadth-first search inside; I did not check the source); the label is `min(component)`.
- Other engines (not executed here): PostgreSQL 14+ could add `CYCLE`, but the `UNION` form works unchanged; MySQL 8 and SQL Server accept the same shape (SQL Server without the word `RECURSIVE`, and its `UNION` in the recursive member is not allowed there: SQL Server requires `UNION ALL` between anchor and recursive member, so the dedup approach needs a path or depth guard instead; stated from memory, not executed).

**Follow-ups:**
- "Why not just iterate label = min(neighbour labels) in SQL?" That needs repeated updates or a recursive member with an aggregate, which is not allowed; the pandas loop does it because it re-runs the merge each round.
- "How many rounds does the pandas loop need?" Up to the diameter of the largest component (a chain of n nodes needs about n rounds with the minimum at one end).
- "Which edges connect two components?" Edges whose endpoints have different labels; after a labelling there are none (printed sizes show three clusters plus the isolated node).

**Common mistakes:**
- Forgetting the symmetric edges, so labels depend on edge direction.
- Using `UNION ALL` and no guard.
- Dropping isolated nodes by building the node list from edges.
- Taking `MIN(reached)` without the self row (a node with no edges then has no label).
- Believing the query scales; it enumerates every reachable pair.

### Q17 ⭐⭐ 🟡 Flight routes with connections and total cost: flights(src, dst, cost). Return every route from 'DEL' to 'BLR' with at most 3 legs, the list of stops, the number of legs and the total cost, then the cheapest and the fewest-legs route. Guard against revisiting an airport with a path string, explain why the cost is added row by row in the recursive member and aggregated outside, and what changes if two flights exist between the same pair of cities (parallel edges multiply the number of routes). State the number of routes as the graph grows to show the combinatorial growth.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Walk out from 'DEL' with a recursive CTE that carries the current city, the number of legs, the running cost and the path string, add each flight's cost in the recursive member, refuse a flight to an airport already in the path, stop at 3 legs, keep the rows that end in 'BLR', and pick the cheapest and the fewest-legs route outside the recursion.

**Schema and sample data:** ten flight rows. There are two different DEL to BOM flights (100 and 90, parallel edges), a loop between BOM and HYD (BOM to HYD 50, HYD to BOM 40), and return flights to DEL (BLR to DEL 250, BOM to DEL 95) that would create cycles back to the origin.
```sql
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BLR',300),('DEL','BOM',100),('DEL','BOM',90),('DEL','HYD',80),
 ('BOM','BLR',120),('BOM','HYD',50),('HYD','BLR',90),('HYD','BOM',40),
 ('BLR','DEL',250),('BOM','DEL',95);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE walk(city, legs, cost, path) AS (
  SELECT 'DEL', 0, 0, 'DEL'
  UNION ALL
  SELECT f.dst, w.legs + 1, w.cost + f.cost, w.path || '>' || f.dst
  FROM walk w JOIN flights f ON f.src = w.city
  WHERE w.city <> 'BLR'
    AND w.legs < 3
    AND ('>' || w.path || '>') NOT LIKE '%>' || f.dst || '>%'
), routes AS (
  SELECT path AS stops, legs, cost FROM walk WHERE city = 'BLR'
)
SELECT stops, legs, cost,
       CASE WHEN cost = MIN(cost) OVER () THEN 1 ELSE 0 END AS is_cheapest,
       CASE WHEN ROW_NUMBER() OVER (ORDER BY legs, cost, stops) = 1 THEN 1 ELSE 0 END AS is_fewest_legs
FROM routes
ORDER BY cost, legs, stops
```
How it works:
- The anchor is the origin with 0 legs and 0 cost. Each step joins the current city to the flights that leave it and adds 1 leg and that flight's cost.
- The guard is `('>' || path || '>') NOT LIKE '%>' || dst || '>%'`: the path is wrapped in delimiters so a city is matched as a whole token ('>BOM>'). Airport codes here are all 3 letters, but the delimiters make the check right for any names. The `legs < 3` condition is a second guard and also the business limit.
- `w.city <> 'BLR'` stops a route once it has arrived, so routes that pass through BLR and come back are not built.
- The cost is added row by row because each row is one route prefix; a total only exists for a finished route. The aggregation (`MIN(cost)`, the ranks) happens outside, where aggregates and window functions are allowed. The recursive member itself cannot contain them.
- `is_cheapest` marks the minimum cost route; `is_fewest_legs` is the first route when ordered by legs, then cost (ties on legs go to the cheaper route).

**pandas answer:** one merge per leg on a frontier frame, with the same path check (shown once, identical to the Code block):
```py
    done, frontier = [], pd.DataFrame({"city": [src], "legs": [0], "cost": [0], "path": [src]})
    for _ in range(max_legs):
        frontier = frontier[frontier["city"] != dst]
        nxt = frontier.merge(flights, left_on="city", right_on="src")
        nxt = nxt[[f">{p}>".find(f">{d}>") < 0 for p, d in zip(nxt["path"], nxt["dst"])]]
        frontier = pd.DataFrame({"city": nxt["dst"], "legs": nxt["legs"] + 1,
                                 "cost": nxt["cost_x"] + nxt["cost_y"], "path": nxt["path"] + ">" + nxt["dst"]})
        done.append(frontier[frontier["city"] == dst])
    out = pd.concat(done).rename(columns={"path": "stops"})[["stops", "legs", "cost"]]
    out = out.sort_values(["cost", "legs", "stops"]).reset_index(drop=True)
    out["is_cheapest"] = (out["cost"] == out["cost"].min()).astype(int)
    out["is_fewest_legs"] = (out.index == out.sort_values(["legs", "cost", "stops"]).index[0]).astype(int)
    return out
```

**Example:** by hand, from DEL.
- 1 leg: DEL to BLR 300, a route; DEL to BOM (100 or 90), DEL to HYD 80 continue.
- 2 legs: BOM to BLR gives 220 (via the 100 flight) and 210 (via the 90 flight); HYD to BLR gives 170. BOM to HYD and HYD to BOM continue. BOM to DEL is blocked by the guard (DEL is in the path).
- 3 legs: DEL > BOM > HYD > BLR is 100 + 50 + 90 = 240 and 90 + 50 + 90 = 230; DEL > HYD > BOM > BLR is 80 + 40 + 120 = 240.
- Seven routes in all (five distinct stop lists, because of the parallel flight). Cheapest: DEL > HYD > BLR at 170. Fewest legs: DEL > BLR, one leg, 300.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after sorting by `cost, legs, stops`. The Code block also prints the no-guard run, a NULL cost, the growth in the number of routes, and the empty case.
```python
# Q17: flight routes with connections: path guard, cost added in the recursive member, aggregated outside
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BLR',300),('DEL','BOM',100),('DEL','BOM',90),('DEL','HYD',80),
 ('BOM','BLR',120),('BOM','HYD',50),('HYD','BLR',90),('HYD','BOM',40),
 ('BLR','DEL',250),('BOM','DEL',95);
"""
SQL_MAIN = """
WITH RECURSIVE walk(city, legs, cost, path) AS (
  SELECT 'DEL', 0, 0, 'DEL'
  UNION ALL
  SELECT f.dst, w.legs + 1, w.cost + f.cost, w.path || '>' || f.dst
  FROM walk w JOIN flights f ON f.src = w.city
  WHERE w.city <> 'BLR'
    AND w.legs < 3
    AND ('>' || w.path || '>') NOT LIKE '%>' || f.dst || '>%'
), routes AS (
  SELECT path AS stops, legs, cost FROM walk WHERE city = 'BLR'
)
SELECT stops, legs, cost,
       CASE WHEN cost = MIN(cost) OVER () THEN 1 ELSE 0 END AS is_cheapest,
       CASE WHEN ROW_NUMBER() OVER (ORDER BY legs, cost, stops) = 1 THEN 1 ELSE 0 END AS is_fewest_legs
FROM routes
ORDER BY cost, legs, stops
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("routes:", len(sql_df), "| distinct stop lists:", sql_df["stops"].nunique(), "(parallel DEL-BOM flights make two routes with the same stops)")

flights = pd.read_sql_query("SELECT * FROM flights", con)

def routes(flights, src="DEL", dst="BLR", max_legs=3):
    # pd:main
    done, frontier = [], pd.DataFrame({"city": [src], "legs": [0], "cost": [0], "path": [src]})
    for _ in range(max_legs):
        frontier = frontier[frontier["city"] != dst]
        nxt = frontier.merge(flights, left_on="city", right_on="src")
        nxt = nxt[[f">{p}>".find(f">{d}>") < 0 for p, d in zip(nxt["path"], nxt["dst"])]]
        frontier = pd.DataFrame({"city": nxt["dst"], "legs": nxt["legs"] + 1,
                                 "cost": nxt["cost_x"] + nxt["cost_y"], "path": nxt["path"] + ">" + nxt["dst"]})
        done.append(frontier[frontier["city"] == dst])
    out = pd.concat(done).rename(columns={"path": "stops"})[["stops", "legs", "cost"]]
    out = out.sort_values(["cost", "legs", "stops"]).reset_index(drop=True)
    out["is_cheapest"] = (out["cost"] == out["cost"].min()).astype(int)
    out["is_fewest_legs"] = (out.index == out.sort_values(["legs", "cost", "stops"]).index[0]).astype(int)
    return out
    # pd:end

pd_df = routes(flights)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by cost, legs, stops
print("pandas frontier merge equal to SQL")

# without the path guard: the loop DEL > BOM > DEL > ... is walked until the leg cap; remove the leg cap too and it never ends
noguard = SQL_MAIN.replace("    AND ('>' || w.path || '>') NOT LIKE '%>' || f.dst || '>%'\n", "")
assert noguard != SQL_MAIN
print("no path guard, leg cap 3:", len(pd.read_sql_query(noguard, con)), "routes (vs", len(sql_df), "with the guard; the extras revisit an airport)")
nocap = noguard.replace("    AND w.legs < 3\n", "").replace("), routes AS", "  LIMIT 5000\n), routes AS")
print("no guard and no leg cap, stopped by LIMIT 5000:", len(pd.read_sql_query(nocap, con)), "routes found so far (it would never end)")

# NULL cost: the whole route cost becomes NULL
con.execute("UPDATE flights SET cost = NULL WHERE src = 'HYD' AND dst = 'BLR'")
nul = pd.read_sql_query(SQL_MAIN, con)
print("with HYD-BLR cost NULL: routes with NULL cost =", int(nul["cost"].isna().sum()), "| cheapest flag set on", int(nul["is_cheapest"].sum()), "rows")
con.execute("UPDATE flights SET cost = 90 WHERE src = 'HYD' AND dst = 'BLR'")

# combinatorial growth: layered graph, 3 airports per layer, every airport connects to all 3 in the next layer
def count_layered(width, layers, parallel=1):
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE fl(src TEXT, dst TEXT, cost INTEGER)")
    rows = [("S", f"L1_{j}", 1) for j in range(width)]
    for k in range(1, layers):
        rows += [(f"L{k}_{i}", f"L{k+1}_{j}", 1) for i in range(width) for j in range(width)]
    rows += [(f"L{layers}_{i}", "T", 1) for i in range(width)]
    c.executemany("INSERT INTO fl VALUES (?, ?, ?)", rows * parallel)
    return c.execute("""WITH RECURSIVE w(city, legs) AS (SELECT 'S', 0 UNION ALL SELECT f.dst, w.legs + 1 FROM w JOIN fl f ON f.src = w.city)
                        SELECT COUNT(*) FROM w WHERE city = 'T'""").fetchone()[0]
print("routes S to T, 3 airports per layer:", {k: count_layered(3, k) for k in (1, 2, 3, 4, 5, 6, 7, 8)})
print("same, every flight offered twice (parallel edges):", {k: count_layered(3, k, 2) for k in (1, 2, 3, 4, 5, 6)})
print("empty flights table ->", len(pd.read_sql_query(SQL_MAIN.replace("FROM walk w JOIN flights f", "FROM walk w JOIN (SELECT * FROM flights WHERE 1 = 0) f"), con)), "routes")
print("asserts passed")
```

**Output (my run):**
```text
          stops  legs  cost  is_cheapest  is_fewest_legs
    DEL>HYD>BLR     2   170            1               0
    DEL>BOM>BLR     2   210            0               0
    DEL>BOM>BLR     2   220            0               0
DEL>BOM>HYD>BLR     3   230            0               0
DEL>BOM>HYD>BLR     3   240            0               0
DEL>HYD>BOM>BLR     3   240            0               0
        DEL>BLR     1   300            0               1
routes: 7 | distinct stop lists: 5 (parallel DEL-BOM flights make two routes with the same stops)
pandas frontier merge equal to SQL
no path guard, leg cap 3: 9 routes (vs 7 with the guard; the extras revisit an airport)
no guard and no leg cap, stopped by LIMIT 5000: 1733 routes found so far (it would never end)
with HYD-BLR cost NULL: routes with NULL cost = 3 | cheapest flag set on 1 rows
routes S to T, 3 airports per layer: {1: 3, 2: 9, 3: 27, 4: 81, 5: 243, 6: 729, 7: 2187, 8: 6561}
same, every flight offered twice (parallel edges): {1: 12, 2: 72, 3: 432, 4: 2592, 5: 15552, 6: 93312}
empty flights table -> 0 routes
asserts passed
```
Honest notes from the run:
- Without the path guard but with the 3-leg cap the query still ends but returns 9 routes: two extras (DEL > BOM > DEL > BLR, once per parallel flight) go back through the origin. The leg cap alone is enough to terminate but not enough to be correct.
- Without the guard and without the cap, the demo only stopped at the 5000-row `LIMIT` (it had found 1733 arrivals by then); it would not terminate on its own.
- The route count grows multiplicatively: with 3 airports per layer and every airport connected to all 3 in the next layer, the number of routes from S to T is 3, 9, 27, 81, 243, 729, 2187, 6561 for 1 to 8 layers (3 to the power of the layers). If every flight is offered twice (parallel edges) the counts are 12, 72, 432, 2592, 15552, 93312: each parallel pair multiplies the routes again.

**Edge cases:**
- Parallel flights between the same cities produce separate routes with the same stops (here DEL > BOM > BLR at 210 and 220). If the question is "the cheapest per stop list", take `MIN(cost)` per stops; or collapse parallel edges to their cheapest flight before the walk.
- NULL cost: the route total becomes NULL (printed: 3 routes), `MIN` and the comparison ignore it, and in SQLite a NULL sorts first in an ascending `ORDER BY`, so a NULL-cost route would appear at the top of the list. Filter or `COALESCE` the costs first.
- No route (no path from the origin to the destination within the legs): empty result; empty flights table: empty result (printed).
- Ties for cheapest: `is_cheapest` flags all tied routes; `is_fewest_legs` flags exactly one (the tie-break is cost, then the stop list).
- Return flights (BLR to DEL) are blocked by the guard; round trips are a different question.

**Then explain:**
- Why add cost in the recursive member: the recursive member only sees the previous row, so the only way to know the total so far is to carry it. Totals by route are then plain columns; the best route is a `MIN` outside.
- Why the guard is by path and not by `UNION`: the rows are made unique by `legs`, `cost` and `path`, so `UNION` would remove nothing and would not stop a cycle (Q7). The path string, or a leg cap, is what terminates it.
- Combinatorics: the work is the number of routes, not the number of flights, which is why airline-style problems need a leg cap and usually a different algorithm (Dijkstra, Q23) once graphs grow.
- Other engines (not executed here): PostgreSQL commonly uses an array of visited airports (`path || dst`, `dst <> ALL(path)`) or the 14+ `CYCLE` clause; MySQL 8 and SQL Server take the same shape with their own concatenation and recursion limits (`cte_max_recursion_depth`, `MAXRECURSION`); Oracle would use `CONNECT BY NOCYCLE` with `SYS_CONNECT_BY_PATH`.

**Follow-ups:**
- "Cheapest route with any number of legs?" Remove the leg cap, keep the path guard, and accept the exponential cost; for a real network use a shortest-path algorithm outside SQL.
- "Layover time or departure times?" Add the arrival time to the row and join on `dep_time >= arr_time + layover`; the guard stays.
- "How many routes are there?" `COUNT(*)` over the routes: 7 here.

**Common mistakes:**
- Putting `MIN(cost)` or `SUM(cost)` inside the recursive member (not allowed) instead of carrying the running cost.
- No guard against revisiting an airport, so routes through the origin appear.
- Matching the path with a bare `LIKE '%BOM%'` when names can be substrings of each other.
- Forgetting that parallel flights are separate routes.
- Not stopping at the destination, so routes continue through it.

### Q18 ⭐⭐ 🟡 Compound interest and loan amortisation schedule: accounts(acct_id, balance, annual_rate) and loans(loan_id, principal, annual_rate, months). (a) Grow each account balance monthly for 12 months with a recursive CTE and compare with the closed form balance * (1 + r/12)^n, (b) build the full amortisation schedule for a 10000 loan at 12 percent annual over 6 months (month, opening balance, interest, principal paid, closing balance, constant EMI computed in the query with power or a documented workaround), with the last-row rounding fix. Explain why rounding each month differs from the closed form by a few paise, that SQLite has power and exp here only when math functions are compiled in (hedge for other engines), and the pandas loop check with asserts.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Compound interest and amortisation are state carried month to month, so the recursive CTE carries the opening balance and each month's row is derived from it; the closed form `balance * (1 + r/12)^n` is the check, it differs from the month-by-month answer by a few paise only because the schedule rounds to 2 decimals every month; and the last payment must be adjusted (pay off the remaining balance) so the loan ends at exactly zero.

**Schema and sample data:** five accounts (one with a 0 rate, one with a NULL rate) and three loans: 10000 at 12 percent for 6 months (the question's loan), 5000 at 0 percent for 4 months (the zero-rate trap) and 1200 at 18 percent for 1 month (a one-row schedule). Rates are stored as decimals (0.12 = 12 percent a year, so the monthly rate is annual_rate / 12).
```sql
CREATE TABLE accounts(acct_id INTEGER PRIMARY KEY, balance REAL, annual_rate REAL);
INSERT INTO accounts VALUES (1,1000,0.12),(2,2500,0.075),(3,100.55,0.06),(4,800,0.0),(5,500,NULL);
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal REAL, annual_rate REAL, months INTEGER);
INSERT INTO loans VALUES (1,10000,0.12,6),(2,5000,0.0,4),(3,1200,0.18,1);
```

**SQL answer:** two queries. Part (a), `SQL_GROWTH` in the Code block: the recursive CTE grows each balance for 12 months, rounding to 2 decimals each month, and compares month 12 with the closed form (`power`):
```sql
WITH RECURSIVE g(acct_id, month, bal) AS (
  SELECT acct_id, 0, balance FROM accounts
  UNION ALL
  SELECT g.acct_id, g.month + 1, ROUND(g.bal * (1 + a.annual_rate / 12.0), 2)
  FROM g JOIN accounts a ON a.acct_id = g.acct_id
  WHERE g.month < 12
)
SELECT g.acct_id, g.bal AS monthly_rounded,
       ROUND(a.balance * power(1 + a.annual_rate / 12.0, 12), 2) AS closed_form,
       ROUND(g.bal - a.balance * power(1 + a.annual_rate / 12.0, 12), 4) AS difference
FROM g JOIN accounts a ON a.acct_id = g.acct_id
WHERE g.month = 12
ORDER BY g.acct_id
```
Part (b), `SQL_MAIN` in the Code block, the amortisation schedule:
```sql
WITH RECURSIVE l AS (
  SELECT loan_id, principal, months, annual_rate / 12.0 AS r,
         CASE WHEN annual_rate = 0 THEN ROUND(principal / months, 2)
              ELSE ROUND(principal * (annual_rate / 12.0) * power(1 + annual_rate / 12.0, months)
                         / (power(1 + annual_rate / 12.0, months) - 1), 2) END AS emi
  FROM loans
), s(loan_id, month, opening) AS (
  SELECT loan_id, 1, principal FROM l
  UNION ALL
  SELECT s.loan_id, s.month + 1,
         ROUND(s.opening - CASE WHEN s.month = l.months THEN s.opening
                                ELSE l.emi - ROUND(s.opening * l.r, 2) END, 2)
  FROM s JOIN l ON l.loan_id = s.loan_id
  WHERE s.month < l.months
), x AS (
  SELECT s.loan_id, s.month, s.opening, l.emi,
         ROUND(s.opening * l.r, 2) AS interest,
         CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END AS principal_paid
  FROM s JOIN l ON l.loan_id = s.loan_id
)
SELECT loan_id, month, opening, interest, ROUND(principal_paid, 2) AS principal_paid,
       ROUND(interest + principal_paid, 2) AS payment,
       ROUND(opening - principal_paid, 2) AS closing
FROM x
ORDER BY loan_id, month
```
How it works:
- `l` computes the constant EMI once per loan: `P * r * (1+r)^n / ((1+r)^n - 1)`, rounded to 2 decimals, with a `CASE` for a zero rate, where that formula divides by zero (it gives NULL in SQLite, printed in the run) and the EMI is just `principal / months`.
- The recursion carries only the opening balance (loan, month, opening). Each step computes the next opening as `opening - principal_paid`, where the principal paid is the EMI minus that month's interest, except in the last month, where it is the whole remaining balance. That `CASE` is the last-row rounding fix: the last payment is `interest + remaining balance`, a few paise different from the EMI.
- Interest, principal paid, payment and closing balance are derived from the opening balance in the outer select `x` (a column alias cannot be reused in the same select list, so I keep the carried state small).
- No cycle is possible (`month` only rises) and `WHERE s.month < l.months` ends each loan.

**pandas answer:** a plain Python/pandas loop with the same rounding rule (shown once, identical to the Code block). `r2` is the half-up rounding helper defined in the Code block, because SQLite's `ROUND` rounds halves away from zero while Python's built-in `round` and numpy/pandas round halves to even:
```py
    grow = accounts.assign(bal=accounts["balance"])
    for _ in range(12):
        grow["bal"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0)) for b, rt in zip(grow["bal"], grow["annual_rate"])]
    grow["closed_form"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0) ** 12) for b, rt in zip(grow["balance"], grow["annual_rate"])]
    rows = []
    for ln in loans.itertuples():
        r = ln.annual_rate / 12.0
        emi = r2(ln.principal / ln.months) if ln.annual_rate == 0 else r2(ln.principal * r * (1 + r) ** ln.months / ((1 + r) ** ln.months - 1))
        opening = ln.principal
        for m in range(1, ln.months + 1):
            interest = r2(opening * r)
            paid = opening if m == ln.months else emi - interest
            rows.append((ln.loan_id, m, opening, interest, r2(paid), r2(interest + paid), r2(opening - paid)))
            opening = r2(opening - paid)
    sch = pd.DataFrame(rows, columns=["loan_id", "month", "opening", "interest", "principal_paid", "payment", "closing"])
    return grow, sch
```

**Example:** the 10000 loan at 1 percent a month for 6 months.
- EMI = 10000 x 0.01 x 1.01^6 / (1.01^6 - 1) = 1725.48 (rounded).
- Month 1: interest 100.00, principal 1725.48 - 100.00 = 1625.48, closing 8374.52. Month 2: interest 83.75, principal 1641.73, closing 6732.79. And so on to month 5 closing 1708.43.
- Month 6: interest 17.08. Normal payment would repay 1725.48 - 17.08 = 1708.40 of principal, leaving 0.03 owing. The fix pays the whole 1708.43, so the last payment is 1725.51 and the closing balance is 0.00. Without the fix the final closing is 0.03 (printed).
- Total interest 352.91 and total paid 10352.91 (printed).
- Account 1: 1000 at 1 percent a month: closed form 1000 x 1.01^12 = 1126.8250, rounded 1126.83; monthly rounding gives 1126.84, a difference of 1 paisa.

**Code:** run with `python3 -I`. Asserts: pandas/Python growth and schedule equal the SQL results (rounded to 2 decimals, compared after sorting by loan and month), principal paid sums to the loan amount, and every final closing balance is 0.
```python
# Q18: compound interest and loan amortisation with recursive CTEs, checked against the closed form and a Python loop
import sqlite3
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd

SCHEMA = """
CREATE TABLE accounts(acct_id INTEGER PRIMARY KEY, balance REAL, annual_rate REAL);
INSERT INTO accounts VALUES (1,1000,0.12),(2,2500,0.075),(3,100.55,0.06),(4,800,0.0),(5,500,NULL);
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal REAL, annual_rate REAL, months INTEGER);
INSERT INTO loans VALUES (1,10000,0.12,6),(2,5000,0.0,4),(3,1200,0.18,1);
"""
SQL_GROWTH = """
WITH RECURSIVE g(acct_id, month, bal) AS (
  SELECT acct_id, 0, balance FROM accounts
  UNION ALL
  SELECT g.acct_id, g.month + 1, ROUND(g.bal * (1 + a.annual_rate / 12.0), 2)
  FROM g JOIN accounts a ON a.acct_id = g.acct_id
  WHERE g.month < 12
)
SELECT g.acct_id, g.bal AS monthly_rounded,
       ROUND(a.balance * power(1 + a.annual_rate / 12.0, 12), 2) AS closed_form,
       ROUND(g.bal - a.balance * power(1 + a.annual_rate / 12.0, 12), 4) AS difference
FROM g JOIN accounts a ON a.acct_id = g.acct_id
WHERE g.month = 12
ORDER BY g.acct_id
"""
SQL_MAIN = """
WITH RECURSIVE l AS (
  SELECT loan_id, principal, months, annual_rate / 12.0 AS r,
         CASE WHEN annual_rate = 0 THEN ROUND(principal / months, 2)
              ELSE ROUND(principal * (annual_rate / 12.0) * power(1 + annual_rate / 12.0, months)
                         / (power(1 + annual_rate / 12.0, months) - 1), 2) END AS emi
  FROM loans
), s(loan_id, month, opening) AS (
  SELECT loan_id, 1, principal FROM l
  UNION ALL
  SELECT s.loan_id, s.month + 1,
         ROUND(s.opening - CASE WHEN s.month = l.months THEN s.opening
                                ELSE l.emi - ROUND(s.opening * l.r, 2) END, 2)
  FROM s JOIN l ON l.loan_id = s.loan_id
  WHERE s.month < l.months
), x AS (
  SELECT s.loan_id, s.month, s.opening, l.emi,
         ROUND(s.opening * l.r, 2) AS interest,
         CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END AS principal_paid
  FROM s JOIN l ON l.loan_id = s.loan_id
)
SELECT loan_id, month, opening, interest, ROUND(principal_paid, 2) AS principal_paid,
       ROUND(interest + principal_paid, 2) AS payment,
       ROUND(opening - principal_paid, 2) AS closing
FROM x
ORDER BY loan_id, month
"""
SQL_NOFIX = SQL_MAIN.replace("CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END", "l.emi - ROUND(s.opening * l.r, 2)")
assert SQL_NOFIX != SQL_MAIN
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
g = pd.read_sql_query(SQL_GROWTH, con)
print("(a) 12 months of monthly compounding, rounded to 2 decimals each month, versus the closed form:")
print(g.to_string(index=False))
sched = pd.read_sql_query(SQL_MAIN, con)
print("(b) amortisation schedules (loan 1 is 10000 at 12 percent for 6 months):")
print(sched.to_string(index=False))
print("EMI per loan:", dict(con.execute("SELECT loan_id, ROUND(principal*(annual_rate/12.0)*power(1+annual_rate/12.0,months)/(power(1+annual_rate/12.0,months)-1),2) FROM loans WHERE annual_rate > 0").fetchall()))
nofix = pd.read_sql_query(SQL_NOFIX, con)
print("without the last-row fix, closing balance after the last month:", nofix.groupby("loan_id")["closing"].last().to_dict())
print("with the fix:", sched.groupby("loan_id")["closing"].last().to_dict())

accounts = pd.read_sql_query("SELECT * FROM accounts", con)
loans = pd.read_sql_query("SELECT * FROM loans", con)

def r2(x):
    return float(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def pandas_side(accounts, loans):
    # pd:main
    grow = accounts.assign(bal=accounts["balance"])
    for _ in range(12):
        grow["bal"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0)) for b, rt in zip(grow["bal"], grow["annual_rate"])]
    grow["closed_form"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0) ** 12) for b, rt in zip(grow["balance"], grow["annual_rate"])]
    rows = []
    for ln in loans.itertuples():
        r = ln.annual_rate / 12.0
        emi = r2(ln.principal / ln.months) if ln.annual_rate == 0 else r2(ln.principal * r * (1 + r) ** ln.months / ((1 + r) ** ln.months - 1))
        opening = ln.principal
        for m in range(1, ln.months + 1):
            interest = r2(opening * r)
            paid = opening if m == ln.months else emi - interest
            rows.append((ln.loan_id, m, opening, interest, r2(paid), r2(interest + paid), r2(opening - paid)))
            opening = r2(opening - paid)
    sch = pd.DataFrame(rows, columns=["loan_id", "month", "opening", "interest", "principal_paid", "payment", "closing"])
    return grow, sch
    # pd:end

grow, sch = pandas_side(accounts, loans)
cmp_g = grow[grow["annual_rate"].notna()][["acct_id", "bal", "closed_form"]].reset_index(drop=True)
g_ok = g[g["monthly_rounded"].notna()].reset_index(drop=True)
assert (cmp_g["bal"].round(2).to_numpy() == g_ok["monthly_rounded"].round(2).to_numpy()).all()
assert (cmp_g["closed_form"].round(2).to_numpy() == g_ok["closed_form"].round(2).to_numpy()).all()
print("pandas/Python growth loop equals SQL (rounded balance and closed form) for the 4 accounts with a rate; account 5 (NULL rate) stays NULL in SQL:", g.loc[g.acct_id == 5, "monthly_rounded"].isna().all())
pd.testing.assert_frame_equal(sch.round(2), sched.round(2), check_dtype=False)   # compared after sorting by loan_id, month
assert abs(sched.groupby("loan_id")["principal_paid"].sum().round(2) - loans.set_index("loan_id")["principal"]).max() < 1e-6
assert (sched.groupby("loan_id")["closing"].last() == 0).all()
print("pandas schedule equal to SQL; principal paid sums to the loan amount; last closing balance is 0")
print("total interest on loan 1:", round(sched[sched.loan_id == 1]["interest"].sum(), 2), "| total paid:", round(sched[sched.loan_id == 1]["payment"].sum(), 2))
print("zero-rate formula without the CASE:", con.execute("SELECT 5000 * 0 * power(1, 4) / (power(1, 4) - 1)").fetchone(), "(division by zero gives NULL in SQLite)")
print("exp/ln check of power(): ", con.execute("SELECT ROUND(power(1.01, 12), 10), ROUND(exp(12 * ln(1.01)), 10)").fetchone())
print("asserts passed")
```

**Output (my run):**
```text
(a) 12 months of monthly compounding, rounded to 2 decimals each month, versus the closed form:
 acct_id  monthly_rounded  closed_form  difference
       1          1126.84      1126.83      0.0150
       2          2694.08      2694.08     -0.0015
       3           106.76       106.75      0.0083
       4           800.00       800.00      0.0000
       5              NaN          NaN         NaN
(b) amortisation schedules (loan 1 is 10000 at 12 percent for 6 months):
 loan_id  month  opening  interest  principal_paid  payment  closing
       1      1 10000.00    100.00         1625.48  1725.48  8374.52
       1      2  8374.52     83.75         1641.73  1725.48  6732.79
       1      3  6732.79     67.33         1658.15  1725.48  5074.64
       1      4  5074.64     50.75         1674.73  1725.48  3399.91
       1      5  3399.91     34.00         1691.48  1725.48  1708.43
       1      6  1708.43     17.08         1708.43  1725.51     0.00
       2      1  5000.00      0.00         1250.00  1250.00  3750.00
       2      2  3750.00      0.00         1250.00  1250.00  2500.00
       2      3  2500.00      0.00         1250.00  1250.00  1250.00
       2      4  1250.00      0.00         1250.00  1250.00     0.00
       3      1  1200.00     18.00         1200.00  1218.00     0.00
EMI per loan: {1: 1725.48, 3: 1218.0}
without the last-row fix, closing balance after the last month: {1: 0.03, 2: 0.0, 3: 0.0}
with the fix: {1: 0.0, 2: 0.0, 3: 0.0}
pandas/Python growth loop equals SQL (rounded balance and closed form) for the 4 accounts with a rate; account 5 (NULL rate) stays NULL in SQL: True
pandas schedule equal to SQL; principal paid sums to the loan amount; last closing balance is 0
total interest on loan 1: 352.91 | total paid: 10352.91
zero-rate formula without the CASE: (None,) (division by zero gives NULL in SQLite)
exp/ln check of power():  (1.1268250301, 1.1268250301)
asserts passed
```
Honest notes from the run:
- The month-by-month balance and the closed form disagree on two of the four rated accounts by 1 paisa (1126.84 versus 1126.83, 106.76 versus 106.75) and agree after rounding on the other two (the unrounded difference column shows 0.015, -0.0015, 0.0083 and 0); it is rounding, not a bug.
- `power` and `exp`/`ln` worked in this SQLite 3.45.1 build (the math functions are compiled in here; I verified `power(1.01, 12)` equals `exp(12 * ln(1.01))` to 10 places). Other SQLite builds may not have them, and the other engines are described below as not executed.
- SQLite `ROUND` and Python round differ on exact halves (Part 8 lesson: 2.675 style cases), so I used a half-up helper in Python; on this data the two agreed everywhere.

**Edge cases:**
- Zero rate: the EMI formula divides by zero (NULL in SQLite; an error in most other engines, not executed here), so a `CASE` is required.
- NULL rate (account 5): every month's balance is NULL and the closed form is NULL; filter or `COALESCE(rate, 0)` according to the business rule.
- One-month loan: the anchor row is also the last row; the fix makes the payment `principal + interest` (1218.00).
- Rounding: rounding each month's interest to paise is what a real lender's statement does, so the schedule is the truth and the closed form is only a check.
- Months in the table are whole numbers. Annual percent versus decimal and day-count conventions (actual/365 versus 30/360) are assumptions; I stated the 1/12 rule.
- Negative or zero principal: not handled; add a check.

**Then explain:**
- Why recursion: the balance after month m depends on the rounded balance of month m-1, which depends on its own. Without rounding there is a closed form (a power), and a window function over a numbers table could produce it; with per-month rounding the state matters and recursion (or a loop) is the exact method.
- `power` is available in this build; the portable alternatives are `POW` or `POWER` in PostgreSQL, MySQL, SQL Server (`POWER`) and Oracle (`POWER`), and `exp(n * ln(1+r))` where only `exp` and `ln` exist. I did not run any of these (not executed).
- An integer-division trap: `annual_rate / 12` with integer columns would truncate; I divide by `12.0`.
- Money in a real system should use `DECIMAL`/`NUMERIC` (exact), not binary floats; SQLite has no true decimal type, so the toy uses `REAL` and rounds each step.

**Follow-ups:**
- "Add a prepayment in month 3?" Subtract it from the opening balance in the recursive step for that month; the later EMI would be recomputed or the term shortened.
- "Interest only for the first 2 months?" `CASE WHEN month <= 2` changes the principal paid to 0.
- "Why not just use the closed form for the balance after k months?" It is fine for an unrounded balance: `P(1+r)^k - EMI * ((1+r)^k - 1)/r`; the schedule gives the rounded figures the customer actually sees.

**Common mistakes:**
- Dividing by zero for a 0 percent loan.
- Letting the last row carry the normal EMI and leaving 0.03 owing (or overpaying).
- Integer division in the monthly rate.
- Rounding only at the end and then not reconciling with the statement.
- Forgetting the cap `month < months`, so the recursion keeps producing rows past the term.

### Q19 ⭐⭐ 🟡 Other state-dependent running calculations: daily_prices(day, close) and assets(asset_id, cost, life_years, rate). Compute (a) an exponentially weighted moving average s_t = a * x_t + (1 - a) * s_(t-1) with a = 0.3 using a recursive CTE, (b) a declining-balance depreciation schedule (book value times a fixed rate each year, floored at a salvage value), and (c) show with a short argument why neither is a plain window function. Verify (a) with pandas ewm(alpha=0.3, adjust=False).mean() and assert equality, and note the rounding and first-row (seed) conventions that make a result differ by the adjust parameter.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Both are "this period's value depends on last period's value", so a recursive CTE carries the previous value; but a premise check first: neither is strictly impossible as a non-recursive query (EWMA has a weighted-sum closed form that overflows on long series, and the floored declining balance is just `MAX(salvage, cost * (1 - rate)^year)`), what is true is that no built-in window function does either one, and the recursion is the transparent, numerically safe way.

**Schema and sample data:** ten daily closes (03-09 and 03-10 are missing from the calendar; the series is treated by row, not by calendar day) and three assets. The question's `assets` table lists cost, life_years and rate and a floor "at a salvage value", so I added a `salvage` column to hold it.
```sql
CREATE TABLE daily_prices(day TEXT, close REAL);
INSERT INTO daily_prices VALUES
 ('2024-03-01',100),('2024-03-02',102),('2024-03-03',101),('2024-03-04',105),('2024-03-05',103),
 ('2024-03-06',108),('2024-03-07',110),('2024-03-08',107),('2024-03-11',111),('2024-03-12',115);
CREATE TABLE assets(asset_id INTEGER PRIMARY KEY, cost REAL, life_years INTEGER, rate REAL, salvage REAL);
INSERT INTO assets VALUES (1,10000,6,0.40,1000),(2,5000,3,0.25,500),(3,800,4,0.50,100);
```

**SQL answer:** (a) `SQL_MAIN` in the Code block, the EWMA with alpha 0.3:
```sql
WITH RECURSIVE p AS (
  SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices
), s(rn, day, close, ewma) AS (
  SELECT rn, day, close, close FROM p WHERE rn = 1
  UNION ALL
  SELECT p.rn, p.day, p.close, 0.3 * p.close + (1 - 0.3) * s.ewma
  FROM s JOIN p ON p.rn = s.rn + 1
)
SELECT day, close, ewma FROM s ORDER BY rn
```
The anchor is the first price (the seed: `s_1 = x_1`); each step is `0.3 * x_t + 0.7 * s_(t-1)`, joined to the next row number. (b) `SQL_DEPR` in the Code block, declining balance with the salvage floor; the book value is carried and `MAX(salvage, book * (1 - rate))` applies the floor; the depreciation of a year is the previous book value minus the new one (`LAG` is applied outside the recursion, which is allowed):
```sql
WITH RECURSIVE b(asset_id, year, book) AS (
  SELECT asset_id, 0, cost FROM assets
  UNION ALL
  SELECT b.asset_id, b.year + 1, MAX(a.salvage, b.book * (1 - a.rate))
  FROM b JOIN assets a ON a.asset_id = b.asset_id
  WHERE b.year < a.life_years
)
SELECT asset_id, year, ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year), 2) AS opening,
       ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year) - book, 2) AS depreciation,
       ROUND(book, 2) AS closing
FROM b
ORDER BY asset_id, year
```

**pandas answer:** `ewm` for (a) and a plain loop for (b) (shown once, identical to the Code block):
```py
    ewma = prices.sort_values("day")["close"].ewm(alpha=0.3, adjust=False).mean()
    rows = []
    for a in assets.itertuples():
        book = a.cost
        rows.append((a.asset_id, 0, np.nan, np.nan, book))
        for y in range(1, a.life_years + 1):
            new = max(a.salvage, book * (1 - a.rate))
            rows.append((a.asset_id, y, book, book - new, new))
            book = new
    depr = pd.DataFrame(rows, columns=["asset_id", "year", "opening", "depreciation", "closing"])
    return ewma, depr
```

**Example:** by hand.
- EWMA: s_1 = 100. s_2 = 0.3 x 102 + 0.7 x 100 = 100.6. s_3 = 0.3 x 101 + 0.7 x 100.6 = 100.72. s_4 = 0.3 x 105 + 0.7 x 100.72 = 102.004.
- Depreciation for asset 1 (cost 10000, 40 percent, floor 1000): book values 6000, 3600, 2160, 1296; the next would be 777.6, below the floor, so year 5 books 296.00 of depreciation to reach 1000 and year 6 books 0. Asset 3 (rate 50 percent, floor 100): 400, 200, 100, then 0.
- Asset 2 (25 percent): 3750, 2812.50, 2109.375; the year 3 depreciation is exactly 703.125, a rounding tie (see below).

**Code:** run with `python3 -I`. Asserts: pandas `ewm(alpha=0.3, adjust=False)` equals the recursive CTE to 1e-9; the Python depreciation loop equals the SQL schedule (compared after sorting by asset and year; SQLite `ROUND` rounds halves away from zero, so the pandas side uses a half-up helper); the closed forms equal the recursive results.
```python
# Q19: EWMA and declining-balance depreciation with recursive CTEs, checked against pandas ewm and closed forms
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE daily_prices(day TEXT, close REAL);
INSERT INTO daily_prices VALUES
 ('2024-03-01',100),('2024-03-02',102),('2024-03-03',101),('2024-03-04',105),('2024-03-05',103),
 ('2024-03-06',108),('2024-03-07',110),('2024-03-08',107),('2024-03-11',111),('2024-03-12',115);
CREATE TABLE assets(asset_id INTEGER PRIMARY KEY, cost REAL, life_years INTEGER, rate REAL, salvage REAL);
INSERT INTO assets VALUES (1,10000,6,0.40,1000),(2,5000,3,0.25,500),(3,800,4,0.50,100);
"""
SQL_MAIN = """
WITH RECURSIVE p AS (
  SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices
), s(rn, day, close, ewma) AS (
  SELECT rn, day, close, close FROM p WHERE rn = 1
  UNION ALL
  SELECT p.rn, p.day, p.close, 0.3 * p.close + (1 - 0.3) * s.ewma
  FROM s JOIN p ON p.rn = s.rn + 1
)
SELECT day, close, ewma FROM s ORDER BY rn
"""
SQL_DEPR = """
WITH RECURSIVE b(asset_id, year, book) AS (
  SELECT asset_id, 0, cost FROM assets
  UNION ALL
  SELECT b.asset_id, b.year + 1, MAX(a.salvage, b.book * (1 - a.rate))
  FROM b JOIN assets a ON a.asset_id = b.asset_id
  WHERE b.year < a.life_years
)
SELECT asset_id, year, ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year), 2) AS opening,
       ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year) - book, 2) AS depreciation,
       ROUND(book, 2) AS closing
FROM b
ORDER BY asset_id, year
"""
# closed forms: no recursion needed for either, shown to prove the recursion is not the only way
SQL_EWMA_CLOSED = """
WITH p AS (SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices)
SELECT day, close,
       SUM(CASE WHEN rn = 1 THEN close / 0.7 ELSE 0.3 * close * power(0.7, -rn) END)
         OVER (ORDER BY rn ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * power(0.7, rn) AS ewma
FROM p ORDER BY rn
"""
SQL_DEPR_CLOSED = """
WITH RECURSIVE y(asset_id, year) AS (
  SELECT asset_id, 0 FROM assets
  UNION ALL SELECT y.asset_id, y.year + 1 FROM y JOIN assets a ON a.asset_id = y.asset_id WHERE y.year < a.life_years
)
SELECT y.asset_id, y.year, ROUND(MAX(a.salvage, a.cost * power(1 - a.rate, y.year)), 2) AS closing
FROM y JOIN assets a ON a.asset_id = y.asset_id
WHERE y.year >= 1 ORDER BY y.asset_id, y.year
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ew = pd.read_sql_query(SQL_MAIN, con)
dep = pd.read_sql_query(SQL_DEPR, con)
print("(a) EWMA, alpha 0.3, seed s_1 = x_1:")
print(ew.round(4).to_string(index=False))
print("(b) declining balance with a salvage floor (year 0 rows have no depreciation):")
print(dep.to_string(index=False))

prices = pd.read_sql_query("SELECT * FROM daily_prices", con)
assets = pd.read_sql_query("SELECT * FROM assets", con)

def pandas_side(prices, assets):
    # pd:main
    ewma = prices.sort_values("day")["close"].ewm(alpha=0.3, adjust=False).mean()
    rows = []
    for a in assets.itertuples():
        book = a.cost
        rows.append((a.asset_id, 0, np.nan, np.nan, book))
        for y in range(1, a.life_years + 1):
            new = max(a.salvage, book * (1 - a.rate))
            rows.append((a.asset_id, y, book, book - new, new))
            book = new
    depr = pd.DataFrame(rows, columns=["asset_id", "year", "opening", "depreciation", "closing"])
    return ewma, depr
    # pd:end

pd_ewma, pd_dep = pandas_side(prices, assets)
np.testing.assert_allclose(pd_ewma.to_numpy(), ew["ewma"].to_numpy(), rtol=0, atol=1e-9)
half_up = lambda col: np.floor(col * 100 + 0.5) / 100   # SQLite ROUND rounds halves away from zero (positive values here)
pd.testing.assert_frame_equal(pd_dep.assign(**{c: half_up(pd_dep[c]) for c in ("opening", "depreciation", "closing")}), dep, check_dtype=False)   # compared after sorting by asset_id, year
print("depreciation of asset 2, year 3 is exactly 703.125: SQLite ROUND gives", dep.loc[(dep.asset_id == 2) & (dep.year == 3), "depreciation"].iloc[0], "| pandas .round(2) gives", pd_dep.round(2).loc[(pd_dep.asset_id == 2) & (pd_dep.year == 3), "depreciation"].iloc[0], "(half to even)")
print("pandas ewm(alpha=0.3, adjust=False) equals the recursive CTE (atol 1e-9); depreciation loop equals SQL")

# conventions
adj = prices["close"].ewm(alpha=0.3, adjust=True).mean()
seed0 = [0.0]
for x in prices["close"]:
    seed0.append(0.3 * x + 0.7 * seed0[-1])
cmp = pd.DataFrame({"day": prices["day"], "recursive_seed_x1": ew["ewma"].round(4), "pandas_adjust_False": pd_ewma.round(4),
                    "pandas_adjust_True": adj.round(4), "seed_zero": np.round(seed0[1:], 4)})
print("conventions (first rows):")
print(cmp.head(4).to_string(index=False))
print("max abs difference adjust=True vs adjust=False over 10 rows:", round(float((adj - pd_ewma).abs().max()), 4), "| last row:", round(float((adj - pd_ewma).abs().iloc[-1]), 6))

# closed forms
cf = pd.read_sql_query(SQL_EWMA_CLOSED, con)
np.testing.assert_allclose(cf["ewma"].to_numpy(), ew["ewma"].to_numpy(), rtol=0, atol=1e-9)
dc = pd.read_sql_query(SQL_DEPR_CLOSED, con)
assert dc["closing"].tolist() == dep[dep.year >= 1]["closing"].tolist()
print("closed forms (weighted running SUM for EWMA, MAX(salvage, cost * (1-rate)^year) for depreciation) equal the recursive results")
# numerical limit of the EWMA closed form: power(0.7, -n) overflows
con.execute("CREATE TABLE long_p(day TEXT, close REAL)")
con.executemany("INSERT INTO long_p VALUES (?, ?)", [(f"{i:05d}", 100.0 + (i % 7)) for i in range(1, 2401)])
lp = pd.read_sql_query(SQL_EWMA_CLOSED.replace("daily_prices", "long_p"), con)
lr = pd.read_sql_query(SQL_MAIN.replace("daily_prices", "long_p"), con)
bad = lp["ewma"].isna() | ((lp["ewma"] - lr["ewma"]).abs() > 1e-6)
print("2400-row series: first row where the closed form is wrong or NULL:", int(bad.idxmax()) + 1 if bad.any() else None, "| recursive form fine to the end:", float(lr["ewma"].iloc[-1].round(4)))

# NULL close: SQL recursion carries the previous value; pandas ewm weights by position
con.execute("UPDATE daily_prices SET close = NULL WHERE day = '2024-03-05'")
sn = pd.read_sql_query(SQL_MAIN.replace("0.3 * p.close + (1 - 0.3) * s.ewma", "CASE WHEN p.close IS NULL THEN s.ewma ELSE 0.3 * p.close + (1 - 0.3) * s.ewma END"), con)
pn = pd.read_sql_query("SELECT * FROM daily_prices", con)["close"].ewm(alpha=0.3, adjust=False).mean()
pni = pd.read_sql_query("SELECT * FROM daily_prices", con)["close"].ewm(alpha=0.3, adjust=False, ignore_na=True).mean()
print("NULL close on 2024-03-05, rows 5 to 7: SQL carry-forward", sn["ewma"].round(4).tolist()[4:7], "| pandas default", pn.round(4).tolist()[4:7], "| pandas ignore_na=True", pni.round(4).tolist()[4:7])
print("empty prices ->", con.execute(SQL_MAIN.replace("FROM daily_prices", "FROM daily_prices WHERE 1 = 0")).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
(a) EWMA, alpha 0.3, seed s_1 = x_1:
       day  close     ewma
2024-03-01  100.0 100.0000
2024-03-02  102.0 100.6000
2024-03-03  101.0 100.7200
2024-03-04  105.0 102.0040
2024-03-05  103.0 102.3028
2024-03-06  108.0 104.0120
2024-03-07  110.0 105.8084
2024-03-08  107.0 106.1659
2024-03-11  111.0 107.6161
2024-03-12  115.0 109.8313
(b) declining balance with a salvage floor (year 0 rows have no depreciation):
 asset_id  year  opening  depreciation  closing
        1     0      NaN           NaN 10000.00
        1     1  10000.0       4000.00  6000.00
        1     2   6000.0       2400.00  3600.00
        1     3   3600.0       1440.00  2160.00
        1     4   2160.0        864.00  1296.00
        1     5   1296.0        296.00  1000.00
        1     6   1000.0          0.00  1000.00
        2     0      NaN           NaN  5000.00
        2     1   5000.0       1250.00  3750.00
        2     2   3750.0        937.50  2812.50
        2     3   2812.5        703.13  2109.38
        3     0      NaN           NaN   800.00
        3     1    800.0        400.00   400.00
        3     2    400.0        200.00   200.00
        3     3    200.0        100.00   100.00
        3     4    100.0          0.00   100.00
depreciation of asset 2, year 3 is exactly 703.125: SQLite ROUND gives 703.13 | pandas .round(2) gives 703.12 (half to even)
pandas ewm(alpha=0.3, adjust=False) equals the recursive CTE (atol 1e-9); depreciation loop equals SQL
conventions (first rows):
       day  recursive_seed_x1  pandas_adjust_False  pandas_adjust_True  seed_zero
2024-03-01            100.000              100.000            100.0000     30.000
2024-03-02            100.600              100.600            101.1765     51.600
2024-03-03            100.720              100.720            101.0959     66.420
2024-03-04            102.004              102.004            102.6372     77.994
max abs difference adjust=True vs adjust=False over 10 rows: 0.6332 | last row: 0.285782
closed forms (weighted running SUM for EWMA, MAX(salvage, cost * (1-rate)^year) for depreciation) equal the recursive results
2400-row series: first row where the closed form is wrong or NULL: 1978 | recursive form fine to the end: 104.2949
NULL close on 2024-03-05, rows 5 to 7: SQL carry-forward [102.004, 103.8028, 105.662] | pandas default [102.004, 104.281, 105.9967] | pandas ignore_na=True [102.004, 103.8028, 105.662]
empty prices -> []
asserts passed
```
Honest notes from the run:
- Rounding surprise: the year 3 depreciation of asset 2 is exactly 703.125. SQLite `ROUND(x, 2)` gives 703.13 and pandas `.round(2)` gives 703.12 (half to even). The first version of my assert failed on exactly this, which is why the code compares through a half-up helper.
- Conventions for (a): `adjust=False` is the recursive formula with the first value as the seed, so it equals the CTE. `adjust=True` (the pandas default) computes a weighted average of all earlier values with weights that sum to 1 at every step; its first rows differ (101.1765 versus 100.6 on day 2) and the difference is still 0.29 on day 10. A seed of 0 (starting from `s_0 = 0`) pulls the first values far below the price (30.0 on day 1), which is why the first value is usually the seed.
- The window-function closed form of the EWMA (a running `SUM` of `0.3 * x * power(0.7, -rn)` times `power(0.7, rn)`) matches the recursion on 10 rows, but on a 2400-row test series it went wrong from row 1978 (the large powers lose precision and then overflow); the recursion stayed fine to the end. That is the reason I would not use it in production.
- NULL close: with a `CASE` that carries the previous value, SQL gives 102.004, 103.8028, 105.662 on the NULL day and the two days after; pandas default `ewm` gives 102.004, 104.281, 105.9967 (it weights by position, so the gap makes the old value decay), and `ignore_na=True` gives the same numbers as the SQL carry-forward.

**Edge cases:**
- First row is the seed (assumption). Say it out loud; interviewers differ on `s_0 = 0` versus `s_1 = x_1`.
- NULL price: the recursive step must decide (carry the previous EWMA, as I did, or skip); an unguarded `0.3 * NULL + ...` gives NULL for the rest of the series.
- Weekend or missing days: this EWMA is by row, not by calendar time; a time-weighted EWMA needs the gap length in the weight.
- Empty table: no anchor, empty result (printed).
- Floor already above cost, rate 0, or salvage 0: handled by the formula (book never goes below the floor; rate 0 keeps the book value).
- Duplicate days: `ROW_NUMBER` would number them arbitrarily; deduplicate first.

**Then explain:** (part c, why neither is a plain window function)
- A window function computes an aggregate over a frame of input values with fixed or running weights. An EWMA has weights that decay with distance, and the built-in aggregates (`SUM`, `AVG`, ...) have no weight parameter, so the engine gives you nothing that applies `0.7^k`. The declining balance multiplies by a constant each year, which is not an aggregate either.
- The recursive member is the natural expression because the next value is a function of the previous output. That is a "fold", and recursion is how SQL expresses a fold.
- Closed forms exist (shown and asserted): EWMA as a weighted running sum scaled by powers, depreciation as `MAX(salvage, cost * (1-rate)^year)`. The depreciation closed form is better than recursion where it applies. A truly state-dependent variant that would still need recursion is the switch-to-straight-line rule (change method when straight-line depreciation exceeds the declining balance), which I did not run.
- Other engines (not executed here): the same queries work in PostgreSQL and MySQL 8 with `WITH RECURSIVE` and in SQL Server without the keyword; `POWER` exists in all of them (from memory, not executed). SQL Server's `OPTION (MAXRECURSION)` and MySQL's `cte_max_recursion_depth` limit long series.

**Follow-ups:**
- "How do you pick alpha from a span?" `alpha = 2 / (span + 1)`, so span 9 gives 0.2 (a pandas documented relation; I did not run other spans here).
- "EWMA by calendar day with gaps?" Weight by the number of days since the last observation: `alpha_eff = 1 - (1 - alpha)^gap_days`.
- "Why not keep the series in pandas?" For one series pandas is simpler and faster; in SQL it is for data that is already there or too big to move.

**Common mistakes:**
- Assuming pandas `ewm` default equals the recursive formula (the default is `adjust=True`).
- Starting from `s_0 = 0` and getting a biased start.
- Comparing floats with `==` instead of a tolerance.
- Letting book value fall below the salvage value, or depreciating past the useful life.
- Using the weighted-sum closed form on long series and getting NULL or garbage from huge powers.

### Q20 ⭐⭐ 🟡 Delete or move a subtree with a recursive CTE: categories(category_id, parent_id, name, path) and employees(emp_id, manager_id). Delete category 5 and everything under it with DELETE ... WHERE category_id IN (WITH RECURSIVE ... SELECT ...), show the rows before and after, then move subtree 8 under parent 2 and rebuild the materialised path of all descendants, and prevent a move that would create a cycle (the new parent must not be a descendant of the moved node). State what a foreign key with ON DELETE CASCADE does instead, and which statements are portable (SQL Server needs the CTE before the DELETE, MySQL 8 supports CTE with DELETE, both hedged, not executed).
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Find the subtree with a recursive CTE and delete by id (`DELETE ... WHERE category_id IN (WITH RECURSIVE ... SELECT id FROM sub)`), move it by updating one `parent_id` and then rebuilding the `path` of the moved node and all its descendants from the new parent's path, and before any move check that the new parent is not inside the moved subtree, because that would create a cycle; a foreign key with `ON DELETE CASCADE` can do the delete without a recursive query, if the engine enforces it.

**Schema and sample data:** a ten-row category tree with a materialised path (`'/1/5/6/'` means 1 > 5 > 6) and a seven-row employee table. Category 5 (Electronics) has Phones (6), Laptops (7) and Android (9, under Phones); category 8 (Garden) has Tools (10), Lawn (11) and Spades (12, under Tools).
```sql
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Store','/1/'),(2,1,'Home','/1/2/'),(5,1,'Electronics','/1/5/'),(6,5,'Phones','/1/5/6/'),
 (7,5,'Laptops','/1/5/7/'),(9,6,'Android','/1/5/6/9/'),(8,1,'Garden','/1/8/'),(10,8,'Tools','/1/8/10/'),
 (11,8,'Lawn','/1/8/11/'),(12,10,'Spades','/1/8/10/12/');
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES (1,NULL),(2,1),(3,1),(4,3),(5,3),(6,4),(7,2);
```

**SQL answer:** the delete is `SQL_MAIN` in the Code block:
```sql
DELETE FROM categories
WHERE category_id IN (
  WITH RECURSIVE sub(id) AS (
    SELECT category_id FROM categories WHERE category_id = 5
    UNION ALL
    SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
  )
  SELECT id FROM sub
)
```
The same pattern for the employee table, deleting manager 3 and everyone below, is `SQL_DELETE_EMP` in the Code block:
```sql
DELETE FROM employees
WHERE emp_id IN (
  WITH RECURSIVE team(id) AS (
    SELECT emp_id FROM employees WHERE emp_id = 3
    UNION ALL SELECT e.emp_id FROM employees e JOIN team t ON e.manager_id = t.id
  )
  SELECT id FROM team
)
```
The move is two statements in one transaction (`SQL_MOVE_PARENT` and `SQL_MOVE_PATHS` in the Code block), after a cycle check (`SQL_CYCLE_CHECK`):
```sql
WITH RECURSIVE sub(id) AS (
  SELECT :moved
  UNION
  SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
)
SELECT COUNT(*) FROM sub WHERE id = :newparent
```
```sql
UPDATE categories SET parent_id = :newparent WHERE category_id = :moved
```
```sql
WITH RECURSIVE t(id, newpath) AS (
  SELECT c.category_id, p.path || c.category_id || '/'
  FROM categories c JOIN categories p ON p.category_id = c.parent_id
  WHERE c.category_id = :moved
  UNION ALL
  SELECT c.category_id, t.newpath || c.category_id || '/'
  FROM categories c JOIN t ON c.parent_id = t.id
)
UPDATE categories SET path = (SELECT newpath FROM t WHERE t.id = categories.category_id)
WHERE category_id IN (SELECT id FROM t)
```
How it works:
- Delete: the recursive CTE starts at the chosen category and adds children until there are none; the outer `DELETE` removes those ids. The subquery is evaluated before rows disappear, so deleting the table you are reading from is safe in SQLite.
- Move: `UPDATE ... SET parent_id` re-attaches the node. The path rebuild is a second recursive CTE: the anchor is the moved node with `new parent's path || its id || '/'`, and each step appends a child's id to its parent's new path. The `UPDATE` then sets every affected row's path from the CTE. A string `REPLACE` of the old prefix would also work for a pure prefix change (not run).
- Cycle check: the subtree of the moved node (including the node itself) is built with `UNION`, so even a data cycle cannot loop; if the proposed new parent is in it, the move is refused. With the materialised path this is simply `new_parent.path LIKE moved.path || '%'` (not run separately here).
- The helper `move()` in the Code block wraps check and both updates in one transaction (`with con:`), so a failure cannot leave the parent changed and the paths stale.

**pandas answer:** a stack-based subtree walk, a drop for the delete and a path rebuild for the move (shown once, identical to the Code block):
```py
    c = cats.set_index("category_id")
    kids = {p: list(g.index) for p, g in c.dropna(subset=["parent_id"]).groupby("parent_id")}
    def subtree(root):
        out, stack = [], [root]
        while stack:
            n = stack.pop()
            out.append(n)
            stack.extend(kids.get(n, []))
        return out
    deleted = c.drop(subtree(5))
    moved = deleted.copy()
    moved.loc[8, "parent_id"] = 2
    for n in subtree(8):   # pre-order: a parent is always handled before its children
        p = moved.loc[n, "parent_id"]
        moved.loc[n, "path"] = moved.loc[int(p), "path"] + f"{n}/"
    return deleted.reset_index(), moved.reset_index()
```

**Example:** by hand.
- Delete category 5: the subtree is 5, 6, 7 and 9 (Electronics, Phones, Laptops, Android): 4 rows deleted; 1, 2, 8, 10, 11, 12 remain. For employees, deleting 3 removes 3, 4, 5 and 6 (4 rows), leaving 1, 2 and 7.
- Move 8 under 2: parent_id of 8 becomes 2. Paths: 8 becomes `/1/2/8/`; its children become `/1/2/8/10/` and `/1/2/8/11/`; Spades becomes `/1/2/8/10/12/`. Four rows change their path; Home, Store are untouched.
- Cycle check: moving 2 under 12 asks "is 12 in the subtree of 2?"; after the move 12 is below 8, which is below 2, so yes: refused. Moving 8 under 8 is refused because the subtree contains the node itself.

**Code:** run with `python3 -I`. Asserts: pandas equals SQL after the delete and after the move (both ordered by `category_id`), and refused moves leave the table unchanged.
```python
# Q20: delete a subtree, move a subtree with a rebuilt materialised path, and refuse a move that creates a cycle
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Store','/1/'),(2,1,'Home','/1/2/'),(5,1,'Electronics','/1/5/'),(6,5,'Phones','/1/5/6/'),
 (7,5,'Laptops','/1/5/7/'),(9,6,'Android','/1/5/6/9/'),(8,1,'Garden','/1/8/'),(10,8,'Tools','/1/8/10/'),
 (11,8,'Lawn','/1/8/11/'),(12,10,'Spades','/1/8/10/12/');
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES (1,NULL),(2,1),(3,1),(4,3),(5,3),(6,4),(7,2);
"""
SQL_MAIN = """
DELETE FROM categories
WHERE category_id IN (
  WITH RECURSIVE sub(id) AS (
    SELECT category_id FROM categories WHERE category_id = 5
    UNION ALL
    SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
  )
  SELECT id FROM sub
)
"""
SQL_CYCLE_CHECK = """
WITH RECURSIVE sub(id) AS (
  SELECT :moved
  UNION
  SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
)
SELECT COUNT(*) FROM sub WHERE id = :newparent
"""
SQL_MOVE_PARENT = """
UPDATE categories SET parent_id = :newparent WHERE category_id = :moved
"""
SQL_MOVE_PATHS = """
WITH RECURSIVE t(id, newpath) AS (
  SELECT c.category_id, p.path || c.category_id || '/'
  FROM categories c JOIN categories p ON p.category_id = c.parent_id
  WHERE c.category_id = :moved
  UNION ALL
  SELECT c.category_id, t.newpath || c.category_id || '/'
  FROM categories c JOIN t ON c.parent_id = t.id
)
UPDATE categories SET path = (SELECT newpath FROM t WHERE t.id = categories.category_id)
WHERE category_id IN (SELECT id FROM t)
"""
SQL_DELETE_EMP = """
DELETE FROM employees
WHERE emp_id IN (
  WITH RECURSIVE team(id) AS (
    SELECT emp_id FROM employees WHERE emp_id = 3
    UNION ALL SELECT e.emp_id FROM employees e JOIN team t ON e.manager_id = t.id
  )
  SELECT id FROM team
)
"""

def load():
    con = sqlite3.connect(":memory:")
    con.executescript(SCHEMA)
    return con

def table(con, name="categories"):
    return pd.read_sql_query(f"SELECT * FROM {name} ORDER BY 1", con)

def move(con, moved, newparent):
    # refuse a move into the moved node's own subtree (that includes the node itself)
    if con.execute(SQL_CYCLE_CHECK, {"moved": moved, "newparent": newparent}).fetchone()[0] > 0:
        return False
    with con:
        con.execute(SQL_MOVE_PARENT, {"moved": moved, "newparent": newparent})
        con.execute(SQL_MOVE_PATHS, {"moved": moved})
    return True

con = load()
before = table(con)
print("categories before:")
print(before.to_string(index=False))
cur = con.execute(SQL_MAIN)
print("DELETE category 5 and everything under it: rows deleted =", cur.rowcount)
after_del = table(con)
print(after_del.to_string(index=False))
cur = con.execute(SQL_DELETE_EMP)
print("DELETE employee 3 and the whole team below: rows deleted =", cur.rowcount, "| employees left:", [r[0] for r in con.execute("SELECT emp_id FROM employees ORDER BY 1")])

ok = move(con, 8, 2)
after_move = table(con)
print("move subtree 8 under 2 (moved =", ok, "):")
print(after_move.to_string(index=False))
print("move 2 under 12 (a descendant of 2 after the move) accepted?", move(con, 2, 12), "| move 8 under itself accepted?", move(con, 8, 8))
assert table(con).equals(after_move), "refused moves must not change anything"

cats = before.copy()

def pandas_side(cats):
    # pd:main
    c = cats.set_index("category_id")
    kids = {p: list(g.index) for p, g in c.dropna(subset=["parent_id"]).groupby("parent_id")}
    def subtree(root):
        out, stack = [], [root]
        while stack:
            n = stack.pop()
            out.append(n)
            stack.extend(kids.get(n, []))
        return out
    deleted = c.drop(subtree(5))
    moved = deleted.copy()
    moved.loc[8, "parent_id"] = 2
    for n in subtree(8):   # pre-order: a parent is always handled before its children
        p = moved.loc[n, "parent_id"]
        moved.loc[n, "path"] = moved.loc[int(p), "path"] + f"{n}/"
    return deleted.reset_index(), moved.reset_index()
    # pd:end

pd_del, pd_move = pandas_side(cats)
pd.testing.assert_frame_equal(pd_del, after_del, check_dtype=False)   # compared after sorting by category_id
pd.testing.assert_frame_equal(pd_move, after_move, check_dtype=False)
print("pandas results equal SQL after the delete and after the move")
assert table(con, "categories")["category_id"].tolist() == [1, 2, 8, 10, 11, 12]
n_sub = con.execute("SELECT COUNT(*) FROM categories WHERE path LIKE '/1/2/8/%'").fetchone()[0]
print("rows whose path starts with /1/2/8/ after the move:", n_sub, "(Garden and its three descendants)")

# what the cycle check protects: a move into the own subtree, forced without the check
c2 = load()
c2.execute("UPDATE categories SET parent_id = 9 WHERE category_id = 5")
reach = c2.execute("""WITH RECURSIVE d(id) AS (SELECT category_id FROM categories WHERE parent_id IS NULL
                      UNION SELECT c.category_id FROM categories c JOIN d ON c.parent_id = d.id) SELECT COUNT(*) FROM d""").fetchone()[0]
print("forced move 5 under 9 without the check: rows reachable from the root drop from 10 to", reach, "(Electronics, Phones, Laptops, Android are now a detached cycle)")
# a naive delete without recursion
c3 = load()
c3.execute("DELETE FROM categories WHERE category_id = 5")
print("plain DELETE of category 5 leaves orphans:", [r[0] for r in c3.execute("SELECT category_id FROM categories WHERE parent_id IS NOT NULL AND parent_id NOT IN (SELECT category_id FROM categories) ORDER BY 1")])

# foreign key with ON DELETE CASCADE does the same without a recursive query, but only with the pragma on
def fk_run(pragma):
    c = sqlite3.connect(":memory:")
    c.execute(f"PRAGMA foreign_keys = {pragma}")
    c.executescript("""
    CREATE TABLE cat(category_id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES cat(category_id) ON DELETE CASCADE, name TEXT);
    INSERT INTO cat VALUES (1,NULL,'Store'),(5,1,'Electronics'),(6,5,'Phones'),(7,5,'Laptops'),(9,6,'Android'),(8,1,'Garden');""")
    c.execute("DELETE FROM cat WHERE category_id = 5")
    return [r[0] for r in c.execute("SELECT category_id FROM cat ORDER BY 1")]
print("ON DELETE CASCADE with foreign_keys = ON leaves", fk_run("ON"), "| with the default (OFF) leaves", fk_run("OFF"))
empty = sqlite3.connect(":memory:")
empty.execute("CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT)")
print("delete a missing id:", load().execute(SQL_MAIN.replace("= 5", "= 999")).rowcount, "rows | empty table:", empty.execute(SQL_MAIN).rowcount, "rows")
print("asserts passed")
```

**Output (my run):**
```text
categories before:
 category_id  parent_id        name        path
           1        NaN       Store         /1/
           2        1.0        Home       /1/2/
           5        1.0 Electronics       /1/5/
           6        5.0      Phones     /1/5/6/
           7        5.0     Laptops     /1/5/7/
           8        1.0      Garden       /1/8/
           9        6.0     Android   /1/5/6/9/
          10        8.0       Tools    /1/8/10/
          11        8.0        Lawn    /1/8/11/
          12       10.0      Spades /1/8/10/12/
DELETE category 5 and everything under it: rows deleted = 4
 category_id  parent_id   name        path
           1        NaN  Store         /1/
           2        1.0   Home       /1/2/
           8        1.0 Garden       /1/8/
          10        8.0  Tools    /1/8/10/
          11        8.0   Lawn    /1/8/11/
          12       10.0 Spades /1/8/10/12/
DELETE employee 3 and the whole team below: rows deleted = 4 | employees left: [1, 2, 7]
move subtree 8 under 2 (moved = True ):
 category_id  parent_id   name          path
           1        NaN  Store           /1/
           2        1.0   Home         /1/2/
           8        2.0 Garden       /1/2/8/
          10        8.0  Tools    /1/2/8/10/
          11        8.0   Lawn    /1/2/8/11/
          12       10.0 Spades /1/2/8/10/12/
move 2 under 12 (a descendant of 2 after the move) accepted? False | move 8 under itself accepted? False
pandas results equal SQL after the delete and after the move
rows whose path starts with /1/2/8/ after the move: 4 (Garden and its three descendants)
forced move 5 under 9 without the check: rows reachable from the root drop from 10 to 6 (Electronics, Phones, Laptops, Android are now a detached cycle)
plain DELETE of category 5 leaves orphans: [6, 7]
ON DELETE CASCADE with foreign_keys = ON leaves [1, 8] | with the default (OFF) leaves [1, 6, 7, 8, 9]
delete a missing id: 0 rows | empty table: 0 rows
asserts passed
```
Honest notes from the run:
- A plain `DELETE ... WHERE category_id = 5` leaves orphans 6 and 7 (the unguarded version of the problem). Forcing 5 under 9 without the check makes four rows a detached cycle and the number of rows reachable from the root drops from 10 to 6, so a top-down query silently loses them.
- `ON DELETE CASCADE` on a self-referencing foreign key deleted the whole subtree (left rows 1 and 8) when `PRAGMA foreign_keys = ON`, and deleted only the one row (left 1, 6, 7, 8, 9) with SQLite's default, because SQLite does not enforce foreign keys unless that pragma is set on the connection.
- Deleting a missing id or running on an empty table deletes 0 rows and raises nothing.

**Edge cases:**
- Deleting the root removes everything; deleting a leaf removes one row; a missing id removes nothing.
- Foreign keys from other tables (for example `products.category_id`) would block the delete or need their own cascade or reassignment; delete children before parents in engines that check row by row.
- Moving a node to the root: `parent_id` NULL and path `'/' || id || '/'`; the SQL above needs a variant for NULL because the anchor joins to the new parent.
- Concurrent edits: two moves at once can create a cycle even though each passed the check; take a lock or run the check and the update in one serialisable transaction (a general rule, not tested here).
- The materialised path must be changed for every descendant: that is the write cost of this storage model (Q24).
- Unknown new parent (id not in the table): the path anchor returns no row and the paths do not change, so check the parent exists first.

**Then explain:**
- Why the new parent must not be a descendant: the moved node would become its own ancestor; the subtree would lose its connection to the root and would be invisible to any top-down query (the forced move printed above).
- `ON DELETE CASCADE` versus a recursive delete: the cascade is declarative and the engine does the walk (if it enforces foreign keys; in SQLite only with the pragma on), but it deletes silently and can be limited in depth in some engines; the recursive `DELETE` is explicit and can be wrapped with a preview `SELECT` using the same CTE.
- Preview first: run the CTE as a `SELECT` to list what would go, then delete.
- Portability (not executed): SQL Server needs the CTE before the statement (`WITH sub AS (...) DELETE FROM categories WHERE category_id IN (SELECT id FROM sub)`) with no `RECURSIVE` keyword; MySQL 8 supports a CTE with `DELETE` (CTE first), and may complain (error 1093) about reading and deleting the same table in a subquery in some forms; PostgreSQL accepts `WITH RECURSIVE ... DELETE`. All three are from memory and documentation snippets, not executed here.

**Follow-ups:**
- "Soft delete instead?" Set `deleted_at` on the same subtree ids; reads must filter it, and a restore uses the same CTE.
- "Move without rebuilding every path?" Use the closure table or nested sets (Q24), which pay a different write cost.
- "What about reassigning children instead of deleting?" Update their `parent_id` to the deleted node's parent before deleting the node.

**Common mistakes:**
- Deleting only the node and leaving orphan children.
- Assuming `ON DELETE CASCADE` works in SQLite without `PRAGMA foreign_keys = ON`.
- Updating `parent_id` but not the paths of the descendants.
- Allowing a move under the node's own descendant, or under itself.
- Doing the check and the move in separate transactions.

### Q21 ⭐⭐ 🟡 Engine portability of hierarchical queries: take the employee subtree query and write it for MySQL 8 (WITH RECURSIVE, CAST in the anchor so the path column is wide enough, cte_max_recursion_depth), SQL Server (WITH without RECURSIVE, OPTION (MAXRECURSION 100 by default), + for concatenation), PostgreSQL 14+ (SEARCH DEPTH FIRST and CYCLE clauses) and Oracle (START WITH ... CONNECT BY PRIOR, LEVEL, SYS_CONNECT_BY_PATH, CONNECT_BY_ISLEAF, NOCYCLE). Run only the SQLite version and mark the others not executed. Include what SQLite 3.45.1 does not support (the CYCLE and SEARCH clauses fail with a syntax error and there is no generate_series without an extension), as checked by running them.
**Asked at:** Oracle hierarchical query documentation (search snippets only, not opened: START WITH, CONNECT BY PRIOR, LEVEL, SYS_CONNECT_BY_PATH, CONNECT_BY_ISLEAF, NOCYCLE, CONNECT_BY_ISCYCLE, ORA-01436 on a loop; Snowflake CONNECT BY docs supporting SYS_CONNECT_BY_PATH but not NOCYCLE, ISCYCLE or ISLEAF) plus the opened PostgreSQL, MySQL 8.4 and SQLite pages; documentation, not candidate reports; interviews on Oracle, SQL Server and PostgreSQL stacks
**Say this first (1 line):** The shape of a hierarchical query (anchor, recursive step, guard) is the same everywhere, but the spelling is not: SQLite, MySQL 8 and PostgreSQL write `WITH RECURSIVE`, SQL Server writes plain `WITH` and caps recursion with `OPTION (MAXRECURSION n)`, Oracle has its own `START WITH ... CONNECT BY PRIOR`, and PostgreSQL 14+ adds `SEARCH` and `CYCLE` clauses that SQLite 3.45.1 rejects; I ran only the SQLite version and the other dialects below are written from the docs and memory, not executed.

**Schema and sample data:** twelve employees, one tree (Tim is the CEO with a NULL manager), and the same data as the other hierarchy questions in this part; the subtree is Hari (emp 3).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
```

**SQL answer:** `SQL_MAIN` in the Code block, the SQLite version (it also runs unchanged on PostgreSQL and MySQL 8 apart from the string concatenation, see the table):
```sql
WITH RECURSIVE sub(emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, s.path || ' > ' || e.name
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT s.emp_id, s.name, s.level, s.path,
       CASE WHEN EXISTS (SELECT 1 FROM employees c WHERE c.manager_id = s.emp_id) THEN 0 ELSE 1 END AS is_leaf
FROM sub s
ORDER BY s.path
```
The `WHERE s.level < 20` line is a depth guard that I keep in every dialect: it is portable, it makes the intent visible, and it works even where the engine has its own cap.

The dialect versions below are **not executed here** (no PostgreSQL, MySQL, SQL Server, Oracle or Snowflake server in this environment). They follow the opened MySQL 8.4 and PostgreSQL pages and my memory of the others; check each against your engine's documentation before relying on it.

MySQL 8 (not executed): `WITH RECURSIVE` is required, `CONCAT` is the safe string join (`||` means OR unless the `PIPES_AS_CONCAT` mode is on), and the column types come from the anchor, so the path column is cast wide enough:
```sql
-- MySQL 8.x, NOT EXECUTED
WITH RECURSIVE sub (emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, CAST(name AS CHAR(200)) FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, CONCAT(s.path, ' > ', e.name)
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT s.emp_id, s.name, s.level, s.path FROM sub s ORDER BY s.path;
-- session cap on iterations (default 1000 per the MySQL 8.4 page): SET SESSION cte_max_recursion_depth = 5000;
```
SQL Server (not executed): no `RECURSIVE` keyword, `+` joins strings, the anchor and recursive column types must match exactly (hence both `CAST`s), and the default recursion cap is 100 levels (error 530, per search snippets; `OPTION (MAXRECURSION 0)` means no cap), written at the very end of the outer statement:
```sql
-- SQL Server, NOT EXECUTED
WITH sub (emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, CAST(name AS VARCHAR(400)) FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, CAST(s.path + ' > ' + e.name AS VARCHAR(400))
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT s.emp_id, s.name, s.level, s.path FROM sub s ORDER BY s.path
OPTION (MAXRECURSION 100);
```
PostgreSQL 14+ (not executed; the version number comes from a search snippet, the clause syntax from the opened PostgreSQL page): `SEARCH` orders the output depth-first or breadth-first, `CYCLE` marks and stops rows that revisit a node, so no hand-written path guard is needed:
```sql
-- PostgreSQL 14+, NOT EXECUTED
WITH RECURSIVE sub (emp_id, name, level) AS (
  SELECT emp_id, name, 0 FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
)
SEARCH DEPTH FIRST BY emp_id SET ordercol
CYCLE emp_id SET is_cycle USING cycle_path
SELECT * FROM sub ORDER BY ordercol;
```
Oracle (not executed; from documentation snippets, not opened): a separate hierarchical syntax. `LEVEL` starts at 1, `SYS_CONNECT_BY_PATH` starts with the separator (so the path is `' > Hari > Shyam'`), `NOCYCLE` suppresses the loop error (ORA-01436 without it, per snippets), `CONNECT_BY_ISLEAF` is the leaf flag:
```sql
-- Oracle, NOT EXECUTED
SELECT emp_id, name, LEVEL - 1 AS lvl, SYS_CONNECT_BY_PATH(name, ' > ') AS path, CONNECT_BY_ISLEAF AS is_leaf
FROM employees
START WITH emp_id = 3
CONNECT BY NOCYCLE PRIOR emp_id = manager_id
ORDER SIBLINGS BY name;
```
Snowflake (not executed): per a search snippet it supports both `WITH RECURSIVE` and `CONNECT BY` with `SYS_CONNECT_BY_PATH`, but not `NOCYCLE`, `CONNECT_BY_ISCYCLE` or `CONNECT_BY_ISLEAF`; I would write the `WITH RECURSIVE` form with a depth counter there.

| Item | SQLite 3.45.1 (run) | MySQL 8 | SQL Server | PostgreSQL | Oracle |
|---|---|---|---|---|---|
| Keyword | `WITH RECURSIVE` | `WITH RECURSIVE` | `WITH` | `WITH RECURSIVE` | `CONNECT BY` (or `WITH`) |
| String join | `\|\|` (`+` gives 0, see Output) | `CONCAT` | `+` or `CONCAT` | `\|\|` | `\|\|` |
| Iteration cap | none; stops by `LIMIT`, empty queue or your depth column | `cte_max_recursion_depth`, default 1000 | `MAXRECURSION`, default 100 | none by default; your depth column or `LIMIT` | no cap; a loop raises an error unless `NOCYCLE` |
| Cycle help | hand-written path or `UNION` | hand-written | hand-written | `CYCLE` clause (14+) | `NOCYCLE`, `CONNECT_BY_ISCYCLE` |
| Order help | `ORDER BY` in the recursive select sets queue order | none | none | `SEARCH` clause (14+) | `ORDER SIBLINGS BY` |
All non-SQLite cells are not executed here.

**pandas answer:** the portability question is about SQL; the pandas counterpart is dialect-free: a frontier merge that expands one level per iteration, with a visited set as the cycle guard. Shown once here and identical to the Code block:
```py
kids = employees[["emp_id", "manager_id", "name"]].rename(columns={"emp_id": "child_id", "name": "child_name"})
frontier = employees.loc[employees["emp_id"] == 3, ["emp_id", "name"]].assign(level=0)
frontier["path"] = frontier["name"]
parts, seen = [frontier], {3}
while len(frontier):
    nxt = frontier[["emp_id", "level", "path"]].merge(kids, left_on="emp_id", right_on="manager_id")
    nxt = nxt[~nxt["child_id"].isin(seen)]
    frontier = pd.DataFrame({"emp_id": nxt["child_id"], "name": nxt["child_name"],
                             "level": nxt["level"] + 1, "path": nxt["path"] + " > " + nxt["child_name"]})
    seen.update(frontier["emp_id"])
    parts.append(frontier)
pd_df = pd.concat(parts, ignore_index=True)
pd_df["is_leaf"] = (~pd_df["emp_id"].isin(employees["manager_id"].dropna())).astype(int)
pd_df = pd_df.sort_values("path").reset_index(drop=True)
```

**Example:** Hari (3) is the anchor, level 0, path `Hari`. Round 1 joins employees whose manager is 3: Shyam (4) and Asha (7), level 1, paths `Hari > Shyam` and `Hari > Asha`. Round 2: the reports of 4 are Ram (10) and Zoya (11), the report of 7 is Nina (12), level 2. Round 3: nobody reports to 10, 11 or 12, the working table is empty and the recursion stops. Six rows in total. `is_leaf` is 1 for Ram, Zoya and Nina (nobody has them as a manager) and 0 for Hari, Shyam and Asha. The pandas loop does the same: three merges (levels 1, 2, and a third that finds nothing), six rows, equal to the SQL after sorting both by `path`.

**Code:** run with `python3 -I`. It runs the SQLite query and the pandas loop, asserts they are equal after sorting both by `path`, then executes each SQLite-limitation probe and prints what happened (the failures are caught on purpose).
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
"""
SQL_MAIN = """
WITH RECURSIVE sub(emp_id, name, level, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE emp_id = 3
  UNION ALL
  SELECT e.emp_id, e.name, s.level + 1, s.path || ' > ' || e.name
  FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT s.emp_id, s.name, s.level, s.path,
       CASE WHEN EXISTS (SELECT 1 FROM employees c WHERE c.manager_id = s.emp_id) THEN 0 ELSE 1 END AS is_leaf
FROM sub s
ORDER BY s.path
"""
PROBES = [
  ("CYCLE clause (PostgreSQL 14+ syntax)",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 3) "
   "CYCLE n SET is_cycle USING path SELECT * FROM t"),
  ("SEARCH DEPTH FIRST clause (PostgreSQL 14+ syntax)",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 3) "
   "SEARCH DEPTH FIRST BY n SET ordercol SELECT * FROM t ORDER BY ordercol"),
  ("generate_series", "SELECT value FROM generate_series(1, 3)"),
  ("CTE referenced twice in the recursive member",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t "
   "WHERE n < 3 AND n NOT IN (SELECT n FROM t)) SELECT * FROM t"),
  ("aggregate in the recursive member",
   "WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT MAX(n) + 1 FROM t WHERE n < 3) SELECT * FROM t"),
  ("'a' + 'b' (SQL Server style concatenation)", "SELECT 'a' + 'b'"),
  ("CAST in the anchor as MySQL needs it: length of the final path",
   "WITH RECURSIVE t(n, p) AS (SELECT 1, CAST('a' AS CHAR(1)) UNION ALL "
   "SELECT n + 1, p || 'bbbb' FROM t WHERE n < 5) SELECT length(p) FROM t WHERE n = 5"),
  ("no default recursion cap: count to 1,000,000",
   "WITH RECURSIVE c(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM c WHERE n < 1000000) "
   "SELECT COUNT(*), MAX(n) FROM c"),
]

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
employees["manager_id"] = employees["manager_id"].astype("Int64")

# pd:main
kids = employees[["emp_id", "manager_id", "name"]].rename(columns={"emp_id": "child_id", "name": "child_name"})
frontier = employees.loc[employees["emp_id"] == 3, ["emp_id", "name"]].assign(level=0)
frontier["path"] = frontier["name"]
parts, seen = [frontier], {3}
while len(frontier):
    nxt = frontier[["emp_id", "level", "path"]].merge(kids, left_on="emp_id", right_on="manager_id")
    nxt = nxt[~nxt["child_id"].isin(seen)]
    frontier = pd.DataFrame({"emp_id": nxt["child_id"], "name": nxt["child_name"],
                             "level": nxt["level"] + 1, "path": nxt["path"] + " > " + nxt["child_name"]})
    seen.update(frontier["emp_id"])
    parts.append(frontier)
pd_df = pd.concat(parts, ignore_index=True)
pd_df["is_leaf"] = (~pd_df["emp_id"].isin(employees["manager_id"].dropna())).astype(int)
pd_df = pd_df.sort_values("path").reset_index(drop=True)
# pd:end
# compare after ordering both by path (the SQL ORDER BY path)
pd.testing.assert_frame_equal(pd_df[list(sql_df.columns)].astype({"emp_id": "int64"}), sql_df, check_dtype=False)
print("pandas frontier loop equals the SQLite recursive CTE:", len(pd_df), "rows,", len(parts) - 1, "merges (the last one finds nothing)")

print("\nProbes on SQLite", sqlite3.sqlite_version, "(each statement was run):")
for label, sql in PROBES:
    try:
        print(f"  OK   {label}: {con.execute(sql).fetchall()}")
    except sqlite3.Error as ex:
        print(f"  FAIL {label}: {type(ex).__name__}: {ex}")
print("asserts passed")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5
 emp_id  name  level                path  is_leaf
      3  Hari      0                Hari        0
      7  Asha      1         Hari > Asha        0
     12  Nina      2  Hari > Asha > Nina        1
      4 Shyam      1        Hari > Shyam        0
     10   Ram      2  Hari > Shyam > Ram        1
     11  Zoya      2 Hari > Shyam > Zoya        1
pandas frontier loop equals the SQLite recursive CTE: 6 rows, 3 merges (the last one finds nothing)

Probes on SQLite 3.45.1 (each statement was run):
  FAIL CYCLE clause (PostgreSQL 14+ syntax): OperationalError: near "CYCLE": syntax error
  FAIL SEARCH DEPTH FIRST clause (PostgreSQL 14+ syntax): OperationalError: near "SEARCH": syntax error
  FAIL generate_series: OperationalError: no such table: generate_series
  FAIL CTE referenced twice in the recursive member: OperationalError: multiple recursive references: t
  FAIL aggregate in the recursive member: OperationalError: recursive aggregate queries not supported
  OK   'a' + 'b' (SQL Server style concatenation): [(0,)]
  OK   CAST in the anchor as MySQL needs it: length of the final path: [(17,)]
  OK   no default recursion cap: count to 1,000,000: [(1000000, 1000000)]
asserts passed
```

**Edge cases:**
- Things SQLite 3.45.1 refused or did differently in my run: the `CYCLE` and `SEARCH` clauses are syntax errors; `generate_series` is "no such table" (it exists in some builds as an extension, not in this one); the CTE name used twice in the recursive member (here inside `NOT IN (SELECT n FROM t)`) fails with `multiple recursive references`; an aggregate in the recursive member fails with `recursive aggregate queries not supported`. So "remember what I already visited" cannot be written as a subquery on the CTE itself; use a path string, or `UNION`.
- `'a' + 'b'` is `0` in SQLite (numeric addition of two non-numeric strings), so SQL Server style concatenation does not fail loudly, it silently returns a number. Use `||`.
- There is no built-in recursion cap in SQLite: a count to 1,000,000 ran in my run without any error. That is why a runaway query on SQLite keeps going until memory or a `LIMIT`, while SQL Server (100) and MySQL (1000) stop it with an error. The default caps are the reason a long chain can fail on SQL Server or MySQL with perfectly correct logic.
- `CAST(... AS CHAR(1))` does not truncate in SQLite (the final path was 17 characters long in my run); in MySQL the anchor's declared width matters, which is why the cast is there (hedged: MySQL behaviour from the opened docs, not executed).
- NULL manager (the CEO) is never joined from a child row, so in a subtree query it matters only for the anchor; ordering by `path` makes the output deterministic across engines (collation differences aside).
- Calendar spines: `generate_series` is the PostgreSQL way (not executed here) and the recursive CTE is the portable one; Part 6 Q31 (calendar table) shows both and `pd.date_range`.

**Then explain:**
- Common core: anchor member, `UNION ALL`, recursive member that joins the CTE to the table, a stop condition (empty result or a depth guard). That is portable; only the keyword, string join, type matching and caps change.
- SQL Server and MySQL want the recursive columns to have the anchor's type, which is the single most common portability failure with path strings (the anchor `name` is narrow, the path grows).
- Iteration caps are a safety net, not a design: a correct query on deep data needs the cap raised (`MAXRECURSION`, `cte_max_recursion_depth`), and a query with a cycle should be fixed with a guard rather than a larger cap.
- `CYCLE` and `SEARCH` in PostgreSQL 14+ replace the hand-written path-and-flag and the manual `ORDER BY path`; in SQLite and MySQL you write those by hand (Q8 shows the path guard).
- Oracle's `CONNECT BY` is a different model (a row source walked from `START WITH`, `PRIOR` marks the parent side), with built-in `LEVEL`, path and leaf functions; Oracle also supports a standard recursive `WITH` (stated from memory, not executed).
- pandas has no dialect problem, but it has its own guard: the visited set.

**Follow-ups:**
- Which engine would stop first on a 500-deep chain? SQL Server with its default 100 (hedged, not executed) and MySQL with 1000 would stop at their caps; SQLite would not stop.
- Can you do this in a view on SQL Server? The `MAXRECURSION` hint cannot be placed inside a view; it goes on the outer query (snippet, not executed).
- How do you make breadth-first output in SQLite? A recursive select with no `ORDER BY` is a FIFO queue (breadth-first); Q27 shows the queue order.

**Common mistakes:**
- Copying a PostgreSQL `CYCLE ...` query to SQLite and being surprised by a syntax error.
- Using `+` for strings in SQLite, or `||` in MySQL, and getting numbers or OR logic back.
- Forgetting the anchor `CAST` on MySQL or SQL Server, and getting truncation or a type-mismatch error when the path grows.
- Raising `MAXRECURSION 0` or the MySQL depth to hide a loop in the data.
- Claiming a dialect works because it looked right: only the SQLite lines in this answer were run.

### Q22 ⭐⭐ 🔴 Topological order and dependency resolution: tasks(task_id, depends_on) with one row per dependency and tasks with no dependency listed with depends_on NULL. Return a valid build order as 'stage' numbers (stage = longest chain of dependencies below the task, so independent tasks share a stage), and detect whether the graph has a cycle (some tasks never get a stage). Show the recursive CTE that propagates the stage as MAX(depth), why a DAG can have many paths to the same node, how the cycle check works (tasks missing from the result), and the Python graphlib.TopologicalSorter or networkx topological_generations equivalent with an assert.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Start the recursion from tasks that have no dependency (stage 0), let every dependent task inherit "depth + 1" from each of its prerequisites, take `MAX(depth)` per task because a DAG can reach the same task through several paths and the longest chain decides the stage, and flag a cycle by the tasks that never receive a stage; independent tasks then share a stage number.

**Schema and sample data:** one row per dependency, `depends_on` NULL for a task with no prerequisite. `tasks` is a DAG: A and F are free, B and C need A, D needs B and C (and the row `('D','B')` is loaded twice on purpose), E needs D and also A directly, G needs F. `tasks_cyc` has a pure loop (X and Y wait for each other, Z waits for Y). `tasks_mix` is the trap: X also depends on a normal task A, so the loop can be entered from a task that has a stage.
```sql
CREATE TABLE tasks(task_id TEXT, depends_on TEXT);
INSERT INTO tasks VALUES
 ('A',NULL),('F',NULL),('B','A'),('C','A'),('D','B'),('D','C'),('E','D'),('E','A'),('G','F'),('D','B');
-- X and Y wait for each other, Z waits for Y; none of them is reachable from a task without dependencies
CREATE TABLE tasks_cyc(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_cyc VALUES
 ('A',NULL),('B','A'),('X','Y'),('Y','X'),('Z','Y');
-- trap: X also depends on a normal task A, so the loop can be entered from a root
CREATE TABLE tasks_mix(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_mix VALUES
 ('A',NULL),('B','A'),('X','A'),('X','Y'),('Y','X'),('Z','Y');
```

**SQL answer:** `SQL_MAIN` in the Code block; run on the DAG, it is the stage per task:
```sql
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT task_id, MAX(depth) AS stage, COUNT(*) AS paths_seen
FROM stage
GROUP BY task_id
ORDER BY stage, task_id
```
Why `HAVING COUNT(depends_on) = 0` for the anchor: `COUNT(col)` skips NULLs, so a task whose only row has `depends_on` NULL has count 0 (no prerequisites); a task with at least one real dependency does not. The depth guard `s.depth < 50` is set above the number of tasks and exists only so a loop cannot run forever.

Which tasks never got a stage (`SQL_NOSTAGE` in the Code block, a plain anti-check on the result of the same CTE):
```sql
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT DISTINCT task_id FROM tasks
WHERE task_id NOT IN (SELECT task_id FROM stage)
ORDER BY task_id
```
A second, more reliable cycle check (`SQL_SELF_REACH`): walk "depends on" as a transitive closure with `UNION` (no depth column, so the set of `(start, cur)` pairs is finite and the query terminates by itself) and report the tasks that reach themselves:
```sql
WITH RECURSIVE w(start, cur) AS (
  SELECT task_id, depends_on FROM tasks WHERE depends_on IS NOT NULL
  UNION
  SELECT w.start, t.depends_on
  FROM w JOIN tasks t ON t.task_id = w.cur
  WHERE t.depends_on IS NOT NULL
)
SELECT DISTINCT start AS task_in_cycle FROM w WHERE cur = start ORDER BY 1
```

**pandas answer:** assign layers in a loop: a task is ready in round `r` when all its prerequisites already have a stage, and then its stage is `r`. That gives 1 + the largest prerequisite stage, which is the same longest-chain rule. Shown once here and identical to the Code block:
```py
def stages_pandas(tasks):
    edges = tasks.dropna(subset=["depends_on"]).drop_duplicates()
    nodes = set(tasks["task_id"])
    ndeps = edges.groupby("task_id").size()
    stage = {t: 0 for t in nodes - set(ndeps.index)}
    r = 0
    while True:
        r += 1
        e = edges[~edges["task_id"].isin(stage)]
        done = e["depends_on"].isin(stage).groupby(e["task_id"]).sum()
        ready = done[done == ndeps.reindex(done.index)].index
        if len(ready) == 0:
            break
        stage.update({t: r for t in ready})
    return pd.DataFrame({"task_id": list(stage), "stage": list(stage.values())})
```
Standard library and networkx versions (these are in the Code block and are asserted equal to the SQL stages): `graphlib.TopologicalSorter` with `prepare()`, then each `get_ready()` batch followed by `done(*batch)` gives one stage per batch; `networkx.topological_generations(G)` with edges prerequisite to task gives the same layers. Both were called as written at run time on Python 3.13 and networkx 3.6.1.

**Example:** DAG, stage by hand. A and F have no prerequisite: stage 0. B and C wait only for A, G waits only for F: stage 1. D waits for B and C (both stage 1): stage 2. E waits for D (stage 2) and for A (stage 0): the longest chain is A, B, D, E, so stage 3, not 1. The recursive CTE visits E four times (once through each dependency row: three rows reach D because `('D','B')` is duplicated, plus the direct `A` row), at depths 3, 3, 3 and 1, and `MAX(depth)` returns 3. The `paths_seen` column in the output is exactly that count: D has 3, E has 4. `MIN` or a plain `GROUP BY` without `MAX` would give a wrong build order.
Cycle: in `tasks_cyc`, X, Y and Z have no way in from stage 0, so they never appear in the CTE and `SQL_NOSTAGE` returns X, Y, Z; `SQL_SELF_REACH` returns only X and Y, because Z is stuck behind the loop but is not part of it.

**Code:** run with `python3 -I`. Compared after ordering by `stage, task_id`; the graphlib and networkx stage dictionaries are asserted equal to the SQL stages on the DAG; the cycle datasets are printed, not asserted equal, because that is the point.
```python
import sqlite3
from graphlib import TopologicalSorter, CycleError
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE tasks(task_id TEXT, depends_on TEXT);
INSERT INTO tasks VALUES
 ('A',NULL),('F',NULL),('B','A'),('C','A'),('D','B'),('D','C'),('E','D'),('E','A'),('G','F'),('D','B');
-- X and Y wait for each other, Z waits for Y; none of them is reachable from a task without dependencies
CREATE TABLE tasks_cyc(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_cyc VALUES
 ('A',NULL),('B','A'),('X','Y'),('Y','X'),('Z','Y');
-- trap: X also depends on a normal task A, so the loop can be entered from a root
CREATE TABLE tasks_mix(task_id TEXT, depends_on TEXT);
INSERT INTO tasks_mix VALUES
 ('A',NULL),('B','A'),('X','A'),('X','Y'),('Y','X'),('Z','Y');
"""
SQL_MAIN = """
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT task_id, MAX(depth) AS stage, COUNT(*) AS paths_seen
FROM stage
GROUP BY task_id
ORDER BY stage, task_id
"""
SQL_NOSTAGE = """
WITH RECURSIVE stage(task_id, depth) AS (
  SELECT task_id, 0 FROM tasks
  GROUP BY task_id
  HAVING COUNT(depends_on) = 0
  UNION ALL
  SELECT t.task_id, s.depth + 1
  FROM tasks t JOIN stage s ON t.depends_on = s.task_id
  WHERE s.depth < 50
)
SELECT DISTINCT task_id FROM tasks
WHERE task_id NOT IN (SELECT task_id FROM stage)
ORDER BY task_id
"""
SQL_SELF_REACH = """
WITH RECURSIVE w(start, cur) AS (
  SELECT task_id, depends_on FROM tasks WHERE depends_on IS NOT NULL
  UNION
  SELECT w.start, t.depends_on
  FROM w JOIN tasks t ON t.task_id = w.cur
  WHERE t.depends_on IS NOT NULL
)
SELECT DISTINCT start AS task_in_cycle FROM w WHERE cur = start ORDER BY 1
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

def swap(sql, table):
    return sql.replace("FROM tasks", f"FROM {table}").replace("JOIN tasks", f"JOIN {table}")

sql_dag = pd.read_sql_query(SQL_MAIN, con)
print("DAG: tasks with no stage:", [r[0] for r in con.execute(SQL_NOSTAGE)])
print("DAG, stage = longest chain below the task (paths_seen = rows the CTE produced for it):")
print(sql_dag.to_string(index=False))

# pd:main
def stages_pandas(tasks):
    edges = tasks.dropna(subset=["depends_on"]).drop_duplicates()
    nodes = set(tasks["task_id"])
    ndeps = edges.groupby("task_id").size()
    stage = {t: 0 for t in nodes - set(ndeps.index)}
    r = 0
    while True:
        r += 1
        e = edges[~edges["task_id"].isin(stage)]
        done = e["depends_on"].isin(stage).groupby(e["task_id"]).sum()
        ready = done[done == ndeps.reindex(done.index)].index
        if len(ready) == 0:
            break
        stage.update({t: r for t in ready})
    return pd.DataFrame({"task_id": list(stage), "stage": list(stage.values())})
# pd:end

tasks = pd.read_sql_query("SELECT * FROM tasks", con)
pd_dag = stages_pandas(tasks).sort_values(["stage", "task_id"]).reset_index(drop=True)
# compare after ordering by stage, task_id (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_dag, sql_dag[["task_id", "stage"]], check_dtype=False)
print("pandas layer loop equals SQL")

# graphlib: dependencies as {task: {what it waits for}}
deps = {}
for t, d in con.execute("SELECT task_id, depends_on FROM tasks").fetchall():
    deps.setdefault(t, set())
    if d is not None:
        deps[t].add(d)
ts = TopologicalSorter(deps)
ts.prepare()
gl, k = {}, 0
while ts.is_active():
    batch = ts.get_ready()
    for t in batch:
        gl[t] = k
    ts.done(*batch)
    k += 1
G = nx.DiGraph()
G.add_nodes_from(deps)
G.add_edges_from((d, t) for t, ds in deps.items() for d in ds)      # edge: prerequisite -> task
nxg = {t: i for i, gen in enumerate(nx.topological_generations(G)) for t in gen}
assert gl == nxg == dict(zip(sql_dag["task_id"], sql_dag["stage"]))
print("graphlib batches and networkx topological_generations equal the SQL stages")

for table in ("tasks_cyc", "tasks_mix"):
    q = swap(SQL_MAIN, table)
    got = pd.read_sql_query(q, con)
    print(f"\n{table}: stages from the recursive CTE (depth cap 50)")
    print(got.to_string(index=False))
    all_tasks = [r[0] for r in con.execute(f"SELECT DISTINCT task_id FROM {table} ORDER BY 1")]
    nostage = [r[0] for r in con.execute(swap(SQL_NOSTAGE, table))]
    assert nostage == sorted(set(all_tasks) - set(got["task_id"]))
    print("  tasks with no stage (SQL_NOSTAGE):", nostage)
    print("  tasks that reach themselves:", [r[0] for r in con.execute(swap(SQL_SELF_REACH, table))])
    t2 = pd.read_sql_query(f"SELECT * FROM {table}", con)
    s2 = stages_pandas(t2)
    print("  pandas layer loop stages:", dict(zip(s2["task_id"], s2["stage"])))
    d2 = {}
    for t, d in con.execute(f"SELECT task_id, depends_on FROM {table}").fetchall():
        d2.setdefault(t, set())
        if d is not None:
            d2[t].add(d)
    try:
        TopologicalSorter(d2).prepare()
    except CycleError as ex:
        print("  graphlib CycleError, cycle found:", ex.args[1])
    G2 = nx.DiGraph([(d, t) for t, ds in d2.items() for d in ds])
    try:
        list(nx.topological_generations(G2))
    except nx.NetworkXUnfeasible as ex:
        print("  networkx NetworkXUnfeasible:", ex)
    print("  networkx find_cycle:", nx.find_cycle(G2))
print("asserts passed")
```

**Output (my run):**
```text
DAG: tasks with no stage: []
DAG, stage = longest chain below the task (paths_seen = rows the CTE produced for it):
task_id  stage  paths_seen
      A      0           1
      F      0           1
      B      1           1
      C      1           1
      G      1           1
      D      2           3
      E      3           4
pandas layer loop equals SQL
graphlib batches and networkx topological_generations equal the SQL stages

tasks_cyc: stages from the recursive CTE (depth cap 50)
task_id  stage  paths_seen
      A      0           1
      B      1           1
  tasks with no stage (SQL_NOSTAGE): ['X', 'Y', 'Z']
  tasks that reach themselves: ['X', 'Y']
  pandas layer loop stages: {'A': 0, 'B': 1}
  graphlib CycleError, cycle found: ['X', 'Y', 'X']
  networkx NetworkXUnfeasible: Graph contains a cycle or graph changed during iteration
  networkx find_cycle: [('Y', 'X'), ('X', 'Y')]

tasks_mix: stages from the recursive CTE (depth cap 50)
task_id  stage  paths_seen
      A      0           1
      B      1           1
      X     49          25
      Z     49          24
      Y     50          25
  tasks with no stage (SQL_NOSTAGE): []
  tasks that reach themselves: ['X', 'Y']
  pandas layer loop stages: {'A': 0, 'B': 1}
  graphlib CycleError, cycle found: ['X', 'Y', 'X']
  networkx NetworkXUnfeasible: Graph contains a cycle or graph changed during iteration
  networkx find_cycle: [('X', 'Y'), ('Y', 'X')]
asserts passed
```

**Edge cases:**
- Loop reachable only from itself (`tasks_cyc`): the CTE returns stages for A and B only; X, Y and Z are missing. "Tasks missing from the result" is therefore the loop check, but it also lists tasks that are merely downstream of a loop (Z).
- The trap (`tasks_mix`): X depends on A and on Y. Starting from A, the CTE reaches X (A is a stage 0 task), then Y, then X again, and so on until my depth guard of 50 stops it. Result in my run: X 49, Z 49, Y 50, and no task is missing. So here the missing-task check says "no cycle" and gives stages that are nonsense (they are just the depth cap). The guard keeps the query finite but the answer wrong; the `SQL_SELF_REACH` closure finds X and Y in both datasets. The rule I state: stages from this CTE are only trustworthy after a cycle check that does not rely on the same CTE.
- The pandas layer loop is safer here: X and Y can never be ready (each waits for the other), so it returns only A and B on both cyclic datasets, and the missing tasks are the cycle and everything stuck behind it.
- Duplicate dependency rows: harmless for `MAX(depth)` (they inflate `paths_seen` only); the pandas loop uses `drop_duplicates` before counting prerequisites, otherwise `ready` would compare against an inflated count.
- Task with a prerequisite that has no row of its own as `task_id`: it would never get a stage in the CTE (nothing starts it). Normalise the input first so every prerequisite also appears as a task with a NULL-dependency row.
- Self dependency (`('W','W')`): a loop of length 1, found by `SQL_SELF_REACH` (start = cur) and never staged.
- graphlib raises `CycleError` (the cycle is in `args[1]`, printed above as `['X', 'Y', 'X']`) and networkx raises `NetworkXUnfeasible`; networkx `find_cycle` returns the loop edges. Those are the library versions of the cycle check.

**Then explain:**
- `stage` equals the length of the longest chain below the task; it is what a scheduler uses for "all tasks of one stage can run in parallel".
- A DAG can have many paths to the same node (E has four rows in the CTE). The recursive CTE enumerates paths, not nodes, so its cost grows with the number of paths: this is cheap on this toy graph and can explode on wide layered graphs (Q29 counts doubling paths).
- `MAX(depth)` over all paths is correct because every dependency must finish before the task: the slowest chain wins.
- The CTE propagates from stage 0 outward, so it never checks that a task's other prerequisites are done. In a DAG that does not matter (the longest chain covers them), in a graph with a loop it can give the wrong answer, as the mixed dataset shows.
- Recursion limits per engine, hedged and not executed: SQL Server `MAXRECURSION`, MySQL `cte_max_recursion_depth`; PostgreSQL 14+ has a `CYCLE` clause that marks loops for you (not executed).
- Window functions are not needed here (they belong to Parts 4-5).

**Follow-ups:**
- Return a full ordering and not stages? Order by `stage, task_id`; ties are free to run in parallel.
- What if a dependency points to a task that does not exist? Treat it as a data error and list it; with the CTE as written such a task is never staged, and `SQL_NOSTAGE` would show it.
- How would you stop a cycle inside the CTE? Add a path string and an `instr` guard, and keep `MAX(depth)`; the answer for tasks behind a loop is still undefined, so report them separately.

**Common mistakes:**
- Using `MIN(depth)` or taking the first row per task: stage ends up one too small for tasks with a long chain.
- Starting the anchor from every task (including ones with prerequisites): everything gets stage 0 rows and `MAX` is polluted.
- Counting a NULL `depends_on` as a dependency (use `COUNT(depends_on)`, not `COUNT(*)`).
- Trusting "no missing tasks" as proof of no cycle (the mixed dataset breaks it).
- Treating the depth guard value as a result (stage 49 or 50 above is a cap, not a stage).

### Q23 ⭐⭐ 🔴 Weighted shortest path with a cycle guard: roads(src, dst, km) on a small directed graph with a loop and two competing routes from 'A' to 'F'. Return the cheapest path with its path string and total km by enumerating all simple paths (path-string guard) and taking the minimum, then explain why this enumeration is exponential in the worst case, why a plain depth limit is not enough to be correct with cycles of negative or zero weight, and how Dijkstra differs (visited set with a priority queue, not expressible with plain recursion without extras). Check the answer with networkx shortest_path (installed here; scipy is not) and a hand-written heapq Dijkstra, asserting all agree.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Enumerate every simple path from A with a path-string guard (never step to a node already in the path), keep the ones that end at F, and take the smallest total; that is correct but exponential in the worst case, a plain depth limit is not a correct guard once a cycle has zero or negative weight, and the real shortest-path algorithm is Dijkstra (priority queue plus a visited set, no negative edges), which I cross-check with `heapq` and networkx.

**Schema and sample data:** nine directed roads between A and F. Two competing families of routes: through B (A to B costs 2) or straight to C (cost 5), a loop between B and C (`B>C` costs 1, `C>B` costs 1), then C or B to D, then D to F directly (6) or via E (1 + 2). `roads_neg` is the same graph with `C>B` set to -3, so the loop B, C, B costs -2 each time round.
```sql
CREATE TABLE roads(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads VALUES
 ('A','B',2),('A','C',5),('B','C',1),('C','B',1),('B','D',7),('C','D',2),
 ('D','E',1),('D','F',6),('E','F',2);
-- same graph but the road C to B has a negative weight (a refund or a downhill credit), so B-C-B costs -2 per loop
CREATE TABLE roads_neg(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads_neg SELECT src, dst, CASE WHEN src = 'C' AND dst = 'B' THEN -3 ELSE km END FROM roads;
```

**SQL answer:** `SQL_MAIN` in the Code block; it returns all simple routes ordered by cost, so the first row is the cheapest:
```sql
WITH RECURSIVE p(node, path, km, legs) AS (
  SELECT 'A', ',A,', 0, 0
  UNION ALL
  SELECT r.dst, p.path || r.dst || ',', p.km + r.km, p.legs + 1
  FROM p JOIN roads r ON r.src = p.node
  WHERE instr(p.path, ',' || r.dst || ',') = 0
)
SELECT trim(path, ',') AS route, km, legs
FROM p
WHERE node = 'F'
ORDER BY km, route
```
The path is stored as `,A,B,` with commas around each node so that `instr(path, ',B,')` cannot match inside a longer name (`AB` versus `B`). `ORDER BY km, route` makes ties deterministic.

**pandas answer:** a frontier of partial paths; each iteration merges the frontier with the edge list on `node = src`, drops the extensions whose `dst` is already in the route, and collects the rows that reached F. Shown once here and identical to the Code block:
```py
paths = pd.DataFrame({"node": ["A"], "route": ["A"], "km": [0], "legs": [0]})
found = []
while len(paths):
    nxt = paths.merge(roads, left_on="node", right_on="src")
    fresh = pd.Series([d not in r.split(">") for d, r in zip(nxt["dst"], nxt["route"])], index=nxt.index, dtype=bool)
    nxt = nxt[fresh]
    paths = pd.DataFrame({"node": nxt["dst"], "route": nxt["route"] + ">" + nxt["dst"],
                          "km": nxt["km"] + nxt["w"], "legs": nxt["legs"] + 1})
    found.append(paths[paths["node"] == "F"])
pd_df = (pd.concat(found)[["route", "km", "legs"]]
           .sort_values(["km", "route"]).reset_index(drop=True))
```
Dijkstra with `heapq` and `networkx.shortest_path`/`shortest_path_length` with `weight='km'` are in the Code block; the asserts compare route and distance across SQL, `heapq` and networkx.

**Example:** from A: routes reaching F by hand. A, B, C, D, E, F costs 2+1+2+1+2 = 8. A, C, D, E, F costs 5+2+1+2 = 10. A, B, C, D, F costs 2+1+2+6 = 11. A, B, D, E, F costs 2+7+1+2 = 12. A, C, D, F is 13, A, B, D, F is 15, and the two routes that use the `C>B` road (A, C, B, D, E, F and A, C, B, D, F) cost 16 and 19. That is 8 simple routes; the cheapest is A>B>C>D>E>F at 8 km over 5 legs, even though it has the most legs: fewest legs and cheapest are different questions. The loop B to C to B is never walked twice because the path guard blocks revisiting B (or C) inside one route.

**Code:** run with `python3 -I`. Compared after ordering by `km, route`; the cheapest route and km are asserted equal across SQL, the pandas frontier merge, a hand-written `heapq` Dijkstra and `networkx.shortest_path` / `shortest_path_length`.
```python
import heapq
import sqlite3
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE roads(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads VALUES
 ('A','B',2),('A','C',5),('B','C',1),('C','B',1),('B','D',7),('C','D',2),
 ('D','E',1),('D','F',6),('E','F',2);
-- same graph but the road C to B has a negative weight (a refund or a downhill credit), so B-C-B costs -2 per loop
CREATE TABLE roads_neg(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads_neg SELECT src, dst, CASE WHEN src = 'C' AND dst = 'B' THEN -3 ELSE km END FROM roads;
"""
SQL_MAIN = """
WITH RECURSIVE p(node, path, km, legs) AS (
  SELECT 'A', ',A,', 0, 0
  UNION ALL
  SELECT r.dst, p.path || r.dst || ',', p.km + r.km, p.legs + 1
  FROM p JOIN roads r ON r.src = p.node
  WHERE instr(p.path, ',' || r.dst || ',') = 0
)
SELECT trim(path, ',') AS route, km, legs
FROM p
WHERE node = 'F'
ORDER BY km, route
"""
SQL_NODEPTH = """
WITH RECURSIVE w(node, km, legs) AS (
  SELECT 'A', 0, 0
  UNION ALL
  SELECT r.dst, w.km + r.km, w.legs + 1
  FROM w JOIN roads_t r ON r.src = w.node
  WHERE w.legs < {cap}
)
SELECT COUNT(*) AS walks_to_F, MIN(km) AS cheapest_km FROM w WHERE node = 'F'
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_df["route"] = sql_df["route"].str.replace(",", ">")
print("All simple routes A to F, cheapest first (SQL path-string guard):")
print(sql_df.to_string(index=False))

roads = pd.read_sql_query("SELECT src, dst, km AS w FROM roads", con)

# pd:main
paths = pd.DataFrame({"node": ["A"], "route": ["A"], "km": [0], "legs": [0]})
found = []
while len(paths):
    nxt = paths.merge(roads, left_on="node", right_on="src")
    fresh = pd.Series([d not in r.split(">") for d, r in zip(nxt["dst"], nxt["route"])], index=nxt.index, dtype=bool)
    nxt = nxt[fresh]
    paths = pd.DataFrame({"node": nxt["dst"], "route": nxt["route"] + ">" + nxt["dst"],
                          "km": nxt["km"] + nxt["w"], "legs": nxt["legs"] + 1})
    found.append(paths[paths["node"] == "F"])
pd_df = (pd.concat(found)[["route", "km", "legs"]]
           .sort_values(["km", "route"]).reset_index(drop=True))
# pd:end
# compare after ordering by km, route (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas frontier merge equals SQL:", len(pd_df), "simple routes")

def dijkstra(edges, source, target):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    best, heap = {source: 0}, [(0, source, [source])]
    done = set()
    while heap:
        d, u, route = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        if u == target:
            return d, ">".join(route)
        for v, w in graph.get(u, []):
            if v not in done and d + w < best.get(v, float("inf")):
                best[v] = d + w
                heapq.heappush(heap, (d + w, v, route + [v]))
    return None

edges = con.execute("SELECT src, dst, km FROM roads").fetchall()
dj_km, dj_route = dijkstra(edges, "A", "F")
G = nx.DiGraph()
G.add_weighted_edges_from(edges, weight="km")
nx_route = ">".join(nx.shortest_path(G, "A", "F", weight="km"))
nx_km = nx.shortest_path_length(G, "A", "F", weight="km")
best = sql_df.iloc[0]
assert (best["route"], best["km"]) == (dj_route, dj_km) == (nx_route, nx_km)
print("cheapest: SQL", (best["route"], int(best["km"])), "| heapq Dijkstra", (dj_route, dj_km), "| networkx", (nx_route, nx_km))

print("\nDepth limit only (no path guard), cheapest walk from A to F and number of walks, by leg cap:")
for table in ("roads", "roads_neg"):
    rows = []
    for cap in (4, 6, 8, 10, 12):
        n, m = con.execute(SQL_NODEPTH.replace("roads_t", table).format(cap=cap)).fetchone()
        rows.append((cap, n, m))
    print(f"  {table}:", rows, "(cap, walks_to_F, cheapest_km)")

neg = nx.DiGraph()
neg.add_weighted_edges_from(con.execute("SELECT src, dst, km FROM roads_neg").fetchall(), weight="km")
print("networkx negative_edge_cycle on roads_neg:", nx.negative_edge_cycle(neg, weight="km"))
try:
    nx.bellman_ford_path(neg, "A", "F", weight="km")
except nx.NetworkXUnbounded as ex:
    print("networkx bellman_ford_path raises NetworkXUnbounded:", ex)
try:
    print("networkx dijkstra on the negative cycle returns:", nx.dijkstra_path(neg, "A", "F", weight="km"))
except Exception as ex:
    print("networkx dijkstra raises", type(ex).__name__, ex)

import time
print("\nSimple-path enumeration on a chain of k diamonds (2 routes per diamond), SQL path-string guard:")
for k in (6, 10, 14):
    d = []
    for i in range(k):
        d += [(f"s{i}", f"a{i}", 1), (f"s{i}", f"b{i}", 1), (f"a{i}", f"s{i+1}", 1), (f"b{i}", f"s{i+1}", 1)]
    con.execute("DROP TABLE IF EXISTS dia")
    con.execute("CREATE TABLE dia(src TEXT, dst TEXT, km INTEGER)")
    con.executemany("INSERT INTO dia VALUES (?, ?, ?)", d)
    q = SQL_MAIN.replace("'A'", "'s0'").replace("roads", "dia").replace("node = 'F'", f"node = 's{k}'")
    t0 = time.perf_counter()
    n = con.execute(f"SELECT COUNT(*) FROM ({q.replace(chr(10) + 'ORDER BY km, route', '')})").fetchone()[0]
    print(f"  k={k:2d}: {n} simple routes (2^k = {2**k}), {len(d)} edges, {time.perf_counter() - t0:.3f} s on this machine")
print("asserts passed")
```

**Output (my run):**
```text
All simple routes A to F, cheapest first (SQL path-string guard):
      route  km  legs
A>B>C>D>E>F   8     5
  A>C>D>E>F  10     4
  A>B>C>D>F  11     4
  A>B>D>E>F  12     4
    A>C>D>F  13     3
    A>B>D>F  15     3
A>C>B>D>E>F  16     5
  A>C>B>D>F  19     4
pandas frontier merge equals SQL: 8 simple routes
cheapest: SQL ('A>B>C>D>E>F', 8) | heapq Dijkstra ('A>B>C>D>E>F', 8) | networkx ('A>B>C>D>E>F', 8)

Depth limit only (no path guard), cheapest walk from A to F and number of walks, by leg cap:
  roads: [(4, 6, 10), (6, 14, 8), (8, 22, 8), (10, 30, 8), (12, 38, 8)] (cap, walks_to_F, cheapest_km)
  roads_neg: [(4, 6, 10), (6, 14, 8), (8, 22, 6), (10, 30, 4), (12, 38, 2)] (cap, walks_to_F, cheapest_km)
networkx negative_edge_cycle on roads_neg: True
networkx bellman_ford_path raises NetworkXUnbounded: Negative cycle detected.
networkx dijkstra raises ValueError ('Contradictory paths found:', 'negative weights?')

Simple-path enumeration on a chain of k diamonds (2 routes per diamond), SQL path-string guard:
  k= 6: 64 simple routes (2^k = 64), 24 edges, 0.000 s on this machine
  k=10: 1024 simple routes (2^k = 1024), 40 edges, 0.004 s on this machine
  k=14: 16384 simple routes (2^k = 16384), 56 edges, 0.071 s on this machine
asserts passed
```

**Edge cases:**
- Depth limit only, no path guard (the `Depth limit only` block in the output): on `roads` the number of walks keeps growing with the cap (6, 14, 22, 30, 38 walks for caps 4, 6, 8, 10, 12) while the cheapest cost stays 8 once the cap reaches 6. A depth limit therefore terminates, but it counts repeated-node walks and costs time; on positive weights the minimum is still right once the cap is big enough.
- With the negative loop (`roads_neg`) the minimum is not stable: cheapest walk cost 10, 8, 6, 4, 2 for caps 4, 6, 8, 10, 12. Every extra lap of B, C, B lowers the cost by 2, so no cap gives "the" answer. That is why a depth limit is not enough when a cycle has negative total weight, and a zero-weight cycle gives infinitely many walks of equal cost (the cost is fine, the row count is not). The path guard answers a different, well-defined question (cheapest simple path), but even that is hard in general with negative edges and is not what Dijkstra computes.
- networkx behaviour I ran: `negative_edge_cycle` returned `True` on `roads_neg`, `bellman_ford_path` raised `NetworkXUnbounded` ("Negative cycle detected."), and `dijkstra_path` raised `ValueError` ("Contradictory paths found: negative weights?"), meaning Dijkstra on negative edges can fail loudly or, on other graphs, return a wrong path without an error (I did not test a silent case here).
- Ties: two routes with the same cost both appear; `ORDER BY km, route` picks the alphabetically first. Dijkstra and networkx may return either of two tied routes; the assert is on this graph where the cheapest is unique.
- No route (target unreachable): the SQL returns no rows, `dijkstra` returns `None` in my function, networkx raises `NetworkXNoPath` (from memory of its documentation, not run here); handle the empty case explicitly.
- Edge direction: the data is directed; for two-way roads insert both directions or the search will miss routes.

**Then explain:**
- Why the enumeration is exponential: every branch point multiplies the number of simple paths. A chain of k diamonds (two routes per diamond) has 2^k simple paths: in my run 64, 1,024 and 16,384 routes for k = 6, 10 and 14 (SQL path guard, last block of the output; the elapsed times printed there are from this machine only). On a dense graph the count is worse than exponential in the number of nodes.
- Dijkstra: keep the best-known distance for each node, always settle the unsettled node with the smallest distance (priority queue), never revisit a settled node; with non-negative weights each node is settled once, so it is about O((V+E) log V). It stores one distance per node, not one row per path.
- Why plain recursion cannot do Dijkstra: the recursive member cannot reference the CTE twice (SQLite fails with `multiple recursive references`, checked in Q21), cannot use aggregates over the CTE, and cannot "settle" a node because the working table is a queue of all rows, not a priority queue with a visited set. You can approximate by keeping `MIN(km)` per node after a depth cap, which is a Bellman-Ford style relaxation, not Dijkstra; I did not run that here.
- A depth limit is a safety net; a path guard (or `UNION` on node) is correctness for cycles. Use both in practice: the guard for correctness, the cap for safety.
- Other engines: PostgreSQL 14+ `CYCLE` clause and SQL Server `MAXRECURSION` / MySQL `cte_max_recursion_depth` caps exist (hedged, not executed).

**Follow-ups:**
- Fewest legs instead of cheapest? Order by `legs` (BFS), then `km`.
- Shortest path for all pairs on a large graph? Not in SQL; use a graph library or a graph database (not covered here; scipy is not installed in this environment, networkx is).
- Why did you not use `UNION` to dedupe? `UNION` removes duplicate rows only; rows with different paths or costs are different rows, so it does not prevent walks around a loop.

**Common mistakes:**
- Substring matching without delimiters (`instr(path, 'B')` also matches `BLR`).
- Using only a depth cap and calling the minimum "the shortest path" when a cheaper loop exists.
- Forgetting the graph is directed, or adding reverse edges that were not roads.
- Ordering by `legs` and calling it cheapest.
- Presenting enumeration as scalable: it is exponential in the worst case.

### Q24 ⭐ 🟡 Hierarchy storage models at concept level: adjacency list (parent_id), materialized path ('/1/4/9/'), nested sets (lft, rgt) and closure table (ancestor, descendant, depth). For one 8-node category tree load all four models in SQLite and write the same query in each: all descendants of node 4, the ancestors of node 9, the depth of each node and the move of a subtree, stating the read and write cost, the integrity risk and the index needed for each. Say which you would pick for a read-heavy catalogue, a comment thread with frequent inserts and a deep, frequently changing org chart. The trade-offs are rules of thumb, not benchmarks.
**Asked at:** hierarchy storage-model guides (search snippets only, not opened: Medium 'From Trees to Tables', jopr, oneuptime MySQL hierarchical schema, dev.to PostgreSQL ltree versus adjacency versus closure table; adjacency is simplest but needs recursion, nested sets fast reads and costly writes, materialized path prefix queries, closure table all pairs with O(n squared) worst-case rows); blog posts, not candidate reports; data modelling and backend-adjacent analyst rounds
**Say this first (1 line):** I load the same tree four ways and run the same questions in each: adjacency list (simple writes, needs recursion to read), materialized path (prefix queries, a subtree move rewrites every path below it), nested sets (very fast subtree reads, an insert or move renumbers many rows) and closure table (every ancestor-descendant pair stored, fast reads both ways, more rows and more write work); the costs I give are rules of thumb from blogs, not benchmarks, and the only numbers here are row counts and query plans I ran.

**Schema and sample data:** premise check: the question says an 8-node tree and also asks for the ancestors of node 9, so the ids cannot be 1 to 8. I use eight nodes with ids 1, 2, 3, 4, 5, 6, 7 and 9 (id 8 was "deleted earlier"), a realistic id gap. Tree: Root(1) has Electronics(2) and Books(3); Electronics has Phones(4) and Laptops(5); Books has Fiction(6); Phones has iOS(7) and Android(9).
```sql
CREATE TABLE adj(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO adj VALUES
 (1,NULL,'Root'),(2,1,'Electronics'),(3,1,'Books'),(4,2,'Phones'),(5,2,'Laptops'),
 (6,3,'Fiction'),(7,4,'iOS'),(9,4,'Android');
```
The other three models are built from the adjacency table (`BUILD` in the Code block creates `mat` (path text) and `closure` (ancestor, descendant, depth, self rows included) with recursive CTEs; nested set numbers `lft`/`rgt` come from a small depth-first walk in Python, children in id order):
```sql
CREATE TABLE mat(id INTEGER PRIMARY KEY, path TEXT);
INSERT INTO mat
WITH RECURSIVE t(id, path) AS (
  SELECT id, '/' || id || '/' FROM adj WHERE parent_id IS NULL
  UNION ALL
  SELECT a.id, t.path || a.id || '/' FROM adj a JOIN t ON a.parent_id = t.id
)
SELECT id, path FROM t;
CREATE TABLE closure(ancestor INTEGER, descendant INTEGER, depth INTEGER, PRIMARY KEY (ancestor, descendant));
INSERT INTO closure
WITH RECURSIVE c(ancestor, descendant, depth) AS (
  SELECT id, id, 0 FROM adj
  UNION ALL
  SELECT c.ancestor, a.id, c.depth + 1 FROM c JOIN adj a ON a.parent_id = c.descendant
)
SELECT ancestor, descendant, depth FROM c;
CREATE INDEX closure_desc ON closure(descendant, ancestor);
```

**SQL answer:** the same three questions in four dialects of the schema (all in the dict `Q` in the Code block, asserted equal to each other; node 4 for descendants, node 9 for ancestors):
- Adjacency list: recursive CTE down for descendants (`SELECT id FROM adj WHERE parent_id = 4` then join on `parent_id = d.id`), recursive CTE up for ancestors (join `a.id = u.parent_id`), recursive CTE from the root for depth. Move: `UPDATE adj SET parent_id = 3 WHERE id = 4`, one row.
- Materialized path: descendants `n.path LIKE t.path || '%'` (plus `n.id <> 4`), ancestors `t.path LIKE a.path || '%'`, depth is the number of slashes minus 2. The trailing slash in the path matters: `/1/2/4/` cannot match `/1/2/40/`. Move:
```sql
UPDATE mat SET path = '/1/3/' || substr(path, length('/1/2/') + 1)
WHERE path LIKE '/1/2/4/%'
```
- Nested sets: descendants `n.lft > t.lft AND n.rgt < t.rgt`, ancestors `a.lft < t.lft AND a.rgt > t.rgt`, depth is a count of ancestors. Move: renumber; I rebuild the numbers in Python and count what changed, since the pure SQL shift is a multi-statement script (not shown, not executed).
- Closure table: descendants `ancestor = 4 AND depth > 0`, ancestors `descendant = 9 AND depth > 0`, depth is the `depth` column from the root's rows. Move is two statements:
```sql
DELETE FROM closure
WHERE descendant IN (SELECT descendant FROM closure WHERE ancestor = 4)
  AND ancestor IN (SELECT ancestor FROM closure WHERE descendant = 4 AND ancestor <> 4)
```
```sql
INSERT INTO closure
SELECT sup.ancestor, sub.descendant, sup.depth + sub.depth + 1
FROM closure sup, closure sub
WHERE sup.descendant = 3 AND sub.ancestor = 4
```
Statement 1 removes the links between the moved subtree and its old ancestors above it (not the links inside the subtree); statement 2 links the moved subtree to the new parent and all of the new parent's ancestors, with depth adding up.

**pandas answer:** the path model and the pair model, built in pandas from the adjacency frame and checked against the SQL results. Shown once here and identical to the Code block:
```py
parent = dict(zip(adj["id"], adj["parent_id"]))
def chain(i):
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out[::-1]
paths = pd.Series({i: "/" + "/".join(map(str, chain(i))) + "/" for i in adj["id"]}).rename_axis("id").rename("path").reset_index()
p4 = paths.loc[paths["id"] == 4, "path"].item()
p9 = paths.loc[paths["id"] == 9, "path"].item()
pd_desc = paths.loc[paths["path"].str.startswith(p4) & (paths["id"] != 4), "id"].sort_values().tolist()
pd_anc = sorted(int(x) for x in p9.strip("/").split("/") if int(x) != 9)
pd_depth = dict(zip(paths["id"], paths["path"].str.count("/") - 2))
pairs = pd.DataFrame([(a, i, k) for i in adj["id"] for k, a in enumerate(chain(i)[::-1])],
                     columns=["ancestor", "descendant", "depth"])
```

**Example:** the path column for node 9 is `/1/2/4/9/`, so its ancestors are the ids in the path before it (1, 2, 4), its depth is 4 slashes minus 2 = 3 (Root is depth 0), and the descendants of 4 are the rows whose path starts with `/1/2/4/` other than 4 itself (7 and 9). In nested sets the numbers from the walk are 1(1,16), 2(2,11), 4(3,8), 7(4,5), 9(6,7), 5(9,10), 3(12,15), 6(13,14); node 4 is (3,8), so descendants are nodes with `lft > 3 and rgt < 8`, which are 7 (4,5) and 9 (6,7), and the ancestors of 9 (6,7) are the nodes with `lft < 6 and rgt > 7`, which are 1, 2 and 4. In the closure table 22 rows exist: 8 self rows plus one per ancestor-descendant pair (depths 0, 1, 1, 2, 2, 2, 3, 3 sum to 14). Moving subtree 4 (nodes 4, 7, 9) under 3: adjacency changes 1 row; materialized path changes 3 paths; the closure table deletes 6 rows (3 nodes times 2 old ancestors, 1 and 2) and inserts 6 (3 nodes times 2 new ancestors, 3 and 1); nested sets changed 6 of 8 rows in my rebuild. After the move all four models agree again: ancestors of 9 are 1, 3 and 4 and its depth is still 3.

**Code:** run with `python3 -I`. It builds the four models, asserts that all three questions give identical results across them before and after the move, asserts the pandas path/prefix and pair frames equal the SQL results, prints the number of rows each move changed, and prints `EXPLAIN QUERY PLAN` for the path-prefix lookup.
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE adj(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO adj VALUES
 (1,NULL,'Root'),(2,1,'Electronics'),(3,1,'Books'),(4,2,'Phones'),(5,2,'Laptops'),
 (6,3,'Fiction'),(7,4,'iOS'),(9,4,'Android');
"""
BUILD = """
CREATE TABLE mat(id INTEGER PRIMARY KEY, path TEXT);
INSERT INTO mat
WITH RECURSIVE t(id, path) AS (
  SELECT id, '/' || id || '/' FROM adj WHERE parent_id IS NULL
  UNION ALL
  SELECT a.id, t.path || a.id || '/' FROM adj a JOIN t ON a.parent_id = t.id
)
SELECT id, path FROM t;
CREATE TABLE closure(ancestor INTEGER, descendant INTEGER, depth INTEGER, PRIMARY KEY (ancestor, descendant));
INSERT INTO closure
WITH RECURSIVE c(ancestor, descendant, depth) AS (
  SELECT id, id, 0 FROM adj
  UNION ALL
  SELECT c.ancestor, a.id, c.depth + 1 FROM c JOIN adj a ON a.parent_id = c.descendant
)
SELECT ancestor, descendant, depth FROM c;
CREATE INDEX closure_desc ON closure(descendant, ancestor);
"""
Q = {
 "adjacency": {
  "desc": """WITH RECURSIVE d(id) AS (SELECT id FROM adj WHERE parent_id = 4
             UNION ALL SELECT a.id FROM adj a JOIN d ON a.parent_id = d.id) SELECT id FROM d ORDER BY id""",
  "anc": """WITH RECURSIVE u(id, parent_id) AS (SELECT id, parent_id FROM adj WHERE id = 9
            UNION ALL SELECT a.id, a.parent_id FROM adj a JOIN u ON a.id = u.parent_id)
            SELECT id FROM u WHERE id <> 9 ORDER BY id""",
  "depth": """WITH RECURSIVE t(id, depth) AS (SELECT id, 0 FROM adj WHERE parent_id IS NULL
              UNION ALL SELECT a.id, t.depth + 1 FROM adj a JOIN t ON a.parent_id = t.id)
              SELECT id, depth FROM t ORDER BY id"""},
 "materialized path": {
  "desc": "SELECT n.id FROM mat n, mat t WHERE t.id = 4 AND n.path LIKE t.path || '%' AND n.id <> 4 ORDER BY n.id",
  "anc": "SELECT a.id FROM mat a, mat t WHERE t.id = 9 AND t.path LIKE a.path || '%' AND a.id <> 9 ORDER BY a.id",
  "depth": "SELECT id, length(path) - length(replace(path, '/', '')) - 2 AS depth FROM mat ORDER BY id"},
 "nested sets": {
  "desc": "SELECT n.id FROM ns n, ns t WHERE t.id = 4 AND n.lft > t.lft AND n.rgt < t.rgt ORDER BY n.id",
  "anc": "SELECT a.id FROM ns a, ns t WHERE t.id = 9 AND a.lft < t.lft AND a.rgt > t.rgt ORDER BY a.id",
  "depth": "SELECT n.id, (SELECT COUNT(*) FROM ns a WHERE a.lft < n.lft AND a.rgt > n.rgt) AS depth FROM ns n ORDER BY n.id"},
 "closure table": {
  "desc": "SELECT descendant FROM closure WHERE ancestor = 4 AND depth > 0 ORDER BY descendant",
  "anc": "SELECT ancestor FROM closure WHERE descendant = 9 AND depth > 0 ORDER BY ancestor",
  "depth": "SELECT descendant, depth FROM closure WHERE ancestor = 1 ORDER BY descendant"},
}
MOVE_MAT = """
UPDATE mat SET path = '/1/3/' || substr(path, length('/1/2/') + 1)
WHERE path LIKE '/1/2/4/%'
"""
MOVE_CLOSURE_DELETE = """
DELETE FROM closure
WHERE descendant IN (SELECT descendant FROM closure WHERE ancestor = 4)
  AND ancestor IN (SELECT ancestor FROM closure WHERE descendant = 4 AND ancestor <> 4)
"""
MOVE_CLOSURE_INSERT = """
INSERT INTO closure
SELECT sup.ancestor, sub.descendant, sup.depth + sub.depth + 1
FROM closure sup, closure sub
WHERE sup.descendant = 3 AND sub.ancestor = 4
"""

def build_nested_sets(con):
    kids = {}
    for i, p in con.execute("SELECT id, parent_id FROM adj ORDER BY id"):
        kids.setdefault(p, []).append(i)
    out, counter = [], [0]
    def visit(i):
        counter[0] += 1
        lft = counter[0]
        for c in kids.get(i, []):
            visit(c)
        counter[0] += 1
        out.append((i, lft, counter[0]))
    visit(kids[None][0])
    con.execute("DROP TABLE IF EXISTS ns")
    con.execute("CREATE TABLE ns(id INTEGER PRIMARY KEY, lft INTEGER, rgt INTEGER)")
    con.executemany("INSERT INTO ns VALUES (?, ?, ?)", out)

def run_all(con):
    return {m: {k: con.execute(q).fetchall() for k, q in qs.items()} for m, qs in Q.items()}

def agree(res):
    base = res["adjacency"]
    for m, r in res.items():
        assert r == base, (m, r, base)

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.executescript(BUILD)
build_nested_sets(con)
print("nested sets (id, lft, rgt):", con.execute("SELECT * FROM ns ORDER BY lft").fetchall())
print("materialized paths:", con.execute("SELECT id, path FROM mat ORDER BY id").fetchall())
print("closure rows:", con.execute("SELECT COUNT(*) FROM closure").fetchone()[0], "for 8 nodes (8 self rows + one per ancestor-descendant pair)")
before = run_all(con)
agree(before)
print("\nBefore the move, the four models agree. descendants of 4:", [r[0] for r in before["adjacency"]["desc"]],
      "| ancestors of 9:", [r[0] for r in before["adjacency"]["anc"]])
print("depth by id:", dict(before["adjacency"]["depth"]))

# pandas: adjacency walk for paths, then prefix tests on the path column and pair rows for the closure
adj = pd.read_sql_query("SELECT * FROM adj", con)
adj["parent_id"] = adj["parent_id"].astype("Int64")

# pd:main
parent = dict(zip(adj["id"], adj["parent_id"]))
def chain(i):
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out[::-1]
paths = pd.Series({i: "/" + "/".join(map(str, chain(i))) + "/" for i in adj["id"]}).rename_axis("id").rename("path").reset_index()
p4 = paths.loc[paths["id"] == 4, "path"].item()
p9 = paths.loc[paths["id"] == 9, "path"].item()
pd_desc = paths.loc[paths["path"].str.startswith(p4) & (paths["id"] != 4), "id"].sort_values().tolist()
pd_anc = sorted(int(x) for x in p9.strip("/").split("/") if int(x) != 9)
pd_depth = dict(zip(paths["id"], paths["path"].str.count("/") - 2))
pairs = pd.DataFrame([(a, i, k) for i in adj["id"] for k, a in enumerate(chain(i)[::-1])],
                     columns=["ancestor", "descendant", "depth"])
# pd:end
assert pd_desc == [r[0] for r in before["adjacency"]["desc"]]
assert pd_anc == [r[0] for r in before["adjacency"]["anc"]]
assert pd_depth == dict(before["adjacency"]["depth"])
sql_pairs = pd.read_sql_query("SELECT ancestor, descendant, depth FROM closure ORDER BY ancestor, descendant", con)
pd.testing.assert_frame_equal(pairs.sort_values(["ancestor", "descendant"]).reset_index(drop=True), sql_pairs, check_dtype=False)
print("pandas path, prefix and pair frames equal the SQL results (pairs compared after sorting by ancestor, descendant)")

# the move: subtree 4 goes under 3
changes = {}
con.execute("UPDATE adj SET parent_id = 3 WHERE id = 4")
changes["adjacency"] = con.execute("SELECT changes()").fetchone()[0]
con.execute(MOVE_MAT)
changes["materialized path"] = con.execute("SELECT changes()").fetchone()[0]
old_ns = dict((i, (l, r)) for i, l, r in con.execute("SELECT * FROM ns"))
build_nested_sets(con)
new_ns = dict((i, (l, r)) for i, l, r in con.execute("SELECT * FROM ns"))
changes["nested sets (rebuild)"] = sum(old_ns[i] != new_ns[i] for i in old_ns)
con.execute(MOVE_CLOSURE_DELETE)
deleted = con.execute("SELECT changes()").fetchone()[0]
con.execute(MOVE_CLOSURE_INSERT)
inserted = con.execute("SELECT changes()").fetchone()[0]
changes["closure table"] = f"{deleted} deleted + {inserted} inserted"
after = run_all(con)
agree(after)
print("\nAfter moving 4 under 3 the four models still agree. ancestors of 9 now:", [r[0] for r in after["adjacency"]["anc"]],
      "| depth of 9 now:", dict(after["adjacency"]["depth"])[9])
print("rows changed by the move:", changes)
print("nested sets after:", sorted(new_ns.items()))

print("\nEXPLAIN QUERY PLAN for the materialized-path prefix lookup:")
con.execute("CREATE INDEX mat_path ON mat(path)")
for label, q in [("LIKE on a default-collation index", "SELECT id FROM mat WHERE path LIKE '/1/3/4/%'"),
                 ("range on the same index", "SELECT id FROM mat WHERE path >= '/1/3/4/' AND path < '/1/3/40'")]:
    print(" ", label, "->", [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q)])
con.execute("DROP INDEX mat_path")
con.execute("CREATE INDEX mat_path ON mat(path COLLATE NOCASE)")
print("  LIKE on a NOCASE index ->", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT id FROM mat WHERE path LIKE '/1/3/4/%'")])
print("asserts passed")
```

**Output (my run):**
```text
nested sets (id, lft, rgt): [(1, 1, 16), (2, 2, 11), (4, 3, 8), (7, 4, 5), (9, 6, 7), (5, 9, 10), (3, 12, 15), (6, 13, 14)]
materialized paths: [(1, '/1/'), (2, '/1/2/'), (3, '/1/3/'), (4, '/1/2/4/'), (5, '/1/2/5/'), (6, '/1/3/6/'), (7, '/1/2/4/7/'), (9, '/1/2/4/9/')]
closure rows: 22 for 8 nodes (8 self rows + one per ancestor-descendant pair)

Before the move, the four models agree. descendants of 4: [7, 9] | ancestors of 9: [1, 2, 4]
depth by id: {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 9: 3}
pandas path, prefix and pair frames equal the SQL results (pairs compared after sorting by ancestor, descendant)

After moving 4 under 3 the four models still agree. ancestors of 9 now: [1, 3, 4] | depth of 9 now: 3
rows changed by the move: {'adjacency': 1, 'materialized path': 3, 'nested sets (rebuild)': 6, 'closure table': '6 deleted + 6 inserted'}
nested sets after: [(1, (1, 16)), (2, (2, 5)), (3, (6, 15)), (4, (7, 12)), (5, (3, 4)), (6, (13, 14)), (7, (8, 9)), (9, (10, 11))]

EXPLAIN QUERY PLAN for the materialized-path prefix lookup:
  LIKE on a default-collation index -> ['SCAN mat']
  range on the same index -> ['SEARCH mat USING COVERING INDEX mat_path (path>? AND path<?)']
  LIKE on a NOCASE index -> ['SEARCH mat USING COVERING INDEX mat_path (path>? AND path<?)']
asserts passed
```

**Edge cases:**
- Index surprise I ran: with a plain index on `mat(path)`, `path LIKE '/1/3/4/%'` was a full `SCAN mat` in SQLite 3.45.1; the same lookup written as a range (`path >= '/1/3/4/' AND path < '/1/3/40'`, where `0` is the character after `/`) used the index, and so did `LIKE` once the index was created `COLLATE NOCASE` (SQLite's default `LIKE` is case-insensitive). Other engines have their own rules for `LIKE` and indexes (not executed here).
- Path as text breaks on ids that contain the separator, and the path length limits the depth; the leading and trailing slash make prefix tests safe.
- Nested sets: insert or move renumbers many rows, and two concurrent writers can corrupt the numbering, so writes need locking or a rebuild. My rebuild changed 6 of 8 rows to move a 3-node subtree in an 8-node tree.
- Closure table grows with the number of ancestor-descendant pairs: 22 rows for 8 nodes here; a straight chain of n nodes has n(n+1)/2 rows (Q26 prints the numbers for a 2,000-node chain).
- Orphans, loops and a second root are not prevented by any of these models by themselves; adjacency needs a foreign key plus a cycle check on move (Q20), and the others can hold impossible states if written by hand.
- Moving a node under its own descendant must be rejected in every model; none of the SQL above checks it.

**Then explain:**
- Adjacency list: simplest, one row per node, trivial inserts and moves (one cell), every subtree read needs a recursive query and an index on `parent_id`; foreign keys keep integrity easily.
- Materialized path: one indexed string per row, descendants by prefix, ancestors by splitting; moving a subtree rewrites every path below it; the path must be kept consistent by the application, no foreign key helps. Index on `path` (with the right collation or a range predicate, see above).
- Nested sets: subtree and ancestor reads are range comparisons with no recursion, depth needs a count; every insert, delete or move touches many rows; integrity is easy to break. Index on `(lft, rgt)`.
- Closure table: ancestors, descendants and depth are one indexed lookup each; storage is O(n squared) in the worst case (a chain); inserting a leaf adds one row per ancestor, moving a subtree rewrites the pairs between the subtree and its old and new ancestors; integrity needs the application or triggers. Index on `(ancestor, descendant)` and `(descendant, ancestor)`.
- My picks (rules of thumb, not benchmarks): read-heavy catalogue with rare changes: closure table or materialized path (or nested sets if the tree almost never changes); comment thread with frequent inserts: adjacency list (plus a materialized path for sorting and fetching a thread); deep org chart that changes often: adjacency list with a recursive CTE, adding a closure table only if the recursive reads become the bottleneck.
- The O(n squared) closure-table and the nested-set write cost come from blog posts I only saw as search snippets; what I measured here is only row counts on one tiny tree.

**Follow-ups:**
- Which gives ordered sibling output for a UI? Nested sets (order by `lft`), or a materialized path padded to fixed width, or an adjacency list with a sort key.
- PostgreSQL has `ltree`; is it a fifth model? It is a typed materialized path with index support; hedged, not executed.
- How do you keep a closure table correct? Insert the node's rows in the same transaction as the node (all ancestors of the parent, plus the self row); on delete remove the rows where it is a descendant.

**Common mistakes:**
- Prefix tests without a trailing separator (`/1/2/4` also matches `/1/2/40`).
- Using `LIKE` on a path column and assuming the index is used.
- Leaving out the self row in the closure table and then missing the node itself in counts.
- Calling the model choice a benchmark result.
- Moving a subtree under its own descendant.

### Q25 ⭐ 🟡 pandas: all reports under a manager with iterative merges. employees DataFrame(emp_id, manager_id, name, salary) with a NaN manager_id for the CEO. Compute the subtree of manager 3 with a while loop that merges the current frontier to the edge frame until the frontier is empty, tracking level and visited ids so cycles terminate, and the equivalent for the whole company (pairs ancestor, descendant). Assert equality with the SQL recursive CTE, note that manager_id becomes float64 because of NaN (use the nullable Int64 dtype) and that merge matches NaN to NaN, and say why a pandas loop costs one merge per level, not per row.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** In pandas I expand the tree one level per iteration: merge the current frontier (ids and their level) to the edge frame on `emp_id = manager_id`, drop anything already seen, and stop when the frontier is empty; the cost is one merge per level of depth, not one per employee, and the two pandas traps are that a NaN manager turns `manager_id` into float64 (use `Int64`) and that `merge` matches NaN to NaN while SQL never does.

**Schema and sample data:** the twelve-employee tree used across this part (Tim is the CEO with a NULL manager; Hari is emp 3). `emp_cyc` is a tiny second table with a loop (6 and 7 manage each other, 8 reports to 7) to show the cycle guard.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
-- a loop: 6 and 7 manage each other, 8 reports to 7
CREATE TABLE emp_cyc(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO emp_cyc VALUES (1,NULL),(2,1),(6,7),(7,6),(8,7);
```

**SQL answer:** three queries in the Code block. The subtree of manager 3 with its level:
```sql
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = 3
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
```
All ancestor-descendant pairs for the whole company with the depth (anchor: every direct manager link; step: extend each pair one level down):
```sql
WITH RECURSIVE pairs(ancestor, descendant, depth) AS (
  SELECT manager_id, emp_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT p.ancestor, e.emp_id, p.depth + 1
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
  WHERE p.depth < 20
)
SELECT ancestor, descendant, depth FROM pairs ORDER BY ancestor, descendant
```
And the loop case with `UNION` (rows are bare ids, so a repeated id is dropped and the recursion ends):
```sql
WITH RECURSIVE sub(emp_id) AS (
  SELECT emp_id FROM emp_cyc WHERE manager_id = 6
  UNION
  SELECT e.emp_id FROM emp_cyc e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id FROM sub ORDER BY emp_id
```

**pandas answer:** two functions, shown once here and identical to the Code block. `subtree` is the frontier loop with a visited set; `all_pairs` is the same loop where the frontier is a pairs frame (ancestor, descendant, depth) and a pair is dropped when it was already seen. Both return the number of merges:
```py
def subtree(emp, boss):
    kids = emp[["emp_id", "manager_id"]]
    frontier = kids[kids["manager_id"] == boss][["emp_id"]].assign(level=1)
    seen, parts, merges = set(frontier["emp_id"]), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(kids, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
        merges += 1
        nxt = nxt[~nxt["emp_id"].isin(seen)]
        frontier = nxt[["emp_id"]].assign(level=nxt["level"] + 1)
        seen.update(frontier["emp_id"])
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges

def all_pairs(emp):
    edges = emp.dropna(subset=["manager_id"]).rename(columns={"manager_id": "ancestor", "emp_id": "descendant"})[["ancestor", "descendant"]]
    frontier = edges.assign(depth=1)
    seen, parts, merges = set(zip(edges["ancestor"], edges["descendant"])), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(edges.rename(columns={"ancestor": "descendant", "descendant": "child"}), on="descendant")
        merges += 1
        nxt = pd.DataFrame({"ancestor": nxt["ancestor"], "descendant": nxt["child"], "depth": nxt["depth"] + 1})
        fresh = [(a, d) not in seen for a, d in zip(nxt["ancestor"], nxt["descendant"])]
        frontier = nxt[pd.Series(fresh, index=nxt.index, dtype=bool)].drop_duplicates(["ancestor", "descendant"])
        seen.update(zip(frontier["ancestor"], frontier["descendant"]))
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges
```

**Example:** subtree of 3. Level 1 (the anchor, direct reports): Shyam (4) and Asha (7). Merge 1 joins these ids to the rows whose manager is 4 or 7: Ram (10), Zoya (11), Nina (12), level 2. Merge 2 finds nobody under 10, 11, 12, the frontier is empty, the loop stops. So 5 rows and 2 merges for a tree with 12 employees: the loop count follows the depth (2 levels below Hari), not the head count. For the whole company, the deepest chain is Tim, Radha, Hari, Shyam, Ram (depth 4), so there are 4 merges, and 29 pairs in total (the sum of depths over all employees).
Loop case: from emp 6 the visited-set loop returns 7 (a report of 6), then 6 and 8 (reports of 7) after merge 1, and merge 2 finds only already-seen ids; result 6, 7, 8 (6 appears as its own descendant because of the loop), same as `UNION` in SQL.

**Code:** run with `python3 -I`. Compared after ordering by `level, emp_id` (subtree) and `ancestor, descendant` (pairs); ids are cast to `int64` after the loop because the frames carry nullable integers.
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
-- a loop: 6 and 7 manage each other, 8 reports to 7
CREATE TABLE emp_cyc(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO emp_cyc VALUES (1,NULL),(2,1),(6,7),(7,6),(8,7);
"""
SQL_SUBTREE = """
WITH RECURSIVE sub(emp_id, level) AS (
  SELECT emp_id, 1 FROM employees WHERE manager_id = 3
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM employees e JOIN sub s ON e.manager_id = s.emp_id
  WHERE s.level < 20
)
SELECT emp_id, level FROM sub ORDER BY level, emp_id
"""
SQL_PAIRS = """
WITH RECURSIVE pairs(ancestor, descendant, depth) AS (
  SELECT manager_id, emp_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT p.ancestor, e.emp_id, p.depth + 1
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
  WHERE p.depth < 20
)
SELECT ancestor, descendant, depth FROM pairs ORDER BY ancestor, descendant
"""
SQL_CYC = """
WITH RECURSIVE sub(emp_id) AS (
  SELECT emp_id FROM emp_cyc WHERE manager_id = 6
  UNION
  SELECT e.emp_id FROM emp_cyc e JOIN sub s ON e.manager_id = s.emp_id
)
SELECT emp_id FROM sub ORDER BY emp_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_sub = pd.read_sql_query(SQL_SUBTREE, con)
sql_pairs = pd.read_sql_query(SQL_PAIRS, con)
sql_cyc = pd.read_sql_query(SQL_CYC, con)
print("SQL subtree of manager 3:\n" + sql_sub.to_string(index=False))
print("SQL ancestor-descendant pairs:", len(sql_pairs), "rows; max depth", sql_pairs["depth"].max())

employees = pd.read_sql_query("SELECT * FROM employees", con)
emp_cyc = pd.read_sql_query("SELECT * FROM emp_cyc", con)
print("\nread_sql dtype of manager_id:", employees["manager_id"].dtype, "| emp_id:", employees["emp_id"].dtype)
employees["manager_id"] = employees["manager_id"].astype("Int64")
emp_cyc["manager_id"] = emp_cyc["manager_id"].astype("Int64")
print("after astype('Int64'):", employees["manager_id"].dtype, "| root value:", employees.loc[0, "manager_id"])

# pd:main
def subtree(emp, boss):
    kids = emp[["emp_id", "manager_id"]]
    frontier = kids[kids["manager_id"] == boss][["emp_id"]].assign(level=1)
    seen, parts, merges = set(frontier["emp_id"]), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(kids, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
        merges += 1
        nxt = nxt[~nxt["emp_id"].isin(seen)]
        frontier = nxt[["emp_id"]].assign(level=nxt["level"] + 1)
        seen.update(frontier["emp_id"])
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges

def all_pairs(emp):
    edges = emp.dropna(subset=["manager_id"]).rename(columns={"manager_id": "ancestor", "emp_id": "descendant"})[["ancestor", "descendant"]]
    frontier = edges.assign(depth=1)
    seen, parts, merges = set(zip(edges["ancestor"], edges["descendant"])), [frontier], 0
    while len(frontier):
        nxt = frontier.merge(edges.rename(columns={"ancestor": "descendant", "descendant": "child"}), on="descendant")
        merges += 1
        nxt = pd.DataFrame({"ancestor": nxt["ancestor"], "descendant": nxt["child"], "depth": nxt["depth"] + 1})
        fresh = [(a, d) not in seen for a, d in zip(nxt["ancestor"], nxt["descendant"])]
        frontier = nxt[pd.Series(fresh, index=nxt.index, dtype=bool)].drop_duplicates(["ancestor", "descendant"])
        seen.update(zip(frontier["ancestor"], frontier["descendant"]))
        parts.append(frontier)
    return pd.concat(parts, ignore_index=True), merges
# pd:end

pd_sub, m1 = subtree(employees, 3)
pd.testing.assert_frame_equal(pd_sub.sort_values(["level", "emp_id"]).reset_index(drop=True).astype("int64"), sql_sub, check_dtype=False)
print(f"\nsubtree of 3: equal to SQL after sorting by level, emp_id; {len(employees)} employees, {m1} merges (levels, not rows)")

pd_pairs, m2 = all_pairs(employees)
pd.testing.assert_frame_equal(pd_pairs.sort_values(["ancestor", "descendant"]).reset_index(drop=True).astype("int64"), sql_pairs, check_dtype=False)
print(f"all pairs: {len(pd_pairs)} rows equal to SQL after sorting by ancestor, descendant; {m2} merges")

# cycle: visited set terminates, SQL UNION (rows are bare ids) terminates
cyc_pd, m3 = subtree(emp_cyc, 6)
assert sorted(cyc_pd["emp_id"]) == sql_cyc["emp_id"].tolist()
print("cycle 6<->7 (8 under 7), subtree of 6, visited-set loop:", sorted(cyc_pd["emp_id"]), "after", m3, "merges; SQL UNION:", sql_cyc["emp_id"].tolist())

# the same loop WITHOUT the visited filter never ends: stop it after 8 merges and watch the frontier
kids = emp_cyc[["emp_id", "manager_id"]]
fr = kids[kids["manager_id"] == 6][["emp_id"]]
sizes = []
for _ in range(8):
    fr = fr.merge(kids, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))[["emp_id"]]
    sizes.append(len(fr))
print("no visited filter, frontier size after each of 8 merges:", sizes, "(never reaches 0)")

# NaN keys: SQL NULL never joins, pandas merge matches NaN to NaN
sql_same = con.execute("SELECT COUNT(*) FROM employees a JOIN employees b ON a.manager_id = b.manager_id").fetchone()[0]
pd_same = len(employees.merge(employees, on="manager_id"))
pd_same_fixed = len(employees.dropna(subset=["manager_id"]).merge(employees.dropna(subset=["manager_id"]), on="manager_id"))
print("same-manager pairs (a.manager_id = b.manager_id): SQL", sql_same, "| pandas merge", pd_same, "| pandas after dropna", pd_same_fixed)
assert pd_same == sql_same + 1 and pd_same_fixed == sql_same
leaf, mleaf = subtree(employees, 10)
assert len(leaf) == 0 and list(leaf.columns) == ["emp_id", "level"]
print("empty case: subtree of leaf 10 ->", len(leaf), "rows, columns", list(leaf.columns), ",", mleaf, "merges")
print("asserts passed")
```

**Output (my run):**
```text
SQL subtree of manager 3:
 emp_id  level
      4      1
      7      1
     10      2
     11      2
     12      2
SQL ancestor-descendant pairs: 29 rows; max depth 4

read_sql dtype of manager_id: float64 | emp_id: int64
after astype('Int64'): Int64 | root value: <NA>

subtree of 3: equal to SQL after sorting by level, emp_id; 12 employees, 2 merges (levels, not rows)
all pairs: 29 rows equal to SQL after sorting by ancestor, descendant; 4 merges
cycle 6<->7 (8 under 7), subtree of 6, visited-set loop: [6, 7, 8] after 2 merges; SQL UNION: [6, 7, 8]
no visited filter, frontier size after each of 8 merges: [2, 1, 2, 1, 2, 1, 2, 1] (never reaches 0)
same-manager pairs (a.manager_id = b.manager_id): SQL 19 | pandas merge 20 | pandas after dropna 19
empty case: subtree of leaf 10 -> 0 rows, columns ['emp_id', 'level'] , 0 merges
asserts passed
```

**Edge cases:**
- dtype: `pd.read_sql_query` gave `manager_id` as float64 in my run because of the NULL; `astype("Int64")` (nullable integer) keeps whole numbers and shows `<NA>` for the root. Joining float ids to int ids works but invites precision and display surprises; cast early.
- NaN matches NaN in `merge`: the same-manager self join (`a.manager_id = b.manager_id`) gave 19 rows in SQLite and 20 in pandas (the CEO row paired with itself). After `dropna(subset=["manager_id"])` pandas also gave 19. In a frontier loop this matters if the frontier can hold NaN keys: dropping NaN first is the safe habit. Also `employees["manager_id"] == np.nan` is never true; use `isna()`.
- Cycle: with the visited filter the loop ended after 2 merges; without it, the frontier sizes were 2, 1, 2, 1, 2, 1, 2, 1 over 8 merges and would never reach 0 (I stopped it myself).
- Duplicate edge rows: the visited filter drops repeats by id, the plain merge would carry duplicates forward (Q28).
- Empty case: a manager with no reports (leaf 10 in my run) gives an empty first frontier, the loop body never runs, and the result is an empty frame that still has the columns `emp_id` and `level` (0 rows, 0 merges).
- Orphans (manager id not in the table) are never reached from the root; they simply do not appear.

**Then explain:**
- One merge per level: each merge expands every frontier row at once (vectorised), so the number of Python-level iterations is the tree depth. A pure row-by-row loop would cost one step per employee.
- Cost of a merge is about frontier size plus edges, so the whole-company pair loop does roughly depth merges each as large as the current pair set; the result size is the number of ancestor-descendant pairs (29 here, but Q26 shows what it can reach on 50,000 or a long chain).
- Why the guard is two things: a visited set (so cycles end) and `drop_duplicates` on the frontier (so duplicate edges do not multiply rows); the SQL equivalents are `UNION` or a path string, and cleaning duplicates beforehand.
- The SQL and pandas results agree on the clean tree; they differ only where NULL key semantics or unguarded loops come in, which is exactly what the edge cases above show.
- Part 4-5 window functions are not needed here.

**Follow-ups:**
- Include the root of the subtree in the result? Add the anchor row with level 0 (the SQL anchor row `SELECT emp_id, 0` does that).
- Many roots at once? Start the frontier from all of them (as `reports` does in Q28).
- Can you avoid the loop? For a known small depth, repeated merges unrolled; for unknown depth use the loop; for very large frames use a graph library (networkx is installed; I did not use it here).

**Common mistakes:**
- Merging float ids against int ids and not noticing `NaN` in the frontier.
- No visited set: infinite loop on a cycle, duplicated rows on a repeated edge.
- Forgetting that `merge` matches NaN to NaN (SQL does not).
- Counting loop iterations as employees (cost is depth).
- Comparing the SQL and pandas results without sorting.

### Q26 ⭐ 🟡 pandas: roll-ups, depth and paths. From the employees DataFrame compute per-employee depth and path string by walking parents with a dict or repeated merge, then the subtree size and subtree salary with groupby, transform and the pairs frame, and use explode to turn the path list into one row per ancestor and the reverse (groupby then list). Assert equality with the SQL results of the roll-up question and show that groupby(manager_id) alone gives direct reports only. Mention the memory cost of the full ancestor-descendant pair frame and when it is acceptable.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Walk each employee's chain of managers once (a dict lookup) to get depth and path, `explode` the chain into one row per (descendant, ancestor) pair, and every roll-up becomes an ordinary `groupby` on the ancestor; `groupby("manager_id")` alone only counts direct reports, and the pair frame costs as many rows as there are ancestor-descendant pairs.

**Schema and sample data:** the twelve-employee tree (Tim is the CEO; salary is toy column data).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
```

**SQL answer:** three queries in the Code block. Depth and path from the root (path of names with `/`):
```sql
WITH RECURSIVE t(emp_id, name, depth, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.depth + 1, t.path || '/' || e.name
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.depth < 20
)
SELECT emp_id, depth, path FROM t ORDER BY emp_id
```
Subtree size and subtree salary per employee, including the employee himself, through a pairs CTE that starts with one self pair per employee (so there is no depth guard needed on a clean tree; Q15 and Q28 cover dirty data):
```sql
WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT emp_id, emp_id FROM employees
  UNION ALL
  SELECT p.ancestor, e.emp_id
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
)
SELECT p.ancestor AS emp_id,
       COUNT(*) AS subtree_size,
       SUM(e.salary) AS subtree_salary
FROM pairs p JOIN employees e ON e.emp_id = p.descendant
GROUP BY p.ancestor
ORDER BY p.ancestor
```
And direct reports only, for the contrast:
```sql
SELECT manager_id AS emp_id, COUNT(*) AS direct_reports FROM employees
WHERE manager_id IS NOT NULL GROUP BY manager_id ORDER BY manager_id
```

**pandas answer:** shown once here and identical to the Code block. `up` is the chain `[emp, manager, ..., CEO]` from a dict walk; `depth` is its length minus 1, `path` joins the names reversed; `explode` makes the pairs frame; the roll-up merges the salary on the descendant and groups by ancestor; `desc_lists` is the reverse (groupby then list); `direct` is the groupby on `manager_id` only:
```py
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
name = dict(zip(employees["emp_id"], employees["name"]))
def chain_up(i):                       # [i, manager, ..., CEO]
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out
emp = employees.assign(up=employees["emp_id"].map(chain_up))
emp["depth"] = emp["up"].str.len() - 1
emp["path"] = emp["up"].map(lambda u: "/".join(name[x] for x in u[::-1]))
# explode: one row per (descendant, ancestor), self included
pairs = emp[["emp_id", "up"]].explode("up").rename(columns={"emp_id": "descendant", "up": "ancestor"})
pairs["ancestor"] = pairs["ancestor"].astype("int64")
roll = (pairs.merge(employees[["emp_id", "salary"]], left_on="descendant", right_on="emp_id")
             .groupby("ancestor")
             .agg(subtree_size=("descendant", "size"), subtree_salary=("salary", "sum"))
             .rename_axis("emp_id").reset_index())
# the reverse: collect the descendants of each ancestor back into a list
desc_lists = pairs.groupby("ancestor")["descendant"].agg(lambda s: sorted(s)).rename("descendants")
# groupby on manager_id alone gives direct reports only
direct = (employees.dropna(subset=["manager_id"]).groupby("manager_id").size()
          .rename("direct_reports").rename_axis("emp_id").reset_index())
```

**Example:** Ram (10): the chain is `[10, 4, 3, 2, 1]`, so depth 4 and path `Tim/Radha/Hari/Shyam/Ram`. `explode` gives five pairs for Ram (ancestors 10, 4, 3, 2, 1, himself included at distance 0). Grouping all pairs by ancestor: Hari (3) has descendants 3, 4, 7, 10, 11, 12, so subtree size 6 and salary 60 + 50 + 45 + 25 + 28 + 27 = 235. Tim has 12 (everybody, salary 590) but `groupby("manager_id")` gives Tim only 2, his direct reports Radha and Meera. The two are different questions: direct reports versus everybody below.

**Code:** run with `python3 -I`. All three pandas results are compared with the SQL results after ordering by `emp_id` (every SQL query is ordered by `emp_id`).
```python
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,NULL,'Tim',100),(2,1,'Radha',80),(3,2,'Hari',60),(4,3,'Shyam',50),(5,1,'Meera',70),
 (6,5,'Kiran',40),(7,3,'Asha',45),(8,6,'Dev',30),(9,5,'Isha',35),(10,4,'Ram',25),
 (11,4,'Zoya',28),(12,7,'Nina',27);
"""
SQL_PATHS = """
WITH RECURSIVE t(emp_id, name, depth, path) AS (
  SELECT emp_id, name, 0, name FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.depth + 1, t.path || '/' || e.name
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.depth < 20
)
SELECT emp_id, depth, path FROM t ORDER BY emp_id
"""
SQL_ROLLUP = """
WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT emp_id, emp_id FROM employees
  UNION ALL
  SELECT p.ancestor, e.emp_id
  FROM pairs p JOIN employees e ON e.manager_id = p.descendant
)
SELECT p.ancestor AS emp_id,
       COUNT(*) AS subtree_size,
       SUM(e.salary) AS subtree_salary
FROM pairs p JOIN employees e ON e.emp_id = p.descendant
GROUP BY p.ancestor
ORDER BY p.ancestor
"""
SQL_DIRECT = """
SELECT manager_id AS emp_id, COUNT(*) AS direct_reports FROM employees
WHERE manager_id IS NOT NULL GROUP BY manager_id ORDER BY manager_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_paths = pd.read_sql_query(SQL_PATHS, con)
sql_roll = pd.read_sql_query(SQL_ROLLUP, con)
sql_direct = pd.read_sql_query(SQL_DIRECT, con)
employees = pd.read_sql_query("SELECT * FROM employees", con)
employees["manager_id"] = employees["manager_id"].astype("Int64")

# pd:main
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
name = dict(zip(employees["emp_id"], employees["name"]))
def chain_up(i):                       # [i, manager, ..., CEO]
    out = [i]
    while not pd.isna(parent[out[-1]]):
        out.append(int(parent[out[-1]]))
    return out
emp = employees.assign(up=employees["emp_id"].map(chain_up))
emp["depth"] = emp["up"].str.len() - 1
emp["path"] = emp["up"].map(lambda u: "/".join(name[x] for x in u[::-1]))
# explode: one row per (descendant, ancestor), self included
pairs = emp[["emp_id", "up"]].explode("up").rename(columns={"emp_id": "descendant", "up": "ancestor"})
pairs["ancestor"] = pairs["ancestor"].astype("int64")
roll = (pairs.merge(employees[["emp_id", "salary"]], left_on="descendant", right_on="emp_id")
             .groupby("ancestor")
             .agg(subtree_size=("descendant", "size"), subtree_salary=("salary", "sum"))
             .rename_axis("emp_id").reset_index())
# the reverse: collect the descendants of each ancestor back into a list
desc_lists = pairs.groupby("ancestor")["descendant"].agg(lambda s: sorted(s)).rename("descendants")
# groupby on manager_id alone gives direct reports only
direct = (employees.dropna(subset=["manager_id"]).groupby("manager_id").size()
          .rename("direct_reports").rename_axis("emp_id").reset_index())
# pd:end
direct["emp_id"] = direct["emp_id"].astype("int64")

# compare after ordering by emp_id (all SQL queries are ordered by emp_id)
pd.testing.assert_frame_equal(emp[["emp_id", "depth", "path"]].sort_values("emp_id").reset_index(drop=True), sql_paths, check_dtype=False)
pd.testing.assert_frame_equal(roll.sort_values("emp_id").reset_index(drop=True), sql_roll, check_dtype=False)
pd.testing.assert_frame_equal(direct.sort_values("emp_id").reset_index(drop=True), sql_direct, check_dtype=False)
print("depth/path, roll-up and direct-report counts equal the SQL results")
print(sql_paths.merge(sql_roll, on="emp_id").merge(sql_direct, on="emp_id", how="left").to_string(index=False))
print("\nexploded pairs for Ram (10):", pairs[pairs["descendant"] == 10]["ancestor"].tolist(), "| descendants list of Hari (3):", desc_lists[3])
print("Tim: direct reports =", int(direct.loc[direct["emp_id"] == 1, "direct_reports"].iloc[0]),
      "but subtree_size =", int(roll.loc[roll["emp_id"] == 1, "subtree_size"].iloc[0]), "(includes Tim himself)")

# memory of the pairs frame: toy tree, a balanced tree of 50,000 nodes (8 children per node) and a 2,000-node chain
def pair_stats(parent_arr):
    n = len(parent_arr)
    depth = np.zeros(n, dtype=np.int64)
    for i in range(1, n):
        depth[i] = depth[parent_arr[i]] + 1
    rows = int((depth + 1).sum())
    return n, rows, rows * 16 / 1e6
bal = np.array([-1] + [(i - 1) // 8 for i in range(1, 50000)])
chain = np.array([-1] + list(range(1999)))
print("\nrows in the pairs frame (self rows included); int64 payload computed as rows x 2 columns x 8 bytes, not allocated:")
print("  toy tree      : %d nodes -> %d rows, deep memory %d bytes" % (len(employees), len(pairs), pairs.memory_usage(deep=True).sum()))
for label, arr in [("balanced 8-ary ", bal), ("straight chain ", chain)]:
    n, rows, mb = pair_stats(arr)
    print(f"  {label}: {n} nodes -> {rows} rows, about {mb:.1f} MB")
print("asserts passed")
```

**Output (my run):**
```text
depth/path, roll-up and direct-report counts equal the SQL results
 emp_id  depth                      path  subtree_size  subtree_salary  direct_reports
      1      0                       Tim            12             590             2.0
      2      1                 Tim/Radha             7             315             1.0
      3      2            Tim/Radha/Hari             6             235             2.0
      4      3      Tim/Radha/Hari/Shyam             3             103             2.0
      5      1                 Tim/Meera             4             175             2.0
      6      2           Tim/Meera/Kiran             2              70             1.0
      7      3       Tim/Radha/Hari/Asha             2              72             1.0
      8      3       Tim/Meera/Kiran/Dev             1              30             NaN
      9      2            Tim/Meera/Isha             1              35             NaN
     10      4  Tim/Radha/Hari/Shyam/Ram             1              25             NaN
     11      4 Tim/Radha/Hari/Shyam/Zoya             1              28             NaN
     12      4  Tim/Radha/Hari/Asha/Nina             1              27             NaN

exploded pairs for Ram (10): [10, 4, 3, 2, 1] | descendants list of Hari (3): [3, 4, 7, 10, 11, 12]
Tim: direct reports = 2 but subtree_size = 12 (includes Tim himself)

rows in the pairs frame (self rows included); int64 payload computed as rows x 2 columns x 8 bytes, not allocated:
  toy tree      : 12 nodes -> 41 rows, deep memory 984 bytes
  balanced 8-ary : 50000 nodes -> 307202 rows, about 4.9 MB
  straight chain : 2000 nodes -> 2001000 rows, about 32.0 MB
asserts passed
```

**Edge cases:**
- The pairs frame includes the self pair, so subtree size counts the manager; "number of reports" is `subtree_size - 1` (Tim: 12 versus 11 reports at any depth).
- Leaves have no direct reports: they are absent from the `groupby(manager_id)` output; the merge in my comparison table shows `NaN` (float) for them, so fill with 0 and cast if you need an integer column.
- The CEO has `NaN` as manager: `groupby` and `dropna` drop it (the root is not a report of anybody); `explode` of the chain is fine because the walk stops at the root.
- `explode` returns object dtype; cast the ancestor to `int64` before merging.
- A cycle or orphan would break the dict walk (an infinite loop for a cycle; a `KeyError` for an unknown manager), so clean first (Q28).
- Order: `groupby` sorts by key by default; I still sort before comparing.

**Then explain:**
- Why `explode`: a list-valued column (the chain) becomes one row per element; it is the pandas version of the SQL pairs CTE (one row per ancestor-descendant pair). The reverse is `groupby("ancestor")["descendant"].agg(list)`.
- Memory and when it is acceptable: the pairs frame has one row per ancestor-descendant pair including self. For the toy tree that is 41 rows (984 bytes in `memory_usage(deep=True)` in my run). For a balanced tree of 50,000 nodes with 8 children per node I computed 307,202 rows, about 4.9 MB of int64 payload (rows times 16 bytes, computed, not allocated); for a straight chain of 2,000 nodes 2,001,000 rows, about 32 MB. It is fine for trees of ordinary depth (rows about nodes times depth) and a problem for very deep ones (rows about nodes squared over two).
- When not to build it: if you only need subtree size and salary and the depth is small, aggregate bottom-up (children before parents, one pass by level) instead of materialising every pair.
- Depth and path are per-row facts; subtree size and salary are per-ancestor facts: the first comes from walking up, the second from grouping the pairs.
- SQL parity: the CTE uses `UNION ALL` and a join back to `employees` for the salary; both versions equal after sorting.

**Follow-ups:**
- Average salary of a subtree? `subtree_salary / subtree_size` from the same frame.
- Roll up by level (a manager's reports at depth 2 only)? Keep the distance column in the pairs frame and filter it.
- Only managers with at least three reports at any depth? Filter `subtree_size - 1 >= 3` after the groupby (Q9).

**Common mistakes:**
- Using `groupby("manager_id").size()` as "team size" (direct reports only).
- Counting the manager in his own subtree without saying so.
- Joining salary onto the ancestor instead of the descendant in the pairs frame (summing the manager's salary many times).
- Building the full pairs frame on a very deep or huge hierarchy without estimating its size.
- Leaving NaN and float dtypes in the key columns.

### Q27 ⭐ 🔴 Plain Python BFS and DFS against SQL: friendships and flights as edge lists. Write BFS (collections.deque) for shortest distance and connected components and DFS (stack) for all simple paths, then check results against the SQL recursive CTE answers with asserts. Say in the answer that networkx 3.6.1 is installed in this environment and scipy is not, show the networkx call (shortest_path_length, connected_components) as the library check, and keep the plain-Python version as the interview answer. Explain the equivalence between a BFS queue and the SQLite recursive queue with ORDER BY level.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** In plain Python I keep an adjacency dict, use a `collections.deque` queue for BFS (shortest distance in an unweighted graph, connected components) and a stack for DFS (all simple paths), then check each result against the SQL recursive CTE and against networkx; a SQLite recursive CTE is itself a queue, and with no `ORDER BY` it is the BFS queue.

**Schema and sample data:** `friendships(user_a, user_b)` stores each undirected friendship once: 1-2, 1-3, 2-4, 3-4, 4-5, 5-6 (one cluster), 7-8, 8-9 (a second cluster), and user 10 has no friends and is only in `nodes`. `flights(src, dst, cost)` is directed: DEL to BOM and HYD, BOM and HYD connect to each other, both reach BLR, and BLR flies back to DEL (a loop).
```sql
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER);
INSERT INTO friendships VALUES (1,2),(1,3),(2,4),(3,4),(4,5),(5,6),(7,8),(8,9);
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BOM',100),('DEL','HYD',80),('BOM','HYD',20),('HYD','BOM',25),
 ('BOM','BLR',90),('HYD','BLR',70),('BLR','DEL',150);
```

**SQL answer:** `SQL_DIST`, `SQL_COMP`, `SQL_PATHS` and `SQL_QUEUE` in the Code block. The undirected edge list is symmetrised in a plain (non-recursive) CTE `e` and distances from user 1 are `MIN(dist)` per node, with a depth cap of 10 as the guard:
```sql
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
)
SELECT node, MIN(dist) AS dist FROM r GROUP BY node ORDER BY dist, node
```
Components as "smallest id reachable" (closure with `UNION`, so it ends by itself):
```sql
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), reach(src, dst) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT reach.src, e.b FROM reach JOIN e ON e.a = reach.dst
)
SELECT src AS node, MIN(dst) AS component FROM reach GROUP BY src ORDER BY src
```
All simple routes DEL to BLR with a path-string guard:
```sql
WITH RECURSIVE p(node, path, cost) AS (
  SELECT 'DEL', ',DEL,', 0
  UNION ALL
  SELECT f.dst, p.path || f.dst || ',', p.cost + f.cost
  FROM p JOIN flights f ON f.src = p.node
  WHERE instr(p.path, ',' || f.dst || ',') = 0
)
SELECT trim(path, ',') AS route, cost FROM p WHERE node = 'BLR' ORDER BY cost, route
```

**pandas answer:** this is a question about algorithms, so the interview answer is plain Python, not pandas; the DataFrames are only the carrier (`pd.DataFrame(...)` of the results compared with the SQL frames). Shown once here and identical to the Code block:
```py
def adjacency(pairs, directed):
    g = {}
    for a, b in pairs:
        g.setdefault(a, []).append(b)
        g.setdefault(b, [])
        if not directed:
            g[b].append(a)
    return {k: sorted(v) for k, v in g.items()}

def bfs_distance(g, start):
    dist, queue, order = {start: 0}, deque([start]), [start]
    while queue:
        u = queue.popleft()
        for v in g[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
                order.append(v)
    return dist, order

def components(g):
    comp = {}
    for s in sorted(g):
        if s in comp:
            continue
        label, queue = s, deque([s])         # s is the smallest unseen node, so it is the component's smallest id
        comp[s] = label
        while queue:
            u = queue.popleft()
            for v in g[u]:
                if v not in comp:
                    comp[v] = label
                    queue.append(v)
    return comp

def all_simple_paths(g, cost, start, goal):
    out, stack = [], [(start, [start], 0)]
    while stack:
        u, path, total = stack.pop()
        if u == goal:
            out.append((">".join(path), total))
            continue
        for v in g[u]:
            if v not in path:
                stack.append((v, path + [v], total + cost[(u, v)]))
    return sorted(out, key=lambda t: (t[1], t[0]))
```
The library check (also in the Code block): `nx.shortest_path_length(G, 1)`, `nx.connected_components(G)` and `nx.all_simple_paths(D, "DEL", "BLR")`, called as written at run time with networkx 3.6.1. scipy is not installed in this environment, so I did not use `scipy.sparse.csgraph`.

**Example:** BFS from user 1: queue `[1]`; pop 1, neighbours 2 and 3 get distance 1; pop 2, neighbour 4 gets distance 2; pop 3, its neighbour 4 is already seen; pop 4, neighbour 5 gets 3; pop 5, neighbour 6 gets 4; the queue empties. Distances 1:0, 2:1, 3:1, 4:2, 5:3, 6:4; users 7, 8, 9, 10 are never reached. Components: BFS from the smallest unseen node labels the whole cluster with that node: {1..6} gets 1, {7, 8, 9} gets 7, {10} gets 10, matching the SQL "smallest reachable id". DFS with a stack from DEL to BLR (never stepping to a node already on the path): DEL, HYD, BLR (150); DEL, BOM, BLR (190); DEL, BOM, HYD, BLR (190); DEL, HYD, BOM, BLR (195). The loop BLR to DEL is never used because DEL is already on every path.

**Code:** run with `python3 -I`. The SQL frames and the Python results are compared after ordering by `dist, node` (distances), `node` (components) and `cost, route` (flight routes); networkx results are asserted equal; the last block prints the SQLite queue order.
```python
import sqlite3
from collections import deque
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER);
INSERT INTO friendships VALUES (1,2),(1,3),(2,4),(3,4),(4,5),(5,6),(7,8),(8,9);
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BOM',100),('DEL','HYD',80),('BOM','HYD',20),('HYD','BOM',25),
 ('BOM','BLR',90),('HYD','BLR',70),('BLR','DEL',150);
"""
SQL_DIST = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
)
SELECT node, MIN(dist) AS dist FROM r GROUP BY node ORDER BY dist, node
"""
SQL_COMP = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), reach(src, dst) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT reach.src, e.b FROM reach JOIN e ON e.a = reach.dst
)
SELECT src AS node, MIN(dst) AS component FROM reach GROUP BY src ORDER BY src
"""
SQL_PATHS = """
WITH RECURSIVE p(node, path, cost) AS (
  SELECT 'DEL', ',DEL,', 0
  UNION ALL
  SELECT f.dst, p.path || f.dst || ',', p.cost + f.cost
  FROM p JOIN flights f ON f.src = p.node
  WHERE instr(p.path, ',' || f.dst || ',') = 0
)
SELECT trim(path, ',') AS route, cost FROM p WHERE node = 'BLR' ORDER BY cost, route
"""
SQL_QUEUE = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
  {order}
)
SELECT node, dist FROM r
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_dist = pd.read_sql_query(SQL_DIST, con)
sql_comp = pd.read_sql_query(SQL_COMP, con)
sql_paths = pd.read_sql_query(SQL_PATHS, con)
friends = pd.read_sql_query("SELECT * FROM friendships", con)
flights = pd.read_sql_query("SELECT * FROM flights", con)
all_nodes = [r[0] for r in con.execute("SELECT node_id FROM nodes ORDER BY 1")]

# pd:main
def adjacency(pairs, directed):
    g = {}
    for a, b in pairs:
        g.setdefault(a, []).append(b)
        g.setdefault(b, [])
        if not directed:
            g[b].append(a)
    return {k: sorted(v) for k, v in g.items()}

def bfs_distance(g, start):
    dist, queue, order = {start: 0}, deque([start]), [start]
    while queue:
        u = queue.popleft()
        for v in g[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
                order.append(v)
    return dist, order

def components(g):
    comp = {}
    for s in sorted(g):
        if s in comp:
            continue
        label, queue = s, deque([s])         # s is the smallest unseen node, so it is the component's smallest id
        comp[s] = label
        while queue:
            u = queue.popleft()
            for v in g[u]:
                if v not in comp:
                    comp[v] = label
                    queue.append(v)
    return comp

def all_simple_paths(g, cost, start, goal):
    out, stack = [], [(start, [start], 0)]
    while stack:
        u, path, total = stack.pop()
        if u == goal:
            out.append((">".join(path), total))
            continue
        for v in g[u]:
            if v not in path:
                stack.append((v, path + [v], total + cost[(u, v)]))
    return sorted(out, key=lambda t: (t[1], t[0]))
# pd:end

g = adjacency(zip(friends["user_a"], friends["user_b"]), directed=False)
for n in all_nodes:
    g.setdefault(n, [])
dist, bfs_order = bfs_distance(g, 1)
py_dist = pd.DataFrame(sorted(dist.items(), key=lambda t: (t[1], t[0])), columns=["node", "dist"])
# compare after ordering by dist, node (the SQL ORDER BY)
pd.testing.assert_frame_equal(py_dist, sql_dist, check_dtype=False)
comp = components(g)
py_comp = pd.DataFrame(sorted(comp.items()), columns=["node", "component"])
pd.testing.assert_frame_equal(py_comp, sql_comp, check_dtype=False)
fg = adjacency(zip(flights["src"], flights["dst"]), directed=True)
cost = {(s, d): c for s, d, c in zip(flights["src"], flights["dst"], flights["cost"])}
py_paths = pd.DataFrame(all_simple_paths(fg, cost, "DEL", "BLR"), columns=["route", "cost"])
sql_paths["route"] = sql_paths["route"].str.replace(",", ">")
pd.testing.assert_frame_equal(py_paths, sql_paths, check_dtype=False)
print("plain Python BFS distances, components and DFS simple paths equal the SQL results")
print("distances from user 1:", dict(zip(py_dist["node"], py_dist["dist"])))
print("components (node -> smallest id):", comp)
print(py_paths.to_string(index=False))

# networkx as the library check
G = nx.Graph(list(zip(friends["user_a"], friends["user_b"])))
G.add_nodes_from(all_nodes)
assert dict(nx.shortest_path_length(G, 1)) == dist
nx_comp = sorted(sorted(c) for c in nx.connected_components(G))
assert nx_comp == sorted(sorted(n for n, c in comp.items() if c == lab) for lab in set(comp.values()))
D = nx.DiGraph([(s, d) for s, d in zip(flights["src"], flights["dst"])])
nx_paths = sorted(">".join(p) for p in nx.all_simple_paths(D, "DEL", "BLR"))
assert nx_paths == sorted(py_paths["route"])
print("networkx", nx.__version__, "agrees: shortest_path_length, connected_components", nx_comp, "all_simple_paths", len(nx_paths))

# SQLite queue: default FIFO order is BFS; ORDER BY in the recursive select changes the queue to LIFO (DFS-like)
fifo = con.execute(SQL_QUEUE.format(order="")).fetchall()
lifo = con.execute(SQL_QUEUE.format(order="ORDER BY 2 DESC")).fetchall()
print("\nSQLite queue order, FIFO (no ORDER BY):", [f"{n}@{d}" for n, d in fifo])
print("SQLite queue order, ORDER BY dist DESC:", [f"{n}@{d}" for n, d in lifo])
print("Python BFS visit order                :", bfs_order)
assert [d for _, d in fifo] == sorted(d for _, d in fifo)
assert sorted(fifo) == sorted(lifo)
print("asserts passed")
```

**Output (my run):**
```text
plain Python BFS distances, components and DFS simple paths equal the SQL results
distances from user 1: {1: 0, 2: 1, 3: 1, 4: 2, 5: 3, 6: 4}
components (node -> smallest id): {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 7, 8: 7, 9: 7, 10: 10}
          route  cost
    DEL>HYD>BLR   150
    DEL>BOM>BLR   190
DEL>BOM>HYD>BLR   190
DEL>HYD>BOM>BLR   195
networkx 3.6.1 agrees: shortest_path_length, connected_components [[1, 2, 3, 4, 5, 6], [7, 8, 9], [10]] all_simple_paths 4

SQLite queue order, FIFO (no ORDER BY): ['1@0', '2@1', '3@1', '1@2', '4@2', '2@3', '3@3', '5@3', '1@4', '4@4', '6@4', '2@5', '3@5', '5@5', '1@6', '4@6', '6@6', '2@7', '3@7', '5@7', '1@8', '4@8', '6@8', '2@9', '3@9', '5@9', '1@10', '4@10', '6@10']
SQLite queue order, ORDER BY dist DESC: ['1@0', '2@1', '1@2', '2@3', '1@4', '2@5', '1@6', '2@7', '1@8', '2@9', '1@10', '4@10', '3@9', '4@8', '5@9', '6@10', '3@7', '4@6', '5@7', '6@8', '3@5', '4@4', '5@5', '6@6', '3@3', '4@2', '5@3', '6@4', '3@1']
Python BFS visit order                : [1, 2, 3, 4, 5, 6]
asserts passed
```

**Edge cases:**
- Isolated node (10): BFS never reaches it from 1, and it needs its own component label; SQL only has it because it comes from the `nodes` table, not from the edge list. Components computed from edges alone would silently drop it.
- Undirected storage (each friendship once): the SQL needs the symmetric edge list; forgetting it makes distances direction-dependent. Python's `adjacency(..., directed=False)` adds both directions.
- Cycle (BLR back to DEL): BFS needs a visited/distance dict, DFS needs "not already on the path"; without them both loop forever.
- Two routes with the same cost (190): both are returned; the sort by `cost, route` makes the order deterministic.
- No route: BFS leaves the node out of `dist`, the SQL has no row, networkx raises `NetworkXNoPath` for `shortest_path` (from its documentation; not run here).
- The SQLite queue in my run (surprise): with `UNION` deduplicating whole rows `(node, dist)`, a node is revisited at each new distance (the FIFO output contains `1@2`, `1@4`, `1@6`, ... because friend 2 leads back to user 1) until the depth cap ends it, so the distance has to be taken with `MIN(dist)` per node, as `SQL_DIST` does. Dedup by node alone, as Python's `dist` dict does, would need the distance not to be a column, which is why SQL BFS needs the cap and the `MIN`.

**Then explain:**
- BFS equals the SQLite recursive queue: the engine takes the oldest row from the queue, runs the recursive select on it, appends the results, so rows come out in order of distance; in my run the distance column of the FIFO output is non-decreasing (asserted). With `ORDER BY dist DESC` in the recursive select the newest and deepest row is taken first (last-in-first-out), which is the depth-first style (SQLite documents `ORDER BY` as the queue order); the output above shows the deep rows first.
- Differences from Python: Python's BFS marks a node visited once and never expands it again; the SQL carries the distance as data, so it re-expands unless the depth cap, a path string or `UNION` on node-only rows stops it.
- Complexity: BFS and DFS visit each node and edge once, O(V + E). Enumerating all simple paths is exponential in the worst case (Q23, Q29).
- Components: repeated BFS from unseen nodes; labelling by the smallest id matches the SQL.
- networkx is the check, not the interview answer: `connected_components` yields sets, `shortest_path_length` returns a dict of distances, `all_simple_paths` yields node lists; I compared them with the plain Python results.

**Follow-ups:**
- Shortest path with weights? Dijkstra with `heapq` (Q23).
- Friends of friends (distance exactly 2, not already friends)? Filter `dist == 2` from the BFS (Q11 shows the SQL).
- BFS on a huge graph? Not in SQL; a graph library or an engine with graph support (not covered here).

**Common mistakes:**
- Marking visited when popping instead of when pushing (the same node gets queued many times).
- Using a list as a queue with `pop(0)` (O(n) per pop); use `deque`.
- Using the edge list for components and losing isolated nodes.
- Forgetting the symmetric edges for an undirected graph.
- Treating `UNION` in a recursive CTE as BFS dedup by node when the distance is a column (it dedups by `(node, dist)`).

### Q28 ⭐ 🔴 SQL versus pandas on cycles, NULL parents and duplicate edges: build one edge table with a duplicate edge row, a NULL parent that is a real root, an edge pointing to an unknown parent and a 2-cycle. Show for each of the recursive CTE (UNION ALL, UNION, with path guard) and the pandas merge loop what happens: duplicated output rows, double counted salaries in a roll-up, missed root when a NULL join key never matches in SQL but does match in pandas merge, infinite loop versus visited-set termination. Return a compact table of behaviours and the cleaning steps (drop_duplicates, flag orphans, break cycles) that make both engines agree.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** The same dirty edge table makes SQL and pandas disagree in four ways: a repeated edge row double counts in both (UNION ALL rows and an unguarded merge loop), a NULL parent never matches in a SQL join but matches in a pandas `merge`, an orphan is silently invisible from the root in both, and a loop runs forever in both unless you add a guard (path string, `UNION` on bare ids, depth cap, or a visited set); after cleaning (drop duplicates, set orphans aside, break loops) the two engines agree.

**Schema and sample data:** one table with no primary key so a loader can repeat a row: emp 1 is the real root (NULL manager), 2 and 3 report to 1, the row for 3 appears twice (duplicate edge), 4 reports to 2, emp 5 points to manager 99 who does not exist (orphan), and 6 and 7 manage each other (a 2-cycle that is not connected to the root). Salaries are toy column data.
```sql
CREATE TABLE employees(emp_id INTEGER, manager_id INTEGER, salary INTEGER);   -- no primary key: a loader may repeat a row
INSERT INTO employees VALUES
 (1,NULL,100),   -- real root: NULL manager
 (2,1,50),(3,1,40),(3,1,40),   -- the last two rows are the same edge twice
 (4,2,30),
 (5,99,35),      -- 99 does not exist: orphan
 (6,7,20),(7,6,25);   -- 2-cycle, unreachable from the root
```

**SQL answer:** `SQL_ROLLUP` in the Code block is the roll-up from the NULL root with `UNION ALL` and a depth cap. The other statements used for the table of behaviours are `SQL_NULL_ANCHOR` (the same text with `manager_id = NULL`), `SQL_CYCLE_ALL` (from the loop, with a guard that I swap), `SQL_UNION_BARE`, `SQL_UNION_LEVEL`, `SQL_PATH`, `SQL_PEERS`, `SQL_LOOPERS` and `SQL_CLEAN`.
```sql
WITH RECURSIVE t(emp_id, level, salary) AS (
  SELECT emp_id, 0, salary FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, t.level + 1, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 10
)
SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people, SUM(salary) AS total_salary FROM t
```
Starting from the loop (emp 6), with a path guard:
```sql
WITH RECURSIVE t(emp_id, path) AS (
  SELECT emp_id, ',' || emp_id || ',' FROM employees WHERE emp_id = 6
  UNION ALL
  SELECT e.emp_id, t.path || e.emp_id || ','
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE instr(t.path, ',' || e.emp_id || ',') = 0
)
SELECT COUNT(*) AS result_rows FROM t
```
Detecting loop members (transitive closure of the manager link with `UNION`, so it ends by itself):
```sql
WITH RECURSIVE w(start, cur) AS (
  SELECT emp_id, manager_id FROM employees WHERE manager_id IS NOT NULL
  UNION
  SELECT w.start, e.manager_id FROM w JOIN employees e ON e.emp_id = w.cur WHERE e.manager_id IS NOT NULL
)
SELECT DISTINCT start FROM w WHERE cur = start ORDER BY 1
```
Cleaning in SQL: `DISTINCT` removes the repeated row, the `WHERE` keeps real roots and rows whose manager exists (the orphan is set aside), and the loop is broken at its smallest id by nulling that manager:
```sql
CREATE TABLE emp_clean AS
SELECT DISTINCT emp_id,
       CASE WHEN emp_id IN (SELECT start FROM ({loopers})) AND emp_id = (SELECT MIN(start) FROM ({loopers}))
            THEN NULL ELSE manager_id END AS manager_id,
       salary
FROM employees e
WHERE manager_id IS NULL OR EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
```

**pandas answer:** `reports` is the frontier merge from given root ids with an optional guard (visited set plus `drop_duplicates`), `clean` is the same three cleaning steps as the SQL, and `loop_members` walks the manager chain. Shown once here and identical to the Code block:
```py
def reports(emp, roots, guard=True, cap=10):
    """Frontier merge from the given root ids; returns one row per output row (emp_id, level, salary)."""
    kids = emp.rename(columns={"emp_id": "child", "salary": "child_salary"})
    frontier = emp[emp["emp_id"].isin(roots)].rename(columns={"salary": "child_salary"}).assign(child=lambda d: d["emp_id"], level=0)
    frontier = frontier[["child", "child_salary", "level"]]
    parts, seen = [frontier], set(frontier["child"])
    for _ in range(cap):
        nxt = frontier.merge(kids, left_on="child", right_on="manager_id", suffixes=("_p", ""))
        if guard:
            nxt = nxt[~nxt["child"].isin(seen)].drop_duplicates("child")
        frontier = pd.DataFrame({"child": nxt["child"], "child_salary": nxt["child_salary"], "level": nxt["level"] + 1})
        if not len(frontier):
            break
        seen.update(frontier["child"])
        parts.append(frontier)
    out = pd.concat(parts, ignore_index=True)
    return out.rename(columns={"child": "emp_id", "child_salary": "salary"})

def clean(emp):
    emp = emp.drop_duplicates()                                                     # repeated edge rows
    orphan = emp["manager_id"].notna() & ~emp["manager_id"].isin(emp["emp_id"])     # unknown manager: set aside
    emp = emp[~orphan]
    loops = loop_members(emp)
    if loops:
        emp = emp.assign(manager_id=emp["manager_id"].where(emp["emp_id"] != min(loops)))   # break each loop at its smallest id
    return emp.reset_index(drop=True)

def loop_members(emp):
    par = dict(zip(emp["emp_id"], emp["manager_id"]))
    out = set()
    for s in par:
        cur, hops = par[s], 0
        while pd.notna(cur) and cur in par and hops <= len(par):
            if cur == s:
                out.add(s)
                break
            cur, hops = par[cur], hops + 1
    return out
```

**Example:** from the real root, by hand. Level 0: emp 1 (100). Level 1: rows whose manager is 1: emp 2 (50), emp 3 (40) and emp 3 again (40) because the edge is stored twice. Level 2: the reports of 2 (emp 4, 30) and the reports of 3 (nobody). That is 5 output rows, 4 distinct people, and salary 100 + 50 + 40 + 40 + 30 = 260, while the true total is 220: the duplicate edge double counted emp 3. Emp 5 (35) is never reached because its manager 99 is not in the table, so a roll-up from the root silently leaves 35 out. Emp 6 and 7 are not reachable from the root either; started from emp 6, a `UNION ALL` bounces 6, 7, 6, 7 forever (6 rows with a depth cap of 5, 8 rows when the outer query has `LIMIT 8`). After cleaning there are two roots (1 and the loop-breaker 6) and the roll-up is 6 rows and 265 (220 for the tree of 1 plus 20 + 25 for 6 and 7; orphan 35 left out on purpose).

**Behaviours (every number from the run below):**

| Situation | SQL (SQLite 3.45.1) | pandas merge loop |
|---|---|---|
| Duplicate edge row, `UNION ALL` / no guard | 5 rows, 4 people, salary 260 | same: 5 rows, 4 people, 260 |
| Duplicate edge row, visited set (pandas) / drop duplicates first | `UNION` on `(emp_id, salary)` hides it only if rows match exactly; the clean way is to dedupe the table | 4 rows, 4 people, 220 |
| Root found by a NULL test | `manager_id IS NULL` finds it; `manager_id = NULL` returns 0 rows and the recursion never starts | `isna()` finds it; `== np.nan` selects 0 rows |
| NULL key in a join (same-manager pairs) | 13 rows: the NULL root never matches | 14 rows: NaN matches NaN; 13 after `dropna` |
| Orphan (manager 99 does not exist) | not reached from the root, no error | same: not reached, no error |
| Loop from emp 6 | `UNION ALL` with depth cap 5: 6 rows; unguarded with outer `LIMIT 8`: 8 rows; path guard: 2 rows; `UNION` on bare ids: 2 rows; `UNION` with a level column and cap 10: 11 rows | no guard with cap 5: 6 rows (never ends without the cap); visited set: 2 rows |

**Code:** run with `python3 -I`. The SQL and pandas cleaned tables are compared after ordering by `emp_id`; the roll-ups after cleaning are compared as (rows, distinct people, salary total).
```python
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER, manager_id INTEGER, salary INTEGER);   -- no primary key: a loader may repeat a row
INSERT INTO employees VALUES
 (1,NULL,100),   -- real root: NULL manager
 (2,1,50),(3,1,40),(3,1,40),   -- the last two rows are the same edge twice
 (4,2,30),
 (5,99,35),      -- 99 does not exist: orphan
 (6,7,20),(7,6,25);   -- 2-cycle, unreachable from the root
"""
SQL_ROLLUP = """
WITH RECURSIVE t(emp_id, level, salary) AS (
  SELECT emp_id, 0, salary FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, t.level + 1, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 10
)
SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people, SUM(salary) AS total_salary FROM t
"""
SQL_NULL_ANCHOR = SQL_ROLLUP.replace("manager_id IS NULL", "manager_id = NULL")
SQL_CYCLE_ALL = """
WITH RECURSIVE t(emp_id, level, salary) AS (
  SELECT emp_id, 0, salary FROM employees WHERE emp_id = 6
  UNION ALL
  SELECT e.emp_id, t.level + 1, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
  {guard}
)
SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people FROM t
"""
SQL_UNION_BARE = """
WITH RECURSIVE t(emp_id, salary) AS (
  SELECT emp_id, salary FROM employees WHERE emp_id = 6
  UNION
  SELECT e.emp_id, e.salary FROM employees e JOIN t ON e.manager_id = t.emp_id
)
SELECT COUNT(*) AS result_rows FROM t
"""
SQL_UNION_LEVEL = """
WITH RECURSIVE t(emp_id, level) AS (
  SELECT emp_id, 0 FROM employees WHERE emp_id = 6
  UNION
  SELECT e.emp_id, t.level + 1 FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 10
)
SELECT COUNT(*) AS result_rows FROM t
"""
SQL_PATH = """
WITH RECURSIVE t(emp_id, path) AS (
  SELECT emp_id, ',' || emp_id || ',' FROM employees WHERE emp_id = 6
  UNION ALL
  SELECT e.emp_id, t.path || e.emp_id || ','
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE instr(t.path, ',' || e.emp_id || ',') = 0
)
SELECT COUNT(*) AS result_rows FROM t
"""
SQL_PEERS = "SELECT COUNT(*) FROM employees a JOIN employees b ON a.manager_id = b.manager_id"
SQL_LOOPERS = """
WITH RECURSIVE w(start, cur) AS (
  SELECT emp_id, manager_id FROM employees WHERE manager_id IS NOT NULL
  UNION
  SELECT w.start, e.manager_id FROM w JOIN employees e ON e.emp_id = w.cur WHERE e.manager_id IS NOT NULL
)
SELECT DISTINCT start FROM w WHERE cur = start ORDER BY 1
"""
SQL_CHECKS = {
  "duplicate emp_id rows": "SELECT emp_id FROM employees GROUP BY emp_id HAVING COUNT(*) > 1",
  "orphans": "SELECT emp_id FROM employees e WHERE manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)",
  "roots": "SELECT DISTINCT emp_id FROM employees WHERE manager_id IS NULL",
}
SQL_CLEAN = """
CREATE TABLE emp_clean AS
SELECT DISTINCT emp_id,
       CASE WHEN emp_id IN (SELECT start FROM ({loopers})) AND emp_id = (SELECT MIN(start) FROM ({loopers}))
            THEN NULL ELSE manager_id END AS manager_id,
       salary
FROM employees e
WHERE manager_id IS NULL OR EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda sql: con.execute(sql).fetchall()
print("raw table: duplicates", [r[0] for r in q(SQL_CHECKS["duplicate emp_id rows"])], "| orphans", [r[0] for r in q(SQL_CHECKS["orphans"])],
      "| roots", [r[0] for r in q(SQL_CHECKS["roots"])], "| members of a loop", [r[0] for r in q(SQL_LOOPERS)])
sql_raw = q(SQL_ROLLUP)[0]
print("SQL UNION ALL from the NULL root (rows, people, salary):", sql_raw, "| true salary of root 1's tree is 220")
print("SQL anchor written as manager_id = NULL:", q(SQL_NULL_ANCHOR)[0])
cycle_runs = {
    "UNION ALL, depth cap 5": q(SQL_CYCLE_ALL.format(guard="WHERE t.level < 5"))[0][0],
    "UNION ALL, no guard, outer LIMIT 8": len(q(SQL_CYCLE_ALL.format(guard="").replace(
        "SELECT COUNT(*) AS result_rows, COUNT(DISTINCT emp_id) AS people FROM t", "SELECT * FROM t LIMIT 8"))),
    "UNION ALL, path guard": q(SQL_PATH)[0][0],
    "UNION on (emp_id, salary), no level column": q(SQL_UNION_BARE)[0][0],
    "UNION with a level column, cap 10": q(SQL_UNION_LEVEL)[0][0],
}
print("SQL from the loop (anchor emp 6), result rows:", cycle_runs)
sql_peers = q(SQL_PEERS)[0][0]

employees = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
def reports(emp, roots, guard=True, cap=10):
    """Frontier merge from the given root ids; returns one row per output row (emp_id, level, salary)."""
    kids = emp.rename(columns={"emp_id": "child", "salary": "child_salary"})
    frontier = emp[emp["emp_id"].isin(roots)].rename(columns={"salary": "child_salary"}).assign(child=lambda d: d["emp_id"], level=0)
    frontier = frontier[["child", "child_salary", "level"]]
    parts, seen = [frontier], set(frontier["child"])
    for _ in range(cap):
        nxt = frontier.merge(kids, left_on="child", right_on="manager_id", suffixes=("_p", ""))
        if guard:
            nxt = nxt[~nxt["child"].isin(seen)].drop_duplicates("child")
        frontier = pd.DataFrame({"child": nxt["child"], "child_salary": nxt["child_salary"], "level": nxt["level"] + 1})
        if not len(frontier):
            break
        seen.update(frontier["child"])
        parts.append(frontier)
    out = pd.concat(parts, ignore_index=True)
    return out.rename(columns={"child": "emp_id", "child_salary": "salary"})

def clean(emp):
    emp = emp.drop_duplicates()                                                     # repeated edge rows
    orphan = emp["manager_id"].notna() & ~emp["manager_id"].isin(emp["emp_id"])     # unknown manager: set aside
    emp = emp[~orphan]
    loops = loop_members(emp)
    if loops:
        emp = emp.assign(manager_id=emp["manager_id"].where(emp["emp_id"] != min(loops)))   # break each loop at its smallest id
    return emp.reset_index(drop=True)

def loop_members(emp):
    par = dict(zip(emp["emp_id"], emp["manager_id"]))
    out = set()
    for s in par:
        cur, hops = par[s], 0
        while pd.notna(cur) and cur in par and hops <= len(par):
            if cur == s:
                out.add(s)
                break
            cur, hops = par[cur], hops + 1
    return out
# pd:end

root = employees[employees["manager_id"].isna()]["emp_id"].tolist()
raw = reports(employees, root, guard=False)
assert (len(raw), raw["emp_id"].nunique(), int(raw["salary"].sum())) == sql_raw
print("\npandas merge loop from the NaN root, no guard:", (len(raw), raw["emp_id"].nunique(), int(raw["salary"].sum())), "(same as SQL UNION ALL)")
guarded = reports(employees, root, guard=True)
print("pandas with visited set + drop_duplicates:", (len(guarded), guarded["emp_id"].nunique(), int(guarded["salary"].sum())))
print("pandas employees.manager_id == np.nan selects", int((employees["manager_id"] == float("nan")).sum()), "rows; isna() selects", len(root))
cyc_nog = reports(employees, [6], guard=False, cap=5)
cyc_g = reports(employees, [6], guard=True)
print("pandas from the loop: no guard, cap 5 ->", len(cyc_nog), "rows; visited set ->", len(cyc_g), "rows")
pd_peers = len(employees.merge(employees, on="manager_id"))
pd_peers_fixed = len(employees.dropna(subset=["manager_id"]).merge(employees.dropna(subset=["manager_id"]), on="manager_id"))
print("same-manager pairs: SQL", sql_peers, "| pandas merge", pd_peers, "| pandas after dropna", pd_peers_fixed)
assert pd_peers == sql_peers + 1 and pd_peers_fixed == sql_peers

# cleaning: dedupe, set aside orphans, break loops; then both engines must agree
con.execute(SQL_CLEAN.format(loopers=SQL_LOOPERS.strip().replace(chr(10), " ")))
clean_sql = pd.read_sql_query("SELECT * FROM emp_clean ORDER BY emp_id", con)
clean_pd = clean(employees).sort_values("emp_id").reset_index(drop=True)
clean_sql["manager_id"] = clean_sql["manager_id"].astype("Int64")
clean_pd["manager_id"] = clean_pd["manager_id"].astype("Int64")
pd.testing.assert_frame_equal(clean_pd, clean_sql, check_dtype=False)
print("\ncleaned table (SQL and pandas identical after sorting by emp_id):")
print(clean_sql.to_string(index=False))
sql_clean_roll = con.execute(SQL_ROLLUP.replace("FROM employees", "FROM emp_clean").replace("JOIN employees", "JOIN emp_clean")).fetchone()
roots_clean = clean_pd[clean_pd["manager_id"].isna()]["emp_id"].tolist()
pd_clean_roll = reports(clean_pd, roots_clean, guard=False)
assert sql_clean_roll == (len(pd_clean_roll), pd_clean_roll["emp_id"].nunique(), int(pd_clean_roll["salary"].sum()))
print("after cleaning, UNION ALL roll-up from all roots: SQL", sql_clean_roll, "| pandas", (len(pd_clean_roll), pd_clean_roll["emp_id"].nunique(), int(pd_clean_roll["salary"].sum())), "no guard needed")
print("asserts passed")
```

**Output (my run):**
```text
raw table: duplicates [3] | orphans [5] | roots [1] | members of a loop [6, 7]
SQL UNION ALL from the NULL root (rows, people, salary): (5, 4, 260) | true salary of root 1's tree is 220
SQL anchor written as manager_id = NULL: (0, 0, None)
SQL from the loop (anchor emp 6), result rows: {'UNION ALL, depth cap 5': 6, 'UNION ALL, no guard, outer LIMIT 8': 8, 'UNION ALL, path guard': 2, 'UNION on (emp_id, salary), no level column': 2, 'UNION with a level column, cap 10': 11}

pandas merge loop from the NaN root, no guard: (5, 4, 260) (same as SQL UNION ALL)
pandas with visited set + drop_duplicates: (4, 4, 220)
pandas employees.manager_id == np.nan selects 0 rows; isna() selects 1
pandas from the loop: no guard, cap 5 -> 6 rows; visited set -> 2 rows
same-manager pairs: SQL 13 | pandas merge 14 | pandas after dropna 13

cleaned table (SQL and pandas identical after sorting by emp_id):
 emp_id  manager_id  salary
      1        <NA>     100
      2           1      50
      3           1      40
      4           2      30
      6        <NA>      20
      7           6      25
after cleaning, UNION ALL roll-up from all roots: SQL (6, 6, 265) | pandas (6, 6, 265) no guard needed
asserts passed
```

**Edge cases:**
- Duplicate edges: the full-row duplicate (3, 1, 40) is removed by `DISTINCT` or `drop_duplicates()`. If the duplicates differ in salary (a data error, not run here), `DISTINCT` keeps both and the cleaning needs a rule for which to keep.
- NULL parent that is a real root: keep it as a root; do not drop it, and do not join on it. The pandas merge matching NaN to NaN is a bug source in sibling-style joins (14 versus 13 pairs in the table above; Q25 shows 20 versus 19 on its own tree) but it is also why a pandas anchor test with `==` fails silently.
- Orphan: decide a policy (treat as a root, quarantine, or fail the load). I set it aside, so its salary (35) is not in the 265 total; a policy of "treat as a root" would add it.
- 2-cycle that is not reachable from the root: a roll-up from the root never sees it, so it does not hang; it hangs only when you start from a member (or start from every row). `UNION` with a level column does not stop a loop (11 rows until the cap), `UNION` on bare ids does.
- Self-managed row (`emp_id = manager_id`): a loop of length 1; `SQL_LOOPERS` finds it (start = cur); not in the sample data and not run here.
- Empty table: the anchor returns nothing, SQL and pandas both return empty results; not run for this table.

**Then explain:**
- Why the engines differ: SQL three-valued logic makes `NULL = NULL` unknown, so it is not a match; pandas treats NaN keys as equal in `merge` by default.
- Why duplicates double count: a recursive CTE with `UNION ALL` and a merge loop both produce one output row per matching edge row; two identical edge rows give two rows per level.
- Guards compared: depth cap (finite, but wrong rows repeat), path string (exact for simple paths), `UNION` on columns that do not grow (cheap, hides duplicates), visited set in pandas (finite and exact).
- Cleaning order that makes both agree: dedupe, flag and set aside orphans, find loop members, break each loop at a deterministic member, then the data is a forest and `UNION ALL` is safe. I asserted the cleaned tables and roll-ups equal.
- Other engines: PostgreSQL 14+ `CYCLE`, SQL Server `MAXRECURSION`, MySQL `cte_max_recursion_depth` would stop or mark the loop differently (hedged, not executed).

**Follow-ups:**
- How do you stop this at load time? A primary key on `emp_id`, a foreign key on `manager_id`, and a check query for loops before publishing (a database cannot easily enforce acyclicity with a constraint).
- Which loop member do you break? Any deterministic rule (smallest id here); the business may have a better one, so report the loop rather than hide it.
- Is `UNION` always a safe guard? Only when the other columns cannot differ between visits; adding a depth or path column makes rows distinct again.

**Common mistakes:**
- Writing `manager_id = NULL` for the anchor (SQL) or `== np.nan` (pandas).
- Trusting a roll-up total without reconciling it to the table total (260 and 220 against 300 for the salaries of the seven distinct people in the table).
- Fixing a loop with a bigger depth cap.
- Dropping the NULL root to avoid the NaN merge problem.
- Comparing SQL and pandas outputs without cleaning and sorting first.

### Q29 ⭐ 🔴 Performance and safety of recursive queries: employees with 50,000 rows in a balanced tree (about 6 levels) and a chain table of 2,000 nodes in a straight line, plus a lattice DAG where the number of paths doubles per level. Time the subtree query with and without an index on manager_id, show EXPLAIN QUERY PLAN in SQLite (executed), show that UNION ALL path enumeration on the lattice explodes (count paths at 10, 15, 20 levels) while DISTINCT node reachability stays linear, and list the guards (depth counters, LIMIT in the recursive member, per-engine recursion limits, timeouts). Report the real timings honestly as machine specific.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** A recursive subtree query is fast when `manager_id` is indexed (each level is an index lookup per frontier row) and catastrophic when it is not, `UNION ALL` path enumeration on a DAG grows with the number of paths (doubling per level in my lattice) while `UNION` reachability stays linear in nodes, and the guards are a depth counter, `LIMIT`, `UNION` on non-growing columns and the engine's own recursion cap; every timing below is from one run on this machine and will differ on yours.

**Schema and sample data:** nothing small to check by hand here, so the data is generated in the Code block and the logic is checked on counts. `emp(emp_id INTEGER PRIMARY KEY, manager_id INTEGER)` has 50,000 rows in a balanced tree: emp 1 is the root and emp i (i >= 2) reports to `(i - 2) / 8 + 1`, so every manager has up to 8 reports and the deepest level is 6 (seven levels counting the root). `chain` has 2,000 nodes in a straight line (each reports to the previous). `lattice(src, dst)` has two nodes per level and every node links to both nodes of the next level, so the number of paths from the start doubles at each level.
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);          -- 50,000 rows, generated in Python
CREATE TABLE chain(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);        -- 2,000 rows, emp i reports to i - 1
CREATE TABLE lattice(src TEXT, dst TEXT);                                  -- (level l, a) to (level l+1, b) for a, b in {0, 1}
```

**SQL answer:** the subtree count (the template used for the tree and the chain; `{t}`, `{root}`, `{cap}` are filled in by the script) and the two lattice queries, all in the Code block:
```sql
WITH RECURSIVE s(emp_id, level) AS (
  SELECT emp_id, 0 FROM {t} WHERE emp_id = {root}
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM {t} e JOIN s ON e.manager_id = s.emp_id
  WHERE s.level < {cap}
)
SELECT COUNT(*) AS people, MAX(level) AS max_level FROM s
```
Path enumeration (one row per path) versus reachability (one row per node):
```sql
WITH RECURSIVE p(node, depth) AS (
  SELECT '0_0', 0
  UNION ALL
  SELECT l.dst, p.depth + 1 FROM p JOIN lattice l ON l.src = p.node
)
SELECT COUNT(*) AS rows_made, SUM(depth = {levels}) AS paths_to_last_level FROM p
```
```sql
WITH RECURSIVE r(node) AS (
  SELECT '0_0'
  UNION
  SELECT l.dst FROM r JOIN lattice l ON l.src = r.node
)
SELECT COUNT(*) AS nodes_reached FROM r
```

**pandas answer:** the frontier merge on the same 50,000-row frame (the count and the deepest level are asserted equal to the SQL result; the merge is on `Int64` ids). Shown once here and identical to the Code block:
```py
frontier = emp.loc[emp["emp_id"] == 2, ["emp_id"]].assign(level=0)
total, merges, deepest = 1, 0, 0
while len(frontier):
    nxt = frontier.merge(emp, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
    merges += 1
    frontier = pd.DataFrame({"emp_id": nxt["emp_id"], "level": nxt["level"] + 1})
    total += len(frontier)
    deepest = deepest + 1 if len(frontier) else deepest
```

**Example:** the subtree of manager 2 on the 50,000-row tree has 17,232 people and reaches level 5. The recursive step runs once per level but processes every frontier row: for each manager in the queue it needs "all employees with `manager_id` = this id". With an index on `manager_id` that is a lookup; without one, it is a scan of the table per frontier row. The plans I ran: default (SQLite built an automatic covering index and added a bloom filter: `SEARCH e USING AUTOMATIC COVERING INDEX (manager_id=?)`), automatic indexing switched off with no index (`SCAN e` inside the recursive step, a full table scan for each frontier row), and my own index (`SEARCH e USING COVERING INDEX emp_mgr (manager_id=?)`). Lattice by hand: level 1 has 2 paths, level 2 has 4, level l has 2^l; so 10 levels make 1,024 paths and 20 levels make 1,048,576, while the number of distinct nodes reached is 2 per level plus the start: 21, 31 and 41.

**Code:** run with `python3 -I`. It builds the data, prints `EXPLAIN QUERY PLAN`, times each variant (best of 3 runs, one run for the very slow no-index case), asserts the three subtree counts are identical and that the lattice counts equal 2^levels, and prints the pandas timing. The assertions cover correctness only; the printed seconds are machine specific.
```python
import sqlite3
import time
import pandas as pd

SQL_SUBTREE = """
WITH RECURSIVE s(emp_id, level) AS (
  SELECT emp_id, 0 FROM {t} WHERE emp_id = {root}
  UNION ALL
  SELECT e.emp_id, s.level + 1 FROM {t} e JOIN s ON e.manager_id = s.emp_id
  WHERE s.level < {cap}
)
SELECT COUNT(*) AS people, MAX(level) AS max_level FROM s
"""
SQL_PATHS = """
WITH RECURSIVE p(node, depth) AS (
  SELECT '0_0', 0
  UNION ALL
  SELECT l.dst, p.depth + 1 FROM p JOIN lattice l ON l.src = p.node
)
SELECT COUNT(*) AS rows_made, SUM(depth = {levels}) AS paths_to_last_level FROM p
"""
SQL_REACH = """
WITH RECURSIVE r(node) AS (
  SELECT '0_0'
  UNION
  SELECT l.dst FROM r JOIN lattice l ON l.src = r.node
)
SELECT COUNT(*) AS nodes_reached FROM r
"""

def timed(con, sql, repeat=3):
    best, res = None, None
    for _ in range(repeat):
        t0 = time.perf_counter()
        res = con.execute(sql).fetchone()
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
    return res, best

def plan(con, sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

con = sqlite3.connect(":memory:")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__, "(all timings are from this machine and this run only)")
con.execute("CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, manager_id INTEGER)")
con.executemany("INSERT INTO emp VALUES (?, ?)", [(1, None)] + [(i, (i - 2) // 8 + 1) for i in range(2, 50001)])
con.execute("CREATE TABLE chain(emp_id INTEGER PRIMARY KEY, manager_id INTEGER)")
con.executemany("INSERT INTO chain VALUES (?, ?)", [(1, None)] + [(i, i - 1) for i in range(2, 2001)])
print("tree:", con.execute("SELECT COUNT(*), MAX(level) FROM (WITH RECURSIVE s(emp_id, level) AS (SELECT 1, 0 UNION ALL SELECT e.emp_id, s.level + 1 FROM emp e JOIN s ON e.manager_id = s.emp_id) SELECT * FROM s)").fetchone(),
      "(rows, deepest level); 8 children per node")

q2 = SQL_SUBTREE.format(t="emp", root=2, cap=100)
qroot = SQL_SUBTREE.format(t="emp", root=1, cap=100)
res = {}
print("\nSubtree of manager 2 on the 50,000-row table:")
con.execute("PRAGMA automatic_index = ON")
r, t = timed(con, q2)
res["default (automatic index allowed, no explicit index)"] = (r, t)
print("  plan:", plan(con, q2))
con.execute("PRAGMA automatic_index = OFF")
r, t = timed(con, q2, repeat=1)
res["automatic_index OFF, no index on manager_id"] = (r, t)
print("  plan:", plan(con, q2))
con.execute("CREATE INDEX emp_mgr ON emp(manager_id)")
r, t = timed(con, q2)
res["explicit index on manager_id"] = (r, t)
print("  plan:", plan(con, q2))
for k, (r, t) in res.items():
    print(f"  {k}: people={r[0]}, max_level={r[1]}, best time {t:.3f} s")
assert len({v[0] for v in res.values()}) == 1
r, t = timed(con, qroot)
print(f"Whole company (root 1) with the index: people={r[0]}, max_level={r[1]}, best time {t:.3f} s")

# pandas frontier merge on the same data
emp = pd.read_sql_query("SELECT * FROM emp", con)
emp["manager_id"] = emp["manager_id"].astype("Int64")
t0 = time.perf_counter()
# pd:main
frontier = emp.loc[emp["emp_id"] == 2, ["emp_id"]].assign(level=0)
total, merges, deepest = 1, 0, 0
while len(frontier):
    nxt = frontier.merge(emp, left_on="emp_id", right_on="manager_id", suffixes=("_p", ""))
    merges += 1
    frontier = pd.DataFrame({"emp_id": nxt["emp_id"], "level": nxt["level"] + 1})
    total += len(frontier)
    deepest = deepest + 1 if len(frontier) else deepest
# pd:end
dt = time.perf_counter() - t0
assert (total, deepest) == res["explicit index on manager_id"][0]
print(f"pandas frontier merge, subtree of 2: people={total}, max_level={deepest}, {merges} merges, {dt:.3f} s")

print("\nChain of 2,000 nodes (depth 1999), with an index on manager_id:")
con.execute("CREATE INDEX chain_mgr ON chain(manager_id)")
r, t = timed(con, SQL_SUBTREE.format(t="chain", root=1, cap=5000))
print(f"  people={r[0]}, max_level={r[1]}, best time {t:.3f} s (no recursion limit in SQLite; a depth cap of 5000 was set by me)")
r2, _ = timed(con, SQL_SUBTREE.format(t="chain", root=1, cap=100), repeat=1)
print(f"  with the usual depth cap of 100 the answer is silently truncated: people={r2[0]}, max_level={r2[1]}")

print("\nLattice DAG: 2 nodes per level, every node links to both nodes of the next level; start at 0_0")
for levels in (10, 15, 20):
    con.execute("DROP TABLE IF EXISTS lattice")
    con.execute("CREATE TABLE lattice(src TEXT, dst TEXT)")
    con.executemany("INSERT INTO lattice VALUES (?, ?)",
                    [(f"{l}_{a}", f"{l + 1}_{b}") for l in range(levels) for a in (0, 1) for b in (0, 1)])
    con.execute("CREATE INDEX lattice_src ON lattice(src)")
    rp, tp = timed(con, SQL_PATHS.format(levels=levels), repeat=1)
    rr, tr = timed(con, SQL_REACH, repeat=1)
    assert rp[1] == 2 ** levels and rp[0] == 2 ** (levels + 1) - 1
    print(f"  {levels:2d} levels: UNION ALL made {rp[0]} rows, {rp[1]} paths to the last level (2^{levels}), {tp:.3f} s | "
          f"UNION reached {rr[0]} nodes, {tr:.4f} s")
print("asserts passed")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5 (all timings are from this machine and this run only)
tree: (50000, 6) (rows, deepest level); 8 children per node

Subtree of manager 2 on the 50,000-row table:
  plan: ['CO-ROUTINE s', 'SETUP', 'SEARCH emp USING INTEGER PRIMARY KEY (rowid=?)', 'RECURSIVE STEP', 'SCAN s', 'BLOOM FILTER ON e (manager_id=?)', 'SEARCH e USING AUTOMATIC COVERING INDEX (manager_id=?)', 'SCAN s']
  plan: ['CO-ROUTINE s', 'SETUP', 'SEARCH emp USING INTEGER PRIMARY KEY (rowid=?)', 'RECURSIVE STEP', 'SCAN s', 'SCAN e', 'SCAN s']
  plan: ['CO-ROUTINE s', 'SETUP', 'SEARCH emp USING INTEGER PRIMARY KEY (rowid=?)', 'RECURSIVE STEP', 'SCAN s', 'SEARCH e USING COVERING INDEX emp_mgr (manager_id=?)', 'SCAN s']
  default (automatic index allowed, no explicit index): people=17232, max_level=5, best time 0.012 s
  automatic_index OFF, no index on manager_id: people=17232, max_level=5, best time 19.968 s
  explicit index on manager_id: people=17232, max_level=5, best time 0.007 s
Whole company (root 1) with the index: people=50000, max_level=6, best time 0.020 s
pandas frontier merge, subtree of 2: people=17232, max_level=5, 6 merges, 0.015 s

Chain of 2,000 nodes (depth 1999), with an index on manager_id:
  people=2000, max_level=1999, best time 0.001 s (no recursion limit in SQLite; a depth cap of 5000 was set by me)
  with the usual depth cap of 100 the answer is silently truncated: people=101, max_level=100

Lattice DAG: 2 nodes per level, every node links to both nodes of the next level; start at 0_0
  10 levels: UNION ALL made 2047 rows, 1024 paths to the last level (2^10), 0.001 s | UNION reached 21 nodes, 0.0000 s
  15 levels: UNION ALL made 65535 rows, 32768 paths to the last level (2^15), 0.030 s | UNION reached 31 nodes, 0.0001 s
  20 levels: UNION ALL made 2097151 rows, 1048576 paths to the last level (2^20), 0.967 s | UNION reached 41 nodes, 0.0002 s
asserts passed
```

**Edge cases:**
- Timings in my run (SQLite 3.45.1, pandas 3.0.5, this machine only; yours will differ, so treat the ratios, not the seconds, as the finding): subtree of manager 2 (17,232 people) took 0.012 s with SQLite's automatic index, 0.007 s with an explicit index and 19.968 s with automatic indexing switched off and no index. The whole company (50,000 people) took 0.020 s with the index. The pandas frontier merge took 0.015 s for the same subtree with 6 merges. The answers were identical in all variants. So the missing index is not a small slowdown, it is the difference between milliseconds and tens of seconds, but SQLite hides it by default with an automatic index (not every engine does that, hedged).
- Chain of 2,000 nodes: with a depth cap of 5000 the full chain came back in about a millisecond (2,000 people, deepest level 1,999). With the usual-looking cap of 100 the answer was silently truncated to 101 people. In SQLite there is no built-in recursion limit (Q21 counted to 1,000,000 without error). Other engines, not executed here: SQL Server stops at 100 levels by default with an error and MySQL at 1000 (`cte_max_recursion_depth`), so a 2,000-deep chain would need the limit raised there.
- Lattice: `UNION ALL` produced 2,047 rows at 10 levels, 65,535 at 15 and 2,097,151 at 20 (1,048,576 paths to the last level); the reachability query returned 21, 31 and 41 nodes. Elapsed times in my run: 0.001 s, 0.030 s and 0.967 s for path enumeration versus under a millisecond for reachability. The explosion is in rows, which also means memory (the whole queue can grow), not only time.
- Cycles: a loop makes the path count infinite; the guards are in the next section.
- Skewed trees (one manager with thousands of reports) make one frontier huge; the cost is still about the number of rows touched.

**Then explain:**
- Where the time goes: each iteration takes the rows produced by the previous iteration, joins them to the table, and the cost is roughly (rows produced) times (cost of one lookup). Index on the join column makes a lookup cheap. An index on `emp_id` as the primary key serves the anchor.
- Output size is the lower bound: a subtree query cannot be cheaper than the number of people it returns; path enumeration returns paths, so on a DAG it can be much larger than the node count.
- Reachability (`UNION` on node ids) versus enumeration (`UNION ALL`): if you only need to know which nodes can be reached, deduplicate so each node is expanded once; if you need every path or a cost per path you pay for the paths.
- Guards: a depth counter column with `WHERE depth < N` (the portable one), an outer `LIMIT` (I used it in Q28 to stop a loop at 8 rows; SQLite stops producing when the limit is reached), a path string with `instr` for loops, `UNION` on columns that cannot grow, and engine-specific caps and timeouts. Engine caps, hedged and not executed: SQL Server `OPTION (MAXRECURSION n)` default 100, MySQL `cte_max_recursion_depth` default 1000 plus `max_execution_time`, PostgreSQL has no default iteration cap but has the `CYCLE` clause from 14 and `statement_timeout`.
- Recursion cannot use aggregates or reference the CTE twice in SQLite (checked in Q21), so "remember visited nodes" is a `UNION` or a path column, not a subquery.
- Window functions are not part of this question (Parts 4-5).

**Follow-ups:**
- How would you speed up very frequent subtree queries? Store a materialized path or a closure table (Q24) and index it, so a read becomes an index range or lookup.
- What if the table is 50 million rows? Index first, limit depth, filter in the anchor (a small subtree), and consider precomputing; I did not benchmark anything at that size.
- How do you see the plan? `EXPLAIN QUERY PLAN` in SQLite (run above); other engines use their own `EXPLAIN` forms (not executed; Part 11 covers plans).

**Common mistakes:**
- No index on the join column of the recursive step.
- Enumerating paths when only reachability is needed.
- A depth cap that is smaller than the real depth: the result is silently truncated (101 people instead of 2,000 above).
- Quoting a timing without saying machine and run; mine is one run on one machine.
- Raising the engine's recursion limit to hide a loop.

### Q30 ⭐ 🔴 Lowest common ancestor and path between two employees: employees(emp_id, manager_id, name). For employees 10 and 12 return their lowest common manager and the number of hops between them. Use the upward chain CTE for each employee (ancestor, distance), join the two on the ancestor, and take the minimum of the sum of distances (a tie-free tree gives one answer). Show what happens when the two are in different trees (no common ancestor, a forest with two roots) and when one is an ancestor of the other, and compare with a materialized-path longest common prefix solution.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Build the upward chain of ancestors with distances for each of the two employees (including the employee himself at distance 0), join the two chains on the ancestor, and take the row with the smallest sum of distances: that ancestor is the lowest common manager and the sum is the number of hops; if the chains share nothing the two are in different trees and there is no answer.

**Schema and sample data:** the twelve-employee company (Tim is the CEO), plus Tej (emp 30, a report of Radha) to test ids that share a prefix, plus a second company with its own root: Zed (20, NULL manager) and Uma (21, reports to Zed), so the data is a forest with two roots.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,2,'Hari'),(4,3,'Shyam'),(5,1,'Meera'),
 (6,5,'Kiran'),(7,3,'Asha'),(8,6,'Dev'),(9,5,'Isha'),(10,4,'Ram'),
 (11,4,'Zoya'),(12,7,'Nina'),
 (30,2,'Tej'),
 (20,NULL,'Zed'),(21,20,'Uma');     -- a second company: a forest with two roots
```

**SQL answer:** `SQL_MAIN` in the Code block (`{a}` and `{b}` are filled in by the script; the example is 10 and 12):
```sql
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees WHERE emp_id IN ({a}, {b})
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
)
SELECT x.ancestor AS lca, x.dist + y.dist AS hops
FROM up x JOIN up y ON y.ancestor = x.ancestor
WHERE x.start = {a} AND y.start = {b}
ORDER BY hops LIMIT 1
```
`LIMIT 1` after `ORDER BY hops` takes the smallest sum; in a tree the minimum is unique, so there is no tie to break. The `WHERE e.manager_id IS NOT NULL` stops the chain at the root.

Materialized-path version (`SQL_MATPATH`): build each employee's path (`/1/2/3/4/10/`), take the longest common character prefix of the two paths with a small recursive counter, cut it back to the last `/` with `rtrim(common, replace(common, '/', ''))` (which strips trailing digits), and look up the employee whose path is that prefix; hops come from the slash counts (depth of each minus twice the depth of the common ancestor):
```sql
WITH RECURSIVE mp(emp_id, path) AS (
  SELECT emp_id, '/' || emp_id || '/' FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, mp.path || e.emp_id || '/' FROM employees e JOIN mp ON e.manager_id = mp.emp_id
), pick AS (
  SELECT (SELECT path FROM mp WHERE emp_id = {a}) AS pa, (SELECT path FROM mp WHERE emp_id = {b}) AS pb
), lcp(n) AS (
  SELECT 0
  UNION ALL
  SELECT n + 1 FROM lcp, pick WHERE n < length(pa) AND n < length(pb) AND substr(pa, n + 1, 1) = substr(pb, n + 1, 1)
), cut AS (
  SELECT substr(pa, 1, MAX(n)) AS common, pa, pb FROM lcp, pick
)
SELECT m.emp_id AS lca,
       (length(pa) - length(replace(pa, '/', '')) - 1) + (length(pb) - length(replace(pb, '/', '')) - 1)
         - 2 * (length(rtrim(common, replace(common, '/', ''))) - length(replace(rtrim(common, replace(common, '/', '')), '/', '')) - 1) AS hops
FROM cut JOIN mp m ON m.path = rtrim(common, replace(common, '/', ''))
```
Also in the Code block is `SQL_ALL_PAIRS`, the chain join for every pair of employees at once; it picks the best candidate per pair with `ROW_NUMBER` (window functions are covered in Parts 4-5) so that the whole table can be compared with the Python answer.

**pandas answer:** the chain of each employee as a dict (ancestor to distance) from a walk up the manager column; the common ancestors are the intersection of the two key sets, and the answer is the one with the smallest sum of distances. Shown once here and identical to the Code block:
```py
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
def up_chain(i):
    out = {i: 0}
    while not pd.isna(parent[i]):
        i = int(parent[i])
        out[i] = len(out)
    return out

def lca_pandas(a, b):
    ca, cb = up_chain(a), up_chain(b)
    common = set(ca) & set(cb)
    if not common:
        return None
    best = min(common, key=lambda x: (ca[x] + cb[x], x))
    return best, ca[best] + cb[best]
```

**Example:** employee 10 (Ram) has the chain Ram 0, Shyam 1, Hari 2, Radha 3, Tim 4. Employee 12 (Nina) has Nina 0, Asha 1, Hari 2, Radha 3, Tim 4. The common ancestors are Hari, Radha and Tim with distance sums 2 + 2 = 4, 3 + 3 = 6 and 4 + 4 = 8; the minimum is 4, so the lowest common manager is Hari and the number of hops between them is 4 (Ram, Shyam, Hari, Asha, Nina). The other cases:
- One is the ancestor of the other (4 and 10): Shyam's own chain contains Shyam at distance 0, so the common ancestor is Shyam with 0 + 1 = 1 hop. This is why each chain must include the employee himself.
- Same employee (10 and 10): the LCA is Ram, 0 hops.
- Different trees (10 and 21): Ram's chain ends at Tim, Uma's at Zed; no common ancestor, no row (SQL returns nothing, my function returns `None`).
- Ids that share a prefix (10 and 30): the paths are `/1/2/3/4/10/` and `/1/2/30/`; the longest common character prefix is `/1/2/3`, which is not an ancestor (3 is not a prefix of 30); cutting back to the last slash gives `/1/2/`, so the answer is Radha (2) with 4 hops. A naive prefix check without the cut would return Hari (3), wrong.

**Code:** run with `python3 -I`. It checks six cases (SQL chain join equals the materialized-path SQL equals the pandas walk), then compares the all-pairs SQL result with the pandas answer for every pair of employees (rows ordered by `a, b`; pairs across the two companies have no row in either), then checks every connected pair against `networkx.lowest_common_ancestor`.
```python
import sqlite3
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,2,'Hari'),(4,3,'Shyam'),(5,1,'Meera'),
 (6,5,'Kiran'),(7,3,'Asha'),(8,6,'Dev'),(9,5,'Isha'),(10,4,'Ram'),
 (11,4,'Zoya'),(12,7,'Nina'),
 (30,2,'Tej'),
 (20,NULL,'Zed'),(21,20,'Uma');     -- a second company: a forest with two roots
"""
SQL_MAIN = """
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees WHERE emp_id IN ({a}, {b})
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
)
SELECT x.ancestor AS lca, x.dist + y.dist AS hops
FROM up x JOIN up y ON y.ancestor = x.ancestor
WHERE x.start = {a} AND y.start = {b}
ORDER BY hops LIMIT 1
"""
SQL_ALL_PAIRS = """
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
), cand AS (
  SELECT x.start AS a, y.start AS b, x.ancestor AS lca, x.dist + y.dist AS hops,
         ROW_NUMBER() OVER (PARTITION BY x.start, y.start ORDER BY x.dist + y.dist) AS rn
  FROM up x JOIN up y ON y.ancestor = x.ancestor
  WHERE x.start < y.start
)
SELECT a, b, lca, hops FROM cand WHERE rn = 1 ORDER BY a, b
"""
SQL_MATPATH = """
WITH RECURSIVE mp(emp_id, path) AS (
  SELECT emp_id, '/' || emp_id || '/' FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, mp.path || e.emp_id || '/' FROM employees e JOIN mp ON e.manager_id = mp.emp_id
), pick AS (
  SELECT (SELECT path FROM mp WHERE emp_id = {a}) AS pa, (SELECT path FROM mp WHERE emp_id = {b}) AS pb
), lcp(n) AS (
  SELECT 0
  UNION ALL
  SELECT n + 1 FROM lcp, pick WHERE n < length(pa) AND n < length(pb) AND substr(pa, n + 1, 1) = substr(pb, n + 1, 1)
), cut AS (
  SELECT substr(pa, 1, MAX(n)) AS common, pa, pb FROM lcp, pick
)
SELECT m.emp_id AS lca,
       (length(pa) - length(replace(pa, '/', '')) - 1) + (length(pb) - length(replace(pb, '/', '')) - 1)
         - 2 * (length(rtrim(common, replace(common, '/', ''))) - length(replace(rtrim(common, replace(common, '/', '')), '/', '')) - 1) AS hops
FROM cut JOIN mp m ON m.path = rtrim(common, replace(common, '/', ''))
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
names = dict(con.execute("SELECT emp_id, name FROM employees").fetchall())

def lca_sql(a, b):
    rows = con.execute(SQL_MAIN.format(a=a, b=b)).fetchall()
    return rows[0] if rows else None

def lca_matpath(a, b):
    rows = con.execute(SQL_MATPATH.format(a=a, b=b)).fetchall()
    return rows[0] if rows else None

cases = [("10 and 12 (the question)", 10, 12), ("4 and 10 (one is the ancestor of the other)", 4, 10),
         ("10 and 10 (same employee)", 10, 10), ("10 and 21 (different trees)", 10, 21),
         ("10 and 30 (ids '/1/2/3/4/10/' and '/1/2/30/')", 10, 30), ("8 and 11", 8, 11)]
print("case -> SQL chain join (lca, hops) | SQL materialized-path prefix (lca, hops)")
for label, a, b in cases:
    r1, r2 = lca_sql(a, b), lca_matpath(a, b)
    print(f"  {label}: {r1} ({names[r1[0]] if r1 else '-'}) | {r2}")
    assert r1 == r2

employees = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
def up_chain(i):
    out = {i: 0}
    while not pd.isna(parent[i]):
        i = int(parent[i])
        out[i] = len(out)
    return out

def lca_pandas(a, b):
    ca, cb = up_chain(a), up_chain(b)
    common = set(ca) & set(cb)
    if not common:
        return None
    best = min(common, key=lambda x: (ca[x] + cb[x], x))
    return best, ca[best] + cb[best]
# pd:end

for label, a, b in cases:
    assert lca_pandas(a, b) == lca_sql(a, b)
sql_all = pd.read_sql_query(SQL_ALL_PAIRS, con)
ids = sorted(employees["emp_id"])
rows = []
for i, a in enumerate(ids):
    for b in ids[i + 1:]:
        r = lca_pandas(a, b)
        if r is not None:
            rows.append((a, b, r[0], r[1]))
pd_all = pd.DataFrame(rows, columns=["a", "b", "lca", "hops"])
# compare after ordering by a, b (the SQL ORDER BY); pairs across the two companies have no row in either
pd.testing.assert_frame_equal(pd_all, sql_all, check_dtype=False)
print(f"\nall {len(sql_all)} connected pairs: SQL chain join == pandas dict walk; pairs across the two companies are absent in both")
print("number of employee pairs in total:", len(ids) * (len(ids) - 1) // 2, "| pairs with no common ancestor:", len(ids) * (len(ids) - 1) // 2 - len(sql_all))

# networkx check on the tree edges (manager -> report)
D = nx.DiGraph([(int(m), int(e)) for e, m in zip(employees["emp_id"], employees["manager_id"]) if pd.notna(m)])
D.add_nodes_from(ids)
for label, a, b in cases:
    got = None
    try:
        got = nx.lowest_common_ancestor(D, a, b)
    except Exception as ex:
        got = type(ex).__name__
    print(f"  networkx lowest_common_ancestor({a}, {b}) = {got}")
bad = 0
for a, b, lca, hops in sql_all.itertuples(index=False):
    got = nx.lowest_common_ancestor(D, a, b)
    bad += (got != lca)
print("networkx 3.6.1 lowest_common_ancestor disagrees with the SQL answer on", bad, "of", len(sql_all), "connected pairs")
print("asserts passed")
```

**Output (my run):**
```text
case -> SQL chain join (lca, hops) | SQL materialized-path prefix (lca, hops)
  10 and 12 (the question): (3, 4) (Hari) | (3, 4)
  4 and 10 (one is the ancestor of the other): (4, 1) (Shyam) | (4, 1)
  10 and 10 (same employee): (10, 0) (Ram) | (10, 0)
  10 and 21 (different trees): None (-) | None
  10 and 30 (ids '/1/2/3/4/10/' and '/1/2/30/'): (2, 4) (Radha) | (2, 4)
  8 and 11: (1, 7) (Tim) | (1, 7)

all 79 connected pairs: SQL chain join == pandas dict walk; pairs across the two companies are absent in both
number of employee pairs in total: 105 | pairs with no common ancestor: 26
  networkx lowest_common_ancestor(10, 12) = 3
  networkx lowest_common_ancestor(4, 10) = 4
  networkx lowest_common_ancestor(10, 10) = 10
  networkx lowest_common_ancestor(10, 21) = None
  networkx lowest_common_ancestor(10, 30) = 2
  networkx lowest_common_ancestor(8, 11) = 1
networkx 3.6.1 lowest_common_ancestor disagrees with the SQL answer on 0 of 79 connected pairs
asserts passed
```

**Edge cases:**
- Different trees: no common ancestor. In SQL the join returns zero rows (so a caller must handle the empty result); in pandas the intersection is empty; networkx returned `None` for 10 and 21 in my run. In my data 26 of the 105 employee pairs are across the two companies (no answer).
- One employee is an ancestor of the other: works because each chain includes distance 0 for the employee himself; without the distance-0 rows the common set would be Hari, Radha and Tim and the query would return Hari with 3 hops, which is wrong (the answer is Shyam with 1).
- Same employee: 0 hops, LCA is himself.
- NULL manager (the root): the upward recursion stops where `manager_id IS NULL` (that is what the guard is for); a NULL is never joined.
- Orphan (manager id missing from the table) would end the chain early, so two employees under such managers can look unrelated; not in this data and not run.
- A loop in the manager data would make the upward recursion run forever; add a depth cap or a path guard (Q8, Q15). Not run here for this query.
- Ties: in a tree the lowest common ancestor is unique. In a DAG (several parents) there can be several lowest common ancestors with the same sum, and `LIMIT 1` would pick one arbitrarily; not applicable here.
- All 105 pairs: 79 had a common manager and all 79 agree between SQL, the pandas walk and networkx; `networkx.lowest_common_ancestor` was called on a directed graph with edges manager to report, as at run time.

**Then explain:**
- Two upward chains are cheap: each is at most depth rows, so the cost is about the depth of the tree, not its size.
- The minimum of the distance sum picks the lowest (deepest) common ancestor: every ancestor above it is also common but strictly further from both.
- Hops equal `dist_a + dist_b` at the LCA because the path between two nodes in a tree goes up to the LCA and back down.
- Materialized path: the LCA is the longest common prefix cut at a separator; it needs no recursion at query time, at the price of storing and maintaining the path (Q24). The prefix must be cut at a separator, otherwise ids such as 3 and 30 fool it.
- Cross-engine: the recursive CTE form needs `WITH RECURSIVE` in SQLite, MySQL 8 and PostgreSQL and plain `WITH` in SQL Server (hedged, not executed); Oracle would use `CONNECT BY PRIOR` upwards (not executed).

**Follow-ups:**
- LCA of many employees at once? Intersect all the chains (the deepest common one), or take the longest common path prefix of all the paths.
- Distance between two employees without the LCA? Not possible in general for trees without it; for a materialized path it is `depth_a + depth_b - 2 * depth_lca`.
- Common manager but also the same department? Add the filter after finding the LCA, not in the chain, or you change the tree.

**Common mistakes:**
- Not including the employee himself in his own chain (breaks the "one is the ancestor of the other" case).
- Taking the first common ancestor found, or the minimum ancestor id, instead of the minimum sum of distances.
- Taking a character prefix of the paths without cutting at a separator (3 versus 30).
- Forgetting the empty result for different trees.
- Hops off by one (counting nodes instead of edges).

