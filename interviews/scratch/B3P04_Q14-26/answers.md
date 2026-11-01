### Q14 ⭐⭐⭐ 🟡 Percent of group total and difference from group average: orders(order_id, region, amount). For each order show its share of the region's total (amount / SUM(amount) OVER (PARTITION BY region)) as a percentage with one decimal, and its difference from the region's average amount. Explain the integer-division trap (multiply by 100.0), what happens when the group total is zero or NULL (NULLIF), why no ORDER BY is used in OVER here, and give the pandas transform('sum') and transform('mean') version.
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `amount / SUM(amount) OVER (PARTITION BY region)` gives each row's share of its region, but it must be written `100.0 * amount / ...` or integer division returns 0, and the denominator needs `NULLIF(..., 0)` so a zero total gives NULL instead of a divide-by-zero.

**Schema and sample data:** nine orders. Region N is clean (total 1000), S has a NULL amount, Z totals zero, E has only a NULL amount.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'N',100),(2,'N',300),(3,'N',600),
  (4,'S',50),(5,'S',150),(6,'S',NULL),
  (7,'Z',0),(8,'Z',0),(9,'E',NULL);
```

**SQL answer:** `SQL_MAIN` (Code block). The other two queries (`SQL_INT`, `SQL_ORDERED`) are the traps, run next to it.
```sql
SELECT order_id, region, amount,
       ROUND(100.0 * amount / NULLIF(SUM(amount) OVER (PARTITION BY region), 0), 1) AS pct_of_region,
       ROUND(amount - AVG(amount) OVER (PARTITION BY region), 2) AS diff_from_avg
FROM orders
ORDER BY order_id
```

**pandas answer:** `transform` returns one value per original row, so the share is a plain column expression.
```python
total = orders.groupby("region")["amount"].transform("sum")
avg = orders.groupby("region")["amount"].transform("mean")
pd_df = orders.assign(
    pct_of_region=(100.0 * orders["amount"] / total.replace(0, np.nan)).round(1),
    diff_from_avg=(orders["amount"] - avg).round(2),
)
```

**Example:**
- Region N: total 100 + 300 + 600 = 1000, average 333.33. Order 1: 100 / 1000 = 10.0 percent, difference 100 - 333.33 = -233.33. Order 2: 30.0 percent, -33.33. Order 3: 60.0 percent, +266.67.
- Region S: `SUM` and `AVG` skip the NULL, so total 200 and average 100. Order 4: 25.0 percent and -50; order 5: 75.0 percent and +50. Order 6 has a NULL amount, so both its numbers are NULL.
- Region Z: total 0, so `NULLIF(0, 0)` is NULL and the share is NULL. The average is 0, so the difference is 0.
- Region E: only a NULL amount, so the total is NULL and everything is NULL.
- No `ORDER BY` inside `OVER`, so the window is the whole region for every row. This is what makes the total a total.

**Code:** run with `python3 -I`.
```python
# Q14: percent of group total and difference from group average
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'N',100),(2,'N',300),(3,'N',600),
  (4,'S',50),(5,'S',150),(6,'S',NULL),
  (7,'Z',0),(8,'Z',0),(9,'E',NULL);
"""
SQL_MAIN = """
SELECT order_id, region, amount,
       ROUND(100.0 * amount / NULLIF(SUM(amount) OVER (PARTITION BY region), 0), 1) AS pct_of_region,
       ROUND(amount - AVG(amount) OVER (PARTITION BY region), 2) AS diff_from_avg
FROM orders
ORDER BY order_id
"""
SQL_INT = """
SELECT order_id, amount / SUM(amount) OVER (PARTITION BY region) * 100 AS int_pct,
       100.0 * amount / SUM(amount) OVER (PARTITION BY region) AS float_pct
