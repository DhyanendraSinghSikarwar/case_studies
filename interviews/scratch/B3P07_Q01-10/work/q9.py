# Q9: users with a streak of at least N days (LeetCode 1454 pattern), duplicates in logins
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE accounts(id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO accounts VALUES (1,'Alice'),(2,'Bob'),(3,'Carol'),(4,'Dan'),(5,'Eve');
CREATE TABLE logins(id INTEGER, login_date TEXT);
INSERT INTO logins VALUES
 (1,'2024-03-05'),(1,'2024-03-01'),(1,'2024-03-03'),(1,'2024-03-03'),(1,'2024-03-02'),(1,'2024-03-04'),
 (2,'2024-03-04'),(2,'2024-03-01'),(2,'2024-03-02'),(2,'2024-03-03'),(2,'2024-03-04'),
 (3,'2024-03-01'),(3,'2024-03-02'),(3,'2024-03-03'),(3,'2024-03-05'),(3,'2024-03-06'),
 (4,'2024-03-01'),(4,'2024-03-02'),(4,'2024-03-03'),(4,'2024-03-04'),(4,'2024-03-05'),(4,'2024-03-06'),
 (4,'2024-03-10'),(4,'2024-03-11'),(4,'2024-03-12'),(4,'2024-03-13'),(4,'2024-03-14'),
 (6,'2024-03-01'),(6,'2024-03-02'),(6,'2024-03-03'),(6,'2024-03-04'),(6,'2024-03-05');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT id, login_date
  FROM logins
  WHERE login_date IS NOT NULL
),
x AS (
  SELECT id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM d
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
ORDER BY a.id
"""
SQL_JOIN_DUPES = """
WITH d AS (
  SELECT DISTINCT id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM d
),
s AS (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
SELECT a.id, a.name FROM accounts a JOIN s ON s.id = a.id ORDER BY a.id
"""
SQL_NO_DISTINCT = """
WITH x AS (
  SELECT id, login_date,
         julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM logins
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
ORDER BY a.id
"""
SQL_DENSE_COUNT_STAR = """
WITH x AS (
  SELECT id, login_date,
         julianday(login_date) - DENSE_RANK() OVER (PARTITION BY id ORDER BY login_date) AS grp
  FROM logins
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x GROUP BY id, grp HAVING COUNT(*) >= ?)
ORDER BY a.id
"""
SQL_LAG = """
WITH d AS (
  SELECT DISTINCT id, login_date FROM logins WHERE login_date IS NOT NULL
),
x AS (
  SELECT id, login_date,
         LAG(login_date, ? - 1) OVER (PARTITION BY id ORDER BY login_date) AS back
  FROM d
)
SELECT a.id, a.name
FROM accounts a
WHERE a.id IN (SELECT id FROM x WHERE julianday(login_date) - julianday(back) = ? - 1)
ORDER BY a.id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def pairs(df):
    return [(int(i), n) for i, n in zip(df["id"], df["name"])]

def rows(sql, *p):
    return pd.read_sql_query(sql, con, params=p)

sql_df = rows(SQL_MAIN, 5)
print("accounts with a streak of 5+ days:")
print(sql_df.to_string(index=False))
print("\nroster of streak lengths (distinct days) per user:")
print(pd.read_sql_query("""
WITH d AS (SELECT DISTINCT id, login_date FROM logins),
x AS (SELECT id, login_date, julianday(login_date) - ROW_NUMBER() OVER (PARTITION BY id ORDER BY login_date) AS grp FROM d)
SELECT id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days FROM x GROUP BY id, grp ORDER BY id, streak_start""", con).to_string(index=False))
print("\nwrong 1, ROW_NUMBER without DISTINCT:", rows(SQL_NO_DISTINCT, 5)["id"].tolist())
print("wrong 2, DENSE_RANK but COUNT(*):", rows(SQL_DENSE_COUNT_STAR, 5)["id"].tolist())
print("join instead of IN, Dan has two qualifying streaks:", rows(SQL_JOIN_DUPES, 5)["id"].tolist())

logins = pd.read_sql_query("SELECT * FROM logins", con)
accounts = pd.read_sql_query("SELECT * FROM accounts", con)
def pd_active(logins, accounts, n):
    # pd:main
    d = logins.dropna(subset=["login_date"]).drop_duplicates()
    d = d.assign(login_date=pd.to_datetime(d["login_date"])).sort_values(["id", "login_date"])
    d["key"] = d["login_date"] - pd.to_timedelta(d.groupby("id").cumcount() + 1, unit="D")
    sizes = d.groupby(["id", "key"]).size()
    ids = sizes[sizes >= n].index.get_level_values("id").unique()
    out = accounts[accounts["id"].isin(ids)].sort_values("id").reset_index(drop=True)
    # pd:end
    return out
# compared after sorting by id
pd.testing.assert_frame_equal(pd_active(logins, accounts, 5), sql_df)
print("\npandas equals SQL for N=5: True")
for n in range(1, 8):
    a = rows(SQL_MAIN, n)
    b = pd_active(logins, accounts, n)
    c = rows(SQL_LAG, n, n)
    assert pairs(b) == pairs(a) == pairs(c)  # lists of (id, name); empty frames differ in dtype, so compare values
    print("N =", n, "-> ids", a["id"].tolist(), "(ROW_NUMBER, pandas and LAG(N-1) agree)")

# edge cases
con.execute("INSERT INTO logins VALUES (5, NULL)")
print("account with only a NULL date, N=1:", rows(SQL_MAIN, 1)["id"].tolist())
con.execute("DELETE FROM logins")
print("empty logins, N=5:", rows(SQL_MAIN, 5)["id"].tolist(), "| pandas rows:", len(pd_active(logins.iloc[0:0], accounts, 5)))
print("asserts passed")
