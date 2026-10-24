# Book 3 — Part 3: Subqueries and CTEs with pandas equivalents

**Topic:** scalar subqueries in SELECT and WHERE (zero and many rows per engine), IN and NOT IN subqueries and the NULL trap, EXISTS and NOT EXISTS, correlated subqueries and per-row execution, derived tables and aliasing, ANY/SOME/ALL and their MAX/MIN/EXISTS equivalents, subquery versus JOIN equivalence, subqueries in HAVING, percent of total and above-average comparisons with scalar subqueries, nth-highest, median and top-N per group without window functions, max-per-group ties, relational division (GROUP BY HAVING COUNT DISTINCT and double NOT EXISTS), CTE syntax, naming, chained CTEs and CTE reuse, CTE versus subquery versus view versus temp table, CTE scaffolding for cohort and funnel questions, refactoring nested queries, debugging a join fan-out hidden in a CTE, UPDATE, DELETE and INSERT ... SELECT with subqueries, LIMIT inside subqueries, and the pandas side (boolean masks, groupby transform, isin and map from aggregated frames, merge of aggregated frames, query, pipe and assign, NaN pitfalls)
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 16, ⭐⭐ 14, ⭐ 10)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers subqueries and non-recursive CTEs. Window functions (Parts 4 and 5) are deliberately absent: nth-highest, top-N per group, max-per-group and running comparisons are answered here without them and each points to the window version in Part 4 or 5. Recursive CTEs (Part 9), retention and funnel logic (Parts 6 and 8) and EXPLAIN-level tuning (Part 11) are out of scope; the CTE scaffolding questions only build the step-by-step structure. Every query question states its tables and columns so Wave B can build small sample data; answers must run on SQLite 3.45 and compare with pandas 3.0.x, and anything engine-specific is shown as hedged text labelled 'not executed'.

Verification notes for Wave B (from pages opened in Wave A, as summarised by the fetch tool): the SQLite expression page says a scalar subquery's value is the first row of its result and NULL when there are no rows, EXISTS gives 1 or 0 regardless of NULLs, an empty right side gives IN false and NOT IN true even for a NULL left operand, a NULL on either side with no match gives NULL for IN and NOT IN, and a correlated subquery is re-evaluated when needed while an uncorrelated one is evaluated once. The SQLite WITH page says CTEs can prefix SELECT, INSERT, DELETE and UPDATE, MATERIALIZED and NOT MATERIALIZED need 3.35.0, the default lets SQLite choose, and WITH cannot be used inside CREATE TRIGGER. The PostgreSQL pages say a non-recursive side-effect-free CTE referenced once is folded into the parent by default and a multiply referenced CTE is materialised by default, that a scalar subquery returning more than one row is an error, that IN is = ANY and NOT IN is <> ALL, and that ALL over an empty subquery is true. The MySQL 8.4 pages say modifying a table and selecting from it in a subquery is restricted (error number 1093 was not on the page and comes from general knowledge), a materialized derived table is the workaround, LIMIT in IN, ALL, ANY or SOME subqueries gives error 1235, WITH is allowed before SELECT, UPDATE and DELETE, and a CTE can be referenced several times unlike a derived table. The pandas groupby page says transform returns a result indexed like the input with the aggregate broadcast, and that NA group keys are dropped unless dropna=False; the Comparison with SQL page says null merge keys match each other. Items NOT verified from pages (run or hedge): whether SQLite requires an alias on a FROM-subquery (the SELECT page excerpt was truncated), SQLite behaviour for LIMIT -1 and expression LIMIT/OFFSET, UPDATE ... FROM support in SQLite 3.33+, row-value comparison support, the exact MySQL error for a many-row scalar subquery (1242 from general knowledge), PostgreSQL 12 as the version of the inlining change (from a guide and general knowledge), and any SQL Server, Oracle, BigQuery or Snowflake behaviour.

Evidence limits: no candidate-reported SQL questions were found; the search returned prep guides, practice-site lesson pages and documentation. The 'Asked at' tags are source types, and 'expert gap-check' marks questions chosen from practice. Star ratings blend how often a topic appears across guides with judgement. See research_notes/Book3_Part03_sources.md for which pages were opened.

---

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

### Q11 ⭐⭐⭐ 🟡 Refactor a messy nested query into CTEs. Given customers(customer_id, name, city), orders(order_id, customer_id, order_date, amount) and this three-level query: SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM (SELECT customer_id, SUM(amount) AS total FROM orders WHERE order_date >= '2025-01-01' GROUP BY customer_id) WHERE total > (SELECT AVG(total) FROM (SELECT SUM(amount) AS total FROM orders WHERE order_date >= '2025-01-01' GROUP BY customer_id))). Rewrite it with two chained, well-named CTEs, show the results are identical, and explain what the CTE version buys (named steps, the filtered per-customer totals computed once in the text, easier debugging by selecting from each CTE).
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Name each step as a CTE: `customer_totals` (the filtered per-customer sums) and `above_average` (the customers over the average of those totals), then join to `customers`; the result is identical, but the filter is written once and you can run each step on its own.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Goa'),(5,'Esha','Delhi'),(6,'Faiz','Goa');
INSERT INTO orders VALUES
 (101,1,'2025-02-01',100),(102,1,'2025-03-05',200),(103,1,'2024-11-30',1000),
 (104,2,'2025-01-10',50),
 (105,3,'2025-04-01',150),(106,3,'2025-04-09',10),
 (107,5,'2024-12-31',900),
 (108,6,'2025-05-05',90);
```

**SQL answer:** `SQL_NESTED` is the three-level original and `SQL_MAIN` is the CTE rewrite; both run in the Code block.
```sql
WITH customer_totals AS (
  SELECT customer_id, SUM(amount) AS total
  FROM orders
  WHERE order_date >= '2025-01-01'
  GROUP BY customer_id
),
above_average AS (
  SELECT customer_id, total
  FROM customer_totals
  WHERE total > (SELECT AVG(total) FROM customer_totals)
)
SELECT c.name
FROM customers c
JOIN above_average a ON a.customer_id = c.customer_id
ORDER BY c.name
```

**pandas answer:** one named variable per CTE (same text as in the Code block).
```python
recent = orders[orders["order_date"] >= "2025-01-01"]
customer_totals = recent.groupby("customer_id")["amount"].sum()
above_average = customer_totals[customer_totals > customer_totals.mean()]
pd_df = (customers[customers["customer_id"].isin(above_average.index)][["name"]]
         .sort_values("name").reset_index(drop=True))
```

**Example:** Orders dated on or after 2025-01-01 only (the filter).
- `customer_totals`: Asha 100 + 200 = 300 (her 1000 order is from 2024-11-30 and is filtered out), Ben 50, Chitra 150 + 10 = 160, Faiz 90. Dev has no orders and Esha has only a 2024-12-31 order, so neither appears.
- The average of those four totals is (300 + 50 + 160 + 90) / 4 = 150.
- `above_average` keeps totals above 150: Asha (300) and Chitra (160). Ben (50) and Faiz (90) drop out.
- Joining to `customers` gives Asha and Chitra. The nested query returns the same two names.
- Without the date filter the totals become Asha 1300, Ben 50, Chitra 160, Esha 900, Faiz 90, the average is 500, and the answer would be Asha and Esha. That is why the filter has to sit inside the totals step.

**Code:** run with `python3 -I`.
```python
# Q11: refactor a three-level nested query into two chained CTEs
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Goa'),(5,'Esha','Delhi'),(6,'Faiz','Goa');
INSERT INTO orders VALUES
 (101,1,'2025-02-01',100),(102,1,'2025-03-05',200),(103,1,'2024-11-30',1000),
 (104,2,'2025-01-10',50),
 (105,3,'2025-04-01',150),(106,3,'2025-04-09',10),
 (107,5,'2024-12-31',900),
 (108,6,'2025-05-05',90);
"""
SQL_NESTED = """
SELECT name FROM customers
WHERE customer_id IN (
  SELECT customer_id FROM (
    SELECT customer_id, SUM(amount) AS total
    FROM orders WHERE order_date >= '2025-01-01' GROUP BY customer_id)
  WHERE total > (
    SELECT AVG(total) FROM (
      SELECT SUM(amount) AS total
      FROM orders WHERE order_date >= '2025-01-01' GROUP BY customer_id)))
ORDER BY name
"""
SQL_MAIN = """
WITH customer_totals AS (
  SELECT customer_id, SUM(amount) AS total
  FROM orders
  WHERE order_date >= '2025-01-01'
  GROUP BY customer_id
),
above_average AS (
  SELECT customer_id, total
  FROM customer_totals
  WHERE total > (SELECT AVG(total) FROM customer_totals)
)
SELECT c.name
FROM customers c
JOIN above_average a ON a.customer_id = c.customer_id
ORDER BY c.name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
nested = pd.read_sql_query(SQL_NESTED, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("nested query:", nested["name"].tolist())
print("CTE query   :", sql_df["name"].tolist())
print("\nstep 1 alone (select from the first CTE):")
print(pd.read_sql_query("""WITH customer_totals AS (SELECT customer_id, SUM(amount) AS total FROM orders
 WHERE order_date >= '2025-01-01' GROUP BY customer_id) SELECT * FROM customer_totals ORDER BY customer_id""", con).to_string(index=False))
print("\naverage of those totals:", con.execute("""WITH customer_totals AS (SELECT customer_id, SUM(amount) AS total FROM orders
 WHERE order_date >= '2025-01-01' GROUP BY customer_id) SELECT AVG(total) FROM customer_totals""").fetchone()[0])
print("\nwithout the date filter the same query returns:",
      [r[0] for r in con.execute(SQL_MAIN.replace("WHERE order_date >= '2025-01-01'", ""))])
print("\nEXPLAIN QUERY PLAN of the CTE version:")
for r in con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN):
    print("  ", r[3])

plan_n = [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + SQL_NESTED)]
plan_c = [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN)]
print("\nscans of orders in the plan: nested =", sum(x.startswith("SCAN orders") for x in plan_n),
      "| CTE =", sum(x.startswith("SCAN orders") for x in plan_c))

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
recent = orders[orders["order_date"] >= "2025-01-01"]
customer_totals = recent.groupby("customer_id")["amount"].sum()
above_average = customer_totals[customer_totals > customer_totals.mean()]
pd_df = (customers[customers["customer_id"].isin(above_average.index)][["name"]]
         .sort_values("name").reset_index(drop=True))
# pd:end
print("\npandas:", pd_df["name"].tolist())
# compared after sorting both by name
pd.testing.assert_frame_equal(nested.sort_values("name").reset_index(drop=True), sql_df.sort_values("name").reset_index(drop=True))
pd.testing.assert_frame_equal(sql_df.sort_values("name").reset_index(drop=True), pd_df, check_dtype=False)
print("asserts passed: nested == CTE == pandas")
```

**Output (my run):**
```text
nested query: ['Asha', 'Chitra']
CTE query   : ['Asha', 'Chitra']

step 1 alone (select from the first CTE):
 customer_id  total
           1    300
           2     50
           3    160
           6     90

average of those totals: 150.0

without the date filter the same query returns: ['Asha', 'Esha']

EXPLAIN QUERY PLAN of the CTE version:
   MATERIALIZE customer_totals
   SCAN orders
   USE TEMP B-TREE FOR GROUP BY
   SCAN customer_totals
   SCALAR SUBQUERY 2
   SCAN customer_totals
   SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   USE TEMP B-TREE FOR ORDER BY

scans of orders in the plan: nested = 2 | CTE = 1

pandas: ['Asha', 'Chitra']
asserts passed: nested == CTE == pandas
```

**Edge cases:**
- Customers with no qualifying orders (Dev, Esha) never reach the average, so they do not pull it down. If you want "average across all customers, zero for silent ones", you must build that population explicitly (LEFT JOIN from `customers`), which gives a different answer.
- Strict `>`: a customer exactly at the average is excluded. `>=` would include them.
- NULL amounts are ignored by SUM and AVG. A customer whose filtered amounts are all NULL gets a NULL total, which fails `total > average` and drops out (not run here, follows from SQL NULL rules).
- The two forms return the same names. In the pandas version `isin` on the index replaces `IN (subquery)`.

**Then explain:**
- **What the CTE buys:** names for each step (`customer_totals`, `above_average`), the `WHERE order_date >= ...` filter written once instead of twice, and a debugging path: replace the final SELECT with `SELECT * FROM customer_totals` and check each step against the sample data. My run does exactly that and prints the four totals.
- **Computed once:** in the text, yes. In the engine it depends. The SQLite plan for the CTE version shows `MATERIALIZE customer_totals` and one `SCAN orders`; the nested version has two `SCAN orders` lines (my run printed 2 versus 1). I would not promise that for other engines (not executed here): some inline a CTE referenced twice and compute it twice.
- **Alias point:** SQLite accepted `FROM (SELECT ...)` without an alias in my run. PostgreSQL and MySQL are commonly said to require an alias on every derived table (from memory, not executed here). A CTE name avoids the question.
- **Why not leave it nested:** the reader has to start at the innermost SELECT and work outwards.

**Follow-ups:**
- *Could this be done with a window function?* Yes, `AVG(total) OVER ()` on the totals, no second subquery. That is Part 4 and Part 5 material.
- *Is a CTE faster than a subquery?* Not by itself; it is mainly about readability. Whether it is materialised or inlined is engine specific (see Q17).
- *Why join instead of `IN (SELECT customer_id FROM above_average)`?* Either works here because `customer_id` is unique in `above_average`; the join avoids a nested subquery.

**Common mistakes:**
- Moving the date filter out of the totals step, which changes both the totals and the average.
- Averaging per-order amounts instead of per-customer totals.
- Naming CTEs `t1`, `t2`, so the refactor reads no better than the original.
- Assuming the CTE is "computed once" in every engine without checking the plan.

### Q12 ⭐⭐⭐ 🟡 Subquery in HAVING: employees(emp_id, name, dept_id, salary) and departments(dept_id, dept_name). List departments whose average salary is higher than the company-wide average salary. Write it with a scalar subquery in HAVING, explain why the subquery is evaluated once, why WHERE cannot hold an aggregate, and the equivalent with a CTE. Give the pandas groupby mean then mask version and state how a department with all-NULL salaries behaves.
**Asked at:** GeeksforGeeks SQL interview questions (subquery, correlated subquery, EXISTS vs IN, CTE entries), not candidate reports; analyst screens at IT services, GCCs and startups
**Say this first (1 line):** Group by department, then in HAVING compare `AVG(salary)` with a scalar subquery `(SELECT AVG(salary) FROM employees)`; WHERE runs before grouping so it cannot see an aggregate, and HAVING runs after.

**Schema and sample data:**
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (1,'Eng'),(2,'Sales'),(3,'HR'),(4,'Ops'),(5,'Legal');
INSERT INTO employees VALUES
 (1,'Asha',1,100),(2,'Ben',1,80),(3,'Chitra',1,120),
 (4,'Dev',2,50),(5,'Esha',2,60),
 (6,'Faiz',3,90),(7,'Gita',3,NULL),
 (8,'Hari',4,NULL),(9,'Isha',4,NULL);
```

**SQL answer:** `SQL_MAIN` is the HAVING version and `SQL_CTE` is the CTE equivalent; both run in the Code block.
```sql
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING AVG(e.salary) > (SELECT AVG(salary) FROM employees)
ORDER BY d.dept_name
```

**pandas answer:** groupby mean, then a boolean mask against the company mean (same text as in the Code block).
```python
dept_avg = employees.groupby("dept_id")["salary"].mean()
company_avg = employees["salary"].mean()
winners = dept_avg[dept_avg > company_avg].rename("avg_salary").reset_index()
pd_df = (winners.merge(departments, on="dept_id")[["dept_name", "avg_salary"]]
         .sort_values("dept_name").reset_index(drop=True))
```

**Example:** The nine employees have salaries 100, 80, 120 (Eng), 50, 60 (Sales), 90 and NULL (HR), NULL and NULL (Ops). Legal has no employees.
- Company average over the six non-NULL salaries: (100 + 80 + 120 + 50 + 60 + 90) / 6 = 500 / 6 = 83.33.
- Department averages: Eng 100, Sales 55, HR 90 (the NULL is ignored: 90 / 1), Ops NULL, Legal has no group at all.
- HAVING keeps Eng (100 > 83.33) and HR (90 > 83.33). Sales fails; Ops compares NULL with 83.33, which is unknown, so it is not kept.
- If NULL were treated as 0, HR would be 45 and would fail. AVG ignores NULL instead.

**Code:** run with `python3 -I`.
```python
# Q12: departments whose average salary beats the company-wide average (scalar subquery in HAVING)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (1,'Eng'),(2,'Sales'),(3,'HR'),(4,'Ops'),(5,'Legal');
INSERT INTO employees VALUES
 (1,'Asha',1,100),(2,'Ben',1,80),(3,'Chitra',1,120),
 (4,'Dev',2,50),(5,'Esha',2,60),
 (6,'Faiz',3,90),(7,'Gita',3,NULL),
 (8,'Hari',4,NULL),(9,'Isha',4,NULL);
"""
SQL_MAIN = """
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING AVG(e.salary) > (SELECT AVG(salary) FROM employees)
ORDER BY d.dept_name
"""
SQL_CTE = """
WITH company AS (SELECT AVG(salary) AS avg_all FROM employees),
dept AS (
  SELECT d.dept_id, d.dept_name, AVG(e.salary) AS avg_salary
  FROM employees e JOIN departments d ON d.dept_id = e.dept_id
  GROUP BY d.dept_id, d.dept_name
)
SELECT dept_name, avg_salary
FROM dept, company
WHERE avg_salary > avg_all
ORDER BY dept_name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
cte_df = pd.read_sql_query(SQL_CTE, con)
print("HAVING with scalar subquery:")
print(sql_df.to_string(index=False))
print("\nCTE version equal:", sql_df.equals(cte_df))
print("\nper department (all, for checking):")
print(pd.read_sql_query("""SELECT d.dept_name, COUNT(e.emp_id) AS heads, COUNT(e.salary) AS with_salary, AVG(e.salary) AS avg_salary
 FROM departments d LEFT JOIN employees e ON e.dept_id = d.dept_id GROUP BY d.dept_id, d.dept_name ORDER BY d.dept_id""", con).to_string(index=False))
print("\ncompany average (NULLs ignored):", con.execute("SELECT AVG(salary) FROM employees").fetchone()[0])
print("average of the department averages (a different number):",
      con.execute("SELECT AVG(a) FROM (SELECT AVG(salary) AS a FROM employees GROUP BY dept_id) x WHERE a IS NOT NULL").fetchone()[0])
calls = []
con.create_function("tick", 1, lambda v: calls.append(v) or v)
con.execute("""SELECT d.dept_name FROM employees e JOIN departments d ON d.dept_id = e.dept_id
               GROUP BY d.dept_id HAVING AVG(e.salary) > (SELECT AVG(tick(salary)) FROM employees)""").fetchall()
print("\ntimes the subquery read a salary row (9 employees, 4 departments):", len(calls))
assert len(calls) == 9
try:
    con.execute("SELECT dept_id FROM employees WHERE AVG(salary) > 80 GROUP BY dept_id")
except sqlite3.Error as e:
    print("\nAggregate in WHERE ->", e)

employees = pd.read_sql_query("SELECT * FROM employees", con)
departments = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
dept_avg = employees.groupby("dept_id")["salary"].mean()
company_avg = employees["salary"].mean()
winners = dept_avg[dept_avg > company_avg].rename("avg_salary").reset_index()
pd_df = (winners.merge(departments, on="dept_id")[["dept_name", "avg_salary"]]
         .sort_values("dept_name").reset_index(drop=True))
# pd:end
print("\npandas dept means:", dept_avg.to_dict(), "| company mean:", company_avg)
print(pd_df.to_string(index=False))
# compared after sorting both by dept_name
pd.testing.assert_frame_equal(sql_df.sort_values("dept_name").reset_index(drop=True), pd_df, check_dtype=False)
assert pd.isna(dept_avg[4]) and not (dept_avg[4] > company_avg)
print("\nsum of an all-NaN group:", employees[employees.dept_id == 4]["salary"].sum(),
      "| with min_count=1:", employees[employees.dept_id == 4]["salary"].sum(min_count=1))
print("asserts passed: SQL == pandas; the all-NULL department (Ops) is not returned")
```

**Output (my run):**
```text
HAVING with scalar subquery:
dept_name  avg_salary
      Eng       100.0
       HR        90.0

CTE version equal: True

per department (all, for checking):
dept_name  heads  with_salary  avg_salary
      Eng      3            3       100.0
    Sales      2            2        55.0
       HR      2            1        90.0
      Ops      2            0         NaN
    Legal      0            0         NaN

company average (NULLs ignored): 83.33333333333333
average of the department averages (a different number): 81.66666666666667

times the subquery read a salary row (9 employees, 4 departments): 9

Aggregate in WHERE -> misuse of aggregate: AVG()

pandas dept means: {1: 100.0, 2: 55.0, 3: 90.0, 4: nan} | company mean: 83.33333333333333
dept_name  avg_salary
      Eng       100.0
       HR        90.0

sum of an all-NaN group: 0.0 | with min_count=1: nan
asserts passed: SQL == pandas; the all-NULL department (Ops) is not returned
```

**Edge cases:**
- **All-NULL department (Ops):** `AVG` is NULL, `NULL > x` is unknown, so the department is dropped. In pandas the group mean is NaN and `NaN > x` is False, so it is dropped as well; my assert checks that. Compare `sum()`: the sum of an all-NaN group is 0.0 in pandas (my run) unless you pass `min_count=1`, which gives NaN. SQL `SUM` of all NULLs is NULL. So a "sum above the company sum" mask would treat Ops as 0 in pandas, not NULL.
- **Department with no employees (Legal):** the inner JOIN never produces a group for it. A LEFT JOIN from `departments` would give it a NULL average, still excluded.
- **Employees with NULL dept_id:** they join to nothing, so they are not in any department row, but they still count in the company average (the subquery reads `employees` directly). I did not include such a row in the sample data.
- **Which "company average":** the average of all salaries (83.33) is not the average of the department averages (81.67 in my run); using the second one is a different question.

**Then explain:**
- **Evaluated once:** the subquery is uncorrelated (it does not mention the outer query), so the engine can compute it one time and reuse the number. I checked this in SQLite with a counting function inside the subquery: it saw 9 salary reads, one per employee, not 9 times four groups. The SQLite docs say an uncorrelated subquery is evaluated once; other engines I have not executed.
- **WHERE cannot hold an aggregate:** WHERE filters individual rows before groups exist. SQLite's error in my run was `misuse of aggregate: AVG()`. HAVING filters groups after aggregation.
- **CTE form:** compute the company average in one CTE and the department averages in another, then compare. Same result (my run printed `CTE version equal: True`), easier to read and test.
- **pandas:** `groupby("dept_id")["salary"].mean()` gives one value per department, the mask keeps those above the scalar `employees["salary"].mean()`, then merge for the names.

**Follow-ups:**
- *Why not WHERE salary > (SELECT AVG ...)?* That answers a different question: employees above the average, not departments.
- *Departments above the average of their own company, per company?* Then the subquery becomes correlated on company id.
- *Window version?* `AVG(salary) OVER ()` next to the department average; see Part 4 and Part 5.

**Common mistakes:**
- Putting `AVG(salary) > ...` in WHERE.
- Comparing with the average of department averages.
- Forgetting that NULL salaries are ignored by AVG and that an all-NULL group is silently dropped.
- Using `sum()` in pandas and expecting NaN for an all-NaN group.

### Q13 ⭐⭐⭐ 🟡 Both an EXISTS and a NOT EXISTS in one query: users(user_id, name) and orders(order_id, user_id, status), where status is 'paid' or 'returned'. List users who have at least one paid order and no returned order. Write it with EXISTS plus NOT EXISTS, and a GROUP BY ... HAVING version using conditional SUM, state which is more readable, and give the pandas version (isin on two key sets).
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
**Say this first (1 line):** Use `EXISTS` for "has a paid order" and `NOT EXISTS` for "has no returned order" in the same WHERE; each subquery is correlated on `user_id` and only asks whether a row exists, so users with several paid orders are not duplicated.

**Schema and sample data:**
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT);
INSERT INTO users VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO orders VALUES
 (101,1,'paid'),(102,1,'paid'),
 (103,2,'paid'),(104,2,'returned'),
 (105,3,'returned'),
 (106,5,'paid'),
 (107,NULL,'returned');
```

**SQL answer:** `SQL_MAIN` is the EXISTS plus NOT EXISTS form, `SQL_HAVING` the conditional-SUM form, `SQL_NOT_IN` the trap version; all run in the Code block.
```sql
SELECT u.user_id, u.name
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.user_id AND o.status = 'paid')
  AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.user_id AND o.status = 'returned')
ORDER BY u.user_id
```

**pandas answer:** two key sets and `isin` (same text as in the Code block).
```python
paid_ids = orders.loc[orders["status"] == "paid", "user_id"]
returned_ids = orders.loc[orders["status"] == "returned", "user_id"]
pd_df = (users[users["user_id"].isin(paid_ids) & ~users["user_id"].isin(returned_ids)]
         .sort_values("user_id").reset_index(drop=True))
```

**Example:**
- Asha has two paid orders and no returns: qualifies (listed once, because EXISTS does not multiply rows).
- Ben has a paid and a returned order: excluded by NOT EXISTS.
- Chitra has only a returned order: excluded by EXISTS.
- Dev has no orders: excluded by EXISTS.
- Esha has one paid order, no returns: qualifies.
- Result: Asha and Esha. Order 107 has a NULL `user_id` and status returned; it belongs to nobody and changes nothing for EXISTS.

**Code:** run with `python3 -I`.
```python
# Q13: users with at least one paid order and no returned order (EXISTS + NOT EXISTS)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT);
INSERT INTO users VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO orders VALUES
 (101,1,'paid'),(102,1,'paid'),
 (103,2,'paid'),(104,2,'returned'),
 (105,3,'returned'),
 (106,5,'paid'),
 (107,NULL,'returned');