FROM orders WHERE region IN ('N', 'Z')
ORDER BY order_id
"""
SQL_ORDERED = """
SELECT order_id, amount, SUM(amount) OVER (PARTITION BY region ORDER BY order_id) AS sum_with_order_by
FROM orders WHERE region = 'N'
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main:"); print(sql_df.to_string(index=False))
print("\nInteger-division trap and zero total (regions N and Z):")
print(pd.read_sql_query(SQL_INT, con).to_string(index=False))
print("\nOrdered window by mistake (region N):")
print(pd.read_sql_query(SQL_ORDERED, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
total = orders.groupby("region")["amount"].transform("sum")
avg = orders.groupby("region")["amount"].transform("mean")
pd_df = orders.assign(
    pct_of_region=(100.0 * orders["amount"] / total.replace(0, np.nan)).round(1),
    diff_from_avg=(orders["amount"] - avg).round(2),
)
# pd:end
print("\npandas transform('sum') per row:", total.tolist())
print(pd_df.to_string(index=False))
# compared after sorting both by order_id
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("order_id").reset_index(drop=True), check_dtype=False)

# surprise: pandas sum of an all-NaN group is 0.0 (SQL SUM is NULL); region E amount is NULL either way
print("\nall-NULL region E: pandas sum =", total[orders["region"] == "E"].tolist(),
      "| SQL SUM =", con.execute("SELECT SUM(amount) FROM orders WHERE region='E'").fetchone())
# division by zero in SQLite is NULL, not an error
print("SQLite 1/0 =", con.execute("SELECT 1.0/0").fetchone())
print("asserts passed: SQL == pandas")
```

**Output (my run):**
```text
SQL main:
 order_id region  amount  pct_of_region  diff_from_avg
        1      N   100.0           10.0        -233.33
        2      N   300.0           30.0         -33.33
        3      N   600.0           60.0         266.67
        4      S    50.0           25.0         -50.00
        5      S   150.0           75.0          50.00
        6      S     NaN            NaN            NaN
        7      Z     0.0            NaN           0.00
        8      Z     0.0            NaN           0.00
        9      E     NaN            NaN            NaN

Integer-division trap and zero total (regions N and Z):
 order_id  int_pct  float_pct
        1      0.0       10.0
        2      0.0       30.0
        3      0.0       60.0
        7      NaN        NaN
        8      NaN        NaN

Ordered window by mistake (region N):
 order_id  amount  sum_with_order_by
        1     100                100
        2     300                400
        3     600               1000

pandas transform('sum') per row: [1000.0, 1000.0, 1000.0, 200.0, 200.0, 200.0, 0.0, 0.0, 0.0]
 order_id region  amount  pct_of_region  diff_from_avg
        1      N   100.0           10.0        -233.33
        2      N   300.0           30.0         -33.33
        3      N   600.0           60.0         266.67
        4      S    50.0           25.0         -50.00
        5      S   150.0           75.0          50.00
        6      S     NaN            NaN            NaN
        7      Z     0.0            NaN           0.00
        8      Z     0.0            NaN           0.00
        9      E     NaN            NaN            NaN

all-NULL region E: pandas sum = [0.0] | SQL SUM = (None,)
SQLite 1/0 = (None,)
asserts passed: SQL == pandas
```

**Edge cases:**
- Zero total: SQLite returns NULL for a divide by zero (the run shows `1.0/0` is NULL), so without `NULLIF` it would also come out NULL here. PostgreSQL raises a division-by-zero error (from memory, not executed here), so `NULLIF` is the portable habit.
- NULL amount: skipped by `SUM` and `AVG`, and the row's own share is NULL. NULL is not 0: decide whether the business wants NULLs treated as zero (`COALESCE(amount, 0)`) before ranking or averaging, because that changes the average.
- All-NULL region: SQL `SUM` is NULL, but pandas `sum` of an all-NaN group is 0.0 (surprise in the run: the pandas total for region E is 0.0). My `replace(0, np.nan)` turns it into NaN, so the result still matches, but only because of that line.
- Percentages of a region should add to 100 only if no rounding and no NULLs; rounded shares can add to 99.9 or 100.1.

**Then explain:**
- **Integer division:** `amount / total` with two integers is integer division in SQLite (and in PostgreSQL, from memory), so 100 / 1000 is 0. Multiplying by `100.0` first makes it a float. The run shows `int_pct` all zero and `float_pct` correct.
- **No ORDER BY in OVER:** with `PARTITION BY` only, the frame is the whole partition. Adding `ORDER BY` changes the default frame to "start to current row (with peers)", so `SUM` becomes a running sum. The run shows region N becoming 100, 400, 1000. That is the classic wrong-total bug.
- **Window versus GROUP BY plus join:** the window keeps every row and attaches the group statistic, with no self-join.
- **pandas:** `groupby().transform("sum")` is the same idea; plain `groupby().sum()` has one row per group and would not line up.

**Follow-ups:**
- *Show the share of the grand total instead?* `SUM(amount) OVER ()`, an empty window, and in pandas `amount / amount.sum()`.
- *Why round in the query?* Presentation only; keep the raw ratio if more arithmetic follows.
- *Where does the window run?* After `WHERE` and `GROUP BY`, so filtered-out rows are not in the total.

**Common mistakes:**
- `amount / SUM(...) * 100` with integers.
- Adding `ORDER BY` inside `OVER` out of habit.
- Forgetting `NULLIF`, then being surprised by a crash on another engine.
- In pandas, using `groupby().sum()` and assigning it to a column (index mismatch) instead of `transform`.

### Q15 ⭐⭐⭐ 🟡 Top product per category per month: sales(sale_id, product_id, category, sale_date, amount) with ISO dates. Return the best-selling product (by total amount) in each category and month using a CTE that aggregates by category, month (strftime('%Y-%m')) and product, then ROW_NUMBER or RANK partitioned by category and month. Explain aggregate-before-rank, the tie rule you choose (product_id as tie-break), the month-must-keep-the-year trap, and give the pandas groupby sum then sort_values and drop_duplicates or idxmax version.
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Aggregate first (one row per category, month, product), then rank those totals inside each (category, month) and keep rank 1; the month must be `'%Y-%m'` so January 2024 and January 2025 stay apart, and the tie rule is "higher total, then lower product_id".

**Schema and sample data:** twelve sales over Books and Toys, in January and February 2024 and January 2025. Books January 2024 is a tie on purpose.
```sql
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, category TEXT, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,1,'Books','2024-01-05',30),(2,1,'Books','2024-01-20',20),(3,2,'Books','2024-01-11',50),
 (4,3,'Books','2024-02-02',10),(5,2,'Books','2024-02-15',15),
 (6,2,'Books','2025-01-09',40),(7,1,'Books','2025-01-10',25),
 (8,4,'Toys','2024-01-03',90),(9,5,'Toys','2024-01-04',60),(10,5,'Toys','2024-01-25',40),
 (11,4,'Toys','2025-01-02',10),(12,6,'Toys','2025-01-30',70);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_RANK` (keeps ties) and `SQL_WRONG` (month without year) are run next to it.
```sql
WITH monthly AS (
  SELECT category, strftime('%Y-%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%Y-%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         ROW_NUMBER() OVER (PARTITION BY category, month ORDER BY total DESC, product_id) AS rn
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rn = 1
ORDER BY category, month
```

**pandas answer:** group and sum, sort so the winner of each group comes first (total descending, product_id ascending), then keep the first row per group.
```python
monthly = (sales.assign(month=pd.to_datetime(sales["sale_date"]).dt.strftime("%Y-%m"))
           .groupby(["category", "month", "product_id"], as_index=False)
           .agg(total=("amount", "sum")))
pd_df = (monthly.sort_values(["category", "month", "total", "product_id"],
                             ascending=[True, True, False, True])
         .drop_duplicates(["category", "month"])
         .reset_index(drop=True))
```

**Example:**
- Books, 2024-01: product 1 has 30 + 20 = 50, product 2 has 50. A tie. `ORDER BY total DESC, product_id` puts product 1 first, so product 1 wins. `RANK` would return both.
- Books, 2024-02: product 3 has 10, product 2 has 15, so product 2 wins.
- Books, 2025-01: product 2 has 40, product 1 has 25, so product 2 wins.
- Toys, 2024-01: product 4 has 90, product 5 has 60 + 40 = 100, so product 5 wins. Note a single sale of 90 would have looked best if I ranked rows instead of totals.
- Toys, 2025-01: product 6 has 70, product 4 has 10, so product 6 wins.
- Result: five rows, one per (category, month).

**Code:** run with `python3 -I`.
```python
# Q15: top product per category per month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, category TEXT, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,1,'Books','2024-01-05',30),(2,1,'Books','2024-01-20',20),(3,2,'Books','2024-01-11',50),
 (4,3,'Books','2024-02-02',10),(5,2,'Books','2024-02-15',15),
 (6,2,'Books','2025-01-09',40),(7,1,'Books','2025-01-10',25),
 (8,4,'Toys','2024-01-03',90),(9,5,'Toys','2024-01-04',60),(10,5,'Toys','2024-01-25',40),
 (11,4,'Toys','2025-01-02',10),(12,6,'Toys','2025-01-30',70);
"""
SQL_MAIN = """
WITH monthly AS (
  SELECT category, strftime('%Y-%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%Y-%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         ROW_NUMBER() OVER (PARTITION BY category, month ORDER BY total DESC, product_id) AS rn
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rn = 1
ORDER BY category, month
"""
SQL_RANK = """
WITH monthly AS (
  SELECT category, strftime('%Y-%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%Y-%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         RANK() OVER (PARTITION BY category, month ORDER BY total DESC) AS rk
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rk = 1
ORDER BY category, month, product_id
"""
SQL_WRONG = """
WITH monthly AS (
  SELECT category, strftime('%m', sale_date) AS month, product_id, SUM(amount) AS total
  FROM sales
  GROUP BY category, strftime('%m', sale_date), product_id
), ranked AS (
  SELECT category, month, product_id, total,
         ROW_NUMBER() OVER (PARTITION BY category, month ORDER BY total DESC, product_id) AS rn
  FROM monthly
)
SELECT category, month, product_id, total
FROM ranked
WHERE rn = 1
ORDER BY category, month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL ROW_NUMBER (tie-break product_id):"); print(sql_df.to_string(index=False))
print("\nSQL RANK (keeps ties):"); print(pd.read_sql_query(SQL_RANK, con).to_string(index=False))
print("\nSQL wrong: month without the year:"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
monthly = (sales.assign(month=pd.to_datetime(sales["sale_date"]).dt.strftime("%Y-%m"))
           .groupby(["category", "month", "product_id"], as_index=False)
           .agg(total=("amount", "sum")))
pd_df = (monthly.sort_values(["category", "month", "total", "product_id"],
                             ascending=[True, True, False, True])
         .drop_duplicates(["category", "month"])
         .reset_index(drop=True))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in order category, month (both already sorted that way)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

# idxmax variant: first row with the max in frame order, so sort first to make it deterministic
im = monthly.sort_values(["category", "month", "product_id"]).reset_index(drop=True)
im = im.loc[im.groupby(["category", "month"])["total"].idxmax()].reset_index(drop=True)
pd.testing.assert_frame_equal(sql_df, im, check_dtype=False)
print("\nidxmax after sorting by product_id gives the same rows (first max wins)")
print("asserts passed: SQL == pandas (drop_duplicates) == pandas (idxmax)")
```

**Output (my run):**
```text
SQL ROW_NUMBER (tie-break product_id):
category   month  product_id  total
   Books 2024-01           1     50
   Books 2024-02           2     15
   Books 2025-01           2     40
    Toys 2024-01           5    100
    Toys 2025-01           6     70

SQL RANK (keeps ties):
category   month  product_id  total
   Books 2024-01           1     50
   Books 2024-01           2     50
   Books 2024-02           2     15
   Books 2025-01           2     40
    Toys 2024-01           5    100
    Toys 2025-01           6     70

SQL wrong: month without the year:
category month  product_id  total
   Books    01           2     90
   Books    02           2     15
    Toys    01           4    100

pandas:
category   month  product_id  total
   Books 2024-01           1     50
   Books 2024-02           2     15
   Books 2025-01           2     40
    Toys 2024-01           5    100
    Toys 2025-01           6     70

idxmax after sorting by product_id gives the same rows (first max wins)
asserts passed: SQL == pandas (drop_duplicates) == pandas (idxmax)
```

**Edge cases:**
- Ties: with `ROW_NUMBER` exactly one winner per group, chosen by `product_id`. With `RANK`, both tied products come back (the run shows two rows for Books 2024-01).
- The month trap: with `strftime('%m')` the January rows of 2024 and 2025 merge. In the run Books January becomes one group (product 2: 50 + 40 = 90 against product 1: 75) and the two real Januaries disappear, as do Toys' two Januaries.
- Category-months with no sales produce no row (they are not in the data to group).
- NULL amounts are skipped by `SUM`; a product with only NULL amounts gets a NULL total, and in `ORDER BY total DESC` SQLite sorts NULL last (so it only wins if it is the only product).

**Then explain:**
- **Aggregate before rank:** the question is "best-selling product", which is about product totals, not single sales rows. Ranking rows first would rank individual sales.
- **Tie rule I choose:** total descending, then product_id ascending; I say it out loud so the answer is reproducible.
- **ROW_NUMBER versus RANK here:** `ROW_NUMBER` for "exactly one product per month"; `RANK` if the business wants all tied winners.
- **pandas:** `sort_values` then `drop_duplicates(subset=[...])` keeps the first row per group, so the sort decides the winner. The `idxmax` version works too, but it returns the first row with the maximum in the frame's current order, so I sort by product_id first to make it deterministic (the run asserts it matches).
- **ISO dates** sort and `strftime` correctly as text in SQLite; in pandas I convert with `to_datetime` before formatting.

**Follow-ups:**
- *Top 3 products per month?* Change `rn = 1` to `rn <= 3` (Q26 covers the tie variants).
- *Why not `GROUP BY` with `MAX(total)`?* It gives the maximum but not which product earned it; joining back would return ties.
- *Share of the month's category sales won by the top product?* Add `SUM(total) OVER (PARTITION BY category, month)` in the ranked CTE.

**Common mistakes:**
- Month name or number without the year.
- Ranking raw sales instead of per-product totals.
- No tie-break, so the winner can change between runs or engines.
- Using `idxmax` on an unsorted frame and assuming it is deterministic.

### Q16 ⭐⭐⭐ 🟡 The Nth transaction per user: transactions(txn_id, user_id, txn_time, amount). Return each user's second transaction (and say how to get the first and the last). Use ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) = 2, and the reversed ORDER BY for the last. Explain users with fewer than two transactions (no row), why the tie-breaker matters when two transactions share a timestamp, and give the pandas groupby().cumcount() + 1 version (cumcount starts at 0).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Number each user's transactions with `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id)` in a subquery and keep `rn = 2`; the first is `rn = 1`, the last is the same numbering with the order reversed, and `txn_id` in the order makes ties on the timestamp deterministic.

**Schema and sample data:** seven transactions. User 2's first two share a timestamp; user 3 has one transaction.
```sql
CREATE TABLE transactions(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_time TEXT, amount INTEGER);
INSERT INTO transactions VALUES
 (1,1,'2024-01-01 09:00',10),(2,1,'2024-01-02 10:00',20),(3,1,'2024-01-03 11:00',30),
 (4,2,'2024-02-01 08:00',5),(5,2,'2024-02-01 08:00',7),(6,2,'2024-02-05 09:00',9),
 (7,3,'2024-03-01 12:00',40);
```

**SQL answer:** `SQL_MAIN` for the second transaction, `SQL_FIRST_LAST` for first and last (Code block).
```sql
SELECT txn_id, user_id, txn_time, amount
FROM (SELECT t.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn
      FROM transactions t)
WHERE rn = 2
ORDER BY user_id
```
```sql
SELECT user_id,
       MAX(CASE WHEN rn_first = 1 THEN txn_id END) AS first_txn,
       MAX(CASE WHEN rn_last = 1 THEN txn_id END) AS last_txn
FROM (SELECT user_id, txn_id,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn_first,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time DESC, txn_id DESC) AS rn_last
      FROM transactions)
GROUP BY user_id
ORDER BY user_id
```

**pandas answer:** sort by user, time and id, number with `cumcount` (starts at 0, so add 1), filter.
```python
s = txn.sort_values(["user_id", "txn_time", "txn_id"]).reset_index(drop=True)
s["n"] = s.groupby("user_id").cumcount() + 1
pd_df = s[s["n"] == 2].drop(columns="n").reset_index(drop=True)
```

**Example:**
- User 1: 09:00, 10:00, 11:00 are numbered 1, 2, 3. Second is txn 2.
- User 2: txn 4 and txn 5 have the same time. `ORDER BY txn_time, txn_id` puts 4 first and 5 second, so the second transaction is txn 5. Txn 6 is third.
- User 3: only rn = 1 exists, so no row comes back.
- First: txns 1, 4, 7. Last (reversed order): txns 3, 6, 7. User 3's first and last are the same row.

**Code:** run with `python3 -I`.
```python
# Q16: Nth transaction per user
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE transactions(txn_id INTEGER PRIMARY KEY, user_id INTEGER, txn_time TEXT, amount INTEGER);
INSERT INTO transactions VALUES
 (1,1,'2024-01-01 09:00',10),(2,1,'2024-01-02 10:00',20),(3,1,'2024-01-03 11:00',30),
 (4,2,'2024-02-01 08:00',5),(5,2,'2024-02-01 08:00',7),(6,2,'2024-02-05 09:00',9),
 (7,3,'2024-03-01 12:00',40);
"""
SQL_MAIN = """
SELECT txn_id, user_id, txn_time, amount
FROM (SELECT t.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn
      FROM transactions t)
WHERE rn = 2
ORDER BY user_id
"""
SQL_FIRST_LAST = """
SELECT user_id,
       MAX(CASE WHEN rn_first = 1 THEN txn_id END) AS first_txn,
       MAX(CASE WHEN rn_last = 1 THEN txn_id END) AS last_txn
FROM (SELECT user_id, txn_id,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time, txn_id) AS rn_first,
             ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time DESC, txn_id DESC) AS rn_last
      FROM transactions)
GROUP BY user_id
ORDER BY user_id
"""
SQL_NO_TIEBREAK = """
SELECT txn_id, user_id
FROM (SELECT t.*, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY txn_time) AS rn
      FROM transactions t)
WHERE rn = 2 AND user_id = 2
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL second transaction per user:"); print(sql_df.to_string(index=False))
sql_fl = pd.read_sql_query(SQL_FIRST_LAST, con)
print("\nSQL first and last txn_id per user:"); print(sql_fl.to_string(index=False))
print("\nWithout txn_id tie-break, user 2 second txn_id (unspecified order, only this run):",
      con.execute(SQL_NO_TIEBREAK).fetchall())

txn = pd.read_sql_query("SELECT * FROM transactions", con)
# pd:main
s = txn.sort_values(["user_id", "txn_time", "txn_id"]).reset_index(drop=True)
s["n"] = s.groupby("user_id").cumcount() + 1
pd_df = s[s["n"] == 2].drop(columns="n").reset_index(drop=True)
# pd:end
print("\ncumcount before +1 (starts at 0):", txn.sort_values(["user_id", "txn_time", "txn_id"]).groupby("user_id").cumcount().tolist())
print("pandas second transaction per user:"); print(pd_df.to_string(index=False))
# compared in user_id order
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("user_id").reset_index(drop=True), check_dtype=False)

first = s.groupby("user_id").head(1)["txn_id"].tolist()
last = s.groupby("user_id").tail(1)["txn_id"].tolist()
last2 = s[s.groupby("user_id").cumcount(ascending=False) == 0]["txn_id"].tolist()
assert first == sql_fl["first_txn"].tolist() and last == sql_fl["last_txn"].tolist() == last2
print("first:", first, "last:", last, "(same as SQL)")
assert sql_df["user_id"].tolist() == [1, 2] and 3 not in sql_df["user_id"].tolist()
print("asserts passed: SQL == pandas; user 3 (one transaction) has no second row")
```

**Output (my run):**
```text
SQL second transaction per user:
 txn_id  user_id         txn_time  amount
      2        1 2024-01-02 10:00      20
      5        2 2024-02-01 08:00       7

SQL first and last txn_id per user:
 user_id  first_txn  last_txn
       1          1         3
       2          4         6
       3          7         7

Without txn_id tie-break, user 2 second txn_id (unspecified order, only this run): [(5, 2)]

cumcount before +1 (starts at 0): [0, 1, 2, 0, 1, 2, 0]
pandas second transaction per user:
 txn_id  user_id         txn_time  amount
      2        1 2024-01-02 10:00      20
      5        2 2024-02-01 08:00       7
first: [1, 4, 7] last: [3, 6, 7] (same as SQL)
asserts passed: SQL == pandas; user 3 (one transaction) has no second row
```

**Edge cases:**
- Fewer than two transactions: no row (user 3). To list the user anyway with NULL, join the users table with `LEFT JOIN` to the filtered result.
- Timestamp ties: without `txn_id` the second transaction of user 2 is whichever tied row the engine happens to put second. The run shows what SQLite did here, but that is not a guarantee, and it can change with an index or another engine.
- Duplicates: if two rows are identical in every column including `txn_id` (no primary key), `ROW_NUMBER` still numbers them, so one of them is called "second". Dedupe first if that is not wanted.
- NULL `txn_time`: SQLite sorts NULL first in ascending order, so a NULL-time row would count as the user's first. Other engines default differently (not executed here); filter or use an explicit `NULLS LAST` (works on SQLite 3.45) when it matters.

**Then explain:**
- **Why a subquery:** window functions cannot appear in `WHERE`, so number in an inner query and filter outside.
- **Last transaction:** either reverse both sort keys (`txn_time DESC, txn_id DESC`) and take `rn = 1`, or compute `COUNT(*) OVER (PARTITION BY user_id)` and compare. Reversing is simpler.
- **Why `ROW_NUMBER`, not `RANK`:** `RANK` can give two rows rank 2 on ties, and "the second transaction" must be exactly one row.
- **pandas:** `cumcount()` is zero-based (the run prints 0, 1, 2 for user 1), so `+ 1` matches `ROW_NUMBER`. `head(1)`/`tail(1)` give first and last; `cumcount(ascending=False) == 0` also gives last, and the run asserts they agree.

**Follow-ups:**
- *Second transaction's gap from the first?* That needs `LAG` or `LEAD` (Part 5).
- *Nth for a parameter N?* Pass N as a Python sqlite3 parameter in `rn = ?`.
- *Why not `LIMIT 1 OFFSET 1`?* It works on the whole table, not per user.

**Common mistakes:**
- No tie-breaker on `txn_time`.
- Off-by-one with `cumcount` (zero-based).
- Using `RANK`, which can return two "second" rows.
- Expecting a row for users with one transaction.

### Q17 ⭐⭐⭐ 🟡 Employees whose salary is their department's top: employees(emp_id, name, dept_id, salary). Return them with MAX(salary) OVER (PARTITION BY dept_id) compared in an outer query, and again with RANK() = 1, and show the two give the same rows including ties. Explain which one reads better, what happens when salary is NULL (a NULL max if all NULL, NULL rows never equal the max), and give the pandas transform('max') mask and the idxmax contrast (idxmax returns only the first tied row).
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Both `salary = MAX(salary) OVER (PARTITION BY dept_id)` and `RANK() = 1` return every employee tied for the top, but they only agree if NULL salaries are filtered for the RANK version; I find the `MAX` comparison clearer, and in pandas it is a `transform("max")` mask, not `idxmax`.

**Schema and sample data:** eight employees. Department 10 has a tie at 70, department 20 has a NULL salary, department 30 has only a NULL salary, department 40 has one employee.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Gita',20,NULL),
  (7,'Farid',30,NULL),(8,'Hari',40,55);
```

**SQL answer:** `SQL_MAIN` (MAX version), `SQL_RANK` (RANK version) and `SQL_RANK_SAFE` (RANK with NULLs filtered) in the Code block.
```sql
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, MAX(salary) OVER (PARTITION BY dept_id) AS dept_max FROM employees e)
WHERE salary = dept_max
ORDER BY emp_id
```
```sql
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk FROM employees e)
WHERE rk = 1
ORDER BY emp_id
```
```sql
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
      FROM employees e WHERE salary IS NOT NULL)
WHERE rk = 1
ORDER BY emp_id
```

**pandas answer:** one value per row (the department maximum), then compare.
```python
dept_max = emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[emp["salary"] == dept_max]
```

**Example:**
- Dept 10: max is 70; Asha and Ben both equal it, so both are returned (tie kept). Chitra (60) is not.
- Dept 20: `MAX` skips the NULL, giving 90; Dev is returned. Esha (40) no. Gita's NULL is not equal to 90.
- Dept 30: Farid's salary is NULL, so the max is NULL, and `NULL = NULL` is unknown, so `MAX` returns no one.
- Dept 40: Hari is alone, so he is the max and is returned.
- `MAX` result: Asha, Ben, Dev, Hari.
- Plain `RANK() ... ORDER BY salary DESC` in SQLite puts NULL last, so dept 20 is fine, but in dept 30 the only row (the NULL) gets rank 1, and Farid also appears. That is the one place the two differ; adding `WHERE salary IS NOT NULL` removes him.

**Code:** run with `python3 -I`.
```python
# Q17: employees whose salary is the department's top (MAX OVER vs RANK = 1)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,70),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Gita',20,NULL),
  (7,'Farid',30,NULL),(8,'Hari',40,55);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, MAX(salary) OVER (PARTITION BY dept_id) AS dept_max FROM employees e)
WHERE salary = dept_max
ORDER BY emp_id
"""
SQL_RANK = """
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk FROM employees e)
WHERE rk = 1
ORDER BY emp_id
"""
SQL_RANK_SAFE = """
SELECT emp_id, name, dept_id, salary
FROM (SELECT e.*, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
      FROM employees e WHERE salary IS NOT NULL)
WHERE rk = 1
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_rank = pd.read_sql_query(SQL_RANK, con)
sql_safe = pd.read_sql_query(SQL_RANK_SAFE, con)
print("MAX() OVER:"); print(sql_main.to_string(index=False))
print("\nRANK() = 1 (no NULL filter):"); print(sql_rank.to_string(index=False))
print("\nRANK() = 1 with salary IS NOT NULL:"); print(sql_safe.to_string(index=False))
print("\nMAX == safe RANK:", sql_main.equals(sql_safe), "| MAX == plain RANK:", sql_main.equals(sql_rank))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
dept_max = emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[emp["salary"] == dept_max]
# pd:end
print("\npandas transform('max') mask:"); print(pd_df.to_string(index=False))
# compared after sorting by emp_id
pd.testing.assert_frame_equal(sql_main, pd_df.sort_values("emp_id").reset_index(drop=True), check_dtype=False)
assert sql_main.equals(sql_safe)

rk = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False)
print("\npandas rank(method='min', ascending=False) == 1:", emp.loc[rk == 1, "name"].tolist(), "(NaN rank is NaN, so Farid is out)")
try:
    emp.groupby("dept_id")["salary"].idxmax()
except ValueError as e:
    print("idxmax with an all-NaN group raises ValueError:", e)
ok = emp.dropna(subset=["salary"])
print("idxmax on non-null rows returns only first tied row:", emp.loc[ok.groupby("dept_id")["salary"].idxmax(), "name"].tolist())
print("asserts passed: MAX OVER == RANK (NULLs filtered) == pandas mask")
```

**Output (my run):**
```text
MAX() OVER:
 emp_id name  dept_id  salary
      1 Asha       10      70
      2  Ben       10      70
      4  Dev       20      90
      8 Hari       40      55

RANK() = 1 (no NULL filter):
 emp_id  name  dept_id  salary
      1  Asha       10    70.0
      2   Ben       10    70.0
      4   Dev       20    90.0
      7 Farid       30     NaN
      8  Hari       40    55.0

RANK() = 1 with salary IS NOT NULL:
 emp_id name  dept_id  salary
      1 Asha       10      70
      2  Ben       10      70
      4  Dev       20      90
      8 Hari       40      55

MAX == safe RANK: True | MAX == plain RANK: False

pandas transform('max') mask:
 emp_id name  dept_id  salary
      1 Asha       10    70.0
      2  Ben       10    70.0
      4  Dev       20    90.0
      8 Hari       40    55.0

pandas rank(method='min', ascending=False) == 1: ['Asha', 'Ben', 'Dev', 'Hari'] (NaN rank is NaN, so Farid is out)
idxmax with an all-NaN group raises ValueError: idxmax with skipna=True encountered all NA values in a group.
idxmax on non-null rows returns only first tied row: ['Asha', 'Dev', 'Hari']
asserts passed: MAX OVER == RANK (NULLs filtered) == pandas mask
```

**Edge cases:**
- All-NULL department: `MAX` version returns nobody; plain `RANK` returns the NULL row. So the premise "they give the same rows" holds for ties but not for an all-NULL group unless you filter.
- NULL among real values: `MAX` ignores it. For `RANK`, where NULL sorts depends on the engine: SQLite treats NULL as smallest, so it is last under `DESC`. PostgreSQL treats NULL as largest by default, so a NULL could rank first under `DESC` (from memory, not executed here); `ORDER BY salary DESC NULLS LAST` makes it explicit and ran on SQLite 3.45 in my probe.
- Ties: both keep every tied row.
- One-employee department: returned by both.

**Then explain:**
- **Which reads better:** `MAX` says exactly what is meant ("equals the department maximum") and has no ranking concept to explain. `RANK` generalises to "top 3" (Q26). I choose by whether the question might become top N.
- **Cost:** both compute one window pass per partition; I did not time them.
- **pandas:** `transform("max")` gives the department maximum per row, so `==` keeps ties. NaN never equals NaN in pandas either, so the all-NaN department is excluded, matching the `MAX` version.
- **idxmax contrast:** `idxmax` returns one row label per group, the first row holding the maximum, so a tie loses a row (the run returns Asha but not Ben). On pandas 3.0.5 it also raises a `ValueError` when a group is all NaN (shown in the run), so drop the NaN rows first.

**Follow-ups:**
- *Show the employee next to the max?* Keep `dept_max` in the select list.
- *Exactly one per department?* `ROW_NUMBER` with a tie-break (Q4, Q20).
- *`QUALIFY`?* Some engines let you filter on a window directly (Snowflake, BigQuery, Teradata, from memory, not executed here); SQLite does not.

**Common mistakes:**
- Using `idxmax` and silently losing tied employees.
- Not filtering NULL salaries in the `RANK` version.
- Writing `WHERE salary = MAX(salary) OVER (...)` in the same query (windows are not allowed in `WHERE`).
- Using `groupby().max()` and merging back without thinking about NULL keys.

### Q18 ⭐⭐⭐ 🟡 Rank users by activity: events(event_id, user_id, event_time). Rank users by number of events (most active first), show ties sharing a rank with RANK and consecutive ranks with DENSE_RANK, and return the top 5 including ties. Explain count-then-rank structure, adding a tie-breaker when you need exactly five, and give the pandas value_counts or groupby size then rank(method='min', ascending=False) version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Count events per user in a CTE, then rank the counts: `RANK()` gives tied users the same number and skips (1, 2, 2, 4), `DENSE_RANK()` does not skip (1, 2, 2, 3), and "top 5 including ties" is `RANK() <= 5` in an outer query; for exactly five rows add a unique tie-breaker and use `ROW_NUMBER`.

**Schema and sample data:** 21 events for seven users, with counts 5, 4, 4, 3, 2, 2, 1.
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
INSERT INTO events VALUES
 (1,1,'2024-01-01'),(2,1,'2024-01-02'),(3,1,'2024-01-03'),(4,1,'2024-01-04'),(5,1,'2024-01-05'),
 (6,2,'2024-01-01'),(7,2,'2024-01-02'),(8,2,'2024-01-03'),(9,2,'2024-01-04'),
 (10,3,'2024-01-01'),(11,3,'2024-01-02'),(12,3,'2024-01-03'),(13,3,'2024-01-04'),
 (14,4,'2024-01-01'),(15,4,'2024-01-02'),(16,4,'2024-01-03'),
 (17,5,'2024-01-01'),(18,5,'2024-01-02'),
 (19,6,'2024-01-01'),(20,6,'2024-01-02'),
 (21,7,'2024-01-01');
```

**SQL answer:** `SQL_MAIN` shows all three rankings; `SQL_TOP5` and `SQL_EXACT5` are the two answers (Code block).
```sql
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events,
         RANK() OVER (ORDER BY n_events DESC) AS rnk,
         DENSE_RANK() OVER (ORDER BY n_events DESC) AS dense_rnk,
         ROW_NUMBER() OVER (ORDER BY n_events DESC, user_id) AS rn
  FROM counts
)
SELECT user_id, n_events, rnk, dense_rnk, rn
FROM ranked
ORDER BY rn
```
```sql
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events, RANK() OVER (ORDER BY n_events DESC) AS rnk
  FROM counts
)
SELECT user_id, n_events, rnk FROM ranked WHERE rnk <= 5 ORDER BY rnk, user_id
```

**pandas answer:** count with `groupby().size()`, rank the counts with `method="min"` (same as `RANK`) and `"dense"` (same as `DENSE_RANK`), filter.
```python
counts = ev.groupby("user_id").size().rename("n_events").reset_index()
counts["rnk"] = counts["n_events"].rank(method="min", ascending=False).astype(int)
counts["dense_rnk"] = counts["n_events"].rank(method="dense", ascending=False).astype(int)
pd_all = counts.sort_values(["n_events", "user_id"], ascending=[False, True]).reset_index(drop=True)
pd_all["rn"] = pd_all.index + 1
pd_top5 = pd_all.loc[pd_all["rnk"] <= 5, ["user_id", "n_events", "rnk"]].reset_index(drop=True)
pd_exact = pd_all.head(5)[["user_id", "n_events", "rn"]]
```

**Example:**
- Counts: user 1 has 5, users 2 and 3 have 4, user 4 has 3, users 5 and 6 have 2, user 7 has 1.
- `RANK`: 1, 2, 2, 4, 5, 5, 7. Users 2 and 3 share 2, the next is 4 (gap). Users 5 and 6 share 5.
- `DENSE_RANK`: 1, 2, 2, 3, 4, 4, 5. No gaps.
- Top 5 with `RANK <= 5`: users 1 to 6 (six rows), because users 5 and 6 are both rank 5. User 7 has rank 7 and is out.
- Exactly five with `ROW_NUMBER` and tie-break `user_id`: users 1, 2, 3, 4, 5. User 6 is dropped only because its id is larger than 5's.

**Code:** run with `python3 -I`.
```python
# Q18: rank users by number of events
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
INSERT INTO events VALUES
 (1,1,'2024-01-01'),(2,1,'2024-01-02'),(3,1,'2024-01-03'),(4,1,'2024-01-04'),(5,1,'2024-01-05'),
 (6,2,'2024-01-01'),(7,2,'2024-01-02'),(8,2,'2024-01-03'),(9,2,'2024-01-04'),
 (10,3,'2024-01-01'),(11,3,'2024-01-02'),(12,3,'2024-01-03'),(13,3,'2024-01-04'),
 (14,4,'2024-01-01'),(15,4,'2024-01-02'),(16,4,'2024-01-03'),
 (17,5,'2024-01-01'),(18,5,'2024-01-02'),
 (19,6,'2024-01-01'),(20,6,'2024-01-02'),
 (21,7,'2024-01-01');
