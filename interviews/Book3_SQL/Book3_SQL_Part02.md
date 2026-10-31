# Book 3 — Part 2: Joins (all types, self joins, anti and semi joins) with pandas equivalents

**Topic:** INNER, LEFT, RIGHT, FULL OUTER and CROSS joins, ON versus WHERE for outer joins, NULL join keys, one-to-many and many-to-many fan-out and the aggregate-before-join fix, duplicate keys, anti-joins (LEFT JOIN IS NULL, NOT EXISTS, NOT IN with NULLs), semi-joins (EXISTS, IN, JOIN plus DISTINCT), self joins (managers, pairs, consecutive rows, one-level hierarchy), non-equi and range joins, date-range and interval joins, USING versus ON, NATURAL join risks, multi-table and multi-column joins, joining to a derived table, comparing two snapshots, JOIN versus UNION, UNION versus UNION ALL, EXCEPT and INTERSECT, cartesian products and calendar-by-entity grids, simulating FULL OUTER JOIN, join performance at concept level, and the pandas side (merge how/on/left_on/right_on/suffixes/indicator/validate, join versus merge versus concat, index joins, merge_asof, cross merge, NaN keys, dtype mismatches, anti-join via indicator or isin)
**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 18, ⭐⭐ 17, ⭐ 10)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part covers joins and set operators. Window functions and ranking (Parts 3 to 5), CTE-based solutions (Part 3), 'second highest salary' (Part 4), recursive hierarchies (Part 9) and EXPLAIN-level tuning (Part 11) are deliberately absent; where a question touches them the answer stays at the join-only solution and points to the later part. Every query question states its tables and columns so Wave B can build small sample data; answers must run on SQLite 3.45 and compare with pandas 3.0.x, and anything engine-specific is shown as hedged text labelled 'not executed'.

Verification notes for Wave B: the pandas user guide page (merge, join, concatenate) and the merge_asof reference were opened and give: how = left, right, outer, inner (default), cross; validate raises MergeError (one_to_one, one_to_many shown); indicator adds a categorical _merge column (left_only, right_only, both); suffixes default ('_x', '_y'); a many-to-many merge returns the Cartesian product of matching rows; DataFrame.join defaults to a left join on the index; concat defaults to an outer join of the other axis; merge_asof needs both frames sorted ascending on a numeric or datetime key and has by, direction (backward default, forward, nearest), tolerance and allow_exact_matches. The MySQL 8.4 join page was opened and shows only LEFT and RIGHT [OUTER] JOIN (no FULL OUTER JOIN), the NATURAL and USING definitions and column order, and the LEFT JOIN IS NULL anti-join example. The SQLite SELECT page diagram lists NATURAL, LEFT, RIGHT, FULL, INNER, CROSS, UNION, UNION ALL, INTERSECT and EXCEPT but does not state versions: the 3.39 version for RIGHT and FULL JOIN is from general knowledge and must be confirmed by running on 3.45. That NaN keys match each other in a pandas merge was NOT stated on the user guide page (it was noted on the 'Comparison with SQL' page in Part 1 research) and must be confirmed by running. Dialect claims about PostgreSQL, SQL Server, Oracle, BigQuery, Snowflake, EXCEPT versus MINUS, MySQL INTERSECT/EXCEPT versions and USING details per engine come from general knowledge or snippets and must be hedged.

Evidence limits: no candidate-reported SQL questions were found; the search returned prep guides, question banks and documentation. The 'Asked at' tags are source types, and 'expert gap-check' marks questions chosen from practice. Star ratings blend how often a topic appears across guides with judgement. See research_notes/Book3_Part02_sources.md for which pages were opened.

---

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

### Q13 ⭐⭐⭐ 🟡 Two child tables, one parent (the chasm trap): customers(customer_id, name), orders(order_id, customer_id, amount) and support_tickets(ticket_id, customer_id). Report per customer the total order amount and the ticket count in one query. Show why joining both child tables directly multiplies rows (3 orders x 2 tickets = 6 rows) and gives wrong totals, and fix it by aggregating each child to one row per customer before joining. Say when COUNT(DISTINCT) rescues a count but not a SUM. Give pandas.
**Asked at:** data-modelling write-ups on fan and chasm traps (Coginiti, Sisense, Holistics; snippets), not candidate reports; analyst and data scientist rounds and BI debugging
**Say this first (1 line):** Joining two child tables straight onto one parent makes every order meet every ticket for that customer (3 orders x 2 tickets = 6 rows), so any SUM or COUNT is multiplied; aggregate each child to one row per customer first, then LEFT JOIN those two small tables to the customer.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE support_tickets(ticket_id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,20),(102,1,20),(103,1,30),(104,2,50);
INSERT INTO support_tickets VALUES (201,1),(202,1),(203,3);
```

**SQL answer:** the fix is `SQL_MAIN` in the Code block (the broken version is `SQL_NAIVE`, run next to it).
```sql
SELECT c.customer_id, c.name,
       COALESCE(o.total_amount, 0) AS total_amount,
       COALESCE(t.ticket_count, 0) AS ticket_count
FROM customers c
LEFT JOIN (SELECT customer_id, SUM(amount) AS total_amount
           FROM orders GROUP BY customer_id) o ON o.customer_id = c.customer_id
LEFT JOIN (SELECT customer_id, COUNT(*) AS ticket_count
           FROM support_tickets GROUP BY customer_id) t ON t.customer_id = c.customer_id
ORDER BY c.customer_id
```
The naive version, for contrast (also executed):
```sql
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.amount), 0)           AS total_amount,
       COUNT(t.ticket_id)                   AS ticket_count,
       COUNT(DISTINCT t.ticket_id)          AS ticket_count_distinct,
       COALESCE(SUM(DISTINCT o.amount), 0)  AS sum_distinct_amount,
       COUNT(*)                             AS joined_rows
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN support_tickets t ON t.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id
```

**pandas answer:** aggregate each child with `groupby`, then merge the two small frames onto customers. `validate="one_to_one"` makes pandas raise if either aggregate is not one row per customer.
```python
order_tot = orders.groupby("customer_id", as_index=False).agg(total_amount=("amount", "sum"))
ticket_cnt = tickets.groupby("customer_id", as_index=False).agg(ticket_count=("ticket_id", "size"))
pd_df = (customers[["customer_id", "name"]]
         .merge(order_tot, on="customer_id", how="left", validate="one_to_one")
         .merge(ticket_cnt, on="customer_id", how="left", validate="one_to_one")
         .fillna({"total_amount": 0, "ticket_count": 0})
         .astype({"total_amount": "int64", "ticket_count": "int64"})
         .sort_values("customer_id").reset_index(drop=True))
```

**Example:** Asha has 3 orders (20, 20, 30; real total 70) and 2 tickets (201, 202).
- Joined directly, Asha becomes 3 x 2 = 6 rows. Each order row appears twice, so `SUM(amount)` = 2 x 70 = 140. Each ticket row appears three times, so `COUNT(t.ticket_id)` = 6.
- `COUNT(DISTINCT t.ticket_id)` = 2 is right, because ticket ids are unique. `SUM(DISTINCT o.amount)` = 20 + 30 = 50 is wrong (real 70, naive 140): it threw away the second order of 20.
- Ben: 1 order (50) and no tickets gives 1 joined row, so the naive result is correct for him. Chitra: no orders and 1 ticket gives 1 row with a NULL amount. Dev: 1 row, all NULL. The bug only bites customers that have 2 or more rows in both children, which is why it can pass a quick check on a few customers.
- Fixed: orders aggregate to (1, 70), (2, 50); tickets aggregate to (1, 2), (3, 1). Each side has one row per customer, so the LEFT JOINs add no rows. `COALESCE` turns the missing sides (Chitra's total, Ben's and Dev's ticket count) into 0.

**Code:** run with `python3 -I`.
```python
# Q13: chasm trap, two child tables under one parent: naive double join vs aggregate-each-child-first
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE support_tickets(ticket_id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,20),(102,1,20),(103,1,30),(104,2,50);
INSERT INTO support_tickets VALUES (201,1),(202,1),(203,3);
"""
SQL_NAIVE = """
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.amount), 0)           AS total_amount,
       COUNT(t.ticket_id)                   AS ticket_count,
       COUNT(DISTINCT t.ticket_id)          AS ticket_count_distinct,
       COALESCE(SUM(DISTINCT o.amount), 0)  AS sum_distinct_amount,
       COUNT(*)                             AS joined_rows
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN support_tickets t ON t.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id
"""
SQL_MAIN = """
SELECT c.customer_id, c.name,
       COALESCE(o.total_amount, 0) AS total_amount,
       COALESCE(t.ticket_count, 0) AS ticket_count
FROM customers c
LEFT JOIN (SELECT customer_id, SUM(amount) AS total_amount
           FROM orders GROUP BY customer_id) o ON o.customer_id = c.customer_id
LEFT JOIN (SELECT customer_id, COUNT(*) AS ticket_count
           FROM support_tickets GROUP BY customer_id) t ON t.customer_id = c.customer_id
ORDER BY c.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
naive = pd.read_sql_query(SQL_NAIVE, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL naive (both children joined directly):")
print(naive.to_string(index=False))
print("\nSQL fixed (each child aggregated to one row per customer first):")
print(sql_df.to_string(index=False))

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
tickets = pd.read_sql_query("SELECT * FROM support_tickets", con)

# pandas naive: the same fan-out
fan = customers.merge(orders, on="customer_id", how="left").merge(tickets, on="customer_id", how="left")
print("\npandas naive merge, rows for Asha:", int((fan["customer_id"] == 1).sum()), "| total rows:", len(fan))
print("pandas naive sum of amount for Asha:", fan.loc[fan["customer_id"] == 1, "amount"].sum())

# pd:main
order_tot = orders.groupby("customer_id", as_index=False).agg(total_amount=("amount", "sum"))
ticket_cnt = tickets.groupby("customer_id", as_index=False).agg(ticket_count=("ticket_id", "size"))
pd_df = (customers[["customer_id", "name"]]
         .merge(order_tot, on="customer_id", how="left", validate="one_to_one")
         .merge(ticket_cnt, on="customer_id", how="left", validate="one_to_one")
         .fillna({"total_amount": 0, "ticket_count": 0})
         .astype({"total_amount": "int64", "ticket_count": "int64"})
         .sort_values("customer_id").reset_index(drop=True))
# pd:end
print("\npandas fixed:")
print(pd_df.to_string(index=False))

# compared after sorting both by customer_id
pd.testing.assert_frame_equal(sql_df.sort_values("customer_id").reset_index(drop=True), pd_df, check_dtype=False)
assert naive.loc[0, "total_amount"] == 140 and sql_df.loc[0, "total_amount"] == 70
assert orders["amount"].sum() == sql_df["total_amount"].sum() == 120   # totals tie to the child table
assert tickets.shape[0] == sql_df["ticket_count"].sum() == 3
print("\nasserts passed: SQL == pandas; totals tie to the child tables (120 and 3 tickets)")
```

**Output (my run):**
```text
SQL naive (both children joined directly):
 customer_id   name  total_amount  ticket_count  ticket_count_distinct  sum_distinct_amount  joined_rows
           1   Asha           140             6                      2                   50            6
           2    Ben            50             0                      0                   50            1
           3 Chitra             0             1                      1                    0            1
           4    Dev             0             0                      0                    0            1

SQL fixed (each child aggregated to one row per customer first):
 customer_id   name  total_amount  ticket_count
           1   Asha            70             2
           2    Ben            50             0
           3 Chitra             0             1
           4    Dev             0             0

pandas naive merge, rows for Asha: 6 | total rows: 9
pandas naive sum of amount for Asha: 140.0

pandas fixed:
 customer_id   name  total_amount  ticket_count
           1   Asha            70             2
           2    Ben            50             0
           3 Chitra             0             1
           4    Dev             0             0

asserts passed: SQL == pandas; totals tie to the child tables (120 and 3 tickets)
```

**Edge cases:**
- Customers with no orders or no tickets: the LEFT JOIN gives NULL, so `COALESCE(..., 0)` is needed in SQL and `fillna(0)` in pandas. In pandas the merged column turns `float64` (NaN), so I cast back to `int64`.
- If I used INNER JOINs to the aggregates, Ben, Chitra and Dev would vanish, because each is missing from one of the two children.
- Orphan children (an order whose customer_id is not in customers) are dropped by joining from `customers`; check totals against the child table to catch that. My assert compares 120 (sum of all orders) and 3 (all tickets) with the fixed result.
- Three child tables multiply the same way, and the fix is the same: one aggregate per child, then join.

**Then explain:**
- **Why it multiplies:** a join returns, for each customer, every combination of one matching order row and one matching ticket row. The two children are not related to each other, so every order pairs with every ticket. Rows per customer = orders x tickets.
- **Rule:** before joining, get every child to the same grain as the parent (one row per customer). Join aggregates, not raw rows.
- **COUNT(DISTINCT):** rescues a count only when you count a unique id of the child that was repeated (`COUNT(DISTINCT t.ticket_id)`, `COUNT(DISTINCT o.order_id)`). It cannot rescue a SUM: `SUM(DISTINCT amount)` collapses equal values that belong to different orders. It also costs a sort or hash on the multiplied rows, so it is a patch, not a design.
- **Order of joins does not help:** joining orders first and tickets second, or the reverse, gives the same 6 rows for Asha.
- **Check:** compare per-customer totals to `SUM(amount)` on the orders table alone. In my run the naive total for Asha is 140, orders alone give 70.
- Scalar subqueries in the SELECT list also work, but I have not run that form here.

**Follow-ups:**
- *Why is this called a chasm trap?* It is the data-modelling name for two one-to-many branches hanging off one parent (the BI-tool write-ups also call the single-branch version a fan trap).
- *Can I fix it with SUM(DISTINCT order_id)-style tricks?* Not safely: you can only distinct a value, and amounts repeat. Aggregate first.
- *What if I need the order and ticket detail rows?* Then they do not belong in one result; return two result sets, or accept the multiplication knowingly and never sum across it.

**Common mistakes:**
- Spotting the inflated SUM and adding `DISTINCT` to it.
- Fixing the count with `COUNT(DISTINCT)` and forgetting the SUM next to it is still wrong.
- Using INNER JOINs to the aggregates and silently dropping customers with no tickets.
- Not checking the result against each child table's own total.
- In pandas, two merges in a row with no `validate=` and no row-count check.

### Q14 ⭐⭐⭐ 🟡 Students and Examinations style grid: students(student_id, name), subjects(subject_name) and exams(student_id, subject_name), one row per exam attended. Report, for every student and every subject, how many times the student attended the exam, including 0. Explain why a CROSS JOIN of students and subjects comes first and a LEFT JOIN to exams second, and give the pandas version (how='cross', then merge and fillna).
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Build the full grid first with a CROSS JOIN of students and subjects (every student-subject pair, even if never examined), then LEFT JOIN the exams onto the grid and COUNT a column from the exams side, so pairs with no exams show 0.

**Schema and sample data:**
```sql
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE subjects(subject_name TEXT PRIMARY KEY);
CREATE TABLE exams(student_id INTEGER, subject_name TEXT);
INSERT INTO students VALUES (1,'Alice'),(2,'Bob'),(6,'Alex'),(13,'John');
INSERT INTO subjects VALUES ('Math'),('Physics'),('Programming');
INSERT INTO exams VALUES (1,'Math'),(1,'Physics'),(1,'Programming'),(2,'Programming'),(1,'Physics'),
 (1,'Math'),(13,'Math'),(13,'Programming'),(13,'Physics'),(2,'Math'),(1,'Math');
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT st.student_id, st.name, su.subject_name,
       COUNT(e.subject_name) AS attended_exams
FROM students st
CROSS JOIN subjects su
LEFT JOIN exams e ON e.student_id = st.student_id AND e.subject_name = su.subject_name
GROUP BY st.student_id, st.name, su.subject_name
ORDER BY st.student_id, su.subject_name
```

**pandas answer:** `how="cross"` for the grid, `groupby(...).size()` for the counts, then a left merge and `fillna`.
```python
grid = students.merge(subjects, how="cross")
counts = exams.groupby(["student_id", "subject_name"], as_index=False).agg(attended_exams=("subject_name", "size"))
pd_df = (grid.merge(counts, on=["student_id", "subject_name"], how="left", validate="one_to_one")
         .fillna({"attended_exams": 0}).astype({"attended_exams": "int64"})
         .sort_values(["student_id", "subject_name"]).reset_index(drop=True))
```

**Example:** 4 students x 3 subjects = 12 grid rows.
- Alice's exam rows: Math x3, Physics x2, Programming x1, so (3, 2, 1).
- Bob: Math 1, Programming 1, Physics 0 (no exam row, so the LEFT JOIN gives NULL and `COUNT(e.subject_name)` counts 0).
- Alex (id 6): no exam rows at all, so (0, 0, 0). John (13): (1, 1, 1).
- The counts add up to 3+2+1+1+0+1+0+0+0+1+1+1 = 11, the number of rows in `exams`. My assert checks this.

**Code:** run with `python3 -I`.
```python
# Q14: students x subjects grid with exam counts (CROSS JOIN first, LEFT JOIN second)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE subjects(subject_name TEXT PRIMARY KEY);
CREATE TABLE exams(student_id INTEGER, subject_name TEXT);
INSERT INTO students VALUES (1,'Alice'),(2,'Bob'),(6,'Alex'),(13,'John');
INSERT INTO subjects VALUES ('Math'),('Physics'),('Programming');
INSERT INTO exams VALUES (1,'Math'),(1,'Physics'),(1,'Programming'),(2,'Programming'),(1,'Physics'),
 (1,'Math'),(13,'Math'),(13,'Programming'),(13,'Physics'),(2,'Math'),(1,'Math');
"""
SQL_MAIN = """
SELECT st.student_id, st.name, su.subject_name,
       COUNT(e.subject_name) AS attended_exams
FROM students st
CROSS JOIN subjects su
LEFT JOIN exams e ON e.student_id = st.student_id AND e.subject_name = su.subject_name
GROUP BY st.student_id, st.name, su.subject_name
ORDER BY st.student_id, su.subject_name
"""
SQL_WRONG_COUNT = """
SELECT st.student_id, su.subject_name, COUNT(*) AS attended_exams
FROM students st CROSS JOIN subjects su
LEFT JOIN exams e ON e.student_id = st.student_id AND e.subject_name = su.subject_name
WHERE st.student_id = 6
GROUP BY st.student_id, su.subject_name ORDER BY su.subject_name
"""
SQL_NO_GRID = """
SELECT st.student_id, e.subject_name, COUNT(*) AS attended_exams
FROM students st LEFT JOIN exams e ON e.student_id = st.student_id
WHERE st.student_id = 6 GROUP BY st.student_id, e.subject_name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nrows:", len(sql_df), "= 4 students x 3 subjects")
print("\nCOUNT(*) instead of COUNT(e.subject_name), Alex (no exams):")
print(pd.read_sql_query(SQL_WRONG_COUNT, con).to_string(index=False))
print("\nLEFT JOIN students to exams only, no grid, Alex:")
print(pd.read_sql_query(SQL_NO_GRID, con).to_string(index=False))

students = pd.read_sql_query("SELECT * FROM students", con)
subjects = pd.read_sql_query("SELECT * FROM subjects", con)
exams = pd.read_sql_query("SELECT * FROM exams", con)

# pd:main
grid = students.merge(subjects, how="cross")
counts = exams.groupby(["student_id", "subject_name"], as_index=False).agg(attended_exams=("subject_name", "size"))
pd_df = (grid.merge(counts, on=["student_id", "subject_name"], how="left", validate="one_to_one")
         .fillna({"attended_exams": 0}).astype({"attended_exams": "int64"})
         .sort_values(["student_id", "subject_name"]).reset_index(drop=True))
# pd:end
print("\npandas dtype of attended_exams after fillna and astype:", pd_df["attended_exams"].dtype)
raw = grid.merge(counts, on=["student_id", "subject_name"], how="left")
print("dtype before fillna:", raw["attended_exams"].dtype)

# compared after sorting by student_id, subject_name
pd.testing.assert_frame_equal(sql_df.sort_values(["student_id", "subject_name"]).reset_index(drop=True),
                              pd_df[sql_df.columns], check_dtype=False)
assert pd_df["attended_exams"].sum() == len(exams) == 11
print("asserts passed: SQL == pandas; counts sum to", len(exams), "exam rows")
```

**Output (my run):**
```text
 student_id  name subject_name  attended_exams
          1 Alice         Math               3
          1 Alice      Physics               2
          1 Alice  Programming               1
          2   Bob         Math               1
          2   Bob      Physics               0
          2   Bob  Programming               1
          6  Alex         Math               0
          6  Alex      Physics               0
          6  Alex  Programming               0
         13  John         Math               1
         13  John      Physics               1
         13  John  Programming               1

rows: 12 = 4 students x 3 subjects

COUNT(*) instead of COUNT(e.subject_name), Alex (no exams):
 student_id subject_name  attended_exams
          6         Math               1
          6      Physics               1
          6  Programming               1

LEFT JOIN students to exams only, no grid, Alex:
 student_id subject_name  attended_exams
          6         None               1

pandas dtype of attended_exams after fillna and astype: int64
dtype before fillna: float64
asserts passed: SQL == pandas; counts sum to 11 exam rows
```

**Edge cases:**
- A student who sat nothing (Alex) still gets three rows of 0, because the grid is built before the exams are looked at.
- A student-subject pair can have many exam rows (Alice took Math three times), so the count can exceed 1. A pair is not unique in `exams`, which is why pandas counts with `groupby().size()` before merging, and why the merge can use `validate="one_to_one"`.
- Duplicate rows in `subjects` or `students` would multiply the grid; the primary key on `subject_name` in the sample guards that in SQL.
- A subject listed in `exams` but missing from `subjects` never appears in the output, because the grid is the source of truth.

**Then explain:**
- **Why CROSS JOIN first:** a LEFT JOIN keeps every row of its left side and nothing else. The left side must already contain every (student, subject) combination, and only a cross product of the two lists can create the combinations that never happened.
- **Why the LEFT JOIN second:** it attaches the exam rows, leaving NULLs where none exist. The ON condition has both keys (student and subject).
- **COUNT(e.subject_name), not COUNT(*):** for Alex, `COUNT(*)` counts the one NULL-extended row and returns 1 for every subject (shown in my output). Counting a column from the right table ignores NULLs and gives 0.
- **Without the grid:** a LEFT JOIN of students to exams alone gives Alex one row with a NULL subject, and Bob has no Physics row at all (shown in my output).
- **pandas dtype:** after the left merge the count column is `float64` (NaN for missing), `fillna(0)` alone keeps float, so cast to `int64` (both dtypes printed in my run).

**Follow-ups:**
- *What if the subject list should come from the data, not a table?* `SELECT DISTINCT subject_name FROM exams` as a derived table works, but it misses subjects nobody took, so keep a subjects table.
- *Can this be done with GROUP BY on exams alone?* No, there are no rows for the zero cases.
- *Cost?* The grid has students x subjects rows, which is fine here and large only for big dimension tables.

**Common mistakes:**
- Using `COUNT(*)` and getting 1 instead of 0.
- A LEFT JOIN from students to exams only, with no grid.
- Putting the subject condition in WHERE (which would turn the LEFT JOIN into an inner join, Q3).
- Forgetting to cast back to integer after `fillna` in pandas.
- Counting rows from `exams` per student without grouping by subject.

### Q15 ⭐⭐⭐ 🟡 Self join for pairs: employees(emp_id, name, dept_id). List all pairs of colleagues in the same department, each pair once and never an employee with themselves. Explain why a.emp_id < b.emp_id (not <>) removes mirror pairs, how many pairs n employees produce, and how to do the same in pandas (merge on dept_id then filter, and itertools.combinations as an alternative).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Self-join employees to itself on the same dept_id with `a.emp_id < b.emp_id`: it drops the self pairs and keeps exactly one of the two mirror pairs; n employees in a department make n(n-1)/2 pairs.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',10),(3,'Chitra',10),(4,'Dev',20),(5,'Esha',20),
                             (6,'Farah',30),(7,'Gopal',NULL),(8,'Hari',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT a.dept_id, a.name AS name_a, b.name AS name_b
FROM employees a
JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id < b.emp_id
ORDER BY a.dept_id, a.emp_id, b.emp_id
```

**pandas answer:** merge the frame with itself on `dept_id`, filter on the id order. I drop NaN departments first (reason below). The alternative is `itertools.combinations` per group; both are in the Code block.
```python
m = emp.dropna(subset=["dept_id"]).merge(emp.dropna(subset=["dept_id"]), on="dept_id", suffixes=("_a", "_b"))
pd_df = (m[m["emp_id_a"] < m["emp_id_b"]][["dept_id", "name_a", "name_b", "emp_id_a", "emp_id_b"]]
         .sort_values(["dept_id", "emp_id_a", "emp_id_b"]).reset_index(drop=True))
```

**Example:** departments 10 = Asha(1), Ben(2), Chitra(3); 20 = Dev(4), Esha(5); 30 = Farah(6); Gopal(7) and Hari(8) have no department.
- Dept 10: pairs (1,2), (1,3), (2,3) = 3 = 3x2/2. Dept 20: (4,5) = 1. Dept 30: no pair (1 person gives 0). Gopal and Hari: NULL = NULL is not true, so no join, no pair.
- Total 4 pairs. With `<>` instead of `<`, each pair appears twice (8 rows). With no id filter at all the join returns 14 rows: 8 ordered pairs plus 6 rows pairing someone with themselves (3 + 2 + 1).

**Code:** run with `python3 -I`.
```python
# Q15: pairs of colleagues in the same department, each pair once (self join, a.emp_id < b.emp_id)
import sqlite3
from itertools import combinations
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',10),(3,'Chitra',10),(4,'Dev',20),(5,'Esha',20),
                             (6,'Farah',30),(7,'Gopal',NULL),(8,'Hari',NULL);
"""
SQL_MAIN = """
SELECT a.dept_id, a.name AS name_a, b.name AS name_b
FROM employees a
JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id < b.emp_id
ORDER BY a.dept_id, a.emp_id, b.emp_id
"""
SQL_NE = "SELECT COUNT(*) FROM employees a JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id <> b.emp_id"
SQL_NO_FILTER = "SELECT COUNT(*) FROM employees a JOIN employees b ON a.dept_id = b.dept_id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\npairs (a.emp_id < b.emp_id):", len(sql_df))
print("rows with <> instead of <:", con.execute(SQL_NE).fetchone()[0], "(every pair twice)")
print("rows with no id filter:", con.execute(SQL_NO_FILTER).fetchone()[0], "(8 ordered pairs + 6 self rows)")

emp = pd.read_sql_query("SELECT * FROM employees", con)
print("\ndept_id dtype in pandas:", emp["dept_id"].dtype)

# pd:main
m = emp.dropna(subset=["dept_id"]).merge(emp.dropna(subset=["dept_id"]), on="dept_id", suffixes=("_a", "_b"))
pd_df = (m[m["emp_id_a"] < m["emp_id_b"]][["dept_id", "name_a", "name_b", "emp_id_a", "emp_id_b"]]
         .sort_values(["dept_id", "emp_id_a", "emp_id_b"]).reset_index(drop=True))
# pd:end
print("\npandas merge + filter (NaN dept dropped first):", len(pd_df), "pairs")

# without dropna: NaN keys match each other in pandas merge
m_nan = emp.merge(emp, on="dept_id", suffixes=("_a", "_b"))
nan_pairs = m_nan[m_nan["emp_id_a"] < m_nan["emp_id_b"]]
print("pandas merge WITHOUT dropna, pairs:", len(nan_pairs))
print(nan_pairs[nan_pairs["dept_id"].isna()][["name_a", "name_b"]].to_string(index=False))

# itertools alternative (groupby drops NaN keys by default)
combo = [(g_dept, a, b) for g_dept, g in emp.groupby("dept_id")
         for (a, b) in combinations(g.sort_values("emp_id")["name"], 2)]
combo_df = pd.DataFrame(combo, columns=["dept_id", "name_a", "name_b"])
print("\nitertools.combinations pairs:", len(combo_df))

# n employees -> n(n-1)/2 pairs per department
sizes = emp.groupby("dept_id").size()
assert int((sizes * (sizes - 1) // 2).sum()) == len(sql_df) == 4
cmp_sql = sql_df.copy(); cmp_sql["dept_id"] = cmp_sql["dept_id"].astype(float)
# all compared after sorting by dept_id, then emp_id order (names listed in id order)
pd.testing.assert_frame_equal(cmp_sql, pd_df[["dept_id", "name_a", "name_b"]], check_dtype=False)
pd.testing.assert_frame_equal(cmp_sql.reset_index(drop=True),
                              combo_df.astype({"dept_id": "float64"}), check_dtype=False)
print("asserts passed: SQL == pandas merge+filter == itertools.combinations")
```

**Output (my run):**
```text
 dept_id name_a name_b
      10   Asha    Ben
      10   Asha Chitra
      10    Ben Chitra
      20    Dev   Esha

pairs (a.emp_id < b.emp_id): 4
rows with <> instead of <: 8 (every pair twice)
rows with no id filter: 14 (8 ordered pairs + 6 self rows)

dept_id dtype in pandas: float64

pandas merge + filter (NaN dept dropped first): 4 pairs
pandas merge WITHOUT dropna, pairs: 5
name_a name_b
 Gopal   Hari

itertools.combinations pairs: 4
asserts passed: SQL == pandas merge+filter == itertools.combinations
```

**Edge cases:**
- NULL dept_id: no pairs in SQL. Surprise in pandas: `merge` matches NaN keys to NaN keys, so merging without the `dropna` produced 5 pairs, with the extra pair Gopal-Hari (shown in the output). The `groupby` route drops NaN keys by default, so `combinations` gave 4. Decide on purpose whether "no department" people count as colleagues.
- A department with one person gives no pair; an empty department gives no row.
- Duplicate employee rows (same person loaded twice with different emp_id) show up as a pair with themselves; clean the data first.
- Ordering of the pair: `a.emp_id < b.emp_id` always puts the smaller id in column a, so (Asha, Ben) appears and (Ben, Asha) does not.

**Then explain:**
- **Why `<` and not `<>`:** `<>` removes self pairs but keeps both (a,b) and (b,a). `<` removes both the self pairs (a.emp_id = b.emp_id is not less) and the mirror pairs, because for any two people exactly one is smaller.
- **How many pairs:** n(n-1)/2 per department, so the self join grows with the square of the department size. A 1,000-person department gives 499,500 pairs, so check sizes first.
- **pandas:** the merge builds all n x n ordered pairs in memory then filters, which wastes memory for large groups; `combinations` generates only the n(n-1)/2 pairs but is a Python loop.
- The key to pass to pandas is the same `dept_id`; the suffixes `_a` and `_b` stand for the two aliases.

**Follow-ups:**
- *How would you include the pair count per department?* `GROUP BY a.dept_id` on the same join with `COUNT(*)`.
- *Three-person groups (triples)?* Add a second self join with `b.emp_id < c.emp_id`.
- *What if the table has no unique id?* Create one first, otherwise there is no ordering to break the tie.

**Common mistakes:**
- Using `<>` and reporting every pair twice.
- Using `a.name < b.name` when names can repeat (identical names would be dropped as "equal").
- Forgetting the dept condition, which makes a cross join of the whole table.
- Assuming pandas treats NaN keys like SQL treats NULLs.

### Q16 ⭐⭐⭐ 🟡 Find unmatched rows on both sides: payments(payment_id, order_id, amount) and orders(order_id, amount). List payments with no order, orders with no payment, and matched rows, in one result with a status column. Use FULL OUTER JOIN (SQLite 3.39+ runs it; hedge MySQL), and pandas merge how='outer' with indicator=True. Explain why the coalesced key is needed in the output.
**Asked at:** StrataScratch join problem list (bank items labelled with company names by the guide, not candidate reports); product-company data scientist screens
**Say this first (1 line):** FULL OUTER JOIN payments to orders on order_id, take the key with `COALESCE(o.order_id, p.order_id)`, and label each row from which side is NULL (matched, payment without order, order without payment); in pandas it is `merge(how="outer", indicator=True)`.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,300);
INSERT INTO payments VALUES (11,1,100),(12,2,150),(13,9,50),(14,NULL,70);
```

**SQL answer:** `SQL_MAIN` in the Code block (executed on SQLite 3.45.1).
```sql
SELECT COALESCE(o.order_id, p.order_id) AS order_id,
       p.payment_id, o.amount AS order_amount, p.amount AS paid_amount,
       CASE WHEN o.order_id IS NULL THEN 'payment_without_order'
            WHEN p.payment_id IS NULL THEN 'order_without_payment'
            ELSE 'matched' END AS status
FROM payments p
FULL OUTER JOIN orders o ON o.order_id = p.order_id
ORDER BY status, order_id, payment_id
```
Dialect notes, **not executed here**: PostgreSQL, SQL Server, Oracle, Snowflake and BigQuery support `FULL OUTER JOIN`; MySQL has no `FULL OUTER JOIN` (the MySQL 8.4 JOIN page I read lists only LEFT and RIGHT), so there you emulate it with a LEFT JOIN plus the unmatched right rows (Q32). That SQLite added RIGHT and FULL JOIN in version 3.39 is from memory; I could only run on 3.45.1, where both work (my run printed a RIGHT JOIN result too).

**pandas answer:** the indicator column says which side each row came from.
```python
m = payments.merge(orders, on="order_id", how="outer", indicator=True,
                   suffixes=("_pay", "_ord"), validate="many_to_one")
m["status"] = m["_merge"].map({"both": "matched", "left_only": "payment_without_order",
                               "right_only": "order_without_payment"}).astype(str)
pd_df = (m.rename(columns={"amount_ord": "order_amount", "amount_pay": "paid_amount"})
         [["order_id", "payment_id", "order_amount", "paid_amount", "status"]]
         .sort_values(["status", "order_id", "payment_id"], na_position="last").reset_index(drop=True))
```

**Example:** orders 1 (100), 2 (200), 3 (300); payments 11 -> order 1 (100), 12 -> order 2 (150), 13 -> order 9 (50), 14 -> order NULL (70).
- Orders 1 and 2 have a matching payment: status `matched` (note order 2 is matched by key even though 150 is not 200; amount checks are a separate step, Q44).
- Order 3 has no payment: `order_without_payment`.
- Payment 13 points to order 9, which does not exist: `payment_without_order`. Payment 14 has a NULL order_id, which cannot equal anything: also `payment_without_order`.
- 5 rows in total: 2 matched, 1 order without payment, 2 payments without order.

**Code:** run with `python3 -I`.
```python
# Q16: reconcile payments and orders with FULL OUTER JOIN and a status column
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,300);
INSERT INTO payments VALUES (11,1,100),(12,2,150),(13,9,50),(14,NULL,70);
"""
SQL_MAIN = """
SELECT COALESCE(o.order_id, p.order_id) AS order_id,
       p.payment_id, o.amount AS order_amount, p.amount AS paid_amount,
       CASE WHEN o.order_id IS NULL THEN 'payment_without_order'
            WHEN p.payment_id IS NULL THEN 'order_without_payment'
            ELSE 'matched' END AS status
FROM payments p
FULL OUTER JOIN orders o ON o.order_id = p.order_id
ORDER BY status, order_id, payment_id
"""
SQL_NO_COALESCE = """
SELECT o.order_id, p.payment_id FROM payments p FULL OUTER JOIN orders o ON o.order_id = p.order_id
ORDER BY o.order_id, p.payment_id
"""
SQL_RIGHT = "SELECT o.order_id, p.payment_id FROM orders o RIGHT JOIN payments p ON o.order_id = p.order_id ORDER BY p.payment_id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("SQLite version:", sqlite3.sqlite_version)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nwithout COALESCE (o.order_id only):")
print(pd.read_sql_query(SQL_NO_COALESCE, con).to_string(index=False))
print("\nRIGHT JOIN runs on this SQLite:", con.execute(SQL_RIGHT).fetchall())

payments = pd.read_sql_query("SELECT * FROM payments", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
m = payments.merge(orders, on="order_id", how="outer", indicator=True,
                   suffixes=("_pay", "_ord"), validate="many_to_one")
m["status"] = m["_merge"].map({"both": "matched", "left_only": "payment_without_order",
                               "right_only": "order_without_payment"}).astype(str)
pd_df = (m.rename(columns={"amount_ord": "order_amount", "amount_pay": "paid_amount"})
         [["order_id", "payment_id", "order_amount", "paid_amount", "status"]]
         .sort_values(["status", "order_id", "payment_id"], na_position="last").reset_index(drop=True))
# pd:end
print("\npandas outer merge with indicator:")
print(m[["order_id", "payment_id", "_merge"]].to_string(index=False))
print("\nstatus counts:", pd_df["status"].value_counts().to_dict())

def norm(d):
    d = d.copy()
    d["order_id"] = d["order_id"].astype("float64")
    for c in ["payment_id", "order_amount", "paid_amount"]:
        d[c] = d[c].astype("float64")
    return d.reset_index(drop=True)
# compared after sorting by status, then order_id, then payment_id (NULL order_id last)
s = sql_df.sort_values(["status", "order_id", "payment_id"], na_position="last")
pd.testing.assert_frame_equal(norm(s), norm(pd_df), check_dtype=False)
assert len(sql_df) == 5 and (sql_df["status"] == "matched").sum() == 2
print("asserts passed: SQL FULL JOIN == pandas outer merge")
```

**Output (my run):**
```text
SQLite version: 3.45.1
 order_id  payment_id  order_amount  paid_amount                status
      1.0        11.0         100.0        100.0               matched
      2.0        12.0         200.0        150.0               matched
      3.0         NaN         300.0          NaN order_without_payment
      NaN        14.0           NaN         70.0 payment_without_order
      9.0        13.0           NaN         50.0 payment_without_order

without COALESCE (o.order_id only):
 order_id  payment_id
      NaN        13.0
      NaN        14.0
      1.0        11.0
      2.0        12.0
      3.0         NaN

RIGHT JOIN runs on this SQLite: [(1, 11), (2, 12), (None, 13), (None, 14)]

pandas outer merge with indicator:
 order_id  payment_id     _merge
      1.0        11.0       both
      2.0        12.0       both
      3.0         NaN right_only
      9.0        13.0  left_only
      NaN        14.0  left_only

status counts: {'matched': 2, 'payment_without_order': 2, 'order_without_payment': 1}
asserts passed: SQL FULL JOIN == pandas outer merge
```

**Edge cases:**
- NULL order_id in payments: never matches, so it lands in the unmatched-payment group. After `COALESCE` its order_id is still NULL, so identify such rows by `payment_id`.
- Several payments for one order give several matched rows (a one-to-many join); aggregate first if you need one row per order (Q44).
- Duplicate order_id in orders would duplicate rows; in pandas `validate="many_to_one"` (payments on the left, orders on the right) raises an error instead.
- In pandas the key and the amount columns become `float64` because the outer merge introduces NaN; the compare step casts both sides.
- `indicator=True` values are `both`, `left_only` (payments only) and `right_only` (orders only); I map them to the same status words. The meaning of left and right flips if you swap the frames.

**Then explain:**
- **Why the coalesced key:** in a FULL JOIN a row from only one side has NULLs for the other side's columns. `o.order_id` alone is NULL for both orphan payments, so order 9 is invisible (the "without COALESCE" block in my output); `p.order_id` alone is NULL for the unpaid order 3. `COALESCE(o.order_id, p.order_id)` gives one key column that is filled for every row.
- **pandas does the coalescing for you** when you merge `on="order_id"`: one key column holding the keys of both sides, with `indicator` as the status. With `left_on` and `right_on` you get two columns and must coalesce yourself.
- **Status logic:** test the primary key of each side for NULL (`o.order_id IS NULL`, `p.payment_id IS NULL`), not an amount, which can be legitimately NULL.
- **RIGHT JOIN** is a LEFT JOIN with the tables swapped; FULL is the union of both.

**Follow-ups:**
- *No FULL JOIN in the engine?* LEFT JOIN plus UNION ALL of the right-only rows (Q32, hedged for MySQL).
- *How do I check the amounts too?* Add `CASE WHEN p.amount <> o.amount` only inside the matched branch, and aggregate payments per order first.
- *Why not UNION of two anti-joins?* That loses the matched rows; you would add a third query.

**Common mistakes:**
- Selecting only `o.order_id` and losing the keys of orphan payments.
- Using `p.amount IS NULL` as the "no payment" test.
- Putting a filter on one side in WHERE, which turns the FULL JOIN into a narrower join (Q3).
- Reading `left_only` as "orders only" in pandas without checking which frame is on the left.

### Q17 ⭐⭐⭐ 🟡 Multiple joins and join order: orders(order_id, customer_id, product_id), customers(customer_id, name, city), products(product_id, name, category_id) and categories(category_id, category_name). Write the four-table join for order, customer name and category. Does join order change the result for INNER joins? For LEFT joins? Show how an INNER JOIN placed after a LEFT JOIN on a nullable path drops rows, and what the optimiser does about join order (concept only).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Start from orders and LEFT JOIN customers, products and categories in a chain; INNER joins can be listed in any order and give the same rows, but an INNER JOIN placed after a LEFT JOIN on a nullable path silently deletes the rows the LEFT JOIN kept.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, category_name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO categories VALUES (1,'Stationery'),(2,'Books');
INSERT INTO products VALUES (10,'Pen',1),(20,'Novel',2),(30,'Lamp',NULL),(40,'Desk',3);
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,2,30),(4,2,40),(5,NULL,10);
```

**SQL answer:** the four-table join keeping every order is `SQL_MAIN` (all LEFT); the all-INNER version is `SQL_INNER`.
```sql
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN customers c  ON c.customer_id = o.customer_id
LEFT JOIN products p   ON p.product_id = o.product_id
LEFT JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
```
```sql
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
JOIN customers c  ON c.customer_id = o.customer_id
JOIN products p   ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
```
The traps, also executed in the Code block:
```sql
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN products p ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
```
```sql
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN (products p JOIN categories cat ON cat.category_id = p.category_id)
       ON p.product_id = o.product_id
ORDER BY o.order_id
```

**pandas answer:** chain the merges, left from the fact table, each with `validate="many_to_one"` (each dimension key is unique).
```python
pd_df = (orders
         .merge(customers.rename(columns={"name": "customer"})[["customer_id", "customer"]],
                on="customer_id", how="left", validate="many_to_one")
         .merge(products.rename(columns={"name": "product"})[["product_id", "product", "category_id"]],
                on="product_id", how="left", validate="many_to_one")
         .merge(categories, on="category_id", how="left", validate="many_to_one")
         [["order_id", "customer", "product", "category_name"]]
         .sort_values("order_id").reset_index(drop=True))
pd_inner = (orders.merge(customers, on="customer_id", validate="many_to_one")
            .merge(products, on="product_id", suffixes=("_cust", "_prod"), validate="many_to_one")
            .merge(categories, on="category_id", validate="many_to_one"))
```

**Example:** orders 1 (Asha, Pen), 2 (Asha, Novel), 3 (Ben, Lamp), 4 (Ben, Desk), 5 (no customer, Pen). Pen is in category 1 and Novel in 2; Lamp has a NULL category_id; Desk points at category 3, which does not exist.
- All LEFT: 5 rows; category_name is NULL for orders 3 and 4, and customer is NULL for order 5.
- All INNER: only orders 1 and 2 survive (order 3: NULL category key, order 4: dangling key, order 5: no customer) = 2 rows.
- `orders LEFT JOIN products` then plain `JOIN categories`: 3 rows (orders 1, 2 and 5). Orders 3 and 4 are dropped, even though the first join kept them, because the NULL-extended category key can never equal a category_id. Order 5 survives because it has a product and a category; its missing customer is not in this query.
- Parenthesised form `orders LEFT JOIN (products JOIN categories ...)`: all 5 orders, but Lamp and Desk appear as NULL products, since the inner pair excluded them before the LEFT JOIN attached.

**Code:** run with `python3 -I`.
```python
# Q17: four-table join, join order, and an INNER JOIN after a LEFT JOIN on a nullable path
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, category_name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO categories VALUES (1,'Stationery'),(2,'Books');
INSERT INTO products VALUES (10,'Pen',1),(20,'Novel',2),(30,'Lamp',NULL),(40,'Desk',3);
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,2,30),(4,2,40),(5,NULL,10);
"""
SQL_MAIN = """
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN customers c  ON c.customer_id = o.customer_id
LEFT JOIN products p   ON p.product_id = o.product_id
LEFT JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
"""
SQL_INNER = """
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
JOIN customers c  ON c.customer_id = o.customer_id
JOIN products p   ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
"""
# same INNER joins written in a different textual order
SQL_INNER_REORDERED = """
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM categories cat
JOIN products p ON p.category_id = cat.category_id
JOIN orders o ON o.product_id = p.product_id
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_LEFT_THEN_INNER = """
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN products p ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
"""
SQL_NESTED = """
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN (products p JOIN categories cat ON cat.category_id = p.category_id)
       ON p.product_id = o.product_id
ORDER BY o.order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def show(title, q):
    d = pd.read_sql_query(q, con); print(title, f"({len(d)} rows)"); print(d.to_string(index=False)); print(); return d
left_df = show("All LEFT joins", SQL_MAIN)
inner_df = show("All INNER joins", SQL_INNER)
inner2 = show("Same INNER joins, tables listed in another order", SQL_INNER_REORDERED)
lti = show("LEFT products, then INNER categories", SQL_LEFT_THEN_INNER)
nested = show("LEFT JOIN (products JOIN categories), nested", SQL_NESTED)

customers = pd.read_sql_query("SELECT * FROM customers", con)
products = pd.read_sql_query("SELECT * FROM products", con)
categories = pd.read_sql_query("SELECT * FROM categories", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("pandas dtypes: orders.customer_id", orders["customer_id"].dtype, "| products.category_id", products["category_id"].dtype)

# pd:main
pd_df = (orders
         .merge(customers.rename(columns={"name": "customer"})[["customer_id", "customer"]],
                on="customer_id", how="left", validate="many_to_one")
         .merge(products.rename(columns={"name": "product"})[["product_id", "product", "category_id"]],
                on="product_id", how="left", validate="many_to_one")
         .merge(categories, on="category_id", how="left", validate="many_to_one")
         [["order_id", "customer", "product", "category_name"]]
         .sort_values("order_id").reset_index(drop=True))
pd_inner = (orders.merge(customers, on="customer_id", validate="many_to_one")
            .merge(products, on="product_id", suffixes=("_cust", "_prod"), validate="many_to_one")
            .merge(categories, on="category_id", validate="many_to_one"))
# pd:end
print("pandas all-left rows:", len(pd_df), "| pandas all-inner rows:", len(pd_inner))

def norm(d): return d.astype(object).where(d.notna(), "<NULL>").reset_index(drop=True)
# compared after sorting by order_id
pd.testing.assert_frame_equal(norm(left_df), norm(pd_df))
assert list(inner_df["order_id"]) == list(pd_inner.sort_values("order_id")["order_id"]) == [1, 2]
pd.testing.assert_frame_equal(inner_df.reset_index(drop=True), inner2.reset_index(drop=True))
assert len(lti) == 3 and len(nested) == 5
# pandas: LEFT then INNER drops rows; inner first (the nested form) keeps all orders
lp = orders.merge(products, on="product_id", how="left").merge(categories, on="category_id")
pc = products.merge(categories, on="category_id")[["product_id", "name", "category_name"]]
np_ = orders.merge(pc, on="product_id", how="left").sort_values("order_id")
print("pandas LEFT then INNER rows:", len(lp), "| nested (inner first, then LEFT) rows:", len(np_))
assert len(lp) == 3 and len(np_) == 5
print("asserts passed: SQL == pandas; INNER join order does not change the result")
```

**Output (my run):**
```text
All LEFT joins (5 rows)
 order_id customer product category_name
        1     Asha     Pen    Stationery
        2     Asha   Novel         Books
        3      Ben    Lamp           NaN
        4      Ben    Desk           NaN
        5      NaN     Pen    Stationery

All INNER joins (2 rows)
 order_id customer product category_name
        1     Asha     Pen    Stationery
        2     Asha   Novel         Books

Same INNER joins, tables listed in another order (2 rows)
 order_id customer product category_name
        1     Asha     Pen    Stationery
        2     Asha   Novel         Books

LEFT products, then INNER categories (3 rows)
 order_id product category_name
        1     Pen    Stationery
        2   Novel         Books
        5     Pen    Stationery

LEFT JOIN (products JOIN categories), nested (5 rows)
 order_id product category_name
        1     Pen    Stationery
        2   Novel         Books
        3     NaN           NaN
        4     NaN           NaN
        5     Pen    Stationery

pandas dtypes: orders.customer_id float64 | products.category_id float64
pandas all-left rows: 5 | pandas all-inner rows: 2
pandas LEFT then INNER rows: 3 | nested (inner first, then LEFT) rows: 5
asserts passed: SQL == pandas; INNER join order does not change the result
```

**Edge cases:**
- A NULL foreign key (Lamp's category, order 5's customer) and a dangling foreign key (Desk's category 3) both give a NULL on the LEFT JOIN side; only a foreign key constraint would stop the dangling one.
- Duplicate keys in a dimension would multiply orders; each pandas merge uses `validate="many_to_one"` for that reason.
- Name clashes (customers.name, products.name): alias the columns, or in pandas rename or pass `suffixes`.
- In pandas the NULL foreign keys make `customer_id` and `category_id` `float64` after `read_sql`, and merging them with `int64` keys worked in my run.

**Then explain:**
- **INNER joins:** associative and commutative, so the order you write them in does not change the result. I proved it by listing the tables in another order (same 2 rows), and the optimiser is free to pick its own order for cost reasons.
- **LEFT joins:** not freely reorderable. `A LEFT JOIN B` is not the same as `B LEFT JOIN A`, and moving an inner join across an outer join can change the rows (the 3-row versus 5-row result above is the same tables joined in a different nesting).
- **Rule:** once a LEFT JOIN has been used on a path, keep every later join on that path LEFT, or you lose the rows it was there to keep. A WHERE condition on the right-hand table has the same effect (Q3).
- **Optimiser (concept only, not executed here):** for INNER joins it can reorder tables by estimated cost; for outer joins it reorders only when the result is provably identical. Plans are Part 11.

**Follow-ups:**
- *When do you want INNER after LEFT?* When you really want to filter to orders with a category; then say so in a WHERE or use INNER for that reason.
- *Does the written order matter for speed?* Usually not for INNER joins; engines differ (hedged), and SQLite documents some cases where CROSS JOIN fixes the order (from memory).
- *Several dimensions off one fact table?* A star join: LEFT JOIN each dimension to the fact table.

**Common mistakes:**
- Mixing LEFT and INNER joins at random and losing rows without noticing.
- Joining categories through `orders` instead of through `products`.
- Using `SELECT *` over four tables with repeated column names.
- Not comparing the row count with `COUNT(*)` from `orders`.

### Q18 ⭐⭐⭐ 🟡 Join to an aggregated derived table: orders(order_id, customer_id, amount) and customers(customer_id, name, city). Return customers whose total spend is above the average total spend of customers in their own city. Build the per-customer totals as a derived table in FROM, join it to a per-city average derived table, and explain the grain of each side. Give pandas groupby, transform or merge. (No window functions or CTEs.)
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build a per-customer totals derived table, build a per-city average of those totals from it as a second derived table, join the two on city, and keep customers whose total is strictly above their city's average; the averages must be over customers, not over order rows.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Pune'),(3,'Chitra','Pune'),(4,'Dev','Delhi'),
                             (5,'Esha','Delhi'),(6,'Farah','Mumbai'),(7,'Gopal','Pune');
INSERT INTO orders VALUES (1,1,60),(2,1,40),(3,2,300),(4,3,200),(5,4,50),(6,5,150),(7,6,70);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT t.customer_id, t.name, t.city, t.total_spend, a.city_avg
FROM (SELECT c.customer_id, c.name, c.city, SUM(o.amount) AS total_spend
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT city, AVG(total_spend) AS city_avg
      FROM (SELECT c.customer_id, c.city, SUM(o.amount) AS total_spend
            FROM customers c JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.city) x
      GROUP BY city) a ON a.city = t.city
WHERE t.total_spend > a.city_avg
ORDER BY t.customer_id
```
Grain: `t` has one row per customer (customer total), `a` has one row per city (average of those totals), so the join `a.city = t.city` is many-to-one and adds no rows. The two variants (`SQL_ZERO`, `SQL_WRONG`) are also in the Code block.

**pandas answer:** (also in the Code block; the `transform` alternative is checked there too)
```python
totals = (customers.merge(orders, on="customer_id")
          .groupby(["customer_id", "name", "city"], as_index=False).agg(total_spend=("amount", "sum")))
city_avg = totals.groupby("city", as_index=False).agg(city_avg=("total_spend", "mean"))
joined = totals.merge(city_avg, on="city", validate="many_to_one")
pd_df = (joined[joined["total_spend"] > joined["city_avg"]]
         .sort_values("customer_id").reset_index(drop=True))
```

**Example:** Pune: Asha 60+40 = 100, Ben 300, Chitra 200 (Gopal has no orders). Delhi: Dev 50, Esha 150. Mumbai: Farah 70.
- Pune average of totals = (100 + 300 + 200) / 3 = 200. Ben 300 > 200 yes; Chitra 200 is not strictly above 200; Asha no.
- Delhi average = (50 + 150) / 2 = 100: Esha 150 yes. Mumbai average = 70: Farah is equal, not above.
- Result: Ben and Esha.

**Code:** run with `python3 -I`.
```python
# Q18: customers whose total spend beats the average customer total in their own city (derived tables, no windows/CTEs)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Pune'),(3,'Chitra','Pune'),(4,'Dev','Delhi'),
                             (5,'Esha','Delhi'),(6,'Farah','Mumbai'),(7,'Gopal','Pune');
INSERT INTO orders VALUES (1,1,60),(2,1,40),(3,2,300),(4,3,200),(5,4,50),(6,5,150),(7,6,70);
"""
SQL_MAIN = """
SELECT t.customer_id, t.name, t.city, t.total_spend, a.city_avg
FROM (SELECT c.customer_id, c.name, c.city, SUM(o.amount) AS total_spend
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT city, AVG(total_spend) AS city_avg
      FROM (SELECT c.customer_id, c.city, SUM(o.amount) AS total_spend
            FROM customers c JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.city) x
      GROUP BY city) a ON a.city = t.city
WHERE t.total_spend > a.city_avg
ORDER BY t.customer_id
"""
# variant: customers with no orders count as 0 in their city's average
SQL_ZERO = """
SELECT t.customer_id, t.name, t.total_spend, a.city_avg
FROM (SELECT c.customer_id, c.name, c.city, COALESCE(SUM(o.amount), 0) AS total_spend
      FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT city, AVG(total_spend) AS city_avg
      FROM (SELECT c.customer_id, c.city, COALESCE(SUM(o.amount), 0) AS total_spend
            FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.city) x
      GROUP BY city) a ON a.city = t.city
WHERE t.total_spend > a.city_avg
ORDER BY t.customer_id
"""
# wrong: average over ORDER rows per city, not over customer totals
SQL_WRONG = """
SELECT t.customer_id, t.name, t.total_spend, a.avg_order
FROM (SELECT c.customer_id, c.name, c.city, SUM(o.amount) AS total_spend
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT c.city, AVG(o.amount) AS avg_order
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id GROUP BY c.city) a ON a.city = t.city
WHERE t.total_spend > a.avg_order ORDER BY t.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main (customers with orders only):"); print(sql_df.to_string(index=False))
print("\nSQL variant, zero-order customers counted as 0:"); print(pd.read_sql_query(SQL_ZERO, con).to_string(index=False))
print("\nWRONG (average over order rows):"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
totals = (customers.merge(orders, on="customer_id")
          .groupby(["customer_id", "name", "city"], as_index=False).agg(total_spend=("amount", "sum")))
city_avg = totals.groupby("city", as_index=False).agg(city_avg=("total_spend", "mean"))
joined = totals.merge(city_avg, on="city", validate="many_to_one")
pd_df = (joined[joined["total_spend"] > joined["city_avg"]]
         .sort_values("customer_id").reset_index(drop=True))
# pd:end
print("\npandas merge version:"); print(pd_df.to_string(index=False))

# transform alternative: no second frame
totals["city_avg"] = totals.groupby("city")["total_spend"].transform("mean")
alt = totals[totals["total_spend"] > totals["city_avg"]].sort_values("customer_id").reset_index(drop=True)
# compared after sorting by customer_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(pd_df, alt, check_dtype=False)
assert list(sql_df["name"]) == ["Ben", "Esha"]
print("\nasserts passed: SQL == pandas merge == pandas transform")
```

**Output (my run):**
```text
SQL main (customers with orders only):
 customer_id name  city  total_spend  city_avg
           2  Ben  Pune          300     200.0
           5 Esha Delhi          150     100.0

SQL variant, zero-order customers counted as 0:
 customer_id   name  total_spend  city_avg
           2    Ben          300     150.0
           3 Chitra          200     150.0
           5   Esha          150     100.0

WRONG (average over order rows):
 customer_id   name  total_spend  avg_order
           2    Ben          300      150.0
           3 Chitra          200      150.0
           5   Esha          150      100.0

pandas merge version:
 customer_id name  city  total_spend  city_avg
           2  Ben  Pune          300     200.0
           5 Esha Delhi          150     100.0

asserts passed: SQL == pandas merge == pandas transform
```

**Edge cases:**
- Customers without orders: my main query counts only customers who ordered, because the totals come from an inner join. If they should count as 0 spend, use LEFT JOIN with `COALESCE`. That changes the answer: with Gopal (Pune, no orders) as 0 the Pune average drops to (100+300+200+0)/4 = 150, so Chitra now qualifies (`SQL_ZERO`, in my output). The question text does not say which one is wanted, so say your choice.
- A city with a single customer: the total equals the average, so nobody qualifies.
- Ties with the average are excluded because of `>`; all totals equal means no rows.
- NULL city: `a.city = t.city` never matches NULL, so these customers drop out; handle explicitly if it matters.
- NULL order amounts are ignored by SUM and AVG.

**Then explain:**
- **Grain of each side:** the first derived table is one row per customer; the second is one row per city. Joining a per-customer table to a per-city table on city fans out per customer (many-to-one), not per order.
- **The classic mistake:** averaging order amounts per city, `AVG(o.amount)`, is the average order, not the average customer spend. In my data that wrongly gives Pune 150 and lets Chitra in (`SQL_WRONG`, in my output). Average the customer totals.
- **Why no window function:** the question rules out windows and CTEs; `AVG(SUM(...)) OVER (PARTITION BY city)` is the later-part solution.
- **pandas:** `groupby` gives the per-customer totals, a second `groupby` the per-city mean, and `merge` (or `groupby(...).transform("mean")`) puts the average on each customer row.

**Follow-ups:**
- *What if the comparison should exclude the customer's own spend?* The average of the other customers needs a different computation (sum minus own, divided by count minus one).
- *Median instead of average?* Not a plain aggregate in SQLite; Part 3 onward.
- *Why not a correlated subquery?* It works but recomputes the city average per row (not run here).

**Common mistakes:**
- Averaging raw order rows per city.
- Joining orders directly to customers and comparing without grouping first, so a customer is compared once per order.
- Using `>=` and counting customers exactly at the average.
- Silently dropping customers without orders without saying so.

### Q19 ⭐⭐ 🟢 Joining on multiple columns: sales(store_id, product_id, qty) and prices(store_id, product_id, price), where price varies by store. Write the join on the composite key and show what goes wrong if you join on product_id alone (fan-out across stores, wrong revenue). Give the pandas merge on=['store_id','product_id'] and validate='many_to_one'.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join on every column that makes up the key, `ON p.store_id = s.store_id AND p.product_id = s.product_id`; joining on product_id alone matches each sale to the price of every store, so rows and revenue are multiplied.

**Schema and sample data:**
```sql
CREATE TABLE sales(store_id INTEGER, product_id INTEGER, qty INTEGER);
CREATE TABLE prices(store_id INTEGER, product_id INTEGER, price INTEGER, PRIMARY KEY(store_id, product_id));
INSERT INTO sales VALUES (1,10,3),(1,20,2),(2,10,5),(2,20,1),(3,10,2);
INSERT INTO prices VALUES (1,10,100),(1,20,50),(2,10,110),(2,20,55);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT s.store_id, s.product_id, s.qty, p.price, s.qty * p.price AS revenue
FROM sales s
JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id
ORDER BY s.store_id, s.product_id
```
The broken version (`SQL_WRONG`) joins on `product_id` only and is run in the Code block.

**pandas answer:**
```python
pd_df = sales.merge(prices, on=["store_id", "product_id"], how="inner", validate="many_to_one")
pd_df["revenue"] = pd_df["qty"] * pd_df["price"]
pd_df = pd_df.sort_values(["store_id", "product_id"]).reset_index(drop=True)
```

**Example:** prices: store 1 sells product 10 at 100 and product 20 at 50; store 2 sells 10 at 110 and 20 at 55. Sales: (1,10,3), (1,20,2), (2,10,5), (2,20,1), and (3,10,2) at a store with no price list.
- Correct: 3x100 + 2x50 + 5x110 + 1x55 = 300 + 100 + 550 + 55 = 1005. The store 3 sale has no price row, so an INNER JOIN drops it (a LEFT JOIN would show a NULL price).
- Product-only join: product 10 has 3 sales rows, each matched to 2 prices = 6 rows; product 20 has 2 sales rows x 2 prices = 4 rows. 10 rows, and revenue = 10 units x (100+110) + 3 units x (50+55) = 2100 + 315 = 2415, more than double the right answer.

**Code:** run with `python3 -I`.
```python
# Q19: joining on a composite key (store_id, product_id); what a product_id-only join does
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(store_id INTEGER, product_id INTEGER, qty INTEGER);
CREATE TABLE prices(store_id INTEGER, product_id INTEGER, price INTEGER, PRIMARY KEY(store_id, product_id));
INSERT INTO sales VALUES (1,10,3),(1,20,2),(2,10,5),(2,20,1),(3,10,2);
INSERT INTO prices VALUES (1,10,100),(1,20,50),(2,10,110),(2,20,55);
"""
SQL_MAIN = """
SELECT s.store_id, s.product_id, s.qty, p.price, s.qty * p.price AS revenue
FROM sales s
JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id
ORDER BY s.store_id, s.product_id
"""
SQL_WRONG = """
SELECT COUNT(*) AS joined_rows, SUM(s.qty * p.price) AS revenue
FROM sales s JOIN prices p ON p.product_id = s.product_id
"""
SQL_RIGHT_TOTAL = "SELECT SUM(s.qty * p.price) FROM sales s JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id"
SQL_LEFT = """
SELECT s.store_id, s.product_id, s.qty, p.price FROM sales s
LEFT JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id
WHERE p.price IS NULL
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\ncorrect revenue:", con.execute(SQL_RIGHT_TOTAL).fetchone()[0])
print("product_id-only join (joined_rows, revenue):", con.execute(SQL_WRONG).fetchone())
print("sales rows with no price for their store:", con.execute(SQL_LEFT).fetchall())

sales = pd.read_sql_query("SELECT * FROM sales", con)
prices = pd.read_sql_query("SELECT * FROM prices", con)
# pd:main
pd_df = sales.merge(prices, on=["store_id", "product_id"], how="inner", validate="many_to_one")
pd_df["revenue"] = pd_df["qty"] * pd_df["price"]
pd_df = pd_df.sort_values(["store_id", "product_id"]).reset_index(drop=True)
# pd:end
print("\npandas revenue:", pd_df["revenue"].sum())
bad = sales.merge(prices, on="product_id", suffixes=("_sale", "_price"))
print("pandas product_id-only merge rows:", len(bad), "revenue:", (bad["qty"] * bad["price"]).sum())
try:
    sales.merge(prices, on="product_id", validate="many_to_one")
except Exception as e:
    print("validate on product_id alone ->", type(e).__name__ + ":", e)
left = sales.merge(prices, on=["store_id", "product_id"], how="left", indicator=True)
print("unmatched sales (indicator left_only):", left.loc[left["_merge"] == "left_only", ["store_id", "product_id"]].values.tolist())

# compared after sorting by store_id, product_id
pd.testing.assert_frame_equal(sql_df, pd_df[sql_df.columns], check_dtype=False)
assert pd_df["revenue"].sum() == 1005
print("asserts passed: SQL == pandas")
```

**Output (my run):**
```text
 store_id  product_id  qty  price  revenue
        1          10    3    100      300
        1          20    2     50      100
        2          10    5    110      550
        2          20    1     55       55

correct revenue: 1005
product_id-only join (joined_rows, revenue): (10, 2415)
sales rows with no price for their store: [(3, 10, 2, None)]

pandas revenue: 1005
pandas product_id-only merge rows: 10 revenue: 2415
validate on product_id alone -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  product_id
         10
         20 ...
unmatched sales (indicator left_only): [[3, 10]]
asserts passed: SQL == pandas
```

**Edge cases:**
- A sale for a store with no price (store 3): INNER drops it, LEFT keeps it with a NULL price, and `qty * price` becomes NULL and is ignored by SUM. Find these with `WHERE p.price IS NULL` (SQL) or `indicator=True` (pandas) rather than letting revenue quietly shrink.
- A NULL in either key column never matches (NULL is not equal to anything).
- If `prices` had two rows for the same store and product, even the composite join would fan out; a PRIMARY KEY on (store_id, product_id) prevents it, and `validate="many_to_one"` checks it in pandas.
- Column order in a composite key does not matter, but the pair must be complete.

**Then explain:**
- **Composite key:** the unit of uniqueness in `prices` is the pair (store, product), so the join must use the pair. product_id alone is not unique in `prices`.
- **What goes wrong:** the join silently returns the cartesian product of sales and prices per product (10 rows instead of 5, matches 2 prices per sale); nothing errors.
- **pandas:** `on=["store_id", "product_id"]` with `validate="many_to_one"`. When I merged on `product_id` alone with `validate="many_to_one"`, pandas raised `MergeError: Merge keys are not unique in right dataset; not a many-to-one merge` (exact text in the output). Without `validate` it silently returned 10 rows and revenue 2415, the same wrong numbers as SQL.
- **Habit:** compare the row count after the join with the row count of the left table.

**Follow-ups:**
- *Why many_to_one and not one_to_one?* Many sales rows can share one store-product price; the price side must be unique.
- *Composite key with a date range?* That is a range join, covered later in this part (Q26).
- *Would an index help?* A composite index on both key columns, concept only (Part 11).

**Common mistakes:**
- Joining on the "obvious" single column because the other column name seems redundant.
- Never comparing the joined row count with the left table.
- Counting revenue after a fan-out join without checking the total.
- Dropping store 3 sales silently through an INNER JOIN.

### Q20 ⭐⭐ 🟢 USING versus ON: employees(emp_id, name, dept_id) and departments(dept_id, dept_name). Show both forms, what SELECT * returns for each (one dept_id column versus two), how USING behaves in outer joins and with qualified column names (hedge by engine: PostgreSQL, MySQL and SQLite differ in details), when ON is required (different column names, extra conditions), and the pandas parallels (on versus left_on/right_on).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `USING (dept_id)` is shorthand for an equality join on a column that has the same name in both tables and returns that column once; `ON` is the general form that works with any condition, different names and extra predicates, and `SELECT *` returns the key twice.

**Schema and sample data:**
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO departments VALUES (10,'Sales'),(20,'Tech'),(30,'HR');
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',99),(4,'Dev',NULL);
```

**SQL answer:** both forms, executed in the Code block (the queries are in its `Q` dictionary):
```sql
SELECT * FROM employees e JOIN departments d ON e.dept_id = d.dept_id ORDER BY emp_id;
SELECT * FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id;
```
The other `Q` entries cover LEFT, RIGHT and FULL joins with USING, FULL with ON, and qualified or unqualified names.

**pandas answer:**
```python
p_on = employees.merge(departments, on="dept_id", how="left")                                   # like USING: one key column
p_lr = employees.merge(departments, left_on="dept_id", right_on="dept_id", how="left")           # same, spelled with left_on/right_on
d2 = departments.rename(columns={"dept_id": "id"})
p_names = employees.merge(d2, left_on="dept_id", right_on="id", how="left")                      # like ON with different names: two key columns
```

**Example:** employees Asha (10), Ben (20), Chitra (99, no such department), Dev (NULL); departments 10 Sales, 20 Tech, 30 HR.
- Inner join with ON, `SELECT *`: Asha and Ben, 5 columns: emp_id, name, dept_id, dept_id, dept_name (the key appears twice). With USING: the same two rows and 4 columns, one dept_id.
- LEFT JOIN USING: also Chitra and Dev with a NULL dept_name. RIGHT JOIN USING: Asha, Ben and the HR department (no employees).
- FULL JOIN: with USING, the HR row has dept_id 30 filled in (SQLite coalesces the key); with ON the same row has two columns, `e.dept_id` NULL and `d.dept_id` 30. Chitra (99) and Dev (NULL) are in both.

**Code:** run with `python3 -I`.
```python
# Q20: USING versus ON
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO departments VALUES (10,'Sales'),(20,'Tech'),(30,'HR');
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',99),(4,'Dev',NULL);
"""
Q = {
 "on_star":    "SELECT * FROM employees e JOIN departments d ON e.dept_id = d.dept_id ORDER BY emp_id",
 "using_star": "SELECT * FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id",
 "left_using": "SELECT * FROM employees e LEFT JOIN departments d USING (dept_id) ORDER BY emp_id",
 "right_using": "SELECT * FROM employees e RIGHT JOIN departments d USING (dept_id) ORDER BY dept_id, emp_id",
 "full_using": "SELECT * FROM employees e FULL JOIN departments d USING (dept_id) ORDER BY dept_id, emp_id",
 "full_on":    "SELECT * FROM employees e FULL JOIN departments d ON e.dept_id = d.dept_id ORDER BY d.dept_id, emp_id",
 "using_qualified": "SELECT e.dept_id, d.dept_id AS d_dept, emp_id FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id",
 "using_unqualified": "SELECT dept_id, name, dept_name FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id",
}
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for k, q in Q.items():
    cur = con.execute(q)
    cols = [c[0] for c in cur.description]
    res[k] = (cols, cur.fetchall())
    print(f"{k}: columns {cols}")
    for r in res[k][1]: print("   ", r)
# the ON form returns two dept_id columns, the USING form one
assert res["on_star"][0].count("dept_id") == 2 and res["using_star"][0].count("dept_id") == 1

employees = pd.read_sql_query("SELECT * FROM employees", con)
departments = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
p_on = employees.merge(departments, on="dept_id", how="left")                                   # like USING: one key column
p_lr = employees.merge(departments, left_on="dept_id", right_on="dept_id", how="left")           # same, spelled with left_on/right_on
d2 = departments.rename(columns={"dept_id": "id"})
p_names = employees.merge(d2, left_on="dept_id", right_on="id", how="left")                      # like ON with different names: two key columns
# pd:end
print("\npandas on='dept_id' columns:", list(p_on.columns))
print("pandas left_on/right_on, different names:", list(p_names.columns))
print("pandas on= with how='outer':")
print(employees.merge(departments, on="dept_id", how="outer").sort_values(["dept_id", "emp_id"]).to_string(index=False))

# USING result (LEFT) equals pandas on= result, compared after sorting by emp_id and reordering columns by name
sql_left = pd.DataFrame(res["left_using"][1], columns=res["left_using"][0])
cols = ["emp_id", "name", "dept_id", "dept_name"]
a = sql_left[cols].sort_values("emp_id").reset_index(drop=True)
b = p_on[cols].sort_values("emp_id").reset_index(drop=True)
pd.testing.assert_frame_equal(a.astype(object).where(a.notna(), None), b.astype(object).where(b.notna(), None), check_dtype=False)
pd.testing.assert_frame_equal(p_on, p_lr)
print("\nasserts passed: SQL LEFT JOIN USING == pandas merge on=; on= == left_on/right_on with the same name")
```

**Output (my run):**
```text
on_star: columns ['emp_id', 'name', 'dept_id', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 10, 'Sales')
    (2, 'Ben', 20, 20, 'Tech')
using_star: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
left_using: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (3, 'Chitra', 99, None)
    (4, 'Dev', None, None)
right_using: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (None, None, 30, 'HR')
full_using: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (4, 'Dev', None, None)
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (None, None, 30, 'HR')
    (3, 'Chitra', 99, None)
full_on: columns ['emp_id', 'name', 'dept_id', 'dept_id', 'dept_name']
    (3, 'Chitra', 99, None, None)
    (4, 'Dev', None, None, None)
    (1, 'Asha', 10, 10, 'Sales')
    (2, 'Ben', 20, 20, 'Tech')
    (None, None, None, 30, 'HR')
using_qualified: columns ['dept_id', 'd_dept', 'emp_id']
    (10, 10, 1)
    (20, 20, 2)
using_unqualified: columns ['dept_id', 'name', 'dept_name']
    (10, 'Asha', 'Sales')
    (20, 'Ben', 'Tech')

pandas on='dept_id' columns: ['emp_id', 'name', 'dept_id', 'dept_name']
pandas left_on/right_on, different names: ['emp_id', 'name', 'dept_id', 'id', 'dept_name']
pandas on= with how='outer':
 emp_id   name  dept_id dept_name
    1.0   Asha     10.0     Sales
    2.0    Ben     20.0      Tech
    NaN    NaN     30.0        HR
    3.0 Chitra     99.0       NaN
    4.0    Dev      NaN       NaN

asserts passed: SQL LEFT JOIN USING == pandas merge on=; on= == left_on/right_on with the same name
```

**Edge cases:**
- Qualified names: in my SQLite run `e.dept_id` and `d.dept_id` were both accepted after `USING`, and the unqualified `dept_id` worked too. This is engine specific: from memory PostgreSQL and MySQL accept the unqualified name, and some engines (older Oracle) reject a qualified name for a USING column; not executed here, check the manual.
- Column order of `SELECT *`: SQLite kept `dept_id` in the left table's position (emp_id, name, dept_id, dept_name). The SQL standard and, I recall, the MySQL and PostgreSQL documentation put the join columns first; not executed here, so do not rely on the order, name your columns.
- Different column names (`departments.id`), extra conditions (`AND d.active = 1`), non-equality joins and expressions need `ON`.
- NULL keys do not match in either form (Dev stays unmatched).
- USING with more than one column is allowed: `USING (store_id, product_id)`.

**Then explain:**
- **One column versus two:** `SELECT *` with USING returns the join column once; with ON it returns both copies. After an outer join the single USING column holds the key from whichever side has it, which is the coalesced key from Q16 for free (seen in my FULL JOIN USING output).
- **When ON is required:** different names, more than an equality, or a condition that is not just equality of same-named columns.
- **Risk of USING:** it depends on names, so renaming a column or adding a second same-named column changes behaviour less than NATURAL JOIN (Q21) but still ties the query to naming conventions.
- **pandas parallels:** `on="dept_id"` is USING (one key column in the result); `left_on`/`right_on` with different names is ON and keeps both key columns (`dept_id` and `id` in my run). With the same name in `left_on` and `right_on` the result equals `on=` (my assert).
- **Outer merge in pandas:** `on=` with `how="outer"` gives one key column holding the keys of both sides, like USING.

**Follow-ups:**
- *Is USING faster?* No; it is syntax (not executed on other engines, concept only).
- *Which one do you write at work?* ON for clarity and safety, USING only for conventional shared key names.
- *What does NATURAL JOIN do?* USING over every common column (Q21).

**Common mistakes:**
- Assuming `SELECT *` shows one key column in an ON join.
- Qualifying the USING column in an engine that rejects it.
- Using USING when the key names differ or when extra conditions are needed.
- Expecting `merge(on=...)` to keep two key columns.

### Q21 ⭐⭐ 🟢 NATURAL JOIN and why many teams ban it: employees(emp_id, name, dept_id, updated_at) and departments(dept_id, dept_name, updated_at). Explain what NATURAL JOIN joins on, how an extra common column (updated_at) silently changes the result to zero rows, and what happens after a schema change adds a column. Contrast with explicit ON.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** NATURAL JOIN joins on every column name the two tables share, with no say from you, so an extra shared column like `updated_at` becomes part of the key and the result quietly shrinks (often to zero rows), and a later schema change can change it again; write an explicit ON.

**Schema and sample data:**
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT, updated_at TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, updated_at TEXT);
INSERT INTO departments VALUES (10,'Sales','2026-01-05'),(20,'Tech','2026-01-06');
INSERT INTO employees VALUES (1,'Asha',10,'2026-03-01'),(2,'Ben',20,'2026-03-02'),(3,'Chitra',20,'2026-01-06');
```

**SQL answer:** both queries run in the Code block.
```sql
SELECT * FROM employees NATURAL JOIN departments ORDER BY emp_id
```
```sql
SELECT e.emp_id, e.name, e.dept_id, d.dept_name
FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id
```

**pandas answer:** `merge` with no `on=` is a natural join too; the explicit version names the key.
```python
p_default = employees.merge(departments)                                           # no on=: joins on ALL common columns
p_explicit = employees.merge(departments[["dept_id", "dept_name"]], on="dept_id", validate="many_to_one")
```

**Example:** employees Asha (dept 10, updated 2026-03-01), Ben (20, 2026-03-02), Chitra (20, 2026-01-06); departments 10 Sales (2026-01-05), 20 Tech (2026-01-06).
- Common columns: `dept_id` and `updated_at`. NATURAL JOIN therefore means `dept_id` equal AND `updated_at` equal.
- Asha: dept 10 matches, but 2026-03-01 differs from 2026-01-05, so no row. Ben: 2026-03-02 differs from 2026-01-06, no row. Chitra: dept 20 and 2026-01-06 equal, so she matches.
- Result: 1 row (Chitra), while the explicit ON on dept_id alone gives 3. In practice timestamps rarely match at all, which gives zero rows; my sample has one coincidence on purpose, to show the wrong answer can look plausible.
- Schema change: after adding a `name` column to departments (it also exists in employees), the NATURAL JOIN returned 0 rows, while the ON query still returned 3.

**Code:** run with `python3 -I`.
```python
# Q21: NATURAL JOIN joins on every same-named column; updated_at silently breaks it
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT, updated_at TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, updated_at TEXT);
INSERT INTO departments VALUES (10,'Sales','2026-01-05'),(20,'Tech','2026-01-06');
INSERT INTO employees VALUES (1,'Asha',10,'2026-03-01'),(2,'Ben',20,'2026-03-02'),(3,'Chitra',20,'2026-01-06');
"""
SQL_NATURAL = "SELECT * FROM employees NATURAL JOIN departments ORDER BY emp_id"
SQL_ON = """
SELECT e.emp_id, e.name, e.dept_id, d.dept_name
FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def run(q):
    cur = con.execute(q); return [c[0] for c in cur.description], cur.fetchall()
cols, rows = run(SQL_NATURAL)
print("NATURAL JOIN columns:", cols); print("rows:", rows)
cols, rows = run(SQL_ON)
print("\nexplicit ON rows:", len(rows)); [print("   ", r) for r in rows]

# a schema change adds a second common column (name) to departments
con.execute("ALTER TABLE departments ADD COLUMN name TEXT")
con.execute("UPDATE departments SET name = 'HQ'")
print("\nafter ALTER TABLE departments ADD COLUMN name -> NATURAL JOIN rows:", len(run(SQL_NATURAL)[1]))
print("explicit ON rows after the same change:", len(run(SQL_ON)[1]))
con.execute("ALTER TABLE departments DROP COLUMN name")

# no common column at all: NATURAL JOIN turns into a cross join
con.executescript("CREATE TABLE tags(tag TEXT); INSERT INTO tags VALUES ('x'),('y');")
print("\nemployees NATURAL JOIN tags (no common column) rows:", len(run("SELECT * FROM employees NATURAL JOIN tags")[1]), "= 3 x 2")

employees = pd.read_sql_query("SELECT * FROM employees", con)
departments = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
p_default = employees.merge(departments)                                           # no on=: joins on ALL common columns
p_explicit = employees.merge(departments[["dept_id", "dept_name"]], on="dept_id", validate="many_to_one")
# pd:end
print("\npandas merge() with no on= uses common columns:", sorted(set(employees.columns) & set(departments.columns)))
print("pandas default merge rows:", len(p_default), "| explicit on='dept_id' rows:", len(p_explicit))
try:
    employees[["emp_id", "name"]].merge(pd.DataFrame({"tag": ["x", "y"]}))
except Exception as e:
    print("no common columns ->", type(e).__name__ + ":", e)

# SQL: natural -> 1 row (only Chitra, whose updated_at matches); explicit ON -> 3 rows
nat_rows = run(SQL_NATURAL)[1]
assert len(nat_rows) == 1 and nat_rows[0][1] == "Chitra"
assert len(run(SQL_ON)[1]) == 3
# the pandas default merge behaves like NATURAL JOIN (same single row); compared after sorting by emp_id
assert p_default["name"].tolist() == [r[1] for r in nat_rows]
sql_on = pd.DataFrame(run(SQL_ON)[1], columns=run(SQL_ON)[0])
pd.testing.assert_frame_equal(sql_on, p_explicit.sort_values("emp_id").reset_index(drop=True)[sql_on.columns], check_dtype=False)
print("asserts passed: NATURAL JOIN == pandas default merge (1 row); explicit ON == pandas on='dept_id' (3 rows)")
```

**Output (my run):**
```text
NATURAL JOIN columns: ['emp_id', 'name', 'dept_id', 'updated_at', 'dept_name']
rows: [(3, 'Chitra', 20, '2026-01-06', 'Tech')]

explicit ON rows: 3
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (3, 'Chitra', 20, 'Tech')

after ALTER TABLE departments ADD COLUMN name -> NATURAL JOIN rows: 0
explicit ON rows after the same change: 3

employees NATURAL JOIN tags (no common column) rows: 6 = 3 x 2

pandas merge() with no on= uses common columns: ['dept_id', 'updated_at']
pandas default merge rows: 1 | explicit on='dept_id' rows: 3
no common columns -> MergeError: No common columns to perform merge on. Merge options: left_on=None, right_on=None, left_index=False, right_index=False
asserts passed: NATURAL JOIN == pandas default merge (1 row); explicit ON == pandas on='dept_id' (3 rows)
```

**Edge cases:**
- Two tables with no common column: NATURAL JOIN becomes a cross join (3 x 2 = 6 rows in my run).
- Columns that are common by accident (`updated_at`, `created_at`, `id`, `name`, `status`) are the usual cause.
- Dropping a column can also widen the result or turn a join into a cross join.
- `SELECT *` with NATURAL JOIN shows each common column once (`dept_id` and `updated_at` once in my output).
- NULL values in the common columns never match, as with any equality.

**Then explain:**
- **What it does:** joins on all same-named columns, as if you wrote USING on all of them.
- **Why teams ban it:** the join key is implicit and can change when someone adds a column to either table, with no error and no warning; code review cannot see the join condition.
- **pandas has the same trap:** `employees.merge(departments)` with no `on=` joins on the intersection of column names (`dept_id`, `updated_at`) and returned the same single row (my run). With no common column at all, pandas raises `MergeError: No common columns to perform merge on` rather than making a cross join.
- **Support (not executed here):** from memory PostgreSQL, MySQL and Oracle support NATURAL JOIN and SQL Server does not; check the manual.
- **Fix:** an explicit ON on the key you mean, and rename audit columns (`emp_updated_at`) to avoid clashes.

**Follow-ups:**
- *Is NATURAL JOIN ever fine?* In a one-off exploration of tables whose columns you know, but not in saved code.
- *What about USING?* Safer than NATURAL, because you name the columns (Q20).
- *Natural outer joins?* `NATURAL LEFT JOIN` exists with the same implicit key.

**Common mistakes:**
- Not noticing that `updated_at` or `id` is a shared column.
- Reading a plausible-looking one-row result as correct.
- Calling `merge` in pandas without `on=` and trusting the guess.
- Renaming or adding a column without searching for NATURAL JOIN users.

### Q22 ⭐⭐ 🟢 One-level hierarchy: employees(emp_id, name, manager_id). List each employee with the manager's name (the top person shows NULL, so use LEFT JOIN), and then managers with at least 5 direct reports (self join plus GROUP BY ... HAVING, the LeetCode Managers with at Least 5 Direct Reports idea). Explain why an INNER JOIN drops the top person and why multi-level chains need recursion (Part 9). Give pandas.
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Self join employees to itself with `e.manager_id = m.emp_id`, using a LEFT JOIN so the top person (NULL manager) still shows up; for managers with at least 5 reports, join, group by the manager and use HAVING COUNT(*) >= 5.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'Zara',NULL),(2,'Ben',1),(3,'Chitra',1),(4,'Dev',1),(5,'Esha',1),(6,'Farah',1),
 (7,'Gopal',2),(8,'Hari',2),(9,'Ira',3),(10,'Jay',2);
```

**SQL answer:** manager names (`SQL_NAMES`) and managers with at least 5 direct reports (`SQL_MAIN`), both in the Code block.
```sql
SELECT e.emp_id, e.name, m.name AS manager_name
FROM employees e LEFT JOIN employees m ON m.emp_id = e.manager_id
ORDER BY e.emp_id
```
```sql
SELECT m.emp_id, m.name, COUNT(*) AS direct_reports
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name
HAVING COUNT(*) >= 5
ORDER BY m.emp_id
```

**pandas answer:**
```python
names_pd = (emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id",
                      how="left", suffixes=("", "_mgr"), validate="many_to_one")
            .rename(columns={"name_mgr": "manager_name"})[["emp_id", "name", "manager_name"]]
            .sort_values("emp_id").reset_index(drop=True))
pairs = emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id", suffixes=("", "_mgr"))
counts = (pairs.groupby(["emp_id_mgr", "name_mgr"], as_index=False).size()
          .rename(columns={"emp_id_mgr": "emp_id", "name_mgr": "name", "size": "direct_reports"}))
pd_df = counts[counts["direct_reports"] >= 5].sort_values("emp_id").reset_index(drop=True)
```

**Example:** 10 employees. Zara (1) has no manager. Reports: Zara has 5 (Ben, Chitra, Dev, Esha, Farah), Ben has 3 (Gopal, Hari, Jay), Chitra has 1 (Ira).
- With LEFT JOIN: 10 rows; Zara's manager_name is NULL.
- With INNER JOIN: 9 rows, Zara disappears because her manager_id NULL matches no emp_id.
- Group by manager: Zara 5, Ben 3, Chitra 1. HAVING COUNT(*) >= 5 keeps only Zara.

**Code:** run with `python3 -I`.
```python
# Q22: one-level hierarchy: manager names, and managers with at least 5 direct reports
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'Zara',NULL),(2,'Ben',1),(3,'Chitra',1),(4,'Dev',1),(5,'Esha',1),(6,'Farah',1),
 (7,'Gopal',2),(8,'Hari',2),(9,'Ira',3),(10,'Jay',2);
"""
SQL_NAMES = """
SELECT e.emp_id, e.name, m.name AS manager_name
FROM employees e LEFT JOIN employees m ON m.emp_id = e.manager_id
ORDER BY e.emp_id
"""
SQL_INNER = "SELECT COUNT(*) FROM employees e JOIN employees m ON m.emp_id = e.manager_id"
SQL_MAIN = """
SELECT m.emp_id, m.name, COUNT(*) AS direct_reports
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name
HAVING COUNT(*) >= 5
ORDER BY m.emp_id
"""
SQL_COUNTS = """
SELECT m.emp_id, m.name, COUNT(*) AS direct_reports
FROM employees e JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name ORDER BY m.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
names_df = pd.read_sql_query(SQL_NAMES, con)
print(names_df.to_string(index=False))
print("\nINNER JOIN rows:", con.execute(SQL_INNER).fetchone()[0], "of 10 employees (Zara dropped)")
print("\nreports per manager:"); print(pd.read_sql_query(SQL_COUNTS, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nmanagers with >= 5 direct reports:"); print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
print("\nmanager_id dtype in pandas:", emp["manager_id"].dtype)
# pd:main
names_pd = (emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id",
                      how="left", suffixes=("", "_mgr"), validate="many_to_one")
            .rename(columns={"name_mgr": "manager_name"})[["emp_id", "name", "manager_name"]]
            .sort_values("emp_id").reset_index(drop=True))
pairs = emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id", suffixes=("", "_mgr"))
counts = (pairs.groupby(["emp_id_mgr", "name_mgr"], as_index=False).size()
          .rename(columns={"emp_id_mgr": "emp_id", "name_mgr": "name", "size": "direct_reports"}))
pd_df = counts[counts["direct_reports"] >= 5].sort_values("emp_id").reset_index(drop=True)
# pd:end
print("pandas result:"); print(pd_df.to_string(index=False))
print("pandas inner merge rows:", len(pairs))

def norm(d): return d.astype(object).where(d.notna(), None).reset_index(drop=True)
# compared after sorting by emp_id
pd.testing.assert_frame_equal(norm(names_df), norm(names_pd), check_dtype=False)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert list(sql_df["name"]) == ["Zara"] and pd.isna(names_df.loc[0, "manager_name"])
print("asserts passed: SQL == pandas for both parts")
```

**Output (my run):**
```text
 emp_id   name manager_name
      1   Zara          NaN
      2    Ben         Zara
      3 Chitra         Zara
      4    Dev         Zara
      5   Esha         Zara
      6  Farah         Zara
      7  Gopal          Ben
      8   Hari          Ben
      9    Ira       Chitra
     10    Jay          Ben

INNER JOIN rows: 9 of 10 employees (Zara dropped)

reports per manager:
 emp_id   name  direct_reports
      1   Zara               5
      2    Ben               3
      3 Chitra               1

managers with >= 5 direct reports:
 emp_id name  direct_reports
      1 Zara               5

manager_id dtype in pandas: float64
pandas result:
 emp_id name  direct_reports
      1 Zara               5
pandas inner merge rows: 9
asserts passed: SQL == pandas for both parts
```

**Edge cases:**
- Employee with a NULL manager: appears with a NULL manager name under LEFT JOIN, never under INNER JOIN.
- Managers with no reports (leaf employees) never show up in the count, which is right: `HAVING COUNT(*) >= 5` cannot be satisfied by 0 rows.
- Group by id and name, not just name, since two managers can share a name.
- A manager_id that points to a deleted employee is dropped by the INNER JOIN (and has a NULL name under a LEFT JOIN); a foreign key would prevent it.
- In pandas `manager_id` is `float64` because of the NaN; merging it with the integer `emp_id` worked, and the NaN key matched nothing.
- The threshold is inclusive ("at least 5"): `>= 5`, not `> 5`.

**Then explain:**
- **The two aliases:** `e` is the employee, `m` is the same table read as the manager; the join condition links the employee's `manager_id` to the manager's `emp_id`.
- **Why INNER drops the top person:** a NULL `manager_id` equals nothing, so Zara has no partner row. LEFT JOIN keeps every employee and fills the manager columns with NULL.
- **Counting:** in the group query the join already restricts to employees who have a manager; each such row is one direct report of the grouped manager.
- **Multi-level chains:** one self join gives one level only (employee to manager). Manager's manager needs another join, and an unknown depth needs a recursive CTE (Part 9).
- **pandas:** `merge(left_on="manager_id", right_on="emp_id", suffixes=...)` for the names, then `groupby().size()` and a filter.

**Follow-ups:**
- *Can you do the count without a self join?* Yes: `GROUP BY manager_id HAVING COUNT(*) >= 5` on the employees table, then join once for the name (not run here).
- *Employees with no manager listed explicitly?* `WHERE manager_id IS NULL` on employees.
- *Number of reports for everyone, including zero?* LEFT JOIN from managers to employees and `COUNT(e.emp_id)`.

**Common mistakes:**
- INNER JOIN for the names, losing the top person.
- `HAVING COUNT(*) > 5` for "at least 5".
- Selecting the name without it being in the GROUP BY (SQLite accepts bare columns; strict engines reject it, not run here).
- Joining on `e.emp_id = m.manager_id`, which reverses who is the manager.

### Q23 ⭐⭐ 🟢 pandas join versus merge versus concat: left has index customer_id and columns name, city; right has index customer_id and column segment. Show left.join(right), pd.merge with left_index/right_index, and pd.concat(axis=1) side by side, explain which aligns on the index, the default how of each (join left, merge inner, concat outer), what concat does with duplicate index labels, and when to reset_index first.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** All three align on the index, but with different defaults: `left.join(right)` is a left join, `pd.merge(..., left_index=True, right_index=True)` is an inner join, and `pd.concat([left, right], axis=1)` is an outer join; `concat(axis=1)` raises on duplicate labels when it has to reindex, so reset_index and merge when the key repeats.

**Schema and sample data:** (the pandas frames are built from these tables, with `customer_id` as the index; the SQL equivalents are LEFT, INNER and FULL JOIN)
```sql
CREATE TABLE left_t(customer_id INTEGER, name TEXT, city TEXT);
CREATE TABLE right_t(customer_id INTEGER, segment TEXT);
INSERT INTO left_t VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO right_t VALUES (2,'gold'),(3,'silver'),(4,'bronze');
```

**SQL answer:** the three queries below are in the Code block, executed on SQLite 3.45.1: `join` is `SQL_LEFT`, `merge` is `SQL_INNER`, `concat(axis=1)` is `SQL_FULL`.
```sql
SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l LEFT JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
```
```sql
SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
```
```sql
SELECT COALESCE(l.customer_id, r.customer_id) AS customer_id, l.name, l.city, r.segment
FROM left_t l FULL JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
```

**pandas answer:**
```python
joined = left.join(right)                                                   # default how='left', aligns on index
merged = pd.merge(left, right, left_index=True, right_index=True)           # default how='inner'
stacked = pd.concat([left, right], axis=1)                                  # default join='outer', aligns on index
```

**Example:** left has customers 1, 2, 3; right has 2, 3, 4.
- `left.join(right)`: all left rows, so 1, 2, 3; customer 1 has NaN segment.
- `merge` with both indexes: only keys on both sides, 2 and 3.
- `concat(axis=1)`: the union of the indexes, 1, 2, 3, 4; customer 4 has NaN name and city.
- Counts: 3, 2 and 4 rows; each matches the SQL query (LEFT, INNER, FULL).

**Code:** run with `python3 -I`.
```python
# Q23: pandas join vs merge vs concat on indexed frames
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE left_t(customer_id INTEGER, name TEXT, city TEXT);
CREATE TABLE right_t(customer_id INTEGER, segment TEXT);
INSERT INTO left_t VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO right_t VALUES (2,'gold'),(3,'silver'),(4,'bronze');
"""
SQL_LEFT = "SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l LEFT JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1"
SQL_INNER = "SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1"
SQL_FULL = """
SELECT COALESCE(l.customer_id, r.customer_id) AS customer_id, l.name, l.city, r.segment
FROM left_t l FULL JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con).set_index("customer_id")
s_left, s_inner, s_full = q(SQL_LEFT), q(SQL_INNER), q(SQL_FULL)

left = pd.read_sql_query("SELECT * FROM left_t", con).set_index("customer_id")
right = pd.read_sql_query("SELECT * FROM right_t", con).set_index("customer_id")
# pd:main
joined = left.join(right)                                                   # default how='left', aligns on index
merged = pd.merge(left, right, left_index=True, right_index=True)           # default how='inner'
stacked = pd.concat([left, right], axis=1)                                  # default join='outer', aligns on index
# pd:end
for title, d in [("left.join(right)", joined), ("pd.merge(left_index, right_index)", merged), ("pd.concat(axis=1)", stacked)]:
    print(title); print(d.to_string()); print()

# duplicate index labels on the right: customer 2 has two segment rows
right_dup = pd.concat([right, pd.DataFrame({"segment": ["promo"]}, index=pd.Index([2], name="customer_id"))])
print("right with duplicate label 2:"); print(right_dup.to_string(), "\n")
print("left.join(right_dup):"); print(left.join(right_dup).to_string(), "\n")
try:
    pd.concat([left, right_dup], axis=1)
except Exception as e:
    print("concat(axis=1) with duplicate labels ->", type(e).__name__ + ":", e)
dup_chk = pd.concat([right_dup, right_dup], axis=1)
print("concat of two frames that share the SAME duplicated index works (identical indexes):", len(dup_chk), "rows")

# reset_index: the key becomes a normal column, so merge/join can use on=
l2, r2 = left.reset_index(), right.reset_index()
by_col = l2.merge(r2, on="customer_id", how="left")
print("\nreset_index + merge on column:"); print(by_col.to_string(index=False))

# all compared after sorting by customer_id (index)
for a, b in [(s_left, joined), (s_inner, merged), (s_full, stacked)]:
    pd.testing.assert_frame_equal(a.sort_index(), b.sort_index(), check_dtype=False)
pd.testing.assert_frame_equal(s_left.reset_index(), by_col.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
assert (len(joined), len(merged), len(stacked)) == (3, 2, 4)
print("\nasserts passed: join == LEFT JOIN, merge == INNER JOIN, concat(axis=1) == FULL JOIN")
```

**Output (my run):**
```text
left.join(right)
               name    city segment
customer_id                        
1              Asha    Pune     NaN
2               Ben   Delhi    gold
3            Chitra  Mumbai  silver

pd.merge(left_index, right_index)
               name    city segment
customer_id                        
2               Ben   Delhi    gold
3            Chitra  Mumbai  silver

pd.concat(axis=1)
               name    city segment
customer_id                        
1              Asha    Pune     NaN
2               Ben   Delhi    gold
3            Chitra  Mumbai  silver
4               NaN     NaN  bronze

right with duplicate label 2:
            segment
customer_id        
2              gold
3            silver
4            bronze
2             promo 

left.join(right_dup):
               name    city segment
customer_id                        
1              Asha    Pune     NaN
2               Ben   Delhi    gold
2               Ben   Delhi   promo
3            Chitra  Mumbai  silver 

concat(axis=1) with duplicate labels -> InvalidIndexError: Reindexing only valid with uniquely valued Index objects
concat of two frames that share the SAME duplicated index works (identical indexes): 4 rows

reset_index + merge on column:
 customer_id   name   city segment
           1   Asha   Pune     NaN
           2    Ben  Delhi    gold
           3 Chitra Mumbai  silver

asserts passed: join == LEFT JOIN, merge == INNER JOIN, concat(axis=1) == FULL JOIN
```

**Edge cases:**
- Duplicate labels on the right (customer 2 twice): `join` repeats the left row, one output row per match (3 -> 4 rows, like a SQL one-to-many join). `concat(axis=1)` with a different duplicated index raised `InvalidIndexError: Reindexing only valid with uniquely valued Index objects`. Concat of two frames that share exactly the same index does not need reindexing, and ran without error (4 rows in my run).
- Overlapping column names: `join` and `merge` need a suffix rule, and concat keeps both columns with the same name; I did not run this case.
- A RangeIndex 0..n on both frames: `concat(axis=1)` and `join` align by position label, which looks fine until a filter changes one of them.
- After `reset_index()`, the key is an ordinary column and `merge(on="customer_id", how="left")` gives the same result as the join (my assert).

**Then explain:**
- **Alignment:** `join`, `merge` with `left_index`/`right_index`, and `concat(axis=1)` all line rows up by index label. Plain `merge(on=column)` ignores the index entirely.
- **Defaults:** `DataFrame.join` is `how="left"`; `pd.merge` is `how="inner"`; `concat` is `join="outer"`. All three accept an explicit setting (concat takes `join="inner"` or `"outer"`, and has no left or right).
- **Duplicates:** join and merge do the SQL thing (all matching combinations); concat refuses when it must reindex a duplicated index.
- **When to reset_index first:** when the key is an index on one frame but a column on the other, when the index has duplicates or is just a meaningless row number, when you need a key column in the output, or when you want `indicator=True` and `validate=` on a merge with named keys.
- **Which to use:** `merge` when you want SQL join semantics and named keys, `join` for quick index lookups, `concat(axis=1)` to place frames with the same index side by side.

**Follow-ups:**
- *Row-wise stacking?* `pd.concat(axis=0)` is UNION ALL (Q10).
- *Join on a column of left and the index of right?* `join(on=...)` supports that; not run here.
- *Which is fastest?* Not measured here; index alignment on a unique sorted index is the cheap case (concept only).

**Common mistakes:**
- Expecting `join` to be an inner join, or `merge` to be a left join.
- Using `concat(axis=1)` with a duplicated index and being surprised by the error.
- Concatenating side by side two frames whose indexes are unrelated row numbers.
- Forgetting that the key is in the index and writing `merge(on="customer_id")`, which fails with a KeyError (not run here).

### Q24 ⭐⭐ 🟢 Anti-join and semi-join in pandas: customers(customer_id, name) and orders(order_id, customer_id). Write customers with no orders and customers with at least one order using (a) merge(how='left', indicator=True) with a _merge filter, (b) ~isin and isin, and (c) merge on drop_duplicates keys. Explain which is fastest conceptually, what happens with NaN in isin, and the SQL NOT IN NULL trap that does not exist in isin.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** In pandas, "no orders" is `~customers.customer_id.isin(orders.customer_id)` and "has orders" is `isin`; the merge forms (`indicator=True` then filter `_merge`, or an inner merge on deduplicated keys) give the same rows, and unlike SQL `NOT IN`, a NaN in the orders keys does not wipe out the result.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);  -- NULL = guest checkout
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,NULL);
```

**SQL answer:** (the reference result; same text as in the Code block)
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
```
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
```
Anti-join is `NOT EXISTS`, semi-join is `EXISTS`. The `NOT IN` version is also in the Code block, only to show that it returns zero rows here (Part 1 Q13 and Part 2 Q2 cover that trap).

**pandas answer:** (same text as in the Code block)
```python
# (a) merge + indicator, then filter _merge
m = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id",
                    how="left", indicator=True, validate="one_to_one")
anti_a = m.loc[m["_merge"] == "left_only", ["customer_id", "name"]]
semi_a = m.loc[m["_merge"] == "both", ["customer_id", "name"]]
```
```python
# (b) isin
anti_b = customers[~customers["customer_id"].isin(orders["customer_id"])]
semi_b = customers[customers["customer_id"].isin(orders["customer_id"])]
```
```python
# (c) inner merge on deduplicated keys (semi-join only)
keys = orders[["customer_id"]].drop_duplicates()
semi_c = customers.merge(keys, on="customer_id", how="inner")
```
In (a) and (c) the orders side is reduced to its distinct key first, so the merge cannot repeat a customer. `validate="one_to_one"` makes pandas check that for me.

**Example:** Customers are 1 Asha, 2 Ben, 3 Chitra, 4 Dev. Orders belong to 1, 1, 2 and a guest (NULL). Distinct order keys: {1, 2, NaN}. Left-merge with indicator: Asha and Ben are `both`, Chitra and Dev are `left_only`. So anti-join = Chitra, Dev and semi-join = Asha, Ben. Without the `drop_duplicates`, Asha would appear twice (two orders), exactly like a plain SQL JOIN.

**Code:** (run with `python3 -I`; the SQL and pandas results are compared as lists of (customer_id, name) sorted by customer_id)
```python
# Q24: anti-join and semi-join in pandas (merge+indicator, isin, merge on deduplicated keys) vs SQL
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

# sql:anti
SQL_ANTI = """
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
"""
# end
# sql:semi
SQL_SEMI = """
SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
"""
# end
SQL_NOT_IN = "SELECT customer_id, name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)"

def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_anti, sql_semi = sql(SQL_ANTI), sql(SQL_SEMI)
print("SQL anti (NOT EXISTS):", sql_anti)
print("SQL semi (EXISTS):    ", sql_semi)
print("SQL NOT IN with a NULL in orders:", sql(SQL_NOT_IN))

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("\norders.customer_id dtype:", orders["customer_id"].dtype, "| customers.customer_id dtype:", customers["customer_id"].dtype)

def rows(df): return [tuple(r) for r in df[["customer_id", "name"]].sort_values("customer_id").itertuples(index=False, name=None)]

# pd:a
m = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id",
                    how="left", indicator=True, validate="one_to_one")
anti_a = m.loc[m["_merge"] == "left_only", ["customer_id", "name"]]
semi_a = m.loc[m["_merge"] == "both", ["customer_id", "name"]]
# end
# pd:b
anti_b = customers[~customers["customer_id"].isin(orders["customer_id"])]
semi_b = customers[customers["customer_id"].isin(orders["customer_id"])]
# end
# pd:c
keys = orders[["customer_id"]].drop_duplicates()
semi_c = customers.merge(keys, on="customer_id", how="inner")
# end
print("\n(a) merge indicator counts:", m["_merge"].value_counts().to_dict())
print("(a) anti:", rows(anti_a), "| semi:", rows(semi_a))
print("(b) anti:", rows(anti_b), "| semi:", rows(semi_b))
print("(c) semi:", rows(semi_c))
assert rows(anti_a) == rows(anti_b) == sql_anti
assert rows(semi_a) == rows(semi_b) == rows(semi_c) == sql_semi
assert len(m) == len(customers)   # validate='one_to_one' + dedup kept the grain at one row per customer

# what goes wrong without drop_duplicates: Asha has two orders
dup = customers.merge(orders[["customer_id"]], on="customer_id", how="inner")
print("\ninner merge WITHOUT drop_duplicates:", dup["name"].tolist(), "(Asha twice, a plain JOIN fan-out)")
try:
    customers.merge(orders[["customer_id"]], on="customer_id", validate="one_to_one")
except pd.errors.MergeError as e:
    print("validate='one_to_one' on the raw orders ->", type(e).__name__, "|", str(e).splitlines()[0])

# NaN in isin: NaN matches NaN. In the SQL NOT IN, a NULL in the subquery kills every row.
print("\nisin with NaN:", pd.Series([1.0, 3.0, np.nan]).isin([1.0, np.nan]).tolist())
cust_nan = pd.DataFrame({"customer_id": [1.0, 3.0, np.nan], "name": ["Asha", "Chitra", "NoKey"]})
print("~isin where BOTH sides have NaN keeps:", cust_nan[~cust_nan["customer_id"].isin(orders["customer_id"])]["name"].tolist(),
      "(NoKey is treated as having an order)")
print("~isin after orders keys .dropna() keeps:",
      cust_nan[~cust_nan["customer_id"].isin(orders["customer_id"].dropna())]["name"].tolist())
print("merge also matches NaN to NaN:",
      cust_nan.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)[["name", "_merge"]].values.tolist())

# dtype note: int64 keys against float64 keys (NaN made orders float) merge fine; int against str raises
try:
    customers.merge(pd.DataFrame({"customer_id": ["1", "2"]}), on="customer_id")
except ValueError as e:
    print("\nint64 vs str key ->", type(e).__name__, "|", str(e)[:75])
print("asserts passed")
```

**Output (my run):**
```text
SQL anti (NOT EXISTS): [(3, 'Chitra'), (4, 'Dev')]
SQL semi (EXISTS):     [(1, 'Asha'), (2, 'Ben')]
SQL NOT IN with a NULL in orders: []

orders.customer_id dtype: float64 | customers.customer_id dtype: int64

(a) merge indicator counts: {'left_only': 2, 'both': 2, 'right_only': 0}
(a) anti: [(3, 'Chitra'), (4, 'Dev')] | semi: [(1, 'Asha'), (2, 'Ben')]
(b) anti: [(3, 'Chitra'), (4, 'Dev')] | semi: [(1, 'Asha'), (2, 'Ben')]
(c) semi: [(1, 'Asha'), (2, 'Ben')]

inner merge WITHOUT drop_duplicates: ['Asha', 'Asha', 'Ben'] (Asha twice, a plain JOIN fan-out)
validate='one_to_one' on the raw orders -> MergeError | Merge keys are not unique in right dataset; not a one-to-one merge

isin with NaN: [True, False, True]
~isin where BOTH sides have NaN keeps: ['Chitra'] (NoKey is treated as having an order)
~isin after orders keys .dropna() keeps: ['Chitra', 'NoKey']
merge also matches NaN to NaN: [['Asha', 'both'], ['Chitra', 'left_only'], ['NoKey', 'both']]

int64 vs str key -> ValueError | You are trying to merge on int64 and str columns for key 'customer_id'. If 
asserts passed
```

**Edge cases:**
- **Duplicate order rows:** semi-join by plain merge repeats the customer once per order. Deduplicate the keys first, or use `isin`, which returns each customer once.
- **NaN in `isin`:** `isin` treats NaN as equal to NaN (output: `[True, False, True]`). With NaN keys on both sides, a customer whose key is NaN counts as "has an order" (`NoKey` vanished from the anti-join). Drop NaN from the keys if that is not what you want. This is the opposite of SQL, where NULL never equals NULL.
- **The SQL `NOT IN` trap does not exist in `isin`:** the SQL `NOT IN` returned `[]` because of the guest NULL; `~isin` returned Chitra and Dev, because `isin` is a plain yes/no membership test with no UNKNOWN state.
- **Merge also matches NaN to NaN** (`NoKey` came back as `both`). I confirmed this by running it on pandas 3.0.5; it is a pandas behaviour, not SQL behaviour.
- **dtype:** the NULL turned `orders.customer_id` into float64 while `customers.customer_id` is int64. Merge and `isin` still match 1 with 1.0. An int key against a string key raises `ValueError` (printed above); that belongs to Q35.
- **Empty orders table:** the anti-join returns all customers and the semi-join none.

**Then explain:**
- **(a) merge with indicator** is the literal LEFT JOIN ... IS NULL: `left_only` is the unmatched rows, `both` the matched ones. It is the most explicit and lets you see both groups in one pass.
- **(b) isin** is a membership test: pandas hashes the orders keys once and probes each customer. For an existence check I would use this first; it is short and cannot change the number of rows.
- **(c) merge on deduplicated keys** is the "JOIN plus DISTINCT" semi-join. It is useful when you want to bring columns across, but then deduplicate to the grain you need first.
- **Which is fastest, conceptually:** all three are hash-based and linear in the sizes. `isin` should do the least work because it builds no result frame with the orders columns and no `_merge` column; the merges allocate a joined frame. I did not benchmark it here, so treat it as expected, not measured. On big data, measure.
- **Choosing:** `isin` for a pure filter, merge when you need columns from the right table or want the `_merge` audit.
- **SQL side:** the dialect-independent safe forms are `NOT EXISTS` and `EXISTS`. I only ran SQLite here, so Postgres, MySQL, BigQuery and Snowflake behaviour of `NOT IN` is from memory (not executed), though the NULL rule is standard.

**Follow-ups:**
- *How do I get SQL-like NOT IN behaviour in pandas?* Say what you want: `if orders["customer_id"].isna().any(): result = empty` replicates SQL; usually you do not want that, so drop the NaN keys and filter.
- *Why not `merge` without `drop_duplicates` for the semi-join?* It repeats customers once per order.
- *How would you catch a changed grain?* `validate="one_to_one"` or `"many_to_one"` and an `assert len(result) == len(customers)`.

**Common mistakes:**
- Using `merge(how="inner")` on raw orders and reporting inflated customers.
- Filtering `_merge == "left_only"` without `indicator=True`, or checking `isna()` on a right column that can itself be NULL, instead of the `_merge` flag.
- Writing `customers[~customers.customer_id.isin(orders.customer_id)]` and assuming NaN keys are excluded; they match each other.
- Assuming `isin` has the SQL `NOT IN` NULL trap, or that SQL `NOT IN` is as forgiving as `~isin`.

### Q25 ⭐⭐ 🟡 Non-equi join with bands: employees(emp_id, name, salary) and grades(grade, min_salary, max_salary). Assign each employee a grade with a range join. Explain what happens at boundary values when ranges overlap or use BETWEEN on both ends (an employee gets two grades), how to define half-open ranges, and show pandas options (cross merge then filter, pd.cut or IntervalIndex, merge_asof on min_salary).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** A band lookup is a non-equi join (`ON salary >= min AND salary < max`); store the bands half-open so every salary falls in exactly one band, because `BETWEEN` on both ends gives an employee on a shared edge two grades.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
CREATE TABLE grades(grade TEXT PRIMARY KEY, min_salary INTEGER, max_salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',30),(2,'Ben',50),(3,'Chitra',75),(4,'Dev',100),(5,'Esha',150),(6,'Farid',250);
INSERT INTO grades VALUES ('C',0,50),('B',50,100),('A',100,200);
```
(The salaries are toy column values. The bands share their edges: C ends at 50 where B starts, B ends at 100 where A starts.)

**SQL answer:** (same text as in the Code block)
```sql
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary >= g.min_salary AND e.salary < g.max_salary
ORDER BY e.emp_id
```
The `BETWEEN` version, which is the trap:
```sql
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary BETWEEN g.min_salary AND g.max_salary
ORDER BY e.emp_id, g.grade
```
I use `LEFT JOIN` so an employee above every band (Farid, 250) is kept with a NULL grade instead of silently disappearing.

**pandas answer:** (same text as in the Code block; all four give the same result)
```python
# 1. cross merge then filter (the literal non-equi join)
x = employees.merge(grades, how="cross")
x = x[(x["salary"] >= x["min_salary"]) & (x["salary"] < x["max_salary"])]
p_cross = employees.merge(x[["emp_id", "grade"]], on="emp_id", how="left", validate="one_to_one")
```
```python
# 2. pd.cut with right=False (half-open)
bins = [0, 50, 100, 200]                      # edges taken from the grade table, sorted
p_cut = employees.assign(grade=pd.cut(employees["salary"], bins=bins, right=False,
                                      labels=["C", "B", "A"]).astype(object))
```
```python
# 3. IntervalIndex lookup
iv = pd.IntervalIndex.from_arrays(grades["min_salary"], grades["max_salary"], closed="left")
idx = iv.get_indexer(employees["salary"])    # -1 when no interval contains the value
p_interval = employees.assign(grade=np.where(idx >= 0, grades["grade"].to_numpy()[idx], None))
```
```python
# 4. merge_asof on the lower bound, then check the upper bound
asof = pd.merge_asof(employees.sort_values("salary"), grades.sort_values("min_salary"),
                     left_on="salary", right_on="min_salary", direction="backward")
asof["grade"] = asof["grade"].where(asof["salary"] < asof["max_salary"])   # asof ignores the upper edge
p_asof = asof.sort_values("emp_id")[["emp_id", "name", "salary", "grade"]]
```

**Example:** Ben earns 50. Under `BETWEEN`, 50 is inside C (0 to 50) and inside B (50 to 100), so Ben gets two rows. Dev earns 100, the edge of B and A, so Dev gets two rows. 6 employees become 8 rows. With half-open bands `[min, max)`, 50 belongs only to B (50 >= 50 and 50 < 100) and 100 only to A. Farid at 250 is outside every band, so he keeps a NULL grade through the LEFT JOIN.

**Code:** (run with `python3 -I`; each pandas result is compared with the half-open SQL result as a list of (emp_id, name, salary, grade) sorted by emp_id)
```python
# Q25: non-equi (range) join with salary bands: BETWEEN overlap vs half-open, plus pandas options
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
CREATE TABLE grades(grade TEXT PRIMARY KEY, min_salary INTEGER, max_salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',30),(2,'Ben',50),(3,'Chitra',75),(4,'Dev',100),(5,'Esha',150),(6,'Farid',250);
INSERT INTO grades VALUES ('C',0,50),('B',50,100),('A',100,200);
""")

# sql:between
SQL_BETWEEN = """
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary BETWEEN g.min_salary AND g.max_salary
ORDER BY e.emp_id, g.grade
"""
# end
# sql:main
SQL_MAIN = """
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary >= g.min_salary AND e.salary < g.max_salary
ORDER BY e.emp_id
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_between, sql_main = sql(SQL_BETWEEN), sql(SQL_MAIN)
print("BETWEEN on both ends (bands share their edges):")
for r in sql_between: print("  ", r)
print("rows:", len(sql_between), "for", 6, "employees")
print("\nhalf-open [min, max):")
for r in sql_main: print("  ", r)

employees = pd.read_sql_query("SELECT * FROM employees", con)
grades = pd.read_sql_query("SELECT * FROM grades", con)

# pd:cross
x = employees.merge(grades, how="cross")
x = x[(x["salary"] >= x["min_salary"]) & (x["salary"] < x["max_salary"])]
p_cross = employees.merge(x[["emp_id", "grade"]], on="emp_id", how="left", validate="one_to_one")
# end
# pd:cut
bins = [0, 50, 100, 200]                      # edges taken from the grade table, sorted
p_cut = employees.assign(grade=pd.cut(employees["salary"], bins=bins, right=False,
                                      labels=["C", "B", "A"]).astype(object))
# end
# pd:interval
iv = pd.IntervalIndex.from_arrays(grades["min_salary"], grades["max_salary"], closed="left")
idx = iv.get_indexer(employees["salary"])    # -1 when no interval contains the value
p_interval = employees.assign(grade=np.where(idx >= 0, grades["grade"].to_numpy()[idx], None))
# end
# pd:asof
asof = pd.merge_asof(employees.sort_values("salary"), grades.sort_values("min_salary"),
                     left_on="salary", right_on="min_salary", direction="backward")
asof["grade"] = asof["grade"].where(asof["salary"] < asof["max_salary"])   # asof ignores the upper edge
p_asof = asof.sort_values("emp_id")[["emp_id", "name", "salary", "grade"]]
# end
def norm(df):
    d = df[["emp_id", "name", "salary", "grade"]].sort_values("emp_id")
    return [(int(a), b, int(c), None if pd.isna(g) else g) for a, b, c, g in d.itertuples(index=False, name=None)]
ref = norm(pd.DataFrame(sql_main, columns=["emp_id", "name", "salary", "grade"]))
for name, df in [("cross+filter", p_cross), ("pd.cut", p_cut), ("IntervalIndex", p_interval), ("merge_asof", p_asof)]:
    assert norm(df) == ref, name
    print(f"pandas {name:14s} == SQL half-open:", norm(df) == ref)

# merge_asof WITHOUT the upper-edge check wrongly grades Farid (250)
raw = pd.merge_asof(employees.sort_values("salary"), grades.sort_values("min_salary"),
                    left_on="salary", right_on="min_salary")
print("\nmerge_asof without the max_salary check, Farid ->", raw.loc[raw["name"] == "Farid", "grade"].iloc[0])
dupes = pd.DataFrame(sql_between, columns=["emp_id", "name", "salary", "grade"]).groupby("emp_id").size()
print("employees with 2 grades under BETWEEN:", dupes[dupes > 1].index.tolist())
print("asserts passed")
```

**Output (my run):**
```text
BETWEEN on both ends (bands share their edges):
   (1, 'Asha', 30, 'C')
   (2, 'Ben', 50, 'B')
   (2, 'Ben', 50, 'C')
   (3, 'Chitra', 75, 'B')
   (4, 'Dev', 100, 'A')
   (4, 'Dev', 100, 'B')
   (5, 'Esha', 150, 'A')
   (6, 'Farid', 250, None)
rows: 8 for 6 employees

half-open [min, max):
   (1, 'Asha', 30, 'C')
   (2, 'Ben', 50, 'B')
   (3, 'Chitra', 75, 'B')
   (4, 'Dev', 100, 'A')
   (5, 'Esha', 150, 'A')
   (6, 'Farid', 250, None)
pandas cross+filter   == SQL half-open: True
pandas pd.cut         == SQL half-open: True
pandas IntervalIndex  == SQL half-open: True
pandas merge_asof     == SQL half-open: True

merge_asof without the max_salary check, Farid -> A
employees with 2 grades under BETWEEN: [2, 4]
asserts passed
```

**Edge cases:**
- **Shared edges with `BETWEEN`:** Ben and Dev were duplicated (row count 8 instead of 6). Any later `SUM` or `COUNT` per employee would double count them (the fan-out of Q12).
- **Gaps:** if the bands were 0-49 and 51-100, a salary of 50 (or 50.5) would match nothing; with a LEFT JOIN you see a NULL grade, with an INNER JOIN the employee vanishes.
- **Above the top band:** Farid has NULL. Decide whether that is a data error or a catch-all grade.
- **NULL salary:** every comparison is UNKNOWN, so the LEFT JOIN keeps the employee with a NULL grade (not run in the sample data; standard SQL rule). In pandas, `merge_asof` raises `ValueError: Merge keys contain null values on left side` (I confirmed this message by running a one-off check on pandas 3.0.5), while `pd.cut` gives NaN.
- **Float salaries** are why half-open bands matter: with integer bands `0-49, 50-99` a salary of 49.5 falls through; `[0, 50)` does not.
- **merge_asof surprise:** it only looks backward at the lower bound, so Farid got grade A (row printed above) until I added the upper-bound check.

**Then explain:**
- **Non-equi join:** the join condition uses `<`, `>=` or `BETWEEN` instead of `=`. Engines cannot hash it, so the work is roughly employees x grades (a nested loop, concept-level and engine dependent). Fine for a handful of bands, expensive for two big tables.
- **Half-open ranges:** write `min <= x AND x < max`, and have each band's `max` equal the next band's `min`. No overlaps and no gaps by construction. Enforce it with a check query on the band table (Q26 shows the overlap check).
- **pandas options:** cross merge then filter is the literal translation but builds employees x grades rows before filtering (see Q31 for the memory risk). `pd.cut` and `IntervalIndex` are lookups; they need bands that do not overlap and have no gaps. `merge_asof` is fast and also needs sorted, non-overlapping bands, and needs the manual upper-bound check.
- `pd.cut` with `right=False` is the half-open version; its default `right=True` gives `(a, b]`, the opposite edge, so check which edge you want.
- I only ran SQLite here. Other engines accept the same `ON` conditions (standard SQL), not executed.

**Follow-ups:**
- *How do you prevent overlapping bands in the data?* A check query or constraint on the band table, then half-open boundaries.
- *What if the bands come with an inclusive max, like 0-49?* Use `salary BETWEEN min AND max` for integers only, and say that a decimal salary can fall into the gap.
- *Can the join be an equi-join?* Only if you first compute a band key (for example `salary / 50`), which works for equal-width bands.

**Common mistakes:**
- `BETWEEN` with bands that share an edge, then not noticing duplicates.
- An INNER JOIN that silently drops employees outside every band.
- Using `merge_asof` and forgetting the upper bound, or forgetting that both sides must be sorted.
- Cross merge on large frames without checking `len(a) * len(b)` first.

### Q26 ⭐⭐ 🟡 Join on date ranges: price_history(product_id, price, valid_from, valid_to) with valid_to NULL for the current price, and orders(order_id, product_id, order_date, qty). Price each order at the price valid on order_date. Explain the BETWEEN with open-ended NULL trap, what a gap or an overlap in the history does (zero rows or duplicate rows), and how you would check the history for overlaps. Give pandas (merge on product_id then filter, or merge_asof).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join orders to the price row whose window contains the order date, `valid_from <= order_date AND (valid_to IS NULL OR order_date <= valid_to)`; `BETWEEN valid_from AND valid_to` silently loses every order on the current price because `valid_to` is NULL, and gaps or overlaps in the history give zero rows or duplicate rows.

**Schema and sample data:**
```sql
CREATE TABLE price_history(product_id INTEGER, price REAL, valid_from TEXT, valid_to TEXT);  -- valid_to NULL = current
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, product_id INTEGER, order_date TEXT, qty INTEGER);
INSERT INTO price_history VALUES
 (1,10.0,'2024-01-01','2024-01-31'),(1,12.0,'2024-02-01',NULL),        -- clean history
 (2, 5.0,'2024-01-01','2024-01-10'),(2, 6.0,'2024-01-15',NULL),        -- gap 11-14 Jan
 (3,20.0,'2024-01-01','2024-01-31'),(3,22.0,'2024-01-20',NULL);        -- overlap 20-31 Jan
INSERT INTO orders VALUES
 (1,1,'2024-01-15',2),(2,1,'2024-02-01',1),(3,1,'2024-03-10',4),(4,1,'2023-12-31',1),
 (5,2,'2024-01-12',3),(6,3,'2024-01-25',1);
```
`valid_to` is inclusive here (the last day the price applies); dates are ISO text, which compares correctly as text in SQLite.

**SQL answer:** (same text as in the Code block)
```sql
SELECT o.order_id, o.product_id, o.order_date, p.price, o.qty * p.price AS revenue
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id
 AND p.valid_from <= o.order_date
 AND (p.valid_to IS NULL OR o.order_date <= p.valid_to)
ORDER BY o.order_id, p.valid_from
```
The trap version:
```sql
SELECT o.order_id, p.price
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id AND o.order_date BETWEEN p.valid_from AND p.valid_to
ORDER BY o.order_id
```
History checks. Overlap: a later version starts on or before the end of an earlier one (an open end counts as far future):
```sql
SELECT a.product_id, a.valid_from AS a_from, a.valid_to AS a_to, b.valid_from AS b_from, b.valid_to AS b_to
FROM price_history a
JOIN price_history b
  ON a.product_id = b.product_id
 AND a.valid_from < b.valid_from
 AND b.valid_from <= COALESCE(a.valid_to, '9999-12-31')
ORDER BY a.product_id, a.valid_from
```
Gap: the day after a version ends must fall inside some version:
```sql
SELECT a.product_id, a.valid_to AS ends_on, date(a.valid_to, '+1 day') AS uncovered_day
FROM price_history a
WHERE a.valid_to IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM price_history b
                  WHERE b.product_id = a.product_id
                    AND b.valid_from <= date(a.valid_to, '+1 day')
                    AND COALESCE(b.valid_to, '9999-12-31') >= date(a.valid_to, '+1 day'))
ORDER BY a.product_id
```

**pandas answer:** (same text as in the Code block)
```python
# merge on product_id, filter the window, then merge back so unpriced orders stay
m = orders.merge(ph, on="product_id", how="left")
ok = (m["valid_from"] <= m["order_date"]) & (m["valid_to"].isna() | (m["order_date"] <= m["valid_to"]))
hit = m.loc[ok, ["order_id", "price", "valid_from"]]
p_main = orders.merge(hit, on="order_id", how="left")
p_main["revenue"] = p_main["qty"] * p_main["price"]
```
```python
# merge_asof: latest valid_from <= order_date per product, then check valid_to
a = pd.merge_asof(orders.sort_values("order_date"), ph.sort_values("valid_from"),
                  left_on="order_date", right_on="valid_from", by="product_id", direction="backward")
a["price"] = a["price"].where(a["valid_to"].isna() | (a["order_date"] <= a["valid_to"]))
```

**Example:** Product 1 has 10.0 up to 31 Jan and 12.0 from 1 Feb with no end. Order 1 (15 Jan) gets 10.0. Order 2 (1 Feb) and order 3 (10 Mar) fall in the open-ended row and get 12.0. With `BETWEEN`, `o.order_date BETWEEN '2024-02-01' AND NULL` is UNKNOWN, so orders 2 and 3 get a NULL price (the `Output` shows `None` for them). Order 4 (31 Dec 2023) is before the history, no row matches, NULL. Order 5 (product 2, 12 Jan) is in the gap, NULL. Order 6 (product 3, 25 Jan) is in the overlap, so it matches both 20.0 and 22.0 and appears twice; its revenue is counted twice if you sum.

**Code:** (run with `python3 -I`; pandas is compared with SQL on (order_id, price) sorted by order_id, price)
```python
# Q26: price each order at the price valid on order_date; BETWEEN/NULL trap, gaps, overlaps, checks
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE price_history(product_id INTEGER, price REAL, valid_from TEXT, valid_to TEXT);  -- valid_to NULL = current
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, product_id INTEGER, order_date TEXT, qty INTEGER);
INSERT INTO price_history VALUES
 (1,10.0,'2024-01-01','2024-01-31'),(1,12.0,'2024-02-01',NULL),        -- clean history
 (2, 5.0,'2024-01-01','2024-01-10'),(2, 6.0,'2024-01-15',NULL),        -- gap 11-14 Jan
 (3,20.0,'2024-01-01','2024-01-31'),(3,22.0,'2024-01-20',NULL);        -- overlap 20-31 Jan
INSERT INTO orders VALUES
 (1,1,'2024-01-15',2),(2,1,'2024-02-01',1),(3,1,'2024-03-10',4),(4,1,'2023-12-31',1),
 (5,2,'2024-01-12',3),(6,3,'2024-01-25',1);
""")

# sql:trap
SQL_TRAP = """
SELECT o.order_id, p.price
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id AND o.order_date BETWEEN p.valid_from AND p.valid_to
ORDER BY o.order_id
"""
# end
# sql:main
SQL_MAIN = """
SELECT o.order_id, o.product_id, o.order_date, p.price, o.qty * p.price AS revenue
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id
 AND p.valid_from <= o.order_date
 AND (p.valid_to IS NULL OR o.order_date <= p.valid_to)
ORDER BY o.order_id, p.valid_from
"""
# end
# sql:overlap
SQL_OVERLAP = """
SELECT a.product_id, a.valid_from AS a_from, a.valid_to AS a_to, b.valid_from AS b_from, b.valid_to AS b_to
FROM price_history a
JOIN price_history b
  ON a.product_id = b.product_id
 AND a.valid_from < b.valid_from
 AND b.valid_from <= COALESCE(a.valid_to, '9999-12-31')
ORDER BY a.product_id, a.valid_from
"""
# end
# sql:gap
SQL_GAP = """
SELECT a.product_id, a.valid_to AS ends_on, date(a.valid_to, '+1 day') AS uncovered_day
FROM price_history a
WHERE a.valid_to IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM price_history b
                  WHERE b.product_id = a.product_id
                    AND b.valid_from <= date(a.valid_to, '+1 day')
                    AND COALESCE(b.valid_to, '9999-12-31') >= date(a.valid_to, '+1 day'))
ORDER BY a.product_id
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
trap, main = sql(SQL_TRAP), sql(SQL_MAIN)
print("BETWEEN with NULL valid_to (order_id, price):", trap)
print("\ncorrect join (order_id, product_id, order_date, price, revenue):")
for r in main: print("  ", r)
print("\noverlap check:", sql(SQL_OVERLAP))
print("gap check:    ", sql(SQL_GAP))

orders = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_date"])
ph = pd.read_sql_query("SELECT * FROM price_history", con, parse_dates=["valid_from", "valid_to"])

# pd:main
m = orders.merge(ph, on="product_id", how="left")
ok = (m["valid_from"] <= m["order_date"]) & (m["valid_to"].isna() | (m["order_date"] <= m["valid_to"]))
hit = m.loc[ok, ["order_id", "price", "valid_from"]]
p_main = orders.merge(hit, on="order_id", how="left")
p_main["revenue"] = p_main["qty"] * p_main["price"]
# end
# pd:asof
a = pd.merge_asof(orders.sort_values("order_date"), ph.sort_values("valid_from"),
                  left_on="order_date", right_on="valid_from", by="product_id", direction="backward")
a["price"] = a["price"].where(a["valid_to"].isna() | (a["order_date"] <= a["valid_to"]))
# end
def norm(rows):
    return sorted((int(r[0]), None if pd.isna(r[1]) else float(r[1])) for r in rows)
sql_prices = norm([(r[0], r[3]) for r in main])
assert norm(p_main[["order_id", "price"]].itertuples(index=False, name=None)) == sql_prices
print("\npandas merge+filter == SQL (order_id, price), incl. the duplicated order 6 and the unpriced orders")
print("pandas rows:", len(p_main), "| SQL rows:", len(main), "| orders:", len(orders))
# merge_asof picks ONE row (the latest valid_from <= date): no duplicates, so the overlap for order 6 is hidden
print("merge_asof (order_id, price):", sorted(zip(a["order_id"], a["price"])))
dups = p_main.groupby("order_id").size()
print("orders priced more than once:", dups[dups > 1].index.tolist())
print("orders with no price:", p_main.loc[p_main["price"].isna(), "order_id"].tolist())
# overlap check in pandas
pm = ph.merge(ph, on="product_id", suffixes=("_a", "_b"))
ov = pm[(pm["valid_from_a"] < pm["valid_from_b"]) &
        (pm["valid_from_b"] <= pm["valid_to_a"].fillna(pd.Timestamp("2262-04-11")))]
assert len(ov) == len(sql(SQL_OVERLAP)) == 1
print("asserts passed")
```

**Output (my run):**
```text
BETWEEN with NULL valid_to (order_id, price): [(1, 10.0), (2, None), (3, None), (4, None), (5, None), (6, 20.0)]

correct join (order_id, product_id, order_date, price, revenue):
   (1, 1, '2024-01-15', 10.0, 20.0)
   (2, 1, '2024-02-01', 12.0, 12.0)
   (3, 1, '2024-03-10', 12.0, 48.0)
   (4, 1, '2023-12-31', None, None)
   (5, 2, '2024-01-12', None, None)
   (6, 3, '2024-01-25', 20.0, 20.0)
   (6, 3, '2024-01-25', 22.0, 22.0)

overlap check: [(3, '2024-01-01', '2024-01-31', '2024-01-20', None)]
gap check:     [(2, '2024-01-10', '2024-01-11')]

pandas merge+filter == SQL (order_id, price), incl. the duplicated order 6 and the unpriced orders
pandas rows: 7 | SQL rows: 7 | orders: 6
merge_asof (order_id, price): [(1, 10.0), (2, 12.0), (3, 12.0), (4, nan), (5, nan), (6, 22.0)]
orders priced more than once: [6]
orders with no price: [4, 5]
asserts passed
```

**Edge cases:**
- **Open end:** `BETWEEN a AND NULL` is never TRUE. Use `valid_to IS NULL OR ...` or `COALESCE(valid_to, '9999-12-31')`. A sentinel date is simple but must be the same in every query.
- **Gap:** the order matches nothing. A LEFT JOIN from orders shows it with a NULL price (orders 4 and 5); an INNER JOIN drops it and revenue falls silently.
- **Overlap:** the order matches two rows and is repeated (order 6). Row count 7 for 6 orders is the signal.
- **Inclusive versus exclusive end:** if `valid_to` is the day the next price starts (exclusive), use `order_date < valid_to`, and the gap check must compare with `valid_to` itself instead of `valid_to + 1 day`. Pick one convention and check the data against it.
- **Timestamps:** with a datetime `order_date`, an inclusive `valid_to` of `2024-01-31` excludes the afternoon of 31 Jan; half-open `[valid_from, valid_to)` with the next start as the end avoids that (not run here; the sample uses dates).
- **merge_asof** returns one row per order, the latest `valid_from <= order_date`. It hid the overlap (order 6 got only 22.0) and needs the `valid_to` check to expose gaps (order 5 became NaN). It also needs both sides sorted by the date key and raises on NaN keys (Q25).

**Then explain:**
- **Why the grain matters:** the lookup must return exactly one row per order. Each of the two failure modes (gap: 0 rows, overlap: 2 rows) breaks that, so test the history rather than trust it.
- **Overlap check:** the self join compares version a with a later version b of the same product. In my run it found one pair, product 3. `a.valid_from < b.valid_from` stops pairs being reported twice and stops a row overlapping itself.
- **Gap check:** it found product 2 (ends 10 Jan, 11 Jan uncovered). My first version asked "does a version start the day after?" and wrongly flagged product 3, whose successor starts early because of the overlap, so I changed it to ask whether the day is covered at all.
- **pandas:** merge on `product_id`, build the boolean window mask, take the hits, then merge back on `order_id` so unpriced orders survive. Filtering after a `how="left"` merge would drop them.
- `merge_asof` is the efficient form for large inputs (sorted merge, no full product per key), but it does not know about the end date or duplicates.
- Fix the source if you can: enforce non-overlapping versions with a constraint (PostgreSQL range types with an exclusion constraint do this; stated from memory, not executed here).

**Follow-ups:**
- *What if there are many orders and few price changes?* The join is cheap if indexed on `(product_id, valid_from)`; merge_asof is the pandas analogue.
- *How would you get the current price only?* `WHERE valid_to IS NULL` (one row per product if the history is clean; add a uniqueness check).
- *What would you do about gaps?* Report them, and decide with the business whether to backfill or let the price be missing; do not default silently.

**Common mistakes:**
- `BETWEEN` with an open-ended NULL.
- INNER JOIN, which hides gaps and unpriced orders.
- Not checking for duplicate order rows after the join (compare row count with the orders count).
- `<=` on both ends when the next version starts on the day the old one ends (double match on that day).

### Q27 ⭐⭐ 🟡 Overlapping intervals with a self join: bookings(booking_id, room_id, start_date, end_date). Find pairs of bookings for the same room that overlap. State the overlap condition (a.start < b.end AND b.start < a.end), explain why a.booking_id < b.booking_id, what changes if end_date is inclusive, and give the pandas version (merge on room_id then filter).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Two bookings of the same room overlap when each starts before the other ends, `a.start < b.end AND b.start < a.end`; add `a.booking_id < b.booking_id` so each pair appears once and no booking is paired with itself, and use `<=` instead of `<` only if the end date is inclusive.

**Schema and sample data:**
```sql
CREATE TABLE bookings(booking_id INTEGER PRIMARY KEY, room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,1,'2024-01-01','2024-01-05'),
 (2,1,'2024-01-03','2024-01-08'),
 (3,1,'2024-01-08','2024-01-10'),
 (4,2,'2024-01-01','2024-01-02'),
 (5,2,'2024-01-05','2024-01-06'),
 (6,3,'2024-01-02','2024-01-04'),
 (7,1,'2024-01-10','2024-01-12');
```
Here `end_date` is the check-out day, so the room is free for the next guest on that day (end exclusive).

**SQL answer:** (same text as in the Code block)
```sql
SELECT a.booking_id AS a_id, b.booking_id AS b_id, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_date < b.end_date
 AND b.start_date < a.end_date
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
```

**pandas answer:** (same text as in the Code block)
```python
m = bk.merge(bk, on="room_id", suffixes=("_a", "_b"))
hit = m[(m["booking_id_a"] < m["booking_id_b"]) &
        (m["start_date_a"] < m["end_date_b"]) &
        (m["start_date_b"] < m["end_date_a"])]
p_main = hit[["booking_id_a", "booking_id_b", "room_id"]].sort_values(["booking_id_a", "booking_id_b"])
```

**Example:** Room 1 has bookings 1 (1 to 5 Jan), 2 (3 to 8 Jan), 3 (8 to 10 Jan) and 7 (10 to 12 Jan). Bookings 1 and 2: 1 Jan < 8 Jan and 3 Jan < 5 Jan, so they overlap (3 to 5 Jan). Bookings 2 and 3: 3 Jan < 10 Jan but 8 Jan < 8 Jan is false, so they only touch at the check-out day and do not overlap. Same for 3 and 7. Room 2 (1 to 2 Jan and 5 to 6 Jan) and room 3 (one booking) have none. Result: the single pair (1, 2).

**Code:** (run with `python3 -I`; compared as sorted lists of (a_id, b_id, room_id) for both the exclusive and the inclusive versions)
```python
# Q27: overlapping bookings with a self join (end exclusive vs inclusive)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE bookings(booking_id INTEGER PRIMARY KEY, room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,1,'2024-01-01','2024-01-05'),
 (2,1,'2024-01-03','2024-01-08'),
 (3,1,'2024-01-08','2024-01-10'),
 (4,2,'2024-01-01','2024-01-02'),
 (5,2,'2024-01-05','2024-01-06'),
 (6,3,'2024-01-02','2024-01-04'),
 (7,1,'2024-01-10','2024-01-12');
""")
# sql:main
SQL_MAIN = """
SELECT a.booking_id AS a_id, b.booking_id AS b_id, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_date < b.end_date
 AND b.start_date < a.end_date
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
# end
# sql:incl
SQL_INCL = """
SELECT a.booking_id AS a_id, b.booking_id AS b_id, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_date <= b.end_date
 AND b.start_date <= a.end_date
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
# end
# sql:no_id
SQL_NO_ID = """
SELECT COUNT(*) FROM bookings a JOIN bookings b
  ON a.room_id = b.room_id AND a.start_date < b.end_date AND b.start_date < a.end_date
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_main, sql_incl = sql(SQL_MAIN), sql(SQL_INCL)
print("end exclusive (a.start < b.end AND b.start < a.end):", sql_main)
print("end inclusive (<=):", sql_incl)
print("same condition WITHOUT a.booking_id < b.booking_id -> rows:", sql(SQL_NO_ID)[0][0])

bk = pd.read_sql_query("SELECT * FROM bookings", con, parse_dates=["start_date", "end_date"])
# pd:main
m = bk.merge(bk, on="room_id", suffixes=("_a", "_b"))
hit = m[(m["booking_id_a"] < m["booking_id_b"]) &
        (m["start_date_a"] < m["end_date_b"]) &
        (m["start_date_b"] < m["end_date_a"])]
p_main = hit[["booking_id_a", "booking_id_b", "room_id"]].sort_values(["booking_id_a", "booking_id_b"])
# end
# pd:incl
hit_i = m[(m["booking_id_a"] < m["booking_id_b"]) &
          (m["start_date_a"] <= m["end_date_b"]) &
          (m["start_date_b"] <= m["end_date_a"])]
p_incl = hit_i[["booking_id_a", "booking_id_b", "room_id"]].sort_values(["booking_id_a", "booking_id_b"])
# end
assert [tuple(map(int, r)) for r in p_main.itertuples(index=False, name=None)] == sql_main
assert [tuple(map(int, r)) for r in p_incl.itertuples(index=False, name=None)] == sql_incl
print("pandas exclusive and inclusive == SQL")
print("rows after the merge on room_id alone:", len(m), "| bookings per room:", bk.groupby("room_id").size().to_dict())
touch = sorted(set(sql_incl) - set(sql_main))
print("pairs that only touch at an endpoint (inclusive adds them):", touch)
print("asserts passed")
```

**Output (my run):**
```text
end exclusive (a.start < b.end AND b.start < a.end): [(1, 2, 1)]
end inclusive (<=): [(1, 2, 1), (2, 3, 1), (3, 7, 1)]
same condition WITHOUT a.booking_id < b.booking_id -> rows: 9
pandas exclusive and inclusive == SQL
rows after the merge on room_id alone: 21 | bookings per room: {1: 4, 2: 2, 3: 1}
pairs that only touch at an endpoint (inclusive adds them): [(2, 3, 1), (3, 7, 1)]
asserts passed
```

**Edge cases:**
- **Why the condition works:** two intervals do not overlap only if one ends before the other starts: `a.end <= b.start` or `b.end <= a.start`. Negating gives `a.start < b.end AND b.start < a.end` (for end-exclusive intervals). It also covers one interval inside another, which a check like "a.start is within b" would miss.
- **Inclusive end dates:** if `end_date` is the last night, use `<=` on both comparisons. In my run this added (2, 3) and (3, 7), the touching pairs. Choose the convention from the business meaning (a hotel check-out day is exclusive; a leave request "1 to 5 Jan" is usually inclusive), and say it out loud.
- **Pair direction:** without `a.booking_id < b.booking_id` the same condition returned 9 rows: each of the 7 bookings overlapping itself plus the pair (1, 2) in both orders. `<>` would drop the self pairs but still return both orders.
- **Three-way overlaps** produce three pairs, one per two bookings; if you need clusters of overlap that is a gaps-and-islands problem (Part 7).
- **NULL end date** (open booking): the comparisons become UNKNOWN and the pair disappears; use `COALESCE(end_date, '9999-12-31')` (see Q26). Not run on this sample.
- **Same room is part of the join key.** Dropping `a.room_id = b.room_id` gives false overlaps across rooms.

**Then explain:**
- **Self join with two aliases:** `a` and `b` are the same table treated as two copies; the `ON` condition decides which pairs to keep.
- **Cost:** per room, every booking is compared with every other (about n squared / 2 pairs). In the sample, merging on `room_id` alone produced 21 rows (4x4 + 2x2 + 1x1) before the date filter. Large rooms with thousands of bookings are costly; an index on `(room_id, start_date)` helps in an engine, and in pandas you would filter early or sort and sweep. Engine behaviour is not executed here.
- **pandas:** merge on `room_id` with suffixes, then filter with the same three conditions. The `booking_id_a < booking_id_b` mask is the pandas version of the ordering rule.
- **Dates:** I parsed them as datetimes in pandas; in SQLite ISO text compares in the right order.

**Follow-ups:**
- *How would you find bookings that overlap a given date range?* One table, the same logic against constants: `start < :range_end AND end > :range_start`.
- *How do you prevent overlaps in the first place?* A constraint or exclusion rule (PostgreSQL range types, from memory, not executed) or a check in the booking transaction.
- *How do you list each booking with the number of conflicts?* Use the pair query as a subquery, or union both sides of each pair and count.

**Common mistakes:**
- Using `<=` on an end-exclusive calendar and flagging back-to-back bookings as conflicts, or `<` on an inclusive one and missing them.
- Testing only "a.start between b.start and b.end", which misses the case where `a` contains `b`.
- `<>` instead of `<` on the id, leaving mirror pairs.
- Forgetting the room condition.

### Q28 ⭐⭐ 🟡 Compare two snapshots, what changed: products_old(product_id, price, status) and products_new(product_id, price, status). Produce added, removed and changed products in one result. Use a FULL OUTER JOIN (or two LEFT JOINs with UNION ALL), a NULL-safe comparison for changed rows, and in pandas merge with indicator=True and DataFrame.compare. Explain why price <> price silently misses rows where one side is NULL.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** FULL OUTER JOIN the two snapshots on the key, then label a row `added` if the old side is missing, `removed` if the new side is missing, and `changed` if a column differs using a NULL-safe test (`IS NOT` in SQLite), because `price <> price` is UNKNOWN when either side is NULL and silently skips those rows.

**Schema and sample data:**
```sql
CREATE TABLE products_old(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
CREATE TABLE products_new(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
INSERT INTO products_old VALUES (1,10,'active'),(2,20,'active'),(3,30,'active'),(4,NULL,'active'),(5,7,'active'),(6,NULL,'active'),(7,15,'active');
INSERT INTO products_new VALUES (1,10,'active'),(2,20,'discontinued'),(3,35,'active'),(4,5,'active'),(5,NULL,'active'),(6,NULL,'active'),(8,40,'active');
```
(Prices are toy values.) Expected by eye: 1 same, 2 status changed, 3 price changed, 4 price NULL to 5, 5 price 7 to NULL, 6 NULL on both sides (not a change), 7 removed, 8 added.

**SQL answer:** (same text as in the Code block, runs on SQLite 3.45.1)
```sql
SELECT COALESCE(o.product_id, n.product_id) AS product_id,
       CASE WHEN o.product_id IS NULL THEN 'added'
            WHEN n.product_id IS NULL THEN 'removed'
            ELSE 'changed' END AS change,
       o.price AS old_price, n.price AS new_price, o.status AS old_status, n.status AS new_status
FROM products_old o
FULL OUTER JOIN products_new n ON n.product_id = o.product_id
WHERE o.product_id IS NULL OR n.product_id IS NULL
   OR o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY product_id
```
Alternative for an engine without FULL JOIN (the same rows; shown and run in the Code block):
```sql
SELECT o.product_id, 'removed' AS change, o.price AS old_price, NULL AS new_price, o.status AS old_status, NULL AS new_status
FROM products_old o LEFT JOIN products_new n ON n.product_id = o.product_id WHERE n.product_id IS NULL
UNION ALL
SELECT n.product_id, 'added', NULL, n.price, NULL, n.status
FROM products_new n LEFT JOIN products_old o ON o.product_id = n.product_id WHERE o.product_id IS NULL
UNION ALL
SELECT o.product_id, 'changed', o.price, n.price, o.status, n.status
FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY 1
```
The trap, which gives the wrong answer:
```sql
SELECT o.product_id FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price <> n.price OR o.status <> n.status ORDER BY 1
```

**pandas answer:** (same text as in the Code block)
```python
m = old.merge(new, on="product_id", how="outer", suffixes=("_old", "_new"), indicator=True, validate="one_to_one")
def differs(a, b):                       # NaN-safe "not equal": two NaN count as equal
    return ~(a.eq(b) | (a.isna() & b.isna()))
changed_mask = (m["_merge"] == "both") & (differs(m["price_old"], m["price_new"]) |
                                         differs(m["status_old"], m["status_new"]))
m["change"] = np.select([m["_merge"] == "right_only", m["_merge"] == "left_only", changed_mask],
                        ["added", "removed", "changed"], default="same")
p_main = m.loc[m["change"] != "same", ["product_id", "change", "price_old", "price_new", "status_old", "status_new"]]
```
```python
# DataFrame.compare on the keys present in both snapshots
both_ids = sorted(set(old["product_id"]) & set(new["product_id"]))
o2 = old.set_index("product_id").loc[both_ids]
n2 = new.set_index("product_id").loc[both_ids]
diff = o2.compare(n2, result_names=("old", "new"))
```

**Example:** Product 7 exists only in the old snapshot (removed) and product 8 only in the new one (added). For product 4 the old price is NULL and the new price is 5: `NULL <> 5` is UNKNOWN, so the naive query does not see the change; `NULL IS NOT 5` is TRUE, so the NULL-safe query does. Product 5 (7 to NULL) is the mirror case. Product 6 has NULL on both sides: `NULL IS NOT NULL` is FALSE, so correctly not changed. Result: changed 2, 3, 4, 5; removed 7; added 8.

**Code:** (run with `python3 -I`; SQL and pandas compared as lists sorted by product_id, NULL and NaN both as None)
```python
# Q28: compare two snapshots: added, removed, changed (NULL-safe), SQL FULL JOIN + pandas indicator / compare
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products_old(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
CREATE TABLE products_new(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
INSERT INTO products_old VALUES (1,10,'active'),(2,20,'active'),(3,30,'active'),(4,NULL,'active'),(5,7,'active'),(6,NULL,'active'),(7,15,'active');
INSERT INTO products_new VALUES (1,10,'active'),(2,20,'discontinued'),(3,35,'active'),(4,5,'active'),(5,NULL,'active'),(6,NULL,'active'),(8,40,'active');
-- 1 same; 2 status; 3 price; 4 NULL->5; 5 7->NULL; 6 NULL on both sides (same); 7 removed; 8 added
""")
# sql:main
SQL_MAIN = """
SELECT COALESCE(o.product_id, n.product_id) AS product_id,
       CASE WHEN o.product_id IS NULL THEN 'added'
            WHEN n.product_id IS NULL THEN 'removed'
            ELSE 'changed' END AS change,
       o.price AS old_price, n.price AS new_price, o.status AS old_status, n.status AS new_status
FROM products_old o
FULL OUTER JOIN products_new n ON n.product_id = o.product_id
WHERE o.product_id IS NULL OR n.product_id IS NULL
   OR o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY product_id
"""
# end
# sql:two
SQL_TWO = """
SELECT o.product_id, 'removed' AS change, o.price AS old_price, NULL AS new_price, o.status AS old_status, NULL AS new_status
FROM products_old o LEFT JOIN products_new n ON n.product_id = o.product_id WHERE n.product_id IS NULL
UNION ALL
SELECT n.product_id, 'added', NULL, n.price, NULL, n.status
FROM products_new n LEFT JOIN products_old o ON o.product_id = n.product_id WHERE o.product_id IS NULL
UNION ALL
SELECT o.product_id, 'changed', o.price, n.price, o.status, n.status
FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY 1
"""
# end
# sql:naive
SQL_NAIVE = """
SELECT o.product_id FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price <> n.price OR o.status <> n.status ORDER BY 1
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_main, sql_two = sql(SQL_MAIN), sql(SQL_TWO)
for r in sql_main: print(r)
print("two LEFT JOINs + UNION ALL gives the same rows:", sql_main == sql_two)
print("naive <> finds only:", [r[0] for r in sql(SQL_NAIVE)], "(misses 4 and 5, where one side is NULL)")

old = pd.read_sql_query("SELECT * FROM products_old", con)
new = pd.read_sql_query("SELECT * FROM products_new", con)
print("\nprice dtype in pandas:", old["price"].dtype, "(NULL made it float)")

# pd:main
m = old.merge(new, on="product_id", how="outer", suffixes=("_old", "_new"), indicator=True, validate="one_to_one")
def differs(a, b):                       # NaN-safe "not equal": two NaN count as equal
    return ~(a.eq(b) | (a.isna() & b.isna()))
changed_mask = (m["_merge"] == "both") & (differs(m["price_old"], m["price_new"]) |
                                         differs(m["status_old"], m["status_new"]))
m["change"] = np.select([m["_merge"] == "right_only", m["_merge"] == "left_only", changed_mask],
                        ["added", "removed", "changed"], default="same")
p_main = m.loc[m["change"] != "same", ["product_id", "change", "price_old", "price_new", "status_old", "status_new"]]
# end
# pd:compare
both_ids = sorted(set(old["product_id"]) & set(new["product_id"]))
o2 = old.set_index("product_id").loc[both_ids]
n2 = new.set_index("product_id").loc[both_ids]
diff = o2.compare(n2, result_names=("old", "new"))
# end
def norm(rows):
    out = []
    for r in rows:
        out.append(tuple(None if (isinstance(v, float) and np.isnan(v)) or v is None else (int(v) if isinstance(v, (float, np.integer)) else v) for v in r))
    return sorted(out)
a = norm(sql_main)
b = norm(p_main.sort_values("product_id").itertuples(index=False, name=None))
assert a == b, (a, b)
print("pandas merge(indicator) == SQL (sorted by product_id, NULL as None)")
print("\nDataFrame.compare on the common ids (only differing cells are shown, NaN == NaN):")
print(diff)
assert sorted(diff.index.tolist()) == [2, 3, 4, 5]
print("compare finds ids", diff.index.tolist(), "= the 'changed' ids", sorted(r[0] for r in sql_main if r[1] == "changed"))
print("asserts passed")
```

**Output (my run):**
```text
(2, 'changed', 20, 20, 'active', 'discontinued')
(3, 'changed', 30, 35, 'active', 'active')
(4, 'changed', None, 5, 'active', 'active')
(5, 'changed', 7, None, 'active', 'active')
(7, 'removed', 15, None, 'active', None)
(8, 'added', None, 40, None, 'active')
two LEFT JOINs + UNION ALL gives the same rows: True
naive <> finds only: [2, 3] (misses 4 and 5, where one side is NULL)

price dtype in pandas: float64 (NULL made it float)
pandas merge(indicator) == SQL (sorted by product_id, NULL as None)

DataFrame.compare on the common ids (only differing cells are shown, NaN == NaN):
           price        status              
             old   new     old           new
product_id                                  
2            NaN   NaN  active  discontinued
3           30.0  35.0     NaN           NaN
4            NaN   5.0     NaN           NaN
5            7.0   NaN     NaN           NaN
compare finds ids [2, 3, 4, 5] = the 'changed' ids [2, 3, 4, 5]
asserts passed
```

**Edge cases:**
- **NULL-safe comparison by dialect:** SQLite has `IS NOT` (ran above) and `IS`. PostgreSQL has `IS DISTINCT FROM` and MySQL `NOT (a <=> b)`; I did not run either. A portable form is `(a <> b OR (a IS NULL AND b IS NOT NULL) OR (a IS NOT NULL AND b IS NULL))`, which I did not run here but follows from the standard rules.
- **Naive `<>`:** it found only products 2 and 3. Products 4 and 5 were missed. It would also miss a status that changes to or from NULL.
- **Duplicate keys in a snapshot** multiply rows; in pandas `validate="one_to_one"` raises `MergeError` (I only used it on clean data). Check uniqueness first.
- **Float price in pandas:** the NULL made the column `float64`; ids with NaN on both sides are equal for `differs`, because I treat two NaN as the same.
- **`DataFrame.compare` surprise:** it shows `NaN` for any cell that did not change, so a real NULL (id 4 old price, id 5 new price) looks the same as "unchanged". Read it together with the source frames. It needs identical row and column labels, so I restricted both frames to the common ids first; it does not handle added or removed rows.
- **Column list:** if you compare many columns, generate the comparison per column; `IS NOT` per column is long but safe.

**Then explain:**
- **Three groups from one join:** added (left key NULL), removed (right key NULL), changed (matched with a difference). `COALESCE(o.product_id, n.product_id)` gives a key in every row (Q16, Q39).
- **FULL JOIN versus two LEFT JOINs + UNION ALL:** same rows when each part is disjoint (removed, added, changed). SQLite 3.45 ran both; I did not run MySQL, which lacks FULL JOIN (hedged).
- **pandas:** `merge(how="outer", indicator=True)` gives `_merge` (`left_only` means removed, `right_only` added); the changed mask needs an explicit NaN-safe comparison, since `NaN != NaN` is True in pandas, which would flag product 6 as changed. This differs from SQL, where the plain `<>` is the one that misses rows.
- **What `compare` is for:** a quick human-readable diff of two same-shaped frames; the merge version is the one you can load into a table.

**Follow-ups:**
- *How would you do this at scale?* Compare row hashes per key first, then drill into the differing keys (concept, not run here).
- *What if there is a composite key?* Join on all key columns and coalesce each.
- *Can EXCEPT do it?* `SELECT * FROM old EXCEPT SELECT * FROM new` returns rows that differ in any column and treats NULLs as equal (Q29), but it does not tell you which column changed or added versus changed.

**Common mistakes:**
- `price <> price` with NULLs.
- Calling a row "changed" when both sides are NULL (the other direction, using `=` or pandas `!=`).
- Filtering the FULL JOIN with `WHERE o.price <> n.price`, which also drops the added and removed rows.
- Reading `compare` output's NaN as "this cell is NULL".

### Q29 ⭐⭐ 🟡 EXCEPT and INTERSECT versus joins: customers_2024(customer_id) and customers_2025(customer_id). Find customers in both years, in 2024 only, and in 2025 only with INTERSECT, EXCEPT and with joins or EXISTS. Say how set operators treat NULLs and duplicates (they de-duplicate and treat NULLs as equal), that Oracle calls EXCEPT MINUS, and MySQL support is version dependent (hedge). Give pandas isin and merge.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `INTERSECT` gives customers in both years, `EXCEPT` gives one year minus the other; both de-duplicate and treat NULL as equal to NULL, which the join and `EXISTS` versions do not, so they agree with the set operators only after `DISTINCT` and a NULL-safe match.

**Schema and sample data:**
```sql
CREATE TABLE customers_2024(customer_id INTEGER);
CREATE TABLE customers_2025(customer_id INTEGER);
INSERT INTO customers_2024 VALUES (1),(2),(3),(3),(NULL);
INSERT INTO customers_2025 VALUES (2),(3),(4),(NULL);
```
(Deliberately dirty: customer 3 is listed twice in 2024, and both years have a NULL id.)

**SQL answer:** (same text as in the Code block)
```sql
SELECT customer_id FROM customers_2024 INTERSECT SELECT customer_id FROM customers_2025 ORDER BY 1
```
```sql
SELECT customer_id FROM customers_2024 EXCEPT SELECT customer_id FROM customers_2025 ORDER BY 1
```
```sql
SELECT customer_id FROM customers_2025 EXCEPT SELECT customer_id FROM customers_2024 ORDER BY 1
```
Join and `EXISTS` versions:
```sql
SELECT DISTINCT a.customer_id FROM customers_2024 a
JOIN customers_2025 b ON b.customer_id = a.customer_id ORDER BY 1
```
```sql
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id = a.customer_id) ORDER BY 1
```
```sql
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id IS a.customer_id) ORDER BY 1
```

**pandas answer:** (same text as in the Code block)
```python
in_both = c24[c24.isin(c25)].drop_duplicates()
only_24 = c24[~c24.isin(c25)].drop_duplicates()
only_25 = c25[~c25.isin(c24)].drop_duplicates()
```
```python
k24, k25 = c24.drop_duplicates().to_frame(), c25.drop_duplicates().to_frame()
mm = k24.merge(k25, on="customer_id", how="outer", indicator=True, validate="one_to_one")
m_both = mm.loc[mm["_merge"] == "both", "customer_id"]
m_only24 = mm.loc[mm["_merge"] == "left_only", "customer_id"]
m_only25 = mm.loc[mm["_merge"] == "right_only", "customer_id"]
```

**Example:** 2024 = {1, 2, 3, 3, NULL}, 2025 = {2, 3, 4, NULL}. `INTERSECT` de-duplicates and matches NULL with NULL, giving {NULL, 2, 3}. `2024 EXCEPT 2025` removes 2, 3 and NULL, leaving {1}. `2025 EXCEPT 2024` leaves {4}. The inner JOIN with `DISTINCT` gives only {2, 3}, because `NULL = NULL` is not TRUE, so the NULL customer is missing. Without `DISTINCT` the plain join returned 3 rows for 2 customers, since 3 appears twice in 2024.

**Code:** (run with `python3 -I`; pandas compared with the SQL set operators as sorted lists, NULL and NaN shown as None and first)
```python
# Q29: INTERSECT / EXCEPT versus joins and EXISTS; NULL and duplicate behaviour; pandas isin and merge
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers_2024(customer_id INTEGER);
CREATE TABLE customers_2025(customer_id INTEGER);
INSERT INTO customers_2024 VALUES (1),(2),(3),(3),(NULL);
INSERT INTO customers_2025 VALUES (2),(3),(4),(NULL);
""")
def sql(q): return [r[0] for r in con.execute(q).fetchall()]
# sql:both
SQL_BOTH = "SELECT customer_id FROM customers_2024 INTERSECT SELECT customer_id FROM customers_2025 ORDER BY 1"
# end
# sql:only24
SQL_ONLY24 = "SELECT customer_id FROM customers_2024 EXCEPT SELECT customer_id FROM customers_2025 ORDER BY 1"
# end
# sql:only25
SQL_ONLY25 = "SELECT customer_id FROM customers_2025 EXCEPT SELECT customer_id FROM customers_2024 ORDER BY 1"
# end
# sql:join_both
SQL_JOIN_BOTH = """
SELECT DISTINCT a.customer_id FROM customers_2024 a
JOIN customers_2025 b ON b.customer_id = a.customer_id ORDER BY 1
"""
# end
# sql:exists_only24
SQL_EX_ONLY24 = """
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id = a.customer_id) ORDER BY 1
"""
# end
# sql:null_safe
SQL_NULL_SAFE = """
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id IS a.customer_id) ORDER BY 1
"""
# end
both, only24, only25 = sql(SQL_BOTH), sql(SQL_ONLY24), sql(SQL_ONLY25)
print("INTERSECT:", both, "| 2024 only (EXCEPT):", only24, "| 2025 only (EXCEPT):", only25)
print("plain JOIN without DISTINCT, row count:", sql("SELECT COUNT(*) FROM customers_2024 a JOIN customers_2025 b ON b.customer_id = a.customer_id")[0])
print("JOIN + DISTINCT:", sql(SQL_JOIN_BOTH), "(NULL dropped by =)")
print("NOT EXISTS, 2024 only:", sql(SQL_EX_ONLY24), "(NULL kept: no equal row exists)")
print("NOT EXISTS with IS (null-safe):", sql(SQL_NULL_SAFE))
print("UNION ALL row count:", sql("SELECT COUNT(*) FROM (SELECT customer_id FROM customers_2024 UNION ALL SELECT customer_id FROM customers_2025)")[0],
      "| UNION:", sql("SELECT customer_id FROM customers_2024 UNION SELECT customer_id FROM customers_2025 ORDER BY 1"))
print("INTERSECT ALL in SQLite 3.45:", end=" ")
try: con.execute("SELECT customer_id FROM customers_2024 INTERSECT ALL SELECT customer_id FROM customers_2025").fetchall(); print("ok")
except sqlite3.Error as e: print("error:", e)

c24 = pd.read_sql_query("SELECT * FROM customers_2024", con)["customer_id"]
c25 = pd.read_sql_query("SELECT * FROM customers_2025", con)["customer_id"]
def lst(s): return [None if pd.isna(v) else int(v) for v in s.sort_values(na_position="first")]
# pd:isin
in_both = c24[c24.isin(c25)].drop_duplicates()
only_24 = c24[~c24.isin(c25)].drop_duplicates()
only_25 = c25[~c25.isin(c24)].drop_duplicates()
# end
# pd:merge
k24, k25 = c24.drop_duplicates().to_frame(), c25.drop_duplicates().to_frame()
mm = k24.merge(k25, on="customer_id", how="outer", indicator=True, validate="one_to_one")
m_both = mm.loc[mm["_merge"] == "both", "customer_id"]
m_only24 = mm.loc[mm["_merge"] == "left_only", "customer_id"]
m_only25 = mm.loc[mm["_merge"] == "right_only", "customer_id"]
# end
assert lst(in_both) == lst(m_both) == both == [None, 2, 3]
assert lst(only_24) == lst(m_only24) == only24 == [1]
assert lst(only_25) == lst(m_only25) == only25 == [4]
print("\npandas isin and merge(outer, indicator) == INTERSECT / EXCEPT (NULL/NaN first, duplicates removed)")
print("pandas in both:", lst(in_both), "| 2024 only:", lst(only_24), "| 2025 only:", lst(only_25))
print("asserts passed")
```

**Output (my run):**
```text
INTERSECT: [None, 2, 3] | 2024 only (EXCEPT): [1] | 2025 only (EXCEPT): [4]
plain JOIN without DISTINCT, row count: 3
JOIN + DISTINCT: [2, 3] (NULL dropped by =)
NOT EXISTS, 2024 only: [None, 1] (NULL kept: no equal row exists)
NOT EXISTS with IS (null-safe): [1]
UNION ALL row count: 9 | UNION: [None, 1, 2, 3, 4]
INTERSECT ALL in SQLite 3.45: error: near "ALL": syntax error

pandas isin and merge(outer, indicator) == INTERSECT / EXCEPT (NULL/NaN first, duplicates removed)
pandas in both: [None, 2, 3] | 2024 only: [1] | 2025 only: [4]
asserts passed
```

**Edge cases:**
- **Set operators and NULL:** `INTERSECT` and `EXCEPT` treat NULLs as equal ("not distinct"), so NULL appeared in the intersection and disappeared from the 2024-only result. Joins and `EXISTS` use `=`, where NULL never matches.
- **A surprise worth remembering:** `NOT EXISTS` for "2024 only" returned `[None, 1]`, `EXCEPT` returned `[1]`. The difference is only the NULL row. Using `IS` (SQLite null-safe equality) in the subquery gave `[1]` again.
- **Duplicates:** set operators return distinct rows; a join repeats a row once per match (3 rows for 2 customers). `DISTINCT` fixes that but hides real duplicate rows; if you need multiplicity, you want `INTERSECT ALL` or `EXCEPT ALL`, which SQLite 3.45 rejected (`near "ALL": syntax error`). They exist in PostgreSQL (from memory, not executed).
- **Column count and types** must match across the two SELECTs.
- **pandas:** `isin` and `merge` match NaN with NaN, so pandas agreed with `INTERSECT` here, not with the join. Duplicates must be removed explicitly (`drop_duplicates`).

**Then explain:**
- **Set operators compare whole rows.** With one column it is the key; with several columns all of them must match, so for "same customer" on wider tables use a join or `EXISTS` on the key instead.
- **Join/EXISTS forms:** `EXISTS` is the semi-join (in both years) and `NOT EXISTS` the anti-join (only one year). They keep the left table's columns and its duplicates, and they let you select other columns, which set operators cannot.
- **Dialects (hedged, not executed here):** Oracle calls `EXCEPT` `MINUS` (newer Oracle versions also accept `EXCEPT`, I believe, check the manual). PostgreSQL, SQL Server, BigQuery and Snowflake have `INTERSECT` and `EXCEPT` (BigQuery requires `DISTINCT` explicitly, from memory). MySQL added `INTERSECT` and `EXCEPT` only in 8.0.31, so older versions need joins or `EXISTS`. Check the version you run.
- **pandas:** the three results above come from `isin` (a filter on one column) or an outer merge of the de-duplicated keys with `indicator=True` (`both`, `left_only`, `right_only`), which gives all three groups in one pass. `validate="one_to_one"` confirms the keys are unique after `drop_duplicates`.

**Follow-ups:**
- *Why use EXISTS if INTERSECT is shorter?* You can return other columns, and you control the NULL treatment.
- *What about a union of both years?* `UNION` de-duplicates (all five distinct values above, including NULL); `UNION ALL` keeps 9 rows.
- *How would you do customers in both years for a composite key?* Compare the full tuple (`INTERSECT` on both columns) or join on both columns.

**Common mistakes:**
- Assuming `INTERSECT` and an inner join return the same thing when NULLs or duplicates are present.
- Expecting `EXCEPT` to preserve duplicates.
- Mismatched column counts or order between the two SELECTs.
- Using `EXCEPT` on MySQL older than 8.0.31 (hedged) or `MINUS` on an engine that does not have it.

### Q30 ⭐⭐ 🟡 Generate a complete grid with a CROSS JOIN: stores(store_id, store_name), calendar(day) and sales(store_id, sale_date, amount), where days with no sales have no rows. Produce one row per store per day with 0 for no sales. Explain the CROSS JOIN then LEFT JOIN pattern, why aggregating after the left join is correct, and how to fill dates without a calendar table (hedge: recursive CTE or GENERATE_SERIES is another part). Give pandas how='cross' or MultiIndex.from_product with reindex.
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Build the grid first with `stores CROSS JOIN calendar` (every store with every day), LEFT JOIN `sales` onto it on both store and date, then `GROUP BY store, day` with `COALESCE(SUM(amount), 0)`; the grid fixes the grain at one row per store per day, so empty days survive.

**Schema and sample data:**
```sql
CREATE TABLE stores(store_id INTEGER PRIMARY KEY, store_name TEXT);
CREATE TABLE calendar(day TEXT PRIMARY KEY);
CREATE TABLE sales(store_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO stores VALUES (1,'North'),(2,'South');
INSERT INTO calendar VALUES ('2024-01-01'),('2024-01-02'),('2024-01-03');
INSERT INTO sales VALUES (1,'2024-01-01',10),(1,'2024-01-01',5),(2,'2024-01-03',7);
```

**SQL answer:** (same text as in the Code block)
```sql
SELECT st.store_id, st.store_name, c.day, COALESCE(SUM(s.amount), 0) AS total
FROM stores st
CROSS JOIN calendar c
LEFT JOIN sales s ON s.store_id = st.store_id AND s.sale_date = c.day
GROUP BY st.store_id, st.store_name, c.day
ORDER BY st.store_id, c.day
```
Without a calendar table, one option is a recursive CTE for the days (it ran on SQLite 3.45 in the Code block, but recursive CTEs are Part 9, and `GENERATE_SERIES` in PostgreSQL is not executed here):
```sql
WITH RECURSIVE days(day) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(day, '+1 day') FROM days WHERE day < '2024-01-03')
SELECT day FROM days
```

**pandas answer:** (same text as in the Code block)
```python
# cross merge, aggregate sales to one row per store and day, merge, fill
grid = stores.merge(calendar, how="cross")
daily = sales.groupby(["store_id", "sale_date"], as_index=False).agg(total=("amount", "sum"))
p_cross = (grid.merge(daily, left_on=["store_id", "day"], right_on=["store_id", "sale_date"],
                      how="left", validate="one_to_one")
           .assign(total=lambda d: d["total"].fillna(0).astype("int64"))
           .loc[:, ["store_id", "store_name", "day", "total"]])
```
```python
# MultiIndex.from_product + reindex
idx = pd.MultiIndex.from_product([stores["store_id"], calendar["day"]], names=["store_id", "day"])
p_re = (sales.groupby(["store_id", "sale_date"])["amount"].sum().rename_axis(["store_id", "day"])
        .reindex(idx, fill_value=0).reset_index(name="total")
        .merge(stores, on="store_id")[["store_id", "store_name", "day", "total"]])
```

**Example:** Two stores x three days = 6 grid rows. North sold 10 and 5 on 1 Jan, so the LEFT JOIN brings two sales rows onto the (North, 1 Jan) grid row and `SUM` gives 15; North has no sales on 2 and 3 Jan, so the LEFT JOIN gives one row with NULL amount and `COALESCE(SUM(NULL), 0)` gives 0. South sold 7 on 3 Jan and nothing on the other two days. Six rows come out: 15, 0, 0, 0, 0, 7.

**Code:** (run with `python3 -I`; compared as lists of (store_id, store_name, day, total) sorted by store_id, day)
```python
# Q30: one row per store per day: CROSS JOIN then LEFT JOIN then aggregate; pandas cross merge / from_product
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE stores(store_id INTEGER PRIMARY KEY, store_name TEXT);
CREATE TABLE calendar(day TEXT PRIMARY KEY);
CREATE TABLE sales(store_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO stores VALUES (1,'North'),(2,'South');
INSERT INTO calendar VALUES ('2024-01-01'),('2024-01-02'),('2024-01-03');
INSERT INTO sales VALUES (1,'2024-01-01',10),(1,'2024-01-01',5),(2,'2024-01-03',7);
""")
# sql:main
SQL_MAIN = """
SELECT st.store_id, st.store_name, c.day, COALESCE(SUM(s.amount), 0) AS total
FROM stores st
CROSS JOIN calendar c
LEFT JOIN sales s ON s.store_id = st.store_id AND s.sale_date = c.day
GROUP BY st.store_id, st.store_name, c.day
ORDER BY st.store_id, c.day
"""
# end
# sql:cte
SQL_CTE = """
WITH RECURSIVE days(day) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(day, '+1 day') FROM days WHERE day < '2024-01-03')
SELECT day FROM days
"""
# end
# sql:wrong
SQL_WRONG = """
SELECT st.store_id, c.day, SUM(s.amount) AS total
FROM stores st CROSS JOIN calendar c
LEFT JOIN sales s ON s.store_id = st.store_id AND s.sale_date = c.day
WHERE s.amount > 0
GROUP BY st.store_id, c.day
"""
# end
sql_main = [tuple(r) for r in con.execute(SQL_MAIN).fetchall()]
for r in sql_main: print(r)
print("recursive CTE days:", [r[0] for r in con.execute(SQL_CTE)], "== calendar:", [r[0] for r in con.execute("SELECT day FROM calendar ORDER BY day")])
print("WHERE s.amount > 0 version returns", len(con.execute(SQL_WRONG).fetchall()), "rows instead of 6")

stores = pd.read_sql_query("SELECT * FROM stores", con)
calendar = pd.read_sql_query("SELECT * FROM calendar", con)
sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:cross
grid = stores.merge(calendar, how="cross")
daily = sales.groupby(["store_id", "sale_date"], as_index=False).agg(total=("amount", "sum"))
p_cross = (grid.merge(daily, left_on=["store_id", "day"], right_on=["store_id", "sale_date"],
                      how="left", validate="one_to_one")
           .assign(total=lambda d: d["total"].fillna(0).astype("int64"))
           .loc[:, ["store_id", "store_name", "day", "total"]])
# end
# pd:reindex
idx = pd.MultiIndex.from_product([stores["store_id"], calendar["day"]], names=["store_id", "day"])
p_re = (sales.groupby(["store_id", "sale_date"])["amount"].sum().rename_axis(["store_id", "day"])
        .reindex(idx, fill_value=0).reset_index(name="total")
        .merge(stores, on="store_id")[["store_id", "store_name", "day", "total"]])
# end
def norm(df): return [tuple(r) for r in df.sort_values(["store_id", "day"]).itertuples(index=False, name=None)]
assert norm(p_cross) == sql_main
assert norm(p_re) == sql_main
print("\npandas cross merge == SQL; from_product + reindex == SQL (sorted by store_id, day)")
print("total dtype after fillna(0) before the cast:",
      grid.merge(daily, left_on=["store_id", "day"], right_on=["store_id", "sale_date"], how="left")["total"].fillna(0).dtype)
print("grid rows:", len(grid), "= stores x days =", len(stores), "*", len(calendar))
print("asserts passed")
```

**Output (my run):**
```text
(1, 'North', '2024-01-01', 15)
(1, 'North', '2024-01-02', 0)
(1, 'North', '2024-01-03', 0)
(2, 'South', '2024-01-01', 0)
(2, 'South', '2024-01-02', 0)
(2, 'South', '2024-01-03', 7)
recursive CTE days: ['2024-01-01', '2024-01-02', '2024-01-03'] == calendar: ['2024-01-01', '2024-01-02', '2024-01-03']
WHERE s.amount > 0 version returns 2 rows instead of 6

pandas cross merge == SQL; from_product + reindex == SQL (sorted by store_id, day)
total dtype after fillna(0) before the cast: float64
grid rows: 6 = stores x days = 2 * 3
asserts passed
```

**Edge cases:**
- **Aggregating after the join is correct:** the grid row is the grain. Several sales rows on the same day collapse into one total through the `GROUP BY`. If you aggregated sales first and then joined, that also works as long as the sales are one row per store per day (the `validate="one_to_one"` in the pandas version checks this).
- **A filter on `sales` in WHERE breaks it:** `WHERE s.amount > 0` turned the LEFT JOIN into an inner join and returned 2 rows instead of 6. Put sale conditions in the `ON` clause (Q3).
- **Sum of nothing:** `SUM` of all-NULL is NULL in SQL, hence the `COALESCE`. pandas `sum` of an empty group is 0, but after a left merge the missing values are NaN, so `fillna(0)` is needed.
- **dtype after `fillna`:** the column was `float64` (printed before the cast); I cast back to `int64`. `reindex(fill_value=0)` kept it integer.
- **Days in `sales` that are not in the calendar** disappear from the grid; that is usually a data quality check worth running.
- **Time zones or timestamps:** truncate to a date before joining; a datetime never equals a date key (not run here).

**Then explain:**
- **Why CROSS JOIN first:** a LEFT JOIN can only keep rows that exist on its left side. You need a row for every (store, day) before sales are attached, and a cross join produces exactly that.
- **Cost:** the grid has stores x days rows, so a thousand stores and a year of days is 365,000 rows; fine, but compute it before you run it (Q31).
- **No calendar table:** generate days (recursive CTE, or `GENERATE_SERIES` in PostgreSQL, hedged and not executed here), or keep a permanent calendar table; a calendar table also carries week, month and holiday columns.
- **pandas:** `how="cross"` is the same product. `MultiIndex.from_product` plus `reindex` builds the same grid without a merge and fills missing combinations in one step.

**Follow-ups:**
- *What if I only want days that stores were open?* Join to an `open_days` table instead of the full calendar.
- *How would you also show the previous day's total?* That needs window functions (Part 5).
- *How would you fill missing days in pandas time series?* `asfreq` or `resample` on a datetime index (not run here).

**Common mistakes:**
- Starting from `sales` and expecting zero rows.
- Filtering on the sales table in WHERE.
- `COUNT(*)` instead of `COUNT(s.sale_date)` when counting sales per day (counts the grid row as one sale).
- Forgetting that `SUM` over no rows is NULL.

### Q31 ⭐⭐ 🟡 Cartesian product pitfalls: a three-table query FROM orders o, customers c, products p WHERE o.customer_id = c.customer_id forgets the products condition. Explain the row explosion (rows multiply), how to detect it (row count vs expected, COUNT(*) vs COUNT(DISTINCT order_id)), why comma joins invite this, why explicit JOIN ... ON is safer, and when a cross join is intentional. Show the pandas how='cross' memory risk.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Forget one join condition in a comma join and the missing table is cross-joined, so rows multiply by its row count (5 orders became 20 rows with 4 products) and every `SUM` is inflated by the same factor; catch it by comparing `COUNT(*)` with `COUNT(DISTINCT order_id)` and use explicit `JOIN ... ON` so a missing condition is visible.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra');
INSERT INTO products VALUES (10,'Pen'),(20,'Ink'),(30,'Pad'),(40,'Cap');
INSERT INTO orders VALUES (1,1,10,100),(2,1,20,200),(3,2,10,50),(4,3,30,70),(5,2,40,30);
```

**SQL answer:** (same text as in the Code block). The buggy query, which forgets `o.product_id = p.product_id`:
```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o, customers c, products p
WHERE o.customer_id = c.customer_id
```
The fixed query:
```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
```

**pandas answer:** (same text as in the Code block)
```python
# the bug: a cross merge with no key
p_bad = orders.merge(customers, on="customer_id").merge(products, how="cross")
```
```python
# the fix, with validate so a duplicated product key would raise
p_main = orders.merge(customers, on="customer_id").merge(products, on="product_id", validate="many_to_one")
```

**Example:** Five orders, three customers, four products. The comma join pairs each order with its customer (condition present), but with all four products (no condition): 5 x 4 = 20 rows. `COUNT(DISTINCT order_id)` is still 5. Revenue is 1800 instead of the true 450, because each amount is repeated four times: 450 x 4 = 1800. The ratio `COUNT(*) / COUNT(DISTINCT order_id)` = 4 equals the number of products, which points straight at the missing table.

**Code:** (run with `python3 -I`; compares the (rows, distinct orders, revenue) triple from SQL with pandas for both the buggy and the fixed version)
```python
# Q31: cartesian product pitfall: forgotten join condition, detection, and the pandas cross-merge risk
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra');
INSERT INTO products VALUES (10,'Pen'),(20,'Ink'),(30,'Pad'),(40,'Cap');
INSERT INTO orders VALUES (1,1,10,100),(2,1,20,200),(3,2,10,50),(4,3,30,70),(5,2,40,30);
""")
# sql:bad
SQL_BAD = """
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o, customers c, products p
WHERE o.customer_id = c.customer_id
"""
# end
# sql:main
SQL_MAIN = """
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
"""
# end
bad = con.execute(SQL_BAD).fetchone()
good = con.execute(SQL_MAIN).fetchone()
print("comma join, missing condition: rows, distinct orders, revenue =", bad)
print("explicit JOIN ... ON:          rows, distinct orders, revenue =", good)
print("n_rows / n_orders =", bad[0] // bad[1], "= number of products (", con.execute("SELECT COUNT(*) FROM products").fetchone()[0], ")")
try:
    con.execute("SELECT * FROM orders o JOIN customers c")  # no ON
    print("JOIN without ON in SQLite: accepted (it behaves as a cross join)")
except sqlite3.Error as e:
    print("JOIN without ON in SQLite: error:", e)

orders = pd.read_sql_query("SELECT * FROM orders", con)
customers = pd.read_sql_query("SELECT * FROM customers", con)
products = pd.read_sql_query("SELECT * FROM products", con)
# pd:bad
p_bad = orders.merge(customers, on="customer_id").merge(products, how="cross")
# end
# pd:main
p_main = orders.merge(customers, on="customer_id").merge(products, on="product_id", validate="many_to_one")
# end
assert (len(p_bad), p_bad["order_id"].nunique(), int(p_bad["amount"].sum())) == bad
assert (len(p_main), p_main["order_id"].nunique(), int(p_main["amount"].sum())) == good
print("pandas cross merge rows:", len(p_bad), "| correct merge rows:", len(p_main), "(both equal SQL)")
try:
    orders.merge(customers, how="cross", on="customer_id")
except pd.errors.MergeError as e:
    print("pandas: how='cross' with on= ->", type(e).__name__, "|", e)
# the memory risk: pure arithmetic, nothing is allocated
for n_left, n_right in [(5, 4), (100_000, 100_000), (1_000_000, 50_000)]:
    rows = n_left * n_right
    print(f"cross merge {n_left:>9,} x {n_right:>7,} = {rows:>16,} rows (not run); at 16 bytes/row if two 8-byte columns: {rows*16/1e9:,.1f} GB")
print("asserts passed")
```

**Output (my run):**
```text
comma join, missing condition: rows, distinct orders, revenue = (20, 5, 1800)
explicit JOIN ... ON:          rows, distinct orders, revenue = (5, 5, 450)
n_rows / n_orders = 4 = number of products ( 4 )
JOIN without ON in SQLite: accepted (it behaves as a cross join)
pandas cross merge rows: 20 | correct merge rows: 5 (both equal SQL)
pandas: how='cross' with on= -> MergeError | Can not pass on, right_on, left_on or set right_index=True or left_index=True
cross merge         5 x       4 =               20 rows (not run); at 16 bytes/row if two 8-byte columns: 0.0 GB
cross merge   100,000 x 100,000 =   10,000,000,000 rows (not run); at 16 bytes/row if two 8-byte columns: 160.0 GB
cross merge 1,000,000 x  50,000 =   50,000,000,000 rows (not run); at 16 bytes/row if two 8-byte columns: 800.0 GB
asserts passed
```

**Edge cases:**
- **How to detect it:** compare the row count with what you expect for the grain (5 orders, 20 rows), compare `COUNT(*)` with `COUNT(DISTINCT order_id)`, and sanity check a total against the single table (`SELECT SUM(amount) FROM orders` = 450).
- **Comma joins invite it:** with `FROM a, b, c WHERE ...`, a missing predicate is not a syntax error, and the conditions are far from the tables. In `JOIN ... ON` every join has its own condition next to it. (Modern engines treat both the same; this is a readability and safety argument, not a speed one.)
- **A forgotten `ON` in SQLite** was accepted and produced a cross join (printed in the output). Some other engines raise a syntax error for `JOIN` without `ON`; not executed here, so check yours.
- **A condition that does not reduce rows** is also a quiet cartesian: `ON 1 = 1`, or a condition that is true for every pair.
- **Intentional cross joins** exist: a grid of every store and every day (Q30), every pair of values in a test matrix, or attaching a one-row parameter table to every row. Write them with `CROSS JOIN` so the intent is visible.
- **Empty table:** a cross join with an empty table returns zero rows, so a forgotten condition can also make the result vanish.

**Then explain:**
- **Rows multiply:** n rows x m rows gives n x m rows. Three unconstrained tables of 1,000 rows each give a billion rows.
- **Inflated measures:** every `SUM` and `COUNT(*)` is multiplied by the factor; `AVG` can look plausible, so it is easy to miss. `COUNT(DISTINCT key)` is the one that stays right, which is why the comparison works as a detector (it is no fix, see Q13).
- **pandas memory risk:** `merge(how="cross")` materializes every pair at once. The lines in the output are plain arithmetic (not run): 100,000 x 100,000 is 10 billion rows. The size estimate assumes just two 8-byte columns, a lower bound; real frames have more columns, so the true memory is larger. `validate=` is no guard here: in a one-off check I ran, `validate="one_to_one"` on a cross merge raised `MergeError` because the hidden constant key is repeated, and passing `on=` with `how="cross"` raises as printed (see Q9 for `validate` on keyed merges).
- **Guard before you run:** compute `len(a) * len(b)` first and refuse above a limit, or filter both sides before crossing.

**Follow-ups:**
- *How would you spot this in a query plan?* A join with no predicate, shown as a nested loop over a full scan; EXPLAIN belongs to Part 11 and is not executed here.
- *Does `JOIN` without ON behave like CROSS JOIN everywhere?* No, not guaranteed: SQLite accepted it; check each engine's behaviour (not executed).
- *How do you bring a single parameter row into every row?* `CROSS JOIN params` (one row), which is a safe cross join.

**Common mistakes:**
- Fixing inflated totals with `SUM(DISTINCT amount)`, which also drops legitimate equal amounts.
- Joining on the wrong column pair (customer_id to product_id), which gives a plausible but wrong result.
- Reading a correct-looking small test as proof; row-count checks are the real test.
- Running `how="cross"` on large frames "to see what happens".

### Q32 ⭐⭐ 🟡 Simulate FULL OUTER JOIN with UNION: a_users(user_id, name) and b_users(user_id, email), for an engine without FULL JOIN (MySQL; hedged). Write LEFT JOIN UNION RIGHT JOIN, then the better version (LEFT JOIN UNION ALL anti-join of the right table), and explain why UNION ALL is correct there, what UNION de-duplication could wrongly collapse, and the cost of the extra scan.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Without FULL JOIN, write `LEFT JOIN` for everything on the left, then `UNION ALL` the right-table rows that have no match on the left (an anti-join); `LEFT JOIN UNION RIGHT JOIN` also works but `UNION` de-duplicates, so it can collapse legitimate duplicate rows, and it scans both sides twice.

**Schema and sample data:**
```sql
CREATE TABLE a_users(user_id INTEGER, name TEXT);
CREATE TABLE b_users(user_id INTEGER, email TEXT);
INSERT INTO a_users VALUES (1,'Ann'),(2,'Bob'),(3,'Cy'),(5,'Eve'),(5,'Eve');
INSERT INTO b_users VALUES (2,'bob@x.com'),(3,'cy@x.com'),(4,'di@x.com');
```
(User 5 is deliberately loaded twice in `a_users` with no match in `b_users`, to show what `UNION` does to duplicates.)

**SQL answer:** (same text as in the Code block)
The better version, LEFT JOIN plus `UNION ALL` of the right-only rows:
```sql
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION ALL
SELECT b.user_id, NULL, b.email FROM b_users b
WHERE NOT EXISTS (SELECT 1 FROM a_users a WHERE a.user_id = b.user_id)
ORDER BY 1, 2, 3
```
The classic version (`LEFT JOIN UNION RIGHT JOIN`), which SQLite 3.45.1 accepts because it supports RIGHT JOIN (confirmed by running):
```sql
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION
SELECT b.user_id, a.name, b.email FROM a_users a RIGHT JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
```
The native form to compare with (SQLite 3.45.1 ran it):
```sql
SELECT COALESCE(a.user_id, b.user_id) AS user_id, a.name, b.email
FROM a_users a FULL OUTER JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
```
MySQL has no FULL OUTER JOIN (hedged: its 8.4 JOIN documentation shows only LEFT and RIGHT; I did not run MySQL), which is why these emulations exist.

**pandas answer:** (same text as in the Code block)
```python
left = a.merge(b, on="user_id", how="left")
b_only = b[~b["user_id"].isin(a["user_id"])].assign(name=None)
p_main = pd.concat([left, b_only[["user_id", "name", "email"]]], ignore_index=True)
```
```python
# the direct equivalent
p_full = a.merge(b, on="user_id", how="outer", indicator=True)
```

**Example:** `a_users` has users 1, 2, 3, 5, 5; `b_users` has 2, 3, 4. A FULL JOIN returns 6 rows: 1 (name only), 2 and 3 (matched), 4 (email only), and 5 twice (name only). The LEFT JOIN part returns users 1, 2, 3, 5, 5 (five rows). The anti-join part returns user 4 (not in `a_users`). `UNION ALL` of the two gives 6 rows and matches the FULL JOIN. With `UNION`, the two identical rows `(5, Eve, NULL)` collapse into one, giving 5 rows, a silently wrong result.

**Code:** (run with `python3 -I`; the three SQL versions are compared and pandas is compared with the native FULL JOIN as sorted rows (user_id, name, email), NULL as None)
```python
# Q32: simulate FULL OUTER JOIN: LEFT JOIN UNION RIGHT JOIN, and LEFT JOIN UNION ALL anti-join; vs native FULL JOIN
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
print("sqlite", sqlite3.sqlite_version)
con.executescript("""
CREATE TABLE a_users(user_id INTEGER, name TEXT);
CREATE TABLE b_users(user_id INTEGER, email TEXT);
INSERT INTO a_users VALUES (1,'Ann'),(2,'Bob'),(3,'Cy'),(5,'Eve'),(5,'Eve');
INSERT INTO b_users VALUES (2,'bob@x.com'),(3,'cy@x.com'),(4,'di@x.com');
""")
# user 5 is in a_users twice (a loaded-twice row), and has no b row
# sql:native
SQL_FULL = """
SELECT COALESCE(a.user_id, b.user_id) AS user_id, a.name, b.email
FROM a_users a FULL OUTER JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
"""
# end
# sql:union
SQL_UNION = """
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION
SELECT b.user_id, a.name, b.email FROM a_users a RIGHT JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
"""
# end
# sql:main
SQL_MAIN = """
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION ALL
SELECT b.user_id, NULL, b.email FROM b_users b
WHERE NOT EXISTS (SELECT 1 FROM a_users a WHERE a.user_id = b.user_id)
ORDER BY 1, 2, 3
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
full, uni, main = sql(SQL_FULL), sql(SQL_UNION), sql(SQL_MAIN)
print("native FULL OUTER JOIN:", len(full), "rows"); [print("  ", r) for r in full]
print("LEFT JOIN UNION RIGHT JOIN:", len(uni), "rows ->", "same as FULL" if uni == full else "DIFFERENT")
print("   FULL has", full.count((5, "Eve", None)), "copies of (5, Eve, None); UNION kept", uni.count((5, "Eve", None)))
print("LEFT JOIN UNION ALL anti-join:", len(main), "rows ->", "same as FULL" if main == full else "DIFFERENT")
assert main == full and uni != full and len(full) - len(uni) == 1

a = pd.read_sql_query("SELECT * FROM a_users", con)
b = pd.read_sql_query("SELECT * FROM b_users", con)
# pd:main
left = a.merge(b, on="user_id", how="left")
b_only = b[~b["user_id"].isin(a["user_id"])].assign(name=None)
p_main = pd.concat([left, b_only[["user_id", "name", "email"]]], ignore_index=True)
# end
# pd:full
p_full = a.merge(b, on="user_id", how="outer", indicator=True)
# end
def norm(df):
    rows = [tuple(None if pd.isna(v) else (int(v) if k == 0 else v) for k, v in enumerate(r))
            for r in df[["user_id", "name", "email"]].itertuples(index=False, name=None)]
    return sorted(rows, key=lambda r: (r[0], r[1] or "", r[2] or ""))
assert norm(p_main) == norm(p_full) == full
print("\npandas concat(left merge, right-only rows) == outer merge == SQL FULL (sorted)")
print("outer merge _merge counts:", p_full["_merge"].value_counts().to_dict())
print("asserts passed")
```

**Output (my run):**
```text
sqlite 3.45.1
native FULL OUTER JOIN: 6 rows
   (1, 'Ann', None)
   (2, 'Bob', 'bob@x.com')
   (3, 'Cy', 'cy@x.com')
   (4, None, 'di@x.com')
   (5, 'Eve', None)
   (5, 'Eve', None)
LEFT JOIN UNION RIGHT JOIN: 5 rows -> DIFFERENT
   FULL has 2 copies of (5, Eve, None); UNION kept 1
LEFT JOIN UNION ALL anti-join: 6 rows -> same as FULL

pandas concat(left merge, right-only rows) == outer merge == SQL FULL (sorted)
outer merge _merge counts: {'left_only': 3, 'both': 2, 'right_only': 1}
asserts passed
```

**Edge cases:**
- **Duplicates:** the example above; `UNION` (and `UNION DISTINCT`) removes duplicate rows, including legitimate ones. A FULL JOIN keeps both Eve rows, so the emulation must too.
- **Why `UNION ALL` is correct:** the two parts cannot overlap. Part 1 holds rows whose key exists in `a_users`; part 2 holds only rows whose key does not. So no row can be produced twice and no de-duplication is needed.
- **Key column in the right part:** take `b.user_id` there. In the `UNION` version, `a.user_id` would be NULL for right-only rows, so I selected `b.user_id` in the second SELECT (the alternative is `COALESCE(a.user_id, b.user_id)` in both).
- **NULL keys:** a NULL `user_id` never matches in the join. In the anti-join, `NOT EXISTS` keeps right rows with a NULL key, as FULL JOIN does. Do not use `NOT IN (SELECT user_id ...)`: one NULL in `a_users` would return no right-only rows (Part 1 Q13).
- **Column order and types** must match in every SELECT of the union (the NULL literal for `name` is typed by the other branch).
- **Cost:** `b_users` is read twice (in the LEFT JOIN and again in the anti-join) and `a_users` is probed twice. With an index on the join key it is cheap; without one it is two full passes. Engine specific and not measured here.

**Then explain:**
- **Why not `UNION`:** it costs a sort or hash to de-duplicate the whole result, and it changes the answer when duplicates are real. `UNION ALL` does neither.
- **Why the anti-join form beats `LEFT UNION RIGHT`:** it joins `b_users` once and filters instead of re-joining everything; it is also exact on duplicates.
- **Native FULL JOIN:** SQLite 3.45.1 ran it; PostgreSQL, SQL Server, Oracle, Snowflake and BigQuery support it (from memory, not executed). Use it when available; it is shorter and cannot make this mistake.
- **pandas:** `how="outer"` is the FULL JOIN. The concat version mirrors the SQL emulation (left merge plus right-only rows via `~isin`) and matched the outer merge; the outer merge's `_merge` counts show 3 left only, 2 both, 1 right only.

**Follow-ups:**
- *Could you add a `source` column?* Yes: `'a_only'`, `'both'`, `'b_only'` by testing which side's key IS NULL (Q16 does this with FULL JOIN).
- *What about MySQL's RIGHT JOIN?* It exists in MySQL, so `LEFT JOIN UNION RIGHT JOIN` runs there; the anti-join form is still preferred (hedged, not executed).
- *Do you ever need UNION instead of UNION ALL here?* Only if the sources can produce duplicate result rows that you also want collapsed, which is a different requirement from a FULL JOIN.

**Common mistakes:**
- Using `UNION` and losing duplicate rows (or paying the de-duplication cost for nothing).
- Using the wrong key column in the right-only branch, so the user id is NULL.
- A `NOT IN` anti-join with NULLs in the left key.
- Forgetting that a FULL JOIN is not supported in the engine and getting a syntax error in production.

### Q33 ⭐⭐ 🟡 Consecutive rows with a self join (join approach only, no window functions): logs(id, num) with consecutive ids. Find numbers that appear at least three times in a row (the LeetCode Consecutive Numbers idea) by joining the table to itself on id + 1 and id + 2. Say what breaks when ids have gaps, why DISTINCT is needed, and the pandas shift-free equivalent using merge with an offset key.
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Join `logs` to itself three times, `l2.id = l1.id + 1` and `l3.id = l1.id + 2` with the same `num` on all three, and select `DISTINCT num`; it works only when ids are gap-free, and DISTINCT is needed because a run longer than three produces several overlapping triples.

**Schema and sample data:**
```sql
CREATE TABLE logs(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs VALUES (1,1),(2,1),(3,1),(4,1),(5,2),(6,3),(7,3),(8,2),(9,2),(10,2);
CREATE TABLE logs_gap(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs_gap VALUES (1,7),(2,7),(4,7),(5,9);   -- id 3 was deleted
```

**SQL answer:** (same text as in the Code block)
```sql
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l2.id = l1.id + 1 AND l2.num = l1.num
JOIN logs l3 ON l3.id = l1.id + 2 AND l3.num = l1.num
ORDER BY 1
```

**pandas answer:** (same text as in the Code block). No `shift`: shift the key instead and merge.
```python
def consecutive(df):
    n1 = df.assign(id=df["id"] - 1).rename(columns={"num": "num1"})     # row at id+1, keyed by this row's id
    n2 = df.assign(id=df["id"] - 2).rename(columns={"num": "num2"})     # row at id+2
    m = (df.merge(n1, on="id", validate="one_to_one")
           .merge(n2, on="id", validate="one_to_one"))
    return sorted(m.loc[(m["num"] == m["num1"]) & (m["num"] == m["num2"]), "num"].unique().tolist())
```

**Example:** `logs` has 1, 1, 1, 1 at ids 1 to 4, then 2, 3, 3, 2, 2, 2. Starting from id 1: id 2 and id 3 also hold 1, so a triple exists. Starting from id 2: ids 3 and 4 hold 1, a second triple. So the number 1 is returned twice without `DISTINCT` (the output shows `[1, 1, 2]`). Starting from id 8: ids 9 and 10 hold 2, so 2 qualifies. The 3 appears only twice in a row (ids 6 and 7), so it fails. Answer with `DISTINCT`: 1 and 2.

**Code:** (run with `python3 -I`; SQL and pandas compared as sorted lists of numbers, both for `logs` and for the gap table)
```python
# Q33: Consecutive Numbers with a self join on id+1 and id+2; gaps; DISTINCT; pandas offset-key merge
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE logs(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs VALUES (1,1),(2,1),(3,1),(4,1),(5,2),(6,3),(7,3),(8,2),(9,2),(10,2);
CREATE TABLE logs_gap(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs_gap VALUES (1,7),(2,7),(4,7),(5,9);   -- id 3 was deleted
""")
# sql:main
SQL_MAIN = """
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l2.id = l1.id + 1 AND l2.num = l1.num
JOIN logs l3 ON l3.id = l1.id + 2 AND l3.num = l1.num
ORDER BY 1
"""
# end
SQL_NO_DISTINCT = SQL_MAIN.replace("SELECT DISTINCT", "SELECT")
def sql(q, t="logs"): return [r[0] for r in con.execute(q.replace("logs", t)).fetchall()]
main = sql(SQL_MAIN)
print("with DISTINCT:   ", main)
print("without DISTINCT:", sql(SQL_NO_DISTINCT), "(num 1 appears in two overlapping triples: ids 1-3 and 2-4)")
print("gap table logs_gap (ids 1,2,4 all num 7):", sql(SQL_MAIN, "logs_gap"), "<- misses it, id 3 is missing")

logs = pd.read_sql_query("SELECT * FROM logs", con)
logs_gap = pd.read_sql_query("SELECT * FROM logs_gap", con)
# pd:main
def consecutive(df):
    n1 = df.assign(id=df["id"] - 1).rename(columns={"num": "num1"})     # row at id+1, keyed by this row's id
    n2 = df.assign(id=df["id"] - 2).rename(columns={"num": "num2"})     # row at id+2
    m = (df.merge(n1, on="id", validate="one_to_one")
           .merge(n2, on="id", validate="one_to_one"))
    return sorted(m.loc[(m["num"] == m["num1"]) & (m["num"] == m["num2"]), "num"].unique().tolist())
# end
p_main = consecutive(logs)
assert p_main == main == [1, 2]
assert consecutive(logs_gap) == sql(SQL_MAIN, "logs_gap") == []
print("\npandas offset-key merge:", p_main, "== SQL; gap table:", consecutive(logs_gap))
print("rows after the two inner merges on logs (ids that have id+1 and id+2):", len(
    logs.merge(logs.assign(id=logs["id"] - 1), on="id").merge(logs.assign(id=logs["id"] - 2), on="id")))
print("asserts passed")
```

**Output (my run):**
```text
with DISTINCT:    [1, 2]
without DISTINCT: [1, 1, 2] (num 1 appears in two overlapping triples: ids 1-3 and 2-4)
gap table logs_gap (ids 1,2,4 all num 7): [] <- misses it, id 3 is missing

pandas offset-key merge: [1, 2] == SQL; gap table: []
rows after the two inner merges on logs (ids that have id+1 and id+2): 8
asserts passed
```

**Edge cases:**
- **Gaps in ids:** in `logs_gap`, the rows with ids 1, 2 and 4 all hold 7 and are consecutive in the table, but `id + 2` does not exist for id 2. The query returned nothing. The join approach assumes ids are exactly `1, 2, 3, ...` (the LeetCode problem states this). If ids can have gaps, number the rows first with `ROW_NUMBER()` (Part 4) or use a window function with `LAG` (Part 5) and compare neighbours by position; not covered in this part.
- **Why DISTINCT:** one run of four equal numbers contains two triples; a run of n has n - 2 triples. `DISTINCT` collapses them.
- **At least three:** runs longer than three qualify, as 1 (four times) did. For exactly three, you would also need to check the neighbours on each side.
- **Ids that are not unique** would multiply the join; the primary key rules this out. In pandas, `validate="one_to_one"` on the shifted frames asserts it.
- **NULL num:** `NULL = NULL` is not TRUE, so NULLs never form a run (not run on the sample).
- **Unsorted ids** do not matter for the join, unlike for window functions.

**Then explain:**
- **Three aliases, one table:** `l1` is the starting row, `l2` the row one id later, `l3` the row two ids later. The two conditions `l2.num = l1.num` and `l3.num = l1.num` say all three values are equal.
- **pandas without `shift`:** subtract the offset from the id of a copy (`id - 1`), so that the row that is really at `id + 1` now carries this row's id and a plain `on="id"` merge lines them up. Two such merges give the three values in one row; the filter does the comparison. `unique()` plays the role of `DISTINCT`. At the edges, ids without `id + 1` or `id + 2` drop out of the inner merges, like in SQL (8 rows survived in my run).
- **Why shift is simpler in practice:** `df["num"].eq(df["num"].shift(1))` is shorter, but depends on the row order being right; the offset-key merge depends on ids instead, which is the same assumption as the SQL join.
- **Generalising to n in a row** needs n - 1 joins; a window-function solution is better (Part 5).

**Follow-ups:**
- *How would you return the start id of each run?* `SELECT l1.id` instead of the number, then group, or use gaps and islands (Part 7).
- *What about "at least 5 times"?* Five aliases, or windows; the self-join gets long.
- *What if the table has no id?* Then there is no order to compare; you must add or define one.

**Common mistakes:**
- Forgetting `DISTINCT`, which returns the same number repeatedly.
- Comparing `l1.num = l2.num` and `l2.num = l3.num` but only `l2.id = l1.id + 1` (missing the third id condition).
- Assuming ids are gap-free after deletes.
- Using `l1.id < l2.id` instead of `id + 1`, which matches rows that are not adjacent.

### Q34 ⭐⭐ 🟡 Many-to-many and duplicate keys in pandas: orders_a(order_id, item) and orders_b(order_id, tag) each repeat some order_id values. Explain why merge returns the Cartesian product of the matching rows per key (2 x 3 = 6), how validate='one_to_one', 'one_to_many' and 'many_to_one' raise MergeError, how to check len(result) against expectations, and the SQL parallel.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** When a key repeats on both sides, merge pairs every left row with every right row for that key, so a key with 2 left rows and 3 right rows gives 2 x 3 = 6 rows; `validate=` makes pandas raise `MergeError` when the key is not unique where you said it should be, and `len(result)` should be checked against the sum of `na * nb` per key.

**Schema and sample data:**
```sql
CREATE TABLE orders_a(order_id INTEGER, item TEXT);
CREATE TABLE orders_b(order_id INTEGER, tag TEXT);
INSERT INTO orders_a VALUES (1,'pen'),(1,'ink'),(2,'book'),(3,'cap');
INSERT INTO orders_b VALUES (1,'gift'),(1,'rush'),(1,'fragile'),(2,'gift'),(4,'promo');
```

**SQL answer:** (same text as in the Code block)
```sql
SELECT a.order_id, a.item, b.tag
FROM orders_a a JOIN orders_b b ON b.order_id = a.order_id
ORDER BY a.order_id, a.item, b.tag
```
SQL has no `validate=`; the equivalent checks are:
```sql
SELECT order_id, COUNT(*) AS n FROM orders_a GROUP BY order_id HAVING COUNT(*) > 1
```
```sql
SELECT SUM(na * nb) FROM
  (SELECT order_id, COUNT(*) AS na FROM orders_a GROUP BY order_id) x
  JOIN (SELECT order_id, COUNT(*) AS nb FROM orders_b GROUP BY order_id) y ON y.order_id = x.order_id
```

**pandas answer:** (same text as in the Code block)
```python
m = a.merge(b, on="order_id", how="inner")
expected = int((a["order_id"].value_counts() * b["order_id"].value_counts()).sum())   # per key: na * nb (inner)
assert len(m) == expected
```
```python
for v in ["one_to_one", "one_to_many", "many_to_one", "many_to_many"]:
    try:
        r = a.merge(b, on="order_id", validate=v)
        print(f"validate={v!r:15} -> ok, {len(r)} rows")
    except pd.errors.MergeError as e:
        print(f"validate={v!r:15} -> MergeError:", str(e).splitlines()[0])
```

**Example:** Order 1 has 2 items (pen, ink) and 3 tags (gift, rush, fragile): the join pairs every item with every tag, 2 x 3 = 6 rows (`pen/gift`, `pen/rush`, `pen/fragile`, `ink/gift`, ...). Order 2 has 1 item and 1 tag: 1 row. Order 3 (only in `a`) and order 4 (only in `b`) have no partner and vanish in an inner merge. Total: 6 + 1 = 7 rows. The check `value_counts() * value_counts()` gives 2 x 3 = 6 and 1 x 1 = 1 for the keys present on both sides, so 7 expected.

**Code:** (run with `python3 -I`; the pandas inner merge is compared with the SQL JOIN as sorted lists of (order_id, item, tag))
```python
# Q34: many-to-many merge in pandas: Cartesian product per key, validate= errors, row-count check, SQL parallel
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders_a(order_id INTEGER, item TEXT);
CREATE TABLE orders_b(order_id INTEGER, tag TEXT);
INSERT INTO orders_a VALUES (1,'pen'),(1,'ink'),(2,'book'),(3,'cap');
INSERT INTO orders_b VALUES (1,'gift'),(1,'rush'),(1,'fragile'),(2,'gift'),(4,'promo');
""")
# sql:main
SQL_MAIN = """
SELECT a.order_id, a.item, b.tag
FROM orders_a a JOIN orders_b b ON b.order_id = a.order_id
ORDER BY a.order_id, a.item, b.tag
"""
# end
# sql:dup
SQL_DUP = """
SELECT order_id, COUNT(*) AS n FROM orders_a GROUP BY order_id HAVING COUNT(*) > 1
"""
# end
# sql:expected
SQL_EXPECTED = """
SELECT SUM(na * nb) FROM
  (SELECT order_id, COUNT(*) AS na FROM orders_a GROUP BY order_id) x
  JOIN (SELECT order_id, COUNT(*) AS nb FROM orders_b GROUP BY order_id) y ON y.order_id = x.order_id
"""
# end
sql_main = [tuple(r) for r in con.execute(SQL_MAIN).fetchall()]
print("SQL join rows:", len(sql_main), "->", sql_main)
print("duplicate keys in orders_a:", con.execute(SQL_DUP).fetchall())
print("expected rows = SUM(na * nb) per key:", con.execute(SQL_EXPECTED).fetchone()[0])

a = pd.read_sql_query("SELECT * FROM orders_a", con)
b = pd.read_sql_query("SELECT * FROM orders_b", con)
# pd:main
m = a.merge(b, on="order_id", how="inner")
expected = int((a["order_id"].value_counts() * b["order_id"].value_counts()).sum())   # per key: na * nb (inner)
assert len(m) == expected
# end
p_main = [tuple(r) for r in m.sort_values(["order_id", "item", "tag"]).itertuples(index=False, name=None)]
assert p_main == sql_main
print("\npandas inner merge rows:", len(m), "== expected", expected, "== SQL", len(sql_main))
print("rows per order_id after the merge:", m["order_id"].value_counts().sort_index().to_dict())

# pd:validate
for v in ["one_to_one", "one_to_many", "many_to_one", "many_to_many"]:
    try:
        r = a.merge(b, on="order_id", validate=v)
        print(f"validate={v!r:15} -> ok, {len(r)} rows")
    except pd.errors.MergeError as e:
        print(f"validate={v!r:15} -> MergeError:", str(e).splitlines()[0])
# end
# validate when one side IS unique
b_unique = b.drop_duplicates("order_id")
r = a.merge(b_unique, on="order_id", validate="many_to_one")
print("\nafter b.drop_duplicates('order_id'): many_to_one ok,", len(r), "rows (orders_a rows 1, 1, 2 matched)")
try:
    a.merge(b_unique, on="order_id", validate="one_to_many")
except pd.errors.MergeError as e:
    print("one_to_many on the same data -> MergeError:", str(e).splitlines()[0])

# how= and indicator for the unmatched keys
o = a.merge(b, on="order_id", how="outer", indicator=True)
print("\nouter merge rows:", len(o), "| _merge:", o["_merge"].value_counts().to_dict())
print("asserts passed")
```

**Output (my run):**
```text
SQL join rows: 7 -> [(1, 'ink', 'fragile'), (1, 'ink', 'gift'), (1, 'ink', 'rush'), (1, 'pen', 'fragile'), (1, 'pen', 'gift'), (1, 'pen', 'rush'), (2, 'book', 'gift')]
duplicate keys in orders_a: [(1, 2)]
expected rows = SUM(na * nb) per key: 7

pandas inner merge rows: 7 == expected 7 == SQL 7
rows per order_id after the merge: {1: 6, 2: 1}
validate='one_to_one'    -> MergeError: Merge keys are not unique in either left or right dataset; not a one-to-one merge.
validate='one_to_many'   -> MergeError: Merge keys are not unique in left dataset; not a one-to-many merge
validate='many_to_one'   -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
validate='many_to_many'  -> ok, 7 rows

after b.drop_duplicates('order_id'): many_to_one ok, 3 rows (orders_a rows 1, 1, 2 matched)
one_to_many on the same data -> MergeError: Merge keys are not unique in left dataset; not a one-to-many merge

outer merge rows: 9 | _merge: {'both': 7, 'left_only': 1, 'right_only': 1}
asserts passed
```

**Edge cases:**
- **Which validate fails:** with duplicates on both sides, `one_to_one` fails (message says not unique in either dataset), `one_to_many` fails (left not unique) and `many_to_one` fails (right not unique); `many_to_many` passes and is the default, so no check happens unless you ask. The messages come from my run on pandas 3.0.5.
- **When one side is unique:** after `b.drop_duplicates("order_id")`, `many_to_one` passed (3 rows), and `one_to_many` on the same data still raised, because the left side has duplicates. Remember the naming: the first word is the left frame, the second is the right frame.
- **validate only looks at the merge keys**, not at whether the result is what you meant. It also does not look at rows without a partner.
- **Unmatched keys:** orders 3 and 4 vanish in the inner merge. `how="outer", indicator=True` kept them: 9 rows, with 7 `both`, 1 `left_only` and 1 `right_only`.
- **NaN keys:** NaN matches NaN in a pandas merge, so many rows with a missing key all pair with each other, a hidden many-to-many (see Q24 and Q6; here the keys have no NaN).
- **Growth is multiplicative:** two frames with 1,000 repeated rows per key give a million per key. Check `len(a)`, `len(b)` and `len(result)` before you continue.

**Then explain:**
- **Why it is a Cartesian product per key:** the join pairs rows, not keys. For each key it returns all combinations of left rows and right rows with that key.
- **How to avoid it:** decide the grain you want. Usually one side should be reduced to one row per key first (`drop_duplicates`, or `groupby` and aggregate), and `validate="one_to_many"` or `"many_to_one"` documents and enforces that.
- **Check the size:** compute the expected count from the key counts (as in the code) and `assert len(result) == expected`; if the number is not what you expect, a key is duplicated somewhere.
- **SQL parallel:** a SQL JOIN does exactly the same (7 rows above). SQL has no `validate` flag; you check uniqueness with `GROUP BY key HAVING COUNT(*) > 1` and compare row counts, or enforce it with a primary key or unique constraint on the table (Q9, Q40).
- **When many-to-many is legitimate:** for example items and tags where you really want every combination. Usually it is a mistake, and the fan-out inflates sums (Q12, Q13).

**Follow-ups:**
- *What does `validate="one_to_one"` check?* That the key is unique in both frames; it raises before the merge result is returned.
- *Does validate cost much?* It checks key uniqueness, which is cheap compared with building a large product (concept; not measured).
- *How do you aggregate before merging?* `b.groupby("order_id")["tag"].agg(list)` or a count per key, then a one-to-one merge.

**Common mistakes:**
- Merging without `validate` and noticing the inflated row count only downstream.
- Mixing up `one_to_many` and `many_to_one` (the first word is the left side).
- Using `drop_duplicates()` on the whole frame instead of on the key, which keeps duplicate keys with different values.
- Expecting `validate` to check anything about unmatched rows.

### Q35 ⭐⭐ 🟡 Key dtype mismatch in pandas merge: customers.customer_id is int64 and orders.customer_id was read from CSV as object (strings, some with trailing spaces) or float64 (because of NaN). Explain the ValueError you get for int versus object, the silent wrong result for strings that look alike, float keys with NaN, and fix with astype('Int64'), str.strip and a post-merge unmatched check. Compare with SQL implicit casting (hedged: engine dependent).
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `merge` never casts a key for you: `int64` against `str` or `object` raises `ValueError`, but text against text, or a mixed `object` column, matches silently wrong, and a `float64` key (because of NaN) merges fine while the NaN rows can never match; so clean the key to one dtype (`str.strip`, `to_numeric`, `astype('Int64')`) and always check the unmatched rows after the merge.

**Schema and sample data:** customers has an `int64` key. The orders CSV has a trailing space on one key (`2 `), a blank key, and an unknown customer (7).
```text
order_id,customer_id
10,1
11,2 
12,3
13,
14,3
15,7
```
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders_raw(order_id INTEGER, customer_id TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders_raw VALUES (10,'1'),(11,'2 '),(12,'3'),(13,NULL),(14,'3'),(15,'7');
```

**SQL answer:** SQL has no dtype error to catch you here, so the point is the explicit cast. `SQL_IMPLICIT` is the lazy join and `SQL_FIX` is the safe one (both run in the Code block):
```sql
SELECT o.order_id, c.name FROM orders_raw o LEFT JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
```
```sql
SELECT o.order_id, CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER) AS customer_id, c.name,
       CASE WHEN c.customer_id IS NULL THEN 'left_only' ELSE 'both' END AS _merge
FROM orders_raw o
LEFT JOIN customers c ON c.customer_id = CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER)
ORDER BY o.order_id
```
`NULLIF(..., '')` matters: in SQLite `CAST('' AS INTEGER)` and `CAST('x' AS INTEGER)` both give 0 (see the output), so without it a blank or junk key silently becomes key 0.

**pandas answer:** read, strip, convert, merge with `indicator=True`, then look at what did not match (same lines as in the Code block):
```py
orders["customer_id"] = pd.to_numeric(orders["customer_id"].str.strip(), errors="coerce").astype("Int64")
p = orders.merge(customers, on="customer_id", how="left", indicator=True)
unmatched = p[p["_merge"] != "both"]
```

**Example:** walk the six order rows through the fixed join. 10 has key 1, so Asha. 11 has `'2 '`, which strips to 2, so Ben. 12 has 3, so Chitra. 13 is blank, so NaN, so no match. 14 is 3 again, so Chitra. 15 has key 7, and there is no customer 7, so no match. Unmatched orders are therefore 13 and 15. Without the strip, text against text also loses order 11, giving 11, 13 and 15, and nothing warns you.

**Code:** run with `python3 -I`; the SQL and pandas fixed results are compared sorted by `order_id` with `assert_frame_equal`.
```python
# Q35: merge key dtype mismatch (int64 vs str/object/float64), silent drops, fix, SQLite implicit casting
import io
import sqlite3
import warnings
import pandas as pd

CSV = "order_id,customer_id\n10,1\n11,2 \n12,3\n13,\n14,3\n15,7\n"   # '2 ' has a trailing space, 13 has no key, 15 is unknown
customers = pd.DataFrame({"customer_id": [1, 2, 3, 4], "name": ["Asha", "Ben", "Chitra", "Dev"]})
print("customers key dtype:", customers["customer_id"].dtype)

# 1) every column read as text (what an object/str column looks like): int64 vs text raises
orders_txt = pd.read_csv(io.StringIO(CSV), dtype=str)
print("orders key dtype (dtype=str):", orders_txt["customer_id"].dtype)
try:
    customers.merge(orders_txt, on="customer_id")
except ValueError as e:
    print("int64 vs str ->", type(e).__name__ + ":", e)
orders_obj = pd.read_csv(io.StringIO(CSV), dtype=object)
try:
    customers.merge(orders_obj, on="customer_id")
except ValueError as e:
    print("int64 vs object ->", type(e).__name__ + ":", e)

# 1b) text on BOTH sides: no error at all, the '2 ' row just fails to match
cust_txt = customers.assign(customer_id=customers["customer_id"].astype(str))
t = orders_txt.merge(cust_txt, on="customer_id", how="left", indicator=True)
print("\ntext vs text, no strip: unmatched order_ids:", t.loc[t["_merge"] == "left_only", "order_id"].tolist())

# 2) silent wrong result: an object column holding a mix of ints and strings does NOT raise
mixed = pd.DataFrame({"order_id": [10, 11, 12], "customer_id": pd.Series([1, "2", 3], dtype=object)})
m = mixed.merge(customers, on="customer_id", how="left", indicator=True)
print("\nmixed object key (1, '2', 3), orders LEFT JOIN customers:")
print(m[["order_id", "customer_id", "name", "_merge"]].to_string(index=False))

# 3) float64 key because of the blank (NaN): matches ints, no error, but NaN row can never match
orders_default = pd.read_csv(io.StringIO(CSV.replace("2 ", "2")))
print("\ndefault read_csv key dtype:", orders_default["customer_id"].dtype)
print(orders_default.merge(customers, on="customer_id", how="left", indicator=True)
      [["order_id", "customer_id", "name", "_merge"]].to_string(index=False))

# 4) the fix: strip, convert to numbers (errors -> NaN), nullable Int64, then merge and check unmatched
orders = orders_txt.copy()
orders["order_id"] = orders["order_id"].astype("int64")
orders["customer_id"] = pd.to_numeric(orders["customer_id"].str.strip(), errors="coerce").astype("Int64")
print("\nafter fix, key dtype:", orders["customer_id"].dtype)
p = orders.merge(customers, on="customer_id", how="left", indicator=True)
p = p[["order_id", "customer_id", "name", "_merge"]].sort_values("order_id").reset_index(drop=True)
print(p.to_string())
unmatched = p[p["_merge"] != "both"]
print("unmatched orders:", unmatched["order_id"].tolist())
assert unmatched["order_id"].tolist() == [13, 15]       # blank key and unknown customer 7

# 5) the same in SQL (SQLite): orders loaded as TEXT, as a CSV import would give
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders_raw(order_id INTEGER, customer_id TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders_raw VALUES (10,'1'),(11,'2 '),(12,'3'),(13,NULL),(14,'3'),(15,'7');
""")
SQL_IMPLICIT = """
SELECT o.order_id, c.name FROM orders_raw o LEFT JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_FIX = """
SELECT o.order_id, CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER) AS customer_id, c.name,
       CASE WHEN c.customer_id IS NULL THEN 'left_only' ELSE 'both' END AS _merge
FROM orders_raw o
LEFT JOIN customers c ON c.customer_id = CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER)
ORDER BY o.order_id
"""
print("\nSQLite implicit cast (TEXT vs INTEGER column, no TRIM):", con.execute(SQL_IMPLICIT).fetchall())
print("SQLite literal compare 1 = '1':", con.execute("SELECT 1 = '1'").fetchone()[0],
      "| '2 ' as number:", con.execute("SELECT CAST('2 ' AS INTEGER)").fetchone()[0],
      "| CAST('x' AS INTEGER):", con.execute("SELECT CAST('x' AS INTEGER)").fetchone()[0],
      "| CAST('' AS INTEGER):", con.execute("SELECT CAST('' AS INTEGER)").fetchone()[0])
s = pd.read_sql_query(SQL_FIX, con)
s["customer_id"] = s["customer_id"].astype("Int64")
s["_merge"] = pd.Categorical(s["_merge"], categories=["left_only", "right_only", "both"])  # same categories as indicator=True
print(s.to_string())
pd.testing.assert_frame_equal(s[["order_id", "customer_id", "name", "_merge"]], p, check_dtype=False)
print("SQL fix == pandas fix (sorted by order_id)")

# 6) a bad text value: pandas coerce gives NaN like NULLIF; SQLite CAST silently gives 0
print("\nto_numeric coerce on ['1',' 2','x']:",
      pd.to_numeric(pd.Series(["1", " 2", "x"]).str.strip(), errors="coerce").tolist())
try:
    pd.Series(["1", "x"]).astype("Int64")
except (ValueError, TypeError) as e:
    print("astype('Int64') on 'x' ->", type(e).__name__ + ":", e)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    customers.merge(pd.DataFrame({"customer_id": [1.0, 2.5]}), on="customer_id")
print("int64 vs float64 with a non-integer float:", [str(x.message)[:60] for x in w])
try:
    pd.Series([1.5]).astype("Int64")
except (ValueError, TypeError) as e:
    print("astype('Int64') on 1.5 ->", type(e).__name__ + ":", e)
print("astype('Int64') on ['1', ' 2'] without strip:", pd.Series(["1", " 2"]).astype("Int64").tolist(),
      "| to_numeric without strip:", pd.to_numeric(pd.Series(["1", " 2"])).tolist())
# NaN keys on BOTH sides: pandas matches NaN with NaN (SQL never matches NULL = NULL)
left_nan = pd.DataFrame({"customer_id": [1.0, None], "name": ["Asha", "Unknown"]})
right_nan = pd.DataFrame({"customer_id": [None, 3.0], "order_id": [13, 12]})
both = left_nan.merge(right_nan, on="customer_id", how="inner")
print("NaN key on both sides, inner merge rows:", both[["name", "order_id"]].values.tolist())
sql_nan = sqlite3.connect(":memory:").execute(
    "SELECT COUNT(*) FROM (SELECT NULL AS k) a JOIN (SELECT NULL AS k) b ON a.k = b.k").fetchone()[0]
print("SQL NULL = NULL join rows:", sql_nan)
con.close()
```

**Output (my run):**
```text
customers key dtype: int64
orders key dtype (dtype=str): str
int64 vs str -> ValueError: You are trying to merge on int64 and str columns for key 'customer_id'. If you wish to proceed you should use pd.concat
int64 vs object -> ValueError: You are trying to merge on int64 and object columns for key 'customer_id'. If you wish to proceed you should use pd.concat

text vs text, no strip: unmatched order_ids: ['11', '13', '15']

mixed object key (1, '2', 3), orders LEFT JOIN customers:
 order_id customer_id   name    _merge
       10           1   Asha      both
       11           2    NaN left_only
       12           3 Chitra      both

default read_csv key dtype: float64
 order_id  customer_id   name    _merge
       10          1.0   Asha      both
       11          2.0    Ben      both
       12          3.0 Chitra      both
       13          NaN    NaN left_only
       14          3.0 Chitra      both
       15          7.0    NaN left_only

after fix, key dtype: Int64
   order_id  customer_id    name     _merge
0        10            1    Asha       both
1        11            2     Ben       both
2        12            3  Chitra       both
3        13         <NA>     NaN  left_only
4        14            3  Chitra       both
5        15            7     NaN  left_only
unmatched orders: [13, 15]

SQLite implicit cast (TEXT vs INTEGER column, no TRIM): [(10, 'Asha'), (11, 'Ben'), (12, 'Chitra'), (13, None), (14, 'Chitra'), (15, None)]
SQLite literal compare 1 = '1': 0 | '2 ' as number: 2 | CAST('x' AS INTEGER): 0 | CAST('' AS INTEGER): 0
   order_id  customer_id    name     _merge
0        10            1    Asha       both
1        11            2     Ben       both
2        12            3  Chitra       both
3        13         <NA>     NaN  left_only
4        14            3  Chitra       both
5        15            7     NaN  left_only
SQL fix == pandas fix (sorted by order_id)

to_numeric coerce on ['1',' 2','x']: [1.0, 2.0, nan]
astype('Int64') on 'x' -> ValueError: invalid literal for int() with base 10: 'x'
int64 vs float64 with a non-integer float: ['You are merging on int and float columns where the float val']
astype('Int64') on 1.5 -> TypeError: cannot safely cast non-equivalent object to int64
astype('Int64') on ['1', ' 2'] without strip: [1, 2] | to_numeric without strip: [1, 2]
NaN key on both sides, inner merge rows: [['Unknown', 13]]
SQL NULL = NULL join rows: 0
```

**Edge cases:**
- **int64 against str or object:** `ValueError: You are trying to merge on int64 and str columns ...` (the message says `object` when the column really is object dtype). On pandas 3.0.5 a text column read from CSV with `dtype=str` shows as `str`; both raised in my run.
- **Silent wrong results, no error:** text against text with a stray space (`'2 '` does not equal `'2'`), and an `object` column holding both ints and strings (the string `'2'` did not match the int 2 and the row fell out of the match, with no error).
- **float64 key because of NaN:** int64 against float64 merges without error and `1.0` matches `1`. The NaN row simply finds no partner. If a float key holds a non-integer value (2.5), pandas only emits a `UserWarning` (seen in my run). And `astype('Int64')` on a column containing 1.5 raised `TypeError`, which is the safe behaviour.
- **Leading and trailing spaces and the numeric cast:** in my run `to_numeric` and `astype('Int64')` both accepted `' 2'` without strip (Python's `int()` tolerates spaces). So the strip is essential for text keys that stay text (names, codes, ids with letters), and a good habit for numeric ones, but do not claim the cast fails without it.
- **Leading zeros:** `'01'` and `'1'` are different text keys but the same number. Decide which meaning you want before choosing text or integer.
- **NaN keys on both sides do match in pandas:** with NaN in both frames, an inner merge joined the NaN row to the NaN row (`Unknown` with order 13 in my run), while the SQL join `NULL = NULL` returned 0 rows. In this question's fixed merge only orders has a missing key, so that row is just `left_only`, but if the customer table also had a NaN key you would get false matches; drop or flag missing keys before merging.

**Then explain:**
- **Why pandas raises for int against str:** it refuses to guess a cast, because the guess could hide a data problem. `object` columns are the dangerous case: they can hold anything, so a mismatch may not be caught.
- **The fix order:** strip, then convert, with `errors="coerce"` so bad values become NaN rather than crash, then `Int64` (capital I) so the key keeps integers and still allows missing values. Plain `int64` cannot hold NaN.
- **The check that matters:** `indicator=True` and look at `left_only`, or compare the row count and the number of matched keys. A merge that silently matches fewer rows than expected is the real risk.
- **SQL implicit casting (ran on SQLite 3.45.1):** joining a TEXT column to an INTEGER column did match (`'2 '` matched 2 and Ben appeared), because SQLite applies numeric affinity to the text side. A bare literal comparison `1 = '1'` gave 0 in the same engine, so the rule depends on column affinity. This is engine dependent and I only ran SQLite.
- **Other engines, not executed here:** PostgreSQL normally errors on `integer = text` for columns (`operator does not exist`), MySQL converts strings to numbers silently (and that conversion can stop an index being used), SQL Server converts by data type precedence and fails with a conversion error on a bad value like `'x'`. Check the manual of your engine.

**Follow-ups:**
- *How do you stop this at load time?* Pass `dtype={"customer_id": "Int64"}` or convert explicitly right after `read_csv`, and assert `df["customer_id"].notna().all()` where blanks are not allowed.
- *Should the key be int or str?* If ids are codes (leading zeros, letters), keep them as stripped text on both sides; if they are numbers, use `Int64`.
- *How do you find which values break the cast?* `bad = s[pd.to_numeric(s.str.strip(), errors="coerce").isna() & s.notna()]`.

**Common mistakes:**
- Casting with `astype(int)` on a column with NaN and getting an error, then dropping rows to make it pass.
- Trusting a merge that did not raise: no error does not mean all rows matched.
- Using `COALESCE(key, 0)` or `CAST('' AS INTEGER)` and creating a fake customer 0.
- Fixing the dtype on one frame only, so the other side still holds text.

### Q36 ⭐ 🟡 Join on the nearest earlier timestamp: trades(trade_id, ticker, trade_time, qty) and quotes(ticker, quote_time, bid). Attach to each trade the latest quote at or before the trade for the same ticker. Show pandas merge_asof (both sorted by time, by='ticker', direction, tolerance, allow_exact_matches), note SQLite has no ASOF JOIN (some engines do, hedged) and write the portable SQL with a correlated MAX(quote_time) subquery.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `pd.merge_asof` is the "latest quote at or before the trade" join (backward direction by default, both frames sorted by time, `by="ticker"`), and the portable SQL is a LEFT JOIN with a correlated `MAX(quote_time)` subquery in the ON clause; SQLite 3.45 has no `ASOF JOIN`.

**Schema and sample data:**
```sql
CREATE TABLE trades(trade_id INTEGER PRIMARY KEY, ticker TEXT, trade_time TEXT, qty INTEGER);
CREATE TABLE quotes(ticker TEXT, quote_time TEXT, bid REAL);
INSERT INTO trades VALUES
 (1,'A','2026-01-05 09:00:05',100),
 (2,'A','2026-01-05 09:00:10', 50),
 (3,'B','2026-01-05 09:00:07', 20),
 (4,'A','2026-01-05 09:00:01', 10),
 (5,'B','2026-01-05 09:01:30', 30);
INSERT INTO quotes VALUES
 ('A','2026-01-05 09:00:02',10.0),
 ('A','2026-01-05 09:00:10',10.5),
 ('A','2026-01-05 09:00:12',11.0),
 ('B','2026-01-05 09:00:03',20.0),
 ('B','2026-01-05 09:00:08',21.0);
```

**SQL answer:** `SQL_MAIN` (the three variants `SQL_MAIN`, `SQL_TOL` for a 30 second tolerance and `SQL_STRICT` for strictly earlier are all in the Code block; `SQL_STRICT` is `SQL_MAIN` with `<=` changed to `<`):
```sql
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
```
The subquery finds, per trade, the latest quote time for the same ticker that is not after the trade. The outer join then fetches that quote row. LEFT JOIN keeps trades that have no earlier quote (they get NULL).

Not executed: DuckDB, Snowflake and ClickHouse, to my knowledge, have a native `ASOF JOIN` (syntax differs by engine), which does this in one clause. SQLite 3.45 rejected it in my run (`near "ASOF": syntax error`).

**pandas answer:** (same text as in the Code block)
```py
out = pd.merge_asof(trades.sort_values("trade_time"), quotes.sort_values("quote_time"),
                    left_on="trade_time", right_on="quote_time", by="ticker", **kw)
```
Here `**kw` is empty for the plain case, `tolerance=pd.Timedelta("30s")` for the tolerance case, `allow_exact_matches=False` for strictly earlier, and `direction="forward"` or `"nearest"` for the other directions. The `asof` helper in the Code block then restores the order by `trade_id`.

**Example:** quotes for A at 09:00:02 (10.0), 09:00:10 (10.5), 09:00:12 (11.0); for B at 09:00:03 (20.0) and 09:00:08 (21.0).
- Trade 1 (A, 09:00:05): latest A quote at or before is 09:00:02, so bid 10.0.
- Trade 2 (A, 09:00:10): there is a quote at exactly 09:00:10, so bid 10.5. With `allow_exact_matches=False` it would take the 09:00:02 quote, bid 10.0.
- Trade 3 (B, 09:00:07): B quote at 09:00:03, so 20.0 (the 09:00:08 quote is in the future).
- Trade 4 (A, 09:00:01): no quote before it, so NULL.
- Trade 5 (B, 09:01:30): latest quote is 09:00:08 (82 seconds old), so 21.0, or NULL with a 30 second tolerance.

**Code:** run with `python3 -I`; each of the three SQL variants is compared with its `merge_asof` call after sorting by `trade_id`.
```python
# Q36: attach the latest quote at or before each trade: SQL correlated MAX vs pandas merge_asof
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE trades(trade_id INTEGER PRIMARY KEY, ticker TEXT, trade_time TEXT, qty INTEGER);
CREATE TABLE quotes(ticker TEXT, quote_time TEXT, bid REAL);
INSERT INTO trades VALUES
 (1,'A','2026-01-05 09:00:05',100),
 (2,'A','2026-01-05 09:00:10', 50),
 (3,'B','2026-01-05 09:00:07', 20),
 (4,'A','2026-01-05 09:00:01', 10),
 (5,'B','2026-01-05 09:01:30', 30);
INSERT INTO quotes VALUES
 ('A','2026-01-05 09:00:02',10.0),
 ('A','2026-01-05 09:00:10',10.5),
 ('A','2026-01-05 09:00:12',11.0),
 ('B','2026-01-05 09:00:03',20.0),
 ('B','2026-01-05 09:00:08',21.0);
"""
SQL_MAIN = """
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
"""
# tolerance of 30 seconds: the quote must also be no older than 30 s
SQL_TOL = """
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time >= datetime(t.trade_time, '-30 seconds')
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
"""
# strictly earlier (allow_exact_matches=False)
SQL_STRICT = SQL_MAIN.replace("<= t.trade_time", "< t.trade_time")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
trades = pd.read_sql_query("SELECT * FROM trades", con, parse_dates=["trade_time"])
quotes = pd.read_sql_query("SELECT * FROM quotes", con, parse_dates=["quote_time"])

def sql_df(q):
    d = pd.read_sql_query(q, con, parse_dates=["trade_time", "quote_time"])
    return d.sort_values("trade_id").reset_index(drop=True)

def asof(**kw):
    out = pd.merge_asof(trades.sort_values("trade_time"), quotes.sort_values("quote_time"),
                        left_on="trade_time", right_on="quote_time", by="ticker", **kw)
    return out[["trade_id", "ticker", "trade_time", "qty", "quote_time", "bid"]].sort_values("trade_id").reset_index(drop=True)

p_main = asof()                                           # direction='backward', exact matches allowed
p_tol = asof(tolerance=pd.Timedelta("30s"))
p_strict = asof(allow_exact_matches=False)
for name, s, p in [("main", SQL_MAIN, p_main), ("tolerance 30s", SQL_TOL, p_tol), ("strictly earlier", SQL_STRICT, p_strict)]:
    d = sql_df(s)
    pd.testing.assert_frame_equal(d, p, check_dtype=False)
    print(f"--- {name}: SQL == merge_asof (sorted by trade_id)")
    print(d[["trade_id", "ticker", "trade_time", "quote_time", "bid"]].to_string(index=False))

# SQLite has no ASOF JOIN
try:
    con.execute("SELECT * FROM trades t ASOF JOIN quotes q ON q.ticker = t.ticker AND q.quote_time <= t.trade_time")
except sqlite3.Error as e:
    print("\nASOF JOIN in SQLite ->", type(e).__name__ + ":", e)

# direction='nearest' and 'forward' exist only in pandas; the SQL needs another subquery
print("\ndirection='forward', bids:", asof(direction="forward")["bid"].tolist())
print("direction='nearest', bids:", asof(direction="nearest")["bid"].tolist())

# merge_asof refuses unsorted input
try:
    pd.merge_asof(trades.sort_values("trade_id", ascending=False), quotes.sort_values("quote_time"),
                  left_on="trade_time", right_on="quote_time", by="ticker")
except ValueError as e:
    print("\nunsorted left ->", type(e).__name__ + ":", e)

# two quotes with the same timestamp: SQL returns two rows for the trade, merge_asof exactly one
con.execute("INSERT INTO quotes VALUES ('A','2026-01-05 09:00:12',11.2)")
con.execute("INSERT INTO trades VALUES (6,'A','2026-01-05 09:00:20',5)")
d = pd.read_sql_query(SQL_MAIN, con)
print("\nwith a duplicate quote timestamp, SQL rows for trade 6:", d[d["trade_id"] == 6]["bid"].tolist())
t2 = pd.read_sql_query("SELECT * FROM trades", con, parse_dates=["trade_time"])
q2 = pd.read_sql_query("SELECT * FROM quotes", con, parse_dates=["quote_time"])
a = pd.merge_asof(t2.sort_values("trade_time"), q2.sort_values("quote_time"),
                  left_on="trade_time", right_on="quote_time", by="ticker")
print("merge_asof rows for trade 6:", a[a["trade_id"] == 6]["bid"].tolist())
con.close()
```

**Output (my run):**
```text
--- main: SQL == merge_asof (sorted by trade_id)
 trade_id ticker          trade_time          quote_time  bid
        1      A 2026-01-05 09:00:05 2026-01-05 09:00:02 10.0
        2      A 2026-01-05 09:00:10 2026-01-05 09:00:10 10.5
        3      B 2026-01-05 09:00:07 2026-01-05 09:00:03 20.0
        4      A 2026-01-05 09:00:01                 NaT  NaN
        5      B 2026-01-05 09:01:30 2026-01-05 09:00:08 21.0
--- tolerance 30s: SQL == merge_asof (sorted by trade_id)
 trade_id ticker          trade_time          quote_time  bid
        1      A 2026-01-05 09:00:05 2026-01-05 09:00:02 10.0
        2      A 2026-01-05 09:00:10 2026-01-05 09:00:10 10.5
        3      B 2026-01-05 09:00:07 2026-01-05 09:00:03 20.0
        4      A 2026-01-05 09:00:01                 NaT  NaN
        5      B 2026-01-05 09:01:30                 NaT  NaN
--- strictly earlier: SQL == merge_asof (sorted by trade_id)
 trade_id ticker          trade_time          quote_time  bid
        1      A 2026-01-05 09:00:05 2026-01-05 09:00:02 10.0
        2      A 2026-01-05 09:00:10 2026-01-05 09:00:02 10.0
        3      B 2026-01-05 09:00:07 2026-01-05 09:00:03 20.0
        4      A 2026-01-05 09:00:01                 NaT  NaN
        5      B 2026-01-05 09:01:30 2026-01-05 09:00:08 21.0

ASOF JOIN in SQLite -> OperationalError: near "ASOF": syntax error

direction='forward', bids: [10.5, 10.5, 21.0, 10.0, nan]
direction='nearest', bids: [10.0, 10.5, 21.0, 10.0, 21.0]

unsorted left -> ValueError: left keys must be sorted

with a duplicate quote timestamp, SQL rows for trade 6: [11.0, 11.2]
merge_asof rows for trade 6: [11.2]
```

**Edge cases:**
- **Unsorted input:** `merge_asof` raised `ValueError: left keys must be sorted` in my run. Sort both frames on the time key (globally, not per ticker; `by` handles the ticker).
- **Duplicate quote timestamps:** with two quotes for A at 09:00:12 (11.0 and 11.2) the SQL returned two rows for the trade at 09:00:20 (`[11.0, 11.2]`), but `merge_asof` returned one (`[11.2]`, the later row). This is an honest difference: SQL needs a tie-break (a quote id or sequence number) to pick one row, `merge_asof` took the last of the tied rows (11.2).
- **No earlier quote:** NULL in SQL, NaN and NaT in pandas.
- **Tolerance:** in pandas it applies to the chosen quote, and a stale quote gives NaN; in SQL I put the age test in the ON clause, so the trade row is kept with NULLs (do not move it to WHERE, which would drop the trade).
- **Direction:** `forward` and `nearest` have no one-line SQL form; you would need a `MIN(quote_time) ... >=` subquery or a comparison of two subqueries.
- **Time zones and text timestamps:** my SQL compares ISO 8601 text (`YYYY-MM-DD HH:MM:SS`), which sorts correctly as text. Mixed formats or time zones would break that, and in pandas make both columns the same tz-aware or tz-naive dtype.

**Then explain:**
- **Why an equality join does not work:** quotes and trades almost never share a timestamp, so you need "the nearest one before".
- **The SQL idea:** a correlated subquery returns the right quote time, then an equality join on it. A window-function version also exists (Parts 4 and 5), not used here.
- **Cost:** the correlated subquery is fast only with an index on `(ticker, quote_time)`; `merge_asof` is a sorted merge scan and is typically much faster on large frames (concept; I did not benchmark).
- **`by`:** matches the ticker exactly, then finds the nearest time within it.
- **`allow_exact_matches=False`:** turns `<=` into `<`, which is what you want if a quote at the same instant may have been caused by the trade.

**Follow-ups:**
- *What if quotes arrive after the trade but you want the next one?* `direction="forward"`, which in SQL is `MIN(quote_time)` with `>=`.
- *What if the quotes table is huge?* Index `(ticker, quote_time)` for the SQL version, or pre-filter the day.
- *How would you handle ties in quote_time?* Add a sequence column and pick by `MAX(seq)`; in pandas sort by the time then the sequence before `merge_asof`.

**Common mistakes:**
- Forgetting to sort, or sorting by ticker then time (the key `on` must be sorted globally).
- Putting the tolerance condition in WHERE, which drops the unmatched trades.
- Using `BETWEEN` or `<=` on the join without a `MAX`, which returns every older quote for every trade (a fan-out).
- Merging on `ticker` first with a normal merge and then filtering (a huge intermediate result).

### Q37 ⭐ 🟡 Market-basket pairs with a self join: order_items(order_id, product_id). Find the ten most common pairs of products bought in the same order, each pair once. Join the table to itself on order_id with a.product_id < b.product_id, group by the pair, and count. Explain row growth with large baskets, duplicate lines of the same product, and the pandas version (merge on order_id and filter, then value_counts).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join the table to itself on `order_id` with `a.product_id < b.product_id` so each pair appears once, `GROUP BY` the pair and `COUNT(*)` orders, but dedupe the lines first, or an order that has the same product on two lines counts a pair twice.

**Schema and sample data:**
```sql
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'C'),
 (4,'B'),(4,'C'),(4,'A'),
 (5,'A'),(5,'B'),(5,'B'),
 (6,'D');
```

**SQL answer:** `SQL_MAIN` in the Code block (derived tables, no CTE, because CTEs are Part 3):
```sql
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM (SELECT DISTINCT order_id, product_id FROM order_items) a
JOIN (SELECT DISTINCT order_id, product_id FROM order_items) b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
```
`SQL_NAIVE` in the Code block is the same query on `order_items` directly (no `DISTINCT`), kept to show the inflation.

**pandas answer:** (same text as in the Code block)
```py
basket = items.drop_duplicates()
pairs = basket.merge(basket, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs["product_id_1"] < pairs["product_id_2"]]
counts = pairs[["product_id_1", "product_id_2"]].value_counts()      # a Series indexed by the pair
```
After that the Code block renames the columns and sorts by count descending then the two ids, so ties come out in a fixed order, then takes `head(10)`.

**Example:** six orders. Order 1 has A, B, C, so pairs AB, AC, BC. Order 2 has A, B, so AB. Order 3 has A, C, so AC. Order 4 has B, C, A, so AB, AC, BC. Order 5 has A, B, B (B twice), so AB after deduplication. Order 6 has only D, so no pair. Totals: AB in orders 1, 2, 4 and 5 is 4; AC in 1, 3, 4 is 3; BC in 1 and 4 is 2. Without the dedupe, order 5 produces AB twice (A with each B line), giving 5, which is wrong.

**Code:** run with `python3 -I`; the SQL result and the pandas result are compared in the order `n_orders` descending, then `p1`, then `p2`.
```python
# Q37: market-basket pairs with a self join: dedupe lines, a < b, GROUP BY pair, top N
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'C'),
 (4,'B'),(4,'C'),(4,'A'),
 (5,'A'),(5,'B'),(5,'B'),
 (6,'D');
"""
SQL_MAIN = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM (SELECT DISTINCT order_id, product_id FROM order_items) a
JOIN (SELECT DISTINCT order_id, product_id FROM order_items) b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
"""
SQL_NAIVE = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (deduplicated baskets):")
print(sql_df.to_string(index=False))
print("\nSQL naive (duplicate line not removed):")
naive = pd.read_sql_query(SQL_NAIVE, con)
print(naive.to_string(index=False))

# pandas: dedupe lines, self-merge on order_id, keep p1 < p2, count pairs
items = pd.read_sql_query("SELECT * FROM order_items", con)
basket = items.drop_duplicates()
pairs = basket.merge(basket, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs["product_id_1"] < pairs["product_id_2"]]
counts = pairs[["product_id_1", "product_id_2"]].value_counts()      # a Series indexed by the pair
p_df = (counts.rename("n_orders").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"})
        .sort_values(["n_orders", "p1", "p2"], ascending=[False, True, True])
        .head(10).reset_index(drop=True))
print("\npandas (value_counts after the filtered self-merge):")
print(p_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, p_df, check_dtype=False)
print("SQL == pandas (compared in the order n_orders desc, p1, p2)")

# row growth: a basket of n distinct products produces n(n-1)/2 pair rows
for n in (3, 10, 100):
    con.execute("DELETE FROM order_items WHERE order_id = 99")
    con.executemany("INSERT INTO order_items VALUES (99, ?)", [(f"P{i:03d}",) for i in range(n)])
    rows = con.execute("""SELECT COUNT(*) FROM order_items a JOIN order_items b
                          ON a.order_id = b.order_id AND a.product_id < b.product_id
                          WHERE a.order_id = 99""").fetchone()[0]
    print(f"basket of {n:>3} products -> {rows} pair rows (n(n-1)/2 = {n*(n-1)//2})")
con.close()
```

**Output (my run):**
```text
SQL (deduplicated baskets):
p1 p2  n_orders
 A  B         4
 A  C         3
 B  C         2

SQL naive (duplicate line not removed):
p1 p2  n_orders
 A  B         5
 A  C         3
 B  C         2

pandas (value_counts after the filtered self-merge):
p1 p2  n_orders
 A  B         4
 A  C         3
 B  C         2
SQL == pandas (compared in the order n_orders desc, p1, p2)
basket of   3 products -> 3 pair rows (n(n-1)/2 = 3)
basket of  10 products -> 45 pair rows (n(n-1)/2 = 45)
basket of 100 products -> 4950 pair rows (n(n-1)/2 = 4950)
```

**Edge cases:**
- **Only three pairs exist in my toy data, so "top ten" returns three rows.** `LIMIT 10` is an upper bound, not a promise of ten.
- **Duplicate lines:** the naive version gave AB = 5 instead of 4. The fix is `SELECT DISTINCT order_id, product_id` on both sides (or a unique constraint on `(order_id, product_id)`).
- **Ties at the cut-off:** `LIMIT 10` cuts arbitrarily among equal counts unless the `ORDER BY` has a tie-break, which is why the query sorts by `p1, p2` after the count.
- **Single-item orders (D):** they produce no pair rows, which is correct.
- **`<` versus `<>`:** `<>` would give both (A,B) and (B,A), doubling every count; `<` also removes the (A,A) self pair.

**Then explain:**
- **Row growth:** an order with n distinct products creates n(n-1)/2 pair rows (3, 45 and 4950 rows for baskets of 3, 10 and 100 products in my run). One very large order (a bulk or test order) can dominate the join. Cap basket size, or filter out baskets above a limit, before the self join.
- **Why filter products first for scale:** keep only products with some minimum frequency before self-joining, since a pair cannot be common if one of its items is rare (this is the idea behind support thresholds; I describe it, I did not run it).
- **Count meaning:** `COUNT(*)` after the dedupe is the number of orders containing both products, which is what "bought together" means. It is not the units sold.
- **pandas:** the self-merge makes the same row blow-up in memory; `value_counts` on two columns counts each pair, and ties come out in no guaranteed order, so I sort explicitly before `head`.

**Follow-ups:**
- *How would you add lift or confidence?* Divide the pair count by the product counts (each from `COUNT(DISTINCT order_id)` on one product); that is a second aggregation joined back on.
- *Triples?* A three-way self join with `a < b < c`; growth is cubic, so filter first.
- *Can you avoid the self join?* Not easily in pure SQL; some engines allow array aggregation then unnesting, which is outside this part.

**Common mistakes:**
- Using `<>`, which doubles every pair.
- Not deduping duplicate lines, inflating counts.
- No tie-break in `ORDER BY ... LIMIT`.
- Running the self join on the full line table with huge baskets and wondering why it crawls.

### Q38 ⭐ 🟡 Students and courses (many-to-many): students(student_id, name), courses(course_id, title) and enrollments(student_id, course_id). Find students enrolled in no course, students enrolled in every course (relational division via GROUP BY HAVING COUNT(DISTINCT course_id) = total courses), and pairs of students sharing a course. Explain the bridge table and why duplicate enrollment rows need DISTINCT. Give pandas.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** The bridge table `enrollments` holds one row per student and course; "no course" is an anti-join, "every course" is `GROUP BY student HAVING COUNT(DISTINCT course_id) = (SELECT COUNT(*) FROM courses)`, and "pairs sharing a course" is a self join on `course_id` with `a.student_id < b.student_id`, always on de-duplicated enrolment rows.

**Schema and sample data:**
```sql
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE courses(course_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE enrollments(student_id INTEGER, course_id INTEGER);   -- no primary key, so duplicates are possible
INSERT INTO students VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO courses VALUES (10,'SQL'),(20,'Stats'),(30,'ML');
INSERT INTO enrollments VALUES
 (1,10),(1,20),(1,30),
 (2,10),(2,10),(2,20),
 (3,10),(3,20),(3,30),
 (5,30);
```
Ben has a duplicated row (course 10 twice); Dev has no enrolment.

**SQL answer:** the queries are `SQL_NONE`, `SQL_ALL`, `SQL_ALL_WRONG` (the trap) and `SQL_PAIRS` in the Code block.
```sql
SELECT s.name FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.student_id)
ORDER BY s.student_id
```
```sql
SELECT s.name
FROM students s
JOIN enrollments e ON e.student_id = s.student_id
JOIN courses c ON c.course_id = e.course_id
GROUP BY s.student_id, s.name
HAVING COUNT(DISTINCT e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
```
```sql
SELECT a.student_id AS s1, b.student_id AS s2, COUNT(*) AS shared_courses
FROM (SELECT DISTINCT student_id, course_id FROM enrollments) a
JOIN (SELECT DISTINCT student_id, course_id FROM enrollments) b ON a.course_id = b.course_id AND a.student_id < b.student_id
GROUP BY a.student_id, b.student_id
ORDER BY s1, s2
```

**pandas answer:** (same text as in the Code block)
```py
none_p = students.loc[~students["student_id"].isin(enr["student_id"]), "name"].tolist()
valid = enr.drop_duplicates().merge(courses[["course_id"]], on="course_id")           # drop dups, keep real courses
n_courses = valid.groupby("student_id")["course_id"].nunique()
all_ids = n_courses[n_courses == len(courses)].index
d = enr.drop_duplicates()
pp = d.merge(d, on="course_id", suffixes=("_1", "_2"))
pp = pp[pp["student_id_1"] < pp["student_id_2"]]
```

**Example:** Courses are 10, 20, 30. Asha: 10, 20, 30, so all three. Ben: 10, 10, 20, so two distinct (three rows). Chitra: 10, 20, 30, so all three. Dev: nothing. Esha: 30 only.
- No enrolment: Dev.
- Every course: Asha and Chitra. Ben's three rows would pass `COUNT(*) = 3`, which is wrong; `COUNT(DISTINCT course_id)` gives 2 and rejects him.
- Pairs: course 10 has Asha, Ben, Chitra, giving (1,2), (1,3), (2,3); course 20 gives the same three; course 30 has Asha, Chitra, Esha, giving (1,3), (1,5), (3,5). Shared courses per pair: (1,2) 2, (1,3) 3, (2,3) 2, (1,5) 1, (3,5) 1.

**Code:** run with `python3 -I`; pairs are compared sorted by `s1, s2`, and the two name lists are compared in `student_id` order.
```python
# Q38: many-to-many: no enrolment, enrolled in every course (division), pairs sharing a course
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE courses(course_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE enrollments(student_id INTEGER, course_id INTEGER);   -- no primary key, so duplicates are possible
INSERT INTO students VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO courses VALUES (10,'SQL'),(20,'Stats'),(30,'ML');
INSERT INTO enrollments VALUES
 (1,10),(1,20),(1,30),
 (2,10),(2,10),(2,20),
 (3,10),(3,20),(3,30),
 (5,30);
"""
SQL_NONE = """
SELECT s.name FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.student_id)
ORDER BY s.student_id
"""
SQL_ALL = """
SELECT s.name
FROM students s
JOIN enrollments e ON e.student_id = s.student_id
JOIN courses c ON c.course_id = e.course_id
GROUP BY s.student_id, s.name
HAVING COUNT(DISTINCT e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
"""
SQL_ALL_WRONG = """
SELECT s.name FROM students s JOIN enrollments e ON e.student_id = s.student_id
GROUP BY s.student_id, s.name
HAVING COUNT(e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
"""
SQL_PAIRS = """
SELECT a.student_id AS s1, b.student_id AS s2, COUNT(*) AS shared_courses
FROM (SELECT DISTINCT student_id, course_id FROM enrollments) a
JOIN (SELECT DISTINCT student_id, course_id FROM enrollments) b ON a.course_id = b.course_id AND a.student_id < b.student_id
GROUP BY a.student_id, b.student_id
ORDER BY s1, s2
"""
SQL_PAIRS_NAIVE = SQL_PAIRS.replace("(SELECT DISTINCT student_id, course_id FROM enrollments)",
                                    "enrollments")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
col = lambda q: [r[0] for r in con.execute(q).fetchall()]
print("no enrolment:", col(SQL_NONE))
print("every course:", col(SQL_ALL))
print("every course, COUNT(e.course_id) instead of DISTINCT (wrong):", col(SQL_ALL_WRONG))
pairs = pd.read_sql_query(SQL_PAIRS, con)
print("\npairs sharing a course (deduplicated):")
print(pairs.to_string(index=False))
print("\npairs with duplicate rows not removed (shared_courses inflated):")
print(pd.read_sql_query(SQL_PAIRS_NAIVE, con).to_string(index=False))

# pandas
students = pd.read_sql_query("SELECT * FROM students", con)
courses = pd.read_sql_query("SELECT * FROM courses", con)
enr = pd.read_sql_query("SELECT * FROM enrollments", con)
none_p = students.loc[~students["student_id"].isin(enr["student_id"]), "name"].tolist()
valid = enr.drop_duplicates().merge(courses[["course_id"]], on="course_id")           # drop dups, keep real courses
n_courses = valid.groupby("student_id")["course_id"].nunique()
all_ids = n_courses[n_courses == len(courses)].index
all_p = students.loc[students["student_id"].isin(all_ids)].sort_values("student_id")["name"].tolist()
d = enr.drop_duplicates()
pp = d.merge(d, on="course_id", suffixes=("_1", "_2"))
pp = pp[pp["student_id_1"] < pp["student_id_2"]]
pairs_p = (pp.groupby(["student_id_1", "student_id_2"], as_index=False).size()
           .rename(columns={"student_id_1": "s1", "student_id_2": "s2", "size": "shared_courses"})
           .sort_values(["s1", "s2"]).reset_index(drop=True))
assert none_p == col(SQL_NONE) == ["Dev"]
assert all_p == col(SQL_ALL) == ["Asha", "Chitra"]
pd.testing.assert_frame_equal(pairs, pairs_p, check_dtype=False)
print("\npandas: no enrolment", none_p, "| every course", all_p)
print("asserts passed (pairs compared sorted by s1, s2)")

# edge: no courses at all
con.execute("DELETE FROM courses")
print("with an empty courses table, 'every course' returns:", col(SQL_ALL))
con.close()
```

**Output (my run):**
```text
no enrolment: ['Dev']
every course: ['Asha', 'Chitra']
every course, COUNT(e.course_id) instead of DISTINCT (wrong): ['Asha', 'Ben', 'Chitra']

pairs sharing a course (deduplicated):
 s1  s2  shared_courses
  1   2               2
  1   3               3
  1   5               1
  2   3               2
  3   5               1

pairs with duplicate rows not removed (shared_courses inflated):
 s1  s2  shared_courses
  1   2               3
  1   3               3
  1   5               1
  2   3               3
  3   5               1

pandas: no enrolment ['Dev'] | every course ['Asha', 'Chitra']
asserts passed (pairs compared sorted by s1, s2)
with an empty courses table, 'every course' returns: []
```

**Edge cases:**
- **Duplicate enrolments:** `COUNT(e.course_id)` returned Ben as enrolled in every course (output line "COUNT(e.course_id) instead of DISTINCT (wrong)"). The pairs query without the `DISTINCT` inflated (1,2), (2,3) from 2 to 3 shared courses.
- **Enrolments for a course that does not exist:** the division query joins to `courses`, so an orphan `course_id` cannot make a student look complete. In pandas the same is the merge with `courses`.
- **No courses at all:** mathematically everyone "took every course" (an empty set), but the `GROUP BY` form returned nobody (empty output in my run), because it only sees students who have enrolments. Decide what you want if the courses table can be empty.
- **A student with no rows in `enrollments`:** not in the division result unless you start from `students`; they are in the "no course" result.
- **Pairs sharing no course:** do not appear; to list all pairs you would need a cross join and an anti-join.

**Then explain:**
- **Bridge table:** many-to-many is stored as a third table with one row per (student, course), and ideally a primary key on the pair, which would also stop duplicate rows at the source.
- **Relational division by counting:** "has every course" equals "has as many distinct courses as exist", valid only if each counted row is a real course, so join to `courses` first and count distinct.
- **Other forms (not run):** a double `NOT EXISTS` expresses division without counting and is robust to duplicates; I did not run it here.
- **Pair self join:** `a.student_id < b.student_id` removes mirror pairs and self pairs; the join on `course_id` gives one row per shared course, so `COUNT(*)` is the number of shared courses.

**Follow-ups:**
- *Students enrolled in exactly the same courses as another student?* Compare the sets; that is harder, and in SQL you would compare `COUNT(*)` of shared courses to each student's total.
- *Students with at least two courses?* `HAVING COUNT(DISTINCT course_id) >= 2`.
- *How do you stop duplicates?* `PRIMARY KEY (student_id, course_id)` on the bridge table.

**Common mistakes:**
- `COUNT(*)` or `COUNT(course_id)` without `DISTINCT` in the division.
- Comparing with a hard-coded course count instead of `(SELECT COUNT(*) FROM courses)`.
- Using an INNER JOIN from `students` for the "no course" case (it cannot show the missing rows).
- Using `<>` for the pair join and returning each pair twice.

### Q39 ⭐ 🟡 Outer join key columns: a(id, x) and b(key, y) joined FULL OUTER ON a.id = b.key. Explain why neither id nor key alone is the full key set, how COALESCE(a.id, b.key) fixes the output, what USING does in engines that support it, and how pandas outer merge with left_on/right_on returns both columns while on= returns one. Include the effect on a downstream GROUP BY.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** In a FULL OUTER JOIN on `a.id = b.key`, `a.id` is NULL for right-only rows and `b.key` is NULL for left-only rows, so neither column is the full key set; select `COALESCE(a.id, b.key)` (or use `USING` where it exists), and group by that, never by one side.

**Schema and sample data:**
```sql
CREATE TABLE a(id INTEGER, x TEXT);
CREATE TABLE b(key INTEGER, y INTEGER);
CREATE TABLE b2(id INTEGER, y INTEGER);          -- same data as b, key column renamed to id for USING
INSERT INTO a VALUES (1,'a1'),(2,'a2'),(3,'a3');
INSERT INTO b VALUES (2,20),(3,30),(4,40),(5,50);
INSERT INTO b2 SELECT key, y FROM b;
```

**SQL answer:** the queries are `SQL_RAW`, `SQL_MAIN`, `SQL_USING`, `SQL_GROUP_WRONG` and `SQL_GROUP_RIGHT` in the Code block.
```sql
SELECT COALESCE(a.id, b.key) AS id, a.x, b.y
FROM a FULL OUTER JOIN b ON a.id = b.key
ORDER BY id
```
```sql
SELECT COALESCE(a.id, b.key) AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY COALESCE(a.id, b.key) ORDER BY grp
```
SQLite 3.45 ran `FULL OUTER JOIN` and `USING`. `USING` needs a column with the same name on both sides, which is why `b2` repeats `b` with the key renamed to `id`. In engines that support USING (not executed: PostgreSQL, MySQL for the inner and left/right forms), the `USING` column is merged into one output column.

**pandas answer:** (same text as in the Code block)
```py
m_lr = a.merge(b, left_on="id", right_on="key", how="outer")
m_on = a.merge(b.rename(columns={"key": "id"}), on="id", how="outer")
m_lr["id"] = m_lr["id"].fillna(m_lr["key"])
```

**Example:** `a` has ids 1, 2, 3; `b` has keys 2, 3, 4, 5. The matched pairs are 2 and 3. Left-only is 1 (so `b.key` is NULL). Right-only are 4 and 5 (so `a.id` is NULL). Reading only `a.id` you would see 1, 2, 3, NULL, NULL and lose 4 and 5. `COALESCE(a.id, b.key)` gives 1, 2, 3, 4, 5. Grouping by `a.id` collapses 4 and 5 into one NULL group (2 rows, sum of y = 40 + 50 = 90); grouping by the coalesced key gives five groups.

**Code:** run with `python3 -I`; the coalesced SQL result is compared with both pandas forms (sorted by `id`), and the grouped totals are compared too.
```python
# Q39: FULL OUTER JOIN key columns: a.id and b.key are each NULL on one side; COALESCE, USING, pandas left_on/right_on vs on
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE a(id INTEGER, x TEXT);
CREATE TABLE b(key INTEGER, y INTEGER);
CREATE TABLE b2(id INTEGER, y INTEGER);          -- same data as b, key column renamed to id for USING
INSERT INTO a VALUES (1,'a1'),(2,'a2'),(3,'a3');
INSERT INTO b VALUES (2,20),(3,30),(4,40),(5,50);
INSERT INTO b2 SELECT key, y FROM b;
"""
SQL_RAW = "SELECT a.id, b.key, a.x, b.y FROM a FULL OUTER JOIN b ON a.id = b.key"
SQL_MAIN = """
SELECT COALESCE(a.id, b.key) AS id, a.x, b.y
FROM a FULL OUTER JOIN b ON a.id = b.key
ORDER BY id
"""
SQL_USING = "SELECT id, x, y FROM a FULL OUTER JOIN b2 USING (id) ORDER BY id"
SQL_GROUP_WRONG = """
SELECT a.id AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY a.id ORDER BY a.id
"""
SQL_GROUP_RIGHT = """
SELECT COALESCE(a.id, b.key) AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY COALESCE(a.id, b.key) ORDER BY grp
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
show = lambda q: print(pd.read_sql_query(q, con).to_string(index=False))
print("raw FULL JOIN, both key columns:"); show(SQL_RAW)
print("\nCOALESCE(a.id, b.key):"); show(SQL_MAIN)
print("\nUSING (id) on b2, SELECT id:"); show(SQL_USING)
print("\nGROUP BY a.id (wrong, right-only keys collapse into one NULL group):"); show(SQL_GROUP_WRONG)
print("\nGROUP BY COALESCE(a.id, b.key):"); show(SQL_GROUP_RIGHT)

# pandas
a = pd.read_sql_query("SELECT * FROM a", con)
b = pd.read_sql_query("SELECT * FROM b", con)
m_lr = a.merge(b, left_on="id", right_on="key", how="outer")
print("\npandas outer, left_on='id' right_on='key' (both columns kept):")
print(m_lr.to_string(index=False)); print("id and key dtypes:", m_lr[["id", "key"]].dtypes.astype(str).to_dict())
m_on = a.merge(b.rename(columns={"key": "id"}), on="id", how="outer")
print("\npandas outer, on='id' after renaming b.key to id (one coalesced column):")
print(m_on.to_string(index=False)); print("id dtype:", str(m_on["id"].dtype))

# the coalesced frame from left_on/right_on, and the group-by
m_lr["id"] = m_lr["id"].fillna(m_lr["key"])
p_main = m_lr[["id", "x", "y"]].sort_values("id").reset_index(drop=True)
sql_main = pd.read_sql_query(SQL_MAIN, con)
pd.testing.assert_frame_equal(sql_main, p_main.astype({"id": "int64", "y": "float64"}), check_dtype=False)
pd.testing.assert_frame_equal(sql_main, m_on[["id", "x", "y"]].sort_values("id").reset_index(drop=True), check_dtype=False)
lr = a.merge(b, left_on="id", right_on="key", how="outer")           # id still has NaN for right-only rows
agg = dict(n_rows=("y", "size"), sum_y=("y", lambda s: s.sum(min_count=1)))
print("\npandas groupby('id') on the uncoalesced column, default dropna=True (right-only rows vanish):")
print(lr.groupby("id").agg(**agg).reset_index().to_string(index=False))
print("pandas groupby('id', dropna=False) (the SQL-like NULL group):")
print(lr.groupby("id", dropna=False).agg(**agg).reset_index().to_string(index=False))
g_right = m_on.groupby("id").agg(**agg).reset_index()
print("\npandas groupby on the coalesced id:"); print(g_right.to_string(index=False))
sql_g = pd.read_sql_query(SQL_GROUP_RIGHT, con)
pd.testing.assert_frame_equal(sql_g.rename(columns={"grp": "id"}), g_right, check_dtype=False)
print("asserts passed: SQL == pandas (sorted by id)")
con.close()
```

**Output (my run):**
```text
raw FULL JOIN, both key columns:
 id  key   x    y
1.0  NaN  a1  NaN
2.0  2.0  a2 20.0
3.0  3.0  a3 30.0
NaN  4.0 NaN 40.0
NaN  5.0 NaN 50.0

COALESCE(a.id, b.key):
 id   x    y
  1  a1  NaN
  2  a2 20.0
  3  a3 30.0
  4 NaN 40.0
  5 NaN 50.0

USING (id) on b2, SELECT id:
 id   x    y
  1  a1  NaN
  2  a2 20.0
  3  a3 30.0
  4 NaN 40.0
  5 NaN 50.0

GROUP BY a.id (wrong, right-only keys collapse into one NULL group):
 grp  n_rows  sum_y
 NaN       2   90.0
 1.0       1    NaN
 2.0       1   20.0
 3.0       1   30.0

GROUP BY COALESCE(a.id, b.key):
 grp  n_rows  sum_y
   1       1    NaN
   2       1   20.0
   3       1   30.0
   4       1   40.0
   5       1   50.0

pandas outer, left_on='id' right_on='key' (both columns kept):
 id   x  key    y
1.0  a1  NaN  NaN
2.0  a2  2.0 20.0
3.0  a3  3.0 30.0
NaN NaN  4.0 40.0
NaN NaN  5.0 50.0
id and key dtypes: {'id': 'float64', 'key': 'float64'}

pandas outer, on='id' after renaming b.key to id (one coalesced column):
 id   x    y
  1  a1  NaN
  2  a2 20.0
  3  a3 30.0
  4 NaN 40.0
  5 NaN 50.0
id dtype: int64

pandas groupby('id') on the uncoalesced column, default dropna=True (right-only rows vanish):
 id  n_rows  sum_y
1.0       1    NaN
2.0       1   20.0
3.0       1   30.0
pandas groupby('id', dropna=False) (the SQL-like NULL group):
 id  n_rows  sum_y
1.0       1    NaN
2.0       1   20.0
3.0       1   30.0
NaN       2   90.0

pandas groupby on the coalesced id:
 id  n_rows  sum_y
  1       1    NaN
  2       1   20.0
  3       1   30.0
  4       1   40.0
  5       1   50.0
asserts passed: SQL == pandas (sorted by id)
```

**Edge cases:**
- **Both sides NULL:** if a row in `a` has `id = NULL`, `COALESCE` returns the other side's key (also NULL if it is unmatched), and NULL keys never match each other in a SQL join (see Q6).
- **Sums over missing:** SQL `SUM(b.y)` for key 1 is NULL (no `b` rows). pandas `sum()` of an all-NaN group gives 0.0, which my first run showed as a mismatch against SQL; the Code block uses `sum(min_count=1)` to get NaN like SQL.
- **pandas groupby drops NaN keys:** `groupby("id")` on the uncoalesced column dropped the NaN group (keys 4 and 5 vanished from the totals); `dropna=False` kept them as one NaN group, like SQL.
- **dtypes:** with `left_on`/`right_on` the key columns became `float64` (NaN needs float); with `on=` the key stayed `int64`.
- **Which column is "right"?** `a.id` is the left key and `b.key` the right key; with `on=` pandas fills both into one column.

**Then explain:**
- **Why:** a full join keeps unmatched rows from both sides; for each unmatched row the other side's columns are NULL, including its key column.
- **SQL fixes:** `COALESCE(a.id, b.key)` in SELECT, GROUP BY and any later join; or `USING (id)` where supported.
- **pandas:** `on="id"` (same name on both sides) returns one key column, filled from whichever side has it; `left_on`/`right_on` returns both, like SQL's raw output.
- **Downstream GROUP BY:** group by the coalesced expression. In my run, `GROUP BY a.id` gave 4 groups (one NULL group of 2 rows summing 90) where the coalesced version gave 5.
- **Dialect (not executed):** in SQLite `SELECT l.id, r.id` with USING in a FULL JOIN kept the sides separate (see Q43 for the run), while `SELECT id` was coalesced; other engines differ in details, so check the manual.

**Follow-ups:**
- *What does `SELECT *` return for USING versus ON?* One key column versus both (verified for SQLite in Q43).
- *Can you ORDER BY the key?* Order by the coalesced expression (or its alias), otherwise NULL keys sort together.
- *What if the key names differ in pandas but you want one column?* Rename before the merge, or merge with `left_on`/`right_on` and then `fillna` as in the Code block.

**Common mistakes:**
- Selecting `a.id` and reporting the right-only rows with a NULL id.
- `GROUP BY a.id` after a full join.
- `WHERE a.id IS NULL` to find "only in b", when that is correct but then using `a.id` as the display key.
- Expecting `merge(left_on=..., right_on=...)` to merge the key columns for you.

### Q40 ⭐ 🟡 Row count changed after adding a join (1,000 rows became 1,400). Describe a systematic diagnosis: define the grain you expect, compare COUNT(*) with COUNT(DISTINCT key) before and after, find the duplicated join keys with GROUP BY ... HAVING, test the join in isolation, and add guards (unique constraints, row-count assertions, validate= in pandas). Include a small worked example with a dimension table that has two current rows per key.
**Asked at:** data-modelling write-ups on fan and chasm traps (Coginiti, Sisense, Holistics; snippets), not candidate reports; analyst and data scientist rounds and BI debugging
**Say this first (1 line):** If 1,000 rows became 1,400, the join key is not unique on the side you added: define the expected grain, compare `COUNT(*)` with `COUNT(DISTINCT key)` before and after, find the duplicated keys with `GROUP BY ... HAVING COUNT(*) > 1`, test the join in isolation, then fix the data and add a guard.

**Schema and sample data:** 1,000 orders, 10 per customer for customers 1 to 100 (amount 10 each, so revenue is 10,000). `customer_dim` is a type 2 style table with an `is_current` flag. Customers 1 to 40 wrongly have two current rows, customers 41 to 60 have one old row and one current row (normal), and customers 61 to 100 have one current row. The Code block builds the data with a loop; the tables are:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE customer_dim(customer_id INTEGER, segment TEXT, valid_from TEXT, is_current INTEGER);
```

**SQL answer:** the diagnosis queries run in the Code block, in order; the join that breaks and the fix are:
```sql
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o JOIN customer_dim d ON d.customer_id = o.customer_id AND d.is_current = 1
```
```sql
SELECT customer_id, COUNT(*) AS n FROM customer_dim WHERE is_current = 1
GROUP BY customer_id HAVING COUNT(*) > 1 ORDER BY customer_id
```
```sql
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o
JOIN customer_dim d
  ON d.customer_id = o.customer_id AND d.is_current = 1
 AND d.valid_from = (SELECT MAX(d2.valid_from) FROM customer_dim d2
                     WHERE d2.customer_id = d.customer_id AND d2.is_current = 1)
ORDER BY o.order_id
```
The fix picks the latest `valid_from` among the current rows, which is a business rule I chose for the example (the right rule depends on your data); it is better to repair the dimension at the source.

**pandas answer:** (same text as in the Code block)
```py
cur = cdim[cdim["is_current"] == 1]
orders.merge(cur, on="customer_id", validate="many_to_one")
latest = cur.sort_values("valid_from").drop_duplicates("customer_id", keep="last")
```

**Example:** the arithmetic is checkable by hand. 40 customers have two current rows, so each of their 10 orders matches twice: 40 customers x 10 orders x 1 extra row = 400 extra rows, 1,000 + 400 = 1,400. `SUM(amount)` goes from 10,000 to 14,000. Customers 41 to 60 do not add rows because their old row has `is_current = 0` and is filtered out in the join.

**Code:** run with `python3 -I`; the fixed SQL and fixed pandas results are compared sorted by `order_id`, and the row count is asserted to be 1,000.
```python
# Q40: 1,000 rows became 1,400 after a join: diagnose with COUNT(*) vs COUNT(DISTINCT), duplicated keys, isolation, guards
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE customer_dim(customer_id INTEGER, segment TEXT, valid_from TEXT, is_current INTEGER);
""")
# 1,000 orders, 10 per customer for customers 1..100
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i - 1) % 100 + 1, 10) for i in range(1, 1001)])
dim = []
for c in range(1, 101):
    if c <= 40:                                        # the bug: two 'current' rows for customers 1..40
        dim += [(c, "gold", "2025-01-01", 1), (c, "silver", "2025-06-01", 1)]
    elif c <= 60:                                      # normal history: one old row (not current) + one current
        dim += [(c, "bronze", "2024-01-01", 0), (c, "gold", "2025-01-01", 1)]
    else:
        dim.append((c, "gold", "2025-01-01", 1))
con.executemany("INSERT INTO customer_dim VALUES (?,?,?,?)", dim)

one = lambda q: con.execute(q).fetchone()
print("1. grain of orders: COUNT(*), COUNT(DISTINCT order_id) =", one("SELECT COUNT(*), COUNT(DISTINCT order_id) FROM orders"))

SQL_BAD = """
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o JOIN customer_dim d ON d.customer_id = o.customer_id AND d.is_current = 1
"""
print("2. after the join: COUNT(*), COUNT(DISTINCT order_id), SUM(amount) =",
      one(f"SELECT COUNT(*), COUNT(DISTINCT order_id), SUM(amount) FROM ({SQL_BAD})"), "(true SUM was 10000)")

SQL_DUPKEYS = """
SELECT customer_id, COUNT(*) AS n FROM customer_dim WHERE is_current = 1
GROUP BY customer_id HAVING COUNT(*) > 1 ORDER BY customer_id
"""
dups = con.execute(SQL_DUPKEYS).fetchall()
print("3. duplicated current keys:", len(dups), "keys, first three:", dups[:3])
print("   expected extra rows = SUM(n - 1) x orders per key =", sum(n - 1 for _, n in dups), "x 10 =",
      sum(n - 1 for _, n in dups) * 10)
print("4. isolate one key:", con.execute("SELECT * FROM customer_dim WHERE customer_id = 1").fetchall())

# fix in the query: pick the latest current row per key
SQL_FIX = """
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o
JOIN customer_dim d
  ON d.customer_id = o.customer_id AND d.is_current = 1
 AND d.valid_from = (SELECT MAX(d2.valid_from) FROM customer_dim d2
                     WHERE d2.customer_id = d.customer_id AND d2.is_current = 1)
ORDER BY o.order_id
"""
fixed = pd.read_sql_query(SQL_FIX, con)
print("5. fixed join rows:", len(fixed), "| SUM(amount):", fixed["amount"].sum())

# pandas: same diagnosis and fix
orders = pd.read_sql_query("SELECT * FROM orders", con)
cdim = pd.read_sql_query("SELECT * FROM customer_dim", con)
cur = cdim[cdim["is_current"] == 1]
try:
    orders.merge(cur, on="customer_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("\npandas validate='many_to_one' ->", type(e).__name__ + ":", e)
print("pandas duplicated current keys:", int(cur["customer_id"].duplicated().sum()))
bad = orders.merge(cur, on="customer_id")
print("pandas unvalidated merge rows:", len(bad), "| sum amount:", bad["amount"].sum())
latest = cur.sort_values("valid_from").drop_duplicates("customer_id", keep="last")
p_fixed = (orders.merge(latest[["customer_id", "segment"]], on="customer_id", how="inner", validate="many_to_one")
           .sort_values("order_id").reset_index(drop=True))
pd.testing.assert_frame_equal(fixed[["order_id", "customer_id", "amount", "segment"]], p_fixed, check_dtype=False)
assert len(p_fixed) == len(orders) == 1000
print("asserts passed: SQL fix == pandas fix (sorted by order_id), row count 1000 == orders")

# guard at the source: a partial unique index makes the duplicate load fail
con.execute("DELETE FROM customer_dim WHERE customer_id <= 40 AND valid_from = '2025-01-01'")
con.execute("CREATE UNIQUE INDEX one_current ON customer_dim(customer_id) WHERE is_current = 1")
try:
    con.execute("INSERT INTO customer_dim VALUES (1, 'gold', '2026-01-01', 1)")
except sqlite3.IntegrityError as e:
    print("\nunique partial index ->", type(e).__name__ + ":", e)
con.close()
```

**Output (my run):**
```text
1. grain of orders: COUNT(*), COUNT(DISTINCT order_id) = (1000, 1000)
2. after the join: COUNT(*), COUNT(DISTINCT order_id), SUM(amount) = (1400, 1000, 14000) (true SUM was 10000)
3. duplicated current keys: 40 keys, first three: [(1, 2), (2, 2), (3, 2)]
   expected extra rows = SUM(n - 1) x orders per key = 40 x 10 = 400
4. isolate one key: [(1, 'gold', '2025-01-01', 1), (1, 'silver', '2025-06-01', 1)]
5. fixed join rows: 1000 | SUM(amount): 10000

pandas validate='many_to_one' -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  customer_id
           1
           2
           3
           4
           5 ...
pandas duplicated current keys: 40
pandas unvalidated merge rows: 1400 | sum amount: 14000
asserts passed: SQL fix == pandas fix (sorted by order_id), row count 1000 == orders

unique partial index -> IntegrityError: UNIQUE constraint failed: customer_dim.customer_id
```

**Edge cases:**
- **Row count unchanged but totals wrong:** a join can also drop one row and duplicate another, so also compare `SUM` and `COUNT(DISTINCT order_id)`, not only `COUNT(*)`.
- **A LEFT JOIN with no match:** keeps the row once, so shrinking row counts point to an INNER JOIN or a filter in WHERE.
- **NULL keys:** orders with a NULL key match nothing and are not duplicated.
- **The unique index guard:** my partial unique index on `customer_id WHERE is_current = 1` made the duplicate insert fail with `IntegrityError`. Partial indexes exist in SQLite and PostgreSQL; MySQL and others differ (hedged, not executed).
- **pandas `MergeError` message:** it lists the duplicated key values (it printed customers 1 to 5 and `...`).

**Then explain:**
- **Step 1, grain:** say it out loud: one row per order. Check the base: 1,000 rows, 1,000 distinct `order_id`.
- **Step 2, after the join:** 1,400 rows but still 1,000 distinct `order_id` means fan-out (some orders repeated).
- **Step 3, find it:** group the joined table's key by `HAVING COUNT(*) > 1` (40 keys with 2 rows).
- **Step 4, isolate:** look at one key (customer 1 has two current rows), and run the join alone without other joins.
- **Step 5, guards:** a unique or partial unique index in the table, a row-count assertion after the join, `validate="many_to_one"` in pandas, and a dimension test in the pipeline.
- **Fix at the source versus in the query:** a query fix hides bad data and has to be repeated everywhere; fix the dimension load and keep the query guard as a second line.

**Follow-ups:**
- *What if the row count went down?* Look for an INNER JOIN or a WHERE on the right table; compare `left_only` rows.
- *Which is faster to detect, count or sum?* Both; sums catch duplicated rows that still keep distinct counts looking fine.
- *How would a dbt style test express this?* A unique test on the dimension key (a concept; not run here).

**Common mistakes:**
- Papering over it with `SELECT DISTINCT`, which hides the cause and can delete legitimate duplicates.
- Checking only the row count of the final query.
- Joining before checking uniqueness of the lookup table.
- Fixing the query but leaving the bad dimension for the next report.

### Q41 ⭐ 🔴 Join performance at concept level: explain nested-loop, hash and merge joins in plain words, why an index on the join key (and on the foreign key column, not just the primary key) helps, why filtering before joining and selecting fewer columns helps, why functions on join columns (ON LOWER(a.email) = LOWER(b.email) or casts) defeat indexes, and why a missing ON clause explodes. Hedge by engine and say deeper work and EXPLAIN belong to Part 11.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** A join is a nested loop, a hash join or a merge join; indexes on the join columns (especially the foreign key side) let the engine look up matches instead of scanning, filters before the join shrink the inputs, functions on join columns hide the column from the index, and a missing `ON` is a Cartesian product; deeper plan reading is Part 11.

**Schema and sample data:** 200 customers (4 cities, an email in mixed case), 2,000 orders (10 per customer), 100 leads with lower-case emails. The Code block creates them with loops; the tables are:
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, email TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE leads(lead_id INTEGER PRIMARY KEY, email TEXT);
```

**SQL answer:** the Code block runs `EXPLAIN QUERY PLAN` (SQLite's plan output, enough for concepts; Part 11 is the proper place) on the foreign key join before and after `CREATE INDEX ix_orders_customer ON orders(customer_id)`, on the `LOWER()` join before and after an expression index, and counts the rows of a join with no `ON`. The filter-first comparison uses these two queries, which return the same result:
```sql
SELECT c.city, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount >= 25 GROUP BY c.city ORDER BY c.city
```
```sql
SELECT c.city, SUM(o.amount) AS total FROM customers c
JOIN (SELECT customer_id, amount FROM orders WHERE amount >= 25) o ON o.customer_id = c.customer_id
GROUP BY c.city ORDER BY c.city
```

**pandas answer:** filter, then merge (same text as in the Code block):
```py
p = (customers.merge(orders[orders["amount"] >= 25][["customer_id", "amount"]], on="customer_id")
     .groupby("city", as_index=False).agg(total=("amount", "sum")).sort_values("city").reset_index(drop=True))
```

**Example:** the three join algorithms in plain words.
- **Nested loop:** for each row of the outer table, look up matching rows in the inner table. With an index on the inner join column each lookup is cheap; without one, it scans the inner table every time. Good for small outer inputs.
- **Hash join:** build an in-memory hash table on the smaller input, then stream the larger one and probe it. Good for large unsorted inputs and equality joins; needs memory.
- **Merge join:** sort both inputs on the key (or read them already sorted from an index) and walk through them together. Good when both sides are sorted or very large.
- In my run: 200 customers x 2,000 orders with no `ON` gave 400,000 rows.

**Code:** run with `python3 -I`; the SQL variants are compared with each other and with the pandas filter-then-merge result.
```python
# Q41: join performance at concept level: plans before/after an index, function on a join column, missing ON, filter-first
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, email TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE leads(lead_id INTEGER PRIMARY KEY, email TEXT);
""")
cities = ["Pune", "Delhi", "Chennai", "Kolkata"]
con.executemany("INSERT INTO customers VALUES (?,?,?)",
                [(i, f"User{i}@Example.com", cities[i % 4]) for i in range(1, 201)])
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i * 7) % 200 + 1, i % 50) for i in range(1, 2001)])
con.executemany("INSERT INTO leads VALUES (?,?)", [(i, f"user{i}@example.com") for i in range(1, 101)])

def plan(q):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q).fetchall()]

Q_FK = "SELECT COUNT(*) FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'"
print("1. join on the foreign key, no index on orders.customer_id:"); [print("   ", p) for p in plan(Q_FK)]
con.execute("CREATE INDEX ix_orders_customer ON orders(customer_id)")
print("   after CREATE INDEX ix_orders_customer:"); [print("   ", p) for p in plan(Q_FK)]

Q_FUNC = "SELECT COUNT(*) FROM leads l JOIN customers c ON LOWER(c.email) = LOWER(l.email)"
Q_PLAIN = "SELECT COUNT(*) FROM leads l JOIN customers c ON c.email = l.email"
print("\n2. LOWER() on both join columns (no index on email yet):"); [print("   ", p) for p in plan(Q_FUNC)]
con.execute("CREATE INDEX ix_cust_email_lower ON customers(LOWER(email))")
print("   after an index on the expression LOWER(email):"); [print("   ", p) for p in plan(Q_FUNC)]
print("   matches:", con.execute(Q_FUNC).fetchone()[0], "| plain equality matches (case differs):", con.execute(Q_PLAIN).fetchone()[0])

n_c, n_o = 200, 2000
print("\n3. missing ON (comma join without a condition):",
      con.execute("SELECT COUNT(*) FROM customers c, orders o").fetchone()[0], "rows =", n_c, "x", n_o)

# 4. filter before join gives the same answer as filter after
Q_AFTER = """SELECT c.city, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount >= 25 GROUP BY c.city ORDER BY c.city"""
Q_BEFORE = """SELECT c.city, SUM(o.amount) AS total FROM customers c
JOIN (SELECT customer_id, amount FROM orders WHERE amount >= 25) o ON o.customer_id = c.customer_id
GROUP BY c.city ORDER BY c.city"""
s_after = pd.read_sql_query(Q_AFTER, con)
s_before = pd.read_sql_query(Q_BEFORE, con)
pd.testing.assert_frame_equal(s_after, s_before)
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
p = (customers.merge(orders[orders["amount"] >= 25][["customer_id", "amount"]], on="customer_id")
     .groupby("city", as_index=False).agg(total=("amount", "sum")).sort_values("city").reset_index(drop=True))
pd.testing.assert_frame_equal(s_before, p, check_dtype=False)
print("\n4. filter-first SQL == filter-after SQL == pandas filter-then-merge (sorted by city):")
print(p.to_string(index=False))
big = customers.merge(orders, how="cross")
print("pandas cross merge rows:", len(big))
con.close()
```

**Output (my run):**
```text
1. join on the foreign key, no index on orders.customer_id:
    SCAN o
    SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   after CREATE INDEX ix_orders_customer:
    SCAN c
    SEARCH o USING COVERING INDEX ix_orders_customer (customer_id=?)

2. LOWER() on both join columns (no index on email yet):
    SCAN l
    SCAN c
   after an index on the expression LOWER(email):
    SCAN l
    SEARCH c USING INDEX ix_cust_email_lower (<expr>=?)
   matches: 100 | plain equality matches (case differs): 0

3. missing ON (comma join without a condition): 400000 rows = 200 x 2000

4. filter-first SQL == filter-after SQL == pandas filter-then-merge (sorted by city):
   city  total
Chennai   9620
  Delhi   8880
Kolkata   8880
   Pune   9620
pandas cross merge rows: 400000
```

**Edge cases:**
- **What I ran versus what I know:** the plans above are SQLite's. SQLite's plans only show scans and index searches (nested-loop style), which is why I describe hash and merge joins from general knowledge of other engines (PostgreSQL, SQL Server, Oracle, MySQL 8 and others differ in which algorithms exist and when they choose them); not executed here.
- **The planner can change the join order:** before the index SQLite scanned `orders` and looked up each customer by primary key; after the index it scanned the (city filtered) customers and used the index on `orders.customer_id`. The same query got a different plan, which is the point of indexing the foreign key.
- **Primary keys are indexed, foreign keys usually are not** (in most engines a foreign key column does not get an index automatically); the many side (`orders.customer_id`) is where joins and deletes need one.
- **Functions on join columns:** `LOWER(c.email) = LOWER(l.email)` scanned both tables (two `SCAN` lines). An index on the expression `LOWER(email)` let SQLite search customers; engines that support expression or function-based indexes behave similarly, others need a stored normalised column (hedged).
- **Casts and mismatched types** have the same effect as functions on the column (Q35).
- **Small tables:** a full scan can be the best plan; do not index everything.

**Then explain:**
- **Why an index on the foreign key helps:** the join asks "which orders belong to this customer", and without an index on `orders.customer_id` the engine must read all orders for each customer or build a temporary structure.
- **Why filter before the join (when it is safe):** fewer rows go into the join and the aggregation; in an INNER JOIN the optimiser usually pushes the filter down itself, so the written order often does not matter (my run gave the same result both ways; I did not time it). For a LEFT JOIN, moving a filter changes the result (Q3).
- **Fewer columns:** wide rows cost memory in sorts and hash tables; select only what you need.
- **Missing ON:** the result is the Cartesian product, 200 x 2,000 = 400,000 rows here, and pandas `how="cross"` made the same 400,000 rows.
- **Where it goes next:** reading `EXPLAIN`, statistics, join hints and partitioning are Part 11.

**Follow-ups:**
- *When is a hash join better than a nested loop?* When there is no useful index and both inputs are large.
- *What about a composite index?* Put the equality columns first; order matters (concept; Part 11).
- *Does `SELECT *` matter for joins?* Yes: it blocks covering-index plans and moves extra bytes.

**Common mistakes:**
- Indexing the primary key and forgetting the foreign key.
- Wrapping join columns in `LOWER`, `CAST` or `DATE`.
- Joining first, filtering later, on a LEFT JOIN where the filter changes meaning.
- Claiming one join algorithm is always best.

### Q42 ⭐ 🔴 Join, EXISTS and IN are not always interchangeable: orders(order_id, customer_id) has several rows per customer. Show a case where JOIN returns duplicates and EXISTS does not, a case where NOT IN returns nothing because of a NULL, and a case where the three agree. State a rule for choosing between them for existence checks versus fetching columns from the other table, and the matching pandas idioms.
**Asked at:** explainextended and SQL Server Central write-ups on NOT IN, NOT EXISTS and LEFT JOIN / IS NULL, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `JOIN` returns one row per match, so it duplicates a customer who has several orders; `EXISTS` and `IN` only test for existence and return the customer once; `NOT IN` silently returns nothing if the subquery has a NULL; and `NOT EXISTS` or a `LEFT JOIN ... IS NULL` is the safe "does not exist" form.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);      -- several rows per customer, one NULL
CREATE TABLE orders_clean(order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL UNIQUE);  -- one row per customer, no NULL
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,1),(104,2),(105,NULL);
INSERT INTO orders_clean VALUES (201,1),(202,2);
```
`orders` has several rows for customer 1 and a NULL customer (guest). `orders_clean` has one row per customer and no NULL.

**SQL answer:** the Code block builds six queries per table with `queries(t)`: `JOIN`, `EXISTS`, `IN`, `NOT EXISTS`, `NOT IN` and `LEFT JOIN IS NULL`. With `t` standing for the table name (`orders` or `orders_clean`), the text in the code is:
```sql
SELECT c.name FROM customers c JOIN {t} o ON o.customer_id = c.customer_id ORDER BY c.customer_id
```
```sql
SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id
```
```sql
SELECT c.name FROM customers c WHERE c.customer_id NOT IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id
```
The Code block fills `{t}` with an f-string; `NOT EXISTS`, `IN` and `LEFT JOIN IS NULL` follow the same pattern in `queries`.

**pandas answer:** (same text as in the Code block)
```py
p_join = customers.merge(orders, on="customer_id").sort_values(["customer_id", "order_id"])["name"].tolist()
p_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_not = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
```

**Example:** customers Asha (1), Ben (2), Chitra (3), Dev (4); orders 101, 102, 103 belong to Asha, 104 to Ben, 105 has a NULL customer.
- "Customers who ordered": `JOIN` gives Asha, Asha, Asha, Ben (4 rows, one per order). `EXISTS` and `IN` give Asha, Ben.
- "Customers who never ordered": `NOT EXISTS` and `LEFT JOIN ... IS NULL` give Chitra, Dev. `NOT IN` gives nothing, because the subquery contains the NULL from order 105, so `3 NOT IN (1, 2, NULL)` is UNKNOWN, not TRUE.
- Where they agree: in `orders_clean` (one order per customer, no NULL) `JOIN`, `EXISTS` and `IN` all give Asha, Ben, and the three "never ordered" forms all give Chitra, Dev.

**Code:** run with `python3 -I`; the asserts check each claim above and compare the pandas lists with the SQL form named in the label, in `customer_id` order.
```python
# Q42: JOIN vs EXISTS vs IN: duplicates, the NOT IN NULL trap, and a case where all forms agree
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);      -- several rows per customer, one NULL
CREATE TABLE orders_clean(order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL UNIQUE);  -- one row per customer, no NULL
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,1),(104,2),(105,NULL);
INSERT INTO orders_clean VALUES (201,1),(202,2);
"""
def queries(t):
    return {
        "JOIN":        f"SELECT c.name FROM customers c JOIN {t} o ON o.customer_id = c.customer_id ORDER BY c.customer_id",
        "EXISTS":      f"SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id",
        "IN":          f"SELECT c.name FROM customers c WHERE c.customer_id IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id",
        "NOT EXISTS":  f"SELECT c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id",
        "NOT IN":      f"SELECT c.name FROM customers c WHERE c.customer_id NOT IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id",
        "LEFT JOIN IS NULL": f"SELECT c.name FROM customers c LEFT JOIN {t} o ON o.customer_id = c.customer_id WHERE o.order_id IS NULL ORDER BY c.customer_id",
    }
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for t in ("orders", "orders_clean"):
    print(f"--- table {t}")
    res[t] = {k: [r[0] for r in con.execute(q).fetchall()] for k, q in queries(t).items()}
    for k, v in res[t].items():
        print(f"{k:>18}: {v}")

# the three existence forms agree on the clean table, JOIN differs on the duplicated table, NOT IN fails on NULLs
c = res["orders_clean"]
assert c["JOIN"] == c["EXISTS"] == c["IN"] == ["Asha", "Ben"]
assert c["NOT EXISTS"] == c["NOT IN"] == c["LEFT JOIN IS NULL"] == ["Chitra", "Dev"]
d = res["orders"]
assert d["JOIN"] == ["Asha", "Asha", "Asha", "Ben"] and d["EXISTS"] == d["IN"] == ["Asha", "Ben"]
assert d["NOT IN"] == [] and d["NOT EXISTS"] == d["LEFT JOIN IS NULL"] == ["Chitra", "Dev"]

# pandas idioms
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
p_join = customers.merge(orders, on="customer_id").sort_values(["customer_id", "order_id"])["name"].tolist()
p_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_semi = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id").sort_values("customer_id")["name"].tolist()
p_not = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
          .query("_merge == 'left_only'").sort_values("customer_id")["name"].tolist())
print("\npandas merge (like JOIN):", p_join)
print("pandas isin (like EXISTS/IN):", p_in)
print("pandas merge on dropped-duplicate keys (semi-join):", p_semi)
print("pandas ~isin (like NOT EXISTS, NOT like NOT IN):", p_not)
print("pandas anti-join via indicator:", p_anti)
assert p_join == d["JOIN"] and p_in == p_semi == d["EXISTS"] and p_not == p_anti == d["NOT EXISTS"]
print("asserts passed: pandas matches the SQL form named in each label (lists in customer_id order)")
con.close()
```

**Output (my run):**
```text
--- table orders
              JOIN: ['Asha', 'Asha', 'Asha', 'Ben']
            EXISTS: ['Asha', 'Ben']
                IN: ['Asha', 'Ben']
        NOT EXISTS: ['Chitra', 'Dev']
            NOT IN: []
 LEFT JOIN IS NULL: ['Chitra', 'Dev']
--- table orders_clean
              JOIN: ['Asha', 'Ben']
            EXISTS: ['Asha', 'Ben']
                IN: ['Asha', 'Ben']
        NOT EXISTS: ['Chitra', 'Dev']
            NOT IN: ['Chitra', 'Dev']
 LEFT JOIN IS NULL: ['Chitra', 'Dev']

pandas merge (like JOIN): ['Asha', 'Asha', 'Asha', 'Ben']
pandas isin (like EXISTS/IN): ['Asha', 'Ben']
pandas merge on dropped-duplicate keys (semi-join): ['Asha', 'Ben']
pandas ~isin (like NOT EXISTS, NOT like NOT IN): ['Chitra', 'Dev']
pandas anti-join via indicator: ['Chitra', 'Dev']
asserts passed: pandas matches the SQL form named in each label (lists in customer_id order)
```

**Edge cases:**
- **JOIN duplicates are a feature when you need columns from orders** (for example the order amount), and a bug when you only need the customer.
- **`IN` with NULL on the positive side is fine** (it can still be TRUE); only `NOT IN` breaks.
- **`SELECT DISTINCT` after a JOIN** fixes the duplicates for existence checks but costs a sort or hash, and it hides fan-out when you also select other columns.
- **Empty subquery:** `NOT IN` returns every customer, `NOT EXISTS` also.
- **pandas:** `~isin` ignores the NULL problem and returns Chitra and Dev (it matches `NOT EXISTS`, not the SQL `NOT IN`), which is why SQL and pandas answers differ in the trap case. NaN in `isin` is covered in Part 1 Q13.

**Then explain:**
- **Rule 1:** if you only need to test whether a related row exists, use `EXISTS` (or `NOT EXISTS`); it is NULL-safe and cannot duplicate rows.
- **Rule 2:** if you need columns from the other table, use a `JOIN`, and make sure you know the grain (one row per match) or aggregate first.
- **Rule 3:** use `IN` when the subquery column is `NOT NULL`, or filter NULLs in it; avoid `NOT IN` unless you can guarantee that.
- **Performance:** the optimiser often turns these into the same semi-join or anti-join plan, but that is engine specific (hedged, not executed); correctness differences matter first.
- **pandas idioms:** `merge` is the JOIN (duplicates included), `isin` or a merge on `drop_duplicates()` keys is the semi-join, `~isin` or `merge(..., indicator=True)` with `left_only` is the anti-join.

**Follow-ups:**
- *Is `EXISTS` slower than `IN`?* Not necessarily; a modern optimiser usually plans both as a semi-join (hedged, engine dependent).
- *What about `<> ALL`?* It is the same as `NOT IN` and has the same NULL problem.
- *How do you return one row per customer with the latest order amount?* That needs a join plus a selection rule (Part 4); `EXISTS` alone cannot return columns.

**Common mistakes:**
- Using `JOIN` for an existence check and then counting customers with `COUNT(*)`.
- Using `NOT IN` against a nullable column.
- Believing the three are always interchangeable.
- Fixing duplicates with `DISTINCT` and not noticing the fan-out in other columns.

### Q43 ⭐ 🔴 Dialect map for joins (answers must hedge and run only what SQLite can): FULL and RIGHT JOIN support (SQLite 3.39+, MySQL has neither FULL), EXCEPT versus MINUS, INTERSECT in MySQL, USING and NATURAL semantics, joined-column output order, cross join syntax (CROSS JOIN versus comma), and the lateral idea (not covered here). Present as a table with a 'verified by running on SQLite' column and a 'hedged, not executed' column.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** On SQLite 3.45.1 I ran INNER, LEFT, RIGHT, FULL, CROSS (both spellings), INTERSECT, EXCEPT, USING and NATURAL; MINUS, `<=>` and LATERAL failed there; everything about PostgreSQL, MySQL, Oracle, SQL Server, BigQuery and Snowflake in the table is from memory and not executed.

**Schema and sample data:** `l` has ids 1, 2, 3 and `r` has ids 2, 3, 4, so there are two matches, one left-only row and one right-only row.
```sql
CREATE TABLE l(id INTEGER, v TEXT);
CREATE TABLE r(id INTEGER, w TEXT);
INSERT INTO l VALUES (1,'l1'),(2,'l2'),(3,'l3');
INSERT INTO r VALUES (2,'r2'),(3,'r3'),(4,'r4');
```

**SQL answer:** the queries run in the Code block, with `attempt()` catching errors so a failing feature prints its error instead of stopping the script. The two columns the question asks for:

| Feature | Verified by running on SQLite 3.45.1 | Hedged, not executed |
|---|---|---|
| RIGHT JOIN | works; 3 rows; same rows as the LEFT JOIN with the tables swapped | PostgreSQL, SQL Server, Oracle, MySQL, BigQuery and Snowflake support it, to my knowledge; I believe SQLite added it in 3.39 (from memory; I only ran 3.45.1) |
| FULL OUTER JOIN | works; 4 rows | PostgreSQL, SQL Server, Oracle, BigQuery and Snowflake support it; MySQL has no FULL OUTER JOIN (the MySQL 8.4 join page shows only LEFT and RIGHT) |
| EXCEPT versus MINUS | `EXCEPT` works (returned 1); `MINUS` gave a syntax error | Oracle uses `MINUS` (older versions have no `EXCEPT`, as I recall); PostgreSQL, SQL Server, BigQuery and Snowflake use `EXCEPT` (Snowflake also accepts `MINUS`) |
| INTERSECT | works (returned 2 and 3) | MySQL support depends on version (added in 8.0.31 from memory; check your version) |
| USING | `SELECT *` returned `id, v, w` (one `id`); also worked with RIGHT and FULL JOIN | PostgreSQL and MySQL support it, with differences in how a qualified `l.id` behaves after an outer join; SQL Server does not support USING; check each manual |
| NATURAL JOIN | worked, same columns as USING (`id, v, w`) | supported in PostgreSQL, MySQL, Oracle and others (not SQL Server); it joins on all same-named columns (Q21) |
| Joined-column output order | ON: `id, v, id, w` (both keys, left columns then right); USING and NATURAL: the shared key first, then the rest | the standard puts the USING/NATURAL columns first; MySQL's join page documents the same coalesced order; I did not run MySQL |
| Cross join syntax | `CROSS JOIN` and the comma form both gave 9 rows | both are standard SQL and accepted widely; some engines or modes treat a comma join differently with precedence against explicit JOINs (hedged) |
| LATERAL | `LATERAL` gave a syntax error in SQLite | PostgreSQL, MySQL 8.0.14 and later and Snowflake support `LATERAL` (SQL Server uses `CROSS APPLY`); the lateral idea is not covered here |
| Null-safe equality | `IS NOT DISTINCT FROM` worked (returned 1) and `NULL IS NULL` returned 1; `<=>` gave a syntax error | PostgreSQL has `IS NOT DISTINCT FROM`; MySQL has `<=>`; others vary |

**pandas answer:** the parallels, run in the same Code block and compared by row count against the SQL result:
```py
l.merge(r, on="id", how="inner")
l.merge(r, on="id", how="outer")
l.merge(r, how="cross")
```
`how="right"` and `how="left"` map to the RIGHT and LEFT joins, `how="cross"` is CROSS JOIN, `on="id"` returns one key column like USING, and `left_on`/`right_on` returns both columns like ON. pandas has no NATURAL join (and `merge` with no `on` joins on all common column names by default, which is the same trap as NATURAL JOIN).

**Example:** by hand, INNER gives ids 2 and 3 (2 rows); LEFT adds id 1 (3 rows); RIGHT adds id 4 instead (3 rows); FULL has both unmatched rows (4 rows); CROSS is 3 x 3 = 9 rows. `l INTERSECT r` gives 2 and 3, and `l EXCEPT r` gives 1.

**Code:** run with `python3 -I`; it asserts the SQLite row counts equal the pandas counts, that RIGHT JOIN equals the swapped LEFT JOIN, and that INTERSECT and EXCEPT equal Python set operations on the ids.
```python
# Q43: join dialect map: run each feature on SQLite 3.45 and record what happens (other engines are NOT executed)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE l(id INTEGER, v TEXT);
CREATE TABLE r(id INTEGER, w TEXT);
INSERT INTO l VALUES (1,'l1'),(2,'l2'),(3,'l3');
INSERT INTO r VALUES (2,'r2'),(3,'r3'),(4,'r4');
""")
print("SQLite version:", sqlite3.sqlite_version)

def attempt(q):
    try:
        cur = con.execute(q)
        rows = cur.fetchall()
        return [d[0] for d in cur.description], rows
    except sqlite3.Error as e:
        return None, f"{type(e).__name__}: {e}"

l = pd.read_sql_query("SELECT * FROM l", con)
r = pd.read_sql_query("SELECT * FROM r", con)

# 1. join types: row counts, compared with pandas how=
checks = {
    "INNER JOIN":      ("SELECT * FROM l INNER JOIN r ON l.id = r.id", l.merge(r, on="id", how="inner")),
    "LEFT JOIN":       ("SELECT * FROM l LEFT JOIN r ON l.id = r.id", l.merge(r, on="id", how="left")),
    "RIGHT JOIN":      ("SELECT * FROM l RIGHT JOIN r ON l.id = r.id", l.merge(r, on="id", how="right")),
    "FULL OUTER JOIN": ("SELECT * FROM l FULL OUTER JOIN r ON l.id = r.id", l.merge(r, on="id", how="outer")),
    "CROSS JOIN":      ("SELECT * FROM l CROSS JOIN r", l.merge(r, how="cross")),
    "comma join":      ("SELECT * FROM l, r", l.merge(r, how="cross")),
}
print("\njoin type: SQLite rows | pandas rows")
for name, (q, pdf) in checks.items():
    cols, rows = attempt(q)
    assert isinstance(rows, list) and len(rows) == len(pdf), name
    print(f"{name:>16}: {len(rows)} | {len(pdf)}")
# RIGHT JOIN is the LEFT JOIN with the tables swapped (same rows, columns in a different order)
a = sorted(map(tuple, con.execute("SELECT r.id, r.w, l.v FROM l RIGHT JOIN r ON l.id = r.id").fetchall()), key=str)
b = sorted(map(tuple, con.execute("SELECT r.id, r.w, l.v FROM r LEFT JOIN l ON l.id = r.id").fetchall()), key=str)
assert a == b
print("RIGHT JOIN == swapped LEFT JOIN: True")

# 2. set operators
for name, q in [("INTERSECT", "SELECT id FROM l INTERSECT SELECT id FROM r"),
                ("EXCEPT", "SELECT id FROM l EXCEPT SELECT id FROM r"),
                ("MINUS", "SELECT id FROM l MINUS SELECT id FROM r")]:
    cols, rows = attempt(q)
    print(f"{name:>9}: {rows}")
assert [x[0] for x in con.execute("SELECT id FROM l INTERSECT SELECT id FROM r ORDER BY id")] == sorted(set(l.id) & set(r.id))
assert [x[0] for x in con.execute("SELECT id FROM l EXCEPT SELECT id FROM r ORDER BY id")] == sorted(set(l.id) - set(r.id))

# 3. USING / NATURAL / ON: which columns does SELECT * return, and in what order
print("\nSELECT * column lists:")
for name, q in [("ON", "SELECT * FROM l JOIN r ON l.id = r.id"),
                ("USING (id)", "SELECT * FROM l JOIN r USING (id)"),
                ("NATURAL JOIN", "SELECT * FROM l NATURAL JOIN r"),
                ("RIGHT JOIN USING", "SELECT * FROM l RIGHT JOIN r USING (id)"),
                ("FULL JOIN USING", "SELECT * FROM l FULL JOIN r USING (id)")]:
    cols, rows = attempt(q)
    print(f"{name:>17}: {cols}")
print("FULL JOIN USING rows:", attempt("SELECT * FROM l FULL JOIN r USING (id) ORDER BY id")[1])
print("qualified l.id with USING in a FULL JOIN:", attempt("SELECT l.id, r.id FROM l FULL JOIN r USING (id) ORDER BY 1, 2")[1])
print("pandas merge on='id' columns:", list(l.merge(r, on="id").columns),
      "| left_on/right_on columns:", list(l.merge(r.rename(columns={"id": "rid"}), left_on="id", right_on="rid").columns))

# 4. null-safe equality spellings and LATERAL
print("\nnull-safe equality in SQLite: NULL IS NULL ->", con.execute("SELECT NULL IS NULL").fetchone()[0],
      "| NULL IS NOT DISTINCT FROM NULL ->", con.execute("SELECT NULL IS NOT DISTINCT FROM NULL").fetchone()[0],
      "| NULL <=> NULL ->", attempt("SELECT NULL <=> NULL")[1])
print("LATERAL:", attempt("SELECT * FROM l, LATERAL (SELECT * FROM r WHERE r.id = l.id)")[1])
con.close()
```

**Output (my run):**
```text
SQLite version: 3.45.1

join type: SQLite rows | pandas rows
      INNER JOIN: 2 | 2
       LEFT JOIN: 3 | 3
      RIGHT JOIN: 3 | 3
 FULL OUTER JOIN: 4 | 4
      CROSS JOIN: 9 | 9
      comma join: 9 | 9
RIGHT JOIN == swapped LEFT JOIN: True
INTERSECT: [(2,), (3,)]
   EXCEPT: [(1,)]
    MINUS: OperationalError: near "SELECT": syntax error

SELECT * column lists:
               ON: ['id', 'v', 'id', 'w']
       USING (id): ['id', 'v', 'w']
     NATURAL JOIN: ['id', 'v', 'w']
 RIGHT JOIN USING: ['id', 'v', 'w']
  FULL JOIN USING: ['id', 'v', 'w']
FULL JOIN USING rows: [(1, 'l1', None), (2, 'l2', 'r2'), (3, 'l3', 'r3'), (4, None, 'r4')]
qualified l.id with USING in a FULL JOIN: [(None, 4), (1, None), (2, 2), (3, 3)]
pandas merge on='id' columns: ['id', 'v', 'w'] | left_on/right_on columns: ['id', 'v', 'rid', 'w']

null-safe equality in SQLite: NULL IS NULL -> 1 | NULL IS NOT DISTINCT FROM NULL -> 1 | NULL <=> NULL -> OperationalError: near ">": syntax error
LATERAL: OperationalError: near "SELECT": syntax error
```

**Edge cases:**
- **Qualified key after a FULL JOIN with USING:** in my run `SELECT l.id, r.id ... FULL JOIN ... USING (id)` returned the left and right keys separately, with NULLs on the unmatched side, while `SELECT id` (or `*`) returned the coalesced value. Use the unqualified name.
- **MINUS error message:** SQLite parsed `MINUS` as an alias, so the error is a confusing `near "SELECT": syntax error`.
- **Set operators and NULLs:** `INTERSECT` and `EXCEPT` treat NULLs as equal and remove duplicates (Q29).
- **pandas:** `merge` without `on` uses every common column name, so it behaves like NATURAL JOIN unless you pass `on`.

**Then explain:**
- **Portable subset:** `INNER JOIN`, `LEFT JOIN`, `CROSS JOIN` and `ON` work everywhere; for FULL JOIN emulate with `LEFT JOIN ... UNION ALL` plus an anti-join (Q32) when the engine lacks it.
- **Where I am sure and where not:** what is in the left result column was executed; the right column is from general knowledge and manuals as I remember them, and versions matter (MySQL INTERSECT and EXCEPT, SQLite RIGHT and FULL JOIN). Always check the engine's current documentation.
- **Lateral:** the idea (a subquery in FROM that can see columns of earlier FROM items) is outside this part; SQLite does not have it.

**Follow-ups:**
- *Why avoid RIGHT JOIN?* Swap the tables and use LEFT JOIN; readers think left to right.
- *How do you port a FULL JOIN to MySQL?* LEFT JOIN, then `UNION ALL` the right-only rows via an anti-join (Q32).
- *Does `UNION` behave like `INTERSECT` on NULL?* Both treat NULLs as equal for de-duplication (Q29).

**Common mistakes:**
- Assuming every engine supports FULL JOIN, USING or INTERSECT.
- Assuming `SELECT *` from a USING join gives two key columns.
- Using NATURAL JOIN in shared code.
- Writing `MINUS` in an engine that expects `EXCEPT`.

### Q44 ⭐ 🔴 Case: reconcile orders(order_id, amount) with payments(payment_id, order_id, paid_amount), where an order can have several partial payments and some payments reference unknown orders. Produce a status per order (unpaid, partial, paid, overpaid) and list orphan payments. Explain why you must aggregate payments to one row per order before joining (fan-out), the FULL or LEFT plus anti-join structure, and give the pandas groupby then merge with indicator=True and assert that total paid ties out.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Aggregate the payments to one row per order first, then LEFT JOIN that to orders and classify with a CASE, because joining orders straight to payments repeats each order once per payment and inflates every order total; list orphan payments with a separate anti-join on the payments side.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, paid_amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,50),(4,80),(5,120);
INSERT INTO payments VALUES
 (1,1,100),            -- order 1 paid in full
 (2,2,120),(3,2,50),   -- order 2 partial (170 of 200)
 (4,3,60),             -- order 3 overpaid
 (5,5,70),(6,5,50),    -- order 5 paid in full with two payments
 (7,99,40),            -- orphan: unknown order
 (8,NULL,25);          -- orphan: no order id at all
```

**SQL answer:** the Code block holds `SQL_MAIN` (status per order), `SQL_ORPHANS`, `SQL_WRONG` (the fan-out bug) and `SQL_FULL` (the one-pass FULL JOIN structure).
```sql
SELECT o.order_id, o.amount, COALESCE(p.paid, 0) AS paid,
       CASE WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial'
            WHEN p.paid = o.amount THEN 'paid'
            ELSE 'overpaid' END AS status
FROM orders o
LEFT JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p
       ON p.order_id = o.order_id
ORDER BY o.order_id
```
```sql
SELECT pm.payment_id, pm.order_id, pm.paid_amount
FROM payments pm LEFT JOIN orders o ON o.order_id = pm.order_id
WHERE o.order_id IS NULL
ORDER BY pm.payment_id
```
`SQL_FULL` does both in one statement: a FULL JOIN of orders to the aggregated payments, with `COALESCE(o.order_id, p.order_id)` as the key and a status of `orphan` when the order side is missing. Its limit: the payments aggregate has one row per `order_id`, so all payments with a NULL `order_id` collapse into one row (25 here) and you lose the payment-level detail, which is why I use the anti-join for the orphan list.

**pandas answer:** (same text as in the Code block)
```py
paid = payments.groupby("order_id", as_index=False).agg(paid=("paid_amount", "sum"))     # NaN order_id group is dropped by default
m = orders.merge(paid, on="order_id", how="left", validate="one_to_one")
chk = payments.merge(orders[["order_id"]], on="order_id", how="left", indicator=True)
```
The Code block then fills the missing paid values with 0, sets the status with four `loc` assignments (default overpaid, then paid, partial and unpaid overwrite it), and builds the orphan list from the `left_only` rows of `chk`.

**Example:** orders 1 to 5 have amounts 100, 200, 50, 80, 120.
- Order 1: one payment of 100, so paid 100 = amount, status paid.
- Order 2: payments 120 and 50, so 170 < 200, partial.
- Order 3: payment 60 > 50, overpaid.
- Order 4: no payment, paid 0, unpaid (the aggregate has no row, so `p.paid IS NULL`).
- Order 5: payments 70 and 50 sum to 120 = amount, paid (two payments, one order).
- Orphans: payment 7 (order 99 does not exist) and payment 8 (NULL order id).
- Tie-out: all payments 515 = matched 450 (100 + 170 + 60 + 0 + 120) + orphan 65 (40 + 25).
- The fan-out bug: summing `o.amount` after joining directly to payments gave 790 against a true order total of 550, because orders 2 and 5 are counted twice.

**Code:** run with `python3 -I`; the status table is compared sorted by `order_id`, the orphan list sorted by `payment_id`, and the tie-out is asserted in both SQL and pandas.
```python
# Q44: reconcile orders with partial payments: aggregate payments first, status per order, orphan payments, tie-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, paid_amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,50),(4,80),(5,120);
INSERT INTO payments VALUES
 (1,1,100),            -- order 1 paid in full
 (2,2,120),(3,2,50),   -- order 2 partial (170 of 200)
 (4,3,60),             -- order 3 overpaid
 (5,5,70),(6,5,50),    -- order 5 paid in full with two payments
 (7,99,40),            -- orphan: unknown order
 (8,NULL,25);          -- orphan: no order id at all
"""
SQL_MAIN = """
SELECT o.order_id, o.amount, COALESCE(p.paid, 0) AS paid,
       CASE WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial'
            WHEN p.paid = o.amount THEN 'paid'
            ELSE 'overpaid' END AS status
FROM orders o
LEFT JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p
       ON p.order_id = o.order_id
ORDER BY o.order_id
"""
SQL_ORPHANS = """
SELECT pm.payment_id, pm.order_id, pm.paid_amount
FROM payments pm LEFT JOIN orders o ON o.order_id = pm.order_id
WHERE o.order_id IS NULL
ORDER BY pm.payment_id
"""
SQL_WRONG = """
SELECT SUM(o.amount) AS inflated_order_total
FROM orders o JOIN payments pm ON pm.order_id = o.order_id
"""
# the single-pass FULL JOIN structure: one row per order, plus one row per orphan order_id group
SQL_FULL = """
SELECT COALESCE(o.order_id, p.order_id) AS order_id, o.amount, p.paid,
       CASE WHEN o.order_id IS NULL THEN 'orphan' WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial' WHEN p.paid = o.amount THEN 'paid' ELSE 'overpaid' END AS status
FROM orders o
FULL JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p ON p.order_id = o.order_id
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_orph = pd.read_sql_query(SQL_ORPHANS, con)
print("status per order:"); print(sql_df.to_string(index=False))
print("\norphan payments:"); print(sql_orph.to_string(index=False))
print("\nFULL JOIN version (NULL order_id group sorts first):"); print(pd.read_sql_query(SQL_FULL, con).to_string(index=False))
print("\ntrue order total:", con.execute("SELECT SUM(amount) FROM orders").fetchone()[0],
      "| joined straight to payments:", con.execute(SQL_WRONG).fetchone()[0])

# pandas
orders = pd.read_sql_query("SELECT * FROM orders", con)
payments = pd.read_sql_query("SELECT * FROM payments", con)
print("\npayments.order_id dtype:", payments["order_id"].dtype, "(NULL became NaN)")
paid = payments.groupby("order_id", as_index=False).agg(paid=("paid_amount", "sum"))     # NaN order_id group is dropped by default
m = orders.merge(paid, on="order_id", how="left", validate="one_to_one")
m["paid"] = m["paid"].fillna(0).astype("int64")
m["status"] = "overpaid"
m.loc[m["paid"] == m["amount"], "status"] = "paid"
m.loc[m["paid"] < m["amount"], "status"] = "partial"
m.loc[m["paid"] == 0, "status"] = "unpaid"
p_df = m[["order_id", "amount", "paid", "status"]].sort_values("order_id").reset_index(drop=True)
chk = payments.merge(orders[["order_id"]], on="order_id", how="left", indicator=True)
p_orph = (chk[chk["_merge"] == "left_only"][["payment_id", "order_id", "paid_amount"]]
          .sort_values("payment_id").reset_index(drop=True))
pd.testing.assert_frame_equal(sql_df, p_df, check_dtype=False)
pd.testing.assert_frame_equal(sql_orph, p_orph, check_dtype=False)
print("asserts passed: status table and orphan list equal SQL (sorted by order_id / payment_id)")

# tie-out: every payment is either on a known order or an orphan
total_paid = int(payments["paid_amount"].sum())
matched = int(p_df["paid"].sum())
orph = int(p_orph["paid_amount"].sum())
print(f"tie-out: total payments {total_paid} = matched {matched} + orphan {orph}")
assert total_paid == matched + orph
g_total = int(paid["paid"].sum())
print("sum of the groupby result (default dropna=True):", g_total, "vs total payments", total_paid,
      "-> the NaN-order_id payment of", total_paid - g_total, "is silently missing from it")
assert total_paid - g_total == 25
sql_tie = con.execute("SELECT (SELECT SUM(paid_amount) FROM payments), "
                      "(SELECT SUM(pm.paid_amount) FROM payments pm JOIN orders o ON o.order_id = pm.order_id), "
                      "(SELECT SUM(paid_amount) FROM payments pm WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = pm.order_id))").fetchone()
print("SQL tie-out (all, matched, orphan):", sql_tie)
assert sql_tie == (total_paid, matched, orph)
con.close()
```

**Output (my run):**
```text
status per order:
 order_id  amount  paid   status
        1     100   100     paid
        2     200   170  partial
        3      50    60 overpaid
        4      80     0   unpaid
        5     120   120     paid

orphan payments:
 payment_id  order_id  paid_amount
          7      99.0           40
          8       NaN           25

FULL JOIN version (NULL order_id group sorts first):
 order_id  amount  paid   status
      NaN     NaN  25.0   orphan
      1.0   100.0 100.0     paid
      2.0   200.0 170.0  partial
      3.0    50.0  60.0 overpaid
      4.0    80.0   NaN   unpaid
      5.0   120.0 120.0     paid
     99.0     NaN  40.0   orphan

true order total: 550 | joined straight to payments: 790

payments.order_id dtype: float64 (NULL became NaN)
asserts passed: status table and orphan list equal SQL (sorted by order_id / payment_id)
tie-out: total payments 515 = matched 450 + orphan 65
sum of the groupby result (default dropna=True): 490 vs total payments 515 -> the NaN-order_id payment of 25 is silently missing from it
SQL tie-out (all, matched, orphan): (515, 450, 65)
```

**Edge cases:**
- **Status boundaries:** equality on integers is safe; on money stored as floats compare with a rounded difference (`ABS(paid - amount) < 0.005`) or store cents as integers. My toy data uses integers.
- **NULL `order_id` payments:** an INNER or LEFT join to orders never matches a NULL key, so they are orphans in the anti-join. The pandas `groupby` dropped the NaN group by default, so the grouped total (490) was 25 short of the 515 total; the orphan list built from the raw payments is what restores the tie-out.
- **Zero-amount or negative payments (refunds):** `SUM` nets them, so an order can be partial after a refund; decide if refunds belong here.
- **Order with amount 0 and no payment:** status unpaid by my CASE (since `paid IS NULL`), though arguably paid; define the rule.
- **Duplicate payment rows (same payment loaded twice):** the sum doubles; check `payment_id` uniqueness first.
- **pandas dtype:** `payments.order_id` came back `float64` because of the NULL, which is harmless for the merge (see Q35).

**Then explain:**
- **Why aggregate first:** the merge between orders and payments is one-to-many; aggregating payments to one row per `order_id` makes it one-to-one, which `validate="one_to_one"` proves in pandas.
- **Structure:** LEFT JOIN from orders answers "what is the status of every order"; the anti-join from payments answers "which payments have no order". A FULL JOIN can do both, at the cost of losing payment-level detail for NULL-key orphans.
- **Tie-out as a test:** total payments must equal matched plus orphan payments; assert it, because a mismatch means a dropped NULL group or a double count.
- **Status rules written down:** unpaid (no payments), partial (0 < paid < amount), paid (equal), overpaid (greater). State what you do for an amount of 0.

**Follow-ups:**
- *What if a payment can reference several orders?* Then you need an allocation table; the join becomes many-to-many (Q45).
- *How do you find which payment caused the overpayment?* That needs a running total ordered by date (Part 5, windows).
- *How would you monitor this daily?* Run the tie-out as a scheduled check and alert if orphan totals grow (a concept, not run).

**Common mistakes:**
- Joining payments directly and summing order amounts.
- Using an INNER JOIN and losing unpaid orders.
- Writing the status CASE in the wrong order, so overpaid is tested after paid with `>=`.
- Ignoring NULL `order_id` payments and finding the totals do not tie.

### Q45 ⭐ 🔴 Many-to-many comparison, a harder one: promo_codes(code, customer_id) has duplicate rows and customers can hold several codes, while orders(order_id, customer_id, amount) has several orders per customer. Report revenue by promo code without double counting an order that several codes of one customer touch, or deciding it must be allocated. Explain the many-to-many fan-out, the policy choices (count once per code, split, or pick one), the check that totals tie to orders, and the pandas merge with validate and groupby.
**Asked at:** data-modelling write-ups on fan and chasm traps (Coginiti, Sisense, Holistics; snippets), not candidate reports; analyst and data scientist rounds and BI debugging
**Say this first (1 line):** First de-duplicate the promo rows to one row per (code, customer), then choose and state a policy because a customer's orders belong to several codes: count the full order in each code (overlapping, does not add up to total revenue), split each order equally across the customer's codes, or pick one code per customer (both tie to the order total); check that the totals tie in every policy.

**Schema and sample data:**
```sql
CREATE TABLE promo_codes(code TEXT, customer_id INTEGER);          -- duplicates possible
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO promo_codes VALUES ('SAVE10',1),('SAVE10',1),('VIP',1),('SAVE10',2),('VIP',3),('FEST',3);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,3,60),(5,3,40),(6,4,30);
```
Customer 1 has `SAVE10` (loaded twice) and `VIP`; customer 2 has `SAVE10`; customer 3 has `VIP` and `FEST`; customer 4 has no code.

**SQL answer:** the Code block holds `SQL_NAIVE` and the three policies `SQL_ONCE`, `SQL_SPLIT` and `SQL_PICK`; `DEDUP` is the derived table `(SELECT DISTINCT code, customer_id FROM promo_codes)` used by the first two (an f-string in the code, so I describe it instead of pasting the rendered text).
```sql
SELECT p.code, SUM(o.amount) AS revenue
FROM promo_codes p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
```
```sql
SELECT p.code, SUM(o.amount) AS revenue
FROM (SELECT customer_id, MIN(code) AS code FROM promo_codes GROUP BY customer_id) p
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
```
`SQL_ONCE` is the naive query with `promo_codes` replaced by `DEDUP`. `SQL_SPLIT` joins `DEDUP` to a per-customer count of codes (`COUNT(*) ... GROUP BY customer_id` over `DEDUP`) and sums `o.amount * 1.0 / n.n_codes`. `SQL_PICK` takes `MIN(code)` per customer as the chosen code; "alphabetically first" is only a placeholder rule, so use a business rule (first used, highest priority) in real work.

**pandas answer:** (same text as in the Code block)
```py
pd_dedup = promo.drop_duplicates()
once = orders.merge(pd_dedup, on="customer_id", validate="many_to_many")          # many-to-many on purpose, after de-duplication
p_once = once.groupby("code")["amount"].sum()
pick = promo.groupby("customer_id", as_index=False).agg(code=("code", "min"))
pk = orders.merge(pick, on="customer_id", validate="many_to_one")
```
The split policy merges `once` with the per-customer code counts and sums `amount / n_codes` per code.

**Example:** orders: customer 1 has 100 and 50 (150), customer 2 has 80, customer 3 has 60 and 40 (100), customer 4 has 30. Total 360; orders of customers who hold a code: 330.
- Naive join (duplicates not removed): SAVE10 380, VIP 250, FEST 100, sum 730 against 330 for customers with a code: customer 1's duplicate SAVE10 row doubles 150, and the overlaps add more.
- Once per code: SAVE10 = 150 + 80 = 230, VIP = 150 + 100 = 250, FEST = 100; sum 580. It is 250 more than 330 because customer 1 (150) and customer 3 (100) sit in two codes each. This is right for "revenue touched by each code" but the codes must not be added up.
- Split equally: SAVE10 = 75 + 80 = 155, VIP = 75 + 50 = 125, FEST = 50; sum 330, which ties.
- Pick one (the alphabetically first code): customer 1 gets SAVE10, customer 2 SAVE10, customer 3 FEST; SAVE10 230, FEST 100, VIP has nothing; sum 330, which ties.
- Customer 4 (30) has no code and sits outside all policies; 330 + 30 = 360.

**Code:** run with `python3 -I`; each policy is compared between SQL and pandas as a code-to-revenue mapping, and the tie-out is asserted.
```python
# Q45: revenue by promo code when customers hold several codes: dedupe, then three allocation policies, with tie-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE promo_codes(code TEXT, customer_id INTEGER);          -- duplicates possible
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO promo_codes VALUES ('SAVE10',1),('SAVE10',1),('VIP',1),('SAVE10',2),('VIP',3),('FEST',3);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,3,60),(5,3,40),(6,4,30);
"""
DEDUP = "(SELECT DISTINCT code, customer_id FROM promo_codes)"
SQL_NAIVE = """
SELECT p.code, SUM(o.amount) AS revenue
FROM promo_codes p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_ONCE = f"""
SELECT p.code, SUM(o.amount) AS revenue
FROM {DEDUP} p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_SPLIT = f"""
SELECT p.code, SUM(o.amount * 1.0 / n.n_codes) AS revenue
FROM {DEDUP} p
JOIN (SELECT customer_id, COUNT(*) AS n_codes FROM {DEDUP} GROUP BY customer_id) n ON n.customer_id = p.customer_id
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_PICK = """
SELECT p.code, SUM(o.amount) AS revenue
FROM (SELECT customer_id, MIN(code) AS code FROM promo_codes GROUP BY customer_id) p
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
total_orders = con.execute("SELECT SUM(amount) FROM orders").fetchone()[0]
with_code = con.execute("SELECT SUM(amount) FROM orders WHERE customer_id IN (SELECT customer_id FROM promo_codes)").fetchone()[0]
print("order total:", total_orders, "| orders of customers holding at least one code:", with_code)
sql = {k: dict(con.execute(q).fetchall()) for k, q in
       [("naive", SQL_NAIVE), ("once per code", SQL_ONCE), ("split equally", SQL_SPLIT), ("pick one (MIN code)", SQL_PICK)]}
for k, v in sql.items():
    print(f"{k:>20}: {v}  sum = {sum(v.values())}")

# pandas
promo = pd.read_sql_query("SELECT * FROM promo_codes", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("\nduplicate promo rows:", int(promo.duplicated().sum()))
try:
    orders.merge(promo, on="customer_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("validate='many_to_one' on the promo table ->", type(e).__name__ + ":", e)
pd_dedup = promo.drop_duplicates()
once = orders.merge(pd_dedup, on="customer_id", validate="many_to_many")          # many-to-many on purpose, after de-duplication
p_once = once.groupby("code")["amount"].sum()
n_codes = pd_dedup.groupby("customer_id").size().rename("n_codes").reset_index()
sp = once.merge(n_codes, on="customer_id", validate="many_to_one")
p_split = (sp["amount"] / sp["n_codes"]).groupby(sp["code"]).sum()
pick = promo.groupby("customer_id", as_index=False).agg(code=("code", "min"))
pk = orders.merge(pick, on="customer_id", validate="many_to_one")
p_pick = pk.groupby("code")["amount"].sum()
for k, s in [("once per code", p_once), ("split equally", p_split), ("pick one (MIN code)", p_pick)]:
    assert {c: float(v) for c, v in s.items()} == {c: float(v) for c, v in sql[k].items()}, k
print("pandas == SQL for all three policies (compared as code -> revenue)")

# tie-out checks
assert sum(sql["once per code"].values()) > with_code               # overlap by design
assert sum(sql["split equally"].values()) == with_code
assert sum(sql["pick one (MIN code)"].values()) == with_code
assert sum(sql["split equally"].values()) + (total_orders - with_code) == total_orders
print("tie-out: split and pick sum to", with_code, "(+", total_orders - with_code, "with no code =", total_orders,
      "); once-per-code sums to", sum(sql["once per code"].values()), "by design, so it must not be added up")
con.close()
```

**Output (my run):**
```text
order total: 360 | orders of customers holding at least one code: 330
               naive: {'FEST': 100, 'SAVE10': 380, 'VIP': 250}  sum = 730
       once per code: {'FEST': 100, 'SAVE10': 230, 'VIP': 250}  sum = 580
       split equally: {'FEST': 50.0, 'SAVE10': 155.0, 'VIP': 125.0}  sum = 330.0
 pick one (MIN code): {'FEST': 100, 'SAVE10': 230}  sum = 330

duplicate promo rows: 1
validate='many_to_one' on the promo table -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  customer_id
           1
           1
           3 ...
pandas == SQL for all three policies (compared as code -> revenue)
tie-out: split and pick sum to 330 (+ 30 with no code = 360 ); once-per-code sums to 580 by design, so it must not be added up
```

**Edge cases:**
- **Duplicate promo rows:** one duplicate (`SAVE10`, customer 1) doubled that customer's orders in the naive query; fix it with `DISTINCT` or a unique constraint on `(code, customer_id)`.
- **Customers without a code:** an INNER JOIN drops them, so the totals do not reach 360; add a "no code" bucket with a LEFT JOIN if you need the grand total to tie.
- **Customer with codes but no orders:** contributes nothing; use a LEFT JOIN from codes if you want codes with 0 revenue to appear.
- **Float rounding in the split:** 1.0 multiplication keeps decimals, so sums can differ in the last digit; round at the end or store cents (my data splits cleanly).
- **Time:** a code may apply only to orders after it was issued; this table has no dates, so the example ignores that, but in real data the join needs a date condition.
- **pandas `validate`:** `many_to_one` on the promo side raised `MergeError`, which is exactly what you want to see before deduplicating; `many_to_many` is accepted but checks nothing, so I use it only after the dedupe, on purpose.

**Then explain:**
- **Why it fans out:** orders and promo codes are both many per customer, so joining them on `customer_id` is many-to-many: every order is repeated once per code row (and once more per duplicate row).
- **Policy choice:** the join cannot decide for you. Count in each code (marketing wants "revenue influenced"), split (finance wants totals that add up), or pick one (a rule such as last touch or priority). Say which one you used next to the number.
- **Tie-out:** split and pick must sum to the revenue of customers with a code (330), and plus the no-code bucket to the order total (360); once-per-code must exceed it by the overlap (580 against 330 here).
- **Order of operations:** de-duplicate, decide allocation, then join and group; never aggregate after a many-to-many join without knowing the policy.
- **True attribution:** a promo is normally attached to the order (an `order_promos` table), not the customer; if you have that, join on `order_id` and the fan-out shrinks (a design point, not run).

**Follow-ups:**
- *What if one order really uses two codes?* Then the grain is (order, code) and you split by a rule or weight; the check is still that the allocated amounts sum to the order amount.
- *How do you show the overlap?* Count orders in more than one code (a `COUNT(DISTINCT code)` per customer greater than 1).
- *Can `COUNT(DISTINCT order_id)` fix this?* It would fix a count of orders per code, but not a `SUM` (Q13).

**Common mistakes:**
- Summing revenue across codes and presenting it as the total.
- Leaving duplicate promo rows in the join.
- Not saying which allocation policy was used.
- Using `SUM(DISTINCT amount)`, which drops legitimate equal amounts.

