### Q13 ⭐⭐⭐ 🟡 NOT IN with NULL: customers(customer_id, name) and orders(order_id, customer_id) where orders.customer_id can be NULL for guest checkouts. Write 'customers who have never ordered' with NOT IN and show it returns zero rows when the subquery contains a NULL; explain it with three-valued logic and fix it with NOT EXISTS or a NOT NULL filter in the subquery. (Subqueries are Part 3 and anti-joins Part 2; the point here is the NULL trap.) Show the pandas ~isin result, and what pandas does with NaN in isin.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `NOT IN` returns zero rows as soon as the subquery contains one NULL, because `x NOT IN (1, 2, NULL)` can never be TRUE; use `NOT EXISTS`, or filter the NULLs out of the subquery.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);  -- NULL = guest checkout
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,NULL);
```

**SQL answer:** three queries are in the Code block: `sql_not_in` (the trap), `sql_not_in_filtered` (NOT NULL filter inside the subquery) and `sql_not_exists` (the safe default).

**pandas answer:** `customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"]`, shown in the Code block as `p_not_in`.

**Example:** Customers 1 to 4, orders belong to customers 1, 1, 2 and one guest (NULL). The real answer is Chitra (3) and Dev (4). For customer 3 the predicate is `NOT (3 = 1 OR 3 = 2 OR 3 = NULL)`. That is `NOT (FALSE OR FALSE OR UNKNOWN)`, which is `NOT UNKNOWN`, which is UNKNOWN. `WHERE` keeps only TRUE, so Chitra is dropped. Customer 4 is the same. Customers 1 and 2 give FALSE. No row can ever be TRUE, so the result is empty.

**Code:** run with `python3 -I`.
```python
# NOT IN with a NULL in the subquery: SQL result, the fixes, and what pandas isin does with NaN.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);  -- NULL = guest checkout
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,NULL);
""")

sql_not_in = "SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders) ORDER BY customer_id"
sql_not_in_filtered = ("SELECT name FROM customers WHERE customer_id NOT IN "
                       "(SELECT customer_id FROM orders WHERE customer_id IS NOT NULL) ORDER BY customer_id")
sql_not_exists = ("SELECT c.name FROM customers c WHERE NOT EXISTS "
                  "(SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id")

def run(q): return [r[0] for r in con.execute(q).fetchall()]
print("NOT IN (subquery has a NULL):", run(sql_not_in))
print("NOT IN with IS NOT NULL filter:", run(sql_not_in_filtered))
print("NOT EXISTS:", run(sql_not_exists))
print("3 NOT IN (1, 2, NULL) ->", con.execute("SELECT 3 NOT IN (1,2,NULL)").fetchone()[0])
print("1 NOT IN (1, 2, NULL) ->", con.execute("SELECT 1 NOT IN (1,2,NULL)").fetchone()[0])
print("3 NOT IN (1, 2)       ->", con.execute("SELECT 3 NOT IN (1,2)").fetchone()[0])

# pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
print("orders.customer_id dtype:", orders["customer_id"].dtype, "(NULL became NaN, ints became float)")
p_not_in = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
print("pandas ~isin:", p_not_in)

# isin and NaN: NaN matches NaN, so a NaN key on the left WOULD be treated as 'found'
left = pd.Series([1.0, 3.0, np.nan])
print("isin with NaN in values:", left.isin([1.0, np.nan]).tolist())

# the pandas result matches the NOT EXISTS result (compare as lists, ordered by customer_id)
assert p_not_in == run(sql_not_exists) == run(sql_not_in_filtered) == ["Chitra", "Dev"]
assert run(sql_not_in) == []

# NOT IN with NULL filtered out explicitly in pandas gives the same thing
ids = orders["customer_id"].dropna()
assert customers.loc[~customers["customer_id"].isin(ids), "name"].tolist() == p_not_in
print("asserts passed")
```

**Output (my run):**
```text
NOT IN (subquery has a NULL): []
NOT IN with IS NOT NULL filter: ['Chitra', 'Dev']
NOT EXISTS: ['Chitra', 'Dev']
3 NOT IN (1, 2, NULL) -> None
1 NOT IN (1, 2, NULL) -> 0
3 NOT IN (1, 2)       -> 1
orders.customer_id dtype: float64 (NULL became NaN, ints became float)
pandas ~isin: ['Chitra', 'Dev']
isin with NaN in values: [True, False, True]
asserts passed
```

**Edge cases:**
- The NULL only has to appear once, and it only matters in a `NOT IN` (or `<> ALL`). A positive `IN` still works: `1 IN (1, 2, NULL)` is TRUE, while `3 IN (1, 2, NULL)` is UNKNOWN (not TRUE, so the row is not returned, which happens to be the answer you wanted).
- If the subquery returns no rows at all, `NOT IN` returns every customer.
- If the left-hand value is itself NULL, `NULL NOT IN (...)` is UNKNOWN for any non-empty list, so that row is also dropped.
- Duplicates in the subquery do not matter.

**Then explain:**
- **Three-valued logic:** comparisons with NULL give UNKNOWN, not FALSE. `NOT UNKNOWN` is UNKNOWN. `WHERE` keeps only TRUE.
- **Why NOT EXISTS is safe:** the correlated test `o.customer_id = c.customer_id` is UNKNOWN for the guest row, `EXISTS` just sees "no matching row", and `NOT EXISTS` returns TRUE.
- **Alternatives:** filter the subquery with `WHERE customer_id IS NOT NULL`, or use a LEFT JOIN ... IS NULL anti-join (Part 2). I recommend `NOT EXISTS` because it does not break when someone later adds NULLs.
- **pandas differs from SQL here:** the SQL query returns nothing, but `~isin` returns Chitra and Dev. `isin` is a plain membership test with no UNKNOWN. In my run the NULL became NaN and the key column became `float64`; that matters only for display, the comparison still works.
- **NaN in isin:** `isin` treats NaN as equal to NaN (`[1.0, 3.0, NaN].isin([1.0, NaN])` gave `[True, False, True]`). So if the left side contains NaN and the list also has NaN, the row counts as "found", the opposite of SQL, where NULL never matches.
- All SQL engines I know follow this standard rule, but I only ran SQLite here (not executed on Postgres, MySQL, BigQuery or Snowflake).

**Follow-ups:**
- *Does `x IN (..., NULL)` have the same problem?* No: it can be TRUE; you only lose the UNKNOWN cases, which were not matches anyway.
- *Why not just use a LEFT JOIN?* That works too (Part 2), and it is NULL-safe if you test a non-null column of the right table.
- *How do you make pandas behave like SQL?* Drop NaN from the keys explicitly and decide what NaN on the left should do; do not rely on `isin` to guess.

**Common mistakes:**
- Blaming the data ("there are no customers without orders") instead of the NULL.
- Fixing it with `COALESCE(customer_id, 0)`, which invents a customer 0.
- Believing `NOT IN` and `NOT EXISTS` are always interchangeable.
- Reading a `float64` key column in pandas as a data problem and casting it away without handling the NaN first.

### Q14 ⭐⭐⭐ 🟡 ORDER BY with NULLs and ties: employees(emp_id, name, dept, salary) where salary can be NULL. Where do NULLs sort in ascending and descending order in PostgreSQL, MySQL, SQLite, SQL Server and Oracle (state as hedged dialect behaviour; check the engine docs) and how do you force NULLS LAST portably with a CASE or an IS NULL sort key? Explain multi-column ORDER BY, sorting by an expression or ordinal, and why ties make output order non-deterministic. Show pandas sort_values with na_position and a stable sort.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** There is no portable default for where NULLs sort (SQLite and, from memory, MySQL and SQL Server treat NULL as smallest, PostgreSQL and, from memory, Oracle as largest), so when it matters I write the NULL position explicitly with `NULLS LAST` where supported or a `CASE WHEN x IS NULL` sort key where not, and I always add a unique tie-breaker column.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha','Eng',90),(2,'Ben','Eng',NULL),(3,'Chitra','Ops',70),
 (4,'Dev','Ops',90),(5,'Esha','Eng',70),(6,'Farid','Ops',NULL),(7,'Gita','Eng',90);
```

**SQL answer:** all queries are in the Code block: plain `ORDER BY salary` (ASC and DESC), `NULLS LAST` / `NULLS FIRST`, the portable `sql_portable` with a CASE key, `sql_multi` for a multi-column sort, an ordinal sort and an expression sort.

**pandas answer:** `df.sort_values(["salary", "emp_id"], ascending=[False, True], na_position="last")`, plus `kind="stable"` for a stable sort; all variants are in the Code block.

**Dialect behaviour of NULL ordering:**

| Engine | NULLs in ASC | NULLs in DESC | NULLS FIRST/LAST keyword | Status |
|---|---|---|---|---|
| SQLite 3.45 | first | last | yes (since 3.30, ran it) | executed here |
| PostgreSQL | last | first | yes | PostgreSQL docs page opened: NULLs sort as if larger |
| MySQL | first | last | no (use a sort key) | from memory, not opened or executed |
| SQL Server | first | last | no (use a sort key) | from memory, not opened or executed |
| Oracle | last | first | yes | from memory, not opened or executed |

Check the engine docs before relying on the last three rows.

**Example:** salaries are Asha 90, Ben NULL, Chitra 70, Dev 90, Esha 70, Farid NULL, Gita 90. `ORDER BY salary, emp_id` in SQLite gives the NULLs first: Ben (2), Farid (6), then the 70s (3, 5), then the 90s (1, 4, 7). `ORDER BY salary DESC, emp_id` gives 1, 4, 7, 3, 5, 2, 6, so NULLs fall to the bottom. The portable `CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC, emp_id` gives the same list `[1, 4, 7, 3, 5, 2, 6]` on every engine, because the CASE key is a plain 0/1 number that sorts the same everywhere.

**Code:** run with `python3 -I`.
```python
# ORDER BY with NULLs and ties: SQLite behaviour, portable NULLS LAST, multi-column, ordinal, ties, pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha','Eng',90),(2,'Ben','Eng',NULL),(3,'Chitra','Ops',70),
 (4,'Dev','Ops',90),(5,'Esha','Eng',70),(6,'Farid','Ops',NULL),(7,'Gita','Eng',90);
