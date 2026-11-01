# Q32: groupby().cumcount() and transform('size'/'max') as window functions
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, order_date TEXT);
INSERT INTO orders VALUES (1,1,50,'2026-01-03'),(2,2,70,'2026-01-01'),(3,1,80,'2026-01-01'),
                          (4,1,50,'2026-01-03'),(5,3,30,'2026-01-02'),(6,2,20,'2026-01-05');
"""
SQL_MAIN = """
SELECT order_id, customer_id, amount, order_date,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn,
       COUNT(*)     OVER (PARTITION BY customer_id)                               AS n_orders,
       MAX(amount)  OVER (PARTITION BY customer_id)                               AS max_amount,
       CASE WHEN ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC, order_id DESC) = 1
            THEN 1 ELSE 0 END                                                     AS is_last
FROM orders
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL:"); print(sql_df.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)   # frame is in order_id order, not date order
# pd:main
ordered = orders.sort_values(["order_date", "order_id"])
g = ordered.groupby("customer_id")
pd_df = orders.copy()
pd_df["rn"] = (g.cumcount() + 1)                      # index-aligned: assigned back by label
pd_df["n_orders"] = orders.groupby("customer_id")["order_id"].transform("size")
pd_df["max_amount"] = orders.groupby("customer_id")["amount"].transform("max")
pd_df["is_last"] = (g.cumcount(ascending=False) == 0).astype("int64")
# pd:end
print("\npandas (original row order kept):"); print(pd_df.to_string())
unsorted_cc = orders.groupby("customer_id").cumcount() + 1
print("\ncumcount WITHOUT sorting by date (follows current row order):", unsorted_cc.tolist())
print("cumcount first value is", orders.groupby("customer_id").cumcount().min(), "(starts at 0, so +1)")
print("index preserved by transform:", pd_df["n_orders"].index.equals(orders.index))
# compared after sorting by order_id
a = sql_df.sort_values("order_id").reset_index(drop=True)
b = pd_df.sort_values("order_id").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)
assert unsorted_cc.tolist() != pd_df["rn"].tolist()
print("asserts passed: SQL window columns == pandas cumcount/transform columns")