"""
SQL_MAIN = """
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events,
         RANK() OVER (ORDER BY n_events DESC) AS rnk,
         DENSE_RANK() OVER (ORDER BY n_events DESC) AS dense_rnk,
         ROW_NUMBER() OVER (ORDER BY n_events DESC, user_id) AS rn
  FROM counts
)
SELECT user_id, n_events, rnk, dense_rnk, rn
FROM ranked
ORDER BY rn
"""
SQL_TOP5 = """
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events, RANK() OVER (ORDER BY n_events DESC) AS rnk
  FROM counts
)
SELECT user_id, n_events, rnk FROM ranked WHERE rnk <= 5 ORDER BY rnk, user_id
"""
SQL_EXACT5 = """
WITH counts AS (
  SELECT user_id, COUNT(*) AS n_events FROM events GROUP BY user_id
), ranked AS (
  SELECT user_id, n_events, ROW_NUMBER() OVER (ORDER BY n_events DESC, user_id) AS rn
  FROM counts
)
SELECT user_id, n_events, rn FROM ranked WHERE rn <= 5 ORDER BY rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_all = pd.read_sql_query(SQL_MAIN, con)
sql_top5 = pd.read_sql_query(SQL_TOP5, con)
sql_exact = pd.read_sql_query(SQL_EXACT5, con)
print("All users ranked:"); print(sql_all.to_string(index=False))
print("\nTop 5 including ties (RANK <= 5):"); print(sql_top5.to_string(index=False))
print("\nExactly five (ROW_NUMBER, tie-break user_id):"); print(sql_exact.to_string(index=False))
print("\nDENSE_RANK <= 5 would return", int((sql_all["dense_rnk"] <= 5).sum()), "users")