""")

def ids(q): return [r[0] for r in con.execute(q).fetchall()]

asc = ids("SELECT emp_id FROM employees ORDER BY salary, emp_id")
desc = ids("SELECT emp_id FROM employees ORDER BY salary DESC, emp_id")
print("SQLite ASC  (salary, emp_id):", asc)
print("SQLite DESC (salary DESC, emp_id):", desc)

nl_asc = ids("SELECT emp_id FROM employees ORDER BY salary NULLS LAST, emp_id")
nl_desc = ids("SELECT emp_id FROM employees ORDER BY salary DESC NULLS FIRST, emp_id")
print("NULLS LAST asc:", nl_asc, "| DESC NULLS FIRST:", nl_desc)

# Portable NULLS LAST: a CASE sort key (works where NULLS LAST is not supported)
sql_portable = """SELECT emp_id FROM employees
ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC, emp_id"""
portable = ids(sql_portable)
print("portable, salary DESC NULLS LAST, tie-break emp_id:", portable)

# multi-column + expression + ordinal
sql_multi = "SELECT emp_id, dept, salary FROM employees ORDER BY dept ASC, salary DESC, emp_id ASC"
print("dept ASC, salary DESC, emp_id ASC (NULL salary is last within each dept):")
print(con.execute(sql_multi).fetchall())
print("ordinal ORDER BY 2, 1:", con.execute("SELECT emp_id, dept FROM employees ORDER BY 2, 1").fetchall())
print("expression ORDER BY -salary (NULL stays NULL):", ids("SELECT emp_id FROM employees ORDER BY -salary, emp_id"))

# ties without tie-breaker: only salary key. Order among equals is up to the engine
print("ties, no tie-breaker (engine's choice, not a guarantee):", ids("SELECT emp_id FROM employees ORDER BY salary DESC"))

# pandas
df = pd.read_sql("SELECT * FROM employees", con)
p_asc = df.sort_values(["salary", "emp_id"])["emp_id"].tolist()                      # na_position='last' is the default
p_asc_first = df.sort_values(["salary", "emp_id"], na_position="first")["emp_id"].tolist()
p_desc = df.sort_values(["salary", "emp_id"], ascending=[False, True])["emp_id"].tolist()
p_desc_first = df.sort_values(["salary", "emp_id"], ascending=[False, True], na_position="first")["emp_id"].tolist()
print("pandas default asc (NaN last):", p_asc)
print("pandas asc na_position='first' (matches SQLite ASC):", p_asc_first)
print("pandas desc default (NaN last, matches SQLite DESC):", p_desc)
print("pandas desc na_position='first':", p_desc_first)

# stable sort: sort by salary only with kind='stable' keeps original row order among ties
st = df.sort_values("salary", ascending=False, kind="stable")["emp_id"].tolist()
print("pandas stable desc, salary only:", st)
st2 = df.sort_values("salary", kind="stable").sort_values("dept", kind="stable")["emp_id"].tolist()
print("two stable passes (salary then dept):", st2)

assert asc == p_asc_first                    # SQLite puts NULL first in ASC
assert desc == p_desc                        # SQLite puts NULL last in DESC
assert nl_asc == p_asc and nl_desc == p_desc_first
assert portable == df.sort_values(["salary", "emp_id"], ascending=[False, True])["emp_id"].tolist()
p_multi = df.sort_values(["dept", "salary", "emp_id"], ascending=[True, False, True])[["emp_id", "dept", "salary"]]
sql_multi_rows = con.execute(sql_multi).fetchall()
assert [(a, b, None if pd.isna(c) else int(c)) for a, b, c in p_multi.itertuples(index=False)] == sql_multi_rows
print("asserts passed")
```

**Output (my run):**
```text
SQLite ASC  (salary, emp_id): [2, 6, 3, 5, 1, 4, 7]
SQLite DESC (salary DESC, emp_id): [1, 4, 7, 3, 5, 2, 6]
NULLS LAST asc: [3, 5, 1, 4, 7, 2, 6] | DESC NULLS FIRST: [2, 6, 1, 4, 7, 3, 5]
portable, salary DESC NULLS LAST, tie-break emp_id: [1, 4, 7, 3, 5, 2, 6]
dept ASC, salary DESC, emp_id ASC (NULL salary is last within each dept):
[(1, 'Eng', 90), (7, 'Eng', 90), (5, 'Eng', 70), (2, 'Eng', None), (4, 'Ops', 90), (3, 'Ops', 70), (6, 'Ops', None)]
ordinal ORDER BY 2, 1: [(1, 'Eng'), (2, 'Eng'), (5, 'Eng'), (7, 'Eng'), (3, 'Ops'), (4, 'Ops'), (6, 'Ops')]
expression ORDER BY -salary (NULL stays NULL): [2, 6, 1, 4, 7, 3, 5]
ties, no tie-breaker (engine's choice, not a guarantee): [1, 4, 7, 3, 5, 2, 6]
pandas default asc (NaN last): [3, 5, 1, 4, 7, 2, 6]
pandas asc na_position='first' (matches SQLite ASC): [2, 6, 3, 5, 1, 4, 7]
pandas desc default (NaN last, matches SQLite DESC): [1, 4, 7, 3, 5, 2, 6]
pandas desc na_position='first': [2, 6, 1, 4, 7, 3, 5]
pandas stable desc, salary only: [1, 4, 7, 3, 5, 2, 6]
two stable passes (salary then dept): [5, 1, 7, 2, 3, 4, 6]
asserts passed
```

**Edge cases:**
- Ties: the 90s are tied three ways. Without the `emp_id` tie-breaker the SQL standard allows any order among them; my SQLite run happened to give 1, 4, 7, which is no guarantee on another engine or after the table grows.
- Multi-column: later keys only break ties of earlier keys, each with its own direction.
- An expression such as `-salary` keeps NULL as NULL, so NULL placement still follows the engine's rule.
- Ordinals (`ORDER BY 2, 1`) work in the engines I know but break when the SELECT list changes (Q23).
- pandas default: `na_position="last"` in both directions. So the pandas default matches SQLite for DESC but not for ASC. I had to pass `na_position="first"` to match SQLite's ASC.

**Then explain:**
- **Force NULLS LAST portably:** `ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC`. In several engines you can sort on the boolean `salary IS NULL` directly, but a CASE is the most portable (Oracle has no boolean type, from memory).
- **Multi-column:** `ORDER BY dept ASC, salary DESC, emp_id ASC`; the first key is the major sort.
- **Expression or ordinal:** you can sort on any expression; ordinal positions are legal but fragile.
- **Ties are not stable:** a stable sort is a pandas feature you opt into (`kind="stable"`); SQL gives no such promise, so make the order total with a unique key.
- **pandas:** `kind="stable"` keeps the original row order among equal keys; in my run `sort_values("salary", ascending=False, kind="stable")` gave 1, 4, 7, 3, 5, 2, 6, ties in original row order. Two stable passes (minor key first) also give a multi-key sort.

**Follow-ups:**
- *How does `DISTINCT` or `GROUP BY` order output?* Not at all; add `ORDER BY` if you need an order.
- *What does `ORDER BY salary DESC LIMIT 1` return with a NULL top?* Depends on the engine's default; with NULLs-first-in-DESC (PostgreSQL) the NULL row wins, which is a classic "highest salary" bug.
- *How do you sort a mixed column of text numbers?* Cast to a number in the sort key (Part 10 has string traps).

**Common mistakes:**
- Assuming NULLs sort the same way in every database.
- No tie-breaker, then a flaky test or flaky pagination.
- Using `salary IS NULL` as a sort key and forgetting that FALSE (0) sorts before TRUE (1) in ASC.
- Using `na_position` and expecting it to apply to the SQL engine.

### Q15 ⭐⭐⭐ 🟡 Translate SQL to pandas. SQL: SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_sal FROM employees WHERE salary IS NOT NULL AND hired >= '2020-01-01' GROUP BY dept HAVING COUNT(*) >= 3 ORDER BY avg_sal DESC LIMIT 5, on employees(emp_id, name, dept, salary, hired). Write the pandas with boolean masks, groupby with named aggregation, query() and sort_values().head(5); explain as_index, reset_index, and how to assert the two results match (same rows, order, dtypes).
**Asked at:** pandas documentation (Comparison with SQL) and prep guides, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `WHERE` becomes a boolean mask, `GROUP BY ... COUNT/AVG` becomes `groupby().agg(n=..., avg_sal=...)` with named aggregation, `HAVING` becomes a second filter (`query` or a mask) on the aggregated frame, and `ORDER BY ... LIMIT` becomes `sort_values().head()`.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER, hired TEXT);
INSERT INTO employees VALUES
 (1,'a1','Eng',100,'2021-03-01'),(2,'a2','Eng',140,'2022-05-10'),(3,'a3','Eng',120,'2020-01-01'),(4,'a4','Eng',NULL,'2023-01-01'),(5,'a5','Eng',500,'2019-12-31'),
 (6,'b1','Ops',60,'2020-06-01'),(7,'b2','Ops',80,'2021-01-01'),(8,'b3','Ops',70,'2024-02-02'),
 (9,'c1','HR',50,'2020-02-02'),(10,'c2','HR',55,'2022-02-02'),(11,'c3','HR',45,'2023-03-03'),(12,'c4','HR',90,'2018-01-01'),
 (13,'d1','Fin',200,'2021-01-01'),(14,'d2','Fin',210,'2021-02-01'),(15,'d3','Fin',190,'2021-03-01'),
 (16,'e1','Mkt',75,'2022-01-01'),(17,'e2','Mkt',85,'2022-02-01'),(18,'e3','Mkt',95,'2022-03-01'),
 (19,'f1','Sales',65,'2020-01-01'),(20,'f2','Sales',66,'2020-02-01'),(21,'f3','Sales',67,'2020-03-01'),
 (22,'g1','Legal',300,'2021-01-01'),(23,'g2','Legal',310,'2021-02-01');
```

**SQL answer:** the query is the string `sql` in the Code block, verbatim from the question.

**pandas answer:** `v1` (masks, named aggregation, `query`, `sort_values`, `head(5)`) and `v2` (`query()` for the row filter, then `reset_index()`) in the Code block.

**Example:** after `WHERE salary IS NOT NULL AND hired >= '2020-01-01'`, Eng keeps ids 1, 2, 3 (id 4 has a NULL salary, id 5 was hired in 2019): n = 3, average of 100, 140, 120 = 120. Ops keeps 60, 80, 70: n = 3, avg 70. HR keeps 50, 55, 45 (id 12 hired 2018): n = 3, avg 50. Fin avg 200, Mkt 85, Sales 66, all with n = 3. Legal has only 2 rows, so `HAVING COUNT(*) >= 3` removes it. Six departments pass; sorted by average descending they are Fin 200, Eng 120, Mkt 85, Ops 70, Sales 66, HR 50, and `LIMIT 5` drops HR.

**Code:** run with `python3 -I`.
```python
# Translate SQL to pandas (Q15) and assert the two results are identical (rows, order, dtypes).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER, hired TEXT);
INSERT INTO employees VALUES
 (1,'a1','Eng',100,'2021-03-01'),(2,'a2','Eng',140,'2022-05-10'),(3,'a3','Eng',120,'2020-01-01'),(4,'a4','Eng',NULL,'2023-01-01'),(5,'a5','Eng',500,'2019-12-31'),
 (6,'b1','Ops',60,'2020-06-01'),(7,'b2','Ops',80,'2021-01-01'),(8,'b3','Ops',70,'2024-02-02'),
 (9,'c1','HR',50,'2020-02-02'),(10,'c2','HR',55,'2022-02-02'),(11,'c3','HR',45,'2023-03-03'),(12,'c4','HR',90,'2018-01-01'),
 (13,'d1','Fin',200,'2021-01-01'),(14,'d2','Fin',210,'2021-02-01'),(15,'d3','Fin',190,'2021-03-01'),
 (16,'e1','Mkt',75,'2022-01-01'),(17,'e2','Mkt',85,'2022-02-01'),(18,'e3','Mkt',95,'2022-03-01'),
 (19,'f1','Sales',65,'2020-01-01'),(20,'f2','Sales',66,'2020-02-01'),(21,'f3','Sales',67,'2020-03-01'),
 (22,'g1','Legal',300,'2021-01-01'),(23,'g2','Legal',310,'2021-02-01');
""")

