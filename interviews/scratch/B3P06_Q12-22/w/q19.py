# Q19: customer lifetime and recency relative to a fixed as-of date
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 09:00:00',100),(2,1,'2024-03-15 10:00:00',50),(3,1,'2024-12-01 18:00:00',70),
 (4,2,'2024-05-05 12:00:00',200),
 (5,3,'2024-02-01 23:30:00',40),(6,3,'2024-02-02 00:30:00',60),
 (7,4,'2024-06-01 10:00:00',90),(8,4,'2025-01-05 09:00:00',30),
 (9,5,'2025-01-10 08:00:00',25);
"""
SQL_MAIN = """
SELECT user_id,
       date(MIN(order_ts)) AS first_order,
       date(MAX(order_ts)) AS last_order,
       CAST(julianday(date(MAX(order_ts))) - julianday(date(MIN(order_ts))) AS INTEGER) AS lifetime_days,
       COUNT(*) AS orders,
       CAST(julianday(:as_of) - julianday(date(MAX(order_ts))) AS INTEGER) AS recency_days
FROM orders
WHERE order_ts < date(:as_of, '+1 day')
GROUP BY user_id
ORDER BY user_id
"""
SQL_NAIVE = """
SELECT user_id,
       CAST(julianday(MAX(order_ts)) - julianday(MIN(order_ts)) AS INTEGER) AS lifetime_days_naive
FROM orders WHERE user_id = 3 GROUP BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": "2024-12-31"})
print("as of 2024-12-31:"); print(sql_df.to_string(index=False))
print("as of 2025-01-31 (the backfill gives a different answer):")
print(pd.read_sql_query(SQL_MAIN, con, params={"as_of": "2025-01-31"}).to_string(index=False))
print("naive lifetime for user 3 (timestamps, 1 hour apart):", con.execute(SQL_NAIVE).fetchone())

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
AS_OF = pd.Timestamp("2024-12-31")
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o = o[o["order_ts"] < AS_OF + pd.Timedelta(days=1)]
agg = o.groupby("user_id").agg(first_ts=("order_ts", "min"), last_ts=("order_ts", "max"),
                               orders=("order_id", "count")).reset_index()
pd_df = pd.DataFrame({
    "user_id": agg["user_id"],
    "first_order": agg["first_ts"].dt.strftime("%Y-%m-%d"),
    "last_order": agg["last_ts"].dt.strftime("%Y-%m-%d"),
    "lifetime_days": (agg["last_ts"].dt.normalize() - agg["first_ts"].dt.normalize()).dt.days,
    "orders": agg["orders"],
    "recency_days": (AS_OF - agg["last_ts"].dt.normalize()).dt.days,
})
# pd:end
# compared in ascending user_id order
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas equals SQL")
u3 = agg[agg["user_id"] == 3].iloc[0]
print("pandas naive lifetime for user 3 (.dt.days on the raw timestamps):", (u3["last_ts"] - u3["first_ts"]).days)
print("asserts passed")
