# Q40: 1,000 rows became 1,400 after a join: diagnose with COUNT(*) vs COUNT(DISTINCT), duplicated keys, isolation, guards
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE customer_dim(customer_id INTEGER, segment TEXT, valid_from TEXT, is_current INTEGER);
""")
# 1,000 orders, 10 per customer for customers 1..100
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i - 1) % 100 + 1, 10) for i in range(1, 1001)])
dim = []
for c in range(1, 101):
    if c <= 40:                                        # the bug: two 'current' rows for customers 1..40
        dim += [(c, "gold", "2025-01-01", 1), (c, "silver", "2025-06-01", 1)]
    elif c <= 60:                                      # normal history: one old row (not current) + one current
        dim += [(c, "bronze", "2024-01-01", 0), (c, "gold", "2025-01-01", 1)]
    else:
        dim.append((c, "gold", "2025-01-01", 1))
con.executemany("INSERT INTO customer_dim VALUES (?,?,?,?)", dim)

one = lambda q: con.execute(q).fetchone()
print("1. grain of orders: COUNT(*), COUNT(DISTINCT order_id) =", one("SELECT COUNT(*), COUNT(DISTINCT order_id) FROM orders"))

SQL_BAD = """
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o JOIN customer_dim d ON d.customer_id = o.customer_id AND d.is_current = 1
"""
print("2. after the join: COUNT(*), COUNT(DISTINCT order_id), SUM(amount) =",
      one(f"SELECT COUNT(*), COUNT(DISTINCT order_id), SUM(amount) FROM ({SQL_BAD})"), "(true SUM was 10000)")

SQL_DUPKEYS = """
SELECT customer_id, COUNT(*) AS n FROM customer_dim WHERE is_current = 1
GROUP BY customer_id HAVING COUNT(*) > 1 ORDER BY customer_id
"""
dups = con.execute(SQL_DUPKEYS).fetchall()
print("3. duplicated current keys:", len(dups), "keys, first three:", dups[:3])
print("   expected extra rows = SUM(n - 1) x orders per key =", sum(n - 1 for _, n in dups), "x 10 =",
      sum(n - 1 for _, n in dups) * 10)
print("4. isolate one key:", con.execute("SELECT * FROM customer_dim WHERE customer_id = 1").fetchall())

# fix in the query: pick the latest current row per key
SQL_FIX = """
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o
JOIN customer_dim d
  ON d.customer_id = o.customer_id AND d.is_current = 1
 AND d.valid_from = (SELECT MAX(d2.valid_from) FROM customer_dim d2
                     WHERE d2.customer_id = d.customer_id AND d2.is_current = 1)
ORDER BY o.order_id
"""
fixed = pd.read_sql_query(SQL_FIX, con)
print("5. fixed join rows:", len(fixed), "| SUM(amount):", fixed["amount"].sum())

# pandas: same diagnosis and fix
orders = pd.read_sql_query("SELECT * FROM orders", con)
cdim = pd.read_sql_query("SELECT * FROM customer_dim", con)
cur = cdim[cdim["is_current"] == 1]
try:
    orders.merge(cur, on="customer_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("\npandas validate='many_to_one' ->", type(e).__name__ + ":", e)
print("pandas duplicated current keys:", int(cur["customer_id"].duplicated().sum()))
bad = orders.merge(cur, on="customer_id")
print("pandas unvalidated merge rows:", len(bad), "| sum amount:", bad["amount"].sum())
latest = cur.sort_values("valid_from").drop_duplicates("customer_id", keep="last")
p_fixed = (orders.merge(latest[["customer_id", "segment"]], on="customer_id", how="inner", validate="many_to_one")
           .sort_values("order_id").reset_index(drop=True))
pd.testing.assert_frame_equal(fixed[["order_id", "customer_id", "amount", "segment"]], p_fixed, check_dtype=False)
assert len(p_fixed) == len(orders) == 1000
print("asserts passed: SQL fix == pandas fix (sorted by order_id), row count 1000 == orders")

# guard at the source: a partial unique index makes the duplicate load fail
con.execute("DELETE FROM customer_dim WHERE customer_id <= 40 AND valid_from = '2025-01-01'")
con.execute("CREATE UNIQUE INDEX one_current ON customer_dim(customer_id) WHERE is_current = 1")
try:
    con.execute("INSERT INTO customer_dim VALUES (1, 'gold', '2026-01-01', 1)")
except sqlite3.IntegrityError as e:
    print("\nunique partial index ->", type(e).__name__ + ":", e)
con.close()
