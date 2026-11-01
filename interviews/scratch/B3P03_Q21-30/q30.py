# Q30: funnel scaffolding: one CTE of DISTINCT users per step, joined, with step-to-step conversion
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_name TEXT, event_time TEXT);
INSERT INTO events VALUES
 (1,'view','2024-05-01 09:00'),(1,'cart','2024-05-01 09:05'),(1,'purchase','2024-05-01 09:10'),
 (2,'view','2024-05-01 10:00'),(2,'cart','2024-05-01 10:02'),
 (3,'view','2024-05-01 11:00'),
 (4,'view','2024-05-01 12:00'),(4,'view','2024-05-01 12:01'),(4,'cart','2024-05-01 12:03'),(4,'cart','2024-05-01 12:04'),
 (5,'cart','2024-05-01 13:00'),
 (6,'purchase','2024-05-01 08:00'),(6,'cart','2024-05-01 08:30'),(6,'view','2024-05-01 09:00');
"""
SQL_MAIN = """
WITH viewed AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'view'),
     carted AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'cart'),
     bought AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'purchase'),
     steps AS (
       SELECT v.user_id AS viewer, c.user_id AS carter, b.user_id AS buyer
       FROM viewed v
       LEFT JOIN carted c ON c.user_id = v.user_id
       LEFT JOIN bought b ON b.user_id = c.user_id
     ),
     counts AS (
       SELECT COUNT(viewer) AS viewed_users, COUNT(carter) AS carted_users, COUNT(buyer) AS bought_users
       FROM steps
     )
SELECT viewed_users, carted_users, bought_users,
       ROUND(1.0 * carted_users / viewed_users, 3) AS view_to_cart,
       ROUND(1.0 * bought_users / carted_users, 3) AS cart_to_buy,
       ROUND(1.0 * bought_users / viewed_users, 3) AS view_to_buy
FROM counts
"""
SQL_NAIVE = """
SELECT COUNT(*) AS joined_rows, COUNT(DISTINCT v.user_id) AS distinct_users
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'
WHERE v.event_name = 'view'
"""
SQL_ORDERED = """
SELECT COUNT(DISTINCT v.user_id)
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'  AND c.event_time > v.event_time
JOIN events p ON p.user_id = v.user_id AND p.event_name = 'purchase' AND p.event_time > c.event_time
WHERE v.event_name = 'view'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
events = pd.read_sql_query("SELECT * FROM events", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("funnel (SQL):")
print(sql_df.to_string(index=False))
print("\nnaive join of raw event rows (view x cart):", con.execute(SQL_NAIVE).fetchone(), "(joined_rows, distinct_users)")
print("distinct users who did cart at all:", con.execute("SELECT COUNT(DISTINCT user_id) FROM events WHERE event_name='cart'").fetchone()[0],
      "| carted AND viewed:", sql_df.loc[0, "carted_users"])
print("users whose view < cart < purchase times are in order:", con.execute(SQL_ORDERED).fetchone()[0], "(simple version counts", sql_df.loc[0, "bought_users"], ")")

# pd:main
viewed = set(events.loc[events["event_name"] == "view", "user_id"])
carted = set(events.loc[events["event_name"] == "cart", "user_id"])
bought = set(events.loc[events["event_name"] == "purchase", "user_id"])
n_view = len(viewed)
n_cart = len(viewed & carted)
n_buy = len(viewed & carted & bought)
pd_df = pd.DataFrame({"viewed_users": [n_view], "carted_users": [n_cart], "bought_users": [n_buy],
                      "view_to_cart": [round(n_cart / n_view, 3)], "cart_to_buy": [round(n_buy / n_cart, 3)],
                      "view_to_buy": [round(n_buy / n_view, 3)]})
# same counts with isin on distinct users
v = events.loc[events["event_name"] == "view", "user_id"].drop_duplicates()
c = events.loc[events["event_name"] == "cart", "user_id"].drop_duplicates()
b = events.loc[events["event_name"] == "purchase", "user_id"].drop_duplicates()
n_cart2 = int(c.isin(v).sum())
n_buy2 = int(b[b.isin(v) & b.isin(c)].shape[0])
# pd:end
print("\npandas sets:")
print(pd_df.to_string(index=False))
print("pandas isin counts:", len(v), n_cart2, n_buy2)

# single row, compared column by column
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert (len(v), n_cart2, n_buy2) == (5, 4, 2)
print("\nasserts passed: SQL == pandas sets == isin counts (5 viewers, 4 carted, 2 purchased)")
