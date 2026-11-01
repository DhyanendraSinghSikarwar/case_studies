# Q29: diagnose a slow dashboard query step by step (SQLite 3.x via sqlite3; VM steps via progress handler).
import sqlite3, time
import numpy as np
import pandas as pd

rng = np.random.default_rng(29)
N_ORD, N_CUS, N_ITM = 300_000, 20_000, 900_000
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, segment TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount REAL);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER, price REAL);
""")
cities = [f"City_{i:02d}" for i in range(40)]
cust = pd.DataFrame({"customer_id": np.arange(1, N_CUS + 1),
                     "name": [f"cust_{i}" for i in range(1, N_CUS + 1)],
                     "city": np.array(cities)[rng.integers(0, 40, N_CUS)],
                     "segment": np.array(["retail", "smb", "corp"])[rng.integers(0, 3, N_CUS)]})
days = pd.Timestamp("2024-11-01") + pd.to_timedelta(rng.integers(0, 730, N_ORD), unit="D")   # to 2026-10-31
orders = pd.DataFrame({"order_id": np.arange(1, N_ORD + 1),
                       "customer_id": rng.integers(1, N_CUS + 1, N_ORD),
                       "order_date": days.strftime("%Y-%m-%d"),
                       "status": np.array(["delivered", "placed", "cancelled", "returned"])[
                           rng.choice(4, N_ORD, p=[0.6, 0.2, 0.1, 0.1])],
                       "amount": rng.integers(500, 20000, N_ORD) / 100})
items = pd.DataFrame({"item_id": np.arange(1, N_ITM + 1), "order_id": rng.integers(1, N_ORD + 1, N_ITM),
                      "product_id": rng.integers(1, 500, N_ITM), "qty": rng.integers(1, 5, N_ITM),
                      "price": rng.integers(100, 5000, N_ITM) / 100})
for name, d in (("customers", cust), ("orders", orders), ("order_items", items)):
    con.executemany(f"INSERT INTO {name} VALUES ({','.join('?' * d.shape[1])})", d.itertuples(index=False, name=None))
con.commit()
print("rows:", [con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("orders", "customers", "order_items")])

CUT = "2026-05-01"   # 'last 6 months' anchored at a fixed date so the run is repeatable (data ends 2026-10-31)

def steps_and_rows(sql):
    cnt = [0]
    def cb():
        cnt[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return cnt[0], rows

def seconds(sql):
    t = time.perf_counter(); con.execute(sql).fetchall(); return time.perf_counter() - t

def plan(sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

TAIL = """
SELECT cm.city, cm.month, cm.revenue, cm.customers FROM cm
WHERE cm.city IN (SELECT city FROM cm GROUP BY city ORDER BY SUM(revenue) DESC LIMIT 10)
ORDER BY cm.city, cm.month"""

S0 = f"""/* S0 baseline */
WITH cm AS (
 SELECT c.city AS city, strftime('%Y-%m', o.order_date) AS month,
        SUM(o.amount) AS revenue, COUNT(DISTINCT o.customer_id) AS customers
 FROM orders o JOIN customers c ON c.customer_id = o.customer_id
               JOIN order_items i ON i.order_id = o.order_id
 WHERE o.status = 'delivered' AND strftime('%Y-%m', o.order_date) >= '2026-05'
 GROUP BY c.city, strftime('%Y-%m', o.order_date)){TAIL}"""
S1 = S0.replace("S0 baseline", "S1 sargable date").replace("strftime('%Y-%m', o.order_date) >= '2026-05'", f"o.order_date >= '{CUT}'")
S2 = S1.replace("S1 sargable date", "S2 after index on order_items(order_id)")
S3 = S2.replace("S2 after index on order_items(order_id)", "S3 drop the unused order_items join").replace(
    "\n               JOIN order_items i ON i.order_id = o.order_id", "")
S4_wide = f"""/* S4a wide SELECT inside a CTE */
WITH j AS (SELECT o.*, c.name, c.city, c.segment FROM orders o JOIN customers c ON c.customer_id = o.customer_id),
cm AS (
 SELECT city, strftime('%Y-%m', order_date) AS month, SUM(amount) AS revenue, COUNT(DISTINCT customer_id) AS customers
 FROM j WHERE status = 'delivered' AND order_date >= '{CUT}'
 GROUP BY city, strftime('%Y-%m', order_date)){TAIL}"""
S5 = S3.replace("S3 drop the unused order_items join", "S5 covering index on orders")
S6 = f"""/* S6 pre-aggregate per customer and month, then join customers */
WITH pc AS (
 SELECT customer_id, substr(order_date, 1, 7) AS month, SUM(amount) AS revenue
 FROM orders WHERE status = 'delivered' AND order_date >= '{CUT}'
 GROUP BY customer_id, substr(order_date, 1, 7)),
