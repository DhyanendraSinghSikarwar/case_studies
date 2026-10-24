# Book 3 — Part 5: Window functions: running totals, LAG/LEAD, moving averages, with pandas equivalents

**Topic:** running totals and cumulative sums (SUM OVER ORDER BY), the default frame and the peers (duplicate date) trap, ROWS versus RANGE versus GROUPS and EXCLUDE, running totals per group, running count, average, percent of total, max and min, moving averages with ROWS BETWEEN n PRECEDING and the incomplete window at the start, centered and trailing windows, time-based windows with RANGE on day numbers (SQLite needs numeric offsets; INTERVAL RANGE is PostgreSQL), LAG and LEAD with offset and default, previous-row differences, day-over-day, month-over-month and year-over-year change and percent change (division by zero and NULL), missing months breaking LAG, FIRST_VALUE, LAST_VALUE trap, NTH_VALUE, running balance and inventory stock, cumulative distinct counts by first-occurrence flag, running rank, increase and decrease flags, Pareto cumulative share, reset-by-condition and forward fill with windows plus MAX, EWMA at concept level, time gaps with julianday, trailing 7-day customers, window performance concept, and the pandas side (cumsum, cummax, cummin, cumprod, cumcount, shift, diff, pct_change, groupby shift and cumsum, rolling with min_periods, center, closed and time offsets, expanding, ewm, resample and reindex for calendar completion) with the SQL-versus-pandas differences (NaN handling, min_periods defaults, pct_change inf, shift upcasting)
**Target:** 45  |  **Actual:** 46 (⭐⭐⭐ 18, ⭐⭐ 16, ⭐ 12)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers running aggregates, frames, LAG and LEAD, moving averages and period-over-period change. Ranking, top-N, deduplication, NTILE, PERCENT_RANK (Part 4), date and cohort logic such as retention and cohorts (Part 6), gaps and islands and sessionization (Part 7) are deliberately out; where a question touches them (streaks, reset by condition, time gaps) it stops at the LAG comparison or a flag and points to the later part. Every query question states its tables and columns so Wave B can build small sample data; answers must run on SQLite 3.45 (window functions since 3.25, GROUPS and EXCLUDE since 3.28) and compare with pandas 3.0.x; anything engine-specific (INTERVAL RANGE, IGNORE NULLS, DATEDIFF, DATE_TRUNC, other engines' default frames) is shown as hedged text labelled 'not executed' unless run.

Evidence limits: no candidate-reported SQL questions were found; the search returned prep guides, practice-site pages, third-party LeetCode list snippets and documentation. One practice page (codemia) states that a Microsoft data scientist phone screen asked a per-user running total; this is the site's own claim, not verified. The 'Asked at' tags are source types, and 'expert gap-check' marks questions chosen from practice. Star ratings blend how often a topic appears across guides with judgement. See research_notes/Book3_Part05_sources.md for which pages were opened.

---

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

### Q13 ⭐⭐⭐ 🟡 Rising Temperature (LeetCode 197 style) with LAG: weather(id, record_date, temperature). Return the dates on which the temperature was higher than on the previous calendar day. Show the LAG version, then explain why LAG compares the previous row and not the previous day, so a missing date gives a wrong answer unless you also check julianday(record_date) - julianday(prev_date) = 1, and give the self-join alternative and the pandas shift and diff version.
**Asked at:** public LeetCode-style problem bank (1321 Restaurant Growth statement seen in a search snippet; 1308 Running Total for Different Genders, 197 Rising Temperature and 180 Consecutive Numbers known only by title from third-party lists), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** `LAG` looks at the previous row in the sort order, not the previous calendar day, so I compare `temperature > prev_temp` and also check `julianday(record_date) - julianday(prev_date) = 1`; without the second test a missing date compares a day with the one before the gap.

**Schema and sample data:** nine days of readings, inserted with ids that do not follow date order. 2024-01-05 has no row, 2024-01-09 has a NULL temperature.
```sql
CREATE TABLE weather(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO weather VALUES (1,'2024-01-02',25),(2,'2024-01-01',10),(3,'2024-01-04',30),
  (4,'2024-01-03',20),(5,'2024-01-06',35),(6,'2024-01-07',35),(7,'2024-01-08',40),
  (8,'2024-01-09',NULL),(9,'2024-01-10',50);
```

**SQL answer:** LAG with the gap check (`SQL_MAIN`), the naive LAG without it, and the self-join alternative. Tie rule: `ORDER BY record_date, id`.
```sql
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp,
         LAG(record_date) OVER (ORDER BY record_date, id) AS prev_date
  FROM weather
)
SELECT record_date
FROM x
WHERE temperature > prev_temp
  AND julianday(record_date) - julianday(prev_date) = 1
ORDER BY record_date
```
```sql
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp
  FROM weather
)
SELECT record_date FROM x WHERE temperature > prev_temp ORDER BY record_date
```
```sql
SELECT t.record_date
FROM weather t
JOIN weather p ON p.record_date = date(t.record_date, '-1 day')
WHERE t.temperature > p.temperature
ORDER BY t.record_date
```

**pandas answer:** sort, then compare with `shift()` for the value and `diff()` for the date gap.
```py
w = weather.assign(record_date=pd.to_datetime(weather["record_date"])).sort_values(["record_date", "id"])
prev_temp = w["temperature"].shift()
gap_days = w["record_date"].diff()
pd_df = w.loc[(w["temperature"] > prev_temp) & (gap_days == pd.Timedelta(days=1)), ["record_date"]]
```

**Example:** sorted by date: 01-01=10, 01-02=25, 01-03=20, 01-04=30, 01-06=35, 01-07=35, 01-08=40, 01-09=NULL, 01-10=50.
- 01-02: 25 > 10 and the gap is 1 day, so it counts.
- 01-03: 20 < 25, no. 01-04: 30 > 20 and gap 1, yes.
- 01-06: 35 > 30, but the previous row is 01-04 (gap 2 days), so the gap check rejects it. The naive LAG query keeps it, which is the wrong row.
- 01-07: 35 = 35, not higher. 01-08: 40 > 35, gap 1, yes.
- 01-09: NULL is never greater than anything. 01-10: previous temperature is NULL, so `50 > NULL` is unknown and it is dropped.
- Result: 01-02, 01-04, 01-08.

**Code:** run with `python3 -I`.
```python
# Q13: Rising Temperature with LAG, gap check, self-join, pandas shift/diff
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE weather(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO weather VALUES (1,'2024-01-02',25),(2,'2024-01-01',10),(3,'2024-01-04',30),
  (4,'2024-01-03',20),(5,'2024-01-06',35),(6,'2024-01-07',35),(7,'2024-01-08',40),
  (8,'2024-01-09',NULL),(9,'2024-01-10',50);
"""
SQL_MAIN = """
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp,
         LAG(record_date) OVER (ORDER BY record_date, id) AS prev_date
  FROM weather
)
SELECT record_date
FROM x
WHERE temperature > prev_temp
  AND julianday(record_date) - julianday(prev_date) = 1
ORDER BY record_date
"""
SQL_NAIVE = """
WITH x AS (
  SELECT record_date, temperature,
         LAG(temperature) OVER (ORDER BY record_date, id) AS prev_temp
  FROM weather
)
SELECT record_date FROM x WHERE temperature > prev_temp ORDER BY record_date
"""
SQL_JOIN = """
SELECT t.record_date
FROM weather t
JOIN weather p ON p.record_date = date(t.record_date, '-1 day')
WHERE t.temperature > p.temperature
ORDER BY t.record_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
naive = [r[0] for r in con.execute(SQL_NAIVE)]
join = [r[0] for r in con.execute(SQL_JOIN)]
print("LAG with gap check:", sql_df["record_date"].tolist())
print("naive LAG (no gap check):", naive)
print("self-join:", join)
assert join == sql_df["record_date"].tolist()

weather = pd.read_sql_query("SELECT * FROM weather", con)
# pd:main
w = weather.assign(record_date=pd.to_datetime(weather["record_date"])).sort_values(["record_date", "id"])
prev_temp = w["temperature"].shift()
gap_days = w["record_date"].diff()
pd_df = w.loc[(w["temperature"] > prev_temp) & (gap_days == pd.Timedelta(days=1)), ["record_date"]]
# pd:end
pd_dates = pd_df["record_date"].dt.strftime("%Y-%m-%d").tolist()
# compared after sorting by record_date
assert pd_dates == sql_df["record_date"].tolist()
print("pandas shift + diff:", pd_dates)

# calendar-correct alternative: shift(freq='D') moves the index, not the data
s = w.set_index("record_date")["temperature"]
prev_day = s.shift(freq="D").reindex(s.index)
alt = s[s > prev_day]
print("pandas shift(freq='D'):", alt.index.strftime("%Y-%m-%d").tolist())
assert alt.index.strftime("%Y-%m-%d").tolist() == pd_dates

# duplicate dates: the question is ill-defined; the gap check at least rejects the pair itself
con.executescript("""
CREATE TABLE wdup(id INTEGER PRIMARY KEY, record_date TEXT, temperature INTEGER);
INSERT INTO wdup VALUES (1,'2024-01-01',10),(2,'2024-01-02',20),(3,'2024-01-02',30),(4,'2024-01-03',40);
""")
dup_sql = SQL_MAIN.replace("FROM weather", "FROM wdup")
print("duplicate date 01-02 (ids 2,3):", [r[0] for r in con.execute(dup_sql)])
print("asserts passed: LAG+gap == self-join == pandas shift/diff == shift(freq='D')")
```

**Output (my run):**
```text
LAG with gap check: ['2024-01-02', '2024-01-04', '2024-01-08']
naive LAG (no gap check): ['2024-01-02', '2024-01-04', '2024-01-06', '2024-01-08']
self-join: ['2024-01-02', '2024-01-04', '2024-01-08']
pandas shift + diff: ['2024-01-02', '2024-01-04', '2024-01-08']
pandas shift(freq='D'): ['2024-01-02', '2024-01-04', '2024-01-08']
duplicate date 01-02 (ids 2,3): ['2024-01-02', '2024-01-03']
asserts passed: LAG+gap == self-join == pandas shift/diff == shift(freq='D')
```

**Edge cases:**
- Missing date: the naive query returned 01-06 as well (four dates instead of three); the gap check, the self-join and pandas all returned three.
- NULL temperature: the comparison is unknown, so the row is dropped, and the row after it is dropped too because its previous value is NULL. If the business wants to skip over NULL days, that is a different question.
- Duplicate dates: the problem assumes one row per date. I tested a table with two rows on 01-02 (ids 2 and 3): with the tie rule `id`, the second copy has a 0-day gap so it is rejected, but the next day then compares only with the higher-id copy and 01-03 was returned. Fix the data (aggregate to one row per date) before trusting the answer.
- Order: the ids are not in date order in my sample, so `ORDER BY id` would give wrong answers; the window must order by `record_date`.
- Dates stored as text must be ISO `YYYY-MM-DD`; otherwise `julianday` returns NULL and the gap check silently drops every row.

**Then explain:**
- `LAG(x)` is positional. It does not know about the calendar, so a gap makes "previous row" and "previous day" different things.
- Self-join: join each row to the row dated exactly one day before (`p.record_date = date(t.record_date, '-1 day')`). A missing day has no partner row, so it drops out by itself; it needs no gap test. The cost is a second scan (an index on `record_date` helps; I did not time it).
- pandas: `shift()` is also positional and `diff()` on a datetime column gives a `Timedelta`, so compare with `pd.Timedelta(days=1)`. `shift(freq="D")` is calendar-based: it moves the index labels by one day instead of moving the data, so `s.shift(freq="D").reindex(s.index)` is NaN where the previous day is missing. It returned the same three dates, but it needs a unique index (reindex raises on duplicate labels, from the documented behaviour; I did not test the error).
- Dialects (not executed here): PostgreSQL can subtract DATE values directly (`record_date - prev_date = 1`), MySQL uses `DATEDIFF(record_date, prev_date) = 1`, BigQuery uses `DATE_DIFF`. As I remember the LeetCode problem it is written for MySQL, so check the platform's dialect.

**Follow-ups:**
- *Temperature lower than the previous day?* Flip the comparison; same gap check.
- *Compare with the day before, whatever the row distance?* The self-join or `shift(freq='D')` form.
- *What if a date can repeat?* Aggregate first (`MAX` or `AVG` per date), then apply the logic.

**Common mistakes:**
- Using LAG alone and trusting it across a missing date.
- Ordering the window by `id` instead of by date.
- Comparing `julianday` differences with the wrong sign or against text dates in a non-ISO format.
- In pandas, forgetting to sort before `shift()` or `diff()`.

### Q14 ⭐⭐⭐ 🟡 Time since the previous order per customer: orders(order_id, customer_id, order_ts) with ISO timestamps text. Return each order with the number of days since the same customer's previous order (NULL for the first order) using LAG and julianday arithmetic, then the average gap per customer. Explain NULL for first orders, ties on order_ts, and give the pandas groupby().diff() version with pd.to_datetime and dt.total_seconds.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Partition by customer, order by timestamp with the order id as a tie-breaker, and subtract `julianday(LAG(order_ts))` from `julianday(order_ts)`; the first order of each customer has no previous row so the gap is NULL, and `AVG` of the gaps ignores those NULLs.

**Schema and sample data:** eight orders for three customers plus one customer (D) with a single order. Orders 2 and 3 for customer A have exactly the same timestamp. Rows for B and C are interleaved in id order, so the table is not stored grouped by customer.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
  (1,'A','2024-01-01 09:00:00'),(2,'A','2024-01-03 21:00:00'),(3,'A','2024-01-03 21:00:00'),
  (4,'A','2024-01-10 09:00:00'),(5,'B','2024-02-01 12:00:00'),(6,'C','2024-02-05 08:00:00'),
  (7,'C','2024-02-05 20:00:00'),(8,'B','2024-02-11 12:00:00'),(9,'D','2024-03-01 00:00:00');
```

**SQL answer:** per-order gap (`SQL_MAIN`) and average gap per customer (`SQL_AVG`).
```sql
WITH g AS (
  SELECT order_id, customer_id, order_ts,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS days_since_prev
  FROM orders
)
SELECT order_id, customer_id, order_ts, ROUND(days_since_prev, 4) AS days_since_prev
FROM g
ORDER BY customer_id, order_ts, order_id
```
```sql
WITH g AS (
  SELECT customer_id,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS d
  FROM orders
)
SELECT customer_id, COUNT(*) AS orders, COUNT(d) AS gaps, ROUND(AVG(d), 4) AS avg_gap_days
FROM g
GROUP BY customer_id
ORDER BY customer_id
```

**pandas answer:** parse the timestamps, sort, `groupby().diff()` gives a `Timedelta`, `dt.total_seconds() / 86400` converts to days.
```py
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"])).sort_values(["customer_id", "order_ts", "order_id"])
o["days_since_prev"] = o.groupby("customer_id")["order_ts"].diff().dt.total_seconds() / 86400
avg_gap = o.groupby("customer_id")["days_since_prev"].agg(orders="size", gaps="count", avg_gap_days="mean")
```

**Example:**
- Customer A: 01-01 09:00, 01-03 21:00, 01-03 21:00, 01-10 09:00. Gaps: NULL, 2.5 days, 0 days (same timestamp, order 3 sorts after order 2 by id), 6.5 days. Average of the three gaps = 9 / 3 = 3.0.
- Customer B: 02-01 12:00 then 02-11 12:00, gap 10.0 days, average 10.0.
- Customer C: 02-05 08:00 then 20:00, gap 0.5 days.
- Customer D: one order, no gap, so the average is NULL (`COUNT(d)` is 0).

**Code:** run with `python3 -I`.
```python
# Q14: days since the previous order per customer, average gap per customer
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_ts TEXT);
INSERT INTO orders VALUES
  (1,'A','2024-01-01 09:00:00'),(2,'A','2024-01-03 21:00:00'),(3,'A','2024-01-03 21:00:00'),
  (4,'A','2024-01-10 09:00:00'),(5,'B','2024-02-01 12:00:00'),(6,'C','2024-02-05 08:00:00'),
  (7,'C','2024-02-05 20:00:00'),(8,'B','2024-02-11 12:00:00'),(9,'D','2024-03-01 00:00:00');
