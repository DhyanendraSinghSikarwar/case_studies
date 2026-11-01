# Q8: semi-join as IN, EXISTS, JOIN + DISTINCT, JOIN + GROUP BY, with and without an index on orders(customer_id).
import random
import sqlite3
import pandas as pd

def build(ncust, nord, active, seed=8):
    random.seed(seed)
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, amount REAL);
    """)
    con.executemany("INSERT INTO customers VALUES (?,?,?)",
                    [(i, f"c{i}", ["Pune", "Delhi"][i % 2]) for i in range(1, ncust + 1)])
    # only the first `active` customers order at all; 'placed' is about 10 percent of orders
    con.executemany("INSERT INTO orders VALUES (?,?,?,?)",
                    [(i, random.randint(1, active), random.choices(["placed", "shipped", "delivered", "cancelled"], [1, 4, 4, 1])[0],
                      round(random.uniform(10, 500), 2)) for i in range(1, nord + 1)])
    con.commit()
    return con

forms = {
 "IN":            "SELECT customer_id, name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders WHERE status = 'placed')",
 "EXISTS":        "SELECT c.customer_id, c.name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'placed')",
 "JOIN+DISTINCT": "SELECT DISTINCT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'placed'",
 "JOIN+GROUP BY": "SELECT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'placed' GROUP BY c.customer_id, c.name",
}
plain = "SELECT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'placed'"

_n = [0]
def plan(con, sql):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]))
def run(con, sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

def report(con, label):
    print(f"=== {label}")
    res = {}
    for name, q in forms.items():
        s, r = run(con, q)
        res[name] = sorted(r)
        print(f"{name:14s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, q)}")
    s, r = run(con, plain)
    print(f"{'plain JOIN':14s} steps {s:9d} rows {len(r):6d}  (distinct customers in those rows: {len(set(r))})")
    ref = res["IN"]
    assert all(v == ref for v in res.values())
    return ref

# 1. no index: the correlated EXISTS rescans orders per customer, so use a small copy (2,000 / 20,000)
small = build(2000, 20000, 1500)
report(small, "NO index on orders(customer_id), SMALL data 2,000 customers / 20,000 orders")

# 2. full size 20,000 / 200,000, with the index
con = build(20000, 200000, 15000)
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
ref = report(con, "index ix_cust(customer_id), FULL data 20,000 customers / 200,000 orders")
con.execute("DROP INDEX ix_cust")
con.execute("CREATE INDEX ix_cs ON orders(customer_id, status)")
ref2 = report(con, "index ix_cs(customer_id, status), FULL data")
assert ref == ref2

# 3. full size without an index, only the forms that finish quickly (EXISTS skipped on purpose)
con.execute("DROP INDEX ix_cs")
print("=== NO index, FULL data (EXISTS not run: it rescans 200,000 rows per customer)")
for name in ["IN", "JOIN+DISTINCT", "JOIN+GROUP BY"]:
    s, r = run(con, forms[name])
    print(f"{name:14s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, forms[name])}")
    assert sorted(r) == ref

# pandas
cu = pd.read_sql("SELECT * FROM customers", con)
od = pd.read_sql("SELECT * FROM orders", con)
placed = od[od.status == "placed"]
via_isin = cu[cu.customer_id.isin(placed.customer_id)]
via_merge = cu.merge(placed[["customer_id"]], on="customer_id")
via_dedup = via_merge.drop_duplicates()
print("\npandas merge rows (duplicates):", len(via_merge), "| isin rows:", len(via_isin), "| merge + drop_duplicates:", len(via_dedup))
b = pd.DataFrame(ref, columns=["customer_id", "name"])
pd.testing.assert_frame_equal(via_isin.sort_values("customer_id")[["customer_id", "name"]].reset_index(drop=True), b, check_dtype=False)
pd.testing.assert_frame_equal(via_dedup.sort_values("customer_id")[["customer_id", "name"]].reset_index(drop=True), b, check_dtype=False)
print("asserts passed: all SQL forms, pandas isin and merge+drop_duplicates equal after sorting by customer_id; rows =", len(b))
