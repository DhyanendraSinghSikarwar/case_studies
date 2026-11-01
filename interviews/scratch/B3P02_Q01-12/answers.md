### Q1 ⭐⭐⭐ 🟢 Explain INNER, LEFT, RIGHT, FULL OUTER and CROSS joins. Using customers(customer_id, name, city) and orders(order_id, customer_id, amount), where one customer has no orders and one order has a NULL customer_id, say which rows each join type returns and how many, why RIGHT JOIN is rarely needed (it is a LEFT JOIN with the tables swapped), and which engines support FULL OUTER JOIN (state SQLite 3.39+ and MySQL as hedged dialect facts). Give the pandas how= equivalents.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** INNER keeps only matching pairs, LEFT keeps every left row, RIGHT keeps every right row, FULL keeps every row from both sides, and CROSS pairs every row with every row; with 4 customers and 5 orders (one customer without orders, one order with a NULL customer) the counts are 4, 5, 5, 6 and 20.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Delhi');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,3,20);
```
Dev (4) has no orders. Order 104 has a NULL customer_id.

**SQL answer:** the five queries are in the Code block as `sql["inner"]`, `sql["left"]`, `sql["right"]`, `sql["outer"]` and `sql["cross"]`, all joined `ON o.customer_id = c.customer_id` (CROSS has no ON). `sql_swapped` is the RIGHT JOIN rewritten as a LEFT JOIN with the tables swapped.

**pandas answer:** `customers.merge(orders, how=..., left_on=..., right_on=...)` with `how` equal to `"inner"`, `"left"`, `"right"`, `"outer"` (that is FULL OUTER) or `"cross"` (no keys). The mapping is one to one: inner = INNER JOIN, left = LEFT JOIN, right = RIGHT JOIN, outer = FULL OUTER JOIN, cross = CROSS JOIN.

**Example:** walk the five orders by hand.
- INNER: 101 and 102 match Asha, 103 matches Ben, 105 matches Chitra. Order 104 has a NULL key, which equals nothing. Dev matches nothing. Result: 4 rows.
- LEFT (all customers kept): the 4 matched rows plus Dev with NULL order columns. 5 rows. Order 104 is not shown because it is on the right side.
- RIGHT (all orders kept): the 4 matched rows plus order 104 with NULL customer columns. 5 rows. Dev is not shown.
- FULL: the 4 matched rows plus Dev plus order 104. 6 rows. That is 4 + 1 + 1: matches, unmatched left, unmatched right.
- CROSS: 4 x 5 = 20 rows, no condition at all.

**Code:** run with `python3 -I`. Rows are compared after sorting every row (NaN turned into None, whole floats into ints).
```python
# Q1: the five join types on one small dataset, SQL (SQLite 3.45) versus pandas how=.
import sqlite3
import pandas as pd

print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Delhi');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,3,20);
""")

COLS = "c.customer_id AS c_id, c.name, o.order_id, o.customer_id AS o_cust, o.amount"
sql = {
 "inner": f"SELECT {COLS} FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id",
 "left":  f"SELECT {COLS} FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id",
 "right": f"SELECT {COLS} FROM customers c RIGHT JOIN orders o ON o.customer_id = c.customer_id",
 "outer": f"SELECT {COLS} FROM customers c FULL OUTER JOIN orders o ON o.customer_id = c.customer_id",
 "cross": f"SELECT {COLS} FROM customers c CROSS JOIN orders o",
}
# RIGHT JOIN is a LEFT JOIN with the tables swapped (same rows, columns listed the same way)
sql_swapped = f"SELECT {COLS} FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id"

def rows(items):
    """Normalise to a sorted list of tuples: NaN -> None, whole floats -> int."""
    out = []
    for r in items:
        t = []
        for x in r:
            if x is None or (isinstance(x, float) and x != x): x = None
            elif isinstance(x, float) and x.is_integer(): x = int(x)
            t.append(x)
        out.append(tuple(t))
    return sorted(out, key=lambda t: tuple((v is None, str(v)) for v in t))

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con).rename(columns={"customer_id": "o_cust"})
orders["c_key"] = orders["o_cust"]          # keep both key columns visible, like the SQL output
customers["c_id"] = customers["customer_id"]

for how in ["inner", "left", "right", "outer", "cross"]:
    s = rows(con.execute(sql[how]).fetchall())
    if how == "cross":
        p = customers.merge(orders, how="cross")
    else:
        p = customers.merge(orders, how=how, left_on="c_id", right_on="c_key")
    p = rows(p[["c_id", "name", "order_id", "o_cust", "amount"]].itertuples(index=False, name=None))
    assert s == p, how                      # compared after sorting all rows
    print(f"{how:5s} -> {len(s):2d} rows (SQL == pandas)")

assert rows(con.execute(sql["right"]).fetchall()) == rows(con.execute(sql_swapped).fetchall())
print("RIGHT JOIN == swapped LEFT JOIN: True")
print("\nFULL OUTER rows (order_id sort, None = NULL):")
for r in sorted(rows(con.execute(sql["outer"]).fetchall()), key=lambda t: (t[2] is None, t[2] or 0, t[0] or 0)):
    print(r)
print("asserts passed")
```

**Output (my run):**
```text
SQLite 3.45.1 | pandas 3.0.5
inner ->  4 rows (SQL == pandas)
left  ->  5 rows (SQL == pandas)
right ->  5 rows (SQL == pandas)
outer ->  6 rows (SQL == pandas)
cross -> 20 rows (SQL == pandas)
RIGHT JOIN == swapped LEFT JOIN: True

FULL OUTER rows (order_id sort, None = NULL):
(1, 'Asha', 101, 1, 100)
(1, 'Asha', 102, 1, 50)
(2, 'Ben', 103, 2, 75)
(None, None, 104, None, 30)
(3, 'Chitra', 105, 3, 20)
(4, 'Dev', None, None, None)
asserts passed
```

**Edge cases:**
- **NULL key on the right (order 104):** it never matches, even a customer whose id is NULL, because `NULL = NULL` is not true. It only appears in RIGHT and FULL (Part 2 Q6 goes deeper).
- **Duplicates:** if a customer id were duplicated, INNER would return one row per matching pair, so the counts above are only right because `customer_id` is the primary key.
- **pandas dtype surprise:** `read_sql` turned `orders.customer_id` into `float64` because of the NULL. Merging that float key against the `int64` customer key still matched correctly in my run (all five asserts passed), so the float is a display issue here, not a wrong join. Part 2 Q35 covers dtype mismatches that do break.
- **Empty side:** an empty orders table gives INNER 0, LEFT = all customers, RIGHT 0, FULL = all customers, CROSS 0.

**Then explain:**
- **RIGHT is rarely needed:** `A RIGHT JOIN B` returns the same rows as `B LEFT JOIN A` (the Code block asserts this; only the column order changes, so I listed columns by name). Teams standardise on LEFT because queries then read top to bottom with the "main" table first.
- **FULL OUTER JOIN is for reconciliation:** compare two lists and see what exists in one, the other or both (Part 2 Q16).
- **CROSS JOIN has no ON:** use it on purpose (grids, combinations), never by accident (Part 2 Q30 and Q31).
- **Dialect facts (hedged):** SQLite added RIGHT and FULL OUTER JOIN in 3.39 (the version boundary is from memory; the queries above did run on SQLite 3.45.1 here). MySQL has no FULL OUTER JOIN; the MySQL 8.4 reference page I opened lists only LEFT and RIGHT [OUTER] JOIN, and the usual workaround is a LEFT JOIN UNION a RIGHT JOIN (Part 2 Q32). PostgreSQL, SQL Server, Oracle, BigQuery and Snowflake support FULL OUTER JOIN as far as I know (not executed here).
- **pandas default:** `merge` defaults to `how="inner"`, like a bare `JOIN`.

**Follow-ups:**
- *Which join returns rows from both tables that match neither side?* None of them; FULL returns unmatched rows from each side, padded with NULLs on the other.
- *Does LEFT JOIN ever return fewer rows than the left table?* No, at least one row per left row. It can return more if the right side has several matches.
- *How do I find the unmatched rows only?* LEFT JOIN with `IS NULL` on a right-side key (Part 2 Q2).

**Common mistakes:**
- Saying "LEFT JOIN returns the same number of rows as the left table" (it can grow with duplicates on the right).
- Expecting the NULL-key order to match a NULL-key customer.
- Using RIGHT JOIN in a chain of LEFT JOINs, which is hard to read.
- Forgetting that `how="outer"` in pandas is the FULL OUTER JOIN.

### Q2 ⭐⭐⭐ 🟢 Anti-join, the everyday case: using customers(customer_id, name) and orders(order_id, customer_id, amount), list customers who have never placed an order. Write it with LEFT JOIN ... WHERE o.order_id IS NULL, with NOT EXISTS, and with NOT IN, say which column you test for NULL in the LEFT JOIN form and why, and show the pandas version (merge with indicator=True, and ~isin).
**Asked at:** explainextended and SQL Server Central write-ups on NOT IN, NOT EXISTS and LEFT JOIN / IS NULL, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** For "customers with no orders" use `LEFT JOIN ... WHERE o.order_id IS NULL` or `NOT EXISTS`; avoid `NOT IN` unless the subquery column can never be NULL, and test a right-table column that is never NULL for matched rows, such as its primary key.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
-- 104 is a guest order (NULL customer); 105 belongs to Esha but its amount is NULL
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,5,NULL);
```

**SQL answer:** in the Code block: `sql_left` (LEFT JOIN with `o.order_id IS NULL`), `sql_not_exists`, `sql_not_in` (the trap), `sql_not_in_safe` (NOT NULL filter in the subquery) and `sql_wrong_col` (tests `o.amount`, which is wrong).

**pandas answer:** two forms in the Code block. `customers.merge(orders, on="customer_id", how="left", indicator=True)` then keep `_merge == "left_only"`, and `customers[~customers["customer_id"].isin(orders["customer_id"])]`.

**Example:** Asha, Ben and Esha each have an order, Chitra and Dev have none, so the answer is Chitra and Dev.
- LEFT JOIN: Chitra and Dev find no order, so their `o.order_id` is NULL and the WHERE keeps them.
- Which column to test: any column that is NULL only when the join found no match. The right table's primary key (`order_id`) is the safe choice. If I test `o.amount`, Esha's matched order 105 also has a NULL amount, so Esha would be listed wrongly. My run shows exactly that.
- NOT IN: the subquery returns 1, 1, 2, NULL, 5. For Chitra the test is `NOT (3 = 1 OR 3 = 2 OR 3 = NULL OR 3 = 5)`, which is UNKNOWN, so the row is dropped. Every customer is dropped, so the result is empty (Part 1 Q13 covers the three-valued logic).

**Code:** run with `python3 -I`. Results are compared in `customer_id` order.
```python
# Q2: anti-join three ways in SQL, plus pandas indicator and ~isin.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
-- 104 is a guest order (NULL customer); 105 belongs to Esha but its amount is NULL
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,5,NULL);
""")

