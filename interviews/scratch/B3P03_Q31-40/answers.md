### Q31 ⭐ 🟡 Correlated subqueries in the SELECT list: orders(order_id, customer_id, order_date, amount). For every order, show the customer's number of orders, the customer's average order amount and how far this order is from that average, each as a correlated scalar subquery. Explain the per-row evaluation, rewrite it as one join to a derived table of per-customer count and average, confirm the results match, and give pandas groupby transform('count') and transform('mean').
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** A correlated scalar subquery in the SELECT list is a small query that is re-run for every outer row using that row's `customer_id`; the same numbers come from one join to a derived table that computes count and average once per customer, and in pandas that is `groupby(...).transform('count')` and `transform('mean')`.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',100),(2,1,'2024-01-20',200),(3,1,'2024-02-02',300),
 (4,2,'2024-01-10',50),(5,2,'2024-03-01',150),
 (6,3,'2024-02-14',80),(7,3,'2024-02-20',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block (three correlated scalar subqueries; the difference column reuses the average subquery).
```sql
SELECT o.order_id, o.customer_id, o.amount,
       (SELECT COUNT(*) FROM orders i WHERE i.customer_id = o.customer_id) AS n_orders,
       (SELECT AVG(i.amount) FROM orders i WHERE i.customer_id = o.customer_id) AS avg_amount,
       o.amount - (SELECT AVG(i.amount) FROM orders i WHERE i.customer_id = o.customer_id) AS diff_from_avg
FROM orders o
ORDER BY o.order_id
```
The rewrite, `SQL_JOIN` in the Code block, run next to it:
```sql
SELECT o.order_id, o.customer_id, o.amount,
       s.n_orders, s.avg_amount, o.amount - s.avg_amount AS diff_from_avg
FROM orders o
JOIN (SELECT customer_id, COUNT(*) AS n_orders, AVG(amount) AS avg_amount
      FROM orders GROUP BY customer_id) s ON s.customer_id = o.customer_id
ORDER BY o.order_id
```

**pandas answer:** (same text as in the Code block)
```py
g = orders.groupby("customer_id")
pd_df = orders.assign(
    n_orders=g["order_id"].transform("count"),
    avg_amount=g["amount"].transform("mean"),
)
pd_df["diff_from_avg"] = pd_df["amount"] - pd_df["avg_amount"]
pd_df = pd_df[["order_id", "customer_id", "amount", "n_orders", "avg_amount", "diff_from_avg"]].sort_values("order_id").reset_index(drop=True)
```

**Example:** Customer 1 has orders 100, 200, 300; customer 2 has 50, 150; customer 3 has 80 and one order with a NULL amount.
- Order 1: the subquery looks at the three rows of customer 1: count 3, average 200, so the difference is 100 - 200 = -100. Orders 2 and 3 give 0 and +100.
- Customer 2: count 2, average 100, differences -50 and +50.
- Customer 3: `COUNT(*)` is 2 (it counts rows), `AVG(amount)` is 80 (it ignores the NULL), so order 6 has difference 0 and order 7 has difference NULL (NULL minus anything is NULL).
- The join version builds one row per customer (1: 3 and 200, 2: 2 and 100, 3: 2 and 80) and attaches it to each order, so every order gets the same three numbers.

**Code:** run with `python3 -I`.
```python
# Q31: correlated scalar subqueries in the SELECT list vs one join to a derived table; pandas transform
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',100),(2,1,'2024-01-20',200),(3,1,'2024-02-02',300),
 (4,2,'2024-01-10',50),(5,2,'2024-03-01',150),
 (6,3,'2024-02-14',80),(7,3,'2024-02-20',NULL);
"""
SQL_MAIN = """
SELECT o.order_id, o.customer_id, o.amount,
       (SELECT COUNT(*) FROM orders i WHERE i.customer_id = o.customer_id) AS n_orders,
       (SELECT AVG(i.amount) FROM orders i WHERE i.customer_id = o.customer_id) AS avg_amount,
       o.amount - (SELECT AVG(i.amount) FROM orders i WHERE i.customer_id = o.customer_id) AS diff_from_avg
FROM orders o
ORDER BY o.order_id
"""
SQL_JOIN = """
SELECT o.order_id, o.customer_id, o.amount,
       s.n_orders, s.avg_amount, o.amount - s.avg_amount AS diff_from_avg
FROM orders o
JOIN (SELECT customer_id, COUNT(*) AS n_orders, AVG(amount) AS avg_amount
      FROM orders GROUP BY customer_id) s ON s.customer_id = o.customer_id
ORDER BY o.order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
join_df = pd.read_sql_query(SQL_JOIN, con)
print("SQL correlated scalar subqueries:")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, join_df)
print("\nassert: correlated version == derived-table join (same rows, ordered by order_id)")

print("\nEXPLAIN QUERY PLAN, correlated version:")
for r in con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN):
    print("  ", r[3])
print("EXPLAIN QUERY PLAN, join version:")
for r in con.execute("EXPLAIN QUERY PLAN " + SQL_JOIN):
    print("  ", r[3])

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
g = orders.groupby("customer_id")
pd_df = orders.assign(
    n_orders=g["order_id"].transform("count"),
    avg_amount=g["amount"].transform("mean"),
)
pd_df["diff_from_avg"] = pd_df["amount"] - pd_df["avg_amount"]
pd_df = pd_df[["order_id", "customer_id", "amount", "n_orders", "avg_amount", "diff_from_avg"]].sort_values("order_id").reset_index(drop=True)
# pd:end
print("\npandas transform:")
print(pd_df.to_string(index=False))
# compared after sorting by order_id; amount is float in pandas because of the NULL
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nassert: SQL == pandas")
print("transform('count') on amount instead of order_id, customer 3:",
      g["amount"].transform("count")[orders.customer_id == 3].tolist(), "(NULL amount not counted; COUNT(*) gives 2)")
print("SQL COUNT(amount) for customer 3:", con.execute("SELECT COUNT(amount) FROM orders WHERE customer_id=3").fetchone()[0])

# an order with a NULL customer_id: correlation '=' never matches it
con.execute("INSERT INTO orders VALUES (8, NULL, '2024-03-05', 40)")
c_df = pd.read_sql_query(SQL_MAIN, con)
j_df = pd.read_sql_query(SQL_JOIN, con)
print("\nafter adding order 8 with customer_id NULL:")
print("correlated row for order 8:", c_df[c_df.order_id == 8][["n_orders", "avg_amount"]].values.tolist(), "(COUNT(*) is 0, AVG is NULL)")
print("rows: correlated", len(c_df), "| INNER JOIN to derived table", len(j_df), "(order 8 is dropped)")
orders2 = pd.read_sql_query("SELECT * FROM orders", con)
tc = orders2.groupby("customer_id")["order_id"].transform("count")
print("pandas transform('count') for order 8:", tc[orders2.order_id == 8].tolist(), "(NaN key, so NaN; SQL gives 0)")
```

**Output (my run):**
```text
SQL correlated scalar subqueries:
 order_id  customer_id  amount  n_orders  avg_amount  diff_from_avg
        1            1   100.0         3       200.0         -100.0
        2            1   200.0         3       200.0            0.0
        3            1   300.0         3       200.0          100.0
        4            2    50.0         2       100.0          -50.0
        5            2   150.0         2       100.0           50.0
        6            3    80.0         2        80.0            0.0
        7            3     NaN         2        80.0            NaN

assert: correlated version == derived-table join (same rows, ordered by order_id)

EXPLAIN QUERY PLAN, correlated version:
   SCAN o
   CORRELATED SCALAR SUBQUERY 1
   SCAN i
   CORRELATED SCALAR SUBQUERY 2
   SCAN i
   CORRELATED SCALAR SUBQUERY 3
   SCAN i
EXPLAIN QUERY PLAN, join version:
   CO-ROUTINE s
   SCAN orders
   USE TEMP B-TREE FOR GROUP BY
   SCAN o
   BLOOM FILTER ON s (customer_id=?)
   SEARCH s USING AUTOMATIC COVERING INDEX (customer_id=?)

pandas transform:
 order_id  customer_id  amount  n_orders  avg_amount  diff_from_avg
        1            1   100.0         3       200.0         -100.0
        2            1   200.0         3       200.0            0.0
        3            1   300.0         3       200.0          100.0
        4            2    50.0         2       100.0          -50.0
        5            2   150.0         2       100.0           50.0
        6            3    80.0         2        80.0            0.0
        7            3     NaN         2        80.0            NaN

assert: SQL == pandas
transform('count') on amount instead of order_id, customer 3: [1, 1] (NULL amount not counted; COUNT(*) gives 2)
SQL COUNT(amount) for customer 3: 1

after adding order 8 with customer_id NULL:
correlated row for order 8: [[0.0, nan]] (COUNT(*) is 0, AVG is NULL)
rows: correlated 8 | INNER JOIN to derived table 7 (order 8 is dropped)
pandas transform('count') for order 8: [nan] (NaN key, so NaN; SQL gives 0)
```

**Edge cases:**
- NULL amount: `COUNT(*)` counts the row, `COUNT(amount)` and pandas `transform('count')` on `amount` do not (customer 3 shows 2 versus 1 in my run). I counted `order_id` in pandas to match `COUNT(*)`; use `transform('size')` if the column can be NULL.
- NULL `customer_id`: `i.customer_id = o.customer_id` is never true, so the correlated version gives count 0 and average NULL for that order, but still returns the row. The INNER JOIN to the derived table silently drops it (8 rows versus 7 in my run); use a LEFT JOIN if you need it. pandas `groupby` drops NaN keys, so `transform` gives NaN there, not 0.
- A customer with a single order: average is that amount and the difference is 0. Customers with no orders never appear, because the outer table is `orders`.
- Float versus integer: `AVG` returns a float, so differences are floats; the pandas frame is compared with `check_dtype=False` because the NULL turns `amount` into float.

**Then explain:**
- **Per-row evaluation:** for each row of `orders` the engine runs each inner query with `o.customer_id` plugged in. Three subqueries means three inner scans per outer row in the naive model. The SQLite plan shows `CORRELATED SCALAR SUBQUERY 1`, `2` and `3`, each with its own `SCAN i`.
- **The join form:** the derived table is computed once (group by customer), then joined. SQLite's plan shows a co-routine for it and an automatic covering index on `customer_id`. Optimisers in other engines may also rewrite a correlated subquery into a join; that varies by engine and version, not executed here.
- **Readability:** the correlated form says exactly what each column means and keeps one row per order with no join to fan out; the join form is the one to reach for when there are many such columns or the table is large.
- **Better still:** the per-row average next to the row is a window function (`AVG(amount) OVER (PARTITION BY customer_id)`), which is Part 4; interviewers often ask for the subquery form first and the window form second.
- **pandas:** `transform` returns a result with the same index as the input, so it lines up with the original rows, which is the exact analogue of a correlated scalar subquery. `agg` returns one row per group and needs a merge back.

**Follow-ups:**
- *Why not one subquery returning both count and average?* A scalar subquery returns one column. Use the derived-table join, or row values in engines that support them.
- *Does the optimiser always run it per row?* Not necessarily; the per-row model is the mental model. In SQLite 3.45 the plan shows it as a correlated subquery and I did not time it here.
- *How would you index it?* An index on `orders(customer_id)` helps the inner lookups (see Q39 for a measured comparison).

**Common mistakes:**
- Forgetting the correlation condition, so every row shows the global count and average.
- Mixing `COUNT(*)` and `COUNT(amount)` and not noticing NULLs.
- Using an INNER JOIN to the derived table and losing orders whose key does not match.
- Writing `o.amount - AVG(...)` in the outer query without a subquery or GROUP BY.
- In pandas, using `groupby().mean()` (one row per group) where `transform('mean')` was needed.

### Q32 ⭐ 🟡 Reusing one CTE twice in a query: sales(sale_id, region, amount). Define regional totals once in a CTE, then return regions whose total is above the average of regional totals and also show the best region's total, referencing the CTE several times. Explain that a derived table cannot be named and reused (MySQL's CTE page says a derived table is derived again for each reference), how engines may inline or materialise a multiply-referenced CTE (hedged: PostgreSQL materialises by default when referenced more than once, SQLite chooses itself), and the pandas intermediate variable.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** A CTE gives a query a name once and lets me reference it as many times as I like (here four times), whereas a derived table has no name outside its own FROM clause, so reusing it means pasting the whole subquery again; in pandas the "CTE" is simply an intermediate DataFrame variable.

**Schema and sample data:**
```sql
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,'North',100),(2,'North',50),(3,'South',80),(4,'East',200),
 (5,'West',40),(6,'West',20),(7,'West',10);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH region_totals AS (
  SELECT region, SUM(amount) AS total FROM sales GROUP BY region
)
SELECT region, total,
       (SELECT AVG(total) FROM region_totals) AS avg_total,
       (SELECT MAX(total) FROM region_totals) AS best_total
FROM region_totals
WHERE total > (SELECT AVG(total) FROM region_totals)
ORDER BY total DESC, region
```
The no-CTE version, `SQL_DERIVED` in the Code block, repeats `(SELECT region, SUM(amount) AS total FROM sales GROUP BY region)` four times (once in FROM, three times in scalar subqueries); the Code block asserts the two give the same rows.

**pandas answer:** (same text as in the Code block)
```py
region_totals = sales.groupby("region", as_index=False).agg(total=("amount", "sum"))
avg_total = region_totals["total"].mean()
best_total = region_totals["total"].max()
pd_df = (region_totals[region_totals["total"] > avg_total]
         .assign(avg_total=avg_total, best_total=best_total)
         .sort_values(["total", "region"], ascending=[False, True])
         .reset_index(drop=True))
```

**Example:** Totals by region: North 100 + 50 = 150, South 80, East 200, West 40 + 20 + 10 = 70.
- Average of the four totals: (150 + 80 + 200 + 70) / 4 = 125. Best total: 200.
- Regions above 125: East (200) and North (150). Each row also carries `avg_total` 125.0 and `best_total` 200.
- Note it is the average of regional totals (125), not the average sale amount, which would be 500 / 7 = 71.4; that is the trap in this question.

**Code:** run with `python3 -I`.
```python
# Q32: one CTE referenced several times vs the same derived table repeated; MATERIALIZED hints; pandas intermediate
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,'North',100),(2,'North',50),(3,'South',80),(4,'East',200),
 (5,'West',40),(6,'West',20),(7,'West',10);
"""
SQL_MAIN = """
WITH region_totals AS (
  SELECT region, SUM(amount) AS total FROM sales GROUP BY region
)
SELECT region, total,
       (SELECT AVG(total) FROM region_totals) AS avg_total,
       (SELECT MAX(total) FROM region_totals) AS best_total
FROM region_totals
WHERE total > (SELECT AVG(total) FROM region_totals)
ORDER BY total DESC, region
"""
SQL_DERIVED = """
SELECT t.region, t.total,
       (SELECT AVG(total) FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region)) AS avg_total,
       (SELECT MAX(total) FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region)) AS best_total
FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region) t
WHERE t.total > (SELECT AVG(total) FROM (SELECT region, SUM(amount) AS total FROM sales GROUP BY region))
ORDER BY t.total DESC, t.region
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL with one CTE referenced 4 times:")
print(sql_df.to_string(index=False))
der_df = pd.read_sql_query(SQL_DERIVED, con)
pd.testing.assert_frame_equal(sql_df, der_df)
print("\nassert: CTE version == derived table written out 4 times (same rows, same order)")

print("\nEXPLAIN QUERY PLAN, CTE version:")
for r in con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN):
    print("  ", r[3])
for hint in ["MATERIALIZED", "NOT MATERIALIZED"]:
    q = SQL_MAIN.replace("AS (\n  SELECT region", "AS %s (\n  SELECT region" % hint)
    assert hint in q
    res = con.execute(q).fetchall()
    plan = [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q)]
    print("\n%s hint parses on SQLite 3.45: rows=%s" % (hint, res))
    print("   plan:", plan)

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
region_totals = sales.groupby("region", as_index=False).agg(total=("amount", "sum"))
avg_total = region_totals["total"].mean()
best_total = region_totals["total"].max()
pd_df = (region_totals[region_totals["total"] > avg_total]
         .assign(avg_total=avg_total, best_total=best_total)
         .sort_values(["total", "region"], ascending=[False, True])
         .reset_index(drop=True))
# pd:end
print("\npandas:")
print(pd_df.to_string(index=False))
# compared in the printed order (total DESC, region)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nassert: SQL == pandas")
print("all region totals:", dict(zip(region_totals.region, region_totals.total)), "| average", avg_total)
```

**Output (my run):**
```text
SQL with one CTE referenced 4 times:
region  total  avg_total  best_total
  East    200      125.0         200
 North    150      125.0         200

assert: CTE version == derived table written out 4 times (same rows, same order)

EXPLAIN QUERY PLAN, CTE version:
   MATERIALIZE region_totals
   SCAN sales
   USE TEMP B-TREE FOR GROUP BY
   SCAN region_totals
   SCALAR SUBQUERY 4
   SCAN region_totals
   SCALAR SUBQUERY 2
   SCAN region_totals
   SCALAR SUBQUERY 3
   SEARCH region_totals
   USE TEMP B-TREE FOR ORDER BY

MATERIALIZED hint parses on SQLite 3.45: rows=[('East', 200, 125.0, 200), ('North', 150, 125.0, 200)]
   plan: ['MATERIALIZE region_totals', 'SCAN sales', 'USE TEMP B-TREE FOR GROUP BY', 'SCAN region_totals', 'SCALAR SUBQUERY 4', 'SCAN region_totals', 'SCALAR SUBQUERY 2', 'SCAN region_totals', 'SCALAR SUBQUERY 3', 'SEARCH region_totals', 'USE TEMP B-TREE FOR ORDER BY']

NOT MATERIALIZED hint parses on SQLite 3.45: rows=[('East', 200, 125.0, 200), ('North', 150, 125.0, 200)]
   plan: ['CO-ROUTINE region_totals', 'SCAN sales', 'USE TEMP B-TREE FOR GROUP BY', 'SCAN region_totals', 'SCALAR SUBQUERY 4', 'CO-ROUTINE region_totals', 'SCAN sales', 'USE TEMP B-TREE FOR GROUP BY', 'SCAN region_totals', 'SCALAR SUBQUERY 2', 'CO-ROUTINE region_totals', 'SCAN sales', 'USE TEMP B-TREE FOR GROUP BY', 'SCAN region_totals', 'SCALAR SUBQUERY 3', 'CO-ROUTINE region_totals', 'SCAN sales', 'USE TEMP B-TREE FOR GROUP BY', 'SEARCH region_totals', 'USE TEMP B-TREE FOR ORDER BY']

pandas:
region  total  avg_total  best_total
  East    200      125.0         200
 North    150      125.0         200

assert: SQL == pandas
all region totals: {'East': 200, 'North': 150, 'South': 80, 'West': 70} | average 125.0
```

**Edge cases:**
- Average of totals versus average of rows: they differ whenever regions have different numbers of rows. Say which one is wanted.
- Ties for the best region: `MAX(total)` is a single number, so ties do not matter here; if the question asked for the best region's name, ties would return several rows (Part 4 has the ranking forms).
- NULL region: `GROUP BY region` forms one NULL group, which then counts as a "region" in the average. NULL amounts are skipped by `SUM`; a group whose amounts are all NULL has total NULL and is skipped by `AVG`.
- Empty `sales`: the CTE has no rows, so the query returns no rows; the scalar subqueries over it would be NULL.

**Then explain:**
- **Reuse:** the CTE is defined once and referenced four times. A derived table exists only inside the FROM clause that declares it, so I had to write it out four times in `SQL_DERIVED`. In my run, using the name outside its scope fails with `no such table` (see Q40). MySQL's documentation states the same point: a derived table is derived again for each reference (as summarised from the page; I did not run MySQL).
- **What the engine does:** it may inline the CTE text at each use, or compute it once and keep the result. SQLite 3.45 chose to materialise it when referenced several times: the plan printed `MATERIALIZE region_totals` once. With the `NOT MATERIALIZED` hint the same plan repeated the `SCAN sales` and `GROUP BY` for every reference, so the hint did change the plan; the rows were identical. Both hints parsed and ran on SQLite 3.45.
- **Other engines (not executed here):** PostgreSQL's documentation says a CTE referenced once is inlined by default and one referenced more than once is materialised (the version that introduced inlining is not stated on the page I read; I recall 12, treat as unverified); both hints exist there. MySQL 8.x has CTEs but, as far as I know, no materialisation hint. Check each engine's manual.
- **Readability:** naming the intermediate result and giving it a business name beats a four-times-pasted subquery, and one edit fixes all uses.
- **pandas:** `region_totals` is a variable; `avg_total` and `best_total` are scalars computed once and broadcast with `assign`. Nothing is recomputed, which is the behaviour a materialised CTE gives you.
- **Not the same as a view or temp table:** a CTE lives for one statement only.

**Follow-ups:**
- *Is a CTE faster than a subquery?* Not by definition; it is mostly a readability tool. Speed depends on whether the engine inlines or materialises it, so check the plan (Part 11).
- *Can one CTE refer to another?* Yes, in one `WITH` separated by commas; Q40 shows what SQLite accepts about order.
- *How would you get the region names above average without the extra columns?* Drop the two scalar columns; the filter alone is `WHERE total > (SELECT AVG(total) FROM region_totals)`.

**Common mistakes:**
- Averaging raw rows when the question says "average of regional totals".
- Writing the CTE and referencing it once and calling that reuse.
- Assuming a CTE is always materialised (or always inlined); it depends on the engine and version.
- Putting `WITH` in the middle of a statement; it starts the statement (or, in SQLite, follows `INSERT INTO t`, shown in Q40).
- In pandas, recomputing the groupby inside every expression.

### Q33 ⭐ 🟡 NaN and NULL pitfalls on the pandas side of subquery logic: a frame with NaN salaries and NaN department keys. Show that df[df.salary > df.salary.mean()] drops NaN rows, that == np.nan is never true, that isin treats NaN as a value, that groupby(...).transform('mean') gives NaN for NaN group keys unless dropna=False, that sum of an all-NaN group is 0 unless min_count=1, and the SQL counterparts (NULL comparisons, IN, GROUP BY puts NULLs in one group). Ask what a candidate should state about NULL handling before answering any subquery question.
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** pandas skips NaN in aggregates and drops NaN rows from comparisons like SQL does, but it differs from SQL in three places: `isin` matches NaN with NaN, `groupby(...).sum()` of an all-NaN group is 0 (SQL gives NULL), and a NaN group key is dropped by default (SQL keeps one NULL group); before any subquery answer I state how NULLs behave in the columns involved.

**Schema and sample data:**
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER);
INSERT INTO emp VALUES
 (1,'A',100),(2,'A',200),(3,'B',NULL),(4,'B',NULL),
 (5,NULL,300),(6,NULL,50),(7,'C',150);
