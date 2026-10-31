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
