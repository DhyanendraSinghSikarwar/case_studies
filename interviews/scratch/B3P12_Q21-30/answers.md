<!-- Book 3 Part 12 answers Q21-Q30 (Wave B). Generated; code blocks were run with python3 -I. -->

### Q21 ⭐⭐ 🟡 [Set F3, Q3 of 5, 8 min, 20 pts] Month-over-month revenue with a missing month (Amazon-style, Part 5 Q16, Part 6 Q6). orders(order_id, order_date, amount) over Jan to May 2025 where April has no orders. Return month, revenue, previous month revenue and growth percent; April must appear with 0 and May's growth must be NULL when the previous month is zero. SQL with a month spine and pandas (resample or reindex), asserting equal.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Build a month spine (Jan to May) so April exists, LEFT JOIN the orders and `COALESCE` the sum to 0, then `LAG` the previous month and divide by `NULLIF(prev, 0)`, so growth is NULL when there is nothing to grow from.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2025-01-10',100),(2,'2025-01-31',50),
 (3,'2025-02-14',200),
 (4,'2025-03-01',150),(5,'2025-03-20',50),
 (6,'2025-05-05',120);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH RECURSIVE spine(m) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < '2025-05-01'
),
monthly AS (
  SELECT substr(s.m, 1, 7) AS month, COALESCE(SUM(o.amount), 0) AS revenue
  FROM spine s
  LEFT JOIN orders o ON substr(o.order_date, 1, 7) = substr(s.m, 1, 7)
  GROUP BY s.m
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
FROM monthly
ORDER BY month
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
m = orders.set_index("order_date")["amount"].resample("MS").sum()
m = m.reindex(pd.date_range("2025-01-01", "2025-05-01", freq="MS"), fill_value=0)
p = m.rename("revenue").to_frame()
p["month"] = p.index.strftime("%Y-%m")
p["prev_revenue"] = p["revenue"].shift(1)
p["growth_pct"] = (100.0 * (p["revenue"] - p["prev_revenue"])
                   / p["prev_revenue"].where(p["prev_revenue"] != 0)).round(1)
p = p[["month", "revenue", "prev_revenue", "growth_pct"]].reset_index(drop=True)
```

**Example:** Orders: Jan 100 + 50 = 150, Feb 200, Mar 150 + 50 = 200, Apr none, May 120. Spine row 2025-04 finds no orders, so the sum is NULL and `COALESCE` makes it 0. Growth Feb = (200 - 150) / 150 = 33.3 percent. Mar = (200 - 200) / 200 = 0.0. Apr = (0 - 200) / 200 = -100.0. May's previous month is 0, so `NULLIF(0, 0)` is NULL and the growth is NULL (not 0, not infinite). Jan has no previous row, so `LAG` gives NULL and growth is NULL too.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q21: month-over-month revenue with a missing month (April), spine in SQL and reindex in pandas.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2025-01-10',100),(2,'2025-01-31',50),
 (3,'2025-02-14',200),
 (4,'2025-03-01',150),(5,'2025-03-20',50),
 (6,'2025-05-05',120);
"""
SQL = """
WITH RECURSIVE spine(m) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < '2025-05-01'
),
monthly AS (
  SELECT substr(s.m, 1, 7) AS month, COALESCE(SUM(o.amount), 0) AS revenue
  FROM spine s
  LEFT JOIN orders o ON substr(o.order_date, 1, 7) = substr(s.m, 1, 7)
  GROUP BY s.m
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
FROM monthly
ORDER BY month
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con, parse_dates=["order_date"])
# PANDAS START
m = orders.set_index("order_date")["amount"].resample("MS").sum()
m = m.reindex(pd.date_range("2025-01-01", "2025-05-01", freq="MS"), fill_value=0)
p = m.rename("revenue").to_frame()
p["month"] = p.index.strftime("%Y-%m")
p["prev_revenue"] = p["revenue"].shift(1)
p["growth_pct"] = (100.0 * (p["revenue"] - p["prev_revenue"])
                   / p["prev_revenue"].where(p["prev_revenue"] != 0)).round(1)
p = p[["month", "revenue", "prev_revenue", "growth_pct"]].reset_index(drop=True)
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (same 5 rows, ordered by month; NULL in SQL equals NaN in pandas)")

# resample alone only spans the months that have orders: it stops at the last order
short = orders[orders["order_date"] < "2025-05-01"].set_index("order_date")["amount"].resample("MS").sum()
print("resample without reindex, orders before May only: rows", len(short), "ending at", short.index.max().strftime("%Y-%m"))
# naive growth without NULLIF would divide by zero
print("SQLite 100.0*(120-0)/0 gives (NULL, no error in SQLite):", con.execute("SELECT 100.0*(120-0)/0").fetchone()[0])
print("pandas 120.0 / 0.0 gives:", (pd.Series([120.0]) / pd.Series([0.0])).iloc[0], "(inf, not NaN, so the zero must be masked)")
```

**Output (my run):**
```text
  month  revenue  prev_revenue  growth_pct
2025-01      150           NaN         NaN
2025-02      200         150.0        33.3
2025-03      200         200.0         0.0
2025-04        0         200.0      -100.0
2025-05      120           0.0         NaN

  month  revenue  prev_revenue  growth_pct
2025-01      150           NaN         NaN
2025-02      200         150.0        33.3
2025-03      200         200.0         0.0
2025-04        0         200.0      -100.0
2025-05      120           0.0         NaN

asserts passed (same 5 rows, ordered by month; NULL in SQL equals NaN in pandas)
resample without reindex, orders before May only: rows 3 ending at 2025-03
SQLite 100.0*(120-0)/0 gives (NULL, no error in SQLite): None
pandas 120.0 / 0.0 gives: inf (inf, not NaN, so the zero must be masked)
```

**Edge cases:**
- Missing month: without the spine the April row simply does not exist, and May's `LAG` would then point at March (growth 120 versus 200 would be wrong). In pandas, `resample("MS")` fills inner gaps with 0 for free, but it stops at the last month that has data; the run shows a series with only orders before May ending at 2025-03. So reindex to an explicit `date_range` when the report must have a fixed set of months.
- Division by zero: SQLite returns NULL for `100.0 * 120 / 0` (the run printed None), so the guard is not needed for SQLite, but keep `NULLIF` anyway: PostgreSQL raises a division-by-zero error for this (not executed here). pandas float division gives `inf` (the run printed inf), so mask the zero with `where`.
- Boundary dates: 2025-01-31 and 2025-03-01 land in January and March because the month key is `substr(date, 1, 7)`; a timestamp column with a time part would still work for the text key but not for a `BETWEEN` on dates.
- Rounding: growth is rounded to one decimal here; SQLite `ROUND` and pandas `round` can differ on exact halves (Part 10), none occurs in this data.

**Then explain:**
- Spine first, then join: the spine owns the months, the orders table only contributes numbers. This is the Part 6 Q6 pattern and the Part 5 Q16 `LAG` growth.
- `LAG` after the aggregation, never over raw orders: it must see one row per month.
- In an interview say the growth definition out loud: (this - previous) / previous, NULL when previous is 0.
- Scoring note (Set F3, Q3 of 5, 20 pts, part-header rubric): about 8 pts for a query that returns April as 0 and the right growth on the seed; 4 pts for May NULL and January NULL (and not 0 or an error); 4 pts for the pandas version matching (resample or reindex); 2 pts for stating the growth formula and that April is a real zero; 2 pts for a one-line check such as 5 rows and revenue total 670. Partial credit: a query without a spine that gets Jan, Feb, Mar, May right but drops April earns the correctness points only up to about half.

**Follow-ups:**
- Year-over-year? Same spine but `LAG(revenue, 12)` over a 12-month-plus spine (Part 6 Q6); with a gap-free spine the offset is exact. Not executed on other engines: PostgreSQL could build the spine with `generate_series` and `date_trunc` (not executed here).
- Why not `LAG` over a table with a missing month? Because `LAG` goes by row position, not by calendar, so May would compare with March.
- What if the first month should show 0 growth instead of NULL? Say that is a business choice; NULL means not defined.

**Common mistakes:**
- Joining orders to the spine with the filter in `WHERE`, which turns the LEFT JOIN back into an inner join and drops April.
- Using `COALESCE(growth, 0)` and hiding the undefined growth.
- Computing growth with integer division in engines that truncate (the `100.0` multiplier avoids it).
- Relying on `resample` to cover a range it does not know about.

### Q22 ⭐⭐ 🟡 [Set F3, Q2 of 5, 8 min, 20 pts] Best-selling product per category per month (Part 4 Q15). order_items(order_id, product_id, qty), orders(order_id, order_date), products(product_id, category). Return per category and month the product with the most units, all products on ties, for Jan and Feb 2025 only. Seed 6 products in 2 categories with a tie in one month. SQL (RANK in a CTE) and pandas (groupby, rank method='min').
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Aggregate units per category, month and product, then `RANK()` descending inside each (category, month) and keep rank 1; `RANK` (not `ROW_NUMBER`) keeps every tied product.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'books'),(2,'books'),(3,'books'),(4,'toys'),(5,'toys'),(6,'toys');
INSERT INTO orders VALUES (1,'2025-01-05'),(2,'2025-01-20'),(3,'2025-02-03'),(4,'2025-02-18'),(5,'2025-03-02');
INSERT INTO order_items VALUES
 (1,1,3),(1,2,2),(1,4,1),
 (2,1,1),(2,2,2),(2,5,4),
 (3,3,5),(3,4,2),(3,5,2),
 (4,6,1),(4,4,0),
 (5,1,9);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH units AS (
  SELECT p.category, substr(o.order_date, 1, 7) AS month, p.product_id, SUM(oi.qty) AS units
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.order_date >= '2025-01-01' AND o.order_date < '2025-03-01'
  GROUP BY p.category, substr(o.order_date, 1, 7), p.product_id
),
ranked AS (
  SELECT *, RANK() OVER (PARTITION BY category, month ORDER BY units DESC) AS rnk
  FROM units
)
SELECT category, month, product_id, units
FROM ranked
WHERE rnk = 1
ORDER BY category, month, product_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
d = oi.merge(o, on="order_id").merge(pr, on="product_id")
d = d[(d["order_date"] >= "2025-01-01") & (d["order_date"] < "2025-03-01")].copy()
d["month"] = d["order_date"].str[:7]
u = d.groupby(["category", "month", "product_id"], as_index=False)["qty"].sum().rename(columns={"qty": "units"})
u["rnk"] = u.groupby(["category", "month"])["units"].rank(method="min", ascending=False)
p = (u[u["rnk"] == 1][["category", "month", "product_id", "units"]]
     .sort_values(["category", "month", "product_id"]).reset_index(drop=True))
