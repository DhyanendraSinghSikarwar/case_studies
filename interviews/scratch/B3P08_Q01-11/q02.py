# Q2: funnel step counts with COUNT(DISTINCT user) in one scan, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:01:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),
 (3,'2024-03-01 12:00:00','view'),
 (4,'2024-03-02 09:00:00','view'),(4,'2024-03-02 09:05:00','cart'),(4,'2024-03-02 09:06:00','cart'),
 (4,'2024-03-02 09:10:00','purchase'),(4,'2024-03-02 09:11:00','purchase'),
 (5,'2024-03-02 13:00:00','purchase'),
 (6,'2024-03-02 14:00:00','cart'),(6,'2024-03-02 14:05:00','view'),(6,'2024-03-02 14:10:00','purchase'),
 (7,'2024-03-03 08:00:00','view'),(7,'2024-03-03 08:01:00','view'),(7,'2024-03-03 08:02:00','view'),
 (8,'2024-03-03 15:00:00','view'),(8,'2024-03-03 15:05:00','cart');
"""
SQL_MAIN = """
WITH s AS (
  SELECT COUNT(DISTINCT CASE WHEN event_name = 'view'     THEN user_id END) AS v,
         COUNT(DISTINCT CASE WHEN event_name = 'cart'     THEN user_id END) AS c,
         COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS p
  FROM events
)
SELECT 'view' AS step, 1 AS step_no, v AS users,
       NULL AS step_conv_pct, ROUND(100.0 * v / NULLIF(v, 0), 1) AS overall_conv_pct FROM s
UNION ALL
SELECT 'cart', 2, c, ROUND(100.0 * c / NULLIF(v, 0), 1), ROUND(100.0 * c / NULLIF(v, 0), 1) FROM s
UNION ALL
SELECT 'purchase', 3, p, ROUND(100.0 * p / NULLIF(c, 0), 1), ROUND(100.0 * p / NULLIF(v, 0), 1) FROM s
ORDER BY step_no
"""
# wrong: count events, not users
SQL_ROWS = """
SELECT event_name, COUNT(*) AS event_rows, COUNT(DISTINCT user_id) AS users
FROM events GROUP BY event_name ORDER BY CASE event_name WHEN 'view' THEN 1 WHEN 'cart' THEN 2 ELSE 3 END
"""
# what the any-order version cannot see
SQL_CHECK = """
SELECT user_id,
       MAX(event_name = 'view') AS has_view, MAX(event_name = 'cart') AS has_cart, MAX(event_name = 'purchase') AS has_purchase
FROM events GROUP BY user_id
HAVING MAX(event_name = 'purchase') = 1 AND (MAX(event_name = 'cart') = 0 OR MAX(event_name = 'view') = 0)
ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL funnel (users, any order):")
print(sql_df.to_string(index=False))
rows_df = pd.read_sql_query(SQL_ROWS, con)
print(rows_df.to_string(index=False))
r = rows_df.set_index("event_name")["event_rows"]
print("wrong, rows: cart/view %.1f  purchase/cart %.1f  overall %.1f" % (
    100 * r["cart"] / r["view"], 100 * r["purchase"] / r["cart"], 100 * r["purchase"] / r["view"]))
print("purchasers without a cart or a view event:")
print(pd.read_sql_query(SQL_CHECK, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
steps = ["view", "cart", "purchase"]
users = events.groupby("event_name")["user_id"].nunique().reindex(steps, fill_value=0)
pd_df = pd.DataFrame({"step": steps, "step_no": [1, 2, 3], "users": users.to_numpy()})
prev = pd_df["users"].shift(1)
pd_df["step_conv_pct"] = (100.0 * pd_df["users"] / prev).round(1)
pd_df["overall_conv_pct"] = (100.0 * pd_df["users"] / pd_df["users"].iloc[0]).round(1)
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
# compare after ordering by step_no (already in that order); NULL and NaN both read as NaN
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("asserts passed")

# rounding probe: SQLite ROUND rounds half away from zero, Python and numpy round half to even
print("probe ROUND(6.25,1), ROUND(2.5), ROUND(-2.5):", con.execute("SELECT ROUND(6.25,1), ROUND(2.5), ROUND(-2.5)").fetchone())
import numpy as np
print("probe python round(6.25,1), round(2.5), round(-2.5):", round(6.25, 1), round(2.5), round(-2.5),
      "| numpy:", np.round(6.25, 1), np.round(2.5), np.round(-2.5),
      "| pandas Series.round:", pd.Series([6.25]).round(1).iloc[0])
# empty table: NULLIF makes every rate NULL instead of an error
con.execute("DELETE FROM events")
print("empty table:", con.execute(SQL_MAIN).fetchall())
