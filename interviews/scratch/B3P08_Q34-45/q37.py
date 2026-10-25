# Q37: NULL channel, test users, bots, NOT IN with NULL, LEFT JOIN drops, bots only in the numerator
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT, channel TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT, user_agent TEXT);
CREATE TABLE bot_users(user_id INTEGER);
INSERT INTO users VALUES (1,'2024-03-01',0),(2,'2024-03-01',0),(3,'2024-03-02',1),(4,'2024-03-02',0),
                         (5,'2024-03-03',0),(6,'2024-03-03',0),(7,'2024-03-04',0),(8,'2024-03-04',0);
INSERT INTO bot_users VALUES (5),(NULL);
INSERT INTO events VALUES
 (1,1,'2024-03-05 10:00:00','visit','Mozilla/5.0'),(2,2,'2024-03-05 10:05:00','visit','Mozilla/5.0'),
 (3,3,'2024-03-05 10:10:00','visit','Mozilla/5.0'),(4,4,'2024-03-05 10:15:00','visit','Googlebot/2.1'),
 (5,5,'2024-03-05 10:20:00','visit','Mozilla/5.0'),(6,6,'2024-03-05 10:25:00','visit','Mozilla/5.0'),
 (7,7,'2024-03-05 10:30:00','visit','AbbottApp/1.0'),(8,8,'2024-03-05 10:35:00','visit','Mozilla/5.0');
INSERT INTO orders VALUES
 (1,1,'2024-03-06 09:00:00',100,'completed','ads'),
 (2,2,'2024-03-06 09:10:00',200,'completed',NULL),
 (3,3,'2024-03-06 09:20:00',300,'completed','ads'),
 (4,4,'2024-03-06 09:30:00',400,'completed','email'),
 (5,5,'2024-03-06 09:40:00',500,'completed',NULL),
 (6,6,'2024-03-06 09:50:00',600,'completed','email'),
 (7,NULL,'2024-03-06 10:00:00',700,'completed','ads'),
 (8,7,'2024-03-06 10:10:00',50,'cancelled','ads');
"""
# clean = not a test user (NULL is_test counts as not test), user_agent has no 'bot', not in bot_users
CLEAN_USERS = """
SELECT u.user_id FROM users u
WHERE COALESCE(u.is_test, 0) = 0
  AND NOT EXISTS (SELECT 1 FROM bot_users b WHERE b.user_id = u.user_id)
  AND NOT EXISTS (SELECT 1 FROM events e WHERE e.user_id = u.user_id AND e.user_agent LIKE '%bot%')
"""
SQL_MAIN = """
WITH clean AS (
  SELECT u.user_id FROM users u
  WHERE COALESCE(u.is_test, 0) = 0
    AND NOT EXISTS (SELECT 1 FROM bot_users b WHERE b.user_id = u.user_id)
    AND NOT EXISTS (SELECT 1 FROM events e WHERE e.user_id = u.user_id AND e.user_agent LIKE '%bot%')
)
SELECT COALESCE(o.channel, 'unknown') AS channel,
       COUNT(*)                       AS orders,
       SUM(o.amount)                  AS revenue
FROM orders o
WHERE o.status = 'completed'
  AND (o.user_id IS NULL OR o.user_id IN (SELECT user_id FROM clean))   -- guest orders stay in revenue
GROUP BY COALESCE(o.channel, 'unknown')
ORDER BY revenue DESC
"""
SQL_CONV = """
WITH clean AS (%s),
a AS (SELECT DISTINCT user_id FROM events WHERE user_id IN (SELECT user_id FROM clean)),
b AS (SELECT DISTINCT user_id FROM orders WHERE status='completed' AND user_id IN (SELECT user_id FROM clean))
SELECT (SELECT COUNT(*) FROM b) AS buyers, (SELECT COUNT(*) FROM a) AS active,
       ROUND(1.0 * (SELECT COUNT(*) FROM b) / (SELECT COUNT(*) FROM a), 4) AS conv
