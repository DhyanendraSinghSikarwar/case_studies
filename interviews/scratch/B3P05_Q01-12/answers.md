### Q1 ⭐⭐⭐ 🟢 Running total basics: daily_sales(sale_date, amount) with one row per day. Return each day with its running (cumulative) total using SUM(amount) OVER (ORDER BY sale_date), explain what the window does row by row, and show the pandas equivalent with cumsum(). Also show what happens to the same query without ORDER BY inside OVER (every row gets the grand total) and why.
**Asked at:** StrataScratch blog 'Top five SQL window functions for data science interviews' (month-over-month change with LEAD/LAG, cumulative cost with SUM, 10-day moving average, first visit with ROW_NUMBER), a guide and not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** `SUM(amount) OVER (ORDER BY sale_date)` adds up every row from the first day to the current one, so each row carries a cumulative total; take away the ORDER BY and there is no "so far", the frame is the whole partition and every row shows the grand total. In pandas it is `sort_values` then `cumsum()`.

**Schema and sample data:** five days, inserted out of date order on purpose (so the pandas sort matters).
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-03',30),('2024-01-01',10),('2024-01-05',50),
  ('2024-01-02',20),('2024-01-04',40);
```

**SQL answer:** `SQL_MAIN`, and `SQL_NOORDER` for the no-ORDER-BY case (Code block).
```sql
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM daily_sales
ORDER BY sale_date
```
```sql
SELECT sale_date, amount,
       SUM(amount) OVER () AS grand_total
FROM daily_sales
ORDER BY sale_date
```

**pandas answer:**
```py
pd_df = sales.sort_values("sale_date").reset_index(drop=True)
pd_df["running_total"] = pd_df["amount"].cumsum()
```

**Example:** walk the rows in date order.
- 01-01: nothing before it, so 10. 01-02: 10 + 20 = 30. 01-03: 30 + 30 = 60. 01-04: 60 + 40 = 100. 01-05: 100 + 50 = 150.
- Row by row the engine does the same thing: for the current row, add up the rows from the start of the partition up to it. The last running total (150) equals the plain `SUM(amount)`.
- `SUM(amount) OVER ()` has no ORDER BY, so there is no ordering to define "so far". The frame is the whole partition and all five rows show 150.
- The pandas frame comes back in insertion order, so a bare `cumsum()` on it gives `[30, 40, 90, 110, 150]`. That is a running total of the wrong order. Sort first.

**Code:** run with `python3 -I`.
```python
# Q1: running total with SUM() OVER (ORDER BY ...)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-03',30),('2024-01-01',10),('2024-01-05',50),
  ('2024-01-02',20),('2024-01-04',40);
"""
SQL_MAIN = """
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date) AS running_total
FROM daily_sales
ORDER BY sale_date
"""
SQL_NOORDER = """
SELECT sale_date, amount,
       SUM(amount) OVER () AS grand_total
FROM daily_sales
ORDER BY sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
no_order = pd.read_sql_query(SQL_NOORDER, con)
print(sql_df.to_string(index=False))
print("\nOVER () with no ORDER BY:")
print(no_order.to_string(index=False))

sales = pd.read_sql_query("SELECT * FROM daily_sales", con)   # rows come back in insertion order
# pd:main
pd_df = sales.sort_values("sale_date").reset_index(drop=True)
pd_df["running_total"] = pd_df["amount"].cumsum()
# pd:end
# compared after sorting by sale_date
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\npandas cumsum WITHOUT sorting first (rows in insertion order):",
      sales["amount"].cumsum().tolist())
print("pandas cumsum after sort_values:", pd_df["running_total"].tolist())
grand = sales["amount"].sum()
assert (no_order["grand_total"] == grand).all()
print("grand total from pandas sum():", int(grand))
print("asserts passed: SQL running total == pandas sort_values + cumsum")
```

**Output (my run):**
```text
 sale_date  amount  running_total
2024-01-01      10             10
2024-01-02      20             30
2024-01-03      30             60
2024-01-04      40            100
2024-01-05      50            150

OVER () with no ORDER BY:
 sale_date  amount  grand_total
2024-01-01      10          150
2024-01-02      20          150
2024-01-03      30          150
2024-01-04      40          150
2024-01-05      50          150

pandas cumsum WITHOUT sorting first (rows in insertion order): [30, 40, 90, 110, 150]
pandas cumsum after sort_values: [10, 30, 60, 100, 150]
grand total from pandas sum(): 150
asserts passed: SQL running total == pandas sort_values + cumsum
```

**Edge cases:**
- Duplicate dates: with two rows on one date the default frame gives both the same total (Q6). Here `sale_date` is the primary key, so each date appears once; I did not need a tie-breaker.
- NULL amount: `SUM` skips it, the total carries on; `cumsum()` in pandas leaves NaN at that position and continues the sum (Q18). Not in this sample.
- Empty table: both return no rows.
- With ISO text dates (`YYYY-MM-DD`) text order equals date order, so ordering by the string is safe. A format like `DD/MM/YYYY` sorts wrongly (Q46).

**Then explain:**
- Why the default frame is "start to current row": when a window has an ORDER BY and no frame clause, the standard default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`. That is what makes `SUM` cumulative. `SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` is the explicit spelling.
- Without ORDER BY the frame is the whole partition (the PostgreSQL docs say so; SQLite gave 150 on every row in my run). So the same function is a running total or a grand total depending on one clause.
- `OVER ()` does not collapse rows like `GROUP BY` does: you keep the daily rows and add the total beside them.
- pandas has no ORDER BY inside the operation; it works in row order, so sort explicitly. `cumsum()` on a plain Series is the same idea as the ROWS frame.

**Follow-ups:**
- *Running total as a percent of the grand total?* Divide by `SUM(amount) OVER ()` (Q15).
- *Per customer, restarting?* Add `PARTITION BY` (Q2).
- *Other engines?* Same syntax in PostgreSQL, MySQL 8, BigQuery and Snowflake (not executed here).

**Common mistakes:**
- Forgetting ORDER BY inside `OVER` and getting the grand total on every row.
- Putting the ORDER BY only at the end of the query: it sorts the output, it does not change what the window sums.
- In pandas, calling `cumsum()` on unsorted data.

### Q2 ⭐⭐⭐ 🟢 Running total per group: transactions(txn_id, user_id, txn_date, amount). Return each transaction with the running total of that user's spend, restarting for every user, using SUM() OVER (PARTITION BY user_id ORDER BY txn_date, txn_id). Explain PARTITION BY versus ORDER BY inside OVER, why the txn_id tie-breaker is there, and give the pandas groupby('user_id')['amount'].cumsum() version after sort_values.
**Asked at:** codemia.io practice page 'running total partitioned by user_id' (the page itself states a Microsoft data scientist phone screen; not independently verified, treat as site-reported); analyst and data scientist screens
**Say this first (1 line):** `PARTITION BY user_id` restarts the running total for every user, `ORDER BY txn_date, txn_id` sets the order of the add-up inside each user, and the `txn_id` tie-breaker makes same-day transactions add one at a time instead of sharing a total.

**Schema and sample data:** seven transactions, three users. User 101 has two transactions on 2024-01-02 (ids 3 and 4), user 102 has a negative amount (a refund).
```sql
CREATE TABLE transactions(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_date TEXT, amount INTEGER);
INSERT INTO transactions VALUES (1,101,'2024-01-01',50),(2,102,'2024-01-01',200),
  (3,101,'2024-01-02',20),(4,101,'2024-01-02',30),(5,102,'2024-01-03',-50),
  (6,101,'2024-01-04',10),(7,103,'2024-01-02',5);
```

**SQL answer:** `SQL_MAIN`; `SQL_NOTIE` is the same query without `txn_id` in the ORDER BY (Code block).
```sql
SELECT txn_id, user_id, txn_date, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date, txn_id) AS running_spend
FROM transactions
ORDER BY user_id, txn_date, txn_id
```
```sql
SELECT txn_id, user_id, txn_date, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date) AS running_spend
FROM transactions
ORDER BY user_id, txn_date, txn_id
```

**pandas answer:**
```py
pd_df = txn.sort_values(["user_id", "txn_date", "txn_id"]).reset_index(drop=True)
pd_df["running_spend"] = pd_df.groupby("user_id")["amount"].cumsum()
```

**Example:**
- User 101, in (date, id) order: 50, then 50 + 20 = 70, then 70 + 30 = 100, then 100 + 10 = 110.
- User 102: 200, then 200 - 50 = 150. User 103: one row, 5.
- The partition resets: user 102's first row is 200, not 110 + 200.
- Without `txn_id`, ids 3 and 4 are peers (same date). The default frame includes all peers, so both rows show 100 and the 70 disappears.

**Code:** run with `python3 -I`.
```python
# Q2: running total per user, restart for every user
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE transactions(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_date TEXT, amount INTEGER);
INSERT INTO transactions VALUES (1,101,'2024-01-01',50),(2,102,'2024-01-01',200),
  (3,101,'2024-01-02',20),(4,101,'2024-01-02',30),(5,102,'2024-01-03',-50),
  (6,101,'2024-01-04',10),(7,103,'2024-01-02',5);
"""
SQL_MAIN = """
SELECT txn_id, user_id, txn_date, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date, txn_id) AS running_spend
FROM transactions
ORDER BY user_id, txn_date, txn_id
"""
SQL_NOTIE = """
SELECT txn_id, user_id, txn_date, amount,
       SUM(amount) OVER (PARTITION BY user_id ORDER BY txn_date) AS running_spend
FROM transactions
ORDER BY user_id, txn_date, txn_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
notie = pd.read_sql_query(SQL_NOTIE, con)
print(sql_df.to_string(index=False))

txn = pd.read_sql_query("SELECT * FROM transactions", con)
# pd:main
pd_df = txn.sort_values(["user_id", "txn_date", "txn_id"]).reset_index(drop=True)
pd_df["running_spend"] = pd_df.groupby("user_id")["amount"].cumsum()
# pd:end
# compared in order user_id, txn_date, txn_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nWithout txn_id in ORDER BY (default RANGE frame, peers share a total):")
print(notie.to_string(index=False))
print("same as the tie-broken query?", notie["running_spend"].tolist() == sql_df["running_spend"].tolist())
print("same as pandas row-by-row cumsum?", notie["running_spend"].tolist() == pd_df["running_spend"].tolist())
print("final total per user, SQL:", dict(con.execute("SELECT user_id, SUM(amount) FROM transactions GROUP BY user_id ORDER BY user_id")))
print("final total per user, pandas:", pd_df.groupby("user_id")["amount"].sum().to_dict())
print("asserts passed: SQL partitioned running total == pandas groupby cumsum")
```

**Output (my run):**
```text
 txn_id  user_id   txn_date  amount  running_spend
      1      101 2024-01-01      50             50
      3      101 2024-01-02      20             70
      4      101 2024-01-02      30            100
      6      101 2024-01-04      10            110
      2      102 2024-01-01     200            200
      5      102 2024-01-03     -50            150
      7      103 2024-01-02       5              5

Without txn_id in ORDER BY (default RANGE frame, peers share a total):
 txn_id  user_id   txn_date  amount  running_spend
      1      101 2024-01-01      50             50
      3      101 2024-01-02      20            100
      4      101 2024-01-02      30            100
      6      101 2024-01-04      10            110
      2      102 2024-01-01     200            200
      5      102 2024-01-03     -50            150
      7      103 2024-01-02       5              5
same as the tie-broken query? False
same as pandas row-by-row cumsum? False
final total per user, SQL: {101: 110, 102: 150, 103: 5}
final total per user, pandas: {101: 110, 102: 150, 103: 5}
asserts passed: SQL partitioned running total == pandas groupby cumsum
```

**Edge cases:**
- Ties: the printed output shows that without the tie-breaker the two 2024-01-02 rows both get 100, which no longer matches a row-by-row `cumsum`. With a tie-breaker the result is deterministic. The tie-breaker must be unique inside the partition; `txn_id` is the primary key.
- Which order is "right" for same-day rows is a business question; I assumed `txn_id` follows posting order. If it does not, use a timestamp or sequence column.
- NULL `amount`: skipped by `SUM`, running total continues.
- A user with no rows does not appear at all; a user with one row gets that amount.

**Then explain:**
- `PARTITION BY` splits the rows into independent groups; the window is computed inside each group and rows are not collapsed. `ORDER BY` inside `OVER` orders rows inside the partition and turns on the "start to current row" frame. Different jobs: one chooses the group, the other the sequence.
- The outer `ORDER BY` only sorts the final output. I repeated the same columns there so the printed rows are in a stable order.
- pandas: `sort_values` supplies the ORDER BY, `groupby("user_id")` supplies PARTITION BY, `cumsum()` is the running sum inside each group. `cumsum` works row by row, so it matches the ROWS-style result, not the peers-sharing default.

