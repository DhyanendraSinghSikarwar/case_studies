# Q29: top 2 products per category by completed revenue at line-item grain, DENSE_RANK keeps ties
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, status TEXT);
CREATE TABLE order_items(order_id INTEGER, product_id INTEGER, qty INTEGER, unit_price REAL);
INSERT INTO products VALUES
 (1,'Electronics','Phone'),(2,'Electronics','Case'),(3,'Electronics','Cable'),(4,'Electronics','Charger'),
 (5,'Books','Novel'),(6,'Books','Notebook'),(7,NULL,'Gift card'),(8,'Home','Lamp');
INSERT INTO orders VALUES
 (1,1,'2024-03-01','completed'),(2,2,'2024-03-02','completed'),(3,3,'2024-03-03','completed'),
 (4,4,'2024-03-04','cancelled'),(5,5,'2024-03-05','completed');
INSERT INTO order_items VALUES
 (1,1,1,500),(1,2,2,50),
 (2,1,1,500),(2,3,1,100),(2,5,3,20),
 (3,2,2,50),(3,4,1,50),(3,6,5,10),
 (4,4,10,50),
 (5,3,1,100),(5,7,1,30),(5,8,2,40),
 (5,99,1,10);
"""

SQL_MAIN = """
WITH p AS (
  SELECT COALESCE(pr.category, 'Uncategorised') AS category, pr.name,
         SUM(oi.qty) AS units, SUM(oi.qty * oi.unit_price) AS revenue
  FROM order_items oi
  JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
  JOIN products pr ON pr.product_id = oi.product_id
  GROUP BY COALESCE(pr.category, 'Uncategorised'), pr.product_id, pr.name
), r AS (
  SELECT category, name, units, revenue,
         ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) AS share_pct,
         DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
  FROM p
)
SELECT category, name, units, revenue, share_pct, rnk
FROM r
WHERE rnk <= 2
ORDER BY category, rnk, name
"""
# wrong: an order total joined onto every item row
SQL_WRONG = """
WITH ot AS (SELECT order_id, SUM(qty * unit_price) AS order_total FROM order_items GROUP BY order_id)
SELECT pr.name, SUM(ot.order_total) AS wrong_revenue, SUM(oi.qty * oi.unit_price) AS line_revenue
FROM order_items oi
JOIN ot ON ot.order_id = oi.order_id
JOIN orders o ON o.order_id = oi.order_id AND o.status = 'completed'
JOIN products pr ON pr.product_id = oi.product_id
WHERE pr.category = 'Electronics'
GROUP BY pr.product_id, pr.name ORDER BY pr.name
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL:")
print(sql_main.to_string(index=False))
print("SQL wrong (order total on every item row), Electronics:")
print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

products = pd.read_sql_query("SELECT * FROM products", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
items = pd.read_sql_query("SELECT * FROM order_items", con)

# pd:main
def top_products(products, orders, items, n=2):
    d = (items.merge(orders.loc[orders["status"] == "completed", ["order_id"]], on="order_id")
              .merge(products, on="product_id"))
    d["category"] = d["category"].fillna("Uncategorised")
    d["revenue"] = d["qty"] * d["unit_price"]
    p = d.groupby(["category", "product_id", "name"], as_index=False).agg(units=("qty", "sum"),
                                                                           revenue=("revenue", "sum"))
    p["share_pct"] = (p["revenue"] * 100.0 / p.groupby("category")["revenue"].transform("sum")).round(2)
    p["rnk"] = p.groupby("category")["revenue"].rank(method="dense", ascending=False).astype(int)
    out = p[p["rnk"] <= n].sort_values(["category", "rnk", "name"]).reset_index(drop=True)
    return out[["category", "name", "units", "revenue", "share_pct", "rnk"]]
# pd:end

pd_res = top_products(products, orders, items)
# compare after sorting by category, rnk, name (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_res, sql_main, check_dtype=False)
print("pandas rows:", len(pd_res), "; SQL rows:", len(sql_main))
print("asserts passed")