```

**SQL answer:** `SQL_MAIN` in the Code block: a department average where the correlation is NULL-safe (`IS`), so rows with a NULL department get the average of the NULL-department group. The other SQL counterparts are the one-line queries printed in the Code block.
```sql
SELECT o.emp_id, o.dept, o.salary,
       (SELECT AVG(i.salary) FROM emp i WHERE i.dept IS o.dept) AS dept_avg
FROM emp o
ORDER BY o.emp_id
```

**pandas answer:** (same text as in the Code block)
```py
pd_df = emp.assign(dept_avg=emp.groupby("dept", dropna=False)["salary"].transform("mean"))
```

**Example:** Seven employees: A has 100 and 200; B has two NULL salaries; two employees have a NULL department (300 and 50); C has 150.
- Overall average: (100 + 200 + 300 + 50 + 150) / 5 = 160, because the two NaN salaries are skipped. `salary > 160` keeps 200 and 300. The two NaN-salary rows compare as False (pandas) or unknown (SQL) and drop out. Count: 2 in pandas and in SQL.
- `salary == np.nan` is False for every row (0 matches), as `salary = NULL` is never true in SQL (0 rows); the right tests are `isna()` and `IS NULL` (2 rows each).
- `isin([100, np.nan])` matches 3 rows: the 100 and the two NaN. SQL `salary IN (100, NULL)` matches 1 row, because comparing with NULL is unknown.
- Department averages with `dropna=False`: A gives 150, B gives NaN (nothing to average), the NULL-department group gives (300 + 50) / 2 = 175, C gives 150. The default `groupby("dept")` gives NaN for the two NULL-department rows, as the SQL `=` correlation does (both printed in my run).
- Sum of B: all NaN. SQL `SUM` gives NULL; pandas gives 0.0 unless `min_count=1`, which gives NaN. SQLite's `TOTAL()` gives 0.0 like pandas.

**Code:** run with `python3 -I`.
```python
# Q33: NaN / NULL pitfalls: pandas vs SQL for the same subquery-style logic
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER);
INSERT INTO emp VALUES
 (1,'A',100),(2,'A',200),(3,'B',NULL),(4,'B',NULL),
 (5,NULL,300),(6,NULL,50),(7,'C',150);
"""
# NULL-safe correlation with IS (SQLite); standard SQL spells it IS NOT DISTINCT FROM (not executed here)
SQL_MAIN = """
SELECT o.emp_id, o.dept, o.salary,
       (SELECT AVG(i.salary) FROM emp i WHERE i.dept IS o.dept) AS dept_avg
FROM emp o
ORDER BY o.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
emp = pd.read_sql_query("SELECT * FROM emp", con)
print("emp (NULL shows as NaN / None in pandas):")
print(emp.to_string(index=False))
print("\nSQL: department average with a NULL-safe correlation (IS):")
print(sql_df.to_string(index=False))

