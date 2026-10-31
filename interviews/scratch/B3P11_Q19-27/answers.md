### Q19 ⭐⭐ 🟡 Fan-out joins and pre-aggregation: customers(customer_id, name) 20,000 rows, orders(order_id, customer_id, order_total) 100,000 rows and order_items(item_id, order_id, qty, price) 400,000 rows. A report wants per-customer order count, revenue from orders and item quantity. Show the naive three-table join with SUM(order_total) over-counting (assert the wrong total), the plan and VM steps, the fix by pre-aggregating each child table in a derived table or CTE before joining, assert both fixed forms agree with a pandas groupby, and compare VM steps. Explain that fan-out is both a correctness and a cost problem (row count multiplication), why aggregating before joining shrinks the join input, and how to check the grain of each side. Cross-reference Part 2 Q12 (fan-out inflates SUM), Q13 (the chasm trap) and Q18 (join to an aggregated derived table).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A three-table join multiplies each order row by its item rows, so any order-level column (SUM(order_total)) is counted once per item; aggregate each child to the grain of the key you join on (one row per customer) before joining, and the totals are right and the join input is smaller.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chen');
INSERT INTO orders VALUES (10,1,100),(11,1,50),(12,2,70);
INSERT INTO order_items VALUES (1,10,1,60),(2,10,2,20),(3,10,1,0),(4,11,3,10),(5,11,1,20),(6,12,2,35);
```

**SQL answer:** `NAIVE` (the wrong one), `FIX_DERIVED` (one derived table per child) and `FIX_CTE` (items rolled up to order grain in a CTE, then orders to customer grain) are in the Code block, copied here.
```sql
SELECT c.customer_id, COUNT(DISTINCT o.order_id) AS n_orders,
       SUM(o.order_total) AS revenue, SUM(i.qty) AS qty
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
GROUP BY c.customer_id ORDER BY c.customer_id

SELECT c.customer_id, COALESCE(oa.n_orders, 0) AS n_orders,
       COALESCE(oa.revenue, 0) AS revenue, COALESCE(ia.qty, 0) AS qty
FROM customers c
LEFT JOIN (SELECT customer_id, COUNT(*) AS n_orders, SUM(order_total) AS revenue
           FROM orders GROUP BY customer_id) oa ON oa.customer_id = c.customer_id
LEFT JOIN (SELECT o.customer_id, SUM(i.qty) AS qty
           FROM order_items i JOIN orders o ON o.order_id = i.order_id
           GROUP BY o.customer_id) ia ON ia.customer_id = c.customer_id
ORDER BY c.customer_id

WITH item_per_order AS (SELECT order_id, SUM(qty) AS qty FROM order_items GROUP BY order_id),
     per_customer AS (
       SELECT o.customer_id, COUNT(*) AS n_orders, SUM(o.order_total) AS revenue,
              SUM(COALESCE(ipo.qty, 0)) AS qty
       FROM orders o LEFT JOIN item_per_order ipo ON ipo.order_id = o.order_id
       GROUP BY o.customer_id)
SELECT c.customer_id, COALESCE(p.n_orders, 0) AS n_orders,
       COALESCE(p.revenue, 0) AS revenue, COALESCE(p.qty, 0) AS qty
FROM customers c LEFT JOIN per_customer p ON p.customer_id = c.customer_id
ORDER BY c.customer_id
```

**pandas answer:** Aggregate each side with `groupby`, then merge at customer grain (the same idea as the SQL fix).
```py
def pandas_answer(cu, od, it):
    oa = od.groupby("customer_id").agg(n_orders=("order_id", "size"), revenue=("order_total", "sum"))
    qty = it.merge(od[["order_id", "customer_id"]], on="order_id").groupby("customer_id")["qty"].sum().rename("qty")
    out = cu[["customer_id"]].merge(oa, on="customer_id", how="left").merge(qty, on="customer_id", how="left")
    out[["n_orders", "revenue", "qty"]] = out[["n_orders", "revenue", "qty"]].fillna(0).astype("int64")
    return out.sort_values("customer_id").reset_index(drop=True)
```

**Example:** Asha has orders 10 (total 100, three items) and 11 (total 50, two items); Ben has order 12 (total 70, one item); Chen has no orders. The naive join returns one row per item: order 10 appears 3 times and order 11 twice, so SUM(order_total) for Asha is 100*3 + 50*2 = 400, but the true revenue is 100 + 50 = 150. Her item quantity is right in both forms (1+2+1 + 3+1 = 8) because `qty` lives at the item grain, and COUNT(DISTINCT order_id) = 2 is right only because of DISTINCT. Ben: 70 and 2 are right (one item, no fan-out). Chen: the naive form gives NULL revenue and quantity (the LEFT JOIN found nothing), the fixed forms give 0 through COALESCE. At scale (seed 19) the true SUM(order_total) is 25,505,616 and the naive query returns 103,626,730, a factor of 4.06 (about the 4 items per order).

**Code:** run with `python3 -I`.
```python
# Q19: fan-out joins and pre-aggregation (SQLite in-memory + pandas)
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1                       # vary the text so the statement cache cannot return a stale plan
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

NAIVE = """
SELECT c.customer_id, COUNT(DISTINCT o.order_id) AS n_orders,
       SUM(o.order_total) AS revenue, SUM(i.qty) AS qty
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
GROUP BY c.customer_id ORDER BY c.customer_id
"""
FIX_DERIVED = """
SELECT c.customer_id, COALESCE(oa.n_orders, 0) AS n_orders,
       COALESCE(oa.revenue, 0) AS revenue, COALESCE(ia.qty, 0) AS qty
FROM customers c
LEFT JOIN (SELECT customer_id, COUNT(*) AS n_orders, SUM(order_total) AS revenue
           FROM orders GROUP BY customer_id) oa ON oa.customer_id = c.customer_id
LEFT JOIN (SELECT o.customer_id, SUM(i.qty) AS qty
           FROM order_items i JOIN orders o ON o.order_id = i.order_id
           GROUP BY o.customer_id) ia ON ia.customer_id = c.customer_id
ORDER BY c.customer_id
"""
FIX_CTE = """
WITH item_per_order AS (SELECT order_id, SUM(qty) AS qty FROM order_items GROUP BY order_id),
     per_customer AS (
       SELECT o.customer_id, COUNT(*) AS n_orders, SUM(o.order_total) AS revenue,
              SUM(COALESCE(ipo.qty, 0)) AS qty
       FROM orders o LEFT JOIN item_per_order ipo ON ipo.order_id = o.order_id
       GROUP BY o.customer_id)
SELECT c.customer_id, COALESCE(p.n_orders, 0) AS n_orders,
       COALESCE(p.revenue, 0) AS revenue, COALESCE(p.qty, 0) AS qty
FROM customers c LEFT JOIN per_customer p ON p.customer_id = c.customer_id
ORDER BY c.customer_id
"""
def pandas_answer(cu, od, it):
    oa = od.groupby("customer_id").agg(n_orders=("order_id", "size"), revenue=("order_total", "sum"))
    qty = it.merge(od[["order_id", "customer_id"]], on="order_id").groupby("customer_id")["qty"].sum().rename("qty")
    out = cu[["customer_id"]].merge(oa, on="customer_id", how="left").merge(qty, on="customer_id", how="left")
    out[["n_orders", "revenue", "qty"]] = out[["n_orders", "revenue", "qty"]].fillna(0).astype("int64")
    return out.sort_values("customer_id").reset_index(drop=True)

# ---- tiny hand-checkable sample ----
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chen');
INSERT INTO orders VALUES (10,1,100),(11,1,50),(12,2,70);
INSERT INTO order_items VALUES (1,10,1,60),(2,10,2,20),(3,10,1,0),(4,11,3,10),(5,11,1,20),(6,12,2,35);
""")
print("tiny naive      :", con.execute(NAIVE).fetchall())
print("tiny derived    :", con.execute(FIX_DERIVED).fetchall())
print("tiny cte        :", con.execute(FIX_CTE).fetchall())
# grain check: count rows per key on each side
print("grain: orders per (order_id) max =", con.execute("SELECT MAX(c) FROM (SELECT COUNT(*) c FROM orders GROUP BY order_id)").fetchone()[0],
      "; items per order_id max =", con.execute("SELECT MAX(c) FROM (SELECT COUNT(*) c FROM order_items GROUP BY order_id)").fetchone()[0])

# ---- scaled data ----
random.seed(19)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
""")
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, "c%d" % i) for i in range(1, 20001)])
# customers 19,001..20,000 have no orders on purpose
con.executemany("INSERT INTO orders VALUES (?,?,?)",
                [(i, random.randint(1, 19000), random.randint(10, 500)) for i in range(1, 100001)])
con.executemany("INSERT INTO order_items VALUES (?,?,?,?)",
                [(i, random.randint(1, 95000), random.randint(1, 5), random.randint(1, 100)) for i in range(1, 400001)])
con.commit()
con.execute("CREATE INDEX ix_o_cust ON orders(customer_id)")
con.execute("CREATE INDEX ix_i_order ON order_items(order_id)")
con.commit()
cu = pd.read_sql("SELECT * FROM customers", con)
od = pd.read_sql("SELECT * FROM orders", con)
it = pd.read_sql("SELECT * FROM order_items", con)

truth = int(od["order_total"].sum())
naive_rows, naive_steps = steps(con, NAIVE)
naive = pd.DataFrame(naive_rows, columns=["customer_id", "n_orders", "revenue", "qty"])
naive_total = int(naive["revenue"].sum())
print("true SUM(order_total) over orders :", truth)
print("naive three-table SUM(order_total):", naive_total, "(over-count x%.2f)" % (naive_total / truth))
assert naive_total != truth and naive_total > truth
print("naive COUNT(DISTINCT order_id) total:", int(naive["n_orders"].sum()), "(correct only because of DISTINCT); orders rows:", len(od))
print("rows after the join (fan-out): ", con.execute("SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id LEFT JOIN order_items i ON i.order_id=o.order_id").fetchone()[0],
      "vs 100,000 orders and 400,000 items")

print("customers with no orders:", con.execute("SELECT COUNT(*) FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id)").fetchone()[0],
      "; orders with no items:", con.execute("SELECT COUNT(*) FROM orders o WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.order_id=o.order_id)").fetchone()[0])
res = {}
for name, sql in (("naive", NAIVE), ("derived tables", FIX_DERIVED), ("CTE", FIX_CTE)):
    rows, n = steps(con, sql)
    res[name] = (pd.DataFrame(rows, columns=["customer_id", "n_orders", "revenue", "qty"]), n)
    print("%-15s VM steps %9d" % (name, n))
exp = pandas_answer(cu, od, it)
for name in ("derived tables", "CTE"):
    pd.testing.assert_frame_equal(res[name][0], exp)   # both sorted by customer_id
print("asserts passed: both fixed forms equal the pandas groupby (sorted by customer_id); total revenue", int(exp["revenue"].sum()))
assert int(exp["revenue"].sum()) == truth
# naive qty and n_orders (DISTINCT) happen to be right, revenue is not:
assert (naive["qty"].fillna(0).astype(int).values == exp["qty"].values).all()
assert (naive["revenue"].fillna(0).values != exp["revenue"].values).any()
for name, sql in (("naive", NAIVE), ("derived tables", FIX_DERIVED), ("CTE", FIX_CTE)):
    print("\nPLAN", name)
    for l in plan(con, sql): print("  ", l)

# same fixed query without the two foreign-key indexes
con.execute("DROP INDEX ix_o_cust"); con.execute("DROP INDEX ix_i_order")
for name, sql in (("naive", NAIVE), ("derived tables", FIX_DERIVED), ("CTE", FIX_CTE)):
    rows, n = steps(con, sql)
    print("no FK indexes, %-15s VM steps %9d" % (name, n))
```

**Output (my run):**
```text
tiny naive      : [(1, 2, 400, 8), (2, 1, 70, 2), (3, 0, None, None)]
tiny derived    : [(1, 2, 150, 8), (2, 1, 70, 2), (3, 0, 0, 0)]
tiny cte        : [(1, 2, 150, 8), (2, 1, 70, 2), (3, 0, 0, 0)]
grain: orders per (order_id) max = 1 ; items per order_id max = 3
true SUM(order_total) over orders : 25505616
naive three-table SUM(order_total): 103626730 (over-count x4.06)
naive COUNT(DISTINCT order_id) total: 100000 (correct only because of DISTINCT); orders rows: 100000
rows after the join (fan-out):  407514 vs 100,000 orders and 400,000 items
customers with no orders: 1106 ; orders with no items: 6408
naive           VM steps   7782137
derived tables  VM steps   6848055
CTE             VM steps   9116103
asserts passed: both fixed forms equal the pandas groupby (sorted by customer_id); total revenue 25505616

PLAN naive
   SCAN c
   SEARCH o USING INDEX ix_o_cust (customer_id=?) LEFT-JOIN
   SEARCH i USING INDEX ix_i_order (order_id=?) LEFT-JOIN
   USE TEMP B-TREE FOR count(DISTINCT)

PLAN derived tables
   MATERIALIZE oa
   SCAN orders USING INDEX ix_o_cust
   MATERIALIZE ia
   SCAN o USING COVERING INDEX ix_o_cust
   SEARCH i USING INDEX ix_i_order (order_id=?)
   SCAN c
   BLOOM FILTER ON oa (customer_id=?)
   SEARCH oa USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN
   BLOOM FILTER ON ia (customer_id=?)
   SEARCH ia USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN

PLAN CTE
   MATERIALIZE per_customer
   MATERIALIZE item_per_order
   SCAN order_items USING INDEX ix_i_order
   SCAN o USING INDEX ix_o_cust
   BLOOM FILTER ON ipo (order_id=?)
   SEARCH ipo USING AUTOMATIC COVERING INDEX (order_id=?) LEFT-JOIN
   SCAN c
   BLOOM FILTER ON p (customer_id=?)
   SEARCH p USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN
no FK indexes, naive           VM steps  11125387
no FK indexes, derived tables  VM steps   9448060
no FK indexes, CTE             VM steps  11716107
```

**Edge cases:**
- Customers with no orders (1,106 of the 20,000 here, including ids 19,001 to 20,000 which get none by construction) come out as NULL in the naive query and 0 in the fixed ones; the pandas answer fills them with 0 too. The assertion compares all 20,000 rows.
- Orders with no items still survive the LEFT JOINs (once, with NULL qty). The naive join returned 407,514 rows: 400,000 item rows plus 1,106 customers without orders plus 6,408 orders without items (400,000 + 1,106 + 6,408).
- Which columns are wrong depends on their grain: order-level measures (order_total) inflate, item-level measures (qty) do not, and COUNT(*) on the joined rows counts items, not orders. Only the first is silent; always check the grain of each column.

**Then explain:**
- Fan-out is a correctness problem and a cost problem at once: the join output has one row per item (here 407,514 rows against 100,000 orders), so everything after the join (GROUP BY, DISTINCT, sort) works on the multiplied row count.
- Aggregating before joining makes each join input one row per key: `oa` is one row per customer from orders, `ia` one row per customer from items. The grain check is a query: `SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY key)` must be 1 on the side you treat as 'one row per key' (printed in the run: orders per order_id 1, items per order_id up to 3).
- Cost, honestly measured: VM steps were 7,782,137 for the naive join, 6,848,055 for the derived-table fix (about 12% fewer) and 9,116,103 for the CTE form, which is MORE than the naive query. The two fixed forms still have to read all 400,000 item rows, and each materialised child gets an automatic covering index (see the plans: `MATERIALIZE`, `BLOOM FILTER`, `AUTOMATIC COVERING INDEX`). In SQLite with indexed foreign keys the saving on this shape is modest; the decisive win is correctness. Without the two foreign-key indexes all three were slower (11,125,387, 9,448,060 and 11,716,107 steps).
- The chasm trap (Part 2 Q13) is the same fault with two sibling children (orders and, say, payments) joined to one customer: each child multiplies the other. Pre-aggregating each child to the customer grain is the standard fix. See Part 2 Q12 for fan-out inflating SUM and Part 2 Q18 for joining to an aggregated derived table.
- COUNT(DISTINCT) or SUM(DISTINCT) are not repairs: SUM(DISTINCT order_total) drops legitimately equal totals.

**Follow-ups:**
- Why did the CTE version take more steps than the naive join? (Two materialisations plus two automatic indexes; steps count work, not elapsed time, and the effect depends on the data.)
- How would you do this in a warehouse? (Same pre-aggregation; planner behaviour and costs on PostgreSQL, MySQL, BigQuery or Snowflake were not executed here.)
- What if items must stay at item grain (revenue = SUM(qty*price))? Then sum at item grain first, then roll up: the grain stays explicit.

**Common mistakes:**
- Adding DISTINCT to a SUM to 'fix' double counting.
- Trusting COUNT(*) after a one-to-many join to mean orders.
- Using an INNER JOIN to the aggregated child and silently dropping customers without orders (use LEFT JOIN and COALESCE).
- Joining two sibling child tables to one parent and aggregating after the join.

### Q20 ⭐⭐ 🔴 Rewrite a slow correlated subquery: employees(emp_id, dept_id, salary, hire_date) with 50,000 rows. Return employees earning more than their department average using (a) a correlated scalar subquery in WHERE, (b) a join to a pre-aggregated department-average derived table, and (c) AVG() OVER (PARTITION BY dept_id). Print each plan with and without an index on (dept_id, salary), count VM steps (the correlated form re-runs once per outer row), assert identical results, and show that SQLite does not build an automatic index for the correlated inner scan in this shape (print what it prints). Say when the engine decorrelates automatically (hedged for PostgreSQL, SQL Server, MySQL, not executed) and why you should not rely on it. Cross-reference Part 3 Q39 (correlated subquery performance).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** The correlated scalar subquery re-runs the department average once per outer row (about n*n work with no index, n times an index range with one), while a derived table or a window computes each department once; SQLite does not decorrelate for you and builds no automatic index for that inner scan, so rewrite it.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT);
INSERT INTO employees VALUES (1,10,100,'2020-01-01'),(2,10,200,'2021-01-01'),(3,10,300,'2022-01-01'),
 (4,20,50,'2020-05-01'),(5,20,50,'2021-05-01'),(6,30,70,'2023-01-01');
```

**SQL answer:** `A` is the correlated scalar subquery, `B` the join to a pre-aggregated derived table, `C` the window; all three are in the Code block, copied here.
```sql
SELECT e.emp_id FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.emp_id

SELECT e.emp_id FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal ORDER BY e.emp_id

SELECT emp_id FROM (SELECT emp_id, salary, AVG(salary) OVER (PARTITION BY dept_id) AS avg_sal FROM employees)
WHERE salary > avg_sal ORDER BY emp_id
```

**pandas answer:** `groupby().transform('mean')` is the window version; the comparison is a boolean mask.
```py
def pandas_answer(df):
    m = df.groupby("dept_id")["salary"].transform("mean")
    return df.loc[df["salary"] > m, ["emp_id"]].sort_values("emp_id").reset_index(drop=True)
```

**Example:** Dept 10 has salaries 100, 200, 300 (average 200): only employee 3 (300) earns more. Dept 20 has 50 and 50 (average 50): nobody earns MORE than the average, so both are excluded (the strict > matters). Dept 30 has one employee, equal to its own average: excluded. Result: emp_id 3 for all three forms (printed as `tiny A/B/C [3]`).

**Code:** run with `python3 -I`.
```python
# Q20: correlated subquery vs derived table vs window (SQLite in-memory + pandas)
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

A = """SELECT e.emp_id FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.emp_id"""
B = """SELECT e.emp_id FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal ORDER BY e.emp_id"""
C = """SELECT emp_id FROM (SELECT emp_id, salary, AVG(salary) OVER (PARTITION BY dept_id) AS avg_sal FROM employees)
WHERE salary > avg_sal ORDER BY emp_id"""
FORMS = (("A correlated", A), ("B derived join", B), ("C window", C))

def build(n, n_dept, seed):
    rnd = random.Random(seed)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT)")
    con.executemany("INSERT INTO employees VALUES (?,?,?,?)",
        [(i, rnd.randint(1, n_dept), rnd.randint(20, 200) * 1000, "20%02d-%02d-01" % (rnd.randint(10, 24), rnd.randint(1, 12))) for i in range(1, n + 1)])
    con.commit()
    return con

def pandas_answer(df):
    m = df.groupby("dept_id")["salary"].transform("mean")
    return df.loc[df["salary"] > m, ["emp_id"]].sort_values("emp_id").reset_index(drop=True)

# tiny sample
con = sqlite3.connect(":memory:")
con.executescript("""CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT);
INSERT INTO employees VALUES (1,10,100,'2020-01-01'),(2,10,200,'2021-01-01'),(3,10,300,'2022-01-01'),(4,20,50,'2020-05-01'),(5,20,50,'2021-05-01'),(6,30,70,'2023-01-01');""")
for name, sql in FORMS:
    print("tiny", name, [r[0] for r in con.execute(sql)])
print("tiny dept avgs:", con.execute("SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id").fetchall())

# the unindexed correlated form is quadratic: measure it on small tables only
print("\nCorrelated form WITHOUT an index, VM steps by table size (200 departments):")
small = {}
for n in (500, 1000, 2000):
    c = build(n, 200, 20)
    rows, st = steps(c, A)
    small[n] = st
    print("  n=%5d  steps %10d  steps/n^2 = %.2f" % (n, st, st / n / n))
print("  plan:", plan(build(500, 200, 20), A))
est = small[2000] / 2000 / 2000 * 50000 * 50000
print("  extrapolated to 50,000 rows by steps/n^2 (an estimate, NOT run): about %.1e steps" % est)

con = build(50000, 200, 20)
df = pd.read_sql("SELECT * FROM employees", con)
exp = pandas_answer(df)
print("\n50,000 employees, 200 departments, pandas answer rows:", len(exp))
for idx in (False, True):
    if idx:
        con.execute("CREATE INDEX ix_dept_sal ON employees(dept_id, salary)"); con.commit()
    print("--- index on (dept_id, salary):", idx)
    for name, sql in FORMS:
        if name.startswith("A") and not idx:
            print("  %-15s not run at 50,000 rows without an index (quadratic, see above)" % name)
            continue
        rows, n = steps(con, sql)
        pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["emp_id"]), exp)
        print("  %-15s rows %5d  VM steps %10d" % (name, len(rows), n))
    for name, sql in FORMS:
        print("  PLAN", name)
        for l in plan(con, sql): print("     ", l)
print("asserts passed: every form run returned the pandas rows (compared sorted by emp_id)")
```

**Output (my run):**
```text
tiny A correlated [3]
tiny B derived join [3]
tiny C window [3]
tiny dept avgs: [(10, 200.0), (20, 50.0), (30, 70.0)]

Correlated form WITHOUT an index, VM steps by table size (200 departments):
  n=  500  steps    1010385  steps/n^2 = 4.04
  n= 1000  steps    4025775  steps/n^2 = 4.03
  n= 2000  steps   16071237  steps/n^2 = 4.02
  plan: ['SCAN e', 'CORRELATED SCALAR SUBQUERY 1', 'SCAN x']
  extrapolated to 50,000 rows by steps/n^2 (an estimate, NOT run): about 1.0e+10 steps

50,000 employees, 200 departments, pandas answer rows: 24915
--- index on (dept_id, salary): False
  A correlated    not run at 50,000 rows without an index (quadratic, see above)
  B derived join  rows 24915  VM steps    1404036
  C window        rows 24915  VM steps    2426239
  PLAN A correlated
      SCAN e
      CORRELATED SCALAR SUBQUERY 1
      SCAN x
  PLAN B derived join
      CO-ROUTINE d
      SCAN employees
      USE TEMP B-TREE FOR GROUP BY
      SCAN e
      BLOOM FILTER ON d (dept_id=?)
      SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)
  PLAN C window
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SCAN employees
      USE TEMP B-TREE FOR ORDER BY
      SCAN (subquery-3)
      SCAN (subquery-1)
      USE TEMP B-TREE FOR ORDER BY
--- index on (dept_id, salary): True
  A correlated    rows 24915  VM steps   51076033
  B derived join  rows 24915  VM steps     628860
  C window        rows 24915  VM steps    2026237
  PLAN A correlated
      SCAN e
      CORRELATED SCALAR SUBQUERY 1
      SEARCH x USING COVERING INDEX ix_dept_sal (dept_id=?)
  PLAN B derived join
      CO-ROUTINE d
      SCAN employees USING COVERING INDEX ix_dept_sal
      SCAN d
      SEARCH e USING COVERING INDEX ix_dept_sal (dept_id=? AND salary>?)
      USE TEMP B-TREE FOR ORDER BY
  PLAN C window
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SCAN employees USING COVERING INDEX ix_dept_sal
      SCAN (subquery-3)
      SCAN (subquery-1)
      USE TEMP B-TREE FOR ORDER BY
asserts passed: every form run returned the pandas rows (compared sorted by emp_id)
```

**Edge cases:**
- Ties and a single-person department return nothing, because salary > average is false when equal. Use >= only if the question says so.
- NULL salaries are ignored by AVG and never satisfy salary > avg; an employee with NULL dept_id gets a NULL average in the correlated form and in B (the equality never matches), so those rows are dropped, but the window form puts all NULL-dept rows in one partition and compares them with that partition's average, so the forms can differ. Reasoned from the rules, not run; there are no NULL departments in this data.
- AVG returns a float: the comparison is exact here because integer salaries make sums exact, but with REAL columns compare with a tolerance in tests.

**Then explain:**
- Cost (VM steps, deterministic proxy). Correlated form, NO index: 1,010,385 steps at 500 rows, 4,025,775 at 1,000 and 16,071,237 at 2,000, i.e. 4.0 steps times n squared every time (doubling the table quadruples the work). Extrapolating by that ratio to 50,000 rows gives about 1.0e10 steps; that number is an estimate and was NOT run.
- At 50,000 rows without an index only B (1,404,036 steps) and C (2,426,239) were run. With an index on (dept_id, salary): A 51,076,033, B 628,860, C 2,026,237 steps. The index turns each inner scan into a covering range search (`SEARCH x USING COVERING INDEX ix_dept_sal (dept_id=?)`) but the subquery still runs once per outer row, so A is still about 81 times B.
- What SQLite prints for the unindexed correlated form: `SCAN e`, `CORRELATED SCALAR SUBQUERY 1`, `SCAN x`. No automatic index appears for the inner scan (automatic indexes were on by default), whereas the derived-table form B shows `BLOOM FILTER ON d` and `SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)`, so SQLite builds an automatic index on the materialised derived table but not on the inner scan of a correlated subquery.
- The window form needs the rows ordered by the partition key: without the index the plan shows `USE TEMP B-TREE FOR ORDER BY` twice (the window sort, then the final ORDER BY); with the index the window sort is replaced by an index scan but the final ORDER BY emp_id still sorts.
- Decorrelation by the optimiser: PostgreSQL, SQL Server and MySQL optimisers can sometimes turn some correlated subqueries into joins (SQL Server and recent MySQL for some patterns; PostgreSQL generally not for a correlated scalar aggregate). I did not run any of them, so treat this as a hedge. Do not rely on it: it differs by engine and version and by query shape, and when it does not happen the cost is quadratic. A rewrite that states the grouping explicitly (B or C) is portable and predictable.
- Cross-reference Part 3 Q39 (correlated subquery performance).

**Follow-ups:**
- When is the correlated form fine? (Small outer set, or a selective outer filter plus an index on the inner key, e.g. one department.)
- Why does C use more steps than B with the index? (Window evaluation buffers partitions and adds coroutines; steps are not time.)
- How would you test the three forms at the same size honestly? (Same data, same asserted result, fresh connection per plan print; steps first, timing only as a machine-specific second opinion.)

**Common mistakes:**
- Assuming the optimiser will decorrelate the subquery.
- Reading a plan from a stale statement cache: this run varies the EXPLAIN text so SQLite cannot return an old plan (see the sources note).
- Comparing with >= and then wondering why ties appear.
- Running the quadratic form at full size 'just to see'; measure it on small sizes and extrapolate, labelled as an estimate.

### Q21 ⭐⭐ 🟡 OR, UNION ALL, IN, != and NOT IN as access paths: orders(order_id, customer_id, status, order_date, amount) with 200,000 rows and indexes on customer_id, order_date and status. Print the plan and VM steps for customer_id = 5 OR customer_id = 7 (rewritten to IN), customer_id = 5 OR order_date = '2024-05-05' (MULTI-INDEX OR), customer_id = 5 OR amount > 400 (one unindexed term forces a scan), the UNION ALL rewrite with a guard against double counting versus plain UNION (dedupe cost, USE TEMP B-TREE), status != 'delivered' where 98% match, status NOT IN ('a','b') and status IN (list of the other values). Explain why OR across columns is only fast when every branch is indexable, why UNION removes duplicates at a cost, why inequality predicates rarely use indexes well and that UNION ALL needs mutually exclusive branches (or a NOT condition) for correctness. Hedge index-merge in MySQL and bitmap-OR in PostgreSQL as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** OR is fast only when every branch has an index (SQLite turns same-column ORs into IN and different indexed columns into a MULTI-INDEX OR), one unindexed term forces a scan, UNION ALL needs mutually exclusive branches to stay correct, UNION pays a temp B-tree to deduplicate, and != / NOT IN on a column that matches 98% of rows is a scan whichever way you write it.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'delivered','2024-05-05',100),(2,5,'cancelled','2024-01-01',20),
 (3,7,'delivered','2024-05-05',30),(4,8,'delivered','2024-05-05',900),(5,9,'returned','2024-02-02',10);
```

**SQL answer:** The tiny forms are `OR2`, `U_ALL_BAD`, `U_ALL_OK` and `U_PLAIN`; the scaled forms are in the `CASES` list of the Code block (same text):
```sql
SELECT order_id FROM orders WHERE customer_id = 5 OR order_date = '2024-05-05' ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' AND customer_id IS NOT 5 ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 UNION
SELECT order_id FROM orders WHERE order_date = '2024-05-05' ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 OR customer_id = 7
SELECT order_id FROM orders WHERE customer_id = 5 OR amount > 400
SELECT order_id FROM orders WHERE status != 'delivered'
SELECT order_id FROM orders WHERE status NOT IN ('cancelled','returned')
SELECT order_id FROM orders WHERE status IN ('cancelled','returned')
```

**pandas answer:** Boolean masks, one per query (these are the `lambda d: ...` bodies in the `CASES` list, which the code asserts against each SQL result after sorting by order_id).
```py
lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]
```

**Example:** Tiny table: customer 5 owns orders 1 and 2; date 2024-05-05 covers orders 1, 3 and 4. The OR returns {1,2,3,4} once each. UNION ALL without a guard returns order 1 twice ([1, 1, 2, 3, 4]) because it matches both branches. The guard `customer_id IS NOT 5` on the second branch removes it: [1, 2, 3, 4]. Plain UNION also returns [1, 2, 3, 4] by deduplicating, at the price of a sort or hash. If a row with customer_id NULL and that date exists (order 6), the guard `IS NOT 5` keeps it ([1,2,3,4,6], correct) but `!= 5` drops it (NULL != 5 is unknown). At 200,000 rows I forced row 1 to customer 5 on 2024-05-05 so the double count shows: the unguarded UNION ALL returned 614 rows against 613 correct.

**Code:** run with `python3 -I`.
```python
# Q21: OR, UNION ALL, IN, != and NOT IN as access paths
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

