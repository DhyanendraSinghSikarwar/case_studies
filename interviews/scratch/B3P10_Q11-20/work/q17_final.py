# Q17: string aggregation with group_concat / string_agg, SQL versus pandas
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept TEXT, name TEXT);
INSERT INTO employees VALUES
 (1,'Eng','Zoya'),(2,'Eng','Asha'),(3,'Eng','Ben'),(4,'Eng','Asha'),(5,'Eng',NULL),
 (6,'Sales','Dev'),(7,'HR',NULL);
CREATE TABLE activities(sell_date TEXT, product TEXT);
INSERT INTO activities VALUES
 ('2020-05-30','Headphone'),('2020-06-01','Pencil'),('2020-06-02','Mask'),('2020-05-30','Basketball'),
 ('2020-06-01','Bible'),('2020-06-02','Mask'),('2020-05-30','T-Shirt');
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)

def run(sql):
    return pd.read_sql_query(sql, con)

# 1. plain group_concat: order inside the group is not guaranteed
print("\n1. GROUP_CONCAT(name, ', ') with no ORDER BY (order is whatever the scan gave):")
print(run("SELECT dept, GROUP_CONCAT(name, ', ') AS names FROM employees GROUP BY dept ORDER BY dept").to_string(index=False))

# 2. DISTINCT: only with the default separator
print("\n2. DISTINCT:")
print("   GROUP_CONCAT(DISTINCT name)       ->", run("SELECT GROUP_CONCAT(DISTINCT name) AS g FROM employees WHERE dept = 'Eng'")["g"][0])
try:
    run("SELECT GROUP_CONCAT(DISTINCT name, ', ') FROM employees")
except Exception as e:
    print("   GROUP_CONCAT(DISTINCT name, ', ') ->", type(e).__name__ + ":", e)

SQL_DEPT = """
SELECT dept, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM employees GROUP BY dept ORDER BY dept
"""
SQL_DEPT_DISTINCT = """
SELECT dept, GROUP_CONCAT(name, ', ' ORDER BY name) AS names
FROM (SELECT DISTINCT dept, name FROM employees)
GROUP BY dept ORDER BY dept
"""
SQL_DATES = """
SELECT sell_date,
       COUNT(DISTINCT product) AS num_sold,
       GROUP_CONCAT(product, ',' ORDER BY product) AS products
FROM (SELECT DISTINCT sell_date, product FROM activities)
GROUP BY sell_date ORDER BY sell_date
"""
SQL_STRING_AGG = """
SELECT dept, STRING_AGG(name, ', ' ORDER BY name) AS names
FROM employees GROUP BY dept ORDER BY dept
"""
SQL_OLD_TRICK = """
SELECT dept, GROUP_CONCAT(name, ', ') AS names
FROM (SELECT dept, name FROM employees ORDER BY name)
GROUP BY dept ORDER BY dept
"""
dept = run(SQL_DEPT)
dept_d = run(SQL_DEPT_DISTINCT)
dates = run(SQL_DATES)
sagg = run(SQL_STRING_AGG)
old = run(SQL_OLD_TRICK)
print("\n3. GROUP_CONCAT(name, ', ' ORDER BY name):"); print(dept.to_string(index=False))
print("   same with DISTINCT applied in a subquery:"); print(dept_d.to_string(index=False))
print("   per date, distinct products sorted (LeetCode 1484 shape):"); print(dates.to_string(index=False))
print("   STRING_AGG(name, ', ' ORDER BY name) equals GROUP_CONCAT version:", sagg.equals(dept))
print("   older subquery ORDER BY trick (no guarantee, but it happened to match here):", old.equals(dept))
one = con.execute("SELECT GROUP_CONCAT(DISTINCT name ORDER BY name) FROM employees WHERE dept='Eng'").fetchone()[0]
print("   GROUP_CONCAT(DISTINCT name ORDER BY name) (default ',') ->", one)

# 4. NULLs
print("\n4. NULL names are skipped; an all-NULL group returns NULL, not ''; Eng has 5 rows, 4 names:")
nul = run("SELECT dept, COUNT(*) AS rows_, COUNT(name) AS names_, GROUP_CONCAT(name, ', ' ORDER BY name) AS g, "
          "COALESCE(GROUP_CONCAT(name, ', ' ORDER BY name), '') AS g_or_empty FROM employees GROUP BY dept ORDER BY dept")
print(nul.to_string(index=False))
print("   NULL separator row-wise: 'a' || NULL ->", con.execute("SELECT 'a' || NULL").fetchone()[0],
      "| concat('a', NULL, 'b') ->", con.execute("SELECT concat('a', NULL, 'b')").fetchone()[0])

emp = pd.read_sql_query("SELECT * FROM employees", con)
acts = pd.read_sql_query("SELECT * FROM activities", con)
p_dept = (emp.groupby("dept")["name"]
             .agg(lambda s: ", ".join(sorted(s.dropna())))
             .rename("names").reset_index())
p_dept["names"] = p_dept["names"].replace("", None)        # SQL gives NULL for an all-NULL group
p_dates = (acts.groupby("sell_date")["product"]
               .agg(num_sold="nunique", products=lambda s: ",".join(sorted(set(s))))
               .reset_index())
print("\npandas groupby + join:"); print(p_dept.to_string(index=False)); print(p_dates.to_string(index=False))
try:
    emp.groupby("dept")["name"].agg(", ".join)
except TypeError as e:
    print("agg(', '.join) on a column with NaN -> TypeError:", e)
p_dist = (emp.groupby("dept")["name"].agg(lambda s: ", ".join(sorted(set(s.dropna())))).rename("names").reset_index())
p_dist["names"] = p_dist["names"].replace("", None)

# comparisons (ordered by dept / sell_date)
pd.testing.assert_frame_equal(p_dept, dept, check_dtype=False)
pd.testing.assert_frame_equal(p_dist, dept_d, check_dtype=False)
pd.testing.assert_frame_equal(p_dates, dates, check_dtype=False)
assert sagg.equals(dept)
print("asserts passed (SQL and pandas equal, ordered by dept / sell_date; the pandas '' became None for the all-NULL group)")
