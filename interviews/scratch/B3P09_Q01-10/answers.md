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