# tiny sample for the correctness walk-through
t = sqlite3.connect(":memory:")
t.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'delivered','2024-05-05',100),(2,5,'cancelled','2024-01-01',20),
 (3,7,'delivered','2024-05-05',30),(4,8,'delivered','2024-05-05',900),(5,9,'returned','2024-02-02',10);
""")
OR2 = "SELECT order_id FROM orders WHERE customer_id = 5 OR order_date = '2024-05-05' ORDER BY order_id"
U_ALL_BAD = """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' ORDER BY order_id"""
U_ALL_OK = """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' AND customer_id IS NOT 5 ORDER BY order_id"""
U_PLAIN = """SELECT order_id FROM orders WHERE customer_id = 5 UNION
SELECT order_id FROM orders WHERE order_date = '2024-05-05' ORDER BY order_id"""
for nm, q in (("OR", OR2), ("UNION ALL, no guard", U_ALL_BAD), ("UNION ALL, guarded", U_ALL_OK), ("UNION", U_PLAIN)):
    print("tiny %-20s" % nm, [r[0] for r in t.execute(q)])
# NULL trap for the guard: customer_id IS NOT 5 vs != 5
t.execute("INSERT INTO orders VALUES (6,NULL,'delivered','2024-05-05',1)")
g1 = [r[0] for r in t.execute(U_ALL_OK)]
g2 = [r[0] for r in t.execute(U_ALL_OK.replace("customer_id IS NOT 5", "customer_id != 5"))]
print("tiny with a NULL customer: guard 'IS NOT 5' ->", g1, "; guard '!= 5' ->", g2, "(the != guard drops order 6)")

# scaled data: 200,000 rows
rnd = random.Random(21)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER)")
sts = ["delivered"] * 98 + ["cancelled"] * 1 + ["returned"] * 1   # about 98 / 1 / 1 percent
rows = []
for i in range(1, 200001):
    rows.append((i, rnd.randint(1, 20000), rnd.choice(sts),
                 "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500)))
rows[0] = (1, 5, "delivered", "2024-05-05", 250)   # force one row that matches both branches
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
con.execute("CREATE INDEX ix_date ON orders(order_date)")
con.execute("CREATE INDEX ix_status ON orders(status)")
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
print("\nstatus counts:", {k: int(v) for k, v in df["status"].value_counts().items()})

CASES = [
 ("OR on one column", "SELECT order_id FROM orders WHERE customer_id = 5 OR customer_id = 7",
   lambda d: d[(d.customer_id == 5) | (d.customer_id == 7)]),
 ("OR, two indexed columns", "SELECT order_id FROM orders WHERE customer_id = 5 OR order_date = '2024-05-05'",
   lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]),
 ("OR with unindexed amount", "SELECT order_id FROM orders WHERE customer_id = 5 OR amount > 400",
   lambda d: d[(d.customer_id == 5) | (d.amount > 400)]),
 ("UNION ALL, guarded", """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' AND customer_id IS NOT 5""",
   lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]),
 ("UNION (dedupe)", """SELECT order_id FROM orders WHERE customer_id = 5 UNION
SELECT order_id FROM orders WHERE order_date = '2024-05-05'""",
   lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]),
 ("status != 'delivered'", "SELECT order_id FROM orders WHERE status != 'delivered'", lambda d: d[d.status != "delivered"]),
 ("status NOT IN (a,b)", "SELECT order_id FROM orders WHERE status NOT IN ('cancelled','returned')",
   lambda d: d[~d.status.isin(["cancelled", "returned"])]),
 ("status IN (other values)", "SELECT order_id FROM orders WHERE status IN ('cancelled','returned')",
   lambda d: d[d.status.isin(["cancelled", "returned"])]),
]
for nm, sql, fn in CASES:
    r, n = steps(con, sql)
    exp = sorted(fn(df)["order_id"].tolist())
    assert sorted(x[0] for x in r) == exp, nm
    print("\n%s: %d rows, VM steps %d" % (nm, len(r), n))
    for l in plan(con, sql): print("   ", l)
bad_r, bad_n = steps(con, """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05'""")
ok = steps(con, CASES[3][1])[0]
print("\nUNION ALL WITHOUT the guard returns %d rows versus %d correct (rows matching both branches counted twice)" % (len(bad_r), len(ok)))
r2, n2 = steps(con, "SELECT order_id FROM orders NOT INDEXED WHERE status != 'delivered'")
print("status != delivered with NOT INDEXED (table scan): %d rows, VM steps %d" % (len(r2), n2))
print("asserts passed: every query returned the pandas filter's order_ids (compared sorted)")
```

**Output (my run):**
```text
tiny OR                   [1, 2, 3, 4]
tiny UNION ALL, no guard  [1, 1, 2, 3, 4]
tiny UNION ALL, guarded   [1, 2, 3, 4]
tiny UNION                [1, 2, 3, 4]
tiny with a NULL customer: guard 'IS NOT 5' -> [1, 2, 3, 4, 6] ; guard '!= 5' -> [1, 2, 3, 4] (the != guard drops order 6)

status counts: {'delivered': 195960, 'returned': 2064, 'cancelled': 1976}

OR on one column: 25 rows, VM steps 133
    SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)

OR, two indexed columns: 613 rows, VM steps 5541
    MULTI-INDEX OR
    INDEX 1
    SEARCH orders USING INDEX ix_cust (customer_id=?)
    INDEX 2
    SEARCH orders USING INDEX ix_date (order_date=?)

OR with unindexed amount: 40185 rows, VM steps 1080349
    SCAN orders

UNION ALL, guarded: 613 rows, VM steps 4265
    COMPOUND QUERY
    LEFT-MOST SUBQUERY
    SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
    UNION ALL
    SEARCH orders USING INDEX ix_date (order_date=?)

UNION (dedupe): 613 rows, VM steps 4926
    COMPOUND QUERY
    LEFT-MOST SUBQUERY
    SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
    UNION USING TEMP B-TREE
    SEARCH orders USING COVERING INDEX ix_date (order_date=?)

status != 'delivered': 4040 rows, VM steps 608089
    SCAN orders USING COVERING INDEX ix_status

status NOT IN (a,b): 195960 rows, VM steps 1785914
    SCAN orders USING COVERING INDEX ix_status

status IN (other values): 4040 rows, VM steps 16188
    SEARCH orders USING COVERING INDEX ix_status (status=?)

UNION ALL WITHOUT the guard returns 614 rows versus 613 correct (rows matching both branches counted twice)
status != delivered with NOT INDEXED (table scan): 4040 rows, VM steps 608088
asserts passed: every query returned the pandas filter's order_ids (compared sorted)
```

**Edge cases:**
- The double-count demonstration needed one forced row: with random data the two branches rarely overlap, so an unguarded UNION ALL can look right in a test and be wrong in production.
- NOT IN with a NULL in the list returns no rows (three-valued logic, see Part 3 Q3); the list here has none. `!=` and NOT IN exclude rows where status is NULL; there are none in this data.
- The status mix is seeded 98/1/1 percent (195,960 delivered, 1,976 cancelled, 2,064 returned in the run), so 'rare values' are 2% in total, not 0.5%.

**Then explain:**
- Plans and VM steps (200,000 rows, indexes on customer_id, order_date, status): `customer_id = 5 OR customer_id = 7` became one `SEARCH ... USING COVERING INDEX ix_cust (customer_id=?)`, 25 rows, 133 steps (SQLite rewrote the OR into IN). Two different indexed columns gave `MULTI-INDEX OR / INDEX 1 / INDEX 2`, 613 rows, 5,541 steps. With the unindexed `amount > 400` as one OR term the plan was `SCAN orders`, 40,185 rows, 1,080,349 steps: one unindexed branch ruins the whole OR.
- UNION ALL (guarded) took 4,265 steps and UNION 4,926; the UNION plan says `UNION USING TEMP B-TREE`, the cost of removing duplicates. Both branches used an index. UNION ALL is only correct when the branches cannot return the same row, or when you add the NOT condition shown.
- Inequality: `status != 'delivered'` matched 4,040 rows (2%) but the plan was `SCAN orders USING COVERING INDEX ix_status`, 608,089 steps, essentially identical to `NOT INDEXED` (608,088). SQLite did not seek an index for !=. `status IN ('cancelled','returned')` used `SEARCH ... (status=?)` and took 16,188 steps, about 38 times fewer, but it needs the complete list of other values and silently misses new statuses. `NOT IN ('cancelled','returned')` returns 98% of the table (195,960 rows, 1,785,914 steps), where no index can help: reading most of the table is what it costs.
- Why OR across columns is only fast when every branch is indexable: each branch needs its own index lookup, merged by rowid; one unindexed term needs a scan to evaluate, which makes the index lookups pointless. SQLite documents the MULTI-INDEX OR strategy; it does not intersect indexes for AND (see the sources note).
- Other engines, not executed: MySQL has an index_merge optimisation (union, intersection) and PostgreSQL combines indexes with bitmap OR / bitmap AND scans; both are hedged here because I only ran SQLite. Whether either is chosen depends on statistics.
- Rewriting with UNION ALL is a manual way to get what MULTI-INDEX OR does automatically: use it only when you have shown that the original OR is slow and the branches are exclusive.

**Follow-ups:**
- How would you make `status != 'delivered'` fast? (Often you cannot; a partial index on the rare statuses, or IN with the known list, or ask whether the report needs those rows at all; see Q22.)
- Why do the UNION plans say COVERING INDEX while the MULTI-INDEX OR plan printed a plain INDEX? (The index holds order_id as the rowid, so no table lookup is needed; I did not investigate why the OR plan does not say covering.)
- What does UNION do with NULLs? (Treats them as equal for deduplication.)

**Common mistakes:**
- UNION ALL over overlapping branches without a guard.
- Writing the guard as `!= 5` and losing NULL rows.
- Expecting an index to help `!=` or `NOT IN` on a column where most rows match.
- Wrapping an indexed column in a function inside the OR and then blaming OR.

### Q22 ⭐⭐ 🟡 Partial, expression and unique indexes: orders(order_id, customer_id, status, order_date, amount, email TEXT) with 200,000 rows where status = 'placed' is about 3% of rows and email is mixed case. Create (1) a partial index ON orders(order_date) WHERE status = 'placed', (2) an expression index on lower(email) and (3) a UNIQUE index on email with some NULLs. Print which queries use each (the query's WHERE must imply the index's WHERE; show that status IN ('placed'), status != 'delivered' and a bound parameter status = ? behave as they actually do on 3.45.1, by running), compare index size from page counts against a full index, show lower(email) = ? using the expression index only when the expression matches exactly, and show that UNIQUE allows several NULLs. Explain the benefits (smaller index, cheaper writes for the rest of the table) and hedge PostgreSQL partial and expression index details and SQL Server filtered indexes as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A partial index is used only when the query's WHERE clearly implies the index's WHERE (in SQLite 3.45.1 `status = 'placed'` and a bound `status = ?` qualify, `IN ('placed')` and `!=` did not), an expression index is used only when the query contains the exact same expression, and a UNIQUE index treats NULLs as distinct so it allows several.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT, email TEXT);
INSERT INTO orders VALUES (1,'placed','2024-06-01','Asha@Mail.com'),(2,'delivered','2024-06-02','ben@mail.com'),
 (3,'placed','2024-06-03',NULL),(4,'delivered','2024-06-04',NULL);
CREATE UNIQUE INDEX ux_email ON orders(email);
```

**SQL answer:** The three indexes and the probe queries are in the Code block, copied here (the full probe list is the `Q` and `E` lists):
```sql
CREATE INDEX ix_placed ON orders(order_date) WHERE status = 'placed'
CREATE INDEX ix_lower_email ON orders(lower(email))
CREATE UNIQUE INDEX ux_email ON orders(email)
CREATE INDEX ix_full ON orders(order_date)
SELECT order_id FROM orders WHERE status = 'placed' AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status IN ('placed') AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status != 'delivered' AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status = ? AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE lower(email) = ?
```

**pandas answer:** Row-for-row filters that the code asserts against the SQL results.
```py
exp = df[(df.status == "placed") & (df.order_date > "2024-11-01")]
```

**Example:** Tiny table: orders 1 and 3 are 'placed'. The partial index ix_placed would hold only those two rows (entries for dates 2024-06-01 and 2024-06-03); orders 2 and 4 are not in it at all. `status = 'placed' AND order_date > '2024-06-02'` is answered from it (order 3). The UNIQUE index on email holds 'Asha@Mail.com', 'ben@mail.com' and two NULL entries: the two NULLs do not conflict (count printed: 2), a second 'ben@mail.com' fails with `UNIQUE constraint failed: orders.email`, and 'BEN@mail.com' is accepted because the default comparison is case-sensitive. At 200,000 rows (6,064 placed, 3.03%) the query `status = 'placed' AND order_date > '2024-11-01'` returned 982 rows, which equals the pandas filter.

