# Q8: funnel by channel (channel taken from the same event, NULL shown as 'unknown'), SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT, channel TEXT);
CREATE TABLE user_channel(user_id INTEGER, channel TEXT);
INSERT INTO users VALUES (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','IN',0),(4,'2024-01-01','IN',0),
 (5,'2024-01-01','IN',0),(6,'2024-01-01','IN',0),(7,'2024-01-01','IN',0),(8,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view','ads'),(1,'2024-03-01 10:05:00','cart','ads'),(1,'2024-03-01 10:10:00','purchase','ads'),
 (2,'2024-03-01 11:00:00','view','ads'),(2,'2024-03-02 09:00:00','cart','email'),(2,'2024-03-02 09:10:00','purchase','email'),
 (3,'2024-03-01 12:00:00','view','organic'),(3,'2024-03-01 12:05:00','cart','organic'),(3,'2024-03-01 12:30:00','purchase','partner'),
 (4,'2024-03-01 13:00:00','view',NULL),(4,'2024-03-01 13:10:00','purchase',NULL),
 (5,'2024-03-01 14:00:00','view','ads'),
 (6,'2024-03-01 15:00:00','view','organic'),(6,'2024-03-01 15:05:00','view','ads'),(6,'2024-03-01 15:10:00','purchase','organic'),
 (7,'2024-03-01 16:00:00','view','email'),(7,'2024-03-01 16:05:00','cart','email'),(7,'2024-03-01 16:10:00','purchase','email'),
 (8,'2024-03-01 17:00:00','view','ads'),(8,'2024-03-01 17:10:00','purchase','ads');
INSERT INTO user_channel VALUES (1,'ads'),(2,'ads'),(2,'email'),(3,'organic'),(4,'ads'),(5,'ads'),(6,'organic'),(7,'email');
"""
SQL_MAIN = """
SELECT COALESCE(e.channel, 'unknown') AS channel,
       COUNT(DISTINCT CASE WHEN e.event_name = 'view'     THEN e.user_id END) AS view_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'cart'     THEN e.user_id END) AS cart_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END) AS purchase_users,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN e.event_name = 'view' THEN e.user_id END), 0), 1) AS view_to_purchase_pct
FROM events e
JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
GROUP BY COALESCE(e.channel, 'unknown')
ORDER BY view_users DESC, channel
"""
# defined attribution rule: the channel of the user's first event, one channel per user
SQL_FIRST_TOUCH = """
WITH ft AS (
  SELECT user_id, COALESCE(channel, 'unknown') AS channel,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts) AS rn
  FROM events
), c AS (SELECT user_id, channel FROM ft WHERE rn = 1)
SELECT c.channel,
       COUNT(DISTINCT CASE WHEN e.event_name = 'view'     THEN e.user_id END) AS view_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'cart'     THEN e.user_id END) AS cart_users,
       COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END) AS purchase_users,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_name = 'purchase' THEN e.user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN e.event_name = 'view' THEN e.user_id END), 0), 1) AS view_to_purchase_pct
FROM events e JOIN c ON c.user_id = e.user_id JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
GROUP BY c.channel ORDER BY view_users DESC, c.channel
"""
SQL_TOTALS = """
SELECT COUNT(DISTINCT CASE WHEN e.event_name='view' THEN e.user_id END) AS distinct_viewers,
       COUNT(DISTINCT CASE WHEN e.event_name='purchase' THEN e.user_id END) AS distinct_purchasers,
       COUNT(CASE WHEN e.event_name='purchase' THEN 1 END) AS purchase_events
FROM events e JOIN users u ON u.user_id = e.user_id WHERE u.is_test = 0
"""
SQL_WRONG_JOIN = """
SELECT COUNT(*) AS purchase_rows_after_join
FROM events e JOIN users u ON u.user_id = e.user_id JOIN user_channel uc ON uc.user_id = e.user_id
WHERE u.is_test = 0 AND e.event_name = 'purchase'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("same-event channel:"); print(sql_df.to_string(index=False))
print("channel rows add up to: view", sql_df["view_users"].sum(), "cart", sql_df["cart_users"].sum(),
      "purchase", sql_df["purchase_users"].sum())
print(pd.read_sql_query(SQL_TOTALS, con).to_string(index=False))
print("one channel per user (first event):"); print(pd.read_sql_query(SQL_FIRST_TOUCH, con).to_string(index=False))
print(pd.read_sql_query(SQL_WRONG_JOIN, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
e = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
e["channel"] = e["channel"].fillna("unknown")
cnt = (e.groupby(["channel", "event_name"])["user_id"].nunique().unstack(fill_value=0)
        .reindex(columns=["view", "cart", "purchase"], fill_value=0))
cnt.columns = ["view_users", "cart_users", "purchase_users"]
cnt["view_to_purchase_pct"] = (100.0 * cnt["purchase_users"] / cnt["view_users"].where(cnt["view_users"] > 0)).round(1)
pd_df = (cnt.reset_index().sort_values(["view_users", "channel"], ascending=[False, True])
            .reset_index(drop=True))
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # ordered by view_users desc, channel asc
print("asserts passed")
# what a default groupby does with the NaN channel
lost = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
print("groupby default keeps channels:", sorted(lost.groupby("channel")["user_id"].nunique().index),
      "| dropna=False:", lost.groupby("channel", dropna=False)["user_id"].nunique().index.tolist())