# pd:main
pd_df = emp.assign(dept_avg=emp.groupby("dept", dropna=False)["salary"].transform("mean"))
# pd:end
print("\npandas transform('mean') with dropna=False:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("assert: SQL (IS correlation) == pandas (dropna=False); compared by emp_id")

print("\n--- the plain '=' correlation and the default groupby ---")
eq = pd.read_sql_query("SELECT o.emp_id, (SELECT AVG(i.salary) FROM emp i WHERE i.dept = o.dept) AS dept_avg FROM emp o ORDER BY o.emp_id", con)
dflt = emp.groupby("dept")["salary"].transform("mean")
print("SQL with '=':           ", eq["dept_avg"].tolist())
print("pandas default dropna: ", dflt.tolist())
print("NaN-key rows are NaN in both (emp 5, 6):", bool(np.isnan(eq["dept_avg"][[4, 5]]).all()), bool(dflt[[4, 5]].isna().all()))

print("\n--- salary > average ---")
n_sql = con.execute("SELECT COUNT(*) FROM emp WHERE salary > (SELECT AVG(salary) FROM emp)").fetchone()[0]
mean = emp.salary.mean()
print("mean skips NaN:", mean, "| SQL AVG:", con.execute("SELECT AVG(salary) FROM emp").fetchone()[0])
print("rows with salary > mean: pandas", int((emp.salary > mean).sum()), "| SQL", n_sql, "| NaN-salary rows among them:", int((emp.salary.isna() & (emp.salary > mean)).sum()), "of", int(emp.salary.isna().sum()), "NaN rows (all dropped)")
assert int((emp.salary > mean).sum()) == n_sql

print("\n--- equality with NaN / NULL ---")
print("pandas (salary == np.nan).sum():", int((emp.salary == np.nan).sum()))
print("SQL salary = NULL rows:", con.execute("SELECT COUNT(*) FROM emp WHERE salary = NULL").fetchone()[0],
      "| salary IS NULL rows:", con.execute("SELECT COUNT(*) FROM emp WHERE salary IS NULL").fetchone()[0],
      "| pandas isna:", int(emp.salary.isna().sum()))

print("\n--- IN / isin with NaN ---")
print("pandas salary.isin([np.nan]).sum():", int(emp.salary.isin([np.nan]).sum()), "(NaN matches NaN)")
print("pandas salary.isin([100, np.nan]).sum():", int(emp.salary.isin([100, np.nan]).sum()))
print("SQL salary IN (100, NULL):", con.execute("SELECT COUNT(*) FROM emp WHERE salary IN (100, NULL)").fetchone()[0], "(NULL never matches)")
print("SQL salary IN (NULL):", con.execute("SELECT COUNT(*) FROM emp WHERE salary IN (NULL)").fetchone()[0])
print("SQL NOT IN with a NULL in the list:", con.execute("SELECT COUNT(*) FROM emp WHERE emp_id NOT IN (SELECT salary FROM emp WHERE dept='B')").fetchone()[0],
      "(subquery returns NULLs)")
print("pandas ~isin of the same values:", int((~emp.emp_id.isin(emp.loc[emp.dept == "B", "salary"])).sum()), "(all 7 rows)")

print("\n--- GROUP BY and NaN group keys ---")
print("SQL GROUP BY dept:", con.execute("SELECT dept, COUNT(*), AVG(salary) FROM emp GROUP BY dept ORDER BY dept").fetchall())
print("pandas groupby default groups:", emp.groupby("dept")["salary"].size().to_dict())
print("pandas groupby dropna=False groups:", emp.groupby("dept", dropna=False)["salary"].size().to_dict())

print("\n--- sum of an all-NaN group ---")
print("SQL SUM per dept:", con.execute("SELECT dept, SUM(salary), TOTAL(salary) FROM emp WHERE dept IS NOT NULL GROUP BY dept ORDER BY dept").fetchall())
print("pandas sum:          ", emp.groupby("dept")["salary"].sum().to_dict())
print("pandas sum min_count=1:", emp.groupby("dept")["salary"].sum(min_count=1).to_dict())
print("pandas Series([nan]).sum():", pd.Series([np.nan]).sum(), "| min_count=1:", pd.Series([np.nan]).sum(min_count=1))
sql_sum = pd.read_sql_query("SELECT dept, SUM(salary) AS s FROM emp WHERE dept IS NOT NULL GROUP BY dept ORDER BY dept", con).set_index("dept")["s"]
pd.testing.assert_series_equal(sql_sum, emp.groupby("dept")["salary"].sum(min_count=1).rename("s"), check_dtype=False)
print("assert: SQL SUM == pandas sum(min_count=1)")
```

**Output (my run):**
```text
emp (NULL shows as NaN / None in pandas):
 emp_id dept  salary
      1    A   100.0
      2    A   200.0
      3    B     NaN
      4    B     NaN
      5  NaN   300.0
      6  NaN    50.0
      7    C   150.0

SQL: department average with a NULL-safe correlation (IS):
 emp_id dept  salary  dept_avg
      1    A   100.0     150.0
      2    A   200.0     150.0
      3    B     NaN       NaN
      4    B     NaN       NaN
      5  NaN   300.0     175.0
      6  NaN    50.0     175.0
      7    C   150.0     150.0

pandas transform('mean') with dropna=False:
 emp_id dept  salary  dept_avg
      1    A   100.0     150.0
      2    A   200.0     150.0
      3    B     NaN       NaN
      4    B     NaN       NaN
      5  NaN   300.0     175.0
      6  NaN    50.0     175.0
      7    C   150.0     150.0
assert: SQL (IS correlation) == pandas (dropna=False); compared by emp_id

--- the plain '=' correlation and the default groupby ---
SQL with '=':            [150.0, 150.0, nan, nan, nan, nan, 150.0]
pandas default dropna:  [150.0, 150.0, nan, nan, nan, nan, 150.0]
NaN-key rows are NaN in both (emp 5, 6): True True

--- salary > average ---
mean skips NaN: 160.0 | SQL AVG: 160.0
rows with salary > mean: pandas 2 | SQL 2 | NaN-salary rows among them: 0 of 2 NaN rows (all dropped)

--- equality with NaN / NULL ---
pandas (salary == np.nan).sum(): 0
SQL salary = NULL rows: 0 | salary IS NULL rows: 2 | pandas isna: 2

--- IN / isin with NaN ---
pandas salary.isin([np.nan]).sum(): 2 (NaN matches NaN)
pandas salary.isin([100, np.nan]).sum(): 3
SQL salary IN (100, NULL): 1 (NULL never matches)
SQL salary IN (NULL): 0
SQL NOT IN with a NULL in the list: 0 (subquery returns NULLs)
pandas ~isin of the same values: 7 (all 7 rows)

--- GROUP BY and NaN group keys ---
SQL GROUP BY dept: [(None, 2, 175.0), ('A', 2, 150.0), ('B', 2, None), ('C', 1, 150.0)]
pandas groupby default groups: {'A': 2, 'B': 2, 'C': 1}
pandas groupby dropna=False groups: {'A': 2, 'B': 2, 'C': 1, nan: 2}

--- sum of an all-NaN group ---
SQL SUM per dept: [('A', 300, 300.0), ('B', None, 0.0), ('C', 150, 150.0)]
pandas sum:           {'A': 300.0, 'B': 0.0, 'C': 150.0}
pandas sum min_count=1: {'A': 300.0, 'B': nan, 'C': 150.0}
pandas Series([nan]).sum(): 0.0 | min_count=1: nan
assert: SQL SUM == pandas sum(min_count=1)
```

**Edge cases:**
- `NOT IN` with a NULL in the subquery result: SQL returns no rows at all (0 in my run), because each comparison is unknown; pandas `~isin(...)` returned all 7 rows. This is the classic NULL trap in anti-joins; use `NOT EXISTS`.
- Floats: NaN is a float, so a pandas integer column becomes `float64` once it holds a NaN (the printed salaries are `100.0`). In a nullable integer dtype (`Int64`) the missing value is `pd.NA`; I did not test how that changes `isin` here.
- A NULL group key in SQL `GROUP BY` forms one group (the output shows `(None, 2, 175.0)`), and `NULL = NULL` is unknown but `GROUP BY` and `DISTINCT` treat NULLs as the same.
- The `IS` correlation is SQLite syntax (it also exists in MySQL as `<=>`, not executed here); standard SQL spells it `IS NOT DISTINCT FROM`, not executed here.

**Then explain:**
- **What to say first:** "Which columns can be NULL, and should a NULL count as a value, as unknown, or as zero?" That one sentence decides `NOT IN` versus `NOT EXISTS`, `COUNT(*)` versus `COUNT(col)`, `COALESCE` or not, and whether NULL group keys are reported.
- **Comparisons:** both worlds return "not true" for NaN/NULL comparisons, so filtered rows silently vanish (`df[df.salary > mean]` drops the NaN rows). To keep them, add `| df.salary.isna()` or `OR salary IS NULL`.
- **Differences that bite:** (1) `isin` treats NaN as a value and SQL `IN` does not. (2) `sum` of nothing is 0 in pandas and NULL in SQL (`min_count=1` aligns them). (3) `groupby` drops NaN keys by default and SQL keeps a NULL group (`dropna=False` aligns them).
- **Where `transform` fits:** it is the pandas version of a correlated average. With default `dropna=True`, rows with NaN keys get NaN, the same answer the SQL `=` correlation gives for a NULL key; `dropna=False` matches the `IS` correlation.
- **Merge keys:** pandas `merge` also matches NaN keys to NaN keys, unlike a SQL join; that came from the pandas Comparison-with-SQL page and I did not re-run it here.

**Follow-ups:**
- *How do you make `isin` ignore NaN like SQL?* Drop NaN from the list and from the column first: `s.notna() & s.isin(values)`.
- *`COALESCE` the salary to 0 before averaging?* That changes the meaning (NULL becomes a real 0 and pulls the average down); only do it if the business rule says missing means zero.
- *What about the `mean` of an all-NaN group?* NaN in pandas, NULL in SQL, the same.

**Common mistakes:**
- Writing `== np.nan` or `= NULL`.
- Assuming `NOT IN` works when the subquery column can be NULL.
- Trusting `sum()` to return NaN for an empty or all-missing group.
- Not noticing that `groupby` dropped the NaN-key group, so totals no longer add up to the table total.
- Filling NaN with 0 before an average without saying so.

### Q34 ⭐ 🟡 Empty results inside subqueries: products(product_id, name, category, price). Show what happens with price > (SELECT MAX(price) FROM products WHERE category = 'Toys') when there are no Toys (MAX of nothing is NULL, so no rows), IN and NOT IN over an empty subquery, EXISTS over an empty set, and COUNT versus MAX on an empty set (0 versus NULL). Explain how COALESCE changes the intent and when you would want a row to come back even though the subquery is empty. Give the pandas parallel (empty Series max is NaN).
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** A scalar subquery over an empty set returns NULL, so `price > NULL` is unknown and no rows come back; `IN (empty)` is false, `NOT IN (empty)` is true for every row, `EXISTS (empty)` is false, and `COUNT` of an empty set is 0 while `MAX`, `SUM` and `AVG` are NULL; pandas is the same except `sum()` is 0.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Pen','Stationery',10),(2,'Book','Books',20),(3,'Bag','Bags',50),(4,'Ball','Sports',30);
```

**SQL answer:** `SQL_MAIN` in the Code block returns one row of aggregates over the empty Toys set; the comparison, `IN`, `NOT IN` and `EXISTS` forms are the one-liners printed in the Code block.
```sql
SELECT COUNT(*)      AS n,
       COUNT(price)  AS n_price,
       MAX(price)    AS max_price,
       SUM(price)    AS sum_price,
       TOTAL(price)  AS total_price,
       AVG(price)    AS avg_price
FROM products WHERE category = 'Toys'
```

**pandas answer:** (same text as in the Code block)
```py
toys = products.loc[products["category"] == "Toys", "price"]
pd_df = pd.DataFrame({
    "n": [len(toys)], "n_price": [toys.count()], "max_price": [toys.max()],
    "sum_price": [toys.sum(min_count=1)], "total_price": [float(toys.sum())], "avg_price": [toys.mean()],
})
```

**Example:** The table has Pen 10, Book 20, Bag 50, Ball 30 and no Toys.
- The Toys subset has 0 rows: `COUNT(*)` and `COUNT(price)` are 0; `MAX`, `SUM` and `AVG` are NULL; SQLite's `TOTAL` is 0.0.
- `price > (SELECT MAX(price) ... 'Toys')` becomes `price > NULL`: unknown for all four rows, so 0 rows. With `COALESCE(..., 0)` it becomes `price > 0`: all 4 rows.
- `product_id IN (empty)`: 0 rows. `NOT IN (empty)`: 4 rows. `EXISTS (empty)`: 0 rows. `NOT EXISTS (empty)`: 4 rows.
- Keep-the-row case: "products pricier than every Book, or all products if there are no Books". Books exist (20), so the result is Bag and Ball. Asked for Toys instead, the `NOT EXISTS` branch fires and all four products return.

**Code:** run with `python3 -I`.
```python
# Q34: empty results inside subqueries
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Pen','Stationery',10),(2,'Book','Books',20),(3,'Bag','Bags',50),(4,'Ball','Sports',30);
"""
# one row of aggregates over an empty set (there are no Toys)
SQL_MAIN = """
SELECT COUNT(*)      AS n,
       COUNT(price)  AS n_price,
       MAX(price)    AS max_price,
       SUM(price)    AS sum_price,
       TOTAL(price)  AS total_price,
       AVG(price)    AS avg_price
FROM products WHERE category = 'Toys'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(sql):
    return con.execute(sql).fetchall()
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL aggregates over an empty set (WHERE category = 'Toys'):")
print(sql_df.to_string(index=False))

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
toys = products.loc[products["category"] == "Toys", "price"]
pd_df = pd.DataFrame({
    "n": [len(toys)], "n_price": [toys.count()], "max_price": [toys.max()],
    "sum_price": [toys.sum(min_count=1)], "total_price": [float(toys.sum())], "avg_price": [toys.mean()],
})
# pd:end
print("\npandas on the empty Series:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.astype({"max_price": "float64", "sum_price": "float64", "avg_price": "float64"}), pd_df, check_dtype=False)
print("assert: SQL aggregates == pandas (one row; SUM needs min_count=1, TOTAL is 0.0 like sum())")

print("\n--- comparisons against the empty-set aggregate ---")
cmp_ = "SELECT COUNT(*) FROM products WHERE price > (SELECT MAX(price) FROM products WHERE category = 'Toys')"
print("price > (max of Toys)               ->", q(cmp_)[0][0], "rows")
print("price > COALESCE(max of Toys, 0)    ->", q("SELECT COUNT(*) FROM products WHERE price > COALESCE((SELECT MAX(price) FROM products WHERE category = 'Toys'), 0)")[0][0], "rows")
print("a scalar subquery that returns zero rows is NULL too:",
      q("SELECT (SELECT price FROM products WHERE category = 'Toys')"))
print("pandas products.price > NaN         ->", int((products.price > toys.max()).sum()), "rows")
mx = toys.max()
thr = 0 if pd.isna(mx) else mx
print("pandas with the COALESCE idea       ->", int((products.price > thr).sum()), "rows")

print("\n--- IN, NOT IN, EXISTS over the empty set ---")
for label, sql in [
    ("IN (empty)", "SELECT COUNT(*) FROM products WHERE product_id IN (SELECT product_id FROM products WHERE category = 'Toys')"),
    ("NOT IN (empty)", "SELECT COUNT(*) FROM products WHERE product_id NOT IN (SELECT product_id FROM products WHERE category = 'Toys')"),
    ("EXISTS (empty)", "SELECT COUNT(*) FROM products WHERE EXISTS (SELECT 1 FROM products WHERE category = 'Toys')"),
    ("NOT EXISTS (empty)", "SELECT COUNT(*) FROM products WHERE NOT EXISTS (SELECT 1 FROM products WHERE category = 'Toys')"),
]:
    print("%-20s -> %d rows" % (label, q(sql)[0][0]))
print("scalar form: 5 IN (empty) =", q("SELECT 5 IN (SELECT price FROM products WHERE category='Toys')")[0][0],
      "| 5 NOT IN (empty) =", q("SELECT 5 NOT IN (SELECT price FROM products WHERE category='Toys')")[0][0],
      "| NULL IN (empty) =", q("SELECT NULL IN (SELECT price FROM products WHERE category='Toys')")[0][0],
      "| NULL NOT IN (empty) =", q("SELECT NULL NOT IN (SELECT price FROM products WHERE category='Toys')")[0][0])
print("EXISTS (empty) as a value:", q("SELECT EXISTS (SELECT 1 FROM products WHERE category='Toys')")[0][0])
n_in = int(products.product_id.isin(products.loc[products.category == "Toys", "product_id"]).sum())
print("pandas isin(empty) rows:", n_in, "| ~isin(empty) rows:", int((~products.product_id.isin(products.loc[products.category == "Toys", "product_id"])).sum()))
assert q(cmp_)[0][0] == int((products.price > toys.max()).sum()) == 0
assert q("SELECT COUNT(*) FROM products WHERE price > COALESCE((SELECT MAX(price) FROM products WHERE category = 'Toys'), 0)")[0][0] == int((products.price > thr).sum()) == 4

print("\n--- when you want the row anyway: keep a row even if the subquery is empty ---")
keep = """
SELECT p.name, p.price FROM products p
WHERE p.price > (SELECT MAX(price) FROM products WHERE category = 'Books')
   OR NOT EXISTS (SELECT 1 FROM products WHERE category = 'Books')
ORDER BY p.product_id"""
print("pricier than every Book (Books exist):", q(keep))
print("same query, category 'Toys' instead  :", q(keep.replace("'Books'", "'Toys'")))
```

**Output (my run):**
```text
SQL aggregates over an empty set (WHERE category = 'Toys'):
 n  n_price max_price sum_price  total_price avg_price
 0        0      None      None          0.0      None

pandas on the empty Series:
 n  n_price  max_price  sum_price  total_price  avg_price
 0        0        NaN        NaN          0.0        NaN
assert: SQL aggregates == pandas (one row; SUM needs min_count=1, TOTAL is 0.0 like sum())

--- comparisons against the empty-set aggregate ---
price > (max of Toys)               -> 0 rows
price > COALESCE(max of Toys, 0)    -> 4 rows
a scalar subquery that returns zero rows is NULL too: [(None,)]
pandas products.price > NaN         -> 0 rows
pandas with the COALESCE idea       -> 4 rows

--- IN, NOT IN, EXISTS over the empty set ---
IN (empty)           -> 0 rows
NOT IN (empty)       -> 4 rows
EXISTS (empty)       -> 0 rows
NOT EXISTS (empty)   -> 4 rows
scalar form: 5 IN (empty) = 0 | 5 NOT IN (empty) = 1 | NULL IN (empty) = 0 | NULL NOT IN (empty) = 1
EXISTS (empty) as a value: 0
pandas isin(empty) rows: 0 | ~isin(empty) rows: 4

--- when you want the row anyway: keep a row even if the subquery is empty ---
pricier than every Book (Books exist): [('Bag', 50), ('Ball', 30)]
same query, category 'Toys' instead  : [('Pen', 10), ('Book', 20), ('Bag', 50), ('Ball', 30)]
```

**Edge cases:**
- Empty is not the same as NULL-containing: `NOT IN` over a subquery that returns a NULL value gives no rows, whereas `NOT IN` over an empty subquery gives every row (that comparison is in Q33). Even `NULL NOT IN (empty)` is true in SQLite (printed as 1), because there is nothing to compare with; I checked this only in SQLite 3.45.
- A zero-row scalar subquery (`SELECT price ... WHERE category = 'Toys'`, no aggregate) is also NULL, as shown in the output.
- `COUNT(*)` over an empty set with no `GROUP BY` returns one row with 0. With `GROUP BY` on an empty set there are no groups, so no rows at all.
- `COALESCE(..., 0)` is only right if 0 is a sensible threshold; for "price above the Toys maximum" a missing Toys category more naturally means "no constraint", which is the `OR NOT EXISTS` form.

**Then explain:**
- **Three-valued logic:** a comparison with NULL is unknown, and `WHERE` keeps only true. So "above the max of nothing" returns nothing, even though one might argue "everything is above nothing". Decide what you want and write it explicitly.
- **COALESCE changes the intent:** `COALESCE(max, 0)` turns "no rows" into "all rows" (given positive prices). `COALESCE(max, 999999)` would turn it back into "no rows". The default you choose is a business rule, not a technicality.
- **Keeping a row when the subquery is empty:** use `OR NOT EXISTS (...)`, or a `LEFT JOIN` to the aggregate with a `CASE`. For a "show a zero count row" report, compute counts with `COUNT` and `COALESCE` the rest.
- **pandas parallel:** an empty Series has `max()` NaN, `mean()` NaN, `count()` 0, `sum()` 0 (not NaN, unless `min_count=1`). `products.price > NaN` is False everywhere (0 rows), `isin([])` is False everywhere, `~isin([])` is True everywhere.
- **Other engines (not executed here):** the empty-set rules are standard SQL and I expect the same in PostgreSQL and MySQL, but I did not run them.

**Follow-ups:**
- *Why does `COUNT` give 0 but `MAX` give NULL?* `COUNT` counts rows and zero rows is a number; there is no maximum of nothing.
- *`SELECT MAX(price) FROM products WHERE 1 = 0` returns how many rows?* One row, with NULL. A bare aggregate always returns one row.
- *`EXISTS` or `COUNT(*) > 0`?* `EXISTS` can stop at the first match; same answer.

**Common mistakes:**
- Expecting `price > (empty subquery)` to behave like `price > 0`.
- Using `COALESCE(..., 0)` blindly when the missing case should mean "no filter".
- Treating an empty subquery like a NULL-containing one under `NOT IN`.
- In pandas, assuming `sum()` of an empty Series is NaN.

### Q35 ⭐ 🔴 Relational division with double NOT EXISTS: products(product_id, name, category) and orders(order_id, customer_id, product_id). List customers who bought every product in category 'Books'. Write the double NOT EXISTS form ('there is no Books product for which there is no order by this customer'), compare it with GROUP BY HAVING COUNT(DISTINCT), and explain the vacuous-truth problem when the category has no products (every customer qualifies), duplicate order rows, and which form handles customers with no orders. Give pandas (set comparison via groupby and issubset).
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** "Customers who bought every Book" means there is no Book that this customer has not bought, which is a double `NOT EXISTS`; the usual alternative is `GROUP BY customer HAVING COUNT(DISTINCT product) = number of Books`, but the two disagree when the category is empty (double `NOT EXISTS` returns everyone, the `HAVING` form returns no one) and `DISTINCT` is essential because customers repeat orders.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO products VALUES (10,'Novel','Books'),(11,'Atlas','Books'),(12,'Diary','Books'),(20,'Pen','Stationery');
INSERT INTO orders VALUES
 (1,1,10),(2,1,11),(3,1,12),(4,1,10),
 (5,2,10),(6,2,11),
 (7,3,10),(8,3,11),(9,3,12),(10,3,20),
 (11,5,10),(12,5,10),(13,5,10);
```

**SQL answer:** `SQL_MAIN` in the Code block, with `:cat` bound to `'Books'` (it starts from `customers`, so people with no orders are considered).
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM products p
  WHERE p.category = :cat
    AND NOT EXISTS (SELECT 1 FROM orders o
                    WHERE o.customer_id = c.customer_id AND o.product_id = p.product_id))
ORDER BY c.customer_id
```
The `HAVING` form, `SQL_HAVING` in the Code block, also run with `:cat` bound:
```sql
SELECT o.customer_id
FROM orders o JOIN products p ON p.product_id = o.product_id
WHERE p.category = :cat
GROUP BY o.customer_id
HAVING COUNT(DISTINCT o.product_id) = (SELECT COUNT(*) FROM products WHERE category = :cat)
ORDER BY o.customer_id
```
The tempting wrong version replaces `COUNT(DISTINCT o.product_id)` with `COUNT(*)` (`SQL_WRONG` in the Code block).

**pandas answer:** (body of the function `divide(cat)` in the Code block; the function is called with the category)
```py
needed = set(products.loc[products["category"] == cat, "product_id"])
bought = orders.groupby("customer_id")["product_id"].agg(set)
per_customer = customers["customer_id"].map(bought).apply(lambda s: s if isinstance(s, set) else set())
return customers.loc[[needed.issubset(s) for s in per_customer], ["customer_id", "name"]].reset_index(drop=True)
```

**Example:** Books are products 10, 11, 12; product 20 is a Pen. Customers: Asha 1, Ben 2, Chitra 3, Dev 4, Esha 5.
- Asha ordered 10, 11, 12 and 10 again: all three Books, so she qualifies (4 order rows, 3 distinct Books).
- Ben ordered 10 and 11: Book 12 has no matching order, so the inner `NOT EXISTS` finds it, and the outer `NOT EXISTS` fails. Out.
- Chitra ordered 10, 11, 12 and the Pen: qualifies (the Pen is not a Book and is ignored by `WHERE category`).
- Dev has no orders: he fails for every Book, so he is out.
- Esha ordered Book 10 three times: 3 order rows, 1 distinct Book. Out.
- Result: Asha (1) and Chitra (3).
- `HAVING COUNT(*) = 3` instead: Asha has 4 rows (wrongly out), Esha has 3 rows (wrongly in); my run returns [3, 5].
- Category with no products (Toys here): the number of Toys is 0. The double `NOT EXISTS` has nothing to violate, so all five customers qualify, Dev included (vacuous truth). The `HAVING` form returns no rows, because only customers with a Toy order appear in the groups and there are none.

**Code:** run with `python3 -I`.
```python
# Q35: relational division: double NOT EXISTS vs GROUP BY HAVING COUNT(DISTINCT); vacuous truth
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO products VALUES (10,'Novel','Books'),(11,'Atlas','Books'),(12,'Diary','Books'),(20,'Pen','Stationery');
INSERT INTO orders VALUES
 (1,1,10),(2,1,11),(3,1,12),(4,1,10),
 (5,2,10),(6,2,11),
 (7,3,10),(8,3,11),(9,3,12),(10,3,20),
 (11,5,10),(12,5,10),(13,5,10);
"""
SQL_MAIN = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM products p
  WHERE p.category = :cat
    AND NOT EXISTS (SELECT 1 FROM orders o
                    WHERE o.customer_id = c.customer_id AND o.product_id = p.product_id))
ORDER BY c.customer_id
"""
SQL_HAVING = """
SELECT o.customer_id
FROM orders o JOIN products p ON p.product_id = o.product_id
WHERE p.category = :cat
GROUP BY o.customer_id
HAVING COUNT(DISTINCT o.product_id) = (SELECT COUNT(*) FROM products WHERE category = :cat)
ORDER BY o.customer_id
"""
SQL_WRONG = SQL_HAVING.replace("COUNT(DISTINCT o.product_id)", "COUNT(*)")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
for cat in ["Books", "Toys"]:
    a = [r[0] for r in con.execute(SQL_MAIN, {"cat": cat})]
    b = [r[0] for r in con.execute(SQL_HAVING, {"cat": cat})]
    w = [r[0] for r in con.execute(SQL_WRONG, {"cat": cat})]
    print("category %-6s double NOT EXISTS: %s | HAVING COUNT(DISTINCT): %s | HAVING COUNT(*): %s" % (cat, a, b, w))
a_books = pd.read_sql_query(SQL_MAIN, con, params={"cat": "Books"})
print("\nSQL double NOT EXISTS, Books:")
print(a_books.to_string(index=False))

customers = pd.read_sql_query("SELECT * FROM customers", con)
products = pd.read_sql_query("SELECT * FROM products", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
def divide(cat):
# pd:main
    needed = set(products.loc[products["category"] == cat, "product_id"])
    bought = orders.groupby("customer_id")["product_id"].agg(set)
    per_customer = customers["customer_id"].map(bought).apply(lambda s: s if isinstance(s, set) else set())
    return customers.loc[[needed.issubset(s) for s in per_customer], ["customer_id", "name"]].reset_index(drop=True)
# pd:end
pd_books = divide("Books")
print("\npandas issubset, Books:")
print(pd_books.to_string(index=False))
# compared in customer_id order
pd.testing.assert_frame_equal(a_books, pd_books)
for cat in ["Books", "Toys"]:
    a = [r[0] for r in con.execute(SQL_MAIN, {"cat": cat})]
    assert a == divide(cat)["customer_id"].tolist()
print("assert: SQL double NOT EXISTS == pandas issubset for Books and for Toys")
print("Toys (no such products): pandas rows ->", divide("Toys")["customer_id"].tolist(), "(every customer, vacuous truth, Dev included)")
b_toys = [r[0] for r in con.execute(SQL_HAVING, {"cat": "Toys"})]
print("HAVING form for Toys ->", b_toys)
print("\norder rows per customer for Books:",
      con.execute("SELECT o.customer_id, COUNT(*), COUNT(DISTINCT o.product_id) FROM orders o JOIN products p USING(product_id) WHERE p.category='Books' GROUP BY o.customer_id").fetchall(),
      "(customer, rows, distinct books)")
```

**Output (my run):**
```text
category Books  double NOT EXISTS: [1, 3] | HAVING COUNT(DISTINCT): [1, 3] | HAVING COUNT(*): [3, 5]
category Toys   double NOT EXISTS: [1, 2, 3, 4, 5] | HAVING COUNT(DISTINCT): [] | HAVING COUNT(*): []

SQL double NOT EXISTS, Books:
 customer_id   name
           1   Asha
           3 Chitra

pandas issubset, Books:
 customer_id   name
           1   Asha
           3 Chitra
assert: SQL double NOT EXISTS == pandas issubset for Books and for Toys
Toys (no such products): pandas rows -> [1, 2, 3, 4, 5] (every customer, vacuous truth, Dev included)
HAVING form for Toys -> []

order rows per customer for Books: [(1, 4, 3), (2, 2, 2), (3, 3, 3), (5, 3, 1)] (customer, rows, distinct books)
```

**Edge cases:**
- **Empty category:** double `NOT EXISTS` returns every customer (all five); `HAVING` returns nobody. Neither is "wrong" mathematically, but the business answer is almost always "nobody", so guard it: add `AND EXISTS (SELECT 1 FROM products WHERE category = :cat)`. I did not run the guarded form.
- **Duplicate order rows:** harmless in double `NOT EXISTS` (it only asks whether a row exists); in `HAVING` you need `COUNT(DISTINCT product_id)`, and a plain `COUNT(*)` is wrong in both directions, as shown.
- **Customers with no orders:** the `NOT EXISTS` form handles them (starting from `customers`), but they only matter in the vacuous case. The `HAVING` form starts from `orders`, so they never appear; for a non-empty category that is what you want.
- **Duplicate product rows in the `products` table:** `COUNT(*)` over products would count a Book twice; use `COUNT(DISTINCT product_id)` there too if the table is not unique on `product_id`.
- **Orders whose product no longer exists in `products`:** ignored by both forms (the join and the inner `NOT EXISTS` only look at products).

**Then explain:**
- **Reading the double `NOT EXISTS`:** "there is no Book for which there is no order by this customer." The inner `NOT EXISTS` finds a missing order; the outer one demands that no Book is missing.
- **HAVING form:** join orders to Books, count distinct Books per customer and compare with the total number of Books. It is shorter and usually quicker to write; it is also the form interviewers expect for the LeetCode-style problem named Customers Who Bought All Products (I know that problem only from list snippets and did not open its page).
- **Which to use:** `HAVING` for the common case with a trusted non-empty category; double `NOT EXISTS` when "every" must be tested against a set that may be filtered or empty, or when you need the vacuous-truth behaviour on purpose.
- **pandas:** build the set of required product ids, the set of products each customer bought (`groupby(...).agg(set)`), then `needed.issubset(bought)`. `issubset` of the empty set is True for everyone, the same vacuous truth as SQL's double `NOT EXISTS`. Customers with no orders must be filled with an empty set via the `customers` frame, or they disappear.
- **Cost:** the double `NOT EXISTS` is customers x books lookups, fine with an index on `orders(customer_id, product_id)`; I did not measure it. Plans belong to Part 11.

**Follow-ups:**
- *Why not `IN`?* `IN` tests one value, not "all of a set"; you need counting or a double negation.
- *What if it is "bought at least 2 of the Books"?* Then `HAVING COUNT(DISTINCT product_id) >= 2`; division is only "all".
- *Customers who bought only Books?* A different anti-join: no order of a non-Book product.

**Common mistakes:**
- Using `COUNT(*)` instead of `COUNT(DISTINCT product_id)`.
- Hard-coding the number of Books (3) in the query.
- Forgetting the empty-category case.
- Putting `category = 'Books'` in the outer `WHERE` of the join and then dividing by the total product count instead of the Book count.
- In pandas, `groupby(...).agg(set)` then forgetting customers with no orders (they are missing, not empty).

### Q36 ⭐ 🔴 Second-highest salary per department without window functions: employees(emp_id, name, dept_id, salary). For each department return the second-highest distinct salary (or NULL if the department has only one distinct salary) using a correlated subquery or a derived table of MAX excluding the top. Explain how ties at the top are handled, why a department with one employee yields NULL and how to keep it in the output, the cost, and the pandas groupby with nlargest or unique. Note that DENSE_RANK in Part 4 is the normal answer.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** The second-highest distinct salary in a department is the maximum of the salaries strictly below the department's maximum; if no such salary exists the inner `MAX` is NULL, which is exactly the "NULL if only one distinct salary" rule, and driving from a `departments` table keeps empty departments in the output.

**Schema and sample data:**
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (1,'Eng'),(2,'Ops'),(3,'Sales'),(4,'Legal'),(5,'HR');
INSERT INTO employees VALUES
 (1,'Asha',1,100),(2,'Ben',1,100),(3,'Chitra',1,90),(4,'Dev',1,80),
 (5,'Esha',2,70),
 (6,'Farid',3,60),(7,'Gita',3,50),
 (8,'Hari',5,40),(9,'Isha',5,NULL),(10,'Jay',5,NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT d.dept_id, d.dept_name,
       (SELECT MAX(e.salary)
        FROM employees e
        WHERE e.dept_id = d.dept_id
          AND e.salary < (SELECT MAX(x.salary) FROM employees x WHERE x.dept_id = d.dept_id)
       ) AS second_highest
FROM departments d
ORDER BY d.dept_id
```
A second form that generalises to the Nth highest (`SQL_COUNT` in the Code block): the salary that has exactly N-1 distinct higher salaries. The Code block asserts both give the same table.
```sql
SELECT d.dept_id, d.dept_name,
       (SELECT DISTINCT e.salary FROM employees e
        WHERE e.dept_id = d.dept_id
          AND (SELECT COUNT(DISTINCT x.salary) FROM employees x
               WHERE x.dept_id = e.dept_id AND x.salary > e.salary) = 1
       ) AS second_highest
FROM departments d
ORDER BY d.dept_id
```

**pandas answer:** (same text as in the Code block)
```py
def second_distinct(s):
    vals = np.sort(s.dropna().unique())[::-1]
    return vals[1] if len(vals) > 1 else np.nan
second = employees.groupby("dept_id")["salary"].apply(second_distinct).rename("second_highest").reset_index()
pd_df = departments.merge(second, on="dept_id", how="left").sort_values("dept_id").reset_index(drop=True)
```

**Example:**
- Eng (dept 1): salaries 100, 100, 90, 80. The department maximum is 100. The salaries below 100 are 90 and 80, whose `MAX` is 90. The tie at the top (two people on 100) does not matter, because "strictly below the maximum" skips both.
- Ops (dept 2): one employee on 70. Nothing is below 70, so the inner `MAX` is NULL.
- Sales (dept 3): 60 and 50, so 50.
- Legal (dept 4): no employees. The inner `MAX`es are NULL; the department still appears because the outer table is `departments`.
- HR (dept 5): salaries 40, NULL, NULL. `MAX` ignores NULLs, so the maximum is 40 and nothing is below it: NULL.
- Result: 90, NULL, 50, NULL, NULL.

**Code:** run with `python3 -I`.
```python
# Q36: second-highest distinct salary per department without window functions
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (1,'Eng'),(2,'Ops'),(3,'Sales'),(4,'Legal'),(5,'HR');
INSERT INTO employees VALUES
 (1,'Asha',1,100),(2,'Ben',1,100),(3,'Chitra',1,90),(4,'Dev',1,80),
 (5,'Esha',2,70),
 (6,'Farid',3,60),(7,'Gita',3,50),
 (8,'Hari',5,40),(9,'Isha',5,NULL),(10,'Jay',5,NULL);
"""
SQL_MAIN = """
SELECT d.dept_id, d.dept_name,
       (SELECT MAX(e.salary)
        FROM employees e
        WHERE e.dept_id = d.dept_id
          AND e.salary < (SELECT MAX(x.salary) FROM employees x WHERE x.dept_id = d.dept_id)
       ) AS second_highest
FROM departments d
ORDER BY d.dept_id
"""
# the Nth-highest version: count distinct higher salaries (generalises to N)
SQL_COUNT = """
SELECT d.dept_id, d.dept_name,
       (SELECT DISTINCT e.salary FROM employees e
        WHERE e.dept_id = d.dept_id
          AND (SELECT COUNT(DISTINCT x.salary) FROM employees x
               WHERE x.dept_id = e.dept_id AND x.salary > e.salary) = 1
       ) AS second_highest
FROM departments d
ORDER BY d.dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
cnt_df = pd.read_sql_query(SQL_COUNT, con)
print("SQL (MAX below the department MAX):")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, cnt_df)
print("\nassert: MAX-below-MAX == count-of-higher-distinct-salaries version")

departments = pd.read_sql_query("SELECT * FROM departments", con)
employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def second_distinct(s):
    vals = np.sort(s.dropna().unique())[::-1]
    return vals[1] if len(vals) > 1 else np.nan
second = employees.groupby("dept_id")["salary"].apply(second_distinct).rename("second_highest").reset_index()
pd_df = departments.merge(second, on="dept_id", how="left").sort_values("dept_id").reset_index(drop=True)
# pd:end
print("\npandas (unique, sort descending, take the second):")
print(pd_df.to_string(index=False))
# compared by dept_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("\nassert: SQL == pandas")

# the tempting nlargest version is wrong when the top salary is tied
nl = employees.groupby("dept_id")["salary"].apply(lambda s: s.nlargest(2).iloc[-1] if s.notna().sum() > 0 else np.nan)
print("\nnlargest(2) without drop_duplicates, last value per dept:", nl.to_dict(), "(dept 1 gives 100, not 90)")
nl2 = employees.groupby("dept_id")["salary"].apply(lambda s: s.drop_duplicates().nlargest(2).iloc[-1])
print("with drop_duplicates, last of nlargest(2):", nl2.to_dict(), "(dept 2 gives its only salary, 70, not NULL)")

# inner join to the employees only would lose Legal (dept 4, no employees)
lost = con.execute("""SELECT d.dept_id FROM departments d JOIN employees e ON e.dept_id = d.dept_id GROUP BY d.dept_id""").fetchall()
print("\ndepartments with at least one employee:", [r[0] for r in lost], "(Legal, dept 4, would vanish without driving from departments)")
```

**Output (my run):**
```text
SQL (MAX below the department MAX):
 dept_id dept_name  second_highest
       1       Eng            90.0
       2       Ops             NaN
       3     Sales            50.0
       4     Legal             NaN
       5        HR             NaN

assert: MAX-below-MAX == count-of-higher-distinct-salaries version

pandas (unique, sort descending, take the second):
 dept_id dept_name  second_highest
       1       Eng            90.0
       2       Ops             NaN
       3     Sales            50.0
       4     Legal             NaN
       5        HR             NaN

assert: SQL == pandas

nlargest(2) without drop_duplicates, last value per dept: {1: 100.0, 2: 70.0, 3: 50.0, 5: nan} (dept 1 gives 100, not 90)
with drop_duplicates, last of nlargest(2): {1: 90.0, 2: 70.0, 3: 50.0, 5: nan} (dept 2 gives its only salary, 70, not NULL)

departments with at least one employee: [1, 2, 3, 5] (Legal, dept 4, would vanish without driving from departments)
```

**Edge cases:**
- **Ties at the top:** handled, because the test is `<` the maximum, not "not the first row". A version using `ORDER BY salary DESC LIMIT 1 OFFSET 1` returns 100 for Eng (the second row, which is the duplicate); the pandas equivalent is `nlargest(2)` without `drop_duplicates`, which my run shows returning 100 as well.
- **Ties at the second place:** 90, 90, 80 under 100 still gives 90 (distinct values, not rows).
- **One distinct salary:** NULL. In pandas, `nlargest` after `drop_duplicates` would return that single salary instead of a missing value, as my run shows for dept 2 (70), so I count the unique values and return NaN when there are fewer than two.
- **NULL salaries:** ignored by `MAX` in SQL and by `dropna()` in pandas.
- **Empty department:** only appears when the query starts from `departments`; driving from `employees` loses it (my run shows dept 4 missing from the inner-joined list).

**Then explain:**
- **How it reads:** for each department row, find the top salary, then the top of everything under it. Two nested correlated subqueries.
- **Cost:** the inner `MAX` runs once per employee row in the department (twice per department in the first form), so the work is about departments x employees-per-department without an index; with an index on `employees(dept_id, salary)` each `MAX` can be an index lookup (typical, I did not time it here; plans are Part 11). The count form is heavier: for every distinct candidate salary it runs another subquery.
- **Not the normal answer:** in an interview, `DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)` then `WHERE rnk = 2` is the standard solution; it is in Part 4. The subquery form is asked to see whether you understand correlation.
- **Nth highest:** the count form changes `= 1` to `= N - 1`; the MAX-below-MAX form would need N-1 levels of nesting.
- **pandas:** take each group's unique non-null salaries, sort descending, pick index 1 if there are at least two, else NaN. Then merge onto `departments` with a left merge to keep the empty department.

**Follow-ups:**
- *What if the question wants the employee names on the second salary?* Join the result back to `employees` on `dept_id` and `salary`; ties return several names.
- *And "second highest per department including duplicates" (row-based)?* That is `ROW_NUMBER`, Part 4.
- *Why return NULL and not an error or a missing row?* A scalar subquery with no rows is NULL, and that keeps one row per department.

**Common mistakes:**
- `ORDER BY salary DESC LIMIT 1 OFFSET 1` without `DISTINCT`, which returns the duplicate top salary.
- Using `NOT IN (SELECT MAX(...))` or `<>` forms to exclude the top salary: `<>` or `NOT IN` against a single maximum works only until NULLs or ties appear; use `<` the maximum.
- Driving from `employees` so departments without a second salary (or without employees) vanish.
- In pandas, `nlargest(2).iloc[-1]` on a group with one value, which silently returns the first value.

### Q37 ⭐ 🔴 Median without window functions: employees(emp_id, name, salary) with an even or odd row count and NULL salaries. Compute the median salary using a scalar subquery for COUNT and ORDER BY salary LIMIT 2 - (n % 2) OFFSET (n - 1) / 2 wrapped in AVG. Explain why NULLs must be filtered in both the count and the sorted set, how even and odd counts are handled, that engines with PERCENTILE_CONT make this simpler (hedged, not executed), and show pandas median with its NaN skipping.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** With n non-NULL salaries sorted ascending, skip `(n - 1) / 2` rows (integer division) and take `2 - n % 2` rows, which is the one middle row when n is odd and the two middle rows when n is even, then `AVG` them; the NULLs have to be removed from both the count and the sorted set, or the middle moves.

**Schema and sample data:** the Code block runs eight small tables (odd, even, ties, with NULLs, one value, all NULL, empty); the main one is the NULL-containing table below.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
-- scenario "NULLs + 5 real (8 rows)": salaries 10, NULL, 20, NULL, 30, 40, 50, NULL
INSERT INTO employees(name, salary) VALUES ('e0',10),('e1',NULL),('e2',20),('e3',NULL),('e4',30),('e5',40),('e6',50),('e7',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT AVG(salary) AS median_salary
FROM (SELECT salary FROM employees
      WHERE salary IS NOT NULL
      ORDER BY salary
      LIMIT 2 - (SELECT COUNT(salary) FROM employees) % 2
      OFFSET ((SELECT COUNT(salary) FROM employees) - 1) / 2)
```
Two wrong variants run next to it: `SQL_NO_NULL_FILTER` (counts non-NULLs but sorts everything) and `SQL_COUNT_STAR` (filters NULLs in the sort but counts all rows).