```

**Example:** Jan books: product 1 sold 3 + 1 = 4, product 2 sold 2 + 2 = 4, so both rank 1 (tie). Jan toys: product 4 sold 1, product 5 sold 4, so product 5 wins. Feb books: only product 3 with 5. Feb toys: product 4 sold 2 + 0 = 2, product 5 sold 2, product 6 sold 1, so products 4 and 5 tie at 2. The March order (product 1, 9 units) is outside the date filter. That gives 6 rows: 2 for books Jan, 1 for books Feb, 1 for toys Jan, 2 for toys Feb.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q22: best-selling product per category per month, all products on ties.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'books'),(2,'books'),(3,'books'),(4,'toys'),(5,'toys'),(6,'toys');
INSERT INTO orders VALUES (1,'2025-01-05'),(2,'2025-01-20'),(3,'2025-02-03'),(4,'2025-02-18'),(5,'2025-03-02');
INSERT INTO order_items VALUES
 (1,1,3),(1,2,2),(1,4,1),
 (2,1,1),(2,2,2),(2,5,4),
 (3,3,5),(3,4,2),(3,5,2),
 (4,6,1),(4,4,0),
 (5,1,9);
"""
SQL = """
WITH units AS (
  SELECT p.category, substr(o.order_date, 1, 7) AS month, p.product_id, SUM(oi.qty) AS units
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.order_date >= '2025-01-01' AND o.order_date < '2025-03-01'
  GROUP BY p.category, substr(o.order_date, 1, 7), p.product_id
),
ranked AS (
  SELECT *, RANK() OVER (PARTITION BY category, month ORDER BY units DESC) AS rnk
  FROM units
)
SELECT category, month, product_id, units
FROM ranked
WHERE rnk = 1
ORDER BY category, month, product_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

oi = pd.read_sql("SELECT * FROM order_items", con)
o = pd.read_sql("SELECT * FROM orders", con)
pr = pd.read_sql("SELECT * FROM products", con)
# PANDAS START
d = oi.merge(o, on="order_id").merge(pr, on="product_id")
d = d[(d["order_date"] >= "2025-01-01") & (d["order_date"] < "2025-03-01")].copy()
d["month"] = d["order_date"].str[:7]
u = d.groupby(["category", "month", "product_id"], as_index=False)["qty"].sum().rename(columns={"qty": "units"})
u["rnk"] = u.groupby(["category", "month"])["units"].rank(method="min", ascending=False)
p = (u[u["rnk"] == 1][["category", "month", "product_id", "units"]]
     .sort_values(["category", "month", "product_id"]).reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (compared after sorting by category, month, product_id)")

# row_number would keep one of the tied products
rn = pd.read_sql(SQL.replace("RANK()", "ROW_NUMBER()"), con)
print("with ROW_NUMBER instead of RANK:", len(rn), "rows vs", len(s), "with RANK")
```

**Output (my run):**
```text
category   month  product_id  units
   books 2025-01           1      4
   books 2025-01           2      4
   books 2025-02           3      5
    toys 2025-01           5      4
    toys 2025-02           4      2
    toys 2025-02           5      2

category   month  product_id  units
   books 2025-01           1      4
   books 2025-01           2      4
   books 2025-02           3      5
    toys 2025-01           5      4
    toys 2025-02           4      2
    toys 2025-02           5      2

asserts passed (compared after sorting by category, month, product_id)
with ROW_NUMBER instead of RANK: 4 rows vs 6 with RANK
```

**Edge cases:**
- Ties: the run returns 6 rows with `RANK`, only 4 with `ROW_NUMBER` (one of each tied pair would be dropped, and which one is not defined without a tiebreaker).
- Date filter: `>= '2025-01-01' AND < '2025-03-01'` is a half-open range, so no end-of-month day is lost and March data (9 units of product 1) is excluded.
- Zero quantity rows (product 4 has a 0 line) add 0 and do not change the sum.
- A category with no sales in a month has no row at all (nothing to rank); add a spine if the report needs an empty line.
- pandas `rank(method="min", ascending=False)` matches `RANK`; `"dense"` would match `DENSE_RANK` and only differs beyond rank 1.

**Then explain:**
- Two steps: sum first (per product), rank second (per category and month); you cannot rank and sum in one pass without a window over an aggregate.
- The window is `PARTITION BY category, month ORDER BY units DESC`. Part 4 Q15 is the same shape.
- In engines with `QUALIFY` (Snowflake, BigQuery, not executed here) the rank filter can go in the same SELECT; in SQLite it needs the CTE.
- Scoring note (Set F3, Q2 of 5, 20 pts): about 8 pts for the right 6 rows; 4 pts for keeping both tied products (using `RANK`, not `ROW_NUMBER`) and excluding March; 4 pts for the pandas groupby and `rank(method="min")` matching; 2 pts for saying what ties mean for the business; 2 pts for a count check. Partial credit: `ROW_NUMBER` or `LIMIT 1` per group gets the structure right but loses the tie points.

**Follow-ups:**
- Top 2 products per category? `rnk <= 2` with `RANK` can return more than 2 rows on ties; with `DENSE_RANK` the ranks are consecutive (Part 4 Q4).
- Why not `MAX(units)` per group joined back? It also works and keeps ties; the window is shorter and extends to top N.
- A deterministic single winner? Add a tiebreaker such as `product_id` to the `ORDER BY` and use `ROW_NUMBER`.

**Common mistakes:**
- `ROW_NUMBER` silently drops one of two tied best sellers.
- Ranking raw order lines instead of per-product totals.
- Filtering the month in a way that includes 2025-03-01 or misses 2025-02-28 timestamps.
- In pandas, `rank()` default is `average`, which gives 1.5 for a tie and then `== 1` finds nothing.

### Q23 ⭐⭐ 🟡 [Set T1, Q3 of 5, 8 min, 20 pts] Latest transaction per user with the balance after it (Part 4 Q9, Part 5 Q12). bank_txns(txn_id, user_id, txn_ts, signed_amount). Return one row per user: last txn_id, last timestamp and the account balance after it. Two transactions can share the same timestamp (break by txn_id). Seed 3 users. SQL (window running sum plus ROW_NUMBER) and pandas (cumsum, groupby tail), asserting equal.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Compute the running balance with `SUM(...) OVER (PARTITION BY user ORDER BY txn_ts, txn_id ROWS ...)` and a `ROW_NUMBER()` in descending order of the same key, then keep row number 1; the `txn_id` in the order is the tiebreaker.

**Schema and sample data:**
```sql
CREATE TABLE bank_txns(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_ts TEXT, signed_amount INTEGER);
INSERT INTO bank_txns VALUES
 (1,1,'2025-06-01 09:00:00',1000),
 (2,1,'2025-06-02 10:00:00',-300),
 (3,1,'2025-06-02 10:00:00',-200),
 (4,2,'2025-06-01 12:00:00',500),
 (5,2,'2025-06-03 08:00:00',250),
 (6,3,'2025-06-05 15:30:00',-40);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH t AS (
  SELECT txn_id, user_id, txn_ts,
         SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts, txn_id
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_after,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_ts DESC, txn_id DESC) AS rn
  FROM bank_txns
)
SELECT user_id, txn_id AS last_txn_id, txn_ts AS last_ts, balance_after
FROM t
WHERE rn = 1
ORDER BY user_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
t = tx.sort_values(["user_id", "txn_ts", "txn_id"]).reset_index(drop=True)
t["balance_after"] = t.groupby("user_id")["signed_amount"].cumsum()
p = (t.groupby("user_id").tail(1)
     .rename(columns={"txn_id": "last_txn_id", "txn_ts": "last_ts"})
     [["user_id", "last_txn_id", "last_ts", "balance_after"]]
     .sort_values("user_id").reset_index(drop=True))
```

**Example:** User 1: txn 1 adds 1000, txn 2 takes 300 and txn 3 takes 200 at the same second (10:00:00). Sorted by (timestamp, txn_id) the balances are 1000, 700, 500, so the latest row is txn 3 with 500. User 2: 500 then 250 gives 750 on txn 5. User 3 has one row, txn 6 with -40, so a negative balance is allowed. The result is one row per user: (1, 3, 500), (2, 5, 750), (3, 6, -40).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q23: latest transaction per user with the balance after it; tie on timestamp broken by txn_id.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE bank_txns(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_ts TEXT, signed_amount INTEGER);
INSERT INTO bank_txns VALUES
 (1,1,'2025-06-01 09:00:00',1000),
 (2,1,'2025-06-02 10:00:00',-300),
 (3,1,'2025-06-02 10:00:00',-200),
 (4,2,'2025-06-01 12:00:00',500),
 (5,2,'2025-06-03 08:00:00',250),
 (6,3,'2025-06-05 15:30:00',-40);
"""
SQL = """
WITH t AS (
  SELECT txn_id, user_id, txn_ts,
         SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts, txn_id
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_after,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_ts DESC, txn_id DESC) AS rn
  FROM bank_txns
)
SELECT user_id, txn_id AS last_txn_id, txn_ts AS last_ts, balance_after
FROM t
WHERE rn = 1
ORDER BY user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

