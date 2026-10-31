# Q22: LTV to date by signup cohort, net of refunds, without fan-out (as-of 2024-06-30)
import sqlite3
import pandas as pd

AS_OF = "2024-06-30"
AS_OF_END = "2024-07-01 00:00:00"

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO users VALUES
 (1,'2024-01-10','IN',0),(2,'2024-01-20','IN',0),(3,'2024-02-05','US',0),(4,'2024-02-25','UK',0),
 (5,'2024-05-15','IN',0),(6,'2024-05-28','US',0),(7,'2024-01-15','IN',1),(8,'2024-04-01','IN',0);
INSERT INTO orders VALUES
 (1,1,'2024-01-12 10:00:00',1000,'completed'),(2,1,'2024-03-10 10:00:00',500,'completed'),
 (3,2,'2024-02-01 10:00:00',800,'completed'),(4,3,'2024-02-06 10:00:00',600,'completed'),
 (5,4,'2024-03-15 10:00:00',400,'cancelled'),(6,4,'2024-04-10 10:00:00',700,'completed'),
 (7,5,'2024-05-20 10:00:00',300,'completed'),(8,6,'2024-06-05 10:00:00',200,'completed'),
 (9,7,'2024-01-20 10:00:00',5000,'completed'),(10,2,'2024-07-02 10:00:00',100,'completed');
INSERT INTO refunds VALUES
 (1,1,'2024-01-20 10:00:00',100),(2,1,'2024-02-05 10:00:00',150),
 (3,4,'2024-03-01 10:00:00',600),(4,8,'2024-07-03 10:00:00',50),(5,5,'2024-03-20 10:00:00',40);
"""

SQL_MAIN = """
WITH rf AS (
  SELECT order_id, SUM(amount) AS refunded
  FROM refunds
  WHERE refund_ts < :as_of_end
  GROUP BY order_id
), ord AS (
  SELECT o.user_id,
         SUM(o.amount)                  AS gross,
         SUM(COALESCE(rf.refunded, 0))  AS refunded
  FROM orders o
  LEFT JOIN rf ON rf.order_id = o.order_id
  WHERE o.status = 'completed'
    AND o.order_ts < :as_of_end
  GROUP BY o.user_id
)
SELECT strftime('%Y-%m', u.signup_date)                              AS signup_month,
       COUNT(*)                                                      AS cohort_size,
       COALESCE(SUM(ord.gross), 0)                                   AS gross,
       COALESCE(SUM(ord.refunded), 0)                                AS refunded,
       COALESCE(SUM(ord.gross - ord.refunded), 0)                    AS net_revenue,
       ROUND(1.0 * COALESCE(SUM(ord.gross - ord.refunded), 0) / COUNT(*), 2) AS ltv_per_signup,
       (CAST(strftime('%Y', :as_of) AS INTEGER) * 12 + CAST(strftime('%m', :as_of) AS INTEGER))
       - (CAST(strftime('%Y', MIN(u.signup_date)) AS INTEGER) * 12
          + CAST(strftime('%m', MIN(u.signup_date)) AS INTEGER))     AS cohort_age_months
FROM users u
LEFT JOIN ord ON ord.user_id = u.user_id
WHERE u.is_test = 0
  AND u.signup_date < :as_of_end
GROUP BY strftime('%Y-%m', u.signup_date)
ORDER BY signup_month
"""

# the fan-out mistake: join orders to refunds first, then sum the order amount
SQL_WRONG = """
SELECT strftime('%Y-%m', u.signup_date) AS signup_month,
       SUM(o.amount) AS wrong_gross, SUM(COALESCE(r.amount, 0)) AS refunded
FROM users u
JOIN orders o ON o.user_id = u.user_id AND o.status = 'completed' AND o.order_ts < :as_of_end
LEFT JOIN refunds r ON r.order_id = o.order_id AND r.refund_ts < :as_of_end
WHERE u.is_test = 0
GROUP BY strftime('%Y-%m', u.signup_date)
ORDER BY signup_month
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"as_of_end": AS_OF_END, "as_of": AS_OF}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))
print("wrong (orders joined to refunds first):")
print(pd.read_sql_query(SQL_WRONG, con, params={"as_of_end": AS_OF_END}).to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
refunds = pd.read_sql_query("SELECT * FROM refunds", con)
# pd:main
cut = pd.Timestamp(AS_OF_END)
rf = refunds[pd.to_datetime(refunds["refund_ts"]) < cut].groupby("order_id", as_index=False)["amount"].sum()
rf = rf.rename(columns={"amount": "refunded"})
o = orders[(orders["status"] == "completed") & (pd.to_datetime(orders["order_ts"]) < cut)]
o = o.merge(rf, on="order_id", how="left").fillna({"refunded": 0})
per_user = o.groupby("user_id", as_index=False).agg(gross=("amount", "sum"), refunded=("refunded", "sum"))
u = users[(users["is_test"] == 0) & (pd.to_datetime(users["signup_date"]) < cut)].copy()
u = u.merge(per_user, on="user_id", how="left").fillna({"gross": 0, "refunded": 0})
u["signup_month"] = pd.to_datetime(u["signup_date"]).dt.strftime("%Y-%m")
g = u.groupby("signup_month").agg(cohort_size=("user_id", "size"), gross=("gross", "sum"),
                                  refunded=("refunded", "sum"), first_signup=("signup_date", "min"))
g["net_revenue"] = g["gross"] - g["refunded"]
g["ltv_per_signup"] = (g["net_revenue"] / g["cohort_size"]).round(2)
asof = pd.Timestamp(AS_OF)
fs = pd.to_datetime(g["first_signup"])
g["cohort_age_months"] = (asof.year * 12 + asof.month) - (fs.dt.year * 12 + fs.dt.month)
pd_df = g.reset_index()[["signup_month", "cohort_size", "gross", "refunded", "net_revenue",
                         "ltv_per_signup", "cohort_age_months"]]
# pd:end
print(pd_df.to_string(index=False))
# compare after ordering by signup_month
pd.testing.assert_frame_equal(sql_df.sort_values("signup_month").reset_index(drop=True),
                              pd_df.sort_values("signup_month").reset_index(drop=True), check_dtype=False)
print("asserts passed")
