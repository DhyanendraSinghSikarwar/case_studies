# Q4: composite index ix(customer_id, status, order_date) and the leftmost-prefix rule
import os, sqlite3, tempfile
import numpy as np
import pandas as pd

rng = np.random.default_rng(4)
N = 200_000
orders = pd.DataFrame({
    "order_id": np.arange(1, N + 1),
    "customer_id": rng.integers(1, 20_001, N),
    "status": rng.choice(["placed", "shipped", "delivered", "cancelled"], N, p=[.2, .3, .4, .1]),
    "order_date": (pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 365, N), unit="D")).strftime("%Y-%m-%d").to_numpy(),
    "amount": rng.integers(100, 50_000, N) / 100,
})
path = os.path.join(tempfile.mkdtemp(), "q4.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders.itertuples(index=False, name=None))
con.execute("CREATE INDEX ix ON orders(customer_id, status, order_date)")
con.commit(); con.close()
print("sqlite", sqlite3.sqlite_version)

def plan(sql, db=path):
    c = sqlite3.connect(db)             # fresh connection per plan
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql)]
    finally:
        c.close()

o = orders
CASES = [
 ("1 customer_id=7",                      "customer_id = 7",
  lambda: o.customer_id == 7),
 ("2 customer_id=7 AND status",           "customer_id = 7 AND status = 'shipped'",
  lambda: (o.customer_id == 7) & (o.status == "shipped")),
 ("3 status alone",                       "status = 'shipped'",
  lambda: o.status == "shipped"),
 ("4 order_date range alone",             "order_date >= '2024-06-01' AND order_date < '2024-07-01'",
  lambda: (o.order_date >= "2024-06-01") & (o.order_date < "2024-07-01")),
 ("5 customer_id=7 AND order_date>",      "customer_id = 7 AND order_date > '2024-06-01'",
  lambda: (o.customer_id == 7) & (o.order_date > "2024-06-01")),
 ("6 customer_id>15000 AND status",       "customer_id > 15000 AND status = 'shipped'",
  lambda: (o.customer_id > 15000) & (o.status == "shipped")),
 ("7 cust=7, status IN, date>",           "customer_id = 7 AND status IN ('shipped','placed') AND order_date > '2024-06-01'",
  lambda: (o.customer_id == 7) & o.status.isin(["shipped", "placed"]) & (o.order_date > "2024-06-01")),
 ("8 cust=7, status, date range",         "customer_id = 7 AND status = 'shipped' AND order_date >= '2024-01-01' AND order_date < '2024-09-01'",
  lambda: (o.customer_id == 7) & (o.status == "shipped") & (o.order_date >= "2024-01-01") & (o.order_date < "2024-09-01")),
]
con = sqlite3.connect(path)
print("\nquery: SELECT order_id, amount FROM orders WHERE <predicate>   (amount is not in the index)")
for label, pred, mask in CASES:
    sql = f"SELECT order_id, amount FROM orders WHERE {pred}"
    p = plan(sql)
    got = sorted(r[0] for r in con.execute(sql))
    assert got == o[mask()].order_id.tolist()
    print(f"{label:34s} {p[0]}   [{len(got)} rows]")
# ORDER BY only
for label, ob, expect in [("ORDER BY customer_id, status, order_date", "customer_id, status, order_date", "USING INDEX ix"),
                          ("ORDER BY customer_id", "customer_id", "USING INDEX ix"),
                          ("ORDER BY status", "status", "TEMP B-TREE"),
                          ("ORDER BY status, order_date", "status, order_date", "TEMP B-TREE")]:
    p = plan(f"SELECT order_id, amount FROM orders ORDER BY {ob}")
    print(f"{label:34s} {' | '.join(p)}")
    assert any(expect in l for l in p)
con.close()

# assertions on plan text
assert "(customer_id=?)" in plan("SELECT order_id, amount FROM orders WHERE customer_id = 7 AND order_date > '2024-06-01'")[0]
assert "(customer_id=? AND status=?)" in plan("SELECT order_id, amount FROM orders WHERE customer_id = 7 AND status = 'shipped'")[0]
assert plan("SELECT order_id, amount FROM orders WHERE status = 'shipped'") == ["SCAN orders"]

# skip-scan: a separate table whose leading column has two values
sp = os.path.join(tempfile.mkdtemp(), "skip.db")
c = sqlite3.connect(sp)
c.execute("CREATE TABLE ev(id INTEGER PRIMARY KEY, kind TEXT, ts INT, pad TEXT)")
rows = [(i, "A" if i % 2 else "B", int(t), "x") for i, t in enumerate(rng.integers(0, 1_000_000, 100_000), 1)]
c.executemany("INSERT INTO ev VALUES (?,?,?,?)", rows)
c.execute("CREATE INDEX ix_ev ON ev(kind, ts)")
c.commit(); c.close()
Q = "SELECT id, pad FROM ev WHERE ts = 777"
before = plan(Q, sp)[0]
c = sqlite3.connect(sp); c.execute("ANALYZE"); c.commit()
stat = c.execute("SELECT idx, stat FROM sqlite_stat1").fetchall(); c.close()
after = plan(Q, sp)[0]
print("\nskip-scan table ev(kind has 2 values), index (kind, ts), query WHERE ts = 777")
print("  before ANALYZE:", before)
print("  sqlite_stat1  :", stat)
print("  after  ANALYZE:", after)
assert before == "SCAN ev" and "ANY(kind)" in after
c = sqlite3.connect(sp)
got = sorted(r[0] for r in c.execute(Q))
df = pd.DataFrame(rows, columns=["id", "kind", "ts", "pad"])
assert got == df[df.ts == 777].id.tolist()
c.close()

# and on orders: ANALYZE does not make status-alone skip-scannable, the leading column has ~20,000 values
c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit()
stat = c.execute("SELECT idx, stat FROM sqlite_stat1").fetchall(); c.close()
p = plan("SELECT order_id, amount FROM orders WHERE status = 'shipped'")
print("\norders after ANALYZE, stat1:", stat)
print("  status alone:", p[0])
assert p == ["SCAN orders"]