sql = """
SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_sal
FROM employees
WHERE salary IS NOT NULL AND hired >= '2020-01-01'
GROUP BY dept
HAVING COUNT(*) >= 3
ORDER BY avg_sal DESC
LIMIT 5
"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

emp = pd.read_sql("SELECT * FROM employees", con)

# version 1: boolean masks + named aggregation
mask = emp["salary"].notna() & (emp["hired"] >= "2020-01-01")
v1 = (emp[mask]
      .groupby("dept", as_index=False)
      .agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))
      .query("n >= 3")
      .sort_values("avg_sal", ascending=False)
      .head(5)
      .reset_index(drop=True))

# version 2: query() for the row filter, as_index=True then reset_index
v2 = (emp.query("salary.notna() and hired >= '2020-01-01'")
         .groupby("dept")
         .agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))
         .query("n >= 3")
         .sort_values("avg_sal", ascending=False)
         .head(5)
         .reset_index())
print(v1.dtypes.to_dict())
print(sql_df.dtypes.to_dict())

pd.testing.assert_frame_equal(sql_df, v1)
pd.testing.assert_frame_equal(sql_df, v2)
print("asserts passed: SQL == v1 == v2 (same rows, same order, same dtypes; no ties in avg_sal here)")

# what as_index=True does if you forget reset_index
g = emp[mask].groupby("dept").agg(n=("emp_id", "size"))
print("as_index=True: dept is the index ->", g.index.name, "| columns:", list(g.columns))

# how many rows got there before the limit
print("depts passing HAVING before LIMIT 5:", len(emp[mask].groupby("dept").filter(lambda x: len(x) >= 3)["dept"].unique()))
```

**Output (my run):**
```text
 dept  n  avg_sal
  Fin  3    200.0
  Eng  3    120.0
  Mkt  3     85.0
  Ops  3     70.0
Sales  3     66.0
{'dept': <StringDtype(storage='python', na_value=nan)>, 'n': dtype('int64'), 'avg_sal': dtype('float64')}
{'dept': <StringDtype(storage='python', na_value=nan)>, 'n': dtype('int64'), 'avg_sal': dtype('float64')}
asserts passed: SQL == v1 == v2 (same rows, same order, same dtypes; no ties in avg_sal here)
as_index=True: dept is the index -> dept | columns: ['n']
depts passing HAVING before LIMIT 5: 6
```

**Edge cases:**
- Ties in `avg_sal` at the 5th/6th place make `LIMIT 5` ambiguous in both SQL and pandas; add a tie-breaker (`ORDER BY avg_sal DESC, dept`; in pandas `sort_values(["avg_sal", "dept"], ascending=[False, True])`). Not needed in this data.
- `COUNT(*)` after the WHERE counts rows (`size`); `COUNT(salary)` would be `count` (here identical, because the mask removes the NULLs).
- A department with zero surviving rows simply does not appear in either version.
- `hired` is text in ISO format, so string comparison works. With real dates in pandas I would `pd.to_datetime` first.

**Then explain:**
- **Order of work is identical:** filter rows, group, aggregate, filter groups, sort, cut.
- **`as_index`:** `groupby("dept")` makes `dept` the index of the result (my run printed `dept` as the index name); `as_index=False` or `reset_index()` puts it back as a column so it matches the SQL frame.
- **Named aggregation:** `agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))` names output columns like SQL aliases.
- **Why HAVING is `query("n >= 3")`:** it runs after aggregation, on the grouped frame, just like HAVING.
- **How to assert a match:** `pd.testing.assert_frame_equal(sql_df, v1)` checks rows, order, column names and dtypes (here `n` is `int64`, `avg_sal` is `float64`, `dept` is pandas' string dtype on both sides). It passed for both versions. For queries without a total order, sort both sides on all columns first.

**Follow-ups:**
- *`size` vs `count`?* `size` counts rows (SQL `COUNT(*)`), `count` counts non-null values of a column (SQL `COUNT(col)`).
- *How would you do it in one chain?* The chain in `v1` is one expression; use `.pipe` if you need to reuse a step.
- *Why is HAVING not just WHERE?* WHERE runs before grouping and cannot see aggregates; HAVING runs after.

**Common mistakes:**
- Forgetting `reset_index` and then trying to use `dept` as a column.
- Putting the `n >= 3` filter before the groupby (that filters rows, not groups).
- Comparing frames by eye instead of asserting dtypes and order.
- Using `count` where SQL used `COUNT(*)`.

### Q16 ⭐⭐⭐ 🟡 SQL vs pandas NULL differences in grouping and aggregation. Given orders(order_id, region, amount) where region and amount have NULLs, show what SQL GROUP BY region returns (NULLs form one group) versus pandas groupby('region') (NaN keys dropped unless dropna=False), SUM of an all-NULL group (NULL in SQL, 0 in pandas unless min_count=1), AVG vs mean skipping missing values, COUNT(col) vs count(), and how to make pandas match SQL.
**Asked at:** pandas documentation (Comparison with SQL) and prep guides, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** SQL and pandas disagree by default on four things: SQL keeps a NULL group, pandas drops NaN keys; SQL `SUM` of only NULLs is NULL, pandas gives 0; `COUNT(col)` and `count()` agree (both skip missing values) but `COUNT(*)` is `size()`; and both `AVG` and `mean` skip missing values. Pass `dropna=False` and `min_count=1` to make pandas match.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',NULL),(3,'North',50),
 (4,'South',NULL),(5,'South',NULL),
 (6,NULL,30),(7,NULL,NULL),(8,'East',20);
```

**SQL answer:** the query is `sql` in the Code block (`COUNT(*)`, `COUNT(amount)`, `SUM`, `AVG` per region, NULL region ordered last by `ORDER BY region IS NULL, region`).

**pandas answer:** `matched` in the Code block: `groupby("region", dropna=False)` with `size`, `count`, a `sum(min_count=1)` lambda and `mean`.

**Example:** North has amounts 100, NULL, 50: 3 rows, 2 non-null amounts, sum 150, average 75 (the NULL is skipped, so it is 150/2, not 150/3). South has 2 rows and no amount at all: `SUM` is NULL, `AVG` is NULL, `COUNT(amount)` is 0. The NULL-region rows (orders 6 and 7) form one group: 2 rows, 1 amount, sum 30. East is 20.

**Code:** run with `python3 -I`.
```python
# SQL vs pandas NULL differences in GROUP BY and aggregates (Q16).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',NULL),(3,'North',50),
 (4,'South',NULL),(5,'South',NULL),
 (6,NULL,30),(7,NULL,NULL),(8,'East',20);
""")

sql = """
SELECT region,
       COUNT(*)      AS n_rows,
       COUNT(amount) AS n_amount,
       SUM(amount)   AS total,
       AVG(amount)   AS avg_amt
FROM orders
GROUP BY region
ORDER BY region IS NULL, region
"""
sql_df = pd.read_sql(sql, con)
print("SQL:"); print(sql_df.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con)

# default pandas: NaN keys dropped, SUM of nothing = 0
naive = orders.groupby("region").agg(n_rows=("order_id", "size"), n_amount=("amount", "count"),
                                     total=("amount", "sum"), avg_amt=("amount", "mean"))
print("\npandas defaults (dropna=True, sum without min_count):"); print(naive)

# matched to SQL: keep the NaN group, min_count=1 so an all-NaN group sums to NaN
matched = (orders.groupby("region", dropna=False)
           .agg(n_rows=("order_id", "size"), n_amount=("amount", "count"),
                total=("amount", lambda s: s.sum(min_count=1)), avg_amt=("amount", "mean"))
           .reset_index()
           .sort_values("region", na_position="last")
           .reset_index(drop=True))
print("\npandas matched to SQL:"); print(matched.to_string(index=False))

# compare: NULL/NaN treated as equal, int columns as int64
pd.testing.assert_frame_equal(sql_df, matched, check_dtype=True)
print("\nasserts passed: SQL == matched pandas (rows ordered by region, NULL region last)")

# whole-table behaviour: all-NULL column
empty_like = orders[orders["region"] == "South"]["amount"]
print("pandas sum of all-NaN:", empty_like.sum(), "| with min_count=1:", empty_like.sum(min_count=1))
print("SQL SUM of all-NULL group:", con.execute("SELECT SUM(amount) FROM orders WHERE region='South'").fetchone()[0],
      "| TOTAL():", con.execute("SELECT TOTAL(amount) FROM orders WHERE region='South'").fetchone()[0],
      "| AVG:", con.execute("SELECT AVG(amount) FROM orders WHERE region='South'").fetchone()[0])
print("pandas mean of all-NaN:", empty_like.mean())
```

**Output (my run):**
```text
SQL:
region  n_rows  n_amount  total  avg_amt
  East       1         1   20.0     20.0
 North       3         2  150.0     75.0
 South       2         0    NaN      NaN
   NaN       2         1   30.0     30.0

pandas defaults (dropna=True, sum without min_count):
        n_rows  n_amount  total  avg_amt
region                                  
East         1         1   20.0     20.0
North        3         2  150.0     75.0
South        2         0    0.0      NaN

pandas matched to SQL:
region  n_rows  n_amount  total  avg_amt
  East       1         1   20.0     20.0
 North       3         2  150.0     75.0
 South       2         0    NaN      NaN
   NaN       2         1   30.0     30.0

asserts passed: SQL == matched pandas (rows ordered by region, NULL region last)
pandas sum of all-NaN: 0.0 | with min_count=1: nan
SQL SUM of all-NULL group: None | TOTAL(): 0.0 | AVG: None
pandas mean of all-NaN: nan
```

**Edge cases:**
- All-NULL group: SQL `SUM` gives NULL; SQLite's `TOTAL()` returns 0.0 (SQLite-specific, shown in the run). pandas `sum()` gave 0.0 and `sum(min_count=1)` gave NaN.
- `mean` of an all-NaN group is NaN in both.
- Default pandas dropped the NULL-region group entirely and the default result had 3 groups instead of 4.
- NULL and NaN are shown differently (`None` vs `NaN`), and `assert_frame_equal` treats them as equal missing values.
- The row-level `n_rows` (`size`) must come from a column that has no gaps (here `order_id`), or use `size()` directly.

**Then explain:**
- **Grouping:** SQL `GROUP BY` puts all NULLs into one group; pandas `groupby` drops them unless `dropna=False`.
- **Sum:** pandas treats the sum of nothing as 0; `min_count=1` says "need at least one non-missing value", giving NaN like SQL.
- **Avg/mean:** both skip missing values, so the denominator is the count of non-null values.
- **Counting:** `COUNT(*)` is `size()`; `COUNT(col)` is `count()`.
- **Sorting:** SQLite sorts NULL first in ASC; pandas `sort_values` puts NaN last by default, so I sorted with an explicit `na_position` before comparing.
- Dialect note: other engines follow the same standard rules for NULL groups and `SUM` (not executed here).

**Follow-ups:**
- *Why does pandas give 0 for an all-NaN sum?* It defines the empty sum as 0, the additive identity; SQL has no such rule. The behaviour shown is from my pandas 3.0.5 run.
- *How do you make SQL match pandas?* `COALESCE(SUM(amount), 0)`.
- *What does `groupby` do to NaN in the value column?* Skips it in `sum`, `mean`, `count`.

**Common mistakes:**
- Forgetting that pandas silently drops NaN-key rows, so totals no longer reconcile with SQL.
- Reporting 0 revenue for a group that has no data (should be NULL/"no data").
- Dividing by `size` instead of `count` for an average.

### Q17 ⭐⭐⭐ 🟡 Debugging: 'This query returns the wrong totals.' A teammate computes revenue per customer from orders(order_id, customer_id, amount, status) with SELECT customer_id, SUM(DISTINCT amount) ... and gets lower totals for some customers; another version filters status in HAVING and fails. Explain what SUM(DISTINCT) does, why two equal-amount orders vanish, when DISTINCT in an aggregate is legitimate, and give the corrected query plus a pandas check that exposes the bug.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `SUM(DISTINCT amount)` adds each distinct amount once, so two orders of the same value count once and revenue is understated; the fix is plain `SUM(amount)` with the status filter in `WHERE`, and the status test belongs in `WHERE` (or inside a `CASE`), not `HAVING`.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT);
INSERT INTO orders VALUES
 (1,1,100,'completed'),(2,1,100,'completed'),(3,1,50,'cancelled'),
 (4,2,200,'completed'),(5,2,300,'completed'),
 (6,3,40,'completed'),(7,3,40,'refunded'),(8,3,40,'completed');
```

**SQL answer:** `fixed` (and the equivalent `fixed_case`) in the Code block. The buggy queries are `buggy` and `buggy_having`.

**pandas answer:** `distinct_all` (drop duplicates then sum) reproduces the bug, `true_all` (plain sum) is the right figure, and `completed` is the corrected pandas result, in the Code block.