**Code:** run with `python3 -I`.
```python
# Q22: partial, expression and unique indexes
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql, params=()):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0], params)]

# tiny sample
t = sqlite3.connect(":memory:")
t.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT, email TEXT);
INSERT INTO orders VALUES (1,'placed','2024-06-01','Asha@Mail.com'),(2,'delivered','2024-06-02','ben@mail.com'),(3,'placed','2024-06-03',NULL),(4,'delivered','2024-06-04',NULL);
CREATE UNIQUE INDEX ux_email ON orders(email);
""")
print("tiny: two NULL emails coexist under UNIQUE:", t.execute("SELECT COUNT(*) FROM orders WHERE email IS NULL").fetchone()[0])
try:
    t.execute("INSERT INTO orders VALUES (5,'placed','2024-06-05','ben@mail.com')")
except sqlite3.IntegrityError as e:
    print("tiny: duplicate non-NULL email ->", type(e).__name__, e)
t.execute("INSERT INTO orders VALUES (6,'placed','2024-06-06','BEN@mail.com')")
print("tiny: 'BEN@mail.com' is accepted next to 'ben@mail.com' (UNIQUE is case-sensitive, BINARY)")

# scaled data: 200,000 rows
rnd = random.Random(22)
rows = []
for i in range(1, 200001):
    st = "placed" if rnd.random() < 0.03 else rnd.choice(["delivered", "delivered", "shipped", "cancelled"])
    local = "user%d" % i
    email = None if rnd.random() < 0.05 else (local.upper() if rnd.random() < 0.3 else local.capitalize()) + "@Example.COM"
    rows.append((i, rnd.randint(1, 20000), st, "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500), email))
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER, email TEXT)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", rows)
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
print("\nplaced rows: %d of %d (%.2f%%)" % ((df.status == "placed").sum(), len(df), 100 * (df.status == "placed").mean()))

con.execute("CREATE INDEX ix_placed ON orders(order_date) WHERE status = 'placed'")
con.execute("CREATE INDEX ix_lower_email ON orders(lower(email))")
con.execute("CREATE UNIQUE INDEX ux_email ON orders(email)")
con.commit()

Q = [
 ("status = 'placed' AND order_date > ...", "SELECT order_id FROM orders WHERE status = 'placed' AND order_date > '2024-11-01'", ()),
 ("status IN ('placed') AND ...", "SELECT order_id FROM orders WHERE status IN ('placed') AND order_date > '2024-11-01'", ()),
 ("status != 'delivered' AND ...", "SELECT order_id FROM orders WHERE status != 'delivered' AND order_date > '2024-11-01'", ()),
 ("status = ? (bound) AND ...", "SELECT order_id FROM orders WHERE status = ? AND order_date > '2024-11-01'", ("placed",)),
 ("order_date > ... only", "SELECT order_id FROM orders WHERE order_date > '2024-11-01'", ()),
]
print("\nPARTIAL INDEX ix_placed(order_date) WHERE status = 'placed'")
for nm, sql, p in Q:
    r, n = steps(con, sql, p)
    print(" %-40s rows %5d steps %8d  %s" % (nm, len(r), n, plan(con, sql, p)))
exp = df[(df.status == "placed") & (df.order_date > "2024-11-01")]
assert sorted(x[0] for x in steps(con, Q[0][1])[0]) == sorted(exp.order_id)
assert sorted(x[0] for x in steps(con, Q[3][1], ("placed",))[0]) == sorted(exp.order_id)

target = df.email.dropna().iloc[1234]
E = [
 ("lower(email) = ?", "SELECT order_id FROM orders WHERE lower(email) = ?", (target.lower(),)),
 ("lower(email) = lower(?)", "SELECT order_id FROM orders WHERE lower(email) = lower(?)", (target,)),
 ("upper(email) = ?", "SELECT order_id FROM orders WHERE upper(email) = ?", (target.upper(),)),
 ("lower(trim(email)) = ?", "SELECT order_id FROM orders WHERE lower(trim(email)) = ?", (target.lower(),)),
 ("email = ? (exact)", "SELECT order_id FROM orders WHERE email = ?", (target,)),
 ("email = ? COLLATE NOCASE", "SELECT order_id FROM orders WHERE email = ? COLLATE NOCASE", (target.lower(),)),
 ("email LIKE ? (case-insensitive)", "SELECT order_id FROM orders WHERE email LIKE ?", (target.lower(),)),
]
print("\nEXPRESSION AND UNIQUE INDEXES, target email", target)
for nm, sql, p in E:
    r, n = steps(con, sql, p)
    print(" %-32s rows %d steps %8d  %s" % (nm, len(r), n, plan(con, sql, p)))
want = df[df.email.str.lower() == target.lower()]["order_id"].tolist()
assert [x[0] for x in con.execute(E[0][1], E[0][2])] == want
print("lower(email) lookup rows match pandas str.lower() filter:", want)

nulls = int(df.email.isna().sum())
print("\nNULL emails in the UNIQUE-indexed column: %d (all allowed)" % nulls)
assert con.execute("SELECT COUNT(*) FROM orders WHERE email IS NULL").fetchone()[0] == nulls
try:
    con.execute("INSERT INTO orders(customer_id,status,order_date,amount,email) VALUES (1,'placed','2024-01-01',1,?)", (target,))
except sqlite3.IntegrityError as e:
    print("duplicate insert ->", e)

# sizes
con.execute("CREATE INDEX ix_full ON orders(order_date)")
con.commit()
print("\nINDEX SIZES (dbstat bytes and pages, page_size %d)" % con.execute("PRAGMA page_size").fetchone()[0])
for nm in ("ix_placed", "ix_full", "ix_lower_email", "ux_email"):
    b, p = con.execute("SELECT SUM(pgsize), COUNT(*) FROM dbstat WHERE name = ?", (nm,)).fetchone()
    print("  %-15s %9d bytes %5d pages" % (nm, b, p))
b, p = con.execute("SELECT SUM(pgsize), COUNT(*) FROM dbstat WHERE name = 'orders'").fetchone()
print("  %-15s %9d bytes %5d pages (the table itself)" % ("orders", b, p))

# write cost: insert 'delivered' rows with only the partial index vs only the full index
import time
def insert_cost(index_sql):
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT)")
    c.execute(index_sql)
    batch = [(i, "delivered", "2024-%02d-%02d" % (1 + i % 12, 1 + i % 28)) for i in range(1, 100001)]
    n = [0]
    def cb():
        n[0] += 1
        return 0
    t0 = time.perf_counter()
    c.set_progress_handler(cb, 1)
    c.executemany("INSERT INTO orders VALUES (?,?,?)", batch)
    c.set_progress_handler(None, 0)
    c.commit()
    ms = (time.perf_counter() - t0) * 1000
    pages = c.execute("SELECT COUNT(*) FROM dbstat WHERE name = 'i'").fetchone()[0]
    return n[0], ms, pages
for label, ddl in (("partial index", "CREATE INDEX i ON orders(order_date) WHERE status = 'placed'"),
                   ("full index", "CREATE INDEX i ON orders(order_date)"),
                   ("no index", "CREATE TABLE IF NOT EXISTS unused(x)")):
    n, ms, pages = insert_cost(ddl)
    print("insert 100,000 'delivered' rows, %-13s: progress callbacks %d, index pages %d, wall %.0f ms (machine-specific, single run)" % (label, n, pages, ms))
```

**Output (my run):**
```text
tiny: two NULL emails coexist under UNIQUE: 2
tiny: duplicate non-NULL email -> IntegrityError UNIQUE constraint failed: orders.email
tiny: 'BEN@mail.com' is accepted next to 'ben@mail.com' (UNIQUE is case-sensitive, BINARY)

placed rows: 6064 of 200000 (3.03%)

PARTIAL INDEX ix_placed(order_date) WHERE status = 'placed'
 status = 'placed' AND order_date > ...   rows   982 steps     2958  ['SEARCH orders USING COVERING INDEX ix_placed (order_date>?)']
 status IN ('placed') AND ...             rows   982 steps   614102  ['SCAN orders']
 status != 'delivered' AND ...            rows 16839 steps   839434  ['SCAN orders']
 status = ? (bound) AND ...               rows   982 steps     5907  ['SEARCH orders USING COVERING INDEX ix_placed (order_date>?)']
 order_date > ... only                    rows 32837 steps   665682  ['SCAN orders']

EXPRESSION AND UNIQUE INDEXES, target email User1298@Example.COM
 lower(email) = ?                 rows 1 steps       17  ['SEARCH orders USING INDEX ix_lower_email (<expr>=?)']
 lower(email) = lower(?)          rows 1 steps       19  ['SEARCH orders USING INDEX ix_lower_email (<expr>=?)']
 upper(email) = ?                 rows 1 steps   800011  ['SCAN orders USING COVERING INDEX ux_email']
 lower(trim(email)) = ?           rows 1 steps  1000011  ['SCAN orders USING COVERING INDEX ux_email']
 email = ? (exact)                rows 1 steps       11  ['SEARCH orders USING COVERING INDEX ux_email (email=?)']
 email = ? COLLATE NOCASE         rows 1 steps   600011  ['SCAN orders USING COVERING INDEX ux_email']
 email LIKE ? (case-insensitive)  rows 1 steps   800013  ['SCAN orders USING COVERING INDEX ux_email']
lower(email) lookup rows match pandas str.lower() filter: [1298]

NULL emails in the UNIQUE-indexed column: 9938 (all allowed)
duplicate insert -> UNIQUE constraint failed: orders.email

INDEX SIZES (dbstat bytes and pages, page_size 4096)
  ix_placed          118784 bytes    29 pages
  ix_full           3792896 bytes   926 pages
  ix_lower_email    5890048 bytes  1438 pages
  ux_email          5890048 bytes  1438 pages
  orders           11223040 bytes  2740 pages (the table itself)
insert 100,000 'delivered' rows, partial index: progress callbacks 2000003, index pages 1, wall 363 ms (machine-specific, single run)
insert 100,000 'delivered' rows, full index   : progress callbacks 2000003, index pages 516, wall 432 ms (machine-specific, single run)
insert 100,000 'delivered' rows, no index     : progress callbacks 1400003, index pages 0, wall 245 ms (machine-specific, single run)
```

**Edge cases:**
- Implication is syntactic and conservative: `status IN ('placed')` means the same as `= 'placed'` but SQLite 3.45.1 scanned the table (614,102 steps against 2,958). `status != 'delivered'` is not implied by `status = 'placed'` anyway (it also matches other statuses) and scanned. A bound parameter `status = ?` did use the index (5,907 steps): the planner accepts a parameter for the equality here; I did not test what happens in other engines.
- A query with no status condition cannot use the partial index (it would miss rows): SCAN.
- UNIQUE on a mixed-case email does not make emails unique ignoring case: add a unique expression index on lower(email) for that (not run here; the lower(email) expression index in the code is non-unique).
- NULL emails: 9,938 of 200,000 rows are NULL and all coexist under the UNIQUE index.

**Then explain:**
- Which query used which index (plans printed in the output): `status = 'placed' AND order_date > ...` used `COVERING INDEX ix_placed (order_date>?)`; `IN ('placed')`, `!=` and the no-status query scanned. `lower(email) = ?` used `ix_lower_email (<expr>=?)` (17 steps), as did `lower(email) = lower(?)`. `upper(email) = ?`, `lower(trim(email)) = ?`, `email = ? COLLATE NOCASE` and `email LIKE ?` all scanned (the plan shows a scan of the narrowest covering index ux_email, 600,011 to 1,000,011 steps). `email = ?` used the UNIQUE index (11 steps). The expression must match exactly.
- Size (dbstat, 4,096-byte pages): partial ix_placed 29 pages (118,784 bytes) against full ix_full 926 pages (3,792,896 bytes), about 3% of the size; ix_lower_email and ux_email 1,438 pages each; the table 2,740 pages.
- Write cost: a partial index is only maintained for rows that satisfy its WHERE, so inserts and updates of the other 97% do not touch it. In a 100,000-row insert of non-'placed' rows the partial index ended with 1 page against 516 for the full index, and wall time was 363 ms against 432 ms (no index: 245 ms; machine-specific single runs). The VM-step proxy did NOT show a difference (2,000,003 callbacks for both), because the progress handler counts jump-style opcodes and the cheap skip is not visible there; do not use steps for this comparison.
- Benefits: smaller index, cheaper writes for rows outside the predicate, and a UNIQUE rule that can be limited to a subset (e.g. one active row per customer, not run here).
- Other engines, not executed: PostgreSQL partial and expression indexes have the same idea (the planner must be able to prove the query predicate implies the index predicate, and parameterised queries and generic plans can change that; check with EXPLAIN there). SQL Server filtered indexes are similar but are reported to be restricted for parameterised queries unless the plan is recompiled, and SQL Server and PostgreSQL treat NULLs in unique indexes differently (SQL Server allows one NULL in a unique index; PostgreSQL allows many, and newer versions have NULLS NOT DISTINCT). All of this is from memory and was not run.

**Follow-ups:**
- What is the risk of an expression index? (Every query and every ORM must write the same expression; a different function or collation silently scans.)
- Would ANALYZE change any of these plans? (Not tested in this answer.)
- How would you enforce case-insensitive uniqueness? (UNIQUE index on lower(email), or a NOCASE collation on the column; the lower(email) unique variant is not run here.)

**Common mistakes:**
- Assuming `IN ('placed')` or `!=` will use a partial index.
- Testing the expression index with `lower(trim(email))` or `upper(email)` and concluding indexes are broken.
- Believing UNIQUE rejects multiple NULLs (SQLite and PostgreSQL allow them; engines differ).
- Counting a partial index as free: the table still pays for all other indexes.

### Q23 ⭐⭐ 🟡 Write cost: batching inserts and transactions. Insert 100,000 seeded rows into events(event_id, user_id, event_type, event_time) in a file-backed SQLite database in four ways: one INSERT and commit per row (use 2,000 rows only), a single transaction with execute in a loop, executemany inside one transaction, and executemany after creating indexes versus creating the indexes afterwards. Report VM steps (deterministic) and wall-clock timings labelled machine-specific, show PRAGMA journal_mode and synchronous, explain why per-row commits are slow (each commit syncs to disk), why bulk loads add indexes after loading, parameter binding (prepared statements) versus string formatting, and mention multi-row INSERT, COPY (PostgreSQL), LOAD DATA (MySQL) and bulk-load paths in warehouses as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Each commit forces a sync to disk, so one commit per row costs milliseconds per row, while one transaction (with executemany and bound parameters) costs microseconds per row; load first, create indexes afterwards, and never build SQL with string formatting.

**Schema and sample data:**
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT);
INSERT INTO events VALUES (1,17,'view','2024-01-01'),(2,17,'click','2024-01-01'),(3,42,'buy','2024-01-02');
```

**SQL answer:** The statements are the constants `DDL`, `INS` and the three `CREATE INDEX` strings in `IDX`; the load shapes are the Python functions in the Code block:
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT)
INSERT INTO events VALUES (?,?,?,?)
CREATE INDEX ix_user ON events(user_id)
CREATE INDEX ix_type ON events(event_type)
CREATE INDEX ix_time ON events(event_time)
```

**pandas answer:** pandas holds the same seeded rows and is the checksum for every load.
```py
pdf = pd.DataFrame(data, columns=["event_id", "user_id", "event_type", "event_time"])
```

**Example:** Three rows go in. With a commit per row there are three transactions: three journal writes and three syncs. In one transaction there is one commit and one sync for all three rows. For 100,000 rows the same logic applies at scale: 100,000 syncs against one. The checksum in the code (row count and SUM(user_id) against the pandas frame) proves every method stored the same rows.

