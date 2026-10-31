# Q21: repeat purchase rate within 60 days (mature cohort) and days from signup to first purchase
import sqlite3
import numpy as np
import pandas as pd

AS_OF = "2024-06-30"
AS_OF_END = "2024-07-01 00:00:00"

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-03-01',0),(2,'2024-03-01',0),(3,'2024-03-10',0),(4,'2024-03-15',0),(5,'2024-04-01',0),
 (6,'2024-05-01',0),(7,'2024-02-01',0),(8,'2024-06-20',0),(9,'2024-02-10',0),(10,'2024-06-01',0),
 (11,'2024-03-20',0),(12,'2024-03-01',1);
INSERT INTO orders VALUES
 (1,1,'2024-03-01 10:00:00',100,'completed'),(2,1,'2024-03-01 18:00:00',40,'completed'),
 (3,2,'2024-03-05 10:00:00',90,'completed'),(4,2,'2024-04-20 10:00:00',60,'completed'),
 (5,3,'2024-03-12 10:00:00',70,'completed'),(6,3,'2024-05-20 10:00:00',30,'completed'),
 (7,4,'2024-04-20 10:00:00',80,'completed'),
 (8,5,'2024-04-02 10:00:00',50,'cancelled'),(9,5,'2024-04-08 10:00:00',50,'completed'),(10,5,'2024-04-20 10:00:00',20,'cancelled'),
 (11,6,'2024-05-15 10:00:00',60,'completed'),(12,6,'2024-05-20 10:00:00',25,'completed'),
 (13,9,'2024-03-01 12:00:00',55,'completed'),(14,9,'2024-04-30 12:00:00',45,'completed'),
 (15,10,'2024-05-30 10:00:00',35,'completed'),
 (201,11,'2024-03-20 09:00:00',65,'completed'),(202,11,'2024-03-20 09:00:00',65,'completed'),
 (16,12,'2024-03-02 10:00:00',999,'completed'),(17,12,'2024-03-03 10:00:00',999,'completed');
