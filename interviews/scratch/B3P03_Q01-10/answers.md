### Q1 ⭐⭐⭐ 🟢 Scalar subquery in WHERE and in SELECT: employees(emp_id, name, dept_id, salary) has some NULL salaries. List employees earning more than the company average salary, and in a second query show each employee's salary next to the company average and the difference. Explain that an uncorrelated scalar subquery is evaluated once, that AVG ignores NULL salaries, what happens to a NULL salary row in the comparison, and give the pandas boolean-mask version (mean computed once, NaN rows dropped by the comparison).
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
**Say this first (1 line):** An uncorrelated scalar subquery runs once, gives one number, and the outer query compares every row to it; AVG skips NULL salaries, and a NULL salary compared with that number is unknown, so the row drops out of the WHERE.

**Schema and sample data:** six employees, two with a NULL salary.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',20,90),
                             (4,'Dev',20,NULL),(5,'Esha',30,40),(6,'Farid',30,NULL);
```

**SQL answer:** the filter is `SQL_MAIN`, the side-by-side version is `SQL_DIFF` (both in the Code block).
```sql
SELECT emp_id, name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY emp_id
```
```sql
SELECT emp_id, name, salary,
       (SELECT AVG(salary) FROM employees) AS company_avg,
       salary - (SELECT AVG(salary) FROM employees) AS diff
FROM employees
ORDER BY emp_id
```

**pandas answer:** compute the mean once as a Python number, then use a boolean mask. NaN compared with a number is False, so NaN rows drop out, the same as SQL.
```python
avg = emp["salary"].mean()                      # skipna=True, like AVG
pd_main = emp[emp["salary"] > avg][["emp_id", "name", "salary"]]
pd_diff = emp.assign(company_avg=avg, diff=emp["salary"] - avg)[
    ["emp_id", "name", "salary", "company_avg", "diff"]]
```

**Example:** the non-NULL salaries are 50, 70, 90, 40, so AVG = 250 / 4 = 62.5.
- Filter: 70 > 62.5 and 90 > 62.5 pass. 50 and 40 fail. Dev and Farid have NULL salary, so `NULL > 62.5` is unknown and they are not returned.
- Side by side: every row gets 62.5 in `company_avg`. The diff is -12.5, 7.5, 27.5, -22.5, and NULL for Dev and Farid (NULL minus anything is NULL). All six rows stay, because there is no WHERE.
- If someone "fixes" the NULLs with `COALESCE(salary, 0)`, the average becomes 250 / 6 = 41.67 and Asha (50) now qualifies. The Code block runs that contrast, and it returns Asha, Ben, Chitra.

**Code:** run with `python3 -I`.
```python
# Q1: scalar subquery in WHERE and in SELECT; NULL salaries; evaluated once
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',20,90),
                             (4,'Dev',20,NULL),(5,'Esha',30,40),(6,'Farid',30,NULL);
"""
SQL_MAIN = """
SELECT emp_id, name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY emp_id
"""
SQL_DIFF = """
SELECT emp_id, name, salary,
       (SELECT AVG(salary) FROM employees) AS company_avg,
       salary - (SELECT AVG(salary) FROM employees) AS diff
