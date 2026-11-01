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