**pandas answer:** (same text as in the Code block, one line inside the scenario loop)
```py
pd_val = emp["salary"].median()
```

**Example:** Five real salaries 10, 20, 30, 40, 50 and three NULLs (8 rows).
- `COUNT(salary)` = 5. `LIMIT 2 - 5 % 2` = `2 - 1` = 1 row. `OFFSET (5 - 1) / 2` = 2 rows skipped. Sorted real salaries 10, 20, 30, 40, 50: skip two, take one: 30. `AVG` of one row = 30.
- With four real salaries 10, 20, 30, 40 (and three NULLs): `COUNT` = 4, `LIMIT 2 - 0` = 2, `OFFSET (4 - 1) / 2` = 1 (3 / 2 truncates to 1). Skip 10, take 20 and 30, average = 25.
- Without the NULL filter in the sorted set, SQLite sorts NULLs first, so the middle is taken from the wrong place and `AVG` returns NULL (both NULL-containing tables in my run). With `COUNT(*)` instead of `COUNT(salary)` the offset and limit are computed from 8 rows instead of 5, and my run printed 45 instead of 30 (8-row table) and 40 instead of 25 (7-row table).

**Code:** run with `python3 -I`.
```python
# Q37: median without window functions: LIMIT 2 - (n % 2) OFFSET (n - 1) / 2 wrapped in AVG
import sqlite3
import numpy as np
import pandas as pd

SQL_MAIN = """
SELECT AVG(salary) AS median_salary
FROM (SELECT salary FROM employees
      WHERE salary IS NOT NULL
      ORDER BY salary
      LIMIT 2 - (SELECT COUNT(salary) FROM employees) % 2
      OFFSET ((SELECT COUNT(salary) FROM employees) - 1) / 2)
"""
SQL_NO_NULL_FILTER = """
SELECT AVG(salary) FROM (SELECT salary FROM employees ORDER BY salary
      LIMIT 2 - (SELECT COUNT(salary) FROM employees) % 2
      OFFSET ((SELECT COUNT(salary) FROM employees) - 1) / 2)
"""
SQL_COUNT_STAR = """
SELECT AVG(salary) FROM (SELECT salary FROM employees WHERE salary IS NOT NULL ORDER BY salary
      LIMIT 2 - (SELECT COUNT(*) FROM employees) % 2
      OFFSET ((SELECT COUNT(*) FROM employees) - 1) / 2)
"""
SCENARIOS = {
    "odd (5 rows)":            [10, 20, 30, 40, 50],
    "even (6 rows)":           [10, 20, 30, 40, 50, 60],
    "ties (4 rows)":           [5, 5, 5, 9],
    "NULLs + 5 real (8 rows)": [10, None, 20, None, 30, 40, 50, None],
    "NULLs + 4 real (7 rows)": [10, None, 20, None, 30, 40, None],
    "one value":               [42],
    "all NULL":                [None, None],
    "empty table":             [],
}
print("%-26s %8s %8s %12s %12s" % ("scenario", "SQL", "pandas", "no NULL flt", "COUNT(*)"))
for name, vals in SCENARIOS.items():
    con = sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);")
    con.executemany("INSERT INTO employees(name, salary) VALUES (?, ?)", [("e%d" % i, v) for i, v in enumerate(vals)])
    sql_val = con.execute(SQL_MAIN).fetchone()[0]
    emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
    pd_val = emp["salary"].median()
# pd:end
    bad1 = con.execute(SQL_NO_NULL_FILTER).fetchone()[0]
    bad2 = con.execute(SQL_COUNT_STAR).fetchone()[0]
    same = (sql_val is None and np.isnan(pd_val)) or sql_val == pd_val
    assert same, (name, sql_val, pd_val)
    print("%-26s %8s %8s %12s %12s" % (name, sql_val, pd_val, bad1, bad2))
print("\nassert: SQL median == pandas median for every scenario (NaN/NULL where there is nothing to take the median of)")

con = sqlite3.connect(":memory:")
print("\nLIMIT / OFFSET with expressions on SQLite 3.45:")
print("  LIMIT 1 + 1       ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT 1 + 1").fetchall())
print("  OFFSET (3 - 1) / 2 ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT 5 OFFSET (3 - 1) / 2").fetchall())
print("  LIMIT (scalar subquery) ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT (SELECT 2)").fetchall())
print("  LIMIT -1 OFFSET 1 ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT -1 OFFSET 1").fetchall())
print("  OFFSET -1          ->", con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) LIMIT 2 OFFSET -1").fetchall())
print("  (0 - 1) / 2 in SQLite (integer division truncates toward zero) =", con.execute("SELECT (0 - 1) / 2").fetchone()[0])
print("  OFFSET without LIMIT ->", end=" ")
try:
    print(con.execute("SELECT * FROM (SELECT 1 UNION ALL SELECT 2) OFFSET 1").fetchall())
except sqlite3.Error as e:
    print("error:", e)
```