FROM employees
ORDER BY emp_id
"""
SQL_ZERO = """
SELECT emp_id, name, salary
FROM employees
WHERE COALESCE(salary, 0) > (SELECT AVG(COALESCE(salary, 0)) FROM employees)
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_diff = pd.read_sql_query(SQL_DIFF, con)
sql_zero = pd.read_sql_query(SQL_ZERO, con)
print("SQL above company average (AVG ignores NULL):")
print(sql_main.to_string(index=False))
print("\nSQL salary next to the company average:")
print(sql_diff.to_string(index=False))
print("\nContrast, NULL treated as 0 (average over all 6 rows):")
print(sql_zero.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
avg = emp["salary"].mean()                      # skipna=True, like AVG
pd_main = emp[emp["salary"] > avg][["emp_id", "name", "salary"]]
pd_diff = emp.assign(company_avg=avg, diff=emp["salary"] - avg)[
    ["emp_id", "name", "salary", "company_avg", "diff"]]
# pd:end
print("\npandas mean of salary:", avg)
print(pd_main.to_string(index=False))
print(pd_diff.to_string(index=False))

# compared after sorting both by emp_id (NaN == NaN is treated as equal by assert_frame_equal)
pd.testing.assert_frame_equal(sql_main.reset_index(drop=True), pd_main.sort_values("emp_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_diff.sort_values("emp_id").reset_index(drop=True), pd_diff.sort_values("emp_id").reset_index(drop=True), check_dtype=False)

# does the uncorrelated subquery run once? count calls of a Python function inside it
calls = {"n": 0}
def tick(x):
    calls["n"] += 1
    return x
con.create_function("tick", 1, tick)
con.execute("SELECT emp_id FROM employees WHERE salary > (SELECT AVG(tick(salary)) FROM employees)").fetchall()
print("\ntick() calls with an uncorrelated subquery over 6 rows:", calls["n"])
assert calls["n"] == 6
print("asserts passed: SQL == pandas for both queries")
```

**Output (my run):**
```text
SQL above company average (AVG ignores NULL):
 emp_id   name  salary
      2    Ben      70
      3 Chitra      90

SQL salary next to the company average:
 emp_id   name  salary  company_avg  diff
      1   Asha    50.0         62.5 -12.5
      2    Ben    70.0         62.5   7.5
      3 Chitra    90.0         62.5  27.5
      4    Dev     NaN         62.5   NaN
      5   Esha    40.0         62.5 -22.5
      6  Farid     NaN         62.5   NaN

Contrast, NULL treated as 0 (average over all 6 rows):
 emp_id   name  salary
      1   Asha      50
      2    Ben      70
      3 Chitra      90

pandas mean of salary: 62.5
 emp_id   name  salary
      2    Ben    70.0
      3 Chitra    90.0
 emp_id   name  salary  company_avg  diff
      1   Asha    50.0         62.5 -12.5
      2    Ben    70.0         62.5   7.5
      3 Chitra    90.0         62.5  27.5
      4    Dev     NaN         62.5   NaN
      5   Esha    40.0         62.5 -22.5
      6  Farid     NaN         62.5   NaN

tick() calls with an uncorrelated subquery over 6 rows: 6
asserts passed: SQL == pandas for both queries
```

**Edge cases:**
- NULL salaries are excluded from the average and from the result of the comparison. In the SELECT-list version they stay as rows with a NULL diff.
- If every salary were NULL, `AVG` would be NULL, the comparison unknown, and the query would return no rows (I did not run that case).
- The numerator and denominator both count only non-NULL rows: AVG is SUM of non-NULL divided by COUNT of non-NULL, not divided by the row count.
- In pandas the NULL column is `float64` with NaN, which is why the printed salaries show `70.0`.

**Then explain:**
- **Scalar subquery:** a subquery that returns one row and one column, so it can sit anywhere a single value can: in WHERE, in the SELECT list, in HAVING.
- **Once, not per row:** the subquery does not mention the outer table, so it is uncorrelated and its result does not change from row to row. The SQLite docs say an uncorrelated subquery is evaluated once and a correlated one is re-evaluated per outer row. My check: I wrapped a Python function around the salary inside the subquery and counted calls. It was called 6 times, once per table row, for the whole 6-row query, not 36. That is SQLite on this query; another engine's optimiser may differ (not executed).
- **Why AVG ignores NULL:** every aggregate except `COUNT(*)` skips NULLs. That is usually what you want; say it out loud so the interviewer knows you checked.
- **pandas:** `emp["salary"].mean()` also skips NaN by default (`skipna=True`), so the two agree. I take the mean outside the mask so it is computed once.
- Correlated versions (average per department) are Q5; the window-function form of "salary versus average" is Part 4.

**Follow-ups:**
- *Why not write `WHERE salary > AVG(salary)`?* WHERE runs before aggregation, so aggregates are not allowed there; the subquery computes the aggregate first. HAVING is for filtering groups (Q12).
- *How do you also show NULL-salary employees in the "above average" list?* Decide what NULL means first; if it means zero, use `COALESCE`, and say the average then changes.
- *Does the subquery cost an extra pass over the table?* One extra pass for the uncorrelated form; the call count above shows one read per row.

**Common mistakes:**
- Using `COALESCE(salary, 0)` inside the AVG and not noticing the average dropped.
- Writing `WHERE salary > AVG(salary)`.
- Expecting the NULL-salary rows to appear in the filter result, or to be counted as below average.
- In pandas, computing `emp["salary"].mean()` inside a per-row apply, which recomputes it for every row.

### Q2 ⭐⭐⭐ 🟢 What happens when a scalar subquery returns more than one row, or none? products(product_id, name, category, price): write WHERE price = (SELECT price FROM products WHERE category = 'Books') where Books has several rows, and a variant where the category has no rows. State the behaviour per engine (SQLite uses the first row silently, PostgreSQL and MySQL raise an error, hedged as not executed), what zero rows gives (NULL, so no rows match), and the safe rewrites (MAX or MIN, IN, LIMIT 1 with ORDER BY, or a join).
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** SQLite does not complain when a scalar subquery returns several rows: it silently takes the first one, which without ORDER BY is whatever row it meets first; zero rows gives NULL, so `price = NULL` is unknown and nothing matches; the safe fix is to say what you mean with MAX, MIN, IN, ORDER BY ... LIMIT 1, or a join.

**Schema and sample data:** Books has three rows (10, 20, 15, in that table order), Games has none.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Novel','Books',10),(2,'Atlas','Books',20),(3,'Comic','Books',15),
                            (4,'Ball','Toys',5),(5,'Pen','Stationery',10),(6,'Kite','Toys',20);
```

**SQL answer:** all in the Code block. The broken query (many rows):
```sql
SELECT product_id, name, price FROM products
WHERE price = (SELECT price FROM products WHERE category = 'Books')
ORDER BY product_id
```
The zero-row variant, and the same empty subquery in a SELECT list:
```sql
SELECT product_id, name, price FROM products
WHERE price = (SELECT price FROM products WHERE category = 'Games')
ORDER BY product_id
```
```sql
SELECT (SELECT price FROM products WHERE category = 'Games') AS picked
```
Safe rewrites. If you mean "the highest Books price":
```sql
SELECT product_id, name, price FROM products
WHERE price = (SELECT MAX(price) FROM products WHERE category = 'Books')
ORDER BY product_id
```
If you mean "any Books price":
```sql
SELECT product_id, name, price FROM products
WHERE price IN (SELECT price FROM products WHERE category = 'Books')
ORDER BY product_id
```
Same as the MAX one, with the pick made explicit:
```sql
SELECT product_id, name, price FROM products
WHERE price = (SELECT price FROM products WHERE category = 'Books' ORDER BY price DESC LIMIT 1)
ORDER BY product_id
```
And the join form (equal to the IN form on this data):
```sql
SELECT p.product_id, p.name, p.price
FROM products p
JOIN (SELECT DISTINCT price FROM products WHERE category = 'Books') b ON b.price = p.price
ORDER BY p.product_id
```

**pandas answer:** pandas has no silent first-row rule; you pick the value explicitly. `books.iloc[0]` mimics SQLite, and is the thing you should not rely on in either tool.
```python
books = prod.loc[prod["category"] == "Books", "price"]
pd_first = prod[prod["price"] == books.iloc[0]]                 # mimic SQLite: first Books row
pd_empty = prod[prod["price"].isin(prod.loc[prod["category"] == "Games", "price"])]
pd_max = prod[prod["price"] == books.max()]
pd_in = prod[prod["price"].isin(books)]
```

**Example:** Books prices in table order are 10, 20, 15.
- Naive query: SQLite takes the first row, 10, and returns products with price 10: Novel (id 1) and Pen (id 5). No error. If the table order changed, a different price would be picked, with no warning.
- With `ORDER BY price DESC` inside the subquery, the first row is 20, so the picked value is 20 (the Code block prints 20).
- Games has no rows, so the subquery gives NULL (printed as `None`), `price = NULL` is unknown, and the WHERE returns 0 rows.
- MAX rewrite: 20, so Atlas and Kite. IN rewrite: 10, 20 or 15, so Novel, Atlas, Comic, Pen, Kite. Join rewrite: the same five.

**Code:** run with `python3 -I`.
```python
# Q2: scalar subquery returning many rows or none
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Novel','Books',10),(2,'Atlas','Books',20),(3,'Comic','Books',15),
                            (4,'Ball','Toys',5),(5,'Pen','Stationery',10),(6,'Kite','Toys',20);
"""
SQL_NAIVE = """
SELECT product_id, name, price FROM products
WHERE price = (SELECT price FROM products WHERE category = 'Books')
ORDER BY product_id
"""
SQL_FIRST_ORDERED = """
SELECT (SELECT price FROM products WHERE category = 'Books' ORDER BY price DESC) AS picked
"""
SQL_EMPTY = """
SELECT product_id, name, price FROM products
WHERE price = (SELECT price FROM products WHERE category = 'Games')
ORDER BY product_id
"""
SQL_EMPTY_SELECT = """
SELECT (SELECT price FROM products WHERE category = 'Games') AS picked
"""
SQL_MAX = """
SELECT product_id, name, price FROM products
WHERE price = (SELECT MAX(price) FROM products WHERE category = 'Books')
ORDER BY product_id
"""
SQL_IN = """
SELECT product_id, name, price FROM products
WHERE price IN (SELECT price FROM products WHERE category = 'Books')
ORDER BY product_id
"""
SQL_LIMIT1 = """
SELECT product_id, name, price FROM products
WHERE price = (SELECT price FROM products WHERE category = 'Books' ORDER BY price DESC LIMIT 1)
ORDER BY product_id
"""
SQL_JOIN = """
SELECT p.product_id, p.name, p.price
FROM products p
JOIN (SELECT DISTINCT price FROM products WHERE category = 'Books') b ON b.price = p.price
ORDER BY p.product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(s): return pd.read_sql_query(s, con)
naive, empty, mx, isin_, lim1, jn = q(SQL_NAIVE), q(SQL_EMPTY), q(SQL_MAX), q(SQL_IN), q(SQL_LIMIT1), q(SQL_JOIN)
print("Books rows in table order:", con.execute("SELECT price FROM products WHERE category='Books'").fetchall())
print("\nSQL naive (many-row scalar subquery), no error:")
print(naive.to_string(index=False))
print("\nOrdered many-row scalar subquery picks:", q(SQL_FIRST_ORDERED).iloc[0, 0])
print("Zero-row scalar subquery in SELECT list gives:", q(SQL_EMPTY_SELECT).iloc[0, 0])
print("\nSQL zero-row variant in WHERE:", len(empty), "rows")
print("\nSQL MAX rewrite:"); print(mx.to_string(index=False))
print("\nSQL IN rewrite:"); print(isin_.to_string(index=False))
print("\nSQL LIMIT 1 rewrite:"); print(lim1.to_string(index=False))
print("\nSQL join rewrite equals IN:", jn.equals(isin_))

prod = q("SELECT * FROM products")
# pd:main
books = prod.loc[prod["category"] == "Books", "price"]
pd_first = prod[prod["price"] == books.iloc[0]]                 # mimic SQLite: first Books row
pd_empty = prod[prod["price"].isin(prod.loc[prod["category"] == "Games", "price"])]
pd_max = prod[prod["price"] == books.max()]
pd_in = prod[prod["price"].isin(books)]
# pd:end
print("\npandas first-row mimic:", pd_first["product_id"].tolist(), "| empty:", len(pd_empty),
      "| max:", pd_max["product_id"].tolist(), "| isin:", pd_in["product_id"].tolist())
# all compared on product_id order
for a, b in [(naive, pd_first), (empty, pd_empty), (mx, pd_max), (isin_, pd_in)]:
    pd.testing.assert_frame_equal(a.reset_index(drop=True), b[["product_id", "name", "price"]].sort_values("product_id").reset_index(drop=True), check_dtype=False)
assert jn.equals(isin_)
# a many-row scalar comparison in pandas has no silent first-row rule: == against a Series aligns by index
try:
    prod[prod["price"] == books]
except Exception as e:
    print("pandas == against a different-length Series:", type(e).__name__)
for stmt in ("SELECT 1 WHERE 10 = ANY (SELECT price FROM products)", "SELECT 1 WHERE 10 > ALL (SELECT price FROM products)"):
    try:
        con.execute(stmt)
    except sqlite3.Error as e:
        print("SQLite", stmt.split("WHERE")[1].split("(")[0].strip(), "->", type(e).__name__, "-", e)
print("asserts passed: SQL == pandas for every variant")
```

**Output (my run):**
```text
Books rows in table order: [(10,), (20,), (15,)]

SQL naive (many-row scalar subquery), no error:
 product_id  name  price
          1 Novel     10
          5   Pen     10

Ordered many-row scalar subquery picks: 20
Zero-row scalar subquery in SELECT list gives: None

SQL zero-row variant in WHERE: 0 rows

SQL MAX rewrite:
 product_id  name  price
          2 Atlas     20
          6  Kite     20

SQL IN rewrite:
 product_id  name  price
          1 Novel     10
          2 Atlas     20
          3 Comic     15
          5   Pen     10
          6  Kite     20

SQL LIMIT 1 rewrite:
 product_id  name  price
          2 Atlas     20
          6  Kite     20

SQL join rewrite equals IN: True

pandas first-row mimic: [1, 5] | empty: 0 | max: [2, 6] | isin: [1, 2, 3, 5, 6]
pandas == against a different-length Series: ValueError
SQLite 10 = ANY -> OperationalError - near "SELECT": syntax error
SQLite 10 > ALL -> OperationalError - near "ALL": syntax error
asserts passed: SQL == pandas for every variant
```

**Edge cases:**
- Zero rows: the scalar subquery yields NULL, so an `=` comparison matches nothing, and `<>` matches nothing either (unknown, not true). A `NOT IN` against an empty subquery, by contrast, is true for every row (that is a different shape, IN, not a scalar).
- Duplicates in the join form: I used `SELECT DISTINCT price` in the derived table, otherwise a repeated Books price would repeat the product rows.
- NULL prices in Books: MAX ignores them; IN will never match a NULL price on the outer side.
- If the subquery returns many rows and I use `ORDER BY ... LIMIT 1` without a tie-break, ties on the sort column still leave the pick arbitrary (the price value is the same here, so the result is stable).

**Then explain:**
- **What I ran:** the SQLite behaviour above, on SQLite 3.45.1. The docs say a scalar subquery takes the first row; they do not say which row is first without ORDER BY, so I do not rely on it.
- **PostgreSQL and MySQL (not executed here):** I recall PostgreSQL raises "more than one row returned by a subquery used as an expression" and MySQL raises error 1242 "Subquery returns more than 1 row". These are from the vendor docs and memory; I did not run them. So a query that "works" in SQLite can fail on migration.
- **ANY and ALL:** `price = ANY (SELECT ...)` and `price > ALL (SELECT ...)` are standard SQL and PostgreSQL and MySQL support them (not executed). SQLite does not: both forms gave `near "SELECT": syntax error` and `near "ALL": syntax error` in my run. In SQLite use IN, `> (SELECT MAX(...))`, or `NOT EXISTS`. `= ANY` is the same as IN; `> ALL` is the same as `> MAX` when the subquery has rows, and is true for every row when it has none (hedged, standard rule, not executed).
- **Choosing the rewrite:** say what the business question is. "Equal to the largest" is MAX; "equal to any of them" is IN; "the single cheapest" is ORDER BY with LIMIT 1 and a tie-break rule.
- **pandas:** comparing a column to a Series of a different length is not a scalar comparison; it raises `ValueError` in my run. Pull the scalar out first (`.max()`, `.iloc[0]`) or use `isin`.

**Follow-ups:**
- *How would you make SQLite raise on many rows?* There is no switch; wrap it in `HAVING COUNT(*) = 1` on a derived table, or check the count in application code.
- *What about `LIMIT` inside an IN subquery?* MySQL rejects it (error 1235 per its docs, not executed); SQLite accepted `ORDER BY ... LIMIT 1` in the scalar subquery above; I did not run LIMIT inside an IN subquery.
- *Does zero rows ever give an error?* Not for a scalar subquery; it gives NULL.

**Common mistakes:**
- Trusting a query because it runs without error in SQLite.
- Adding `LIMIT 1` with no ORDER BY, which only hides the problem.
- Forgetting that the zero-row case turns `=` into "no rows" instead of an error, so a typo in the category silently returns nothing.
- Using `= ALL` or `ANY` in SQLite.

### Q3 ⭐⭐⭐ 🟢 The NOT IN NULL trap: customers(customer_id, name) and orders(order_id, customer_id, amount), where one order row has customer_id NULL. List customers who have never ordered using NOT IN (SELECT customer_id FROM orders). Show that it returns no rows, explain three-valued logic (x NOT IN (1, NULL) is never true), give the three fixes (filter IS NOT NULL inside the subquery, NOT EXISTS, LEFT JOIN ... IS NULL), and the pandas ~isin version, noting isin does not have this trap.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** If the NOT IN subquery returns even one NULL, `x NOT IN (...)` can never be true (it is false or unknown for every x), so the query returns nothing; fix it with `IS NOT NULL` inside the subquery, with NOT EXISTS, or with LEFT JOIN ... IS NULL.

**Schema and sample data:** order 104 has a NULL customer_id.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,50),(102,1,70),(103,2,30),(104,NULL,90);
```

**SQL answer:** the trap, then the three fixes (all in the Code block).
```sql
SELECT customer_id, name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY customer_id
```
Fix 1, filter the NULL out of the subquery:
```sql
SELECT customer_id, name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)
ORDER BY customer_id
```
Fix 2, NOT EXISTS:
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
```
Fix 3, anti-join:
```sql
SELECT c.customer_id, c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id
```

**pandas answer:** `~isin` has no such trap. The NaN in the orders column is just one more value that never equals a real customer id.
```python
pd_df = customers[~customers["customer_id"].isin(orders["customer_id"])][["customer_id", "name"]]
```

**Example:** the orders customer ids are {1, 1, 2, NULL}. Chitra (3) and Dev (4) never ordered.
- `3 NOT IN (1, 1, 2, NULL)` expands to `3 <> 1 AND 3 <> 1 AND 3 <> 2 AND 3 <> NULL`. The first three are true, the last is unknown (NULL), and true AND unknown is unknown. WHERE keeps only true rows, so the row is dropped. The same happens to Dev. Asha and Ben are false instead (for Asha, `1 <> 1` is false), so no customer is returned and the result has 0 rows.
- My run shows the truth values for `IN (1, NULL)`: `1 IN` is 1, `5 IN` is NULL, `5 NOT IN` is NULL, `1 NOT IN` is 0. The only way for NOT IN to be true is that the list has no NULL.
- With any of the three fixes the result is Chitra and Dev.

**Code:** run with `python3 -I`.
```python
# Q3: the NOT IN NULL trap
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,50),(102,1,70),(103,2,30),(104,NULL,90);
"""
SQL_TRAP = """
SELECT customer_id, name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY customer_id
"""
SQL_FIX1 = """
SELECT customer_id, name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)
ORDER BY customer_id
"""
SQL_FIX2 = """
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
"""
SQL_FIX3 = """
SELECT c.customer_id, c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id
"""
SQL_TRUTH = """
SELECT 1 IN (1, NULL) AS one_in, 5 IN (1, NULL) AS five_in, 5 NOT IN (1, NULL) AS five_not_in,
       1 NOT IN (1, NULL) AS one_not_in
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(s): return pd.read_sql_query(s, con)
trap, f1, f2, f3 = q(SQL_TRAP), q(SQL_FIX1), q(SQL_FIX2), q(SQL_FIX3)
print("NOT IN with a NULL in the subquery:", len(trap), "rows")
print("\nFix 1 (IS NOT NULL inside), fix 2 (NOT EXISTS), fix 3 (LEFT JOIN IS NULL):")
print(f1.to_string(index=False))
print("fix2 equals fix1:", f2.equals(f1), "| fix3 equals fix1:", f3.equals(f1))
print("\nTruth values (None means NULL):", con.execute(SQL_TRUTH).fetchone())

customers, orders = q("SELECT * FROM customers"), q("SELECT * FROM orders")
# pd:main
pd_df = customers[~customers["customer_id"].isin(orders["customer_id"])][["customer_id", "name"]]
# pd:end
print("\npandas ~isin (orders.customer_id has NaN):")
print(pd_df.to_string(index=False))
# compared after sorting by customer_id
pd.testing.assert_frame_equal(f1, pd_df.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
assert len(trap) == 0
assert f1.equals(f2) and f1.equals(f3)
print("\nisin treats NaN as a value: Series([nan]).isin([nan]) =", pd.Series([np.nan]).isin([np.nan]).tolist())
print("asserts passed: SQL fixes == pandas; the trap query returned no rows")
```

**Output (my run):**
```text
NOT IN with a NULL in the subquery: 0 rows

Fix 1 (IS NOT NULL inside), fix 2 (NOT EXISTS), fix 3 (LEFT JOIN IS NULL):
 customer_id   name
           3 Chitra
           4    Dev
fix2 equals fix1: True | fix3 equals fix1: True

Truth values (None means NULL): (1, None, None, 0)

pandas ~isin (orders.customer_id has NaN):
 customer_id   name
           3 Chitra
           4    Dev

isin treats NaN as a value: Series([nan]).isin([nan]) = [True]
asserts passed: SQL fixes == pandas; the trap query returned no rows
```

**Edge cases:**
- Empty subquery: `x NOT IN (empty)` is true for every row, and the SQLite docs say that holds even when x is NULL (my scratch check ran it with a non-NULL x and got every row; it is not in the Code block). So NOT IN is safe when the subquery is empty or has no NULLs, and unsafe otherwise.
- A NULL on the outer side: `NULL NOT IN (1, 2)` is unknown, so a customer with a NULL id is never returned by the trap query nor by `IS NOT NULL` fix 1; NOT EXISTS would return it, by the rules (NULL = anything is unknown, so no match exists; I did not run that case). Decide whether that is what you want.
- The trap is silent: no error, no warning. It depends on the data, so it can pass tests and fail in production when the first NULL arrives.
- LEFT JOIN fix: if orders had two rows for one customer you still get one row for the customer with no orders, because only unmatched rows survive the IS NULL filter.

**Then explain:**
- **Three-valued logic:** a comparison with NULL is unknown, not false. AND with an unknown can only be false or unknown, never true, so NOT IN with a NULL in the list cannot become true.
- **Which fix:** NOT EXISTS is the one I would write by default, because it does not care about NULLs and says what it means. `IS NOT NULL` inside the subquery is the quickest patch. LEFT JOIN ... IS NULL is the join form; check the IS NULL test is on a column that is never NULL when matched (here `order_id`).
- **Same table, not hedged:** all three fixes returned identical rows in my run.
- **pandas:** `isin` uses equality on values, so a NaN in the list does not poison the answer. Careful the other way: `Series([nan]).isin([nan])` is True in my run (pandas matches NaN to NaN, unlike SQL), so a NaN customer id in the left frame would count as "found" if the orders list also has NaN.
- Other engines: NOT IN and NULL follow the same standard rule in PostgreSQL and MySQL, to my knowledge (not executed).

**Follow-ups:**
- *Is IN affected the same way?* No: `x IN (1, NULL)` is true if x is 1 and unknown otherwise, so the NULL only fails to add matches, it does not block them.
- *Why not `COALESCE(customer_id, -1)` in the subquery?* It works if -1 is never a real id, but it is a magic number; `IS NOT NULL` says it more clearly.
- *Which is fastest?* Depends on the engine and indexes; I did not measure. On this toy data all three are the same.

**Common mistakes:**
- Using NOT IN against a nullable column and not testing with a NULL.
- Saying "NOT IN is slow, EXISTS is fast" as the reason, rather than the correctness difference.
- Fixing only the subquery and forgetting that the outer column can be NULL too.
- In pandas, assuming `merge` or `isin` will drop NaN keys like SQL does.

### Q4 ⭐⭐⭐ 🟢 EXISTS versus IN: customers(customer_id, name) and orders(order_id, customer_id, amount). List customers who have at least one order over 100 with EXISTS and with IN, explain why EXISTS ignores the select list (SELECT 1 versus SELECT *), why EXISTS never returns NULL, why duplicates in the subquery do not duplicate outer rows, how the two forms differ when the subquery column contains NULL, and give the pandas isin or merge version.
**Asked at:** GeeksforGeeks SQL interview questions (subquery, correlated subquery, EXISTS vs IN, CTE entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** EXISTS asks "is there at least one matching row" and returns true or false, so duplicates and the select list do not matter; IN compares a value to a list and, unlike EXISTS, a NULL in that list changes the answer for NOT IN but not for IN.

**Schema and sample data:** order 105 has a NULL customer_id and an amount over 100, so the subquery column contains a NULL.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,150),(102,1,200),(103,2,80),(104,3,120),(105,NULL,500);
```

**SQL answer:** all in the Code block. EXISTS:
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.amount > 100)
ORDER BY c.customer_id
```
IN:
```sql
SELECT customer_id, name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE amount > 100)
ORDER BY customer_id
```
Negations used for the NULL comparison:
```sql
SELECT customer_id, name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE amount > 100)
ORDER BY customer_id
```
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.amount > 100)
ORDER BY c.customer_id
```
`SQL_EXISTS_STAR` is the same as `SQL_EXISTS` with `SELECT *`, and `SQL_JOIN_DUP` joins customers to orders directly to show the duplicated rows.

**pandas answer:** `isin`, or a merge on the deduplicated key set (the merge duplicates customers without `drop_duplicates`).
```python
big = orders[orders["amount"] > 100]
pd_isin = customers[customers["customer_id"].isin(big["customer_id"])][["customer_id", "name"]]
pd_merge = customers.merge(big[["customer_id"]].drop_duplicates(), on="customer_id")[["customer_id", "name"]]
```

**Example:** orders over 100 are 101 and 102 (customer 1), 104 (customer 3), and 105 (NULL customer).
- EXISTS: Asha has a matching order, Chitra has one, Ben's only order is 80, Dev has none. Result: Asha, Chitra. Asha has two matching orders but EXISTS stops at the first, and the outer row appears once.
- IN: the subquery list is {1, 1, 3, NULL}. Asha and Chitra are in the list; Ben and Dev are not (unknown, so dropped). Same result as EXISTS.
- Negated: `NOT IN` returns 0 rows because of the NULL. `NOT EXISTS` returns Ben and Dev, the right answer.
- A plain JOIN with `amount > 100` returns Asha twice (customer ids 1, 1, 3), which is why a join is not a drop-in replacement.

**Code:** run with `python3 -I`.
```python
# Q4: EXISTS versus IN
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,150),(102,1,200),(103,2,80),(104,3,120),(105,NULL,500);
"""
SQL_EXISTS = """
SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.amount > 100)
ORDER BY c.customer_id
"""
SQL_EXISTS_STAR = """
SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT * FROM orders o WHERE o.customer_id = c.customer_id AND o.amount > 100)
ORDER BY c.customer_id
"""
SQL_IN = """
SELECT customer_id, name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE amount > 100)
ORDER BY customer_id
"""
SQL_NOT_IN = """
SELECT customer_id, name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE amount > 100)
ORDER BY customer_id
"""
SQL_NOT_EXISTS = """
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.amount > 100)
ORDER BY c.customer_id
"""
SQL_JOIN_DUP = """
SELECT c.customer_id, c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id AND o.amount > 100
ORDER BY c.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(s): return pd.read_sql_query(s, con)
ex, exs, inn, nin, nex, jd = q(SQL_EXISTS), q(SQL_EXISTS_STAR), q(SQL_IN), q(SQL_NOT_IN), q(SQL_NOT_EXISTS), q(SQL_JOIN_DUP)
print("EXISTS:"); print(ex.to_string(index=False))
print("EXISTS with SELECT * equal:", ex.equals(exs), "| IN equal:", ex.equals(inn))
print("\nNOT IN rows:", len(nin), "| NOT EXISTS rows:", nex["customer_id"].tolist())
print("Plain JOIN rows (Asha has 2 orders over 100):", jd["customer_id"].tolist())
print("EXISTS returns only 1/0:", con.execute("SELECT EXISTS (SELECT 1 FROM orders WHERE 0), EXISTS (SELECT NULL FROM orders)").fetchone())

