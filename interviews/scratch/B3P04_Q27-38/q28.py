# Q28: rank within a filtered subset: filter before the window (WHERE) vs after (outer query)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER, status TEXT);
INSERT INTO employees VALUES
 (1,'Asha',10,90,'active'),(2,'Ben',10,100,'left'),(3,'Chitra',10,80,'active'),(4,'Dev',10,80,'active'),
 (5,'Esha',20,70,'left'),(6,'Farid',20,60,'active'),(7,'Gita',20,50,'active'),
 (8,'Hari',30,40,'left');
"""
SQL_MAIN = """
SELECT emp_id, name, dept_id, salary,
       RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk_active
FROM employees
WHERE status = 'active'
ORDER BY dept_id, rnk_active, emp_id
"""
SQL_AFTER = """
SELECT emp_id, name, dept_id, salary, rnk_all
FROM (SELECT emp_id, name, dept_id, salary, status,
             RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk_all
      FROM employees)
WHERE status = 'active'
ORDER BY dept_id, rnk_all, emp_id
"""
SQL_TOP1 = """
SELECT 'filter first' AS how, emp_id, name, dept_id FROM (
  SELECT emp_id, name, dept_id, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
  FROM employees WHERE status = 'active') WHERE r = 1
UNION ALL
SELECT 'filter after', emp_id, name, dept_id FROM (
  SELECT emp_id, name, dept_id, status, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
  FROM employees) WHERE r = 1 AND status = 'active'
ORDER BY 1, dept_id, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
before = pd.read_sql_query(SQL_MAIN, con)
after = pd.read_sql_query(SQL_AFTER, con)
top1 = pd.read_sql_query(SQL_TOP1, con)
print("SQL filter BEFORE the window (rank among active only):"); print(before.to_string(index=False))
print("\nSQL filter AFTER the window (rank among everyone, then hide 'left'):"); print(after.to_string(index=False))
print("\nTop-1 per department, both ways:"); print(top1.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
active = emp[emp["status"] == "active"].copy()
active["rnk_active"] = active.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("int64")
everyone = emp.copy()
everyone["rnk_all"] = everyone.groupby("dept_id")["salary"].rank(method="min", ascending=False).astype("int64")
after_pd = everyone[everyone["status"] == "active"]
# pd:end
# compared after sorting by emp_id
pd.testing.assert_frame_equal(
    before.sort_values("emp_id").reset_index(drop=True),
    active.drop(columns="status").sort_values("emp_id").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(
    after.sort_values("emp_id").reset_index(drop=True),
    after_pd.drop(columns="status").sort_values("emp_id").reset_index(drop=True), check_dtype=False)
diff = before.merge(after, on=["emp_id", "name", "dept_id", "salary"])
diff["same"] = diff["rnk_active"] == diff["rnk_all"]
print("\nSide by side (ranks differ for", int((~diff["same"]).sum()), "of", len(diff), "active employees):")
print(diff.sort_values("emp_id").to_string(index=False))
assert top1[top1["how"] == "filter first"]["emp_id"].tolist() == [1, 6]
assert top1[top1["how"] == "filter after"].empty
print("asserts passed: SQL == pandas for both orders; top-1 after the filter is empty")