"""
SQL_MAIN = """
WITH g AS (
  SELECT order_id, customer_id, order_ts,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS days_since_prev
  FROM orders
)
SELECT order_id, customer_id, order_ts, ROUND(days_since_prev, 4) AS days_since_prev
FROM g
ORDER BY customer_id, order_ts, order_id
"""
SQL_AVG = """
WITH g AS (
  SELECT customer_id,
         julianday(order_ts) - julianday(LAG(order_ts) OVER (PARTITION BY customer_id
                                                            ORDER BY order_ts, order_id)) AS d
  FROM orders
)
SELECT customer_id, COUNT(*) AS orders, COUNT(d) AS gaps, ROUND(AVG(d), 4) AS avg_gap_days
FROM g
GROUP BY customer_id
ORDER BY customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_avg = pd.read_sql_query(SQL_AVG, con)
print(sql_df.to_string(index=False))
print()
print(sql_avg.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"])).sort_values(["customer_id", "order_ts", "order_id"])
o["days_since_prev"] = o.groupby("customer_id")["order_ts"].diff().dt.total_seconds() / 86400
avg_gap = o.groupby("customer_id")["days_since_prev"].agg(orders="size", gaps="count", avg_gap_days="mean")
# pd:end
out = o[["order_id", "customer_id", "days_since_prev"]].round({"days_since_prev": 4})
# compared after sorting by customer_id, order_ts, order_id (already sorted above)
pd.testing.assert_frame_equal(sql_df[["order_id", "customer_id", "days_since_prev"]].reset_index(drop=True),
                              out.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_avg.set_index("customer_id"), avg_gap.round({"avg_gap_days": 4}),
                              check_dtype=False)
print("\npandas avg gap:")
print(avg_gap.round(4).to_string())

# the trap: diff() without groupby crosses customer boundaries
wrong = orders.assign(order_ts=pd.to_datetime(orders["order_ts"])).sort_values(["order_ts", "order_id"])
wrong_gap = (wrong["order_ts"].diff().dt.total_seconds() / 86400).round(4)
print("\nungrouped diff() on the whole table gives (order_id order):",
      dict(zip(wrong["order_id"], wrong_gap.tolist())))
print("Timedelta(days=2.5).days gives", pd.Timedelta(days=2.5).days)
print("asserts passed: SQL LAG/julianday == pandas groupby().diff()")
```

**Output (my run):**
```text
 order_id customer_id            order_ts  days_since_prev
        1           A 2024-01-01 09:00:00              NaN
        2           A 2024-01-03 21:00:00              2.5
        3           A 2024-01-03 21:00:00              0.0
        4           A 2024-01-10 09:00:00              6.5
        5           B 2024-02-01 12:00:00              NaN
        8           B 2024-02-11 12:00:00             10.0
        6           C 2024-02-05 08:00:00              NaN
        7           C 2024-02-05 20:00:00              0.5
        9           D 2024-03-01 00:00:00              NaN

customer_id  orders  gaps  avg_gap_days
          A       4     3           3.0
          B       2     1          10.0
          C       2     1           0.5
          D       1     0           NaN

pandas avg gap:
             orders  gaps  avg_gap_days
customer_id                            
A                 4     3           3.0
B                 2     1          10.0
C                 2     1           0.5
D                 1     0           NaN

ungrouped diff() on the whole table gives (order_id order): {1: nan, 2: 2.5, 3: 0.0, 4: 6.5, 5: 22.125, 6: 3.8333, 7: 0.5, 8: 5.6667, 9: 18.5}
Timedelta(days=2.5).days gives 2
asserts passed: SQL LAG/julianday == pandas groupby().diff()
```

**Edge cases:**
- First order: `LAG` returns NULL, so the difference is NULL, not 0. Keep it NULL; 0 would pull the average down and would look like "ordered twice at the same moment".
- Ties on `order_ts` (orders 2 and 3): the second one gets a gap of 0. Without the `order_id` tie-breaker the engine may put either row first, so which order is labelled "the 0-day one" is not guaranteed. With the tie-breaker order 3 is always the repeat.
- Customer with one order: appears in the output with NULL average, because the gaps were computed per order and then grouped (a customer is not dropped).
- `AVG(d)` skips NULLs, so it divides by the number of gaps (3 for A), not by the number of orders (4). `COUNT(*)` versus `COUNT(d)` shows this.
- `julianday` differences are floating point, so I rounded to 4 places before comparing. Timestamps must be ISO text (`YYYY-MM-DD HH:MM:SS`) or `julianday` gives NULL; time zones are not handled (all values are treated as the same zone).
- pandas: `groupby("customer_id")["order_ts"].diff()` gives `NaT` for the first row, so `total_seconds()` gives NaN. Without `groupby`, `diff()` runs across customers; the output shows order 5 (customer B) getting 22.125 days because it was compared with customer A's last order.

**Then explain:**
- The window is `PARTITION BY customer_id ORDER BY order_ts, order_id`: partition so customers do not mix, order so "previous" is defined, tie-breaker so it is deterministic.
- It is two steps: gap per order in a CTE, then `AVG` per customer in the outer query.
- Other engines: PostgreSQL would subtract timestamps and use `EXTRACT(EPOCH FROM ...) / 86400`; MySQL `TIMESTAMPDIFF(SECOND, ...)`; BigQuery `TIMESTAMP_DIFF` (all not executed here).

**Follow-ups:**
- *Gap in hours?* Multiply the day difference by 24 (SQL) or use `total_seconds() / 3600` (pandas).
- *Median gap rather than average?* Needs a percentile function; SQLite has no percentile function; pandas has `median()`.
- *Repeat customers only?* `HAVING COUNT(d) >= 1` on the grouped query.

**Common mistakes:**
- Computing the gap without `PARTITION BY customer_id`.
- Treating the first order's NULL gap as 0.
- Ordering by `order_id`, which is not time order.
- Using `.days` on the `Timedelta` in pandas, which drops the fractional part (the run prints 2 for a 2.5 day Timedelta).

### Q15 ⭐⭐⭐ 🟡 Running count, running average and cumulative percent of total: daily_sales(sale_date, amount). Return for each day the running count of days, the running average (AVG OVER an ordered window, which is cumulative), the running total and the cumulative percent of the grand total using SUM(amount) OVER () as the denominator. Give the pandas cumcount()+1, expanding().mean() and cumsum()/sum() versions and explain that an AVG with ORDER BY in OVER is not a plain average.
**Asked at:** StrataScratch blog 'Top five SQL window functions for data science interviews' (month-over-month change with LEAD/LAG, cumulative cost with SUM, 10-day moving average, first visit with ROW_NUMBER), a guide and not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** All four are window aggregates over the same cumulative frame (`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`) except the denominator, which is `SUM(amount) OVER ()` (whole table); `AVG(...) OVER (ORDER BY ...)` is a running average, not the plain average, because adding `ORDER BY` changes the frame.

**Schema and sample data:** six days of sales, one row per day, total 1000.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',100),('2024-01-02',50),('2024-01-03',150),
  ('2024-01-04',200),('2024-01-05',100),('2024-01-06',400);
```

**SQL answer:** I write the frame out so the intent is visible and duplicate dates cannot change it.
```sql
SELECT sale_date, amount,
       COUNT(*)    OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_days,
       ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_avg,
       SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 1.0
             / SUM(amount) OVER (), 4) AS cum_pct
FROM daily_sales
ORDER BY sale_date
```

**pandas answer:** `cumcount() + 1` needs a groupby, so I group by a constant key; `expanding().mean()` is the running average; `cumsum() / sum()` is the cumulative share.
```py
out = ds.copy()
out["running_days"] = out.assign(g=1).groupby("g").cumcount() + 1
out["running_avg"] = out["amount"].expanding().mean().round(2)
out["running_total"] = out["amount"].cumsum()
out["cum_pct"] = (out["amount"].cumsum() / out["amount"].sum()).round(4)
```

**Example:** amounts 100, 50, 150, 200, 100, 400.
- Running total: 100, 150, 300, 500, 600, 1000.
- Running average: 100/1 = 100, 150/2 = 75, 300/3 = 100, 500/4 = 125, 600/5 = 120, 1000/6 = 166.67.
- Cumulative percent of grand total 1000: 0.10, 0.15, 0.30, 0.50, 0.60, 1.00.
- Running count of days: 1 to 6.

**Code:** run with `python3 -I`.
```python
# Q15: running count, running average, running total, cumulative percent of total
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',100),('2024-01-02',50),('2024-01-03',150),
  ('2024-01-04',200),('2024-01-05',100),('2024-01-06',400);
"""
SQL_MAIN = """
SELECT sale_date, amount,
       COUNT(*)    OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_days,
       ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_avg,
       SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 1.0
             / SUM(amount) OVER (), 4) AS cum_pct
FROM daily_sales
ORDER BY sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
out = ds.copy()
out["running_days"] = out.assign(g=1).groupby("g").cumcount() + 1
out["running_avg"] = out["amount"].expanding().mean().round(2)
out["running_total"] = out["amount"].cumsum()
out["cum_pct"] = (out["amount"].cumsum() / out["amount"].sum()).round(4)
# pd:end
# compared in sale_date order (both sorted by sale_date)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)

# AVG(...) OVER (ORDER BY ...) is cumulative; AVG(...) OVER () is the plain average
plain = con.execute("SELECT AVG(amount) OVER () FROM daily_sales LIMIT 1").fetchone()[0]
cum_last = sql_df["running_avg"].iloc[-1]
print("\nplain average AVG() OVER ():", round(plain, 4), "| ordered AVG on the last row:", cum_last,
      "| ordered AVG on the first row:", sql_df["running_avg"].iloc[0])

# duplicate dates: default frame is RANGE through peers
con.executescript("""
CREATE TABLE sales_dup(id INTEGER PRIMARY KEY, sale_date TEXT, amount INTEGER);
INSERT INTO sales_dup VALUES (1,'2024-01-01',100),(2,'2024-01-02',50),(3,'2024-01-02',150),(4,'2024-01-03',200);
""")
for label, order in [("default frame, ORDER BY sale_date      ", "ORDER BY sale_date"),
                     ("ROWS frame, ORDER BY sale_date, id     ", "ORDER BY sale_date, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW")]:
    rows = con.execute(f"SELECT id, COUNT(*) OVER ({order}), SUM(amount) OVER ({order}) FROM sales_dup ORDER BY id").fetchall()
    print(label, "(id, running_count, running_sum):", rows)

# empty/zero denominator and NULL amount
con.executescript("""
CREATE TABLE zeros(d TEXT, amount INTEGER);
INSERT INTO zeros VALUES ('2024-01-01',0),('2024-01-02',0);
CREATE TABLE nulls(d TEXT, amount INTEGER);
INSERT INTO nulls VALUES ('2024-01-01',10),('2024-01-02',NULL),('2024-01-03',30);
""")
print("zero grand total, SQL cum_pct:", con.execute(
    "SELECT SUM(amount) OVER (ORDER BY d) * 1.0 / SUM(amount) OVER () FROM zeros").fetchall())
z = pd.Series([0, 0])
print("zero grand total, pandas cumsum()/sum():", (z.cumsum() / z.sum()).tolist())
print("NULL amount: COUNT(*) vs COUNT(amount) vs AVG, last row:", con.execute(
    "SELECT COUNT(*) OVER w, COUNT(amount) OVER w, AVG(amount) OVER w FROM nulls "
    "WINDOW w AS (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) ORDER BY d DESC LIMIT 1").fetchall())
n = pd.Series([10, None, 30])
print("NULL amount, pandas expanding().count() last / expanding().mean() last:",
      n.expanding().count().iloc[-1], n.expanding().mean().iloc[-1])
print("asserts passed: SQL running aggregates == pandas cumcount/expanding/cumsum")
```

**Output (my run):**
```text
 sale_date  amount  running_days  running_avg  running_total  cum_pct
2024-01-01     100             1       100.00            100     0.10
2024-01-02      50             2        75.00            150     0.15
2024-01-03     150             3       100.00            300     0.30
2024-01-04     200             4       125.00            500     0.50
2024-01-05     100             5       120.00            600     0.60
2024-01-06     400             6       166.67           1000     1.00

plain average AVG() OVER (): 166.6667 | ordered AVG on the last row: 166.67 | ordered AVG on the first row: 100.0
default frame, ORDER BY sale_date       (id, running_count, running_sum): [(1, 1, 100), (2, 3, 300), (3, 3, 300), (4, 4, 500)]
ROWS frame, ORDER BY sale_date, id      (id, running_count, running_sum): [(1, 1, 100), (2, 2, 150), (3, 3, 300), (4, 4, 500)]
zero grand total, SQL cum_pct: [(None,), (None,)]
zero grand total, pandas cumsum()/sum(): [nan, nan]
NULL amount: COUNT(*) vs COUNT(amount) vs AVG, last row: [(3, 2, 20.0)]
NULL amount, pandas expanding().count() last / expanding().mean() last: 2.0 20.0
asserts passed: SQL running aggregates == pandas cumcount/expanding/cumsum
```

**Edge cases:**
- Duplicate dates: with only `ORDER BY sale_date` and no frame, the default is `RANGE UNBOUNDED PRECEDING` through the last peer, so rows with the same date are included together. In my duplicate test (two rows on 01-02, ids 2 and 3) the default frame gave running counts 1, 3, 3, 4 and running sums 100, 300, 300, 500, so both peers showed the same total; `ORDER BY sale_date, id ROWS ...` gave 1, 2, 3, 4 and 100, 150, 300, 500. In this question's table the date is the primary key, so both agree, but I still write ROWS and a unique order.
- Zero grand total: the SQL divides by 0 and SQLite returns NULL (output shows `None`); pandas `0 / 0` gives NaN. A non-zero numerator over a zero total would be `inf` in pandas; other SQL engines may raise a division error (not executed here), so guard with `NULLIF(total, 0)`.
- NULL amount: the running count of days (`COUNT(*)`) still counts that day, but `COUNT(amount)` and `AVG` do not. In my test `[10, NULL, 30]` gave COUNT(*) 3, COUNT(amount) 2 and average 20.0 on the last row; pandas `expanding().count()` gave 2.0 and `expanding().mean()` 20.0 (both skip NaN). `cumcount() + 1` counts the NaN row, like `COUNT(*)`.
- Empty table: no rows, no output.

**Then explain:**
- `AVG(x) OVER ()` is the plain average of the whole table (one number repeated on every row). `AVG(x) OVER (ORDER BY d)` is the average from the first row to this row; it is the same number as the plain average only on the last row (166.67 and 166.6667 in the output).
- The denominator `SUM(amount) OVER ()` has no `ORDER BY`, so its frame is the whole partition: one grand total repeated on every row. That is how a window function gives "share of total" without a self-join.
- pandas: `expanding()` is the pandas name for the cumulative frame; `cumsum() / sum()` is the vectorised share. I rounded both sides to 4 places before asserting equality.
- Percent versus fraction: I return a fraction (0.10); multiply by 100 for a percentage.

**Follow-ups:**
- *Running average over the last 3 days only?* Change the frame (Q8).
- *Percent of total per month or per category?* Add `PARTITION BY` to the denominator window.
- *Why not `AVG(amount) OVER (ORDER BY d)` with no ROWS?* It works when dates are unique; with duplicates the default RANGE frame gives peers the same value.

**Common mistakes:**
- Thinking `AVG() OVER (ORDER BY ...)` is the overall average.
- Putting `ORDER BY` inside the denominator window, turning the "grand total" into another running total.
- Integer division: `SUM(amount) / SUM(amount) OVER ()` on two integers can truncate to 0; I multiplied by 1.0 to avoid it (how other engines behave is not executed here).
- Forgetting the `ORDER BY` on the outer query: window order and output order are separate.

### Q16 ⭐⭐⭐ 🟡 Month-over-month change with a missing month: monthly_revenue(month, revenue) where one month (for example March) has no row. Show that LAG(revenue) then compares April with February, explain why, and fix it by building a complete month calendar (a recursive CTE or a month table), LEFT JOIN the revenue, and COALESCE missing months to 0 or leave NULL as a deliberate choice. Give the pandas resample('MS') or reindex version and state what the percent change for the month after a zero month should be.
**Asked at:** LearnSQL revenue-growth and Craig Kerstiens month-over-month blog write-ups (LAG, percent change, gaps break LAG, divide by zero), guides and not candidate reports; analyst screens at product companies and startups
**Say this first (1 line):** `LAG` returns the previous row that exists, so with March missing it compares April with February and calls it month-over-month; build a full month calendar (recursive CTE), LEFT JOIN the revenue, and decide on purpose whether a missing month is NULL (unknown) or 0 (no sales).

**Schema and sample data:** four months, March has no row. Months are stored as first-of-month dates so both SQLite `date()` and pandas `resample('MS')` can use them.
```sql
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES ('2024-01-01',100),('2024-02-01',120),('2024-04-01',150),('2024-05-01',165);
```

**SQL answer:** the naive LAG, then the calendar version that leaves March NULL (`SQL_MAIN`), then the version that turns missing months into 0 (`SQL_ZERO`; it is `SQL_MAIN` with the line `SELECT c.month, r.revenue` replaced by `SELECT c.month, COALESCE(r.revenue, 0) AS revenue`, which is exactly what the Code block does).
```sql
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / LAG(revenue) OVER (ORDER BY month), 2) AS mom_pct
FROM monthly_revenue
ORDER BY month
```
```sql
WITH RECURSIVE cal(month) AS (
  SELECT MIN(month) FROM monthly_revenue
  UNION ALL
  SELECT date(month, '+1 month') FROM cal WHERE month < (SELECT MAX(month) FROM monthly_revenue)
), filled AS (
  SELECT c.month, r.revenue
  FROM cal c LEFT JOIN monthly_revenue r ON r.month = c.month
)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) AS mom_pct
FROM filled
ORDER BY month
```

**pandas answer:** `asfreq("MS")` creates the missing month as NaN; `pct_change()` then leaves NaN around it. For the zero version, `fillna(0)` and replace the infinity with NaN.
```py
s = mr.assign(month=pd.to_datetime(mr["month"])).set_index("month")["revenue"]
full = s.asfreq("MS")                       # complete month calendar, missing months become NaN
pd_null = (full.pct_change() * 100).round(2)
zero = full.fillna(0)
pd_zero = (zero.pct_change() * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
```

**Example:** revenue Jan 100, Feb 120, Apr 150, May 165.
- Naive LAG: Apr is compared with Feb, giving +25.0%; this is a two-month change shown as a month-over-month number. There is no March row at all, so nobody can see the problem.
- Calendar, March NULL: Mar = NULL, growth Mar = NULL (no revenue to compare), Apr = NULL (no previous month value), May = (165 - 150) / 150 = +10.0%.
- Calendar, March = 0: Mar = (0 - 120) / 120 = -100.0%, Apr = NULL because the base is 0 (`NULLIF` avoids dividing by zero), May = +10.0%.

**Code:** run with `python3 -I`.
```python
# Q16: month-over-month change when a month has no row
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES ('2024-01-01',100),('2024-02-01',120),('2024-04-01',150),('2024-05-01',165);
"""
SQL_NAIVE = """
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / LAG(revenue) OVER (ORDER BY month), 2) AS mom_pct
FROM monthly_revenue
ORDER BY month
"""
SQL_MAIN = """
WITH RECURSIVE cal(month) AS (
  SELECT MIN(month) FROM monthly_revenue
  UNION ALL
  SELECT date(month, '+1 month') FROM cal WHERE month < (SELECT MAX(month) FROM monthly_revenue)
), filled AS (
  SELECT c.month, r.revenue
  FROM cal c LEFT JOIN monthly_revenue r ON r.month = c.month
)
SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) AS mom_pct
FROM filled
ORDER BY month
"""
SQL_ZERO = SQL_MAIN.replace("SELECT c.month, r.revenue", "SELECT c.month, COALESCE(r.revenue, 0) AS revenue")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
naive = pd.read_sql_query(SQL_NAIVE, con)
sql_null = pd.read_sql_query(SQL_MAIN, con)
sql_zero = pd.read_sql_query(SQL_ZERO, con)
print("naive LAG on the table with a missing row:"); print(naive.to_string(index=False))
print("\ncalendar + LEFT JOIN, March left NULL:"); print(sql_null.to_string(index=False))
print("\ncalendar + COALESCE(revenue, 0), NULLIF on the divisor:"); print(sql_zero.to_string(index=False))

mr = pd.read_sql_query("SELECT * FROM monthly_revenue", con)
# pd:main
s = mr.assign(month=pd.to_datetime(mr["month"])).set_index("month")["revenue"]
full = s.asfreq("MS")                       # complete month calendar, missing months become NaN
pd_null = (full.pct_change() * 100).round(2)
zero = full.fillna(0)
pd_zero = (zero.pct_change() * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
# pd:end
# compared in month order
pd.testing.assert_series_equal(pd_null.reset_index(drop=True), sql_null["mom_pct"], check_names=False, check_dtype=False)
pd.testing.assert_series_equal(pd_zero.reset_index(drop=True), sql_zero["mom_pct"], check_names=False, check_dtype=False)
print("\npandas asfreq('MS') + pct_change (NaN kept):", pd_null.tolist())
print("pandas fillna(0).pct_change() raw (before replacing inf):", (zero.pct_change() * 100).round(2).tolist())

# alternatives and pitfalls
print("\nresample('MS').sum() turns the missing month into", s.resample("MS").sum().loc["2024-03-01"],
      "| resample('MS').mean() gives", s.resample("MS").mean().loc["2024-03-01"])
print("reindex(pd.date_range(..., freq='MS')) equals asfreq:",
      s.reindex(pd.date_range(s.index.min(), s.index.max(), freq="MS")).equals(full))
print("pct_change() on the table WITHOUT the calendar (pandas, same mistake as SQL LAG):",
      (s.pct_change() * 100).round(2).tolist())
try:
    full.pct_change(fill_method="ffill")
except Exception as e:
    print("pct_change(fill_method='ffill') in this pandas:", type(e).__name__, "-", e)
print("asserts passed: SQL calendar versions == pandas asfreq versions")
```

**Output (my run):**
```text
naive LAG on the table with a missing row:
     month  revenue  prev_rev  mom_pct
2024-01-01      100       NaN      NaN
2024-02-01      120     100.0     20.0
2024-04-01      150     120.0     25.0
2024-05-01      165     150.0     10.0

calendar + LEFT JOIN, March left NULL:
     month  revenue  prev_rev  mom_pct
2024-01-01    100.0       NaN      NaN
2024-02-01    120.0     100.0     20.0
2024-03-01      NaN     120.0      NaN
2024-04-01    150.0       NaN      NaN
2024-05-01    165.0     150.0     10.0

calendar + COALESCE(revenue, 0), NULLIF on the divisor:
     month  revenue  prev_rev  mom_pct
2024-01-01      100       NaN      NaN
2024-02-01      120     100.0     20.0
2024-03-01        0     120.0   -100.0
2024-04-01      150       0.0      NaN
2024-05-01      165     150.0     10.0

pandas asfreq('MS') + pct_change (NaN kept): [nan, 20.0, nan, nan, 10.0]
pandas fillna(0).pct_change() raw (before replacing inf): [nan, 20.0, -100.0, inf, 10.0]

resample('MS').sum() turns the missing month into 0 | resample('MS').mean() gives nan
reindex(pd.date_range(..., freq='MS')) equals asfreq: True
pct_change() on the table WITHOUT the calendar (pandas, same mistake as SQL LAG): [nan, 20.0, 25.0, 10.0]
pct_change(fill_method='ffill') in this pandas: ValueError - fill_method must be None; got fill_method='ffill'.
asserts passed: SQL calendar versions == pandas asfreq versions
```

**Edge cases:**
- Percent change after a zero month: undefined (divide by zero). I return NULL; pandas gives `inf` (shown in the output as the raw `fillna(0).pct_change()`), which I replaced with NaN to match. Do not show `inf` or a huge number on a dashboard; say "n/a" or "new".
- NULL versus 0 for the missing month is a business decision: no row because the store was closed (NULL) is different from no sales (0). I show both and let the question decide.
- Several missing months in a row: the calendar handles it; the NULL months then propagate as shown.
- Duplicate month rows: the primary key in this table prevents them; without it, aggregate to one row per month before the calendar join.
- `resample("MS").sum()` turns a missing month into 0 silently (output: 0), while `resample("MS").mean()` gives NaN. Use `asfreq` or `reindex` if you want NaN, and `.sum()` only if 0 is the intended answer.
- `pct_change` in this pandas (3.0.5): NaN is not forward-filled by default (April stayed NaN), and passing `fill_method="ffill"` raised `ValueError: fill_method must be None`. Older pandas filled NaN forward by default (from memory of the deprecation, not executed here).

**Then explain:**
- Why LAG fails: it is positional. A gap in the data is invisible to it.
- The recursive CTE generates one row per month from the minimum to the maximum month with `date(month, '+1 month')`. Other engines have `generate_series` (PostgreSQL), `GENERATE_DATE_ARRAY` (BigQuery) or a calendar table (not executed here).
- A permanent calendar table is the usual choice in a warehouse: you join to it for every report.
- pandas `reindex(pd.date_range(min, max, freq="MS"))` and `asfreq("MS")` gave the same result in my run.

**Follow-ups:**
- *Same for days or weeks?* Same pattern with a daily calendar.
- *Should the missing month be forward-filled with February's revenue?* Only for stock-like values (balance, price), not for flows like revenue.
- *Year-over-year with missing months?* Q23.

**Common mistakes:**
- Trusting LAG on gappy data.
- `COALESCE` to 0 and then dividing by it.
- Using `resample().sum()` and not realising it invented zeros.
- Calendar built from the data's own months (no help: the missing month must come from the calendar, not from the table).

### Q17 ⭐⭐⭐ 🟡 Running Total for Different Genders (LeetCode 1308 style): Scores(player_name, gender, day, score_points) with PRIMARY KEY (gender, day). Return gender, day and the running total of score_points per gender ordered by day, ordered by gender and day. Explain PARTITION BY gender versus ORDER BY day, and give the pandas groupby('gender')['score_points'].cumsum().
**Asked at:** public LeetCode-style problem bank (1321 Restaurant Growth statement seen in a search snippet; 1308 Running Total for Different Genders, 197 Rising Temperature and 180 Consecutive Numbers known only by title from third-party lists), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** `SUM(score_points) OVER (PARTITION BY gender ORDER BY day)`: `PARTITION BY gender` restarts the total for each gender, `ORDER BY day` makes it cumulative inside each gender; the final `ORDER BY gender, day` is a separate clause for the output.

**Schema and sample data:** seven scores, four for M and three for F, primary key `(gender, day)` so a gender never has two rows on the same day. The sample is not the LeetCode example data; the table shape follows the problem title.
```sql
CREATE TABLE Scores(player_name TEXT, gender TEXT, day TEXT, score_points INTEGER, PRIMARY KEY (gender, day));
INSERT INTO Scores VALUES ('Aron','F','2020-01-01',17),('Alice','F','2020-01-07',23),
  ('Cy','F','2020-01-10',5),('Joe','M','2019-12-18',2),('Bajrang','M','2019-12-25',7),
  ('Khali','M','2019-12-30',11),('Slaman','M','2019-12-31',13);
```

**SQL answer:** two broken variants are in the Code block for contrast.
```sql
SELECT gender, day,
       SUM(score_points) OVER (PARTITION BY gender ORDER BY day
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total
FROM Scores
ORDER BY gender, day
```

**pandas answer:** sort by gender and day, then `groupby('gender')['score_points'].cumsum()`.
```py
s = scores.sort_values(["gender", "day"])
s["total"] = s.groupby("gender")["score_points"].cumsum()
pd_df = s[["gender", "day", "total"]]
```

**Example:**
- F: 17 on 01-01, then 17 + 23 = 40 on 01-07, then 40 + 5 = 45 on 01-10.
- M: 2, 2 + 7 = 9, 9 + 11 = 20, 20 + 13 = 33.
- The two genders never mix: F restarts at its own first row.

**Code:** run with `python3 -I`.
```python
# Q17: running total per gender (LeetCode 1308 style)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE Scores(player_name TEXT, gender TEXT, day TEXT, score_points INTEGER, PRIMARY KEY (gender, day));
INSERT INTO Scores VALUES ('Aron','F','2020-01-01',17),('Alice','F','2020-01-07',23),
  ('Cy','F','2020-01-10',5),('Joe','M','2019-12-18',2),('Bajrang','M','2019-12-25',7),
  ('Khali','M','2019-12-30',11),('Slaman','M','2019-12-31',13);
"""
SQL_MAIN = """
SELECT gender, day,
       SUM(score_points) OVER (PARTITION BY gender ORDER BY day
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total
FROM Scores
ORDER BY gender, day
"""
SQL_NO_ORDER = """
SELECT gender, day, SUM(score_points) OVER (PARTITION BY gender) AS total
FROM Scores ORDER BY gender, day
"""
SQL_NO_PARTITION = """
SELECT gender, day, SUM(score_points) OVER (ORDER BY day) AS total
FROM Scores ORDER BY gender, day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nPARTITION BY gender, no ORDER BY (whole-partition total on every row):",
      [r[2] for r in con.execute(SQL_NO_ORDER)])
print("ORDER BY day, no PARTITION BY (genders mixed together):",
      [(r[0], r[2]) for r in con.execute(SQL_NO_PARTITION)])

scores = pd.read_sql_query("SELECT * FROM Scores", con)
# pd:main
s = scores.sort_values(["gender", "day"])
s["total"] = s.groupby("gender")["score_points"].cumsum()
pd_df = s[["gender", "day", "total"]]
# pd:end
# compared after sorting by gender, day
pd.testing.assert_frame_equal(sql_df, pd_df.reset_index(drop=True), check_dtype=False)

# without the sort, groupby().cumsum() follows the physical row order (here: rows reversed)
rev = scores.iloc[::-1]
unsorted = rev.assign(total=rev.groupby("gender")["score_points"].cumsum())
print("\npandas cumsum on a reversed, unsorted frame, M rows (day, total):",
      unsorted.loc[unsorted["gender"] == "M", ["day", "total"]].values.tolist())
print("asserts passed: SQL PARTITION BY/ORDER BY == pandas sort + groupby().cumsum()")
```

**Output (my run):**
```text
gender        day  total
     F 2020-01-01     17
     F 2020-01-07     40
     F 2020-01-10     45
     M 2019-12-18      2
     M 2019-12-25      9
     M 2019-12-30     20
     M 2019-12-31     33

PARTITION BY gender, no ORDER BY (whole-partition total on every row): [45, 45, 45, 33, 33, 33, 33]
ORDER BY day, no PARTITION BY (genders mixed together): [('F', 50), ('F', 73), ('F', 78), ('M', 2), ('M', 9), ('M', 20), ('M', 33)]

pandas cumsum on a reversed, unsorted frame, M rows (day, total): [['2019-12-31', 13], ['2019-12-30', 24], ['2019-12-25', 31], ['2019-12-18', 33]]
asserts passed: SQL PARTITION BY/ORDER BY == pandas sort + groupby().cumsum()
```

**Edge cases:**
- Ties: none possible, because `(gender, day)` is the primary key. If the key allowed two rows per gender-day, the default frame would give both rows the same total; add a tie-breaker and `ROWS` in that case (I tested this effect in Q15).
- Missing `ORDER BY`: every row gets the partition total (45 for all F rows, 33 for all M rows in my run), a non-running number.
- Missing `PARTITION BY`: one running total across both genders ordered by day (in the output the F rows show 50, 73 and 78, because the earlier M days, which total 33, were already added).
- NULL `score_points`: SQL `SUM` ignores NULL and the total carries on; pandas `cumsum()` leaves NaN at that row (details in Q18). The sample has no NULLs.
- Empty gender group: cannot appear; a gender with no rows has no output rows.
- pandas without the sort: `cumsum` follows physical row order. On a reversed copy of the frame the M totals came out 13, 24, 31, 33 instead of 2, 9, 20, 33.

**Then explain:**
- `PARTITION BY` is like `GROUP BY` for windows without collapsing rows: separate running totals per group.
- `ORDER BY` inside `OVER` defines the order of accumulation. `ORDER BY` at the end of the query only defines the order of the result.
- pandas `groupby(...).cumsum()` is the same idea; unlike SQL it does not take an order, so sort first.

**Follow-ups:**
- *Total across both genders too?* A second window with no partition (`SUM(...) OVER (ORDER BY day)`), as in the broken variant; here it is shown to be the wrong answer to this question but the right one for an overall total.
- *Percent of the gender's final total?* Divide by `SUM(...) OVER (PARTITION BY gender)`.
- *Only players on the same team?* Add the team column to `PARTITION BY`.

**Common mistakes:**
- Leaving out `PARTITION BY`, mixing genders.
- Leaving out `ORDER BY` in `OVER`, getting a partition total on every row.
- Ordering the final result only by `day`, when the problem asks for gender then day.
- Forgetting to sort in pandas before `cumsum`.

### Q18 ⭐⭐⭐ 🟡 SQL versus pandas NaN and NULL in running totals and lag: a series with a missing value (amount NULL on one day). Show SUM(amount) OVER (ORDER BY day) (NULL ignored, total carries on), COUNT(amount) versus COUNT(*) as a running count, then pandas cumsum() (skipna=True keeps NaN at that position but continues the sum) and cumsum(skipna=False), and shift() turning integer columns into float64 unless fill_value is passed. Run both and assert where they match.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** SQL aggregates skip NULL, so `SUM(amount) OVER (ORDER BY day)` carries the total across the missing day, and `COUNT(amount)` is one lower than `COUNT(*)` from then on; pandas `cumsum()` also skips NaN but leaves NaN in that row's own output, so `cumsum().ffill()` is what matches SQL, while `cumsum(skipna=False)` turns everything after the NaN into NaN.

**Schema and sample data:** five days, day 3 has a NULL amount.
```sql
CREATE TABLE s(day INTEGER PRIMARY KEY, amount INTEGER);
INSERT INTO s VALUES (1,10),(2,20),(3,NULL),(4,40),(5,50);
```

**SQL answer:**
```sql
SELECT day, amount,
       SUM(amount)   OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_sum,
       COUNT(*)      OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_rows,
       COUNT(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_nonnull,
       LAG(amount)   OVER (ORDER BY day) AS prev_amount
FROM s
ORDER BY day
```

**pandas answer:** `read_sql_query` returns the NULL as NaN in a float64 column, so the integer amounts arrive as floats.
```py
a = s["amount"]                                   # float64: NULL arrives as NaN
out = pd.DataFrame({"day": s["day"], "amount": a})
out["running_sum"] = a.cumsum().ffill()           # cumsum() keeps NaN at the NaN row; ffill restores SQL's carried total
out["n_rows"] = range(1, len(a) + 1)
out["n_nonnull"] = a.notna().cumsum()
out["prev_amount"] = a.shift()
```

**Example:** amounts 10, 20, NULL, 40, 50.
- SQL running sum: 10, 30, 30 (NULL adds nothing), 70, 120. `COUNT(*)`: 1 to 5. `COUNT(amount)`: 1, 2, 2, 3, 4. `LAG(amount)`: NULL, 10, 20, NULL (day 3 was NULL), 40.
- pandas `cumsum()`: 10, 30, NaN, 70, 120: the sum continues, but the NaN row shows NaN. `cumsum(skipna=False)`: 10, 30, NaN, NaN, NaN: NaN is sticky.
- `cumsum().ffill()` gives 10, 30, 30, 70, 120, the same as SQL. `fillna(0).cumsum()` gives the same numbers here too.

**Code:** run with `python3 -I`.
```python
# Q18: NULL versus NaN in running totals, running counts and lag
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE s(day INTEGER PRIMARY KEY, amount INTEGER);
INSERT INTO s VALUES (1,10),(2,20),(3,NULL),(4,40),(5,50);
"""
SQL_MAIN = """
SELECT day, amount,
       SUM(amount)   OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_sum,
       COUNT(*)      OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_rows,
       COUNT(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS n_nonnull,
       LAG(amount)   OVER (ORDER BY day) AS prev_amount
FROM s
ORDER BY day
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

s = pd.read_sql_query("SELECT * FROM s ORDER BY day", con)
# pd:main
a = s["amount"]                                   # float64: NULL arrives as NaN
out = pd.DataFrame({"day": s["day"], "amount": a})
out["running_sum"] = a.cumsum().ffill()           # cumsum() keeps NaN at the NaN row; ffill restores SQL's carried total
out["n_rows"] = range(1, len(a) + 1)
out["n_nonnull"] = a.notna().cumsum()
out["prev_amount"] = a.shift()
# pd:end
# compared in day order (both ordered by day)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)

print("\npandas cumsum()              :", a.cumsum().tolist())
print("pandas cumsum(skipna=False)  :", a.cumsum(skipna=False).tolist())
print("pandas cumsum().ffill()      :", a.cumsum().ffill().tolist(), "(matches SQL SUM OVER)")
print("pandas fillna(0).cumsum()    :", a.fillna(0).cumsum().tolist())

# nullable dtypes (verified here on pandas 3.0.5)
n = pd.Series([1, None, 3], dtype="Int64")
print("\nInt64 cumsum()               :", n.cumsum().tolist(), "dtype", n.cumsum().dtype)
print("Int64 cumsum(skipna=False)   :", n.cumsum(skipna=False).tolist())
print("Int64 shift()                :", n.shift().tolist(), "dtype", n.shift().dtype)

# shift and dtype
ints = pd.Series([5, 6, 7])
print("\nint64 .shift() dtype         :", ints.shift().dtype, ints.shift().tolist())
print("int64 .shift(fill_value=0)   :", ints.shift(fill_value=0).dtype, ints.shift(fill_value=0).tolist())
print("SQL LAG(amount, 1, 0) day 1  :", con.execute("SELECT LAG(amount, 1, 0) OVER (ORDER BY day) FROM s ORDER BY day LIMIT 1").fetchone()[0])

# NULL in the first row: SQL SUM gives NULL until the first non-NULL value; pandas gives NaN
con.executescript("CREATE TABLE f(day INTEGER, amount INTEGER); INSERT INTO f VALUES (1,NULL),(2,5),(3,NULL);")
print("\nfirst-row NULL, SQL running sum :", [r[0] for r in con.execute(
    "SELECT SUM(amount) OVER (ORDER BY day) FROM f ORDER BY day")])
fa = pd.Series([None, 5, None], dtype="float64")
print("first-row NULL, pandas cumsum().ffill():", fa.cumsum().ffill().tolist())
print("asserts passed: SQL window == pandas cumsum().ffill(), notna().cumsum(), shift()")
```

**Output (my run):**
```text
 day  amount  running_sum  n_rows  n_nonnull  prev_amount
   1    10.0           10       1          1          NaN
   2    20.0           30       2          2         10.0
   3     NaN           30       3          2         20.0
   4    40.0           70       4          3          NaN
   5    50.0          120       5          4         40.0

pandas cumsum()              : [10.0, 30.0, nan, 70.0, 120.0]
pandas cumsum(skipna=False)  : [10.0, 30.0, nan, nan, nan]
pandas cumsum().ffill()      : [10.0, 30.0, 30.0, 70.0, 120.0] (matches SQL SUM OVER)
pandas fillna(0).cumsum()    : [10.0, 30.0, 30.0, 70.0, 120.0]

Int64 cumsum()               : [1, <NA>, 4] dtype Int64
Int64 cumsum(skipna=False)   : [1, <NA>, <NA>]
Int64 shift()                : [<NA>, 1, <NA>] dtype Int64

int64 .shift() dtype         : float64 [nan, 5.0, 6.0]
int64 .shift(fill_value=0)   : int64 [0, 5, 6]
SQL LAG(amount, 1, 0) day 1  : 0

first-row NULL, SQL running sum : [None, 5, 5]
first-row NULL, pandas cumsum().ffill(): [nan, 5.0, 5.0]
asserts passed: SQL window == pandas cumsum().ffill(), notna().cumsum(), shift()
```

**Edge cases:**
- Where they match: the SQL running sum equals pandas `cumsum().ffill()` on every row of my sample; SQL `COUNT(amount)` equals `notna().cumsum()`; SQL `LAG` equals `shift()` (NULL versus NaN); the asserts check all four. Where they differ before the fix: SQL shows 30 on the NULL day, plain `cumsum()` shows NaN.
- NULL in the first row: SQL `SUM` is NULL until the first non-NULL value (output: None, 5, 5); `cumsum().ffill()` gives NaN, 5.0, 5.0. A fully NULL partition in SQL gives NULL, not 0, whereas `fillna(0).cumsum()` would give 0, so the two zero-based versions differ in that corner.
- `shift()` and dtype: an int64 column becomes float64 after `shift()` because NaN needs a float; `shift(fill_value=0)` keeps int64. SQL `LAG(amount, 1, 0)` gives 0 on the first row, the same idea.
- Nullable dtypes: on pandas 3.0.5 an `Int64` series `[1, <NA>, 3]` gave `cumsum()` = `[1, <NA>, 4]` (dtype stays `Int64`), `cumsum(skipna=False)` = `[1, <NA>, <NA>]`, and `shift()` kept `Int64`, with `<NA>` in the first slot. So with nullable integers you keep integers and avoid the float conversion.
- Running count of rows: `COUNT(*)` counts the NULL row; `COUNT(amount)` does not. For "average so far", `AVG` uses the non-NULL count (Q15).
- Duplicate days: `day` is the primary key here. With duplicate days, add a tie-breaker and `ROWS` (Q15).

**Then explain:**
- NULL means unknown. SQL aggregates ignore it because it is not a number to add; they never invent a zero.
- pandas has two NA flavours: NaN in float64 columns, `pd.NA` in nullable dtypes. Both are skipped by default (`skipna=True`).
- `skipna=True` still keeps the NaN in its own position: it only means the running sum ignores it, not that the position is filled.
- Which to choose is a business question: treat missing as zero (`fillna(0)`), carry forward (`ffill`), or keep unknown (`skipna=False`).

**Follow-ups:**
- *How would you make SQL behave like `skipna=False`?* A running flag (`MAX(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)` over the same frame) and return NULL once it is 1; I did not run this one.
- *And `COALESCE(amount, 0)`?* Then the NULL day counts as a real zero for averages and counts.
- *Why did `shift()` change my integer column to float?* Because NaN cannot live in int64; use `fill_value` or `Int64`.

**Common mistakes:**
- Assuming `cumsum()` fills the NaN row.
- Comparing the SQL and pandas results with `==` on NaN (NaN is not equal to NaN; use `assert_frame_equal`).
- Using `COUNT(*)` when you mean the number of non-NULL values.
- Not noticing the dtype switch to float64 after `shift()` and then writing it back to an integer column.

### Q19 ⭐⭐ 🟢 NTH_VALUE and the second order per customer: orders(order_id, customer_id, order_date, amount). Return each customer's second order amount with NTH_VALUE(amount, 2) over a full-partition frame, explain that the answer is NULL when the customer has fewer than two orders and that the default frame also changes the result for the first row, and give the pandas groupby().nth(1) or iloc version. Mention that FROM LAST and IGNORE NULLS are not available in SQLite and PostgreSQL does not implement them.
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `NTH_VALUE(amount, 2)` returns the second row's value of the window frame, so it needs `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to see the whole partition; with the default frame the first row gets NULL, and a customer with fewer than two orders gets NULL everywhere.

**Schema and sample data:** four customers. Customer 1 has three orders, customer 2 has one, customer 3 has two orders on the same date, customer 4's second order has a NULL amount.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-01',100),(2,1,'2024-01-05',150),(3,1,'2024-01-09',90),
  (4,2,'2024-01-02',70),
  (5,3,'2024-01-03',40),(6,3,'2024-01-03',60),(7,3,'2024-01-10',80),
  (8,4,'2024-02-01',30),(9,4,'2024-02-02',NULL),(10,4,'2024-02-03',55);