customers, orders = q("SELECT * FROM customers"), q("SELECT * FROM orders")
# pd:main
big = orders[orders["amount"] > 100]
pd_isin = customers[customers["customer_id"].isin(big["customer_id"])][["customer_id", "name"]]
pd_merge = customers.merge(big[["customer_id"]].drop_duplicates(), on="customer_id")[["customer_id", "name"]]
# pd:end
pd_merge_dup = customers.merge(big[["customer_id"]], on="customer_id")
print("\npandas isin:", pd_isin["customer_id"].tolist(), "| merge on deduplicated keys:", pd_merge["customer_id"].tolist(),
      "| merge without drop_duplicates:", pd_merge_dup["customer_id"].tolist())
# compared after sorting by customer_id
for b in (pd_isin, pd_merge):
    pd.testing.assert_frame_equal(ex, b.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
assert len(nin) == 0 and nex["customer_id"].tolist() == [2, 4]
assert jd["customer_id"].tolist() == [1, 1, 3]
print("asserts passed: EXISTS == IN == pandas; NOT IN is empty, NOT EXISTS is [2, 4]")
```

**Output (my run):**
```text
EXISTS:
 customer_id   name
           1   Asha
           3 Chitra
EXISTS with SELECT * equal: True | IN equal: True

NOT IN rows: 0 | NOT EXISTS rows: [2, 4]
Plain JOIN rows (Asha has 2 orders over 100): [1, 1, 3]
EXISTS returns only 1/0: (0, 1)

pandas isin: [1, 3] | merge on deduplicated keys: [1, 3] | merge without drop_duplicates: [1, 1, 3]
asserts passed: EXISTS == IN == pandas; NOT IN is empty, NOT EXISTS is [2, 4]
```

**Edge cases:**
- EXISTS never returns NULL: it is true or false (SQLite gives 1 or 0). `EXISTS (SELECT NULL FROM orders)` was 1 in my run because a row exists, whatever it contains; the select list is not evaluated for its value.
- IN can return NULL (unknown), which WHERE treats like false; for IN that is harmless, for NOT IN it is the trap from Q3.
- Empty subquery: EXISTS is false, IN is false, NOT IN is true.
- Duplicates in the subquery do not duplicate outer rows with IN or EXISTS. They do with a JOIN.

**Then explain:**
- **SELECT 1 versus SELECT \*:** the same result. EXISTS only checks whether any row comes back, so the columns are irrelevant. Many people write `SELECT 1` to make that obvious; I ran both and they matched. Whether an engine does less work with one or the other I have not measured, and I would say optimisers generally treat them the same (not executed).
- **Correlated:** my EXISTS refers to `c.customer_id`, so conceptually it is checked per customer, and the engine can stop at the first match.
- **IN with a subquery:** is uncorrelated here, so conceptually the list is built once (I did not measure it). Many optimisers rewrite IN and EXISTS to the same semi-join (not executed here).
- **When I prefer which:** EXISTS when the condition has several columns or the inner side is nullable; IN when it is a short, simple list of keys.
- **pandas:** `isin` is the semi-join; `merge` is a join and multiplies rows unless the right side is unique.

**Follow-ups:**
- *Is EXISTS faster than IN?* It depends on the engine, the indexes and the data; do not claim it generally. I did not benchmark.
- *Can EXISTS use several columns?* Yes, in the correlation predicate, for example matching on customer and date.
- *How do I get a semi-join through a JOIN?* Deduplicate the right side first, as in my pandas merge.

**Common mistakes:**
- Using a JOIN and getting duplicate customers.
- Using NOT IN on a nullable column.
- Saying EXISTS returns the first row's data. It returns only true or false.
- Believing `SELECT *` inside EXISTS is slower in a way that changes results.

### Q5 ⭐⭐⭐ 🟢 Correlated subquery, the classic: employees(emp_id, name, dept_id, salary). List employees who earn more than the average salary of their own department. Write it as a correlated subquery, explain in words what 'executed once per outer row' means and what the correlation predicate is, then write the equivalent join to a derived table of department averages, and the pandas transform('mean') mask. Note that the window-function version belongs to Part 4.
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
**Say this first (1 line):** A correlated subquery refers to a column of the outer row, so conceptually it is re-evaluated for each outer row with that row's department; the same answer comes from joining to a derived table of department averages, and in pandas from `groupby(...).transform("mean")`.

**Schema and sample data:** nine employees, one NULL salary (Gita), two with a NULL department (Hari, Ila), and one department (30) with a single employee.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55),(7,'Gita',20,NULL),
  (8,'Hari',NULL,100),(9,'Ila',NULL,60);
```

**SQL answer:** correlated version `SQL_MAIN`, join version `SQL_JOIN` (Code block).
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(i.salary) FROM employees i WHERE i.dept_id = e.dept_id)
ORDER BY e.emp_id
```
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS dept_avg FROM employees GROUP BY dept_id) d
  ON d.dept_id = e.dept_id
WHERE e.salary > d.dept_avg
ORDER BY e.emp_id
```

