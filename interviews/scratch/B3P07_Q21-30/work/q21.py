# Q21: streaks per user from one island CTE (count, average, longest, at least 3), with duplicates, NULLs, unsorted input
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-01-08'),(1,'2024-01-01'),(1,'2024-01-03'),(1,'2024-01-02'),(1,'2024-01-05'),(1,'2024-01-07'),
 (2,'2024-01-01'),(2,'2024-01-02'),(2,'2024-01-03'),(2,'2024-01-03'),
 (3,'2024-01-10'),
 (4,'2024-01-20'),(4,'2024-01-21'),(4,'2024-01-22'),(4,'2024-01-23'),
 (5,NULL);
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), n AS (
  SELECT user_id, login_date,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
  FROM d
), isl AS (
  SELECT user_id,
         date(login_date, '-' || rn || ' days') AS island_key,
         COUNT(*) AS len
  FROM n
  GROUP BY user_id, island_key
)
SELECT user_id,
       COUNT(*) AS streaks,
       ROUND(AVG(len), 2) AS avg_len,
       MAX(len) AS longest,
       SUM(len >= 3) AS streaks_3plus
FROM isl
GROUP BY user_id
ORDER BY user_id
"""
SQL_KEYS = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL),
n AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM d)
SELECT user_id, login_date, rn, date(login_date, '-' || rn || ' days') AS island_key
FROM n ORDER BY user_id, login_date
"""
SQL_WRONG_KEYONLY = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL),
n AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM d),
isl AS (SELECT date(login_date, '-' || rn || ' days') AS island_key, COUNT(*) AS len, COUNT(DISTINCT user_id) AS users_merged
        FROM n GROUP BY island_key)
SELECT island_key, len, users_merged FROM isl ORDER BY island_key
"""
SQL_WRONG_DISTINCT = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL),
n AS (SELECT user_id, login_date, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn FROM d)
SELECT COUNT(DISTINCT date(login_date, '-' || rn || ' days')) AS distinct_keys_all_users,
       (SELECT COUNT(*) FROM (SELECT DISTINCT user_id, date(login_date, '-' || rn || ' days') FROM n)) AS true_streaks_all_users
FROM n
"""
SQL_NODEDUP = """
WITH n AS (
  SELECT user_id, login_date,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
  FROM logins WHERE login_date IS NOT NULL
)
SELECT user_id, COUNT(DISTINCT date(login_date, '-' || rn || ' days')) AS keys_without_dedupe
FROM n GROUP BY user_id ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer:")
print(sql_df.to_string(index=False))
print("island keys per login (user 1 and user 2 share the key 2023-12-31):")
print(pd.read_sql_query(SQL_KEYS, con).to_string(index=False))
print("wrong 1, island grouped by key only:")
print(pd.read_sql_query(SQL_WRONG_KEYONLY, con).to_string(index=False))
print("wrong 2, COUNT(DISTINCT key) over all users:")
print(pd.read_sql_query(SQL_WRONG_DISTINCT, con).to_string(index=False))
print("wrong 3, no DISTINCT on (user, date), user 2 has a duplicate date:")
print(pd.read_sql_query(SQL_NODEDUP, con).to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
d = logins.dropna(subset=["login_date"]).drop_duplicates()
d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["user_id", "login_date"])
d["rn"] = d.groupby("user_id").cumcount() + 1
d["island_key"] = d["login_date"] - pd.to_timedelta(d["rn"], unit="D")
isl = d.groupby(["user_id", "island_key"]).size().rename("len").reset_index()
pd_df = (isl.groupby("user_id")["len"]
            .agg(streaks="size", avg_len="mean", longest="max", streaks_3plus=lambda s: int((s >= 3).sum()))
            .round(2).reset_index())
# pd:end
print("pandas answer:")
print(pd_df.to_string(index=False))
a = sql_df.sort_values("user_id").reset_index(drop=True)
b = pd_df.sort_values("user_id").reset_index(drop=True)
pd.testing.assert_frame_equal(a, b, check_dtype=False)  # compared after sorting both by user_id

# edge: a user with no logins at all (or only a NULL date, user 5) has no row; join from users to get 0
print("user 5 (only a NULL date) in result:", 5 in set(sql_df["user_id"]))

# day numbers: julianday (float) versus unixepoch (integer seconds) over a recursive-CTE date spine of 40001 consecutive days
chk = con.execute("""
WITH RECURSIVE sp(d) AS (SELECT '1900-01-01' UNION ALL SELECT date(d, '+1 day') FROM sp WHERE d < '2009-06-16'),
n AS (SELECT d, ROW_NUMBER() OVER (ORDER BY d) AS rn FROM sp)
SELECT COUNT(*), MIN(d), MAX(d),
       COUNT(DISTINCT julianday(d) - rn),
       COUNT(DISTINCT CAST(julianday(d) AS INTEGER) - rn),
       COUNT(DISTINCT date(d, '-' || rn || ' days'))
FROM n""").fetchone()
print("spine rows, first, last, distinct keys by julianday(d)-rn, by CAST(julianday) - rn, by date(d, -rn days):", chk)
print("asserts passed")
