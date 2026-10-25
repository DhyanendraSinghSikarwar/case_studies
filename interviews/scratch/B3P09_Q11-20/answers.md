### Q11 ⭐⭐⭐ 🔴 Degrees of separation and friends of friends: friendships(user_a, user_b) stores each friendship once (a < b), so the graph is undirected. For user 1 return every user within 3 hops with the shortest distance, the friends-of-friends list (distance exactly 2, excluding existing friends and the user), and the count of mutual friends for each suggestion. Show how the edge list is made symmetric with UNION ALL, why a distance guard or visited check is required (friend loops are cycles), and why MIN(distance) over all paths is the shortest path in an unweighted graph.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Make the edge list symmetric with `UNION ALL`, walk outwards from user 1 with a recursive CTE that carries a distance and stops at 3, take `MIN(dist)` per user (in an unweighted graph the first level at which a user appears is the shortest path), then friends of friends are the users at distance exactly 2 and the mutual-friend count is the number of their friends who are also friends of user 1.

**Schema and sample data:** eleven friendship rows, each stored once with `user_a < user_b`. Users 1 to 8 are connected; users 11 and 12 are a separate pair (never reachable from user 1). User 1's friends are 2 and 3, who are also friends with each other (a triangle, so friend loops exist).
```sql
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER, PRIMARY KEY (user_a, user_b), CHECK (user_a < user_b));
INSERT INTO friendships VALUES
 (1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,6),(5,6),(6,7),(7,8),(11,12);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
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
```
How it works:
- `e` is the symmetric edge list: each stored pair is emitted once as (a, b) and once as (b, a), so one join `e.src = w.node` follows a friendship in either direction. `UNION ALL` is fine here because the two halves cannot overlap (a < b means (a, b) never equals (b, a)).
- `walk` is the recursion. Its row is only (node, dist). I use plain `UNION`, not `UNION ALL`, so a row already produced is discarded; and `WHERE w.dist < 3` is a depth cap. The pair (node, dist) can only take (number of users x 4) values, so the recursion has to end.
- `best` is `MIN(dist)` per user. `walk` contains a user once for each distance at which some walk reaches them (user 2 is reached at distance 1, and also at distance 2 and 3 by walking back and forth), so the minimum picks the shortest.
- `fof` takes the users at distance exactly 2 (which by construction are not friends and not user 1, because those appear at distance 1 or 0 and `MIN` is smaller) and counts the distinct neighbours of that user who are also neighbours of user 1.
- A second version, `SQL_PATH` in the Code block, tracks a path string `',1,2,'` and refuses a step when the next user is already in it. That enumerates every simple path, which is exact but exponential in a dense graph, and it also gives a free `COUNT(*)` of routes; I print it to show it agrees on the distances.

**pandas answer:** a frontier loop, one merge per hop (shown once, identical to the Code block):
```py
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
```

**Example:** by hand on the sample data.
- Level 0 is user 1. Friends of 1 are 2 and 3, so distance 1 is {2, 3}.
- Neighbours of 2 are 1, 3, 4; neighbours of 3 are 1, 2, 4, 5. New users are 4 and 5, so distance 2 is {4, 5}.
- Neighbours of 4 are 2, 3, 6; of 5 are 3, 6. New user is 6, distance 3. A fourth hop would add 7, which the cap of 3 excludes.
- Mutual friends: user 4 knows 2 and 3, both friends of 1, so 2. User 5 knows 3 (and 6, who is not a friend of 1), so 1.
- Final answer: 2 and 3 at distance 1; 4 (2 mutual) and 5 (1 mutual) at distance 2; 6 at distance 3. Users 7, 8, 11 and 12 are outside 3 hops.

**Code:** run with `python3 -I`. The asserts compare SQL and pandas after sorting by `dist, user_id`, compare the path-guard distances to the `UNION` version, and check that duplicate edge rows do not change the result.
```python
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
```

**Output (my run):**
```text
SQL (user 1, within 3 hops, mutual friends for distance 2):
 user_id  dist  mutual_friends
       2     1               0
       3     1               0
       4     2               2
       5     2               1
       6     3               0
path-guard version (simple_paths = distinct routes found):
 user_id  dist  simple_paths
       2     1             3
       3     1             3
       4     2             4
       5     2             2
       6     3             3
no guard, UNION ALL, stopped by LIMIT 1000: (1000, 7)
pandas result equal to SQL
duplicate edge rows (1,2) and (3,5): result unchanged = True
same query with COUNT(x.dst) on the duplicated table:
 user_id  dist  mutual_friends
       4     2               3
       5     2               2
user 99 (no friends): []
users in the table but not within 3 hops of user 1: [7, 8, 11, 12] (7 and 8 are 4 and 5 hops away, 11 and 12 are a separate component)
pandas for user 99: 0 rows
asserts passed
```
Honest notes from the run: the path-guard version shows user 4 reachable by 4 simple paths (1-2-4, 1-3-4, 1-2-3-4, 1-3-2-4), which is why path enumeration blows up on dense friend graphs while the (node, dist) version stays small. Without any guard the recursion produced 1000 rows and reached level 7 before the `LIMIT 1000` inside the recursive select stopped it; without the `LIMIT` it would run until memory or time ran out (the walk bounces between friends forever).

**Edge cases:**
- Cycles: any friendship is a 2-cycle (1 to 2 to 1) and the triangle 1-2-3 is a 3-cycle, so without a guard the walk never ends (demonstrated above, bounded by `LIMIT`). The guard here is the distance cap plus `UNION` on (node, dist); the path-string guard is the alternative.
- Duplicate friendship rows (loaded without the primary key): distances are unchanged, but a plain `COUNT(x.dst)` over-counts mutual friends (user 4 showed 3 instead of 2). `COUNT(DISTINCT x.dst)` is the fix; or deduplicate the edge list first.
- User with no friends (user 99) or an unknown user: the anchor row exists but nothing joins, and `best` excludes the start user, so the result is empty (the pandas version returns 0 rows too).
- A user within 3 hops but at distance 1 is never a suggestion, because suggestions need `dist = 2` from `MIN`; a friend who is also at distance 2 by another route is still distance 1.
- Mutual count is 0 for everyone not at distance 2 by design (the column is only meaningful for suggestions).
- Unreachable users (11, 12) simply never appear.

**Then explain:**
- Symmetric edges: storing each friendship once halves storage but the walk must be able to go both ways; `UNION ALL` of the table with its reversed copy is the standard trick. In SQLite the CTE `e` is a plain (non-recursive) CTE, so referencing it in the recursive member is allowed; the recursive CTE `walk` itself is referenced only once.
- Why the guard is required: undirected friendship is a cycle for every edge. A recursive CTE stops only when the recursive member returns no rows, and here it always can walk back.
- Why `MIN(dist)` is the shortest path: every edge costs 1 and `dist` counts the edges walked, so every row for a user is the length of some real walk to them, and the shortest walk is among the rows because the cap of 3 allows it. The minimum over all rows is therefore the shortest distance, whatever order the engine processes the queue in (SQLite does not guarantee a row order without `ORDER BY`). With weighted edges this reasoning fails (see Q23 in this part).
- Cost: the (node, dist) version is at most nodes x max_dist rows; the path version is the number of simple paths, which can be exponential.
- Other engines (not executed here): PostgreSQL 14+ has `CYCLE node SET is_cycle USING path`, MySQL 8 needs `WITH RECURSIVE` and caps recursion at `cte_max_recursion_depth` (default 1000), SQL Server omits the word `RECURSIVE` and stops at `MAXRECURSION` (default 100), and Oracle would use `CONNECT BY NOCYCLE`. Graph databases do this natively, but the interview answer is the SQL one.

**Follow-ups:**
- "People you may know ranked by mutual friends?" Order the `fof` rows by `mutual_friends DESC` and cap with `LIMIT`; ties need a deterministic second key such as `user_id`.
- "What about a million users?" The recursive CTE materialises each level; at scale use an adjacency table with an index on `src`, a depth of 2 only, or precompute friends-of-friends in a batch job (graph or Spark tools are out of scope here).
- "Directed follows instead of friends?" Drop the `UNION ALL` reversal; mutual then means follows in both directions.

**Common mistakes:**
- Forgetting the symmetric edge list and finding only friends with a larger id (a < b storage).
- No guard: the query never ends, or hits an engine recursion limit.
- Using `UNION` with a path or a distance column that makes every row unique and believing it still dedups (it does not remove cycles then; here `(node, dist)` is bounded only because the distance cap exists).
- Counting mutual friends with `COUNT(*)` on data that has duplicate edge rows.
- Taking friends of friends as "distance 2 or less" and so suggesting existing friends, or forgetting to exclude the user themself.

---

### Q12 ⭐⭐⭐ 🔴 Cumulative sum that resets once it passes a threshold: txns(acct_id, txn_id, amount) ordered by txn_id. Keep a running total and, when it reaches or exceeds 100, emit a flag and restart from 0 on the next row (so the total depends on where earlier resets happened). Show why a window function cannot do it (the group key depends on the output of the previous row), solve with a recursive CTE that carries (acct_id, rn, running, reset_flag) and joins to the next row number, and compare with the easy variant that resets on a stored flag (Part 7 Q24, solved there with a running SUM of is_reset as group key). Give the pandas loop version with an assert and say that a recursive CTE here is a row-by-row loop in disguise.
**Asked at:** threshold-reset running total threads (search snippets only, not opened: SQLServerCentral 'reset running total', Microsoft Q&A 'Reset sum() OVER PARTITION BY for condition' saying there is no set-based form and a recursive CTE is the workaround, a recursive running total that 'forgets' after two rows); forum posts, not candidate reports; the deferred problem from Part 7 Q24; data engineer and analyst rounds
**Say this first (1 line):** A window function cannot do it, because whether row n starts a new group depends on the running total of row n-1, which is itself the output; so I carry the state (running total and reset flag) in a recursive CTE that walks the rows in order, and I say plainly that it is a row-by-row loop written in SQL.