**Output (my run):**
```text
scenario                        SQL   pandas  no NULL flt     COUNT(*)
odd (5 rows)                   30.0     30.0         30.0         30.0
even (6 rows)                  35.0     35.0         35.0         35.0
ties (4 rows)                   5.0      5.0          5.0          5.0
NULLs + 5 real (8 rows)        30.0     30.0         None         45.0
NULLs + 4 real (7 rows)        25.0     25.0         None         40.0
one value                      42.0     42.0         42.0         42.0
all NULL                       None      nan         None         None
empty table                    None      nan         None         None

assert: SQL median == pandas median for every scenario (NaN/NULL where there is nothing to take the median of)

LIMIT / OFFSET with expressions on SQLite 3.45:
  LIMIT 1 + 1       -> [(1,), (2,)]
  OFFSET (3 - 1) / 2 -> [(2,), (3,)]
  LIMIT (scalar subquery) -> [(1,), (2,)]
  LIMIT -1 OFFSET 1 -> [(2,), (3,)]
  OFFSET -1          -> [(1,), (2,)]
  (0 - 1) / 2 in SQLite (integer division truncates toward zero) = 0
  OFFSET without LIMIT -> error: near "1": syntax error
```

**Edge cases:**
- **NULLs:** must be removed from both places, `WHERE salary IS NOT NULL` in the sorted set and `COUNT(salary)` (not `COUNT(*)`) for n. The two wrong variants in the output show different wrong answers.
- **Ties:** harmless; the middle values are just equal numbers (the 5, 5, 5, 9 scenario gives 5).
- **One value:** `LIMIT 1 OFFSET 0`, returns the value itself (42).
- **Empty or all-NULL:** n = 0 gives `OFFSET (0 - 1) / 2`, which SQLite evaluates as 0 (integer division truncates toward zero, printed in the output), and `LIMIT 2`; no rows, so `AVG` is NULL, matching pandas NaN. In SQLite a negative offset is treated as 0 too (printed), but I would not rely on that in other engines (not executed).
- **Integer division:** `/` on two integers truncates in SQLite. In engines where `/` of integers is decimal division, `(n - 1) / 2` would need a floor (not executed here).
- **Even count with integers:** `AVG` returns a float, so the median of 20 and 30 is 25.0.