sql_left = """SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL ORDER BY c.customer_id"""
sql_not_exists = """SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id"""
sql_not_in = """SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY customer_id"""
sql_not_in_safe = """SELECT name FROM customers WHERE customer_id NOT IN
(SELECT customer_id FROM orders WHERE customer_id IS NOT NULL) ORDER BY customer_id"""
sql_wrong_col = """SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount IS NULL ORDER BY c.customer_id"""   # tests a nullable data column: wrong

run = lambda q: [r[0] for r in con.execute(q).fetchall()]
print("LEFT JOIN ... o.order_id IS NULL:", run(sql_left))
print("NOT EXISTS                      :", run(sql_not_exists))
print("NOT IN (subquery has a NULL)    :", run(sql_not_in))
print("NOT IN with IS NOT NULL filter  :", run(sql_not_in_safe))
print("LEFT JOIN ... o.amount IS NULL  :", run(sql_wrong_col), "<- Esha is wrongly listed")

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

m = customers.merge(orders, on="customer_id", how="left", indicator=True)
p_ind = m.loc[m["_merge"] == "left_only", "name"].tolist()
p_isin = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
print("pandas merge indicator:", p_ind, "| pandas ~isin:", p_isin)
print(m[["name", "order_id", "_merge"]].to_string(index=False))

# all agree with the order-by-customer_id SQL results
assert run(sql_left) == run(sql_not_exists) == run(sql_not_in_safe) == p_ind == p_isin == ["Chitra", "Dev"]
assert run(sql_not_in) == []
assert run(sql_wrong_col) == ["Chitra", "Dev", "Esha"]
print("asserts passed")
```

**Output (my run):**
```text
LEFT JOIN ... o.order_id IS NULL: ['Chitra', 'Dev']
NOT EXISTS                      : ['Chitra', 'Dev']
NOT IN (subquery has a NULL)    : []
NOT IN with IS NOT NULL filter  : ['Chitra', 'Dev']
LEFT JOIN ... o.amount IS NULL  : ['Chitra', 'Dev', 'Esha'] <- Esha is wrongly listed
pandas merge indicator: ['Chitra', 'Dev'] | pandas ~isin: ['Chitra', 'Dev']
  name  order_id    _merge
  Asha     101.0      both
  Asha     102.0      both
   Ben     103.0      both
Chitra       NaN left_only
   Dev       NaN left_only
  Esha     105.0      both
asserts passed
```

**Edge cases:**
- **NULL keys on the right (guest order 104):** harmless for LEFT JOIN and NOT EXISTS, fatal for NOT IN.
- **Duplicate orders per customer:** LEFT JOIN returns one row per match, but the anti-join keeps only rows with no match, so duplicates cannot appear in the result.
- **Empty orders table:** all three safe forms return every customer.
- **pandas:** `isin` is a plain membership test. NaN in `orders["customer_id"]` does not hurt the `~isin` result here (it matched my SQL answer), but a NaN on the customer side would count as "found" if the list also had NaN (Part 1 Q13 showed that).

**Then explain:**
- **Three equivalent safe forms:** LEFT JOIN + IS NULL, NOT EXISTS, and NOT IN with an `IS NOT NULL` filter all returned Chitra and Dev in my SQLite run.
- **Performance:** I am not claiming a speed difference from this run. Optimisers in many engines turn LEFT JOIN anti-joins and NOT EXISTS into the same plan, but that is engine specific (not executed here; Part 11 covers plans).
- **pandas:** `indicator=True` adds a `_merge` column with `left_only`, `right_only`, `both`. The `isin` form needs no merge and creates no extra rows, so it is the cheaper one to read.
- **Why order_id and not customer_id?** `customer_id` would also work for matched rows (the match means it is not NULL), but using the primary key of the right table is a habit that cannot go wrong.

**Follow-ups:**
- *Why does NOT IN fail?* One NULL in the subquery makes every comparison UNKNOWN.
- *Is LEFT JOIN IS NULL faster than NOT EXISTS?* Depends on the engine; measure it (hedged, not executed here).
- *How do I get customers that have orders?* The semi-join (Part 2 Q8).

**Common mistakes:**
- `WHERE o.customer_id IS NULL` is fine, but `WHERE o.amount IS NULL` mislabels customers whose order has a NULL amount.
- Putting an extra filter on the orders table in the WHERE instead of the ON (Part 2 Q3).
- `NOT IN` against a nullable column.
- In pandas, forgetting `indicator=True` and testing a column such as `amount` for NaN, which has the same trap as the SQL.

### Q3 ⭐⭐⭐ 🟢 ON versus WHERE with a LEFT JOIN, the classic trap: customers(customer_id, name) and orders(order_id, customer_id, status, amount). Report every customer with the number of their completed orders, including customers with zero. Show why putting status = 'completed' in WHERE silently turns the LEFT JOIN into an inner join, why putting it in ON keeps the zero rows, and what changes for an INNER JOIN (nothing). Give the pandas equivalent (filter the right frame before merge).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** A filter on the right table written in WHERE removes the NULL-padded rows and turns the LEFT JOIN into an INNER JOIN; put it in ON to keep customers with zero matches, and for an INNER JOIN it makes no difference.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,'completed',100),(102,1,'completed',50),(103,1,'cancelled',40),
                          (104,2,'cancelled',75),(105,4,'completed',20);
```

**SQL answer:** in the Code block: `sql_on` (status in ON, correct), `sql_where` (status in WHERE, the trap), and `sql_inner_on` and `sql_inner_where` for the INNER JOIN case. All count with `COUNT(o.order_id)`.

**pandas answer:** filter the right frame first, then merge: `done = orders[orders["status"] == "completed"]; customers.merge(done, on="customer_id", how="left")`, then `groupby(...)["order_id"].count()`. The trap version merges first and filters after.

**Example:** The LEFT JOIN first pairs every customer with their orders. Ben has only a cancelled order, Chitra has none.
- Filter in ON: the condition decides which orders count as a match. Ben's cancelled order is not a match, so Ben is kept once with NULL order columns, and `COUNT(o.order_id)` counts 0. Chitra is the same. Asha has 2 completed matches and Dev has 1. Result: Asha 2, Ben 0, Chitra 0, Dev 1.
- Filter in WHERE: after the join, Ben's row is (cancelled), Chitra's row has `status` NULL. `NULL = 'completed'` is not true, so both rows are removed, and so is Asha's cancelled order. Result: Asha 2, Dev 1. The zero rows are gone, which is what an INNER JOIN would have given.

**Code:** run with `python3 -I`. Compared in `customer_id` order.
```python
# Q3: ON versus WHERE for a filter on the right table of a LEFT JOIN.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,'completed',100),(102,1,'completed',50),(103,1,'cancelled',40),
                          (104,2,'cancelled',75),(105,4,'completed',20);
""")

sql_on = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""
sql_where = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""
sql_inner_on = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""
sql_inner_where = """SELECT c.name, COUNT(o.order_id) AS completed_orders
FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name ORDER BY c.customer_id"""

run = lambda q: con.execute(q).fetchall()
r_on, r_where = run(sql_on), run(sql_where)
print("LEFT, filter in ON   :", r_on)
print("LEFT, filter in WHERE:", r_where)
print("INNER, filter in ON   :", run(sql_inner_on))
print("INNER, filter in WHERE:", run(sql_inner_where))

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

# pandas: filter the RIGHT frame first, then merge (this is the ON version)
done = orders[orders["status"] == "completed"]
m = customers.merge(done, on="customer_id", how="left")
p_on = (m.groupby(["customer_id", "name"], as_index=False)["order_id"].count()
         .rename(columns={"order_id": "completed_orders"}).sort_values("customer_id"))
# the trap in pandas: merge first, filter after (this is the WHERE version)
m2 = customers.merge(orders, on="customer_id", how="left")
p_where = (m2[m2["status"] == "completed"].groupby(["customer_id", "name"], as_index=False)["order_id"].count()
           .rename(columns={"order_id": "completed_orders"}).sort_values("customer_id"))
print(p_on[["name", "completed_orders"]].to_string(index=False))
print("pandas filter-after-merge rows:", p_where["name"].tolist())

as_tuples = lambda df: list(df[["name", "completed_orders"]].itertuples(index=False, name=None))
assert as_tuples(p_on) == r_on == [("Asha", 2), ("Ben", 0), ("Chitra", 0), ("Dev", 1)]
assert as_tuples(p_where) == r_where == [("Asha", 2), ("Dev", 1)]
assert run(sql_inner_on) == run(sql_inner_where) == r_where
print("asserts passed (compared in customer_id order)")
```

**Output (my run):**
```text
LEFT, filter in ON   : [('Asha', 2), ('Ben', 0), ('Chitra', 0), ('Dev', 1)]
LEFT, filter in WHERE: [('Asha', 2), ('Dev', 1)]
INNER, filter in ON   : [('Asha', 2), ('Dev', 1)]
INNER, filter in WHERE: [('Asha', 2), ('Dev', 1)]
  name  completed_orders
  Asha                 2
   Ben                 0
Chitra                 0
   Dev                 1
pandas filter-after-merge rows: ['Asha', 'Dev']
asserts passed (compared in customer_id order)
```

**Edge cases:**
- **INNER JOIN:** ON and WHERE give identical results (the run shows both are Asha 2, Dev 1) because an inner join never keeps unmatched rows anyway.
- **`WHERE o.status = 'completed' OR o.status IS NULL` is not a fix:** it rescues only customers with no orders at all (Chitra). Ben, whose only order is cancelled, is still dropped. Use ON.
- **Conditions on the left table** (for example `c.city = 'Pune'`) are safe in WHERE for a LEFT JOIN, since they filter the preserved side.
- **Other engines:** this rule is part of standard SQL semantics, so I expect the same behaviour on other engines (not executed here).

**Then explain:**
- **Why:** ON decides which rows match; WHERE filters the joined rows afterwards. Unmatched left rows have NULLs on the right, and a comparison with NULL is not true.
- **Count the right column:** `COUNT(o.order_id)` counts matches only; `COUNT(*)` would give Ben and Chitra a 1 (Part 2 Q5).
- **pandas:** there is no ON versus WHERE, just order of operations. Filtering the right frame before `merge` equals the ON version; filtering after equals the WHERE version (my run: Ben and Chitra disappear).
- **Alternative:** a conditional count, `SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END)`, over an unfiltered LEFT JOIN also keeps zeros. I did not run that variant.

**Follow-ups:**
- *Where would you put a condition on the left table?* WHERE is fine.
- *Does this apply to RIGHT JOIN?* Mirror image: filter on the left table belongs in ON.
- *Why not WHERE with IS NULL?* It rescues only customers with no orders at all, not customers with only non-completed orders, which is a different query.

**Common mistakes:**
- Writing the filter in WHERE and wondering why the zero rows vanished.
- Counting with `COUNT(*)`.
- Assuming the result changes for an INNER JOIN.
- In pandas, merging first and filtering the merged frame.

