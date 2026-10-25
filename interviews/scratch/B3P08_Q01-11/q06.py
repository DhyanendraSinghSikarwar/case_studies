# Q6: LeetCode 1633 Percentage of Users Attended a Contest, SQL and pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, user_name TEXT);
CREATE TABLE register(contest_id INTEGER, user_id INTEGER);
CREATE TABLE contests(contest_id INTEGER PRIMARY KEY);
INSERT INTO users VALUES (1,'A'),(2,'B'),(3,'C'),(4,'D'),(5,'E'),(6,'F'),(7,'G'),(8,'H');
INSERT INTO register VALUES
 (100,1),(100,2),(100,3),(100,4),(100,1),
 (200,2),(200,3),
 (300,5),(300,6),(300,7),
 (400,1),(400,2),(400,3),(400,4);
INSERT INTO contests VALUES (100),(200),(300),(400),(500);
"""
SQL_MAIN = """
SELECT contest_id,
       ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM users), 2) AS percentage
FROM register
GROUP BY contest_id
ORDER BY percentage DESC, contest_id
"""
SQL_COUNT_ROWS = """
SELECT contest_id, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM users), 2) AS percentage
FROM register GROUP BY contest_id ORDER BY percentage DESC, contest_id
"""
SQL_WRONG_DENOM = """
SELECT contest_id, ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM register), 2) AS percentage
FROM register GROUP BY contest_id ORDER BY percentage DESC, contest_id
"""
SQL_INT_DIV = """
SELECT contest_id, COUNT(DISTINCT user_id) * 100 / (SELECT COUNT(*) FROM users) AS percentage
FROM register GROUP BY contest_id ORDER BY percentage DESC, contest_id
"""
SQL_WITH_CONTESTS = """
SELECT c.contest_id,
       ROUND(100.0 * COUNT(DISTINCT r.user_id) / (SELECT COUNT(*) FROM users), 2) AS percentage
FROM contests c LEFT JOIN register r ON r.contest_id = c.contest_id
GROUP BY c.contest_id
ORDER BY percentage DESC, c.contest_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main:"); print(sql_df.to_string(index=False))
print("COUNT(*) with a duplicate row:", con.execute(SQL_COUNT_ROWS).fetchall())
print("denominator = register rows:", con.execute(SQL_WRONG_DENOM).fetchall())
print("integer division:", con.execute(SQL_INT_DIV).fetchall())
print("with a contests table:", con.execute(SQL_WITH_CONTESTS).fetchall())
print("SQLite 3/2 =", con.execute("SELECT 3/2, 3/2.0, 3*1.0/2").fetchone())

users = pd.read_sql_query("SELECT * FROM users", con)
register = pd.read_sql_query("SELECT * FROM register", con)
# pd:main
n_users = users["user_id"].nunique()
pd_df = (register.groupby("contest_id")["user_id"].nunique().mul(100).div(n_users).round(2)
         .rename("percentage").reset_index()
         .sort_values(["percentage", "contest_id"], ascending=[False, True], kind="stable")
         .reset_index(drop=True))
# pd:end
print("pandas:"); print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # both ordered by percentage desc, contest_id asc
print("asserts passed")
# rounding on a tie: 100 * 1 / 16 = 6.25 percent, one decimal
print("ROUND(6.25, 1) in SQLite:", con.execute("SELECT ROUND(6.25, 1)").fetchone()[0],
      "| pandas round(1):", pd.Series([6.25]).round(1).iloc[0])
