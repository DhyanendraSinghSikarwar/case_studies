# Q14: seller scorecard: cancel rate, late rate among delivered, average rating, rank by late rate within tier
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sellers(seller_id INTEGER PRIMARY KEY, name TEXT, tier TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, seller_id INTEGER, placed_at TEXT, delivered_at TEXT, promised_by TEXT, status TEXT);
CREATE TABLE reviews(order_id INTEGER, rating INTEGER);
INSERT INTO sellers VALUES (1,'Alpha','GOLD'),(2,'Beta','GOLD'),(3,'Gamma','SILVER'),(4,'Delta','SILVER');
INSERT INTO orders VALUES
 (1,1,'2025-01-01','2025-01-04','2025-01-05','DELIVERED'),
 (2,1,'2025-01-02','2025-01-07','2025-01-05','DELIVERED'),
 (3,1,'2025-01-03',NULL,'2025-01-08','CANCELLED'),
 (4,1,'2025-01-04','2025-01-10','2025-01-10','DELIVERED'),
 (5,2,'2025-01-01','2025-01-09','2025-01-05','DELIVERED'),
 (6,2,'2025-01-02','2025-01-08','2025-01-06','DELIVERED'),
 (7,2,'2025-01-03','2025-01-05','2025-01-06','DELIVERED'),
 (8,3,'2025-01-01','2025-01-03','2025-01-04','DELIVERED'),
 (9,3,'2025-01-02',NULL,'2025-01-06','CANCELLED'),
 (10,4,'2025-01-01',NULL,'2025-01-05','CANCELLED'),
 (11,4,'2025-01-02',NULL,'2025-01-06','SHIPPED');
INSERT INTO reviews VALUES (1,5),(2,3),(4,4),(5,2),(6,4),(6,2),(8,5);
""")
sql = """
WITH o AS (
  SELECT seller_id,
         COUNT(*) AS orders,
         SUM(status = 'CANCELLED') AS cancelled,
         SUM(status = 'DELIVERED' AND delivered_at IS NOT NULL) AS delivered,
         SUM(status = 'DELIVERED' AND delivered_at > promised_by) AS late
  FROM orders GROUP BY seller_id),
rv AS (  -- one rating per order first (an order can have two review rows)
  SELECT o.seller_id, AVG(x.avg_rating) AS avg_rating
  FROM (SELECT order_id, AVG(rating) AS avg_rating FROM reviews GROUP BY order_id) x
  JOIN orders o ON o.order_id = x.order_id GROUP BY o.seller_id),
card AS (
  SELECT s.seller_id, s.name, s.tier, COALESCE(o.orders, 0) AS orders,
         ROUND(1.0 * o.cancelled / NULLIF(o.orders, 0), 4) AS cancel_rate,
         ROUND(1.0 * o.late / NULLIF(o.delivered, 0), 4) AS late_rate,
         ROUND(rv.avg_rating, 2) AS avg_rating
  FROM sellers s LEFT JOIN o ON o.seller_id = s.seller_id LEFT JOIN rv ON rv.seller_id = s.seller_id)
SELECT seller_id, name, tier, orders, cancel_rate, late_rate, avg_rating,
       CASE WHEN late_rate IS NULL THEN NULL
            ELSE RANK() OVER (PARTITION BY tier ORDER BY late_rate DESC NULLS LAST) END AS late_rank
FROM card ORDER BY tier, late_rank NULLS LAST, seller_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

# what averaging over review ROWS (instead of per order) would give for Beta
print("\nBeta average over review rows:", con.execute(
    "SELECT ROUND(AVG(rating),2) FROM reviews r JOIN orders o ON o.order_id=r.order_id WHERE o.seller_id=2").fetchone()[0],
    "vs per order:", a.loc[a.name == "Beta", "avg_rating"].iloc[0])

sellers = pd.read_sql("SELECT * FROM sellers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
rev = pd.read_sql("SELECT * FROM reviews", con)
orders["is_cancel"] = orders.status == "CANCELLED"
orders["is_deliv"] = (orders.status == "DELIVERED") & orders.delivered_at.notna()
orders["is_late"] = (orders.status == "DELIVERED") & (orders.delivered_at > orders.promised_by)
g = orders.groupby("seller_id").agg(orders=("order_id", "size"), cancelled=("is_cancel", "sum"),
                                    delivered=("is_deliv", "sum"), late=("is_late", "sum")).reset_index()
per_order = rev.groupby("order_id")["rating"].mean().rename("r").reset_index().merge(orders[["order_id", "seller_id"]], on="order_id")
rv = per_order.groupby("seller_id")["r"].mean().rename("avg_rating").reset_index()
p = sellers.merge(g, on="seller_id", how="left").merge(rv, on="seller_id", how="left")
p["orders"] = p.orders.fillna(0).astype("int64")
p["cancel_rate"] = (p.cancelled / p.orders.where(p.orders > 0)).round(4)
p["late_rate"] = (p.late / p.delivered.where(p.delivered > 0)).round(4)
p["avg_rating"] = p.avg_rating.round(2)
p["late_rank"] = p.groupby("tier")["late_rate"].rank(method="min", ascending=False, na_option="keep")
p = p[["seller_id", "name", "tier", "orders", "cancel_rate", "late_rate", "avg_rating", "late_rank"]]
p = p.sort_values(["tier", "late_rank", "seller_id"], na_position="last").reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by tier, late_rank (NULL last), seller_id")