"""
SQL_MAIN = """
SELECT u.user_id, u.name
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.user_id AND o.status = 'paid')
  AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.user_id AND o.status = 'returned')
ORDER BY u.user_id
"""
SQL_HAVING = """
SELECT u.user_id, u.name
FROM users u
JOIN orders o ON o.user_id = u.user_id
GROUP BY u.user_id, u.name
HAVING SUM(CASE WHEN o.status = 'paid' THEN 1 ELSE 0 END) >= 1
   AND SUM(CASE WHEN o.status = 'returned' THEN 1 ELSE 0 END) = 0
ORDER BY u.user_id
"""
SQL_NOT_IN = """
SELECT u.user_id, u.name
FROM users u
WHERE u.user_id IN (SELECT user_id FROM orders WHERE status = 'paid')
  AND u.user_id NOT IN (SELECT user_id FROM orders WHERE status = 'returned')
ORDER BY u.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
having_df = pd.read_sql_query(SQL_HAVING, con)
not_in_df = pd.read_sql_query(SQL_NOT_IN, con)
print("EXISTS + NOT EXISTS:", sql_df["name"].tolist())
print("GROUP BY/HAVING    :", having_df["name"].tolist())
print("IN + NOT IN (orphan returned row has NULL user_id):", not_in_df["name"].tolist())
dup = con.execute("SELECT COUNT(*) FROM users u JOIN orders o ON o.user_id = u.user_id AND o.status = 'paid' WHERE u.user_id = 1").fetchone()[0]
print("rows a plain JOIN gives Asha for her paid orders:", dup)

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
paid_ids = orders.loc[orders["status"] == "paid", "user_id"]
returned_ids = orders.loc[orders["status"] == "returned", "user_id"]
pd_df = (users[users["user_id"].isin(paid_ids) & ~users["user_id"].isin(returned_ids)]
         .sort_values("user_id").reset_index(drop=True))
# pd:end
print("\npandas:", pd_df["name"].tolist(), "| returned_ids has NaN:", bool(returned_ids.isna().any()))
# compared after sorting both by user_id
pd.testing.assert_frame_equal(sql_df, having_df)
pd.testing.assert_frame_equal(sql_df.sort_values("user_id").reset_index(drop=True), pd_df, check_dtype=False)
assert not_in_df.empty
print("asserts passed: EXISTS version == HAVING version == pandas; NOT IN version returned 0 rows")
```

**Output (my run):**
```text
EXISTS + NOT EXISTS: ['Asha', 'Esha']
GROUP BY/HAVING    : ['Asha', 'Esha']
IN + NOT IN (orphan returned row has NULL user_id): []
rows a plain JOIN gives Asha for her paid orders: 2

pandas: ['Asha', 'Esha'] | returned_ids has NaN: True
asserts passed: EXISTS version == HAVING version == pandas; NOT IN version returned 0 rows
```

**Edge cases:**
- **NOT IN trap:** `u.user_id NOT IN (SELECT user_id FROM orders WHERE status = 'returned')` returns zero rows here, because the subquery contains a NULL (order 107) and `x NOT IN (..., NULL)` is never true. The asserts in my run check this. NOT EXISTS has no such problem.
- **Users with no orders:** the HAVING version starts from `users JOIN orders`, so Dev never appears; here that is correct, but for "no returned order" alone (without the paid condition) a join-based version would lose users with no orders.
- **NULL status:** the conditional SUM treats a NULL status as neither paid nor returned (`CASE` falls to ELSE 0). The brief says status is only paid or returned, so I did not put one in the data.
- **pandas and NaN:** `returned_ids` contains NaN (my run printed `True`). `isin` would match a NaN `user_id` against it, but users have no NaN ids, and `~isin` returns a plain True/False, so there is no NOT IN trap in pandas.

**Then explain:**
- **Readability:** EXISTS plus NOT EXISTS says the business rule in two lines. The HAVING version needs two CASE sums and a join plus group, which is compact but harder to read; I would pick EXISTS for this question. HAVING wins when you also want the counts (how many paid, how many returned) in the output.
- **Duplicates:** a plain join to paid orders gives Asha two rows (my run printed 2), so a join version needs DISTINCT; EXISTS does not.
- **Both forms agree:** my run asserts they return the same rows, and pandas matches.
- **Performance:** with an index on `orders(user_id, status)` both EXISTS probes are index lookups. I did not time it here.

**Follow-ups:**
- *Users with a paid order and a returned order?* Two EXISTS.
- *Only if the return came after the paid order?* Correlate the dates in the second subquery.
- *Why SELECT 1?* The select list is ignored by EXISTS; the 1 is convention.

**Common mistakes:**
- Using NOT IN with a subquery column that can be NULL.
- Joining to orders and filtering `status = 'paid' AND status <> 'returned'`, which tests one row at a time and can never exclude a user.
- Using `HAVING SUM(status = 'returned') = 0` and forgetting that a user with no rows is already gone after the join.

### Q14 ⭐⭐⭐ 🔴 Customers who bought every product (the Customers Who Bought All Products idea): products(product_id, name) and orders(order_id, customer_id, product_id), where a customer may buy the same product several times and product_id is never NULL. List customers who bought every product. Use GROUP BY customer_id HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products), explain why DISTINCT is essential, what breaks if orders contains a product_id not in products, and give pandas (groupby nunique compared with the product count).
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Group orders by customer and keep customers where `COUNT(DISTINCT product_id)` equals the number of products; DISTINCT is essential because repeat purchases inflate a plain count, and the product list must be limited to real products.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO products VALUES (1,'Phone'),(2,'Case'),(3,'Charger');
INSERT INTO orders VALUES
 (1,1,1),(2,1,2),(3,1,3),(4,1,1),
 (5,2,1),(6,2,2),
 (7,3,3),(8,3,2),(9,3,1),
 (10,4,1),(11,4,1),(12,4,1),
 (13,5,1),(14,5,2),(15,5,99);
```

**SQL answer:** `SQL_MAIN` is the form from the question, `SQL_SAFE` is the version that ignores product ids that are not in `products`, and `SQL_DIVISION` is the double NOT EXISTS form; all run in the Code block.
```sql
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products)
ORDER BY customer_id
```

**pandas answer:** filter to known products first, then `nunique` against the product count (same text as in the Code block).
```python
n_products = len(products)
valid = orders[orders["product_id"].isin(products["product_id"])]
bought = valid.groupby("customer_id")["product_id"].nunique()
pd_df = bought[bought == n_products].index.to_frame(index=False).sort_values("customer_id").reset_index(drop=True)
```

**Example:** Three products (1 Phone, 2 Case, 3 Charger).
- Customer 1: products 1, 2, 3, 1 (4 rows, 3 distinct): bought all. Customer 3: 3, 2, 1: bought all.
- Customer 2: 1, 2: missing the Charger. Customer 4: three Phones, 1 distinct: no.
- Customer 5: products 1, 2 and 99. 99 is not in `products`, so distinct count is 3, which equals the product count, but the Charger was never bought. `SQL_MAIN` wrongly returns 5; filtering to known products (`SQL_SAFE`) gives only 1 and 3.
- Without DISTINCT, `COUNT(product_id)` counts rows: customer 1 has 4 rows and is wrongly dropped, while customers 4 and 5 (3 rows each) are wrongly kept. My run returned 3, 4, 5.

**Code:** run with `python3 -I`.
```python
# Q14: customers who bought every product (relational division)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO products VALUES (1,'Phone'),(2,'Case'),(3,'Charger');
INSERT INTO orders VALUES
 (1,1,1),(2,1,2),(3,1,3),(4,1,1),
 (5,2,1),(6,2,2),
 (7,3,3),(8,3,2),(9,3,1),
 (10,4,1),(11,4,1),(12,4,1),
 (13,5,1),(14,5,2),(15,5,99);
"""
SQL_MAIN = """
SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products)
ORDER BY customer_id
"""
SQL_SAFE = """
SELECT customer_id
FROM orders
WHERE product_id IN (SELECT product_id FROM products)
GROUP BY customer_id
HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products)
ORDER BY customer_id
"""
SQL_DIVISION = """
SELECT c.customer_id
FROM (SELECT DISTINCT customer_id FROM orders) c
WHERE NOT EXISTS (
  SELECT 1 FROM products p
  WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.product_id = p.product_id))
ORDER BY c.customer_id
"""
SQL_NO_DISTINCT = """
SELECT customer_id FROM orders GROUP BY customer_id
HAVING COUNT(product_id) = (SELECT COUNT(*) FROM products) ORDER BY customer_id
"""
def ids(con, sql):
    return [r[0] for r in con.execute(sql)]
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("per customer: rows / distinct products / distinct valid products")
for r in con.execute("""SELECT customer_id, COUNT(*), COUNT(DISTINCT product_id),
   COUNT(DISTINCT CASE WHEN product_id IN (SELECT product_id FROM products) THEN product_id END)
   FROM orders GROUP BY customer_id"""):
    print("  ", r)
print("\nHAVING COUNT(DISTINCT) as written      :", ids(con, SQL_MAIN))
print("same, but filtered to known products   :", ids(con, SQL_SAFE))
print("double NOT EXISTS                      :", ids(con, SQL_DIVISION))
print("without DISTINCT (wrong)               :", ids(con, SQL_NO_DISTINCT))

# empty products table: vacuous truth
con2 = sqlite3.connect(":memory:")
con2.executescript(SCHEMA)
con2.execute("DELETE FROM products")
print("\nwith an empty products table -> HAVING version:", ids(con2, SQL_SAFE), "| double NOT EXISTS:", ids(con2, SQL_DIVISION))

products = pd.read_sql_query("SELECT * FROM products", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
n_products = len(products)
valid = orders[orders["product_id"].isin(products["product_id"])]
bought = valid.groupby("customer_id")["product_id"].nunique()
pd_df = bought[bought == n_products].index.to_frame(index=False).sort_values("customer_id").reset_index(drop=True)
# pd:end
naive = orders.groupby("customer_id")["product_id"].nunique()
print("\npandas nunique on all rows:", naive.to_dict(), "-> would wrongly keep", naive[naive == n_products].index.tolist())
print("pandas after filtering to known products:", pd_df["customer_id"].tolist())
sql_df = pd.DataFrame({"customer_id": ids(con, SQL_SAFE)})
# compared after sorting both by customer_id
pd.testing.assert_frame_equal(sql_df.sort_values("customer_id").reset_index(drop=True), pd_df, check_dtype=False)
assert ids(con, SQL_SAFE) == ids(con, SQL_DIVISION) == [1, 3]
assert ids(con, SQL_MAIN) == [1, 3, 5] and ids(con, SQL_NO_DISTINCT) == [3, 4, 5]
assert ids(con2, SQL_SAFE) == [] and ids(con2, SQL_DIVISION) == [1, 2, 3, 4, 5]
print("asserts passed: SQL == pandas == [1, 3]")
```

**Output (my run):**
```text
per customer: rows / distinct products / distinct valid products
   (1, 4, 3, 3)
   (2, 2, 2, 2)
   (3, 3, 3, 3)
   (4, 3, 1, 1)
   (5, 3, 3, 2)

HAVING COUNT(DISTINCT) as written      : [1, 3, 5]
same, but filtered to known products   : [1, 3]
double NOT EXISTS                      : [1, 3]
without DISTINCT (wrong)               : [3, 4, 5]

with an empty products table -> HAVING version: [] | double NOT EXISTS: [1, 2, 3, 4, 5]

pandas nunique on all rows: {1: 3, 2: 2, 3: 3, 4: 1, 5: 3} -> would wrongly keep [1, 3, 5]
pandas after filtering to known products: [1, 3]
asserts passed: SQL == pandas == [1, 3]
```

**Edge cases:**
- **Product not in the catalogue:** shown above (customer 5). Fix with `WHERE product_id IN (SELECT product_id FROM products)` or a join to `products`, or a foreign key if the data model allows.
- **Empty `products` table:** the HAVING form returns no customers (their distinct count is at least 1, never 0). The double NOT EXISTS form returns every customer, because "for every product..." is vacuously true (my run: `[]` against `[1, 2, 3, 4, 5]`). Decide which is meant.
- **NULL product_id:** the question says it is never NULL; `COUNT(DISTINCT x)` ignores NULLs anyway.
- **Customers with no orders:** not in `orders`, so not returned. Starting the division from a `customers` table would need `NOT EXISTS` with that table.

**Then explain:**
- **Why DISTINCT:** you are asking "how many different products", not "how many order lines". Without it the answer depends on how often people re-buy.
- **Shape:** this is relational division. Two standard answers: count distinct and compare with the total (short, but fragile if the data is dirty) or double NOT EXISTS ("there is no product for which this customer has no order"), which is robust to extra product ids but harder to read.
- **pandas:** `groupby("customer_id")["product_id"].nunique()` compared with `len(products)`. My run shows that without the `isin` filter pandas makes the same mistake with customer 5.
- **Scalar subquery:** `(SELECT COUNT(*) FROM products)` is uncorrelated and is read once.

**Follow-ups:**
- *Customers who bought all products in a category?* Add the category filter to both the products count and the orders.
- *What if the same product can be returned?* Filter the orders you count first.
- *Window version?* Not natural here; this one is a grouping problem.

**Common mistakes:**
- Dropping DISTINCT.
- Comparing with a hard-coded number of products.
- Not checking for orders whose product is not in the catalogue.
- Expecting the empty-catalogue case to behave the same in both forms.

### Q15 ⭐⭐⭐ 🔴 Nth highest salary without window functions (the window version is Part 4): employees(emp_id, name, salary) with duplicate salaries and possibly fewer than N distinct values. Write the 2nd and generic Nth highest distinct salary with SELECT DISTINCT salary ... ORDER BY salary DESC LIMIT 1 OFFSET n-1 wrapped so it returns NULL when absent, and with a correlated COUNT(DISTINCT) version. Explain why DISTINCT matters with ties, how to return NULL (scalar subquery around the LIMIT), and the pandas drop_duplicates, nlargest or unique approach. Note that the ranking-function version is covered in Part 4.
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Take the distinct salaries, sort them descending, skip N-1 and take one, all inside a scalar subquery so that a missing Nth value comes back as NULL instead of no row; the correlated alternative counts how many distinct salaries are higher.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',300),(2,'Ben',300),(3,'Chitra',200),(4,'Dev',200),
 (5,'Esha',150),(6,'Faiz',100),(7,'Gita',NULL);
```

**SQL answer:** `SQL_MAIN` is the LIMIT/OFFSET version with `?` as N, `SQL_CORR` is the correlated COUNT(DISTINCT) version; both run in the Code block.
```sql
SELECT (SELECT DISTINCT salary
        FROM employees
        WHERE salary IS NOT NULL
        ORDER BY salary DESC
        LIMIT 1 OFFSET ? - 1) AS nth_salary
```
```sql
SELECT (SELECT DISTINCT e1.salary
        FROM employees e1
        WHERE (SELECT COUNT(DISTINCT e2.salary) FROM employees e2 WHERE e2.salary > e1.salary) = ? - 1) AS nth_salary
```

**pandas answer:** deduplicate, sort, index (same text as in the Code block); the Code block also checks an `nlargest` form.
```python
def nth_highest(df, n):
    s = df["salary"].dropna().drop_duplicates().sort_values(ascending=False)
    return s.iloc[n - 1] if 1 <= n <= len(s) else None
```

**Example:** Salaries are 300, 300, 200, 200, 150, 100 and one NULL (Gita).
- Distinct, non-NULL, descending: 300, 200, 150, 100.
- N = 2: skip one row, take the next: 200. Without DISTINCT the 2nd row would be 300 again (my run printed 300 for the no-DISTINCT query).
- N = 5 or 6: only four distinct values exist, the inner query returns no row, and the scalar subquery turns that into NULL.
- Correlated version for N = 2: a salary qualifies when exactly N-1 = 1 distinct salary is higher. Only 200 has one higher distinct value (300), so it returns 200.

**Code:** run with `python3 -I`.
```python
# Q15: Nth highest distinct salary without window functions, NULL when absent
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',300),(2,'Ben',300),(3,'Chitra',200),(4,'Dev',200),
 (5,'Esha',150),(6,'Faiz',100),(7,'Gita',NULL);
"""
SQL_MAIN = """
SELECT (SELECT DISTINCT salary
        FROM employees
        WHERE salary IS NOT NULL
        ORDER BY salary DESC
        LIMIT 1 OFFSET ? - 1) AS nth_salary
"""
SQL_CORR = """
SELECT (SELECT DISTINCT e1.salary
        FROM employees e1
        WHERE (SELECT COUNT(DISTINCT e2.salary) FROM employees e2 WHERE e2.salary > e1.salary) = ? - 1) AS nth_salary
"""
SQL_NO_DISTINCT = """
SELECT salary FROM employees WHERE salary IS NOT NULL ORDER BY salary DESC LIMIT 1 OFFSET 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
employees = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
def nth_highest(df, n):
    s = df["salary"].dropna().drop_duplicates().sort_values(ascending=False)
    return s.iloc[n - 1] if 1 <= n <= len(s) else None
# pd:end
def nth_nlargest(df, n):
    s = df["salary"].dropna().drop_duplicates()
    return s.nlargest(n).iloc[-1] if 1 <= n <= len(s) else None

print("N | LIMIT/OFFSET | correlated | pandas sort | pandas nlargest")
rows = []
for n in range(0, 7):
    a = con.execute(SQL_MAIN, (n,)).fetchone()[0]
    b = con.execute(SQL_CORR, (n,)).fetchone()[0]
    c = nth_highest(employees, n)
    d = nth_nlargest(employees, n)
    c = None if c is None else int(c)
    d = None if d is None else int(d)
    rows.append((n, a, b, c, d))
    print(n, "|", a, "|", b, "|", c, "|", d)
print("\nwithout DISTINCT, 2nd row of the salaries:", con.execute(SQL_NO_DISTINCT).fetchone()[0])
print("NULL salary sorted last or first in DESC order (SQLite):",
      [r[0] for r in con.execute("SELECT DISTINCT salary FROM employees ORDER BY salary DESC")])
print("pandas iloc[-1] when n = 0 would give the LOWEST:", employees["salary"].dropna().drop_duplicates().sort_values(ascending=False).iloc[-1])
# compared row by row for N = 1..6 (N = 0 is shown above but excluded: the two SQL forms disagree there)
for n, a, b, c, d in rows:
    if n >= 1:
        assert a == b == c == d, (n, a, b, c, d)
assert [r[1] for r in rows] == [300, 300, 200, 150, 100, None, None] and rows[0][2] is None
print("asserts passed for N = 1..6: both SQL forms == both pandas forms")
```

**Output (my run):**
```text
N | LIMIT/OFFSET | correlated | pandas sort | pandas nlargest
0 | 300 | None | None | None
1 | 300 | 300 | 300 | 300
2 | 200 | 200 | 200 | 200
3 | 150 | 150 | 150 | 150
4 | 100 | 100 | 100 | 100
5 | None | None | None | None
6 | None | None | None | None

without DISTINCT, 2nd row of the salaries: 300
NULL salary sorted last or first in DESC order (SQLite): [300, 200, 150, 100, None]
pandas iloc[-1] when n = 0 would give the LOWEST: 100.0
asserts passed for N = 1..6: both SQL forms == both pandas forms
```

**Edge cases:**
- **Fewer than N distinct values:** NULL in all four methods (pandas gives `None` by my guard).
- **NULL salary:** in SQLite NULL sorts first ascending and last descending (my run shows it as the last value of the DESC list), so it would be skipped by small N, but it could be returned as the last distinct "value" when N is large. Filter with `salary IS NOT NULL`. PostgreSQL puts NULLs first in DESC order by default (from memory, not executed here), which would be wrong for the unfiltered form.
- **N = 0 (a surprise):** the LIMIT/OFFSET version computes `OFFSET -1`. SQLite treats a negative offset as 0, so it returned 300, the highest, silently (my run, N = 0 row). The correlated version returned NULL. Validate N >= 1 in the caller. Other engines are said to reject a negative OFFSET (not executed here).
- **pandas N = 0:** `iloc[-1]` would return the lowest salary (100.0 in my run), so the guard `1 <= n <= len(s)` is needed.
- **Ties:** DISTINCT collapses them; that is "Nth highest distinct salary". If you want the Nth row including ties, drop DISTINCT but then say so.

**Then explain:**
- **Why DISTINCT:** two people at 300 are one salary level; without it "2nd highest" is 300 again.
- **Why a scalar subquery for NULL:** a scalar subquery returning no rows evaluates to NULL (SQLite docs and my run: the N = 5 row). A bare `SELECT ... LIMIT 1 OFFSET 4` returns zero rows, which an application may treat as an error.
- **Expressions in LIMIT/OFFSET:** `LIMIT 1 OFFSET ? - 1` ran in my SQLite 3.45 run, with the parameter bound. Whether other engines accept an expression or a parameter there is not executed here.
- **Correlated version:** simpler to reason about for any N but O(n squared) work in the worst case; it also returns every row's salary that matches, so wrap it as I did if you need a single value.
- **Ranking functions:** `DENSE_RANK() OVER (ORDER BY salary DESC)` is the clean version; see Part 4.

**Follow-ups:**
- *Nth highest per department?* The correlated count becomes `... AND e2.dept_id = e1.dept_id`, or use ranking in Part 4.
- *Nth highest without DISTINCT, ties counted?* Use the OFFSET without DISTINCT.
- *Median?* Needs two rows around the middle; covered later in this part.

**Common mistakes:**
- Forgetting DISTINCT.
- Returning no row instead of NULL when N exceeds the distinct count.
- Letting NULL salaries into the ordering.
- Off-by-one: OFFSET is N-1, not N.
- Not guarding N <= 0.

### Q16 ⭐⭐⭐ 🔴 Debug a wrong total caused by a join fan-out inside a CTE: orders(order_id, customer_id, order_total) and order_items(item_id, order_id, product_id, qty). A report has WITH j AS (SELECT o.order_id, o.customer_id, o.order_total, i.item_id FROM orders o JOIN order_items i ON i.order_id = o.order_id) SELECT customer_id, SUM(order_total) FROM j GROUP BY customer_id and shows inflated revenue. Diagnose it by selecting from the CTE and comparing COUNT(*) with COUNT(DISTINCT order_id), then fix it two ways (aggregate items to one row per order in the CTE first, or sum from orders alone). Explain why the CTE hid the problem and how to test each CTE separately, and show the same bug and fix in pandas.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Joining orders to order_items repeats each order once per item, so `SUM(order_total)` is counted once per item row; select from the CTE and compare `COUNT(*)` with `COUNT(DISTINCT order_id)` to see it, then aggregate items to one row per order first or sum from `orders` alone.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,200),(4,3,80);
INSERT INTO order_items VALUES (11,1,7,1),(12,1,8,2),(13,1,9,1),(14,2,7,1),(15,3,8,1),(16,3,9,4);
```

**SQL answer:** `SQL_BAD` is the report as written, `SQL_DIAG` is the diagnosis, `SQL_MAIN` is fix 1, `SQL_ALONE` is fix 2; all run in the Code block.
```sql
WITH item_totals AS (
  SELECT order_id, SUM(qty) AS units FROM order_items GROUP BY order_id
),
j AS (
  SELECT o.order_id, o.customer_id, o.order_total, COALESCE(t.units, 0) AS units
  FROM orders o LEFT JOIN item_totals t ON t.order_id = o.order_id
)
SELECT customer_id, SUM(order_total) AS revenue, SUM(units) AS units
FROM j GROUP BY customer_id ORDER BY customer_id
```
Fix 2, when item detail is not needed:
```sql
SELECT customer_id, SUM(order_total) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id
```

**pandas answer:** aggregate items first, then a validated left merge (same text as in the Code block).
```python
item_totals = items.groupby("order_id", as_index=False).agg(units=("qty", "sum"))
j = orders.merge(item_totals, on="order_id", how="left", validate="one_to_one").fillna({"units": 0})
pd_df = (j.groupby("customer_id", as_index=False)
          .agg(revenue=("order_total", "sum"), units=("units", "sum"))
          .astype({"units": "int64"}).sort_values("customer_id").reset_index(drop=True))
```

**Example:**
- Order 1 (customer 1, total 100) has 3 item rows; order 2 (customer 1, total 50) has 1; order 3 (customer 2, total 200) has 2; order 4 (customer 3, total 80) has none.
- The report's inner join gives 6 rows for 3 orders. Customer 1 shows 100 x 3 + 50 = 350 instead of 150; customer 2 shows 200 x 2 = 400 instead of 200.
- Customer 3 is missing entirely: the inner join drops an order with no items. So there are two bugs, inflation and loss.
- Diagnosis query on the CTE: 6 rows, 3 distinct orders (and the table has 4 orders). If rows exceed distinct orders, the CTE fanned out.
- Fix 1: item_totals gives one row per order (order 1 has 4 units, order 2 has 1, order 3 has 5); a LEFT JOIN keeps order 4 with 0 units. Revenue is 150, 200, 80 and units are 5, 5, 0. It ties to 430, the sum of `orders` alone.