**Premise correction:** the question says the HAVING version "fails". In SQLite it does not fail: it runs and silently returns the wrong thing (my run: totals of all statuses, 250, 500, 120, not the completed-only totals). A strict engine (PostgreSQL, and MySQL with `ONLY_FULL_GROUP_BY`, from memory, not executed) rejects it because `status` is neither grouped nor aggregated. In every engine, `HAVING` filters groups after aggregation, not rows before it.

**Example:** customer 1 has orders 100, 100 (completed) and 50 (cancelled). `SUM(DISTINCT amount)` = 100 + 50 = 150, but the real total is 250 (200 completed). Customer 3 has 40, 40, 40: DISTINCT gives 40 instead of 120 (80 completed). Customer 2 has two different amounts, so DISTINCT happens to be right (500), which is why the bug shows up only for "some customers".

**Code:** run with `python3 -I`.
```python
# Debugging SUM(DISTINCT amount) and HAVING on a non-aggregated column (Q17).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT);
INSERT INTO orders VALUES
 (1,1,100,'completed'),(2,1,100,'completed'),(3,1,50,'cancelled'),
 (4,2,200,'completed'),(5,2,300,'completed'),
 (6,3,40,'completed'),(7,3,40,'refunded'),(8,3,40,'completed');
""")

buggy = "SELECT customer_id, SUM(DISTINCT amount) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id"
buggy_having = ("SELECT customer_id, SUM(amount) AS revenue FROM orders GROUP BY customer_id "
                "HAVING status = 'completed' ORDER BY customer_id")
fixed = ("SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed' "
         "GROUP BY customer_id ORDER BY customer_id")
fixed_case = ("SELECT customer_id, SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS revenue "
              "FROM orders GROUP BY customer_id ORDER BY customer_id")
fixed_all = "SELECT customer_id, SUM(amount) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id"

for name, q in [("buggy SUM(DISTINCT)", buggy), ("HAVING status (bare column)", buggy_having),
                ("fixed (WHERE before GROUP BY)", fixed), ("fixed (SUM(CASE ...))", fixed_case), ("SUM(amount), all statuses", fixed_all)]:
    print(name, con.execute(q).fetchall())

# pandas check that exposes the bug
orders = pd.read_sql("SELECT * FROM orders", con)
true_all = orders.groupby("customer_id")["amount"].sum()
distinct_all = orders.groupby("customer_id")["amount"].apply(lambda s: s.drop_duplicates().sum())
check = pd.DataFrame({"sum": true_all, "sum_distinct": distinct_all})
check["lost"] = check["sum"] - check["sum_distinct"]
print(check)
print("customers where DISTINCT lost money:", check.index[check["lost"] > 0].tolist())

completed = orders[orders["status"] == "completed"].groupby("customer_id", as_index=False)["amount"].sum()
completed = completed.rename(columns={"amount": "revenue"})
sql_fixed = pd.read_sql(fixed, con)
pd.testing.assert_frame_equal(sql_fixed, completed)
pd.testing.assert_frame_equal(pd.read_sql(fixed_case, con), completed)
# the buggy SQL equals the pandas drop_duplicates version (proves what DISTINCT does)
sql_buggy = pd.read_sql(buggy, con)
assert sql_buggy["revenue"].tolist() == distinct_all.tolist()
# the real totals differ from the buggy ones for customers 1 and 3
assert true_all.tolist() != distinct_all.tolist()

# legitimate DISTINCT: count distinct customers, not rows
print("legit: COUNT(DISTINCT customer_id) =", con.execute("SELECT COUNT(DISTINCT customer_id) FROM orders").fetchone()[0],
      "| pandas nunique =", orders["customer_id"].nunique())
print("asserts passed (rows ordered by customer_id)")
```

**Output (my run):**
```text
buggy SUM(DISTINCT) [(1, 150), (2, 500), (3, 40)]
HAVING status (bare column) [(1, 250), (2, 500), (3, 120)]
fixed (WHERE before GROUP BY) [(1, 200), (2, 500), (3, 80)]
fixed (SUM(CASE ...)) [(1, 200), (2, 500), (3, 80)]
SUM(amount), all statuses [(1, 250), (2, 500), (3, 120)]
             sum  sum_distinct  lost
customer_id                         
1            250           150   100
2            500           500     0
3            120            40    80
customers where DISTINCT lost money: [1, 3]
legit: COUNT(DISTINCT customer_id) = 3 | pandas nunique = 3
asserts passed (rows ordered by customer_id)
```

**Edge cases:**
- Customers whose amounts are all different look fine, so spot checks on a few rows can pass.
- A customer with no completed orders disappears from the `WHERE` version, but shows revenue 0 in the `SUM(CASE ...)` version. Choose which one you want.
- NULL amounts are ignored by both `SUM` and `SUM(DISTINCT)`.
- Float amounts: two prices that look equal can differ in the last digit, and DISTINCT then does not remove them.

**Then explain:**
- **What DISTINCT does:** de-duplicates the values, not the rows or the orders. `SUM(DISTINCT amount)` treats amounts as a set.
- **When DISTINCT in an aggregate is right:** `COUNT(DISTINCT customer_id)` (unique customers). For sums, de-duplicate by key (for example `SELECT DISTINCT order_id, amount` in a subquery, or fix the join that fanned rows out), never by value.
- **Corrected query:** filter rows with `WHERE status = 'completed'`, then `SUM(amount) ... GROUP BY customer_id`; or `SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END)`. Both gave 200, 500, 80.
- **pandas check:** `sum` versus `drop_duplicates().sum()` per customer; the `lost` column (100 and 80) shows exactly which customers were hit, and the buggy SQL equals the drop-duplicates version.
- **HAVING:** use it only for conditions on aggregates (`HAVING SUM(amount) > 100`).

**Follow-ups:**
- *How would a join cause a similar problem?* A one-to-many join repeats the amount on each child row, so `SUM` overstates; `DISTINCT` on the amount is the wrong repair (Part 2).
- *`AVG(DISTINCT x)`?* Same idea: averages the distinct values.
- *How do you catch this in review?* Reconcile against an independent total (pandas or `SUM` without DISTINCT).

**Common mistakes:**
- Adding DISTINCT to make a number "look right".
- Putting a row filter in `HAVING`.
- Not checking per-group totals against a second method.

### Q18 ⭐⭐⭐ 🟡 Debugging: this query errors in PostgreSQL but runs in some MySQL setups: SELECT customer_id, status, SUM(amount) FROM orders GROUP BY customer_id. Explain the rule that every non-aggregated SELECT column must be in GROUP BY (or functionally dependent on it), what MySQL ONLY_FULL_GROUP_BY and SQLite bare columns do instead (hedged), why silent arbitrary values are dangerous, and how to fix it correctly for each intended meaning (group by status too, or aggregate it).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Every non-aggregated SELECT column must be in `GROUP BY` or functionally dependent on it; PostgreSQL rejects the query, MySQL with `ONLY_FULL_GROUP_BY` (the default in recent versions, from memory) rejects it, while SQLite accepts it and returns the `status` of one arbitrary row, which is dangerous because it looks like a real answer.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'completed',100),(2,1,'cancelled',50),(3,1,'completed',70),
 (4,2,'refunded',200),(5,2,'completed',30);
```

**SQL answer:** `bad` is the query from the question; `f1` (group by customer and status) and `f2` (aggregate the status) are the fixes, all in the Code block.

**pandas answer:** `p1` (`groupby(["customer_id", "status"])`) and `p2` (named aggregation with `max`/`nunique`) in the Code block. pandas has no bare columns: a non-key column must go through an explicit function such as `first`.

**Example:** customer 1 has completed 100, cancelled 50, completed 70. The bad query returns one row per customer with total 220, and a status of `completed`, but the query never says which status. For customer 2 (refunded 200, completed 30) it returned `refunded`. If the intent was "total per customer and status", `f1` returns four rows (1/cancelled 50, 1/completed 170, 2/completed 30, 2/refunded 200). If the intent was "total per customer, plus one summary of the status", `f2` makes the choice explicit (`MAX(status)`, number of distinct statuses).

**Code:** run with `python3 -I`.
```python
# Debugging a bare column in GROUP BY (Q18): SQLite runs it, silently.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'completed',100),(2,1,'cancelled',50),(3,1,'completed',70),
 (4,2,'refunded',200),(5,2,'completed',30);
