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