ev = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
counts = ev.groupby("user_id").size().rename("n_events").reset_index()
counts["rnk"] = counts["n_events"].rank(method="min", ascending=False).astype(int)
counts["dense_rnk"] = counts["n_events"].rank(method="dense", ascending=False).astype(int)
pd_all = counts.sort_values(["n_events", "user_id"], ascending=[False, True]).reset_index(drop=True)
pd_all["rn"] = pd_all.index + 1
pd_top5 = pd_all.loc[pd_all["rnk"] <= 5, ["user_id", "n_events", "rnk"]].reset_index(drop=True)
pd_exact = pd_all.head(5)[["user_id", "n_events", "rn"]]
# pd:end
print("\npandas value_counts:", ev["user_id"].value_counts().sort_index().tolist())
# compared in rn order (most events first, then user_id)
pd.testing.assert_frame_equal(sql_all, pd_all[["user_id", "n_events", "rnk", "dense_rnk", "rn"]], check_dtype=False)
pd.testing.assert_frame_equal(sql_top5, pd_top5, check_dtype=False)
pd.testing.assert_frame_equal(sql_exact, pd_exact.reset_index(drop=True), check_dtype=False)
print("asserts passed: SQL == pandas for ranks, top 5 with ties and exactly five")
```

**Output (my run):**
```text
All users ranked:
 user_id  n_events  rnk  dense_rnk  rn
       1         5    1          1   1
       2         4    2          2   2
       3         4    2          2   3
       4         3    4          3   4
       5         2    5          4   5
       6         2    5          4   6
       7         1    7          5   7

Top 5 including ties (RANK <= 5):
 user_id  n_events  rnk
       1         5    1
       2         4    2
       3         4    2
       4         3    4
       5         2    5
       6         2    5

Exactly five (ROW_NUMBER, tie-break user_id):
 user_id  n_events  rn
       1         5   1
       2         4   2
       3         4   3
       4         3   4
       5         2   5

DENSE_RANK <= 5 would return 7 users

pandas value_counts: [5, 4, 4, 3, 2, 2, 1]
asserts passed: SQL == pandas for ranks, top 5 with ties and exactly five
```

**Edge cases:**
- Ties at the cutoff: the tied users 5 and 6 are both returned with `RANK <= 5`; "top 5" then returns six rows. If a downstream step needs exactly five, say so and pick a tie-break.
- `DENSE_RANK <= 5` would return all seven users here (the run prints 7) because there are only five distinct counts.
- Users with zero events do not appear: they have no rows to count. Join to a users table with `LEFT JOIN` and `COUNT(e.event_id)` if they should be ranked at 0.
- Empty events table: the CTE is empty, so the query returns no rows.

**Then explain:**
- **Count then rank:** `RANK() OVER (ORDER BY COUNT(*) DESC)` in the same `GROUP BY` query also works in SQLite because windows are evaluated after grouping, but the CTE form is easier to read and to extend.
- **Tie-breaker for exactly five:** the choice (lowest user_id, earliest first event, and so on) is a business rule, and I state it.
- **pandas:** `rank(method="min", ascending=False)` returns floats, so I cast to int. `value_counts()` sorts by count but its order among equal counts is not something I rely on; I sort by `n_events` and `user_id` explicitly.

**Follow-ups:**
- *Top 5 per country?* Add `PARTITION BY country` to the window and join the user's country (Q4 pattern).
- *Rank by distinct days active?* `COUNT(DISTINCT date(event_time))`.
- *Use `LIMIT 5`?* That gives exactly five with an arbitrary tie rule unless `ORDER BY` includes a tie-break.

**Common mistakes:**
- Ranking raw events instead of counts.
- `LIMIT 5` without a tie-break, then claiming "top 5 including ties".
- Using `ROW_NUMBER` and silently dropping tied users.
- Forgetting `ascending=False` in pandas `rank` (rank 1 would be the least active).

### Q19 ⭐⭐⭐ 🔴 FIRST_VALUE, LAST_VALUE and the default-frame trap: products(product_id, category, name, price). For each product show the cheapest and the most expensive product name in its category using FIRST_VALUE and LAST_VALUE over (PARTITION BY category ORDER BY price). Show that LAST_VALUE returns the current row's own value (or its ties) under the default frame, explain that the default frame with ORDER BY is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, and fix it with ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING or by reversing the ORDER BY. Give the pandas groupby transform('first') / transform('last') after sorting.
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** With `ORDER BY` in the window, the default frame ends at the current row (and its peers), so `LAST_VALUE` just returns the current row's own value; fix it with `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, or get the same answer from `FIRST_VALUE` over the reversed order.

**Schema and sample data:** six products, Fruit has two items at price 20 (Banana, Cherry) to show peers.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Veg','Okra',25);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_PEERS` shows the peer behaviour.
```sql
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS priciest_default,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS priciest_fixed,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price DESC, product_id DESC) AS priciest_rev
FROM products
ORDER BY product_id
```

**pandas answer:** sort, then take the first and last name of each group with `transform`.
```python
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
g = s.groupby("category")["name"]
pd_df = s.assign(cheapest=g.transform("first"), priciest_fixed=g.transform("last"))
```

**Example:**
- Fruit sorted by price, product_id: Banana (20), Cherry (20), Apple (30), Date (50). Veg: Leek (10), Okra (25).
- `FIRST_VALUE(name)`: Banana for every Fruit row, Leek for every Veg row. Correct.
- `LAST_VALUE(name)` with the default frame: the frame for Banana is just Banana (start to current row), so it returns Banana; Cherry returns Cherry; Apple returns Apple; Date returns Date. Each row sees itself, never the group's last row. Same for Veg.
- With `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, the frame is the whole category, so every Fruit row gets Date and every Veg row gets Okra.
- Reversed order: `FIRST_VALUE(name)` over `ORDER BY price DESC, product_id DESC` gives the same Date and Okra, with no frame clause needed.
- Peers: if the window orders by `price` only, Banana and Cherry are peers (same price). The default frame is a RANGE frame, so a row's frame includes all its peers: `COUNT(*)` over that frame is 2 for both Banana and Cherry (the run shows it), not 1 and 2. So a peer can see a later tied row. I printed a count rather than a name because which tied name comes last is unspecified.

**Code:** run with `python3 -I`.
```python
# Q19: FIRST_VALUE, LAST_VALUE and the default-frame trap
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Veg','Okra',25);
"""
SQL_MAIN = """
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS priciest_default,
       LAST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS priciest_fixed,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price DESC, product_id DESC) AS priciest_rev
FROM products
ORDER BY product_id
"""
SQL_PEERS = """
SELECT product_id, name, price,
       COUNT(*) OVER (PARTITION BY category ORDER BY price) AS rows_in_frame
FROM products WHERE category = 'Fruit'
ORDER BY product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))
print("\nPeers under the default frame (price only in ORDER BY):")
print(pd.read_sql_query(SQL_PEERS, con).to_string(index=False))

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
g = s.groupby("category")["name"]
pd_df = s.assign(cheapest=g.transform("first"), priciest_fixed=g.transform("last"))
# pd:end
print("\npandas:"); print(pd_df.sort_values("product_id").to_string(index=False))
cols = ["product_id", "category", "name", "price", "cheapest"]
# compared after sorting by product_id
pd.testing.assert_frame_equal(sql_df[cols], pd_df.sort_values("product_id").reset_index(drop=True)[cols], check_dtype=False)
assert sql_df["priciest_fixed"].tolist() == pd_df.sort_values("product_id")["priciest_fixed"].tolist()
assert sql_df["priciest_rev"].tolist() == sql_df["priciest_fixed"].tolist()
assert sql_df["priciest_default"].tolist() == sql_df["name"].tolist()   # default frame: last_value is the row itself here
print("\nasserts passed: fixed frame == reversed order == pandas 'last'; default LAST_VALUE equals the row's own name")
```

**Output (my run):**
```text
SQL:
 product_id category   name  price cheapest priciest_default priciest_fixed priciest_rev
          1    Fruit  Apple     30   Banana            Apple           Date         Date
          2    Fruit Banana     20   Banana           Banana           Date         Date
          3    Fruit Cherry     20   Banana           Cherry           Date         Date
          4    Fruit   Date     50   Banana             Date           Date         Date
          5      Veg   Leek     10     Leek             Leek           Okra         Okra
          6      Veg   Okra     25     Leek             Okra           Okra         Okra

Peers under the default frame (price only in ORDER BY):
 product_id   name  price  rows_in_frame
          1  Apple     30              3
          2 Banana     20              2
          3 Cherry     20              2
          4   Date     50              4

pandas:
 product_id category   name  price cheapest priciest_fixed
          1    Fruit  Apple     30   Banana           Date
          2    Fruit Banana     20   Banana           Date
          3    Fruit Cherry     20   Banana           Date
          4    Fruit   Date     50   Banana           Date
          5      Veg   Leek     10     Leek           Okra
          6      Veg   Okra     25     Leek           Okra

asserts passed: fixed frame == reversed order == pandas 'last'; default LAST_VALUE equals the row's own name
```

**Edge cases:**
- Ties on price: the cheapest name depends on the tie-break; I added `product_id` so the answer is fixed. Without it, which tied product is "first" is unspecified.
- NULL price: SQLite sorts NULL first in ascending order, so a NULL-priced product would be "cheapest". Filter NULL prices first or use `ORDER BY price NULLS LAST` (ran on SQLite 3.45). Other engines default differently (not executed here).
- One product in a category: first and last are that product.
- `FIRST_VALUE` is not affected by the trap because the default frame always starts at the partition start.

**Then explain:**
- **Default frame:** when the window has `ORDER BY` and no frame clause, it is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`; without `ORDER BY` it is the whole partition. SQLite documents this default.
- **Two fixes:** an explicit full frame, or reverse the order and use `FIRST_VALUE`. I prefer the explicit frame because it states intent.
- **ROWS versus RANGE:** `ROWS` counts physical rows, `RANGE` includes all peers (rows tied on the `ORDER BY` key).
- **pandas:** there is no frame, just sort, then `transform("first")` and `transform("last")`. The sort is the whole definition of "first".

**Follow-ups:**
- *Price difference from the cheapest?* `price - FIRST_VALUE(price) OVER (...)`.
- *Why not `MIN`/`MAX`?* They give the price but not the name; for names you need the value functions or a join.
- *Does the same trap hit `NTH_VALUE`?* Yes, it is also frame-sensitive (Q23).

**Common mistakes:**
- Using `LAST_VALUE` with the default frame and getting "the current row" back.
- Reversing the order but forgetting the tie-break.
- Forgetting to sort in pandas before `first`/`last`.

### Q20 ⭐⭐ 🟢 Choosing the ranking function from the requirement: for each requirement below state ROW_NUMBER, RANK or DENSE_RANK and show it on employees(emp_id, name, dept_id, salary) with ties: 'exactly one row per department', 'everyone tied for the top', 'top three salary levels', 'second highest salary', 'number every row for pagination', 'leaderboard with shared positions and gaps'. Explain the reasoning in one line each and give the pandas rank(method=...) mapping.
**Asked at:** GeeksforGeeks SQL interview questions (RANK vs DENSE_RANK vs ROW_NUMBER, window functions, duplicates entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** `ROW_NUMBER` when you need exactly N rows or a unique number, `RANK` when tied rows should share a place and the next place is skipped, `DENSE_RANK` when you count distinct values (salary levels) with no gaps.

**Schema and sample data:** eight employees; Asha and Ben tie at 90, Dev and Esha tie at 70 in dept 10; Gita and Hari tie at 50 in dept 20.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',10,70),(6,'Farid',20,60),(7,'Gita',20,50),(8,'Hari',20,50);
```

**SQL answer:** `SQL_MAIN` computes all three functions (Code block). The requirements below filter it.
```sql
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dr
FROM employees
ORDER BY dept_id, rn
```

**pandas answer:** `rank` with `method="first"` / `"min"` / `"dense"` maps to `ROW_NUMBER` / `RANK` / `DENSE_RANK`. I get `ROW_NUMBER` with `cumcount` after an explicit sort so ties are deterministic.
```python
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int))
```

**Example:** dept 10, salary descending: Asha 90, Ben 90, Chitra 80, Dev 70, Esha 70. `ROW_NUMBER` with tie-break `emp_id`: 1, 2, 3, 4, 5. `RANK`: 1, 1, 3, 4, 4. `DENSE_RANK`: 1, 1, 2, 3, 3. Dept 20: Farid 60, Gita 50, Hari 50: `RANK` 1, 2, 2; `DENSE_RANK` 1, 2, 2.

| Requirement | Function and filter | Reason, one line | pandas |
|---|---|---|---|
| Exactly one row per department | `ROW_NUMBER`, `rn = 1` | Always one row per partition; the tie-break decides who. | `rank(method="first")` after sorting, or `head(1)` |
| Everyone tied for the top | `RANK`, `rk = 1` | Tied rows share rank 1. | `rank(method="min") == 1` |
| Top three salary levels | `DENSE_RANK`, `dr <= 3` | Counts distinct salaries, so ties do not use up places. | `rank(method="dense") <= 3` |
| Second highest salary | `DENSE_RANK`, `dr = 2` | `RANK = 2` returns nothing when two people tie for first. | `rank(method="dense") == 2` |
| Number every row for pagination | `ROW_NUMBER` over a total order | Unique and gapless, so pages never repeat or skip a row. | `reset_index` after sort, then slice |
| Leaderboard with shared positions and gaps | `RANK` | Competition style: 1, 1, 3. | `rank(method="min")` |

**Code:** run with `python3 -I`.
```python
# Q20: choosing the ranking function from the requirement
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',10,70),(6,'Farid',20,60),(7,'Gita',20,50),(8,'Hari',20,50);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk,
       DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dr