""")

bad = "SELECT customer_id, status, SUM(amount) AS total FROM orders GROUP BY customer_id ORDER BY customer_id"
print("bare column (SQLite runs it; value of status is not defined by the query):")
print(con.execute(bad).fetchall())

# SQLite special case: with a single MIN() or MAX(), bare columns come from the row holding the min/max
mx = "SELECT customer_id, status, MAX(amount) AS top_amt FROM orders GROUP BY customer_id ORDER BY customer_id"
print("SQLite MAX special case (status of the max row):", con.execute(mx).fetchall())
two = "SELECT customer_id, status, MAX(amount), MIN(amount) FROM orders GROUP BY customer_id ORDER BY customer_id"
print("with MAX and MIN both (no special case, arbitrary row):", con.execute(two).fetchall())

# fix 1: the intended meaning is 'per customer and status'
f1 = "SELECT customer_id, status, SUM(amount) AS total FROM orders GROUP BY customer_id, status ORDER BY customer_id, status"
# fix 2: the intended meaning is 'per customer, status is an aggregate' (say which one)
f2 = ("SELECT customer_id, MAX(status) AS max_status, COUNT(DISTINCT status) AS n_statuses, SUM(amount) AS total "
      "FROM orders GROUP BY customer_id ORDER BY customer_id")
print("fix 1:", con.execute(f1).fetchall())
print("fix 2:", con.execute(f2).fetchall())

orders = pd.read_sql("SELECT * FROM orders", con)
p1 = (orders.groupby(["customer_id", "status"], as_index=False)["amount"].sum()
      .rename(columns={"amount": "total"}).sort_values(["customer_id", "status"]).reset_index(drop=True))
p2 = (orders.groupby("customer_id")
      .agg(max_status=("status", "max"), n_statuses=("status", "nunique"), total=("amount", "sum"))
      .reset_index())
pd.testing.assert_frame_equal(pd.read_sql(f1, con), p1)
pd.testing.assert_frame_equal(pd.read_sql(f2, con), p2)
print(p1.to_string(index=False)); print(p2.to_string(index=False))
print("asserts passed (fix 1 ordered by customer_id, status; fix 2 by customer_id)")

# pandas has no bare columns: asking for a non-key column needs an explicit function
print("pandas explicit first():", orders.groupby("customer_id").agg(status=("status", "first"), total=("amount", "sum")).reset_index().to_dict("records"))
```

**Output (my run):**
```text
bare column (SQLite runs it; value of status is not defined by the query):
[(1, 'completed', 220), (2, 'refunded', 230)]
SQLite MAX special case (status of the max row): [(1, 'completed', 100), (2, 'refunded', 200)]
with MAX and MIN both (no special case, arbitrary row): [(1, 'cancelled', 100, 50), (2, 'completed', 200, 30)]
fix 1: [(1, 'cancelled', 50), (1, 'completed', 170), (2, 'completed', 30), (2, 'refunded', 200)]
fix 2: [(1, 'completed', 2, 220), (2, 'refunded', 2, 230)]
 customer_id    status  total
           1 cancelled     50
           1 completed    170
           2 completed     30
           2  refunded    200
 customer_id max_status  n_statuses  total
           1  completed           2    220
           2   refunded           2    230
asserts passed (fix 1 ordered by customer_id, status; fix 2 by customer_id)
pandas explicit first(): [{'customer_id': 1, 'status': 'completed', 'total': 220}, {'customer_id': 2, 'status': 'refunded', 'total': 230}]
```

**Edge cases:**
- SQLite's documented special case (confirmed by my run): with a single `MAX()` or `MIN()` in the query, bare columns come from the row that holds the max or min (customer 1 gave `completed` with 100, customer 2 `refunded` with 200). With both `MAX` and `MIN` it falls back to an arbitrary row (customer 1 gave `cancelled`). Do not rely on it.
- Functional dependence: grouping by a primary key lets PostgreSQL (and MySQL 5.7+, from memory) accept other columns of that table.
- `GROUP BY customer_id` with a `name` column from the same customers table is fine only under that rule.

**Then explain:**
- **The rule:** after grouping, each output row represents a group; a column with several values per group has no single value to show.
- **MySQL:** `ONLY_FULL_GROUP_BY` SQL mode rejects the query; when the mode is switched off, MySQL silently picks a value (from memory, not executed here).
- **Danger:** the result looks valid, passes review and changes when the plan changes.
- **Fix by intent:** add the column to `GROUP BY`, or aggregate it (`MAX`, `COUNT(DISTINCT)`, `MIN`), or use a window function for "status of the latest order" (Part 4).
- **pandas:** the equivalent of a bare column is `first()`/`last()`, which is explicit about the choice and depends on row order.

**Follow-ups:**
- *How do you get the status of the largest order per customer?* Use a ranking window (Part 4); the SQLite `MAX` trick is not portable.
- *Is `ANY_VALUE` an option?* MySQL and some others have it (from memory, not executed); it states "I do not care which".
- *Does SELECT DISTINCT have this issue?* No, it applies to the whole row.

**Common mistakes:**
- "Fixing" the error by adding every column to `GROUP BY` and changing the grain.
- Disabling `ONLY_FULL_GROUP_BY` to make the query run.
- Trusting SQLite's output as a model of other engines.

### Q19 ⭐⭐ 🟢 What is the difference between SELECT DISTINCT and GROUP BY? Using orders(order_id, customer_id, status, city), show DISTINCT on one and on several columns, how NULLs are treated (collapsed to one value), COUNT(DISTINCT customer_id) versus COUNT(DISTINCT customer_id, city) (multi-column count is not portable; hedge), and when GROUP BY is needed because you also aggregate. Pandas: drop_duplicates, unique, nunique and groupby.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `SELECT DISTINCT` and `GROUP BY` with no aggregate return the same rows; use `GROUP BY` when you also need an aggregate, and note that both treat NULLs as one value, while `COUNT(DISTINCT col)` skips NULLs.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, city TEXT);
INSERT INTO orders VALUES
 (1,10,'paid','Pune'),(2,10,'paid','Pune'),(3,10,'paid','Delhi'),
 (4,20,'refunded','Pune'),(5,20,NULL,'Pune'),(6,30,NULL,NULL),
 (7,NULL,'paid','Delhi'),(8,NULL,'paid','Delhi');
```

**SQL answer:** `d1`, `d2`, `g1`, `agg`, `portable` and `only_complete` in the Code block.

**pandas answer:** `drop_duplicates`, `unique`, `nunique` and `groupby(...).agg(...)` in the Code block.

**Example:** `status` values are paid, paid, paid, refunded, NULL, NULL, paid, paid, so `DISTINCT status` returns NULL, paid, refunded (3 values: the two NULLs collapse into one). `DISTINCT customer_id, city` returns 5 pairs: (NULL, Delhi), (10, Delhi), (10, Pune), (20, Pune), (30, NULL). `COUNT(DISTINCT customer_id)` is 3 (10, 20, 30; the NULL customer is not counted), but counting the `DISTINCT customer_id` subquery rows gives 4 because the NULL is a row there.

**Code:** run with `python3 -I`.
```python
# SELECT DISTINCT vs GROUP BY, NULLs, COUNT(DISTINCT) variants (Q19).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, city TEXT);
INSERT INTO orders VALUES
 (1,10,'paid','Pune'),(2,10,'paid','Pune'),(3,10,'paid','Delhi'),
 (4,20,'refunded','Pune'),(5,20,NULL,'Pune'),(6,30,NULL,NULL),
 (7,NULL,'paid','Delhi'),(8,NULL,'paid','Delhi');
""")
def rows(q): return con.execute(q).fetchall()

d1 = "SELECT DISTINCT status FROM orders ORDER BY status"
d2 = "SELECT DISTINCT customer_id, city FROM orders ORDER BY customer_id, city"
g1 = "SELECT status FROM orders GROUP BY status ORDER BY status"
print("DISTINCT status:", rows(d1))
print("GROUP BY status:", rows(g1), "(same rows)")
print("DISTINCT customer_id, city:", rows(d2))
assert rows(d1) == rows(g1)

print("COUNT(DISTINCT customer_id):", rows("SELECT COUNT(DISTINCT customer_id) FROM orders")[0][0], "(NULL not counted)")
print("COUNT(*) over DISTINCT customer_id subquery:", rows("SELECT COUNT(*) FROM (SELECT DISTINCT customer_id FROM orders)")[0][0], "(NULL counted as a value)")
try:
    con.execute("SELECT COUNT(DISTINCT customer_id, city) FROM orders")
except sqlite3.Error as e:
    print("COUNT(DISTINCT a, b) in SQLite ->", type(e).__name__, e)
portable = "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, city FROM orders)"
print("pairs via subquery (NULL pairs kept):", rows(portable)[0][0])
only_complete = "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, city FROM orders WHERE customer_id IS NOT NULL AND city IS NOT NULL)"
print("pairs with no NULLs (what a multi-column COUNT(DISTINCT) would give where supported):", rows(only_complete)[0][0])

# GROUP BY is needed when you also aggregate
agg = "SELECT customer_id, COUNT(*) AS n_orders, COUNT(DISTINCT city) AS n_cities FROM orders GROUP BY customer_id ORDER BY customer_id"
print("GROUP BY with aggregates:", rows(agg))

# pandas
df = pd.read_sql("SELECT * FROM orders", con)
p1 = df[["status"]].drop_duplicates().sort_values("status", na_position="first").reset_index(drop=True)
print("pandas drop_duplicates on status:", p1["status"].tolist())
print("unique():", df["status"].unique().tolist())
print("nunique() default dropna=True:", df["customer_id"].nunique(), "| dropna=False:", df["customer_id"].nunique(dropna=False))
p2 = df[["customer_id", "city"]].drop_duplicates()
print("pairs via drop_duplicates:", len(p2), "| NULL-free pairs:", len(p2.dropna()))
sql_d2 = pd.read_sql(d2, con)
p2s = p2.sort_values(["customer_id", "city"], na_position="first").reset_index(drop=True)
assert list(map(tuple, sql_d2.astype(object).where(sql_d2.notna(), None).values.tolist())) == \
       list(map(tuple, p2s.astype(object).where(p2s.notna(), None).values.tolist()))
sql_agg = pd.read_sql(agg, con)
p_agg = (df.groupby("customer_id", dropna=False).agg(n_orders=("order_id", "size"), n_cities=("city", "nunique"))
         .reset_index().sort_values("customer_id", na_position="first").reset_index(drop=True))
pd.testing.assert_frame_equal(sql_agg, p_agg, check_dtype=False)
assert rows("SELECT COUNT(DISTINCT customer_id) FROM orders")[0][0] == df["customer_id"].nunique()
assert rows(portable)[0][0] == len(p2) and rows(only_complete)[0][0] == len(p2.dropna())
print("asserts passed (sorted with NULL first, as SQLite does)")
```

**Output (my run):**
```text
DISTINCT status: [(None,), ('paid',), ('refunded',)]
GROUP BY status: [(None,), ('paid',), ('refunded',)] (same rows)
DISTINCT customer_id, city: [(None, 'Delhi'), (10, 'Delhi'), (10, 'Pune'), (20, 'Pune'), (30, None)]
COUNT(DISTINCT customer_id): 3 (NULL not counted)
COUNT(*) over DISTINCT customer_id subquery: 4 (NULL counted as a value)
COUNT(DISTINCT a, b) in SQLite -> OperationalError wrong number of arguments to function COUNT()
pairs via subquery (NULL pairs kept): 5
pairs with no NULLs (what a multi-column COUNT(DISTINCT) would give where supported): 3
GROUP BY with aggregates: [(None, 2, 1), (10, 3, 2), (20, 2, 1), (30, 1, 0)]
pandas drop_duplicates on status: [nan, 'paid', 'refunded']
unique(): ['paid', 'refunded', nan]
nunique() default dropna=True: 3 | dropna=False: 4
pairs via drop_duplicates: 5 | NULL-free pairs: 3
asserts passed (sorted with NULL first, as SQLite does)
```

**Edge cases:**
- Multi-column `COUNT(DISTINCT a, b)` is not valid in SQLite (my run raised `wrong number of arguments to function COUNT()`). MySQL accepts it (and skips rows where any argument is NULL, from memory); PostgreSQL does not accept the comma form (a row-constructor form exists, with its own NULL behaviour); not executed here. The portable form is `SELECT COUNT(*) FROM (SELECT DISTINCT a, b ...)`, which counts a pair with a NULL as a value (5 here), unlike a NULL-skipping multi-column count (3).
- `DISTINCT` applies to the whole row, not to the first column: `SELECT DISTINCT a, b` is not "distinct a".
- pandas `nunique()` skips NaN by default (3), `nunique(dropna=False)` counts it (4); `unique()` keeps NaN in the output.
- `groupby` drops NaN keys unless `dropna=False`; the run used `dropna=False` to match SQL.

**Then explain:**
- **Equivalence:** `DISTINCT x` is the same result as `GROUP BY x`; engines often plan them the same way (hedged, not checked here).
- **Choose GROUP BY** when you aggregate (`COUNT(*)`, `COUNT(DISTINCT city)`); choose DISTINCT for a plain unique list.
- **NULLs:** collapsed into one value by both.
- **Counting uniques:** `COUNT(DISTINCT col)` ignores NULL; `COUNT(*)` over a DISTINCT subquery does not.
- **pandas:** `df[["status"]].drop_duplicates()` (keeps first NaN), `Series.unique()` (array, order of appearance), `nunique()` (count), `groupby(...).agg(n=("order_id", "size"))`.

**Follow-ups:**
- *Is DISTINCT slow?* It needs a sort or hash over the selected columns; use it only when duplicates are real (Part 11).
- *Why not put DISTINCT in every query?* It hides a join fan-out bug (Part 2) and costs time.
- *DISTINCT ON?* PostgreSQL-only (from memory, not executed).

**Common mistakes:**
- Thinking `COUNT(DISTINCT x)` counts NULL as a value.
- Using DISTINCT to hide a duplicate-producing join.
- Using a multi-column `COUNT(DISTINCT a, b)` and expecting it to run everywhere.

### Q20 ⭐⭐ 🟢 Column expressions and aliases: given order_items(item_id, order_id, qty, unit_price, discount_pct), write a SELECT with a computed line_total, a rounded value, and a text label built by concatenation (|| versus CONCAT, hedged). Explain alias scope, quoting aliases with spaces, integer division (qty/2 when both are integers) and implicit casting, and how the same is written in pandas with assign and round.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** A SELECT list can hold any expression; an alias names it, but an alias cannot be used in the WHERE clause of standard SQL (SQLite allows it) and dividing two integers truncates, so write `/ 100.0` or cast.

**Schema and sample data:**
```sql
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, unit_price REAL, discount_pct INTEGER);
INSERT INTO order_items VALUES
 (1,100,3,199.99,10),(2,100,5,49.50,0),(3,101,1,2.50,0),(4,101,2,15.25,25),(5,102,7,12.00,5);
