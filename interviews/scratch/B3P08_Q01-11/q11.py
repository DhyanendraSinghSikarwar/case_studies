# Q11: cancellation rate, refund rate by count and by value, per order month, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (7,6,'2024-01-25 10:00:00',60,'cancelled'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed'),
 (9,5,'2024-03-20 10:00:00',60,'completed'),
 (8,7,'2024-03-09 10:00:00',40,'cancelled'),
 (10,7,'2024-03-12 10:00:00',25,'cancelled'),
 (11,1,'2024-04-02 10:00:00',70,'cancelled');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
"""
SQL_MAIN = """
WITH ref AS (SELECT order_id, SUM(amount) AS refunded FROM refunds GROUP BY order_id)
SELECT strftime('%Y-%m', o.order_ts) AS month,
       COUNT(*) AS orders,
       SUM(o.status = 'cancelled') AS cancelled,
       ROUND(100.0 * SUM(o.status = 'cancelled') / COUNT(*), 1) AS cancel_rate,
       SUM(o.status = 'completed') AS completed,
       SUM(o.status = 'completed' AND r.order_id IS NOT NULL) AS refunded_orders,
       ROUND(100.0 * SUM(o.status = 'completed' AND r.order_id IS NOT NULL)
             / NULLIF(SUM(o.status = 'completed'), 0), 1) AS refund_rate_count,
       ROUND(100.0 * SUM(CASE WHEN o.status = 'completed' THEN COALESCE(r.refunded, 0) END)
             / NULLIF(SUM(CASE WHEN o.status = 'completed' THEN o.amount END), 0), 1) AS refund_rate_value
FROM orders o
LEFT JOIN ref r ON r.order_id = o.order_id
GROUP BY month
ORDER BY month
"""
SQL_EXISTS = """
SELECT strftime('%Y-%m', o.order_ts) AS month,
       ROUND(100.0 * SUM(EXISTS (SELECT 1 FROM refunds r WHERE r.order_id = o.order_id))
             / NULLIF(COUNT(*), 0), 1) AS refund_rate_count
FROM orders o
WHERE o.status = 'completed'
GROUP BY month ORDER BY month
"""
# wrong: refunds bucketed by refund_ts month over completed orders by order_ts month
SQL_WRONG = """
WITH o AS (SELECT strftime('%Y-%m', order_ts) AS month, COUNT(*) AS completed, SUM(amount) AS amt
           FROM orders WHERE status = 'completed' GROUP BY month),
r AS (SELECT strftime('%Y-%m', r.refund_ts) AS month, COUNT(*) AS refund_rows, SUM(r.amount) AS refunded
      FROM refunds r JOIN orders x ON x.order_id = r.order_id WHERE x.status = 'completed' GROUP BY month)
SELECT o.month, ROUND(100.0 * COALESCE(r.refund_rows, 0) / o.completed, 1) AS refund_rate_count_wrong,
       ROUND(100.0 * COALESCE(r.refunded, 0) / o.amt, 1) AS refund_rate_value_wrong
FROM o LEFT JOIN r ON r.month = o.month ORDER BY o.month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
ex = pd.read_sql_query(SQL_EXISTS, con)
print("EXISTS version of the count rate:"); print(ex.to_string(index=False))
print("wrong (refund month over order month):"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
o = orders.assign(month=orders["order_ts"].str[:7])
per_order = refunds.groupby("order_id")["amount"].sum().rename("refunded")
o = o.merge(per_order, on="order_id", how="left")
o["is_cancelled"] = o["status"] == "cancelled"
o["is_completed"] = o["status"] == "completed"
o["has_refund"] = o["is_completed"] & o["refunded"].notna()
o["done_amount"] = o["amount"].where(o["is_completed"], 0.0)
o["done_refunded"] = o["refunded"].fillna(0.0).where(o["is_completed"], 0.0)
g = o.groupby("month", as_index=False).agg(
    orders=("order_id", "size"), cancelled=("is_cancelled", "sum"), completed=("is_completed", "sum"),
    refunded_orders=("has_refund", "sum"), done_amount=("done_amount", "sum"), done_refunded=("done_refunded", "sum"))
den = g["completed"].where(g["completed"] > 0)
amt = g["done_amount"].where(g["done_amount"] > 0)
g["cancel_rate"] = (100.0 * g["cancelled"] / g["orders"]).round(1)
g["refund_rate_count"] = (100.0 * g["refunded_orders"] / den).round(1)
g["refund_rate_value"] = (100.0 * g["done_refunded"] / amt).round(1)
pd_df = g[["month", "orders", "cancelled", "cancel_rate", "completed", "refunded_orders",
           "refund_rate_count", "refund_rate_value"]]
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # ordered by month
pd.testing.assert_series_equal(ex["refund_rate_count"].iloc[:3].reset_index(drop=True),
                               sql_df["refund_rate_count"].iloc[:3].reset_index(drop=True))
print("asserts passed")
