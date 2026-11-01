# Q19: missing dates against a date spine (2024-03-01 to 2024-03-10), anti-join forms, compact ranges
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1),(2),(3),(4);
INSERT INTO logins VALUES
 (1,'2024-03-06'),(1,'2024-03-01'),(1,'2024-03-02'),(1,'2024-03-02'),(1,'2024-03-03'),(1,'2024-03-07'),(1,'2024-03-10'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-04'),(3,'2024-03-05'),
 (3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-08'),(3,'2024-03-09'),(3,'2024-03-10'),
 (4,'2024-03-05'),(4,'2024-02-28'),(4,'2024-03-11'),(4,NULL);
"""
SQL_LEFT = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
WHERE l.user_id IS NULL
ORDER BY u.user_id, s.d
"""
SQL_NOTEXISTS = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u
CROSS JOIN spine s
WHERE NOT EXISTS (SELECT 1 FROM logins l WHERE l.user_id = u.user_id AND l.login_date = s.d)
ORDER BY u.user_id, s.d
"""
SQL_RANGES = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
), m AS (
  SELECT u.user_id, s.d AS missing_date
  FROM users u
  CROSS JOIN spine s
  LEFT JOIN logins l ON l.user_id = u.user_id AND l.login_date = s.d
  WHERE l.user_id IS NULL
), g AS (
  SELECT user_id, missing_date,
         date(missing_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY missing_date) || ' days') AS grp
  FROM m
)
SELECT user_id, MIN(missing_date) AS range_start, MAX(missing_date) AS range_end, COUNT(*) AS days_missing
FROM g
GROUP BY user_id, grp
ORDER BY user_id, range_start
"""
# traps
SQL_NOTIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-10'
)
SELECT u.user_id, s.d AS missing_date
FROM users u CROSS JOIN spine s
WHERE s.d NOT IN (SELECT l.login_date FROM logins l WHERE l.user_id = u.user_id)
ORDER BY u.user_id, s.d
"""
SQL_USERS_FROM_LOGINS = SQL_LEFT.replace("FROM users u", "FROM (SELECT DISTINCT user_id FROM logins) u")
assert SQL_USERS_FROM_LOGINS != SQL_LEFT

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_LEFT, con)
b = pd.read_sql_query(SQL_NOTEXISTS, con)
pd.testing.assert_frame_equal(a, b)
print("missing days per user (LEFT JOIN ... IS NULL), counts:", a.groupby("user_id").size().to_dict())
print(a.groupby("user_id")["missing_date"].apply(lambda s: ",".join(x[8:] for x in s)).to_string())
print("NOT EXISTS gives the same rows: True")
r = pd.read_sql_query(SQL_RANGES, con)
print("compact missing ranges:"); print(r.to_string(index=False))
n = pd.read_sql_query(SQL_NOTIN, con)
print("NOT IN with a NULL login_date: user_ids returned =", sorted(n.user_id.unique().tolist()),
      "(user 4 has a NULL date and vanishes)")
w = pd.read_sql_query(SQL_USERS_FROM_LOGINS, con)
print("user list taken from logins: user_ids returned =", sorted(w.user_id.unique().tolist()), "(user 2 vanishes)")

logins = pd.read_sql_query("SELECT * FROM logins", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
spine = pd.date_range("2024-03-01", "2024-03-10", freq="D")
grid = pd.MultiIndex.from_product([users["user_id"], spine], names=["user_id", "d"]).to_frame(index=False)
seen = logins.dropna(subset=["login_date"]).assign(d=lambda x: pd.to_datetime(x["login_date"]))[["user_id", "d"]].drop_duplicates()
m = grid.merge(seen, on=["user_id", "d"], how="left", indicator=True)
miss = m[m["_merge"] == "left_only"][["user_id", "d"]].sort_values(["user_id", "d"]).reset_index(drop=True)
miss["grp"] = (miss["d"] - pd.Timestamp("1970-01-01")).dt.days - miss.groupby("user_id").cumcount()
ranges = (miss.groupby(["user_id", "grp"], as_index=False)
              .agg(range_start=("d", "min"), range_end=("d", "max"), days_missing=("d", "size"))
              .drop(columns="grp"))
# pd:end
p_miss = miss.assign(missing_date=miss["d"].dt.strftime("%Y-%m-%d"))[["user_id", "missing_date"]]
pd.testing.assert_frame_equal(p_miss, a, check_dtype=False)   # ordered by user_id, missing_date
for c in ("range_start", "range_end"):
    ranges[c] = ranges[c].dt.strftime("%Y-%m-%d")
pd.testing.assert_frame_equal(ranges.sort_values(["user_id", "range_start"]).reset_index(drop=True), r, check_dtype=False)
print("pandas equals SQL (missing days ordered by user_id, missing_date; ranges by user_id, range_start): True")
print("asserts passed")
