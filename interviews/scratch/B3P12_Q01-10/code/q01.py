# Q1: friend suggestions: non-friend pairs with >= 2 mutual friends. SQL (UNION ALL edge list + self join) vs pandas merge.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE friends(user_id INTEGER, friend_id INTEGER);  -- stored once, user_id < friend_id
INSERT INTO users VALUES (1,'Asha'),(2,'Bala'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid'),(7,'Gita'),(8,'Hari');
INSERT INTO friends VALUES
 (1,2),(1,3),(2,4),(3,4),(2,5),(3,5),(4,5),(4,6),(5,6),(6,7),(1,7);
""")

sql = """
WITH e AS (                                   -- symmetric edge list: (person, friend)
  SELECT user_id AS p, friend_id AS f FROM friends
  UNION ALL
  SELECT friend_id, user_id FROM friends
)
SELECT e1.p AS a, e2.p AS b, COUNT(*) AS mutual
FROM e e1
JOIN e e2 ON e1.f = e2.f AND e1.p < e2.p      -- same friend, a < b: each pair once
WHERE NOT EXISTS (SELECT 1 FROM friends x WHERE x.user_id = e1.p AND x.friend_id = e2.p)
GROUP BY e1.p, e2.p
HAVING COUNT(*) >= 2
ORDER BY mutual DESC, a, b
"""
naive = """
WITH e AS (SELECT user_id AS p, friend_id AS f FROM friends UNION ALL SELECT friend_id, user_id FROM friends)
SELECT e1.p AS a, e2.p AS b, COUNT(*) AS mutual
FROM e e1 JOIN e e2 ON e1.f = e2.f AND e1.p <> e2.p
GROUP BY e1.p, e2.p HAVING COUNT(*) >= 2 ORDER BY a, b
"""
one = """
WITH e AS (SELECT user_id AS p, friend_id AS f FROM friends UNION ALL SELECT friend_id, user_id FROM friends)
SELECT e1.p AS a, e2.p AS b, COUNT(*) AS mutual
FROM e e1 JOIN e e2 ON e1.f = e2.f AND e1.p < e2.p
WHERE NOT EXISTS (SELECT 1 FROM friends x WHERE x.user_id = e1.p AND x.friend_id = e2.p)
GROUP BY e1.p, e2.p HAVING COUNT(*) = 1 ORDER BY a, b
"""
s = pd.read_sql(sql, con)
print("SQL result (non-friends, >= 2 mutual):"); print(s.to_string(index=False)); print()
print("pairs with exactly 1 mutual friend (excluded):"); print(pd.read_sql(one, con).to_string(index=False)); print()
n = pd.read_sql(naive, con)
print("naive p <> p version: %d rows (each pair twice, friends included)" % len(n)); print()

# pandas
friends = pd.read_sql("SELECT * FROM friends", con)
users = pd.read_sql("SELECT * FROM users", con)
e = pd.concat([friends.rename(columns={"user_id": "p", "friend_id": "f"}),
               friends.rename(columns={"user_id": "f", "friend_id": "p"})], ignore_index=True)
m = e.merge(e, on="f", suffixes=("_1", "_2"))
m = m[m["p_1"] < m["p_2"]]                       # same rule as SQL: a < b, each pair once
m = m.merge(friends.assign(is_friend=True), left_on=["p_1", "p_2"], right_on=["user_id", "friend_id"], how="left")
m = m[m["is_friend"].isna()]                     # anti-join: drop pairs that are already friends
p = (m.groupby(["p_1", "p_2"]).size().rename("mutual").reset_index()
       .rename(columns={"p_1": "a", "p_2": "b"}))
p = p[p["mutual"] >= 2].sort_values(["mutual", "a", "b"], ascending=[False, True, True]).reset_index(drop=True)
print("pandas result:"); print(p.to_string(index=False)); print()

# compare in the same order (mutual desc, a, b); both already sorted that way
pd.testing.assert_frame_equal(s, p, check_dtype=False)
named = s.merge(users, left_on="a", right_on="user_id").merge(users, left_on="b", right_on="user_id", suffixes=("_a", "_b"))
print("with names:"); print(named[["name_a", "name_b", "mutual"]].to_string(index=False))
print("asserts passed (same order: mutual desc, a, b)")