**Code:** run with `python3 -I`.
```python
# Q16: wrong total from a join fan-out hidden inside a CTE
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,200),(4,3,80);
INSERT INTO order_items VALUES (11,1,7,1),(12,1,8,2),(13,1,9,1),(14,2,7,1),(15,3,8,1),(16,3,9,4);
"""
SQL_BAD = """
WITH j AS (
  SELECT o.order_id, o.customer_id, o.order_total, i.item_id
  FROM orders o JOIN order_items i ON i.order_id = o.order_id
)
SELECT customer_id, SUM(order_total) AS revenue FROM j GROUP BY customer_id ORDER BY customer_id
"""
SQL_DIAG = """
WITH j AS (
  SELECT o.order_id, o.customer_id, o.order_total, i.item_id
  FROM orders o JOIN order_items i ON i.order_id = o.order_id
)
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT order_id) AS n_orders FROM j
"""
SQL_MAIN = """
WITH item_totals AS (
  SELECT order_id, SUM(qty) AS units FROM order_items GROUP BY order_id
),
j AS (
  SELECT o.order_id, o.customer_id, o.order_total, COALESCE(t.units, 0) AS units
  FROM orders o LEFT JOIN item_totals t ON t.order_id = o.order_id
)
SELECT customer_id, SUM(order_total) AS revenue, SUM(units) AS units
FROM j GROUP BY customer_id ORDER BY customer_id
"""
SQL_ALONE = "SELECT customer_id, SUM(order_total) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
bad = pd.read_sql_query(SQL_BAD, con)
diag = pd.read_sql_query(SQL_DIAG, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
alone = pd.read_sql_query(SQL_ALONE, con)
print("report as written:");               print(bad.to_string(index=False))
print("\ndiagnosis, selecting from the CTE:"); print(diag.to_string(index=False))
print("orders in the table:", con.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
print("\nfix 1, items aggregated to one row per order first:"); print(sql_df.to_string(index=False))
print("\nfix 2, sum from orders alone:");  print(alone.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
items = pd.read_sql_query("SELECT * FROM order_items", con)
# the same bug in pandas
j_bad = orders.merge(items, on="order_id")
pd_bad = j_bad.groupby("customer_id", as_index=False).agg(revenue=("order_total", "sum"))
print("\npandas bug: merged rows =", len(j_bad), "| orders =", len(orders), "| revenue:", pd_bad["revenue"].tolist(), "| customers:", pd_bad["customer_id"].tolist())
try:
    orders.merge(items, on="order_id", validate="one_to_one")
except Exception as e:
    print("validate='one_to_one' raises:", type(e).__name__)
# pd:main
item_totals = items.groupby("order_id", as_index=False).agg(units=("qty", "sum"))
j = orders.merge(item_totals, on="order_id", how="left", validate="one_to_one").fillna({"units": 0})
pd_df = (j.groupby("customer_id", as_index=False)
          .agg(revenue=("order_total", "sum"), units=("units", "sum"))
          .astype({"units": "int64"}).sort_values("customer_id").reset_index(drop=True))
# pd:end
print("\npandas fixed:"); print(pd_df.to_string(index=False))
# compared after sorting both by customer_id
pd.testing.assert_frame_equal(sql_df.sort_values("customer_id").reset_index(drop=True), pd_df, check_dtype=False)
assert diag.loc[0, "n_rows"] == 6 and diag.loc[0, "n_orders"] == 3
assert sql_df["revenue"].tolist() == alone["revenue"].tolist() == [150, 200, 80]
assert bad["revenue"].tolist() == [350, 400]
print("asserts passed: SQL == pandas; revenue ties to the orders table (430)")
```

**Output (my run):**
```text
report as written:
 customer_id  revenue
           1      350
           2      400

diagnosis, selecting from the CTE:
 n_rows  n_orders
      6         3
orders in the table: 4

fix 1, items aggregated to one row per order first:
 customer_id  revenue  units
           1      150      5
           2      200      5
           3       80      0

fix 2, sum from orders alone:
 customer_id  revenue
           1      150
           2      200
           3       80

pandas bug: merged rows = 6 | orders = 4 | revenue: [350, 400] | customers: [1, 2]
validate='one_to_one' raises: MergeError

pandas fixed:
 customer_id  revenue  units
           1      150      5
           2      200      5
           3       80      0
asserts passed: SQL == pandas; revenue ties to the orders table (430)
```

**Edge cases:**
- **Orders without items:** inner join loses them (customer 3 above); use LEFT JOIN, or decide that "orders with items only" is intended and say so.
- **One item per order everywhere:** the bug is invisible in testing, which is how it ships. It appears only when some order has 2 or more items.
- **SUM(DISTINCT order_total):** not a fix, because two orders with the same total collapse into one.
- **Other measure columns:** any column from `orders` summed after the join is multiplied the same way.
- **pandas:** `merge` multiplies in exactly the same way (6 rows in my run). `validate="one_to_one"` between orders and raw items raises `MergeError`; on the fixed merge it passes, because item_totals has one row per order.

**Then explain:**
- **Why the CTE hid it:** the CTE `j` looks like "orders plus an item id", the final query only mentions `order_total`, and nothing in the output shows the row count. Readers trust the name.
- **How to test a CTE:** replace the final SELECT with `SELECT * FROM j` or the count/distinct check, and compare the row count with what you expect at that grain (one row per order). Do this for every CTE in a chain.
- **The rule:** before summing a parent column, make sure the joined result is still one row per parent. Aggregate the many side first.
- **Tie-out check:** compare the total with the same sum computed on `orders` alone (430 here).

**Follow-ups:**
- *What if I need units and revenue in one report?* Fix 1 gives both: revenue from `orders`, units from the aggregated items.
- *What if I only want orders that have items?* Use `WHERE EXISTS (SELECT 1 FROM order_items ...)` instead of a join, which does not multiply rows.
- *Two child tables?* See the chasm-trap question in Part 2 (Q13).

**Common mistakes:**
- Adding DISTINCT to the SUM.
- Not checking row counts between CTE steps.
- Using an inner join and silently dropping orders.
- Testing only the final number against a single order.

### Q17 ⭐⭐ 🟢 Subquery versus CTE versus view versus temporary table: for the same per-customer totals over orders(order_id, customer_id, amount), show each form in SQLite (subquery, CTE, CREATE VIEW, CREATE TEMP TABLE). Compare lifetime, reuse across statements, whether data is stored, indexability, and who sees the result. Explain that whether a CTE is materialised or inlined is engine specific (SQLite and PostgreSQL have MATERIALIZED and NOT MATERIALIZED hints; hedge MySQL and others, not executed) and that readability is the main reason to choose a CTE.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** All four give the same numbers today; they differ in lifetime and reuse: a subquery or CTE lives for one statement, a view is a saved query that re-runs on every use and everyone sees it, a temp table stores a snapshot that only your session sees and can be indexed.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,200),(3,2,50),(4,3,150),(5,3,10);
```

**SQL answer:** the four forms, each run in the Code block (`SQL_SUBQ`, `SQL_MAIN` for the CTE, `SQL_VIEW_DDL` plus `SQL_VIEW`, `SQL_TEMP_DDL` plus `SQL_TEMP`).
```sql
SELECT t.customer_id, t.total FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) t
WHERE t.total > 100 ORDER BY t.customer_id
```
```sql
WITH totals AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
SELECT customer_id, total FROM totals WHERE total > 100 ORDER BY customer_id
```
```sql
CREATE VIEW v_totals AS SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
```
```sql
CREATE TEMP TABLE tmp_totals AS SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
```

**pandas answer:** a function (like a view: recomputed from the current data) versus a saved copy (like a temp table: a snapshot); same text as in the Code block.
```python
def totals(df):
    return df.groupby("customer_id", as_index=False).agg(total=("amount", "sum"))
big = totals(orders).query("total > 100")
pd_df = big.sort_values("customer_id").reset_index(drop=True)
```

**Example:** Totals per customer are 1: 300, 2: 50, 3: 160; "over 100" gives customers 1 and 3 for every form. Then a new order of 500 arrives for customer 2.
- The CTE and the view recompute and now show customer 2 (550).
- The temp table keeps the old totals (customer 2 is still missing).
- A second connection to the same in-memory database sees the view but gets `no such table` for the temp table.

**Code:** run with `python3 -I`.
```python
# Q17: subquery vs CTE vs view vs temporary table for the same per-customer totals
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,200),(3,2,50),(4,3,150),(5,3,10);
"""
SQL_SUBQ = """
SELECT t.customer_id, t.total FROM (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) t
WHERE t.total > 100 ORDER BY t.customer_id
"""
SQL_MAIN = """
WITH totals AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
SELECT customer_id, total FROM totals WHERE total > 100 ORDER BY customer_id
"""
SQL_VIEW_DDL = "CREATE VIEW v_totals AS SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id"
SQL_TEMP_DDL = "CREATE TEMP TABLE tmp_totals AS SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id"
SQL_VIEW = "SELECT customer_id, total FROM v_totals WHERE total > 100 ORDER BY customer_id"
SQL_TEMP = "SELECT customer_id, total FROM tmp_totals WHERE total > 100 ORDER BY customer_id"

URI = "file:q17db?mode=memory&cache=shared"
con = sqlite3.connect(URI, uri=True)
other = sqlite3.connect(URI, uri=True)       # a second session on the same database
con.executescript(SCHEMA)
con.execute(SQL_VIEW_DDL)
con.execute(SQL_TEMP_DDL)
con.commit()
frames = {
    "subquery": pd.read_sql_query(SQL_SUBQ, con),
    "cte": pd.read_sql_query(SQL_MAIN, con),
    "view": pd.read_sql_query(SQL_VIEW, con),
    "temp table": pd.read_sql_query(SQL_TEMP, con),
}
for k, v in frames.items():
    print(f"{k:11s}", v.values.tolist())

print("\nlifetime and reuse")
print("  other session sees the view     :", other.execute("SELECT COUNT(*) FROM v_totals").fetchone()[0], "rows")
try:
    other.execute("SELECT COUNT(*) FROM tmp_totals")
except sqlite3.Error as e:
    print("  other session sees the temp table:", e)
con.execute("INSERT INTO orders VALUES (6,2,500)")
con.commit()
print("  after a new order for customer 2 (500):")
print("    view      :", con.execute(SQL_VIEW).fetchall())
print("    temp table:", con.execute(SQL_TEMP).fetchall(), "(snapshot, stale)")
print("    cte       :", con.execute(SQL_MAIN).fetchall())
print("  stored data: view rows in sqlite_master type:", con.execute("SELECT type FROM sqlite_master WHERE name='v_totals'").fetchone()[0],
      "| temp table type:", con.execute("SELECT type FROM sqlite_temp_master WHERE name='tmp_totals'").fetchone()[0])
con.execute("CREATE INDEX ix_tmp ON tmp_totals(customer_id)")
print("  index on the temp table: created")
try:
    con.execute("CREATE INDEX ix_v ON v_totals(customer_id)")
except sqlite3.Error as e:
    print("  index on the view:", e)

print("\nEXPLAIN QUERY PLAN for a CTE referenced twice (self-join), by hint:")
for label, body in (("filter CTE   ", "SELECT * FROM orders WHERE amount > 10"),
                    ("aggregate CTE", "SELECT customer_id, SUM(amount) AS amount FROM orders GROUP BY customer_id")):
    for hint in ("", "MATERIALIZED", "NOT MATERIALIZED"):
        q = f"WITH t AS {hint} ({body}) SELECT a.amount FROM t a JOIN t b ON a.amount < b.amount"
        plan = [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q)]
        print(f"  {label} {hint or 'default':16s}: materialised={any(p.startswith('MATERIALIZE') for p in plan)}, scans of orders={sum(p == 'SCAN orders' for p in plan)}")
r1 = con.execute("""WITH t AS MATERIALIZED (SELECT 1 AS x) SELECT x FROM t""").fetchall()
r2 = con.execute("""WITH t AS NOT MATERIALIZED (SELECT 1 AS x) SELECT x FROM t""").fetchall()
assert r1 == r2 == [(1,)]

# pandas: the same totals, a variable (CTE-like), a function (view-like), a saved copy (temp-table-like)
con.execute("DELETE FROM orders WHERE order_id = 6"); con.commit()
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
def totals(df):
    return df.groupby("customer_id", as_index=False).agg(total=("amount", "sum"))
big = totals(orders).query("total > 100")
pd_df = big.sort_values("customer_id").reset_index(drop=True)
# pd:end
snapshot = totals(orders)
orders.loc[len(orders)] = [6, 2, 500]
print("\npandas after the same new order: function result", totals(orders).query("total > 100")["customer_id"].tolist(),
      "| snapshot", snapshot.query("total > 100")["customer_id"].tolist())
# compared after sorting by customer_id
base = frames["cte"].sort_values("customer_id").reset_index(drop=True)
for k, v in frames.items():
    pd.testing.assert_frame_equal(v.sort_values("customer_id").reset_index(drop=True), base)
pd.testing.assert_frame_equal(base, pd_df, check_dtype=False)
print("asserts passed: subquery == CTE == view == temp table == pandas")
```

**Output (my run):**
```text
subquery    [[1, 300], [3, 160]]
cte         [[1, 300], [3, 160]]
view        [[1, 300], [3, 160]]
temp table  [[1, 300], [3, 160]]

lifetime and reuse
  other session sees the view     : 3 rows
  other session sees the temp table: no such table: tmp_totals
  after a new order for customer 2 (500):
    view      : [(1, 300), (2, 550), (3, 160)]
    temp table: [(1, 300), (3, 160)] (snapshot, stale)
    cte       : [(1, 300), (2, 550), (3, 160)]
  stored data: view rows in sqlite_master type: view | temp table type: table
  index on the temp table: created
  index on the view: views may not be indexed

EXPLAIN QUERY PLAN for a CTE referenced twice (self-join), by hint:
  filter CTE    default         : materialised=False, scans of orders=2
  filter CTE    MATERIALIZED    : materialised=True, scans of orders=1
  filter CTE    NOT MATERIALIZED: materialised=False, scans of orders=2
  aggregate CTE default         : materialised=True, scans of orders=1
  aggregate CTE MATERIALIZED    : materialised=True, scans of orders=1
  aggregate CTE NOT MATERIALIZED: materialised=True, scans of orders=1

pandas after the same new order: function result [1, 2, 3] | snapshot [1, 3]
asserts passed: subquery == CTE == view == temp table == pandas
```

**Edge cases:**
- **Stale temp table:** the main risk; you must refresh it (drop and recreate, or delete and insert).
- **View on a view on a view:** every layer re-runs. A view is not a cache.
- **Indexing:** SQLite refused an index on the view (`views may not be indexed`) and accepted one on the temp table. Other engines (PostgreSQL materialized views, SQL Server indexed views) behave differently; not executed here.
- **Plain CTE or subquery referenced twice:** whether it runs twice depends on the engine and the query (next section).

**Then explain:**

| | Subquery | CTE | View | Temp table |
|---|---|---|---|---|
| Lifetime | one statement | one statement | until dropped | until the session ends (or dropped) |
| Reuse across statements | no | no | yes | yes |
| Stores data | no | no (may be materialised internally) | no | yes |
| Indexable | no | no | no (in SQLite) | yes |
| Who sees it | nobody else | nobody else | everyone with access to the database | only your connection |

- **Materialised or inlined (SQLite, my run):** for a CTE referenced twice, SQLite inlined a plain filter CTE (two scans of `orders`) but materialised an aggregate CTE (one scan). `AS MATERIALIZED` forced materialisation of the filter CTE, and `AS NOT MATERIALIZED` did not stop SQLite from materialising the aggregate: the hint is not binding. These hints need SQLite 3.35 or later.
- **PostgreSQL and MySQL:** PostgreSQL's documentation (as summarised in Wave A) describes the same hints and says a CTE used once is folded into the parent by default while one used several times is materialised; I did not run PostgreSQL. I am not sure how MySQL 8.4 decides (not executed here). Treat engine behaviour as something to check with the plan, not assume.
- **Why choose a CTE:** readability and the ability to name and reference a step, not speed.
- **When a temp table is justified:** an expensive step reused by many statements, or when you need an index on the intermediate result.

**Follow-ups:**
- *View versus materialized view?* A materialized view stores the result and needs a refresh; SQLite has none, so I did not execute it.
- *Can a view take parameters?* Not in plain SQL; filter outside it.
- *Why is my CTE slow?* Look at the plan: it may be recomputed per reference.

**Common mistakes:**
- Believing a CTE is always cached.
- Using a temp table and forgetting that the data goes stale.
- Creating a view to "speed up" a query.
- Assuming the hints are commands rather than requests.

### Q18 ⭐⭐ 🟢 pandas boolean masks, transform and assign for subquery logic: employees(emp_id, name, dept_id, salary). Reproduce 'earn above the department average' and 'earn above the company average' with a boolean mask, groupby transform('mean') and assign, and with query() using a @variable. Explain why transform returns a result aligned to the original rows (unlike agg), the cost of a lambda versus the built-in 'mean', and that rows with a NaN dept_id get NaN from transform (dropna=True default).
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `groupby(...).transform("mean")` returns one value per original row (the group mean broadcast back), so you can compare a row's salary with its own department average using a plain boolean mask, assign it as a column, or use `query`; `agg` would return one row per group.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',1,100),(2,'Ben',1,80),(3,'Chitra',1,120),
 (4,'Dev',2,50),(5,'Esha',2,60),(6,'Faiz',2,70),
 (7,'Gita',NULL,90),(8,'Hari',NULL,40),
 (9,'Isha',3,NULL),(10,'Jai',3,65);
```

**SQL answer:** the correlated subquery `SQL_DEPT` and the scalar `SQL_MAIN`; both run in the Code block.
```sql
SELECT e.emp_id, e.name FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.emp_id
```
```sql
SELECT emp_id, name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY emp_id
```

**pandas answer:** same text as in the Code block.
```python
dept_avg = emp.groupby("dept_id")["salary"].transform("mean")
above_dept = emp[emp["salary"] > dept_avg]
company_avg = emp["salary"].mean()
above_company = emp[emp["salary"] > company_avg]
q_dept = emp.assign(dept_avg=dept_avg).query("salary > dept_avg").drop(columns="dept_avg")
q_company = emp.query("salary > @company_avg")
```

**Example:** Department 1: 100, 80, 120 (mean 100). Department 2: 50, 60, 70 (mean 60). Department 3: NULL, 65 (mean 65, the NaN is skipped). Department NaN: 90 and 40. Company mean over the nine known salaries: 675 / 9 = 75.
- Above department average: Chitra (120 > 100) and Faiz (70 > 60). Asha (100) is equal, Jai (65 vs 65) is equal, Isha has no salary, and Gita and Hari have no department mean.
- Above the company average (75): Asha 100, Ben 80, Chitra 120, Gita 90.

**Code:** run with `python3 -I`.
```python
# Q18: pandas masks, transform and assign for "above the department / company average"
import sqlite3
import time
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',1,100),(2,'Ben',1,80),(3,'Chitra',1,120),
 (4,'Dev',2,50),(5,'Esha',2,60),(6,'Faiz',2,70),
 (7,'Gita',NULL,90),(8,'Hari',NULL,40),
 (9,'Isha',3,NULL),(10,'Jai',3,65);
"""
SQL_DEPT = """
SELECT e.emp_id, e.name FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.emp_id
"""
SQL_MAIN = """
SELECT emp_id, name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_dept = pd.read_sql_query(SQL_DEPT, con)
sql_co = pd.read_sql_query(SQL_MAIN, con)
emp = pd.read_sql_query("SELECT * FROM employees", con)
print("employees as pandas sees them (dept_id is float because of the NULLs):")
print(emp.dtypes.to_dict())

# pd:main
dept_avg = emp.groupby("dept_id")["salary"].transform("mean")
above_dept = emp[emp["salary"] > dept_avg]
company_avg = emp["salary"].mean()
above_company = emp[emp["salary"] > company_avg]
q_dept = emp.assign(dept_avg=dept_avg).query("salary > dept_avg").drop(columns="dept_avg")
q_company = emp.query("salary > @company_avg")
# pd:end
print("\nper-row department average (aligned to emp):", dept_avg.round(2).tolist())
print("agg result is one row per group:", emp.groupby("dept_id")["salary"].agg("mean").round(2).to_dict())
print("company average:", company_avg)
print("\nabove dept avg   :", above_dept["name"].tolist())
print("above company avg:", above_company["name"].tolist())
print("query() versions equal the mask versions:", q_dept.equals(above_dept), q_company.equals(above_company))
print("\nNaN dept_id rows got transform =", dept_avg[emp["dept_id"].isna()].tolist())
alt = emp.groupby("dept_id", dropna=False)["salary"].transform("mean")
print("with dropna=False the NaN-dept rows form their own group:", alt[emp["dept_id"].isna()].tolist(),
      "-> above dept avg would also include", sorted(set(emp[emp["salary"] > alt]["name"]) - set(above_dept["name"])))

# compared after sorting both by emp_id
pd.testing.assert_frame_equal(sql_dept[["emp_id"]], above_dept[["emp_id"]].sort_values("emp_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(sql_co[["emp_id"]], above_company[["emp_id"]].sort_values("emp_id").reset_index(drop=True), check_dtype=False)
assert q_dept.equals(above_dept) and q_company.equals(above_company)

# built-in 'mean' versus a lambda, on 300,000 rows and 3,000 groups (timings vary by machine)
rng = np.random.default_rng(0)
big = pd.DataFrame({"g": rng.integers(0, 3000, 300_000), "x": rng.normal(100, 15, 300_000)})
t0 = time.perf_counter(); a = big.groupby("g")["x"].transform("mean"); t1 = time.perf_counter()
b = big.groupby("g")["x"].transform(lambda s: s.mean()); t2 = time.perf_counter()
print(f"\ntransform('mean'): {t1 - t0:.4f}s | transform(lambda): {t2 - t1:.4f}s | same values: {np.allclose(a, b)}")
assert np.allclose(a, b)
print("asserts passed: SQL == pandas for both questions; query() == mask")
```

**Output (my run):**
```text
employees as pandas sees them (dept_id is float because of the NULLs):
{'emp_id': dtype('int64'), 'name': <StringDtype(storage='python', na_value=nan)>, 'dept_id': dtype('float64'), 'salary': dtype('float64')}

per-row department average (aligned to emp): [100.0, 100.0, 100.0, 60.0, 60.0, 60.0, nan, nan, 65.0, 65.0]
agg result is one row per group: {1.0: 100.0, 2.0: 60.0, 3.0: 65.0}
company average: 75.0

above dept avg   : ['Chitra', 'Faiz']
above company avg: ['Asha', 'Ben', 'Chitra', 'Gita']
query() versions equal the mask versions: True True

NaN dept_id rows got transform = [nan, nan]
with dropna=False the NaN-dept rows form their own group: [65.0, 65.0] -> above dept avg would also include ['Gita']

transform('mean'): 0.0123s | transform(lambda): 0.2022s | same values: True
asserts passed: SQL == pandas for both questions; query() == mask
```

**Edge cases:**
- **NaN dept_id:** with the default `dropna=True` the NaN-department rows are not in any group, so `transform` returns NaN for them (my run: `[nan, nan]`), `salary > NaN` is False, and they are dropped. The SQL correlated version agrees, because `x.dept_id = NULL` is never true and the average is NULL. The assert in my run checks SQL equals pandas.
- **`dropna=False`:** NaN department rows become their own group (mean 65.0 in my run), and Gita (90) would then be included. That is not the SQL answer.
- **NaN salary (Isha):** compares False; SQL NULL is unknown. Same outcome.
- **dtypes:** the NULLs made `dept_id` and `salary` floats in pandas; `name` came back as pandas's string dtype.
- **Strictly greater:** ties with the mean are excluded.

**Then explain:**
- **transform versus agg:** `agg` collapses to one row per department, so you must merge it back to compare. `transform` keeps the index of the input, so alignment is automatic.
- **Lambda versus built-in:** `transform("mean")` uses the optimised path; `transform(lambda s: s.mean())` calls Python once per group. On 300,000 rows and 3,000 groups my run took 0.0123 seconds against 0.2505 seconds (same values; timings vary by machine). Use the string name whenever one exists.
- **query:** `emp.query("salary > @company_avg")` reads a Python variable with `@`. For the department version the average must exist as a column first (`assign`, then `query`), because `query` has no groupby.
- **Mask versus query:** both returned the same rows (my run: `True True`); the mask is easier to debug, `query` reads like SQL.

**Follow-ups:**
- *Same with median?* `transform("median")`.
- *Why not loop over departments?* Slow and unnecessary.
- *SQL equivalent of transform?* A window function `AVG(salary) OVER (PARTITION BY dept_id)`; see Part 4.

**Common mistakes:**
- Using `agg` and trying to compare it with the original column (shape mismatch).
- Using a lambda where a built-in exists.
- Forgetting that NaN keys are dropped and the rows come back as NaN.
- Writing `query("salary > company_avg")` without the `@`.

### Q19 ⭐⭐ 🟢 CTE chains versus pandas pipelines: translate a three-CTE SQL query (filtered orders, per-customer totals, customers above the overall average of those totals) over orders(order_id, customer_id, order_date, amount) into pandas using named intermediate DataFrames, then into one .pipe() / assign() chain. Explain the mapping of each CTE to a variable or pipe step, the benefit of debugging a single intermediate, and the copy-on-write behaviour of pandas 3 that makes intermediate frames safe to modify.
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Each CTE becomes a named DataFrame (or a function used with `.pipe()`), the final SELECT becomes the last step, and the "average of the totals" CTE becomes a scalar or an `assign` column; debugging means inspecting any one intermediate frame.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2025-01-05',100),(2,1,'2025-02-10',200),(3,1,'2024-12-20',500),
 (4,2,'2025-01-15',60),(5,3,'2025-03-01',150),(6,3,'2025-03-09',50),
 (7,4,'2025-03-11',90),(8,5,'2024-06-01',999);
```

**SQL answer:** `SQL_MAIN` with three CTEs; it runs in the Code block.
```sql
WITH filtered AS (
  SELECT order_id, customer_id, amount FROM orders WHERE order_date >= '2025-01-01'
),
totals AS (
  SELECT customer_id, SUM(amount) AS total FROM filtered GROUP BY customer_id
),
overall AS (
  SELECT AVG(total) AS avg_total FROM totals
)
SELECT t.customer_id, t.total
FROM totals t CROSS JOIN overall o
WHERE t.total > o.avg_total
ORDER BY t.customer_id
```

**pandas answer:** the pipeline form (same text as in the Code block). The Code block also builds the named-variable form, one variable per CTE (`filtered`, `totals`, `overall`).
```python
def filter_orders(df, since):
    return df.loc[df["order_date"] >= since, ["order_id", "customer_id", "amount"]]

def customer_totals(df):
    return df.groupby("customer_id", as_index=False).agg(total=("amount", "sum"))

pd_df = (orders
         .pipe(filter_orders, "2025-01-01")
         .pipe(customer_totals)
         .assign(avg_total=lambda d: d["total"].mean())
         .query("total > avg_total")
         .drop(columns="avg_total")
         .sort_values("customer_id").reset_index(drop=True))
```

**Example:** Orders dated on or after 2025-01-01 (six of the eight rows pass the filter).
- `filtered`: orders 1, 2, 4, 5, 6, 7 (order 3 is from 2024-12-20 and order 8 from 2024-06-01).
- `totals`: customer 1 = 100 + 200 = 300, customer 2 = 60, customer 3 = 150 + 50 = 200, customer 4 = 90.
- `overall`: (300 + 60 + 200 + 90) / 4 = 162.5.
- Result: customers 1 (300) and 3 (200). My run printed the intermediates and the result.

**Code:** run with `python3 -I`.
```python
# Q19: three chained CTEs versus a pandas pipeline
import sqlite3
import warnings
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2025-01-05',100),(2,1,'2025-02-10',200),(3,1,'2024-12-20',500),
 (4,2,'2025-01-15',60),(5,3,'2025-03-01',150),(6,3,'2025-03-09',50),
 (7,4,'2025-03-11',90),(8,5,'2024-06-01',999);
"""
SQL_MAIN = """
WITH filtered AS (
  SELECT order_id, customer_id, amount FROM orders WHERE order_date >= '2025-01-01'
),
totals AS (
  SELECT customer_id, SUM(amount) AS total FROM filtered GROUP BY customer_id
),
overall AS (
  SELECT AVG(total) AS avg_total FROM totals
)
SELECT t.customer_id, t.total
FROM totals t CROSS JOIN overall o
WHERE t.total > o.avg_total
ORDER BY t.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))
orders = pd.read_sql_query("SELECT * FROM orders", con)

# version 1: one variable per CTE
since = "2025-01-01"
filtered = orders.loc[orders["order_date"] >= since, ["order_id", "customer_id", "amount"]]
totals = filtered.groupby("customer_id", as_index=False).agg(total=("amount", "sum"))
overall = totals["total"].mean()
v1 = totals[totals["total"] > overall].sort_values("customer_id").reset_index(drop=True)
print("\nintermediates: filtered rows =", len(filtered), "| totals =", totals["total"].tolist(), "| overall average =", overall)

# pd:main
def filter_orders(df, since):
    return df.loc[df["order_date"] >= since, ["order_id", "customer_id", "amount"]]

def customer_totals(df):
    return df.groupby("customer_id", as_index=False).agg(total=("amount", "sum"))

pd_df = (orders
         .pipe(filter_orders, "2025-01-01")
         .pipe(customer_totals)
         .assign(avg_total=lambda d: d["total"].mean())
         .query("total > avg_total")
         .drop(columns="avg_total")
         .sort_values("customer_id").reset_index(drop=True))
# pd:end
print("\npipeline result:"); print(pd_df.to_string(index=False))

# copy-on-write in pandas 3: changing a derived object never changes its parent
before = orders["amount"].tolist()
sub = orders[orders["customer_id"] == 1]
sub.loc[sub.index[0], "amount"] = -1
col = orders["amount"]
col.iloc[0] = -2
print("\nparent unchanged after editing a filtered frame and a column:", orders["amount"].tolist() == before)
# chained assignment is also a no-op now
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    orders[orders["customer_id"] == 2]["amount"] = 0
print("chained assignment orders[mask]['amount'] = 0 changed the parent:", orders["amount"].tolist() != before,
      "| warning raised:", [w.category.__name__ for w in caught])

# compared after sorting both by customer_id
pd.testing.assert_frame_equal(sql_df, v1, check_dtype=False)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert orders["amount"].tolist() == before
print("asserts passed: SQL == named variables == pipe/assign chain")
```

**Output (my run):**
```text
SQL:
 customer_id  total
           1    300
           3    200

intermediates: filtered rows = 6 | totals = [300, 60, 200, 90] | overall average = 162.5

pipeline result:
 customer_id  total
           1    300
           3    200

parent unchanged after editing a filtered frame and a column: True
chained assignment orders[mask]['amount'] = 0 changed the parent: False | warning raised: ['ChainedAssignmentError']
asserts passed: SQL == named variables == pipe/assign chain
```

**Edge cases:**
- **Empty filtered frame:** `totals` is empty and the mean is NaN; the comparison is False for every row, so the result is empty, the same as SQL (AVG of nothing is NULL). I did not run the empty case.
- **Strict `>`:** customers exactly at the average are excluded.
- **`assign` with a lambda:** the lambda sees the frame at that step, so `d["total"].mean()` is computed over the filtered totals, as the CTE does; if you used the original frame by mistake the average would change.
- **Column order and names:** pandas does not enforce the CTE's column list; I selected columns in `filter_orders` to mirror it.

**Then explain:**
- **Mapping:** `filtered` is `orders.loc[...]`, `totals` is `groupby().agg()`, `overall` is `totals["total"].mean()` (or an assign column), and the final SELECT is the mask or `query`. `.pipe(func, arg)` calls `func(df, arg)` and keeps the chain readable.
- **Debugging:** with named variables you can print `totals`; with a pipe you break the chain at any step (`orders.pipe(filter_orders, ...)` alone). In SQL you replace the final SELECT. Either way you look at one step at a time.
- **Copy-on-write (pandas 3):** a frame or column derived from another behaves as a copy, so changing it never changes the parent. My run edited a filtered frame and a column and the parent `orders["amount"]` was unchanged. A chained assignment such as `orders[mask]["amount"] = 0` also does not update the parent, and pandas 3 raised `ChainedAssignmentError` as a warning (captured in my run). This is why intermediates are safe to modify. It does not remove the memory cost of large intermediates: the copy happens only when you write.
- **Named variables versus one chain:** variables are easier to inspect, a chain avoids a pile of names. Pick the one that debugs better.

**Follow-ups:**
- *Is a pipe faster than variables?* No, it is only style.
- *How would the third CTE look with a window function?* `AVG(total) OVER ()`; see Part 4.
- *How do I log each step's row count?* Add a `pipe` step that prints `len(df)` and returns the frame.

**Common mistakes:**
- Mutating an intermediate and expecting the parent to change (or fearing it will).
- Using chained assignment.
- Computing the overall average from the unfiltered frame.
- Long unreadable one-liners instead of named steps.

### Q20 ⭐⭐ 🟢 INSERT ... SELECT: tables orders(order_id, customer_id, order_date, amount) and orders_archive with the same columns. Archive orders older than 2024-01-01 with INSERT INTO orders_archive (column list) SELECT ..., then delete them in a way that cannot lose rows. Explain why you name the columns, what happens if the archive already holds some ids (primary-key conflict) and how to skip them with NOT EXISTS, and the pandas parallel (concat of a filtered frame). Note the transaction and the dialect points (hedged, not executed).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** In one transaction, `INSERT INTO orders_archive (columns) SELECT ... WHERE order_date < '2024-01-01' AND NOT EXISTS (already archived)`, then `DELETE` only the old orders that now have an identical archived copy, so a failure can only roll the whole thing back and never lose a row.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
CREATE TABLE orders_archive(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2023-03-01',100),(2,2,'2023-07-15',250),(3,1,'2023-12-31',75),
 (4,3,'2024-01-01',60),(5,2,'2023-05-05',40),(6,4,'2025-02-02',500);
INSERT INTO orders_archive VALUES (1,1,'2023-03-01',100),(5,2,'2023-05-05',45);
```

**SQL answer:** `SQL_INSERT` then `SQL_DELETE`, inside `BEGIN ... COMMIT`; both run in the Code block.
```sql
INSERT INTO orders_archive (order_id, customer_id, order_date, amount)
SELECT o.order_id, o.customer_id, o.order_date, o.amount
FROM orders o
WHERE o.order_date < '2024-01-01'
  AND NOT EXISTS (SELECT 1 FROM orders_archive a WHERE a.order_id = o.order_id)
```
```sql
DELETE FROM orders
WHERE order_date < '2024-01-01'
  AND EXISTS (SELECT 1 FROM orders_archive a
              WHERE a.order_id = orders.order_id
                AND a.customer_id IS orders.customer_id
                AND a.order_date  IS orders.order_date
                AND a.amount      IS orders.amount)
```

**pandas answer:** filter, drop ids already archived, concat, then keep in `orders` everything that is not safely archived (same text as in the Code block).
```python
old = orders[orders["order_date"] < "2024-01-01"]
to_archive = old[~old["order_id"].isin(archive["order_id"])]
archive_new = pd.concat([archive, to_archive], ignore_index=True)
cols = ["order_id", "customer_id", "order_date", "amount"]
marked = old.merge(archive_new[cols], on=cols, how="left", indicator=True)
safe_ids = marked.loc[marked["_merge"] == "both", "order_id"]
orders_new = orders[~orders["order_id"].isin(safe_ids)]
```

**Example:** Orders 1, 2, 3 and 5 are older than 2024-01-01; order 4 (2024-01-01 exactly) and order 6 stay. The archive already holds order 1 (identical) and order 5 (amount 45, but the order says 40).
- INSERT: order 1 is already archived, order 5 is already archived (same id), so only orders 2 and 3 are inserted (my run: 2 rows).
- DELETE: orders 1, 2 and 3 have an identical archived copy, so they are deleted (3 rows). Order 5's archived copy differs (45 vs 40), so it is not deleted: it stays in `orders` for someone to reconcile.
- Result: orders left 4, 5, 6; archive 1, 2, 3, 5. Running both statements again does nothing (0 and 0).

**Code:** run with `python3 -I`.
```python
# Q20: archive old orders with INSERT ... SELECT, then delete only what is safely archived
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
CREATE TABLE orders_archive(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2023-03-01',100),(2,2,'2023-07-15',250),(3,1,'2023-12-31',75),
 (4,3,'2024-01-01',60),(5,2,'2023-05-05',40),(6,4,'2025-02-02',500);
INSERT INTO orders_archive VALUES (1,1,'2023-03-01',100),(5,2,'2023-05-05',45);
"""
SQL_INSERT = """
INSERT INTO orders_archive (order_id, customer_id, order_date, amount)
SELECT o.order_id, o.customer_id, o.order_date, o.amount
FROM orders o
WHERE o.order_date < '2024-01-01'
  AND NOT EXISTS (SELECT 1 FROM orders_archive a WHERE a.order_id = o.order_id)
"""
SQL_DELETE = """
DELETE FROM orders
WHERE order_date < '2024-01-01'
  AND EXISTS (SELECT 1 FROM orders_archive a
              WHERE a.order_id = orders.order_id
                AND a.customer_id IS orders.customer_id
                AND a.order_date  IS orders.order_date
                AND a.amount      IS orders.amount)
"""
def table(con, name):
    return pd.read_sql_query(f"SELECT * FROM {name} ORDER BY order_id", con)

