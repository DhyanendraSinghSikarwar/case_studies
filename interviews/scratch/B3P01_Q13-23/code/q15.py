# Translate SQL to pandas (Q15) and assert the two results are identical (rows, order, dtypes).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER, hired TEXT);
INSERT INTO employees VALUES
 (1,'a1','Eng',100,'2021-03-01'),(2,'a2','Eng',140,'2022-05-10'),(3,'a3','Eng',120,'2020-01-01'),(4,'a4','Eng',NULL,'2023-01-01'),(5,'a5','Eng',500,'2019-12-31'),
 (6,'b1','Ops',60,'2020-06-01'),(7,'b2','Ops',80,'2021-01-01'),(8,'b3','Ops',70,'2024-02-02'),
 (9,'c1','HR',50,'2020-02-02'),(10,'c2','HR',55,'2022-02-02'),(11,'c3','HR',45,'2023-03-03'),(12,'c4','HR',90,'2018-01-01'),
 (13,'d1','Fin',200,'2021-01-01'),(14,'d2','Fin',210,'2021-02-01'),(15,'d3','Fin',190,'2021-03-01'),
 (16,'e1','Mkt',75,'2022-01-01'),(17,'e2','Mkt',85,'2022-02-01'),(18,'e3','Mkt',95,'2022-03-01'),
 (19,'f1','Sales',65,'2020-01-01'),(20,'f2','Sales',66,'2020-02-01'),(21,'f3','Sales',67,'2020-03-01'),
 (22,'g1','Legal',300,'2021-01-01'),(23,'g2','Legal',310,'2021-02-01');
""")

sql = """
SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_sal
FROM employees
WHERE salary IS NOT NULL AND hired >= '2020-01-01'
GROUP BY dept
HAVING COUNT(*) >= 3
ORDER BY avg_sal DESC
LIMIT 5
"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

emp = pd.read_sql("SELECT * FROM employees", con)

# version 1: boolean masks + named aggregation
mask = emp["salary"].notna() & (emp["hired"] >= "2020-01-01")
v1 = (emp[mask]
      .groupby("dept", as_index=False)
      .agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))
      .query("n >= 3")
      .sort_values("avg_sal", ascending=False)
      .head(5)
      .reset_index(drop=True))

# version 2: query() for the row filter, as_index=True then reset_index
v2 = (emp.query("salary.notna() and hired >= '2020-01-01'")
         .groupby("dept")
         .agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))
         .query("n >= 3")
         .sort_values("avg_sal", ascending=False)
         .head(5)
         .reset_index())
print(v1.dtypes.to_dict())
print(sql_df.dtypes.to_dict())

pd.testing.assert_frame_equal(sql_df, v1)
pd.testing.assert_frame_equal(sql_df, v2)
print("asserts passed: SQL == v1 == v2 (same rows, same order, same dtypes; no ties in avg_sal here)")

# what as_index=True does if you forget reset_index
g = emp[mask].groupby("dept").agg(n=("emp_id", "size"))
print("as_index=True: dept is the index ->", g.index.name, "| columns:", list(g.columns))

# how many rows got there before the limit
print("depts passing HAVING before LIMIT 5:", len(emp[mask].groupby("dept").filter(lambda x: len(x) >= 3)["dept"].unique()))
