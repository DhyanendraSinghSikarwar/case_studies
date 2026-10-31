# Q15: current streak as of a fixed date (2024-03-20), two rules, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-20'),
 (2,'2024-03-17'),(2,'2024-03-18'),
 (3,'2024-03-20'),(3,'2024-03-02'),(3,'2024-03-01'),(3,'2024-03-03'),(3,'2024-03-04'),
 (3,'2024-03-05'),(3,'2024-03-06'),(3,'2024-03-07'),(3,'2024-03-19'),(3,'2024-03-20'),
 (4,'2024-03-19'),(4,'2024-03-17'),(4,'2024-03-18'),
 (5,'2024-03-22'),(5,'2024-03-19'),(5,'2024-03-20'),(5,'2024-03-21'),
 (6,NULL);
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'
), r AS (
  SELECT user_id, login_date,
         date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp
  FROM d
), isl AS (
  SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
  FROM r
  GROUP BY user_id, grp
)
SELECT u.user_id, COALESCE(i.streak_days, 0) AS current_streak
FROM (SELECT DISTINCT user_id FROM logins) u
LEFT JOIN isl i
  ON i.user_id = u.user_id
 AND i.streak_end >= date('2024-03-20', '-1 day')
ORDER BY u.user_id
"""
# other rule: the streak must end ON the as-of date
SQL_STRICT = SQL_MAIN.replace("i.streak_end >= date('2024-03-20', '-1 day')", "i.streak_end = '2024-03-20'")
assert SQL_STRICT != SQL_MAIN
# wrong 1: no cut-off on the as-of date (future rows counted)
SQL_NOCUT = SQL_MAIN.replace(" AND login_date <= '2024-03-20'", "")
assert SQL_NOCUT != SQL_MAIN
# wrong 2: report the longest island instead of the current one
SQL_LONGEST = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'),
r AS (SELECT user_id, login_date,
      date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp FROM d)
SELECT user_id, MAX(n) AS longest_streak FROM (SELECT user_id, grp, COUNT(*) AS n FROM r GROUP BY user_id, grp)
GROUP BY user_id ORDER BY user_id
"""
SQL_ISLANDS = """
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins WHERE login_date IS NOT NULL AND login_date <= '2024-03-20'),
r AS (SELECT user_id, login_date,
      date(login_date, '-' || ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) || ' days') AS grp FROM d)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS streak_days
FROM r GROUP BY user_id, grp ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("islands up to the as-of date:"); print(pd.read_sql_query(SQL_ISLANDS, con).to_string(index=False))
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_STRICT, con)
c = pd.read_sql_query(SQL_NOCUT, con)
l = pd.read_sql_query(SQL_LONGEST, con)
cmp_ = a.rename(columns={"current_streak": "end_asof_or_day_before"}).assign(
    end_on_asof_only=b["current_streak"], wrong_no_cutoff=c["current_streak"],
    wrong_longest=l.set_index("user_id")["longest_streak"].reindex(a["user_id"]).fillna(0).astype(int).values)
print("current streak as of 2024-03-20:"); print(cmp_.to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
AS_OF = pd.Timestamp("2024-03-20")

def current_streak(logins, as_of, rule_a=True):
    # pd:main
    users = logins["user_id"].drop_duplicates()
    d = logins.dropna(subset=["login_date"]).copy()
    d["login_date"] = pd.to_datetime(d["login_date"])
    d = d[d["login_date"] <= as_of].drop_duplicates().sort_values(["user_id", "login_date"])
    d["key"] = (d["login_date"] - pd.Timestamp("1970-01-01")).dt.days - d.groupby("user_id").cumcount()
    isl = d.groupby(["user_id", "key"], as_index=False).agg(
        streak_end=("login_date", "max"), streak_days=("login_date", "size"))
    cutoff = as_of - pd.Timedelta(days=1) if rule_a else as_of
    cur = isl[isl["streak_end"] >= cutoff].set_index("user_id")["streak_days"]
    out = cur.reindex(users).fillna(0).astype(int).rename("current_streak").reset_index()
    # pd:end
    return out.sort_values("user_id").reset_index(drop=True)

pa = current_streak(logins, AS_OF, True)
pb = current_streak(logins, AS_OF, False)
pd.testing.assert_frame_equal(pa, a, check_dtype=False)   # ordered by user_id
pd.testing.assert_frame_equal(pb, b, check_dtype=False)
print("pandas equals SQL for both rules (ordered by user_id): True")

# different as-of date, same data: 2024-03-08 (user 3's long streak just ended on 03-07)
print("rule A as of 2024-03-08:", dict(zip(*[current_streak(logins, pd.Timestamp('2024-03-08'), True)[k] for k in ('user_id','current_streak')])))
print("asserts passed")