con = sqlite3.connect(":memory:", isolation_level=None)   # explicit BEGIN / COMMIT
con.executescript(SCHEMA)

# 1. the plain INSERT ... SELECT collides with ids already archived
con.execute("BEGIN")
try:
    con.execute("""INSERT INTO orders_archive (order_id, customer_id, order_date, amount)
                   SELECT order_id, customer_id, order_date, amount FROM orders WHERE order_date < '2024-01-01'""")
except sqlite3.IntegrityError as e:
    print("plain INSERT ... SELECT ->", e)
con.execute("ROLLBACK")
print("archive after the failed statement (unchanged):", table(con, "orders_archive")["order_id"].tolist())

# 2. column order matters when you do not name the columns
con.execute("CREATE TABLE swapped(customer_id INTEGER, order_id INTEGER, order_date TEXT, amount INTEGER)")
con.execute("INSERT INTO swapped SELECT * FROM orders WHERE order_id = 3")
print("INSERT ... SELECT * into a table with other column order:", con.execute("SELECT * FROM swapped").fetchall(), "(order 3 of customer 1 is now stored as customer 3, order 1)")

# 3. the safe version, in one transaction
con.execute("BEGIN")
con.execute(SQL_INSERT)
inserted = con.execute("SELECT changes()").fetchone()[0]
con.execute(SQL_DELETE)
deleted = con.execute("SELECT changes()").fetchone()[0]
con.execute("COMMIT")
print(f"\ninserted {inserted} rows, deleted {deleted} rows")
orders_after, arch_after = table(con, "orders"), table(con, "orders_archive")
print("orders left:", orders_after["order_id"].tolist(), "| archive:", arch_after["order_id"].tolist())
print("archive row 5 amount (stale copy kept, not overwritten):", arch_after.loc[arch_after.order_id == 5, "amount"].tolist())
print("run it again (idempotent): inserted", con.execute(SQL_INSERT).rowcount, "rows, deleted", con.execute(SQL_DELETE).rowcount)

# 4. ON CONFLICT DO NOTHING, the other way to skip duplicates (SQLite needs WHERE true after a SELECT)
con.execute("CREATE TABLE arc2(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER)")
con.execute("INSERT INTO arc2 VALUES (1,1,'2023-03-01',100)")
con.execute("""INSERT INTO arc2 (order_id, customer_id, order_date, amount)
               SELECT order_id, customer_id, order_date, amount FROM orders_archive WHERE order_id >= 1
               ON CONFLICT (order_id) DO NOTHING""")
print("ON CONFLICT DO NOTHING keeps:", con.execute("SELECT order_id FROM arc2 ORDER BY 1").fetchall())

# pandas, from the original data
con2 = sqlite3.connect(":memory:")
con2.executescript(SCHEMA)
orders = table(con2, "orders")
archive = table(con2, "orders_archive")
# pd:main
old = orders[orders["order_date"] < "2024-01-01"]
to_archive = old[~old["order_id"].isin(archive["order_id"])]
archive_new = pd.concat([archive, to_archive], ignore_index=True)
cols = ["order_id", "customer_id", "order_date", "amount"]
marked = old.merge(archive_new[cols], on=cols, how="left", indicator=True)
safe_ids = marked.loc[marked["_merge"] == "both", "order_id"]
orders_new = orders[~orders["order_id"].isin(safe_ids)]
# pd:end
print("\npandas: archive", sorted(archive_new["order_id"]), "| orders left", orders_new["order_id"].tolist())
# compared after sorting both tables by order_id
pd.testing.assert_frame_equal(arch_after, archive_new.sort_values("order_id").reset_index(drop=True))
pd.testing.assert_frame_equal(orders_after, orders_new.sort_values("order_id").reset_index(drop=True))
assert len(orders) + len(archive) - 1 == len(orders_new) + len(archive_new)   # row 1 was in both; no row lost
print("asserts passed: SQL == pandas; every order is in orders or the archive")
```

**Output (my run):**
```text
plain INSERT ... SELECT -> UNIQUE constraint failed: orders_archive.order_id
archive after the failed statement (unchanged): [1, 5]
INSERT ... SELECT * into a table with other column order: [(3, 1, '2023-12-31', 75)] (order 3 of customer 1 is now stored as customer 3, order 1)

inserted 2 rows, deleted 3 rows
orders left: [4, 5, 6] | archive: [1, 2, 3, 5]
archive row 5 amount (stale copy kept, not overwritten): [45]
run it again (idempotent): inserted 0 rows, deleted 0
ON CONFLICT DO NOTHING keeps: [(1,), (2,), (3,), (5,)]

pandas: archive [1, 2, 3, 5] | orders left [4, 5, 6]
asserts passed: SQL == pandas; every order is in orders or the archive
```

**Edge cases:**
- **Primary-key conflict:** a plain `INSERT ... SELECT` fails with `UNIQUE constraint failed` on the first duplicate id and the whole statement is rolled back (archive unchanged in my run). `NOT EXISTS` on the key skips the already archived ids. SQLite also has `INSERT OR IGNORE` and `ON CONFLICT DO NOTHING` (the latter ran in my SQLite 3.45 run; with a SELECT source SQLite wants a WHERE clause before ON CONFLICT). Both skip a conflicting row without checking whether the contents match. Whether other engines have the same spelling is not executed here: PostgreSQL has `ON CONFLICT DO NOTHING`, MySQL has `INSERT IGNORE`, from memory.
- **Stale archived copy (order 5):** skipped by the insert and kept by the delete, as designed; a plain `DELETE ... WHERE order_date < ...` would have lost the 40.
- **NULL columns:** I compare with `IS` (SQLite's null-safe equality) so a NULL amount matches a NULL amount; standard SQL spells this `IS NOT DISTINCT FROM`. With `=` a NULL would never match and the order would never be deleted (kept, not lost). Not executed outside SQLite.
- **Boundary:** `< '2024-01-01'` excludes 2024-01-01 itself (order 4). Compare dates as ISO strings or real date types, not mixed formats.
- **Column order:** `INSERT ... SELECT *` into a table with a different column order stored order 3 as customer 3, order 1 (my run) with no error, because both columns are integers. Naming the columns on both sides prevents that and keeps working when someone adds a column.

**Then explain:**
- **Why name the columns:** the INSERT maps by position when no list is given, so a reordered or extended table silently puts values in the wrong columns, or fails.
- **Cannot lose rows:** (1) one transaction, so a failure between INSERT and DELETE rolls both back; (2) DELETE only rows that exist in the archive with identical contents; (3) the operation is repeatable. In Python's sqlite3 I used `isolation_level=None` and an explicit `BEGIN` so the transaction was clear.
- **Other engines (not executed here):** PostgreSQL and others can do the move in one statement with a data-modifying CTE or `DELETE ... RETURNING` feeding the INSERT; SQLite has `RETURNING` from 3.35 but I did not run it here. Large archives are usually done in batches to keep locks and the log small.
- **pandas parallel:** `pd.concat([archive, to_archive])` plus a mask for the remaining orders. There is no transaction in pandas: write the archive first, then the new `orders`, and keep the old copy until both succeeded. My run asserts that the final tables equal the SQL result.

**Follow-ups:**
- *Why not just DELETE after INSERT without checking?* If the insert silently skipped a row (conflict or stale copy), the delete would destroy the only good copy.
- *What if the table is huge?* Archive and delete in batches of ids; I did not run that.
- *How would I verify afterwards?* Count `orders` plus archive before and after (my assert does this in pandas).

**Common mistakes:**
- `INSERT ... SELECT *` with no column list.
- Deleting by date alone after an insert that may have skipped rows.
- Running INSERT and DELETE in separate autocommit statements.
- `INSERT OR IGNORE` hiding a stale or different row.
- Comparing NULL columns with `=`.

### Q21 ⭐⭐ 🟡 Translating IN and NOT IN subqueries to pandas: customers(customer_id, name, city) and orders(order_id, customer_id, amount) with some NaN customer_id in orders. Write 'customers with total spend over 500' using an aggregated frame, then isin on its index, then map of the aggregated Series onto customers, then a merge. Show what isin does with NaN (NaN matches NaN) versus SQL IN, and why ~isin has no NOT IN trap. State which form keeps customers without orders.
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `IN (subquery)` becomes `customers[customers.customer_id.isin(...)]` on an aggregated Series' index, `map` gives you the total as a column, and a left merge does the same with a join; pandas `isin` treats NaN as equal to NaN while SQL `IN` never matches NULL, and `~isin` is a plain boolean flip, so it has no NOT IN trap.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Goa');
INSERT INTO orders VALUES (1,1,300),(2,1,250),(3,2,200),(4,2,100),(5,NULL,900),(6,3,50);
```
The NULL customer_id order (900) is the trap: it makes a NULL group that is bigger than 500.

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT customer_id, name, city
FROM customers
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      HAVING SUM(amount) > 500)
ORDER BY customer_id
```
The anti-join twins, `SQL_NOT_IN` and `SQL_NOT_EXISTS`, are in the Code block too.
```sql
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id
                          FROM orders
                          GROUP BY customer_id
                          HAVING SUM(amount) > 500)
ORDER BY customer_id
```
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1
                  FROM orders o
                  WHERE o.customer_id = c.customer_id
                  GROUP BY o.customer_id
                  HAVING SUM(o.amount) > 500)
ORDER BY c.customer_id
```

**pandas answer:** three forms of the same subquery, all inside `# pd:main` in the Code block.
```python
agg = orders.groupby("customer_id")["amount"].sum()          # NaN group dropped (dropna=True default)
big = agg[agg > 500]
form_isin = customers[customers["customer_id"].isin(big.index)]
form_map = (customers.assign(total=customers["customer_id"].map(agg))
            .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
form_merge = (customers.merge(agg.rename("total").reset_index(), on="customer_id", how="left")
              .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
```
`agg` plays the role of the subquery: one row per customer, indexed by `customer_id`. The `isin` form is the direct translation of `IN`. The `map` form looks up each customer's total (NaN if none). The merge form joins the same Series back as a column.

**Example:**
- Group totals from the orders table: Asha 300 + 250 = 550, Ben 200 + 100 = 300, Chitra 50, and the NULL-id order 900 forms its own group.
- `HAVING SUM(amount) > 500` keeps Asha (550) and the NULL group (900). The subquery returns the list (1, NULL).
- `customer_id IN (1, NULL)`: Asha matches 1, so true. Ben gives `2 = 1` false and `2 = NULL` unknown, so the result is unknown, which WHERE treats as not true. Result: Asha only.
- pandas: `groupby("customer_id")` silently drops the NaN key, so `agg` has Asha 550, Ben 300, Chitra 50. `big` is Asha only. All three forms return Asha.
- Flip it to NOT IN: the list is (1, NULL), and `2 NOT IN (1, NULL)` is `2 <> 1 AND 2 <> NULL`, true AND unknown = unknown. Every customer is unknown or false, so SQL returns zero rows. pandas `~isin([1])` returns Ben, Chitra and Dev.

**Code:** run with `python3 -I`.
```python
# Q21: IN / NOT IN subqueries translated to pandas (isin, map, merge), with NaN customer_id in orders
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Goa');
INSERT INTO orders VALUES (1,1,300),(2,1,250),(3,2,200),(4,2,100),(5,NULL,900),(6,3,50);
"""
SQL_MAIN = """
SELECT customer_id, name, city
FROM customers
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      HAVING SUM(amount) > 500)
ORDER BY customer_id
"""
SQL_NOT_IN = """
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id
                          FROM orders
                          GROUP BY customer_id
                          HAVING SUM(amount) > 500)
ORDER BY customer_id
"""
SQL_NOT_EXISTS = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1
                  FROM orders o
                  WHERE o.customer_id = c.customer_id
                  GROUP BY o.customer_id
                  HAVING SUM(o.amount) > 500)
ORDER BY c.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("orders customer_id dtype in pandas:", orders["customer_id"].dtype, "| NaN count:", int(orders["customer_id"].isna().sum()))

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nSQL IN subquery (customers with total spend > 500):")
print(sql_df.to_string(index=False))
print("SQL group totals incl. the NULL group:", con.execute(
    "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id ORDER BY customer_id").fetchall())

# pd:main
agg = orders.groupby("customer_id")["amount"].sum()          # NaN group dropped (dropna=True default)
big = agg[agg > 500]
form_isin = customers[customers["customer_id"].isin(big.index)]
form_map = (customers.assign(total=customers["customer_id"].map(agg))
            .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
form_merge = (customers.merge(agg.rename("total").reset_index(), on="customer_id", how="left")
              .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
# pd:end
for label, f in [("isin", form_isin), ("map", form_map), ("merge(left)", form_merge)]:
    f = f.sort_values("customer_id").reset_index(drop=True)
    pd.testing.assert_frame_equal(sql_df, f, check_dtype=False)
    print(f"pandas form {label}: rows {f['customer_id'].tolist()} == SQL")

print("\nWhich form keeps customers without orders (before filtering)?")
print("  isin: only filters customers, it produces no total column")
print("  map keeps every customer, total is NaN for Dev:", customers.assign(total=customers["customer_id"].map(agg))["total"].tolist())
print("  merge how='left' rows:", len(customers.merge(agg.rename('total').reset_index(), on='customer_id', how='left')),
      "| how='inner' rows:", len(customers.merge(agg.rename('total').reset_index(), on='customer_id', how='inner')))

print("\nNaN handling:")
s = pd.Series([1.0, np.nan, 3.0])
print("  pandas  s.isin([nan]) ->", s.isin([np.nan]).tolist(), "  (NaN matches NaN)")
print("  SQLite  NULL IN (NULL)         ->", con.execute("SELECT NULL IN (NULL)").fetchone()[0])
print("  SQLite  1 NOT IN (2, NULL)     ->", con.execute("SELECT 1 NOT IN (2, NULL)").fetchone()[0])
print("  pandas  ~isin([2, nan]) on [1,nan,3] ->", (~s.isin([2.0, np.nan])).tolist())

print("  empty list: pandas ~isin([]) ->", (~s.isin([])).tolist(), "| SQLite 1 NOT IN (SELECT 1 WHERE 0) ->", con.execute("SELECT 1 NOT IN (SELECT 1 WHERE 0)").fetchone()[0])

not_in = pd.read_sql_query(SQL_NOT_IN, con)
not_ex = pd.read_sql_query(SQL_NOT_EXISTS, con)
print("\nSQL NOT IN over a list that contains the NULL group, rows:", len(not_in))
print("SQL NOT EXISTS, ids:", not_ex["customer_id"].tolist())
pd_not = customers[~customers["customer_id"].isin(big.index)]
print("pandas ~isin, ids:", pd_not["customer_id"].tolist())
# the SQL list was (1, NULL); the pandas list is [1] because groupby dropped NaN, so give pandas the NULL too:
big_with_nan = orders.groupby("customer_id", dropna=False)["amount"].sum()
big_with_nan = big_with_nan[big_with_nan > 500]
print("pandas groupby(dropna=False) list:", big_with_nan.index.tolist(),
      "-> ~isin ids:", customers[~customers["customer_id"].isin(big_with_nan.index)]["customer_id"].tolist())
assert len(not_in) == 0
assert not_ex["customer_id"].tolist() == pd_not["customer_id"].tolist() == [2, 3, 4]
print("\nasserts passed: SQL IN == pandas isin == map == merge (compared after sorting by customer_id)")
```

