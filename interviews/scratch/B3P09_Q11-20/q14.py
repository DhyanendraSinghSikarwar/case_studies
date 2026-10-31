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