**Code:** run with `python3 -I`.
```python
# Q23: write cost: batching inserts and transactions (file-backed SQLite)
import sqlite3, random, os, tempfile, time
import pandas as pd

random.seed(23)
N = 100_000
types = ["view", "click", "cart", "buy"]
data = [(i, random.randint(1, 5000), random.choice(types), "2024-%02d-%02d" % (random.randint(1, 12), random.randint(1, 28)))
        for i in range(1, N + 1)]
pdf = pd.DataFrame(data, columns=["event_id", "user_id", "event_type", "event_time"])
DDL = "CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT)"
INS = "INSERT INTO events VALUES (?,?,?,?)"
IDX = ["CREATE INDEX ix_user ON events(user_id)", "CREATE INDEX ix_type ON events(event_type)", "CREATE INDEX ix_time ON events(event_time)"]
tmp = tempfile.TemporaryDirectory()

def fresh(name):
    path = os.path.join(tmp.name, name + ".db")
    con = sqlite3.connect(path)
    con.execute(DDL)
    con.commit()
    return con

def run(label, fn, con, expect_rows):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    t0 = time.perf_counter()
    fn(con)
    ms = (time.perf_counter() - t0) * 1000
    con.set_progress_handler(None, 0)
    cnt, s = con.execute("SELECT COUNT(*), SUM(user_id) FROM events").fetchone()
    assert cnt == expect_rows
    assert s == int(pdf["user_id"].iloc[:expect_rows].sum())       # same rows as the pandas frame
    print("%-52s rows %6d  progress steps %9d  wall %8.1f ms" % (label, cnt, n[0], ms))
    return n[0], ms

con = fresh("probe")
print("journal_mode =", con.execute("PRAGMA journal_mode").fetchone()[0], "| synchronous =", con.execute("PRAGMA synchronous").fetchone()[0], "(2 = FULL)")
con.close()

def per_row(con):
    for r in data[:2000]:
        con.execute(INS, r)
        con.commit()
def loop_one_txn(con):
    for r in data:
        con.execute(INS, r)
    con.commit()
def many(con):
    con.executemany(INS, data)
    con.commit()
def multirow(con, k=500):
    for i in range(0, N, k):
        chunk = data[i:i + k]
        con.execute("INSERT INTO events VALUES " + ",".join(["(?,?,?,?)"] * len(chunk)), [v for r in chunk for v in r])
    con.commit()
def indexes_first(con):
    for s in IDX: con.execute(s)
    con.executemany(INS, data); con.commit()
def indexes_after(con):
    con.executemany(INS, data)
    for s in IDX: con.execute(s)
    con.commit()
def fmt_strings(con):                          # unsafe string formatting, shown only for cost
    for r in data:
        con.execute("INSERT INTO events VALUES (%d,%d,'%s','%s')" % r)
    con.commit()

print("\n-- commit granularity (default journal_mode, synchronous=FULL)")
a = run("1. execute + commit per row, 2,000 rows only", per_row, fresh("a"), 2000)
b = run("2. execute in a loop, one transaction, 100,000 rows", loop_one_txn, fresh("b"), N)
c = run("3. executemany, one transaction, 100,000 rows", many, fresh("c"), N)
d = run("3b. multi-row INSERT VALUES (500 rows per statement)", multirow, fresh("d"), N)
e = run("3c. execute with string formatting (not safe), one txn", fmt_strings, fresh("e"), N)
print("per-row commit costs %.2f ms per row; executemany costs %.4f ms per row (machine-specific)" % (a[1] / 2000, c[1] / N))

print("\n-- three secondary indexes before versus after the load (executemany, one transaction)")
f = run("4a. indexes created BEFORE loading", indexes_first, fresh("f"), N)
g = run("4b. indexes created AFTER loading", indexes_after, fresh("g"), N)

print("\n-- per-row commits under other settings (2,000 rows, machine-specific)")
settings = [("journal_mode=WAL, synchronous=FULL", ["PRAGMA journal_mode=WAL"]),
            ("journal_mode=WAL, synchronous=NORMAL", ["PRAGMA journal_mode=WAL", "PRAGMA synchronous=NORMAL"]),
            ("journal_mode=DELETE, synchronous=OFF", ["PRAGMA synchronous=OFF"])]
for j, (label, pragmas) in enumerate(settings):
    con = fresh("h%d" % j)
    for p in pragmas:
        con.execute(p).fetchall()
    run("5. per-row commit, " + label, per_row, con, 2000)

# the safe path: parameters. A quote in the data breaks the formatted statement
c2 = fresh("q")
try:
    c2.execute("INSERT INTO events VALUES (1,1,'it's','x')")
except sqlite3.OperationalError as ex:
    print("\nformatted SQL with a quote in the value ->", ex)
c2.execute(INS, (1, 1, "it's", "x"))
print("bound parameters store it safely:", c2.execute("SELECT event_type FROM events").fetchone()[0])
print("compile option for the bound-variable limit:", [o for o in sqlite3.connect(":memory:").execute("PRAGMA compile_options") if "MAX_VARIABLE" in o[0]])
print("asserts passed: every load produced the same row count and SUM(user_id) as the pandas frame")
tmp.cleanup()
```

**Output (my run):**
```text
journal_mode = delete | synchronous = 2 (2 = FULL)

-- commit granularity (default journal_mode, synchronous=FULL)
1. execute + commit per row, 2,000 rows only         rows   2000  progress steps     42000  wall   2179.2 ms
2. execute in a loop, one transaction, 100,000 rows  rows 100000  progress steps   1500006  wall    341.6 ms
3. executemany, one transaction, 100,000 rows        rows 100000  progress steps   1500006  wall    306.0 ms
3b. multi-row INSERT VALUES (500 rows per statement) rows 100000  progress steps   1401606  wall    257.4 ms
3c. execute with string formatting (not safe), one txn rows 100000  progress steps   1500006  wall    593.3 ms
per-row commit costs 1.09 ms per row; executemany costs 0.0031 ms per row (machine-specific)

-- three secondary indexes before versus after the load (executemany, one transaction)
4a. indexes created BEFORE loading                   rows 100000  progress steps   3100168  wall    985.8 ms
4b. indexes created AFTER loading                    rows 100000  progress steps   4200168  wall    719.9 ms

-- per-row commits under other settings (2,000 rows, machine-specific)
5. per-row commit, journal_mode=WAL, synchronous=FULL rows   2000  progress steps     42000  wall    575.1 ms
5. per-row commit, journal_mode=WAL, synchronous=NORMAL rows   2000  progress steps     42000  wall     46.9 ms
5. per-row commit, journal_mode=DELETE, synchronous=OFF rows   2000  progress steps     42000  wall     99.5 ms

formatted SQL with a quote in the value -> near "s": syntax error
bound parameters store it safely: it's
compile option for the bound-variable limit: [('MAX_VARIABLE_NUMBER=250000',)]
asserts passed: every load produced the same row count and SUM(user_id) as the pandas frame
```

**Edge cases:**
- Per-row commit was run on 2,000 rows only (as asked); 100,000 syncs would take minutes on this storage. The per-row figures are not extrapolated into a total in the text.
- VM steps are the same per row for commit-per-row (21 steps per row) and for one transaction (15 per row): commit-and-sync cost is I/O wait, not VM work, so the deterministic step count cannot show it. Only wall-clock shows it, so the timings below are the evidence and they are machine- and disk-specific single runs.
- File-backed database in a temporary directory; storage type, filesystem and fsync behaviour change the numbers a lot (WAL with synchronous=NORMAL is far faster for per-row commits but gives up some durability on power loss).

**Then explain:**
- Results in my run (machine-specific): commit per row 2,000 rows took about 2.2 seconds, around 1.1 ms per row; the same loop in one transaction inserted 100,000 rows in about 0.34 s (a few microseconds per row); executemany took about the same (0.31 s), because the loop overhead of Python is small next to the commit. A multi-row INSERT with 500 rows per statement was a little faster (0.26 s) and used the fewest VM steps (1,401,606 against 1,500,006). String formatting took longer (0.59 s) and cannot bind a value that contains a quote (the run shows `near "s": syntax error`) and is an injection hole: bound parameters are also faster because the statement is prepared once and reused.
- Settings printed: `PRAGMA journal_mode` = delete and `PRAGMA synchronous` = 2 (FULL) by default. For 2,000 per-row commits: WAL with synchronous=FULL about 0.58 s, WAL with synchronous=NORMAL about 0.05 s, journal_mode delete with synchronous=OFF about 0.1 s. Fewer syncs, faster commits; the price is durability, which is a business decision.
- Indexes: with three secondary indexes created BEFORE the load the insert took 3,100,168 steps and about 1.0 s; creating them AFTER the load took 4,200,168 steps but about 0.7 s. The step count went UP while the time went DOWN: a bulk index build sorts the keys and appends them in order instead of doing a random B-tree insert per row, and that is I/O and cache behaviour that VM steps do not capture. Use steps only for what they measure.
- Not executed here: PostgreSQL COPY, MySQL LOAD DATA, and bulk-load paths in warehouses (stage files then COPY or LOAD) are the same idea at a larger scale: few large operations rather than many small ones. Multi-row INSERT VALUES is standard SQL and was run on SQLite; its row limits differ by engine (SQLite's compile option here is MAX_VARIABLE_NUMBER=250000 bound variables, printed in the run).

**Follow-ups:**
- What does executemany do beyond the loop? (Reuses one prepared statement; the speed-up over a per-row execute in one transaction was small here.)
- What is the durability trade-off of synchronous=NORMAL or OFF? (A crash or power loss can lose recent commits or corrupt data in OFF mode.)
- Would you load into an indexed table if it is live? (Yes if readers need it; for a one-off bulk load, drop or defer indexes.)

**Common mistakes:**
- Calling commit inside the loop 'to be safe'.
- Leaving autocommit on with the Python default and wondering why it is slow (each INSERT outside a transaction commits).
- Building SQL with f-strings.
- Quoting wall-clock timings as if they were deterministic.

### Q24 ⭐⭐ 🟡 The N+1 query pattern from application code: customers(customer_id, name) 100 seeded rows and orders(order_id, customer_id, amount) 1,000 rows. Write the loop that fetches the customer list and then runs one query per customer, count the statements with Connection.set_trace_callback (101), then replace it with one JOIN/GROUP BY query (1 statement) and with one IN (?, ?, ...) batched query, assert the same data, and print the plan of the per-customer lookup. Explain why N+1 is a round-trip problem that grows with network latency (the SQLite example is in-process so its time is misleading: say so), the ORM lazy-loading origin and eager-loading fixes (described, no ORM executed), batching limits on IN lists (SQLite's variable limit, check compile options), and the pandas equivalent of looping over rows with read_sql per row versus one read_sql plus merge.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** N+1 is one query for the list plus one query per row, 101 statements here against 1 (JOIN + GROUP BY) or 2 (a batched IN); in-process SQLite hides the cost, but against a networked database every extra statement is a round trip, so latency multiplies by N.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'cust001'),(2,'cust002'),(3,'cust003');
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,3,70);
```

**SQL answer:** The three shapes are in the Code block (the loop statement, the JOIN/GROUP BY and the batched IN), copied here:
```sql
SELECT customer_id, name FROM customers ORDER BY customer_id
SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?
SELECT c.customer_id, c.name, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id
SELECT customer_id, amount FROM orders WHERE customer_id IN (%s)
```

**pandas answer:** Per-row `read_sql` in a loop versus one `read_sql`, groupby and merge (both are in the Code block, copied here):
```py
agg = ord_df.groupby("customer_id")["amount"].agg(cnt="size", total="sum").reset_index()
```

**Example:** Tiny table: customer 1 has orders of 100 and 50 (count 2, total 150), customer 2 has none (count 0, total 0), customer 3 has 70. The N+1 loop issues the list query and then three lookups: 4 statements, in general 1 + N. The JOIN with GROUP BY returns the same three rows in one statement; the LEFT JOIN keeps customer 2 with count 0. At scale (100 customers, 1,000 orders) the trace callback counted exactly 101, 1 and 2 statements, and the three results are asserted equal.

**Code:** run with `python3 -I`.
```python
# Q24: the N+1 query pattern
import sqlite3, random, time
import pandas as pd