```

**SQL answer:** tie rule: `order_date, order_id`. `DISTINCT` collapses the repeated per-row value to one row per customer.
```sql
WITH n AS (
  SELECT customer_id,
         NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id
                                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_amount
  FROM orders
)
SELECT DISTINCT customer_id, second_amount FROM n ORDER BY customer_id
```
```sql
SELECT order_id, customer_id,
       NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS second_default_frame
FROM orders WHERE customer_id = 1 ORDER BY order_date, order_id
```

**pandas answer:** `groupby().nth(1)` takes the second row of each group (0-based), but only for groups that have one, so reindex to bring back the short groups.
```py
o = orders.sort_values(["customer_id", "order_date", "order_id"])
nth = o.groupby("customer_id")["amount"].nth(1)          # rows only for customers with 2+ orders
second = (o.loc[nth.index].set_index("customer_id")["amount"]
            .reindex(sorted(orders["customer_id"].unique())))   # bring back customers with one order
pd_df = second.rename("second_amount").reset_index()
```

**Example:**
- Customer 1: amounts in date order 100, 150, 90, second is 150.
- Customer 2: one order, so there is no second one: NULL.
- Customer 3: two orders on 01-03 (ids 5 and 6) then 01-10. Tie-breaker `order_id` puts 40 first and 60 second, so the answer is 60. Without the tie-breaker the engine could return 40 or 60 for the second slot.
- Customer 4: the second row is the NULL amount, so the answer is NULL (the 55 is the third value, not the second non-NULL one).
- Default frame for customer 1, row by row: NULL, 150, 150. The first row cannot see its own second row yet.

**Code:** run with `python3 -I`.
```python
# Q19: NTH_VALUE and the second order per customer
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-01',100),(2,1,'2024-01-05',150),(3,1,'2024-01-09',90),
  (4,2,'2024-01-02',70),
  (5,3,'2024-01-03',40),(6,3,'2024-01-03',60),(7,3,'2024-01-10',80),
  (8,4,'2024-02-01',30),(9,4,'2024-02-02',NULL),(10,4,'2024-02-03',55);
"""
SQL_MAIN = """
WITH n AS (
  SELECT customer_id,
         NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id
                                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_amount
  FROM orders
)
SELECT DISTINCT customer_id, second_amount FROM n ORDER BY customer_id
"""
SQL_DEFAULT = """
SELECT order_id, customer_id,
       NTH_VALUE(amount, 2) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS second_default_frame
FROM orders WHERE customer_id = 1 ORDER BY order_date, order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\ndefault frame, customer 1 (row by row):", con.execute(SQL_DEFAULT).fetchall())

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.sort_values(["customer_id", "order_date", "order_id"])
nth = o.groupby("customer_id")["amount"].nth(1)          # rows only for customers with 2+ orders
second = (o.loc[nth.index].set_index("customer_id")["amount"]
            .reindex(sorted(orders["customer_id"].unique())))   # bring back customers with one order
pd_df = second.rename("second_amount").reset_index()
# pd:end
# compared after sorting by customer_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\npandas nth(1) returned original row labels:", nth.index.tolist(), "-> customer 2 is missing from nth")

# iloc version: explicit about the short group
iloc = o.groupby("customer_id")["amount"].apply(lambda g: g.iloc[1] if len(g) > 1 else float("nan"))
pd.testing.assert_series_equal(iloc.reset_index(drop=True), pd_df["second_amount"], check_names=False, check_dtype=False)
print("pandas groupby.apply(iloc[1]) :", iloc.tolist())

# NTH_VALUE and nth(1) both count the NULL row; they do not skip it
print("customer 4 second order amount is NULL, not 55 (SQL):", sql_df.loc[sql_df["customer_id"] == 4, "second_amount"].tolist())

# not available in SQLite 3.45
for label, sql in [("FROM LAST", "SELECT NTH_VALUE(amount,2) FROM LAST OVER (ORDER BY order_id) FROM orders"),
                   ("IGNORE NULLS", "SELECT NTH_VALUE(amount,2) IGNORE NULLS OVER (ORDER BY order_id) FROM orders")]:
    try:
        con.execute(sql).fetchall()
        print(label, "ran")
    except Exception as e:
        print(label, "->", type(e).__name__, e)
print("asserts passed: SQL NTH_VALUE == pandas groupby().nth(1) after reindex == iloc[1]")
```

**Output (my run):**
```text
 customer_id  second_amount
           1          150.0
           2            NaN
           3           60.0
           4            NaN

default frame, customer 1 (row by row): [(1, 1, None), (2, 1, 150), (3, 1, 150)]

pandas nth(1) returned original row labels: [1, 5, 8] -> customer 2 is missing from nth
pandas groupby.apply(iloc[1]) : [150.0, nan, 60.0, nan]
customer 4 second order amount is NULL, not 55 (SQL): [nan]
FROM LAST -> OperationalError near "(": syntax error
IGNORE NULLS -> OperationalError near "NULLS": syntax error
asserts passed: SQL NTH_VALUE == pandas groupby().nth(1) after reindex == iloc[1]
```

**Edge cases:**
- Fewer than two orders: NULL in SQL; `nth(1)` simply has no row for that group (customer 2 is missing from the labels `[1, 5, 8]`), so reindexing creates NaN. The `iloc[1]` version needs an explicit length check.
- NULL second value: `NTH_VALUE` counts rows, it does not skip NULLs, so customer 4 gives NULL. `nth(1)` in pandas 3.0.5 also kept the NaN row (label 8 is in the `nth` output labels), unlike `first()` which skips NaN. SQLite has no `IGNORE NULLS`: my run gave `syntax error near "NULLS"`; `FROM LAST` also gave a syntax error. PostgreSQL does not implement either (per the Wave A sources note on the PostgreSQL documentation; I did not run PostgreSQL); some other engines do (not executed here).
- Ties on `order_date`: customer 3, handled by `order_id`.
- pandas `nth` return shape: in this version it returns rows labelled by the original index (the output's `[1, 5, 8]`), like a filter, not a frame indexed by group key, so I looked the rows up with `loc` and set the index to `customer_id`. This is the behaviour I observed on pandas 3.0.5; older versions returned a different index (from memory, not executed).

**Then explain:**
- Frame matters because `NTH_VALUE` looks inside the frame, not the partition. The default frame with `ORDER BY` ends at the current row (including peers), so early rows cannot see later values.
- `DISTINCT` is a shortcut because the value is identical on every row of a customer when the frame is the whole partition. Alternatives: `ROW_NUMBER() = 2` in a CTE (Part 4) or a correlated subquery.
- pandas: `nth(1)` is 0-based; SQL's `NTH_VALUE(x, 2)` is 1-based. `iloc[1]` is the same 0-based position.

**Follow-ups:**
- *Second-highest instead of second-earliest?* Order by amount descending (Part 4, ranking; ties then matter).
- *Last value?* Use `LAST_VALUE` with the full frame or `ORDER BY ... DESC` and `FIRST_VALUE`; SQLite has no `FROM LAST`.
- *Why NULL for customer 2 and not an error?* The function returns NULL when the frame has fewer rows than N.

**Common mistakes:**
- Forgetting the frame and getting NULL on the first row.
- Treating `NTH_VALUE(x, 2)` as 0-based.
- Not breaking date ties, so the "second" order changes between runs.
- Using `nth(1)` and not noticing that short groups disappear from the output.

### Q20 ⭐⭐ 🟢 Running max and running min, and drawdown: stock_prices(trade_date, close_price). Return each day's running maximum close (all-time high so far), the running minimum, and the drawdown from the running high as close / running_max - 1. Give pandas cummax(), cummin() and the drawdown calculation, and explain why an ordered MAX OVER is cumulative.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `MAX(close) OVER (ORDER BY date)` is a running maximum because the ordered window is cumulative, `MIN` likewise, and drawdown is `close / running_max - 1`, which is 0 at a new high and negative below it; pandas has `cummax()` and `cummin()`.

**Schema and sample data:** seven daily closes with a new high on 01-02 and on 01-05, and a tie with the old high on 01-07.
```sql
CREATE TABLE stock_prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO stock_prices VALUES ('2024-01-01',100),('2024-01-02',110),('2024-01-03',99),
  ('2024-01-04',90),('2024-01-05',121),('2024-01-06',108.9),('2024-01-07',121);
