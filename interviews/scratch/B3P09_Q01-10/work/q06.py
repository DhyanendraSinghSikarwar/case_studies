# Q6: level, path, indentation, root/leaf flags and a depth-first sort; padded sort key; queue order in SQLite
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, manager_id INTEGER, name TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1, NULL, 'Tim', 500), (2, 1, 'Radha', 300), (3, 1, 'Hari', 300), (4, 2, 'Asha', 100),
 (5, 3, 'Ben', 200), (6, 3, 'Chen', 200), (7, 5, 'Dev', 150), (8, 5, 'Esha', 150),
 (9, 6, 'Farid', 120), (10, 7, 'Gita', 100), (11, 7, 'Hugo', 100), (12, 10, 'Ivy', 90),
 (13, 99, 'Jay', 80),          -- orphan: never reached from the CEO
 (14, 1, 'Kim', 100);          -- id 14 sorts before 2 as text
"""
SQL_MAIN = """
WITH RECURSIVE t(emp_id, name, level, path, sortkey) AS (
  SELECT emp_id, name, 0, name, printf('%03d', emp_id)
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.level + 1, t.path || '/' || e.name, t.sortkey || '/' || printf('%03d', e.emp_id)
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE t.level < 20                                        -- depth guard
)
SELECT t.emp_id,
       printf('%*s', 2 * t.level, '') || t.name AS display_name,
       t.level, t.path,
       (t.level = 0) AS is_root,
       NOT EXISTS (SELECT 1 FROM employees x WHERE x.manager_id = t.emp_id) AS is_leaf
FROM t
ORDER BY t.sortkey
"""
SQL_QUEUE_DFS = """
WITH RECURSIVE t(emp_id, name, level, sortkey) AS (
  SELECT emp_id, name, 0, printf('%03d', emp_id) FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.level + 1, t.sortkey || '/' || printf('%03d', e.emp_id)
  FROM employees e JOIN t ON e.manager_id = t.emp_id
  ORDER BY 4                                               -- queue order: the smallest sortkey is taken next
)
SELECT name FROM t                                         -- no outer ORDER BY: order is whatever the queue gave
"""
SQL_NAIVE = """
WITH RECURSIVE t(emp_id, name, idpath) AS (
  SELECT emp_id, name, CAST(emp_id AS TEXT) FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.emp_id, e.name, t.idpath || '/' || e.emp_id FROM employees e JOIN t ON e.manager_id = t.emp_id
  WHERE length(t.idpath) < 60                              -- guard
)
SELECT name FROM t ORDER BY idpath
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
for r in sql_df.itertuples():
    print(f"{r.emp_id:>2} [{r.display_name:<14}] level={r.level} root={r.is_root} leaf={r.is_leaf} path={r.path}")

employees = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
edges = employees.dropna(subset=["manager_id"]).astype({"manager_id": "int64"})
cur = employees[employees["manager_id"].isna()].assign(level=0, path=lambda d: d["name"], sortkey=lambda d: d["emp_id"].map("{:03d}".format))
frames = [cur]
while not cur.empty and cur["level"].iloc[0] < 20:
    cur = (cur[["emp_id", "level", "path", "sortkey"]].rename(columns={"emp_id": "manager_id"})
           .merge(edges[["emp_id", "manager_id", "name"]], on="manager_id")
           .assign(level=lambda d: d["level"] + 1, path=lambda d: d["path"] + "/" + d["name"],
                   sortkey=lambda d: d["sortkey"] + "/" + d["emp_id"].map("{:03d}".format)))
    frames.append(cur)
t = pd.concat(frames, ignore_index=True)
t["display_name"] = ["  " * l + n for l, n in zip(t["level"], t["name"])]
t["is_root"] = (t["level"] == 0).astype(int)
t["is_leaf"] = (~t["emp_id"].isin(employees["manager_id"].dropna().astype(int))).astype(int)
pd_df = t.sort_values("sortkey")[["emp_id", "display_name", "level", "path", "is_root", "is_leaf"]].reset_index(drop=True)
# pd:end
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)        # both ordered by the padded sort key
print("pandas equals SQL (ordered by padded sort key)")

queue_order = [r[0] for r in con.execute(SQL_QUEUE_DFS)]
print("queue DFS (ORDER BY in recursive member):", queue_order)
assert queue_order == sql_df["display_name"].str.strip().tolist()
naive = [r[0] for r in con.execute(SQL_NAIVE)]
print("naive text sort of '1/14' vs '1/2':", naive[:4], "... differs from true DFS:", naive != queue_order)
assert naive != queue_order

# Edge cases
print("orphan Jay in output:", 13 in set(sql_df["emp_id"]), "| rows:", len(sql_df), "of", len(employees))
con.execute("UPDATE employees SET manager_id = NULL WHERE emp_id = 13")
print("after Jay becomes a second root:", len(pd.read_sql_query(SQL_MAIN, con)), "rows, roots:", int(pd.read_sql_query(SQL_MAIN, con)["is_root"].sum()))
print("asserts passed")
