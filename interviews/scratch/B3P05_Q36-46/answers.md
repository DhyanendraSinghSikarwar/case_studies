### Q36 ⭐ 🟡 EXCLUDE clauses for leave-one-out comparisons: employees(emp_id, dept_id, salary). Return each employee's salary versus the average of the other employees in the same department using AVG(salary) OVER (PARTITION BY dept_id ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING EXCLUDE CURRENT ROW), explain EXCLUDE GROUP and EXCLUDE TIES, show the portable equivalent (SUM OVER minus salary, divided by count minus 1), and say EXCLUDE exists in PostgreSQL 11+ (hedged) and not in MySQL.
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `AVG(salary) OVER (PARTITION BY dept_id ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING EXCLUDE CURRENT ROW)` averages everyone in the department except the row itself; the portable version is `(SUM OVER - own salary) / (COUNT OVER - 1)`, which I have to make NULL-safe by hand.

**Schema and sample data:** nine employees. Department 10 has a salary tie (70 and 70), department 30 has one person, department 40 has one real salary and one NULL.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,10,50),(2,10,70),(3,10,70),(4,10,100),
  (5,20,40),(6,20,60),(7,30,55),(8,40,80),(9,40,NULL);
```

**SQL answer:** **EXCLUDE version** (`SQL_EXCL` in the Code block). The frame is the whole partition, and `EXCLUDE CURRENT ROW` removes the row being computed.
```sql
SELECT emp_id, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                         EXCLUDE CURRENT ROW) AS others_avg
FROM employees
ORDER BY emp_id
```
**Portable version** (`SQL_PORTABLE`): the department total minus my own salary, divided by the department count minus me.
```sql
SELECT emp_id, dept_id, salary,
       (SUM(salary) OVER (PARTITION BY dept_id) - COALESCE(salary, 0))
         * 1.0 / NULLIF(COUNT(salary) OVER (PARTITION BY dept_id)
                        - (salary IS NOT NULL), 0) AS others_avg
FROM employees
ORDER BY emp_id
```

**pandas answer:** `transform("count")` and `transform("sum")` give the department figures on every row; then I subtract the row itself.
```py
g = emp.groupby("dept_id")["salary"]
n_others = g.transform("count") - emp["salary"].notna()
sum_others = g.transform("sum") - emp["salary"].fillna(0)
pd_avg = (sum_others / n_others.where(n_others > 0)).rename("others_avg")
```

**Example:**
- Department 10 salaries are 50, 70, 70, 100, total 290. Asha (50): (290 - 50) / 3 = 80. Ben (70): (290 - 70) / 3 = 73.33, and Chitra gets the same. Dev (100): 190 / 3 = 63.33.
- Department 20 is 40 and 60: each person's "others" is just the other one, so 60 and 40.
- Department 30 has one person: no others, so the answer is NULL, not 0 (the `NULLIF(..., 0)` and `.where(n_others > 0)` guard).
- Department 40: Ila is 80 and Jay is NULL. Ila's others are {NULL}, so the average is NULL. Jay's others are {80}, so Jay gets 80. The `AVG` ignores NULL, so the portable formula must ignore it too.
- Result column `others_avg`: 80, 73.33, 73.33, 63.33, 60, 40, NULL, NULL, 80. Subtract it from `salary` for "versus the others".

**Code:** run with `python3 -I`; the same code block also runs the EXCLUDE GROUP / TIES / NO OTHERS comparison.
```python
# Q36: leave-one-out average with EXCLUDE CURRENT ROW and the portable equivalent
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,10,50),(2,10,70),(3,10,70),(4,10,100),
  (5,20,40),(6,20,60),(7,30,55),(8,40,80),(9,40,NULL);
"""
SQL_EXCL = """
SELECT emp_id, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                         EXCLUDE CURRENT ROW) AS others_avg
FROM employees
ORDER BY emp_id
"""
SQL_PORTABLE = """
SELECT emp_id, dept_id, salary,
       (SUM(salary) OVER (PARTITION BY dept_id) - COALESCE(salary, 0))
         * 1.0 / NULLIF(COUNT(salary) OVER (PARTITION BY dept_id)
                        - (salary IS NOT NULL), 0) AS others_avg
FROM employees
ORDER BY emp_id
"""
SQL_NAIVE = """
SELECT emp_id,
       (SUM(salary) OVER (PARTITION BY dept_id) - salary) * 1.0
         / (COUNT(*) OVER (PARTITION BY dept_id) - 1) AS others_avg
FROM employees
ORDER BY emp_id
"""
SQL_GROUP_TIES = """
SELECT emp_id, salary,
       AVG(salary) OVER w_cur  AS excl_current_row,
       AVG(salary) OVER w_grp  AS excl_group,
       AVG(salary) OVER w_ties AS excl_ties,
       AVG(salary) OVER w_none AS excl_no_others
FROM employees
WHERE dept_id = 10
WINDOW w_cur  AS (PARTITION BY dept_id ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING EXCLUDE CURRENT ROW),
       w_grp  AS (PARTITION BY dept_id ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING EXCLUDE GROUP),
       w_ties AS (PARTITION BY dept_id ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING EXCLUDE TIES),
       w_none AS (PARTITION BY dept_id ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING EXCLUDE NO OTHERS)
ORDER BY salary, emp_id
"""
SQL_NOORDER_GROUP = """
SELECT emp_id, AVG(salary) OVER (PARTITION BY dept_id ROWS BETWEEN UNBOUNDED PRECEDING
       AND UNBOUNDED FOLLOWING EXCLUDE GROUP) AS a FROM employees WHERE dept_id = 10 ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
excl = pd.read_sql_query(SQL_EXCL, con)
port = pd.read_sql_query(SQL_PORTABLE, con)
naive = pd.read_sql_query(SQL_NAIVE, con)
print("EXCLUDE CURRENT ROW:"); print(excl.to_string(index=False))
print("\nportable (SUM - own) / (COUNT - 1), NULL-safe version:"); print(port.to_string(index=False))
print("\nnaive portable (SUM - salary) / (COUNT(*) - 1):"); print(naive.to_string(index=False))
print("\nEXCLUDE variants on dept 10 (ORDER BY salary, frame = whole partition):")
print(pd.read_sql_query(SQL_GROUP_TIES, con).to_string(index=False))
print("\nEXCLUDE GROUP with no ORDER BY (whole partition is one peer group):",
      [r[1] for r in con.execute(SQL_NOORDER_GROUP)])

emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
g = emp.groupby("dept_id")["salary"]
n_others = g.transform("count") - emp["salary"].notna()
sum_others = g.transform("sum") - emp["salary"].fillna(0)
pd_avg = (sum_others / n_others.where(n_others > 0)).rename("others_avg")
# pd:end
pd_df = emp.assign(others_avg=pd_avg)
# compared after sorting by emp_id; NaN equals NaN, floats within default tolerance
pd.testing.assert_frame_equal(excl, pd_df.sort_values("emp_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(excl, port, check_dtype=False)
print("\npandas others_avg:", pd_df["others_avg"].round(3).tolist())
print("asserts passed: EXCLUDE CURRENT ROW == portable NULL-safe formula == pandas")
```

**Output (my run):**
```text
EXCLUDE CURRENT ROW:
 emp_id  dept_id  salary  others_avg
      1       10    50.0   80.000000
      2       10    70.0   73.333333
      3       10    70.0   73.333333
      4       10   100.0   63.333333
      5       20    40.0   60.000000
      6       20    60.0   40.000000
      7       30    55.0         NaN
      8       40    80.0         NaN
      9       40     NaN   80.000000

portable (SUM - own) / (COUNT - 1), NULL-safe version:
 emp_id  dept_id  salary  others_avg
      1       10    50.0   80.000000
      2       10    70.0   73.333333
      3       10    70.0   73.333333
      4       10   100.0   63.333333
      5       20    40.0   60.000000
      6       20    60.0   40.000000
      7       30    55.0         NaN
      8       40    80.0         NaN
      9       40     NaN   80.000000

naive portable (SUM - salary) / (COUNT(*) - 1):
 emp_id  others_avg
      1   80.000000
      2   73.333333
      3   73.333333
      4   63.333333
      5   60.000000
      6   40.000000
      7         NaN
      8    0.000000
      9         NaN

EXCLUDE variants on dept 10 (ORDER BY salary, frame = whole partition):
 emp_id  salary  excl_current_row  excl_group  excl_ties  excl_no_others
      1      50         80.000000   80.000000  72.500000            72.5
      2      70         73.333333   75.000000  73.333333            72.5
      3      70         73.333333   75.000000  73.333333            72.5
      4     100         63.333333   63.333333  72.500000            72.5

EXCLUDE GROUP with no ORDER BY (whole partition is one peer group): [None, None, None, None]

pandas others_avg: [80.0, 73.333, 73.333, 63.333, 60.0, 40.0, nan, nan, 80.0]
asserts passed: EXCLUDE CURRENT ROW == portable NULL-safe formula == pandas
```

**Edge cases:**
- Naive portable formula `(SUM - salary) / (COUNT(*) - 1)` is wrong with NULLs. In my run it gave 0.0 for Ila (it counted Jay in `COUNT(*)` and divided 0 by 1) where EXCLUDE gives NULL, and NULL for Jay (`SUM - NULL` is NULL) where EXCLUDE gives 80. The NULL-safe version uses `COALESCE(salary, 0)`, `COUNT(salary)` and `(salary IS NOT NULL)`; it matched EXCLUDE on every row (asserted).
- One-person department: NULL both ways.
- Ties: `EXCLUDE CURRENT ROW` removes only my own row, so the other 70 still counts. That is why Ben and Chitra both get 73.33.
- `EXCLUDE GROUP` and `EXCLUDE TIES` depend on what counts as a peer, so they need an `ORDER BY` in the window. With no `ORDER BY` the whole partition is one peer group, and `EXCLUDE GROUP` removed everything: the average came back NULL for all four rows of department 10 in my run.
- Integer division: in SQLite `7 / 2` is 3 (I wrote `* 1.0` in the portable form so the average is not truncated).

**Then explain:**
- A frame says which rows the aggregate sees. `UNBOUNDED PRECEDING ... UNBOUNDED FOLLOWING` is the whole partition; `EXCLUDE` then removes some of those rows.
- The four options, run on department 10 with `ORDER BY salary` (Ben = 70, tied with Chitra). The numbers below are from the output of the Code block:
  | Option | What it removes | Ben (70, tied) | Asha (50, no tie) |
  |---|---|---|---|
  | `NO OTHERS` (default) | nothing | 72.5 | 72.5 |
  | `CURRENT ROW` | my row | 73.33 | 80 |
  | `GROUP` | my row and all my peers (same `ORDER BY` value) | 75 | 80 |
  | `TIES` | my peers but keep my row | 73.33 | 72.5 |
  For a row with no ties, `TIES` removes nothing, so it equals `NO OTHERS`; `GROUP` equals `CURRENT ROW`.
- Why `EXCLUDE CURRENT ROW` is useful: leave-one-out means and anomaly scores, where my own value should not pull the benchmark towards itself.
- Version support: SQLite supports GROUPS and EXCLUDE from 3.28.0 (per the SQLite page opened in Part 4); I ran them on 3.45.1. PostgreSQL has `EXCLUDE CURRENT ROW / GROUP / TIES / NO OTHERS` (the PostgreSQL syntax page I opened lists them; "since 11" is from memory, not executed here). MySQL 8.0 has window functions but, as far as I remember, no `EXCLUDE` or `GROUPS` (not executed). On an engine without it, use the portable form.

**Follow-ups:**
- *Compare each salary with the others' average?* Add `salary - others_avg` in an outer SELECT.
- *Leave-one-out median?* No portable shortcut; `EXCLUDE` helps with any aggregate that works over a frame, but a median function is not built in on SQLite.
- *Why not a self-join?* It works, but it re-reads the department for every row; the window reads each department once.

**Common mistakes:**
- Using `COUNT(*)` instead of `COUNT(salary)` and mishandling NULL salaries.
- Dividing by `COUNT - 1` with no guard for a one-person group (division by zero gives NULL in SQLite; other engines may raise an error, not executed).
- Keeping the default frame (which stops at the current row) and then expecting `EXCLUDE CURRENT ROW` to see later rows.
- Expecting `EXCLUDE TIES` to remove my own row; it keeps it.

### Q37 ⭐ 🟡 Exponentially weighted moving average at concept level: prices(trade_date, close_price). Explain the EWMA recursion ewma_t = alpha * x_t + (1 - alpha) * ewma_(t-1), build it with a recursive CTE in SQLite (not a window function), and compare with pandas ewm(alpha=0.3, adjust=False).mean(). Say why adjust=True (the pandas default) gives different values at the start, and state that most engines have no built-in EWMA window.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** EWMA is `ewma_t = alpha * x_t + (1 - alpha) * ewma_(t-1)` with `ewma_0 = x_0`; SQLite has no built-in EWMA window, so I build it with a recursive CTE walking the rows in order, and it matches pandas `ewm(alpha=0.3, adjust=False).mean()`; the pandas default `adjust=True` is a different, normalised formula, so its early values differ.

**Schema and sample data:** six trading days; the weekend gap is fine because the recursion goes by observation, not by calendar day. `trade_date` is a PRIMARY KEY, so there is exactly one price per date.
```sql
CREATE TABLE prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO prices VALUES ('2024-01-01',10),('2024-01-02',12),('2024-01-03',11),('2024-01-04',15),
  ('2024-01-05',14),('2024-01-08',16);
```

**SQL answer:** Number the rows with `ROW_NUMBER`, start the recursion at row 1 (its EWMA is its own price), and add row n + 1 from row n (`SQL_MAIN`).
```sql
WITH RECURSIVE ordered AS (
  SELECT trade_date, close_price,
         ROW_NUMBER() OVER (ORDER BY trade_date) AS n
  FROM prices
),
ewma(n, trade_date, close_price, ewma) AS (
  SELECT n, trade_date, close_price, close_price FROM ordered WHERE n = 1
  UNION ALL
  SELECT o.n, o.trade_date, o.close_price, 0.3 * o.close_price + 0.7 * e.ewma
  FROM ordered o JOIN ewma e ON o.n = e.n + 1
)
SELECT trade_date, close_price, ewma FROM ewma ORDER BY n
```

**pandas answer:** `adjust=False` is the recursion above; `adjust=True` (the default) is a weighted average.
```py
ew = prices["close_price"].ewm(alpha=0.3, adjust=False).mean()
```

**Example:** alpha = 0.3, so the old EWMA keeps weight 0.7.
- Day 1: 10 (the start).
- Day 2: 0.3 x 12 + 0.7 x 10 = 3.6 + 7 = 10.6.
- Day 3: 0.3 x 11 + 0.7 x 10.6 = 3.3 + 7.42 = 10.72.
- Day 4: 0.3 x 15 + 0.7 x 10.72 = 4.5 + 7.504 = 12.004.
- With `adjust=True`, day 2 is (12 + 0.7 x 10) / (1 + 0.7) = 19 / 1.7 = 11.1765, not 10.6. Same inputs, different formula.

**Code:** run with `python3 -I`.
```python
# Q37: EWMA with a recursive CTE versus pandas ewm
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO prices VALUES ('2024-01-01',10),('2024-01-02',12),('2024-01-03',11),('2024-01-04',15),
  ('2024-01-05',14),('2024-01-08',16);
"""
SQL_MAIN = """
WITH RECURSIVE ordered AS (
  SELECT trade_date, close_price,
         ROW_NUMBER() OVER (ORDER BY trade_date) AS n
  FROM prices
),
ewma(n, trade_date, close_price, ewma) AS (
  SELECT n, trade_date, close_price, close_price FROM ordered WHERE n = 1
  UNION ALL
  SELECT o.n, o.trade_date, o.close_price, 0.3 * o.close_price + 0.7 * e.ewma
  FROM ordered o JOIN ewma e ON o.n = e.n + 1
)
SELECT trade_date, close_price, ewma FROM ewma ORDER BY n
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL recursive CTE (alpha = 0.3):"); print(sql_df.to_string(index=False))

try:
    con.execute("INSERT INTO prices VALUES ('2024-01-03', 99)")
except sqlite3.IntegrityError as e:
    print("\nduplicate trade_date rejected by PRIMARY KEY:", e)

prices = pd.read_sql_query("SELECT * FROM prices ORDER BY trade_date", con)
# pd:main
ew = prices["close_price"].ewm(alpha=0.3, adjust=False).mean()
# pd:end
ew_adj = prices["close_price"].ewm(alpha=0.3).mean()
# adjust=True written out: sum(w_i x_i) / sum(w_i) with w_i = (1 - alpha) ** (t - i)
x = prices["close_price"].tolist()
manual = [sum(0.7 ** (t - i) * x[i] for i in range(t + 1)) / sum(0.7 ** (t - i) for i in range(t + 1))
          for t in range(len(x))]
# compared by row position after ORDER BY trade_date
pd.testing.assert_series_equal(sql_df["ewma"], ew.rename("ewma"), check_dtype=False)
assert all(abs(a - b) < 1e-12 for a, b in zip(manual, ew_adj))
print("\nadjust=False (matches SQL):", ew.round(4).tolist())
print("adjust=True  (default)     :", ew_adj.round(4).tolist())
print("adjust=True by hand        :", [round(v, 4) for v in manual])
print("gap adjust=False - adjust=True:", (ew - ew_adj).round(4).tolist())

# NULL price: the recursion poisons everything after it; pandas ewm skips it
con.execute("UPDATE prices SET close_price = NULL WHERE trade_date = '2024-01-03'")
null_sql = pd.read_sql_query(SQL_MAIN, con)
null_pd = pd.read_sql_query("SELECT * FROM prices ORDER BY trade_date", con)["close_price"].ewm(alpha=0.3, adjust=False).mean()
print("\nwith a NULL price on 01-03, SQL ewma:", null_sql["ewma"].round(4).tolist())
print("with a NaN price on 01-03, pandas   :", null_pd.round(4).tolist())
print("asserts passed: recursive CTE == ewm(alpha=0.3, adjust=False); adjust=True == weighted-average formula")
```

**Output (my run):**
```text
SQL recursive CTE (alpha = 0.3):
trade_date  close_price     ewma
2024-01-01         10.0 10.00000
2024-01-02         12.0 10.60000
2024-01-03         11.0 10.72000
2024-01-04         15.0 12.00400
2024-01-05         14.0 12.60280
2024-01-08         16.0 13.62196

duplicate trade_date rejected by PRIMARY KEY: UNIQUE constraint failed: prices.trade_date

adjust=False (matches SQL): [10.0, 10.6, 10.72, 12.004, 12.6028, 13.622]
adjust=True  (default)     : [10.0, 11.1765, 11.0959, 12.6372, 13.1286, 14.1049]
adjust=True by hand        : [10.0, 11.1765, 11.0959, 12.6372, 13.1286, 14.1049]
gap adjust=False - adjust=True: [0.0, -0.5765, -0.3759, -0.6332, -0.5258, -0.4829]

with a NULL price on 01-03, SQL ewma: [10.0, 10.6, nan, nan, nan, nan]
with a NaN price on 01-03, pandas   : [10.0, 10.6, 10.6, 12.2709, 12.7896, 13.7527]
asserts passed: recursive CTE == ewm(alpha=0.3, adjust=False); adjust=True == weighted-average formula
```

**Edge cases:**
- Duplicate dates: the table has a PRIMARY KEY, and the code tries to insert a second '2024-01-03' to show the `UNIQUE constraint failed` error. On a feed that can repeat a date, collapse it first (for example the last price per date) or give `ROW_NUMBER` a tie-breaker; otherwise the recursion's order is not defined.
- NULL price: the SQL recursion poisons the chain. In my run, with 01-03 set to NULL, the SQL EWMA was NULL from that day on. pandas skips the missing value but still counts the elapsed step (default `ignore_na=False`): it repeated 10.6 for the missing day and gave 12.2709 for the next, not 12.004. To make SQL behave like that, you would carry the previous EWMA with `COALESCE` in the recursive step, and decide what a missing day should mean.
- Irregular spacing: both versions weight by observation, not by elapsed time. (pandas has a `times=` option for time-based decay; I did not run it.)
- Empty table: the anchor row does not exist, so the CTE returns no rows.

**Then explain:**
- Meaning: each new value pulls the average towards it by `alpha`; older values fade by `0.7` per step. Bigger `alpha` reacts faster.
- Why a recursive CTE: a window function sees input rows, not its own previous output, so the recursion `ewma_t` depends on `ewma_(t-1)` cannot be a plain window frame. The CTE feeds each output row into the next.
- Why `adjust=True` differs at the start: it divides by the sum of the weights, `sum(0.7^k)`, which is below its long-run value early on, so the first few values are re-scaled; `adjust=False` starts from `x_0` and applies the recursion. The code asserts that my hand-written weighted average equals pandas `adjust=True`, and prints the gap per row (-0.58 on day 2, still -0.48 on day 6): it fades only slowly, as `0.7^t`.
- To the best of my knowledge most SQL engines have no built-in EWMA window (not executed on any other engine), so people use a recursive CTE, a UDF, or compute it in pandas or Spark.
- Cost: the CTE walks the rows one by one; fine for thousands, heavy for millions per series.

**Follow-ups:**
- *Choose alpha from a span?* In pandas `span=N` means `alpha = 2 / (N + 1)`; I did not run it here.
- *Do the same per ticker?* Add the ticker to the join (`o.ticker = e.ticker AND o.n = e.n + 1`) and number rows per ticker.
- *Why not `AVG ... OVER`?* A moving average gives equal weights in a fixed frame; EWMA weights decay and have no cut-off.

**Common mistakes:**
- Comparing SQL with pandas default `ewm(alpha=0.3).mean()` and concluding the SQL is wrong: the default is `adjust=True`.
- Forgetting a tie-break or unique key, so the order of the recursion is undefined.
- Letting one NULL price kill the rest of the series without noticing.
- Starting the recursion at 0 instead of `x_0`.

### Q38 ⭐ 🟡 Percent change pitfalls and index to 100: prices(trade_date, close_price) with a zero price, a NULL price and a negative value. Show LAG-based percent change with NULLIF, the pandas pct_change() result (inf for a zero base, NaN for missing, fill_method no longer fills in pandas 3: fill missing values yourself with ffill before pct_change), and rebasing a series to 100 using FIRST_VALUE or iloc[0]. Run both and assert matches.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Percent change is `(price - prev) / prev`; in SQL use `LAG` and `NULLIF(prev, 0)` so a zero base gives NULL, and in pandas `pct_change()` gives `inf` for a zero base and `NaN` for missing data without filling in pandas 3, so forward-fill first if that is what you want; index to 100 is `price / first price * 100`.

**Schema and sample data:** eight days with a zero price, a NULL price and then negative values. One price per date (PRIMARY KEY).
```sql
CREATE TABLE prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO prices VALUES ('2024-01-01',100),('2024-01-02',110),('2024-01-03',0),('2024-01-04',50),
  ('2024-01-05',NULL),('2024-01-06',60),('2024-01-07',-20),('2024-01-08',-10);
```

**SQL answer:** `SQL_MAIN` is the LAG percent change. `SQL_FFILL` first fills the NULL with the last known price (SQLite has no `IGNORE NULLS`, so a correlated subquery does it). `SQL_REBASE` indexes to 100.
```sql
SELECT trade_date, close_price,
       (close_price - LAG(close_price) OVER (ORDER BY trade_date))
         / NULLIF(LAG(close_price) OVER (ORDER BY trade_date), 0) AS pct_change
FROM prices
ORDER BY trade_date
```
```sql
WITH f AS (
  SELECT trade_date,
         (SELECT p2.close_price FROM prices p2
          WHERE p2.trade_date <= p.trade_date AND p2.close_price IS NOT NULL
          ORDER BY p2.trade_date DESC LIMIT 1) AS filled
  FROM prices p
)
SELECT trade_date, filled,
       (filled - LAG(filled) OVER (ORDER BY trade_date))
         / NULLIF(LAG(filled) OVER (ORDER BY trade_date), 0) AS pct_change
FROM f
ORDER BY trade_date
```
```sql
SELECT trade_date, close_price,
       100.0 * close_price / FIRST_VALUE(close_price) OVER (ORDER BY trade_date) AS idx
FROM prices
ORDER BY trade_date
```

**pandas answer:** ```py
pct = s.pct_change()
pct_ffill = s.ffill().pct_change()
index100 = s / s.iloc[0] * 100
```

**Example:**
Prices: 100, 110, 0, 50, NULL, 60, -20, -10.
- 110: (110 - 100) / 100 = 0.10. 0: (0 - 110) / 110 = -1.0.
- 50: base is 0. SQL `NULLIF` makes it NULL; pandas gives `inf`. Neither is a meaningful percentage.
- NULL day: NULL in both. 60: its base is the NULL day, so NULL in both (no fill).
- -20: (-20 - 60) / 60 = -1.3333. -10: (-10 - (-20)) / (-20) = -0.5: the price went up by 10 but the percent change is negative, because the base is negative. Percent change is not meaningful for series that cross zero; some people divide by `ABS(prev)`.
- After forward-filling, the NULL day becomes 50, so day 5 is 0.0 and day 6 is 60 / 50 - 1 = 0.2.
- Index to 100: 100 x price / 100, so 100, 110, 0, 50, NULL, 60, -20, -10 (the first price is 100, which makes it simple).

**Code:** run with `python3 -I`; extra checks at the end cover `fill_method`, `periods`, `freq` and a zero first price.
```python
# Q38: percent change pitfalls and rebasing to 100
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO prices VALUES ('2024-01-01',100),('2024-01-02',110),('2024-01-03',0),('2024-01-04',50),
  ('2024-01-05',NULL),('2024-01-06',60),('2024-01-07',-20),('2024-01-08',-10);
"""
SQL_MAIN = """
SELECT trade_date, close_price,
       (close_price - LAG(close_price) OVER (ORDER BY trade_date))
         / NULLIF(LAG(close_price) OVER (ORDER BY trade_date), 0) AS pct_change
FROM prices
ORDER BY trade_date
"""
# fill the NULL with the last known price first (SQLite has no IGNORE NULLS)
SQL_FFILL = """
WITH f AS (
  SELECT trade_date,
         (SELECT p2.close_price FROM prices p2
          WHERE p2.trade_date <= p.trade_date AND p2.close_price IS NOT NULL
          ORDER BY p2.trade_date DESC LIMIT 1) AS filled
  FROM prices p
)
SELECT trade_date, filled,
       (filled - LAG(filled) OVER (ORDER BY trade_date))
         / NULLIF(LAG(filled) OVER (ORDER BY trade_date), 0) AS pct_change
FROM f
ORDER BY trade_date
"""
SQL_LAG2 = """
SELECT trade_date,
       (close_price - LAG(close_price, 2) OVER (ORDER BY trade_date))
         / NULLIF(LAG(close_price, 2) OVER (ORDER BY trade_date), 0) AS pct_2
FROM prices
ORDER BY trade_date
"""
SQL_REBASE = """
SELECT trade_date, close_price,
       100.0 * close_price / FIRST_VALUE(close_price) OVER (ORDER BY trade_date) AS idx
FROM prices
ORDER BY trade_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
ff_df = pd.read_sql_query(SQL_FFILL, con)
lag2 = pd.read_sql_query(SQL_LAG2, con)
reb = pd.read_sql_query(SQL_REBASE, con)
print("SQL LAG percent change with NULLIF:"); print(sql_df.to_string(index=False))
print("\nSQL after forward-filling the NULL price:"); print(ff_df.to_string(index=False))

prices = pd.read_sql_query("SELECT * FROM prices ORDER BY trade_date", con)
s = prices["close_price"]
# pd:main
pct = s.pct_change()
pct_ffill = s.ffill().pct_change()
index100 = s / s.iloc[0] * 100
# pd:end
print("\npandas pct_change():", pct.round(4).tolist())
print("pandas ffill().pct_change():", pct_ffill.round(4).tolist())
# inf appears where the base is 0: SQL gives NULL there, so compare after inf -> NaN
pd.testing.assert_series_equal(sql_df["pct_change"], pct.replace([np.inf, -np.inf], np.nan).rename("pct_change"), check_dtype=False)
pd.testing.assert_series_equal(ff_df["pct_change"], pct_ffill.replace([np.inf, -np.inf], np.nan).rename("pct_change"), check_dtype=False)
pd.testing.assert_series_equal(reb["idx"], index100.rename("idx"), check_dtype=False)
pd.testing.assert_series_equal(lag2["pct_2"], s.pct_change(periods=2).replace([np.inf, -np.inf], np.nan).rename("pct_2"), check_dtype=False)
print("\nindex to 100, SQL FIRST_VALUE:", reb["idx"].round(2).tolist())

# pandas 3: fill_method behaviour
for fm in ("pad", None):
    try:
        out = s.pct_change(fill_method=fm).round(4).tolist()
        print(f"pct_change(fill_method={fm!r}) ran:", out)
    except Exception as e:
        print(f"pct_change(fill_method={fm!r}) raised {type(e).__name__}:", str(e)[:90])

# freq: shifts by calendar label, so a missing calendar day gives NaN, not the previous row
ts = s.copy(); ts.index = pd.to_datetime(prices["trade_date"])
gap = ts.drop(pd.Timestamp("2024-01-02"))
print("\nwith 01-02 missing, row-based pct_change:", gap.pct_change().round(4).tolist())
print("with 01-02 missing, pct_change(freq='D'):", gap.pct_change(freq="D").round(4).tolist())
print("shift(freq='D') moves the index, not the data:", ts.shift(1, freq="D").index[:2].strftime("%Y-%m-%d").tolist())

# rebasing when the first value is NULL or 0
print("\nrebase when first value is 0:  SQL",
      [r[0] for r in con.execute("SELECT 100.0*v/FIRST_VALUE(v) OVER (ORDER BY d) FROM (SELECT 1 d, 0.0 v UNION ALL SELECT 2, 5)")],
      " pandas", (pd.Series([0.0, 5.0]) / 0.0 * 100).tolist())
print("asserts passed: SQL LAG/NULLIF == pandas pct_change (inf -> NaN), ffill versions, periods=2, index to 100")
```

**Output (my run):**
```text
SQL LAG percent change with NULLIF:
trade_date  close_price  pct_change
2024-01-01        100.0         NaN
2024-01-02        110.0    0.100000
2024-01-03          0.0   -1.000000
2024-01-04         50.0         NaN
2024-01-05          NaN         NaN
2024-01-06         60.0         NaN
2024-01-07        -20.0   -1.333333
2024-01-08        -10.0   -0.500000

SQL after forward-filling the NULL price:
trade_date  filled  pct_change
2024-01-01   100.0         NaN
2024-01-02   110.0    0.100000
2024-01-03     0.0   -1.000000
2024-01-04    50.0         NaN
2024-01-05    50.0    0.000000
2024-01-06    60.0    0.200000
2024-01-07   -20.0   -1.333333
2024-01-08   -10.0   -0.500000

pandas pct_change(): [nan, 0.1, -1.0, inf, nan, nan, -1.3333, -0.5]
pandas ffill().pct_change(): [nan, 0.1, -1.0, inf, 0.0, 0.2, -1.3333, -0.5]

index to 100, SQL FIRST_VALUE: [100.0, 110.0, 0.0, 50.0, nan, 60.0, -20.0, -10.0]
pct_change(fill_method='pad') raised ValueError: fill_method must be None; got fill_method='pad'.
pct_change(fill_method=None) ran: [nan, 0.1, -1.0, inf, nan, nan, -1.3333, -0.5]

with 01-02 missing, row-based pct_change: [nan, -1.0, inf, nan, nan, -1.3333, -0.5]
with 01-02 missing, pct_change(freq='D'): [nan, nan, inf, nan, nan, -1.3333, -0.5]
shift(freq='D') moves the index, not the data: ['2024-01-02', '2024-01-03']

rebase when first value is 0:  SQL [None, None]  pandas [nan, inf]
asserts passed: SQL LAG/NULLIF == pandas pct_change (inf -> NaN), ffill versions, periods=2, index to 100
```

**Edge cases:**
- Zero base: SQL NULL (via `NULLIF`), pandas `inf`. I compare after replacing `inf` with NaN; decide in the report which you want shown.
- NULL price: no fill in pandas 3. In my run `pct_change(fill_method='pad')` raised `ValueError: fill_method must be None; got fill_method='pad'.` and `fill_method=None` gave the same result as the default. So fill yourself with `ffill()` before `pct_change()`.
- `periods=2` matches `LAG(close_price, 2)`; I asserted it.
- `freq='D'` works on a DatetimeIndex and shifts by label: with 01-02 removed, row-based `pct_change()` compared 01-03 with 01-01 (giving -1.0), while `pct_change(freq='D')` gave NaN because yesterday is not there. `shift(freq='D')` moves the index, not the data (checked).
- Negative prices: see the example; sign of the percent change flips meaning.
- Rebase with a first price of 0: SQL gave NULL for both rows (division by zero is NULL in SQLite); pandas gave `[nan, inf]`. With a NULL first price everything is NULL; pick a base date with a real price.
- Percent change is a fraction (0.10), not 10.

**Then explain:**
- `LAG` gives the previous row's price; the first row has none, so NULL.
- `NULLIF(x, 0)` turns a zero base into NULL, so the division returns NULL instead of an error on engines that raise one (not executed on other engines).
- pandas `pct_change()` is `s / s.shift(1) - 1`, so the zero base is `x / 0 = inf` and missing values stay NaN.
- Forward fill is a business decision: carrying the last price over is fine for a closing-price series with holidays, wrong for sparse measurements.
- `FIRST_VALUE(close_price) OVER (ORDER BY trade_date)` is the base for every row; in pandas it is `s.iloc[0]`. If the first row can be NULL, take the first non-NULL one instead.

**Follow-ups:**
- *Month-over-month with gaps?* LAG goes by row, not by calendar; join to a calendar or use `freq` in pandas (Part 6 covers month logic).
- *Log returns?* `LN(price / prev)`; they add up over time, unlike percent changes.
- *Show it as a percentage?* Multiply by 100 at the end, keep fractions in calculations.

**Common mistakes:**
- Dividing by the current price instead of the previous one.
- Forgetting `NULLIF` and getting errors or `inf` in a report.
- Calling `pct_change()` on a series with NaN and assuming it forward-fills (older pandas did; pandas 3 does not).
- Reading a negative percent change as a price fall when the base is negative.

### Q39 ⭐ 🟡 Time gaps between events with timestamps: events(event_id, user_id, event_ts). Compute the gap in minutes between consecutive events per user with LAG and (julianday(event_ts) - julianday(prev_ts)) * 1440, flag gaps over 30 minutes as 'new burst start' (only flag, do not number sessions; sessionization is Part 7), and handle identical timestamps with a deterministic tie-breaker. Give pandas diff().dt.total_seconds() / 60.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts, event_id)` gives the previous event; the gap in minutes is `(julianday(event_ts) - julianday(prev_ts)) * 1440`, rounded because of float error, and a gap over 30 is flagged 'new burst start'; pandas does `groupby(...).diff().dt.total_seconds() / 60`.

**Schema and sample data:** ten events for three users; user 1 has two events at exactly 09:10:00, a gap of exactly 30 minutes (09:10 to 09:40), and one gap that crosses a day boundary (user 3).
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
  (1,1,'2024-03-01 09:00:00'),(2,1,'2024-03-01 09:10:00'),(3,1,'2024-03-01 09:10:00'),
  (4,1,'2024-03-01 09:40:00'),(5,1,'2024-03-01 10:11:00'),(6,1,'2024-03-01 14:00:00'),
  (7,2,'2024-03-01 09:05:00'),(8,2,'2024-03-01 09:35:30'),
  (9,3,'2024-03-01 23:50:00'),(10,3,'2024-03-02 00:25:00');
```

**SQL answer:** Tie-break for identical timestamps: lower `event_id` first, in the window and in the final ORDER BY (`SQL_MAIN`). A gap of exactly 30 minutes is not over 30, so it is not flagged. The first event of a user has no previous event; I label it 'first event' and flag only gaps over 30 (numbering bursts is Part 7).
```sql
WITH g AS (
  SELECT event_id, user_id, event_ts,
         LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_ts
  FROM events
)
SELECT event_id, user_id, event_ts,
       ROUND((julianday(event_ts) - julianday(prev_ts)) * 1440, 3) AS gap_min,
       CASE WHEN prev_ts IS NULL THEN 'first event'
            WHEN ROUND((julianday(event_ts) - julianday(prev_ts)) * 1440, 3) > 30 THEN 'new burst start'
            ELSE '' END AS flag
FROM g
ORDER BY user_id, event_ts, event_id
```

**pandas answer:** ```py
ev["event_ts"] = pd.to_datetime(ev["event_ts"])
ev = ev.sort_values(["user_id", "event_ts", "event_id"]).reset_index(drop=True)
ev["gap_min"] = ev.groupby("user_id")["event_ts"].diff().dt.total_seconds() / 60
ev["flag"] = "new burst start"
ev.loc[ev["gap_min"] <= 30, "flag"] = ""
ev.loc[ev["gap_min"].isna(), "flag"] = "first event"
```

**Example:**
- User 1 in order (09:00, 09:10 id 2, 09:10 id 3, 09:40, 10:11, 14:00): gaps are NULL, 10, 0, 30, 31, 229 minutes.
- Events 2 and 3 have the same timestamp. The tie-breaker puts id 2 first, so id 3 gets gap 0 and id 2 keeps 10.
- 09:10 to 09:40 is exactly 30, so no flag. 09:40 to 10:11 is 31, so 'new burst start'. 10:11 to 14:00 is 229, so flagged.
- User 2: 09:05 to 09:35:30 is 30.5 minutes, flagged (it is over 30 by 30 seconds).
- User 3: 23:50 to 00:25 across midnight is 35 minutes, flagged.

**Code:** run with `python3 -I`.
```python
# Q39: time gaps between consecutive events per user, flagging gaps over 30 minutes
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
  (1,1,'2024-03-01 09:00:00'),(2,1,'2024-03-01 09:10:00'),(3,1,'2024-03-01 09:10:00'),
  (4,1,'2024-03-01 09:40:00'),(5,1,'2024-03-01 10:11:00'),(6,1,'2024-03-01 14:00:00'),
  (7,2,'2024-03-01 09:05:00'),(8,2,'2024-03-01 09:35:30'),
  (9,3,'2024-03-01 23:50:00'),(10,3,'2024-03-02 00:25:00');
"""
# tie-break for identical timestamps: lower event_id first
SQL_MAIN = """
WITH g AS (
  SELECT event_id, user_id, event_ts,
         LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_ts
  FROM events
)
SELECT event_id, user_id, event_ts,
       ROUND((julianday(event_ts) - julianday(prev_ts)) * 1440, 3) AS gap_min,
       CASE WHEN prev_ts IS NULL THEN 'first event'
            WHEN ROUND((julianday(event_ts) - julianday(prev_ts)) * 1440, 3) > 30 THEN 'new burst start'
            ELSE '' END AS flag
FROM g
ORDER BY user_id, event_ts, event_id
"""
SQL_RAW = """
WITH g AS (
  SELECT event_id, event_ts,
         LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_ts
  FROM events
)
SELECT event_id, (julianday(event_ts) - julianday(prev_ts)) * 1440 AS raw_min,
       (strftime('%s', event_ts) - strftime('%s', prev_ts)) / 60.0 AS sec_min
FROM g WHERE event_id IN (4, 5, 10)
ORDER BY event_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nraw float gap vs integer-seconds gap for events 4, 5, 10:")
for r in con.execute(SQL_RAW):
    print(r[0], repr(r[1]), r[2])

ev = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
ev["event_ts"] = pd.to_datetime(ev["event_ts"])
ev = ev.sort_values(["user_id", "event_ts", "event_id"]).reset_index(drop=True)
ev["gap_min"] = ev.groupby("user_id")["event_ts"].diff().dt.total_seconds() / 60
ev["flag"] = "new burst start"
ev.loc[ev["gap_min"] <= 30, "flag"] = ""
ev.loc[ev["gap_min"].isna(), "flag"] = "first event"
# pd:end
out = ev.assign(event_ts=ev["event_ts"].dt.strftime("%Y-%m-%d %H:%M:%S"), gap_min=ev["gap_min"].round(3))
# compared in the order user_id, event_ts, event_id
pd.testing.assert_frame_equal(sql_df, out[sql_df.columns], check_dtype=False)

print("\nrows with identical timestamps get gap 0:", sql_df.loc[sql_df["gap_min"] == 0, "event_id"].tolist())

# groupby().nth(1): the second event per user (rows, original index kept) in pandas 3
second = ev.groupby("user_id").nth(1)
print("nth(1) columns:", list(second.columns)[:3], "| event_ids:", second["event_id"].tolist())
print("asserts passed: SQL LAG/julianday == pandas groupby diff, flags equal")
```

**Output (my run):**
```text
 event_id  user_id            event_ts  gap_min            flag
        1        1 2024-03-01 09:00:00      NaN     first event
        2        1 2024-03-01 09:10:00     10.0                
        3        1 2024-03-01 09:10:00      0.0                
        4        1 2024-03-01 09:40:00     30.0                
        5        1 2024-03-01 10:11:00     31.0 new burst start
        6        1 2024-03-01 14:00:00    229.0 new burst start
        7        2 2024-03-01 09:05:00      NaN     first event
        8        2 2024-03-01 09:35:30     30.5 new burst start
        9        3 2024-03-01 23:50:00      NaN     first event
       10        3 2024-03-02 00:25:00     35.0 new burst start

raw float gap vs integer-seconds gap for events 4, 5, 10:
4 30.000000223517418 30.0
5 30.99999949336052 31.0
10 34.999999925494194 35.0

rows with identical timestamps get gap 0: [3]
nth(1) columns: ['event_id', 'user_id', 'event_ts'] | event_ids: [2, 8, 10]
asserts passed: SQL LAG/julianday == pandas groupby diff, flags equal
```

**Edge cases:**
- Float surprise: `(julianday(a) - julianday(b)) * 1440` is a float. For the exact-30-minute gap my run printed 30.000000223517418, and for the 31-minute gap 30.99999949336052. Without rounding, `gap > 30` would wrongly flag the exact 30-minute gap. I used `ROUND(..., 3)`; an integer alternative is `(strftime('%s', ts) - strftime('%s', prev)) / 60.0`, which printed 30.0, 31.0 and 35.0.
- Identical timestamps: gap 0, and the order inside the tie follows `event_id`. Without a second sort key the order among the tied rows is not defined, so the labels could swap between runs or engines; I did not try to provoke it.
- First event per user: NULL gap (pandas NaT / NaN).
- Time zones and daylight saving: the text timestamps carry no zone, so I assumed one zone. With mixed zones convert to UTC first.
- Day boundary: handled, because julianday works on full timestamps.

**Then explain:**
- `LAG` with `PARTITION BY user_id` stops the gap from crossing users; the `ORDER BY` with the tie-breaker makes the answer repeatable.
- Flag, not session numbers: the flag only marks the start of a new burst. Turning flags into burst numbers is a running sum of the flag; that and the cases around it are Part 7.
- pandas: `diff()` on a datetime column gives a timedelta; `.dt.total_seconds() / 60` gives minutes. Sort by `user_id, event_ts, event_id` first, or `diff()` follows the file order.
- Another dialect would use other functions (PostgreSQL timestamp subtraction with `EXTRACT(EPOCH ...)`, MySQL `TIMESTAMPDIFF`, SQL Server `DATEDIFF`); I did not run them. Some of those count unit boundaries crossed rather than elapsed time (from memory, not executed), so check the doc before using them for gaps.
- Extra pandas check: `groupby("user_id").nth(1)` in pandas 3.0.5 returned the second event of each user as ordinary rows with their original columns (event ids 2, 8, 10), not a frame indexed by user.

**Follow-ups:**
- *Number the bursts?* Cumulative sum of the new-burst flag per user: Part 7.
- *Different threshold per user?* Join a thresholds table before the comparison.
- *Time since the previous event of any user?* Drop the PARTITION BY.

**Common mistakes:**
- Comparing the raw float to 30 (flagging an exact 30-minute gap).
- Forgetting `PARTITION BY user_id` and measuring gaps between different users.
- No tie-breaker, so identical timestamps give different results on different runs.
- Calling a missing previous event a 'new burst' by accident, or not saying how the first event is treated.

### Q40 ⭐ 🟡 Cumulative product and compounding: returns(trade_date, daily_return) as decimals such as 0.01. Compute the growth of 1 unit with a running product. SQLite has no product aggregate, so show EXP(SUM(LN(1 + r)) OVER (...)) (run it; note SQLite math functions may be build dependent, hedged) and the pandas (1 + r).cumprod(). Explain the floating-point error and that a window PRODUCT aggregate is not in the SQL standard.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** A running product is `EXP(SUM(LN(1 + r)) OVER (ORDER BY trade_date ROWS UNBOUNDED PRECEDING))` in SQLite (a product is a sum of logs), or a recursive CTE for an exact multiply; pandas does it with `(1 + r).cumprod()`; floating point makes the two agree only to about 1e-15, and the SQL standard has no product aggregate.

**Schema and sample data:** six daily returns as decimals (0.01 is 1 percent); one row per date (PRIMARY KEY).
```sql
CREATE TABLE returns(trade_date TEXT PRIMARY KEY, daily_return REAL);
INSERT INTO returns VALUES ('2024-01-01',0.01),('2024-01-02',-0.02),('2024-01-03',0.03),
  ('2024-01-04',0.00),('2024-01-05',-0.01),('2024-01-08',0.02);
```

**SQL answer:** `SQL_MAIN` uses logs. `SQL_REC` multiplies in a recursive CTE (no logs); it needs the rows numbered, so it relies on the order by date.
```sql
SELECT trade_date, daily_return,
       EXP(SUM(LN(1 + daily_return)) OVER (ORDER BY trade_date
                                           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) AS growth
FROM returns
ORDER BY trade_date
```
```sql
WITH RECURSIVE o AS (
  SELECT trade_date, daily_return, ROW_NUMBER() OVER (ORDER BY trade_date) AS n FROM returns
),
g(n, trade_date, growth) AS (
  SELECT n, trade_date, 1 + daily_return FROM o WHERE n = 1
  UNION ALL
  SELECT o.n, o.trade_date, g.growth * (1 + o.daily_return) FROM o JOIN g ON o.n = g.n + 1
)
SELECT trade_date, growth FROM g ORDER BY n
```

**pandas answer:** ```py
growth = (1 + r["daily_return"]).cumprod()
```

**Example:**
Growth of 1 unit:
- Day 1: 1 x 1.01 = 1.01. Day 2: 1.01 x 0.98 = 0.9898. Day 3: 0.9898 x 1.03 = 1.019494.
- Day 4: return 0, so still 1.019494. Day 5: x 0.99 = 1.009299. Day 6: x 1.02 = 1.029485 (1.0294850412).
- With logs: sum of `LN(1 + r)` up to day 3 is `LN(1.01) + LN(0.98) + LN(1.03)`; `EXP` of that is 1.019494. Same number, different route.

**Code:** run with `python3 -I`; it also prints the build's math option, a 2000-row error test and the edge cases.
```python
# Q40: cumulative product (growth of 1 unit)
import math
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE returns(trade_date TEXT PRIMARY KEY, daily_return REAL);
INSERT INTO returns VALUES ('2024-01-01',0.01),('2024-01-02',-0.02),('2024-01-03',0.03),
  ('2024-01-04',0.00),('2024-01-05',-0.01),('2024-01-08',0.02);
"""
SQL_MAIN = """
SELECT trade_date, daily_return,
       EXP(SUM(LN(1 + daily_return)) OVER (ORDER BY trade_date
                                           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)) AS growth
FROM returns
ORDER BY trade_date
"""
SQL_REC = """
WITH RECURSIVE o AS (
  SELECT trade_date, daily_return, ROW_NUMBER() OVER (ORDER BY trade_date) AS n FROM returns
),
g(n, trade_date, growth) AS (
  SELECT n, trade_date, 1 + daily_return FROM o WHERE n = 1
  UNION ALL
  SELECT o.n, o.trade_date, g.growth * (1 + o.daily_return) FROM o JOIN g ON o.n = g.n + 1
)
SELECT trade_date, growth FROM g ORDER BY n
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("SQLite math functions compiled in:",
      [r[0] for r in con.execute("PRAGMA compile_options") if "MATH" in r[0]] or "no MATH option listed")
sql_df = pd.read_sql_query(SQL_MAIN, con)
rec_df = pd.read_sql_query(SQL_REC, con)
print(sql_df.to_string(index=False))

r = pd.read_sql_query("SELECT * FROM returns ORDER BY trade_date", con)
# pd:main
growth = (1 + r["daily_return"]).cumprod()
# pd:end
pd.testing.assert_series_equal(sql_df["growth"], growth.rename("growth"), check_dtype=False)
pd.testing.assert_series_equal(rec_df["growth"], growth.rename("growth"), check_dtype=False)
exact = []
p = 1.0
for v in r["daily_return"]:
    p *= 1 + v
    exact.append(p)
print("\nlast value  exp(sum(ln))  :", repr(float(sql_df["growth"].iloc[-1])))
print("last value  cumprod       :", repr(float(growth.iloc[-1])))
print("last value  recursive CTE :", repr(float(rec_df["growth"].iloc[-1])))
print("last value  python loop   :", repr(exact[-1]))
print("last value  math.fsum of logs, exp:", repr(math.exp(math.fsum(math.log(1 + v) for v in r["daily_return"]))))
print("max abs gap exp/ln vs cumprod:", max(abs(a - b) for a, b in zip(sql_df["growth"], growth)))
print("exactly equal rows (==):", int((sql_df["growth"] == growth).sum()), "of", len(r))

# longer series: 2000 deterministic returns, to see the float error
con.execute("CREATE TABLE long_r(d INTEGER PRIMARY KEY, daily_return REAL)")
con.executemany("INSERT INTO long_r VALUES (?, ?)", [(i, 0.0007 * ((i * 7) % 11 - 5)) for i in range(1, 2001)])
lg = pd.read_sql_query("""SELECT d, EXP(SUM(LN(1+daily_return)) OVER (ORDER BY d)) AS growth FROM long_r ORDER BY d""", con)
lr = pd.read_sql_query("SELECT * FROM long_r ORDER BY d", con)
lcp = (1 + lr["daily_return"]).cumprod()
rel = ((lg["growth"] - lcp).abs() / lcp)
print("\n2000 rows: max relative gap exp/ln vs cumprod:", float(rel.max()), "| rows not bit-equal:", int((lg["growth"] != lcp).sum()))
print("last value exp/ln:", repr(float(lg["growth"].iloc[-1])), " cumprod:", repr(float(lcp.iloc[-1])))
assert rel.max() < 1e-12

# edge cases: -100 percent, below -100 percent, NULL return
con.executescript("""
CREATE TABLE r2(d INTEGER PRIMARY KEY, daily_return REAL);
INSERT INTO r2 VALUES (1,0.10),(2,NULL),(3,0.10),(4,-1.0),(5,0.50),(6,-1.5);
""")
print("\nedge cases, SQL exp(sum(ln(1+r))):")
for row in con.execute("""SELECT d, daily_return, LN(1+daily_return) AS ln1p,
  EXP(SUM(LN(1+daily_return)) OVER (ORDER BY d)) AS growth FROM r2 ORDER BY d"""):
    print(row)
e = pd.Series([0.10, None, 0.10, -1.0, 0.50, -1.5])
print("pandas (1+r).cumprod():", (1 + e).cumprod().tolist())
print("asserts passed: SQL exp/ln == pandas cumprod == recursive CTE product (within float tolerance)")
```

**Output (my run):**
```text
SQLite math functions compiled in: ['ENABLE_MATH_FUNCTIONS']
trade_date  daily_return   growth
2024-01-01          0.01 1.010000
2024-01-02         -0.02 0.989800
2024-01-03          0.03 1.019494
2024-01-04          0.00 1.019494
2024-01-05         -0.01 1.009299
2024-01-08          0.02 1.029485

last value  exp(sum(ln))  : 1.0294850412
last value  cumprod       : 1.0294850412
last value  recursive CTE : 1.0294850412
last value  python loop   : 1.0294850412
last value  math.fsum of logs, exp: 1.0294850412
max abs gap exp/ln vs cumprod: 0.0
exactly equal rows (==): 6 of 6

2000 rows: max relative gap exp/ln vs cumprod: 4.6600118847503715e-15 | rows not bit-equal: 1922
last value exp/ln: 0.9993017069733997  cumprod: 0.9993017069733952

edge cases, SQL exp(sum(ln(1+r))):
(1, 0.1, 0.09531017980432493, 1.1)
(2, None, None, 1.1)
(3, 0.1, 0.09531017980432493, 1.2100000000000002)
(4, -1.0, None, 1.2100000000000002)
(5, 0.5, 0.4054651081081644, 1.8150000000000002)
(6, -1.5, None, 1.8150000000000002)
pandas (1+r).cumprod(): [1.1, nan, 1.2100000000000002, 0.0, 0.0, -0.0]
asserts passed: SQL exp/ln == pandas cumprod == recursive CTE product (within float tolerance)
```

**Edge cases:**
- Build dependence: `LN` and `EXP` worked in this Python's SQLite (`PRAGMA compile_options` lists `ENABLE_MATH_FUNCTIONS`). SQLite's math functions are optional at compile time, so on another build they may be missing (I could not test other builds). Other engines have `LN`/`LOG` of their own; not executed.
- Float error on 6 rows: no visible difference, all 6 rows were bit-identical between `EXP(SUM(LN))` and `cumprod` in my run. On 2000 deterministic returns the largest relative gap was 4.66e-15 and 1922 of the 2000 rows were not bit-equal. Harmless for reporting, but do not compare with `=`; compare with a tolerance.
- A return of -100 percent: `LN(0)` is NULL in SQLite (`LN` of 0 or a negative number gives NULL), `SUM` skips NULL, so the growth stayed at its previous value (1.21) instead of dropping to 0. A return below -100 percent (here -1.5) is also NULL. pandas gave 0.0 and then -0.0. If such returns are possible, use the recursive CTE or guard with `CASE`.
- NULL return: SQL carries the previous growth for that row (1.1); pandas gives NaN on that row but continues the product afterwards (1.21 on the next row). Decide whether a missing day means 0 percent.
- Duplicate dates: the PRIMARY KEY prevents them. If duplicates were allowed, add a unique tie-breaker to the `ORDER BY` and keep `ROWS` (a `RANGE` frame would give both rows of a date the same total).

**Then explain:**
- A product of `(1 + r)` terms is `EXP` of a sum of `LN(1 + r)` terms. That turns a product into a sum, which windows can do.
- The SQL standard has no product aggregate, as far as I know; `SUM`, `AVG`, `MIN`, `MAX`, `COUNT` are what the standard gives you, so a window PRODUCT is not portable (not checked against every engine). The log trick or a recursive CTE are the workarounds.
- Recursive CTE: each row multiplies the previous result by `1 + r`. It is exact in the sense of plain float multiplication, and it matched `cumprod` in the run. It is also one row at a time.
- Floating point: `EXP(SUM(LN(...)))` does several roundings (logs, sums, an exp). Plain multiplication rounds once per step. Neither is 'exact'; differences are around 1e-15 relative.
- Compounding vs adding: sum of returns is not growth. Cumulative return is `growth - 1`.

**Follow-ups:**
- *Annualise?* `growth ^ (252 / n) - 1`, with 252 trading days an assumption; I did not run it.
- *Per ticker?* Add `PARTITION BY ticker`.
- *Drawdown?* Needs a running maximum of the growth series; a follow-up on the same window machinery.

**Common mistakes:**
- Summing returns and calling it growth.
- Using `LN(r)` instead of `LN(1 + r)`.
- Not guarding against `r <= -1`.
- Comparing floats with `=` in a test.

### Q41 ⭐ 🟡 Window performance concept: a running total over 10 million rows partitioned by customer. Explain that the engine sorts per partition (or reads an index in the right order), that ROWS frames with UNBOUNDED PRECEDING are incremental, that sliding frames and RANGE with offsets cost more, that several windows with different PARTITION BY or ORDER BY mean several sorts, and why a self-join running total is quadratic. Show EXPLAIN QUERY PLAN on SQLite for a windowed query with and without a matching index (run), and defer tuning to Part 11.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** A running total over 10 million rows costs one sort per distinct partition-and-order (or none if an index already delivers that order), then one pass; a `ROWS UNBOUNDED PRECEDING` frame is incremental, whereas a self-join re-reads every earlier row per row and is quadratic; I show the SQLite plan with and without a matching index, and leave tuning to Part 11.

**Schema and sample data:** 600 orders over 6 customers for the plans (the generator in the Code block also builds bigger tables for timing). Dates repeat inside a customer, so the order is `order_date, order_id`.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
```

**SQL answer:** `SQL_MAIN` is the running total with a unique ordering. `SQL_TWO` adds a second window with a different PARTITION BY and ORDER BY. `SQL_SELF` is the quadratic self-join form.
```sql
SELECT order_id, customer_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date, order_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
ORDER BY customer_id, order_date, order_id
```
```sql
SELECT order_id,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS a,
       SUM(amount) OVER (PARTITION BY order_date ORDER BY order_id) AS b
FROM orders
```
```sql
SELECT o.order_id, (SELECT SUM(i.amount) FROM orders i
                    WHERE i.customer_id = o.customer_id
                      AND (i.order_date < o.order_date OR (i.order_date = o.order_date AND i.order_id <= o.order_id))) AS running_total
FROM orders o ORDER BY o.order_id
```

**pandas answer:** ```py
orders = orders.sort_values(["customer_id", "order_date", "order_id"])
orders["running_total"] = orders.groupby("customer_id")["amount"].cumsum()
```

**Example:**
What the engine does, in words, for 10 million rows and about 1 million customers:
- Sort by (customer_id, order_date, order_id). If an index already stores rows in that order, skip the sort and read the index.
- Walk each partition once, adding each amount to a running value: 10 million additions, not 10 million times the partition size.
- A self-join instead matches every order with every earlier order of the same customer; a customer with 1000 orders makes about 500,000 pairs.
In my SQLite runs the plans were:
- no index, one window: `SCAN orders`, `USE TEMP B-TREE FOR ORDER BY`, then `SCAN` of the window subquery;
- with index on `(customer_id, order_date, order_id, amount)`: `SCAN orders USING COVERING INDEX ix_cust_date`, no temp B-tree;
- two windows with different partitions: two `USE TEMP B-TREE FOR ORDER BY`, one per window, even with that index (it matches only the first window).

**Code:** run with `python3 -I`; the timings are from my machine and change from run to run, so only the shape (not the digits) matters.
```python
# Q41: window performance: EXPLAIN QUERY PLAN with and without an index, and window vs self-join timing
import sqlite3
import time
import pandas as pd

def make(con, n, customers):
    con.executescript("DROP TABLE IF EXISTS orders; CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);")
    rows = [(i, (i * 37) % customers, "2024-%02d-%02d" % (1 + (i * 13) % 12, 1 + (i * 17) % 28), 1 + (i * 7) % 50) for i in range(1, n + 1)]
    con.executemany("INSERT INTO orders VALUES (?,?,?,?)", rows)

# tie-break: order_id, so duplicate dates in one customer still give one fixed order
SQL_MAIN = """
SELECT order_id, customer_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date, order_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
ORDER BY customer_id, order_date, order_id
"""
SQL_TWO = """
SELECT order_id,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS a,
       SUM(amount) OVER (PARTITION BY order_date ORDER BY order_id) AS b
FROM orders
"""
SQL_SELF = """
SELECT o.order_id, (SELECT SUM(i.amount) FROM orders i
                    WHERE i.customer_id = o.customer_id
                      AND (i.order_date < o.order_date OR (i.order_date = o.order_date AND i.order_id <= o.order_id))) AS running_total
FROM orders o ORDER BY o.order_id
"""
def plan(con, sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

con = sqlite3.connect(":memory:")
make(con, 600, 6)
print("PLAN without index, one window:")
for p in plan(con, SQL_MAIN): print("  ", p)
print("PLAN without index, two windows with different PARTITION BY / ORDER BY:")
for p in plan(con, SQL_TWO): print("  ", p)
con.execute("CREATE INDEX ix_cust_date ON orders(customer_id, order_date, order_id, amount)")
print("PLAN with index (customer_id, order_date, order_id, amount), one window:")
for p in plan(con, SQL_MAIN): print("  ", p)
print("PLAN with that index, two windows:")
for p in plan(con, SQL_TWO): print("  ", p)

sql_df = pd.read_sql_query(SQL_MAIN, con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
orders = orders.sort_values(["customer_id", "order_date", "order_id"])
orders["running_total"] = orders.groupby("customer_id")["amount"].cumsum()
# pd:end
pd_df = orders.sort_values(["customer_id", "order_date", "order_id"]).reset_index(drop=True)
# compared in the order customer_id, order_date, order_id
pd.testing.assert_frame_equal(sql_df, pd_df[sql_df.columns], check_dtype=False)
self_df = pd.read_sql_query(SQL_SELF, con).set_index("order_id")["running_total"]
assert self_df.sort_index().tolist() == orders.set_index("order_id")["running_total"].sort_index().tolist()
print("\nwindow == pandas cumsum == self-join subquery, 600 rows")

print("\ntimings (seconds, this machine; two customers so partitions are large):")
for n in (1000, 2000, 4000):
    c = sqlite3.connect(":memory:")
    make(c, n, 2)
    t0 = time.perf_counter(); c.execute(SQL_MAIN).fetchall(); tw = time.perf_counter() - t0
    c.execute("CREATE INDEX ix ON orders(customer_id, order_date, order_id, amount)")
    t0 = time.perf_counter(); c.execute(SQL_SELF).fetchall(); ts = time.perf_counter() - t0
    print(f"  n={n:5d}  window={tw:.4f}  self-join (with index)={ts:.4f}")

# frame shape: one big partition, 20000 rows; same query, different frame / aggregate
c = sqlite3.connect(":memory:")
make(c, 20000, 1)
frames = {
 "SUM  ROWS UNBOUNDED PRECEDING     ": "SELECT SUM(amount) OVER (ORDER BY order_date, order_id ROWS UNBOUNDED PRECEDING) FROM orders",
 "SUM  ROWS 2000 PRECEDING          ": "SELECT SUM(amount) OVER (ORDER BY order_date, order_id ROWS BETWEEN 2000 PRECEDING AND CURRENT ROW) FROM orders",
 "MAX  ROWS 2000 PRECEDING          ": "SELECT MAX(amount) OVER (ORDER BY order_date, order_id ROWS BETWEEN 2000 PRECEDING AND CURRENT ROW) FROM orders",
 "SUM  RANGE 30 PRECEDING (julianday)": "SELECT SUM(amount) OVER (ORDER BY julianday(order_date) RANGE BETWEEN 30 PRECEDING AND CURRENT ROW) FROM orders",
}
print("\nframe shape on one 20000-row partition (seconds, this machine):")
for name, q in frames.items():
    best = min((lambda t0: (c.execute(q).fetchall(), time.perf_counter() - t0)[1])(time.perf_counter()) for _ in range(3))
    print(f"  {name} {best:.4f}")
print("asserts passed: window == pandas groupby cumsum == self-join")
```

**Output (my run):**
```text
PLAN without index, one window:
   CO-ROUTINE (subquery-2)
   SCAN orders
   USE TEMP B-TREE FOR ORDER BY
   SCAN (subquery-2)
PLAN without index, two windows with different PARTITION BY / ORDER BY:
   CO-ROUTINE (subquery-2)
   CO-ROUTINE (subquery-3)
   SCAN orders
   USE TEMP B-TREE FOR ORDER BY
   SCAN (subquery-3)
   USE TEMP B-TREE FOR ORDER BY
   SCAN (subquery-2)
PLAN with index (customer_id, order_date, order_id, amount), one window:
   CO-ROUTINE (subquery-2)
   SCAN orders USING COVERING INDEX ix_cust_date
   SCAN (subquery-2)
PLAN with that index, two windows:
   CO-ROUTINE (subquery-2)
   CO-ROUTINE (subquery-3)
   SCAN orders
   USE TEMP B-TREE FOR ORDER BY
   SCAN (subquery-3)
   USE TEMP B-TREE FOR ORDER BY
   SCAN (subquery-2)

window == pandas cumsum == self-join subquery, 600 rows

timings (seconds, this machine; two customers so partitions are large):
  n= 1000  window=0.0021  self-join (with index)=0.0385
  n= 2000  window=0.0039  self-join (with index)=0.1541
  n= 4000  window=0.0076  self-join (with index)=0.5820

frame shape on one 20000-row partition (seconds, this machine):
  SUM  ROWS UNBOUNDED PRECEDING      0.0152
  SUM  ROWS 2000 PRECEDING           0.0206
  MAX  ROWS 2000 PRECEDING           0.0283
  SUM  RANGE 30 PRECEDING (julianday) 0.0145
asserts passed: window == pandas groupby cumsum == self-join
```

**Edge cases:**
- Duplicate dates inside a partition: `ORDER BY order_date, order_id` plus a `ROWS` frame gives one fixed order. With only `ORDER BY order_date` and the default frame, tied dates would share one total (Q46).
- Window plus outer `ORDER BY`: with the index, the outer `ORDER BY customer_id, order_date, order_id` is covered by the same order, so no extra sort showed up.
- Small data hides everything: at 600 rows any plan is instant. The timings use larger tables.
- NULL in the sort key: NULLs sort first in SQLite ascending; other engines differ (not executed).
- The plan text is SQLite's own wording; PostgreSQL shows Sort and WindowAgg nodes and MySQL shows other labels (from memory, not executed).

**Then explain:**
- Sorting: a window needs its rows in partition and order sequence. The engine either sorts or reads an index that already has that order. Cost is roughly n log n, and spills to disk when it exceeds memory (general engine behaviour, not measured here).
- Incremental frames: `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` only adds the new row to the state. A sliding frame such as `ROWS 2000 PRECEDING` has to drop rows from the other end as well, which engines do cheaply for `SUM` and `COUNT` (subtract) but not for `MIN`/`MAX` (from memory about how engines work).
- My measurements on one 20000-row partition (seconds): `SUM` unbounded 0.0152, `SUM ROWS 2000 PRECEDING` 0.0206, `MAX ROWS 2000 PRECEDING` 0.0283, `SUM RANGE 30 PRECEDING` over `julianday` 0.0145. So sliding `MAX` was the slowest, the unbounded and `RANGE` ones were similar, and the differences are small. I cannot back 'RANGE with offsets is expensive' from this run; on engines that scan peers for every row it can be (not measured).
- Several windows: each different PARTITION BY / ORDER BY combination needs its own ordering, so more sorts. Windows with the same specification can share one sort; windows with the same partition but a different order cannot. Reuse a named `WINDOW`.
- Self-join: per partition of size m it does about m^2 / 2 row visits. In my timings with 2 customers and an index, 1000, 2000, 4000 rows took 0.0385, 0.1541, 0.5820 seconds (about 4x per doubling), while the window took 0.0021, 0.0039, 0.0076.
- Scope: tuning (index design, partitioning, statistics, parallelism) is Part 11.

**Follow-ups:**
- *Make it faster?* A covering index on (customer_id, order_date, order_id, amount); or pre-aggregate by day first. Details in Part 11.
- *Only the latest running total per customer?* The sum per customer; you do not need the window.
- *Same on a distributed engine?* Partitioning by customer lets it sort partitions in parallel; not executed here.

**Common mistakes:**
- Timing on 600 rows and drawing conclusions.
- Reading `EXPLAIN` output as a measurement of time; it is a plan.
- Writing a self-join running total 'because it is portable' on big tables.
- Putting windows with different orders in one query and not expecting several sorts.

### Q42 ⭐ 🟡 Dialect map for running totals and LAG/LEAD (hedge everything not run on SQLite 3.45): RANGE with INTERVAL offsets (PostgreSQL), DATEDIFF versus julianday, LAG default argument, GROUPS and EXCLUDE support, IGNORE NULLS, MySQL 8.0 window support (none in 5.7), the default frame in engines that differ from the standard (hedged, check the docs for each), and DATE_TRUNC availability. Present a table with a 'verified by running on SQLite' column and a 'hedged, not executed' column.
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** On SQLite 3.45 I could run most of the window features (LAG default, GROUPS, EXCLUDE, RANGE offsets on numbers, the default frame) and see which fail (INTERVAL offsets, IGNORE NULLS, DISTINCT in a window, DATE_TRUNC, DATEDIFF, QUALIFY); everything about other engines is from memory and not executed.

**Schema and sample data:** five rows with a duplicate date and a NULL, used by every probe.
```sql
CREATE TABLE t(id INTEGER PRIMARY KEY, d TEXT, v INTEGER);
INSERT INTO t VALUES (1,'2024-01-01',10),(2,'2024-01-02',20),(3,'2024-01-02',30),
  (4,'2024-01-05',40),(5,'2024-01-06',NULL);
```

**SQL answer:** Each probe is one small query in the Code block (see `probe(...)` calls). The window ones I report are the default frame, the `ROWS` fix, `GROUPS`, `EXCLUDE`, `RANGE` on a number, and `LAG(v, 1, -1)`; there is no single main query.

**pandas answer:** ```py
lag_pd = df["v"].shift(1, fill_value=-1)
default_pd = df["v"].fillna(0).cumsum().groupby(df["d"]).transform("max")
day = pd.to_datetime(df["d"]).map(pd.Timestamp.toordinal)
range_pd = [df.loc[(day >= x - 1) & (day <= x), "v"].sum(min_count=1) for x in day]
```

**Example:**
Reading the SQLite output for `t` (ids 1-5):
- Default frame with `ORDER BY d`: 10, 60, 60, 100, 100. Rows 2 and 3 share a date, so both see 10 + 20 + 30 = 60.
- `ROWS` with `ORDER BY d, id`: 10, 30, 60, 100, 100.
- `GROUPS BETWEEN 1 PRECEDING`: the previous date group plus the current one: 10, 60, 60, 90, 40.
- `EXCLUDE CURRENT ROW` on the whole frame: 90, 80, 70, 60, 100 (the total 100 minus the row itself).
- `RANGE 1 PRECEDING` ordered by `julianday(d)`: 10, 60, 60, 40, 40: row 4 (01-05) sees nothing from 01-02 because it is 3 days earlier. The same `RANGE` ordered by the text `d`: 10, 50, 50, 40, NULL, which is wrong and raised no error.

**Code:** run with `python3 -I`; every probe prints OK with its result or ERROR with SQLite's message.
```python
# Q42: dialect probes on SQLite, each one run; the table in the answer is built from this output
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE t(id INTEGER PRIMARY KEY, d TEXT, v INTEGER);
INSERT INTO t VALUES (1,'2024-01-01',10),(2,'2024-01-02',20),(3,'2024-01-02',30),
  (4,'2024-01-05',40),(5,'2024-01-06',NULL);
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("SQLite", sqlite3.sqlite_version)

def probe(name, sql):
    try:
        rows = [r[-1] if len(r) > 1 else r[0] for r in con.execute(sql)]
        print(f"{name:34s} OK     {rows}")
        return rows
    except Exception as e:
        print(f"{name:34s} ERROR  {type(e).__name__}: {e}")
        return None

lag_default = probe("LAG(v,1,-1) default arg",
    "SELECT id, LAG(v, 1, -1) OVER (ORDER BY id) FROM t ORDER BY id")
default_frame = probe("default frame, duplicate dates",
    "SELECT id, SUM(v) OVER (ORDER BY d) FROM t ORDER BY id")
rows_frame = probe("ROWS frame + tie-break",
    "SELECT id, SUM(v) OVER (ORDER BY d, id ROWS UNBOUNDED PRECEDING) FROM t ORDER BY id")
groups = probe("GROUPS BETWEEN 1 PRECEDING",
    "SELECT id, SUM(v) OVER (ORDER BY d GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) FROM t ORDER BY id")
excl = probe("EXCLUDE CURRENT ROW",
    "SELECT id, SUM(v) OVER (ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING EXCLUDE CURRENT ROW) FROM t ORDER BY id")
range_text = probe("RANGE 1 PRECEDING on TEXT date",
    "SELECT id, SUM(v) OVER (ORDER BY d RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) FROM t ORDER BY id")
range_jd = probe("RANGE 1 PRECEDING on julianday(d)",
    "SELECT id, SUM(v) OVER (ORDER BY julianday(d) RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) FROM t ORDER BY id")
probe("RANGE INTERVAL 1 DAY PRECEDING",
    "SELECT id, SUM(v) OVER (ORDER BY d RANGE BETWEEN INTERVAL 1 DAY PRECEDING AND CURRENT ROW) FROM t")
probe("IGNORE NULLS in LAST_VALUE",
    "SELECT id, LAST_VALUE(v) IGNORE NULLS OVER (ORDER BY id) FROM t")
probe("COUNT(DISTINCT v) OVER",
    "SELECT id, COUNT(DISTINCT v) OVER (ORDER BY id) FROM t")
probe("DATE_TRUNC('month', d)", "SELECT DATE_TRUNC('month', d) FROM t")
probe("DATEDIFF('day', a, b)", "SELECT DATEDIFF('day', '2024-01-01', '2024-01-05')")
probe("julianday diff", "SELECT julianday('2024-01-05') - julianday('2024-01-01')")
probe("strftime month start", "SELECT date(d, 'start of month') FROM t WHERE id = 1")
probe("QUALIFY", "SELECT id FROM t QUALIFY ROW_NUMBER() OVER (ORDER BY id) = 1")
probe("FILTER on a window aggregate",
    "SELECT id, SUM(v) FILTER (WHERE v > 15) OVER (ORDER BY id) FROM t ORDER BY id")
probe("NTH_VALUE(v, 2)", "SELECT id, NTH_VALUE(v, 2) OVER (ORDER BY id ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) FROM t ORDER BY id")
probe("LAST_VALUE default frame",
    "SELECT id, LAST_VALUE(v) OVER (ORDER BY id) FROM t ORDER BY id")

df = pd.read_sql_query("SELECT * FROM t ORDER BY id", con)
# pd:main
lag_pd = df["v"].shift(1, fill_value=-1)
default_pd = df["v"].fillna(0).cumsum().groupby(df["d"]).transform("max")
day = pd.to_datetime(df["d"]).map(pd.Timestamp.toordinal)
range_pd = [df.loc[(day >= x - 1) & (day <= x), "v"].sum(min_count=1) for x in day]
# pd:end
range_pd = [None if pd.isna(x) else int(x) for x in range_pd]
# compared in id order; min_count=1 makes an all-NULL frame NULL like SQL SUM
assert lag_default == [int(x) for x in lag_pd]
assert default_frame == [int(x) for x in default_pd]
assert range_jd == range_pd
print("\npandas shift(1, fill_value=-1):", [int(x) for x in lag_pd])
print("pandas peer-aware cumsum      :", [int(x) for x in default_pd])
print("pandas calendar-day window    :", range_pd)
print("RANGE on TEXT dates (wrong)   :", range_text, " vs correct:", range_jd)
print("asserts passed: LAG default == shift(fill_value), default-frame peers == cumsum then group max, julianday RANGE == calendar mask")
```

**Output (my run):**
```text
SQLite 3.45.1
LAG(v,1,-1) default arg            OK     [-1, 10, 20, 30, 40]
default frame, duplicate dates     OK     [10, 60, 60, 100, 100]
ROWS frame + tie-break             OK     [10, 30, 60, 100, 100]
GROUPS BETWEEN 1 PRECEDING         OK     [10, 60, 60, 90, 40]
EXCLUDE CURRENT ROW                OK     [90, 80, 70, 60, 100]
RANGE 1 PRECEDING on TEXT date     OK     [10, 50, 50, 40, None]
RANGE 1 PRECEDING on julianday(d)  OK     [10, 60, 60, 40, 40]
RANGE INTERVAL 1 DAY PRECEDING     ERROR  OperationalError: near "1": syntax error
IGNORE NULLS in LAST_VALUE         ERROR  OperationalError: near "NULLS": syntax error
COUNT(DISTINCT v) OVER             ERROR  OperationalError: DISTINCT is not supported for window functions
DATE_TRUNC('month', d)             ERROR  OperationalError: no such function: DATE_TRUNC
DATEDIFF('day', a, b)              ERROR  OperationalError: no such function: DATEDIFF
julianday diff                     OK     [4.0]
strftime month start               OK     ['2024-01-01']
QUALIFY                            ERROR  OperationalError: near "ROW_NUMBER": syntax error
FILTER on a window aggregate       OK     [None, 20, 50, 90, 90]
NTH_VALUE(v, 2)                    OK     [20, 20, 20, 20, 20]
LAST_VALUE default frame           OK     [10, 20, 30, 40, None]

pandas shift(1, fill_value=-1): [-1, 10, 20, 30, 40]
pandas peer-aware cumsum      : [10, 60, 60, 100, 100]
pandas calendar-day window    : [10, 60, 60, 40, 40]
RANGE on TEXT dates (wrong)   : [10, 50, 50, 40, None]  vs correct: [10, 60, 60, 40, 40]
asserts passed: LAG default == shift(fill_value), default-frame peers == cumsum then group max, julianday RANGE == calendar mask
```

**Edge cases:**
- Default frame with duplicate dates: peers share a total; that is the standard rule, and my run shows it. Fix with a unique tie-breaker and `ROWS`.
- `RANGE` with a numeric offset on a TEXT date column: no error, wrong sums (the output above). Order by `julianday(d)` or a day number instead.
- `LAST_VALUE` with the default frame returns the current row's value (10, 20, 30, 40, NULL in my run), not the last one.
- `NTH_VALUE(v, 2)` with a full frame gave 20 on every row.
- pandas counterparts that I asserted: `shift(1, fill_value=-1)` equals `LAG(v, 1, -1)`; cumulative sum then the group maximum equals the default frame with ties; a calendar-day mask equals `RANGE ... julianday`.

**Then explain:**
Verified by running on SQLite 3.45.1 (this run) versus hedged (not executed here). Names in the first column are the probes in the Code block.
| Topic | Verified by running on SQLite | Hedged, not executed |
|---|---|---|
| LAG default argument | `LAG(v, 1, -1)` works: [-1, 10, 20, 30, 40] | PostgreSQL and MySQL 8.0 accept the same three-argument form (from memory) |
| Default frame | `ORDER BY` without a frame gives `RANGE UNBOUNDED PRECEDING` to the current row including peers (60, 60 on the tied date) | The standard says the same; I have seen claims that a few engines default differently, so check each engine's docs (not verified) |
| GROUPS frames | Works: `GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW` | PostgreSQL 11+ (from memory); not in MySQL 8.0 (from memory) |
| EXCLUDE | `EXCLUDE CURRENT ROW` works | PostgreSQL 11+ (from memory); not in MySQL 8.0 (from memory) |
| RANGE with a number offset | Works on a numeric key (`julianday(d)`); on TEXT dates it gave wrong sums with no error | PostgreSQL needs numeric or date/timestamp ordering key; MySQL has RANGE offsets too (from memory) |
| RANGE with INTERVAL | `RANGE BETWEEN INTERVAL 1 DAY PRECEDING` is a syntax error | PostgreSQL uses `INTERVAL '1 day'` for date/timestamp keys (the docs page I opened says the offset is an interval); MySQL accepts `INTERVAL 1 DAY` (from memory); BigQuery and Snowflake support differs, check docs |
| IGNORE NULLS | `LAST_VALUE(v) IGNORE NULLS` is a syntax error | The PostgreSQL docs I opened say it is not implemented there; other engines (for example Snowflake, BigQuery, Oracle) have it, from memory |
| COUNT(DISTINCT) OVER | Error: DISTINCT is not supported for window functions | A PostgreSQL mailing-list snippet says the same for PostgreSQL; other engines vary |
| Date difference | `julianday(b) - julianday(a)` works (4.0); `DATEDIFF` fails with no such function | MySQL `DATEDIFF(a, b)` returns days; SQL Server and Snowflake `DATEDIFF(day, a, b)`; BigQuery `DATE_DIFF`; PostgreSQL subtracts dates (all from memory) |
| DATE_TRUNC | Fails: no such function. `date(d, 'start of month')` works | PostgreSQL, Snowflake and BigQuery have `DATE_TRUNC` (BigQuery's argument order differs); MySQL does not (use `DATE_FORMAT` or `DATE_SUB`); from memory |
| QUALIFY | Syntax error | Snowflake, BigQuery and a few others have it (from memory) |
| Window support | Works since 3.25 (per the SQLite page opened in Part 4) | MySQL 8.0 has window functions; 5.7 has none (from memory) |
| FILTER on a window aggregate | Works: `SUM(v) FILTER (WHERE v > 15) OVER (...)` | PostgreSQL has it; MySQL does not (from memory) |
- Rule I follow in an interview: say which engine I am on, keep the portable core (`ROWS` + unique order), and look up the engine's rules for frames, intervals and date functions.

**Follow-ups:**
- *Which engines differ on the default frame?* I would say 'the standard says RANGE through peers; I check the manual for each engine' rather than guess.
- *Why not use DATEDIFF here?* SQLite does not have it; `julianday` differences are in days.
- *How do I port a GROUPS query?* Replace it with a `RANGE` over a day number, or number the groups with `DENSE_RANK` and join.

**Common mistakes:**
- Assuming SQLite error-checks `RANGE` offsets on text.
- Quoting engine support from memory as if it were tested.
- Using `LAST_VALUE` with the default frame and expecting the last row.
- Assuming `DATE_TRUNC` or `QUALIFY` exists everywhere.

### Q43 ⭐ 🔴 Cumulative sum that resets when a condition is met: payments(payment_id, user_id, amount) in order. Keep a running sum per user that restarts from zero once it reaches or exceeds 100 (the row that crosses the cap closes the batch). Show why plain SUM OVER cannot do it, solve with a recursive CTE and run it, give the pandas loop or numba-free groupby-apply version, and say that this and related 'reset on flag' problems are gaps-and-islands territory (Part 7).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Plain `SUM() OVER` cannot reset, because each row's total depends on the previous output, so I use a recursive CTE that carries the running value (`CASE WHEN prev >= 100 THEN amount ELSE prev + amount END`); in pandas it is a loop inside `groupby().transform`, and this family of reset-on-condition problems is gaps-and-islands territory (Part 7).

**Schema and sample data:** thirteen payments for three users in `payment_id` order. User 1 crosses 100 at payment 3 (40 + 30 + 50 = 120), user 2 pays 100 twice, user 3 reaches exactly 100.
```sql
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, amount INTEGER);
INSERT INTO payments VALUES (1,1,40),(2,1,30),(3,1,50),(4,1,20),(5,1,90),(6,1,15),
  (7,2,100),(8,2,100),(9,2,60),(10,2,10),(11,3,99),(12,3,1),(13,3,5);
```

**SQL answer:** `SQL_PLAIN` shows what the plain window does (never resets). `SQL_MAIN` is the recursive version; order inside a user is `payment_id` (unique, so no ties).
```sql
SELECT payment_id, user_id, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY payment_id) AS plain_running
FROM payments ORDER BY payment_id
```
```sql
WITH RECURSIVE o AS (
  SELECT payment_id, user_id, amount,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY payment_id) AS n
  FROM payments
),
r(payment_id, user_id, n, amount, running) AS (
  SELECT payment_id, user_id, n, amount, amount FROM o WHERE n = 1
  UNION ALL
  SELECT o.payment_id, o.user_id, o.n, o.amount,
         CASE WHEN r.running >= 100 THEN o.amount ELSE r.running + o.amount END
  FROM o JOIN r ON o.user_id = r.user_id AND o.n = r.n + 1
)
SELECT payment_id, user_id, amount, running,
       CASE WHEN running >= 100 THEN 'closes batch' ELSE '' END AS flag
FROM r ORDER BY payment_id
```

**pandas answer:** A plain loop, applied per user with `transform`.
```py
def capped_running(s, cap=100):
    out, run = [], 0
    for a in s:
        run = a if run >= cap else run + a
        out.append(run)
    return pd.Series(out, index=s.index)

pay = pay.sort_values(["user_id", "payment_id"])
pay["running"] = pay.groupby("user_id")["amount"].transform(capped_running)
pay["flag"] = pay["running"].ge(100).map({True: "closes batch", False: ""})
```

**Example:**
User 1 amounts 40, 30, 50, 20, 90, 15:
- 40, then 70, then 120: it reached 100, so the row closes the batch.
- Next row starts again: 20. Then 20 + 90 = 110: closes again. Then 15.
- Running column: 40, 70, 120, 20, 110, 15.
User 2: 100 closes at once (100 >= 100), the next 100 starts a new batch and closes too, then 60, 70. User 3: 99, then 99 + 1 = 100 closes, then 5.
The plain `SUM OVER` gives 40, 70, 120, 140, 230, 245 for user 1: the 20 is added to 120.

**Code:** run with `python3 -I`.
```python
# Q43: running sum per user that restarts once it reaches or exceeds 100
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, amount INTEGER);
INSERT INTO payments VALUES (1,1,40),(2,1,30),(3,1,50),(4,1,20),(5,1,90),(6,1,15),
  (7,2,100),(8,2,100),(9,2,60),(10,2,10),(11,3,99),(12,3,1),(13,3,5);
"""
# order inside a user = payment_id (unique), so no tie problem
SQL_PLAIN = """
SELECT payment_id, user_id, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY payment_id) AS plain_running
FROM payments ORDER BY payment_id
"""
SQL_MAIN = """
WITH RECURSIVE o AS (
  SELECT payment_id, user_id, amount,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY payment_id) AS n
  FROM payments
),
r(payment_id, user_id, n, amount, running) AS (
  SELECT payment_id, user_id, n, amount, amount FROM o WHERE n = 1
  UNION ALL
  SELECT o.payment_id, o.user_id, o.n, o.amount,
         CASE WHEN r.running >= 100 THEN o.amount ELSE r.running + o.amount END
  FROM o JOIN r ON o.user_id = r.user_id AND o.n = r.n + 1
)
SELECT payment_id, user_id, amount, running,
       CASE WHEN running >= 100 THEN 'closes batch' ELSE '' END AS flag
FROM r ORDER BY payment_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("plain SUM OVER (never resets):")
print(pd.read_sql_query(SQL_PLAIN, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nrecursive CTE with reset:"); print(sql_df.to_string(index=False))

pay = pd.read_sql_query("SELECT * FROM payments ORDER BY payment_id", con)
# pd:main
def capped_running(s, cap=100):
    out, run = [], 0
    for a in s:
        run = a if run >= cap else run + a
        out.append(run)
    return pd.Series(out, index=s.index)

pay = pay.sort_values(["user_id", "payment_id"])
pay["running"] = pay.groupby("user_id")["amount"].transform(capped_running)
pay["flag"] = pay["running"].ge(100).map({True: "closes batch", False: ""})
# pd:end
# compared after sorting by payment_id
pd.testing.assert_frame_equal(sql_df, pay.sort_values("payment_id").reset_index(drop=True)[sql_df.columns], check_dtype=False)

# NULL amount: in SQL the NULL poisons the rest of the chain
con.executescript("""
CREATE TABLE p2(payment_id INTEGER PRIMARY KEY, user_id INTEGER, amount INTEGER);
INSERT INTO p2 VALUES (1,1,60),(2,1,NULL),(3,1,70),(4,1,30);
""")
q = SQL_MAIN.replace("FROM payments", "FROM p2")
print("\nNULL amount, as is:", [r[3] for r in con.execute(q)])
q2 = q.replace("SELECT payment_id, user_id, amount,\n         ROW_NUMBER()", "SELECT payment_id, user_id, COALESCE(amount, 0) AS amount,\n         ROW_NUMBER()")
print("NULL amount treated as 0 (COALESCE inside o):", [r[3] for r in con.execute(q2)])
print("pandas loop with NaN:", capped_running(pd.Series([60, None, 70, 30])).tolist())
print("asserts passed: recursive CTE == pandas groupby transform with a Python loop")
```

**Output (my run):**
```text
plain SUM OVER (never resets):
 payment_id  user_id  amount  plain_running
          1        1      40             40
          2        1      30             70
          3        1      50            120
          4        1      20            140
          5        1      90            230
          6        1      15            245
          7        2     100            100
          8        2     100            200
          9        2      60            260
         10        2      10            270
         11        3      99             99
         12        3       1            100
         13        3       5            105

recursive CTE with reset:
 payment_id  user_id  amount  running         flag
          1        1      40       40             
          2        1      30       70             
          3        1      50      120 closes batch
          4        1      20       20             
          5        1      90      110 closes batch
          6        1      15       15             
          7        2     100      100 closes batch
          8        2     100      100 closes batch
          9        2      60       60             
         10        2      10       70             
         11        3      99       99             
         12        3       1      100 closes batch
         13        3       5        5             

NULL amount, as is: [60, None, None, None]
NULL amount treated as 0 (COALESCE inside o): [60, 60, 130, 30]
pandas loop with NaN: [60.0, nan, nan, nan]
asserts passed: recursive CTE == pandas groupby transform with a Python loop
```

**Edge cases:**
- Exactly 100 closes the batch (`>=`), as asked; user 3's 99 + 1 is the case.
- A single payment of 100 or more closes the batch by itself (user 2).
- The row that crosses the cap keeps the crossing total (120, 110): it is not clipped to 100 and the extra is not carried to the next batch. If the business wants the overflow carried, that is a different rule.
- NULL amount: it poisons the SQL chain. In my run, amounts 60, NULL, 70, 30 gave 60, NULL, NULL, NULL. `COALESCE(amount, 0)` inside the numbered CTE gave 60, 60, 130, 30. The pandas loop with NaN also poisons (60, NaN, NaN, NaN). Decide what a NULL payment means.
- Order: unique `payment_id`. If order were by a date with ties, the batches would depend on the tie-break; add one.
- Empty user: no rows, no output.

**Then explain:**
- Why a plain window fails: the reset depends on the previous result (was the last running value >= 100?), and a window frame reads input values, not earlier output. `SUM() OVER` always adds from the start of the partition. Subtracting `FLOOR(total / 100) * 100` does not work either, because the batch closes when the running sum first reaches 100, and the overshoot depends on the amounts.
- Recursive CTE: the first row of each user starts the chain; each next row looks at the previous row's `running`. The join key is `user_id` plus `n = n + 1`.
- pandas: the loop is the honest solution; `cumsum` cannot express the reset, and there is no vectorised trick for this exact rule. A numba or Cython loop speeds it up (I did not use either).
- Gaps and islands: 'start a new group when a condition on the running state is met' belongs with Part 7 (streaks, sessionization). The usual trick there is a flag plus a running count of flags to name the batch, which works when the reset depends on the current row only; here it depends on the running total, so the recursion is the clean solution.

**Follow-ups:**
- *Number the batches?* Carry a `batch_no` column in the recursion (add 1 when the previous running value was >= 100).
- *Cap per user per month?* Add the month to the partition.
- *Millions of users?* A recursive CTE is sequential per user; do it in Python/Spark per partition (not executed).

**Common mistakes:**
- Trying `SUM OVER` with `MOD`.
- Using `>` instead of `>=`.
- Clipping the crossing row to 100 without saying so.
- Not deciding what a NULL amount does.

### Q44 ⭐ 🔴 Running rank (rank among everything seen so far): scores(game_id, game_date, score). For each game, return its rank among all games up to and including that date (how many earlier games scored higher, plus one), and flag new all-time records. Show the correlated subquery or self-join (a window function cannot rank over an expanding set directly), the RANK-based approach over cumulative flags where possible, and pandas expanding().rank() (run it on pandas 3.0.x) or an O(n^2) loop.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** For each game, rank = 1 + the number of earlier games with a higher score, which needs a correlated subquery or self-join because a window frame cannot rank over an expanding set; a new record is a score above the maximum of everything before it, which a `MAX() OVER (... 1 PRECEDING)` window gives directly; pandas does the rank with `expanding().rank()`.

**Schema and sample data:** eight games; games 5 and 6 share a date, games 2 and 4 tie on 70.
```sql
CREATE TABLE scores(game_id INTEGER PRIMARY KEY, game_date TEXT, score INTEGER);
INSERT INTO scores VALUES (1,'2024-01-01',50),(2,'2024-01-02',70),(3,'2024-01-03',60),
  (4,'2024-01-04',70),(5,'2024-01-05',90),(6,'2024-01-05',95),(7,'2024-01-06',40),(8,'2024-01-07',80);
```

**SQL answer:** Sequence is `(game_date, game_id)`, so two games on one date are ordered by `game_id` (stated tie-breaker). 'Earlier' means earlier in that sequence. `SQL_MAIN` is the correlated version, `SQL_JOIN` the self-join, `SQL_WIN` the window-only record flag.
```sql
SELECT s.game_id, s.game_date, s.score,
       1 + (SELECT COUNT(*) FROM scores p
            WHERE (p.game_date < s.game_date OR (p.game_date = s.game_date AND p.game_id < s.game_id))
              AND p.score > s.score) AS running_rank,
       CASE WHEN s.score > COALESCE((SELECT MAX(p.score) FROM scores p
            WHERE p.game_date < s.game_date OR (p.game_date = s.game_date AND p.game_id < s.game_id)), -1)
            THEN 1 ELSE 0 END AS new_record
FROM scores s
ORDER BY s.game_date, s.game_id
```
```sql
SELECT s.game_id, 1 + COUNT(p.game_id) AS running_rank
FROM scores s
LEFT JOIN scores p
  ON (p.game_date < s.game_date OR (p.game_date = s.game_date AND p.game_id < s.game_id))
 AND p.score > s.score
GROUP BY s.game_id
ORDER BY s.game_id
```
```sql
SELECT game_id,
       CASE WHEN score > COALESCE(MAX(score) OVER (ORDER BY game_date, game_id
                                   ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), -1)
            THEN 1 ELSE 0 END AS new_record
FROM scores ORDER BY game_date, game_id
```
The other reading, 'everything up to and including that date, same-date games included', is `SQL_DATE_INCL`:
```sql
SELECT s.game_id,
       1 + (SELECT COUNT(*) FROM scores p WHERE p.game_date <= s.game_date AND p.score > s.score) AS rank_date_inclusive
FROM scores s ORDER BY s.game_date, s.game_id
```

**pandas answer:** `expanding().rank()` ranks the newest element within everything seen so far; `method="min"` with `ascending=False` gives 1 + the count of higher scores, so a tie shares the best rank.
```py
sc["running_rank"] = sc["score"].expanding().rank(method="min", ascending=False).astype(int)
prior_max = sc["score"].cummax().shift(1)
sc["new_record"] = (sc["score"] > prior_max.fillna(-1)).astype(int)
```

**Example:**
Scores in order: 50, 70, 60, 70, 90, 95, 40, 80.
- Game 1: nothing earlier, rank 1, a record.
- Game 2 (70): earlier higher scores: none (50). Rank 1, record (70 > 50).
- Game 3 (60): one earlier higher (70). Rank 2, not a record.
- Game 4 (70): earlier higher: none (the other 70 is equal, not higher). Rank 1, but not a record because it only ties the maximum of 70.
- Game 5 (90): rank 1, record. Game 6 (95): rank 1, record.
- Game 7 (40): all six earlier are higher: rank 7. Game 8 (80): 90 and 95 are higher: rank 3.
- Date-inclusive reading: game 5 now sees game 6 (95) on the same date, so its rank is 2 instead of 1.
Running rank list: 1, 1, 2, 1, 1, 1, 7, 3. Record list: 1, 1, 0, 0, 1, 1, 0, 0.

**Code:** run with `python3 -I`; it also prints the global `RANK()` for contrast and the default `expanding().rank()`.
```python
# Q44: running rank among all games so far, and new all-time record flag
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE scores(game_id INTEGER PRIMARY KEY, game_date TEXT, score INTEGER);
INSERT INTO scores VALUES (1,'2024-01-01',50),(2,'2024-01-02',70),(3,'2024-01-03',60),
  (4,'2024-01-04',70),(5,'2024-01-05',90),(6,'2024-01-05',95),(7,'2024-01-06',40),(8,'2024-01-07',80);
"""
# sequence = (game_date, game_id): same-date games are ordered by game_id
SQL_MAIN = """
SELECT s.game_id, s.game_date, s.score,
       1 + (SELECT COUNT(*) FROM scores p
            WHERE (p.game_date < s.game_date OR (p.game_date = s.game_date AND p.game_id < s.game_id))
              AND p.score > s.score) AS running_rank,
       CASE WHEN s.score > COALESCE((SELECT MAX(p.score) FROM scores p
            WHERE p.game_date < s.game_date OR (p.game_date = s.game_date AND p.game_id < s.game_id)), -1)
            THEN 1 ELSE 0 END AS new_record
FROM scores s
ORDER BY s.game_date, s.game_id
"""
SQL_JOIN = """
SELECT s.game_id, 1 + COUNT(p.game_id) AS running_rank
FROM scores s
LEFT JOIN scores p
  ON (p.game_date < s.game_date OR (p.game_date = s.game_date AND p.game_id < s.game_id))
 AND p.score > s.score
GROUP BY s.game_id
ORDER BY s.game_id
"""
# record flag with windows only: compare with the maximum of all earlier rows
SQL_WIN = """
SELECT game_id,
       CASE WHEN score > COALESCE(MAX(score) OVER (ORDER BY game_date, game_id
                                   ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), -1)
            THEN 1 ELSE 0 END AS new_record
FROM scores ORDER BY game_date, game_id
"""
# same-date games count as 'seen so far' for each other (date-inclusive reading of the question)
SQL_DATE_INCL = """
SELECT s.game_id,
       1 + (SELECT COUNT(*) FROM scores p WHERE p.game_date <= s.game_date AND p.score > s.score) AS rank_date_inclusive
FROM scores s ORDER BY s.game_date, s.game_id
"""
SQL_GLOBAL = """
SELECT game_id, RANK() OVER (ORDER BY score DESC) AS global_rank FROM scores ORDER BY game_date, game_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
join_df = pd.read_sql_query(SQL_JOIN, con)
win_df = pd.read_sql_query(SQL_WIN, con)
dinc = pd.read_sql_query(SQL_DATE_INCL, con)
glob = pd.read_sql_query(SQL_GLOBAL, con)
print(sql_df.to_string(index=False))
print("\ndate-inclusive rank (same-date games see each other):", dinc["rank_date_inclusive"].tolist())
print("global RANK() over the whole table (not running)   :", glob["global_rank"].tolist())
assert join_df.sort_values("game_id")["running_rank"].tolist() == sql_df.sort_values("game_id")["running_rank"].tolist()
assert win_df["new_record"].tolist() == sql_df["new_record"].tolist()

sc = pd.read_sql_query("SELECT * FROM scores ORDER BY game_date, game_id", con)
# pd:main
sc["running_rank"] = sc["score"].expanding().rank(method="min", ascending=False).astype(int)
prior_max = sc["score"].cummax().shift(1)
sc["new_record"] = (sc["score"] > prior_max.fillna(-1)).astype(int)
# pd:end
loop = [1 + int(sum(sc["score"][j] > sc["score"][i] for j in range(i))) for i in range(len(sc))]
# compared in the order game_date, game_id
pd.testing.assert_frame_equal(sql_df[["game_id", "running_rank", "new_record"]], sc[["game_id", "running_rank", "new_record"]], check_dtype=False)
assert loop == sc["running_rank"].tolist()
print("\npandas expanding().rank(method='min', ascending=False):", sc["running_rank"].tolist())
print("O(n^2) loop:", loop)
print("expanding().rank default method (average):", sc["score"].expanding().rank(ascending=False).tolist())
print("asserts passed: correlated subquery == self-join == pandas expanding rank == loop; window MAX flag == cummax flag")
```

**Output (my run):**
```text
 game_id  game_date  score  running_rank  new_record
       1 2024-01-01     50             1           1
       2 2024-01-02     70             1           1
       3 2024-01-03     60             2           0
       4 2024-01-04     70             1           0
       5 2024-01-05     90             1           1
       6 2024-01-05     95             1           1
       7 2024-01-06     40             7           0
       8 2024-01-07     80             3           0

date-inclusive rank (same-date games see each other): [1, 1, 2, 1, 2, 1, 7, 3]
global RANK() over the whole table (not running)   : [7, 4, 6, 4, 2, 1, 8, 3]

pandas expanding().rank(method='min', ascending=False): [1, 1, 2, 1, 1, 1, 7, 3]
O(n^2) loop: [1, 1, 2, 1, 1, 1, 7, 3]
expanding().rank default method (average): [1.0, 1.0, 2.0, 1.5, 1.0, 1.0, 7.0, 3.0]
asserts passed: correlated subquery == self-join == pandas expanding rank == loop; window MAX flag == cummax flag
```

**Edge cases:**
- Ties on score: a tie with the best earlier score is rank 1 but not a record (game 4); say which you want. In my run `expanding().rank()` with the default `method='average'` gave 1.5 for game 4, so choose `method='min'`.
- Same-date games: with the sequence tie-break on `game_id`, game 5 does not see game 6 but game 6 sees game 5. With the date-inclusive reading both see each other (game 5 became rank 2). Both are shown.
- First row: no earlier games; `MAX` over an empty frame is NULL, so `COALESCE(..., -1)` makes the first game a record (assuming scores are non-negative).
- NULL score: `score > ...` is unknown, so no record and no rank; I did not add NULL scores to the data.
- Global rank is a different thing: `RANK() OVER (ORDER BY score DESC)` over the whole table gave 7, 4, 6, 4, 2, 1, 8, 3: it uses future games as well, so it is not the running rank.

**Then explain:**
- Why a window cannot do it: a window frame for row i would have to be 'all earlier rows', and then rank *within that frame by score*. `RANK() OVER (...)` ranks within the partition, not within a frame, so I count the higher earlier scores directly.
- Correlated subquery and self-join give the same answer (asserted). Both are quadratic: each game scans the earlier ones (O(n^2)); fine for hundreds of rows, not millions.
- Record flag: this one needs only the maximum before the row, so a window works: `MAX(score) OVER (ORDER BY game_date, game_id ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)`. It matches the correlated version (asserted) and is O(n). Equivalent in pandas: `cummax().shift(1)`.
- pandas: `Series.expanding().rank()` exists and ran on 3.0.5; it computes a rank in each growing window, so it is also quadratic in the worst case (I did not time it). The O(n^2) Python loop gave the same list (asserted).
- A 'top-N so far' is the same idea with a count threshold; ranking and top-N in general belong to Part 4.

**Follow-ups:**
- *Rank per player?* Add `AND p.player = s.player` / `groupby("player")`.
- *Faster than O(n^2)?* Keep a sorted structure of scores seen so far (a Fenwick tree or sorted list) in Python; SQL has no equivalent.
- *Percentile so far?* Divide the rank by the number of games seen.

**Common mistakes:**
- Using `RANK() OVER (ORDER BY score DESC)` and calling it a running rank.
- Counting ties as higher (`>=` instead of `>`).
- Ordering by date only and getting an undefined order for two games on one date.
- Calling a tie with the record a new record without saying so.

### Q45 ⭐ 🔴 Rolling 7-day active customers: orders(order_id, customer_id, order_date). For every date in the calendar, count distinct customers who ordered in the 7 days up to that date. Explain why COUNT(DISTINCT) OVER a frame fails, build it with a calendar CTE joined to orders on order_date between date - 6 and date, then give a window-based alternative using first-occurrence flags where a customer's activity interval is considered, and the pandas approach. Discuss cost.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `COUNT(DISTINCT x) OVER (...)` is rejected, so I build a calendar and join each date to orders from date - 6 to date with `COUNT(DISTINCT customer_id)`, and offer a window version that turns each customer's activity into non-overlapping covered segments and counts the segments alive per day; pandas does the same with a date range and `nunique`, or a per-customer `rolling('7D')`.

**Schema and sample data:** ten orders by four customers over 14 days; customer 1 orders twice on 05-01, and there are days with no orders.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT);
INSERT INTO orders VALUES (1,1,'2024-05-01'),(2,2,'2024-05-01'),(3,1,'2024-05-01'),(4,1,'2024-05-03'),
  (5,3,'2024-05-04'),(6,2,'2024-05-08'),(7,1,'2024-05-10'),(8,4,'2024-05-10'),(9,3,'2024-05-14'),
  (10,2,'2024-05-14');
```

**SQL answer:** `SQL_MAIN` is the calendar join (a recursive CTE `cal` builds one row per day). `SQL_WIN` is the window alternative, which I explain in 'Then explain'.
```sql
WITH RECURSIVE cal(d) AS (
  SELECT MIN(order_date) FROM orders
  UNION ALL
  SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(order_date) FROM orders)
)
SELECT c.d AS day, COUNT(DISTINCT o.customer_id) AS active_7d
FROM cal c
LEFT JOIN orders o ON o.order_date BETWEEN date(c.d, '-6 days') AND c.d
GROUP BY c.d
ORDER BY c.d
```
```sql
WITH RECURSIVE cal(d) AS (
  SELECT MIN(order_date) FROM orders
  UNION ALL
  SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(order_date) FROM orders)
)
, cd AS (SELECT DISTINCT customer_id, order_date AS d FROM orders),
seg AS (
  SELECT customer_id, d AS s,
         MIN(date(d, '+6 days'), COALESCE(date(LEAD(d) OVER (PARTITION BY customer_id ORDER BY d), '-1 day'), '9999-12-31')) AS e
  FROM cd
),
delta AS (
  SELECT s AS d, 1 AS x FROM seg
  UNION ALL
  SELECT date(e, '+1 day'), -1 FROM seg
)
SELECT c.d AS day,
       SUM(COALESCE(dl.x, 0)) OVER (ORDER BY c.d ROWS UNBOUNDED PRECEDING) AS active_7d
FROM cal c
LEFT JOIN (SELECT d, SUM(x) AS x FROM delta GROUP BY d) dl ON dl.d = c.d
ORDER BY c.d
```
The query that fails (`SQL_BAD`):
```sql
SELECT COUNT(DISTINCT customer_id) OVER (ORDER BY order_date RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) FROM orders
```

**pandas answer:** ```py
days = pd.date_range(o["order_date"].min(), o["order_date"].max(), freq="D")
active = [o.loc[(o["order_date"] >= d - pd.Timedelta(days=6)) & (o["order_date"] <= d), "customer_id"].nunique()
          for d in days]
pd_df = pd.DataFrame({"day": days.strftime("%Y-%m-%d"), "active_7d": active})
```

**Example:**
'The 7 days up to the date' means the date and the six days before it.
- 05-01: customers 1 and 2 (customer 1 twice, counted once): 2.
- 05-04: window 04-28 to 05-04: customers 1 (05-01, 05-03), 2 (05-01), 3 (05-04): 3.
- 05-07: window 05-01 to 05-07: still 1, 2, 3: 3. 05-08: window 05-02 to 05-08: 1 (05-03), 3 (05-04), 2 (05-08): 3.
- 05-10: window 05-04 to 05-10: customers 3, 2, 1, 4: 4. 05-11: window 05-05 to 05-11: 2, 1, 4: 3 (customer 3 dropped out).
- 05-14: window 05-08 to 05-14: 2, 1, 4, 3: 4.
- Days with no orders (05-02, 05-05, ...) still appear, because the calendar drives the query.

**Code:** run with `python3 -I`; it prints the error for `COUNT(DISTINCT) OVER`, both SQL versions side by side, and the `rolling('7D')` check.
```python
# Q45: rolling 7-day distinct active customers
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT);
INSERT INTO orders VALUES (1,1,'2024-05-01'),(2,2,'2024-05-01'),(3,1,'2024-05-01'),(4,1,'2024-05-03'),
  (5,3,'2024-05-04'),(6,2,'2024-05-08'),(7,1,'2024-05-10'),(8,4,'2024-05-10'),(9,3,'2024-05-14'),
  (10,2,'2024-05-14');