**Schema and sample data:** four accounts. A has 8 rows with overshoots (120, 110, 110), B has two exact hits of 100 in a row and an exact hit again at the end, C has a single row above the limit, D has a NULL amount. Reset rule used: the flag is set when the running total is `>= 100`, and the next row restarts from 0 (so the next row's amount is the new running total).
```sql
CREATE TABLE txns(acct_id TEXT, txn_id INTEGER, amount INTEGER);
INSERT INTO txns VALUES
 ('A',1,40),('A',2,30),('A',3,50),('A',4,20),('A',5,90),('A',6,10),('A',7,100),('A',8,5),
 ('B',1,100),('B',2,100),('B',3,60),('B',4,30),('B',5,10),
 ('C',1,150),
 ('D',1,50),('D',2,NULL),('D',3,60);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, txn_id, amount, running, reset_flag) AS (
  SELECT acct_id, rn, txn_id, amount, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END
  FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn, t.txn_id, t.amount,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
)
SELECT acct_id, txn_id, amount, running, reset_flag
FROM r
ORDER BY acct_id, rn
```
How it works:
- `t` numbers each account's rows with `ROW_NUMBER()`, so gaps in `txn_id` do not matter, and replaces a NULL amount by 0 (otherwise `running + NULL` is NULL and every later row stays NULL).
- The anchor is row 1 of every account: running total is its amount, flag is whether that alone reaches 100.
- The recursive member joins the previous output row `r` to the next row `t.rn = r.rn + 1` of the same account. If the previous flag was 1 the total restarts at this row's amount, otherwise it adds. The flag is computed from the same expression (the CASE is repeated because a column alias cannot be used in the same SELECT).
- The recursion ends by itself when there is no row `rn + 1`. No cycle is possible (`rn` only increases), so no cycle guard is needed here; the guard question is only the depth limit of the engine.

**pandas answer:** a plain loop per account (shown once, identical to the Code block):
```py
    t = txns.assign(amount=txns["amount"].fillna(0).astype(int)).sort_values(["acct_id", "txn_id"])
    rows = []
    for acct, g in t.groupby("acct_id", sort=True):
        running, flag = 0, 0
        for txn_id, amount in zip(g["txn_id"], g["amount"]):
            running = amount if flag == 1 else running + amount
            flag = 1 if running >= limit else 0
            rows.append((acct, txn_id, amount, running, flag))
    return pd.DataFrame(rows, columns=["acct_id", "txn_id", "amount", "running", "reset_flag"])
```

**Example:** account A, amounts 40, 30, 50, 20, 90, 10, 100, 5.
- 40 (total 40), 30 (70), 50 (120, reached 100, flag 1).
- The next row restarts: 20 (total 20), 90 (110, flag 1). Restart: 10 (10), 100 (110, flag 1). Restart: 5 (5).
- Totals: 40, 70, 120, 20, 110, 10, 110, 5; flags on rows 3, 5, 7.
- Account B: 100 (flag), restart 100 (flag), restart 60, 90, 100 (flag). Account C: 150 (flag). Account D: 50, then the NULL counts as 0 (50), then 110 (flag).
- Why a window cannot do it: after the first reset at 120 the second group starts at row 4, but you only know that row 4 starts a group by having computed row 3's total. Cutting the plain running total into buckets of 100 puts the resets in the wrong rows (the 20 left over from 120 is not carried; the code prints the rows where the buckets give a wrong running total).

**Code:** run with `python3 -I`. Asserts: pandas loop equals the recursive CTE (both sorted by `acct_id, txn_id`), and a window function equals it when the flags are supplied from the recursion.
```python
# Q12: running total that resets after it reaches a threshold (100): recursive CTE versus pandas loop
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE txns(acct_id TEXT, txn_id INTEGER, amount INTEGER);
INSERT INTO txns VALUES
 ('A',1,40),('A',2,30),('A',3,50),('A',4,20),('A',5,90),('A',6,10),('A',7,100),('A',8,5),
 ('B',1,100),('B',2,100),('B',3,60),('B',4,30),('B',5,10),
 ('C',1,150),
 ('D',1,50),('D',2,NULL),('D',3,60);
"""
SQL_MAIN = """
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, txn_id, amount, running, reset_flag) AS (
  SELECT acct_id, rn, txn_id, amount, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END
  FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn, t.txn_id, t.amount,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
)
SELECT acct_id, txn_id, amount, running, reset_flag
FROM r
ORDER BY acct_id, rn
"""
# a window function once the flags are known: the group key is the number of resets strictly before the row
SQL_WINDOW_GIVEN_FLAGS = """
WITH RECURSIVE t AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         ROW_NUMBER() OVER (PARTITION BY acct_id ORDER BY txn_id) AS rn
  FROM txns
), r(acct_id, rn, running, reset_flag) AS (
  SELECT acct_id, rn, amount, CASE WHEN amount >= 100 THEN 1 ELSE 0 END FROM t WHERE rn = 1
  UNION ALL
  SELECT t.acct_id, t.rn,
         CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END,
         CASE WHEN (CASE WHEN r.reset_flag = 1 THEN t.amount ELSE r.running + t.amount END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN t ON t.acct_id = r.acct_id AND t.rn = r.rn + 1
), g AS (
  SELECT t.acct_id, t.rn, t.txn_id, t.amount, r.reset_flag,
         COALESCE(SUM(r.reset_flag) OVER (PARTITION BY t.acct_id ORDER BY t.rn
                  ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING), 0) AS grp
  FROM t JOIN r ON r.acct_id = t.acct_id AND r.rn = t.rn
)
SELECT acct_id, txn_id, amount,
       SUM(amount) OVER (PARTITION BY acct_id, grp ORDER BY rn) AS running, reset_flag
FROM g ORDER BY acct_id, rn
"""
# the tempting window-only answer: cut the plain running total into buckets of 100
SQL_NAIVE = """
WITH c AS (
  SELECT acct_id, txn_id, COALESCE(amount, 0) AS amount,
         SUM(COALESCE(amount, 0)) OVER (PARTITION BY acct_id ORDER BY txn_id) AS cum
  FROM txns
)
SELECT acct_id, txn_id, amount, cum, cum % 100 AS naive_running, CASE WHEN cum / 100 > LAG(cum / 100, 1, 0) OVER (PARTITION BY acct_id ORDER BY txn_id) THEN 1 ELSE 0 END AS naive_flag
FROM c ORDER BY acct_id, txn_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("recursive CTE result:")
print(sql_df.to_string(index=False))

txns = pd.read_sql_query("SELECT * FROM txns", con)

def reset_running(txns, limit=100):
    # pd:main
    t = txns.assign(amount=txns["amount"].fillna(0).astype(int)).sort_values(["acct_id", "txn_id"])
    rows = []
    for acct, g in t.groupby("acct_id", sort=True):
        running, flag = 0, 0
        for txn_id, amount in zip(g["txn_id"], g["amount"]):
            running = amount if flag == 1 else running + amount
            flag = 1 if running >= limit else 0
            rows.append((acct, txn_id, amount, running, flag))
    return pd.DataFrame(rows, columns=["acct_id", "txn_id", "amount", "running", "reset_flag"])
    # pd:end

pd_df = reset_running(txns)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by acct_id, txn_id
print("pandas loop equal to recursive CTE")

win = pd.read_sql_query(SQL_WINDOW_GIVEN_FLAGS, con)
pd.testing.assert_frame_equal(win, sql_df, check_dtype=False)
print("window function with the flags supplied: equal (the flags still came from the recursion)")

naive = pd.read_sql_query(SQL_NAIVE, con)
m = naive.merge(sql_df[["acct_id", "txn_id", "running", "reset_flag"]], on=["acct_id", "txn_id"])
print("window-only buckets of 100, rows that disagree with the true result:")
print(m[(m.naive_running != m.running) | (m.naive_flag != m.reset_flag)][["acct_id", "txn_id", "amount", "running", "naive_running", "reset_flag", "naive_flag"]].to_string(index=False))

# long account: SQLite has no default depth limit like MySQL (1000) or SQL Server (100)
con.execute("CREATE TABLE big(acct_id TEXT, txn_id INTEGER, amount INTEGER)")
con.executemany("INSERT INTO big VALUES ('Z', ?, ?)", [(i, 7) for i in range(1, 5001)])
n = con.execute(SQL_MAIN.replace("FROM txns", "FROM big").replace("ORDER BY acct_id, rn", "ORDER BY acct_id, rn DESC LIMIT 1")).fetchone()
print("5000-row single account, last row:", n, "(5000 recursion levels ran in SQLite)")
bigdf = pd.read_sql_query("SELECT * FROM big", con)
assert reset_running(bigdf).iloc[-1].tolist() == list(n)
print("empty table:", con.execute(SQL_MAIN.replace("FROM txns", "FROM txns WHERE 1 = 0")).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
recursive CTE result:
acct_id  txn_id  amount  running  reset_flag
      A       1      40       40           0
      A       2      30       70           0
      A       3      50      120           1
      A       4      20       20           0
      A       5      90      110           1
      A       6      10       10           0
      A       7     100      110           1
      A       8       5        5           0
      B       1     100      100           1
      B       2     100      100           1
      B       3      60       60           0
      B       4      30       90           0
      B       5      10      100           1
      C       1     150      150           1
      D       1      50       50           0
      D       2       0       50           0
      D       3      60      110           1
pandas loop equal to recursive CTE
window function with the flags supplied: equal (the flags still came from the recursion)
window-only buckets of 100, rows that disagree with the true result:
acct_id  txn_id  amount  running  naive_running  reset_flag  naive_flag
      A       3      50      120             20           1           1
      A       4      20       20             40           0           0
      A       5      90      110             30           1           1
      A       6      10       10             40           0           0
      A       7     100      110             40           1           1
      A       8       5        5             45           0           0
      B       1     100      100              0           1           1
      B       2     100      100              0           1           1
      B       5      10      100              0           1           1
      C       1     150      150             50           1           1
      D       3      60      110             10           1           1
5000-row single account, last row: ('Z', 5000, 7, 35, 0) (5000 recursion levels ran in SQLite)
empty table: []
asserts passed
```
Honest notes from the run:
- A window query becomes possible once the flags exist: the group key is the count of resets strictly before the row (`SUM(flag)` over `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`), then `SUM(amount) OVER (PARTITION BY acct_id, grp)`. In the Code block the flags still come from the recursion, so this is only a presentation trick; it proves the loop is where the real work happens.
- The window-only bucket attempt gets the reset rows' flags right in this data by luck but the running total wrong on 11 rows: the overshoot is not carried and the exact-100 rows show 0.
- A 5000-row single account ran fine in SQLite (I did not look for its limit). Other engines cap recursion by default (SQL Server `MAXRECURSION` 100, MySQL `cte_max_recursion_depth` 1000; both not executed here), so a long account would need `OPTION (MAXRECURSION 0)` or a raised setting, or a loop outside SQL.

**Edge cases:**
- NULL amount: replaced with 0 here (a business choice; ignoring the row entirely would need to skip it in the numbering). Without `COALESCE` the total turns NULL and stays NULL for the rest of the account.
- Reaching exactly 100 resets (`>=`), as asked; use `>` if the rule is "exceeds".
- Overshoot (120) is not carried to the next row; the restart is from 0 as the question states. If the business rule is to carry the excess, the recursive member changes to `running - 100`.
- Ties or duplicate `txn_id` in an account: `ROW_NUMBER` needs a tie-break column, otherwise the order is arbitrary.
- Account with a single row (C) is just the anchor. Empty table: no anchor rows, empty result (printed).
- Negative amounts: allowed; the total can drop and a flag happens only when it is at least 100.

**Then explain:**
- Why not a window: the group id of row n is a function of the whole history through the output, not of the input columns. `SUM() OVER` and `LAG()` only see input columns.
- Compare with the easy variant (Part 7 Q24, checked: "Cumulative sum that resets by condition"): there the reset flag is a stored column, so the group key is a running `SUM(is_reset)` and it is a plain window query. Here the flag depends on the running total, so it must be computed row by row.
- A recursive CTE here is a loop in disguise: each round turns the previous output row into the next, one row per account per round, so the depth is the longest account, not the number of accounts.
- SQLite allows the recursive member to join another table (`t`) once the CTE is referenced only once; it must not use aggregates or windows (windows were already applied in `t`).
- Other engines (not executed here): PostgreSQL and MySQL 8 accept the same query shape; SQL Server drops the `RECURSIVE` keyword; for very long histories a procedural loop, a cursor, or a pandas/Python job is usually the practical choice.

**Follow-ups:**
- "Can you do it without recursion?" Not as a single window; a self-join cannot either. Some engines offer `MODEL`/`MATCH_RECOGNIZE` (Oracle, others) or procedural code (not executed here).
- "Reset at 100 and carry the excess?" Use `running - 100` after a flag instead of the new amount.
- "How would you scale it?" Partition by account (the recursion already does), limit depth, or run it in pandas or a stored procedure.

**Common mistakes:**
- Trying `SUM() OVER` with `FLOOR(cum / 100)` as a group key (wrong as soon as the total overshoots).
- Forgetting `COALESCE` on a NULL amount.
- Joining on `txn_id + 1` when the ids have gaps (use a row number).
- Ending the recursion with an unbounded long account on an engine with a default recursion cap.
- Starting the next group with the old running total instead of the new amount.

---

### Q13 ⭐⭐ 🟢 Category tree and breadcrumbs: categories(category_id, parent_id, name) and products(product_id, category_id). Return for each category its breadcrumb ('Electronics > Phones > Android'), its depth, and the number of products in it including all descendant categories (a roll-up to every ancestor). Show the top-down recursion building the breadcrumb, the closure-pair recursion for the roll-up, why a product count by category_id alone misses the descendants, and how to list only leaf categories.
**Asked at:** employee-manager hierarchy guides: jdsatpathy Substack 'Find All Managers of an Employee Up to the CEO' (opened; anchor at the employee, join employee to manager, no cycle guard, UNION ALL), DataVidhya recursive hierarchy pattern page (opened; reports under a manager, ancestors of a category, paths in a dependency graph, depth tracking and cycle detection), and search snippets of datadriven.io and a Medium recursive CTE interview post (not opened); guides, not candidate reports; analyst and data engineer rounds at product companies, GCCs and consulting firms
**Say this first (1 line):** Walk the tree top-down from the roots to build the breadcrumb and depth, build the ancestor-descendant pairs (including each category paired with itself) with a second recursion, join products to the descendant side and `GROUP BY ancestor` for the roll-up, and a leaf is a category that nobody lists as a parent.

**Schema and sample data:** eight categories in two trees (Electronics and Books), 14 products. Product 113 has a NULL category and product 114 points to a category that does not exist; both are deliberately outside every count. Tablets is an empty leaf.
```sql
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Electronics'),(2,1,'Phones'),(3,2,'Android'),(4,2,'iOS'),(5,1,'Laptops'),
 (6,NULL,'Books'),(7,6,'Fiction'),(8,1,'Tablets');
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category_id INTEGER);
INSERT INTO products VALUES
 (101,3),(102,3),(103,3),(104,4),(105,4),(106,5),(107,5),(108,2),
 (109,7),(110,7),(111,7),(112,7),(113,NULL),(114,99);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE tree(category_id, depth, breadcrumb) AS (
  SELECT category_id, 0, name FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.category_id, t.depth + 1, t.breadcrumb || ' > ' || c.name
  FROM categories c JOIN tree t ON c.parent_id = t.category_id
), closure(ancestor, descendant) AS (
  SELECT category_id, category_id FROM categories
  UNION ALL
  SELECT cl.ancestor, c.category_id
  FROM closure cl JOIN categories c ON c.parent_id = cl.descendant
), rollup AS (
  SELECT cl.ancestor AS category_id, COUNT(p.product_id) AS products_incl_descendants
  FROM closure cl LEFT JOIN products p ON p.category_id = cl.descendant
  GROUP BY cl.ancestor
)
SELECT t.category_id, t.breadcrumb, t.depth,
       COALESCE(r.products_incl_descendants, 0) AS products_incl_descendants,
       CASE WHEN EXISTS (SELECT 1 FROM categories k WHERE k.parent_id = t.category_id) THEN 0 ELSE 1 END AS is_leaf
FROM tree t LEFT JOIN rollup r ON r.category_id = t.category_id
ORDER BY t.category_id
```
How it works:
- `tree` is top-down: the anchor is every root (`parent_id IS NULL`) with depth 0 and the breadcrumb equal to its name; each recursive step joins a child to its parent's row, adds 1 to the depth and appends `' > ' || name`.
- `closure` holds (ancestor, descendant) pairs. The anchor pairs every category with itself, and the recursive step extends a pair by one child of the descendant, so a category ends up paired with itself, its children, their children and so on. The aggregate is applied outside the recursion, in `rollup` (aggregates are not allowed in the recursive member).
- `LEFT JOIN products` keeps categories with no products (Tablets gets 0 instead of vanishing); `COUNT(p.product_id)` counts only matched rows.
- Leaf: `NOT EXISTS` a child row. I avoid `NOT IN (SELECT parent_id ...)` because the roots have a NULL `parent_id`, which makes the whole `NOT IN` return nothing (printed: 0 rows).

**pandas answer:** a parent walk for the breadcrumb and a merge loop for the pairs (shown once, identical to the Code block):
```py
    name = dict(zip(cats["category_id"], cats["name"]))
    parent = dict(zip(cats["category_id"], cats["parent_id"].astype("Int64")))
    rows = []
    for cid in cats["category_id"]:
        crumbs, cur, depth = [name[cid]], cid, 0
        while pd.notna(parent[cur]):
            cur = int(parent[cur])
            crumbs.append(name[cur])
            depth += 1
        rows.append((cid, " > ".join(reversed(crumbs)), depth))
    rep = pd.DataFrame(rows, columns=["category_id", "breadcrumb", "depth"])
    pairs = pd.DataFrame({"ancestor": cats["category_id"], "descendant": cats["category_id"]})
    edges = cats.dropna(subset=["parent_id"]).astype({"parent_id": int})
    frontier = pairs
    while not frontier.empty:
        frontier = (frontier.merge(edges, left_on="descendant", right_on="parent_id")
                            [["ancestor", "category_id"]].rename(columns={"category_id": "descendant"}))
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    counts = (pairs.merge(prods, left_on="descendant", right_on="category_id", how="left")
                   .groupby("ancestor")["product_id"].count().rename("products_incl_descendants"))
    rep = rep.merge(counts, left_on="category_id", right_index=True, how="left")
    rep["is_leaf"] = (~rep["category_id"].isin(edges["parent_id"])).astype(int)
    return rep.sort_values("category_id").reset_index(drop=True)
```

**Example:** by hand.
- Breadcrumbs: Android's parent is Phones (2), whose parent is Electronics (1): 'Electronics > Phones > Android', depth 2. Books has no parent: 'Books', depth 0.
- Direct counts (a plain `GROUP BY category_id`): Phones 1, Android 3, iOS 2, Laptops 2, Fiction 4, others 0.
- Roll-up: Phones = its own 1 + Android 3 + iOS 2 = 6. Electronics = Phones 6 + Laptops 2 + Tablets 0 + itself 0 = 8. Books = Fiction 4 = 4.
- Leaves: Android, iOS, Laptops, Tablets, Fiction.
- Products 113 (NULL category) and 114 (unknown category) are in no total; the root totals 8 + 4 = 12 equal the 12 products with a valid category.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after sorting by `category_id`.
```python
# Q13: category tree: breadcrumb, depth, product count including descendants, leaf flag
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Electronics'),(2,1,'Phones'),(3,2,'Android'),(4,2,'iOS'),(5,1,'Laptops'),
 (6,NULL,'Books'),(7,6,'Fiction'),(8,1,'Tablets');
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category_id INTEGER);
INSERT INTO products VALUES
 (101,3),(102,3),(103,3),(104,4),(105,4),(106,5),(107,5),(108,2),
 (109,7),(110,7),(111,7),(112,7),(113,NULL),(114,99);
"""
SQL_MAIN = """
WITH RECURSIVE tree(category_id, depth, breadcrumb) AS (
  SELECT category_id, 0, name FROM categories WHERE parent_id IS NULL
  UNION ALL
  SELECT c.category_id, t.depth + 1, t.breadcrumb || ' > ' || c.name
  FROM categories c JOIN tree t ON c.parent_id = t.category_id
), closure(ancestor, descendant) AS (
  SELECT category_id, category_id FROM categories
  UNION ALL
  SELECT cl.ancestor, c.category_id
  FROM closure cl JOIN categories c ON c.parent_id = cl.descendant
), rollup AS (
  SELECT cl.ancestor AS category_id, COUNT(p.product_id) AS products_incl_descendants
  FROM closure cl LEFT JOIN products p ON p.category_id = cl.descendant
  GROUP BY cl.ancestor
)
SELECT t.category_id, t.breadcrumb, t.depth,
       COALESCE(r.products_incl_descendants, 0) AS products_incl_descendants,
       CASE WHEN EXISTS (SELECT 1 FROM categories k WHERE k.parent_id = t.category_id) THEN 0 ELSE 1 END AS is_leaf
FROM tree t LEFT JOIN rollup r ON r.category_id = t.category_id
ORDER BY t.category_id
"""
SQL_DIRECT = """
SELECT c.category_id, COUNT(p.product_id) AS direct_products
FROM categories c LEFT JOIN products p ON p.category_id = c.category_id
GROUP BY c.category_id ORDER BY c.category_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("direct count only (GROUP BY category_id):", dict(con.execute(SQL_DIRECT).fetchall()))

cats = pd.read_sql_query("SELECT * FROM categories", con)
prods = pd.read_sql_query("SELECT * FROM products", con)

def category_report(cats, prods):
    # pd:main
    name = dict(zip(cats["category_id"], cats["name"]))
    parent = dict(zip(cats["category_id"], cats["parent_id"].astype("Int64")))
    rows = []
    for cid in cats["category_id"]:
        crumbs, cur, depth = [name[cid]], cid, 0
        while pd.notna(parent[cur]):
            cur = int(parent[cur])
            crumbs.append(name[cur])
            depth += 1
        rows.append((cid, " > ".join(reversed(crumbs)), depth))
    rep = pd.DataFrame(rows, columns=["category_id", "breadcrumb", "depth"])
    pairs = pd.DataFrame({"ancestor": cats["category_id"], "descendant": cats["category_id"]})
    edges = cats.dropna(subset=["parent_id"]).astype({"parent_id": int})
    frontier = pairs
    while not frontier.empty:
        frontier = (frontier.merge(edges, left_on="descendant", right_on="parent_id")
                            [["ancestor", "category_id"]].rename(columns={"category_id": "descendant"}))
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    counts = (pairs.merge(prods, left_on="descendant", right_on="category_id", how="left")
                   .groupby("ancestor")["product_id"].count().rename("products_incl_descendants"))
    rep = rep.merge(counts, left_on="category_id", right_index=True, how="left")
    rep["is_leaf"] = (~rep["category_id"].isin(edges["parent_id"])).astype(int)
    return rep.sort_values("category_id").reset_index(drop=True)
    # pd:end

pd_df = category_report(cats, prods)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by category_id
print("pandas equal to SQL; leaf categories:", list(pd_df.loc[pd_df.is_leaf == 1, "breadcrumb"]))
print("products not counted anywhere (NULL category or unknown category):",
      con.execute("SELECT product_id FROM products WHERE category_id IS NULL OR category_id NOT IN (SELECT category_id FROM categories)").fetchall())
# a leaf can be filtered with NOT IN only if parent_id has no NULLs: it has (roots), so show the trap
print("NOT IN version of the leaf filter returns:", con.execute("SELECT COUNT(*) FROM categories WHERE category_id NOT IN (SELECT parent_id FROM categories)").fetchone()[0], "rows (NULL parent_id of the roots poisons it)")
print("total rollup of roots:", int(pd_df.loc[pd_df.depth == 0, "products_incl_descendants"].sum()), "= products with a valid category:", int(prods["category_id"].isin(cats["category_id"]).sum()))
print("no root rows (anchor returns nothing) ->", pd.read_sql_query(SQL_MAIN.replace("FROM categories WHERE parent_id IS NULL", "FROM categories WHERE 1 = 0"), con).shape[0], "rows")
print("asserts passed")
```

**Output (my run):**
```text
 category_id                     breadcrumb  depth  products_incl_descendants  is_leaf
           1                    Electronics      0                          8        0
           2           Electronics > Phones      1                          6        0
           3 Electronics > Phones > Android      2                          3        1
           4     Electronics > Phones > iOS      2                          2        1
           5          Electronics > Laptops      1                          2        1
           6                          Books      0                          4        0
           7                Books > Fiction      1                          4        1
           8          Electronics > Tablets      1                          0        1
direct count only (GROUP BY category_id): {1: 0, 2: 1, 3: 3, 4: 2, 5: 2, 6: 0, 7: 4, 8: 0}
pandas equal to SQL; leaf categories: ['Electronics > Phones > Android', 'Electronics > Phones > iOS', 'Electronics > Laptops', 'Books > Fiction', 'Electronics > Tablets']
products not counted anywhere (NULL category or unknown category): [(113,), (114,)]
NOT IN version of the leaf filter returns: 0 rows (NULL parent_id of the roots poisons it)
total rollup of roots: 12 = products with a valid category: 12
no root rows (anchor returns nothing) -> 0 rows
asserts passed
```

**Edge cases:**
- Product with a NULL or unknown category: not counted under any category. Report them separately as a data-quality number.
- Category with no products or no children: the `LEFT JOIN` and `COALESCE` keep a 0 row (Tablets).
- A category whose parent_id points to a missing row never appears in `tree` (the top-down walk starts only at roots); Q15 in this part covers finding such orphans.
- Cycles in the category table would make both recursions loop; this data has none, and a depth cap or path guard (Q8) is the fix if the data cannot be trusted.
- Duplicate `(category_id)` rows would double counts; the primary key prevents it here.
- Multiple roots are normal (Electronics and Books).

**Then explain:**
- Why `GROUP BY category_id` alone misses descendants: a product is stored on its own category only, so Electronics shows 0 although it contains 8 products. The roll-up needs every ancestor to see the product, which is exactly what the closure pairs provide.
- Top-down versus pairs: the top-down walk carries one row per category (breadcrumb, depth), while the closure carries one row per (ancestor, descendant), which is about nodes x depth rows for a tree; fine for a catalogue, heavy for a huge deep tree.
- `' > '` is the separator; `||` is standard SQL concatenation (SQL Server uses `+` or `CONCAT`, MySQL uses `CONCAT` unless `PIPES_AS_CONCAT` is on; not executed here).
- MySQL 8 fixes the column type from the anchor, so the breadcrumb needs a `CAST(name AS CHAR(500))` in the anchor to avoid truncation (from the MySQL docs; not executed here).

**Follow-ups:**
- "Only leaf categories with products?" Filter `is_leaf = 1 AND products_incl_descendants > 0`.
- "Products per breadcrumb for a dashboard?" Join the report back to products on `category_id`.
- "Count distinct products if a product can sit in two categories?" Use `COUNT(DISTINCT p.product_id)` so a product in both Phones and Android is counted once under Electronics.

**Common mistakes:**
- `NOT IN` with NULL parents for the leaf filter.
- Counting products with an inner join and losing empty categories.
- Anchoring the closure without the self pair, so a category's own products are not counted.
- Counting a product twice at an ancestor when it belongs to two descendants and using `COUNT(*)` instead of `COUNT(DISTINCT ...)`.
- Aggregating inside the recursive member.

---

### Q14 ⭐⭐ 🟢 Recursive CTE versus self-join versus window: employees(emp_id, manager_id, name). For a company known to have at most three levels return each employee with manager and grand-manager names using LEFT JOINs, then the recursive version for unknown depth. State when each is right (fixed known depth and a tiny table versus unknown depth), why window functions (LAG, SUM OVER) cannot follow parent pointers by themselves, and one case where a window function beats recursion (a running total with no state dependence). Compare the readability, the query plan shape and the failure mode when the org gets a fourth level.
**Asked at:** LeetCode 1270 All People Report to the Given Manager (doocs mirror opened: head is employee 1, chain at most three managers, two self-joins; the 'given manager' framing at Hello Interview and DataVidhya seen only as search snippets, so a general version is an expert extension); public problem bank, not a candidate report; analyst and data scientist screens
**Say this first (1 line):** For a table known to have at most three levels, two `LEFT JOIN`s to the same table are the simplest, fastest and most readable answer; for unknown depth I use a recursive CTE that produces (employee, ancestor, distance) rows; window functions cannot follow a parent pointer, they only look at neighbouring rows in a sort order, so they are the right tool only for running or ranked calculations that need no per-row state.

**Schema and sample data:** six employees on three levels (Tim is CEO). Later in the Code block I insert Meera under Shyam to create a fourth level and show what the fixed join does then.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),(5,2,'Asha'),(6,3,'Ram');
```

**SQL answer:** two versions. The fixed-depth `SQL_FIXED` (in the Code block):
```sql
SELECT e.emp_id, e.name, m.name AS manager, g.name AS grand_manager,
       COALESCE(g.name, m.name, e.name) AS top_boss
FROM employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id
LEFT JOIN employees g ON g.emp_id = m.manager_id
ORDER BY e.emp_id
```
and the unknown-depth `SQL_MAIN` (in the Code block). It builds every (employee, ancestor, distance) pair with a depth cap of 20 as a guard, then picks distance 1, distance 2 and the farthest ancestor as the top boss:
```sql
WITH RECURSIVE anc(emp_id, anc_id, dist) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT a.emp_id, e.manager_id, a.dist + 1
  FROM anc a JOIN employees e ON e.emp_id = a.anc_id
  WHERE e.manager_id IS NOT NULL AND a.dist < 20
)
SELECT e.emp_id, e.name,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 1) AS manager,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 2) AS grand_manager,
       COALESCE((SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id
                 WHERE a.emp_id = e.emp_id ORDER BY a.dist DESC LIMIT 1), e.name) AS top_boss