**Then explain:**
- **Why `AVG` and not just a pick:** for even n the median is the mean of the two middle rows; for odd n the `AVG` of one row is that row. One formula covers both.
- **Why `LIMIT 2 - n % 2`:** it equals 1 when n is odd and 2 when n is even.
- **LIMIT and OFFSET with expressions:** SQLite 3.45 accepted `LIMIT 1 + 1`, `LIMIT (SELECT 2)` and `OFFSET (3 - 1) / 2`, and also `LIMIT -1` (no limit). `OFFSET` alone, without `LIMIT`, is a syntax error. PostgreSQL accepts expressions there, as I recall; MySQL, as I recall, wants literals or variables for `LIMIT` and `OFFSET` (a scalar subquery there is not allowed); neither was executed here.
- **Easier engines (not executed):** PostgreSQL, Snowflake and Oracle offer `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)`; BigQuery has `PERCENTILE_CONT` as an analytic function; SQLite 3.45 has neither. Check each manual.
- **Window version:** `ROW_NUMBER` and `COUNT` windows give the middle rows without a LIMIT trick (Parts 4-5).
- **pandas:** `Series.median()` skips NaN by default (`skipna=True`) and returns NaN for an empty or all-NaN Series, which is the same thing the SQL returns; the code asserts equality for all eight scenarios.

**Follow-ups:**
- *Median per group?* The LIMIT trick does not work per group; use a window function (Part 4) or a correlated count.
- *What about a weighted median?* Out of scope here.
- *Why is this slow on big tables?* It sorts the table once for the median, and the two `COUNT` subqueries scan it again; no per-row work.

**Common mistakes:**
- Using `COUNT(*)` while NULLs are in the table, or filtering NULLs in one place only.
- Forgetting the `AVG` wrapper, so even counts return one of the two middle values.
- Using `(n + 1) / 2` offsets and off-by-one errors; check with one, two, three and four rows.
- Assuming `LIMIT` accepts an expression in every engine.
- In pandas, filling NaN with 0 before `median()`.

### Q38 ⭐ 🔴 Orders larger than the customer's earlier average: orders(order_id, customer_id, order_date, amount) with ISO dates. List orders whose amount is greater than the average of the same customer's earlier orders, using a correlated subquery with a date comparison. Explain what happens for a customer's first order (average over an empty set is NULL, so excluded), same-date orders (use order_id as a tie-break), the per-row cost, and a pandas version with groupby and expanding mean shifted by one (note the cumulative-window version is Part 5).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** For each order I take the average of the same customer's earlier orders with a correlated subquery whose WHERE says "earlier date, or the same date and a smaller order_id", and keep the order if its amount is above that average; a customer's first order has no earlier orders, the average is NULL, and the comparison drops it.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-01',100),(2,1,'2024-01-10',200),(3,1,'2024-01-10',150),(4,1,'2024-02-01',90),
 (5,2,'2024-01-05',50),(6,2,'2024-01-06',70),
 (7,3,'2024-01-09',500);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT o.order_id, o.customer_id, o.order_date, o.amount,
       (SELECT AVG(p.amount) FROM orders p
        WHERE p.customer_id = o.customer_id
          AND (p.order_date < o.order_date
               OR (p.order_date = o.order_date AND p.order_id < o.order_id))) AS earlier_avg
FROM orders o
WHERE o.amount > (SELECT AVG(p.amount) FROM orders p
                  WHERE p.customer_id = o.customer_id
                    AND (p.order_date < o.order_date
                         OR (p.order_date = o.order_date AND p.order_id < o.order_id)))
ORDER BY o.order_id
```
`SQL_ROW` in the Code block is the same condition written with a row-value comparison, `(p.order_date, p.order_id) < (o.order_date, o.order_id)`; the Code block asserts that it returns the same rows.

**pandas answer:** (same text as in the Code block)
```py
o = orders.sort_values(["customer_id", "order_date", "order_id"]).copy()
o["earlier_avg"] = o.groupby("customer_id")["amount"].transform(lambda s: s.expanding().mean().shift(1))
pd_df = (o[o["amount"] > o["earlier_avg"]]
         .sort_values("order_id").reset_index(drop=True))
```

**Example:**
- Customer 1: order 1 (100, 1 Jan), order 2 (200, 10 Jan), order 3 (150, 10 Jan), order 4 (90, 1 Feb).
- Order 1: no earlier orders, so the average is NULL and `200 > NULL` style comparisons are unknown: dropped.
- Order 2 (200): earlier orders are order 1 only (order 3 has the same date but a larger id, so it is not earlier): average 100; 200 > 100, kept.
- Order 3 (150): earlier orders are order 1 and order 2 (same date, smaller id): average (100 + 200) / 2 = 150; 150 > 150 is false (strict), dropped.
- Order 4 (90): earlier average (100 + 200 + 150) / 3 = 150; 90 is below, dropped.
- Customer 2: order 5 (50) has no earlier order; order 6 (70) has average 50, kept. Customer 3 has one order (500) and is dropped.
- Result: orders 2 and 6. A date-only version with no tie-break returns [2, 3, 6]: order 3 would be compared with order 1 only (average 100) and wrongly kept; my run printed that.

**Code:** run with `python3 -I`.
```python
# Q38: orders above the customer's average of EARLIER orders: correlated subquery with date and tie-break
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-01',100),(2,1,'2024-01-10',200),(3,1,'2024-01-10',150),(4,1,'2024-02-01',90),
 (5,2,'2024-01-05',50),(6,2,'2024-01-06',70),
 (7,3,'2024-01-09',500);
"""
SQL_MAIN = """
SELECT o.order_id, o.customer_id, o.order_date, o.amount,
       (SELECT AVG(p.amount) FROM orders p
        WHERE p.customer_id = o.customer_id
          AND (p.order_date < o.order_date
               OR (p.order_date = o.order_date AND p.order_id < o.order_id))) AS earlier_avg
FROM orders o
WHERE o.amount > (SELECT AVG(p.amount) FROM orders p
                  WHERE p.customer_id = o.customer_id
                    AND (p.order_date < o.order_date
                         OR (p.order_date = o.order_date AND p.order_id < o.order_id)))
ORDER BY o.order_id
"""
# the same condition with a row-value comparison
SQL_ROW = """
SELECT o.order_id, o.customer_id, o.order_date, o.amount,
       (SELECT AVG(p.amount) FROM orders p
        WHERE p.customer_id = o.customer_id AND (p.order_date, p.order_id) < (o.order_date, o.order_id)) AS earlier_avg
FROM orders o
WHERE o.amount > (SELECT AVG(p.amount) FROM orders p
                  WHERE p.customer_id = o.customer_id AND (p.order_date, p.order_id) < (o.order_date, o.order_id))
ORDER BY o.order_id
"""
SQL_ALL = """
SELECT o.order_id, (SELECT AVG(p.amount) FROM orders p
        WHERE p.customer_id = o.customer_id
          AND (p.order_date < o.order_date OR (p.order_date = o.order_date AND p.order_id < o.order_id))) AS earlier_avg
