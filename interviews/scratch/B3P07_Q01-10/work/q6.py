# Q6: consecutive-day login streaks per user (date minus ROW_NUMBER with julianday) + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-07'),(1,'2024-03-02'),(1,'2024-03-01'),(1,'2024-03-09'),(1,'2024-03-08'),(1,'2024-03-04'),
 (2,'2024-03-15'),
 (3,'2025-01-02'),(3,'2024-12-30'),(3,'2025-01-01'),(3,'2024-12-31'),
 (4,'2024-03-01'),(4,'2024-02-28'),(4,'2024-02-29');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
),
x AS (
  SELECT user_id, login_date,
         julianday(login_date)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM d
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS streak_days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start
"""
SQL_INT_KEY = SQL_MAIN.replace(
    "julianday(login_date)\n           - ROW_NUMBER()",
    "CAST(julianday(login_date) AS INTEGER)\n           - ROW_NUMBER()")
SQL_STRING_KEY = SQL_MAIN.replace(
    "julianday(login_date)\n           - ROW_NUMBER()",
    "CAST(strftime('%Y%m%d', login_date) AS INTEGER)\n           - ROW_NUMBER()")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
assert SQL_INT_KEY != SQL_MAIN and SQL_STRING_KEY != SQL_MAIN
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("streaks (SQL):")
print(sql_df.to_string(index=False))
pd.testing.assert_frame_equal(pd.read_sql_query(SQL_INT_KEY, con), sql_df)
print("integer day-number key gives the same streaks: True")
bad = pd.read_sql_query(SQL_STRING_KEY, con)
print("\nyyyymmdd-style key, wrong at month ends (users 3 and 4):")
print(bad.query("user_id in (3, 4)").to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
l = (logins.dropna(subset=["login_date"]).drop_duplicates()
           .assign(login_date=lambda t: pd.to_datetime(t["login_date"]))
           .sort_values(["user_id", "login_date"]))
l["key"] = l["login_date"] - pd.to_timedelta(l.groupby("user_id").cumcount() + 1, unit="D")
pd_df = (l.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), streak_days=("login_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start"]).reset_index(drop=True))
# pd:end
for c in ("streak_start", "streak_end"):
    pd_df[c] = pd_df[c].dt.strftime("%Y-%m-%d")
# compared after sorting by user_id, streak_start
pd.testing.assert_frame_equal(pd_df, sql_df)
print("\npandas equals SQL: True")

# second pandas idiom: new streak when the day step is not exactly one day
step = l.groupby("user_id")["login_date"].diff()
new = step != pd.Timedelta(days=1)
sid = new.groupby(l["user_id"]).cumsum()
alt = l.groupby(["user_id", sid]).agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"),
        streak_days=("login_date", "size")).reset_index(level=0).reset_index(drop=True)
alt["streak_start"] = alt["streak_start"].dt.strftime("%Y-%m-%d")
alt["streak_end"] = alt["streak_end"].dt.strftime("%Y-%m-%d")
pd.testing.assert_frame_equal(alt, sql_df)
print("diff() != 1 day version equals SQL: True")

# exact-threshold gap and single login
print("user 1 steps in days:", [int(x.days) if pd.notna(x) else None for x in step[l["user_id"] == 1]])
print("single-login user 2:", sql_df[sql_df.user_id == 2].to_dict("records"))

# timestamps instead of dates: julianday is fractional, date() fixes it
con.executescript("""
CREATE TABLE lt(user_id INTEGER, login_date TEXT);
INSERT INTO lt VALUES (7,'2024-03-01 09:00:00'),(7,'2024-03-02 08:00:00'),(7,'2024-03-03 23:30:00');
""")
print("\ntimestamps, julianday key on raw text:", con.execute(SQL_MAIN.replace("FROM logins", "FROM lt")).fetchall())
fixed = SQL_MAIN.replace("SELECT DISTINCT user_id, login_date\n  FROM logins", "SELECT DISTINCT user_id, date(login_date) AS login_date\n  FROM lt")
print("timestamps, date() first:", con.execute(fixed).fetchall())
print("non-ISO text: julianday('2024-1-6') =", con.execute("SELECT julianday('2024-1-6')").fetchone()[0])

# duplicates and NULL and empty
con.executescript("INSERT INTO logins VALUES (1,'2024-03-02'),(2,NULL);")
pd.testing.assert_frame_equal(pd.read_sql_query(SQL_MAIN, con), sql_df)
print("duplicate day and NULL date added: SQL result unchanged (DISTINCT and IS NOT NULL in the CTE)")
con.execute("DELETE FROM logins")
print("empty table rows:", len(con.execute(SQL_MAIN).fetchall()))
print("asserts passed")
