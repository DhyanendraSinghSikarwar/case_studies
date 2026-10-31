# Q33: three real SQLite plans (nested loop + index, automatic index / bloom filter, co-routine / materialize)
# and the rollback pattern for statements that execute.
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(33)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE a(x INTEGER, k INTEGER);
CREATE TABLE b(y INTEGER, k INTEGER);
""")
cust = pd.DataFrame({"customer_id": range(1, 2001), "name": [f"c{i}" for i in range(1, 2001)],
                     "city": np.array(["Pune", "Delhi", "Chennai", "Kolkata"])[rng.integers(0, 4, 2000)]})
orders = pd.DataFrame({"order_id": range(1, 20001), "customer_id": rng.integers(1, 2001, 20000),
                       "amount": rng.integers(10, 500, 20000)})
A = pd.DataFrame({"x": range(3000), "k": rng.integers(0, 500, 3000)})
B = pd.DataFrame({"y": range(3000), "k": rng.integers(0, 500, 3000)})
for nm, d in (("customers", cust), ("orders", orders), ("a", A), ("b", B)):
    con.executemany(f"INSERT INTO {nm} VALUES ({','.join('?' * d.shape[1])})", d.itertuples(index=False, name=None))
con.execute("CREATE INDEX ix_o_cust ON orders(customer_id)")

def plan(sql): return [(r[3]) for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

q1 = "SELECT c.name, o.amount FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'"
q2 = "SELECT COUNT(*) FROM a JOIN b ON b.k = a.k"
q3 = ("WITH t AS (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) "
      "SELECT t1.customer_id, t1.s FROM t t1 WHERE t1.s > (SELECT AVG(s) FROM t) ORDER BY t1.customer_id")

print("Plan 1: nested loop with an index probe on the inner table")
for p in plan(q1): print("   ", p)
print("Plan 2: no index on either side -> automatic index (before ANALYZE)")
for p in plan(q2): print("   ", p)
con.execute("ANALYZE")
print("Plan 2 after ANALYZE (a new statement text is used so no cached plan is reused):")
for p in plan(q2 + " /* after analyze */"): print("   ", p)
print("Plan 3: a CTE used twice -> MATERIALIZE plus a scalar subquery")
for p in plan(q3): print("   ", p)

q4 = "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE s > 6000"
print("Plan 4: a grouped subquery used once -> co-routine instead of materialising")
for p in plan(q4): print("   ", p)
assert len(con.execute(q4).fetchall()) == int((orders.groupby("customer_id")["amount"].sum() > 6000).sum())

# results equal pandas
r1 = pd.read_sql(q1, con).sort_values(["name", "amount"]).reset_index(drop=True)
e1 = cust[cust.city == "Pune"].merge(orders, on="customer_id")[["name", "amount"]].sort_values(["name", "amount"]).reset_index(drop=True)
pd.testing.assert_frame_equal(r1, e1, check_dtype=False)
n2 = con.execute(q2).fetchone()[0]
assert n2 == len(A.merge(B, on="k"))
r3 = pd.read_sql(q3, con)
t = orders.groupby("customer_id")["amount"].sum()
e3 = t[t > t.mean()].reset_index().rename(columns={"amount": "s"}).sort_values("customer_id").reset_index(drop=True)
pd.testing.assert_frame_equal(r3, e3, check_dtype=False)
print(f"\nrows: plan1 {len(r1)}, plan2 count {n2}, plan3 {len(r3)}; all equal to pandas merge/groupby (sorted by name, amount / customer_id)")

con.commit()
# EXPLAIN in SQLite does not execute; the rollback pattern for statements that do
before = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
con.execute("EXPLAIN QUERY PLAN DELETE FROM orders WHERE amount < 100").fetchall()
mid = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
con.execute("BEGIN"); con.execute("DELETE FROM orders WHERE amount < 100")
inside = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
con.execute("ROLLBACK")
after = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print("orders rows: before", before, "| after EXPLAIN QUERY PLAN DELETE", mid, "| inside BEGIN..DELETE", inside, "| after ROLLBACK", after)
print("SQLite version:", sqlite3.sqlite_version)