FROM employees e
ORDER BY e.emp_id
```

**pandas answer:** the merge loop for the recursive result (shown once, identical to the Code block); the two-merge fixed-depth version is in the Code block too:
```py
    nm = emps.set_index("emp_id")["name"]
    pairs = emps.dropna(subset=["manager_id"]).assign(anc_id=lambda d: d["manager_id"].astype(int), dist=1)[["emp_id", "anc_id", "dist"]]
    allp, cur = [pairs], pairs
    while not cur.empty:
        nxt = cur.merge(emps.dropna(subset=["manager_id"]), left_on="anc_id", right_on="emp_id", suffixes=("", "_m"))
        cur = nxt.assign(anc_id=nxt["manager_id"].astype(int), dist=nxt["dist"] + 1)[["emp_id", "anc_id", "dist"]]
        allp.append(cur)
    anc = pd.concat(allp, ignore_index=True)
    out = emps[["emp_id", "name"]].copy()
    for label, k in (("manager", 1), ("grand_manager", 2)):
        s = anc[anc["dist"] == k].set_index("emp_id")["anc_id"].map(nm)
        out[label] = out["emp_id"].map(s)
    top = anc.sort_values("dist").groupby("emp_id")["anc_id"].last().map(nm)
    out["top_boss"] = out["emp_id"].map(top).fillna(out["name"])
    return out.sort_values("emp_id").reset_index(drop=True)
```

**Example:** on the three-level data, Ram reports to Hari, who reports to Tim: manager Hari, grand-manager Tim, top boss Tim. Tim has no manager (NULL, so the `LEFT JOIN` finds nothing): manager and grand-manager are NULL and the top boss falls back to Tim himself. Radha has a manager but no grand-manager, so her top boss is the manager, Tim. Both queries give the identical table here (asserted). Now insert Meera under Shyam: Tim > Radha > Shyam > Meera. The fixed join still shows manager Shyam and grand-manager Radha correctly (those two columns are what it was built for), but its top boss for Meera is Radha because it believes grand-manager is the top; the recursive version says Tim. No error is raised.

**Code:** run with `python3 -I`. Asserts: recursive equals fixed on three levels; the pandas loop equals the SQL recursive result and the pandas two-merge equals the fixed SQL on four levels (all sorted by `emp_id`).
```python
# Q14: recursive CTE versus fixed self-joins versus window functions on a manager hierarchy
import sqlite3
import pandas as pd

SCHEMA3 = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),(5,2,'Asha'),(6,3,'Ram');
"""
SQL_MAIN = """
WITH RECURSIVE anc(emp_id, anc_id, dist) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT a.emp_id, e.manager_id, a.dist + 1
  FROM anc a JOIN employees e ON e.emp_id = a.anc_id
  WHERE e.manager_id IS NOT NULL AND a.dist < 20
)
SELECT e.emp_id, e.name,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 1) AS manager,
       (SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id WHERE a.emp_id = e.emp_id AND a.dist = 2) AS grand_manager,
       COALESCE((SELECT n.name FROM anc a JOIN employees n ON n.emp_id = a.anc_id
                 WHERE a.emp_id = e.emp_id ORDER BY a.dist DESC LIMIT 1), e.name) AS top_boss
FROM employees e
ORDER BY e.emp_id
"""
SQL_FIXED = """
SELECT e.emp_id, e.name, m.name AS manager, g.name AS grand_manager,
       COALESCE(g.name, m.name, e.name) AS top_boss
FROM employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id
LEFT JOIN employees g ON g.emp_id = m.manager_id
ORDER BY e.emp_id
"""
SQL_LAG = """
SELECT emp_id, name, LAG(name) OVER (ORDER BY emp_id) AS lag_as_manager, manager_id FROM employees ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA3)
rec3 = pd.read_sql_query(SQL_MAIN, con)
fix3 = pd.read_sql_query(SQL_FIXED, con)
print("three-level company, fixed LEFT JOINs:")
print(fix3.to_string(index=False))
pd.testing.assert_frame_equal(rec3, fix3)
print("recursive version gives the identical table on 3 levels")

con.execute("INSERT INTO employees VALUES (7, 4, 'Meera')")   # a fourth level: Tim > Radha > Shyam > Meera
rec4 = pd.read_sql_query(SQL_MAIN, con)
fix4 = pd.read_sql_query(SQL_FIXED, con)
print("after adding a fourth level (Meera reports to Shyam):")
diff = rec4.merge(fix4, on=["emp_id", "name"], suffixes=("_rec", "_fixed"))
print(diff[diff.top_boss_rec != diff.top_boss_fixed][["name", "manager_rec", "grand_manager_rec", "top_boss_rec", "top_boss_fixed"]].to_string(index=False))
print("rows where the fixed join disagrees with the recursive one:", int((diff.top_boss_rec != diff.top_boss_fixed).sum()), "(no error, just a wrong top boss)")
print("LAG over emp_id is not the manager:")
print(pd.read_sql_query(SQL_LAG, con).to_string(index=False))

emps = pd.read_sql_query("SELECT * FROM employees", con)

def hierarchy(emps):
    # pd:main
    nm = emps.set_index("emp_id")["name"]
    pairs = emps.dropna(subset=["manager_id"]).assign(anc_id=lambda d: d["manager_id"].astype(int), dist=1)[["emp_id", "anc_id", "dist"]]
    allp, cur = [pairs], pairs
    while not cur.empty:
        nxt = cur.merge(emps.dropna(subset=["manager_id"]), left_on="anc_id", right_on="emp_id", suffixes=("", "_m"))
        cur = nxt.assign(anc_id=nxt["manager_id"].astype(int), dist=nxt["dist"] + 1)[["emp_id", "anc_id", "dist"]]
        allp.append(cur)
    anc = pd.concat(allp, ignore_index=True)
    out = emps[["emp_id", "name"]].copy()
    for label, k in (("manager", 1), ("grand_manager", 2)):
        s = anc[anc["dist"] == k].set_index("emp_id")["anc_id"].map(nm)
        out[label] = out["emp_id"].map(s)
    top = anc.sort_values("dist").groupby("emp_id")["anc_id"].last().map(nm)
    out["top_boss"] = out["emp_id"].map(top).fillna(out["name"])
    return out.sort_values("emp_id").reset_index(drop=True)
    # pd:end

pd.testing.assert_frame_equal(hierarchy(emps), rec4)   # compared after sorting by emp_id
print("pandas ancestor loop equal to the SQL recursive result (4 levels)")
f = emps.merge(emps[["emp_id", "name", "manager_id"]].rename(columns={"emp_id": "mid", "name": "manager", "manager_id": "gid"}), left_on="manager_id", right_on="mid", how="left")
f = f.merge(emps[["emp_id", "name"]].rename(columns={"emp_id": "gid", "name": "grand_manager"}), on="gid", how="left")
f["top_boss"] = f["grand_manager"].fillna(f["manager"]).fillna(f["name"])
f = f[["emp_id", "name", "manager", "grand_manager", "top_boss"]].sort_values("emp_id").reset_index(drop=True)
pd.testing.assert_frame_equal(f, fix4)
print("pandas two-merge version equal to the fixed-join SQL")

for label, q in (("fixed joins", SQL_FIXED), ("recursive", SQL_MAIN)):
    print("EXPLAIN QUERY PLAN,", label)
    for r in con.execute("EXPLAIN QUERY PLAN " + q):
        print("  ", r[3])

