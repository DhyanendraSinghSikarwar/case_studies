# Q9: org-size roll-up with an ancestor/descendant pairs CTE, aggregated outside; pandas pair expansion
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1, NULL, 'Tim', 500), (2, 1, 'Radha', 300), (3, 1, 'Hari', 300), (4, 2, 'Asha', 100),
 (5, 3, 'Ben', 200), (6, 3, 'Chen', 200), (7, 5, 'Dev', 150), (8, 5, 'Esha', 150),
 (9, 6, 'Farid', 120), (10, 7, 'Gita', 100), (11, 7, 'Hugo', 100),
 (12, 10, 'Ivy', NULL),          -- salary not recorded
 (13, 99, 'Jay', 80);            -- orphan: manager 99 does not exist
"""
SQL_MAIN = """
WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT manager_id, emp_id FROM employees WHERE manager_id IS NOT NULL
  UNION                                                   -- pairs are unique, so a loop cannot repeat forever
  SELECT p.ancestor, e.emp_id FROM pairs p JOIN employees e ON e.manager_id = p.descendant
)
SELECT m.emp_id, m.name,
       COUNT(*) AS reports,
       COALESCE(SUM(d.salary), 0) AS reports_salary,
       m.salary + COALESCE(SUM(d.salary), 0) AS subtree_salary
FROM pairs p
JOIN employees m ON m.emp_id = p.ancestor
JOIN employees d ON d.emp_id = p.descendant
GROUP BY m.emp_id, m.name, m.salary
ORDER BY m.emp_id
"""
SQL_TOP3 = SQL_MAIN.replace("GROUP BY m.emp_id, m.name, m.salary\n", "GROUP BY m.emp_id, m.name, m.salary\nHAVING COUNT(*) >= 3\n")
assert SQL_TOP3 != SQL_MAIN
SQL_DIRECT = "SELECT manager_id, COUNT(*) AS direct_reports FROM employees GROUP BY manager_id ORDER BY manager_id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
top3 = pd.read_sql_query(SQL_TOP3, con)
print(sql_df.to_string(index=False))
print("managers with >= 3 reports at any depth:", top3["emp_id"].tolist())
print("plain GROUP BY manager_id (direct only):", con.execute(SQL_DIRECT).fetchall())

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def pairs_of(employees):
    e0 = (employees.dropna(subset=["manager_id"])[["manager_id", "emp_id"]]
          .astype("int64").rename(columns={"manager_id": "ancestor", "emp_id": "descendant"}))
    pairs, frontier = e0, e0
    while not frontier.empty:
        nxt = (frontier.merge(e0.rename(columns={"ancestor": "descendant", "descendant": "d2"}), on="descendant")
               [["ancestor", "d2"]].rename(columns={"d2": "descendant"}).drop_duplicates())
        frontier = nxt[~pd.MultiIndex.from_frame(nxt).isin(pd.MultiIndex.from_frame(pairs))]
        pairs = pd.concat([pairs, frontier], ignore_index=True)
    return pairs
def rollup(employees, pairs):
    x = (pairs.merge(employees[["emp_id", "name", "salary"]], left_on="ancestor", right_on="emp_id")
              .merge(employees[["emp_id", "salary"]].rename(columns={"emp_id": "d_id", "salary": "d_salary"}),
                     left_on="descendant", right_on="d_id"))
    g = (x.groupby(["emp_id", "name", "salary"], as_index=False, dropna=False)    # dropna=False: a NaN salary must not drop the group
          .agg(reports=("d_id", "size"), reports_salary=("d_salary", "sum")))
    g["subtree_salary"] = g["salary"] + g["reports_salary"]
    return g[["emp_id", "name", "reports", "reports_salary", "subtree_salary"]].sort_values("emp_id").reset_index(drop=True)
pd_df = rollup(employees, pairs_of(employees))
pd_top3 = pd_df[pd_df["reports"] >= 3].reset_index(drop=True)
direct = employees.groupby("manager_id").size()
# pd:end
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)          # both ordered by emp_id
pd.testing.assert_frame_equal(pd_top3, top3, check_dtype=False)
print("pandas equals SQL (ordered by emp_id)")
print("pandas groupby(manager_id) direct counts (NaN key dropped):", direct.to_dict())

# Edge cases: pairs for the orphan manager 99, a loop, a NULL salary
pairs = pd.read_sql_query("""WITH RECURSIVE pairs(ancestor, descendant) AS (
  SELECT manager_id, emp_id FROM employees WHERE manager_id IS NOT NULL
  UNION SELECT p.ancestor, e.emp_id FROM pairs p JOIN employees e ON e.manager_id = p.descendant)
SELECT * FROM pairs""", con)
print("pair rows:", len(pairs), "| pairs whose ancestor is 99:", pairs.loc[pairs.ancestor == 99].values.tolist(), "(dropped by the inner join to the manager row)")
print("Gita (10) reports_salary:", int(sql_df.loc[sql_df.emp_id == 10, "reports_salary"].iloc[0]), "(her only report Ivy has a NULL salary)")
con.execute("UPDATE employees SET manager_id = 12 WHERE emp_id = 5")      # loop 5 -> 7 -> 10 -> 12 -> 5
loop_df = pd.read_sql_query(SQL_MAIN, con)
loop_pd = rollup(pd.read_sql_query("SELECT * FROM employees", con), pairs_of(pd.read_sql_query("SELECT * FROM employees", con)))
pd.testing.assert_frame_equal(loop_pd, loop_df, check_dtype=False)
print("with a loop 5-7-10-12-5 the UNION version still ends:", loop_df.loc[loop_df.emp_id.isin([5, 7, 10, 12]), ["emp_id", "reports"]].values.tolist(), "(each loop member counts himself)")
print("asserts passed")