tx = pd.read_sql("SELECT * FROM bank_txns", con)
# PANDAS START
t = tx.sort_values(["user_id", "txn_ts", "txn_id"]).reset_index(drop=True)
t["balance_after"] = t.groupby("user_id")["signed_amount"].cumsum()
p = (t.groupby("user_id").tail(1)
     .rename(columns={"txn_id": "last_txn_id", "txn_ts": "last_ts"})
     [["user_id", "last_txn_id", "last_ts", "balance_after"]]
     .sort_values("user_id").reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (one row per user, ordered by user_id)")

# the tie trap: ORDER BY txn_ts DESC only picks either of txns 2 and 3 for user 1 (not defined)
# and a default-frame running sum gives both tied rows the SAME balance
r = con.execute("""SELECT txn_id, SUM(signed_amount) OVER (PARTITION BY user_id ORDER BY txn_ts) AS bal
                   FROM bank_txns WHERE user_id = 1 ORDER BY txn_id""").fetchall()
print("user 1, default frame, ORDER BY txn_ts only (txn_id, balance):", r)
```

**Output (my run):**
```text
 user_id  last_txn_id             last_ts  balance_after
       1            3 2025-06-02 10:00:00            500
       2            5 2025-06-03 08:00:00            750
       3            6 2025-06-05 15:30:00            -40

 user_id  last_txn_id             last_ts  balance_after
       1            3 2025-06-02 10:00:00            500
       2            5 2025-06-03 08:00:00            750
       3            6 2025-06-05 15:30:00            -40

asserts passed (one row per user, ordered by user_id)
user 1, default frame, ORDER BY txn_ts only (txn_id, balance): [(1, 1000), (2, 500), (3, 500)]
```

**Edge cases:**
- Tie on timestamp: which row is "last" depends on the tiebreaker. With `txn_id` ascending as the posting order, txn 3 is last for user 1; if you broke the tie the other way txn 2 would be last. The final balance (500) is the same either way, the reported `last_txn_id` is not.
- Default frame trap: with `ORDER BY txn_ts` only, the default frame is `RANGE` and tied rows share one balance; the run shows user 1 as (1, 1000), (2, 500), (3, 500), so txn 2 appears to leave 500, not 700.
- A user with a single transaction works (rank 1 is that row). A user with no transactions has no row at all; join from a users table if you need them.
- Timestamps are text in ISO format, which sorts correctly as text.

**Then explain:**
- Two windows with the same partition and the same ordering key, one ascending (running sum) and one descending (pick the last). Part 4 Q9 gives the latest row, Part 5 Q12 the running balance.
- The sum must be computed over all rows before filtering to the last row, so both live in a CTE and the filter is outside.
- pandas: sort, `groupby.cumsum`, then `groupby.tail(1)`; sort first or `cumsum` runs in file order.
- Scoring note (Set T1, Q3 of 5, 20 pts): about 8 pts for three correct rows with balances; 4 pts for a deterministic tiebreak (txn_id) and naming the tie; 4 pts for pandas `cumsum` plus `tail(1)` matching; 2 pts for stating the tie rule; 2 pts for checking that the last balance equals the sum of all amounts per user. Partial credit: a correct latest row without the balance, or a balance from a tie-unsafe frame.

**Follow-ups:**
- Balance before the last transaction? Use `LAG(balance_after)` or subtract the amount.
- Why `ROWS` rather than `RANGE`? `RANGE` treats equal timestamps as one group; `ROWS` counts physical rows in the given order.
- Why not `MAX(txn_ts)` joined back? It returns both tied rows for user 1 and still has no balance.

**Common mistakes:**
- Filtering to the last row first and then summing (the balance becomes just that one amount).
- Ordering by timestamp only and trusting the engine's order for ties.
- In pandas, calling `cumsum` before sorting, or `groupby.last()` which skips NaN per column instead of returning a whole row.

### Q24 ⭐⭐ 🟡 [Set T1, Q2 of 5, 8 min, 20 pts] Duplicate payment detector. payments(payment_id, user_id, merchant, amount, paid_at TEXT). A payment is a suspected duplicate if the same user paid the same merchant the same amount within 5 minutes of an earlier payment (Part 7 Q26 style for adjacent events). Return the later payment ids with the earlier payment id they duplicate. Seed 7 rows including a triple duplicate and a same-amount payment 6 minutes later. SQL (self join or LAG) and pandas (shift within groups).
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Partition by (user, merchant, amount), order by time, use `LAG` to get the previous matching payment and flag the row when the gap is 300 seconds or less; a self join over all earlier matches is the alternative but returns a pair for every earlier payment in the window.

**Schema and sample data:**
```sql
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, merchant TEXT, amount INTEGER, paid_at TEXT);
INSERT INTO payments VALUES
 (1,1,'m1',500,'2025-06-01 10:00:00'),
 (2,1,'m1',500,'2025-06-01 10:02:00'),
 (3,1,'m1',500,'2025-06-01 10:04:30'),
 (4,1,'m1',500,'2025-06-01 10:10:30'),
 (5,2,'m1',500,'2025-06-01 10:01:00'),
 (6,1,'m2',500,'2025-06-01 10:03:00'),
 (7,1,'m1',450,'2025-06-01 10:03:00');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH x AS (
  SELECT payment_id, paid_at,
         LAG(payment_id) OVER w AS earlier_id,
         LAG(paid_at)    OVER w AS earlier_at
  FROM payments
  WINDOW w AS (PARTITION BY user_id, merchant, amount ORDER BY paid_at, payment_id)
)
SELECT payment_id AS later_id, earlier_id,
       CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) AS gap_seconds
FROM x
WHERE earlier_id IS NOT NULL
  AND CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) <= 300
ORDER BY later_id
```
The all-pairs alternative is `SQL_ALL_PAIRS` in the Code block (a self join on the same keys with an earlier-than condition).

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
d = pay.assign(ts=pd.to_datetime(pay["paid_at"])).sort_values(["user_id", "merchant", "amount", "ts", "payment_id"])
g = d.groupby(["user_id", "merchant", "amount"])
d["earlier_id"] = g["payment_id"].shift(1)
d["gap_seconds"] = (d["ts"] - g["ts"].shift(1)).dt.total_seconds()
hit = d[d["earlier_id"].notna() & (d["gap_seconds"] <= 300)]
p = (hit.rename(columns={"payment_id": "later_id"})[["later_id", "earlier_id", "gap_seconds"]]
     .astype({"earlier_id": "int64", "gap_seconds": "int64"})
     .sort_values("later_id").reset_index(drop=True))
```

**Example:** User 1 pays merchant m1 an amount of 500 at 10:00:00 (payment 1), 10:02:00 (payment 2), 10:04:30 (payment 3) and 10:10:30 (payment 4). Payment 2 is 120 seconds after 1, so it duplicates 1. Payment 3 is 150 seconds after 2, so it duplicates 2. Payment 4 is 360 seconds (6 minutes) after 3, so it is not flagged. Payment 5 is another user, payment 6 another merchant and payment 7 another amount, so none of them join any chain. Result: (2 duplicates 1) and (3 duplicates 2).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q24: duplicate payment detector (same user, merchant, amount, within 5 minutes of the previous such payment).
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, user_id INTEGER, merchant TEXT, amount INTEGER, paid_at TEXT);
INSERT INTO payments VALUES
 (1,1,'m1',500,'2025-06-01 10:00:00'),
 (2,1,'m1',500,'2025-06-01 10:02:00'),
 (3,1,'m1',500,'2025-06-01 10:04:30'),
 (4,1,'m1',500,'2025-06-01 10:10:30'),
 (5,2,'m1',500,'2025-06-01 10:01:00'),
 (6,1,'m2',500,'2025-06-01 10:03:00'),
 (7,1,'m1',450,'2025-06-01 10:03:00');
"""
SQL = """
WITH x AS (
  SELECT payment_id, paid_at,
         LAG(payment_id) OVER w AS earlier_id,
         LAG(paid_at)    OVER w AS earlier_at
  FROM payments
  WINDOW w AS (PARTITION BY user_id, merchant, amount ORDER BY paid_at, payment_id)
)
SELECT payment_id AS later_id, earlier_id,
       CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) AS gap_seconds
FROM x
WHERE earlier_id IS NOT NULL
  AND CAST(strftime('%s', paid_at) AS INTEGER) - CAST(strftime('%s', earlier_at) AS INTEGER) <= 300
ORDER BY later_id
"""
SQL_ALL_PAIRS = """
SELECT b.payment_id AS later_id, a.payment_id AS earlier_id
FROM payments a
JOIN payments b
  ON b.user_id = a.user_id AND b.merchant = a.merchant AND b.amount = a.amount
 AND (b.paid_at > a.paid_at OR (b.paid_at = a.paid_at AND b.payment_id > a.payment_id))
 AND CAST(strftime('%s', b.paid_at) AS INTEGER) - CAST(strftime('%s', a.paid_at) AS INTEGER) <= 300
ORDER BY later_id, earlier_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

pay = pd.read_sql("SELECT * FROM payments", con)
# PANDAS START
d = pay.assign(ts=pd.to_datetime(pay["paid_at"])).sort_values(["user_id", "merchant", "amount", "ts", "payment_id"])
g = d.groupby(["user_id", "merchant", "amount"])
d["earlier_id"] = g["payment_id"].shift(1)
d["gap_seconds"] = (d["ts"] - g["ts"].shift(1)).dt.total_seconds()
hit = d[d["earlier_id"].notna() & (d["gap_seconds"] <= 300)]
p = (hit.rename(columns={"payment_id": "later_id"})[["later_id", "earlier_id", "gap_seconds"]]
     .astype({"earlier_id": "int64", "gap_seconds": "int64"})
     .sort_values("later_id").reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (compared after sorting by later_id)")

allp = pd.read_sql(SQL_ALL_PAIRS, con)
print("\nself join on every earlier match returns", len(allp), "pairs:", [(int(a), int(b)) for a, b in allp.values])
print("payment 4 is 6:00 after payment 3, so it is not flagged; gap in seconds:",
      con.execute("SELECT CAST(strftime('%s','2025-06-01 10:10:30') AS INTEGER) - CAST(strftime('%s','2025-06-01 10:04:30') AS INTEGER)").fetchone()[0])
```

**Output (my run):**
```text
 later_id  earlier_id  gap_seconds
        2           1          120
        3           2          150

 later_id  earlier_id  gap_seconds
        2           1          120
        3           2          150

asserts passed (compared after sorting by later_id)

self join on every earlier match returns 3 pairs: [(2, 1), (3, 1), (3, 2)]
payment 4 is 6:00 after payment 3, so it is not flagged; gap in seconds: 360
```

**Edge cases:**
- Triple duplicate: `LAG` links each payment to the previous matching one, so the triple gives 2 rows. A self join on every earlier match gives 3 pairs, (2,1), (3,1) and (3,2), because payment 3 is also within 5 minutes of payment 1 (270 seconds). Decide which one the business wants: one row per suspected duplicate payment (LAG) or every pair.
- Boundary: the rule is `<= 300` seconds, so a gap of exactly 5:00 is flagged; say so, since "within 5 minutes" is ambiguous. The 6:00 case (360 seconds) is not flagged.
- Chains: with `LAG` a stream of payments each 4 minutes apart is flagged all the way down, even though the first and last are far apart; that is usually what a fraud team wants, but say it.
- Same timestamp: `payment_id` breaks the tie so the earlier id is "earlier".
- Time arithmetic on text uses `strftime('%s', ts)` cast to integer seconds; on timestamp columns PostgreSQL would subtract directly (not executed here).

**Then explain:**
- Adjacent events in a group is a `LAG` problem (Part 7 Q26); the partition holds the equality conditions, the `ORDER BY` holds time.
- The 5-minute test is a difference in seconds so it has no calendar rounding.
- pandas: sort, `groupby(...).shift(1)` for the previous id and time, subtract timestamps.
- Scoring note (Set T1, Q2 of 5, 20 pts): about 8 pts for the two correct (later, earlier) pairs; 4 pts for rejecting the 6-minute payment and the different user, merchant and amount rows; 4 pts for pandas `shift` matching; 2 pts for stating inclusive or exclusive and LAG versus all-pairs; 2 pts for a count check (2 flagged of 7). Partial credit: a self join without the earlier-than condition returns each pair twice or pairs a row with itself.

**Follow-ups:**
- Count of duplicates per user? Group the flagged rows by user.
- Why not a `RANGE` window of 5 minutes? SQLite cannot do `RANGE` with an interval over text timestamps (Part 5 and the set note); PostgreSQL 11 and later accepts `RANGE BETWEEN INTERVAL '5 minutes' PRECEDING AND CURRENT ROW` on a timestamp column (not executed here).
- Make it idempotent for retries? That is a data-quality design point: a unique idempotency key beats detecting duplicates after the fact.

**Common mistakes:**
- Self join without `b.paid_at > a.paid_at` (each pair twice, plus a row paired with itself).
- Comparing text timestamps with `<` and forgetting the difference is not a number of minutes.
- Missing the amount (or merchant) in the partition.
- In pandas, shifting without sorting first, or shifting across groups instead of inside them.

### Q25 ⭐⭐ 🟡 [Set T2, Q3 of 5, 8 min, 20 pts] Days past due buckets (lending). loans(loan_id, due_date, paid_date NULL) as of 2025-06-30. Bucket each loan: PAID_ON_TIME, PAID_LATE, CURRENT, DPD_1_30, DPD_31_60, DPD_61_PLUS using days between due_date and paid_date or the as-of date (Part 6 Q3, Part 1 Q10). Seed 9 loans on every boundary (due exactly 30 and 31 days ago). SQL with CASE and julianday, pandas with pd.cut and an explicit as-of date; assert equal and state the boundary rule.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Compute days past due as the as-of date minus the due date for unpaid loans and map it with a CASE whose edges are 0, 30 and 60; paid loans are PAID_ON_TIME when `paid_date <= due_date`, else PAID_LATE.

**Schema and sample data:**
```sql
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, due_date TEXT, paid_date TEXT);
INSERT INTO loans VALUES
 (1,'2025-06-30',NULL),
 (2,'2025-07-15',NULL),
 (3,'2025-06-29',NULL),
 (4,'2025-05-31',NULL),
 (5,'2025-05-30',NULL),
 (6,'2025-05-01',NULL),
 (7,'2025-04-30',NULL),
 (8,'2025-05-10','2025-05-10'),
 (9,'2025-05-10','2025-05-11');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
