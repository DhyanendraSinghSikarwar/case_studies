# Q10: net revenue after refunds without fan-out (order-month view, plus a cash view), SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
"""
SQL_WRONG = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(o.amount) AS gross_wrong, SUM(COALESCE(r.amount, 0)) AS refunded,
       SUM(o.amount) - SUM(COALESCE(r.amount, 0)) AS net_wrong
FROM orders o LEFT JOIN refunds r ON r.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
"""
SQL_PREAGG = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       SUM(o.amount) AS gross,
       COALESCE(SUM(r.refunded), 0) AS refunded,
       SUM(o.amount) - COALESCE(SUM(r.refunded), 0) AS net
FROM orders o
LEFT JOIN (SELECT order_id, SUM(amount) AS refunded FROM refunds GROUP BY order_id) r
       ON r.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
"""
SQL_SCALAR = """
WITH x AS (
  SELECT strftime('%Y-%m', o.order_ts) AS month, o.amount,
         COALESCE((SELECT SUM(r.amount) FROM refunds r WHERE r.order_id = o.order_id), 0) AS refunded
  FROM orders o WHERE o.status = 'completed'
)
SELECT month, SUM(amount) AS gross, SUM(refunded) AS refunded, SUM(amount) - SUM(refunded) AS net
FROM x GROUP BY month ORDER BY month
"""
SQL_CASH = """
WITH ev AS (
  SELECT strftime('%Y-%m', order_ts) AS month, amount AS a FROM orders WHERE status = 'completed'
  UNION ALL
  SELECT strftime('%Y-%m', r.refund_ts), -r.amount
  FROM refunds r JOIN orders o ON o.order_id = r.order_id WHERE o.status = 'completed'
)
SELECT month, SUM(a) AS net_cash FROM ev GROUP BY month ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("wrong (join first, sum orders.amount):"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))
a = pd.read_sql_query(SQL_PREAGG, con)
b = pd.read_sql_query(SQL_SCALAR, con)
print("fix 1, pre-aggregate refunds:"); print(a.to_string(index=False))
pd.testing.assert_frame_equal(a, b)  # the two fixes agree, ordered by month
cash = pd.read_sql_query(SQL_CASH, con)
print("cash view (refund counted in the month it is paid):"); print(cash.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
done = orders[orders["status"] == "completed"].copy()
done["month"] = done["order_ts"].str[:7]
per_order = refunds.groupby("order_id")["amount"].sum().rename("refunded")
j = done.merge(per_order, on="order_id", how="left").fillna({"refunded": 0.0})
pd_df = (j.groupby("month", as_index=False)
          .agg(gross=("amount", "sum"), refunded=("refunded", "sum")))
pd_df["net"] = pd_df["gross"] - pd_df["refunded"]
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, a, check_dtype=False)  # ordered by month
# the fan-out in pandas: merging refund rows directly repeats order 1
wrong = done.merge(refunds[["order_id", "amount"]].rename(columns={"amount": "r"}), on="order_id", how="left")
print("pandas wrong gross by month:", wrong.groupby("month")["amount"].sum().to_dict())
print("asserts passed")