FROM employees
ORDER BY dept_id, rn
"""
SQL_PAGE = """
SELECT name, salary FROM (
  SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS rn FROM employees)
WHERE rn BETWEEN 4 AND 6
ORDER BY rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in dept_id, rn order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

pick = {
    "exactly one row per department (rn = 1)": sql_df[sql_df.rn == 1]["name"].tolist(),
    "everyone tied for the top (rk = 1)": sql_df[sql_df.rk == 1]["name"].tolist(),
    "top three salary levels (dr <= 3)": sql_df[sql_df.dr <= 3]["name"].tolist(),
    "second highest salary (dr = 2)": sql_df[sql_df.dr == 2]["name"].tolist(),
    "leaderboard with gaps (rk)": list(zip(sql_df["name"], sql_df["rk"])),
}
print()
for k, v in pick.items():
    print(k, "->", v)
print("pagination, page 2 of size 3 over the whole table (global ROW_NUMBER, rn 4..6):")
print(pd.read_sql_query(SQL_PAGE, con).to_string(index=False))
# the pandas 'first' method numbers ties in order of appearance, which is only deterministic after sorting
first = s.groupby("dept_id")["salary"].rank(method="first", ascending=False).astype(int)
assert first.tolist() == pd_df["rn"].tolist()
print("\nasserts passed: SQL == pandas; rank(method='first') on sorted data == ROW_NUMBER")
```

**Output (my run):**
```text
SQL:
 emp_id   name  dept_id  salary  rn  rk  dr
      1   Asha       10      90   1   1   1
      2    Ben       10      90   2   1   1
      3 Chitra       10      80   3   3   2
      4    Dev       10      70   4   4   3
      5   Esha       10      70   5   4   3
      6  Farid       20      60   1   1   1
      7   Gita       20      50   2   2   2
      8   Hari       20      50   3   2   2

pandas:
 emp_id   name  dept_id  salary  rn  rk  dr
      1   Asha       10      90   1   1   1
      2    Ben       10      90   2   1   1
      3 Chitra       10      80   3   3   2
      4    Dev       10      70   4   4   3
      5   Esha       10      70   5   4   3
      6  Farid       20      60   1   1   1
      7   Gita       20      50   2   2   2
      8   Hari       20      50   3   2   2

exactly one row per department (rn = 1) -> ['Asha', 'Farid']
everyone tied for the top (rk = 1) -> ['Asha', 'Ben', 'Farid']
top three salary levels (dr <= 3) -> ['Asha', 'Ben', 'Chitra', 'Dev', 'Esha', 'Farid', 'Gita', 'Hari']
second highest salary (dr = 2) -> ['Chitra', 'Gita', 'Hari']
leaderboard with gaps (rk) -> [('Asha', 1), ('Ben', 1), ('Chitra', 3), ('Dev', 4), ('Esha', 4), ('Farid', 1), ('Gita', 2), ('Hari', 2)]
pagination, page 2 of size 3 over the whole table (global ROW_NUMBER, rn 4..6):
 name  salary
  Dev      70
 Esha      70
Farid      60

asserts passed: SQL == pandas; rank(method='first') on sorted data == ROW_NUMBER
```

**Edge cases:**
- Without a tie-break, `ROW_NUMBER` still assigns 1..n but the order among tied rows is unspecified, so I always add `emp_id` (shown here).
- Second highest salary with `RANK = 2`: dept 10 has two people at 90, so `RANK` goes 1, 1, 3 and `rk = 2` returns no one; `dr = 2` correctly returns Chitra.
- NULL salary: SQLite sorts NULL last under `DESC` (smallest), so NULL rows rank last; other engines can differ (not executed here), and pandas `rank` leaves NaN unranked by default (`na_option="keep"`).
- Pagination over the whole table needs a total order; the page query in the run uses `salary DESC, emp_id`.

**Then explain:**
- Three questions pick the function: do ties need separate numbers (`ROW_NUMBER`), do I need the gap after a tie (`RANK`), do I count distinct values (`DENSE_RANK`).
- **pandas methods:** `rank` returns floats, so I cast to int. `method="first"` numbers ties in the order rows appear, which is why I sort first.
- For huge offsets, keyset pagination (`WHERE (salary, emp_id) < (?, ?)`) is better than numbering every row; not executed here.

**Follow-ups:**
- *Which one for "top 3 earners" if the business says "3 people"?* Ask; `ROW_NUMBER` gives exactly three, `RANK` may give more (Q26).
- *Percent rank?* `PERCENT_RANK`, Q22.
- *Do the functions ignore `PARTITION BY` by default?* Without it, the whole result is one partition.

**Common mistakes:**
- `RANK = 2` for the second highest salary.
- `ROW_NUMBER` without a tie-break and treating the order as stable.
- Forgetting `ascending=False` in pandas.
- Using `RANK` for pagination: gaps and repeats make page boundaries wrong.

### Q21 ⭐⭐ 🟢 NTILE: bucket customers into quartiles by total spend. customers(customer_id, name) and orders(order_id, customer_id, amount). Compute each customer's total, then NTILE(4) OVER (ORDER BY total DESC) so bucket 1 is the top spenders. Show what happens when the row count does not divide evenly (SQLite: larger groups come first) and say what ordering direction does to bucket meaning. Give the pandas version (rank then qcut or a computed bucket) and note NTILE is positional.
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Total spend per customer in a CTE, then `NTILE(4) OVER (ORDER BY total DESC)`; bucket 1 is the top quarter, ten customers split 3, 3, 2, 2 (larger groups first), and NTILE is purely positional, so customers with equal totals can land in different buckets.

**Schema and sample data:** ten customers; Jai has no orders. Ben and Chitra tie at 400, and Hari and Ila tie at 100.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),
  (6,'Farid'),(7,'Gita'),(8,'Hari'),(9,'Ila'),(10,'Jai');
INSERT INTO orders VALUES (1,1,300),(2,1,200),(3,2,400),(4,3,250),(5,3,150),(6,4,300),
  (7,5,250),(8,6,100),(9,6,100),(10,7,150),(11,8,100),(12,9,60),(13,9,40);
```

**SQL answer:** `SQL_MAIN` (Code block). `SQL_ASC` is the ascending variant.
```sql
WITH totals AS (
  SELECT c.customer_id, c.name, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, total,
       NTILE(4) OVER (ORDER BY total DESC, customer_id) AS quartile
FROM totals
ORDER BY total DESC, customer_id
```

**pandas answer:** sort by total (with a tie-break), then compute the bucket from the 0-based position with the same rule SQLite uses: with n rows and k buckets, the first `n % k` buckets get one extra row. `pd.qcut` is shown in the run as a contrast, not as the equivalent.
```python
def ntile(pos0, n, k):
    # pos0 = 0-based position; the first n % k buckets get one extra row (SQLite and most engines)
    q, r = divmod(n, k)
    cut = r * (q + 1)
    return pos0 // (q + 1) + 1 if pos0 < cut else r + (pos0 - cut) // q + 1

tot = (customers.merge(orders.groupby("customer_id", as_index=False).agg(total=("amount", "sum")),
                       on="customer_id", how="left")
       .fillna({"total": 0}).astype({"total": "int64"}))
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
tot["quartile"] = [ntile(i, len(tot), 4) for i in range(len(tot))]
pd_df = tot
```

**Example:**
- Totals: Asha 500, Ben 400, Chitra 400, Dev 300, Esha 250, Farid 200, Gita 150, Hari 100, Ila 100, Jai 0 (no orders, so `COALESCE` gives 0).
- 10 rows into 4 buckets is 2 each plus 2 left over, and the first two buckets get the extra row: sizes 3, 3, 2, 2.
- Sorted by total descending, then customer_id: positions 1 to 3 (Asha, Ben, Chitra) are bucket 1; 4 to 6 (Dev, Esha, Farid) bucket 2; 7 and 8 (Gita, Hari) bucket 3; 9 and 10 (Ila, Jai) bucket 4.
- Hari and Ila both spent 100, yet Hari is in bucket 3 and Ila in bucket 4. That is the positional nature of NTILE: the tie-break (customer_id) decides.
- With ascending order bucket 1 would mean the lowest spenders, and the extra rows would go to the low buckets (the run shows Ben and Chitra, tied at 400, landing in buckets 3 and 4).

**Code:** run with `python3 -I`.
```python
# Q21: NTILE quartiles by total spend
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),
  (6,'Farid'),(7,'Gita'),(8,'Hari'),(9,'Ila'),(10,'Jai');
INSERT INTO orders VALUES (1,1,300),(2,1,200),(3,2,400),(4,3,250),(5,3,150),(6,4,300),
  (7,5,250),(8,6,100),(9,6,100),(10,7,150),(11,8,100),(12,9,60),(13,9,40);
"""
SQL_MAIN = """
WITH totals AS (
  SELECT c.customer_id, c.name, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, total,
       NTILE(4) OVER (ORDER BY total DESC, customer_id) AS quartile
FROM totals
ORDER BY total DESC, customer_id
"""
SQL_ASC = """
WITH totals AS (
  SELECT c.customer_id, COALESCE(SUM(o.amount), 0) AS total
  FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
  GROUP BY c.customer_id
)
SELECT customer_id, total, NTILE(4) OVER (ORDER BY total, customer_id) AS quartile_asc
FROM totals
ORDER BY total DESC, customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL NTILE(4), bucket 1 = top spenders:"); print(sql_df.to_string(index=False))
print("\nbucket sizes:", sql_df["quartile"].value_counts().sort_index().tolist())
asc = pd.read_sql_query(SQL_ASC, con)
print("\nSame with ascending order (bucket 1 = lowest spenders):", asc["quartile_asc"].tolist())

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
def ntile(pos0, n, k):
    # pos0 = 0-based position; the first n % k buckets get one extra row (SQLite and most engines)
    q, r = divmod(n, k)
    cut = r * (q + 1)
    return pos0 // (q + 1) + 1 if pos0 < cut else r + (pos0 - cut) // q + 1

tot = (customers.merge(orders.groupby("customer_id", as_index=False).agg(total=("amount", "sum")),
                       on="customer_id", how="left")
       .fillna({"total": 0}).astype({"total": "int64"}))
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
tot["quartile"] = [ntile(i, len(tot), 4) for i in range(len(tot))]
pd_df = tot
# pd:end
print("\npandas positional NTILE:"); print(pd_df.to_string(index=False))
# compared in total DESC, customer_id order
pd.testing.assert_frame_equal(sql_df, pd_df[["customer_id", "name", "total", "quartile"]], check_dtype=False)

# contrast: qcut cuts by VALUE quantiles, so equal values stay together and sizes are not forced
qc = 4 - pd.qcut(pd_df["total"], 4, labels=False)
pd_df = pd_df.assign(qcut_bucket=qc)
print("\nqcut (relabelled so 1 = top):"); print(pd_df[["name", "total", "quartile", "qcut_bucket"]].to_string(index=False))
print("qcut bucket sizes:", pd_df["qcut_bucket"].value_counts().sort_index().tolist())
diff = pd_df[pd_df["quartile"] != pd_df["qcut_bucket"]]["name"].tolist()
print("customers where NTILE and qcut disagree:", diff)
print("asserts passed: SQL NTILE == pandas positional version")
```

**Output (my run):**
```text
SQL NTILE(4), bucket 1 = top spenders:
 customer_id   name  total  quartile
           1   Asha    500         1
           2    Ben    400         1
           3 Chitra    400         1
           4    Dev    300         2
           5   Esha    250         2
           6  Farid    200         2
           7   Gita    150         3
           8   Hari    100         3
           9    Ila    100         4
          10    Jai      0         4

bucket sizes: [3, 3, 2, 2]

Same with ascending order (bucket 1 = lowest spenders): [4, 3, 4, 3, 2, 2, 2, 1, 1, 1]

pandas positional NTILE:
 customer_id   name  total  quartile
           1   Asha    500         1
           2    Ben    400         1
           3 Chitra    400         1
           4    Dev    300         2
           5   Esha    250         2
           6  Farid    200         2
           7   Gita    150         3
           8   Hari    100         3
           9    Ila    100         4
          10    Jai      0         4

qcut (relabelled so 1 = top):
  name  total  quartile  qcut_bucket
  Asha    500         1            1
   Ben    400         1            1
Chitra    400         1            1
   Dev    300         2            2
  Esha    250         2            2
 Farid    200         2            3
  Gita    150         3            3
  Hari    100         3            4
   Ila    100         4            4
   Jai      0         4            4
qcut bucket sizes: [3, 2, 2, 3]
customers where NTILE and qcut disagree: ['Farid', 'Hari']
asserts passed: SQL NTILE == pandas positional version
```