**Output (my run):**
```text
orders customer_id dtype in pandas: float64 | NaN count: 1

SQL IN subquery (customers with total spend > 500):
 customer_id name city
           1 Asha Pune
SQL group totals incl. the NULL group: [(None, 900), (1, 550), (2, 300), (3, 50)]
pandas form isin: rows [1] == SQL
pandas form map: rows [1] == SQL
pandas form merge(left): rows [1] == SQL

Which form keeps customers without orders (before filtering)?
  isin: only filters customers, it produces no total column
  map keeps every customer, total is NaN for Dev: [550.0, 300.0, 50.0, nan]
  merge how='left' rows: 4 | how='inner' rows: 3

NaN handling:
  pandas  s.isin([nan]) -> [False, True, False]   (NaN matches NaN)
  SQLite  NULL IN (NULL)         -> None
  SQLite  1 NOT IN (2, NULL)     -> None
  pandas  ~isin([2, nan]) on [1,nan,3] -> [True, False, True]
  empty list: pandas ~isin([]) -> [True, True, True] | SQLite 1 NOT IN (SELECT 1 WHERE 0) -> 1

SQL NOT IN over a list that contains the NULL group, rows: 0
SQL NOT EXISTS, ids: [2, 3, 4]
pandas ~isin, ids: [2, 3, 4]
pandas groupby(dropna=False) list: [1.0, nan] -> ~isin ids: [2, 3, 4]

asserts passed: SQL IN == pandas isin == map == merge (compared after sorting by customer_id)
```

**Edge cases:**
- **Which form keeps customers without orders:** `isin` returns a filtered copy of `customers`, so a customer with no orders is simply "not in the list" and dropped by a positive filter. `map` and a `how="left"` merge keep Dev with a NaN total (the printed list shows `nan` for Dev); filtering `total > 500` then drops him because NaN > 500 is False. A `how="inner"` merge drops Dev (3 rows in my run), which is the same hidden loss as an INNER JOIN in SQL.
- **NaN customer_id in orders:** the column becomes `float64` in pandas (1 NaN in my run), so customer ids come back as 1.0, 2.0. `groupby` drops NaN keys by default; `groupby(..., dropna=False)` keeps them (my run shows the index `[1.0, nan]`).
- **isin and NaN:** `Series([1.0, nan, 3.0]).isin([nan])` is `[False, True, False]` in my run. NaN matches NaN. SQL `NULL IN (NULL)` is NULL (it printed `None`).
- **`~isin` has no NOT IN trap:** `~Series([1, nan, 3]).isin([2, nan])` gave `[True, False, True]`. A NaN in the list only removes NaN values; it does not wipe out the whole result. The SQL equivalent, `1 NOT IN (2, NULL)`, printed `None` (unknown).
- **A NaN in the pandas list is not what changes the answer here:** I also ran `groupby(dropna=False)` so the list was `[1.0, nan]`, and `~isin` still returned ids 2, 3, 4 while SQL `NOT IN` returned zero rows.
- **Empty list:** `~isin([])` is all True in pandas, and SQLite `1 NOT IN (empty subquery)` is 1 (true), both printed in my run. An empty list is the one case where SQL NOT IN is safe.

**Then explain:**
- **Subquery as a Series:** the aggregated Series is the "subquery result". Its index is the list of ids, its values are the totals. Filtering the Series (`agg > 500`) is the `HAVING`.
- **Three forms:** `isin` for a yes/no filter (semi-join), `map` when you also need the value as a column, `merge` when you need several columns from the other side or a left/inner choice. `merge(..., validate="many_to_one")` raises if the right side has duplicate keys.
- **NOT IN in pandas:** use `~isin`, or a left merge with `indicator=True` and keep `left_only` (the anti-join). Neither can return nothing because of one missing value.
- **Where pandas differs from SQL:** NaN matches NaN in `isin` and in `merge` keys, while SQL NULL matches nothing. The pandas documentation's SQL comparison page notes that null merge keys match each other.
- In SQL, use `NOT EXISTS` (or filter NULLs inside the subquery) for the anti-join. In my run `NOT EXISTS` returned ids 2, 3, 4.
- Joins and how they differ from subqueries are in Part 2; window-function versions are in Parts 4 and 5.

**Follow-ups:**
- *Why did `groupby` hide the NULL group?* `dropna=True` is the default for group keys, so NaN keys vanish. That helped here, but if the NaN rows matter you must say `dropna=False`.
- *How do I make pandas behave like SQL on NaN?* Drop or mask NaN before `isin` or `merge`, for example `orders.dropna(subset=["customer_id"])`.
- *What about `isin` on a nullable `Int64` column?* I did not run it, so I will not claim how it treats `pd.NA`; test before relying on it.
- *Which engines have the same NOT IN trap?* The NULL rule is standard three-valued logic and the PostgreSQL documentation describes the same NOT IN behaviour, but I only ran SQLite here; other engines are not executed.

**Common mistakes:**
- Using `NOT IN (subquery)` on a nullable column and getting an empty result.
- Assuming `isin` follows SQL rules for NaN.
- Using an inner merge and losing the customers with no orders.
- Forgetting that the NaN-key rows were dropped by `groupby` and then reconciling totals against the orders table (900 is missing from the pandas side).

### Q22 ⭐⭐ 🟡 ANY, SOME and ALL when the engine lacks them (SQLite has none; PostgreSQL and MySQL do): products(product_id, name, category, price). Write 'price greater than ALL prices in Books' and 'price greater than ANY price in Books' as the native syntax (hedged text, not executed) and as the runnable equivalents (> MAX(...), > MIN(...), or NOT EXISTS / EXISTS). Explain what each does when the Books subquery is empty and when it contains NULL prices, and that = ANY is IN and <> ALL is NOT IN.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `> ALL (subquery)` means greater than every value, so it is `> MAX(...)` only when the subquery has no NULLs and is not empty, and `> ANY` means greater than at least one value, which is `> MIN(...)`; SQLite has neither keyword, so I use the MAX/MIN form with care or the `NOT EXISTS` / `EXISTS` form, which is exact.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Atlas','Books',10),(2,'Novel','Books',20),(3,'Cookbook','Books',30),
 (4,'Digest','Mags',15),(5,'Zine','Mags',NULL),
 (6,'Pen','Stationery',5),(7,'Lamp','Home',25),(8,'Chair','Home',40),(9,'Desk','Home',35),
 (10,'Bag','Travel',NULL);
```
Three subqueries to test: Books (clean prices 10, 20, 30), Mags (prices 15 and NULL) and Toys (no such category, so an empty subquery).

**SQL answer:** the native syntax is below; it is hedged text, not executed on SQLite (the Code block shows what SQLite does with it). The runnable forms are in the Code block.
```sql
-- native, PostgreSQL and MySQL (not executed here)
SELECT name FROM products WHERE price > ALL (SELECT price FROM products WHERE category = 'Books');
SELECT name FROM products WHERE price > ANY (SELECT price FROM products WHERE category = 'Books');
```
Runnable equivalents, `?` is the category:
```sql
SELECT product_id FROM products
WHERE price > (SELECT MAX(price) FROM products WHERE category = ?)
ORDER BY product_id
```
```sql
SELECT p.product_id FROM products p
WHERE NOT EXISTS (SELECT 1 FROM products b
                  WHERE b.category = ?
                    AND NOT COALESCE(p.price > b.price, 0))
ORDER BY p.product_id
```
```sql
SELECT product_id FROM products
WHERE price > (SELECT MIN(price) FROM products WHERE category = ?)
ORDER BY product_id
```
```sql
SELECT p.product_id FROM products p
WHERE EXISTS (SELECT 1 FROM products b
              WHERE b.category = ?
                AND p.price > b.price)
ORDER BY p.product_id
```

**pandas answer:** compare each price with every value of the subquery as a 2-D boolean array, then `.all` or `.any` across the subquery axis. NaN comparisons are False, which is exactly SQL's "not true".
```python
def pd_all(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]   # NaN compares False
    return df.loc[cmp.all(axis=1), "product_id"].tolist()            # all() of an empty row is True

def pd_any(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]
    return df.loc[cmp.any(axis=1), "product_id"].tolist()            # any() of an empty row is False
```

**Example:** Books prices are 10, 20, 30.
- `price > ALL`: the price must beat 30. Chair (40) and Desk (35) do. Lamp (25) does not. Result ids 8 and 9. `price > MAX(...)` gives the same.
- `price > ANY`: the price must beat at least one value, so beating 10 is enough. Novel 20, Cookbook 30, Digest 15, Lamp, Chair and Desk qualify (ids 2, 3, 4, 7, 8, 9). Atlas (10) does not beat itself, Pen (5) does not.
- Mags prices are 15 and NULL. `price > ALL (15, NULL)`: the NULL comparison is unknown for every row, so no row can be true. The `NOT EXISTS` form returns nothing. `> MAX(...)` ignores the NULL, uses 15, and returns five rows (ids 2, 3, 7, 8, 9). That is a different answer from the native syntax.
- Toys is empty. `> ALL (empty)` is true for every row, even rows with a NULL price (all ten products). `> MAX(empty)` is `> NULL`, unknown for all, so zero rows. `> ANY (empty)` is false for every row, and `> MIN(empty)` returns zero rows too, so ANY survives an empty set.

**Code:** run with `python3 -I`.
```python
# Q22: ANY / SOME / ALL when SQLite has none: MAX / MIN and EXISTS / NOT EXISTS equivalents
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Atlas','Books',10),(2,'Novel','Books',20),(3,'Cookbook','Books',30),
 (4,'Digest','Mags',15),(5,'Zine','Mags',NULL),
 (6,'Pen','Stationery',5),(7,'Lamp','Home',25),(8,'Chair','Home',40),(9,'Desk','Home',35),
 (10,'Bag','Travel',NULL);
"""
# native syntax (PostgreSQL / MySQL), NOT executed on SQLite
NATIVE_ALL = "SELECT name FROM products WHERE price > ALL (SELECT price FROM products WHERE category = ?)"
NATIVE_ANY = "SELECT name FROM products WHERE price > ANY (SELECT price FROM products WHERE category = ?)"

SQL_ALL_MAX = """
SELECT product_id FROM products
WHERE price > (SELECT MAX(price) FROM products WHERE category = ?)
ORDER BY product_id
"""
SQL_ALL_NOT_EXISTS = """
SELECT p.product_id FROM products p
WHERE NOT EXISTS (SELECT 1 FROM products b
                  WHERE b.category = ?
                    AND NOT COALESCE(p.price > b.price, 0))
ORDER BY p.product_id
"""
SQL_ANY_MIN = """
SELECT product_id FROM products
WHERE price > (SELECT MIN(price) FROM products WHERE category = ?)
ORDER BY product_id
"""
SQL_ANY_EXISTS = """
SELECT p.product_id FROM products p
WHERE EXISTS (SELECT 1 FROM products b
              WHERE b.category = ?
                AND p.price > b.price)
ORDER BY p.product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

for label, sql in [("price > ALL", NATIVE_ALL), ("price > ANY", NATIVE_ANY), ("price > SOME", NATIVE_ANY.replace("ANY", "SOME"))]:
    try:
        con.execute(sql, ("Books",)).fetchall()
        print(label, "-> ran")
    except sqlite3.Error as e:
        print(f"{label} on SQLite -> {type(e).__name__}: {e}")

prices = pd.read_sql_query("SELECT * FROM products", con)
def ids(sql, cat):
    return [r[0] for r in con.execute(sql, (cat,))]

# pd:main
def pd_all(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]   # NaN compares False
    return df.loc[cmp.all(axis=1), "product_id"].tolist()            # all() of an empty row is True

def pd_any(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]
    return df.loc[cmp.any(axis=1), "product_id"].tolist()            # any() of an empty row is False
# pd:end

print()
res = {}
for cat, what in [("Books", "clean prices"), ("Mags", "one NULL price"), ("Toys", "empty subquery")]:
    r = (ids(SQL_ALL_MAX, cat), ids(SQL_ALL_NOT_EXISTS, cat), pd_all(prices, cat),
         ids(SQL_ANY_MIN, cat), ids(SQL_ANY_EXISTS, cat), pd_any(prices, cat))
    res[cat] = r
    print(f"{cat:5s} ({what})")
    for name, v in zip(["ALL MAX", "ALL NOT EXISTS", "pandas all", "ANY MIN", "ANY EXISTS", "pandas any"], r):
        print(f"   {name:15s}{v}")

for cat in res:
    mx, ne, pa, mn, ex, pn = res[cat]
    assert ne == pa and ex == pn and mn == ex       # NOT EXISTS / EXISTS forms equal pandas; ANY via MIN always equal
assert res["Books"][0] == res["Books"][1] == [8, 9]
assert res["Mags"][0] != res["Mags"][1] and res["Toys"][0] != res["Toys"][1]
print("\nasserts passed: NOT EXISTS == pandas all, EXISTS == MIN == pandas any; MAX differs from ALL on NULL and empty sets")
```

**Output (my run):**
```text
price > ALL on SQLite -> OperationalError: near "ALL": syntax error
price > ANY on SQLite -> OperationalError: near "SELECT": syntax error
price > SOME on SQLite -> OperationalError: near "SELECT": syntax error

Books (clean prices)
   ALL MAX        [8, 9]
   ALL NOT EXISTS [8, 9]
   pandas all     [8, 9]
   ANY MIN        [2, 3, 4, 7, 8, 9]
   ANY EXISTS     [2, 3, 4, 7, 8, 9]
   pandas any     [2, 3, 4, 7, 8, 9]
Mags  (one NULL price)
   ALL MAX        [2, 3, 7, 8, 9]
   ALL NOT EXISTS []
   pandas all     []
   ANY MIN        [2, 3, 7, 8, 9]
   ANY EXISTS     [2, 3, 7, 8, 9]
   pandas any     [2, 3, 7, 8, 9]
