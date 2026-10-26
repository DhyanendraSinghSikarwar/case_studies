# Q4: composite index ix(customer_id, status, order_date): which columns does each predicate use?
import random
import sqlite3
import pandas as pd

random.seed(4)
statuses = ["placed", "shipped", "delivered", "cancelled"]
rows = [(i, random.randint(1, 20000), random.choice(statuses),
         f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", round(random.uniform(10, 500), 2))
        for i in range(1, 200001)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.execute("CREATE INDEX ix ON orders(customer_id, status, order_date)")
con.commit()

_n = [0]
def plan(where, order=""):
    _n[0] += 1
    w = f"WHERE {where} " if where else ""
    rows_ = con.execute(f"EXPLAIN QUERY PLAN SELECT * FROM orders {w}{order}" + " " * _n[0]).fetchall()
    return " | ".join(r[3] for r in rows_)

def steps(sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    n = len(con.execute(sql).fetchall())
    con.set_progress_handler(None, 0)
    return c[0], n

tests = [
    ("customer_id=5",                                   "customer_id = 5"),
    ("customer_id=5 AND status",                        "customer_id = 5 AND status = 'placed'"),
    ("all three equal",                                 "customer_id = 5 AND status = 'placed' AND order_date = '2024-03-05'"),
    ("status alone",                                    "status = 'placed'"),
    ("order_date range alone",                          "order_date >= '2024-03-01' AND order_date < '2024-04-01'"),
    ("customer_id=5 AND order_date>? (gap)",            "customer_id = 5 AND order_date > '2024-06-01'"),
    ("customer_id>? AND status=?",                      "customer_id > 19900 AND status = 'placed'"),
    ("cust=5 AND status IN AND date>",                  "customer_id = 5 AND status IN ('placed','shipped') AND order_date > '2024-06-01'"),
    ("cust=5 AND status>? AND date>?",                  "customer_id = 5 AND status > 'a' AND order_date > '2024-06-01'"),
]
rowsout = []
for name, w in tests:
    s, n = steps(f"SELECT * FROM orders WHERE {w}")
    rowsout.append((name, plan(w), s, n))
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
print(pd.DataFrame(rowsout, columns=["predicate", "plan", "vm_steps", "rows"]).to_string(index=False))

print("\nORDER BY only:")
print("ORDER BY customer_id, status, order_date LIMIT 5 ->", plan("", "ORDER BY customer_id, status, order_date LIMIT 5"))
print("ORDER BY status LIMIT 5 ->", plan("", "ORDER BY status LIMIT 5"))
print("cust=5 ORDER BY status, order_date ->", plan("customer_id = 5", "ORDER BY status, order_date"))
print("cust=5 ORDER BY order_date ->", plan("customer_id = 5", "ORDER BY order_date"))

# skip-scan: leading column with few distinct values, only after ANALYZE
con.execute("CREATE TABLE o2 AS SELECT * FROM orders")
con.execute("CREATE INDEX ix2 ON o2(status, order_date)")
def plan2(sql):
    _n[0] += 1
    return con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]).fetchall()[0][3]
q = "SELECT * FROM o2 WHERE order_date = '2024-03-05'"
print("\nskip-scan before ANALYZE:", plan2(q), steps(q))
con.execute("ANALYZE")
print("stat1:", con.execute("SELECT idx, stat FROM sqlite_stat1 WHERE tbl='o2'").fetchall())
print("skip-scan after ANALYZE: ", plan2(q), steps(q))
# a high-cardinality leading column: no skip-scan
con.execute("CREATE TABLE o3 AS SELECT * FROM orders")
con.execute("CREATE INDEX ix3 ON o3(customer_id, order_date)")
con.execute("ANALYZE")
print("high-cardinality leading column:", plan2("SELECT * FROM o3 WHERE order_date = '2024-03-05'"))

# pandas: groupby/filter on a MultiIndex needs the leading levels in order
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount"])
mi = df.set_index(["customer_id", "status", "order_date"]).sort_index()
a = mi.loc[(5, "placed")].reset_index()
b = df[(df.customer_id == 5) & (df.status == "placed")]
assert sorted(a.order_id) == sorted(b.order_id)
sqlids = sorted(r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id=5 AND status='placed'"))
assert sqlids == sorted(b.order_id)
print("\npandas MultiIndex .loc[(5,'placed')] rows:", len(a), "| same as mask and SQL (sorted order_id): True")
