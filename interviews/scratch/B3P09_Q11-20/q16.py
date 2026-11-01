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