Toys  (empty subquery)
   ALL MAX        []
   ALL NOT EXISTS [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   pandas all     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   ANY MIN        []
   ANY EXISTS     []
   pandas any     []

asserts passed: NOT EXISTS == pandas all, EXISTS == MIN == pandas any; MAX differs from ALL on NULL and empty sets
```

**Edge cases:**
- **NULLs in the subquery:** `> ALL` is the fragile one. One NULL in the set turns "no row fails" into "some comparison is unknown", and a WHERE clause drops unknown. `> ANY` is not hurt, because one true comparison is enough. My run shows this: Mags gives `[]` for ALL (NOT EXISTS form) but the same five rows as MIN for ANY.
- **Empty subquery:** `> ALL (empty)` is TRUE for every row, `> ANY (empty)` is FALSE. The MAX/MIN rewrites cannot express this, because aggregates over zero rows are NULL (Toys: MAX form returned `[]`, the NOT EXISTS form returned all 10).
- **NULL on the left:** a product with a NULL price (Zine, Bag) fails `> ANY` and `> ALL` against a non-empty set, but passes `> ALL (empty)`. Bag appears in the Toys ALL result.
- **Fixing the MAX form:** add `AND NOT EXISTS (SELECT 1 FROM ... WHERE price IS NULL)` and a guard for the empty case. At that point `NOT EXISTS` is simpler and exact.
- **Ties:** `>` is strict, so a product priced exactly 30 does not beat Books' 30. Use `>= ALL` for "at least as expensive as all".

**Then explain:**
- **Meaning:** `x op ANY (S)` is true if the comparison is true for at least one value in S. `x op ALL (S)` is true if it is true for every value. `SOME` is a synonym for `ANY`.
- **Identities:** `= ANY (S)` is `IN (S)`, and `<> ALL (S)` is `NOT IN (S)`. So `NOT IN` inherits the same NULL trap as `<> ALL`: one NULL in S and no row can pass. I have not run the native forms.
- **Support:** SQLite rejected `ALL`, `ANY` and `SOME` with a syntax error in my run (messages above). PostgreSQL's subquery-expressions page documents `ANY`, `SOME` and `ALL`, with the empty-subquery and NULL rules above; the MySQL subquery-restrictions page lists them as well. Both are hedged, not executed.
- **MySQL restriction:** per its documentation, `ALL`, `ANY` and `SOME` need a scalar left side, and `LIMIT` inside them is not allowed. That is the same restriction as Q28; not executed here.
- **Which rewrite:** use MAX/MIN when you know the set is non-empty and has no NULLs (say so out loud), otherwise `NOT EXISTS` / `EXISTS`.

**Follow-ups:**
- *Is `> ANY` the same as `> MIN`?* Yes, in a WHERE clause: my runs matched on all three scenarios. MIN ignores NULLs, and an empty set gives no rows either way.
- *Why is `x <> ALL (S)` dangerous?* It is `NOT IN`, so a NULL in S gives no rows.
- *How would you write "price equals ANY"?* Just use `IN`.

**Common mistakes:**
- Treating `> ALL` as `> MAX` and getting wrong rows when the subquery is empty or contains NULL.
- Expecting `> ALL (empty)` to return no rows. It returns every row.
- Writing `NOT EXISTS (... WHERE p.price <= b.price)` and forgetting the unknown case when prices are NULL (use `NOT COALESCE(p.price > b.price, 0)` as in the Code block).
- Assuming SQLite supports `ANY`/`ALL` because other engines do.

### Q23 ⭐⭐ 🟡 Subquery versus JOIN: do they always return the same rows? customers(customer_id, name) and orders(order_id, customer_id, amount) with several orders per customer and a NULL customer_id order. Compare SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders) with the same via JOIN, and NOT IN versus LEFT JOIN ... IS NULL. Show where counts differ (duplicates from the JOIN, the NULL in NOT IN), say when you need DISTINCT, and when a subquery is clearer than a join because you only need a yes or no.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** No, not always: `IN (subquery)` returns each customer once, a JOIN returns one row per matching order (so Asha with 3 orders appears 3 times), and `NOT IN` returns nothing at all when the subquery contains one NULL while `LEFT JOIN ... IS NULL` and `NOT EXISTS` return the right customers.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,1,30),(4,2,40),(5,NULL,50);
```

**SQL answer:** all seven queries are in the Code block. The two pairs:
```sql
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders)
ORDER BY name
```
```sql
SELECT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
```
```sql
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY name
```
```sql
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.name
```
Also in the Code block: `SQL_JOIN_DISTINCT` (JOIN with DISTINCT), `SQL_NOT_IN_FIXED` (NOT IN with `WHERE customer_id IS NOT NULL` in the subquery) and `SQL_NOT_EXISTS`.

**pandas answer:** `isin` is the subquery form, `merge` the join form, and a left merge with `indicator=True` the anti-join.
```python
pd_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
pd_join = customers.merge(orders, on="customer_id")["name"].sort_values().tolist()
pd_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
           .query("_merge == 'left_only'")["name"].sort_values().tolist())
pd_not_isin = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
```

**Example:**
- Orders by customer: Asha 3 rows (10, 20, 30), Ben 1 row (40), one order with a NULL customer_id (50), Chitra and Dev none.
- `IN (SELECT customer_id FROM orders)`: the list is (1, 1, 1, 2, NULL). Asha matches, Ben matches, Chitra gives `3 = 1`, `3 = 2` false and `3 = NULL` unknown, so not true. Result Asha, Ben (2 rows). The NULL in the list is harmless for `IN`.
- `JOIN`: each order matches its customer once. Asha 3 rows, Ben 1 row, the NULL order matches nothing and drops. 4 rows, with Asha repeated. `SELECT DISTINCT` brings it back to 2.
- `NOT IN (1, 1, 1, 2, NULL)`: for Chitra, `3 <> 1 AND 3 <> 2 AND 3 <> NULL` is true AND true AND unknown, which is unknown, so she is dropped. Same for Dev. Zero rows.
- `LEFT JOIN ... WHERE o.order_id IS NULL`: Chitra and Dev have no order row, so the right side is NULL. Result Chitra, Dev. `NOT EXISTS` does the same, and so does `NOT IN` with the NULLs filtered out inside the subquery.

**Code:** run with `python3 -I`.
```python
# Q23: subquery vs JOIN: IN vs JOIN (duplicates) and NOT IN vs LEFT JOIN ... IS NULL (the NULL trap)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,1,30),(4,2,40),(5,NULL,50);
"""
SQL_IN = """
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders)
ORDER BY name
"""
SQL_JOIN = """
SELECT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
"""
SQL_JOIN_DISTINCT = """
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
"""
SQL_NOT_IN = """
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY name
"""
SQL_NOT_IN_FIXED = """
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)
ORDER BY name
"""
SQL_ANTI_JOIN = """
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.name
"""
SQL_NOT_EXISTS = """
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def names(sql):
    return [r[0] for r in con.execute(sql)]
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)

r = {k: names(v) for k, v in [("IN", SQL_IN), ("JOIN", SQL_JOIN), ("JOIN DISTINCT", SQL_JOIN_DISTINCT),
                              ("NOT IN", SQL_NOT_IN), ("NOT IN (NULLs filtered)", SQL_NOT_IN_FIXED),
                              ("LEFT JOIN IS NULL", SQL_ANTI_JOIN), ("NOT EXISTS", SQL_NOT_EXISTS)]}
for k, v in r.items():
    print(f"{k:24s} {len(v)} rows  {v}")

# pd:main
pd_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
pd_join = customers.merge(orders, on="customer_id")["name"].sort_values().tolist()
pd_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
           .query("_merge == 'left_only'")["name"].sort_values().tolist())
pd_not_isin = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
# pd:end
print("\npandas isin          ", pd_in)
print("pandas merge (join)  ", pd_join)
print("pandas anti-join     ", pd_anti)
print("pandas ~isin         ", pd_not_isin)

assert r["IN"] == pd_in == ["Asha", "Ben"]
assert r["JOIN"] == pd_join == ["Asha", "Asha", "Asha", "Ben"]
assert r["JOIN DISTINCT"] == ["Asha", "Ben"]
assert r["NOT IN"] == []
assert r["NOT IN (NULLs filtered)"] == r["LEFT JOIN IS NULL"] == r["NOT EXISTS"] == pd_anti == pd_not_isin == ["Chitra", "Dev"]
print("\nasserts passed: IN == isin (2 rows), JOIN == merge (4 rows with duplicates), NOT IN returns 0 rows, anti-joins return Chitra and Dev")
```

**Output (my run):**
```text
IN                       2 rows  ['Asha', 'Ben']
JOIN                     4 rows  ['Asha', 'Asha', 'Asha', 'Ben']
JOIN DISTINCT            2 rows  ['Asha', 'Ben']
NOT IN                   0 rows  []
NOT IN (NULLs filtered)  2 rows  ['Chitra', 'Dev']
LEFT JOIN IS NULL        2 rows  ['Chitra', 'Dev']
NOT EXISTS               2 rows  ['Chitra', 'Dev']

pandas isin           ['Asha', 'Ben']
pandas merge (join)   ['Asha', 'Asha', 'Asha', 'Ben']
pandas anti-join      ['Chitra', 'Dev']
pandas ~isin          ['Chitra', 'Dev']

asserts passed: IN == isin (2 rows), JOIN == merge (4 rows with duplicates), NOT IN returns 0 rows, anti-joins return Chitra and Dev
```

**Edge cases:**
- **Duplicates from the JOIN:** only the "one-to-many" side multiplies. Joining customers to orders gives 4 rows; a SUM over the joined rows is fine for a per-order measure but wrong for a per-customer measure (Part 2 Q13 has the fan-out case). If you only need the customer once, use `IN`, `EXISTS`, or `DISTINCT`.
- **The NULL order:** an INNER JOIN drops it silently. `IN` ignores it. `NOT IN` is wrecked by it. In pandas, `isin` and `merge` do not treat NaN like SQL (see Q21) but here the customer ids have no NaN, so the results match.
- **Empty subquery:** `NOT IN (empty)` returns every customer, `IN (empty)` none. Only a NULL in the list triggers the trap.
- **Orders pointing to a missing customer:** the JOIN and `IN` ignore them; an anti-join from the orders side would show them.

**Then explain:**
- **When they are the same:** `IN` and `JOIN` match when the subquery side has at most one row per key (a unique key such as a customer id). Here the orders side repeats keys, so they differ.
- **Subquery is clearer** when you only need a yes or no ("has this customer ever ordered?") and no columns from the other table. It also cannot multiply rows, so no DISTINCT is needed.
- **JOIN is needed** when you want columns from the other side (order amount, date), or to aggregate over them.
- **Anti-join:** prefer `NOT EXISTS` or `LEFT JOIN ... IS NULL`. If you keep `NOT IN`, filter NULLs in the subquery or the column must be declared NOT NULL.
- **Performance:** I did not measure it here. Optimisers often turn an `IN` or `EXISTS` subquery into a semi-join, so do not assume a subquery is slower; I have not run EXPLAIN on other engines (not executed). See Part 11 for plans.
- **Test the `IS NULL` check on a non-null column of the right side** (`o.order_id`), not on a column that can be NULL in a matching row.

**Follow-ups:**
- *Which is faster?* Depends on engine and data; look at the plan. Not measured here.
- *How do I get the same 2 rows from the JOIN?* `DISTINCT`, or join to `(SELECT DISTINCT customer_id FROM orders)`.
- *Why not just filter `NOT IN` with `IS NOT NULL`?* You can, I did (`SQL_NOT_IN_FIXED`), but you must remember to do it every time; `NOT EXISTS` is safe by construction.

**Common mistakes:**
- Using `NOT IN` against a nullable column.
- Counting customers with `COUNT(*)` after a one-to-many JOIN.
- Putting the filter on the right table in the `WHERE` of a LEFT JOIN (e.g. `o.amount > 0`), which turns it into an inner join.
- Adding `DISTINCT` to hide a join that should have been a semi-join.

### Q24 ⭐⭐ 🟡 UPDATE with a subquery: customers(customer_id, name, total_spent) and orders(order_id, customer_id, amount). Set total_spent to each customer's order total, with 0 for customers with no orders, using a correlated scalar subquery with COALESCE. Explain what happens without COALESCE (NULL), that SQLite supports this, and the dialect points as hedged text: UPDATE ... FROM in PostgreSQL and SQLite 3.33+, join-update syntax in MySQL, and MySQL error 1093 when the subquery reads the table being updated. Show a before and after check and the pandas map or merge equivalent.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Set the column to a correlated scalar subquery `(SELECT SUM(amount) FROM orders WHERE orders.customer_id = customers.customer_id)` wrapped in `COALESCE(..., 0)`, because a customer with no orders gets a NULL sum, and without the COALESCE you overwrite their total with NULL.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, total_spent INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha',999),(2,'Ben',NULL),(3,'Chitra',NULL),(4,'Dev',77),(5,'Esha',NULL);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,200),(4,5,NULL);
```
Asha and Dev start with stale totals (999 and 77), so you can see which updates overwrite them. Esha has one order whose amount is NULL.

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
UPDATE customers
SET total_spent = COALESCE((SELECT SUM(o.amount)
                            FROM orders o
                            WHERE o.customer_id = customers.customer_id), 0)
```
Variants, all executed in the Code block, each on a fresh copy of the data: the same without COALESCE,
```sql
UPDATE customers
SET total_spent = (SELECT SUM(o.amount)
                   FROM orders o
                   WHERE o.customer_id = customers.customer_id)
```
`UPDATE ... FROM` (SQLite 3.33 and later; it ran on the 3.45.1 used here),
```sql
UPDATE customers
SET total_spent = t.s
FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) AS t
WHERE customers.customer_id = t.customer_id
```
and a CTE before the UPDATE.
```sql
WITH t AS (SELECT customer_id, COALESCE(SUM(amount), 0) AS s FROM orders GROUP BY customer_id)
UPDATE customers
SET total_spent = COALESCE((SELECT s FROM t WHERE t.customer_id = customers.customer_id), 0)
```

**pandas answer:** aggregate once, `map` the Series onto the customer ids, fill the gaps with 0.
```python
totals = orders.groupby("customer_id")["amount"].sum()                 # all-NaN group sums to 0.0 by default
pd_df = cust.assign(total_spent=cust["customer_id"].map(totals).fillna(0).astype("int64"))
```

**Example:**
- Order totals: Asha 100 + 50 = 150, Ben 200, Esha only has a NULL amount (SUM of only NULLs is NULL), Chitra and Dev have no orders (subquery returns no row, so the scalar subquery is NULL).
- Before: Asha 999, Ben NULL, Chitra NULL, Dev 77, Esha NULL.
- With COALESCE: Asha 150, Ben 200, Chitra 0, Dev 0, Esha 0. Five rows updated. Dev's stale 77 is correctly reset to 0.
- Without COALESCE: Asha 150, Ben 200, and Chitra, Dev, Esha all NULL (printed `NaN` by pandas).
- `UPDATE ... FROM` joins to the per-customer aggregate, so it touches only customers that have order rows (3 rows: Asha, Ben, Esha). Chitra stays NULL and Dev keeps the stale 77. Esha is updated to NULL because her SUM is NULL.
- Check: the updated column adds to 350 and so does `SUM(amount)` on the orders table (assert in the Code block).

**Code:** run with `python3 -I`.
```python
# Q24: UPDATE with a correlated scalar subquery (COALESCE), UPDATE ... FROM, WITH before UPDATE, pandas map
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, total_spent INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha',999),(2,'Ben',NULL),(3,'Chitra',NULL),(4,'Dev',77),(5,'Esha',NULL);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,200),(4,5,NULL);
"""
SQL_MAIN = """
UPDATE customers
SET total_spent = COALESCE((SELECT SUM(o.amount)
                            FROM orders o
                            WHERE o.customer_id = customers.customer_id), 0)
"""
SQL_NO_COALESCE = """
UPDATE customers
SET total_spent = (SELECT SUM(o.amount)
                   FROM orders o
                   WHERE o.customer_id = customers.customer_id)
"""
SQL_UPDATE_FROM = """
UPDATE customers
SET total_spent = t.s
FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) AS t
WHERE customers.customer_id = t.customer_id
"""
SQL_WITH_UPDATE = """
WITH t AS (SELECT customer_id, COALESCE(SUM(amount), 0) AS s FROM orders GROUP BY customer_id)
UPDATE customers
SET total_spent = COALESCE((SELECT s FROM t WHERE t.customer_id = customers.customer_id), 0)
"""
CHECK = "SELECT customer_id, name, total_spent FROM customers ORDER BY customer_id"

def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c
BASE = fresh().total_changes                   # rows inserted by the setup script
def run(sql):
    c = fresh()
    c.execute(sql)
    return c, c.total_changes - BASE     # rowcount is -1 for a statement that starts with WITH
def table(c):
    return pd.read_sql_query(CHECK, c)

con = fresh()
before = table(con)
print("BEFORE (stale values 999 and 77, NULLs elsewhere):")
print(before.to_string(index=False))
print("check query, orders per customer:", con.execute(
    "SELECT customer_id, SUM(amount), COUNT(*) FROM orders GROUP BY customer_id").fetchall())

c_main, n_main = run(SQL_MAIN)
c_nc, n_nc = run(SQL_NO_COALESCE)
c_from, n_from = run(SQL_UPDATE_FROM)
c_with, n_with = run(SQL_WITH_UPDATE)
sql_df = table(c_main)
print(f"\nAFTER SQL_MAIN (correlated subquery + COALESCE), rows updated: {n_main}")
print(sql_df.to_string(index=False))
print(f"\nAFTER SQL_NO_COALESCE, rows updated: {n_nc}")
print(table(c_nc).to_string(index=False))
print(f"\nAFTER SQL_UPDATE_FROM (SQLite 3.45), rows updated: {n_from}")
print(table(c_from).to_string(index=False))
print(f"\nAFTER SQL_WITH_UPDATE, rows updated: {n_with}")
print(table(c_with).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
cust = before.copy()
# pd:main
totals = orders.groupby("customer_id")["amount"].sum()                 # all-NaN group sums to 0.0 by default
pd_df = cust.assign(total_spent=cust["customer_id"].map(totals).fillna(0).astype("int64"))
# pd:end
print("\npandas map + fillna(0):")
print(pd_df.to_string(index=False))
strict = orders.groupby("customer_id")["amount"].sum(min_count=1)
print("pandas sum() of Esha's only (NaN) order:", totals.loc[5], "| with min_count=1:", strict.loc[5])

# compared by customer_id, same order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(sql_df, table(c_with), check_dtype=False)
assert table(c_nc)["total_spent"].isna().tolist() == [False, False, True, True, True]
assert table(c_from)["total_spent"].fillna(-1).tolist() == [150, 200, -1, 77, -1]
assert orders["amount"].sum() == sql_df["total_spent"].sum() == 350
print("\nasserts passed: SQL == pandas == WITH variant; UPDATE ... FROM leaves unmatched customers untouched; totals tie to orders (350)")
```

**Output (my run):**
```text
BEFORE (stale values 999 and 77, NULLs elsewhere):
 customer_id   name  total_spent
           1   Asha        999.0
           2    Ben          NaN
           3 Chitra          NaN
           4    Dev         77.0
           5   Esha          NaN
check query, orders per customer: [(1, 150, 2), (2, 200, 1), (5, None, 1)]

AFTER SQL_MAIN (correlated subquery + COALESCE), rows updated: 5
 customer_id   name  total_spent
           1   Asha          150
           2    Ben          200
           3 Chitra            0
           4    Dev            0
           5   Esha            0

AFTER SQL_NO_COALESCE, rows updated: 5
 customer_id   name  total_spent
           1   Asha        150.0
           2    Ben        200.0
           3 Chitra          NaN
           4    Dev          NaN
           5   Esha          NaN

AFTER SQL_UPDATE_FROM (SQLite 3.45), rows updated: 3
 customer_id   name  total_spent
           1   Asha        150.0
           2    Ben        200.0
           3 Chitra          NaN
           4    Dev         77.0
           5   Esha          NaN

AFTER SQL_WITH_UPDATE, rows updated: 5
 customer_id   name  total_spent
           1   Asha          150
           2    Ben          200
           3 Chitra            0
           4    Dev            0
           5   Esha            0

pandas map + fillna(0):
 customer_id   name  total_spent
           1   Asha          150
           2    Ben          200
           3 Chitra            0
           4    Dev            0
           5   Esha            0
pandas sum() of Esha's only (NaN) order: 0.0 | with min_count=1: nan

asserts passed: SQL == pandas == WITH variant; UPDATE ... FROM leaves unmatched customers untouched; totals tie to orders (350)
```

**Edge cases:**
- **No orders:** the correlated subquery returns no rows, and a scalar subquery with no rows is NULL. `COALESCE(..., 0)` turns that into 0. The stale 77 on Dev shows the difference between "update everyone" and "update only matched customers".
- **NULL amounts:** Esha's `SUM(NULL)` is NULL, so even a customer who has an order can get NULL; the COALESCE covers both. pandas differs: `sum()` of an all-NaN group is 0.0 by default and NaN only with `min_count=1` (both printed in my run). So the pandas `map` result needs no `fillna` for Esha, only for customers missing from the Series.
- **Row count:** the Python `sqlite3` module reports `rowcount = -1` for a statement that starts with `WITH`, so I counted changes with `total_changes` instead.
- **Many orders per customer:** the subquery aggregates inside, so there is still one value per customer. An unaggregated subquery returning several rows would silently take the first row in SQLite (see Q26).
- **Run it as a transaction:** wrap the UPDATE in a transaction and check the before/after counts first when doing it on real data (`BEGIN; UPDATE ...; check; COMMIT`).

**Then explain:**
- **Correlated:** the inner query refers to the outer row (`customers.customer_id`), so it runs per customer. For an UPDATE the outer row is the row being updated.
- **Why COALESCE:** an UPDATE assigns whatever the subquery returns, NULL included. Decide whether "no orders" should be 0 or NULL and write it down.
- **Dialect points (not executed here):** PostgreSQL supports `UPDATE ... SET ... FROM ... WHERE`, the same shape as my SQLite 3.45 run. MySQL uses a join in the UPDATE (`UPDATE customers c LEFT JOIN (SELECT ...) t ON ... SET c.total_spent = COALESCE(t.s, 0)`). The MySQL documentation says you cannot modify a table and select from the same table in a subquery; that is error 1093 (the number is from memory, not on the page I read), and the workaround is to wrap the subquery in a derived table. Not executed here. SQLite allowed the subquery here because the subquery reads `orders`, not `customers` (Q25 shows the same-table case).
- **LEFT JOIN update:** `UPDATE ... FROM` with an inner join skips unmatched rows. To reset the unmatched ones you need the COALESCE form, a second UPDATE, or a LEFT JOIN where the dialect allows it.
- **CTE before UPDATE:** SQLite accepted `WITH ... UPDATE` in my run.

**Follow-ups:**
- *How would you make it safe to rerun?* The statement is idempotent: running it twice gives the same totals, because it recomputes from orders.
- *Is it slow?* It runs one aggregate per customer; with an index on `orders(customer_id)` that is a lookup. I did not time it here.
- *Why not store the total at all?* A stored total goes stale as orders change; a view or query computes it fresh. If you must store it, rebuild it on a schedule or maintain it with a trigger.

**Common mistakes:**
- Forgetting COALESCE and wiping totals to NULL.
- Using `UPDATE ... FROM` with an inner join and leaving stale values on unmatched rows.
- Assuming pandas and SQL agree on a sum of only NULLs (0.0 versus NULL).
- Running the UPDATE without a before/after count check.

### Q25 ⭐⭐ 🟡 DELETE with a subquery: employees(emp_id, name, email) has duplicate rows for the same email. Delete the duplicates keeping the row with the smallest emp_id using DELETE FROM employees WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email), and a NOT EXISTS / correlated version. Explain the NULL-email risk, the NOT IN with NULL id risk, that SQLite allows a subquery on the same table while MySQL raises error 1093 (hedged; workaround is a derived table), and the pandas drop_duplicates(keep='first').
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Keep the smallest `emp_id` per email and delete the rest with `DELETE FROM employees WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email)`, but know that `GROUP BY` puts all NULL emails in one group (so NULL-email rows get "deduplicated" too) and that a NULL in the id list would make NOT IN delete nothing; `NOT EXISTS` with an earlier row of the same email avoids both.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO employees VALUES
 (1,'Asha','a@x.com'),(2,'Asha R','a@x.com'),
 (3,'Ben','b@x.com'),(4,'Ben K','b@x.com'),(5,'Ben K2','b@x.com'),
 (6,'Chitra','c@x.com'),
 (7,'Dev',NULL),(8,'Eve',NULL);
```
The Code block also builds a second table, `emp_loose(emp_id INTEGER, email TEXT)`, with no primary key and two NULL ids, for the NULL-id risk.

**SQL answer:** all in the Code block. The question's version:
```sql
DELETE FROM employees
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email)
```
The correlated NOT EXISTS-style version (delete a row if an earlier row has the same email):
```sql
DELETE FROM employees
WHERE EXISTS (SELECT 1 FROM employees e2
              WHERE e2.email = employees.email
                AND e2.emp_id < employees.emp_id)
```
The same NOT IN with a CTE in front of DELETE (it ran on SQLite 3.45):
```sql
WITH keep AS (SELECT MIN(emp_id) AS id FROM employees GROUP BY email)
DELETE FROM employees WHERE emp_id NOT IN (SELECT id FROM keep)
```

**pandas answer:** sort by `emp_id` and keep the first row per email.
```python
dedup_all = emp.sort_values("emp_id").drop_duplicates(subset="email", keep="first")        # NaN emails count as equal
dedup_sql_exists = emp[emp["email"].isna() | ~emp.duplicated(subset="email", keep="first")]  # NULL emails never match
```
`dedup_all` is the NOT IN result. `dedup_sql_exists` keeps every NULL-email row, which is what the correlated version does.

**Example:**
- Groups by email: a@x.com has ids 1, 2 (min 1); b@x.com has 3, 4, 5 (min 3); c@x.com has id 6 (min 6); the NULL group has ids 7, 8 (min 7).
- `NOT IN (1, 3, 6, 7)` deletes ids 2, 4, 5, 8: four rows. Kept 1, 3, 6, 7.
- The NOT EXISTS version looks for an earlier row with the same email: id 2 has id 1 (delete), ids 4 and 5 have id 3 (delete), id 8 has no match because `NULL = NULL` is not true, so it stays. Three rows deleted, kept 1, 3, 6, 7, 8.
- So the two are not the same whenever emails can be NULL: GROUP BY treats NULLs as one group, equality does not. Whether Dev and Eve are duplicates is a business decision; neither query asks it.
- pandas `drop_duplicates(subset="email")` treats NaN as equal to NaN, so it matches the NOT IN result, ids 1, 3, 6, 7.

**Code:** run with `python3 -I`.
```python
# Q25: DELETE duplicates with a subquery on the same table: NOT IN vs NOT EXISTS, NULL email, NULL id
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO employees VALUES
 (1,'Asha','a@x.com'),(2,'Asha R','a@x.com'),
 (3,'Ben','b@x.com'),(4,'Ben K','b@x.com'),(5,'Ben K2','b@x.com'),
 (6,'Chitra','c@x.com'),
 (7,'Dev',NULL),(8,'Eve',NULL);
CREATE TABLE emp_loose(emp_id INTEGER, email TEXT);
INSERT INTO emp_loose VALUES (1,'a@x.com'),(2,'a@x.com'),(NULL,'b@x.com'),(NULL,'b@x.com'),(5,'c@x.com');
"""
SQL_NOT_IN = """
DELETE FROM employees
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email)
"""
SQL_NOT_EXISTS = """
DELETE FROM employees
WHERE EXISTS (SELECT 1 FROM employees e2
              WHERE e2.email = employees.email
                AND e2.emp_id < employees.emp_id)
"""
SQL_WITH_DELETE = """
WITH keep AS (SELECT MIN(emp_id) AS id FROM employees GROUP BY email)
DELETE FROM employees WHERE emp_id NOT IN (SELECT id FROM keep)
"""
SQL_LOOSE_NOT_IN = """
DELETE FROM emp_loose
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM emp_loose GROUP BY email)
"""
SQL_LOOSE_NOT_EXISTS = """
DELETE FROM emp_loose
WHERE NOT EXISTS (SELECT 1 FROM (SELECT MIN(emp_id) AS m FROM emp_loose GROUP BY email) k
                  WHERE k.m = emp_loose.emp_id)
"""
def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c
BASE = fresh().total_changes          # rows inserted by the setup script
def run(sql, tbl="employees"):
    c = fresh()
    c.execute(sql)
    rows = c.execute(f"SELECT * FROM {tbl} ORDER BY emp_id").fetchall()
    return rows, c.total_changes - BASE

con = fresh()
emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
print("before:", len(emp), "rows")
rows_in, n_in = run(SQL_NOT_IN)
rows_ex, n_ex = run(SQL_NOT_EXISTS)
rows_with, n_with = run(SQL_WITH_DELETE)
print("\nNOT IN (MIN(emp_id) ... GROUP BY email):  deleted", n_in, "kept ids", [r[0] for r in rows_in])
print("NOT EXISTS (earlier row, same email):     deleted", n_ex, "kept ids", [r[0] for r in rows_ex])
print("WITH keep AS (...) DELETE ... NOT IN:      deleted", n_with, "kept ids", [r[0] for r in rows_with])

# pd:main
dedup_all = emp.sort_values("emp_id").drop_duplicates(subset="email", keep="first")        # NaN emails count as equal
dedup_sql_exists = emp[emp["email"].isna() | ~emp.duplicated(subset="email", keep="first")]  # NULL emails never match
# pd:end
print("\npandas drop_duplicates(subset='email', keep='first') ids:", dedup_all["emp_id"].tolist())
print("pandas NULL emails kept (like NOT EXISTS) ids:           ", dedup_sql_exists["emp_id"].tolist())

loose_in, _ = run(SQL_LOOSE_NOT_IN, "emp_loose")
loose_ex, _ = run(SQL_LOOSE_NOT_EXISTS, "emp_loose")
print("\nemp_loose has NULL emp_id rows (no primary key). Before: 5 rows")
print("  NOT IN with a NULL in the list, rows left:", len(loose_in), loose_in)
print("  NOT EXISTS form, rows left:               ", len(loose_ex), loose_ex)

assert [r[0] for r in rows_in] == [r[0] for r in rows_with] == dedup_all["emp_id"].tolist() == [1, 3, 6, 7]
assert [r[0] for r in rows_ex] == dedup_sql_exists["emp_id"].tolist() == [1, 3, 6, 7, 8]
assert len(loose_in) == 5
print("\nasserts passed: NOT IN == WITH variant == drop_duplicates (ids 1,3,6,7); NOT EXISTS == pandas with NULL emails kept (ids 1,3,6,7,8); compared as lists of emp_id sorted ascending")
```

**Output (my run):**
```text
before: 8 rows

NOT IN (MIN(emp_id) ... GROUP BY email):  deleted 4 kept ids [1, 3, 6, 7]
NOT EXISTS (earlier row, same email):     deleted 3 kept ids [1, 3, 6, 7, 8]
WITH keep AS (...) DELETE ... NOT IN:      deleted 4 kept ids [1, 3, 6, 7]

pandas drop_duplicates(subset='email', keep='first') ids: [1, 3, 6, 7]
pandas NULL emails kept (like NOT EXISTS) ids:            [1, 3, 6, 7, 8]

emp_loose has NULL emp_id rows (no primary key). Before: 5 rows
  NOT IN with a NULL in the list, rows left: 5 [(None, 'b@x.com'), (None, 'b@x.com'), (1, 'a@x.com'), (2, 'a@x.com'), (5, 'c@x.com')]
  NOT EXISTS form, rows left:                2 [(1, 'a@x.com'), (5, 'c@x.com')]

asserts passed: NOT IN == WITH variant == drop_duplicates (ids 1,3,6,7); NOT EXISTS == pandas with NULL emails kept (ids 1,3,6,7,8); compared as lists of emp_id sorted ascending
```

**Edge cases:**
- **NULL email:** covered above. Decide whether rows with no email are duplicates. If not, exclude them: `WHERE email IS NOT NULL` in the subquery and keep NULL-email rows with `OR email IS NULL`, or use the NOT EXISTS form.
- **NULL emp_id risk:** if the id column can be NULL (my `emp_loose` table has no primary key), a group whose ids are all NULL has `MIN` equal to NULL, so the NOT IN list contains a NULL and no row can pass `NOT IN`. In my run nothing was deleted (5 rows left, the duplicate id 2 included). The `NOT EXISTS`-against-the-keep-list form deleted both NULL-id rows and left 2 rows. Neither is right, so dedupe on a real, non-null key, and keep the primary key.
- **Ties:** `MIN(emp_id)` is unique per group only because `emp_id` is unique. If the key repeats, you keep several rows per group.
- **Rows deleted count:** `SELECT COUNT(*) FROM employees` before and after (8 to 4 for NOT IN, 8 to 5 for NOT EXISTS here).
- **Case and spaces:** `A@x.com` and `a@x.com ` are different strings, so normalise with `LOWER(TRIM(email))` first if that matters. I did not run that here.

**Then explain:**
- **Why it works:** the subquery returns the one id to keep for each email; every other id is deleted. The subquery runs once (it is not correlated), and the result list is checked per row.
- **Same-table subquery:** SQLite let me delete from `employees` while selecting from it. MySQL does not (error 1093, number from memory; the MySQL documentation says you cannot modify and select from the same table in a subquery). The workaround is a derived table around the inner query, for example `NOT IN (SELECT id FROM (SELECT MIN(emp_id) AS id FROM employees GROUP BY email) k)`. Not executed here. PostgreSQL's behaviour for this statement I did not run.
- **Check before deleting:** run the same subquery as a SELECT (`SELECT * FROM employees WHERE emp_id NOT IN (...)`) first, then wrap the DELETE in a transaction.
- **pandas:** `keep='first'` after sorting keeps the smallest id. `keep='last'` keeps the largest, `keep=False` drops every duplicated row.
- A window-function version (ROW_NUMBER, then delete rows numbered above 1) is in Part 4.

**Follow-ups:**
- *Why not `DELETE ... JOIN`?* Join-delete syntax is not standard SQL and differs by engine (MySQL has `DELETE e1 FROM ... JOIN`); not executed here.
- *How do I keep the newest instead?* Use `MAX(emp_id)` (or the latest date).
- *How do I stop it happening again?* A `UNIQUE` constraint on the email column; NULLs are allowed multiple times under UNIQUE in most engines (I did not run that here).

**Common mistakes:**
- Using `NOT IN` where the subquery can return NULL.
- Not thinking about NULL emails and silently deleting rows that were never real duplicates.
- Running the DELETE without previewing it as a SELECT and without a transaction.
- Using `MIN(name)` or another non-key column to choose the keeper.

### Q26 ⭐⭐ 🟡 The max-per-group tie problem: employees(emp_id, name, dept_id, salary). Return the highest-paid employee in each department, and all of them when there is a tie. Solve it by joining to a derived table of MAX(salary) per department, and with a correlated subquery, and show that a LIMIT 1 per group or a GROUP BY with a bare column gives one arbitrary row. Explain the tie behaviour, the pandas transform('max') mask versus idxmax, and the pointer to the window version in Part 4.
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** To keep ties, find each department's MAX(salary) first and match every employee against it, either by joining to a derived table of those maxima or with a correlated `salary = (SELECT MAX(...) ... same dept)`; `LIMIT 1` per group or a bare column under `GROUP BY` returns exactly one row, so a tie is cut down to one arbitrary person.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
 (4,'Dev',20,80),
 (5,'Eve',30,60),(6,'Farid',30,50),
 (7,'Hari',40,NULL),
 (8,'Ivy',NULL,95);
```
Department 10 has a tie at 90. Hari's salary is NULL. Ivy has no department.

**SQL answer:** `SQL_MAIN` (derived-table join) in the Code block.
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, MAX(salary) AS max_salary
      FROM employees
      GROUP BY dept_id) m
  ON m.dept_id = e.dept_id AND m.max_salary = e.salary
ORDER BY e.dept_id, e.emp_id
```
The correlated version:
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary = (SELECT MAX(e2.salary)
                  FROM employees e2
                  WHERE e2.dept_id = e.dept_id)
ORDER BY e.dept_id, e.emp_id
```
The two wrong-by-design forms, for contrast. A `LIMIT 1` per group:
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.emp_id = (SELECT e2.emp_id FROM employees e2
                  WHERE e2.dept_id = e.dept_id
                  ORDER BY e2.salary DESC LIMIT 1)
ORDER BY e.dept_id
```
And a bare column under `GROUP BY`:
```sql
SELECT dept_id, name, MAX(salary) AS max_salary
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id
ORDER BY dept_id
```
The Code block also has `SQL_NOT_EXISTS` ("nobody in my department earns more").

**pandas answer:** a mask against the per-group max keeps all ties; `idxmax` keeps one row per group.
```python
mask = emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[mask].sort_values(["dept_id", "emp_id"]).reset_index(drop=True)
idx_df = emp.dropna(subset=["salary", "dept_id"]).loc[lambda d: d.groupby("dept_id")["salary"].idxmax()]
```

**Example:**
- Department maxima: 10 gives 90, 20 gives 80, 30 gives 60, 40 gives NULL (its only salary is NULL), and the NULL department forms one group with max 95.
- Join: Asha (10, 90) matches 90, Ben (10, 90) matches 90, Chitra (70) does not. Dev matches 80. Eve matches 60, Farid does not. So the result is Asha, Ben, Dev, Eve (ids 1, 2, 4, 5). The tie in department 10 produces two rows.
- Hari: `m.max_salary = e.salary` is `NULL = NULL`, not true, so he is dropped. Ivy: `m.dept_id = e.dept_id` is `NULL = NULL`, also dropped.
- Correlated: for Asha the inner query returns 90, equal, kept. For Ivy the inner `e2.dept_id = NULL` matches no row, the scalar subquery is NULL, `95 = NULL` is not true, dropped. Same result, ids 1, 2, 4, 5.
- `LIMIT 1` per group: each department yields one `emp_id`; in my run department 10 returned Asha and not Ben. Ben is simply cut, and nothing in the SQL says why Asha won.
- pandas: `transform("max")` writes the department maximum on every row (90, 90, 90, 80, 60, 60, NaN, NaN; the NaN key and the all-NaN department both give NaN), and `salary == max` is False for NaN rows. Mask gives ids 1, 2, 4, 5, same as SQL.

**Code:** run with `python3 -I`.
```python
# Q26: highest-paid employee per department, ties included: derived-table join vs correlated subquery
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
 (4,'Dev',20,80),
 (5,'Eve',30,60),(6,'Farid',30,50),
 (7,'Hari',40,NULL),
 (8,'Ivy',NULL,95);
"""
SQL_MAIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, MAX(salary) AS max_salary
      FROM employees
      GROUP BY dept_id) m
  ON m.dept_id = e.dept_id AND m.max_salary = e.salary
