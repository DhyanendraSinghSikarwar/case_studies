# Q9: why funnel step 3 can exceed step 2: reproduce three causes, then a corrected cumulative funnel
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,1),(10,0);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),(2,'2024-03-01 11:10:00','purchase'),(2,'2024-03-01 11:10:02','purchase'),
 (3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:03:00','purchase'),
 (4,'2024-03-01 13:00:00','view'),(4,'2024-03-01 13:05:00','cart'),
 (5,'2024-03-01 14:00:00','view'),
 (6,'2024-03-01 15:00:00','view'),(6,'2024-03-01 15:05:00','cart'),(6,'2024-03-01 15:10:00','purchase'),
 (7,'2024-03-01 16:00:00','view'),(7,'2024-03-01 16:05:00','cart'),
 (8,'2024-03-01 17:00:00','view'),
 (9,'2024-03-01 18:00:00','purchase'),
 (10,'2024-03-01 19:00:00','view'),(10,'2024-03-01 19:02:00','purchase');
"""
# 1 naive: purchase EVENTS, test users in; 2 distinct users; 3 drop test users; 4 each step requires the previous one
SQL_NAIVE = """
SELECT 'naive: purchase events, test users in' AS version,
       COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END) AS view_n,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END) AS cart_n,
       COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) AS purchase_n
FROM events
"""
SQL_USERS = """
SELECT 'distinct users, test users in',
       COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END),
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END),
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END)
FROM events
"""
SQL_NOTEST = """
SELECT 'distinct users, test users out',
       COUNT(DISTINCT CASE WHEN e.event_name = 'view' THEN e.user_id END),
       COUNT(DISTINCT CASE WHEN e.event_name = 'cart' THEN e.user_id END),
       COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END)
FROM events e JOIN users u ON u.user_id = e.user_id WHERE u.is_test = 0
"""
SQL_CUM = """
WITH f AS (
  SELECT e.user_id,
         MAX(e.event_name = 'view') AS v, MAX(e.event_name = 'cart') AS c, MAX(e.event_name = 'purchase') AS p
  FROM events e JOIN users u ON u.user_id = e.user_id
  WHERE u.is_test = 0
  GROUP BY e.user_id
)
SELECT 'cumulative: each step needs the previous (presence, not order)' AS version,
       SUM(v), SUM(v * c), SUM(v * c * p)
FROM f
"""
SQL_SKIP = """
SELECT e.user_id FROM events e JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0 GROUP BY e.user_id
HAVING MAX(e.event_name = 'purchase') = 1 AND MAX(e.event_name = 'cart') = 0 ORDER BY e.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
cols = ["version", "view_n", "cart_n", "purchase_n"]
sql_rows = []
for q in (SQL_NAIVE, SQL_USERS, SQL_NOTEST, SQL_CUM):
    sql_rows.append(list(con.execute(q).fetchone()))
sql_df = pd.DataFrame(sql_rows, columns=cols)
print(sql_df.to_string(index=False))
print("purchasers with no cart event (express checkout), test users out:", [r[0] for r in con.execute(SQL_SKIP)])

events = pd.read_sql_query("SELECT * FROM events", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
def counts(ev, purchase_as_events=False):
    n = ev.groupby("event_name")["user_id"].nunique()
    p = (ev["event_name"] == "purchase").sum() if purchase_as_events else n.get("purchase", 0)
    return [n.get("view", 0), n.get("cart", 0), p]

clean = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
flags = pd.crosstab(clean["user_id"], clean["event_name"]).clip(upper=1).reindex(
    columns=["view", "cart", "purchase"], fill_value=0)
cum = [flags["view"].sum(), (flags["view"] * flags["cart"]).sum(),
       (flags["view"] * flags["cart"] * flags["purchase"]).sum()]
rows = [["naive: purchase events, test users in"] + counts(events, True),
        ["distinct users, test users in"] + counts(events),
        ["distinct users, test users out"] + counts(clean),
        ["cumulative: each step needs the previous (presence, not order)"] + cum]
pd_df = pd.DataFrame(rows, columns=["version", "view_n", "cart_n", "purchase_n"])
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # same four rows in the same order
print("asserts passed")
