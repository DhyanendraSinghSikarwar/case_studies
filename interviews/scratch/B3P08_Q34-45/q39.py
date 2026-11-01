# Q39: registered users, MAU, payers, revenue, ARPU, revenue per active user, ARPPU by month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-12-10',0),(2,'2023-12-20',0),(3,'2024-01-05',0),(4,'2024-01-20',0),
 (5,'2024-02-10',0),(6,'2024-02-12',1),
 (7,'2024-03-02',0),(8,'2024-03-03',0),(9,'2024-03-05',0),(10,'2024-03-08',0),(11,'2024-03-09',0),(12,'2024-03-20',0);
INSERT INTO events VALUES
 (1,'2024-01-03 10:00:00','open'),(2,'2024-01-07 10:00:00','open'),(3,'2024-01-08 10:00:00','open'),(4,'2024-01-21 10:00:00','open'),
 (1,'2024-02-02 10:00:00','open'),(3,'2024-02-03 10:00:00','open'),(5,'2024-02-11 10:00:00','open'),(6,'2024-02-13 10:00:00','open'),
 (1,'2024-03-02 10:00:00','open'),(3,'2024-03-04 10:00:00','open'),(7,'2024-03-02 11:00:00','open'),(8,'2024-03-03 11:00:00','open'),
 (9,'2024-03-05 11:00:00','open'),(10,'2024-03-08 11:00:00','open'),(11,'2024-03-09 11:00:00','open'),(12,'2024-03-20 11:00:00','open');
INSERT INTO orders VALUES
 (1,1,'2024-01-04 09:00:00',100,'completed'),(2,3,'2024-01-09 09:00:00',200,'completed'),
 (3,2,'2024-01-15 09:00:00',100,'completed'),
 (4,1,'2024-02-04 09:00:00',100,'completed'),(5,5,'2024-02-12 09:00:00',300,'completed'),
 (6,2,'2024-02-15 09:00:00',100,'completed'),(7,6,'2024-02-14 09:00:00',999,'completed'),
 (8,1,'2024-03-05 09:00:00',100,'completed'),(9,7,'2024-03-06 09:00:00',100,'completed'),
 (10,2,'2024-03-15 09:00:00',100,'completed'),(11,3,'2024-03-16 09:00:00',50,'cancelled');
"""
SQL_MAIN = """
WITH RECURSIVE m(ms) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(ms, '+1 month') FROM m WHERE ms < '2024-03-01'
), u AS (SELECT user_id, signup_date FROM users WHERE COALESCE(is_test, 0) = 0),
reg AS (SELECT m.ms, COUNT(u.user_id) AS registered
        FROM m LEFT JOIN u ON u.signup_date < date(m.ms, '+1 month') GROUP BY m.ms),
act AS (SELECT date(e.event_ts, 'start of month') AS ms, COUNT(DISTINCT e.user_id) AS mau
        FROM events e JOIN u ON u.user_id = e.user_id GROUP BY 1),
pay AS (SELECT date(o.order_ts, 'start of month') AS ms, COUNT(DISTINCT o.user_id) AS payers,
               SUM(o.amount) AS revenue
        FROM orders o JOIN u ON u.user_id = o.user_id WHERE o.status = 'completed' GROUP BY 1),
pa AS (SELECT date(o.order_ts, 'start of month') AS ms, COUNT(DISTINCT o.user_id) AS active_payers
       FROM orders o JOIN u ON u.user_id = o.user_id
       WHERE o.status = 'completed'
         AND EXISTS (SELECT 1 FROM events e WHERE e.user_id = o.user_id
                       AND date(e.event_ts, 'start of month') = date(o.order_ts, 'start of month'))
       GROUP BY 1)
SELECT strftime('%Y-%m', m.ms) AS month, reg.registered, COALESCE(act.mau, 0) AS mau,
       COALESCE(pay.payers, 0) AS payers, COALESCE(pa.active_payers, 0) AS active_payers,
       COALESCE(pay.revenue, 0) AS revenue,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(reg.registered, 0), 2)  AS arpu,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(act.mau, 0), 2)         AS rev_per_active,
       ROUND(1.0 * COALESCE(pay.revenue, 0) / NULLIF(pay.payers, 0), 2)      AS arppu,
       ROUND(1.0 * COALESCE(pa.active_payers, 0) / NULLIF(act.mau, 0), 3)    AS payer_share_of_mau,
       ROUND(1.0 * COALESCE(pay.payers, 0) / NULLIF(act.mau, 0), 3)          AS naive_payers_over_mau
FROM m JOIN reg ON reg.ms = m.ms LEFT JOIN act ON act.ms = m.ms
       LEFT JOIN pay ON pay.ms = m.ms LEFT JOIN pa ON pa.ms = m.ms
ORDER BY m.ms
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
real = users[users["is_test"].fillna(0).eq(0)]
ids = set(real["user_id"])
ev = events[events["user_id"].isin(ids)].assign(month=lambda d: pd.to_datetime(d["event_ts"]).dt.strftime("%Y-%m"))
oc = orders[orders["user_id"].isin(ids) & orders["status"].eq("completed")].assign(
    month=lambda d: pd.to_datetime(d["order_ts"]).dt.strftime("%Y-%m"))
rows = []
for month in ["2024-01", "2024-02", "2024-03"]:
    month_end = (pd.Timestamp(month + "-01") + pd.offsets.MonthBegin(1)).strftime("%Y-%m-%d")
    registered = int((real["signup_date"] < month_end).sum())
    active = set(ev.loc[ev["month"].eq(month), "user_id"])
    m_orders = oc[oc["month"].eq(month)]
    payers = set(m_orders["user_id"])
    revenue = float(m_orders["amount"].sum())
    rows.append({"month": month, "registered": registered, "mau": len(active), "payers": len(payers),
                 "active_payers": len(payers & active), "revenue": revenue,
                 "arpu": round(revenue / registered, 2), "rev_per_active": round(revenue / len(active), 2),
                 "arppu": round(revenue / len(payers), 2),
                 "payer_share_of_mau": round(len(payers & active) / len(active), 3),
                 "naive_payers_over_mau": round(len(payers) / len(active), 3)})
pd_df = pd.DataFrame(rows)
# pd:end
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # both ordered by month
print("asserts passed")