random.seed(24)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
""")
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, "cust%03d" % i) for i in range(1, 101)])
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, random.randint(1, 100), random.randint(10, 500)) for i in range(1, 1001)])
con.commit()

class Counter:
    def __init__(self, c):
        self.stmts = []
        c.set_trace_callback(self.stmts.append)
    def reset(self):
        self.stmts.clear()
ctr = Counter(con)

# 1. N+1: one query for the list, then one per customer
ctr.reset()
t0 = time.perf_counter()
customers = con.execute("SELECT customer_id, name FROM customers ORDER BY customer_id").fetchall()
n_plus_1 = []
for cid, name in customers:
    tot, cnt = con.execute("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?", (cid,)).fetchone()
    n_plus_1.append((cid, name, cnt, tot))
t1 = (time.perf_counter() - t0) * 1000
print("N+1 loop: %d statements; first three traced:" % len(ctr.stmts))
for s in ctr.stmts[:3]: print("   ", s)
assert len(ctr.stmts) == 101

# 2. one JOIN + GROUP BY
ctr.reset()
t0 = time.perf_counter()
joined = con.execute("""SELECT c.customer_id, c.name, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id""").fetchall()
t2 = (time.perf_counter() - t0) * 1000
print("JOIN + GROUP BY: %d statement" % len(ctr.stmts))
assert len(ctr.stmts) == 1

# 3. one batched IN (?, ?, ...) query, then group in Python
ctr.reset()
t0 = time.perf_counter()
ids = [c[0] for c in con.execute("SELECT customer_id FROM customers ORDER BY customer_id")]
ph = ",".join("?" * len(ids))
fetched = con.execute("SELECT customer_id, amount FROM orders WHERE customer_id IN (%s)" % ph, ids).fetchall()
agg = {}
for cid, amt in fetched:
    c, s = agg.get(cid, (0, 0)); agg[cid] = (c + 1, s + amt)
names = dict(customers)
batched = [(cid, names[cid], *agg.get(cid, (0, 0))) for cid in ids]
t3 = (time.perf_counter() - t0) * 1000
print("batched IN: %d statements (1 for ids + 1 for orders)" % len(ctr.stmts))
assert len(ctr.stmts) == 2
assert n_plus_1 == joined == batched
print("asserts passed: N+1, JOIN and batched IN give the same 100 rows (customer_id, name, order_count, total)")
print("in-process times (machine-specific, MISLEADING for a network database): N+1 %.2f ms, JOIN %.2f ms, IN %.2f ms" % (t1, t2, t3))
print("simulated latency of 0.5 ms per round trip (arithmetic, not a measurement): N+1 adds %.1f ms, JOIN adds %.1f ms, IN adds %.1f ms" % (101 * 0.5, 1 * 0.5, 2 * 0.5))

print("\nplan of the per-customer lookup, no index:", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM orders WHERE customer_id = ?", (5,))])
con.execute("CREATE INDEX ix_orders_cust ON orders(customer_id)")
print("plan with index on orders(customer_id):  ", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM orders WHERE customer_id = ? ", (5,))])

n = [0]
def cb():
    n[0] += 1
    return 0
def vm(sql, p=()):
    n[0] = 0; con.set_progress_handler(cb, 1); con.execute(sql, p).fetchall(); con.set_progress_handler(None, 0); return n[0]
loop_steps = sum(vm("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?", (cid,)) for cid in ids)
print("VM steps with the index: 100 lookups total %d; the single JOIN/GROUP BY query %d" % (loop_steps, vm("""SELECT c.customer_id, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id GROUP BY c.customer_id""")))

opts = [o[0] for o in con.execute("PRAGMA compile_options") if "MAX_VARIABLE" in o[0]]
print("\nbound-variable limit compile option:", opts)
big = list(range(1, 300001))
try:
    con.execute("SELECT COUNT(*) FROM orders WHERE customer_id IN (%s)" % ",".join("?" * len(big)), big)
except sqlite3.Error as ex:
    print("IN list with 300,000 placeholders ->", type(ex).__name__, ex)
chunks = [ids[i:i + 30] for i in range(0, len(ids), 30)]
tot = sum(con.execute("SELECT COUNT(*) FROM orders WHERE customer_id IN (%s)" % ",".join("?" * len(ch)), ch).fetchone()[0] for ch in chunks)
print("chunked IN (4 chunks of up to 30 ids): %d orders counted, table has %d" % (tot, con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]))

# pandas: read_sql per row versus one read_sql + merge
ctr.reset()
rows = []
cust_df = pd.read_sql("SELECT * FROM customers ORDER BY customer_id", con)
for cid in cust_df["customer_id"]:
    one = pd.read_sql("SELECT COALESCE(SUM(amount),0) AS total, COUNT(*) AS cnt FROM orders WHERE customer_id = ?", con, params=(int(cid),))
    rows.append((int(cid), int(one.at[0, "cnt"]), int(one.at[0, "total"])))
loop_df = pd.DataFrame(rows, columns=["customer_id", "cnt", "total"])
print("\npandas per-row read_sql loop: %d statements" % len(ctr.stmts))
ctr.reset()
ord_df = pd.read_sql("SELECT customer_id, amount FROM orders", con)
agg = ord_df.groupby("customer_id")["amount"].agg(cnt="size", total="sum").reset_index()
merged = cust_df.merge(agg, on="customer_id", how="left").fillna({"cnt": 0, "total": 0}).astype({"cnt": "int64", "total": "int64"})
print("pandas one read_sql + groupby + merge: %d statements" % len(ctr.stmts))
pd.testing.assert_frame_equal(loop_df, merged[["customer_id", "cnt", "total"]])
print("asserts passed: both pandas versions equal (sorted by customer_id)")
```

**Output (my run):**
```text
N+1 loop: 101 statements; first three traced:
    SELECT customer_id, name FROM customers ORDER BY customer_id
    SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = 1
    SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = 2
JOIN + GROUP BY: 1 statement
batched IN: 2 statements (1 for ids + 1 for orders)
asserts passed: N+1, JOIN and batched IN give the same 100 rows (customer_id, name, order_count, total)
in-process times (machine-specific, MISLEADING for a network database): N+1 4.65 ms, JOIN 0.95 ms, IN 1.24 ms
simulated latency of 0.5 ms per round trip (arithmetic, not a measurement): N+1 adds 50.5 ms, JOIN adds 0.5 ms, IN adds 1.0 ms

plan of the per-customer lookup, no index: ['SCAN orders']
plan with index on orders(customer_id):   ['SEARCH orders USING INDEX ix_orders_cust (customer_id=?)']
VM steps with the index: 100 lookups total 7700; the single JOIN/GROUP BY query 15219

bound-variable limit compile option: ['MAX_VARIABLE_NUMBER=250000']
IN list with 300,000 placeholders -> OperationalError too many SQL variables
chunked IN (4 chunks of up to 30 ids): 1000 orders counted, table has 1000

pandas per-row read_sql loop: 101 statements
pandas one read_sql + groupby + merge: 1 statements
asserts passed: both pandas versions equal (sorted by customer_id)
```

**Edge cases:**
- Customers without orders: the loop form gives (0, 0) through COALESCE and the JOIN needs a LEFT JOIN (with an INNER JOIN they would vanish, and the assert would fail).
- The batched IN query returns raw order rows, so the grouping happens in Python; customers with no orders are filled with (0, 0) in the code.
- An empty id list makes `IN ()`: build the placeholders from a non-empty list or skip the query.

**Then explain:**
- Why N+1 hurts: each statement costs a round trip (network latency plus parse and plan). In-process SQLite has no network, so the timing is misleading: the loop took about 4.5 ms and the JOIN about 1 ms in my run (machine-specific), a small absolute difference. Illustrative arithmetic only, not a measurement: at an assumed 0.5 ms per round trip, 101 statements add about 50 ms while 1 statement adds 0.5 ms, and for 10,000 rows N+1 would add 5 seconds.
- Even in process the plan of the per-customer lookup matters: `SCAN orders` without an index (so the loop reads the whole orders table 100 times) and `SEARCH orders USING INDEX ix_orders_cust (customer_id=?)` with one. With the index, 100 lookups took 7,700 VM steps and the single JOIN/GROUP BY 15,219 steps (it reads all 1,000 orders): in VM steps N+1 was not worse. The cost of N+1 is latency, not engine work, which is why in-process counts hide it.
- ORM origin (described, no ORM executed): lazy loading fetches related rows when an attribute is first touched, so iterating over 100 parents and reading `parent.children` triggers 100 child queries. Eager-loading options (a JOIN fetch, or a second query with IN over the parent ids, usually called select-in or batch loading) turn it into 1 or 2 statements. Check the ORM's SQL log, as this answer does with `set_trace_callback`.
- Batching limits: an IN list is limited by the engine's bound-variable limit. SQLite here reports `MAX_VARIABLE_NUMBER=250000`; an IN list of 300,000 placeholders failed with `OperationalError too many SQL variables`. Other engines have their own limits (hedged, not executed); chunk the ids (the code runs 4 chunks of up to 30 ids).
- pandas: loading customers and then calling `read_sql` once per customer produced 101 statements (1 + 100); one `read_sql` for orders followed by `groupby` and `merge` produced 1 statement (the customers frame was reused from the first part; reading it again would make 2).

**Follow-ups:**
- When is IN batching better than a JOIN? (When the child query needs different columns, filters or a different database or service from the parent.)
- How do you detect N+1 in production? (Statement counts per request in the application log or APM, repeated identical query shapes with different parameters.)
- What is the fix when the parent list is huge? (Chunk the ids, or push the work into one set-based query.)

**Common mistakes:**
- Judging N+1 by in-process timing.
- Using an INNER JOIN and dropping parents without children.
- Putting 100,000 ids into one IN list without checking the engine's limit.
- Looping over DataFrame rows and calling the database inside the loop.

### Q25 ⭐⭐ 🟡 CTE materialisation and subquery flattening: orders(order_id, customer_id, order_date, amount) with 200,000 rows and an index on customer_id. Print the plan for a CTE referenced twice (MATERIALIZE or CO-ROUTINE), for the same CTE written AS MATERIALIZED and AS NOT MATERIALIZED, for a filter applied outside a GROUP BY subquery (WHERE customer_id = 5 on top of the aggregate) and for the equivalent subquery inlined, and count VM steps. State what SQLite does with a CTE used once (flattened like a subquery) versus several times, the predicate push-down limits (a LIMIT or DISTINCT inside blocks it), and that PostgreSQL 12+ inlines single-use CTEs and MATERIALIZED/NOT MATERIALIZED exist there too (hedged, not executed), while older PostgreSQL treated a CTE as an optimisation fence. Cross-reference Part 3 Q32 (reusing one CTE twice).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** In SQLite 3.45.1 a CTE (or subquery) used once is run as a co-routine and a filter on its grouping column is pushed down into it, a CTE used twice is materialised once by default (AS NOT MATERIALIZED re-runs it for each reference, which here doubled the steps), and a LIMIT or an aggregate condition inside blocks the push-down.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'2024-01-01',10),(2,5,'2024-01-02',30),(3,6,'2024-01-03',5),(4,7,'2024-01-04',100);
```

**SQL answer:** The CTE-twice query is `TWICE` with `%s` replaced by nothing, `MATERIALIZED` or `NOT MATERIALIZED`; the others are below (same text as the Code block):
```sql
WITH t AS %s (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE s > (SELECT AVG(s) FROM t) ORDER BY customer_id
SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE customer_id = 5
SELECT customer_id, SUM(amount) AS s FROM orders WHERE customer_id = 5 GROUP BY customer_id
```

**pandas answer:** Group, then compare with the mean of the group totals (the CTE-twice question), and a plain filter for customer 5.
```py
exp5 = int(df.loc[df.customer_id == 5, "amount"].sum())
```

**Example:** Tiny table: customer totals are 5 -> 40, 6 -> 5, 7 -> 100; the average of the totals is 48.33, so only customer 7 (100) is above it: the CTE `t` is read twice, once for the rows and once inside the scalar subquery for the average. With `WHERE customer_id = 5` on top of the aggregate the answer is the single row (5, 40). The question is whether SQLite computes all customers' totals first and then throws four away, or computes only customer 5's.

**Code:** run with `python3 -I`.
```python
# Q25: CTE materialisation and subquery flattening
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

# tiny sample
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'2024-01-01',10),(2,5,'2024-01-02',30),(3,6,'2024-01-03',5),(4,7,'2024-01-04',100);""")
TWICE = "WITH t AS %s (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE s > (SELECT AVG(s) FROM t) ORDER BY customer_id"
print("tiny: per-customer totals", t.execute("SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id").fetchall(),
      "average of totals", t.execute("SELECT AVG(s) FROM (SELECT SUM(amount) s FROM orders GROUP BY customer_id)").fetchone()[0])
print("tiny: customers above the average total:", t.execute(TWICE % "").fetchall())

