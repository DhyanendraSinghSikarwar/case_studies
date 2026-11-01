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
