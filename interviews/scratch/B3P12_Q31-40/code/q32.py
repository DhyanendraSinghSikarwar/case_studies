# Q32: frequently bought together pairs, each pair once, distinct orders.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'B'),(3,'B'),
 (4,'B'),(4,'C'),
 (5,'A'),(5,'C'),
 (6,'D');
""")

sql_answer = """
WITH d AS (SELECT DISTINCT order_id, product_id FROM order_items)
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM d a
JOIN d b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
"""
sql_naive = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM order_items a
JOIN order_items b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
"""
got = pd.read_sql(sql_answer, con)
print("SQL answer"); print(got.to_string(index=False))
print("\nnaive (no DISTINCT), duplicate row counted twice"); print(pd.read_sql(sql_naive, con).to_string(index=False))

# --- pandas
items = pd.read_sql("SELECT * FROM order_items", con).drop_duplicates()
pairs = items.merge(items, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs.product_id_1 < pairs.product_id_2]
want = (pairs.groupby(["product_id_1", "product_id_2"]).size().rename("orders_together").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"}))
want = (want[want.orders_together >= 2]
        .sort_values(["orders_together", "p1", "p2"], ascending=[False, True, True]).reset_index(drop=True))
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: same rows in the same order (count desc, p1, p2)")