**Follow-ups:**
- *Running count per user?* `COUNT(*) OVER (PARTITION BY user_id ORDER BY txn_date, txn_id)`, in pandas `groupby("user_id").cumcount() + 1`.
- *Last total per user only?* The `GROUP BY` sum, which my code printed for both sides.
- *Why not a self-join?* It re-reads rows per row and is quadratic (Q41).

**Common mistakes:**
- Using `ORDER BY` without `PARTITION BY` and getting one running total across all users.
- No unique tie-breaker, so same-day rows share a total or the order flips between runs.
- In pandas, `groupby().cumsum()` on unsorted data, or `cumsum()` without the groupby.

### Q3 ⭐⭐⭐ 🟢 LAG and LEAD with offset and default: stock_prices(ticker, trade_date, close_price). For every row return the previous close, the next close, the close two rows back using LAG(close_price, 2) and a default so the first rows show 0 instead of NULL (LAG(close_price, 1, 0)). Explain offset, default, NULL at partition edges, why you need PARTITION BY ticker, and give pandas groupby().shift(periods, fill_value) and shift(-1) as LEAD.
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `LAG(col, n, default)` reads the value n rows before in the window order and `LEAD` reads n rows after; where no such row exists it returns NULL, or the default if you gave one; add `PARTITION BY ticker` so one ticker never reads another's prices; pandas does the same with `groupby("ticker")["close_price"].shift(n)`, negative n for LEAD.

**Schema and sample data:** three tickers. AAA has four days, BBB has three with a NULL close in the middle, CCC has a single row.
```sql
CREATE TABLE stock_prices(ticker TEXT, trade_date TEXT, close_price INTEGER, PRIMARY KEY (ticker, trade_date));
INSERT INTO stock_prices VALUES ('AAA','2024-01-01',100),('AAA','2024-01-02',102),('AAA','2024-01-03',101),
  ('AAA','2024-01-04',105),('BBB','2024-01-01',50),('BBB','2024-01-02',NULL),('BBB','2024-01-03',52),
  ('CCC','2024-01-01',9);
```

**SQL answer:** `SQL_MAIN` with a named window; `SQL_NOPART` shows the leak without PARTITION BY (Code block).
```sql
SELECT ticker, trade_date, close_price,
       LAG(close_price)       OVER w AS prev_close,
       LEAD(close_price)      OVER w AS next_close,
       LAG(close_price, 2)    OVER w AS close_2_back,
       LAG(close_price, 1, 0) OVER w AS prev_or_zero
FROM stock_prices
WINDOW w AS (PARTITION BY ticker ORDER BY trade_date)
ORDER BY ticker, trade_date
```
```sql
SELECT ticker, trade_date, LAG(close_price) OVER (ORDER BY ticker, trade_date) AS prev_close
FROM stock_prices
ORDER BY ticker, trade_date
```

**pandas answer:**
```py
px = px.sort_values(["ticker", "trade_date"]).reset_index(drop=True)
g = px.groupby("ticker")["close_price"]
px["prev_close"] = g.shift(1)
px["next_close"] = g.shift(-1)
px["close_2_back"] = g.shift(2)
px["prev_or_zero"] = g.shift(1, fill_value=0)
```

**Example:**
- AAA 2024-01-03 (close 101): previous 102, next 105, two back 100.
- AAA 2024-01-01: nothing before it, so previous and two-back are NULL, and `LAG(close_price, 1, 0)` shows 0.
- AAA 2024-01-04: nothing after it, so next is NULL (there is no default argument on my LEAD).
- CCC has one row: all of previous, next and two-back are NULL, the default column shows 0.
- BBB 2024-01-03 (close 52): the previous row exists but its value is NULL, so previous is NULL and `prev_or_zero` is also NULL, not 0. The default replaces a missing row, not a NULL value. pandas `fill_value` behaves the same way (printed row BBB 01-03).

**Code:** run with `python3 -I`.
```python
# Q3: LAG and LEAD with offset and default
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE stock_prices(ticker TEXT, trade_date TEXT, close_price INTEGER, PRIMARY KEY (ticker, trade_date));
INSERT INTO stock_prices VALUES ('AAA','2024-01-01',100),('AAA','2024-01-02',102),('AAA','2024-01-03',101),
  ('AAA','2024-01-04',105),('BBB','2024-01-01',50),('BBB','2024-01-02',NULL),('BBB','2024-01-03',52),
  ('CCC','2024-01-01',9);
"""
SQL_MAIN = """
SELECT ticker, trade_date, close_price,
       LAG(close_price)       OVER w AS prev_close,
       LEAD(close_price)      OVER w AS next_close,
       LAG(close_price, 2)    OVER w AS close_2_back,
       LAG(close_price, 1, 0) OVER w AS prev_or_zero
FROM stock_prices
WINDOW w AS (PARTITION BY ticker ORDER BY trade_date)
ORDER BY ticker, trade_date
"""
SQL_NOPART = """
SELECT ticker, trade_date, LAG(close_price) OVER (ORDER BY ticker, trade_date) AS prev_close
FROM stock_prices
ORDER BY ticker, trade_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

px = pd.read_sql_query("SELECT * FROM stock_prices", con)
# pd:main
px = px.sort_values(["ticker", "trade_date"]).reset_index(drop=True)
g = px.groupby("ticker")["close_price"]
px["prev_close"] = g.shift(1)
px["next_close"] = g.shift(-1)
px["close_2_back"] = g.shift(2)
px["prev_or_zero"] = g.shift(1, fill_value=0)
# pd:end
# compared in order ticker, trade_date (NULL and NaN are both treated as missing)
pd.testing.assert_frame_equal(sql_df, px, check_dtype=False)
print("\ndtypes after shift:", px[["prev_close", "prev_or_zero"]].dtypes.to_dict())
ints = pd.Series([1, 2, 3])
print("int Series shift(1) dtype:", ints.shift(1).dtype, "| shift(1, fill_value=0) dtype:", ints.shift(1, fill_value=0).dtype)
print("\nWithout PARTITION BY, LAG leaks across tickers:")
print(pd.read_sql_query(SQL_NOPART, con).to_string(index=False))
print("\nraw shift on the unpartitioned column (same leak in pandas):",
      px["close_price"].shift(1).tolist())
neg = [r[0] for r in con.execute("SELECT LAG(close_price, -1) OVER (PARTITION BY ticker ORDER BY trade_date) FROM stock_prices ORDER BY ticker, trade_date")]
same = neg == [None if pd.isna(v) else int(v) for v in sql_df["next_close"]]
assert same
print("SQLite LAG(close_price, -1) equals LEAD(close_price):", same)
print("asserts passed: SQL LAG/LEAD == pandas groupby shift")
```

**Output (my run):**
```text
ticker trade_date  close_price  prev_close  next_close  close_2_back  prev_or_zero
   AAA 2024-01-01        100.0         NaN       102.0           NaN           0.0
   AAA 2024-01-02        102.0       100.0       101.0           NaN         100.0
   AAA 2024-01-03        101.0       102.0       105.0         100.0         102.0
   AAA 2024-01-04        105.0       101.0         NaN         102.0         101.0
   BBB 2024-01-01         50.0         NaN         NaN           NaN           0.0
   BBB 2024-01-02          NaN        50.0        52.0           NaN          50.0
   BBB 2024-01-03         52.0         NaN         NaN          50.0           NaN
   CCC 2024-01-01          9.0         NaN         NaN           NaN           0.0

dtypes after shift: {'prev_close': dtype('float64'), 'prev_or_zero': dtype('float64')}
int Series shift(1) dtype: float64 | shift(1, fill_value=0) dtype: int64

Without PARTITION BY, LAG leaks across tickers:
ticker trade_date  prev_close
   AAA 2024-01-01         NaN
   AAA 2024-01-02       100.0
   AAA 2024-01-03       102.0
   AAA 2024-01-04       101.0
   BBB 2024-01-01       105.0
   BBB 2024-01-02        50.0
   BBB 2024-01-03         NaN
   CCC 2024-01-01        52.0

raw shift on the unpartitioned column (same leak in pandas): [nan, 100.0, 102.0, 101.0, 105.0, 50.0, nan, 52.0]
SQLite LAG(close_price, -1) equals LEAD(close_price): True
asserts passed: SQL LAG/LEAD == pandas groupby shift
```

**Edge cases:**
- Offset and default: offset is how many rows back (default 1), default is the value returned when that row does not exist (default NULL). `LAG(x, 1, 0)` hides the difference between "no previous day" and "previous price was 0"; for prices I would keep NULL.
- dtype: pandas upcasts integers to float64 when `shift` introduces NaN; passing an integer `fill_value` keeps int64 (printed). The table here is float already because BBB has a NULL.
- Duplicates in `(ticker, trade_date)`: the primary key rules them out here; with duplicates the order of the tied rows is unspecified and LAG would depend on it (add a tie-breaker, Q2).
- Missing calendar days are not rows, so "previous row" is not "previous day" (Q13, Q16).

**Then explain:**
- Without `PARTITION BY`, the first BBB row reads 105, AAA's last close (the printed second table; row CCC gets 52 from BBB). The same leak happens with an ungrouped `shift` in pandas (printed).
- LEAD is LAG with the direction flipped: `LEAD(x, n)` equals `LAG(x, -n)` in meaning; pandas uses `shift(-n)`. SQLite accepted `LAG(close_price, -1)` and returned the LEAD values (printed), but I would not rely on negative offsets in other engines (not executed); use LEAD.
- LAG and LEAD ignore the frame clause; they look by row position inside the partition order.

**Follow-ups:**
- *Day-over-day change?* `close_price - LAG(close_price)` (Q4).
- *Skip NULL prices?* SQLite has no `IGNORE NULLS`; see the forward-fill pattern (Q34). Some engines support it natively (not executed).
- *Why does the default only apply at the edges?* Because it replaces "no row", not "row with NULL".

**Common mistakes:**
- Forgetting `PARTITION BY ticker`, so the first row of each ticker reads the previous ticker.
- Reading `LAG(x, 1, 0)` zeros as real prices.
- Expecting `fill_value` to fill existing NaN values.

### Q4 ⭐⭐⭐ 🟢 Day-over-day change and percent change: daily_sales(sale_date, amount). Return each day's change from the previous day and the percent change, with the first row as NULL and a previous value of zero handled with NULLIF so there is no division by zero. Show LAG, the percent formula (current - previous) / previous * 100, and pandas diff() and pct_change(), including what pandas returns when the previous value is 0 (run it).
**Asked at:** LearnSQL revenue-growth and Craig Kerstiens month-over-month blog write-ups (LAG, percent change, gaps break LAG, divide by zero), guides and not candidate reports; analyst screens at product companies and startups
**Say this first (1 line):** Put `LAG(amount)` in a CTE, then `change = amount - prev_amount` and `pct = (amount - prev_amount) * 100.0 / NULLIF(prev_amount, 0)`; the first row has no previous so both are NULL, and NULLIF turns a zero previous value into NULL; pandas `diff()` and `pct_change()` give the same numbers, except that pandas returns `inf` for a zero base.

**Schema and sample data:** six days; day 3 has amount 0, so day 4 has a zero base.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',100),('2024-01-02',120),('2024-01-03',0),
  ('2024-01-04',50),('2024-01-05',50),('2024-01-06',80);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_NONULLIF` is a small extra query that divides by zero on purpose.
```sql
WITH d AS (
  SELECT sale_date, amount, LAG(amount) OVER (ORDER BY sale_date) AS prev_amount
  FROM daily_sales
)
SELECT sale_date, amount, prev_amount,
       amount - prev_amount AS change,
       ROUND((amount - prev_amount) * 100.0 / NULLIF(prev_amount, 0), 2) AS pct_change
FROM d
ORDER BY sale_date
```

**pandas answer:**
```py
sales["prev_amount"] = sales["amount"].shift(1)
sales["change"] = sales["amount"].diff()
sales["pct_change"] = (sales["amount"].pct_change() * 100).round(2)
```

**Example:**
- 01-02: change 120 - 100 = 20; percent 20 / 100 * 100 = 20.0.
- 01-03: 0 - 120 = -120; percent -120 / 120 * 100 = -100.0.
- 01-04: change 50 - 0 = 50; the previous is 0, so `NULLIF(0, 0)` is NULL and the percent is NULL (a jump from zero has no defined percent).
- 01-05: 0 change, 0.0 percent. 01-06: 30, 60.0. 01-01: NULL and NULL (no previous).

**Code:** run with `python3 -I`.
```python
# Q4: day-over-day change and percent change
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',100),('2024-01-02',120),('2024-01-03',0),
  ('2024-01-04',50),('2024-01-05',50),('2024-01-06',80);