"""

SQL_REPEAT = """
WITH co AS (
  SELECT o.user_id, o.order_ts,
         ROW_NUMBER() OVER (PARTITION BY o.user_id ORDER BY o.order_ts, o.order_id) AS rn
  FROM orders o JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed' AND u.is_test = 0
), f AS (
  SELECT user_id,
         MIN(CASE WHEN rn = 1 THEN order_ts END) AS t1,
         MIN(CASE WHEN rn = 2 THEN order_ts END) AS t2
  FROM co GROUP BY user_id
), m AS (
  SELECT * FROM f WHERE datetime(t1, '+60 days') < :as_of_end
)
SELECT COUNT(*) AS mature_purchasers,
       SUM(CASE WHEN t2 IS NOT NULL AND t2 <= datetime(t1, '+60 days') THEN 1 ELSE 0 END) AS repeaters,
       ROUND(100.0 * SUM(CASE WHEN t2 IS NOT NULL AND t2 <= datetime(t1, '+60 days') THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS repeat_pct
FROM m
"""

SQL_REPEAT_DAYS = """
WITH days AS (
  SELECT DISTINCT o.user_id, date(o.order_ts) AS d
  FROM orders o JOIN users u ON u.user_id = o.user_id
  WHERE o.status = 'completed' AND u.is_test = 0
), r AS (
  SELECT user_id, d, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) AS rn FROM days
), f AS (
  SELECT user_id, MIN(CASE WHEN rn = 1 THEN d END) AS d1, MIN(CASE WHEN rn = 2 THEN d END) AS d2
  FROM r GROUP BY user_id
), m AS (
  SELECT * FROM f WHERE date(d1, '+60 days') <= :as_of
)
SELECT COUNT(*) AS mature_purchasers,
       SUM(CASE WHEN d2 IS NOT NULL AND d2 <= date(d1, '+60 days') THEN 1 ELSE 0 END) AS repeaters,
       ROUND(100.0 * SUM(CASE WHEN d2 IS NOT NULL AND d2 <= date(d1, '+60 days') THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS repeat_pct
FROM m
"""

SQL_BUCKETS = """
WITH fp AS (
  SELECT u.user_id, u.signup_date, MIN(o.order_ts) AS first_ts
  FROM users u
  LEFT JOIN orders o ON o.user_id = u.user_id AND o.status = 'completed'
  WHERE u.is_test = 0
  GROUP BY u.user_id, u.signup_date
), b AS (
  SELECT user_id,
         CASE WHEN first_ts IS NULL THEN 5
              WHEN date(first_ts) < signup_date THEN 6
              ELSE CASE
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) = 0 THEN 1
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) <= 7 THEN 2
                WHEN CAST(ROUND(julianday(date(first_ts)) - julianday(signup_date)) AS INTEGER) <= 30 THEN 3
                ELSE 4 END
         END AS k
  FROM fp
), labels(k, bucket) AS (
  VALUES (1,'same day'),(2,'1-7 days'),(3,'8-30 days'),(4,'over 30 days'),(5,'never'),(6,'before signup (data issue)')
)
SELECT l.bucket,
       COUNT(b.user_id) AS users,
       ROUND(100.0 * COUNT(b.user_id) / (SELECT COUNT(*) FROM fp), 1) AS pct_of_signups
FROM labels l LEFT JOIN b ON b.k = l.k
GROUP BY l.k, l.bucket
ORDER BY l.k
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
rep = pd.read_sql_query(SQL_REPEAT, con, params={"as_of_end": AS_OF_END})
rep_day = pd.read_sql_query(SQL_REPEAT_DAYS, con, params={"as_of": AS_OF})
bk = pd.read_sql_query(SQL_BUCKETS, con)
print("(a) order level:"); print(rep.to_string(index=False))
print("(a) day level:"); print(rep_day.to_string(index=False))
print("(b) buckets:"); print(bk.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
co = orders.merge(users[users["is_test"] == 0], on="user_id")
co = co[co["status"] == "completed"].copy()
co["order_ts"] = pd.to_datetime(co["order_ts"])
co = co.sort_values(["user_id", "order_ts", "order_id"])
co["rn"] = co.groupby("user_id").cumcount() + 1
t1 = co[co["rn"] == 1].set_index("user_id")["order_ts"].rename("t1")
t2 = co[co["rn"] == 2].set_index("user_id")["order_ts"].rename("t2")
f = pd.concat([t1, t2], axis=1)
m = f[f["t1"] + pd.Timedelta(days=60) < pd.Timestamp(AS_OF_END)]
rep_ok = m["t2"].notna() & (m["t2"] <= m["t1"] + pd.Timedelta(days=60))
pd_rep = pd.DataFrame([{"mature_purchasers": len(m), "repeaters": int(rep_ok.sum()),
                        "repeat_pct": round(100.0 * rep_ok.sum() / len(m), 1)}])
# day-level: distinct purchase days
days = co.assign(d=co["order_ts"].dt.normalize())[["user_id", "d"]].drop_duplicates().sort_values(["user_id", "d"])
days["rn"] = days.groupby("user_id").cumcount() + 1
d1 = days[days["rn"] == 1].set_index("user_id")["d"].rename("d1")
d2 = days[days["rn"] == 2].set_index("user_id")["d"].rename("d2")
fd = pd.concat([d1, d2], axis=1)
md = fd[fd["d1"] + pd.Timedelta(days=60) <= pd.Timestamp(AS_OF)]
rep_day_ok = md["d2"].notna() & (md["d2"] <= md["d1"] + pd.Timedelta(days=60))
pd_rep_day = pd.DataFrame([{"mature_purchasers": len(md), "repeaters": int(rep_day_ok.sum()),
                            "repeat_pct": round(100.0 * rep_day_ok.sum() / len(md), 1)}])
# (b) buckets
u = users[users["is_test"] == 0].copy()
u["first_day"] = u["user_id"].map(t1.dt.normalize())
u["gap"] = (u["first_day"] - pd.to_datetime(u["signup_date"])).dt.days
k = np.select([u["first_day"].isna(), u["gap"] < 0, u["gap"] == 0, u["gap"] <= 7, u["gap"] <= 30],
              [5, 6, 1, 2, 3], default=4)
labels = {1: "same day", 2: "1-7 days", 3: "8-30 days", 4: "over 30 days", 5: "never", 6: "before signup (data issue)"}
cnt = pd.Series(k).value_counts().reindex(list(labels), fill_value=0)
pd_bk = pd.DataFrame({"bucket": list(labels.values()), "users": cnt.to_numpy(),
                      "pct_of_signups": (100.0 * cnt / len(u)).round(1).to_numpy()})
# pd:end
print(pd_rep.to_string(index=False)); print(pd_rep_day.to_string(index=False)); print(pd_bk.to_string(index=False))
pd.testing.assert_frame_equal(rep, pd_rep, check_dtype=False)          # one row
pd.testing.assert_frame_equal(rep_day, pd_rep_day, check_dtype=False)  # one row
pd.testing.assert_frame_equal(bk, pd_bk, check_dtype=False)            # compared in bucket order 1..6
print("asserts passed")