### Q4 ⭐⭐⭐ 🟢 Self join, the Employees Earning More Than Their Managers problem: employees(emp_id, name, salary, manager_id), where manager_id points to emp_id and is NULL for the top person. Write the query, explain the two aliases and why the top person never appears, and show the pandas version using merge with left_on and right_on and suffixes.
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Join the employees table to itself as `e` (employee) and `m` (manager) on `e.manager_id = m.emp_id`, then keep rows where `e.salary > m.salary`; the top person has a NULL manager_id, matches nothing, and never appears.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, manager_id INTEGER);
INSERT INTO employees VALUES (1,'Ann',90,NULL),(2,'Bob',60,1),(3,'Cy',100,1),(4,'Di',70,2),(5,'Eli',55,2);
```
Salaries are toy column data.

**SQL answer:** `sql` in the Code block (an INNER JOIN of `employees e` to `employees m`, with the salary comparison in WHERE). `sql_all` lists every employee-manager pair.

**pandas answer:** `emp.merge(emp, left_on="manager_id", right_on="emp_id", suffixes=("_emp", "_mgr"))` then filter `salary_emp > salary_mgr`.

**Example:** Pairs produced by the join: Bob-Ann, Cy-Ann, Di-Bob, Eli-Bob (Ann has no manager so she has no pair). Compare salaries: Bob 60 vs Ann 90, no. Cy 100 vs Ann 90, yes. Di 70 vs Bob 60, yes. Eli 55 vs Bob 60, no. Answer: Cy and Di.

**Code:** run with `python3 -I`. Compared in `emp_id` order.
```python
# Q4: self join, employees earning more than their managers.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, manager_id INTEGER);
INSERT INTO employees VALUES (1,'Ann',90,NULL),(2,'Bob',60,1),(3,'Cy',100,1),(4,'Di',70,2),(5,'Eli',55,2);
""")

sql = """SELECT e.name AS employee, e.salary AS emp_salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary
ORDER BY e.emp_id"""
sql_all = """SELECT e.name, m.name FROM employees e JOIN employees m ON e.manager_id = m.emp_id ORDER BY e.emp_id"""

s = con.execute(sql).fetchall()
print("SQL:", s)
print("all employee-manager pairs (Ann has no row):", con.execute(sql_all).fetchall())

emp = pd.read_sql("SELECT * FROM employees", con)
print("manager_id dtype:", emp["manager_id"].dtype)   # float64 because of the NULL
p = emp.merge(emp, left_on="manager_id", right_on="emp_id", suffixes=("_emp", "_mgr"))
p = p[p["salary_emp"] > p["salary_mgr"]].sort_values("emp_id_emp")
p = p[["name_emp", "salary_emp", "name_mgr", "salary_mgr"]]
print(p.to_string(index=False))

assert list(p.itertuples(index=False, name=None)) == s == [("Cy", 100, "Ann", 90), ("Di", 70, "Bob", 60)]
print("asserts passed (compared in emp_id order)")
```

**Output (my run):**
```text
SQL: [('Cy', 100, 'Ann', 90), ('Di', 70, 'Bob', 60)]
all employee-manager pairs (Ann has no row): [('Bob', 'Ann'), ('Cy', 'Ann'), ('Di', 'Bob'), ('Eli', 'Bob')]
manager_id dtype: float64
name_emp  salary_emp name_mgr  salary_mgr
      Cy         100      Ann          90
      Di          70      Bob          60
asserts passed (compared in emp_id order)
```

**Edge cases:**
- **Top person:** `manager_id` is NULL, so the INNER JOIN has no partner. That is correct for this question (the CEO earns more than nobody). If you need everyone listed with the manager shown, use a LEFT JOIN (Part 2 Q22).
- **Manager who left (dangling manager_id):** also dropped by the INNER JOIN.
- **Equal salaries:** `>` excludes ties.
- **pandas dtype:** `manager_id` became `float64` because of the NULL (my run printed it in the Code output above). The merge against the `int64` `emp_id` still matched correctly.
- **pandas NaN key:** the NaN manager_id has no NaN partner in `emp_id`, so no false match appears here.

**Then explain:**
- **Two aliases:** the same table plays two roles; `e` is the employee row, `m` is the manager row reached through `manager_id`. Without aliases the column names are ambiguous.
- **Why the top person never appears:** NULL never equals anything, so there is no manager row to compare with.
- **pandas suffixes:** merging a frame with itself duplicates every column name, so `suffixes` is what makes `salary_emp` and `salary_mgr` distinguishable (without it you would get `_x` and `_y`).
- **Alternative:** a correlated subquery, `WHERE salary > (SELECT salary FROM employees WHERE emp_id = e.manager_id)`, also works; I did not run it, and the join reads more naturally when you want manager columns in the output.

**Follow-ups:**
- *How do I also list employees without a manager?* LEFT JOIN, then the salary condition must handle NULL.
- *Employees earning more than the average of their team?* Aggregate by manager first (Part 3).
- *Two levels up?* Another self join, or a recursive CTE (Part 9).

**Common mistakes:**
- Joining on `e.emp_id = m.manager_id` (reversed: gives managers with their reports, and the comparison is flipped).
- Forgetting the second alias.
- Expecting the top person in the output.
- In pandas, omitting `suffixes` and reading `salary_x`/`salary_y` backwards.

### Q5 ⭐⭐⭐ 🟢 Left join to build a complete list with zeros: products(product_id, name) and sales(sale_id, product_id, qty), where some products never sold. Report every product with total units sold, showing 0 for unsold products. Explain COALESCE(SUM(qty), 0), why COUNT(s.sale_id) is right but COUNT(*) is wrong in the same query, and give the pandas version (merge how='left', fillna, and the dtype after fillna).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** LEFT JOIN products to sales, group by product, and use `COALESCE(SUM(s.qty), 0)`; count with `COUNT(s.sale_id)` because `COUNT(*)` counts the NULL-padded row and reports 1 for products that never sold.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen'),(2,'Book'),(3,'Bag'),(4,'Cap');
INSERT INTO sales VALUES (1,1,5),(2,1,3),(3,2,4);
```

**SQL answer:** `sql` in the Code block (LEFT JOIN, `COALESCE(SUM(s.qty), 0)` as `units`, `COUNT(s.sale_id)` as `n_sales`). `sql_bad` shows `COUNT(*)`, `COUNT(s.sale_id)` and the raw `SUM` side by side.

**pandas answer:** `products.merge(sales, on="product_id", how="left")`, then `groupby(["product_id","name"]).agg(units=("qty","sum"), n_sales=("sale_id","count"))`, then `fillna(0).astype("int64")` on `units`.

**Example:** Pen sold 5 + 3 = 8 in 2 sales, Book 4 in 1 sale. Bag and Cap have no sales rows, so the LEFT JOIN gives each one row with NULL `qty` and NULL `sale_id`.
- `SUM(s.qty)` over only NULLs is NULL, so `COALESCE` turns it into 0.
- `COUNT(*)` counts that single padded row, giving 1 (wrong). `COUNT(s.sale_id)` skips NULLs, giving 0 (right).

**Code:** run with `python3 -I`. Compared in `product_id` order.
```python
# Q5: left join to get zeros for unsold products.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen'),(2,'Book'),(3,'Bag'),(4,'Cap');
INSERT INTO sales VALUES (1,1,5),(2,1,3),(3,2,4);
""")

sql = """SELECT p.name, COALESCE(SUM(s.qty), 0) AS units, COUNT(s.sale_id) AS n_sales
FROM products p LEFT JOIN sales s ON s.product_id = p.product_id
GROUP BY p.product_id, p.name ORDER BY p.product_id"""
sql_bad = """SELECT p.name, COUNT(*) AS wrong_count, COUNT(s.sale_id) AS right_count, SUM(s.qty) AS raw_sum
FROM products p LEFT JOIN sales s ON s.product_id = p.product_id
GROUP BY p.product_id, p.name ORDER BY p.product_id"""
s = con.execute(sql).fetchall()
print("SQL:", s)
for r in con.execute(sql_bad): print("COUNT(*) vs COUNT(s.sale_id) vs raw SUM:", r)

products = pd.read_sql("SELECT * FROM products", con)
sales = pd.read_sql("SELECT * FROM sales", con)
m = products.merge(sales, on="product_id", how="left")
print("qty dtype after merge:", m["qty"].dtype)
g = m.groupby(["product_id", "name"], as_index=False).agg(units=("qty", "sum"), n_sales=("sale_id", "count"))
print("units dtype straight out of groupby sum:", g["units"].dtype, "(float64, because qty was float64)")
g_min = m.groupby("name")["qty"].sum(min_count=1)
print("sum(min_count=1) for Bag:", g_min["Bag"], "(NaN, the SQL-style raw SUM)")
g["units"] = g["units"].fillna(0).astype("int64")      # fillna alone keeps float64; astype restores int
print("dtype after fillna + astype:", g["units"].dtype)
print(g[["name", "units", "n_sales"]].to_string(index=False))

# the pandas trap equivalent to COUNT(*): size() counts the NaN row from the left join
print("size() per product (like COUNT(*)):", m.groupby("name").size().to_dict())

assert list(g[["name", "units", "n_sales"]].itertuples(index=False, name=None)) == s
assert s == [("Pen", 8, 2), ("Book", 4, 1), ("Bag", 0, 0), ("Cap", 0, 0)]
print("asserts passed (compared in product_id order)")
```

**Output (my run):**
```text
SQL: [('Pen', 8, 2), ('Book', 4, 1), ('Bag', 0, 0), ('Cap', 0, 0)]
COUNT(*) vs COUNT(s.sale_id) vs raw SUM: ('Pen', 2, 2, 8)
COUNT(*) vs COUNT(s.sale_id) vs raw SUM: ('Book', 1, 1, 4)
COUNT(*) vs COUNT(s.sale_id) vs raw SUM: ('Bag', 1, 0, None)
COUNT(*) vs COUNT(s.sale_id) vs raw SUM: ('Cap', 1, 0, None)
qty dtype after merge: float64
units dtype straight out of groupby sum: float64 (float64, because qty was float64)
sum(min_count=1) for Bag: nan (NaN, the SQL-style raw SUM)
dtype after fillna + astype: int64
name  units  n_sales
 Pen      8        2
Book      4        1
 Bag      0        0
 Cap      0        0