ORDER BY e.dept_id, e.emp_id
"""
SQL_CORRELATED = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary = (SELECT MAX(e2.salary)
                  FROM employees e2
                  WHERE e2.dept_id = e.dept_id)
ORDER BY e.dept_id, e.emp_id
"""
SQL_NOT_EXISTS = """
SELECT e.emp_id FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM employees e2
                  WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary)
ORDER BY e.emp_id
"""
SQL_LIMIT1 = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.emp_id = (SELECT e2.emp_id FROM employees e2
                  WHERE e2.dept_id = e.dept_id
                  ORDER BY e2.salary DESC LIMIT 1)
ORDER BY e.dept_id
"""
SQL_BARE = """
SELECT dept_id, name, MAX(salary) AS max_salary
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id
ORDER BY dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
corr_df = pd.read_sql_query(SQL_CORRELATED, con)
print("derived-table join (ties kept):")
print(sql_df.to_string(index=False))
print("correlated subquery ids:", corr_df["emp_id"].tolist())
print("NOT EXISTS (nobody earns more) ids:", [r[0] for r in con.execute(SQL_NOT_EXISTS)])
print("\nLIMIT 1 per group (no tie-break) -> one row per department:")
print(pd.read_sql_query(SQL_LIMIT1, con).to_string(index=False))
print("\nGROUP BY dept_id with bare column `name` next to MAX(salary) (SQLite only):")
print(pd.read_sql_query(SQL_BARE, con).to_string(index=False))

print("\nFROM-subquery without an alias:", con.execute(
    "SELECT MAX(m) FROM (SELECT MAX(salary) AS m FROM employees GROUP BY dept_id)").fetchall())
print("scalar subquery returning many rows (dept 10, ORDER BY salary ASC / DESC):",
      con.execute("SELECT (SELECT salary FROM employees WHERE dept_id = 10 ORDER BY salary), "
                  "(SELECT salary FROM employees WHERE dept_id = 10 ORDER BY salary DESC)").fetchone())

# pd:main
mask = emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[mask].sort_values(["dept_id", "emp_id"]).reset_index(drop=True)
idx_df = emp.dropna(subset=["salary", "dept_id"]).loc[lambda d: d.groupby("dept_id")["salary"].idxmax()]
# pd:end
print("\npandas transform('max') mask ids:", pd_df["emp_id"].tolist())
print("pandas idxmax ids (one per dept):", idx_df["emp_id"].tolist())
print("transform('max') on the NaN dept key:", emp.groupby("dept_id")["salary"].transform("max").tolist())

# compared after sorting by dept_id, emp_id; NaN dept/salary rows never match in either engine
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert corr_df["emp_id"].tolist() == sql_df["emp_id"].tolist() == [1, 2, 4, 5]
assert len(idx_df) == 3 and set(idx_df["dept_id"]) == {10, 20, 30}
print("\nasserts passed: join == correlated == pandas transform mask (ids 1,2,4,5); idxmax returns one row per department")
```

**Output (my run):**
```text
derived-table join (ties kept):
 emp_id name  dept_id  salary
      1 Asha       10      90
      2  Ben       10      90
      4  Dev       20      80
      5  Eve       30      60
correlated subquery ids: [1, 2, 4, 5]
NOT EXISTS (nobody earns more) ids: [1, 2, 4, 5, 7, 8]

LIMIT 1 per group (no tie-break) -> one row per department:
 emp_id name  dept_id  salary
      1 Asha       10    90.0
      4  Dev       20    80.0
      5  Eve       30    60.0
      7 Hari       40     NaN

GROUP BY dept_id with bare column `name` next to MAX(salary) (SQLite only):
 dept_id name  max_salary
      10 Asha        90.0
      20  Dev        80.0
      30  Eve        60.0
      40 Hari         NaN

FROM-subquery without an alias: [(95,)]
scalar subquery returning many rows (dept 10, ORDER BY salary ASC / DESC): (70, 90)

pandas transform('max') mask ids: [1, 2, 4, 5]
pandas idxmax ids (one per dept): [1, 4, 5]
transform('max') on the NaN dept key: [90.0, 90.0, 90.0, 80.0, 60.0, 60.0, nan, nan]

asserts passed: join == correlated == pandas transform mask (ids 1,2,4,5); idxmax returns one row per department
```

**Edge cases:**
- **Ties:** the join, the correlated subquery and the pandas mask all return both Asha and Ben. If you want exactly one per department, say how to break the tie (lowest `emp_id`, earliest hire date) and put it in the query; Part 4 does this with `ROW_NUMBER`.
- **NULL salary:** `NOT EXISTS (higher salary)` returned Hari and Ivy as well (ids 7 and 8) because a NULL comparison finds no higher row, so "nobody earns more" is true. The join and `=` versions drop them. Pick on purpose.
- **NULL department:** the NULL group exists in `GROUP BY` (max 95), but `NULL = NULL` never joins it back to Ivy. pandas `groupby` drops NaN keys, so `transform("max")` gives NaN for Ivy and the mask excludes her. SQL and pandas agree for different reasons.
- **Department with all NULL salaries:** department 40 appears in the SQL maxima with a NULL max, and returns nothing. pandas `idxmax` on an all-NaN group would be a problem, so I dropped NaN salary and department rows before `idxmax` (I did not run the version without the drop).
- **Empty department:** a department with no employees has no row, so it cannot appear in either result.

**Then explain:**
- **Tie behaviour:** the join compares with `=` to the max, so every employee at the max qualifies. That is usually what "the highest-paid, and all of them when tied" asks for.
- **`LIMIT 1` per group:** a correlated `ORDER BY salary DESC LIMIT 1` returns one row per department. With a tie the choice depends on the engine and plan unless you add a tie-breaker such as `, e2.emp_id`.
- **Bare column with GROUP BY:** SQLite accepted `SELECT dept_id, name, MAX(salary) ... GROUP BY dept_id`, and returned Asha for department 10; the other engines I know of reject a non-aggregated column like that or pick arbitrarily (not executed here; PostgreSQL rejects it from what I know, MySQL depends on `ONLY_FULL_GROUP_BY`). Do not rely on it. It also hides the tie.
- **Two other SQLite facts from the run:** a FROM-subquery without an alias is accepted (the Code block ran `FROM (SELECT ...)` with no name; other engines may require one, not executed), and a scalar subquery that returns several rows does not error, it returns the first row in its `ORDER BY` (70 ascending, 90 descending for department 10). PostgreSQL documents an error for that case, which I did not run.
- **pandas:** `transform("max")` keeps the original index and length, so a boolean mask works directly (the same idea as the derived-table join). `idxmax` returns the index label of the first max in each group, so it returns one row and drops the tie.
- Window version, `RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) = 1`, is in Part 4.

**Follow-ups:**
- *How do I get exactly one per department?* Add a deterministic tie-break, `ORDER BY salary DESC, emp_id LIMIT 1`, or `ROW_NUMBER` in Part 4.
- *Which is faster, join or correlated?* Not measured here; the join aggregates once, the correlated form runs the inner query per outer row unless the optimiser rewrites it (not executed).
- *How would I find the second highest?* Part 4 and Q27.

**Common mistakes:**
- `WHERE salary = (SELECT MAX(salary) FROM employees)`: that is the single highest in the whole company, not per department.
- `GROUP BY dept_id` with `name` selected and trusting the name that comes back.
- Using `idxmax` and being surprised that ties vanish.
- Forgetting that NULL salaries and NULL departments fall out of equality joins.

### Q27 ⭐⭐ 🟡 Top-N per group via a correlated subquery, no window functions: employees(emp_id, name, dept_id, salary). Return the top 2 earners in each department using WHERE (SELECT COUNT(*) FROM employees e2 WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2. Explain why strict > makes ties share a rank (so more than 2 rows can return), how to break ties with emp_id, the cost (one count per outer row, quadratic per group), why LIMIT inside a per-group subquery is not portable (hedged: MySQL error 1235 for LIMIT in IN), and the pandas groupby head or nlargest. Point to Part 4 for ROW_NUMBER.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** For each employee, count how many people in the same department earn strictly more, and keep the employee if that count is below 2; because the test is strict `>`, tied salaries share a rank, so a tie at second place returns more than 2 rows, and you add `emp_id` to the comparison to get exactly 2.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,60),
 (5,'Eve',20,80),(6,'Farid',20,75),(7,'Gita',20,75),(8,'Hari',20,60),
 (9,'Ivy',30,50);
```
Department 20 has a tie for second place (Farid and Gita at 75).

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
```
With the tie broken by `emp_id` (`SQL_TIEBREAK`):
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary > e.salary OR (e2.salary = e.salary AND e2.emp_id < e.emp_id))) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
```
The same with a row-value comparison (`SQL_ROWVALUE`), which ran on SQLite 3.45:
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id)) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
```

**pandas answer:** `rank(method="min")` reproduces the strict-greater count, `head(2)` after a sort reproduces the tie-break, and `nlargest` is the per-group shortcut.
```python
rank_min = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False)     # = (count strictly higher) + 1
pd_ties = emp[rank_min <= 2].sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
           .groupby("dept_id").head(2))
pd_nlargest = emp.groupby("dept_id", group_keys=False).apply(lambda g: g.nlargest(2, "salary", keep="first"))
```

**Example:** the inner count for each employee (printed as `higher` in the Code block).
- Department 10: Asha 90 has 0 higher, Ben 90 has 0 (equal is not higher), Chitra 70 has 2, Dev 60 has 3. `< 2` keeps Asha and Ben.
- Department 20: Eve 80 has 0, Farid 75 has 1, Gita 75 has 1, Hari 60 has 3. `< 2` keeps Eve, Farid and Gita, three rows for a "top 2".
- Department 30: Ivy 50 has 0, kept.
- Total 6 rows for `SQL_MAIN`.
- With the tie-break: Gita's count becomes 2 (Eve higher, and Farid has the same salary with a smaller id), so she drops. Department 20 returns Eve and Farid. Total 5 rows, exactly 2 per department (department 30 has only one person).
- The row-value version compares `(salary, -emp_id)` as a pair, higher salary first and lower id winning ties. It returned the same ids, 1, 2, 5, 6, 9.

**Code:** run with `python3 -I`.
```python
# Q27: top-N per group with a correlated COUNT subquery (no window functions); ties; tie-break; row values
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,60),
 (5,'Eve',20,80),(6,'Farid',20,75),(7,'Gita',20,75),(8,'Hari',20,60),
 (9,'Ivy',30,50);
"""
SQL_MAIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_TIEBREAK = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary > e.salary OR (e2.salary = e.salary AND e2.emp_id < e.emp_id))) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_ROWVALUE = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id)) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_COUNTS = """
SELECT e.emp_id, e.dept_id, e.salary,
       (SELECT COUNT(*) FROM employees e2
        WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) AS higher
FROM employees e ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_LIMIT_IN = """
SELECT emp_id FROM employees
WHERE emp_id IN (SELECT e2.emp_id FROM employees e2 ORDER BY e2.salary DESC, e2.emp_id LIMIT 2)
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
tb_df = pd.read_sql_query(SQL_TIEBREAK, con)
rv_df = pd.read_sql_query(SQL_ROWVALUE, con)
print("strict > (ties share a rank):")
print(sql_df.to_string(index=False))
print("\nhow many strictly higher earners in the department, per employee:")
print(pd.read_sql_query(SQL_COUNTS, con).to_string(index=False))
print("\ntie-break by emp_id, rows:", len(tb_df), "ids", tb_df["emp_id"].tolist())
print("row-value tie-break (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id), ids", rv_df["emp_id"].tolist())
print("LIMIT inside an IN subquery runs on SQLite (global top 2, not per group):", [r[0] for r in con.execute(SQL_LIMIT_IN)])

# pd:main
rank_min = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False)     # = (count strictly higher) + 1
pd_ties = emp[rank_min <= 2].sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
           .groupby("dept_id").head(2))
pd_nlargest = emp.groupby("dept_id", group_keys=False).apply(lambda g: g.nlargest(2, "salary", keep="first"))
# pd:end
pairs = int((emp.groupby("dept_id").size() ** 2).sum())
print("\npandas rank(method='min') <= 2 ids:", pd_ties["emp_id"].tolist())
print("pandas sort + groupby.head(2) ids:", pd_head["emp_id"].tolist())
print("pandas groupby nlargest(2, keep='first') ids:", sorted(pd_nlargest["emp_id"].tolist()))
print(f"comparisons the correlated count makes: {pairs} (sum of group size squared) for {len(emp)} rows")

pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_ties.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(tb_df.reset_index(drop=True), pd_head.reset_index(drop=True), check_dtype=False)
assert rv_df["emp_id"].tolist() == tb_df["emp_id"].tolist()
assert sorted(pd_nlargest["emp_id"]) == sorted(tb_df["emp_id"])
print("\nasserts passed: strict-> SQL == rank(method='min'); tie-break SQL == row-value SQL == head(2) == nlargest; compared in dept_id, salary desc, emp_id order")
```

**Output (my run):**
```text
strict > (ties share a rank):
 emp_id  name  dept_id  salary
      1  Asha       10      90
      2   Ben       10      90
      5   Eve       20      80
      6 Farid       20      75
      7  Gita       20      75
      9   Ivy       30      50

how many strictly higher earners in the department, per employee:
 emp_id  dept_id  salary  higher
      1       10      90       0
      2       10      90       0
      3       10      70       2
      4       10      60       3
      5       20      80       0
      6       20      75       1
      7       20      75       1
      8       20      60       3
      9       30      50       0

tie-break by emp_id, rows: 5 ids [1, 2, 5, 6, 9]
row-value tie-break (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id), ids [1, 2, 5, 6, 9]
LIMIT inside an IN subquery runs on SQLite (global top 2, not per group): [1, 2]

pandas rank(method='min') <= 2 ids: [1, 2, 5, 6, 7, 9]
pandas sort + groupby.head(2) ids: [1, 2, 5, 6, 9]
pandas groupby nlargest(2, keep='first') ids: [1, 2, 5, 6, 9]
comparisons the correlated count makes: 33 (sum of group size squared) for 9 rows

asserts passed: strict-> SQL == rank(method='min'); tie-break SQL == row-value SQL == head(2) == nlargest; compared in dept_id, salary desc, emp_id order
```

**Edge cases:**
- **Ties:** strict `>` gives tied people the same count, so they share a rank (SQL's RANK behaviour). A tie across the cutoff returns more than N rows (3 rows in department 20 above). A tie across the whole top is fine (Asha and Ben both 90).
- **Fewer than N rows in a group:** the group returns everything it has (Ivy).
- **NULL salary:** `e2.salary > NULL` is unknown, so a NULL-salary employee has a count of 0 and passes `< 2`, and is treated as top earner. Filter `salary IS NOT NULL` first. I did not run NULL salaries in this table.
- **NULL department:** `e2.dept_id = e.dept_id` never matches NULL, so those rows have count 0 and are all returned. I did not run that here either; filter them.
- **Duplicate `emp_id`:** the tie-break assumes ids are unique.

**Then explain:**
- **Why it works:** a person's rank is 1 plus the number of people ahead of them. "Count below 2" means at most 2 are ahead, so the person is in the top 2 (or tied into it).
- **Cost:** the count runs for every outer row and scans the department, so work grows with the square of the group size. In my run that is 33 comparisons (16 + 16 + 1) for 9 rows. With an index on `(dept_id, salary)` an engine can do better; I did not test this and optimisers differ (not executed).
- **LIMIT inside a per-group subquery is not portable:** you cannot write "LIMIT 2 per department" as a plain inner query, because the inner query would be limited globally. In my run `... IN (SELECT ... ORDER BY salary DESC LIMIT 2)` returned the global top 2 (ids 1 and 2), not top 2 per department. MySQL rejects `LIMIT` inside `IN`/`ALL`/`ANY`/`SOME` subqueries with error 1235 (from its documentation; not executed here); see Q28.
- **pandas:** `groupby("dept_id").head(2)` after sorting is the simplest tie-broken top N. `nlargest(2, "salary", keep="first")` per group is equivalent; `keep="all"` would keep the tied rows. The rank form keeps ties like the SQL count.
- **Window version:** `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id)` is the standard answer, and it is covered in Part 4 (and `RANK` / `DENSE_RANK` there too). The correlated count is the "no windows" answer an interviewer may ask for.

**Follow-ups:**
- *What changes for DENSE_RANK semantics?* Count distinct higher salaries, `COUNT(DISTINCT e2.salary)`, instead of rows. Not run here.
- *How do I get the top 1?* `< 1`, which is Q26.
- *Why not `LIMIT 2` in the correlated subquery?* A scalar subquery can return one value, not two rows. You can use `IN` with a per-row subquery on some engines, but MySQL rejects it (hedged).

**Common mistakes:**
- Using `>=` without noticing that every employee then counts themself, so the cutoff would have to become `<= 2`.
- Not breaking ties and returning 3 rows for a "top 2".
- Forgetting NULL salaries rank as top.
- Believing `LIMIT` inside the subquery limits per department.

### Q28 ⭐⭐ 🟡 Subqueries with LIMIT: customers(customer_id, name) and orders(order_id, customer_id, amount). Show the orders of the top 3 customers by total spend. Write WHERE customer_id IN (SELECT customer_id FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC LIMIT 3), explain that SQLite accepts it, that MySQL rejects LIMIT inside IN, ALL, ANY or SOME subqueries with error 1235 (hedged, not executed) and that a derived-table join is the portable workaround. Cover the tie at rank 3 and ORDER BY determinism, and give pandas nlargest then isin.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Rank customers by `SUM(amount)` in a subquery with `ORDER BY ... DESC LIMIT 3` and keep the orders whose customer is in that list; SQLite accepts the `LIMIT` inside `IN`, MySQL (per its documentation) does not, so the portable form joins to the same query as a derived table, and you must add a tie-breaker because customer 3 and customer 4 tie for third place.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Eve'),(6,'Farid');
INSERT INTO orders VALUES
 (1,1,300),(2,1,200),(3,2,400),(4,3,300),(5,4,100),(6,4,200),(7,5,100);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT order_id, customer_id, amount
FROM orders
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      ORDER BY SUM(amount) DESC, customer_id
                      LIMIT 3)
ORDER BY order_id
```
The portable derived-table join (`SQL_DERIVED`):
```sql
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN (SELECT customer_id
      FROM orders
      GROUP BY customer_id
      ORDER BY SUM(amount) DESC, customer_id
      LIMIT 3) top3 ON top3.customer_id = o.customer_id
ORDER BY o.order_id
```
Tie-inclusive: every customer whose total is at least the third-highest total (`SQL_TIES`):
```sql
WITH spend AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN spend s ON s.customer_id = o.customer_id
WHERE s.total >= (SELECT total FROM spend ORDER BY total DESC LIMIT 1 OFFSET 2)
ORDER BY o.order_id
```

**pandas answer:** aggregate, take the top three with an explicit tie-break, then `isin`; `nlargest(..., keep="all")` is the tie-inclusive form.
```python
totals = orders.groupby("customer_id")["amount"].sum().reset_index()
top3 = totals.sort_values(["amount", "customer_id"], ascending=[False, True]).head(3)     # tie-break by id
pd_df = orders[orders["customer_id"].isin(top3["customer_id"])].sort_values("order_id").reset_index(drop=True)
tie_ids = totals.set_index("customer_id")["amount"].nlargest(3, keep="all").index     # keep every tie at rank 3
pd_ties = orders[orders["customer_id"].isin(tie_ids)].sort_values("order_id").reset_index(drop=True)
```

**Example:**
- Totals: Asha 300 + 200 = 500, Ben 400, Chitra 300, Dev 100 + 200 = 300, Eve 100, Farid no orders.
- Ranked by total: Asha 500, Ben 400, then Chitra and Dev tied at 300, then Eve 100.
- `ORDER BY SUM(amount) DESC, customer_id LIMIT 3` picks Asha, Ben, and Chitra (the tie goes to the smaller id). The outer query returns their orders: 1, 2 (Asha), 3 (Ben), 4 (Chitra).
- The tie-inclusive query uses the third-highest total, 300 (`OFFSET 2`), and keeps everyone with a total of at least 300: Asha, Ben, Chitra and Dev. That adds Dev's orders 5 and 6.
- Without the `customer_id` tie-break, my run picked Dev (customers 1, 2, 4), not Chitra. Both are valid answers to the SQL as written, which is the point.

**Code:** run with `python3 -I`.
```python
# Q28: orders of the top 3 customers by total spend: LIMIT inside IN, derived-table join, tie at rank 3
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Eve'),(6,'Farid');
INSERT INTO orders VALUES
 (1,1,300),(2,1,200),(3,2,400),(4,3,300),(5,4,100),(6,4,200),(7,5,100);
"""
SQL_MAIN = """
SELECT order_id, customer_id, amount
FROM orders
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      ORDER BY SUM(amount) DESC, customer_id
                      LIMIT 3)
ORDER BY order_id
"""
SQL_DERIVED = """
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN (SELECT customer_id
      FROM orders
      GROUP BY customer_id
      ORDER BY SUM(amount) DESC, customer_id
      LIMIT 3) top3 ON top3.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_TIES = """
WITH spend AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN spend s ON s.customer_id = o.customer_id
WHERE s.total >= (SELECT total FROM spend ORDER BY total DESC LIMIT 1 OFFSET 2)
ORDER BY o.order_id
"""
SQL_NO_TIEBREAK = """
SELECT customer_id FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC LIMIT 3
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("totals per customer:", con.execute(
    "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC, customer_id").fetchall())

sql_df = pd.read_sql_query(SQL_MAIN, con)
der_df = pd.read_sql_query(SQL_DERIVED, con)
ties_df = pd.read_sql_query(SQL_TIES, con)
print("\nIN (... LIMIT 3), tie broken by customer_id:")
print(sql_df.to_string(index=False))
print("derived-table join gives the same rows:", sql_df.equals(der_df))
print("tie-inclusive (total >= third-highest total) customers:", sorted(ties_df["customer_id"].unique().tolist()))
print("without the customer_id tie-break the rank-3 pick is left to the engine; this run chose:",
      [r[0] for r in con.execute(SQL_NO_TIEBREAK)])

print("\nLIMIT / OFFSET forms on SQLite 3.45:")
print("  LIMIT 1+1 OFFSET 4/2        ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT 1+1 OFFSET 4/2")])
print("  LIMIT -1 OFFSET 5           ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT -1 OFFSET 5")])
print("  LIMIT (SELECT 2)            ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT (SELECT 2)")])
try:
    con.execute("SELECT order_id FROM orders ORDER BY order_id OFFSET 1").fetchall()
except sqlite3.Error as e:
    print("  OFFSET without LIMIT        -> error:", e)

# pd:main
totals = orders.groupby("customer_id")["amount"].sum().reset_index()
top3 = totals.sort_values(["amount", "customer_id"], ascending=[False, True]).head(3)     # tie-break by id
pd_df = orders[orders["customer_id"].isin(top3["customer_id"])].sort_values("order_id").reset_index(drop=True)
tie_ids = totals.set_index("customer_id")["amount"].nlargest(3, keep="all").index     # keep every tie at rank 3
pd_ties = orders[orders["customer_id"].isin(tie_ids)].sort_values("order_id").reset_index(drop=True)
# pd:end
print("\npandas nlargest(3, keep='all') customers:", sorted(tie_ids.tolist()))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(ties_df, pd_ties, check_dtype=False)
assert sorted(sql_df["customer_id"].unique()) == [1, 2, 3] and sorted(ties_df["customer_id"].unique()) == [1, 2, 3, 4]
print("\nasserts passed: SQL IN(LIMIT) == derived join == pandas (customers 1, 2, 3); tie-inclusive == nlargest(keep='all') (1, 2, 3, 4); compared by order_id")
```

**Output (my run):**
```text
totals per customer: [(1, 500), (2, 400), (3, 300), (4, 300), (5, 100)]

IN (... LIMIT 3), tie broken by customer_id:
 order_id  customer_id  amount
        1            1     300
        2            1     200
        3            2     400
        4            3     300
derived-table join gives the same rows: True
tie-inclusive (total >= third-highest total) customers: [1, 2, 3, 4]
without the customer_id tie-break the rank-3 pick is left to the engine; this run chose: [1, 2, 4]

LIMIT / OFFSET forms on SQLite 3.45:
  LIMIT 1+1 OFFSET 4/2        -> [3, 4]
  LIMIT -1 OFFSET 5           -> [6, 7]
  LIMIT (SELECT 2)            -> [1, 2]
  OFFSET without LIMIT        -> error: near "OFFSET": syntax error

pandas nlargest(3, keep='all') customers: [1, 2, 3, 4]