```

**SQL answer:** the CTE computes the running max and min once; the drawdown divides by the running max. `SQL_MAXDD` finds the worst drawdown day (earliest day on a tie).
```sql
WITH r AS (
  SELECT trade_date, close_price,
         MAX(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max,
         MIN(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_min
  FROM stock_prices
)
SELECT trade_date, close_price, running_max, running_min,
       ROUND(close_price / running_max - 1, 4) AS drawdown
FROM r
ORDER BY trade_date
```
```sql
WITH r AS (
  SELECT trade_date, close_price / MAX(close_price) OVER (ORDER BY trade_date
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) - 1 AS dd
  FROM stock_prices
)
SELECT trade_date, ROUND(dd, 4) AS max_drawdown FROM r ORDER BY dd, trade_date LIMIT 1
```

**pandas answer:**
```py
out = px.copy()
out["running_max"] = px["close_price"].cummax()
out["running_min"] = px["close_price"].cummin()
out["drawdown"] = (px["close_price"] / out["running_max"] - 1).round(4)
dd_row = out.loc[out["drawdown"].idxmin(), ["trade_date", "drawdown"]]
```

**Example:** closes 100, 110, 99, 90, 121, 108.9, 121.
- Running max: 100, 110, 110, 110, 121, 121, 121. Running min: 100, 100, 99, 90, 90, 90, 90.
- Drawdown: 100/100 - 1 = 0; 110/110 - 1 = 0; 99/110 - 1 = -0.1; 90/110 - 1 = -0.1818; 121/121 - 1 = 0; 108.9/121 - 1 = -0.1; 121/121 - 1 = 0.
- Worst drawdown: -0.1818 on 01-04 (rounded to 4 places).

**Code:** run with `python3 -I`.
```python
# Q20: running max, running min and drawdown
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE stock_prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO stock_prices VALUES ('2024-01-01',100),('2024-01-02',110),('2024-01-03',99),
  ('2024-01-04',90),('2024-01-05',121),('2024-01-06',108.9),('2024-01-07',121);
"""
SQL_MAIN = """
WITH r AS (
  SELECT trade_date, close_price,
         MAX(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max,
         MIN(close_price) OVER (ORDER BY trade_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_min
  FROM stock_prices
)
SELECT trade_date, close_price, running_max, running_min,
       ROUND(close_price / running_max - 1, 4) AS drawdown
FROM r
ORDER BY trade_date
"""
SQL_MAXDD = """
WITH r AS (
  SELECT trade_date, close_price / MAX(close_price) OVER (ORDER BY trade_date
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) - 1 AS dd
  FROM stock_prices
)
SELECT trade_date, ROUND(dd, 4) AS max_drawdown FROM r ORDER BY dd, trade_date LIMIT 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
maxdd = con.execute(SQL_MAXDD).fetchone()
print("\nmax drawdown (SQL):", maxdd)

px = pd.read_sql_query("SELECT * FROM stock_prices ORDER BY trade_date", con)
# pd:main
out = px.copy()
out["running_max"] = px["close_price"].cummax()
out["running_min"] = px["close_price"].cummin()
out["drawdown"] = (px["close_price"] / out["running_max"] - 1).round(4)
dd_row = out.loc[out["drawdown"].idxmin(), ["trade_date", "drawdown"]]
# pd:end
# compared in trade_date order (both sorted by trade_date)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)
assert (dd_row["trade_date"], float(dd_row["drawdown"])) == maxdd
print("pandas max drawdown:", (dd_row["trade_date"], float(dd_row["drawdown"])))

# the ordered MAX OVER is cumulative; without ORDER BY it is the whole-partition max
print("MAX() OVER ()            :", [r[0] for r in con.execute("SELECT MAX(close_price) OVER () FROM stock_prices ORDER BY trade_date")])
print("MAX() OVER (ORDER BY ...):", [r[0] for r in con.execute("SELECT MAX(close_price) OVER (ORDER BY trade_date) FROM stock_prices ORDER BY trade_date")])

# duplicate dates: peers share the default frame, a unique tie-breaker makes it deterministic
con.executescript("""
CREATE TABLE px2(id INTEGER PRIMARY KEY, d TEXT, c REAL);
INSERT INTO px2 VALUES (1,'2024-01-01',100),(2,'2024-01-02',90),(3,'2024-01-02',130),(4,'2024-01-03',120);
""")
print("dup date, default frame running max by id:", [r[1] for r in con.execute(
    "SELECT id, MAX(c) OVER (ORDER BY d) FROM px2 ORDER BY id")])
print("dup date, ORDER BY d, id ROWS         :", [r[1] for r in con.execute(
    "SELECT id, MAX(c) OVER (ORDER BY d, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM px2 ORDER BY id")])

# NULL close: MAX ignores it, drawdown for that row is NULL; pandas cummax keeps NaN at that row
con.executescript("CREATE TABLE px3(d TEXT, c REAL); INSERT INTO px3 VALUES ('2024-01-01',100),('2024-01-02',NULL),('2024-01-03',80);")
print("NULL close, SQL running max :", [r[0] for r in con.execute(
    "SELECT MAX(c) OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM px3 ORDER BY d")])
print("NULL close, pandas cummax() :", pd.Series([100, None, 80], dtype="float64").cummax().tolist())
print("asserts passed: SQL running MAX/MIN/drawdown == pandas cummax/cummin")
```

**Output (my run):**
```text
trade_date  close_price  running_max  running_min  drawdown
2024-01-01        100.0        100.0        100.0    0.0000
2024-01-02        110.0        110.0        100.0    0.0000
2024-01-03         99.0        110.0         99.0   -0.1000
2024-01-04         90.0        110.0         90.0   -0.1818
2024-01-05        121.0        121.0         90.0    0.0000
2024-01-06        108.9        121.0         90.0   -0.1000
2024-01-07        121.0        121.0         90.0    0.0000

max drawdown (SQL): ('2024-01-04', -0.1818)
pandas max drawdown: ('2024-01-04', -0.1818)
MAX() OVER ()            : [121.0, 121.0, 121.0, 121.0, 121.0, 121.0, 121.0]
MAX() OVER (ORDER BY ...): [100.0, 110.0, 110.0, 110.0, 121.0, 121.0, 121.0]
dup date, default frame running max by id: [100.0, 130.0, 130.0, 130.0]
dup date, ORDER BY d, id ROWS         : [100.0, 100.0, 130.0, 130.0]
NULL close, SQL running max : [100.0, 100.0, 100.0]
NULL close, pandas cummax() : [100.0, nan, 100.0]
asserts passed: SQL running MAX/MIN/drawdown == pandas cummax/cummin
```

**Edge cases:**
- `MAX() OVER ()` without ORDER BY is the whole-table max (121.0 on every row in the output); `MAX() OVER (ORDER BY date)` is the cumulative one. That is the cumulative-versus-total difference the question asks about.
- Duplicate dates: the default frame treats rows with the same date as peers, so both get the same running max. In my test (ids 1-4, two rows on 01-02 with closes 90 and 130) the default frame gave 100, 130, 130, 130 for ids 1 to 4, while `ORDER BY d, id` with `ROWS` gave 100, 100, 130, 130. Use the tie-breaker when the date is not unique.
- NULL close: SQL `MAX` ignores the NULL, so the NULL row still shows the earlier max (100.0, 100.0, 100.0); pandas `cummax()` leaves NaN on that row (100.0, nan, 100.0). The drawdown for that day is NULL in SQL.
- Ties for the worst drawdown: my sample has none. By construction `ORDER BY dd, trade_date LIMIT 1` takes the earliest day, and pandas `idxmin` returns the first label with the minimum, so both would pick the earliest.
- First row: drawdown is 0 (close equals the running max).
- Rounding: `close/max - 1` is floating point, so I round to 4 places before asserting.

**Then explain:**
- Adding `ORDER BY` inside `OVER` makes the default frame "start of partition to current row (and peers)", so aggregates become running aggregates. I write the `ROWS` frame to be explicit and to avoid the peer effect.
- Drawdown measures how far below the all-time high so far you are; the maximum drawdown is the most negative value.
- All-time high so far uses only past data, so it is usable live; no look-ahead.

**Follow-ups:**
- *Reset the high every year?* `PARTITION BY` the year.
- *Max drawdown as a number?* `MIN(drawdown)` (here -0.1818), as in the second query.
- *Duration of the drawdown?* That needs gap/island logic (Part 7).

**Common mistakes:**
- Forgetting `ORDER BY` and returning the global max on every row.
- Dividing by the wrong thing (`close / first_close`, which is return, not drawdown).
- Using `max_close - close` and calling it a percentage.
- Reporting drawdown as positive on one side and negative on another.

### Q21 ⭐⭐ 🟡 Centered moving average: daily_sales(sale_date, amount). Return a 3-day centered average with ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING, show that the first and last rows only average two values, how to blank them (COUNT = 3 check), and give pandas rolling(3, center=True) with min_periods. Explain why centered averages cannot be used for forecasting or live dashboards (they look into the future).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `AVG(amount) OVER (ORDER BY d ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)` averages yesterday, today and tomorrow; at the first and last rows the frame has only two rows so it quietly averages two, which I blank with `CASE WHEN COUNT(amount) = 3`; pandas `rolling(3, center=True)` does the same, and it needs `min_periods=1` to match SQL's partial windows.

**Schema and sample data:** seven daily totals, one row per day.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',10),('2024-01-02',20),('2024-01-03',60),
  ('2024-01-04',40),('2024-01-05',50),('2024-01-06',90),('2024-01-07',30);
```

**SQL answer:** the named window `w` is reused three times. `SQL_TRAILING` (the usual backward-looking average) is in the Code block for the future-looking test.
```sql
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER w, 2) AS avg_available,
       COUNT(amount) OVER w AS n_in_window,
       CASE WHEN COUNT(amount) OVER w = 3 THEN ROUND(AVG(amount) OVER w, 2) END AS centered_avg
FROM daily_sales
WINDOW w AS (ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
ORDER BY sale_date
```

**pandas answer:**
```py
out = ds.copy()
out["avg_available"] = ds["amount"].rolling(3, center=True, min_periods=1).mean().round(2)
out["n_in_window"] = ds["amount"].rolling(3, center=True, min_periods=1).count().astype(int)
out["centered_avg"] = ds["amount"].rolling(3, center=True).mean().round(2)   # min_periods defaults to 3
```

**Example:** amounts 10, 20, 60, 40, 50, 90, 30.
- 01-01: window is only 01-01 and 01-02, (10 + 20) / 2 = 15.0 with 2 rows, so the centered value is blanked.
- 01-02: (10 + 20 + 60) / 3 = 30.0. 01-03: (20 + 60 + 40) / 3 = 40.0. 01-04: (60 + 40 + 50) / 3 = 50.0. 01-05: (40 + 50 + 90) / 3 = 60.0. 01-06: (50 + 90 + 30) / 3 = 56.67.
- 01-07: window is 01-06 and 01-07, (90 + 30) / 2 = 60.0 with 2 rows, blanked.

**Code:** run with `python3 -I`.
```python
# Q21: centered 3-day moving average
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',10),('2024-01-02',20),('2024-01-03',60),
  ('2024-01-04',40),('2024-01-05',50),('2024-01-06',90),('2024-01-07',30);
"""
SQL_MAIN = """
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER w, 2) AS avg_available,
       COUNT(amount) OVER w AS n_in_window,
       CASE WHEN COUNT(amount) OVER w = 3 THEN ROUND(AVG(amount) OVER w, 2) END AS centered_avg
FROM daily_sales
WINDOW w AS (ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
ORDER BY sale_date
"""
SQL_TRAILING = """
SELECT sale_date, ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS trailing_avg
FROM daily_sales ORDER BY sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
out = ds.copy()
out["avg_available"] = ds["amount"].rolling(3, center=True, min_periods=1).mean().round(2)
out["n_in_window"] = ds["amount"].rolling(3, center=True, min_periods=1).count().astype(int)
out["centered_avg"] = ds["amount"].rolling(3, center=True).mean().round(2)   # min_periods defaults to 3
# pd:end
# compared in sale_date order (both sorted by sale_date)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)

# looking into the future: change the LAST day only and see which rows move
before = pd.read_sql_query(SQL_MAIN, con)["centered_avg"]
trail_before = pd.read_sql_query(SQL_TRAILING, con)["trailing_avg"]
con.execute("UPDATE daily_sales SET amount = 300 WHERE sale_date = '2024-01-07'")
after = pd.read_sql_query(SQL_MAIN, con)["centered_avg"]
trail_after = pd.read_sql_query(SQL_TRAILING, con)["trailing_avg"]
changed_c = [d for d, b, a in zip(ds["sale_date"], before, after) if not (pd.isna(b) and pd.isna(a)) and b != a]
changed_t = [d for d, b, a in zip(ds["sale_date"], trail_before, trail_after) if b != a]
print("\nafter changing 2024-01-07 from 30 to 300:")
print("  centered average changed on:", changed_c)
print("  trailing average changed on :", changed_t)
print("asserts passed: SQL ROWS 1 PRECEDING..1 FOLLOWING == pandas rolling(3, center=True)")
```

**Output (my run):**
```text
 sale_date  amount  avg_available  n_in_window  centered_avg
2024-01-01      10          15.00            2           NaN
2024-01-02      20          30.00            3         30.00
2024-01-03      60          40.00            3         40.00
2024-01-04      40          50.00            3         50.00
2024-01-05      50          60.00            3         60.00
2024-01-06      90          56.67            3         56.67
2024-01-07      30          60.00            2           NaN

after changing 2024-01-07 from 30 to 300:
  centered average changed on: ['2024-01-06']
  trailing average changed on : ['2024-01-07']
asserts passed: SQL ROWS 1 PRECEDING..1 FOLLOWING == pandas rolling(3, center=True)
```

**Edge cases:**
- Ends: both ends average only two values. `COUNT(amount) = 3` (not `COUNT(*)`) is the safer check because a NULL amount inside the window should also make the average unreliable; `AVG` skips NULL and would silently average two values. I expect pandas with its default `min_periods` (3) to give NaN for a window containing a NaN, but I did not run that case.
- Ties and duplicates: `ROWS` counts rows, so duplicate dates would be treated as separate rows and a "3-day" average would span fewer days. The table has a primary key on the date; with duplicates, aggregate to one row per day first.
- Missing days: `ROWS` frames count rows, not days. A missing date makes the window span a longer time. Use a calendar or `RANGE` over day numbers for calendar windows (Part 5 Q24).
- Window size must be odd to be centered. With an even size pandas and SQL both need a choice of which side gets the extra row (not run here).
- One or two rows in total: the centered value is NULL everywhere.

**Then explain:**
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` is symmetric: one row on each side plus the current row.
- Why it cannot be used live: the value for day t needs day t+1. When I changed only the last day (30 to 300) the centered average changed on 01-06, a day before; the trailing average changed only on 01-07. That is the look-ahead. For a forecast or a live dashboard, use the trailing average, which depends on the past only.
- Centered averages are good for smoothing historical charts because they do not lag the data.

**Follow-ups:**
- *5-day centered?* `2 PRECEDING AND 2 FOLLOWING`, `COUNT = 5`; pandas `rolling(5, center=True)`.
- *Why not `RANGE`?* `RANGE` with an offset works on values (day numbers), not row counts; see Q24.
- *Why does the centered value change when future data arrives?* Because it uses it; the trailing one does not change when later rows arrive.

**Common mistakes:**
- Showing the two-value ends as if they were 3-day averages.
- Using a centered average as a model feature, leaking the future into training.
- Using `COUNT(*)` and missing NULL gaps.
- Assuming rows equal days.

### Q22 ⭐⭐ 🟡 Inventory running stock: inventory_moves(move_id, sku, move_date, qty_in, qty_out). Return the running stock per sku after each move, flag the first move where stock drops below a reorder level of 10, and list SKUs that ever went negative. Use signed quantities, SUM() OVER (PARTITION BY sku ORDER BY move_date, move_id) and a MIN OVER check, with the pandas groupby cumsum version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Turn each move into a signed quantity (`COALESCE(qty_in,0) - COALESCE(qty_out,0)`), take `SUM() OVER (PARTITION BY sku ORDER BY move_date, move_id)` for the stock after each move, flag the first row whose stock is below 10 with a running count of "below 10" rows equal to 1, and list SKUs where the minimum running stock is negative.

**Schema and sample data:** three SKUs, eleven moves. NULL in `qty_in` or `qty_out` means "none". SKU C has an in and an out on the same date.
```sql
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_in INTEGER, qty_out INTEGER);
INSERT INTO inventory_moves VALUES
  (1,'A','2024-01-01',50,NULL),(2,'A','2024-01-03',NULL,20),(3,'A','2024-01-05',NULL,25),
  (4,'A','2024-01-07',30,NULL),(5,'A','2024-01-09',NULL,28),
  (6,'B','2024-01-02',10,NULL),(7,'B','2024-01-04',NULL,12),(8,'B','2024-01-06',20,NULL),
  (9,'C','2024-01-01',5,NULL),(10,'C','2024-01-01',NULL,2),(11,'C','2024-01-02',20,NULL);
```

**SQL answer:** tie rule: `move_date, move_id`. `SQL_NEG` lists SKUs that ever went negative by taking `MIN` of the running stock.
```sql
WITH s AS (
  SELECT move_id, sku, move_date,
         COALESCE(qty_in, 0) - COALESCE(qty_out, 0) AS delta,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
), f AS (
  SELECT *, SUM(CASE WHEN stock < 10 THEN 1 ELSE 0 END)
              OVER (PARTITION BY sku ORDER BY move_date, move_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS below_so_far
  FROM s
)
SELECT move_id, sku, move_date, delta, stock,
       CASE WHEN stock < 10 AND below_so_far = 1 THEN 1 ELSE 0 END AS first_below_10
FROM f
ORDER BY sku, move_date, move_id
```
```sql
WITH s AS (
  SELECT sku,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
)
SELECT sku, MIN(stock) AS min_stock FROM s GROUP BY sku HAVING MIN(stock) < 0 ORDER BY sku
```

**pandas answer:** same signed delta, `groupby().cumsum()`, and the first flag by counting below-10 rows per SKU.
```py
m = moves.sort_values(["sku", "move_date", "move_id"]).copy()
m["delta"] = m["qty_in"].fillna(0) - m["qty_out"].fillna(0)
m["stock"] = m.groupby("sku")["delta"].cumsum()
below = m["stock"] < 10
m["first_below_10"] = (below & (below.groupby(m["sku"]).cumsum() == 1)).astype(int)
pd_df = m[["move_id", "sku", "move_date", "delta", "stock", "first_below_10"]]
neg = m.groupby("sku")["stock"].min()
pd_neg = neg[neg < 0].rename("min_stock").reset_index()
```

**Example:**
- SKU A: +50 = 50, -20 = 30, -25 = 5 (first below 10, flagged), +30 = 35, -28 = 7 (below 10 again, but not the first).
- SKU B: +10 = 10 (not below 10: the test is `< 10`), -12 = -2 (first below 10 and negative), +20 = 18. B is the negative SKU, minimum -2.
- SKU C: +5 = 5 on the first move (already below 10, so the first move is flagged), -2 = 3, +20 = 23.

**Code:** run with `python3 -I`.
```python
# Q22: running stock per SKU, first move below the reorder level, SKUs that went negative
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_in INTEGER, qty_out INTEGER);
INSERT INTO inventory_moves VALUES
  (1,'A','2024-01-01',50,NULL),(2,'A','2024-01-03',NULL,20),(3,'A','2024-01-05',NULL,25),
  (4,'A','2024-01-07',30,NULL),(5,'A','2024-01-09',NULL,28),
  (6,'B','2024-01-02',10,NULL),(7,'B','2024-01-04',NULL,12),(8,'B','2024-01-06',20,NULL),
  (9,'C','2024-01-01',5,NULL),(10,'C','2024-01-01',NULL,2),(11,'C','2024-01-02',20,NULL);
"""
SQL_MAIN = """
WITH s AS (
  SELECT move_id, sku, move_date,
         COALESCE(qty_in, 0) - COALESCE(qty_out, 0) AS delta,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
), f AS (
  SELECT *, SUM(CASE WHEN stock < 10 THEN 1 ELSE 0 END)
              OVER (PARTITION BY sku ORDER BY move_date, move_id
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS below_so_far
  FROM s
)
SELECT move_id, sku, move_date, delta, stock,
       CASE WHEN stock < 10 AND below_so_far = 1 THEN 1 ELSE 0 END AS first_below_10
FROM f
ORDER BY sku, move_date, move_id
"""
SQL_NEG = """
WITH s AS (
  SELECT sku,
         SUM(COALESCE(qty_in, 0) - COALESCE(qty_out, 0))
           OVER (PARTITION BY sku ORDER BY move_date, move_id
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves
)
SELECT sku, MIN(stock) AS min_stock FROM s GROUP BY sku HAVING MIN(stock) < 0 ORDER BY sku
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_neg = pd.read_sql_query(SQL_NEG, con)
print(sql_df.to_string(index=False))
print("\nSKUs that ever went negative:"); print(sql_neg.to_string(index=False))

moves = pd.read_sql_query("SELECT * FROM inventory_moves", con)
# pd:main
m = moves.sort_values(["sku", "move_date", "move_id"]).copy()
m["delta"] = m["qty_in"].fillna(0) - m["qty_out"].fillna(0)
m["stock"] = m.groupby("sku")["delta"].cumsum()
below = m["stock"] < 10
m["first_below_10"] = (below & (below.groupby(m["sku"]).cumsum() == 1)).astype(int)
pd_df = m[["move_id", "sku", "move_date", "delta", "stock", "first_below_10"]]
neg = m.groupby("sku")["stock"].min()
pd_neg = neg[neg < 0].rename("min_stock").reset_index()
# pd:end
# compared after sorting by sku, move_date, move_id
pd.testing.assert_frame_equal(sql_df, pd_df.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_neg, pd_neg, check_dtype=False)

# alternative reading of "drops below": a crossing from >= 10 to < 10 (SKU C starts below, so it never crosses)
cross = m.assign(prev=m.groupby("sku")["stock"].shift())
crossing = cross[(cross["stock"] < 10) & (cross["prev"] >= 10)][["move_id", "sku"]]
print("\ncrossing-based flag (prev >= 10 and now < 10), all crossings:", crossing.values.tolist())
print("first_below_10 flags:", sql_df.loc[sql_df["first_below_10"] == 1, ["move_id", "sku"]].values.tolist())
# tie rule matters: SKU C has an in and an out on the same date
alt = con.execute(SQL_NEG.replace("ORDER BY move_date, move_id", "ORDER BY move_date, move_id DESC")).fetchall()
print("with ties ordered move_id DESC the negative SKUs become:", alt)
print("asserts passed: SQL windows == pandas groupby cumsum")
```

**Output (my run):**
```text
 move_id sku  move_date  delta  stock  first_below_10
       1   A 2024-01-01     50     50               0
       2   A 2024-01-03    -20     30               0
       3   A 2024-01-05    -25      5               1
       4   A 2024-01-07     30     35               0
       5   A 2024-01-09    -28      7               0
       6   B 2024-01-02     10     10               0
       7   B 2024-01-04    -12     -2               1
       8   B 2024-01-06     20     18               0
       9   C 2024-01-01      5      5               1
      10   C 2024-01-01     -2      3               0
      11   C 2024-01-02     20     23               0

SKUs that ever went negative:
sku  min_stock
  B         -2

crossing-based flag (prev >= 10 and now < 10), all crossings: [[3, 'A'], [5, 'A'], [7, 'B']]
first_below_10 flags: [[3, 'A'], [7, 'B'], [9, 'C']]
with ties ordered move_id DESC the negative SKUs become: [('B', -2), ('C', -2)]
asserts passed: SQL windows == pandas groupby cumsum
```

**Edge cases:**
- Definition of "first move where stock drops below 10": I flag the first move whose stock after the move is below 10 (SKU C starts below, so it is flagged on move 9). If you want only crossings from 10 or above to below 10, the code also prints that variant: it flags moves 3 and 5 for A and 7 for B, and never flags C. Both readings are defensible; say which one you use.
- Same-date moves: the order matters. For SKU C the in (move 9) and out (move 10) share a date. With `move_id ASC` the stock never goes negative; when I reversed the tie order (`move_id DESC`) the out came first and C appeared as negative (minimum -2) in the SKU list as well as B. A real system should order by a timestamp or sequence number.
- NULL quantities: `COALESCE` to 0 before subtracting; otherwise `NULL - 20` is NULL and the running sum skips that move. In pandas `fillna(0)` does the same.
- Exactly 10: not below the reorder level (SKU B's first move).
- SKU with no moves: no rows, so it cannot appear; join to a SKU table for that.
- Opening stock is assumed to be 0: add an opening-balance row if it is not.

**Then explain:**
- Signed quantities turn a two-column in/out ledger into one number so a single running `SUM` works.
- "First time" = the running count of flagged rows equals 1 at a flagged row. Windows cannot be nested, so the stock window is in one CTE and the count of below-10 rows in the next.
- "Ever negative" is a `MIN` over the running stock, either `MIN() OVER (PARTITION BY sku)` or a `GROUP BY sku HAVING MIN(stock) < 0` over the CTE (the second form is in the code).
- pandas: `below.groupby(m["sku"]).cumsum() == 1` is the same running count; `groupby("sku")["stock"].min()` is the negative check.

**Follow-ups:**
- *When did each SKU first go negative?* Same trick with `stock < 0` instead of `< 10`.
- *Per warehouse too?* Add warehouse to `PARTITION BY`.
- *Days below the reorder level?* That is a streak problem (Part 7).

**Common mistakes:**
- Not ordering ties, so the stock order of same-day moves changes.
- Not handling NULL quantities.
- Using `<= 10` when the rule says below 10.
- Flagging every row below 10 rather than the first.

### Q23 ⭐⭐ 🟡 Year-over-year change: monthly_sales(month, revenue) where month is a text like '2024-03', with 24 consecutive months of data. Compute the YoY percent change with LAG(revenue, 12) and with a self-join on the same month a year earlier, and explain that LAG(12) is correct only when no month is missing (and when each month has exactly one row). Give pandas shift(12) and pct_change(12), and state what both return for the first 12 months.
**Asked at:** LearnSQL revenue-growth and Craig Kerstiens month-over-month blog write-ups (LAG, percent change, gaps break LAG, divide by zero), guides and not candidate reports; analyst screens at product companies and startups
**Say this first (1 line):** `LAG(revenue, 12) OVER (ORDER BY month)` fetches the row 12 rows back, which is the same month last year only when there are exactly 24 consecutive months with one row each; the self-join on "the same month minus one year" is safe against gaps and I show both.

**Schema and sample data:** 24 months, 2023-11 is deliberately 0 so the zero-base case shows up.
```sql
CREATE TABLE monthly_sales(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_sales VALUES
  ('2023-01',100),('2023-02',110),('2023-03',120),('2023-04',130),('2023-05',140),('2023-06',150),
  ('2023-07',160),('2023-08',170),('2023-09',180),('2023-10',190),('2023-11',0),('2023-12',210),
  ('2024-01',120),('2024-02',121),('2024-03',150),('2024-04',143),('2024-05',126),('2024-06',165),
  ('2024-07',176),('2024-08',170),('2024-09',162),('2024-10',228),('2024-11',220),('2024-12',252);
```

**SQL answer:** `LAG(12)` version, then the self-join (a LEFT JOIN so the first year is kept with NULLs).
```sql
SELECT month, revenue, LAG(revenue, 12) OVER (ORDER BY month) AS prev_year,
       ROUND((revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0), 2) AS yoy_pct
FROM monthly_sales
ORDER BY month
```
```sql
SELECT c.month, c.revenue, p.revenue AS prev_year,
       ROUND((c.revenue - p.revenue) * 100.0 / NULLIF(p.revenue, 0), 2) AS yoy_pct
FROM monthly_sales c
LEFT JOIN monthly_sales p
  ON p.month = (CAST(substr(c.month, 1, 4) AS INTEGER) - 1) || substr(c.month, 5)
ORDER BY c.month
```

**pandas answer:** `shift(12)` for the previous-year value, `pct_change(12)` for the ratio (inf where the base is 0, replaced by NaN to match `NULLIF`).
```py
s = ms.set_index("month")["revenue"]
pd_df = pd.DataFrame({"revenue": s, "prev_year": s.shift(12)})
pd_df["yoy_pct"] = (s.pct_change(12) * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
```

**Example:**
- 2024-01: 120 versus 2023-01: 100 gives +20.0%. 2024-03: 150 versus 120 gives +25.0%. 2024-05: 126 versus 140 gives -10.0%. 2024-08: 170 versus 170 gives 0.0%.
- 2024-11: the base 2023-11 is 0, so the percent is undefined: NULL (`NULLIF`).
- 2023-01 to 2023-12: there are no rows 12 months back, so `prev_year` and the percent are NULL (NaN in pandas), 12 rows in total.

**Code:** run with `python3 -I`.
```python
# Q23: year-over-year change with LAG(12), a self-join, and pandas shift(12) / pct_change(12)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_sales(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_sales VALUES
  ('2023-01',100),('2023-02',110),('2023-03',120),('2023-04',130),('2023-05',140),('2023-06',150),
  ('2023-07',160),('2023-08',170),('2023-09',180),('2023-10',190),('2023-11',0),('2023-12',210),
  ('2024-01',120),('2024-02',121),('2024-03',150),('2024-04',143),('2024-05',126),('2024-06',165),
  ('2024-07',176),('2024-08',170),('2024-09',162),('2024-10',228),('2024-11',220),('2024-12',252);
"""

SQL_MAIN = """
SELECT month, revenue, LAG(revenue, 12) OVER (ORDER BY month) AS prev_year,
       ROUND((revenue - LAG(revenue, 12) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue, 12) OVER (ORDER BY month), 0), 2) AS yoy_pct
FROM monthly_sales
ORDER BY month
"""
SQL_JOIN = """
SELECT c.month, c.revenue, p.revenue AS prev_year,
       ROUND((c.revenue - p.revenue) * 100.0 / NULLIF(p.revenue, 0), 2) AS yoy_pct
FROM monthly_sales c
LEFT JOIN monthly_sales p
  ON p.month = (CAST(substr(c.month, 1, 4) AS INTEGER) - 1) || substr(c.month, 5)
ORDER BY c.month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
join_df = pd.read_sql_query(SQL_JOIN, con)
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, join_df, check_dtype=False)
print("\nLAG(12) and self-join agree on all 24 rows")

ms = pd.read_sql_query("SELECT * FROM monthly_sales ORDER BY month", con)
# pd:main
s = ms.set_index("month")["revenue"]
pd_df = pd.DataFrame({"revenue": s, "prev_year": s.shift(12)})
pd_df["yoy_pct"] = (s.pct_change(12) * 100).replace([float("inf"), -float("inf")], float("nan")).round(2)
# pd:end
# compared in month order (both sorted by month)
pd.testing.assert_frame_equal(sql_df.set_index("month"), pd_df, check_dtype=False)
print("pandas first 12 prev_year:", pd_df["prev_year"].head(12).isna().all(), "| first 12 yoy_pct all NaN:", pd_df["yoy_pct"].head(12).isna().all())
print("raw pct_change(12) on 2024-11 (base 0):", (s.pct_change(12) * 100).loc["2024-11"])

# a missing month and a duplicated month break LAG(12) and shift(12), not the self-join
con.executescript("""
CREATE TABLE gap(month TEXT, revenue INTEGER);
INSERT INTO gap SELECT month, revenue FROM monthly_sales WHERE month <> '2023-03';
CREATE TABLE dup(month TEXT, revenue INTEGER);
INSERT INTO dup SELECT month, revenue FROM monthly_sales;
INSERT INTO dup VALUES ('2023-05', 1);
""")
JOIN_TMPL = """SELECT c.month, p.revenue FROM {t} c
               LEFT JOIN {t} p ON p.month = (CAST(substr(c.month, 1, 4) AS INTEGER) - 1) || substr(c.month, 5)
               WHERE c.month LIKE '2024-%' ORDER BY c.month, p.revenue"""
LAG_TMPL = """SELECT month, LAG(revenue, 12) OVER (ORDER BY month, revenue) FROM {t}
              ORDER BY month, revenue"""
for name in ("gap", "dup"):
    lag24 = [(m, v) for m, v in con.execute(LAG_TMPL.format(t=name)) if m.startswith("2024-")]
    jn24 = con.execute(JOIN_TMPL.format(t=name)).fetchall()
    print(f"\ntable {name}: LAG(12) 2024 rows:", [v for _, v in lag24])
    print(f"table {name}: self-join 2024 rows:", [v for _, v in jn24], "(" + str(len(jn24)) + " rows)")
g = pd.read_sql_query("SELECT * FROM gap ORDER BY month", con)
gs = g.set_index("month")["revenue"]
print("\npandas shift(12) on the gap table, 2024-03 sees:", gs.shift(12).loc["2024-03"], "(true 2023-03 is missing; 2023-02 is", gs.loc["2023-02"], ")")
p = gs.copy()
p.index = pd.PeriodIndex(p.index, freq="M")
prev_year = p.set_axis(p.index + 12).reindex(p.index)
print("pandas PeriodIndex calendar shift, 2024-03 sees:", prev_year.loc["2024-03"], "(NaN: no row a year earlier)")
print("SQLite 1.0/0 gives", con.execute("SELECT 1.0/0").fetchone()[0])
print("asserts passed: SQL LAG(12) == self-join == pandas shift(12)/pct_change(12) on the clean 24 months")
```

**Output (my run):**
```text
  month  revenue  prev_year  yoy_pct
2023-01      100        NaN      NaN
2023-02      110        NaN      NaN
2023-03      120        NaN      NaN
2023-04      130        NaN      NaN
2023-05      140        NaN      NaN
2023-06      150        NaN      NaN
2023-07      160        NaN      NaN
2023-08      170        NaN      NaN
2023-09      180        NaN      NaN
2023-10      190        NaN      NaN
2023-11        0        NaN      NaN
2023-12      210        NaN      NaN
2024-01      120      100.0     20.0
2024-02      121      110.0     10.0
2024-03      150      120.0     25.0
2024-04      143      130.0     10.0
2024-05      126      140.0    -10.0
2024-06      165      150.0     10.0
2024-07      176      160.0     10.0
2024-08      170      170.0      0.0
2024-09      162      180.0    -10.0
2024-10      228      190.0     20.0
2024-11      220        0.0      NaN
2024-12      252      210.0     20.0

LAG(12) and self-join agree on all 24 rows
pandas first 12 prev_year: True | first 12 yoy_pct all NaN: True
raw pct_change(12) on 2024-11 (base 0): inf

table gap: LAG(12) 2024 rows: [None, 100, 110, 130, 140, 150, 160, 170, 180, 190, 0, 210]
table gap: self-join 2024 rows: [100, 110, None, 130, 140, 150, 160, 170, 180, 190, 0, 210] (12 rows)

table dup: LAG(12) 2024 rows: [110, 120, 130, 1, 140, 150, 160, 170, 180, 190, 0, 210]
table dup: self-join 2024 rows: [100, 110, 120, 130, 1, 140, 150, 160, 170, 180, 190, 0, 210] (13 rows)

pandas shift(12) on the gap table, 2024-03 sees: 110.0 (true 2023-03 is missing; 2023-02 is 110 )
pandas PeriodIndex calendar shift, 2024-03 sees: nan (NaN: no row a year earlier)
SQLite 1.0/0 gives None
asserts passed: SQL LAG(12) == self-join == pandas shift(12)/pct_change(12) on the clean 24 months
```

**Edge cases:**
- First 12 months: NULL in SQL, NaN in pandas for both `shift(12)` and `pct_change(12)`; the output shows all 12 are NaN.
- Zero base: SQL with `NULLIF` returns NULL; pandas gave `inf` (raw value printed in the output) and I replaced it with NaN. Without `NULLIF`, SQLite also returns NULL for division by zero; other engines may raise an error (not executed here).
- Missing month: I removed 2023-03 to make a 23-row table. `LAG(12)` then returned NULL for 2024-01 (the right answer is 100), 100 for 2024-02 (right: 110) and 110 for 2024-03 (right: NULL, since 2023-03 has no row). From 2024-04 onward it re-aligned. The self-join returned the right values. pandas `shift(12)` on the same table gave 110.0 for 2024-03, which is 2023-02's value; a `PeriodIndex` shifted by 12 months gave NaN, the correct answer.
- Duplicate month: I added a second 2023-05 row (revenue 1). `LAG(12)` shifted every later row by one (for example 2024-01 got 110 instead of 100), and the self-join returned 13 rows for the 12 months of 2024 because 2024-05 matched both 2023-05 rows. Fix: aggregate to one row per month first.
- Ties: with duplicate months I ordered by `month, revenue` to make `LAG` deterministic; the right fix is still to remove the duplicates.
- Text months: `'2024-03'` sorts correctly as text. The self-join builds the previous year with `(CAST(substr(month,1,4) AS INTEGER) - 1) || substr(month,5)`.

**Then explain:**
- `LAG(x, 12)` is positional, like in Q13 and Q16: correct only if the rows are a complete, unique monthly series.
- The join is calendar-based. It needs an index on `month` to be fast on large tables (not timed here).
- pandas `shift(12)` and `pct_change(12)` are positional too. On a datetime or period index, shift the index (for example `PeriodIndex + 12`) and align, which is the join.
- State the first-year result plainly: no prior year, so no YoY value; do not fill with 0.

**Follow-ups:**
- *Month-over-month on the same table?* `LAG(revenue)` and the same gap caveat (Q16).
- *YoY for quarterly or daily data?* Change the offset (4 or 365 rows is only right with complete data; for days, leap years also break a 365-row shift).
- *Percent or percentage points?* Percent change here; for rates, subtract.

**Common mistakes:**
- Using `LAG(12)` on a gappy or duplicated table.
- Dividing by a zero base.
- Comparing months as text arithmetic.
- Reporting the first year as 0% growth.

### Q24 ⭐⭐ 🟡 Time-based window on dates: sales(sale_date, amount) with gaps (some calendar days missing). Compute the sum over the trailing 7 calendar days, not the trailing 7 rows. Show why ROWS BETWEEN 6 PRECEDING is wrong with gaps, how RANGE BETWEEN 6 PRECEDING AND CURRENT ROW works in SQLite when ORDER BY uses a number such as julianday(sale_date), and that ordering by the text date with a numeric offset gives a silently wrong answer in SQLite 3.45 (run it). PostgreSQL uses RANGE BETWEEN INTERVAL '6 days' PRECEDING (hedged, not executed). Give pandas rolling('7D', on='sale_date').
**Asked at:** vendor documentation (PostgreSQL window-function syntax and function pages, SQLite window functions), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `ROWS BETWEEN 6 PRECEDING` counts rows, so with missing days it reaches back past 7 calendar days; use `RANGE BETWEEN 6 PRECEDING AND CURRENT ROW` ordered by a number such as `julianday(sale_date)`, which keeps the rows whose day number is within 6 of the current one, and never put a numeric offset on a text date, because SQLite 3.45 accepts it and returns wrong sums without an error.

**Schema and sample data:** seven raw rows; 2024-01-04 has two sales, and 01-03, 01-05 to 01-07 and 01-10 to 01-14 have none.
```sql
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES ('2024-01-01',1),('2024-01-02',2),('2024-01-04',4),('2024-01-04',8),
  ('2024-01-08',16),('2024-01-09',32),('2024-01-15',64);
```

**SQL answer:** first one row per day (so a duplicate date cannot give peers a different story), then the RANGE frame on the day number. The ROWS and text-date versions are in the Code block as `SQL_ROWS` and `SQL_TEXT`, to show the wrong answers.
```sql
WITH daily AS (
  SELECT sale_date, SUM(amount) AS amount FROM sales GROUP BY sale_date
)
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY julianday(sale_date)
                         RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS last_7_days
FROM daily
ORDER BY sale_date
```

**pandas answer:** `rolling("7D", on="sale_date")` is a time-based window. It needs the `on` column to be datetime and sorted, and its default `closed="right"` means the window is (t - 7 days, t], which for midnight dates is the same as day numbers t-6 to t.
```py
daily = sales.groupby("sale_date", as_index=False)["amount"].sum()
daily["sale_date"] = pd.to_datetime(daily["sale_date"])
daily["last_7_days"] = daily.rolling("7D", on="sale_date")["amount"].sum()
```

**Example:** daily totals are 01-01 = 1, 01-02 = 2, 01-04 = 12 (4 + 8), 01-08 = 16, 01-09 = 32, 01-15 = 64.
- 01-04: days 01-01 to 01-04 hold 1 + 2 + 12 = 15.
- 01-08: days 01-02 to 01-08 hold 2 + 12 + 16 = 30 (01-01 is 7 days back, outside).
- 01-09: days 01-03 to 01-09 hold 12 + 16 + 32 = 60.
- 01-15: days 01-09 to 01-15 hold 32 + 64 = 96 (the gap before it is simply empty).
- `ROWS BETWEEN 6 PRECEDING` gives 31, 63 and 127 for the last three days, because it sums the previous rows whatever their dates (01-08 gets 1 + 2 + 12 + 16 = 31, which includes 01-01).

**Code:** run with `python3 -I`.
```python
# Q24: trailing 7 calendar days with gaps (RANGE on a day number) versus ROWS and text-date RANGE
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES ('2024-01-01',1),('2024-01-02',2),('2024-01-04',4),('2024-01-04',8),
  ('2024-01-08',16),('2024-01-09',32),('2024-01-15',64);
"""
# one row per calendar day first, then RANGE over the day number: window = day-6 .. day
SQL_MAIN = """
WITH daily AS (
  SELECT sale_date, SUM(amount) AS amount FROM sales GROUP BY sale_date
)
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY julianday(sale_date)
                         RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS last_7_days
FROM daily
ORDER BY sale_date
"""
SQL_ROWS = """
WITH daily AS (SELECT sale_date, SUM(amount) AS amount FROM sales GROUP BY sale_date)
SELECT sale_date, SUM(amount) OVER (ORDER BY sale_date
                                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS wrong_rows
FROM daily ORDER BY sale_date
"""
SQL_TEXT = """
WITH daily AS (SELECT sale_date, SUM(amount) AS amount FROM sales GROUP BY sale_date)
SELECT sale_date, SUM(amount) OVER (ORDER BY sale_date
                                    RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS wrong_text_range
FROM daily ORDER BY sale_date
"""
# raw rows (two rows on 2024-01-04): RANGE gives both peers the same value
SQL_RAW = """
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY julianday(sale_date)
                         RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS last_7_days
FROM sales
ORDER BY sale_date, amount
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
rows_df = pd.read_sql_query(SQL_ROWS, con)
text_df = pd.read_sql_query(SQL_TEXT, con)
raw_df = pd.read_sql_query(SQL_RAW, con)
cmp = sql_df.merge(rows_df, on="sale_date").merge(text_df, on="sale_date")
print(cmp.to_string(index=False))

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
daily = sales.groupby("sale_date", as_index=False)["amount"].sum()
daily["sale_date"] = pd.to_datetime(daily["sale_date"])
daily["last_7_days"] = daily.rolling("7D", on="sale_date")["amount"].sum()
# pd:end
pd_df = daily.assign(sale_date=daily["sale_date"].dt.strftime("%Y-%m-%d")).sort_values("sale_date").reset_index(drop=True)
# compared after sorting by sale_date; sums are exact, so compare as int
pd_df["last_7_days"] = pd_df["last_7_days"].astype("int64")
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert rows_df["wrong_rows"].tolist() != sql_df["last_7_days"].tolist()
assert text_df["wrong_text_range"].tolist() != sql_df["last_7_days"].tolist()

print("\nraw rows (duplicate date) with SQL RANGE:")
print(raw_df.to_string(index=False))
raw = sales.assign(sale_date=pd.to_datetime(sales["sale_date"])).sort_values(["sale_date", "amount"]).reset_index(drop=True)
raw["pandas_7D_row_by_row"] = raw.rolling("7D", on="sale_date")["amount"].sum().astype("int64")
print("\npandas rolling('7D') on the same raw rows:")
print(raw.to_string(index=False))
last_of_day = raw.groupby("sale_date")["pandas_7D_row_by_row"].transform("last")
assert last_of_day.tolist() == raw_df["last_7_days"].tolist()
print("\nlast row of each date in pandas equals the SQL RANGE value: True")
print("asserts passed: SQL RANGE on julianday == pandas rolling('7D') on daily rows")
```

**Output (my run):**
```text
 sale_date  amount  last_7_days  wrong_rows  wrong_text_range
2024-01-01       1            1           1                 1
2024-01-02       2            3           3                 2
2024-01-04      12           15          15                12
2024-01-08      16           30          31                16
2024-01-09      32           60          63                32
2024-01-15      64           96         127                64

raw rows (duplicate date) with SQL RANGE:
 sale_date  amount  last_7_days
2024-01-01       1            1
2024-01-02       2            3
2024-01-04       4           15
2024-01-04       8           15
2024-01-08      16           30
2024-01-09      32           60
2024-01-15      64           96

pandas rolling('7D') on the same raw rows:
 sale_date  amount  pandas_7D_row_by_row
2024-01-01       1                     1
2024-01-02       2                     3
2024-01-04       4                     7
2024-01-04       8                    15
2024-01-08      16                    30
2024-01-09      32                    60
2024-01-15      64                    96

last row of each date in pandas equals the SQL RANGE value: True
asserts passed: SQL RANGE on julianday == pandas rolling('7D') on daily rows
```

**Edge cases:**
- **Text date with a numeric offset:** in my run `ORDER BY sale_date RANGE BETWEEN 6 PRECEDING ...` raised no error and each row summed only its own day (1, 2, 12, 16, 32, 64), so no 7-day window at all. I did not dig into the mechanism; the rule is to give RANGE a numeric ORDER BY expression.
- **Duplicate dates:** with raw rows, both 2024-01-04 rows get 15 in SQL (RANGE treats equal day numbers as peers). pandas `rolling("7D")` on the same raw rows gives 7 for the first 01-04 row and 15 for the second: it moves row by row inside a tie. The last row of each date equals the SQL value (asserted). Aggregating to one row per day first removes the question, and that is what the main query does.
- **Empty days:** a day with no sales produces no output row. If the report needs a row for every calendar day, join a calendar first (Part 6 territory); the windowed sum is then still a RANGE frame, now over a complete list.
- **Timestamps instead of dates:** `julianday` of a timestamp has a fractional part, and `6 PRECEDING` then means exactly 6.0 days back. Cut to the date first if you want calendar days.
- **Dialects (not executed here):** PostgreSQL orders by the date itself and writes `RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW`. In my scratch check an `INTERVAL` offset was a syntax error on SQLite 3.45.

**Then explain:**
- ROWS frame = N physical rows; RANGE frame = rows whose ORDER BY value is within an offset of the current value. A calendar window is a value question, so it is RANGE.
- RANGE with an offset allows exactly one ORDER BY expression (PostgreSQL docs, opened; I did not test the multi-column case on SQLite), and the run above shows what a text ORDER BY does.
- The sum is over days that exist; if you want a 7-day average that divides by 7 even when days are missing, use `SUM / 7`, not `AVG`.

**Follow-ups:**
- *30-day window?* `RANGE BETWEEN 29 PRECEDING AND CURRENT ROW`.
- *Why not a correlated subquery?* It works and handles duplicates the same way (Q28), but is usually slower on big tables (I did not time it here).
- *The data has a row for every day, do I still need RANGE?* No, ROWS is fine, but RANGE is the safer default when you cannot promise no gaps.

**Common mistakes:**
- `ROWS BETWEEN 6 PRECEDING` on data with gaps.
- Ordering by the text date and adding a number: no error, wrong answer.
- Forgetting pandas needs a sorted datetime `on` column, and that `'7D'` is (t - 7D, t], so a row exactly 7 days back is excluded.

### Q25 ⭐⭐ 🟡 Pareto and cumulative share: product_sales(product_id, revenue). Sort products by revenue descending, compute the cumulative share of total revenue, and return the products that together make up the first 80 percent (including the product that crosses the line). Use SUM() OVER (ORDER BY revenue DESC, product_id) and SUM() OVER (), say how ties on revenue are handled, and give the pandas cumsum version. Mention that the 'top 10 percent of customers' variant is NTILE (Part 4).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Sort by revenue descending with `product_id` as the tie-break, take a running `SUM(revenue)` and divide by `SUM(revenue) OVER ()`; to include the product that crosses the 80 percent line, keep a row while the cumulative total before it is still under 80 percent (`cum - revenue < 0.8 * total`), not while its own cumulative share is at most 80 percent.

**Schema and sample data:** five products; 103 and 104 tie at 12.
```sql
CREATE TABLE product_sales(product_id INTEGER PRIMARY KEY, revenue INTEGER);
INSERT INTO product_sales VALUES (101,40),(102,25),(103,12),(104,12),(105,11);
```

**SQL answer:** the threshold is a parameter. I compare in integers (`(cum - revenue) * 100 < pct * total`) so an exact 80 percent boundary is not a floating-point coin toss.
```sql
WITH c AS (
  SELECT product_id, revenue,
         SUM(revenue) OVER (ORDER BY revenue DESC, product_id
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_revenue,
         SUM(revenue) OVER () AS total
  FROM product_sales
)
SELECT product_id, revenue, cum_revenue,
       ROUND(100.0 * cum_revenue / total, 1) AS cum_share_pct
FROM c
WHERE (cum_revenue - revenue) * 100 < ? * total
ORDER BY revenue DESC, product_id
```

**pandas answer:** sort with the same two keys, `cumsum`, then the same integer test.
```py
d = ps.sort_values(["revenue", "product_id"], ascending=[False, True]).reset_index(drop=True)
d["cum_revenue"] = d["revenue"].cumsum()
total = d["revenue"].sum()
d["cum_share_pct"] = (100.0 * d["cum_revenue"] / total).round(1)
out = d[(d["cum_revenue"] - d["revenue"]) * 100 < pct * total]
```

**Example:** total revenue is 40 + 25 + 12 + 12 + 11 = 100, sorted 101 (40), 102 (25), 103 (12), 104 (12), 105 (11). Cumulative: 40, 65, 77, 89, 100.
- 80 percent: cumulative before 104 is 77, under 80, so 104 is kept even though its own cumulative share is 89; cumulative before 105 is 89, so 105 stops the list. Result 101, 102, 103, 104.
- 70 percent: before 103 is 65 (under 70, kept); before 104 is 77 (stop). Result 101, 102, 103.
- 65 percent: before 102 is 40, kept; before 103 is 65, not under 65, so the list stops at 102. A product that lands exactly on the line is included, the next one is not.

**Code:** run with `python3 -I`.
```python
# Q25: Pareto, cumulative share of revenue, products making up the first X percent
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE product_sales(product_id INTEGER PRIMARY KEY, revenue INTEGER);
INSERT INTO product_sales VALUES (101,40),(102,25),(103,12),(104,12),(105,11);
"""
# ties on revenue: lower product_id first. Integer arithmetic avoids float error on the 80% line.
SQL_MAIN = """
WITH c AS (
  SELECT product_id, revenue,
         SUM(revenue) OVER (ORDER BY revenue DESC, product_id
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_revenue,
         SUM(revenue) OVER () AS total
  FROM product_sales
)
SELECT product_id, revenue, cum_revenue,
       ROUND(100.0 * cum_revenue / total, 1) AS cum_share_pct
FROM c
WHERE (cum_revenue - revenue) * 100 < ? * total
ORDER BY revenue DESC, product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ps = pd.read_sql_query("SELECT * FROM product_sales", con)

def pandas_pareto(ps, pct):
    # pd:main
    d = ps.sort_values(["revenue", "product_id"], ascending=[False, True]).reset_index(drop=True)
    d["cum_revenue"] = d["revenue"].cumsum()
    total = d["revenue"].sum()
    d["cum_share_pct"] = (100.0 * d["cum_revenue"] / total).round(1)
    out = d[(d["cum_revenue"] - d["revenue"]) * 100 < pct * total]
    # pd:end
    return out.reset_index(drop=True)

for pct in (80, 70, 65):
    sql_df = pd.read_sql_query(SQL_MAIN, con, params=(pct,))
    pd_df = pandas_pareto(ps, pct)
    # compared in the order revenue DESC, product_id ASC
    pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
    print(f"first {pct} percent (a row is kept while the cumulative total BEFORE it is under {pct}% of total):")
    print(sql_df.to_string(index=False))
    print()
full = pd.read_sql_query(SQL_MAIN, con, params=(101,))
print("threshold 101 keeps every row:", full["product_id"].tolist())

# tie check: reversing product_id order inside the tie changes who makes the 70% cut
rev = pd.read_sql_query("""
WITH c AS (SELECT product_id, revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC, product_id DESC) AS cum, SUM(revenue) OVER () AS total
        FROM product_sales)
SELECT product_id FROM c WHERE (cum - revenue) * 100 < 70 * total ORDER BY product_id""", con)
print("70% cut with the tie order reversed (product_id DESC):", rev["product_id"].tolist())

print("asserts passed: SQL window == pandas cumsum for 80, 70 and 65 percent")
```

**Output (my run):**
```text
first 80 percent (a row is kept while the cumulative total BEFORE it is under 80% of total):
 product_id  revenue  cum_revenue  cum_share_pct
        101       40           40           40.0
        102       25           65           65.0
        103       12           77           77.0
        104       12           89           89.0

first 70 percent (a row is kept while the cumulative total BEFORE it is under 70% of total):
 product_id  revenue  cum_revenue  cum_share_pct
        101       40           40           40.0
        102       25           65           65.0
        103       12           77           77.0

first 65 percent (a row is kept while the cumulative total BEFORE it is under 65% of total):
 product_id  revenue  cum_revenue  cum_share_pct
        101       40           40           40.0
        102       25           65           65.0

threshold 101 keeps every row: [101, 102, 103, 104, 105]
70% cut with the tie order reversed (product_id DESC): [101, 102, 104]
asserts passed: SQL window == pandas cumsum for 80, 70 and 65 percent
```

**Edge cases:**
- **Ties:** 103 and 104 both have revenue 12. With `product_id` ascending as the tie-break, 103 is in the 70 percent list and 104 is out; reversing the tie-break (run above) swaps them. The cut inside a tie is arbitrary, so say the rule out loud; without a tie-breaker the order inside a tie is not guaranteed and the list may change between runs.
- **Exactly on the line:** handled by the strict `<` on the amount before the row (65 percent run).
- **NULL revenue:** `SUM` skips it, but the row would still sit in the ordering (SQLite sorts NULL last in DESC order); filter `WHERE revenue IS NOT NULL` first if NULLs are possible.
- **Zero or negative revenue:** cumulative share is no longer monotone; this answer assumes non-negative revenue.
- **Duplicate product_id rows:** aggregate to one row per product before the window.

**Then explain:**
- Two windows over the same table: one ordered and cumulative, one empty (`OVER ()`) giving the grand total on every row. A window function cannot be used in WHERE, so the filter sits in the outer query.
- "Including the crossing product" is the interview twist: filter on the cumulative total before the row.
- The pandas side is the same steps: `sort_values`, `cumsum`, divide by `sum()`.
- The "top 10 percent of customers" variant is bucketing by rank, which is `NTILE` and belongs to Part 4; I did not use it here.

**Follow-ups:**
- *How many products make up 80 percent?* Count the rows returned.
- *Share of products, not revenue?* `ROW_NUMBER` over the count of products; that is a ranking problem (Part 4).
- *What if the question is "at most 80 percent" (do not include the crossing product)?* Filter `cum_share <= 0.8` instead.

**Common mistakes:**
- Filtering `cum_share <= 0.8`, which drops the crossing product.
- No tie-breaker, so the list is not reproducible.
- Comparing floating-point shares to 0.8 on an exact boundary.

### Q26 ⭐⭐ 🟡 Detect increases and decreases with LAG: stock_prices(trade_date, close_price). Label every day 'up', 'down', 'flat' or NULL (first row) by comparing with the previous close, count up days per month, and flag days where the price rose three days in a row using LAG with offsets 1 and 2. Show the pandas shift/diff version, and say that finding the longest streak of any length is a gaps-and-islands problem (Part 7); LeetCode 180 Consecutive Numbers is the same LAG(1), LAG(2) idea.
**Asked at:** public LeetCode-style problem bank (1321 Restaurant Growth statement seen in a search snippet; 1308 Running Total for Different Genders, 197 Rising Temperature and 180 Consecutive Numbers known only by title from third-party lists), not candidate reports; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Compare each close with `LAG(close_price)` in a CASE to label up, down, flat (NULL on the first row), sum the up days per month, and for a streak combine several LAGs; note that "rose three days in a row" is three rises, which needs `LAG` offsets 1, 2 and 3, while offsets 1 and 2 only prove three rising closes (two rises).

**Schema and sample data:** one ticker, ten trading days across January and February, `trade_date` is the primary key (so there are no duplicate dates; with several tickers add `PARTITION BY ticker`).
```sql
CREATE TABLE stock_prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO stock_prices VALUES
 ('2024-01-29',10),('2024-01-30',11),('2024-01-31',12),('2024-02-01',13),('2024-02-02',13),
 ('2024-02-05',12),('2024-02-06',13),('2024-02-07',14),('2024-02-08',15),('2024-02-09',14);
```

**SQL answer:** labels and flags in one query (`SQL_MAIN`), monthly count as `SQL_MONTH` in the Code block.
```sql
WITH l AS (
  SELECT trade_date, close_price,
         LAG(close_price, 1) OVER w AS p1,
         LAG(close_price, 2) OVER w AS p2,
         LAG(close_price, 3) OVER w AS p3
  FROM stock_prices
  WINDOW w AS (ORDER BY trade_date)
)
SELECT trade_date, close_price,
       CASE WHEN p1 IS NULL THEN NULL
            WHEN close_price > p1 THEN 'up'
            WHEN close_price < p1 THEN 'down'
            ELSE 'flat' END AS move,
       CASE WHEN p3 IS NULL THEN NULL
            WHEN close_price > p1 AND p1 > p2 AND p2 > p3 THEN 1 ELSE 0 END AS rose_3_days,
       CASE WHEN p2 IS NULL THEN NULL
            WHEN close_price > p1 AND p1 > p2 THEN 1 ELSE 0 END AS three_rising_closes
FROM l
ORDER BY trade_date
```
```sql
WITH l AS (
  SELECT trade_date, close_price, LAG(close_price) OVER (ORDER BY trade_date) AS p1
  FROM stock_prices
)
SELECT substr(trade_date, 1, 7) AS month,
       SUM(CASE WHEN close_price > p1 THEN 1 ELSE 0 END) AS up_days
FROM l
GROUP BY substr(trade_date, 1, 7)
ORDER BY month
```

**pandas answer:** `diff()` gives the change, `np.select` labels it, `shift` on the boolean "up" series gives the earlier days.
```py
d = sp.sort_values("trade_date").reset_index(drop=True)
diff = d["close_price"].diff()
d["move"] = np.select([diff.isna(), diff > 0, diff < 0], [None, "up", "down"], default="flat")
up = diff > 0
d["three_rising_closes"] = (up & up.shift(1, fill_value=False)).astype(int).where(diff.shift(1).notna())
d["rose_3_days"] = (up & up.shift(1, fill_value=False) & up.shift(2, fill_value=False)).astype(int).where(diff.shift(2).notna())
up_days = up.groupby(d["trade_date"].str[:7]).sum().astype(int).rename("up_days").reset_index().rename(columns={"trade_date": "month"})
```

**Example:** closes 10, 11, 12, 13, 13, 12, 13, 14, 15, 14.
- 01-29 has no previous close: label NULL. 01-30, 01-31, 02-01 are up. 02-02 is flat (13 = 13). 02-05 is down.
- 02-01: the three previous moves (11 over 10, 12 over 11, 13 over 12) are all rises, so `rose_3_days = 1`. 01-31 only has two moves behind it, so it is `three_rising_closes = 1` but `rose_3_days` is NULL (no `LAG(3)`).
- 02-08: 13 to 14 to 15 after a rise from 12 gives three rises: flag 1. 02-07 has only two rises since the dip: `three_rising_closes = 1`, `rose_3_days = 0`.
- Up days: January 2 (01-30, 01-31), February 4 (02-01, 02-06, 02-07, 02-08). The 02-01 up day counts for February although its streak started in January.

**Code:** run with `python3 -I`.
```python
# Q26: up/down/flat labels, up days per month, three rises in a row with LAG
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE stock_prices(trade_date TEXT PRIMARY KEY, close_price REAL);
INSERT INTO stock_prices VALUES
 ('2024-01-29',10),('2024-01-30',11),('2024-01-31',12),('2024-02-01',13),('2024-02-02',13),
 ('2024-02-05',12),('2024-02-06',13),('2024-02-07',14),('2024-02-08',15),('2024-02-09',14);
"""
# one ticker, one row per trade_date (PRIMARY KEY). With several tickers add PARTITION BY ticker.
SQL_MAIN = """
WITH l AS (
  SELECT trade_date, close_price,
         LAG(close_price, 1) OVER w AS p1,
         LAG(close_price, 2) OVER w AS p2,
         LAG(close_price, 3) OVER w AS p3
  FROM stock_prices
  WINDOW w AS (ORDER BY trade_date)
)
SELECT trade_date, close_price,
       CASE WHEN p1 IS NULL THEN NULL
            WHEN close_price > p1 THEN 'up'
            WHEN close_price < p1 THEN 'down'
            ELSE 'flat' END AS move,
       CASE WHEN p3 IS NULL THEN NULL
            WHEN close_price > p1 AND p1 > p2 AND p2 > p3 THEN 1 ELSE 0 END AS rose_3_days,
       CASE WHEN p2 IS NULL THEN NULL
            WHEN close_price > p1 AND p1 > p2 THEN 1 ELSE 0 END AS three_rising_closes
FROM l
ORDER BY trade_date
"""
SQL_MONTH = """
WITH l AS (
  SELECT trade_date, close_price, LAG(close_price) OVER (ORDER BY trade_date) AS p1
  FROM stock_prices
)
SELECT substr(trade_date, 1, 7) AS month,
       SUM(CASE WHEN close_price > p1 THEN 1 ELSE 0 END) AS up_days
FROM l
GROUP BY substr(trade_date, 1, 7)
ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_month = pd.read_sql_query(SQL_MONTH, con)
print(sql_df.to_string(index=False))
print()
print(sql_month.to_string(index=False))

sp = pd.read_sql_query("SELECT * FROM stock_prices", con)
# pd:main
d = sp.sort_values("trade_date").reset_index(drop=True)
diff = d["close_price"].diff()
d["move"] = np.select([diff.isna(), diff > 0, diff < 0], [None, "up", "down"], default="flat")
up = diff > 0
d["three_rising_closes"] = (up & up.shift(1, fill_value=False)).astype(int).where(diff.shift(1).notna())
d["rose_3_days"] = (up & up.shift(1, fill_value=False) & up.shift(2, fill_value=False)).astype(int).where(diff.shift(2).notna())
up_days = up.groupby(d["trade_date"].str[:7]).sum().astype(int).rename("up_days").reset_index().rename(columns={"trade_date": "month"})
# pd:end
pd_df = d[["trade_date", "close_price", "move", "rose_3_days", "three_rising_closes"]]
# compared after sorting by trade_date; NaN and None are both NULL
a = sql_df.copy(); b = pd_df.copy()
for col in ("move",):
    a[col] = a[col].astype(object).where(a[col].notna(), None)
    b[col] = b[col].astype(object).where(b[col].notna(), None)
assert a["move"].tolist() == b["move"].tolist()
for col in ("rose_3_days", "three_rising_closes"):
    pd.testing.assert_series_equal(sql_df[col].astype("float64"), pd_df[col].astype("float64"), check_names=False)
pd.testing.assert_frame_equal(sql_month, up_days, check_dtype=False)
print("\npandas up-days per month:", dict(zip(up_days["month"], up_days["up_days"])))
print("asserts passed: SQL LAG labels, flags and monthly counts == pandas diff/shift")
```

**Output (my run):**
```text
trade_date  close_price move  rose_3_days  three_rising_closes
2024-01-29         10.0  NaN          NaN                  NaN
2024-01-30         11.0   up          NaN                  NaN
2024-01-31         12.0   up          NaN                  1.0
2024-02-01         13.0   up          1.0                  1.0
2024-02-02         13.0 flat          0.0                  0.0
2024-02-05         12.0 down          0.0                  0.0
2024-02-06         13.0   up          0.0                  0.0
2024-02-07         14.0   up          0.0                  1.0
2024-02-08         15.0   up          1.0                  1.0
2024-02-09         14.0 down          0.0                  0.0

  month  up_days
2024-01        2
2024-02        4

pandas up-days per month: {'2024-01': 2, '2024-02': 4}
asserts passed: SQL LAG labels, flags and monthly counts == pandas diff/shift
```

**Edge cases:**
- **First rows:** `LAG` is NULL at the start, so the label is NULL, and a flag needing `LAG(3)` is NULL for the first three rows; that is "not enough history", not "no".
- **Flat days:** `close = prev` is neither up nor down; a three-in-a-row rule with `>` breaks on a flat day, which is usually what you want.
- **NULL close:** any comparison with NULL is unknown, so the label and flags go NULL for that row and for the rows that look back at it. Decide whether to drop or fill first.
- **Missing trading days:** `LAG` compares with the previous row, which for a market is the previous trading day, which is what you want; for calendar-day questions see Q13 and Q16.
- **Duplicate dates:** the primary key rules them out; otherwise aggregate first, or the `LAG` order is not well defined.

**Then explain:**
- `WINDOW w AS (ORDER BY trade_date)` is a named window reused by three `LAG` calls; I did not repeat the ORDER BY.
- You cannot filter on a window result in WHERE, hence the CTE.
- pandas: `diff() > 0` is the up series; `up & up.shift(1) & up.shift(2)` is the same logic as the chained comparisons, with `fill_value=False` for the edges and `.where(...)` to put NULL back where history is missing.
- LeetCode 180 (Consecutive Numbers) uses the same LAG(1), LAG(2) idea with equality. I know it by title only (Wave A notes), so I do not quote its statement. The longest streak of any length is a gaps-and-islands problem (Part 7).

**Follow-ups:**
- *Longest streak of up days?* Gaps and islands, Part 7.
- *Up days per month including days with zero?* Months with no up days still have a row here because every month has trading days; for months with no rows at all, join a month calendar.
- *Compare to the same weekday last week?* `LAG(close, 5)` if trading days are Monday to Friday and none missing; else a join on date.

**Common mistakes:**
- Calling two LAG comparisons "three days in a row" (that is three closes, two rises).
- Treating NULL (not enough history) as 0.
- Using `LAG` across tickers without `PARTITION BY`.

### Q27 ⭐⭐ 🟡 Differences of a cumulative counter with resets: meter_readings(meter_id, read_ts, reading) where reading is a cumulative counter that sometimes resets to 0 after maintenance. Compute the usage per interval as reading - LAG(reading) per meter, treat a negative difference as a reset (use the new reading as the usage) with CASE, and give the pandas diff() and where() version. Explain what you would do about a missing reading.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Usage per interval is `reading - LAG(reading)` per meter, but when the difference is negative the counter has reset, so use the new reading as the usage (`CASE WHEN reading >= prev THEN reading - prev ELSE reading END`); first readings stay NULL, and a missing reading is dropped first so that the next interval spans the gap.

**Schema and sample data:** meter 1 resets between 10:00 (160) and 11:00 (20); meter 2 has a NULL reading at 10:00; meter 3 has one reading. `(meter_id, read_ts)` is the primary key, so the order inside a meter is unique.
```sql
CREATE TABLE meter_readings(meter_id INTEGER, read_ts TEXT, reading INTEGER,
                            PRIMARY KEY (meter_id, read_ts));
INSERT INTO meter_readings VALUES
 (1,'2024-03-01 08:00',100),(1,'2024-03-01 09:00',130),(1,'2024-03-01 10:00',160),
 (1,'2024-03-01 11:00',20),(1,'2024-03-01 12:00',50),
 (2,'2024-03-01 08:00',500),(2,'2024-03-01 09:00',520),(2,'2024-03-01 10:00',NULL),
 (2,'2024-03-01 11:00',560),
 (3,'2024-03-01 08:00',70);
```

**SQL answer:**
```sql
WITH r AS (
  SELECT meter_id, read_ts, reading,
         LAG(reading) OVER w AS prev_reading,
         LAG(read_ts) OVER w AS prev_ts
  FROM meter_readings
  WHERE reading IS NOT NULL
  WINDOW w AS (PARTITION BY meter_id ORDER BY read_ts)
)
SELECT meter_id, read_ts, reading, prev_reading,
       CASE WHEN prev_reading IS NULL THEN NULL
            WHEN reading >= prev_reading THEN reading - prev_reading
            ELSE reading END AS usage,
       CASE WHEN prev_reading IS NOT NULL AND reading < prev_reading THEN 1 ELSE 0 END AS reset_flag,
       ROUND((julianday(read_ts) - julianday(prev_ts)) * 24, 1) AS hours
FROM r
ORDER BY meter_id, read_ts
```

**pandas answer:** `diff()` per meter, then `where` keeps the difference where it is not negative and substitutes the reading otherwise. The extra `diff.isna() |` matters: without it the NaN of a first reading counts as "not non-negative" and gets replaced by the reading.
```py
m = mr.dropna(subset=["reading"]).sort_values(["meter_id", "read_ts"]).reset_index(drop=True)
g = m.groupby("meter_id")
m["prev_reading"] = g["reading"].shift(1)
diff = g["reading"].diff()
m["usage"] = diff.where(diff.isna() | (diff >= 0), m["reading"])
m["reset_flag"] = (diff < 0).astype(int)
prev_ts = g["read_ts"].shift(1)
m["hours"] = ((pd.to_datetime(m["read_ts"]) - pd.to_datetime(prev_ts)).dt.total_seconds() / 3600).round(1)
```

**Example:** meter 1: 100, 130, 160, 20, 50.
- 09:00 and 10:00: 30 and 30.
- 11:00: 20 - 160 = -140 is negative, so the counter reset; usage is the new reading, 20 (assumes it restarted from 0 and counted 20 since).
- 12:00: 50 - 20 = 30.
- Meter 2: 500, 520, (NULL), 560. With the NULL row removed, 11:00 is compared with 09:00: 560 - 520 = 40 over 2 hours.
- First readings (and the single reading of meter 3) have no previous row: NULL.

**Code:** run with `python3 -I`.
```python
# Q27: usage per interval from a cumulative counter that can reset
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE meter_readings(meter_id INTEGER, read_ts TEXT, reading INTEGER,
                            PRIMARY KEY (meter_id, read_ts));
INSERT INTO meter_readings VALUES
 (1,'2024-03-01 08:00',100),(1,'2024-03-01 09:00',130),(1,'2024-03-01 10:00',160),
 (1,'2024-03-01 11:00',20),(1,'2024-03-01 12:00',50),
 (2,'2024-03-01 08:00',500),(2,'2024-03-01 09:00',520),(2,'2024-03-01 10:00',NULL),
 (2,'2024-03-01 11:00',560),
 (3,'2024-03-01 08:00',70);
"""
# PRIMARY KEY (meter_id, read_ts) makes the order unique. NULL readings are dropped first,
# so the next interval simply spans the gap (hours column shows how long).
SQL_MAIN = """
WITH r AS (
  SELECT meter_id, read_ts, reading,
         LAG(reading) OVER w AS prev_reading,
         LAG(read_ts) OVER w AS prev_ts
  FROM meter_readings
  WHERE reading IS NOT NULL
  WINDOW w AS (PARTITION BY meter_id ORDER BY read_ts)
)
SELECT meter_id, read_ts, reading, prev_reading,
       CASE WHEN prev_reading IS NULL THEN NULL
            WHEN reading >= prev_reading THEN reading - prev_reading
            ELSE reading END AS usage,
       CASE WHEN prev_reading IS NOT NULL AND reading < prev_reading THEN 1 ELSE 0 END AS reset_flag,
       ROUND((julianday(read_ts) - julianday(prev_ts)) * 24, 1) AS hours
FROM r
ORDER BY meter_id, read_ts
"""
SQL_NAIVE = """
SELECT meter_id, read_ts, reading - LAG(reading) OVER (PARTITION BY meter_id ORDER BY read_ts) AS naive_diff
FROM meter_readings ORDER BY meter_id, read_ts
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nnaive reading - LAG(reading), NULL rows kept in:")
print(pd.read_sql_query(SQL_NAIVE, con).to_string(index=False))
try:
    con.execute("INSERT INTO meter_readings VALUES (1,'2024-03-01 08:00',999)")
except sqlite3.IntegrityError as e:
    print("\nduplicate (meter_id, read_ts) rejected:", e)

mr = pd.read_sql_query("SELECT * FROM meter_readings", con)
# pd:main
m = mr.dropna(subset=["reading"]).sort_values(["meter_id", "read_ts"]).reset_index(drop=True)
g = m.groupby("meter_id")
m["prev_reading"] = g["reading"].shift(1)
diff = g["reading"].diff()
m["usage"] = diff.where(diff.isna() | (diff >= 0), m["reading"])
m["reset_flag"] = (diff < 0).astype(int)
prev_ts = g["read_ts"].shift(1)
m["hours"] = ((pd.to_datetime(m["read_ts"]) - pd.to_datetime(prev_ts)).dt.total_seconds() / 3600).round(1)
# pd:end
naive = diff.where(diff >= 0, m["reading"])
pd_df = m[["meter_id", "read_ts", "reading", "prev_reading", "usage", "reset_flag", "hours"]]
# compared after sorting by meter_id, read_ts; NaN equals NULL
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\npandas usage:", m["usage"].tolist())
print("naive diff.where(diff >= 0, reading) wrongly fills first readings:", naive.tolist())
print("asserts passed: SQL LAG == pandas groupby diff/where")
```

**Output (my run):**
```text
 meter_id          read_ts  reading  prev_reading  usage  reset_flag  hours
        1 2024-03-01 08:00      100           NaN    NaN           0    NaN
        1 2024-03-01 09:00      130         100.0   30.0           0    1.0
        1 2024-03-01 10:00      160         130.0   30.0           0    1.0
        1 2024-03-01 11:00       20         160.0   20.0           1    1.0
        1 2024-03-01 12:00       50          20.0   30.0           0    1.0
        2 2024-03-01 08:00      500           NaN    NaN           0    NaN
        2 2024-03-01 09:00      520         500.0   20.0           0    1.0
        2 2024-03-01 11:00      560         520.0   40.0           0    2.0
        3 2024-03-01 08:00       70           NaN    NaN           0    NaN

naive reading - LAG(reading), NULL rows kept in:
 meter_id          read_ts  naive_diff
        1 2024-03-01 08:00         NaN
        1 2024-03-01 09:00        30.0
        1 2024-03-01 10:00        30.0
        1 2024-03-01 11:00      -140.0
        1 2024-03-01 12:00        30.0
        2 2024-03-01 08:00         NaN
        2 2024-03-01 09:00        20.0
        2 2024-03-01 10:00         NaN
        2 2024-03-01 11:00         NaN
        3 2024-03-01 08:00         NaN

duplicate (meter_id, read_ts) rejected: UNIQUE constraint failed: meter_readings.meter_id, meter_readings.read_ts

pandas usage: [nan, 30.0, 30.0, 20.0, 30.0, nan, 20.0, 40.0, nan]
naive diff.where(diff >= 0, reading) wrongly fills first readings: [100.0, 30.0, 30.0, 20.0, 30.0, 500.0, 20.0, 40.0, 70.0]
asserts passed: SQL LAG == pandas groupby diff/where
```

**Edge cases:**
- **Reset assumption:** `reading` after a reset is taken as the usage in the interval. Usage between the last pre-reset reading and the reset itself is lost, and a reset to a non-zero value, or a reset followed by enough growth to exceed the old reading, is indistinguishable from normal growth. Say so in the interview and ask whether the device logs a reset event.
- **Missing reading (NULL):** the naive `reading - LAG(reading)` with the NULL row left in gives NULL for the NULL row and also for the next row (output above: meter 2 loses both 10:00 and 11:00). Filtering NULL readings first keeps the 11:00 usage, as a longer interval, and the `hours` column shows the interval length so the consumer can see it. Do not spread it evenly over the gap unless the business agrees. If a reset hid inside the gap, you cannot tell.
- **Duplicate timestamps:** the primary key rejects them (my run shows the error). If they are possible, aggregate or add a reading id as a tie-breaker.
- **Equal reading** (`reading = prev`): usage 0, not a reset (`>=`).
- **Single-reading meter:** no interval, NULL.

**Then explain:**
- `LAG` with `PARTITION BY meter_id` so one meter's last reading is never the next meter's previous reading.
- pandas `where(cond, other)` keeps values where `cond` is True; the printed `naive` version in the Output shows the first-reading trap (it fills 100, 500 and 70).
- This is a per-row problem (one `LAG`), so no recursion or islands are needed; a counter that resets without a clear drop is harder.

**Follow-ups:**
- *Total usage per meter?* `SUM(usage)` of the column above.
- *Resets only if the new reading is below some fraction of the old?* Add a threshold to the CASE.
- *Rollover of a fixed-width counter (for example it wraps at 9999)?* Usage = reading + 10000 - prev if you know the maximum; that is a different rule from "reset to 0".

**Common mistakes:**
- Letting a negative difference stand as negative usage.
- Leaving NULL rows in, which loses the next interval as well.
- In pandas, `where` without protecting the NaN first rows.

### Q28 ⭐⭐ 🟡 Orders in the trailing 7 days for each order row: orders(order_id, customer_id, order_date, amount). For every order, return the count and sum of that customer's orders in the 7 days up to and including that order (same customer). Show the RANGE window on julianday(order_date) with PARTITION BY customer_id, the correlated-subquery alternative, and the pandas groupby().rolling('7D', on='order_date') version; explain which handles several orders on the same day.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Partition by customer and run a RANGE frame over `julianday(order_date)` with `6 PRECEDING AND CURRENT ROW`; a correlated subquery gives the same answer, and both count every order on the same day as a peer, whereas pandas `groupby().rolling('7D', on=...)` moves row by row inside a day, so you give each same-day row the last row's value to match.

**Schema and sample data:** customer 1 has two orders on 2024-05-03; customer 2 has two orders ten days apart; customer 3 has one order.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-05-01',10),(2,1,'2024-05-03',20),(3,1,'2024-05-03',30),(4,1,'2024-05-07',40),
 (5,1,'2024-05-10',50),(6,2,'2024-05-02',5),(7,2,'2024-05-12',6),(8,3,'2024-05-04',7);
```

**SQL answer:** window version (named window, used twice), then the correlated-subquery alternative `SQL_SUBQ`.
```sql
SELECT order_id, customer_id, order_date, amount,
       COUNT(*)    OVER w AS orders_7d,
       SUM(amount) OVER w AS amount_7d
FROM orders
WINDOW w AS (PARTITION BY customer_id ORDER BY julianday(order_date)
             RANGE BETWEEN 6 PRECEDING AND CURRENT ROW)
ORDER BY customer_id, order_date, order_id
```
```sql
SELECT o.order_id, o.customer_id, o.order_date, o.amount,
       (SELECT COUNT(*) FROM orders p
         WHERE p.customer_id = o.customer_id
           AND julianday(p.order_date) BETWEEN julianday(o.order_date) - 6 AND julianday(o.order_date)) AS orders_7d,
       (SELECT SUM(p.amount) FROM orders p
         WHERE p.customer_id = o.customer_id
           AND julianday(p.order_date) BETWEEN julianday(o.order_date) - 6 AND julianday(o.order_date)) AS amount_7d
FROM orders o
ORDER BY o.customer_id, o.order_date, o.order_id
```

**pandas answer:** sort first (the `on` column must be monotonic inside each group), use a column of ones to count, then fix the peers. `groupby().rolling()` returns its rows grouped by customer in sorted order, so I assign with `to_numpy()` after sorting; the assert against SQL guards that alignment.
```py
o = orders.assign(order_date=pd.to_datetime(orders["order_date"]), one=1)
o = o.sort_values(["customer_id", "order_date", "order_id"]).reset_index(drop=True)
r = o.groupby("customer_id").rolling("7D", on="order_date")[["one", "amount"]].sum()
o["row_orders_7d"] = r["one"].to_numpy()
o["row_amount_7d"] = r["amount"].to_numpy()
# same-day orders are peers in SQL RANGE: give each one the value of the last row of its day
day = o.groupby(["customer_id", "order_date"])
o["orders_7d"] = day["row_orders_7d"].transform("last").astype(int)
o["amount_7d"] = day["row_amount_7d"].transform("last").astype(int)
```

**Example:** customer 1 orders: 05-01 (10), 05-03 (20), 05-03 (30), 05-07 (40), 05-10 (50).
- 05-03, either order: the window is 04-27 to 05-03, which holds 10, 20, 30, so count 3 and sum 60, for both rows. The second 05-03 row is a peer of the first, so it sees the first even though it was not "before" it.
- 05-07: 05-01 to 05-07 holds 10, 20, 30, 40: count 4, sum 100.
- 05-10: 05-04 to 05-10 holds 40 and 50: count 2, sum 90.
- Customer 2: 05-12 looks back to 05-06, so the 05-02 order is out: count 1.

**Code:** run with `python3 -I`.
```python
# Q28: per customer, count and sum of orders in the 7 days up to and including each order
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-05-01',10),(2,1,'2024-05-03',20),(3,1,'2024-05-03',30),(4,1,'2024-05-07',40),
 (5,1,'2024-05-10',50),(6,2,'2024-05-02',5),(7,2,'2024-05-12',6),(8,3,'2024-05-04',7);
"""
# window = same customer, order_date - 6 days .. order_date. Same-day orders are peers: all of them count.
SQL_MAIN = """
SELECT order_id, customer_id, order_date, amount,
       COUNT(*)    OVER w AS orders_7d,
       SUM(amount) OVER w AS amount_7d
FROM orders
WINDOW w AS (PARTITION BY customer_id ORDER BY julianday(order_date)
             RANGE BETWEEN 6 PRECEDING AND CURRENT ROW)
ORDER BY customer_id, order_date, order_id
"""
SQL_SUBQ = """
SELECT o.order_id, o.customer_id, o.order_date, o.amount,
       (SELECT COUNT(*) FROM orders p
         WHERE p.customer_id = o.customer_id
           AND julianday(p.order_date) BETWEEN julianday(o.order_date) - 6 AND julianday(o.order_date)) AS orders_7d,
       (SELECT SUM(p.amount) FROM orders p
         WHERE p.customer_id = o.customer_id
           AND julianday(p.order_date) BETWEEN julianday(o.order_date) - 6 AND julianday(o.order_date)) AS amount_7d
FROM orders o
ORDER BY o.customer_id, o.order_date, o.order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sub_df = pd.read_sql_query(SQL_SUBQ, con)
print(sql_df.to_string(index=False))
assert sql_df.equals(sub_df)
print("\ncorrelated subquery gives the same rows: True")

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.assign(order_date=pd.to_datetime(orders["order_date"]), one=1)
o = o.sort_values(["customer_id", "order_date", "order_id"]).reset_index(drop=True)
r = o.groupby("customer_id").rolling("7D", on="order_date")[["one", "amount"]].sum()
o["row_orders_7d"] = r["one"].to_numpy()
o["row_amount_7d"] = r["amount"].to_numpy()
# same-day orders are peers in SQL RANGE: give each one the value of the last row of its day
day = o.groupby(["customer_id", "order_date"])
o["orders_7d"] = day["row_orders_7d"].transform("last").astype(int)
o["amount_7d"] = day["row_amount_7d"].transform("last").astype(int)
# pd:end
pd_df = o.assign(order_date=o["order_date"].dt.strftime("%Y-%m-%d"))[["order_id", "customer_id", "order_date", "amount", "orders_7d", "amount_7d"]]
# compared in the order customer_id, order_date, order_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\npandas row-by-row rolling before the peer fix:")
print(o[["order_id", "customer_id", "order_date", "row_orders_7d", "row_amount_7d"]].to_string(index=False))
print("asserts passed: SQL RANGE == correlated subquery == pandas groupby().rolling('7D', on=...) with peer fix")
```

**Output (my run):**
```text
 order_id  customer_id order_date  amount  orders_7d  amount_7d
        1            1 2024-05-01      10          1         10
        2            1 2024-05-03      20          3         60
        3            1 2024-05-03      30          3         60
        4            1 2024-05-07      40          4        100
        5            1 2024-05-10      50          2         90
        6            2 2024-05-02       5          1          5
        7            2 2024-05-12       6          1          6
        8            3 2024-05-04       7          1          7

correlated subquery gives the same rows: True

pandas row-by-row rolling before the peer fix:
 order_id  customer_id order_date  row_orders_7d  row_amount_7d
        1            1 2024-05-01            1.0           10.0
        2            1 2024-05-03            2.0           30.0
        3            1 2024-05-03            3.0           60.0
        4            1 2024-05-07            4.0          100.0
        5            1 2024-05-10            2.0           90.0
        6            2 2024-05-02            1.0            5.0
        7            2 2024-05-12            1.0            6.0
        8            3 2024-05-04            1.0            7.0
asserts passed: SQL RANGE == correlated subquery == pandas groupby().rolling('7D', on=...) with peer fix
```

**Edge cases:**
- **Several orders on the same day:** SQL RANGE and the correlated subquery both include all same-day orders for each of them (count 3 for both 05-03 rows). pandas row-by-row rolling gives 2 for the first same-day row and 3 for the second, because it only sees rows up to the current one; the Output shows these before the fix. Which one is right is a business decision ("orders in the 7 days up to this date" says SQL's). If you want "strictly before this order" use `ROWS` with `ORDER BY order_date, order_id`.
- **Timestamps:** here `order_date` is a date. With a time part, pandas `'7D'` would slide by exact time while the SQL day-number version would still be fractional days; cut both to the date for calendar semantics.
- **Customer with a gap larger than 7 days:** the window holds just the current day (customer 2).
- **NULL amount:** `SUM` skips it, `COUNT(*)` still counts the order; use `COUNT(amount)` if you want to count only non-NULL amounts.

**Then explain:**
- `PARTITION BY customer_id` restarts the window per customer; the ORDER BY is the day number; the frame is a value range, not a row count (Q24).
- The correlated subquery does the same by brute force: for each order it rescans that customer's orders. Easy to read, usually slower on large tables (I did not time it).
- pandas: `groupby().rolling('7D', on=...)` needs sorted data; unsorted data in my scratch run raised "Each group within d must be monotonic". The result's index is not the original row index, so assign by position after sorting, or merge on keys.

**Follow-ups:**
- *Distinct customers in the trailing 7 days overall?* A distinct count over a frame is not allowed (Q33); see Part 6/8.
- *Exclude the current order?* Subtract it, or a frame `7 PRECEDING AND 1 PRECEDING` with ROWS (Q35).

**Common mistakes:**
- No `PARTITION BY`, so one customer's orders fall into another's window.
- `ROWS BETWEEN 6 PRECEDING` for a calendar window.
- Not noticing that the pandas rolling index is not the original index.

### Q29 ⭐⭐ 🟡 Translate a SQL window pipeline to pandas groupby: given sales(store_id, sale_date, amount), write the SQL for previous-day amount (LAG), running total (SUM OVER) and running share of the store's total, then the pandas equivalent with sort_values, groupby().shift(fill_value=0), groupby().cumsum() and transform('sum'). Explain why you must sort first (SQL window ORDER BY is explicit, pandas is by row order) and index alignment after transform, and assert both results match row by row.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** In SQL, `LAG(amount, 1, 0) OVER (PARTITION BY store_id ORDER BY sale_date)`, a running `SUM` over the same window and `SUM(amount) OVER (PARTITION BY store_id)` for the store total; in pandas, `sort_values(["store_id", "sale_date"])` first, then `groupby("store_id")["amount"]` with `shift(1, fill_value=0)`, `cumsum()` and `transform("sum")`, because SQL orders by its explicit ORDER BY while pandas uses whatever row order it has.

**Schema and sample data:** two stores, three days each, rows inserted out of date order on purpose; `(store_id, sale_date)` is the primary key, so each store has one row per date.
```sql
CREATE TABLE sales(store_id INTEGER, sale_date TEXT, amount INTEGER, PRIMARY KEY (store_id, sale_date));
INSERT INTO sales VALUES
 (1,'2024-01-03',30),(2,'2024-01-02',5),(1,'2024-01-01',10),(2,'2024-01-01',15),
 (1,'2024-01-02',20),(2,'2024-01-03',30);
```

**SQL answer:**
```sql
SELECT store_id, sale_date, amount,
       LAG(amount, 1, 0) OVER w AS prev_amount,
       SUM(amount) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(1.0 * SUM(amount) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                 / SUM(amount) OVER (PARTITION BY store_id), 4) AS running_share
FROM sales
WINDOW w AS (PARTITION BY store_id ORDER BY sale_date)
ORDER BY store_id, sale_date
```

**pandas answer:**
```py
s = sales.sort_values(["store_id", "sale_date"]).reset_index(drop=True)
g = s.groupby("store_id")["amount"]
s["prev_amount"] = g.shift(1, fill_value=0)
s["running_total"] = g.cumsum()
s["running_share"] = (s["running_total"] / g.transform("sum")).round(4)
```

**Example:** store 1 sales are 10, 20, 30 on 01-01 to 01-03; the store total is 60.
- previous amount: 0 (default), 10, 20.
- running total: 10, 30, 60.
- running share: 10/60 = 0.1667, 30/60 = 0.5, 60/60 = 1.
- Store 2 (15, 5, 30; total 50): previous 0, 15, 5; running 15, 20, 50; share 0.3, 0.4, 1.

**Code:** run with `python3 -I`.
```python
# Q29: SQL window pipeline (LAG, running total, running share of store total) translated to pandas
import sqlite3
import pandas as pd

# rows inserted OUT of date order on purpose; (store_id, sale_date) is unique
SCHEMA = """
CREATE TABLE sales(store_id INTEGER, sale_date TEXT, amount INTEGER, PRIMARY KEY (store_id, sale_date));
INSERT INTO sales VALUES
 (1,'2024-01-03',30),(2,'2024-01-02',5),(1,'2024-01-01',10),(2,'2024-01-01',15),
 (1,'2024-01-02',20),(2,'2024-01-03',30);
"""
SQL_MAIN = """
SELECT store_id, sale_date, amount,
       LAG(amount, 1, 0) OVER w AS prev_amount,
       SUM(amount) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(1.0 * SUM(amount) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                 / SUM(amount) OVER (PARTITION BY store_id), 4) AS running_share
FROM sales
WINDOW w AS (PARTITION BY store_id ORDER BY sale_date)
ORDER BY store_id, sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

# read in storage order (the order rows were inserted), not date order
sales = pd.read_sql_query("SELECT * FROM sales ORDER BY rowid", con)
print("\nstorage order seen by pandas:", list(zip(sales["store_id"], sales["sale_date"])))

# pd:main
s = sales.sort_values(["store_id", "sale_date"]).reset_index(drop=True)
g = s.groupby("store_id")["amount"]
s["prev_amount"] = g.shift(1, fill_value=0)
s["running_total"] = g.cumsum()
s["running_share"] = (s["running_total"] / g.transform("sum")).round(4)
# pd:end
# compared in the order store_id, sale_date
pd.testing.assert_frame_equal(sql_df, s, check_dtype=False)

# trap 1: forget sort_values, cumsum follows row order
bad = sales.copy()
bad["running_total"] = bad.groupby("store_id")["amount"].cumsum()
print("\nwithout sorting, running_total in storage order:", bad["running_total"].tolist())
assert not (bad.sort_values(["store_id", "sale_date"])["running_total"].tolist() == sql_df["running_total"].tolist())

# trap 2: index alignment. Assigning a Series aligns on index LABELS; assigning .to_numpy() aligns on position
ordered = sales.sort_values(["store_id", "sale_date"])          # keeps the old index labels
by_label = sales.assign(running_total=ordered.groupby("store_id")["amount"].cumsum())
by_position = sales.assign(running_total=ordered.groupby("store_id")["amount"].cumsum().to_numpy())
want = sql_df.set_index(["store_id", "sale_date"])["running_total"]
ok_label = by_label.set_index(["store_id", "sale_date"])["running_total"].reindex(want.index).equals(want)
ok_pos = by_position.set_index(["store_id", "sale_date"])["running_total"].reindex(want.index).equals(want)
print("assign Series back to the unsorted frame (label alignment) correct:", ok_label)
print("assign .to_numpy() back to the unsorted frame (position) correct:", ok_pos)
assert ok_label and not ok_pos
print("asserts passed: SQL window pipeline == pandas groupby pipeline")
```

**Output (my run):**
```text
 store_id  sale_date  amount  prev_amount  running_total  running_share
        1 2024-01-01      10            0             10         0.1667
        1 2024-01-02      20           10             30         0.5000
        1 2024-01-03      30           20             60         1.0000
        2 2024-01-01      15            0             15         0.3000
        2 2024-01-02       5           15             20         0.4000
        2 2024-01-03      30            5             50         1.0000

storage order seen by pandas: [(1, '2024-01-03'), (2, '2024-01-02'), (1, '2024-01-01'), (2, '2024-01-01'), (1, '2024-01-02'), (2, '2024-01-03')]

without sorting, running_total in storage order: [30, 5, 40, 20, 60, 50]
assign Series back to the unsorted frame (label alignment) correct: True
assign .to_numpy() back to the unsorted frame (position) correct: False
asserts passed: SQL window pipeline == pandas groupby pipeline
```

**Edge cases:**
- **Unsorted pandas:** on the storage order the unsorted cumsum gives 30, 5, 40, 20, 60, 50, which is meaningless as a running total. SQL does not have this trap because the order is in the query.
- **Index alignment:** after sorting, the frame keeps its old index labels. Assigning a Series (such as the result of `cumsum()` on the sorted frame) back to the unsorted frame aligns on labels and is right (printed True); assigning `.to_numpy()` aligns on position and is wrong (printed False). `transform` returns a Series with the same index as its input, which is why it lines up.
- **Duplicate (store, date):** the primary key rules them out. Without it, add a tie-breaker to both the SQL ORDER BY and `sort_values`; otherwise tied rows get an arbitrary order in both.
- **NULL amount:** SUM and `cumsum` skip it (Q18); the share's denominator also skips it.
- **Store total of zero:** the share is a division by zero; use `NULLIF` in SQL, and pandas would give `inf` or NaN.
- **Float comparison:** I rounded shares to 4 places on both sides before the assert.

**Then explain:**
- `PARTITION BY store_id` is `groupby("store_id")`; the window ORDER BY is the `sort_values` you must do yourself; `LAG(x, 1, 0)` is `shift(1, fill_value=0)`.
- `SUM(...) OVER (PARTITION BY store_id)` with no ORDER BY is the whole-partition total, which is `transform("sum")`.
- The running total uses an explicit ROWS frame so a tie in the date could not merge rows into peers (Q6).

**Follow-ups:**
- *Why not groupby().sum()?* It collapses to one row per store; `transform` keeps one row per input row.
- *Why sort inside the pipeline rather than before?* So the code states its own assumption; a sort three steps earlier is easy to break.

**Common mistakes:**
- Forgetting `sort_values` and trusting the row order.
- Assigning a NumPy array back to an unsorted frame.
- Forgetting `fill_value=0`, which leaves NaN and turns the column to float.

### Q30 ⭐⭐ 🟡 shift versus LAG and LEAD in detail: series daily_sales(sale_date, amount). Show LAG(amount, 1, NULL) versus shift(1), the default value and fill_value, negative periods as LEAD, shift(freq='D') which moves the index rather than the data and is not the same as shift(periods), the integer-to-float upcast after shift with NaN and how Int64 or fill_value avoids it, and the difference with missing dates. Run and compare.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `LAG(amount, n, default)` and `shift(n, fill_value=...)` both look n rows back (position, not date), a negative shift is `LEAD`, `shift(freq="D")` is different (it moves the index labels, so values land on the next calendar day and nothing is lost or filled), and a shift that introduces NaN turns an integer column into float64 unless you pass `fill_value` or use `Int64`.

**Schema and sample data:** four days with 2024-01-03 missing.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',10),('2024-01-02',20),('2024-01-04',40),('2024-01-05',50);
```

**SQL answer:** row-based `LAG` and `LEAD`; and, for what `shift(freq='D')` does, a self-join on the previous calendar day (`SQL_DAY` in the Code block).
```sql
SELECT sale_date, amount,
       LAG(amount, 1, NULL) OVER w AS lag_row,
       LAG(amount, 1, 0)    OVER w AS lag_row_0,
       LEAD(amount)         OVER w AS lead_row
FROM daily_sales
WINDOW w AS (ORDER BY sale_date)
ORDER BY sale_date
```
```sql
SELECT a.sale_date, b.amount AS prev_calendar_day
FROM daily_sales a LEFT JOIN daily_sales b ON b.sale_date = date(a.sale_date, '-1 day')
ORDER BY a.sale_date
```

**pandas answer:**
```py
ds["sale_date"] = pd.to_datetime(ds["sale_date"])
s = ds.set_index("sale_date")["amount"]
out = pd.DataFrame({"amount": s,
                    "lag_row": s.shift(1),
                    "lag_row_0": s.shift(1, fill_value=0),
                    "lead_row": s.shift(-1)})
by_day = s.shift(freq="D").reindex(s.index)
```

**Example:** amounts 10, 20, 40, 50 on 01-01, 01-02, 01-04, 01-05.
- `LAG(amount, 1, NULL)` and `shift(1)`: NULL/NaN, 10, 20, 40. With default 0 / `fill_value=0`: 0, 10, 20, 40.
- `LEAD` and `shift(-1)`: 20, 40, 50, NULL/NaN.
- 01-04 is preceded by the row 01-02, so `LAG` returns 20 although yesterday (01-03) has no sales. The previous calendar day by self-join, and `shift(freq="D")` reindexed to the original dates, give NULL for 01-01 and 01-04 and 10 and 40 for 01-02 and 01-05.

**Code:** run with `python3 -I`.
```python
# Q30: LAG/LEAD versus pandas shift (periods, fill_value, freq, dtype)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES ('2024-01-01',10),('2024-01-02',20),('2024-01-04',40),('2024-01-05',50);
"""
# 2024-01-03 is missing on purpose. LAG/LEAD look at the previous/next ROW, not the previous/next DAY.
SQL_MAIN = """
SELECT sale_date, amount,
       LAG(amount, 1, NULL) OVER w AS lag_row,
       LAG(amount, 1, 0)    OVER w AS lag_row_0,
       LEAD(amount)         OVER w AS lead_row
FROM daily_sales
WINDOW w AS (ORDER BY sale_date)
ORDER BY sale_date
"""
# what shift(freq='D') means in SQL: the amount on the previous CALENDAR day, by self-join
SQL_DAY = """
SELECT a.sale_date, b.amount AS prev_calendar_day
FROM daily_sales a LEFT JOIN daily_sales b ON b.sale_date = date(a.sale_date, '-1 day')
ORDER BY a.sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
day_df = pd.read_sql_query(SQL_DAY, con)
print(sql_df.to_string(index=False))
print()
print(day_df.to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
ds["sale_date"] = pd.to_datetime(ds["sale_date"])
s = ds.set_index("sale_date")["amount"]
out = pd.DataFrame({"amount": s,
                    "lag_row": s.shift(1),
                    "lag_row_0": s.shift(1, fill_value=0),
                    "lead_row": s.shift(-1)})
by_day = s.shift(freq="D").reindex(s.index)
# pd:end
out = out.reset_index()
out["sale_date"] = out["sale_date"].dt.strftime("%Y-%m-%d")
# compared in sale_date order; NaN equals NULL
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)
assert by_day.isna().tolist() == day_df["prev_calendar_day"].isna().tolist()
assert by_day.dropna().tolist() == day_df["prev_calendar_day"].dropna().tolist()

print("\ndtypes: amount", s.dtype, "| shift(1)", s.shift(1).dtype, "| shift(1, fill_value=0)", s.shift(1, fill_value=0).dtype,
      "| Int64 shift(1)", s.astype("Int64").shift(1).dtype)
print("Int64 shift(1):", s.astype("Int64").shift(1).tolist())
raw_freq = s.shift(freq="D")
print("\nshift(freq='D') moves the labels and keeps every value; index now:", [d.strftime("%m-%d") for d in raw_freq.index])
print("shift(freq='D') values:", raw_freq.tolist())
print("shift(freq='D') reindexed back to the original dates:", by_day.tolist())
print("shift(1) by position:", s.shift(1).tolist())
con.executescript("CREATE TABLE n(d INT, v INT); INSERT INTO n VALUES (1,5),(2,NULL),(3,7);")
print("\nstored NULL in the data: LAG(v,1,0) gives", [r[1] for r in con.execute("SELECT d, LAG(v,1,0) OVER (ORDER BY d) FROM n")],
      "| shift(1, fill_value=0) gives", pd.Series([5, None, 7]).shift(1, fill_value=0).tolist())
print("asserts passed: LAG/LEAD == shift(periods); self-join on the previous day == shift(freq='D')")
```

**Output (my run):**
```text
 sale_date  amount  lag_row  lag_row_0  lead_row
2024-01-01      10      NaN          0      20.0
2024-01-02      20     10.0         10      40.0
2024-01-04      40     20.0         20      50.0
2024-01-05      50     40.0         40       NaN

 sale_date  prev_calendar_day
2024-01-01                NaN
2024-01-02               10.0
2024-01-04                NaN
2024-01-05               40.0

dtypes: amount int64 | shift(1) float64 | shift(1, fill_value=0) int64 | Int64 shift(1) Int64
Int64 shift(1): [<NA>, 10, 20, 40]

shift(freq='D') moves the labels and keeps every value; index now: ['01-02', '01-03', '01-05', '01-06']
shift(freq='D') values: [10, 20, 40, 50]
shift(freq='D') reindexed back to the original dates: [nan, 10.0, nan, 40.0]
shift(1) by position: [nan, 10.0, 20.0, 40.0]

stored NULL in the data: LAG(v,1,0) gives [0, 5, None] | shift(1, fill_value=0) gives [0.0, 5.0, nan]
asserts passed: LAG/LEAD == shift(periods); self-join on the previous day == shift(freq='D')
```

**Edge cases:**
- **Missing dates:** `LAG` and `shift(n)` count rows. For "the value from yesterday" use the date: self-join or `shift(freq="D")`, or fill the calendar first (Q16).
- **`shift(freq="D")` moves the index:** the result has the same four values but dates 01-02, 01-03, 01-05, 01-06; no NaN appears at the ends, and a new date (01-06) shows up. To compare with the original rows I `reindex` it back, which produces the NaNs.
- **dtype:** `amount` is int64; `shift(1)` gives float64 (NaN needs float); `shift(1, fill_value=0)` stays int64; `astype("Int64")` then `shift(1)` stays `Int64` with `<NA>` (printed).
- **Edges:** the first row of `LAG` is NULL without a default, and the last row of `LEAD`; a partition boundary needs `PARTITION BY` in SQL and `groupby().shift()` in pandas.
- **Default with NULL data:** the LAG default and `fill_value` fill only the edge position that has no row to look at; a stored NULL or NaN in the data stays missing (last line of the Output: `[0, 5, None]` and `[0.0, 5.0, nan]`).

**Then explain:**
- Same idea, two spellings: offset by rows. `LAG(x, 1, 0)` ≈ `shift(1, fill_value=0)`; `LEAD(x)` ≈ `shift(-1)`.
- The default argument in SQL (third argument) is what `fill_value` is in pandas; a stored NULL stays NULL in both.
- `shift(freq=...)` is a time-series tool: it shifts the labels, which is handy for aligning a series with itself a day or a week later, and it is not the same as shifting the data.

**Follow-ups:**
- *Value a week earlier?* `LAG(amount, 7)` only with no missing days; else a date self-join.
- *Percent change?* Q4 and Q38; `pct_change` is built on `shift` and has its own `freq` argument.
- *Why does an integer column turn to float?* NaN does not exist in numpy integers; the nullable `Int64` can hold `<NA>`.

**Common mistakes:**
- Treating `shift(freq="D")` as `shift(1)`.
- Trusting `LAG(…, 7)` as "last week" when days are missing.
- Not seeing the int to float change and then printing 20.0 where 20 was expected.

### Q31 ⭐⭐ 🟡 pandas rolling versus SQL frames: show rolling(7).mean() (row-based, min_periods defaults to 7), rolling('7D', on='date').mean() (time-based, min_periods defaults to 1, closed='right' means (t-7D, t]), expanding().mean() as the running average, and how each corresponds to ROWS BETWEEN 6 PRECEDING, RANGE with a 6-day offset, and ROWS BETWEEN UNBOUNDED PRECEDING. Use data with a missing day and a duplicate date, run both sides and show where pandas and SQL differ.
**Asked at:** pandas reference pages (rolling, shift, pct_change; opened) and user guide, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `rolling(7)` is `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` with `min_periods` defaulting to 7 (SQL's AVG averages whatever rows exist, so it matches `rolling(7, min_periods=1)`), `rolling("7D", on=...)` is a time window (t - 7D, t] that matches `RANGE` over a 6-day offset but treats rows with the same date one after the other instead of as peers, and `expanding().mean()` is `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

**Schema and sample data:** nine rows; 2024-01-03 appears twice (ids 3 and 4); 01-04 and 01-07 are missing.
```sql
CREATE TABLE daily_sales(id INTEGER PRIMARY KEY, sale_date TEXT, amount INTEGER);
INSERT INTO daily_sales VALUES
 (1,'2024-01-01',10),(2,'2024-01-02',20),(3,'2024-01-03',30),(4,'2024-01-03',40),
 (5,'2024-01-05',50),(6,'2024-01-06',60),(7,'2024-01-08',70),(8,'2024-01-09',80),(9,'2024-01-10',90);
```

**SQL answer:** five frames side by side. `ROWS` frames use `ORDER BY sale_date, id` so ties are broken by `id`; the RANGE frame sums peers.
```sql
SELECT id, sale_date, amount,
       AVG(amount) OVER (ORDER BY sale_date, id ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rows6_avg,
       CASE WHEN COUNT(*) OVER (ORDER BY sale_date, id ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) = 7
            THEN AVG(amount) OVER (ORDER BY sale_date, id ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) END AS rows6_full,
       AVG(amount) OVER (ORDER BY julianday(sale_date) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS range6_avg,
       AVG(amount) OVER (ORDER BY sale_date, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_avg_rows,
       AVG(amount) OVER (ORDER BY sale_date) AS running_avg_default
FROM daily_sales
ORDER BY sale_date, id
```

**pandas answer:** `time7D` is the raw time-based rolling mean; `range6_avg` gives each same-date row the value of the last row of its date, which is what RANGE does with peers.
```py
p = pd.DataFrame({"id": ds["id"], "sale_date": ds["sale_date"].dt.strftime("%Y-%m-%d"), "amount": ds["amount"]})
p["rows6_avg"] = ds["amount"].rolling(7, min_periods=1).mean()
p["rows6_full"] = ds["amount"].rolling(7).mean()
p["time7D"] = ds.rolling("7D", on="sale_date")["amount"].mean()
p["range6_avg"] = p.groupby("sale_date")["time7D"].transform("last")
p["running_avg_rows"] = ds["amount"].expanding().mean()
p["running_avg_default"] = p.groupby("sale_date")["running_avg_rows"].transform("last")
```

**Example:** by hand for a few rows (ids sorted by date, then id).
- id 9 (01-10): `ROWS 6 PRECEDING` covers ids 3 to 9 = (30 + 40 + 50 + 60 + 70 + 80 + 90) / 7 = 60. The 7-day RANGE covers 01-04 to 01-10 = ids 5 to 9 = (50 + 60 + 70 + 80 + 90) / 5 = 70.
- id 7 (01-08): the RANGE window is 01-02 to 01-08 = 20, 30, 40, 50, 60, 70 over 6 rows = 45; the ROWS window (ids 1 to 7) gives 280 / 7 = 40.
- ids 3 and 4 (01-03): RANGE gives both rows (10 + 20 + 30 + 40) / 4 = 25. pandas `'7D'` gives 20 for id 3 (it has not yet "seen" id 4) and 25 for id 4.
- Running average at id 4: ROWS gives 25 (10, 20, 30, 40), and the default frame gives 25 for both date peers; at id 3 ROWS gives 20 and the default frame gives 25.

**Code:** run with `python3 -I`.
```python
# Q31: pandas rolling / expanding versus SQL ROWS, RANGE and UNBOUNDED frames
import sqlite3
import pandas as pd

# 2024-01-03 appears twice (ids 3 and 4); 01-04 and 01-07 are missing
SCHEMA = """
CREATE TABLE daily_sales(id INTEGER PRIMARY KEY, sale_date TEXT, amount INTEGER);
INSERT INTO daily_sales VALUES
 (1,'2024-01-01',10),(2,'2024-01-02',20),(3,'2024-01-03',30),(4,'2024-01-03',40),
 (5,'2024-01-05',50),(6,'2024-01-06',60),(7,'2024-01-08',70),(8,'2024-01-09',80),(9,'2024-01-10',90);
"""
# tie-breaker for ROWS and expanding: id. RANGE peers (same date) share one value.
SQL_MAIN = """
SELECT id, sale_date, amount,
       AVG(amount) OVER (ORDER BY sale_date, id ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rows6_avg,
       CASE WHEN COUNT(*) OVER (ORDER BY sale_date, id ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) = 7
            THEN AVG(amount) OVER (ORDER BY sale_date, id ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) END AS rows6_full,
       AVG(amount) OVER (ORDER BY julianday(sale_date) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS range6_avg,
       AVG(amount) OVER (ORDER BY sale_date, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_avg_rows,
       AVG(amount) OVER (ORDER BY sale_date) AS running_avg_default
FROM daily_sales
ORDER BY sale_date, id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.round(3).to_string(index=False))

ds = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date, id", con)
ds["sale_date"] = pd.to_datetime(ds["sale_date"])
# pd:main
p = pd.DataFrame({"id": ds["id"], "sale_date": ds["sale_date"].dt.strftime("%Y-%m-%d"), "amount": ds["amount"]})
p["rows6_avg"] = ds["amount"].rolling(7, min_periods=1).mean()
p["rows6_full"] = ds["amount"].rolling(7).mean()
p["time7D"] = ds.rolling("7D", on="sale_date")["amount"].mean()
p["range6_avg"] = p.groupby("sale_date")["time7D"].transform("last")
p["running_avg_rows"] = ds["amount"].expanding().mean()
p["running_avg_default"] = p.groupby("sale_date")["running_avg_rows"].transform("last")
# pd:end
# compared in the order sale_date, id; NaN equals NULL
cols = ["id", "sale_date", "amount", "rows6_avg", "rows6_full", "range6_avg", "running_avg_rows", "running_avg_default"]
pd.testing.assert_frame_equal(sql_df, p[cols], check_dtype=False)

print("\nwhere pandas and SQL differ before the peer fix (duplicate date, ids 3 and 4):")
print(pd.DataFrame({"id": p["id"], "sql_range6": sql_df["range6_avg"].round(3), "pandas_7D_raw": p["time7D"].round(3)}).to_string(index=False))

# closed= matters: default closed='right' is (t-7D, t]; a row exactly 7 days back is excluded
edge = pd.DataFrame({"d": pd.to_datetime(["2024-01-01", "2024-01-08"]), "v": [100, 1]})
print("\nrow exactly 7 days back, closed right :", edge.rolling("7D", on="d")["v"].sum().tolist())
print("row exactly 7 days back, closed both  :", edge.rolling("7D", on="d", closed="both")["v"].sum().tolist())
con.executescript("CREATE TABLE e(d TEXT, v INT); INSERT INTO e VALUES ('2024-01-01',100),('2024-01-08',1);")
print("SQL RANGE 6 PRECEDING                 :", [r[0] for r in con.execute("SELECT SUM(v) OVER (ORDER BY julianday(d) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) FROM e")])
print("SQL RANGE 7 PRECEDING                 :", [r[0] for r in con.execute("SELECT SUM(v) OVER (ORDER BY julianday(d) RANGE BETWEEN 7 PRECEDING AND CURRENT ROW) FROM e")])
print("asserts passed: ROWS == rolling(7, min_periods=1); RANGE == rolling('7D') after the peer fix; UNBOUNDED == expanding()")
```

**Output (my run):**
```text
 id  sale_date  amount  rows6_avg  rows6_full  range6_avg  running_avg_rows  running_avg_default
  1 2024-01-01      10       10.0         NaN        10.0              10.0                 10.0
  2 2024-01-02      20       15.0         NaN        15.0              15.0                 15.0
  3 2024-01-03      30       20.0         NaN        25.0              20.0                 25.0
  4 2024-01-03      40       25.0         NaN        25.0              25.0                 25.0
  5 2024-01-05      50       30.0         NaN        30.0              30.0                 30.0
  6 2024-01-06      60       35.0         NaN        35.0              35.0                 35.0
  7 2024-01-08      70       40.0        40.0        45.0              40.0                 40.0
  8 2024-01-09      80       50.0        50.0        55.0              45.0                 45.0
  9 2024-01-10      90       60.0        60.0        70.0              50.0                 50.0

where pandas and SQL differ before the peer fix (duplicate date, ids 3 and 4):
 id  sql_range6  pandas_7D_raw
  1        10.0           10.0
  2        15.0           15.0
  3        25.0           20.0
  4        25.0           25.0
  5        30.0           30.0
  6        35.0           35.0
  7        45.0           45.0
  8        55.0           55.0
  9        70.0           70.0

row exactly 7 days back, closed right : [100.0, 1.0]
row exactly 7 days back, closed both  : [100.0, 101.0]
SQL RANGE 6 PRECEDING                 : [100, 1]
SQL RANGE 7 PRECEDING                 : [100, 101]
asserts passed: ROWS == rolling(7, min_periods=1); RANGE == rolling('7D') after the peer fix; UNBOUNDED == expanding()
```

**Edge cases:**
- **min_periods:** `rolling(7)` gives NaN for the first six rows (`rows6_full`); SQL's `AVG` averages 1 to 6 rows there (`rows6_avg`), the same as `rolling(7, min_periods=1)`. To get NaN in SQL, test `COUNT(*) OVER (same frame) = 7` (as in `rows6_full`). For an offset window like `'7D'`, `min_periods` defaults to 1 (the first value in my run was not NaN).
- **Duplicate dates:** peers in SQL RANGE, row by row in pandas (id 3 differs, printed before the fix). The ROWS version needs a tie-breaker (`id`) to be deterministic; without one the tied rows can swap.
- **Missing days:** `rolling(7)` and ROWS count rows, so after a gap they reach back more than 7 days (id 9 averaged ids 3 to 9, which starts on 01-03). The time-based window handles it.
- **closed:** the default `closed="right"` is (t - 7D, t]. A row exactly 7 days back is excluded (`[100.0, 1.0]`); `closed="both"` includes it (`[100.0, 101.0]`), which matches SQL `RANGE 7 PRECEDING` (`[100, 101]`). SQL `6 PRECEDING` gave `[100, 1]`, matching the default.
- **Offsets must be fixed frequencies** in pandas rolling (docs say 'B' or 'ME' raise; I did not run them).

**Then explain:**
- Three kinds of frame: count of rows (`rolling(n)`, ROWS), span of time or value (`rolling('7D')`, RANGE), everything so far (`expanding()`, UNBOUNDED PRECEDING).
- `AVG(...) OVER (ORDER BY sale_date)` with no explicit frame is the RANGE-through-peers frame; `expanding()` is the ROWS version, so they differ on a duplicate date (the last two columns of the SQL output).
- Match them by choosing the frame explicitly in SQL and by fixing peers in pandas.

**Follow-ups:**
- *Centered window?* `rolling(3, center=True)` and `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` (Q21).
- *GROUPS frames?* No pandas equivalent that I know of; Q7.

**Common mistakes:**
- Assuming `rolling('7D')` and `RANGE` treat duplicate dates the same.
- Expecting `rolling(7)` to give partial means at the start.
- Using `ROWS` on data with missing days and calling it a 7-day average.

### Q32 ⭐⭐ 🟡 Year-to-date and period reset: monthly_sales(sale_month, revenue) with months across 2023 and 2024. Compute year-to-date revenue that resets every January using PARTITION BY year, the same-period-last-year YTD by joining or LAG, and the YTD growth percent. Show pandas groupby(year).cumsum(). Explain how PARTITION BY gives the reset and why a reset by arbitrary condition is harder (Part 7).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `SUM(revenue) OVER (PARTITION BY year ORDER BY month)` gives a running total that restarts in January because every year is its own partition; the same period last year comes from joining the YTD back to itself on (year - 1, same month) (or `LAG(ytd, 12)` only when no month is missing), and growth is `(ytd - ytd_ly) / NULLIF(ytd_ly, 0)`.

**Schema and sample data:** all twelve months of 2023 (10, 20, ... 120) and January to June 2024 (15, 25, ... 65); `sale_month` is the primary key, so one row per month.
```sql
CREATE TABLE monthly_sales(sale_month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_sales VALUES
 ('2023-01',10),('2023-02',20),('2023-03',30),('2023-04',40),('2023-05',50),('2023-06',60),
 ('2023-07',70),('2023-08',80),('2023-09',90),('2023-10',100),('2023-11',110),('2023-12',120),
 ('2024-01',15),('2024-02',25),('2024-03',35),('2024-04',45),('2024-05',55),('2024-06',65);
```

**SQL answer:** the join form is the main answer; `SQL_LAG` is the `LAG(ytd, 12)` alternative in the Code block.
```sql
WITH y AS (
  SELECT sale_month, CAST(substr(sale_month, 1, 4) AS INTEGER) AS yr, revenue,
         SUM(revenue) OVER (PARTITION BY substr(sale_month, 1, 4) ORDER BY sale_month
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS ytd
  FROM monthly_sales
)
SELECT c.sale_month, c.revenue, c.ytd,
       p.ytd AS ytd_last_year,
       ROUND(100.0 * (c.ytd - p.ytd) / NULLIF(p.ytd, 0), 1) AS ytd_growth_pct
FROM y c
LEFT JOIN y p ON p.yr = c.yr - 1 AND substr(p.sale_month, 6) = substr(c.sale_month, 6)
ORDER BY c.sale_month
```

**pandas answer:** `groupby(year).cumsum()` for the reset; a merge on (year + 1, month) for last year's YTD.
```py
m = ms.sort_values("sale_month").reset_index(drop=True)
m["yr"] = m["sale_month"].str[:4].astype(int)
m["ytd"] = m.groupby("yr")["revenue"].cumsum()
prev = m[["yr", "sale_month", "ytd"]].assign(yr=lambda f: f["yr"] + 1, mm=lambda f: f["sale_month"].str[5:]).drop(columns="sale_month")
m["mm"] = m["sale_month"].str[5:]
m = m.merge(prev.rename(columns={"ytd": "ytd_last_year"}), on=["yr", "mm"], how="left")
m["ytd_growth_pct"] = (100.0 * (m["ytd"] - m["ytd_last_year"]) / m["ytd_last_year"].where(m["ytd_last_year"] != 0)).round(1)
```

**Example:** 2023 YTD: 10, 30, 60, 100, 150, 210, ... 780 (December).
- 2024-01: YTD 15 (the sum restarted), last year's January YTD was 10, growth (15 - 10) / 10 = 50.0 percent.
- 2024-03: YTD 15 + 25 + 35 = 75 against 2023 YTD 60: (75 - 60) / 60 = 25.0 percent.
- 2024-06: YTD 240 against 210: 14.3 percent.
- 2023 rows have no earlier year: NULL.

**Code:** run with `python3 -I`.
```python
# Q32: year-to-date revenue with a reset every January, same-period-last-year YTD, YTD growth
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_sales(sale_month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_sales VALUES
 ('2023-01',10),('2023-02',20),('2023-03',30),('2023-04',40),('2023-05',50),('2023-06',60),
 ('2023-07',70),('2023-08',80),('2023-09',90),('2023-10',100),('2023-11',110),('2023-12',120),
 ('2024-01',15),('2024-02',25),('2024-03',35),('2024-04',45),('2024-05',55),('2024-06',65);
"""
# sale_month is unique (PRIMARY KEY), so the ROWS frame has no peers to worry about.
SQL_MAIN = """
WITH y AS (
  SELECT sale_month, CAST(substr(sale_month, 1, 4) AS INTEGER) AS yr, revenue,
         SUM(revenue) OVER (PARTITION BY substr(sale_month, 1, 4) ORDER BY sale_month
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS ytd
  FROM monthly_sales
)
SELECT c.sale_month, c.revenue, c.ytd,
       p.ytd AS ytd_last_year,
       ROUND(100.0 * (c.ytd - p.ytd) / NULLIF(p.ytd, 0), 1) AS ytd_growth_pct
FROM y c
LEFT JOIN y p ON p.yr = c.yr - 1 AND substr(p.sale_month, 6) = substr(c.sale_month, 6)
ORDER BY c.sale_month
"""
SQL_LAG = """
WITH y AS (
  SELECT sale_month, SUM(revenue) OVER (PARTITION BY substr(sale_month, 1, 4) ORDER BY sale_month) AS ytd
  FROM monthly_sales
)
SELECT sale_month, LAG(ytd, 12) OVER (ORDER BY sale_month) AS ytd_last_year FROM y ORDER BY sale_month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

ms = pd.read_sql_query("SELECT * FROM monthly_sales", con)
# pd:main
m = ms.sort_values("sale_month").reset_index(drop=True)
m["yr"] = m["sale_month"].str[:4].astype(int)
m["ytd"] = m.groupby("yr")["revenue"].cumsum()
prev = m[["yr", "sale_month", "ytd"]].assign(yr=lambda f: f["yr"] + 1, mm=lambda f: f["sale_month"].str[5:]).drop(columns="sale_month")
m["mm"] = m["sale_month"].str[5:]
m = m.merge(prev.rename(columns={"ytd": "ytd_last_year"}), on=["yr", "mm"], how="left")
m["ytd_growth_pct"] = (100.0 * (m["ytd"] - m["ytd_last_year"]) / m["ytd_last_year"].where(m["ytd_last_year"] != 0)).round(1)
# pd:end
# compared in sale_month order; NaN equals NULL
cols = ["sale_month", "revenue", "ytd", "ytd_last_year", "ytd_growth_pct"]
pd.testing.assert_frame_equal(sql_df, m[cols].sort_values("sale_month").reset_index(drop=True), check_dtype=False)

# the LAG(ytd, 12) route works only while no month is missing
lag_ok = pd.read_sql_query(SQL_LAG, con)["ytd_last_year"]
assert lag_ok.fillna(-1).tolist() == sql_df["ytd_last_year"].fillna(-1).tolist()
con.execute("DELETE FROM monthly_sales WHERE sale_month = '2023-03'")
join_gap = pd.read_sql_query(SQL_MAIN, con)
lag_gap = pd.read_sql_query(SQL_LAG, con)
print("\nwith 2023-03 deleted, ytd_last_year for 2024-01..2024-06:")
print("  join on (year - 1, same month):", join_gap["ytd_last_year"].tail(6).tolist())
print("  LAG(ytd, 12)                  :", lag_gap["ytd_last_year"].tail(6).tolist())
print("asserts passed: SQL PARTITION BY year == pandas groupby(year).cumsum(); LAG(12) == join when complete")
```

**Output (my run):**
```text
sale_month  revenue  ytd  ytd_last_year  ytd_growth_pct
   2023-01       10   10            NaN             NaN
   2023-02       20   30            NaN             NaN
   2023-03       30   60            NaN             NaN
   2023-04       40  100            NaN             NaN
   2023-05       50  150            NaN             NaN
   2023-06       60  210            NaN             NaN
   2023-07       70  280            NaN             NaN
   2023-08       80  360            NaN             NaN
   2023-09       90  450            NaN             NaN
   2023-10      100  550            NaN             NaN
   2023-11      110  660            NaN             NaN
   2023-12      120  780            NaN             NaN
   2024-01       15   15           10.0            50.0
   2024-02       25   40           30.0            33.3
   2024-03       35   75           60.0            25.0
   2024-04       45  120          100.0            20.0
   2024-05       55  175          150.0            16.7
   2024-06       65  240          210.0            14.3

with 2023-03 deleted, ytd_last_year for 2024-01..2024-06:
  join on (year - 1, same month): [10.0, 30.0, nan, 70.0, 120.0, 180.0]
  LAG(ytd, 12)                  : [nan, 10.0, 30.0, 70.0, 120.0, 180.0]
asserts passed: SQL PARTITION BY year == pandas groupby(year).cumsum(); LAG(12) == join when complete
```

**Edge cases:**
- **Missing month:** I deleted 2023-03 and re-ran. The join form gives NULL for 2024-03 (nothing to match) and correct values for the others; `LAG(ytd, 12)` shifts by 12 rows, so every 2024 row after the gap is paired with the wrong month (output above). Note also that 2023's YTD from April on is now short a month; that is a data problem, not a query problem.
- **Partial current year:** growth compares 2024 January to June with 2023 January to June because the join matches month by month; comparing 2024 YTD with all of 2023 would be a mistake.
- **Zero last-year YTD:** `NULLIF` makes growth NULL; pandas needs `.where(... != 0)` as in the code, otherwise it gives inf.
- **Fiscal years:** if the year starts in April, the partition key must be the fiscal year, not `substr(month, 1, 4)`.
- **Unique month:** with duplicate months the running total needs an ORDER BY tie-breaker or a frame ROWS; aggregate to one row per month first.

**Then explain:**
- `PARTITION BY` is a reset: each partition is computed independently, so the running total starts again when the key changes. `groupby(year).cumsum()` is the same idea.
- A reset by an arbitrary condition (for example "restart when the total passes 100") cannot be done with PARTITION BY alone: that is Q43 and Part 7.
- I compare with an explicit `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` frame so that equal months could never be merged as peers.

**Follow-ups:**
- *Rolling 12 months instead of YTD?* A sliding frame, `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW`, if no month is missing.
- *Month-over-month and YoY change?* Q16 and Q23.

**Common mistakes:**
- Partitioning by month instead of year.
- Using `LAG(ytd, 12)` with a gap.
- Comparing partial-year YTD with a full previous year.

### Q33 ⭐⭐ 🔴 Cumulative distinct count: events(event_date, user_id). Return for each date the number of new users that day and the cumulative number of distinct users so far. Show that COUNT(DISTINCT user_id) OVER (ORDER BY event_date) is rejected in SQLite (and PostgreSQL), then use the first-occurrence flag trick (MIN(event_date) per user in a CTE, then count first appearances per day and take a running SUM), and give the pandas drop_duplicates or ~duplicated().cumsum() version.
**Asked at:** guide snippets for forward fill and cumulative distinct counts (ibis forward-fill how-to, Red Gate Simple Talk, SingleStore forum, PostgreSQL mailing list; not opened), not candidate reports; analyst and data engineer screens
**Say this first (1 line):** `COUNT(DISTINCT user_id) OVER (ORDER BY event_date)` is rejected by SQLite 3.45 ("DISTINCT is not supported for window functions"; as I recall PostgreSQL rejects it too, not executed here), so mark each user's first appearance (`MIN(event_date)` per user), count first appearances per date, and take a running `SUM` of those counts; in pandas `drop_duplicates("user_id")` or `~duplicated()` followed by `cumsum`.

**Schema and sample data:** four days, four real users, one user seen twice in a day (user 1 on 02-01), and one NULL user.
```sql
CREATE TABLE events(event_date TEXT, user_id INTEGER);
INSERT INTO events VALUES
 ('2024-02-01',1),('2024-02-01',2),('2024-02-01',1),
 ('2024-02-02',2),('2024-02-02',3),
 ('2024-02-03',1),('2024-02-03',2),
 ('2024-02-04',4),('2024-02-04',3),('2024-02-04',NULL);
```

**SQL answer:** every date that has at least one event gets a row, with 0 new users if none; NULL users are ignored.
```sql
WITH first_seen AS (
  SELECT user_id, MIN(event_date) AS first_date
  FROM events
  WHERE user_id IS NOT NULL
  GROUP BY user_id
),
per_day AS (
  SELECT d.event_date, COUNT(f.user_id) AS new_users
  FROM (SELECT DISTINCT event_date FROM events) d
  LEFT JOIN first_seen f ON f.first_date = d.event_date
  GROUP BY d.event_date
)
SELECT event_date, new_users,
       SUM(new_users) OVER (ORDER BY event_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_users
FROM per_day
ORDER BY event_date
```

**pandas answer:**
```py
e = ev.dropna(subset=["user_id"]).sort_values(["event_date", "user_id"])
first = e.drop_duplicates("user_id")                       # first row per user, in date order
new_users = first.groupby("event_date").size().reindex(sorted(ev["event_date"].unique()), fill_value=0)
out = new_users.rename("new_users").reset_index()
out["cumulative_users"] = out["new_users"].cumsum()
```

**Example:**
- first_seen: user 1 on 02-01, user 2 on 02-01, user 3 on 02-02, user 4 on 02-04 (the NULL user is filtered out).
- New users per date: 02-01 has 2 (users 1 and 2; user 1's second row does not count again), 02-02 has 1 (user 3), 02-03 has 0 (users 1 and 2 are repeats), 02-04 has 1 (user 4; user 3 is a repeat).
- Running sum: 2, 3, 3, 4.

**Code:** run with `python3 -I`.
```python
# Q33: cumulative distinct users via a first-occurrence flag
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_date TEXT, user_id INTEGER);
INSERT INTO events VALUES
 ('2024-02-01',1),('2024-02-01',2),('2024-02-01',1),
 ('2024-02-02',2),('2024-02-02',3),
 ('2024-02-03',1),('2024-02-03',2),
 ('2024-02-04',4),('2024-02-04',3),('2024-02-04',NULL);
"""
# NULL user_id rows are ignored. Every date that has an event gets a row, even with 0 new users.
SQL_MAIN = """
WITH first_seen AS (
  SELECT user_id, MIN(event_date) AS first_date
  FROM events
  WHERE user_id IS NOT NULL
  GROUP BY user_id
),
per_day AS (
  SELECT d.event_date, COUNT(f.user_id) AS new_users
  FROM (SELECT DISTINCT event_date FROM events) d
  LEFT JOIN first_seen f ON f.first_date = d.event_date
  GROUP BY d.event_date
)
SELECT event_date, new_users,
       SUM(new_users) OVER (ORDER BY event_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_users
FROM per_day
ORDER BY event_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
try:
    con.execute("SELECT event_date, COUNT(DISTINCT user_id) OVER (ORDER BY event_date) FROM events").fetchall()
except sqlite3.OperationalError as e:
    print("COUNT(DISTINCT) OVER on SQLite 3.45:", e)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

ev = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = ev.dropna(subset=["user_id"]).sort_values(["event_date", "user_id"])
first = e.drop_duplicates("user_id")                       # first row per user, in date order
new_users = first.groupby("event_date").size().reindex(sorted(ev["event_date"].unique()), fill_value=0)
out = new_users.rename("new_users").reset_index()
out["cumulative_users"] = out["new_users"].cumsum()
# pd:end
# compared in event_date order
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)

# the row-level form: flag each first appearance, cumulate, take the last value per date
e2 = e.assign(is_new=~e["user_id"].duplicated())
e2["cum"] = e2["is_new"].cumsum()
per_date = e2.groupby("event_date")["cum"].last().tolist()
print("\n~duplicated().cumsum(), last per date:", per_date)
assert per_date == sql_df["cumulative_users"].tolist()
print("distinct users overall:", ev["user_id"].nunique(), "| last cumulative value:", sql_df["cumulative_users"].iloc[-1])
print("asserts passed: SQL first-occurrence flag == pandas drop_duplicates / ~duplicated().cumsum()")
```

**Output (my run):**
```text
COUNT(DISTINCT) OVER on SQLite 3.45: DISTINCT is not supported for window functions
event_date  new_users  cumulative_users
2024-02-01          2                 2
2024-02-02          1                 3
2024-02-03          0                 3
2024-02-04          1                 4

~duplicated().cumsum(), last per date: [2, 3, 3, 4]
distinct users overall: 4 | last cumulative value: 4
asserts passed: SQL first-occurrence flag == pandas drop_duplicates / ~duplicated().cumsum()
```

**Edge cases:**
- **Day with no new users:** 02-03 must still be in the result, so the per-day list comes from the distinct event dates with a LEFT JOIN; a plain `GROUP BY first_date` would lose it.
- **Day with no events at all:** not in the output; if the report needs every calendar day, drive it from a calendar (Part 6) and the running sum will repeat the previous value.
- **NULL user_id:** excluded in both versions (`WHERE user_id IS NOT NULL`, `dropna`). Without the filter, `GROUP BY user_id` would form one NULL group; my `COUNT(f.user_id)` would skip it anyway, but a `COUNT(*)` version would count it as a user.
- **Same user twice on the first day:** counted once, by `MIN` per user and by `drop_duplicates`.
- **Ties in the window:** `per_day` has one row per date, so the ROWS and default frames agree; I wrote ROWS explicitly.
- **Dialect:** the `COUNT(DISTINCT) OVER` failure was run on SQLite 3.45 only. Other engines may differ (for example SQL Server is reported to reject it as well, not executed).

**Then explain:**
- Why it works: a user is "new" on exactly one date, their first. Distinct users so far = number of users whose first date is at or before now = running sum of the new-user counts.
- Why the window cannot do it directly: a distinct count over an expanding frame would have to remember every value already seen; engines do not support it for windows.
- pandas: `drop_duplicates("user_id")` after sorting by date keeps each user's first row; `~duplicated()` marks the same rows (the printed row-level check agrees).

**Follow-ups:**
- *Distinct users in a trailing 7 days?* A different problem, because users leave the window (Q45; the first-occurrence trick no longer works).
- *Returning users per day?* Total distinct users that day minus new ones.

**Common mistakes:**
- Writing `COUNT(DISTINCT ...) OVER` and expecting it to run.
- Cumulating a count of rows per day instead of first appearances.
- Dropping days with 0 new users by grouping only the first-seen table.

### Q34 ⭐⭐ 🔴 Forward fill (last non-null carried forward): sensor_readings(sensor_id, read_date, value) where value is sometimes NULL. Fill each NULL with the previous non-null value of the same sensor. SQLite and PostgreSQL have no IGNORE NULLS, so use the running COUNT(value) as a group id and MAX(value) over (PARTITION BY sensor_id, group_id), explain why it works, and give pandas groupby()['value'].ffill(). State what happens to leading NULLs.
**Asked at:** guide snippets for forward fill and cumulative distinct counts (ibis forward-fill how-to, Red Gate Simple Talk, SingleStore forum, PostgreSQL mailing list; not opened), not candidate reports; analyst and data engineer screens
**Say this first (1 line):** Running `COUNT(value) OVER (PARTITION BY sensor_id ORDER BY read_date)` goes up by one at every real reading and ignores NULLs, so a real value and the NULLs after it share one group number, and `MAX(value) OVER (PARTITION BY sensor_id, grp)` then spreads that value over the group; leading NULLs sit in group 0 and stay NULL; pandas does it with `groupby("sensor_id")["value"].ffill()`.

**Schema and sample data:** sensor 1 starts with a NULL, has a 0.0 reading in the middle, and ends on a real value; sensor 2 ends with a NULL; sensor 3 is all NULL. `(sensor_id, read_date)` is the primary key.
```sql
CREATE TABLE sensor_readings(sensor_id INTEGER, read_date TEXT, value REAL,
                             PRIMARY KEY (sensor_id, read_date));
INSERT INTO sensor_readings VALUES
 (1,'2024-04-01',NULL),(1,'2024-04-02',5.0),(1,'2024-04-03',NULL),(1,'2024-04-04',NULL),
 (1,'2024-04-05',0.0),(1,'2024-04-06',NULL),(1,'2024-04-07',7.5),
 (2,'2024-04-01',3.0),(2,'2024-04-02',NULL),
 (3,'2024-04-01',NULL),(3,'2024-04-02',NULL);
```

**SQL answer:** `SQL_MAIN` is the group trick; `SQL_CHECK` (Code block) is a correlated "latest non-NULL at or before" subquery used as a cross-check.
```sql
WITH g AS (
  SELECT sensor_id, read_date, value,
         COUNT(value) OVER (PARTITION BY sensor_id ORDER BY read_date
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM sensor_readings
)
SELECT sensor_id, read_date, value, grp,
       MAX(value) OVER (PARTITION BY sensor_id, grp) AS filled
FROM g
ORDER BY sensor_id, read_date
```

**pandas answer:**
```py
s = sr.sort_values(["sensor_id", "read_date"]).reset_index(drop=True)
s["filled"] = s.groupby("sensor_id")["value"].ffill()
```

**Example:** sensor 1 values: NULL, 5, NULL, NULL, 0, NULL, 7.5.
- Running `COUNT(value)`: 0, 1, 1, 1, 2, 2, 3. That is the group id.
- Group 0 (the first row) has no value, so MAX is NULL: the leading NULL stays NULL.
- Group 1 is the 5 and the two NULLs after it: MAX = 5, so all three rows show 5. Group 2 is 0 and one NULL: both show 0. Group 3 is 7.5.
- Sensor 2: 3.0, NULL becomes 3.0, 3.0. Sensor 3: every row is in group 0, all NULL.

**Code:** run with `python3 -I`.
```python
# Q34: forward fill with a running COUNT as group id
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE sensor_readings(sensor_id INTEGER, read_date TEXT, value REAL,
                             PRIMARY KEY (sensor_id, read_date));
INSERT INTO sensor_readings VALUES
 (1,'2024-04-01',NULL),(1,'2024-04-02',5.0),(1,'2024-04-03',NULL),(1,'2024-04-04',NULL),
 (1,'2024-04-05',0.0),(1,'2024-04-06',NULL),(1,'2024-04-07',7.5),
 (2,'2024-04-01',3.0),(2,'2024-04-02',NULL),
 (3,'2024-04-01',NULL),(3,'2024-04-02',NULL);
"""
# PRIMARY KEY (sensor_id, read_date): one row per sensor per day, so the running COUNT has no peers.
# COUNT(value) counts non-NULLs: it goes up by 1 on every real reading, so each real value
# and the NULLs after it share one grp number. Group 0 = leading NULLs.
SQL_MAIN = """
WITH g AS (
  SELECT sensor_id, read_date, value,
         COUNT(value) OVER (PARTITION BY sensor_id ORDER BY read_date
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM sensor_readings
)
SELECT sensor_id, read_date, value, grp,
       MAX(value) OVER (PARTITION BY sensor_id, grp) AS filled
FROM g
ORDER BY sensor_id, read_date
"""
SQL_CHECK = """
SELECT r.sensor_id, r.read_date,
       (SELECT p.value FROM sensor_readings p
         WHERE p.sensor_id = r.sensor_id AND p.read_date <= r.read_date AND p.value IS NOT NULL
         ORDER BY p.read_date DESC LIMIT 1) AS filled
FROM sensor_readings r ORDER BY r.sensor_id, r.read_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
chk = pd.read_sql_query(SQL_CHECK, con)
print(sql_df.to_string(index=False))
pd.testing.assert_series_equal(sql_df["filled"], chk["filled"], check_names=False)
print("\ncorrelated 'latest non-NULL at or before' subquery gives the same filled column: True")

try:
    con.execute("SELECT LAST_VALUE(value IGNORE NULLS) OVER (PARTITION BY sensor_id ORDER BY read_date) FROM sensor_readings")
except sqlite3.OperationalError as e:
    print("LAST_VALUE(... IGNORE NULLS) on SQLite 3.45:", e)

sr = pd.read_sql_query("SELECT * FROM sensor_readings", con)
# pd:main
s = sr.sort_values(["sensor_id", "read_date"]).reset_index(drop=True)
s["filled"] = s.groupby("sensor_id")["value"].ffill()
# pd:end
# compared in the order sensor_id, read_date; NaN equals NULL
pd.testing.assert_series_equal(sql_df["filled"], s["filled"], check_names=False)
print("leading NULLs stay NULL (sensor 1 first row, sensor 3 all rows):", s.loc[[0, 9, 10], "filled"].tolist())
print("value 0.0 is a real reading and is carried forward:", s.loc[(s.sensor_id == 1) & (s.read_date == "2024-04-06"), "filled"].tolist())
print("asserts passed: SQL COUNT/MAX group trick == correlated subquery == pandas groupby().ffill()")
```

**Output (my run):**
```text
 sensor_id  read_date  value  grp  filled
         1 2024-04-01    NaN    0     NaN
         1 2024-04-02    5.0    1     5.0
         1 2024-04-03    NaN    1     5.0
         1 2024-04-04    NaN    1     5.0
         1 2024-04-05    0.0    2     0.0
         1 2024-04-06    NaN    2     0.0
         1 2024-04-07    7.5    3     7.5
         2 2024-04-01    3.0    1     3.0
         2 2024-04-02    NaN    1     3.0
         3 2024-04-01    NaN    0     NaN
         3 2024-04-02    NaN    0     NaN

correlated 'latest non-NULL at or before' subquery gives the same filled column: True
LAST_VALUE(... IGNORE NULLS) on SQLite 3.45: near "IGNORE": syntax error
leading NULLs stay NULL (sensor 1 first row, sensor 3 all rows): [nan, nan, nan]
value 0.0 is a real reading and is carried forward: [0.0]
asserts passed: SQL COUNT/MAX group trick == correlated subquery == pandas groupby().ffill()
```

**Edge cases:**
- **Leading NULLs:** nothing earlier to carry, so they stay NULL in SQL and in pandas (`ffill` has nothing before them); fill with `COALESCE(filled, 0)` or `bfill` only if the business agrees.
- **A real 0 or negative value:** counted as a reading and carried forward (`COUNT(value)` counts it); `MAX` works because each group holds exactly one non-NULL value, so negative or zero values are not a problem.
- **Duplicate dates:** the primary key prevents them. Duplicates would be peers in the default RANGE frame and would both increase the count; give a tie-breaker and a ROWS frame (I used an explicit ROWS frame).
- **IGNORE NULLS:** `LAST_VALUE(value IGNORE NULLS) OVER (...)` is a syntax error on SQLite 3.45 (printed in the Output). PostgreSQL's docs, which I opened, say IGNORE NULLS is not implemented there; other engines that do offer it (hedged, not executed) make the whole trick unnecessary.
- **Stale data:** forward fill can hide a sensor that has been silent for weeks; pandas has `ffill(limit=n)`, and in SQL you would also keep the date of the carried reading (`MAX(read_date)` of the group's real row) and cap the age.

**Then explain:**
- A running count of non-NULLs is a step counter that increases only at real values; rows between two steps belong to the earlier value. `PARTITION BY sensor_id, grp` therefore isolates "one real value plus its trailing NULLs".
- `MAX` (or `MIN`, or `FIRST_VALUE`) is just a way to pick the one non-NULL value in the group; there is only one, so any of them gives it.
- It needs the partition and the order to be exactly the same in both windows.

**Follow-ups:**
- *Why not LAG repeatedly?* It works for exactly one missing value in a row, not for runs of NULLs.
- *Backward fill?* `COUNT(value)` over the reverse order, or pandas `bfill`.
- *Fill with the average of neighbours?* That is interpolation; pandas `interpolate`, in SQL a join to the next and previous real value.

**Common mistakes:**
- Using `COUNT(*)`, which counts the NULL rows and makes each row its own group.
- Forgetting `PARTITION BY sensor_id`, so one sensor's last value fills the next sensor's leading NULLs.
- Expecting leading NULLs to be filled.

### Q35 ⭐ 🟡 Rolling window excluding the current row: daily_sales(sale_date, amount). Compute the average of the previous 7 days excluding today with ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING (and show EXCLUDE CURRENT ROW on a centered frame), and flag days where amount is more than twice that trailing average (a simple anomaly flag). Give pandas rolling(7).mean().shift(1) and the rolling(..., closed='left') alternative and explain why excluding today avoids leakage.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** For "the average of the previous 7 days, not including today" use `ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING` (the frame stops one row before the current row), require 7 days of history, and flag `amount > 2 * trailing_avg`; `EXCLUDE CURRENT ROW` is for frames that contain the current row, such as a centered one; in pandas it is `rolling(7).mean().shift(1)` or `rolling(7, closed="left").mean()`.

**Schema and sample data:** twelve consecutive days, ten a day for seven days, then 30, 20, 50, 12, 10. `sale_date` is the primary key, one row per day, no missing days.
```sql
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES
 ('2024-06-01',10),('2024-06-02',10),('2024-06-03',10),('2024-06-04',10),('2024-06-05',10),
 ('2024-06-06',10),('2024-06-07',10),('2024-06-08',30),('2024-06-09',20),('2024-06-10',50),
 ('2024-06-11',12),('2024-06-12',10);
```

**SQL answer:** main query `SQL_MAIN` (trailing average and anomaly flag); `SQL_CENTER` (the EXCLUDE CURRENT ROW example) is in the Code block.
```sql
WITH t AS (
  SELECT sale_date, amount,
         COUNT(amount) OVER w AS n_prev,
         AVG(amount)   OVER w AS avg_prev
  FROM daily_sales
  WINDOW w AS (ORDER BY sale_date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING)
)
SELECT sale_date, amount, n_prev,
       CASE WHEN n_prev = 7 THEN avg_prev END AS trailing_avg,
       CASE WHEN n_prev < 7 THEN NULL
            WHEN amount > 2 * avg_prev THEN 1 ELSE 0 END AS is_anomaly
FROM t
ORDER BY sale_date
```
```sql
SELECT sale_date, amount,
       AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING EXCLUDE CURRENT ROW) AS neighbours_avg
FROM daily_sales ORDER BY sale_date
```

**pandas answer:**
```py
a = ds["amount"]
trailing = a.rolling(7).mean().shift(1)                 # window ends yesterday, 7 full days needed
trailing_left = a.rolling(7, closed="left").mean()      # same window written with closed='left'
n_prev = a.rolling(7, min_periods=1, closed="left").count().fillna(0).astype(int)
flag = (a > 2 * trailing).astype(float).where(trailing.notna())
# centered, excluding self: (sum of 3 - self) / (count of 3 - 1)
s3 = a.rolling(3, center=True, min_periods=1)
neighbours = (s3.sum() - a) / (s3.count() - 1)
```

**Example:**
- 06-08 (30): the previous seven days are all 10, average 10; 30 > 20, so the flag is 1.
- 06-09 (20): the previous seven days are 06-02 to 06-08 = 10 x 6 + 30 = 90, average 12.857; 20 is not above 25.7, flag 0.
- 06-10 (50): previous seven are 10 x 5 + 30 + 20 = 100, average 14.286; 50 > 28.6, flag 1.
- 06-07 and earlier: fewer than seven previous days, so average and flag are NULL ("not enough history").
- Centered with EXCLUDE: 06-09 (20) averages its two neighbours 30 and 50 = 40, not the three-day average of 33.3.

**Code:** run with `python3 -I`.
```python
# Q35: trailing average excluding today, anomaly flag, EXCLUDE CURRENT ROW on a centered frame
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE daily_sales(sale_date TEXT PRIMARY KEY, amount INTEGER);
INSERT INTO daily_sales VALUES
 ('2024-06-01',10),('2024-06-02',10),('2024-06-03',10),('2024-06-04',10),('2024-06-05',10),
 ('2024-06-06',10),('2024-06-07',10),('2024-06-08',30),('2024-06-09',20),('2024-06-10',50),
 ('2024-06-11',12),('2024-06-12',10);
"""
# one row per day with no missing days (a ROWS frame counts rows, not days). Flag only with 7 days of history.
SQL_MAIN = """
WITH t AS (
  SELECT sale_date, amount,
         COUNT(amount) OVER w AS n_prev,
         AVG(amount)   OVER w AS avg_prev
  FROM daily_sales
  WINDOW w AS (ORDER BY sale_date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING)
)
SELECT sale_date, amount, n_prev,
       CASE WHEN n_prev = 7 THEN avg_prev END AS trailing_avg,
       CASE WHEN n_prev < 7 THEN NULL
            WHEN amount > 2 * avg_prev THEN 1 ELSE 0 END AS is_anomaly
FROM t
ORDER BY sale_date
"""
SQL_CENTER = """
SELECT sale_date, amount,
       AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING EXCLUDE CURRENT ROW) AS neighbours_avg
FROM daily_sales ORDER BY sale_date
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
cen_df = pd.read_sql_query(SQL_CENTER, con)
print(sql_df.round(3).to_string(index=False))
print()
print(cen_df.round(3).to_string(index=False))
noexc = con.execute("""SELECT SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING EXCLUDE CURRENT ROW) FROM daily_sales""").fetchall()
same = con.execute("""SELECT SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) FROM daily_sales""").fetchall()
print("\nEXCLUDE CURRENT ROW on a frame that already stops at 1 PRECEDING changes nothing:", noexc == same)

ds = pd.read_sql_query("SELECT * FROM daily_sales ORDER BY sale_date", con)
# pd:main
a = ds["amount"]
trailing = a.rolling(7).mean().shift(1)                 # window ends yesterday, 7 full days needed
trailing_left = a.rolling(7, closed="left").mean()      # same window written with closed='left'
n_prev = a.rolling(7, min_periods=1, closed="left").count().fillna(0).astype(int)
flag = (a > 2 * trailing).astype(float).where(trailing.notna())
# centered, excluding self: (sum of 3 - self) / (count of 3 - 1)
s3 = a.rolling(3, center=True, min_periods=1)
neighbours = (s3.sum() - a) / (s3.count() - 1)
# pd:end
out = pd.DataFrame({"sale_date": ds["sale_date"], "amount": a, "n_prev": n_prev,
                    "trailing_avg": trailing, "is_anomaly": flag})
# compared in sale_date order; NaN equals NULL
pd.testing.assert_series_equal(trailing, trailing_left, check_names=False)
pd.testing.assert_frame_equal(sql_df, out, check_dtype=False)
pd.testing.assert_series_equal(cen_df["neighbours_avg"], neighbours, check_names=False)
leak = a.rolling(7).mean()
print("\nwith today inside the window (leakage), 2024-06-10 would be judged against", round(leak.iloc[9], 3),
      "instead of", round(trailing.iloc[9], 3))
print("asserts passed: SQL frames == pandas rolling(7).shift(1) == closed='left'; EXCLUDE CURRENT ROW == (sum - self)/(n - 1)")
```

**Output (my run):**
```text
 sale_date  amount  n_prev  trailing_avg  is_anomaly
2024-06-01      10       0           NaN         NaN
2024-06-02      10       1           NaN         NaN
2024-06-03      10       2           NaN         NaN
2024-06-04      10       3           NaN         NaN
2024-06-05      10       4           NaN         NaN
2024-06-06      10       5           NaN         NaN
2024-06-07      10       6           NaN         NaN
2024-06-08      30       7        10.000         1.0
2024-06-09      20       7        12.857         0.0
2024-06-10      50       7        14.286         1.0
2024-06-11      12       7        20.000         0.0
2024-06-12      10       7        20.286         0.0

 sale_date  amount  neighbours_avg
2024-06-01      10            10.0
2024-06-02      10            10.0
2024-06-03      10            10.0
2024-06-04      10            10.0
2024-06-05      10            10.0
2024-06-06      10            10.0
2024-06-07      10            20.0
2024-06-08      30            15.0
2024-06-09      20            40.0
2024-06-10      50            16.0
2024-06-11      12            30.0
2024-06-12      10            12.0

EXCLUDE CURRENT ROW on a frame that already stops at 1 PRECEDING changes nothing: True

with today inside the window (leakage), 2024-06-10 would be judged against 20.0 instead of 14.286
asserts passed: SQL frames == pandas rolling(7).shift(1) == closed='left'; EXCLUDE CURRENT ROW == (sum - self)/(n - 1)
```

**Edge cases:**
- **Fewer than 7 previous rows:** SQL `AVG` would average what exists (1 to 6 rows); I blank it with `COUNT = 7`. pandas `rolling(7)` has `min_periods=7`, so it gives NaN in the same places (asserted equal).
- **First row:** the frame is empty, `AVG` is NULL, and a comparison with NULL is unknown, so the flag is NULL, not 0.
- **Strict `>`:** an amount of exactly twice the average is not flagged.
- **Missing days:** the ROWS frame counts rows, so with gaps "7 PRECEDING" reaches back more than a week; use the RANGE form over `julianday` (Q24) with `7 PRECEDING AND 1 PRECEDING`.
- **NULL amounts:** `AVG` and `COUNT(amount)` skip them (so `n_prev` can stay below 7 for a while); pandas `rolling(7)` with the default `min_periods` returns NaN for every window that contains a NaN (checked on a scratch series), matching SQL's `n_prev < 7` blanking.
- **EXCLUDE CURRENT ROW on a frame that already ends before the current row:** no change (printed True). It supports `EXCLUDE GROUP` and `EXCLUDE TIES` too (Q36). PostgreSQL has EXCLUDE from version 11, from memory, and MySQL has no EXCLUDE (not executed).

**Then explain:**
- Leakage: if today's amount is inside the average, an outlier raises its own benchmark and hides itself. In my data, with today included 06-10 would be compared with 20.0 instead of 14.286.
- Excluding today is also what is knowable at the time, which matters for any live alerting or feature for a model.
- `shift(1)` after `rolling(7)` moves the window one step back; `closed="left"` builds the window as [t - 7 rows, t) directly. The two agree here (asserted).
- Centered with EXCLUDE: `(sum of the 3-row window - self) / (count - 1)` in pandas.

**Follow-ups:**
- *Use a median or a standard deviation instead of a mean?* A robust anomaly rule; SQLite has no median function, so use pandas or a percentile in an engine that has it.
- *Why twice the average rather than a z-score?* A simple rule for the interview; a z-score needs the trailing standard deviation too.

**Common mistakes:**
- Using `ROWS BETWEEN 7 PRECEDING AND CURRENT ROW` and comparing a value with a window that contains itself.
- Treating the NULL of the first rows as "not an anomaly" in a report that must show "not enough history".
- `rolling(7).mean()` without the `shift(1)`.

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