""" % CLEAN_USERS
SQL_CONV_NUM_ONLY = """
WITH clean AS (%s),
b AS (SELECT DISTINCT user_id FROM orders WHERE status='completed' AND user_id IN (SELECT user_id FROM clean))
SELECT (SELECT COUNT(*) FROM b) AS buyers,
       (SELECT COUNT(DISTINCT user_id) FROM events WHERE user_id IN (SELECT user_id FROM users WHERE COALESCE(is_test,0)=0)) AS active_with_bots,
       ROUND(1.0 * (SELECT COUNT(*) FROM b) / (SELECT COUNT(DISTINCT user_id) FROM events
             WHERE user_id IN (SELECT user_id FROM users WHERE COALESCE(is_test,0)=0)), 4) AS conv
""" % CLEAN_USERS
SQL_NOTIN = "SELECT COUNT(*) FROM users WHERE user_id NOT IN (SELECT user_id FROM bot_users)"
SQL_NOTEXISTS = "SELECT COUNT(*) FROM users u WHERE NOT EXISTS (SELECT 1 FROM bot_users b WHERE b.user_id = u.user_id)"
SQL_LEFT_DROP = """
SELECT COUNT(*) AS orders, SUM(o.amount) AS revenue FROM orders o LEFT JOIN users u ON u.user_id = o.user_id
WHERE o.status='completed' AND u.is_test = 0
"""
SQL_LEFT_OK = """
SELECT COUNT(*) AS orders, SUM(o.amount) AS revenue FROM orders o LEFT JOIN users u ON u.user_id = o.user_id
WHERE o.status='completed' AND COALESCE(u.is_test, 0) = 0
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("revenue by channel, clean (SQL):"); print(sql_df.to_string(index=False))
print("all completed revenue, no filter:", con.execute("SELECT SUM(amount) FROM orders WHERE status='completed'").fetchone()[0])
print("clean users:", [r[0] for r in con.execute(CLEAN_USERS + " ORDER BY 1")])
conv = con.execute(SQL_CONV).fetchone()
conv_bad = con.execute(SQL_CONV_NUM_ONLY).fetchone()
print("conversion, bots out of both (buyers, active, rate):", conv)
print("conversion, bots out of numerator only (buyers, active incl bots, rate):", conv_bad)
print("NOT IN with a NULL in bot_users -> users returned:", con.execute(SQL_NOTIN).fetchone()[0],
      "| NOT EXISTS ->", con.execute(SQL_NOTEXISTS).fetchone()[0])
print("LEFT JOIN + u.is_test = 0 (orders, revenue):", con.execute(SQL_LEFT_DROP).fetchone(),
      "| with COALESCE:", con.execute(SQL_LEFT_OK).fetchone())
print("LIKE '%bot%' matches:", [r for r in con.execute("SELECT user_id, user_agent FROM events WHERE user_agent LIKE '%bot%' ORDER BY 1")])

users = pd.read_sql_query("SELECT * FROM users", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
events = pd.read_sql_query("SELECT * FROM events", con)
bots = pd.read_sql_query("SELECT * FROM bot_users", con)
# pd:main
bot_ids = set(bots["user_id"].dropna().astype(int)) | set(
    events.loc[events["user_agent"].str.contains("bot", case=False, na=False), "user_id"])
clean_ids = set(users.loc[users["is_test"].fillna(0).eq(0), "user_id"]) - bot_ids
oc = orders[orders["status"].eq("completed") & (orders["user_id"].isna() | orders["user_id"].isin(clean_ids))]
pd_df = (oc.assign(channel=oc["channel"].fillna("unknown"))
           .groupby("channel", as_index=False)
           .agg(orders=("order_id", "size"), revenue=("amount", "sum"))
           .sort_values("revenue", ascending=False, kind="stable").reset_index(drop=True))
active = events.loc[events["user_id"].isin(clean_ids), "user_id"].nunique()
buyers = orders.loc[orders["status"].eq("completed") & orders["user_id"].isin(clean_ids), "user_id"].nunique()
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # both ordered by revenue desc (no ties here)
assert (buyers, active, round(buyers / active, 4)) == tuple(conv)
assert "bot" in "AbbottApp/1.0".lower()  # the false positive is real
print("pandas conversion:", buyers, active, round(buyers / active, 4))
print("asserts passed")