**Edge cases:**
- Customers with no orders: the `LEFT JOIN` plus `COALESCE` keeps them as 0 spend (Jai). An inner join would drop them and change the bucket sizes. Whether non-buyers belong in the quartiles is a business decision; say it.
- Ties: NTILE can split equal totals across buckets; if equal totals must share a bucket, use `qcut`-style value thresholds or `PERCENT_RANK`/`CUME_DIST` (Q22) and bucket on those.
- Fewer rows than buckets (for example 3 customers, `NTILE(4)`): the first three buckets get one row each and bucket 4 is empty, from SQLite's documented behaviour; I did not run it here.
- NULL total: not possible after `COALESCE`; with a NULL, SQLite would sort it last under `DESC`.

**Then explain:**
- **Uneven split:** SQLite puts the larger groups first, as documented and shown in the run (3, 3, 2, 2). I believe other engines do the same, but that is not executed here.
- **Direction:** `ORDER BY total DESC` makes bucket 1 the best; `ASC` flips the meaning. I name the column (`top_quartile`) so nobody misreads it.
- **qcut versus NTILE:** the run shows `qcut` sizes 3, 2, 2, 3 against NTILE's 3, 3, 2, 2, and they disagree for Farid and Hari. `qcut` computes quantile edges from the values and puts each value into a bin, so Hari and Ila (both 100) share a bin; NTILE counts positions and splits them.
- **pandas:** there is no built-in NTILE. A positional formula (above) reproduces it exactly, which the run asserts; `rank(method="first")` then integer arithmetic is the other common route.

**Follow-ups:**
- *Average spend per quartile?* Group the result by `quartile`.
- *Deciles?* `NTILE(10)`.
- *Quartile within each region?* Add `PARTITION BY region`.

**Common mistakes:**
- Forgetting the tie-break, so bucket membership of tied customers is arbitrary.
- Reading NTILE as "value thresholds" instead of "equal counts".
- Inner join dropping customers with no orders.
- Using `pd.qcut` and expecting it to match NTILE exactly.

### Q22 ⭐⭐ 🟢 PERCENT_RANK and CUME_DIST: scores(student_id, score) with ties. Show RANK, PERCENT_RANK (rank-1)/(n-1) and CUME_DIST (rows up to and including the last peer / n) side by side, explain the one-row partition (PERCENT_RANK is 0.0) and what each one means in words ('percentage of rows below you' versus 'at or below you'), and give the pandas rank(pct=True) comparison.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `PERCENT_RANK` is (rank - 1) / (n - 1), the share of rows strictly below you (0 for the lowest, 1 for the highest); `CUME_DIST` is (rows up to and including your last tie) / n, the share at or below you, and pandas `rank(pct=True, method="max")` equals `CUME_DIST`.

**Schema and sample data:** five scores with a tie at 60, plus a one-row table.
```sql
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,50),(2,60),(3,60),(4,70),(5,90);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
```

**SQL answer:** `SQL_MAIN` uses one named window for all three (Code block); `SQL_SOLO` tests the one-row case.
```sql
SELECT student_id, score,
       RANK() OVER w AS rnk,
       PERCENT_RANK() OVER w AS pct_rank,
       CUME_DIST() OVER w AS cume_dist
FROM scores
WINDOW w AS (ORDER BY score)
ORDER BY score, student_id
```

**pandas answer:** `PERCENT_RANK` from a `method="min"` rank; `CUME_DIST` from `rank(method="max", pct=True)`.
```python
n = len(scores)
rk = scores["score"].rank(method="min")
pd_df = scores.assign(
    rnk=rk.astype(int),
    pct_rank=(rk - 1) / (n - 1),
    cume_dist=scores["score"].rank(method="max", pct=True),
).sort_values(["score", "student_id"]).reset_index(drop=True)
```

**Example:** n = 5; scores 50, 60, 60, 70, 90.
- `RANK`: 1, 2, 2, 4, 5.
- `PERCENT_RANK` = (rank - 1) / 4: 0.0, 0.25, 0.25, 0.75, 1.0.
- `CUME_DIST` = rows at or below / 5: 50 has 1 row so 0.2; both 60s have 3 rows up to the last tie so 0.6; 70 has 4 so 0.8; 90 has 5 so 1.0.
- In words: the score of 70 is above 75 percent of the rows (percent rank) and at or above 80 percent of the rows (cumulative distribution). The two 60s both get 0.6 for `CUME_DIST` because it counts through the last peer.
- One row: `PERCENT_RANK` is 0.0 (SQLite does not divide by zero here), `CUME_DIST` is 1.0.

**Code:** run with `python3 -I`.
```python
# Q22: PERCENT_RANK and CUME_DIST
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,50),(2,60),(3,60),(4,70),(5,90);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
"""
SQL_MAIN = """
SELECT student_id, score,
       RANK() OVER w AS rnk,
       PERCENT_RANK() OVER w AS pct_rank,
       CUME_DIST() OVER w AS cume_dist
FROM scores
WINDOW w AS (ORDER BY score)
ORDER BY score, student_id
"""
SQL_SOLO = """
SELECT student_id, score, PERCENT_RANK() OVER (ORDER BY score) AS pct_rank,
       CUME_DIST() OVER (ORDER BY score) AS cume_dist
FROM solo
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))
print("\nOne-row table:"); print(pd.read_sql_query(SQL_SOLO, con).to_string(index=False))

scores = pd.read_sql_query("SELECT * FROM scores", con)
# pd:main
n = len(scores)
rk = scores["score"].rank(method="min")
pd_df = scores.assign(
    rnk=rk.astype(int),
    pct_rank=(rk - 1) / (n - 1),
    cume_dist=scores["score"].rank(method="max", pct=True),
).sort_values(["score", "student_id"]).reset_index(drop=True)
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in score, student_id order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)

print("\nrank(pct=True) default method (average):", scores["score"].rank(pct=True).tolist())
print("rank(pct=True, method='max'):            ", scores["score"].rank(pct=True, method="max").tolist())
one = pd.Series([75])
with np.errstate(all="ignore"):
    print("one row: my pct_rank formula =", ((one.rank(method="min") - 1) / (len(one) - 1)).tolist(),
          "| rank(pct=True) =", one.rank(pct=True).tolist())
manual = [(scores['score'] <= v).sum() / n for v in sql_df['score']]
assert sql_df['cume_dist'].tolist() == manual
print("asserts passed: SQL == pandas; cume_dist == rank(method='max', pct=True)")
```

**Output (my run):**
```text
SQL:
 student_id  score  rnk  pct_rank  cume_dist
          1     50    1      0.00        0.2
          2     60    2      0.25        0.6
          3     60    2      0.25        0.6
          4     70    4      0.75        0.8
          5     90    5      1.00        1.0

One-row table:
 student_id  score  pct_rank  cume_dist
          1     75       0.0        1.0

pandas:
 student_id  score  rnk  pct_rank  cume_dist
          1     50    1      0.00        0.2
          2     60    2      0.25        0.6
          3     60    2      0.25        0.6
          4     70    4      0.75        0.8
          5     90    5      1.00        1.0

rank(pct=True) default method (average): [0.2, 0.5, 0.5, 0.8, 1.0]
rank(pct=True, method='max'):             [0.2, 0.6, 0.6, 0.8, 1.0]
one row: my pct_rank formula = [nan] | rank(pct=True) = [1.0]
asserts passed: SQL == pandas; cume_dist == rank(method='max', pct=True)
```

**Edge cases:**
- One-row partition: SQLite returns 0.0 for `PERCENT_RANK` (the run). My pandas formula gives NaN there because (1-1)/(1-1) is 0/0, so guard it if single-row groups can occur; `rank(pct=True)` on one value is 1.0, which matches `CUME_DIST`, not `PERCENT_RANK`.
- Ties: `PERCENT_RANK` uses the first row of the tie (rank), `CUME_DIST` the last. Surprise from the run: pandas default `rank(pct=True)` uses the average method and gives 0.5 for the tied 60s, which equals neither SQL function. Only `method="max"` matches `CUME_DIST`.
- NULL scores: SQLite orders them first and counts them in n. pandas `rank` leaves NaN unranked and `pct=True` divides by the non-NaN count, so results can differ (I did not run a NULL case here).
- `CUME_DIST` is never 0; `PERCENT_RANK` is always 0 for the first rank.

**Then explain:**
- **Which to use:** "what percent of students scored below me" is `PERCENT_RANK`; "what percentile am I at or below" is `CUME_DIST`. Say which one you mean.
- **Formulas:** both are documented in the SQLite window-function page; the run confirms them on this data.
- **Top 10 percent:** `CUME_DIST() > 0.9` on a descending order, or `PERCENT_RANK`, are the usual filters.

**Follow-ups:**
- *Do they depend on ties?* Yes, as above.
- *Percentile value (median)?* That is `PERCENTILE_CONT`, which is not in SQLite; pandas `quantile` does it.
- *Same as `NTILE`?* No: NTILE equalises counts, these report position.

**Common mistakes:**
- Using pandas `rank(pct=True)` with the default method and expecting `CUME_DIST`.
- Reading `PERCENT_RANK = 1.0` as "100 percent of rows are below you"; it is the top rank.
- Not guarding the single-row group in pandas.

### Q23 ⭐⭐ 🟢 FIRST_VALUE and NTH_VALUE: products(product_id, category, name, price). For each product show the cheapest product's name in its category and the second cheapest, using FIRST_VALUE and NTH_VALUE(name, 2) over (PARTITION BY category ORDER BY price, product_id). Explain that NTH_VALUE returns NULL when the frame has fewer than N rows (and is frame-sensitive, so rows early in the default frame may see NULL), and give the pandas groupby nth or sort and cumcount version.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `FIRST_VALUE(name)` gives the cheapest name for every row, and `NTH_VALUE(name, 2)` gives the second cheapest only for rows whose frame already contains two rows, so with the default frame early rows see NULL; add `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` so every row sees it.

**Schema and sample data:** seven products. Fruit has four (Banana and Cherry tie at 20), Dairy has two, Veg has one.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Dairy','Milk',12),(7,'Dairy','Curd',18);
```

**SQL answer:** `SQL_MAIN` shows `FIRST_VALUE`, the default-frame `NTH_VALUE`, and the full-frame `NTH_VALUE` (Code block).
```sql
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id) AS second_default,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_cheapest
FROM products
ORDER BY product_id
```

**pandas answer:** sort, number with `cumcount`, take the position-2 row per category and map it back.
```python
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
s["pos"] = s.groupby("category").cumcount() + 1
second = s[s["pos"] == 2].set_index("category")["name"]
pd_df = s.assign(cheapest=s.groupby("category")["name"].transform("first"),
                 second_cheapest=s["category"].map(second)).drop(columns="pos")
```

**Example:** ordering inside each category is `price, product_id`.
- Fruit: Banana (20, id 2), Cherry (20, id 3), Apple (30), Date (50). Cheapest is Banana for every row.
- Second cheapest is Cherry (the tie on price is settled by `product_id`).
- Default frame: Banana's frame is just Banana (one row), so `NTH_VALUE(name, 2)` is NULL; Cherry's frame has two rows, so it is Cherry; Apple and Date also see Cherry. That is why the `second_default` column starts with a NULL in each category.
- Full frame: all four Fruit rows show Cherry.
- Dairy: Milk (12), Curd (18): second is Curd. With the default frame, Milk gets NULL, Curd gets Curd.
- Veg: one product, so `NTH_VALUE(name, 2)` is NULL in every case. The run shows NULL there even with the full frame.

**Code:** run with `python3 -I`.
```python
# Q23: FIRST_VALUE and NTH_VALUE
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Fruit','Apple',30),(2,'Fruit','Banana',20),(3,'Fruit','Cherry',20),
  (4,'Fruit','Date',50),(5,'Veg','Leek',10),(6,'Dairy','Milk',12),(7,'Dairy','Curd',18);
"""
SQL_MAIN = """
SELECT product_id, category, name, price,
       FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY price, product_id) AS cheapest,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id) AS second_default,
       NTH_VALUE(name, 2) OVER (PARTITION BY category ORDER BY price, product_id
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS second_cheapest
FROM products
ORDER BY product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))
try:
    con.execute("SELECT NTH_VALUE(name, 2) FROM LAST OVER (ORDER BY price) FROM products").fetchall()
    print("\nFROM LAST accepted")
except sqlite3.Error as e:
    print("\nNTH_VALUE ... FROM LAST on SQLite 3.45:", e)

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
s = products.sort_values(["category", "price", "product_id"]).reset_index(drop=True)
s["pos"] = s.groupby("category").cumcount() + 1
second = s[s["pos"] == 2].set_index("category")["name"]
pd_df = s.assign(cheapest=s.groupby("category")["name"].transform("first"),
                 second_cheapest=s["category"].map(second)).drop(columns="pos")
# pd:end
print("\npandas:"); print(pd_df.sort_values("product_id").to_string(index=False))
cols = ["product_id", "category", "name", "price", "cheapest", "second_cheapest"]
# compared after sorting by product_id
pd.testing.assert_frame_equal(sql_df[cols], pd_df.sort_values("product_id").reset_index(drop=True)[cols], check_dtype=False)
nth = s.groupby("category")["name"].nth(1)
print("\ngroupby().nth(1) returns:", nth.tolist(), "(rows, one per category with at least 2 items)")
assert sorted(nth.tolist()) == sorted(second.tolist())
print("asserts passed: SQL (full frame) == pandas; nth(1) agrees")
```

**Output (my run):**
```text
SQL:
 product_id category   name  price cheapest second_default second_cheapest
          1    Fruit  Apple     30   Banana         Cherry          Cherry
          2    Fruit Banana     20   Banana            NaN          Cherry
          3    Fruit Cherry     20   Banana         Cherry          Cherry
          4    Fruit   Date     50   Banana         Cherry          Cherry
          5      Veg   Leek     10     Leek            NaN             NaN
          6    Dairy   Milk     12     Milk            NaN            Curd
          7    Dairy   Curd     18     Milk           Curd            Curd