**pandas answer:** `transform("mean")` returns one value per original row (the mean of that row's group), so it lines up with the frame and can be used in a mask.
```python
dept_avg = emp.groupby("dept_id")["salary"].transform("mean")
pd_df = emp[emp["salary"] > dept_avg]
```

**Example:** department averages ignore NULL: 10 is (50 + 70 + 60) / 3 = 60, 20 is (90 + 40) / 2 = 65 (Gita's NULL is skipped), 30 is 55.
- Dept 10: Ben (70) is above 60; Asha (50) and Chitra (60) are not (60 is not above 60).
- Dept 20: Dev (90) is above 65; Esha (40) is not; Gita's NULL salary is never above anything.
- Dept 30: Farid is the only employee, so he equals his own average and is not above it.
- NULL department (Hari, Ila): `i.dept_id = e.dept_id` is `NULL = NULL`, unknown, so the inner query finds no rows, AVG is NULL, and `salary > NULL` is unknown. They are excluded. Result: Ben and Dev.

**Code:** run with `python3 -I`.
```python
# Q5: correlated subquery, above own department average
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55),(7,'Gita',20,NULL),
  (8,'Hari',NULL,100),(9,'Ila',NULL,60);
"""
SQL_MAIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(i.salary) FROM employees i WHERE i.dept_id = e.dept_id)
ORDER BY e.emp_id
"""
SQL_JOIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS dept_avg FROM employees GROUP BY dept_id) d
  ON d.dept_id = e.dept_id
WHERE e.salary > d.dept_avg
ORDER BY e.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_join = pd.read_sql_query(SQL_JOIN, con)
print("SQL correlated:"); print(sql_main.to_string(index=False))
print("SQL join to derived table equal:", sql_main.equals(sql_join))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
dept_avg = emp.groupby("dept_id")["salary"].transform("mean")
pd_df = emp[emp["salary"] > dept_avg]
# pd:end
print("\npandas transform('mean') per row:", dept_avg.round(2).tolist())
print(pd_df.to_string(index=False))
# compared after sorting by emp_id
pd.testing.assert_frame_equal(sql_main, pd_df.sort_values("emp_id").reset_index(drop=True), check_dtype=False)
assert sql_main.equals(sql_join)

# surprise: dropna=False gives the NULL-department rows a group of their own; SQL's = never matches NULL
alt = emp[emp["salary"] > emp.groupby("dept_id", dropna=False)["salary"].transform("mean")]
print("\nwith dropna=False pandas also returns:", alt["name"].tolist())

# how many times does the inner query read rows? count calls of a Python function inside it
calls = {"n": 0}
def tick(x):
    calls["n"] += 1
    return x
con.create_function("tick", 1, tick)
con.execute("SELECT emp_id FROM employees e WHERE salary > (SELECT AVG(tick(i.salary)) FROM employees i WHERE i.dept_id = e.dept_id)").fetchall()
print("tick() calls for the correlated form over 9 rows:", calls["n"])
print("asserts passed: correlated == join == pandas transform")
```

**Output (my run):**
```text
SQL correlated:
 emp_id name  dept_id  salary
      2  Ben       10      70
      4  Dev       20      90
SQL join to derived table equal: True

pandas transform('mean') per row: [60.0, 60.0, 60.0, 65.0, 65.0, 55.0, 65.0, nan, nan]
 emp_id name  dept_id  salary
      2  Ben     10.0    70.0
      4  Dev     20.0    90.0

with dropna=False pandas also returns: ['Ben', 'Dev', 'Hari']
tick() calls for the correlated form over 9 rows: 19
asserts passed: correlated == join == pandas transform
```

**Edge cases:**
- NULL department: SQL excludes them (NULL never equals NULL). pandas `groupby` drops NaN keys by default, so `transform` gives NaN for those rows and the mask is False: same result. Surprise: with `dropna=False` pandas gives the NaN-keyed rows a group of their own (mean 80) and Hari (100) is returned, which SQL does not do.
- A department of one: never above its own average.
- NULL salary: skipped in the average, and the row itself is never returned.
- Ties with the average (Chitra at exactly 60) are excluded by the strict `>`.

**Then explain:**
- **"Executed once per outer row":** think of a loop. For each employee, plug that employee's dept_id into the inner query, get an average, compare. The correlation predicate is `i.dept_id = e.dept_id`: it ties the inner query to the current outer row.
- **What I measured:** I wrapped a Python function around the salary in the inner query and counted calls. For these 9 employees it was called 19 times: 3 x 3 for dept 10, 3 x 3 for dept 20, 1 for dept 30, and 0 for the NULL-department rows. So SQLite did re-read the department rows per outer row here (it did not cache by department). Other engines may decorrelate the query into a join (not executed here), so do not say "always slow".
- **Join to a derived table:** compute each department's average once, join on dept_id, compare. Same result in my run, and usually the form I write for big tables.
- **pandas:** `transform` is the equivalent of the join, one value per row, no merge needed.
- Window function form (`AVG(salary) OVER (PARTITION BY dept_id)`) belongs to Part 4; I do not use it here.

**Follow-ups:**
- *Why not `GROUP BY` in the outer query?* Then you lose the employee rows; the point is to keep rows and compare with a group statistic.
- *Which do you pick?* Join to the derived table if the table is large or the logic is reused; correlated if it reads best and the table is small. I did not time them.
- *What if you want departments with no peers shown anyway?* Change the comparison, then say so.

**Common mistakes:**
- Forgetting the correlation predicate, which turns it into "above the company average".
- Using `>=` and including people exactly at the average.
- Using an INNER JOIN to the averages and silently dropping NULL-department rows; a LEFT JOIN would keep them, but the comparison with NULL would still drop them.
- In pandas, `df.groupby("dept_id").salary.mean()` without transform, which has a different length from the frame.

### Q6 ⭐⭐⭐ 🟢 Derived tables (subquery in FROM) and the aliasing rule: orders(order_id, customer_id, amount). Find the average of per-customer total spend, which needs an aggregate of an aggregate. Write it as a derived table, say why you cannot nest AVG(SUM(amount)) in plain SQL, state the alias rule (PostgreSQL and MySQL require an alias on a derived table; test whether SQLite does), and give pandas groupby then mean.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** To average the per-customer totals you first compute one total per customer in a subquery in the FROM clause (a derived table), then average that; SQL does not let you nest `AVG(SUM(amount))` in one plain query, and in pandas it is `groupby().sum().mean()`.

**Schema and sample data:** customer 1 has two orders, customer 2 one, customer 3 three.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,200),(104,3,40),(105,3,60),(106,3,20);
```

**SQL answer:** `SQL_MAIN` is the derived table with an alias; `SQL_NO_ALIAS`, `SQL_NESTED` and `SQL_WRONG` are the other three tests (Code block).
```sql
SELECT AVG(t.total) AS avg_customer_total
FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) AS t
```
```sql
SELECT AVG(total) AS avg_customer_total
FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
```
```sql
SELECT AVG(SUM(amount)) FROM orders GROUP BY customer_id
```
```sql
SELECT AVG(amount) FROM orders
```

**pandas answer:**
```python
pd_val = orders.groupby("customer_id")["amount"].sum().mean()
```

**Example:** totals per customer: 1 -> 100 + 50 = 150, 2 -> 200, 3 -> 40 + 60 + 20 = 120. Average of totals = (150 + 200 + 120) / 3 = 156.67. The average of the six order amounts is 470 / 6 = 78.33, a different question.
- Edge demo: add order 107 with a NULL customer_id and 30 as the amount. SQL puts it in its own NULL group, so there are four totals (150, 200, 120, 30) and the average is 125.0. pandas with the default `groupby` drops the NaN key and still gives 156.67; with `dropna=False` it gives 125.0.

**Code:** run with `python3 -I`.
```python
# Q6: derived table, aggregate of an aggregate, alias rule
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,200),(104,3,40),(105,3,60),(106,3,20);
"""
SQL_MAIN = """
SELECT AVG(t.total) AS avg_customer_total
FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) AS t
"""
SQL_NO_ALIAS = """
SELECT AVG(total) AS avg_customer_total
FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
"""
SQL_NESTED = """
SELECT AVG(SUM(amount)) FROM orders GROUP BY customer_id
"""
SQL_WRONG = """
SELECT AVG(amount) FROM orders
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_val = con.execute(SQL_MAIN).fetchone()[0]
print("SQL derived table:", sql_val)
print("SQL without an alias on the derived table runs in SQLite:", con.execute(SQL_NO_ALIAS).fetchone()[0])
try:
    con.execute(SQL_NESTED)
