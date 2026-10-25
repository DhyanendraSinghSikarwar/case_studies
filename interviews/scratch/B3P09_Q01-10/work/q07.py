# Q7: UNION versus UNION ALL in recursion on a graph with two routes to D and a cycle D -> A
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE edges(src TEXT, dst TEXT);
INSERT INTO edges VALUES ('A','B'), ('A','C'), ('B','D'), ('C','D'), ('D','A');
"""
SQL_ALL_CAP = """
WITH RECURSIVE r(node, depth) AS (
  SELECT 'A', 0
  UNION ALL
  SELECT e.dst, r.depth + 1 FROM edges e JOIN r ON e.src = r.node
  WHERE r.depth < 4                                      -- depth cap: the only stop
)
SELECT node, depth FROM r ORDER BY depth, node
"""
SQL_UNION = """
WITH RECURSIVE r(node) AS (
  SELECT 'A'
  UNION                                                  -- drops a row that was already produced
  SELECT e.dst FROM edges e JOIN r ON e.src = r.node
)
SELECT node FROM r ORDER BY node
"""
SQL_UNION_DEPTH = """
WITH RECURSIVE r(node, depth) AS (
  SELECT 'A', 0
  UNION                                                  -- depth makes every row new, so nothing is dropped
  SELECT e.dst, r.depth + 1 FROM edges e JOIN r ON e.src = r.node
)
SELECT node, depth FROM r LIMIT 15                       -- LIMIT is the only reason this demo stops
"""
SQL_UNION_ALL_LOOP = """
WITH RECURSIVE r(node) AS (
  SELECT 'A' UNION ALL SELECT e.dst FROM edges e JOIN r ON e.src = r.node
)
SELECT node FROM r LIMIT 12
"""
SQL_PATH = """
WITH RECURSIVE r(node, path) AS (
  SELECT 'A', ',A,'
  UNION ALL
  SELECT e.dst, r.path || e.dst || ','
  FROM edges e JOIN r ON e.src = r.node
  WHERE instr(r.path, ',' || e.dst || ',') = 0           -- visited check on the path
)
SELECT node, path FROM r ORDER BY path
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
cap = pd.read_sql_query(SQL_ALL_CAP, con)
print("UNION ALL, depth cap 4:", cap.groupby("depth")["node"].apply(lambda s: "".join(s)).to_dict(), "| rows:", len(cap), "| D appears", int((cap.node == "D").sum()), "times")
uni = pd.read_sql_query(SQL_UNION, con)
print("UNION, node only:", uni["node"].tolist())
print("UNION ALL, no guard, LIMIT 12:", "".join(r[0] for r in con.execute(SQL_UNION_ALL_LOOP)))
ud = con.execute(SQL_UNION_DEPTH).fetchall()
print("UNION with a depth column, LIMIT 15:", len(ud), "rows, all distinct:", len(set(ud)) == len(ud), "| last 3:", ud[-3:])
path = pd.read_sql_query(SQL_PATH, con)
print("UNION ALL with path guard:", path["path"].tolist())

edges = pd.read_sql_query("SELECT * FROM edges", con)
# pd:main
step = lambda f: f.merge(edges, left_on="node", right_on="src")[["dst"]].rename(columns={"dst": "node"})
# (1) UNION ALL with a depth cap: no de-duplication
frontier = pd.DataFrame({"node": ["A"], "depth": 0})
frames = [frontier]
for d in range(1, 5):
    frontier = step(frontier).assign(depth=d)
    frames.append(frontier)
pd_cap = pd.concat(frames, ignore_index=True).sort_values(["depth", "node"]).reset_index(drop=True)
# (2) UNION on a key-only row: keep a visited frame, anti-join the new rows against it
reach = pd.DataFrame({"node": ["A"]})
frontier = reach
while not frontier.empty:
    nxt = step(frontier).drop_duplicates()
    frontier = nxt[~nxt["node"].isin(reach["node"])]
    reach = pd.concat([reach, frontier], ignore_index=True)
pd_uni = reach.sort_values("node").reset_index(drop=True)
# (3) UNION ALL with a path guard
fr = pd.DataFrame({"node": ["A"], "path": [",A,"]})
rows = [fr]
while not fr.empty:
    nx = fr.merge(edges, left_on="node", right_on="src")
    nx = nx[[("," + d + ",") not in p for d, p in zip(nx["dst"], nx["path"])]]
    fr = pd.DataFrame({"node": nx["dst"].to_numpy(), "path": (nx["path"] + nx["dst"] + ",").to_numpy()})
    rows.append(fr)
pd_path = pd.concat(rows, ignore_index=True).sort_values("path").reset_index(drop=True)
# pd:end
pd.testing.assert_frame_equal(pd_cap[["node", "depth"]], cap, check_dtype=False)
pd.testing.assert_frame_equal(pd_uni, uni, check_dtype=False)
pd.testing.assert_frame_equal(pd_path, path, check_dtype=False)
print("pandas equals SQL for all three (each sorted as its SQL ORDER BY)")

# Edge cases: duplicate edge, NULL destination, start node not in the graph
con.execute("CREATE TABLE edges_dup AS SELECT * FROM edges"); con.execute("INSERT INTO edges_dup VALUES ('A','B')")
dup_path = con.execute(SQL_PATH.replace("edges", "edges_dup")).fetchall()
dup_uni = con.execute(SQL_UNION.replace("edges", "edges_dup")).fetchall()
print("duplicate edge A->B: path rows", len(path), "->", len(dup_path), "| UNION node rows", len(uni), "->", len(dup_uni))
con.execute("CREATE TABLE edges_null AS SELECT * FROM edges"); con.execute("INSERT INTO edges_null VALUES ('D', NULL)")
print("edge D -> NULL, UNION:", con.execute(SQL_UNION.replace("edges", "edges_null").replace("ORDER BY node", "ORDER BY node IS NULL, node")).fetchall())
print("start node 'Z' not in the graph (literal anchor):", con.execute(SQL_UNION.replace("SELECT 'A'", "SELECT 'Z'")).fetchall())
print("start node 'Z' (anchor from the edge table):", con.execute(SQL_UNION.replace("SELECT 'A'", "SELECT dst FROM edges WHERE src = 'Z'")).fetchall())
print("asserts passed")