"""
SQL_MAIN = """
WITH RECURSIVE cal(d) AS (
  SELECT MIN(order_date) FROM orders
  UNION ALL
  SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(order_date) FROM orders)
)
SELECT c.d AS day, COUNT(DISTINCT o.customer_id) AS active_7d
FROM cal c
LEFT JOIN orders o ON o.order_date BETWEEN date(c.d, '-6 days') AND c.d
GROUP BY c.d
ORDER BY c.d
"""
# window alternative: each customer-day covers [d, d+6], but only up to the day before their next order,
# so a customer's covered days form non-overlapping segments; count segments alive per day
SQL_WIN = """
WITH RECURSIVE cal(d) AS (
  SELECT MIN(order_date) FROM orders
  UNION ALL
  SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(order_date) FROM orders)
)
, cd AS (SELECT DISTINCT customer_id, order_date AS d FROM orders),
seg AS (
  SELECT customer_id, d AS s,
         MIN(date(d, '+6 days'), COALESCE(date(LEAD(d) OVER (PARTITION BY customer_id ORDER BY d), '-1 day'), '9999-12-31')) AS e
  FROM cd
),
delta AS (
  SELECT s AS d, 1 AS x FROM seg
  UNION ALL
  SELECT date(e, '+1 day'), -1 FROM seg
)
SELECT c.d AS day,
       SUM(COALESCE(dl.x, 0)) OVER (ORDER BY c.d ROWS UNBOUNDED PRECEDING) AS active_7d
