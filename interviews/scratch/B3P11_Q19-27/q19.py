# Q19: fan-out joins and pre-aggregation (SQLite 3.45 + pandas)
import os, random, sqlite3, tempfile
import pandas as pd

random.seed(19)
path = os.path.join(tempfile.mkdtemp(), "q19.db")
con = sqlite3.connect(path)
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
""")
N_CUST, N_ORD, N_ITEM = 20_000, 100_000, 400_000
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, f"c{i}") for i in range(1, N_CUST + 1)])
con.executemany("INSERT INTO orders VALUES (?,?,?)",
                [(i, random.randint(1, N_CUST), random.randint(100, 5000)) for i in range(1, N_ORD + 1)])
con.executemany("INSERT INTO order_items VALUES (?,?,?,?)",
                [(i, random.randint(1, N_ORD), random.randint(1, 5), random.randint(10, 500)) for i in range(1, N_ITEM + 1)])
con.execute("CREATE INDEX ix_ord_cust ON orders(customer_id)")
con.execute("CREATE INDEX ix_item_ord ON order_items(order_id)")
con.commit()
con.close()
print("sqlite", sqlite3.sqlite_version, "| pandas", pd.__version__)

def run(sql, params=()):
    c = sqlite3.connect(path)
    try:
        return c.execute(sql, params).fetchall()
    finally:
        c.close()

def plan(sql):
    return [r[3] for r in run("EXPLAIN QUERY PLAN " + sql)]   # fresh connection every time

def steps(sql):
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

# grain checks: is each side one row per key?
print("\ngrain checks")
print("orders: rows", run("SELECT COUNT(*) FROM orders")[0][0], "distinct order_id", run("SELECT COUNT(DISTINCT order_id) FROM orders")[0][0])
print("order_items: rows", run("SELECT COUNT(*) FROM order_items")[0][0], "distinct order_id", run("SELECT COUNT(DISTINCT order_id) FROM order_items")[0][0],
      "-> many items per order")
print("rows in the 3-table join:", run("""SELECT COUNT(*) FROM customers c JOIN orders o ON o.customer_id = c.customer_id
                                        JOIN order_items i ON i.order_id = o.order_id""")[0][0])

NAIVE = """
SELECT c.customer_id,
       COUNT(o.order_id)  AS n_orders,
       SUM(o.order_total) AS revenue,
       SUM(i.qty)         AS qty
FROM customers c
LEFT JOIN orders o      ON o.customer_id = c.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
GROUP BY c.customer_id
ORDER BY c.customer_id
"""
FIX_ORDERS_ITEMS = """
SELECT c.customer_id,
       COUNT(o.order_id)                AS n_orders,
       COALESCE(SUM(o.order_total), 0)  AS revenue,
       COALESCE(SUM(oi.qty), 0)         AS qty
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN (SELECT order_id, SUM(qty) AS qty
           FROM order_items
           GROUP BY order_id) oi ON oi.order_id = o.order_id
GROUP BY c.customer_id
ORDER BY c.customer_id
"""
FIX_PER_CUSTOMER = """
WITH o AS (SELECT customer_id, COUNT(*) AS n_orders, SUM(order_total) AS revenue
           FROM orders
           GROUP BY customer_id),
     q AS (SELECT o2.customer_id, SUM(i.qty) AS qty
           FROM orders o2
           JOIN order_items i ON i.order_id = o2.order_id
           GROUP BY o2.customer_id)
SELECT c.customer_id,
       COALESCE(o.n_orders, 0) AS n_orders,
       COALESCE(o.revenue, 0)  AS revenue,
       COALESCE(q.qty, 0)      AS qty
FROM customers c
LEFT JOIN o ON o.customer_id = c.customer_id
LEFT JOIN q ON q.customer_id = c.customer_id
ORDER BY c.customer_id
"""

cols = ["customer_id", "n_orders", "revenue", "qty"]
res, st, pl = {}, {}, {}
for name, sql in [("naive", NAIVE), ("fix_orders_items", FIX_ORDERS_ITEMS), ("fix_per_customer", FIX_PER_CUSTOMER)]:
    st[name], rows = steps(sql)
    res[name] = pd.DataFrame(rows, columns=cols)
    pl[name] = plan(sql)

# pandas truth: groupby on each grain, then merge
cust = pd.read_sql_query("SELECT * FROM customers", sqlite3.connect(path))
orders = pd.read_sql_query("SELECT * FROM orders", sqlite3.connect(path))
items = pd.read_sql_query("SELECT * FROM order_items", sqlite3.connect(path))
# pd:main
o_agg = orders.groupby("customer_id").agg(n_orders=("order_id", "size"), revenue=("order_total", "sum"))
item_cust = items.merge(orders[["order_id", "customer_id"]], on="order_id")
q_agg = item_cust.groupby("customer_id").agg(qty=("qty", "sum"))
pd_res = (cust[["customer_id"]].merge(o_agg, on="customer_id", how="left")
                               .merge(q_agg, on="customer_id", how="left")
                               .fillna(0).astype("int64")
                               .sort_values("customer_id").reset_index(drop=True))
# pd:end
pd_res = pd_res[cols]

true_rev, true_cnt, true_qty = int(pd_res.revenue.sum()), int(pd_res.n_orders.sum()), int(pd_res.qty.sum())
print("\ntruth (pandas): orders", true_cnt, "| SUM(order_total) over all customers", true_rev, "| qty", true_qty)
print("naive join   : orders", int(res["naive"].n_orders.sum()), "| SUM(order_total)", int(res["naive"].revenue.sum()),
      "| qty", int(res["naive"].qty.sum()))
assert int(res["naive"].revenue.sum()) != true_rev and int(res["naive"].n_orders.sum()) != true_cnt
assert int(res["naive"].qty.sum()) == true_qty          # qty is on the finest grain, so it survives
print("naive inflates revenue by factor %.3f (orders-with-items repeated once per item)" % (res["naive"].revenue.sum() / true_rev))

# both fixes equal pandas (compared after sorting by customer_id, all four columns)
for name in ("fix_orders_items", "fix_per_customer"):
    pd.testing.assert_frame_equal(res[name], pd_res, check_dtype=False)
print("both pre-aggregated forms equal the pandas groupby on all", len(pd_res), "customers (sorted by customer_id)")

print("\nVM steps (set_progress_handler, deterministic):")
for k in st:
    print(f"  {k:18s} {st[k]:>12,}")
print("\nplans (fresh connection per plan):")
for k in pl:
    print(" ", k)
    for line in pl[k]:
        print("     ", line)