size() per product (like COUNT(*)): {'Bag': 1, 'Book': 1, 'Cap': 1, 'Pen': 2}
asserts passed (compared in product_id order)
```

**Edge cases:**
- **Sale row with NULL qty:** `SUM` ignores it, `COUNT(s.sale_id)` still counts the sale. So units and sale count can disagree; decide which one you mean. I did not run this case.
- **Product with only NULL qty rows:** same as no sales for the sum, COALESCE gives 0.
- **Ties and ordering:** the output order is set by `ORDER BY p.product_id`, not by the join.
- **pandas dtype:** after the left merge `qty` is `float64` (NaN needs a float). Surprise from my run: `groupby(...).sum()` already returned 0 for the unsold products (an all-NaN group sums to 0 by default), so the sum was `float64` with no NaN. `fillna(0)` therefore changed nothing there, and the `astype("int64")` is what restores integers. To get SQL's NULL for an all-NULL group you need `sum(min_count=1)`, which gave NaN for Bag.
- **pandas size():** `groupby.size()` counts rows including the padded one, like `COUNT(*)`; `count()` on a column skips NaN, like `COUNT(col)`.

**Then explain:**
- **Why LEFT JOIN:** an inner join drops products that never sold, so they could not show 0.
- **COALESCE:** turns the NULL sum into 0 at the end, after aggregation.
- **COUNT variants:** `COUNT(*)` = rows, `COUNT(col)` = non-NULL values. After an outer join, count a right-table column.
- **pandas:** `fillna` before or after the groupby both work here; the dtype is the point to mention.

**Follow-ups:**
- *Why not `COALESCE(s.qty, 0)` inside the SUM?* Also fine; `SUM(COALESCE(s.qty,0))` returns 0 directly. The outer COALESCE is cheaper to read.
- *What if you also want a revenue column?* Same pattern, but aggregate sales to one row per product first if other one-to-many tables join in (Part 2 Q12).
- *What does SUM of no rows return?* NULL in SQL, which is why the COALESCE is needed.

**Common mistakes:**
- `COUNT(*)` giving 1 for unsold products.
- `INNER JOIN` dropping the zeros.
- Putting a sales filter in WHERE (Part 2 Q3).
- Leaving pandas units as `float64` and printing 8.0, or assuming `fillna` fixes the dtype.

### Q6 ⭐⭐⭐ 🟢 How do NULL join keys behave? Given employees(emp_id, name, dept_id) where some dept_id values are NULL and departments(dept_id, dept_name), explain why NULL = NULL is not true so those employees drop out of an INNER JOIN and show up with NULL dept_name in a LEFT JOIN. Then cover null-safe options (IS NOT DISTINCT FROM in PostgreSQL, <=> in MySQL, IS in SQLite; hedged dialect notes) and say what pandas merge does instead when both frames have NaN keys.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** A NULL join key matches nothing in SQL (`NULL = NULL` is not true), so those employees vanish from an INNER JOIN and appear with a NULL dept_name in a LEFT JOIN; pandas does the opposite and matches NaN keys with each other.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
CREATE TABLE departments(dept_id INTEGER, dept_name TEXT);          -- dept_id nullable, no PK
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',NULL),(4,'Dev',NULL),(5,'Esha',30);
INSERT INTO departments VALUES (10,'Sales'),(20,'Eng'),(NULL,'Unassigned');
```
Esha has dept 30, which does not exist. The departments table has a NULL-key row on purpose, to show that it still does not match.

**SQL answer:** in the Code block: `sql_inner` (`ON e.dept_id = d.dept_id`, INNER), `sql_left` (same ON, LEFT), `sql_is` (LEFT with `ON e.dept_id IS d.dept_id`) and `sql_isndf` (LEFT with `IS NOT DISTINCT FROM`).

**pandas answer:** the plain `emp.merge(dep, on="dept_id", how=...)`, and the SQL-like version that first drops NaN keys: `emp.dropna(subset=["dept_id"])` and `dep.dropna(subset=["dept_id"])` (for the LEFT case drop only on the right so unmatched employees stay).

**Example:**
- INNER with `=`: Asha matches Sales, Ben matches Eng. Chitra and Dev have a NULL key, `NULL = NULL` is UNKNOWN, no match, dropped. Esha has no dept 30, dropped. 2 rows.
- LEFT with `=`: the same two matches plus Chitra, Dev and Esha with NULL `dept_name`. 5 rows. Note that Chitra and Dev do not pick up the 'Unassigned' row.
- Null-safe `IS`: Chitra and Dev now match the NULL-key department row and get 'Unassigned'. Esha stays NULL.
- pandas merge: the NaN keys match each other, so even an inner merge returns 4 rows including Chitra and Dev with 'Unassigned'.

**Code:** run with `python3 -I`. Compared in `emp_id` order.
```python
# Q6: NULL join keys in SQL versus NaN join keys in pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
CREATE TABLE departments(dept_id INTEGER, dept_name TEXT);          -- dept_id nullable, no PK
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',NULL),(4,'Dev',NULL),(5,'Esha',30);
INSERT INTO departments VALUES (10,'Sales'),(20,'Eng'),(NULL,'Unassigned');
""")
print("NULL = NULL ->", con.execute("SELECT NULL = NULL").fetchone()[0],
      "| NULL IS NULL ->", con.execute("SELECT NULL IS NULL").fetchone()[0])

q = lambda on, how="LEFT": f"""SELECT e.name, d.dept_name FROM employees e {how} JOIN departments d ON {on}
ORDER BY e.emp_id"""
sql_inner = q("e.dept_id = d.dept_id", "INNER")
sql_left = q("e.dept_id = d.dept_id")
sql_is = q("e.dept_id IS d.dept_id")
sql_isndf = q("e.dept_id IS NOT DISTINCT FROM d.dept_id")
run = lambda s: con.execute(s).fetchall()
print("INNER  =        :", run(sql_inner))
print("LEFT   =        :", run(sql_left))
print("LEFT   IS       :", run(sql_is))
print("LEFT   IS NOT DISTINCT FROM (runs on SQLite 3.45):", run(sql_isndf))
assert run(sql_is) == run(sql_isndf)

emp = pd.read_sql("SELECT * FROM employees", con)
dep = pd.read_sql("SELECT * FROM departments", con)
print("dept_id dtypes:", emp["dept_id"].dtype, dep["dept_id"].dtype)

key = lambda df: list(df[["name", "dept_name"]].itertuples(index=False, name=None))
fix = lambda t: [(a, None if b != b else b) for a, b in t]     # NaN -> None for comparison
p_inner = emp.merge(dep, on="dept_id", how="inner").sort_values("emp_id")
p_left = emp.merge(dep, on="dept_id", how="left").sort_values("emp_id")
print("pandas inner merge (NaN keys match NaN):", key(p_inner))
print("pandas left  merge                     :", key(p_left))

# pandas default equals the SQLite IS version, not the = version
assert fix(key(p_left)) == run(sql_is)
# to get SQL = behaviour in pandas, drop NaN keys on both sides first
emp_k = emp.dropna(subset=["dept_id"]); dep_k = dep.dropna(subset=["dept_id"])
p_sql_like_inner = emp_k.merge(dep_k, on="dept_id", how="inner").sort_values("emp_id")
p_sql_like_left = emp.merge(dep_k, on="dept_id", how="left").sort_values("emp_id")
assert key(p_sql_like_inner) == run(sql_inner)
assert fix(key(p_sql_like_left)) == run(sql_left)
print("pandas with NaN keys dropped from the right side matches SQL =:", fix(key(p_sql_like_left)))
many = pd.DataFrame({"dept_id": [None, None], "who": ["x", "y"]}).merge(pd.DataFrame({"dept_id": [None, None, None], "d": [1, 2, 3]}), on="dept_id")
print("2 NaN keys x 3 NaN keys in pandas ->", len(many), "rows")
assert len(many) == 6
print("asserts passed (compared in emp_id order)")
```

**Output (my run):**
```text
NULL = NULL -> None | NULL IS NULL -> 1
INNER  =        : [('Asha', 'Sales'), ('Ben', 'Eng')]
LEFT   =        : [('Asha', 'Sales'), ('Ben', 'Eng'), ('Chitra', None), ('Dev', None), ('Esha', None)]
LEFT   IS       : [('Asha', 'Sales'), ('Ben', 'Eng'), ('Chitra', 'Unassigned'), ('Dev', 'Unassigned'), ('Esha', None)]
LEFT   IS NOT DISTINCT FROM (runs on SQLite 3.45): [('Asha', 'Sales'), ('Ben', 'Eng'), ('Chitra', 'Unassigned'), ('Dev', 'Unassigned'), ('Esha', None)]
dept_id dtypes: float64 float64
pandas inner merge (NaN keys match NaN): [('Asha', 'Sales'), ('Ben', 'Eng'), ('Chitra', 'Unassigned'), ('Dev', 'Unassigned')]
pandas left  merge                     : [('Asha', 'Sales'), ('Ben', 'Eng'), ('Chitra', 'Unassigned'), ('Dev', 'Unassigned'), ('Esha', nan)]
pandas with NaN keys dropped from the right side matches SQL =: [('Asha', 'Sales'), ('Ben', 'Eng'), ('Chitra', None), ('Dev', None), ('Esha', None)]
2 NaN keys x 3 NaN keys in pandas -> 6 rows
asserts passed (compared in emp_id order)
```

**Edge cases:**
- **Both sides NULL is the only case where pandas and `=` disagree**, but it changes row counts, so check it before merging real data.
- **One side NULL only:** no match in either world.
- **Many NaN keys on both sides:** pandas matches every NaN left row with every NaN right row (a Cartesian product within the NaN group). With 2 NaN-key employees and 3 NaN-key departments that is 6 rows (the Code block runs this and prints it).
- **dtype:** `dept_id` became `float64` in both frames because of the NULLs, and the merge still worked.

**Then explain:**
- **Why:** NULL means unknown, and an unknown can't be said to equal another unknown. The comparison is UNKNOWN and joins keep only TRUE.
- **Null-safe operators (hedged dialect notes):** `IS NOT DISTINCT FROM` is standard SQL and works in PostgreSQL (not executed here); MySQL's equivalent is `<=>` (not executed here); SQLite's `IS` works for any two values (run here). In my run SQLite 3.45.1 also accepted `IS NOT DISTINCT FROM`, so the standard form works in SQLite too (I believe it arrived in 3.39 along with RIGHT/FULL JOIN; that version number is from memory).
- **pandas:** `merge` matches NaN with NaN. To get SQL behaviour, drop NaN keys first, as the Code block does and asserts equal to the SQL result. The pandas user guide page I opened did not state this; I confirmed it by running.
- **Practical rule:** decide what a missing key should mean. If you want "unassigned" rows grouped, say so explicitly; do not let the join decide.

**Follow-ups:**
- *Is a NULL-safe join index-friendly?* Usually not as well as plain equality in many engines (hedged, not executed here).
- *How do I keep employees with no department?* LEFT JOIN.
- *Can I replace NULL with a sentinel like -1?* Yes in the join (`COALESCE(dept_id, -1)`), but it makes the unassigned group match deliberately and can mask data problems.

**Common mistakes:**
- Expecting NULL-keyed employees to join the 'Unassigned' row.
- Assuming pandas follows SQL on NaN keys.
- Using `WHERE d.dept_id IS NULL` to find unmatched rows when NULL keys on the left also qualify.
- Forgetting to check row counts after a merge.