"""
SQL_MAIN = """
WITH d AS (
  SELECT sale_date, amount, LAG(amount) OVER (ORDER BY sale_date) AS prev_amount
  FROM daily_sales
)
SELECT sale_date, amount, prev_amount,
       amount - prev_amount AS change,
       ROUND((amount - prev_amount) * 100.0 / NULLIF(prev_amount, 0), 2) AS pct_change
FROM d
ORDER BY sale_date
"""
SQL_NONULLIF = """
SELECT sale_date, (amount - 0) * 100.0 / (amount - amount) AS divide_by_zero FROM daily_sales LIMIT 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nSQLite without NULLIF, x / 0 gives:", con.execute(SQL_NONULLIF).fetchall())

sales = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
sales["prev_amount"] = sales["amount"].shift(1)
sales["change"] = sales["amount"].diff()
sales["pct_change"] = (sales["amount"].pct_change() * 100).round(2)
# pd:end
raw = sales["pct_change"].tolist()
print("\npandas raw pct_change * 100 (inf where the previous value is 0):", raw)
sales["pct_change"] = sales["pct_change"].replace([np.inf, -np.inf], np.nan)   # the NULLIF step
# compared in order sale_date
pd.testing.assert_frame_equal(sql_df, sales[sql_df.columns], check_dtype=False)
print("pandas after replacing inf with NaN:", sales["pct_change"].tolist())
print("diff() first value:", sales["amount"].diff().iloc[0], "| pct_change() first value:", sales["amount"].pct_change().iloc[0])
print("asserts passed: SQL LAG change and percent == pandas diff and pct_change")
```

**Output (my run):**
```text
 sale_date  amount  prev_amount  change  pct_change
2024-01-01     100          NaN     NaN         NaN
2024-01-02     120        100.0    20.0        20.0
2024-01-03       0        120.0  -120.0      -100.0
2024-01-04      50          0.0    50.0         NaN
2024-01-05      50         50.0     0.0         0.0
2024-01-06      80         50.0    30.0        60.0

SQLite without NULLIF, x / 0 gives: [('2024-01-01', None)]

pandas raw pct_change * 100 (inf where the previous value is 0): [nan, 20.0, -100.0, inf, 0.0, 60.0]
pandas after replacing inf with NaN: [nan, 20.0, -100.0, nan, 0.0, 60.0]
diff() first value: nan | pct_change() first value: nan
asserts passed: SQL LAG change and percent == pandas diff and pct_change
```

**Edge cases:**
- Zero previous value: SQLite returns NULL for `x / 0` even without NULLIF (printed), so the query would not crash here, but PostgreSQL raises a division-by-zero error (hedged, not executed) and MySQL returns NULL by default (from memory, not executed). `NULLIF` makes it portable and explicit.
- pandas: `pct_change()` returns `inf` for a non-zero value over a zero base (printed `inf` on 01-04) and NaN for 0 over 0. I replaced `inf` with NaN to match SQL's NULL; that is a choice, so say it.
- Missing days: `LAG` takes the previous row, not the previous calendar day (Q16). Here every day is present.
- NULL amount: the change is NULL for that row and for the next one (Q38).
- Sign: for a negative previous value the percent formula flips sign; divide by `ABS(prev)` if that matters.

**Then explain:**
- Percent change is a ratio, so order matters: LAG over `ORDER BY sale_date`.
- pandas `pct_change()` returns a fraction (0.2), not a percent; multiply by 100.
- In pandas 3 `pct_change` no longer forward-fills missing values by default: `fill_method` only accepts `None` (I confirmed that `fill_method="pad"` raises). Fill missing values yourself first (Q38).
- `diff()` and `pct_change()` need sorted rows, exactly like LAG needs ORDER BY.

**Follow-ups:**
- *Month-over-month?* Aggregate to months first, then the same LAG (Q16).
- *Percent points versus percent?* Difference of two percentages is percentage points, not percent.
- *What would you show for a zero base?* NULL, with a note; some reports show "n/a" or cap the value.

**Common mistakes:**
- Dividing by `prev` without NULLIF.
- Dividing by the current value, giving the wrong base.
- Reporting pandas `inf` in a dashboard.
- Using `ROUND` before the comparison and then testing equality on floats.

### Q5 ⭐⭐⭐ 🟡 Cumulative sum over an aggregate: orders(order_id, order_date, amount). Produce the running total of monthly revenue in one query, so the window is applied on top of GROUP BY (SUM(SUM(amount)) OVER (ORDER BY month)). Explain why windows are evaluated after GROUP BY, why a CTE with monthly totals gives the same answer, and give the pandas groupby then cumsum version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** In one query, `GROUP BY` runs first and the window runs on its output, so `SUM(SUM(amount)) OVER (ORDER BY month)` means "inner SUM per month, outer window running total over those monthly sums"; a CTE of monthly totals with `SUM(monthly_revenue) OVER (ORDER BY month)` gives the identical answer, and pandas is `groupby().sum()` then `cumsum()`.

**Schema and sample data:** seven orders over four months. February has one NULL amount, March has only a NULL amount.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-05',100),(2,'2024-01-20',50),(3,'2024-02-03',200),
  (4,'2024-02-14',NULL),(5,'2024-03-09',NULL),(6,'2024-04-01',70),(7,'2024-04-30',30);
```

**SQL answer:** `SQL_MAIN` is the one-query form, `SQL_CTE` the two-step form (Code block).
```sql
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(amount) AS monthly_revenue,
       SUM(SUM(amount)) OVER (ORDER BY strftime('%Y-%m', order_date)) AS running_revenue
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month
```
```sql
WITH monthly AS (
  SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS monthly_revenue
  FROM orders
  GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, monthly_revenue,
       SUM(monthly_revenue) OVER (ORDER BY month) AS running_revenue
FROM monthly
ORDER BY month
```

**pandas answer:**
```py
orders["month"] = pd.to_datetime(orders["order_date"]).dt.strftime("%Y-%m")
monthly = orders.groupby("month")["amount"].sum(min_count=1)
pd_df = monthly.rename("monthly_revenue").to_frame()
pd_df["running_revenue"] = pd_df["monthly_revenue"].fillna(0).cumsum()
pd_df = pd_df.reset_index()
```

**Example:**
- Jan: 100 + 50 = 150, running 150. Feb: 200 (the NULL is skipped), running 150 + 200 = 350.
- Mar: both rows are NULL, so `SUM(amount)` is NULL (not 0), and the running total stays 350.
- Apr: 70 + 30 = 100, running 350 + 100 = 450.

**Code:** run with `python3 -I`.
```python
# Q5: cumulative sum over an aggregate
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-05',100),(2,'2024-01-20',50),(3,'2024-02-03',200),
  (4,'2024-02-14',NULL),(5,'2024-03-09',NULL),(6,'2024-04-01',70),(7,'2024-04-30',30);
"""
SQL_MAIN = """
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(amount) AS monthly_revenue,
       SUM(SUM(amount)) OVER (ORDER BY strftime('%Y-%m', order_date)) AS running_revenue
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month
"""
SQL_CTE = """
WITH monthly AS (
  SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS monthly_revenue
  FROM orders
  GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, monthly_revenue,
       SUM(monthly_revenue) OVER (ORDER BY month) AS running_revenue
FROM monthly
ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
cte_df = pd.read_sql_query(SQL_CTE, con)
print(sql_df.to_string(index=False))
assert sql_df.equals(cte_df)
print("CTE version identical:", sql_df.equals(cte_df))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
orders["month"] = pd.to_datetime(orders["order_date"]).dt.strftime("%Y-%m")
monthly = orders.groupby("month")["amount"].sum(min_count=1)
pd_df = monthly.rename("monthly_revenue").to_frame()
pd_df["running_revenue"] = pd_df["monthly_revenue"].fillna(0).cumsum()
pd_df = pd_df.reset_index()
# pd:end
# compared in order month
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\npandas default sum() on an all-NaN month:",
      orders.groupby("month")["amount"].sum().to_dict())
print("with min_count=1:", monthly.to_dict())
print("cumsum() WITHOUT fillna keeps NaN at the all-NULL month:", monthly.cumsum().tolist())
print("asserts passed: windowed SUM(SUM()) == CTE == pandas groupby then cumsum")
```

**Output (my run):**
```text
  month  monthly_revenue  running_revenue
2024-01            150.0              150
2024-02            200.0              350
2024-03              NaN              350
2024-04            100.0              450
CTE version identical: True

pandas default sum() on an all-NaN month: {'2024-01': 150.0, '2024-02': 200.0, '2024-03': 0.0, '2024-04': 100.0}
with min_count=1: {'2024-01': 150.0, '2024-02': 200.0, '2024-03': nan, '2024-04': 100.0}
cumsum() WITHOUT fillna keeps NaN at the all-NULL month: [150.0, 350.0, nan, 450.0]
asserts passed: windowed SUM(SUM()) == CTE == pandas groupby then cumsum
```

**Edge cases:**
- All-NULL month: SQL `SUM` gives NULL; pandas `sum()` gives 0.0 by default (printed). I used `min_count=1` to get NaN like SQL. Then `cumsum()` leaves NaN at that month (printed), whereas SQL carries 350, so I used `fillna(0)` before `cumsum()` for the running column.
- A month with no orders at all is simply absent from both outputs; the running total does not show it. Build a calendar if you need every month (Q16).
- Month key: `strftime('%Y-%m', ...)` sorts correctly as text. SQLite has no `DATE_TRUNC`; PostgreSQL/Snowflake/BigQuery do (not executed).
- ORDER BY inside the window repeats the expression `strftime(...)` instead of the alias `month`; referencing an output alias inside `OVER` is not allowed in every engine (PostgreSQL rejects it, from memory, not executed), so the expression is the portable form.

**Then explain:**
- Logical order: FROM, WHERE, GROUP BY, HAVING, then window functions, then SELECT output and ORDER BY. So a window can use aggregates as input; that is why the outer `SUM` takes `SUM(amount)` as its argument. It also means you cannot use a window result in WHERE or HAVING (Part 4 lesson).
- The inner `SUM(amount)` is a normal aggregate; the outer one is a window function because of `OVER`.
- The CTE form is the one I would write in review: it is easier to read and to test the monthly totals on their own. Same result in my run.
- In pandas the two steps are explicit: `groupby("month")["amount"].sum()` collapses rows, `cumsum()` accumulates.

**Follow-ups:**
- *Running total that resets each year?* Add a partition on year (Q32).
- *Percent of the final total?* Divide by `SUM(SUM(amount)) OVER ()`.
- *Why not `SUM(amount) OVER (ORDER BY order_date)` with GROUP BY?* The raw `amount` column is not a grouped value, so the query would not mean what you want; aggregate first.

**Common mistakes:**
- Using one `SUM(amount) OVER` without the grouping step and getting daily rather than monthly rows.
- Expecting a running total of an all-NULL month to be NULL (it carries the previous total).
- In pandas, forgetting that an empty month sums to 0, and that `cumsum()` keeps the NaN.

### Q6 ⭐⭐⭐ 🟡 My running total is wrong with two orders on the same date: orders(order_id, order_date, amount) where two orders share a date. The query SUM(amount) OVER (ORDER BY order_date) gives both rows the same running total. Explain the default frame RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW and peers, reproduce the bug, and show three fixes (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, a unique tie-breaker such as order_id in ORDER BY, or aggregate to one row per date first) and say which one you prefer and when RANGE behaviour is actually what you want.
**Asked at:** guide snippets on default-frame and duplicate-date running totals (reintech, oneuptime, Brent Ozar, mssqltips; not opened), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `SUM(amount) OVER (ORDER BY order_date)` uses the default frame `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, and in RANGE mode "current row" includes all peers (rows with the same order key), so two orders on the same date both get the date's final total; fix it with a ROWS frame, a unique tie-breaker in ORDER BY, or by aggregating per date first.

**Schema and sample data:** four orders; orders 2 and 3 share 2024-01-02.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-01',100),(2,'2024-01-02',50),(3,'2024-01-02',30),(4,'2024-01-04',20);
```

