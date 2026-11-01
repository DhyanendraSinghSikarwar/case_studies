# Q20: gaps larger than one day between consecutive logins, and the longest break per user
import sqlite3
import datetime as dt
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-10'),(1,'2024-03-04'),(1,'2024-03-01'),(1,'2024-03-04'),(1,'2024-03-02'),
 (2,'2024-03-05'),
 (3,'2024-03-03'),(3,'2024-03-01'),(3,'2024-03-02'),
 (4,'2024-03-01'),(4,NULL),(4,'2024-03-03');
"""
SQL_GAPS = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
)
SELECT user_id,
       date(login_date, '+1 day') AS gap_start,
       date(next_date, '-1 day') AS gap_end,
       CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
FROM x
WHERE julianday(next_date) - julianday(login_date) > 1
ORDER BY user_id, gap_start
"""
SQL_LONGEST = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
), x AS (
  SELECT user_id, login_date,
         LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date
  FROM d
), gaps AS (
  SELECT user_id, CAST(ROUND(julianday(next_date) - julianday(login_date)) AS INTEGER) - 1 AS days_missing
  FROM x
  WHERE julianday(next_date) - julianday(login_date) > 1
)
SELECT u.user_id, COALESCE(MAX(g.days_missing), 0) AS longest_break_days
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN gaps g ON g.user_id = u.user_id
GROUP BY u.user_id
ORDER BY u.user_id
"""
SQL_DETAIL = """
SELECT user_id, login_date,
       LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_date,
       julianday(LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date)) - julianday(login_date) AS diff_days
FROM (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL)
ORDER BY user_id, login_date
"""
# no dedupe, to see what duplicates do
SQL_NODEDUP = SQL_GAPS.replace("SELECT DISTINCT user_id, login_date", "SELECT user_id, login_date")
assert SQL_NODEDUP != SQL_GAPS

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("LEAD detail (diff_days is NULL on each user's last row):"); print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
a = pd.read_sql_query(SQL_GAPS, con)
print("gaps:"); print(a.to_string(index=False))
l = pd.read_sql_query(SQL_LONGEST, con)
print("longest break (most missing days in a row between two logins; 0 if none):"); print(l.to_string(index=False))
nd = pd.read_sql_query(SQL_NODEDUP, con)
print("without DISTINCT the gap rows are the same as with it:", nd.equals(a))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
d = logins.dropna(subset=["login_date"]).copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.drop_duplicates().sort_values(["user_id", "login_date"]).reset_index(drop=True)
d["next_date"] = d.groupby("user_id")["login_date"].shift(-1)
d["diff_days"] = (d["next_date"] - d["login_date"]).dt.days
g = d[d["diff_days"] > 1]
gaps = pd.DataFrame({
    "user_id": g["user_id"],
    "gap_start": (g["login_date"] + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "gap_end": (g["next_date"] - pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "days_missing": (g["diff_days"] - 1).astype(int),
}).reset_index(drop=True)
longest = (gaps.groupby("user_id")["days_missing"].max()
               .reindex(logins["user_id"].drop_duplicates().sort_values()).fillna(0).astype(int)
               .rename("longest_break_days").reset_index())
# pd:end
pd.testing.assert_frame_equal(gaps, a, check_dtype=False)        # ordered by user_id, gap_start
pd.testing.assert_frame_equal(longest, l, check_dtype=False)     # ordered by user_id
print("pandas equals SQL for gaps and longest break: True")

# julianday on whole dates: exact? compare with unixepoch over 20000 date pairs
rows, base = [], dt.date(2000, 1, 1)
for i in range(20000):
    x = base + dt.timedelta(days=i * 3)
    y = x + dt.timedelta(days=1 + i % 400)
    rows.append((x.isoformat(), y.isoformat()))
con.execute("CREATE TABLE pairs(a TEXT, b TEXT)")
con.executemany("INSERT INTO pairs VALUES (?, ?)", rows)
print(con.execute("SELECT COUNT(*), SUM(julianday(b) - julianday(a) = CAST(julianday(b) - julianday(a) AS INTEGER)), "
                  "SUM((unixepoch(b) - unixepoch(a)) % 86400 = 0), "
                  "SUM(julianday(b) - julianday(a) = (unixepoch(b) - unixepoch(a)) / 86400) FROM pairs").fetchone(),
      "<- pairs, julianday diff is a whole number, unixepoch diff is whole days, the two agree")
print("asserts passed")