### Q7 ⭐⭐⭐ 🟢 pandas merge basics for an SQL person: customers(customer_id, name) and orders(order_id, cust_id, amount) have differently named keys and both have a column called created_at. Show merge with how=, on, left_on/right_on, suffixes, indicator=True and validate='one_to_many', say what each argument guards against, and explain the default how and the _x/_y suffixes. Map each argument to the SQL clause.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `merge` is a SQL join: `how=` is the join type (default `inner`), `on`/`left_on`/`right_on` is the ON clause, `suffixes` renames clashing columns (default `_x`/`_y`), `indicator=True` adds a `_merge` column showing which side matched, and `validate=` raises an error if the key relationship is not what you assumed.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, created_at TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, cust_id INTEGER, amount INTEGER, created_at TEXT);
INSERT INTO customers VALUES (1,'Asha','2024-01-01'),(2,'Ben','2024-02-01'),(3,'Chitra','2024-03-01');
INSERT INTO orders VALUES (101,1,50,'2024-05-01'),(102,1,20,'2024-05-02'),(103,2,30,'2024-05-03'),(104,9,10,'2024-05-04');
```
Order 104 points to customer 9, who does not exist. Chitra has no orders.

**SQL answer:** `sql` in the Code block: a FULL OUTER JOIN `ON c.customer_id = o.cust_id`, with the two `created_at` columns aliased `created_at_cust` and `created_at_order`.

**pandas answer:** `customers.merge(orders, how="outer", left_on="customer_id", right_on="cust_id", suffixes=("_cust","_order"), indicator=True, validate="one_to_many")`, in the Code block as `p`.

**Example:** Matches: Asha twice (101, 102) and Ben once (103). Chitra is `left_only`, order 104 is `right_only`. Total 5 rows, which is the SQL FULL JOIN row count.

| pandas argument | SQL clause | what it guards against |
|---|---|---|
| `how="inner"` (default) | `INNER JOIN`, or just `JOIN` | surprise loss of unmatched rows if you expected a left join |
| `how="left"`/`"right"`/`"outer"`/`"cross"` | `LEFT`/`RIGHT`/`FULL OUTER`/`CROSS JOIN` | choose which unmatched rows survive |
| `on="k"` | `USING (k)` or `ON a.k = b.k` | same-named key, one output key column |
| `left_on`, `right_on` | `ON a.customer_id = b.cust_id` | differently named keys; both key columns stay in the output |
| `suffixes=("_a","_b")` | column aliases `AS created_at_a` | silent `_x`/`_y` names you then misread |
| `indicator=True` | a hand-made `CASE WHEN a.k IS NULL ...` flag | not knowing which rows are unmatched |
| `validate="one_to_many"` | a uniqueness constraint on the `one` side | duplicate keys silently multiplying rows |

**Code:** run with `python3 -I`. Rows compared after sorting (NaN as None).
```python
# Q7: pandas merge arguments mapped to SQL, with differently named keys and a shared created_at column.
import sqlite3
import pandas as pd
from pandas.errors import MergeError

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, created_at TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, cust_id INTEGER, amount INTEGER, created_at TEXT);
INSERT INTO customers VALUES (1,'Asha','2024-01-01'),(2,'Ben','2024-02-01'),(3,'Chitra','2024-03-01');
INSERT INTO orders VALUES (101,1,50,'2024-05-01'),(102,1,20,'2024-05-02'),(103,2,30,'2024-05-03'),(104,9,10,'2024-05-04');
""")
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)

# 1) default merge: how='inner', and a clash on created_at gives _x / _y
d = customers.merge(orders, left_on="customer_id", right_on="cust_id")
print("default how, auto suffixes:", list(d.columns), "| rows:", len(d))

# 2) the full version: how, left_on/right_on, suffixes, indicator, validate
p = customers.merge(orders, how="outer", left_on="customer_id", right_on="cust_id",
                    suffixes=("_cust", "_order"), indicator=True, validate="one_to_many")
print(p[["customer_id", "name", "order_id", "cust_id", "_merge"]].to_string(index=False))
print(p["_merge"].value_counts().to_dict())

sql = """SELECT c.customer_id, c.name, c.created_at AS created_at_cust, o.order_id, o.cust_id, o.amount,
       o.created_at AS created_at_order
FROM customers c FULL OUTER JOIN orders o ON c.customer_id = o.cust_id"""
s = con.execute(sql).fetchall()

cols = ["customer_id", "name", "created_at_cust", "order_id", "cust_id", "amount", "created_at_order"]
def rows(items):
    out = []
    for r in items:
        out.append(tuple(None if (x is None or (isinstance(x, float) and x != x))
                         else int(x) if isinstance(x, float) else x for x in r))
    return sorted(out, key=lambda t: tuple((v is None, str(v)) for v in t))
assert rows(p[cols].itertuples(index=False, name=None)) == rows(s)   # all rows sorted before comparing
print("SQL FULL OUTER JOIN == pandas outer merge (", len(s), "rows )")

# 3) what validate guards: a duplicated key on the 'one' side
dup = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)
try:
    dup.merge(orders, left_on="customer_id", right_on="cust_id", validate="one_to_many")
except MergeError as e:
    print("MergeError:", e)
print("without validate the duplicate silently gives", len(dup.merge(orders, left_on="customer_id", right_on="cust_id")), "rows (was", len(d), ")")
assert len(d) == 3
print("asserts passed")
```

**Output (my run):**
```text
default how, auto suffixes: ['customer_id', 'name', 'created_at_x', 'order_id', 'cust_id', 'amount', 'created_at_y'] | rows: 3
 customer_id   name  order_id  cust_id     _merge
         1.0   Asha     101.0      1.0       both
         1.0   Asha     102.0      1.0       both
         2.0    Ben     103.0      2.0       both
         3.0 Chitra       NaN      NaN  left_only
         NaN    NaN     104.0      9.0 right_only
{'both': 3, 'left_only': 1, 'right_only': 1}
SQL FULL OUTER JOIN == pandas outer merge ( 5 rows )
MergeError: Merge keys are not unique in left dataset; not a one-to-many merge
Duplicates in left:
  customer_id
           1 ...
without validate the duplicate silently gives 5 rows (was 3 )
asserts passed
```

**Edge cases:**
- **Default suffixes:** without `suffixes`, the two `created_at` columns came out as `created_at_x` (left) and `created_at_y` (right) in my run. `_x` is the left frame, `_y` the right.
- **`left_on`/`right_on` keeps both keys:** in an outer merge `customer_id` is NaN for the orphan order and `cust_id` is NaN for Chitra (see the printed frame). With `on="customer_id"` you would get a single combined key column (Part 2 Q39).
- **validate on duplicates:** a duplicated customer made `validate="one_to_many"` raise `MergeError: Merge keys are not unique in left dataset; not a one-to-many merge`. Without `validate`, the same merge silently returned 5 rows instead of 3.
- **NaN keys** match each other (Part 2 Q6).
- **Float display:** `customer_id` shows as 1.0, 2.0 because the outer merge introduces NaN.

**Then explain:**
- **Default how:** `inner`, so unmatched rows disappear without a warning.
- **`_merge` values:** `left_only`, `right_only`, `both`; the counts in my run were 3 both, 1 left_only, 1 right_only.
- **validate options:** `one_to_one`, `one_to_many`, `many_to_one`, `many_to_many`. It checks key uniqueness on the sides named "one". It does not check that every row matched; use `indicator` for that.
- **Write `validate` on every production merge:** it is the pandas analogue of a primary-key constraint on the lookup side.

**Follow-ups:**
- *What if the key columns have different dtypes?* A ValueError or silent mismatches (Part 2 Q35).
- *join versus merge?* `DataFrame.join` is index-based and defaults to a left join (Part 2 Q23).
- *How do I drop the extra key column?* `.drop(columns="cust_id")` after the merge.

**Common mistakes:**
- Assuming the default is a left join.
- Reading `_x` and `_y` as "first" and "second" without checking which frame is which.
- Not passing `validate=` and finding duplicate keys after the totals look wrong.
- Forgetting that `left_on`/`right_on` leaves two key columns.

### Q8 ⭐⭐⭐ 🟢 Semi-join: list customers who have placed at least one order, using customers(customer_id, name) and orders(order_id, customer_id, amount). Write it with EXISTS, with IN, and with JOIN plus DISTINCT, explain why a plain JOIN returns a customer once per order, which form is safest when the subquery column can hold NULLs, and give the pandas version (isin on the key, or merge on the deduplicated keys).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** For "customers with at least one order" use `WHERE EXISTS (correlated subquery)`; `IN` and `JOIN ... DISTINCT` give the same customers, a plain JOIN returns a customer once per order, and EXISTS is the form that never depends on NULLs.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30);   -- 104 = guest, NULL customer
```

**SQL answer:** in the Code block: `sql_exists`, `sql_in`, `sql_join_distinct` and, for the contrast, `sql_plain_join`.

**pandas answer:** `customers[customers["customer_id"].isin(orders["customer_id"])]`, or `customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id")`.

**Example:** Orders belong to customers 1, 1, 2 and a guest (NULL). Asha and Ben have orders, Chitra and Dev do not. The semi-join returns Asha and Ben, once each. A plain JOIN produces a row per order: Asha, Asha, Ben (3 rows), because Asha has two orders.

**Code:** run with `python3 -I`. Compared in `customer_id` order.
```python
# Q8: semi-join: customers with at least one order.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30);   -- 104 = guest, NULL customer
""")
sql_exists = """SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id"""
sql_in = """SELECT customer_id, name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders) ORDER BY customer_id"""
sql_join_distinct = """SELECT DISTINCT c.customer_id, c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id ORDER BY c.customer_id"""
sql_plain_join = """SELECT c.customer_id, c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id ORDER BY c.customer_id"""
run = lambda q: con.execute(q).fetchall()
print("EXISTS           :", run(sql_exists))
print("IN (NULL present):", run(sql_in))
print("JOIN + DISTINCT  :", run(sql_join_distinct))
print("plain JOIN       :", run(sql_plain_join), "<- Asha twice")

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
p_isin = customers[customers["customer_id"].isin(orders["customer_id"])]
keys = orders[["customer_id"]].drop_duplicates()
p_merge = customers.merge(keys, on="customer_id", how="inner")
print("pandas isin:", p_isin["name"].tolist(), "| merge on dedup keys:", p_merge["name"].tolist())
p_plain = customers.merge(orders, on="customer_id")
print("pandas merge on raw orders rows:", len(p_plain), "(one per order, like the plain JOIN)")