except sqlite3.Error as e:
    print("AVG(SUM(amount)):", type(e).__name__, "-", e)
print("average of order amounts (the wrong question):", round(con.execute(SQL_WRONG).fetchone()[0], 4))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
pd_val = orders.groupby("customer_id")["amount"].sum().mean()
# pd:end
print("pandas groupby sum then mean:", pd_val)
# single value, compared with a tolerance
assert abs(sql_val - pd_val) < 1e-9
assert abs(sql_val - 470 / 3) < 1e-9

# edge: a NULL customer_id forms its own group in SQL; pandas groupby drops it by default
con.execute("INSERT INTO orders VALUES (107, NULL, 30)")
orders2 = pd.read_sql_query("SELECT * FROM orders", con)
print("\nafter inserting an order with NULL customer_id:")
print("SQL:", con.execute(SQL_MAIN).fetchone()[0])
print("pandas default:", orders2.groupby("customer_id")["amount"].sum().mean())
print("pandas dropna=False:", orders2.groupby("customer_id", dropna=False)["amount"].sum().mean())
assert abs(con.execute(SQL_MAIN).fetchone()[0] - orders2.groupby("customer_id", dropna=False)["amount"].sum().mean()) < 1e-9
print("asserts passed: SQL == pandas (and == dropna=False after the NULL row)")
```

**Output (my run):**
```text
SQL derived table: 156.66666666666666
SQL without an alias on the derived table runs in SQLite: 156.66666666666666
AVG(SUM(amount)): OperationalError - misuse of aggregate function SUM()
average of order amounts (the wrong question): 78.3333
pandas groupby sum then mean: 156.66666666666666

after inserting an order with NULL customer_id:
SQL: 125.0
pandas default: 156.66666666666666
pandas dropna=False: 125.0
asserts passed: SQL == pandas (and == dropna=False after the NULL row)
```

**Edge cases:**
- NULL customer_id: a group in SQL, dropped by default in pandas (see the Example). This is a real, silent difference. Decide whether orphan orders count as a customer.
- Customers with no orders do not appear in `orders`, so they are not in the average. If they should count as 0, start from the customers table and LEFT JOIN (Q8).
- Empty table: the inner query returns no rows, so `AVG` is NULL (not run).
- Integer amounts: SQLite's `AVG` returns a float (156.666...). In some engines AVG over integers may return a decimal with fixed scale; I have not run those.

**Then explain:**
- **Why no AVG(SUM(...)):** an aggregate cannot take another aggregate directly as its argument in the same query level. SQLite gave `OperationalError - misuse of aggregate function SUM()` in my run. You need two levels: group first, average second. A derived table (or a CTE, Q7) is how you get two levels.
- **Alias rule:** PostgreSQL and MySQL require an alias on a derived table, as the question says (I recall errors like "subquery in FROM must have an alias" and MySQL "Every derived table must have its own alias"; not executed). SQLite does not require one: in my run `SQL_NO_ALIAS` ran and returned the same 156.67. I still write the alias, `AS t`, because it is portable and lets me qualify columns. I have heard newer PostgreSQL versions relaxed the rule, but I have not verified that.
- **Naming the columns:** give the aggregate an alias (`AS total`), or the outer query has no stable name to refer to.
- **pandas:** the first `groupby(...).sum()` is the inner query; `.mean()` on the resulting Series is the outer one.

**Follow-ups:**
- *CTE or derived table?* Same result; the CTE reads top to bottom and can be reused (Q7).
- *What if I want the median of totals instead?* SQLite has no median function; that is Part 4 (window functions) or sorted `LIMIT/OFFSET` (a later question), not here.
- *Does the outer query see the inner table's other columns?* Only the ones the derived table selects.

**Common mistakes:**
- Writing `AVG(SUM(amount))` and being surprised by the error.
- Averaging the order amounts and calling it "average customer spend".
- Leaving out the alias because SQLite allows it, then failing on another engine.
- Forgetting that pandas drops NaN group keys.

### Q7 ⭐⭐⭐ 🟢 CTE basics: write WITH syntax with a name, an optional column list and a body, and convert this derived-table query into a CTE: SELECT city, AVG(t.total) FROM (SELECT c.city, o.customer_id, SUM(o.amount) AS total FROM orders o JOIN customers c ON c.customer_id = o.customer_id GROUP BY c.city, o.customer_id) t GROUP BY city, using customers(customer_id, name, city) and orders(order_id, customer_id, amount). Explain scope (the CTE exists only for that statement), naming advice, and that a CTE is not a persisted table or view. Give the pandas equivalent.
**Asked at:** GeeksforGeeks SQL interview questions (subquery, correlated subquery, EXISTS vs IN, CTE entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** A CTE is a named subquery written before the main query as `WITH name (col1, col2) AS (SELECT ...) SELECT ... FROM name`; it exists only for that one statement and is not a table or a view.

**Schema and sample data:** Mumbai has a customer but no orders.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Pune'),(3,'Chitra','Delhi'),(4,'Dev','Delhi'),(5,'Esha','Mumbai');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,200),(104,3,120),(105,3,30),(106,4,60);
```

**SQL answer:** the derived-table query from the question is `SQL_DERIVED`; the CTE version is `SQL_MAIN` (Code block).
```sql
SELECT city, AVG(t.total) AS avg_customer_total
FROM (SELECT c.city, o.customer_id, SUM(o.amount) AS total
      FROM orders o JOIN customers c ON c.customer_id = o.customer_id
      GROUP BY c.city, o.customer_id) t
GROUP BY city
ORDER BY city
```
```sql
WITH customer_totals (city, customer_id, total) AS (
    SELECT c.city, o.customer_id, SUM(o.amount)
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY c.city, o.customer_id
)
SELECT city, AVG(total) AS avg_customer_total
FROM customer_totals
GROUP BY city
ORDER BY city
```
Syntax shape: `WITH name [(column, ...)] AS (select) [, name2 AS (select)] main_select`. The column list is optional and renames the CTE's output columns in order.

**pandas answer:** the CTE becomes a named intermediate DataFrame.
```python
customer_totals = (orders.merge(customers, on="customer_id")
                   .groupby(["city", "customer_id"], as_index=False)["amount"].sum()
                   .rename(columns={"amount": "total"}))
pd_df = (customer_totals.groupby("city", as_index=False)["total"].mean()
         .rename(columns={"total": "avg_customer_total"}))
```

**Example:** orders joined to customers: Asha has 100 and 50, Ben 200, Chitra 120 and 30, Dev 60.
- `customer_totals` (the CTE body): (Pune, 1, 150), (Pune, 2, 200), (Delhi, 3, 150), (Delhi, 4, 60).
- Outer query: Pune is (150 + 200) / 2 = 175.0, Delhi is (150 + 60) / 2 = 105.0.
- Esha (Mumbai) has no orders, so the inner join drops her and Mumbai is missing from the result. That is the same in the derived-table form.