NTH_VALUE ... FROM LAST on SQLite 3.45: near "(": syntax error

pandas:
 product_id category   name  price cheapest second_cheapest
          1    Fruit  Apple     30   Banana          Cherry
          2    Fruit Banana     20   Banana          Cherry
          3    Fruit Cherry     20   Banana          Cherry
          4    Fruit   Date     50   Banana          Cherry
          5      Veg   Leek     10     Leek             NaN
          6    Dairy   Milk     12     Milk            Curd
          7    Dairy   Curd     18     Milk            Curd

groupby().nth(1) returns: ['Curd', 'Cherry'] (rows, one per category with at least 2 items)
asserts passed: SQL (full frame) == pandas; nth(1) agrees
```

**Edge cases:**
- Fewer than N rows in the frame: NULL (Veg; also the first row of every category under the default frame).
- Ties in price: without `product_id` the "second" could be either tied product, so I include it.
- NULL price: SQLite orders NULL first, so a NULL-priced product would be "cheapest". Filter or order explicitly.
- pandas: a category with one product has no position-2 row, so `map` gives NaN; SQL gives NULL. They compare equal in the assertion.

**Then explain:**
- **Frame-sensitive:** `FIRST_VALUE`, `LAST_VALUE` and `NTH_VALUE` look inside the frame, not the partition. Default frame with `ORDER BY` ends at the current row (and peers), so "second" is not visible yet for the first row (Q19 covers `LAST_VALUE`).
- **Counting direction:** SQLite does not support `FROM LAST` on `NTH_VALUE`; the run prints SQLite 3.45's syntax error for it. Reverse the order instead. Other engines may support it (not executed here).
- **pandas:** `cumcount() + 1 == 2` is explicit and keeps the row; `groupby().nth(1)` returns the same rows, as the run asserts. `nth` is zero-based.

**Follow-ups:**
- *Third cheapest?* `NTH_VALUE(name, 3)`.
- *Second cheapest price gap from the cheapest?* `NTH_VALUE(price, 2) - FIRST_VALUE(price)` over the full frame.
- *Why not `LIMIT 1 OFFSET 1`?* It is not per category.

**Common mistakes:**
- Using `NTH_VALUE` with the default frame and wondering about NULLs.
- Off-by-one between SQL (1-based) and pandas `nth`/`cumcount` (0-based).
- Not breaking price ties.

### Q24 ⭐⭐ 🟢 Named windows and reuse: employees(emp_id, name, dept_id, salary). Write one query that uses ROW_NUMBER, RANK, DENSE_RANK and AVG over the same (PARTITION BY dept_id ORDER BY salary DESC) via a WINDOW clause (WINDOW w AS (...)) and OVER w. Explain where the WINDOW clause sits (after HAVING, before ORDER BY), the benefit (one definition, no drift), that a named window can be extended in OVER (w ORDER BY ...) in some cases (hedge), and that PostgreSQL, MySQL 8 and SQLite support it (hedged beyond SQLite).
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Define the window once with `WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC)` after `HAVING` and before `ORDER BY`, then write `OVER w` on each function; a named window can be extended with `OVER (w ORDER BY ...)` only when `w` does not already have that clause, and `AVG` over an ordered window is a running average, not the department average.

**Schema and sample data:** five employees; Asha and Ben tie at 90 in dept 10.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
  (4,'Dev',20,80),(5,'Esha',20,60);
```

**SQL answer:** `SQL_MAIN` (Code block). It defines three windows: `dept` (partition only), `w` (extends `dept` with the salary order) and `ws` (adds `emp_id` so `ROW_NUMBER` is deterministic).
```sql
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER ws AS rn,
       RANK() OVER w AS rk,
       DENSE_RANK() OVER w AS dr,
       AVG(salary) OVER w AS avg_same_window,
       AVG(salary) OVER dept AS dept_avg
FROM employees
WINDOW dept AS (PARTITION BY dept_id),
       w AS (dept ORDER BY salary DESC),
       ws AS (dept ORDER BY salary DESC, emp_id)
ORDER BY dept_id, rn
```

**pandas answer:** there is no named-window object; the equivalent reuse is one sorted frame and one `groupby`.
```python
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int),
                 dept_avg=g.transform("mean"))
```

**Example:**
- Dept 10 by salary descending: Asha 90, Ben 90, Chitra 70. Dept 20: Dev 80, Esha 60.
- `RANK` over `w`: 1, 1, 3 and 1, 2. `DENSE_RANK`: 1, 1, 2 and 1, 2. `ROW_NUMBER` over `ws` (tie-break `emp_id`): 1, 2, 3 and 1, 2.
- `AVG(salary) OVER dept` (no ORDER BY): the whole department, (90 + 90 + 70) / 3 = 83.33 for all three dept 10 rows; 70 for dept 20.
- `AVG(salary) OVER w` (the same ordered window): this is a cumulative average through the current row and its peers. Asha and Ben are peers, so both get (90 + 90) / 2 = 90; Chitra gets 83.33. In dept 20: Dev 80, then (80 + 60) / 2 = 70. So it equals the department average only on the last row. If someone asks for "the same window including AVG", I point this out and use the unordered window for the department average.

**Code:** run with `python3 -I`.
```python
# Q24: named windows and reuse
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
  (4,'Dev',20,80),(5,'Esha',20,60);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       ROW_NUMBER() OVER ws AS rn,
       RANK() OVER w AS rk,
       DENSE_RANK() OVER w AS dr,
       AVG(salary) OVER w AS avg_same_window,
       AVG(salary) OVER dept AS dept_avg
FROM employees
WINDOW dept AS (PARTITION BY dept_id),
       w AS (dept ORDER BY salary DESC),
       ws AS (dept ORDER BY salary DESC, emp_id)
ORDER BY dept_id, rn
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

def attempt(label, sql):
    try:
        con.execute(sql).fetchall()
        print(label, "-> OK")
    except sqlite3.Error as e:
        print(label, "-> ERROR:", e)
attempt("extend a window with no ORDER BY: OVER (dept ORDER BY salary)",
        "SELECT RANK() OVER (d ORDER BY salary) FROM employees WINDOW d AS (PARTITION BY dept_id)")
attempt("override an existing ORDER BY: OVER (w ORDER BY emp_id)",
        "SELECT RANK() OVER (w ORDER BY emp_id) FROM employees WINDOW w AS (PARTITION BY dept_id ORDER BY salary)")
attempt("add PARTITION BY to a named window: OVER (w PARTITION BY dept_id)",
        "SELECT RANK() OVER (w PARTITION BY dept_id) FROM employees WINDOW w AS (ORDER BY salary)")
attempt("WINDOW clause after ORDER BY",
        "SELECT RANK() OVER w FROM employees ORDER BY emp_id WINDOW w AS (ORDER BY salary)")
attempt("WINDOW clause after GROUP BY/HAVING, before ORDER BY",
        "SELECT dept_id, RANK() OVER w FROM employees GROUP BY dept_id HAVING COUNT(*) > 0 WINDOW w AS (ORDER BY dept_id) ORDER BY dept_id")

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
s = employees.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True]).reset_index(drop=True)
g = s.groupby("dept_id")["salary"]
pd_df = s.assign(rn=s.groupby("dept_id").cumcount() + 1,
                 rk=g.rank(method="min", ascending=False).astype(int),
                 dr=g.rank(method="dense", ascending=False).astype(int),
                 dept_avg=g.transform("mean"))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
cols = ["emp_id", "name", "dept_id", "salary", "rn", "rk", "dr", "dept_avg"]
# compared in dept_id, rn order
pd.testing.assert_frame_equal(sql_df.drop(columns="avg_same_window"), pd_df[cols], check_dtype=False)
print("\nasserts passed: SQL == pandas on rn, rk, dr, dept_avg (avg_same_window is a cumulative average, not compared)")
```

**Output (my run):**
```text
SQL:
 emp_id   name  dept_id  salary  rn  rk  dr  avg_same_window  dept_avg
      1   Asha       10      90   1   1   1        90.000000 83.333333
      2    Ben       10      90   2   1   1        90.000000 83.333333
      3 Chitra       10      70   3   3   2        83.333333 83.333333
      4    Dev       20      80   1   1   1        80.000000 70.000000
      5   Esha       20      60   2   2   2        70.000000 70.000000
extend a window with no ORDER BY: OVER (dept ORDER BY salary) -> OK
override an existing ORDER BY: OVER (w ORDER BY emp_id) -> ERROR: cannot override ORDER BY clause of window: w
add PARTITION BY to a named window: OVER (w PARTITION BY dept_id) -> ERROR: cannot override PARTITION clause of window: w
WINDOW clause after ORDER BY -> ERROR: near "WINDOW": syntax error
WINDOW clause after GROUP BY/HAVING, before ORDER BY -> OK

pandas:
 emp_id   name  dept_id  salary  rn  rk  dr  dept_avg
      1   Asha       10      90   1   1   1 83.333333
      2    Ben       10      90   2   1   1 83.333333
      3 Chitra       10      70   3   3   2 83.333333
      4    Dev       20      80   1   1   1 70.000000
      5   Esha       20      60   2   2   2 70.000000

asserts passed: SQL == pandas on rn, rk, dr, dept_avg (avg_same_window is a cumulative average, not compared)
```

**Edge cases:**
- Extending: `OVER (dept ORDER BY salary)` works because `dept` has no `ORDER BY`. `OVER (w ORDER BY emp_id)` fails because `w` already has one, and `OVER (w PARTITION BY ...)` fails because partitions cannot be added (error texts above, SQLite 3.45). So the rule in my run is: you may add `ORDER BY` (and a frame) to a base that lacks them; you cannot override.
- Clause position: after `HAVING`, before `ORDER BY` works; after `ORDER BY` is a syntax error (both tried in the run).
- Ties: `RANK` and `DENSE_RANK` treat tied rows as peers; `ROW_NUMBER` needs the extra `emp_id` key.
- PostgreSQL and MySQL 8 also have the `WINDOW` clause (from memory, not executed here); the extension rules are stated in the SQL standard and I believe they are similar, but I did not test them.

**Then explain:**
- **Benefit:** one definition, so changing the partition or order in one place cannot leave a column on a different window ("no drift"), and the select list is shorter.
- **Where it sits:** `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... WINDOW ... ORDER BY ... LIMIT`.
- **pandas:** sort once, `groupby` once, then `rank(method=...)` and `transform("mean")`; the mean is the department mean (the unordered window), which the run asserts. The cumulative average has no direct single call and belongs to Part 5.

**Follow-ups:**
- *Can the same name be used in two different clauses?* Yes, any number of `OVER w`.
- *Does naming a window change performance?* Not by itself as far as I know; I did not time it.
- *Why not just repeat the clause?* It works, but it invites drift.

**Common mistakes:**
- Putting `WINDOW` after `ORDER BY`.
- Trying to override an `ORDER BY` of a named window.
- Treating `AVG(...) OVER (... ORDER BY ...)` as the group average.
- `ROW_NUMBER` with ties and no tie-break key.

### Q25 ⭐⭐ 🟡 PARTITION BY versus ORDER BY inside OVER, and the default frame basics: employees(emp_id, name, dept_id, salary). Compare SUM(salary) OVER (PARTITION BY dept_id) with SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary) and explain why the second one changes row by row (default frame RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, peers share a value) while the first is the whole partition. Show ROWS versus RANGE with two equal salaries. Keep it to the idea of a frame; running totals are Part 5. Give the pandas transform('sum') contrast.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `PARTITION BY` splits rows into groups and `SUM(...) OVER (PARTITION BY dept_id)` is the whole group's total on every row; adding `ORDER BY` inside `OVER` also sets a default frame that ends at the current row (and its peers), so the same `SUM` changes row by row, and equal salaries share one value under `RANGE` but not under `ROWS`.

**Schema and sample data:** six employees; Ben and Chitra both earn 60 in dept 10.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,60),(3,'Chitra',10,60),(4,'Dev',10,80),
  (5,'Esha',20,40),(6,'Farid',20,70);
```

**SQL answer:** `SQL_MAIN` (Code block).
```sql
SELECT emp_id, name, dept_id, salary,
       SUM(salary) OVER (PARTITION BY dept_id) AS dept_total,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary) AS sum_range,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary, emp_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sum_rows
FROM employees
ORDER BY dept_id, salary, emp_id
```

**pandas answer:** `transform("sum")` is the unordered window; `cumsum` after a sort behaves like a `ROWS` frame; taking the maximum of that within tied rows gives the `RANGE` value.
```python
s = employees.sort_values(["dept_id", "salary", "emp_id"]).reset_index(drop=True)
s["dept_total"] = s.groupby("dept_id")["salary"].transform("sum")
s["sum_rows"] = s.groupby("dept_id")["salary"].cumsum()
s["sum_range"] = s.groupby(["dept_id", "salary"])["sum_rows"].transform("max")
pd_df = s[["emp_id", "name", "dept_id", "salary", "dept_total", "sum_range", "sum_rows"]]
```

**Example:** dept 10, ordered by salary: Asha 50, Ben 60, Chitra 60, Dev 80. Dept total 250.
- `SUM OVER (PARTITION BY dept_id)`: 250 on all four rows (whole partition, no ordering involved).
- `SUM OVER (PARTITION BY dept_id ORDER BY salary)` with the default `RANGE` frame: Asha 50; Ben and Chitra are peers (same salary), so both see everything up to the last peer: 50 + 60 + 60 = 170 for both; Dev 250.
- Same with `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (ordering by `salary, emp_id` so the row order is fixed): Asha 50, Ben 110, Chitra 170, Dev 250. Only the tied pair differs from `RANGE` (110 versus 170).
- Dept 20: Esha 40 then Farid 70: total 110 on both, and 40 then 110 under both frames (no ties).

