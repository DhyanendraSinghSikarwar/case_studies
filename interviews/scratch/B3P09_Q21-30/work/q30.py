import sqlite3
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT);
INSERT INTO employees VALUES
 (1,NULL,'Tim'),(2,1,'Radha'),(3,2,'Hari'),(4,3,'Shyam'),(5,1,'Meera'),
 (6,5,'Kiran'),(7,3,'Asha'),(8,6,'Dev'),(9,5,'Isha'),(10,4,'Ram'),
 (11,4,'Zoya'),(12,7,'Nina'),
 (30,2,'Tej'),
 (20,NULL,'Zed'),(21,20,'Uma');     -- a second company: a forest with two roots
"""
SQL_MAIN = """
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees WHERE emp_id IN ({a}, {b})
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
)
SELECT x.ancestor AS lca, x.dist + y.dist AS hops
FROM up x JOIN up y ON y.ancestor = x.ancestor
WHERE x.start = {a} AND y.start = {b}
ORDER BY hops LIMIT 1
"""
SQL_ALL_PAIRS = """
WITH RECURSIVE up(start, ancestor, dist) AS (
  SELECT emp_id, emp_id, 0 FROM employees
  UNION ALL
  SELECT up.start, e.manager_id, up.dist + 1
  FROM up JOIN employees e ON e.emp_id = up.ancestor
  WHERE e.manager_id IS NOT NULL
), cand AS (
  SELECT x.start AS a, y.start AS b, x.ancestor AS lca, x.dist + y.dist AS hops,
         ROW_NUMBER() OVER (PARTITION BY x.start, y.start ORDER BY x.dist + y.dist) AS rn
  FROM up x JOIN up y ON y.ancestor = x.ancestor
  WHERE x.start < y.start
)
SELECT a, b, lca, hops FROM cand WHERE rn = 1 ORDER BY a, b
"""
SQL_MATPATH = """
WITH RECURSIVE mp(emp_id, path) AS (
  SELECT emp_id, '/' || emp_id || '/' FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, mp.path || e.emp_id || '/' FROM employees e JOIN mp ON e.manager_id = mp.emp_id
), pick AS (
  SELECT (SELECT path FROM mp WHERE emp_id = {a}) AS pa, (SELECT path FROM mp WHERE emp_id = {b}) AS pb
), lcp(n) AS (
  SELECT 0
  UNION ALL
  SELECT n + 1 FROM lcp, pick WHERE n < length(pa) AND n < length(pb) AND substr(pa, n + 1, 1) = substr(pb, n + 1, 1)
), cut AS (
  SELECT substr(pa, 1, MAX(n)) AS common, pa, pb FROM lcp, pick
)
SELECT m.emp_id AS lca,
       (length(pa) - length(replace(pa, '/', '')) - 1) + (length(pb) - length(replace(pb, '/', '')) - 1)
         - 2 * (length(rtrim(common, replace(common, '/', ''))) - length(replace(rtrim(common, replace(common, '/', '')), '/', '')) - 1) AS hops
FROM cut JOIN mp m ON m.path = rtrim(common, replace(common, '/', ''))
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
names = dict(con.execute("SELECT emp_id, name FROM employees").fetchall())

def lca_sql(a, b):
    rows = con.execute(SQL_MAIN.format(a=a, b=b)).fetchall()
    return rows[0] if rows else None

def lca_matpath(a, b):
    rows = con.execute(SQL_MATPATH.format(a=a, b=b)).fetchall()
    return rows[0] if rows else None

cases = [("10 and 12 (the question)", 10, 12), ("4 and 10 (one is the ancestor of the other)", 4, 10),
         ("10 and 10 (same employee)", 10, 10), ("10 and 21 (different trees)", 10, 21),
         ("10 and 30 (ids '/1/2/3/4/10/' and '/1/2/30/')", 10, 30), ("8 and 11", 8, 11)]
print("case -> SQL chain join (lca, hops) | SQL materialized-path prefix (lca, hops)")
for label, a, b in cases:
    r1, r2 = lca_sql(a, b), lca_matpath(a, b)
    print(f"  {label}: {r1} ({names[r1[0]] if r1 else '-'}) | {r2}")
    assert r1 == r2

employees = pd.read_sql_query("SELECT * FROM employees", con)

# pd:main
parent = dict(zip(employees["emp_id"], employees["manager_id"]))
def up_chain(i):
    out = {i: 0}
    while not pd.isna(parent[i]):
        i = int(parent[i])
        out[i] = len(out)
    return out

def lca_pandas(a, b):
    ca, cb = up_chain(a), up_chain(b)
    common = set(ca) & set(cb)
    if not common:
        return None
    best = min(common, key=lambda x: (ca[x] + cb[x], x))
    return best, ca[best] + cb[best]
# pd:end

for label, a, b in cases:
    assert lca_pandas(a, b) == lca_sql(a, b)
sql_all = pd.read_sql_query(SQL_ALL_PAIRS, con)
ids = sorted(employees["emp_id"])
rows = []
for i, a in enumerate(ids):
    for b in ids[i + 1:]:
        r = lca_pandas(a, b)
        if r is not None:
            rows.append((a, b, r[0], r[1]))
pd_all = pd.DataFrame(rows, columns=["a", "b", "lca", "hops"])
# compare after ordering by a, b (the SQL ORDER BY); pairs across the two companies have no row in either
pd.testing.assert_frame_equal(pd_all, sql_all, check_dtype=False)
print(f"\nall {len(sql_all)} connected pairs: SQL chain join == pandas dict walk; pairs across the two companies are absent in both")
print("number of employee pairs in total:", len(ids) * (len(ids) - 1) // 2, "| pairs with no common ancestor:", len(ids) * (len(ids) - 1) // 2 - len(sql_all))

# networkx check on the tree edges (manager -> report)
D = nx.DiGraph([(int(m), int(e)) for e, m in zip(employees["emp_id"], employees["manager_id"]) if pd.notna(m)])
D.add_nodes_from(ids)
for label, a, b in cases:
    got = None
    try:
        got = nx.lowest_common_ancestor(D, a, b)
    except Exception as ex:
        got = type(ex).__name__
    print(f"  networkx lowest_common_ancestor({a}, {b}) = {got}")
bad = 0
for a, b, lca, hops in sql_all.itertuples(index=False):
    got = nx.lowest_common_ancestor(D, a, b)
    bad += (got != lca)
print("networkx 3.6.1 lowest_common_ancestor disagrees with the SQL answer on", bad, "of", len(sql_all), "connected pairs")
print("asserts passed")