FROM orders o ORDER BY o.order_id
"""
SQL_DATE_ONLY = SQL_MAIN.replace("OR (p.order_date = o.order_date AND p.order_id < o.order_id)", "")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
row_df = pd.read_sql_query(SQL_ROW, con)
print("earlier average for every order (NULL = no earlier order):")
print(pd.read_sql_query(SQL_ALL, con).to_string(index=False))
print("\nSQL result (amount > earlier average):")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, row_df)
print("\nassert: row-value comparison (a, b) < (c, d) gives the same rows as the OR form")
print("date-only version (no tie-break):", [r[0] for r in con.execute(SQL_DATE_ONLY)], "| with tie-break:", sql_df["order_id"].tolist())

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.sort_values(["customer_id", "order_date", "order_id"]).copy()
o["earlier_avg"] = o.groupby("customer_id")["amount"].transform(lambda s: s.expanding().mean().shift(1))
pd_df = (o[o["amount"] > o["earlier_avg"]]
         .sort_values("order_id").reset_index(drop=True))
# pd:end
print("\npandas expanding().mean().shift(1):")
print(pd_df.to_string(index=False))
# compared by order_id
pd.testing.assert_frame_equal(sql_df, pd_df[["order_id", "customer_id", "order_date", "amount", "earlier_avg"]], check_dtype=False)
print("\nassert: SQL == pandas")
```

**Output (my run):**
```text
earlier average for every order (NULL = no earlier order):
 order_id  earlier_avg
        1          NaN
        2        100.0
        3        150.0
        4        150.0
        5          NaN
        6         50.0
        7          NaN

SQL result (amount > earlier average):
 order_id  customer_id order_date  amount  earlier_avg
        2            1 2024-01-10     200        100.0
        6            2 2024-01-06      70         50.0

assert: row-value comparison (a, b) < (c, d) gives the same rows as the OR form
date-only version (no tie-break): [2, 3, 6] | with tie-break: [2, 6]

pandas expanding().mean().shift(1):
 order_id  customer_id order_date  amount  earlier_avg
        2            1 2024-01-10     200        100.0
        6            2 2024-01-06      70         50.0

assert: SQL == pandas
```

**Edge cases:**
- **First order per customer:** `AVG` of an empty set is NULL, so the row is excluded; if you want first orders shown (for example with a flag), use `COALESCE` on the average or put the average in the SELECT list and filter later.
- **Same date:** without the `order_id` tie-break, orders on one date either all see each other as "not earlier" (strict `<` on date only) or all as "earlier"; the result then depends on the data layout, not on a rule.
- **ISO text dates:** `'2024-01-10' < '2024-02-01'` works because ISO strings sort like dates; other formats (`10/01/2024`) would not.
- **NULL amounts:** `AVG` skips them; I did not test NULL amounts in the pandas version, where `expanding().mean()` also skips NaN but the shift is by row, not by non-null row.
- **Equal to the average:** not kept (strict `>`).
- **Row-value comparison:** `(a, b) < (c, d)` compared lexicographically in SQLite 3.45, as the matching result shows. PostgreSQL and MySQL support row values too, as I recall (not executed here); SQL Server does not, as I recall.

**Then explain:**
- **Cost:** the inner `AVG` scans the customer's rows for every outer row, so a customer with k orders costs about k x k row visits. An index on `orders(customer_id, order_date, order_id)` can turn the inner scan into a range read (typical, not measured here).
- **Window alternative:** `AVG(amount) OVER (PARTITION BY customer_id ORDER BY order_date, order_id ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)` does it in one pass; the frame clause is Part 5, so I only name it.
- **pandas:** sort by customer, date and order_id; `expanding().mean()` is the mean of everything up to and including the current row, so `.shift(1)` moves it to "everything before". Doing the shift inside each group (inside the `transform`) matters: shifting the whole column would leak the previous customer's last average into the next customer's first row.
- **Equivalent without `shift`:** `(cumsum - amount) / (cumcount)` gives the earlier mean; not run here.

**Follow-ups:**
- *Earlier orders within the last 30 days only?* Add a date lower bound; date arithmetic is Part 6.
- *Compare with the customer's overall average instead?* That is Q31 (a non-correlated-by-date version).
- *What if order_id is not increasing with time?* It is only a tie-break among equal dates, so that is fine.

**Common mistakes:**
- Using `<=` on the date, which includes the order itself and its same-day peers.
- No tie-break for orders on the same date.
- Forgetting that the first order is dropped (and not realising it silently).
- In pandas, `expanding().mean()` without `shift`, which includes the current row, or `shift` on the whole frame instead of per group.

### Q39 ⭐ 🔴 Correlated subquery performance, concept and equivalence: a correlated COUNT subquery runs once per outer row, so n outer rows and m inner rows may cost about n times m without an index. Using orders(order_id, customer_id, amount) and customers(customer_id, name), write the customers with more than 3 orders as a correlated subquery in WHERE, as IN with GROUP BY HAVING, and as a join to a derived table, confirm the three give identical results on small data, and state how an index on orders(customer_id) and the optimiser's decorrelation change things (hedged by engine, not executed). Say EXPLAIN-level work belongs to Part 11.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** A correlated `COUNT` in `WHERE` is run once for each customer row, so without an index it costs roughly customers x orders; `IN` with `GROUP BY ... HAVING` and a join to a derived table compute the counts once and give the same rows, and an index on `orders(customer_id)` turns each inner scan into a lookup.

**Schema and sample data:** a small hand-checkable set, plus a larger synthetic one built in the Code block for the effort comparison.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
-- small set: customer 1 has 4 orders, 2 has 3, 3 has 5, 4 has 0, 5 has 1
```
(The inserts are generated by the `build()` function in the Code block.)

**SQL answer:** `SQL_MAIN` in the Code block, the correlated form.
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) > 3
ORDER BY c.customer_id
```
`SQL_IN` and `SQL_JOIN`, also in the Code block:
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE c.customer_id IN (SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) > 3)
ORDER BY c.customer_id
```
```sql
SELECT c.customer_id, c.name FROM customers c
JOIN (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id) s ON s.customer_id = c.customer_id
WHERE s.n > 3
ORDER BY c.customer_id
```

**pandas answer:** (same text as in the Code block)
```py
counts = orders.groupby("customer_id").size()
pd_df = (customers[customers["customer_id"].map(counts).fillna(0) > 3]
         .sort_values("customer_id").reset_index(drop=True))
```

**Example:** Order counts: customer 1 has 4, customer 2 has 3, customer 3 has 5, customer 4 has none, customer 5 has 1.
- "More than 3" keeps 4 and 5 orders: customers 1 and 3. Customer 2 has exactly 3, which is not more than 3.
- Correlated form: for customer 1 the inner query counts 4, for 2 it counts 3, for 4 it counts 0 (a `COUNT` over no rows is 0), and so on; five inner counts for five customers.
- `IN` form: the subquery groups the orders table once, keeps customer ids 1 and 3 (the ones with `COUNT(*) > 3`), and the outer query checks membership.
- Join form: the derived table has one row per customer that has orders (1: 4, 2: 3, 3: 5, 5: 1); joining and filtering `n > 3` leaves 1 and 3. A customer with zero orders (4) is not in the derived table; for "more than 3" that does not matter, but for "fewer than 3" or "exactly 0" it would.

**Code:** run with `python3 -I`.
```python
# Q39: three equivalent forms of "customers with more than 3 orders", and what an index changes
import sqlite3
import pandas as pd

def build(n_customers, orders_per):
    con = sqlite3.connect(":memory:")
    con.executescript("CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);"
                      "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);")
    con.executemany("INSERT INTO customers VALUES (?, ?)", [(c, "c%d" % c) for c in range(1, n_customers + 1)])
    oid = 0
    rows = []
    for c in range(1, n_customers + 1):
        for _ in range(orders_per(c)):
            oid += 1
            rows.append((oid, c, 10 + oid % 7))
    con.executemany("INSERT INTO orders VALUES (?, ?, ?)", rows)
    return con

SQL_MAIN = """
SELECT c.customer_id, c.name FROM customers c
WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) > 3
ORDER BY c.customer_id
"""
SQL_IN = """
SELECT c.customer_id, c.name FROM customers c
WHERE c.customer_id IN (SELECT customer_id FROM orders GROUP BY customer_id HAVING COUNT(*) > 3)
ORDER BY c.customer_id
"""
SQL_JOIN = """
SELECT c.customer_id, c.name FROM customers c
JOIN (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id) s ON s.customer_id = c.customer_id
WHERE s.n > 3
ORDER BY c.customer_id
"""
# small hand-checkable data: customer 1 has 4 orders, 2 has 3, 3 has 5, 4 has 0, 5 has 1
small = build(5, lambda c: {1: 4, 2: 3, 3: 5, 4: 0, 5: 1}[c])
res = {name: pd.read_sql_query(sql, small) for name, sql in [("correlated", SQL_MAIN), ("IN + HAVING", SQL_IN), ("join to derived", SQL_JOIN)]}
for k, v in res.items():
    print("%-16s ->" % k, v["customer_id"].tolist())
pd.testing.assert_frame_equal(res["correlated"], res["IN + HAVING"])
pd.testing.assert_frame_equal(res["correlated"], res["join to derived"])
print("assert: all three forms give the same rows (compared by customer_id)")

customers = pd.read_sql_query("SELECT * FROM customers", small)
orders = pd.read_sql_query("SELECT * FROM orders", small)
# pd:main
counts = orders.groupby("customer_id").size()
pd_df = (customers[customers["customer_id"].map(counts).fillna(0) > 3]
         .sort_values("customer_id").reset_index(drop=True))
# pd:end
pd.testing.assert_frame_equal(res["correlated"], pd_df)
print("pandas:", pd_df["customer_id"].tolist(), "| assert: SQL == pandas")

# how much work each form does: count SQLite virtual-machine instructions (a deterministic proxy for effort, not wall time)
def vm_steps(con, sql):
    n = [0]
    con.set_progress_handler(lambda: n.__setitem__(0, n[0] + 1) or 0, 1)
    rows = con.execute(sql).fetchall()
    con.set_progress_handler(None, 1)
    return n[0], len(rows)

big = build(300, lambda c: 1 + c % 7)     # 300 customers, 1..7 orders each
print("\nbig data: %d customers, %d orders" % (300, big.execute("SELECT COUNT(*) FROM orders").fetchone()[0]))
def report(label):
    out = {}
    for name, sql in [("correlated", SQL_MAIN), ("IN + HAVING", SQL_IN), ("join to derived", SQL_JOIN)]:
        out[name] = vm_steps(big, sql)
    print("%-28s" % label, {k: "%d steps, %d rows" % v for k, v in out.items()})
    return out
before = report("no index on orders:")
assert len({v[1] for v in before.values()}) == 1
plan = [r[3] for r in big.execute("EXPLAIN QUERY PLAN " + SQL_MAIN)]
print("plan (no index):  ", plan)
big.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
after = report("with index on customer_id:")
assert len({v[1] for v in after.values()}) == 1
plan = [r[3] for r in big.execute("EXPLAIN QUERY PLAN " + SQL_MAIN)]
print("plan (with index):", plan)
```

**Output (my run):**
```text
correlated       -> [1, 3]
IN + HAVING      -> [1, 3]
join to derived  -> [1, 3]
assert: all three forms give the same rows (compared by customer_id)
pandas: [1, 3] | assert: SQL == pandas

big data: 300 customers, 1203 orders
no index on orders:          {'correlated': '1448929 steps, 172 rows', 'IN + HAVING': '19785 steps, 172 rows', 'join to derived': '20989 steps, 172 rows'}
plan (no index):   ['SCAN c', 'CORRELATED SCALAR SUBQUERY 1', 'SCAN o']
with index on customer_id:   {'correlated': '8035 steps, 172 rows', 'IN + HAVING': '13768 steps, 172 rows', 'join to derived': '14972 steps, 172 rows'}
plan (with index): ['SCAN c', 'CORRELATED SCALAR SUBQUERY 1', 'SEARCH o USING COVERING INDEX idx_orders_customer (customer_id=?)']
```

**Edge cases:**
- **Customers with no orders:** invisible to the `IN` and join forms, and counted as 0 by the correlated form. They only matter for conditions like `= 0` or `< 3`; there use the correlated form, or a `LEFT JOIN` with `COALESCE(n, 0)`.
- **NULL `customer_id` in orders:** `GROUP BY` forms a NULL group in the `IN` form; `c.customer_id IN (..., NULL)` never matches the NULL, so nothing breaks, but `NOT IN` on this subquery would (Q33).
- **Exactly at the threshold:** `> 3` versus `>= 3`, checked by customer 2 (3 orders).
- **Duplicate customer rows:** the join form multiplies rows if `customers` has duplicates; the `IN` form does not.

**Then explain:**
- **The cost model:** the correlated inner query runs per outer row. For n customers and m orders with no index, the engine scans the orders table n times, about n x m row visits. With an index on `orders(customer_id)` each inner count is a lookup, so about n x (orders per customer).
- **What I measured:** as a deterministic stand-in for time I counted SQLite virtual-machine instructions (a progress handler counting each instruction) on 300 customers and 1203 orders. Without an index the correlated form took about 1.45 million steps and the other two about 20,000. After `CREATE INDEX` on `orders(customer_id)` the correlated form dropped to about 8,000, below the other two (about 13,800 and 15,000), because the lookups are cheap and the grouping forms still scan the whole orders table. All three returned the same 172 customers. This is an SQLite VM count on synthetic data, not wall time and not a claim about any other engine.
- **Plans:** `SCAN o` became `SEARCH o USING COVERING INDEX idx_orders_customer (customer_id=?)` after the index. EXPLAIN-level work belongs to Part 11.
- **Optimiser decorrelation (hedged, not executed):** some engines (I recall PostgreSQL, SQL Server, Oracle and others) can rewrite certain correlated subqueries into joins automatically; which ones, and on which versions, differs by engine, so check the plan instead of assuming. In SQLite 3.45 the plan kept the correlated subquery as a per-row lookup.
- **Readability:** the correlated form says what it means, the `IN` form is the shortest to get right, the join form is the one you extend when you need the count in the output.
- **pandas:** one `groupby` size, map it onto customers (`fillna(0)` for customers with no orders), filter.

**Follow-ups:**
- *Which would you pick?* The `IN` with `HAVING` form for a plain filter; the join form if I also need the count; the correlated form only when the logic really needs per-row context (Q31, Q38).
- *Does `EXISTS` help?* For "has at least one order" yes; for "more than 3" it needs a count, so no.
- *Is the correlated query always slower?* No; with an index on the inner column and a small outer set it can be the cheapest, as my run shows.

**Common mistakes:**
- Saying "correlated subqueries are always slow" or "the optimiser always fixes them", without looking at the plan.
- Forgetting the index on the inner table's join column.
- Using `COUNT(*) > 3` in a join form that drops customers whose count is 0 when the question needs them.
- Comparing the three forms on tiny data and concluding they cost the same.

### Q40 ⭐ 🔴 Dialect map for subqueries and CTEs (hedge everything not run on SQLite 3.45): scalar subquery returning many rows (first row in SQLite, error in PostgreSQL and MySQL), alias required on a derived table, ANY/SOME/ALL support, LIMIT inside IN subqueries (MySQL error 1235), UPDATE/DELETE reading the same table (MySQL error 1093), WITH before UPDATE, DELETE and INSERT, MATERIALIZED and NOT MATERIALIZED hints (SQLite 3.35+, PostgreSQL 12+), a derived table referenced once versus a CTE referenced many times, and LATERAL (not covered here). Present a table with a 'verified by running on SQLite' column and a 'hedged, not executed' column.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** On SQLite 3.45 I ran every row of the table below; the engines differ most on a many-row scalar subquery (SQLite returns the first row, PostgreSQL and MySQL are documented to raise an error), on `ANY`/`ALL` (SQLite has no syntax for them), and on rules about aliases, `LIMIT` in subqueries and modifying the table you read (all of which SQLite accepts); everything else is from the vendor documentation or memory and is marked "not executed".

**Schema and sample data:**
```sql
CREATE TABLE prices(id INTEGER PRIMARY KEY, price INTEGER);
CREATE TABLE new_prices(id INTEGER, new_price INTEGER);
CREATE TABLE archive(id INTEGER, price INTEGER);
INSERT INTO prices VALUES (1,10),(2,20),(3,30);
INSERT INTO new_prices VALUES (1,11),(3,33);
```

**SQL answer:** the one statement with a pandas twin is `UPDATE ... FROM` (`SQL_MAIN` in the Code block; SQLite 3.33 and later). All other probes are one-line statements run by the `probe()` helper in the Code block, each on a fresh copy of the tables.
```sql
UPDATE prices SET price = n.new_price FROM new_prices n WHERE prices.id = n.id
```

**pandas answer:** (same text as in the Code block)
```py
pd_df = base.assign(price=base["id"].map(newp.set_index("id")["new_price"]).fillna(base["price"]).astype("int64"))
```

**Example:** `prices` holds ids 1, 2, 3 at 10, 20, 30; `new_prices` has 1 -> 11 and 3 -> 33. `UPDATE ... FROM` joins each row of `prices` to its `new_prices` row and rewrites it: 1 becomes 11, 3 becomes 33, and 2 has no match so it stays 20. The pandas version maps `id` to the new price, and `fillna` keeps the old price where there is no new one.

**Code:** run with `python3 -I`.
```python
# Q40: dialect map for subqueries and CTEs: every SQLite row below is executed, nothing else is claimed as run
import sqlite3
import pandas as pd

print("SQLite version:", sqlite3.sqlite_version)

SCHEMA = """
CREATE TABLE prices(id INTEGER PRIMARY KEY, price INTEGER);
CREATE TABLE new_prices(id INTEGER, new_price INTEGER);
CREATE TABLE archive(id INTEGER, price INTEGER);
INSERT INTO prices VALUES (1,10),(2,20),(3,30);
INSERT INTO new_prices VALUES (1,11),(3,33);
"""
# UPDATE ... FROM: the one statement that also has a pandas twin
SQL_MAIN = """
UPDATE prices SET price = n.new_price FROM new_prices n WHERE prices.id = n.id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.execute(SQL_MAIN)
sql_df = pd.read_sql_query("SELECT id, price FROM prices ORDER BY id", con)
base = pd.DataFrame({"id": [1, 2, 3], "price": [10, 20, 30]})
newp = pd.DataFrame({"id": [1, 3], "new_price": [11, 33]})
# pd:main
pd_df = base.assign(price=base["id"].map(newp.set_index("id")["new_price"]).fillna(base["price"]).astype("int64"))
# pd:end
print("\nUPDATE ... FROM result (SQLite):")
print(sql_df.to_string(index=False))
print("pandas map + fillna:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df)
print("assert: SQL UPDATE ... FROM == pandas map/fillna (compared by id)")

def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c

def probe(label, sql, after=None):
    c = fresh()
    try:
        cur = c.execute(sql)
        rows = cur.fetchall() if cur.description else "ok"
        if after:
            rows = "%s; then %s" % (rows, c.execute(after).fetchall())
        print("%-46s -> %s" % (label, rows))
    except sqlite3.Error as e:
        print("%-46s -> ERROR: %s" % (label, e))

print("\n--- scalar subquery returning many rows ---")
probe("SELECT (SELECT price FROM prices)", "SELECT (SELECT price FROM prices)")
probe("SELECT (... ORDER BY price DESC)", "SELECT (SELECT price FROM prices ORDER BY price DESC)")
probe("SELECT ... WHERE price = (SELECT price FROM prices)", "SELECT id FROM prices WHERE price = (SELECT price FROM prices)")
print("pandas twin: Series([10, 20, 30]).item() ->", end=" ")
try:
    pd.Series([10, 20, 30]).item()
except ValueError as e:
    print("ValueError:", e)

print("\n--- alias on a derived table ---")
probe("SELECT * FROM (SELECT 1 AS a)", "SELECT * FROM (SELECT 1 AS a)")
probe("SELECT t.a FROM (SELECT 1 AS a) t", "SELECT t.a FROM (SELECT 1 AS a) t")
probe("join of two un-aliased derived tables", "SELECT * FROM (SELECT 1 AS a) JOIN (SELECT 1 AS b) ON a = b")
probe("two un-aliased derived tables, same column name", "SELECT a FROM (SELECT 1 AS a) JOIN (SELECT 1 AS a)")

print("\n--- ANY / SOME / ALL ---")
probe("price > ANY (SELECT ...)", "SELECT id FROM prices WHERE price > ANY (SELECT price FROM prices)")
probe("price > ALL (SELECT ...)", "SELECT id FROM prices WHERE price > ALL (SELECT price FROM prices)")
probe("price = SOME (SELECT ...)", "SELECT id FROM prices WHERE price = SOME (SELECT price FROM prices)")
probe("emulation: price > (SELECT MIN(price) ...)", "SELECT id FROM prices WHERE price > (SELECT MIN(price) FROM prices)")
probe("emulation: price >= (SELECT MAX(price) ...)", "SELECT id FROM prices WHERE price >= (SELECT MAX(price) FROM prices)")

print("\n--- LIMIT inside IN, LIMIT / OFFSET forms ---")
probe("IN (SELECT ... ORDER BY ... LIMIT 2)", "SELECT id FROM prices WHERE id IN (SELECT id FROM prices ORDER BY price DESC LIMIT 2) ORDER BY id")
probe("LIMIT 1 + 1", "SELECT id FROM prices ORDER BY id LIMIT 1 + 1")
probe("LIMIT (SELECT COUNT(*) - 1 ...)", "SELECT id FROM prices ORDER BY id LIMIT (SELECT COUNT(*) - 1 FROM prices)")
probe("LIMIT -1 OFFSET 1", "SELECT id FROM prices ORDER BY id LIMIT -1 OFFSET 1")
probe("OFFSET alone", "SELECT id FROM prices ORDER BY id OFFSET 1")

print("\n--- UPDATE / DELETE reading the table they change ---")
probe("UPDATE ... WHERE price > (SELECT AVG(price) same table)", "UPDATE prices SET price = price + 1 WHERE price > (SELECT AVG(price) FROM prices)", after="SELECT id, price FROM prices ORDER BY id")
probe("DELETE ... WHERE price < (SELECT AVG(price) same table)", "DELETE FROM prices WHERE price < (SELECT AVG(price) FROM prices)", after="SELECT id, price FROM prices ORDER BY id")
probe("DELETE ... WHERE id IN (SELECT id FROM same table)", "DELETE FROM prices WHERE id IN (SELECT id FROM prices WHERE price > 15)", after="SELECT id, price FROM prices ORDER BY id")

print("\n--- WITH before UPDATE, DELETE, INSERT ---")
probe("WITH ... UPDATE", "WITH hi AS (SELECT id FROM prices WHERE price > 15) UPDATE prices SET price = 0 WHERE id IN (SELECT id FROM hi)", after="SELECT id, price FROM prices ORDER BY id")
probe("WITH ... DELETE", "WITH hi AS (SELECT id FROM prices WHERE price > 15) DELETE FROM prices WHERE id IN (SELECT id FROM hi)", after="SELECT id, price FROM prices ORDER BY id")
probe("WITH ... INSERT INTO ... SELECT", "WITH hi AS (SELECT id, price FROM prices WHERE price > 15) INSERT INTO archive SELECT id, price FROM hi", after="SELECT id, price FROM archive ORDER BY id")
probe("INSERT INTO ... WITH ... SELECT", "INSERT INTO archive WITH hi AS (SELECT id, price FROM prices WHERE price > 15) SELECT id, price FROM hi", after="SELECT id, price FROM archive ORDER BY id")
probe("INSERT ... SELECT ... RETURNING", "INSERT INTO archive SELECT id, price FROM prices WHERE price > 15 RETURNING id")

print("\n--- UPDATE ... FROM (shown above), row values ---")
probe("(a, b) < (c, d)", "SELECT (1, 2) < (1, 3), (1, 2) = (1, 2), (1, NULL) = (1, 2)")
probe("(id, price) IN (SELECT id, price ...)", "SELECT id FROM prices WHERE (id, price) IN (SELECT id, price FROM prices WHERE price > 15) ORDER BY id")
probe("(id, price) IN (VALUES (1, 10), (3, 30))", "SELECT id FROM prices WHERE (id, price) IN (VALUES (1, 10), (3, 30)) ORDER BY id")

print("\n--- CTE rules ---")
probe("CTE used twice", "WITH t AS (SELECT price FROM prices) SELECT (SELECT MAX(price) FROM t), (SELECT MIN(price) FROM t)")
probe("MATERIALIZED / NOT MATERIALIZED", "WITH a AS MATERIALIZED (SELECT 1 AS x), b AS NOT MATERIALIZED (SELECT 2 AS y) SELECT x, y FROM a, b")
probe("CTE with column list", "WITH t(a, b) AS (SELECT id, price FROM prices) SELECT a, b FROM t ORDER BY a LIMIT 1")
probe("later CTE referenced by an earlier one", "WITH a AS (SELECT * FROM b), b AS (SELECT 1 AS x) SELECT * FROM a")
probe("earlier CTE referenced by a later one", "WITH b AS (SELECT 1 AS x), a AS (SELECT * FROM b) SELECT * FROM a")
probe("derived table name reused outside its scope", "SELECT * FROM (SELECT 1 AS x) d, d")
probe("WITH inside a subquery", "SELECT * FROM (WITH t AS (SELECT 5 AS v) SELECT v FROM t)")
probe("two WITH keywords in a row", "WITH a AS (SELECT 1 AS x) WITH b AS (SELECT 2 AS y) SELECT * FROM a, b")

print("\n--- LATERAL ---")
probe("LATERAL (SELECT ...)", "SELECT * FROM prices p, LATERAL (SELECT 1 AS x WHERE p.id > 0)")
```

**Output (my run):**
```text
SQLite version: 3.45.1

UPDATE ... FROM result (SQLite):
 id  price
  1     11
  2     20
  3     33
pandas map + fillna:
 id  price
  1     11
  2     20
  3     33
assert: SQL UPDATE ... FROM == pandas map/fillna (compared by id)

--- scalar subquery returning many rows ---
SELECT (SELECT price FROM prices)              -> [(10,)]
SELECT (... ORDER BY price DESC)               -> [(30,)]
SELECT ... WHERE price = (SELECT price FROM prices) -> [(1,)]
pandas twin: Series([10, 20, 30]).item() -> ValueError: can only convert an array of size 1 to a Python scalar

--- alias on a derived table ---
SELECT * FROM (SELECT 1 AS a)                  -> [(1,)]
SELECT t.a FROM (SELECT 1 AS a) t              -> [(1,)]
join of two un-aliased derived tables          -> [(1, 1)]
two un-aliased derived tables, same column name -> ERROR: ambiguous column name: a

--- ANY / SOME / ALL ---
price > ANY (SELECT ...)                       -> ERROR: near "SELECT": syntax error
price > ALL (SELECT ...)                       -> ERROR: near "ALL": syntax error
price = SOME (SELECT ...)                      -> ERROR: near "SELECT": syntax error
emulation: price > (SELECT MIN(price) ...)     -> [(2,), (3,)]
emulation: price >= (SELECT MAX(price) ...)    -> [(3,)]

--- LIMIT inside IN, LIMIT / OFFSET forms ---
IN (SELECT ... ORDER BY ... LIMIT 2)           -> [(2,), (3,)]
LIMIT 1 + 1                                    -> [(1,), (2,)]
LIMIT (SELECT COUNT(*) - 1 ...)                -> [(1,), (2,)]
LIMIT -1 OFFSET 1                              -> [(2,), (3,)]
OFFSET alone                                   -> ERROR: near "OFFSET": syntax error

--- UPDATE / DELETE reading the table they change ---
UPDATE ... WHERE price > (SELECT AVG(price) same table) -> ok; then [(1, 10), (2, 20), (3, 31)]
DELETE ... WHERE price < (SELECT AVG(price) same table) -> ok; then [(2, 20), (3, 30)]
DELETE ... WHERE id IN (SELECT id FROM same table) -> ok; then [(1, 10)]

--- WITH before UPDATE, DELETE, INSERT ---
WITH ... UPDATE                                -> ok; then [(1, 10), (2, 0), (3, 0)]
WITH ... DELETE                                -> ok; then [(1, 10)]
WITH ... INSERT INTO ... SELECT                -> ok; then [(2, 20), (3, 30)]
INSERT INTO ... WITH ... SELECT                -> ok; then [(2, 20), (3, 30)]
INSERT ... SELECT ... RETURNING                -> [(2,), (3,)]

--- UPDATE ... FROM (shown above), row values ---
(a, b) < (c, d)                                -> [(1, 1, None)]
(id, price) IN (SELECT id, price ...)          -> [(2,), (3,)]
(id, price) IN (VALUES (1, 10), (3, 30))       -> [(1,), (3,)]

--- CTE rules ---
CTE used twice                                 -> [(30, 10)]
MATERIALIZED / NOT MATERIALIZED                -> [(1, 2)]
CTE with column list                           -> [(1, 10)]
later CTE referenced by an earlier one         -> [(1,)]
earlier CTE referenced by a later one          -> [(1,)]
derived table name reused outside its scope    -> ERROR: no such table: d
WITH inside a subquery                         -> [(5,)]
two WITH keywords in a row                     -> ERROR: near "WITH": syntax error

--- LATERAL ---
LATERAL (SELECT ...)                           -> ERROR: near "SELECT": syntax error
```

**The map:**

| Feature | Verified by running on SQLite 3.45.1 | Hedged, not executed here |
|---|---|---|
| Scalar subquery returning many rows | No error; returns the first row it produces (10 with no ORDER BY, 30 with `ORDER BY price DESC`); used in `WHERE price = (...)` it also ran | PostgreSQL and MySQL are documented to raise an error when a scalar subquery returns more than one row |
| Alias on a derived table | `SELECT * FROM (SELECT 1 AS a)` ran without an alias; two un-aliased derived tables joined fine (a clash of column names gave `ambiguous column name`) | PostgreSQL (before 16, as I recall) and MySQL require an alias; Oracle does not; always write one |
| `ANY` / `SOME` / `ALL` | Syntax error for `> ANY (SELECT ...)`, `> ALL` and `= SOME`; emulate with `> (SELECT MIN(...))` and `>= (SELECT MAX(...))` (ran) | PostgreSQL and MySQL support `ANY`, `SOME` and `ALL` with a subquery; MySQL restricts them on `LIMIT` subqueries; semantics on an empty set per the PostgreSQL docs: `ALL` true, `ANY` false |
| `LIMIT` inside an `IN` subquery | Ran | MySQL raises error 1235 for `LIMIT` inside `IN`/`ALL`/`ANY`/`SOME` subqueries (number from the MySQL 8.4 restrictions page as summarised, not run); workaround is a derived table |
| `LIMIT`/`OFFSET` with expressions | `LIMIT 1 + 1`, `LIMIT (SELECT COUNT(*) - 1 ...)` and `LIMIT -1 OFFSET 1` ran; `OFFSET` without `LIMIT` is a syntax error | MySQL wants literals or variables as I recall; PostgreSQL accepts `OFFSET` alone and expressions |
| `UPDATE`/`DELETE` reading the table it changes | Ran in all three forms (subquery average, `IN` on same table) | MySQL error 1093 ("can't specify target table for update in FROM clause", number from memory and not on the page I read); workaround is a derived table wrapper |
| `UPDATE ... FROM` | Ran and matches the pandas result | PostgreSQL has it; MySQL and standard SQL use a multi-table `UPDATE` or a correlated subquery instead; SQL Server has `UPDATE ... FROM` with different join syntax |
| `WITH` before `UPDATE`, `DELETE`, `INSERT` | Ran: `WITH ... UPDATE`, `WITH ... DELETE`, `WITH ... INSERT INTO ... SELECT` and `INSERT INTO ... WITH ... SELECT` | MySQL 8.4: `WITH` before `UPDATE`, `DELETE` and `SELECT`, and `WITH` inside `INSERT ... SELECT` (per its CTE page, as summarised); PostgreSQL also has data-modifying CTEs (`WITH x AS (DELETE ... RETURNING ...)`) |
| Row-value comparison | `(1, 2) < (1, 3)` is true; `(1, NULL) = (1, 2)` is NULL; `(id, price) IN (SELECT ...)` and `IN (VALUES ...)` ran | PostgreSQL and MySQL support row values as I recall; SQL Server does not |
| `MATERIALIZED` / `NOT MATERIALIZED` | Both parse and ran (SQLite 3.35 and later); Q32 shows the plan change | PostgreSQL 12 and later has both hints (the version is not on the page I read); I did not check other engines |
| CTE referenced many times, derived table once | A CTE used twice ran; a derived table name used outside its subquery gives `no such table` | MySQL's docs say a derived table is derived again for each reference |
| CTE order and syntax | A later CTE referenced by an earlier one ran in SQLite; `WITH inside a subquery` ran; two `WITH` keywords in a row is a syntax error | MySQL: a CTE may refer only to earlier CTEs in the list (per its page); one `WITH` per query level |
| `LATERAL` | Syntax error in SQLite 3.45 | PostgreSQL, MySQL 8.0.14 and later, Oracle (as `LATERAL` and `CROSS APPLY`), SQL Server (`CROSS APPLY`), Snowflake and BigQuery have forms of it; not covered here |

**Edge cases:**
- **SQLite accepts more than other engines:** a query that runs on SQLite is not proof that it runs elsewhere. The first-row scalar subquery is the dangerous one, since the answer depends on the row order the engine happens to produce.
- **Version dependence inside SQLite:** `UPDATE ... FROM` needs 3.33, `MATERIALIZED` hints 3.35, `RETURNING` 3.35; the Code block prints `sqlite3.sqlite_version` (3.45.1 in my run).
- **Row order of the many-row scalar subquery:** with no `ORDER BY` the result is not guaranteed; I saw 10 because that row came first.

**Then explain:**
- **What is portable:** the standard forms: always alias derived tables, avoid `ANY`/`ALL` in favour of `MIN`/`MAX` or `EXISTS`, never rely on a many-row scalar subquery, put `WITH` at the start of the statement when you can, and use a derived-table wrapper when MySQL complains about the target table.
- **pandas twin:** `Series.item()` on a three-element Series raises `ValueError` (printed in the output), the strict behaviour the other engines apply to a many-row scalar subquery; `map` plus `fillna` is the `UPDATE ... FROM` equivalent.
- **Honest limit:** this is a map of what I ran and what I recall or read in documentation; in an interview say "I would check the manual for that engine" for any hedged cell.

**Follow-ups:**
- *Is `LATERAL` covered?* No, not in Part 3; the SQLite syntax error is shown only to prove it is unavailable here.
- *Why does a derived table need an alias in some engines?* They require every table expression in `FROM` to have a name so columns can be qualified.
- *How to emulate `ALL`?* `price > ALL (S)` is `price > (SELECT MAX(...))` when S is non-empty; on an empty S, `ALL` is true while `> (SELECT MAX)` is NULL, so add `OR NOT EXISTS`.

**Common mistakes:**
- Treating "it ran on SQLite" as "it is standard".
- Relying on the first-row scalar subquery.
- Using `ANY`/`ALL` in code meant to be portable to SQLite.
- Quoting MySQL error numbers or PostgreSQL version numbers with more confidence than the source gives.
