# Q12: net revenue per order after partial returns, without join fan-out
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, shipping_fee INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id TEXT, qty INTEGER, unit_price INTEGER);
CREATE TABLE returns(return_id INTEGER PRIMARY KEY, item_id INTEGER, qty_returned INTEGER, refund_amount INTEGER);
INSERT INTO orders VALUES (1,10,'2025-01-05',50),(2,11,'2025-01-06',0),(3,12,'2025-01-07',40),(4,10,'2025-01-08',30),(5,13,'2025-01-09',0);
INSERT INTO order_items VALUES (1,1,'P1',2,100),(2,1,'P2',1,200),(3,2,'P1',1,100),(4,3,'P3',3,50),(5,3,'P2',1,200),(6,4,'P1',1,100),(7,5,'P4',4,25);
INSERT INTO returns VALUES (1,1,1,100),(2,1,1,100),(3,4,1,50),(4,6,1,100);
""")

naive = """
SELECT o.order_id, SUM(i.qty * i.unit_price) AS items_total, SUM(COALESCE(r.refund_amount, 0)) AS refunds,
       SUM(i.qty * i.unit_price) - SUM(COALESCE(r.refund_amount, 0)) AS net
FROM orders o JOIN order_items i ON i.order_id = o.order_id
LEFT JOIN returns r ON r.item_id = i.item_id
GROUP BY o.order_id ORDER BY o.order_id
"""
sql = """
WITH item_tot AS (
  SELECT order_id, SUM(qty * unit_price) AS items_total FROM order_items GROUP BY order_id),
ret_tot AS (
  SELECT i.order_id, SUM(r.refund_amount) AS refunds, COUNT(*) AS return_rows
  FROM returns r JOIN order_items i ON i.item_id = r.item_id GROUP BY i.order_id)
SELECT o.order_id, COALESCE(t.items_total, 0) AS items_total, COALESCE(r.refunds, 0) AS refunds,
       COALESCE(t.items_total, 0) - COALESCE(r.refunds, 0) AS net
FROM orders o LEFT JOIN item_tot t ON t.order_id = o.order_id
LEFT JOIN ret_tot r ON r.order_id = o.order_id
ORDER BY o.order_id
"""
share = """
SELECT COUNT(*) AS orders,
       SUM(EXISTS (SELECT 1 FROM returns r JOIN order_items i ON i.item_id = r.item_id WHERE i.order_id = o.order_id)) AS orders_with_return,
       ROUND(1.0 * SUM(EXISTS (SELECT 1 FROM returns r JOIN order_items i ON i.item_id = r.item_id WHERE i.order_id = o.order_id)) / COUNT(*), 4) AS return_share
FROM orders o
"""
n = pd.read_sql(naive, con); a = pd.read_sql(sql, con); s = pd.read_sql(share, con)
print("naive three-table join"); print(n.to_string(index=False), "\nnaive total net:", n.net.sum())
print("\npre-aggregated SQL"); print(a.to_string(index=False), "\ntotal net:", a.net.sum())
print("\nshare of orders with any return (SQL)"); print(s.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con)
items = pd.read_sql("SELECT * FROM order_items", con)
rets = pd.read_sql("SELECT * FROM returns", con)
items["line"] = items.qty * items.unit_price
it = items.groupby("order_id")["line"].sum().rename("items_total")
rt = rets.merge(items[["item_id", "order_id"]], on="item_id").groupby("order_id").agg(refunds=("refund_amount", "sum"), return_rows=("return_id", "size"))
p = orders[["order_id"]].merge(it, on="order_id", how="left").merge(rt[["refunds"]], on="order_id", how="left")
p[["items_total", "refunds"]] = p[["items_total", "refunds"]].fillna(0).astype("int64")
p["net"] = p.items_total - p.refunds
pshare = pd.DataFrame({"orders": [len(orders)], "orders_with_return": [int(orders.order_id.isin(rt.index).sum())]})
pshare["return_share"] = (pshare.orders_with_return / pshare.orders).round(4)
print("\npandas"); print(p.to_string(index=False)); print(pshare.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
pd.testing.assert_frame_equal(s, pshare, check_dtype=False)
print("\nasserts passed: per-order table (ordered by order_id) and share row equal")