as_t = lambda df: list(df[["customer_id", "name"]].itertuples(index=False, name=None))
assert as_t(p_isin) == as_t(p_merge.sort_values("customer_id")) == run(sql_exists) == run(sql_in) == run(sql_join_distinct)
assert len(run(sql_plain_join)) == 3 == len(p_plain)
print("asserts passed (compared in customer_id order)")
```

**Output (my run):**
```text
EXISTS           : [(1, 'Asha'), (2, 'Ben')]
IN (NULL present): [(1, 'Asha'), (2, 'Ben')]
JOIN + DISTINCT  : [(1, 'Asha'), (2, 'Ben')]
plain JOIN       : [(1, 'Asha'), (1, 'Asha'), (2, 'Ben')] <- Asha twice
pandas isin: ['Asha', 'Ben'] | merge on dedup keys: ['Asha', 'Ben']
pandas merge on raw orders rows: 3 (one per order, like the plain JOIN)
asserts passed (compared in customer_id order)
```

**Edge cases:**
- **NULL in the subquery:** harmless here for `IN` (a positive `IN` can still be TRUE for real matches) and for EXISTS. It breaks only the negated forms, `NOT IN` (Part 2 Q2).
- **Safest form:** EXISTS. It stays correct whether the subquery column holds NULLs or not, and the negated form (`NOT EXISTS`) is just as safe, so one habit covers both semi and anti joins.
- **Duplicates in the right table:** EXISTS and IN ignore them; JOIN multiplies them, so aggregates over the joined rows are inflated (Part 2 Q12).
- **pandas dtype:** the orders key was `float64` because of the NULL; `isin` still matched the integer customer ids correctly in my run.
- **Customers with duplicate ids in the left table** would be returned twice by every form, since the duplication is on the left.

**Then explain:**
- **Semi-join:** return left rows that have a match, without returning right columns and without multiplying rows.
- **JOIN + DISTINCT** works but does extra work to remove duplicates it should never have created, and it only works if the selected columns identify the customer (DISTINCT over `name` alone would merge two different customers with the same name).
- **pandas:** `isin` is a membership test and returns the original rows. The merge form needs `drop_duplicates()` on the key first, or you reproduce the plain-JOIN row multiplication (3 rows in my run).
- **Engines:** many optimisers turn EXISTS and IN into a semi-join plan, but I did not check any plan here (hedged; not executed).

**Follow-ups:**
- *Which is faster, IN or EXISTS?* Depends on the engine and version; modern optimisers often treat them the same (not executed here).
- *Need columns from the orders table?* Then a JOIN is the right tool, and you must decide how to handle several orders per customer.
- *The opposite?* Anti-join (Part 2 Q2).

**Common mistakes:**
- Using a plain JOIN and getting duplicates, then "fixing" with `SELECT DISTINCT *`.
- Using `DISTINCT` on a column that is not the customer key.
- Believing the NULL trap applies to `IN` the same way it does to `NOT IN`.
- Merging without deduplicating the keys in pandas.

### Q9 ⭐⭐⭐ 🟢 Duplicate keys in the lookup table: products(product_id, name, price) was loaded twice for some products, and order_items(item_id, order_id, product_id, qty) joins to it. Show how the join silently inflates row counts and revenue, how to detect duplicate keys (GROUP BY key HAVING COUNT(*) > 1), how to fix it at the source versus in the query, and how pandas catches it (validate='many_to_one' raising MergeError, duplicated on the key).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** If the lookup table repeats a key, every joined row is repeated and counts and revenue inflate silently; find the duplicate keys with `GROUP BY key HAVING COUNT(*) > 1`, fix the load or add a key constraint, and in pandas use `validate="many_to_one"` so the merge raises `MergeError`.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER, name TEXT, price INTEGER);      -- no PK: loaded twice
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen',10),(1,'Pen',10),(2,'Book',20),(3,'Cap',5);
INSERT INTO order_items VALUES (1,1,1,2),(2,1,2,1),(3,2,3,4);
```
Product 1 (Pen) was loaded twice.

**SQL answer:** in the Code block: the "bad" join (`order_items` JOIN `products`), `sql_detect` (the GROUP BY HAVING query), and `sql_fix` (join to a derived table of `SELECT DISTINCT product_id, name, price FROM products`). The source fix is the `products_clean` table with `PRIMARY KEY`.

**pandas answer:** `products[products.duplicated("product_id", keep=False)]` to see them, `items.merge(products, on="product_id", validate="many_to_one")` to raise, and `products.drop_duplicates(subset=["product_id","name","price"])` to fix.

**Example:** True revenue: item 1 is 2 x 10 = 20, item 2 is 1 x 20 = 20, item 3 is 4 x 5 = 20, total 60. Pen appears twice in `products`, so item 1 joins to two rows and counts twice (40). Result: 4 rows and revenue 80 instead of 3 rows and 60. Nothing errored.

**Code:** run with `python3 -I`.
```python
# Q9: duplicate keys in a lookup table inflate a join; detect, fix, guard.
import sqlite3
import pandas as pd
from pandas.errors import MergeError

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(product_id INTEGER, name TEXT, price INTEGER);      -- no PK: loaded twice
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen',10),(1,'Pen',10),(2,'Book',20),(3,'Cap',5);
INSERT INTO order_items VALUES (1,1,1,2),(2,1,2,1),(3,2,3,4);
""")
run = lambda q: con.execute(q).fetchall()

truth = run("SELECT SUM(qty * (SELECT MAX(price) FROM products p WHERE p.product_id = i.product_id)) FROM order_items i")[0][0]
bad = run("""SELECT COUNT(*), SUM(i.qty * p.price) FROM order_items i JOIN products p ON p.product_id = i.product_id""")[0]
print("true revenue:", truth, "| joined rows, revenue:", bad, "(3 items became", bad[0], "rows)")

sql_detect = "SELECT product_id, COUNT(*) AS n FROM products GROUP BY product_id HAVING COUNT(*) > 1"
print("duplicate keys:", run(sql_detect))
sql_fix = """SELECT COUNT(*), SUM(i.qty * p.price) FROM order_items i
JOIN (SELECT DISTINCT product_id, name, price FROM products) p ON p.product_id = i.product_id"""
fixed = run(sql_fix)[0]
print("after DISTINCT in a derived table:", fixed)
assert fixed == (3, truth) and bad == (4, 80) and truth == 60

# conflicting duplicates would survive DISTINCT: it keeps both rows
con.execute("INSERT INTO products VALUES (2,'Book',25)")
print("DISTINCT with a conflicting price keeps", run("SELECT COUNT(*) FROM (SELECT DISTINCT product_id, name, price FROM products) WHERE product_id=2")[0][0], "rows for product 2")
con.execute("DELETE FROM products WHERE price = 25")

# fix at the source: a key constraint rejects the second load
con.executescript("""CREATE TABLE products_clean(product_id INTEGER PRIMARY KEY, name TEXT, price INTEGER);
INSERT INTO products_clean SELECT DISTINCT product_id, name, price FROM products;""")
try:
    con.execute("INSERT INTO products_clean VALUES (1,'Pen',10)")
except sqlite3.IntegrityError as e:
    print("IntegrityError:", e)

# pandas
products = pd.read_sql("SELECT * FROM products", con)
items = pd.read_sql("SELECT * FROM order_items", con)
print("duplicated product_id rows:\n", products[products.duplicated("product_id", keep=False)].to_string(index=False))
m = items.merge(products, on="product_id")
print("naive merge:", len(m), "rows, revenue", int((m["qty"] * m["price"]).sum()))
try:
    items.merge(products, on="product_id", validate="many_to_one")
except MergeError as e:
    print("MergeError:", e)
clean = products.drop_duplicates(subset=["product_id", "name", "price"])
m2 = items.merge(clean, on="product_id", validate="many_to_one")
rev = int((m2["qty"] * m2["price"]).sum())
print("after drop_duplicates + validate:", len(m2), "rows, revenue", rev)
assert (len(m), int((m["qty"] * m["price"]).sum())) == bad and (len(m2), rev) == fixed
print("asserts passed")
```

**Output (my run):**
```text
true revenue: 60 | joined rows, revenue: (4, 80) (3 items became 4 rows)
duplicate keys: [(1, 2)]
after DISTINCT in a derived table: (3, 60)
DISTINCT with a conflicting price keeps 2 rows for product 2
IntegrityError: UNIQUE constraint failed: products_clean.product_id
duplicated product_id rows:
  product_id name  price
          1  Pen     10
          1  Pen     10
naive merge: 4 rows, revenue 80
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  product_id
          1 ...
after drop_duplicates + validate: 3 rows, revenue 60
asserts passed
```

**Edge cases:**
- **Exact duplicates vs conflicting duplicates:** `DISTINCT` fixes the first kind (same price twice). If product 2 had two different prices, `DISTINCT` keeps both rows, as my run shows (2 rows for product 2). Then you need a rule (latest load, MAX, a date column) or a data fix.
- **Duplicate keys with no matching items:** harmless to this join, but they will bite later.
- **NULL keys** in the lookup do not join but are not flagged by `HAVING COUNT(*) > 1` as a join problem; check `COUNT(*) - COUNT(product_id)` as well (I did not run that check).
- **Fix at the source:** a `PRIMARY KEY` or `UNIQUE` constraint rejects the second row (my run: `IntegrityError: UNIQUE constraint failed: products_clean.product_id`). Cloud warehouses often do not enforce primary keys (hedged, not executed here), so add a test or an assertion in the load job.

**Then explain:**
- **Why inflation:** a join returns one row per matching pair, so 2 matching lookup rows turn one item into 2.
- **Detect:** `GROUP BY key HAVING COUNT(*) > 1` finds repeated keys; also compare `COUNT(*)` of the join to `COUNT(*)` of the fact table.
- **Source vs query:** fix the load and add a constraint so every consumer is safe. De-duplicating inside each query is a workaround, and it hides a data quality problem.
- **pandas:** `validate="many_to_one"` raised `MergeError: Merge keys are not unique in right dataset; not a many-to-one merge`. The naive merge returned 4 rows and revenue 80, same as the SQL.

**Follow-ups:**
- *Which duplicate do you keep?* Define it (latest by timestamp, highest version) and write it down.
- *How do I alert on this?* A scheduled check that returns rows from the HAVING query and fails if non-empty.
- *Is it only a problem for SUM?* No; counts and averages are distorted too.

**Common mistakes:**
- Checking the total against a different join and trusting it.
- Using `DISTINCT *` on the final result.
- Fixing conflicting duplicates with `DISTINCT`.
- Skipping `validate=` in pandas.

### Q10 ⭐⭐⭐ 🟢 UNION versus UNION ALL versus JOIN: web_orders(order_id, customer_id, amount) and store_orders(order_id, customer_id, amount) have the same columns. When do you stack rows (UNION ALL, UNION) and when do you join side by side? Explain the duplicate-removal cost of UNION, the silent loss of legitimate duplicate rows, the requirement for matching column counts and types, adding a channel column, and pandas concat versus merge.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Stack rows with `UNION ALL` (keeps every row, cheapest) or `UNION` (removes duplicates, costs a sort or hash and can drop real rows) when two tables describe the same kind of row, and join side by side when you want extra columns about the same entity; in pandas that is `concat` versus `merge`.

**Schema and sample data:**
```sql
CREATE TABLE web_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
CREATE TABLE store_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
INSERT INTO web_orders   VALUES (1,10,100),(2,11,50),(3,12,75);
INSERT INTO store_orders VALUES (3,12,75),(4,10,100),(5,13,20);   -- order 3 is loaded in both channels
```

**SQL answer:** in the Code block: `sql_all` (UNION ALL), `sql_union` (UNION), `sql_chan` (UNION ALL with a literal `channel` column), `sql_proj_all` and `sql_proj_union` (only `customer_id, amount`), and `sql_join` (side by side).

**pandas answer:** `pd.concat([web, store], ignore_index=True)` for UNION ALL, `.drop_duplicates()` for UNION, `web.assign(channel="web")` before the concat to add the channel, and `web.merge(store, on="order_id", suffixes=("_web","_store"))` for a side-by-side join.

