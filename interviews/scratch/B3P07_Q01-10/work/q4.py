# Q4: Consecutive Numbers (LeetCode 180 pattern): self join, LEAD, ROW_NUMBER difference, pandas run key
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logs(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs VALUES
 (1,1),(2,1),(3,1),(4,2),(5,1),(6,2),(7,2),(8,2),(9,2),(10,3),(11,3),(12,NULL),(13,NULL),(14,NULL);
"""
SQL_JOIN = """
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l2.id = l1.id + 1 AND l2.num = l1.num
JOIN logs l3 ON l3.id = l1.id + 2 AND l3.num = l1.num
ORDER BY consecutive_num
"""
SQL_JOIN_NO_DISTINCT = SQL_JOIN.replace("SELECT DISTINCT", "SELECT")
SQL_LEAD = """
WITH x AS (
  SELECT num,
         LEAD(num, 1) OVER (ORDER BY id) AS n1,
         LEAD(num, 2) OVER (ORDER BY id) AS n2
  FROM logs
)
SELECT DISTINCT num AS consecutive_num
FROM x
WHERE num = n1 AND num = n2
ORDER BY consecutive_num
"""
SQL_ISLAND = """
WITH x AS (
  SELECT id, num,
         ROW_NUMBER() OVER (ORDER BY id)
           - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS grp
  FROM logs
  WHERE num IS NOT NULL
)
SELECT DISTINCT num AS consecutive_num
FROM x
GROUP BY num, grp
HAVING COUNT(*) >= ?
ORDER BY consecutive_num
"""
SQL_ISLAND_NO_FILTER = SQL_ISLAND.replace("  WHERE num IS NOT NULL\n", "")
SQL_ISLAND_IDS = """
WITH x AS (
  SELECT id, num,
         id - ROW_NUMBER() OVER (PARTITION BY num ORDER BY id) AS grp
  FROM logs
  WHERE num IS NOT NULL
)
SELECT DISTINCT num AS consecutive_num
FROM x
GROUP BY num, grp
HAVING COUNT(*) >= ?
ORDER BY consecutive_num
"""

def col(con, sql, *params):
    return [r[0] for r in con.execute(sql, params)]

def pd_consec(logs, n=3, respect_ids=False):
    # pd:main
    d = logs.sort_values("id")
    run = (d["num"] != d["num"].shift()).cumsum()
    if respect_ids:
        run = run + (d["id"].diff() != 1).cumsum()
    g = d.groupby(run).agg(num=("num", "first"), n=("id", "size"))
    out = sorted(int(v) for v in g.loc[(g["n"] >= n) & g["num"].notna(), "num"].unique())
    # pd:end
    return out

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
j = col(con, SQL_JOIN)
print("self join:", j)
print("self join without DISTINCT:", col(con, SQL_JOIN_NO_DISTINCT), "(num 2 has a run of 4, so two start rows)")
l = col(con, SQL_LEAD)
i3 = col(con, SQL_ISLAND, 3)
print("LEAD + DISTINCT:", l)
print("ROW_NUMBER difference, N=3:", i3)
assert j == l == i3
logs = pd.read_sql_query("SELECT * FROM logs", con)
print("pandas, N=3:", pd_consec(logs, 3))
# compared as sorted lists of num values
assert pd_consec(logs, 3) == i3
for n in (2, 3, 4, 5):
    s = col(con, SQL_ISLAND, n)
    p = pd_consec(logs, n)
    assert s == p
    print("N =", n, "-> SQL", s, "| pandas", p)
print("NULL rows (ids 12-14) with no IS NOT NULL filter, N=3:", col(con, SQL_ISLAND_NO_FILTER, 3))

# gaps in ids: id 3 was deleted, so 7,7,7 sits at ids 1,2,4
con.executescript("""
CREATE TABLE logs_gap(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs_gap VALUES (5,8),(1,7),(4,7),(2,7),(6,8);
""")
def on_gap(sql):
    return sql.replace("FROM logs", "FROM logs_gap")
print("\nids 1,2,4 hold 7,7,7 (id 3 missing):")
print("  self join (id arithmetic):", col(con, on_gap(SQL_JOIN)))
print("  LEAD (positional):", col(con, on_gap(SQL_LEAD)))
print("  id - ROW_NUMBER per num (id arithmetic):", col(con, on_gap(SQL_ISLAND_IDS), 3))
print("  ROW_NUMBER difference (positional):", col(con, on_gap(SQL_ISLAND), 3))
lg = pd.read_sql_query("SELECT * FROM logs_gap", con)
print("  pandas positional:", pd_consec(lg, 3), "| pandas respecting ids:", pd_consec(lg, 3, respect_ids=True))
assert pd_consec(lg, 3) == col(con, on_gap(SQL_ISLAND), 3)
assert pd_consec(lg, 3, respect_ids=True) == col(con, on_gap(SQL_ISLAND_IDS), 3) == col(con, on_gap(SQL_JOIN))
print("  asserts: positional == positional, id-aware == id-aware")

# single row and empty table
con.execute("DELETE FROM logs_gap")
print("\nempty table:", col(con, on_gap(SQL_ISLAND), 3), "| pandas:", pd_consec(pd.read_sql_query("SELECT * FROM logs_gap", con), 3))
con.execute("INSERT INTO logs_gap VALUES (1, 9)")
print("single row, N=1:", col(con, on_gap(SQL_ISLAND), 1), "| N=3:", col(con, on_gap(SQL_ISLAND), 3))
print("asserts passed")
