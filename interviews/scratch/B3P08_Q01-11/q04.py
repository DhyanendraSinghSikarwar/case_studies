# Q4: GMV, AOV, ARPU, ARPPU for one month, with explicit status and denominator choices
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-02-10','IN',0),(3,'2024-03-05','IN',0),(4,'2024-03-20','US',0),
 (5,'2024-04-02','IN',0),(6,'2024-01-15','IN',1),(7,'2024-02-01','IN',0);
INSERT INTO orders VALUES
 (1,1,'2024-03-03 10:00:00',100,'completed'),
 (2,1,'2024-03-10 10:00:00',50,'completed'),
 (3,2,'2024-03-12 10:00:00',200,'returned'),
 (4,3,'2024-03-15 10:00:00',80,'completed'),
 (5,3,'2024-03-16 10:00:00',60,'cancelled'),
 (6,4,'2024-03-31 23:30:00',40,'completed'),
 (7,6,'2024-03-05 10:00:00',999,'completed'),
 (8,2,'2024-02-28 10:00:00',300,'completed'),
 (9,5,'2024-04-03 10:00:00',70,'completed');
"""
# assumptions: GMV = completed + returned orders placed in the month (cancelled excluded);
# net revenue = completed only; AOV = GMV / orders in GMV; test users out everywhere
SQL_MAIN = """
WITH u AS (SELECT user_id, signup_date FROM users WHERE is_test = 0),
m AS (SELECT o.* FROM orders o JOIN u ON u.user_id = o.user_id
      WHERE o.order_ts >= :m_start AND o.order_ts < date(:m_start, '+1 month')),
agg AS (
  SELECT SUM(CASE WHEN status IN ('completed', 'returned') THEN amount END) AS gmv,
         COUNT(CASE WHEN status IN ('completed', 'returned') THEN 1 END) AS gmv_orders,
         SUM(CASE WHEN status = 'completed' THEN amount END) AS net_revenue,
         COUNT(DISTINCT user_id) AS active_users,
         COUNT(DISTINCT CASE WHEN status = 'completed' THEN user_id END) AS paying_users
  FROM m),
reg AS (SELECT COUNT(*) AS registered FROM u WHERE signup_date < date(:m_start, '+1 month'))
SELECT substr(:m_start, 1, 7) AS month,
       COALESCE(gmv, 0) AS gmv, gmv_orders,
       ROUND(1.0 * gmv / NULLIF(gmv_orders, 0), 2) AS aov,
       COALESCE(net_revenue, 0) AS net_revenue,
       registered, active_users, paying_users,
       ROUND(1.0 * COALESCE(net_revenue, 0) / NULLIF(registered, 0), 2) AS arpu_registered,
       ROUND(1.0 * net_revenue / NULLIF(active_users, 0), 2) AS arpu_active,
       ROUND(1.0 * net_revenue / NULLIF(paying_users, 0), 2) AS arppu
FROM agg CROSS JOIN reg
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
months = ["2024-03-01", "2024-05-01"]  # May has no orders
sql_df = pd.concat([pd.read_sql_query(SQL_MAIN, con, params={"m_start": m}) for m in months], ignore_index=True)
sql_df[sql_df.columns[1:]] = sql_df[sql_df.columns[1:]].astype(float)  # None becomes NaN
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)

def ratio(n, d):
    return round(n / d, 2) if d else np.nan

def metrics(m_start):
    # pd:main
    start = pd.Timestamp(m_start)
    end = start + pd.offsets.MonthBegin(1)
    u = users[users["is_test"] == 0]
    m = orders.merge(u[["user_id"]], on="user_id")
    ts = pd.to_datetime(m["order_ts"])
    m = m[(ts >= start) & (ts < end)]
    gm = m[m["status"].isin(["completed", "returned"])]
    paid = m[m["status"] == "completed"]
    registered = int((pd.to_datetime(u["signup_date"]) < end).sum())
    gmv, net = float(gm["amount"].sum()), float(paid["amount"].sum())
    active, payers = m["user_id"].nunique(), paid["user_id"].nunique()
    return {"month": m_start[:7], "gmv": gmv, "gmv_orders": len(gm), "aov": ratio(gmv, len(gm)),
            "net_revenue": net, "registered": registered, "active_users": active, "paying_users": payers,
            "arpu_registered": ratio(net, registered), "arpu_active": ratio(net, active),
            "arppu": ratio(net, payers)}
    # pd:end

pd_df = pd.DataFrame([metrics(m) for m in months])
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # rows in month order
print("asserts passed")
# how the status choice moves GMV for March (non-test)
alt = con.execute("""SELECT SUM(amount), SUM(CASE WHEN status<>'cancelled' THEN amount END),
  SUM(CASE WHEN status='completed' THEN amount END) FROM orders o JOIN users u USING(user_id)
  WHERE u.is_test=0 AND order_ts >= '2024-03-01' AND order_ts < '2024-04-01'""").fetchone()
print("March GMV all statuses / excl cancelled / completed only:", alt)
