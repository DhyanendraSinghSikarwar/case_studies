# Q11: strict-order checkout funnel (SQL chained MIN per step, pandas groupby min per step)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 10:00:00','view'),(1,'2025-03-01 10:05:00','add_to_cart'),(1,'2025-03-01 10:10:00','checkout'),(1,'2025-03-01 10:15:00','purchase'),
 (2,'2025-03-01 10:00:00','view'),(2,'2025-03-01 10:05:00','add_to_cart'),(2,'2025-03-01 10:10:00','checkout'),
 (3,'2025-03-01 10:00:00','view'),(3,'2025-03-01 10:05:00','add_to_cart'),
 (4,'2025-03-01 10:00:00','view'),
 (5,'2025-03-01 09:00:00','view'),(5,'2025-03-01 09:10:00','checkout'),(5,'2025-03-01 09:20:00','purchase'),(5,'2025-03-01 09:30:00','add_to_cart'),
 (6,'2025-03-01 10:00:00','view'),(6,'2025-03-01 10:10:00','add_to_cart'),(6,'2025-03-01 10:20:00','view'),
 (7,'2025-03-01 09:00:00','add_to_cart'),(7,'2025-03-01 09:30:00','view'),(7,'2025-03-01 10:00:00','add_to_cart'),(7,'2025-03-01 10:10:00','checkout'),(7,'2025-03-01 10:20:00','purchase'),
 (8,'2025-03-01 10:00:00','add_to_cart'),(8,'2025-03-01 10:05:00','checkout'),(8,'2025-03-01 10:10:00','purchase'),
 (9,'2025-03-01 10:00:00','view'),(9,'2025-03-01 10:00:00','add_to_cart'),
 (10,'2025-03-02 11:00:00','view'),(10,'2025-03-02 11:05:00','add_to_cart'),(10,'2025-03-02 11:10:00','checkout'),(10,'2025-03-02 11:15:00','purchase'),(10,'2025-03-02 11:20:00','purchase');
""")

# strict order: each step uses the EARLIEST event of that step that is later than the previous step's time
sql = """
WITH s1 AS (SELECT user_id, MIN(event_ts) AS t FROM events WHERE event_name = 'view' GROUP BY user_id),
s2 AS (SELECT s1.user_id, MIN(e.event_ts) AS t FROM s1 JOIN events e
         ON e.user_id = s1.user_id AND e.event_name = 'add_to_cart' AND e.event_ts > s1.t GROUP BY s1.user_id),
s3 AS (SELECT s2.user_id, MIN(e.event_ts) AS t FROM s2 JOIN events e
         ON e.user_id = s2.user_id AND e.event_name = 'checkout' AND e.event_ts > s2.t GROUP BY s2.user_id),
s4 AS (SELECT s3.user_id, MIN(e.event_ts) AS t FROM s3 JOIN events e
         ON e.user_id = s3.user_id AND e.event_name = 'purchase' AND e.event_ts > s3.t GROUP BY s3.user_id),
f AS (
  SELECT 1 AS step, 'view' AS step_name, COUNT(*) AS users FROM s1
  UNION ALL SELECT 2, 'add_to_cart', COUNT(*) FROM s2
  UNION ALL SELECT 3, 'checkout', COUNT(*) FROM s3
  UNION ALL SELECT 4, 'purchase', COUNT(*) FROM s4)
SELECT step, step_name, users,
       ROUND(1.0 * users / LAG(users) OVER (ORDER BY step), 4) AS step_conv,
       ROUND(1.0 * users / FIRST_VALUE(users) OVER (ORDER BY step), 4) AS overall_conv
FROM f ORDER BY step
"""
a = pd.read_sql(sql, con)
print("SQL strict funnel"); print(a.to_string(index=False))

# the 'simple' MIN(CASE) per step, with and without chaining, to show where each goes wrong
simple = """
WITH t AS (SELECT user_id,
  MIN(CASE WHEN event_name='view' THEN event_ts END) AS v,
  MIN(CASE WHEN event_name='add_to_cart' THEN event_ts END) AS c,
  MIN(CASE WHEN event_name='checkout' THEN event_ts END) AS k,
  MIN(CASE WHEN event_name='purchase' THEN event_ts END) AS p
  FROM events GROUP BY user_id)
SELECT COUNT(v) AS view_n, COUNT(c) AS cart_any, COUNT(k) AS checkout_any, COUNT(p) AS purchase_any,
  SUM(c > v) AS cart_chain, SUM(c > v AND k > c) AS checkout_chain, SUM(c > v AND k > c AND p > k) AS purchase_chain
FROM t
"""
print("\nsimple MIN(CASE) counts (no order / chained min):")
print(pd.read_sql(simple, con).to_string(index=False))

# pandas: same chain, one merge per step
ev = pd.read_sql("SELECT * FROM events", con)
cur = ev[ev.event_name == "view"].groupby("user_id")["event_ts"].min().rename("t").reset_index()
counts = [("view", len(cur))]
for name in ["add_to_cart", "checkout", "purchase"]:
    nxt = ev[ev.event_name == name][["user_id", "event_ts"]].merge(cur, on="user_id")
    nxt = nxt[nxt.event_ts > nxt.t].groupby("user_id")["event_ts"].min().rename("t").reset_index()
    counts.append((name, len(nxt)))
    cur = nxt
p = pd.DataFrame(counts, columns=["step_name", "users"])
p.insert(0, "step", range(1, 5))
p["step_conv"] = (p.users / p.users.shift(1)).round(4)
p["overall_conv"] = (p.users / p.users.iloc[0]).round(4)
print("\npandas strict funnel"); print(p.to_string(index=False))
# compare in step order (both already ordered by step)
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: SQL == pandas, rows in step order")