```

**SQL answer:** the query is `sql` in the Code block: `line_total`, a rounded value with a quoted alias containing spaces, and a text label with `||`.

**pandas answer:** `assign(...)` with `round(2)` and string concatenation, in the Code block (`p`).

**Example:** item 1: 3 x 199.99 with 10 per cent off = 3 x 199.99 x 0.9 = 539.973, rounded 539.97. Item 3: 1 x 2.50, no discount = 2.5. Item 4: 2 x 15.25 x 0.75 = 22.875, rounded to 22.88. The label for item 1 is `Item 1 x3`. Now the integer trap: `discount_pct / 100` with `discount_pct = 10` is `0` (integer division), so the discount would vanish (my run: `(10, 0, 0.1)`). `qty / 2` for qty 5 gives 2, not 2.5.

**Code:** run with `python3 -I`.
```python
# Column expressions, aliases, integer division, rounding, concatenation (Q20).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, unit_price REAL, discount_pct INTEGER);
INSERT INTO order_items VALUES
 (1,100,3,199.99,10),(2,100,5,49.50,0),(3,101,1,2.50,0),(4,101,2,15.25,25),(5,102,7,12.00,5);
""")

sql = """
SELECT item_id,
       qty * unit_price * (1 - discount_pct / 100.0)            AS line_total,
       ROUND(qty * unit_price * (1 - discount_pct / 100.0), 2)  AS "Line Total (rounded)",
       'Item ' || item_id || ' x' || qty                        AS label
FROM order_items
ORDER BY item_id
"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

# the traps
print("qty / 2 (both integers):", con.execute("SELECT qty, qty / 2, qty / 2.0 FROM order_items ORDER BY item_id").fetchall())
print("discount_pct / 100 (integer):", con.execute("SELECT discount_pct, discount_pct / 100, discount_pct / 100.0 FROM order_items WHERE item_id IN (1,4)").fetchall())
print("alias in ORDER BY works:", con.execute("SELECT qty*unit_price AS gross FROM order_items ORDER BY gross DESC LIMIT 1").fetchall())
try:
    print("alias in WHERE (SQLite accepts it as an extension):", con.execute("SELECT qty*unit_price AS gross FROM order_items WHERE gross > 100 ORDER BY item_id").fetchall())
except sqlite3.Error as e:
    print("alias in WHERE ->", e)
print("'Item ' || NULL ->", con.execute("SELECT 'Item ' || NULL").fetchone()[0])
print("'5' + 3 =", con.execute("SELECT '5' + 3").fetchone()[0], "| typeof('5' + 3) =", con.execute("SELECT typeof('5' + 3)").fetchone()[0])

# pandas
oi = pd.read_sql("SELECT * FROM order_items", con)
p = (oi.assign(line_total=lambda d: d["qty"] * d["unit_price"] * (1 - d["discount_pct"] / 100),
               rounded=lambda d: d["line_total"].round(2),
               label=lambda d: "Item " + d["item_id"].astype(str) + " x" + d["qty"].astype(str))
       [["item_id", "line_total", "rounded", "label"]]
       .rename(columns={"rounded": "Line Total (rounded)"}))
pd.testing.assert_frame_equal(sql_df, p)
print("asserts passed: SQL == pandas (ordered by item_id, round to 2 places; float values agree exactly here)")