SELECT loan_id, due_date, paid_date,
       CASE WHEN paid_date IS NULL
            THEN CAST(julianday(:as_of) - julianday(due_date) AS INTEGER) END AS dpd,
       CASE
         WHEN paid_date IS NOT NULL AND paid_date <= due_date THEN 'PAID_ON_TIME'
         WHEN paid_date IS NOT NULL THEN 'PAID_LATE'
         WHEN julianday(:as_of) - julianday(due_date) <= 0 THEN 'CURRENT'
         WHEN julianday(:as_of) - julianday(due_date) <= 30 THEN 'DPD_1_30'
         WHEN julianday(:as_of) - julianday(due_date) <= 60 THEN 'DPD_31_60'
         ELSE 'DPD_61_PLUS'
       END AS bucket
FROM loans
ORDER BY loan_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
as_of = pd.Timestamp("2025-06-30")
due = pd.to_datetime(loans["due_date"])
paid = pd.to_datetime(loans["paid_date"])
dpd = (as_of - due).dt.days
cut = pd.cut(dpd, bins=[-10**6, 0, 30, 60, 10**6],
             labels=["CURRENT", "DPD_1_30", "DPD_31_60", "DPD_61_PLUS"]).astype(object)
bucket = np.select([paid.notna() & (paid <= due), paid.notna()],
                   ["PAID_ON_TIME", "PAID_LATE"], default=cut)
p = loans[["loan_id", "due_date", "paid_date"]].copy()
p["dpd"] = dpd.where(paid.isna())
p["bucket"] = bucket
```

**Example:** As of 2025-06-30: loan 1 is due today (0 days) so CURRENT, loan 2 is due 2025-07-15 (-15) so CURRENT. Loan 3 is due 06-29 (1 day) so DPD_1_30, loan 4 due 05-31 is exactly 30 days so still DPD_1_30, loan 5 due 05-30 is 31 days so DPD_31_60, loan 6 due 05-01 is exactly 60 so DPD_31_60, loan 7 due 04-30 is 61 so DPD_61_PLUS. Loan 8 was paid on its due date so PAID_ON_TIME, loan 9 was paid a day later so PAID_LATE. Bucket counts: CURRENT 2, DPD_1_30 2, DPD_31_60 2, DPD_61_PLUS 1, one PAID_LATE, one PAID_ON_TIME.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q25: days-past-due buckets as of 2025-06-30.
import sqlite3
import numpy as np
import pandas as pd

AS_OF = "2025-06-30"
DDL = """
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, due_date TEXT, paid_date TEXT);
INSERT INTO loans VALUES
 (1,'2025-06-30',NULL),
 (2,'2025-07-15',NULL),
 (3,'2025-06-29',NULL),
 (4,'2025-05-31',NULL),
 (5,'2025-05-30',NULL),
 (6,'2025-05-01',NULL),
 (7,'2025-04-30',NULL),
 (8,'2025-05-10','2025-05-10'),
 (9,'2025-05-10','2025-05-11');
"""
SQL = """
SELECT loan_id, due_date, paid_date,
       CASE WHEN paid_date IS NULL
            THEN CAST(julianday(:as_of) - julianday(due_date) AS INTEGER) END AS dpd,
       CASE
         WHEN paid_date IS NOT NULL AND paid_date <= due_date THEN 'PAID_ON_TIME'
         WHEN paid_date IS NOT NULL THEN 'PAID_LATE'
         WHEN julianday(:as_of) - julianday(due_date) <= 0 THEN 'CURRENT'
         WHEN julianday(:as_of) - julianday(due_date) <= 30 THEN 'DPD_1_30'
         WHEN julianday(:as_of) - julianday(due_date) <= 60 THEN 'DPD_31_60'
         ELSE 'DPD_61_PLUS'
       END AS bucket
FROM loans
ORDER BY loan_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con, params={"as_of": AS_OF})
print(s.to_string(index=False))

loans = pd.read_sql("SELECT * FROM loans", con)
# PANDAS START
as_of = pd.Timestamp("2025-06-30")
due = pd.to_datetime(loans["due_date"])
paid = pd.to_datetime(loans["paid_date"])
dpd = (as_of - due).dt.days
cut = pd.cut(dpd, bins=[-10**6, 0, 30, 60, 10**6],
             labels=["CURRENT", "DPD_1_30", "DPD_31_60", "DPD_61_PLUS"]).astype(object)
bucket = np.select([paid.notna() & (paid <= due), paid.notna()],
                   ["PAID_ON_TIME", "PAID_LATE"], default=cut)
p = loans[["loan_id", "due_date", "paid_date"]].copy()
p["dpd"] = dpd.where(paid.isna())
p["bucket"] = bucket
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by loan_id; dpd NULL equals NaN for paid loans)")
print("pd.cut default is right-closed: 30 falls in (0, 30], 31 in (30, 60]; counts by bucket:")
print(p["bucket"].value_counts().sort_index().to_string())
```

**Output (my run):**
```text
 loan_id   due_date  paid_date   dpd       bucket
       1 2025-06-30        NaN   0.0      CURRENT
       2 2025-07-15        NaN -15.0      CURRENT
       3 2025-06-29        NaN   1.0     DPD_1_30
       4 2025-05-31        NaN  30.0     DPD_1_30
       5 2025-05-30        NaN  31.0    DPD_31_60
       6 2025-05-01        NaN  60.0    DPD_31_60
       7 2025-04-30        NaN  61.0  DPD_61_PLUS
       8 2025-05-10 2025-05-10   NaN PAID_ON_TIME
       9 2025-05-10 2025-05-11   NaN    PAID_LATE

 loan_id   due_date  paid_date   dpd       bucket
       1 2025-06-30        NaN   0.0      CURRENT
       2 2025-07-15        NaN -15.0      CURRENT
       3 2025-06-29        NaN   1.0     DPD_1_30
       4 2025-05-31        NaN  30.0     DPD_1_30
       5 2025-05-30        NaN  31.0    DPD_31_60
       6 2025-05-01        NaN  60.0    DPD_31_60
       7 2025-04-30        NaN  61.0  DPD_61_PLUS
       8 2025-05-10 2025-05-10   NaN PAID_ON_TIME
       9 2025-05-10 2025-05-11   NaN    PAID_LATE

asserts passed (ordered by loan_id; dpd NULL equals NaN for paid loans)
pd.cut default is right-closed: 30 falls in (0, 30], 31 in (30, 60]; counts by bucket:
bucket
CURRENT         2
DPD_1_30        2
DPD_31_60       2
DPD_61_PLUS     1
PAID_LATE       1
PAID_ON_TIME    1
```

**Edge cases:**
- Boundary rule written down: 0 days is CURRENT (due today is not late yet), 1 to 30 inclusive is DPD_1_30, 31 to 60 inclusive is DPD_31_60, 61 and above is DPD_61_PLUS. The run puts day 30 in the first bucket and day 31 in the next, day 60 in DPD_31_60 and day 61 in DPD_61_PLUS.
- `pd.cut` is right-closed by default, so bins `(-inf, 0], (0, 30], (30, 60], (60, inf)` reproduce those edges; `right=False` would move every boundary day into the next bucket.
- Paid loans have no days-past-due value (NULL in SQL, NaN in pandas); the unpaid-only `dpd` column avoids mixing the two meanings.
- A future due date gives a negative number (-15), which is CURRENT.
- Not in the seed: a loan paid after the as-of date would need `paid_date > as_of` treated as unpaid at that date; say so rather than silently labelling it paid.
- `julianday` differences are whole numbers for date-only text; with times they would be fractions and `CAST` truncates.

**Then explain:**
- Order the CASE branches so the paid cases come first; a paid loan must never reach the days-past-due branches.
- The as-of date is a parameter, not `date('now')`, so results are reproducible. The SQL binds it by name (`:as_of`).
- Part 6 Q3 is the date difference, Part 1 Q10 the CASE bucketing.
- Scoring note (Set T2, Q3 of 5, 20 pts): about 8 pts for all 9 buckets right; 4 pts for the boundary days (30, 31, 60, 61) landing correctly and paid loans handled before the DPD branches; 4 pts for pandas `pd.cut` (or `np.select`) matching; 2 pts for stating the boundary rule first; 2 pts for a count check (9 loans, bucket counts add to 9). Partial credit: correct buckets for unpaid loans only.

**Follow-ups:**
- Weighted exposure per bucket? Sum the outstanding amount per bucket (Part 2 Q5 style).
- Why a parameter instead of today's date? Reproducible reports and tests.
- Month-end snapshots for every month? Cross join the loans with a spine of as-of dates, not executed here.

**Common mistakes:**
- Using `<` where the rule says `<=` and moving day 30 into the next bucket.
- Treating due-today as late.
- `pd.cut` with default `right=True` misread as left-closed.
- Letting paid loans fall into the DPD branches because the NULL check came last.

### Q26 ⭐⭐ 🟡 [Set T2, Q2 of 5, 8 min, 20 pts] Running balance with same-timestamp ties (Part 5 Q6). acct_txns(txn_id, account_id, txn_ts, amount_paise) where deposits are positive. Return each transaction with a running balance per account in a deterministic order, and show what a RANGE-framed or ORDER BY txn_ts-only version returns when two rows share a timestamp. Seed 2 accounts with a tie. Give SQL and pandas and say which tie rule you chose.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Use `SUM(amount) OVER (PARTITION BY account ORDER BY txn_ts, txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`; ordering by the timestamp alone uses the default `RANGE` frame, which gives tied rows the same balance.

