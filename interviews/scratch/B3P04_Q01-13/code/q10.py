# Q10: finding duplicates with windows and GROUP BY
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO users VALUES (1,'Asha','a@x.com'),(2,'Ben','b@x.com'),(3,'Chitra','a@x.com'),
  (4,'Dev',NULL),(5,'Esha',NULL),(6,'Farid','c@x.com'),(7,'Gita','a@x.com'),(8,'Hari','A@x.com');
"""
# first copy = lowest user_id
SQL_MAIN = """
WITH w AS (
  SELECT user_id, name, email,
         COUNT(*) OVER (PARTITION BY email) AS copies,
         ROW_NUMBER() OVER (PARTITION BY email ORDER BY user_id) AS rn
  FROM users
)
SELECT user_id, name, email, copies, rn,
       CASE WHEN rn = 1 THEN 'first copy' ELSE 'extra copy' END AS flag
FROM w
WHERE copies > 1
ORDER BY user_id
"""
SQL_GROUP = """
SELECT u.user_id, u.name, u.email
FROM users u
JOIN (SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1) d
  ON u.email IS d.email
ORDER BY u.user_id
"""
SQL_GROUP_EQ = SQL_GROUP.replace("u.email IS d.email", "u.email = d.email")
SQL_COUNTCOL = """
SELECT user_id FROM (SELECT user_id, COUNT(email) OVER (PARTITION BY email) AS c FROM users)
WHERE c > 1 ORDER BY user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
grp_df = pd.read_sql_query(SQL_GROUP, con)
print(sql_df.to_string(index=False))
print("\nGROUP BY version with ON u.email IS d.email:", grp_df["user_id"].tolist())
print("same with ON u.email = d.email (NULL rows drop):", [r[0] for r in con.execute(SQL_GROUP_EQ)])
print("COUNT(email) OVER instead of COUNT(*):", [r[0] for r in con.execute(SQL_COUNTCOL)])
assert grp_df["user_id"].tolist() == sql_df["user_id"].tolist()

users = pd.read_sql_query("SELECT * FROM users ORDER BY user_id", con)
# pd:main
all_copies = users[users.duplicated(subset="email", keep=False)]
extra = users.duplicated(subset="email", keep="first")
# pd:end
pd_df = all_copies.assign(flag=extra[all_copies.index].map({True: "extra copy", False: "first copy"}))
# compared after sorting by user_id
pd.testing.assert_frame_equal(sql_df[["user_id", "name", "email", "flag"]],
                              pd_df[["user_id", "name", "email", "flag"]].sort_values("user_id").reset_index(drop=True),
                              check_dtype=False)
print("\npandas duplicated(keep=False) user_ids:", all_copies["user_id"].tolist())
print("pandas keep='first' marks as extra:", users.loc[extra, "user_id"].tolist())
print("asserts passed: window == GROUP BY join == pandas duplicated")