rnd = random.Random(25)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?)",
    [(i, rnd.randint(1, 20000), "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500)) for i in range(1, 200001)])
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
tot = df.groupby("customer_id")["amount"].sum()
exp_twice = tot[tot > tot.mean()].reset_index().rename(columns={"amount": "s"}).sort_values("customer_id").reset_index(drop=True)
exp5 = int(df.loc[df.customer_id == 5, "amount"].sum())

print("\n== CTE referenced twice (customers whose total exceeds the average total)")
for nm, hint in (("default", ""), ("AS MATERIALIZED", "MATERIALIZED"), ("AS NOT MATERIALIZED", "NOT MATERIALIZED")):
    sql = TWICE % hint
    rows, n = steps(con, sql)
    pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["customer_id", "s"]), exp_twice)
    print("%-20s rows %5d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)

print("\n== filter applied OUTSIDE a GROUP BY subquery versus the inlined query (customer_id = 5)")
OUT = "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE customer_id = 5"
INL = "SELECT customer_id, SUM(amount) AS s FROM orders WHERE customer_id = 5 GROUP BY customer_id"
CTE1 = "WITH t AS (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE customer_id = 5"
CTE1M = CTE1.replace("AS (SELECT", "AS MATERIALIZED (SELECT")
NOFILT = "SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id"
for nm, sql in (("subquery, filter outside", OUT), ("inlined filter", INL), ("CTE used once, filter outside", CTE1),
                ("CTE used once, AS MATERIALIZED", CTE1M), ("whole aggregate, no filter (for scale)", NOFILT)):
    rows, n = steps(con, sql)
    if "no filter" not in nm:
        assert rows == [(5, exp5)], (nm, rows)
    print("%-38s rows %5d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)

print("\n== what blocks push-down (outer filter customer_id = 5)")
BLOCK = [
 ("LIMIT inside", "SELECT customer_id, amount FROM (SELECT customer_id, amount FROM orders LIMIT 1000000) WHERE customer_id = 5"),
 ("no LIMIT (flattened)", "SELECT customer_id, amount FROM (SELECT customer_id, amount FROM orders) WHERE customer_id = 5"),
 ("DISTINCT inside, filter on a distinct column", "SELECT customer_id, amount FROM (SELECT DISTINCT customer_id, amount FROM orders) WHERE customer_id = 5"),
 ("window inside, filter on PARTITION BY column", "SELECT customer_id, rn FROM (SELECT customer_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id) rn FROM orders) WHERE customer_id = 5"),
 ("window inside, filter on the rank", "SELECT customer_id, rn FROM (SELECT customer_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id) rn FROM orders) WHERE rn = 1 AND customer_id = 5"),
 ("aggregate inside, filter on the aggregate", "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) s FROM orders GROUP BY customer_id) WHERE s > 2000"),
]
for nm, sql in BLOCK:
    rows, n = steps(con, sql)
    want = int((tot > 2000).sum()) if "s > 2000" in sql else (1 if "rn = 1" in sql else int((df.customer_id == 5).sum()))
    assert len(rows) == want, (nm, len(rows), want)
    print("%-46s rows %6d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)
print("asserts passed: every CTE or subquery form matched the pandas result (compared sorted by customer_id)")
```

**Output (my run):**
```text
tiny: per-customer totals [(5, 40), (6, 5), (7, 100)] average of totals 48.333333333333336
tiny: customers above the average total: [(7, 100)]

== CTE referenced twice (customers whose total exceeds the average total)
default              rows  9516  VM steps  2385659
      MATERIALIZE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      SCALAR SUBQUERY 2
      SCAN t
      USE TEMP B-TREE FOR ORDER BY
AS MATERIALIZED      rows  9516  VM steps  2385659
      MATERIALIZE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      SCALAR SUBQUERY 2
      SCAN t
      USE TEMP B-TREE FOR ORDER BY
AS NOT MATERIALIZED  rows  9516  VM steps  4465655
      CO-ROUTINE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      SCALAR SUBQUERY 2
      CO-ROUTINE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      USE TEMP B-TREE FOR ORDER BY

== filter applied OUTSIDE a GROUP BY subquery versus the inlined query (customer_id = 5)
subquery, filter outside               rows     1  VM steps      138
      CO-ROUTINE (subquery-1)
      SEARCH orders USING INDEX ix_cust (customer_id=?)
      SCAN (subquery-1)
inlined filter                         rows     1  VM steps      125
      SEARCH orders USING INDEX ix_cust (customer_id=?)
CTE used once, filter outside          rows     1  VM steps      138
      CO-ROUTINE t
      SEARCH orders USING INDEX ix_cust (customer_id=?)
      SCAN t
CTE used once, AS MATERIALIZED         rows     1  VM steps  2180011
      MATERIALIZE t
      SCAN orders USING INDEX ix_cust
      SCAN t
whole aggregate, no filter (for scale) rows 19999  VM steps  2080004
      SCAN orders USING INDEX ix_cust

== what blocks push-down (outer filter customer_id = 5)
LIMIT inside                                   rows      9  VM steps  1800040
      CO-ROUTINE (subquery-1)
      SCAN orders
      SCAN (subquery-1)
no LIMIT (flattened)                           rows      9  VM steps       63
      SEARCH orders USING INDEX ix_cust (customer_id=?)
DISTINCT inside, filter on a distinct column   rows      9  VM steps      161
      CO-ROUTINE (subquery-1)
      SEARCH orders USING INDEX ix_cust (customer_id=?)
      USE TEMP B-TREE FOR DISTINCT
      SCAN (subquery-1)
window inside, filter on PARTITION BY column   rows      9  VM steps      349
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
      SCAN (subquery-3)
      SCAN (subquery-1)
window inside, filter on the rank              rows      1  VM steps      329
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
      SCAN (subquery-3)
      SCAN (subquery-1)
aggregate inside, filter on the aggregate      rows  13890  VM steps  2178912
      CO-ROUTINE (subquery-1)
      SCAN orders USING INDEX ix_cust
      SCAN (subquery-1)
asserts passed: every CTE or subquery form matched the pandas result (compared sorted by customer_id)
```

**Edge cases:**
- Both materialisation hints return identical rows; they change work, not results (asserted equal to the pandas totals).
- For a CTE referenced twice, NOT MATERIALIZED duplicates the work: it is only a good idea when the CTE is cheap or each use is selective.
- The plan wording CO-ROUTINE versus MATERIALIZE may change between SQLite versions (the EXPLAIN QUERY PLAN format is not a stable interface); these lines are 3.45.1.

**Then explain:**
- CTE referenced twice (200,000 rows, index on customer_id): the default plan was `MATERIALIZE t / SCAN orders USING INDEX ix_cust / SCAN t / SCALAR SUBQUERY 2 / SCAN t`, 2,385,659 steps, identical to AS MATERIALIZED. AS NOT MATERIALIZED showed `CO-ROUTINE t` twice and took 4,465,655 steps, because the whole GROUP BY ran twice. So for several uses SQLite materialises by default.
- A filter outside a GROUP BY subquery on the grouping column (`WHERE customer_id = 5`) was pushed into the subquery: plan `CO-ROUTINE (subquery-1) / SEARCH orders USING INDEX ix_cust (customer_id=?)`, 138 steps, against 125 for the hand-inlined form. The CTE used once with the same filter gave the identical plan and 138 steps: used once, a CTE behaves like a subquery. Adding AS MATERIALIZED to that single-use CTE disabled the push-down: `MATERIALIZE t / SCAN orders`, 2,180,011 steps (computing all 19,999 groups to keep one), close to the unfiltered aggregate (2,080,004 steps).
- Push-down limits observed (outer filter `customer_id = 5`): a LIMIT inside the subquery blocked it (`SCAN orders`, 1,800,040 steps, against 63 without the LIMIT, because the filter after a LIMIT is a different question). A filter on an aggregate result (`s > 2000`) cannot be pushed below the GROUP BY (2,178,912 steps, 13,890 rows). In this version a DISTINCT inside did NOT block a filter on one of the distinct columns (161 steps), and a window with the filter on its PARTITION BY column was pushed down too (349 steps); I did not test a filter on the rank value alone. The premise 'DISTINCT blocks push-down' is therefore only partly true: I tested the case where the filtered column is part of the DISTINCT list, and it did push.
- PostgreSQL, not executed here: from version 12 a single-use CTE that has no side effects is inlined and treated like a subquery, and MATERIALIZED and NOT MATERIALIZED exist there too; before 12, a CTE was an optimisation fence (always materialised). MySQL and SQL Server behaviour is not discussed here because it was not checked.
- Cross-reference Part 3 Q32 (reusing one CTE twice).

**Follow-ups:**
- Why can't `s > 2000` be pushed in? (It depends on the aggregate result, so it is a HAVING.)
- How do you force a one-time computation? (AS MATERIALIZED, or a temporary table.)
- How do you force re-evaluation? (AS NOT MATERIALIZED, useful when the filter makes the CTE tiny.)

**Common mistakes:**
- Treating a CTE as a stored temporary result in every engine.
- Adding AS MATERIALIZED 'for speed' and losing the push-down.
- Reading a plan once and generalising: the plan changes with the SQLite version and the data.

### Q26 ⭐⭐ 🔴 Window-function sort cost and top-N per group plans: sales(sale_id, region, product_id, sale_date, amount) with 300,000 rows, 50 regions. Print plans and VM steps for the top 3 sales per region using (a) ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) filtered in an outer query, with no index, with an index on (region, amount DESC), (b) a correlated COUNT subquery, and (c) a correlated IN subquery with ORDER BY ... LIMIT 3 (check by running what each accepts and prints). Explain that a window needs rows ordered by the partition and order keys so the cost is a sort unless an index supplies the order, why one extra ORDER BY on a different key means a second sort, and why filtering the rank after the window cannot be pushed before it. Cross-reference Part 4 Q40 (window function performance concept) and Part 4 Q39 (top N and pagination).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A window function needs rows ordered by partition then order key, so unless an index supplies that order the plan sorts the whole table; an outer filter on the rank cannot run before the window, so the window still reads all 300,000 rows, and the correlated COUNT form grows quadratically.

**Schema and sample data:**
```sql
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'N',1,'2024-01-01',50),(2,'N',2,'2024-01-02',90),(3,'N',3,'2024-01-03',90),(4,'N',4,'2024-01-04',70),(5,'N',5,'2024-01-05',10),
 (6,'S',1,'2024-01-06',20),(7,'S',2,'2024-01-07',30);
```

**SQL answer:** `WIN` (window), `CNT` (correlated COUNT) and `INL` (correlated IN with ORDER BY ... LIMIT 3) are in the Code block, copied here; the tie-break (amount DESC, sale_id) makes the result deterministic:
```sql
SELECT region, sale_id, amount FROM (
  SELECT region, sale_id, amount, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY region, amount DESC, sale_id

SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE (SELECT COUNT(*) FROM sales b WHERE b.region = a.region
       AND (b.amount > a.amount OR (b.amount = a.amount AND b.sale_id < a.sale_id))) < 3
ORDER BY a.region, a.amount DESC, a.sale_id

SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE a.sale_id IN (SELECT b.sale_id FROM sales b WHERE b.region = a.region ORDER BY b.amount DESC, b.sale_id LIMIT 3)
ORDER BY a.region, a.amount DESC, a.sale_id
```

**pandas answer:** Sort, then `groupby().head(3)`.
```py
def pandas_top3(df):
    d = df.sort_values(["region", "amount", "sale_id"], ascending=[True, False, True])
    return d.groupby("region").head(3)[["region", "sale_id", "amount"]].reset_index(drop=True)
```

**Example:** Tiny table, region N: amounts 50 (id 1), 90 (id 2), 90 (id 3), 70 (id 4), 10 (id 5). Sorted by amount DESC then sale_id: 2 (90), 3 (90), 4 (70), 1 (50), 5 (10); the top 3 are ids 2, 3, 4. Region S: 30 (id 7) and 20 (id 6). All three SQL forms return [('N',2,90),('N',3,90),('N',4,70),('S',7,30),('S',6,20)]. The two 90s are a tie: ROW_NUMBER with the sale_id tie-break picks both; the COUNT form needs the same tie-break in its comparison or it would count ties as equal and could return more than 3 rows.

**Code:** run with `python3 -I`.
```python
# Q26: window sort cost and top-N per group plans
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

WIN = """SELECT region, sale_id, amount FROM (
  SELECT region, sale_id, amount, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY region, amount DESC, sale_id"""
CNT = """SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE (SELECT COUNT(*) FROM sales b WHERE b.region = a.region
       AND (b.amount > a.amount OR (b.amount = a.amount AND b.sale_id < a.sale_id))) < 3
ORDER BY a.region, a.amount DESC, a.sale_id"""
INL = """SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE a.sale_id IN (SELECT b.sale_id FROM sales b WHERE b.region = a.region ORDER BY b.amount DESC, b.sale_id LIMIT 3)
ORDER BY a.region, a.amount DESC, a.sale_id"""
WIN_EXTRA = """SELECT region, sale_id, amount, sale_date FROM (
  SELECT region, sale_id, amount, sale_date, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY sale_date"""

def build(n, seed=26, regions=50):
    rnd = random.Random(seed)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER)")
    con.executemany("INSERT INTO sales VALUES (?,?,?,?,?)",
        [(i, "R%02d" % rnd.randint(1, regions), rnd.randint(1, 500), "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 3000)) for i in range(1, n + 1)])
    con.commit()
    return con

def pandas_top3(df):
    d = df.sort_values(["region", "amount", "sale_id"], ascending=[True, False, True])
    return d.groupby("region").head(3)[["region", "sale_id", "amount"]].reset_index(drop=True)

# tiny sample with a tie
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'N',1,'2024-01-01',50),(2,'N',2,'2024-01-02',90),(3,'N',3,'2024-01-03',90),(4,'N',4,'2024-01-04',70),(5,'N',5,'2024-01-05',10),
 (6,'S',1,'2024-01-06',20),(7,'S',2,'2024-01-07',30);""")
for nm, q in (("window", WIN), ("correlated COUNT", CNT), ("correlated IN + LIMIT", INL)):
    print("tiny", nm, t.execute(q).fetchall())
print("tiny: plain count form with only '>' would return", t.execute("""SELECT a.sale_id FROM sales a WHERE (SELECT COUNT(*) FROM sales b WHERE b.region=a.region AND b.amount > a.amount) < 3 AND a.region='N' ORDER BY 1""").fetchall(), "(ties at 90 both rank 0, 70 rank 2, 50 rank 3 excluded; tie-break matters when ranks collide)")

# same-size comparison of all forms at 6,000 rows (the correlated forms are too slow at 300,000 without early exit)
print("\n== 6,000 rows (50 regions x about 120 rows), all forms, with and without the index")
small = build(6000)
sdf = pd.read_sql("SELECT * FROM sales", small)
exp_s = pandas_top3(sdf)
for idx in (False, True):
    if idx:
        small.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)"); small.commit()
    for nm, q in (("window", WIN), ("correlated COUNT", CNT), ("correlated IN + LIMIT", INL)):
        rows, n = steps(small, q)
        pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_s)
        print("index=%-5s %-22s rows %3d VM steps %9d" % (idx, nm, len(rows), n))
        for l in plan(small, q): print("       ", l)

print("\n== quadratic growth of the correlated COUNT with the index (rows per region grows with n)")
for n in (3000, 6000, 12000):
    c = build(n); c.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)")
    print("  n=%6d steps %9d  steps/n = %.1f" % (n, steps(c, CNT)[1], steps(c, CNT)[1] / n))

print("\n== 300,000 rows")
big = build(300000)
bdf = pd.read_sql("SELECT * FROM sales", big)
exp_b = pandas_top3(bdf)
rows, n = steps(big, WIN)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("window, no index:                      rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, WIN): print("       ", l)
big.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)"); big.commit()
rows, n = steps(big, WIN)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("window, index (region, amount DESC, sale_id): rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, WIN): print("       ", l)
rows, n = steps(big, INL)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("correlated IN + LIMIT, index:           rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, INL): print("       ", l)
print("(correlated COUNT not run at 300,000 rows: it needs about n*rows-per-region/2 index entries, see the growth table)")

print("\n== where the sorts come from, 300,000 rows (index present)")
WIN_NOORD = WIN.replace(" ORDER BY region, amount DESC, sale_id", "")
for nm, q in (("window, NO outer ORDER BY", WIN_NOORD), ("window, outer ORDER BY region, amount DESC, sale_id", WIN),
              ("window, outer ORDER BY sale_date (another key)", WIN_EXTRA)):
    rows, n = steps(big, q)
    pl = plan(big, q)
    print("%-52s rows %d VM steps %9d temp b-trees %d" % (nm, len(rows), n, sum("TEMP B-TREE" in l for l in pl)))
    for l in pl: print("       ", l)
big.execute("DROP INDEX ix_reg_amt"); big.commit()
for nm, q in (("NO index, no outer ORDER BY", WIN_NOORD), ("NO index, outer ORDER BY", WIN)):
    pl = plan(big, q)
    print("%-52s temp b-trees %d" % (nm, sum("TEMP B-TREE" in l for l in pl)))
print("asserts passed: all forms equal the pandas sort + groupby.head(3) (compared in order region, amount desc, sale_id)")
```

**Output (my run):**
```text
tiny window [('N', 2, 90), ('N', 3, 90), ('N', 4, 70), ('S', 7, 30), ('S', 6, 20)]
tiny correlated COUNT [('N', 2, 90), ('N', 3, 90), ('N', 4, 70), ('S', 7, 30), ('S', 6, 20)]
tiny correlated IN + LIMIT [('N', 2, 90), ('N', 3, 90), ('N', 4, 70), ('S', 7, 30), ('S', 6, 20)]
tiny: plain count form with only '>' would return [(2,), (3,), (4,)] (ties at 90 both rank 0, 70 rank 2, 50 rank 3 excluded; tie-break matters when ranks collide)

== 6,000 rows (50 regions x about 120 rows), all forms, with and without the index
index=False window                 rows 150 VM steps    290187
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales
        USE TEMP B-TREE FOR ORDER BY
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
index=False correlated COUNT       rows 150 VM steps 147731516
        SCAN a
        CORRELATED SCALAR SUBQUERY 1
        SCAN b
        USE TEMP B-TREE FOR ORDER BY
index=False correlated IN + LIMIT  rows 150 VM steps 148685000
        SCAN a
        CORRELATED LIST SUBQUERY 1
        SCAN b
        USE TEMP B-TREE FOR ORDER BY
        USE TEMP B-TREE FOR ORDER BY
index=True  window                 rows 150 VM steps    230185
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
index=True  correlated COUNT       rows 150 VM steps   5195467
        SCAN a USING COVERING INDEX ix_reg_amt
        CORRELATED SCALAR SUBQUERY 1
        SEARCH b USING COVERING INDEX ix_reg_amt (region=?)
index=True  correlated IN + LIMIT  rows 150 VM steps    162611
        SCAN a USING COVERING INDEX ix_reg_amt
        CORRELATED LIST SUBQUERY 1
        SEARCH b USING COVERING INDEX ix_reg_amt (region=?)

== quadratic growth of the correlated COUNT with the index (rows per region grows with n)
  n=  3000 steps   1332755  steps/n = 444.2
  n=  6000 steps   5195467  steps/n = 865.9
  n= 12000 steps  20470934  steps/n = 1705.9

== 300,000 rows
window, no index:                      rows 150 VM steps  14402187
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales
        USE TEMP B-TREE FOR ORDER BY
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
window, index (region, amount DESC, sale_id): rows 150 VM steps  11402185
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
correlated IN + LIMIT, index:           rows 150 VM steps   8100611
        SCAN a USING COVERING INDEX ix_reg_amt
        CORRELATED LIST SUBQUERY 1
        SEARCH b USING COVERING INDEX ix_reg_amt (region=?)
(correlated COUNT not run at 300,000 rows: it needs about n*rows-per-region/2 index entries, see the growth table)

== where the sorts come from, 300,000 rows (index present)
window, NO outer ORDER BY                            rows 150 VM steps  11401132 temp b-trees 0
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
window, outer ORDER BY region, amount DESC, sale_id  rows 150 VM steps  11402181 temp b-trees 1
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
window, outer ORDER BY sale_date (another key)       rows 150 VM steps  12602486 temp b-trees 1
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
NO index, no outer ORDER BY                          temp b-trees 1
NO index, outer ORDER BY                             temp b-trees 2
asserts passed: all forms equal the pandas sort + groupby.head(3) (compared in order region, amount desc, sale_id)
```

**Edge cases:**
- Ties at the cut-off: ROW_NUMBER gives exactly 3 rows per region; RANK or the plain `b.amount > a.amount` COUNT can return more. The tie-break columns in every form make the comparison with pandas exact.
- A region with fewer than 3 rows returns what it has (region S).
- The correlated forms were compared at 6,000 rows (all three forms, with and without the index) and at 300,000 rows only where they finish in reasonable time (window, correlated IN with index); the correlated COUNT was not run at 300,000 rows.

**Then explain:**
- 6,000 rows (50 regions x about 120 rows) VM steps, no index: window 290,187; correlated COUNT 147,731,516; correlated IN + LIMIT 148,685,000. With an index on (region, amount DESC, sale_id): window 230,185; COUNT 5,195,467; IN + LIMIT 162,611. Without an index each correlated outer row rescans or re-sorts its region (two temp B-trees for the IN form).
- Growth of the correlated COUNT with the index: 3,000 rows 1,332,755 steps (444 per row), 6,000 rows 5,195,467 (866 per row), 12,000 rows 20,470,934 (1,706 per row): steps per row double when n doubles, so cost is quadratic, because each row counts the rows above it in its region. That is why it was not run at 300,000.
- 300,000 rows: window with no index 14,402,187 steps; with the index 11,402,185 steps; correlated IN with ORDER BY ... LIMIT 3 and the index 8,100,611 steps (each outer row reads about three index entries), lower than the window here. All three were asserted equal to pandas. SQLite accepted LIMIT inside an IN subquery; MySQL is known to reject LIMIT in such a subquery (hedged, not run).
- Sorts, counted from the plans: with no index the window plan has `USE TEMP B-TREE FOR ORDER BY` twice (the window's partition/order sort plus the final ORDER BY: 2); with the index the window sort disappears (`SCAN sales USING COVERING INDEX ix_reg_amt`) and only the final ORDER BY sort remains (1); dropping that final ORDER BY leaves 0. A different outer ORDER BY key (sale_date) needs its own sort on top of whatever order the window had (1 sort, plus a non-covering index scan, 12,602,486 steps). So an extra ORDER BY on another key is an extra sort.
- Why the rank filter is not pushed before the window: `rn <= 3` depends on the window's output, and the window needs all rows of each partition to number them, so the plan reads all 300,000 rows (about 11.4 million steps even with the index) to return 150. The index saves the sort, not the scan.
- Cross-references: Part 4 Q40 (window function performance concept) and Part 4 Q39 (top N and pagination).

**Follow-ups:**
- How would you make top 3 per region cheap at 300,000 rows? (The correlated IN with an index above, or a LATERAL join in engines that have it, not executed; or keep a pre-aggregated table.)
- RANK versus ROW_NUMBER at a tie? (RANK keeps both tied rows, so more than 3 can come back.)
- Does the same plan appear in PostgreSQL? (Not executed; there, a WindowAgg node over a Sort or an Index Scan is the usual shape.)

**Common mistakes:**
- Running the correlated COUNT on the full table without checking its growth.
- Forgetting a tie-break and getting nondeterministic or inflated results.
- Believing `WHERE rn <= 3` makes the window stop early.
- Comparing plans for a statement text the connection has already planned (this run varies the text).

### Q27 ⭐⭐ 🟡 Push SQL work down before loading into pandas: a SQLite orders table with 500,000 seeded rows (order_id, customer_id, order_date, status, amount) and the task 'monthly revenue for delivered orders in 2024'. Compare (a) pd.read_sql of the whole table then pandas filter and groupby, (b) read_sql with WHERE and GROUP BY in SQL, (c) read_sql with chunksize (stream and aggregate per chunk), and (d) read_sql with only the columns needed. Assert the three results equal, report rows transferred, df.memory_usage(deep=True) and timings labelled machine-specific, and explain when to push down (filters, aggregations, joins on indexed keys, sampling) and when pandas is better (iterative exploration, logic hard to express in SQL), and why chunked aggregation only works for decomposable aggregates (sum and count, not median).
**Asked at:** pandas user guide pages 'Enhancing performance' and 'Scaling to large datasets' (opened); official documentation, not candidate reports; data scientist and analytics engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Filter, aggregate and join in the database before the rows reach pandas: pulling 500,000 rows to compute 12 monthly totals moved 500,000 rows and 70 MB while the GROUP BY query moved 12 rows, and chunked reading saves memory, not time; chunked aggregation only works for decomposable aggregates such as sum and count.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-05','delivered',100),(2,2,'2024-01-20','delivered',50),(3,3,'2024-01-21','cancelled',999),
 (4,1,'2024-02-02','delivered',70),(5,2,'2023-12-31','delivered',500),(6,3,'2025-01-01','delivered',5);
```

**SQL answer:** The pushed-down query `SQL` is in the Code block, copied here:
```sql
SELECT substr(order_date, 1, 7) AS month, SUM(amount) AS revenue, COUNT(*) AS n_orders
FROM orders WHERE status = 'delivered' AND order_date >= '2024-01-01' AND order_date < '2025-01-01'
GROUP BY month ORDER BY month
```

**pandas answer:** The same aggregation in pandas, used for (a), (c) and (d) (a function in the Code block):
```py
def pandas_agg(df):
    d = df[(df["status"] == "delivered") & (df["order_date"] >= "2024-01-01") & (df["order_date"] < "2025-01-01")]
    g = d.assign(month=d["order_date"].str[:7]).groupby("month").agg(revenue=("amount", "sum"), n_orders=("amount", "size"))
    return g.reset_index().sort_values("month").reset_index(drop=True)
```

**Example:** Tiny table: delivered orders in 2024 are 1 (Jan, 100), 2 (Jan, 50) and 4 (Feb, 70). Order 3 is cancelled (excluded), order 5 is 2023-12-31 and order 6 is 2025-01-01 (outside 2024). Result: 2024-01 revenue 150 (2 orders) and 2024-02 revenue 70 (1 order); the run prints `[('2024-01', 150, 2), ('2024-02', 70, 1)]`. At 500,000 rows (seed 27) the same 12 monthly totals come out of all methods.

**Code:** run with `python3 -I`.
```python
# Q27: push SQL work down before loading into pandas
import sqlite3, random, os, tempfile, time
import numpy as np
import pandas as pd

rnd = random.Random(27)
statuses = ["delivered"] * 70 + ["cancelled"] * 10 + ["returned"] * 10 + ["placed"] * 10
rows = [(i, rnd.randint(1, 50000), "%d-%02d-%02d" % (rnd.choice([2023, 2024, 2024, 2025]), rnd.randint(1, 12), rnd.randint(1, 28)),
         rnd.choice(statuses), rnd.randint(10, 5000)) for i in range(1, 500001)]
tmp = tempfile.TemporaryDirectory()
path = os.path.join(tmp.name, "orders.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.commit()
con.close()
print("database file: %.1f MB, 500,000 rows" % (os.path.getsize(path) / 1e6))

# tiny sample for the hand walk-through
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-05','delivered',100),(2,2,'2024-01-20','delivered',50),(3,3,'2024-01-21','cancelled',999),
 (4,1,'2024-02-02','delivered',70),(5,2,'2023-12-31','delivered',500),(6,3,'2025-01-01','delivered',5);""")
SQL = """SELECT substr(order_date, 1, 7) AS month, SUM(amount) AS revenue, COUNT(*) AS n_orders
FROM orders WHERE status = 'delivered' AND order_date >= '2024-01-01' AND order_date < '2025-01-01'
GROUP BY month ORDER BY month"""
print("tiny:", t.execute(SQL).fetchall())

def timed(fn):
    t0 = time.perf_counter()
    out = fn()
    return out, (time.perf_counter() - t0) * 1000

conn = sqlite3.connect(path)
res = {}

def pandas_agg(df):
    d = df[(df["status"] == "delivered") & (df["order_date"] >= "2024-01-01") & (df["order_date"] < "2025-01-01")]
    g = d.assign(month=d["order_date"].str[:7]).groupby("month").agg(revenue=("amount", "sum"), n_orders=("amount", "size"))
    return g.reset_index().sort_values("month").reset_index(drop=True)

# (a) whole table
full, ms = timed(lambda: pd.read_sql("SELECT * FROM orders", conn))
mem_a = int(full.memory_usage(deep=True).sum())
res["a"], ms2 = timed(lambda: pandas_agg(full))
print("(a) read whole table: rows transferred %d, memory_usage(deep) %.1f MB, load %.0f ms + filter/groupby %.0f ms" % (len(full), mem_a / 1e6, ms, ms2))
print("    dtypes:", dict(full.dtypes.astype(str)))
t_a = ms + ms2
# (b) SQL does the filter and aggregation
dfb, t_b = timed(lambda: pd.read_sql(SQL, conn))
res["b"] = dfb
print("(b) WHERE + GROUP BY in SQL: rows transferred %d, memory_usage(deep) %d bytes, %.0f ms" % (len(dfb), dfb.memory_usage(deep=True).sum(), t_b))
# (c) chunked: stream, aggregate per chunk, combine
def chunked():
    parts, total_rows, peak = [], 0, 0
    for ch in pd.read_sql("SELECT * FROM orders", conn, chunksize=50000):
        total_rows += len(ch)
        peak = max(peak, int(ch.memory_usage(deep=True).sum()))
        parts.append(pandas_agg(ch))
    allp = pd.concat(parts)
    out = allp.groupby("month", as_index=False)[["revenue", "n_orders"]].sum().sort_values("month").reset_index(drop=True)
    return out, total_rows, peak
(res["c"], rows_c, peak_c), t_c = timed(chunked)
print("(c) chunksize=50,000, aggregate per chunk: rows transferred %d, peak chunk memory %.1f MB, %.0f ms" % (rows_c, peak_c / 1e6, t_c))
# (d) only the needed columns, filter in SQL but aggregate in pandas; and columns only (no WHERE)
def cols_only():
    return pd.read_sql("SELECT order_date, status, amount FROM orders", conn)
dcols, t_d1 = timed(cols_only)
res["d"], t_d2 = timed(lambda: pandas_agg(dcols))
print("(d) only 3 needed columns, filter in pandas: rows transferred %d, memory_usage(deep) %.1f MB, %.0f ms + %.0f ms" % (len(dcols), dcols.memory_usage(deep=True).sum() / 1e6, t_d1, t_d2))
dwhere, t_d3 = timed(lambda: pd.read_sql("SELECT order_date, amount FROM orders WHERE status = 'delivered' AND order_date >= '2024-01-01' AND order_date < '2025-01-01'", conn))
res["e"] = (dwhere.assign(month=dwhere["order_date"].str[:7]).groupby("month").agg(revenue=("amount", "sum"), n_orders=("amount", "size")).reset_index())
print("(e) WHERE pushed down, 2 columns, aggregate in pandas: rows transferred %d, memory_usage(deep) %.1f MB, %.0f ms" % (len(dwhere), dwhere.memory_usage(deep=True).sum() / 1e6, t_d3))

for k in ("a", "c", "d", "e"):
    pd.testing.assert_frame_equal(res[k][["month", "revenue", "n_orders"]].astype({"revenue": "int64", "n_orders": "int64"}),
                                   res["b"][["month", "revenue", "n_orders"]].astype({"revenue": "int64", "n_orders": "int64"}))
print("asserts passed: (a), (c), (d), (e) equal (b); compared sorted by month; revenue and n_orders as int64")
print(res["b"].to_string(index=False))
print("timings are machine-specific single runs: a=%.0f ms, b=%.0f ms, c=%.0f ms, d=%.0f ms, e=%.0f ms" % (t_a, t_b, t_c, t_d1 + t_d2, t_d3))

# decomposable versus not
chunk_med = []
for ch in pd.read_sql("SELECT order_date, status, amount FROM orders WHERE status = 'delivered'", conn, chunksize=50000):
    chunk_med.append(ch["amount"].median())
true_med = pd.read_sql("SELECT amount FROM orders WHERE status = 'delivered'", conn)["amount"].median()
print("\nmedian of delivered amounts: true %.1f; mean of the 50,000-row chunk medians %.1f (equal here only because every chunk is a random sample of the same distribution)" % (true_med, float(np.mean(chunk_med))))
c1, c2 = pd.Series([1, 2, 9]), pd.Series([3, 4, 5, 6, 7])
print("counterexample: true median of all 8 values %.1f, mean of the two chunk medians %.1f" % (pd.concat([c1, c2]).median(), (c1.median() + c2.median()) / 2))
# mean needs (sum, count) pairs
sums = pd.read_sql("SELECT SUM(amount) s, COUNT(*) c FROM orders WHERE status = 'delivered'", conn).iloc[0]
print("mean from decomposed (sum, count): %.4f; direct mean: %.4f" % (sums["s"] / sums["c"], full.loc[full.status == "delivered", "amount"].mean()))
tmp.cleanup()
```

**Output (my run):**
```text
database file: 17.6 MB, 500,000 rows
tiny: [('2024-01', 150, 2), ('2024-02', 70, 1)]
(a) read whole table: rows transferred 500000, memory_usage(deep) 70.3 MB, load 1249 ms + filter/groupby 251 ms
    dtypes: {'order_id': 'int64', 'customer_id': 'int64', 'order_date': 'str', 'status': 'str', 'amount': 'int64'}
(b) WHERE + GROUP BY in SQL: rows transferred 12, memory_usage(deep) 996 bytes, 155 ms
(c) chunksize=50,000, aggregate per chunk: rows transferred 500000, peak chunk memory 7.0 MB, 1492 ms
(d) only 3 needed columns, filter in pandas: rows transferred 500000, memory_usage(deep) 62.3 MB, 787 ms + 284 ms
(e) WHERE pushed down, 2 columns, aggregate in pandas: rows transferred 174908, memory_usage(deep) 11.7 MB, 316 ms
asserts passed: (a), (c), (d), (e) equal (b); compared sorted by month; revenue and n_orders as int64
  month  revenue  n_orders
2024-01 37025467     14746
2024-02 36307646     14513
2024-03 37027482     14744
2024-04 36358880     14419
2024-05 37196747     14761
2024-06 36614750     14526
2024-07 36298940     14510
2024-08 36623888     14588
2024-09 36100832     14392
2024-10 36491865     14610
2024-11 36228945     14444
2024-12 36541770     14655
timings are machine-specific single runs: a=1500 ms, b=155 ms, c=1492 ms, d=1071 ms, e=316 ms

median of delivered amounts: true 2511.0; mean of the 50,000-row chunk medians 2511.0 (equal here only because every chunk is a random sample of the same distribution)
counterexample: true median of all 8 values 4.5, mean of the two chunk medians 3.5
mean from decomposed (sum, count): 2507.8495; direct mean: 2507.8495
```

**Edge cases:**
- The date range is a half-open interval (`>= '2024-01-01' AND < '2025-01-01'`), which is safe for dates stored as ISO text; the month is `substr(order_date,1,7)` in SQL and `str[:7]` in pandas.
- Chunked results are partial sums per month; the per-chunk frames are concatenated and summed again. A month absent from a chunk simply contributes nothing.
- All five paths are asserted equal after casting revenue and n_orders to int64 and comparing sorted by month.

**Then explain:**
- Measured (500,000-row file database of 17.6 MB; timings are machine-specific single runs): (a) read the whole table: 500,000 rows transferred, `memory_usage(deep=True)` 70.3 MB, load about 1.2 s plus about 0.25 s to filter and group. (b) WHERE + GROUP BY in SQL: 12 rows, 996 bytes, about 0.16 s. (c) `chunksize=50,000`: still 500,000 rows transferred, peak chunk memory 7.0 MB, about 1.5 s: memory bounded, time not better. (d) only the three needed columns, filter in pandas: 500,000 rows, 62.3 MB, about 0.8 s load plus 0.28 s. (e) WHERE pushed down but aggregation in pandas, two columns: 174,908 rows, 11.7 MB, about 0.3 s.
- Honest observations: selecting columns alone (d) saved only 8 MB because the two dropped columns are integers, while the string columns order_date and status dominate the memory (pandas 3 uses the `str` dtype). The biggest saving is moving the filter (e) and the aggregation (b) to the database. No index was created here, so (b) still scanned the table in SQLite; an index on (status, order_date) would help but was not measured.
- Push down: filters, aggregations, joins on indexed keys, sampling and `LIMIT`; it reduces transferred rows and memory and uses the engine's indexes. Pandas is better for iterative exploration (re-slicing the same data many times after one load), logic that is awkward in SQL (complex reshaping, custom Python functions) and when the data is already small.
- Chunked aggregation works for decomposable aggregates (sum, count, min, max, and mean via sum and count): partial results combine exactly. The run shows mean from decomposed (sum, count) equal to the direct mean (2507.8495). A median does not decompose: the mean of 50,000-row chunk medians equalled the true median here only by chance (every chunk is a random sample of the same distribution); the counterexample with chunks [1,2,9] and [3,4,5,6,7] gives a true median of 4.5 and a mean of chunk medians of 3.5.
- Source note: the pandas guides named in the Asked-at line were opened for ideas only; no numbers from them are used.

**Follow-ups:**
- Would you use chunksize with a GROUP BY already in SQL? (Not needed: the result is small.)
- How would you do an exact median in chunks? (Two passes with a histogram or a sorted external merge, or use the database's percentile function where it exists; not run.)
- What if the table has no index? (Pushdown still reduces transfer, but the database scans; add an index for repeated queries.)

**Common mistakes:**
- Reading the whole table 'because pandas is easier' and then filtering.
- Using chunksize to speed things up (it reduces peak memory).
- Averaging chunk means or medians of unequal chunks.
- Forgetting that SELECT * of text columns costs far more memory than the integer columns.