**Code:** run with `python3 -I`.
```python
# Q7: CTE basics, converting a derived table
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Pune'),(3,'Chitra','Delhi'),(4,'Dev','Delhi'),(5,'Esha','Mumbai');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,200),(104,3,120),(105,3,30),(106,4,60);
"""
SQL_DERIVED = """
SELECT city, AVG(t.total) AS avg_customer_total
FROM (SELECT c.city, o.customer_id, SUM(o.amount) AS total
      FROM orders o JOIN customers c ON c.customer_id = o.customer_id
      GROUP BY c.city, o.customer_id) t
GROUP BY city
ORDER BY city
"""
SQL_MAIN = """
WITH customer_totals (city, customer_id, total) AS (
    SELECT c.city, o.customer_id, SUM(o.amount)
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY c.city, o.customer_id
)
SELECT city, AVG(total) AS avg_customer_total
FROM customer_totals
GROUP BY city
ORDER BY city
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
derived = pd.read_sql_query(SQL_DERIVED, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL derived table:"); print(derived.to_string(index=False))
print("SQL CTE:"); print(sql_df.to_string(index=False))
try:
    con.execute("SELECT * FROM customer_totals")
except sqlite3.Error as e:
    print("\nafter the statement, the CTE name is gone:", e)
print("objects in the database:", con.execute("SELECT name FROM sqlite_master ORDER BY name").fetchall())

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
customer_totals = (orders.merge(customers, on="customer_id")
                   .groupby(["city", "customer_id"], as_index=False)["amount"].sum()
                   .rename(columns={"amount": "total"}))
pd_df = (customer_totals.groupby("city", as_index=False)["total"].mean()
         .rename(columns={"total": "avg_customer_total"}))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared after sorting by city
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("city").reset_index(drop=True), check_dtype=False)
assert derived.equals(sql_df)
print("asserts passed: derived table == CTE == pandas (Mumbai has no orders, so it is absent from all three)")
```

**Output (my run):**
```text
SQL derived table:
 city  avg_customer_total
Delhi               105.0
 Pune               175.0
SQL CTE:
 city  avg_customer_total
Delhi               105.0
 Pune               175.0

after the statement, the CTE name is gone: no such table: customer_totals
objects in the database: [('customers',), ('orders',)]

pandas:
 city  avg_customer_total
Delhi               105.0
 Pune               175.0
asserts passed: derived table == CTE == pandas (Mumbai has no orders, so it is absent from all three)
```

**Edge cases:**
- Cities with no orders vanish because of the inner join. To keep them, LEFT JOIN from customers and treat NULL totals deliberately.
- Column list: if you give `customer_totals (city, customer_id, total)`, the names come from the list and the body needs no aliases. Without a list, names come from the body's aliases. The column count must match (I did not run a mismatch).
- Name clash: a CTE named like a real table hides the table inside that statement (not run); pick distinct names.
- A CTE can be referenced more than once in the same statement, which a derived table cannot (used in Q8).

**Then explain:**
- **Scope:** the name is visible only in the one statement that carries the WITH. After the statement, `SELECT * FROM customer_totals` gave `no such table` in my run, and `sqlite_master` listed only `customers` and `orders`.
- **Not persisted:** it is not a table, not a view, and not a temp table. Nothing is stored; it is query text. Whether an engine computes it once or inlines it into the query is an engine choice: SQLite's WITH page documents `MATERIALIZED` and `NOT MATERIALIZED` hints (3.35+) that guide, not force, this; PostgreSQL has similar hints (docs, not executed).
- **Naming advice:** name by what the rows are (`customer_totals`, `paid_orders`), not `t1`, `cte`. One transformation per CTE.
- **Same result:** the derived table and the CTE returned identical frames in my run, so the CTE is a readability choice here, not a speed one.
- Recursive CTEs (`WITH RECURSIVE`) are Part 9; this part stays on non-recursive ones.

**Follow-ups:**
- *CTE vs temp table?* A temp table is stored for the session and can be indexed; a CTE is gone after the statement. A view is a stored query definition.
- *Can I chain CTEs?* Yes, separated by commas, each seeing the earlier ones (Q11 and later questions).
- *Can the WITH go before INSERT, UPDATE or DELETE?* In SQLite 3.45 it ran for all three in my scratch checks.

**Common mistakes:**
- Calling a CTE "a temporary table" or saying it speeds the query up by itself.
- Trying to use the CTE name in the next statement.
- Giving the CTE a column list of the wrong length.
- Forgetting the comma between two CTEs in one WITH.

### Q8 ⭐⭐⭐ 🟡 Customers whose total spend is above the average customer total: orders(order_id, customer_id, amount) and customers(customer_id, name). Write it as a CTE of per-customer totals plus a scalar subquery on that CTE, and as a derived table. Explain the difference between the average of order amounts and the average of customer totals (a common wrong answer), what happens to customers with no orders, and give pandas groupby plus a boolean mask.
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
**Say this first (1 line):** Build per-customer totals in a CTE, take the average of those totals with a scalar subquery on the same CTE, and keep customers above it; the common wrong answer averages the individual order amounts instead of the customer totals.

**Schema and sample data:** Dev has no orders; Chitra has three small ones.
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,200),(104,3,40),(105,3,60),(106,3,20);
```

**SQL answer:** the CTE with a scalar subquery `SQL_MAIN`, the derived-table form `SQL_DERIVED`, the wrong version `SQL_WRONG_AVG`, and the variant that counts zero-spend customers `SQL_ZERO` (Code block).
```sql
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
)
SELECT c.customer_id, c.name, t.total
FROM totals t
JOIN customers c ON c.customer_id = t.customer_id
WHERE t.total > (SELECT AVG(total) FROM totals)
ORDER BY c.customer_id
```
```sql
SELECT c.customer_id, c.name, t.total
FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) t
JOIN customers c ON c.customer_id = t.customer_id
WHERE t.total > (SELECT AVG(total)
                 FROM (SELECT SUM(amount) AS total FROM orders GROUP BY customer_id))
ORDER BY c.customer_id
```
```sql
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
)
SELECT c.customer_id, c.name, t.total
FROM totals t JOIN customers c ON c.customer_id = t.customer_id
WHERE t.total > (SELECT AVG(amount) FROM orders)
ORDER BY c.customer_id
```
```sql
WITH totals AS (
    SELECT c.customer_id, c.name, COALESCE(SUM(o.amount), 0) AS total
    FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, total FROM totals
WHERE total > (SELECT AVG(total) FROM totals)
ORDER BY customer_id
```

**pandas answer:** `groupby().sum()` gives a Series of totals; a mask compares it with its own mean. The zero-spend variant in the Code block uses `reindex(..., fill_value=0)` over all customers.
```python
totals = orders.groupby("customer_id")["amount"].sum()
pd_df = (totals[totals > totals.mean()].rename("total").reset_index()
         .merge(customers, on="customer_id")[["customer_id", "name", "total"]])
```

**Example:** totals are Asha 150, Ben 200, Chitra 40 + 60 + 20 = 120.
- Average of customer totals = (150 + 200 + 120) / 3 = 156.67. Only Ben (200) is above it.
- Wrong version: the average order amount is 470 / 6 = 78.33, which is much lower, so all three customers are above it (Asha, Ben, Chitra). The answer set is wrong because the wrong thing was averaged.
- Zero-spend variant: counting Dev as 0 gives 470 / 4 = 117.5, and Asha, Ben and Chitra are above it. In this data it happens to return the same three names as the wrong version, for a different reason.
- So three reasonable-looking definitions give two different answers: Ben alone, or Asha, Ben and Chitra.

**Code:** run with `python3 -I`.
```python
# Q8: customers whose total spend is above the average customer total
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,200),(104,3,40),(105,3,60),(106,3,20);
"""
SQL_MAIN = """
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
)
SELECT c.customer_id, c.name, t.total
FROM totals t
JOIN customers c ON c.customer_id = t.customer_id
WHERE t.total > (SELECT AVG(total) FROM totals)
ORDER BY c.customer_id
"""
SQL_DERIVED = """
SELECT c.customer_id, c.name, t.total
FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) t
JOIN customers c ON c.customer_id = t.customer_id
WHERE t.total > (SELECT AVG(total)
                 FROM (SELECT SUM(amount) AS total FROM orders GROUP BY customer_id))
