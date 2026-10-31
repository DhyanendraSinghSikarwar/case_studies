# Q14: pandas streaks per user: translate date-minus-ROW_NUMBER to pandas, two keys, global diff leak
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-03'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-05'),
 (2,'2024-03-07'),(2,'2024-03-06'),(2,'2024-03-10'),(2,NULL),
 (3,'2024-03-09'),
 (4,'2024-03-04'),(4,'2024-03-05');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r
GROUP BY user_id, grp
ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_res = pd.read_sql_query(SQL_MAIN, con)
print("SQL streaks:"); print(sql_res.to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)

# pd:main
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
# key 1: a new streak starts when the gap to the previous login of the SAME user is not 1 day
gap_days = d.groupby("user_id")["login_date"].diff().dt.days
d["key1"] = (gap_days != 1).groupby(d["user_id"]).cumsum()
# key 2: day number minus position inside the user's list is constant on a streak
daynum = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days
d["key2"] = daynum - d.groupby("user_id").cumcount()
res1 = d.groupby(["user_id", "key1"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
res2 = d.groupby(["user_id", "key2"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
# pd:end
def fmt(r):
    r = r[["user_id", "streak_start", "streak_end", "streak_days"]].copy()
    for c in ("streak_start", "streak_end"):
        r[c] = r[c].dt.strftime("%Y-%m-%d")
    return r.sort_values(["user_id", "streak_start"]).reset_index(drop=True)
p1, p2 = fmt(res1), fmt(res2)
print("pandas key1 (groupby diff):"); print(p1.to_string(index=False))
pd.testing.assert_frame_equal(p1, sql_res, check_dtype=False)
pd.testing.assert_frame_equal(p2, sql_res, check_dtype=False)  # rows ordered by user_id, streak_start
print("both pandas keys equal the SQL result (ordered by user_id, streak_start): True")
print("gap_days dtype:", gap_days.dtype, "| first values:", gap_days.head(4).tolist())
print("NaN != 1 ->", float("nan") != 1)

# wrong: global diff (no groupby) and grouping on the key alone
gd = d["login_date"].diff().dt.days
d["wrong_key"] = (gd != 1).cumsum()
leak_alone = d.groupby("wrong_key", as_index=False).agg(
    user_id=("user_id", "first"), streak_start=("login_date", "min"),
    streak_end=("login_date", "max"), streak_days=("login_date", "size"), users=("user_id", "nunique"))
print("global diff, grouped by the key only (users column = distinct users inside the group):")
print(leak_alone.assign(streak_start=leak_alone.streak_start.dt.strftime("%Y-%m-%d"),
                        streak_end=leak_alone.streak_end.dt.strftime("%Y-%m-%d"))
      .drop(columns="wrong_key").to_string(index=False))
same_by_luck = d.groupby(["user_id", "wrong_key"], as_index=False).agg(
    streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
print("global diff but grouped by (user_id, key) equals the right answer:",
      fmt(same_by_luck).equals(sql_res))

print("asserts passed")
