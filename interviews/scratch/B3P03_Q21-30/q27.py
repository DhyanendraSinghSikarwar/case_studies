# Q27: top-N per group with a correlated COUNT subquery (no window functions); ties; tie-break; row values
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,60),
 (5,'Eve',20,80),(6,'Farid',20,75),(7,'Gita',20,75),(8,'Hari',20,60),
 (9,'Ivy',30,50);
"""
SQL_MAIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_TIEBREAK = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary > e.salary OR (e2.salary = e.salary AND e2.emp_id < e.emp_id))) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_ROWVALUE = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id)) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_COUNTS = """
SELECT e.emp_id, e.dept_id, e.salary,
       (SELECT COUNT(*) FROM employees e2
        WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) AS higher
FROM employees e ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_LIMIT_IN = """
SELECT emp_id FROM employees
WHERE emp_id IN (SELECT e2.emp_id FROM employees e2 ORDER BY e2.salary DESC, e2.emp_id LIMIT 2)
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
tb_df = pd.read_sql_query(SQL_TIEBREAK, con)
rv_df = pd.read_sql_query(SQL_ROWVALUE, con)
print("strict > (ties share a rank):")
print(sql_df.to_string(index=False))
print("\nhow many strictly higher earners in the department, per employee:")
print(pd.read_sql_query(SQL_COUNTS, con).to_string(index=False))
print("\ntie-break by emp_id, rows:", len(tb_df), "ids", tb_df["emp_id"].tolist())
print("row-value tie-break (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id), ids", rv_df["emp_id"].tolist())
print("LIMIT inside an IN subquery runs on SQLite (global top 2, not per group):", [r[0] for r in con.execute(SQL_LIMIT_IN)])

# pd:main
rank_min = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False)     # = (count strictly higher) + 1
pd_ties = emp[rank_min <= 2].sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
           .groupby("dept_id").head(2))
pd_nlargest = emp.groupby("dept_id", group_keys=False).apply(lambda g: g.nlargest(2, "salary", keep="first"))
# pd:end
pairs = int((emp.groupby("dept_id").size() ** 2).sum())
print("\npandas rank(method='min') <= 2 ids:", pd_ties["emp_id"].tolist())
print("pandas sort + groupby.head(2) ids:", pd_head["emp_id"].tolist())
print("pandas groupby nlargest(2, keep='first') ids:", sorted(pd_nlargest["emp_id"].tolist()))
print(f"comparisons the correlated count makes: {pairs} (sum of group size squared) for {len(emp)} rows")

pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_ties.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(tb_df.reset_index(drop=True), pd_head.reset_index(drop=True), check_dtype=False)
assert rv_df["emp_id"].tolist() == tb_df["emp_id"].tolist()
assert sorted(pd_nlargest["emp_id"]) == sorted(tb_df["emp_id"])
print("\nasserts passed: strict-> SQL == rank(method='min'); tie-break SQL == row-value SQL == head(2) == nlargest; compared in dept_id, salary desc, emp_id order")
