# Q1: why date minus ROW_NUMBER identifies islands (SQLite julianday key) + pandas twin
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-05'),(1,'2024-03-01'),(1,'2024-03-03'),(1,'2024-03-06'),(1,'2024-03-02'),
 (2,'2024-03-10'),
 (3,'2025-01-02'),(3,'2024-12-30'),(3,'2025-01-01'),(3,'2024-12-31');
"""
SQL_KEYS = """
SELECT user_id, login_date,
       ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn,
       julianday(login_date) AS day_no,
       julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
FROM logins
ORDER BY user_id, login_date
"""
SQL_MAIN = """
WITH x AS (
  SELECT user_id, login_date,
         julianday(login_date)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_EPOCH = """
WITH x AS (
  SELECT user_id, login_date,
         unixepoch(login_date) / 86400
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_WRONG_TEXT = """
WITH x AS (
  SELECT user_id, login_date,
         login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""
SQL_WRONG_YMD = """
WITH x AS (
  SELECT user_id, login_date,
         CAST(strftime('%Y%m%d', login_date) AS INTEGER)
           - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS grp
  FROM logins
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
FROM x
GROUP BY user_id, grp
ORDER BY user_id, streak_start, streak_end
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("key table (day_no is julianday, grp = day_no - rn):")
print(pd.read_sql_query(SQL_KEYS, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nislands (SQL julianday):")
print(sql_df.to_string(index=False))
epoch_df = pd.read_sql_query(SQL_EPOCH, con)
pd.testing.assert_frame_equal(epoch_df, sql_df)
print("\nunixepoch/86400 integer key gives the same islands: True")
print("\nwrong 1, login_date - rn (text coerced to 2024 / 2025):")
print(pd.read_sql_query(SQL_WRONG_TEXT, con).to_string(index=False))
print("\nwrong 2, yyyymmdd - rn (breaks at month and year ends):")
print(pd.read_sql_query(SQL_WRONG_YMD, con).query("user_id == 3").to_string(index=False))

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
l = logins.assign(login_date=pd.to_datetime(logins["login_date"])).sort_values(["user_id", "login_date"])
l["rn"] = l.groupby("user_id").cumcount() + 1
l["key"] = l["login_date"] - pd.to_timedelta(l["rn"], unit="D")
pd_df = (l.groupby(["user_id", "key"])
          .agg(streak_start=("login_date", "min"), streak_end=("login_date", "max"), days=("login_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["user_id", "streak_start", "streak_end"]).reset_index(drop=True))
# pd:end
for c in ("streak_start", "streak_end"):
    pd_df[c] = pd_df[c].dt.strftime("%Y-%m-%d")
# compared after sorting by user_id, streak_start, streak_end
pd.testing.assert_frame_equal(pd_df, sql_df)
print("\npandas islands equal SQL islands: True")

# duplicates in the date column: the key splits the run
con.executescript("""
CREATE TABLE dup(user_id INTEGER, login_date TEXT);
INSERT INTO dup VALUES (9,'2024-03-01'),(9,'2024-03-01'),(9,'2024-03-02');
""")
print("\nduplicate day 03-01 (one user, run is really 2 days):")
print(pd.read_sql_query(SQL_MAIN.replace("FROM logins", "FROM dup"), con).to_string(index=False))

# NULL date and empty table
con.execute("INSERT INTO logins VALUES (2, NULL)")
print("\nwith a NULL login_date for user 2, no filter:")
print(pd.read_sql_query(SQL_MAIN, con).query("user_id == 2").to_string(index=False))
sql_null = pd.read_sql_query(SQL_MAIN.replace("FROM logins", "FROM logins WHERE login_date IS NOT NULL"), con)
pd.testing.assert_frame_equal(sql_null, sql_df)
lp = pd.read_sql_query("SELECT * FROM logins", con)
lp = lp.assign(login_date=pd.to_datetime(lp["login_date"])).sort_values(["user_id", "login_date"])
lp["rn"] = lp.groupby("user_id").cumcount() + 1
lp["key"] = lp["login_date"] - pd.to_timedelta(lp["rn"], unit="D")
g = lp.groupby(["user_id", "key"]).size()
print("pandas, NULL kept, groups for user 2:", len(g.loc[2]), "(NaT key group silently dropped)")
con.execute("DELETE FROM logins")
print("empty table, SQL rows:", len(con.execute(SQL_MAIN).fetchall()))
# precision check: float julianday key vs integer unixepoch key on timestamps (3 consecutive days, same clock time)
import random
random.seed(7)
split_jd = split_ux = trials = 0
for _ in range(2000):
    start = "%04d-%02d-%02d %02d:%02d:%02d.%03d" % (random.choice([2020, 2024, 2026]), random.randint(1, 12),
            random.randint(1, 25), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59), random.randint(0, 999))
    jd, ux = set(), set()
    for i in range(3):
        ts = con.execute("SELECT strftime('%Y-%m-%d %H:%M:%f', ?, ?)", (start, "+%d day" % i)).fetchone()[0]
        jd.add(con.execute("SELECT julianday(?) - ?", (ts, i + 1)).fetchone()[0])
        ux.add(con.execute("SELECT unixepoch(?, 'subsec') - 86400 * ?", (ts, i + 1)).fetchone()[0])
    trials += 1
    split_jd += len(jd) > 1
    split_ux += len(ux) > 1
print("timestamp trials:", trials, "| julianday key split a run:", split_jd, "| unixepoch subsec key split a run:", split_ux)
print("asserts passed")