asserts passed: SQL IN(LIMIT) == derived join == pandas (customers 1, 2, 3); tie-inclusive == nlargest(keep='all') (1, 2, 3, 4); compared by order_id
```

**Edge cases:**
- **Tie at rank 3:** `LIMIT 3` must cut somewhere. Decide: arbitrary (bad), deterministic with a tie-break (my `SQL_MAIN`), or include all tied customers (`SQL_TIES`, 4 customers, 6 orders in my run). pandas: `nlargest(3, keep="first")` or `keep="all"`.
- **Non-deterministic ORDER BY:** with only `ORDER BY SUM(amount) DESC`, which tied customer wins depends on the plan. Always end the `ORDER BY` with a unique column.
- **Fewer than 3 customers:** `LIMIT 3` returns what exists.
- **Customers without orders (Farid):** they have no rows in `orders`, so they cannot rank. If you want them in a ranking, start from `customers` with a LEFT JOIN.
- **NULL customer_id orders:** the NULL group is a group in `GROUP BY` and could rank in the top 3; the outer `IN` then never matches it. I did not include such a row here, so filter `customer_id IS NOT NULL` in the subquery if you may have them.
- **LIMIT with expressions:** on SQLite 3.45, `LIMIT 1+1 OFFSET 4/2` ran (rows 3 and 4), `LIMIT -1 OFFSET 5` ran (a negative limit means no limit; rows 6 and 7), `LIMIT (SELECT 2)` ran, and `OFFSET` without `LIMIT` is a syntax error. Other engines differ (for example, PostgreSQL allows `OFFSET` alone); not executed here.

**Then explain:**
- **What the subquery returns:** a list of three ids. `IN` then keeps the orders of those customers. A subquery with `GROUP BY ... ORDER BY aggregate ... LIMIT n` is the standard "top N entities" pattern.
- **MySQL (hedged, not executed here):** its documentation says `LIMIT` is not supported inside `IN`, `ALL`, `ANY` or `SOME` subqueries (error 1235). The workaround is the derived-table join, which my run shows returns exactly the same rows as the `IN` form on SQLite.
- **Other engines:** PostgreSQL's subquery documentation does not forbid it as far as I read it, but I did not run PostgreSQL, BigQuery or Snowflake here, so I would test it on the target engine.
- **Tie rule:** "top 3" is ambiguous when there is a tie. Ask the interviewer, then say which you chose.
- **pandas:** `groupby().sum()` then `nlargest`, then `isin`. The `isin` is the `IN`, the `nlargest` is the `ORDER BY ... LIMIT`. `nlargest` defaults to `keep="first"`, which resolves ties by position, but I did not run that form, so I used an explicit sort on `(amount, customer_id)` for the tie-break.
- **Window version:** `DENSE_RANK() OVER (ORDER BY total DESC) <= 3` is in Part 4.

**Follow-ups:**
- *Why the derived table in MySQL?* It turns the limited subquery into a table that is joined, not a list tested with `IN`.
- *How do I get the top 3 per region?* That is top-N per group, Q27 and Part 4.
- *What if two customers tie for first?* They take ranks 1 and 1, and with `LIMIT 3` you may only get one of the tied rank-3 customers.

**Common mistakes:**
- Leaving out the tie-breaker, then wondering why the answer changes between runs or engines.
- Putting `LIMIT 3` on the outer query, which returns three orders, not the orders of three customers.
- Using `SUM` per order row without `GROUP BY` in the subquery.
- Assuming `LIMIT` inside `IN` works everywhere.

### Q29 ⭐⭐ 🟡 CTE scaffolding for a cohort-style question (scaffolding only; retention logic is Part 6): orders(order_id, customer_id, order_date, amount) with ISO date strings. Using chained CTEs, compute each customer's first order date, label every order as 'first' or 'repeat', and count new versus repeat customers per month (strftime). Explain why each CTE has one purpose and one grain, how to check grain with COUNT(*) versus COUNT(DISTINCT customer_id), and give the pandas groupby/transform('min') version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build it in layers: one CTE gives each customer's first order date (one row per customer), the next labels every order `first` or `repeat` by comparing its date with that first date (one row per order), and the last counts distinct customers per month and label; each layer has one job and one grain, which I check with `COUNT(*)` against `COUNT(DISTINCT customer_id)`.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',20),(2,1,'2024-01-20',30),(3,2,'2024-01-25',40),
 (4,1,'2024-02-03',10),(5,2,'2024-02-10',25),
 (6,3,'2024-02-15',60),(7,3,'2024-02-15',15),
 (8,4,'2024-03-01',35),(9,1,'2024-03-09',50);
```
Customer 3 has two orders on the same first day, which is the one grain trap in the data.

**SQL answer:** `SQL_MAIN` in the Code block (scaffolding only; retention curves are Part 6).
```sql
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders
  GROUP BY customer_id
),
labelled AS (
  SELECT o.order_id, o.customer_id, strftime('%Y-%m', o.order_date) AS order_month,
         CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o
  JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT order_month,
       COUNT(DISTINCT CASE WHEN label = 'first'  THEN customer_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN label = 'repeat' THEN customer_id END) AS repeat_customers
FROM labelled
GROUP BY order_month
ORDER BY order_month
```
The grain check, `SQL_GRAIN`, is also in the Code block.
```sql
WITH first_order AS (SELECT customer_id, MIN(order_date) AS first_date FROM orders GROUP BY customer_id),
labelled AS (
  SELECT o.order_id, o.customer_id, CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT 'first_order' AS cte, COUNT(*) AS n_rows, COUNT(DISTINCT customer_id) AS n_customers FROM first_order
UNION ALL SELECT 'labelled', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled
UNION ALL SELECT 'labelled first rows', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled WHERE label = 'first'
UNION ALL SELECT 'orders', COUNT(*), COUNT(DISTINCT customer_id) FROM orders
```

**pandas answer:** `transform("min")` is the `first_order` CTE joined back onto every order in one step.
```python
o = orders.assign(first_date=orders.groupby("customer_id")["order_date"].transform("min"),
                  order_month=orders["order_date"].str[:7])
o["label"] = (o["order_date"] == o["first_date"]).map({True: "first", False: "repeat"})
new_c = o[o["label"] == "first"].groupby("order_month")["customer_id"].nunique()
rep_c = o[o["label"] == "repeat"].groupby("order_month")["customer_id"].nunique()
pd_df = (pd.DataFrame({"new_customers": new_c, "repeat_customers": rep_c})
         .fillna(0).astype("int64").rename_axis("order_month").reset_index())
```

**Example:**
- `first_order`: customer 1 first on 2024-01-05, customer 2 on 2024-01-25, customer 3 on 2024-02-15, customer 4 on 2024-03-01. 4 rows, 4 customers.
- `labelled`: orders 1, 3, 6, 7, 8 are `first` (their date equals the customer's first date; order 7 ties with order 6 on 2024-02-15). Orders 2, 4, 5, 9 are `repeat`. 9 rows, 4 customers.
- January: new customers are 1 and 2 (2). Customer 1 also ordered again on 2024-01-20, which is a repeat order in the same month, so repeat customers = 1.
- February: new is customer 3 (1; two rows, one customer). Repeat customers: 1 (order 4) and 2 (order 5) = 2.
- March: new is customer 4 (1), repeat is customer 1 (order 9) = 1.
- So the table is (Jan 2, 1), (Feb 1, 2), (Mar 1, 1). A customer can be both new and repeat in their first month.
- Counting rows instead would give February `new = 2`, because both of customer 3's same-day orders are labelled `first`. The distinct count prevents that.

**Code:** run with `python3 -I`.
```python
# Q29: chained CTEs: first order date, first/repeat label, new vs repeat customers per month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',20),(2,1,'2024-01-20',30),(3,2,'2024-01-25',40),
 (4,1,'2024-02-03',10),(5,2,'2024-02-10',25),
 (6,3,'2024-02-15',60),(7,3,'2024-02-15',15),
 (8,4,'2024-03-01',35),(9,1,'2024-03-09',50);
"""
SQL_MAIN = """
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders
  GROUP BY customer_id
),
labelled AS (
  SELECT o.order_id, o.customer_id, strftime('%Y-%m', o.order_date) AS order_month,
         CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o
  JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT order_month,
       COUNT(DISTINCT CASE WHEN label = 'first'  THEN customer_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN label = 'repeat' THEN customer_id END) AS repeat_customers
FROM labelled
GROUP BY order_month
ORDER BY order_month
"""
SQL_GRAIN = """
WITH first_order AS (SELECT customer_id, MIN(order_date) AS first_date FROM orders GROUP BY customer_id),
labelled AS (
  SELECT o.order_id, o.customer_id, CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT 'first_order' AS cte, COUNT(*) AS n_rows, COUNT(DISTINCT customer_id) AS n_customers FROM first_order
UNION ALL SELECT 'labelled', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled
UNION ALL SELECT 'labelled first rows', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled WHERE label = 'first'
UNION ALL SELECT 'orders', COUNT(*), COUNT(DISTINCT customer_id) FROM orders
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
orders = pd.read_sql_query("SELECT * FROM orders", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("new vs repeat customers per month (SQL):")
print(sql_df.to_string(index=False))
print("\ngrain check (rows vs distinct customers):")
print(pd.read_sql_query(SQL_GRAIN, con).to_string(index=False))

# pd:main
o = orders.assign(first_date=orders.groupby("customer_id")["order_date"].transform("min"),
                  order_month=orders["order_date"].str[:7])
o["label"] = (o["order_date"] == o["first_date"]).map({True: "first", False: "repeat"})
new_c = o[o["label"] == "first"].groupby("order_month")["customer_id"].nunique()
rep_c = o[o["label"] == "repeat"].groupby("order_month")["customer_id"].nunique()
pd_df = (pd.DataFrame({"new_customers": new_c, "repeat_customers": rep_c})
         .fillna(0).astype("int64").rename_axis("order_month").reset_index())
# pd:end
print("\npandas version:")
print(pd_df.to_string(index=False))
print("\nlabelled orders per label:", o["label"].value_counts().to_dict())

# compared after ordering both by order_month
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert o["first_date"].notna().all() and len(o) == len(orders) == 9
assert o.loc[o["label"] == "first", "customer_id"].nunique() == 4 and (o["label"] == "first").sum() == 5
print("\nasserts passed: SQL == pandas (4 customers, 5 rows labelled 'first' because customer 3 has two orders on the first day)")
```

**Output (my run):**
```text
new vs repeat customers per month (SQL):
order_month  new_customers  repeat_customers
    2024-01              2                 1
    2024-02              1                 2
    2024-03              1                 1

grain check (rows vs distinct customers):
                cte  n_rows  n_customers
        first_order       4            4
           labelled       9            4
labelled first rows       5            4
             orders       9            4

pandas version:
order_month  new_customers  repeat_customers
    2024-01              2                 1
    2024-02              1                 2
    2024-03              1                 1

labelled orders per label: {'first': 5, 'repeat': 4}

asserts passed: SQL == pandas (4 customers, 5 rows labelled 'first' because customer 3 has two orders on the first day)
```

**Edge cases:**
- **Same-day first orders:** the `first` label is on the order, not the customer, so customer 3 has 2 `first` rows (5 `first` rows for 4 customers in my run). Count customers with `COUNT(DISTINCT customer_id)`. If you need exactly one first order per customer, add a tie-break on `order_id` (a window function in Part 4).
- **Month with no repeat customers:** the `COUNT(DISTINCT CASE ...)` form returns 0, not a missing row. In pandas the two series do not line up, so the frame is built from both and `fillna(0)` fills the gap; I used `astype("int64")` afterwards.
- **A month with no orders at all:** it does not appear in either result. A calendar table or a generated series would be needed; not done here.
- **NULL dates or customers:** `MIN(order_date)` ignores NULLs. A NULL `order_date` gives `strftime` NULL, a NULL month group. A NULL `customer_id` forms its own group in `first_order`, and the join `f.customer_id = o.customer_id` drops it (and in pandas `groupby` drops NaN keys, so `transform` gives NaN). I did not put NULLs in this table.
- **Date format:** ISO strings (`YYYY-MM-DD`) sort correctly as text, so `MIN` works. Other formats (`DD/MM/YYYY`) do not.

**Then explain:**
- **One purpose, one grain:** `first_order` is one row per customer. `labelled` is one row per order. The last select is one row per month. When a result has the wrong number of rows, you can find which layer broke the grain.
- **Grain check:** `COUNT(*)` versus `COUNT(DISTINCT customer_id)` on each CTE (printed above). For `first_order` they must be equal (4 and 4), for `labelled` the row count must equal the orders table (9). If a join step makes `labelled` bigger than `orders`, a key was not unique.
- **Why CTEs here:** each can be selected alone while debugging, and the names document the logic. The same query as nested subqueries would work and return the same rows; I did not time either (see the follow-up below).
- **pandas:** `groupby("customer_id")["order_date"].transform("min")` repeats the customer's min date on every order row, so no merge is needed. Then `nunique` per month and label.
- **strftime:** `strftime('%Y-%m', date)` is SQLite. PostgreSQL uses `TO_CHAR` or `DATE_TRUNC`, MySQL `DATE_FORMAT`, BigQuery `FORMAT_DATE` (from memory, not executed here).

**Follow-ups:**
- *Is a CTE faster than a subquery?* Not by itself. SQLite's documentation says the `MATERIALIZED` and `NOT MATERIALIZED` hints exist (3.35+) and are not binding. I did not measure it.
- *How would this become retention?* Join each order to the cohort month of its customer and count months since first order: Part 6.
- *What if the first order is on a later day than the first signup?* Then the cohort is defined by signup, not by order; use that table instead.

**Common mistakes:**
- Counting rows (`COUNT(*)`) instead of distinct customers and double counting same-day first orders.
- Joining `first_order` on something that is not unique.
- Comparing dates stored as text in a non-ISO format.
- Putting everything in one 40-line query so no layer can be checked alone.

### Q30 ⭐⭐ 🟡 CTE scaffolding for a funnel-style question (scaffolding only; funnel metrics are Part 8): events(user_id, event_name, event_time) with names 'view', 'cart', 'purchase'. With one CTE per step (users who viewed, users who carted, users who purchased) and joins, count users at each step and the step-to-step conversion. Explain why a CTE of DISTINCT users per step avoids double counting, that step order is ignored by this simple version, and give pandas sets or isin. Note that ordering within a session is a later part.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Make one CTE per step holding the DISTINCT users who did it, chain them with LEFT JOINs from the first step so each later step only counts users who passed the earlier ones, count each column, and divide for conversion; DISTINCT users per step is what stops a user with two views and two carts from counting four times.

**Schema and sample data:**
```sql
CREATE TABLE events(user_id INTEGER, event_name TEXT, event_time TEXT);
INSERT INTO events VALUES
 (1,'view','2024-05-01 09:00'),(1,'cart','2024-05-01 09:05'),(1,'purchase','2024-05-01 09:10'),
 (2,'view','2024-05-01 10:00'),(2,'cart','2024-05-01 10:02'),
 (3,'view','2024-05-01 11:00'),
 (4,'view','2024-05-01 12:00'),(4,'view','2024-05-01 12:01'),(4,'cart','2024-05-01 12:03'),(4,'cart','2024-05-01 12:04'),
 (5,'cart','2024-05-01 13:00'),
 (6,'purchase','2024-05-01 08:00'),(6,'cart','2024-05-01 08:30'),(6,'view','2024-05-01 09:00');
```
User 4 repeats events, user 5 carted without viewing, and user 6 did all three steps but in the wrong order.

**SQL answer:** `SQL_MAIN` in the Code block (scaffolding only; real funnel metrics are Part 8).
```sql
WITH viewed AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'view'),
     carted AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'cart'),
     bought AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'purchase'),
     steps AS (
       SELECT v.user_id AS viewer, c.user_id AS carter, b.user_id AS buyer
       FROM viewed v
       LEFT JOIN carted c ON c.user_id = v.user_id
       LEFT JOIN bought b ON b.user_id = c.user_id
     ),
     counts AS (
       SELECT COUNT(viewer) AS viewed_users, COUNT(carter) AS carted_users, COUNT(buyer) AS bought_users
       FROM steps
     )
SELECT viewed_users, carted_users, bought_users,
       ROUND(1.0 * carted_users / viewed_users, 3) AS view_to_cart,
       ROUND(1.0 * bought_users / carted_users, 3) AS cart_to_buy,
       ROUND(1.0 * bought_users / viewed_users, 3) AS view_to_buy
FROM counts
```
The naive join that double counts (`SQL_NAIVE`) and a time-ordered check (`SQL_ORDERED`) are in the Code block too.
```sql
SELECT COUNT(*) AS joined_rows, COUNT(DISTINCT v.user_id) AS distinct_users
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'
WHERE v.event_name = 'view'
```

**pandas answer:** sets of user ids per step, intersected in funnel order; the `isin` form is the same count.
```python
viewed = set(events.loc[events["event_name"] == "view", "user_id"])
carted = set(events.loc[events["event_name"] == "cart", "user_id"])
bought = set(events.loc[events["event_name"] == "purchase", "user_id"])
n_view = len(viewed)
n_cart = len(viewed & carted)
n_buy = len(viewed & carted & bought)
pd_df = pd.DataFrame({"viewed_users": [n_view], "carted_users": [n_cart], "bought_users": [n_buy],
                      "view_to_cart": [round(n_cart / n_view, 3)], "cart_to_buy": [round(n_buy / n_cart, 3)],
                      "view_to_buy": [round(n_buy / n_view, 3)]})
# same counts with isin on distinct users
v = events.loc[events["event_name"] == "view", "user_id"].drop_duplicates()
c = events.loc[events["event_name"] == "cart", "user_id"].drop_duplicates()
b = events.loc[events["event_name"] == "purchase", "user_id"].drop_duplicates()
n_cart2 = int(c.isin(v).sum())
n_buy2 = int(b[b.isin(v) & b.isin(c)].shape[0])
```

**Example:**
- Distinct users per step: viewers 1, 2, 3, 4, 6 (5 users); carters 1, 2, 4, 5, 6 (5 users); purchasers 1, 6 (2 users).
- Step 1: 5 viewers.
- Step 2: viewers who also carted are 1, 2, 4, 6. User 3 never carted and user 5 never viewed, so 4. view-to-cart is 4 / 5 = 0.8.
- Step 3: carters among those who bought are 1 and 6, so 2. cart-to-buy is 2 / 4 = 0.5; view-to-buy is 2 / 5 = 0.4.
- Without the per-step DISTINCT: user 4 has 2 view rows and 2 cart rows, so a direct join of view rows to cart rows gives 4 rows for that one user. The naive join returned 7 rows for 4 users in my run (users 1, 2, 6 contribute 1 row each, user 4 contributes 4).
- Order is ignored: user 6 purchased at 08:00, carted at 08:30 and viewed at 09:00, yet counts as a full funnel user. With `view < cart < purchase` time conditions only 1 user (user 1) qualifies in my run, so the simple version reports 2.

**Code:** run with `python3 -I`.
```python
# Q30: funnel scaffolding: one CTE of DISTINCT users per step, joined, with step-to-step conversion
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_name TEXT, event_time TEXT);
INSERT INTO events VALUES
 (1,'view','2024-05-01 09:00'),(1,'cart','2024-05-01 09:05'),(1,'purchase','2024-05-01 09:10'),
 (2,'view','2024-05-01 10:00'),(2,'cart','2024-05-01 10:02'),
 (3,'view','2024-05-01 11:00'),
 (4,'view','2024-05-01 12:00'),(4,'view','2024-05-01 12:01'),(4,'cart','2024-05-01 12:03'),(4,'cart','2024-05-01 12:04'),
 (5,'cart','2024-05-01 13:00'),
 (6,'purchase','2024-05-01 08:00'),(6,'cart','2024-05-01 08:30'),(6,'view','2024-05-01 09:00');
"""
SQL_MAIN = """
WITH viewed AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'view'),
     carted AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'cart'),
     bought AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'purchase'),
     steps AS (
       SELECT v.user_id AS viewer, c.user_id AS carter, b.user_id AS buyer
       FROM viewed v
       LEFT JOIN carted c ON c.user_id = v.user_id
       LEFT JOIN bought b ON b.user_id = c.user_id
     ),
     counts AS (
       SELECT COUNT(viewer) AS viewed_users, COUNT(carter) AS carted_users, COUNT(buyer) AS bought_users
       FROM steps
     )
SELECT viewed_users, carted_users, bought_users,
       ROUND(1.0 * carted_users / viewed_users, 3) AS view_to_cart,
       ROUND(1.0 * bought_users / carted_users, 3) AS cart_to_buy,
       ROUND(1.0 * bought_users / viewed_users, 3) AS view_to_buy
FROM counts
"""
SQL_NAIVE = """
SELECT COUNT(*) AS joined_rows, COUNT(DISTINCT v.user_id) AS distinct_users
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'
WHERE v.event_name = 'view'
"""
SQL_ORDERED = """
SELECT COUNT(DISTINCT v.user_id)
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'  AND c.event_time > v.event_time
JOIN events p ON p.user_id = v.user_id AND p.event_name = 'purchase' AND p.event_time > c.event_time
WHERE v.event_name = 'view'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
events = pd.read_sql_query("SELECT * FROM events", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("funnel (SQL):")
print(sql_df.to_string(index=False))
print("\nnaive join of raw event rows (view x cart):", con.execute(SQL_NAIVE).fetchone(), "(joined_rows, distinct_users)")
print("distinct users who did cart at all:", con.execute("SELECT COUNT(DISTINCT user_id) FROM events WHERE event_name='cart'").fetchone()[0],
      "| carted AND viewed:", sql_df.loc[0, "carted_users"])
print("users whose view < cart < purchase times are in order:", con.execute(SQL_ORDERED).fetchone()[0], "(simple version counts", sql_df.loc[0, "bought_users"], ")")

# pd:main
viewed = set(events.loc[events["event_name"] == "view", "user_id"])
carted = set(events.loc[events["event_name"] == "cart", "user_id"])
bought = set(events.loc[events["event_name"] == "purchase", "user_id"])
n_view = len(viewed)
n_cart = len(viewed & carted)
n_buy = len(viewed & carted & bought)
pd_df = pd.DataFrame({"viewed_users": [n_view], "carted_users": [n_cart], "bought_users": [n_buy],
                      "view_to_cart": [round(n_cart / n_view, 3)], "cart_to_buy": [round(n_buy / n_cart, 3)],
                      "view_to_buy": [round(n_buy / n_view, 3)]})
# same counts with isin on distinct users
v = events.loc[events["event_name"] == "view", "user_id"].drop_duplicates()
c = events.loc[events["event_name"] == "cart", "user_id"].drop_duplicates()
b = events.loc[events["event_name"] == "purchase", "user_id"].drop_duplicates()
n_cart2 = int(c.isin(v).sum())
n_buy2 = int(b[b.isin(v) & b.isin(c)].shape[0])
# pd:end
print("\npandas sets:")
print(pd_df.to_string(index=False))
print("pandas isin counts:", len(v), n_cart2, n_buy2)

# single row, compared column by column
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert (len(v), n_cart2, n_buy2) == (5, 4, 2)
print("\nasserts passed: SQL == pandas sets == isin counts (5 viewers, 4 carted, 2 purchased)")
```

**Output (my run):**
```text
funnel (SQL):
 viewed_users  carted_users  bought_users  view_to_cart  cart_to_buy  view_to_buy
            5             4             2           0.8          0.5          0.4

naive join of raw event rows (view x cart): (7, 4) (joined_rows, distinct_users)
distinct users who did cart at all: 5 | carted AND viewed: 4
users whose view < cart < purchase times are in order: 1 (simple version counts 2 )

pandas sets:
 viewed_users  carted_users  bought_users  view_to_cart  cart_to_buy  view_to_buy
            5             4             2           0.8          0.5          0.4
pandas isin counts: 5 4 2

asserts passed: SQL == pandas sets == isin counts (5 viewers, 4 carted, 2 purchased)
```

**Edge cases:**
- **Repeated events:** `SELECT DISTINCT user_id` per step removes them; the grain of each step CTE is one row per user. In pandas, `drop_duplicates` or a set does the same.
- **Skipped steps:** user 5 carted without a view. Joining from `viewed` leaves them out of the cart step, so the funnel is "of the viewers". If you want raw reach per step, count each CTE alone (5 carters in my run, versus 4 in the funnel).
- **Order:** the simple version asks "did the user ever do each thing". It does not know about order or time windows (see `SQL_ORDERED`, which uses text comparison on ISO timestamps). Sessions and ordering belong to Part 8 and Part 7.
- **Empty step:** if no one purchased, `COUNT(buyer)` is 0 and `cart_to_buy` is 0 (fine). If no one carted, `bought_users / carted_users` would divide by zero (SQLite returns NULL for division by zero; I did not run that case) and pandas would raise or return inf for a float division; guard with `NULLIF` or an `if`.
- **Duplicate users in the join:** the join key `user_id` is unique in each CTE, so no step can multiply the rows.

**Then explain:**
- **Why DISTINCT users:** the question is "how many people", not "how many events". Events are many per user; the CTE brings each step to the grain of one row per user before any join (same principle as Q29 and Part 2 Q13).
- **Why LEFT JOIN from step 1:** it keeps everyone who viewed and shows NULL where a later step is missing, so `COUNT(column)` counts only the non-NULL ones. The purchase join is on `c.user_id` so only users who carted are looked up.
- **Conversion:** step-to-step is this step over the previous step; overall is the last over the first. Multiply by `1.0` so the division is not integer division in SQLite.
- **Limits of the simple version:** order ignored, no time window, no sessions, no unique-per-day definition. These are real funnel work and are Part 8.
- **pandas:** sets are the most readable form for three steps. For more steps, `isin` with chained boolean filters or a pivot of event flags per user scales better.
- **Name check:** the event names are exact strings. A misspelt `'purchase'` gives an empty step, not an error.

**Follow-ups:**
- *How would you enforce the order?* Join step tables on time, `c.event_time > v.event_time`, as in `SQL_ORDERED` (executed in the Code block); sessionisation needs window functions (later parts).
- *Why not just `COUNT(DISTINCT user_id)` with `CASE`?* You can: `COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)` for each step. That counts raw reach per step, not the funnel of viewers, unless you intersect.
- *What about a time window of 24 hours?* Add the time difference to the join; date arithmetic differs by engine (not executed here).

**Common mistakes:**
- Joining raw event tables, which multiplies rows for users with repeated events.
- Counting events instead of users.
- Dividing integers in SQLite (`3 / 4` is 0) instead of using `1.0 *`.
- Reporting the simple version as if it respected order.

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

