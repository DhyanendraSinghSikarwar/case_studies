# Q29: diagnose a slow dashboard query: baseline, read the plan, change one thing, re-measure VM steps, re-check results
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(29)
N_C, N_O, N_I = 20_000, 300_000, 900_000
cities = [f"City{i:02d}" for i in range(40)]
cust = pd.DataFrame({"customer_id": np.arange(1, N_C + 1),
                     "name": [f"cust{i}" for i in range(1, N_C + 1)],
                     "city": rng.choice(cities, N_C),
                     "segment": rng.choice(["retail", "smb", "corp"], N_C)})
days = pd.date_range("2024-01-01", "2025-06-30").strftime("%Y-%m-%d").to_numpy()
orders = pd.DataFrame({"order_id": np.arange(1, N_O + 1),
                       "customer_id": rng.integers(1, N_C + 1, N_O),
                       "order_date": rng.choice(days, N_O),
                       "status": rng.choice(["placed", "shipped", "delivered", "returned"], N_O, p=[.1, .15, .6, .15])})
item_order = np.concatenate([np.arange(1, N_O + 1), rng.integers(1, N_O + 1, N_I - N_O)])
items = pd.DataFrame({"item_id": np.arange(1, N_I + 1), "order_id": item_order,
                      "product_id": rng.integers(1, 5001, N_I),
                      "qty": rng.integers(1, 6, N_I), "price": rng.integers(1, 501, N_I)})
items["line"] = items["qty"] * items["price"]
orders["amount"] = orders["order_id"].map(items.groupby("order_id")["line"].sum()).astype("int64")

def build(indexes=()):
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, segment TEXT);
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
    CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER, price INTEGER);
    """)
    con.executemany("INSERT INTO customers VALUES (?,?,?,?)", cust.itertuples(index=False, name=None))
    con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders.itertuples(index=False, name=None))
    con.executemany("INSERT INTO order_items VALUES (?,?,?,?,?)", items[["item_id","order_id","product_id","qty","price"]].itertuples(index=False, name=None))
    for ddl in indexes:
        con.execute(ddl)
    con.commit()
    return con

def steps(con, sql):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql).fetchall()
    con.set_progress_handler(None, 1)
    return rows, n[0]

def plan(con, sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

# the six-month window is 2025-01-01 .. 2025-06-30; top 10 (city, month) rows by revenue, ties broken by city, month
S0 = """
SELECT c.city, strftime('%Y-%m', o.order_date) AS month,
       SUM(o.amount) AS revenue, COUNT(DISTINCT o.customer_id) AS customers
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items i ON i.order_id = o.order_id
WHERE o.status = 'delivered' AND strftime('%Y-%m', o.order_date) >= '2025-01'
GROUP BY c.city, month
ORDER BY revenue DESC, c.city, month
LIMIT 10
"""
S1 = S0.replace("strftime('%Y-%m', o.order_date) >= '2025-01'", "o.order_date >= '2025-01-01' AND o.order_date < '2025-07-01'")
S3 = """
SELECT c.city, strftime('%Y-%m', o.order_date) AS month,
       SUM(o.amount) AS revenue, COUNT(DISTINCT o.customer_id) AS customers
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'delivered' AND o.order_date >= '2025-01-01' AND o.order_date < '2025-07-01'
GROUP BY c.city, month
ORDER BY revenue DESC, c.city, month
LIMIT 10
"""
S5 = """
SELECT c.city, m.month, SUM(m.revenue) AS revenue, COUNT(*) AS customers
FROM (SELECT customer_id, substr(order_date, 1, 7) AS month, SUM(amount) AS revenue
      FROM orders
      WHERE status = 'delivered' AND order_date >= '2025-01-01' AND order_date < '2025-07-01'
      GROUP BY customer_id, month) m
JOIN customers c ON c.customer_id = m.customer_id
GROUP BY c.city, m.month
ORDER BY revenue DESC, c.city, m.month
LIMIT 10
"""
S3W = """
SELECT w.city, strftime('%Y-%m', w.order_date) AS month,
       SUM(w.amount) AS revenue, COUNT(DISTINCT w.customer_id) AS customers
FROM (SELECT o.*, c.name, c.segment, c.city
      FROM orders o JOIN customers c ON c.customer_id = o.customer_id) w
WHERE w.status = 'delivered' AND w.order_date >= '2025-01-01' AND w.order_date < '2025-07-01'
GROUP BY w.city, month
ORDER BY revenue DESC, w.city, month
LIMIT 10
"""
IX_FK = ["CREATE INDEX ix_items_order ON order_items(order_id)", "CREATE INDEX ix_orders_cust ON orders(customer_id)"]
IX_COV = ["CREATE INDEX ix_orders_sd ON orders(status, order_date, customer_id, amount)"]

# pandas reference: the correct answer, and the fan-out inflated one the baseline computes
o = orders[(orders.status == "delivered") & (orders.order_date >= "2025-01-01") & (orders.order_date < "2025-07-01")].copy()
o["month"] = o["order_date"].str[:7]
o = o.merge(cust[["customer_id", "city"]], on="customer_id")
def top10(frame):
    g = frame.groupby(["city", "month"]).agg(revenue=("amount", "sum"), customers=("customer_id", "nunique")).reset_index()
    return g.sort_values(["revenue", "city", "month"], ascending=[False, True, True]).head(10).reset_index(drop=True)
good = top10(o)
n_items = items.groupby("order_id").size()
oi = o.loc[o.index.repeat(o["order_id"].map(n_items))]          # one row per order item: the fan-out
inflated = top10(oi)

def check(rows, expect):
    got = pd.DataFrame(rows, columns=["city", "month", "revenue", "customers"])
    pd.testing.assert_frame_equal(got, expect, check_dtype=False)

results = []
def run(label, sql, indexes, expect, show_plan=True):
    con = build(indexes)
    rows, n = steps(con, sql)                      # fresh connection per step: no stale cached plan
    check(rows, expect)
    results.append((label, n, rows[0]))
    print(f"\n== {label}\nVM steps: {n:,}   top row: {rows[0]}")
    if show_plan:
        for p in plan(con, sql):
            print("   plan:", p)
    con.close()

print("rows:", len(cust), len(orders), len(items), "| pandas correct top row:", tuple(good.iloc[0].tolist()), "| inflated top row:", tuple(inflated.iloc[0].tolist()))
run("0 baseline (primary keys only)", S0, [], inflated)
run("1 sargable date range instead of strftime on the column", S1, [], inflated)
run("2 add FK indexes order_items(order_id), orders(customer_id)", S1, IX_FK, inflated)
run("3 drop the order_items join (fan-out), still FK indexes", S3, IX_FK, good)
run("3b same as 3 but the join selects o.*, c.name, c.segment through a derived table", S3W, IX_FK, good)
run("4 covering index orders(status, order_date, customer_id, amount)", S3, IX_FK + IX_COV, good)
run("5 pre-aggregate per customer and month, then join customers", S5, IX_FK + IX_COV, good)
base = results[0][1]
print("\nsummary (VM steps, ratio to baseline):")
for label, n, _ in results:
    print(f"  {n:>12,}  {n/base:7.4f}  {label}")