**Schema and sample data:**
```sql
CREATE TABLE acct_txns(txn_id INTEGER PRIMARY KEY, account_id INTEGER, txn_ts TEXT, amount_paise INTEGER);
INSERT INTO acct_txns VALUES
 (1,1,'2025-06-01 09:00:00',10000),
 (2,1,'2025-06-01 10:00:00',-2500),
 (3,1,'2025-06-01 10:00:00',-4000),
 (4,1,'2025-06-02 09:00:00',700),
 (5,2,'2025-06-01 11:00:00',3000),
 (6,2,'2025-06-01 12:00:00',-500);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
SELECT txn_id, account_id, txn_ts, amount_paise,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_rows,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts) AS balance_default_range
FROM acct_txns
ORDER BY account_id, txn_ts, txn_id
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
p = t.sort_values(["account_id", "txn_ts", "txn_id"]).reset_index(drop=True)
p["balance_rows"] = p.groupby("account_id")["amount_paise"].cumsum()
# RANGE-like: every row of a tied timestamp shows the balance after the whole tie group
p["balance_default_range"] = p.groupby(["account_id", "txn_ts"])["balance_rows"].transform("last")
```

**Example:** Account 1: +10000 at 09:00, then -2500 (txn 2) and -4000 (txn 3) both at 10:00:00, then +700 the next day. Deterministic order by (txn_ts, txn_id): 10000, 7500, 3500, 4200. With `ORDER BY txn_ts` only (default `RANGE` frame) rows 2 and 3 are peers, so both show 3500, the balance after the whole tie group; the intermediate 7500 never appears. Account 2: 3000 then -500 gives 3000, 2500 (no tie).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q26: running balance per account with a same-timestamp tie.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE acct_txns(txn_id INTEGER PRIMARY KEY, account_id INTEGER, txn_ts TEXT, amount_paise INTEGER);
INSERT INTO acct_txns VALUES
 (1,1,'2025-06-01 09:00:00',10000),
 (2,1,'2025-06-01 10:00:00',-2500),
 (3,1,'2025-06-01 10:00:00',-4000),
 (4,1,'2025-06-02 09:00:00',700),
 (5,2,'2025-06-01 11:00:00',3000),
 (6,2,'2025-06-01 12:00:00',-500);
"""
SQL = """
SELECT txn_id, account_id, txn_ts, amount_paise,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance_rows,
       SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts) AS balance_default_range
FROM acct_txns
ORDER BY account_id, txn_ts, txn_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

t = pd.read_sql("SELECT * FROM acct_txns", con)
# PANDAS START
p = t.sort_values(["account_id", "txn_ts", "txn_id"]).reset_index(drop=True)
p["balance_rows"] = p.groupby("account_id")["amount_paise"].cumsum()
# RANGE-like: every row of a tied timestamp shows the balance after the whole tie group
p["balance_default_range"] = p.groupby(["account_id", "txn_ts"])["balance_rows"].transform("last")
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by account_id, txn_ts, txn_id; both balance columns equal)")

# reversing txn_id inside the tie changes the intermediate balance but not the final one
alt = con.execute("""SELECT txn_id, SUM(amount_paise) OVER (PARTITION BY account_id ORDER BY txn_ts, txn_id DESC
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM acct_txns
                     WHERE account_id = 1 ORDER BY txn_id""").fetchall()
print("account 1 with the tie broken by txn_id DESC (txn_id, balance):", alt)
```

**Output (my run):**
```text
 txn_id  account_id              txn_ts  amount_paise  balance_rows  balance_default_range
      1           1 2025-06-01 09:00:00         10000         10000                  10000
      2           1 2025-06-01 10:00:00         -2500          7500                   3500
      3           1 2025-06-01 10:00:00         -4000          3500                   3500
      4           1 2025-06-02 09:00:00           700          4200                   4200
      5           2 2025-06-01 11:00:00          3000          3000                   3000
      6           2 2025-06-01 12:00:00          -500          2500                   2500

 txn_id  account_id              txn_ts  amount_paise  balance_rows  balance_default_range
      1           1 2025-06-01 09:00:00         10000         10000                  10000
      2           1 2025-06-01 10:00:00         -2500          7500                   3500
      3           1 2025-06-01 10:00:00         -4000          3500                   3500
      4           1 2025-06-02 09:00:00           700          4200                   4200
      5           2 2025-06-01 11:00:00          3000          3000                   3000
      6           2 2025-06-01 12:00:00          -500          2500                   2500