cm AS (
 SELECT c.city AS city, pc.month AS month, SUM(pc.revenue) AS revenue, COUNT(*) AS customers
 FROM pc JOIN customers c ON c.customer_id = pc.customer_id
 GROUP BY c.city, pc.month){TAIL}"""

def run(tag, sql, note=""):
    st, rows = steps_and_rows(sql)
    sec = seconds(sql)
    print(f"\n== {tag} {note}\nVM steps: {st:,}   seconds (machine-specific, one run): {sec:.2f}   rows returned: {len(rows)}")
    for p in plan(sql): print("   plan:", p)
    return st, rows

res = {}
res["S0"] = run("S0 baseline: strftime on date, no FK index, fan-out join, COUNT(DISTINCT)", S0)
res["S1"] = run("S1 sargable date predicate (order_date >= literal)", S1)
con.execute("CREATE INDEX ix_items_order ON order_items(order_id)")
res["S2"] = run("S2 + index on order_items(order_id)", S2)
res["S3"] = run("S3 drop the unused order_items join (removes the fan-out)", S3)
res["S4a"] = run("S4a wide SELECT o.*, c.* inside a CTE, otherwise S3", S4_wide)
con.execute("CREATE INDEX ix_ord_cov ON orders(status, order_date, customer_id, amount)")
res["S5"] = run("S5 + covering index orders(status, order_date, customer_id, amount)", S5)
res["S6"] = run("S6 pre-aggregate by customer and month, then join customers", S6)

# correctness: pandas on the same data
o = orders[(orders.status == "delivered") & (orders.order_date >= CUT)].merge(cust[["customer_id", "city"]], on="customer_id")
o["month"] = o["order_date"].str[:7]
cm = o.groupby(["city", "month"]).agg(revenue=("amount", "sum"), customers=("customer_id", "nunique")).reset_index()
top = cm.groupby("city")["revenue"].sum().nlargest(10).index
exp = cm[cm.city.isin(top)].sort_values(["city", "month"]).reset_index(drop=True)
exp["revenue"] = exp["revenue"].round(2)
print("\npandas expected rows:", len(exp), "| top-10 cities:", sorted(top))
print(exp.head(4).to_string(index=False))

def frame(rows):
    f = pd.DataFrame(rows, columns=["city", "month", "revenue", "customers"])
    f["revenue"] = f["revenue"].round(2)
    return f.sort_values(["city", "month"]).reset_index(drop=True)

for k in ("S3", "S4a", "S5", "S6"):
    pd.testing.assert_frame_equal(frame(res[k][1]), exp, check_dtype=False)
print("S3, S4a, S5, S6 equal pandas (compared after sorting by city, month)")
w, g = frame(res["S0"][1]), exp
print("S0 (fan-out) top-10 city set equals pandas?", set(w.city) == set(g.city),
      "| revenue equal?", bool(np.allclose(w.revenue.values, g.revenue.values)) if len(w) == len(g) else "row counts differ")
m = w.merge(g, on=["city", "month"], suffixes=("_s0", "_ok"))
print("   inflation of revenue in S0 (first rows):", (m.revenue_s0 / m.revenue_ok).round(2).head(4).tolist())
print("   S0 customers column equal on the shared city-months?", bool((m.customers_s0 == m.customers_ok).all()),
      "| orders with no items (dropped by the inner join):", int(len(set(orders.order_id) - set(items.order_id))))
print("orders delivered in the window:", len(o), "| items per order mean: %.2f" % (N_ITM / N_ORD))
print("\nsteps summary:", {k: v[0] for k, v in res.items()})

# the hand-checkable mini example (3 orders), same two shapes of query
m = sqlite3.connect(":memory:")
m.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount REAL);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER);
INSERT INTO customers VALUES (1,'Pune'),(2,'Pune');
INSERT INTO orders VALUES (1,1,'2026-06-10','delivered',100),(2,1,'2026-06-20','delivered',50),(3,2,'2026-03-01','delivered',70),(4,2,'2026-06-25','placed',999);
INSERT INTO order_items VALUES (1,1,1),(2,1,1),(3,1,2),(4,2,1),(5,3,1),(6,3,1);
""")
fan = m.execute("SELECT c.city, SUM(o.amount), COUNT(DISTINCT o.customer_id) FROM orders o JOIN customers c ON c.customer_id=o.customer_id "
                "JOIN order_items i ON i.order_id=o.order_id WHERE o.status='delivered' AND o.order_date >= '2026-05-01' GROUP BY c.city").fetchall()
ok = m.execute("SELECT c.city, SUM(o.amount), COUNT(DISTINCT o.customer_id) FROM orders o JOIN customers c ON c.customer_id=o.customer_id "
               "WHERE o.status='delivered' AND o.order_date >= '2026-05-01' GROUP BY c.city").fetchall()
print("\nmini example: with the order_items join", fan, "| without it", ok)
assert fan == [("Pune", 350.0, 1)] and ok == [("Pune", 150.0, 1)]
print("\nrecommended query (S5), exactly as run:\n" + S5)
