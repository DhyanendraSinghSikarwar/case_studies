# Q13: conversion rate by experiment arm (counts, rates, uplift; no p-values)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 10:00:00'),(2,'control','2024-03-01 11:00:00'),
 (3,'control','2024-03-02 09:00:00'),(4,'control','2024-03-02 12:00:00'),
 (5,'control','2024-03-03 08:00:00'),(6,'control','2024-03-03 09:00:00'),
 (7,'treatment','2024-03-01 10:30:00'),(8,'treatment','2024-03-01 12:00:00'),
 (9,'treatment','2024-03-02 10:00:00'),(10,'treatment','2024-03-02 13:00:00'),
 (11,'treatment','2024-03-03 08:30:00'),(12,'treatment','2024-03-03 10:00:00');
INSERT INTO orders VALUES
 (101,1,'2024-03-02 10:00:00',100,'completed'),(102,1,'2024-03-05 10:00:00',50,'completed'),
 (103,2,'2024-03-01 11:00:00',80,'completed'),
 (104,3,'2024-02-20 09:00:00',200,'completed'),
 (105,4,'2024-03-03 12:00:00',60,'cancelled'),
 (106,7,'2024-03-02 09:00:00',120,'completed'),(107,7,'2024-03-04 09:00:00',30,'completed'),
 (108,8,'2024-03-01 12:30:00',90,'completed'),
 (109,9,'2024-03-01 10:00:00',500,'completed'),
 (110,10,'2024-03-03 13:00:00',70,'completed');
"""

SQL_MAIN = """
WITH per_user AS (
  SELECT x.user_id, x.arm,
         COUNT(o.order_id)            AS n_orders,
         COALESCE(SUM(o.amount), 0)   AS revenue
  FROM experiments x
  LEFT JOIN orders o
    ON o.user_id = x.user_id
   AND o.status = 'completed'
   AND o.order_ts >= x.assigned_ts
  GROUP BY x.user_id, x.arm
), arms AS (
  SELECT arm,
         COUNT(*)                                   AS assigned_users,
         SUM(CASE WHEN n_orders > 0 THEN 1 ELSE 0 END) AS converters,
         SUM(revenue)                               AS revenue
  FROM per_user
  GROUP BY arm
), r AS (
  SELECT arm, assigned_users, converters, revenue,
         100.0 * converters / assigned_users AS conv_pct,
         1.0 * revenue / assigned_users      AS rev_per_user
  FROM arms
)
SELECT t.arm, t.assigned_users, t.converters,
       ROUND(t.conv_pct, 1)     AS conv_pct,
       ROUND(t.rev_per_user, 2) AS rev_per_assigned_user,
       CASE WHEN t.arm <> 'control' THEN ROUND(t.conv_pct - c.conv_pct, 1) END AS abs_uplift_pp,
       CASE WHEN t.arm <> 'control'
            THEN ROUND(100.0 * (t.conv_pct - c.conv_pct) / NULLIF(c.conv_pct, 0), 1) END AS rel_uplift_pct
FROM r t CROSS JOIN (SELECT conv_pct FROM r WHERE arm = 'control') c
ORDER BY t.arm
"""

# three wrong versions, for the walk-through
SQL_NO_TIME_FILTER = """
SELECT x.arm, COUNT(DISTINCT x.user_id) AS assigned_users,
       COUNT(DISTINCT CASE WHEN o.order_id IS NOT NULL THEN x.user_id END) AS converters
FROM experiments x
LEFT JOIN orders o ON o.user_id = x.user_id AND o.status = 'completed'
GROUP BY x.arm ORDER BY x.arm
"""
SQL_WHERE_FILTER = """
SELECT x.arm, COUNT(DISTINCT x.user_id) AS assigned_users
FROM experiments x
LEFT JOIN orders o ON o.user_id = x.user_id
WHERE o.status = 'completed' AND o.order_ts >= x.assigned_ts
GROUP BY x.arm ORDER BY x.arm
"""
SQL_ROWS = """
SELECT x.arm, COUNT(*) AS joined_rows, COUNT(DISTINCT x.user_id) AS users
FROM experiments x
LEFT JOIN orders o ON o.user_id = x.user_id AND o.status = 'completed' AND o.order_ts >= x.assigned_ts
GROUP BY x.arm ORDER BY x.arm
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("wrong 1, no time filter (orders before assignment count):")
print(pd.read_sql_query(SQL_NO_TIME_FILTER, con).to_string(index=False))
print("wrong 2, time filter in WHERE (LEFT JOIN turns into inner join, non-buyers vanish):")
print(pd.read_sql_query(SQL_WHERE_FILTER, con).to_string(index=False))
print("wrong 3, COUNT(*) on the joined rows:")
print(pd.read_sql_query(SQL_ROWS, con).to_string(index=False))

experiments = pd.read_sql_query("SELECT * FROM experiments", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
x = experiments.assign(assigned_ts=pd.to_datetime(experiments["assigned_ts"]))
o = orders[orders["status"] == "completed"].copy()
o["order_ts"] = pd.to_datetime(o["order_ts"])
j = o.merge(x[["user_id", "assigned_ts"]], on="user_id")
j = j[j["order_ts"] >= j["assigned_ts"]]
per = j.groupby("user_id").agg(n_orders=("order_id", "size"), revenue=("amount", "sum"))
pu = x.merge(per, on="user_id", how="left").fillna({"n_orders": 0, "revenue": 0})
a = pu.groupby("arm").agg(assigned_users=("user_id", "nunique"),
                          converters=("n_orders", lambda s: int((s > 0).sum())),
                          revenue=("revenue", "sum"))
a["conv_pct"] = 100.0 * a["converters"] / a["assigned_users"]
a["rev_per_user"] = a["revenue"] / a["assigned_users"]
ctl = a.loc["control", "conv_pct"]
a["abs_uplift_pp"] = (a["conv_pct"] - ctl).where(a.index != "control").round(1)
a["rel_uplift_pct"] = (100.0 * (a["conv_pct"] - ctl) / (ctl if ctl != 0 else float("nan"))).where(a.index != "control").round(1)
a["conv_pct"] = a["conv_pct"].round(1)
a["rev_per_assigned_user"] = a["rev_per_user"].round(2)
pd_df = a.reset_index()[["arm", "assigned_users", "converters", "conv_pct",
                         "rev_per_assigned_user", "abs_uplift_pp", "rel_uplift_pct"]]
# pd:end
print(pd_df.to_string(index=False))
# compare after ordering by arm
pd.testing.assert_frame_equal(sql_df.sort_values("arm").reset_index(drop=True),
                              pd_df.sort_values("arm").reset_index(drop=True), check_dtype=False)
print("asserts passed")