**SQL answer:** the bug (`SQL_BUG`), then the fixes (Code block).
```sql
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM orders
ORDER BY order_date, order_id
```
```sql
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date, order_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
ORDER BY order_date, order_id
```
```sql
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date, order_id) AS running_total
FROM orders
ORDER BY order_date, order_id
```
```sql
WITH daily AS (
  SELECT order_date, SUM(amount) AS day_total FROM orders GROUP BY order_date
)
SELECT order_date, day_total,
       SUM(day_total) OVER (ORDER BY order_date) AS running_total
FROM daily
ORDER BY order_date
```
`SQL_ROWS_NOTIE` (ROWS frame, ORDER BY `order_date` only) is also in the Code block: it shows why a ROWS frame still needs a tie-breaker.

**pandas answer:**
```py
pd_df = orders.sort_values(["order_date", "order_id"]).reset_index(drop=True)
pd_df["running_total"] = pd_df["amount"].cumsum()                      # row by row, like ROWS
by_date = pd_df.groupby("order_date")["amount"].sum().cumsum()         # one row per date
pd_df["range_total"] = pd_df["order_date"].map(by_date)                # peers share the total, like RANGE
```

**Example:**
- Peers: rows 2 and 3 have the same `order_date`, so they are peers. For either row, the RANGE frame ends at the last peer, so it includes both: 100 + 50 + 30 = 180 on both rows. That is the "bug": order 2 cannot have 180, it only had 150 after it.
- ROWS frame (or tie-breaker): row 2 = 100 + 50 = 150, row 3 = 150 + 30 = 180. Row 4 = 200.
- Aggregate first: 01-01 = 100, 01-02 = 50 + 30 = 80, 01-04 = 20; running 100, 180, 200: one row per date, same final totals.
- The query is not wrong, it just answers a different question: "total through the end of this date".

**Code:** run with `python3 -I`.
```python
# Q6: running total wrong with two orders on the same date (default RANGE frame, peers)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'2024-01-01',100),(2,'2024-01-02',50),(3,'2024-01-02',30),(4,'2024-01-04',20);
"""
SQL_BUG = """
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date) AS running_total
FROM orders
ORDER BY order_date, order_id
"""
SQL_ROWS = """
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date, order_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
ORDER BY order_date, order_id
"""
SQL_TIEBREAK = """
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date, order_id) AS running_total
FROM orders
ORDER BY order_date, order_id
"""
SQL_ROWS_NOTIE = """
SELECT order_id, order_date, amount,
       SUM(amount) OVER (ORDER BY order_date
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
ORDER BY order_date, order_id
"""
SQL_DAILY = """
WITH daily AS (
  SELECT order_date, SUM(amount) AS day_total FROM orders GROUP BY order_date
)
SELECT order_date, day_total,
       SUM(day_total) OVER (ORDER BY order_date) AS running_total
FROM daily
ORDER BY order_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
bug = pd.read_sql_query(SQL_BUG, con)
rows = pd.read_sql_query(SQL_ROWS, con)
tie = pd.read_sql_query(SQL_TIEBREAK, con)
notie = pd.read_sql_query(SQL_ROWS_NOTIE, con)
daily = pd.read_sql_query(SQL_DAILY, con)
show = bug.rename(columns={"running_total": "bug_range"})
show["fix_rows"] = rows["running_total"]
show["fix_tiebreak"] = tie["running_total"]
show["rows_no_tiebreak"] = notie["running_total"]
print(show.to_string(index=False))
print("\nFix 3, one row per date first:")
print(daily.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
pd_df = orders.sort_values(["order_date", "order_id"]).reset_index(drop=True)
pd_df["running_total"] = pd_df["amount"].cumsum()                      # row by row, like ROWS
by_date = pd_df.groupby("order_date")["amount"].sum().cumsum()         # one row per date
pd_df["range_total"] = pd_df["order_date"].map(by_date)                # peers share the total, like RANGE
# pd:end
# compared in order order_date, order_id
assert rows["running_total"].tolist() == tie["running_total"].tolist() == pd_df["running_total"].tolist()
assert bug["running_total"].tolist() == pd_df["range_total"].tolist()
assert daily["running_total"].tolist() == by_date.tolist()
last_rows = notie.groupby("order_date")["running_total"].max().tolist()
assert last_rows == daily["running_total"].tolist()
print("\npandas cumsum (row by row):", pd_df["running_total"].tolist())
print("pandas date-level cumsum mapped back (RANGE-like):", pd_df["range_total"].tolist())
print("asserts passed: ROWS == tie-breaker == pandas cumsum; default RANGE == pandas date-level cumsum")
```

**Output (my run):**
```text
 order_id order_date  amount  bug_range  fix_rows  fix_tiebreak  rows_no_tiebreak
        1 2024-01-01     100        100       100           100               100
        2 2024-01-02      50        180       150           150               150
        3 2024-01-02      30        180       180           180               180
        4 2024-01-04      20        200       200           200               200

Fix 3, one row per date first:
order_date  day_total  running_total
2024-01-01        100            100
2024-01-02         80            180
2024-01-04         20            200

pandas cumsum (row by row): [100, 150, 180, 200]
pandas date-level cumsum mapped back (RANGE-like): [100, 180, 180, 200]
asserts passed: ROWS == tie-breaker == pandas cumsum; default RANGE == pandas date-level cumsum
```

**Edge cases:**
- The last row of each date is the same under every fix (180 on 01-02); only the in-between rows differ. The code asserts that.
- ROWS with `ORDER BY order_date` only: SQLite returned 150 then 180 in my run (insertion order), but the order of tied rows is unspecified, so another plan or engine could return 130 then 180. Tie-breaker `order_id` removes the guess.
- NULL amount: skipped by SUM. NULL dates: all NULLs are peers of each other, and sort first in SQLite.
- Which row is "first" within a date is a business rule; `order_id` assumes ids follow arrival order.

**Then explain:**
- Frame modes: ROWS counts physical rows; RANGE counts by value of the ORDER BY key and takes all peers; GROUPS counts peer groups (Q7).
- The standard default (with an ORDER BY) is RANGE, so the bug appears whenever the order key is not unique. In engines I know of the default is the same (hedged, not executed); the PostgreSQL documentation I opened states it.
- Which fix I prefer: the tie-breaker in ORDER BY, because it also makes the order of tied rows deterministic and works with the default frame, plus I spell the frame out (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`) in production code so the intent is clear. Aggregate per date when the report is a daily line, not a per-order list.
- When RANGE is what you want: "balance as of end of day" or "total through this date" reports, where two same-day rows should show the same figure; and time windows by value (Q24).
- pandas `cumsum()` is always row by row (like ROWS). To get peer-sharing behaviour map the date-level cumulative sum back to each row (code).

**Follow-ups:**
- *Why not just `ORDER BY order_id`?* If order ids are not chronological, you change the meaning; use the business time first, id second.
- *What does GROUPS do here?* `GROUPS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` also includes whole peer groups, so it matches the default on this data (Q7 runs GROUPS).
- *Does adding a tie-breaker change the final total?* No.

**Common mistakes:**
- Calling it an engine bug; it is the specified default.
- Fixing with ROWS but no tie-breaker, leaving the intermediate rows undefined.
- Using a non-unique tie-breaker.

### Q7 ⭐⭐⭐ 🟡 ROWS versus RANGE versus GROUPS frames: on a table events(event_date, amount) with duplicate dates and a gap, show SUM(amount) with ROWS BETWEEN 1 PRECEDING AND CURRENT ROW, RANGE BETWEEN 1 PRECEDING AND CURRENT ROW (numeric day numbers, since SQLite needs numeric offsets) and GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW side by side and explain peers, what CURRENT ROW means in each mode, and when each is the right tool. State that PostgreSQL has all three, and run them on SQLite 3.45.
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** All three frames slide a window, but they count differently: ROWS counts physical rows, RANGE counts by the value of the ORDER BY key (here day numbers) and includes all peers, GROUPS counts whole groups of peers (distinct dates); with duplicate dates and a gap the three give different sums.

**Schema and sample data:** seven events with duplicate dates (01-01 twice, 01-06 twice) and a gap (01-02 to 01-05). I added an `event_id` so the ROWS frame has a deterministic order.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_date TEXT, amount INTEGER);
INSERT INTO events VALUES (1,'2024-01-01',10),(2,'2024-01-01',20),(3,'2024-01-02',5),(4,'2024-01-05',7),
  (5,'2024-01-06',1),(6,'2024-01-06',2),(7,'2024-01-10',100);
```

**SQL answer:** three queries, run side by side in the Code block. RANGE needs a number to do arithmetic on, so it orders by `julianday(event_date)`.
```sql
SELECT event_id, SUM(amount) OVER (ORDER BY event_date, event_id
                                   ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS rows_1
FROM events ORDER BY event_id
```
```sql
SELECT event_id, SUM(amount) OVER (ORDER BY julianday(event_date)
                                   RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) AS range_1
FROM events ORDER BY event_id
```
```sql
SELECT event_id, SUM(amount) OVER (ORDER BY event_date
                                   GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS groups_1
FROM events ORDER BY event_id
```

**pandas answer:** there is no direct "RANGE" or "GROUPS" in `rolling`, so I emulate them (day number mask; per-date sums with a 2-row window).
```py
ev["day"] = (pd.to_datetime(ev["event_date"]) - pd.Timestamp("2024-01-01")).dt.days
ev = ev.sort_values(["event_date", "event_id"]).reset_index(drop=True)
ev["rows_1"] = ev["amount"].rolling(2, min_periods=1).sum()
ev["range_1"] = [ev.loc[(ev["day"] >= d - 1) & (ev["day"] <= d), "amount"].sum() for d in ev["day"]]
per_date = ev.groupby("event_date")["amount"].sum().rolling(2, min_periods=1).sum()
ev["groups_1"] = ev["event_date"].map(per_date)
```

**Example:** "1 PRECEDING" read three ways.
- ROWS: the previous physical row plus this one. Event 4 (01-05, 7): previous row is event 3 (5), so 12. Event 2: 10 + 20 = 30. Event 1: only itself, 10.
- RANGE (day numbers): all rows whose day number is within 1 of this one, peers included. Event 4 (01-05): day 01-04 does not exist and 01-02 is 3 days away, so only itself, 7. Event 1 and 2: both on 01-01, so 30 for both. Event 3 (01-02): 01-01 is 1 day away, so 10 + 20 + 5 = 35.
- GROUPS: the previous distinct date's rows plus the current date's rows, whatever the gap. Event 4: group before is 01-02 (5), so 5 + 7 = 12. Event 7 (01-10): group before is 01-06 (1 + 2), so 103.
- CURRENT ROW: in ROWS it is this row only (later peers are not in the frame yet); in RANGE and GROUPS it also reaches the last peer, so rows on the same date show the same value (30, 30; 10, 10).

**Code:** run with `python3 -I`.
```python
# Q7: ROWS vs RANGE vs GROUPS frames side by side
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, event_date TEXT, amount INTEGER);
INSERT INTO events VALUES (1,'2024-01-01',10),(2,'2024-01-01',20),(3,'2024-01-02',5),(4,'2024-01-05',7),
  (5,'2024-01-06',1),(6,'2024-01-06',2),(7,'2024-01-10',100);
"""
SQL_ROWS = """
SELECT event_id, SUM(amount) OVER (ORDER BY event_date, event_id
                                   ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS rows_1
FROM events ORDER BY event_id
"""
SQL_RANGE = """
SELECT event_id, SUM(amount) OVER (ORDER BY julianday(event_date)
                                   RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) AS range_1
FROM events ORDER BY event_id
"""
SQL_GROUPS = """
SELECT event_id, SUM(amount) OVER (ORDER BY event_date
                                   GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS groups_1
FROM events ORDER BY event_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ev = pd.read_sql_query("SELECT * FROM events ORDER BY event_id", con)
sql_df = ev.copy()
for sql, col in [(SQL_ROWS, "rows_1"), (SQL_RANGE, "range_1"), (SQL_GROUPS, "groups_1")]:
    sql_df[col] = pd.read_sql_query(sql, con)[col]
print(sql_df.to_string(index=False))

# pd:main
ev["day"] = (pd.to_datetime(ev["event_date"]) - pd.Timestamp("2024-01-01")).dt.days
ev = ev.sort_values(["event_date", "event_id"]).reset_index(drop=True)
ev["rows_1"] = ev["amount"].rolling(2, min_periods=1).sum()
ev["range_1"] = [ev.loc[(ev["day"] >= d - 1) & (ev["day"] <= d), "amount"].sum() for d in ev["day"]]
per_date = ev.groupby("event_date")["amount"].sum().rolling(2, min_periods=1).sum()
ev["groups_1"] = ev["event_date"].map(per_date)
# pd:end
# compared in order event_id
pd_df = ev.sort_values("event_id").reset_index(drop=True)
pd.testing.assert_frame_equal(sql_df[["event_id", "rows_1", "range_1", "groups_1"]],
                              pd_df[["event_id", "rows_1", "range_1", "groups_1"]], check_dtype=False)

ev["rolling_2D"] = ev.assign(d=pd.to_datetime(ev["event_date"])).rolling("2D", on="d")["amount"].sum()
print("\npandas rolling('2D', on=date) in row order:", ev["rolling_2D"].tolist())
print("SQL RANGE in the same row order:          ", ev["range_1"].tolist())
print("asserts passed: SQL ROWS/RANGE/GROUPS == pandas emulations")
```

**Output (my run):**
```text
 event_id event_date  amount  rows_1  range_1  groups_1
        1 2024-01-01      10      10       30        30
        2 2024-01-01      20      30       30        30
        3 2024-01-02       5      25       35        35
        4 2024-01-05       7      12        7        12
        5 2024-01-06       1       8       10        10
        6 2024-01-06       2       3       10        10
        7 2024-01-10     100     102      100       103

pandas rolling('2D', on=date) in row order: [10.0, 30.0, 35.0, 7.0, 8.0, 10.0, 100.0]
SQL RANGE in the same row order:           [30, 30, 35, 7, 10, 10, 100]
asserts passed: SQL ROWS/RANGE/GROUPS == pandas emulations
```

**Edge cases:**
- Duplicates: only ROWS depends on the tie order (hence `event_id`); RANGE and GROUPS give peers the same value.
- Gaps: RANGE respects them (event 4 sees nothing from 01-02), GROUPS ignores them (event 4 still sees 01-02), ROWS ignores them too.
- RANGE with a numeric offset needs exactly one numeric ORDER BY expression. Ordering by the text date with an offset ran without an error on 3.45.1 but gave wrong sums (Q24 shows it).
- pandas `rolling('2D', on=date)` is close to RANGE but not equal on duplicates: in row order it gave 10, 30, 35, 7, 8, 10, 100 against SQL's 30, 30, 35, 7, 10, 10, 100 (printed), because pandas windows only see rows that come earlier in the frame order, not later peers.

**Then explain:**
- Peers are rows that tie on the ORDER BY key. ROWS ignores peer-ness, RANGE and GROUPS are built on it.
- When to use which: ROWS for "last N observations" with one row per time step (moving average), RANGE for "last N days by value" when rows can repeat or be missing, GROUPS for "last N distinct dates/periods" when you want whole days but ignore gaps.
- PostgreSQL has all three (GROUPS and EXCLUDE since version 11, from memory, not executed); RANGE with a date column takes an `INTERVAL` there (not executed). MySQL 8 has ROWS and RANGE only, from memory (not executed). SQLite supports GROUPS and EXCLUDE since 3.28 per the notes; I ran them on 3.45.1.

**Follow-ups:**
- *RANGE with an unbounded side?* `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` is the default frame and does not need a numeric key.
- *What if the key is text?* A numeric offset on text is meaningless; convert to a number first.
- *EXCLUDE?* Removes the current row, its peers, or ties from the frame (Q36).

**Common mistakes:**
- Using ROWS when "within the last 7 days" was meant, so a gap silently widens the time span.
- Using RANGE with a text date.
- Not saying how duplicate dates should count.

### Q8 ⭐⭐⭐ 🟡 3-day and 7-day moving average: daily_sales(sale_date, amount), one row per day. Compute the 3-day moving average with AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), explain the incomplete window at the start (AVG over fewer rows), show how to return NULL for the first two days using COUNT(*) OVER the same frame, and give the pandas rolling(3).mean() with and without min_periods=1, noting rolling's default min_periods equals the window size.
**Asked at:** StrataScratch blog 'Top five SQL window functions for data science interviews' (month-over-month change with LEAD/LAG, cumulative cost with SUM, 10-day moving average, first visit with ROW_NUMBER), a guide and not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** `AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` averages the current row and the two before it, so the first two days average fewer rows; wrap it in `CASE WHEN COUNT(*) OVER (same frame) = 3` to return NULL until the window is full; pandas `rolling(3).mean()` already returns NaN there because `min_periods` defaults to the window size.

**Schema and sample data:** eight days, one row per day.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',12),('2024-01-02',18),('2024-01-03',30),('2024-01-04',24),
  ('2024-01-05',36),('2024-01-06',60),('2024-01-07',42),('2024-01-08',48);
```

**SQL answer:** one query, 3-day partial, 3-day strict and 7-day strict averages (Code block). The two frames are named in a WINDOW clause.
```sql
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER w3, 2) AS ma3_partial,
       COUNT(*) OVER w3              AS rows_in_window,
       CASE WHEN COUNT(*) OVER w3 = 3 THEN ROUND(AVG(amount) OVER w3, 2) END AS ma3,
       CASE WHEN COUNT(*) OVER w7 = 7 THEN ROUND(AVG(amount) OVER w7, 2) END AS ma7
