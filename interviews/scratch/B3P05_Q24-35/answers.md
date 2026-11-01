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
