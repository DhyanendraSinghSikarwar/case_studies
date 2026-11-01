# Q12: activation rate within 7 days of signup, mature cohorts only (as-of 2024-06-30)
import sqlite3
import pandas as pd

AS_OF = "2024-06-30"   # data is complete through the end of this day

SCHEMA = """
CREATE TABLE users(user_id INTEGER, signup_date TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (10,'2024-04-15',0),(11,'2024-04-20',0),(12,'2024-04-22',0),
 (1,'2024-05-10',0),(2,'2024-05-20',0),(3,'2024-05-25',0),(4,'2024-05-28',0),(5,'2024-05-30',1),
 (6,'2024-06-10',0),(7,'2024-06-23',0),(8,'2024-06-24',0),(9,'2024-06-29',0);
INSERT INTO events VALUES
 (10,'2024-04-16 09:00:00','create_project'),(10,'2024-04-17 09:00:00','create_project'),
 (11,'2024-04-21 09:00:00','login'),
 (12,'2024-04-22 00:00:00','create_project'),
 (1,'2024-05-10 08:00:00','create_project'),
 (2,'2024-05-27 23:59:59','create_project'),
 (3,'2024-06-02 00:00:00','create_project'),
 (4,'2024-05-27 12:00:00','create_project'),(4,'2024-05-29 12:00:00','login'),
 (5,'2024-05-31 10:00:00','create_project'),
 (6,'2024-06-13 10:00:00','create_project'),
 (7,'2024-06-25 10:00:00','login');
"""

SQL_MAIN = """
WITH cohort AS (
  SELECT u.user_id,
         strftime('%Y-%m', u.signup_date) AS signup_month,
         CASE WHEN date(u.signup_date, '+7 days') <= :as_of THEN 1 ELSE 0 END AS mature,
         CASE WHEN EXISTS (
                SELECT 1 FROM events e
                WHERE e.user_id = u.user_id
                  AND e.event_name = 'create_project'
                  AND date(e.event_ts) BETWEEN u.signup_date AND date(u.signup_date, '+7 days')
              ) THEN 1 ELSE 0 END AS activated
  FROM users u
  WHERE u.is_test = 0
)
SELECT signup_month,
       SUM(mature)                                              AS mature_users,
       SUM(mature * activated)                                  AS activated_users,
       ROUND(100.0 * SUM(mature * activated) / NULLIF(SUM(mature), 0), 1) AS activation_pct,
       SUM(1 - mature)                                          AS immature_excluded,
       ROUND(100.0 * SUM(activated) / COUNT(*), 1)              AS naive_pct_all_signups
FROM cohort
GROUP BY signup_month
ORDER BY signup_month
"""

SQL_INTDIV = """
SELECT 2 / 3 AS integer_division, 2.0 / 3 AS float_division
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": AS_OF})
print(sql_df.to_string(index=False))
print("integer division demo (2 / 3, 2.0 / 3):", con.execute(SQL_INTDIV).fetchone())

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
u = users[users["is_test"] == 0].copy()
u["signup"] = pd.to_datetime(u["signup_date"])
u["win_end"] = u["signup"] + pd.Timedelta(days=7)
e = events[events["event_name"] == "create_project"].copy()
e["day"] = pd.to_datetime(e["event_ts"]).dt.normalize()
m = u.merge(e[["user_id", "day"]], on="user_id", how="left")
m["hit"] = (m["day"] >= m["signup"]) & (m["day"] <= m["win_end"])
u["activated"] = u["user_id"].map(m.groupby("user_id")["hit"].max()).astype(int)
u["mature"] = (u["win_end"] <= pd.Timestamp(AS_OF)).astype(int)
u["act_mature"] = u["activated"] * u["mature"]
u["signup_month"] = u["signup"].dt.strftime("%Y-%m")
g = u.groupby("signup_month").agg(
    mature_users=("mature", "sum"),
    activated_users=("act_mature", "sum"),
    n=("user_id", "size"),
    act_all=("activated", "sum"),
)
g["activation_pct"] = (100.0 * g["activated_users"] / g["mature_users"].where(g["mature_users"] > 0)).round(1)
g["immature_excluded"] = g["n"] - g["mature_users"]
g["naive_pct_all_signups"] = (100.0 * g["act_all"] / g["n"]).round(1)
pd_df = g.reset_index()[["signup_month", "mature_users", "activated_users", "activation_pct",
                         "immature_excluded", "naive_pct_all_signups"]]
# pd:end
print(pd_df.to_string(index=False))
# compare after ordering by signup_month (both are already sorted by it)
pd.testing.assert_frame_equal(sql_df.sort_values("signup_month").reset_index(drop=True),
                              pd_df.sort_values("signup_month").reset_index(drop=True),
                              check_dtype=False)

# who is activated, user by user (the hand walk-through)
detail = u[["user_id", "signup_date", "mature", "activated"]].sort_values("user_id")
print(detail.to_string(index=False))

# edge: text comparison trap, event_ts <= '2024-06-30' would drop events later on the 30th
print("trap:", con.execute("SELECT '2024-06-30 10:00:00' <= '2024-06-30', date('2024-06-30 10:00:00') <= '2024-06-30'").fetchone())
print("asserts passed")
