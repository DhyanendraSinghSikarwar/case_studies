# Q14: share of total and growth contribution by country, Feb vs Mar 2024
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2023-12-01','IN',0),(2,'2023-12-05','IN',0),(3,'2023-12-10','US',0),
 (4,'2023-12-15','UK',0),(5,'2024-01-05','SG',0),(6,'2023-11-01','IN',1);
INSERT INTO orders VALUES
 (1,1,'2024-02-05 10:00:00',600,'completed'),(2,2,'2024-02-20 11:00:00',400,'completed'),
 (3,3,'2024-02-10 09:00:00',600,'completed'),(4,4,'2024-02-12 15:00:00',400,'completed'),
 (5,1,'2024-02-14 12:00:00',300,'cancelled'),(6,6,'2024-02-15 12:00:00',900,'completed'),
 (7,1,'2024-03-03 10:00:00',900,'completed'),(8,2,'2024-03-31 23:30:00',600,'completed'),
 (9,3,'2024-03-09 09:00:00',500,'completed'),(10,5,'2024-03-15 10:00:00',200,'completed'),
 (11,4,'2024-03-20 10:00:00',250,'cancelled');
"""

SQL_MAIN = """
WITH m AS (
  SELECT u.country, strftime('%Y-%m', o.order_ts) AS month, SUM(o.amount) AS rev
  FROM orders o
  JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed'
    AND u.is_test = 0
    AND strftime('%Y-%m', o.order_ts) IN ('2024-02', '2024-03')
  GROUP BY u.country, strftime('%Y-%m', o.order_ts)
), countries AS (
  SELECT DISTINCT country FROM m
), g AS (
  SELECT c.country,
         COALESCE(f.rev, 0) AS feb,
         COALESCE(r.rev, 0) AS mar
  FROM countries c
  LEFT JOIN m f ON f.country = c.country AND f.month = '2024-02'
  LEFT JOIN m r ON r.country = c.country AND r.month = '2024-03'
)
SELECT country,
       feb AS rev_feb,
       mar AS rev_mar,
       ROUND(100.0 * feb / SUM(feb) OVER (), 1) AS share_feb_pct,
       ROUND(100.0 * mar / SUM(mar) OVER (), 1) AS share_mar_pct,
       mar - feb AS change,
       ROUND(100.0 * (mar - feb) / NULLIF(SUM(mar - feb) OVER (), 0), 1) AS contribution_pct
FROM g
ORDER BY country
"""

# the same shares and contributions with scalar subqueries instead of window functions
SQL_ALT = """
WITH m AS (
  SELECT u.country, strftime('%Y-%m', o.order_ts) AS month, SUM(o.amount) AS rev
  FROM orders o
  JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed'
    AND u.is_test = 0
    AND strftime('%Y-%m', o.order_ts) IN ('2024-02', '2024-03')
  GROUP BY u.country, strftime('%Y-%m', o.order_ts)
), g AS (
  SELECT c.country,
         COALESCE((SELECT rev FROM m WHERE m.country = c.country AND m.month = '2024-02'), 0) AS feb,
         COALESCE((SELECT rev FROM m WHERE m.country = c.country AND m.month = '2024-03'), 0) AS mar
  FROM (SELECT DISTINCT country FROM m) c
)
SELECT country, feb AS rev_feb, mar AS rev_mar,
       ROUND(100.0 * feb / (SELECT SUM(feb) FROM g), 1) AS share_feb_pct,
       ROUND(100.0 * mar / (SELECT SUM(mar) FROM g), 1) AS share_mar_pct,
       mar - feb AS change,
       ROUND(100.0 * (mar - feb) / NULLIF((SELECT SUM(mar - feb) FROM g), 0), 1) AS contribution_pct
FROM g
ORDER BY country
"""

def make():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c

# pd:main
def pd_growth(orders, users):
    d = orders.merge(users, on="user_id")
    d = d[(d["status"] == "completed") & (d["is_test"] == 0)].copy()
    d["month"] = pd.to_datetime(d["order_ts"]).dt.strftime("%Y-%m")
    d = d[d["month"].isin(["2024-02", "2024-03"])]
    p = d.pivot_table(index="country", columns="month", values="amount", aggfunc="sum", fill_value=0)
    p = p.reindex(columns=["2024-02", "2024-03"], fill_value=0)
    out = pd.DataFrame({"country": p.index, "rev_feb": p["2024-02"].to_numpy(), "rev_mar": p["2024-03"].to_numpy()})
    out["share_feb_pct"] = (100.0 * out["rev_feb"] / out["rev_feb"].sum()).round(1)
    out["share_mar_pct"] = (100.0 * out["rev_mar"] / out["rev_mar"].sum()).round(1)
    out["change"] = out["rev_mar"] - out["rev_feb"]
    total_change = out["change"].sum()
    denom = total_change if total_change != 0 else np.nan
    out["contribution_pct"] = (100.0 * out["change"] / denom).round(1)
    return out.sort_values("country").reset_index(drop=True)
# pd:end

def same(sql_df, pd_df):
    sql_df = sql_df.assign(contribution_pct=sql_df["contribution_pct"].astype(float))  # NULL -> NaN
    pd.testing.assert_frame_equal(sql_df.sort_values("country").reset_index(drop=True),
                                  pd_df.sort_values("country").reset_index(drop=True), check_dtype=False)

con = make()
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("main (windows):"); print(sql_df.to_string(index=False))
alt_df = pd.read_sql_query(SQL_ALT, con)
pd.testing.assert_frame_equal(sql_df, alt_df)
users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
pd_df = pd_growth(orders, users)
print("pandas:"); print(pd_df.to_string(index=False))
same(sql_df, pd_df)

# scenario A: total growth is zero (drop the SG order of 200 in March)
a = make(); a.execute("DELETE FROM orders WHERE order_id = 10")
a_sql = pd.read_sql_query(SQL_MAIN, a)
print("zero total growth:"); print(a_sql.to_string(index=False))
same(a_sql, pd_growth(pd.read_sql_query("SELECT * FROM orders", a), users))
# scenario B: total growth is negative (IN falls to 1200 in March)
b = make(); b.execute("UPDATE orders SET amount = 600 WHERE order_id = 7")
b_sql = pd.read_sql_query(SQL_MAIN, b)
print("negative total growth:"); print(b_sql.to_string(index=False))
same(b_sql, pd_growth(pd.read_sql_query("SELECT * FROM orders", b), users))
print("asserts passed")
