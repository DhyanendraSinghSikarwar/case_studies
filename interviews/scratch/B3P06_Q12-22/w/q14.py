# Q14: new vs returning customers per month, NOT EXISTS version, pandas np.where
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05 10:00:00',100),(2,1,'2024-01-20 12:00:00',50),(3,1,'2024-02-10 09:00:00',80),
 (4,2,'2024-01-15 15:00:00',200),(5,2,'2024-03-02 11:00:00',60),
 (6,3,'2024-02-03 08:00:00',40),(7,3,'2024-02-25 19:00:00',30),
 (8,4,'2024-03-10 14:00:00',90),
 (9,5,'2024-03-11 10:00:00',10),(10,5,'2024-03-12 10:00:00',20);
"""
SQL_MAIN = """
WITH f AS (
  SELECT user_id, MIN(order_ts) AS first_ts FROM orders GROUP BY user_id
),
j AS (
  SELECT o.user_id, o.amount,
         strftime('%Y-%m', o.order_ts) AS month,
         strftime('%Y-%m', f.first_ts) AS first_month
  FROM orders o JOIN f ON f.user_id = o.user_id
)
SELECT month,
       COUNT(DISTINCT CASE WHEN month = first_month THEN user_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN month > first_month THEN user_id END) AS returning_customers,
       SUM(CASE WHEN month = first_month THEN amount ELSE 0 END) AS new_revenue,
       SUM(CASE WHEN month > first_month THEN amount ELSE 0 END) AS returning_revenue
FROM j
GROUP BY month
ORDER BY month
"""
SQL_NOT_EXISTS = """
WITH om AS (
  SELECT user_id, strftime('%Y-%m', order_ts) AS month, SUM(amount) AS revenue
  FROM orders GROUP BY user_id, strftime('%Y-%m', order_ts)
)
SELECT month,
       SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM orders p
                                 WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM orders p
                             WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN 1 ELSE 0 END) AS returning_customers,
       SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM orders p
                                 WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN revenue ELSE 0 END) AS new_revenue,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM orders p
                             WHERE p.user_id = om.user_id AND p.order_ts < month || '-01')
                THEN revenue ELSE 0 END) AS returning_revenue
FROM om
GROUP BY month
ORDER BY month
"""
SQL_ORDER_LEVEL = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM orders p WHERE p.user_id = o.user_id
                                 AND (p.order_ts < o.order_ts OR (p.order_ts = o.order_ts AND p.order_id < o.order_id)))
                THEN o.amount ELSE 0 END) AS first_order_revenue,
       SUM(CASE WHEN EXISTS (SELECT 1 FROM orders p WHERE p.user_id = o.user_id
                             AND (p.order_ts < o.order_ts OR (p.order_ts = o.order_ts AND p.order_id < o.order_id)))
                THEN o.amount ELSE 0 END) AS later_order_revenue
FROM orders o GROUP BY month ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
ne_df = pd.read_sql_query(SQL_NOT_EXISTS, con)
print("customer-level (first-order month), SQL_MAIN:")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, ne_df)  # both ordered by month
print("NOT EXISTS version equals SQL_MAIN")
print("order-level split (second order in first month counts as later):")
print(pd.read_sql_query(SQL_ORDER_LEVEL, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o["month"] = o["order_ts"].dt.to_period("M")
o["first_month"] = o.groupby("user_id")["order_ts"].transform("min").dt.to_period("M")
o["kind"] = np.where(o["month"] == o["first_month"], "new", "returning")
cust = o.groupby(["month", "kind"])["user_id"].nunique().unstack(fill_value=0)
rev = o.groupby(["month", "kind"])["amount"].sum().unstack(fill_value=0)
cust = cust.reindex(columns=["new", "returning"], fill_value=0)
rev = rev.reindex(columns=["new", "returning"], fill_value=0)
pd_df = pd.DataFrame({"month": cust.index.astype(str),
                      "new_customers": cust["new"].to_numpy(),
                      "returning_customers": cust["returning"].to_numpy(),
                      "new_revenue": rev["new"].to_numpy(),
                      "returning_revenue": rev["returning"].to_numpy()})
# pd:end
# compared after sorting by month (already ascending)
pd.testing.assert_frame_equal(pd_df.sort_values("month").reset_index(drop=True), sql_df, check_dtype=False)
print("pandas equals SQL")
print(pd_df.to_string(index=False))
print("asserts passed")
