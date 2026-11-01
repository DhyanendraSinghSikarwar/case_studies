# Q41: weekly KPI row from several one-row CTEs, week 2024-03-04 (Mon) to 2024-03-10 (Sun)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO users VALUES
 (1,'2024-02-01','IN',0),(2,'2024-02-10','IN',0),(3,'2024-03-04','IN',0),(4,'2024-03-06','US',0),
 (5,'2024-03-10','IN',0),(6,'2024-03-11','IN',0),(7,'2024-03-05','IN',1),(8,'2024-02-20','US',0);
INSERT INTO events VALUES
 (1,'2024-03-04 09:00:00','open'),(1,'2024-03-05 09:00:00','open'),(2,'2024-03-06 09:00:00','open'),
 (3,'2024-03-04 10:00:00','open'),(4,'2024-03-06 10:00:00','open'),(5,'2024-03-10 23:30:00','open'),
 (6,'2024-03-11 00:30:00','open'),(7,'2024-03-05 10:00:00','open'),(1,'2024-03-03 23:00:00','open');
INSERT INTO orders VALUES
 (1,1,'2024-03-04 12:00:00',100,'completed'),(2,1,'2024-03-05 12:00:00',200,'completed'),
 (3,2,'2024-03-06 12:00:00',300,'completed'),(4,3,'2024-03-07 12:00:00',50,'cancelled'),
 (5,4,'2024-03-08 12:00:00',400,'completed'),(6,8,'2024-03-09 12:00:00',150,'completed'),
 (7,7,'2024-03-05 12:00:00',999,'completed'),(8,1,'2024-03-03 12:00:00',500,'completed');
INSERT INTO refunds VALUES
 (1,2,'2024-03-06 08:00:00',50),(2,2,'2024-03-07 08:00:00',30),(3,5,'2024-03-09 08:00:00',100),(4,8,'2024-03-04 08:00:00',500);
"""
SQL_MAIN = """
WITH u AS (SELECT user_id, signup_date FROM users WHERE COALESCE(is_test, 0) = 0),
signups AS (SELECT COUNT(*) AS new_signups FROM u WHERE signup_date BETWEEN '2024-03-04' AND '2024-03-10'),
wau AS (SELECT COUNT(DISTINCT e.user_id) AS wau
        FROM events e JOIN u ON u.user_id = e.user_id
        WHERE e.event_ts >= '2024-03-04 00:00:00' AND e.event_ts < '2024-03-11 00:00:00'),
ord AS (SELECT COUNT(*) AS orders, COALESCE(SUM(o.amount), 0) AS gmv, COUNT(DISTINCT o.user_id) AS paying_users
        FROM orders o JOIN u ON u.user_id = o.user_id
        WHERE o.status = 'completed'
          AND o.order_ts >= '2024-03-04 00:00:00' AND o.order_ts < '2024-03-11 00:00:00'),
ref AS (SELECT COALESCE(SUM(r.amount), 0) AS refund_amount
        FROM refunds r JOIN orders o ON o.order_id = r.order_id JOIN u ON u.user_id = o.user_id
        WHERE r.refund_ts >= '2024-03-04 00:00:00' AND r.refund_ts < '2024-03-11 00:00:00'),
pa AS (SELECT COUNT(DISTINCT o.user_id) AS active_payers
       FROM orders o JOIN u ON u.user_id = o.user_id
       WHERE o.status = 'completed' AND o.order_ts >= '2024-03-04 00:00:00' AND o.order_ts < '2024-03-11 00:00:00'
         AND o.user_id IN (SELECT e.user_id FROM events e
                           WHERE e.event_ts >= '2024-03-04 00:00:00' AND e.event_ts < '2024-03-11 00:00:00'))
SELECT signups.new_signups, wau.wau, ord.orders, ord.gmv,
       ROUND(1.0 * ord.gmv / NULLIF(ord.orders, 0), 2)                     AS aov,
       ref.refund_amount, ord.gmv - ref.refund_amount                      AS net_revenue,
       ord.paying_users,
       ROUND(1.0 * pa.active_payers / NULLIF(wau.wau, 0), 4)               AS paid_conversion,
       ROUND(1.0 * ord.gmv / NULLIF(wau.wau, 0), 2)                        AS revenue_per_active
FROM signups CROSS JOIN wau CROSS JOIN ord CROSS JOIN ref CROSS JOIN pa
"""
SQL_BIG = """
SELECT COUNT(*) AS joined_rows, SUM(o.amount) AS gmv_wrong, COUNT(DISTINCT o.order_id) AS orders_ok, COUNT(o.order_id) AS orders_wrong
FROM users u JOIN events e ON e.user_id = u.user_id
             JOIN orders o ON o.user_id = u.user_id AND o.status = 'completed'
             LEFT JOIN refunds r ON r.order_id = o.order_id
WHERE COALESCE(u.is_test,0)=0
  AND e.event_ts >= '2024-03-04' AND e.event_ts < '2024-03-11'
  AND o.order_ts >= '2024-03-04' AND o.order_ts < '2024-03-11'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.T.to_string(header=False))
print("big join, same week:", con.execute(SQL_BIG).fetchone(), "(joined_rows, GMV, correct order count, wrong order count)")

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
lo, hi = pd.Timestamp("2024-03-04"), pd.Timestamp("2024-03-11")       # half-open week, Monday start, UTC
real = users[users["is_test"].fillna(0).eq(0)]
ids = set(real["user_id"])
in_week = lambda s: (pd.to_datetime(s) >= lo) & (pd.to_datetime(s) < hi)
wau_ids = set(events.loc[in_week(events["event_ts"]) & events["user_id"].isin(ids), "user_id"])
oc = orders[orders["status"].eq("completed") & in_week(orders["order_ts"]) & orders["user_id"].isin(ids)]
ref = refunds.merge(orders[["order_id", "user_id"]], on="order_id")
ref = ref[in_week(ref["refund_ts"]) & ref["user_id"].isin(ids)]
gmv = float(oc["amount"].sum())
pd_df = pd.DataFrame([{
    "new_signups": int(pd.to_datetime(real["signup_date"]).between(lo, hi - pd.Timedelta(days=1)).sum()),
    "wau": len(wau_ids), "orders": len(oc), "gmv": gmv, "aov": round(gmv / len(oc), 2),
    "refund_amount": float(ref["amount"].sum()), "net_revenue": gmv - float(ref["amount"].sum()),
    "paying_users": oc["user_id"].nunique(),
    "paid_conversion": round(len(set(oc["user_id"]) & wau_ids) / len(wau_ids), 4),
    "revenue_per_active": round(gmv / len(wau_ids), 2)}])
# pd:end
print(pd_df.T.to_string(header=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # single row
# each CTE alone against a hand count (counted on paper from the INSERTs)
hand = {"new_signups": 3, "wau": 5, "orders": 5, "gmv": 1150.0, "refund_amount": 680.0,
        "net_revenue": 470.0, "paying_users": 4, "aov": 230.0, "paid_conversion": 0.6, "revenue_per_active": 230.0}
for k, v in hand.items():
    assert sql_df.iloc[0][k] == v, (k, sql_df.iloc[0][k], v)
print("hand counts match; asserts passed")