**Example:** 3 web + 3 store rows = 6 rows with UNION ALL. Order 3 is in both tables with identical values, so `UNION` removes one copy: 5 rows. With a `channel` column the two copies of order 3 differ ('web' versus 'store'), so even `UNION` keeps both (my run prints 6 for that case). Projected to `(customer_id, amount)` only, `UNION` returns 4 rows from 6: it merges the duplicated order 3, which is fine, but it also merges orders 1 and 4, two different orders by customer 10 for 100, which is a real loss. The join on `order_id` returns only order 3, the one order present in both tables.

**Code:** run with `python3 -I`. Rows compared after sorting.
```python
# Q10: UNION vs UNION ALL vs JOIN, and pandas concat vs merge.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE web_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
CREATE TABLE store_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
INSERT INTO web_orders   VALUES (1,10,100),(2,11,50),(3,12,75);
INSERT INTO store_orders VALUES (3,12,75),(4,10,100),(5,13,20);   -- order 3 is loaded in both channels
""")
run = lambda q: con.execute(q).fetchall()
sql_all = "SELECT * FROM web_orders UNION ALL SELECT * FROM store_orders"
sql_union = "SELECT * FROM web_orders UNION SELECT * FROM store_orders"
sql_chan = """SELECT 'web' AS channel, order_id, customer_id, amount FROM web_orders
UNION ALL SELECT 'store', order_id, customer_id, amount FROM store_orders"""
sql_proj_all = "SELECT customer_id, amount FROM web_orders UNION ALL SELECT customer_id, amount FROM store_orders"
sql_proj_union = "SELECT customer_id, amount FROM web_orders UNION SELECT customer_id, amount FROM store_orders"
sql_join = """SELECT w.order_id, w.amount AS web_amount, s.amount AS store_amount
FROM web_orders w JOIN store_orders s ON s.order_id = w.order_id"""
print("UNION ALL rows:", len(run(sql_all)), "| UNION rows:", len(run(sql_union)),
      "| with channel column:", len(run(sql_chan)))
print("UNION with the channel column:", len(run("SELECT 'web' AS channel, * FROM web_orders UNION SELECT 'store', * FROM store_orders")), "rows")
print("projected to (customer_id, amount): UNION ALL", len(run(sql_proj_all)), "rows, UNION", len(run(sql_proj_union)),
      "rows (orders 1 and 4 look identical and one vanished)")
print("JOIN side by side:", run(sql_join))
try:
    con.execute("SELECT order_id, amount FROM web_orders UNION ALL SELECT * FROM store_orders")
except sqlite3.OperationalError as e:
    print("column-count mismatch ->", e)

web = pd.read_sql("SELECT * FROM web_orders", con)
store = pd.read_sql("SELECT * FROM store_orders", con)
cat = pd.concat([web.assign(channel="web"), store.assign(channel="store")], ignore_index=True)
rows = lambda df: sorted(df.itertuples(index=False, name=None))
assert rows(pd.concat([web, store], ignore_index=True)) == sorted(run(sql_all))
assert rows(pd.concat([web, store], ignore_index=True).drop_duplicates()) == sorted(run(sql_union))
assert rows(cat[["channel", "order_id", "customer_id", "amount"]]) == sorted(run(sql_chan))
proj = pd.concat([web, store])[["customer_id", "amount"]]
assert len(proj) == 6 and len(proj.drop_duplicates()) == len(run(sql_proj_union)) == 4
j = web.merge(store, on="order_id", suffixes=("_web", "_store"))
assert rows(j[["order_id", "amount_web", "amount_store"]]) == sorted(run(sql_join))
print("pandas concat:", len(cat), "rows | concat+drop_duplicates (UNION):",
      len(pd.concat([web, store]).drop_duplicates()), "| merge on order_id:", len(j), "row")
print("asserts passed (all compared after sorting rows)")
```

**Output (my run):**
```text
UNION ALL rows: 6 | UNION rows: 5 | with channel column: 6
UNION with the channel column: 6 rows
projected to (customer_id, amount): UNION ALL 6 rows, UNION 4 rows (orders 1 and 4 look identical and one vanished)
JOIN side by side: [(3, 75, 75)]
column-count mismatch -> SELECTs to the left and right of UNION ALL do not have the same number of result columns
pandas concat: 6 rows | concat+drop_duplicates (UNION): 5 | merge on order_id: 1 row
asserts passed (all compared after sorting rows)
```

**Edge cases:**
- **Legitimate duplicates:** two real orders with the same customer and amount look identical once `order_id` is dropped. `UNION` removes one, so a total computed afterwards is short. Use `UNION ALL` unless you really want set semantics.
- **Column count:** must match; SQLite error in my run: "SELECTs to the left and right of UNION ALL do not have the same number of result columns".
- **Types:** matching types are required by the standard; how strictly each engine enforces or coerces them differs (not executed here; I only tested the column-count error). Cast explicitly.
- **Column names:** the result takes names from the first SELECT; matching is by position, not by name. In pandas `concat` matches by column name and fills missing columns with NaN.
- **NULLs:** `UNION` treats NULLs as equal when de-duplicating (stated in the SQL standard; not tested here).
- **Cost:** `UNION` has to compare rows, usually via a sort or hash (hedged; I did not measure it), so it is slower than `UNION ALL` on large inputs.

**Then explain:**
- **Stack vs join:** stack when the tables are the same entity split by source or time (web and store orders). Join when the tables describe different facts about the same key (orders and customers). The test is: do I want more rows or more columns?
- **Add a channel column** before stacking, or you cannot tell where a row came from; it also keeps cross-channel copies of one order distinguishable.
- **De-duplicate on a key, not on all columns:** if you need "one row per order_id" across channels, decide the rule explicitly rather than relying on `UNION`.
- **pandas:** `concat` is `UNION ALL` (it never de-duplicates), `drop_duplicates` makes it `UNION`, and `merge` is the join. All asserts in the Code block compare these to SQL.

**Follow-ups:**
- *Does UNION ALL guarantee order?* No; add ORDER BY.
- *What if the column order differs between the two tables?* Name the columns in each SELECT so position matches.
- *Join or union for comparing channels?* A FULL JOIN on order_id (Part 2 Q16).

**Common mistakes:**
- Using `UNION` "to be safe" and silently dropping rows.
- Different column order between the SELECTs.
- Forgetting a source label.
- Using `merge` where `concat` is needed (merge returned 1 row here).

### Q11 ⭐⭐⭐ 🟢 Predicting row counts: explain join cardinality (one-to-one, one-to-many, many-to-many) and how to estimate how many rows a join returns before running it. Given customers(customer_id, name) with 100 rows and orders(order_id, customer_id, amount) with 450 rows (every order has a valid customer, 20 customers have no orders), state the row count of INNER, LEFT and RIGHT joins, of a CROSS JOIN, and of the join when customer_id is duplicated in customers. Say how you would verify the grain with COUNT(*) versus COUNT(DISTINCT key), and the pandas check.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Rows in a join = for each key, (rows on the left with that key) x (rows on the right with that key), plus unmatched rows for outer joins; with 100 customers, 450 orders and 20 customers without orders, INNER is 450, LEFT 470, RIGHT 450, FULL 470 and CROSS 45,000.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
-- 100 customers (ids 1..100); 450 orders (ids 1..450) spread over customers 1..80 (customers 81..100 never order)
```
The data is generated in the Code block (loops), not typed in by hand; the sizes are the point.

**SQL answer:** the `COUNT(*)` queries over each join type in the Code block (the dict `counts`), plus the grain checks `COUNT(*)` versus `COUNT(DISTINCT customer_id)` on each table.

**pandas answer:** `len(cust.merge(orders, on="customer_id", how=...))` for each `how`, `cust["customer_id"].is_unique`, `cust["customer_id"].nunique()`, and `validate="one_to_many"` as a guard.

**Example (by hand):**
- Every order has a valid customer and the key is unique in `customers`, so each order matches exactly one customer. INNER = 450.
- LEFT keeps all 100 customers: 450 matched rows, plus the 20 customers with no orders, once each. 450 + 20 = 470.
- RIGHT keeps all 450 orders. Every order already matched, so there are no extra rows: 450.
- FULL: 450 matched + 20 unmatched customers + 0 unmatched orders = 470.
- CROSS: 100 x 450 = 45,000, no keys involved.
- Duplicated key in `customers`: if customers 1 to 5 are each loaded twice, every order of those customers matches twice. In my data customers 1 to 5 have 6 orders each (30 orders), so INNER grows by 30 to 480. If customer 90 (no orders) is also duplicated, LEFT grows by 1 for that unmatched row on top: 480 + 20 + 1 = 501.

**Code:** run with `python3 -I`.
```python
# Q11: predicting join row counts; 100 customers, 450 orders, 20 customers without orders.
import sqlite3
from collections import Counter
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE customers(customer_id INTEGER, name TEXT); CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);")
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, f"c{i}") for i in range(1, 101)])
# customers 81..100 (20 of them) never order; orders 1..450 are spread over customers 1..80
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i - 1) % 80 + 1, 10) for i in range(1, 451)])
n = lambda q: con.execute(q).fetchone()[0]
J = "customers c {} orders o ON o.customer_id = c.customer_id"
counts = {k: n(f"SELECT COUNT(*) FROM " + J.format(k)) for k in ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"]}
counts["CROSS"] = n("SELECT COUNT(*) FROM customers CROSS JOIN orders")
print("SQL counts:", counts)
assert counts == {"INNER JOIN": 450, "LEFT JOIN": 470, "RIGHT JOIN": 450, "FULL JOIN": 470, "CROSS": 45000}

print("grain customers: COUNT(*) =", n("SELECT COUNT(*) FROM customers"), " COUNT(DISTINCT customer_id) =", n("SELECT COUNT(DISTINCT customer_id) FROM customers"))
print("grain orders   : COUNT(*) =", n("SELECT COUNT(*) FROM orders"), " COUNT(DISTINCT order_id) =", n("SELECT COUNT(DISTINCT order_id) FROM orders"))

# duplicate customer_id: customers 1..5 (they have orders) and customer 90 (no orders) loaded twice
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, f"c{i}") for i in (1, 2, 3, 4, 5, 90)])
inner_dup = n("SELECT COUNT(*) FROM " + J.format("INNER JOIN"))
left_dup = n("SELECT COUNT(*) FROM " + J.format("LEFT JOIN"))
print("after duplicating customers 1-5 and 90: INNER", inner_dup, "| LEFT", left_dup)

# formula: sum over keys of (left rows with key) x (right rows with key); LEFT adds unmatched left rows
cl = Counter(r[0] for r in con.execute("SELECT customer_id FROM customers"))
cr = Counter(r[0] for r in con.execute("SELECT customer_id FROM orders"))
pred_inner = sum(cl[k] * cr[k] for k in cl)
pred_left = pred_inner + sum(cl[k] for k in cl if k not in cr)
print("formula predicts INNER", pred_inner, "LEFT", pred_left)
assert pred_inner == inner_dup and pred_left == left_dup