**Code:** run with `python3 -I`.
```python
# Q25: PARTITION BY versus ORDER BY inside OVER; default frame basics
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,60),(3,'Chitra',10,60),(4,'Dev',10,80),
  (5,'Esha',20,40),(6,'Farid',20,70);
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       SUM(salary) OVER (PARTITION BY dept_id) AS dept_total,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary) AS sum_range,
       SUM(salary) OVER (PARTITION BY dept_id ORDER BY salary, emp_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sum_rows
FROM employees
ORDER BY dept_id, salary, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
s = employees.sort_values(["dept_id", "salary", "emp_id"]).reset_index(drop=True)
s["dept_total"] = s.groupby("dept_id")["salary"].transform("sum")
s["sum_rows"] = s.groupby("dept_id")["salary"].cumsum()
s["sum_range"] = s.groupby(["dept_id", "salary"])["sum_rows"].transform("max")
pd_df = s[["emp_id", "name", "dept_id", "salary", "dept_total", "sum_range", "sum_rows"]]
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in dept_id, salary, emp_id order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nasserts passed: SQL == pandas (cumsum is ROWS-like; max over peers gives the RANGE value)")
```

**Output (my run):**
```text
SQL:
 emp_id   name  dept_id  salary  dept_total  sum_range  sum_rows
      1   Asha       10      50         250         50        50
      2    Ben       10      60         250        170       110
      3 Chitra       10      60         250        170       170
      4    Dev       10      80         250        250       250
      5   Esha       20      40         110         40        40
      6  Farid       20      70         110        110       110

pandas:
 emp_id   name  dept_id  salary  dept_total  sum_range  sum_rows
      1   Asha       10      50         250         50        50
      2    Ben       10      60         250        170       110
      3 Chitra       10      60         250        170       170
      4    Dev       10      80         250        250       250
      5   Esha       20      40         110         40        40
      6  Farid       20      70         110        110       110

asserts passed: SQL == pandas (cumsum is ROWS-like; max over peers gives the RANGE value)
```

**Edge cases:**
- Ties: peers share a `RANGE` value; `ROWS` depends on physical row order, so add a tie-break (`emp_id`) to make it deterministic. Without one, which of Ben and Chitra shows 110 is unspecified.
- NULL salary: `SUM` skips it, and in the ordered window SQLite sorts NULL first, so the NULL row would come first with a NULL-only partial sum if it is first. I did not run a NULL case here.
- One-row partition: the sum is just that row, under any frame.
- Without `ORDER BY`, the default frame is the whole partition, which is why the first column is a total.

**Then explain:**
- **Two jobs inside `OVER`:** `PARTITION BY` chooses which rows are in the group; `ORDER BY` chooses their order and, as a side effect, shrinks the default frame to "start through current row and peers".
- **ROWS versus RANGE:** `ROWS` counts rows; `RANGE` includes all rows whose `ORDER BY` value equals the current row's.
- **Scope:** I am only using this to explain frames. Running totals as a technique, moving averages and `LAG`/`LEAD` are Part 5.
- **pandas:** `transform("sum")` repeats the group total; `cumsum` is ROWS-like, so I take the maximum per tied salary to emulate RANGE.

**Follow-ups:**
- *Why did my share-of-total break?* An `ORDER BY` slipped into the window (Q14).
- *Can I change the frame?* Yes, with `ROWS`/`RANGE`/`GROUPS` clauses; SQLite supports all three (documented; I only ran ROWS and the default RANGE here).
- *Default frame without ORDER BY?* Whole partition.

**Common mistakes:**
- Adding `ORDER BY` to a total and getting a running sum.
- Assuming `ROWS` and `RANGE` are the same when there are ties.
- No tie-break with `ROWS`, so the output order of ties changes.

### Q26 ⭐⭐ 🟡 Top-N with ties rules: products(product_id, category, name, sales). Return the top 3 products by sales per category in three variants: exactly 3 (ROW_NUMBER with a tie-breaker), 3 including ties at the cutoff (RANK <= 3), and top 3 distinct sales values (DENSE_RANK <= 3). Show the standard FETCH FIRST n ROWS WITH TIES / WITH TIES syntax as dialect text (PostgreSQL 13+, hedged, not executed; SQLite has no WITH TIES; per-group still needs a window). Explain how to ask the interviewer which variant they want.
**Asked at:** techinterview.org window-function gotchas article (ties, RANK = 2 returning nothing, window in WHERE, default frame), a guide and not a candidate report; analyst and data scientist screens
**Say this first (1 line):** "Top 3" is ambiguous when sales tie, so I pick by the requirement: `ROW_NUMBER <= 3` with a tie-breaker for exactly 3 rows, `RANK <= 3` for 3 places plus everyone tied at the cutoff, and `DENSE_RANK <= 3` for the top 3 distinct sales values; I ask the interviewer which one they mean before writing it.

**Schema and sample data:** category A has a three-way tie at 90 right below the leader; category B has a tie for first and only four products.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, sales INTEGER);
INSERT INTO products VALUES (1,'A','P1',100),(2,'A','P2',90),(3,'A','P3',90),(4,'A','P4',90),
  (5,'A','P5',80),(6,'A','P6',70),(7,'B','P7',50),(8,'B','P8',50),(9,'B','P9',40),(10,'B','P10',30);
```

**SQL answer:** `SQL_MAIN` shows all three numberings; `SQL_EXACT`, `SQL_TIES` and `SQL_DISTINCT` are the three answers (Code block).
```sql
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC, product_id) AS rn
  FROM products)
WHERE rn <= 3
ORDER BY category, product_id
```
```sql
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rk
  FROM products)
WHERE rk <= 3
ORDER BY category, product_id
```
```sql
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dr
  FROM products)
WHERE dr <= 3
ORDER BY category, product_id
```

**pandas answer:** sort with the tie-break, then `head(3)` per group for exactly 3, and `rank` with `method="min"` / `"dense"` for the other two.
```python
s = products.sort_values(["category", "sales", "product_id"], ascending=[True, False, True])
g = s.groupby("category")["sales"]
cols = ["category", "product_id", "sales"]
pd_exact = s.groupby("category").head(3)[cols]
pd_ties = s[g.rank(method="min", ascending=False) <= 3][cols]
pd_dist = s[g.rank(method="dense", ascending=False) <= 3][cols]
```

**Example:**
- Category A sales: P1 100, P2 90, P3 90, P4 90, P5 80, P6 70. `ROW_NUMBER` (tie-break product_id): 1 to 6, so exactly 3 gives P1, P2, P3. `RANK`: 1, 2, 2, 2, 5, 6, so `rk <= 3` gives P1 to P4 (four rows). `DENSE_RANK`: 1, 2, 2, 2, 3, 4, so `dr <= 3` gives P1 to P5 (five rows).
- Category B: P7 50, P8 50, P9 40, P10 30. `ROW_NUMBER`: P7, P8, P9. `RANK`: 1, 1, 3, 4, so P7, P8, P9. `DENSE_RANK`: 1, 1, 2, 3, so all four products.
- Totals: 6, 7 and 9 rows for the three variants.

**Code:** run with `python3 -I`.
```python
# Q26: top-N with ties rules
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, sales INTEGER);
INSERT INTO products VALUES (1,'A','P1',100),(2,'A','P2',90),(3,'A','P3',90),(4,'A','P4',90),
  (5,'A','P5',80),(6,'A','P6',70),(7,'B','P7',50),(8,'B','P8',50),(9,'B','P9',40),(10,'B','P10',30);
"""
SQL_MAIN = """
SELECT category, product_id, sales, rn, rk, dr
FROM (SELECT category, product_id, sales,
             ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC, product_id) AS rn,
             RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rk,
             DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dr
      FROM products)
ORDER BY category, rn
"""
SQL_EXACT = """
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales DESC, product_id) AS rn
  FROM products)
WHERE rn <= 3
ORDER BY category, product_id
"""
SQL_TIES = """
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS rk
  FROM products)
WHERE rk <= 3
ORDER BY category, product_id
"""
SQL_DISTINCT = """
SELECT category, product_id, sales FROM (
  SELECT category, product_id, sales,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY sales DESC) AS dr
  FROM products)
WHERE dr <= 3
ORDER BY category, product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("All ranks:"); print(pd.read_sql_query(SQL_MAIN, con).to_string(index=False))
exact = pd.read_sql_query(SQL_EXACT, con)
ties = pd.read_sql_query(SQL_TIES, con)
dist = pd.read_sql_query(SQL_DISTINCT, con)
for label, d in (("exactly 3 (ROW_NUMBER)", exact), ("3 including ties (RANK <= 3)", ties), ("top 3 distinct values (DENSE_RANK <= 3)", dist)):
    print("\n" + label + ":", len(d), "rows"); print(d.to_string(index=False))
try:
    con.execute("SELECT product_id FROM products ORDER BY sales DESC FETCH FIRST 3 ROWS WITH TIES").fetchall()
except sqlite3.Error as e:
    print("\nFETCH FIRST ... WITH TIES on SQLite 3.45:", e)

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
s = products.sort_values(["category", "sales", "product_id"], ascending=[True, False, True])
g = s.groupby("category")["sales"]
cols = ["category", "product_id", "sales"]
pd_exact = s.groupby("category").head(3)[cols]
pd_ties = s[g.rank(method="min", ascending=False) <= 3][cols]
pd_dist = s[g.rank(method="dense", ascending=False) <= 3][cols]
# pd:end
# compared in category, product_id order
for a, b in ((exact, pd_exact), (ties, pd_ties), (dist, pd_dist)):
    pd.testing.assert_frame_equal(a, b.sort_values(["category", "product_id"]).reset_index(drop=True), check_dtype=False)
print("\nrow counts:", len(pd_exact), len(pd_ties), len(pd_dist))
print("asserts passed: all three SQL variants == pandas")
```

**Output (my run):**
```text
All ranks:
category  product_id  sales  rn  rk  dr
       A           1    100   1   1   1
       A           2     90   2   2   2
       A           3     90   3   2   2
       A           4     90   4   2   2
       A           5     80   5   5   3
       A           6     70   6   6   4
       B           7     50   1   1   1
       B           8     50   2   1   1
       B           9     40   3   3   2
       B          10     30   4   4   3

exactly 3 (ROW_NUMBER): 6 rows
category  product_id  sales
       A           1    100
       A           2     90
       A           3     90
       B           7     50
       B           8     50
       B           9     40

3 including ties (RANK <= 3): 7 rows
category  product_id  sales
       A           1    100
       A           2     90
       A           3     90
       A           4     90
       B           7     50
       B           8     50
       B           9     40

top 3 distinct values (DENSE_RANK <= 3): 9 rows
category  product_id  sales
       A           1    100
       A           2     90
       A           3     90
       A           4     90
       A           5     80
       B           7     50
       B           8     50
       B           9     40
       B          10     30

FETCH FIRST ... WITH TIES on SQLite 3.45: near "FETCH": syntax error

row counts: 6 7 9
asserts passed: all three SQL variants == pandas
```

**Edge cases:**
- Fewer than 3 products in a category: all of them are returned in every variant.
- Ties at the cutoff: only `ROW_NUMBER` cuts through a tie, and it does so by the tie-breaker I choose (lowest product_id), which drops P4 from A even though it sold as much as P2 and P3.
- NULL sales: SQLite sorts NULL last under `DESC`, so NULL rows rank last but can still enter the top 3 in a small category; filter `sales IS NOT NULL` if they should not.
- Dialect text, not executed here: PostgreSQL 13+ supports `FETCH FIRST 3 ROWS WITH TIES` (the `ORDER BY` must precede it), and MySQL has no `WITH TIES`. SQLite 3.45 rejects it (the run prints the syntax error). Even where it exists it limits the whole result, not each group, so per-category top 3 with ties still needs a window or a lateral join.

**Then explain:**
- **Which variant, in interview terms:** I ask "if two products tie for third, do you want both, or exactly three?" and "is it the top three products or the top three sales values?" Then I state my tie-break aloud for the exactly-3 case.
- **Why filter outside:** windows cannot appear in `WHERE`, so the number is computed in a subquery and filtered outside (Q3).
- **pandas:** `groupby().head(3)` is the `ROW_NUMBER` answer only after sorting with a tie-break; `rank` with `min` and `dense` give the others. All three match SQL in the run.
- **Ordering of output:** I order by category and product_id before comparing, since the variants return different row counts.

**Follow-ups:**
- *`QUALIFY`?* Snowflake, BigQuery and Teradata let you filter window results directly (from memory, not executed here); SQLite does not.
- *Top 3 overall, not per group?* Drop `PARTITION BY` (or `LIMIT 3` with a tie-break).
- *Performance?* The window sorts each partition; an index on (category, sales) may help, but I did not test it here.

**Common mistakes:**
- Using `ROW_NUMBER` with no tie-break and calling the result "the top 3".
- Using `RANK <= 3` and being surprised by four or more rows.
- Using `DENSE_RANK` when the business means "3 products".
- Assuming `WITH TIES` is per group.