asserts passed (ordered by account_id, txn_ts, txn_id; both balance columns equal)
account 1 with the tie broken by txn_id DESC (txn_id, balance): [(1, 10000), (2, 3500), (3, 6000), (4, 4200)]
```

**Edge cases:**
- Tie rule chosen: the ledger sequence `txn_id` ascending, because ids are assigned in posting order. If the tie were broken by `txn_id` DESC the run gives 10000, 3500, 6000, 4200 for account 1 (txn 3 first), so the intermediate balance changes while the end balance (4200) does not.
- A negative intermediate balance can appear or vanish depending on the tie order, which is why overdraft checks must use a defined order.
- RANGE-framed or ORDER BY txn_ts-only: peers share one value (shown in the last column). `ROWS` with only the timestamp in the order is a different trap: the order inside the tie is not defined, so I did not rely on it (not shown).
- Amounts are integer paise, so the sums are exact; floats would drift.
- pandas has no frame default: `cumsum` is always row by row after your sort, so it matches the `ROWS` column; the `RANGE` column needs `transform("last")` over the tied group.

**Then explain:**
- Same idea as Part 5 Q6: a running total needs a total order of rows, and timestamps alone are not one.
- `ROWS` counts physical rows; `RANGE` groups rows with equal ORDER BY values (peers). The standard's default frame when an ORDER BY is present is `RANGE UNBOUNDED PRECEDING` to `CURRENT ROW`, and PostgreSQL behaves the same (not executed here); SQLite showed it in the run.
- State the tie rule as a business rule, not a coincidence of `rowid` order.
- Scoring note (Set T2, Q2 of 5, 20 pts): about 8 pts for the correct deterministic running balance on all 6 rows; 4 pts for showing and explaining what the tie does under the default frame; 4 pts for pandas `cumsum` after a full sort matching (and, for a strong answer, the `transform("last")` for the peer behaviour); 2 pts for naming the tie rule; 2 pts for a check that the last balance per account equals the account total. Partial credit: a correct running sum that orders by timestamp only (right on the seed by luck, undefined on ties).

**Follow-ups:**
- Why does the default frame use RANGE? The standard says so; it is meant to treat equal sort keys as one position, which is surprising for ledgers.
- First moment the balance goes below zero? Filter the running balance (Part 5 Q22).
- What if two engines break ties differently? Then the results differ; only a total order (timestamp, id) is portable.

**Common mistakes:**
- `ORDER BY txn_ts` only, then reporting the same balance for two different transactions.
- Using floats for money.
- In pandas, sorting by timestamp only with an unstable sort and expecting a stable tie order (use a total key).
- Believing `ROWS` fixes ties by itself; it does not define the order inside the tie.

### Q27 ⭐⭐ 🟡 [Set T3, Q3 of 5, 8 min, 20 pts] Cohort retention counts, months 0 to 2 (Part 6 Q10, Q11). wallet_topups(customer_id, topup_date). Cohort = month of first top-up; return cohort_month, month_offset 0 to 2 and distinct customers active. Missing offsets must show 0, and cohorts too young to observe offset 2 must show NULL as of 2025-04-30. Seed 8 customers across Jan and Feb 2025 cohorts. SQL and pandas, asserting equal.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Find each customer's first top-up month, count distinct active customers per (cohort, month offset) from a 0 to 2 offsets list, return 0 where nobody was active, and return NULL where the offset month is not finished by the as-of date.

**Schema and sample data:**
```sql
CREATE TABLE wallet_topups(customer_id INTEGER, topup_date TEXT);
INSERT INTO wallet_topups VALUES
 (1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-12'),
 (2,'2025-01-20'),(2,'2025-03-03'),
 (3,'2025-01-15'),(3,'2025-01-25'),
 (4,'2025-01-31'),(4,'2025-02-01'),
 (5,'2025-01-02'),
 (6,'2025-02-03'),(6,'2025-03-04'),(6,'2025-04-05'),
 (7,'2025-02-14'),(7,'2025-04-20'),
 (8,'2025-02-28');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH t AS (
  SELECT DISTINCT customer_id, substr(topup_date, 1, 7) AS act_month
  FROM wallet_topups WHERE topup_date <= :as_of
),
first AS (
  SELECT customer_id, MIN(act_month) AS cohort_month FROM t GROUP BY customer_id
),
offs(month_offset) AS (VALUES (0), (1), (2)),
cohorts AS (
  SELECT cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY cohort_month
)
SELECT c.cohort_month, o.month_offset,
       CASE WHEN date(c.cohort_month || '-01', '+' || (o.month_offset + 1) || ' months', '-1 day') <= :as_of
            THEN (SELECT COUNT(*) FROM first f JOIN t
                    ON t.customer_id = f.customer_id
                   AND t.act_month = substr(date(f.cohort_month || '-01', '+' || o.month_offset || ' months'), 1, 7)
                  WHERE f.cohort_month = c.cohort_month)
       END AS active
FROM cohorts c CROSS JOIN offs o
ORDER BY c.cohort_month, o.month_offset
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
def pandas_version(raw, as_of):
    as_of = pd.Timestamp(as_of)
    d = raw.assign(m=pd.to_datetime(raw["topup_date"]).dt.to_period("M"))
    d = d[pd.to_datetime(raw["topup_date"]) <= as_of][["customer_id", "m"]].drop_duplicates()
    d["cohort"] = d.groupby("customer_id")["m"].transform("min")
    d["off"] = (d["m"] - d["cohort"]).apply(lambda x: x.n)
    counts = d.groupby(["cohort", "off"])["customer_id"].nunique()
    rows = []
    for c in sorted(d["cohort"].unique()):
        for off in range(3):
            done = (c + off).end_time.normalize() <= as_of
            rows.append((str(c), off, int(counts.get((c, off), 0)) if done else None))
    return pd.DataFrame(rows, columns=["cohort_month", "month_offset", "active"])
```

**Example:** January cohort: customers 1 to 5 (5 people). Active in January (offset 0): all 5. Active in February (offset 1): customers 1 and 4, so 2. Active in March (offset 2): customers 1 and 2, so 2. February cohort: customers 6, 7, 8 (3 people), offset 0 = 3, offset 1 (March) = customer 6 only = 1, offset 2 (April) = customers 6 and 7 = 2. As of 2025-04-30 that is 6 rows with no NULLs. The first run therefore shows the retention table; the second run (as of 2025-03-31) turns February offset 2 into NULL because April is not over; the third run deletes customers 1 and 4 to show a true zero (January offset 1 becomes 0).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q27: cohort retention counts for months 0 to 2, NULL where the offset month is not finished yet.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE wallet_topups(customer_id INTEGER, topup_date TEXT);
INSERT INTO wallet_topups VALUES
 (1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-12'),
 (2,'2025-01-20'),(2,'2025-03-03'),
 (3,'2025-01-15'),(3,'2025-01-25'),
 (4,'2025-01-31'),(4,'2025-02-01'),
 (5,'2025-01-02'),
 (6,'2025-02-03'),(6,'2025-03-04'),(6,'2025-04-05'),
 (7,'2025-02-14'),(7,'2025-04-20'),
 (8,'2025-02-28');
"""
SQL = """
WITH t AS (
  SELECT DISTINCT customer_id, substr(topup_date, 1, 7) AS act_month
  FROM wallet_topups WHERE topup_date <= :as_of
),
first AS (
  SELECT customer_id, MIN(act_month) AS cohort_month FROM t GROUP BY customer_id
),
offs(month_offset) AS (VALUES (0), (1), (2)),
cohorts AS (
  SELECT cohort_month, COUNT(*) AS cohort_size FROM first GROUP BY cohort_month
)
SELECT c.cohort_month, o.month_offset,
       CASE WHEN date(c.cohort_month || '-01', '+' || (o.month_offset + 1) || ' months', '-1 day') <= :as_of
            THEN (SELECT COUNT(*) FROM first f JOIN t
                    ON t.customer_id = f.customer_id
                   AND t.act_month = substr(date(f.cohort_month || '-01', '+' || o.month_offset || ' months'), 1, 7)
                  WHERE f.cohort_month = c.cohort_month)
       END AS active
FROM cohorts c CROSS JOIN offs o
ORDER BY c.cohort_month, o.month_offset
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
raw = pd.read_sql("SELECT * FROM wallet_topups", con)

# PANDAS START
def pandas_version(raw, as_of):
    as_of = pd.Timestamp(as_of)
    d = raw.assign(m=pd.to_datetime(raw["topup_date"]).dt.to_period("M"))
    d = d[pd.to_datetime(raw["topup_date"]) <= as_of][["customer_id", "m"]].drop_duplicates()
    d["cohort"] = d.groupby("customer_id")["m"].transform("min")
    d["off"] = (d["m"] - d["cohort"]).apply(lambda x: x.n)
    counts = d.groupby(["cohort", "off"])["customer_id"].nunique()
    rows = []
    for c in sorted(d["cohort"].unique()):
        for off in range(3):
            done = (c + off).end_time.normalize() <= as_of
            rows.append((str(c), off, int(counts.get((c, off), 0)) if done else None))
    return pd.DataFrame(rows, columns=["cohort_month", "month_offset", "active"])
# PANDAS END

def run(as_of, raw):
    s = pd.read_sql(SQL, con, params={"as_of": as_of})
    p = pandas_version(raw, as_of)
    s["active"] = s["active"].astype("Float64"); p["active"] = p["active"].astype("Float64")
    print(s.to_string(index=False))
    pd.testing.assert_frame_equal(s, p, check_dtype=False)
    print("asserts passed (ordered by cohort_month, month_offset)\n")

print("as of 2025-04-30 (both cohorts fully observable)")
run("2025-04-30", raw)
print("as of 2025-03-31 (February cohort is too young for offset 2)")
run("2025-03-31", raw)
con.execute("DELETE FROM wallet_topups WHERE customer_id IN (1, 4)")
raw2 = pd.read_sql("SELECT * FROM wallet_topups", con)
print("as of 2025-04-30 after deleting customers 1 and 4 (nobody active in February from the January cohort)")
run("2025-04-30", raw2)
```

**Output (my run):**
```text
as of 2025-04-30 (both cohorts fully observable)
cohort_month  month_offset  active
     2025-01             0     5.0
     2025-01             1     2.0
     2025-01             2     2.0
     2025-02             0     3.0
     2025-02             1     1.0
     2025-02             2     2.0
asserts passed (ordered by cohort_month, month_offset)

as of 2025-03-31 (February cohort is too young for offset 2)
cohort_month  month_offset  active
     2025-01             0     5.0
     2025-01             1     2.0
     2025-01             2     2.0
     2025-02             0     3.0
     2025-02             1     1.0
     2025-02             2    <NA>
asserts passed (ordered by cohort_month, month_offset)

as of 2025-04-30 after deleting customers 1 and 4 (nobody active in February from the January cohort)
cohort_month  month_offset  active
     2025-01             0     3.0
     2025-01             1     0.0
     2025-01             2     1.0
     2025-02             0     3.0
     2025-02             1     1.0
     2025-02             2     2.0
asserts passed (ordered by cohort_month, month_offset)
```

**Edge cases:**
- Premise check: the question asks for NULL for cohorts too young as of 2025-04-30, but with only January and February cohorts and offsets 0 to 2, every offset month (the latest is April, which ends on 04-30) is already finished, so no NULL appears. I show the NULL rule with an earlier as-of date (2025-03-31) where February offset 2 is NULL. With a March cohort in the data, March offset 2 (May) would be NULL on 2025-04-30.
- Zero versus NULL: zero means observed and nobody came back (third run: January offset 1 is 0); NULL means not observable yet. Mixing them makes young cohorts look like churn.
- Observable rule used: the offset month is complete when its last day is on or before the as-of date, written `date(cohort || '-01', '+k months', '-1 day') <= :as_of` (so a mid-month as-of date makes that month NULL).
- Duplicates: a customer topping up three times in a month counts once (`DISTINCT` over customer and month); customer 3 has two January rows.
- Data after the as-of date is ignored (customer 6's April top-up is excluded in the March run).
- pandas returns `None` for the unobservable cells; the comparison uses the nullable Float64 type so NaN equals NULL.

**Then explain:**
- Three small tables: first month per customer (cohort), distinct customer-months (activity), and the offsets list (0, 1, 2). The result is cohort times offset, not only the offsets that happen to have data.
- Month offset is calendar months between first top-up month and activity month (Part 6 Q10); in pandas a `Period` subtraction gives it.
- The `VALUES` common table expression for offsets is standard in SQLite (`WITH offs(month_offset) AS (VALUES (0), (1), (2))`).
- Scoring note (Set T3, Q3 of 5, 20 pts): about 8 pts for the correct counts (5, 2, 2 and 3, 1, 2); 4 pts for the zero versus NULL distinction and the observable-month rule; 4 pts for the pandas version matching on all scenarios; 2 pts for saying what a month offset means and that active means at least one top-up; 2 pts for a check (offset 0 equals cohort size). Partial credit: counts without NULL handling, or offsets that exist only where there is data.

**Follow-ups:**
- Retention percent? Divide by the offset 0 count; keep NULL for unobserved cells (Part 6 Q11).
- Month offset when the cohort is defined by signup, not first top-up? Same shape, different source of the cohort month.
- Why not `DATEDIFF` in months? SQLite has none; Postgres `age` or `DATE_DIFF` variants exist (not executed here).

**Common mistakes:**
- Returning no row for an offset nobody reached, which hides a zero.
- Treating a young cohort's missing future as 0 retention.
- Counting rows instead of distinct customers.
- Off-by-one on the offset (month 1 is the month after the first top-up, not the same month).

### Q28 ⭐⭐ 🟡 [Set T3, Q2 of 5, 8 min, 20 pts] Chargeback rate by merchant category without fan-out (Part 8 Q10, Q11). merchants(merchant_id, category), card_payments(payment_id, merchant_id, amount), chargebacks(chargeback_id, payment_id, amount) with one payment having two chargeback rows. Return per category the payment count, the number of payments with any chargeback, the rate and the chargeback amount. Show the naive join count and then the correct one. SQL and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Pre-aggregate the chargebacks to one row per payment before joining, then count payments with `COUNT(*)` and payments with a chargeback with `COUNT(cb.payment_id)`; joining the raw chargebacks repeats the payment and inflates its counts.

**Schema and sample data:**
```sql
CREATE TABLE merchants(merchant_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE card_payments(payment_id INTEGER PRIMARY KEY, merchant_id INTEGER, amount INTEGER);
CREATE TABLE chargebacks(chargeback_id INTEGER PRIMARY KEY, payment_id INTEGER, amount INTEGER);
INSERT INTO merchants VALUES (1,'travel'),(2,'travel'),(3,'grocery'),(4,'gaming');
INSERT INTO card_payments VALUES
 (1,1,1000),(2,1,2000),(3,2,500),(4,2,700),(5,3,300),(6,3,400),(7,3,350),(8,3,250),(9,4,900);
INSERT INTO chargebacks VALUES (1,1,600),(2,1,400),(3,3,500),(4,5,300);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
Naive version (shows the fan-out):
```sql
SELECT m.category, COUNT(*) AS payments, SUM(c.amount) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN chargebacks c ON c.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
```
```sql
WITH cb AS (
  SELECT payment_id, SUM(amount) AS cb_amount
  FROM chargebacks
  GROUP BY payment_id
)
SELECT m.category,
       COUNT(*) AS payments,
       COUNT(cb.payment_id) AS payments_with_cb,
       ROUND(1.0 * COUNT(cb.payment_id) / COUNT(*), 4) AS cb_rate,
       COALESCE(SUM(cb.cb_amount), 0) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN cb ON cb.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
cb = cbs.groupby("payment_id", as_index=False)["amount"].sum().rename(columns={"amount": "cb_amount"})
d = pay.merge(mer, on="merchant_id").merge(cb, on="payment_id", how="left")
p = (d.groupby("category")
       .agg(payments=("payment_id", "size"),
            payments_with_cb=("cb_amount", "count"),
            chargeback_amount=("cb_amount", "sum"))
       .reset_index())
p["cb_rate"] = (p["payments_with_cb"] / p["payments"]).round(4)
p = p[["category", "payments", "payments_with_cb", "cb_rate", "chargeback_amount"]].sort_values("category").reset_index(drop=True)
```

**Example:** Payment 1 has two chargebacks (600 and 400). Naive join payment-to-chargeback: travel shows 5 payments instead of 4 because payment 1 appears twice. Pre-aggregated: travel has payments 1 to 4 (merchants 1 and 2), payments 1 and 3 have chargebacks, so 2 of 4 = 0.5 and the chargeback amount is 1000 + 500 = 1500. Grocery has payments 5 to 8, only payment 5 has a chargeback (300), so 1 of 4 = 0.25. Gaming has payment 9 with none: 0 of 1 = 0.00 and an amount of 0 (not NULL).

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q28: chargeback rate by merchant category without fan-out.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE merchants(merchant_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE card_payments(payment_id INTEGER PRIMARY KEY, merchant_id INTEGER, amount INTEGER);
CREATE TABLE chargebacks(chargeback_id INTEGER PRIMARY KEY, payment_id INTEGER, amount INTEGER);
INSERT INTO merchants VALUES (1,'travel'),(2,'travel'),(3,'grocery'),(4,'gaming');
INSERT INTO card_payments VALUES
 (1,1,1000),(2,1,2000),(3,2,500),(4,2,700),(5,3,300),(6,3,400),(7,3,350),(8,3,250),(9,4,900);
INSERT INTO chargebacks VALUES (1,1,600),(2,1,400),(3,3,500),(4,5,300);
"""
SQL_NAIVE = """
SELECT m.category, COUNT(*) AS payments, SUM(c.amount) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN chargebacks c ON c.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
"""
SQL = """
WITH cb AS (
  SELECT payment_id, SUM(amount) AS cb_amount
  FROM chargebacks
  GROUP BY payment_id
)
SELECT m.category,
       COUNT(*) AS payments,
       COUNT(cb.payment_id) AS payments_with_cb,
       ROUND(1.0 * COUNT(cb.payment_id) / COUNT(*), 4) AS cb_rate,
       COALESCE(SUM(cb.cb_amount), 0) AS chargeback_amount
FROM card_payments p
JOIN merchants m ON m.merchant_id = p.merchant_id
LEFT JOIN cb ON cb.payment_id = p.payment_id
GROUP BY m.category
ORDER BY m.category
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
naive = pd.read_sql(SQL_NAIVE, con)
print("naive join (payment 1 has two chargebacks):")
print(naive.to_string(index=False))
s = pd.read_sql(SQL, con)
print("\npre-aggregated:")
print(s.to_string(index=False))

pay = pd.read_sql("SELECT * FROM card_payments", con)
mer = pd.read_sql("SELECT * FROM merchants", con)
cbs = pd.read_sql("SELECT * FROM chargebacks", con)
# PANDAS START
cb = cbs.groupby("payment_id", as_index=False)["amount"].sum().rename(columns={"amount": "cb_amount"})
d = pay.merge(mer, on="merchant_id").merge(cb, on="payment_id", how="left")
p = (d.groupby("category")
       .agg(payments=("payment_id", "size"),
            payments_with_cb=("cb_amount", "count"),
            chargeback_amount=("cb_amount", "sum"))
       .reset_index())
p["cb_rate"] = (p["payments_with_cb"] / p["payments"]).round(4)
p = p[["category", "payments", "payments_with_cb", "cb_rate", "chargeback_amount"]].sort_values("category").reset_index(drop=True)
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by category)")

nv = pay.merge(mer, on="merchant_id").merge(cbs, on="payment_id", how="left")
print("pandas naive merge rows:", len(nv), "vs payments:", len(pay))
```

**Output (my run):**
```text
naive join (payment 1 has two chargebacks):
category  payments  chargeback_amount
  gaming         1                NaN
 grocery         4              300.0
  travel         5             1500.0

pre-aggregated:
category  payments  payments_with_cb  cb_rate  chargeback_amount
  gaming         1                 0     0.00                  0
 grocery         4                 1     0.25                300
  travel         4                 2     0.50               1500

category  payments  payments_with_cb  cb_rate  chargeback_amount
  gaming         1                 0     0.00                0.0
 grocery         4                 1     0.25              300.0
  travel         4                 2     0.50             1500.0

asserts passed (ordered by category)
pandas naive merge rows: 10 vs payments: 9
```

**Edge cases:**
- Fan-out: the naive query reports 5 travel payments (the run) and the pandas naive merge gives 10 rows for 9 payments. The chargeback sum itself (1500) survives in this seed because each chargeback row is counted once, but any payment-side measure would be double counted.
- Categories with no chargeback: NULL in the naive output (gaming), 0 after `COALESCE` in SQL; in pandas `sum` of an all-NaN group is 0.0, so the column is float (0.0 versus integer 0 in SQL, compared with `check_dtype=False`).
- A payment with two chargebacks counts once in `payments_with_cb`; if the business wants chargeback events, count chargeback rows instead and say so.
- A merchant with no payments would not appear (join from payments); start from merchants if empty categories must show.

**Then explain:**
- This is Part 8 Q10: aggregate the many side to the grain of the one side before the join, so the join is one-to-one.
- `COUNT(cb.payment_id)` counts non-NULL, so payments without chargebacks are not counted.
- pandas: `groupby("payment_id").sum()` then a left merge, then named aggregation (`count` skips NaN, `size` does not).
- Scoring note (Set T3, Q2 of 5, 20 pts): about 8 pts for the correct pre-aggregated table (4, 2, 0.5, 1500 for travel); 4 pts for demonstrating the naive count (5) and explaining the fan-out; 4 pts for pandas matching; 2 pts for stating payments versus chargeback events as the unit; 2 pts for a check that the payment counts add up to 9. Partial credit: `COUNT(DISTINCT payment_id)` on the naive join gets the counts right but still double counts any payment amount.

**Follow-ups:**
- Chargeback amount as a percent of payment volume? Sum payment amounts on the payment side first, then divide; never `SUM(p.amount)` after the fan-out join.
- `COUNT(DISTINCT)` fix? Works for counts, not for sums; pre-aggregation fixes both.
- Time lag between payment and chargeback? Bucket by months since payment, a cohort-style cut (Part 6).

**Common mistakes:**
- `COUNT(*)` after a one-to-many join.
- `SUM(payment.amount)` after the join, which counts payment 1's amount twice.
- Inner joining chargebacks and losing categories with no chargebacks.
- Reporting NULL instead of 0 for the chargeback amount.

### Q29 ⭐⭐ 🟡 [Set E1, Q3 of 5, 8 min, 20 pts] Repeat purchase and days to second order (Part 6 Q20, Part 8 Q21). orders(order_id, customer_id, order_date, status). Exclude CANCELLED orders. Return the share of customers with 2 or more orders and the average days between first and second order among them. Seed 8 customers including one whose first order was cancelled and a same-day second order. SQL and pandas, and state the denominator.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Drop CANCELLED orders first, number each customer's remaining orders by date, take the first and second dates per customer, and divide customers with a second order by customers with at least one non-cancelled order; the average gap uses only those repeaters.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2025-01-01','DELIVERED'),(2,1,'2025-01-31','DELIVERED'),
 (3,2,'2025-01-05','DELIVERED'),(4,2,'2025-01-05','DELIVERED'),
 (5,3,'2025-01-01','CANCELLED'),(6,3,'2025-01-10','DELIVERED'),(7,3,'2025-01-20','DELIVERED'),
 (8,4,'2025-02-01','DELIVERED'),
 (9,5,'2025-02-10','DELIVERED'),
 (10,6,'2025-03-01','DELIVERED'),(11,6,'2025-03-05','CANCELLED'),
 (12,7,'2025-01-15','DELIVERED'),(13,7,'2025-02-14','DELIVERED'),(14,7,'2025-03-16','DELIVERED'),
 (15,8,'2025-02-20','CANCELLED');
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
WITH ok AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
  WHERE status <> 'CANCELLED'
),
per AS (
  SELECT customer_id,
         MAX(CASE WHEN rn = 1 THEN order_date END) AS first_date,
         MAX(CASE WHEN rn = 2 THEN order_date END) AS second_date
  FROM ok
  GROUP BY customer_id
)
SELECT COUNT(*) AS customers,
       COUNT(second_date) AS repeaters,
       ROUND(1.0 * COUNT(second_date) / COUNT(*), 4) AS repeat_share,
       AVG(julianday(second_date) - julianday(first_date)) AS avg_days_to_second
FROM per
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
ok = o[o["status"] != "CANCELLED"].copy()
ok["order_date"] = pd.to_datetime(ok["order_date"])
ok = ok.sort_values(["customer_id", "order_date", "order_id"])
ok["rn"] = ok.groupby("customer_id").cumcount() + 1
first = ok[ok["rn"] == 1].set_index("customer_id")["order_date"]
second = ok[ok["rn"] == 2].set_index("customer_id")["order_date"]
days = (second - first.reindex(second.index)).dt.days
p = pd.DataFrame({"customers": [len(first)], "repeaters": [len(second)],
                  "repeat_share": [round(len(second) / len(first), 4)],
                  "avg_days_to_second": [days.mean()]})
```

**Example:** After dropping cancelled orders: customer 1 has 01-01 and 01-31 (30 days), customer 2 has two orders on 01-05 (0 days), customer 3 loses the cancelled 01-01 order and has 01-10 and 01-20 (10 days), customers 4 and 5 have one order each, customer 6 keeps only 03-01 (the second order was cancelled), customer 7 has 01-15, 02-14, 03-16 (first to second 30 days), customer 8 had only a cancelled order so disappears. That leaves 7 customers, 4 repeaters (1, 2, 3, 7), share 4/7 = 0.5714 and average (30 + 0 + 10 + 30) / 4 = 17.5 days.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q29: repeat purchase share and days from first to second order, cancelled orders excluded.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
INSERT INTO orders VALUES
 (1,1,'2025-01-01','DELIVERED'),(2,1,'2025-01-31','DELIVERED'),
 (3,2,'2025-01-05','DELIVERED'),(4,2,'2025-01-05','DELIVERED'),
 (5,3,'2025-01-01','CANCELLED'),(6,3,'2025-01-10','DELIVERED'),(7,3,'2025-01-20','DELIVERED'),
 (8,4,'2025-02-01','DELIVERED'),
 (9,5,'2025-02-10','DELIVERED'),
 (10,6,'2025-03-01','DELIVERED'),(11,6,'2025-03-05','CANCELLED'),
 (12,7,'2025-01-15','DELIVERED'),(13,7,'2025-02-14','DELIVERED'),(14,7,'2025-03-16','DELIVERED'),
 (15,8,'2025-02-20','CANCELLED');
"""
SQL = """
WITH ok AS (
  SELECT customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
  WHERE status <> 'CANCELLED'
),
per AS (
  SELECT customer_id,
         MAX(CASE WHEN rn = 1 THEN order_date END) AS first_date,
         MAX(CASE WHEN rn = 2 THEN order_date END) AS second_date
  FROM ok
  GROUP BY customer_id
)
SELECT COUNT(*) AS customers,
       COUNT(second_date) AS repeaters,
       ROUND(1.0 * COUNT(second_date) / COUNT(*), 4) AS repeat_share,
       AVG(julianday(second_date) - julianday(first_date)) AS avg_days_to_second
FROM per
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

o = pd.read_sql("SELECT * FROM orders", con)
# PANDAS START
ok = o[o["status"] != "CANCELLED"].copy()
ok["order_date"] = pd.to_datetime(ok["order_date"])
ok = ok.sort_values(["customer_id", "order_date", "order_id"])
ok["rn"] = ok.groupby("customer_id").cumcount() + 1
first = ok[ok["rn"] == 1].set_index("customer_id")["order_date"]
second = ok[ok["rn"] == 2].set_index("customer_id")["order_date"]
days = (second - first.reindex(second.index)).dt.days
p = pd.DataFrame({"customers": [len(first)], "repeaters": [len(second)],
                  "repeat_share": [round(len(second) / len(first), 4)],
                  "avg_days_to_second": [days.mean()]})
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (single row)")
print("per-customer days to second order:", days.sort_index().to_dict())
print("customers with any order (incl. cancelled-only):", o["customer_id"].nunique(),
      "-> share on that denominator:", round(len(second) / o["customer_id"].nunique(), 4))
```

**Output (my run):**
```text
 customers  repeaters  repeat_share  avg_days_to_second
         7          4        0.5714                17.5

 customers  repeaters  repeat_share  avg_days_to_second
         7          4        0.5714                17.5

asserts passed (single row)
per-customer days to second order: {1: 30, 2: 0, 3: 10, 7: 30}
customers with any order (incl. cancelled-only): 8 -> share on that denominator: 0.5
```

**Edge cases:**
- Denominator: customers with at least one non-cancelled order (7). Using all customers in the table (8, including the cancelled-only customer 8) gives 0.5, as the run prints. Say which one, since both are defensible.
- First order cancelled: customer 3 is a repeater measured from the first surviving order, not from the cancelled one.
- Same-day second order: customer 2 gives 0 days and still counts as a repeater; `order_id` breaks the tie between the two same-day orders.
- AVG over days ignores NULL (non-repeaters) in SQL and NaN in pandas; do not fill them with 0.
- A customer with orders on two dates but one cancelled is a single-order customer (customer 6).

**Then explain:**
- Part 6 Q20 and Part 8 Q21 are the model: first and second order per customer through `ROW_NUMBER` and conditional `MAX`.
- Filter before numbering; otherwise a cancelled order takes position 1 or 2.
- pandas: filter, sort, `groupby.cumcount()`, pick positions 1 and 2, subtract dates.
- Scoring note (Set E1, Q3 of 5, 20 pts): about 8 pts for 7 customers, 4 repeaters, 0.5714 and 17.5; 4 pts for the cancelled-first and same-day cases handled and the denominator named; 4 pts for pandas matching; 2 pts for stating the denominator out loud; 2 pts for a check (repeaters at most customers). Partial credit: right repeat share but days measured from the cancelled order.

**Follow-ups:**
- Repeat within 30 days only? Add `days <= 30` to the numerator; the denominator question gets sharper because young customers cannot have repeated yet (Part 6).
- Median days instead of average? SQLite has no median function; use a `ROW_NUMBER` or percentile in pandas (not run here).
- Repeat rate by acquisition month? Group the same table by the first-order month.

**Common mistakes:**
- Counting cancelled orders toward the order count.
- Dividing by all customers when the cancelled-only customer never really bought.
- Counting two same-day orders as one visit without saying so.
- Averaging days over non-repeaters as 0.

### Q30 ⭐⭐ 🟡 [Set E1, Q2 of 5, 8 min, 20 pts] GMV, AOV and cancelled share (Part 8 Q4). orders(order_id, customer_id, order_date, status, amount) with statuses DELIVERED, CANCELLED, RETURNED. Report per month GMV (all orders), net revenue (DELIVERED only), AOV on net orders and the cancelled share by count. Seed 10 orders over 2 months. SQL with conditional aggregation and pandas with named aggregations; say which denominator each metric uses.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Group by month with conditional aggregation: GMV is the sum over all orders, net revenue the sum over DELIVERED only, AOV is net revenue divided by delivered orders, and the cancelled share is cancelled orders divided by all orders.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2025-01-03','DELIVERED',100),(2,2,'2025-01-09','DELIVERED',200),
 (3,3,'2025-01-15','CANCELLED',150),(4,1,'2025-01-20','RETURNED',120),
 (5,4,'2025-01-28','DELIVERED',300),
 (6,2,'2025-02-02','DELIVERED',250),(7,5,'2025-02-06','CANCELLED',80),
 (8,6,'2025-02-11','CANCELLED',90),(9,3,'2025-02-19','DELIVERED',100),
 (10,1,'2025-02-25','RETURNED',60);
```

**SQL answer:** the `SQL` string in the Code block, shown here verbatim.
```sql
SELECT substr(order_date, 1, 7) AS month,
       COUNT(*) AS orders,
       SUM(amount) AS gmv,
       SUM(CASE WHEN status = 'DELIVERED' THEN amount ELSE 0 END) AS net_revenue,
       ROUND(1.0 * SUM(CASE WHEN status = 'DELIVERED' THEN amount END)
             / NULLIF(COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END), 0), 2) AS aov_net,
       ROUND(1.0 * COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) / COUNT(*), 4) AS cancelled_share
