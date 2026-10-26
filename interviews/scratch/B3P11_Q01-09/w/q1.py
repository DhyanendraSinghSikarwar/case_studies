# Q1: reading EXPLAIN QUERY PLAN on SQLite (fresh connection for every plan)
import os, sqlite3, tempfile
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
N, C = 200_000, 20_000
orders = pd.DataFrame({
    "order_id": np.arange(1, N + 1),
    "customer_id": rng.integers(1, C + 1, N),
    "order_date": (pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 365, N), unit="D")).strftime("%Y-%m-%d").to_numpy(),
    "status": rng.choice(["placed", "shipped", "delivered", "cancelled"], N, p=[.2, .3, .4, .1]),
    "amount": rng.integers(100, 50_000, N) / 100,
})
cities = np.array(["Pune", "Mumbai", "Delhi", "Chennai", "Kolkata"])
customers = pd.DataFrame({"customer_id": np.arange(1, C + 1),
                          "name": [f"cust{i}" for i in range(1, C + 1)],
                          "city": cities[rng.integers(0, 5, C)]})

path = os.path.join(tempfile.mkdtemp(), "q1.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL)")
con.execute("CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", orders.itertuples(index=False, name=None))
con.executemany("INSERT INTO customers VALUES (?,?,?)", customers.itertuples(index=False, name=None))
con.commit(); con.close()
print("sqlite", sqlite3.sqlite_version, "pandas", pd.__version__)

def plan(sql):
    """Fresh connection each time: Python's statement cache can return a stale plan after CREATE/DROP INDEX."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql)]
    finally:
        c.close()

def show(title, sql):
    p = plan(sql)
    print(f"\n{title}\n  {sql}")
    for line in p:
        print("   ", line)
    return p

Q_LOOK = "SELECT * FROM orders WHERE customer_id = 5"
Q_COVER = "SELECT customer_id, order_id FROM orders WHERE customer_id = 5"
Q_ORDER = "SELECT * FROM orders ORDER BY amount"
Q_DIST = "SELECT DISTINCT status FROM orders"
Q_GROUP = "SELECT status, COUNT(*) AS n FROM orders GROUP BY status"

p_before = show("A) lookup, no index", Q_LOOK)
assert p_before == ["SCAN orders"]
c = sqlite3.connect(path); c.execute("CREATE INDEX ix_cust ON orders(customer_id)"); c.commit(); c.close()
p_after = show("B) lookup, after CREATE INDEX ix_cust", Q_LOOK)
assert any("SEARCH orders USING INDEX ix_cust (customer_id=?)" in l for l in p_after)
p_cov = show("C) covering select", Q_COVER)
assert any("USING COVERING INDEX ix_cust" in l for l in p_cov)
p_ord = show("D) ORDER BY amount (no index on amount)", Q_ORDER)
assert any("USE TEMP B-TREE FOR ORDER BY" in l for l in p_ord)
p_dis = show("E) DISTINCT status", Q_DIST)
assert any("USE TEMP B-TREE FOR DISTINCT" in l for l in p_dis)
p_grp = show("F) GROUP BY status", Q_GROUP)
assert any("USE TEMP B-TREE FOR GROUP BY" in l for l in p_grp)

# results: SQL versus pandas (compared after sorting by order_id / status)
con = sqlite3.connect(path)
sql_look = pd.read_sql_query(Q_LOOK + " ORDER BY order_id", con)
# pd:main
pd_look = orders[orders["customer_id"] == 5].sort_values("order_id").reset_index(drop=True)
pd_dist = sorted(orders["status"].unique())
pd_group = orders.groupby("status").size().rename("n").reset_index().sort_values("status").reset_index(drop=True)
# pd:end
pd.testing.assert_frame_equal(sql_look, pd_look, check_dtype=False)
assert sorted(r[0] for r in con.execute(Q_DIST)) == pd_dist
sql_group = pd.read_sql_query(Q_GROUP + " ORDER BY status", con)
pd.testing.assert_frame_equal(sql_group, pd_group, check_dtype=False)
print("\ncustomer 5 has", len(sql_look), "orders; statuses:", pd_dist)
print(sql_group.to_string(index=False))
print("SQL and pandas agree (lookup sorted by order_id, groups sorted by status)")
con.close()