ORDER BY c.customer_id
"""
SQL_WRONG_AVG = """
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
)
SELECT c.customer_id, c.name, t.total
FROM totals t JOIN customers c ON c.customer_id = t.customer_id
WHERE t.total > (SELECT AVG(amount) FROM orders)
ORDER BY c.customer_id
"""
SQL_ZERO = """
WITH totals AS (
    SELECT c.customer_id, c.name, COALESCE(SUM(o.amount), 0) AS total
    FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT customer_id, name, total FROM totals
WHERE total > (SELECT AVG(total) FROM totals)
ORDER BY customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(s): return pd.read_sql_query(s, con)
sql_df, derived, wrong, zero = q(SQL_MAIN), q(SQL_DERIVED), q(SQL_WRONG_AVG), q(SQL_ZERO)
print("CTE + scalar subquery:"); print(sql_df.to_string(index=False))
print("derived-table version equal:", derived.equals(sql_df))
print("\nWRONG (compares totals with the average order amount, 78.33):"); print(wrong.to_string(index=False))
print("\nIncluding zero-spend customers (average over 4 customers, 117.5):"); print(zero.to_string(index=False))

customers, orders = q("SELECT * FROM customers"), q("SELECT * FROM orders")
# pd:main
totals = orders.groupby("customer_id")["amount"].sum()
pd_df = (totals[totals > totals.mean()].rename("total").reset_index()
         .merge(customers, on="customer_id")[["customer_id", "name", "total"]])
# pd:end
print("\npandas: mean of totals =", round(totals.mean(), 4), "| mean of order amounts =", round(orders['amount'].mean(), 4))
print(pd_df.to_string(index=False))
# zero-spend variant in pandas: reindex over all customers, fill 0
totals0 = totals.reindex(customers["customer_id"], fill_value=0)
pd_zero = totals0[totals0 > totals0.mean()].rename("total").reset_index().merge(customers, on="customer_id")[["customer_id", "name", "total"]]
# compared after sorting by customer_id
pd.testing.assert_frame_equal(sql_df, pd_df.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(zero, pd_zero.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
assert derived.equals(sql_df) and sql_df["name"].tolist() == ["Ben"]
print("asserts passed: SQL == pandas for the main and the zero-spend variants")
```

**Output (my run):**
```text
CTE + scalar subquery:
 customer_id name  total
           2  Ben    200
derived-table version equal: True

WRONG (compares totals with the average order amount, 78.33):
 customer_id   name  total
           1   Asha    150
           2    Ben    200
           3 Chitra    120

Including zero-spend customers (average over 4 customers, 117.5):
 customer_id   name  total
           1   Asha    150
           2    Ben    200
           3 Chitra    120

pandas: mean of totals = 156.6667 | mean of order amounts = 78.3333
 customer_id name  total
           2  Ben    200
asserts passed: SQL == pandas for the main and the zero-spend variants
```

**Edge cases:**
- Customers with no orders: the inner query on `orders` never sees them, so they are not in the average and cannot be returned. To include them, LEFT JOIN from customers and `COALESCE(SUM(...), 0)`, which lowers the average. This is a business decision; state it.
- Ties with the average: strict `>` excludes a customer exactly at the average.
- NULL customer_id in orders: forms a group in SQL (not shown here, see Q6) and is dropped by pandas groupby; the join to customers then drops it anyway.
- NULL amounts: SUM skips them; a customer whose amounts are all NULL gets a NULL total and is never above the average.

**Then explain:**
- **Why a CTE here:** the totals are used twice, once for the rows and once inside the scalar subquery. With a CTE I write the grouping once. With the derived-table form I wrote the grouping twice, which is easy to let drift apart.
- **Average of orders vs average of customers:** different grain. Orders are the rows of `orders`; customers are the groups. A customer with many small orders pulls the order average down but not the customer-total average.
- **Does the CTE run twice?** I have not measured. SQLite's docs describe `MATERIALIZED` hints but do not promise a rule for the default; treat the double use as a readability gain, not a guarantee of a single computation.
- **pandas:** `totals.mean()` is a Python number computed once.

**Follow-ups:**
- *How do you show how far above average?* Select `t.total - (SELECT AVG(total) FROM totals)`.
- *What if the question says "customers" but the data is at order level?* Ask what the grain is before writing anything.
- *Top spenders instead?* ORDER BY total DESC with LIMIT; ranking with ties is Part 4.

**Common mistakes:**
- Comparing totals with `AVG(amount)` over orders.
- Dropping the zero-spend customers without saying so.
- Writing `HAVING SUM(amount) > AVG(SUM(amount))`, which is not valid.
- Joining to customers before aggregating and multiplying rows (Part 2, Q13).

### Q9 ⭐⭐⭐ 🟡 Percent of total with a scalar subquery (no window functions): sales(sale_id, region, amount). Report each region's total, its share of the grand total as a percentage rounded to 1 decimal, ordered by share. Show the scalar subquery in the SELECT list, the integer-division trap (use 100.0 or CAST), the cross-join-to-a-one-row-CTE alternative, what happens if the grand total is NULL or zero (NULLIF), and the pandas version (sum then divide).
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Put the grand total in a scalar subquery next to each region's `SUM`, multiply by `100.0` (not `100`) so the division is not integer, round, and wrap the denominator in `NULLIF(..., 0)` so a zero total cannot divide by zero.

**Schema and sample data:** North 100 + 150, South 50 + 50, East 200, West 50; grand total 600.
```sql
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'North',100),(2,'North',150),(3,'South',50),(4,'South',50),(5,'East',200),(6,'West',50);
```

**SQL answer:** the scalar subquery version `SQL_MAIN`, the integer-division trap `SQL_INT_TRAP`, and the CTE cross-join version `SQL_CTE` (Code block).
```sql
SELECT region, SUM(amount) AS total,
       ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM sales), 1) AS pct
FROM sales
GROUP BY region
ORDER BY pct DESC, region
```
```sql
SELECT region, 100 * SUM(amount) / (SELECT SUM(amount) FROM sales) AS pct_int
FROM sales GROUP BY region ORDER BY region
```
```sql
WITH r AS (SELECT region, SUM(amount) AS total FROM sales GROUP BY region),
     g AS (SELECT SUM(amount) AS grand FROM sales)
SELECT r.region, r.total, ROUND(100.0 * r.total / NULLIF(g.grand, 0), 1) AS pct
FROM r CROSS JOIN g
ORDER BY pct DESC, r.region
```

**pandas answer:** group and sum, divide by the grand sum, round.
```python
tot = sales.groupby("region")["amount"].sum()
pd_df = (pd.DataFrame({"total": tot, "pct": (100.0 * tot / tot.sum()).round(1)})
         .reset_index().sort_values(["pct", "region"], ascending=[False, True]).reset_index(drop=True))
```

**Example:** region totals: North 250, South 100, East 200, West 50. Grand total 600.
- North: 100.0 * 250 / 600 = 41.666..., which rounds to 41.7. East 33.3, South 16.7, West 8.3. Ordered by share descending: North, East, South, West. The rounded shares add up to 100.0 here, though rounding can leave a total of 99.9 or 100.1 in general.
- Integer trap: `100 * SUM(amount) / (SELECT SUM(amount) FROM sales)` is integer arithmetic when both are integers: North 41, East 33, South 16, West 8. It silently truncates (it does not round) and the shares add up to 98.
- CTE version: `g` is a one-row CTE; `CROSS JOIN g` attaches its single `grand` value to every region row. Same result.

**Code:** run with `python3 -I`.
```python
# Q9: percent of total with a scalar subquery
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'North',100),(2,'North',150),(3,'South',50),(4,'South',50),(5,'East',200),(6,'West',50);
"""
SQL_MAIN = """
SELECT region, SUM(amount) AS total,
       ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM sales), 1) AS pct
FROM sales
GROUP BY region
ORDER BY pct DESC, region
"""
SQL_INT_TRAP = """
SELECT region, 100 * SUM(amount) / (SELECT SUM(amount) FROM sales) AS pct_int
FROM sales GROUP BY region ORDER BY region
"""
SQL_CTE = """
WITH r AS (SELECT region, SUM(amount) AS total FROM sales GROUP BY region),
     g AS (SELECT SUM(amount) AS grand FROM sales)
SELECT r.region, r.total, ROUND(100.0 * r.total / NULLIF(g.grand, 0), 1) AS pct
FROM r CROSS JOIN g
ORDER BY pct DESC, r.region
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(s): return pd.read_sql_query(s, con)
sql_df, trap, cte = q(SQL_MAIN), q(SQL_INT_TRAP), q(SQL_CTE)
print("SQL scalar subquery:"); print(sql_df.to_string(index=False))
print("\nInteger-division trap (100 * SUM / grand):"); print(trap.to_string(index=False))
print("\nCTE cross join equal:", cte.equals(sql_df))

sales = q("SELECT * FROM sales")
# pd:main
tot = sales.groupby("region")["amount"].sum()
pd_df = (pd.DataFrame({"total": tot, "pct": (100.0 * tot / tot.sum()).round(1)})
         .reset_index().sort_values(["pct", "region"], ascending=[False, True]).reset_index(drop=True))
# pd:end
print("\npandas:"); print(pd_df.to_string(index=False))
# compared in the SQL order (pct descending, region ascending)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert cte.equals(sql_df)
print("sum of the rounded shares:", round(sql_df["pct"].sum(), 1))

# zero and NULL grand totals
con.executescript("CREATE TABLE z(region TEXT, amount INTEGER); INSERT INTO z VALUES ('A',0),('B',0);"
                  "CREATE TABLE n(region TEXT, amount INTEGER); INSERT INTO n VALUES ('A',NULL),('B',NULL);")
for t in ("z", "n"):
    plain = con.execute(f"SELECT region, 100.0 * SUM(amount) / (SELECT SUM(amount) FROM {t}) FROM {t} GROUP BY region").fetchall()
    safe = con.execute(f"SELECT region, 100.0 * SUM(amount) / NULLIF((SELECT SUM(amount) FROM {t}), 0) FROM {t} GROUP BY region").fetchall()
    print(f"table {t}: plain {plain} | with NULLIF {safe}")
# rounding rule difference
print("SQLite ROUND(0.25, 1), ROUND(2.5):", con.execute("SELECT ROUND(0.25, 1), ROUND(2.5)").fetchone())
print("pandas Series([0.25, 2.5]).round(1).tolist():", pd.Series([0.25, 2.5]).round(1).tolist(), "| Series([2.5]).round(0):", pd.Series([2.5]).round(0).tolist())
zero = pd.Series({"A": 0, "B": 0})
print("pandas 100.0 * zero totals / zero grand total:", (100.0 * zero / zero.sum()).tolist())
print("asserts passed: SQL == CTE == pandas")
```

**Output (my run):**
```text
SQL scalar subquery:
region  total  pct
 North    250 41.7
  East    200 33.3
 South    100 16.7
  West     50  8.3

Integer-division trap (100 * SUM / grand):
region  pct_int
  East       33
 North       41
 South       16
  West        8

CTE cross join equal: True

pandas:
region  total  pct
 North    250 41.7
  East    200 33.3
 South    100 16.7
  West     50  8.3
