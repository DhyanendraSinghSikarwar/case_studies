# Q18: the funnel in pandas, checked against SQL on the same data
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT, channel TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view','ads'),(1,'2024-03-01 10:05:00','cart','ads'),(1,'2024-03-01 10:10:00','purchase','ads'),
 (2,'2024-03-01 11:00:00','view','organic'),(2,'2024-03-01 11:30:00','cart','organic'),
 (3,'2024-03-02 09:00:00','view','ads'),(3,'2024-03-02 09:30:00','cart','ads'),(3,'2024-03-02 09:40:00','cart','ads'),
 (3,'2024-03-02 08:00:00','purchase','ads'),
 (4,'2024-03-02 10:00:00','view',NULL),(4,'2024-03-02 10:10:00','cart',NULL),(4,'2024-03-02 10:20:00','purchase',NULL),
 (5,'2024-03-03 12:00:00','view','ads'),(5,'2024-03-03 12:05:00','view','organic'),(5,'2024-03-03 12:30:00','purchase','organic'),
 (NULL,'2024-03-03 13:00:00','view','ads');
"""

SQL_STEPS = """
SELECT COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)     AS view_users,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END)     AS cart_users,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchase_users
FROM events
"""

SQL_STRICT = """
WITH t AS (
  SELECT user_id,
         MIN(CASE WHEN event_name = 'view' THEN event_ts END)     AS t_view,
         MIN(CASE WHEN event_name = 'cart' THEN event_ts END)     AS t_cart,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS t_purchase
  FROM events
  WHERE user_id IS NOT NULL
  GROUP BY user_id
)
SELECT COUNT(t_view)                                                       AS viewers,
       SUM(CASE WHEN t_cart > t_view THEN 1 ELSE 0 END)                    AS then_cart,
       SUM(CASE WHEN t_cart > t_view AND t_purchase > t_cart THEN 1 ELSE 0 END) AS then_purchase
FROM t
"""

SQL_CHANNEL = """
SELECT COALESCE(channel, 'unknown') AS channel,
       COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)     AS view,
       COUNT(DISTINCT CASE WHEN event_name = 'cart' THEN user_id END)     AS cart,
       COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchase,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END)
             / NULLIF(COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END), 0), 1) AS conv_pct
FROM events
GROUP BY COALESCE(channel, 'unknown')
ORDER BY view DESC, channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_steps = pd.read_sql_query(SQL_STEPS, con)
sql_strict = pd.read_sql_query(SQL_STRICT, con)
sql_channel = pd.read_sql_query(SQL_CHANNEL, con)
print(sql_steps.to_string(index=False)); print(sql_strict.to_string(index=False)); print(sql_channel.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)   # user_id becomes float64 because of the NULL
print(events.dtypes.to_dict())
steps = ["view", "cart", "purchase"]
ev = events.assign(event_ts=pd.to_datetime(events["event_ts"]))

# pd:steps
counts = ev.groupby("event_name")["user_id"].nunique().reindex(steps)
pd_steps = pd.DataFrame([{"view_users": counts["view"], "cart_users": counts["cart"],
                          "purchase_users": counts["purchase"]}])
# pd:end
pd.testing.assert_frame_equal(sql_steps, pd_steps, check_dtype=False)

# pd:strict
first = ev.pivot_table(index="user_id", columns="event_name", values="event_ts", aggfunc="min")
first_g = ev.groupby(["user_id", "event_name"])["event_ts"].min().unstack()   # same table, groupby form
assert first.equals(first_g.reindex(columns=first.columns))
ok_cart = first["cart"] > first["view"]
ok_purchase = ok_cart & (first["purchase"] > first["cart"])
pd_strict = pd.DataFrame([{"viewers": int(first["view"].notna().sum()),
                           "then_cart": int(ok_cart.sum()), "then_purchase": int(ok_purchase.sum())}])
# pd:end
pd.testing.assert_frame_equal(sql_strict, pd_strict, check_dtype=False)

# pd:merge
def step_first(name):
    s = ev[ev["event_name"] == name].groupby("user_id")["event_ts"].min()
    return s.rename("t_" + name).reset_index()
m1 = step_first("view").merge(step_first("cart"), on="user_id")
m1 = m1[m1["t_cart"] > m1["t_view"]]
m2 = m1.merge(step_first("purchase"), on="user_id")
m2 = m2[m2["t_purchase"] > m2["t_cart"]]
merge_counts = (step_first("view")["user_id"].nunique(), len(m1), len(m2))
# pd:end
assert merge_counts == tuple(sql_strict.iloc[0]), merge_counts

# pd:channel
ch = ev.assign(channel=ev["channel"].fillna("unknown"))
pv = ch.pivot_table(index="channel", columns="event_name", values="user_id",
                    aggfunc="nunique", fill_value=0)[steps]
pv["conv_pct"] = (100.0 * pv["purchase"] / pv["view"].where(pv["view"] > 0)).round(1)
pd_channel = (pv.reset_index().sort_values(["view", "channel"], ascending=[False, True])
                .reset_index(drop=True))
# pd:end
pd.testing.assert_frame_equal(sql_channel, pd_channel[["channel", "view", "cart", "purchase", "conv_pct"]],
                              check_dtype=False, check_names=False)
print(pd_channel.to_string(index=False))

print("--- behaviours demonstrated ---")
print("nunique skips NaN:", events["user_id"].nunique(), "| nunique(dropna=False):", events["user_id"].nunique(dropna=False),
      "| len(set(...)):", len(set(events["user_id"])))
print("groupby default drops the NaN channel:", events.groupby("channel")["user_id"].size().to_dict())
print("groupby(dropna=False) keeps it:", events.groupby("channel", dropna=False)["user_id"].size().to_dict())
print("SQL GROUP BY keeps a NULL group:", con.execute("SELECT channel, COUNT(*) FROM events GROUP BY channel ORDER BY channel").fetchall())
raw = events.pivot_table(index="channel", columns="event_name", values="user_id", aggfunc="nunique")
print("pivot_table on raw channel (default dropna=True), index:", list(raw.index))
raw2 = events.pivot_table(index="channel", columns="event_name", values="user_id", aggfunc="nunique", dropna=False)
print("pivot_table(dropna=False), index:", list(raw2.index))
trap = events.pivot_table(index="channel", columns="event_name", values="user_id")
print("pivot_table with the default aggfunc='mean' on user_id:")
print(trap.to_string())
print("merge on NaN keys matches NaN with NaN:",
      len(pd.DataFrame({"k": [1.0, np.nan]}).merge(pd.DataFrame({"k": [np.nan, 2.0]}), on="k")),
      "| SQL join on NULL keys:",
      con.execute("SELECT COUNT(*) FROM (SELECT NULL AS k) a JOIN (SELECT NULL AS k) b ON a.k = b.k").fetchone()[0])
print("total of channel view rows:", int(pd_channel["view"].sum()), "vs distinct viewers:", int(pd_steps["view_users"].iloc[0]))
print("asserts passed")
