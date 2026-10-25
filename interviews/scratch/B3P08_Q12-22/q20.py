# Q20: first-touch versus last-touch attribution with a 30-day lookback
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE touches(user_id INTEGER, touch_ts TEXT, channel TEXT);
CREATE TABLE orders(order_id INTEGER, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO touches VALUES
 (1,'2024-03-01 09:00:00','seo'),(1,'2024-03-10 09:00:00','email'),(1,'2024-03-19 09:00:00','ads'),
 (1,'2024-03-26 09:00:00','social'),
 (2,'2024-02-01 09:00:00','ads'),(2,'2024-03-05 09:00:00','email'),
 (4,'2024-03-10 09:00:00','social'),(4,'2024-03-14 10:00:00','ads'),(4,'2024-03-14 10:00:00','email'),
 (6,'2024-02-09 10:00:00','ads'),(6,'2024-03-10 10:00:00','push'),
 (5,'2024-03-01 09:00:00','seo');
INSERT INTO orders VALUES
 (1,1,'2024-03-20 12:00:00',100,'completed'),
 (2,1,'2024-03-25 09:00:00',50,'completed'),
 (3,2,'2024-03-22 10:00:00',200,'completed'),
 (4,3,'2024-03-18 10:00:00',80,'completed'),
 (5,4,'2024-03-15 08:00:00',60,'completed'),
 (6,5,'2024-03-16 08:00:00',70,'cancelled'),
 (7,6,'2024-03-10 10:00:00',40,'completed');
"""

SQL_MAIN = """
WITH co AS (
  SELECT order_id, user_id, order_ts, amount FROM orders WHERE status = 'completed'
), cand AS (
  SELECT co.order_id, t.channel,
         ROW_NUMBER() OVER (PARTITION BY co.order_id ORDER BY t.touch_ts ASC,  t.channel ASC) AS rn_first,
         ROW_NUMBER() OVER (PARTITION BY co.order_id ORDER BY t.touch_ts DESC, t.channel ASC) AS rn_last
  FROM co
  JOIN touches t
    ON t.user_id = co.user_id
   AND t.touch_ts <= co.order_ts
   AND t.touch_ts >= datetime(co.order_ts, '-30 days')
), ord AS (
  SELECT co.order_id, co.amount,
         COALESCE(f.channel, 'unattributed') AS first_channel,
         COALESCE(l.channel, 'unattributed') AS last_channel
  FROM co
  LEFT JOIN cand f ON f.order_id = co.order_id AND f.rn_first = 1
  LEFT JOIN cand l ON l.order_id = co.order_id AND l.rn_last = 1
), chan AS (
  SELECT first_channel AS channel FROM ord
  UNION
  SELECT last_channel FROM ord
)
SELECT c.channel,
       COALESCE((SELECT SUM(amount) FROM ord WHERE first_channel = c.channel), 0) AS first_touch_rev,
       COALESCE((SELECT SUM(amount) FROM ord WHERE last_channel  = c.channel), 0) AS last_touch_rev
FROM chan c
ORDER BY c.channel = 'unattributed', c.channel
"""

SQL_TOTAL = "SELECT SUM(amount) FROM orders WHERE status = 'completed'"

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
total = con.execute(SQL_TOTAL).fetchone()[0]
print(sql_df.to_string(index=False))
print("completed revenue:", total, "| first-touch sum:", sql_df["first_touch_rev"].sum(), "| last-touch sum:", sql_df["last_touch_rev"].sum())
assert sql_df["first_touch_rev"].sum() == total and sql_df["last_touch_rev"].sum() == total

touches = pd.read_sql_query("SELECT * FROM touches", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
co = orders[orders["status"] == "completed"].copy()
co["order_ts"] = pd.to_datetime(co["order_ts"])
t = touches.assign(touch_ts=pd.to_datetime(touches["touch_ts"]))
j = co.merge(t, on="user_id")
j = j[(j["touch_ts"] <= j["order_ts"]) & (j["touch_ts"] >= j["order_ts"] - pd.Timedelta(days=30))]
first = (j.sort_values(["order_id", "touch_ts", "channel"], ascending=[True, True, True])
          .drop_duplicates("order_id").set_index("order_id")["channel"])
last = (j.sort_values(["order_id", "touch_ts", "channel"], ascending=[True, False, True])
         .drop_duplicates("order_id").set_index("order_id")["channel"])
co["first_channel"] = co["order_id"].map(first).fillna("unattributed")
co["last_channel"] = co["order_id"].map(last).fillna("unattributed")
a = co.groupby("first_channel")["amount"].sum().rename("first_touch_rev")
b = co.groupby("last_channel")["amount"].sum().rename("last_touch_rev")
pd_df = pd.concat([a, b], axis=1).fillna(0).rename_axis("channel").reset_index()
pd_df = (pd_df.assign(_u=pd_df["channel"] == "unattributed")
              .sort_values(["_u", "channel"]).drop(columns="_u").reset_index(drop=True))
# pd:end
print(pd_df.to_string(index=False))
# compare with unattributed last, then channel name ascending (same ORDER BY as the SQL)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert pd_df["first_touch_rev"].sum() == total and pd_df["last_touch_rev"].sum() == total

# per-order detail for the walk-through
print(pd.DataFrame({"order_id": co["order_id"], "amount": co["amount"],
                    "first": co["first_channel"], "last": co["last_channel"]}).to_string(index=False))
print("asserts passed")
