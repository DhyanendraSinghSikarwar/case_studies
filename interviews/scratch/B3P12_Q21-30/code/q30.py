# Q30: GMV, net revenue, AOV and cancelled share per month.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2025-01-03','DELIVERED',100),(2,2,'2025-01-09','DELIVERED',200),
 (3,3,'2025-01-15','CANCELLED',150),(4,1,'2025-01-20','RETURNED',120),
 (5,4,'2025-01-28','DELIVERED',300),
 (6,2,'2025-02-02','DELIVERED',250),(7,5,'2025-02-06','CANCELLED',80),
 (8,6,'2025-02-11','CANCELLED',90),(9,3,'2025-02-19','DELIVERED',100),
 (10,1,'2025-02-25','RETURNED',60);
"""
SQL = """
SELECT substr(order_date, 1, 7) AS month,
       COUNT(*) AS orders,
       SUM(amount) AS gmv,
       SUM(CASE WHEN status = 'DELIVERED' THEN amount ELSE 0 END) AS net_revenue,
       ROUND(1.0 * SUM(CASE WHEN status = 'DELIVERED' THEN amount END)
             / NULLIF(COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END), 0), 2) AS aov_net,
       ROUND(1.0 * COUNT(CASE WHEN status = 'CANCELLED' THEN 1 END) / COUNT(*), 4) AS cancelled_share
FROM orders
GROUP BY substr(order_date, 1, 7)
ORDER BY month
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

o = pd.read_sql("SELECT * FROM orders", con)
# PANDAS START
d = o.assign(month=o["order_date"].str[:7],
             delivered=o["status"].eq("DELIVERED"),
             cancelled=o["status"].eq("CANCELLED"))
d["net_amount"] = d["amount"].where(d["delivered"], 0)
p = (d.groupby("month")
       .agg(orders=("order_id", "size"), gmv=("amount", "sum"),
            net_revenue=("net_amount", "sum"),
            n_delivered=("delivered", "sum"), n_cancelled=("cancelled", "sum"))
       .reset_index())
p["aov_net"] = (p["net_revenue"] / p["n_delivered"].where(p["n_delivered"] != 0)).round(2)
p["cancelled_share"] = (p["n_cancelled"] / p["orders"]).round(4)
p = p[["month", "orders", "gmv", "net_revenue", "aov_net", "cancelled_share"]]
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (ordered by month)")
print("AOV if you divide by ALL orders instead of delivered:",
      (p["net_revenue"] / p["orders"]).round(2).tolist())
