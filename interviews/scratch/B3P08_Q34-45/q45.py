# Q45: linear and time-decay (half-life 7 days) multi-touch attribution, 30-day lookback, unattributed row
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE touches(user_id INTEGER, touch_ts TEXT, channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO touches VALUES
 (1,'2024-02-28 10:00:00','social'),(1,'2024-03-02 10:00:00','ads'),(1,'2024-03-24 10:00:00','email'),(1,'2024-03-31 09:00:00','search'),
 (2,'2024-03-10 12:00:00','ads'),(2,'2024-03-17 12:00:00','social'),
 (4,'2024-03-18 12:00:00','ads'),(5,'2024-03-25 12:00:00','email');
INSERT INTO orders VALUES
 (1,1,'2024-03-31 10:00:00',120,'completed'),(2,2,'2024-03-17 12:00:00',60,'completed'),
 (3,3,'2024-03-20 12:00:00',80,'completed'),(4,4,'2024-03-20 12:00:00',500,'cancelled'),
 (5,5,'2024-03-20 12:00:00',90,'completed');
"""
SQL_MAIN = """
WITH j AS (                                  -- touches in the 30 days up to and including the order time
  SELECT o.order_id, o.amount, t.channel,
         (unixepoch(o.order_ts) - unixepoch(t.touch_ts)) / 86400.0 AS age_days
  FROM orders o JOIN touches t
    ON t.user_id = o.user_id
   AND t.touch_ts <= o.order_ts
   AND unixepoch(o.order_ts) - unixepoch(t.touch_ts) <= 30 * 86400
  WHERE o.status = 'completed'
), w AS (
  SELECT order_id, amount, channel, power(0.5, age_days / 7.0) AS decay_w FROM j
), s AS (
  SELECT order_id, amount, channel,
         1.0 / COUNT(*) OVER (PARTITION BY order_id)                 AS lin_w,
         decay_w / SUM(decay_w) OVER (PARTITION BY order_id)         AS dec_w
  FROM w
)
SELECT channel, ROUND(SUM(amount * lin_w), 4) AS linear, ROUND(SUM(amount * dec_w), 4) AS time_decay
FROM s GROUP BY channel
UNION ALL
SELECT 'unattributed', SUM(amount), SUM(amount)
FROM orders o WHERE o.status = 'completed' AND NOT EXISTS (SELECT 1 FROM j WHERE j.order_id = o.order_id)
ORDER BY channel
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("math functions compiled in:", con.execute("SELECT sqlite_compileoption_used('ENABLE_MATH_FUNCTIONS')").fetchone()[0],
      "| power(0.5, 2) =", con.execute("SELECT power(0.5, 2)").fetchone()[0],
      "| exp(-2*ln(2)) =", round(con.execute("SELECT exp(-2 * ln(2))").fetchone()[0], 12))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
total = con.execute("SELECT SUM(amount) FROM orders WHERE status='completed'").fetchone()[0]
assert abs(sql_df["linear"].sum() - total) < 1e-6 and abs(sql_df["time_decay"].sum() - total) < 1e-6
print("completed revenue:", total, "| linear sum:", round(sql_df["linear"].sum(), 6), "| time-decay sum:", round(sql_df["time_decay"].sum(), 6))

# fallback without power()/exp(): a lookup table of weights by whole days of age (0..30), built outside SQL
con.execute("CREATE TABLE lut(age_day INTEGER PRIMARY KEY, w REAL)")
con.executemany("INSERT INTO lut VALUES (?, ?)", [(d, 0.5 ** (d / 7.0)) for d in range(31)])
SQL_LUT = SQL_MAIN.replace("power(0.5, age_days / 7.0) AS decay_w FROM j",
                           "(SELECT w FROM lut WHERE age_day = CAST(age_days AS INTEGER)) AS decay_w FROM j")
lut_df = pd.read_sql_query(SQL_LUT, con)
print("LUT fallback (age truncated to whole days):"); print(lut_df.to_string(index=False))
print("largest difference to the exact weights: %.4f" % (lut_df["time_decay"] - sql_df["time_decay"]).abs().max())

touches = pd.read_sql_query("SELECT * FROM touches", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
o = orders[orders["status"].eq("completed")].assign(ots=pd.to_datetime(orders["order_ts"]))
t = touches.assign(tts=pd.to_datetime(touches["touch_ts"]))
j = o.merge(t, on="user_id")
j["age_days"] = (j["ots"] - j["tts"]).dt.total_seconds() / 86400.0
j = j[(j["tts"] <= j["ots"]) & (j["age_days"] <= 30)].copy()
j["lin_w"] = 1.0 / j.groupby("order_id")["order_id"].transform("size")
j["decay_w"] = 0.5 ** (j["age_days"] / 7.0)
j["dec_w"] = j["decay_w"] / j.groupby("order_id")["decay_w"].transform("sum")
by_ch = (j.assign(linear=j["amount"] * j["lin_w"], time_decay=j["amount"] * j["dec_w"])
           .groupby("channel", as_index=False)[["linear", "time_decay"]].sum())
unatt = o.loc[~o["order_id"].isin(j["order_id"]), "amount"].sum()
pd_df = pd.concat([by_ch, pd.DataFrame({"channel": ["unattributed"], "linear": [unatt], "time_decay": [unatt]})],
                  ignore_index=True).sort_values("channel").reset_index(drop=True)
pd_df[["linear", "time_decay"]] = pd_df[["linear", "time_decay"]].round(4)
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # both sorted by channel
assert abs(pd_df["linear"].sum() - total) < 1e-6 and abs(pd_df["time_decay"].sum() - total) < 1e-6
print("order 1 time-decay weights:", j[j["order_id"].eq(1)][["channel", "age_days", "dec_w"]].round(4).to_dict("records"))
print("asserts passed")
