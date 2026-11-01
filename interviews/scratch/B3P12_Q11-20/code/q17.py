# Q17: users within the top 2 DISTINCT post counts of their country, March 2025
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE posts(post_id INTEGER PRIMARY KEY, user_id INTEGER, created_at TEXT);
INSERT INTO users VALUES (1,'IN'),(2,'IN'),(3,'IN'),(4,'IN'),(5,'IN'),(6,'US'),(7,'US'),(8,'UK');
""")
rows = []
pid = 0
def add(u, n, ts):
    global pid
    for _ in range(n):
        pid += 1
        rows.append((pid, u, ts))
add(1, 5, "2025-03-10 10:00:00"); add(2, 3, "2025-03-11 10:00:00"); add(3, 3, "2025-03-12 10:00:00"); add(4, 3, "2025-03-31 23:59:59")
add(5, 1, "2025-03-05 10:00:00"); add(5, 2, "2025-02-27 10:00:00")
add(6, 4, "2025-03-02 10:00:00"); add(7, 2, "2025-03-03 10:00:00"); add(7, 1, "2025-04-01 00:00:00")
con.executemany("INSERT INTO posts VALUES (?,?,?)", rows)

sql = """
WITH c AS (
  SELECT u.country, u.user_id, COUNT(*) AS posts
  FROM users u JOIN posts p ON p.user_id = u.user_id
  WHERE p.created_at >= '2025-03-01' AND p.created_at < '2025-04-01'
  GROUP BY u.country, u.user_id),
r AS (SELECT *, DENSE_RANK() OVER (PARTITION BY country ORDER BY posts DESC) AS rk FROM c)
SELECT country, user_id, posts, rk FROM r WHERE rk <= 2 ORDER BY country, posts DESC, user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
print("\nwith ROW_NUMBER instead of DENSE_RANK the kept (country, user_id) would be:",
      [(r[0], r[1]) for r in con.execute(sql.replace("DENSE_RANK()", "ROW_NUMBER()"))])

u = pd.read_sql("SELECT * FROM users", con); po = pd.read_sql("SELECT * FROM posts", con)
po = po[(po.created_at >= "2025-03-01") & (po.created_at < "2025-04-01")]
c = u.merge(po, on="user_id").groupby(["country", "user_id"]).size().rename("posts").reset_index()
c["rk"] = c.groupby("country")["posts"].rank(method="dense", ascending=False).astype("int64")
p = c[c.rk <= 2].sort_values(["country", "posts", "user_id"], ascending=[True, False, True]).reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by country, posts desc, user_id")
