# Q3: three versions of "paid conversion rate" with different denominators, SQL and pandas
import sqlite3
import pandas as pd

AS_OF = "2024-06-30"
SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-10',0),(2,'2024-02-01',0),(3,'2024-03-15',0),(4,'2024-04-01',0),
 (5,'2024-05-20',0),(6,'2024-06-10',0),(7,'2024-02-20',0),(8,'2024-01-05',1),(9,'2024-05-31',0);
INSERT INTO orders VALUES
 (101,1,'2024-01-12 10:00:00',100,'completed'),
 (102,1,'2024-04-02 10:00:00',50,'completed'),
 (103,1,'2024-04-03 10:00:00',70,'cancelled'),
 (104,2,'2024-04-15 10:00:00',80,'completed'),
 (105,3,'2024-03-20 10:00:00',60,'cancelled'),
 (106,3,'2024-03-25 10:00:00',90,'cancelled'),
 (107,4,'2024-04-20 10:00:00',40,'completed'),
 (108,4,'2024-04-21 10:00:00',40,'completed'),
 (109,5,'2024-06-05 10:00:00',55,'completed'),
 (110,6,'2024-06-12 10:00:00',30,'completed'),
 (111,8,'2024-01-06 10:00:00',500,'completed'),
 (113,1,'2024-05-01 10:00:00',25,'completed'),
 (114,9,'2024-06-30 15:00:00',35,'completed'),
 (115,9,'2024-06-02 10:00:00',20,'cancelled');
"""
SQL_MAIN = """
WITH nt AS (SELECT user_id, signup_date FROM users WHERE is_test = 0),
o AS (SELECT o.* FROM orders o JOIN nt ON nt.user_id = o.user_id),
mature AS (SELECT * FROM nt WHERE signup_date <= date(:as_of, '-30 days'))
SELECT
  ROUND(100.0 * (SELECT COUNT(DISTINCT user_id) FROM o WHERE status = 'completed')
        / (SELECT COUNT(*) FROM nt), 1) AS a_users_over_signups,
  ROUND(100.0 * (SELECT COUNT(*) FROM o WHERE status = 'completed')
        / (SELECT COUNT(*) FROM o), 1) AS b_orders_over_orders,
  ROUND(100.0 * (SELECT COUNT(*) FROM mature m WHERE EXISTS (
          SELECT 1 FROM o WHERE o.user_id = m.user_id AND o.status = 'completed'
            AND date(o.order_ts) >= m.signup_date
            AND date(o.order_ts) <= date(m.signup_date, '+30 days')))
        / (SELECT COUNT(*) FROM mature), 1) AS c_30d_window_mature
"""
SQL_BUG = """
WITH nt AS (SELECT user_id FROM users WHERE is_test = 0),
o AS (SELECT o.* FROM orders o JOIN nt ON nt.user_id = o.user_id)
SELECT ROUND(100.0 * (SELECT COUNT(DISTINCT user_id) FROM o WHERE status = 'completed')
             / (SELECT COUNT(*) FROM o), 1) AS users_over_orders_bug,
       ROUND(100.0 * (SELECT COUNT(*) FROM o WHERE status = 'completed')
             / (SELECT COUNT(*) FROM nt), 1) AS orders_over_users_bug
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": AS_OF})
print(sql_df.to_string(index=False))
print(pd.read_sql_query(SQL_BUG, con).to_string(index=False))
print("maturity cutoff:", con.execute("SELECT date(:a,'-30 days')", {"a": AS_OF}).fetchone()[0])

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
nt = users[users["is_test"] == 0]
o = orders.merge(nt[["user_id", "signup_date"]], on="user_id")
done = o[o["status"] == "completed"]
a = 100.0 * done["user_id"].nunique() / len(nt)
b = 100.0 * len(done) / len(o)
mature = nt[pd.to_datetime(nt["signup_date"]) <= pd.Timestamp(AS_OF) - pd.Timedelta(days=30)]
d = done.merge(mature[["user_id"]], on="user_id")
day = pd.to_datetime(d["order_ts"]).dt.normalize()
sign = pd.to_datetime(d["signup_date"])
hit = d[(day >= sign) & (day <= sign + pd.Timedelta(days=30))]
c = 100.0 * hit["user_id"].nunique() / len(mature)
pd_df = pd.DataFrame({"a_users_over_signups": [round(a, 1)], "b_orders_over_orders": [round(b, 1)],
                      "c_30d_window_mature": [round(c, 1)]})
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # one row
print("asserts passed")
print("mature users:", len(mature), "| non-test signups:", len(nt), "| orders (non-test):", len(o),
      "| completed:", len(done))
# date() window and unixepoch window agree on this data
x = con.execute("""SELECT COUNT(*) FROM users u JOIN orders o ON o.user_id = u.user_id
 WHERE o.status='completed' AND date(o.order_ts) >= u.signup_date
   AND unixepoch(date(o.order_ts)) <= unixepoch(u.signup_date) + 30*86400""").fetchone()[0]
y = con.execute("""SELECT COUNT(*) FROM users u JOIN orders o ON o.user_id = u.user_id
 WHERE o.status='completed' AND date(o.order_ts) >= u.signup_date
   AND date(o.order_ts) <= date(u.signup_date,'+30 days')""").fetchone()[0]
print("rows in window, unixepoch vs date():", x, y)
