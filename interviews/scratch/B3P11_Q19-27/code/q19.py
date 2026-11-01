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