FROM daily_sales
WINDOW w3 AS (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
       w7 AS (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
ORDER BY sale_date
```

**pandas answer:**
```py
sales["ma3_partial"] = sales["amount"].rolling(3, min_periods=1).mean().round(2)
sales["rows_in_window"] = sales["amount"].rolling(3, min_periods=1).count()
sales["ma3"] = sales["amount"].rolling(3).mean().round(2)
sales["ma7"] = sales["amount"].rolling(7).mean().round(2)
```

**Example:**
- Day 1: window is just 12, so the partial average is 12.0 and `COUNT(*)` is 1: the strict version is NULL. Day 2: (12 + 18) / 2 = 15.0, count 2, NULL.
- Day 3: (12 + 18 + 30) / 3 = 20.0, count 3, now returned. Day 4: (18 + 30 + 24) / 3 = 24.0. Day 6: (24 + 36 + 60) / 3 = 40.0. Day 8: (60 + 42 + 48) / 3 = 50.0.
- 7-day: first complete on day 7: (12 + 18 + 30 + 24 + 36 + 60 + 42) / 7 = 222 / 7 = 31.71. Day 8: 258 / 7 = 36.86.

**Code:** run with `python3 -I`.
```python
# Q8: 3-day and 7-day moving average, incomplete window at the start
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',12),('2024-01-02',18),('2024-01-03',30),('2024-01-04',24),
  ('2024-01-05',36),('2024-01-06',60),('2024-01-07',42),('2024-01-08',48);
"""
SQL_MAIN = """
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER w3, 2) AS ma3_partial,
       COUNT(*) OVER w3              AS rows_in_window,
       CASE WHEN COUNT(*) OVER w3 = 3 THEN ROUND(AVG(amount) OVER w3, 2) END AS ma3,
       CASE WHEN COUNT(*) OVER w7 = 7 THEN ROUND(AVG(amount) OVER w7, 2) END AS ma7
FROM daily_sales
WINDOW w3 AS (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),
       w7 AS (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
ORDER BY sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

sales = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
sales["ma3_partial"] = sales["amount"].rolling(3, min_periods=1).mean().round(2)
sales["rows_in_window"] = sales["amount"].rolling(3, min_periods=1).count()
sales["ma3"] = sales["amount"].rolling(3).mean().round(2)
sales["ma7"] = sales["amount"].rolling(7).mean().round(2)
# pd:end
# compared in order sale_date
pd.testing.assert_frame_equal(sql_df, sales[sql_df.columns], check_dtype=False)

# a NULL amount on 2024-01-05: AVG skips it, COUNT(*) still counts the row, pandas min_periods counts non-NaN values only
con.execute("UPDATE daily_sales SET amount = NULL WHERE sale_date = '2024-01-05'")
q = """
SELECT sale_date,
       ROUND(AVG(amount) OVER w3, 2) AS avg_skips_null,
       COUNT(*) OVER w3 AS count_star, COUNT(amount) OVER w3 AS count_amount,
       CASE WHEN COUNT(*) OVER w3 = 3 THEN ROUND(AVG(amount) OVER w3, 2) END AS ma3_count_star,
       CASE WHEN COUNT(amount) OVER w3 = 3 THEN ROUND(AVG(amount) OVER w3, 2) END AS ma3_count_amount
FROM daily_sales WINDOW w3 AS (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
ORDER BY sale_date
"""
nul = pd.read_sql_query(q, con)
s2 = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
nul["pandas_rolling3"] = s2["amount"].rolling(3).mean().round(2)
nul["pandas_minp1"] = s2["amount"].rolling(3, min_periods=1).mean().round(2)
print("\nWith amount NULL on 2024-01-05:")
print(nul.to_string(index=False))
pd.testing.assert_series_equal(nul["ma3_count_amount"], nul["pandas_rolling3"], check_names=False)
pd.testing.assert_series_equal(nul["avg_skips_null"], nul["pandas_minp1"], check_names=False)
print("asserts passed: SQL moving averages == pandas rolling (COUNT(amount) is the pandas-style guard)")
```

**Output (my run):**
```text
 sale_date  amount  ma3_partial  rows_in_window  ma3   ma7
2024-01-01      12         12.0               1  NaN   NaN
2024-01-02      18         15.0               2  NaN   NaN
2024-01-03      30         20.0               3 20.0   NaN
2024-01-04      24         24.0               3 24.0   NaN
2024-01-05      36         30.0               3 30.0   NaN
2024-01-06      60         40.0               3 40.0   NaN
2024-01-07      42         46.0               3 46.0 31.71
2024-01-08      48         50.0               3 50.0 36.86

With amount NULL on 2024-01-05:
 sale_date  avg_skips_null  count_star  count_amount  ma3_count_star  ma3_count_amount  pandas_rolling3  pandas_minp1
2024-01-01            12.0           1             1             NaN               NaN              NaN          12.0
2024-01-02            15.0           2             2             NaN               NaN              NaN          15.0
2024-01-03            20.0           3             3            20.0              20.0             20.0          20.0
2024-01-04            24.0           3             3            24.0              24.0             24.0          24.0
2024-01-05            27.0           3             2            27.0               NaN              NaN          27.0
2024-01-06            42.0           3             2            42.0               NaN              NaN          42.0
2024-01-07            51.0           3             2            51.0               NaN              NaN          51.0
2024-01-08            50.0           3             3            50.0              50.0             50.0          50.0
asserts passed: SQL moving averages == pandas rolling (COUNT(amount) is the pandas-style guard)
```

**Edge cases:**
- Incomplete start: AVG over fewer rows is a different statistic. Decide whether to show it, hide it (the CASE), or mark it.
- pandas defaults: `rolling(3)` needs 3 observations, `rolling(3, min_periods=1)` accepts fewer, which equals the SQL partial window. For an offset window like `'7D'` the default `min_periods` is 1 (per the pandas docs I opened).
- NULL in the data (I set 2024-01-05 to NULL and re-ran): `AVG` skips it, so the average of the remaining values is returned; `COUNT(*)` still counts the row, so the NULL guard passes and shows 27.0, 42.0 and 51.0 (printed). pandas `min_periods` counts non-NaN observations, so `rolling(3).mean()` returns NaN for those windows. The pandas-like guard in SQL is `COUNT(amount) = 3`, which printed NaN on exactly the same rows. Which one you want is a business choice; say it.
- Missing days: ROWS frames count rows, not days. A missing day makes "3 rows" cover more than 3 days (Q9, Q24).
- Ties: dates are unique here (primary key). With duplicates, aggregate per day first.

**Then explain:**
- The frame `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` is the trailing window of 3 rows; `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` is 7 rows.
- `COUNT(*) OVER w3` over the same named window tells you how many rows were actually in the frame, which is how to detect the incomplete start.
- Round after averaging; I rounded to 2 decimals on both sides and the assert passed, but compare floats with a tolerance in general.

**Follow-ups:**
- *Centered average?* `1 PRECEDING AND 1 FOLLOWING` (Q21).
- *Why a moving average at all?* It smooths noise; the longer the window, the more lag.
- *Exclude today (no leakage)?* Q35.

**Common mistakes:**
- Treating the first two rows' partial averages as real 3-day averages.
- Confusing ROWS 2 PRECEDING (3 rows) with a 2-day window.
- Using RANGE or the default frame with ties, so the average includes later rows of the same date.
- Assuming one row per calendar day without checking.

### Q9 ⭐⭐⭐ 🟡 Restaurant Growth (LeetCode 1321 style): customer(customer_id, name, visited_on, amount) with several customers per day. For each date that has a full 7-day window (the current day plus the 6 previous days), return the 7-day total amount and the 7-day average rounded to 2 decimals. Aggregate to one row per day first, apply ROWS BETWEEN 6 PRECEDING AND CURRENT ROW, drop the first six days, and state the assumption that every calendar day has a row (and how a missing day breaks a ROWS frame). Give the pandas version.
**Asked at:** public LeetCode-style problem bank (1321 Restaurant Growth statement seen in a search snippet; 1308 Running Total for Different Genders, 197 Rising Temperature and 180 Consecutive Numbers known only by title from third-party lists), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Collapse to one row per day with a CTE, run `SUM` and `AVG` over `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`, round the average to 2 decimals, and keep only dates from the first date plus 6 days onward; this is correct only if every calendar day has a row, because a ROWS frame counts rows, not days.

**Schema and sample data:** fourteen visits over ten days (several customers on 01-02, 01-04, 01-07, 01-10). The daily totals are 100, 100, 60, 100, 70, 90, 100, 120, 30, 60.
```sql
CREATE TABLE customer(customer_id INTEGER, name TEXT, visited_on TEXT, amount INTEGER,
                      PRIMARY KEY (customer_id, visited_on));
INSERT INTO customer VALUES (1,'Asha','2024-01-01',100),(2,'Ben','2024-01-02',50),(3,'Chitra','2024-01-02',50),
  (4,'Dev','2024-01-03',60),(1,'Asha','2024-01-04',80),(5,'Esha','2024-01-04',20),(6,'Farid','2024-01-05',70),
  (2,'Ben','2024-01-06',90),(7,'Gita','2024-01-07',40),(1,'Asha','2024-01-07',60),(8,'Hari','2024-01-08',120),
  (3,'Chitra','2024-01-09',30),(4,'Dev','2024-01-10',50),(5,'Esha','2024-01-10',10);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_RANGE` is the same query with a calendar-based RANGE frame on `julianday`, used for the missing-day check.
```sql
WITH daily AS (
  SELECT visited_on, SUM(amount) AS day_total
  FROM customer
  GROUP BY visited_on
), w AS (
  SELECT visited_on,
         SUM(day_total) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
         AVG(day_total) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_raw
  FROM daily
)
SELECT visited_on, amount, ROUND(avg_raw, 2) AS average_amount
FROM w
WHERE visited_on >= date((SELECT MIN(visited_on) FROM daily), '+6 days')
ORDER BY visited_on
```

**pandas answer:**
```py
daily = cust.groupby("visited_on", as_index=False)["amount"].sum().sort_values("visited_on")
daily["visited_on"] = pd.to_datetime(daily["visited_on"])
daily["total"] = daily["amount"].rolling(7).sum()
daily["average_amount"] = (daily["total"] / 7).round(2)
full = daily[daily["visited_on"] >= daily["visited_on"].min() + pd.Timedelta(days=6)]
pd_df = full.assign(visited_on=full["visited_on"].dt.strftime("%Y-%m-%d"))
pd_df = pd_df[["visited_on", "total", "average_amount"]].rename(columns={"total": "amount"})
```

**Example:**
- Day 1 to day 7 are the first full window: 100 + 100 + 60 + 100 + 70 + 90 + 100 = 620, average 620 / 7 = 88.57 (rounded). Days 1 to 6 have fewer than seven days, so they are dropped.
- Day 8: slide the window: 620 - 100 (day 1 leaves) + 120 = 640, average 91.43.
- Day 9: 640 - 100 + 30 = 570, average 81.43. Day 10: 570 - 60 + 60 = 570, average 81.43.
- Four rows come back: 01-07 to 01-10.

**Code:** run with `python3 -I`.
```python
# Q9: Restaurant Growth style, 7-day total and average per day
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customer(customer_id INTEGER, name TEXT, visited_on TEXT, amount INTEGER,
                      PRIMARY KEY (customer_id, visited_on));
INSERT INTO customer VALUES (1,'Asha','2024-01-01',100),(2,'Ben','2024-01-02',50),(3,'Chitra','2024-01-02',50),
  (4,'Dev','2024-01-03',60),(1,'Asha','2024-01-04',80),(5,'Esha','2024-01-04',20),(6,'Farid','2024-01-05',70),
  (2,'Ben','2024-01-06',90),(7,'Gita','2024-01-07',40),(1,'Asha','2024-01-07',60),(8,'Hari','2024-01-08',120),
  (3,'Chitra','2024-01-09',30),(4,'Dev','2024-01-10',50),(5,'Esha','2024-01-10',10);
"""
SQL_MAIN = """
WITH daily AS (
  SELECT visited_on, SUM(amount) AS day_total
  FROM customer
  GROUP BY visited_on
), w AS (
  SELECT visited_on,
         SUM(day_total) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS amount,
         AVG(day_total) OVER (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_raw
  FROM daily
)
SELECT visited_on, amount, ROUND(avg_raw, 2) AS average_amount
FROM w
WHERE visited_on >= date((SELECT MIN(visited_on) FROM daily), '+6 days')
ORDER BY visited_on
"""
SQL_RANGE = SQL_MAIN.replace("ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW",
                             "ORDER BY julianday(visited_on) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
assert sql_df.equals(pd.read_sql_query(SQL_RANGE, con))
print("ROWS frame and RANGE-on-julianday frame agree on complete data: True")

cust = pd.read_sql_query("SELECT * FROM customer", con)
# pd:main
daily = cust.groupby("visited_on", as_index=False)["amount"].sum().sort_values("visited_on")
daily["visited_on"] = pd.to_datetime(daily["visited_on"])
daily["total"] = daily["amount"].rolling(7).sum()
daily["average_amount"] = (daily["total"] / 7).round(2)
full = daily[daily["visited_on"] >= daily["visited_on"].min() + pd.Timedelta(days=6)]
pd_df = full.assign(visited_on=full["visited_on"].dt.strftime("%Y-%m-%d"))
pd_df = pd_df[["visited_on", "total", "average_amount"]].rename(columns={"total": "amount"})
# pd:end
# compared in order visited_on
pd.testing.assert_frame_equal(sql_df, pd_df.reset_index(drop=True), check_dtype=False)

# the assumption "every calendar day has a row" breaks when 2024-01-04 has no sales at all
con.execute("DELETE FROM customer WHERE visited_on = '2024-01-04'")
bad = pd.read_sql_query(SQL_MAIN, con)
good = pd.read_sql_query(SQL_RANGE, con)
cmp = bad.merge(good, on="visited_on", suffixes=("_rows", "_range"))
print("\nWith 2024-01-04 missing, ROWS frame versus a calendar RANGE frame:")
print(cmp.to_string(index=False))
c2 = pd.read_sql_query("SELECT * FROM customer", con)
d2 = c2.groupby("visited_on", as_index=False)["amount"].sum()
d2["visited_on"] = pd.to_datetime(d2["visited_on"])
print("pandas rolling(7), complete windows only (rows 7 on):", d2["amount"].rolling(7).sum().dropna().tolist())
r7 = d2.rolling("7D", on="visited_on")["amount"].sum()
print("pandas rolling('7D', on=...) for the same four dates:", r7[d2["visited_on"] >= pd.Timestamp("2024-01-07")].tolist())
print("asserts passed: SQL ROWS frame == pandas rolling(7) on complete days")
```

**Output (my run):**
```text
visited_on  amount  average_amount
2024-01-07     620           88.57
2024-01-08     640           91.43
2024-01-09     570           81.43
2024-01-10     570           81.43
ROWS frame and RANGE-on-julianday frame agree on complete data: True

With 2024-01-04 missing, ROWS frame versus a calendar RANGE frame:
visited_on  amount_rows  average_amount_rows  amount_range  average_amount_range
2024-01-07          520                86.67           520                 86.67
2024-01-08          640                91.43           540                 90.00
2024-01-09          570                81.43           470                 78.33
2024-01-10          530                75.71           470                 78.33
pandas rolling(7), complete windows only (rows 7 on): [640.0, 570.0, 530.0]
pandas rolling('7D', on=...) for the same four dates: [520.0, 540.0, 470.0, 470.0]
asserts passed: SQL ROWS frame == pandas rolling(7) on complete days
```

**Edge cases:**
- Missing calendar day: I deleted 2024-01-04 and re-ran. The ROWS frame then gives 640 for 01-08, because its seven rows reach back to 01-01, a window of eight calendar days; the calendar frame (RANGE on day numbers) gives 540. Also 01-07 comes back with only six real rows (520), as the first-date-plus-6 filter passes it. The fix is either a calendar table with zero-filled days, or RANGE on `julianday` (Q24). pandas shows the same split: `rolling(7)` is row-based, `rolling('7D', on=...)` is calendar-based (520, 540, 470, 470, printed).
- Why I filtered by date and not by row count: `COUNT(*) OVER (...) = 7` would also pass windows that hit seven rows over a longer span.
- Rounding: SQLite `ROUND` and pandas `round` agreed here. They can differ on exact halves (half away from zero versus half to even on the binary value); I did not test that.
- NULL amount: `SUM` ignores it; a day with only NULL amounts would be NULL.
- Same customer twice on a day: the statement I worked from (a search snippet, not opened) is read here as the primary key on (customer_id, visited_on), so it cannot happen; I sum per day anyway.

**Then explain:**
- Order of work: aggregate (GROUP BY day), then window, then filter. The window cannot be filtered in the same SELECT, hence the CTE `w` and the outer WHERE.
- `6 PRECEDING AND CURRENT ROW` is 7 rows: the current day plus 6 earlier.
- Result is a trailing window, so the first six days have no full week and are excluded by definition.
- The ROWS frame and the RANGE-on-julianday frame agree on complete data (checked in the code), so ROWS is fine when you have verified there is no gap.

**Follow-ups:**
- *What if days can be missing?* Calendar table or RANGE (Q24, Q45).
- *Why not a self-join?* It works (the Inflearn thread mentions one, per the notes) but is harder to read and slower on big data.
- *Show the partial weeks too?* Drop the filter and label them partial (Q8).

**Common mistakes:**
- Windowing before aggregating, so two customers on one day count as two days.
- Dropping the first six rows with LIMIT/OFFSET instead of a date rule, which breaks with gaps.
- Rounding the daily numbers before averaging.

### Q10 ⭐⭐⭐ 🟡 LAST_VALUE trap and first value per partition: employees(emp_id, dept_id, hire_date, salary). Show FIRST_VALUE(salary) OVER (PARTITION BY dept_id ORDER BY hire_date) and the broken LAST_VALUE with the default frame (returns the current row's salary), then fix it with ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING, and show the trick of reversing the ORDER BY. Explain why the default frame stops at the current row and give the pandas groupby('dept_id')['salary'].transform('first') and 'last'.
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `FIRST_VALUE` works as expected because the default frame starts at the partition start, but `LAST_VALUE` with the default frame stops at the current row (and its peers), so it just returns the current row's own salary; widen the frame to `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, or flip the ORDER BY and use `FIRST_VALUE`.

**Schema and sample data:** seven employees in three departments. Dept 10 has two hires on the same date (ids 1 and 2). Dept 20's last hire has a NULL salary; dept 30's first hire has a NULL salary.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, hire_date TEXT, salary INTEGER);
INSERT INTO employees VALUES (1,10,'2020-01-01',50),(2,10,'2020-01-01',70),(3,10,'2021-06-01',60),
  (4,20,'2019-03-01',90),(5,20,'2022-01-01',NULL),(6,30,'2018-05-01',NULL),(7,30,'2020-02-01',80);
```

**SQL answer:** `SQL_MAIN` shows all four columns; `SQL_PEERS` is a small extra for the peer case (Code block).
```sql
SELECT emp_id, dept_id, hire_date, salary,
       FIRST_VALUE(salary) OVER w AS first_sal,
       LAST_VALUE(salary)  OVER w AS last_default,
       LAST_VALUE(salary)  OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_fixed,
       FIRST_VALUE(salary) OVER (PARTITION BY dept_id ORDER BY hire_date DESC, emp_id DESC) AS last_reversed
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY hire_date, emp_id)
ORDER BY emp_id
```

**pandas answer:**
```py
emp = emp.sort_values(["dept_id", "hire_date", "emp_id"]).reset_index(drop=True)
g = emp.groupby("dept_id")["salary"]
emp["first_sal"] = g.transform(lambda s: s.iloc[0])
emp["last_fixed"] = g.transform(lambda s: s.iloc[-1])
emp["first_skipna"] = g.transform("first")
emp["last_skipna"] = g.transform("last")
```

**Example:**
- Dept 10 in order (hire date, id): 50, 70, 60. `FIRST_VALUE` = 50 on every row. Default `LAST_VALUE` = the row's own salary: 50, 70, 60. Fixed `LAST_VALUE` and reversed `FIRST_VALUE` = 60 on every row.
- Why the default fails: at row 1 the frame is only row 1, so the "last" row in the frame is row 1.
- Peers: ordered by `hire_date` only, emps 1 and 2 are peers, so the default frame for emp 1 already includes emp 2 and `LAST_VALUE` returns 70 for both (printed `last_default_no_tiebreak`). That is the RANGE-peers rule (Q6) again.
- Dept 20: first = 90, last = NULL (the last hire has a NULL salary). Dept 30: first = NULL, last = 80.

**Code:** run with `python3 -I`.
```python
# Q10: FIRST_VALUE, the LAST_VALUE trap, and the fixes
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, hire_date TEXT, salary INTEGER);
INSERT INTO employees VALUES (1,10,'2020-01-01',50),(2,10,'2020-01-01',70),(3,10,'2021-06-01',60),
  (4,20,'2019-03-01',90),(5,20,'2022-01-01',NULL),(6,30,'2018-05-01',NULL),(7,30,'2020-02-01',80);
"""
SQL_MAIN = """
SELECT emp_id, dept_id, hire_date, salary,
       FIRST_VALUE(salary) OVER w AS first_sal,
       LAST_VALUE(salary)  OVER w AS last_default,
       LAST_VALUE(salary)  OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_fixed,
       FIRST_VALUE(salary) OVER (PARTITION BY dept_id ORDER BY hire_date DESC, emp_id DESC) AS last_reversed
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY hire_date, emp_id)
ORDER BY emp_id
"""
SQL_PEERS = """
SELECT emp_id, LAST_VALUE(salary) OVER (PARTITION BY dept_id ORDER BY hire_date) AS last_default_no_tiebreak
FROM employees WHERE dept_id = 10 ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nLAST_VALUE default frame, ORDER BY hire_date only, dept 10 (emps 1 and 2 are peers):")
print(pd.read_sql_query(SQL_PEERS, con).to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
emp = emp.sort_values(["dept_id", "hire_date", "emp_id"]).reset_index(drop=True)
g = emp.groupby("dept_id")["salary"]
emp["first_sal"] = g.transform(lambda s: s.iloc[0])
emp["last_fixed"] = g.transform(lambda s: s.iloc[-1])
emp["first_skipna"] = g.transform("first")
emp["last_skipna"] = g.transform("last")
# pd:end
# compared in order emp_id
pd_df = emp.sort_values("emp_id").reset_index(drop=True)
pd.testing.assert_series_equal(sql_df["first_sal"], pd_df["first_sal"], check_dtype=False)
pd.testing.assert_series_equal(sql_df["last_fixed"], pd_df["last_fixed"], check_dtype=False)
pd.testing.assert_series_equal(sql_df["last_fixed"], sql_df["last_reversed"], check_dtype=False, check_names=False)
assert sql_df["last_default"].equals(sql_df["salary"])
print("\npandas first/last with NaN skipped versus positional (SQL-like):")
print(pd_df[["emp_id", "dept_id", "salary", "first_sal", "first_skipna", "last_fixed", "last_skipna"]].to_string(index=False))
print("asserts passed: FIRST_VALUE, fixed LAST_VALUE and reversed FIRST_VALUE == pandas positional transform; default LAST_VALUE == salary")
```

**Output (my run):**
```text
 emp_id  dept_id  hire_date  salary  first_sal  last_default  last_fixed  last_reversed
      1       10 2020-01-01    50.0       50.0          50.0        60.0           60.0
      2       10 2020-01-01    70.0       50.0          70.0        60.0           60.0
      3       10 2021-06-01    60.0       50.0          60.0        60.0           60.0
      4       20 2019-03-01    90.0       90.0          90.0         NaN            NaN
      5       20 2022-01-01     NaN       90.0           NaN         NaN            NaN
      6       30 2018-05-01     NaN        NaN           NaN        80.0           80.0
      7       30 2020-02-01    80.0        NaN          80.0        80.0           80.0

LAST_VALUE default frame, ORDER BY hire_date only, dept 10 (emps 1 and 2 are peers):
 emp_id  last_default_no_tiebreak
      1                        70
      2                        70
      3                        60

pandas first/last with NaN skipped versus positional (SQL-like):
 emp_id  dept_id  salary  first_sal  first_skipna  last_fixed  last_skipna
      1       10    50.0       50.0          50.0        60.0         60.0
      2       10    70.0       50.0          50.0        60.0         60.0
      3       10    60.0       50.0          50.0        60.0         60.0
      4       20    90.0       90.0          90.0         NaN         90.0
      5       20     NaN       90.0          90.0         NaN         90.0
      6       30     NaN        NaN          80.0        80.0         80.0
      7       30    80.0        NaN          80.0        80.0         80.0
asserts passed: FIRST_VALUE, fixed LAST_VALUE and reversed FIRST_VALUE == pandas positional transform; default LAST_VALUE == salary
```

**Edge cases:**
- NULL values: `FIRST_VALUE` and `LAST_VALUE` return NULL if that row's value is NULL. SQLite has no `IGNORE NULLS`, and neither does PostgreSQL (per the PostgreSQL docs I opened). Some engines have it (not executed).
- pandas surprise: `transform("first")` and `transform("last")` skip NaN, so dept 20's last becomes 90 and dept 30's first becomes 80 (printed columns `first_skipna`, `last_skipna`). To match SQL's positional meaning use `s.iloc[0]` and `s.iloc[-1]` (the code does and asserts equality).
- Ties: always give the window a unique ORDER BY (`hire_date, emp_id`), otherwise "first hire" among same-day hires is arbitrary.
- Single-row partition: first and last are that row.
- The window name with an extra frame (`OVER (w ROWS BETWEEN ...)`) ran on SQLite 3.45.1 because `w` itself has no frame clause. A base window with its own frame cannot be extended (not tested).

**Then explain:**
- Window functions with an ORDER BY use the default frame, `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: the frame stops at the current row (and peers). `FIRST_VALUE`, `LAST_VALUE` and `NTH_VALUE` read from the frame, not the whole partition, unlike `LAG`/`LEAD` and the ranking functions.
- Reverse trick: `FIRST_VALUE(x) OVER (... ORDER BY hire_date DESC, emp_id DESC)` is the last value of the ascending order; the frame still starts at the partition start in the new order. The tie-breaker must be reversed too.
- pandas: `groupby("dept_id")["salary"].transform(...)` returns one value per row aligned to the original index, after sorting by the order columns.

**Follow-ups:**
- *Latest salary per department as one row?* Group, or rank and filter (Part 4).
- *NTH_VALUE?* Same frame trap (Q19).
- *Why not `MAX(hire_date)`?* It returns a date, not the salary on that date.

**Common mistakes:**
- Using `LAST_VALUE` with ORDER BY and no frame, getting the current row back.
- Forgetting the tie-breaker, so the "first" among same-day rows is arbitrary.
- Using pandas `'last'` on data with NaN and expecting the last row.

### Q11 ⭐⭐⭐ 🟡 Compare each row with the first value in its group: monthly_active(user_id, month, minutes). For each user show minutes in the first month, minutes this month, and the percentage of the first month's value, using FIRST_VALUE(minutes) OVER (PARTITION BY user_id ORDER BY month). Explain the NULL or zero first value case, and give the pandas groupby().transform('first') version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `FIRST_VALUE(minutes) OVER (PARTITION BY user_id ORDER BY month)` puts each user's first-month minutes on every row, so `100.0 * minutes / first_minutes` is the percent of the first month; if the first value is 0, divide with `NULLIF(first, 0)` (NULL result, no crash), and if it is NULL the percent is NULL; in pandas it is `groupby("user_id")["minutes"].transform(...)`.

**Schema and sample data:** user 1 has three months, user 2's first month is 0, user 3's first month is NULL, user 4 has one month.
```sql
CREATE TABLE monthly_active(user_id INTEGER, month TEXT, minutes INTEGER, PRIMARY KEY (user_id, month));
INSERT INTO monthly_active VALUES (1,'2024-01',50),(1,'2024-02',60),(1,'2024-03',40),
  (2,'2024-01',0),(2,'2024-02',30),(3,'2024-01',NULL),(3,'2024-02',20),(4,'2024-01',80);
```

**SQL answer:** `SQL_MAIN` (Code block).
```sql
WITH f AS (
  SELECT user_id, month, minutes,
         FIRST_VALUE(minutes) OVER (PARTITION BY user_id ORDER BY month) AS first_minutes
  FROM monthly_active
)
SELECT user_id, month, first_minutes, minutes,
       ROUND(100.0 * minutes / NULLIF(first_minutes, 0), 1) AS pct_of_first
FROM f
ORDER BY user_id, month
```

**pandas answer:**
```py
ma = ma.sort_values(["user_id", "month"]).reset_index(drop=True)
g = ma.groupby("user_id")["minutes"]
ma["first_minutes"] = g.transform(lambda s: s.iloc[0])
ma["pct_of_first"] = (100 * ma["minutes"] / ma["first_minutes"].where(ma["first_minutes"] != 0)).round(1)
```

**Example:**
- User 1: first 50. Month 01: 50 / 50 = 100.0; month 02: 60 / 50 = 120.0; month 03: 40 / 50 = 80.0.
- User 2: first is 0, so `NULLIF(0, 0)` is NULL and both percents are NULL. User 3: the first value is NULL, so every percent is NULL, even month 02 (20).
- User 4: only one month, 80 / 80 = 100.0.

**Code:** run with `python3 -I`.
```python
# Q11: compare each row with the first value in its group
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_active(user_id INTEGER, month TEXT, minutes INTEGER, PRIMARY KEY (user_id, month));
INSERT INTO monthly_active VALUES (1,'2024-01',50),(1,'2024-02',60),(1,'2024-03',40),
  (2,'2024-01',0),(2,'2024-02',30),(3,'2024-01',NULL),(3,'2024-02',20),(4,'2024-01',80);
"""
SQL_MAIN = """
WITH f AS (
  SELECT user_id, month, minutes,
         FIRST_VALUE(minutes) OVER (PARTITION BY user_id ORDER BY month) AS first_minutes
  FROM monthly_active
)
SELECT user_id, month, first_minutes, minutes,
       ROUND(100.0 * minutes / NULLIF(first_minutes, 0), 1) AS pct_of_first
FROM f
ORDER BY user_id, month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

ma = pd.read_sql_query("SELECT * FROM monthly_active", con)
# pd:main
ma = ma.sort_values(["user_id", "month"]).reset_index(drop=True)
g = ma.groupby("user_id")["minutes"]
ma["first_minutes"] = g.transform(lambda s: s.iloc[0])
ma["pct_of_first"] = (100 * ma["minutes"] / ma["first_minutes"].where(ma["first_minutes"] != 0)).round(1)
# pd:end
# compared in order user_id, month
pd.testing.assert_frame_equal(sql_df, ma[sql_df.columns], check_dtype=False)
print("\ntransform('first') skips NaN:", g.transform("first").tolist())
print("positional first (matches SQL): ", ma["first_minutes"].tolist())
print("raw division by a 0 first value in pandas:", (100 * ma["minutes"] / ma.groupby("user_id")["minutes"].transform(lambda s: s.iloc[0])).tolist()[3:5])
print("asserts passed: FIRST_VALUE + NULLIF percent == pandas positional first + masked zero")
```

**Output (my run):**
```text
 user_id   month  first_minutes  minutes  pct_of_first
       1 2024-01           50.0     50.0         100.0
       1 2024-02           50.0     60.0         120.0
       1 2024-03           50.0     40.0          80.0
       2 2024-01            0.0      0.0           NaN
       2 2024-02            0.0     30.0           NaN
       3 2024-01            NaN      NaN           NaN
       3 2024-02            NaN     20.0           NaN
       4 2024-01           80.0     80.0         100.0

transform('first') skips NaN: [50.0, 50.0, 50.0, 0.0, 0.0, 20.0, 20.0, 80.0]
positional first (matches SQL):  [50.0, 50.0, 50.0, 0.0, 0.0, nan, nan, 80.0]
raw division by a 0 first value in pandas: [nan, inf]
asserts passed: FIRST_VALUE + NULLIF percent == pandas positional first + masked zero
```

**Edge cases:**
- Zero first value: percent is undefined; NULL is the honest answer. pandas would give `inf` (30 / 0) and NaN (0 / 0) (printed), so I masked the zero with `.where(first != 0)`.
- NULL first value: SQL `FIRST_VALUE` returns NULL (no `IGNORE NULLS` in SQLite). pandas `transform("first")` skips NaN and returned 20.0 for user 3, which is the first non-null, not the first month (printed). Use `s.iloc[0]` for the SQL meaning, or decide that the first non-null month is the baseline and say so.
- "First month" is the first row of the user, not the user's signup month; with missing months you may want a calendar join (Q16).
- Duplicates: `(user_id, month)` is the primary key here; otherwise add a tie-breaker.

**Then explain:**
- The window is the default frame, which includes the partition start, so `FIRST_VALUE` is safe without a frame clause (unlike `LAST_VALUE`, Q10).
- The percent is of the baseline: 120.0 means 20 percent above month one; the change is `pct - 100`.
- The CTE is needed because I use the window result in a further expression (`first_minutes` as a divisor); an alias cannot be reused in the same SELECT.
- A `MIN(month)` join would also work, but needs a self-join.

**Follow-ups:**
- *Index to 100 for prices?* Same formula (Q38).
- *Compare with the previous month instead?* LAG (Q4).
- *Compare with the user's best month?* `MAX(minutes) OVER (PARTITION BY user_id)`.

**Common mistakes:**
- Dividing by a first value of zero without NULLIF.
- Assuming pandas `'first'` is positional.
- Not ordering the window, so "first" is arbitrary.

### Q12 ⭐⭐⭐ 🟡 Running balance for a bank account: bank_txns(txn_id, account_id, txn_date, txn_type, amount) where txn_type is 'deposit' or 'withdrawal' and amount is always positive. Convert to a signed amount with CASE, compute the running balance per account ordered by txn_date and txn_id, flag rows where the balance goes below zero, and return each account's closing balance. Give the pandas version with np.where and groupby().cumsum(), and say what you would do if two transactions share a timestamp.
**Asked at:** codemia.io practice page 'running total partitioned by user_id' (the page itself states a Microsoft data scientist phone screen; not independently verified, treat as site-reported); analyst and data scientist screens
**Say this first (1 line):** Turn each row into a signed amount (`CASE txn_type WHEN 'deposit' THEN amount WHEN 'withdrawal' THEN -amount END`), take `SUM(signed) OVER (PARTITION BY account_id ORDER BY txn_date, txn_id)` for the running balance, flag `balance < 0`, and get the closing balance as the per-account sum (which equals the last running balance); if two transactions share a timestamp, order is a business rule, so break the tie with a posting sequence, here `txn_id`.

**Schema and sample data:** three accounts. Account 1 has a withdrawal of 70 and a deposit of 50 on the same date (ids 3 and 4). Account 2 ends exactly at zero.
```sql
CREATE TABLE bank_txns(txn_id INTEGER PRIMARY KEY, account_id INTEGER, txn_date TEXT, txn_type TEXT, amount INTEGER);
INSERT INTO bank_txns VALUES (1,1,'2024-01-01','deposit',100),(2,1,'2024-01-02','withdrawal',60),
  (3,1,'2024-01-03','withdrawal',70),(4,1,'2024-01-03','deposit',50),
  (5,2,'2024-01-01','deposit',20),(6,2,'2024-01-02','withdrawal',20),(7,3,'2024-01-05','deposit',500);
```

**SQL answer:** `SQL_MAIN` (running balance and flag), `SQL_CLOSING` (closing balance), and `SQL_DEPOSIT_FIRST`, the same query with deposits ordered before withdrawals on the same date (Code block).
```sql
WITH s AS (
  SELECT txn_id, account_id, txn_date, txn_type, amount,
         CASE txn_type WHEN 'deposit' THEN amount WHEN 'withdrawal' THEN -amount END AS signed_amount
  FROM bank_txns
)
SELECT txn_id, account_id, txn_date, txn_type, signed_amount,
       SUM(signed_amount) OVER (PARTITION BY account_id ORDER BY txn_date, txn_id) AS balance,
       CASE WHEN SUM(signed_amount) OVER (PARTITION BY account_id ORDER BY txn_date, txn_id) < 0
            THEN 1 ELSE 0 END AS below_zero
FROM s
ORDER BY account_id, txn_date, txn_id
```
```sql
SELECT account_id,
       SUM(CASE txn_type WHEN 'deposit' THEN amount WHEN 'withdrawal' THEN -amount END) AS closing_balance
FROM bank_txns
GROUP BY account_id
ORDER BY account_id
```

**pandas answer:**
```py
txns = txns.sort_values(["account_id", "txn_date", "txn_id"]).reset_index(drop=True)
txns["signed_amount"] = np.where(txns["txn_type"] == "deposit", txns["amount"],
                                 np.where(txns["txn_type"] == "withdrawal", -txns["amount"], np.nan))
txns["balance"] = txns.groupby("account_id")["signed_amount"].cumsum()
txns["below_zero"] = (txns["balance"] < 0).astype(int)
pd_closing = txns.groupby("account_id", as_index=False)["signed_amount"].sum().rename(columns={"signed_amount": "closing_balance"})
```

**Example:**
- Account 1, in (date, id) order: +100 gives 100; -60 gives 40; -70 gives -30 (below zero, flagged); +50 gives 20. Closing balance 20.
- Account 2: +20 gives 20; -20 gives 0, which is not below zero (the flag uses `< 0`). Account 3: 500.
- Same-date order matters: if the deposit (id 4) is processed before the withdrawal (id 3), the balances are 100, 40, 90, 20 and nothing is flagged. The printed run shows the order is an assumption that changes the overdraft flag.

**Code:** run with `python3 -I`.
```python
# Q12: running balance for a bank account
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE bank_txns(txn_id INTEGER PRIMARY KEY, account_id INTEGER, txn_date TEXT, txn_type TEXT, amount INTEGER);
INSERT INTO bank_txns VALUES (1,1,'2024-01-01','deposit',100),(2,1,'2024-01-02','withdrawal',60),
  (3,1,'2024-01-03','withdrawal',70),(4,1,'2024-01-03','deposit',50),
  (5,2,'2024-01-01','deposit',20),(6,2,'2024-01-02','withdrawal',20),(7,3,'2024-01-05','deposit',500);
"""
SQL_MAIN = """
WITH s AS (
  SELECT txn_id, account_id, txn_date, txn_type, amount,
         CASE txn_type WHEN 'deposit' THEN amount WHEN 'withdrawal' THEN -amount END AS signed_amount
  FROM bank_txns
)
SELECT txn_id, account_id, txn_date, txn_type, signed_amount,
       SUM(signed_amount) OVER (PARTITION BY account_id ORDER BY txn_date, txn_id) AS balance,
       CASE WHEN SUM(signed_amount) OVER (PARTITION BY account_id ORDER BY txn_date, txn_id) < 0
            THEN 1 ELSE 0 END AS below_zero
FROM s
ORDER BY account_id, txn_date, txn_id
"""
SQL_CLOSING = """
SELECT account_id,
       SUM(CASE txn_type WHEN 'deposit' THEN amount WHEN 'withdrawal' THEN -amount END) AS closing_balance
FROM bank_txns
GROUP BY account_id
ORDER BY account_id
"""
SQL_DEPOSIT_FIRST = SQL_MAIN.replace("ORDER BY txn_date, txn_id", "ORDER BY txn_date, txn_type, txn_id")
SQL_UNKNOWN = """
SELECT CASE t WHEN 'deposit' THEN a WHEN 'withdrawal' THEN -a END AS signed FROM (SELECT 'fee' AS t, 5 AS a)
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
closing = pd.read_sql_query(SQL_CLOSING, con)
print(sql_df.to_string(index=False))
print("\nClosing balance per account:")
print(closing.to_string(index=False))

txns = pd.read_sql_query("SELECT * FROM bank_txns", con)
# pd:main
txns = txns.sort_values(["account_id", "txn_date", "txn_id"]).reset_index(drop=True)
txns["signed_amount"] = np.where(txns["txn_type"] == "deposit", txns["amount"],
                                 np.where(txns["txn_type"] == "withdrawal", -txns["amount"], np.nan))
txns["balance"] = txns.groupby("account_id")["signed_amount"].cumsum()
txns["below_zero"] = (txns["balance"] < 0).astype(int)
pd_closing = txns.groupby("account_id", as_index=False)["signed_amount"].sum().rename(columns={"signed_amount": "closing_balance"})
# pd:end
# compared in order account_id, txn_date, txn_id
pd.testing.assert_frame_equal(sql_df, txns[sql_df.columns], check_dtype=False)
pd.testing.assert_frame_equal(closing, pd_closing, check_dtype=False)
assert txns.groupby("account_id")["balance"].last().tolist() == closing["closing_balance"].tolist()

alt = pd.read_sql_query(SQL_DEPOSIT_FIRST, con)
print("\nAccount 1 on 2024-01-03 with deposit processed first instead (ORDER BY txn_date, txn_type, txn_id):")
print(alt[alt["account_id"] == 1][["txn_id", "txn_type", "balance", "below_zero"]].to_string(index=False))
print("rows flagged below zero, txn_id order: ", sql_df.loc[sql_df["below_zero"] == 1, "txn_id"].tolist())
print("rows flagged below zero, deposit first:", alt.loc[alt["below_zero"] == 1, "txn_id"].tolist())
print("\nunknown txn_type 'fee' in SQL CASE (no ELSE):", con.execute(SQL_UNKNOWN).fetchall(),
      "| the naive np.where(type == 'deposit', amount, -amount) would give", int(np.where("fee" == "deposit", 5, -5)))
print("asserts passed: SQL running balance, flag and closing == pandas np.where + groupby cumsum")
```

**Output (my run):**
```text
 txn_id  account_id   txn_date   txn_type  signed_amount  balance  below_zero
      1           1 2024-01-01    deposit            100      100           0
      2           1 2024-01-02 withdrawal            -60       40           0
      3           1 2024-01-03 withdrawal            -70      -30           1
      4           1 2024-01-03    deposit             50       20           0
      5           2 2024-01-01    deposit             20       20           0
      6           2 2024-01-02 withdrawal            -20        0           0
      7           3 2024-01-05    deposit            500      500           0

Closing balance per account:
 account_id  closing_balance
          1               20
          2                0
          3              500

Account 1 on 2024-01-03 with deposit processed first instead (ORDER BY txn_date, txn_type, txn_id):
 txn_id   txn_type  balance  below_zero
      1    deposit      100           0
      2 withdrawal       40           0
      3 withdrawal       20           0
      4    deposit       90           0
rows flagged below zero, txn_id order:  [3]
rows flagged below zero, deposit first: []

unknown txn_type 'fee' in SQL CASE (no ELSE): [(None,)] | the naive np.where(type == 'deposit', amount, -amount) would give -5
asserts passed: SQL running balance, flag and closing == pandas np.where + groupby cumsum
```

**Edge cases:**
- Same timestamp: I assumed `txn_id` follows posting order. If it does not, use a real sequence or timestamp with time, or define a rule (for example deposits first, as many banks post credits before debits, which I did not verify). Say the assumption aloud.
- Unknown `txn_type` (for example 'fee'): my CASE has no ELSE, so SQL gives NULL and SUM ignores the row silently (printed). The naive `np.where(type == 'deposit', amount, -amount)` would treat it as a withdrawal (-5, printed). I nested `np.where` so unknown types become NaN, matching SQL; better, reject unknown types with a constraint.
- NULL amount: signed is NULL, ignored by SUM; `cumsum` skips it too.
- Account with no transactions: no row, and no closing balance; join to an accounts table if you need zeros.
- Closing balance: `SUM(...) GROUP BY` equals the last running balance (the code asserts it); I did not need ROW_NUMBER (Part 4).
- The flag marks every row where the balance is negative, not only the first time it goes negative.

**Then explain:**
- Signed amount first, because a window sum over positive amounts cannot know which are debits.
- The window sums rows in `(txn_date, txn_id)` order inside each account, so each row's balance is the balance after that transaction.
- The same window expression appears twice (balance and flag). In production I would put the balance in a CTE and flag in the outer query; I repeated it to keep one query.
- pandas: `np.where` for the sign, `groupby("account_id")["signed_amount"].cumsum()` for the balance, and a boolean cast for the flag.

**Follow-ups:**
- *First time the balance goes negative per account?* Filter the flagged rows and take the first (ranking, Part 4), or `MIN(CASE WHEN balance < 0 THEN txn_id END)` per account.
- *Maximum overdraft?* `MIN(balance)` per account.
- *Opening balance?* Add it as a first signed row or add a constant.

**Common mistakes:**
- Running the SUM over unsigned amounts.
- No `txn_id` tie-breaker, so same-day order is arbitrary and the overdraft flag may change between runs.
- Using `np.where` with a single condition, which misclassifies unknown types.
- Using `<= 0` for "below zero".