FROM cal c
LEFT JOIN (SELECT d, SUM(x) AS x FROM delta GROUP BY d) dl ON dl.d = c.d
ORDER BY c.d
"""
SQL_BAD = "SELECT COUNT(DISTINCT customer_id) OVER (ORDER BY order_date RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) FROM orders"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
try:
    con.execute(SQL_BAD)
except Exception as e:
    print("COUNT(DISTINCT) OVER:", type(e).__name__, "-", e)
sql_df = pd.read_sql_query(SQL_MAIN, con)
win_df = pd.read_sql_query(SQL_WIN, con)
print(pd.concat([sql_df, win_df["active_7d"].rename("window_version")], axis=1).to_string(index=False))
assert sql_df.equals(win_df)

o = pd.read_sql_query("SELECT * FROM orders", con)
o["order_date"] = pd.to_datetime(o["order_date"])
# pd:main
days = pd.date_range(o["order_date"].min(), o["order_date"].max(), freq="D")
active = [o.loc[(o["order_date"] >= d - pd.Timedelta(days=6)) & (o["order_date"] <= d), "customer_id"].nunique()
          for d in days]
pd_df = pd.DataFrame({"day": days.strftime("%Y-%m-%d"), "active_7d": active})
# pd:end
# compared in calendar order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

# a faster pandas route: one 0/1 row per customer-day, per-customer rolling '7D', then count customers still active
cd = o.drop_duplicates(["customer_id", "order_date"]).assign(one=1).sort_values(["customer_id", "order_date"])
roll = cd.groupby("customer_id").rolling("7D", on="order_date")["one"].sum().reset_index()
print("\ngroupby().rolling('7D', on=...) returns columns:", list(roll.columns))
# SQL day-number RANGE equivalent of rolling('7D') on daily timestamps: (t-7D, t] == t-6 .. t
con.execute("CREATE TABLE cd AS SELECT DISTINCT customer_id, order_date FROM orders")
sql_roll = pd.read_sql_query("""SELECT customer_id, order_date,
    SUM(1) OVER (PARTITION BY customer_id ORDER BY julianday(order_date)
                 RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS n
    FROM cd ORDER BY customer_id, order_date""", con)
roll = roll.sort_values(["customer_id", "order_date"]).reset_index(drop=True)
assert sql_roll["n"].tolist() == roll["one"].astype(int).tolist()
print("rolling('7D') == RANGE BETWEEN 6 PRECEDING over julianday, per customer:", sql_roll["n"].tolist())
print("asserts passed: calendar join == segment-window version == pandas loop; rolling('7D') == SQL RANGE 6 PRECEDING")
```

**Output (my run):**
```text
COUNT(DISTINCT) OVER: OperationalError - DISTINCT is not supported for window functions
       day  active_7d  window_version
2024-05-01          2               2
2024-05-02          2               2
2024-05-03          2               2
2024-05-04          3               3
2024-05-05          3               3
2024-05-06          3               3
2024-05-07          3               3
2024-05-08          3               3
2024-05-09          3               3
2024-05-10          4               4
2024-05-11          3               3
2024-05-12          3               3
2024-05-13          3               3
2024-05-14          4               4

groupby().rolling('7D', on=...) returns columns: ['customer_id', 'order_date', 'one']
rolling('7D') == RANGE BETWEEN 6 PRECEDING over julianday, per customer: [1, 2, 1, 1, 1, 2, 1, 1, 1]
asserts passed: calendar join == segment-window version == pandas loop; rolling('7D') == SQL RANGE 6 PRECEDING
```

**Edge cases:**
- `COUNT(DISTINCT) OVER`: SQLite 3.45.1 raised `DISTINCT is not supported for window functions` (run). A PostgreSQL mailing-list snippet says it is not implemented there either; other engines differ (not executed).
- Duplicate orders for one customer on one day: counted once by `DISTINCT`, and deduplicated first (`SELECT DISTINCT customer_id, order_date`) in the window version.
- Days with no orders: the calendar plus `LEFT JOIN` gives 0 for a day nobody was in the window (none in this data, but the join handles it).
- Calendar edges: it runs from the first to the last order date. Days after the last order are not shown, and the first six days have partial windows; say whether that is wanted.
- Text dates must be ISO `YYYY-MM-DD` for `BETWEEN` and `date(...)` to work.
- Equivalence check: pandas `groupby('customer_id').rolling('7D', on='order_date')` uses the window (t - 7D, t], which for midnight timestamps is t - 6 days to t. On the customer-day data it matched `SUM(1) OVER (PARTITION BY customer_id ORDER BY julianday(order_date) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW)` row for row (asserted).

**Then explain:**
- Why `COUNT(DISTINCT) OVER` fails: a distinct count over a sliding frame needs a set of seen values per frame; most window implementations cannot maintain one incrementally, so the engine rejects it (SQLite does here; I did not test others).
- Calendar join: for each date, find orders in `[date - 6, date]` and count distinct customers. Easy to read and always correct. Cost: each calendar day touches all orders in its window, roughly days x orders per window; with an index on `order_date` that is fine; without one it is days x all orders.
- Window alternative: a customer is active on day x if they ordered in `[x - 6, x]`. For each customer-day `d` with next order `n`, the days it newly covers are `d` to `min(d + 6, n - 1)`, so a customer's covered days form non-overlapping segments. Add +1 on a segment's start day and -1 the day after its end, then a running `SUM` of those deltas over the calendar gives the number of customers active. That is the 'first occurrence' idea: count a customer once at the start of each stretch of activity. It matched the join version on all 14 days. It scans orders about once plus one window pass; but it is harder to read, and the segment ends depend on `LEAD` and on the 6-day rule.
- pandas: the loop in `pd:main` is O(days x orders); the code also runs a per-customer `rolling('7D')` on customer-days (used for the equivalence check with SQL `RANGE`); turning that into a daily distinct count needs one more step that I did not write. `nunique` per window is the simplest.
- Scope: retention and cohort logic belongs to Part 6.

**Follow-ups:**
- *Make it 30 days?* Change 6 to 29 (or window length minus 1); the segment version changes `+6 days` to `+29 days`.
- *Weekly active by calendar week instead?* Group by week; a different problem (Part 6).
- *Millions of orders?* Pre-aggregate to customer-days, index the date, or use an approximate distinct count (HyperLogLog) where the engine offers it (not executed).

**Common mistakes:**
- Using `BETWEEN date - 7 AND date`, which is eight days.
- Using `COUNT(order_id)` and counting orders, not customers.
- Building the answer from `orders` alone and missing the days with no orders.
- Counting a customer twice in the window version when two segments overlap.

### Q46 ⭐ 🔴 Window query fault-finding drill: given a running-total report that is off by a few rows, list five suspects in the order you would check them (duplicate dates and the default RANGE frame, missing PARTITION BY, ORDER BY on a text column that sorts wrongly, a join fan-out before the window, NULLs in the summed column) and show for each a tiny reproducing query on SQLite and the pandas counterpart where one exists. Finish with how you would prove the fixed total equals SUM(amount) per group.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** I check, in this order: (1) duplicate dates with the default `RANGE` frame, (2) a missing `PARTITION BY`, (3) `ORDER BY` on text that sorts wrongly, (4) a join fan-out before the window, (5) NULLs in the summed column; then I prove the fix by tying the last running total of each group to `SUM(amount)` and the report's row count to the source's.

**Schema and sample data:** four small tables; the first has account A with two transactions on one date, and account B.
```sql
CREATE TABLE tx(id INTEGER PRIMARY KEY, acct TEXT, d TEXT, amount INTEGER);
INSERT INTO tx VALUES (1,'A','2024-03-01',100),(2,'A','2024-03-02',50),(3,'A','2024-03-02',25),
  (4,'A','2024-03-03',10),(5,'B','2024-03-01',200),(6,'B','2024-03-04',-40);
CREATE TABLE tx_txt(id INTEGER PRIMARY KEY, d TEXT, amount INTEGER);       -- dates stored as DD/MM/YYYY text
INSERT INTO tx_txt VALUES (1,'09/03/2024',10),(2,'10/03/2024',20),(3,'02/04/2024',30);
CREATE TABLE tags(id INTEGER, tag TEXT);                                    -- id 2 has two tags
INSERT INTO tags VALUES (2,'promo'),(2,'vip'),(4,'promo');
CREATE TABLE tx_null(id INTEGER PRIMARY KEY, d TEXT, amount INTEGER);
INSERT INTO tx_null VALUES (1,'2024-03-01',NULL),(2,'2024-03-02',30),(3,'2024-03-03',NULL),(4,'2024-03-04',20);
```

**SQL answer:** All the broken and fixed queries are in the Code block, printed one after another. The fix for suspect 1, as an example:
```sql
SELECT id, d, amount, SUM(amount) OVER (PARTITION BY acct ORDER BY d, id ROWS UNBOUNDED PRECEDING) AS rt
FROM tx WHERE acct = 'A' ORDER BY d, id
```
The check is `proof_sql` in the Code block.

**pandas answer:** All five counterparts are in the `pd:main` block below; what each one reproduces is listed in the table under 'Then explain'.
```py
a = tx[tx["acct"] == "A"].sort_values(["d", "id"])
fix1 = a["amount"].cumsum()                                              # suspect 1: row-based, ties never merge
peer = a["amount"].cumsum().groupby(a["d"]).transform("max")             # what the default RANGE frame did
fix2 = tx.sort_values(["acct", "d", "id"]).groupby("acct")["amount"].cumsum()   # suspect 2
bad2 = tx.sort_values(["d", "id"])["amount"].cumsum()
tt = pd.read_sql_query("SELECT * FROM tx_txt", con)
bad3 = tt.sort_values("d")["amount"].cumsum()                            # suspect 3: string sort
fix3 = tt.assign(k=pd.to_datetime(tt["d"], format="%d/%m/%Y")).sort_values(["k", "id"])["amount"].cumsum()
fan = tx[tx["acct"] == "A"].merge(pd.read_sql_query("SELECT * FROM tags", con), on="id", how="left")
bad4 = fan.sort_values(["d", "id"])["amount"].cumsum()                   # suspect 4: merge fan-out
nul = pd.read_sql_query("SELECT * FROM tx_null ORDER BY d, id", con)
nul_cum = nul["amount"].cumsum()                                         # suspect 5
```

**Example:**
Walk through the suspects on the sample data (account A is 100, 50, 25, 10; its correct total is 185):
1. Duplicate dates, default frame: ids 2 and 3 share 03-02, so both show 175 and the 150 never appears. Correct: 100, 150, 175, 185.
2. Missing `PARTITION BY`: ordered by date and id, B's first row (id 5) shows 300, which is A's 100 plus its own 200, and B's last row shows 345. Correct B: 200, 160.
3. Text dates: '02/04/2024' (2 April) sorts before '09/03/2024' (9 March) as text, so the running totals are 30, 40, 60 instead of 10, 30, 60.
4. Join fan-out: id 2 has two tags, so after the join its 50 appears twice: 100, 150, 200, 225, 235 instead of 100, 150, 175, 185, and five rows instead of four.
5. NULLs: amounts NULL, 30, NULL, 20 give running 'NULL, 30, 30, 50': the first NULL row shows NULL (not 0), the later NULL row repeats the total.
Proof: A: last running total 185 = SUM 185, B: 160 = 160; row counts 4 and 2 match the source. On the report without `PARTITION BY` the last totals are 385 and 345, so the check fails, which is what a check is for.

**Code:** run with `python3 -I`.
```python
# Q46: fault-finding drill for a running-total report
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE tx(id INTEGER PRIMARY KEY, acct TEXT, d TEXT, amount INTEGER);
INSERT INTO tx VALUES (1,'A','2024-03-01',100),(2,'A','2024-03-02',50),(3,'A','2024-03-02',25),
  (4,'A','2024-03-03',10),(5,'B','2024-03-01',200),(6,'B','2024-03-04',-40);
CREATE TABLE tx_txt(id INTEGER PRIMARY KEY, d TEXT, amount INTEGER);
INSERT INTO tx_txt VALUES (1,'09/03/2024',10),(2,'10/03/2024',20),(3,'02/04/2024',30);
CREATE TABLE tags(id INTEGER, tag TEXT);
INSERT INTO tags VALUES (2,'promo'),(2,'vip'),(4,'promo');
CREATE TABLE tx_null(id INTEGER PRIMARY KEY, d TEXT, amount INTEGER);
INSERT INTO tx_null VALUES (1,'2024-03-01',NULL),(2,'2024-03-02',30),(3,'2024-03-03',NULL),(4,'2024-03-04',20);
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def show(title, sql):
    df = pd.read_sql_query(sql, con)
    print(title); print(df.to_string(index=False)); print()
    return df

# 1. duplicate dates + default RANGE frame
s1_bad = show("1 BAD  default frame (RANGE through peers), rows 2 and 3 share a date:", """
SELECT id, d, amount, SUM(amount) OVER (PARTITION BY acct ORDER BY d) AS rt FROM tx WHERE acct = 'A' ORDER BY d, id""")
SQL_FIX1 = """
SELECT id, d, amount, SUM(amount) OVER (PARTITION BY acct ORDER BY d, id ROWS UNBOUNDED PRECEDING) AS rt
FROM tx WHERE acct = 'A' ORDER BY d, id"""
s1_fix = show("1 FIX  ORDER BY d, id with ROWS:", SQL_FIX1)

# 2. missing PARTITION BY
s2_bad = show("2 BAD  no PARTITION BY (accounts bleed into each other):", """
SELECT id, acct, amount, SUM(amount) OVER (ORDER BY d, id ROWS UNBOUNDED PRECEDING) AS rt FROM tx ORDER BY d, id""")
SQL_FIX2 = """
SELECT id, acct, amount, SUM(amount) OVER (PARTITION BY acct ORDER BY d, id ROWS UNBOUNDED PRECEDING) AS rt
FROM tx ORDER BY acct, d, id"""
s2_fix = show("2 FIX  PARTITION BY acct:", SQL_FIX2)

# 3. text dates
s3_bad = show("3 BAD  ORDER BY a DD/MM/YYYY text column:", """
SELECT id, d, amount, SUM(amount) OVER (ORDER BY d ROWS UNBOUNDED PRECEDING) AS rt FROM tx_txt ORDER BY d""")
SQL_FIX3 = """
SELECT id, d, amount,
       SUM(amount) OVER (ORDER BY substr(d,7,4) || '-' || substr(d,4,2) || '-' || substr(d,1,2), id
                         ROWS UNBOUNDED PRECEDING) AS rt
FROM tx_txt ORDER BY substr(d,7,4) || '-' || substr(d,4,2) || '-' || substr(d,1,2), id"""
s3_fix = show("3 FIX  rebuild an ISO key (or store real dates):", SQL_FIX3)

# 4. join fan-out
s4_bad = show("4 BAD  join to tags before the window (id 2 has two tags):", """
SELECT t.id, t.amount, SUM(t.amount) OVER (ORDER BY t.d, t.id ROWS UNBOUNDED PRECEDING) AS rt
FROM tx t LEFT JOIN tags g ON g.id = t.id WHERE t.acct = 'A' ORDER BY t.d, t.id""")
SQL_FIX4 = """
SELECT t.id, t.amount, SUM(t.amount) OVER (ORDER BY t.d, t.id ROWS UNBOUNDED PRECEDING) AS rt,
       (SELECT COUNT(*) FROM tags g WHERE g.id = t.id) AS n_tags
FROM tx t WHERE t.acct = 'A' ORDER BY t.d, t.id"""
s4_fix = show("4 FIX  window over tx alone, attach tag info after (or aggregate tags first):", SQL_FIX4)

# 5. NULLs
s5 = show("5 NULL amounts: SUM skips them; leading NULLs give NULL, later NULL rows repeat the total:", """
SELECT id, d, amount, SUM(amount) OVER (ORDER BY d, id ROWS UNBOUNDED PRECEDING) AS rt_null,
       SUM(COALESCE(amount, 0)) OVER (ORDER BY d, id ROWS UNBOUNDED PRECEDING) AS rt_zero FROM tx_null ORDER BY d, id""")

# pandas counterparts
tx = pd.read_sql_query("SELECT * FROM tx ORDER BY id", con)
# pd:main
a = tx[tx["acct"] == "A"].sort_values(["d", "id"])
fix1 = a["amount"].cumsum()                                              # suspect 1: row-based, ties never merge
peer = a["amount"].cumsum().groupby(a["d"]).transform("max")             # what the default RANGE frame did
fix2 = tx.sort_values(["acct", "d", "id"]).groupby("acct")["amount"].cumsum()   # suspect 2
bad2 = tx.sort_values(["d", "id"])["amount"].cumsum()
tt = pd.read_sql_query("SELECT * FROM tx_txt", con)
bad3 = tt.sort_values("d")["amount"].cumsum()                            # suspect 3: string sort
fix3 = tt.assign(k=pd.to_datetime(tt["d"], format="%d/%m/%Y")).sort_values(["k", "id"])["amount"].cumsum()
fan = tx[tx["acct"] == "A"].merge(pd.read_sql_query("SELECT * FROM tags", con), on="id", how="left")
bad4 = fan.sort_values(["d", "id"])["amount"].cumsum()                   # suspect 4: merge fan-out
nul = pd.read_sql_query("SELECT * FROM tx_null ORDER BY d, id", con)
nul_cum = nul["amount"].cumsum()                                         # suspect 5
# pd:end
assert fix1.tolist() == s1_fix["rt"].tolist() and peer.tolist() == s1_bad["rt"].tolist()
assert fix2.tolist() == s2_fix["rt"].tolist() and bad2.tolist() == s2_bad["rt"].tolist()
assert bad3.tolist() == s3_bad["rt"].tolist() and fix3.tolist() == s3_fix["rt"].tolist()
assert bad4.tolist() == s4_bad["rt"].tolist()
print("pandas suspect 1 default-frame lookalike:", peer.tolist(), "| row-based cumsum:", fix1.tolist())
print("pandas suspect 3 string sort:", bad3.tolist(), "| date sort:", fix3.tolist())
print("pandas suspect 4 after merge:", bad4.tolist(), "rows:", len(fan), "vs", int((tx.acct == "A").sum()))
print("pandas suspect 5 float cumsum:", nul_cum.tolist(), " vs SQL rt_null:", s5["rt_null"].tolist())
n_int = pd.Series([None, 30, None, 20], dtype="Int64")
print("Int64 cumsum skipna=True :", n_int.cumsum().tolist())
print("Int64 cumsum skipna=False:", n_int.cumsum(skipna=False).tolist())

# proof: fixed running totals tie back to SUM(amount) per group
proof_sql = """
WITH rpt AS (SELECT id, acct, d, amount,
       SUM(amount) OVER (PARTITION BY acct ORDER BY d, id ROWS UNBOUNDED PRECEDING) AS rt FROM tx),
last AS (SELECT acct, rt AS last_rt FROM rpt r
         WHERE id = (SELECT id FROM rpt r2 WHERE r2.acct = r.acct ORDER BY d DESC, id DESC LIMIT 1)),
tot AS (SELECT acct, SUM(amount) AS total, COUNT(*) AS n FROM tx GROUP BY acct)
SELECT t.acct, t.n, (SELECT COUNT(*) FROM rpt WHERE rpt.acct = t.acct) AS report_rows,
       t.total, l.last_rt, CASE WHEN t.total = l.last_rt THEN 'ok' ELSE 'MISMATCH' END AS tie_out
FROM tot t JOIN last l USING (acct) ORDER BY t.acct"""
proof = show("PROOF fixed report: last running total vs SUM(amount) and row count per acct:", proof_sql)
bad_proof = proof_sql.replace("PARTITION BY acct ORDER BY d, id ROWS UNBOUNDED PRECEDING", "ORDER BY d, id ROWS UNBOUNDED PRECEDING")
show("PROOF on the report missing PARTITION BY (it must fail):", bad_proof)
fixed = tx.sort_values(["acct", "d", "id"]).assign(rt=lambda x: x.groupby("acct")["amount"].cumsum())
lastp = fixed.groupby("acct")["rt"].last()
assert (lastp == tx.groupby("acct")["amount"].sum()).all()
assert (fixed["rt"].groupby(fixed["acct"]).diff().fillna(fixed["rt"]) == fixed["amount"]).all()
assert (proof["tie_out"] == "ok").all() and proof["n"].tolist() == proof["report_rows"].tolist()
print("pandas last rt per acct:", lastp.to_dict(), "| SUM:", tx.groupby("acct")["amount"].sum().to_dict())
print("asserts passed: each fixed query == pandas cumsum, each bad query == its pandas lookalike, tie-out holds")
```

**Output (my run):**
```text
1 BAD  default frame (RANGE through peers), rows 2 and 3 share a date:
 id          d  amount  rt
  1 2024-03-01     100 100
  2 2024-03-02      50 175
  3 2024-03-02      25 175
  4 2024-03-03      10 185

1 FIX  ORDER BY d, id with ROWS:
 id          d  amount  rt
  1 2024-03-01     100 100
  2 2024-03-02      50 150
  3 2024-03-02      25 175
  4 2024-03-03      10 185

2 BAD  no PARTITION BY (accounts bleed into each other):
 id acct  amount  rt
  1    A     100 100
  5    B     200 300
  2    A      50 350
  3    A      25 375
  4    A      10 385
  6    B     -40 345

2 FIX  PARTITION BY acct:
 id acct  amount  rt
  1    A     100 100
  2    A      50 150
  3    A      25 175
  4    A      10 185
  5    B     200 200
  6    B     -40 160

3 BAD  ORDER BY a DD/MM/YYYY text column:
 id          d  amount  rt
  3 02/04/2024      30  30
  1 09/03/2024      10  40
  2 10/03/2024      20  60

3 FIX  rebuild an ISO key (or store real dates):
 id          d  amount  rt
  1 09/03/2024      10  10
  2 10/03/2024      20  30
  3 02/04/2024      30  60

4 BAD  join to tags before the window (id 2 has two tags):
 id  amount  rt
  1     100 100
  2      50 150
  2      50 200
  3      25 225
  4      10 235

4 FIX  window over tx alone, attach tag info after (or aggregate tags first):
 id  amount  rt  n_tags
  1     100 100       0
  2      50 150       2
  3      25 175       0
  4      10 185       1

5 NULL amounts: SUM skips them; leading NULLs give NULL, later NULL rows repeat the total:
 id          d  amount  rt_null  rt_zero
  1 2024-03-01     NaN      NaN        0
  2 2024-03-02    30.0     30.0       30
  3 2024-03-03     NaN     30.0       30
  4 2024-03-04    20.0     50.0       50

pandas suspect 1 default-frame lookalike: [100, 175, 175, 185] | row-based cumsum: [100, 150, 175, 185]
pandas suspect 3 string sort: [30, 40, 60] | date sort: [10, 30, 60]
pandas suspect 4 after merge: [100, 150, 200, 225, 235] rows: 5 vs 4
pandas suspect 5 float cumsum: [nan, 30.0, nan, 50.0]  vs SQL rt_null: [nan, 30.0, 30.0, 50.0]
Int64 cumsum skipna=True : [<NA>, 30, <NA>, 50]
Int64 cumsum skipna=False: [<NA>, <NA>, <NA>, <NA>]
PROOF fixed report: last running total vs SUM(amount) and row count per acct:
acct  n  report_rows  total  last_rt tie_out
   A  4            4    185      185      ok
   B  2            2    160      160      ok

PROOF on the report missing PARTITION BY (it must fail):
acct  n  report_rows  total  last_rt  tie_out
   A  4            4    185      385 MISMATCH
   B  2            2    160      345 MISMATCH

pandas last rt per acct: {'A': 185, 'B': 160} | SUM: {'A': 185, 'B': 160}
asserts passed: each fixed query == pandas cumsum, each bad query == its pandas lookalike, tie-out holds
```

**Edge cases:**
- Suspect 1 is the most common because it looks right whenever dates are unique. With ties, the default frame gives peers the same total; fix with a unique tie-breaker and `ROWS`.
- Suspect 2: no `PARTITION BY` means one big partition; I check by counting groups in the output.
- Suspect 3: dates stored as DD/MM/YYYY text sort by day first. In SQLite I rebuilt an ISO key with `substr`; the clean fix is to store real ISO dates. `ORDER BY` on a non-padded or non-ISO string is the same trap in pandas (`sort_values` on strings).
- Suspect 4: any one-to-many join before the window duplicates amounts; the cure is to window first and join later (or aggregate the many side to one row per key). Row counts expose it.
- Suspect 5: `SUM` skips NULL. A leading NULL gives NULL, not 0, and later NULL rows repeat the total. pandas float `cumsum` gives NaN on the NULL row but continues the sum afterwards (the next rows showed 30.0 then NaN then 50.0, so the NaN rows differ from SQL's repeated 30). pandas nullable `Int64` `cumsum()` printed `[<NA>, 30, <NA>, 50]` with the default `skipna=True`, and with `skipna=False` every value after the first NA became NA. `COALESCE(amount, 0)` is a business decision, not a free fix.
- Not in the five but worth a look: a text-typed amount column (adding strings) and a `WHERE` that filters rows before the window (the window then sums only the survivors).

**Then explain:**
Order I would check, and why: cheapest and most common first.
| # | Suspect | Quick test | SQL symptom (my run) | pandas counterpart |
|---|---|---|---|---|
| 1 | Duplicate dates and default `RANGE` | `ORDER BY d` only? Same totals on two rows | 100, 175, 175, 185 | `cumsum` is row-based, so no issue; the default-frame look-alike is cumsum then group max |
| 2 | Missing `PARTITION BY` | totals do not restart per group | B starts at 300 (continues from A) | `df["amount"].cumsum()` without `groupby` |
| 3 | `ORDER BY` on text | sort the column alone and read it | 30, 40, 60 instead of 10, 30, 60 | `sort_values` on a string column; `to_datetime(format=...)` fixes it |
| 4 | Join fan-out before the window | compare row counts before and after the join | 235 at the end, 5 rows instead of 4 | `merge` with a one-to-many table, then `cumsum` |
| 5 | NULL in the summed column | `COUNT(*)` vs `COUNT(amount)` | NULL first, then repeats | NaN: float `cumsum` and `Int64` `cumsum` as noted in the edge cases |
- Proof of the fix, three tie-outs: (a) the last running total per group equals `SUM(amount)` per group; (b) the report has the same number of rows as the source (catches fan-out and filters); (c) the difference between consecutive running totals equals each row's amount (pandas check in the code). The check must also fail on the broken query: on the report without `PARTITION BY` it printed MISMATCH for both accounts.
- Habit: write the check as a query that returns zero rows when everything is right, and run it after every change.

**Follow-ups:**
- *The totals are right but the order looks odd?* Final `ORDER BY` is separate from the window's `ORDER BY`; set both.
- *Off by exactly one row's amount?* Check `ROWS` against `RANGE`, and `1 PRECEDING` frames.
- *Float sums off by a cent?* Use integers (cents) or `DECIMAL` where the engine has it; not run here.

**Common mistakes:**
- Fixing the symptom (subtracting the difference) instead of the cause.
- Checking only the last row and not the row count.
- Trusting a report because it matches on unique-date test data.
- Replacing NULL by 0 without asking what NULL means.
