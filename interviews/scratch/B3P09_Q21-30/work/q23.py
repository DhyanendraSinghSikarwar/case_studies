import heapq
import sqlite3
import networkx as nx
import pandas as pd

SCHEMA = """
CREATE TABLE roads(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads VALUES
 ('A','B',2),('A','C',5),('B','C',1),('C','B',1),('B','D',7),('C','D',2),
 ('D','E',1),('D','F',6),('E','F',2);
-- same graph but the road C to B has a negative weight (a refund or a downhill credit), so B-C-B costs -2 per loop
CREATE TABLE roads_neg(src TEXT, dst TEXT, km INTEGER);
INSERT INTO roads_neg SELECT src, dst, CASE WHEN src = 'C' AND dst = 'B' THEN -3 ELSE km END FROM roads;
"""
SQL_MAIN = """
WITH RECURSIVE p(node, path, km, legs) AS (
  SELECT 'A', ',A,', 0, 0
  UNION ALL
  SELECT r.dst, p.path || r.dst || ',', p.km + r.km, p.legs + 1
  FROM p JOIN roads r ON r.src = p.node
  WHERE instr(p.path, ',' || r.dst || ',') = 0
)
SELECT trim(path, ',') AS route, km, legs
FROM p
WHERE node = 'F'
ORDER BY km, route
"""
SQL_NODEPTH = """
WITH RECURSIVE w(node, km, legs) AS (
  SELECT 'A', 0, 0
  UNION ALL
  SELECT r.dst, w.km + r.km, w.legs + 1
  FROM w JOIN roads_t r ON r.src = w.node
  WHERE w.legs < {cap}
)
SELECT COUNT(*) AS walks_to_F, MIN(km) AS cheapest_km FROM w WHERE node = 'F'
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_df["route"] = sql_df["route"].str.replace(",", ">")
print("All simple routes A to F, cheapest first (SQL path-string guard):")
print(sql_df.to_string(index=False))

roads = pd.read_sql_query("SELECT src, dst, km AS w FROM roads", con)

# pd:main
paths = pd.DataFrame({"node": ["A"], "route": ["A"], "km": [0], "legs": [0]})
found = []
while len(paths):
    nxt = paths.merge(roads, left_on="node", right_on="src")
    fresh = pd.Series([d not in r.split(">") for d, r in zip(nxt["dst"], nxt["route"])], index=nxt.index, dtype=bool)
    nxt = nxt[fresh]
    paths = pd.DataFrame({"node": nxt["dst"], "route": nxt["route"] + ">" + nxt["dst"],
                          "km": nxt["km"] + nxt["w"], "legs": nxt["legs"] + 1})
    found.append(paths[paths["node"] == "F"])
pd_df = (pd.concat(found)[["route", "km", "legs"]]
           .sort_values(["km", "route"]).reset_index(drop=True))
# pd:end
# compare after ordering by km, route (the SQL ORDER BY)
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)
print("pandas frontier merge equals SQL:", len(pd_df), "simple routes")

def dijkstra(edges, source, target):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    best, heap = {source: 0}, [(0, source, [source])]
    done = set()
    while heap:
        d, u, route = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        if u == target:
            return d, ">".join(route)
        for v, w in graph.get(u, []):
            if v not in done and d + w < best.get(v, float("inf")):
                best[v] = d + w
                heapq.heappush(heap, (d + w, v, route + [v]))
    return None

edges = con.execute("SELECT src, dst, km FROM roads").fetchall()
dj_km, dj_route = dijkstra(edges, "A", "F")
G = nx.DiGraph()
G.add_weighted_edges_from(edges, weight="km")
nx_route = ">".join(nx.shortest_path(G, "A", "F", weight="km"))
nx_km = nx.shortest_path_length(G, "A", "F", weight="km")
best = sql_df.iloc[0]
assert (best["route"], best["km"]) == (dj_route, dj_km) == (nx_route, nx_km)
print("cheapest: SQL", (best["route"], int(best["km"])), "| heapq Dijkstra", (dj_route, dj_km), "| networkx", (nx_route, nx_km))

print("\nDepth limit only (no path guard), cheapest walk from A to F and number of walks, by leg cap:")
for table in ("roads", "roads_neg"):
    rows = []
    for cap in (4, 6, 8, 10, 12):
        n, m = con.execute(SQL_NODEPTH.replace("roads_t", table).format(cap=cap)).fetchone()
        rows.append((cap, n, m))
    print(f"  {table}:", rows, "(cap, walks_to_F, cheapest_km)")

neg = nx.DiGraph()
neg.add_weighted_edges_from(con.execute("SELECT src, dst, km FROM roads_neg").fetchall(), weight="km")
print("networkx negative_edge_cycle on roads_neg:", nx.negative_edge_cycle(neg, weight="km"))
try:
    nx.bellman_ford_path(neg, "A", "F", weight="km")
except nx.NetworkXUnbounded as ex:
    print("networkx bellman_ford_path raises NetworkXUnbounded:", ex)
try:
    print("networkx dijkstra on the negative cycle returns:", nx.dijkstra_path(neg, "A", "F", weight="km"))
except Exception as ex:
    print("networkx dijkstra raises", type(ex).__name__, ex)

import time
print("\nSimple-path enumeration on a chain of k diamonds (2 routes per diamond), SQL path-string guard:")
for k in (6, 10, 14):
    d = []
    for i in range(k):
        d += [(f"s{i}", f"a{i}", 1), (f"s{i}", f"b{i}", 1), (f"a{i}", f"s{i+1}", 1), (f"b{i}", f"s{i+1}", 1)]
    con.execute("DROP TABLE IF EXISTS dia")
    con.execute("CREATE TABLE dia(src TEXT, dst TEXT, km INTEGER)")
    con.executemany("INSERT INTO dia VALUES (?, ?, ?)", d)
    q = SQL_MAIN.replace("'A'", "'s0'").replace("roads", "dia").replace("node = 'F'", f"node = 's{k}'")
    t0 = time.perf_counter()
    n = con.execute(f"SELECT COUNT(*) FROM ({q.replace(chr(10) + 'ORDER BY km, route', '')})").fetchone()[0]
    print(f"  k={k:2d}: {n} simple routes (2^k = {2**k}), {len(d)} edges, {time.perf_counter() - t0:.3f} s on this machine")
print("asserts passed")
