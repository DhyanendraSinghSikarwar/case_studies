import sqlite3
from collections import deque
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE nodes(node_id INTEGER PRIMARY KEY);
INSERT INTO nodes VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
CREATE TABLE friendships(user_a INTEGER, user_b INTEGER);
INSERT INTO friendships VALUES (1,2),(1,3),(2,4),(3,4),(4,5),(5,6),(7,8),(8,9);
CREATE TABLE flights(src TEXT, dst TEXT, cost INTEGER);
INSERT INTO flights VALUES
 ('DEL','BOM',100),('DEL','HYD',80),('BOM','HYD',20),('HYD','BOM',25),
 ('BOM','BLR',90),('HYD','BLR',70),('BLR','DEL',150);
"""
SQL_DIST = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
)
SELECT node, MIN(dist) AS dist FROM r GROUP BY node ORDER BY dist, node
"""
SQL_COMP = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), reach(src, dst) AS (
  SELECT node_id, node_id FROM nodes
  UNION
  SELECT reach.src, e.b FROM reach JOIN e ON e.a = reach.dst
)
SELECT src AS node, MIN(dst) AS component FROM reach GROUP BY src ORDER BY src
"""
SQL_PATHS = """
WITH RECURSIVE p(node, path, cost) AS (
  SELECT 'DEL', ',DEL,', 0
  UNION ALL
  SELECT f.dst, p.path || f.dst || ',', p.cost + f.cost
  FROM p JOIN flights f ON f.src = p.node
  WHERE instr(p.path, ',' || f.dst || ',') = 0
)
SELECT trim(path, ',') AS route, cost FROM p WHERE node = 'BLR' ORDER BY cost, route
"""
SQL_QUEUE = """
WITH RECURSIVE e(a, b) AS (
  SELECT user_a, user_b FROM friendships UNION ALL SELECT user_b, user_a FROM friendships
), r(node, dist) AS (
  SELECT 1, 0
  UNION
  SELECT e.b, r.dist + 1 FROM r JOIN e ON e.a = r.node WHERE r.dist < 10
  {order}
)
SELECT node, dist FROM r
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_dist = pd.read_sql_query(SQL_DIST, con)
sql_comp = pd.read_sql_query(SQL_COMP, con)
sql_paths = pd.read_sql_query(SQL_PATHS, con)
friends = pd.read_sql_query("SELECT * FROM friendships", con)
flights = pd.read_sql_query("SELECT * FROM flights", con)
all_nodes = [r[0] for r in con.execute("SELECT node_id FROM nodes ORDER BY 1")]

# pd:main
def adjacency(pairs, directed):
    g = {}
    for a, b in pairs:
        g.setdefault(a, []).append(b)
        g.setdefault(b, [])
        if not directed:
            g[b].append(a)
    return {k: sorted(v) for k, v in g.items()}

def bfs_distance(g, start):
    dist, queue, order = {start: 0}, deque([start]), [start]
    while queue:
        u = queue.popleft()
        for v in g[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
                order.append(v)
    return dist, order

def components(g):
    comp = {}
    for s in sorted(g):
        if s in comp:
            continue
        label, queue = s, deque([s])         # s is the smallest unseen node, so it is the component's smallest id
        comp[s] = label
        while queue:
            u = queue.popleft()
            for v in g[u]:
                if v not in comp:
                    comp[v] = label
                    queue.append(v)
    return comp

def all_simple_paths(g, cost, start, goal):
    out, stack = [], [(start, [start], 0)]
    while stack:
        u, path, total = stack.pop()
        if u == goal:
            out.append((">".join(path), total))
            continue
        for v in g[u]:
            if v not in path:
                stack.append((v, path + [v], total + cost[(u, v)]))
    return sorted(out, key=lambda t: (t[1], t[0]))
# pd:end

g = adjacency(zip(friends["user_a"], friends["user_b"]), directed=False)
for n in all_nodes:
    g.setdefault(n, [])
dist, bfs_order = bfs_distance(g, 1)
py_dist = pd.DataFrame(sorted(dist.items(), key=lambda t: (t[1], t[0])), columns=["node", "dist"])
# compare after ordering by dist, node (the SQL ORDER BY)
pd.testing.assert_frame_equal(py_dist, sql_dist, check_dtype=False)
comp = components(g)
py_comp = pd.DataFrame(sorted(comp.items()), columns=["node", "component"])
pd.testing.assert_frame_equal(py_comp, sql_comp, check_dtype=False)
fg = adjacency(zip(flights["src"], flights["dst"]), directed=True)
cost = {(s, d): c for s, d, c in zip(flights["src"], flights["dst"], flights["cost"])}
py_paths = pd.DataFrame(all_simple_paths(fg, cost, "DEL", "BLR"), columns=["route", "cost"])
sql_paths["route"] = sql_paths["route"].str.replace(",", ">")
pd.testing.assert_frame_equal(py_paths, sql_paths, check_dtype=False)
print("plain Python BFS distances, components and DFS simple paths equal the SQL results")
print("distances from user 1:", dict(zip(py_dist["node"], py_dist["dist"])))
print("components (node -> smallest id):", comp)
print(py_paths.to_string(index=False))

# networkx as the library check
G = nx.Graph(list(zip(friends["user_a"], friends["user_b"])))
G.add_nodes_from(all_nodes)
assert dict(nx.shortest_path_length(G, 1)) == dist
nx_comp = sorted(sorted(c) for c in nx.connected_components(G))
assert nx_comp == sorted(sorted(n for n, c in comp.items() if c == lab) for lab in set(comp.values()))
D = nx.DiGraph([(s, d) for s, d in zip(flights["src"], flights["dst"])])
nx_paths = sorted(">".join(p) for p in nx.all_simple_paths(D, "DEL", "BLR"))
assert nx_paths == sorted(py_paths["route"])
print("networkx", nx.__version__, "agrees: shortest_path_length, connected_components", nx_comp, "all_simple_paths", len(nx_paths))

# SQLite queue: default FIFO order is BFS; ORDER BY in the recursive select changes the queue to LIFO (DFS-like)
fifo = con.execute(SQL_QUEUE.format(order="")).fetchall()
lifo = con.execute(SQL_QUEUE.format(order="ORDER BY 2 DESC")).fetchall()
print("\nSQLite queue order, FIFO (no ORDER BY):", [f"{n}@{d}" for n, d in fifo])
print("SQLite queue order, ORDER BY dist DESC:", [f"{n}@{d}" for n, d in lifo])
print("Python BFS visit order                :", bfs_order)
assert [d for _, d in fifo] == sorted(d for _, d in fifo)
assert sorted(fifo) == sorted(lifo)
print("asserts passed")