# a window function where it wins: running total with no state dependence
con.executescript("CREATE TABLE sales(day TEXT, amount INTEGER); INSERT INTO sales VALUES ('2024-03-01',10),('2024-03-02',5),('2024-03-03',20);")
print(con.execute("SELECT day, amount, SUM(amount) OVER (ORDER BY day) FROM sales ORDER BY day").fetchall())
print("empty employees ->", con.execute(SQL_MAIN.replace("FROM employees e\nORDER", "FROM employees e WHERE 1 = 0\nORDER")).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
three-level company, fixed LEFT JOINs:
 emp_id  name manager grand_manager top_boss
      1   Tim     NaN           NaN      Tim
      2 Radha     Tim           NaN      Tim
      3  Hari     Tim           NaN      Tim
      4 Shyam   Radha           Tim      Tim
      5  Asha   Radha           Tim      Tim
      6   Ram    Hari           Tim      Tim
recursive version gives the identical table on 3 levels
after adding a fourth level (Meera reports to Shyam):
 name manager_rec grand_manager_rec top_boss_rec top_boss_fixed
Meera       Shyam             Radha          Tim          Radha
rows where the fixed join disagrees with the recursive one: 1 (no error, just a wrong top boss)
LAG over emp_id is not the manager:
 emp_id  name lag_as_manager  manager_id
      1   Tim            NaN         NaN
      2 Radha            Tim         1.0
      3  Hari          Radha         1.0
      4 Shyam           Hari         2.0
      5  Asha          Shyam         2.0
      6   Ram           Asha         3.0
      7 Meera            Ram         4.0
pandas ancestor loop equal to the SQL recursive result (4 levels)
pandas two-merge version equal to the fixed-join SQL
EXPLAIN QUERY PLAN, fixed joins
   SCAN e
   SEARCH m USING INTEGER PRIMARY KEY (rowid=?) LEFT-JOIN
   SEARCH g USING INTEGER PRIMARY KEY (rowid=?) LEFT-JOIN
EXPLAIN QUERY PLAN, recursive
   SCAN e
   CORRELATED SCALAR SUBQUERY 3
   MATERIALIZE anc
   SETUP
   SCAN employees
   RECURSIVE STEP
   SCAN a
   SEARCH e USING INTEGER PRIMARY KEY (rowid=?)
   BLOOM FILTER ON a (emp_id=? AND dist=?)
   SEARCH a USING AUTOMATIC PARTIAL COVERING INDEX (emp_id=? AND dist=?)
   SEARCH n USING INTEGER PRIMARY KEY (rowid=?)
   CORRELATED SCALAR SUBQUERY 4
   BLOOM FILTER ON a (emp_id=? AND dist=?)
   SEARCH a USING AUTOMATIC PARTIAL COVERING INDEX (emp_id=? AND dist=?)
   SEARCH n USING INTEGER PRIMARY KEY (rowid=?)
   CORRELATED SCALAR SUBQUERY 5
   BLOOM FILTER ON a (emp_id=?)
   SEARCH a USING AUTOMATIC COVERING INDEX (emp_id=?)
   SEARCH n USING INTEGER PRIMARY KEY (rowid=?)
   USE TEMP B-TREE FOR ORDER BY
[('2024-03-01', 10, 10), ('2024-03-02', 5, 15), ('2024-03-03', 20, 35)]
empty employees -> []
asserts passed
```
The query plan lines are what SQLite 3.45.1 printed here; other versions may word them differently.

**Edge cases:**
- CEO (NULL manager): the `LEFT JOIN` keeps the row with NULL manager columns; with an `INNER JOIN` the CEO and all second-level employees would disappear (a common bug).
- Orphan (manager_id pointing to a missing row): the fixed join gives a NULL manager name (looks like a CEO); the recursive version stops at the missing row. See Q15 for the checks.
- Cycle in the data: the fixed join is immune (it only goes two hops), the recursive version needs a guard; I used `a.dist < 20`.
- Empty table: both return no rows (printed for the recursive one).
- The LAG attempt shows why windows fail: `LAG(name) OVER (ORDER BY emp_id)` gives the previous row in id order, which happened to be right for Radha and wrong for everyone else (Hari gets Radha, Meera gets Ram).

**Then explain:**
- Readability: the two-join query is easy to read, but each extra level is another join and another `COALESCE`; the recursive version is longer once but does not change with depth.
- Query plan shape: the fixed version is one scan of `e` with one primary-key lookup per join (printed). The recursive plan has a `SETUP` and `RECURSIVE STEP` for the CTE, and SQLite built automatic indexes on the materialised result for the three correlated subqueries. For a tiny table both are instant; at scale, an index on `manager_id` matters for the recursive step.
- Failure mode on a fourth level: the fixed join does not fail, it silently answers for the first two levels only. The recursive version either gets it right or (on a cycle without guard) never ends, which is a loud failure.
- When each is right: fixed joins for a known shallow hierarchy and one-off reports; recursion for unknown depth, subtree or chain questions, and roll-ups.
- Where a window function wins: a running total such as `SUM(amount) OVER (ORDER BY day)` (printed: 10, 15, 35) needs no per-row state beyond the sort order, and it is a single pass with no recursion.

**Follow-ups:**
- "How many levels does the company have?" `MAX(dist) + 1` from the ancestor pairs, or a recursive depth query.
- "Can you flatten to a fixed number of columns for a BI tool?" Yes, with pivot-style `MAX(CASE WHEN dist = k ...)` columns, choosing a maximum k and accepting that deeper levels are cut off.
- "What changes in other engines?" PostgreSQL and MySQL 8 use `WITH RECURSIVE`, SQL Server omits `RECURSIVE` (default `MAXRECURSION` 100); all hedged, not executed.

**Common mistakes:**
- `INNER JOIN` to the manager, which drops the CEO.
- Assuming "at most three levels" stays true.
- Trying `LAG` or `SUM OVER` to climb parent pointers.
- Writing the top boss as the last non-NULL in a fixed chain and not noticing when the chain is longer.
- No depth cap or visited check when the data may contain loops.

---

### Q15 ⭐⭐ 🟡 Cycles, orphans and multiple roots in hierarchy data: employees(emp_id, manager_id, name) loaded from an HR export. Write queries that find (a) orphans (manager_id not NULL and not in the table), (b) self-managed rows, (c) rows with more than one root or no root, (d) employees whose upward chain loops (cycle membership, using a path or depth guard), and (e) employees unreachable from the CEO by a top-down walk. Explain why NOT IN with a NULL manager_id is a trap, why a cycle has no root and so is invisible to a top-down query, and give a data-quality summary row per problem type.
**Asked at:** cycle-handling guides (search snippets only, not opened: manual path string or array of visited ids with a flag, the itprotoday 'Cycling with CTEs' article, Oracle NOCYCLE and CONNECT_BY_ISCYCLE docs, PostgreSQL CYCLE); the opened PostgreSQL page says UNION cannot stop a cycle when a depth column makes every row unique; guides and documentation, not candidate reports; data engineer and analyst rounds
**Say this first (1 line):** One query per problem type, then a summary row each: orphans with `NOT EXISTS` (never `NOT IN`), self-managed with `manager_id = emp_id`, roots by counting `manager_id IS NULL` (should be exactly one), cycles by an upward walk with a step cap, and unreachable rows by a top-down walk from the CEO, because a cycle has no root so a top-down query never sees it.

**Schema and sample data:** twelve rows from an imaginary HR export, with every problem planted. Tim (1) is the CEO and has a proper tree (Radha, Hari, Shyam: 1 to 4). Employee 5 is an orphan (manager 99 does not exist) and 12 reports to the orphan. Employee 6 is self-managed. Employees 7, 8, 9 form a 3-cycle (7 reports to 8, 8 to 9, 9 to 7) and 10 reports into the cycle. Zed (11) is a second root.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),
 (5,99,'Orphan'),(6,6,'Selfie'),
 (7,8,'LoopA'),(8,9,'LoopB'),(9,7,'LoopC'),(10,7,'BelowLoop'),
 (11,NULL,'Zed'),(12,5,'BelowOrphan');
```

**SQL answer:** `SQL_MAIN` in the Code block, one row per problem type with a count and the ids:
```sql
WITH RECURSIVE n(n) AS (SELECT COUNT(*) FROM employees),
up(emp_id, cur, steps) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.emp_id, e.manager_id, u.steps + 1
  FROM up u JOIN employees e ON e.emp_id = u.cur
  WHERE e.manager_id IS NOT NULL AND u.steps < (SELECT n FROM n)
),
down(emp_id) AS (
  SELECT emp_id FROM employees WHERE emp_id = 1
  UNION
  SELECT e.emp_id FROM employees e JOIN down d ON e.manager_id = d.emp_id
),
issues(problem, emp_id) AS (
  SELECT 'a orphan (manager not in table)', e.emp_id FROM employees e
    WHERE e.manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
  UNION ALL SELECT 'b self-managed', emp_id FROM employees WHERE manager_id = emp_id
  UNION ALL SELECT 'c root rows (manager NULL)', emp_id FROM employees WHERE manager_id IS NULL
  UNION ALL SELECT 'd member of a cycle', emp_id FROM up WHERE cur = emp_id GROUP BY emp_id
  UNION ALL SELECT 'd chain never reaches a root', emp_id FROM up WHERE steps = (SELECT n FROM n) GROUP BY emp_id
  UNION ALL SELECT 'e unreachable from CEO (emp 1)', emp_id FROM employees WHERE emp_id NOT IN (SELECT emp_id FROM down)
)
SELECT problem, COUNT(*) AS n_rows,
       group_concat(emp_id, ',') AS emp_ids
FROM (SELECT * FROM issues ORDER BY problem, emp_id)
GROUP BY problem
ORDER BY problem
```
How it works:
- (a) Orphans: `manager_id` is not NULL and no row has that `emp_id`. `NOT EXISTS` is safe with NULLs.
- (b) Self-managed: `manager_id = emp_id`.
- (c) Roots: rows with `manager_id IS NULL`. A healthy table has exactly one. Two or more means multiple roots (here 1 and 11); zero means every row has a manager, which means there is a cycle somewhere (checked on a ring table below).
- (d) Cycles: `up` walks from each employee to their manager, then that manager's manager, and so on. A row with `cur = emp_id` means the walk came back to its own start, so the employee is a member of a cycle (a self-managed row is a cycle of length 1, so 6 is reported here as well as in (b)). The step cap is the guard: the walk stops after `n` (the row count) steps, because a chain without a cycle has at most n - 1 managers. A walk that reaches `n` steps never ended: that finds the members and also the rows hanging below a cycle (employee 10), which are not members but whose chain loops.
- (e) Unreachable from the CEO: walk down from emp 1 with `UNION` (dedups rows, so even a duplicate edge cannot loop) and list everyone not in the result. That finds the second root and its tree, the orphan subtree, the self-managed row and the whole cycle.
- The outer query groups the issue rows into one summary row per problem with `COUNT` and `group_concat` of the ids (the ids are sorted in the subquery; SQLite keeps that order here, but `group_concat` order is not guaranteed by the standard, which is why the pandas version sorts explicitly and the assert would catch a mismatch).

**pandas answer:** dict-based version of the same five checks (shown once, identical to the Code block):
```py
    ids = set(emps["emp_id"])
    par = dict(zip(emps["emp_id"], emps["manager_id"]))
    n = len(emps)
    found = {
        "a orphan (manager not in table)": [e for e, m in par.items() if pd.notna(m) and m not in ids],
        "b self-managed": [e for e, m in par.items() if pd.notna(m) and m == e],
        "c root rows (manager NULL)": [e for e, m in par.items() if pd.isna(m)],
    }
    cyc, never = [], []
    for e in par:
        cur, steps, hit = par[e], 0, False
        while pd.notna(cur) and cur in ids and steps < n:
            steps += 1
            if cur == e:
                hit = True
            cur = par[cur]
        if hit:
            cyc.append(e)
        if steps == n:
            never.append(e)
    found["d member of a cycle"] = cyc
    found["d chain never reaches a root"] = never
    kids = emps.dropna(subset=["manager_id"]).groupby("manager_id")["emp_id"].apply(list).to_dict()
    seen, stack = {ceo}, [ceo]
    while stack:
        for k in kids.get(stack.pop(), []):
            if k not in seen:
                seen.add(k)
                stack.append(k)
    found["e unreachable from CEO (emp 1)"] = [e for e in par if e not in seen]
    rows = [(p, len(v), ",".join(str(x) for x in sorted(v))) for p, v in found.items() if v]
    return pd.DataFrame(rows, columns=["problem", "n_rows", "emp_ids"]).sort_values("problem").reset_index(drop=True)
```

**Example:** by hand.
- Orphans: 5 (manager 99 missing). Self-managed: 6. Roots: 1 and 11 (two roots).
- Cycle: 7 to 8 to 9 to 7. Walking up from 7 gives 8, 9, 7, which is 7 itself, so 7, 8, 9 are members; 6 is a one-step cycle. Employee 10's walk goes 7, 8, 9, 7, ... and never reaches a root but is not a member; so "chain never reaches a root" is 6, 7, 8, 9, 10 (five rows) and "member of a cycle" is 6, 7, 8, 9 (four rows). Employee 12 walks 5, then 99 is missing and the walk stops, so 12 is an orphan-subtree row, not a cycle row.
- Top-down from 1 reaches 1, 2, 3, 4 only. Unreachable: 5, 6, 7, 8, 9, 10, 11, 12 (eight rows).

**Code:** run with `python3 -I`. The assert compares the SQL summary and the pandas summary after sorting by problem name; the NOT IN trap, the ring table and the unguarded loop are printed after.
```python
# Q15: data-quality checks on an HR hierarchy: orphans, self-managed, roots, cycles, unreachable rows
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,1,'Hari'),(4,2,'Shyam'),
 (5,99,'Orphan'),(6,6,'Selfie'),
 (7,8,'LoopA'),(8,9,'LoopB'),(9,7,'LoopC'),(10,7,'BelowLoop'),
 (11,NULL,'Zed'),(12,5,'BelowOrphan');
"""
SQL_MAIN = """
WITH RECURSIVE n(n) AS (SELECT COUNT(*) FROM employees),
up(emp_id, cur, steps) AS (
  SELECT emp_id, manager_id, 1 FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.emp_id, e.manager_id, u.steps + 1
  FROM up u JOIN employees e ON e.emp_id = u.cur
  WHERE e.manager_id IS NOT NULL AND u.steps < (SELECT n FROM n)
),
down(emp_id) AS (
  SELECT emp_id FROM employees WHERE emp_id = 1
  UNION
  SELECT e.emp_id FROM employees e JOIN down d ON e.manager_id = d.emp_id
),
issues(problem, emp_id) AS (
  SELECT 'a orphan (manager not in table)', e.emp_id FROM employees e
    WHERE e.manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM employees m WHERE m.emp_id = e.manager_id)
  UNION ALL SELECT 'b self-managed', emp_id FROM employees WHERE manager_id = emp_id
  UNION ALL SELECT 'c root rows (manager NULL)', emp_id FROM employees WHERE manager_id IS NULL
  UNION ALL SELECT 'd member of a cycle', emp_id FROM up WHERE cur = emp_id GROUP BY emp_id
  UNION ALL SELECT 'd chain never reaches a root', emp_id FROM up WHERE steps = (SELECT n FROM n) GROUP BY emp_id
  UNION ALL SELECT 'e unreachable from CEO (emp 1)', emp_id FROM employees WHERE emp_id NOT IN (SELECT emp_id FROM down)
)
SELECT problem, COUNT(*) AS n_rows,
       group_concat(emp_id, ',') AS emp_ids
FROM (SELECT * FROM issues ORDER BY problem, emp_id)
GROUP BY problem
ORDER BY problem
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))

emps = pd.read_sql_query("SELECT * FROM employees", con)

def quality(emps, ceo=1):
    # pd:main
    ids = set(emps["emp_id"])
    par = dict(zip(emps["emp_id"], emps["manager_id"]))
    n = len(emps)
    found = {
        "a orphan (manager not in table)": [e for e, m in par.items() if pd.notna(m) and m not in ids],
        "b self-managed": [e for e, m in par.items() if pd.notna(m) and m == e],
        "c root rows (manager NULL)": [e for e, m in par.items() if pd.isna(m)],
    }
    cyc, never = [], []
    for e in par:
        cur, steps, hit = par[e], 0, False
        while pd.notna(cur) and cur in ids and steps < n:
            steps += 1
            if cur == e:
                hit = True
            cur = par[cur]
        if hit:
            cyc.append(e)
        if steps == n:
            never.append(e)
    found["d member of a cycle"] = cyc
    found["d chain never reaches a root"] = never
    kids = emps.dropna(subset=["manager_id"]).groupby("manager_id")["emp_id"].apply(list).to_dict()
    seen, stack = {ceo}, [ceo]
    while stack:
        for k in kids.get(stack.pop(), []):
            if k not in seen:
                seen.add(k)
                stack.append(k)
    found["e unreachable from CEO (emp 1)"] = [e for e in par if e not in seen]
    rows = [(p, len(v), ",".join(str(x) for x in sorted(v))) for p, v in found.items() if v]
    return pd.DataFrame(rows, columns=["problem", "n_rows", "emp_ids"]).sort_values("problem").reset_index(drop=True)
    # pd:end

pd_df = quality(emps)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by problem
print("pandas equal to SQL")

# the NOT IN trap
print("leaf query with NOT IN (NULL manager_id in the list):",
      con.execute("SELECT COUNT(*) FROM employees WHERE emp_id NOT IN (SELECT manager_id FROM employees)").fetchone()[0], "rows")
print("same with NOT IN ... WHERE manager_id IS NOT NULL:",
      con.execute("SELECT COUNT(*) FROM employees WHERE emp_id NOT IN (SELECT manager_id FROM employees WHERE manager_id IS NOT NULL)").fetchone()[0], "rows")
con.executescript("CREATE TABLE raw(emp_id INTEGER, manager_id INTEGER); INSERT INTO raw SELECT emp_id, manager_id FROM employees; INSERT INTO raw VALUES (NULL, 1);")
print("orphans via NOT IN on an export whose emp_id has a NULL row:",
      con.execute("SELECT COUNT(*) FROM raw WHERE manager_id NOT IN (SELECT emp_id FROM raw)").fetchone()[0],
      "| via NOT EXISTS:", con.execute("SELECT COUNT(*) FROM raw r WHERE manager_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM raw m WHERE m.emp_id = r.manager_id)").fetchone()[0])

# no root at all: a table that is only a cycle looks fine to a top-down query
con.executescript("CREATE TABLE ring(emp_id INTEGER PRIMARY KEY, manager_id INTEGER); INSERT INTO ring VALUES (1,2),(2,3),(3,1);")
print("ring table: root rows =", con.execute("SELECT COUNT(*) FROM ring WHERE manager_id IS NULL").fetchone()[0],
      "| top-down walk from the root finds", con.execute("""
WITH RECURSIVE d(emp_id) AS (SELECT emp_id FROM ring WHERE manager_id IS NULL UNION SELECT r.emp_id FROM ring r JOIN d ON r.manager_id = d.emp_id)
SELECT COUNT(*) FROM d""").fetchone()[0], "rows")

# what happens without the guard: the upward walk from emp 7, bounded only by LIMIT
print("upward walk from emp 7 with UNION ALL and no step cap, stopped by LIMIT 12:",
      con.execute("""WITH RECURSIVE up(cur, steps) AS (SELECT manager_id, 1 FROM employees WHERE emp_id = 7
                     UNION ALL SELECT e.manager_id, u.steps + 1 FROM up u JOIN employees e ON e.emp_id = u.cur LIMIT 12)
                     SELECT COUNT(*), MAX(steps) FROM up""").fetchone())
con2 = sqlite3.connect(":memory:")
con2.execute("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT)")
print("empty table ->", len(pd.read_sql_query(SQL_MAIN, con2)), "problem rows; pandas:", len(quality(emps.iloc[0:0])), "rows")
print("asserts passed")
```

**Output (my run):**
```text
                        problem  n_rows            emp_ids
a orphan (manager not in table)       1                  5
                 b self-managed       1                  6
     c root rows (manager NULL)       2               1,11
   d chain never reaches a root       5         6,7,8,9,10
            d member of a cycle       4            6,7,8,9
 e unreachable from CEO (emp 1)       8 5,6,7,8,9,10,11,12
pandas equal to SQL
leaf query with NOT IN (NULL manager_id in the list): 0 rows
same with NOT IN ... WHERE manager_id IS NOT NULL: 5 rows
orphans via NOT IN on an export whose emp_id has a NULL row: 0 | via NOT EXISTS: 1
ring table: root rows = 0 | top-down walk from the root finds 0 rows
upward walk from emp 7 with UNION ALL and no step cap, stopped by LIMIT 12: (12, 12)
empty table -> 0 problem rows; pandas: 0 rows
asserts passed
```
In the run, the unguarded upward walk from employee 7 (UNION ALL, no step cap) produced 12 rows and reached step 12 before the `LIMIT 12` inside the recursive select stopped it; without the limit it would not terminate.

**Edge cases:**
- NULL `manager_id` is a legitimate root, not an orphan. Checks (a) and (b) require `manager_id IS NOT NULL` first.
- `NOT IN` trap, shown by running it: `emp_id NOT IN (SELECT manager_id FROM employees)` returns 0 rows because the subquery contains the CEO's NULL and `x NOT IN (..., NULL)` is never true (printed: 0 rows; filtering the NULL out gives 5 rows). The same happens on orphans when the export has a row with a NULL `emp_id`: `manager_id NOT IN (SELECT emp_id ...)` returned 0 while `NOT EXISTS` found 1.
- No root at all: the ring table (1 to 2 to 3 to 1) has 0 root rows and a top-down query from the roots returns 0 rows, so the whole table is invisible. A cycle has no root, so only the "unreachable" or "number of roots is not 1" checks reveal it.
- Duplicate rows: `emp_id` is a primary key here so none; if the export has no key, duplicates multiply every walk (use `UNION` for the downward walk and `SELECT DISTINCT` first).
- Empty table: no problem rows (printed, both engines).
- Which row is "the CEO" is an assumption (emp 1 here); if there are two roots you have to be told which is the real one.

**Then explain:**
- Why no root means no top-down visibility: a top-down recursion starts from rows with no manager and follows children; a cycle's rows all have managers and are children of each other, never of a root.
- Why a guard is mandatory here: the point of the query is to run on data that may be broken, so the walk has to terminate on a cycle by construction. The cap `steps < n` is simple and engine-independent; path tracking (as in Q8) is the alternative.
- A summary row per problem type is what a data-quality gate wants: fail the load if orphans, self-managed or cycle counts are non-zero, and if the root count is not 1.
- Other engines (not executed here): PostgreSQL 14+ has a `CYCLE ... SET ... USING` clause that marks rows which revisit a node; Oracle has `CONNECT BY NOCYCLE` with `CONNECT_BY_ISCYCLE` and raises ORA-01436 on a loop without NOCYCLE; MySQL stops at `cte_max_recursion_depth` and SQL Server at `MAXRECURSION` with an error (all from documentation and snippets, not run).

**Follow-ups:**
- "How would you break the cycle?" Pick the intended parent per cycle with the business, set one `manager_id` to NULL (or the right value), and rerun the checks; do not delete rows blindly.
- "How do you stop it happening?" A foreign key `manager_id` to `emp_id` removes orphans (not cycles or self-managed; a `CHECK (manager_id <> emp_id)` removes the self-managed rows), and a trigger or a load-time validation catches cycles.
- "Are two roots always wrong?" Not always (a holding structure, or a forest of trees); it is wrong only if the business says there is one CEO.

**Common mistakes:**
- `NOT IN` with a nullable column.
- Treating a NULL manager as an orphan.
- Running only a top-down query and concluding the data is clean because it returned no error.
- No step cap on the upward walk, so the check query itself never ends on the bad data it is meant to find.
- Counting roots with `COUNT(manager_id)`, which ignores NULLs and so counts non-roots.

---

### Q16 ⭐⭐ 🟡 Graph reachability and connected components: edges(a, b) lists undirected edges between nodes 1 to 9 forming three clusters and an isolated node listed in nodes(node_id). Return for every node its component id as the smallest node id it can reach, and the component sizes. Show the symmetric edge list, the reachability recursion with UNION to stop cycles, and MIN(reached) per start node as the component label. Explain why this is O(nodes x reachable) and not suitable for big graphs, and compare with networkx connected_components (installed in this environment, version stated in the answer) and a plain Python union-find.
**Asked at:** SQLite lang_with documentation (opened: compound SELECT with a non-recursive initial select, UNION discards rows already queued and stops cycles, UNION ALL needs little memory, LIMIT on the recursive select, ORDER BY in the recursive select as queue order for breadth-first or depth-first, no aggregates or windows in the recursive select, queue algorithm) plus PostgreSQL WITH queries documentation (opened: working table and intermediate table evaluation); official documentation, not candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Make the edge list symmetric, compute for every start node the set of nodes it can reach with a recursive CTE using plain `UNION` (so already-seen (start, node) pairs are dropped and cycles stop by themselves), and the component id of a node is the minimum node id it can reach; sizes are a count per component. It costs about the sum of component size squared, so it is a teaching and small-graph answer, not a big-graph one.

**Schema and sample data:** nine nodes, seven edge rows. Cluster {1,2,3} is a triangle and also contains a duplicate edge in the opposite direction ((1,2) and (2,1)). Cluster {4,5,6} is a chain. Cluster {7,8} is a pair. Node 9 is isolated: it is only in the `nodes` table (that is why the node list is needed; edges alone would never mention it).
```sql
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9);
CREATE TABLE edges(a INTEGER, b INTEGER);
INSERT INTO edges VALUES (1,2),(2,3),(1,3),(2,1),(4,5),(5,6),(7,8);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE e(src, dst) AS (
  SELECT a, b FROM edges
  UNION
  SELECT b, a FROM edges
), reach(start, node) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT r.start, e.dst FROM reach r JOIN e ON e.src = r.node
), label AS (
  SELECT start AS node_id, MIN(node) AS component FROM reach GROUP BY start
)
SELECT l.node_id, l.component,
       (SELECT COUNT(*) FROM label x WHERE x.component = l.component) AS component_size
FROM label l
ORDER BY l.node_id
```
How it works:
- `e` is the symmetric edge list; I used `UNION` (not `UNION ALL`) so the duplicate (1,2)/(2,1) pair collapses.
- `reach(start, node)` starts with every node reaching itself (that is what makes node 9 appear with itself as its only reached node) and follows edges. `UNION` discards a (start, node) pair that is already there, so the triangle cannot loop: the number of distinct pairs is finite and the queue empties.
- `label` takes `MIN(node)` per start: the smallest id in the component, the same for every member. The final select adds the component size as a count of nodes with the same label.
- The sizes table in the output is just a `GROUP BY component`.

**pandas answer:** label propagation with merges: start with each node labelled by itself, repeatedly set each node's label to the minimum label among itself and its neighbours until nothing changes (shown once, identical to the Code block):
```py
    sym = pd.concat([edges.rename(columns={"a": "src", "b": "dst"}),
                     edges.rename(columns={"b": "src", "a": "dst"})]).drop_duplicates()
    lab = nodes.rename(columns={"node_id": "node"}).assign(component=nodes["node_id"])
    while True:
        nb = sym.merge(lab, left_on="dst", right_on="node")[["src", "component"]]
        best = nb.groupby("src")["component"].min()
        new = pd.concat([lab["node"].map(best), lab["component"]], axis=1).min(axis=1).astype(int)
        if new.equals(lab["component"]):
            break
        lab = lab.assign(component=new)
    lab = lab.rename(columns={"node": "node_id"})
    lab["component_size"] = lab.groupby("component")["node_id"].transform("size")
    return lab.sort_values("node_id").reset_index(drop=True)
```

**Example:** by hand.
- Component 1: from node 1 you reach 1, 2, 3 (also back to 1, which is dropped by `UNION`); the minimum is 1. From 3 you reach 3, 1, 2; minimum 1. So nodes 1, 2, 3 are labelled 1 and the size is 3.
- Component 4: node 4 reaches 4, 5, 6; node 6 reaches 6, 5, 4; label 4, size 3. Component 7: label 7, size 2. Node 9 reaches only itself: label 9, size 1.
- Rows in `reach`: 3x3 + 3x3 + 2x2 + 1x1 = 23 (printed, equal to the sum of size squared).

**Code:** run with `python3 -I`. The asserts compare SQL, pandas, a plain Python union-find and networkx (all sorted by node id; the networkx components are mapped to their minimum id).
```python
# Q16: connected components: reachability recursion with UNION, MIN(reached) as the label; checks with union-find and networkx
import sqlite3
import pandas as pd
import networkx as nx

SCHEMA = """
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9);
CREATE TABLE edges(a INTEGER, b INTEGER);
INSERT INTO edges VALUES (1,2),(2,3),(1,3),(2,1),(4,5),(5,6),(7,8);
"""
SQL_MAIN = """
WITH RECURSIVE e(src, dst) AS (
  SELECT a, b FROM edges
  UNION
  SELECT b, a FROM edges
), reach(start, node) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT r.start, e.dst FROM reach r JOIN e ON e.src = r.node
), label AS (
  SELECT start AS node_id, MIN(node) AS component FROM reach GROUP BY start
)
SELECT l.node_id, l.component,
       (SELECT COUNT(*) FROM label x WHERE x.component = l.component) AS component_size
FROM label l
ORDER BY l.node_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
sizes = sql_df.groupby("component").size().rename("size").reset_index()
print("component sizes:")
print(sizes.to_string(index=False))
SQL_REACH_ROWS = """
WITH RECURSIVE e(src, dst) AS (SELECT a, b FROM edges UNION SELECT b, a FROM edges),
reach(start, node) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT r.start, e.dst FROM reach r JOIN e ON e.src = r.node
)
SELECT COUNT(*) FROM reach
"""
print("rows in reach (start, node) pairs:", con.execute(SQL_REACH_ROWS).fetchone()[0], "= sum of size squared:", int((sizes["size"] ** 2).sum()))

nodes = pd.read_sql_query("SELECT * FROM nodes", con)
edges = pd.read_sql_query("SELECT * FROM edges", con)

def components(nodes, edges):
    # pd:main
    sym = pd.concat([edges.rename(columns={"a": "src", "b": "dst"}),
                     edges.rename(columns={"b": "src", "a": "dst"})]).drop_duplicates()
    lab = nodes.rename(columns={"node_id": "node"}).assign(component=nodes["node_id"])
    while True:
        nb = sym.merge(lab, left_on="dst", right_on="node")[["src", "component"]]
        best = nb.groupby("src")["component"].min()
        new = pd.concat([lab["node"].map(best), lab["component"]], axis=1).min(axis=1).astype(int)
        if new.equals(lab["component"]):
            break
        lab = lab.assign(component=new)
    lab = lab.rename(columns={"node": "node_id"})
    lab["component_size"] = lab.groupby("component")["node_id"].transform("size")
    return lab.sort_values("node_id").reset_index(drop=True)
    # pd:end

pd_df = components(nodes, edges)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by node_id
print("pandas label propagation equal to SQL")

def union_find(nodes, edges):
    parent = {n: n for n in nodes["node_id"]}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in zip(edges["a"], edges["b"]):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    return {n: find(n) for n in parent}

uf = union_find(nodes, edges)
assert uf == dict(zip(sql_df["node_id"], sql_df["component"]))
G = nx.Graph()
G.add_nodes_from(nodes["node_id"])
G.add_edges_from(zip(edges["a"], edges["b"]))
nxc = {n: min(c) for c in nx.connected_components(G) for n in c}
assert nxc == uf
print("networkx", nx.__version__, "and union-find agree with SQL; networkx components:", sorted(sorted(c) for c in nx.connected_components(G)))

# cost: a chain of n nodes gives n*n reach rows
for n in (50, 100, 200):
    c = sqlite3.connect(":memory:")
    c.executescript("CREATE TABLE nodes(node_id INTEGER PRIMARY KEY); CREATE TABLE edges(a INTEGER, b INTEGER);")
    c.executemany("INSERT INTO nodes VALUES (?)", [(i,) for i in range(1, n + 1)])
    c.executemany("INSERT INTO edges VALUES (?, ?)", [(i, i + 1) for i in range(1, n)])
    rows = c.execute(SQL_REACH_ROWS).fetchone()[0]
    print(f"chain of {n} nodes: reach rows = {rows} (n squared = {n*n})")

# without UNION (UNION ALL) the walk never ends on this graph; capped by LIMIT
print("UNION ALL reach, stopped by LIMIT 500:", con.execute("""WITH RECURSIVE e(src,dst) AS (SELECT a,b FROM edges UNION SELECT b,a FROM edges),
  reach(start,node) AS (SELECT node_id,node_id FROM nodes UNION ALL SELECT r.start,e.dst FROM reach r JOIN e ON e.src=r.node LIMIT 500)
  SELECT COUNT(*) FROM reach""").fetchone()[0], "rows")
# edge to a node missing from nodes, and no edges at all
con.execute("INSERT INTO edges VALUES (9, 50)")
print("edge to unknown node 50: label of node 9 =", con.execute(SQL_MAIN.replace("ORDER BY l.node_id", "ORDER BY l.node_id")).fetchall()[8][1], "(50 is never a start, so it never gets its own row)")
con.execute("DELETE FROM edges")
print("no edges: components =", sorted(set(r[1] for r in con.execute(SQL_MAIN))), "(every node is its own component)")
print("asserts passed")
```

**Output (my run):**
```text
 node_id  component  component_size
       1          1               3
       2          1               3
       3          1               3
       4          4               3
       5          4               3
       6          4               3
       7          7               2
       8          7               2
       9          9               1
component sizes:
 component  size
         1     3
         4     3
         7     2
         9     1
rows in reach (start, node) pairs: 23 = sum of size squared: 23
pandas label propagation equal to SQL
networkx 3.6.1 and union-find agree with SQL; networkx components: [[1, 2, 3], [4, 5, 6], [7, 8], [9]]
chain of 50 nodes: reach rows = 2500 (n squared = 2500)
chain of 100 nodes: reach rows = 10000 (n squared = 10000)
chain of 200 nodes: reach rows = 40000 (n squared = 40000)
UNION ALL reach, stopped by LIMIT 500: 500 rows
edge to unknown node 50: label of node 9 = 9 (50 is never a start, so it never gets its own row)
no edges: components = [1, 2, 3, 4, 5, 6, 7, 8, 9] (every node is its own component)
asserts passed
```
The environment has networkx 3.6.1; scipy is not installed, so no `scipy.sparse.csgraph` here. `nx.connected_components` and `nx.Graph.add_nodes_from`/`add_edges_from` were called exactly as written in the Code block.

**Edge cases:**
- Isolated node: only the `nodes` table gives it a row; derive nodes from the edge list and it disappears.
- Duplicate or reversed edges: harmless with `UNION`; with `UNION ALL` they would multiply rows (and, on a cycle, never end; the Code block shows the unguarded `UNION ALL` run, stopped at 500 rows by a `LIMIT`).
- Self-loop edge (a = b): harmless.
- Edge to a node missing from `nodes` (I inserted (9, 50)): node 9 now reaches 50 internally but 50 is never a start, so it gets no row of its own; the label of 9 stays 9. Clean the data or add endpoints to the node list with a `UNION`.
- No edges at all: every node is its own component (printed).
- Directed edges would need a different definition (strongly connected components), not covered by this query.

**Then explain:**
- Why `UNION` works here: the row is just (start, node), and there are at most nodes x nodes of those; a pair already produced is not produced again, so every cycle is cut.
- Cost: O(nodes x reachable). A chain of 50, 100 and 200 nodes produced exactly 2500, 10000 and 40000 reach rows (printed): quadratic growth in the component size. A component with a million nodes would need 10 to the power 12 rows, which is why this is not a big-graph tool. Real systems use union-find (near linear) or a library.
- Plain Python union-find: keep a parent map, `find` with path compression, `union` by the smaller root; one pass over the edges. It is the interview-friendly alternative, and it scales.
- networkx `connected_components` (checked here, version 3.6.1) returns one set of nodes per component (I believe it is a breadth-first search inside; I did not check the source); the label is `min(component)`.
- Other engines (not executed here): PostgreSQL 14+ could add `CYCLE`, but the `UNION` form works unchanged; MySQL 8 and SQL Server accept the same shape (SQL Server without the word `RECURSIVE`, and its `UNION` in the recursive member is not allowed there: SQL Server requires `UNION ALL` between anchor and recursive member, so the dedup approach needs a path or depth guard instead; stated from memory, not executed).

**Follow-ups:**
- "Why not just iterate label = min(neighbour labels) in SQL?" That needs repeated updates or a recursive member with an aggregate, which is not allowed; the pandas loop does it because it re-runs the merge each round.
- "How many rounds does the pandas loop need?" Up to the diameter of the largest component (a chain of n nodes needs about n rounds with the minimum at one end).
- "Which edges connect two components?" Edges whose endpoints have different labels; after a labelling there are none (printed sizes show three clusters plus the isolated node).

**Common mistakes:**
- Forgetting the symmetric edges, so labels depend on edge direction.
- Using `UNION ALL` and no guard.
- Dropping isolated nodes by building the node list from edges.
- Taking `MIN(reached)` without the self row (a node with no edges then has no label).
- Believing the query scales; it enumerates every reachable pair.

---

### Q17 ⭐⭐ 🟡 Flight routes with connections and total cost: flights(src, dst, cost). Return every route from 'DEL' to 'BLR' with at most 3 legs, the list of stops, the number of legs and the total cost, then the cheapest and the fewest-legs route. Guard against revisiting an airport with a path string, explain why the cost is added row by row in the recursive member and aggregated outside, and what changes if two flights exist between the same pair of cities (parallel edges multiply the number of routes). State the number of routes as the graph grows to show the combinatorial growth.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Walk out from 'DEL' with a recursive CTE that carries the current city, the number of legs, the running cost and the path string, add each flight's cost in the recursive member, refuse a flight to an airport already in the path, stop at 3 legs, keep the rows that end in 'BLR', and pick the cheapest and the fewest-legs route outside the recursion.

**Schema and sample data:** ten flight rows. There are two different DEL to BOM flights (100 and 90, parallel edges), a loop between BOM and HYD (BOM to HYD 50, HYD to BOM 40), and return flights to DEL (BLR to DEL 250, BOM to DEL 95) that would create cycles back to the origin.
```sql
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BLR',300),('DEL','BOM',100),('DEL','BOM',90),('DEL','HYD',80),
 ('BOM','BLR',120),('BOM','HYD',50),('HYD','BLR',90),('HYD','BOM',40),
 ('BLR','DEL',250),('BOM','DEL',95);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
WITH RECURSIVE walk(city, legs, cost, path) AS (
  SELECT 'DEL', 0, 0, 'DEL'
  UNION ALL
  SELECT f.dst, w.legs + 1, w.cost + f.cost, w.path || '>' || f.dst
  FROM walk w JOIN flights f ON f.src = w.city
  WHERE w.city <> 'BLR'
    AND w.legs < 3
    AND ('>' || w.path || '>') NOT LIKE '%>' || f.dst || '>%'
), routes AS (
  SELECT path AS stops, legs, cost FROM walk WHERE city = 'BLR'
)
SELECT stops, legs, cost,
       CASE WHEN cost = MIN(cost) OVER () THEN 1 ELSE 0 END AS is_cheapest,
       CASE WHEN ROW_NUMBER() OVER (ORDER BY legs, cost, stops) = 1 THEN 1 ELSE 0 END AS is_fewest_legs
FROM routes
ORDER BY cost, legs, stops
```
How it works:
- The anchor is the origin with 0 legs and 0 cost. Each step joins the current city to the flights that leave it and adds 1 leg and that flight's cost.
- The guard is `('>' || path || '>') NOT LIKE '%>' || dst || '>%'`: the path is wrapped in delimiters so a city is matched as a whole token ('>BOM>'). Airport codes here are all 3 letters, but the delimiters make the check right for any names. The `legs < 3` condition is a second guard and also the business limit.
- `w.city <> 'BLR'` stops a route once it has arrived, so routes that pass through BLR and come back are not built.
- The cost is added row by row because each row is one route prefix; a total only exists for a finished route. The aggregation (`MIN(cost)`, the ranks) happens outside, where aggregates and window functions are allowed. The recursive member itself cannot contain them.
- `is_cheapest` marks the minimum cost route; `is_fewest_legs` is the first route when ordered by legs, then cost (ties on legs go to the cheaper route).

**pandas answer:** one merge per leg on a frontier frame, with the same path check (shown once, identical to the Code block):
```py
    done, frontier = [], pd.DataFrame({"city": [src], "legs": [0], "cost": [0], "path": [src]})
    for _ in range(max_legs):
        frontier = frontier[frontier["city"] != dst]
        nxt = frontier.merge(flights, left_on="city", right_on="src")
        nxt = nxt[[f">{p}>".find(f">{d}>") < 0 for p, d in zip(nxt["path"], nxt["dst"])]]
        frontier = pd.DataFrame({"city": nxt["dst"], "legs": nxt["legs"] + 1,
                                 "cost": nxt["cost_x"] + nxt["cost_y"], "path": nxt["path"] + ">" + nxt["dst"]})
        done.append(frontier[frontier["city"] == dst])
    out = pd.concat(done).rename(columns={"path": "stops"})[["stops", "legs", "cost"]]
    out = out.sort_values(["cost", "legs", "stops"]).reset_index(drop=True)
    out["is_cheapest"] = (out["cost"] == out["cost"].min()).astype(int)
    out["is_fewest_legs"] = (out.index == out.sort_values(["legs", "cost", "stops"]).index[0]).astype(int)
    return out
```

**Example:** by hand, from DEL.
- 1 leg: DEL to BLR 300, a route; DEL to BOM (100 or 90), DEL to HYD 80 continue.
- 2 legs: BOM to BLR gives 220 (via the 100 flight) and 210 (via the 90 flight); HYD to BLR gives 170. BOM to HYD and HYD to BOM continue. BOM to DEL is blocked by the guard (DEL is in the path).
- 3 legs: DEL > BOM > HYD > BLR is 100 + 50 + 90 = 240 and 90 + 50 + 90 = 230; DEL > HYD > BOM > BLR is 80 + 40 + 120 = 240.
- Seven routes in all (five distinct stop lists, because of the parallel flight). Cheapest: DEL > HYD > BLR at 170. Fewest legs: DEL > BLR, one leg, 300.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after sorting by `cost, legs, stops`. The Code block also prints the no-guard run, a NULL cost, the growth in the number of routes, and the empty case.
```python
# Q17: flight routes with connections: path guard, cost added in the recursive member, aggregated outside
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BLR',300),('DEL','BOM',100),('DEL','BOM',90),('DEL','HYD',80),
 ('BOM','BLR',120),('BOM','HYD',50),('HYD','BLR',90),('HYD','BOM',40),
 ('BLR','DEL',250),('BOM','DEL',95);
"""
SQL_MAIN = """
WITH RECURSIVE walk(city, legs, cost, path) AS (
  SELECT 'DEL', 0, 0, 'DEL'
  UNION ALL
  SELECT f.dst, w.legs + 1, w.cost + f.cost, w.path || '>' || f.dst
  FROM walk w JOIN flights f ON f.src = w.city
  WHERE w.city <> 'BLR'
    AND w.legs < 3
    AND ('>' || w.path || '>') NOT LIKE '%>' || f.dst || '>%'
), routes AS (
  SELECT path AS stops, legs, cost FROM walk WHERE city = 'BLR'
)
SELECT stops, legs, cost,
       CASE WHEN cost = MIN(cost) OVER () THEN 1 ELSE 0 END AS is_cheapest,
       CASE WHEN ROW_NUMBER() OVER (ORDER BY legs, cost, stops) = 1 THEN 1 ELSE 0 END AS is_fewest_legs
FROM routes
ORDER BY cost, legs, stops
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("routes:", len(sql_df), "| distinct stop lists:", sql_df["stops"].nunique(), "(parallel DEL-BOM flights make two routes with the same stops)")

flights = pd.read_sql_query("SELECT * FROM flights", con)

def routes(flights, src="DEL", dst="BLR", max_legs=3):
    # pd:main
    done, frontier = [], pd.DataFrame({"city": [src], "legs": [0], "cost": [0], "path": [src]})
    for _ in range(max_legs):
        frontier = frontier[frontier["city"] != dst]
        nxt = frontier.merge(flights, left_on="city", right_on="src")
        nxt = nxt[[f">{p}>".find(f">{d}>") < 0 for p, d in zip(nxt["path"], nxt["dst"])]]
        frontier = pd.DataFrame({"city": nxt["dst"], "legs": nxt["legs"] + 1,
                                 "cost": nxt["cost_x"] + nxt["cost_y"], "path": nxt["path"] + ">" + nxt["dst"]})
        done.append(frontier[frontier["city"] == dst])
    out = pd.concat(done).rename(columns={"path": "stops"})[["stops", "legs", "cost"]]
    out = out.sort_values(["cost", "legs", "stops"]).reset_index(drop=True)
    out["is_cheapest"] = (out["cost"] == out["cost"].min()).astype(int)
    out["is_fewest_legs"] = (out.index == out.sort_values(["legs", "cost", "stops"]).index[0]).astype(int)
    return out
    # pd:end

pd_df = routes(flights)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)   # compared after sorting by cost, legs, stops
print("pandas frontier merge equal to SQL")

# without the path guard: the loop DEL > BOM > DEL > ... is walked until the leg cap; remove the leg cap too and it never ends
noguard = SQL_MAIN.replace("    AND ('>' || w.path || '>') NOT LIKE '%>' || f.dst || '>%'\n", "")
assert noguard != SQL_MAIN
print("no path guard, leg cap 3:", len(pd.read_sql_query(noguard, con)), "routes (vs", len(sql_df), "with the guard; the extras revisit an airport)")
nocap = noguard.replace("    AND w.legs < 3\n", "").replace("), routes AS", "  LIMIT 5000\n), routes AS")
print("no guard and no leg cap, stopped by LIMIT 5000:", len(pd.read_sql_query(nocap, con)), "routes found so far (it would never end)")

# NULL cost: the whole route cost becomes NULL
con.execute("UPDATE flights SET cost = NULL WHERE src = 'HYD' AND dst = 'BLR'")
nul = pd.read_sql_query(SQL_MAIN, con)
print("with HYD-BLR cost NULL: routes with NULL cost =", int(nul["cost"].isna().sum()), "| cheapest flag set on", int(nul["is_cheapest"].sum()), "rows")
con.execute("UPDATE flights SET cost = 90 WHERE src = 'HYD' AND dst = 'BLR'")

# combinatorial growth: layered graph, 3 airports per layer, every airport connects to all 3 in the next layer
def count_layered(width, layers, parallel=1):
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE fl(src TEXT, dst TEXT, cost INTEGER)")
    rows = [("S", f"L1_{j}", 1) for j in range(width)]
    for k in range(1, layers):
        rows += [(f"L{k}_{i}", f"L{k+1}_{j}", 1) for i in range(width) for j in range(width)]
    rows += [(f"L{layers}_{i}", "T", 1) for i in range(width)]
    c.executemany("INSERT INTO fl VALUES (?, ?, ?)", rows * parallel)
    return c.execute("""WITH RECURSIVE w(city, legs) AS (SELECT 'S', 0 UNION ALL SELECT f.dst, w.legs + 1 FROM w JOIN fl f ON f.src = w.city)
                        SELECT COUNT(*) FROM w WHERE city = 'T'""").fetchone()[0]
print("routes S to T, 3 airports per layer:", {k: count_layered(3, k) for k in (1, 2, 3, 4, 5, 6, 7, 8)})
print("same, every flight offered twice (parallel edges):", {k: count_layered(3, k, 2) for k in (1, 2, 3, 4, 5, 6)})
print("empty flights table ->", len(pd.read_sql_query(SQL_MAIN.replace("FROM walk w JOIN flights f", "FROM walk w JOIN (SELECT * FROM flights WHERE 1 = 0) f"), con)), "routes")
print("asserts passed")
```

**Output (my run):**
```text
          stops  legs  cost  is_cheapest  is_fewest_legs
    DEL>HYD>BLR     2   170            1               0
    DEL>BOM>BLR     2   210            0               0
    DEL>BOM>BLR     2   220            0               0
DEL>BOM>HYD>BLR     3   230            0               0
DEL>BOM>HYD>BLR     3   240            0               0
DEL>HYD>BOM>BLR     3   240            0               0
        DEL>BLR     1   300            0               1
routes: 7 | distinct stop lists: 5 (parallel DEL-BOM flights make two routes with the same stops)
pandas frontier merge equal to SQL
no path guard, leg cap 3: 9 routes (vs 7 with the guard; the extras revisit an airport)
no guard and no leg cap, stopped by LIMIT 5000: 1733 routes found so far (it would never end)
with HYD-BLR cost NULL: routes with NULL cost = 3 | cheapest flag set on 1 rows
routes S to T, 3 airports per layer: {1: 3, 2: 9, 3: 27, 4: 81, 5: 243, 6: 729, 7: 2187, 8: 6561}
same, every flight offered twice (parallel edges): {1: 12, 2: 72, 3: 432, 4: 2592, 5: 15552, 6: 93312}
empty flights table -> 0 routes
asserts passed
```
Honest notes from the run:
- Without the path guard but with the 3-leg cap the query still ends but returns 9 routes: two extras (DEL > BOM > DEL > BLR, once per parallel flight) go back through the origin. The leg cap alone is enough to terminate but not enough to be correct.
- Without the guard and without the cap, the demo only stopped at the 5000-row `LIMIT` (it had found 1733 arrivals by then); it would not terminate on its own.
- The route count grows multiplicatively: with 3 airports per layer and every airport connected to all 3 in the next layer, the number of routes from S to T is 3, 9, 27, 81, 243, 729, 2187, 6561 for 1 to 8 layers (3 to the power of the layers). If every flight is offered twice (parallel edges) the counts are 12, 72, 432, 2592, 15552, 93312: each parallel pair multiplies the routes again.

**Edge cases:**
- Parallel flights between the same cities produce separate routes with the same stops (here DEL > BOM > BLR at 210 and 220). If the question is "the cheapest per stop list", take `MIN(cost)` per stops; or collapse parallel edges to their cheapest flight before the walk.
- NULL cost: the route total becomes NULL (printed: 3 routes), `MIN` and the comparison ignore it, and in SQLite a NULL sorts first in an ascending `ORDER BY`, so a NULL-cost route would appear at the top of the list. Filter or `COALESCE` the costs first.
- No route (no path from the origin to the destination within the legs): empty result; empty flights table: empty result (printed).
- Ties for cheapest: `is_cheapest` flags all tied routes; `is_fewest_legs` flags exactly one (the tie-break is cost, then the stop list).
- Return flights (BLR to DEL) are blocked by the guard; round trips are a different question.

**Then explain:**
- Why add cost in the recursive member: the recursive member only sees the previous row, so the only way to know the total so far is to carry it. Totals by route are then plain columns; the best route is a `MIN` outside.
- Why the guard is by path and not by `UNION`: the rows are made unique by `legs`, `cost` and `path`, so `UNION` would remove nothing and would not stop a cycle (Q7). The path string, or a leg cap, is what terminates it.
- Combinatorics: the work is the number of routes, not the number of flights, which is why airline-style problems need a leg cap and usually a different algorithm (Dijkstra, Q23) once graphs grow.
- Other engines (not executed here): PostgreSQL commonly uses an array of visited airports (`path || dst`, `dst <> ALL(path)`) or the 14+ `CYCLE` clause; MySQL 8 and SQL Server take the same shape with their own concatenation and recursion limits (`cte_max_recursion_depth`, `MAXRECURSION`); Oracle would use `CONNECT BY NOCYCLE` with `SYS_CONNECT_BY_PATH`.

**Follow-ups:**
- "Cheapest route with any number of legs?" Remove the leg cap, keep the path guard, and accept the exponential cost; for a real network use a shortest-path algorithm outside SQL.
- "Layover time or departure times?" Add the arrival time to the row and join on `dep_time >= arr_time + layover`; the guard stays.
- "How many routes are there?" `COUNT(*)` over the routes: 7 here.

**Common mistakes:**
- Putting `MIN(cost)` or `SUM(cost)` inside the recursive member (not allowed) instead of carrying the running cost.
- No guard against revisiting an airport, so routes through the origin appear.
- Matching the path with a bare `LIKE '%BOM%'` when names can be substrings of each other.
- Forgetting that parallel flights are separate routes.
- Not stopping at the destination, so routes continue through it.

---

### Q18 ⭐⭐ 🟡 Compound interest and loan amortisation schedule: accounts(acct_id, balance, annual_rate) and loans(loan_id, principal, annual_rate, months). (a) Grow each account balance monthly for 12 months with a recursive CTE and compare with the closed form balance * (1 + r/12)^n, (b) build the full amortisation schedule for a 10000 loan at 12 percent annual over 6 months (month, opening balance, interest, principal paid, closing balance, constant EMI computed in the query with power or a documented workaround), with the last-row rounding fix. Explain why rounding each month differs from the closed form by a few paise, that SQLite has power and exp here only when math functions are compiled in (hedge for other engines), and the pandas loop check with asserts.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Compound interest and amortisation are state carried month to month, so the recursive CTE carries the opening balance and each month's row is derived from it; the closed form `balance * (1 + r/12)^n` is the check, it differs from the month-by-month answer by a few paise only because the schedule rounds to 2 decimals every month; and the last payment must be adjusted (pay off the remaining balance) so the loan ends at exactly zero.

**Schema and sample data:** five accounts (one with a 0 rate, one with a NULL rate) and three loans: 10000 at 12 percent for 6 months (the question's loan), 5000 at 0 percent for 4 months (the zero-rate trap) and 1200 at 18 percent for 1 month (a one-row schedule). Rates are stored as decimals (0.12 = 12 percent a year, so the monthly rate is annual_rate / 12).
```sql
CREATE TABLE accounts(acct_id INTEGER PRIMARY KEY, balance REAL, annual_rate REAL);
INSERT INTO accounts VALUES (1,1000,0.12),(2,2500,0.075),(3,100.55,0.06),(4,800,0.0),(5,500,NULL);
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal REAL, annual_rate REAL, months INTEGER);
INSERT INTO loans VALUES (1,10000,0.12,6),(2,5000,0.0,4),(3,1200,0.18,1);
```

**SQL answer:** two queries. Part (a), `SQL_GROWTH` in the Code block: the recursive CTE grows each balance for 12 months, rounding to 2 decimals each month, and compares month 12 with the closed form (`power`):
```sql
WITH RECURSIVE g(acct_id, month, bal) AS (
  SELECT acct_id, 0, balance FROM accounts
  UNION ALL
  SELECT g.acct_id, g.month + 1, ROUND(g.bal * (1 + a.annual_rate / 12.0), 2)
  FROM g JOIN accounts a ON a.acct_id = g.acct_id
  WHERE g.month < 12
)
SELECT g.acct_id, g.bal AS monthly_rounded,
       ROUND(a.balance * power(1 + a.annual_rate / 12.0, 12), 2) AS closed_form,
       ROUND(g.bal - a.balance * power(1 + a.annual_rate / 12.0, 12), 4) AS difference
FROM g JOIN accounts a ON a.acct_id = g.acct_id
WHERE g.month = 12
ORDER BY g.acct_id
```
Part (b), `SQL_MAIN` in the Code block, the amortisation schedule:
```sql
WITH RECURSIVE l AS (
  SELECT loan_id, principal, months, annual_rate / 12.0 AS r,
         CASE WHEN annual_rate = 0 THEN ROUND(principal / months, 2)
              ELSE ROUND(principal * (annual_rate / 12.0) * power(1 + annual_rate / 12.0, months)
                         / (power(1 + annual_rate / 12.0, months) - 1), 2) END AS emi
  FROM loans
), s(loan_id, month, opening) AS (
  SELECT loan_id, 1, principal FROM l
  UNION ALL
  SELECT s.loan_id, s.month + 1,
         ROUND(s.opening - CASE WHEN s.month = l.months THEN s.opening
                                ELSE l.emi - ROUND(s.opening * l.r, 2) END, 2)
  FROM s JOIN l ON l.loan_id = s.loan_id
  WHERE s.month < l.months
), x AS (
  SELECT s.loan_id, s.month, s.opening, l.emi,
         ROUND(s.opening * l.r, 2) AS interest,
         CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END AS principal_paid
  FROM s JOIN l ON l.loan_id = s.loan_id
)
SELECT loan_id, month, opening, interest, ROUND(principal_paid, 2) AS principal_paid,
       ROUND(interest + principal_paid, 2) AS payment,
       ROUND(opening - principal_paid, 2) AS closing
FROM x
ORDER BY loan_id, month
```
How it works:
- `l` computes the constant EMI once per loan: `P * r * (1+r)^n / ((1+r)^n - 1)`, rounded to 2 decimals, with a `CASE` for a zero rate, where that formula divides by zero (it gives NULL in SQLite, printed in the run) and the EMI is just `principal / months`.
- The recursion carries only the opening balance (loan, month, opening). Each step computes the next opening as `opening - principal_paid`, where the principal paid is the EMI minus that month's interest, except in the last month, where it is the whole remaining balance. That `CASE` is the last-row rounding fix: the last payment is `interest + remaining balance`, a few paise different from the EMI.
- Interest, principal paid, payment and closing balance are derived from the opening balance in the outer select `x` (a column alias cannot be reused in the same select list, so I keep the carried state small).
- No cycle is possible (`month` only rises) and `WHERE s.month < l.months` ends each loan.

**pandas answer:** a plain Python/pandas loop with the same rounding rule (shown once, identical to the Code block). `r2` is the half-up rounding helper defined in the Code block, because SQLite's `ROUND` rounds halves away from zero while Python's built-in `round` and numpy/pandas round halves to even:
```py
    grow = accounts.assign(bal=accounts["balance"])
    for _ in range(12):
        grow["bal"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0)) for b, rt in zip(grow["bal"], grow["annual_rate"])]
    grow["closed_form"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0) ** 12) for b, rt in zip(grow["balance"], grow["annual_rate"])]
    rows = []
    for ln in loans.itertuples():
        r = ln.annual_rate / 12.0
        emi = r2(ln.principal / ln.months) if ln.annual_rate == 0 else r2(ln.principal * r * (1 + r) ** ln.months / ((1 + r) ** ln.months - 1))
        opening = ln.principal
        for m in range(1, ln.months + 1):
            interest = r2(opening * r)
            paid = opening if m == ln.months else emi - interest
            rows.append((ln.loan_id, m, opening, interest, r2(paid), r2(interest + paid), r2(opening - paid)))
            opening = r2(opening - paid)
    sch = pd.DataFrame(rows, columns=["loan_id", "month", "opening", "interest", "principal_paid", "payment", "closing"])
    return grow, sch
```

**Example:** the 10000 loan at 1 percent a month for 6 months.
- EMI = 10000 x 0.01 x 1.01^6 / (1.01^6 - 1) = 1725.48 (rounded).
- Month 1: interest 100.00, principal 1725.48 - 100.00 = 1625.48, closing 8374.52. Month 2: interest 83.75, principal 1641.73, closing 6732.79. And so on to month 5 closing 1708.43.
- Month 6: interest 17.08. Normal payment would repay 1725.48 - 17.08 = 1708.40 of principal, leaving 0.03 owing. The fix pays the whole 1708.43, so the last payment is 1725.51 and the closing balance is 0.00. Without the fix the final closing is 0.03 (printed).
- Total interest 352.91 and total paid 10352.91 (printed).
- Account 1: 1000 at 1 percent a month: closed form 1000 x 1.01^12 = 1126.8250, rounded 1126.83; monthly rounding gives 1126.84, a difference of 1 paisa.

**Code:** run with `python3 -I`. Asserts: pandas/Python growth and schedule equal the SQL results (rounded to 2 decimals, compared after sorting by loan and month), principal paid sums to the loan amount, and every final closing balance is 0.
```python
# Q18: compound interest and loan amortisation with recursive CTEs, checked against the closed form and a Python loop
import sqlite3
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd

SCHEMA = """
CREATE TABLE accounts(acct_id INTEGER PRIMARY KEY, balance REAL, annual_rate REAL);
INSERT INTO accounts VALUES (1,1000,0.12),(2,2500,0.075),(3,100.55,0.06),(4,800,0.0),(5,500,NULL);
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal REAL, annual_rate REAL, months INTEGER);
INSERT INTO loans VALUES (1,10000,0.12,6),(2,5000,0.0,4),(3,1200,0.18,1);
"""
SQL_GROWTH = """
WITH RECURSIVE g(acct_id, month, bal) AS (
  SELECT acct_id, 0, balance FROM accounts
  UNION ALL
  SELECT g.acct_id, g.month + 1, ROUND(g.bal * (1 + a.annual_rate / 12.0), 2)
  FROM g JOIN accounts a ON a.acct_id = g.acct_id
  WHERE g.month < 12
)
SELECT g.acct_id, g.bal AS monthly_rounded,
       ROUND(a.balance * power(1 + a.annual_rate / 12.0, 12), 2) AS closed_form,
       ROUND(g.bal - a.balance * power(1 + a.annual_rate / 12.0, 12), 4) AS difference
FROM g JOIN accounts a ON a.acct_id = g.acct_id
WHERE g.month = 12
ORDER BY g.acct_id
"""
SQL_MAIN = """
WITH RECURSIVE l AS (
  SELECT loan_id, principal, months, annual_rate / 12.0 AS r,
         CASE WHEN annual_rate = 0 THEN ROUND(principal / months, 2)
              ELSE ROUND(principal * (annual_rate / 12.0) * power(1 + annual_rate / 12.0, months)
                         / (power(1 + annual_rate / 12.0, months) - 1), 2) END AS emi
  FROM loans
), s(loan_id, month, opening) AS (
  SELECT loan_id, 1, principal FROM l
  UNION ALL
  SELECT s.loan_id, s.month + 1,
         ROUND(s.opening - CASE WHEN s.month = l.months THEN s.opening
                                ELSE l.emi - ROUND(s.opening * l.r, 2) END, 2)
  FROM s JOIN l ON l.loan_id = s.loan_id
  WHERE s.month < l.months
), x AS (
  SELECT s.loan_id, s.month, s.opening, l.emi,
         ROUND(s.opening * l.r, 2) AS interest,
         CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END AS principal_paid
  FROM s JOIN l ON l.loan_id = s.loan_id
)
SELECT loan_id, month, opening, interest, ROUND(principal_paid, 2) AS principal_paid,
       ROUND(interest + principal_paid, 2) AS payment,
       ROUND(opening - principal_paid, 2) AS closing
FROM x
ORDER BY loan_id, month
"""
SQL_NOFIX = SQL_MAIN.replace("CASE WHEN s.month = l.months THEN s.opening ELSE l.emi - ROUND(s.opening * l.r, 2) END", "l.emi - ROUND(s.opening * l.r, 2)")
assert SQL_NOFIX != SQL_MAIN
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
g = pd.read_sql_query(SQL_GROWTH, con)
print("(a) 12 months of monthly compounding, rounded to 2 decimals each month, versus the closed form:")
print(g.to_string(index=False))
sched = pd.read_sql_query(SQL_MAIN, con)
print("(b) amortisation schedules (loan 1 is 10000 at 12 percent for 6 months):")
print(sched.to_string(index=False))
print("EMI per loan:", dict(con.execute("SELECT loan_id, ROUND(principal*(annual_rate/12.0)*power(1+annual_rate/12.0,months)/(power(1+annual_rate/12.0,months)-1),2) FROM loans WHERE annual_rate > 0").fetchall()))
nofix = pd.read_sql_query(SQL_NOFIX, con)
print("without the last-row fix, closing balance after the last month:", nofix.groupby("loan_id")["closing"].last().to_dict())
print("with the fix:", sched.groupby("loan_id")["closing"].last().to_dict())

accounts = pd.read_sql_query("SELECT * FROM accounts", con)
loans = pd.read_sql_query("SELECT * FROM loans", con)

def r2(x):
    return float(Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def pandas_side(accounts, loans):
    # pd:main
    grow = accounts.assign(bal=accounts["balance"])
    for _ in range(12):
        grow["bal"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0)) for b, rt in zip(grow["bal"], grow["annual_rate"])]
    grow["closed_form"] = [None if pd.isna(rt) else r2(b * (1 + rt / 12.0) ** 12) for b, rt in zip(grow["balance"], grow["annual_rate"])]
    rows = []
    for ln in loans.itertuples():
        r = ln.annual_rate / 12.0
        emi = r2(ln.principal / ln.months) if ln.annual_rate == 0 else r2(ln.principal * r * (1 + r) ** ln.months / ((1 + r) ** ln.months - 1))
        opening = ln.principal
        for m in range(1, ln.months + 1):
            interest = r2(opening * r)
            paid = opening if m == ln.months else emi - interest
            rows.append((ln.loan_id, m, opening, interest, r2(paid), r2(interest + paid), r2(opening - paid)))
            opening = r2(opening - paid)
    sch = pd.DataFrame(rows, columns=["loan_id", "month", "opening", "interest", "principal_paid", "payment", "closing"])
    return grow, sch
    # pd:end

grow, sch = pandas_side(accounts, loans)
cmp_g = grow[grow["annual_rate"].notna()][["acct_id", "bal", "closed_form"]].reset_index(drop=True)
g_ok = g[g["monthly_rounded"].notna()].reset_index(drop=True)
assert (cmp_g["bal"].round(2).to_numpy() == g_ok["monthly_rounded"].round(2).to_numpy()).all()
assert (cmp_g["closed_form"].round(2).to_numpy() == g_ok["closed_form"].round(2).to_numpy()).all()
print("pandas/Python growth loop equals SQL (rounded balance and closed form) for the 4 accounts with a rate; account 5 (NULL rate) stays NULL in SQL:", g.loc[g.acct_id == 5, "monthly_rounded"].isna().all())
pd.testing.assert_frame_equal(sch.round(2), sched.round(2), check_dtype=False)   # compared after sorting by loan_id, month
assert abs(sched.groupby("loan_id")["principal_paid"].sum().round(2) - loans.set_index("loan_id")["principal"]).max() < 1e-6
assert (sched.groupby("loan_id")["closing"].last() == 0).all()
print("pandas schedule equal to SQL; principal paid sums to the loan amount; last closing balance is 0")
print("total interest on loan 1:", round(sched[sched.loan_id == 1]["interest"].sum(), 2), "| total paid:", round(sched[sched.loan_id == 1]["payment"].sum(), 2))
print("zero-rate formula without the CASE:", con.execute("SELECT 5000 * 0 * power(1, 4) / (power(1, 4) - 1)").fetchone(), "(division by zero gives NULL in SQLite)")
print("exp/ln check of power(): ", con.execute("SELECT ROUND(power(1.01, 12), 10), ROUND(exp(12 * ln(1.01)), 10)").fetchone())
print("asserts passed")
```

**Output (my run):**
```text
(a) 12 months of monthly compounding, rounded to 2 decimals each month, versus the closed form:
 acct_id  monthly_rounded  closed_form  difference
       1          1126.84      1126.83      0.0150
       2          2694.08      2694.08     -0.0015
       3           106.76       106.75      0.0083
       4           800.00       800.00      0.0000
       5              NaN          NaN         NaN
(b) amortisation schedules (loan 1 is 10000 at 12 percent for 6 months):
 loan_id  month  opening  interest  principal_paid  payment  closing
       1      1 10000.00    100.00         1625.48  1725.48  8374.52
       1      2  8374.52     83.75         1641.73  1725.48  6732.79
       1      3  6732.79     67.33         1658.15  1725.48  5074.64
       1      4  5074.64     50.75         1674.73  1725.48  3399.91
       1      5  3399.91     34.00         1691.48  1725.48  1708.43
       1      6  1708.43     17.08         1708.43  1725.51     0.00
       2      1  5000.00      0.00         1250.00  1250.00  3750.00
       2      2  3750.00      0.00         1250.00  1250.00  2500.00
       2      3  2500.00      0.00         1250.00  1250.00  1250.00
       2      4  1250.00      0.00         1250.00  1250.00     0.00
       3      1  1200.00     18.00         1200.00  1218.00     0.00
EMI per loan: {1: 1725.48, 3: 1218.0}
without the last-row fix, closing balance after the last month: {1: 0.03, 2: 0.0, 3: 0.0}
with the fix: {1: 0.0, 2: 0.0, 3: 0.0}
pandas/Python growth loop equals SQL (rounded balance and closed form) for the 4 accounts with a rate; account 5 (NULL rate) stays NULL in SQL: True
pandas schedule equal to SQL; principal paid sums to the loan amount; last closing balance is 0
total interest on loan 1: 352.91 | total paid: 10352.91
zero-rate formula without the CASE: (None,) (division by zero gives NULL in SQLite)
exp/ln check of power():  (1.1268250301, 1.1268250301)
asserts passed
```
Honest notes from the run:
- The month-by-month balance and the closed form disagree on two of the four rated accounts by 1 paisa (1126.84 versus 1126.83, 106.76 versus 106.75) and agree after rounding on the other two (the unrounded difference column shows 0.015, -0.0015, 0.0083 and 0); it is rounding, not a bug.
- `power` and `exp`/`ln` worked in this SQLite 3.45.1 build (the math functions are compiled in here; I verified `power(1.01, 12)` equals `exp(12 * ln(1.01))` to 10 places). Other SQLite builds may not have them, and the other engines are described below as not executed.
- SQLite `ROUND` and Python round differ on exact halves (Part 8 lesson: 2.675 style cases), so I used a half-up helper in Python; on this data the two agreed everywhere.

**Edge cases:**
- Zero rate: the EMI formula divides by zero (NULL in SQLite; an error in most other engines, not executed here), so a `CASE` is required.
- NULL rate (account 5): every month's balance is NULL and the closed form is NULL; filter or `COALESCE(rate, 0)` according to the business rule.
- One-month loan: the anchor row is also the last row; the fix makes the payment `principal + interest` (1218.00).
- Rounding: rounding each month's interest to paise is what a real lender's statement does, so the schedule is the truth and the closed form is only a check.
- Months in the table are whole numbers. Annual percent versus decimal and day-count conventions (actual/365 versus 30/360) are assumptions; I stated the 1/12 rule.
- Negative or zero principal: not handled; add a check.

**Then explain:**
- Why recursion: the balance after month m depends on the rounded balance of month m-1, which depends on its own. Without rounding there is a closed form (a power), and a window function over a numbers table could produce it; with per-month rounding the state matters and recursion (or a loop) is the exact method.
- `power` is available in this build; the portable alternatives are `POW` or `POWER` in PostgreSQL, MySQL, SQL Server (`POWER`) and Oracle (`POWER`), and `exp(n * ln(1+r))` where only `exp` and `ln` exist. I did not run any of these (not executed).
- An integer-division trap: `annual_rate / 12` with integer columns would truncate; I divide by `12.0`.
- Money in a real system should use `DECIMAL`/`NUMERIC` (exact), not binary floats; SQLite has no true decimal type, so the toy uses `REAL` and rounds each step.

**Follow-ups:**
- "Add a prepayment in month 3?" Subtract it from the opening balance in the recursive step for that month; the later EMI would be recomputed or the term shortened.
- "Interest only for the first 2 months?" `CASE WHEN month <= 2` changes the principal paid to 0.
- "Why not just use the closed form for the balance after k months?" It is fine for an unrounded balance: `P(1+r)^k - EMI * ((1+r)^k - 1)/r`; the schedule gives the rounded figures the customer actually sees.

**Common mistakes:**
- Dividing by zero for a 0 percent loan.
- Letting the last row carry the normal EMI and leaving 0.03 owing (or overpaying).
- Integer division in the monthly rate.
- Rounding only at the end and then not reconciling with the statement.
- Forgetting the cap `month < months`, so the recursion keeps producing rows past the term.

---

### Q19 ⭐⭐ 🟡 Other state-dependent running calculations: daily_prices(day, close) and assets(asset_id, cost, life_years, rate). Compute (a) an exponentially weighted moving average s_t = a * x_t + (1 - a) * s_(t-1) with a = 0.3 using a recursive CTE, (b) a declining-balance depreciation schedule (book value times a fixed rate each year, floored at a salvage value), and (c) show with a short argument why neither is a plain window function. Verify (a) with pandas ewm(alpha=0.3, adjust=False).mean() and assert equality, and note the rounding and first-row (seed) conventions that make a result differ by the adjust parameter.
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Both are "this period's value depends on last period's value", so a recursive CTE carries the previous value; but a premise check first: neither is strictly impossible as a non-recursive query (EWMA has a weighted-sum closed form that overflows on long series, and the floored declining balance is just `MAX(salvage, cost * (1 - rate)^year)`), what is true is that no built-in window function does either one, and the recursion is the transparent, numerically safe way.

**Schema and sample data:** ten daily closes (03-09 and 03-10 are missing from the calendar; the series is treated by row, not by calendar day) and three assets. The question's `assets` table lists cost, life_years and rate and a floor "at a salvage value", so I added a `salvage` column to hold it.
```sql
CREATE TABLE daily_prices(day TEXT, close REAL);
INSERT INTO daily_prices VALUES
 ('2024-03-01',100),('2024-03-02',102),('2024-03-03',101),('2024-03-04',105),('2024-03-05',103),
 ('2024-03-06',108),('2024-03-07',110),('2024-03-08',107),('2024-03-11',111),('2024-03-12',115);
CREATE TABLE assets(asset_id INTEGER PRIMARY KEY, cost REAL, life_years INTEGER, rate REAL, salvage REAL);
INSERT INTO assets VALUES (1,10000,6,0.40,1000),(2,5000,3,0.25,500),(3,800,4,0.50,100);
```

**SQL answer:** (a) `SQL_MAIN` in the Code block, the EWMA with alpha 0.3:
```sql
WITH RECURSIVE p AS (
  SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices
), s(rn, day, close, ewma) AS (
  SELECT rn, day, close, close FROM p WHERE rn = 1
  UNION ALL
  SELECT p.rn, p.day, p.close, 0.3 * p.close + (1 - 0.3) * s.ewma
  FROM s JOIN p ON p.rn = s.rn + 1
)
SELECT day, close, ewma FROM s ORDER BY rn
```
The anchor is the first price (the seed: `s_1 = x_1`); each step is `0.3 * x_t + 0.7 * s_(t-1)`, joined to the next row number. (b) `SQL_DEPR` in the Code block, declining balance with the salvage floor; the book value is carried and `MAX(salvage, book * (1 - rate))` applies the floor; the depreciation of a year is the previous book value minus the new one (`LAG` is applied outside the recursion, which is allowed):
```sql
WITH RECURSIVE b(asset_id, year, book) AS (
  SELECT asset_id, 0, cost FROM assets
  UNION ALL
  SELECT b.asset_id, b.year + 1, MAX(a.salvage, b.book * (1 - a.rate))
  FROM b JOIN assets a ON a.asset_id = b.asset_id
  WHERE b.year < a.life_years
)
SELECT asset_id, year, ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year), 2) AS opening,
       ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year) - book, 2) AS depreciation,
       ROUND(book, 2) AS closing
FROM b
ORDER BY asset_id, year
```

**pandas answer:** `ewm` for (a) and a plain loop for (b) (shown once, identical to the Code block):
```py
    ewma = prices.sort_values("day")["close"].ewm(alpha=0.3, adjust=False).mean()
    rows = []
    for a in assets.itertuples():
        book = a.cost
        rows.append((a.asset_id, 0, np.nan, np.nan, book))
        for y in range(1, a.life_years + 1):
            new = max(a.salvage, book * (1 - a.rate))
            rows.append((a.asset_id, y, book, book - new, new))
            book = new
    depr = pd.DataFrame(rows, columns=["asset_id", "year", "opening", "depreciation", "closing"])
    return ewma, depr
```

**Example:** by hand.
- EWMA: s_1 = 100. s_2 = 0.3 x 102 + 0.7 x 100 = 100.6. s_3 = 0.3 x 101 + 0.7 x 100.6 = 100.72. s_4 = 0.3 x 105 + 0.7 x 100.72 = 102.004.
- Depreciation for asset 1 (cost 10000, 40 percent, floor 1000): book values 6000, 3600, 2160, 1296; the next would be 777.6, below the floor, so year 5 books 296.00 of depreciation to reach 1000 and year 6 books 0. Asset 3 (rate 50 percent, floor 100): 400, 200, 100, then 0.
- Asset 2 (25 percent): 3750, 2812.50, 2109.375; the year 3 depreciation is exactly 703.125, a rounding tie (see below).

**Code:** run with `python3 -I`. Asserts: pandas `ewm(alpha=0.3, adjust=False)` equals the recursive CTE to 1e-9; the Python depreciation loop equals the SQL schedule (compared after sorting by asset and year; SQLite `ROUND` rounds halves away from zero, so the pandas side uses a half-up helper); the closed forms equal the recursive results.
```python
# Q19: EWMA and declining-balance depreciation with recursive CTEs, checked against pandas ewm and closed forms
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE daily_prices(day TEXT, close REAL);
INSERT INTO daily_prices VALUES
 ('2024-03-01',100),('2024-03-02',102),('2024-03-03',101),('2024-03-04',105),('2024-03-05',103),
 ('2024-03-06',108),('2024-03-07',110),('2024-03-08',107),('2024-03-11',111),('2024-03-12',115);
CREATE TABLE assets(asset_id INTEGER PRIMARY KEY, cost REAL, life_years INTEGER, rate REAL, salvage REAL);
INSERT INTO assets VALUES (1,10000,6,0.40,1000),(2,5000,3,0.25,500),(3,800,4,0.50,100);
"""
SQL_MAIN = """
WITH RECURSIVE p AS (
  SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices
), s(rn, day, close, ewma) AS (
  SELECT rn, day, close, close FROM p WHERE rn = 1
  UNION ALL
  SELECT p.rn, p.day, p.close, 0.3 * p.close + (1 - 0.3) * s.ewma
  FROM s JOIN p ON p.rn = s.rn + 1
)
SELECT day, close, ewma FROM s ORDER BY rn
"""
SQL_DEPR = """
WITH RECURSIVE b(asset_id, year, book) AS (
  SELECT asset_id, 0, cost FROM assets
  UNION ALL
  SELECT b.asset_id, b.year + 1, MAX(a.salvage, b.book * (1 - a.rate))
  FROM b JOIN assets a ON a.asset_id = b.asset_id
  WHERE b.year < a.life_years
)
SELECT asset_id, year, ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year), 2) AS opening,
       ROUND(LAG(book) OVER (PARTITION BY asset_id ORDER BY year) - book, 2) AS depreciation,
       ROUND(book, 2) AS closing
FROM b
ORDER BY asset_id, year
"""
# closed forms: no recursion needed for either, shown to prove the recursion is not the only way
SQL_EWMA_CLOSED = """
WITH p AS (SELECT day, close, ROW_NUMBER() OVER (ORDER BY day) AS rn FROM daily_prices)
SELECT day, close,
       SUM(CASE WHEN rn = 1 THEN close / 0.7 ELSE 0.3 * close * power(0.7, -rn) END)
         OVER (ORDER BY rn ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * power(0.7, rn) AS ewma
FROM p ORDER BY rn
"""
SQL_DEPR_CLOSED = """
WITH RECURSIVE y(asset_id, year) AS (
  SELECT asset_id, 0 FROM assets
  UNION ALL SELECT y.asset_id, y.year + 1 FROM y JOIN assets a ON a.asset_id = y.asset_id WHERE y.year < a.life_years
)
SELECT y.asset_id, y.year, ROUND(MAX(a.salvage, a.cost * power(1 - a.rate, y.year)), 2) AS closing
FROM y JOIN assets a ON a.asset_id = y.asset_id
WHERE y.year >= 1 ORDER BY y.asset_id, y.year
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ew = pd.read_sql_query(SQL_MAIN, con)
dep = pd.read_sql_query(SQL_DEPR, con)
print("(a) EWMA, alpha 0.3, seed s_1 = x_1:")
print(ew.round(4).to_string(index=False))
print("(b) declining balance with a salvage floor (year 0 rows have no depreciation):")
print(dep.to_string(index=False))

prices = pd.read_sql_query("SELECT * FROM daily_prices", con)
assets = pd.read_sql_query("SELECT * FROM assets", con)

def pandas_side(prices, assets):
    # pd:main
    ewma = prices.sort_values("day")["close"].ewm(alpha=0.3, adjust=False).mean()
    rows = []
    for a in assets.itertuples():
        book = a.cost
        rows.append((a.asset_id, 0, np.nan, np.nan, book))
        for y in range(1, a.life_years + 1):
            new = max(a.salvage, book * (1 - a.rate))
            rows.append((a.asset_id, y, book, book - new, new))
            book = new
    depr = pd.DataFrame(rows, columns=["asset_id", "year", "opening", "depreciation", "closing"])
    return ewma, depr
    # pd:end

pd_ewma, pd_dep = pandas_side(prices, assets)
np.testing.assert_allclose(pd_ewma.to_numpy(), ew["ewma"].to_numpy(), rtol=0, atol=1e-9)
half_up = lambda col: np.floor(col * 100 + 0.5) / 100   # SQLite ROUND rounds halves away from zero (positive values here)
pd.testing.assert_frame_equal(pd_dep.assign(**{c: half_up(pd_dep[c]) for c in ("opening", "depreciation", "closing")}), dep, check_dtype=False)   # compared after sorting by asset_id, year
print("depreciation of asset 2, year 3 is exactly 703.125: SQLite ROUND gives", dep.loc[(dep.asset_id == 2) & (dep.year == 3), "depreciation"].iloc[0], "| pandas .round(2) gives", pd_dep.round(2).loc[(pd_dep.asset_id == 2) & (pd_dep.year == 3), "depreciation"].iloc[0], "(half to even)")
print("pandas ewm(alpha=0.3, adjust=False) equals the recursive CTE (atol 1e-9); depreciation loop equals SQL")

# conventions
adj = prices["close"].ewm(alpha=0.3, adjust=True).mean()
seed0 = [0.0]
for x in prices["close"]:
    seed0.append(0.3 * x + 0.7 * seed0[-1])
cmp = pd.DataFrame({"day": prices["day"], "recursive_seed_x1": ew["ewma"].round(4), "pandas_adjust_False": pd_ewma.round(4),
                    "pandas_adjust_True": adj.round(4), "seed_zero": np.round(seed0[1:], 4)})
print("conventions (first rows):")
print(cmp.head(4).to_string(index=False))
print("max abs difference adjust=True vs adjust=False over 10 rows:", round(float((adj - pd_ewma).abs().max()), 4), "| last row:", round(float((adj - pd_ewma).abs().iloc[-1]), 6))

# closed forms
cf = pd.read_sql_query(SQL_EWMA_CLOSED, con)
np.testing.assert_allclose(cf["ewma"].to_numpy(), ew["ewma"].to_numpy(), rtol=0, atol=1e-9)
dc = pd.read_sql_query(SQL_DEPR_CLOSED, con)
assert dc["closing"].tolist() == dep[dep.year >= 1]["closing"].tolist()
print("closed forms (weighted running SUM for EWMA, MAX(salvage, cost * (1-rate)^year) for depreciation) equal the recursive results")
# numerical limit of the EWMA closed form: power(0.7, -n) overflows
con.execute("CREATE TABLE long_p(day TEXT, close REAL)")
con.executemany("INSERT INTO long_p VALUES (?, ?)", [(f"{i:05d}", 100.0 + (i % 7)) for i in range(1, 2401)])
lp = pd.read_sql_query(SQL_EWMA_CLOSED.replace("daily_prices", "long_p"), con)
lr = pd.read_sql_query(SQL_MAIN.replace("daily_prices", "long_p"), con)
bad = lp["ewma"].isna() | ((lp["ewma"] - lr["ewma"]).abs() > 1e-6)
print("2400-row series: first row where the closed form is wrong or NULL:", int(bad.idxmax()) + 1 if bad.any() else None, "| recursive form fine to the end:", float(lr["ewma"].iloc[-1].round(4)))

# NULL close: SQL recursion carries the previous value; pandas ewm weights by position
con.execute("UPDATE daily_prices SET close = NULL WHERE day = '2024-03-05'")
sn = pd.read_sql_query(SQL_MAIN.replace("0.3 * p.close + (1 - 0.3) * s.ewma", "CASE WHEN p.close IS NULL THEN s.ewma ELSE 0.3 * p.close + (1 - 0.3) * s.ewma END"), con)
pn = pd.read_sql_query("SELECT * FROM daily_prices", con)["close"].ewm(alpha=0.3, adjust=False).mean()
pni = pd.read_sql_query("SELECT * FROM daily_prices", con)["close"].ewm(alpha=0.3, adjust=False, ignore_na=True).mean()
print("NULL close on 2024-03-05, rows 5 to 7: SQL carry-forward", sn["ewma"].round(4).tolist()[4:7], "| pandas default", pn.round(4).tolist()[4:7], "| pandas ignore_na=True", pni.round(4).tolist()[4:7])
print("empty prices ->", con.execute(SQL_MAIN.replace("FROM daily_prices", "FROM daily_prices WHERE 1 = 0")).fetchall())
print("asserts passed")
```

**Output (my run):**
```text
(a) EWMA, alpha 0.3, seed s_1 = x_1:
       day  close     ewma
2024-03-01  100.0 100.0000
2024-03-02  102.0 100.6000
2024-03-03  101.0 100.7200
2024-03-04  105.0 102.0040
2024-03-05  103.0 102.3028
2024-03-06  108.0 104.0120
2024-03-07  110.0 105.8084
2024-03-08  107.0 106.1659
2024-03-11  111.0 107.6161
2024-03-12  115.0 109.8313
(b) declining balance with a salvage floor (year 0 rows have no depreciation):
 asset_id  year  opening  depreciation  closing
        1     0      NaN           NaN 10000.00
        1     1  10000.0       4000.00  6000.00
        1     2   6000.0       2400.00  3600.00
        1     3   3600.0       1440.00  2160.00
        1     4   2160.0        864.00  1296.00
        1     5   1296.0        296.00  1000.00
        1     6   1000.0          0.00  1000.00
        2     0      NaN           NaN  5000.00
        2     1   5000.0       1250.00  3750.00
        2     2   3750.0        937.50  2812.50
        2     3   2812.5        703.13  2109.38
        3     0      NaN           NaN   800.00
        3     1    800.0        400.00   400.00
        3     2    400.0        200.00   200.00
        3     3    200.0        100.00   100.00
        3     4    100.0          0.00   100.00
depreciation of asset 2, year 3 is exactly 703.125: SQLite ROUND gives 703.13 | pandas .round(2) gives 703.12 (half to even)
pandas ewm(alpha=0.3, adjust=False) equals the recursive CTE (atol 1e-9); depreciation loop equals SQL
conventions (first rows):
       day  recursive_seed_x1  pandas_adjust_False  pandas_adjust_True  seed_zero
2024-03-01            100.000              100.000            100.0000     30.000
2024-03-02            100.600              100.600            101.1765     51.600
2024-03-03            100.720              100.720            101.0959     66.420
2024-03-04            102.004              102.004            102.6372     77.994
max abs difference adjust=True vs adjust=False over 10 rows: 0.6332 | last row: 0.285782
closed forms (weighted running SUM for EWMA, MAX(salvage, cost * (1-rate)^year) for depreciation) equal the recursive results
2400-row series: first row where the closed form is wrong or NULL: 1978 | recursive form fine to the end: 104.2949
NULL close on 2024-03-05, rows 5 to 7: SQL carry-forward [102.004, 103.8028, 105.662] | pandas default [102.004, 104.281, 105.9967] | pandas ignore_na=True [102.004, 103.8028, 105.662]
empty prices -> []
asserts passed
```
Honest notes from the run:
- Rounding surprise: the year 3 depreciation of asset 2 is exactly 703.125. SQLite `ROUND(x, 2)` gives 703.13 and pandas `.round(2)` gives 703.12 (half to even). The first version of my assert failed on exactly this, which is why the code compares through a half-up helper.
- Conventions for (a): `adjust=False` is the recursive formula with the first value as the seed, so it equals the CTE. `adjust=True` (the pandas default) computes a weighted average of all earlier values with weights that sum to 1 at every step; its first rows differ (101.1765 versus 100.6 on day 2) and the difference is still 0.29 on day 10. A seed of 0 (starting from `s_0 = 0`) pulls the first values far below the price (30.0 on day 1), which is why the first value is usually the seed.
- The window-function closed form of the EWMA (a running `SUM` of `0.3 * x * power(0.7, -rn)` times `power(0.7, rn)`) matches the recursion on 10 rows, but on a 2400-row test series it went wrong from row 1978 (the large powers lose precision and then overflow); the recursion stayed fine to the end. That is the reason I would not use it in production.
- NULL close: with a `CASE` that carries the previous value, SQL gives 102.004, 103.8028, 105.662 on the NULL day and the two days after; pandas default `ewm` gives 102.004, 104.281, 105.9967 (it weights by position, so the gap makes the old value decay), and `ignore_na=True` gives the same numbers as the SQL carry-forward.

**Edge cases:**
- First row is the seed (assumption). Say it out loud; interviewers differ on `s_0 = 0` versus `s_1 = x_1`.
- NULL price: the recursive step must decide (carry the previous EWMA, as I did, or skip); an unguarded `0.3 * NULL + ...` gives NULL for the rest of the series.
- Weekend or missing days: this EWMA is by row, not by calendar time; a time-weighted EWMA needs the gap length in the weight.
- Empty table: no anchor, empty result (printed).
- Floor already above cost, rate 0, or salvage 0: handled by the formula (book never goes below the floor; rate 0 keeps the book value).
- Duplicate days: `ROW_NUMBER` would number them arbitrarily; deduplicate first.

**Then explain (c), why neither is a plain window function:**
- A window function computes an aggregate over a frame of input values with fixed or running weights. An EWMA has weights that decay with distance, and the built-in aggregates (`SUM`, `AVG`, ...) have no weight parameter, so the engine gives you nothing that applies `0.7^k`. The declining balance multiplies by a constant each year, which is not an aggregate either.
- The recursive member is the natural expression because the next value is a function of the previous output. That is a "fold", and recursion is how SQL expresses a fold.
- Closed forms exist (shown and asserted): EWMA as a weighted running sum scaled by powers, depreciation as `MAX(salvage, cost * (1-rate)^year)`. The depreciation closed form is better than recursion where it applies. A truly state-dependent variant that would still need recursion is the switch-to-straight-line rule (change method when straight-line depreciation exceeds the declining balance), which I did not run.
- Other engines (not executed here): the same queries work in PostgreSQL and MySQL 8 with `WITH RECURSIVE` and in SQL Server without the keyword; `POWER` exists in all of them (from memory, not executed). SQL Server's `OPTION (MAXRECURSION)` and MySQL's `cte_max_recursion_depth` limit long series.

**Follow-ups:**
- "How do you pick alpha from a span?" `alpha = 2 / (span + 1)`, so span 9 gives 0.2 (a pandas documented relation; I did not run other spans here).
- "EWMA by calendar day with gaps?" Weight by the number of days since the last observation: `alpha_eff = 1 - (1 - alpha)^gap_days`.
- "Why not keep the series in pandas?" For one series pandas is simpler and faster; in SQL it is for data that is already there or too big to move.

**Common mistakes:**
- Assuming pandas `ewm` default equals the recursive formula (the default is `adjust=True`).
- Starting from `s_0 = 0` and getting a biased start.
- Comparing floats with `==` instead of a tolerance.
- Letting book value fall below the salvage value, or depreciating past the useful life.
- Using the weighted-sum closed form on long series and getting NULL or garbage from huge powers.

---

### Q20 ⭐⭐ 🟡 Delete or move a subtree with a recursive CTE: categories(category_id, parent_id, name, path) and employees(emp_id, manager_id). Delete category 5 and everything under it with DELETE ... WHERE category_id IN (WITH RECURSIVE ... SELECT ...), show the rows before and after, then move subtree 8 under parent 2 and rebuild the materialised path of all descendants, and prevent a move that would create a cycle (the new parent must not be a descendant of the moved node). State what a foreign key with ON DELETE CASCADE does instead, and which statements are portable (SQL Server needs the CTE before the DELETE, MySQL 8 supports CTE with DELETE, both hedged, not executed).
**Asked at:** expert gap-check from practice, no candidate report found; analyst, data scientist and data engineer rounds at product companies and GCCs; tested on SQLite 3.45.1
**Say this first (1 line):** Find the subtree with a recursive CTE and delete by id (`DELETE ... WHERE category_id IN (WITH RECURSIVE ... SELECT id FROM sub)`), move it by updating one `parent_id` and then rebuilding the `path` of the moved node and all its descendants from the new parent's path, and before any move check that the new parent is not inside the moved subtree, because that would create a cycle; a foreign key with `ON DELETE CASCADE` can do the delete without a recursive query, if the engine enforces it.

**Schema and sample data:** a ten-row category tree with a materialised path (`'/1/5/6/'` means 1 > 5 > 6) and a seven-row employee table. Category 5 (Electronics) has Phones (6), Laptops (7) and Android (9, under Phones); category 8 (Garden) has Tools (10), Lawn (11) and Spades (12, under Tools).
```sql
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Store','/1/'),(2,1,'Home','/1/2/'),(5,1,'Electronics','/1/5/'),(6,5,'Phones','/1/5/6/'),
 (7,5,'Laptops','/1/5/7/'),(9,6,'Android','/1/5/6/9/'),(8,1,'Garden','/1/8/'),(10,8,'Tools','/1/8/10/'),
 (11,8,'Lawn','/1/8/11/'),(12,10,'Spades','/1/8/10/12/');
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES (1,NULL),(2,1),(3,1),(4,3),(5,3),(6,4),(7,2);
```

**SQL answer:** the delete is `SQL_MAIN` in the Code block:
```sql
DELETE FROM categories
WHERE category_id IN (
  WITH RECURSIVE sub(id) AS (
    SELECT category_id FROM categories WHERE category_id = 5
    UNION ALL
    SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
  )
  SELECT id FROM sub
)
```
The same pattern for the employee table, deleting manager 3 and everyone below, is `SQL_DELETE_EMP` in the Code block:
```sql
DELETE FROM employees
WHERE emp_id IN (
  WITH RECURSIVE team(id) AS (
    SELECT emp_id FROM employees WHERE emp_id = 3
    UNION ALL SELECT e.emp_id FROM employees e JOIN team t ON e.manager_id = t.id
  )
  SELECT id FROM team
)
```
The move is two statements in one transaction (`SQL_MOVE_PARENT` and `SQL_MOVE_PATHS` in the Code block), after a cycle check (`SQL_CYCLE_CHECK`):
```sql
WITH RECURSIVE sub(id) AS (
  SELECT :moved
  UNION
  SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
)
SELECT COUNT(*) FROM sub WHERE id = :newparent
```
```sql
UPDATE categories SET parent_id = :newparent WHERE category_id = :moved
```
```sql
WITH RECURSIVE t(id, newpath) AS (
  SELECT c.category_id, p.path || c.category_id || '/'
  FROM categories c JOIN categories p ON p.category_id = c.parent_id
  WHERE c.category_id = :moved
  UNION ALL
  SELECT c.category_id, t.newpath || c.category_id || '/'
  FROM categories c JOIN t ON c.parent_id = t.id
)
UPDATE categories SET path = (SELECT newpath FROM t WHERE t.id = categories.category_id)
WHERE category_id IN (SELECT id FROM t)
```
How it works:
- Delete: the recursive CTE starts at the chosen category and adds children until there are none; the outer `DELETE` removes those ids. The subquery is evaluated before rows disappear, so deleting the table you are reading from is safe in SQLite.
- Move: `UPDATE ... SET parent_id` re-attaches the node. The path rebuild is a second recursive CTE: the anchor is the moved node with `new parent's path || its id || '/'`, and each step appends a child's id to its parent's new path. The `UPDATE` then sets every affected row's path from the CTE. A string `REPLACE` of the old prefix would also work for a pure prefix change (not run).
- Cycle check: the subtree of the moved node (including the node itself) is built with `UNION`, so even a data cycle cannot loop; if the proposed new parent is in it, the move is refused. With the materialised path this is simply `new_parent.path LIKE moved.path || '%'` (not run separately here).
- The helper `move()` in the Code block wraps check and both updates in one transaction (`with con:`), so a failure cannot leave the parent changed and the paths stale.

**pandas answer:** a stack-based subtree walk, a drop for the delete and a path rebuild for the move (shown once, identical to the Code block):
```py
    c = cats.set_index("category_id")
    kids = {p: list(g.index) for p, g in c.dropna(subset=["parent_id"]).groupby("parent_id")}
    def subtree(root):
        out, stack = [], [root]
        while stack:
            n = stack.pop()
            out.append(n)
            stack.extend(kids.get(n, []))
        return out
    deleted = c.drop(subtree(5))
    moved = deleted.copy()
    moved.loc[8, "parent_id"] = 2
    for n in subtree(8):   # pre-order: a parent is always handled before its children
        p = moved.loc[n, "parent_id"]
        moved.loc[n, "path"] = moved.loc[int(p), "path"] + f"{n}/"
    return deleted.reset_index(), moved.reset_index()
```

**Example:** by hand.
- Delete category 5: the subtree is 5, 6, 7 and 9 (Electronics, Phones, Laptops, Android): 4 rows deleted; 1, 2, 8, 10, 11, 12 remain. For employees, deleting 3 removes 3, 4, 5 and 6 (4 rows), leaving 1, 2 and 7.
- Move 8 under 2: parent_id of 8 becomes 2. Paths: 8 becomes `/1/2/8/`; its children become `/1/2/8/10/` and `/1/2/8/11/`; Spades becomes `/1/2/8/10/12/`. Four rows change their path; Home, Store are untouched.
- Cycle check: moving 2 under 12 asks "is 12 in the subtree of 2?"; after the move 12 is below 8, which is below 2, so yes: refused. Moving 8 under 8 is refused because the subtree contains the node itself.

**Code:** run with `python3 -I`. Asserts: pandas equals SQL after the delete and after the move (both ordered by `category_id`), and refused moves leave the table unchanged.
```python
# Q20: delete a subtree, move a subtree with a rebuilt materialised path, and refuse a move that creates a cycle
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT);
INSERT INTO categories VALUES
 (1,NULL,'Store','/1/'),(2,1,'Home','/1/2/'),(5,1,'Electronics','/1/5/'),(6,5,'Phones','/1/5/6/'),
 (7,5,'Laptops','/1/5/7/'),(9,6,'Android','/1/5/6/9/'),(8,1,'Garden','/1/8/'),(10,8,'Tools','/1/8/10/'),
 (11,8,'Lawn','/1/8/11/'),(12,10,'Spades','/1/8/10/12/');
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES (1,NULL),(2,1),(3,1),(4,3),(5,3),(6,4),(7,2);
"""
SQL_MAIN = """
DELETE FROM categories
WHERE category_id IN (
  WITH RECURSIVE sub(id) AS (
    SELECT category_id FROM categories WHERE category_id = 5
    UNION ALL
    SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
  )
  SELECT id FROM sub
)
"""
SQL_CYCLE_CHECK = """
WITH RECURSIVE sub(id) AS (
  SELECT :moved
  UNION
  SELECT c.category_id FROM categories c JOIN sub s ON c.parent_id = s.id
)
SELECT COUNT(*) FROM sub WHERE id = :newparent
"""
SQL_MOVE_PARENT = """
UPDATE categories SET parent_id = :newparent WHERE category_id = :moved
"""
SQL_MOVE_PATHS = """
WITH RECURSIVE t(id, newpath) AS (
  SELECT c.category_id, p.path || c.category_id || '/'
  FROM categories c JOIN categories p ON p.category_id = c.parent_id
  WHERE c.category_id = :moved
  UNION ALL
  SELECT c.category_id, t.newpath || c.category_id || '/'
  FROM categories c JOIN t ON c.parent_id = t.id
)
UPDATE categories SET path = (SELECT newpath FROM t WHERE t.id = categories.category_id)
WHERE category_id IN (SELECT id FROM t)
"""
SQL_DELETE_EMP = """
DELETE FROM employees
WHERE emp_id IN (
  WITH RECURSIVE team(id) AS (
    SELECT emp_id FROM employees WHERE emp_id = 3
    UNION ALL SELECT e.emp_id FROM employees e JOIN team t ON e.manager_id = t.id
  )
  SELECT id FROM team
)
"""

def load():
    con = sqlite3.connect(":memory:")
    con.executescript(SCHEMA)
    return con

def table(con, name="categories"):
    return pd.read_sql_query(f"SELECT * FROM {name} ORDER BY 1", con)

def move(con, moved, newparent):
    # refuse a move into the moved node's own subtree (that includes the node itself)
    if con.execute(SQL_CYCLE_CHECK, {"moved": moved, "newparent": newparent}).fetchone()[0] > 0:
        return False
    with con:
        con.execute(SQL_MOVE_PARENT, {"moved": moved, "newparent": newparent})
        con.execute(SQL_MOVE_PATHS, {"moved": moved})
    return True

con = load()
before = table(con)
print("categories before:")
print(before.to_string(index=False))
cur = con.execute(SQL_MAIN)
print("DELETE category 5 and everything under it: rows deleted =", cur.rowcount)
after_del = table(con)
print(after_del.to_string(index=False))
cur = con.execute(SQL_DELETE_EMP)
print("DELETE employee 3 and the whole team below: rows deleted =", cur.rowcount, "| employees left:", [r[0] for r in con.execute("SELECT emp_id FROM employees ORDER BY 1")])

ok = move(con, 8, 2)
after_move = table(con)
print("move subtree 8 under 2 (moved =", ok, "):")
print(after_move.to_string(index=False))
print("move 2 under 12 (a descendant of 2 after the move) accepted?", move(con, 2, 12), "| move 8 under itself accepted?", move(con, 8, 8))
assert table(con).equals(after_move), "refused moves must not change anything"

cats = before.copy()

def pandas_side(cats):
    # pd:main
    c = cats.set_index("category_id")
    kids = {p: list(g.index) for p, g in c.dropna(subset=["parent_id"]).groupby("parent_id")}
    def subtree(root):
        out, stack = [], [root]
        while stack:
            n = stack.pop()
            out.append(n)
            stack.extend(kids.get(n, []))
        return out
    deleted = c.drop(subtree(5))
    moved = deleted.copy()
    moved.loc[8, "parent_id"] = 2
    for n in subtree(8):   # pre-order: a parent is always handled before its children
        p = moved.loc[n, "parent_id"]
        moved.loc[n, "path"] = moved.loc[int(p), "path"] + f"{n}/"
    return deleted.reset_index(), moved.reset_index()
    # pd:end

pd_del, pd_move = pandas_side(cats)
pd.testing.assert_frame_equal(pd_del, after_del, check_dtype=False)   # compared after sorting by category_id
pd.testing.assert_frame_equal(pd_move, after_move, check_dtype=False)
print("pandas results equal SQL after the delete and after the move")
assert table(con, "categories")["category_id"].tolist() == [1, 2, 8, 10, 11, 12]
n_sub = con.execute("SELECT COUNT(*) FROM categories WHERE path LIKE '/1/2/8/%'").fetchone()[0]
print("rows whose path starts with /1/2/8/ after the move:", n_sub, "(Garden and its three descendants)")

# what the cycle check protects: a move into the own subtree, forced without the check
c2 = load()
c2.execute("UPDATE categories SET parent_id = 9 WHERE category_id = 5")
reach = c2.execute("""WITH RECURSIVE d(id) AS (SELECT category_id FROM categories WHERE parent_id IS NULL
                      UNION SELECT c.category_id FROM categories c JOIN d ON c.parent_id = d.id) SELECT COUNT(*) FROM d""").fetchone()[0]
print("forced move 5 under 9 without the check: rows reachable from the root drop from 10 to", reach, "(Electronics, Phones, Laptops, Android are now a detached cycle)")
# a naive delete without recursion
c3 = load()
c3.execute("DELETE FROM categories WHERE category_id = 5")
print("plain DELETE of category 5 leaves orphans:", [r[0] for r in c3.execute("SELECT category_id FROM categories WHERE parent_id IS NOT NULL AND parent_id NOT IN (SELECT category_id FROM categories) ORDER BY 1")])

# foreign key with ON DELETE CASCADE does the same without a recursive query, but only with the pragma on
def fk_run(pragma):
    c = sqlite3.connect(":memory:")
    c.execute(f"PRAGMA foreign_keys = {pragma}")
    c.executescript("""
    CREATE TABLE cat(category_id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES cat(category_id) ON DELETE CASCADE, name TEXT);
    INSERT INTO cat VALUES (1,NULL,'Store'),(5,1,'Electronics'),(6,5,'Phones'),(7,5,'Laptops'),(9,6,'Android'),(8,1,'Garden');""")
    c.execute("DELETE FROM cat WHERE category_id = 5")
    return [r[0] for r in c.execute("SELECT category_id FROM cat ORDER BY 1")]
print("ON DELETE CASCADE with foreign_keys = ON leaves", fk_run("ON"), "| with the default (OFF) leaves", fk_run("OFF"))
empty = sqlite3.connect(":memory:")
empty.execute("CREATE TABLE categories(category_id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, path TEXT)")
print("delete a missing id:", load().execute(SQL_MAIN.replace("= 5", "= 999")).rowcount, "rows | empty table:", empty.execute(SQL_MAIN).rowcount, "rows")
print("asserts passed")
```

**Output (my run):**
```text
categories before:
 category_id  parent_id        name        path
           1        NaN       Store         /1/
           2        1.0        Home       /1/2/
           5        1.0 Electronics       /1/5/
           6        5.0      Phones     /1/5/6/
           7        5.0     Laptops     /1/5/7/
           8        1.0      Garden       /1/8/
           9        6.0     Android   /1/5/6/9/
          10        8.0       Tools    /1/8/10/
          11        8.0        Lawn    /1/8/11/
          12       10.0      Spades /1/8/10/12/
DELETE category 5 and everything under it: rows deleted = 4
 category_id  parent_id   name        path
           1        NaN  Store         /1/
           2        1.0   Home       /1/2/
           8        1.0 Garden       /1/8/
          10        8.0  Tools    /1/8/10/
          11        8.0   Lawn    /1/8/11/
          12       10.0 Spades /1/8/10/12/
DELETE employee 3 and the whole team below: rows deleted = 4 | employees left: [1, 2, 7]
move subtree 8 under 2 (moved = True ):
 category_id  parent_id   name          path
           1        NaN  Store           /1/
           2        1.0   Home         /1/2/
           8        2.0 Garden       /1/2/8/
          10        8.0  Tools    /1/2/8/10/
          11        8.0   Lawn    /1/2/8/11/
          12       10.0 Spades /1/2/8/10/12/
move 2 under 12 (a descendant of 2 after the move) accepted? False | move 8 under itself accepted? False
pandas results equal SQL after the delete and after the move
rows whose path starts with /1/2/8/ after the move: 4 (Garden and its three descendants)
forced move 5 under 9 without the check: rows reachable from the root drop from 10 to 6 (Electronics, Phones, Laptops, Android are now a detached cycle)
plain DELETE of category 5 leaves orphans: [6, 7]
ON DELETE CASCADE with foreign_keys = ON leaves [1, 8] | with the default (OFF) leaves [1, 6, 7, 8, 9]
delete a missing id: 0 rows | empty table: 0 rows
asserts passed
```
Honest notes from the run:
- A plain `DELETE ... WHERE category_id = 5` leaves orphans 6 and 7 (the unguarded version of the problem). Forcing 5 under 9 without the check makes four rows a detached cycle and the number of rows reachable from the root drops from 10 to 6, so a top-down query silently loses them.
- `ON DELETE CASCADE` on a self-referencing foreign key deleted the whole subtree (left rows 1 and 8) when `PRAGMA foreign_keys = ON`, and deleted only the one row (left 1, 6, 7, 8, 9) with SQLite's default, because SQLite does not enforce foreign keys unless that pragma is set on the connection.
- Deleting a missing id or running on an empty table deletes 0 rows and raises nothing.

**Edge cases:**
- Deleting the root removes everything; deleting a leaf removes one row; a missing id removes nothing.
- Foreign keys from other tables (for example `products.category_id`) would block the delete or need their own cascade or reassignment; delete children before parents in engines that check row by row.
- Moving a node to the root: `parent_id` NULL and path `'/' || id || '/'`; the SQL above needs a variant for NULL because the anchor joins to the new parent.
- Concurrent edits: two moves at once can create a cycle even though each passed the check; take a lock or run the check and the update in one serialisable transaction (a general rule, not tested here).
- The materialised path must be changed for every descendant: that is the write cost of this storage model (Q24).
- Unknown new parent (id not in the table): the path anchor returns no row and the paths do not change, so check the parent exists first.

**Then explain:**
- Why the new parent must not be a descendant: the moved node would become its own ancestor; the subtree would lose its connection to the root and would be invisible to any top-down query (the forced move printed above).
- `ON DELETE CASCADE` versus a recursive delete: the cascade is declarative and the engine does the walk (if it enforces foreign keys; in SQLite only with the pragma on), but it deletes silently and can be limited in depth in some engines; the recursive `DELETE` is explicit and can be wrapped with a preview `SELECT` using the same CTE.
- Preview first: run the CTE as a `SELECT` to list what would go, then delete.
- Portability (not executed): SQL Server needs the CTE before the statement (`WITH sub AS (...) DELETE FROM categories WHERE category_id IN (SELECT id FROM sub)`) with no `RECURSIVE` keyword; MySQL 8 supports a CTE with `DELETE` (CTE first), and may complain (error 1093) about reading and deleting the same table in a subquery in some forms; PostgreSQL accepts `WITH RECURSIVE ... DELETE`. All three are from memory and documentation snippets, not executed here.

**Follow-ups:**
- "Soft delete instead?" Set `deleted_at` on the same subtree ids; reads must filter it, and a restore uses the same CTE.
- "Move without rebuilding every path?" Use the closure table or nested sets (Q24), which pay a different write cost.
- "What about reassigning children instead of deleting?" Update their `parent_id` to the deleted node's parent before deleting the node.

**Common mistakes:**
- Deleting only the node and leaving orphan children.
- Assuming `ON DELETE CASCADE` works in SQLite without `PRAGMA foreign_keys = ON`.
- Updating `parent_id` but not the paths of the descendants.
- Allowing a move under the node's own descendant, or under itself.
- Doing the check and the move in separate transactions.