FROM orders
GROUP BY substr(order_date, 1, 7)
ORDER BY month
```

**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.
```py
d = o.assign(month=o["order_date"].str[:7],
             delivered=o["status"].eq("DELIVERED"),
             cancelled=o["status"].eq("CANCELLED"))
d["net_amount"] = d["amount"].where(d["delivered"], 0)
p = (d.groupby("month")
       .agg(orders=("order_id", "size"), gmv=("amount", "sum"),
            net_revenue=("net_amount", "sum"),
            n_delivered=("delivered", "sum"), n_cancelled=("cancelled", "sum"))
       .reset_index())
p["aov_net"] = (p["net_revenue"] / p["n_delivered"].where(p["n_delivered"] != 0)).round(2)
p["cancelled_share"] = (p["n_cancelled"] / p["orders"]).round(4)
p = p[["month", "orders", "gmv", "net_revenue", "aov_net", "cancelled_share"]]
```

**Example:** January: 5 orders, 100 + 200 + 150 + 120 + 300 = 870 GMV. Delivered amounts are 100, 200, 300 so net revenue 600 over 3 delivered orders, AOV 200.00. One of 5 orders was cancelled: 0.2. February: 5 orders and 250 + 80 + 90 + 100 + 60 = 580 GMV, delivered 250 and 100 give net 350 over 2 orders, AOV 175.00, 2 of 5 cancelled = 0.4. The RETURNED orders are inside GMV but outside net revenue.

**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).
```python
# Q30: GMV, net revenue, AOV and cancelled share per month.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2025-01-03','DELIVERED',100),(2,2,'2025-01-09','DELIVERED',200),
 (3,3,'2025-01-15','CANCELLED',150),(4,1,'2025-01-20','RETURNED',120),
 (5,4,'2025-01-28','DELIVERED',300),
 (6,2,'2025-02-02','DELIVERED',250),(7,5,'2025-02-06','CANCELLED',80),
 (8,6,'2025-02-11','CANCELLED',90),(9,3,'2025-02-19','DELIVERED',100),
 (10,1,'2025-02-25','RETURNED',60);