# pandas: the same counts and the checks
cust = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
print("pandas: customer_id.is_unique:", cust["customer_id"].is_unique, "| rows", len(cust), "nunique", cust["customer_id"].nunique())
assert len(cust.merge(orders, on="customer_id")) == inner_dup
assert len(cust.merge(orders, on="customer_id", how="left")) == left_dup
cust1 = cust.drop_duplicates("customer_id")
res = {h: len(cust1.merge(orders, on="customer_id", how=h)) for h in ["inner", "left", "right", "outer"]}
res["cross"] = len(cust1.merge(orders, how="cross"))
print("pandas on deduplicated customers:", res)
assert res == {"inner": 450, "left": 470, "right": 450, "outer": 470, "cross": 45000}
assert len(cust1.merge(orders, on="customer_id", validate="one_to_many")) == 450
print("asserts passed")
```

**Output (my run):**
```text
SQL counts: {'INNER JOIN': 450, 'LEFT JOIN': 470, 'RIGHT JOIN': 450, 'FULL JOIN': 470, 'CROSS': 45000}
grain customers: COUNT(*) = 100  COUNT(DISTINCT customer_id) = 100
grain orders   : COUNT(*) = 450  COUNT(DISTINCT order_id) = 450
after duplicating customers 1-5 and 90: INNER 480 | LEFT 501
formula predicts INNER 480 LEFT 501
pandas: customer_id.is_unique: False | rows 106 nunique 100
pandas on deduplicated customers: {'inner': 450, 'left': 470, 'right': 450, 'outer': 470, 'cross': 45000}
asserts passed
```

**Edge cases:**
- **One-to-one:** at most min(left, right) rows for INNER.
- **Many-to-many:** the per-key product can exceed both table sizes (Part 2 Q34).
- **NULL keys:** never match, so they are missing from INNER and appear once in outer joins.
- **Empty table:** INNER and CROSS give 0, outer joins give the preserved side.
- **Filters in ON versus WHERE** change outer-join counts (Part 2 Q3).

**Then explain:**
- **Cardinality:** one-to-one (each key at most once on both sides), one-to-many (the key is unique on one side only; the many side drives the row count), many-to-many (neither side unique; rows multiply per key).
- **Estimate before running:** know the grain (what one row means) and key uniqueness of each table, then apply the formula `sum over keys of left_count x right_count`. The Code block applies that formula with a `Counter` and gets 480 and 501, matching the real joins.
- **Verify the grain:** `COUNT(*)` equals `COUNT(DISTINCT key)` only if the key is unique. Here both were 100 for customers and 450 for orders. After the duplicates were loaded, pandas showed 106 rows but 100 unique ids.
- **pandas check:** `is_unique`, `nunique()` versus `len`, `validate=`, and `len(result)` compared with the expected number.

**Follow-ups:**
- *Why is the CROSS JOIN count useful?* It is the upper bound of any join, a sanity limit.
- *What if the join is on a non-unique key on both sides?* Multiply per key, then sum.
- *How do I guard this in production?* Row-count assertions and constraints (Part 2 Q40).

**Common mistakes:**
- Assuming a LEFT JOIN returns exactly the left row count.
- Forgetting the unmatched rows in the outer-join count.
- Trusting a key is unique because it is named `id`.
- Counting rows after the join and not before.

### Q12 ⭐⭐⭐ 🟡 Fan-out inflates SUM: orders(order_id, customer_id, order_total) and order_items(item_id, order_id, product_id, qty). An analyst writes SELECT SUM(o.order_total) FROM orders o JOIN order_items i ON i.order_id = o.order_id and gets double the revenue. Explain exactly why (one-to-many repeats the order row), show the correct versions (sum from orders alone, aggregate items to one row per order first then join, or SUM over distinct order ids is NOT safe), and show the same bug and fix in pandas.
**Asked at:** data-modelling write-ups on fan and chasm traps (Coginiti, Sisense, Holistics; snippets), not candidate reports; analyst and data scientist rounds and BI debugging
**Say this first (1 line):** Joining orders to order_items repeats each order's `order_total` once per item, so `SUM(order_total)` over the join adds it several times; sum from `orders` alone, or aggregate the items to one row per order before joining, and do not use `SUM(DISTINCT)` because it drops legitimate equal totals.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,2,80),(5,3,40);
INSERT INTO order_items VALUES (1,1,7,1),(2,1,8,2),(3,2,7,1),(4,3,7,1),(5,3,8,1),(6,3,9,3),(7,4,7,1);
-- order 1 has 2 items, 2 has 1, 3 has 3, 4 has 1, 5 has none
```

**SQL answer:** in the Code block: `sql_bug` (the analyst's query), `sql_orders_only`, `sql_distinct` (`SUM(DISTINCT ...)`, also wrong), `sql_fix` (LEFT JOIN to a derived table that sums `qty` per `order_id`) and `sql_fix_units` (the fix when you need item totals as well).

**pandas answer:** the bug is `orders.merge(items, on="order_id")["order_total"].sum()`; the fixes are `orders["order_total"].sum()` or `per_order = items.groupby("order_id", as_index=False).agg(units=("qty","sum"))` then `orders.merge(per_order, on="order_id", how="left", validate="one_to_one")`.

**Example:** True revenue: 100 + 50 + 80 + 80 + 40 = 350.
- Joined (INNER): order 1 appears 2 times (200), order 2 once (50), order 3 three times (240), order 4 once (80). Order 5 has no items so it disappears. Total 570, which is 1.63 times the true value and not "double". It is double only if every order has exactly two items.
- `SUM(DISTINCT order_total)` over the join: the distinct values are 100, 50, 80 (the 40 is gone with order 5). Total 230. Orders 3 and 4 have the same total of 80 and one of them is lost, so this is wrong in the other direction.
- Pre-aggregated: one row per order in the derived table, so the join cannot repeat order rows. Total 350.

**Code:** run with `python3 -I`.
```python
# Q12: fan-out inflates SUM(order_total); the fixes in SQL and pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,2,80),(5,3,40);
INSERT INTO order_items VALUES (1,1,7,1),(2,1,8,2),(3,2,7,1),(4,3,7,1),(5,3,8,1),(6,3,9,3),(7,4,7,1);
-- order 1 has 2 items, 2 has 1, 3 has 3, 4 has 1, 5 has none
""")
one = lambda q: con.execute(q).fetchone()[0]
sql_bug = "SELECT SUM(o.order_total) FROM orders o JOIN order_items i ON i.order_id = o.order_id"
sql_orders_only = "SELECT SUM(order_total) FROM orders"
sql_distinct = "SELECT SUM(DISTINCT o.order_total) FROM orders o JOIN order_items i ON i.order_id = o.order_id"
sql_fix = """SELECT SUM(o.order_total) FROM orders o
LEFT JOIN (SELECT order_id, SUM(qty) AS units FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id"""
sql_fix_units = """SELECT SUM(o.order_total) AS revenue, SUM(COALESCE(i.units, 0)) AS units FROM orders o
LEFT JOIN (SELECT order_id, SUM(qty) AS units FROM order_items GROUP BY order_id) i ON i.order_id = o.order_id"""
print("true (orders only):", one(sql_orders_only))
print("buggy join SUM    :", one(sql_bug))
print("SUM(DISTINCT)     :", one(sql_distinct), "<- also wrong")
print("pre-aggregated    :", one(sql_fix), "| with units:", con.execute(sql_fix_units).fetchone())
print("rows after join   :", one("SELECT COUNT(*) FROM orders o JOIN order_items i ON i.order_id = o.order_id"), "from", one("SELECT COUNT(*) FROM orders"), "orders")
assert (one(sql_orders_only), one(sql_bug), one(sql_distinct), one(sql_fix)) == (350, 570, 230, 350)

orders = pd.read_sql("SELECT * FROM orders", con)
items = pd.read_sql("SELECT * FROM order_items", con)
bug = orders.merge(items, on="order_id")["order_total"].sum()
dist = orders.merge(items, on="order_id")["order_total"].drop_duplicates().sum()
per_order = items.groupby("order_id", as_index=False).agg(units=("qty", "sum"))
fixed = orders.merge(per_order, on="order_id", how="left", validate="one_to_one")
print("pandas bug:", bug, "| drop_duplicates on the VALUE:", dist, "| orders alone:", orders["order_total"].sum(),
      "| pre-aggregated:", fixed["order_total"].sum(), "| units:", int(fixed["units"].fillna(0).sum()))
assert (bug, dist) == (570, 230) and fixed["order_total"].sum() == orders["order_total"].sum() == 350
assert int(fixed["units"].fillna(0).sum()) == con.execute(sql_fix_units).fetchone()[1]
# the merge is legitimately one-to-many, so validate= does NOT flag this bug
orders.merge(items, on="order_id", validate="one_to_many")
print("validate='one_to_many' passes on the buggy merge: the bug is the aggregation, not the join")
print("asserts passed")
```

**Output (my run):**
```text
true (orders only): 350
buggy join SUM    : 570
SUM(DISTINCT)     : 230 <- also wrong
pre-aggregated    : 350 | with units: (350, 10)
rows after join   : 7 from 5 orders
pandas bug: 570 | drop_duplicates on the VALUE: 230 | orders alone: 350 | pre-aggregated: 350 | units: 10
validate='one_to_many' passes on the buggy merge: the bug is the aggregation, not the join
asserts passed
```

**Edge cases:**
- **Orders with no items:** an INNER JOIN drops them (order 5, 40 missing). Even a correct pre-aggregation needs a LEFT JOIN if you want them counted.
- **Premise check:** the question says "double"; the multiplier depends on the number of items per order (here 570 versus 350). The same query would also be too small if orders without items were large.
- **COUNT:** `COUNT(DISTINCT o.order_id)` rescues a count of orders, but not a sum.
- **pandas:** `validate="one_to_many"` passed on the buggy merge, because the merge is legitimately one-to-many. The bug is in the aggregation, not in the join. `validate="one_to_one"` on the fixed merge guards the grain.
- **Dropping duplicates on the value** (`order_total.drop_duplicates()`) gave the same wrong 230 as `SUM(DISTINCT)`; dropping duplicates on `order_id` would be right but is just a roundabout way of summing from `orders`.

**Then explain:**
- **Why:** the join returns one row per item (7 rows from 5 orders), and the order-level column is carried on each. SUM adds every copy.
- **Rule:** only aggregate a column at the grain where it lives. Order-level numbers belong to the orders grain; item-level numbers to the items grain.
- **Fixes in order of preference:** (1) sum from the table where the column lives; (2) if you need both levels, aggregate the many side to the parent's grain, then join; (3) avoid `SUM(DISTINCT)`.
- **Detect it:** compare `COUNT(*)` before and after the join, and compare the total to the same sum from the source table (570 versus 350 here).

**Follow-ups:**
- *What if I need revenue per product and per order?* Different grains, different queries (Part 2 Q13, two child tables).
- *Is there a safe DISTINCT form?* Only over a pair like `(order_id, order_total)` in a derived table, and aggregating that; it is clearer to sum from `orders`.
- *Does a window function fix it?* It can (Part 4); the grain rule is the same.

**Common mistakes:**
- Using `SUM(DISTINCT)`.
- Blaming the data when the total is 570 and the source says 350.
- Not noticing the INNER JOIN also removed orders without items.
- In pandas, trusting `validate=` to catch this bug.
