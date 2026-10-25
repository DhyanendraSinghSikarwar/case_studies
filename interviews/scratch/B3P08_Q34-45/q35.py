# Q35: skipped steps, cumulative (max step) funnel versus strict ordered funnel
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:01:00','cart'),(1,'2024-03-01 10:02:00','checkout'),(1,'2024-03-01 10:03:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:01:00','cart'),(2,'2024-03-01 11:03:00','purchase'),
 (3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:05:00','purchase'),
 (4,'2024-03-01 13:00:00','view'),(4,'2024-03-01 13:01:00','cart'),
 (5,'2024-03-01 14:00:00','purchase'),
 (6,'2024-03-01 15:00:00','view'),(6,'2024-03-01 15:01:00','cart'),(6,'2024-03-01 15:02:00','checkout'),
 (7,'2024-03-01 16:00:00','view'),(7,'2024-03-01 16:05:00','checkout'),(7,'2024-03-01 16:10:00','cart'),(7,'2024-03-01 16:20:00','purchase'),
 (8,'2024-03-01 17:01:00','cart'),(8,'2024-03-01 17:02:00','checkout'),
 (9,'2024-03-01 18:00:00','view'),(9,'2024-03-01 18:01:00','login');
"""
SQL_MAIN = """
WITH s AS (
  SELECT user_id,
         MAX(CASE event_name WHEN 'view' THEN 1 WHEN 'cart' THEN 2
                             WHEN 'checkout' THEN 3 WHEN 'purchase' THEN 4 END) AS max_step
  FROM events
  GROUP BY user_id
), k(step, step_name) AS (
  VALUES (1,'view'),(2,'cart'),(3,'checkout'),(4,'purchase')
)
SELECT k.step, k.step_name,
       COUNT(s.user_id) AS users_cumulative
FROM k LEFT JOIN s ON s.max_step >= k.step
GROUP BY k.step, k.step_name
ORDER BY k.step
"""
SQL_SKIP = """
SELECT user_id,
       MAX(event_name = 'cart')     AS has_cart,
       MAX(event_name = 'checkout') AS has_checkout
FROM events
GROUP BY user_id
HAVING MAX(event_name = 'purchase') = 1
   AND (MAX(event_name = 'cart') = 0 OR MAX(event_name = 'checkout') = 0)
ORDER BY user_id
"""
SQL_PRESENCE = """
SELECT event_name, COUNT(DISTINCT user_id) AS users_any_order
FROM events WHERE event_name IN ('view','cart','checkout','purchase')
GROUP BY event_name
"""
SQL_STRICT = """
WITH t AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view'     THEN event_ts END) AS t1,
         MIN(CASE WHEN event_name = 'cart'     THEN event_ts END) AS t2,
         MIN(CASE WHEN event_name = 'checkout' THEN event_ts END) AS t3,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS t4
  FROM events GROUP BY user_id
)
SELECT COUNT(t1) AS s1,
       SUM(t1 IS NOT NULL AND t2 > t1) AS s2,
       SUM(t1 IS NOT NULL AND t2 > t1 AND t3 > t2) AS s3,
       SUM(t1 IS NOT NULL AND t2 > t1 AND t3 > t2 AND t4 > t3) AS s4
FROM t
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("cumulative funnel (SQL):"); print(sql_df.to_string(index=False))
skip_sql = pd.read_sql_query(SQL_SKIP, con)
print("users who reached purchase but skipped a step (SQL):"); print(skip_sql.to_string(index=False))
print("any-order presence per step (SQL):"); print(pd.read_sql_query(SQL_PRESENCE, con).to_string(index=False))
strict_sql = con.execute(SQL_STRICT).fetchone()
print("strict ordered funnel s1..s4 (SQL):", strict_sql)

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
steps = ["view", "cart", "checkout", "purchase"]
ev = events[events["event_name"].isin(steps)]
flags = (pd.crosstab(ev["user_id"], ev["event_name"]).gt(0)
           .reindex(columns=steps, fill_value=False))
max_step = ev["event_name"].map({s: i + 1 for i, s in enumerate(steps)}).groupby(ev["user_id"]).max()
cum = pd.DataFrame({"step": range(1, 5), "step_name": steps,
                    "users_cumulative": [int((max_step >= k).sum()) for k in range(1, 5)]})
skipped = flags[flags["purchase"] & ~(flags["cart"] & flags["checkout"])]
skip_pd = skipped.astype(int).rename(columns={"cart": "has_cart", "checkout": "has_checkout"})[["has_cart", "has_checkout"]].reset_index()
# pd:end
print(cum.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.sort_values("step").reset_index(drop=True), cum, check_dtype=False)
pd.testing.assert_frame_equal(skip_sql.sort_values("user_id").reset_index(drop=True),
                              skip_pd.sort_values("user_id").reset_index(drop=True), check_dtype=False)
# alternative idiom 1: row-wise cumprod of the presence booleans = "no skipped step" chain
chain = flags.astype(int).cumprod(axis=1).sum()
print("cumprod of presence booleans (no skipped step):", chain.to_dict())
# alternative idiom 2: strict ordered, from the first timestamp of each step
t = (ev.assign(event_ts=pd.to_datetime(ev["event_ts"]))
       .pivot_table(index="user_id", columns="event_name", values="event_ts", aggfunc="min")
       .reindex(columns=steps))
s1 = t["view"].notna()
s2 = s1 & (t["cart"] > t["view"])
s3 = s2 & (t["checkout"] > t["cart"])
s4 = s3 & (t["purchase"] > t["checkout"])
strict_pd = tuple(int(x.sum()) for x in (s1, s2, s3, s4))
print("strict ordered funnel s1..s4 (pandas):", strict_pd)
assert strict_pd == tuple(int(x) for x in strict_sql)
print("any-order presence (pandas):", flags.sum().to_dict())
print("asserts passed")
