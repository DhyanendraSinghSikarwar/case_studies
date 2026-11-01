# Q22: best-selling product per category per month, all products on ties.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'books'),(2,'books'),(3,'books'),(4,'toys'),(5,'toys'),(6,'toys');
INSERT INTO orders VALUES (1,'2025-01-05'),(2,'2025-01-20'),(3,'2025-02-03'),(4,'2025-02-18'),(5,'2025-03-02');
INSERT INTO order_items VALUES
 (1,1,3),(1,2,2),(1,4,1),
 (2,1,1),(2,2,2),(2,5,4),
 (3,3,5),(3,4,2),(3,5,2),
 (4,6,1),(4,4,0),
 (5,1,9);
"""
SQL = """
WITH units AS (
  SELECT p.category, substr(o.order_date, 1, 7) AS month, p.product_id, SUM(oi.qty) AS units
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id
  JOIN products p ON p.product_id = oi.product_id
  WHERE o.order_date >= '2025-01-01' AND o.order_date < '2025-03-01'
  GROUP BY p.category, substr(o.order_date, 1, 7), p.product_id
),
ranked AS (
  SELECT *, RANK() OVER (PARTITION BY category, month ORDER BY units DESC) AS rnk
  FROM units
)
SELECT category, month, product_id, units
FROM ranked
WHERE rnk = 1
ORDER BY category, month, product_id
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

oi = pd.read_sql("SELECT * FROM order_items", con)
o = pd.read_sql("SELECT * FROM orders", con)
pr = pd.read_sql("SELECT * FROM products", con)
# PANDAS START
d = oi.merge(o, on="order_id").merge(pr, on="product_id")
d = d[(d["order_date"] >= "2025-01-01") & (d["order_date"] < "2025-03-01")].copy()
d["month"] = d["order_date"].str[:7]
u = d.groupby(["category", "month", "product_id"], as_index=False)["qty"].sum().rename(columns={"qty": "units"})
u["rnk"] = u.groupby(["category", "month"])["units"].rank(method="min", ascending=False)
p = (u[u["rnk"] == 1][["category", "month", "product_id", "units"]]
     .sort_values(["category", "month", "product_id"]).reset_index(drop=True))
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (compared after sorting by category, month, product_id)")

# row_number would keep one of the tied products
rn = pd.read_sql(SQL.replace("RANK()", "ROW_NUMBER()"), con)
print("with ROW_NUMBER instead of RANK:", len(rn), "rows vs", len(s), "with RANK")
