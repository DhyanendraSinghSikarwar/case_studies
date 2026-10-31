# Q20: first-to-second purchase gap, repeat purchase rate, repeat within 30 days (as-of aware)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-01 10:00:00',100),(2,1,'2024-01-11 10:00:00',50),(3,1,'2024-03-01 10:00:00',70),
 (4,2,'2024-01-05 09:00:00',200),(5,2,'2024-02-20 09:00:00',80),
 (6,3,'2024-02-01 12:00:00',40),
 (8,4,'2024-03-01 10:00:00',90),(7,4,'2024-03-01 10:00:00',30),
 (9,5,'2024-01-15 08:00:00',25),(10,5,'2024-01-20 08:00:00',35),
 (11,6,'2024-04-01 15:00:00',60);
"""
AS_OF = "2024-04-15"
SQL_GAPS = """
WITH r AS (
  SELECT user_id, order_id, order_ts,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id) AS rn
  FROM orders
  WHERE order_ts < date(:as_of, '+1 day')
)
SELECT a.user_id,
       CAST(julianday(date(b.order_ts)) - julianday(date(a.order_ts)) AS INTEGER) AS gap_days
FROM r a JOIN r b ON b.user_id = a.user_id AND a.rn = 1 AND b.rn = 2
ORDER BY a.user_id
"""
SQL_STATS = """
WITH r AS (
  SELECT user_id, order_id, order_ts,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id) AS rn
  FROM orders WHERE order_ts < date(:as_of, '+1 day')
),
g AS (
  SELECT a.user_id,
         CAST(julianday(date(b.order_ts)) - julianday(date(a.order_ts)) AS INTEGER) AS gap_days
  FROM r a JOIN r b ON b.user_id = a.user_id AND a.rn = 1 AND b.rn = 2
),
o AS (
  SELECT gap_days, ROW_NUMBER() OVER (ORDER BY gap_days) AS k, COUNT(*) OVER () AS n FROM g
)
SELECT (SELECT ROUND(AVG(gap_days), 2) FROM g) AS avg_gap,
       (SELECT AVG(gap_days) FROM o WHERE k IN ((n + 1) / 2, (n + 2) / 2)) AS median_gap
"""
SQL_RATES = """
WITH r AS (
  SELECT user_id, order_ts,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_ts, order_id) AS rn
  FROM orders WHERE order_ts < date(:as_of, '+1 day')
),
u AS (
  SELECT a.user_id, a.order_ts AS first_ts, b.order_ts AS second_ts
  FROM r a LEFT JOIN r b ON b.user_id = a.user_id AND b.rn = 2
  WHERE a.rn = 1
)
SELECT COUNT(*) AS customers,
       COUNT(second_ts) AS repeaters,
       ROUND(100.0 * COUNT(second_ts) / COUNT(*), 1) AS repeat_rate_pct,
       SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of THEN 1 ELSE 0 END) AS eligible_30d,
       SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of
                 AND second_ts IS NOT NULL
                 AND date(second_ts) <= date(first_ts, '+30 days') THEN 1 ELSE 0 END) AS repeat_30d,
       ROUND(100.0 * SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of
                               AND second_ts IS NOT NULL
                               AND date(second_ts) <= date(first_ts, '+30 days') THEN 1 ELSE 0 END)
             / NULLIF(SUM(CASE WHEN date(first_ts, '+30 days') <= :as_of THEN 1 ELSE 0 END), 0), 1) AS repeat_30d_pct
FROM u
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
P = {"as_of": AS_OF}
gaps_sql = pd.read_sql_query(SQL_GAPS, con, params=P)
stats_sql = pd.read_sql_query(SQL_STATS, con, params=P)
rates_sql = pd.read_sql_query(SQL_RATES, con, params=P)
print("gaps:"); print(gaps_sql.to_string(index=False))
print(stats_sql.to_string(index=False))
print(rates_sql.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
AS_OF_TS = pd.Timestamp(AS_OF)
o = orders.assign(order_ts=pd.to_datetime(orders["order_ts"]))
o = o[o["order_ts"] < AS_OF_TS + pd.Timedelta(days=1)].sort_values(["user_id", "order_ts", "order_id"])
o["rn"] = o.groupby("user_id").cumcount() + 1
first = o[o["rn"] == 1][["user_id", "order_ts"]].rename(columns={"order_ts": "first_ts"})
second = o[o["rn"] == 2][["user_id", "order_ts"]].rename(columns={"order_ts": "second_ts"})
u = first.merge(second, on="user_id", how="left")
u["gap_days"] = (u["second_ts"].dt.normalize() - u["first_ts"].dt.normalize()).dt.days
gaps_pd = u.dropna(subset=["gap_days"])[["user_id", "gap_days"]].astype({"gap_days": int}).reset_index(drop=True)
avg_gap = round(gaps_pd["gap_days"].mean(), 2)
median_gap = gaps_pd["gap_days"].quantile(0.5)
eligible = u["first_ts"].dt.normalize() + pd.Timedelta(days=30) <= AS_OF_TS
repeat30 = eligible & u["second_ts"].notna() & (u["second_ts"].dt.normalize() <= u["first_ts"].dt.normalize() + pd.Timedelta(days=30))
# pd:end
# compared in ascending user_id order
pd.testing.assert_frame_equal(gaps_pd, gaps_sql, check_dtype=False)
assert avg_gap == stats_sql["avg_gap"][0] and median_gap == stats_sql["median_gap"][0]
r = rates_sql.iloc[0]
assert len(u) == r["customers"] and u["second_ts"].notna().sum() == r["repeaters"]
assert round(100.0 * u["second_ts"].notna().mean(), 1) == r["repeat_rate_pct"]
assert eligible.sum() == r["eligible_30d"] and repeat30.sum() == r["repeat_30d"]
assert round(100.0 * repeat30.sum() / eligible.sum(), 1) == r["repeat_30d_pct"]
print("pandas equals SQL: gaps", gaps_pd["gap_days"].tolist(), "avg", avg_gap, "median", median_gap)
# the tie-breaker: user 4 has two orders at the same timestamp
print("user 4 rows by order_id:", o[o["user_id"] == 4][["order_id", "order_ts", "rn"]].to_dict("records"))
print("asserts passed")
