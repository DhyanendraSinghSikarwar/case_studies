# Q18: Consecutive Available Seats (LeetCode 603 style): self join, LAG/LEAD, island version
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER);
INSERT INTO cinema VALUES
 (14,1),(1,1),(2,1),(3,0),(4,1),(5,0),(6,1),(7,1),(8,1),(9,0),(10,NULL),(11,1),(13,1);
"""
SQL_JOIN = """
SELECT DISTINCT a.seat_id
FROM cinema a
JOIN cinema b ON ABS(a.seat_id - b.seat_id) = 1
WHERE a.free = 1 AND b.free = 1
ORDER BY a.seat_id
"""
SQL_LAGLEAD = """
WITH x AS (
  SELECT seat_id, free,
         LAG(seat_id)  OVER (ORDER BY seat_id) AS prev_id,
         LAG(free)     OVER (ORDER BY seat_id) AS prev_free,
         LEAD(seat_id) OVER (ORDER BY seat_id) AS next_id,
         LEAD(free)    OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id
FROM x
WHERE free = 1
  AND ((prev_free = 1 AND prev_id = seat_id - 1) OR (next_free = 1 AND next_id = seat_id + 1))
ORDER BY seat_id
"""
SQL_ISLAND = """
WITH f AS (
  SELECT seat_id, seat_id - ROW_NUMBER() OVER (ORDER BY seat_id) AS grp
  FROM cinema
  WHERE free = 1
)
SELECT seat_id
FROM f
WHERE grp IN (SELECT grp FROM f GROUP BY grp HAVING COUNT(*) >= 2)
ORDER BY seat_id
"""
# wrong: LAG/LEAD on rows without checking that the ids are consecutive
SQL_NAIVE = """
WITH x AS (
  SELECT seat_id, free,
         LAG(free)  OVER (ORDER BY seat_id) AS prev_free,
         LEAD(free) OVER (ORDER BY seat_id) AS next_free
  FROM cinema
)
SELECT seat_id FROM x WHERE free = 1 AND (prev_free = 1 OR next_free = 1) ORDER BY seat_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for name, sql in (("self join", SQL_JOIN), ("LAG/LEAD with id check", SQL_LAGLEAD),
                  ("island (ids minus ROW_NUMBER)", SQL_ISLAND), ("naive LAG/LEAD, no id check", SQL_NAIVE)):
    res[name] = [r[0] for r in con.execute(sql)]
    print(f"{name}: {res[name]}")

cinema = pd.read_sql_query("SELECT * FROM cinema", con)
# pd:main
c = cinema.sort_values("seat_id").reset_index(drop=True)
is_free = c["free"].eq(1)                      # NULL counts as not free
prev_adj = is_free.shift(fill_value=False) & (c["seat_id"].diff() == 1)
next_adj = is_free.shift(-1, fill_value=False) & (c["seat_id"].diff(-1) == -1)
pd_neighbor = c.loc[is_free & (prev_adj | next_adj), "seat_id"].tolist()
f = c[is_free]
key = f["seat_id"] - range(len(f))
pd_island = f.loc[key.groupby(key).transform("size") >= 2, "seat_id"].tolist()
# pd:end
print("pandas neighbour version:", pd_neighbor)
print("pandas island version:", pd_island)
expected = [1, 2, 6, 7, 8, 13, 14]
assert res["self join"] == res["LAG/LEAD with id check"] == res["island (ids minus ROW_NUMBER)"] == expected
assert pd_neighbor == pd_island == expected   # all lists are ordered by seat_id
assert res["naive LAG/LEAD, no id check"] != expected
print("the naive version adds:", sorted(set(res["naive LAG/LEAD, no id check"]) - set(expected)))

# tiny cases: one seat, empty table, all free
for label, rows in (("single free seat", [(1, 1)]), ("empty table", []), ("all free, ids 5..7", [(5, 1), (6, 1), (7, 1)])):
    c2 = sqlite3.connect(":memory:")
    c2.execute("CREATE TABLE cinema(seat_id INTEGER PRIMARY KEY, free INTEGER)")
    c2.executemany("INSERT INTO cinema VALUES (?, ?)", rows)
    out = [[r[0] for r in c2.execute(s)] for s in (SQL_JOIN, SQL_LAGLEAD, SQL_ISLAND)]
    assert out[0] == out[1] == out[2]
    print(f"{label}: all three SQL versions return {out[0]}")
print("asserts passed")