sum of the rounded shares: 100.0
table z: plain [('A', None), ('B', None)] | with NULLIF [('A', None), ('B', None)]
table n: plain [('A', None), ('B', None)] | with NULLIF [('A', None), ('B', None)]
SQLite ROUND(0.25, 1), ROUND(2.5): (0.3, 3.0)
pandas Series([0.25, 2.5]).round(1).tolist(): [0.2, 2.5] | Series([2.5]).round(0): [2.0]
pandas 100.0 * zero totals / zero grand total: [nan, nan]
asserts passed: SQL == CTE == pandas
```

**Edge cases:**
- Grand total NULL or zero: I ran two tables, one with amounts 0 and one with all-NULL amounts. In SQLite, dividing by zero gives NULL (no error), so the plain and the `NULLIF` versions both returned NULL for every region. So in SQLite, `NULLIF` makes no visible difference; it matters for portability. PostgreSQL raises a division-by-zero error, to my knowledge (not executed here), and MySQL's behaviour depends on the SQL mode (not executed), so write the `NULLIF` anyway and say why.
- All-NULL amounts: `SUM` is NULL, so the grand total is NULL and every share is NULL (my run). In my zero-total run pandas gave NaN for 0.0 / 0.0, matching SQL's NULL.
- Rounding differs: SQLite `ROUND(0.25, 1)` is 0.3 (half away from zero), but pandas `Series([0.25]).round(1)` is 0.2 (half to even). In my run `ROUND(2.5)` was 3.0 in SQLite and pandas `round(0)` gave 2.0. Here no share lands exactly on a half, so the two agree. Round once, at the end.
- Ties in share: add the region as a tie-breaker in ORDER BY to make the order deterministic (I did).
- Regions with no sales do not appear at all; they would need a regions table and a LEFT JOIN.

**Then explain:**
- **No window functions:** the window version (`SUM(SUM(amount)) OVER ()`) is Part 4. The scalar subquery gives the same number without it.
- **Evaluated once:** the grand-total subquery is uncorrelated, so it is one value, not recalculated per region (Q1 measured this).
- **Integer division:** in SQLite, integer divided by integer truncates, as in my trap output. In PostgreSQL integer / integer also truncates, and MySQL's `/` gives a decimal (from memory, not executed). Use `100.0 *` or `CAST(... AS REAL)` and you are safe everywhere.
- **Cross join to a one-row CTE:** fine when the CTE is guaranteed to have exactly one row; an aggregate without GROUP BY always has one.
- **pandas:** `100.0 * tot / tot.sum()`; floats already, so no trap.

**Follow-ups:**
- *Percent within a group, for example share of region within country?* That is a correlated subquery or a window function (Part 4).
- *Why does a share list not always add to 100?* Rounding each row separately.
- *Sort by share ascending?* Change the order direction; keep the region tie-breaker.

**Common mistakes:**
- `100 * SUM(amount) / total` with integer columns.
- Rounding before dividing or summing rounded shares.
- Using `SUM(amount) / SUM(amount)` in the same GROUP BY query, where the denominator is the group total, not the grand total.
- No `NULLIF`, then a division error in another engine.

### Q10 ⭐⭐⭐ 🟡 Latest order per customer with a correlated subquery: orders(order_id, customer_id, order_date, amount). Return each customer's most recent order row (all columns) using WHERE order_date = (SELECT MAX(order_date) FROM orders WHERE customer_id = o.customer_id). Explain what happens when a customer has two orders on the latest date (both returned), how to break ties by order_id, and give the pandas versions (sort and drop_duplicates, or idxmax) with the tie behaviour stated.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** For each order, keep it if its date equals the maximum date among that customer's orders; if a customer has two orders on the latest date, both come back, so break the tie with order_id (or take one row by sorting), and say which tie rule you chose.

**Schema and sample data:** customer 1 has two orders on 2025-02-10 (a tie).
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (101,1,'2025-01-05',100),(102,1,'2025-02-10',50),(103,1,'2025-02-10',75),
  (104,2,'2025-01-20',200),(105,3,'2025-03-01',30),(106,3,'2025-02-15',60);
```

**SQL answer:** the correlated query `SQL_MAIN` (ties returned) and a tie-broken one `SQL_TIE` that takes exactly one row per customer (Code block).
```sql
SELECT o.order_id, o.customer_id, o.order_date, o.amount
FROM orders o
WHERE o.order_date = (SELECT MAX(order_date) FROM orders WHERE customer_id = o.customer_id)
ORDER BY o.customer_id, o.order_id
```
```sql
SELECT o.order_id, o.customer_id, o.order_date, o.amount
FROM orders o
WHERE o.order_id = (SELECT i.order_id FROM orders i
                    WHERE i.customer_id = o.customer_id
                    ORDER BY i.order_date DESC, i.order_id DESC LIMIT 1)
ORDER BY o.customer_id
```

**pandas answer:** three ways, with different tie behaviour (all in the Code block).
```python
pd_all = orders[orders["order_date"] == orders.groupby("customer_id")["order_date"].transform("max")]
pd_one = (orders.sort_values(["order_date", "order_id"])
          .drop_duplicates("customer_id", keep="last"))
pd_idx = orders.loc[orders.groupby("customer_id")["order_date"].idxmax()]
```

**Example:** latest dates: customer 1 is 2025-02-10, customer 2 is 2025-01-20, customer 3 is 2025-03-01.
- `SQL_MAIN`: for order 102 and 103 the inner query returns 2025-02-10 for customer 1, so both match. Result: 102, 103, 104, 105 (4 rows for 3 customers).
- `SQL_TIE`: the inner query sorts customer 1's orders by date then order_id, descending, and takes the first, which is order 103. The outer query keeps the order whose order_id equals that. Result: 103, 104, 105.
- pandas: the `transform("max")` mask returns 102, 103, 104, 105 (same as `SQL_MAIN`); sorting by date and order_id and `drop_duplicates(keep="last")` returns 103, 104, 105 (same as `SQL_TIE`); `idxmax` returns 102, 104, 105, the first of the tied rows, which is a different tie rule again.

**Code:** run with `python3 -I`.
```python
# Q10: latest order per customer, correlated subquery
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (101,1,'2025-01-05',100),(102,1,'2025-02-10',50),(103,1,'2025-02-10',75),
  (104,2,'2025-01-20',200),(105,3,'2025-03-01',30),(106,3,'2025-02-15',60);
"""
SQL_MAIN = """
SELECT o.order_id, o.customer_id, o.order_date, o.amount
FROM orders o
WHERE o.order_date = (SELECT MAX(order_date) FROM orders WHERE customer_id = o.customer_id)
ORDER BY o.customer_id, o.order_id
"""
SQL_TIE = """
SELECT o.order_id, o.customer_id, o.order_date, o.amount
FROM orders o
WHERE o.order_id = (SELECT i.order_id FROM orders i
                    WHERE i.customer_id = o.customer_id
                    ORDER BY i.order_date DESC, i.order_id DESC LIMIT 1)
ORDER BY o.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(s): return pd.read_sql_query(s, con)
sql_df, tie = q(SQL_MAIN), q(SQL_TIE)
print("SQL max-date correlated (ties both returned):"); print(sql_df.to_string(index=False))
print("\nSQL tie-broken to one row per customer:"); print(tie.to_string(index=False))

orders = q("SELECT * FROM orders")
# pd:main
pd_all = orders[orders["order_date"] == orders.groupby("customer_id")["order_date"].transform("max")]
pd_one = (orders.sort_values(["order_date", "order_id"])
          .drop_duplicates("customer_id", keep="last"))
pd_idx = orders.loc[orders.groupby("customer_id")["order_date"].idxmax()]
# pd:end
print("\npandas transform('max') mask:", pd_all["order_id"].tolist())
print("pandas sort + drop_duplicates(keep='last'):", sorted(pd_one["order_id"].tolist()))
print("pandas idxmax (first of the tied rows):", sorted(pd_idx["order_id"].tolist()))
# compared after sorting by customer_id, order_id
pd.testing.assert_frame_equal(sql_df, pd_all.sort_values(["customer_id", "order_id"]).reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(tie, pd_one.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
assert sorted(pd_idx["order_id"].tolist()) == [102, 104, 105]

# edge: a customer whose only order has a NULL date
con.execute("INSERT INTO orders VALUES (107, 4, NULL, 90)")
sql2 = q(SQL_MAIN)
print("\nafter adding customer 4 with a NULL order_date, SQL customers:", sorted(set(sql2["customer_id"])))
o2 = q("SELECT * FROM orders")
print("pandas transform('max') mask customers:", sorted(set(o2[o2["order_date"] == o2.groupby("customer_id")["order_date"].transform("max")]["customer_id"])))
try:
    o2.loc[o2.groupby("customer_id")["order_date"].idxmax()]
except Exception as e:
    print("pandas idxmax on an all-NULL group:", type(e).__name__)
print("asserts passed: SQL == pandas (ties kept, and tie-broken)")
```

**Output (my run):**
```text
SQL max-date correlated (ties both returned):
 order_id  customer_id order_date  amount
      102            1 2025-02-10      50
      103            1 2025-02-10      75
      104            2 2025-01-20     200
      105            3 2025-03-01      30

SQL tie-broken to one row per customer:
 order_id  customer_id order_date  amount
      103            1 2025-02-10      75
      104            2 2025-01-20     200
      105            3 2025-03-01      30

pandas transform('max') mask: [102, 103, 104, 105]
pandas sort + drop_duplicates(keep='last'): [103, 104, 105]
pandas idxmax (first of the tied rows): [102, 104, 105]

after adding customer 4 with a NULL order_date, SQL customers: [1, 2, 3]
pandas transform('max') mask customers: [1, 2, 3]
pandas idxmax on an all-NULL group: ValueError
asserts passed: SQL == pandas (ties kept, and tie-broken)
```

**Edge cases:**
- Ties on the latest date: `SQL_MAIN` returns all of them. If the business wants one row, you must define the tie-break (here the larger order_id).
- NULL order_date: I added order 107 for a new customer 4 whose only date is NULL. `MAX(order_date)` is NULL, `order_date = NULL` is unknown, and the customer disappears from the result. pandas does the same with the mask (NaN == NaN is False) in my run. `idxmax` is worse: on the all-NULL group it raised `ValueError` in pandas 3.0.5.
- Dates stored as ISO text (`YYYY-MM-DD`) sort correctly as text. In other formats `MAX` would compare strings and could pick the wrong order.
- Customer with one order: always returned.
- The correlated version is evaluated per outer row, so on a large table it needs an index on (customer_id, order_date) to be reasonable (not measured here).

**Then explain:**
- **How the correlation works:** the inner `WHERE customer_id = o.customer_id` ties the maximum to the current order's customer. Each outer row asks "is my date my customer's latest date".
- **Tie handling is a requirement, not a detail:** with ties the question "most recent order" has two answers; ask the interviewer. For ties by time of day, a timestamp column usually removes them.
- **Alternatives:** join to a derived table `SELECT customer_id, MAX(order_date) ... GROUP BY customer_id` on both columns, or `ROW_NUMBER()` in Part 4. I only ran the forms above here.
- **pandas tie rules:** the mask keeps all ties; `drop_duplicates(keep="last")` after a full sort picks the last by the sort keys; `idxmax` picks the first occurrence, so it depends on row order.
- Row-value comparisons such as `(a, b) IN (SELECT ...)` also ran in my scratch check on SQLite 3.45, but I used single-column forms above because they are more portable.

**Follow-ups:**
- *Latest order with its total amount per customer?* Aggregate in a derived table first, then join, to avoid multiplying rows.
- *What if I want the top 2 per customer?* That needs ranking; Part 4.
- *Why not `SELECT *, MAX(order_date) ... GROUP BY customer_id`?* SQLite would return the other columns from the max row (a SQLite special case), but other engines reject or return arbitrary rows; do not rely on it.

**Common mistakes:**
- Not mentioning ties, so a customer appears twice.
- Using `MAX(order_id)` as a proxy for "latest" when ids are not time-ordered.
- Writing `WHERE order_date = (SELECT MAX(order_date) FROM orders)` without the correlation, which returns only the globally latest orders.
- Using `idxmax` and not noticing it silently picks the first of the ties.
