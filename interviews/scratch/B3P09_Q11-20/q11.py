# Q11: degrees of separation and friends of friends on an undirected friendship graph
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER, PRIMARY KEY (user_a, user_b), CHECK (user_a < user_b));
INSERT INTO friendships VALUES
 (1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,6),(5,6),(6,7),(7,8),(11,12);
"""
SQL_MAIN = """
WITH RECURSIVE e(src, dst) AS (
  SELECT user_a, user_b FROM friendships
  UNION ALL
  SELECT user_b, user_a FROM friendships
), walk(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.dst, w.dist + 1 FROM walk w JOIN e ON e.src = w.node WHERE w.dist < 3
), best AS (
  SELECT node AS user_id, MIN(dist) AS dist FROM walk WHERE node <> 1 GROUP BY node
), fof AS (
  SELECT f.user_id, COUNT(DISTINCT x.dst) AS mutual_friends
  FROM best f
  JOIN e x ON x.src = f.user_id
  JOIN e me ON me.src = 1 AND me.dst = x.dst
  WHERE f.dist = 2
  GROUP BY f.user_id
)
SELECT b.user_id, b.dist, COALESCE(f.mutual_friends, 0) AS mutual_friends
FROM best b LEFT JOIN fof f ON f.user_id = b.user_id
ORDER BY b.dist, b.user_id
"""
# the same walk with a visited-path guard (enumerates every simple path, so it is the expensive version)
SQL_PATH = """
WITH RECURSIVE e(src, dst) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), walk(node, dist, path) AS (
  SELECT 1, 0, ',1,'
  UNION ALL
  SELECT e.dst, w.dist + 1, w.path || e.dst || ','
  FROM walk w JOIN e ON e.src = w.node
  WHERE w.dist < 3 AND w.path NOT LIKE '%,' || e.dst || ',%'
)
SELECT node AS user_id, MIN(dist) AS dist, COUNT(*) AS simple_paths
FROM walk WHERE node <> 1 GROUP BY node ORDER BY dist, node
"""
# the unguarded version: no distance cap, UNION ALL; bounded here only by LIMIT so the demo terminates
SQL_NOGUARD = """
WITH RECURSIVE e(src, dst) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), walk(node, dist) AS (
  SELECT 1, 0
  UNION ALL
  SELECT e.dst, w.dist + 1 FROM walk w JOIN e ON e.src = w.node
  LIMIT 1000
)
SELECT COUNT(*) AS rows_before_limit_stops_it, MAX(dist) AS deepest_level FROM walk
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (user 1, within 3 hops, mutual friends for distance 2):")
print(sql_df.to_string(index=False))
print("path-guard version (simple_paths = distinct routes found):")
print(pd.read_sql_query(SQL_PATH, con).to_string(index=False))
print("no guard, UNION ALL, stopped by LIMIT 1000:", con.execute(SQL_NOGUARD).fetchone())

friend = pd.read_sql_query("SELECT * FROM friendships", con)

def separation(friend, start, max_hops=3):
    # pd:main
    edges = pd.concat([friend.rename(columns={"user_a": "src", "user_b": "dst"}),
                       friend.rename(columns={"user_b": "src", "user_a": "dst"})]).drop_duplicates()
    seen = {start: 0}
    frontier = pd.DataFrame({"node": [start]})
    for d in range(1, max_hops + 1):
        nxt = frontier.merge(edges, left_on="node", right_on="src")["dst"].drop_duplicates()
        nxt = nxt[~nxt.isin(list(seen))]
        if nxt.empty:
            break
        seen.update({n: d for n in nxt})
        frontier = pd.DataFrame({"node": nxt.to_numpy()})
    best = pd.DataFrame({"user_id": [n for n in seen if n != start], "dist": [d for n, d in seen.items() if n != start]})
    mine = set(edges.loc[edges["src"] == start, "dst"])
    nbrs = edges.groupby("src")["dst"].agg(set)
    best["mutual_friends"] = [len(nbrs[u] & mine) if d == 2 else 0 for u, d in zip(best["user_id"], best["dist"])]
    return best.sort_values(["dist", "user_id"]).reset_index(drop=True)
    # pd:end

pd_df = separation(friend, 1)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after ORDER BY dist, user_id
print("pandas result equal to SQL")
# the path-guard version and the UNION version agree on the distances
pg = pd.read_sql_query(SQL_PATH, con)
assert pg[["user_id", "dist"]].equals(sql_df[["user_id", "dist"]])

# edge cases: duplicate friendship row (loaded without the primary key), a user with no friends, an unreachable component
con.executescript("CREATE TABLE f2(user_a INTEGER, user_b INTEGER); INSERT INTO f2 SELECT * FROM friendships; INSERT INTO f2 VALUES (1,2),(3,5);")
dup = pd.read_sql_query(SQL_MAIN.replace("friendships", "f2"), con)
assert dup.equals(sql_df), "COUNT(DISTINCT) keeps mutual counts right under duplicate edges"
print("duplicate edge rows (1,2) and (3,5): result unchanged =", dup.equals(sql_df))
naive = SQL_MAIN.replace("COUNT(DISTINCT x.dst)", "COUNT(x.dst)").replace("friendships", "f2")
print("same query with COUNT(x.dst) on the duplicated table:")
print(pd.read_sql_query(naive, con).query("dist == 2").to_string(index=False))
print("user 99 (no friends):", con.execute(SQL_MAIN.replace("SELECT 1, 0", "SELECT 99, 0").replace("<> 1", "<> 99").replace("me.src = 1", "me.src = 99")).fetchall())
allu = set(friend["user_a"]) | set(friend["user_b"])
print("users in the table but not within 3 hops of user 1:", sorted(allu - set(sql_df["user_id"]) - {1}), "(7 and 8 are 4 and 5 hops away, 11 and 12 are a separate component)")
print("pandas for user 99:", len(separation(friend, 99)), "rows")
print("asserts passed")