# pandas / in Python is TRUE division; SQL integer / is truncating. Match with //.
print("pandas qty / 2:", (oi["qty"] / 2).tolist(), "| qty // 2:", (oi["qty"] // 2).tolist())
assert (oi["qty"] // 2).tolist() == [r[0] for r in con.execute("SELECT qty / 2 FROM order_items ORDER BY item_id")]

# honest surprise: halves round differently. SQLite rounds half away from zero, numpy rounds half to even.
print("ROUND(2.5), ROUND(3.5) in SQLite:", con.execute("SELECT ROUND(2.5), ROUND(3.5)").fetchone())
print("pandas Series([2.5, 3.5]).round():", pd.Series([2.5, 3.5]).round().tolist())
```

**Output (my run):**
```text
 item_id  line_total  Line Total (rounded)     label
       1     539.973                539.97 Item 1 x3
       2     247.500                247.50 Item 2 x5
       3       2.500                  2.50 Item 3 x1
       4      22.875                 22.88 Item 4 x2
       5      79.800                 79.80 Item 5 x7
qty / 2 (both integers): [(3, 1, 1.5), (5, 2, 2.5), (1, 0, 0.5), (2, 1, 1.0), (7, 3, 3.5)]
discount_pct / 100 (integer): [(10, 0, 0.1), (25, 0, 0.25)]
alias in ORDER BY works: [(599.97,)]
alias in WHERE (SQLite accepts it as an extension): [(599.97,), (247.5,)]
'Item ' || NULL -> None
'5' + 3 = 8 | typeof('5' + 3) = integer
asserts passed: SQL == pandas (ordered by item_id, round to 2 places; float values agree exactly here)
pandas qty / 2: [1.5, 2.5, 0.5, 1.0, 3.5] | qty // 2: [1, 2, 0, 1, 3]
ROUND(2.5), ROUND(3.5) in SQLite: (3.0, 4.0)
pandas Series([2.5, 3.5]).round(): [2.0, 4.0]
```

**Edge cases:**
- Alias scope: you can use an alias in `ORDER BY`; standard SQL evaluates `WHERE` before the SELECT list, so aliases are not visible there. SQLite accepted `WHERE gross > 100` anyway (shown in the run); PostgreSQL and SQL Server reject it (from memory, not executed). Repeat the expression or use a subquery or CTE.
- NULL: `'Item ' || NULL` is NULL in SQLite (shown in the run). `CONCAT` ignores NULLs in MySQL and PostgreSQL (from memory, not executed).
- Rounding of exact halves differs: SQLite `ROUND(2.5)` is 3.0, pandas `Series([2.5, 3.5]).round()` gave `[2.0, 4.0]` (round half to even). In this data the 22.875 case agreed (22.88 in both) and I did not hit a conflict in the two-decimal results, but a half at the rounding digit can differ between engines; a decimal type or integer cents is safer for money.
- Implicit casting: in SQLite `'5' + 3` gave the integer 8; other engines are stricter or differ (from memory, not executed).

**Then explain:**
- **Computed column:** `qty * unit_price * (1 - discount_pct / 100.0) AS line_total`.
- **Quoting an alias with spaces:** double quotes in standard SQL (`"Line Total (rounded)"`); MySQL uses backticks, SQL Server brackets (from memory, not executed). Avoid spaces in real code.
- **Concatenation:** `||` is standard (SQLite, PostgreSQL, Oracle); `CONCAT()` in MySQL, SQL Server and others; in MySQL `||` is logical OR by default (from memory, not executed).
- **Integer division:** `qty / 2` with two integers truncates in SQLite (and in PostgreSQL, SQL Server; MySQL's `/` returns a decimal, with `DIV` for integer division; from memory, not executed). Write `qty / 2.0` or `CAST(qty AS REAL) / 2`.
- **pandas:** `assign(line_total=..., rounded=lambda d: d["line_total"].round(2))`; `/` is true division, `//` matches SQL's truncation for non-negative numbers (for negatives floor and truncation differ).

**Follow-ups:**
- *Why not alias in WHERE?* The WHERE clause runs before SELECT is computed (execution order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY).
- *How do you round money?* Store integer minor units or a decimal type; round at the end.
- *What about floating-point display?* `0.1 + 0.2` style noise; round for display, not for storage.

**Common mistakes:**
- `discount_pct / 100` with integers, silently giving no discount.
- Using an alias in WHERE and having it fail on the next database.
- Rounding in the middle of a calculation and then summing.
- Assuming `ROUND` and `numpy.round` agree on halves.

### Q21 ⭐⭐ 🟢 String filtering basics: customers(customer_id, name, email, city). Write filters for names starting with 'A', emails ending in '@gmail.com', cities in a list, case-insensitive match (ILIKE, LOWER, COLLATE, hedged), and a name containing a literal underscore. Explain why a leading wildcard usually prevents index use (light note; Part 11 has indexes) and the pandas str.startswith, str.contains(case=False, regex=False) and na handling.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** use `LIKE 'A%'` for starts-with, `LIKE '%@gmail.com'` for ends-with, `IN (...)` for lists, `ESCAPE` for a literal `_` or `%`, and `LOWER(col) LIKE LOWER(...)` for a case-insensitive match that works everywhere; remember that `_` is a wildcard and NULL never matches.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@gmail.com','Pune'),
 (2,'arjun','arjun@Gmail.com','Delhi'),
 (3,'Ben','ben@work.in','Mumbai'),
 (4,'A_B Traders','ab@gmail.com','Pune'),
 (5,'Chitra',NULL,'Delhi'),
 (6,'Aman','aman@gmail.com.fake','Chennai'),
 (7,'Dev','dev@gmail.com',NULL),
 (8,'AxB Co','x@y.com','Pune');
```

**SQL answer:** the queries `q_start`, `q_start_cs`, `q_end`, `q_in`, `q_ci`, `q_nocase`, `q_under` and `q_under_wrong` in the Code block.

**pandas answer:** `str.startswith`, `str.endswith`, `isin`, `str.contains(..., case=False, regex=False)` and the lower-cased variants, all with `na=False`, in the Code block.

**Example:** names starting with A (SQLite, case-insensitive `LIKE`): Asha, arjun, A_B Traders, Aman, AxB Co, so ids 1, 2, 4, 6, 8. Emails ending in `@gmail.com`: ids 1, 2 (`@Gmail.com` matches because SQLite's `LIKE` ignores ASCII case), 4 and 7; the NULL email (5) and `aman@gmail.com.fake` (6) are not returned. Cities in (Pune, Delhi): 1, 2, 4, 5, 8; customer 7 has a NULL city, so it never matches. A literal underscore: `name LIKE '%\_%' ESCAPE '\'` returns only id 4. Without the escape, `'A_B%'` returns ids 4 and 8, because `_` matches any single character, so 'AxB Co' matches too.

**Code:** run with `python3 -I`.
```python
# String filtering: LIKE, IN, case-insensitive, literal underscore, NULLs, and the pandas equivalents (Q21).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@gmail.com','Pune'),
 (2,'arjun','arjun@Gmail.com','Delhi'),
 (3,'Ben','ben@work.in','Mumbai'),
 (4,'A_B Traders','ab@gmail.com','Pune'),
 (5,'Chitra',NULL,'Delhi'),
 (6,'Aman','aman@gmail.com.fake','Chennai'),
 (7,'Dev','dev@gmail.com',NULL),
 (8,'AxB Co','x@y.com','Pune');
""")
def ids(q, *a): return [r[0] for r in con.execute(q, a).fetchall()]

q_start = "SELECT customer_id FROM customers WHERE name LIKE 'A%' ORDER BY customer_id"
q_start_cs = "SELECT customer_id FROM customers WHERE name GLOB 'A*' ORDER BY customer_id"
q_end = "SELECT customer_id FROM customers WHERE email LIKE '%@gmail.com' ORDER BY customer_id"
q_in = "SELECT customer_id FROM customers WHERE city IN ('Pune','Delhi') ORDER BY customer_id"
q_ci = "SELECT customer_id FROM customers WHERE LOWER(email) LIKE '%@gmail.com' ORDER BY customer_id"
q_nocase = "SELECT customer_id FROM customers WHERE email COLLATE NOCASE LIKE '%@gmail.com' ORDER BY customer_id"
q_under = "SELECT customer_id FROM customers WHERE name LIKE '%\\_%' ESCAPE '\\' ORDER BY customer_id"
q_under_wrong = "SELECT customer_id FROM customers WHERE name LIKE 'A_B%' ORDER BY customer_id"

print("name LIKE 'A%' (SQLite LIKE ignores ASCII case):", ids(q_start))
print("name GLOB 'A*' (case-sensitive, SQLite only):", ids(q_start_cs))
print("email LIKE '%@gmail.com' (NULL email excluded, 'Gmail' matches):", ids(q_end))
print("city IN list:", ids(q_in), "(NULL city never matches IN)")
print("LOWER(email) LIKE ...:", ids(q_ci))
print("COLLATE NOCASE LIKE:", ids(q_nocase))
print("literal underscore with ESCAPE:", ids(q_under))
print("unescaped 'A_B%' (underscore is a wildcard for one character, so 'AxB Co' matches too):", ids(q_under_wrong))
print("PRAGMA case_sensitive_like makes LIKE case-sensitive:")
con.execute("PRAGMA case_sensitive_like = ON")
print("  name LIKE 'A%' now:", ids(q_start))
con.execute("PRAGMA case_sensitive_like = OFF")

# pandas
df = pd.read_sql("SELECT * FROM customers", con)
def pid(mask): return df.loc[mask, "customer_id"].tolist()
p_start_ci = pid(df["name"].str.lower().str.startswith("a", na=False))
p_start_cs = pid(df["name"].str.startswith("A", na=False))
p_end_ci = pid(df["email"].str.lower().str.endswith("@gmail.com", na=False))
p_in = pid(df["city"].isin(["Pune", "Delhi"]))
p_contains = pid(df["email"].str.contains("@GMAIL.COM", case=False, regex=False, na=False))
p_under = pid(df["name"].str.contains("_", regex=False, na=False))
print("pandas startswith 'A' case-sensitive:", p_start_cs, "| lower().startswith('a'):", p_start_ci)
print("pandas email endswith (lowercased):", p_end_ci, "| contains('@GMAIL.COM', case=False, regex=False):", p_contains)
print("raw str.startswith without na= on a NaN row ->", df["email"].str.startswith("a").tolist())
print("raw str.contains('gmail') with na default ->", df["email"].str.contains("gmail", regex=False).tolist())

assert ids(q_start) == p_start_ci and ids(q_start_cs) == p_start_cs
assert ids(q_ci) == ids(q_nocase) == p_end_ci
assert ids(q_end) == p_end_ci
assert ids(q_in) == p_in and ids(q_under) == p_under == [4]
assert ids(q_under_wrong) == [4, 8]
print("asserts passed (results compared as customer_id lists, ascending)")
```

**Output (my run):**
```text
name LIKE 'A%' (SQLite LIKE ignores ASCII case): [1, 2, 4, 6, 8]
name GLOB 'A*' (case-sensitive, SQLite only): [1, 4, 6, 8]
email LIKE '%@gmail.com' (NULL email excluded, 'Gmail' matches): [1, 2, 4, 7]
city IN list: [1, 2, 4, 5, 8] (NULL city never matches IN)
LOWER(email) LIKE ...: [1, 2, 4, 7]
COLLATE NOCASE LIKE: [1, 2, 4, 7]
literal underscore with ESCAPE: [4]
unescaped 'A_B%' (underscore is a wildcard for one character, so 'AxB Co' matches too): [4, 8]
PRAGMA case_sensitive_like makes LIKE case-sensitive:
  name LIKE 'A%' now: [1, 4, 6, 8]
pandas startswith 'A' case-sensitive: [1, 4, 6, 8] | lower().startswith('a'): [1, 2, 4, 6, 8]
pandas email endswith (lowercased): [1, 2, 4, 7] | contains('@GMAIL.COM', case=False, regex=False): [1, 2, 4, 6, 7]
raw str.startswith without na= on a NaN row -> [True, True, False, True, False, True, False, False]
raw str.contains('gmail') with na default -> [True, False, False, True, False, True, True, False]
asserts passed (results compared as customer_id lists, ascending)
```

**Edge cases:**
- Case sensitivity is a per-engine surprise: SQLite `LIKE` is case-insensitive for ASCII (shown: 1, 2, 4, 6, 8), `GLOB` and `PRAGMA case_sensitive_like = ON` make it case-sensitive (1, 4, 6, 8). PostgreSQL `LIKE` is case-sensitive and has `ILIKE`; in MySQL and SQL Server it depends on the column collation (all from memory, not executed). `LOWER(col) LIKE ...` is portable. `COLLATE NOCASE` is SQLite-specific syntax (other engines name collations differently).
- NULL: `NULL LIKE '%x'` is UNKNOWN, so the row is dropped; `NOT LIKE` drops it as well.
- `IN` with a NULL city: never matches (see Q13 for the NOT IN trap).
- pandas on NaN: in my pandas 3.0.5 run `str.startswith("a")` returned `False` for the NaN row, but older object-dtype columns returned NaN (from memory), which breaks a boolean mask. Always pass `na=False`.
- `str.contains` is a substring test, not an ends-with test: `contains("@GMAIL.COM", case=False, regex=False)` also matched id 6 (`aman@gmail.com.fake`), so it returned 1, 2, 4, 6, 7 versus the SQL answer 1, 2, 4, 7.

**Then explain:**
- **Wildcards:** `%` means any run of characters, `_` means exactly one.
- **Literal underscore or percent:** `LIKE '%\_%' ESCAPE '\'`; the escape character is chosen by the `ESCAPE` clause in standard SQL.
- **Leading wildcard and indexes (light note):** `LIKE '%gmail.com'` cannot use an ordinary B-tree index to seek, because the start of the string is unknown; `LIKE 'A%'` often can (hedged: it depends on the engine and collation; Part 11 covers indexes).
- **pandas:** `str.contains(case=False, regex=False)` treats the pattern literally, which avoids regex metacharacters such as `.` and `_`.
- **Case-insensitive options:** `LOWER`, `ILIKE` (PostgreSQL), `COLLATE` (engine-specific).

**Follow-ups:**
- *Regex?* `REGEXP`, `~` or `RLIKE` depending on the engine (not executed here); SQLite needs a user function for REGEXP.
- *How would you match the domain exactly?* Extract it (for example with `SUBSTR` and `INSTR` after the `@`) and compare for equality, instead of pattern-matching the whole address.
- *Trim spaces?* Clean with `TRIM` first (Part 10).

**Common mistakes:**
- Forgetting that `_` is a wildcard.
- Assuming `LIKE` is case-sensitive (or case-insensitive) in every database.
- Using `str.contains` with the default `regex=True` and a pattern with `.`, `+` or `(`.
- No `na=False`, then a mask with NaN fails on indexing.

### Q22 ⭐⭐ 🟡 LIMIT and OFFSET for pagination: orders(order_id, created_at, amount). Show page 3 with 10 rows per page, why OFFSET gets slower on deep pages, why pages can overlap or skip rows if the sort key has ties or rows are inserted between requests, and the keyset (seek) alternative with WHERE (created_at, order_id) < (...) (row-value syntax is not available everywhere; hedge). Pandas: iloc slicing and head/tail, nlargest with offset from the pandas docs.
**Asked at:** interview-prep guide and platform question bank (StrataScratch, DataLemur style), not a candidate report; product-company data scientist screens
**Say this first (1 line):** page N is `ORDER BY ... LIMIT 10 OFFSET (N-1)*10`, which needs a total order (add the unique key) and gets slower on deep pages and unstable when rows arrive; for infinite scroll use keyset pagination, `WHERE (created_at, order_id) < (last_created_at, last_order_id)`.

**Schema and sample data:** 30 orders, two per day so `created_at` has ties: order `i` (1 to 30) has `created_at = '2025-03-' || day` with `day = (i - 1) / 2 + 1` (orders 1 and 2 on 2025-03-01, 3 and 4 on 03-02, ..., 29 and 30 on 03-15) and `amount = 100 + 10 * i`. The Code block creates it with `executemany`.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, created_at TEXT, amount INTEGER);
-- 30 rows built by the Python loop in the Code block
```

**SQL answer:** `page3` (offset form), `keyset_rv` (row-value keyset) and `keyset_or` (expanded keyset) in the Code block.

**pandas answer:** `ordered.iloc[20:30]`, and the pandas-docs idiom `nlargest(30, ...).tail(10)`, in the Code block.

**Example:** sorted newest first with `order_id` as the tie-breaker the list is 30, 29, 28, ..., 1. Page 1 is 30..21, page 2 is 20..11, page 3 (`OFFSET 20 LIMIT 10`) is 10..1. If a new order 31 arrives after the client fetched page 1, page 2 now starts one row lower: my run returned 21..12, so order 21 appears on both pages. Keyset page 2 after order 30..21 uses the last row (2025-03-11, id 21): `(created_at, order_id) < ('2025-03-11', 21)` gives 20..11 again, even after order 31 is inserted.

**Code:** run with `python3 -I`.
```python
# LIMIT/OFFSET pagination, its failure modes, and keyset (seek) pagination (Q22).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, created_at TEXT, amount INTEGER)")
# 30 orders, two per day (so created_at has ties): ids 1,2 on 2025-03-01; 3,4 on 2025-03-02; ... 29,30 on 2025-03-15
rows = [(i, f"2025-03-{(i - 1) // 2 + 1:02d}", 100 + 10 * i) for i in range(1, 31)]
con.executemany("INSERT INTO orders VALUES (?,?,?)", rows)

PAGE, N = 10, 3
page3 = f"SELECT order_id, created_at FROM orders ORDER BY created_at DESC, order_id DESC LIMIT {PAGE} OFFSET {(N - 1) * PAGE}"
r3 = con.execute(page3).fetchall()
print("page 3 (OFFSET 20):", [r[0] for r in r3])

page1 = "SELECT order_id FROM orders ORDER BY created_at DESC, order_id DESC LIMIT 10 OFFSET 0"
page2 = "SELECT order_id FROM orders ORDER BY created_at DESC, order_id DESC LIMIT 10 OFFSET 10"
p1 = [r[0] for r in con.execute(page1)]
print("page 1:", p1)

# a new order arrives between requests -> offset pages shift
con.execute("INSERT INTO orders VALUES (31,'2025-03-16',999)")
p2_after_insert = [r[0] for r in con.execute(page2)]
print("page 2 after a new order arrived:", p2_after_insert, "-> repeats", sorted(set(p1) & set(p2_after_insert)), "from page 1")
con.execute("DELETE FROM orders WHERE order_id = 31")

# ties: sort key without the tie-breaker (created_at only) can split a tie group unpredictably between pages
tie_q = "SELECT order_id FROM orders ORDER BY created_at DESC LIMIT 3 OFFSET {}"
print("created_at-only order, pages of 3 (engine's tie order, not guaranteed):",
      [[r[0] for r in con.execute(tie_q.format(o))] for o in (0, 3)])

# keyset (seek): continue after the last row of page 1 with a row-value comparison
last = con.execute("SELECT created_at, order_id FROM orders WHERE order_id = ?", (p1[-1],)).fetchone()
keyset_rv = ("SELECT order_id FROM orders WHERE (created_at, order_id) < (?, ?) "
             "ORDER BY created_at DESC, order_id DESC LIMIT 10")
keyset_or = ("SELECT order_id FROM orders WHERE created_at < ? OR (created_at = ? AND order_id < ?) "
             "ORDER BY created_at DESC, order_id DESC LIMIT 10")
k_rv = [r[0] for r in con.execute(keyset_rv, last)]
k_or = [r[0] for r in con.execute(keyset_or, (last[0], last[0], last[1]))]
print("keyset page 2 (row values):", k_rv)
print("keyset page 2 (expanded OR):", k_or)

# after a new row arrives, keyset page 2 is unchanged
con.execute("INSERT INTO orders VALUES (31,'2025-03-16',999)")
print("keyset page 2 after insert:", [r[0] for r in con.execute(keyset_rv, last)])
con.execute("DELETE FROM orders WHERE order_id = 31")

# pandas
df = pd.read_sql("SELECT * FROM orders", con)
ordered = df.sort_values(["created_at", "order_id"], ascending=False).reset_index(drop=True)
pp3 = ordered.iloc[(N - 1) * PAGE : N * PAGE]
print("pandas iloc[20:30]:", pp3["order_id"].tolist())
# nlargest then tail is the pandas docs' idiom for LIMIT/OFFSET (tail of the top 30 = rows 21-30)
# nlargest needs numeric or datetime columns, so convert the text date first
df2 = df.assign(day=pd.to_datetime(df["created_at"]))
nl = df2.nlargest(30, ["day", "order_id"]).tail(10)
print("nlargest(30, ['day','order_id']).tail(10):", nl["order_id"].tolist())
try:
    df.nlargest(3, "created_at")
except TypeError as e:
    print("nlargest on a text column ->", type(e).__name__, e)

assert [r[0] for r in r3] == pp3["order_id"].tolist() == nl["order_id"].tolist()
assert k_rv == k_or == [r[0] for r in con.execute(page2)] == ordered.iloc[10:20]["order_id"].tolist()
print("asserts passed (all compared in order, newest first with order_id tie-break)")
```

**Output (my run):**
```text
page 3 (OFFSET 20): [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
page 1: [30, 29, 28, 27, 26, 25, 24, 23, 22, 21]
page 2 after a new order arrived: [21, 20, 19, 18, 17, 16, 15, 14, 13, 12] -> repeats [21] from page 1
created_at-only order, pages of 3 (engine's tie order, not guaranteed): [[29, 30, 27], [28, 25, 26]]
keyset page 2 (row values): [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
keyset page 2 (expanded OR): [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
keyset page 2 after insert: [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
pandas iloc[20:30]: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
nlargest(30, ['day','order_id']).tail(10): [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
nlargest on a text column -> TypeError Column 'created_at' has dtype str, cannot use method 'nlargest' with this dtype
asserts passed (all compared in order, newest first with order_id tie-break)
```

**Edge cases:**
- Ties: with `ORDER BY created_at DESC` alone (no `order_id`), the order inside a day is the engine's choice; my run printed pages `[29, 30, 27]` and `[28, 25, 26]`, which is not even consistent within a day, and rows can skip or repeat across pages.
- Inserts or deletes between requests shift OFFSET pages (shown: a repeated row).
- Offset beyond the end returns an empty page.
- Row-value comparison `(a, b) < (x, y)` ran in SQLite 3.45; PostgreSQL and MySQL support it (from memory); SQL Server does not (from memory, not executed). Where it is missing use the expanded form `created_at < ? OR (created_at = ? AND order_id < ?)`, which I also ran.
- Row-value comparison against a NULL key is UNKNOWN; keyset needs non-null sort columns.
- `nlargest` does not work on a text column (my run raised `TypeError`); convert the date first.

**Then explain:**
- **Page 3 of 10:** `LIMIT 10 OFFSET 20`.
- **Why deep pages get slow:** the database still has to produce and discard the first 20 (or 20,000) rows before returning the next 10 (a general statement, not timed here).
- **Why pages shift:** OFFSET counts positions, not rows; a new row at the top moves every later row down by one.
- **Keyset:** remember the last key and ask for rows after it; cost does not grow with page depth when an index matches the sort order (hedged; Part 11), and it is stable under inserts. Its limits: no jumping to page N, and it needs a unique sort key.
- **Standard syntax:** `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` (SQL Server, Oracle 12c+, PostgreSQL), `LIMIT/OFFSET` in SQLite, PostgreSQL, MySQL (from memory, not executed except SQLite).
- **pandas:** `iloc[20:30]` after sorting; `head(30).tail(10)`; `nlargest(30, cols).tail(10)` is the pandas docs' LIMIT/OFFSET idiom.

**Follow-ups:**
- *Does a client see duplicates with keyset pagination?* Not from inserts above the cursor; deletes of the cursor row are fine because you compare on values.
- *How do you show "page 3 of N"?* `COUNT(*)` separately; or avoid the total.
- *Total order needs what?* A unique tie-breaker such as the primary key.

**Common mistakes:**
- `OFFSET` without a unique `ORDER BY`.
- Using `OFFSET` for million-row exports.
- Writing the keyset condition only on `created_at`, which skips tied rows.
- Mixing ascending and descending columns in a row-value comparison (it needs one direction).

### Q23 ⭐⭐ 🟡 GROUP BY ordinals and aliases, and ORDER BY ordinals: write 'SELECT status, COUNT(*) FROM orders GROUP BY 1 ORDER BY 2 DESC' and explain what the numbers mean, which dialects accept aliases in GROUP BY (hedged), why ordinals are fragile when the SELECT list changes, and the style used in team code. Include the pandas equivalent value_counts() and groupby().size().sort_values().
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `GROUP BY 1 ORDER BY 2 DESC` means group by the first SELECT column and sort by the second; it is a quick shortcut in ad-hoc work, but it silently changes meaning when the SELECT list changes, so team code usually names the columns.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'completed'),(2,'completed'),(3,'completed'),(4,'cancelled'),(5,'cancelled'),
 (6,'refunded'),(7,'pending'),(8,NULL),(9,NULL);
```

**SQL answer:** `q` (ordinals, with a tie-breaker `, 1`) and `q_alias` (names) in the Code block; the assert shows they return the same rows.

**pandas answer:** `value_counts(dropna=False)` and `groupby("status", dropna=False).size()`, each sorted by `n` descending then `status`, as `v` and `g` in the Code block.

**Example:** statuses: completed 3, cancelled 2, NULL 2, refunded 1, pending 1. `GROUP BY 1` groups by `status` (the first SELECT item) and `ORDER BY 2 DESC` sorts by `COUNT(*)`. The result in my run is completed 3, NULL 2, cancelled 2, pending 1, refunded 1. The tie between NULL and cancelled (2 each) and between pending and refunded (1 each) is why I added `, 1` as a tie-breaker; SQLite puts NULL before text in ascending order.

**Code:** run with `python3 -I`.
```python
# GROUP BY / ORDER BY ordinals and aliases (Q23), plus pandas value_counts and groupby().size().
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'completed'),(2,'completed'),(3,'completed'),(4,'cancelled'),(5,'cancelled'),
 (6,'refunded'),(7,'pending'),(8,NULL),(9,NULL);
""")

q = "SELECT status, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC, 1"
q_alias = "SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY n DESC, status"
print("GROUP BY 1 ORDER BY 2 DESC, 1:", con.execute(q).fetchall())
assert con.execute(q).fetchall() == con.execute(q_alias).fetchall()

# fragility: reorder the SELECT list and the ordinal silently points at another column
frag = "SELECT COUNT(*) AS n, status FROM orders GROUP BY 1 ORDER BY 2"
print("reordered SELECT, ordinals updated by hand (correct):", con.execute("SELECT COUNT(*) AS n, status FROM orders GROUP BY 2 ORDER BY 1 DESC, 2").fetchall())
# someone inserts a column before COUNT(*): ORDER BY 2 now silently sorts by first_id, no error
print("column inserted, ORDER BY 2 left alone (silently wrong):",
      con.execute("SELECT status, MIN(order_id) AS first_id, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC").fetchall())
try:
    print(con.execute(frag).fetchall())
except sqlite3.Error as e:
    print("reordered SELECT but GROUP BY 1 not updated (column 1 is now COUNT(*)) ->", type(e).__name__, e)
try:
    con.execute("SELECT status, COUNT(*) FROM orders GROUP BY 1 ORDER BY 3")
except sqlite3.Error as e:
    print("ORDER BY 3 with two columns ->", type(e).__name__, e)

# alias in GROUP BY, alias of an expression
q_expr = "SELECT LENGTH(COALESCE(status,'')) AS len, COUNT(*) AS n FROM orders GROUP BY len ORDER BY len"
print("alias of an expression in GROUP BY (SQLite accepts):", con.execute(q_expr).fetchall())

# pandas: three equivalents. value_counts and groupby both drop NaN by default; SQL keeps the NULL group.
orders = pd.read_sql("SELECT * FROM orders", con)
sql_df = pd.read_sql(q, con)
v = (orders["status"].value_counts(dropna=False).rename("n").rename_axis("status").reset_index()
     .sort_values(["n", "status"], ascending=[False, True], na_position="first").reset_index(drop=True))
g = (orders.groupby("status", dropna=False).size().rename("n").reset_index()
     .sort_values(["n", "status"], ascending=[False, True], na_position="first").reset_index(drop=True))
print("value_counts() default (NaN dropped):", orders["status"].value_counts().to_dict())
print("groupby().size() default (NaN dropped):", orders.groupby("status").size().to_dict())
print(g.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, v)
pd.testing.assert_frame_equal(sql_df, g)
print("asserts passed (n DESC, status ASC tie-break; NULL status sorts first inside the tie, as in SQLite)")
```

**Output (my run):**
```text
GROUP BY 1 ORDER BY 2 DESC, 1: [('completed', 3), (None, 2), ('cancelled', 2), ('pending', 1), ('refunded', 1)]
reordered SELECT, ordinals updated by hand (correct): [(3, 'completed'), (2, None), (2, 'cancelled'), (1, 'pending'), (1, 'refunded')]
column inserted, ORDER BY 2 left alone (silently wrong): [(None, 8, 2), ('pending', 7, 1), ('refunded', 6, 1), ('cancelled', 4, 2), ('completed', 1, 3)]
reordered SELECT but GROUP BY 1 not updated (column 1 is now COUNT(*)) -> OperationalError aggregate functions are not allowed in the GROUP BY clause
ORDER BY 3 with two columns -> OperationalError 1st ORDER BY term out of range - should be between 1 and 2
alias of an expression in GROUP BY (SQLite accepts): [(0, 2), (7, 1), (8, 1), (9, 5)]
value_counts() default (NaN dropped): {'completed': 3, 'cancelled': 2, 'refunded': 1, 'pending': 1}
groupby().size() default (NaN dropped): {'cancelled': 2, 'completed': 3, 'pending': 1, 'refunded': 1}
   status  n
completed  3
      NaN  2
cancelled  2
  pending  1
 refunded  1
asserts passed (n DESC, status ASC tie-break; NULL status sorts first inside the tie, as in SQLite)
```

**Edge cases:**
- Fragility, run: if you reorder the SELECT list to `COUNT(*), status` and leave `GROUP BY 1`, SQLite raises `aggregate functions are not allowed in the GROUP BY clause`. If a column is inserted before `COUNT(*)` and `ORDER BY 2` stays, there is no error: my run silently sorted by `MIN(order_id)` instead of the count.
- An ordinal beyond the SELECT list is an error (`1st ORDER BY term out of range`).
- Alias of an expression in GROUP BY: SQLite accepted `GROUP BY len`. Support elsewhere, from memory and not executed: PostgreSQL, MySQL, BigQuery and Snowflake accept aliases (and ordinals) in GROUP BY; SQL Server does not accept an alias or ordinal in GROUP BY (it does in ORDER BY); Oracle's support varies by version. Treat this as a list to verify.
- Ties in `n`: `value_counts` and `sort_values` order of ties is not something to depend on; add the key as a second sort column in both.
- NULLs: SQL keeps the NULL group; `value_counts()` and `groupby().size()` drop NaN by default (the default `value_counts()` printed no NaN entry). I used `dropna=False` to match.

**Then explain:**
- **Ordinals** are 1-based positions in the SELECT list.
- **Fragile:** adding, removing or reordering SELECT columns changes the meaning, sometimes without any error.
- **Team style:** name the columns in `GROUP BY` and `ORDER BY` for production code; ordinals are accepted in exploration. The alias in `ORDER BY` is allowed everywhere, since ORDER BY runs after SELECT.
- **pandas:** `orders["status"].value_counts()` is the one-liner; `groupby("status").size().sort_values(ascending=False)` is the long form and lets you add more keys.

**Follow-ups:**
- *Why can ORDER BY use an alias but WHERE cannot?* ORDER BY is evaluated after SELECT.
- *Does `GROUP BY 1` hurt performance?* No, it is syntax only.
- *How do you break ties in pandas?* `sort_values(["n", "status"], ascending=[False, True])`.

**Common mistakes:**
- Editing the SELECT list and forgetting the ordinals.
- Leaving ties unbroken, then a flaky output order.
- Forgetting that pandas drops the NULL group by default.
