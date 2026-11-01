# Q7: longest streak per user with dates, tie rule most recent (days DESC, streak_end DESC)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-11'),(1,'2024-03-01'),(1,'2024-03-10'),(1,'2024-03-02'),(1,'2024-03-12'),(1,'2024-03-03'),(1,'2024-03-06'),
 (2,'2024-04-05'),(2,'2024-04-01'),(2,'2024-04-02'),(2,'2024-04-03'),(2,'2024-04-04'),(2,'2024-04-20'),(2,'2024-04-21'),
 (3,'2024-05-09'),
 (4,'2024-06-01'),(4,'2024-06-02'),(4,'2024-06-05'),(4,'2024-06-06');
CREATE TABLE users(user_id INTEGER);
INSERT INTO users VALUES (1),(2),(3),(4),(5);
"""
ISLANDS = """
WITH d AS (
  SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
),
s AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
  FROM x
  GROUP BY user_id, grp
)
"""
SQL_ALL = ISLANDS + "SELECT * FROM s ORDER BY user_id, streak_start"
SQL_RANK_ONE = """
, r AS (
  SELECT user_id, streak_start, streak_end, days,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, streak_end DESC) AS rn
  FROM s
)
SELECT user_id, streak_start, streak_end, days
FROM r
WHERE rn = 1
ORDER BY user_id
"""
SQL_MAIN = ISLANDS + SQL_RANK_ONE
SQL_RANK_TIES = """
, r AS (
  SELECT user_id, streak_start, streak_end, days,
         RANK() OVER (PARTITION BY user_id ORDER BY days DESC) AS rk
  FROM s
)
SELECT user_id, streak_start, streak_end, days
FROM r
WHERE rk = 1
ORDER BY user_id, streak_start
"""
SQL_BOTH = ISLANDS + SQL_RANK_TIES
SQL_MAX_ONLY = ISLANDS + "SELECT user_id, MAX(days) AS days FROM s GROUP BY user_id ORDER BY user_id"
SQL_ZERO = ISLANDS + """
, r AS (
  SELECT user_id, days,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, streak_end DESC) AS rn
  FROM s
)
SELECT u.user_id, COALESCE(r.days, 0) AS days
FROM users u LEFT JOIN r ON r.user_id = u.user_id AND r.rn = 1
ORDER BY u.user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
show = lambda sql: print(pd.read_sql_query(sql, con).to_string(index=False))
print("all streaks:"); show(SQL_ALL)
print("\nlongest per user, tie -> most recent (ROW_NUMBER):"); show(SQL_MAIN)
print("\nlongest per user, ties kept (RANK):"); show(SQL_BOTH)
print("\nMAX(days) grouped, dates lost:"); show(SQL_MAX_ONLY)
print("\nusers with no logins via LEFT JOIN + COALESCE:"); show(SQL_ZERO)
print("\nSQLite bare-column quirk (not standard, tie is arbitrary), MAX(days) with streak_start:")
show(ISLANDS + "SELECT user_id, MAX(days) AS days, streak_start FROM s GROUP BY user_id ORDER BY user_id")
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_both = pd.read_sql_query(SQL_BOTH, con)

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
l = (logins.dropna(subset=["login_date"]).drop_duplicates()
           .assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
           .sort_values(["user_id", "login_date"]))
l["key"] = l["login_date"] - pd.to_timedelta(l.groupby("user_id").cumcount() + 1, unit="D")
st = (l.groupby(["user_id", "key"])
        .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), days=("login_date", "size"))
        .reset_index().drop(columns="key"))
best = (st.sort_values(["user_id", "days", "streak_end"], ascending=[True, False, False])
          .groupby("user_id").head(1).sort_values("user_id").reset_index(drop=True))
both = st[st["days"] == st.groupby("user_id")["days"].transform("max")].sort_values(["user_id", "streak_start"]).reset_index(drop=True)
# pd:end
fmt = lambda f: f.assign(streak_start=f["streak_start"].dt.strftime("%Y-%m-%d"), streak_end=f["streak_end"].dt.strftime("%Y-%m-%d"))
# compared after sorting by user_id (and streak_start for the keep-ties version)
pd.testing.assert_frame_equal(fmt(best), sql_df)
pd.testing.assert_frame_equal(fmt(both), sql_both)
print("\npandas most-recent-tie and keep-ties versions equal SQL: True")
print("pandas groupby max only:", st.groupby("user_id")["days"].max().to_dict())
idx = st.groupby("user_id")["days"].idxmax()
print("idxmax picks the first row among ties (stable by position), user 1 ->", st.loc[idx[1], "streak_end"].strftime("%Y-%m-%d"), "(older streak, not the most recent)")

# edge: empty and single-row
con.execute("DELETE FROM logins")
print("empty table, rows:", len(con.execute(SQL_MAIN).fetchall()), "| users LEFT JOIN:", con.execute(SQL_ZERO).fetchall())
print("asserts passed")
