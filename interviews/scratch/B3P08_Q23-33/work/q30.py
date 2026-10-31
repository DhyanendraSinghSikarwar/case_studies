# Q30: pandas pivot_table, crosstab and value_counts with a NaN channel, checked against SQL GROUP BY
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_channel TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, status TEXT);
INSERT INTO users VALUES (1,'ads'),(2,'organic'),(3,'referral'),(4,'ads'),(5,'organic');
INSERT INTO orders VALUES
 (1,1,'ads','completed'),(2,1,'ads','cancelled'),(3,2,'organic','completed'),
 (4,2,'organic','completed'),(5,3,'referral','cancelled'),(6,4,NULL,'completed'),
 (7,4,NULL,'cancelled'),(8,5,NULL,'completed'),(9,3,'referral','completed'),
 (10,1,'ads','completed');
"""

SQL_COUNTS = """
SELECT COALESCE(channel, 'unknown') AS channel,
       SUM(status = 'cancelled') AS cancelled,
       SUM(status = 'completed') AS completed,
       COUNT(*) AS orders,
       ROUND(SUM(status = 'completed') * 1.0 / COUNT(*), 4) AS completed_share,
       ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM orders), 4) AS channel_mix
FROM orders
GROUP BY COALESCE(channel, 'unknown')
ORDER BY channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_COUNTS, con)
print("SQL GROUP BY (NULL channel kept as 'unknown'):")
print(sql_res.to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
users = pd.read_sql_query("SELECT * FROM users", con)
print("channel dtype:", orders["channel"].dtype, "; NaN rows:", int(orders["channel"].isna().sum()))

# (a) counts: default drops NaN keys
pv = pd.pivot_table(orders, index="channel", columns="status", values="order_id",
                    aggfunc="count", fill_value=0)
print("(a) pivot_table, default dropna=True:")
print(pv)
print("    rows kept:", int(pv.to_numpy().sum()), "of", len(orders))
# the aggfunc='mean' default trap
trap = pd.pivot_table(orders, index="channel", columns="status", values="order_id")
print("(a') pivot_table with the default aggfunc='mean' on order_id (not a count):")
print(trap)
# explicit NaN bucket
orders["channel_f"] = orders["channel"].fillna("unknown")
pv_f = pd.pivot_table(orders, index="channel_f", columns="status", values="order_id",
                      aggfunc="count", fill_value=0)
print("(a'') pivot_table after fillna('unknown'):")
print(pv_f)

# (b) crosstab row shares
ct = pd.crosstab(orders["channel"], orders["status"], normalize="index")
ct_f = pd.crosstab(orders["channel_f"], orders["status"], normalize="index")
print("(b) crosstab normalize='index', NaN channel silently absent:")
print(ct.round(4))
print("(b') crosstab after fillna('unknown'):")
print(ct_f.round(4))
ct_all = pd.crosstab(orders["channel"], orders["status"], normalize="all")
print("(b'') crosstab normalize='all' sums to", round(float(ct_all.to_numpy().sum()), 4),
      "(shares of the 7 kept rows, not of 10)")

# (c) value_counts
vc = orders["channel"].value_counts(normalize=True)
vc_na = orders["channel"].value_counts(normalize=True, dropna=False)
print("(c) value_counts(normalize=True):")
print(vc.round(4).to_string())
print("(c') value_counts(normalize=True, dropna=False):")
print(vc_na.round(4).to_string())

# assertions against SQL
pd_res = pd.DataFrame({"channel": pv_f.index, "cancelled": pv_f["cancelled"].to_numpy(),
                       "completed": pv_f["completed"].to_numpy()})
pd_res["orders"] = pd_res["cancelled"] + pd_res["completed"]
pd_res["completed_share"] = ct_f.loc[pd_res["channel"], "completed"].round(4).to_numpy()
mix = orders["channel_f"].value_counts(normalize=True, dropna=False)
pd_res["channel_mix"] = mix.loc[pd_res["channel"]].round(4).to_numpy()
# compare after sorting by channel (SQL ORDER BY channel)
pd.testing.assert_frame_equal(pd_res.sort_values("channel").reset_index(drop=True), sql_res, check_dtype=False)

# crosstab or pivot on a categorical key: observed / dropna defaults
cat = orders.assign(channel_c=pd.Categorical(orders["channel_f"],
                    categories=["ads", "organic", "referral", "unknown", "affiliate"]))
print("categorical key with an unused category 'affiliate':")
print("  pivot_table default rows:", list(pd.pivot_table(cat, index="channel_c", columns="status",
      values="order_id", aggfunc="count", fill_value=0).index))
print("  pivot_table observed=False rows:", list(pd.pivot_table(cat, index="channel_c", columns="status",
      values="order_id", aggfunc="count", fill_value=0, observed=False).index))
print("  crosstab default rows:", list(pd.crosstab(cat["channel_c"], cat["status"]).index))
print("  crosstab dropna=False rows:", list(pd.crosstab(cat["channel_c"], cat["status"], dropna=False).index))

# fallback to the signup channel through a merge
m = orders.merge(users, on="user_id", how="left")
m["channel_fb"] = m["channel"].fillna(m["signup_channel"])
print("after fallback to signup channel, NaN left:", int(m["channel_fb"].isna().sum()))
print(m["channel_fb"].value_counts().to_string())
print("asserts passed")
