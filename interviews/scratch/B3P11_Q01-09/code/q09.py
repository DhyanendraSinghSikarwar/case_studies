# Q9: NOT IN vs NOT EXISTS vs LEFT JOIN ... IS NULL: plans, VM steps, and the NULL trap.
import random
import sqlite3
import pandas as pd

def build(ncust, nord, active, nulls=0, seed=9):
    random.seed(seed)
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, amount REAL);
    """)
    con.executemany("INSERT INTO customers VALUES (?,?)", [(i, f"c{i}") for i in range(1, ncust + 1)])
    con.executemany("INSERT INTO orders VALUES (?,?,?)",
                    [(i, random.randint(1, active), round(random.uniform(10, 500), 2)) for i in range(1, nord + 1)])
    # a few orders with no customer at all
    for j in range(nulls):
        con.execute("INSERT INTO orders VALUES (?,NULL,1.0)", (nord + 1 + j,))
    con.commit()
    return con

forms = {
 "NOT IN":     "SELECT customer_id, name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)",
 "NOT EXISTS": "SELECT c.customer_id, c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)",
 "LEFT JOIN":  "SELECT c.customer_id, c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id WHERE o.order_id IS NULL",
}
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

def report(con, label, skip=()):
    print(f"=== {label}")
    res = {}
    for name, q in forms.items():
        if name in skip:
            print(f"{name:11s} (not run: too slow at this size)")
            continue
        s, r = run(con, q)
        res[name] = sorted(r)
        print(f"{name:11s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, q)}")
    return res

# 1. no index, small copy 2,000 customers / 20,000 orders (the correlated form is too slow at full size)
small = build(2000, 20000, 1700)
r = report(small, "NO index, SMALL 2,000 customers / 20,000 orders (300 customers without orders)")
assert len({tuple(v) for v in r.values()}) == 1

# 2. full size, with the index
con = build(20000, 200000, 17000)
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
res = report(con, "index ix_cust, FULL 20,000 / 200,000 (3,000 customers without orders)")
ref = res["NOT IN"]
assert all(v == ref for v in res.values())
print("rows (customers with no orders):", len(ref))

# 3. full size, no index: NOT IN and LEFT JOIN only
con.execute("DROP INDEX ix_cust")
res3 = report(con, "NO index, FULL size (NOT EXISTS skipped)", skip=("NOT EXISTS",))
assert all(v == ref for v in res3.values())

# 4. the NULL trap: add 3 orders with customer_id NULL
con.execute("INSERT INTO orders VALUES (900001, NULL, 1.0), (900002, NULL, 1.0), (900003, NULL, 1.0)")
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
print("\n=== after inserting 3 orders with customer_id NULL (index ix_cust present)")
res4 = {}
for name, q in forms.items():
    s, r = run(con, q)
    res4[name] = sorted(r)
    print(f"{name:11s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, q)}")
assert res4["NOT IN"] == [] and res4["NOT EXISTS"] == ref and res4["LEFT JOIN"] == ref
# the NULL-safe version of NOT IN
safe = "SELECT customer_id, name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)"
s, r = run(con, safe)
print(f"{'NOT IN + IS NOT NULL':11s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, safe)}")
assert sorted(r) == ref

# pandas: isin / ~isin behaves like NOT EXISTS, because NaN never matches a customer_id
cu = pd.read_sql("SELECT * FROM customers", con)
od = pd.read_sql("SELECT * FROM orders", con)
print("\npandas orders.customer_id dtype with NULLs:", od.customer_id.dtype)
p_anti = cu[~cu.customer_id.isin(od.customer_id)].sort_values("customer_id")[["customer_id", "name"]].reset_index(drop=True)
m = cu.merge(od[["customer_id", "order_id"]], on="customer_id", how="left", indicator=True)
p_merge = m[m["_merge"] == "left_only"][["customer_id", "name"]].sort_values("customer_id").reset_index(drop=True)
expected = pd.DataFrame(ref, columns=["customer_id", "name"])
pd.testing.assert_frame_equal(p_anti, expected, check_dtype=False)
pd.testing.assert_frame_equal(p_merge, expected, check_dtype=False)
print("pandas ~isin and merge(indicator) return", len(p_anti), "rows with NULLs present (same as NOT EXISTS / LEFT JOIN, not NOT IN)")
print("asserts passed (compared after sorting by customer_id)")
