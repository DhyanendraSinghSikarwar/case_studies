# Q8: duplicate dates break date minus ROW_NUMBER; fix with DISTINCT or DENSE_RANK + COUNT(DISTINCT)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-02'),(2,'2024-03-01'),(2,'2024-03-03'),(2,'2024-03-01'),
 (3,'2024-03-13'),(3,'2024-03-10'),(3,'2024-03-13'),(3,'2024-03-11'),
 (4,'2024-03-09'),(4,'2024-03-09');
"""
SQL_WRONG = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_DENSE_COUNT_STAR = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - DENSE_RANK() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_DISTINCT = """
WITH d AS (
  SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_DENSE = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date) - DENSE_RANK() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
  WHERE login_date IS NOT NULL
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end,
       COUNT(DISTINCT login_date) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda sql: pd.read_sql_query(sql, con)
wrong, dense_star, fix1, fix2 = q(SQL_WRONG), q(SQL_DENSE_COUNT_STAR), q(SQL_DISTINCT), q(SQL_DENSE)
for title, df in [("WRONG: ROW_NUMBER on duplicate rows", wrong),
                  ("WRONG: DENSE_RANK but COUNT(*)", dense_star),
                  ("FIX 1: DISTINCT first", fix1),
                  ("FIX 2: DENSE_RANK + COUNT(DISTINCT login_date)", fix2)]:
    print(title); print(df.to_string(index=False)); print()
pd.testing.assert_frame_equal(fix1, fix2)
assert not wrong.equals(fix1) and not dense_star.equals(fix1)
print("fix 1 equals fix 2: True; both wrong versions differ from the fixed result: True")
print("user 1, wrong vs fixed:", wrong[wrong.user_id == 1][["streak_start", "streak_end", "streak_days"]].values.tolist(),
      "vs", fix1[fix1.user_id == 1][["streak_start", "streak_end", "streak_days"]].values.tolist())

logins = pd.read_sql_query("SELECT * FROM logins", con)
def streaks(frame, mode):
    f = frame.dropna(subset=["login_date"]).assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
    f = f.sort_values(["user_id", "login_date"])
    if mode == "row_number":
        rn = f.groupby("user_id").cumcount() + 1
    else:
        rn = f.groupby("user_id")["login_date"].rank(method="dense").astype("int64")
    f["key"] = f["login_date"] - pd.to_timedelta(rn, unit="D")
    return f
# pd:main
d = logins.dropna(subset=["login_date"]).drop_duplicates()
d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["user_id", "login_date"])
d["key"] = d["login_date"] - pd.to_timedelta(d.groupby("user_id").cumcount() + 1, unit="D")
pd_df = (d.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "nunique"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
# pd:end
pd_df["streak_start"] = pd_df["streak_start"].dt.strftime("%Y-%m-%d")
pd_df["streak_end"] = pd_df["streak_end"].dt.strftime("%Y-%m-%d")
# compared after sorting by user_id, streak_start, streak_end
pd.testing.assert_frame_equal(pd_df, fix1)
print("pandas (drop_duplicates first) equals the fixed SQL: True")

# pandas without the fix reproduces the SQL bug; dense rank in pandas fixes it
f = streaks(logins, "row_number")
bug = f.groupby(["user_id", "key"]).agg(streak_days=("login_date", "size")).reset_index()
print("pandas without drop_duplicates, user 1 row counts per island:", bug[bug.user_id == 1]["streak_days"].tolist())
g = streaks(logins, "dense")
dd = (g.groupby(["user_id", "key"]).agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"),
      streak_days=("login_date", "nunique")).reset_index().drop(columns="key")
      .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
dd["streak_start"] = dd["streak_start"].dt.strftime("%Y-%m-%d")
dd["streak_end"] = dd["streak_end"].dt.strftime("%Y-%m-%d")
pd.testing.assert_frame_equal(dd, fix1)
print("pandas rank(method='dense') + nunique equals the fixed SQL: True")
print("rank returns dtype:", logins.assign(login_date=pd.to_datetime(logins["login_date"])).groupby("user_id")["login_date"].rank(method="dense").dtype)

# NULL date: DENSE_RANK variant without the filter, single-row and exact-threshold checks
con.execute("INSERT INTO logins VALUES (4, NULL)")
print("NULL date, DENSE version unfiltered:", con.execute(SQL_DENSE.replace("  WHERE login_date IS NOT NULL\n", "")).fetchall()[-2:])
pd.testing.assert_frame_equal(q(SQL_DENSE), fix1)
print("NULL date, filtered versions unchanged: True")
con.execute("DELETE FROM logins")
print("empty table:", len(con.execute(SQL_DISTINCT).fetchall()), "rows")
print("asserts passed")