"""
SQL = """
SELECT substr(order_date, 1, 7) AS month,
       COUNT(*) AS orders,
       SUM(amount) AS gmv,
       SUM(CASE WHEN status = 'DELIVERED' THEN amount ELSE 0 END) AS net_revenue,
       ROUND(1.0 * SUM(CASE WHEN status = 'DELIVERED' THEN amount END)
             / NULLIF(COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END), 0), 2) AS aov_net,
       ROUND(1.0 * COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) / COUNT(*), 4) AS cancelled_share
FROM orders
GROUP BY substr(order_date, 1, 7)
ORDER BY month
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

o = pd.read_sql("SELECT * FROM orders", con)
# PANDAS START
d = o.assign(month=o["order_date"].str[:7],
             delivered=o["status"].eq("DELIVERED"),
             cancelled=o["status"].eq("CANCELLED"))
d["net_amount"] = d["amount"].where(d["delivered"], 0)
p = (d.groupby("month")
       .agg(orders=("order_id", "size"), gmv=("amount", "sum"),
            net_revenue=("net_amount", "sum"),
            n_delivered=("delivered", "sum"), n_cancelled=("cancelled", "sum"))
       .reset_index())
p["aov_net"] = (p["net_revenue"] / p["n_delivered"].where(p["n_delivered"] != 0)).round(2)
p["cancelled_share"] = (p["n_cancelled"] / p["orders"]).round(4)
p = p[["month", "orders", "gmv", "net_revenue", "aov_net", "cancelled_share"]]
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by month)")
print("AOV if you divide by ALL orders instead of delivered:",
      (p["net_revenue"] / p["orders"]).round(2).tolist())
```

**Output (my run):**
```text
  month  orders  gmv  net_revenue  aov_net  cancelled_share
2025-01       5  870          600    200.0              0.2
2025-02       5  580          350    175.0              0.4

  month  orders  gmv  net_revenue  aov_net  cancelled_share
2025-01       5  870          600    200.0              0.2
2025-02       5  580          350    175.0              0.4

asserts passed (ordered by month)
AOV if you divide by ALL orders instead of delivered: [120.0, 70.0]
```

**Edge cases:**
- Denominators differ by metric: GMV and the cancelled share use all orders (5 each month), AOV uses delivered orders (3 and 2). Dividing net revenue by all orders gives 120.00 and 70.00 instead, which is the common mistake (the run prints it).
- A month with no delivered orders: `NULLIF(..., 0)` makes AOV NULL (pandas masks the zero to NaN); it would be a 0 divided by 0 otherwise. Not in the seed.
- GMV definition varies by company (some exclude cancelled orders); here it is all orders as the question states, and RETURNED is kept in it.
- `SUM(CASE ... END)` with no ELSE is NULL when no row matches; I used `ELSE 0` for net revenue so it prints 0.
- Rounding: AOV is rounded to 2 decimals and the share to 4; the seed values are exact, so SQLite and pandas rounding agree.

**Then explain:**
- One scan with conditional aggregation (Part 8 Q4): `SUM(CASE WHEN status = ... THEN amount END)` and `COUNT(CASE WHEN ... THEN 1 END)`. PostgreSQL, SQLite 3.30 and later and others also have `FILTER (WHERE ...)` (I did not use it here; not executed).
- pandas named aggregation cannot take a condition, so add helper columns (`delivered`, `cancelled`, `net_amount`) first; booleans sum to counts.
- Say the denominator for each metric before coding, then the definitions are visible to the interviewer.
- Scoring note (Set E1, Q2 of 5, 20 pts): about 8 pts for the 2 correct rows (870, 600, 200.00, 0.2 and 580, 350, 175.00, 0.4); 4 pts for the right denominators and the NULL guard on AOV; 4 pts for pandas named aggregation matching; 2 pts for stating the GMV and net definitions; 2 pts for a check that GMV equals the sum of all amounts (1450). Partial credit: one scan with the right numerators but a single denominator for all metrics.

**Follow-ups:**
- AOV on all orders, or per customer? Different metrics; ask which the team uses.
- Return rate? RETURNED count over DELIVERED plus RETURNED, a definition to state first (Part 8).
- Month-over-month change in these metrics? Add a `LAG` over the monthly table as in Q21.

**Common mistakes:**
- Using `COUNT(*)` as the AOV denominator.
- Putting the status filter in `WHERE`, which also changes GMV and the cancelled share.
- Integer division for the share (the `1.0 *` avoids it).
- Silently excluding returned orders from GMV without saying so.
