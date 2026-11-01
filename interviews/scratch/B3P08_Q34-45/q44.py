# Q44: experiment contamination, first assignment only, 14-day window, excluded counts as rows, dirty versus clean
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE experiments(user_id INTEGER, arm TEXT, assigned_ts TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO experiments VALUES
 (1,'control','2024-03-01 10:00:00'),(2,'treatment','2024-03-01 10:00:00'),
 (3,'control','2024-03-01 10:00:00'),(3,'control','2024-03-03 10:00:00'),
 (4,'control','2024-03-02 10:00:00'),(4,'treatment','2024-03-04 10:00:00'),
 (5,'treatment','2024-03-02 10:00:00'),(6,'control','2024-03-02 10:00:00'),
 (7,'treatment','2024-03-02 10:00:00'),(8,'treatment','2024-03-03 10:00:00'),
 (9,'control','2024-03-20 10:00:00'),(10,'treatment','2024-03-21 10:00:00'),
 (11,'control','2024-03-05 10:00:00'),(12,'treatment','2024-03-05 10:00:00'),
 (13,'treatment','2024-03-06 10:00:00'),(13,'treatment','2024-03-07 10:00:00'),
 (14,'control','2024-03-03 10:00:00');
INSERT INTO orders VALUES
 (1,1,'2024-03-03 09:00:00',100,'completed'),(2,2,'2024-03-04 09:00:00',100,'completed'),
 (3,3,'2024-03-16 12:00:00',100,'completed'),(4,4,'2024-03-05 09:00:00',100,'completed'),
 (5,5,'2024-03-01 09:00:00',100,'completed'),(6,6,'2024-03-04 09:00:00',100,'cancelled'),
 (7,7,'2024-03-16 10:00:00',100,'completed'),(8,8,'2024-03-10 09:00:00',100,'completed'),
 (9,9,'2024-03-22 09:00:00',100,'completed'),(10,12,'2024-03-06 09:00:00',100,'completed'),
 (11,12,'2024-03-07 09:00:00',100,'completed'),(12,13,'2024-03-08 09:00:00',100,'completed');
"""
# as-of 2024-03-25: an assignment is mature when assigned_ts + 14 days <= as-of end of day 2024-03-25 00:00
SQL_MAIN = """
WITH per AS (
  SELECT user_id, COUNT(*) AS n_rows, COUNT(DISTINCT arm) AS n_arms, MIN(assigned_ts) AS first_ts
  FROM experiments GROUP BY user_id
), fa AS (
  SELECT x.user_id, x.arm, x.assigned_ts, per.n_rows, per.n_arms,
         ROW_NUMBER() OVER (PARTITION BY x.user_id ORDER BY x.assigned_ts) AS rn
  FROM experiments x JOIN per ON per.user_id = x.user_id
), f AS (
  SELECT user_id, arm, assigned_ts, n_rows, n_arms,
         CASE WHEN n_arms > 1 THEN 'both_arms'
              WHEN unixepoch(assigned_ts) + 14 * 86400 > unixepoch('2024-03-25 00:00:00') THEN 'immature'
              ELSE 'clean' END AS status
  FROM fa WHERE rn = 1
), c AS (
  SELECT f.*, EXISTS (SELECT 1 FROM orders o WHERE o.user_id = f.user_id AND o.status = 'completed'
                      AND o.order_ts >= f.assigned_ts
                      AND unixepoch(o.order_ts) < unixepoch(f.assigned_ts) + 14 * 86400) AS conv
  FROM f
)
SELECT grp, users, conversions, conv_rate FROM (
  SELECT CASE arm WHEN 'control' THEN 0 ELSE 1 END AS ord, arm AS grp, COUNT(*) AS users,
         SUM(conv) AS conversions, ROUND(1.0 * SUM(conv) / COUNT(*), 4) AS conv_rate
  FROM c WHERE status = 'clean' GROUP BY arm
  UNION ALL SELECT 2, 'excluded_both_arms', COUNT(*), NULL, NULL FROM c WHERE status = 'both_arms'
  UNION ALL SELECT 3, 'excluded_immature', COUNT(*), NULL, NULL FROM c WHERE status = 'immature'
  UNION ALL SELECT 4, 'dropped_duplicate_rows', SUM(n_rows - 1), NULL, NULL FROM c WHERE status <> 'both_arms'
) ORDER BY ord
"""
SQL_DIRTY = """
SELECT x.arm AS grp, COUNT(*) AS rows_as_users,
       SUM(EXISTS (SELECT 1 FROM orders o WHERE o.user_id = x.user_id AND o.status = 'completed'
                   AND o.order_ts >= x.assigned_ts
                   AND unixepoch(o.order_ts) < unixepoch(x.assigned_ts) + 14 * 86400)) AS conversions,
       ROUND(1.0 * SUM(EXISTS (SELECT 1 FROM orders o WHERE o.user_id = x.user_id AND o.status = 'completed'
                   AND o.order_ts >= x.assigned_ts
                   AND unixepoch(o.order_ts) < unixepoch(x.assigned_ts) + 14 * 86400)) / COUNT(*), 4) AS conv_rate
FROM experiments x GROUP BY x.arm ORDER BY x.arm
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("clean table with excluded rows:"); print(sql_df.to_string(index=False))
dirty = pd.read_sql_query(SQL_DIRTY, con)
print("no cleaning (every assignment row, immature windows included):"); print(dirty.to_string(index=False))
cl = sql_df.set_index("grp")
print("clean: absolute uplift %.4f, relative uplift %.1f%%" % (
    cl.loc["treatment", "conv_rate"] - cl.loc["control", "conv_rate"],
    100 * (cl.loc["treatment", "conv_rate"] / cl.loc["control", "conv_rate"] - 1)))
d = dirty.set_index("grp")
print("dirty: absolute uplift %.4f, relative uplift %.1f%%" % (
    d.loc["treatment", "conv_rate"] - d.loc["control", "conv_rate"],
    100 * (d.loc["treatment", "conv_rate"] / d.loc["control", "conv_rate"] - 1)))

experiments = pd.read_sql_query("SELECT * FROM experiments", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
ex = experiments.assign(ts=pd.to_datetime(experiments["assigned_ts"]))
oc = orders[orders["status"].eq("completed")].assign(ots=pd.to_datetime(orders["order_ts"]))
per = ex.groupby("user_id").agg(n_rows=("arm", "size"), n_arms=("arm", "nunique")).reset_index()
first = ex.sort_values(["user_id", "ts"], kind="stable").drop_duplicates("user_id").merge(per, on="user_id")
first["status"] = "clean"
first.loc[first["ts"] + pd.Timedelta(days=14) > pd.Timestamp("2024-03-25"), "status"] = "immature"
first.loc[first["n_arms"] > 1, "status"] = "both_arms"
def converted(frame):
    m = frame[["user_id", "ts"]].reset_index().merge(oc[["user_id", "ots"]], on="user_id", how="left")
    ok = m[(m["ots"] >= m["ts"]) & (m["ots"] < m["ts"] + pd.Timedelta(days=14))]
    return frame.index.isin(ok["index"])
first["conv"] = converted(first)
clean = first[first["status"].eq("clean")]
arm_rows = (clean.groupby("arm").agg(users=("user_id", "size"), conversions=("conv", "sum")).reset_index()
                 .rename(columns={"arm": "grp"}))
arm_rows["conv_rate"] = (arm_rows["conversions"] / arm_rows["users"]).round(4)
extra = pd.DataFrame({"grp": ["excluded_both_arms", "excluded_immature", "dropped_duplicate_rows"],
                      "users": [int(first["status"].eq("both_arms").sum()), int(first["status"].eq("immature").sum()),
                                int((first.loc[first["status"].ne("both_arms"), "n_rows"] - 1).sum())]})
pd_df = pd.concat([arm_rows, extra], ignore_index=True)
ex["conv"] = converted(ex)
pd_dirty = (ex.groupby("arm").agg(rows_as_users=("user_id", "size"), conversions=("conv", "sum")).reset_index()
              .rename(columns={"arm": "grp"}))
pd_dirty["conv_rate"] = (pd_dirty["conversions"] / pd_dirty["rows_as_users"]).round(4)
# pd:end
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)  # same fixed row order (control, treatment, excluded rows)
pd.testing.assert_frame_equal(dirty, pd_dirty, check_dtype=False)  # ordered by arm
print("asserts passed")
