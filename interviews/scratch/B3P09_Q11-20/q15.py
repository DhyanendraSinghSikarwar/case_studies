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
