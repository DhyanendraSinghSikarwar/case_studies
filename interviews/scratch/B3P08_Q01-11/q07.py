# Q7: strictly ordered funnel with MIN(CASE): first-of-each versus a chained (greedy) funnel, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 09:00:00','purchase'),(2,'2024-03-01 09:30:00','view'),(2,'2024-03-01 09:40:00','cart'),
 (3,'2024-03-01 10:00:00','view'),(3,'2024-03-01 10:05:00','cart'),(3,'2024-03-01 10:07:00','cart'),(3,'2024-03-01 10:20:00','purchase'),
 (4,'2024-03-01 08:00:00','cart'),(4,'2024-03-01 09:00:00','view'),(4,'2024-03-01 09:10:00','cart'),(4,'2024-03-01 09:30:00','purchase'),
 (5,'2024-03-01 11:00:00','view'),(5,'2024-03-01 11:05:00','purchase'),
 (6,'2024-03-01 12:00:00','view'),(6,'2024-03-01 12:05:00','cart'),
 (7,'2024-03-01 13:00:00','view'),(7,'2024-03-01 13:01:00','view'),
 (8,'2024-03-01 12:00:00','view'),(8,'2024-03-01 12:00:00','cart'),(8,'2024-03-01 12:10:00','purchase');
"""
SQL_FIRST = """
WITH f AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view'     THEN event_ts END) AS first_view,
         MIN(CASE WHEN event_name = 'cart'     THEN event_ts END) AS first_cart,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY user_id
)
SELECT COUNT(first_view) AS viewed,
       COUNT(CASE WHEN first_view < first_cart THEN 1 END) AS carted,
       COUNT(CASE WHEN first_view < first_cart AND first_cart < first_purchase THEN 1 END) AS purchased
FROM f
"""
SQL_ANY = """
SELECT COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END) AS viewed,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END) AS carted,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchased
FROM events
"""
SQL_CHAIN = """
WITH v AS (SELECT user_id, MIN(event_ts) AS t1 FROM events WHERE event_name = 'view' GROUP BY user_id),
c AS (SELECT v.user_id, MIN(e.event_ts) AS t2
      FROM v JOIN events e ON e.user_id = v.user_id AND e.event_name = 'cart' AND e.event_ts > v.t1
      GROUP BY v.user_id),
p AS (SELECT c.user_id, MIN(e.event_ts) AS t3
      FROM c JOIN events e ON e.user_id = c.user_id AND e.event_name = 'purchase' AND e.event_ts > c.t2
      GROUP BY c.user_id)
SELECT (SELECT COUNT(*) FROM v) AS viewed, (SELECT COUNT(*) FROM c) AS carted, (SELECT COUNT(*) FROM p) AS purchased
"""
SQL_PER_USER = """
SELECT user_id,
       MIN(CASE WHEN event_name = 'view' THEN substr(event_ts, 12, 5) END) AS first_view,
       MIN(CASE WHEN event_name = 'cart' THEN substr(event_ts, 12, 5) END) AS first_cart,
       MIN(CASE WHEN event_name = 'purchase' THEN substr(event_ts, 12, 5) END) AS first_purchase
FROM events GROUP BY user_id ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print(pd.read_sql_query(SQL_PER_USER, con).to_string(index=False))
res = {}
for name, q in [("any-order", SQL_ANY), ("strict first-of-each", SQL_FIRST), ("chained after first view", SQL_CHAIN)]:
    res[name] = pd.read_sql_query(q, con).iloc[0]
sql_df = pd.DataFrame(res).T
print(sql_df.to_string())

events = pd.read_sql_query("SELECT * FROM events", con)
events["event_ts"] = pd.to_datetime(events["event_ts"])
# pd:main
first = events.groupby(["user_id", "event_name"])["event_ts"].min().unstack()
any_order = first[["view", "cart", "purchase"]].notna().sum()
ok2 = first["view"] < first["cart"]
ok3 = ok2 & (first["cart"] < first["purchase"])
strict = pd.Series({"viewed": first["view"].notna().sum(), "carted": ok2.sum(), "purchased": ok3.sum()})
# chained: cart must be after the first view, purchase after that cart
v = first["view"].dropna().rename("t1").reset_index()
carts = events[events["event_name"] == "cart"][["user_id", "event_ts"]]
c = v.merge(carts, on="user_id")
c = c[c["event_ts"] > c["t1"]].groupby("user_id", as_index=False)["event_ts"].min().rename(columns={"event_ts": "t2"})
purchases = events[events["event_name"] == "purchase"][["user_id", "event_ts"]]
p = c.merge(purchases, on="user_id")
p = p[p["event_ts"] > p["t2"]].groupby("user_id", as_index=False)["event_ts"].min()
chain = pd.Series({"viewed": len(v), "carted": len(c), "purchased": len(p)})
# pd:end
pd_df = pd.DataFrame({"any-order": any_order.to_numpy(), "strict first-of-each": strict.to_numpy(),
                      "chained after first view": chain.to_numpy()},
                     index=["viewed", "carted", "purchased"]).T
print(pd_df.to_string())
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # rows: any-order, strict, chained
print("asserts passed")
